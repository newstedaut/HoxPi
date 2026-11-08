#!/usr/bin/env python3
"""HoxPi Remote Console - page /display of the dashboard (port 80).

A wall-panel style view for TopTronic(R) E systems: outside / room / flow / hot-water temperatures,
ventilation, operating state of HK1, a browsable parameter catalogue and - only if explicitly enabled -
changing the HK1 room setpoints 03-051/03-053/03-054.

Data sources (no invented values, everything carries its age):
  1. panel/hoxpi_panel.py (optional, HOXPI_PANEL_DIR): page_values.json, status.json, writes via cmd.json
  2. the bridge's warm cache (HOXPI_BRIDGE_DIR/cache_last.json + bridge_state.json + registers.json)
     - works without the panel daemon, read only.
Catalogue: HOXPI_PANEL_DIR/bedienteil_katalog.csv if you built one for your installation, otherwise it is
generated from registers.json (the official datapoint list).

Not affiliated with Hoval AG. Own drawings and icons, free font stack (Inter if installed, else system UI).
"""
import csv, json, os, time

PANEL_BASE = os.environ.get("HOXPI_PANEL_DIR", "/home/admin/hoxpi_panel")
BRIDGE_BASE = os.environ.get("HOXPI_BRIDGE_DIR", "/home/admin/hoval-bridge")
STAT_F = os.path.join(PANEL_BASE, "status.json")
VAL_F = os.path.join(PANEL_BASE, "page_values.json")
SEED_F = os.path.join(PANEL_BASE, "page_values_seed.json")
CMD_F = os.path.join(PANEL_BASE, "cmd.json")
CMD_RES_F = os.path.join(PANEL_BASE, "cmd_result.json")
CFG_F = os.path.join(PANEL_BASE, "config.json")
KAT_F = os.path.join(PANEL_BASE, "bedienteil_katalog.csv")
REG_F = os.path.join(BRIDGE_BASE, "registers.json")
CACHE_F = os.path.join(BRIDGE_BASE, "cache_last.json")
BSTATE_F = os.path.join(BRIDGE_BASE, "bridge_state.json")
MAX_LIVE_AGE_S = 600      # older = "stale", shown greyed out
STATUS_HK1_REG = 1501
ST_HC = {0: "Aus", 1: "Heizen normal", 2: "Heizen Komfort", 3: "Heizen Eco", 4: "Frostschutz", 5: "Zwangsabnahme",
         6: "Zwangsreduktion", 7: "Ferien", 8: "Party", 9: "Kühlen normal", 12: "Störung", 13: "Handbetrieb",
         22: "Kühlen extern", 23: "Heizen extern", 26: "SmartGrid"}

LAST_WRITE_TS = 0
MIN_WRITE_INTERVAL = 2.0
WRITE_WHITELIST = {
    (1, 0, 3051): (150, 260, 1, "03-051 Normal-Raumtemperatur Heizen HK1 (15,0-26,0 °C)"),
    (1, 0, 3053): (150, 240, 1, "03-053 Spar-Raumtemperatur Heizen HK1 (15,0-24,0 °C)"),
    (1, 0, 3054): (200, 280, 1, "03-054 Normal-Raumtemperatur Kühlen HK1 (20,0-28,0 °C)"),
}
WRITE_HINWEIS = "Vor dem Ändern prüfen, dass weder Loxone noch ein Pi-Dienst denselben Wert nachschreibt."

_reg_cache = {"mtime": None, "rows": [], "by_key": {}}
_kat_cache = {"mtime": None, "rows": []}


def _load_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def _fachmann_code():
    """Code only from the panel's config.json - never in source or HTML."""
    return str(_load_json(CFG_F, {}).get("fachmann_code", "")).strip()


def _send_cmd(cmd):
    if not os.path.isdir(PANEL_BASE):
        return False
    try:
        tmp = CMD_F + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(cmd, f)
        os.replace(tmp, CMD_F)
        return True
    except Exception:
        return False


def _registers():
    """registers.json (official list) indexed by 'fg_fn_dp'; reloaded only when the file changes."""
    try:
        mt = os.path.getmtime(REG_F)
    except OSError:
        return [], {}
    if _reg_cache["mtime"] != mt:
        rows = _load_json(REG_F, [])
        by_key = {}
        for r in rows if isinstance(rows, list) else []:
            k = f"{r.get('fg', 0)}_{r.get('fn', 0)}_{r.get('dp', 0)}"
            by_key.setdefault(k, r)
        _reg_cache.update(mtime=mt, rows=rows if isinstance(rows, list) else [], by_key=by_key)
    return _reg_cache["rows"], _reg_cache["by_key"]


def _bridge_values():
    """{reg: (raw_u16, age_s)} from the bridge's warm cache, ages per register if available."""
    cache = _load_json(CACHE_F, {})
    regs = cache.get("regs") or {}
    bstate = _load_json(BSTATE_F, {}) or {}
    ages = bstate.get("reg_age_s") or {}
    # reg_age_s is relative to bridge_state.json's own timestamp; without it fall back to the cache time
    ref = float(bstate.get("ts", 0) or 0) if ages else float(cache.get("ts", 0) or 0)
    base_age = max(0, time.time() - ref)
    out = {}
    for k, v in regs.items():
        try:
            out[int(k)] = (int(v), base_age + float(ages.get(str(k), 1e9) if ages else 0))
        except (TypeError, ValueError):
            continue
    return out


def _scale(reg_row, raw):
    """Raw U16 from the bridge -> number according to type/decimal of registers.json."""
    if raw is None:
        return None
    typ = str(reg_row.get("type", "")).upper()
    if typ.startswith("S") and raw >= 0x8000:
        raw -= 0x10000
    if raw in (-32768, 32768):
        return None    # "no value"
    dec = int(reg_row.get("decimal") or 0)
    return raw / (10 ** dec) if dec else raw


FG_NAMES = {0: "Allgemein", 2: "Warmwasser", 50: "Lüftung", 60: "Wärmeerzeuger (Verdichter)"}


def _fg_name(fg, fn):
    """Folder name for the generated catalogue (function group of the datapoint list)."""
    try:
        fg, fn = int(fg), int(fn)
    except (TypeError, ValueError):
        return "Sonstige"
    if fg == 1:
        return "Heizkreis %d" % (fn + 1)
    return FG_NAMES.get(fg, "Funktionsgruppe %d" % fg)


