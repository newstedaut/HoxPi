/*
 * hoval_can.c — TWAI-Anbindung an den Hoval-TopTronic-E-Bus (50 kbit/s, 29-bit-IDs)
 *
 * Aufgaben (Gegenstueck zu HovalBridge.rx_loop/poll_targets in hoval_bridge.py):
 *   RX-Task  : Frames empfangen -> hp_reasm_feed -> Antwort zerlegen -> dekodieren -> store()
 *   Poll-Task: alle Tabellenzeilen zyklisch per GET abfragen (WEZ alle POLL_S Sekunden,
 *              HomeVent alle 5 s), Sendeabstand POLL_DELAY_MS, Bus-Off-Recovery
 *
 * Noch NICHT auf Hardware getestet (Stand 02.09.2026, kein Board vorhanden). Pins/Bitrate via Kconfig.
 */
#include "hoval_can.h"
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"
#include "driver/twai.h"
#include "esp_log.h"
#include "esp_timer.h"
#include "sdkconfig.h"

static const char *TAG = "hoval_can";

#ifndef CONFIG_HOXPI_CAN_TX_GPIO
#define CONFIG_HOXPI_CAN_TX_GPIO 5
#endif
#ifndef CONFIG_HOXPI_CAN_RX_GPIO
#define CONFIG_HOXPI_CAN_RX_GPIO 35
#endif
#ifndef CONFIG_HOXPI_POLL_INTERVAL_S
#define CONFIG_HOXPI_POLL_INTERVAL_S 30
#endif
#ifndef CONFIG_HOXPI_POLL_DELAY_MS
#define CONFIG_HOXPI_POLL_DELAY_MS 100
#endif

static hc_store_cb_t s_store;
static hc_stats_t    s_stats;
static hp_reasm_t    s_reasm;
static uint8_t       s_seen[8192];         /* 65536 Register als Bitmap = 8 KB */
static SemaphoreHandle_t s_tx_lock;

static inline uint32_t now_ms(void) { return (uint32_t)(esp_timer_get_time() / 1000); }
static inline void seen_set(uint16_t reg) { s_seen[reg >> 3] |= (uint8_t)(1u << (reg & 7)); }
bool hc_seen(uint16_t reg) { return (s_seen[reg >> 3] >> (reg & 7)) & 1u; }
const hc_stats_t *hc_stats(void) { return &s_stats; }

/* ---- vollstaendige Nachricht -> Register ---- */
static void on_msg(const uint8_t *raw, size_t len, void *ctx)
{
    (void)ctx;
    uint8_t fg, fn; uint16_t dp; const uint8_t *val; size_t vlen;
    if (!hp_parse_answer(raw, len, &fg, &fn, &dp, &val, &vlen)) return;
    const hp_reg_t *rows[4];
    size_t n = hp_find_by_dp(fg, fn, dp, rows, 4);
    for (size_t i = 0; i < n; i++) {
        int32_t v; uint16_t w[2];
        if (!hp_decode((hp_type_t)rows[i]->type, val, vlen, &v)) continue;
        size_t k = hp_to_regs((hp_type_t)rows[i]->type, v, w);
        for (size_t j = 0; j < k; j++) {
            s_store((uint16_t)(rows[i]->reg + j), w[j]);
            seen_set((uint16_t)(rows[i]->reg + j));
        }
        s_stats.decoded++;
        s_stats.last_rx_ms = now_ms();
    }
}

static void rx_task(void *arg)
{
    (void)arg;
    twai_message_t m;
    for (;;) {
        if (twai_receive(&m, pdMS_TO_TICKS(1000)) != ESP_OK) {
            twai_status_info_t st;
            if (twai_get_status_info(&st) == ESP_OK && st.state == TWAI_STATE_BUS_OFF) {
                s_stats.bus_off++;
                ESP_LOGW(TAG, "Bus-Off -> Recovery");
                twai_initiate_recovery();
                vTaskDelay(pdMS_TO_TICKS(500));
                twai_start();
            }
            continue;
        }
        if (!m.extd || m.rtr) continue;             /* Hoval nutzt nur Extended-Datenframes */
        s_stats.rx_frames++;
        hp_reasm_feed(&s_reasm, m.identifier, m.data, m.data_length_code, now_ms(), on_msg, NULL);
        s_stats.rx_msgs = s_reasm.rx_msgs;
    }
}

