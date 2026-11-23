# F56 – Heizlast-Kennlinie aus Messung (Analyse-Agent, 01.11.2026)

Nur gelesen. An Anlage, Loxone und Pi-Diensten nichts geändert. Hilfsskript nur auf dem Pi: `/tmp/f56_heizlast_20261101.py`, Ausgabe `/tmp/f56_heizlast_20261101.out`.

## Frage
Wie viel Heizwärme (ohne WW) braucht das Haus je Tag in Abhängigkeit vom Tagesmittel der Außentemperatur? Wo liegt die Heizgrenze, welche mittlere Leistung ergibt sich bei −15 °C (Projektannahme 3–5 kW), und wie passt das zur kleinsten WP-Leistung (~7–8 kW, Mod 35 %, A-7/W35)?

## Datenquelle
| Kürzel | Quelle | Inhalt |
|---|---|---|
| [VL] | Pi `~/hoxpi_fulllog/2026-09-01.csv.gz` … `2026-10-30.csv.gz`, `2026-10-31.csv`, `2026-11-01.csv` (5 min, Spalten per Kopfzeile) | 1477 AF1 außen (×0,1 °C), 1490 HK1-Soll von Loxone (×0,1 °C), 1510 Raum-Ist HK1 (×0,1 °C), 27484/27485 Wärmemenge Heizen (hi/lo, kWh), 27488/27489 Wärmemenge WW, 27486/27487 Wärmemenge Kühlen, 1505/1506 Wärmemenge gesamt, 25614 Strom gesamt (kWh), 1519 Starts |
| [REG] | hoxpi `search_registers("Wärmemenge")` 01.11.2026 | 27485 „Wärmemenge Heizen_low“ 7,425 MWh-Anzeige, 27489 „Wärmemenge WW_low“ 40,194, 1506 gesamt 47,619 (je + High-Word ×65 536 kWh) |
| [OFEN] | `[lokaler Pfad]` | Ofen-Nachlauf (seit 27.09.) setzt 1490 = 240 (24,0 °C); 25.09. von der Betreiber als Ofenabend bestätigt |
| [KF] | `[lokaler Pfad]` Punkt 2 | Kühlmodus-Falle WZ 20.–22.10. (~36 h) und 22./23.10. (~11 h) |
| [ALT] | `[lokaler Pfad]` | frühere Schätzung ~80 W/K (20.–22.10.), 3–5 kW bei −15 °C |

## Methode
- Tageswärme Heizen = (27484·65 536 + 27485) im **ersten gültigen Datensatz des Folgetags** minus im ersten gültigen Datensatz des Tages (≈ 00:00 Ortszeit, Datei-Zeitstempel). Nullwerte (Busausfall) übersprungen. WW (27488/89) und Kühlen (27486/87) getrennt, **nicht** mitgezählt [VL].
- Plausibilität: gesamt (1505/1506) − Heizen − WW − Kühlen = **0 kWh an jedem Tag 02.09.–31.10.** → die drei Teilzähler sind vollständig und konsistent [sicher, VL]. (01.09. ein Fehlwert im WW-Zähler, nicht verwendet.)
- AT-Tagesmittel = Mittel aller 5-min-Werte von 1477 (vorzeichenbehaftet) [VL].
- Ofentag = mindestens ein 5-min-Wert 1490 = 240 (Loxone-Ofen-Nachlauf aktiv) [OFEN], zusätzlich 25.09. (bestätigt). Gegenprobe: an allen diesen Tagen 1510 abends (17–24 h) ≥ 23,4 °C, sonst ≤ 22,9 °C (Ausnahme 24.09. 24,2 °C, s. Offen) [VL].
- „Folgetag“ = erster Tag nach einem Ofentag ohne eigenen Ofen (Estrich/Raum noch vorgewärmt).
- Lineare Regression kWh_th/Tag = a + b·AT (kleinste Quadrate), 95-%-Vertrauensbereich der **Mittelwertgeraden** bei −15 °C (t-Verteilung). Heizgrenze = −a/b.
- Auswertezeitraum Hauptfit: **22.09.–31.10.** (durchgehend Heizbetrieb, Zähler lückenlos). Erste Heizwärme überhaupt am 12.09. (26 kWh).
- 1-kWh-Auflösung des Zählers → ±1 kWh je Tag, vernachlässigbar gegen die Tagesstreuung.

