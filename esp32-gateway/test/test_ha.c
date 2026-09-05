/*
 * test_ha.c — Host-Test fuer hoval_ha.c (Home-Assistant-Port von mqtt/hoval_mqtt.py):
 *   1. Discovery-Payloads aller Entities -> out_ha_discovery.jsonl (eine Zeile je Topic);
 *      ref_ha.py prueft sie mit json.loads und vergleicht Namen/Einheiten/Optionen/Topics mit den
 *      Tabellen in hoval_mqtt.py (per ast gelesen, ohne paho/Modbus).
 *   2. Zustands-Texte gegen eine Register-Attrappe (Dezimalen, Enum, Fehlercode, Kaeltekreis-Sentinel,
 *      Ruecklauf-Fallback, -127-Sollwert, COP-Fallback + Startfilter, Kuehl-Phasen).
 *   3. Kommandos (select-Klartext, number mit Rundung, S16-Wrap, Fehlerfaelle).
 * Braucht die VOLLE Tabelle nicht: Entities ohne Tabellenzeile werden ausgelassen (wie im Gateway).
 */
#include <stdio.h>
#include <string.h>
#include <assert.h>
#include <stdlib.h>
#include <limits.h>
#include "hoval_ha.h"
#include "hoval_cfg.h"
#include "hoval_proto.h"

/* ---- Register-Attrappe ---- */
#define MEM_N 64
static struct { uint16_t reg, word; bool seen; } mem[MEM_N];
static int mem_n;
static void mem_clear(void) { mem_n = 0; }
static void mem_set(uint16_t reg, int32_t val, bool seen)
{
    for (int i = 0; i < mem_n; i++) if (mem[i].reg == reg) { mem[i].word = (uint16_t)(val & 0xFFFF); mem[i].seen = seen; return; }
    assert(mem_n < MEM_N);
    mem[mem_n].reg = reg; mem[mem_n].word = (uint16_t)(val & 0xFFFF); mem[mem_n].seen = seen; mem_n++;
}
static bool fake_read(uint16_t reg, uint16_t *word, bool *seen)
{
    if (!hp_find_reg(reg)) return false;
    for (int i = 0; i < mem_n; i++) if (mem[i].reg == reg) { *word = mem[i].word; *seen = mem[i].seen; return true; }
    *word = 0; *seen = false;      /* in der Tabelle, aber nie vom CAN gelesen */
    return true;
}
static const ha_ent_t *sensor(const char *key)
{
    for (uint8_t i = 0; i < ha_sensors_n; i++) if (!strcmp(ha_sensors[i].key, key)) return &ha_sensors[i];
    assert(0); return NULL;
}
static int has_reg(uint16_t reg) { return hp_find_reg(reg) != NULL; }

/* Zustand als Text holen; "" = nichts publiziert */
static const char *st(const char *key)
{
    static char out[HA_STATE_MAX]; int32_t raw; bool hr;
    if (!ha_state(sensor(key), fake_read, out, sizeof out, &raw, &hr)) return "";
    return out;
}
static int tests = 0, skipped = 0;
#define EXPECT(reg, key, want) do { tests++; if (!has_reg(reg)) { skipped++; } else { const char *g = st(key); \
    if (strcmp(g, want)) { fprintf(stderr, "FEHLER %s: '%s' statt '%s'\n", key, g, want); return 1; } } } while (0)

