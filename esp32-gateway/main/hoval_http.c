/*
 * hoval_http.c — Status-/Konfigseite auf esp_http_server (ESP-IDF >= 5.3). Routen siehe hoval_http.h.
 * JSON-Aufbau + Body-Zerlegung liegen in hoval_json.c (host-getestet); hier nur Transport, Token,
 * NVS-Sicherung und die statische HTML-Seite. Noch NICHT auf Hardware getestet (05.09.2026, kein Board).
 */
#include "hoval_http.h"
#include "hoval_json.h"
#include "hoval_cfg.h"
#include "hoval_proto.h"
#include "hoval_can.h"
#include "hoval_modbus.h"
#include "hoval_mqtt.h"
#include "hoval_ota.h"
#include <string.h>
#include <stdlib.h>
#include "esp_log.h"
#include "esp_err.h"
#include "esp_timer.h"
#include "esp_system.h"
#include "esp_http_server.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "sdkconfig.h"

#ifndef CONFIG_HOXPI_HTTP_PORT
#define CONFIG_HOXPI_HTTP_PORT 80
#endif
#ifndef CONFIG_HOXPI_HTTP_TOKEN
#define CONFIG_HOXPI_HTTP_TOKEN ""
#endif
#ifndef CONFIG_HOXPI_MODBUS_PORT
#define CONFIG_HOXPI_MODBUS_PORT 502
#endif

#define HH_VERSION   "esp32-0.6"
#define HH_BODY_MAX  (HCFG_WL_TEXT_MAX + 256)   /* laengster sinnvoller /config-Body */
#define HH_OUT_MAX   4096                        /* /status mit voller Whitelist (128 Eintraege) < 3 KB */

static const char *TAG = "hoval_http";
static bool s_write_effective;
static httpd_handle_t s_srv;

/* ---- Hilfen ---------------------------------------------------------------- */
static bool read_cb(uint16_t reg, uint16_t *word, bool *seen)
{
    if (!hm_read(reg, word)) return false;
    *seen = hc_seen(reg);
    return true;
}

static esp_err_t send_json(httpd_req_t *req, const char *status, const char *body)
{
    httpd_resp_set_status(req, status);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_set_hdr(req, "Cache-Control", "no-store");
    return httpd_resp_send(req, body, HTTPD_RESP_USE_STRLEN);
}

static esp_err_t send_error(httpd_req_t *req, const char *status, const char *msg)
{
    char buf[200];
    snprintf(buf, sizeof buf, "{\"error\":\"%s\"}", msg);
    return send_json(req, status, buf);
}

/* POST-Schutz: Token-Header muss dem Kconfig-Token entsprechen; leeres Token = POST gesperrt */
static bool check_token(httpd_req_t *req)
{
    const char *want = CONFIG_HOXPI_HTTP_TOKEN;
    if (!want[0]) { send_error(req, "403 Forbidden", "POST gesperrt: HOXPI_HTTP_TOKEN ist leer (menuconfig)"); return false; }
    char got[65] = { 0 };
    if (httpd_req_get_hdr_value_str(req, "X-Token", got, sizeof got) != ESP_OK || strcmp(got, want) != 0) {
        send_error(req, "401 Unauthorized", "X-Token fehlt oder falsch");
        return false;
    }
    return true;
}

static bool restart_required(void)
{
    /* wr_en in der (NVS-)Konfiguration weicht vom beim Start uebernommenen Schreibpfad ab */
    return hcfg_get()->enable_write != s_write_effective;
}

