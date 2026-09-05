/*
 * hoval_json.h — JSON fuer die Statusseite (reines C, host-testbar; test/test_json.c)
 *
 * Erzeugt die Antworten von GET /status und GET|POST /config (hoval_http.c) und zerlegt den
 * POST-Body von /config. Bewusst ohne cJSON: die Bodies sind flach ({"poll_wez":60,
 * "whitelist":"1490,1497"}), ein kleiner Schluessel-Scanner reicht und laesst sich auf dem Host
 * mit gcc pruefen. Vorbild ist HoxPi: bridge_state.json (Warm-Cache/CAN-Zaehler), MCP get_status
 * (Kernwerte) und die Dashboard-Seite "Register" (Whitelist-Pflege).
 */
#ifndef HOVAL_JSON_H
#define HOVAL_JSON_H

#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include "hoval_cfg.h"

#ifdef __cplusplus
extern "C" {
#endif

/* Kernregister, die /status als "values" mitliefert (nur die, die in der Tabelle stehen) */
#define HJ_CORE_REGS  1501, 1534, 1477, 1525, 1535, 1500, 1499, 1537, 25611, 27490
#define HJ_CORE_N     10

/* Rohwort eines Registers lesen; *seen = schon einmal vom CAN empfangen. false = nicht in der Tabelle. */
typedef bool (*hj_read_cb_t)(uint16_t reg, uint16_t *word, bool *seen);

typedef struct {
    const char *version;            /* z. B. "esp32-0.4" */
    uint32_t uptime_s;
    uint32_t heap_free;
    /* CAN (hc_stats_t) */
    uint32_t rx_frames, rx_msgs, decoded, tx_frames, tx_errors, bus_off;
    bool     have_rx;               /* schon ein Datenpunkt dekodiert? */
    uint32_t last_rx_age_s;         /* Sekunden seit dem letzten dekodierten Datenpunkt */
    /* Modbus */
    uint16_t modbus_port;
    bool     write_enabled;         /* wirksam (beim Start uebernommen) */
    /* Tabelle */
    uint16_t regs_count, areas_count;
    /* Konfiguration */
    const hcfg_t *cfg;
    uint16_t wl_active_n;           /* aktive Whitelist-Laenge (Kompilat oder NVS) */
    bool     restart_required;      /* wr_en im NVS != wirksamer Schreibpfad */
    /* MQTT (hmq_stats_t); mqtt_enabled = URI konfiguriert. Bei false nur {"enabled":false}. */
    bool     mqtt_enabled, mqtt_connected;
    uint32_t mqtt_pub_ok, mqtt_pub_fail, mqtt_cmd_ok, mqtt_cmd_rej;
} hj_status_in_t;

/* Gesamtstatus als JSON. read darf NULL sein (dann ohne "values"). Liefert Laenge ohne NUL;
 * bei zu kleinem Puffer wird abgeschnitten (Rueckgabe >= cap zeigt das an). */
size_t hj_status_json(char *out, size_t cap, const hj_status_in_t *in, hj_read_cb_t read);

/* Konfiguration als JSON (Poll-Werte, Schreibfreigabe, Whitelist als Liste + Text, Herkunft je Wert). */
size_t hj_config_json(char *out, size_t cap, const hcfg_t *c, uint16_t wl_active_n, bool write_effective,
                      bool restart_required);

/* Einzelnes Register: Rohwort + Tabellenzeile. false wenn reg unbekannt (out enthaelt dann {"error":...}). */
bool   hj_register_json(char *out, size_t cap, uint16_t reg, hj_read_cb_t read);

/* POST-Body von /config auf eine Konfigurations-KOPIE anwenden. Erkannte Schluessel:
 *   poll_wez / poll_hv / poll_delay (Zahl), wr_en (0/1/true/false),
 *   whitelist ("1490,1497" ODER [1490,1497]; leer = nichts schreibbar).
 * Rueckgabe: Bitmaske HCFG_SRC_* der geaenderten Werte (0 = kein bekannter Schluessel),
 * -1 bei Fehler (err erklaert; Konfiguration dann unveraendert). */
int    hj_parse_config(const char *body, hcfg_t *c, char *err, size_t errcap);

#ifdef __cplusplus
}
#endif
#endif /* HOVAL_JSON_H */
