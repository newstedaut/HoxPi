#!/usr/bin/env python3
"""
fehler_catcher.py - Backlog 13c: CAN-Rohframes der Fehlerstruktur dp 29042-29046
("Aktiver Fehler 1-5", je 9 Felder) automatisch mitschneiden, sobald sich etwas aendert.

Hintergrund: die Bridge liefert fuer alle 9 Modbus-Register eines Eintrags denselben
Rohwert (nur die ersten Bytes der 16-Byte-Antwort). Die vollstaendige Antwort kommt als
4-Frame-Multiframe (Header 0x21 = 4 Frames, Schluesselbyte, Payload 16 Byte + CRC).
Ohne Fehler: FF 00 FF FF FF FF FF FF 00 00 00 00 00 00 00 00. Die Feldoffsets lassen
sich nur mit einem echten Ereignis festlegen -> dieses Skript wartet darauf.

Ablauf (admin-Cron, minuetlich, rein lesend, kein Schreibzugriff, kein sudo):
  1. Modbus-Signatur lesen: 1534 (Fehlercode), 1540 (Stoerungsflag), erstes Register
     jedes Eintrags 1565/1574/1583/1592/1601.
  2. Aendert sich die Signatur gegenueber dem letzten Lauf (auch zurueck auf "kein
     Fehler" -> disappear-Felder!), wird 45 s `candump` mitgeschnitten. Die Bridge fragt
     29042-29046 ohnehin alle ~8 s ab, es sind also ~5 Antworten je Eintrag im Fenster.
  3. Aus dem Dump werden die Antworten auf dp 0x7172-0x7176 reassembliert und als Hex
     neben die Modbus-Werte in eine .txt geschrieben.
  --test: erzwingt einen Mitschnitt (Baseline / Funktionsprobe).
Dateien: ~/fehler_catch/<zeit>_fc<1534>.log (candump), .txt (Auswertung), state.json, catch.log
"""
import socket, struct, json, os, sys, datetime, subprocess, re, time

MB      = ("127.0.0.1", 502)
BASE    = os.path.expanduser("~/fehler_catch")
STATE   = os.path.join(BASE, "state.json")
LOG     = os.path.join(BASE, "catch.log")
DUMP_S  = 45                      # Sekunden candump
MAX_PER_DAY = 24                  # Schutz gegen Dauerfeuer (SD-Karte)
SIG_REGS = [1534, 1540, 1565, 1574, 1583, 1592, 1601]
ENTRY_REGS = {29042: range(1565, 1574), 29043: range(1574, 1583), 29044: range(1583, 1592),
              29045: range(1592, 1601), 29046: range(1601, 1610)}
DP_HEX = {29042: "71 72", 29043: "71 73", 29044: "71 74", 29045: "71 75", 29046: "71 76"}
FIELDS = ["appearance_time U16", "appearance_date U16", "disappear_time U16", "disappear_date U16",
          "source U16", "function_group U8", "function_number U8", "error_type U8", "error_code U16"]

os.makedirs(BASE, exist_ok=True)

# ---------- Modbus ----------
_tid = [0]
def rd_many(addrs):
    out = {}
    try:
        s = socket.create_connection(MB, 4); s.settimeout(4)
        for a in addrs:
            _tid[0] = (_tid[0] + 1) & 0xFFFF
            s.sendall(struct.pack(">HHHBBHH", _tid[0], 0, 6, 1, 3, a, 1))
            r = s.recv(64)
            out[a] = struct.unpack(">H", r[9:11])[0] if len(r) >= 11 and r[7] == 3 else None
        s.close()
    except Exception as e:
        log("Modbus-Fehler: %s" % e)
    return out

def log(msg):
    with open(LOG, "a") as f:
        f.write("%s %s\n" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg))

def load_state():
    try:
        return json.load(open(STATE))
    except Exception:
        return {}

def save_state(st):
    tmp = STATE + ".tmp"
    json.dump(st, open(tmp, "w"))
    os.replace(tmp, STATE)

# ---------- candump + Reassembly ----------
LINE = re.compile(r"\((\S+ \S+)\)\s+can0\s+([0-9A-F]{8})\s+\[(\d)\]\s+((?:[0-9A-F]{2} ?)*)")

def _is_err_dp(body):
    """Antwort (0x42) auf fg 0 / fn 0 / dp 29042-29046?"""
    return (len(body) >= 5 and body[0] == 0x42 and body[1] == 0 and body[2] == 0
            and body[3] == 0x71 and 0x72 <= body[4] <= 0x76)

