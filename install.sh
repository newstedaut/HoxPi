#!/bin/bash
# HoxPi-Installation auf Raspberry Pi (Debian 13 bzw. Raspberry Pi OS "Trixie", arm64)
# Als root ausfuehren: sudo bash install.sh            (interaktiv)
#                      sudo bash install.sh --yes      (alles automatisch, inkl. Grafana/MQTT)
#                      bash install.sh --dry-run       (nur zeigen, was passieren wuerde - aendert NICHTS,
#                                                       braucht kein root; mit --yes kombinierbar)
# Getestet auf: Raspberry Pi 4 (2 GB), Debian 13, USB-CAN DSD-TECH SH-C30G
set -e
set -o pipefail

YES=0; DRY=0
for arg in "$@"; do
  case "$arg" in
    --yes|-y)      YES=1 ;;
    --dry-run|-n)  DRY=1 ;;
    -h|--help)
      sed -n '2,7p' "$0"; exit 0 ;;
    *) echo "Unbekannte Option: $arg  (erlaubt: --yes, --dry-run, --help)"; exit 2 ;;
  esac
done
cd "$(dirname "$0")"
HOME_ADM=/home/${SUDO_USER:-admin}
ADM=${SUDO_USER:-admin}
WARN=0

# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------
# run: fuehrt einen aendernden Befehl aus - im Trockenlauf wird er nur angezeigt.
run() {
  if [ "$DRY" = "1" ]; then
    printf '  [dry-run] %s\n' "$*"
  else
    "$@"
  fi
}
# ask: j/N-Frage; bei --yes automatisch ja, im Trockenlauf ebenfalls ja (zeigt den vollen Umfang)
ask() {
  if [ "$YES" = "1" ] || [ "$DRY" = "1" ]; then a=j; else read -r -p "$1 [j/N] " a; fi
  [ "$a" = "j" ] || [ "$a" = "J" ]
}
warn() { echo "WARNUNG: $*"; WARN=$((WARN+1)); }
die()  { echo "FEHLER: $*"; exit 1; }
# Bei einem unerwarteten Abbruch sagen, WO es geklemmt hat (statt stumm zu sterben)
STEP="Start"
trap 'rc=$?; [ $rc -ne 0 ] && echo "" && echo "ABBRUCH in Schritt \"$STEP\" (Exit $rc). Nichts weiter geaendert - Fehler oben beheben und install.sh erneut starten (ist idempotent)."' EXIT

echo "=== HoxPi-Installation ==="
[ "$DRY" = "1" ] && echo "*** TROCKENLAUF: es wird nichts installiert oder veraendert ***"
if [ "$(id -u)" != "0" ]; then
  [ "$DRY" = "1" ] || die "Bitte mit sudo ausfuehren (fuer den Trockenlauf: bash install.sh --dry-run)."
fi

# ---------------------------------------------------------------------------
# 0) Vorpruefungen (nur lesen - laufen auch im Trockenlauf komplett durch)
# ---------------------------------------------------------------------------
STEP="0) Vorpruefungen"
echo "--- 0) Vorpruefungen ---"

# 0a) Betriebssystem / Paketmanager
if ! command -v apt-get >/dev/null 2>&1; then
  die "apt-get nicht gefunden - install.sh ist fuer Debian/Raspberry Pi OS gedacht."
fi
if [ -r /etc/os-release ]; then
  . /etc/os-release
  echo "OS: ${PRETTY_NAME:-unbekannt} ($(uname -m))"
  case "${VERSION_ID:-0}" in
    13|1[4-9]) ;;
    12) warn "Debian 12 'Bookworm' erkannt - liefert Python 3.11, HoxPi braucht 3.12+ (Trixie empfohlen)." ;;
    *)  warn "Unbekannte Debian-Version '${VERSION_ID:-?}' - Installation ungetestet." ;;
  esac
fi
case "$(uname -m)" in
  aarch64|x86_64) ;;
  armv7l) warn "32-Bit-System (armv7l) - HoxPi ist auf arm64 getestet; python3-pymodbus kann fehlen." ;;
  *)      warn "Architektur $(uname -m) ungetestet." ;;
esac

# 0b) Python-Version
if ! command -v python3 >/dev/null 2>&1; then
  die "python3 nicht gefunden (apt-get install python3)."
fi
PYV=$(python3 -c 'import sys; print("%d.%d.%d" % sys.version_info[:3])')
if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)'; then
  echo "FEHLER: Python $PYV gefunden - HoxPi braucht Python 3.12+."
  echo "Raspberry Pi OS 'Bookworm' liefert nur 3.11 - bitte 'Trixie' (Debian 13) verwenden."
  exit 1
