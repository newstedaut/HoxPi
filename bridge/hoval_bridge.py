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
import re

# 01.09.2026: Hovals Datenpunktliste benennt die 2. Haelfte eines 32-Bit-Wertes
# mal "..._low" (Unterstrich) und mal "... low" (Leerzeichen, teils mit
# Trailing Space). Der alte endswith("_low") erwischte nur die Unterstrich-
# Variante -> 31 von 116 32-Bit-Registern bekamen in BEIDE Haelften denselben
# (auf das High-Word gekuerzten) Wert. Belegt an den Laufzeitzaehlern:
# CAN-Rohwert 60-7-1033 = 0x00018CB0 (=10155,2 h), Modbus lieferte 0,1 h.
_LOW_SUFFIX = re.compile(r"[_ ]low$", re.I)

log = logging.getLogger("hoval-bridge")

# ---- CAN-Protokoll (TTE) ----------------------------------------------------
OP_GET, OP_RESPONSE, OP_SET = 0x40, 0x42, 0x46
# Eigene Bus-Identitaeten (msg_id) - wie hoval-exporter, um Kollisionen zu vermeiden
ARB_POLL    = 0x06E40801   # msg_id=6  (WEZ lesen)
ARB_WRITE   = 0x07E40801   # msg_id=7  (WEZ schreiben)
ARB_HV_POLL = 0x1FE08A08   # GET an HomeVent/Lueftung (UnitId 520), wie die Anlage selbst

# --- Mehrere Geraete gleicher Art (22.11.2026, Issue #1) ----------------------
# Antworten (0x42) kommen als Broadcast; der ABSENDER-Knoten steht in den Bits
# 11-15 der CAN-ID (gemessen: WEZ 1 -> Knoten 1, HomeVent 520 -> Knoten 8,
# PS 143 -> Knoten 15, zweite WP -> Knoten 2). Der Knoten ist UnitId & 0x1F.
# Frueher wurde jede Antwort nur ueber (fg,fn,dp) zugeordnet: an einem Bus mit
# zwei Waermepumpen landeten Werte der WP 2 in den Registern der WP 1.
WEZ_UNITS = range(1, 17)            # offizielle Liste: WEZ UnitId 1..16
WRITE_UNITS = {1, 520}              # nur dorthin gibt es einen geprueften SET-Weg

def src_node(arb):
    return (arb >> 11) & 0x1F

def unit_node(unit_id):
    return None if unit_id is None else int(unit_id) & 0x1F

def poll_arb(unit_id):
    """GET-ID fuer einen WEZ: ARB_POLL mit Ziel-Knoten in den unteren 11 Bit."""
    return (ARB_POLL & ~0x7FF) | (int(unit_id) & 0x7FF)

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
    # --- Erweiterung 03.07.2026: UG-Kuehlung & Heizen (Hoval Master Template) ---
    1490,   # HK1 Konstantanforderung Heizen (dp 7048, dec1, 10-80 C, 0=aus)
    1491,   # HK2 Konstantanforderung Heizen (dito)
    19482,  # HK1 Konstantanforderung Kuehlen (dp 7047, dec1; 180 = 18.0 C, 0 = aus)
    23755,  # HK2 Konstantanforderung Kuehlen (dito; 0 = Phantom-Anforderung weg)
    27510,  # Regelstrategie HK1 (0=Witterung, 3=Konstant, 4=Witterung Heizen + Konstant Kuehlen)
    27511,  # Regelstrategie HK2 (dito)
    27531,  # SG Offset Raum-Soll Kuehlen HK1/UG (dp 7046, dec1, 0-120 = 0-12.0 K) - 04.07.2026
    27532,  # SG Offset Raum-Soll Kuehlen HK2/OG (dito) - 04.07.2026
}
WRITE_MIN_INTERVAL = 0.05   # s, minimales Intervall (verhindert Bus-Flut, laesst Loxone-Befehle sofort durch)

