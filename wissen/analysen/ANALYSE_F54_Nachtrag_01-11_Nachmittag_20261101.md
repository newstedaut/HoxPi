# ANALYSE F54 – Nachtrag 01.11.2026 Nachmittag (Läufe ab 14:25, Reg 1520)

Erstellt 01.11.2026 ~17:00 MEZ, Analyse-Agent, nur lesend (kein Schreibzugriff auf Anlage/Pi).

## Frage
(a) Wann und bei welchem Rücklauf stoppte der Heizlauf mit Start ~15:32? Trifft V131(a') zu (Stopp bei RL = 1520 + 3,0 = 34,5 °C)? Weitere Läufe danach? Tabelle aller Läufe.
(b) War Reg 1520 in den Fenstern 13:40–14:25 und 15:10–15:35 konstant 31,5 °C? Ist V129r(b) („Start, wenn RL <= 1520 − 1,5 K, 13–18 min später“) für die Starts 14:25 und 15:32 sicher oder nur wahrscheinlich?

## Datenquellen
- HoxPi-MCP `get_history` (Prometheus, 1-min-Raster): `p_el_kw`, `ruecklauf_c`, 13:28–16:58.
- Volllogger Pi `~/hoxpi_fulllog/2026-11-01.csv` (5-min-Raster, Rohwerte ×10), Spalten: 1 = zeit, 15 = 1490 (HK1-Soll), 38 = 1513 (HK1-VL-Ist), 45 = 1520 (WP-VL-Soll), 60 = 1535 (RL), 363 = 25611 (P_el ×100). Gelesen per `hoxpi_ssh.py "grep … | cut -d, -f1,15,38,45,60,363"`, Zeilen 13:00–16:55.
- `~/ww_hires/` existiert nicht (ls: No such file) – keine höhere Auflösung für 1520 verfügbar.

## Ergebnis

### Läufe seit 14:25 (Heizbetrieb; Start/Stopp aus p_el 1-min, RL aus ruecklauf_c 1-min, 1520 aus Volllogger 5-min)

| Lauf | Start (erste Minute P>0) | RL bei Start | 1520 bei Start | Stopp (erste Minute P=0) | RL bei Stopp | 1520 bei Stopp | Laufdauer | Pause davor |
|---|---|---|---|---|---|---|---|---|
| A | 14:25 (1,75 kW) | 30,0 | 31,5 | 14:54 (letzte On-Minute 14:53 = 1,80 kW) | 34,5 (14:53 und 14:54) | 31,5 | ~29 min | ~46 min (WW-Lauf endete 13:39) |
| B | 15:33 (2,01 kW; 15:32 noch 0,0) | 29,5 (15:32: 29,0) | 31,5 | 16:09 (letzte On-Minute 16:08 = 1,80 kW) | 34,5 (16:08 und 16:09) | 31,5 | ~36 min | ~39 min (ab 14:54) |
| – | kein weiterer Start bis 16:58 | – | – | – | – | – | – | ≥ 49 min (ab 16:09, läuft) |

Unterschwellen-Zeit vor Start (RL erstmals <= 30,0 = 1520 − 1,5):
- Lauf A: RL 30,0 ab 14:12 → Start 14:25 = **13 min** Verzögerung.
- Lauf B: RL 30,0 ab 15:17, 29,5 ab 15:25, 29,0 um 15:32 → Start 15:33 = **16 min** Verzögerung.

Stopp: beide Läufe enden in der ersten Minute, in der RL = 34,5 erreicht ist bzw. eine Minute danach (A: 34,5 ab 14:53, Stopp 14:54; B: 34,5 ab 16:08, Stopp 16:09). 1520 + 3,0 = 34,5.

### Reg 1520 im 5-min-Raster (Volllogger, Rohwert ×10)

| Zeit | 1490 | 1520 | 1535 RL | 25611 P_el |
|---|---|---|---|---|
| 13:35 | 29,9 | 56,0 (WW) | 54,0 | 2,63 |
| 13:40 | 29,9 | 31,5 | 54,0 | 0 |
| 13:45–14:20 (8 Zeilen) | 29,7 | 31,5 | 31,0 → 30,0 | 0 |
| 14:25 | 29,7 | 31,5 | 30,0 | 2,08 |
| 14:30–14:50 | 29,8 | 31,5 | 30,5 → 34,0 | 1,62–1,78 |
| 14:55–15:10 | 29,8/29,7 | 31,5 | 34,0 → 31,5 | 0 |
| 15:15–15:30 | 29,9 | 31,5 | 30,5 → 29,5 | 0 |
| 15:35 | 29,9 | 31,5 | 29,5 | 1,61 |
| 15:40–16:05 | 29,9/29,8 | 31,5 | 30,5 → 34,0 | 1,63–1,79 |
| 16:10–16:40 | 29,9 | 31,5 | 34,5 → 31,5 | 0 |
| 16:45–16:55 | 30,0 | **32,0** | 31,0 → 30,5 | 0 |

(RL-Spalte hier aus Volllogger 1535, deckt sich mit Prometheus `ruecklauf_c` auf ±0,5 K; Zeitstempel Volllogger ~:01–:02 s nach der Minute.)

- 1520 war von 13:40 bis 16:40 in jeder 5-min-Zeile **31,5** – also in beiden Fenstern 13:40–14:25 und 15:10–15:35 konstant. [sicher im 5-min-Raster; Ausreißer < 5 min nicht ausschließbar, da keine feinere Quelle]
- 1520 wechselte um 16:45 auf **32,0** (gleichzeitig 1490 29,9 → 30,0). Vorher 13:00: 32,0 bei 1490 = 30,0. Muster: 1490 29,7–29,9 → 1520 31,5; 1490 30,0 → 1520 32,0 [wahrscheinlich: 1520 = 1490 + Überhöhung, auf 0,5 K gerastet – Vermutung zur Rundung].

## Urteil

| Regel | Lauf A (14:25) | Lauf B (15:33) |
|---|---|---|
| V129r(b) Startbedingung RL <= 1520 − 1,5 (= 30,0) | erfüllt (RL 30,0 bei Start) [sicher] | erfüllt (RL 29,0–29,5 bei Start) [sicher] |
| V129r(b) Verzögerung 13–18 min | 13 min [sicher] | 16 min [sicher] |
| V129r(b) als Mechanismus (feste Schwelle + Wartezeit) | [wahrscheinlich] | [wahrscheinlich] |
| V131(a') Stopp bei RL = 1520 + 3,0 = 34,5 | ja, 34,5 [sicher] | ja, 34,5 [sicher] |

Begründung „wahrscheinlich“ statt „sicher“ für den Mechanismus von V129r(b):
- RL ist auf 0,5 K gerastet; „<= 1520 − 1,5“ und „< 1520 − 1,0“ sind mit diesen Daten nicht unterscheidbar.
- Bei Lauf B lag RL schon 8 min unter der Schwelle (29,5), trotzdem kein früherer Start; mit reiner Wartezeit ab Schwellen-Unterschreitung (15:17) passt das, ein Gradminuten-Integral wäre aber ebenfalls möglich (A: 1,5 K × 13 min ≈ 20 Kmin; B: ≈ 28 Kmin – nicht deckungsgleich, spricht eher für Zeitglied) [Vermutung].
- Erst 2 Starts mit gleichem 1520 = 31,5; die Abhängigkeit von 1520 (statt einer festen 30,0-°C-Grenze) ist mit diesen beiden Läufen nicht prüfbar.

V131(a') ist bei beiden Läufen auf die Minute bestätigt (Stopp in der Minute nach Erreichen von 34,5), auch hier nur mit 1520 = 31,5.

## Stichprobe (Rohwerte)
1. Volllogger `~/hoxpi_fulllog/2026-11-01.csv`, Zeile `2026-11-01 15:35:01`: 1490 = 299, 1513 = 274, 1520 = 315, 1535 = 295, 25611 = 161 → 1520 = 31,5 °C, RL 29,5 °C, P_el 1,61 kW (Lauf B läuft).
2. Prometheus `get_history p_el_kw`: 2026-11-01 16:08 = 1,80 kW, 16:09 = 0,0 kW; `ruecklauf_c` 16:08 = 34,5, 16:09 = 34,5 → Stopp Lauf B bei RL 34,5.

## Offen
- Prüfstein für die 1520-Abhängigkeit: seit 16:45 ist 1520 = 32,0 → neue Schwelle 30,5. RL hat 30,5 um 16:49 erreicht. Nach V129r(b) ist der nächste Start **~17:02–17:07** bei RL ~30,5 zu erwarten, Stopp bei RL **35,0**. Startet die WP dagegen erst bei RL 30,0, ist die Schwelle fest und nicht 1520-bezogen. Bis 16:58 kein Start (noch innerhalb des Fensters).
- Höher aufgelöste 1520-Daten fehlen (`~/ww_hires/` nicht vorhanden); 1520 ist nicht als Prometheus-Metrik verfügbar.
- Zeitglied vs. Integral: weitere Starts mit unterschiedlichem Unterschwellen-Verlauf nötig.