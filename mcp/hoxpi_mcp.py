#!/usr/bin/env python3
"""HoxPi MCP-Server - KI-Schnittstelle für die Hoval-Anlage.

Erlaubt KI-Assistenten (Claude, u. a.) die Anlage zu inspizieren, Werte zu
erklären, Historie auszuwerten und - falls freigeschaltet - zu steuern.

Transport: Streamable HTTP auf Port 8808 -> http://<pi-ip>:8808/mcp
Schreiben: standardmäßig AUS (config.json: {"enable_write": true} zum Aktivieren)
und dann nur von den Adressen in "write_clients" (Standard 127.0.0.1), siehe Zugangsschutz.
Jeder Write läuft zusätzlich durch die Bridge-Sicherungen (Whitelist,
Wertebereich, Rate-Limit, Kalt-Cache).
"""
import json, socket, struct, subprocess, threading, urllib.request, urllib.parse
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
mcp = FastMCP("HoxPi", host=str(cfg.get("host", "0.0.0.0")), port=int(cfg.get("port", 8808)))

# ---------- Zugangsschutz (22.11.2026) ----------
# Der MCP-Server hat keine eigene Anmeldung. Ohne Schutz koennte jedes Geraet im
# LAN (und ueber DNS-Rebinding sogar eine Webseite im Browser eines LAN-PCs) die
# Schreib-Werkzeuge aufrufen, sobald enable_write an ist. Darum, alles in config.json:
#   "allowed_clients": ["192.168.1.0/24", "127.0.0.1"]  wer ueberhaupt verbinden darf (Standard: alle)
#   "write_clients":   ["192.168.1.50", "127.0.0.1"]    wer write_register/set_whitelist aufrufen darf
#                                                       (Standard: nur 127.0.0.1)
#   "token":           "lange-zufallszeichenkette"      optional; dann Pflicht fuer JEDE Anfrage
#                                                       (Header "Authorization: Bearer <token>")
#   "allowed_hosts":   ["hoxpi.local"]                  zusaetzliche Host-Namen (IP-Adressen und
#                                                       localhost sind immer erlaubt)
# Anfragen mit fremdem Host- oder Origin-Header (DNS-Rebinding, Browser) werden abgewiesen.
import ipaddress, hmac

WRITE_TOOLS = {"write_register", "set_whitelist"}

def _nets(lst, default):
    out = []
    for x in (lst if lst is not None else default):
        try:
            out.append(ipaddress.ip_network(str(x).strip(), strict=False))
        except ValueError:
            pass
    return out

def _ip_in(ip, nets):
    try:
        a = ipaddress.ip_address(ip)
    except ValueError:
        return False
    if a.version == 6 and a.ipv4_mapped:
        a = a.ipv4_mapped
    return any(a in n for n in nets)

def _host_ok(hostport, extra):
    h = (hostport or "").strip().lower()
    if h.startswith("["):
        h = h[1:].split("]", 1)[0]
    elif h.count(":") == 1:
        h = h.split(":", 1)[0]
    if not h:
        return False
    if h == "localhost" or h in extra:
        return True
    try:
        ipaddress.ip_address(h)
        return True
    except ValueError:
        return False

