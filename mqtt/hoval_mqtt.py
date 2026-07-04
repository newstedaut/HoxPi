#!/usr/bin/env python3
"""HoxPi MQTT-Publisher: liest kuratierte Register der Modbus-Bridge (127.0.0.1:502)
und published sie nach MQTT (localhost) inkl. Home-Assistant-Auto-Discovery."""
import json, socket, struct, time
import paho.mqtt.client as mqtt

MB_HOST, MB_PORT = "127.0.0.1", 502
INTERVAL = 30
BASE = "hoval"
AVAIL = BASE + "/bridge/status"

HK_STATUS = {0:"Abgeschaltet",1:"Heizen Normal",2:"Heizen Komfort",3:"Heizen Spar",4:"Frostschutz",
             7:"Ferien",8:"Party",9:"Kuehlen Normal",10:"Kuehlen Komfort",11:"Kuehlen Spar",
             12:"Stoerung",13:"Handbetrieb",14:"Schutz Kuehlen",22:"Kuehlen extern",23:"Heizen extern",
             26:"SmartGrid Vorzug"}
SG_STATUS = {0:"Normal",1:"Vorzugbetrieb",2:"Gesperrt",3:"Abnahmezwang",255:"inaktiv"}
WEZ_WAHL  = {0:"Aus",1:"Automatik",4:"Manuell Heizen",5:"Manuell Kuehlen"}

# key, reg, Anzeigename, unit, device_class, enum-map (None=numerisch)
SENSORS = [
    ("aussentemp",   1477, "Aussentemperatur",     "°C", "temperature", None),
    ("vorlauf",     18760, "Vorlauf",              "°C", "temperature", None),
    ("ruecklauf",    1535, "Ruecklauf",            "°C", "temperature", None),
    ("ww_ist",       1500, "Warmwasser Ist",       "°C", "temperature", None),
    ("ww_soll",      1499, "Warmwasser Soll",      "°C", "temperature", None),
    ("raum_ist",     1510, "Raum Ist HK1",         "°C", "temperature", None),
    ("el_leistung", 25611, "El. Leistung",         "kW", "power",       None),
    ("heizleistung",25612, "Heizleistung",         "kW", "power",       None),
    ("modulation",  18726, "Modulation",           "%",  None,          None),
    ("status_hk1",   1501, "Status HK1",           None, None,          HK_STATUS),
    ("status_hk2",   1502, "Status HK2",           None, None,          HK_STATUS),
    ("status_ww",    1504, "Status WW-Regelung",   None, None,          None),
    ("sg_status",   27537, "SmartGrid Status",     None, None,          SG_STATUS),
    ("betriebswahl", 1561, "Betriebswahl WEZ",     None, None,          WEZ_WAHL),
    ("kuehlventil", 19870, "Kuehlventil UKA",      None, None,          {0:"zu",1:"offen"}),
    ("konst_kuehl_hk1", 19482, "Konst-Anf. Kuehlen HK1", "°C", "temperature", None),
]
COP_HI, COP_LO = 31667, 31668

REGMAP = {r["reg"]: r for r in json.load(open("/home/admin/hoval-bridge/registers.json", encoding="utf-8"))}

_tid = 0
def mb_read(addr, words=1):
    global _tid; _tid += 1
    s = socket.create_connection((MB_HOST, MB_PORT), 3); s.settimeout(3)
    s.sendall(struct.pack(">HHHBBHH", _tid, 0, 6, 1, 3, addr, words))
    r = s.recv(260); s.close()
    if r[7] & 0x80: return None
    return [struct.unpack(">H", r[9+2*i:11+2*i])[0] for i in range(words)]

def scaled(reg, raw):
    r = REGMAP.get(reg, {})
    t = (r.get("type") or "").upper()
    v = raw
    if t in ("S16", "S8") and v > 32767: v -= 65536
    dec = int(r.get("decimal") or 0)
    return round(v / (10 ** dec), dec) if dec else v

def client_new():
    try:
        c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="hoxpi-pub")
    except Exception:
        c = mqtt.Client(client_id="hoxpi-pub")
    c.will_set(AVAIL, "offline", retain=True)
    c.connect("127.0.0.1", 1883, 60)
    c.loop_start()
    return c

DEVICE = {"identifiers": ["hoxpi"], "name": "HoxPi Waermepumpe",
          "model": "CAN-Modbus-Bridge fuer Hoval(R) TTE", "manufacturer": "HoxPi"}

def discovery(c):
    for key, reg, name, unit, dc, enum in SENSORS + [("cop", COP_HI, "COP aktuell", None, None, None)]:
        cfg = {"name": name, "unique_id": f"hoxpi_{key}",
               "state_topic": f"{BASE}/{key}/state",
               "availability_topic": AVAIL, "device": DEVICE}
        if unit: cfg["unit_of_measurement"] = unit
        if dc:
            cfg["device_class"] = dc
            cfg["state_class"] = "measurement"
        c.publish(f"homeassistant/sensor/hoxpi/{key}/config", json.dumps(cfg), retain=True)

def main():
    c = client_new()
    discovery(c)
    c.publish(AVAIL, "online", retain=True)
    while True:
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
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
