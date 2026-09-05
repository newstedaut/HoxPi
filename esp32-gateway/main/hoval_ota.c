/*
 * hoval_ota.c — Firmware-Update per esp_https_ota (ESP-IDF >= 5.3) + Rollback-Wache. Siehe hoval_ota.h.
 * Noch NICHT auf Hardware getestet (05.09.2026, kein Board) — IDF-Aufrufe nur gegen test/idf_stubs/ geprueft.
 */
#include "hoval_ota.h"
#include "hoval_json.h"
#include "hoval_can.h"
#include <string.h>
#include <stdio.h>
#include <inttypes.h>
#include "esp_log.h"
#include "esp_err.h"
#include "esp_timer.h"
#include "esp_system.h"
#include "esp_ota_ops.h"
#include "esp_app_desc.h"
#include "esp_http_client.h"
#include "esp_https_ota.h"
#include "esp_crt_bundle.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "sdkconfig.h"

#ifndef CONFIG_HOXPI_OTA_ENABLE
#define CONFIG_HOXPI_OTA_ENABLE 1
#endif
#ifndef CONFIG_HOXPI_OTA_ALLOW_HTTP
#define CONFIG_HOXPI_OTA_ALLOW_HTTP 0
#endif
#ifndef CONFIG_HOXPI_OTA_VALID_AFTER_S
#define CONFIG_HOXPI_OTA_VALID_AFTER_S 600
#endif
#ifndef CONFIG_HOXPI_OTA_TIMEOUT_MS
#define CONFIG_HOXPI_OTA_TIMEOUT_MS 15000
#endif

static const char *TAG = "hoval_ota";

static volatile hota_state_t s_state = HOTA_IDLE;
static char     s_url[HOTA_URL_MAX];
static volatile uint32_t s_bytes;
static volatile int32_t  s_total = -1;
static char     s_err[96];
static uint32_t s_started_s, s_finished_s;

static uint32_t uptime_s(void) { return (uint32_t)(esp_timer_get_time() / 1000000); }

bool hota_enabled(void) { return CONFIG_HOXPI_OTA_ENABLE != 0; }

static void fail(const char *what, esp_err_t e)
{
    snprintf(s_err, sizeof s_err, "%s: %s", what, esp_err_to_name(e));
    ESP_LOGE(TAG, "Update fehlgeschlagen - %s (%" PRIu32 " Bytes geladen)", s_err, (uint32_t)s_bytes);
    s_finished_s = uptime_s();
    s_state = HOTA_FAILED;
}

static void restart_task(void *arg) { (void)arg; vTaskDelay(pdMS_TO_TICKS(1500)); esp_restart(); }

static void ota_task(void *arg)
{
    (void)arg;
    esp_http_client_config_t http = {
        .url = s_url,
        .timeout_ms = CONFIG_HOXPI_OTA_TIMEOUT_MS,
        .keep_alive_enable = true,
#if CONFIG_HOXPI_OTA_CERT_BUNDLE
        .crt_bundle_attach = esp_crt_bundle_attach,   /* Mozilla-Wurzelzertifikate aus der IDF (https) */
#endif
    };
    esp_https_ota_config_t cfg = { .http_config = &http };
    esp_https_ota_handle_t h = NULL;
    esp_err_t e = esp_https_ota_begin(&cfg, &h);
    if (e != ESP_OK) { fail("begin", e); vTaskDelete(NULL); return; }

    s_total = esp_https_ota_get_image_size(h);
    ESP_LOGI(TAG, "Update laeuft: %s (%" PRId32 " Bytes)", s_url, (int32_t)s_total);
    /* Header-Check gleich zu Beginn: gleiche Version noch einmal flashen ist erlaubt (bewusst), aber geloggt */
    esp_app_desc_t neu;
    if (esp_https_ota_get_img_desc(h, &neu) == ESP_OK) {
        const esp_app_desc_t *alt = esp_app_get_description();
        ESP_LOGI(TAG, "Image: %s %s (%s %s), laufend: %s", neu.project_name, neu.version, neu.date, neu.time, alt->version);
        if (strcmp(neu.project_name, alt->project_name) != 0) {
            esp_https_ota_abort(h);
            snprintf(s_err, sizeof s_err, "falsches Projekt: %s (erwartet %s)", neu.project_name, alt->project_name);
            ESP_LOGE(TAG, "%s", s_err);
            s_finished_s = uptime_s(); s_state = HOTA_FAILED;
            vTaskDelete(NULL); return;
        }
    }
    for (;;) {
        e = esp_https_ota_perform(h);
        s_bytes = (uint32_t)esp_https_ota_get_image_len_read(h);
        if (e != ESP_ERR_HTTPS_OTA_IN_PROGRESS) break;
    }
    if (e != ESP_OK) { esp_https_ota_abort(h); fail("perform", e); vTaskDelete(NULL); return; }
    if (!esp_https_ota_is_complete_data_received(h)) { esp_https_ota_abort(h); fail("unvollstaendig", ESP_FAIL); vTaskDelete(NULL); return; }
    e = esp_https_ota_finish(h);      /* prueft Image (Magic/SHA/Signatur je Config) und setzt die Boot-Partition */
    if (e != ESP_OK) { fail("finish", e); vTaskDelete(NULL); return; }

    s_finished_s = uptime_s();
    s_state = HOTA_OK;
    ESP_LOGW(TAG, "Update ok (%" PRIu32 " Bytes) - Neustart in 1,5 s; Rollback greift, wenn das neue Image binnen %d s keinen CAN-Datenpunkt dekodiert",
             (uint32_t)s_bytes, CONFIG_HOXPI_OTA_VALID_AFTER_S);
    xTaskCreate(restart_task, "hota_restart", 2048, NULL, 5, NULL);
    vTaskDelete(NULL);
}

