# ANALYSE F83 - Gilt WP011 (15 min) auch vor WW-Ladungen? - Stand 02.11.2026

Daten bis 02.11. 10:55:52. Nur lesend, lokal gerechnet (Pi unverändert). Ersteller: Claude (Subagent F83).

## Kernaussage

1. **Ja: Die 15-min-Sperre gilt vor WW-Ladungen.** Seit 01.10. **113 WW-Ladungen** (F79: 112, plus 02.11. 08:55): **6 Fälle Anforderung < 15 min nach Stopp, alle 6 warten bis Stopp + 15** (Klasse a). Kein Fall startet früher; kleinste mögliche Sperrdauer 14,70 min. [sicher]
2. **Nach Ablauf der Sperre Sofortstart:** 89 Ladungen Anforderung ≥ 18,3 min nach Stopp, Start 0,65-1,17 min nach `WW_Status` = 1 (Median 0,85), ohne Ausnahme (Klasse b). Die rund 50 s sind die normale Kette SLP -> Ladesoll -> Anlauf. [sicher]
3. **Läuft der Verdichter schon, gibt es keinen Stopp und keine Wartezeit:** 18 Ladungen gehen aus dem laufenden Heizen direkt über, P_el nie unter 161 (= 1,61 kW) in den Minuten um den Wechsel (Klasse c). [sicher für 15; bei 3 ist die Reihenfolge Start/Anforderung nicht auflösbar, siehe unten]
4. **Gegenbeispiele zu „immer 15 min“: nur nach Abtauung und nach Regler-Reset.** Von 281 Pausen seit 01.10. sind 16 kürzer als 14,5 min: 14 Abtauung, 1 Reset (18.10.), 1 Standbild (29.10.). **Kein echter Stopp ohne diese Ursachen startet früher.** V107 damit bisher nicht widerlegt. [sicher]
5. **Kosten klein:** 6 von 113 Ladungen (5 %), zusammen 61,5 min Wartezeit, davon ca. 56 min sperrbedingt, in 33 Tagen; WW-Ist fällt in der Wartezeit 0,3-1,2 K. Kein Mehrverbrauch sichtbar, aber nur n = 2. [sicher für Minuten und Kelvin, wahrscheinlich für Energie]

## Tabelle Klasse a: Anforderung < 15 min nach Stopp (6 von 6 nicht widerlegt)

Zeiten aus `~/hoxpi_fulllog/ww_hires.csv`. Stopp = erste Zeile P_el < 20; Sperrdauer = Fenster aus `ww_hires` und Lauf-Dateien `verdichter_catch/runs` zusammen. WW-Ist: bei Anforderung / Minimum / bei Start.

| Datum | letzte P_el ≥ 20 | Stopp | WW_Status 1 | Start | Stopp -> Anf. [min] | Wartezeit [min] | Sperrdauer-Fenster [min] | WW-Ist [°C] | Soll | 1539 in der Wartezeit |
|---|---|---|---|---|---|---|---|---|---|---|
| 03.10. | 13:07:51 | 13:08:51 | 13:10:02 | 13:24:02 | 1,2 | 14,0 | 15,00-15,67 | 52,1 / 50,8 / 51,0 | 57 | 16, 16 |
| 07.10. | 17:33:51 | 17:34:52 | 17:43:41 | 17:50:02 | 8,8 | 6,3 | 15,00-15,47 | 50,8 / 50,0 / 50,3 | 57 | 16 |
| 30.10. | 09:30:52 | 09:31:52 | 09:40:02 | 09:47:01 | 8,2 | 7,0 | 15,20-16,12 | 45,1 / 44,3 / 44,4 | 50 | 16 |
| 30.10. | 14:56:51 | 14:57:52 | 14:58:01 | 15:12:52 | 0,1 | 14,8 | 14,97-15,90 | 47,1 / 45,9 / 45,9 | 52 | 16, 16, 16 |
| 31.10. | 11:23:52 | 11:24:52 | 11:28:51 | 11:40:13 | 4,0 | 11,4 | 15,18-15,78 | 45,2 / 44,7 / 44,9 | 57 | 16, 16 |
| 02.11. | 08:47:52 | 08:48:52 | 08:55:42 | 09:03:42 | 6,8 | 8,0 | 14,70-15,63 | 45,2 / 44,7 / 44,8 | 50 | 16 |

