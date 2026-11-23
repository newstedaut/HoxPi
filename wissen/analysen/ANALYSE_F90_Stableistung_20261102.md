# F90 - Wie viel zieht der PV-Heizstab im Speicher wirklich? (02.11.2026, ca. 15:15 MEZ)

Claude, Subagent, nur gelesen. An Anlage, Bussen, Miniserver, Projektdatei und Pi nichts geaendert. Rohdaten-Zeitstempel Loxone in UTC ("Z"); Pi-Zeiten lokal, also bis 24.10. MESZ (Z+2), am 01.11. MEZ (Z+1).

## Ergebnis

1. **Der Stab zieht rund 2,5 kW, Band 2,3-2,7 kW.** [wahrscheinlich] Vier saubere Schaltkanten ergeben 2,26 / 2,36 / 2,62 / 2,69 kW, Mittel 2,48 kW. Vier saubere Heizphasen (23.09., 25.09., 29.09., 01.11. 13:45-14:30) ergeben 2,56-2,59 kW (+/- 0,24 aus C). Typenschild 2,5 kW bei 230 V.
2. **Die 2,50 kWh/h sind keine Messung, sondern Festwert x Einschaltzeit.** [sicher: Projektdatei] Der Wert ist aber richtig gewaehlt [wahrscheinlich]. Bis 23.09. stand dort 2,82, und das war zu hoch.
3. **Der Ueberhang in den Stabstunden am 01.11. kommt nicht vom Stab.** [wahrscheinlich] Dafuer muesste der Stab 3,7-4,7 kW ziehen. Das widerlegen die Kanten und der Speicher: Er stieg in keiner sauberen Phase ueber 5,2 K/h, 4,7 kW waeren etwa 9,6 K/h. Um 16 Uhr, Stab aus, liegt der Rest noch bei 2,07 kW.
4. **F87-Rest und F85-Netto brauchen keine Korrektur.** [wahrscheinlich] Das Band 2,3-2,7 kW bewegt den F87-Rest um +/- 0,8 kWh am Tag, F85 "heute" um +/- 0,5 kWh je Woche, B kaum.
5. **Nebenbefund R119 geklaert:** Der Stab laeuft ohne Stufen durch; die Fuehler reagieren erst rund 15 min nach dem Einschalten. [wahrscheinlich] Das erklaert auch den alten Widerspruch "Zaehler laeuft, Temperatur steht".

## Tabelle je Stablauf

Methode a = Stufe in der Bilanz, Methode b = C x Steigung + Ruheverlust 0,16 kW, C = 0,47 +/- 0,04. Methode c gilt fuer alle Laeufe: Der Zaehler zeigt seit 24.09. Laufzeit x 2,50, davor Laufzeit x 2,82.

| Lauf | Kante, aus Zaehlerstunde | a: Stufe kW | Fenster b (lokal) | b: K/h T_m | b: kW | Bewertung |
|---|---|--:|---|--:|--:|---|
| 23.09. | AUS 13:32Z | **2,62** (+/- 0,3) | 14:00-15:00, volle Stabstunde | 5,17 | **2,59** | beide sauber [wahrscheinlich] |
| 25.09. | AUS 12:51Z | nicht nutzbar: WP startet fast zugleich, Wallbox an dem Tag 7,5 kWh | 14:00-14:50 | 5,18 | **2,59** | nur b |
| 26.09. | AUS 12:41Z | **2,69** (roh 2,49 + PV-Trend 0,21; +/- 0,3) | 14:00-14:40 | 6,09 | (3,02) | a sauber; b zu hoch, siehe Fehler |
| 27.09. | EIN ca. 13:20Z, AUS ca. 14:00Z | **2,26** (EIN 2,29, AUS 2,23; +/- 0,3) | 14:20-14:55 | 4,54 | 2,30 | a sauber, Zeitpunkt aus der Stufe selbst |
| 28.09. | AUS 13:04Z | (3,53) | - | - | - | Ausreisser: Stufe groesser als Stab, kein WP, keine Wallbox. Ein weiterer Verbraucher fiel weg [Vermutung] |
| 29.09. | - (Batterie laedt und schluckt die Stufe) | - | 16:05-17:00, volle Stabstunde | 5,14 | **2,58** | nur b |
| 01.10. | AUS 13:19Z | nicht nutzbar: WP geht fast zugleich aus, Batterie 1,37 kW | 14:30-15:18 | 5,80 | (2,89) | b zu hoch |
| 01.11. | EIN 11:00:01Z, AUS 14:54:07Z | EIN 2,7-2,9, AUS ca. 1,9 (je +/- 0,6 bis 1) | 13:45-14:30 | 5,10 | **2,56** | Netz zu unruhig; b sinkt spaeter, siehe unten |
| 01.11. | wie oben | - | 15:00-15:50 | 3,17 | 1,65 | Untergrenze, SF2 faellt zwischendurch |

