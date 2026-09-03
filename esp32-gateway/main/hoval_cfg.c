/*
 * hoval_cfg.c — Laufzeit-Konfiguration: Defaults, Grenzen, Whitelist-Text <-> Liste, Validierung.
 * Reines C (host-testbar, test/test_cfg.c). Die NVS-Seite steht in hoval_cfg_nvs.c.
 */
#include "hoval_cfg.h"
#include "hoval_proto.h"
#include <string.h>
#include <stdio.h>

static hcfg_t s_cfg;

const hcfg_t *hcfg_get(void) { return &s_cfg; }
hcfg_t       *hcfg_mut(void) { return &s_cfg; }

static uint16_t clampu(unsigned v, unsigned lo, unsigned hi)
{
    if (v < lo) return (uint16_t)lo;
    if (v > hi) return (uint16_t)hi;
    return (uint16_t)v;
}

void hcfg_defaults(hcfg_t *c, unsigned poll_wez_s, unsigned poll_hv_s, unsigned poll_delay_ms, bool enable_write)
{
    memset(c, 0, sizeof *c);
    c->poll_wez_s    = clampu(poll_wez_s,    HCFG_POLL_WEZ_MIN,   HCFG_POLL_WEZ_MAX);
    c->poll_hv_s     = clampu(poll_hv_s,     HCFG_POLL_HV_MIN,    HCFG_POLL_HV_MAX);
    c->poll_delay_ms = clampu(poll_delay_ms, HCFG_POLL_DELAY_MIN, HCFG_POLL_DELAY_MAX);
    c->enable_write  = enable_write;
}

bool hcfg_set(hcfg_t *c, const char *key, long v)
{
    if (!c || !key) return false;
    if (!strcmp(key, HCFG_KEY_POLL_WEZ)) {
        if (v < HCFG_POLL_WEZ_MIN || v > HCFG_POLL_WEZ_MAX) return false;
        c->poll_wez_s = (uint16_t)v; c->from_nvs |= HCFG_SRC_POLL_WEZ; return true;
    }
    if (!strcmp(key, HCFG_KEY_POLL_HV)) {
        if (v < HCFG_POLL_HV_MIN || v > HCFG_POLL_HV_MAX) return false;
        c->poll_hv_s = (uint16_t)v; c->from_nvs |= HCFG_SRC_POLL_HV; return true;
    }
    if (!strcmp(key, HCFG_KEY_POLL_DELAY)) {
        if (v < HCFG_POLL_DELAY_MIN || v > HCFG_POLL_DELAY_MAX) return false;
        c->poll_delay_ms = (uint16_t)v; c->from_nvs |= HCFG_SRC_POLL_DELAY; return true;
    }
    if (!strcmp(key, HCFG_KEY_WR_EN)) {
        if (v != 0 && v != 1) return false;
        c->enable_write = (v == 1); c->from_nvs |= HCFG_SRC_WR_EN; return true;
    }
    return false;
}

/* Trenner: Komma, Semikolon, Leerzeichen, Tab, Zeilenumbruch */
static bool is_sep(char ch) { return ch == ',' || ch == ';' || ch == ' ' || ch == '\t' || ch == '\r' || ch == '\n'; }

int hcfg_parse_whitelist(const char *text, uint16_t *out, size_t max)
{
    size_t n = 0;
    if (!text) return 0;
    if (strlen(text) > HCFG_WL_TEXT_MAX) return -1;
    const char *p = text;
    for (;;) {
        while (*p && is_sep(*p)) p++;
        if (!*p) break;
        if (*p < '0' || *p > '9') return -1;
        unsigned long v = 0;
        while (*p >= '0' && *p <= '9') {
            v = v * 10 + (unsigned long)(*p - '0');
            if (v > 65535ul) return -1;
            p++;
        }
        if (*p && !is_sep(*p)) return -1;              /* z. B. "1490x" */
        bool dup = false;
        for (size_t i = 0; i < n; i++) if (out[i] == (uint16_t)v) { dup = true; break; }
        if (dup) continue;
        if (n >= max) return -2;
        out[n++] = (uint16_t)v;
    }
    return (int)n;
}

size_t hcfg_format_whitelist(const uint16_t *regs, size_t n, char *out, size_t cap)
{
    size_t len = 0;
    if (!out || cap == 0) return 0;
    out[0] = '\0';
    for (size_t i = 0; i < n; i++) {
        char tmp[8];
        int k = snprintf(tmp, sizeof tmp, "%s%u", i ? "," : "", (unsigned)regs[i]);
        if (k < 0) break;
        if (len + (size_t)k + 1 > cap) break;          /* abgeschnitten, aber immer NUL-terminiert */
        memcpy(out + len, tmp, (size_t)k + 1);
        len += (size_t)k;
    }
    return len;
}

int hcfg_set_whitelist_text(hcfg_t *c, const char *text)
{
    uint16_t tmp[HCFG_WL_MAX];
    int n = hcfg_parse_whitelist(text, tmp, HCFG_WL_MAX);
    if (n < 0) return n;
    memcpy(c->wl, tmp, (size_t)n * sizeof tmp[0]);
    c->wl_n = (uint16_t)n;
    c->wl_override = true;
    c->from_nvs |= HCFG_SRC_WHITELIST;
    return n;
}

size_t hcfg_whitelist_validate(uint16_t *regs, uint16_t *n, hcfg_warn_cb_t warn)
{
    size_t dropped = 0, w = 0;
    for (size_t i = 0; i < *n; i++) {
        const hp_reg_t *r = hp_find_reg(regs[i]);
        if (!r) {
            if (warn) warn("Whitelist: Register nicht in der Tabelle - verworfen", regs[i]);
            dropped++;
            continue;
        }
        if (r->flags & HP_F_LOW_HALF) {
            if (warn) warn("Whitelist: Low-Wort eines 32-bit-Paares - verworfen", regs[i]);
            dropped++;
            continue;
        }
        if (!(r->flags & HP_F_WRITABLE) && warn)
            warn("Whitelist: laut Hoval-Liste nicht schreibbar (bleibt, wie bei HoxPi)", regs[i]);
        regs[w++] = regs[i];
    }
    *n = (uint16_t)w;
    return dropped;
}

size_t hcfg_apply(hcfg_t *c, hcfg_warn_cb_t warn)
{
    size_t dropped = 0;
    if (c->wl_override) {
        dropped = hcfg_whitelist_validate(c->wl, &c->wl_n, warn);
        hp_whitelist_override(c->wl, c->wl_n);
    } else {
        hp_whitelist_override(NULL, 0);
    }
    return dropped;
}
