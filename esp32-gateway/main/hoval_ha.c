/*
 * hoval_ha.c — Home-Assistant-Entities, Discovery-Payloads, Zustands-Texte und Kommandos
 * (reines C, Portierung von mqtt/hoval_mqtt.py; siehe hoval_ha.h)
 */
#include "hoval_ha.h"
#include "hoval_proto.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <limits.h>
#include <stdarg.h>

/* ---------- Enum-Texte (1:1 hoval_mqtt.py) ---------- */
static const ha_enum_t HK_STATUS[] = {
    {0,"Abgeschaltet"},{1,"Heizen Normal"},{2,"Heizen Komfort"},{3,"Heizen Spar"},{4,"Frostschutz"},
    {7,"Ferien"},{8,"Party"},{9,"Kuehlen Normal"},{10,"Kuehlen Komfort"},{11,"Kuehlen Spar"},
    {12,"Stoerung"},{13,"Handbetrieb"},{14,"Schutz Kuehlen"},{22,"Kuehlen extern"},{23,"Heizen extern"},
    {26,"SmartGrid Vorzug"} };
static const ha_enum_t DHW_STATUS[] = {
    {0,"Aus"},{1,"Laden Normal"},{2,"Laden Komfort"},{5,"Stoerung"},{6,"Zapfung"},{8,"Laden reduziert"},
    {12,"SmartGrid Vorzug"},{13,"SmartGrid Zwang"} };
static const ha_enum_t SG_STATUS[]  = { {0,"Normal"},{1,"Vorzugbetrieb"},{2,"Gesperrt"},{3,"Abnahmezwang"},{255,"inaktiv"} };
static const ha_enum_t WEZ_STATUS[] = {
    {0,"Aus"},{1,"Heizen"},{2,"Kuehlen"},{4,"Warmwasser"},{16,"Wiedereinschaltsperre"},
    {17,"Verriegelung (Stoerung)"},{51,"Startvorbereitung"},{98,"Startphase (W:61)"} };
static const ha_enum_t UKA[]   = { {0,"zu"},{1,"offen"} };
static const ha_enum_t ANF[]   = { {0,"nein"},{100,"ja"} };
/* Schreibbare LIST-Register */
static const ha_enum_t BW_HK[]  = { {0,"Standby"},{1,"Woche 1"},{2,"Woche 2"},{4,"Konstant"},{5,"Sparbetrieb"},{7,"Hand Heizen"},{8,"Hand Kuehlen"} };
static const ha_enum_t BW_WW[]  = { {0,"Standby"},{1,"Woche 1"},{2,"Woche 2"},{4,"Konstant"},{6,"Sparbetrieb"} };
static const ha_enum_t BW_WEZ[] = { {0,"Aus"},{1,"Automatik"},{4,"Manuell Heizen"},{5,"Manuell Kuehlen"} };
static const ha_enum_t SG_BUS[] = { {0,"Normal"},{1,"Vorzugbetrieb"},{2,"Gesperrt"},{3,"Abnahmezwang"} };
static const ha_enum_t SG_TRG[] = { {0,"Aus"},{1,"Eingangskontakte"},{2,"Systembus"},{3,"Leistung gedaempft"} };
#define EN(t) t, (uint8_t)(sizeof t / sizeof t[0])

/* Fehlercode 1534: 255 = OK, 0 = kein Wert, sonst code+1 = Klasse*64+Nr (Klasse 1=W 2=B 3=E) */
static const struct { const char *code, *txt; } FEHLER_TXT[] = {
    {"B:02","Niederdruck"},{"E:02","Niederdruck, verriegelt"},{"W:58","E-Stab nach Verriegelung"},
    {"W:61","Startphase-Sonderzustand"},{"B:63","Service-/Parametereingriff"},{"E:31","Verriegelung nach Eingriff"} };

/* Kaeltekreis fg=60/fn=7: 16-bit signed, Skala je Register (KK_SENS) */
static const struct { uint16_t reg; uint8_t dec; } KK_SENS[] = {
    {31903,1},{31905,1},{31907,1},{31913,2},{31915,2},{31917,2},{31921,1} };
