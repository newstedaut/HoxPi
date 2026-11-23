# ANALYSE F41 — Prometheus `hoval_ww_soll_c` 56,1 am 22.10. 13:53: Ausreißer oder echter Wert? (Orchestrator 25.10.2026 11:20)

## Frage
02_Status_Offen Z. 138 (OR 22.10. 22:54): Ausreißer Prometheus `ww_soll_c` = 56,1 °C um 22.10. 13:53 klären.

## Ergebnis
- **Kein Ausreißer (sicher).** Der Exporter `/home/<user>/hoval-exporter/hoval_exporter.py` Z. 11 liest für `hoval_ww_soll_c` **Reg 1499** („Warmwasser-Soll, berechneter Sollwert“, HoxPi `read_register` 25.10. 11:15 = 50,0), nicht Reg 1497 („Normal-Warmwassertemperatur“, Parameter = 50,0).
  Prometheus-Rohsamples 22.10.: 11:51:06Z = 57, ab 11:51:36Z (13:51:36 MESZ) durchgehend 56,1 (30-s-Raster, Abfrage `hoval_ww_soll_c[12m]` @ 11:58Z).
- **Muster (sicher, Volllogger `~/hoxpi_fulllog/2026-10-14…25`):** 1499 weicht nur am Ende von Ladungen mit 1497 = 57,0 (Smart-Grid/Kick) von 1497 ab, dann bis zur nächsten Sollwertänderung:

| Zeit (MESZ) | 1497 | 1499 | 1500 (WW oben) | 1521 |
|---|---|---|---|---|
| 15.10. 14:25 | 57,0 | 55,5 | 55,8 | 0 |
| 16.10. 12:45 | 57,0 | 55,6 | 56,2 | 0 |
| 16.10. 16:30 | 57,0 | 55,2 | 55,5 | 0 |
| 17.10. 14:50 | 50,0 | 55,2 | 55,5 | 0 |
| 18.10. 18:05 | 57,0 | 56,1 | 56,3 | 0 |
| 20.10. 12:20 | 57,0 | 55,9 | 56,2 | 0 |
| 20.10. 17:15 | 57,0 | 54,6 | 52,8 | 0 |
| 22.10. 13:55 | 57,0 | 56,1 | 56,8 | 0 |
| 23.10. 16:45 | 57,0 | 55,9 | 56,3 | 0 |

  In 24.10. und 25.10. (Kick 52 °C) keine Abweichung. 1499 liegt beim Wechsel 0,2–0,7 K unter 1500 (Ausnahme 20.10. 17:15).
- **Wahrscheinlich:** Die 57-°C-Ladung wird vor Erreichen des Solls beendet (HD-Begrenzer/Bodenlauf, vgl. F33 `ANALYSE_HD_Haltepunkt_WW_20261025.md`), und die TopTronic setzt das berechnete WW-Soll auf die erreichte Speichertemperatur, damit die Ladung nicht sofort neu startet. Welcher Hoval-Parameter das steuert: **nicht ermittelt**.
- **Vermutung:** 17.10. 14:50 (1497 schon 50, 1499 = 55,2) ist ein 5-min-Zeitversatz zwischen den Rundumabfragen (WEZ-Register bis 60 s alt).

## Was bringt uns das
- Auswertungen mit Prometheus `hoval_ww_soll_c` messen das **berechnete** Soll (1499), nicht den eingestellten Wert (1497). Für Ladeziel-Rechnungen (Soll + 4 K, F34) 1497 oder 5051 nehmen.
- Jede 57-°C-Ladung endet zurzeit ohne das Ziel zu erreichen, ~0,5–2 K darunter. Das stützt „Abend-WW 57 → 52“ (F33/F39).

## Stichprobe (Rohdaten)
- Volllogger `~/hoxpi_fulllog/2026-10-22.csv.gz` 13:55:02: 1497 = 570, 1499 = 561, 1500 = 568, 1521 = 0.
- Prometheus `hoval_ww_soll_c` 2026-10-22 11:51:36Z = 56.1, 11:51:06Z = 57.

## Quellen / Skripte (nur lesend)
`[lokaler Pfad]`, `or_wwsoll2_20261025_1120.sh` (Pi `/tmp`), HoxPi-MCP `read_register` 1497/1499.