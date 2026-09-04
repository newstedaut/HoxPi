# HoxPi — Installationsanleitung (von der leeren SD-Karte bis zum laufenden Dashboard)

HoxPi macht aus einem Raspberry Pi ein **offenes Hoval-Modbus-TCP-Gateway**: Er liest den
Hoval-CAN-Bus (TopTronic E) mit und stellt alle Register per Modbus-TCP (Port 502) bereit —
so wie das originale, kostenpflichtige Hoval-Gateway. Loxone und Home Assistant binden sich
1:1 an. Zusätzlich: Dashboard, Störungs-Wächter, Backup, Home-Assistant-Auto-Discovery und
der **Inbetriebnahme-Assistent**.

## ⚡ Schnellstart (empfohlen)

Wer nicht alles von Hand machen will: Abschnitte **1–3** (Hardware, OS, SSH) erledigen, dann übernimmt `install.sh` den Rest — Pakete, CAN-Dienst, Registerlisten, alle Dienste, Wächter, Backup, Cronjobs, optional Home Assistant/Grafana/MCP:

```bash
git clone https://github.com/newstedaut/HoxPi.git && cd HoxPi
bash install.sh --dry-run     # Trockenlauf: prüft Python/CAN-Adapter/Dateien und zeigt nur, was passieren würde
sudo bash install.sh          # interaktiv — fragt bei jedem optionalen Teil nach
# oder: sudo bash install.sh --yes   (alles automatisch)
```

`--dry-run` braucht kein root und ändert nichts. Bricht die Installation ab, nennt sie den Schritt — das Skript ist idempotent und kann nach der Korrektur einfach erneut gestartet werden (bestehende `whitelist.json`/`hoxpi-features.json` bleiben erhalten).

Danach weiter bei Abschnitt **7** (2FA) und **8** (Inbetriebnahme-Assistent). Die Abschnitte 4–6 unten beschreiben, was install.sh im Detail tut — nützlich zum Verstehen und für Sonderfälle.

> Diese Anleitung beschreibt den Nachbau. Alle fertigen Skripte/Configs liegen im Repo bzw.
> im jüngsten Backup (`Heizung/HoxPi-Backups/hoxpi_*.tar.gz`).

---

## 1 · Hardware (Einkaufsliste)

| Teil | Hinweis |
|---|---|
| **Raspberry Pi 4** (2 GB reichen) | Auch Pi 5 / Pi 3B+ möglich |
| **USB-CAN-Adapter** | candleLight/gs_usb-kompatibel (z. B. DSD-TECH SH-C30G). Meldet sich als `1d50:606f Geschwister Schneider CAN adapter`. |
| **microSD-Karte** | ab 16 GB, besser 32 GB |
| **Stromversorgung** | USB-Netzteil **5 V / 3 A**, oder PoE-Splitter (5 V/≥3 A) am Netzwerkkabel |
| Gehäuse | passend für Pi 4 |
| 3 Adern | für den CAN-Abgriff am Hoval WEZ-Modul |

**CAN-Verkabelung (passiv & parallel — bestehender Bus läuft unverändert weiter):**
- Abgriff am Hoval **WEZ-Modul**, Klemme **„+ ⏚ H L"** (der echte TopTronic-E-CAN, 50 kbit/s, 64 Ω terminiert).
- **H, L, ⏚** parallel mit aufklemmen. ⚠ **Aderfarben bitte an der eigenen Anlage prüfen** — sie sind nicht überall gleich.
- **Nicht** an Klemme X4 anschließen — das ist RS485 (Innen- ↔ Außeneinheit, WFA-201 Klemmen 130/131/132 ↔ WFA-200, Hoval-Schema Blatt 5), kein CAN. Der TopTronic-CAN liegt nur am WEZ-Modul.

---

## 2 · Betriebssystem aufspielen

1. **Raspberry Pi Imager** (raspberrypi.com/software) → **Raspberry Pi OS Lite (64-bit)**.
2. Vor dem Schreiben im Imager (Zahnrad): **Hostname** `hoxpi`, **SSH aktivieren**, **Benutzer** `admin` + Passwort, **WLAN/LAN** nach Bedarf.
3. SD einlegen, Pi starten, per SSH verbinden: `ssh admin@hoxpi` (bzw. IP).
4. Aktualisieren:
   ```bash
   sudo apt update && sudo apt full-upgrade -y
   sudo apt install -y python3-venv python3-pip can-utils mosquitto mosquitto-clients git
   ```

