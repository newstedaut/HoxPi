#!/usr/bin/env python3
"""HoxPi MQTT-Bridge fuer Home Assistant.

- Liest kuratierte Register der Modbus-Bridge (127.0.0.1:502) und published sie
  nach MQTT inkl. Home-Assistant-Auto-Discovery (Sensoren).
- STEUERUNG: fuer freigegebene (Whitelist-)Register werden zusaetzlich
  number-/select-Entities mit command_topic angelegt. HA schreibt darauf,
  der Dienst uebersetzt zum Modbus-FC6-Write in die Bridge. Die Bridge prueft
  weiterhin Whitelist + Wertebereich + Rate-Limit.
"""
import json, socket, struct, time, threading
import paho.mqtt.client as mqtt

MB_HOST, MB_PORT = "127.0.0.1", 502
INTERVAL = 30
BASE = "hoval"
AVAIL = BASE + "/bridge/status"
WHITELIST_PATH = "/home/admin/hoval-bridge/whitelist.json"
REGMAP = {r["reg"]: r for r in json.load(open("/home/admin/hoval-bridge/registers.json", encoding="utf-8"))}

# ---------- Enum-Texte ----------
HK_STATUS = {0:"Abgeschaltet",1:"Heizen Normal",2:"Heizen Komfort",3:"Heizen Spar",4:"Frostschutz",
             7:"Ferien",8:"Party",9:"Kuehlen Normal",10:"Kuehlen Komfort",11:"Kuehlen Spar",
             12:"Stoerung",13:"Handbetrieb",14:"Schutz Kuehlen",22:"Kuehlen extern",23:"Heizen extern",
             26:"SmartGrid Vorzug"}
DHW_STATUS = {0:"Aus",1:"Laden Normal",2:"Laden Komfort",5:"Stoerung",6:"Zapfung",8:"Laden reduziert",
              12:"SmartGrid Vorzug",13:"SmartGrid Zwang"}
SG_STATUS = {0:"Normal",1:"Vorzugbetrieb",2:"Gesperrt",3:"Abnahmezwang",255:"inaktiv"}
WEZ_STATUS = {0:"Aus",1:"Heizen",2:"Kuehlen",4:"Warmwasser",16:"Wiedereinschaltsperre",17:"Verriegelung (Stoerung)",
              51:"Startvorbereitung",98:"Startphase (W:61)"}
# Register 1534: 255 = kein Fehler, sonst gepackt code+1 = Klasse*64+Nr (Klasse 1=W 2=B 3=E). Texte: eigene Analyse.
FEHLER_TXT = {"B:02":"Niederdruck","E:02":"Niederdruck, verriegelt","W:58":"E-Stab nach Verriegelung",
              "W:61":"Startphase-Sonderzustand","B:63":"Service-/Parametereingriff","E:31":"Verriegelung nach Eingriff"}
class _FehlerEnum(dict):
    def get(self, raw, default=None):
        raw = int(raw)
        if raw == 255: return "OK"
        if raw == 0: return "kein Wert"  # FA antwortet nicht (z. B. nach Netz-Ein), keine Stoerung
        c = raw + 1; code = "%s:%02d" % ("IWBE"[(c >> 6) & 3], c & 63)
        return code + (" " + FEHLER_TXT[code] if code in FEHLER_TXT else "")
FEHLER_ENUM = _FehlerEnum()
# Schreibbare LIST-Register (Enum-Maps)
BW_HK  = {0:"Standby",1:"Woche 1",2:"Woche 2",4:"Konstant",5:"Sparbetrieb",7:"Hand Heizen",8:"Hand Kuehlen"}
BW_WW  = {0:"Standby",1:"Woche 1",2:"Woche 2",4:"Konstant",6:"Sparbetrieb"}
BW_WEZ = {0:"Aus",1:"Automatik",4:"Manuell Heizen",5:"Manuell Kuehlen"}
SG_BUS = {0:"Normal",1:"Vorzugbetrieb",2:"Gesperrt",3:"Abnahmezwang"}
SG_TRG = {0:"Aus",1:"Eingangskontakte",2:"Systembus",3:"Leistung gedaempft"}

