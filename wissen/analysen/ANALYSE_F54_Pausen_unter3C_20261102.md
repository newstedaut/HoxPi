# F54 Vertiefung: Heizpausen unter 3 °C (02.11.2026, nur lesend)

Nichts an Anlage, Pi oder Loxone geändert. Zeiten Ortszeit. Vorarbeit und Methode: `[lokaler Pfad]`.

## Kurz
- **Am Hoval-Fühler 1477 gibt es genau 1 reine Pause unter 3 °C** (02.11. 04:00, Mittel 2,99 °C). Daraus kein Median [sicher].
- **„Unter 3 °C“ hängt am Fühler:** 1477 lag im Fenster nie unter 2,9 °C, die Luft X26 `0106` zur selben Zeit bei 0,2–1,8 °C. Mit `0106` < 3 °C gibt es 8 reine Pausen [sicher], Median 57 min, 40–94 min [sicher für 01./02.11.]. Echter Frost an 1477 fehlt weiter.
- **Faustregel trägt, ist aber im Schnitt 5 min zu kurz** [wahrscheinlich]. Exakt passt 4,5 K statt 4 K und 16 statt 15 min [sicher als Messung, aber zur Hälfte zirkulär, siehe Befund 3].
- **Die Pause wird im gemessenen Bereich nicht kürzer, weil es kälter wird** [wahrscheinlich].

## Datenquelle
| Quelle | Pfad | Inhalt | Raster |
|---|---|---|---|
| Volllogger Kopie | `[lokaler Pfad]` … `2026-10-31.csv` | 24.–31.10. | 5 min |
| Volllogger Pi, heute gelesen | `/home/<user>/hoxpi_fulllog/2026-11-01.csv`, `/home/<user>/hoxpi_fulllog/2026-11-02.csv` (Kopien `[lokaler Pfad]`, `f54_pi_2026-11-02.csv`) | bis 02.11. 09:55:02 | 5 min |
| Minutenlogger Pi | `/home/<user>/hoxpi_fulllog/ww_hires.csv` (Kopie `...\f54_hires.csv`) | Spalten `P_el`, `Ruecklauf`, `Aussen`, 31.10. 22:00 – 02.11. 09:57 | 1 min |
| Luft X26 `0106` | `...\f80_p1101_a.csv`, `f80_p1101_frueh.csv`, `f80_p1101.csv`, `f80_p1102.csv`, neu dekodiert `...\f54_p1102_heute.csv` | ab 01.11. 01:47, für 31.10. nicht geholt | ~8 min |
| Bridge-Journal | `journalctl -u hoval-bridge`, Auszug `...\f54_set1490.txt` | `SET reg 1490`, **erst ab 01.11. 14:22** vorhanden | s |
| Laufgrenzen Abtauung | `...\f80_runs.txt`, `...\f80_ausw_out.txt` (X4 Run) | 02.11. | s |

Skripte: `[lokaler Pfad]`, `f54_ausw2.py`. Ergebnisse: `...\f54_ergebnis.txt`, `f54_ergebnis2.txt`.

**Gegenprobe Methode:** Mein Skript liefert für 24.10.–01.11. wieder n = 34 reine Pausen, Median 52 min, rThr-Median 8,7 K/h, also dieselben Zahlen wie die Analyse vom 01.11. Mit den 2 neuen reinen Pausen (n = 36) bleibt r(Dauer, 1/rThr) = 0,86 [sicher].

**Begriffe:** Dauer = Minutenlogger, P_el fällt auf 0 bis P_el > 0,5 kW. r = (RL beim Stopp − erster RL unter 1520 − 1,0) / Zeit, aus dem Minutenlogger. rThr = Rate nach F54 aus dem 5-min-Raster (RL erste Pausenzeile bis erste Zeile RL ≤ 1520 − 1,0). AT = Mittel 1477 über die Pause. Luft = Mittel `0106`. „rein“ = keine WW-Ladung, keine Abtauung, 1490 nie 0 und nie 24,0 im Raster.