---

## 3 · CAN-Schnittstelle (can0) einrichten

Der gs_usb-Adapter wird vom Kernel automatisch als `can0` erkannt. Bitrate **50000** setzen —
als systemd-Dienst, damit es nach jedem Neustart automatisch hochkommt:

`/etc/systemd/system/can0.service`:
```ini
[Unit]
Description=Hoval CAN (can0) 50 kbit/s
After=network.target
[Service]
Type=oneshot
RemainAfterExit=yes
ExecStartPre=/bin/sh -c 'for i in 1 2 3 4 5; do ip link show can0 && break || sleep 2; done'
ExecStart=/sbin/ip link set can0 up type can bitrate 50000
ExecStop=/sbin/ip link set can0 down
[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl enable --now can0.service
candump can0   # Test: es müssen Frames durchlaufen (mit Strg+C beenden)
```

---

## 4 · Python-Umgebung + Programme

Virtuelle Umgebung für die Bridge (hält Abhängigkeiten sauber):
```bash
python3 -m venv ~/hoval-bridge-venv
~/hoval-bridge-venv/bin/pip install python-can pymodbus pyserial
# für den MQTT-Dienst nutzt das System-Python paho:
sudo apt install -y python3-paho-mqtt
```
Getestete Stände: Debian 13, Python 3.13, python-can 4.6.1, pymodbus 3.6.9, pyserial 3.5.
> ⚠ **Python 3.12 oder neuer erforderlich** (das Dashboard nutzt moderne f-strings / PEP 701). Raspberry Pi OS „Bookworm" liefert 3.11 — dann Raspberry Pi OS „Trixie" (Debian 13) nehmen oder Python 3.12+ nachinstallieren.

**Programme ablegen** (aus Repo/Backup entpacken). Standard-Ablage:
| Programm | Pfad | läuft mit |
|---|---|---|
| Bridge (CAN↔Modbus-TCP) | `~/hoval-bridge/hoval_bridge.py` (+ `registers.json`, `whitelist.json`) | venv-Python, `--enable-write` |
| Dashboard (Port 80) | `/usr/local/bin/hoval_status.py` | venv-Python |
| MQTT/Home-Assistant | `~/hoval-mqtt/hoval_mqtt.py` | System-Python |
| Prometheus-Exporter (:9101) | `~/hoval-exporter/hoval_exporter.py` | System-Python |
| Keepalive | `~/hoval_keepalive.py` | venv-Python (Cron) |
| Störungs-Wächter | `~/hoval_watch.py` | System-Python (Cron) |
| Backup | `~/hoxpi_backup.sh` | bash (Cron) |
| Feature-Schalter | `~/hoxpi-features.json` | von allen gelesen |

> ⚠ **Wichtig beim Warten:** Der Dienst führt genau den Pfad aus der jeweiligen `.service`-Datei aus
> (`systemctl cat <dienst> | grep ExecStart`). Es gibt teils gleichnamige Kopien im Home-Verzeichnis —
> **immer die Datei patchen, die der Dienst wirklich startet**, sonst wirkt die Änderung nicht.

---

## 5 · systemd-Dienste