def _load_katalog():
    """Own catalogue (CSV) if present, else generated from registers.json."""
    try:
        mt = os.path.getmtime(KAT_F)
    except OSError:
        mt = None
    if mt is not None:
        if _kat_cache["mtime"] != mt:
            rows = []
            try:
                with open(KAT_F, encoding="utf-8") as f:
                    rows = [dict(r) for r in csv.DictReader(f, delimiter=";")]
            except Exception as e:
                rows = [{"Pfad": "Service", "Parameter": "—", "Bezeichnung": "Katalog nicht lesbar", "Wert": str(e)}]
            _kat_cache.update(mtime=mt, rows=rows)
        return [dict(r) for r in _kat_cache["rows"]]
    regs, _ = _registers()
    rows = []
    for r in regs:
        unit = str(r.get("unit_name") or "Gerät")
        dec = int(r.get("decimal") or 0)
        rows.append({"Pfad": "Service › " + unit + " › " + _fg_name(r.get("fg", 0), r.get("fn", 0)),
                     "Parameter": f"{r.get('fg', 0)}-{r.get('fn', 0)}-{r.get('dp', 0)} · Reg {r.get('reg')}",
                     "Bezeichnung": r.get("name", ""), "Wert": "", "Dez": dec,
                     "Einheit": r.get("unit", ""), "CAN_Key": f"{r.get('fg', 0)}_{r.get('fn', 0)}_{r.get('dp', 0)}",
                     "Reg": str(r.get("reg", ""))})
    if not rows:
        rows.append({"Pfad": "Service", "Parameter": "—", "Bezeichnung": "Kein Katalog: weder " + KAT_F + " noch " + REG_F,
                     "Wert": ""})
    return rows


def _panel_values():
    vals = _load_json(SEED_F, {})
    for k, v in (_load_json(VAL_F, {}) or {}).items():
        if not isinstance(v, dict):
            continue
        old = vals.get(k)
        if not old or v.get("ts", 0) >= old.get("ts", 0):
            merged = dict(v)
            if old and old.get("ascii") and not merged.get("ascii"):
                merged["ascii"] = old["ascii"]
            vals[k] = merged
    return vals


def _q(qs, key, default=""):
    v = (qs or {}).get(key, default)
    return v[0] if isinstance(v, list) and v else (v if not isinstance(v, list) else default)


def display_api(qs_dict=None):
    """GET /api/display  - home values every poll, catalogue only with ?kat=1 (it is large)."""
    now = time.time()
    vals = _panel_values()
    bridge = _bridge_values()
    _, reg_by_key = _registers()

    def gv(key, div=10.0):
        """(value, age) from panel live values, else bridge cache; (None, None) if nothing known."""
        h = vals.get(key) or (vals.get("HV_" + key) if not key.startswith("HV_") else None)
        best = None
        if h and h.get("val") is not None and h.get("val") != -32768:
            best = (round(h["val"] / div, 1), max(0, round(now - h.get("ts", 0))))
        rr = reg_by_key.get(key)
        if rr and int(rr.get("reg", 0)) in bridge:
            raw, age = bridge[int(rr["reg"])]
            v = _scale(rr, raw)
            if v is not None and (best is None or age < best[1]):
                best = (round(float(v), 1), round(age))
        return best if best else (None, None)

    home = {}
    for name, key, div in (("aussen", "0_0_0", 10.0), ("raum_ist", "1_0_1", 10.0), ("vl_ist", "10_1_7", 10.0),
                           ("ww_ist", "2_0_4", 10.0), ("kwl_mod", "50_0_40651", 1.0), ("feuchte", "50_0_40652", 1.0),
                           ("raum_soll", "1_0_3051", 10.0)):
        v, a = gv(key, div)
        home[name] = {"v": v, "age": a, "alt": (a is None or a > MAX_LIVE_AGE_S)}
    home["hk_name"] = "Heizkreis 1"
    st = bridge.get(STATUS_HK1_REG)
    home["mode_text"] = (ST_HC.get(st[0], "Status %d" % st[0]) if st and st[1] <= MAX_LIVE_AGE_S else None)

    panel_stat = _load_json(STAT_F, None) or {}
    if panel_stat:
        try:
            age = now - time.mktime(time.strptime(panel_stat.get("zeit", ""), "%Y-%m-%d %H:%M:%S"))
            panel_stat["veraltet"] = age > 30
        except ValueError:
            panel_stat["veraltet"] = True
    panel_stat["anzahl_werte"] = len(vals)
    out = {"ok": True, "home": home, "max_live_age_s": MAX_LIVE_AGE_S, "panel": panel_stat,
           "schreiben_moeglich": bool(_fachmann_code()) and bool(_load_json(CFG_F, {}).get("schreiben_erlaubt", False)),
           "hinweis_schreiben": WRITE_HINWEIS, "zeit": time.strftime("%H:%M:%S")}

    if _q(qs_dict, "kat") == "1":
        rows = _load_katalog()
        for r in rows:
            key = r.get("CAN_Key", "") or ""
            hit = vals.get(key) if key else None
            if not hit and key.startswith(("HV_", "WEZ_", "BM_")):
                hit = vals.get(key.split("_", 1)[1])
            if hit and (hit.get("val") is not None or hit.get("ascii") or hit.get("hex")):
                r["live_raw"] = hit.get("val")
                if hit.get("ascii"):
                    r["live_ascii"] = hit["ascii"]
                r["live_age_s"] = max(0, round(now - hit.get("ts", 0)))
            rr = reg_by_key.get(key.split("_", 1)[1] if key.startswith(("HV_", "WEZ_", "BM_")) else key)
            if rr and int(rr.get("reg", 0)) in bridge:
                raw, age = bridge[int(rr["reg"])]
                if r.get("live_age_s") is None or age < r["live_age_s"]:
                    v = _scale(dict(rr, decimal=0), raw)     # raw, decimals applied in the browser
                    if v is not None:
                        r["live_raw"], r["live_age_s"] = v, round(age)
                        r.pop("live_ascii", None)
            parts = key.split("_")
            if len(parts) == 3 and all(p.lstrip("-").isdigit() for p in parts):
                t = tuple(int(p) for p in parts)
                if t in WRITE_WHITELIST:
                    mn, mx, dec, txt = WRITE_WHITELIST[t]
                    r["write"] = {"fg": t[0], "fn": t[1], "dp": t[2], "min": mn, "max": mx, "dec": dec, "text": txt}
        out["katalog"] = rows
    return out


