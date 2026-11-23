# ANALYSE F55 – Abnahme Überhöhung 07-001 = 2,0 K (Reg 30684)

Stand: 01.11.2026, Daten bis 15:50:01 Ortszeit. Erstellt von Claude (Analyse-Agent, nur lesend). Keine Schreibzugriffe auf Anlage oder Pi.

## Frage
07-001 (Reg 30684, „WEZ Überhöhung/Abschlag VL-Sollwert“) wurde am 31.10.2026 22:01 von 3,0 K (Rohwert 30) auf 2,0 K (Rohwert 20) gesetzt (Quelle: `[lokaler Pfad]`, Eintrag „07-001 auf 2,0 K gesetzt“). Rückweg: 30684 = 30.
1. Fällt der HK1-Vorlauf-Ist im Heizbetrieb unter das HK1-Soll (Reg 1490)?
2. Ändern sich Laufzeit je Start, kWh_el und Arbeitszahl gegen 24.–31.10. (3,0 K) im selben Außentemperaturband?
3. Sinken die Raumtemperaturen UG?

## Datenquelle
- Volllogger Pi `/home/<user>/hoxpi_fulllog/2026-10-20.csv.gz` … `2026-10-30.csv.gz`, `2026-10-31.csv`, `2026-11-01.csv` (5-min-Raster, Rohwerte). Kopfzeilen aller Dateien geprüft: identisch [sicher].
- Ausgeschnittene Spalten (Kopie auf Windows-PC): `[lokaler Pfad]`, `[lokaler Pfad]`.
- Register (Bedeutung per `hoxpi__read_register` / `search_registers` geprüft, 01.11.2026 ~16:00):
  - 1477 Außen ×10, 1490 HK1-Vorlauf-Soll ×10 (von Loxone geschrieben), 1513 **HK1 „Vorlauf-Ist“** ×10, 1525 WP-Vorlauf ×10 (bei 0 Ersatz 31893), 1539 WEZ-Status (1 = Heizen, 4 = WW), 1504 WW-Status, 1501 HK1-Status (23 = Heizen), 25611 P_el ×100 kW, 25612 P_th kW (ganzzahlig), 1506 Gesamtwärmezähler kWh, 27489 WW-Wärmezähler kWh, 30684 07-001 ×10, 1510 „Raum Ist HK1“ ×10.
  - Hinweis: 18760 („Anlage Vorlauftemperatur Heizen“), im Statuseintrag als HK1-VL-Ist genannt, ist **nicht** der HK1-Vorlauf, sondern läuft mit 1525 mit (z. B. 01.11. 05:45:01: 1525 = 380, 18760 = 380, 1513 = HK1). Für diese Analyse daher 1513 verwendet [sicher, aus Registername + Rohdaten].
- Raumtemperatur: Reg 1510 (Quelle der Zuordnung: `/home/<user>/hoval_exporter.py` Zeile 12 „hoval_raum_ist_c: (1510, 0.1)“). Die Loxone-Raumregler (`IRoomControllerV2`) haben keine abrufbare Statistik (control_statistics: „not chartable“).
- Methodik-Vorlage: `[lokaler Pfad]` (MD-12).
- Skripte (nur lesend): `[lokaler Pfad]`, `f55_summary.py`, `f55_extra.py`, `f55_steady.py`, `f55_raum.py`.