bool hota_start(const char *url, char *err, size_t errcap)
{
    if (err && errcap) err[0] = 0;
    if (!hota_enabled()) { if (err) snprintf(err, errcap, "OTA deaktiviert (HOXPI_OTA_ENABLE)"); return false; }
    if (s_state == HOTA_RUNNING) { if (err) snprintf(err, errcap, "Update laeuft bereits"); return false; }
    char tmp[HOTA_URL_MAX];
    if (!hj_check_ota_url(url, CONFIG_HOXPI_OTA_ALLOW_HTTP != 0, tmp, sizeof tmp, err, errcap)) return false;
    strcpy(s_url, tmp);
    s_bytes = 0; s_total = -1; s_err[0] = 0;
    s_started_s = uptime_s(); s_finished_s = 0;
    s_state = HOTA_RUNNING;
    if (xTaskCreate(ota_task, "hota", 8192, NULL, 4, NULL) != pdPASS) {
        s_state = HOTA_FAILED; snprintf(s_err, sizeof s_err, "Task nicht angelegt");
        if (err) snprintf(err, errcap, "%s", s_err);
        return false;
    }
    return true;
}

static bool pending_verify(void)
{
    const esp_partition_t *run = esp_ota_get_running_partition();
    esp_ota_img_states_t st;
    return run && esp_ota_get_state_partition(run, &st) == ESP_OK && st == ESP_OTA_IMG_PENDING_VERIFY;
}

void hota_info(hota_info_t *o)
{
    memset(o, 0, sizeof *o);
    const esp_partition_t *run = esp_ota_get_running_partition();
    const esp_partition_t *boot = esp_ota_get_boot_partition();
    const esp_app_desc_t *d = esp_app_get_description();
    o->enabled = hota_enabled();
    o->running = run ? run->label : "?";
    o->boot = boot ? boot->label : "?";
    o->app_version = d->version;
    o->app_date = d->date;
    o->pending_verify = pending_verify();
    o->state = s_state;
    strcpy(o->url, s_url);
    o->bytes = s_bytes; o->total = s_total;
    o->error = s_err;
    o->started_s = s_started_s; o->finished_s = s_finished_s;
}

void hota_log_boot(void)
{
    hota_info_t i; hota_info(&i);
    ESP_LOGI(TAG, "App %s (%s) auf Partition %s, Boot %s, OTA %s%s", i.app_version, i.app_date, i.running, i.boot,
             i.enabled ? "an" : "aus", i.pending_verify ? " - NEUES IMAGE, wartet auf CAN-Bestaetigung" : "");
}

static void watch_task(void *arg)
{
    (void)arg;
    uint32_t t0 = uptime_s();
    for (;;) {
        vTaskDelay(pdMS_TO_TICKS(2000));
        if (hc_stats()->decoded > 0) {
            esp_err_t e = esp_ota_mark_app_valid_cancel_rollback();
            ESP_LOGW(TAG, "neues Image bestaetigt (CAN dekodiert nach %" PRIu32 " s): %s", uptime_s() - t0, esp_err_to_name(e));
            break;
        }
        if (uptime_s() - t0 > CONFIG_HOXPI_OTA_VALID_AFTER_S) {
            ESP_LOGE(TAG, "neues Image hat in %d s keinen CAN-Datenpunkt dekodiert - ROLLBACK auf die vorige Firmware",
                     CONFIG_HOXPI_OTA_VALID_AFTER_S);
            esp_ota_mark_app_invalid_rollback_and_reboot();   /* kehrt nicht zurueck */
            break;
        }
    }
    vTaskDelete(NULL);
}

void hota_watch(void)
{
    if (!pending_verify()) return;
    xTaskCreate(watch_task, "hota_watch", 3072, NULL, 3, NULL);
}