Werte in Klammern gehen nicht in das Ergebnis ein. Skripte: `[lokaler Pfad]`, `f90_b.py`, `f90_wp.py`, `f90_lox.py`, `f90_pi.py`; 1-min-Daten `f90_ww.csv` (Auszug aus `/home/<user>/hoxpi_fulllog/ww_hires.csv`).

## Methode a: Bilanz an den Kanten

**Neue Datenlage:** `control_statistics` Gruppe 2 `raw` beim Hauptstromzaehler `<UUID>` liefert Zaehlerstaende im 10-min-Raster, also echte Energie je 10 min und keine Stichprobe wie Gruppe 1 in F87. [sicher] PV und Batterie zaehlen dort nur stuendlich; Batterie Gruppe 1 ist eine 30-min-Stichprobe.

**Kantenzeit:** nur moeglich, wenn eine Zaehlerstunde teilweise voll ist und der Lauf zusammenhaengt, z. B. 26.09. 12Z 1,708 kWh / 2,5 kW = 41,0 min. Der Sprung liegt genau im Eimer 12:40-12:50Z.

**Saubere Kanten:** PV-Tage, Batterie steht, keine Wallbox in der Stunde, WP aus oder aus 1-min-P_el herausgerechnet. Die Stufe zeigt sich direkt in der Einspeisung (kW je 10 min):

| Kante | vorher | nachher | Korrektur |
|---|---|---|---|
| 26.09. AUS | 3,01 / 2,92 | (5,32) / 5,50 / 5,40 | PV-Trend -0,42 kW/h x 0,5 h, aus 7 PV-Zaehlern 12Z 6,79 und 13Z 6,37 kWh |
| 23.09. AUS | 0,35 + WP 1,76 / 0,97 + WP 1,05 | (4,32) / 4,72 / 4,66 | WP aus 1-min-Daten |
| 30.09. AUS | 1,81 / 1,65 | 3,73 / 3,41 / 3,46 | PV-Trend -1,34 kW/h x 25 min; die Uhrzeit 14:10Z trifft die Eimergrenze |
| 27.09. EIN/AUS | 3,49 auf 1,34; 1,28/1,11 auf 3,83 | | Batterie 0,23-0,36 kW; das Mittel aus EIN und AUS hebt den PV-Trend auf |

**Probe der Methode:** Die WP-Stufe erscheint mit der richtigen Groesse: 30.09. 13:20Z 2,09 auf 0,66 kW = 1,43 kW gegen P_el ~1,6 kW; 23.09. 13:10Z 2,37 auf 0,35 = 2,0 kW gegen 1,76 kW. Daher kommt die Streuung +/- 0,3 kW. [wahrscheinlich]

**01.11. taugt allein nicht fuer die Stufe.** Netz minus WP schwankt um 2-4 kW ohne Stabkante (5,26 / 4,27 / 1,37 / 2,55 / 3,75 / 2,21 kW ab 14:30Z). Dazu Batterie-Stoesse 4,46 kW (11:30Z) und 6,25 kW (14:00Z). [sicher als Messung] EIN: vorher 0,97, nachher 3,70 kW = 2,73 kW, mit PV und Batterie etwa 2,9 kW. AUS: vorher Mittel 4,77, nachher 2,83 kW = ca. 1,9 kW. Beides passt zu 2,5 kW, belegt es aber nicht allein.

## Methode b: Speicher-Anstieg, und ihre Fehler

- **Beide Fuehler zusammen:** T_m = (1500 + 27483)/2, wie C in F1 bestimmt. 1500 allein aendert das Ergebnis in den sauberen Fenstern kaum (2,60 / 2,61 / 2,61 statt 2,59 / 2,58 / 2,59 kW); in Fenstern mit Schichtung streut er mehr (01.11. 15:00-15:50: 1,79 statt 1,65 kW).
- **Fehler C:** +/- 8,5 % = +/- 0,21 kW, dazu Ruheverlust +/- 0,03 kW. Das ist der groesste Einzelposten. [sicher als Rechnung]
- **Zu hoch nach einer WW-Ladung:** 26.09., 30.09. und 01.10. folgen kurz auf WP-Ladungen, die Schichtung gleicht sich noch aus. Deshalb 2,85-3,02 kW; nicht gewertet. [wahrscheinlich]
- **Zu tief im Ganzlauf:** Die ersten Minuten zeigen beide Fuehler nichts. 25.09.: Einschalten rechnerisch 13:32, T_m steigt erst ab etwa 13:48. Ganzer Lauf: Zaehler 3,26 kWh gegen Speicher 2,42 + Ruhe 0,22 = 2,64 kWh; es fehlen 0,62 kWh, das sind 15 min x 2,5 kW. [sicher als Rechnung; Vermutung: Waerme geht zuerst in eine Zone ausserhalb der Fuehler]

