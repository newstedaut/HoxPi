# ANALYSE F55 – Zwischenstand nach erstem vollen Tag (07-001 = 2,0 K)

Stand: 01.11.2026 23:58, Daten bis 01.11.2026 23:55:01 (letzte Volllogger-Zeile). Erstellt von Claude (Analyse-Agent, nur lesend). Keine Schreibzugriffe auf Anlage, Pi, Loxone. Ergänzt `[lokaler Pfad]` (Stand 15:50) um den Rest des 01.11. – Methode und Läufe 85–94 dort, hier nicht wiederholt.

## Frage
Hält das Bild nach dem ersten vollen Tag mit 07-001 = 2,0 K (Reg 30684 = 20, seit 31.10.2026 22:01) gegen die Referenz 24.10.–31.10. 22:00 (3,0 K)? Konkret: Laufzeit je Start, Starts/Tag, Abstand WP-VL 1525 − 1490, HK1-Ist 1513 − 1490, Arbeitszahl, Raum 1510 – jeweils im gleichen Außentemperaturband.

## Datenquelle
- Volllogger Pi: `/home/<user>/hoxpi_fulllog/2026-10-24.csv.gz` … `2026-10-30.csv.gz`, `/home/<user>/hoxpi_fulllog/2026-10-31.csv`, `/home/<user>/hoxpi_fulllog/2026-11-01.csv` (288 Zeilen, 00:00:01–23:55:01). Spaltenposition im Kopf beider Dateien identisch geprüft (1477 = Feld 2, 1490 = 15, 1501 = 26, 1504 = 29, 1506 = 31, 1510 = 35, 1513 = 38, 1525 = 50, 1539 = 64, 19870 = 294, 25611 = 363, 25612 = 364, 27489 = 374, 30684 = 470, 31893 = 526) [sicher].
- Referenzdaten bis 31.10.: `[lokaler Pfad]` (Auszug der Vorgängeranalyse); 01.11. komplett frisch vom Pi gezogen (nur im Speicher, keine neue Datei).
- Auswertung: `[lokaler Pfad]` unverändert (per exec mit neuen Zeilen gefüttert), Zusatzrechnungen ad hoc (nicht gespeichert).
- Zeitraum NACH: 31.10.2026 22:01 – 01.11.2026 24:00. VOR: 24.10.2026 00:00 – 31.10.2026 21:30 (30684 = 30).

## Methode
- Wie Vorgängeranalyse: Heiztakt = 1539 = 1 und 1504 = 0 und 25611 ≥ 30; Takte < 400 s Abstand = ein Lauf; Läufe mit 1490 = 0 ausgeschlossen. E_el = Σ 25611/100 · 5/60, Q_th = Σ 25612 · 5/60, AZ_Pth = ΣQ/ΣE, AZ_1506 = (Δ1506 − Δ27489)/E_el.
- **WW-Erkennung:** 19870 (Umschaltventil) steht im Volllogger 24.10.–01.11. in allen 2604 Zeilen auf 0, auch bei 1504 = 1 (291 Zeilen) → im Volllogger nicht brauchbar; WW daher wie zuvor über 1504/1539 [sicher, Zählung (1504,19870): (0,0) = 2313, (1,0) = 291].
- Außenband: Laufmittel 1477 in [3,0; 4,5) und [4,5; 6,5) °C, zusätzlich gesamt [3,0; 6,5). Tagesvergleich mit 25.10. (AT 4,61 °C ≈ 01.11. 4,69 °C).
- 1490 = 0 = Heizpause Klimacontroller UG (belegt in `[lokaler Pfad]`).

## Ergebnis