#define KK_N (sizeof KK_SENS / sizeof KK_SENS[0])

/* ---------- Sensoren (read-only) ---------- */
const ha_ent_t ha_sensors[] = {
    {"aussentemp",        1477, "Aussentemperatur",          "°C", "temperature", NULL,0, HA_SENSOR},
    {"vorlauf",          18760, "Vorlauf",                   "°C", "temperature", NULL,0, HA_SENSOR},
    {"ruecklauf",         1535, "Ruecklauf",                 "°C", "temperature", NULL,0, HA_SENSOR},
    {"ww_ist",            1500, "Warmwasser Ist",            "°C", "temperature", NULL,0, HA_SENSOR},
    {"raum_ist",          1510, "Raum Ist HK1",              "°C", "temperature", NULL,0, HA_SENSOR},
    {"el_leistung",      25611, "El. Leistung",              "kW", "power",       NULL,0, HA_SENSOR},
    {"heizleistung",     25612, "Heizleistung",              "kW", "power",       NULL,0, HA_SENSOR},
    {"modulation",       18726, "Modulation",                "%",  NULL,          NULL,0, HA_SENSOR},
    {"status_hk1",        1501, "Status HK1",                NULL, NULL, EN(HK_STATUS),  HA_SENSOR},
    {"status_hk2",        1502, "Status HK2",                NULL, NULL, EN(HK_STATUS),  HA_SENSOR},
    {"status_ww",         1504, "Status WW-Regelung",        NULL, NULL, EN(DHW_STATUS), HA_SENSOR},
    {"sg_status",        27537, "SmartGrid Status",          NULL, NULL, EN(SG_STATUS),  HA_SENSOR},
    {"kuehlventil",      19870, "Kuehlventil UKA",           NULL, NULL, EN(UKA),        HA_SENSOR},
    {"jaz",              27467, "Jahresarbeitszahl",         NULL, NULL,          NULL,0, HA_SENSOR},
    {"leistungssollwert",18767, "Leistungs-Sollwert WEZ",    "%",  NULL,          NULL,0, HA_SENSOR},
    {"anforderung",      18768, "Anforderung WEZ",           NULL, NULL, EN(ANF),        HA_SENSOR},
    {"status_wez",        1539, "Status WEZ",                NULL, NULL, EN(WEZ_STATUS), HA_SENSOR},
    {"fehlercode",        1534, "Fehlercode WEZ",            NULL, NULL,          NULL,0, HA_SENSOR}, /* FEHLER_ENUM, s. ha_fehler_text */
    {"kk_lufteintritt",  31903, "Kaeltekreis Lufteintritt",  "°C", "temperature", NULL,0, HA_SENSOR},
    {"kk_sauggas",       31905, "Kaeltekreis Sauggas",       "°C", "temperature", NULL,0, HA_SENSOR},
    {"kk_heissgas",      31907, "Kaeltekreis Heissgas",      "°C", "temperature", NULL,0, HA_SENSOR},
    {"kk_ueberhitzung",  31913, "Kaeltekreis Ueberhitzung",  "K",  NULL,          NULL,0, HA_SENSOR},
    {"kk_niederdruck",   31915, "Kaeltekreis Niederdruck",   "bar","pressure",    NULL,0, HA_SENSOR},
    {"kk_hochdruck",     31917, "Kaeltekreis Hochdruck",     "bar","pressure",    NULL,0, HA_SENSOR},
    {"kk_drehzahl",      31921, "Verdichter Istdrehzahl",    "%",  NULL,          NULL,0, HA_SENSOR},
};
const uint8_t ha_sensors_n = (uint8_t)(sizeof ha_sensors / sizeof ha_sensors[0]);