class AccessGuard:
    """Reine ASGI-Schicht vor dem MCP-App: Client-IP, Token, Host/Origin, Schreibrecht."""
    MAX_BODY = 1_000_000

    def __init__(self, app, conf):
        self.app = app
        self.allowed = _nets(conf.get("allowed_clients"), ["0.0.0.0/0", "::/0"])
        self.writers = _nets(conf.get("write_clients"), ["127.0.0.1/32", "::1/128"])
        self.token = str(conf.get("token") or "")
        self.hosts = {str(h).lower() for h in conf.get("allowed_hosts", [])}

    async def _deny(self, send, code, msg):
        body = json.dumps({"fehler": msg}).encode()
        await send({"type": "http.response.start", "status": code,
                    "headers": [(b"content-type", b"application/json"),
                                (b"content-length", str(len(body)).encode())]})
        await send({"type": "http.response.body", "body": body})

    async def __call__(self, scope, receive, send):
        if scope.get("type") != "http":
            return await self.app(scope, receive, send)
        client = (scope.get("client") or ("", 0))[0]
        hdr = {k.decode("latin-1").lower(): v.decode("latin-1") for k, v in scope.get("headers", [])}
        if not _ip_in(client, self.allowed):
            return await self._deny(send, 403, "Client nicht erlaubt (allowed_clients)")
        if not _host_ok(hdr.get("host", ""), self.hosts):
            return await self._deny(send, 403, "Host-Header nicht erlaubt (allowed_hosts)")
        origin = hdr.get("origin")
        if origin and not _host_ok(urllib.parse.urlsplit(origin).netloc, self.hosts):
            return await self._deny(send, 403, "Origin nicht erlaubt")
        if self.token:
            got = hdr.get("authorization", "")
            got = got[7:] if got.lower().startswith("bearer ") else hdr.get("x-hoxpi-token", "")
            if not hmac.compare_digest(got.encode(), self.token.encode()):
                return await self._deny(send, 401, "Token fehlt oder falsch")
        if scope.get("method") != "POST" or _ip_in(client, self.writers):
            return await self.app(scope, receive, send)
        # POST von einem Client ohne Schreibrecht: Body lesen und Schreib-Werkzeuge abweisen.
        chunks, size, more = [], 0, True
        while more:
            msg = await receive()
            if msg["type"] != "http.request":
                break
            chunks.append(msg.get("body", b""))
            size += len(chunks[-1])
            more = msg.get("more_body", False)
            if size > self.MAX_BODY:
                return await self._deny(send, 413, "Anfrage zu gross")
        body = b"".join(chunks)
        try:
            data = json.loads(body or b"null")
        except Exception:
            data = None
        for m in (data if isinstance(data, list) else [data]):
            if (isinstance(m, dict) and m.get("method") == "tools/call"
                    and (m.get("params") or {}).get("name") in WRITE_TOOLS):
                return await self._deny(send, 403, "Schreib-Werkzeuge von diesem Client nicht erlaubt (write_clients)")
        sent = [False]
        async def replay():
            if not sent[0]:
                sent[0] = True
                return {"type": "http.request", "body": body, "more_body": False}
            return await receive()
        return await self.app(scope, replay, send)

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
         4: "Frostschutz", 6: "Zwangsdrosselung (WW-Vorrang)", 7: "Ferien", 8: "Party", 9: "Kühlen normal", 10: "Kühlen Komfort",
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
_conn = {"sock": None}
_lock = threading.Lock()
def _sock():
    if _conn["sock"] is None:
        s = socket.create_connection(("127.0.0.1", 502), 3); s.settimeout(3)
        _conn["sock"] = s
    return _conn["sock"]
def _drop():
    try: _conn["sock"].close()
    except Exception: pass
    _conn["sock"] = None
def _mb(fc, addr, val_or_words):
    # Persistente Modbus-Verbindung wiederverwenden (verhindert TIME_WAIT-Anhaeufung).
    with _lock:
        _tid[0] = (_tid[0] + 1) & 0xFFFF
        for _ in range(2):
            try:
                s = _sock()
                s.sendall(struct.pack(">HHHBBHH", _tid[0], 0, 6, 1, fc, addr, val_or_words))
                r = s.recv(260)
                if not r or (r[7] & 0x80):
                    return None
                if fc == 3:
                    words = val_or_words
                    return [struct.unpack(">H", r[9 + 2 * i:11 + 2 * i])[0] for i in range(words)]
                return True
            except Exception:
                _drop()
        return None

def _rd(addr, words=1):
    return _mb(3, addr, words)

def _wr(addr, value):
    return _mb(6, addr, value & 0xFFFF) is not None

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

def _cop_gated():
    """COP 31667/68 (dec1); COP-Startfilter: in den ersten ~25 s eines Laufs liefert der FA Unsinn,
    weil Pel noch ~0 ist -> 0 zurueckgeben, solange 25611 < 0,5 kW."""
    cop = _r32(31667, 1)
    if not cop:  # 31667 (60-3-1054) antwortet nach Netz-Ein nicht mehr (F1, 04.09.) -> FA-COP dp 45 (27490, U8, 0,1)
        fa = _rd(27490)
        if fa and fa[0] not in (0x8000, 0xFFFF) and fa[0] <= 200:
            cop = round(fa[0] / 10.0, 1)
    pel = _rd(25611)
    if not pel or pel[0] in (0x8000, 0xFFFF) or pel[0] < 50:
        return 0.0
    return cop

