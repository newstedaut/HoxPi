#!/usr/bin/env python3
"""HoxPi Konfigurations-Keepalive für die Hoval TopTronic E.

Schreibt die (flüchtigen) Datenpunkte nach, die das unveränderte Hoval-Loxone-
Template relais-/kontaktlos betreiben. WELCHE Datenpunkte geschrieben werden,
steht in hoxpi-features.json → "keepalive_dps" — jeder einzeln ein-/ausschaltbar
(Dashboard: Sicherheit → Funktionen).

Standard-Datenpunkte:
  30046 = 0   Zuo. Eing. Ext. Konstantanforderung Heizen  → AUS (bus-getrieben)
  30057 = 0   Zuo. Eing. Ext. Konstantanforderung Kühlen  → AUS (bus-getrieben)
  30066 = 0   Zuo. Eing. Umschaltung Heizen/Kühlen         → AUS (Richtung übers Register)
  3032  = 3   Regelstrategie 3 (Konstant) — REDUNDANT: schreibt auch Loxone (27510)
              und der Parameter ist gespeichert; standardmäßig deaktivierbar.

Warum die 30er nachschreiben: nicht persistent (auf dieser Anlage zusätzlich
SW-Mismatch BedienModul 2.19 > WEZ 2.15). Die 3032 dagegen bleibt gesetzt →
kann i.d.R. aus.
"""
import can, time, sys, json

FEAT = "/home/admin/hoxpi-features.json"
DEFAULT_DPS = {
    "30046": {"enabled": True, "value": 0},
    "30057": {"enabled": True, "value": 0},
    "30066": {"enabled": True, "value": 0},
    "3032":  {"enabled": True, "value": 3},
}
try:
    F = json.load(open(FEAT))
except Exception:
    F = {}

# Master-Schalter
if not F.get("keepalive", {}).get("enabled", True):
    print("%s keepalive deaktiviert (features.json)" % time.strftime("%F %T")); sys.exit(0)

dps = F.get("keepalive_dps") or DEFAULT_DPS

ARB = 0x1FE08801
try:
    bus = can.Bus(channel='can0', interface='socketcan')
except Exception as e:
    print('%s CAN-Fehler: %s' % (time.strftime('%F %T'), e)); sys.exit(1)

def setdp(dp, val, fg=1, fn=0):
    f = bytes([0x01, 0x46, fg, fn, (dp >> 8) & 0xFF, dp & 0xFF]) + bytes([val & 0xFF])
    for _ in range(2):
        bus.send(can.Message(arbitration_id=ARB, data=f, is_extended_id=True))
        time.sleep(0.2)

done = []
for dp, cfg in dps.items():
    if cfg.get("enabled", True):
        setdp(int(dp), int(cfg.get("value", 0)))
        done.append("dp%s=%s" % (dp, cfg.get("value", 0)))

bus.shutdown()
print('%s keepalive ok: %s' % (time.strftime('%F %T'), ", ".join(done) if done else "(nichts aktiv)"))
