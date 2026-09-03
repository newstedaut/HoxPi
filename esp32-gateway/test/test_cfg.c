/*
 * test_cfg.c — Host-Test fuer hoval_cfg.c (Laufzeit-Konfiguration, gcc, kein ESP-IDF).
 * Prueft: Defaults + Klemmen, hcfg_set-Grenzen, Whitelist-Text-Parser (Trenner, Duplikate, Fehler,
 * Ueberlauf), Formatierer (Roundtrip, Abschneiden), Validierung gegen die Registertabelle
 * (unbekannt/Low-Wort verworfen, nicht-schreibbar gemeldet) und den Override in hp_in_whitelist().
 */
#include <stdio.h>
#include <string.h>
#include <assert.h>
#include "hoval_cfg.h"
#include "hoval_proto.h"

static int warns; static uint16_t last_warn_reg; static char last_warn_msg[96];
static void warn(const char *msg, uint16_t reg)
{
    warns++; last_warn_reg = reg;
    strncpy(last_warn_msg, msg, sizeof last_warn_msg - 1); last_warn_msg[sizeof last_warn_msg - 1] = 0;
}

int main(void)
{
    hcfg_t c;
    uint16_t wl[HCFG_WL_MAX];
    char buf[HCFG_WL_TEXT_MAX + 1];

    /* --- Defaults + Klemmen --- */
    hcfg_defaults(&c, 30, 5, 100, false);
    assert(c.poll_wez_s == 30 && c.poll_hv_s == 5 && c.poll_delay_ms == 100 && !c.enable_write);
    assert(!c.wl_override && c.wl_n == 0 && c.from_nvs == 0);
    hcfg_defaults(&c, 1, 0, 99999, true);                         /* ausserhalb -> eingeklemmt */
    assert(c.poll_wez_s == HCFG_POLL_WEZ_MIN && c.poll_hv_s == HCFG_POLL_HV_MIN && c.poll_delay_ms == HCFG_POLL_DELAY_MAX && c.enable_write);

    /* --- hcfg_set: Grenzen und Herkunft --- */
    hcfg_defaults(&c, 30, 5, 100, false);
    assert(hcfg_set(&c, "poll_wez", 60) && c.poll_wez_s == 60 && (c.from_nvs & HCFG_SRC_POLL_WEZ));
    assert(!hcfg_set(&c, "poll_wez", 4) && c.poll_wez_s == 60);   /* abgelehnt -> alter Wert bleibt */
    assert(!hcfg_set(&c, "poll_wez", 3601));
    assert(hcfg_set(&c, "poll_hv", 1) && c.poll_hv_s == 1);
    assert(!hcfg_set(&c, "poll_hv", 0));
    assert(hcfg_set(&c, "poll_delay", 250) && c.poll_delay_ms == 250);
    assert(!hcfg_set(&c, "poll_delay", 9) && !hcfg_set(&c, "poll_delay", 2001));
    assert(hcfg_set(&c, "wr_en", 1) && c.enable_write && (c.from_nvs & HCFG_SRC_WR_EN));
    assert(!hcfg_set(&c, "wr_en", 2) && c.enable_write);
    assert(hcfg_set(&c, "wr_en", 0) && !c.enable_write);
    assert(!hcfg_set(&c, "gibtsnicht", 1) && !hcfg_set(NULL, "poll_wez", 30) && !hcfg_set(&c, NULL, 30));

    /* --- Whitelist-Parser --- */
    assert(hcfg_parse_whitelist("1490,1497,27509", wl, HCFG_WL_MAX) == 3 && wl[0] == 1490 && wl[1] == 1497 && wl[2] == 27509);
    assert(hcfg_parse_whitelist(" 1490 ; 1497\t27509\n,,1490 ", wl, HCFG_WL_MAX) == 3 && wl[2] == 27509);  /* Trenner + Duplikat */
    assert(hcfg_parse_whitelist("", wl, HCFG_WL_MAX) == 0);
    assert(hcfg_parse_whitelist("   ", wl, HCFG_WL_MAX) == 0);
    assert(hcfg_parse_whitelist(NULL, wl, HCFG_WL_MAX) == 0);
    assert(hcfg_parse_whitelist("65535,0", wl, HCFG_WL_MAX) == 2 && wl[0] == 65535 && wl[1] == 0);
    assert(hcfg_parse_whitelist("65536", wl, HCFG_WL_MAX) == -1);
    assert(hcfg_parse_whitelist("1490x", wl, HCFG_WL_MAX) == -1);
    assert(hcfg_parse_whitelist("-1", wl, HCFG_WL_MAX) == -1);
    assert(hcfg_parse_whitelist("1490,abc", wl, HCFG_WL_MAX) == -1);
    assert(hcfg_parse_whitelist("0x5D2", wl, HCFG_WL_MAX) == -1);
    assert(hcfg_parse_whitelist("1,2,3", wl, 2) == -2);            /* mehr als max */
    assert(hcfg_parse_whitelist("1,2,2,2", wl, 2) == 2);           /* Duplikate zaehlen nicht */
    {
        char lang[HCFG_WL_TEXT_MAX + 8];
        memset(lang, '1', sizeof lang - 1); lang[sizeof lang - 1] = 0;
        assert(hcfg_parse_whitelist(lang, wl, HCFG_WL_MAX) == -1);  /* Text zu lang */
    }
    {
        /* 128 verschiedene Register passen genau, 129 nicht */
        char viele[HCFG_WL_TEXT_MAX + 1]; size_t len = 0;
        for (int i = 0; i < HCFG_WL_MAX; i++) len += (size_t)snprintf(viele + len, sizeof viele - len, "%s%d", i ? "," : "", 1000 + i);
        assert(hcfg_parse_whitelist(viele, wl, HCFG_WL_MAX) == HCFG_WL_MAX);
        len += (size_t)snprintf(viele + len, sizeof viele - len, ",%d", 1000 + HCFG_WL_MAX);
        assert(hcfg_parse_whitelist(viele, wl, HCFG_WL_MAX) == -2);
    }

    /* --- Formatierer: Roundtrip + Abschneiden --- */
    uint16_t src[] = { 1490, 1497, 27509, 65535 };
    size_t l = hcfg_format_whitelist(src, 4, buf, sizeof buf);
    assert(l == strlen("1490,1497,27509,65535") && !strcmp(buf, "1490,1497,27509,65535"));
    assert(hcfg_parse_whitelist(buf, wl, HCFG_WL_MAX) == 4 && wl[3] == 65535);
    assert(hcfg_format_whitelist(src, 0, buf, sizeof buf) == 0 && buf[0] == 0);
    assert(hcfg_format_whitelist(src, 4, buf, 10) == strlen("1490,1497") && !strcmp(buf, "1490,1497"));  /* passt nur bis 2 */
    assert(hcfg_format_whitelist(src, 4, buf, 1) == 0 && buf[0] == 0);
    assert(hcfg_format_whitelist(src, 4, NULL, 0) == 0);

    /* --- Set per Text: Fehler laesst Konfiguration unveraendert --- */
    hcfg_defaults(&c, 30, 5, 100, false);
    assert(hcfg_set_whitelist_text(&c, "1490,1497") == 2 && c.wl_override && c.wl_n == 2 && (c.from_nvs & HCFG_SRC_WHITELIST));
    assert(hcfg_set_whitelist_text(&c, "kaputt") == -1 && c.wl_n == 2 && c.wl[1] == 1497);
    assert(hcfg_set_whitelist_text(&c, "") == 0 && c.wl_override && c.wl_n == 0);   /* leer = nichts schreibbar */

    /* --- Validierung gegen die Tabelle (regmap_example.h bzw. regmap_gen.h) --- */
    hcfg_defaults(&c, 30, 5, 100, false);
    /* 1490 schreibbar; 1501 in Tabelle aber nicht WRITABLE (nur Meldung); 25614 Low-Wort; 4711 unbekannt */
    assert(hcfg_set_whitelist_text(&c, "1490,1501,25614,4711,27509") == 5);
    warns = 0;
    size_t dropped = hcfg_whitelist_validate(c.wl, &c.wl_n, warn);
    assert(dropped == 2 && c.wl_n == 3 && c.wl[0] == 1490 && c.wl[1] == 1501 && c.wl[2] == 27509);
    assert(warns == 3);                                             /* 1501 gemeldet, 25614 + 4711 verworfen */
    assert(hcfg_whitelist_validate(c.wl, &c.wl_n, NULL) == 0 && c.wl_n == 3);   /* idempotent, warn NULL ok */

    /* --- Override wirkt in hp_in_whitelist --- */
    uint16_t n_act = 0;
    hp_whitelist_override(NULL, 0);
    hp_whitelist_active(&n_act);
    assert(n_act == hp_whitelist_count);
    assert(hp_in_whitelist(1497) && hp_in_whitelist(27509));         /* Kompilat: 1497 drin */
    hcfg_defaults(&c, 30, 5, 100, false);
    assert(hcfg_set_whitelist_text(&c, "1490,4711") == 2);
    warns = 0;
    assert(hcfg_apply(&c, warn) == 1 && c.wl_n == 1 && warns == 1 && last_warn_reg == 4711);
    hp_whitelist_active(&n_act);
    assert(n_act == 1);
    assert(hp_in_whitelist(1490) && !hp_in_whitelist(1497) && !hp_in_whitelist(27509) && !hp_in_whitelist(4711));
    /* leere NVS-Liste = alles gesperrt */
    assert(hcfg_set_whitelist_text(&c, "") == 0 && hcfg_apply(&c, warn) == 0);
    hp_whitelist_active(&n_act);
    assert(n_act == 0 && !hp_in_whitelist(1490));
    /* kein Override -> Kompilat zurueck */
    hcfg_defaults(&c, 30, 5, 100, false);
    assert(hcfg_apply(&c, warn) == 0);
    hp_whitelist_active(&n_act);
    assert(n_act == hp_whitelist_count && hp_in_whitelist(1497));

    /* --- globale Instanz --- */
    hcfg_defaults(hcfg_mut(), 30, 5, 100, false);
    assert(hcfg_get()->poll_wez_s == 30 && hcfg_get() == hcfg_mut());
    assert(hcfg_set(hcfg_mut(), "poll_wez", 45) && hcfg_get()->poll_wez_s == 45);

    printf("CFG ok: Defaults/Grenzen, Whitelist-Parser %d Faelle, Validierung (2 verworfen, 1 gemeldet), Override, Tabelle %u Register\n",
           14, hp_regs_count);
    return 0;
}