/* ---------- Steuerbare Entities (unit = registers.json, wie num_meta() in hoval_mqtt.py) ---------- */
const ha_ent_t ha_controls[] = {
    {"set_ww_normal",      1497, "WW Normal-Soll",               "°C", NULL, NULL,0,      HA_NUMBER},
    {"set_ww_eco",         1498, "WW Eco-Soll",                  "°C", NULL, NULL,0,      HA_NUMBER},
    {"set_raum_normal",    1481, "Raumtemp Normal HK1",          "°C", NULL, NULL,0,      HA_NUMBER},
    {"set_raum_eco",       1482, "Raumtemp Eco HK1",             "°C", NULL, NULL,0,      HA_NUMBER},
    {"set_bw_hk1",         1478, "Betriebswahl HK1",             NULL, NULL, EN(BW_HK),   HA_SELECT},
    {"set_bw_hk2",         1479, "Betriebswahl HK2",             NULL, NULL, EN(BW_HK),   HA_SELECT},
    {"set_bw_ww",          1496, "Betriebswahl Warmwasser",      NULL, NULL, EN(BW_WW),   HA_SELECT},
    {"set_bw_wez",         1561, "Betriebswahl Waermeerzeuger",  NULL, NULL, EN(BW_WEZ),  HA_SELECT},
    {"set_raumist_hk1",    1510, "Raum-Ist Einspeisung HK1",     "°C", NULL, NULL,0,      HA_NUMBER},
    {"set_konst_kk_hk1",  19482, "Konst-Anford. Kuehlen HK1",    "°C", NULL, NULL,0,      HA_NUMBER},
    {"set_sg_off_ww",     27509, "SG-Offset Warmwasser",         "K" , NULL, NULL,0,      HA_NUMBER},
    {"set_sg_off_hk1",    27528, "SG-Offset Raum HK1 (Heizen)",  "K" , NULL, NULL,0,      HA_NUMBER},
    {"set_sg_off_kk1",    27531, "SG-Offset Raum HK1 (Kuehlen)", "K" , NULL, NULL,0,      HA_NUMBER},
    {"set_sg_off_puffer", 28839, "SG-Offset Heizpuffer",         "K" , NULL, NULL,0,      HA_NUMBER},
    {"set_sg_bus",        27545, "SmartGrid Zustand (Bus)",      NULL, NULL, EN(SG_BUS),  HA_SELECT},
    {"set_sg_trigger",    27546, "SmartGrid Ausloeser",          NULL, NULL, EN(SG_TRG),  HA_SELECT},
};
const uint8_t ha_controls_n = (uint8_t)(sizeof ha_controls / sizeof ha_controls[0]);

/* ---------- kleiner Anhaenger (wie hoval_json.c) ---------- */
typedef struct { char *out; size_t cap, len; } w_t;
static void w_raw(w_t *w, const char *s)
{
    size_t n = strlen(s);
    if (w->cap && w->len < w->cap) {
        size_t room = w->cap - w->len - 1, k = n < room ? n : room;
        memcpy(w->out + w->len, s, k); w->out[w->len + k] = 0;
    }
    w->len += n;
}
static void w_fmt(w_t *w, const char *fmt, ...) __attribute__((format(printf, 2, 3)));
static void w_fmt(w_t *w, const char *fmt, ...)
{
    char tmp[200]; va_list ap; va_start(ap, fmt); vsnprintf(tmp, sizeof tmp, fmt, ap); va_end(ap); w_raw(w, tmp);
}
static void w_str(w_t *w, const char *s)
{
    w_raw(w, "\"");
    for (; s && *s; s++) {
        unsigned char c = (unsigned char)*s;
        if (c == '"' || c == '\\') { char e[3] = { '\\', (char)c, 0 }; w_raw(w, e); }
        else if (c < 0x20)        { w_fmt(w, "\\u%04x", c); }
        else                       { char e[2] = { (char)c, 0 }; w_raw(w, e); }
    }
    w_raw(w, "\"");
}
static void w_kv(w_t *w, const char *k, const char *v) { w_raw(w, ",\""); w_raw(w, k); w_raw(w, "\":"); w_str(w, v); }
static void w_device(w_t *w)
{
    w_raw(w, ",\"device\":{\"identifiers\":[\"" HA_DEVICE_ID "\"],\"name\":\"HoxPi Waermepumpe\","
             "\"model\":\"CAN-Modbus-Bridge fuer Hoval(R) TTE\",\"manufacturer\":\"HoxPi\"}");
}

