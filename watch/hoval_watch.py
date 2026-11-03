#!/usr/bin/env python3
"""HoxPi Wächter — Störungs-Alerts + Verdichter-Kurzzyklus-Wächter.

Läuft per Cron (*/2 Min). Liest kuratierte Register der Bridge (127.0.0.1:502),
erkennt Störungen und Kurztakten und verteilt Alarme über mehrere Kanäle:
  - MQTT/Home Assistant (Auto-Discovery binary_sensor + Text-Sensor) — nur wenn
    in config.json aktiviert UND Broker erreichbar (HA-optional!)
  - Logdatei ~/hoval-watch/alerts.log (immer)
  - Optional Webhook (POST JSON) — wenn webhook_url in config.json gesetzt

De-Dup über Statusdatei: gemeldet wird nur bei ZUSTANDSWECHSEL (neue Störung
bzw. Entwarnung), nicht in jeder Runde. Transiente WP-Detailstörungen
(Hochdruck/Niederdruck/Inverter) erst nach 2 aufeinanderfolgenden Checks
(vermeidet Fehlalarme direkt nach Neustart/Abtauen).
"""
import json, os, socket, struct, time, urllib.request

BASE_DIR = os.path.expanduser("~/hoval-watch")
STATE_F  = os.path.join(BASE_DIR, "state.json")
CONF_F   = os.path.join(BASE_DIR, "config.json")
LOG_F    = os.path.join(BASE_DIR, "alerts.log")

DEFAULT_CONF = {
    "mqtt": True,                 # MQTT/HA-Alarme senden (False = HA nicht genutzt)
    "webhook_url": None,          # optional: POST-Ziel für Alarme
    "max_starts_per_h": 5,        # Verdichter: mehr Starts/h = Kurztakten
    "ww_delta_k": 10,             # WW gilt als "zu kalt", wenn Ist < Soll - delta
    "ww_hours": 4,                # ... und das länger als so viele Stunden
}

# WP-Detailstatus-Codes, die eine (persistente) Störung sind
WP_FAULT = {11: "Hochdruck-Störung", 12: "Niederdruck-Störung", 55: "Inverter-Störung"}
HK_ST    = {12: "Störung"}

def load_json(p, default):
    try:
        with open(p, encoding="utf-8") as f: return json.load(f)
    except Exception: return default

def save_json(p, obj):
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f: json.dump(obj, f)
    os.replace(tmp, p)

# ---------- Modbus ----------
def rd(addr, words=1):
    try:
        s = socket.create_connection(("127.0.0.1", 502), 3); s.settimeout(3)
        s.sendall(struct.pack(">HHHBBHH", 1, 0, 6, 1, 3, addr, words))
        r = s.recv(260); s.close()
        if not r or (r[7] & 0x80): return None
        return [struct.unpack(">H", r[9+2*i:11+2*i])[0] for i in range(words)]
    except Exception:
        return None

def r32(addr):
    w = rd(addr, 2)
    return None if not w or len(w) < 2 else (w[0] << 16) | w[1]

# ---------- Checks ----------
def collect_alerts(conf, state):
    """Gibt dict {alert_id: text} der AKTUELL aktiven Alarme zurück."""
    active = {}
    now = time.time()

    fc = rd(1534)
    if fc is not None and fc[0] not in (0, 255):
        _c = fc[0] + 1  # Hoval: code+1 = Klasse*64+Nr, W/B/E = Warnung/Blockierung/Verriegelung
        active["stoerung_fa"] = "Wärmeerzeuger meldet Fehler %s:%02d (Code %d)" % ("IWBE"[(_c >> 6) & 3], _c & 63, fc[0])

    for reg, label in ((1501, "HK1"), (1502, "HK2")):
        v = rd(reg)
        if v is not None and v[0] in HK_ST:
            active[f"stoerung_{label.lower()}"] = f"{label}: {HK_ST[v[0]]}"

    # WP-Detailstörung mit Persistenz (2 aufeinanderfolgende Checks)
    wp = rd(18723)
    persist = state.get("wp_last_fault")
    if wp is not None and wp[0] in WP_FAULT:
        code = wp[0]
        if persist == code:
            active["stoerung_wp"] = f"Wärmepumpe: {WP_FAULT[code]}"
        state["wp_last_fault"] = code   # beim nächsten Lauf ggf. bestätigt
    else:
        state["wp_last_fault"] = None

    # Verdichter-Kurzzyklus (Zaehler-/Reset-Schutz, Backlog Z3, 07.09.2026)
    MIN_SPAN_S = 600      # unter 10 min Fenster wird nicht bewertet
    MAX_RATE_H = 30.0     # mehr ist physikalisch unmoeglich -> Lesefehler
    RESET_RUNS = 5        # so oft muss ein Ruecksprung bestaetigt werden
    zyk = r32(1518)
    if zyk is not None:
        hist = state.get("cycles", [])
        hoch = state.get("cycles_max")
        if hoch is not None and zyk < hoch:
            # Ruecksprung: entweder Lesefehler oder echter Zaehlerreset.
            n = int(state.get("cycles_low_runs", 0)) + 1
            state["cycles_low_runs"] = n
            state["cycles"] = []
            if n >= RESET_RUNS:
                # bestaetigt -> neue Basis, Alarm bleibt fuer dieses Fenster aus
                state["cycles_max"] = zyk
                state["cycles_low_runs"] = 0
                state["cycles"] = [[now, zyk]]
        else:
            state["cycles_low_runs"] = 0
            state["cycles_max"] = zyk
            hist.append([now, zyk])
            hist = [e for e in hist if now - e[0] <= 3600]   # 60-Min-Fenster
            state["cycles"] = hist
            span_s = now - hist[0][0]
            if len(hist) >= 2 and span_s >= MIN_SPAN_S:
                starts = zyk - hist[0][1]
                span_h = span_s / 3600.0
                rate = starts / span_h
                if starts < 0 or rate > MAX_RATE_H:
                    state["cycles"] = [[now, zyk]]      # unplausibel -> neu ansetzen
                elif rate > conf["max_starts_per_h"] and starts >= conf["max_starts_per_h"]:
                    active["kurzzyklus"] = (f"Verdichter taktet kurz: {int(starts)} Starts "
                                            f"in {span_h*60:.0f} Min (~{rate:.1f}/h)")

    # Warmwasser-Fühler oben ungültig (06.09.2026: 05-076-Vorfall) – nach 5 min melden
    sf = rd(1500)
    if sf is not None and sf[0] in (-32768, 32768):
        since = state.get("sf_invalid_since") or now
        state["sf_invalid_since"] = since
        if now - since >= 300:
            active["ww_fuehler"] = ("Warmwasser-Fühler oben (SF) ungültig seit %.0f min – "
                                    "WW-Ladung nicht möglich (Funktionsapplikation 05-076 / Fühler prüfen)" % ((now-since)/60))
    else:
        state["sf_invalid_since"] = None

    # Warmwasser zu kalt über längere Zeit
    ist = rd(1500); soll = rd(1499)
    if ist and soll and ist[0] not in (-32768, 32768):
        ist_c, soll_c = ist[0]/10.0, soll[0]/10.0
        if ist_c < soll_c - conf["ww_delta_k"]:
            since = state.get("ww_cold_since") or now
            state["ww_cold_since"] = since
            if now - since >= conf["ww_hours"] * 3600:
                active["ww_kalt"] = (f"Warmwasser seit {(now-since)/3600:.1f} h zu kalt "
                                     f"({ist_c:.1f} statt {soll_c:.1f} °C)")
        else:
            state["ww_cold_since"] = None

    return active

