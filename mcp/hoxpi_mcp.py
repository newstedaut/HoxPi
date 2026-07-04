#!/usr/bin/env python3
"""HoxPi MCP-Server - KI-Schnittstelle für die Hoval-Anlage.

Erlaubt KI-Assistenten (Claude, u. a.) die Anlage zu inspizieren, Werte zu
erklären, Historie auszuwerten und - falls freigeschaltet - zu steuern.

Transport: Streamable HTTP auf Port 8808 -> http://<pi-ip>:8808/mcp
Schreiben: standardmäßig AUS (config.json: {"enable_write": true} zum Aktivieren).
Jeder Write läuft zusätzlich durch die Bridge-Sicherungen (Whitelist,
Wertebereich, Rate-Limit, Kalt-Cache).
"""
import json, socket, struct, subprocess, urllib.request, urllib.parse
import time as _time
from mcp.server.fastmcp import FastMCP

BRIDGE_DIR = "/home/admin/hoval-bridge"
CONFIG_PATH = "/home/admin/hoxpi-mcp/config.json"
PROM_URL = "http://127.0.0.1:9090"

def _config():
    try:
        return json.load(open(CONFIG_PATH, encoding="utf-8"))
    except Exception:
        return {}

cfg = _config()
mcp = FastMCP("HoxPi", host="0.0.0.0", port=int(cfg.get("port", 8808)))

# ---------- Anlagen-Daten ----------
_cache = {}
def _regmap():
    if "regs" not in _cache:
        rows = json.load(open(f"{BRIDGE_DIR}/registers.json", encoding="utf-8"))
        _cache["regs"] = {r["reg"]: r for r in rows}
    return _cache["regs"]

def _texts():
    if "texts" not in _cache:
        try:
            _cache["texts"] = json.load(open(f"{BRIDGE_DIR}/reg_texts.json", encoding="utf-8"))
        except Exception:
            _cache["texts"] = {}
    return _cache["texts"]

def _whitelist():
    try:
        return set(json.load(open(f"{BRIDGE_DIR}/whitelist.json", encoding="utf-8")).get("allowed", []))
    except Exception:
        return set()

ST_HC = {0: "Abgeschaltet", 1: "Heizen normal", 2: "Heizen Komfort", 3: "Heizen Eco",
         4: "Frostschutz", 7: "Ferien", 8: "Party", 9: "Kühlen normal", 10: "Kühlen Komfort",
         11: "Kühlen Eco", 12: "STÖRUNG", 13: "Handbetrieb", 14: "Schutz-Kühlbetrieb",
         22: "Kühlen extern/konstant", 23: "Heizen extern/konstant", 26: "SmartGrid-Vorzug"}
ST_DHW = {0: "Aus", 1: "Laden normal", 2: "Laden Komfort", 5: "STÖRUNG", 6: "Zapfung",
          8: "Laden reduziert", 12: "SmartGrid-Vorzug", 13: "SmartGrid-Zwang"}
ST_HP = {0: "Aus", 1: "Heizen", 2: "Aktiv-Kühlen", 3: "Sperre", 4: "Warmwasser-Laden",
         5: "Frostschutz", 8: "Abtauen", 9: "Passiv-Kühlen", 11: "HOCHDRUCK-STÖRUNG",
         12: "NIEDERDRUCK-STÖRUNG", 16: "Wiedereinschaltverzögerung", 17: "EVU-/EW-Sperre",
         18: "Vorlaufzeit", 19: "Nachlaufzeit", 44: "MOP", 49: "Abtauung erfolglos",
         51: "Kondensatorpumpe", 55: "INVERTER-STÖRUNG", 97: "Ölvorwärmung", 98: "Kaltstart"}
ST_SG = {0: "Normal", 1: "Vorzugbetrieb", 2: "Gesperrt", 3: "Abnahmezwang", 255: "inaktiv"}

_tid = [0]
def _rd(addr, words=1):
    _tid[0] += 1
    try:
        s = socket.create_connection(("127.0.0.1", 502), 3); s.settimeout(3)
        s.sendall(struct.pack(">HHHBBHH", _tid[0], 0, 6, 1, 3, addr, words))
        r = s.recv(260); s.close()
        if r[7] & 0x80:
            return None
        return [struct.unpack(">H", r[9 + 2 * i:11 + 2 * i])[0] for i in range(words)]
    except Exception:
        return None