def _name(reg):
    t = _texts().get(str(reg), {})
    return t.get("nd") or _regmap().get(reg, {}).get("name", "")

# ---------- Tools ----------
# --- R86 (12.09.2026): Datenfrische der von get_status benutzten Register ---
# Quelle ist bridge_state.json, das die Bridge alle 15 s atomar schreibt (HP-1).
#   never  = wird gepollt, hat seit dem Bridge-Start NIE geantwortet
#   frozen = hat geantwortet und ist dann verstummt (Alter > 4x Sweep)
_FRISCHE_REGS = {
    1477: "aussentemperatur_c", 18760: "vorlauf_c", 1535: "ruecklauf_c",
    1500: "warmwasser_ist_c", 1499: "warmwasser_soll_c", 1510: "raumtemperatur_c",
    1538: "wasserdruck_bar", 25611: "leistung_elektrisch_kw", 25612: "leistung_thermisch_kw",
    18726: "modulation_prozent", 27467: "jahresarbeitszahl", 18723: "wp_detailstatus",
    1501: "heizkreis_1", 1502: "heizkreis_2", 1504: "warmwasser_status",
    27537: "smart_grid", 27509: "sg_offset_ww_k", 27528: "sg_offset_raum_hk1_k",
    19870: "kuehlventil_uka", 1534: "fehlercode",
}

def _datenfrische():
    try:
        import json as _js, os as _o, time as _t   # bewusst lokal: keine Annahme ueber die Importe der Datei
        _sf = "/home/admin/hoval-bridge/bridge_state.json"
        if not _o.path.exists(_sf) or _t.time() - _o.path.getmtime(_sf) > 180:
            return {"bridge_zustand": "bridge_state.json fehlt oder ist veraltet",
                    "tote_felder": None, "verstummte_felder": None}
        _st = _js.load(open(_sf))
        _never = set(_st.get("never_regs") or [])
        _frozen = set(_st.get("frozen_regs") or [])
        _age = _st.get("reg_age_s") or {}
        tot = sorted({_FRISCHE_REGS[r]: r for r in _FRISCHE_REGS if r in _never}.items())
        ver = sorted({_FRISCHE_REGS[r]: r for r in _FRISCHE_REGS if r in _frozen}.items())
        alt = [(round(float(_age[str(r)]), 1), _FRISCHE_REGS[r])
               for r in _FRISCHE_REGS if str(r) in _age]
        alt.sort(reverse=True)
        out = {
            "bridge_zustand": "ok",
            "tote_felder": [{"feld": f, "reg": r} for f, r in tot] or None,
            "verstummte_felder": [{"feld": f, "reg": r} for f, r in ver] or None,
            "aeltester_wert": ({"feld": alt[0][1], "alter_s": alt[0][0]} if alt else None),
            "sweep_s": _st.get("sweep_s"),
        }
        if tot or ver:
            out["warnung"] = ("Diese Felder stammen aus Registern ohne aktuelle CAN-Antwort "
                              "und sind NICHT als Messwert zu verwenden: "
                              + ", ".join([f for f, _ in tot + ver]))
        return out
    except Exception as _e:
        return {"bridge_zustand": "nicht auswertbar: %s" % _e}

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
        "vorlauf_c": g(18760), "ruecklauf_c": _ruecklauf(),
        "warmwasser_ist_c": g(1500), "warmwasser_soll_c": g(1499),
        "raumtemperatur_c": g(1510),
        # 12.09.2026: 18738 antwortet nicht mehr (HP-1 "never") und lieferte 0
        # -> Dauerfehlalarm "Wasserdruck niedrig". 1538 = selbe Groesse auf fg60/fn254,
        # liefert 0x8000 (kein Sensor verdrahtet) -> _scaled() -> None -> Pruefung uebersprungen.
        "wasserdruck_bar": g(1538),
        "leistung_elektrisch_kw": g(25611), "leistung_thermisch_kw": g(25612),
        "modulation_prozent": g(18726),
        "cop_aktuell": _cop_gated(),  # nur im laufenden Betrieb ungleich 0; COP-Startfilter (Pel < 0,5 kW -> 0)
        "jahresarbeitszahl": (g(27467) or None),  # JAZ/SPF - verlässlicher Langzeit-Effizienzwert
        "wp_detailstatus": {"code": (hp or [None])[0],
                            "text": ST_HP.get(hp and hp[0], "?") if hp else "?"},
        "heizkreis_1": {"code": hc1 and hc1[0], "text": ST_HC.get(hc1 and hc1[0], "?")},
        "heizkreis_2": {"code": hc2 and hc2[0], "text": ST_HC.get(hc2 and hc2[0], "?")},
        "warmwasser_status": {"code": ww and ww[0], "text": ST_DHW.get(ww and ww[0], "?")},
        "smart_grid": {"code": sg and sg[0], "text": ST_SG.get(sg and sg[0], "?")},
        "sg_offset_ww_k": g(27509), "sg_offset_raum_hk1_k": g(27528),
        "kuehlventil_uka": (_rd(19870) or [None])[0],
        "fehlercode": (_rd(1534) or [None])[0],
        "fehlercode_hinweis": "0 = kein Wert (FA antwortet nicht, z. B. nach Netz-Ein), 255 = OK" if ((_rd(1534) or [255])[0] == 0) else None,
        "datenfrische": _datenfrische(),
    }