### A. Neue Läufe 01.11. ab 15:30 (Messung)
| Lauf | Start–Ende | min | AT °C | WP-VL 1525 Mittel °C | 1490 Mittel °C | 1525−1490 Mittel K | 1525−1490 Ende K | 1513−1490 Mittel K | 1513−1490 min K | E_el kWh | Q_th kWh | AZ_Pth | ΔQ1506 | AZ_1506 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 95 | 15:35–16:05 | 35 | 5,6 | 35,1 | 29,9 | 5,29 | 7,6 | −0,54 | −2,5 | 0,991 | 4,50 | 4,54 | 5 | 5,05 |
| 96 | 17:05–17:15 | 15 | 4,9 | 33,8 | 28,6 | 5,23 | 8,0 | −0,80 | −2,5 | 0,458 | 1,42 | 3,10 | 2 | 4,37 |
| *97 (ausgeschl.)* | 20:15 | 5 | 4,4 | – | 0 | – | – | – | – | 0,175 | 0,58 | – | 0 | – |

- Lauf 96 endet, weil Loxone 1490 um 17:20:02 auf 0 setzt (17:15: 280 → 17:20: 0) [sicher, Volllogger].
- **Ab 17:20 bis 24:00 Heizpause** (1490 = 0, 1501 = 0, 400 von 485 min im Fenster 15:51–24:00). Raum 1510 in der Pause 21,9–22,5 °C (steigend ohne WP-Wärme) [sicher, Messung]. Lauf 97: ein einzelner 5-min-Takt 20:15 mit 1539 = 1, P_el 2,10 kW, aber 1490 = 0 und 1501 = 0 – Ursache unklar (Kurzlaufschutz/I3 laut Formel F21 würde 1490 ≥ 20 setzen, tut es aber nicht) [Vermutung].
- Keine WW-Ladung nach 15:51 (1504 durchgehend 0) [sicher].

### B. Band-Vergleich VOR (3,0 K) vs. NACH (2,0 K), alle Läufe inkl. 95/96
| Band AT | Gruppe | n | AT Mittel | Laufzeit Median / Mittel min | 1525−1490 Mittel K | 1525−1490 Ende Median K | 1513−1490 Mittel K | 1513−1490 min (Mittel) K | AZ_Pth | AZ_1506 | E_el/Lauf kWh |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3,0–4,5 | VOR | 5 | 3,58 | 55 / 56,0 | 5,59 | 8,80 | −1,34 | −5,66 | 4,24 | 4,08 | 1,714 |
| 3,0–4,5 | NACH | 3 | 3,64 | 30 / 35,0 | 4,74 | 7,50 | −1,23 | −2,93 | 4,06 | 3,19 | 1,046 |
| 4,5–6,5 | VOR | 32 | 5,59 | 35 / 34,7 | 5,42 | 8,65 | −1,37 | −3,95 | 4,45 | 4,20 | 1,042 |
| 4,5–6,5 | NACH | 9 | 5,30 | 35 / 29,4 | 5,31 | 7,70 | −0,94 | −2,78 | 4,17 | 4,11 | 0,865 |
| 3,0–6,5 | VOR | 37 | 5,32 | 35 / 37,6 | 5,45 | 8,70 | −1,37 | −4,18 | 4,41 | 4,18 | 1,133 |
| 3,0–6,5 | NACH | 12 | 4,88 | 32 / 30,8 | 5,17 | 7,65 | −1,01 | −2,82 | 4,14 | 3,85 | 0,910 |

(≥ 15 min: VOR 32, NACH 11; 1525−1490 Ende Median 8,75 → 7,70 K; AZ_Pth 4,42 → 4,16.)

