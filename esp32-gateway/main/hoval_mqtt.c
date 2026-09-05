/*
 * hoval_mqtt.c — MQTT/Home-Assistant-Anbindung (esp-mqtt), Gegenstueck zu mqtt/hoval_mqtt.py
 *
 * Ablauf: hmq_start() legt den Client an (URI/User/Passwort aus Kconfig, LWT hoval/bridge/status = offline)
 * und startet einen Task. Der Ereignis-Handler setzt nur Flags (CONNECTED -> Discovery faellig) und reicht
 * Kommandos (hoval/<key>/set) an hm_write() weiter, das denselben Pruefpfad wie ein Modbus-Schreibzugriff
 * nimmt (Schreibfreigabe, Whitelist, Kalt-Cache, min/max, Rate-Limit, Kanal-Exklusion). Der Task publiziert
 * alle CONFIG_HOXPI_MQTT_INTERVAL_S Sekunden die Zustaende (retain) und erneuert die Discovery, wenn sich
 * die aktive Whitelist aendert (POST /config) — wie hoval_mqtt.py bei geaenderter whitelist.json.
 *
 * Nicht auf Hardware getestet (05.09.2026, kein Board): esp-mqtt-API nach ESP-IDF 5.3 (broker.address.uri,
 * credentials.*, session.last_will). Payload-Aufbau ist in hoval_ha.c und wird auf dem Host geprueft.
 */
#include <string.h>
#include <stdio.h>
#include <inttypes.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "esp_timer.h"
#include "mqtt_client.h"
#include "sdkconfig.h"
#include "hoval_mqtt.h"
#include "hoval_ha.h"
#include "hoval_proto.h"
#include "hoval_modbus.h"
#include "hoval_can.h"

static const char *TAG = "hoval_mqtt";

#ifndef CONFIG_HOXPI_MQTT_URI
#define CONFIG_HOXPI_MQTT_URI ""
#endif
#ifndef CONFIG_HOXPI_MQTT_USER
#define CONFIG_HOXPI_MQTT_USER ""
#endif
#ifndef CONFIG_HOXPI_MQTT_PASS
#define CONFIG_HOXPI_MQTT_PASS ""
#endif
#ifndef CONFIG_HOXPI_MQTT_INTERVAL_S
#define CONFIG_HOXPI_MQTT_INTERVAL_S 30
#endif
#ifndef CONFIG_HOXPI_MQTT_STALE_MIN
#define CONFIG_HOXPI_MQTT_STALE_MIN 10
#endif

#define HMQ_PAYLOAD_MAX 1024      /* laengste Discovery (select mit 7 Optionen + device) < 600 B */

static esp_mqtt_client_handle_t s_cli;
static volatile bool s_connected, s_need_discovery;
static uint32_t s_wl_sig;         /* Kennung der aktiven Whitelist (Discovery bei Aenderung erneuern) */
static uint32_t s_pub_ok, s_pub_fail, s_cmd_ok, s_cmd_rej;
static char s_buf[HMQ_PAYLOAD_MAX];   /* nur vom Task benutzt */

static bool read_cb(uint16_t reg, uint16_t *word, bool *seen)
{
    if (!hm_read(reg, word)) return false;
    *seen = hc_seen(reg);
    return true;
}

static void pub(const char *topic, const char *payload, bool retain)
{
    if (!s_cli || !s_connected) return;
    int id = esp_mqtt_client_publish(s_cli, topic, payload, 0, 0, retain ? 1 : 0);
    if (id < 0) s_pub_fail++; else s_pub_ok++;
}

static uint32_t whitelist_sig(void)
{
    uint16_t n = 0; const uint16_t *wl = hp_whitelist_active(&n);
    uint32_t h = 2166136261u;
    for (uint16_t i = 0; i < n; i++) { h ^= wl[i]; h *= 16777619u; }
    return h ^ n;
}

/* ---- Discovery: alle Entities (retain); Steuerungen ausserhalb der Whitelist werden geloescht ("" retain) ---- */
static void discovery(void)
{
    char topic[HA_TOPIC_MAX];
    unsigned n_sens = 0, n_ctrl = 0, n_del = 0;
    for (uint8_t i = 0; i < ha_sensors_n; i++) {
        if (!ha_discovery_json(s_buf, sizeof s_buf, &ha_sensors[i])) continue;   /* Register nicht in der Tabelle */
        pub(ha_topic_discovery(topic, sizeof topic, "sensor", ha_sensors[i].key), s_buf, true); n_sens++;
    }
    ha_discovery_cop_json(s_buf, sizeof s_buf);   pub(ha_topic_discovery(topic, sizeof topic, "sensor", "cop"), s_buf, true);
    ha_discovery_stale_json(s_buf, sizeof s_buf); pub(ha_topic_discovery(topic, sizeof topic, "binary_sensor", "stale"), s_buf, true);
    ha_discovery_kuehl_json(s_buf, sizeof s_buf); pub(ha_topic_discovery(topic, sizeof topic, "binary_sensor", "kuehl_wartet"), s_buf, true);
    for (uint8_t i = 0; i < ha_controls_n; i++) {
        const ha_ent_t *e = &ha_controls[i];
        ha_topic_discovery(topic, sizeof topic, ha_kind_str((ha_kind_t)e->kind), e->key);
        if (!ha_control_enabled(e) || !ha_discovery_json(s_buf, sizeof s_buf, e)) { pub(topic, "", true); n_del++; continue; }
        pub(topic, s_buf, true); n_ctrl++;
    }
    s_wl_sig = whitelist_sig();
    ESP_LOGI(TAG, "Discovery: %u Sensoren + COP/stale/kuehl_wartet, %u Steuerungen (%u nicht freigegeben -> entfernt)", n_sens, n_ctrl, n_del);
}