def _wr(addr, value):
    _tid[0] += 1
    s = socket.create_connection(("127.0.0.1", 502), 3); s.settimeout(3)
    s.sendall(struct.pack(">HHHBBHH", _tid[0], 0, 6, 1, 6, addr, value & 0xFFFF))
    r = s.recv(260); s.close()
    return not (r[7] & 0x80)

def _scaled(reg, raw=None):
    r = _regmap().get(reg)
    if r is None:
        return None, None
    if raw is None:
        w = _rd(reg)
        if not w:
            return None, r
        raw = w[0]
    if raw in (0x8000, 0xFFFF):
        return None, r
    t = (r.get("type") or "").upper()
    v = raw
    if t == "S16" and raw > 32767:
        v = raw - 65536
    elif t == "S8" and (raw & 0xFF) > 127:
        v = (raw & 0xFF) - 256
    dec = r.get("decimal") or 0
    if dec:
        v = round(v / (10 ** dec), dec)
    return v, r

def _r32(reg, dec=0):
    w = _rd(reg, 2)
    if not w or len(w) < 2:
        return None
    v = (w[0] << 16) | w[1]
    return round(v / (10 ** dec), dec) if dec else v

def _name(reg):
    t = _texts().get(str(reg), {})
    return t.get("nd") or _regmap().get(reg, {}).get("name", "")

# ---------- Tools ----------
@mcp.tool()
def get_status() -> dict:
    """Kuratierter Live-Zustand der Anlage: Temperaturen, Leistung, COP,
    Betriebszustände (Klartext), Smart Grid, Warmwasser. Erster Anlaufpunkt."""
    def g(reg):
        v, _ = _scaled(reg)
        return v
    hc1, hc2, ww, hp = _rd(1501), _rd(1502), _rd(1504), _rd(18723)
    sg = _rd(27537)
    return {
        "aussentemperatur_c": g(1477),
        "vorlauf_c": g(18760), "ruecklauf_c": g(1535),
        "warmwasser_ist_c": g(1500), "warmwasser_soll_c": g(1499),
        "raumtemperatur_c": g(1510),
        "wasserdruck_bar": g(18738),
        "leistung_elektrisch_kw": g(25611), "leistung_thermisch_kw": g(25612),
        "modulation_prozent": g(18726),
        "cop_aktuell": _r32(31667, 1),
        "wp_detailstatus": {"code": (hp or [None])[0] and round((hp[0]) / 10),
                            "text": ST_HP.get(hp and round(hp[0] / 10), "?") if hp else "?"},
        "heizkreis_1": {"code": hc1 and hc1[0], "text": ST_HC.get(hc1 and hc1[0], "?")},
        "heizkreis_2": {"code": hc2 and hc2[0], "text": ST_HC.get(hc2 and hc2[0], "?")},
        "warmwasser_status": {"code": ww and ww[0], "text": ST_DHW.get(ww and ww[0], "?")},
        "smart_grid": {"code": sg and sg[0], "text": ST_SG.get(sg and sg[0], "?")},
        "sg_offset_ww_k": g(27509), "sg_offset_raum_hk1_k": g(27528),
        "kuehlventil_uka": (_rd(19870) or [None])[0],
        "fehlercode": (_rd(1534) or [None])[0],
    }

@mcp.tool()
def diagnose() -> dict:
    """Gesundheits-Check: Dienste, Störcodes, Plausibilität (Wasserdruck etc.).
    Liefert eine Liste konkreter Hinweise."""
    dienste = {}
    for s in ("hoval-bridge", "hoval-status", "hoval-exporter", "prometheus",
              "grafana-server", "hoval-mqtt", "mosquitto"):
        try:
            dienste[s] = subprocess.run(["systemctl", "is-active", s],
                                        capture_output=True, text=True, timeout=5).stdout.strip()
        except Exception:
            dienste[s] = "?"
    st = get_status()
    hinweise = []
    if dienste.get("hoval-bridge") != "active":
        hinweise.append("KRITISCH: Bridge läuft nicht - keine Verbindung zur Wärmepumpe!")
    if st.get("fehlercode") not in (0, 255, None):
        hinweise.append(f"Fehlercode vom Automaten: {st['fehlercode']} (Hoval-Display prüfen)")
    code = (st.get("wp_detailstatus") or {}).get("code")
    if code in (11, 12, 55, 49):
        hinweise.append(f"WP-Störung aktiv: {st['wp_detailstatus']['text']}")
    druck = st.get("wasserdruck_bar")
    if druck is not None and druck < 1.0:
        hinweise.append(f"Wasserdruck niedrig ({druck} bar) - Anlage nachfüllen")
    if (st.get("heizkreis_1") or {}).get("code") == 12 or (st.get("heizkreis_2") or {}).get("code") == 12:
        hinweise.append("Heizkreis meldet Störung")
    if not hinweise:
        hinweise.append("Keine Auffälligkeiten gefunden.")
    return {"dienste": dienste, "hinweise": hinweise, "status": st}