### C. Tagesbilanz 00:00–24:00 (Heizbetrieb, ohne WW)
| Tag | AT °C | Starts (≥15 min) | Laufzeit min | min/Start | E_el kWh | Q_th kWh | AZ_Pth | AZ_1506 | Raum 1510 Mittel/min/max °C | 1513−1490 Mittel K | Anteil < Soll / < −1 K / < −2 K | 1490 = 0 min | WW-Ladungen |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 24.10. | 5,83 | 8 (7) | 240 | 30,0 | 7,16 | 32,4 | 4,53 | 4,47 | 22,05 / 20,6 / 24,2 | −0,85 | 73 / 34 / 11 % | 730 | 3 |
| 25.10. | 4,61 | 9 (8) | 340 | 37,8 | 10,24 | 44,8 | 4,37 | 4,30 | 21,51 / 20,9 / 22,3 | −1,25 | 74 / 41 / 23 % | 625 | 4 |
| 26.10. | 6,50 | 7 (7) | 260 | 37,1 | 7,87 | 35,5 | 4,51 | 4,70 | 21,84 / 21,1 / 24,0 | −0,85 | 71 / 32 / 14 % | 555 | 4 |
| 27.10. | 7,78 | 6 (5) | 210 | 35,0 | 6,30 | 30,2 | 4,79 | 4,60 | 21,79 / 20,9 / 22,8 | −1,71 | 75 / 44 / 25 % | 970 | 4 |
| 28.10. | 8,48 | 8 (7) | 240 | 30,0 | 7,26 | 36,1 | 4,97 | 4,96 | 21,39 / 20,6 / 22,1 | −1,16 | 69 / 40 / 19 % | 805 | 4 |
| 29.10. | 7,29 | 10 (8) | 295 | 29,5 | 8,84 | 41,5 | 4,70 | 4,07 | 21,18 / 20,6 / 21,9 | −0,89 | 69 / 33 / 16 % | 570 | 4 |
| 30.10. | 6,83 | 13 (12) | 400 | 30,8 | 11,88 | 52,3 | 4,41 | 4,46 | 21,34 / 20,8 / 22,2 | −0,86 | 76 / 33 / 15 % | 250 | 4 |
| **01.11. (2,0 K)** | **4,69** | **12 (10)** | **335** | **27,9** | **9,98** | **41,2** | **4,12** | **4,11** | **21,49 / 20,6 / 22,5** | **−1,27** | **81 / 56 / 31 %** | **420** | **2** |
| NACH gesamt 31.10. 22:01–24:00 | 4,77 | 13 (11) | 405 | 31,2 | 12,01 | 49,8 | 4,15 | 4,16 | 21,45 / 20,6 / 22,5 | −1,23 | 80 / 55 / 30 % | – | – |

Stunden-Starts hochgerechnet: NACH 13 Starts in 26 h = 12,0/Tag (VOR 6–13/Tag, Mittel 8,7) [sicher, Zählung].

### D. Stichprobe zum Nachrechnen – Lauf 95, `/home/<user>/hoxpi_fulllog/2026-11-01.csv`
Spalten: zeit, 1477, 1490, 1501, 1504, 1506, 1513, 1525, 1539, 25611, 25612, 27489, 30684 (Rohwerte)
```
2026-11-01 15:30:02 58 299 23 0 47616 275 295 0   0 0 40194 20  (vor Lauf)
2026-11-01 15:35:01 58 299 23 0 47616 274 325 1 161 6 40194 20
2026-11-01 15:40:02 57 299 23 0 47617 279 335 1 163 8 40194 20
2026-11-01 15:45:01 57 298 23 0 47617 285 345 1 167 8 40194 20
2026-11-01 15:50:01 56 298 23 0 47618 295 355 1 170 8 40194 20
2026-11-01 15:55:02 56 298 23 0 47619 299 360 1 173 8 40194 20
2026-11-01 16:00:02 55 299 23 0 47619 308 365 1 176 8 40194 20
2026-11-01 16:05:02 55 299 23 0 47620 312 375 1 179 8 40194 20  (letzter Lauftakt)
2026-11-01 16:10:02 55 299 23 0 47621 305 340 0   0 0 40194 20  (nach Lauf)
```
- 1525 − 1490 am Laufende: (375 − 299)/10 = **7,6 K**; Laufmittel (325+335+345+355+360+365+375)/7 = 351,4 → 35,14 − 29,87 = **5,27 K** (Skript 5,29 K, 1490 schwankt 298/299).
- E_el = (161+163+167+170+173+176+179)/100 · 5/60 = 11,89 · 0,0833 = **0,991 kWh**; Q_th = 54 · 5/60 = **4,50 kWh**; AZ_Pth = **4,54**; ΔQ1506 = 47621 − 47616 = 5 → AZ_1506 = 5,05 (1-kWh-Stufung).
- 1513 − 1490: −2,5 K (15:35) → +1,3 K (16:05), Mittel −0,54 K.

