/*
 * hoval_json.c — JSON-Ausgabe der Statusseite + Zerlegung des /config-Bodys (reines C, siehe hoval_json.h)
 */
#include "hoval_json.h"
#include "hoval_proto.h"
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include <stdarg.h>

/* ---- kleiner Anhaenger: schreibt in out[cap], zaehlt auch ueber cap hinaus (Abschneide-Erkennung) ---- */
typedef struct { char *out; size_t cap, len; } jw_t;

static void jw_raw(jw_t *w, const char *s)
{
    size_t n = strlen(s);
    if (w->len < w->cap) {
        size_t room = w->cap - w->len - 1;
        size_t k = n < room ? n : room;
        memcpy(w->out + w->len, s, k);
        w->out[w->len + k] = 0;
    }
    w->len += n;
}

static void jw_fmt(jw_t *w, const char *fmt, ...)
{
    char tmp[160];
    va_list ap; va_start(ap, fmt);
    vsnprintf(tmp, sizeof tmp, fmt, ap);
    va_end(ap);
    jw_raw(w, tmp);
}

/* Zeichenkette mit Escapes (nur ASCII-Steuerzeichen, " und \) */
static void jw_str(jw_t *w, const char *s)
{
    jw_raw(w, "\"");
    for (; s && *s; s++) {
        unsigned char c = (unsigned char)*s;
        if (c == '"' || c == '\\') { char e[3] = { '\\', (char)c, 0 }; jw_raw(w, e); }
        else if (c < 0x20)        { jw_fmt(w, "\\u%04x", c); }
        else                       { char e[2] = { (char)c, 0 }; jw_raw(w, e); }
    }
    jw_raw(w, "\"");
}

static void jw_bool(jw_t *w, bool b) { jw_raw(w, b ? "true" : "false"); }

static void jw_whitelist(jw_t *w, const uint16_t *regs, uint16_t n)
{
    jw_raw(w, "[");
    for (uint16_t i = 0; i < n; i++) jw_fmt(w, "%s%u", i ? "," : "", (unsigned)regs[i]);
    jw_raw(w, "]");
}

static void jw_config_body(jw_t *w, const hcfg_t *c, uint16_t wl_active_n, bool write_effective, bool restart_required)
{
    uint16_t n = 0;
    const uint16_t *wl = hp_whitelist_active(&n);
    jw_fmt(w, "\"poll_wez\":%u,\"poll_hv\":%u,\"poll_delay\":%u,\"wr_en\":", c->poll_wez_s, c->poll_hv_s, c->poll_delay_ms);
    jw_bool(w, c->enable_write);
    jw_raw(w, ",\"write_effective\":"); jw_bool(w, write_effective);
    jw_raw(w, ",\"restart_required\":"); jw_bool(w, restart_required);
    jw_fmt(w, ",\"whitelist_n\":%u,\"whitelist_src\":\"%s\",\"whitelist\":", (unsigned)(wl ? n : wl_active_n),
           c->wl_override ? "nvs" : "compiled");
    jw_whitelist(w, wl, wl ? n : 0);
    jw_raw(w, ",\"from_nvs\":{\"poll_wez\":"); jw_bool(w, c->from_nvs & HCFG_SRC_POLL_WEZ);
    jw_raw(w, ",\"poll_hv\":");   jw_bool(w, c->from_nvs & HCFG_SRC_POLL_HV);
    jw_raw(w, ",\"poll_delay\":"); jw_bool(w, c->from_nvs & HCFG_SRC_POLL_DELAY);
    jw_raw(w, ",\"wr_en\":");     jw_bool(w, c->from_nvs & HCFG_SRC_WR_EN);
    jw_raw(w, ",\"whitelist\":"); jw_bool(w, c->from_nvs & HCFG_SRC_WHITELIST);
    jw_raw(w, "}");
}

static void jw_register_body(jw_t *w, const hp_reg_t *r, hj_read_cb_t read)
{
    uint16_t word = 0; bool seen = false;
    bool have = read ? read(r->reg, &word, &seen) : false;
    jw_fmt(w, "\"reg\":%u,\"unit\":%u,\"fg\":%u,\"fn\":%u,\"dp\":%u,\"type\":\"%s\",\"dec\":%d,\"writable\":",
           r->reg, r->unit_id, r->fg, r->fn, r->dp, hp_type_str((hp_type_t)r->type), r->decimal);
    jw_bool(w, r->flags & HP_F_WRITABLE);
    jw_raw(w, ",\"whitelist\":"); jw_bool(w, hp_in_whitelist(r->reg));
    jw_raw(w, ",\"low_half\":");  jw_bool(w, r->flags & HP_F_LOW_HALF);
    if (!(r->flags & HP_F_NO_RANGE)) jw_fmt(w, ",\"min\":%ld,\"max\":%ld", (long)r->min, (long)r->max);
    jw_raw(w, ",\"seen\":"); jw_bool(w, have && seen);
    if (have && seen) jw_fmt(w, ",\"raw\":%u,\"val\":%ld", word, (long)hp_check_value((hp_type_t)r->type, word));
    else              jw_raw(w, ",\"raw\":null,\"val\":null");
}