/* ---- Routen ---------------------------------------------------------------- */
static const char INDEX_HTML[] =
"<!doctype html><html lang=de><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
"<title>HoxPi-ESP32</title><style>body{font:15px system-ui,sans-serif;margin:1.5em;max-width:46em}"
"h1{font-size:1.3em}table{border-collapse:collapse}td{padding:.15em .8em .15em 0}code{background:#eee;padding:0 .3em}"
".warn{color:#b00}.ok{color:#080}</style>"
"<h1>HoxPi-ESP32 Gateway</h1><p id=s>lade /status …</p><table id=t></table>"
"<p>Konfiguration: <code>GET /config</code>, aendern: <code>POST /config</code> mit Header <code>X-Token</code>"
" (Body z.&nbsp;B. <code>{\"poll_wez\":60,\"whitelist\":\"1490,1497\"}</code>). Register: <code>/register?reg=1501</code>."
" Firmware: <code>POST /ota</code> mit <code>{\"url\":\"https://…/hoxpi_esp32.bin\"}</code>, Zustand <code>GET /ota</code>.</p>"
"<script>"
"const N={1501:'Betriebsmodus',1534:'Fehlercode (255=ok, 0=kein Wert)',1477:'Aussen °C',1525:'WP-Vorlauf °C',1535:'WP-Ruecklauf °C',"
"1500:'WW Ist °C',1499:'WW Soll °C',1537:'Modulation %',25611:'Pel kW',27490:'COP'};"
"function f(v,d){return v==null?'—':(d>0?(v/Math.pow(10,d)).toFixed(d):v)}"
"fetch('/status').then(r=>r.json()).then(j=>{"
"document.getElementById('s').innerHTML=`Version ${j.version}, Laufzeit ${Math.floor(j.uptime_s/60)} min, Heap ${j.heap_free} B, "
"CAN rx ${j.can.rx_frames} / dekodiert ${j.can.decoded} / tx ${j.can.tx_frames} (Fehler ${j.can.tx_errors}, bus-off ${j.can.bus_off}) — "
"<span class='${j.can.stale?'warn':'ok'}'>${j.can.stale?'STALE: keine Hoval-Antwort':'CAN lebt, letzter DP vor '+j.can.last_rx_age_s+' s'}</span><br>"
"Modbus-TCP :${j.modbus.port}, Schreiben ${j.modbus.write_enabled?'AN':'AUS'}${j.config.restart_required?' <span class=warn>(NVS abweichend – Neustart noetig)</span>':''}, "
"Whitelist ${j.config.whitelist_n} Register (${j.config.whitelist_src}), Poll WEZ ${j.config.poll_wez} s / HV ${j.config.poll_hv} s / Abstand ${j.config.poll_delay} ms, "
"Tabelle ${j.table.registers} Register in ${j.table.areas} Bereichen<br>"
"MQTT ${!j.mqtt.enabled?'aus':`<span class='${j.mqtt.connected?'ok':'warn'}'>${j.mqtt.connected?'verbunden':'GETRENNT'}</span>, "
"publiziert ${j.mqtt.pub_ok} (Fehler ${j.mqtt.pub_fail}), Kommandos ${j.mqtt.cmd_ok} ok / ${j.mqtt.cmd_rej} abgelehnt`}`;"
"fetch('/ota').then(r=>r.json()).then(o=>{document.getElementById('s').innerHTML+=`<br>Firmware ${o.app_version} (${o.app_date}) auf ${o.running}${o.pending_verify?' <span class=warn>NEU – wartet auf CAN-Bestaetigung</span>':''}, OTA ${o.enabled?'an':'aus'}, letztes Update: ${o.state}${o.error?' – '+o.error:''}`}).catch(()=>{});"
"let h='';for(const r in j.values){const v=j.values[r];h+=`<tr><td>${r}</td><td>${N[r]||''}</td><td>${f(v.val,v.dec)}</td><td>${v.seen?'':'<span class=warn>nie gelesen</span>'}</td></tr>`}"
"document.getElementById('t').innerHTML=h}).catch(e=>{document.getElementById('s').textContent='Fehler: '+e})"
"</script>";

static esp_err_t h_index(httpd_req_t *req)
{
    httpd_resp_set_type(req, "text/html; charset=utf-8");
    return httpd_resp_send(req, INDEX_HTML, HTTPD_RESP_USE_STRLEN);
}

static esp_err_t h_status(httpd_req_t *req)
{
    const hc_stats_t *s = hc_stats();
    uint32_t now_ms = (uint32_t)(esp_timer_get_time() / 1000);
    uint16_t wn = 0; hp_whitelist_active(&wn);
    hmq_stats_t mq = { 0 }; hmq_stats(&mq);
    hj_status_in_t in = {
        .version = HH_VERSION,
        .uptime_s = now_ms / 1000,
        .heap_free = (uint32_t)esp_get_free_heap_size(),
        .rx_frames = s->rx_frames, .rx_msgs = s->rx_msgs, .decoded = s->decoded,
        .tx_frames = s->tx_frames, .tx_errors = s->tx_errors, .bus_off = s->bus_off,
        .have_rx = s->last_rx_ms != 0,
        .last_rx_age_s = s->last_rx_ms ? (now_ms - s->last_rx_ms) / 1000 : 0,
        .modbus_port = CONFIG_HOXPI_MODBUS_PORT,
        .write_enabled = s_write_effective,
        .regs_count = hp_regs_count, .areas_count = hp_areas_count,
        .cfg = hcfg_get(), .wl_active_n = wn,
        .restart_required = restart_required(),
        .mqtt_enabled = hmq_enabled(), .mqtt_connected = mq.connected,
        .mqtt_pub_ok = mq.pub_ok, .mqtt_pub_fail = mq.pub_fail, .mqtt_cmd_ok = mq.cmd_ok, .mqtt_cmd_rej = mq.cmd_rej,
    };
    char *out = malloc(HH_OUT_MAX);
    if (!out) return send_error(req, "500 Internal Server Error", "kein Speicher");
    size_t n = hj_status_json(out, HH_OUT_MAX, &in, read_cb);
    esp_err_t r = n < HH_OUT_MAX ? send_json(req, "200 OK", out) : send_error(req, "500 Internal Server Error", "Antwort zu lang");
    free(out);
    return r;
}

