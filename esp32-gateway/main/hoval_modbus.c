/*
 * hoval_modbus.c — Modbus-TCP-Slave auf esp-modbus (v1.x API), Registerkarte 1:1 wie HoxPi
 *
 * Speicher: je hp_area ein zusammenhaengender uint16-Puffer (Holding Register). Loxone liest
 * mit FC3 dieselben Registernummern wie beim Raspberry-HoxPi, die Templates passen unveraendert.
 *
 * Schreibpfad (FC6/FC16) = HovalBridge.on_write() in C:
 *   esp-modbus schreibt das Wort zuerst in den Puffer und meldet dann ein WR-Ereignis. Wir
 *   vergleichen den Puffer mit dem Schatten (letzter CAN-Stand), pruefen
 *     1) Whitelist  1b) Kalt-Cache (Register schon vom CAN gelesen)  2) min/max (S16-Sicht)
 *     3) Rate-Limit je Register  ->  SET-Frame; sonst Wort auf den Schattenwert zuruecksetzen.
 *   Kanal-Exklusion: aktiver Heiz-/Kuehl-Sollwert (>0) nullt den Partnerkanal (EXCL_PAIRS).
 *
 * Noch NICHT auf Hardware getestet (02.09.2026). API-Referenz: espressif/esp-modbus 1.0.x
 * (mbc_slave_init_tcp / mbc_slave_setup / mbc_slave_set_descriptor / mbc_slave_start /
 *  mbc_slave_check_event / mbc_slave_get_param_info). Fuer esp-modbus 2.x muessen die Aufrufe
 * auf die Handle-Variante umgestellt werden (siehe README).
 */
#include "hoval_modbus.h"
#include "hoval_proto.h"
#include "hoval_can.h"
#include <string.h>
#include <stdlib.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "esp_timer.h"
#include "esp_modbus_slave.h"
#include "sdkconfig.h"

static const char *TAG = "hoval_mb";

#ifndef CONFIG_HOXPI_MODBUS_PORT
#define CONFIG_HOXPI_MODBUS_PORT 502
#endif
#define WRITE_MIN_INTERVAL_MS   50      /* WRITE_MIN_INTERVAL = 0.05 s */
#define EXCL_MIN_INTERVAL_MS    2000    /* EXCL_MIN_INTERVAL  = 2.0 s  */

static uint16_t *s_buf[64];      /* Puffer je Bereich (max. 64 Bereiche; Generator liefert ~27) */
static uint16_t *s_shadow[64];   /* letzter CAN-Stand, um abgelehnte Writes zurueckzusetzen */
static bool      s_enable_write;
static uint32_t  s_last_write_ms[256]; static uint16_t s_last_write_reg[256]; /* kleiner Ring fuer Rate-Limit */
static uint32_t  s_excl_last_ms[8];  static uint16_t s_excl_last_reg[8];

static inline uint32_t now_ms(void) { return (uint32_t)(esp_timer_get_time() / 1000); }

static int area_of(uint16_t reg, uint16_t *off)
{
    for (uint16_t a = 0; a < hp_areas_count; a++)
        if (reg >= hp_areas[a].start && reg < hp_areas[a].start + hp_areas[a].count) {
            *off = (uint16_t)(reg - hp_areas[a].start); return a;
        }
    return -1;
}

void hm_store(uint16_t reg, uint16_t word)
{
    uint16_t off; int a = area_of(reg, &off);
    if (a < 0 || !s_buf[a]) return;
    s_buf[a][off] = word;          /* 16-bit-Schreiben ist auf ESP32 atomar */
    s_shadow[a][off] = word;
}

bool hm_read(uint16_t reg, uint16_t *word)
{
    uint16_t off; int a = area_of(reg, &off);
    if (a < 0 || !s_buf[a]) return false;
    *word = s_buf[a][off]; return true;
}

/* --- Rate-Limit-Helfer (kleine assoziative Ringe statt dict) --- */
static uint32_t *last_slot(uint32_t *ms, uint16_t *regs, size_t n, uint16_t reg)
{
    size_t free_i = n;
    for (size_t i = 0; i < n; i++) {
        if (regs[i] == reg) return &ms[i];
        if (regs[i] == 0 && free_i == n) free_i = i;
    }
    if (free_i == n) free_i = reg % n;     /* voll: verdraengen */
    regs[free_i] = reg; ms[free_i] = 0;
    return &ms[free_i];
}

/* Ein geschriebenes Wort pruefen und ggf. auf den CAN senden. Liefert true = akzeptiert. */
static bool handle_write(uint16_t reg, uint16_t word, uint32_t now)
{
    const hp_reg_t *r = hp_find_reg(reg);
    if (!r) return false;                                   /* Luecke im Bereich */
    if (!s_enable_write) { ESP_LOGW(TAG, "Schreiben deaktiviert - reg %u ignoriert", reg); return false; }
    if (!hp_in_whitelist(reg))     { ESP_LOGW(TAG, "ABGELEHNT reg %u: nicht in Whitelist", reg); return false; }
    if (!hc_seen(reg))             { ESP_LOGW(TAG, "ABGELEHNT reg %u: noch nie vom CAN gelesen (Cache kalt)", reg); return false; }
    int32_t chk = hp_check_value((hp_type_t)r->type, word);
    if (!(r->flags & HP_F_NO_RANGE) && !(r->min <= chk && chk <= r->max)) {
        ESP_LOGW(TAG, "ABGELEHNT reg %u: Wert %ld ausserhalb [%ld..%ld]", reg, (long)chk, (long)r->min, (long)r->max);
        return false;
    }
    uint32_t *lw = last_slot(s_last_write_ms, s_last_write_reg, 256, reg);
    if (*lw && now - *lw < WRITE_MIN_INTERVAL_MS) { ESP_LOGW(TAG, "ABGELEHNT reg %u: Rate-Limit", reg); return false; }
    *lw = now;
    if (!hc_send_set(r, word)) return false;

    /* Kanal-Exklusion Heizen <-> Kuehlen */
    uint16_t partner = hp_excl_partner(reg);
    if (partner && chk > 0) {
        uint32_t *el = last_slot(s_excl_last_ms, s_excl_last_reg, 8, partner);
        if (*el == 0 || now - *el >= EXCL_MIN_INTERVAL_MS) {
            const hp_reg_t *pr = hp_find_reg(partner);
            if (pr && hc_send_set(pr, 0)) {
                *el = now;
                *last_slot(s_last_write_ms, s_last_write_reg, 256, partner) = now;
                ESP_LOGI(TAG, "EXKLUSION: reg %u aktiv -> Partner reg %u auf 0", reg, partner);
            }
        }
    }
    return true;
}