## Ergebnis – Regression
| Fit | Tage | n | Gerade kWh_th/Tag | R² | Streuung s | Heizgrenze | Q(−15 °C) mittel ± 95 % |
|---|---|---|---|---|---|---|---|
| A alle Tage | 22.09.–31.10. | 40 | 57,9 − 3,43·AT | 0,55 | 9,3 kWh/d | 16,9 °C | 109 ± 26 kWh/d = **4,6 ± 1,1 kW** |
| B ohne Ofentage | dto. | 32 | 56,8 − 3,28·AT | 0,53 | 9,7 | 17,4 °C | 4,4 ± 1,3 kW |
| C ohne Ofen + Folgetag | dto. | 27 | 61,1 − 3,53·AT | 0,56 | 9,8 | 17,3 °C | 4,8 ± 1,4 kW |
| **D = C ohne Kühlfalle 20.–22.10.** | dto. | **24** | **64,1 − 3,76·AT** | **0,70** | 7,9 | **17,1 °C** | 120 ± 29 kWh/d = **5,0 ± 1,2 kW** |
| E wie D, ab 12.09. | 12.09.–31.10. | 34 | 63,8 − 3,73·AT | 0,68 | 7,9 | 17,1 °C | 5,0 ± 1,1 kW |
| F 3-Tage-Blöcke, alle | 22.09.–29.10. | 13 | 56,3 − 3,30·AT | 0,76 | – | 17,1 °C | 4,4 ± 1,3 kW |
| G 3-Tage-Blöcke ohne Ofen | dto. | 8 | 68,6 − 4,14·AT | 0,82 | – | 16,6 °C | 5,5 ± 2,2 kW |
Quelle aller Zeilen: Tagestabelle unten [VL], Rechnung lokal (numpy/scipy).

**Kernaussagen**
- **Steigung 3,3–3,8 kWh/Tag je K = 140–157 W/K** (Fit D: 157 W/K) für die WP-Heizwärme [sicher als Messwert; Interpretation als Gebäude-H wahrscheinlich]. Das ist rund **doppelt so viel wie die 80 W/K** aus [ALT]; [ALT] rechnete genau mit 20.–22.10., also mit Tagen in der Kühlfalle → zu niedrig [wahrscheinlich].
- **Heizgrenze 16,6–17,4 °C Tagesmittel**, robust über alle Varianten [sicher für die Daten]. Sie fällt mit der eingestellten Heizgrenze 17 °C zusammen [KF Abschnitt 2 „nicht anfassen“] – die Regelung bestimmt die Grenze also mit [wahrscheinlich].
- **Mittlere Heizleistung bei −15 °C: ~5 kW (Bandbreite 3,8–6,2 kW, 95 %, Fit D)** [wahrscheinlich]. Projektannahme 3–5 kW → **oberes Ende bestätigt, eher 4–6 kW**.
- **Vorbehalt Extrapolation:** kältestes Tagesmittel im Datensatz 4,6 °C (25.10.). −15 °C liegt 20 K außerhalb; der Vertrauensbereich gilt nur, wenn das Gebäude linear bleibt (gilt physikalisch für Transmission/Lüftung), Sonnengewinne im Winter kleiner sind (→ eher **mehr** Bedarf) und Raum-Soll gleich bleibt [Vermutung].
- R² der Tageswerte nur 0,55–0,70: Ursache ist die Speichermasse (τ ~225 h laut [ALT]), WW-Vorrang-Unterbrechungen und Sonne. 3-Tage-Blöcke heben R² auf 0,76–0,82 ohne die Steigung grob zu ändern [sicher].

