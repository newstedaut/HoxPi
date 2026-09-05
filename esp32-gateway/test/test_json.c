/*
 * test_json.c — Host-Test fuer hoval_json.c (Statusseite): /status- und /config-JSON, /register,
 * POST-Body-Zerlegung (Zahlen, true/false, Whitelist als Text/Liste, Fehlerfaelle, Grenzen),
 * Abschneide-Erkennung, OTA (URL-Pruefung, /ota-Body, /ota-JSON). Ohne ESP-IDF (gcc). Die JSON-Ausgabe wird zusaetzlich mit Python
 * (json.loads) gegengeprueft, wenn `python3` vorhanden ist — siehe Makefile-Ziel test.
 */
#include <stdio.h>
#include <string.h>
#include <assert.h>
#include <stdlib.h>
#include "hoval_json.h"
#include "hoval_cfg.h"
#include "hoval_proto.h"
#include "hoval_ota.h"

/* Register-Attrappe: 1501 = 22 gesehen, 1477 = -3,2 °C gesehen, 1534 nie gelesen, Rest wie Tabelle */
static bool fake_read(uint16_t reg, uint16_t *word, bool *seen)
{
    if (!hp_find_reg(reg)) return false;
    *seen = (reg == 1501 || reg == 1477);
    if (reg == 1501) *word = 22;
    if (reg == 1477) *word = (uint16_t)(-32 & 0xFFFF);
    return true;
}

static int has(const char *hay, const char *needle) { return strstr(hay, needle) != NULL; }

static void write_file(const char *name, const char *s) { FILE *f = fopen(name, "w"); assert(f); fputs(s, f); fclose(f); }