## Tabelle 1: Alle Pausen mit 1477 < 3 °C und 3–4,5 °C (31.10. 22:01 – 02.11. 09:55)
Quelle: Volllogger und Minutenlogger, `...\f54_ergebnis.txt`.

| Band 1477 | Beginn | Ende | Dauer min | AT 1477 °C | Luft 0106 °C | r K/h | rThr K/h | RL / 1520 Beginn | RL / 1520 Ende | Ursache Pausenbeginn | rein |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **< 3** | 02.11. 03:58:51 | 04:38:51 | **40** | 2,99 | 0,37 | 11,2 | 10,5 | 37,5 / 34,5 | 31,5 / 34,5 | Hoval-RL-Schwelle (+3,0 K) | **ja** |
| < 3 | 02.11. 04:52:51 | 04:57:51 | 5 | 2,90 | 0,7–0,6 ¹ | – | – | 31,0 / 34,5 | 28,5 / 34,5 | Abtauung 04:47–04:52 | nein |
| 3–4,5 | 01.11. 06:36:41 | 06:58:52 | 22 | 3,50 | 0,40 | – | – | 53,0 / 56,0 | 32,0 / 34,5 | WW-Ladeende | nein |
| 3–4,5 | **01.11. 07:29:52** | 08:16:52 | **47** | 3,40 | 0,30 | 8,7 | 9,6 | 35,5 / 32,5 | 30,5 / 32,5 | Hoval-RL-Schwelle (+3,0 K) | **ja** |
| 3–4,5 | **01.11. 08:46:52** | 10:20:52 | **94** | 3,76 | 0,68 | 3,5 | 3,5 | 35,0 / 32,0 | 30,5 / 32,0 | Hoval-RL-Schwelle (+3,0 K) | **ja** |
| 3–4,5 | 02.11. 02:27:51 | 02:33:51 | 6 | 3,50 | 1,5 | – | – | 31,5 / 34,5 | 28,5 / 34,5 | Abtauung 02:22–02:27 | nein |
| 3–4,5 | 02.11. 06:24:31 | 06:36:51 | 12 | 3,17 | 0,5–0,8 ² | – | – | 48,5 / 54,0 | 31,0 / 34,5 | Abtauung bricht WW-Ladung ab, darin Abtauung 06:25–06:31 | nein |
| 3–4,5 | **02.11. 07:15:52** | 08:09:51 | **54** | 3,04 | 0,30 | 7,1 | 7,0 | 35,5 / 32,5 | 30,5 / 32,5 | Hoval-RL-Schwelle (+3,0 K), 1490 kurz vorher um 1,7 K gesenkt | **ja** |


Nicht gezählt: Pause seit 09:37 ist offen (nach WW-Ladung, bis 09:57 kein Start). Die Pause 08:48–09:03 endete in einer WW-Ladung, dieser Block hat noch keinen Folge-Heizlauf [sicher].

## Tabelle 2: Faustregel je reine Pause mit Luft `0106` < 3 °C
Quelle: `...\f54_ergebnis2.txt`. Abw. = gemessen − Vorhersage.

| Beginn | AT 1477 | Luft | Dauer min | rThr | Faustregel (3+1)/rThr + 15 | Abw. min (5-min-Raster) | r | 4,5/r + 16 | Abw. min | Start nach RL < 1520−1 | Abw. mit Frührate ³ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 01.11. 01:26 | 5,19 | 2,47 | 66 | 4,5 | 68 | −3 | 5,5 | 65 | +1 | 17 | +21 |
| 01.11. 04:04 | 4,54 | 1,74 | 65 | 6,0 | 55 | +10 | 5,6 | 64 | +1 | 17 | +20 |
| 01.11. 07:29 | 3,40 | 0,30 | 47 | 9,6 | 40 | +10 | 8,7 | 47 | 0 | 16 | +8 |
| 01.11. 08:46 | 3,76 | 0,68 | 94 | 3,5 | 84 | +11 | 3,5 | 94 | 0 | 16 | +39 |
| 01.11. 10:55 | 4,95 | 1,61 | 58 | 7,0 | 49 | +6 | 6,7 | 56 | +2 | 18 | +6 |
| 01.11. 16:08 | 5,26 | 2,53 | 56 | 6,0 | 55 | 0 | 6,0 | 61 | −5 ⁴ | 16 | +1 |
| **02.11. 03:58** | **2,99** | 0,37 | 40 | 10,5 | 38 | +2 | 11,2 | 40 | 0 | 16 | +5 |
| 02.11. 07:15 | 3,04 | 0,30 | 54 | 7,0 | 49 | +1 | 7,1 | 54 | 0 | 16 | +9 |