## Methode
- **Heiztakt** (5-min-Probe): 1539 = 1 und 1504 = 0 und 25611 ≥ 30 (P_el ≥ 0,30 kW) – wie MD-12. Aufeinanderfolgende Heiztakte (Abstand < 400 s) = ein Heizlauf. Dauer = Anzahl Takte × 5 min.
- **E_el** = Σ 25611/100 × 5/60 kWh. **Q_th** = Σ 25612 × 5/60 kWh. **AZ_Pth** = Q_th/E_el. **AZ_1506** = (Δ1506 − Δ27489) vom Takt vor Laufbeginn bis Takt nach Laufende / E_el (1-kWh-Stufung, je Lauf ±12–25 % Rauschen).
- **WP-VL − Soll:** 1525 − 1490 als Laufmittel und am letzten Lauftakt („Laufende“, MD-04-Methode). **HK1-VL − Soll:** 1513 − 1490 Laufmittel und Minimum, zusätzlich über alle Heizbetriebs-Proben (1501 = 23, 1504 = 0, 1490 > 0) getrennt nach WP an/aus.
- **Gruppen:** NACH = Läufe mit Start ≥ 31.10. 22:01 und 30684 = 20 (Lauf 84, 21:35–22:30, gemischt → ausgeschlossen; Lauf 95 ab 15:35 noch offen → ausgeschlossen). VOR = Läufe 24.10. 00:00 – 31.10. 21:30, 30684 = 30. Außenband beider Gruppen: Laufmittel 1477 zwischen 3,0 und 6,5 °C (NACH liegt bei 3,4–6,1 °C). Läufe mit 1490 = 0 (Soll-Lücke) ausgeschlossen.
- **AT-Korrektur:** lineare Regression je Kennzahl über 69 VOR-Läufe ≥ 15 min, 20.–31.10., AT 2–10 °C; NACH als Residuum.
- **Zeitfensterbilanz:** gleiches Uhrzeitfenster 22:01–15:51 (17,8 h) an den Vortagen 24./25.10. … 30./31.10. gegen 31.10./01.11.

## Ergebnis

### 1. Heizläufe NACH Umstellung (07-001 = 2,0 K), Volllogger `2026-10-31.csv` / `2026-11-01.csv`
| Lauf | Start–Ende (Ortszeit) | min | AT °C | WP-VL−1490 Ende K | WP-VL−1490 Mittel K | HK1(1513)−1490 Mittel K | HK1−1490 min K | E_el kWh | Q_th kWh | AZ_Pth | ΔQ1506 kWh | AZ_1506 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 85 | 31.10. 23:20–23:55 | 40 | 5,7 | 8,0 | 4,96 | −1,14 | −3,0 | 1,116 | 4,67 | 4,18 | 5 | 4,48 |
| 86 | 01.11. 00:55–01:25 | 35 | 5,4 | 7,9 | 5,17 | −1,29 | −3,0 | 1,078 | 4,00 | 3,71 | 4 | 3,71 |
| 87 | 01.11. 02:35–02:40 | 10 | 5,0 | 7,0 | 4,70 | −1,50 | −3,1 | 0,287 | 1,00 | 3,49 | 1 | 3,49 |
| 88 | 01.11. 03:35–04:00 | 30 | 4,7 | 7,7 | 5,37 | −1,40 | −3,1 | 0,927 | 3,75 | 4,05 | 4 | 4,32 |
| 89 | 01.11. 05:10–05:50 | 45 | 4,0 | 6,0 | 3,74 | −2,01 | −3,5 | 1,346 | 5,42 | 4,02 | 4 | 2,97 |
| 90 | 01.11. 07:00–07:25 | 30 | 3,5 | 7,5 | 5,30 | −0,68 | −3,0 | 0,925 | 3,67 | 3,96 | 3 | 3,24 |
| 91 | 01.11. 08:20–08:45 | 30 | 3,4 | 7,6 | 5,18 | −1,00 | −2,3 | 0,866 | 3,67 | 4,23 | 3 | 3,46 |
| 92 | 01.11. 10:25–10:55 | 35 | 4,7 | 8,0 | 5,97 | −0,36 | −2,5 | 1,012 | 4,50 | 4,45 | 4 | 3,95 |
| 93 | 01.11. 11:55–12:25 | 35 | 5,5 | 7,6 | 5,33 | −0,59 | −2,5 | 1,031 | 4,42 | 4,28 | 4 | 3,88 |
| 94 | 01.11. 14:25–14:50 | 30 | 6,1 | 7,7 | 5,80 | −0,85 | −2,8 | 0,887 | 4,25 | 4,79 | 3 | 3,38 |
| *84 (gemischt)* | 31.10. 21:35–22:30 | 60 | 6,2 | 8,1 | 4,53 | −1,37 | −3,9 | 1,741 | 7,67 | 4,40 | 8 | 4,60 |
| *95 (offen)* | 01.11. 15:35–15:50+ | 20+ | 5,7 | 5,7 | 4,15 | −1,53 | −2,5 | 0,551 | 2,50 | 4,54 | – | – |

