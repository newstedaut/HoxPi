/*
 * hoval_proto.h — Hoval TopTronic-E CAN-Protokoll (reine C-Bibliothek, keine ESP-IDF-Abhaengigkeit)
 *
 * 1:1-Portierung der verifizierten Logik aus bridge/hoval_bridge.py (HoxPi, Raspberry Pi):
 *   - GET/SET-Frames bauen (Einzelframe, 6 bzw. 7/8 Datenbytes)
 *   - Antworten reassemblieren (Einzel- UND Mehrfachframe, CRC abschneiden)
 *   - Werte dekodieren (U8/S8/U16/S16/U32/S32/LIST, big-endian) und in 16-bit-Modbus-Woerter legen
 *   - Registertabelle (generiert aus registers.json, siehe tools/gen_esp32_regmap.py)
 *
 * Das Modul ist absichtlich frei von Hardware-Code, damit es auf dem Host (gcc) mit
 * test/test_proto.c gegen die Python-Referenz geprueft werden kann.
 */
#ifndef HOVAL_PROTO_H
#define HOVAL_PROTO_H

#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ---- Opcodes / Arbitration-IDs (29-bit Extended) — VERBATIM aus hoval_bridge.py ---- */
#define HP_OP_GET       0x40u
#define HP_OP_RESPONSE  0x42u
#define HP_OP_SET       0x46u

#define HP_ARB_POLL     0x06E40801u   /* WEZ (UnitId 1) lesen            */
#define HP_ARB_WRITE    0x07E40801u   /* WEZ (UnitId 1) schreiben        */
#define HP_ARB_HV_POLL  0x1FE08A08u   /* HomeVent (UnitId 520): lesen UND schreiben */

#define HP_UNIT_WEZ     1u
#define HP_UNIT_HV      520u
#define HP_UNIT_PS      143u

/* Datentypen (Kodierung wie in registers.json, als Enum fuer die Tabelle) */
typedef enum {
    HP_T_U8 = 0, HP_T_S8, HP_T_U16, HP_T_S16, HP_T_U32, HP_T_S32, HP_T_LIST, HP_T_UNKNOWN
} hp_type_t;

/* Flags je Tabellenzeile */
#define HP_F_WRITABLE   0x01u   /* laut Hoval-Liste schreibbar (NICHT die Whitelist!)      */
#define HP_F_LOW_HALF   0x02u   /* zweite Haelfte eines 32-bit-Paares -> nie selbst dekodieren */
#define HP_F_NO_RANGE   0x04u   /* min/max fehlen oder 0/0 -> keine Bereichspruefung        */

/* Eine Registerzeile (generiert). Sortiert nach reg aufsteigend. */
typedef struct {
    uint16_t reg;       /* Modbus-Registeradresse (Hoval-Nummerierung, 0-basiert wie HoxPi) */
    uint16_t unit_id;   /* 1 = WEZ, 520 = HomeVent, 143 = Puffermodul */
    uint8_t  fg;        /* Funktionsgruppe */
    uint8_t  fn;        /* Funktionsnummer */
    uint16_t dp;        /* Datenpunkt (Bedienteilnummer ohne Bindestrich) */
    uint8_t  type;      /* hp_type_t */
    int8_t   decimal;   /* Nachkommastellen (nur Info; Modbus liefert Rohwerte wie HoxPi) */
    uint8_t  flags;     /* HP_F_* */
    int32_t  min;       /* Rohwert-Grenzen fuers Schreiben */
    int32_t  max;
} hp_reg_t;

/* Modbus-Bereich (zusammenhaengender Registerblock) fuer den esp-modbus-Slave */
typedef struct {
    uint16_t start;     /* erste Registeradresse */
    uint16_t count;     /* Anzahl 16-bit-Woerter */
} hp_area_t;

/* Die generierte Tabelle (regmap_gen.h) liefert diese Symbole: */
extern const hp_reg_t  hp_regs[];
extern const uint16_t  hp_regs_count;
extern const hp_area_t hp_areas[];
extern const uint16_t  hp_areas_count;
extern const uint16_t  hp_whitelist[];   /* Register, die per Modbus geschrieben werden duerfen */
extern const uint16_t  hp_whitelist_count;