int main(void)
{
    static char buf[2048], topic[HA_TOPIC_MAX];
    hcfg_t *c = hcfg_mut();
    hcfg_defaults(c, 30, 5, 100, false);
    hcfg_apply(c, NULL);

    /* ---------- 1. Discovery ---------- */
    FILE *f = fopen("out_ha_discovery.jsonl", "w"); assert(f);
    int n_disc = 0;
    for (uint8_t i = 0; i < ha_sensors_n; i++) {
        if (!ha_discovery_json(buf, sizeof buf, &ha_sensors[i])) { assert(!has_reg(ha_sensors[i].reg)); continue; }
        fprintf(f, "%s\t%s\n", ha_topic_discovery(topic, sizeof topic, "sensor", ha_sensors[i].key), buf); n_disc++;
    }
    for (uint8_t i = 0; i < ha_controls_n; i++) {
        if (!ha_discovery_json(buf, sizeof buf, &ha_controls[i])) { assert(!has_reg(ha_controls[i].reg)); continue; }
        fprintf(f, "%s\t%s\n", ha_topic_discovery(topic, sizeof topic, ha_kind_str((ha_kind_t)ha_controls[i].kind), ha_controls[i].key), buf); n_disc++;
    }
    ha_discovery_stale_json(buf, sizeof buf); fprintf(f, "homeassistant/binary_sensor/hoxpi/stale/config\t%s\n", buf);
    ha_discovery_kuehl_json(buf, sizeof buf); fprintf(f, "homeassistant/binary_sensor/hoxpi/kuehl_wartet/config\t%s\n", buf);
    ha_discovery_cop_json(buf, sizeof buf);   fprintf(f, "homeassistant/sensor/hoxpi/cop/config\t%s\n", buf);
    fclose(f);
    /* Abschneide-Erkennung: zu kleiner Puffer -> false, aber NUL-terminiert */
    { char small[40]; assert(!ha_discovery_json(small, sizeof small, &ha_sensors[0]) || !has_reg(ha_sensors[0].reg)); assert(strlen(small) < sizeof small); }
    /* number-Bereiche (num_meta): 1497 100..700/10 -> 10.0..70.0 step 0.5; 27531 -600..0 -> -60.0..90.0 */
    if (has_reg(1497)) { ha_discovery_json(buf, sizeof buf, ha_find_control("set_ww_normal"));
        assert(strstr(buf, "\"min\":10.0,\"max\":70.0,\"step\":0.5")); assert(strstr(buf, "\"unit_of_measurement\":\"°C\"")); assert(strstr(buf, "\"command_topic\":\"hoval/set_ww_normal/set\"")); }
    if (has_reg(27531)) { ha_discovery_json(buf, sizeof buf, ha_find_control("set_sg_off_kk1")); assert(strstr(buf, "\"min\":-60.0,\"max\":90.0")); }
    if (has_reg(1498))  { ha_discovery_json(buf, sizeof buf, ha_find_control("set_ww_eco")); assert(strstr(buf, "\"min\":10,\"max\":70,\"step\":1")); }
    if (has_reg(1510))  { ha_discovery_json(buf, sizeof buf, ha_find_control("set_raumist_hk1")); assert(strstr(buf, "\"min\":0.0,\"max\":90.0")); }
    if (has_reg(1478))  { ha_discovery_json(buf, sizeof buf, ha_find_control("set_bw_hk1")); assert(strstr(buf, "\"options\":[\"Standby\",\"Woche 1\",\"Woche 2\",\"Konstant\",\"Sparbetrieb\",\"Hand Heizen\",\"Hand Kuehlen\"]")); }

    /* ---------- 2. Zustaende ---------- */
    mem_clear();
    mem_set(1477, -32, true);        /* -3,2 °C */
    mem_set(1500, 460, true);        /* 46,0 */
    mem_set(1501, 22, true);
    mem_set(1502, 99, true);         /* unbekannter Enum-Wert -> "99" */
    mem_set(1534, 255, true);
    mem_set(18767, -1270, true);
    mem_set(18768, 100, true);
    mem_set(1539, 4, true);
    mem_set(27537, 255, true);
    mem_set(25611, 0, true);
    EXPECT(1477, "aussentemp", "-3.2");
    EXPECT(1500, "ww_ist", "46.0");
    EXPECT(1501, "status_hk1", "Kuehlen extern");
    EXPECT(1502, "status_hk2", "99");
    EXPECT(1534, "fehlercode", "OK");
    EXPECT(18767, "leistungssollwert", "unknown");
    EXPECT(18768, "anforderung", "ja");
    EXPECT(1539, "status_wez", "Warmwasser");
    EXPECT(27537, "sg_status", "inaktiv");
    EXPECT(25611, "el_leistung", "0.00");
    /* nie gelesen -> nichts publizieren */
    tests++; if (has_reg(18760)) { assert(!strcmp(st("vorlauf"), "")); }
    /* Enum-Rohwert */
    if (has_reg(1501)) { int32_t raw = -1; bool hr = false; char o[HA_STATE_MAX]; assert(ha_state(sensor("status_hk1"), fake_read, o, sizeof o, &raw, &hr)); assert(hr && raw == 22); }
    /* Fehlercode-Dekodierung (FEHLER_ENUM): raw+1 = Klasse*64+Nr */
    { char o[32];
      assert(!strcmp(ha_fehler_text(0, o, sizeof o), "kein Wert"));
      assert(!strcmp(ha_fehler_text(255, o, sizeof o), "OK"));
      assert(!strcmp(ha_fehler_text(2*64+2-1, o, sizeof o), "B:02 Niederdruck"));
      assert(!strcmp(ha_fehler_text(3*64+2-1, o, sizeof o), "E:02 Niederdruck, verriegelt"));
      assert(!strcmp(ha_fehler_text(1*64+61-1, o, sizeof o), "W:61 Startphase-Sonderzustand"));
      assert(!strcmp(ha_fehler_text(1*64+7-1, o, sizeof o), "W:07")); }
    mem_set(1534, 2*64+2-1, true); EXPECT(1534, "fehlercode", "B:02 Niederdruck");
    /* Ruecklauf-Fallback: 1535 = 0 -> 31894/31895 (S32) ; 186 -> 18,6 */
    mem_set(1535, 0, true); mem_set(31894, 0, true); mem_set(31895, 186, true);
    if (has_reg(1535) && has_reg(31894)) EXPECT(1535, "ruecklauf", "18.6");
    mem_set(31895, 0xFFFF, true); mem_set(31894, 0xFFFF, true);
    tests++; if (has_reg(1535) && has_reg(31894)) assert(!strcmp(st("ruecklauf"), ""));      /* Sentinel -> nichts */
    mem_set(31894, 0, true); mem_set(31895, 2000, true);
    tests++; if (has_reg(1535) && has_reg(31894)) assert(!strcmp(st("ruecklauf"), ""));      /* > 150 °C -> nichts */
    mem_set(1535, 190, true); EXPECT(1535, "ruecklauf", "19.0");
    /* Kaeltekreis: Gruppe stumm -> unknown; belegt -> Skala */
    if (has_reg(31903)) {
        mem_set(31903, 0, true); mem_set(31905, 0, true); mem_set(31907, 0, true); mem_set(31913, 0, true);
        mem_set(31915, 0, true); mem_set(31917, 0, true); mem_set(31921, 0, true);
        EXPECT(31903, "kk_lufteintritt", "unknown");
        mem_set(31903, 173, true); mem_set(31913, 648, true); mem_set(31915, 1264, true); mem_set(31905, -15, true);
        EXPECT(31903, "kk_lufteintritt", "17.3");
        EXPECT(31913, "kk_ueberhitzung", "6.48");
        EXPECT(31915, "kk_niederdruck", "12.64");
        EXPECT(31905, "kk_sauggas", "-1.5");
        EXPECT(31907, "kk_heissgas", "0.0");           /* einzelne 0 in antwortender Gruppe bleibt gueltig */
        mem_set(31917, 0x8000, true); EXPECT(31917, "kk_hochdruck", "unknown");
    }
    /* COP: 31667/31668 = 0 + FA 27490 = 43 -> Pel 0 -> Startfilter 0.0 ; Pel 1,2 kW -> 4.3 */
    if (has_reg(31667) && has_reg(27490) && has_reg(25611)) {
        char o[HA_STATE_MAX];
        mem_set(31667, 0, true); mem_set(31668, 0, true); mem_set(27490, 43, true);
        assert(ha_cop_state(fake_read, o, sizeof o) && !strcmp(o, "0.0"));
        mem_set(25611, 120, true);
        assert(ha_cop_state(fake_read, o, sizeof o) && !strcmp(o, "4.3"));
        mem_set(31668, 38, true);                                  /* nativ 3,8 hat Vorrang */
        assert(ha_cop_state(fake_read, o, sizeof o) && !strcmp(o, "3.8"));
        mem_set(31668, 250, true);                                 /* 25,0 unplausibel -> nichts */
        assert(!ha_cop_state(fake_read, o, sizeof o));
        mem_set(31668, 0, true); mem_set(27490, 250, true);        /* FA-Artefakt > 20 -> nichts */
        assert(!ha_cop_state(fake_read, o, sizeof o));
        mem_set(25611, 0, true);
    }
    /* Kuehl-Phasen (15c): 1501=22, 19870=1, 1539=0, VL 19,0 -> 1 ; VL 19,5 -> 2 ; 1539=2 -> 3 ; 1501=0 -> 0 */
    if (has_reg(1501) && has_reg(19870) && has_reg(1539) && has_reg(1525)) {
        int32_t vl;
        mem_set(19870, 1, true); mem_set(1539, 0, true); mem_set(1525, 190, true);
        assert(ha_kuehl_phase(fake_read, &vl) == 1 && vl == 190);
        mem_set(1525, 195, true); assert(ha_kuehl_phase(fake_read, &vl) == 2);
        mem_set(1539, 2, true);   assert(ha_kuehl_phase(fake_read, &vl) == 3);
        mem_set(1539, 0, true); mem_set(25611, 60, true); assert(ha_kuehl_phase(fake_read, &vl) == 3);   /* Pel >= 0,5 kW */
        mem_set(25611, 0, true); mem_set(1501, 0, true); assert(ha_kuehl_phase(fake_read, &vl) == 0);
        mem_set(1501, 22, true); mem_set(1525, 0x8000, true); assert(ha_kuehl_phase(fake_read, &vl) == -1);
        mem_set(1525, 190, true);
        ha_kuehl_attr_json(buf, sizeof buf, 2, 195);
        assert(!strcmp(buf, "{\"phase\":2,\"phase_txt\":\"Startmarke erreicht, Freigabe folgt\",\"vorlauf_c\":19.5,\"startmarke_c\":19.5}"));
        ha_kuehl_attr_json(buf, sizeof buf, 0, INT32_MIN); assert(strstr(buf, "\"vorlauf_c\":null"));
    }
    ha_stale_attr_json(buf, sizeof buf, 700, true, 10);  assert(strstr(buf, "\"reason\":\"can\"") && strstr(buf, "\"age_s\":700"));
    ha_stale_attr_json(buf, sizeof buf, 5, true, 10);    assert(strstr(buf, "\"reason\":\"ok\""));
    ha_stale_attr_json(buf, sizeof buf, 0, false, 10);   assert(strstr(buf, "\"reason\":\"can-nie\""));

    /* ---------- 3. Kommandos ---------- */
    {
        uint16_t w; const ha_ent_t *e;
        assert(ha_find_control("nix") == NULL);
        e = ha_find_control("set_bw_hk1"); assert(e);
        if (has_reg(1478)) {
            assert(ha_command(e, "Konstant", &w) == 0 && w == 4);
            assert(ha_command(e, "  Hand Kuehlen \n", &w) == 0 && w == 8);
            assert(ha_command(e, "Woche 3", &w) == -1);
            assert(ha_command(e, "4", &w) == -1);                       /* select nimmt nur Klartext */
        }
        e = ha_find_control("set_ww_normal"); assert(e);
        if (has_reg(1497)) {
            assert(ha_command(e, "52", &w) == 0 && w == 520);
            assert(ha_command(e, "52.0", &w) == 0 && w == 520);
            assert(ha_command(e, "52.05", &w) == 0 && w == 521);        /* round(520.5) -> 521 */
            assert(ha_command(e, "52.04", &w) == 0 && w == 520);
            assert(ha_command(e, " 48.5 ", &w) == 0 && w == 485);
            assert(ha_command(e, "abc", &w) == -1);
            assert(ha_command(e, "", &w) == -1);
            assert(ha_command(e, "52,0", &w) == -1);                    /* Komma nicht akzeptiert (HA sendet Punkt) */
        }
        e = ha_find_control("set_sg_off_kk1"); assert(e);
        if (has_reg(27531)) { assert(ha_command(e, "-2.5", &w) == 0 && w == (uint16_t)(-25 & 0xFFFF)); }
        e = ha_find_control("set_ww_eco"); assert(e);
        if (has_reg(1498)) { assert(ha_command(e, "45", &w) == 0 && w == 45); assert(ha_command(e, "45.6", &w) == 0 && w == 46); }
        /* Whitelist-Gate: 1497 ist in der Beispiel-/HoxPi-Liste, 1479 (HK2) auch; ein Test mit Override */
        assert(ha_control_enabled(ha_find_control("set_ww_normal")));
        static const uint16_t only[] = { 1561 };
        hp_whitelist_override(only, 1);
        assert(!ha_control_enabled(ha_find_control("set_ww_normal")) && ha_control_enabled(ha_find_control("set_bw_wez")));
        hp_whitelist_override(NULL, 0);
        assert(ha_control_enabled(ha_find_control("set_ww_normal")));
    }
    /* ---------- Zahlformat ---------- */
    { char o[24];
      ha_fmt_scaled(o, sizeof o, -5, 1);   assert(!strcmp(o, "-0.5"));
      ha_fmt_scaled(o, sizeof o, 5, 2);    assert(!strcmp(o, "0.05"));
      ha_fmt_scaled(o, sizeof o, -1270, 1); assert(!strcmp(o, "-127.0"));
      ha_fmt_scaled(o, sizeof o, 12345, 3); assert(!strcmp(o, "12.345"));
      ha_fmt_scaled(o, sizeof o, 7, 0);    assert(!strcmp(o, "7")); }

    printf("HA ok: %u Sensoren + %u Steuerungen definiert, %d Discovery-Payloads geschrieben, %d Zustandsfaelle (%d ohne Tabellenzeile uebersprungen)\n",
           ha_sensors_n, ha_controls_n, n_disc, tests, skipped);
    return 0;
}
