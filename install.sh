#!/bin/bash
# HoxPi-Installation auf Raspberry Pi (Debian 12/13 bzw. Raspberry Pi OS, arm64)
# Als root ausfuehren: sudo bash install.sh          (interaktiv)
#                      sudo bash install.sh --yes    (alles automatisch, inkl. Grafana)
# Getestet auf: Raspberry Pi 4 (2 GB), Debian 13, USB-CAN DSD-TECH SH-C30G
set -e
YES=0; [ "$1" = "--yes" ] && YES=1
cd "$(dirname "$0")"

echo "=== HoxPi-Installation ==="
[ "$(id -u)" = "0" ] || { echo "Bitte mit sudo ausfuehren."; exit 1; }

echo "--- 1) Pakete ---"
apt-get update
apt-get install -y python3 python3-can python3-pymodbus python3-openpyxl python3-qrcode can-utils curl

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
install -d -o "${SUDO_USER:-admin}" /opt/hoxpi
python3 tools/gen_registers.py "$XLSX" "1,520,143" /opt/hoxpi/registers.json
python3 tools/gen_reg_texts.py "$XLSX" /opt/hoxpi/registers.json /opt/hoxpi/reg_texts.json
install -m 755 bridge/hoval_bridge.py /opt/hoxpi/
install -m 644 bridge/whitelist.example.json /opt/hoxpi/whitelist.json
install -m 755 dashboard/hoval_status.py /opt/hoxpi/
install -m 755 exporter/hoval_exporter.py /opt/hoxpi/
[ -f mqtt/hoval_mqtt.py ] && install -m 755 mqtt/hoval_mqtt.py /opt/hoxpi/ || true
# Hinweis: Die Skripte erwarten die Dateien unter /home/admin/hoval-bridge/ -
# fuer /opt/hoxpi einen Symlink setzen (kompatibel zur Referenzinstallation):
install -d /home/admin 2>/dev/null || true
[ -e /home/admin/hoval-bridge ] || ln -s /opt/hoxpi /home/admin/hoval-bridge

echo "--- 4) CAN-Interface + Dienste ---"
install -m 644 systemd/can0.service /etc/systemd/system/ 2>/dev/null || true
install -m 644 systemd/hoval-bridge.service /etc/systemd/system/
install -m 644 systemd/hoval-status.service /etc/systemd/system/
install -m 644 systemd/hoval-exporter.service /etc/systemd/system/
install -m 644 avahi/hoxpi-device-info.service /etc/avahi/services/ 2>/dev/null || true
systemctl daemon-reload
systemctl enable --now can0 2>/dev/null || echo "can0.service pruefen (USB-CAN angesteckt?)"
systemctl enable --now hoval-bridge hoval-status hoval-exporter

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

echo ""
echo "=== Fertig ==="
echo "Dashboard:  http://<pi-ip>/            (Uebersicht, Register, Integration)"
echo "Modbus-TCP: <pi-ip>:502                (offizielle Loxone-Hoval-Templates)"
echo "Grafana:    http://<pi-ip>:3000/d/hoxpi (falls installiert)"
echo ""
echo "WICHTIG: Nur im vertrauenswuerdigen Heimnetz betreiben - das Dashboard hat"
echo "keine Anmeldung. Schreibzugriffe sind ab Werk auf eine kleine, gepruefte"
echo "Whitelist beschraenkt (Seite 'Register')."