/* ---- Frames bauen ---------------------------------------------------------- */
/* GET: [0x01, 0x40, fg, fn, dp_hi, dp_lo]  -> 6 Bytes */
size_t   hp_build_get(uint8_t fg, uint8_t fn, uint16_t dp, uint8_t out[8]);
/* SET: [0x01, 0x46, fg, fn, dp_hi, dp_lo] + 1 Byte (U8/S8/LIST) oder 2 Byte BE -> 7/8 Bytes */
size_t   hp_build_set(uint8_t fg, uint8_t fn, uint16_t dp, hp_type_t type, int32_t value, uint8_t out[8]);
/* Arbitration-ID fuer einen Zieleinheit: HV hoert auf HV_POLL auch beim Schreiben */
uint32_t hp_arb_for(uint16_t unit_id, bool write);

/* ---- Antworten reassemblieren ---------------------------------------------- */
/* Callback fuer eine vollstaendige Nachricht (raw[0] == 0x42 erwartet, sonst ignorieren) */
typedef void (*hp_msg_cb_t)(const uint8_t *raw, size_t len, void *ctx);

#define HP_PENDING_SLOTS 8
#define HP_MSG_MAX       32   /* Hoval-Antworten sind <= 5+4 Bytes Nutzlast; Reserve fuer Strings */

typedef struct {
    uint16_t devkey;    /* arb & 0xFFFF */
    uint8_t  seq;       /* Folge-ID */
    int8_t   remaining; /* Zaehler wie in hoval_bridge.py (remaining-1, fertig bei <= 0) */
    uint8_t  len;
    uint8_t  buf[HP_MSG_MAX];
    uint32_t t_ms;      /* Ankunft des Startframes (Timeout 5 s) */
    bool     used;
} hp_pending_t;

typedef struct {
    hp_pending_t slot[HP_PENDING_SLOTS];
    uint32_t rx_frames, rx_msgs, drops;
} hp_reasm_t;

void hp_reasm_init(hp_reasm_t *r);
/* Einen empfangenen CAN-Frame einspeisen. now_ms = monotone Millisekunden. */
void hp_reasm_feed(hp_reasm_t *r, uint32_t arb, const uint8_t *d, size_t len,
                   uint32_t now_ms, hp_msg_cb_t cb, void *ctx);

/* Antwort zerlegen: raw = [0x42, fg, fn, dp_hi, dp_lo, value...]. false wenn kein Antwortframe. */
bool hp_parse_answer(const uint8_t *raw, size_t len, uint8_t *fg, uint8_t *fn, uint16_t *dp,
                     const uint8_t **val, size_t *vlen);

/* ---- Werte ------------------------------------------------------------------ */
/* Rohbytes -> Rohwert (OHNE Dezimalskalierung, wie decode_value in hoval_bridge.py). false bei leerem val. */
bool     hp_decode(hp_type_t type, const uint8_t *val, size_t vlen, int32_t *out);
/* Rohwert -> 16-bit-Woerter, hi zuerst. Liefert 1 oder 2. */
size_t   hp_to_regs(hp_type_t type, int32_t value, uint16_t out[2]);
/* S16-Sicht auf ein Modbus-Wort (fuer Bereichspruefung beim Schreiben) */
int32_t  hp_check_value(hp_type_t type, uint16_t word);
hp_type_t hp_type_from_str(const char *s);
const char *hp_type_str(hp_type_t t);

/* ---- Tabelle ---------------------------------------------------------------- */
const hp_reg_t *hp_find_reg(uint16_t reg);                            /* binaere Suche */
/* Alle Zeilen zu (fg,fn,dp) ohne LOW_HALF; liefert Anzahl, schreibt Zeiger nach out[max]. */
size_t hp_find_by_dp(uint8_t fg, uint8_t fn, uint16_t dp, const hp_reg_t **out, size_t max);
bool   hp_in_whitelist(uint16_t reg);
/* Laufzeit-Whitelist (NVS, hoval_cfg.c) ueber die kompilierte legen; regs = NULL -> wieder hp_whitelist[].
 * Der Zeiger muss dauerhaft gueltig bleiben (hcfg_t liegt statisch). */
void   hp_whitelist_override(const uint16_t *regs, uint16_t n);
/* aktive Liste (Kompilat oder Override) fuer Log/Statusseite */
const uint16_t *hp_whitelist_active(uint16_t *n);
/* Kanal-Exklusion Heizen<->Kuehlen: Partnerregister oder 0 */
uint16_t hp_excl_partner(uint16_t reg);

#ifdef __cplusplus
}
#endif
#endif /* HOVAL_PROTO_H */