# ---------- Sensoren (read-only) ----------
# key, reg, name, unit, device_class, enum
SENSORS = [
    ("aussentemp",   1477, "Aussentemperatur",     "°C", "temperature", None),
    ("vorlauf",     18760, "Vorlauf",              "°C", "temperature", None),
    ("ruecklauf",    1535, "Ruecklauf",            "°C", "temperature", None),
    ("ww_ist",       1500, "Warmwasser Ist",       "°C", "temperature", None),
    ("raum_ist",     1510, "Raum Ist HK1",         "°C", "temperature", None),
    ("el_leistung", 25611, "El. Leistung",         "kW", "power",       None),
    ("heizleistung",25612, "Heizleistung",         "kW", "power",       None),
    ("modulation",  18726, "Modulation",           "%",  None,          None),
    ("status_hk1",   1501, "Status HK1",           None, None,          HK_STATUS),
    ("status_hk2",   1502, "Status HK2",           None, None,          HK_STATUS),
    ("status_ww",    1504, "Status WW-Regelung",   None, None,          DHW_STATUS),
    ("sg_status",   27537, "SmartGrid Status",     None, None,          SG_STATUS),
    ("kuehlventil", 19870, "Kuehlventil UKA",      None, None,          {0:"zu",1:"offen"}),
    ("jaz",         27467, "Jahresarbeitszahl",    None, None,          None),
    ("leistungssollwert", 18767, "Leistungs-Sollwert WEZ", "%", None, None),
    ("anforderung",       18768, "Anforderung WEZ",       None, None, {0: "nein", 100: "ja"}),
    ("status_wez",         1539, "Status WEZ",            None, None, WEZ_STATUS),
    ("fehlercode",         1534, "Fehlercode WEZ",        None, None, FEHLER_ENUM),
]
# 18767: Leistungs-Sollwert des Waermeerzeugers, S16 /10, -100..+100 %.
#   -100.0 = kein Bedarf (unterer Anschlag des Reglerausgangs, gueltiger Wert)
#   -127.0 = UNGUELTIG -> wird unten als "unknown" publiziert, nie als Zahl.
# 18768: binaeres Anforderungs-Flag (nur 0 oder 100), trotz Hoval-Name "0-100%".
INVALID_SETPOINT = -127.0
COP_HI, COP_LO = 31667, 31668

# ---------- Verfuegbarkeits-Alarm (Backlog #9) ----------
# "stale" = seit STALE_MIN Minuten kein erfolgreicher Modbus-Read von der Bridge
#   ODER can0 rx_packets seit STALE_MIN Minuten unveraendert (Regler/CAN tot ->
#   die Bridge antwortet weiter, liefert aber eingefrorene Werte).
STALE_MIN_DEFAULT = 10
CAN_RX_STAT = "/sys/class/net/can0/statistics/rx_packets"
_stale = {"last_ok": time.time(), "can_rx": -1, "can_t": time.time(), "state": None}
def _can_rx():
    try: return int(open(CAN_RX_STAT).read().strip())
    except Exception: return None
def stale_check(c, stale_min):
    now = time.time()
    rx = _can_rx()
    if rx is not None and rx != _stale["can_rx"]:
        _stale["can_rx"] = rx; _stale["can_t"] = now
    age_mb  = now - _stale["last_ok"]
    age_can = now - _stale["can_t"]
    lim = stale_min * 60
    reasons = []
    if age_mb  > lim: reasons.append("modbus")
    if age_can > lim: reasons.append("can0")
    if rx is None:    reasons.append("can0-fehlt")
    on = bool(reasons)
    attr = {"age_s": int(max(age_mb, age_can)), "modbus_age_s": int(age_mb), "can_age_s": int(age_can),
            "can_rx": rx, "reason": ",".join(reasons) or "ok", "stale_min": stale_min,
            "last_ok": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(_stale["last_ok"]))}
    c.publish(f"{BASE}/stale/state", "ON" if on else "OFF", retain=True)
    c.publish(f"{BASE}/stale/attr", json.dumps(attr), retain=True)
    if on != _stale["state"]:
        _stale["state"] = on
        print(time.strftime("%H:%M:%S"), "stale ->", "ON" if on else "OFF", attr["reason"], flush=True)