/* ---------- Topics ---------- */
const char *ha_topic_discovery(char *out, size_t cap, const char *art, const char *key)
{ snprintf(out, cap, "homeassistant/%s/" HA_DEVICE_ID "/%s/config", art, key); return out; }
const char *ha_topic_state(char *out, size_t cap, const char *key, const char *suffix)
{ snprintf(out, cap, HA_BASE "/%s/%s", key, suffix); return out; }
const char *ha_kind_str(ha_kind_t k) { return k == HA_NUMBER ? "number" : k == HA_SELECT ? "select" : "sensor"; }

/* ---------- Zahlen ---------- */
size_t ha_fmt_scaled(char *out, size_t cap, int32_t raw, int dec)
{
    if (dec <= 0) return (size_t)snprintf(out, cap, "%ld", (long)raw);
    long div = 1; for (int i = 0; i < dec; i++) div *= 10;
    long a = raw < 0 ? -(long)raw : (long)raw;
    return (size_t)snprintf(out, cap, "%s%ld.%0*ld", raw < 0 ? "-" : "", a / div, dec, a % div);
}
static int32_t signed_view(const hp_reg_t *r, uint16_t word)
{
    if ((r->type == HP_T_S16 || r->type == HP_T_S8) && word > 32767) return (int32_t)word - 65536;
    return word;
}
static const char *enum_txt(const ha_enum_t *en, uint8_t n, int32_t v)
{
    for (uint8_t i = 0; i < n; i++) if (en[i].val == v) return en[i].txt;
    return NULL;
}
static bool is_sentinel(uint16_t w) { return w == 0x8000 || w == 0xFFFF; }
static bool rd(ha_read_cb_t read, uint16_t reg, uint16_t *w)
{
    bool seen = false;
    return read(reg, w, &seen) && seen;
}

/* ---------- Discovery ---------- */
bool ha_discovery_json(char *out, size_t cap, const ha_ent_t *e)
{
    const hp_reg_t *r = hp_find_reg(e->reg);
    if (cap) out[0] = 0;
    if (!r) return false;
    w_t w = { out, cap, 0 };
    char t[HA_TOPIC_MAX];
    w_raw(&w, "{\"name\":"); w_str(&w, e->name);
    w_fmt(&w, ",\"unique_id\":\"" HA_DEVICE_ID "_%s\"", e->key);
    w_kv(&w, "state_topic", ha_topic_state(t, sizeof t, e->key, "state"));
    if (e->kind != HA_SENSOR) w_kv(&w, "command_topic", ha_topic_state(t, sizeof t, e->key, "set"));
    w_kv(&w, "availability_topic", HA_AVAIL);
    if (e->kind == HA_SENSOR) {
        if (e->unit) w_kv(&w, "unit_of_measurement", e->unit);
        if (e->dev_class) { w_kv(&w, "device_class", e->dev_class); w_kv(&w, "state_class", "measurement"); }
    } else if (e->kind == HA_NUMBER) {
        /* num_meta(): min/max aus der Tabelle (Rohwert / 10^dec), sonst 0..90; step 0,5 bei Dezimalen */
        int dec = r->decimal > 0 ? r->decimal : 0;
        char lo[24], hi[24];
        long div = 1; for (int i = 0; i < dec; i++) div *= 10;
        bool have_min = !(r->flags & HP_F_NO_RANGE), have_max = have_min && r->max != 0;
        int32_t lo_raw = have_min ? r->min : 0;
        int32_t hi_raw = have_max ? r->max : (int32_t)(90 * div);
        if (hi_raw <= lo_raw) hi_raw = lo_raw + (int32_t)(90 * div);
        ha_fmt_scaled(lo, sizeof lo, lo_raw, dec);
        ha_fmt_scaled(hi, sizeof hi, hi_raw, dec);
        w_fmt(&w, ",\"min\":%s,\"max\":%s,\"step\":%s,\"mode\":\"box\"", lo, hi, dec ? "0.5" : "1");
        if (e->unit) w_kv(&w, "unit_of_measurement", e->unit);
    } else {
        w_raw(&w, ",\"options\":[");
        for (uint8_t i = 0; i < e->en_n; i++) { if (i) w_raw(&w, ","); w_str(&w, e->en[i].txt); }
        w_raw(&w, "]");
    }
    w_device(&w);
    w_raw(&w, "}");
    return w.len < cap;
}