/* ---- Zustaende ---- */
static void publish_states(void)
{
    char topic[HA_TOPIC_MAX], st[HA_STATE_MAX];
    int32_t raw; bool have_raw;
    for (uint8_t i = 0; i < ha_sensors_n; i++) {
        if (!ha_state(&ha_sensors[i], read_cb, st, sizeof st, &raw, &have_raw)) continue;
        pub(ha_topic_state(topic, sizeof topic, ha_sensors[i].key, "state"), st, true);
        if (have_raw) { char r[16]; snprintf(r, sizeof r, "%ld", (long)raw); pub(ha_topic_state(topic, sizeof topic, ha_sensors[i].key, "raw"), r, true); }
    }
    if (ha_cop_state(read_cb, st, sizeof st)) pub(HA_BASE "/cop/state", st, true);
    for (uint8_t i = 0; i < ha_controls_n; i++) {
        if (!ha_control_enabled(&ha_controls[i])) continue;
        if (!ha_state(&ha_controls[i], read_cb, st, sizeof st, &raw, &have_raw)) continue;
        pub(ha_topic_state(topic, sizeof topic, ha_controls[i].key, "state"), st, true);
    }
    /* Backlog 15c: Kuehl-Wartezustand */
    int32_t vl; int ph = ha_kuehl_phase(read_cb, &vl);
    if (ph < 0) pub(HA_BASE "/kuehl_wartet/state", "unknown", true);
    else {
        pub(HA_BASE "/kuehl_wartet/state", (ph == 1 || ph == 2) ? "ON" : "OFF", true);
        ha_kuehl_attr_json(s_buf, sizeof s_buf, ph, vl); pub(HA_BASE "/kuehl_wartet/attr", s_buf, true);
    }
    /* Verfuegbarkeits-Alarm (Backlog #9): kein dekodierter Datenpunkt seit n Minuten */
    const hc_stats_t *cs = hc_stats();
    bool have_rx = cs->last_rx_ms != 0;
    uint32_t age_s = have_rx ? (uint32_t)((esp_timer_get_time() / 1000 - cs->last_rx_ms) / 1000) : 0;
    bool stale = !have_rx || age_s > (uint32_t)CONFIG_HOXPI_MQTT_STALE_MIN * 60u;
    pub(HA_BASE "/stale/state", stale ? "ON" : "OFF", true);
    ha_stale_attr_json(s_buf, sizeof s_buf, age_s, have_rx, CONFIG_HOXPI_MQTT_STALE_MIN); pub(HA_BASE "/stale/attr", s_buf, true);
    pub(HA_AVAIL, "online", true);
}

/* ---- Kommando hoval/<key>/set (aus dem esp-mqtt-Task, kurz halten) ---- */
static void on_command(const char *topic, size_t tlen, const char *data, size_t dlen)
{
    char key[40], payload[48];
    const char *pre = HA_BASE "/"; size_t plen = strlen(pre);
    if (tlen <= plen + 4 || strncmp(topic, pre, plen) != 0 || strncmp(topic + tlen - 4, "/set", 4) != 0) return;
    size_t klen = tlen - plen - 4;
    if (klen == 0 || klen >= sizeof key || memchr(topic + plen, '/', klen)) return;
    memcpy(key, topic + plen, klen); key[klen] = 0;
    if (dlen >= sizeof payload) { ESP_LOGW(TAG, "Kommando %s: Payload zu lang (%u)", key, (unsigned)dlen); s_cmd_rej++; return; }
    memcpy(payload, data, dlen); payload[dlen] = 0;

    const ha_ent_t *e = ha_find_control(key);
    if (!e)                      { ESP_LOGW(TAG, "Kommando %s: unbekannt", key); s_cmd_rej++; return; }
    if (!ha_control_enabled(e))  { ESP_LOGW(TAG, "Kommando %s: reg %u nicht in der Whitelist", key, e->reg); s_cmd_rej++; return; }
    uint16_t word;
    int rc = ha_command(e, payload, &word);
    if (rc != 0)                 { ESP_LOGW(TAG, "Kommando %s: Payload '%s' unbrauchbar (%d)", key, payload, rc); s_cmd_rej++; return; }
    if (hm_write(e->reg, word))  { ESP_LOGI(TAG, "Kommando %s -> reg %u = %u ('%s')", key, e->reg, word, payload); s_cmd_ok++; }
    else                         { s_cmd_rej++; }       /* Grund hat hoval_modbus geloggt */
}