Lauf 89 enthält kein WW (WW-Ladung erst 05:55–06:35, 1504 = 1), endet aber durch die WW-Umschaltung, daher kleines Ende-Delta 6,0 K [sicher, Volllogger 01.11. 05:50:02 → 05:55:02].

### 2. Vergleichsläufe VOR Umstellung (07-001 = 3,0 K), AT 3,0–6,5 °C, Volllogger `2026-10-24.csv.gz` … `2026-10-31.csv`
| Lauf | Start–Ende | min | AT °C | WP-VL−1490 Ende K | WP-VL−1490 Mittel K | HK1−1490 Mittel K | HK1−1490 min K | E_el kWh | Q_th kWh | AZ_Pth | ΔQ1506 | AZ_1506 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 17 | 24.10. 06:30–07:00 | 35 | 5,3 | 8,7 | 6,40 | −0,53 | −2,3 | 1,081 | 4,42 | 4,09 | 4 | 3,70 |
| 18 | 24.10. 10:40–10:45 | 10 | 5,8 | 4,1 | 3,65 | −3,30 | −4,5 | 0,298 | 1,42 | 4,75 | 1 | 3,35 |
| 19 | 24.10. 11:45–12:25 | 45 | 6,5 | 8,9 | 5,69 | −0,81 | −2,9 | 1,343 | 6,42 | 4,78 | 5 | 3,72 |
| 23 | 24.10. 18:30–18:55 | 30 | 5,3 | 8,6 | 6,45 | −0,18 | −1,8 | 0,912 | 3,83 | 4,20 | 4 | 4,39 |
| 24 | 24.10. 20:15–20:35 | 25 | 4,8 | 8,8 | 6,76 | +0,20 | −1,1 | 0,732 | 3,25 | 4,44 | 3 | 4,10 |
| 25 | 25.10. 04:00–04:50 | 55 | 3,0 | 8,3 | 5,66 | −1,63 | −7,9 | 1,680 | 7,00 | 4,17 | 8 | 4,76 |
| 26 | 25.10. 05:35–06:50 | 80 | 3,1 | 8,8 | 5,61 | −0,76 | −3,4 | 2,437 | 9,92 | 4,07 | 9 | 3,69 |
| 27 | 25.10. 08:05–08:30 | 30 | 3,4 | 8,8 | 6,22 | −0,50 | −2,3 | 0,917 | 3,75 | 4,09 | 3 | 3,27 |
| 28 | 25.10. 10:30–11:10 | 45 | 4,7 | 8,7 | 6,09 | −0,33 | −2,5 | 1,303 | 5,83 | 4,48 | 6 | 4,60 |
| 29 | 25.10. 12:25–12:40 | 20 | 5,2 | 6,7 | 5,35 | −0,98 | −1,8 | 0,606 | 2,67 | 4,40 | 3 | 4,95 |
| 30 | 25.10. 15:20–16:00 | 45 | 6,0 | 9,5 | 5,90 | −0,64 | −3,2 | 1,350 | 6,58 | 4,88 | 5 | 3,70 |
| 31 | 25.10. 18:45–19:05 | 25 | 6,3 | 8,7 | 6,66 | −0,86 | −5,0 | 0,727 | 3,58 | 4,93 | 4 | 5,50 |
| 32 | 25.10. 20:20–20:45 | 30 | 6,2 | 9,0 | 6,42 | −0,25 | −2,1 | 0,902 | 4,17 | 4,62 | 4 | 4,44 |
| 33 | 25.10. 22:50–22:55 | 10 | 5,2 | 6,4 | 5,90 | −3,15 | −5,6 | 0,323 | 1,25 | 3,88 | 0 | – |
| 34 | 26.10. 02:20–02:50 | 35 | 5,0 | 8,9 | 6,47 | −0,87 | −5,8 | 1,067 | 4,50 | 4,22 | 5 | 4,68 |
| 35 | 26.10. 03:40–04:10 | 35 | 4,9 | 9,3 | 6,67 | −0,30 | −2,2 | 1,074 | 4,58 | 4,27 | 5 | 4,65 |
| 36 | 26.10. 05:20–06:30 | 75 | 4,4 | 9,2 | 5,00 | −1,65 | −6,5 | 2,279 | 10,33 | 4,53 | 10 | 4,39 |
| 37 | 26.10. 08:00–08:50 | 55 | 4,8 | 8,5 | 4,71 | −1,61 | −4,6 | 1,676 | 7,17 | 4,28 | 7 | 4,18 |
| 41 | 27.10. 04:55–05:40 | 50 | 5,2 | 9,0 | 5,65 | −1,70 | −7,1 | 1,544 | 7,08 | 4,59 | 7 | 4,53 |
| 42 | 27.10. 06:30–06:40 | 15 | 5,3 | 5,3 | 4,23 | −2,43 | −3,0 | 0,460 | 2,00 | 4,35 | 2 | 4,35 |
| 43 | 27.10. 06:55–06:55 | 5 | 5,1 | −2,1 | −2,10 | −7,20 | −7,2 | 0,165 | 0,67 | 4,04 | −1 | – |
| 44 | 27.10. 08:20–09:35 | 80 | 6,2 | 9,5 | 3,85 | −2,36 | −7,8 | 2,358 | 11,58 | 4,91 | 11 | 4,66 |
| 47 | 28.10. 03:40–04:30 | 55 | 5,9 | 8,1 | 4,65 | −3,09 | −14,3 | 1,681 | 8,08 | 4,81 | 8 | 4,76 |
| 56 | 29.10. 05:25–06:10 | 50 | 6,4 | 9,2 | 6,13 | −0,63 | −2,7 | 1,529 | 7,25 | 4,74 | 7 | 4,58 |
| 57 | 29.10. 08:00–08:50 | 55 | 6,1 | 7,2 | 4,50 | −1,37 | −3,9 | 1,601 | 7,75 | 4,84 | 8 | 5,00 |
| 63 | 29.10. 19:50–20:10 | 25 | 6,4 | 8,3 | 6,28 | −0,40 | −2,1 | 0,756 | 3,25 | 4,30 | 3 | 3,97 |
| 65 | 30.10. 00:20–00:55 | 40 | 3,9 | 8,6 | 5,48 | −2,15 | −8,2 | 1,258 | 5,33 | 4,24 | 5 | 3,98 |
| 66 | 30.10. 02:10–02:15 | 10 | 4,9 | 5,3 | 5,05 | −3,10 | −4,8 | 0,295 | 1,25 | 4,24 | 1 | 3,39 |
| 67 | 30.10. 03:10–03:40 | 35 | 5,2 | 8,4 | 5,83 | −0,77 | −2,2 | 1,082 | 3,92 | 3,62 | 4 | 3,70 |
| 68 | 30.10. 04:35–05:10 | 40 | 5,5 | 9,5 | 6,12 | −0,47 | −2,1 | 1,108 | 4,67 | 4,21 | 4 | 3,61 |
| 69 | 30.10. 05:45–06:25 | 45 | 5,6 | 9,0 | 6,33 | −0,54 | −2,6 | 1,365 | 5,92 | 4,33 | 6 | 4,40 |
| 70 | 30.10. 07:10–07:40 | 35 | 5,7 | 8,5 | 6,29 | −0,41 | −2,2 | 1,057 | 4,67 | 4,41 | 5 | 4,73 |
| 77 | 30.10. 21:40–22:05 | 30 | 6,4 | 8,3 | 5,63 | −0,72 | −2,5 | 0,893 | 3,58 | 4,01 | 3 | 3,36 |
| 78 | 31.10. 03:30–04:00 | 35 | 5,6 | 9,0 | 6,43 | −1,67 | −9,2 | 1,097 | 4,67 | 4,25 | 5 | 4,56 |
| 79 | 31.10. 05:10–06:10 | 65 | 5,7 | 9,5 | 5,62 | −0,71 | −2,9 | 1,904 | 8,17 | 4,29 | 8 | 4,20 |
| 80 | 31.10. 06:50–07:10 | 25 | 5,7 | 8,4 | 5,38 | −0,94 | −2,4 | 0,772 | 3,17 | 4,10 | 3 | 3,89 |
| 81 | 31.10. 08:40–08:45 | 10 | 5,8 | 5,6 | 4,60 | −1,70 | −2,0 | 0,278 | 1,17 | 4,19 | 0 | – |

