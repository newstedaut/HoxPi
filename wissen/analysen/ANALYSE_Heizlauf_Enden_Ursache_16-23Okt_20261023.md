# Heizlauf-Enden 16.–23.10.2026 – wer schaltet den Verdichter im Heizbetrieb ab?

> → Korrektur 25.10.2026 (ersetzt den Vermerk vom 23.10.): soweit hier mit 300 l / 0,349 kWh/K gerechnet wird, gilt verbindlich das wirksame WW-Volumen des CombiVal ESR 400 von ~405 l, C = 0,47 ± 0,04 kWh/K (F1, 20 zapffreie Ladungen, `[lokaler Pfad]`). Speicher-Wärmemengen und Verluste hier um Faktor 1,35 (+35 %) nach oben korrigieren, nicht +26 %. (EnerVal 300 = Puffer, CombiVal ESR 400 = WW.)
Agent ag1, 23.10.2026 · nur lesend · Quelle: Volllogger `~/hoxpi_fulllog/2026-10-16…23.csv(.gz)` (Kopien `Emulation\or_ag1_2026-10-*.csv*`), 2136 Punkte 16.10. 00:00 – 23.10. 09:55.
Skripte: `Emulation\or_ag1_enden.py` (Läufe, Starts, Energie), `or_ag1_enden2.py` (Klassen mit 1501/18768, WW-Segmente), `or_ag1_wwsoll.py` (WW-Soll 1497), `or_ag1_peek.py`/`or_ag1_peek2.py` (Rohzeilen).

**Methode:** Heizlauf = zusammenhängende 5-min-Punkte mit 1539 = 1 (Heizen) und 18726 > 0. Ende = letzter Punkt mit 1539 = 1. Klasse am **ersten Folgepunkt**:
(a) 1539 = 4 (WW) · (c-Lox) 1501 → 0 und/oder 18768 → 0 (Heizanforderung „Heizen extern“ = 23 weg) · (b) 1501 bleibt 23, 18768 bleibt 100, RL 1535 − Soll 1529 ≥ 2,0 K · Rest = unklar.
Register: 1477 AT, 1539 WEZ-Status (1 Heizen, 4 WW, 0 Aus), 1501 HK-Status (23 Heizen extern, 6 Zwangsreduktion, 0 Aus), 18768 Anforderung WEZ (100/0), 1529 WEZ-Soll (0 wenn aus), 1535 RL, 18726 Modulation, 25611 P_el (×0,01 kW), 25612 Q_th (ganze kW!), 1497 WW-Soll, 1498 = 45, 1500 WW-Ist.
**Unschärfe 5-min-Raster:** Ende liegt 0–5 min nach dem letzten Laufpunkt; RL steigt am Laufende ~0,5 K/5 min → „dRL am letzten Punkt“ ist ein Unterwert, der erste Aus-Punkt ein Oberwert. Laufdauer = Punkte × 5 min (±5 min; „5 min“ heißt real 1–10 min). 1539 hat zusätzlich bis 60 s Sweep-Nachlauf.