size_t ha_discovery_stale_json(char *out, size_t cap)
{
    w_t w = { out, cap, 0 }; if (cap) out[0] = 0;
    w_raw(&w, "{\"name\":\"HoxPi Daten veraltet\",\"unique_id\":\"" HA_DEVICE_ID "_stale\",\"device_class\":\"problem\","
              "\"state_topic\":\"" HA_BASE "/stale/state\",\"json_attributes_topic\":\"" HA_BASE "/stale/attr\"");
    w_device(&w); w_raw(&w, "}");   /* bewusst OHNE availability_topic */
    return w.len;
}
size_t ha_discovery_kuehl_json(char *out, size_t cap)
{
    w_t w = { out, cap, 0 }; if (cap) out[0] = 0;
    w_raw(&w, "{\"name\":\"Kuehlen wartet auf Kreis-Temperatur\",\"unique_id\":\"" HA_DEVICE_ID "_kuehl_wartet\","
              "\"state_topic\":\"" HA_BASE "/kuehl_wartet/state\",\"json_attributes_topic\":\"" HA_BASE "/kuehl_wartet/attr\","
              "\"availability_topic\":\"" HA_AVAIL "\"");
    w_device(&w); w_raw(&w, "}");
    return w.len;
}
size_t ha_discovery_cop_json(char *out, size_t cap)
{
    w_t w = { out, cap, 0 }; if (cap) out[0] = 0;
    w_raw(&w, "{\"name\":\"COP aktuell\",\"unique_id\":\"" HA_DEVICE_ID "_cop\",\"state_topic\":\"" HA_BASE "/cop/state\","
              "\"availability_topic\":\"" HA_AVAIL "\"");
    w_device(&w); w_raw(&w, "}");
    return w.len;
}

/* ---------- Fehlercode ---------- */
const char *ha_fehler_text(uint16_t raw, char *out, size_t cap)
{
    if (raw == 255) { snprintf(out, cap, "OK"); return out; }
    if (raw == 0)   { snprintf(out, cap, "kein Wert"); return out; }
    unsigned c = raw + 1u;
    char code[8]; snprintf(code, sizeof code, "%c:%02u", "IWBE"[(c >> 6) & 3], c & 63);
    for (size_t i = 0; i < sizeof FEHLER_TXT / sizeof FEHLER_TXT[0]; i++)
        if (!strcmp(code, FEHLER_TXT[i].code)) { snprintf(out, cap, "%s %s", code, FEHLER_TXT[i].txt); return out; }
    snprintf(out, cap, "%s", code);
    return out;
}

/* ---------- Zustaende ---------- */
static bool kk_group_silent(ha_read_cb_t read)
{
    /* alle Kaeltekreis-Register 0/Sentinel (oder nicht lesbar) -> Regler beantwortet fn=7 gerade nicht */
    for (size_t i = 0; i < KK_N; i++) {
        uint16_t w;
        if (rd(read, KK_SENS[i].reg, &w) && w != 0 && !is_sentinel(w)) return false;
    }
    return true;
}
static int kk_dec(uint16_t reg)
{
    for (size_t i = 0; i < KK_N; i++) if (KK_SENS[i].reg == reg) return KK_SENS[i].dec;
    return -1;
}

