#!/usr/bin/env python3
"""can0-Waechter (HoxPi) - erkennt einen stillen CAN-Stall und heilt ihn selbst.

Anlass 29.09.2026: 17:51-19:24 war der USB-CAN-Adapter (gs_usb) stumm, RX und TX
eingefroren, ERROR-ACTIVE ohne Fehlerzaehler; Bridge warf ENOBUFS. Nur ein
Neuaufbau des Links (can0.service) half.

Schreibt NIE an die Anlage. Macht ausschliesslich lokal:
  Stufe 1: systemctl restart can0.service  (ip link down/up, 50 kbit/s)
  Stufe 2: gs_usb unbind/bind + Stufe 1   (nur wenn Stufe 1 nichts bringt)
  danach:  systemctl restart hoval-bridge, optionaler Hook, MQTT-Meldung
Bremsen: nach jeder Aktion 5 min Ruhe, hoechstens 6 Aktionen je 24 h.

Installation (optional, als root):
  install -m 755 tools/can0_watchdog.py /usr/local/sbin/can0_watchdog.py
  install -m 644 systemd/can0-watchdog.service /etc/systemd/system/
  systemctl daemon-reload && systemctl enable --now can0-watchdog
Umgebung (optional, z. B. per systemctl edit):
  HOXPI_CAN0_WD_LOG   Logdatei (Standard /var/log/can0_watchdog.log)
  HOXPI_CAN0_WD_HOOK  Shell-Befehl, der nach jeder Heilung laeuft (z. B. eigene Rekorder neu starten)
"""
import os, sys, time, subprocess, datetime, collections

NET = "/sys/class/net/can0"
RXF, TXF = NET + "/statistics/rx_packets", NET + "/statistics/tx_packets"
LOG = os.environ.get("HOXPI_CAN0_WD_LOG", "/var/log/can0_watchdog.log")
HOOK = os.environ.get("HOXPI_CAN0_WD_HOOK", "").strip()
TAKT = 5            # s Messintervall
STILL_RX = 60       # s ohne einen einzigen empfangenen Frame -> Stall
STILL_TX = 120      # s ohne gesendeten Frame (Bridge pollt dauernd) -> Stall
RUHE = 300          # s Sperrzeit nach einer Aktion
MAX_24H = 6


def log(msg):
    line = "%s %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg)
    print(line, flush=True)
    try:
        with open(LOG, "a") as f:
            f.write(line + "\n")
        os.chmod(LOG, 0o644)
    except Exception:
        pass


def cnt(f):
    try:
        return int(open(f).read().strip())
    except Exception:
        return None


def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    log("  $ %s -> rc=%d %s" % (cmd, r.returncode, (r.stdout + r.stderr).strip()[:160]))
    return r.returncode


def rx_delta(sec=10):
    a = cnt(RXF); time.sleep(sec); b = cnt(RXF)
    return (b - a) if (a is not None and b is not None) else 0


def usb_id():
    try:
        return os.path.basename(os.path.realpath(NET + "/device"))
    except Exception:
        return None


def heilen(grund):
    log("STALL erkannt: %s" % grund)
    dev = usb_id()
    log("Stufe 1: can0.service neu")
    sh("systemctl restart can0.service")
    time.sleep(4)
    d = rx_delta()
    log("  RX nach Stufe 1: %s Frames/10 s" % d)
    if d <= 0 and dev and os.path.exists("/sys/bus/usb/drivers/gs_usb"):
        log("Stufe 2: gs_usb %s neu binden" % dev)
        sh("echo %s > /sys/bus/usb/drivers/gs_usb/unbind" % dev)
        time.sleep(3)
        sh("echo %s > /sys/bus/usb/drivers/gs_usb/bind" % dev)
        time.sleep(4)
        sh("systemctl restart can0.service")
        time.sleep(4)
        d = rx_delta()
        log("  RX nach Stufe 2: %s Frames/10 s" % d)
    sh("systemctl restart hoval-bridge")
    time.sleep(5)
    # Optional: eigene Mitschreiber o. ae. sofort wiederbeleben (Befehl kommt aus der Umgebung)
    if HOOK:
        sh(HOOK)
    # Meldung per MQTT (Loxone/HA koennen darauf reagieren); Fehler egal
    sh("mosquitto_pub -h localhost -r -t hoxpi/can0_watchdog/letzte_heilung -m '%s %s' 2>/dev/null" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "ok" if d > 0 else "FEHLGESCHLAGEN"))
    log("ERGEBNIS: %s" % ("CAN wieder da" if d > 0 else "CAN weiter stumm - Hardware pruefen"))
    return d > 0


class Waechter:
    """Reine Entscheidungslogik, offline testbar."""
    def __init__(self):
        self.rx = self.tx = None
        self.rx_seit = self.tx_seit = None
        self.letzte_aktion = -1e9
        self.aktionen = collections.deque()

    def schritt(self, t, rx, tx):
        if rx is None or tx is None:          # Interface weg (z. B. USB weg)
            return "can0 fehlt"
        if self.rx is None or rx != self.rx:
            self.rx, self.rx_seit = rx, t
        if self.tx is None or tx != self.tx:
            self.tx, self.tx_seit = tx, t
        grund = None
        if t - self.rx_seit >= STILL_RX:
            grund = "RX steht seit %d s" % (t - self.rx_seit)
        elif t - self.tx_seit >= STILL_TX:
            grund = "TX steht seit %d s" % (t - self.tx_seit)
        if not grund:
            return None
        if t - self.letzte_aktion < RUHE:
            return None
        while self.aktionen and t - self.aktionen[0] > 86400:
            self.aktionen.popleft()
        if len(self.aktionen) >= MAX_24H:
            return "BREMSE:" + grund
        self.letzte_aktion = t
        self.aktionen.append(t)
        return grund

    def nach_aktion(self, t):
        self.rx = self.tx = None


def main():
    w = Waechter()
    log("can0-Waechter gestartet (RX-Stall %d s, TX-Stall %d s, Ruhe %d s, max %d/24h)" % (STILL_RX, STILL_TX, RUHE, MAX_24H))
    gebremst_gemeldet = 0
    while True:
        t = time.monotonic()
        r = w.schritt(t, cnt(RXF), cnt(TXF))
        if r == "can0 fehlt":
            if t - w.letzte_aktion >= RUHE:
                w.letzte_aktion = t; w.aktionen.append(t)
                heilen("Interface can0 fehlt"); w.nach_aktion(time.monotonic())
        elif r and r.startswith("BREMSE:"):
            if t - gebremst_gemeldet > 3600:
                log("BREMSE aktiv (%d Aktionen in 24 h) - keine weitere Aktion: %s" % (MAX_24H, r[7:]))
                gebremst_gemeldet = t
        elif r:
            heilen(r)
            w.nach_aktion(time.monotonic())
        time.sleep(TAKT)


if __name__ == "__main__":
    main()