bool hm_write(uint16_t reg, uint16_t word)
{
    uint16_t off; int a = area_of(reg, &off);
    if (a < 0 || !s_buf[a]) return false;
    if (!handle_write(reg, word, now_ms())) return false;
    s_buf[a][off] = word; s_shadow[a][off] = word;      /* wie ein akzeptierter Modbus-Write */
    return true;
}

/* Ereignis-Task: auf Schreibzugriffe warten, geaenderte Woerter gegen den Schatten finden */
static void mb_task(void *arg)
{
    (void)arg;
    for (;;) {
        mb_event_group_t ev = mbc_slave_check_event(MB_EVENT_HOLDING_REG_WR);
        if (!(ev & MB_EVENT_HOLDING_REG_WR)) continue;
        mb_param_info_t info;
        if (mbc_slave_get_param_info(&info, pdMS_TO_TICKS(100)) != ESP_OK) continue;
        uint32_t now = now_ms();
        /* Bereich ueber den Zeiger bestimmen (robust gegen Offset-Semantik der esp-modbus-Versionen) */
        for (uint16_t a = 0; a < hp_areas_count; a++) {
            uint16_t *base = s_buf[a];
            if (!base) continue;
            uint8_t *p = (uint8_t *)info.address, *b0 = (uint8_t *)base, *b1 = (uint8_t *)(base + hp_areas[a].count);
            if (p < b0 || p >= b1) continue;
            uint16_t first = (uint16_t)((p - b0) / 2);
            uint16_t n = (uint16_t)(info.size ? info.size : 1);
            for (uint16_t i = 0; i < n && first + i < hp_areas[a].count; i++) {
                uint16_t off = (uint16_t)(first + i), reg = (uint16_t)(hp_areas[a].start + off);
                uint16_t neu = base[off], alt = s_shadow[a][off];
                if (neu == alt) continue;               /* kein Wechsel (z. B. FC16 mit altem Wert) */
                if (handle_write(reg, neu, now)) s_shadow[a][off] = neu;
                else base[off] = alt;                   /* abgelehnt -> zurueck auf CAN-Stand */
            }
            break;
        }
    }
}

bool hm_start(void *netif, bool enable_write)
{
    s_enable_write = enable_write;
    if (hp_areas_count > 64) { ESP_LOGE(TAG, "zu viele Bereiche (%u > 64) - merge-gap erhoehen", hp_areas_count); return false; }
    size_t words = 0;
    for (uint16_t a = 0; a < hp_areas_count; a++) {
        s_buf[a]    = calloc(hp_areas[a].count, sizeof(uint16_t));
        s_shadow[a] = calloc(hp_areas[a].count, sizeof(uint16_t));
        if (!s_buf[a] || !s_shadow[a]) { ESP_LOGE(TAG, "kein RAM fuer Bereich %u", a); return false; }
        words += hp_areas[a].count;
    }

    void *handle = NULL;
    if (mbc_slave_init_tcp(&handle) != ESP_OK) { ESP_LOGE(TAG, "mbc_slave_init_tcp"); return false; }
    mb_communication_info_t comm = { 0 };
    comm.ip_port      = CONFIG_HOXPI_MODBUS_PORT;
    comm.ip_addr_type = MB_IPV4;
    comm.ip_mode      = MB_MODE_TCP;
    comm.ip_addr      = NULL;                 /* alle Clients zulassen (Loxone, Diagnose) */
    comm.ip_netif_ptr = netif;
    if (mbc_slave_setup(&comm) != ESP_OK) { ESP_LOGE(TAG, "mbc_slave_setup"); return false; }
    for (uint16_t a = 0; a < hp_areas_count; a++) {
        mb_register_area_descriptors_t d = { 0 };
        d.type = MB_PARAM_HOLDING;
        d.start_offset = hp_areas[a].start;
        d.address = s_buf[a];
        d.size = hp_areas[a].count * sizeof(uint16_t);
        if (mbc_slave_set_descriptor(d) != ESP_OK) { ESP_LOGE(TAG, "set_descriptor Bereich %u (%u+%u)", a, hp_areas[a].start, hp_areas[a].count); return false; }
    }
    if (mbc_slave_start() != ESP_OK) { ESP_LOGE(TAG, "mbc_slave_start"); return false; }
    xTaskCreate(mb_task, "hoval_mb", 4096, NULL, 6, NULL);
    ESP_LOGI(TAG, "Modbus-TCP :%d, %u Bereiche / %u Woerter (%u Register), Schreiben %s",
             CONFIG_HOXPI_MODBUS_PORT, hp_areas_count, (unsigned)words, hp_regs_count, enable_write ? "AN" : "AUS");
    return true;
}