# ---------- Dispatch ----------
def log(msg):
    os.makedirs(BASE_DIR, exist_ok=True)
    with open(LOG_F, "a", encoding="utf-8") as f:
        f.write(time.strftime("%F %T ") + msg + "\n")

def mqtt_publish(active):
    """binary_sensor + Text-Sensor via HA-Discovery; still nichts, wenn Broker weg."""
    try:
        import paho.mqtt.client as mqtt
    except Exception:
        return
    try:
        try: c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="hoxpi-watch")
        except Exception: c = mqtt.Client(client_id="hoxpi-watch")
        c.connect("127.0.0.1", 1883, 10)
        c.loop_start()
        dev = {"identifiers": ["hoxpi"], "name": "HoxPi Waermepumpe",
               "model": "CAN-Modbus-Bridge fuer Hoval(R) TTE", "manufacturer": "HoxPi"}
        c.publish("homeassistant/binary_sensor/hoxpi/alarm/config", json.dumps({
            "name": "Störung", "unique_id": "hoxpi_alarm", "device_class": "problem",
            "state_topic": "hoval/alarm/state", "availability_topic": "hoval/bridge/status",
            "device": dev}), retain=True)
        c.publish("homeassistant/sensor/hoxpi/alarm_text/config", json.dumps({
            "name": "Störungstext", "unique_id": "hoxpi_alarm_text", "icon": "mdi:alert",
            "state_topic": "hoval/alarm/text", "availability_topic": "hoval/bridge/status",
            "device": dev}), retain=True)
        c.publish("hoval/alarm/state", "ON" if active else "OFF", retain=True)
        info = c.publish("hoval/alarm/text", " · ".join(active.values()) if active else "OK", retain=True)
        try: info.wait_for_publish(3)
        except Exception: pass
        time.sleep(0.3)
        c.loop_stop(); c.disconnect()
    except Exception:
        pass

def webhook(url, changed, active):
    try:
        data = json.dumps({"geraet": "HoxPi", "geaendert": changed,
                           "aktiv": list(active.values())}).encode()
        req = urllib.request.Request(url, data=data,
                                     headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=8)
    except Exception:
        pass

# ---------- Main ----------
def main():
    os.makedirs(BASE_DIR, exist_ok=True)
    _feat = load_json("/home/admin/hoxpi-features.json", {})
    if not _feat.get("watch", {}).get("enabled", True):
        if _feat.get("mqtt_ha", {}).get("enabled", True):
            try: mqtt_publish({})
            except Exception: pass
        return
    conf = {**DEFAULT_CONF, **load_json(CONF_F, {})}
    if not os.path.exists(CONF_F):
        save_json(CONF_F, DEFAULT_CONF)   # beim ersten Lauf Default schreiben
    state = load_json(STATE_F, {})
    prev = set(state.get("active", []))

    active = collect_alerts(conf, state)
    now_ids = set(active.keys())

    neu   = now_ids - prev
    weg   = prev - now_ids
    changed = []
    for a in sorted(neu): changed.append("NEU: " + active[a]);            log("ALARM " + active[a])
    for a in sorted(weg): changed.append("Entwarnung: " + a);             log("ENTWARNUNG " + a)

    # State immer sichern
    state["active"] = sorted(now_ids)
    save_json(STATE_F, state)

    # Dispatch nur bei Änderung (MQTT-Status aber immer aktualisieren, ist billig)
    if conf.get("mqtt"): mqtt_publish(active)
    if changed and conf.get("webhook_url"): webhook(conf["webhook_url"], changed, active)

if __name__ == "__main__":
    main()
