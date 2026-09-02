/*
 * test_proto.c — Host-Test fuer hoval_proto.c (gcc, kein ESP-IDF noetig).
 *
 * Gibt eine kanonische Textausgabe aus; ref_proto.py erzeugt dieselbe Ausgabe mit den
 * Funktionen aus bridge/hoval_bridge.py. `make test` vergleicht beide (diff) und prueft
 * zusaetzlich Reassembly/Tabellenzugriff mit Assertions.
 */
#include <stdio.h>
#include <string.h>
#include <assert.h>
#include "hoval_proto.h"

static void hex(const char *tag, const uint8_t *b, size_t n)
{
    printf("%s", tag);
    for (size_t i = 0; i < n; i++) printf(" %02x", b[i]);
    printf("\n");
}

/* Ergebnis der Reassembly */
static uint8_t last_msg[HP_MSG_MAX]; static size_t last_len; static int msgs;
static void on_msg(const uint8_t *raw, size_t len, void *ctx)
{
    (void)ctx; memcpy(last_msg, raw, len); last_len = len; msgs++;
}

int main(void)
{
    uint8_t f[8]; size_t n;

    /* --- Frames (Vergleich mit Python) --- */
    n = hp_build_get(1, 0, 2051, f);            hex("GET 1-0-2051     ", f, n);
    n = hp_build_get(60, 254, 27, f);           hex("GET 60-254-27    ", f, n);
    n = hp_build_get(50, 0, 40650, f);          hex("GET 50-0-40650   ", f, n);
    n = hp_build_set(1, 0, 3050, HP_T_LIST, 4, f);      hex("SET LIST 4       ", f, n);
    n = hp_build_set(1, 0, 7036, HP_T_S16, 250, f);     hex("SET S16 250      ", f, n);
    n = hp_build_set(1, 0, 7036, HP_T_S16, 0, f);       hex("SET S16 0        ", f, n);
    n = hp_build_set(2, 0, 5077, HP_T_S16, 80, f);      hex("SET S16 80       ", f, n);
    n = hp_build_set(1, 0, 3051, HP_T_S16, -100 & 0xFFFF, f); hex("SET S16 -100     ", f, n);
    n = hp_build_set(60, 254, 27, HP_T_U8, 255, f);     hex("SET U8 255       ", f, n);
    printf("ARB WEZ read  %08x\n", hp_arb_for(1, false));
    printf("ARB WEZ write %08x\n", hp_arb_for(1, true));
    printf("ARB HV read   %08x\n", hp_arb_for(520, false));
    printf("ARB HV write  %08x\n", hp_arb_for(520, true));
    printf("ARB PS write  %08x\n", hp_arb_for(143, true));

    /* --- Dekodierung (Vergleich mit Python decode_value/to_registers) --- */
    struct { const char *t; uint8_t b[4]; size_t n; } dec[] = {
        {"U8",  {0x16}, 1}, {"S8", {0xF6}, 1}, {"U16", {0x01, 0x2C}, 2}, {"S16", {0xFF, 0x9C}, 2},
        {"S16", {0x80, 0x00}, 2}, {"LIST", {0x00, 0x04}, 2}, {"U32", {0x00, 0x01, 0x19, 0x2B}, 4},
        {"S32", {0xFF, 0xFF, 0xFF, 0x38}, 4}, {"U32", {0x12, 0x34, 0x56, 0x78}, 4},
        {"U16", {0xFF, 0xFF}, 2}, {"S16", {0x05}, 1}, {"U32", {0x01, 0x02}, 2},
    };
    for (size_t i = 0; i < sizeof dec / sizeof dec[0]; i++) {
        int32_t v; uint16_t w[2];
        hp_type_t t = hp_type_from_str(dec[i].t);
        assert(hp_decode(t, dec[i].b, dec[i].n, &v));
        size_t k = hp_to_regs(t, v, w);
        printf("DEC %-4s", dec[i].t);
        for (size_t j = 0; j < dec[i].n; j++) printf(" %02x", dec[i].b[j]);
        printf(" -> %ld regs", (long)v);
        for (size_t j = 0; j < k; j++) printf(" %u", w[j]);
        printf("\n");
    }
    printf("CHK S16 65436 -> %ld\n", (long)hp_check_value(HP_T_S16, 65436));
    printf("CHK S16 250 -> %ld\n",   (long)hp_check_value(HP_T_S16, 250));
    printf("CHK U16 65436 -> %ld\n", (long)hp_check_value(HP_T_U16, 65436));

    /* --- Reassembly (Assertions) --- */
    hp_reasm_t R; hp_reasm_init(&R);
    uint8_t fg, fn; uint16_t dp; const uint8_t *val; size_t vlen; int32_t v;

    /* Einzelframe: Antwort 1-0-2051 = 22 (U8) */
    uint8_t s1[] = {0x00, 0x42, 0x01, 0x00, 0x08, 0x03, 0x16};
    hp_reasm_feed(&R, 0x1F000801u, s1, sizeof s1, 1000, on_msg, NULL);
    assert(msgs == 1 && last_len == 6);
    assert(hp_parse_answer(last_msg, last_len, &fg, &fn, &dp, &val, &vlen));
    assert(fg == 1 && fn == 0 && dp == 2051 && vlen == 1);
    assert(hp_decode(HP_T_U8, val, vlen, &v) && v == 22);

    /* Mehrfachframe: 32-bit-Antwort 10-1-23009 = 0x0001192B, remaining=2 (Start + 1 Fortsetzung), CRC hinten */
    uint8_t m1[] = {0x10, 0x07, 0x42, 0x0A, 0x01, 0x59, 0xE1, 0x00};
    uint8_t m2[] = {0x07, 0x01, 0x19, 0x2B, 0xAA, 0xBB};
    hp_reasm_feed(&R, 0x1F000801u, m1, sizeof m1, 1001, on_msg, NULL);
    assert(msgs == 1);                                   /* noch unvollstaendig */
    hp_reasm_feed(&R, 0x08000801u, m2, sizeof m2, 1002, on_msg, NULL);
    assert(msgs == 2 && last_len == 9);
    assert(hp_parse_answer(last_msg, last_len, &fg, &fn, &dp, &val, &vlen));
    assert(fg == 10 && fn == 1 && dp == 23009 && vlen == 4);
    assert(hp_decode(HP_T_U32, val, vlen, &v) && v == 0x0001192B);

    /* remaining=1 verhaelt sich wie in Python: ebenfalls fertig nach 1 Fortsetzung */
    uint8_t m3[] = {0x08, 0x09, 0x42, 0x3C, 0xFE, 0x00, 0x33, 0x00};
    uint8_t m4[] = {0x09, 0x00, 0x00, 0x2A, 0x00, 0x00};
    hp_reasm_feed(&R, 0x1F000801u, m3, sizeof m3, 1003, on_msg, NULL);
    hp_reasm_feed(&R, 0x08000801u, m4, sizeof m4, 1004, on_msg, NULL);
    assert(msgs == 3 && last_len == 9);
    assert(hp_parse_answer(last_msg, last_len, &fg, &fn, &dp, &val, &vlen) && dp == 51 && fg == 60);
    assert(hp_decode(HP_T_U32, val, vlen, &v) && v == 42);

    /* Fortsetzung ohne Start -> ignoriert; Typ 0x00 -> ignoriert; anderer devkey -> kein Treffer */
    hp_reasm_feed(&R, 0x08000801u, m2, sizeof m2, 1005, on_msg, NULL);
    hp_reasm_feed(&R, 0x00000801u, s1, sizeof s1, 1005, on_msg, NULL);
    hp_reasm_feed(&R, 0x1F000802u, m1, sizeof m1, 1006, on_msg, NULL);
    hp_reasm_feed(&R, 0x08000801u, m2, sizeof m2, 1007, on_msg, NULL);   /* devkey 0801 != 0802 */
    assert(msgs == 3);
    /* Timeout: Slot nach 5 s freigeben (alle 8 Slots fuellen, 9. Start verdraengt) */
    for (int i = 0; i < 9; i++) {
        uint8_t st[] = {0x10, (uint8_t)(0x20 + i), 0x42, 0, 0, 0, 0, 0};
        hp_reasm_feed(&R, 0x1F000803u, st, sizeof st, 2000 + i, on_msg, NULL);
    }
    assert(R.drops >= 1 && msgs == 3);
    assert(!hp_parse_answer((const uint8_t *)"\x40\x01\x00\x08\x03", 5, &fg, &fn, &dp, &val, &vlen)); /* GET ist keine Antwort */
    printf("REASM ok: frames=%lu msgs=%lu drops=%lu\n", (unsigned long)R.rx_frames, (unsigned long)R.rx_msgs, (unsigned long)R.drops);

    /* --- Tabelle (regmap_example.h) --- */
    assert(hp_regs_count >= 10);
    for (uint16_t i = 1; i < hp_regs_count; i++) assert(hp_regs[i - 1].reg < hp_regs[i].reg);   /* sortiert, eindeutig */
    const hp_reg_t *r = hp_find_reg(1501);
    assert(r && r->fg == 1 && r->fn == 0 && r->dp == 2051 && r->type == HP_T_U8);
    assert(hp_find_reg(1) == NULL && hp_find_reg(65535) == NULL);
    const hp_reg_t *hits[4];
    size_t k = hp_find_by_dp(10, 1, 23009, hits, 4);
    assert(k == 1 && hits[0]->reg == 25613);                    /* Low-Wort 25614 nicht dabei */
    assert(hp_find_reg(25614)->flags & HP_F_LOW_HALF);
    k = hp_find_by_dp(60, 254, 51, hits, 4);
    assert(k == 1 && hits[0]->reg == 27486);                    /* beide "_high" benannt -> strukturell gepaart */
    assert(hp_in_whitelist(1490) && hp_in_whitelist(27509) && !hp_in_whitelist(1501) && !hp_in_whitelist(1534));
    assert(hp_excl_partner(1490) == 19482 && hp_excl_partner(19482) == 1490 && hp_excl_partner(1501) == 0);
    assert(hp_find_reg(1478)->flags & HP_F_WRITABLE);
    assert(hp_find_reg(1478)->flags & HP_F_NO_RANGE);           /* min null -> keine Pruefung */
    assert(!(hp_find_reg(1490)->flags & HP_F_NO_RANGE) && hp_find_reg(1490)->min == 100 && hp_find_reg(1490)->max == 1100);
    assert(hp_areas_count >= 1);
    for (uint16_t i = 0; i < hp_areas_count; i++) {
        uint32_t s = hp_areas[i].start, e = s + hp_areas[i].count;
        assert(e <= 65536);
        if (i) assert(s > (uint32_t)hp_areas[i - 1].start + hp_areas[i - 1].count);
    }
    for (uint16_t i = 0; i < hp_regs_count; i++) {          /* jedes Register liegt in einem Bereich */
        bool in = false;
        for (uint16_t a = 0; a < hp_areas_count; a++)
            if (hp_regs[i].reg >= hp_areas[a].start && hp_regs[i].reg < hp_areas[a].start + hp_areas[a].count) in = true;
        assert(in);
    }
    printf("TABLE ok: %u regs, %u areas, %u whitelist\n", hp_regs_count, hp_areas_count, hp_whitelist_count);
    return 0;
}