**Gegenprobe zu F1:** Mit 2,5 kW ergibt sich aus den drei sauberen Fenstern und 13:45-14:30 C = 0,452-0,459 kWh/K, mit 2,6 kW etwa 0,47. Das liegt im Band von F1. C bleibt verbindlich 0,47 +/- 0,04. Kein Rundlauf, weil die Kanten ohne C auskommen. [wahrscheinlich]

**R110 nachgerechnet:** "2,52 kW" stimmte eher zufaellig [wahrscheinlich]: C = 0,576 und die Anlaufzeit im Fenster glichen sich aus. Der Vermerk vom 25.10. dort (C = 0,47 ergibt 2,06 kW) nimmt das Fenster 13:00-15:00 MESZ und damit die Anlaufzeit mit. Nur die volle Stabstunde 14:00-15:00 ergibt 2,59 kW.

## Methode c: Zaehler-Logik

**Festwert x Einschaltzeit** [sicher]. `[lokaler Pfad]`:
- Z. 16727 [Zaehler](https://www.loxone.com/dede/kb/zaehler/) `Type="MeterDig"` "Heizstab Trinkwasser", Notiz "24.09.2026: Ppwr 2,82 -> 2,5 kW".
- Z. 16729 Eingang A = `<UUID>`, Ausgang des [UND](https://www.loxone.com/dede/kb/und/) "Heizstab: Freigabe" (Z. 16801).
- Z. 16732 `Ppwr Def="2.5"`.
- Z. 17158-17162 Ausgangsverweis auf Relais Q8 (Z. 6270) haengt am selben Signal. Zaehler und Relais schalten also gleich.
- Z. 8137 [Energiemanager](https://www.loxone.com/dede/kb/energiemanager/)-Last `MaxPwr="2.5"`.

Folgen:
- **Daten:** Stundenmaximum 2,8200 bis 23.09., 2,5000 ab 29.09. (14Z 2,500003), 01.11. dreimal 2,5000. [sicher]
- **Der Zaehler sieht weder Spannung noch einen stabeigenen Thermostat.** Bei z. B. 240 V Netzspannung waeren es rechnerisch 2,72 kW bei gleicher Anzeige. Ein Spannungswert ist in Loxone nicht vorhanden (`control_find`: nur Batteriespannung). [sicher]
- **Typenschild:** Austria Email EBH-REU-1B, 2,5 kW / 230 V / 10,9 A, laut `[lokaler Pfad]` Z. 643. Foto hier nicht geprueft. `BAUTEILE_BEKANNT.md` enthaelt den Stab nicht. [wahrscheinlich]
- **Altbestand:** Summen bis 23.09. sind um 12,8 % zu hoch, wie R110 sagt. Sept. 1.-23.: 59,5 kWh Zaehler, rund 6,8 kWh zu viel. Die September-Zahl 87,9 kWh in F57 enthaelt das. Der Jahreszaehler 1206,6 kWh waere etwa 130 kWh zu hoch, falls 2,82 das ganze Jahr galt. [Vermutung fuers Jahr]

## Korrektur F87-Rest

Rest A 01.11., Zaehler 2,50 kW, gegen Band:

| Stunde MEZ | Rest A F87 | Rest bei 2,3 kW | Rest bei 2,7 kW | Ueberhang gegen Tageswert 0,97 kW |
|---|--:|--:|--:|--:|
| 12 | 2,20 | 2,40 | 2,00 | 1,0-1,4 |
| 13 | 3,16 | 3,36 | 2,96 | 2,0-2,4 |
| 14 | 2,66 | 2,86 | 2,46 | 1,5-1,9 |
| 15 | 2,60 | 2,76 | 2,44 | 1,5-1,8 |
| 16, Stab aus | 2,07 | 2,07 | 2,07 | 1,1 |

- **Tagessumme Rest A:** 28,26 kWh, Band 27,5-29,0 kWh. Anteil bleibt rund 52 %. [wahrscheinlich]
- **Der Ueberhang bleibt.** Er ist echte, nicht zugeordnete Last. Sie endet nicht mit dem Stab (16 Uhr), und 15:00-15:20 MEZ steht das Netz fast still (0,28 und 0,14 kW), waehrend die Batterie entlaedt: Stundenwert 1,72 kWh, Probe 6,25 kW um 15:00. Das ergibt grob 5,7 kW Last bei WP = 0, davon 3,2 kW neben dem Stab. [sicher: Messwerte; Vermutung: dass die 1,72 kWh ganz in diese 20 min fielen]
- **Keine Zuordnung.** Sonntag/Feiertag mittags ist Haushalt moeglich, das ist nicht belegt. [Vermutung]

## Korrektur F85-Netto

Geruest aus F60/F85 unveraendert. Eingang: kWh = Laufzeit x P; Waermebedarf bleibt, der Stabanteil skaliert.

| Groesse | F85/F60 | bei 2,3 kW | bei **2,5 kW** | bei 2,7 kW | Urteil |
|---|--:|--:|--:|--:|---|
| 01.11. Stab real kWh | 9,56 | 8,80 | **9,56** | 10,32 | Zaehler zeigt immer 9,56 |
| **Ist 01.11.** netto | ~6,7 | 6,1 | **6,7** | 7,4 | keine Aenderung |
| **heute**, normaler Sonntag netto | ~7,7 | 8,2 | **7,7** | 7,3 | keine Aenderung; hoehere P = weniger Verlustzeit |
| **A'** netto | ~4,0 | 3,6 | **4,0** | 4,5 | keine Aenderung; braucht weiter aktiven WP-Start (F85) |
| **B** Stab kWh | 3,35 | 3,42 | **3,35** | 3,30 | netto bleibt ~2,6 |
| Sonntag typisch, Reset | ~16:25 | ~17:05 | **~16:25** | ~15:55 | empfindlichste Groesse |
| Zaehleranzeige dann | ~11 | 12,7 | **11,0** | 9,7 | Anzeige = Laufzeit x 2,5 |

Alles Rechnung, Sicherheit [wahrscheinlich]. **Einsparung B gegen heute bleibt ~5 kWh_el/Woche.** Die Vorhersage aus F85 fuer den 08.11. bleibt stehen.

## Was bringt uns das

- **Fuer die Legionellen-Entscheidung:** Die Stabzahlen in F60 und F85 sind brauchbar, auch ohne eigenen Stromzaehler am Stab. B bleibt die einzige saubere Option; nichts beschlossen, das entscheidest du.
- **Fuer die Hauslast (F87):** Stab als Erklaerung scheidet aus. Die Suche nach dem Rest muss bei Haushalt, Sockel und Block weitergehen.
- **Fuer spaetere Auswertungen:** Zaehlerstaende Gruppe 2 `raw` geben 10-min-Energie, damit lassen sich Stufen anderer Geraete messen.

## Offen

- **Echte Stromaufnahme nie direkt gemessen.** Alle Aussagen sind indirekt. Eine Zangenmessung im Lauf oder Spannung plus Strom wuerde das Band von +/- 0,2 kW auf wenige Prozent druecken. Vorschlag, Entscheidung bei dir.
- **Netzspannung unbekannt,** kein Wert in Loxone. Damit ist 2,5 gegen 2,6 kW nicht trennbar.
- **Kanten:** Keine davon ist minutengenau gemessen; Kantenzeiten stammen aus Zaehlerstunden, bei 27.09. aus der Stufe selbst. PV nur stuendlich, Trend linear angenommen. Die 28.09.-Stufe 3,53 kW ist ungeklaert.
- **Alle sauberen Kanten aus Sept.** Am 01.11. nur grob bestaetigt. Der 08.11. ist die naechste Gelegenheit, dann mit `control_state` live die Sekundenkante.
- **Stab fehlt in** `[lokaler Pfad]` (nicht geaendert, nicht Teil dieses Auftrags). R119 und der Vermerk in R110 sollten auf diese Analyse zeigen.
- **Lageversatz:** Wo die Anlaufwaerme der ersten 15 min bleibt, nicht geklaert.

## Stichproben

1. **26.09. 12:30-12:50Z, Einspeisung:** Hauptstromzaehler `<UUID>`, Gruppe 2 raw, `totalNeg` 12:30Z 2667,3204, 12:40Z 2667,8076, 12:50Z 2668,6942, also 0,487 und 0,887 kWh je 10 min = 2,92 und 5,32 kW. Stab-Zaehler `<UUID>`, Gruppe 2 diff/hour, 26.09. 12Z = 1,7082 kWh = 41,0 min.
2. **29.09. 16:05 und 17:00 MESZ, Speicher:** Volllogger `/home/<user>/hoxpi_fulllog/2026-09-29.csv.gz`, Zeile 16:05:01: 1500 = 552, 27483 = 551, 1504 = 0; Zeile 17:00:01: 1500 = 600, 27483 = 597, 1504 = 0. Das sind +4,65 K in 55 min = 5,07 K/h. Stab-Zaehler 29.09. 14Z = 2,500003 kWh.
3. **Projektdatei:** `[lokaler Pfad]` Z. 16732: `<Co K="Ppwr" Def="2.5" ...>`, Z. 16727 `Type="MeterDig"`. Dazu Stab-Zaehler 23.09. 12Z = 2,8200 kWh (Quelle wie 1), 01.11. raw 12Z-11Z: 3346,99698 - 3344,49700 = 2,49998 kWh.