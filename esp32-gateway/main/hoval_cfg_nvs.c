/*
 * hoval_cfg_nvs.c — NVS-Anbindung der Laufzeit-Konfiguration (ESP-IDF nvs.h).
 *
 * Namespace HCFG_NS ("hoxpi"), Schluessel siehe hoval_cfg.h. Fehlende Schluessel lassen den
 * Kompilat-Default stehen; ungueltige Werte werden mit Warnung ignoriert. Befuellen ohne Board:
 *   python3 tools/gen_esp32_nvs.py -w whitelist.json --poll-wez 30 -o nvs_config.csv
 *   python3 $IDF_PATH/components/nvs_flash/nvs_partition_generator/nvs_partition_gen.py generate nvs_config.csv nvs.bin 0x6000
 *   esptool.py write_flash 0x9000 nvs.bin        (Offset/Groesse der nvs-Partition aus der Partitionstabelle)
 * Noch NICHT auf Hardware getestet (03.09.2026, kein Board) — nur Stub-Syntaxpruefung (test/make syntax).
 */
#include "hoval_cfg.h"
#include <stdlib.h>
#include <string.h>
#include "nvs_flash.h"
#include "nvs.h"
#include "esp_log.h"

static const char *TAG = "hoval_cfg";

static void load_u16(nvs_handle_t h, hcfg_t *c, const char *key)
{
    uint16_t v;
    esp_err_t e = nvs_get_u16(h, key, &v);
    if (e == ESP_ERR_NVS_NOT_FOUND) return;
    if (e != ESP_OK) { ESP_LOGW(TAG, "NVS %s: Lesefehler 0x%x", key, (unsigned)e); return; }
    if (!hcfg_set(c, key, v)) ESP_LOGW(TAG, "NVS %s=%u ausserhalb der Grenzen - ignoriert", key, (unsigned)v);
    else ESP_LOGI(TAG, "NVS %s = %u", key, (unsigned)v);
}

bool hcfg_nvs_load(hcfg_t *c)
{
    nvs_handle_t h;
    esp_err_t e = nvs_open(HCFG_NS, NVS_READONLY, &h);
    if (e == ESP_ERR_NVS_NOT_FOUND) { ESP_LOGI(TAG, "kein NVS-Namespace '%s' - Kompilat-Defaults", HCFG_NS); return true; }
    if (e != ESP_OK) { ESP_LOGW(TAG, "nvs_open(%s) 0x%x - Kompilat-Defaults", HCFG_NS, (unsigned)e); return false; }

    load_u16(h, c, HCFG_KEY_POLL_WEZ);
    load_u16(h, c, HCFG_KEY_POLL_HV);
    load_u16(h, c, HCFG_KEY_POLL_DELAY);

    uint8_t v8;
    e = nvs_get_u8(h, HCFG_KEY_WR_EN, &v8);
    if (e == ESP_OK) {
        if (!hcfg_set(c, HCFG_KEY_WR_EN, v8)) ESP_LOGW(TAG, "NVS %s=%u ungueltig (0/1) - ignoriert", HCFG_KEY_WR_EN, (unsigned)v8);
        else ESP_LOGI(TAG, "NVS %s = %u", HCFG_KEY_WR_EN, (unsigned)v8);
    } else if (e != ESP_ERR_NVS_NOT_FOUND) ESP_LOGW(TAG, "NVS %s: Lesefehler 0x%x", HCFG_KEY_WR_EN, (unsigned)e);

    size_t len = 0;
    e = nvs_get_str(h, HCFG_KEY_WHITELIST, NULL, &len);
    if (e == ESP_OK) {
        if (len == 0 || len > HCFG_WL_TEXT_MAX + 1) {
            ESP_LOGW(TAG, "NVS %s: Laenge %u unbrauchbar - kompilierte Liste bleibt", HCFG_KEY_WHITELIST, (unsigned)len);
        } else {
            char *s = malloc(len);
            if (s && nvs_get_str(h, HCFG_KEY_WHITELIST, s, &len) == ESP_OK) {
                int n = hcfg_set_whitelist_text(c, s);
                if (n == -1)      ESP_LOGW(TAG, "NVS %s: Syntaxfehler in '%s' - kompilierte Liste bleibt", HCFG_KEY_WHITELIST, s);
                else if (n == -2) ESP_LOGW(TAG, "NVS %s: mehr als %d Eintraege - kompilierte Liste bleibt", HCFG_KEY_WHITELIST, HCFG_WL_MAX);
                else              ESP_LOGI(TAG, "NVS %s = %d Register", HCFG_KEY_WHITELIST, n);
            } else ESP_LOGW(TAG, "NVS %s: Lesefehler", HCFG_KEY_WHITELIST);
            free(s);
        }
    } else if (e != ESP_ERR_NVS_NOT_FOUND) ESP_LOGW(TAG, "NVS %s: Lesefehler 0x%x", HCFG_KEY_WHITELIST, (unsigned)e);

    nvs_close(h);
    return true;
}

bool hcfg_nvs_save(const hcfg_t *c)
{
    nvs_handle_t h;
    if (nvs_open(HCFG_NS, NVS_READWRITE, &h) != ESP_OK) { ESP_LOGE(TAG, "nvs_open(%s, rw) fehlgeschlagen", HCFG_NS); return false; }
    bool ok = true;
    ok &= nvs_set_u16(h, HCFG_KEY_POLL_WEZ,   c->poll_wez_s)    == ESP_OK;
    ok &= nvs_set_u16(h, HCFG_KEY_POLL_HV,    c->poll_hv_s)     == ESP_OK;
    ok &= nvs_set_u16(h, HCFG_KEY_POLL_DELAY, c->poll_delay_ms) == ESP_OK;
    ok &= nvs_set_u8 (h, HCFG_KEY_WR_EN,      c->enable_write ? 1 : 0) == ESP_OK;
    if (c->wl_override) {
        char buf[HCFG_WL_TEXT_MAX + 1];
        hcfg_format_whitelist(c->wl, c->wl_n, buf, sizeof buf);
        ok &= nvs_set_str(h, HCFG_KEY_WHITELIST, buf) == ESP_OK;
    } else {
        esp_err_t e = nvs_erase_key(h, HCFG_KEY_WHITELIST);      /* zurueck auf Kompilat */
        ok &= (e == ESP_OK || e == ESP_ERR_NVS_NOT_FOUND);
    }
    ok &= nvs_commit(h) == ESP_OK;
    nvs_close(h);
    ESP_LOGI(TAG, "NVS gespeichert: %s", ok ? "ok" : "FEHLER");
    return ok;
}

bool hcfg_nvs_reset(void)
{
    nvs_handle_t h;
    if (nvs_open(HCFG_NS, NVS_READWRITE, &h) != ESP_OK) return false;
    bool ok = nvs_erase_all(h) == ESP_OK && nvs_commit(h) == ESP_OK;
    nvs_close(h);
    return ok;
}