### 3. Zusammenfassung VOR vs. NACH (gleiches AT-Band 3,0–6,5 °C)
| Kennzahl | VOR 3,0 K (n = 37 / ≥15 min: 32) | NACH 2,0 K (n = 10 / ≥15 min: 9) | Differenz | Einstufung |
|---|---|---|---|---|
| AT Laufmittel | 5,32 °C | 4,81 °C | −0,5 K kälter | [sicher] |
| WP-VL am Laufende (Median, ≥15 min) | 40,0 °C | 38,0 °C | −2,0 K | [sicher] |
| WP-VL − 1490 am Laufende (Median / Mittel, ≥15 min) | 8,75 / 8,60 K | 7,70 / 7,56 K | **−1,05 K** | [sicher] |
| WP-VL − 1490 Laufmittel (Median, alle) | 5,69 K | 5,24 K | −0,45 K | [sicher] |
| HK1(1513) − 1490 Laufmittel (Median, alle) | −0,86 K | −1,07 K | −0,2 K | [sicher] |
| Laufzeit je Start (Median / Mittel, alle) | 35 / 37,6 min | 32 / 32,0 min | −5,6 min (Mittel) | [sicher] |
| Laufzeit AT-korrigiert (Residuum, ≥15 min) | Fit 57,6 − 3,23·AT | −7,7 min (Basis-Streuung sd 13,8) | kürzer | [wahrscheinlich] |
| E_el je Lauf (Median / Mittel, alle) | 1,081 / 1,133 kWh | 0,969 / 0,947 kWh | −0,19 kWh | [sicher] |
| AZ_Pth Σ Q / Σ E (alle) | 4,41 | 4,15 | −0,26 | [sicher] |
| AZ_Pth AT-korrigiert (Residuum, ≥15 min) | Fit 3,707 + 0,131·AT | −0,15 (sd Basis 0,27) | im Rauschen | [wahrscheinlich] |
| AZ_1506 Σ Zähler / Σ E (alle) | 4,18 | 3,69 | −0,49 | [Vermutung] (1-kWh-Stufung, n = 10) |
| AZ stationär (ab 3. Lauftakt), P_th/P_el | 4,62 (VL 38,1 °C, AT 5,22) | 4,49 (VL 37,3 °C, AT 4,78) | −0,13, AT-bereinigt ≈ −0,07 | [wahrscheinlich] |
| AZ der Anlauftakte (1.+2. Takt) / Anteil an allen Takten | 3,73 / 23,8 % | 3,40 / 29,0 % | mehr Anlaufanteil | [sicher] |
| Abtautakte (1539 = 8/16) | 11 von 2286 Proben | 0 von 214 | – | [sicher] |

