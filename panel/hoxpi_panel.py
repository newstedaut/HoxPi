#!/usr/bin/env python3
"""HoxPi panel daemon - registers the Pi as an additional operating panel on the TopTronic(R) E CAN bus.

Feeds the web page /display (dashboard/display_module.py) with live values and, if explicitly enabled,
lets a small whitelist of room setpoints be changed. Not affiliated with Hoval AG.

Safety rules:
  1. Default is DRY ("modus": "trocken"): nothing at all is sent on CAN. Live mode must be set in config.json.
  2. Address-collision guard: a heartbeat on our own panel address that is not ours switches the daemon
     to passive at once (emergency stop, unlock only via the 'unlock' command).
  3. Night lock 23:00-07:00: cyclic frames only with "nachts_senden": true, writes only with "nachts_schreiben": true.
  4. Writes: off by default ("schreiben_erlaubt": false), need a non-empty code from config.json, a hard
     whitelist (room setpoints 03-051/03-053/03-054 of HK1) and are read back with 0x40 GET.
  5. 0x44 (subscribe) is OFF by default ("abo_0x44": false) - on TopTronic E a subscription can freeze a
     datapoint until the controller restarts.
  6. Audit log of every write attempt (audit_writes.log).

Files live in HOXPI_PANEL_DIR (default /home/admin/hoxpi_panel): config.json, status.json, page_values.json,
cmd.json/cmd_result.json (command exchange with the dashboard), panel.log, audit_writes.log.
"""
import errno, json, os, time, datetime, threading
import can

BASE = os.environ.get("HOXPI_PANEL_DIR", "/home/admin/hoxpi_panel")
CFG_F = os.path.join(BASE, "config.json")
STAT_F = os.path.join(BASE, "status.json")
CMD_F = os.path.join(BASE, "cmd.json")
CMD_RES_F = os.path.join(BASE, "cmd_result.json")
VAL_F = os.path.join(BASE, "page_values.json")
SEED_F = os.path.join(BASE, "page_values_seed.json")
LOG_F = os.path.join(BASE, "panel.log")
AUDIT_LOG_F = os.path.join(BASE, "audit_writes.log")
CAN_CHANNEL = os.environ.get("HOXPI_CAN", "can0")

DEFAULT_CFG = {
    "modus": "trocken",          # "trocken" = send nothing, "live" = act as panel on the bus
    "adresse": 2,                # panel address 0..31 - must not be used by a real panel
    "fachmann_code": "",         # empty = writing impossible
    "schreiben_erlaubt": False,
    "fachmann_immer_aktiv": False,
    "nachts_senden": False,
    "nachts_schreiben": False,
    "abo_0x44": False,
    "active_page": "standard",
}

VALUES_SAVE_S = 30        # page_values.json at most every 30 s (SD card wear: file is ~150 kB)
RX_SILENT_REOPEN_S = 90   # no frame at all for this long -> reopen the CAN socket
MULTI_TIMEOUT_S = 0.25

# CAN-ID bases (address is shifted in at bit 15)
HB_BASE = 0x00E00FFF      # heartbeat 01 02
SYNC_BASE = 0x1FE00FFF    # sync 01 61
PANEL_BASE = 0x1FE00801   # panel communication (0x62, 0x44, 0x40, 0x46)

# Writable datapoints (fg, fn, dp) - room setpoints of HK1 only
SAFE_CAN_WRITES = {(1, 0, 3051), (1, 0, 3053), (1, 0, 3054), (1, 1, 3051), (1, 1, 3053), (1, 1, 3054)}