³ Faustregel mit der Rate der ersten 15 min nach Stopp, also vorab bekannt. Mittlerer Fehler 13,6 min. ⁴ 1520 stieg in der Pause von 31,5 auf 32,0.

## Befund
1. **Zu wenig reine Pausen an 1477:** n = 1 unter 3 °C (40 min, 10,5 K/h). 1477 lag nur in 7 Rasterzeilen unter 3,0 °C (02.11. 04:30–04:55 und 07:55, je Rohwert 29) [sicher]. Das reicht für keinen Median, auch nicht als Tendenz.
2. **1477 und `0106` weichen stark ab:** 1477 − `0106` Median 2,8 K, Bereich 1,1–3,8 K (n = 245, 01.11. 01:47 – 02.11. 09:54) [sicher]. Die Angabe „erstmals Luft unter 3 °C in der Nacht 01./02.11.“ gilt nur eingeschränkt: `0106` lag schon am 01.11. 07:30 bei 0,3 °C, 1477 dabei bei 3,4 °C [sicher]. Welcher Fühler die wahre Außenluft zeigt, ist offen.
3. **Faustregel (3+1 K)/Rate + 15 min:** Abweichung 02.11. 04:00 **+2 min**. Über die 8 Pausen mit Luft < 3 °C −3 bis +11 min, im Mittel +4,6, mittlerer Fehler 5,4 min [sicher]. Sie trägt, liegt aber systematisch zu kurz [wahrscheinlich].
   - Grund im Minutenlogger: Stopp bei RL = 1520 + 3,0 K in 11 von 11 reinen Pausen seit 31.10. Unterschritten wird die Schwelle bei RL = 1520 − 1,5 (0,5-K-Raster). Das sind 4,5 K statt 4 K, in 10 von 11 Fällen genau so [sicher]. Der Start folgt 16–18 min danach, nicht 15 (7 × 16, 3 × 17, 1 × 18 min) [sicher].
   - Mit 4,5/r + 16 ist der mittlere Fehler 0,9 min (n = 11, Maximum 5 min) [sicher]. **Das ist kein Beweis für Vorhersagekraft:** r wird aus derselben Pause gerechnet, die Formel prüft nur die beiden Konstanten [sicher].
4. **Vorab ist die Pause schlecht vorhersagbar:** Die Rate der ersten 15 min liegt über der Rate bis zur Schwelle (Median 8,0 gegen 6,4 K/h), die Abkühlung flacht ab. Faustregel damit: mittlerer Fehler 13,6 min, bis +39 min [sicher, n = 8].
5. **Kürzer durch höhere Rate?** Im gemessenen Bereich nein [wahrscheinlich]. r(rThr, 1477) = −0,19, n = 36 ab 24.10. r(r, `0106`) = +0,03, n = 9 ab 01.11. [sicher]. Median rThr je 1477-Band: 3–4,5 °C 9,3 K/h (n = 6), 4,5–6 °C 7,1 (n = 16), 6–9 °C 10,5 (n = 10) [sicher]. Bei gleicher Luft 0,3–0,4 °C streut r mit 7,1 / 8,7 / 11,2 K/h. Die kurze 40-min-Pause von 04:00 ist also kein Frosteffekt-Beleg. Warum r so streut, ist offen (tagsüber Sonne oder geschlossene Stellantriebe = Vermutung).
6. **Abtaupausen gehorchen der Faustregel nicht:** Stillstand nach Abtauung 5,4 / 5,4 / 5,3 min (X4 Run 02:27:28→02:32:49, 04:51:58→04:57:20; Status-8-Ende 06:31:11→Run 06:36:28), danach Status 16 [sicher, n = 3]. Am 02.11. fiel der RL erst um 06:31:51 unter 33,5 (RL 33,0, 1520 = 34,5), Run kam 06:36:28, also nach rund 5 min. Die 15-min-Verzögerung griff hier nicht [sicher für diesen Fall; ob das immer gilt: Vermutung].

