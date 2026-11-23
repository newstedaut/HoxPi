# F54 Rest: Pausenl?nge je Au?entemperatur (OR 01.11.2026, nur lesend)

## Frage
Wie lang sind die Pausen zwischen Heizl?ufen je AT-Band (<3, 3?6, 6?9, >9 ?C)? Erkl?rt die Abk?hlrate des R?cklaufs 1535 (K/h) die Pausenl?nge? Wie viel der Pause ist "Abk?hlen bis Schwelle" (RL ? 1520 ? HV012 1,0 K), wie viel HKA59-Verz?gerung (15 min), wie viel "Loxone-Anforderung fehlt (1490 = 0)" bzw. WW-Ladung/Abtauung dazwischen?

## Datenquelle
- Volllogger am Pi (nur gelesen, per `[lokaler Pfad]`): `/home/<user>/hoxpi_fulllog/2026-10-24.csv.gz` ? `2026-10-30.csv.gz`, `/home/<user>/hoxpi_fulllog/2026-10-31.csv`, `/home/<user>/hoxpi_fulllog/2026-11-01.csv` (Stand 01.11. 23:55), 2604 Zeilen, 5-min-Raster, keine L?cken (25.10. Zeitumstellung: 300 Zeilen, als 5-min-Schritte gez?hlt).
- Spalten: 1477 AT, 1490 HK1-Soll Loxone, 1501, 1520 Soll K?lteregler, 1525 VL, 1535 RL, 1539 Betriebsart, 25611 P_el (Rohwert/100 kW).
- Vorarbeiten: `[lokaler Pfad]`, `[lokaler Pfad]`, `[lokaler Pfad]`, Argon MD-14 `[lokaler Pfad]` (nur Kopf gelesen; Pausenliste neu gerechnet, weil MD-14 nur bis 01.11. 15:50 reicht und keine Abk?hlrate/Schwellenzeit enth?lt).
- Zwischenablage der Rohzeilen (nur Cache, keine Projektdatei): `[lokaler Pfad]`, `[lokaler Pfad]`.

## Methode
- Lauf = zusammenh?ngende Zeilen mit 25611 > 0,5 kW; Heizlauf = Mehrheit 1539 = 1. 24.10.?01.11. 24:00: 105 L?ufe, 72 Heizl?ufe, 31 WW, 1 Abtauung, 1 Typ 17 ? 71 Pausen zwischen zwei Heizl?ufen [sicher].
- Pause = erste Zeile ohne Lauf bis erste Zeile des n?chsten Heizlaufs (Raster ?5 min). Klassen: **WW/Abt** = Lauf oder 1539 = 4/8 dazwischen; sonst **Lox0** = mind. eine Zeile 1490 = 0; sonst **rein**.
- AT = Mittel 1477 ?ber die Pause. Abk?hlrate rThr = (RL erste Pausenzeile ? RL an der Schwellenzeile) / Zeit; Schwellenzeile = erste Pausenzeile mit 1535 ? 1520 ? 1,0 K. t_abk = Pausenbeginn ? Schwellenzeile, Rest = Schwellenzeile ? n?chster Start. rGes = RL-Abfall ?ber die ganze Pause.
- Ausgeschlossen 1 Pause (01.11. 06:40?07:00, RL 51,5 ?C in der ersten Pausenzeile = Nachlauf einer WW-Ladung, falsch als "rein" erkannt).

## Tabelle Pausen je AT-Band (24.10.?01.11.2026)
| Klasse | AT-Band | n | Median min | Min/Max min | rThr K/h (Median) | rGes K/h (Mittel) | t_abk Median | Rest Median | davon 1490 = 0 Median |
|---|---|---|---|---|---|---|---|---|---|
| rein | <3 ?C | 0 | ? | ? | ? | ? | ? | ? | ? |
| rein | 3?6 | 21 | 55 | 30/95 | 8,0 | 5,8 | 30 | 25 | 0 |
| rein | 6?9 | 10 | 43 | 30/70 | 10,5 | 7,4 | 20 | 20 | 0 |
| rein | >9 | 3 | 95 | 75/100 | 3,7 | 3,4 | 65 | 25 | 0 |
| **rein** | **alle (? 6,0 ?C)** | **34** | **52** | 30/100 | **8,7** | 6,1 | **25** | **23** | 0 |
| Lox0 | 3?6 | 7 | 160 | 50/320 | 4,2 | 3,6 | 45 | 20 | 125 |
| Lox0 | 6?9 / >9 | 2 / 2 | 68 / 65 | 50/80 | 7,5 / 6,4 | 5,1 / 5,2 | 38 / 40 | 30 / 25 | 18 / 22 |
| **Lox0** | **alle** | **11** | **70** | 50/320 | 6,0 | 4,2 | 45 | 20 | 30 |
| WW/Abt | 3?6 / 6?9 / >9 | 10 / 11 / 4 | 155 / 180 / 150 | 65/940 | 5,1 / 7,0 / 4,6 | 2,0 | 37 | 95 | 30 |