int main(void)
{
    static char out[8192];
    hcfg_t *c = hcfg_mut();
    hcfg_defaults(c, 30, 5, 100, false);
    hcfg_apply(c, NULL);

    /* --- /status --- */
    hj_status_in_t in = {
        .version = "test-0.4", .uptime_s = 3661, .heap_free = 123456,
        .rx_frames = 1000, .rx_msgs = 900, .decoded = 850, .tx_frames = 7, .tx_errors = 1, .bus_off = 0,
        .have_rx = true, .last_rx_age_s = 12, .modbus_port = 502, .write_enabled = false,
        .regs_count = hp_regs_count, .areas_count = hp_areas_count, .cfg = hcfg_get(), .wl_active_n = 0,
        .restart_required = false,
        .mqtt_enabled = false,
    };
    size_t n = hj_status_json(out, sizeof out, &in, fake_read);
    assert(n > 0 && n < sizeof out && strlen(out) == n);
    assert(has(out, "\"gateway\":\"hoxpi-esp32\"") && has(out, "\"version\":\"test-0.4\""));
    assert(has(out, "\"uptime_s\":3661") && has(out, "\"rx_frames\":1000") && has(out, "\"bus_off\":0"));
    assert(has(out, "\"last_rx_age_s\":12,\"stale\":false"));
    assert(has(out, "\"modbus\":{\"port\":502,\"write_enabled\":false}"));
    assert(has(out, "\"mqtt\":{\"enabled\":false},\"config\":{"));            /* aus: keine Zaehler */
    assert(has(out, "\"poll_wez\":30,\"poll_hv\":5,\"poll_delay\":100,\"wr_en\":false"));
    assert(has(out, "\"whitelist_src\":\"compiled\""));
    assert(has(out, "\"1501\":{\"type\":\"U8\",\"dec\":0,\"seen\":true,\"raw\":22,\"val\":22}"));
    assert(has(out, "\"1477\":{\"type\":\"S16\",\"dec\":1,\"seen\":true,\"raw\":65504,\"val\":-32}"));   /* S16-Sicht */
    assert(has(out, "\"1534\":{\"type\":\"U8\",\"dec\":0,\"seen\":false,\"raw\":null,\"val\":null}"));
    write_file("out_status.json", out);
    printf("STATUS %zu Bytes\n", n);

    /* stale: nie ein Datenpunkt bzw. > 10 min */
    in.have_rx = false;
    hj_status_json(out, sizeof out, &in, NULL);
    assert(has(out, "\"last_rx_age_s\":null,\"stale\":true") && !has(out, "\"values\""));
    in.have_rx = true; in.last_rx_age_s = 601;
    hj_status_json(out, sizeof out, &in, NULL);
    assert(has(out, "\"stale\":true"));

    /* MQTT an: hmq_stats()-Zaehler erscheinen (Vorbild: Exporter hoxpi_mqtt_* / Dashboard-Karte) */
    in.mqtt_enabled = true; in.mqtt_connected = true;
    in.mqtt_pub_ok = 4711; in.mqtt_pub_fail = 2; in.mqtt_cmd_ok = 3; in.mqtt_cmd_rej = 1;
    hj_status_json(out, sizeof out, &in, NULL);
    assert(has(out, "\"mqtt\":{\"enabled\":true,\"connected\":true,\"pub_ok\":4711,\"pub_fail\":2,\"cmd_ok\":3,\"cmd_rej\":1}"));
    in.mqtt_connected = false;
    hj_status_json(out, sizeof out, &in, NULL);
    assert(has(out, "\"enabled\":true,\"connected\":false,"));
    in.mqtt_enabled = false;

    /* Abschneiden: Rueckgabe >= cap, Puffer bleibt NUL-terminiert */
    char small[64];
    n = hj_status_json(small, sizeof small, &in, fake_read);
    assert(n >= sizeof small && strlen(small) == sizeof small - 1);

    /* --- /config --- */
    n = hj_config_json(out, sizeof out, hcfg_get(), 0, false, false);
    assert(n < sizeof out && out[0] == '{' && out[n - 1] == '}');
    assert(has(out, "\"whitelist_n\":25") && has(out, "\"whitelist\":[1478,1479,") && has(out, "\"from_nvs\":{\"poll_wez\":false"));
    write_file("out_config.json", out);

    /* --- /register --- */
    assert(hj_register_json(out, sizeof out, 1490, fake_read));
    assert(has(out, "\"reg\":1490,\"unit\":1,\"fg\":1,\"fn\":0,\"dp\":7036,\"type\":\"S16\",\"dec\":1,\"writable\":true"));
    assert(has(out, "\"whitelist\":true") && has(out, "\"min\":100,\"max\":1100") && has(out, "\"seen\":false"));
    assert(hj_register_json(out, sizeof out, 1477, fake_read));
    assert(!has(out, "\"min\"") && has(out, "\"raw\":65504,\"val\":-32"));
    assert(!hj_register_json(out, sizeof out, 9, fake_read) && has(out, "\"error\""));
    write_file("out_register.json", out);

    /* --- POST /config: Zahlen + Whitelist-Text --- */
    hcfg_t t; char err[96];
    hcfg_defaults(&t, 30, 5, 100, false);
    int ch = hj_parse_config("{\"poll_wez\": 60, \"poll_hv\":2,\"poll_delay\":250,\"wr_en\":true,\"whitelist\":\"1490, 1497\"}", &t, err, sizeof err);
    assert(ch == (HCFG_SRC_POLL_WEZ | HCFG_SRC_POLL_HV | HCFG_SRC_POLL_DELAY | HCFG_SRC_WR_EN | HCFG_SRC_WHITELIST));
    assert(t.poll_wez_s == 60 && t.poll_hv_s == 2 && t.poll_delay_ms == 250 && t.enable_write);
    assert(t.wl_override && t.wl_n == 2 && t.wl[0] == 1490 && t.wl[1] == 1497);

    /* Whitelist als Zahlenliste, wr_en als 0, Zahl in Anfuehrungszeichen */
    hcfg_defaults(&t, 30, 5, 100, true);
    ch = hj_parse_config("{ \"whitelist\" : [ 1497 , 27509,1490 ], \"wr_en\":0, \"poll_wez\":\"45\" }", &t, err, sizeof err);
    assert(ch == (HCFG_SRC_WHITELIST | HCFG_SRC_WR_EN | HCFG_SRC_POLL_WEZ));
    assert(!t.enable_write && t.poll_wez_s == 45 && t.wl_n == 3 && t.wl[0] == 1497 && t.wl[1] == 27509 && t.wl[2] == 1490);

    /* leere Whitelist = nichts schreibbar (Override aktiv, 0 Eintraege) */
    hcfg_defaults(&t, 30, 5, 100, false);
    assert(hj_parse_config("{\"whitelist\":\"\"}", &t, err, sizeof err) == HCFG_SRC_WHITELIST && t.wl_override && t.wl_n == 0);
    hcfg_defaults(&t, 30, 5, 100, false);
    assert(hj_parse_config("{\"whitelist\":[]}", &t, err, sizeof err) == HCFG_SRC_WHITELIST && t.wl_override && t.wl_n == 0);

    /* Teilupdate laesst den Rest stehen */
    hcfg_defaults(&t, 30, 5, 100, false);
    assert(hj_parse_config("{\"poll_hv\":10}", &t, err, sizeof err) == HCFG_SRC_POLL_HV && t.poll_wez_s == 30 && t.poll_hv_s == 10 && !t.wl_override);

    /* Fehler: Grenzen, keine Zahl, kaputte Whitelist, unbekannte Schluessel -> Konfig unveraendert */
    hcfg_defaults(&t, 30, 5, 100, false);
    assert(hj_parse_config("{\"poll_wez\":4}", &t, err, sizeof err) == -1 && has(err, "Grenzen") && t.poll_wez_s == 30);
    assert(hj_parse_config("{\"poll_wez\":60,\"poll_hv\":0}", &t, err, sizeof err) == -1 && t.poll_wez_s == 30);   /* alles oder nichts */
    assert(hj_parse_config("{\"poll_delay\":\"abc\"}", &t, err, sizeof err) == -1 && has(err, "Zahl"));
    assert(hj_parse_config("{\"wr_en\":2}", &t, err, sizeof err) == -1);
    assert(hj_parse_config("{\"whitelist\":\"1490,x\"}", &t, err, sizeof err) == -1 && has(err, "Syntax") && !t.wl_override);
    assert(hj_parse_config("{\"whitelist\":[1490,\"x\"]}", &t, err, sizeof err) == -1);
    assert(hj_parse_config("{\"whitelist\":42}", &t, err, sizeof err) == -1);
    assert(hj_parse_config("{\"foo\":1}", &t, err, sizeof err) == 0);
    assert(hj_parse_config("", &t, err, sizeof err) == 0);
    assert(hj_parse_config(NULL, &t, err, sizeof err) == -1);
    /* Schluessel als Wert darf nicht anspringen: {"name":"poll_wez"} */
    assert(hj_parse_config("{\"name\":\"poll_wez\"}", &t, err, sizeof err) == 0);
    /* Ueberlauf: 129 Eintraege */
    {
        char big[HCFG_WL_TEXT_MAX + 64]; size_t p = 0;
        p += (size_t)snprintf(big + p, sizeof big - p, "{\"whitelist\":\"");
        for (int i = 0; i < HCFG_WL_MAX + 1 && p < sizeof big - 16; i++) p += (size_t)snprintf(big + p, sizeof big - p, "%s%d", i ? "," : "", 1000 + i);
        snprintf(big + p, sizeof big - p, "\"}");
        assert(hj_parse_config(big, &t, err, sizeof err) == -1 && !t.wl_override);
    }

    /* Rundlauf: geparste Konfig anwenden -> /config zeigt sie (Whitelist-Validierung wirft Unbekannte raus) */
    hcfg_defaults(c, 30, 5, 100, false);
    assert(hj_parse_config("{\"poll_wez\":90,\"whitelist\":[1490,1497,60000]}", c, err, sizeof err) > 0);
    size_t dropped = hcfg_apply(c, NULL);
    assert(dropped == 1);
    uint16_t wn = 0; hp_whitelist_active(&wn);
    n = hj_config_json(out, sizeof out, hcfg_get(), wn, false, false);
    assert(has(out, "\"poll_wez\":90") && has(out, "\"whitelist_n\":2,\"whitelist_src\":\"nvs\",\"whitelist\":[1490,1497]"));
    assert(has(out, "\"from_nvs\":{\"poll_wez\":true,\"poll_hv\":false") && has(out, "\"whitelist\":true}"));
    assert(hp_in_whitelist(1490) && !hp_in_whitelist(1478));
    hp_whitelist_override(NULL, 0);

    /* --- OTA: URL-Pruefung --- */
    {
        char u[HOTA_URL_MAX], err[120];
        assert( hj_check_ota_url("https://example.org/fw/hoxpi_esp32.bin", false, u, sizeof u, err, sizeof err) && !strcmp(u, "https://example.org/fw/hoxpi_esp32.bin"));
        assert(!hj_check_ota_url("http://192.168.1.168:8000/hoxpi_esp32.bin", false, u, sizeof u, err, sizeof err) && has(err, "https"));
        assert( hj_check_ota_url("http://192.168.1.168:8000/hoxpi_esp32.bin", true,  u, sizeof u, err, sizeof err));
        assert(!hj_check_ota_url("ftp://x/y.bin", true, u, sizeof u, err, sizeof err) && has(err, "https://"));
        assert(!hj_check_ota_url("https:///y.bin", true, u, sizeof u, err, sizeof err) && has(err, "Host"));
        assert(!hj_check_ota_url("https://", true, u, sizeof u, err, sizeof err) && has(err, "Host"));
        assert(!hj_check_ota_url("", true, u, sizeof u, err, sizeof err) && has(err, "fehlt"));
        assert(!hj_check_ota_url(NULL, true, u, sizeof u, err, sizeof err));
        assert(!hj_check_ota_url("https://h/a b.bin", true, u, sizeof u, err, sizeof err) && has(err, "Position 11"));
        assert(!hj_check_ota_url("https://h/a\"b.bin", true, u, sizeof u, err, sizeof err) && has(err, "Zeichen"));
        assert(!hj_check_ota_url("https://h/\xc3\xa4.bin", true, u, sizeof u, err, sizeof err) && has(err, "Zeichen"));
        char lang[HOTA_URL_MAX + 40]; memset(lang, 'a', sizeof lang - 1); lang[sizeof lang - 1] = 0; memcpy(lang, "https://", 8);
        assert(!hj_check_ota_url(lang, true, u, sizeof u, err, sizeof err) && has(err, "laenger"));
        char genau[HOTA_URL_MAX]; memset(genau, 'a', sizeof genau - 1); genau[sizeof genau - 1] = 0; memcpy(genau, "https://", 8);
        assert( hj_check_ota_url(genau, true, u, sizeof u, err, sizeof err) && strlen(u) == HOTA_URL_MAX - 1);

        /* --- /ota-Body --- */
        assert( hj_parse_ota("{\"url\":\"https://h/x.bin\"}", u, sizeof u, err, sizeof err) && !strcmp(u, "https://h/x.bin"));
        assert( hj_parse_ota("{ \"foo\" : 1 , \"url\" : \"https://h/x.bin\" }", u, sizeof u, err, sizeof err) && !strcmp(u, "https://h/x.bin"));
        assert(!hj_parse_ota("{\"uri\":\"https://h/x.bin\"}", u, sizeof u, err, sizeof err) && has(err, "fehlt"));
        assert(!hj_parse_ota("{\"url\":42}", u, sizeof u, err, sizeof err) && has(err, "Zeichenkette"));
        assert(!hj_parse_ota("{\"url\":\"https://h/x.bin}", u, sizeof u, err, sizeof err) && has(err, "geschlossen"));
        assert(!hj_parse_ota(NULL, u, sizeof u, err, sizeof err));
        assert( hj_parse_ota("{\"url\":\"\"}", u, sizeof u, err, sizeof err) && !u[0]);      /* leer: Body ok, URL-Pruefung lehnt ab */
        assert(!hj_check_ota_url(u, true, u, sizeof u, err, sizeof err));
        char body[HOTA_URL_MAX + 60]; snprintf(body, sizeof body, "{\"url\":\"%s\"}", lang);
        assert(!hj_parse_ota(body, u, sizeof u, err, sizeof err) && has(err, "laenger"));

        /* --- /ota-JSON --- */
        hota_info_t oi = { .enabled = true, .running = "ota_0", .boot = "ota_1", .app_version = "v0.6-3-gabc", .app_date = "Sep  5 2026",
                           .pending_verify = false, .state = HOTA_OK, .bytes = 1234567, .total = 1234567, .error = "",
                           .started_s = 100, .finished_s = 160 };
        strcpy(oi.url, "https://h/x.bin");
        n = hj_ota_json(out, sizeof out, &oi);
        assert(n < sizeof out && strlen(out) == n);
        assert(has(out, "\"enabled\":true,\"running\":\"ota_0\",\"boot\":\"ota_1\",\"app_version\":\"v0.6-3-gabc\""));
        assert(has(out, "\"pending_verify\":false,\"state\":\"ok\",\"url\":\"https://h/x.bin\",\"bytes\":1234567,\"total\":1234567"));
        assert(has(out, "\"started_s\":100,\"finished_s\":160,\"error\":\"\"}"));
        write_file("out_ota.json", out);
        hota_info_t oi2 = { .enabled = false, .running = "factory", .boot = "factory", .app_version = "", .app_date = "",
                            .pending_verify = true, .state = HOTA_IDLE, .total = -1, .error = "" };
        n = hj_ota_json(out, sizeof out, &oi2);
        assert(has(out, "\"enabled\":false") && has(out, "\"pending_verify\":true,\"state\":\"idle\",\"error\":\"\"}") && !has(out, "\"url\""));
        hota_info_t oi3 = oi; oi3.state = HOTA_FAILED; oi3.total = -1; oi3.finished_s = 0; oi3.error = "begin: ESP_ERR_HTTP_CONNECT \"x\"";
        n = hj_ota_json(out, sizeof out, &oi3);
        assert(has(out, "\"state\":\"failed\"") && has(out, "\"total\":null") && has(out, "\"finished_s\":null") && has(out, "\\\"x\\\""));
        write_file("out_ota_failed.json", out);
        assert(hj_ota_json(out, 20, &oi) > 20);                                   /* Abschneide-Erkennung */
        printf("OTA OK (URL 13 Faelle, Body 8, JSON 3)\n");
    }

    printf("JSON OK (status/config/register, 20 POST-Faelle)\n");
    return 0;
}