size_t hj_status_json(char *out, size_t cap, const hj_status_in_t *in, hj_read_cb_t read)
{
    jw_t w = { out, cap, 0 };
    if (cap) out[0] = 0;
    jw_raw(&w, "{\"gateway\":\"hoxpi-esp32\",\"version\":");
    jw_str(&w, in->version ? in->version : "");
    jw_fmt(&w, ",\"uptime_s\":%lu,\"heap_free\":%lu,", (unsigned long)in->uptime_s, (unsigned long)in->heap_free);
    jw_fmt(&w, "\"can\":{\"rx_frames\":%lu,\"rx_msgs\":%lu,\"decoded\":%lu,\"tx_frames\":%lu,\"tx_errors\":%lu,\"bus_off\":%lu,",
           (unsigned long)in->rx_frames, (unsigned long)in->rx_msgs, (unsigned long)in->decoded,
           (unsigned long)in->tx_frames, (unsigned long)in->tx_errors, (unsigned long)in->bus_off);
    if (in->have_rx) jw_fmt(&w, "\"last_rx_age_s\":%lu,", (unsigned long)in->last_rx_age_s);
    else             jw_raw(&w, "\"last_rx_age_s\":null,");
    /* stale wie HoxPi-Statuslog: > 10 min ohne Datenpunkt (oder noch nie einer) */
    jw_raw(&w, "\"stale\":"); jw_bool(&w, !in->have_rx || in->last_rx_age_s > 600);
    jw_raw(&w, "},");
    jw_fmt(&w, "\"modbus\":{\"port\":%u,\"write_enabled\":", in->modbus_port); jw_bool(&w, in->write_enabled);
    jw_fmt(&w, "},\"table\":{\"registers\":%u,\"areas\":%u},", in->regs_count, in->areas_count);
    /* MQTT-Zaehler wie hmq_stats(): pub_ok/pub_fail = Veroeffentlichungen, cmd_ok/cmd_rej = hoval/<key>/set */
    jw_raw(&w, "\"mqtt\":{\"enabled\":"); jw_bool(&w, in->mqtt_enabled);
    if (in->mqtt_enabled) {
        jw_raw(&w, ",\"connected\":"); jw_bool(&w, in->mqtt_connected);
        jw_fmt(&w, ",\"pub_ok\":%lu,\"pub_fail\":%lu,\"cmd_ok\":%lu,\"cmd_rej\":%lu",
               (unsigned long)in->mqtt_pub_ok, (unsigned long)in->mqtt_pub_fail,
               (unsigned long)in->mqtt_cmd_ok, (unsigned long)in->mqtt_cmd_rej);
    }
    jw_raw(&w, "},");
    jw_raw(&w, "\"config\":{");
    jw_config_body(&w, in->cfg, in->wl_active_n, in->write_enabled, in->restart_required);
    jw_raw(&w, "}");
    if (read) {
        static const uint16_t core[HJ_CORE_N] = { HJ_CORE_REGS };
        jw_raw(&w, ",\"values\":{");
        bool first = true;
        for (size_t i = 0; i < HJ_CORE_N; i++) {
            const hp_reg_t *r = hp_find_reg(core[i]);
            if (!r) continue;                      /* Beispieltabelle hat nicht alle */
            jw_fmt(&w, "%s\"%u\":{", first ? "" : ",", core[i]); first = false;
            uint16_t word = 0; bool seen = false;
            bool have = read(core[i], &word, &seen);
            jw_fmt(&w, "\"type\":\"%s\",\"dec\":%d,\"seen\":", hp_type_str((hp_type_t)r->type), r->decimal);
            jw_bool(&w, have && seen);
            if (have && seen) jw_fmt(&w, ",\"raw\":%u,\"val\":%ld}", word, (long)hp_check_value((hp_type_t)r->type, word));
            else              jw_raw(&w, ",\"raw\":null,\"val\":null}");
        }
        jw_raw(&w, "}");
    }
    jw_raw(&w, "}");
    return w.len;
}

size_t hj_config_json(char *out, size_t cap, const hcfg_t *c, uint16_t wl_active_n, bool write_effective, bool restart_required)
{
    jw_t w = { out, cap, 0 };
    if (cap) out[0] = 0;
    jw_raw(&w, "{");
    jw_config_body(&w, c, wl_active_n, write_effective, restart_required);
    jw_raw(&w, "}");
    return w.len;
}

