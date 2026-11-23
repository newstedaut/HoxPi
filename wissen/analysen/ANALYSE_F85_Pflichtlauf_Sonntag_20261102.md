# F85 - Legionellen-Pflichtlauf an einem normalen Sonntag, Vorhersage So 08.11.2026

Claude, Subagent, nur gelesen. An Anlage, Bussen, Loxone und Pi nichts geändert. Daten bis 02.11. 12:02 MEZ. **Vorhersage in Abschnitt 3 notiert 02.11.2026 ~12:10 MEZ, also vor dem Ereignis.**

## Ergebnis

1. **Der Feiertag hat am 01.11. genau eines bewirkt: die WP-Ladung <MAC>.** Der Kalender stellte 1497 um 13:00 auf 52, 1500 stand bei 47,1 °C, die WP startete 11 s später. Am normalen Sonntag bleibt 1497 auf 50, die WP startet dann erst bei etwa 45,1 °C. Der Stab selbst, das Fenster, der Zähler und der Reset hängen nicht am Feiertag. [sicher: Messung und Datei; wahrscheinlich: dass die Ladung ohne 52 ausgeblieben wäre, Gegenbeispiel 25.10.]
2. **So 08.11. kommt der Pflichtlauf, wenn vorher kein PV-Nachweis fällt:** Zähler um 12:00 = **6,80 d**, Schwelle 6,5 d seit 04:47. [sicher: Rechnung aus zwei Live-Lesungen; wahrscheinlich: kein PV-Nachweis bis dahin]
3. **Vorhersage So 08.11.: Stab 12:00, Reset etwa 16:25 (15:10-17:30), etwa 11 kWh_el (8-14), meist aus dem Netz, keine WP-Ladung im Fenster.** [Vermutung: Ende und kWh; wahrscheinlich: Rest]
5. **Netto-Rechnung:** Ist ~6,7 ist am normalen Sonntag eher ~7,7 kWh_el/Woche (5,7-9,6). B ~2,6 hält. A' ~4,0 hält **nur**, wenn etwas die WP aktiv startet; "nur Reihenfolge" reicht nicht. Damit ist der einzige saubere Weg B. [wahrscheinlich; alles Rechnung, Messung erst 08.11.]
6. **Thermometer-Termin So 08.11. ist richtig, aber nicht "nach 12 Uhr", sondern 10 bis 30 min nach dem Reset**, also etwa 16:35-16:55 im Mittel. Zeichen: "Tage seit Legionellenschutz" springt auf 0. [wahrscheinlich]

**Nebenfund Zähler:** Der Reset wirkt als Pegel. Der Zähler bleibt auf 0, solange der kühlere Fühler nicht unter 59,5 °C gefallen ist, und läuft erst dann los: am 01.11. nicht ab 15:54, sondern ab **16:47:00**. Darum liegt er 53 min hinter der Uhr (F81 las 0,68 d, das war kein Ablesefehler). [sicher: zwei Lesungen, Rate 1 d/d; wahrscheinlich: Mechanismus]

## 1. Logik mit Zeilen

**Laufender Stand:** Der Umbau 01.11. 23:36 ist nicht im Miniserver (F67, `[lokaler Pfad]` Z. 155). Letzter Stand davor ist `[lokaler Pfad]` (SHA C02DE5E8, 25.10. 22:44). [wahrscheinlich, Miniserver nicht zurücklesbar] **Das ändert hier nichts:** alle 28 Bausteine der Kette sind in diesem Stand, in `UMBAU_wwabend_20261025_NEU.Loxone` und in `UMBAU_kwl_zirk_wcug_20261101_NEU.Loxone` gleich, nur Koordinaten ignoriert (`f85_e.py`). [sicher] Das Einspielen vor dem 08.11. ändert die Kette also nicht.

"-" in der Spalte NEU heisst: Zeile nicht einzeln notiert, Baustein laut Vergleich gleich.

