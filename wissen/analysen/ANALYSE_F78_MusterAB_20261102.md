# ANALYSE F78 - Muster a/b der dunklen SG-Flanken (02.11.2026)
Claude, Subagent, nur lesend. An Anlage, Miniserver, Projektdatei und Pi nichts geändert. Ergänzt `[lokaler Pfad]` und `[lokaler Pfad]`.
Zeiten: Z = UTC. Lokal im Oktober bis 25.10. = Z + 2, danach Z + 1. „Dunkel" = PV der Stunde unter 0,5 kWh.

## Ergebnis
1. **Das Vorzeichen von Spwr ist falsch herum.** Doku: negativ = Laden. Messung bei uns: negativ = Entladung. [sicher]
2. **Muster b (abends): „Entladung zählt als Überschuss" erklärt es im Kern.** Dunkle Abendflanken: 0 in den 18 Tagen vor dem Fix vom 18.10., 6 in den 5 Tagen danach. Der Fix gibt die Entladung erst seitdem an den Energiemanager (EM). Beste Einzelflanke: 19.10. 17:05, Akku +6,04 kW, SOC 97. Der Punkt liegt 5 min vor der Flanke. Von den 5 anderen sind 4 mit dem Akku-Takt vereinbar, aber nicht einzeln gemessen, 22.10. 17:00 passt eher nicht. [wahrscheinlich]
3. **Muster a (morgens, 14. und 16.10.): nicht erklärt.** Entladung lag an, ist aber nicht der Unterschied. Gleiche oder stärkere Lage ohne Flanke: 19.10. 06:00 (Akku +5,68 kW, WP 4,73 kW), 30.10. 02:30 (+4,36 kW). [sicher: Messung; Ursache offen]
4. **Entladung allein reicht nie als Regel.** Von 32 Stunden mit mindestens 1,5 kWh Entladung hatten nur 3 eine Flanke. Dazu kommt die SOC-Schwelle: Unter MinSoc 95 % gibt es fast nie eine Flanke, auch bei 3,4 kW Entladung. [sicher: Zählung; Deutung wahrscheinlich]
5. **Korrektur F76: „Akku 0" bei den Abendflanken ist ein Abtastfehler.** Die Meter-Statistik hat nur 30-min-Punkte. 23.10. 17 Z: Punkte 0 und 0, aber 0,90 kWh entladen, SOC 93 → 87. Der Akku läuft dort in Pulsen. [sicher]