## Bewertung
- **Überhöhung wirkt [sicher]:** 1525 − 1490 am Laufende sinkt in beiden Bändern um ~1 K (8,80 → 7,50 bzw. 8,65 → 7,70 K). Die zwei neuen Läufe (7,6 / 8,0 K) bestätigen das. Am Laufmittel ist der Effekt kleiner (−0,1 bis −0,85 K), weil der Lauf früher endet.
- **HK1-Ist unter Soll [sicher Messung, Deutung wahrscheinlich]:** Laufmittel 1513 − 1490 ist NACH nicht schlechter (Band 4,5–6,5: −0,94 vs. −1,37 K). Über alle Heizbetriebsminuten des 01.11. aber 56 % mehr als 1 K unter Soll – höher als an jedem Referenztag (32–44 %); Mittel −1,27 K liegt innerhalb der Referenz (−0,85 … −1,71 K). Deutung: in den Pausen zwischen kürzeren Läufen sinkt HK1 tiefer ab [wahrscheinlich].
- **Kürzere Läufe, mehr Starts [Messung sicher, Ursache Vermutung]:** Band 3,0–4,5: 56 → 35 min (n = 5 / 3); gesamt 37,6 → 30,8 min; 01.11. 27,9 min/Start gegen 37,8 am gleich kalten 25.10., 12 statt 9 Starts. Mechanismus wahrscheinlich: niedrigeres WP-Soll → Abschaltkriterium früher erreicht. n ist klein, die Streuung der Referenz groß (24.10./28.10. auch 30 min/Start).
- **Arbeitszahl eher schlechter, nicht besser [wahrscheinlich, n klein]:** 01.11. AZ_Pth 4,12 / AZ_1506 4,11 gegen 25.10. 4,37 / 4,30 bei gleicher AT (−0,2 bis −0,25); Läufe im Band 4,5–6,5: 4,45 → 4,17. Das widerspricht dem erwarteten Gewinn (+2 %/K ≈ +0,09) und passt zum höheren Anlaufanteil der kürzeren Läufe. Mit einem Tag und 12 Läufen nicht signifikant (Tagesstreuung VOR 4,37–4,97, stark AT-abhängig) [sicher].
- **Komfort unverändert [wahrscheinlich]:** Raum 1510 am 01.11. 21,49 °C (min 20,6) – gleich wie 25.10. (21,51 / 20,9). Abends ab 17:20 sogar Heizpause bei 22,0–22,5 °C. Wärmebedarf 01.11. (41,2 kWh_th) ≈ 25.10. (44,8) → der Mehrbedarf aus dem 15:50-Zwischenstand war eine Fensterfrage (Nacht/Vormittag), kein Tagestrend [wahrscheinlich].
- **Zwischenurteil:** 2,0 K weiter halten bis 07.11.; kein Komfortproblem. Ein Effizienzgewinn ist bisher **nicht** belegt, eher ein leichter Verlust durch Takten. Wenn sich das bis 07.11. bestätigt (AZ im Band ≤ VOR, min/Start kürzer), spricht das für Rückkehr auf 3,0 K (30684 = 30) oder für Kombination mit längerer Laufzeit (Hysterese/Kurzlaufschutz) statt weniger Überhöhung [Vermutung].

## Offen
- Abnahme 07.11.2026: gleiche Methode, Ziel ≥ 30 Läufe NACH; Kennzahlen je Band: min/Start, AZ_Pth, Anteil HK1 < Soll −1 K.
- Lauf 97 (01.11. 20:15, Verdichter mit 1490 = 0 und 1501 = 0): Ursache klären (Hoval-eigene Anforderung, Frostschutz, Puffer?) – im Journal `SET reg 1490` um 20:10–20:20 nachsehen.
- 19870 im Volllogger konstant 0 → Logger-Spalte prüfen (HoxPi liefert den Wert live laut Projektanweisung); bis dahin WW nur über 1504/1539.
- Statuseintrag `[lokaler Pfad]`: HK1-VL-Ist = Reg 1513 (nicht 18760) – weiterhin offen.