static esp_err_t send_config(httpd_req_t *req, const char *status)
{
    char *out = malloc(HH_OUT_MAX);
    if (!out) return send_error(req, "500 Internal Server Error", "kein Speicher");
    uint16_t wn = 0; hp_whitelist_active(&wn);
    size_t n = hj_config_json(out, HH_OUT_MAX, hcfg_get(), wn, s_write_effective, restart_required());
    esp_err_t r = n < HH_OUT_MAX ? send_json(req, status, out) : send_error(req, "500 Internal Server Error", "Antwort zu lang");
    free(out);
    return r;
}

static esp_err_t h_config_get(httpd_req_t *req) { return send_config(req, "200 OK"); }

static void cfg_warn(const char *msg, uint16_t reg) { ESP_LOGW(TAG, "%s: reg %u", msg, reg); }

static esp_err_t h_config_post(httpd_req_t *req)
{
    if (!check_token(req)) return ESP_OK;
    if (req->content_len == 0 || req->content_len > HH_BODY_MAX) return send_error(req, "400 Bad Request", "Body fehlt oder zu lang");
    char *body = malloc(req->content_len + 1);
    if (!body) return send_error(req, "500 Internal Server Error", "kein Speicher");
    size_t got = 0;
    while (got < req->content_len) {
        int r = httpd_req_recv(req, body + got, req->content_len - got);
        if (r <= 0) { free(body); return send_error(req, "400 Bad Request", "Body unvollstaendig"); }
        got += (size_t)r;
    }
    body[got] = 0;

    char err[96];
    hcfg_t neu = *hcfg_get();
    int changed = hj_parse_config(body, &neu, err, sizeof err);
    free(body);
    if (changed < 0)  return send_error(req, "400 Bad Request", err);
    if (changed == 0) return send_error(req, "400 Bad Request", "kein bekannter Schluessel (poll_wez, poll_hv, poll_delay, wr_en, whitelist)");

    /* live anwenden (Whitelist wird dabei gegen die Tabelle validiert), dann sichern */
    *hcfg_mut() = neu;
    size_t dropped = hcfg_apply(hcfg_mut(), cfg_warn);
    bool saved = hcfg_nvs_save(hcfg_get());
    uint16_t wn = 0; hp_whitelist_active(&wn);
    ESP_LOGI(TAG, "Konfig per HTTP geaendert (Maske 0x%02x): Poll WEZ %u s, HV %u s, Abstand %u ms, wr_en %u, Whitelist %u Register%s, NVS %s",
             changed, hcfg_get()->poll_wez_s, hcfg_get()->poll_hv_s, hcfg_get()->poll_delay_ms, hcfg_get()->enable_write, wn,
             dropped ? " (Eintraege verworfen)" : "", saved ? "gesichert" : "NICHT gesichert");
    if (!saved) return send_error(req, "500 Internal Server Error", "angewendet, aber NVS-Sicherung fehlgeschlagen");
    return send_config(req, "200 OK");
}

static esp_err_t h_config_reset(httpd_req_t *req)
{
    if (!check_token(req)) return ESP_OK;
    bool ok = hcfg_nvs_reset();
    ESP_LOGW(TAG, "NVS-Konfiguration per HTTP geloescht (%s) - Kompilat-Defaults ab dem naechsten Start", ok ? "ok" : "FEHLER");
    return ok ? send_json(req, "200 OK", "{\"reset\":true,\"restart_required\":true}")
              : send_error(req, "500 Internal Server Error", "NVS-Reset fehlgeschlagen");
}

static void restart_task(void *arg) { (void)arg; vTaskDelay(pdMS_TO_TICKS(500)); esp_restart(); }

