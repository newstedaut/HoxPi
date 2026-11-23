# ANALYSE WW-Volumen verbindlich (F1) – 23.10.2026 (Analyse-Agent, nur lesend)

**Frage F1:** Wirksames WW-Volumen des CombiVal ESR 400: 379 l (0,44 kWh/K, Datenblatt) oder ~495 l (0,576 kWh/K, Sept.)?

**Ergebnis in 3 Zeilen**
2. Dazu kommt je Ladung ein **Fixanteil Q0 ≈ 1,3 kWh** (WP-Kreis, Leitungen), den `27489` zählt, der aber nicht im Speicher bleibt. Der Rohquotient Wärme/ΔT ohne Q0-Abzug liegt bei denselben Ladungen bei Median 0,56 (Kaltstarts 0,54). Das ist die alte 0,576. **Sicher.**
3. **Datenblatt (379 l, 0,44 kWh/K) passt, 495 l als Speichergröße ist widerlegt:** 0,576 liegt außerhalb des 95-%-Bereichs, und das Modell „0,576 ohne Fixanteil“ erklärt die Ladungen schlechter (Gegenprobe Abschnitt 4). **Wahrscheinlich.** 0,44 und 0,47 kann ich mit diesen Fühlern nicht trennen.

**Verbindliche Rechenwerte** *(verbindlich seit 25.10.2026 – der Betreiber: „bei neuem Wissen altes immer korrigieren“; Doku, Skill-Kopien, Vault und Memory an diesem Tag nachgezogen, Skript `[lokaler Pfad]`)*
- Speicherinhalt (PV-Stab, Ruheverlust, „wie viel kWh stecken drin“): **0,47 kWh/K**.
- WP-Wärme je Ladung: **Q_WP ≈ 0,47 kWh/K · ΔT(Mittel SF/SF2) + 1,3 kWh**.

**Was bringt uns das**
- Die Zahl ist jetzt aus zapffreien Ladungen belegt, nicht mehr aus Ladungen, in denen gezapft wurde. Sie bestätigt die Vorarbeit (0,51 bzw. Kaltstarts 0,47) und schließt F1 bis auf die Doku-Korrekturen.
- PV-Stab 50 → 62 °C: 0,47 × 12 K ≈ **5,6 kWh** (≈ 2,0 h bei 2,82 kW). Mit der alten 0,576 wären es 6,9 kWh gewesen.
- Ruheverlust aus Temperaturabfall: 0,1 K/h × 0,47 = 47 W (statt 58 W mit 0,576).
- Kleine WP-Ladungen bleiben teuer: Bei ΔT 5 K sind 1,3 von 3,7 kWh (35 %) Fixanteil.

---