@mcp.tool()
def read_register(reg: int) -> dict:
    """Ein Register lesen: Rohwert, skalierter Wert, Name (DE/EN), Beschreibung,
    Typ, Einheit, ob laut Katalog schreibbar und ob in der Schreib-Whitelist."""
    r = _regmap().get(reg)
    if r is None:
        return {"fehler": f"Register {reg} nicht in der Registerkarte (514 bekannte)"}
    w = _rd(reg)
    raw = w[0] if w else None
    v, _ = _scaled(reg, raw) if raw is not None else (None, r)
    t = _texts().get(str(reg), {})
    return {"reg": reg, "rohwert": raw, "wert": v, "einheit": r.get("unit") or "",
            "name_de": t.get("nd") or r.get("name"), "name_en": t.get("ne") or r.get("name"),
            "beschreibung_de": t.get("dd") or "", "beschreibung_en": t.get("ed") or "",
            "typ": r.get("type"), "dezimalstellen": r.get("decimal"),
            "katalog_schreibbar": str(r.get("writable")).lower() == "yes",
            "in_whitelist": reg in _whitelist()}

@mcp.tool()
def search_registers(query: str, limit: int = 20) -> list:
    """Register per Stichwort suchen (deutsch oder englisch, z. B. 'Warmwasser',
    'cooling', 'Offset'). Liefert Register mit Live-Wert."""
    q = query.lower()
    hits = []
    texts = _texts()
    wl = _whitelist()
    for reg, r in sorted(_regmap().items()):
        t = texts.get(str(reg), {})
        hay = " ".join([t.get("nd", ""), t.get("ne", ""), t.get("dd", ""),
                        t.get("ed", ""), r.get("name", "")]).lower()
        if q in hay:
            v, _ = _scaled(reg)
            hits.append({"reg": reg, "name_de": t.get("nd") or r.get("name"),
                         "wert": v, "einheit": r.get("unit") or "",
                         "schreibbar": str(r.get("writable")).lower() == "yes",
                         "in_whitelist": reg in wl})
            if len(hits) >= max(1, min(limit, 50)):
                break
    return hits

@mcp.tool()
def get_history(metric: str = "aussentemp_c", hours: float = 24) -> dict:
    """Zeitreihe aus Prometheus (falls Statistik aktiv). metric z. B.:
    aussentemp_c, vorlauf_c, ww_ist_c, p_el_kw, cop, hc1_status, sg_status,
    energie_el_mwh. 'list' zeigt alle verfügbaren Metriken."""
    try:
        if metric == "list":
            with urllib.request.urlopen(f"{PROM_URL}/api/v1/label/__name__/values", timeout=5) as f:
                names = json.load(f)["data"]
            return {"metriken": [n.replace("hoval_", "") for n in names if n.startswith("hoval_")]}
        name = metric if metric.startswith("hoval_") else f"hoval_{metric}"
        end = _time.time(); start = end - hours * 3600
        step = max(60, int(hours * 3600 / 300))
        q = urllib.parse.urlencode({"query": name, "start": start, "end": end, "step": step})
        with urllib.request.urlopen(f"{PROM_URL}/api/v1/query_range?{q}", timeout=10) as f:
            data = json.load(f)
        res = data.get("data", {}).get("result", [])
        if not res:
            return {"fehler": f"Keine Daten für '{name}'. Tipp: metric='list' zeigt alle Metriken."}
        pts = [{"zeit": _time.strftime("%Y-%m-%d %H:%M", _time.localtime(ts)), "wert": float(v)}
               for ts, v in res[0]["values"]]
        vals = [p["wert"] for p in pts]
        return {"metrik": name, "stunden": hours, "punkte": len(pts),
                "min": min(vals), "max": max(vals), "mittel": round(sum(vals) / len(vals), 2),
                "verlauf": pts}
    except Exception as e:
        return {"fehler": f"Prometheus nicht erreichbar ({e}) - ist die Statistik aktiviert?"}