static esp_err_t h_restart(httpd_req_t *req)
{
    if (!check_token(req)) return ESP_OK;
    ESP_LOGW(TAG, "Neustart per HTTP");
    esp_err_t r = send_json(req, "200 OK", "{\"restart\":true}");
    xTaskCreate(restart_task, "hh_restart", 2048, NULL, 5, NULL);
    return r;
}

static esp_err_t send_ota(httpd_req_t *req, const char *status)
{
    hota_info_t i; hota_info(&i);
    char out[600];
    size_t n = hj_ota_json(out, sizeof out, &i);
    return n < sizeof out ? send_json(req, status, out) : send_error(req, "500 Internal Server Error", "Antwort zu lang");
}

static esp_err_t h_ota_get(httpd_req_t *req) { return send_ota(req, "200 OK"); }

static esp_err_t h_ota_post(httpd_req_t *req)
{
    if (!check_token(req)) return ESP_OK;
    if (req->content_len == 0 || req->content_len > 512) return send_error(req, "400 Bad Request", "Body fehlt oder zu lang");
    char body[513];
    size_t got = 0;
    while (got < req->content_len) {
        int r = httpd_req_recv(req, body + got, req->content_len - got);
        if (r <= 0) return send_error(req, "400 Bad Request", "Body unvollstaendig");
        got += (size_t)r;
    }
    body[got] = 0;
    char url[HOTA_URL_MAX], err[120];
    if (!hj_parse_ota(body, url, sizeof url, err, sizeof err)) return send_error(req, "400 Bad Request", err);
    if (!hota_start(url, err, sizeof err)) {
        bool busy = strstr(err, "bereits") != NULL;
        return send_error(req, busy ? "409 Conflict" : "400 Bad Request", err);
    }
    ESP_LOGW(TAG, "Firmware-Update per HTTP angestossen: %s", url);
    return send_ota(req, "202 Accepted");
}

static esp_err_t h_register(httpd_req_t *req)
{
    char q[32], v[8];
    if (httpd_req_get_url_query_str(req, q, sizeof q) != ESP_OK || httpd_query_key_value(q, "reg", v, sizeof v) != ESP_OK)
        return send_error(req, "400 Bad Request", "?reg=N fehlt");
    char *end; long reg = strtol(v, &end, 10);
    if (*end || reg < 0 || reg > 65535) return send_error(req, "400 Bad Request", "reg ungueltig");
    char out[400];
    bool ok = hj_register_json(out, sizeof out, (uint16_t)reg, read_cb);
    return send_json(req, ok ? "200 OK" : "404 Not Found", out);
}

bool hh_start(bool modbus_write_effective)
{
    s_write_effective = modbus_write_effective;
    httpd_config_t cfg = HTTPD_DEFAULT_CONFIG();
    cfg.server_port = CONFIG_HOXPI_HTTP_PORT;
    cfg.max_uri_handlers = 12;
    cfg.lru_purge_enable = true;
    if (httpd_start(&s_srv, &cfg) != ESP_OK) { ESP_LOGE(TAG, "httpd_start :%d fehlgeschlagen", CONFIG_HOXPI_HTTP_PORT); return false; }
    const httpd_uri_t routes[] = {
        { .uri = "/",             .method = HTTP_GET,  .handler = h_index },
        { .uri = "/status",       .method = HTTP_GET,  .handler = h_status },
        { .uri = "/config",       .method = HTTP_GET,  .handler = h_config_get },
        { .uri = "/config",       .method = HTTP_POST, .handler = h_config_post },
        { .uri = "/config/reset", .method = HTTP_POST, .handler = h_config_reset },
        { .uri = "/restart",      .method = HTTP_POST, .handler = h_restart },
        { .uri = "/ota",          .method = HTTP_GET,  .handler = h_ota_get },
        { .uri = "/ota",          .method = HTTP_POST, .handler = h_ota_post },
        { .uri = "/register",     .method = HTTP_GET,  .handler = h_register },
    };
    for (size_t i = 0; i < sizeof routes / sizeof routes[0]; i++) httpd_register_uri_handler(s_srv, &routes[i]);
    ESP_LOGI(TAG, "Statusseite http://<ip>:%d/  (/status, /config, /register?reg=N, /ota; POST %s)",
             CONFIG_HOXPI_HTTP_PORT, CONFIG_HOXPI_HTTP_TOKEN[0] ? "mit X-Token" : "GESPERRT - HOXPI_HTTP_TOKEN leer");
    return true;
}
