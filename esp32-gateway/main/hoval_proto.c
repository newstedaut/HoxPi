/*
 * hoval_proto.c — Hoval TopTronic-E CAN-Protokoll, reine C-Umsetzung von bridge/hoval_bridge.py
 * (Frames, Reassembly, Dekodierung, Tabellenzugriff). Keine ESP-IDF-Abhaengigkeit.
 */
#include "hoval_proto.h"
#include <string.h>

/* ---- Frames --------------------------------------------------------------- */
size_t hp_build_get(uint8_t fg, uint8_t fn, uint16_t dp, uint8_t out[8])
{
    out[0] = 0x01; out[1] = HP_OP_GET; out[2] = fg; out[3] = fn;
    out[4] = (uint8_t)(dp >> 8); out[5] = (uint8_t)(dp & 0xFF);
    return 6;
}

size_t hp_build_set(uint8_t fg, uint8_t fn, uint16_t dp, hp_type_t type, int32_t value, uint8_t out[8])
{
    out[0] = 0x01; out[1] = HP_OP_SET; out[2] = fg; out[3] = fn;
    out[4] = (uint8_t)(dp >> 8); out[5] = (uint8_t)(dp & 0xFF);
    if (type == HP_T_U8 || type == HP_T_S8 || type == HP_T_LIST) {
        out[6] = (uint8_t)(value & 0xFF);
        return 7;
    }
    /* 16-bit big-endian — auch fuer 32-bit-Typen (HoxPi schreibt nie 32-bit; Whitelist sperrt sie) */
    out[6] = (uint8_t)((value >> 8) & 0xFF);
    out[7] = (uint8_t)(value & 0xFF);
    return 8;
}

uint32_t hp_arb_for(uint16_t unit_id, bool write)
{
    if (unit_id == HP_UNIT_HV) return HP_ARB_HV_POLL;   /* Lueftung ignoriert die WEZ-Schreib-ID */
    return write ? HP_ARB_WRITE : HP_ARB_POLL;
}

/* ---- Reassembly ------------------------------------------------------------
 * Arb-Top-Byte = Frame-Typ (parren/hoval-ultrasource-agent, in HoxPi live verifiziert):
 *   0x1f = Start: Data[0]>>3 = Anzahl Folgeframes (0 => Einzelframe, Nutzdaten ab Data[1]);
 *          sonst Seq-ID = Data[1], Nutzdaten ab Data[2]
 *   0x00 = ignorieren
 *   sonst = Fortsetzung: Seq-ID = Data[0], Nutzdaten ab Data[1]; am Ende 2 Byte CRC abschneiden
 * Geraeteschluessel = arb & 0xFFFF.
 */
void hp_reasm_init(hp_reasm_t *r) { memset(r, 0, sizeof(*r)); }

static hp_pending_t *slot_find(hp_reasm_t *r, uint16_t devkey, uint8_t seq)
{
    for (int i = 0; i < HP_PENDING_SLOTS; i++)
        if (r->slot[i].used && r->slot[i].devkey == devkey && r->slot[i].seq == seq)
            return &r->slot[i];
    return NULL;
}

static hp_pending_t *slot_alloc(hp_reasm_t *r, uint32_t now_ms)
{
    hp_pending_t *oldest = &r->slot[0];
    for (int i = 0; i < HP_PENDING_SLOTS; i++) {
        hp_pending_t *s = &r->slot[i];
        if (!s->used) return s;
        if (now_ms - s->t_ms > 5000) { s->used = false; r->drops++; return s; }   /* veraltet */
        if ((int32_t)(s->t_ms - oldest->t_ms) < 0) oldest = s;
    }
    r->drops++;
    oldest->used = false;
    return oldest;
}

void hp_reasm_feed(hp_reasm_t *r, uint32_t arb, const uint8_t *d, size_t len,
                   uint32_t now_ms, hp_msg_cb_t cb, void *ctx)
{
    if (len == 0 || len > 8) return;
    r->rx_frames++;
    uint8_t  ftype  = (uint8_t)((arb >> 24) & 0xFF);
    uint16_t devkey = (uint16_t)(arb & 0xFFFF);

    if (ftype == 0x1f) {
        if (len < 2) return;
        uint8_t remaining = (uint8_t)(d[0] >> 3);
        if (remaining == 0) {                       /* Einzelframe */
            r->rx_msgs++;
            cb(d + 1, len - 1, ctx);
            return;
        }
        /* Python-Semantik exakt: Zaehler = remaining-1, je Folgeframe -1, fertig bei <= 0.
         * Ein Startframe wartet also IMMER auf mindestens einen Folgeframe (32-bit-Antwort =
         * Start + 1 Fortsetzung, live verifiziert). */
        hp_pending_t *s = slot_find(r, devkey, d[1]);
        if (!s) s = slot_alloc(r, now_ms);
        s->used = true; s->devkey = devkey; s->seq = d[1];
        s->remaining = (int8_t)(remaining - 1);
        s->len = 0; s->t_ms = now_ms;
        size_t n = len - 2;
        if (n > HP_MSG_MAX) n = HP_MSG_MAX;
        memcpy(s->buf, d + 2, n); s->len = (uint8_t)n;
        return;
    }
    if (ftype == 0x00) return;

    /* Fortsetzung */
    hp_pending_t *s = slot_find(r, devkey, d[0]);
    if (!s) return;
    size_t n = len - 1;
    if (s->len + n > HP_MSG_MAX) n = HP_MSG_MAX - s->len;
    memcpy(s->buf + s->len, d + 1, n); s->len = (uint8_t)(s->len + n);
    s->remaining--;
    if (s->remaining <= 0) {
        s->used = false; r->rx_msgs++;
        cb(s->buf, s->len >= 2 ? s->len - 2 : 0, ctx);   /* CRC (2 Byte) abschneiden */
    }
}

