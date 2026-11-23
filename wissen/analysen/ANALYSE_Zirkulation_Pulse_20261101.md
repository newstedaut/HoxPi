# F64 Zirkulation: Pulse je Tag und WW-Abfall je Puls – 01.11.2026 (Claude Code für den Orchestrator, nur lesend)

## Frage


## Datenquelle
| Quelle | Inhalt | Zeitraum |
|---|---|---|
| Loxone-MCP `control_statistics` raw, Baustein „Zirkulationspumpe“ (InfoOnlyDigital, Raum Zentral, UUID <UUID> = Relais Q3) | 573 Flanken 0/1 mit Sekundenzeitstempel (UTC) | 23.10. 03:14Z – 01.11. 16:18Z |
| Volllogger-Kopien `[lokaler Pfad] … 2026-11-01.csv` (5 min, Ortszeit, Spalte `zeit`) | `1500` WW oben (×10), `1539` Betriebsart WEZ (4 = WW-Ladung, 1 = Heizen), `25611` (≥ 30 bei Verdichterlauf, auch im Heizbetrieb) | 23.10. 00:00 – 01.11. 16:55, 2 808 Zeilen |
| Loxone-Projektdatei `[lokaler Pfad] Config\Projects\Fam der Betreiber UMBAU.Loxone` | Pulslogik (Monoflop 240 s, Freigabe 05:00–23:30, Morgen 05:20) – übernommen aus Analyse 22.10., heute nicht neu gelesen | – |

Zeitumrechnung: UTC+2 bis 25.10. 03:00, danach UTC+1. Zeilen 25.10. 02:00–02:59 (doppelte Stunde) verworfen.

## Methode
1. **Pulse/Tag** [sicher]: steigende Flanke = Pulsbeginn, je Ortstag gezählt. 10 Einträge sind „0 ohne vorausgehende 1“ (23.10.: 5, 24.10.: 4, 25.10.: 1) → als fehlende Einschaltflanke gewertet, Beginn = Aus − 4 min.
3. **Gegenprobe Tagesfenster**: 30-min-Fenster ab Pulsbeginn gegen 30-min-Fenster ohne Puls (05–23 h) und Nachtfenster; Stundenregression ΔT ~ Pulsanzahl. Mit dem Filter `25611 < 30 und 1539 ≠ 4` bleiben nur 9 isolierte Pulsfenster/19–23 Stunden übrig (Heizbetrieb hält 25611 tagsüber oft ≥ 30) → nur Gegenprobe, Zapfung nicht getrennt.
4. **Abstandsverteilung** der Pulse (Ende vorheriger → Beginn nächster) für die Hochrechnung warm/kalt.

## Ergebnis

### 1. Pulse je Tag [sicher] (Loxone-Statistik Q3, Ortstag)
| Tag | Pulse | Laufzeit min | davon ohne Ein-Flanke |
|---|---|---|---|
| Fr 23.10. | 29 | 132,8 | 5 |
| Sa 24.10. | 22 | 94,2 | 4 |
| So 25.10. | 27 | 117,7 | 1 |
| Mo 26.10. | 39 | 167,9 | 0 |
| Di 27.10. | 34 | 159,6 | 0 |
| Mi 28.10. | 27 | 118,5 | 0 |
| Do 29.10. | 32 | 131,6 | 0 |
| Fr 30.10. | 30 | 125,5 | 0 |
| Sa 31.10. | 32 | 145,9 | 0 |
| So 01.11. (bis 17:18) | 19 | 89,5 | 0 |
| **Mittel 9 volle Tage** | **30,2** (22–39) | **133** (≈ 2,2 h) | |

- Abstand Pulsende → nächster Pulsbeginn (290 Abstände): < 5 min 68 · 5–20 min 99 · 20–60 min 64 · > 60 min 59 [sicher]. → **58 % der Pulse treffen eine noch warme Leitung**, ~20 % (≈ 6/Tag) eine ausgekühlte.
- Pulsrate gegenüber 19.–22.10. (47/28/37/31) unverändert → die vorgeschlagene 20-min-Sperre (V1) ist **nicht** aktiv [wahrscheinlich; Projektdatei heute nicht neu geprüft].