fi
echo "OK: Python $PYV"

# 0c) Alle Dateien da, die installiert werden? (schuetzt vor unvollstaendigem Download/Clone)
MISSING=""
for f in tools/gen_registers.py tools/gen_reg_texts.py bridge/hoval_bridge.py bridge/whitelist.example.json \
         dashboard/hoval_status.py exporter/hoval_exporter.py hoxpi-features.example.json \
         keepalive/hoval_keepalive.py watch/hoval_watch.py backup/hoxpi_backup.sh \
         systemd/hoval-bridge.service systemd/hoval-status.service systemd/hoval-exporter.service; do
  [ -f "$f" ] || MISSING="$MISSING $f"
done
[ -z "$MISSING" ] || die "Dateien fehlen im Repo-Verzeichnis:$MISSING  (unvollstaendiger Download? git clone erneut ausfuehren)"
echo "OK: alle Installationsdateien vorhanden"

# 0d) CAN-Adapter (USB-CAN angesteckt?). Kein Abbruch - der Adapter kann auch spaeter kommen.
CANDEV=$(ls -d /sys/class/net/can* 2>/dev/null | head -1 || true)
if [ -n "$CANDEV" ]; then
  echo "OK: CAN-Interface $(basename "$CANDEV") erkannt"
  if command -v ip >/dev/null 2>&1; then
    ip -details link show "$(basename "$CANDEV")" 2>/dev/null | grep -q "bitrate 50000" \
      && echo "    (laeuft bereits mit 50 kbit/s)" || true
  fi
else
  if lsusb 2>/dev/null | grep -qiE "CAN|canable|1d50:606f|0483:1234"; then
    warn "USB-CAN-Geraet per lsusb sichtbar, aber kein can*-Netzwerkinterface - Kernelmodul (gs_usb/slcan) fehlt?"
  else
    warn "Kein CAN-Interface (can0) gefunden - USB-CAN-Adapter angesteckt? Dienste werden trotzdem installiert; can0.service startet erst, wenn der Adapter da ist."
  fi
  if [ "$DRY" != "1" ] && [ "$YES" != "1" ]; then
    ask "Ohne CAN-Adapter fortfahren?" || die "Abgebrochen - Adapter anstecken und erneut starten."
  fi
fi

# 0e) Platz / Netz
AVAIL_MB=$(df -Pm / | awk 'NR==2{print $4}')
[ "${AVAIL_MB:-0}" -ge 1500 ] || warn "Nur ${AVAIL_MB} MB frei auf / - fuer Pakete (+Grafana ca. 150 MB) knapp."
if ! getent hosts deb.debian.org >/dev/null 2>&1; then
  warn "deb.debian.org nicht aufloesbar - kein Internet/DNS? apt-get wird scheitern."
fi

# 0f) Bestehende Installation erkennen (idempotent, aber gut zu wissen)
if [ -d /opt/hoxpi ] || systemctl list-unit-files 2>/dev/null | grep '^hoval-bridge' >/dev/null; then
  echo "Hinweis: bestehende HoxPi-Installation gefunden - Dateien werden aktualisiert, Configs (whitelist.json, hoxpi-features.json) bleiben erhalten."
fi
[ "$WARN" = "0" ] && echo "Vorpruefungen: alles OK" || echo "Vorpruefungen: $WARN Warnung(en), siehe oben"

# ---------------------------------------------------------------------------
# 1) Pakete
# ---------------------------------------------------------------------------
STEP="1) Pakete"
echo "--- 1) Pakete ---"
run apt-get update
run apt-get install -y python3 python3-can python3-pymodbus python3-openpyxl python3-qrcode python3-paho-mqtt can-utils curl