### 4. HK1-Vorlauf-Ist (1513) gegen HK1-Soll (1490), alle Heizbetriebs-Proben (1501 = 23, 1504 = 0)
| Zeitraum | Proben | Mittel 1513−1490 | Anteil < Soll | < Soll −1 K | < Soll −2 K | Minimum |
|---|---|---|---|---|---|---|
| VOR 24.10. 00:00 – 31.10. 21:30, gesamt | 1073 | −1,03 K | 73,0 % | 36,1 % | 16,9 % | −15,4 K |
| VOR, WP an | 433 | −0,89 K | 58,7 % | 41,3 % | 21,5 % | −14,3 K |
| VOR, WP aus | 640 | −1,12 K | 82,7 % | 32,5 % | 13,8 % | −15,4 K |
| NACH 31.10. 22:01 – 01.11. 15:50, gesamt | 194 | −1,28 K | 81,4 % | 56,7 % | 30,9 % | −7,2 K |
| NACH, WP an | 74 | −1,02 K | 70,3 % | 48,6 % | 31,1 % | −3,5 K |
| NACH, WP aus | 120 | −1,44 K | 88,3 % | 61,7 % | 30,8 % | −7,2 K |

Quelle: Volllogger 24.10.–01.11., Spalten 1501/1504/1513/1490. Achtung: VOR-Band hier nicht nach AT gefiltert (24.10.–31.10., AT im Mittel ≈ 6,8 °C), NACH bei 4,9 °C.