# ---------- Steuerbare Entities ----------
# key, reg, name, art ("number"|"select"), enum-map (bei select)
CONTROLS = [
    ("set_ww_normal",     1497, "WW Normal-Soll",          "number", None),
    ("set_ww_eco",        1498, "WW Eco-Soll",             "number", None),
    ("set_raum_normal",   1481, "Raumtemp Normal HK1",     "number", None),
    ("set_raum_eco",      1482, "Raumtemp Eco HK1",        "number", None),
    ("set_bw_hk1",        1478, "Betriebswahl HK1",        "select", BW_HK),
    ("set_bw_hk2",        1479, "Betriebswahl HK2",        "select", BW_HK),
    ("set_bw_ww",         1496, "Betriebswahl Warmwasser", "select", BW_WW),
    ("set_bw_wez",        1561, "Betriebswahl Waermeerzeuger", "select", BW_WEZ),
    ("set_raumist_hk1",   1510, "Raum-Ist Einspeisung HK1","number", None),
    ("set_konst_kk_hk1",  19482,"Konst-Anford. Kuehlen HK1","number", None),
    ("set_sg_off_ww",     27509,"SG-Offset Warmwasser",    "number", None),
    ("set_sg_off_hk1",    27528,"SG-Offset Raum HK1 (Heizen)","number", None),
    ("set_sg_off_kk1",    27531,"SG-Offset Raum HK1 (Kuehlen)","number", None),
    ("set_sg_off_puffer", 28839,"SG-Offset Heizpuffer",    "number", None),
    ("set_sg_bus",        27545,"SmartGrid Zustand (Bus)", "select", SG_BUS),
    ("set_sg_trigger",    27546,"SmartGrid Ausloeser",     "select", SG_TRG),
]
CTRL_BY_KEY = {c[0]: c for c in CONTROLS}

# ---------- Modbus (persistente Verbindung + Lock) ----------
_tid = [0]
_conn = {"sock": None}
_lock = threading.Lock()
def _sock():
    if _conn["sock"] is None:
        s = socket.create_connection((MB_HOST, MB_PORT), 3); s.settimeout(3)
        _conn["sock"] = s
    return _conn["sock"]
def _drop():
    try: _conn["sock"].close()
    except Exception: pass
    _conn["sock"] = None
def _mb(fc, addr, val_or_words):
    with _lock:
        _tid[0] = (_tid[0] + 1) & 0xFFFF
        for _ in range(2):
            try:
                s = _sock()
                s.sendall(struct.pack(">HHHBBHH", _tid[0], 0, 6, 1, fc, addr, val_or_words))
                r = s.recv(260)
                if not r or (r[7] & 0x80): return None
                if fc == 3:
                    return [struct.unpack(">H", r[9+2*i:11+2*i])[0] for i in range(val_or_words)]
                return True
            except Exception:
                _drop()
        return None
def mb_read(addr, words=1): return _mb(3, addr, words)
def mb_write(addr, value):  return _mb(6, addr, value & 0xFFFF) is not None

def _dec(reg): return int(REGMAP.get(reg, {}).get("decimal") or 0)
def scaled(reg, raw):
    r = REGMAP.get(reg, {}); t = (r.get("type") or "").upper(); v = raw
    if t in ("S16","S8") and v > 32767: v -= 65536
    d = _dec(reg)
    return round(v / (10 ** d), d) if d else v
def unscale(reg, value):
    return int(round(float(value) * (10 ** _dec(reg)))) & 0xFFFF