@mcp.tool()
def get_whitelist() -> dict:
    """Aktuelle Schreib-Whitelist (Register, die Loxone/HA/KI schreiben dürfen)."""
    wl = sorted(_whitelist())
    return {"anzahl": len(wl),
            "register": [{"reg": r, "name": _name(r)} for r in wl],
            "schreiben_via_mcp": bool(_config().get("enable_write"))}

@mcp.tool()
def set_whitelist(reg: int, allow: bool, confirm: bool = False) -> dict:
    """Register zur Schreib-Whitelist hinzufügen/entfernen. Erfordert
    enable_write in der MCP-Config UND confirm=True."""
    if not _config().get("enable_write"):
        return {"fehler": "Schreiben via MCP ist deaktiviert (config.json: enable_write)"}
    if not confirm:
        return {"fehler": "Sicherheitsabfrage: mit confirm=True bestätigen",
                "vorschau": {"reg": reg, "name": _name(reg), "allow": allow}}
    r = _regmap().get(reg)
    if not r or str(r.get("writable")).lower() != "yes":
        return {"fehler": "Register ist laut Hoval-Katalog nicht schreibbar"}
    import tempfile, os
    p = f"{BRIDGE_DIR}/whitelist.json"
    wl = _whitelist()
    (wl.add(reg) if allow else wl.discard(reg))
    data = {"allowed": sorted(wl), "hinweis": "Verwaltet via Dashboard/MCP.",
            "geaendert": _time.strftime("%Y-%m-%dT%H:%M:%S")}
    fd, tmp = tempfile.mkstemp(dir=BRIDGE_DIR)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
    os.replace(tmp, p)
    return {"ok": True, "reg": reg, "allow": allow, "anzahl": len(wl)}

@mcp.tool()
def write_register(reg: int, value: int, confirm: bool = False) -> dict:
    """Rohwert in ein Register schreiben (z. B. 45.0 °C = 450 bei dec1!).
    Erfordert enable_write UND confirm=True UND Register in Whitelist.
    Die Bridge prüft zusätzlich Wertebereich, Rate-Limit und Kalt-Cache."""
    if not _config().get("enable_write"):
        return {"fehler": "Schreiben via MCP ist deaktiviert (config.json: enable_write)"}
    info = read_register(reg)
    if not confirm:
        return {"fehler": "Sicherheitsabfrage: mit confirm=True bestätigen",
                "vorschau": {"reg": reg, "name": info.get("name_de"),
                             "aktueller_rohwert": info.get("rohwert"), "neuer_rohwert": value}}
    if reg not in _whitelist():
        return {"fehler": "Register nicht in der Schreib-Whitelist (erst freigeben)"}
    ok = _wr(reg, value)
    _time.sleep(1)
    nach = read_register(reg)
    return {"ok": ok, "reg": reg, "geschrieben": value,
            "rohwert_nachher": nach.get("rohwert"),
            "hinweis": "Bridge kann Writes still ablehnen (Range/Rate/Cache) - Rohwert nachher prüfen"}

@mcp.tool()
def about() -> dict:
    """Anlagen- und Systemübersicht für den Einstieg: Was ist HoxPi, welche
    Geräte, wichtige Register, weitere Schnittstellen."""
    regs = _regmap()
    units = {}
    for r in regs.values():
        units[r["unit_name"]] = units.get(r["unit_name"], 0) + 1
    return {
        "system": "HoxPi - offenes Gateway für Hoval TopTronic E (Raspberry Pi + CAN)",
        "geraete": units,
        "register_gesamt": len(regs),
        "schnittstellen": {"modbus_tcp": ":502 (Loxone/HA)", "dashboard": ":80",
                           "prometheus_exporter": ":9101", "prometheus": ":9090",
                           "grafana": ":3000/d/hoxpi", "mcp": ":8808/mcp"},
        "wichtige_register": {
            "1477": "Außentemperatur", "1500": "Warmwasser Ist", "1497": "WW-Soll Normal",
            "1501/1502": "Status Heizkreis 1/2 (Enum)", "18723": "WP-Detailstatus (Enum)",
            "25611": "el. Leistung (dec2)", "27537": "Smart-Grid-Status",
            "27509": "SG-Offset WW (dec1)", "27510": "Regelstrategie"},
        "hinweis_schreiben": "Rohwerte! dec1 heißt Wert×10 (45.0°C = 450).",
        "projekt": "https://github.com/newstedaut/HoxPi",
    }

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