def _ruecklauf():
    # 1535 (fg60/fn254 dp29) antwortet nach Netz-Ein nicht (0 = kein Wert) -> Fallback fn=7 dp258 (31895, WP-Ruecklauf)
    v = g_rl = _scaled(1535)[0]
    if v in (None, 0, 0.0):
        v = _scaled(31895)[0]
    return v

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
    os.chmod(tmp, 0o644)  # welt-lesbar: MQTT-Dienst (User admin) muss die Liste lesen koennen
    os.replace(tmp, p)
    return {"ok": True, "reg": reg, "allow": allow, "anzahl": len(wl)}

# Register, die erfahrungsgemaess von aussen zurueckgesetzt werden.
# Quelle: systematische Messung 20.08.2026 (schreiben, alle 2 s nachlesen).
FREMDGESTEUERT = {
    1478:  "Hoval-Bedienteil (Betriebswahl Heizkreis 1) - Rueckschreiben nach ca. 6-8 s",
    23622: "Hoval-Bedienteil (Betriebswahl Lueftung)",
    23626: "Hoval-Bedienteil (Feuchte-Sollwert)",
    1510:  "zyklischer Schreiber (Loxone: Raumtemperatur-Einspeisung HK1)",
    27509: "zyklischer Schreiber (Loxone: SG-Offset Warmwasser)",
    27528: "zyklischer Schreiber (Loxone: SG-Offset Raum Heizen HK1)",
    27531: "zyklischer Schreiber (Loxone: SG-Offset Raum Kuehlen KK1)",
    29435: "zyklischer Schreiber (Loxone: Vorlaufminimaltemp. Kuehlen)",
    29436: "zyklischer Schreiber (Loxone: Vorlaufminimaltemp. Kuehlen)",
    23623: "zyklischer Schreiber (Loxone: Lueftungsmodulation)",
}

_write_checks = {}   # reg -> Ergebnis der Hintergrundpruefung


def _verify_later(reg, value, delay=15):
    """Prueft im Hintergrund, ob ein geschriebener Wert stehen bleibt."""
    def run():
        _time.sleep(delay)
        try:
            spaeter = read_register(reg).get("rohwert")
        except Exception as e:                      # pragma: no cover
            _write_checks[reg] = {"reg": reg, "fehler": str(e)}
            return
        _write_checks[reg] = {
            "reg": reg, "geschrieben": value, "rohwert_nach_%ds" % delay: spaeter,
            "haelt": spaeter == value,
            "geprueft_um": _time.strftime("%H:%M:%S"),
            "hinweis": ("Wert haelt." if spaeter == value else
                        "FREMDGESTEUERT: Wert wurde auf %s zurueckgesetzt. %s"
                        % (spaeter, FREMDGESTEUERT.get(reg, "Ursache: Bedienteil oder ein "
                           "zyklischer Schreiber (Loxone/HA).")))}
    threading.Thread(target=run, daemon=True).start()