bool hp_parse_answer(const uint8_t *raw, size_t len, uint8_t *fg, uint8_t *fn, uint16_t *dp,
                     const uint8_t **val, size_t *vlen)
{
    if (len < 5 || raw[0] != HP_OP_RESPONSE) return false;
    *fg = raw[1]; *fn = raw[2];
    *dp = (uint16_t)((raw[3] << 8) | raw[4]);
    *val = raw + 5; *vlen = len - 5;
    return true;
}

/* ---- Werte ------------------------------------------------------------------ */
bool hp_decode(hp_type_t type, const uint8_t *val, size_t vlen, int32_t *out)
{
    if (vlen == 0) return false;
    switch (type) {
    case HP_T_U8:   *out = val[0]; return true;
    case HP_T_S8:   *out = (int8_t)val[0]; return true;
    case HP_T_U16: case HP_T_LIST:
        if (vlen < 2) { *out = val[0]; return true; }
        *out = (uint16_t)((val[0] << 8) | val[1]); return true;
    case HP_T_S16:
        if (vlen < 2) { *out = (int8_t)val[0]; return true; }
        *out = (int16_t)((val[0] << 8) | val[1]); return true;
    case HP_T_U32: case HP_T_S32:
        if (vlen < 4) {   /* Python: int.from_bytes(raw[:4]) nimmt was da ist */
            uint32_t v = 0; for (size_t i = 0; i < vlen; i++) v = (v << 8) | val[i];
            *out = (int32_t)v; return true;
        }
        *out = (int32_t)(((uint32_t)val[0] << 24) | ((uint32_t)val[1] << 16) |
                         ((uint32_t)val[2] << 8) | val[3]);
        return true;
    default:
        if (vlen < 2) { *out = val[0]; return true; }
        *out = (uint16_t)((val[0] << 8) | val[1]); return true;
    }
}

size_t hp_to_regs(hp_type_t type, int32_t value, uint16_t out[2])
{
    if (type == HP_T_U32 || type == HP_T_S32) {
        uint32_t v = (uint32_t)value;
        out[0] = (uint16_t)(v >> 16); out[1] = (uint16_t)(v & 0xFFFF);
        return 2;
    }
    out[0] = (uint16_t)(value & 0xFFFF);
    return 1;
}

int32_t hp_check_value(hp_type_t type, uint16_t word)
{
    if (type == HP_T_S16 && word > 32767) return (int32_t)word - 65536;
    return word;
}

static const char *TYPE_NAMES[] = { "U8", "S8", "U16", "S16", "U32", "S32", "LIST", "?" };

hp_type_t hp_type_from_str(const char *s)
{
    if (!s) return HP_T_UNKNOWN;
    for (int i = 0; i < HP_T_UNKNOWN; i++) {
        const char *a = TYPE_NAMES[i], *b = s; bool eq = true;
        while (*a || *b) {
            char ca = *a, cb = *b;
            if (cb >= 'a' && cb <= 'z') cb = (char)(cb - 32);
            if (ca != cb) { eq = false; break; }
            a++; b++;
        }
        if (eq) return (hp_type_t)i;
    }
    return HP_T_UNKNOWN;
}

const char *hp_type_str(hp_type_t t) { return TYPE_NAMES[t < HP_T_UNKNOWN ? t : HP_T_UNKNOWN]; }

/* ---- Tabelle ---------------------------------------------------------------- */
const hp_reg_t *hp_find_reg(uint16_t reg)
{
    int lo = 0, hi = (int)hp_regs_count - 1;
    while (lo <= hi) {
        int mid = (lo + hi) / 2;
        if (hp_regs[mid].reg == reg) return &hp_regs[mid];
        if (hp_regs[mid].reg < reg) lo = mid + 1; else hi = mid - 1;
    }
    return NULL;
}

size_t hp_find_by_dp(uint8_t fg, uint8_t fn, uint16_t dp, const hp_reg_t **out, size_t max)
{
    size_t n = 0;
    for (uint16_t i = 0; i < hp_regs_count && n < max; i++) {
        const hp_reg_t *r = &hp_regs[i];
        if (r->fg == fg && r->fn == fn && r->dp == dp && !(r->flags & HP_F_LOW_HALF))
            out[n++] = r;
    }
    return n;
}

bool hp_in_whitelist(uint16_t reg)
{
    for (uint16_t i = 0; i < hp_whitelist_count; i++)
        if (hp_whitelist[i] == reg) return true;
    return false;
}

/* Paarung Heizen <-> Kuehlen je Heizkreis (EXCL_PAIRS in hoval_bridge.py) */
uint16_t hp_excl_partner(uint16_t reg)
{
    switch (reg) {
    case 1490:  return 19482; case 19482: return 1490;    /* HC1 */
    case 1491:  return 23755; case 23755: return 1491;    /* HC2 */
    case 1492:  return 23756; case 23756: return 1492;    /* HC3 */
    default:    return 0;
    }
}
