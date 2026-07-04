#!/usr/bin/env python3
"""
Hoval TopTronic-E CAN  <->  Modbus-TCP Bruecke

Liest Hoval-CAN (50 kbit/s, SocketCAN) und stellt die Werte als Modbus-Holding-
Register bereit, exakt nach der offiziellen TTE-GW-Modbus-Registerkarte
(registers.json). Damit koennen die offiziellen Loxone-Hoval-Templates 1:1
genutzt werden (FC3 lesen, FC6 schreiben).

Modi:
  --dry-run   nur passiv mithoeren + dekodierte Werte ausgeben (kein Modbus, kein Poll)
  (default)   Modbus-TCP-Server + aktives Pollen + Schreiben

Protokoll-Referenz: hoval-exporter README (TTE-Protokoll).
Stand: Skelett, gegen Live-Bus noch zu verifizieren (HV-Adressierung, 32-bit-Layout,
Modbus-Adress-Offset 0/1-basiert je nach Loxone-Vorlage).
"""
import argparse, json, logging, os, struct, threading, time

log = logging.getLogger("hoval-bridge")

# ---- CAN-Protokoll (TTE) ----------------------------------------------------
OP_GET, OP_RESPONSE, OP_SET = 0x40, 0x42, 0x46
# Eigene Bus-Identitaeten (msg_id) - wie hoval-exporter, um Kollisionen zu vermeiden
ARB_POLL    = 0x06E40801   # msg_id=6  (WEZ lesen)
ARB_WRITE   = 0x07E40801   # msg_id=7  (WEZ schreiben)
ARB_HV_POLL = 0x1FE08A08   # GET an HomeVent/Lueftung (UnitId 520), wie die Anlage selbst

# Nur diese Register darf Loxone schreiben (verifizierte, sichere WEZ-Steuer-Datenpunkte).
# Kritische/interne Register bleiben tabu, auch wenn Hoval sie als "writable" fuehrt.
WRITE_WHITELIST = {
    1478,   # Betriebsart Heizen (Standby/Woche1/.../Hand)
    1479,   # Betriebswahl HK2 (0=Standby 1=Woche1 ... 8=Hand Kuehlen) - 03.07.2026 Status-9-Kick
    1481,   # Raumtemperatur Normal (Heizen)  10-30 C
    1482,   # Raumtemperatur Eco (Heizen)      5-20 C
    1496,   # Betriebsart Warmwasser
    1497,   # Warmwasser Normal-Temperatur    10-70 C
    1498,   # Warmwasser Eco-Temperatur       10-70 C
    # --- SG-Ready / Smart Grid (offizielle Loxone-Template-Aktoren) ---
    27509,  # SG Offset Warmwasser-Soll        0-80 K   (Hauptregler/WEZ)
    27528,  # SG Offset Raum-Soll HC1          0-12 K   (Hauptregler/WEZ)
    27529,  # SG Offset Raum-Soll HC2          0-12 K
    27530,  # SG Offset Raum-Soll HC3          0-12 K
    27545,  # SG ueber Systembus (Schalter)    0-3      (Bus-Ansteuerung statt Klemmen)
    27546,  # SG Ausloesen / function trigger  0-3
    28839,  # SG Offset Heizpuffer-Soll        0-90 K   (PS-Modul; wirkt erst wenn PS angesteckt)
    # --- Erweiterung 02.07.2026 ---
    1561,   # Betriebswahl Waermeerzeuger      0=aus 1=Auto 4=Man.Heizen 5=Man.Kuehlen (LIST)
    1510,   # Raum-Ist HK1 (extern einspeisbar, S16 dec1)
    1511,   # Raum-Ist HK2
    1512,   # Raum-Ist HK3
    # --- Erweiterung 03.07.2026: UG-Kuehlung (To-do 8) ---
    19482,  # HK1 Konstantanforderung Kuehlen (dp 7047, dec1; 180 = 18.0 C, 0 = aus)
    23755,  # HK2 Konstantanforderung Kuehlen (dito; 0 = Phantom-Anforderung weg)
    27531,  # SG Offset Raum-Soll Kuehlen HK1/UG (dp 7046, dec1, 0-120 = 0-12.0 K) - 04.07.2026
    27532,  # SG Offset Raum-Soll Kuehlen HK2/OG (dito) - 04.07.2026
}
WRITE_MIN_INTERVAL = 2.0   # s, Rate-Limit pro Register