## Ergebnis – Ofentage
| Tag | AT | Heizen kWh | 1510 Abend max | 1490=240 (5-min-Werte) | Modell C | Abweichung |
|---|---|---|---|---|---|---|
| 25.09. | 9,5 | 18 | 24,0 | 0 (vor Nachlauf, bestätigt) | 27,4 | −9 |
| 10.10. | 10,1 | 23 | 23,9 | 11 | 25,3 | −2 |
| 11.10. | 9,9 | 12 | 23,4 | 5 | 26,2 | −14 |
| 16.10. | 9,8 | 27 | 25,8 | 46 | 26,7 | 0 |
| 17.10. | 11,0 | 10 | 24,0 | 19 | 22,4 | −12 |
| 18.10. | 11,9 | 11 | 24,0 | 35 | 19,1 | −8 |
| 23.10. | 5,6 | 49 | 24,7 | 12 | 41,4 | +8 |
| 26.10. | 6,5 | 37 | 24,0 | 17 | 38,2 | −1 |
| Folgetage 26.09./12.10./19.10./24.10./27.10. | – | 13/20/7/32/29 | ≤ 22,2 | 0 | – | −10/−9/−15/−9/−5 |
- Ofentage und **vor allem die Folgetage** liegen im Mittel ~8 kWh/Tag unter der Kennlinie [sicher als Zahl]; die Ofenwärme ersetzt ≈ 0,3 kW WP-Wärme über 2 Tage [wahrscheinlich]. Am Ofentag selbst läuft die WP teils trotzdem (Nachlauf hält Kreise offen, 16.10. / 23.10.).

