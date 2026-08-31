#!/bin/bash
# HoxPi Konfigurations-Backup — nächtlich per Cron.
# Sichert alle Skripte/Configs/Unit-Dateien versioniert als tar.gz.
# KEINE venvs, Logs, Massendaten (fulllog-CSV, .NAL) — nur das, was HoxPi ausmacht.
# Behält die letzten 14 Stände. Off-Device-Kopie holt sich der Cowork-Loop (scp).
python3 -c "import json,sys; sys.exit(0 if json.load(open('/home/admin/hoxpi-features.json')).get('backup',{}).get('enabled',True) else 1)" 2>/dev/null || { echo "$(date) Backup deaktiviert (features.json)"; exit 0; }
set -u
BDIR="/home/admin/hoxpi-backups"
mkdir -p "$BDIR"
TS=$(date +%Y%m%d_%H%M%S)
OUT="$BDIR/hoxpi_$TS.tar.gz"
STAGE=$(mktemp -d)

# 1) Skripte + Configs (nur existierende Pfade)
FILES=(
  /home/admin/hoval-bridge/hoval_bridge.py
  /home/admin/hoval-bridge/whitelist.json
  /home/admin/hoval-bridge/registers.json
  /home/admin/hoval-bridge/reg_texts.json
  /home/admin/hoval-bridge/labels.json
  /home/admin/hoval-bridge/datapoints_version.json
  /home/admin/hoval-bridge/hoval-bridge.service
  /home/admin/hoval_keepalive.py
  /home/admin/hoval_watch.py
  /home/admin/hoval_exporter.py
  /home/admin/hoval_mqtt.py
  /home/admin/hoval_status.py
  /home/admin/discovery.py
  /home/admin/hoxpi_fulllog.py
  /home/admin/wp_takte_log.py
  /home/admin/kuehl_langzeit.py
  /home/admin/hoval-watch/config.json
)
mkdir -p "$STAGE/scripts"
for f in "${FILES[@]}"; do [ -f "$f" ] && cp -a "$f" "$STAGE/scripts/" 2>/dev/null; done

# 2) Ordner mit Skripten (ohne Logs/Daten)
for d in rs485_sniff verdichter_catch; do
  [ -d "/home/admin/$d" ] && mkdir -p "$STAGE/$d" && \
    find "/home/admin/$d" -maxdepth 1 -type f \( -name "*.py" -o -name "*.sh" \) -exec cp -a {} "$STAGE/$d/" \; 2>/dev/null
done

# 3) Crontab + Systemd-Units + Paketstände
crontab -l > "$STAGE/crontab.txt" 2>/dev/null
cp -a /etc/systemd/system/hoval-*.service /etc/systemd/system/can0.service "$STAGE/" 2>/dev/null
{ echo "# HoxPi Backup $TS"; echo "## dpkg python3-*"; dpkg -l 'python3-*' 2>/dev/null | grep -E "paho|can|serial" ; \
  echo "## can0"; ip -details link show can0 2>/dev/null; } > "$STAGE/system_info.txt" 2>/dev/null

# 4) Packen + Aufräumen
tar -czf "$OUT" -C "$STAGE" . 2>/dev/null
rm -rf "$STAGE"
ls -1t "$BDIR"/hoxpi_*.tar.gz | tail -n +15 | xargs -r rm -f   # nur letzte 14 behalten
echo "$(date '+%F %T') Backup: $OUT ($(du -h "$OUT" | cut -f1))"