## Rechnung des EM und Verdrahtung
Baustein [Energiemanager](https://www.loxone.com/dede/kb/energiemanager-2/), `[lokaler Pfad]`:
| Eingang | Quelle | Zeile |
|---|---|---|
| EM `EnergyManager2` | Reihenfolge: WP, Wallbox, Heizstab, Heizkörper (live `loads`: prio 0, 1, 2, 3) | 8078 |
| Gpwr | Victron Grid (Div) | 8079, 11357 |
| Spwr (Eingang Z. 8085) | [Formel](https://www.loxone.com/enen/kb/formula/) (DE-Seite nicht gefunden) O64266 `IF(I3==1;MIN(I1;0);IF(I2<I4;I1;IF(I1<0;0;I1)))` | 8308 |
| I1 der Formel | Reg 842, Skalierung 1000 → 1, keine Invertierung | 2936 |
| I3 | Abend_Spwr_Sperre: ab 180 min vor Sonnenuntergang | 8324 |
| Soc / MinSoc | Victron / SOC_Freigabe, live 95 | 8088, 7448 |
| IL6 | Reg 25611 | 7548 |
| Last WP | MinRt 2.700 s, SwPwr 1,5, MaxPwr 6,9, RT 300 | 8135 |

Arbeitsmodell, Formel nicht veröffentlicht, aus FUND: `A = -Gpwr - Spwr + Istleistung niedriger priorisierter Lasten - (Soc < MinSoc ? MaxSpwr 6 : 0)`, Einschalten bei `A > 1,5`. [Vermutung]
Spwr = -D bei Entladung D, also steht bei uns `A = -G + D + ...`. Die Sperre „Reserve 6 kW" wirkt nicht hart, siehe 26.10. und 23.10. 17:06. Ob IL6 selbst hinzugerechnet wird, bleibt offen: Mit IL6 und Reserve wäre 19.10. 06:00 klar eine Flanke (A = 4,4), ohne beides ebenso (A = 5,6), es kam keine. [sicher: Rechnung; Modell Vermutung]
Halten: Die Regel „Aus erst, wenn Bezug über 5,4 kW und MinRt abgelaufen" passt weiter (FUND).

## Tabelle je dunkler Flanke
Akku + = Entladung (`Meter LiFePO4 actual`, 30-min-Punkte davor/danach). Netz = Hauptstromzähler, 10-min-Punkt am nächsten. Entl = kWh der Stunde. „D nötig" = Entladung, die für A > 1,5 ohne Reserve reichen müsste, Wallbox als Istlast zurückgerechnet.
| Flanke lokal | Muster | SOC | Akku kW | Netz kW | WP / Wallbox kW | PV / Entl kWh | D nötig | Erklärt durch Entladung? |
|---|---|---|---|---|---|---|---|---|
| **14.10. 06:23:41** | a | 42 → 30 | 1,17 / -0,08; bei Flanke ≈ 5 [wahrscheinlich: Netz 0 bei WP 4,93] | -0,01 | 4,93 / 0 | 0,00 / 1,65 | 1,5 | Entladung ja, aber Gegenprobe 19.10. spricht dagegen: **nein** |
| 16.10. 06:10:44 | a | 50 → 31 | 3,14 / 3,08 | 0,34 | 4,08 / 0 | 0,00 / 2,89 | 1,84 | wie oben: **nein** |
| **19.10. 17:05:31** | b | 97 | **6,04** / 0,75 | 0,25 | 2,60 → 0 / nicht geprüft | 0,48 / 0,54 | 1,75 | **ja** [wahrscheinlich] |
| **19.10. 18:56:26** | b | 96 → 95 | 0 / 0,59 | 0,60 → 0,05 | 0 / 0 | 0,01 / 0,18 | 1,55-2,1 | möglich, Puls ≤ 7 min [Vermutung] |
| 22.10. 17:00:33 | b | 96 | -1,72 / -0,06 | 4,32 | 0 / 0 | 0,45 / 0,30 | 5,8 | **unklar**, Punkt zeigt Ladung [Vermutung: nein] |
| 22.10. 18:11:47 | b | 96 → 92 | 0 / 0 | 2,95 | 0 / 0 | 0,01 / 0,73 | 4,45 | möglich, Puls ≤ 10 min [Vermutung] |
| 23.10. 18:05:45 | b | 97 → 93 | 0 / 0 | 6,53 | 0 / 5,69 | 0,00 / 0,46 | 2,34 | möglich, Puls ≤ 12 min [Vermutung] |
| 23.10. 19:06:27 | b | 93 → 87 | 0 / 0 | 7,26 | 0 → 2,28 / 5,63 | 0,00 / 0,90 | 3,13 | möglich, aber SOC unter 95 [Vermutung] |
Fett: die 3 dunklen Flanken mit Ladung aus F76. Pulsdauer = Entl / D nötig, obere Grenze aus der Stundenenergie.

## Gegenprobe
### Entladung ohne Flanke
| Zeit lokal | SOC | Akku kW | Netz kW | WP kW | Flanke | Aussage |
|---|---|---|---|---|---|---|
| 19.10. 06:00 | 49 → 30 | **+5,68** / +4,04 | 0,04 | 4,73, st0 → st4 | keine | Stärker als 14./16.10. Widerlegt Muster a als reine Entladungsfolge |
| 30.10. 02:30 | ≈ 49 | +4,36 | -0,10 | 3,02, st1 → st4 wie 14./16.10. | keine | Auch der Warmstart ist kein Unterscheider. 16 Warmstarts gesamt, nur 2 mit Flanke |
| 13.10. 17:00-18:00 (15 Z) | 98 → 80 | 2,74 kWh/h | 0,06 | - | keine | SOC ≥ 95 vor Fix, Spwr = 0: Kontrolle zu 19.10. |
| 19.10. 20:00 und 21:00 | 89, 83 | +3,44, +3,57 | -0,27, -0,39 | - | keine | SOC unter 95 sperrt |
| 31.10. 15-16 Z | 93 → 74 | 1,14-1,63 kWh/h | - | - | keine | SOC unter 95 sperrt |
| 02.11. 13:15:55 | 44 | Spwr -8,147 (aus Katalog F78) | - | - | keine | Stärkster Wert; kurz, Spwr 30 s später -4,977. Letzter Statistik-Eintrag 31.10. |

Zählung (Stunden mit Entl ≥ 1,5 kWh, `[lokaler Pfad]`): 32, davon mit Flanke 3 (14.10., 16.10., 26.10. 15:36). [sicher]

### Vorher-Nachher-Fix (das stärkste Argument für Muster b)
| Zeitraum | Spwr abends | Dunkle Flanken ab 13 Z | Stunden ab 13 Z mit Entl ≥ 1 kWh |
|---|---|---|---|
| 01.10. - 18.10. 17:48 | immer 0 | **0** | 33, darunter bis 3,08 kWh |
| 18.10. 17:48 - 23.10. | -D | **6** | nicht ausgezählt |
| 24.10. - 02.11. | -D | 0 | SOC ≥ 95 abends nur 26.10. und 31.10. |

Vor dem Fix gab es abends ebenfalls SOC ≥ 95 (13., 15., 16., 17., 18.10.), die Tage sind also vergleichbar. Formeländerung per Dateivergleich, sonst keine EM-Änderung seit `UMBAU_stand_20261011_0034` (`[lokaler Pfad]`). [sicher für die Dateien; welcher Stand wann lief, nicht direkt gelesen]

### Flanken ohne Entladung
Keine dunkle Flanke liegt in einer Stunde mit Entl = 0, das Minimum ist 0,18 kWh. [sicher] Wenig trennscharf, weil abends fast jede Stunde etwas entlädt. Scharf ist nur 23.10.: 17 Uhr lokal (15 Z) Entl **0,00**, SOC 96, SG aus, keine Flanke; 18 und 19 Uhr Entl 0,46 und 0,90, je eine Flanke. [sicher]
Nebenbefund: Tagesflanken bei PV fallen fast alle in die Stunde, in der der SOC 95 überschreitet (16.10. 74 → 98, 19.10. 78 → 98, 20.10. 76 → 98). Das stützt die MinSoc-Sperre. [wahrscheinlich]

### Ausreißer gegen die SOC-Sperre
- **26.10. 15:36:09:** SOC 88, Akku +4,51, Netz -0,24, PV 1,31 kWh. Modell mit Reserve gibt A ≈ -1,3, trotzdem Flanke. [sicher: Messung]
- Morgens 14./16.10. und 23.10. 19:06 ebenso unter 95. [sicher]
- Mögliche gemeinsame Ursache: kurze Akku-Spitzen über 7,5 kW treffen einen Rechenzeitpunkt. Spitzen dieser Höhe gibt es (8,147 kW). Passt zur Seltenheit, ist aber nicht belegt. [Vermutung]

## Doku-Zitat
- Spwr: „Negativer Wert wenn der Speicher geladen wird." [Energiemanager, DE](https://www.loxone.com/dede/kb/energiemanager-2/), am 02.11. erreichbar. Gleichlautend EN: „Negative value when charging storage." [Energy Manager, EN](https://www.loxone.com/enen/kb/energy-manager-2/) [sicher]
- Gpwr: „Negativer Wert wenn ans Netz geliefert wird." (dieselbe Seite) [sicher]
- Abruf über den Web-Leser, der direkte Abruf per Skript wurde von loxone.com blockiert. Die Wörter MinRt und IL stehen nicht in der DE-Seite. Mindestlaufzeit nur aus FUND zitiert, nicht neu geprüft.

## Was bringt uns das
| Punkt | Wirkung | Einstufung |
|---|---|---|
| Derzeit | Dunkle Flanken heben 1497 nicht (seit 24.10. kein Zugriff auf 57, F76). Sie schalten aber Klimacontroller-Eingänge über Merker.Q | wahrscheinlich, aus F76 |
| Sobald I2 repariert wird (F76-Vorschlag) | Kehren die dunklen 45-min-Phasen zurück: **1-2, höchstens 2,6 kWh_el/Woche** laut F76/F74, sofern SOC ≥ 95 abends | Vermutung |
| Vorzeichenfehler | Betrifft auch Wallbox, Heizstab, Heizkörper am selben EM. Kosten dort nicht beziffert | wahrscheinlich |

**Vorschlag, nichts umgesetzt, du entscheidest** (Backup und Skill `loxone-xml-umbau` zuerst):
1. Nur den Abendzweig in O64266 (Z. 8308) drehen: `MIN(I1;0)` → `MAX(-I1;0)`. Dann mindert Entladung den Überschuss, wie die Notiz vom 18.10. es wollte. Rückweg: alter Ausdruck. Danach 2-3 Abende mit SOC ≥ 95 prüfen.
2. Den Tageszweig nicht mit drehen. Dort stimmt das Vorzeichen ebenfalls nicht, aber die PV-Starts laufen. Eine Umkehr ließe die Ladung als Überschuss zählen, die Lasten kämen deutlich früher. Eigene Entscheidung.
3. Das ersetzt nicht die Reparatur von I2 aus F76. Reihenfolge: erst 1, dann I2.

## Offen
1. **Muster a bleibt ungeklärt.** 2 Fälle, beide vor dem 18.10., seither 15 Tage kein weiterer bei mehreren passenden Starts. Eine Änderung am Morgenzweig gab es in den Dateien nicht.
2. Sekundengenaue Daten fehlen. Spwr, Gpwr und OL6 werden nicht aufgezeichnet. Für 5 der 6 Abendflanken ist D zum Schaltzeitpunkt nur eingegrenzt. Nötig: Mitschrift `control_state` über eine echte Flanke; heute kein SG-Ereignis.
3. SOC_Freigabe im Oktober: heute 95, Verlauf nicht lesbar. Notiz vom 18.10. nennt 95. [wahrscheinlich]
4. Warum steht der Akku in Pulsen bei SOC 96-97 still, während das Netz 3 kW trägt? Die 3 kW am 22.10. sind nicht WP, Wallbox oder Heizstab (alle 0); gehört zu F87.
5. RT: Flankenzeiten liegen nicht auf einem festen 5-min-Raster. Ausschalten kommt meist 7-39 s nach MinRt. Rechenintervall weiter unbekannt.
6. Offizielle Formel weiter nicht veröffentlicht.

## Stichproben
| Zeit | Wert | Quelle |
|---|---|---|
| 19.10. 06:05:01 lokal | 27545 = 0, 1497 = 520, 1539 = 4, 25611 = 482 (Gegenprobe; Akku 04:00 Z +5,68 aus Loxone-Statistik LiFePO4 Gruppe 1) | `[lokaler Pfad]` |
| 14.10. 06:25:02 lokal | 27545 = 1, 1497 = 570, 1539 = 4, 25611 = 360 (Muster a) | `[lokaler Pfad]` |
| 23.10. Stunde 15 Z | Bezug 7,26, PV 0,04, **Entl 0,00**, Lade 0,01 kWh; Stunde 17 Z Entl 0,90 | `[lokaler Pfad]`, Zeile `10-23` |

Skripte: `[lokaler Pfad]` bis `f78b_f.py`. Daten aus Loxone-Statistik: Meter `<UUID>`, Hauptstromzähler `<UUID>`, Wallbox `<UUID>`, „Berechneter SG Ready" `<UUID>`.