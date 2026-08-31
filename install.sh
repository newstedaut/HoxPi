#!/bin/bash
# HoxPi-Installation auf Raspberry Pi (Debian 13 bzw. Raspberry Pi OS "Trixie", arm64)
# Als root ausfuehren: sudo bash install.sh          (interaktiv)
#                      sudo bash install.sh --yes    (alles automatisch, inkl. Grafana/MQTT)
# Getestet auf: Raspberry Pi 4 (2 GB), Debian 13, USB-CAN DSD-TECH SH-C30G
set -e
YES=0; [ "$1" = "--yes" ] && YES=1
cd "$(dirname "$0")"
HOME_ADM=/home/${SUDO_USER:-admin}
ADM=${SUDO_USER:-admin}

echo "=== HoxPi-Installation ==="
[ "$(id -u)" = "0" ] || { echo "Bitte mit sudo ausfuehren."; exit 1; }

echo "--- 0) Python-Version pruefen ---"
python3 - <<'PYEOF'
import sys
if sys.version_info < (3, 12):
    print(f"FEHLER: Python {sys.version.split()[0]} gefunden - HoxPi braucht Python 3.12+.")
    print("Raspberry Pi OS 'Bookworm' liefert nur 3.11 - bitte 'Trixie' (Debian 13) verwenden.")
    sys.exit(1)
print(f"OK: Python {sys.version.split()[0]}")
PYEOF

echo "--- 1) Pakete ---"
apt-get update
apt-get install -y python3 python3-can python3-pymodbus python3-openpyxl python3-qrcode python3-paho-mqtt can-utils curl

