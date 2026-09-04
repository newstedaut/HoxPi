#!/usr/bin/env python3
"""hoval_sollzustand.py — setpoint-state guard for the Hoval TopTronic E (HoxPi).

Purpose: after a power cut, a service visit or an accidental change at the control panel
the Pi restores the basic operating mode of the system ITSELF — no chat, no AI, no Loxone.
Runs every 5 min via cron (user admin), reads the registers through HoxPi's own bridge
(Modbus-TCP 127.0.0.1:502, FC3) and writes only when a value deviates from the target
TWICE in a row (= 10 min) — protects against a cold bridge cache right after boot and
against short transients. Writing = FC6 through the bridge, so whitelist / value range /
rate limit of the bridge still apply (the register must be on the whitelist!).

Configuration: /home/admin/hoxpi-sollzustand.json  (see watch/hoxpi-sollzustand.example.json)
  {"register": {"1561": 1, "1478": 4, "27510": 3, "27546": 2}, "bestaetigungen": 2}
  1561 operating mode heat generator = 1 automatic · 1478 operating mode HC1 = 4 constant
  27510 control strategy = 3 constant · 27546 Smart-Grid trigger = 2 system bus
  Adapt the register list to YOUR system — these are the values of the reference system.

Feature switch: hoxpi-features.json -> "sollzustand": {"enabled": true}  (dashboard: Security -> Features)
Maintenance: create the file /home/admin/WARTUNG -> the guard does nothing (only a log line).
Delete the file afterwards -> the guard restores the target state again.
Log: /home/admin/sollzustand.log (deviations, corrections and errors only).
"""
import socket, struct, json, os, time, sys

HOME = "/home/admin"
CFG = HOME + "/hoxpi-sollzustand.json"
FEAT = HOME + "/hoxpi-features.json"
STATE = HOME + "/.sollzustand_state.json"
LOG = HOME + "/sollzustand.log"
FLAG = HOME + "/WARTUNG"
HOST, PORT, UNIT = "127.0.0.1", 502, 1
DEFAULT = {"register": {"1561": 1, "1478": 4, "27510": 3, "27546": 2}, "bestaetigungen": 2}

def log(msg):
    line = "%s %s\n" % (time.strftime("%F %T"), msg)
    with open(LOG, "a") as f: f.write(line)
    print(line, end="")

def mb(sock, pdu, tid):
    sock.sendall(struct.pack(">HHHB", tid, 0, len(pdu) + 1, UNIT) + pdu)
    hdr = sock.recv(7)
    if len(hdr) < 7: raise IOError("short reply")
    _, _, ln, _ = struct.unpack(">HHHB", hdr)
    body = b""
    while len(body) < ln - 1:
        chunk = sock.recv(ln - 1 - len(body))
        if not chunk: break
        body += chunk
    if body and body[0] & 0x80: raise IOError("Modbus exception %d (FC %d)" % (body[1], body[0] & 0x7F))
    return body

def read(sock, reg, tid):
    b = mb(sock, struct.pack(">BHH", 3, reg, 1), tid)
    return struct.unpack(">h", b[2:4])[0]

def write(sock, reg, val, tid):
    mb(sock, struct.pack(">BHh", 6, reg, val), tid)

def feature_enabled():
    try:
        return bool(json.load(open(FEAT)).get("sollzustand", {}).get("enabled", True))
    except Exception:
        return True

def main():
    if not feature_enabled():
        return 0
    try: cfg = json.load(open(CFG))
    except Exception: cfg = DEFAULT
    regs = {int(k): int(v) for k, v in cfg.get("register", DEFAULT["register"]).items()}
    need = int(cfg.get("bestaetigungen", 2))
    try: state = json.load(open(STATE))
    except Exception: state = {}
    if os.path.exists(FLAG):
        if state.get("_wartung") != True:
            log("WARTUNG-Flag vorhanden → Wächter pausiert (Datei %s löschen zum Fortsetzen)" % FLAG)
        state = {"_wartung": True}; json.dump(state, open(STATE, "w")); return 0
    if state.get("_wartung"):
        log("WARTUNG beendet → Wächter aktiv"); state = {}
    try:
        s = socket.create_connection((HOST, PORT), timeout=5)
    except Exception as e:
        log("Bridge nicht erreichbar: %s" % e); return 1
    tid = int(time.time()) & 0xFFFF
    rc = 0
    for reg, soll in regs.items():
        key = str(reg)
        try:
            ist = read(s, reg, tid); tid = (tid + 1) & 0xFFFF
        except Exception as e:
            log("reg %d: Lesefehler %s" % (reg, e)); rc = 1; continue
        if ist == soll:
            if state.get(key, 0): log("reg %d wieder %d (ohne Eingriff)" % (reg, soll))
            state[key] = 0; continue
        state[key] = state.get(key, 0) + 1
        if state[key] < need:
            log("reg %d = %d statt %d (Abweichung %d/%d, noch kein Eingriff)" % (reg, ist, soll, state[key], need)); continue
        try:
            write(s, reg, soll, tid); tid = (tid + 1) & 0xFFFF
            time.sleep(3)
            neu = read(s, reg, tid); tid = (tid + 1) & 0xFFFF
            if neu == soll:
                log("KORRIGIERT reg %d: %d → %d" % (reg, ist, soll)); state[key] = 0
            else:
                log("reg %d: Schreiben %d NICHT übernommen (danach %d) — Bridge abgelehnt (Whitelist/Cache kalt) oder fremdgesteuert; nächster Versuch in 5 min" % (reg, soll, neu)); rc = 1
        except Exception as e:
            log("reg %d: Schreiben %d abgelehnt/fehlgeschlagen: %s" % (reg, soll, e)); rc = 1
    s.close()
    json.dump(state, open(STATE, "w"))
    return rc

if __name__ == "__main__":
    sys.exit(main())