# --- Fast-Lane (07.09.2026) -------------------------------------------------
# Register, die sich schnell aendern und in Dashboard/Grafana/MQTT/Loxone als
# "live" gelten. Sie bekommen einen eigenen Poll-Thread, weil der normale
# WEZ-Zyklus ~60 s dauert (304 Ziele x poll_delay + poll_interval).
FAST_REGS = [
    18726,   # Modulation Verdichter
    25611,   # elektrische Leistung WEZ
    25612,   # thermische Leistung WEZ
    18760,   # Systemvorlauf
    1535,    # Ruecklauf
    1500,    # Warmwasser Ist
    1504,    # Warmwasser Status
    1501,    # Status Heizkreis 1
    1477,    # Aussentemperatur
    1534,    # Fehlercode
    18767,   # Leistungs-Sollwert (Fruehindikator)
    19870,   # UKA-/Kuehlventil
    31708,   # Volumenstrom
]

# --- Kanal-Exklusion Heizen/Kuehlen (relais-freier Template-Betrieb) ----------
# Pro Heizkreis darf nur EIN Sollwert-Register != 0 sein. Schreibt Loxone den
# einen Kanal (>0), nullt HoxPi automatisch den gepaarten anderen Kanal - so
# uebernimmt HoxPi in Software die Rolle des Umschaltkontakts (VE3).
# Paarung Heizen <-> Kuehlen je HK: HC1 1490/19482, HC2 1491/23755, HC3 1492/23756.
EXCL_PAIRS = {
    1490: 19482, 19482: 1490,   # HC1
    1491: 23755, 23755: 1491,   # HC2
    1492: 23756, 23756: 1492,   # HC3
}
EXCL_MIN_INTERVAL = 2.0   # s, Throttle fuer den Partner-Null-Write