Volllogger Reg 1500 (°C), alle Fenster mit `1539` = 1/0/8 (kein WW-Laden), nächster Puls jeweils ≥ 06:20.
| Tag | 04:00 | 05:20 | Nachtdrift K/h | 05:50 | Überschuss 30 min K | 06:20 | Überschuss 60 min K |
|---|---|---|---|---|---|---|---|
| 25.10. | 50,3 | 49,9 | −0,30 | 49,6 | −0,15 | 49,2 | −0,40 |
| 26.10. | 49,5 | 49,1 | −0,30 | 48,9 | −0,05 | 48,5 | −0,30 |
| 27.10. | 48,3 | 48,0 | −0,23 | 47,5 | −0,39 | 47,3 | −0,48 |
| 28.10. | 47,7 | 47,5 | −0,15 | 47,1 | −0,33 | 46,9 | −0,45 |
| 29.10. | 51,7 | 51,4 | −0,23 | 51,3 | +0,01 | 50,8 | −0,38 |
| 30.10. | 50,3 | 49,9 | −0,30 | 49,6 | −0,15 | 49,5 | −0,10 |
| 31.10. | 47,3 | 47,1 | −0,15 | 46,5 | −0,53 | 46,5 | −0,45 |
| **Mittel (n = 7)** | | | **−0,24** | | **−0,23** (Median −0,15) | | **−0,37** (Median −0,40) |
- 01.11.: zwei Pulse (05:20 + 05:32), 05:20→05:50 −0,8 K bei Drift −0,30 K/h → Überschuss −0,65 K = **−0,33 K/Puls** (bestätigt die Größenordnung; ab 06:00 WW-Ladung).
- **Ein Puls auf kalte Leitung (≥ 6 h Stillstand) kostet 0,23–0,37 K am Fühler oben ≈ 0,11–0,17 kWh Wärme** (× C = 0,47 kWh/K) [wahrscheinlich]. Passt physikalisch zum Aufheizen von ~20 m gedämmter Leitung (≈ 0,12 kWh, Annahme aus Analyse 22.10.). Einschränkung: Auflösung 0,1 K, 5-min-Raster, Fühler oben ≠ ganzer Speicher.

### 3. Gegenprobe tagsüber (mit Kleinzapfung vermischt) [wahrscheinlich, Obergrenze]
| Fenster (30 min, Filter 25611 < 30 & 1539 ≠ 4) | n | Median K | Mittel K |
|---|---|---|---|
| ab Pulsbeginn, isoliert (kein anderer Puls ±30 min) | 9 | −0,50 | −0,69 |
| ab Pulsbeginn, alle | 60 | −1,25 | −1,59 |
| Tag 05–23 h ohne Puls | 21 | −0,20 | −0,18 |
| Nacht 23:30–04:30 | 52 | −0,20 | −0,18 |
- Stundenregression 05–23 h: **−0,47 K/Puls** (ohne Großzapfung, n = 19 h) bzw. −0,55 K/Puls (alle, n = 23 h).

### 4. Hochrechnung kWh/Tag
| Pulsklasse (Abstand zum Vorpuls) | Pulse/Tag | kWh/Puls | kWh/Tag | Sicherheit |
|---|---|---|---|---|
| kalt (> 60 min) | 6,1 | 0,11–0,17 | 0,7–1,0 | wahrscheinlich (gemessen) |
| mittel (20–60 min) | 6,7 | 0,05–0,09 | 0,3–0,6 | Vermutung (halber Kaltwert) |
| warm (< 20 min) | 17,4 | 0,02–0,04 | 0,3–0,7 | Vermutung (4 min Leitungsverlust + Nachheizen) |
| **Summe** | **30,2** | | **≈ 1,4–2,3 kWh Wärme/Tag** | Vermutung |
- ≈ 0,45–0,8 kWh Strom/Tag bei WW-AZ ~3,0 → ~165–290 kWh Strom/Jahr [Vermutung].
- Anteil am WW-Tagüberschuss (~7 kWh, Argon) ≈ 20–30 %; Rest = Zapfung.
- Eine 20-min-Sperre (V1, Analyse 22.10.) würde fast nur die „warm“-Klasse treffen → ~0,3–0,7 kWh Wärme/Tag Ersparnis [Vermutung], deckt sich mit der früheren Schätzung 0,4–0,8.

## Stichprobe (nachprüfbar)
- Volllogger `[lokaler Pfad]`, Spalte `1500`: **04:00:01 = 473**, **05:20:01 = 471**, **05:50:01 = 465**, 06:20:02 = 465; Spalte `1539` = 1 (Heizen) bzw. 0, nie 4.
- → Drift vorher −0,2 K/80 min = −0,15 K/h; nach Puls −0,6 K/30 min; Überschuss −0,53 K ≈ 0,25 kWh (höchster Einzelwert der Reihe).

## Offen
1. **Kosten eines Pulses auf warme Leitung** (58 % aller Pulse) sind nicht gemessen, nur geschätzt. Tagsüber fällt jeder Präsenzpuls mit Zapfung zusammen.
2. Fehlender Datenpunkt: **Zirkulations-Rücklauftemperatur** (kein Fühler, Hoval 19755 leer) und **Zapfmenge/Kaltwasserdurchfluss**. Beides bräuchte Hardware.
5. Pulsrate 30/Tag ist gegenüber 22.10. unverändert → Sperre V1 ist nicht eingebaut (Entscheidung der Betreiber).