| Tag | AT mittel (min/max) °C | Heizen kWh | WW kWh | Strom kWh | Starts | 1510 mittel / Abend max °C | 1490=240 | Marke |
|---|---|---|---|---|---|---|---|---|
| 12.09. | 13,6 (9,2/20,1) | 26 | 11 | – | 9 | 21,3 / 22,1 | 0 | |
| 13.09. | 14,7 (9,9/20,6) | 0 | 7 | – | 1 | 21,4 / 22,5 | 0 | |
| 14.09. | 15,8 (11,7/20,3) | 1 | 22 | – | 3 | 21,2 / 21,9 | 0 | |
| 15.09. | 14,9 (10,6/21,5) | 20 | 17 | – | 7 | 21,3 / 22,7 | 0 | |
| 16.09. | 16,6 (12,0/23,6) | 4 | 22 | – | 3 | 21,1 / 22,0 | 0 | |
| 17.09. | 14,1 (10,5/18,3) | 14 | 19 | – | 6 | 20,8 / 21,4 | 0 | |
| 18.09. | 13,8 (10,0/19,2) | 13 | 8 | – | 4 | 21,2 / 22,7 | 0 | |
| 19.09. | 13,8 (9,6/20,0) | 5 | 11 | 0 | 2 | 21,5 / 22,1 | 0 | |
| 20.09. | 14,9 (10,2/21,2) | 12 | 16 | 7 | 5 | 21,3 / 22,3 | 0 | |
| 21.09. | 14,0 (8,6/17,2) | 0 | 10 | 3 | 1 | 21,4 / 22,1 | 0 | |
| 22.09. | 11,2 (7,4/16,5) | 26 | 12 | 9 | 6 | 21,4 / 22,9 | 0 | |
| 23.09. | 10,2 (5,3/16,9) | 18 | 10 | 6 | 7 | 21,8 / 22,2 | 0 | |
| 24.09. | 10,7 (8,2/13,4) | 17 | 30 | 13 | 8 | 21,9 / 24,2 | 0 | (unklar) |
| 25.09. | 9,5 (5,0/15,5) | 18 | 10 | 6 | 7 | 22,3 / 24,0 | 0 | O |
| 26.09. | 10,8 (5,7/18,1) | 13 | 9 | 6 | 7 | 21,3 / 21,3 | 0 | F |
| 27.09. | 12,5 (7,0/19,8) | 18 | 13 | 7 | 6 | 21,3 / 22,3 | 0 | |
| 28.09. | 13,8 (8,7/21,0) | 17 | 18 | 8 | 8 | 21,3 / 22,3 | 0 | |
| 29.09. | 15,1 (10,6/21,7) | 16 | 25 | 9 | 6 | 21,3 / 22,3 | 0 | |
| 30.09. | 15,7 (11,2/21,8) | 8 | 3 | 2 | 3 | 21,4 / 22,2 | 0 | |
| 01.10. | 15,3 (10,7/21,2) | 12 | 4 | 3 | 4 | 21,3 / 22,2 | 0 | |
| 02.10. | 15,1 (11,8/19,6) | 0 | 15 | 4 | 2 | 21,1 / 21,9 | 0 | |
| 03.10. | 14,6 (11,6/19,5) | 14 | 12 | 6 | 7 | 21,2 / 22,3 | 0 | |
| 04.10. | 14,3 (10,2/20,1) | 8 | 38 | 12 | 6 | 21,2 / 22,0 | 0 | |
| 05.10. | 14,4 (10,8/18,9) | 6 | 28 | 9 | 5 | 20,9 / 22,1 | 0 | |
| 06.10. | 12,5 (9,1/18,8) | 17 | 16 | 8 | 7 | 21,2 / 22,2 | 0 | |
| 07.10. | 12,6 (8,2/19,6) | 11 | 26 | 10 | 6 | 21,4 / 22,2 | 0 | |
| 08.10. | 13,5 (11,2/17,4) | 13 | 26 | 10 | 8 | 21,1 / 22,5 | 0 | |
| 09.10. | 10,9 (9,0/13,9) | 0 | 19 | 6 | 3 | 21,4 / 21,9 | 0 | |
| 10.10. | 10,1 (8,8/11,9) | 23 | 19 | 11 | 9 | 21,6 / 23,9 | 11 | O |
| 11.10. | 9,9 (8,3/12,4) | 12 | 26 | 10 | 8 | 22,0 / 23,4 | 5 | O |
| 12.10. | 9,2 (4,7/13,6) | 20 | 19 | 12 | 6 | 21,8 / 22,0 | 0 | F |
| 13.10. | 7,5 (2,1/13,4) | 35 | 21 | 15 | 11 | 21,4 / 21,7 | 0 | |
| 14.10. | 10,8 (8,5/14,1) | 20 | 21 | 10 | 7 | 21,4 / 22,0 | 0 | |
| 15.10. | 11,1 (8,5/15,7) | 37 | 33 | 17 | 11 | 21,5 / 22,2 | 0 | |
| 16.10. | 9,8 (5,5/15,4) | 27 | 16 | 11 | 10 | 22,1 / 25,8 | 46 | O |
| 17.10. | 11,0 (6,7/16,1) | 10 | 29 | 10 | 7 | 22,8 / 24,0 | 19 | O |
| 18.10. | 11,9 (8,7/16,6) | 11 | 17 | 8 | 8 | 22,6 / 24,0 | 35 | O |
| 19.10. | 11,2 (8,3/15,7) | 7 | 34 | 12 | 8 | 22,2 / 22,2 | 0 | F |
| 20.10. | 10,9 (8,7/16,2) | 44 | 15 | 13 | 10 | 21,2 / 22,5 | 0 | K (CAN-Ausfall 12:23–17:10) |
| 21.10. | 13,4 (9,1/15,9) | 5 | 28 | 10 | 6 | 21,5 / 21,5 | 0 | K |
| 22.10. | 7,8 (4,1/11,7) | 12 | 31 | 13 | 7 | 21,2 / 21,7 | 0 | K |
| 23.10. | 5,6 (1,7/10,7) | 49 | 17 | 18 | 11 | 21,8 / 24,7 | 12 | O |
| 24.10. | 5,8 (3,2/8,3) | 32 | 17 | 13 | 10 | 22,1 / 22,0 | 0 | F |
| 25.10. | 4,6 (2,9/6,5) | 44 | 20 | 17 | 12 | 21,5 / 22,0 | 0 | (25 h, Zeitumstellung) |
| 26.10. | 6,5 (4,0/10,6) | 37 | 21 | 16 | 13 | 21,8 / 24,0 | 17 | O |
| 27.10. | 7,8 (4,0/11,9) | 29 | 36 | 18 | 10 | 21,8 / 21,7 | 0 | F |
| 28.10. | 8,5 (5,6/11,6) | 36 | 23 | 15 | 11 | 21,4 / 22,1 | 0 | |
| 29.10. | 7,3 (3,8/10,2) | 36 | 22 | 14 | 12 | 21,2 / 21,9 | 0 | (Busausfall 08:55–10:42) |
| 30.10. | 6,8 (3,8/9,9) | 53 | 18 | 19 | 15 | 21,3 / 22,2 | 0 | |
| 31.10. | 7,1 (5,5/11,0) | 39 | 39 | 21 | 11 | 21,7 / 21,9 | 0 | |
Summe 22.09.–31.10.: Heizen 850 kWh in 40 Tagen = 21,3 kWh/d; Blockmittel 23.–31.10.: AT 6,7 °C, **39,4 kWh/d = 1,64 kW** [VL].
Strom 12.–18.09. leer: Zähler 25614 stand still bzw. 0 (bekannt aus `ANALYSE_F50_Loxone_WP_Stromzaehler_Datenqualitaet_20261029.md`). Zählerdifferenzen über die Busausfälle 20.10./29.10. sind gültig (der Zähler holt nach) [sicher].