Pausensummen: rein 1885 min (davon 1075 min Abk?hlen bis Schwelle), Lox0 1275 min (davon 915 min mit 1490 = 0 = 72 %), WW/Abt 6725 min (davon 4125 min mit 1490 = 0) [sicher, 5-min-Raster].
AT lag im ganzen Zeitraum nur bei 3,1?11,3 ?C ? Band <3 ?C ist leer [sicher].

## Bewertung
1. **Reine Pausen = Abk?hlen bis Schwelle + konstanter Rest** [sicher]: Rest nach Erreichen von RL ? 1520 ? 1,0 ist 15?35 min, Median 20?25 min (einmal 65 min) = 15 min HKA59 + 5?10 min Rasterversatz/Anlauf. Die variable Gr??e ist allein das Abk?hlen (20?65 min).
2. **Pausenl?nge h?ngt an der RL-Abk?hlrate, nicht an der AT** [sicher f?r 3?11 ?C]: r(Dauer, 1/rThr) = 0,86; r(Dauer, AT) = 0,16; r(rThr, AT) = ?0,21. Lange reine Pausen (95?100 min) liegen tags?ber bei kleiner Rate (3?4 K/h, 26.10. 13:50, 30.10. 13:00, 01.11. 08:50) ? Ursache Sonne/Fremdw?rme bzw. Raumregler mit geschlossenen Stellantrieben [Vermutung, Durchfluss/Ventilstellung nicht geloggt]. Tags 9?18 Uhr: Median 55 min bei 6,5 K/h, sonst 48 min bei 9,8 K/h [sicher].
3. **Faustregel Pausenl?nge ? (3,0 + 1,0 K)/Abk?hlrate + 15 min (+5 min Raster)** [wahrscheinlich, tr?gt]: mit der Rate der jeweiligen Pause Median-Fehler 0 min, mittlerer Fehler 6,8 min (n = 34). Mit 3,5 K statt 4,0 K (gemessener Median-Abstand RL erste Pausenzeile ? Schwelle, weil der RL in den ersten 5 min schon ~0,5 K f?llt) Median ?4 min, MAE 7,7 min. **Einschr?nkung:** Die Rate stammt aus derselben Pause (teils zirkul?r); mit einer Band-Median-Rate vorhergesagt ist der mittlere Fehler 13 min ? die AT allein liefert keine brauchbare Rate [sicher].
4. **Lox0-Pausen**: Median 70 min (bis 320 min); 72 % ihrer Dauer fehlt die Loxone-Anforderung (1490 = 0); die Abk?hlrate ist dort kleiner (4?6 K/h), weil der HK ohne Anforderung weniger abnimmt [wahrscheinlich].
5. **WW/Abt-Pausen**: Median 155 min, der Rest nach Erreichen der Schwelle (95 min) ist vor allem WW-Ladung + 1490 = 0 (N?chte) ? nicht Hoval-Hysterese [sicher].
6. Zwilling: Pause_rein ? 4 K / rRL + 20 min mit rRL ? 8?10 K/h nachts, 3?7 K/h tags?ber; AT nicht als Pr?diktor verwenden [wahrscheinlich].

### Stichprobe (Volllogger `/home/<user>/hoxpi_fulllog/2026-10-28.csv.gz`, Rohwerte ?10)
| Zeit | 1477 | 1490 | 1520 | 1525 | 1535 | 1539 | 25611 |
|---|---|---|---|---|---|---|---|
| 06:05:01 (letzte Laufzeile) | 65 | 317 | 345 | 415 | 375 | 1 | 193 |
| 06:10:01 (Pausenbeginn) | 66 | 317 | 345 | 355 | 360 | 0 | 0 |
| 06:25:01 (Schwelle RL ? 33,5) | 66 | 317 | 345 | 330 | 330 | 0 | 0 |
| 06:35:01 (Pausenende) | 66 | 317 | 345 | 325 | 325 | 0 | 0 |
| 06:40:01 (Start) | 66 | 317 | 345 | 360 | 325 | 1 | 222 |
Stopp bei RL 37,5 = 1520 + 3,0 K; Schwelle 06:25 (RL 33,0 ? 34,5 ? 1,0); Start 06:40 = 15 min sp?ter (HKA59). Pause 30 min = 15 min Abk?hlen + 15 min Verz?gerung; rThr 12 K/h; Faustregel 4/12?60 + 15 = 35 min [sicher].

## Offen
- Band <3 ?C: noch keine Daten (Wiederholung bei Frost) [sicher].
- Ursache der niedrigen Tages-Abk?hlraten: Ventilstellungen/demandHeat der Loxone-Raumregler je Pause mitloggen [Vermutung zur Ursache].
- F?hlerort des K?lteregler-RL (eigener F?hler vs. 1535) weiter unbelegt; 5-min-Raster begrenzt die Genauigkeit auf ?5 min.