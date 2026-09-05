/*
 * hoval_ha.h — Home-Assistant-Sicht auf die Registerkarte (reines C, host-testbar; test/test_ha.c)
 *
 * Portierung von mqtt/hoval_mqtt.py: dieselben Entities (Sensoren, number/select-Steuerungen),
 * dieselben Klartexte (HK-/WW-/SG-/WEZ-Status, Fehlercode 1534), dieselben Sonderregeln
 * (Kaeltekreis-Sentinel-Gruppe, Ruecklauf-Fallback 31894/31895, Leistungs-Sollwert -127 = unknown,
 * COP 31667 mit FA-Fallback 27490 + Startfilter, Kuehl-Wartezustand 15c) und dieselben Topics:
 *
 *     hoval/<key>/state            Zustand (Zahl, Klartext oder "unknown")           retain
 *     hoval/<key>/raw              Rohwert zu Enum-Sensoren                          retain
 *     hoval/<key>/set              Kommando (HA -> Gateway), nur Steuer-Entities
 *     hoval/bridge/status          online/offline (LWT)                              retain
 *     hoval/stale/state|attr       Verfuegbarkeits-Alarm (kein Datenpunkt seit n min)
 *     hoval/kuehl_wartet/state|attr  Backlog 15c
 *     homeassistant/<sensor|number|select|binary_sensor>/hoxpi/<key>/config   Auto-Discovery
 *
 * Damit landen ESP32 und Raspberry-HoxPi unter derselben HA-Geraetekennung "hoxpi" — beide
 * gleichzeitig betreiben wuerde die Entities ueberschreiben (HA_DEVICE_ID anpassen).
 *
 * Dieses Modul kennt kein MQTT und kein ESP-IDF: es formt nur Topics, Payloads und Kommandos.
 * Registerzugriff ueber einen Lese-Callback (Rohwort + "schon einmal vom CAN gesehen").
 */
#ifndef HOVAL_HA_H
#define HOVAL_HA_H

#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

#define HA_BASE        "hoval"                    /* BASE in hoval_mqtt.py */
#define HA_AVAIL       HA_BASE "/bridge/status"   /* AVAIL */
#define HA_DEVICE_ID   "hoxpi"
#define HA_TOPIC_MAX   96
#define HA_STATE_MAX   48
#define HA_KUEHL_START_MIN_VL_X10  195            /* 19,5 °C, Vorlauf 1525 (Backlog #15b/15c) */
#define HA_INVALID_SETPOINT_RAW    (-1270)        /* 18767: -127,0 = kein gueltiger Sollwert */

typedef enum { HA_SENSOR = 0, HA_NUMBER, HA_SELECT } ha_kind_t;

typedef struct { int32_t val; const char *txt; } ha_enum_t;

typedef struct {
    const char     *key;        /* Topic-Teil + unique_id-Suffix */
    uint16_t        reg;        /* Modbus-Register (Hoval-Nummerierung) */
    const char     *name;       /* HA-Anzeigename */
    const char     *unit;       /* unit_of_measurement oder NULL */
    const char     *dev_class;  /* device_class oder NULL (dann auch kein state_class) */
    const ha_enum_t *en;        /* Klartext-Tabelle oder NULL */
    uint8_t         en_n;
    uint8_t         kind;       /* ha_kind_t */
} ha_ent_t;

extern const ha_ent_t ha_sensors[];   extern const uint8_t ha_sensors_n;
extern const ha_ent_t ha_controls[];  extern const uint8_t ha_controls_n;

/* Rohwort eines Registers lesen; *seen = schon vom CAN empfangen. false = nicht in der Tabelle. */
typedef bool (*ha_read_cb_t)(uint16_t reg, uint16_t *word, bool *seen);

/* ---- Topics ---------------------------------------------------------------- */
/* homeassistant/<art>/hoxpi/<key>/config bzw. hoval/<key>/<suffix> ; Rueckgabe = out */
const char *ha_topic_discovery(char *out, size_t cap, const char *art, const char *key);
const char *ha_topic_state(char *out, size_t cap, const char *key, const char *suffix);
const char *ha_kind_str(ha_kind_t k);   /* "sensor" / "number" / "select" */

/* ---- Discovery-Payloads (retain) ------------------------------------------- */
/* Sensor / number / select. false = Register nicht in der Tabelle (Entity dann auslassen). */
bool   ha_discovery_json(char *out, size_t cap, const ha_ent_t *e);
/* Die beiden binary_sensors (stale = ohne availability_topic, kuehl_wartet = mit) */
size_t ha_discovery_stale_json(char *out, size_t cap);
size_t ha_discovery_kuehl_json(char *out, size_t cap);
/* COP-Sensor (eigene Regel, kein Tabellen-Register) */
size_t ha_discovery_cop_json(char *out, size_t cap);

/* ---- Zustaende --------------------------------------------------------------- */
/* Zustand einer Entity als Text (Zahl mit Dezimalen, Klartext oder "unknown").
 * raw_out: bei Enum-Sensoren der Rohwert fuer hoval/<key>/raw (sonst unveraendert), have_raw sagt ob.
 * false = Register unbekannt oder nie gelesen -> nichts publizieren. */
bool   ha_state(const ha_ent_t *e, ha_read_cb_t read, char *out, size_t cap, int32_t *raw_out, bool *have_raw);
/* COP: 31667/31668 (S32, 0,1) sonst FA-COP 27490 (U8, 0,1); Pel 25611 < 0,5 kW -> 0; nur 0..20. false = nichts. */
bool   ha_cop_state(ha_read_cb_t read, char *out, size_t cap);
/* Kuehl-Wartezustand: Phase 0..3 (-1 = Register fehlen); vl_x10 = Vorlauf 1525 in 0,1 °C oder INT32_MIN */
int    ha_kuehl_phase(ha_read_cb_t read, int32_t *vl_x10);
const char *ha_kuehl_phase_txt(int phase);
size_t ha_kuehl_attr_json(char *out, size_t cap, int phase, int32_t vl_x10);
/* Stale-Attribute wie hoval_mqtt.py (age_s, reason, stale_min) */
size_t ha_stale_attr_json(char *out, size_t cap, uint32_t age_s, bool have_rx, unsigned stale_min);
/* Fehlercode 1534 -> "OK" / "kein Wert" / "B:02 Niederdruck" ... (FEHLER_ENUM) */
const char *ha_fehler_text(uint16_t raw, char *out, size_t cap);
/* Dezimalzahl mit dec Nachkommastellen (ohne float, "-3.2" / "46" / "0.05") */
size_t ha_fmt_scaled(char *out, size_t cap, int32_t raw, int dec);

/* ---- Kommandos (hoval/<key>/set) ------------------------------------------- */
/* Steuer-Entity zum Topic-Schluessel; NULL wenn unbekannt */
const ha_ent_t *ha_find_control(const char *key);
/* Payload -> Rohwort. select: Klartext muss in der Tabelle stehen; number: Dezimalzahl,
 * mit den Dezimalen des Registers skaliert, gerundet, als 16-bit-Wort (S16-Wrap).
 * Liefert 0 = ok, -1 = Payload unbrauchbar, -2 = Register nicht in der Tabelle. */
int    ha_command(const ha_ent_t *e, const char *payload, uint16_t *word);
/* Aktive Whitelist-Mitgliedschaft (Steuer-Entities werden nur dann angelegt) */
bool   ha_control_enabled(const ha_ent_t *e);

#ifdef __cplusplus
}
#endif
#endif /* HOVAL_HA_H */