## Vergleich mit der Wärmepumpenleistung (Fit D)
| AT Tagesmittel | Heizwärme mittel | nötige Laufzeit bei 7–8 kW Minimum | Bemerkung |
|---|---|---|---|
| 7 °C (heute) | 37,8 kWh/d = 1,6 kW | 20–22 % ≈ 5 h/Tag | gemessen 23.–31.10.: 1,64 kW [sicher] |
| 0 °C | 64 kWh/d = 2,7 kW | 33–36 % | extrapoliert [wahrscheinlich] |
| −7 °C | 90 kWh/d = 3,8 kW | 47–54 % | [wahrscheinlich] |
| −15 °C | 120 kWh/d = 5,0 kW (3,8–6,2) | 50–83 %, Mitte ~67 % | [wahrscheinlich, Extrapolation] |
- Minimum 7–8 kW (Mod 35 %, A-7/W35) aus Projektbeschreibung/Datenblatt; bei wärmerer Luft liegt die Mindest-Heizleistung eher höher → Laufanteil bei +7 °C eher < 20 % [Vermutung].
- Die WP ist damit bei Normaußentemperatur **~1,5-fach** (Min.-Leistung) bzw. ~3-fach (Nennleistung 14,8 kW) zu groß, nicht 3–5-fach gegenüber dem Minimum. Takten bleibt den ganzen Winter bauartbedingt, nimmt aber zu −15 °C hin klar ab [wahrscheinlich].
- Der 6-kW-Heizstab der WP wird für die Heizlast nie gebraucht; Reserve der WP auch bei −15 °C ≥ 2× [wahrscheinlich].
- Ohne Ofen und ohne WW. Mit WW (~20 kWh/d, [VL]) ist der Gesamtwärmebedarf bei −15 °C ~140 kWh/d ≈ 5,8 kW Mittel [wahrscheinlich].