- **Korrektur zu `WP_Verhaltenskarte.md` Z. 917:** `WW_Status` = 1 kam schon 08:55:42, 08:56:01 ist der erste Ladesoll-Wert (`AnlageSoll_WW`). Rest der Zeile bestätigt. [sicher]
- **Eine feste Sperrdauer passt zu allen 6:** Die Fenster überschneiden sich bei 15,20-15,47 min, also 900 s plus ca. 12-28 s bis P_el sichtbar. [wahrscheinlich, Rasterbreite]
- **Live-Beleg für Status 16 (Restprüfung V99):** `1539` = 16 in 10 Volllogger-Proben, alle in den Wartezeiten mit `1504` = 1. Zwei weitere Proben mit `1504` = 1 zeigen noch 0 (03.10. 13:10:01, 30.10. 09:40:01), beide 1 s vor der ersten `WW_Status`-Zeile. Die restlichen 7 Proben mit 16 liegen alle in Pausen nach Abtauung. In reinen Heizpausen ohne Anforderung steht 0, nie 16. [sicher für Zählung]
- **Zusatz 07.09.-30.09. (37 Ladungen, a/b/c = 3/28/6):** 12.09. Stopp 15:33:11, Start 15:48:22 (15,02-15,35 min); 20.09. Stopp 12:17:52, Start 12:33:12 (15,17-16,33 min). Beide nicht widerlegt; der dritte Fall (28.09.) ist die Abtau-Ausnahme unten. [sicher]

## Klasse b und c

| Klasse | n | Bedingung | Ergebnis | Belastbarkeit |
|---|---|---|---|---|
| b | 89 | Anforderung ≥ 15 min nach Stopp, gemessen ab 18,3 min | Start 0,65 / 0,85 / 1,17 min nach `WW_Status` = 1 (min / Median / max); keine Wartezeit > 1,5 min; WW-Ist-Änderung bis Start -0,3 / 0,0 / +0,6 K | [sicher] |
| c, klar | 15 | Verdichter lief ≥ 5 min vor Anforderung | Kein Stopp bis Ladungsende, Verdichter stoppt 30-60 s nach WW-Ende (02.11. 06:24 durch Abtauung) | [sicher] |
| c, unklar | 3 | Lauf erst 0,3 / 1,0 / 1,2 min vor Anforderung (24.10. 05:27:51, 27.10. 06:54:52, 15.10. 18:19:52) | Kein Widerspruch, aber Reihenfolge im 60-s-Raster und bei Registeralter nicht auflösbar | [wahrscheinlich Heizstart, Vermutung WW-Start nicht auszuschließen] |

Nächste b-Fälle an der Grenze: 15.10. 05:36:11 (18,3 min), 24.10. 14:24:31 (18,6), 06.10. 06:09:52 (19,0), 11.10. 11:34:22 (20,5); Start jeweils nach 0,67-1,02 min. [sicher]

## Getrennt: was gehalten hat, was nicht

**Nicht widerlegt (Sperre gilt):** 6 von 6 ab 01.10., dazu 2 von 2 im September. Alle Fälle: Stopp ohne WW-Ladung und ohne Abtauung davor (ab 01.10. Heizlauf; im September Heizen/Kühlen nicht unterschieden).

**Widerlegt als Regel „immer 15 min“:**

| Zeit | Fall | Pause | Einordnung |
|---|---|---|---|
| 28.09. 04:44:52 -> 04:50:22 | WW-Anforderung direkt nach Abtauung | 5,33-5,67 min | Abtau-Ausnahme, einziger WW-Fall [sicher] |
| 7 Pausen nach Abtauung seit 01.10. (13.10. 07:15 und 08:42, 26.10. 05:09, 27.10. 06:47, 02.11. 02:26, 04:51, 06:30) | Heizen nach Abtauung | 4,8-6,5 min | Passt ungefähr zu 300 s (V99/CL006) [wahrscheinlich]. Die in der Firmware genannten 30 s nicht beobachtet [sicher] |
| 18.10. 11:11:32 -> 11:13:52 | **Mitten in einer WW-Ladung**: Fehler 222/Regler-Reset, dann Neustart | 2,0-2,3 min | Reset hebt die Sperre auf; 1 Fall [Zeit sicher, Mechanismus wahrscheinlich] |

**Keine echte Pause, aus der Wertung genommen:** 7 Lücken direkt vor dem Status-8-Lauf einer Abtauung (0-3 min) und 29.10. 10:41:52 -> 10:46:52: Standbild, der Betreiber hatte die WP ab 08:55 abgeschaltet (`ANALYSE_F73_Lauf_ohne_Soll_20261102.md`). [sicher]

**Unklar:** die 3 c-Fälle oben und der unbeobachtete Bereich unter „Offen“.

## Was kostet die Sperre