/* ---- Senden ---- */
static bool tx(uint32_t arb, const uint8_t *d, size_t n)
{
    twai_message_t m = { 0 };
    m.extd = 1; m.identifier = arb; m.data_length_code = (uint8_t)n;
    memcpy(m.data, d, n);
    xSemaphoreTake(s_tx_lock, portMAX_DELAY);
    esp_err_t e = twai_transmit(&m, pdMS_TO_TICKS(200));
    xSemaphoreGive(s_tx_lock);
    if (e != ESP_OK) { s_stats.tx_errors++; return false; }
    s_stats.tx_frames++;
    return true;
}

bool hc_send_set(const hp_reg_t *r, int32_t value)
{
    uint8_t f[8];
    size_t n = hp_build_set(r->fg, r->fn, r->dp, (hp_type_t)r->type, value, f);
    bool ok = tx(hp_arb_for(r->unit_id, true), f, n);
    ESP_LOGI(TAG, "SET reg %u (%u-%u-%u) <- %ld %s", r->reg, r->fg, r->fn, r->dp, (long)value, ok ? "" : "FEHLER");
    return ok;
}

/* ---- Poll: eine Runde ueber alle Zeilen einer Einheit; (fg,fn,dp) nur einmal je Runde ---- */
static void poll_round(uint16_t unit_id)
{
    uint8_t f[8];
    uint32_t arb = hp_arb_for(unit_id, false);
    for (uint16_t i = 0; i < hp_regs_count; i++) {
        const hp_reg_t *r = &hp_regs[i];
        if (r->unit_id != unit_id || (r->flags & HP_F_LOW_HALF)) continue;
        /* Duplikate (gleiche fg/fn/dp weiter vorne) ueberspringen */
        bool dup = false;
        for (uint16_t j = 0; j < i; j++)
            if (hp_regs[j].unit_id == unit_id && hp_regs[j].fg == r->fg && hp_regs[j].fn == r->fn && hp_regs[j].dp == r->dp) { dup = true; break; }
        if (dup) continue;
        size_t n = hp_build_get(r->fg, r->fn, r->dp, f);
        tx(arb, f, n);
        vTaskDelay(pdMS_TO_TICKS(CONFIG_HOXPI_POLL_DELAY_MS));
    }
}

static void poll_wez_task(void *arg)
{
    (void)arg;
    /* wie hoval_bridge.build_targets(): nur WEZ (UnitId 1) und HomeVent (520); das Puffermodul
     * (143) wird von HoxPi nicht gepollt - seine Datenpunkte antworten ohne PS-Modul ohnehin nie */
    for (;;) { poll_round(HP_UNIT_WEZ); vTaskDelay(pdMS_TO_TICKS(CONFIG_HOXPI_POLL_INTERVAL_S * 1000)); }
}

static void poll_hv_task(void *arg)
{
    (void)arg;
    for (;;) { poll_round(HP_UNIT_HV); vTaskDelay(pdMS_TO_TICKS(5000)); }
}

bool hc_start(hc_store_cb_t store)
{
    s_store = store;
    hp_reasm_init(&s_reasm);
    memset(s_seen, 0, sizeof s_seen);
    s_tx_lock = xSemaphoreCreateMutex();

    twai_general_config_t g = TWAI_GENERAL_CONFIG_DEFAULT(CONFIG_HOXPI_CAN_TX_GPIO, CONFIG_HOXPI_CAN_RX_GPIO, TWAI_MODE_NORMAL);
    g.rx_queue_len = 64; g.tx_queue_len = 16;
    twai_timing_config_t t = TWAI_TIMING_CONFIG_50KBITS();
    twai_filter_config_t f = TWAI_FILTER_CONFIG_ACCEPT_ALL();
    if (twai_driver_install(&g, &t, &f) != ESP_OK) { ESP_LOGE(TAG, "twai_driver_install fehlgeschlagen"); return false; }
    if (twai_start() != ESP_OK) { ESP_LOGE(TAG, "twai_start fehlgeschlagen"); return false; }
    ESP_LOGI(TAG, "TWAI 50 kbit/s, TX GPIO %d, RX GPIO %d, %u Register", CONFIG_HOXPI_CAN_TX_GPIO, CONFIG_HOXPI_CAN_RX_GPIO, hp_regs_count);

    xTaskCreate(rx_task, "hoval_rx", 4096, NULL, 10, NULL);
    xTaskCreate(poll_wez_task, "hoval_poll", 3072, NULL, 5, NULL);
    bool has_hv = false;
    for (uint16_t i = 0; i < hp_regs_count; i++) if (hp_regs[i].unit_id == HP_UNIT_HV) { has_hv = true; break; }
    if (has_hv) xTaskCreate(poll_hv_task, "hoval_poll_hv", 3072, NULL, 5, NULL);
    return true;
}