## Stichprobe (nachprüfbar)
30.10.2026, Datei `~/hoxpi_fulllog/2026-10-30.csv.gz`, erste Zeile `2026-10-30 00:00:02`: 27484 = 1, **27485 = 7296**, 27489 = 40127, 1477 = 38 (3,8 °C).
Ende: Datei `~/hoxpi_fulllog/2026-10-31.csv`, erste Zeile `2026-10-31 00:00:02`: 27484 = 1, **27485 = 7349**, 27489 = 40145 (letzte Zeile 30.10. `23:55:02` ebenfalls 7349).
→ Heizen **53 kWh**, WW 18 kWh, Tagesmittel AT 6,83 °C; Modell D: 64,1 − 3,76·6,83 = 38,4 kWh → Tag liegt +15 kWh (≈ 2 s) über der Linie (kältester Wochenteil nach Ofenpause, Speicher nachgeladen) [sicher als Messung].
Prüfbefehl: `py -3 [lokaler Pfad] "zcat ~/hoxpi_fulllog/2026-10-30.csv.gz | head -2 | cut -d, -f1,2,369,370,373,374"` (Spalten laut Kopfzeile dieser Datei).

## Offen
- **Kalte Tage fehlen:** kein Tagesmittel unter 4,6 °C. Neu rechnen, sobald ≥ 10 ofenfreie Tage unter 0 °C vorliegen (Skript auf dem Pi wiederverwendbar, Enddatum im Skript anpassen) → dann −15-°C-Wert mit halbem Fehlerband.
- **24.09.:** Raum abends 24,2 °C ohne Nachlauf-Signal, bisher nicht als Ofen gezählt ([OFEN] ebenso). Ändert die Fits kaum (liegt nur im Fit A/B/C, nicht als Ausreißer).
- **Sonne nicht getrennt:** warme Tage sind oft sonnige Tage → Steigung evtl. etwas überschätzt, Winterbedarf bei −15 °C bei weniger Sonne aber eher höher; beides ±10–20 % [Vermutung]. Globalstrahlung aus Loxone-Wetter oder PV-Ertrag als zweite Variable wäre der nächste Schritt.
- **OG-Versorgung ungeklärt:** Der Hoval-Zähler Heizen erfasst alle WP-Heizwärme; ob das OG voll beheizt wird, ist offen → bei späterem Zuschalten steigt die Kennlinie [Vermutung].
- **Holzofenwärme** ist nicht gemessen; Ofen+Folgetage nur ausgeschlossen, nicht korrigiert.

## Was bringt uns das
- **Projektannahme korrigieren:** Heizlast bei −15 °C **~5 kW (4–6 kW)** statt 3–5 kW, Gebäudekennwert WP-seitig ~150 W/K statt 80 W/K. Die alte 80-W/K-Zahl stammt aus Kühlfalle-Tagen und sollte nicht weiter verwendet werden [wahrscheinlich].
- **Überdimensionierung relativieren:** gegen das WP-Minimum nur ~1,5-fach bei −15 °C; heute (+7 °C) ~4–5-fach. Takt-Optimierungen (MinHr, Puffer) wirken vor allem in der Übergangszeit; im Kernwinter nimmt das Takten von selbst ab.
- **Heizgrenze 17 °C passt:** Messung und Einstellung decken sich, kein Handlungsbedarf.
- **Ofen messbar:** ein Ofenabend spart grob 8 kWh_th (≈ 1,6–2 kWh Strom bei AZ ~4–5) verteilt auf Ofen- und Folgetag [wahrscheinlich].
- **Referenzlinie für den Winter:** Q = 64 − 3,76·AT kWh/Tag. Liegt ein ofenfreier Tag deutlich darunter, ist das ein Hinweis auf Kühlfalle/geschlossene Ventile; deutlich darüber auf Lüftung/Fenster oder höhere Raumsoll – einfacher Tagescheck für Orchestrator/Wochenbilanz.