# --- Dynamische Whitelist (Dashboard-Checkboxen, 04.07.2026) ------------------
# whitelist.json wird vom Dashboard (Seite "Register") verwaltet; Aenderungen
# wirken OHNE Neustart (mtime-Check). Fehlt/kaputt -> eingebaute WRITE_WHITELIST.
ZERO_OK_REGS = {1490, 1491, 19482, 23755}   # Vorlauf-Soll Konstantanforderung: 0 = keine Anforderung
WHITELIST_FILE = "/home/admin/hoval-bridge/whitelist.json"
# R8 (04.09.2026): Warm-Cache - zuletzt vom CAN gesehene Registerwoerter ueberleben
# einen Bridge-Neustart, damit Loxone nach einem Kaltstart keine 0-Werte sieht
# (1477 = 0,0 C -> Frostschutz-Latch am 03.09.2026). Geladene Werte zaehlen NICHT
# als "vom CAN gelesen" (Schreibsperre 1b bleibt aktiv, bis der CAN antwortet).
CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache_last.json")
CACHE_INTERVAL = 60.0        # s zwischen zwei Sicherungen
CACHE_MAX_AGE = 48 * 3600    # s; aeltere Caches werden ignoriert (nur Log)
CACHE_EXCLUDE = {1534}       # Fehlercode: 0 = "kein Wert" muss nach Neustart sichtbar bleiben
# R8b (05.09.2026): Zustandsdatei fuer Dashboard/Exporter (stale = geladen, vom CAN noch nicht bestaetigt)
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bridge_state.json")
STATE_INTERVAL = 15.0        # s zwischen zwei Zustandsberichten
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
    # HP-1: ab welchem Vielfachen des gemessenen Poll-Durchlaufs ein Register als
    # eingefroren gilt. 4 laesst einzelne verlorene Antworten durchgehen und schlaegt
    # trotzdem lange vor den 4 Tagen an, die 25613 unbemerkt stillstand.
    FROZEN_FACTOR = 4.0

    def __init__(self, args):
        self._pair_cache = {}
        self.args = args
        self.regmap = RegMap(args.registers)
        self.bus = None
        self.block = None
        self.context = None
        self.rx_count = 0
        self.dec_count = 0
        self.err_count = 0
        self._last_write = {}
        self._pending = {}   # Mehrfach-Frame-Reassembly: (devkey,seq) -> [bytearray, remaining, timestamp]
        # HP-1 (12.09.2026): war eine MENGE ("jemals gesehen"). Damit galt ein Register,
        # das der CAN nach der ersten Bestaetigung nie wieder lieferte, ewig als frisch --
        # genau so blieben 25613/25614/27467 seit 08.09. 13:25 als Standbild unentdeckt.
        # Jetzt ein DICT reg -> Zeitstempel der LETZTEN Bestaetigung. `in`, `len` und
        # Iteration verhalten sich wie bei der Menge, die uebrigen Stellen bleiben gueltig.
        self._seen_from_can = {}
        self._sweep_s = {}           # label -> gemessene Dauer eines vollen Poll-Durchlaufs [s]
        self._poll_regs = set()      # HP-1: alle Register, die wir aktiv POLLEN (Sollzustand)
        self._cache_regs = set()     # R8b: beim Start aus dem Warm-Cache vorbelegte Registerwoerter
        self._cache_loaded = 0
        self._cache_age = 0.0
        self._t0 = time.time()
        self._send_lock = threading.Lock()

    def open_can(self):
        import can
        self.bus = can.Bus(channel=self.args.can, interface="socketcan")
        log.info("CAN offen: %s", self.args.can)

    def send_msg(self, msg):
        """Thread-sicheres Senden auf SocketCAN."""
        with self._send_lock:
            self.bus.send(msg)

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
        now = time.time()
        # Veraltete unvollständige Reassembly-Puffer aufräumen (verhindert Memory-Leaks bei CAN-Drops)
        if len(self._pending) > 20:
            stale = [k for k, v in self._pending.items() if len(v) > 2 and (now - v[2]) > 5.0]
            for k in stale:
                self._pending.pop(k, None)

        if ftype == 0x1f:
            if len(d) < 2:
                return
            remaining = d[0] >> 3
            if remaining == 0:
                self._parse_message(d[1:], src_node(a))
            else:
                self._pending[(devkey, d[1])] = [bytearray(d[2:]), remaining - 1, now]
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
                self._parse_message(bytes(data), src_node(devkey))

    def _effective_rows(self, fg, fn, dp, regs):
        """32-Bit-Paare STRUKTURELL erkennen statt ueber den Namen.

        01.09.2026: Hovals Datenpunktliste benennt die zweite Haelfte eines
        32-Bit-Wertes uneinheitlich - mal "_low", mal " low", und bei
        dp51/dp55/dp1029/dp1033 heissen BEIDE Haelften "_high" bzw. tragen
        gar kein Suffix. Namensbasiertes Ueberspringen liess dort beide
        Zeilen durch: die zweite schrieb ihr High-Wort nach reg+1 und ihr
        Low-Wort nach reg+2 - also in ein FREMDES Register
        (27487->27488/27489, 31658->31659/31660, 31662->31663/31664).
        Jetzt: gleiche (unit_id,fg,fn,dp) + direkt aufeinanderfolgende
        reg-Nummern = ein Paar, nur die erste Zeile (=high) verarbeiten.
        Verifiziert gegen registers.json: das Low-Wort steht nie zuerst.
        Der Namenscheck bleibt zusaetzlich fuer Einzelgaenger erhalten.
        """
        key = (fg, fn, dp)
        cached = self._pair_cache.get(key)
        if cached is not None:
            return cached
        skip = set()
        by_unit = {}
        for r in regs:
            if (r["type"] or "").upper() in ("U32", "S32"):
                by_unit.setdefault(r.get("unit_id"), []).append(r)
        for rows in by_unit.values():
            rows.sort(key=lambda x: x["reg"])
            i = 0
            while i < len(rows) - 1:
                if rows[i + 1]["reg"] == rows[i]["reg"] + 1:
                    skip.add(id(rows[i + 1]))
                    i += 2
                else:
                    i += 1
        out = []
        for r in regs:
            if id(r) in skip:
                continue
            if ((r["type"] or "").upper() in ("U32", "S32")
                    and _LOW_SUFFIX.search((r.get("name") or "").strip())):
                continue
            out.append(r)
        self._pair_cache[key] = out
        return out

    def _parse_message(self, raw, src=None):
        """src = Absender-Knoten aus der CAN-ID; None = ohne Absenderpruefung."""
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
        now = time.time()
        check_src = src is not None and getattr(self.args, "sender_filter", True)
        for r in self._effective_rows(fg, fn, dp, regs):
            # Nur in den Registerblock des Geraets schreiben, das geantwortet hat.
            if check_src and r.get("unit_id") is not None and unit_node(r["unit_id"]) != src:
                continue
            t = (r["type"] or "").upper()
            v = decode_value(t, val)
            if v is None:
                continue
            self.dec_count += 1
            self._seen_from_can[r["reg"]] = now   # HP-1: JEDE Bestaetigung stempeln, nicht nur die erste
            if self.block is not None:
                self.block.set_internal(r["reg"], to_registers(t, v))

    # ----- R8 Warm-Cache -----
    def save_cache(self):
        """Alle je vom CAN dekodierten Registerwoerter atomar sichern."""
        if self.block is None:
            return 0
        try:
            seen = self._seen_from_can
            vals = getattr(self.block, "values", {})
            out = {}
            for addr, val in list(vals.items()):
                if addr in seen:
                    base = addr
                elif (addr - 1) in seen and (self.regmap.by_reg.get(addr - 1, {}).get("type") or "").upper() in ("U32", "S32"):
                    base = addr - 1          # zweites Wort eines 32-Bit-Werts
                else:
                    continue
                if base in CACHE_EXCLUDE:
                    continue
                out[str(addr)] = int(val)
            if not out:
                return 0     # noch nichts vom CAN gesehen -> alten Cache NICHT ueberschreiben
            tmp = CACHE_FILE + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump({"ts": time.time(), "regs": out}, f)
            os.replace(tmp, CACHE_FILE)
            return len(out)
        except Exception as e:
            log.warning("cache-save: %s", e)
            return 0

    def load_cache(self):
        """Datastore mit dem letzten Stand vorbelegen (ohne _seen_from_can zu setzen)."""
        try:
            if not os.path.exists(CACHE_FILE):
                log.info("Warm-Cache: keine Datei %s (Kaltstart, alles 0)", CACHE_FILE)
                return 0
            data = json.load(open(CACHE_FILE, encoding="utf-8"))
            age = time.time() - float(data.get("ts", 0))
            if age > CACHE_MAX_AGE:
                log.warning("Warm-Cache ignoriert: %.1f h alt (> %.0f h)", age / 3600, CACHE_MAX_AGE / 3600)
                return 0
            n = 0
            for k, v in data.get("regs", {}).items():
                addr = int(k)
                if addr in CACHE_EXCLUDE:
                    continue
                self.block.set_internal(addr, [int(v) & 0xFFFF])
                self._cache_regs.add(addr)
                n += 1
            self._cache_loaded = n
            self._cache_age = age
            log.info("Warm-Cache geladen: %d Registerwoerter, %.1f min alt (gelten als stale, bis der CAN antwortet)", n, age / 60)
            return n
        except Exception as e:
            log.warning("cache-load: %s", e)
            return 0

    def write_state(self):
        """R8b: kleiner Zustandsbericht fuer Dashboard/Exporter (atomar, alle STATE_INTERVAL s)."""
        try:
            seen = self._seen_from_can
            def confirmed(addr):
                if addr in seen:
                    return True
                return (addr - 1) in seen and (self.regmap.by_reg.get(addr - 1, {}).get("type") or "").upper() in ("U32", "S32")
            stale = sorted(a for a in self._cache_regs if not confirmed(a))
            now = time.time()
            # --- HP-1: Alter je Register + Einfrier-Erkennung -------------------
            # `stale` oben heisst weiterhin nur "aus dem Warm-Cache, seit dem Start nie
            # bestaetigt". Das ist die ALTE, beim Start eingefrorene Frage. Neu ist
            # `frozen`: Register, die IM LAUFENDEN BETRIEB aufgehoert haben zu antworten.
            sweep = max(list(self._sweep_s.values()) + [float(getattr(self.args, "poll_interval", 30.0))])
            thresh = max(self.FROZEN_FACTOR * sweep, 120.0)
            ages = {str(a): round(now - ts, 1) for a, ts in seen.items()}
            # Das zweite Wort eines 32-Bit-Wertes wird unter der HIGH-Adresse dekodiert
            # und nie eigenstaendig gestempelt. Es ist aber genauso frisch. Ohne diesen
            # Zusatz erschienen 1506 (zu 1505) und 27489 (zu 27488) faelschlich als "nie
            # gesehen" -- dieselbe Falle, die confirmed() oben schon beruecksichtigt.
            for a, ts in list(seen.items()):
                if (self.regmap.by_reg.get(a, {}).get("type") or "").upper() in ("U32", "S32"):
                    if (a + 1) in self.regmap.by_reg and str(a + 1) not in ages:
                        ages[str(a + 1)] = round(now - ts, 1)
            frozen = sorted(int(a) for a, age in ages.items() if age > thresh)
            # HP-1, dritter Fall: gepollt, aber seit dem Start NIE beantwortet.
            # Faengt die Register, die aus stale und frozen herausfallen.
            never = sorted(a for a in self._poll_regs if str(a) not in ages)
            st = {"ts": now, "start": self._t0, "cache_loaded": self._cache_loaded,
                  "cache_age_s": int(self._cache_age), "stale": len(stale), "stale_regs": stale[:50],
                  "seen_can": len(seen), "rx": self.rx_count, "dec": self.dec_count, "err": self.err_count,
                  # HP-1
                  "sweep_s": {k: round(v, 1) for k, v in self._sweep_s.items()},
                  "frozen_threshold_s": round(thresh, 1),
                  "frozen": len(frozen), "frozen_regs": frozen[:100],
                  "polled": len(self._poll_regs),
                  "never": len(never), "never_regs": never[:100],
                  "reg_age_s": ages}
            tmp = STATE_FILE + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(st, f)
            os.replace(tmp, STATE_FILE)
        except Exception as e:
            log.debug("state-write: %s", e)

    def cache_loop(self):
        self.write_state()
        n = 0
        while True:
            time.sleep(STATE_INTERVAL)
            n += 1
            if n % max(1, int(CACHE_INTERVAL // STATE_INTERVAL)) == 0:
                self.save_cache()
            self.write_state()

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
            elif r["unit_id"] in WEZ_UNITS:
                # weiterer Waermeerzeuger (WEZ 2..16) am selben Bus: nur LESEN, GET an seinen Knoten
                wez.append((poll_arb(r["unit_id"]), r))
            elif r["unit_id"] == 520:
                # ALLE Lueftungs-Register pollen, nicht nur fg=50 (Betriebswerte).
                # fg=0 enthaelt u.a. Wartungs-/Filterzaehler (28934-28946) und den
                # Fehlerspeicher (24150-24194); die blieben sonst dauerhaft leer.
                # Aufwand unkritisch: ~72 statt 13 Register = 7 s je 30-s-Zyklus.
                hv.append((ARB_HV_POLL, r))
        # HP-1: Sollzustand festhalten -- welche Register FRAGEN wir ueberhaupt ab?
        # Ohne diese Menge faellt ein Register, das die Anlage ueberhaupt nicht
        # beantwortet, nach zwei Neustarts aus JEDEM Netz: es ist dann weder `stale`
        # (nicht mehr im Warm-Cache, weil save_cache nur Bestaetigtes sichert) noch
        # `frozen` (nie einen Zeitstempel bekommen) -- es verschwindet einfach.
        # Genau das passiert mit 25613/25614/27467.
        for _arb, _r in (wez + hv):
            for _r2 in self.regmap.by_dp.get((_r["fg"], _r["fn"], _r["dp"]), []):
                self._poll_regs.add(_r2["reg"])
        return wez, hv

    def poll_targets(self, targets, interval, label="poll"):
        import can
        while True:
            t0 = time.time()
            for arb, r in targets:
                payload = bytes([0x01, OP_GET, r["fg"] & 0xFF, r["fn"] & 0xFF,
                                 (r["dp"] >> 8) & 0xFF, r["dp"] & 0xFF])
                try:
                    self.send_msg(can.Message(arbitration_id=arb,
                                              data=payload, is_extended_id=True))
                except Exception as e:
                    log.debug("poll-send: %s", e)
                time.sleep(self.args.poll_delay)
            # HP-1: gemessene Dauer eines vollen Durchlaufs inkl. Pause. Das ist das
            # ECHTE Erwartungsintervall je Register -- NICHT --poll-interval, denn der
            # WEZ-Sweep allein dauert ~304 x poll_delay.
            self._sweep_s[label] = (time.time() - t0) + interval
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
            # 0) Nur Geraete mit geprueftem SET-Weg. Frueher ging jedes Nicht-520-Register
            #    ueber ARB_WRITE an Knoten 1 - ein Register der WP 2 haette WP 1 verstellt.
            if r.get("unit_id") not in WRITE_UNITS:
                log.warning("ABGELEHNT reg %d (%s): Schreiben auf UnitId %s nicht unterstuetzt (nur %s)",
                            reg, r.get("name"), r.get("unit_id"), sorted(WRITE_UNITS))
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
                # 0 = "keine Anforderung" ist fuer die Konstantanforderungs-Register gueltig (04.09.2026)
                if chk == 0 and reg in ZERO_OK_REGS:
                    pass
                elif not (mn <= chk <= mx):
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
                # HomeVent/Lueftung (UnitId 520) hoert auf ARB_HV_POLL auch fuer SET;
                # WEZ-Schreib-ID (ARB_WRITE) wuerde von der Lueftung ignoriert.
                self.send_msg(can.Message(arbitration_id=(ARB_HV_POLL if r.get("unit_id")==520 else ARB_WRITE),
                                          data=payload, is_extended_id=True))
                log.info("SET reg %d (%s) <- %s (raw)", reg, r.get("name"), v)
                # --- Kanal-Exklusion: aktiver Kanal (>0) nullt den Partner-Kanal ---
                partner = EXCL_PAIRS.get(reg)
                if partner is not None and chk > 0:
                    excl_last = getattr(self, "_excl_last", None)
                    if excl_last is None:
                        excl_last = self._excl_last = {}
                    if now - excl_last.get(partner, 0) >= EXCL_MIN_INTERVAL:
                        pr = self.regmap.by_reg.get(partner)
                        if pr is not None:
                            ptyp = (pr.get("type") or "").upper()
                            pdata = bytes([0]) if ptyp in ("U8", "S8", "LIST") else bytes([0, 0])
                            ppayload = bytes([0x01, OP_SET, pr["fg"] & 0xFF, pr["fn"] & 0xFF,
                                              (pr["dp"] >> 8) & 0xFF, pr["dp"] & 0xFF]) + pdata
                            try:
                                self.send_msg(can.Message(
                                    arbitration_id=(ARB_HV_POLL if pr.get("unit_id") == 520 else ARB_WRITE),
                                    data=ppayload, is_extended_id=True))
                                excl_last[partner] = now
                                self._last_write[partner] = now
                                log.info("EXKLUSION: reg %d aktiv (%s) -> Partner reg %d auf 0", reg, r.get("name"), partner)
                            except Exception as e:
                                log.error("exkl-send: %s", e)
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
        self.load_cache()
        threading.Thread(target=self.cache_loop, daemon=True).start()
        import signal
        def _on_term(signum, frame):
            n = self.save_cache()
            log.info("SIGTERM: Warm-Cache gesichert (%d Woerter), beende", n)
            raise SystemExit(0)
        try:
            signal.signal(signal.SIGTERM, _on_term)
        except Exception as e:
            log.debug("signal: %s", e)
        if not self.args.no_poll:
            wez, hv = self.build_targets()
            fastkeys = set()
            for _rg in FAST_REGS:
                _rr = self.regmap.by_reg.get(_rg)
                if _rr and _rr.get("fg") is not None and _rr.get("unit_id") == 1:
                    fastkeys.add((_rr["fg"], _rr["fn"], _rr["dp"]))
            fast = [(a, r) for (a, r) in wez
                    if (r["fg"], r["fn"], r["dp"]) in fastkeys]
            log.info("Poll: %d WEZ (alle %ss) + %d Lueftung (alle 5s) + %d Live (alle %ss)",
                     len(wez), self.args.poll_interval, len(hv),
                     len(fast), self.args.fast_interval)
            threading.Thread(target=self.poll_targets, args=(wez, self.args.poll_interval, "wez"), daemon=True).start()
            if hv:
                threading.Thread(target=self.poll_targets, args=(hv, 5.0, "hv"), daemon=True).start()
            if fast and self.args.fast_interval > 0:
                threading.Thread(target=self.poll_targets,
                                 args=(fast, self.args.fast_interval, "fast"), daemon=True).start()
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
    ap.add_argument("--fast-interval", type=float, default=5.0,
                    help="Pollintervall der Live-Register (FAST_REGS); 0 = aus")
    ap.add_argument("--no-poll", action="store_true")
    ap.add_argument("--enable-write", action="store_true",
                    help="erlaubt Modbus-FC6/16 -> CAN-SET (Schreiben auf die WP). Default AUS = nur lesen.")
    ap.add_argument("--no-sender-filter", dest="sender_filter", action="store_false",
                    help="Antworten wie vor 11/2026 nur ueber (fg,fn,dp) zuordnen, ohne Absender-Pruefung")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args()
    logging.basicConfig(level=args.log_level,
                        format="%(asctime)s %(levelname)s %(message)s")
    Bridge(args).run()

if __name__ == "__main__":
    main()