bool ha_state(const ha_ent_t *e, ha_read_cb_t read, char *out, size_t cap, int32_t *raw_out, bool *have_raw)
{
    const hp_reg_t *r = hp_find_reg(e->reg);
    uint16_t w;
    *have_raw = false;
    if (!r || !rd(read, e->reg, &w)) return false;

    int kd = kk_dec(e->reg);
    if (kd >= 0) {                                   /* Kaeltekreis: 16-bit signed, eigene Skala */
        if (is_sentinel(w) || kk_group_silent(read)) { snprintf(out, cap, "unknown"); return true; }
        int32_t v = w > 32767 ? (int32_t)w - 65536 : w;
        ha_fmt_scaled(out, cap, v, kd);
        return true;
    }
    if (e->reg == 1535 && w == 0) {                   /* FA-Ruecklauf stumm -> WP-Ruecklauf 60-7-258 (S32 31894/31895) */
        uint16_t hi, lo;
        if (!rd(read, 31894, &hi) || !rd(read, 31895, &lo)) return false;
        uint32_t u = ((uint32_t)hi << 16) | lo;
        if (u == 0xFFFFFFFFu || u == 0x80000000u) return false;
        int32_t v = (int32_t)u;
        if (v < -500 || v > 1500) return false;
        w = (uint16_t)(v & 0xFFFF);
    }
    if (e->reg == 1534) { ha_fehler_text(w, out, cap); *raw_out = w; *have_raw = true; return true; }

    int32_t v = signed_view(r, w);
    if (e->en) {
        const char *t = enum_txt(e->en, e->en_n, v);
        if (e->kind == HA_SELECT) { snprintf(out, cap, "%s", t ? t : ""); return true; }   /* enum.get(..., "") */
        if (t) snprintf(out, cap, "%s", t); else snprintf(out, cap, "%ld", (long)v);        /* enum.get(..., str(v)) */
        *raw_out = v; *have_raw = true;
        return true;
    }
    if (e->reg == 18767 && v == HA_INVALID_SETPOINT_RAW) { snprintf(out, cap, "unknown"); return true; }
    ha_fmt_scaled(out, cap, v, r->decimal);
    return true;
}

bool ha_cop_state(ha_read_cb_t read, char *out, size_t cap)
{
    uint16_t hi = 0, lo = 0, fa, pel;
    int32_t cop_x10 = -1;
    bool ok = rd(read, 31667, &hi) && rd(read, 31668, &lo) && !is_sentinel(hi) && !is_sentinel(lo)
              && (((uint32_t)hi << 16) | lo) != 0;
    if (ok) cop_x10 = (int32_t)(((uint32_t)hi << 16) | lo);
    else if (rd(read, 27490, &fa) && !is_sentinel(fa) && fa <= 200) cop_x10 = fa;   /* F1: FA-COP dp 45 (U8, 0,1) */
    if (cop_x10 < 0) return false;
    if (!rd(read, 25611, &pel) || is_sentinel(pel) || pel < 50) cop_x10 = 0;      /* Startfilter: Pel < 0,5 kW */
    if (cop_x10 > 200) return false;                                              /* Plausibilitaet 0..20 */
    ha_fmt_scaled(out, cap, cop_x10, 1);
    return true;
}

int ha_kuehl_phase(ha_read_cb_t read, int32_t *vl_x10)
{
    uint16_t hk, uka, wez, vl, pel;
    *vl_x10 = INT32_MIN;
    if (!rd(read, 1501, &hk) || !rd(read, 19870, &uka) || !rd(read, 1539, &wez)) return -1;
    if (rd(read, 1525, &vl) && !is_sentinel(vl)) *vl_x10 = vl > 32767 ? (int32_t)vl - 65536 : vl;
    if (hk != 22) return 0;
    if (wez != 0 || (rd(read, 25611, &pel) && !is_sentinel(pel) && pel >= 50)) return 3;
    if (uka != 1) return 0;
    if (*vl_x10 == INT32_MIN) return -1;
    return *vl_x10 >= HA_KUEHL_START_MIN_VL_X10 ? 2 : 1;
}
const char *ha_kuehl_phase_txt(int phase)
{
    switch (phase) {
    case 0: return "keine Anforderung";
    case 1: return "wartet auf Kreis-Temperatur";
    case 2: return "Startmarke erreicht, Freigabe folgt";
    case 3: return "Kuehlen aktiv";
    default: return "unbekannt";
    }
}
size_t ha_kuehl_attr_json(char *out, size_t cap, int phase, int32_t vl_x10)
{
    w_t w = { out, cap, 0 }; if (cap) out[0] = 0;
    char v[24], m[24];
    ha_fmt_scaled(m, sizeof m, HA_KUEHL_START_MIN_VL_X10, 1);
    w_fmt(&w, "{\"phase\":%d,\"phase_txt\":", phase); w_str(&w, ha_kuehl_phase_txt(phase));
    if (vl_x10 == INT32_MIN) w_raw(&w, ",\"vorlauf_c\":null");
    else { ha_fmt_scaled(v, sizeof v, vl_x10, 1); w_fmt(&w, ",\"vorlauf_c\":%s", v); }
    w_fmt(&w, ",\"startmarke_c\":%s}", m);
    return w.len;
}
size_t ha_stale_attr_json(char *out, size_t cap, uint32_t age_s, bool have_rx, unsigned stale_min)
{
    w_t w = { out, cap, 0 }; if (cap) out[0] = 0;
    bool on = !have_rx || age_s > stale_min * 60u;
    w_fmt(&w, "{\"age_s\":%lu,\"can_age_s\":%lu,\"reason\":\"%s\",\"stale_min\":%u}",
          (unsigned long)age_s, (unsigned long)age_s, on ? (have_rx ? "can" : "can-nie") : "ok", stale_min);
    return w.len;
}