## Alle Heizlauf-Enden (28 Läufe, 27 abgeschlossen)
| # | Start | Ende (letzter Pkt) | min | AT °C | RL | Soll 1529 | dRL letzt / 1. Aus-Pkt | Folgepunkt 1539/1501/18768 | Klasse |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 16.10. 05:50 | 06:05 | 20 | 6,4 | 35,0 | 34,5 | +0,5 / – | 4 / 6 / 100 | **a WW** |
| 2 | 16.10. 07:05 | 07:50 | 50 | 5,6 | 36,5 | 34,0 | +2,5 / +2,5 | 0 / 23 / 100 | **b RL** |
| 3 | 16.10. 08:30 | 08:35 | 10 | 5,5 | 32,0 | 34,0 | −2,0 / −2,0 | 0 / 0 / 0 | c-Lox |
| 4 | 16.10. 13:05 | 13:05 | 5 | 12,7 | 29,0 | 38,5 | −9,5 / −8,5 | 0 / 0 / 0 | c-Lox |
| 5 | 16.10. 13:35 | 13:55 | 25 | 14,1 | 34,0 | 38,0 | −4,0 / −3,0 | 0 / 0 / 0 | c-Lox |
| 6 | 16.10. 14:50 | 15:25 | 40 | 15,4 | 40,0 | 37,5 | +2,5 / +2,0 | 0 / 0 / 0 | c-Lox (RL schon +2,5 → zeitgleich, mehrdeutig) |
| 7 | 16.10. 17:10 | 17:30 | 25 | 14,6 | 39,5 | 37,0 | +2,5 / +2,5 | 0 / 23 / 100 | **b RL** |
| 8 | 16.10. 18:25 | 18:25 | 5 | 12,6 | 35,0 | 37,0 | −2,0 / −1,5 | 0 / 0 / 0 | c-Lox |
| 9 | 17.10. 08:45 | 09:05 | 25 | 7,8 | 34,5 | 33,5 | +1,0 / +1,0 | 0 / 0 / 0 | c-Lox (1501 schon am letzten Pkt 0) |
| 10 | 17.10. 10:00 | 10:20 | 25 | 9,0 | 35,5 | 32,5 | +3,0 / +3,0 | 0 / 0 / 0 | c-Lox (RL schon +3 → mehrdeutig) |
| 11 | 17.10. 18:00 | 18:20 | 25 | 14,2 | 37,0 | 38,0 | −1,0 / −0,5 | 0 / 0 / 0 | c-Lox |
| 12 | 18.10. 07:55 | 08:15 | 25 | 10,2 | 35,0 | 33,0 | +2,0 / +3,0 | 0 / 23 / 100 | **b RL** |
| 13 | 18.10. 14:40 | 14:55 | 20 | 16,2 | 34,0 | 38,0 | −4,0 / −2,5 | 0 / 0 / 0 | c-Lox |
| 14 | 18.10. 18:25 | 18:35 | 15 | 13,3 | 33,0 | 32,5 | +0,5 / +0,5 | 0 / 0 / 0 | c-Lox |
| 15 | 19.10. 07:20 | 07:35 | 20 | 9,7 | 31,5 | 33,5 | −2,0 / −2,0 | 0 / 0 / 0 | c-Lox |
| 16 | 19.10. 09:15 | 09:35 | 25 | 10,0 | 35,0 | 33,0 | +2,0 / +3,0 | 0 / 23 / 100 | **b RL** |
| 17 | 20.10. 07:20 | 08:20 | 65 | 8,7 | 36,5 | 34,0 | +2,5 / +3,0 | 0 / 23 / 100 | **b RL** |
| 18 | 20.10. 09:00 | 09:30 | 35 | 8,8 | 36,0 | 34,0 | +2,0 / +2,5 | 0 / 23 / 100 | **b RL** |
| 19 | 20.10. 10:25 | 10:45 | 25 | 9,6 | 36,0 | 33,5 | +2,5 / +3,0 | 0 / 23 / 100 | **b RL** |
| 20 | 21.10. 15:30 | 15:30 | 5 | 14,3 | 34,0 | 32,0 | +2,0 / +3,0 | 0 / 23 / 100 | **b RL** (Kurzlauf, RL schon warm) |
| 21 | 21.10. 17:30 | 17:50 | 25 | 12,7 | 34,5 | 32,5 | +2,0 / +3,0 | 0 / 23 / 100 | **b RL** |
| 22 | 22.10. 04:25 | 05:00 | 40 | 7,2 | 36,0 | 34,5 | +1,5 / +1,5 | 0 / 0 / 0 | c-Lox |
| 23 | 22.10. 07:25 | 07:45 | 25 | 6,5 | 35,5 | 34,5 | +1,0 / +1,5 | 0 / 0 / 0 | c-Lox |
| 24 | 22.10. 08:20 | 08:30 | 15 | 6,4 | 32,5 | 34,0 | −1,5 / −1,0 | 0 / 0 / 0 | c-Lox |
| 25 | 23.10. 03:05 | 03:40 | 40 | 2,6 | 35,0 | 36,0 | −1,0 / −1,5 | 0 / 0 / 0 | c-Lox |
| 26 | 23.10. 05:40 | 07:20 | 105 | 1,7 | 37,0 | 35,5 | +1,5 / – | 4 / 6 / 100 | **a WW** |
| 27 | 23.10. 08:10 | 08:50 | 45 | 2,3 | 37,5 | 35,0 | +2,5 / +2,5 | 0 / 23 / 100 | **b RL** |
| 28 | 23.10. 09:45 | (läuft 09:55) | ≥15 | 2,2 | 33,5 | 34,5 | – | – | offen |