def _bridge_ablehnung(reg, sekunden=5):
    """F173 (12.11.2026): Hat die Bridge den letzten Schreibversuch auf reg abgelehnt?
    Liest das Bridge-Journal der letzten Sekunden. Rueckgabe: Ablehnungsgrund als Text oder None."""
    try:
        import subprocess
        out = subprocess.run(["journalctl", "-u", "hoval-bridge", "--no-pager", "-o", "cat",
                              "--since", "-%ds" % sekunden], capture_output=True, text=True, timeout=5).stdout
        z = [l for l in out.splitlines() if ("reg %d " % reg) in l and ("SET reg" in l or "ABGELEHNT" in l)]
        if not z:
            return "kein SET im Bridge-Protokoll (Schreiben kam nicht am CAN an)"
        if "ABGELEHNT" in z[-1]:
            return z[-1].split("ABGELEHNT", 1)[1].strip()
        return None
    except Exception:
        return None


@mcp.tool()
def write_register(reg: int, value: int, confirm: bool = False) -> dict:
    """Rohwert in ein Register schreiben (z. B. 45.0 °C = 450 bei dec1!).
    Erfordert enable_write UND confirm=True UND Register in Whitelist.
    Die Bridge prueft zusaetzlich Wertebereich, Rate-Limit und Kalt-Cache.

    ACHTUNG: Ein Lesen direkt nach dem Schreiben beweist NICHT, dass der Wert
    bleibt. Manche Register werden vom Hoval-Bedienteil oder von einem zyklischen
    Schreiber (Loxone/HA) nach 6-10 s zurueckgesetzt. Dieses Tool startet deshalb
    eine Hintergrundpruefung; das Ergebnis nach ca. 15 s mit `schreib_pruefung(reg)`
    abholen."""
    if not _config().get("enable_write"):
        return {"fehler": "Schreiben via MCP ist deaktiviert (config.json: enable_write)"}
    info = read_register(reg)
    if not confirm:
        return {"fehler": "Sicherheitsabfrage: mit confirm=True bestätigen",
                "vorschau": {"reg": reg, "name": info.get("name_de"),
                             "aktueller_rohwert": info.get("rohwert"), "neuer_rohwert": value,
                             "warnung": FREMDGESTEUERT.get(reg)}}
    if reg not in _whitelist():
        return {"fehler": "Register nicht in der Schreib-Whitelist (erst freigeben)"}
    vorher = info.get("rohwert")
    ok = _wr(reg, value)
    _time.sleep(1)
    sofort = read_register(reg).get("rohwert")
    abgelehnt = _bridge_ablehnung(reg)

    res = {"ok": ok, "reg": reg, "name": info.get("name_de"),
           "rohwert_vorher": vorher, "geschrieben": value, "rohwert_sofort": sofort}

    if abgelehnt:
        res["bridge"] = "ABGELEHNT: " + abgelehnt
    if not ok or sofort != value or abgelehnt:
        res["haelt"] = False
        res["hinweis"] = ("Schreiben von der Bridge abgelehnt oder sofort verworfen "
                          "(Wertebereich, Rate-Limit oder Kalt-Cache-Schutz).")
        return res

    _write_checks.pop(reg, None)
    _verify_later(reg, value)
    res["haelt"] = None
    res["persistenz"] = "wird geprueft - in ca. 15 s schreib_pruefung(%d) aufrufen" % reg
    if reg in FREMDGESTEUERT:
        res["warnung"] = ("Dieses Register ist als fremdgesteuert bekannt: %s. "
                          "Der Wert wird sehr wahrscheinlich NICHT bleiben."
                          % FREMDGESTEUERT[reg])
    return res