echo "--- 2) Hoval-Datenpunktliste ---"
XLSX=$(ls ./*.xlsx 2>/dev/null | head -1 || true)
if [ -z "$XLSX" ]; then
  echo "Keine xlsx gefunden. Bitte die offizielle Hoval-Datenpunktliste herunterladen"
  echo "  https://www.hoval.com/misc/TTE/TTE-GW-Modbus-datapoints.xlsx"
  echo "und neben install.sh legen (wird aus Urheberrechtsgruenden nicht mitgeliefert)."
  if [ "$YES" = "1" ]; then a=j; else read -r -p "Jetzt automatisch herunterladen? [j/N] " a; fi
  if [ "$a" = "j" ] || [ "$a" = "J" ]; then
    curl -fL -o TTE-GW-Modbus-datapoints.xlsx "https://www.hoval.com/misc/TTE/TTE-GW-Modbus-datapoints.xlsx"
    XLSX=./TTE-GW-Modbus-datapoints.xlsx
  else
    exit 1
  fi
fi
echo "Nutze: $XLSX"

echo "--- 3) Dateien installieren ---"
install -d -o "$ADM" /opt/hoxpi
python3 tools/gen_registers.py "$XLSX" "1,520,143" /opt/hoxpi/registers.json
python3 tools/gen_reg_texts.py "$XLSX" /opt/hoxpi/registers.json /opt/hoxpi/reg_texts.json
install -m 755 bridge/hoval_bridge.py /opt/hoxpi/
install -m 644 bridge/whitelist.example.json /opt/hoxpi/whitelist.json
install -m 755 dashboard/hoval_status.py /opt/hoxpi/
install -m 755 exporter/hoval_exporter.py /opt/hoxpi/
install -m 644 assistant/hoxpi_assistent.html /opt/hoxpi/ 2>/dev/null || true
# Die Skripte erwarten die Dateien unter /home/admin/hoval-bridge/ - Symlink setzen:
install -d "$HOME_ADM" 2>/dev/null || true
[ -e "$HOME_ADM/hoval-bridge" ] || ln -s /opt/hoxpi "$HOME_ADM/hoval-bridge"

echo "--- 3b) Zusatzfunktionen: Feature-Schalter, Keepalive, Waechter, Backup ---"
# Zentrale Feature-Schalter (auch im Dashboard: Sicherheit -> Funktionen)
[ -f "$HOME_ADM/hoxpi-features.json" ] || install -m 644 -o "$ADM" hoxpi-features.example.json "$HOME_ADM/hoxpi-features.json"
# Keepalive: haelt bei relais-freiem Betrieb die Eingaenge 30-046/057/066 = AUS (Bus statt Kontakt)
install -m 755 -o "$ADM" keepalive/hoval_keepalive.py "$HOME_ADM/hoval_keepalive.py"
# Stoerungs-Waechter + Verdichter-Kurzzyklus-Alarm (meldet an Home Assistant / Logdatei / Webhook)
install -m 755 -o "$ADM" watch/hoval_watch.py "$HOME_ADM/hoval_watch.py"
install -d -o "$ADM" "$HOME_ADM/hoval-watch"
# Naechtliches versioniertes Backup aller Skripte + Configs
install -m 755 -o "$ADM" backup/hoxpi_backup.sh "$HOME_ADM/hoxpi_backup.sh"
install -d -o "$ADM" "$HOME_ADM/hoxpi-backups"
# Cronjobs (User admin) idempotent eintragen:
TMPCRON=$(mktemp)
crontab -u "$ADM" -l 2>/dev/null | grep -vE "hoval_keepalive|hoval_watch|hoxpi_backup" > "$TMPCRON" || true
cat >> "$TMPCRON" <<CRONEOF
*/5 * * * * /usr/bin/python3 $HOME_ADM/hoval_keepalive.py >> /tmp/keepalive.log 2>&1
*/2 * * * * /usr/bin/python3 $HOME_ADM/hoval_watch.py >/dev/null 2>&1
17 3 * * * /bin/bash $HOME_ADM/hoxpi_backup.sh >> $HOME_ADM/hoxpi-backups/backup.log 2>&1
CRONEOF
crontab -u "$ADM" "$TMPCRON"; rm -f "$TMPCRON"
echo "Cronjobs fuer $ADM eingetragen (Keepalive */5, Waechter */2, Backup 03:17)."

echo "--- 4) CAN-Interface + Dienste ---"
install -m 644 systemd/can0.service /etc/systemd/system/ 2>/dev/null || true
install -m 644 systemd/hoval-bridge.service /etc/systemd/system/
install -m 644 systemd/hoval-status.service /etc/systemd/system/
install -m 644 systemd/hoval-exporter.service /etc/systemd/system/
install -m 644 avahi/hoxpi-device-info.service /etc/avahi/services/ 2>/dev/null || true
systemctl daemon-reload
systemctl enable --now can0 2>/dev/null || echo "can0.service pruefen (USB-CAN angesteckt?)"
systemctl enable --now hoval-bridge hoval-status hoval-exporter

echo "--- 4b) Optional: Home Assistant (MQTT-Auto-Discovery) ---"
if [ "$YES" = "1" ]; then a=j; else read -r -p "Home-Assistant-Anbindung per MQTT installieren (empfohlen, wenn HA genutzt wird)? [j/N] " a; fi
if [ "$a" = "j" ] || [ "$a" = "J" ]; then
  apt-get install -y mosquitto mosquitto-clients
  install -d -o "$ADM" "$HOME_ADM/hoval-mqtt"
  install -m 755 -o "$ADM" mqtt/hoval_mqtt.py "$HOME_ADM/hoval-mqtt/hoval_mqtt.py"
  install -m 644 systemd/hoval-mqtt.service /etc/systemd/system/
  systemctl daemon-reload
  systemctl enable --now mosquitto hoval-mqtt
  echo "In Home Assistant nur die MQTT-Integration auf diesen Broker zeigen lassen -"
  echo "alle Werte + Steuerung erscheinen automatisch (Geraet 'HoxPi Waermepumpe')."
else
  echo "Uebersprungen - spaeter jederzeit nachinstallierbar (oder im Dashboard abschaltbar)."
fi

echo "--- 5) Optional: Statistik (Prometheus + Grafana) ---"
if [ "$YES" = "1" ]; then a=j; else read -r -p "Grafana-Statistik installieren (ca. 150 MB)? [j/N] " a; fi
if [ "$a" = "j" ] || [ "$a" = "J" ]; then
  apt-get install -y --no-install-recommends prometheus
  install -m 644 prometheus/prometheus.yml /etc/prometheus/prometheus.yml
  grep -q retention /etc/default/prometheus 2>/dev/null || echo 'ARGS="--storage.tsdb.retention.time=400d"' >> /etc/default/prometheus
  mkdir -p /etc/apt/keyrings
  curl -fsSL https://apt.grafana.com/gpg.key | gpg --dearmor -o /etc/apt/keyrings/grafana.gpg
  echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" > /etc/apt/sources.list.d/grafana.list
  apt-get update && apt-get install -y grafana
  install -m 644 grafana/datasource-hoxpi.yaml /etc/grafana/provisioning/datasources/hoxpi.yaml
  install -m 644 grafana/dashboards-hoxpi.yaml /etc/grafana/provisioning/dashboards/hoxpi.yaml
  install -d -o grafana -g grafana /var/lib/grafana/dashboards
  install -m 644 -o grafana -g grafana grafana/dashboard-hoxpi.json /var/lib/grafana/dashboards/hoxpi.json
  mkdir -p /etc/systemd/system/grafana-server.service.d
  install -m 644 grafana/grafana-override.conf /etc/systemd/system/grafana-server.service.d/override.conf
  systemctl daemon-reload
  systemctl enable --now prometheus grafana-server
fi

echo "--- 6) Optional: KI-Schnittstelle (MCP-Server) ---"
if [ "$YES" = "1" ]; then a=j; else read -r -p "MCP-Server installieren (KI-Assistenten wie Claude koennen die Anlage inspizieren)? [j/N] " a; fi
if [ "$a" = "j" ] || [ "$a" = "J" ]; then
  python3 -m venv "$HOME_ADM/hoxpi-mcp-venv" 2>/dev/null || python3 -m venv /opt/hoxpi/mcp-venv
  VENV=$HOME_ADM/hoxpi-mcp-venv; [ -d "$VENV" ] || VENV=/opt/hoxpi/mcp-venv
  $VENV/bin/pip install --quiet mcp
  mkdir -p "$HOME_ADM/hoxpi-mcp"
  install -m 755 mcp/hoxpi_mcp.py "$HOME_ADM/hoxpi-mcp/"
  [ -f "$HOME_ADM/hoxpi-mcp/config.json" ] || echo '{"enable_write": false, "port": 8808}' > "$HOME_ADM/hoxpi-mcp/config.json"
  install -m 644 systemd/hoxpi-mcp.service /etc/systemd/system/
  systemctl daemon-reload
  systemctl enable --now hoxpi-mcp
fi

echo ""
echo "=== Fertig ==="
echo "Dashboard:   http://<pi-ip>/             (Uebersicht, Register, Integration)"
echo "Assistent:   Inbetriebnahme-Assistent im Dashboard bzw. assistant/hoxpi_assistent.html"
echo "Modbus-TCP:  <pi-ip>:502                 (offizielle Loxone-Hoval-Templates)"
echo "Grafana:     http://<pi-ip>:3000/d/hoxpi (falls installiert)"
echo ""
echo "Naechste Schritte:"
echo " 1. Dashboard oeffnen -> Seite Sicherheit -> 2FA einrichten (empfohlen):"
echo "    danach sind Schreibfreigaben + Feature-Schalter per Authenticator-Code geschuetzt."
echo " 2. Inbetriebnahme-Assistent durchlaufen -> passt hoxpi-features.json an die Anlage an"
echo "    (Heizkreise, relais-frei/klassisch, Home Assistant ja/nein)."
echo " 3. Seite Register: nur die Sollwert-Register freigeben, die Loxone/HA schreiben soll."
echo ""
echo "Nur im vertrauenswuerdigen Heimnetz betreiben."