def display_set_api(raw_bytes):
    """POST /api/display/set - check_code or write one whitelisted setpoint via the panel daemon."""
    global LAST_WRITE_TS
    try:
        payload = json.loads(raw_bytes.decode("utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("kein Objekt")
    except Exception as e:
        return {"ok": False, "fehler": f"Ungültiges JSON: {e}"}
    code = str(payload.get("code", "")).strip()
    fc = _fachmann_code()
    if not fc:
        return {"ok": False, "fehler": "Kein Code eingerichtet (config.json des Panel-Dienstes) - Schreiben ist aus."}
    if code != fc:
        time.sleep(1.0)  # slows down guessing
        return {"ok": False, "fehler": "Ungültiger Code"}
    if payload.get("action") == "check_code":
        return {"ok": True}
    try:
        fg, fn, dp, val = int(payload["fg"]), int(payload["fn"]), int(payload["dp"]), int(payload["val"])
    except (KeyError, TypeError, ValueError) as e:
        return {"ok": False, "fehler": f"Fehlende/ungültige Parameter: {e}"}
    wl = WRITE_WHITELIST.get((fg, fn, dp))
    if not wl:
        return {"ok": False, "fehler": f"[{fg}-{fn}-{dp}] ist über das Display nicht verstellbar (nicht in der Whitelist)."}
    mn, mx, dec, txt = wl
    if not (mn <= val <= mx):
        return {"ok": False, "fehler": f"Wert {val} außerhalb [{mn}..{mx}] für {txt}"}
    now = time.time()
    if now - LAST_WRITE_TS < MIN_WRITE_INTERVAL:
        return {"ok": False, "fehler": "Bitte kurz warten (max. ein Schreibbefehl alle 2 s)."}
    LAST_WRITE_TS = now
    req_id = f"set_{dp}_{int(now * 1000)}"
    if not _send_cmd({"action": "set", "id": req_id, "fg": fg, "fn": fn, "dp": dp, "val": val,
                      "code": code, "user": "web"}):
        return {"ok": False, "fehler": "Panel-Dienst nicht eingerichtet (" + PANEL_BASE + " fehlt)"}
    t0 = time.time()
    while time.time() - t0 < 4.0:
        time.sleep(0.1)
        res = _load_json(CMD_RES_F, {})
        if res.get("id") == req_id:
            return {"ok": res.get("ok", False), "nachricht": res.get("message", "") or res.get("error", ""),
                    "readback": res.get("readback")}
    try:
        os.remove(CMD_F)   # not picked up -> do not leave a stale write command behind
    except OSError:
        pass
    return {"ok": False, "fehler": "Keine Antwort vom Panel-Dienst in 4 s (Dienst aus? Modus trocken? Nachtsperre?) - nichts gesendet."}


def display_page(lang="de"):
    return _PAGE


_PAGE = r"""
<style>
.tte-wrap{display:flex;justify-content:center;padding:12px 0 30px;font-family:'Inter',system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;user-select:none}
.tte-bezel{background:#f8fafc;border:14px solid #f1f5f9;border-radius:22px;box-shadow:0 24px 55px rgba(0,0,0,.35),inset 0 2px 4px rgba(255,255,255,.9);padding:26px 32px 32px 58px;max-width:980px;width:100%;position:relative;box-sizing:border-box}
.tte-brand{position:absolute;right:34px;top:6px;display:flex;align-items:center;gap:3px;font-weight:900;font-size:.95rem;letter-spacing:.5px}
.tte-brand .hox{color:#1e293b}.tte-brand .pi{color:#16a34a;background:#dcfce7;padding:1px 5px;border-radius:4px}
.tte-led{position:absolute;left:24px;top:50%;transform:translateY(-50%);width:14px;height:14px;border-radius:50%;background:#22c55e;box-shadow:0 0 14px #22c55e}
.tte-led.off{background:#f87171;box-shadow:0 0 14px #f87171}
.tte-scr{background:#000a17;border:3px solid #0f172a;border-radius:8px;height:520px;display:flex;flex-direction:column;overflow:hidden;color:#fff;position:relative}
.tte-topbar{height:36px;border-bottom:1px solid #03395b;display:flex;align-items:center;justify-content:space-between;padding:0 16px;background:#011627;font-size:.85rem;color:#7dd3fc}
.tte-topbar-left{display:flex;align-items:center;gap:10px}
.tte-back-btn{background:transparent;border:0;color:#38bdf8;font-size:.88rem;font-weight:700;cursor:pointer;display:flex;align-items:center;gap:4px;padding:4px 8px;border-radius:4px}
.tte-back-btn:hover{background:#03426d;color:#fff}
.tte-topbar-title{font-weight:700;color:#e0f2fe;font-size:1rem}
.tte-topbar-right{display:flex;align-items:center;gap:12px;color:#94a3b8}
.tte-view-pane{flex:1;display:flex;overflow:hidden;position:relative}
.orig-home{flex:1;display:flex;height:100%}
.orig-col{padding:16px 20px;display:flex;flex-direction:column;justify-content:space-between;position:relative}
.orig-col-left{width:30%;border-right:1px solid #0284c7}
.orig-col-mid{width:42%;border-right:1px solid #0284c7;padding:16px 14px;align-items:center}
.orig-col-right{width:28%;padding:18px 20px}
.col-hdr-btn{font-size:1.15rem;color:#38bdf8;font-weight:700;cursor:pointer;display:inline-flex;align-items:center;gap:4px}
.col-hdr-btn:hover{color:#bae6fd}
.soll-block{margin:auto 0;cursor:pointer}
.soll-lbl{font-size:.95rem;color:#7dd3fc;margin-bottom:2px;font-weight:600}
.soll-row{display:flex;align-items:center;gap:12px}
.soll-val{font-size:3.1rem;font-weight:800;color:#facc15;letter-spacing:-1px;line-height:1}
.soll-unit{font-size:1.5rem;color:#facc15;font-weight:700;vertical-align:top;margin-left:3px}
.adj-bar{border:1.5px solid #0284c7;border-radius:4px;padding:4px 8px;color:#38bdf8;font-size:1.3rem;font-weight:800;cursor:pointer;line-height:1}
.adj-bar:hover{background:#0284c7;color:#fff}
.rf1-hint{font-size:.82rem;color:#64748b;margin-top:8px}.rf1-hint b{color:#38bdf8;font-size:.92rem}
.mid-top{display:flex;align-items:center;gap:18px;margin-bottom:4px;width:100%;justify-content:center}
.sun-svg{width:52px;height:52px}.aussen-txt{font-size:1.9rem;font-weight:700;color:#e0f2fe}
.house-box{margin:auto 0;display:flex;justify-content:center;width:100%;cursor:pointer}
.orig-house-svg{width:220px;height:220px}
.right-top{display:flex;flex-direction:column;justify-content:center;height:45%;cursor:pointer}
.ww-row{display:flex;align-items:center;gap:16px}
.tap-svg{width:52px;height:52px}.ww-val{font-size:2.8rem;font-weight:800;color:#38bdf8;line-height:1}
.right-bot{display:flex;flex-direction:column;justify-content:flex-end;height:55%}
.kwl-row{display:flex;align-items:center;gap:14px;font-size:1.5rem;font-weight:700;color:#38bdf8;cursor:pointer;margin-bottom:12px}
.kwl-row:hover{color:#bae6fd}.kwl-icon{width:32px;height:32px}
.gear-box{display:flex;justify-content:flex-end;margin-top:6px}
.gear-btn{background:transparent;border:0;color:#38bdf8;font-size:2.1rem;cursor:pointer;padding:4px;line-height:1}
.tte-drop-m{display:none;position:absolute;background:#011627;border:2px solid #0284c7;border-radius:8px;padding:8px 0;z-index:50;box-shadow:0 12px 30px rgba(0,0,0,.8)}
.tte-drop-item{padding:8px 18px;font-size:.9rem;color:#cbd5e1;cursor:pointer}
.tte-drop-item:hover{background:#0284c7;color:#fff}.tte-drop-item.active{color:#facc15;font-weight:700}
.orig-menu{flex:1;display:none;flex-direction:column;padding:18px 26px;justify-content:space-between}
.menu-title{font-size:1.2rem;color:#38bdf8;font-weight:700}
.menu-grid{display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(2,1fr);gap:18px 30px;margin:auto 0}
.menu-tile{display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;text-align:center}
.menu-circle{width:68px;height:68px;border-radius:50%;border:2.5px solid #0284c7;display:flex;align-items:center;justify-content:center;margin-bottom:6px;background:#011627}
.menu-circle:hover{background:#03294c;border-color:#38bdf8}
.menu-circle.green{border-color:#34d399}.menu-circle.white{border-color:#e0e7ff}
.menu-label{font-size:.85rem;color:#e0f2fe;font-weight:600}
.menu-footer{display:flex;justify-content:space-between;align-items:center;padding:0 8px}
.menu-nav-btn{background:transparent;border:1.5px solid #0284c7;border-radius:50%;width:38px;height:38px;color:#38bdf8;font-size:1.3rem;cursor:pointer}
.menu-nav-btn:hover{background:#0284c7;color:#fff}
.menu-page-dots{font-size:.9rem;color:#7dd3fc;font-weight:700}
.tte-srv{flex:1;display:none;flex-direction:column;overflow:hidden}
.tte-srv-head{padding:10px 16px;border-bottom:1px solid #03395b;display:flex;align-items:center;justify-content:space-between;background:#011627;gap:8px}
.tte-bc{font-size:.85rem;color:#7dd3fc;display:flex;align-items:center;gap:4px;flex-wrap:wrap}
.tte-bc-it{color:#38bdf8;cursor:pointer}.tte-bc-it:hover{text-decoration:underline}
.tte-search{background:#02142b;border:1px solid #03426d;color:#fff;border-radius:4px;padding:3px 8px;font-size:.8rem;width:150px}
.tte-tbl-w{flex:1;overflow-y:auto;background:#000a17}
.tte-tbl{width:100%;border-collapse:collapse;font-size:.8rem;background:transparent;border-radius:0;margin-top:0}
.tte-tbl th{position:sticky;top:0;background:#03294c;color:#7dd3fc;text-align:left;padding:8px 10px;border-bottom:1px solid #0284c7}
.tte-tbl td{padding:8px 10px;border-bottom:1px solid #08213b;color:#cbd5e1;text-align:left}
.tte-tbl tr,.tte-tbl td{background:transparent}
.tte-tbl tbody tr:nth-child(even),.tte-tbl tbody tr:nth-child(odd){background:transparent}
.tte-tbl tr:hover,.tte-tbl tbody tr:hover{background:#031d36}
.tte-tbl .fold{color:#38bdf8;font-weight:700;cursor:pointer}
.tte-val-box{font-weight:700;color:#facc15}
.tte-w-btn{background:#0284c7;color:#fff;border:0;border-radius:4px;padding:3px 8px;font-size:.72rem;cursor:pointer;font-weight:700}
.tte-mbg{display:none;position:fixed;inset:0;background:rgba(0,0,0,.75);z-index:9999;align-items:center;justify-content:center}
.tte-m{background:#0f172a;border:2px solid #0284c7;border-radius:12px;padding:24px 28px;max-width:440px;width:90%;color:#fff}
.tte-m h3{margin:0 0 12px;font-size:1.15rem;color:#38bdf8}
.tte-m input{width:100%;background:#02142b;border:1.5px solid #03426d;color:#fff;padding:10px 12px;border-radius:6px;font-size:1.2rem;font-weight:700;box-sizing:border-box}
.tte-m button{padding:8px 16px;border-radius:6px;font-weight:700;border:0;cursor:pointer;font-size:.88rem;margin-left:8px}
.tte-note{font-size:.75rem;color:#64748b;text-align:center;margin-top:6px}
</style>

<div class="tte-wrap">
 <div class="tte-bezel">
  <div class="tte-brand"><span class="hox">Hox</span><span class="pi">Pi</span></div>
  <div class="tte-led" id="led"></div>
  <div class="tte-scr">
   <div class="tte-topbar">
    <div class="tte-topbar-left">
     <button class="tte-back-btn" id="topBackBtn" style="display:none" onclick="showWallHome()">‹ Startseite</button>
     <div class="tte-topbar-title" id="topTitle">HoxPi Remote Console</div>
    </div>
    <div class="tte-topbar-right">
     <span id="panelTxt" title="Zustand des Panel-Dienstes (hoxpi-panel)"></span>
     <span id="topClock">--:--</span>
     <span style="font-size:1.1rem;cursor:pointer" onclick="openMenuPage(1)" title="Menü">⚙️</span>
    </div>
   </div>

   <div class="tte-view-pane">
    <div class="orig-home" id="viewHome">
     <div class="orig-col orig-col-left">
      <div>
       <div class="col-hdr-btn" onclick="toggleHkDrop(event)" title="Heizkreis">
        <span id="hkNameLbl">Heizkreis 1</span> <span style="font-size:.9rem">˅</span>
       </div>
       <div class="tte-drop-m" id="hkDrop" style="top:44px;left:18px">
        <div class="tte-drop-item active" onclick="closeDrops()">● Heizkreis 1</div>
        <div class="tte-drop-item" style="color:#64748b">○ weitere Heizkreise: noch nicht unterstützt</div>
       </div>
      </div>
      <div class="soll-block" onclick="sollClick()" title="Normal-Raumtemperatur HK1 (03-051)">
       <div class="soll-lbl">Raum-Soll (03-051)</div>
       <div class="soll-row">
        <div><span class="soll-val" id="sollVal">—</span><span class="soll-unit">°C</span></div>
        <div class="adj-bar">±</div>
       </div>
       <div class="rf1-hint">Raum-Ist: <b id="rf1Val">—</b></div>
      </div>
      <div><div class="col-hdr-btn" title="Status Heizkreis 1 (Register 1501, nur Anzeige)"><span id="modeLbl">—</span></div></div>
     </div>

     <div class="orig-col orig-col-mid">
      <div class="mid-top">
       <svg class="sun-svg" viewBox="0 0 100 100" aria-hidden="true">
        <circle cx="50" cy="50" r="22" fill="#22c55e"/>
        <g stroke="#22c55e" stroke-width="6" stroke-linecap="round">
         <line x1="50" y1="12" x2="50" y2="20"/><line x1="50" y1="80" x2="50" y2="88"/>
         <line x1="12" y1="50" x2="20" y2="50"/><line x1="80" y1="50" x2="88" y2="50"/>
         <line x1="23" y1="23" x2="29" y2="29"/><line x1="71" y1="71" x2="77" y2="77"/>
         <line x1="23" y1="77" x2="29" y2="71"/><line x1="71" y1="29" x2="77" y2="23"/>
        </g>
       </svg>
       <div class="aussen-txt" id="aussenTxt" title="Außentemperatur">—</div>
      </div>
      <div class="house-box" onclick="goFolder('Heizkreis 1')" title="Parameter Heizkreis 1">
       <svg class="orig-house-svg" viewBox="0 0 200 200" aria-hidden="true">
        <polygon points="100,10 185,85 170,85 170,185 30,185 30,85 15,85" fill="#003554" stroke="#0284c7" stroke-width="4"/>
        <line x1="30" y1="95" x2="170" y2="95" stroke="#0284c7" stroke-width="3" stroke-dasharray="4 4"/>
        <text x="100" y="68" fill="#38bdf8" font-size="28" font-weight="800" text-anchor="middle" id="houseKwl">—</text>
        <text x="100" y="85" fill="#7dd3fc" font-size="12" font-weight="600" text-anchor="middle">Lüftung</text>
        <text x="100" y="145" fill="#facc15" font-size="34" font-weight="800" text-anchor="middle" id="houseVl">—</text>
        <text x="100" y="165" fill="#7dd3fc" font-size="12" font-weight="600" text-anchor="middle">Vorlauf Heizkreis</text>
       </svg>
      </div>
      <div style="font-size:.78rem;color:#64748b;text-align:center" id="syncTxt">HoxPi Live-Sync</div>
     </div>

     <div class="orig-col orig-col-right">
      <div class="right-top" onclick="goFolder('Warmwasser')" title="Warmwasser-Parameter">
       <div class="ww-row">
        <svg class="tap-svg" viewBox="0 0 64 64" fill="none" aria-hidden="true">
         <path d="M12 36 C12 24 24 16 38 16 H44 V26 H38 C32 26 26 30 26 36 V40 H12 Z" fill="#38bdf8"/>
         <rect x="36" y="8" width="16" height="8" rx="2" fill="#38bdf8"/>
         <rect x="42" y="26" width="10" height="6" fill="#38bdf8"/>
         <ellipse cx="47" cy="42" rx="3.5" ry="5.5" fill="#38bdf8"/>
         <ellipse cx="47" cy="54" rx="2.5" ry="4" fill="#38bdf8"/>
        </svg>
        <div class="ww-val" id="wwVal">—</div>
       </div>
       <div style="font-size:.78rem;color:#7dd3fc;margin-top:4px">Warmwasser</div>
      </div>
      <div class="right-bot">
       <div class="kwl-row" onclick="goFolder('Lüftung')" title="Lüftung: Modulation">
        <svg class="kwl-icon" viewBox="0 0 24 24" fill="#38bdf8" aria-hidden="true"><path d="M12 12 Q18 4 24 8 Q20 16 12 12 Z M12 12 Q20 18 16 24 Q8 20 12 12 Z M12 12 Q4 20 0 16 Q4 8 12 12 Z M12 12 Q4 4 8 0 Q16 4 12 12 Z"/></svg>
        <span id="kwlVal">—</span>
       </div>
       <div class="kwl-row" onclick="goFolder('Lüftung')" title="Lüftung: Feuchte" style="font-size:1.3rem">
        <svg class="kwl-icon" viewBox="0 0 24 24" fill="#38bdf8" aria-hidden="true"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>
        <span id="kwlHum">—</span>
       </div>
       <div class="gear-box"><button class="gear-btn" onclick="openMenuPage(1)" title="Menü">⚙️</button></div>
      </div>
     </div>
    </div>

    <div class="orig-menu" id="viewMenu">
     <div style="display:flex;justify-content:space-between;align-items:center">
      <div class="menu-title">Menü</div>
      <button class="tte-back-btn" onclick="showWallHome()">‹ Zurück zur Startseite</button>
     </div>
     <div class="menu-grid" id="menuGrid"></div>
     <div class="menu-footer">
      <button class="menu-nav-btn" onclick="menuStep(-1)">‹</button>
      <div class="menu-page-dots" id="menuPageNum">1/2</div>
      <button class="menu-nav-btn" onclick="menuStep(1)">›</button>
     </div>
    </div>

    <div class="tte-srv" id="viewService">
     <div class="tte-srv-head">
      <div class="tte-bc" id="bc"></div>
      <div style="display:flex;gap:8px;align-items:center">
       <input class="tte-search" id="srch" placeholder="Suchen…" oninput="render()">
       <button class="tte-back-btn" onclick="openMenuPage(curMenuPage||1)">‹ Menü</button>
       <button class="tte-back-btn" onclick="showWallHome()">‹ Startseite</button>
      </div>
     </div>
     <div class="tte-tbl-w">
      <table class="tte-tbl">
       <thead><tr><th>Parameter</th><th>Bezeichnung</th><th>Wert</th><th>Status</th><th>Aktion</th></tr></thead>
       <tbody id="tb"></tbody>
      </table>
     </div>
    </div>
   </div>
  </div>
  <div class="tte-note">Eigenständige Anzeige von HoxPi, nicht mit Hoval AG verbunden. Werte mit Alter; grau = älter als 10 min.</div>
 </div>
</div>

<div id="toast" style="display:none;position:fixed;left:50%;top:18px;transform:translateX(-50%);background:#0f172a;color:#fff;border:1px solid #38bdf8;border-radius:8px;padding:10px 16px;z-index:10000;font-size:.9rem"></div>

<div class="tte-mbg" id="pinM">
 <div class="tte-m">
  <h3>Freischaltung</h3>
  <input type="password" id="pinI" placeholder="Code eingeben" maxlength="12" onkeydown="if(event.key==='Enter')pinOk()">
  <div style="margin:10px 0;font-size:.78rem;color:#94a3b8">Code aus der config.json des Panel-Dienstes. Ist die Anmeldung (2FA) aktiv, braucht Schreiben zusätzlich die Anmeldung auf der Seite „Sicherheit“.</div>
  <div style="text-align:right">
   <button style="background:#334155;color:#fff" onclick="hide('pinM')">Abbrechen</button>
   <button style="background:#facc15;color:#0f172a" onclick="pinOk()">OK</button>
  </div>
 </div>
</div>

<div class="tte-mbg" id="edM">
 <div class="tte-m">
  <h3 id="edT"></h3>
  <div id="edH" style="font-size:.78rem;color:#fbbf24;margin:6px 0 10px"></div>
  <input type="number" id="edI" step="0.5">
  <div style="text-align:right;margin-top:14px">
   <button style="background:#334155;color:#fff" onclick="hide('edM')">Abbrechen</button>
   <button style="background:#facc15;color:#0f172a" id="edS" onclick="edSend()">An Anlage senden</button>
  </div>
 </div>
</div>

<script>
let KAT=[], path=['Service'], unl=false, unlCode='', edRow=null, curMenuPage=1, ONLINE=true, WRITE_OK=false, katBusy=false;
const SEP=' › ';
function esc(s){ return String(s==null?'':s).replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }

const MENU_PAGES = {
 1: [
  {title:'Heizkreise', icon:'floor', go:'Heizkreis 1'},
  {title:'Warmwasser', icon:'tap', go:'Warmwasser'},
  {title:'Lüftung', icon:'fan', go:'Lüftung'},
  {title:'Wärmeerzeuger', icon:'chart', go:'Wärmeerz'},
  {title:'Programme', icon:'time', cls:'green', go:'Wochenprogramm'},
  {title:'Startseite', icon:'net', home:true}
 ],
 2: [
  {title:'Alle Parameter', icon:'tool', service:true},
  {title:'Freischaltung', icon:'key', cls:'white', lock:true},
  {title:'Energiemanager', icon:'pv', go:'Wärmemanager'},
  {title:'Info', icon:'info', go:'CAN'}
 ]
};
const NPAGES = Object.keys(MENU_PAGES).length;

const ICONS = {
 chart:'<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.5"><polyline points="3 17 9 9 14 15 21 7"/></svg>',
 net:'<svg width="34" height="34" viewBox="0 0 24 24" fill="#38bdf8"><path d="M12 3 L22 12 L19 12 L19 21 L5 21 L5 12 L2 12 Z"/></svg>',
 floor:'<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.5"><path d="M4 6 H20 V10 H8 V14 H20 V18 H4"/></svg>',
 tap:'<svg width="34" height="34" viewBox="0 0 24 24" fill="#38bdf8"><path d="M4 12 H14 V8 H18 V12 H20 V15 H18 V17 H15 V15 H4 Z M16 19 Q17 22 17 23 A1.5 1.5 0 0 1 14 23 Q14 22 16 19 Z"/></svg>',
 time:'<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7 V12 L16 14"/></svg>',
 info:'<svg width="34" height="34" viewBox="0 0 24 24" fill="#38bdf8"><circle cx="12" cy="7" r="2"/><rect x="10" y="11" width="4" height="8" rx="1"/></svg>',
 key:'<svg width="34" height="34" viewBox="0 0 24 24" fill="#e0e7ff"><circle cx="12" cy="8" r="4"/><path d="M10 12 L10 20 L13 20 L13 18 L14 18 L14 16 L12 16 L12 12 Z"/></svg>',
 tool:'<svg width="34" height="34" viewBox="0 0 24 24" fill="#38bdf8"><path d="M14 4 A4 4 0 0 1 18 10 L8 20 L4 16 L14 6 Z"/></svg>',
 fan:'<svg width="34" height="34" viewBox="0 0 24 24" fill="#38bdf8"><path d="M12 12 Q18 4 24 8 Q20 16 12 12 Z M12 12 Q20 18 16 24 Q8 20 12 12 Z M12 12 Q4 20 0 16 Q4 8 12 12 Z M12 12 Q4 4 8 0 Q16 4 12 12 Z"/></svg>',
 pv:'<svg width="34" height="34" viewBox="0 0 24 24" fill="#38bdf8"><circle cx="6" cy="6" r="3"/><polygon points="8,10 20,10 17,21 5,21"/></svg>'
};

function views(home, menu, srv){
 document.getElementById('viewHome').style.display = home ? 'flex' : 'none';
 document.getElementById('viewMenu').style.display = menu ? 'flex' : 'none';
 document.getElementById('viewService').style.display = srv ? 'flex' : 'none';
 document.getElementById('topBackBtn').style.display = home ? 'none' : 'flex';
 closeDrops();
}
function showWallHome(){ views(1,0,0); document.getElementById('topTitle').textContent='HoxPi Remote Console'; }
function openMenuPage(pg){
 curMenuPage = pg; renderMenuGrid(); views(0,1,0);
 document.getElementById('topTitle').textContent = 'Menü (' + pg + '/' + NPAGES + ')';
}
function menuStep(dir){
 curMenuPage += dir;
 if(curMenuPage < 1) curMenuPage = NPAGES;
 if(curMenuPage > NPAGES) curMenuPage = 1;
 openMenuPage(curMenuPage);
}
function tileClick(i){
 const it = (MENU_PAGES[curMenuPage] || [])[i]; if(!it) return;
 if(it.home) showWallHome(); else if(it.lock) lockClick(); else if(it.service) openServiceDirect(); else goFolder(it.go);
}
function renderMenuGrid(){
 document.getElementById('menuPageNum').textContent = curMenuPage + '/' + NPAGES;
 const items = MENU_PAGES[curMenuPage] || [];
 document.getElementById('menuGrid').innerHTML = items.map((it, i) =>
  `<div class="menu-tile" onclick="tileClick(${i})"><div class="menu-circle ${it.cls||''}">${ICONS[it.icon]||''}</div><div class="menu-label">${esc(it.title)}</div></div>`).join('');
}
function openService(title){
 views(0,0,1); document.getElementById('topTitle').textContent = title;
 if(!KAT.length) loadKat(); else render();
}
function openServiceDirect(){ path=['Service']; openService('Alle Parameter'); }
function goFolder(sub){
 if(!KAT.length){ views(0,0,1); document.getElementById('tb').innerHTML='<tr><td colspan="5" style="color:#64748b">lädt…</td></tr>'; loadKat().then(() => goFolder(sub)); return; }
 const f = KAT.find(r => r.Pfad && r.Pfad.toLowerCase().includes(sub.toLowerCase()));
 path = f ? f.Pfad.split(SEP) : ['Service'];
 if(!f && KAT.length) document.getElementById('srch').value = sub;
 openService('Parameter › ' + sub);
}
function toggleHkDrop(ev){
 if(ev) ev.stopPropagation();
 const el = document.getElementById('hkDrop');
 el.style.display = (el.style.display === 'block') ? 'none' : 'block';
}
function closeDrops(){ document.getElementById('hkDrop').style.display = 'none'; }
document.addEventListener('click', closeDrops);
function toast(t){ const e=document.getElementById('toast'); e.textContent=t; e.style.display='block'; clearTimeout(window._tt); window._tt=setTimeout(()=>e.style.display='none',4500); }
function sollClick(){
 if(!WRITE_OK){ toast('Schreiben ist aus (Panel-Dienst: kein Code oder schreiben_erlaubt=false).'); return; }
 const go = () => { const i = KAT.findIndex(r => r.CAN_Key === '1_0_3051' && r.write); if(i < 0){ toast('03-051 nicht im Katalog'); return; } edClick(i); };
 if(KAT.length) go(); else loadKat().then(go);
}
function fmtVal(it){
 if(it.live_ascii) return esc(it.live_ascii);
 if(it.live_raw == null) return (it.Wert ? esc(it.Wert) + ' <span style="color:#64748b;font-size:.7rem">(Katalog)</span>' : '—');
 const m = String(it.Wert||'').match(/^-?\d+[,.](\d+)$/);
 const dec = (it.Dez != null && it.Dez !== '') ? Number(it.Dez) : (m ? m[1].length : 0);
 let v = it.live_raw;
 if(dec > 0){ v = (it.live_raw / Math.pow(10, dec)).toFixed(dec).replace('.', ','); }
 return esc(v) + (it.Einheit ? ' ' + esc(it.Einheit) : '');
}
function fmtAge(a){
 if(a == null) return '';
 if(a < 120) return 'live';
 if(a < 3600) return 'vor ' + Math.round(a/60) + ' min';
 if(a < 86400) return 'vor ' + Math.round(a/3600) + ' h';
 return 'vor ' + Math.round(a/86400) + ' d';
}
function fitScreen(){
 const w = document.querySelector('.tte-wrap'), b = document.querySelector('.tte-bezel');
 if(!w || !b) return;
 b.style.transform=''; w.style.height='';
 const need = 900, have = w.clientWidth;
 if(have < need){ const k = have/need; b.style.width=need+'px'; b.style.maxWidth='none'; b.style.transform='scale('+k+')'; b.style.transformOrigin='top left'; w.style.justifyContent='flex-start'; w.style.height=(b.offsetHeight*k+40)+'px'; }
 else { b.style.width=''; b.style.maxWidth=''; w.style.justifyContent='center'; }
}
window.addEventListener('resize', fitScreen);

let FOLDS = [];
function render(){
 const q = (document.getElementById('srch').value || '').trim().toLowerCase();
 document.getElementById('bc').innerHTML = path.map((p, i) => `<span class="tte-bc-it" onclick="goPath(${i})">${esc(p)}</span>`).join(' <span>›</span> ');
 const cur = path.join(SEP), folds = new Set(), items = [];
 for(const r of KAT){
  const p = r.Pfad || '';
  if(q){
   if((p === cur || p.startsWith(cur + SEP)) && ((r.Bezeichnung||'') + ' ' + (r.Parameter||'')).toLowerCase().includes(q)) items.push(r);
  } else if(p === cur) items.push(r);
  else if(p.startsWith(cur + SEP)) folds.add(p.slice((cur + SEP).length).split(SEP)[0]);
 }
 FOLDS = Array.from(folds).sort();
 let h = FOLDS.map((f, i) => `<tr><td>📁</td><td class="fold" onclick="into(${i})">${esc(f)}</td><td>—</td><td>Ordner</td><td></td></tr>`).join('');
 for(const it of items.slice(0, 400)){
  const a = it.live_age_s, fresh = (a != null && a < 120);
  const st = (a == null) ? '<span style="color:#64748b">○ kein Livewert</span>'
           : fresh ? '<span style="color:#22c55e">● live</span>'
           : `<span style="color:#f59e0b" title="Wert ist ${a} s alt">● ${fmtAge(a)}</span>`;
  const btn = (it.write && WRITE_OK) ? `<button class="tte-w-btn" onclick="edClick(${it.idx})">Ändern</button>` : '';
  h += `<tr${fresh || a == null ? '' : ' style="opacity:.6"'}><td style="font-family:monospace;color:#94a3b8">${esc(it.Parameter||'—')}</td><td>${esc(it.Bezeichnung||'—')}</td><td class="tte-val-box">${fmtVal(it)}</td><td>${st}</td><td>${btn}</td></tr>`;
 }
 if(items.length > 400) h += `<tr><td colspan="5" style="color:#64748b">… ${items.length-400} weitere - Suche verfeinern</td></tr>`;
 document.getElementById('tb').innerHTML = h || '<tr><td colspan="5" style="text-align:center;color:#64748b;padding:20px">Keine Einträge</td></tr>';
}
function into(i){ path.push(FOLDS[i]); document.getElementById('srch').value=''; render(); }
function goPath(idx){ path = path.slice(0, idx+1); render(); }
function show(id){ document.getElementById(id).style.display='flex'; }
function hide(id){ document.getElementById(id).style.display='none'; }

function lockClick(){ show('pinM'); setTimeout(()=>document.getElementById('pinI').focus(), 50); }
function pinOk(){
 const val = document.getElementById('pinI').value.trim();
 document.getElementById('pinI').value = '';
 fetch('/api/display/set', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({action:'check_code', code: val})})
 .then(r => r.json()).then(res => {
  if(res.ok){ unl = true; unlCode = val; hide('pinM'); toast('Freigeschaltet (bis die Seite neu geladen wird).'); }
  else toast(res.fehler || 'Ungültiger Code');
 }).catch(() => toast('Pi nicht erreichbar'));
}
function edClick(idx){
 if(!unl){ lockClick(); return; }
 edRow = KAT[idx];
 const w = edRow.write;
 document.getElementById('edT').textContent = w.text;
 document.getElementById('edH').textContent = 'Bereich ' + (w.min/10).toFixed(1) + ' bis ' + (w.max/10).toFixed(1) + ' °C. Prüfe vorher, dass nicht Loxone denselben Wert nachschreibt.';
 document.getElementById('edI').value = ((edRow.live_raw != null ? edRow.live_raw : w.min) / 10).toFixed(1);
 show('edM');
}
function edSend(){
 const val = parseFloat(String(document.getElementById('edI').value).replace(',', '.'));
 const w = edRow && edRow.write;
 if(!w || !isFinite(val)){ toast('Ungültiger Wert'); return; }
 const raw = Math.round(val * 10);
 if(raw < w.min || raw > w.max){ toast('Außerhalb ' + (w.min/10).toFixed(1) + '…' + (w.max/10).toFixed(1) + ' °C'); return; }
 const b = document.getElementById('edS'); b.disabled = true;
 fetch('/api/display/set', {method:'POST', headers:{'Content-Type':'application/json'},
  body: JSON.stringify({fg: w.fg, fn: w.fn, dp: w.dp, val: raw, code: unlCode})})
 .then(r => r.json().then(j => [r.status, j])).then(([status, res]) => {
  if(status === 401){ toast(res.fehler || 'Nicht angemeldet (Seite Sicherheit)'); return; }
  if(res.ok){ toast('Gesendet und zurückgelesen: ' + (res.readback != null ? (res.readback/10).toFixed(1).replace('.', ',') + ' °C' : 'ok')); hide('edM'); loadKat(); }
  else toast('Nicht bestätigt: ' + (res.fehler || res.nachricht || 'unbekannt'));
 }).catch(() => toast('Pi nicht erreichbar - Ergebnis unbekannt')).finally(() => { b.disabled = false; });
}

function setHome(id, f, unit, dec){
 const el = document.getElementById(id);
 if(!f || f.v == null){ el.textContent = '—'; el.style.opacity = .5; return; }
 el.textContent = (dec ? f.v.toFixed(dec).replace('.', ',') : Math.round(f.v)) + unit;
 el.style.opacity = f.alt ? .45 : 1;
 if(el.setAttribute) el.setAttribute('data-age', f.alt ? ('veraltet: ' + fmtAge(f.age)) : ('live, ' + f.age + ' s alt'));
}
function setOffline(off){
 document.getElementById('led').classList.toggle('off', off);
 if(off === !ONLINE) return;
 ONLINE = !off;
 document.getElementById('topClock').style.color = off ? '#f87171' : '';
 document.getElementById('syncTxt').textContent = off ? 'KEINE VERBINDUNG ZUM PI - Werte eingefroren' : 'HoxPi Live-Sync';
 document.getElementById('syncTxt').style.color = off ? '#f87171' : '#64748b';
 document.querySelector('.tte-view-pane').style.opacity = off ? .45 : 1;
 if(off) document.getElementById('topClock').textContent = 'offline';
}
function panelText(p){
 if(!p || !p.modus) return 'Panel: aus';
 if(p.veraltet) return 'Panel: hängt';
 if(p.gesperrt) return 'Panel: NOTAUS';
 if(p.modus !== 'live') return 'Panel: trocken';
 return p.sendet ? 'Panel: live' : 'Panel: pausiert';
}
let katP = null;
function loadKat(){
 if(katBusy) return katP;
 katBusy = true;
 return katP = fetch('/api/display?kat=1', {cache:'no-store'}).then(r => r.json()).then(data => {
  if(data && data.katalog){
   KAT = data.katalog; KAT.forEach((r, i) => r.idx = i);
   const modalOpen = ['pinM','edM'].some(id => document.getElementById(id).style.display === 'flex');
   if(document.getElementById('viewService').style.display === 'flex' && !modalOpen) render();
  }
 }).catch(() => {}).finally(() => { katBusy = false; });
}
function poll(){
 fetch('/api/display', {cache:'no-store'}).then(r => r.json()).then(data => {
  if(!data.ok){ setOffline(true); return; }
  setOffline(false);
  WRITE_OK = !!data.schreiben_moeglich;
  document.getElementById('topClock').textContent = (data.zeit || '').slice(0,5);
  const p = data.panel || {}; const pt = panelText(p);
  const pe = document.getElementById('panelTxt'); pe.textContent = pt; pe.style.color = /NOTAUS|hängt/.test(pt) ? '#f87171' : '';
  const h = data.home || {};
  setHome('aussenTxt', h.aussen, ' °C', 0);
  setHome('rf1Val', h.raum_ist, ' °C', 1);
  setHome('sollVal', h.raum_soll, '', 1);
  setHome('houseVl', h.vl_ist, ' °C', 0);
  setHome('houseKwl', h.kwl_mod, ' %', 0);
  setHome('wwVal', h.ww_ist, ' °C', 0);
  setHome('kwlVal', h.kwl_mod, ' %', 0);
  setHome('kwlHum', h.feuchte, ' %', 0);
  document.getElementById('hkNameLbl').textContent = h.hk_name || 'Heizkreis 1';
  document.getElementById('modeLbl').textContent = h.mode_text || '—';
 }).catch(() => setOffline(true));
 if(document.getElementById('viewService').style.display === 'flex') loadKat();
}

setInterval(poll, 5000);
poll();
renderMenuGrid();
fitScreen();
setTimeout(fitScreen, 300);
</script>
"""