| Schritt | Baustein | Z. Stand 2336 | Z. NEU 01.11. | Inhalt |
|---|---|---|---|---|
| Nachweis-Fühler | [Formel](https://www.loxone.com/dede/kb/formel/) "kühlerer oberer Fühler" | 16978 | - | `MIN(1-Wire oben; 1500)` |
| Schwelle | [Schwellwertschalter](https://www.loxone.com/dede/kb/schwellwertschalter/) | 16990 | - | ein ab 60,0, aus unter 59,5 |
| Haltezeit | [Einschaltverzögerung](https://www.loxone.com/dede/kb/) | 17002 | 16883 | 1800 s; Q geht auf Reset und Zirk-Spülung 10 min (Z. 17129) |
| Zähler | [Betriebsstundenzähler](https://www.loxone.com/dede/kb/) | 17011 | 16892 | zählt immer, 10-Tage-Intervall, über 10 d Push |
| Tage | Formel | 17027 | - | `MAX(0;10-Restzeit)` |
| **fällig** | Schwellwertschalter | 17046 | 16927 | ein ab **6,5 d**, aus unter 0,5 d |
| **Fenster** | [Schaltuhr](https://www.loxone.com/dede/kb/schaltuhr/) "Pflichtfenster" | 16697, Eintrag 16713 | 16578, 16594 | `From=720 To=1080 Ix=6`: Sonntag 12:00-18:00; Betriebsarten nur Mo-So, kein Feiertag |
| **Pflichtlauf** | [UND](https://www.loxone.com/dede/kb/und/) | 17100 | 16981 | Fenster UND fällig |
| Legionellen aktiv | [ODER](https://www.loxone.com/dede/kb/logik/) | 17109 | - | Pflichtlauf ODER PV-Legionellen (Z. 17091, 17082, 17058: ab 3 d UND Prognose ab 26 kWh UND PV-Stufe 2 UND WP fertig) |
| **Soll Stab** | Formel | 17118 | 16999 | `IF(I1>0;62;59)` |
| Stab-Regler | 2-Punkt | 16810 | 16691 | 1-Wire oben, Hysterese 2 K, laut Notiz ein unter 61, aus über 63 |
| **Stab** | UND "Freigabe", dann Relais | 16801 | - | 2-Punkt UND (PV-Anforderung ODER Legionellen) |
| **WW-Soll WP** | Schaltuhr "Sollwert-Kalender" | 16343, Einträge 16357-16365 | 16252 ff. | Grundwert 50; siehe unten |
| Prognose-Deckel | Formel | 16909 | - | Prognose gut: `MIN(Kalender;50)` |
| Letzte Stufe | Formel "WW-Soll final" | 16523 | 16432 | `MAX(MAX(MIN(I1;52+5*I4);I2*52);I3*57)`, I2 Boost, I3 Kick |

**Wann was** [sicher für die Datei]:
- **Stab:** So 12:00 bis zum Nachweis oder bis 18:00, wenn fällig. Die Bedingung "WP fertig" (Z. 16792) gilt nur im PV-Zweig, der Pflichtlauf umgeht sie. Parallelbetrieb ist also möglich.
- **WP:** Von "Legionellen aktiv" führt kein Weg zu 1497 (Ausgänge von Z. 17109 nur Z. 16753 und 17119). Der Pflichtlauf startet die WP also nie. Sie lädt nur nach ihrer eigenen Regel: Kalender, Boost oder Kick (SF2 unter 40, F84).
- **Reset:** Q der Einschaltverzögerung. Dadurch fällt "fällig", dadurch geht der Stab aus.

**Sonntag gegen Feiertag:**
| Schaltuhr | Sonntag (Ix 9) | Feiertag (Ix 0) | Sonst |
|---|---|---|---|
| Pflichtfenster, Z. 16713 | 12:00-18:00 | Betriebsart nicht vorhanden, Sonntag gilt | nichts |

Die Zuordnung Ix zu Betriebsart stammt aus `Modes` und der Live-`modeList`. Dass eine Schaltuhr ohne Feiertag auf den Wochentag zurückfällt, ist live zu sehen: am 02.11. 10:57-10:59Z steht der Kalender auf `mode=2` (Freier Tag), das Pflichtfenster zugleich auf `mode=3` (Montag). [sicher] Die Notiz Z. 16343 nennt den Grund für die Lücke: "sonntags heizt der Heizstab ... sonst doppelt geladen". Der Sonntag ist also Absicht, der Feiertag wurde dabei übersehen. [wahrscheinlich]

## 2. Messung 01.11. gegen Logik

Rohwerte /10 außer P_el. Volllogger `2026-11-01.csv`, 5 min; Minutenwerte aus `ww_hires.csv`.

| Zeit MEZ | 1497 | 1500 | 27483 | 1504 | 1539 | 25611 | Ereignis | Hängt am Feiertag? |
|---|---|---|---|---|---|---|---|---|
| 12:00:01 | 50,0 | 47,2 | 46,1 | 0 | 1 | 162 | Stab ein, 2,5 kW (Loxone, Bucket 11Z = 2,50 kWh); WP im Heizen | nein |
| 12:30:02 | 50,0 | 47,2 | 47,4 | 0 | 0 | 0 | Stab allein, rund 25 min | nein |
| **13:00:02** | **52,0** | 47,1 | 44,3 | 0 | 0 | 0 | Kalender schaltet (hires 13:00:02) | **ja** |
| **13:00:13** | 52,0 | 47,1 | 44,3 | | | | **WW_Status = 1, WP lädt** (hires; im Volllogger 1504 erst 13:05) | **ja** |
| 13:05:01 | 52,0 | 46,8 | 44,2 | 1 | 4 | 450 | WW-Ladung | ja |
| 13:37:02 | 52,0 | 51,8 | 51,0 | | | | Status 0, 27489 +4 kWh | ja |
| 13:40:02 | 52,0 | 52,4 | 51,6 | 0 | 0 | 0 | wieder Stab allein | Niveau ja |
| 15:13:51 | 52,0 | 60,0 | | 0 | | | 1500 erstmals 60,0 (hires) | nein |
| ~15:24 | | | | | | | Nachweis-Uhr läuft: 30 min vor Reset. 1-Wire lag also etwa 10 min hinter 1500 | nein |
| 15:50:01 | 52,0 | 62,0 | 61,4 | 0 | 1 | 170 | 1500 Spitze | nein |
| **15:54:07 / 15:54:21** | 52,0 | 61,6-61,9 | 61,1 | 0 | 1 | 172 | Stab aus / Zähler 7,92 -> 0 (F57) | nein |
| 16:00:02 | 50,0 | 61,6 | 60,4 | 0 | 1 | 176 | Kalender zurück | ja |
| 16:26:52 | 50,0 | 60,1 | | | | | 1500 letztmals 60 (hires) | nein |
| 16:44:51 | 50,0 | 59,4 | 58,2 | 0 | 0 | 0 | 1500 erstmals unter 59,5 | nein |
| **16:47:00** | | | | | | | **Zähler beginnt zu laufen** (aus Live-Wert) | nein |

- **Gegenbeispiel normaler Sonntag 25.10.** (ohne Stab, Zähler noch unter 6,5): 1497 bleibt 50 um 13:00, 1500 stand bei 47,3 und fiel weiter. Die WP startete erst **14:07:22 bei 44,9 °C**. 1497 ging erst danach auf 57/52 durch SF2 unter 40. [sicher] Genau der Unterschied zum 01.11.: Dort startete die WP bei 47,1 °C.
- Die Morgenladung 01.11. 05:50-06:36 lief mit Kick 57 und hat mit dem Feiertag nichts zu tun. [wahrscheinlich]
- **Welche Betriebsart am 01.11. wirklich aktiv war, ist nicht zurücklesbar** (Modus hat keinen Verlauf). Belegt ist nur 1497 = 52 ab 13:00 an einem Sonntag, also nicht Betriebsart Sonntag. Feiertag (Z. 352/420) oder Freier Tag würde das gleiche ergeben. [sicher]

## 3. Vorhersage So 08.11.2026 (notiert vor dem Ereignis)

**Zähler:** 0,79824 d um 10:56:28Z und 0,80209 d um 11:02:01Z. Das ergibt beide Male Laufstart **01.11. 15:47:00Z = 16:47:00 MEZ**, Rate genau 1. Daraus: 6,5 d am **08.11. 04:47 MEZ**, um 12:00 MEZ **6,80 d**. [sicher, sofern kein Nachweis dazwischen]

**PV-Nachweis vorher?** Möglich ab 04.11. 16:47 (3 d), braucht Prognose ab 26 kWh. Heute 16,2 und morgen 12,4 kWh (live 02.11. 11:59 MEZ). Seit 24.10. fiel in dem Zweig kein Stab-kWh. Unwahrscheinlich. [wahrscheinlich] Eine Wetterprognose bis zum 08.11. habe ich nicht (`loxone__weather` nicht verfügbar).

**Startlage:** T_m um 12:00 an den 9 Tagen 24.10.-01.11.: Median **47,3 °C** (46,65 am 01.11.; ohne 31.10. mit 30,45 reicht es von 44,25 bis 49,7). 1500 um 12:00: Median 48,5.


|---|---|---|---|
| 49,7 | 14:40, 6,7 kWh | 15:39, 9,1 kWh | 16:59, 12,5 kWh |
| **47,3** | 15:13, 8,0 kWh | **16:24, 11,0 kWh** | 18:00, 15,0 kWh, Grenzfall |
| 44,25 | 15:55, 9,8 kWh | 17:22, 13,4 kWh | Fenster verfehlt, 15,0 kWh |

**Vorhersage** (alles MEZ):
| Größe | Wert | Sicherheit |
|---|---|---|
| Zähler 08.11. 12:00 | 6,80 d (± 0,01) | sicher, ohne PV-Nachweis |
| Stab Beginn | 12:00 (± 2 min), 2,5 kW | wahrscheinlich |
| Stab-Ziel | 62 °C am 1-Wire (nur in der Logik, kein Register) | sicher: Datei |
| 1497 13:00-16:00 | **50**, solange SF2 nicht unter 40 fällt | wahrscheinlich |
| WP-WW im Fenster (1504) | keine, außer 1500 fällt auf etwa 45,1 oder SF2 unter 40 | wahrscheinlich |
| 1500 erreicht 60 °C | etwa 15:50 (14:10-17:00) | Vermutung |
| Reset | etwa **16:25**, 15:10-17:30 | Vermutung |
| Stab-Energie (Tageszähler "Heizstab Trinkwasser") | etwa **11 kWh_el**, 8-14, hart höchstens 15,0 | Vermutung, Obergrenze sicher |
| Woher | überwiegend Netz, wie 01.11. | wahrscheinlich, Wetter offen |
| Fenster verfehlt (kein Reset bis 18:00) | etwa 10-15 % | Vermutung |

**Widerlegt, wenn:**
1. Zähler 08.11. 11:55 nicht bei 6,80 d (und kein Nachweis in der Woche) -> Zählerlogik falsch.
2. Zähler hoch und Stab nicht bis 12:05 an -> Fenster oder Sonntagsbetriebsart falsch.
3. **1497 = 52 um 13:00 mit SF2 über 40 -> Feiertags-Erklärung falsch** (oder Eintrag für den Tag in der App, siehe Offen).
4. WP-WW-Start mit 1500 über 47 °C und SF2 über 40 -> Startregel falsch.
5. Stab-Energie über 15,1 kWh oder Stab läuft nach 18:01 -> Fensterlogik falsch.
6. Reset vor 14:30 oder nach 18:00 trotz Fühler über 60 ab 17:30 -> Modell oder Haltezeit falsch.

**Wenn das Fenster verfehlt wird:** Stab um 18:00 aus, kein Reset, Wärme bleibt im Speicher. Push "überfällig" dann ab 11.11. 16:47 (10 d), nächster Lauf 15.11. Hygienisch keine Katastrophe, teuer ohne Ertrag. [sicher: Logik]

**Thermometer (F82, Waschtisch Bad):**
- So 08.11. ist der richtige Tag. [wahrscheinlich]
- Sinnvoll ab **10 min nach dem Reset** (Zirk-Spülung 10 min, Z. 17129), spätestens 30 min danach. Am 01.11. entspräche das 16:05-16:25, 1500 bei 61,0-60,3 °C. Danach fällt der Speicher, um 16:44 schon unter 59,5.
- **Vorher in der App schauen:** um 12:00 Zähler ab 6,5 d, dann läuft es. Springt der Wert auf 0, Stoppuhr 10 min, dann messen. Bleibt er bis 17:30 hoch, Messung lassen, heute kommt kein Nachweis.
- Uhrzeit notieren, damit ich den Wert gegen 1500 aus `ww_hires.csv` (1-min) stellen kann. Thermometer in den Strahl, nicht die Hand (`ANALYSE_F82_Verbruehschutz_Fotos_20261102.md` Z. 68 f.).

## 4. Netto-Rechnung F60/F81 2.6

F60 rechnet Netto = (Stab über 52: 5,39 - Gutschrift 1,36) + Malus. Malus = Stab-kWh unter 52 x (1 - 1/2,86), am 01.11. 4,17 x 0,65 = 2,71, Summe 6,7. Das Gerüst übernehme ich, Eingangswerte F60 nicht nachgerechnet.

| Variante | F60/F81 | Normaler Sonntag | Urteil |
|---|---|---|---|
| Ist, Stab ohne WP-Hilfe | ~6,7 | **~7,7 (5,7-9,6)**: Stab 11 (8-14), Anteil unter 52 = 5,6 (2,6-8,6) | Verfälscht, in Summe mäßig. Zwei Effekte heben sich teils auf: Am 01.11. nahm die WP dem Stab 4 kWh_th ab (ohne sie 13,6 kWh Stab und 9,3 netto), aber der 01.11. hatte auch überdurchschnittlich viel Zapfung (5,7 kWh in Phase a). [wahrscheinlich] |
| A' Stab erst nach WP-Ladung | ~4,0 | ~4,0 **nur mit aktiver WP-Ladung auf 52** | Bei 1497 = 50 startet die WP nicht von selbst: 1500 um 12:00 lag nur an 1 von 9 Tagen unter 45,1. Mit 52 an 3 von 9 (unter 47,3). "Nur Reihenfolge" reicht also nicht, der Stab würde warten und nichts käme. [sicher: Zählung; wahrscheinlich: Folge] |
| B WP 57, dann Stab-Rest | ~2,6 | ~2,6-3 | Hält. Kick 57 startet bei 1500 bis etwa 52: 9 von 9 Tagen. Basis 50 statt 52 kostet etwa 0,3 kWh_el mehr. [wahrscheinlich] |

**Korrigierte Aussage:** Einsparung von B gegen den normalen Sonntag eher **~5 kWh_el/Woche** statt ~4. A' ist keine eigene billige Stufe, sondern braucht denselben WP-Start wie B. Die Empfehlung "erst 08.11. ansehen" bleibt richtig; der 08.11. misst Ist, nicht A' oder B. [wahrscheinlich]

## Belege

Alles nur gelesen. Skripte `[lokaler Pfad]` bis `f85_g.py`.

**Messung:**
- `/home/<user>/hoxpi_fulllog/2026-11-01.csv`, `2026-10-25.csv.gz` (Kopien im Ordner oben), Spalten 1497, 1499, 1500, 27483, 1504, 1539, 25611, 27489.
- `/home/<user>/hoxpi_fulllog/ww_hires.csv`, Kopie `[lokaler Pfad]`: 01.11. 13:00:13 Status 1, Ist 471, Soll 520; 13:37:02 Status 0, Ist 518; 25.10. 14:07:22 Status 1, Ist 449, Soll 500.
- Loxone `<UUID>` value 0,7982407 (10:56:28Z), 0,8020949 (11:02:01Z).
- Loxone `<UUID>` mode 3, value 0; `<UUID>` mode 2, modeList.
- Loxone Heizstab `<UUID>` Leistung: 11:30Z bis 14:30Z 2,5 kW, 15:00Z 0 (30-min-Punkte). 1-Wire `<UUID>`, nur Stundenwerte: 15:00 MEZ 58,5; 16:00 61,0; 17:00 60,1.
- PV_Forecast_Today 16,16, Tomorrow 12,36.

**Datei:** `[lokaler Pfad]`, Zeilen Abschnitt 1. Kalender Z. 352/420 Allerheiligen; Ferien-Einträge Z. 440-448 enden 04.04.2026.

**Theorie, nicht gemessen:** Laufzeit- und kWh-Modell, Netto-Rechnung, Wahrscheinlichkeit Fensterverfehlen. Übernommen aus F57/F60: Zeiten 15:54:07 und 15:54:21, Stab-Stunden, C = 0,47, AZ 2,86, Phase (b).

Loxone-Links aus früheren Analysen übernommen, nicht geöffnet; für Einschaltverzögerung und Betriebsstundenzähler keine geprüfte Einzeladresse, deshalb nur die KB-Startseite.

## Offen

- **Live-Kalender weicht von der Datei ab:** Heute steht der Kalender auf `mode=2` (Freier Tag), in der Datei gibt es dazu für 02.11. keinen Eintrag. Wohl in der App eingetragen (Allerseelen?). Ein solcher Eintrag für 08.11. ist aus der Datei nicht auszuschließen; dann käme 52 um 13:00. Die Einträge sind nicht lesbar. [sicher: Abweichung; Vermutung: Ursache]
- Betriebsart am 01.11. nicht zurücklesbar.
- 1-Wire nur Stundenwerte, Übergang über 60 °C nur aus Reset minus 30 min gefolgert (etwa 15:24). Warum 1-Wire beim Aufheizen hinter 1500 liegt und danach darüber, nicht geklärt.
- Laufstart 16:47:00 passt zu 1500 erstmals 59,4 um 16:44:51, aber nicht exakt. Einzelwert zwischen Loxone-Abfrage und hires nicht trennbar. Pegel statt Flanke beim Reset ist aus der Messung gefolgert. Loxone-Doku nicht gelesen.
- Übersteht der Zähler "In Miniserver speichern"? Notiz Z. 17011 sagt ja. Rückrechnung 7,92 d auf 24.10. ~18:49 MESZ passt zum Überleben der Speicherungen vom 25.10., F57 nannte ~12 Uhr. Nicht direkt getestet. Falls er auf 0 fällt, entfällt der Lauf am 08.11.; vor dem Sonntag einmal lesen.
- Ob Netto ~7,7 stimmt, zeigt erst der 08.11.: Stab-kWh und Startlage 12:00 einsetzen.

## Was bringt uns das

- **Der Vorbehalt aus F81 stimmt, die Folge ist aber kleiner als befürchtet:** Der 01.11. war in genau einem Punkt Sonderfall (WP-Ladung). Ist steigt von ~6,7 auf ~7,7, B bleibt ~2,6.
- **Für die Entscheidung Legionellen:** Nur noch eine Option vorlegen, nämlich B, weil A' denselben WP-Start braucht. Hebel gegen den normalen Sonntag etwa 5 kWh_el/Woche [wahrscheinlich]. Dazu entfällt das Risiko, das Fenster zu verfehlen. Nichts beschlossen, Entscheidung bei dir.
- **Für dich So 08.11.:** Um 12:00 einmal in die App, nach dem Sprung auf 0 Stoppuhr 10 min, dann Waschtisch messen. Kein Termin "ab mittags" nötig.
- **Für den Stundenbericht:** Wer am 08.11. ab 12:00 prüft, hat oben eine fertige Vorhersage mit sechs Widerlegt-Bedingungen, und der scheinbar nachlaufende Zähler ist kein Fehler.