## 1. Methode
- **Daten:** `~/hoxpi_fulllog/ww_hires.csv` (Rohwerte ×10; SF2 gemischt skaliert, mit `while >100: /10` korrigiert, SF2 = 0 verworfen) und `~/ww_abnahme.csv` (Klartext, nur während Ladungen). Es sind lokale Kopien in `%TEMP%\or_wwkap\`, Stand 23.10.2026 16:56, nur gelesen.
- **Skripte:** `[lokaler Pfad]` (Ladungen + Ausschluss), `…_2_auswertung.py` (Ergebnis + Gegenprobe), `…_3_stichprobe.py` (Rohzeilen), `…_4_mdtabelle.py` (Tabellen). Zu jedem gibt es eine `.out`-Datei. Kein Bus-Zugriff, nichts geschrieben.
- **Ladung:** SLP an für mindestens 15 min (Lücken bis 3 Zeilen überbrückt). Start ist die letzte Zeile vor SLP an.
- **ΔT:** Mittel (SF `1500` + SF2 `27483`)/2, und zwar 30 min nach Ladeende minus Start.
- **Wärme:** Zähler `27489` (WW-Wärme WP, 1 kWh Auflösung). Gerechnet wird erste minus letzte Abnahme-Zeile der Ladung. Zum Vergleich: Flow `31708` · (VL `18725` − RL `1535`) · 1,163 Wh/(l·K). Abgezogen wird der Ruheverlust 137 W × (Dauer + 30 min).
- **Zapffrei** heißt, keines der folgenden Kriterien greift:
  - **SF2-Sprungdetektor** (Regel `sf2-sprungdetektor`, verschärft von 0,8 auf **0,5 K**): Im Fenster [Start − 20 min, Ende + 30 min] fällt SF2 um höchstens 0,5 K unter sein laufendes Maximum. Damit sind auch Wannen-Gradienten (≥ 8 K in 5 min, Regel `ww-zapfsignatur-sf2-gradient`) abgedeckt.
  - **Nachlauf:** Das Fühlermittel fällt zwischen Ende und +30 min um höchstens 0,3 K unter sein Maximum. Das erfasst Zapfungen, die nur oben sichtbar sind.
- **Sonst sauber:**
  - kein PV-Stab (davor: Mittel +0,3 K ohne SLP; danach: von +30 bis +60 min mehr als +0,5 K)
  - keine neue SLP bis +30 min
  - Abnahme-Abdeckung ≥ 85 %
  - nicht im SF2-Standbild 16.10. 18:00 – 18.10. 11:20
- **SF oben** darf während der Ladung einbrechen, solange SF2 steigt. Das ist Durchmischung, keine Zapfung (Memory `ww-entladedelle-keine-zapfung-sf2`).

## 2. Die 20 zapffreien Ladungen
Temperaturen in °C, Wärme in kWh_th.
- C_roh = (Q`27489` − Verlust)/ΔT30
- C_netto = (Q`27489` − Verlust − 1,32)/ΔT30

| # | Start | Ende | min | SF/SF2 Start | SF/SF2 +30 min | ΔT30 [K] | `27489` Stand | Q `27489` [kWh] | Q Flow·ΔT | C_roh | C_netto |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 08.09. 11:11 | 12:08 | 58 | 45,1/25,9 | 56,5/55,5 | 20,50 | 39152→39162 | 10 | 10,32 | 0,478 | 0,414 |
| 2 | 12.09. 07:41 | 08:22 | 42 | 45,2/30,3 | 51,3/48,9 | 12,35 | 39205→39211 | 6 | 6,82 | 0,473 | 0,366 |
| 3 | 14.09. 05:30 | 06:31 | 61 | 42,3/20,0 | 51,8/48,2 | 18,85 | 39223→39235 | 12 | 12,18 | 0,625 | 0,555 |
| 4 | 15.09. 05:30 | 06:27 | 58 | 43,6/19,7 | 50,6/48,2 | 17,75 | 39245→39256 | 11 | 11,58 | 0,608 | 0,534 |
| 5 | 15.09. 11:48 | 12:31 | 44 | 49,2/38,5 | 55,5/53,5 | 10,65 | 39256→39262 | 6 | 6,81 | 0,548 | 0,424 |
| 6 | 17.09. 15:39 | 16:37 | 58 | 45,5/22,5 | 53,0/50,6 | 17,80 | 39284→39294 | 10 | 10,55 | 0,550 | 0,476 |
| 7 | 18.09. 13:59 | 14:51 | 52 | 46,7/32,0 | 55,4/53,8 | 15,25 | 39303→39311 | 8 | 8,52 | 0,512 | 0,426 |
| 8 | 20.09. 05:30 | 06:32 | 63 | 44,5/19,2 | 53,1/50,7 | 20,05 | 39322→39333 | 11 | 11,28 | 0,538 | 0,472 |
| 9 | 21.09. 10:11 | 11:03 | 53 | 45,2/19,2 | 52,0/48,7 | 18,15 | 39338→39348 | 10 | 10,06 | 0,541 | 0,468 |
| 10 | 22.09. 05:28 | 06:49 | 82 | 45,3/26,2 | 54,9/53,5 | 18,45 | 39348→39360 | 12 | 12,42 | 0,637 | 0,565 |
| 11 | 23.09. 08:44 | 09:45 | 62 | 47,2/19,7 | 52,8/50,5 | 18,20 | 39360→39370 | 10 | 10,39 | 0,538 | 0,465 |
| 12 | 24.09. 05:30 | 06:33 | 63 | 43,7/18,8 | 51,4/48,5 | 18,70 | 39370→39381 | 11 | 11,25 | 0,577 | 0,506 |
| 13 | 25.09. 07:39 | 08:07 | 28 | 50,6/45,1 | 52,7/50,6 | 3,80 | 39402→39405 | 3 | 3,06 | 0,754 | 0,407 |
| 14 | 28.09. 04:44 | 05:51 | 67 | 39,9/22,0 | 53,1/49,8 | 20,50 | 39434→39444 | 10 | 10,74 | 0,477 | 0,413 |
| 15 | 28.09. 11:37 | 12:18 | 42 | 51,3/44,1 | 56,5/55,4 | 8,25 | 39444→39450 | 6 | 6,27 | 0,707 | 0,547 |
| 16 | 02.10. 16:35 | 17:26 | 51 | 46,7/19,9 | 52,3/49,0 | 17,35 | 39482→39491 | 9 | 9,58 | 0,508 | 0,432 |
| 17 | 04.10. 01:11 | 01:47 | 37 | 45,2/41,4 | 51,3/47,9 | 6,30 | 39509→39514 | 5 | 5,44 | 0,769 | 0,560 |
| 18 | 06.10. 11:45 | 12:29 | 45 | 48,0/45,4 | 56,5/55,6 | 9,35 | 39582→39588 | 6 | 6,03 | 0,623 | 0,482 |
| 19 | 08.10. 12:36 | 13:07 | 31 | 51,8/49,5 | 56,3/55,6 | 5,30 | 39631→39635 | 4 | 4,10 | 0,728 | 0,479 |
| 20 | 21.10. 03:56 | 04:30 | 34 | 45,2/40,7 | 51,5/49,3 | 7,45 | 39912→39917 | 5 | 4,75 | 0,651 | 0,474 |

Seit 08.10. gibt es kaum zapffreie Ladungen: Fast jede Ladung wird durch eine Zapfung ausgelöst oder von einer begleitet. Die Messreihe verlängert sich deshalb nur langsam.

### 2.1 Verworfene Ladungen (95 von 115)
| Grund (Mehrfachnennung) | Anzahl |
|---|---|
| Zapfung SF2 ≥ 0,5 K unter Maximum (davon 9 mit nur 0,5–0,79 K) | 87 |
| Zapfung im Nachlauf (Fühlermittel −0,3 K) | 33 |
| PV-Stab davor/danach | 9 |
| SF2-Standbild 16.–18.10. | 7 |
| Abnahme-Abdeckung < 85 % / Datenlücke / neue SLP | 5 |

Die Einzelliste mit Grund je Ladung steht in `[lokaler Pfad]` (zweite Tabelle). Zwei der vier Ladungen der Sept.-Herleitung (16.09. 06:20 und 11:09) fallen dort heraus: Der SF2 fiel um 0,5 K.

## 3. Ergebnis (Quelle: `or_f1_20261023_2_auswertung.out`)
| Größe | Wärme `27489` | Wärme Flow·ΔT |
|---|---|---|
| Regression Q = C·ΔT + Q0: **C** | **0,473 ± 0,035** (Bootstrap-95 % 0,419–0,534) | 0,490 ± 0,033 (0,433–0,552) |
| Q0 (Fixanteil je Ladung) | 1,32 kWh | 1,44 kWh |
| RMSE / R² | 0,83 kWh / 0,909 | 0,78 kWh / 0,924 |
| C_netto Einzelwerte (n = 20) | Median 0,473, s 0,058 | Median 0,478, s 0,060 |
| C_netto nur ΔT ≥ 15 K (n = 12) | Median 0,470, s 0,053 | 0,480, s 0,051 |
| C_roh (ohne Q0), alle 20 | Median 0,564, Spanne 0,47–0,77 | 0,604 |
| C_roh nur ΔT ≥ 15 K | Median 0,539, s 0,053 | 0,556 |
| Liter-Äquivalent C/1,163 | **407 l** | 421 l |

- Mit der Sprungschwelle 0,8 statt 0,5 K kommen 9 Ladungen dazu (n = 29). Das ergibt C = 0,464 ± 0,025 und Q0 = 1,52 kWh. Das Ergebnis ist also stabil gegen die Schwellenwahl.
- Zum Vergleich die Vorarbeit mit 34 Ladungen inkl. Zapfungen: 0,514 ± 0,048 und Q0 1,77. Die zapffreie Auswahl rückt den Wert näher an das Datenblatt und senkt die Streuung.

## 4. Gegenprobe nach Werkzeugregel 6 (gleiche Rechnung mit falschen Annahmen)
Regel aus Memory `werkzeugregel6-nullhypothese`: Ein statistisches Argument gilt erst, wenn dieselbe Rechnung mit falschen Annahmen schlechter ausfällt. Hinweis: Im Journal `loop_journal_archiv_bis_20260919.md` trägt Nr. 6 einen anderen Text („Gerät führt Register ≠ Master benutzt es“), dort steht die Nullhypothesen-Regel als Nr. 5 (R95). Gemeint ist hier die Nullhypothese, so steht es auch in `PLAN_Wissensausbau_20261023.md`.

**(a) Modelle gegen die 20 Ladungen** (`27489`, Fehler in kWh, LOO = Leave-one-out, also Vorhersage jeder Ladung ohne sie selbst)
| Annahme | C | Q0 | RMSE | LOO |
|---|---|---|---|---|
| frei (C und Q0 gefittet) | 0,473 | 1,32 | 0,83 | 0,91 |
| **Datenblatt 0,441 + Q0 gefittet** | 0,441 | 1,78 | 0,85 | **0,89** |
| **Sept.-Annahme 0,576, kein Q0** | 0,576 | 0 | 1,02 | **1,02** |
| 0,576 + Q0 gefittet | 0,576 | −0,14 | 1,01 | 1,06 |
| C gefittet, kein Q0 | 0,554 | 0 | 0,96 | 1,01 |
| Datenblatt 0,441, kein Q0 | 0,441 | 0 | 1,97 | 1,97 |

Lesart:
- Die Sept.-Annahme (495 l, kein Fixanteil) sagt die Ladungen schlechter voraus als jedes Modell mit Fixanteil (LOO 1,02 gegen 0,89–0,91).
- Lässt man bei C = 0,576 ein Q0 zu, wählt der Fit Q0 ≈ 0. Das Modell bleibt trotzdem schlechter.
- **Aber:** 0,441 + Q0 und 0,473 + Q0 sind gleich gut. Die Daten trennen „0,576 ohne Q0“ von „0,44–0,53 mit Q0“, **nicht 0,44 von 0,47**.

**(b) Permutation:** ΔT und Q wurden 10 000-mal zufällig vertauscht. Die Steigung liegt dann im Median bei 0,00, das 99-%-Quantil bei 0,26. Keine einzige Vertauschung erreicht 0,473. Die Steigung ist also echtes Signal und kein Artefakt der Auswahl.

**(c) Falsche Fühler- oder Zeitannahme** (dieselbe Regression)
| ΔT aus | C | Q0 | RMSE | R² |
|---|---|---|---|---|
| Mittel SF/SF2 +30 min (Hauptweg) | 0,473 ± 0,035 | 1,32 | 0,83 | 0,909 |
| Mittel am Ladeende | 0,484 ± 0,032 | 1,93 | 0,75 | 0,925 |
| nur SF oben | 0,728 ± 0,205 | 2,74 | 2,10 | 0,413 |
| nur SF2 unten | 0,272 ± 0,023 | 2,31 | 0,91 | 0,890 |

Einzelne Fühler liefern Unsinn: SF oben allein bringt R² 0,41, SF2 allein ergibt physikalisch unmögliche 234 l. Das Zwei-Fühler-Mittel ist nötig. Ob man am Ladeende oder bei +30 min misst, ändert C kaum (0,47–0,48); es verschiebt nur Q0.

**(d) Falsche Zapfannahme:** Dieselbe Regression nur über die 72 wegen Zapfung verworfenen Ladungen ergibt C = 0,457 ± 0,069, Q0 = 3,0, RMSE 2,35 und R² 0,38. Die Streuung ist dreimal so groß. Der Zapffilter trennt also tatsächlich gestörte von sauberen Ladungen. Die Steigung landet zufällig ähnlich, der Rohquotient (Median 0,79) aber nicht.

**Fazit der Gegenprobe:**
- 495 l bzw. 0,576 als Speicherkapazität besteht die Gegenprobe nicht. **Wahrscheinlich**, denn es liegt außerhalb des 95-%-Bereichs und erklärt schlechter.
- Ein Speicher von 0,44–0,53 kWh/K plus Fixanteil besteht sie.
- Der Unterschied Datenblatt 0,44 gegen gemessen 0,47 ist mit diesen Daten **nicht entscheidbar**.

## 5. Stichprobe zum Selbst-Nachprüfen: Ladung #8, 20.09.2026 05:30–06:32
Quelle: `or_f1_20261023_3_stichprobe.out`. Spaltenköpfe wie in `ww_hires.csv` bzw. `ww_abnahme.csv`; SF = Spalte `WW_Ist`, SF2 = letzte Spalte, beide ×10.
```
ww_hires 2026-09-20 05:30:12,1,0,1,445,4,520,520,0,0,45,260,250,307,294,0,0,0,0,-1270,0,0,0,107,255,192   (Start, SLP=0)
ww_hires 2026-09-20 06:32:52,0,1,1,523,4,500,500,0,0,45,540,490,307,294,0,0,0,0,-1270,0,0,0,105,255,483   (letzte SLP-Zeile)
ww_hires 2026-09-20 07:02:51,0,0,0,531,4,500,500,0,0,45,350,310,307,294,164,10,35,1000,200,23,0,1,103,255,507  (+30 min)
ww_abnahme 2026-09-20 05:31:01,1,1,44.3,52.0,56.0,24.5,23.5,26.0,0,0.0,0,45848,30087,39322,0,0,37.5,10.7,-19.8
ww_abnahme 2026-09-20 06:29:02,1,1,51.7,52.0,56.0,57.5,53.5,57.0,33,2.59,8,45858,30091,39333,0,0,26.4,10.6,5.8
```
Rechnung:
- Mittel Start (44,5 + 19,2)/2 = 31,85 °C. Mittel bei +30 min (53,1 + 50,7)/2 = 51,90 °C. Also **ΔT = 20,05 K**.
- `27489`: 39322 → 39333 = **11 kWh**.
- Verlust 0,21 kWh.
- C_roh = 10,79/20,05 = **0,538**. C_netto = (10,79 − 1,32)/20,05 = **0,472 kWh/K**.

Prüfbefehl Pi (lesend):
```
grep -E '^2026-09-20 (05:[12][0-9]|05:30|06:3[0-3]|07:0[0-3])' ~/hoxpi_fulllog/ww_hires.csv
grep -E '^2026-09-20 0(5:3|6:2)' ~/ww_abnahme.csv
```
Damit kannst du auch nachsehen, dass SF2 von 05:10 bis 07:02 nie um 0,5 K fällt.

Die Abnahme-Datei endet 06:29, SLP läuft bis 06:32. Höchstens ~0,4 kWh könnten dadurch fehlen; das liegt innerhalb der 1-kWh-Auflösung von `27489`.

## 6. Einstufung
**Sicher (aus Rohdaten gerechnet)**
- 20 von 115 Ladungen sind nach den Kriterien in Abschnitt 1 zapffrei.
- Der Rohquotient `27489`/ΔT liegt bei Kaltstarts (ΔT ≥ 15 K) bei 0,54 ± 0,05. Das ist die Größe, die im September als 0,576 = „495 l“ notiert wurde, und sie enthält den Fixanteil.
- Die Steigung Q über ΔT ist echtes Signal (Permutation 0/10 000).

**Wahrscheinlich**
- Wirksame Speicherkapazität **0,47 ± 0,04 kWh/K** (≈ 405 l Wasseräquivalent). Das ist mit dem Datenblatt (379 l ≈ 0,44 kWh/K + Stahl/Email) vereinbar.
- 495 l bzw. 0,576 kWh/K ist als Speichergröße widerlegt.
- Fixanteil Q0 ≈ 1,3–1,5 kWh je Ladung.

**Vermutung**
- Die Restdifferenz 0,47 gegen 0,44 kommt aus Stahl/Email (~0,02 kWh/K, Behältermasse nicht belegt), dem ungeeichten Durchfluss bzw. der 1-kWh-Auflösung von `27489` und der Fühlerlage.

**Nicht entscheidbar mit diesen Daten:** 0,44 gegen 0,47 (Gegenprobe a).

## 7. Vorgeschlagene Korrekturen (nicht ausgeführt, der Betreiber bzw. Orchestrator entscheidet)
1. **`[lokaler Pfad]`**, Abschnitt „Warmwasserspeicher – Hoval CombiVal ESR (400)“, neue Zeile:
2. **„+26 %“-Vermerke** (Kopfzeile „rechnet mit 300 l statt ~379 l – Ergebnis um ca. +26 % zu korrigieren“) in:
   - `ANALYSE_Arbeitszahl_Aussen_20261022.md`
   - `ANALYSE_Arbeitszahl_je_Lauf_19-22Okt_20261022.md`
   - `ANALYSE_Heizlauf_Enden_Ursache_16-23Okt_20261023.md`
   - `ANALYSE_WW_Ladungen_20261021.md`
   - `ANALYSE_WW_Speicherverlust_und_Kurzlaeufe_20261022.md`
   - `BACKLOG.md`
   - `R101_Cwirksam_Eichung_20260921_1915.md`
   - `R101_Hochband_61Grad_20260920_1920.md`
   - `R101_kWh_nach_K_und_Skalenfehler_20260921_1630.md`
   - `R101_SF1SF2_Split_20260921_0730.md`

   Alle liegen unter `[lokaler Pfad]`. Ersetzen durch:
   `> Korrektur 23.10.2026 (F1): rechnet mit 300 l (0,35 kWh/K). Speicherinhalt richtig 0,47 kWh/K → Wärmeinhalte ×1,35 (+35 %). Wurde daraus WP-Ladewärme abgeleitet: Q = 0,47·ΔT + 1,3 kWh. Quelle: ANALYSE_WW_Volumen_verbindlich_20261023.md`
   - Die +26 % (379/300) unterschätzen den Wert. Mit 0,47/0,349 sind es +35 %.
3. **Memory/Skill `ww-speicher-combival-495l-pvstab`** und Skill `hoxpi-heizung`: „~495 l, 0,576 kWh/K“ ersetzen durch „0,47 kWh/K (≈ 405 l äquivalent, F1 23.10.2026); 0,54–0,58 kWh/K = Ladewärme je K bei Kaltstart inkl. Fixanteil 1,3 kWh“. Den Dateinamen „495l“ am besten umbenennen.
4. **`R101_PV_Stab_kWh_K_GELOEST_20260919.md`** (Zeilen 101/114/[Nummer]) und **`R101_Cwirksam_n21_20260922_1909.md`** (Zeile 34: „455–480 l“): je ein Kopfvermerk „überholt durch F1: 0,47 kWh/K“.
5. **`FRAGENKATALOG.md` F1:** Status → **erledigt** (Zahl mit Streuung aus 20 zapffreien Ladungen, Gegenprobe gerechnet). Sobald die Punkte 1–3 eingetragen sind, ist die Abnahme vollständig.
6. **`02_Status_Offen.md`** Zeilen 15/17: Den Widerspruch mit Verweis auf diese Datei schließen. Die dort genannten Werte 0,514 und Q0 1,8 auf 0,47 und 1,3 aktualisieren.