def whitelist():
    try: return set(json.load(open(WHITELIST_PATH, encoding="utf-8")).get("allowed", []))
    except Exception: return set()

DEVICE = {"identifiers": ["hoxpi"], "name": "HoxPi Waermepumpe",
          "model": "CAN-Modbus-Bridge fuer Hoval(R) TTE", "manufacturer": "HoxPi"}

def num_meta(reg):
    """min/max/step/unit fuer number aus REGMAP (Rohwerte -> skaliert)."""
    r = REGMAP.get(reg, {}); d = _dec(reg)
    mn, mx = r.get("min"), r.get("max")
    sc = 10 ** d
    lo = (mn / sc) if isinstance(mn, (int, float)) and mn is not None else 0
    hi = (mx / sc) if isinstance(mx, (int, float)) and mx not in (None, 0) else 90
    if hi <= lo: hi = lo + 90
    unit = (r.get("unit") or "").strip()
    step = 0.5 if d else 1
    return lo, hi, step, unit

def discovery(c, wl):
    for key, reg, name, unit, dc, enum in SENSORS + [("cop", COP_HI, "COP aktuell", None, None, None)]:
        cfg = {"name": name, "unique_id": f"hoxpi_{key}", "state_topic": f"{BASE}/{key}/state",
               "availability_topic": AVAIL, "device": DEVICE}
        if unit: cfg["unit_of_measurement"] = unit
        if dc: cfg["device_class"] = dc; cfg["state_class"] = "measurement"
        c.publish(f"homeassistant/sensor/hoxpi/{key}/config", json.dumps(cfg), retain=True)
    # Verfuegbarkeits-Alarm: bewusst OHNE availability_topic, damit HA ihn auch zeigt,
    # wenn die Bridge steht (der MQTT-Dienst selbst lebt ja noch).
    c.publish("homeassistant/binary_sensor/hoxpi/stale/config", json.dumps({
        "name": "HoxPi Daten veraltet", "unique_id": "hoxpi_stale", "device_class": "problem",
        "state_topic": f"{BASE}/stale/state", "json_attributes_topic": f"{BASE}/stale/attr",
        "device": DEVICE}), retain=True)
    for key, reg, name, art, enum in CONTROLS:
        topic = f"homeassistant/{art}/hoxpi/{key}/config"
        if reg not in wl:
            c.publish(topic, "", retain=True)  # entfernen falls nicht (mehr) freigegeben
            continue
        cfg = {"name": name, "unique_id": f"hoxpi_{key}",
               "state_topic": f"{BASE}/{key}/state", "command_topic": f"{BASE}/{key}/set",
               "availability_topic": AVAIL, "device": DEVICE}
        if art == "number":
            lo, hi, step, unit = num_meta(reg)
            cfg.update({"min": lo, "max": hi, "step": step, "mode": "box"})
            if unit: cfg["unit_of_measurement"] = unit
        elif art == "select":
            cfg["options"] = list(enum.values())
        c.publish(topic, json.dumps(cfg), retain=True)

def on_message(c, userdata, msg):
    parts = msg.topic.split("/")
    if len(parts) != 3 or parts[2] != "set": return
    ctrl = CTRL_BY_KEY.get(parts[1])
    if not ctrl: return
    _, reg, name, art, enum = ctrl
    if reg not in whitelist(): return
    payload = msg.payload.decode().strip()
    try:
        if art == "select":
            rev = {v: k for k, v in enum.items()}
            if payload not in rev: return
            raw = rev[payload]
        else:
            raw = unscale(reg, payload)
        mb_write(reg, raw)
    except Exception:
        pass

def on_connect(c, userdata, flags, rc, props=None):
    # Bei jedem (Re)Connect: Discovery + Subscribe erneuern (robust gegen Reconnects)
    discovery(c, whitelist())
    c.subscribe(f"{BASE}/+/set")
    c.publish(AVAIL, "online", retain=True)