Je Programm eine Unit unter `/etc/systemd/system/`. Muster (Bridge):
```ini
[Unit]
Description=Hoval CAN <-> Modbus-TCP Bridge (fuer Loxone)
After=network-online.target can0.service
Wants=network-online.target can0.service
[Service]
Type=simple
ExecStart=/home/admin/hoval-bridge-venv/bin/python /home/admin/hoval-bridge/hoval_bridge.py --enable-write
Restart=on-failure
RestartSec=5
User=root
[Install]
WantedBy=multi-user.target
```
Analog: `hoval-status` (Port 80 → root), `hoval-mqtt`, `hoval-exporter`. Dann:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now hoval-bridge hoval-status hoval-mqtt hoval-exporter
```

**Cronjobs** (`crontab -e`, User admin):
```cron
*/5  * * * * /usr/bin/python3 /home/admin/hoxpi_fulllog.py >/dev/null 2>&1
*/5  * * * * /home/admin/hoval-bridge-venv/bin/python /home/admin/hoval_keepalive.py >> /tmp/keepalive.log 2>&1
*/2  * * * * /usr/bin/python3 /home/admin/hoval_watch.py >/dev/null 2>&1
17 3 * * *   /bin/bash /home/admin/hoxpi_backup.sh >> /home/admin/hoxpi-backups/backup.log 2>&1
```
(dazu optional: Takte-Tagesbilanz, Discovery-Scanner, RS485-Watchdog — je nach Ausbau.)

---

## 6 · Erste Kontrolle

```bash
systemctl is-active can0 hoval-bridge hoval-status hoval-mqtt hoval-exporter   # alles "active"
```
Im Browser **`http://<pi-ip>/`** öffnen → das HoxPi-Dashboard erscheint (Start, Live-Werte,
Register, Integration, Sicherheit).

---

## 7 · Sicherheit / 2FA einrichten (empfohlen)

Das Dashboard ist nur im Heimnetz erreichbar. Wer Schreib-Aktionen (Register-Freigaben,
Feature-Schalter) zusätzlich schützen will:

1. Dashboard → Seite **Sicherheit**.
2. **2FA einrichten** → QR-Code mit einer Authenticator-App (Google Authenticator, Aegis …) scannen, Code bestätigen.
3. Danach verlangen alle Schreib-Aktionen einmalig den 6-stelligen Code.
   Handy verloren? `sudo rm ~/hoval-bridge/auth.json` auf dem Pi + Dashboard-Dienst neu starten → Schutz zurückgesetzt.

Ohne 2FA funktioniert alles genauso — der Schutz ist dann „nur" das lokale Heimnetz.

---

## 8 · Anlage anbinden (Inbetriebnahme-Assistent)

Jetzt kommt der **Inbetriebnahme-Assistent** — im Dashboard auf der Seite **Assistent**
(`http://<pi-ip>/assistent`). Er fragt Heizkreise, Steuerungsart (relais-frei über Bus /
klassisch über Kontakt / nur lesen), Home-Assistant-Nutzung und Extras ab und erzeugt die
passende **`hoxpi-features.json`**. Am Ende schreibt der Knopf **„Auf diesem HoxPi übernehmen"**
die Konfiguration direkt auf den Pi (bei aktiver 2FA nur mit Anmeldung). Die Datei
`assistant/hoxpi_assistent.html` lässt sich auch offline im Browser öffnen — dann reiner
Trockentest, es wird nichts geschrieben. Reihenfolge:

1. **Loxone/HA anbinden:** Modbus-TCP-Gerät (IP des Pi, Port 502) anlegen; Hoval-Templates aus
   der Loxone Library laden. Bei Home Assistant genügt die MQTT-Integration (Auto-Discovery).
2. **Schreibrechte:** auf der Seite **Register** die Sollwert-Register freigeben, die Loxone/HA
   schreiben soll (z. B. 1490/19482 Vorlauf-Soll, Betriebswahl, SG-Offsets).
3. **Assistent durchlaufen** → erzeugte `hoxpi-features.json` übernehmen (Feature-Schalter auf
   der Seite Sicherheit → Funktionen; einzeln jederzeit umschaltbar).
4. **Relais-frei (falls gewählt):** Keepalive hält die Eingänge 30-046/057/066 = AUS → das
   unveränderte Hoval-Template steuert Heizen/Kühlen kontaktlos.

---

## 9 · Kurz-Referenz

- Dashboard: `http://<pi>/` · Modbus-TCP: `<pi>:502` (FC 3 lesen / FC 6 schreiben)
- Exporter: `<pi>:9101/metrics` · MQTT-Broker: `<pi>:1883`
- Alle Funktionen an/aus: Dashboard → **Sicherheit → Funktionen**
- Backups: `~/hoxpi-backups/` (nächtlich) + Off-Device-Kopie
- Dienst-Logs: `journalctl -u <dienst>` · Wächter-Alarme: `~/hoval-watch/alerts.log`

**HoxPi ist ein unabhängiges Open-Source-Projekt, nicht mit der Hoval AG verbunden.**