# --- Dynamische Whitelist (Dashboard-Checkboxen, 04.07.2026) ------------------
# whitelist.json wird vom Dashboard (Seite "Register") verwaltet; Aenderungen
# wirken OHNE Neustart (mtime-Check). Fehlt/kaputt -> eingebaute WRITE_WHITELIST.
WHITELIST_FILE = "/home/admin/hoval-bridge/whitelist.json"
_wl_cache = {"mtime": None, "set": None}
def current_whitelist():
    import os as _os
    try:
        mt = _os.path.getmtime(WHITELIST_FILE)
    except OSError:
        return WRITE_WHITELIST
    if _wl_cache["mtime"] != mt:
        try:
            with open(WHITELIST_FILE) as f:
                data = json.load(f)
            _wl_cache["set"] = set(int(x) for x in data.get("allowed", []))
            _wl_cache["mtime"] = mt
            log.info("Whitelist neu geladen: %d Register erlaubt", len(_wl_cache["set"]))
        except Exception as e:
            log.error("whitelist.json fehlerhaft (%s) - nutze eingebaute Liste", e)
            return WRITE_WHITELIST
    return _wl_cache["set"] if _wl_cache["set"] is not None else WRITE_WHITELIST


def decode_value(typ, raw):
    """raw bytes -> int (Rohwert wie vom Hoval-Gateway, OHNE Dezimalskalierung)."""
    if not raw:
        return None
    t = (typ or "").upper()
    if t in ("U8",):    return raw[0]
    if t in ("S8",):    return struct.unpack(">b", raw[:1])[0]
    if t in ("U16","LIST"): return int.from_bytes(raw[:2], "big")
    if t in ("S16",):   return int.from_bytes(raw[:2], "big", signed=True)
    if t in ("U32",):   return int.from_bytes(raw[:4], "big")
    if t in ("S32",):   return int.from_bytes(raw[:4], "big", signed=True)
    return int.from_bytes(raw[:2], "big")

def to_registers(typ, value):
    """int -> Liste von 16-bit-Registerwoertern (big-endian, hi zuerst)."""
    t = (typ or "").upper()
    if t in ("U32","S32"):
        v = value & 0xFFFFFFFF
        return [(v >> 16) & 0xFFFF, v & 0xFFFF]
    return [value & 0xFFFF]

SENTINELS = {0x8000, 0xFFFF}  # "kein Sensor"

# ---- Register-Map -----------------------------------------------------------
class RegMap:
    def __init__(self, path):
        self.rows = json.load(open(path, encoding="utf-8"))
        self.by_reg = {r["reg"]: r for r in self.rows}
        # Index nach (fg,fn,dp) -> Liste von Registern (fuer passive Dekodierung)
        self.by_dp = {}
        for r in self.rows:
            self.by_dp.setdefault((r["fg"], r["fn"], r["dp"]), []).append(r)
        self.min_reg = min(self.by_reg)
        self.max_reg = max(self.by_reg)
    def writable(self, reg):
        r = self.by_reg.get(reg)
        return r and str(r.get("writable")).strip().lower() in ("yes","true","1","x","w")

# ---- Modbus-Datastore-Brueckung --------------------------------------------
def build_modbus(regmap, on_write):
    from pymodbus.datastore import (ModbusServerContext, ModbusSlaveContext,
                                    ModbusSparseDataBlock)
    class WriteBlock(ModbusSparseDataBlock):
        def set_internal(self, address, values):
            # interne Aktualisierung aus CAN-Dekodierung -> NUR Datastore, KEIN Rueckschreiben
            super().setValues(address, values)
        def setValues(self, address, values):
            # externer Modbus-Schreibzugriff (FC6/FC16) von Loxone -> ggf. CAN-SET
            super().setValues(address, values)
            try:
                on_write(address, values)
            except Exception as e:
                log.error("write-callback: %s", e)
    init = {r: 0 for r in regmap.by_reg}      # alle bekannten Register, Startwert 0
    block = WriteBlock(init)
    slave = ModbusSlaveContext(hr=block, zero_mode=True)  # Adresse = Registernummer
    return ModbusServerContext(slaves=slave, single=True), block