# ---------------------------------------------------------------------------
# 2) Hoval-Datenpunktliste
# ---------------------------------------------------------------------------
STEP="2) Hoval-Datenpunktliste"
echo "--- 2) Hoval-Datenpunktliste ---"
XLSX_URL="https://www.hoval.com/misc/TTE/TTE-GW-Modbus-datapoints.xlsx"
XLSX=$(ls ./*.xlsx 2>/dev/null | head -1 || true)
if [ -z "$XLSX" ]; then
  echo "Keine xlsx gefunden. Bitte die offizielle Hoval-Datenpunktliste herunterladen"
  echo "  $XLSX_URL"
  echo "und neben install.sh legen (wird aus Urheberrechtsgruenden nicht mitgeliefert)."
  if ask "Jetzt automatisch herunterladen?"; then
    if [ "$DRY" = "1" ]; then
      run curl -fL -o TTE-GW-Modbus-datapoints.xlsx "$XLSX_URL"
      XLSX=./TTE-GW-Modbus-datapoints.xlsx
    else
      if ! curl -fL --retry 3 -o TTE-GW-Modbus-datapoints.xlsx "$XLSX_URL"; then
        rm -f TTE-GW-Modbus-datapoints.xlsx
        die "Download fehlgeschlagen (Netz? URL geaendert?). Datei manuell besorgen und neben install.sh legen."
      fi
      XLSX=./TTE-GW-Modbus-datapoints.xlsx
    fi
  else
    die "Ohne Datenpunktliste geht es nicht weiter."
  fi
fi
echo "Nutze: $XLSX"

# ---------------------------------------------------------------------------
# 3) Dateien installieren
# ---------------------------------------------------------------------------
STEP="3) Dateien installieren"
echo "--- 3) Dateien installieren ---"
run install -d -o "$ADM" /opt/hoxpi
run python3 tools/gen_registers.py "$XLSX" "1,520,143" /opt/hoxpi/registers.json
run python3 tools/gen_reg_texts.py "$XLSX" /opt/hoxpi/registers.json /opt/hoxpi/reg_texts.json
run install -m 755 bridge/hoval_bridge.py /opt/hoxpi/
# whitelist nur beim ersten Mal (anlagenspezifisch, nie ueberschreiben)
if [ -f /opt/hoxpi/whitelist.json ]; then echo "  whitelist.json vorhanden - bleibt unveraendert"
else run install -m 644 bridge/whitelist.example.json /opt/hoxpi/whitelist.json; fi
run install -m 755 dashboard/hoval_status.py /opt/hoxpi/
run install -m 755 exporter/hoval_exporter.py /opt/hoxpi/
[ -f assistant/hoxpi_assistent.html ] && run install -m 644 assistant/hoxpi_assistent.html /opt/hoxpi/
# Die Skripte erwarten die Dateien unter /home/admin/hoval-bridge/ - Symlink setzen:
[ -d "$HOME_ADM" ] || run install -d "$HOME_ADM"
[ -e "$HOME_ADM/hoval-bridge" ] || run ln -s /opt/hoxpi "$HOME_ADM/hoval-bridge"

STEP="3b) Zusatzfunktionen"
echo "--- 3b) Zusatzfunktionen: Feature-Schalter, Keepalive, Waechter, Sollzustand, Backup ---"
# Zentrale Feature-Schalter (auch im Dashboard: Sicherheit -> Funktionen)
if [ -f "$HOME_ADM/hoxpi-features.json" ]; then echo "  hoxpi-features.json vorhanden - bleibt unveraendert"
else run install -m 644 -o "$ADM" hoxpi-features.example.json "$HOME_ADM/hoxpi-features.json"; fi
# Keepalive: haelt bei relais-freiem Betrieb die Eingaenge 30-046/057/066 = AUS (Bus statt Kontakt)
run install -m 755 -o "$ADM" keepalive/hoval_keepalive.py "$HOME_ADM/hoval_keepalive.py"
# Stoerungs-Waechter + Verdichter-Kurzzyklus-Alarm (meldet an Home Assistant / Logdatei / Webhook)
run install -m 755 -o "$ADM" watch/hoval_watch.py "$HOME_ADM/hoval_watch.py"
run install -d -o "$ADM" "$HOME_ADM/hoval-watch"
# Sollzustands-Waechter: stellt nach Stromausfall/Wartung die Grund-Betriebsart selbst wieder her (Pause: touch $HOME_ADM/WARTUNG)
run install -m 755 -o "$ADM" watch/hoval_sollzustand.py "$HOME_ADM/hoval_sollzustand.py"
if [ -f "$HOME_ADM/hoxpi-sollzustand.json" ]; then echo "  hoxpi-sollzustand.json vorhanden - bleibt unveraendert"
else run install -m 644 -o "$ADM" watch/hoxpi-sollzustand.example.json "$HOME_ADM/hoxpi-sollzustand.json"; fi
# Naechtliches versioniertes Backup aller Skripte + Configs
run install -m 755 -o "$ADM" backup/hoxpi_backup.sh "$HOME_ADM/hoxpi_backup.sh"
run install -d -o "$ADM" "$HOME_ADM/hoxpi-backups"
# Cronjobs (User admin) idempotent eintragen:
CRONLINES="*/5 * * * * /usr/bin/python3 $HOME_ADM/hoval_keepalive.py >> /tmp/keepalive.log 2>&1
*/2 * * * * /usr/bin/python3 $HOME_ADM/hoval_watch.py >/dev/null 2>&1
*/5 * * * * /usr/bin/python3 $HOME_ADM/hoval_sollzustand.py >/dev/null 2>&1
17 3 * * * /bin/bash $HOME_ADM/hoxpi_backup.sh >> $HOME_ADM/hoxpi-backups/backup.log 2>&1"
if [ "$DRY" = "1" ]; then
  echo "  [dry-run] crontab -u $ADM: folgende Zeilen eintragen (alte hoval_keepalive/hoval_watch/hoval_sollzustand/hoxpi_backup-Zeilen ersetzen):"
  echo "$CRONLINES" | sed 's/^/             /'
else
  TMPCRON=$(mktemp)
  crontab -u "$ADM" -l 2>/dev/null | grep -vE "hoval_keepalive|hoval_watch|hoval_sollzustand|hoxpi_backup" > "$TMPCRON" || true
  echo "$CRONLINES" >> "$TMPCRON"
  crontab -u "$ADM" "$TMPCRON"; rm -f "$TMPCRON"
  echo "Cronjobs fuer $ADM eingetragen (Keepalive */5, Waechter */2, Sollzustand */5, Backup 03:17)."
fi

# ---------------------------------------------------------------------------
# 4) CAN-Interface + Dienste
# ---------------------------------------------------------------------------
STEP="4) CAN-Interface + Dienste"
echo "--- 4) CAN-Interface + Dienste ---"
[ -f systemd/can0.service ] && run install -m 644 systemd/can0.service /etc/systemd/system/
run install -m 644 systemd/hoval-bridge.service /etc/systemd/system/
run install -m 644 systemd/hoval-status.service /etc/systemd/system/
run install -m 644 systemd/hoval-exporter.service /etc/systemd/system/
[ -f avahi/hoxpi-device-info.service ] && [ -d /etc/avahi/services ] && run install -m 644 avahi/hoxpi-device-info.service /etc/avahi/services/
run systemctl daemon-reload
if [ "$DRY" = "1" ]; then
  run systemctl enable --now can0
else
  systemctl enable --now can0 2>/dev/null || warn "can0.service konnte nicht starten (USB-CAN angesteckt?) - startet automatisch nach Neustart mit Adapter."
fi
run systemctl enable --now hoval-bridge hoval-status hoval-exporter

# ---------------------------------------------------------------------------
# 4b) Optional: Home Assistant
# ---------------------------------------------------------------------------
STEP="4b) Home Assistant / MQTT"
echo "--- 4b) Optional: Home Assistant (MQTT-Auto-Discovery) ---"
if ask "Home-Assistant-Anbindung per MQTT installieren (empfohlen, wenn HA genutzt wird)?"; then
  run apt-get install -y mosquitto mosquitto-clients
  run install -d -o "$ADM" "$HOME_ADM/hoval-mqtt"
  run install -m 755 -o "$ADM" mqtt/hoval_mqtt.py "$HOME_ADM/hoval-mqtt/hoval_mqtt.py"
  run install -m 644 systemd/hoval-mqtt.service /etc/systemd/system/
  run systemctl daemon-reload
  run systemctl enable --now mosquitto hoval-mqtt
  echo "In Home Assistant nur die MQTT-Integration auf diesen Broker zeigen lassen -"
  echo "alle Werte + Steuerung erscheinen automatisch (Geraet 'HoxPi Waermepumpe')."
else
  echo "Uebersprungen - spaeter jederzeit nachinstallierbar (oder im Dashboard abschaltbar)."
fi

# ---------------------------------------------------------------------------
# 5) Optional: Prometheus + Grafana
# ---------------------------------------------------------------------------
STEP="5) Prometheus + Grafana"
echo "--- 5) Optional: Statistik (Prometheus + Grafana) ---"
if ask "Grafana-Statistik installieren (ca. 150 MB)?"; then
  run apt-get install -y --no-install-recommends prometheus
  run install -m 644 prometheus/prometheus.yml /etc/prometheus/prometheus.yml
  if grep -q retention /etc/default/prometheus 2>/dev/null; then :
  elif [ "$DRY" = "1" ]; then echo "  [dry-run] /etc/default/prometheus: ARGS=\"--storage.tsdb.retention.time=400d\" anhaengen"
  else echo 'ARGS="--storage.tsdb.retention.time=400d"' >> /etc/default/prometheus; fi
  run mkdir -p /etc/apt/keyrings
  if [ "$DRY" = "1" ]; then
    echo "  [dry-run] Grafana-APT-Key nach /etc/apt/keyrings/grafana.gpg + Quelle /etc/apt/sources.list.d/grafana.list"
  else
    curl -fsSL --retry 3 https://apt.grafana.com/gpg.key | gpg --dearmor -o /etc/apt/keyrings/grafana.gpg \
      || die "Grafana-Signaturschluessel nicht ladbar (Netz?). Grafana spaeter nachinstallieren, Rest ist fertig."
    echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" > /etc/apt/sources.list.d/grafana.list
  fi
  run apt-get update
  run apt-get install -y grafana
  run install -m 644 grafana/datasource-hoxpi.yaml /etc/grafana/provisioning/datasources/hoxpi.yaml
  run install -m 644 grafana/dashboards-hoxpi.yaml /etc/grafana/provisioning/dashboards/hoxpi.yaml
  run install -d -o grafana -g grafana /var/lib/grafana/dashboards
  run install -m 644 -o grafana -g grafana grafana/dashboard-hoxpi.json /var/lib/grafana/dashboards/hoxpi.json
  run mkdir -p /etc/systemd/system/grafana-server.service.d
  run install -m 644 grafana/grafana-override.conf /etc/systemd/system/grafana-server.service.d/override.conf
  run systemctl daemon-reload
  run systemctl enable --now prometheus grafana-server
fi

# ---------------------------------------------------------------------------
# 6) Optional: MCP-Server
# ---------------------------------------------------------------------------
STEP="6) MCP-Server"
echo "--- 6) Optional: KI-Schnittstelle (MCP-Server) ---"
if ask "MCP-Server installieren (KI-Assistenten wie Claude koennen die Anlage inspizieren)?"; then
  VENV=$HOME_ADM/hoxpi-mcp-venv
  if [ "$DRY" = "1" ]; then
    run python3 -m venv "$VENV"
    run "$VENV/bin/pip" install --quiet mcp
  else
    python3 -m venv "$VENV" 2>/dev/null || { VENV=/opt/hoxpi/mcp-venv; python3 -m venv "$VENV"; }
    "$VENV/bin/pip" install --quiet mcp || die "pip install mcp fehlgeschlagen (Netz? python3-venv installiert?)."
  fi
  run mkdir -p "$HOME_ADM/hoxpi-mcp"
  run install -m 755 mcp/hoxpi_mcp.py "$HOME_ADM/hoxpi-mcp/"
  if [ -f "$HOME_ADM/hoxpi-mcp/config.json" ]; then :
  elif [ "$DRY" = "1" ]; then echo "  [dry-run] $HOME_ADM/hoxpi-mcp/config.json anlegen: {\"enable_write\": false, \"port\": 8808}"
  else echo '{"enable_write": false, "port": 8808}' > "$HOME_ADM/hoxpi-mcp/config.json"; fi
  run install -m 644 systemd/hoxpi-mcp.service /etc/systemd/system/
  run systemctl daemon-reload
  run systemctl enable --now hoxpi-mcp
fi

# ---------------------------------------------------------------------------
# 7) Abschluss + Selbsttest
# ---------------------------------------------------------------------------
STEP="7) Abschluss"
echo ""
if [ "$DRY" = "1" ]; then
  echo "=== Trockenlauf beendet - nichts veraendert ==="
  echo "Echte Installation:  sudo bash install.sh        (oder --yes fuer alles automatisch)"
  trap - EXIT; exit 0
fi

echo "--- Selbsttest ---"
sleep 3
for s in hoval-bridge hoval-status hoval-exporter; do
  if systemctl is-active --quiet "$s"; then echo "OK:   $s laeuft"
  else warn "$s laeuft NICHT - 'journalctl -u $s -n 30' zeigt warum (haeufig: CAN-Adapter fehlt)."; fi
done
if systemctl is-active --quiet can0; then echo "OK:   can0 hochgefahren"
else warn "can0 nicht aktiv - ohne CAN-Adapter liefert die Bridge keine Werte."; fi
if curl -fs -o /dev/null --max-time 5 http://127.0.0.1/; then echo "OK:   Dashboard antwortet auf Port 80"
else warn "Dashboard antwortet nicht auf Port 80 (journalctl -u hoval-status)."; fi

echo ""
echo "=== Fertig === ($WARN Warnung(en))"
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
trap - EXIT