## Vorhersage für den Frost (Zeile für `[lokaler Pfad]`, notiert 02.11.2026, Datenstand 09:57)
Bei reinen Heizpausen mit 1477 < 3 °C auch unter 0 °C (1501 = 23, 1520 in der Pause konstant, keine WW-Ladung, keine Abtauung): Dauer Stopp→Start [min] = 4,5 K / r × 60 + 16, r = (RL beim Stopp − erster RL unter 1520 − 1,0) / Zeit im `ww_hires`, Toleranz ±5 min, und nachts (22–06 Uhr) r = 5–12 K/h, also Pause 38–70 min; widerlegt, wenn von den nächsten 5 solchen Pausen mindestens 2 außerhalb ±5 min liegen oder der Nacht-Median von r über 12 K/h steigt. Abtaupausen: 5–6 min, Faustregel gilt dort nicht.

## Stichprobe zum Gegenprüfen
Volllogger `/home/<user>/hoxpi_fulllog/2026-11-02.csv`, Rohwerte ×10 (25611 ×100):

| Zeit | 1477 | 1490 | 1501 | 1520 | 1535 | 1539 | 25611 | Bedeutung |
|---|---|---|---|---|---|---|---|---|
| 03:55:02 | 30 | 327 | 23 | 345 | 370 | 1 | 192 | letzte Laufzeile |
| 04:00:02 | 30 | 327 | 23 | 345 | 370 | 0 | 0 | erste Pausenzeile |
| 04:20:01 | 30 | 327 | 23 | 345 | 335 | 0 | 0 | |
| 04:25:01 | 30 | 327 | 23 | 345 | 330 | 0 | 0 | RL 33,0 < 34,5 − 1,0 |
| 04:30:01 | 29 | 327 | 23 | 345 | 325 | 0 | 0 | |
| 04:35:02 | 29 | 327 | 23 | 345 | 320 | 0 | 0 | |
| 04:40:02 | 29 | 327 | 23 | 345 | 320 | 1 | 212 | Lauf |

Minutenlogger `ww_hires.csv`: 03:57:52 P_el 193, RL 375; 03:58:51 P_el 0, RL 375 (Stopp, 37,5 = 34,5 + 3,0); 04:21:52 RL 335; 04:22:52 RL 330 (erstmals unter 33,5); 04:37:52 P_el 0; 04:38:51 P_el 205 (Start).

Rechnung: 24 min für 4,5 K ergibt r = 11,2 K/h. 4,5/11,2 × 60 + 16 = 40 min, gemessen 40,0 min. Alte Faustregel 4/10,5 × 60 + 15 = 38 min, Abweichung +2 min im 5-min-Raster [sicher].

## Offen
- Echter Frost an 1477 (unter 2,9 °C, erst recht unter 0 °C) fehlt, die Vorhersage ist dort eine Fortschreibung [sicher].
- Welcher Fühler die Außenluft richtig zeigt, 1477 oder `0106`, und woher die 2,8 K kommen. Für künftige Bänder immer beide angeben [sicher, dass offen].
- `0106` für 24.–31.10. nicht ausgewertet: r gegen Luft stützt sich auf n = 9 von 01./02.11.
- Warum r bei gleicher Luft um den Faktor 1,6 streut (Stellantriebe oder `demandHeat` der Raumregler sind nicht je Pause geloggt).
- Gilt die kurze Wiedereinschaltzeit nach Abtauung auch bei WW-Abbruch immer? Bisher 1 Fall, der Zwilling sollte das nicht fest annehmen.

## Was bringt uns das
Der Zwilling kann die Pausen unter 3 °C mit derselben Rechnung abbilden wie bei mildem Wetter, muss aber die Abkühlrate aus der Pause selbst nehmen, weil die Außentemperatur sie nicht vorhersagt.