# Menu pages (fg, fn, dp, label, unit, decimals). Labels as shown on the panel of one UltraSource B
# installation; entries marked "?" are not confirmed.
PAGES_CATALOG = {
    "standard": [
        (0, 0, 0, "Außentemperatur AF1", "°C", 1),
        (3, 0, 96, "Vorlauftemperatur WP", "°C", 1),
        (60, 254, 29, "Rücklauftemperatur WP", "°C", 1),
        (60, 254, 45, "Aktuelle Leistungszahl (COP)", "", 1),
        (2, 0, 4, "Warmwasserspeicher oben (SF)", "°C", 1),
        (2, 0, 6, "Warmwasserspeicher unten (SF2)", "°C", 1),
        (1, 0, 3051, "03-051 Normal-Raumtemperatur Heizen", "°C", 1),
        (1, 0, 3053, "03-053 Spar-Raumtemperatur Heizen", "°C", 1),
        (1, 0, 3050, "03-050 Betriebswahl Heizung (4 = Konstant)", "code", 0),
    ],
    "fachmann_hk1": [
        (1, 0, 3051, "03-051 Normal-Raumtemperatur Heizen", "°C", 1),
        (1, 0, 3053, "03-053 Spar-Raumtemperatur Heizen", "°C", 1),
        (1, 0, 3012, "03-012 Heizkurve Fußpunkt", "°C", 1),
        (1, 0, 3013, "03-013 Heizkurve Steilheit ?", "", 2),
        (1, 0, 7008, "07-008 Vorlauf Maximaltemperatur", "°C", 1),
        (1, 0, 3001, "03-001 ?", "°C", 1),
        (1, 0, 7036, "07-036 Vorlauf-Soll Konstantanforderung Heizen", "°C", 1),
        (1, 0, 3032, "03-032 Regelstrategie (3 = Konstant)", "code", 0),
        (1, 0, 3050, "03-050 Betriebswahl Heizung", "code", 0),
    ],
    "fachmann_kuehlen": [
        (1, 0, 7044, "07-044 Vorlauf Minimaltemperatur Kühlen", "°C", 1),
        (1, 0, 3054, "03-054 Normal-Raumtemperatur Kühlen", "°C", 1),
        (1, 0, 3056, "03-056 Spar-Raumtemperatur Kühlen", "°C", 1),
        (1, 0, 3048, "03-048 ?", "°C", 1),
        (1, 0, 3043, "03-043 ?", "°C", 1),
        (1, 0, 7047, "07-047 Vorlauf-Soll Konstantanforderung Kühlen", "°C", 1),
        (1, 0, 7014, "07-014 Kühlbetrieb Freigabe", "code", 0),
    ],
    "fachmann_zuordnung": [
        (1, 0, 30045, "30-045 Zuo. Eingang Schaltmodemkontakt Heizen", "code", 0),
        (1, 0, 30046, "30-046 Zuo. Eingang ext. Konstantanforderung Heizen", "code", 0),
        (2, 0, 30050, "30-050 ?", "code", 0),
        (1, 0, 30056, "30-056 Zuo. Eingang Freigabekontakt Kühlen", "code", 0),
        (1, 0, 30057, "30-057 Zuo. Eingang ext. Konstantanforderung Kühlen", "code", 0),
        (1, 0, 30066, "30-066 Zuo. Eingang Umschaltung Heizen/Kühlen", "code", 0),
    ],
}


def now_s():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(msg):
    line = now_s() + " " + msg
    print(line, flush=True)
    try:
        with open(LOG_F, "a") as f:
            f.write(line + "\n")
        if os.path.getsize(LOG_F) > 2_000_000:
            os.replace(LOG_F, LOG_F + ".1")
    except Exception:
        pass


def audit_log(fg, fn, dp, val, old_val, user, status, verified_val=None):
    entry = f"[{now_s()}] SET fg={fg} fn={fn} dp={dp} val={val} (alt={old_val}) user={user} status={status}"
    if verified_val is not None:
        entry += f" readback={verified_val}"
    try:
        with open(AUDIT_LOG_F, "a") as f:
            f.write(entry + "\n")
    except Exception:
        pass
    log(f"AUDIT: {entry}")


def load_cfg():
    cfg = dict(DEFAULT_CFG)
    try:
        with open(CFG_F) as f:
            cfg.update(json.load(f))
    except FileNotFoundError:
        os.makedirs(BASE, exist_ok=True)
        try:
            with open(CFG_F, "w") as f:
                json.dump(cfg, f, indent=2)
        except Exception:
            pass
    except Exception as e:
        log(f"Warnung config.json: {e}")
    try:
        cfg["adresse"] = int(cfg.get("adresse", 2)) & 0x1F
    except (TypeError, ValueError):
        cfg["adresse"] = 2
    return cfg