static void mqtt_event(void *arg, esp_event_base_t base, int32_t id, void *data)
{
    (void)arg; (void)base;
    esp_mqtt_event_handle_t ev = (esp_mqtt_event_handle_t)data;
    switch ((esp_mqtt_event_id_t)id) {
    case MQTT_EVENT_CONNECTED:
        s_connected = true; s_need_discovery = true;
        ESP_LOGI(TAG, "verbunden mit %s", CONFIG_HOXPI_MQTT_URI);
        break;
    case MQTT_EVENT_DISCONNECTED:
        s_connected = false;
        ESP_LOGW(TAG, "Verbindung getrennt (Broker/Netz?) - esp-mqtt verbindet neu");
        break;
    case MQTT_EVENT_DATA:
        if (ev->topic && ev->topic_len > 0 && ev->data_len >= 0 && ev->current_data_offset == 0)
            on_command(ev->topic, (size_t)ev->topic_len, ev->data, (size_t)ev->data_len);
        break;
    case MQTT_EVENT_ERROR:
        ESP_LOGW(TAG, "MQTT-Fehler (Typ %d)", ev->error_handle ? (int)ev->error_handle->error_type : -1);
        break;
    default: break;
    }
}

static void mqtt_task(void *arg)
{
    (void)arg;
    uint32_t last_pub = 0;
    for (;;) {
        vTaskDelay(pdMS_TO_TICKS(1000));
        if (!s_connected) continue;
        uint32_t now = (uint32_t)(esp_timer_get_time() / 1000000);
        if (s_need_discovery) {
            s_need_discovery = false;
            discovery();
            esp_mqtt_client_subscribe(s_cli, HA_BASE "/+/set", 0);
            pub(HA_AVAIL, "online", true);
            last_pub = 0;                                   /* sofort Zustaende nachschieben */
        } else if (whitelist_sig() != s_wl_sig) {
            ESP_LOGI(TAG, "Whitelist geaendert -> Discovery erneuern");
            discovery();
        }
        if (now - last_pub >= (uint32_t)CONFIG_HOXPI_MQTT_INTERVAL_S) {
            last_pub = now;
            publish_states();
        }
    }
}

bool hmq_enabled(void) { return CONFIG_HOXPI_MQTT_URI[0] != 0; }

bool hmq_start(void)
{
    if (!hmq_enabled()) { ESP_LOGI(TAG, "MQTT aus (HOXPI_MQTT_URI leer)"); return false; }
    esp_mqtt_client_config_t cfg = {
        .broker.address.uri = CONFIG_HOXPI_MQTT_URI,
        .credentials.client_id = "hoxpi-esp32",
        .session.last_will.topic = HA_AVAIL,
        .session.last_will.msg = "offline",
        .session.last_will.msg_len = 7,
        .session.last_will.qos = 0,
        .session.last_will.retain = 1,
        .session.keepalive = 60,
        .network.reconnect_timeout_ms = 10000,
    };
    if (CONFIG_HOXPI_MQTT_USER[0]) { cfg.credentials.username = CONFIG_HOXPI_MQTT_USER; cfg.credentials.authentication.password = CONFIG_HOXPI_MQTT_PASS; }
    s_cli = esp_mqtt_client_init(&cfg);
    if (!s_cli) { ESP_LOGE(TAG, "esp_mqtt_client_init"); return false; }
    if (esp_mqtt_client_register_event(s_cli, ESP_EVENT_ANY_ID, mqtt_event, NULL) != ESP_OK) { ESP_LOGE(TAG, "register_event"); return false; }
    if (esp_mqtt_client_start(s_cli) != ESP_OK) { ESP_LOGE(TAG, "client_start"); return false; }
    xTaskCreate(mqtt_task, "hoxpi_mqtt", 4096, NULL, 3, NULL);
    ESP_LOGI(TAG, "MQTT -> %s, Intervall %d s, stale > %d min, %u Sensoren / %u Steuerungen (Whitelist entscheidet)",
             CONFIG_HOXPI_MQTT_URI, CONFIG_HOXPI_MQTT_INTERVAL_S, CONFIG_HOXPI_MQTT_STALE_MIN, ha_sensors_n, ha_controls_n);
    return true;
}

void hmq_stats(hmq_stats_t *s)
{
    s->connected = s_connected; s->pub_ok = s_pub_ok; s->pub_fail = s_pub_fail; s->cmd_ok = s_cmd_ok; s->cmd_rej = s_cmd_rej;
}