@mcp.tool()
def schreiblast(minuten: int = 30, reg: int = 0) -> dict:
    """Wer beschreibt die Anlage, wie oft und mit welchem Wert?

    Wertet das Bridge-Protokoll aus (jeder Schreibvorgang wird dort mit Register,
    Name und Rohwert geloggt) und liefert eine Rangliste nach Haeufigkeit plus den
    ermittelten Wiederholtakt je Register.

    Damit laesst sich in Sekunden klaeren, warum ein geschriebener Wert nicht
    stehen bleibt: Meist schreibt ein zyklischer Aktor in Loxone oder Home
    Assistant denselben Datenpunkt im Sekundentakt zurueck. Ein Register, das hier
    auftaucht, ist per Modbus nicht dauerhaft von aussen setzbar, solange der
    Verursacher nicht abgestellt oder sein Wiederholintervall verlaengert wird.

    minuten: betrachteter Zeitraum (Default 30)
    reg:     optional auf ein einzelnes Register einschraenken
    """
    try:
        out = subprocess.run(
            ["journalctl", "-u", "hoval-bridge", "--since", "-%d min" % minuten,
             "--no-pager", "-o", "short-iso"],
            capture_output=True, text=True, timeout=30).stdout
    except Exception as e:
        return {"fehler": "Protokoll nicht lesbar: %s" % e}

    import re
    muster = re.compile(r"^(\S+).*SET reg (\d+) \((.*?)\) <- (-?\d+)")
    treffer = {}
    for zeile in out.splitlines():
        m = muster.search(zeile)
        if not m:
            continue
        zeit, r, name, wert = m.group(1), int(m.group(2)), m.group(3), int(m.group(4))
        if reg and r != reg:
            continue
        e = treffer.setdefault(r, {"reg": r, "name": name, "anzahl": 0,
                                   "werte": {}, "zeiten": []})
        e["anzahl"] += 1
        e["werte"][wert] = e["werte"].get(wert, 0) + 1
        e["zeiten"].append(zeit)

    liste = []
    for e in treffer.values():
        z = e.pop("zeiten")
        takt = None
        if len(z) > 2:
            try:
                from datetime import datetime
                ts = [datetime.fromisoformat(x.replace("Z", "+00:00")) for x in z]
                d = [(ts[i+1]-ts[i]).total_seconds() for i in range(len(ts)-1)]
                d = sorted(x for x in d if x > 0)
                if d:
                    takt = round(d[len(d)//2], 1)   # Median
            except Exception:
                pass
        e["takt_sekunden"] = takt
        e["name_de"] = _name(e["reg"]) or e["name"]
        liste.append(e)
    liste.sort(key=lambda x: -x["anzahl"])

    gesamt = sum(e["anzahl"] for e in liste)
    return {
        "zeitraum_minuten": minuten,
        "schreibvorgaenge_gesamt": gesamt,
        "pro_minute": round(gesamt / minuten, 1) if minuten else None,
        "register": liste,
        "hinweis": ("Register in dieser Liste werden zyklisch von aussen (Loxone/HA) "
                    "beschrieben und lassen sich per Modbus nicht dauerhaft aendern, "
                    "solange der Verursacher aktiv ist. Leere Liste = niemand schreibt."),
    }


@mcp.tool()
def schreib_pruefung(reg: int = 0) -> dict:
    """Ergebnis der Persistenzpruefung nach einem write_register abholen.
    Ohne Argument werden alle vorliegenden Pruefungen zurueckgegeben.
    Liegt noch nichts vor, ist die Pruefung noch nicht abgeschlossen (ca. 15 s warten)."""
    if reg:
        return _write_checks.get(reg, {
            "reg": reg,
            "status": "noch kein Ergebnis - Pruefung laeuft (ca. 15 s nach dem Schreiben) "
                      "oder es wurde nichts auf dieses Register geschrieben"})
    return {"pruefungen": list(_write_checks.values()),
            "bekannt_fremdgesteuert": FREMDGESTEUERT}

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
    import uvicorn
    uvicorn.run(AccessGuard(mcp.streamable_http_app(), cfg),
                host=mcp.settings.host, port=mcp.settings.port, log_level="info")
