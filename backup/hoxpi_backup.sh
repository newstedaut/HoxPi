#!/bin/bash
# HoxPi Konfigurations-Backup — nächtlich per Cron (17 3 * * *).
# v2 (03.09.2026): sichert die LIVE-Dateien der Dienste (ExecStart-Pfade), nicht mehr die
#   veralteten Kopien im Home (~/hoval_status.py, ~/hoval_mqtt.py, ~/hoval_exporter.py,
#   ~/hoval_bridge.py waren seit 30.08. nicht mehr das, was läuft).
#   Neu dabei: Dashboard (/usr/local/bin/hoval_status.py), Assistent-HTML, hoxpi-features.json,
#   2FA-auth.json (!), MCP-Server (hoxpi-mcp, lohates-mcp), alle hoval-/hoxpi-/kwl-/can0-Units
#   + Timer, Prometheus/Grafana-Provisioning + Dashboard-JSON, Mosquitto-local.conf,
#   Bridge-tools/, sowie eine MANIFEST.txt (Ziel ← Quelle, md5) für die Wiederherstellung.
# KEINE venvs, Logs, Massendaten (fulllog-CSV, .NAL, rs485-Logs) — nur das, was HoxPi ausmacht.
# Behält die letzten 14 Stände. Off-Device-Kopie per scp (z. B. aus einem Cowork-/Cron-Lauf) empfohlen.
python3 -c "import json,sys; sys.exit(0 if json.load(open('/home/admin/hoxpi-features.json')).get('backup',{}).get('enabled',True) else 1)" 2>/dev/null || { echo "$(date) Backup deaktiviert (features.json)"; exit 0; }
set -u
BDIR="/home/admin/hoxpi-backups"
mkdir -p "$BDIR"
TS=$(date +%Y%m%d_%H%M%S)
OUT="$BDIR/hoxpi_$TS.tar.gz"
STAGE=$(mktemp -d)
MAN="$STAGE/MANIFEST.txt"
echo "# HoxPi Backup $TS — Ziel im Archiv <- Quelle auf dem Pi (md5)" > "$MAN"

# put <quelle> <zielordner-im-archiv>  — kopiert nur existierende, lesbare Dateien, schreibt Manifest
put() {
  local src="$1" dst="$2"
  [ -f "$src" ] && [ -r "$src" ] || { echo "FEHLT/UNLESBAR $src" >> "$MAN"; return 0; }
  mkdir -p "$STAGE/$dst"
  cp -a "$src" "$STAGE/$dst/" 2>/dev/null || cp "$src" "$STAGE/$dst/" 2>/dev/null || { echo "KOPIE-FEHLER $src" >> "$MAN"; return 0; }
  echo "$dst/$(basename "$src") <- $src ($(md5sum "$src" | cut -c1-32))" >> "$MAN"
}

# 1) Bridge (CAN<->Modbus, Dienst hoval-bridge, läuft als root)
for f in hoval_bridge.py whitelist.json registers.json reg_texts.json labels.json datapoints_version.json \
         auth.json hoxpi_assistent.html hoval-bridge.service; do
  put "/home/admin/hoval-bridge/$f" bridge