### 5. Zeitfensterbilanz 22:01–15:51 (17,8 h), Heizbetrieb
| Fenster | AT °C | E_el Heizen kWh | Q_th kWh | AZ_Pth | Starts | Laufanteil | Raum 1510 Mittel / min / max °C | 1490 Mittel °C |
|---|---|---|---|---|---|---|---|---|
| 24./25.10. | 3,96 | 7,99 | 34,2 | 4,29 | 6 | 23,5 % | 21,54 / 20,9 / 22,3 | 31,06 |
| 25./26.10. | 6,43 | 8,19 | 36,8 | 4,49 | 8 | 25,2 % | 21,59 / 21,1 / 22,3 | 30,75 |
| 26./27.10. | 6,68 | 6,30 | 30,2 | 4,79 | 6 | 19,6 % | 22,08 / 20,9 / 24,0 | 30,38 |
| 27./28.10. | 8,25 | 7,09 | 35,4 | 4,99 | 7 | 22,0 % | 21,22 / 20,6 / 22,0 | 30,68 |
| 28./29.10. | 7,75 | 6,57 | 31,4 | 4,78 | 6 | 20,6 % | 21,18 / 20,6 / 22,1 | 31,06 |
| 29./30.10. | 6,42 | 8,82 | 38,8 | 4,40 | 9 | 27,6 % | 21,21 / 20,8 / 21,7 | 30,62 |
| 30./31.10. | 6,97 | 5,78 | 25,3 | 4,39 | 6 | 18,2 % | 21,86 / 21,0 / 22,9 | 30,89 |
| **31.10./01.11. (2,0 K)** | **4,90** | **10,93** | **45,8** | **4,19** | **11** | **34,6 %** | **21,13 / 20,6 / 22,0** | **31,13** |

Quelle: Volllogger + `f55_raum.csv` (Reg 1510), Skripte `f55_extra.py`, `f55_raum.py`. Starts = Laufbeginne im Fenster inkl. Kurzläufe.

## Stichprobe (zum Gegenrechnen) – Lauf 88, `/home/<user>/hoxpi_fulllog/2026-11-01.csv`
Rohwerte, Spalten: zeit, 1477, 1490, 1501, 1504, 1506, 1513, 1525, 1539, 25611, 25612, 27489, 30684
```
2026-11-01 03:30:02 48 322 23 0 47577 293 325 0   0 0 40184 20   (Takt vor Lauf)
2026-11-01 03:35:01 48 322 23 0 47577 291 350 1 208 6 40184 20
2026-11-01 03:40:02 48 322 23 0 47578 296 360 1 171 7 40184 20
2026-11-01 03:45:01 47 322 23 0 47578 303 375 1 178 8 40184 20
2026-11-01 03:50:01 47 322 23 0 47579 312 380 1 182 8 40184 20
2026-11-01 03:55:01 47 322 23 0 47580 321 390 1 185 8 40184 20
2026-11-01 04:00:02 46 323 23 0 47580 326 400 1 188 8 40184 20   (letzter Lauftakt)
2026-11-01 04:05:01 46 323 23 0 47581 331 375 0   0 0 40184 20   (Takt nach Lauf)
```
- E_el = (208+171+178+182+185+188)/100 × 5/60 = 11,12 × 0,0833 = **0,927 kWh**; Q_th = (6+7+8+8+8+8) × 5/60 = **3,75 kWh**; AZ_Pth = **4,05**.
- ΔQ1506 = 47581 − 47577 = 4 kWh, Δ27489 = 0 → AZ_1506 = **4,32**.
- WP-VL − 1490 am Laufende = 40,0 − 32,3 = **7,7 K** (mit 3,0 K lag dieser Wert im Median bei 8,75 K).
- HK1 (1513) − 1490: von −3,1 K (03:35) bis +0,3 K (04:00), Mittel −1,40 K. Der HK1-Vorlauf erreicht das Soll erst kurz vor Laufende.