## Auswertung
| Klasse | Anzahl (von 27) | Laufdauer Ø / Median | dRL am letzten Laufpunkt | dRL am 1. Aus-Punkt |
|---|---|---|---|---|
| (b) WP-eigene Abschaltung, Anforderung steht weiter | **10** (+2 mehrdeutige #6, #10) | 33 / 25 min | +2,0 (5×), +2,5 (5×) | +2,0 … +3,0 |
| (c) Loxone nimmt „Heizen extern“ weg (1501 23→0, 18768 100→0, 1520 → 0) | **15** | 22 / 25 min | −9,5 … +3,0, davon 11× < +2,0 | |
| (a) Umschaltung auf WW | **2** (16.10. 06:05, 23.10. 07:20) | 20 / 105 min | +0,5 / +1,5 | |

Starts je Tag (Verdichter 0 → >0): 16.10. 10 · 17.10. 7 · 18.10. 7 · 19.10. 8 · 20.10. 5 · 21.10. 6 · 22.10. 7 · 23.10. (bis 09:55) 5 → **55 Starts, davon 27 WW-Starts, 28 Heiz-Starts**. Nur **2 Heiz-Starts** (16.10. 07:05, 23.10. 08:10) sind Neustarts nach WW-Abbruch; ein WW→Heizen-Übergang ohne Pause kam **nie** vor (nach WW immer 1539 = 0, ≥ 20 min Pause). Heiz-Kurzläufe ≤ 15 min: 6 (#3, 4, 8, 14, 20, 24), davon 5 durch Loxone beendet.
Außentemperatur Tagesmittel: 16.10. 9,8 · 17.10. 11,0 · 18.10. 11,9 · 19.10. 11,1 · 20.10. 10,9 · 21.10. 13,4 · 22.10. 7,7 · 23.10. 2,6 °C (min 1,7).

**Energie (5-min-Raster, Q_th aus 25612 in ganzen kW → grob, AZ ±0,3–0,5):**
| Betrieb | Punkte | kWh_el | kWh_th | AZ |
|---|---|---|---|---|
| Heizen (1539 = 1) | 160 (13,3 h) | 24,5 | 117 | ~4,8 (Woche überwiegend 8–13 °C; X26-Messung 23.10. bei 2 °C: 4,0–4,2) |
| WW (1539 = 4), 29 Ladungen | 241 (20,1 h) | 59,6 | 184 | ~3,1 |
| davon Morgenfenster 52 °C (9 Ladungen 04:35–07:25) | | 17,4 | 50,2 | **~2,9** (2,39 … 3,36) |
| davon Soll 50 °C (7 Ladungen, Mittag/Abend) | | | | ~3,3 |
| davon Soll 57 °C (12 Ladungen, Mittag/Nachmittag) | | | | ~3,1 |

WW-Soll 1497 (sicher aus Log): täglich **04:30 50 → 52 °C, 07:30 zurück auf 50**; zusätzlich Phasen mit **57 °C** (meist 10–19 Uhr). WW startet jeweils bei 1500 ≈ 1497 − 4,5 K (z. B. 45,2 bei Soll 50; 47,2 bei 52; 52,4 bei 57) → 1498 = 45 ist **wahrscheinlich** die WW-Schaltdifferenz 4,5 K.

## Bewertung
- **Sicher:** Die WP-eigene Abschaltung im Heizbetrieb liegt bei **RL 1535 ≈ Soll 1529 + 2,5 K**: bei allen 10 sauberen b-Enden letzter Laufpunkt +2,0…+2,5, erster Aus-Punkt +2,0…+3,0 (Raster-Unschärfe ±0,5 K). Hypothese aus dem Lauf 23.10. 08:53 an 10 Enden bestätigt; Schwelle exakt +2,5 vs. +2,0/+3,0 ist im 5-min-Raster **nicht** trennbar.
- **Sicher:** Die **häufigste** Ursache ist nicht die WP, sondern der Wegfall der externen Heizanforderung (15 von 27): HK-Status 1501 springt von 23 „Heizen extern“ auf 0, 18768 auf 0, HK-Soll 1520/1490 auf 0 – Betriebsart 1478 bleibt dabei 4. 11 davon bei RL noch unter Soll + 2 K, d. h. die WP hätte weiterlaufen wollen.
- **Sicher:** WW verbraucht in dieser Woche ~71 % des WP-Stroms (59,6 von 84 kWh_el) und stellt die Hälfte der Starts.
- **Wahrscheinlich:** Die 15 c-Enden kommen aus der Loxone-Raumregelung (Räume auf Soll → externe Anforderung weg). Welcher Baustein/Ausgang das Signal setzt, ist aus dem Hoval-Log **nicht ermittelbar** (Loxone-Statistik/Config nötig). Bei #4 (16.10. 13:05–13:20) flattert die Anforderung: aus 13:10, wieder an 13:20, Neustart 13:35.
- **Wahrscheinlich:** Das 52-°C-Morgenfenster ist die teuerste WW-Variante (AZ ~2,9 bei kältester Außentemperatur, 23.10.: 2,4–2,5).
- **Nicht ermittelbar:** echte Stopp-Sekunde und RL genau beim Stopp (5-min-Raster); ob #6/#10 WP- oder Loxone-Ende war (beides im selben Intervall); Wärmepumpen-Mindeststehzeit exakt (Pausen ≥ 15–20 min sichtbar).

## Einstellvorschlag (nur Vorschlag – nichts verstellt, der Betreiber entscheidet)
1. **Loxone-Heizanforderung mit Mindestlaufzeit/Hysterese** statt hartem Abwurf: Anforderung „Heizen extern“ erst wegnehmen, wenn sie ≥ 40–60 min stand, oder an die WP-Logik übergeben (WP schaltet selbst bei Soll + 2,5 K ab). Umsetzung z. B. mit Monoflop/Ausschaltverzögerung vor dem Ausgang ([Loxone Monoflop](https://www.loxone.com/dede/kb/monoflop/), [Intelligente Raumregelung](https://www.loxone.com/dede/kb/intelligente-raumregelung/)). Zuerst lesen, welcher Ausgang 1501 = 23 erzeugt.
2. **52-°C-Morgenfenster 04:30–07:30 auf den Nachmittag verlegen** (z. B. 13:00–16:00, wärmste Stunden/PV), morgens Soll 50 lassen. Dann startet WW morgens erst bei 1500 ≤ 45,5 statt ≤ 47,5 °C – die typischen Morgenwerte 47,2–47,3 °C lösen keine Ladung mehr aus.
3. 57-°C-Phasen nur bei echtem PV-Überschuss; 10 von 12 starteten bei 1500 ≥ 50 °C (reine Anhebungsladungen).

## Was bringt uns das
- **Loxone-Mindestlaufzeit:** größter Hebel. 15 von 27 Heizläufen wurden extern beendet, 5 davon als Kurzläufe ≤ 15 min. Bei ~10 min schlechtem Anlauf (COP 1,4–2,8, je ~0,3–0,4 kWh_el) sind das grob **3–5 kWh_el/Woche** und ~1 Start/Tag weniger (grobe Schätzung, nicht gemessen).
- **Morgenfenster verlegen:** 9 Ladungen × AZ 2,9 → bei AZ ~3,3 am Nachmittag ~**2 kWh_el/Woche**, dazu die 2 WW-Abbrüche/Woche samt Neustart (~0,7 kWh_el). Starts werden dadurch nicht weniger (Ladung wandert nur), aber der Morgen-Heizlauf läuft ungestört durch.
- Ehrlich: zusammen grob 5–8 kWh_el/Woche bei ~84 kWh_el Verbrauch → **ca. 5–10 %**, vor allem weniger Verschleiß durch Starts. Der eigentliche Stromfresser bleibt WW (71 %) – das Volumen-/Energie-Rätsel der WW-Ladungen (Vermutung oben) ist der nächste Prüfschritt.

## Rohdaten-Stichproben zum Gegenprüfen (Volllogger, Rohwerte ×0,1 °C)
- b-Ende 20.10. 08:20:02: 1539=1, 1501=23, 18768=100, 1529=340, 1535=365, 18726=35, 25611=188 → 08:25:01: 1539=0, 1501=23, 18768=100, 1535=370 (= Soll + 3,0).
- c-Ende 22.10. 05:00:01: 1539=1, 1501=23, 18768=100, 1529=345, 1535=360 → 05:05:01: 1539=0, 1501=0, 18768=0, 1520=0, 1535=360 (Soll + 1,5, Anforderung weg).
- a-Ende 16.10. 06:05:02: 1539=1, 1529=345, 1535=350, 1500=473 → 06:10:01: 1539=4, 1501=6, 1504=1, 1529=560, 1497=520.