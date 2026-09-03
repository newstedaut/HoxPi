/*
 * hoval_cfg.h — Laufzeit-Konfiguration des Gateways (Poll-Intervalle, Schreibfreigabe, Whitelist)
 *
 * Gegenstueck zu HoxPi: dort steuern hoxpi.json / whitelist.json die Bridge ohne Neubau. Auf dem ESP32
 * liegen dieselben Werte im NVS (Namespace "hoxpi"); fehlt ein Schluessel, gilt das Kompilat
 * (Kconfig bzw. hp_whitelist[] aus regmap_gen.h). Reihenfolge beim Start:
 *     hcfg_defaults()  ->  hcfg_nvs_load()  ->  hcfg_apply()
 *
 * Dieses Modul ist (bis auf hoval_cfg_nvs.c) reines C ohne ESP-IDF, damit test/test_cfg.c es auf dem
 * Host prueft. NVS-Schluessel (alle im Namespace HCFG_NS):
 *     poll_wez   u16  Sekunden zwischen zwei WEZ-Runden        (5..3600, Kconfig-Default 30)
 *     poll_hv    u16  Sekunden zwischen zwei HomeVent-Runden   (1..3600, Default 5)
 *     poll_delay u16  Millisekunden zwischen zwei GET-Frames   (10..2000, Default 100)
 *     wr_en      u8   0/1 Schreibpfad Modbus -> CAN            (Default Kconfig HOXPI_ENABLE_WRITE)
 *     whitelist  str  "1490,1497,27509" — Register, die Modbus-Clients schreiben duerfen.
 *                     Schluessel vorhanden = ersetzt die kompilierte Liste (auch wenn leer = nichts
 *                     schreibbar); Schluessel fehlt = kompilierte Liste. Unbekannte Register werden
 *                     beim Anwenden verworfen (Frame nicht baubar), nicht-schreibbare nur gemeldet
 *                     (HoxPi prueft ebenfalls nur die Mitgliedschaft, siehe current_whitelist()).
 * Erzeugen ohne Board: tools/gen_esp32_nvs.py -> CSV -> nvs_partition_gen.py -> esptool write_flash.
 */
#ifndef HOVAL_CFG_H
#define HOVAL_CFG_H

#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

#define HCFG_NS             "hoxpi"
#define HCFG_KEY_POLL_WEZ   "poll_wez"
#define HCFG_KEY_POLL_HV    "poll_hv"
#define HCFG_KEY_POLL_DELAY "poll_delay"
#define HCFG_KEY_WR_EN      "wr_en"
#define HCFG_KEY_WHITELIST  "whitelist"

#define HCFG_WL_MAX         128     /* Whitelist-Eintraege zur Laufzeit (HoxPi-Liste: 25) */
#define HCFG_WL_TEXT_MAX    1024    /* laengste akzeptierte Whitelist-Zeichenkette (NVS-Strings: max 4000) */

/* Grenzen (inklusive) */
#define HCFG_POLL_WEZ_MIN   5
#define HCFG_POLL_WEZ_MAX   3600
#define HCFG_POLL_HV_MIN    1
#define HCFG_POLL_HV_MAX    3600
#define HCFG_POLL_DELAY_MIN 10
#define HCFG_POLL_DELAY_MAX 2000

/* Herkunft je Wert (Bitmaske in hcfg_t.from_nvs) */
#define HCFG_SRC_POLL_WEZ   0x01u
#define HCFG_SRC_POLL_HV    0x02u
#define HCFG_SRC_POLL_DELAY 0x04u
#define HCFG_SRC_WR_EN      0x08u
#define HCFG_SRC_WHITELIST  0x10u

typedef struct {
    uint16_t poll_wez_s;
    uint16_t poll_hv_s;
    uint16_t poll_delay_ms;
    bool     enable_write;
    bool     wl_override;           /* true: wl[]/wl_n gilt statt hp_whitelist[] */
    uint16_t wl_n;
    uint16_t wl[HCFG_WL_MAX];
    uint8_t  from_nvs;              /* HCFG_SRC_* — nur Info fuers Log/Statusseite */
} hcfg_t;

/* Kompilat-Defaults setzen (Werte ausserhalb der Grenzen werden eingeklemmt). */
void hcfg_defaults(hcfg_t *c, unsigned poll_wez_s, unsigned poll_hv_s, unsigned poll_delay_ms, bool enable_write);

/* Einen Zahlenwert per Schluessel setzen (poll_wez/poll_hv/poll_delay/wr_en); false = Schluessel
 * unbekannt oder Wert ausserhalb der Grenzen (dann bleibt der alte Wert stehen). */
bool hcfg_set(hcfg_t *c, const char *key, long value);

/* "1490, 1497;27509" -> Register (Duplikate entfernt, Reihenfolge erhalten).
 * Liefert Anzahl, -1 bei Syntaxfehler (Nicht-Ziffer, Wert > 65535, Text zu lang), -2 bei mehr als max Eintraegen. */
int    hcfg_parse_whitelist(const char *text, uint16_t *out, size_t max);
/* Umkehrung: "1490,1497,27509". Liefert Laenge (ohne NUL); bei zu kleinem Puffer wird abgeschnitten. */
size_t hcfg_format_whitelist(const uint16_t *regs, size_t n, char *out, size_t cap);

/* Whitelist-Text in die Konfiguration uebernehmen (setzt wl_override). Rueckgabe wie hcfg_parse_whitelist;
 * bei Fehler bleibt die Konfiguration unveraendert. */
int    hcfg_set_whitelist_text(hcfg_t *c, const char *text);

/* Liste gegen die Registertabelle pruefen: unbekannte Register und Low-Woerter werden entfernt
 * (Rueckgabe = Anzahl entfernt), Register ohne HP_F_WRITABLE nur per warn() gemeldet. warn darf NULL sein. */
typedef void (*hcfg_warn_cb_t)(const char *msg, uint16_t reg);
size_t hcfg_whitelist_validate(uint16_t *regs, uint16_t *n, hcfg_warn_cb_t warn);

/* Konfiguration wirksam machen: Whitelist validieren + in hoval_proto einhaengen. Liefert Anzahl
 * verworfener Whitelist-Eintraege. (Poll-Werte lesen die Tasks direkt ueber hcfg_get().) */
size_t hcfg_apply(hcfg_t *c, hcfg_warn_cb_t warn);

/* Die globale Instanz */
const hcfg_t *hcfg_get(void);
hcfg_t       *hcfg_mut(void);

/* ---- NVS-Anbindung (nur ESP-IDF, hoval_cfg_nvs.c) ---- */
/* Vorhandene Schluessel ueber die Defaults legen. true auch wenn der Namespace fehlt (= Defaults). */
bool hcfg_nvs_load(hcfg_t *c);
/* Alle Werte schreiben (fuer die spaetere Statusseite / Konsole). */
bool hcfg_nvs_save(const hcfg_t *c);
/* Namespace loeschen -> naechster Start mit Kompilat-Defaults. */
bool hcfg_nvs_reset(void);

#ifdef __cplusplus
}
#endif
#endif /* HOVAL_CFG_H */