/* ---------- Kommandos ---------- */
const ha_ent_t *ha_find_control(const char *key)
{
    for (uint8_t i = 0; i < ha_controls_n; i++) if (!strcmp(ha_controls[i].key, key)) return &ha_controls[i];
    return NULL;
}
bool ha_control_enabled(const ha_ent_t *e) { return hp_in_whitelist(e->reg); }

/* Dezimalzahl -> Rohwert x 10^dec, kaufmaennisch gerundet; ohne float (kein printf-Float noetig) */
static bool parse_scaled(const char *s, int dec, int32_t *out)
{
    while (isspace((unsigned char)*s)) s++;
    bool neg = false;
    if (*s == '+' || *s == '-') { neg = *s == '-'; s++; }
    if (!isdigit((unsigned char)*s) && *s != '.') return false;
    long ip = 0; int nd = 0;
    while (isdigit((unsigned char)*s)) { if (ip > 100000000L) return false; ip = ip * 10 + (*s - '0'); s++; nd++; }
    long fp = 0; int fd = 0;
    if (*s == '.') {
        s++;
        while (isdigit((unsigned char)*s)) {
            if (fd < dec)       { fp = fp * 10 + (*s - '0'); fd++; }
            else if (fd == dec) { if (*s >= '5') fp++; fd++; }   /* erste ueberzaehlige Stelle rundet */
            else fd++;
            s++; nd++;
        }
    }
    if (!nd) return false;
    while (fd < dec) { fp *= 10; fd++; }
    while (isspace((unsigned char)*s)) s++;
    if (*s) return false;
    long div = 1; for (int i = 0; i < dec; i++) div *= 10;
    long v = ip * div + fp;
    *out = (int32_t)(neg ? -v : v);
    return true;
}

int ha_command(const ha_ent_t *e, const char *payload, uint16_t *word)
{
    const hp_reg_t *r = hp_find_reg(e->reg);
    if (!r) return -2;
    if (e->kind == HA_SELECT) {
        /* Klartext, umgekehrt nachschlagen (Leerzeichen am Rand tolerieren) */
        char buf[48]; size_t n = strlen(payload);
        while (n && isspace((unsigned char)payload[n - 1])) n--;
        while (n && isspace((unsigned char)*payload)) { payload++; n--; }
        if (n >= sizeof buf) return -1;
        memcpy(buf, payload, n); buf[n] = 0;
        for (uint8_t i = 0; i < e->en_n; i++)
            if (!strcmp(e->en[i].txt, buf)) { *word = (uint16_t)(e->en[i].val & 0xFFFF); return 0; }
        return -1;
    }
    int32_t raw;
    if (!parse_scaled(payload, r->decimal > 0 ? r->decimal : 0, &raw)) return -1;
    *word = (uint16_t)(raw & 0xFFFF);        /* unscale(): int(round(v * 10**d)) & 0xFFFF */
    return 0;
}