bool hj_register_json(char *out, size_t cap, uint16_t reg, hj_read_cb_t read)
{
    jw_t w = { out, cap, 0 };
    if (cap) out[0] = 0;
    const hp_reg_t *r = hp_find_reg(reg);
    if (!r) { jw_fmt(&w, "{\"error\":\"register %u nicht in der Tabelle\"}", reg); return false; }
    jw_raw(&w, "{"); jw_register_body(&w, r, read); jw_raw(&w, "}");
    return true;
}

/* ---- Body-Scanner ------------------------------------------------------------ */
/* Zeiger hinter  "key" <ws> : <ws>  oder NULL. Sucht nur Schluessel in Anfuehrungszeichen. */
static const char *find_key(const char *body, const char *key)
{
    size_t kl = strlen(key);
    for (const char *p = body; (p = strchr(p, '"')) != NULL; p++) {
        if (strncmp(p + 1, key, kl) == 0 && p[1 + kl] == '"') {
            const char *q = p + 2 + kl;
            while (isspace((unsigned char)*q)) q++;
            if (*q != ':') continue;
            q++;
            while (isspace((unsigned char)*q)) q++;
            return q;
        }
    }
    return NULL;
}

/* Zahl oder true/false (fuer wr_en). false bei allem anderen. */
static bool scan_number(const char *v, long *out)
{
    if (!strncmp(v, "true", 4))  { *out = 1; return true; }
    if (!strncmp(v, "false", 5)) { *out = 0; return true; }
    bool quoted = (*v == '"');
    if (quoted) v++;
    char *end; long x = strtol(v, &end, 10);
    if (end == v) return false;
    if (quoted && *end != '"') return false;
    if (!quoted && *end && *end != ',' && *end != '}' && !isspace((unsigned char)*end)) return false;
    *out = x; return true;
}

/* Whitelist als "1490,1497" oder [1490, 1497] -> Text in tmp (fuer hcfg_set_whitelist_text) */
static bool scan_whitelist(const char *v, char *tmp, size_t cap)
{
    size_t n = 0;
    if (*v == '"') {
        const char *e = strchr(v + 1, '"');
        if (!e) return false;
        size_t len = (size_t)(e - v - 1);
        if (len >= cap) return false;
        memcpy(tmp, v + 1, len); tmp[len] = 0;
        return true;
    }
    if (*v == '[') {
        const char *p = v + 1;
        for (;;) {
            while (isspace((unsigned char)*p) || *p == ',') p++;
            if (*p == ']') break;
            if (!isdigit((unsigned char)*p)) return false;
            const char *s = p;
            while (isdigit((unsigned char)*p)) p++;
            size_t len = (size_t)(p - s);
            if (n + len + 2 >= cap) return false;
            if (n) tmp[n++] = ',';
            memcpy(tmp + n, s, len); n += len; tmp[n] = 0;
        }
        tmp[n] = 0;
        return true;
    }
    if (!strncmp(v, "null", 4)) { tmp[0] = 0; return true; }
    return false;
}

int hj_parse_config(const char *body, hcfg_t *c, char *err, size_t errcap)
{
    static const struct { const char *key; uint8_t bit; } NUM[] = {
        { HCFG_KEY_POLL_WEZ, HCFG_SRC_POLL_WEZ }, { HCFG_KEY_POLL_HV, HCFG_SRC_POLL_HV },
        { HCFG_KEY_POLL_DELAY, HCFG_SRC_POLL_DELAY }, { HCFG_KEY_WR_EN, HCFG_SRC_WR_EN },
    };
    if (err && errcap) err[0] = 0;
    if (!body || !c) { if (err) snprintf(err, errcap, "leerer Body"); return -1; }
    hcfg_t tmp = *c;
    int changed = 0;
    for (size_t i = 0; i < sizeof NUM / sizeof NUM[0]; i++) {
        const char *v = find_key(body, NUM[i].key);
        if (!v) continue;
        long x;
        if (!scan_number(v, &x)) { if (err) snprintf(err, errcap, "%s: keine Zahl", NUM[i].key); return -1; }
        if (!hcfg_set(&tmp, NUM[i].key, x)) { if (err) snprintf(err, errcap, "%s=%ld ausserhalb der Grenzen", NUM[i].key, x); return -1; }
        changed |= NUM[i].bit;
    }
    const char *v = find_key(body, HCFG_KEY_WHITELIST);
    if (v) {
        char text[HCFG_WL_TEXT_MAX + 1];
        if (!scan_whitelist(v, text, sizeof text)) { if (err) snprintf(err, errcap, "whitelist: Zeichenkette oder Zahlenliste erwartet"); return -1; }
        int n = hcfg_set_whitelist_text(&tmp, text);
        if (n == -1) { if (err) snprintf(err, errcap, "whitelist: Syntaxfehler"); return -1; }
        if (n == -2) { if (err) snprintf(err, errcap, "whitelist: mehr als %d Eintraege", HCFG_WL_MAX); return -1; }
        changed |= HCFG_SRC_WHITELIST;
    }
    if (changed) *c = tmp;
    return changed;
}
