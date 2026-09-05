#!/usr/bin/env python3
"""Referenzpruefung fuer test_ha: out_ha_discovery.jsonl (Topic <TAB> JSON aus hoval_ha.c) gegen die
Tabellen in mqtt/hoval_mqtt.py. Die Python-Datei wird NICHT importiert (sie braucht paho + Modbus),
sondern per ast gelesen: SENSORS, CONTROLS, die Enum-Dicts, BASE/AVAIL/DEVICE.

Geprueft je Entity: Topic, name, unique_id, state_topic, command_topic, availability_topic,
unit_of_measurement, device_class/state_class, options (select, Reihenfolge), device-Block.
number-Grenzen (min/max/step) kommen aus registers.json und werden nur auf Plausibilitaet geprueft
(min < max, step 0.5/1), weil dem Host-Test die volle Tabelle fehlen darf.
Entities, deren Register in der C-Tabelle fehlen, duerfen fehlen (Beispieltabelle); mit der vollen
Tabelle muessen alle da sein (--full)."""
import ast, json, sys

src = sys.argv[1] if len(sys.argv) > 1 else "../../mqtt/hoval_mqtt.py"
full = "--full" in sys.argv
tree = ast.parse(open(src, encoding="utf-8").read())
ns = {"FEHLER_ENUM": None}          # Klasseninstanz in hoval_mqtt.py, hier nur Platzhalter
for node in tree.body:                     # nur Zuweisungen von Literalen/Dicts auswerten
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        try: ns[node.targets[0].id] = ast.literal_eval(node.value)
        except Exception:
            # SENSORS/CONTROLS enthalten Namen (HK_STATUS ...) -> mit bekannten Dicts auswerten
            try: ns[node.targets[0].id] = eval(compile(ast.Expression(node.value), src, "eval"), dict(ns))
            except Exception: pass
BASE, AVAIL, DEVICE = ns["BASE"], ns["AVAIL"], ns["DEVICE"]
SENSORS, CONTROLS = ns["SENSORS"], ns["CONTROLS"]

got = {}
for line in open("out_ha_discovery.jsonl", encoding="utf-8"):
    topic, payload = line.rstrip("\n").split("\t", 1)
    got[topic] = json.loads(payload)          # wirft bei kaputtem JSON

errors = []
def chk(cond, msg):
    if not cond: errors.append(msg)

expected = 0
for key, reg, name, unit, dc, enum in SENSORS + [("cop", 31667, "COP aktuell", None, None, None)]:
    topic = f"homeassistant/sensor/hoxpi/{key}/config"
    expected += 1
    if topic not in got:
        if full: errors.append(f"fehlt: {topic}")
        continue
    g = got[topic]
    chk(g["name"] == name, f"{key}: name {g['name']!r} != {name!r}")
    chk(g["unique_id"] == f"hoxpi_{key}", f"{key}: unique_id {g['unique_id']}")
    chk(g["state_topic"] == f"{BASE}/{key}/state", f"{key}: state_topic {g['state_topic']}")
    chk(g["availability_topic"] == AVAIL, f"{key}: availability_topic {g['availability_topic']}")
    chk(g.get("unit_of_measurement") == unit, f"{key}: unit {g.get('unit_of_measurement')!r} != {unit!r}")
    chk(g.get("device_class") == dc, f"{key}: device_class {g.get('device_class')!r} != {dc!r}")
    chk(g.get("state_class") == ("measurement" if dc else None), f"{key}: state_class")
    chk(g["device"] == DEVICE, f"{key}: device-Block {g['device']}")
    chk("command_topic" not in g, f"{key}: Sensor mit command_topic")

for key, reg, name, art, enum in CONTROLS:
    topic = f"homeassistant/{art}/hoxpi/{key}/config"
    expected += 1
    if topic not in got:
        if full: errors.append(f"fehlt: {topic}")
        continue
    g = got[topic]
    chk(g["name"] == name, f"{key}: name {g['name']!r} != {name!r}")
    chk(g["unique_id"] == f"hoxpi_{key}", f"{key}: unique_id")
    chk(g["state_topic"] == f"{BASE}/{key}/state" and g["command_topic"] == f"{BASE}/{key}/set", f"{key}: Topics")
    chk(g["availability_topic"] == AVAIL and g["device"] == DEVICE, f"{key}: avail/device")
    if art == "select":
        chk(g["options"] == list(enum.values()), f"{key}: options {g['options']} != {list(enum.values())}")
    else:
        chk(isinstance(g["min"], (int, float)) and isinstance(g["max"], (int, float)) and g["min"] < g["max"], f"{key}: min/max {g.get('min')}/{g.get('max')}")
        chk(g["step"] in (0.5, 1) and g["mode"] == "box", f"{key}: step/mode")

for topic, uid, avail in (("homeassistant/binary_sensor/hoxpi/stale/config", "hoxpi_stale", False),
                          ("homeassistant/binary_sensor/hoxpi/kuehl_wartet/config", "hoxpi_kuehl_wartet", True)):
    expected += 1
    g = got.get(topic)
    chk(g is not None, f"fehlt: {topic}")
    if g:
        chk(g["unique_id"] == uid and g["device"] == DEVICE, f"{topic}: unique_id/device")
        chk(("availability_topic" in g) == avail, f"{topic}: availability_topic {'fehlt' if avail else 'unerwartet'}")
        chk(g["json_attributes_topic"].endswith("/attr"), f"{topic}: attr-Topic")

extra = set(got) - {f"homeassistant/sensor/hoxpi/{k}/config" for k, *_ in SENSORS} - {"homeassistant/sensor/hoxpi/cop/config"} \
        - {f"homeassistant/{a}/hoxpi/{k}/config" for k, r, n, a, e in CONTROLS} \
        - {"homeassistant/binary_sensor/hoxpi/stale/config", "homeassistant/binary_sensor/hoxpi/kuehl_wartet/config"}
chk(not extra, f"unerwartete Topics: {sorted(extra)}")

if errors:
    print("\n".join("REF-FEHLER " + e for e in errors)); sys.exit(1)
print(f"REFERENZ HA OK: {len(got)} von {expected} Discovery-Payloads identisch mit hoval_mqtt.py "
      f"({len(SENSORS)} Sensoren, {len(CONTROLS)} Steuerungen, COP, stale, kuehl_wartet){' - VOLL' if full else ''}")