def reassemble(path):
    """Antworten auf dp 0x7172-0x7176 (fg 0 / fn 0) aus dem candump zusammensetzen.
    Erstframe: d[0]>>3 = Frames gesamt, d[1] = Schluessel, d[2:] = Payload-Beginn
    (0x42 = Antwort, fg, fn, dp_hi, dp_lo, ...). Folgeframes: d[0] = Schluessel, d[1:] = Payload.
    Letzte 2 Byte = CRC (wie hoval_bridge/verdichter_catcher)."""
    pend = {}
    res = []
    for ln in open(path, errors="replace"):
        m = LINE.search(ln)
        if not m:
            continue
        ts, arb, n, hexs = m.groups()
        d = bytes.fromhex(hexs.replace(" ", ""))
        if len(d) < 2:
            continue
        ft = int(arb[:2], 16)
        if ft == 0x1F:                       # Erstframe (Antwort) / Einzelframe
            total = d[0] >> 3
            if total == 0:
                body = d[1:]
                if _is_err_dp(body):
                    res.append((ts, body))
                continue
            key = d[1]
            body = bytearray(d[2:])
            if _is_err_dp(body):
                pend[key] = [ts, body, total - 1]
        else:
            key = d[0]
            u = pend.get(key)
            if u is None:
                continue
            u[1] += d[1:]
            u[2] -= 1
            if u[2] <= 0:
                pend.pop(key, None)
                res.append((u[0], bytes(u[1][:-2])))   # CRC abschneiden
    return res

def decode_guess(payload):
    """Erste Deutungsversuche der 16 Datenbytes (nur Anzeige, keine Wahrheit)."""
    data = payload[5:]
    out = ["  daten(16): " + " ".join("%02X" % b for b in data)]
    if len(data) >= 15:
        v = struct.unpack(">HHHHHBBBH", data[:15])
        out.append("  Deutung A (15 B big-endian, Katalogreihenfolge): " +
                   ", ".join("%s=%s" % (f.split()[0], x) for f, x in zip(FIELDS, v)))
    if len(data) >= 16:
        v = struct.unpack(">HHHHHBBBH", data[1:16])
        out.append("  Deutung B (1 Byte Vorspann %02X, dann 15 B): " % data[0] +
                   ", ".join("%s=%s" % (f.split()[0], x) for f, x in zip(FIELDS, v)))
    return out

def capture(reason, sig):
    today = datetime.date.today().isoformat()
    st = load_state()
    cnt = st.get("count", {})
    if cnt.get(today, 0) >= MAX_PER_DAY:
        log("Tageslimit erreicht, kein Mitschnitt (%s)" % reason)
        return
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fc = sig.get("1534", "x")
    dump = os.path.join(BASE, "%s_fc%s.log" % (ts, fc))
    log("Mitschnitt %s s -> %s (%s) Signatur %s" % (DUMP_S, os.path.basename(dump), reason, sig))
    with open(dump, "w") as f:
        subprocess.run(["timeout", str(DUMP_S), "candump", "-t", "A", "can0"], stdout=f, stderr=subprocess.DEVNULL)
    vals = rd_many([r for rr in ENTRY_REGS.values() for r in rr] + [1534, 1540])
    frames = reassemble(dump)
    txt = dump[:-4] + ".txt"
    with open(txt, "w") as f:
        f.write("fehler_catcher %s  Grund: %s\n" % (ts, reason))
        f.write("Modbus 1534=%s 1540=%s\n" % (vals.get(1534), vals.get(1540)))
        for dp, rr in ENTRY_REGS.items():
            f.write("dp %d (Modbus %d-%d): %s\n" % (dp, rr[0], rr[-1], " ".join(str(vals.get(r)) for r in rr)))
        f.write("\nCAN-Antworten (%d im Fenster):\n" % len(frames))
        seen = {}
        for t, body in frames:
            dp = (body[3] << 8) | body[4]
            key = (dp, bytes(body))
            seen[key] = seen.get(key, 0) + 1
        for (dp, body), n in sorted(seen.items()):
            f.write("dp %d  x%d  %s\n" % (dp, n, " ".join("%02X" % b for b in body)))
            for line in decode_guess(body):
                f.write(line + "\n")
    cnt[today] = cnt.get(today, 0) + 1
    st["count"] = {k: v for k, v in cnt.items() if k >= (datetime.date.today() - datetime.timedelta(days=3)).isoformat()}
    st["last_capture"] = ts
    save_state(st)
    log("fertig: %d Antworten, %s" % (len(frames), os.path.basename(txt)))

def main():
    force = "--test" in sys.argv
    vals = rd_many(SIG_REGS)
    if any(v is None for v in vals.values()):
        log("Signatur unvollstaendig %s" % vals)
        if not force:
            return
    sig = {str(k): v for k, v in vals.items()}
    st = load_state()
    last = st.get("sig")
    if force:
        capture("--test", sig)
    elif last is None:
        log("Erststart, Signatur %s" % sig)
    elif sig != last:
        capture("Signatur geaendert (vorher %s)" % last, sig)
    st = load_state()
    st["sig"] = sig
    st["last_run"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_state(st)

if __name__ == "__main__":
    main()