def ids_for(addr):
    hb = HB_BASE | ((addr & 0x1F) << 15)
    sync = SYNC_BASE | ((addr & 0x1F) << 15)
    panel = PANEL_BASE | ((addr & 0x1F) << 15)
    return hb, sync, panel


def is_night():
    h = time.localtime().tm_hour
    return h >= 23 or h < 7


class SendBlocked(Exception):
    pass


class HoxPiPanelDaemon:
    def __init__(self):
        self.cfg = load_cfg()
        self.running = True
        self.bus = None
        self.bus_bad = False
        self.lock = threading.Lock()
        self.start = time.time()
        self.active_page = self.cfg.get("active_page", "standard")
        self.last_own_hb = 0
        self.last_rx = time.time()
        self.sync_seq = 1
        self.last_page_sub = 0
        self.values_dirty = False
        self.last_values_save = 0

        self.sent = {"hb": 0, "sync": 0, "sub": 0, "get": 0, "set": 0}
        self.tx_errors = 0
        self.reopens = 0
        self.seen = {}
        self.devices = {}
        self.page_values = {}
        self.metadata = {}
        self.multi_buf = {}
        self.locked_reason = None

        for path in (SEED_F, VAL_F):
            if not os.path.exists(path):
                continue
            try:
                with open(path, encoding="utf-8") as f:
                    for k, v in json.load(f).items():
                        if not isinstance(v, dict):
                            continue
                        old = self.page_values.get(k)
                        if not old or v.get("ts", 0) >= old.get("ts", 0):
                            if old and old.get("ascii") and not v.get("ascii"):
                                v["ascii"] = old["ascii"]
                            self.page_values[k] = v
            except Exception as e:
                log(f"Warnung {os.path.basename(path)}: {e}")

    # ---------------- Bus ----------------
    def open_bus(self):
        try:
            if self.bus is not None:
                try:
                    self.bus.shutdown()
                except Exception:
                    pass
            self.bus = can.Bus(channel=CAN_CHANNEL, interface="socketcan")
            self.bus_bad = False
            self.last_rx = time.time()
            log(f"CAN-Bus {CAN_CHANNEL} geöffnet (Modus: {self.cfg['modus']}, Adresse: {self.cfg['adresse']})")
            return True
        except Exception as e:
            self.bus_bad = True
            log(f"FEHLER: {CAN_CHANNEL} konnte nicht geöffnet werden: {e}")
            return False

    def may_send(self):
        """Central send gate: live mode, no emergency stop, night lock respected."""
        if self.cfg.get("modus") != "live":
            return False, "Modus trocken"
        if self.locked_reason:
            return False, self.locked_reason
        if is_night() and not self.cfg.get("nachts_senden", False):
            return False, "Nachtpause (23-07 Uhr)"
        if self.bus is None or self.bus_bad:
            return False, "CAN-Bus nicht bereit"
        return True, ""

    def send_frame(self, arb, data):
        ok, why = self.may_send()
        if not ok:
            raise SendBlocked(why)
        try:
            self.bus.send(can.Message(arbitration_id=arb, data=data, is_extended_id=True), timeout=0.5)
        except can.CanError as e:
            self.tx_errors += 1
            code = getattr(e, "error_code", None)
            if code in (errno.ENXIO, errno.ENODEV, errno.ENETDOWN) or "No such device" in str(e):
                # interface was removed/re-created (USB re-enumeration, can0 restart) -> socket is dead
                if not self.bus_bad:
                    log(f"CAN-Socket tot ({e}) - wird neu geöffnet")
                self.bus_bad = True
            raise

    # ---------------- RX ----------------
    def _store_payload(self, arb, payload, t):
        if len(payload) < 5:
            return
        op = payload[0]
        fg, fn = payload[1], payload[2]
        dp = (payload[3] << 8) | payload[4]
        val = payload[5:]
        is_hv = (arb & 0xFFFF) == 0x47FF
        if op == 0x42 and val:
            val_int = int.from_bytes(val, "big", signed=(len(val) in (2, 4))) if len(val) in (1, 2, 4) else None
            ascii_str = None
            clean_val = val.rstrip(b"\x00")
            if len(clean_val) >= 2 and all(32 <= b < 127 or b in (0xC4, 0xD6, 0xDC, 0xE4, 0xF6, 0xFC, 0xDF) for b in clean_val):
                try:
                    ascii_str = clean_val.decode("latin1")
                except Exception:
                    pass
            entry = {"fg": fg, "fn": fn, "dp": dp, "val": val_int,
                     "hex": " ".join(f"{b:02X}" for b in val), "ts": t}
            if ascii_str:
                entry["ascii"] = ascii_str
            if is_hv:
                self.page_values[f"HV_{fg}_{fn}_{dp}"] = dict(entry)
                if fg in (50, 61, 62, 90) or f"{fg}_{fn}_{dp}" not in self.page_values:
                    self.page_values[f"{fg}_{fn}_{dp}"] = entry
            else:
                self.page_values[f"{fg}_{fn}_{dp}"] = entry
            self.values_dirty = True
        elif op == 0x56:
            self.metadata[f"{fg}_{fn}_{dp}"] = " ".join(f"{b:02X}" for b in val)

    def rx_loop(self):
        while self.running:
            bus = self.bus
            if bus is None or self.bus_bad:
                time.sleep(0.5)
                continue
            try:
                msg = bus.recv(timeout=0.5)
            except Exception:
                time.sleep(0.5)
                continue
            if not msg:
                continue

            arb = msg.arbitration_id
            d = bytes(msg.data)
            t = time.time()
            self.last_rx = t

            with self.lock:
                dev = self.devices.setdefault(arb, {"n": 0, "last": t})
                dev["n"] += 1
                dev["last"] = t

                if (arb & 0x1FE00FFF) == HB_BASE:
                    addr = (arb >> 15) & 0x1F
                    # Rule 2: a heartbeat on our address that we did not send ourselves.
                    # python-can does not deliver our own frames, so anything within 0.35 s of our
                    # own heartbeat is tolerated (looped-back copy from another socket).
                    if addr == self.cfg.get("adresse", 2) and self.cfg.get("modus") == "live":
                        if self.last_own_hb == 0 or (t - self.last_own_hb > 0.35):
                            if not self.locked_reason:
                                self.locked_reason = f"Fremdes Lebenszeichen auf Adresse {addr} erkannt! Notabschaltung aktiv."
                                log(f"SICHERHEITSNOTABSCHALTUNG: {self.locked_reason}")
                    s = self.seen.setdefault(addr, {"hb_n": 0, "hb_last": 0})
                    s["hb_n"] += 1
                    s["hb_last"] = t

                elif d and d[0] == 0x01 and len(d) >= 6:
                    self._store_payload(arb, d[1:], t)

                elif (arb >> 20) in (0x1F4, 0x1F5) and len(d) >= 3:
                    self.multi_buf[(arb & 0xFFFFF, d[1])] = (t, arb, bytearray(d[2:]))

                elif (arb >> 24) in (0x1E, 0x1D, 0x1C, 0x1B, 0x1A) and len(d) >= 2:
                    mkey = (arb & 0xFFFFF, d[0])
                    if mkey in self.multi_buf:
                        ts0, arb0, buf = self.multi_buf[mkey]
                        if t - ts0 <= MULTI_TIMEOUT_S:
                            buf.extend(d[1:])
                            if ((arb >> 20) & 0x8) != 0:
                                self.multi_buf.pop(mkey, None)
                                payload = bytes(buf[:-2]) if len(buf) >= 2 else bytes(buf)
                                self._store_payload(arb0, payload, t)
                        else:
                            self.multi_buf.pop(mkey, None)

                if len(self.multi_buf) > 64:   # drop unfinished multi-frame transfers
                    for k in [k for k, v in self.multi_buf.items() if t - v[0] > MULTI_TIMEOUT_S]:
                        self.multi_buf.pop(k, None)

    # ---------------- Requests ----------------
    def target_id_for_fg(self, fg, dev=None):
        addr = self.cfg.get("adresse", 2) & 0x1F
        if dev == "HV" or (dev is None and fg in (50, 61, 62, 90)):
            return 0x1FE00A08 | (addr << 15)  # ventilation unit (TTE-HV 8)
        if dev == "BM" or (dev is None and fg in (80, 81, 82, 83, 91)):
            return 0x1FE00C00 | (addr << 15)  # operating panel module
        return 0x1FE00801 | (addr << 15)      # heat generator (TTE-WEZ 1)

    def _request(self, items):
        """items: list of (dev, fg, fn, dp). Optional 0x44 subscribe, then 0x40 GET. Returns count sent."""
        n = 0
        if self.cfg.get("abo_0x44", False):
            for dev, fg, fn, dp in items:
                try:
                    self.send_frame(self.target_id_for_fg(fg, dev), bytes([0x01, 0x44, fg, fn, (dp >> 8) & 0xFF, dp & 0xFF]))
                    self.sent["sub"] += 1
                    time.sleep(0.03)
                except SendBlocked:
                    return 0
                except Exception as e:
                    log(f"Fehler 0x44 ({dp}): {e}")
        for dev, fg, fn, dp in items:
            try:
                self.send_frame(self.target_id_for_fg(fg, dev), bytes([0x01, 0x40, fg, fn, (dp >> 8) & 0xFF, dp & 0xFF]))
                self.sent["get"] += 1
                n += 1
                time.sleep(0.04)
            except SendBlocked:
                break
            except Exception:
                pass
        self.last_page_sub = time.time()
        return n

    def subscribe_dps(self, keys):
        """Live request for a list of keys ([DEV_]fg_fn_dp), max. 50."""
        parsed = []
        for k in keys[:50]:
            try:
                parts = str(k).split("_")
                if len(parts) == 4 and parts[0] in ("HV", "WEZ", "BM"):
                    parsed.append((parts[0], int(parts[1]), int(parts[2]), int(parts[3])))
                elif len(parts) == 3:
                    parsed.append((None, int(parts[0]), int(parts[1]), int(parts[2])))
            except ValueError:
                continue
        if not parsed:
            return 0
        return self._request(parsed)

    def subscribe_page(self, page_name):
        items = PAGES_CATALOG.get(page_name, [])
        if not items:
            return 0
        return self._request([(None, fg, fn, dp) for fg, fn, dp, *_ in items])

    # ---------------- Write ----------------
    def set_datapoint(self, fg, fn, dp, val_int, code, user="web"):
        """0x46 SET with code check, night lock, whitelist and read-back."""
        cfg_code = str(self.cfg.get("fachmann_code", "")).strip()
        if not cfg_code or str(code).strip() != cfg_code:
            audit_log(fg, fn, dp, val_int, None, user, "ABGELEHNT_CODE")
            return False, "Ungültiger oder nicht eingerichteter Code", None
        if not self.cfg.get("schreiben_erlaubt", False):
            audit_log(fg, fn, dp, val_int, None, user, "ABGELEHNT_CONFIG_GESPERRT")
            return False, "Schreiben in config.json gesperrt (schreiben_erlaubt=false)", None
        if is_night() and not self.cfg.get("nachts_schreiben", False):
            audit_log(fg, fn, dp, val_int, None, user, "ABGELEHNT_NACHTSPERRE")
            return False, "Schreiben nachts gesperrt (23:00-07:00)", None
        if (fg, fn, dp) not in SAFE_CAN_WRITES:
            audit_log(fg, fn, dp, val_int, None, user, "ABGELEHNT_WHITELIST")
            return False, f"fg={fg} fn={fn} dp={dp} ist nicht in der Schreib-Whitelist", None
        ok, why = self.may_send()
        if not ok:
            audit_log(fg, fn, dp, val_int, None, user, "ABGELEHNT_" + why.replace(" ", "_"))
            return False, f"Senden nicht möglich: {why}", None

        key = f"{fg}_{fn}_{dp}"
        with self.lock:
            old_val = self.page_values.get(key, {}).get("val")
        _, _, panel_id = ids_for(self.cfg["adresse"])
        val_bytes = int(val_int).to_bytes(2, "big", signed=True)   # whitelist = S16 temperatures (x10)
        frame = bytes([0x01, 0x46, fg, fn, (dp >> 8) & 0xFF, dp & 0xFF]) + val_bytes
        log(f"SCHREIBEN (0x46): fg={fg} fn={fn} dp={dp} val={val_int} bytes={frame.hex()} auf {panel_id:08X}")
        try:
            t_set = time.time()
            self.send_frame(panel_id, frame)
            time.sleep(0.05)
            self.send_frame(panel_id, frame)
            self.sent["set"] += 1
            time.sleep(0.35)
            self.send_frame(panel_id, bytes([0x01, 0x40, fg, fn, (dp >> 8) & 0xFF, dp & 0xFF]))
            verified, readback_val = False, None
            while time.time() - t_set < 2.0:
                time.sleep(0.1)
                with self.lock:
                    entry = self.page_values.get(key)
                    if entry and entry.get("ts", 0) >= t_set:
                        readback_val = entry.get("val")
                        if readback_val == val_int:
                            verified = True
                            break
            audit_log(fg, fn, dp, val_int, old_val, user, "OK_VERIFIZIERT" if verified else "GESENDET_UNBESTAETIGT", readback_val)
            msg = f"SET gesendet für dp={dp} val={val_int}"
            if verified:
                msg += f" (Rücklesen bestätigt: {readback_val})"
            elif readback_val is not None:
                msg += f" (Rücklesewert abweichend: {readback_val})"
            else:
                msg += " (kein Rücklesewert)"
            return verified, msg, readback_val
        except Exception as e:
            log(f"Fehler beim Senden von 0x46: {e}")
            audit_log(fg, fn, dp, val_int, old_val, user, f"FEHLER_{e}")
            return False, str(e), None

    # ---------------- Commands from the dashboard ----------------
    def check_commands(self):
        if not os.path.exists(CMD_F):
            return
        try:
            with open(CMD_F) as f:
                cmd = json.load(f)
            os.remove(CMD_F)
        except Exception:
            return

        res = {"id": cmd.get("id", str(time.time())), "ok": False, "ts": now_s()}
        action = cmd.get("action")
        try:
            if action == "page":
                page = cmd.get("page", "standard")
                if page in PAGES_CATALOG:
                    self.active_page = page
                    res["count"] = self.subscribe_page(page)
                    res["ok"], res["page"] = True, page
                else:
                    res["error"] = f"Unbekannte Seite '{page}'"
            elif action == "subscribe_dps":
                res["count"] = self.subscribe_dps(cmd.get("keys", []))
                res["ok"] = True
            elif action == "reload_cfg":
                self.cfg = load_cfg()
                res["ok"] = True
            elif action == "unlock":
                self.locked_reason = None
                log("Notabschaltung manuell aufgehoben")
                res["ok"] = True
            elif action == "set":
                ok, msg, rb = self.set_datapoint(int(cmd.get("fg", 1)), int(cmd.get("fn", 0)), int(cmd.get("dp", 0)),
                                                 int(cmd.get("val", 0)), cmd.get("code", ""), cmd.get("user", "web"))
                res.update({"ok": ok, "message": msg, "readback": rb})
            else:
                res["error"] = f"Unbekannte Aktion '{action}'"
        except (TypeError, ValueError) as e:
            res["error"] = f"Ungültiger Befehl: {e}"
        try:
            tmp = CMD_RES_F + ".tmp"
            with open(tmp, "w") as f:
                json.dump(res, f)
            os.replace(tmp, CMD_RES_F)
        except Exception:
            pass

    # ---------------- TX loop ----------------
    def tx_loop(self):
        t0 = time.time()
        next_hb, next_sync, next_disp, next_sub = t0 + 1.0, t0 + 0.5, t0 + 2.0, t0 + 3.0
        last_cfg = 0
        next_reopen = 0
        while self.running:
            t = time.time()
            if t - last_cfg > 5:
                self.cfg = load_cfg()
                last_cfg = t

            # reopen a dead socket (ENXIO after can0 restart) or a silent bus
            if (self.bus_bad or t - self.last_rx > RX_SILENT_REOPEN_S) and t >= next_reopen:
                next_reopen = t + 10
                self.reopens += 1
                log("CAN-Socket wird neu geöffnet" + ("" if self.bus_bad else f" (seit {int(t - self.last_rx)} s kein Empfang)"))
                self.open_bus()

            self.check_commands()
            hb_id, sync_id, panel_id = ids_for(self.cfg["adresse"])
            live = self.may_send()[0]

            if t >= next_hb:
                next_hb = t + 5.0
                if live:
                    try:
                        self.send_frame(hb_id, bytes([0x01, 0x02]))
                        self.last_own_hb = time.time()
                        self.sent["hb"] += 1
                    except Exception as e:
                        log(f"HB-Fehler: {e}")
            if t >= next_sync:
                next_sync = t + 7.0
                if live:
                    try:
                        seq = self.sync_seq & 0xFF
                        self.sync_seq = (self.sync_seq + 1) if self.sync_seq < 250 else 1
                        self.send_frame(sync_id, bytes([0x01, 0x61, seq, 0xFF, 0xFF]))
                        self.sent["sync"] += 1
                    except Exception as e:
                        log(f"Sync-Fehler: {e}")
            if t >= next_disp:
                next_disp = t + 5.0
                if live:
                    try:
                        self.send_frame(panel_id, bytes([0x01, 0x62, 0x01, 0x02, 0x00]))
                    except Exception:
                        pass
            if t >= next_sub:
                next_sub = t + 20.0
                if live and self.active_page:
                    self.subscribe_page(self.active_page)
            time.sleep(0.15)

    # ---------------- Status loop ----------------
    def status_loop(self):
        while self.running:
            time.sleep(1.5)
            t = time.time()
            with self.lock:
                hb_id, sync_id, panel_id = ids_for(self.cfg["adresse"])
                panels = [{"adresse": a, "lebenszeichen": s["hb_n"], "zuletzt_s": round(t - s["hb_last"], 1),
                           "aktiv": bool(s["hb_last"] and t - s["hb_last"] < 15), "wir": a == self.cfg["adresse"]}
                          for a, s in sorted(self.seen.items())]
                devs = [{"id": f"{k:08X}", "n": v["n"], "zuletzt_s": round(t - v["last"], 1)}
                        for k, v in sorted(self.devices.items())]
                sendet, warum = self.may_send()
                st = {
                    "zeit": now_s(),
                    "laeuft_seit_s": int(t - self.start),
                    "modus": self.cfg["modus"],
                    "sendet": sendet,
                    "sendet_nicht_weil": warum,
                    "adresse": self.cfg["adresse"],
                    "hb_id": f"{hb_id:08X}", "sync_id": f"{sync_id:08X}", "panel_id": f"{panel_id:08X}",
                    "active_page": self.active_page,
                    "fachmann_immer_aktiv": bool(self.cfg.get("fachmann_immer_aktiv", False)),
                    "nachts_senden": bool(self.cfg.get("nachts_senden", False)),
                    "schreiben_erlaubt": bool(self.cfg.get("schreiben_erlaubt", False)),
                    "gesendet": dict(self.sent),
                    "sendefehler": self.tx_errors,
                    "neu_geoeffnet": self.reopens,
                    "letzter_empfang_s": round(t - self.last_rx, 1),
                    "gesperrt": self.locked_reason,
                    "bedienteile": panels,
                    "lebenszeichen_alle": devs[:10],
                    "anzahl_werte": len(self.page_values),
                }
                save_vals = self.values_dirty and t - self.last_values_save >= VALUES_SAVE_S
                vals = dict(self.page_values) if save_vals else None
                if save_vals:
                    self.values_dirty = False
                    self.last_values_save = t
            for path, data in ((STAT_F, st), (VAL_F, vals)):
                if data is None:
                    continue
                try:
                    tmp = path + ".tmp"
                    with open(tmp, "w") as f:
                        json.dump(data, f, indent=None if path == VAL_F else 1)
                    os.replace(tmp, path)
                except Exception:
                    pass

    def run(self):
        log("HoxPi-Bedienteil-Daemon startet...")
        os.makedirs(BASE, exist_ok=True)
        self.open_bus()   # on failure the tx loop retries every 10 s
        for fn in (self.rx_loop, self.tx_loop, self.status_loop):
            threading.Thread(target=fn, daemon=True).start()
        try:
            while self.running:
                time.sleep(1.0)
        except KeyboardInterrupt:
            log("Beende HoxPi-Bedienteil...")
            self.running = False
        return 0


if __name__ == "__main__":
    raise SystemExit(HoxPiPanelDaemon().run())