## Urteil
**07-001 = 2,0 K halten – Abnahme noch nicht abgeschlossen** [wahrscheinlich].
- Die Änderung wirkt wie gedacht: WP-VL − Soll am Laufende sinkt um 1,05 K (8,75 → 7,70 K), WP-VL am Laufende 40,0 → 38,0 °C [sicher].
- Komfort: Raum 1510 im Fenster 21,13 °C (min 20,6), gleich wie 27.–30.10. (21,18–21,22 °C, min 20,6–20,8) bei 0,5–3 K kälterer Außenluft [wahrscheinlich – nur ein Fühler, 17,8 h]. Kein Absinken erkennbar.
- HK1-Vorlauf: liegt **schon mit 3,0 K** in 73 % der Heizminuten unter 1490 (Sägezahn durch Takten, HK1 bekommt das Soll erst gegen Laufende). Mit 2,0 K: 81 %, im Mittel −1,28 statt −1,03 K (−0,25 K). Das Kriterium „< 2 % der Heizminuten unter Soll“ aus `02_Status_Offen.md` war mit 3,0 K nie erfüllt und ist damit kein brauchbares Abnahmekriterium [sicher].
- Effizienz: **kein messbarer Gewinn** in 10 Läufen. Stationär-AZ AT-bereinigt ≈ −0,07 (Rauschen), Lauf-AZ −0,15 Residuum bei sd 0,27 [wahrscheinlich]. Gegenwirkung: Läufe ~6–8 min kürzer, Anlauftakte machen 29 % statt 24 % der Laufzeit aus, Anlauf-AZ ~3,4–3,7 [wahrscheinlich]. Erwarteter Gewinn laut MD-12 nur +2 %/K ≈ +0,09 AZ – das ist mit 10 Läufen nicht auflösbar [sicher].
- Auffällig, aber **nicht** durch 07-001 erklärbar: im Fenster 31.10./01.11. 11 Starts, 10,9 kWh_el und 45,8 kWh_th – deutlich mehr Wärme als am kälteren 24./25.10. (34,2 kWh_th bei 3,96 °C). Weniger Überhöhung kann den Wärmebedarf nicht erhöhen; Ursache wahrscheinlich Haus/N [entfernt] (Feiertag 01.11., kein Ofen – 1510-Maximum nur 22,0 °C) [Vermutung].
- Rückweg (30684 = 30) nur, wenn bis 07.11. Raum 1510 im Mittel < 20,8 °C fällt oder der Betreiber Komfortverlust meldet.

## Was bringt uns das
- Bestätigt: 07-001 senkt die Vorlauf-Spitze 1:1 (−1 K Überhöhung → −1,05 K am Laufende). Die Hoval setzt den Parameter so um, wie die Doku sagt [sicher].
- Komfort ist nach dem ersten Tag nicht schlechter. Du kannst den Wert stehen lassen.
- Der Stromgewinn ist klein (theoretisch ~2 %, ≈ 0,2 kWh/Tag bei ~10 kWh_el Heizen) und wird zum Teil vom häufigeren Takten (kürzere Läufe) aufgefressen. Große Sprünge kommen nicht von 07-001, sondern von weniger Starts bzw. längeren Läufen (Heizkurve, Hysterese, Puffer) [wahrscheinlich].
- Für die Abnahme am 07.11. gilt als besseres Kriterium: Mittel 1513 − 1490 über alle Heizminuten (Ziel: nicht schlechter als −1,5 K) plus Raum 1510, statt „< 2 % unter Soll“.

## Offen
- 7-Tage-Abnahme bis 07.11.2026 18:00 mit derselben Methode wiederholen (Skript `[lokaler Pfad]` + `f55_summary.py`, Rohdaten neu ziehen). Erst ab ~30 Läufen nach Umstellung ist ein AZ-Unterschied von ±0,1 auflösbar [wahrscheinlich].
- Raumtemperaturen je UG-Raum: Loxone-Raumregler (`IRoomControllerV2`, z. B. Wohnzimmer `<UUID>`) liefern keine Statistik. Klären, welcher Fühler Reg 1510 speist (Loxone-Schreibwert oder Hoval-Raumfühler) – Doku: https://www.loxone.com/dede/kb/intelligente-raumregelung/
- Ursache des hohen Wärmebedarfs 31.10./01.11. (45,8 kWh_th in 17,8 h): Ofen-Nutzung, Fenster, Wind? der Betreiber fragen oder Loxone-Ofen-Nachlauf nachsehen.
- Mehr Starts (14,8/24 h hochgerechnet gegen 7,6–12,1/24 h): beobachten, ob das an 07-001 (früheres Abschalten) oder am Wärmebedarf hängt.
- Statuseintrag `02_Status_Offen.md` korrigieren: HK1-VL-Ist ist Reg **1513**, nicht 18760 (18760 = Anlagen-Vorlauf, ≈ 1525).