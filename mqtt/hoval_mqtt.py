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
]
COP_HI, COP_LO = 31667, 31668

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
        wl = whitelist()
        if wl != last_wl:
            discovery(c, wl); last_wl = wl
        for key, reg, name, unit, dc, enum in SENSORS:
            try:
                w = mb_read(reg)
                if w is None: continue
                v = scaled(reg, w[0])
                if enum is not None:
                    c.publish(f"{BASE}/{key}/state", enum.get(int(v), str(v)), retain=True)
                    c.publish(f"{BASE}/{key}/raw", int(v), retain=True)
                else:
                    c.publish(f"{BASE}/{key}/state", v, retain=True)
            except Exception:
                pass
        try:
            hl = mb_read(COP_HI, 2)
            if hl: c.publish(f"{BASE}/cop/state", ((hl[0] << 16) | hl[1]) / 10, retain=True)
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
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
