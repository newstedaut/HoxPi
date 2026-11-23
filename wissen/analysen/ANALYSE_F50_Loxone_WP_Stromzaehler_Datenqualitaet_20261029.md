# F50 – Loxone „WP Stromzähler“ gegen Hoval-Stromzähler 25614 (Orchestrator 29.10.2026 18:00)

Nur gelesen: Loxone-MCP `control_statistics` auf [Zähler](https://www.loxone.com/dede/kb/zaehler/) „WP Stromzähler“ `<UUID>` (group 2 diff day/hour/month, group 1 raw), Volllogger `~/hoxpi_fulllog/2026-09-*.csv.gz` / `2026-10-*` (Reg 25614 = el. Gesamtenergie dp 23009, kWh ganzzahlig; 25613 High-Word = 0).
Skript: `[lokaler Pfad]` (+ `.out`), am Pi nur `/tmp/or_f50strom_20261029_1800.py`. An Anlage, Loxone und Pi-Diensten nichts geändert.
Loxone-Buckets beginnen 00:00 UTC (= 02:00 MESZ bis 25.10., 01:00 MEZ danach); Hoval-Stand jeweils an derselben Grenze genommen.

## Ergebnis
| Befund | Zahl | Sicherheit |
|---|---|---|
| Echter Septemberverbrauch WP | Hoval 25614: 01.09. 29 987 → 01.10. 30 163 = **176 kWh**; Loxone ohne Sprung 165,9 kWh | sicher (Hoval), Differenz s. nächste Zeile |
| 09./10.09. Loxone 0 kWh, ab 11.09. Bruchzahlen | Hoval-Zähler stand 08.09. 13:25 – 19.09. still (30 027, dann 0 geliefert, 19.09. 30 087); Loxone integriert ab 11.09. die Momentanleistung | sicher (beide Datenreihen) |
| Jahr 2026 in Loxone | enthält dieselben +29 996 kWh | sicher |
| **Oktober** 01.10. 02:00 – 29.10. 17:55 | Loxone 332,8 kWh, Hoval 328 kWh (±1) → **+4,7 kWh (+1,4 %)** | sicher (Summen) |
| 20.10. CAN-Ausfall 12:23–17:10 | Loxone `actual` = 0 von 10:30 bis 15:30 UTC, Tag 7,7 kWh gegen Hoval 13 kWh → **−5,3 kWh** (Unterzählung) | sicher |
| 29.10. Bus-Ausfall 08:55–10:42 | `actual` als Standbild 1,85 kW → Tag 15,8 kWh bis 17:56 gegen Hoval 11 kWh → **+4,8 kWh** (Überzählung, Loop 13:35: ~3,3 kWh im Fenster) | sicher (Tag), Fensteranteil wahrscheinlich |
| übrige 26 Oktobertage | Loxone im Mittel +0,2 kWh/Tag über Hoval, Summe +5,2 kWh (+1,6 %) | wahrscheinlich systematisch (Integration 25611 vs. Zähler), Einzeltage ±1 kWh sind Rundung des 1-kWh-Zählers |

## Zwei Fehlerbilder bei Busausfall
1. Bridge liefert 0 (20.10., „never“-Register als 0, Bridge-Freshness v3/v4) → Loxone **zählt zu wenig**, der Hoval-Zähler holt nach.
2. Bridge liefert Standbild (29.10.) → Loxone **zählt weiter**, Phantomverbrauch.
Beide verschwinden in Monatssummen nur zufällig gegeneinander (Oktober −5,3 / +4,8).

## Was bringt uns das
- Monats-/Jahresbilanzen (Wochenbilanz, AZ, Kosten) **nie aus dem Loxone-Zähler** für September/Jahr 2026 nehmen; Quelle für Tage/Monate = Hoval 25614 (Volllogger), Loxone nur für Stundenprofile.
- Oktober-Loxone-Wert ist brauchbar (+1,4 %), Ausfalltage 20.10./29.10. aber einzeln falsch.

## Vorschlag (der Betreiber entscheidet, nichts umgesetzt)
- Loxone: `actual` des WP-Zählers über ein Frische-Gate führen (0 setzen, wenn get_status-Feld `leistung_elektrisch_kw` in `verstummte_felder` steht) – beseitigt Fehlerbild 2; Fehlerbild 1 bleibt (Unterzählung, Hoval-Zähler ist Referenz).
- Septemberwert in der Loxone-Statistik ist nur in Loxone Config von Hand korrigierbar (Vermutung) – sonst in Auswertungen mit 176 kWh rechnen.