- **Warte-Minuten:** 6,3-14,8 min je Fall (Median 9,7), Summe 61,5 min; abzüglich 6 x 0,85 min normalem Anlauf ca. 56 min in 33 Tagen. [sicher]
- **WW-Ist:** Abfall bis Start 1,1 / 0,5 / 0,7 / 1,2 / 0,3 / 0,4 K. Tiefster Wert 44,3 °C (30.10. 09:46:52), kein Komfortthema. [sicher] Das sind 1,6-6,0 K/h gegen 0,55-0,83 K/h in normalen Pausen (F79). [sicher]
- **Heizkreis:** `Pumpe_HK1` steht 84-95 % der Wartezeit, also 6-15 min keine Wärme in die FBH. Für die träge FBH bedeutungslos. [sicher für Zeit, Bewertung wahrscheinlich]
- **Energie:** Ladungen ab Ist 45,1 ±0,25, Soll 50, außen < 12 °C: a n = 2 Median 1,72 kWh_el, b n = 19 Median 1,74 kWh_el. Kein Unterschied sichtbar, Außentemperatur verschieden (5,3 / 10,1 °C). [wahrscheinlich, sehr wenige Fälle]
- **PV:** 3 von 6 Fällen sind Soll 57 (03.10., 07.10., 31.10.), zusammen 31,7 min PV-Fenster ohne Ladung. [sicher für Minuten; Ertragsverlust nicht gerechnet]

## Was bringt uns das

**Zwilling-Regel WW-Start** (Stoppzeit `t_stopp`, Anforderung `t_ws`):

- Verdichter läuft: Übergang ohne Stopp, Wartezeit 0.
- Verdichter steht, normaler Stopp: Start = später von `t_ws + 0,85 min` (0,65-1,17) und `t_stopp + 15,3 min` (15,2-15,5).
- Verdichter steht, Abtauung davor: Start ca. 5-6 min nach Abtauende.
- Nach Regler-Reset: keine Sperre (1 Fall).

Für Loxone: Eine PV-Anhebung auf 57 kurz nach einem Heizstopp kann die Ladung nicht beschleunigen. Eine Soll-Anhebung, solange der Verdichter noch läuft, geht dagegen ohne Wartezeit in die Ladung über (Klasse c). Eingriff lohnt nicht: 56 min in 33 Tagen, WP011 sitzt im Kälteregler und bleibt unberührt.

## Auflösung und Unsicherheit

| Quelle | Raster | Folge |
|---|---|---|
| `ww_hires`, `WW_Status` = 0 | 60 s (einzelne Abschnitte 10 s) | Stopp bis 60 s unscharf |
| `ww_hires`, `WW_Status` = 1 | 10 s | Start und Anforderung ±10 s |
| `verdichter_catch/runs` | 46 s (67 s bei Lesefehlern) | Stoppfenster auf 26-46 s eingegrenzt; Lauf-Start zum Teil bis 27 s später als P_el (30.10. 09:47:28 gegen 09:47:01), daher nur Stoppseite genutzt |

- WEZ-Register sind bis 60 s alt. Alle Zeiten sind daher „sichtbar ab“, nicht Schaltzeitpunkte. Klassengrenze nicht betroffen: Die a-Fälle reichen bis 8,8 min, die b-Fälle beginnen bei 18,3 min. [sicher]
- `WP_VL` und `WP_RL` in `ww_hires` stehen vom 12.09. bis 17.10. 12:24 auf 307/294 (Standbild). Temperaturaussagen zum WP-Kreis daher nur aus 30.10.-02.11. [sicher]

## Offen

- **Bereich 8,8-18,3 min nicht beobachtet.** Vorhersage, vor dem Ereignis notiert: Anforderung 9-15 min nach Stopp -> Start bei `t_stopp` + 15,2-15,5 oder `t_ws` + ≤ 1,2 min, je nachdem was später liegt. **Widerlegt** bei Start < `t_stopp` + 14,5 ohne Abtauung/Reset oder bei Wartezeit > 2 min nach Ablauf der Sperre. Noch nicht in die Verhaltenskarte übernommen.
- WW-Ladung direkt nach WW-Ladung-Stopp: kein Fall (`prevWW` immer 0). Geltung dort nur aus der Firmware (V99).
- Abtau-Ausnahme bei WW: nur 28.09. Die 30-s-Variante der Firmware nie gesehen.
- Warum `WW_Status` zweimal innerhalb 1 min nach einem Stopp kam (30.10. 14:58:01, 12.09. 15:33:41), nicht geklärt. Bei 8 Fällen Zufall möglich.
- Sperre vor Heizstarts mit anliegender Anforderung nicht Teil von F83; 0 echte Gegenbeispiele in den 281 Pausen.

## Vorgehen und Dateien

Ladung = zusammenhängende Zeilen `WW_Status` = 1 (Lücke ≤ 150 s, wie F79). Verdichter an = P_el ≥ 20 (Einheit 10 W). Skripte, Rohdaten und Ausgaben (`f83_f.out`, `f83_g.out`, `f83_h.out`, `f83_i.out`) in `[lokaler Pfad]`: `f83_a.py` bis `f83_i.py`, `f83_ww_hires.csv`, `f83_full\`. Vorlauf: `[lokaler Pfad]`, `ANALYSE_Taktschutz_V99_V101_20261022.md`, `WP_Verhaltenskarte.md` (V99, V107, Z. 917).