def client_new():
    try:
        c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="hoxpi-pub")
    except Exception:
        c = mqtt.Client(client_id="hoxpi-pub")
    c.will_set(AVAIL, "offline", retain=True)
    c.on_message = on_message
    c.on_connect = on_connect
    c.connect("127.0.0.1", 1883, 60)
    c.loop_start()
    return c

def main():
    c = client_new()
    last_wl = whitelist()
    while True:
        try: _f = json.load(open("/home/admin/hoxpi-features.json"))
        except Exception: _f = {}
        if not _f.get("mqtt_ha", {}).get("enabled", True):
            c.publish(AVAIL, "offline", retain=True)
            for _k,_r,_n,_u,_dc,_e in SENSORS + [("cop",COP_HI,"",None,None,None)]:
                c.publish(f"homeassistant/sensor/hoxpi/{_k}/config", "", retain=True)
            for _k,_r,_n,_a,_e in CONTROLS:
                c.publish(f"homeassistant/{_a}/hoxpi/{_k}/config", "", retain=True)
            c.publish("homeassistant/binary_sensor/hoxpi/stale/config", "", retain=True)
            main._was_off = True
            time.sleep(INTERVAL); continue
        else:
            c.publish(AVAIL, "online", retain=True)
            if getattr(main, "_was_off", False):
                discovery(c, whitelist()); main._was_off = False
        wl = whitelist()
        if wl != last_wl:
            discovery(c, wl); last_wl = wl
        for key, reg, name, unit, dc, enum in SENSORS:
            try:
                w = mb_read(reg)
                if w is None: continue
                if reg == 1535 and w[0] == 0:  # FA-Ruecklauf nach Netz-Ein stumm (0 = kein Wert) -> WP-Ruecklauf 60-7-258 (S32 31894/31895)
                    hl = mb_read(31894, 2)
                    if not hl or len(hl) < 2: continue
                    _r = (hl[0] << 16) | hl[1]
                    if _r in (0xFFFFFFFF, 0x80000000): continue
                    if _r > 0x7FFFFFFF: _r -= 0x100000000
                    if not -500 <= _r <= 1500: continue
                    w = [_r & 0xFFFF]
                _stale["last_ok"] = time.time()
                v = scaled(reg, w[0])
                if enum is not None:
                    c.publish(f"{BASE}/{key}/state", enum.get(int(v), str(v)), retain=True)
                    c.publish(f"{BASE}/{key}/raw", int(v), retain=True)
                elif reg == 18767 and float(v) == INVALID_SETPOINT:
                    # Hoval meldet -127.0 = kein gueltiger Sollwert.
                    c.publish(f"{BASE}/{key}/state", "unknown", retain=True)
                else:
                    c.publish(f"{BASE}/{key}/state", v, retain=True)
            except Exception:
                pass
        try:
            hl = mb_read(COP_HI, 2)
            if hl:
                _cop = ((hl[0] << 16) | hl[1]) / 10
                try: _copf = json.load(open("/home/admin/hoxpi-features.json")).get("cop_filter",{}).get("enabled",True)
                except Exception: _copf = True
                if (not _copf) or (0 <= _cop <= 20):  # COP-Plausibilitaet
                    c.publish(f"{BASE}/cop/state", _cop, retain=True)
        except Exception:
            pass
        for key, reg, name, art, enum in CONTROLS:
            if reg not in wl: continue
            try:
                w = mb_read(reg)
                if w is None: continue
                if art == "select":
                    c.publish(f"{BASE}/{key}/state", enum.get(int(scaled(reg, w[0])), ""), retain=True)
                else:
                    c.publish(f"{BASE}/{key}/state", scaled(reg, w[0]), retain=True)
            except Exception:
                pass
        try:
            stale_check(c, int(_f.get("mqtt_ha", {}).get("stale_min", STALE_MIN_DEFAULT)))
        except Exception as e:
            print("stale_check:", e, flush=True)
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