done
for f in /home/admin/hoval-bridge/tools/*.py; do put "$f" bridge/tools; done

# 2) Dienste — LIVE-Pfade laut systemd ExecStart
put /usr/local/bin/hoval_status.py            dashboard      # hoval-status (Port 80, 2FA)
put /home/admin/hoval-mqtt/hoval_mqtt.py      mqtt           # hoval-mqtt
put /home/admin/hoval-exporter/hoval_exporter.py exporter    # hoval-exporter (:9101)
put /home/admin/hoval-exporter/config.yml     exporter
put /home/admin/hoxpi-mcp/hoxpi_mcp.py        mcp/hoxpi-mcp  # hoxpi-mcp (:8808)
put /home/admin/hoxpi-mcp/config.json         mcp/hoxpi-mcp
put /home/admin/lohates-mcp/lohates_mcp.py    mcp/lohates-mcp
put /home/admin/lohates-mcp/config.json       mcp/lohates-mcp

# 3) Cron-Skripte + Feature-/Wächter-Konfiguration (Home)
for f in hoval_keepalive.py hoval_watch.py discovery.py hoxpi_fulllog.py wp_takte_log.py kuehl_langzeit.py \
         wez_status_evidenz.py kwl_logger.py hoval_dp.py hoval_dp_map.json hoxpi-features.json hoxpi_backup.sh; do
  put "/home/admin/$f" cron-skripte
done
put /home/admin/hoval-watch/config.json watch

# 4) Mess-Aufbau (Skripte, keine Logs)
for d in rs485_sniff verdichter_catch; do
  [ -d "/home/admin/$d" ] || continue
  for f in /home/admin/$d/*.py /home/admin/$d/*.sh; do [ -f "$f" ] && put "$f" "$d"; done
done

# 5) Crontab + Systemd-Units/Timer + Prometheus/Grafana/Mosquitto
crontab -l > "$STAGE/crontab.txt" 2>/dev/null && echo "crontab.txt <- crontab -l (admin)" >> "$MAN"
for f in /etc/systemd/system/hoval-*.service /etc/systemd/system/hoval-*.timer /etc/systemd/system/hoxpi-*.service \
         /etc/systemd/system/lohates-*.service /etc/systemd/system/kwl-*.service /etc/systemd/system/kwl-*.timer \
         /etc/systemd/system/can0.service; do
  [ -f "$f" ] && put "$f" systemd
done
put /etc/prometheus/prometheus.yml                 prometheus
put /etc/grafana/provisioning/dashboards/hoxpi.yaml grafana
put /var/lib/grafana/dashboards/hoxpi.json          grafana
put /etc/mosquitto/conf.d/local.conf               mosquitto

# 6) Systeminfo (Paketstände, CAN, Dienststatus, ExecStart-Pfade als Beleg)
{ echo "# HoxPi Backup $TS"; echo "## uname"; uname -a
  echo "## dpkg python3-*"; dpkg -l 'python3-*' 2>/dev/null | grep -E "paho|can|serial|yaml|prometheus"
  echo "## can0"; ip -details link show can0 2>/dev/null
  echo "## Dienste (ExecStart / aktiv / enabled)"
  for u in hoval-bridge hoval-status hoval-mqtt hoval-exporter hoxpi-mcp lohates-mcp prometheus grafana-server mosquitto; do
    printf "%s | %s | %s | %s\n" "$u" "$(systemctl show -p ExecStart --value "$u" 2>/dev/null | grep -o 'argv\[\]=[^;]*' | head -1)" \
      "$(systemctl is-active "$u" 2>/dev/null)" "$(systemctl is-enabled "$u" 2>/dev/null)"
  done
  echo "## Timer"; systemctl list-timers --no-pager 2>/dev/null | grep -iE "hoval|hoxpi|kwl"
  echo "## Units nur root-lesbar (Inhalt via systemctl show)"
  for u in hoval-datapoints-update.service hoval-datapoints-update.timer; do
    echo "### $u"; systemctl show -p Description,ExecStart,OnCalendar,Persistent,User,Unit "$u" 2>/dev/null
  done
} > "$STAGE/system_info.txt" 2>/dev/null

# 7) Packen + Aufräumen
tar -czf "$OUT" -C "$STAGE" . 2>/dev/null
rm -rf "$STAGE"
ls -1t "$BDIR"/hoxpi_*.tar.gz | tail -n +15 | xargs -r rm -f   # nur letzte 14 behalten
echo "$(date '+%F %T') Backup: $OUT ($(du -h "$OUT" | cut -f1), $(tar tzf "$OUT" | grep -vc '/$') Dateien)"