# ---- CAN-Handling -----------------------------------------------------------
class Bridge:
    def __init__(self, args):
        self.args = args
        self.regmap = RegMap(args.registers)
        self.bus = None
        self.block = None
        self.context = None
        self.rx_count = 0
        self.dec_count = 0
        self.err_count = 0
        self._last_write = {}
        self._pending = {}   # Mehrfach-Frame-Reassembly: (devkey,seq) -> [bytearray, remaining]
        self._seen_from_can = set()  # Register, die schon mind. 1x vom CAN dekodiert wurden

    def open_can(self):
        import can
        self.bus = can.Bus(channel=self.args.can, interface="socketcan")
        log.info("CAN offen: %s", self.args.can)

    # ----- passiv: Frames reassemblieren (Einzel- UND Mehrfach-Frame) + dekodieren -----
    # Protokoll (aus parren/hoval-ultrasource-agent): Arb-Top-Byte = Frame-Typ.
    #   0x1f = Start (Data[0]>>3 = Folge-Frames; 0 => Einzel-Frame, sonst Seq-ID=Data[1], Daten ab Data[2])
    #   0x00 = ignorieren; sonst Fortsetzung (Seq-ID=Data[0], Daten ab Data[1]; am Ende 2 Byte CRC weg)
    #   Geraete-Schluessel = arb & 0xFFFF (devType<<8|devId).
    def handle_frame(self, msg):
        if getattr(msg, "is_error_frame", False):
            self.err_count += 1
            return
        self.rx_count += 1
        a = msg.arbitration_id
        ftype = (a >> 24) & 0xFF
        devkey = a & 0xFFFF
        d = bytes(msg.data)
        if not d:
            return
        if ftype == 0x1f:
            if len(d) < 2:
                return
            remaining = d[0] >> 3
            if remaining == 0:
                self._parse_message(d[1:])
            else:
                self._pending[(devkey, d[1])] = [bytearray(d[2:]), remaining - 1]
        elif ftype == 0x00:
            return
        else:
            key = (devkey, d[0])
            unf = self._pending.get(key)
            if unf is None:
                return
            unf[0] += d[1:]
            unf[1] -= 1
            if unf[1] <= 0:
                self._pending.pop(key, None)
                data = unf[0]
                if len(data) >= 2:
                    data = data[:-2]   # CRC abschneiden
                self._parse_message(bytes(data))

    def _parse_message(self, raw):
        if len(raw) < 5:
            return
        if raw[0] != 0x42:                      # nur saubere ANSWER-Frames (16- u. 32-bit)
            return
        fg, fn = raw[1], raw[2]
        dp = int.from_bytes(raw[3:5], "big")
        val = bytes(raw[5:])
        regs = self.regmap.by_dp.get((fg, fn, dp))
        if not regs:
            return
        for r in regs:
            t = (r["type"] or "").upper()
            # 32-bit: an das "_high"-Register beide Woerter (high@reg, low@reg+1) schreiben;
            # das "_low"-Register dabei ueberspringen (wird mitgeschrieben).
            if t in ("U32", "S32") and (r.get("name") or "").endswith("_low"):
                continue
            v = decode_value(t, val)
            if v is None:
                continue
            self.dec_count += 1
            self._seen_from_can.add(r["reg"])
            if self.block is not None:
                self.block.set_internal(r["reg"], to_registers(t, v))

    def rx_loop(self):
        for msg in self.bus:
            if msg is None:
                continue
            try:
                self.handle_frame(msg)
            except Exception as e:
                log.debug("frame-err: %s", e)

    # ----- aktiv: GET-Requests fuer WEZ-Datenpunkte -----
    def build_targets(self):
        # WEZ (UnitId 1) ueber ARB_POLL, HomeVent/Lueftung (UnitId 520, fg=50) ueber ARB_HV_POLL.
        # 32-bit jetzt MIT pollen (Reassembly dekodiert Mehrfach-Frames). Doppelte (fg,fn,dp) nur einmal.
        seen = set(); wez = []; hv = []
        for r in self.regmap.rows:
            if r["fg"] is None:
                continue
            key = (r["unit_id"], r["fg"], r["fn"], r["dp"])
            if key in seen:
                continue
            seen.add(key)
            if r["unit_id"] == 1:
                wez.append((ARB_POLL, r))
            elif r["unit_id"] == 520 and r["fg"] == 50:
                hv.append((ARB_HV_POLL, r))
        return wez, hv

    def poll_targets(self, targets, interval):
        import can
        while True:
            for arb, r in targets:
                payload = bytes([0x01, OP_GET, r["fg"] & 0xFF, r["fn"] & 0xFF,
                                 (r["dp"] >> 8) & 0xFF, r["dp"] & 0xFF])
                try:
                    self.bus.send(can.Message(arbitration_id=arb,
                                              data=payload, is_extended_id=True))
                except Exception as e:
                    log.debug("poll-send: %s", e)
                time.sleep(self.args.poll_delay)
            time.sleep(interval)

    # ----- Schreiben: Modbus FC6 -> CAN SET -----
    def on_write(self, address, values):
        import can, time
        if not getattr(self.args, "enable_write", False):
            log.warning("Schreibzugriff deaktiviert (--enable-write fehlt) - ignoriere Modbus-Write reg %s", address)
            return
        now = time.time()
        for i, v in enumerate(values):
            reg = address + i
            r = self.regmap.by_reg.get(reg)
            if not r:
                continue
            # 1) Whitelist
            if reg not in current_whitelist():
                log.warning("ABGELEHNT reg %d (%s): nicht in Schreib-Whitelist",
                            reg, r.get("name"))
                continue
            # 1b) Kalt-Cache-Schutz: erst schreiben, wenn Register 1x vom CAN gelesen wurde
            #     (verhindert versehentliche 0-Writes direkt nach Neustart)
            if reg not in self._seen_from_can:
                log.warning("ABGELEHNT reg %d (%s): noch nie vom CAN gelesen (Cache kalt)",
                            reg, r.get("name"))
                continue
            # 2) Wertebereich (min/max sind Rohwerte; signed beachten)
            typ = (r.get("type") or "").upper()
            chk = v - 65536 if (typ == "S16" and v > 32767) else v
            mn, mx = r.get("min"), r.get("max")
            if mn is not None and mx is not None and not (mn == 0 and mx == 0):
                if not (mn <= chk <= mx):
                    log.warning("ABGELEHNT reg %d (%s): Wert %s ausserhalb [%s..%s]",
                                reg, r.get("name"), chk, mn, mx)
                    continue
            # 3) Rate-Limit pro Register
            if now - self._last_write.get(reg, 0) < WRITE_MIN_INTERVAL:
                log.warning("ABGELEHNT reg %d (%s): Rate-Limit (zu schnell)", reg, r.get("name"))
                continue
            self._last_write[reg] = now
            # 4) CAN-SET, datentyp-gerecht (U8/LIST = 1 Byte, sonst 2 Byte BE)
            dp = r["dp"]
            data = bytes([v & 0xFF]) if typ in ("U8", "S8", "LIST") \
                   else bytes([(v >> 8) & 0xFF, v & 0xFF])
            payload = bytes([0x01, OP_SET, r["fg"] & 0xFF, r["fn"] & 0xFF,
                             (dp >> 8) & 0xFF, dp & 0xFF]) + data
            try:
                self.bus.send(can.Message(arbitration_id=ARB_WRITE,
                                          data=payload, is_extended_id=True))
                log.info("SET reg %d (%s) <- %s (raw)", reg, r.get("name"), v)
            except Exception as e:
                log.error("set-send: %s", e)

    def run(self):
        self.open_can()
        threading.Thread(target=self.rx_loop, daemon=True).start()
        if self.args.dry_run:
            log.info("DRY-RUN: nur mithoeren. Strg+C zum Beenden.")
            while True:
                time.sleep(5)
                log.info("Daten-Frames=%d, dekodiert=%d, Error-Frames=%d",
                         self.rx_count, self.dec_count, self.err_count)
        # Modbus + Poll
        self.context, self.block = build_modbus(self.regmap, self.on_write)
        if not self.args.no_poll:
            wez, hv = self.build_targets()
            log.info("Poll: %d WEZ (alle %ss) + %d Lueftung (alle 5s)",
                     len(wez), self.args.poll_interval, len(hv))
            threading.Thread(target=self.poll_targets, args=(wez, self.args.poll_interval), daemon=True).start()
            if hv:
                threading.Thread(target=self.poll_targets, args=(hv, 5.0), daemon=True).start()
        from pymodbus.server import StartTcpServer
        log.info("Modbus-TCP-Server auf %s:%d  (%d Register)",
                 self.args.host, self.args.port, len(self.regmap.by_reg))
        StartTcpServer(context=self.context, address=(self.args.host, self.args.port))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--can", default="can0")
    ap.add_argument("--registers", default=os.path.join(os.path.dirname(__file__), "registers.json"))
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=502)
    ap.add_argument("--poll-interval", type=float, default=30.0)
    ap.add_argument("--poll-delay", type=float, default=0.1)
    ap.add_argument("--no-poll", action="store_true")
    ap.add_argument("--enable-write", action="store_true",
                    help="erlaubt Modbus-FC6/16 -> CAN-SET (Schreiben auf die WP). Default AUS = nur lesen.")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args()
    logging.basicConfig(level=args.log_level,
                        format="%(asctime)s %(levelname)s %(message)s")
    Bridge(args).run()

if __name__ == "__main__":
    main()
