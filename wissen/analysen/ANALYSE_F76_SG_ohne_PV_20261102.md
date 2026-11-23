# ANALYSE F76 - Smart-Grid-Phasen ohne PV bis 23.10.2026 (02.11.2026)
Claude, Subagent, nur lesend. An Anlage, Loxone und Pi nichts geändert. Ergänzt und korrigiert `[lokaler Pfad]`.

## Ergebnis
1. **27545 hängt allein am Energiemanager-Ausgang OL6 („Wärmepumpe"), ohne eigene PV-, SOC- oder Sonnen-Bedingung.** Haltezeit 45 min (MinRt 2.700 s), Schaltleistung 1,5 kW (bis 08.10. 2,6). Kein Monoflop. [sicher für die Datei]
2. **Die 7 Ladungen fast ohne PV haben verschiedene Gründe:** 3 Starts bei echtem Überschuss, danach trug nur noch das Halten (08.10., 15.10., 23.10.); 1 Rechenartefakt von F74 (18.10., Einspeisung lief); 3 Einschaltungen ohne erkennbaren Überschuss (14.10., 19.10. zweimal). [sicher für Flanken und Messwerte]
3. **Warum OL6 bei den dunklen Flanken einschaltet, ist nicht geklärt.** Die Statistik hat nur 10-/30-min-Werte, Spwr ist nicht aufgezeichnet. Zwei Muster, Erklärungen nur [Vermutung].
4. **Das Ende am 23.10. kommt nicht vom Deckel (Korrektur F74), sondern sehr wahrscheinlich vom Umbau 24.10. 18:27.** Seit 26.10. gibt es 27545 = 1 bei 1497 = 50,0. Der Deckel gäbe mindestens 52,0. Der Eingang I2 von „WW-Soll Manager" sieht also 0. [sicher: Messung; wahrscheinlich: Ursache Umverdrahtung]
5. **Der Spwr-Fix vom 18.10. hat dunkle Flanken nicht beseitigt** (19., 22., 23.10.), und 20.10. hielt SG noch bis 19:12. [sicher]

## Belege
### Logik (`[lokaler Pfad]`, Zeilen)
- Aktor 27545 Z. 3434 (Wiederholung 300 s) ← Verweis Z. 8449, AI ← OL6. Der in der Notiz genannte Hand-Schieber ist nicht verdrahtet. OL6 geht auch auf Merker „Smart Grid Auslösen" Z. 8380 und Anzeige „Berechneter SG Ready" Z. 8372.
- [Energiemanager](https://www.loxone.com/dede/kb/) Z. 8078: Gpwr = Victron Grid, Ppwr = PV-Total, Spwr = Formel O64266, Soc = Victron, MinSoc = SOC_Freigabe (heute 95), IL1 Wallbox, IL3 Heizkörper, IL6 = 25611 (seit 08.10.). Last WP Z. 8135: Priorität 0 vor Wallbox, MinRt 2.700 s, SwPwr 1,5, MaxPwr 6,9, RT 300 s. Reset nur aus Wallbox-Logik (Z. 8276). Das interne Rechenverfahren ist nicht einsehbar (Hilfeseite nicht abrufbar).
- O64266 Z. 8308: `IF(I3==1;MIN(I1;0);IF(I2<I4;I1;IF(I1<0;0;I1)))`, I1 = Reg 842, I2 SOC, I3 Abend (ab 180 min vor Sonnenuntergang), I4 SOC_Freigabe. Vorzeichen 842: negativ = Entladung (Zähler LiFePO4 mit InvPf zeigt nachts positiv). Tagsüber ab SOC_Freigabe wird Entladung auf 0 gesetzt: der EM sieht den Akku nicht. Die Notiz Z. 8336 spricht von „negativer Ladeleistung", das passt nicht zum Vorzeichen. [sicher]
- Formel: bis `UMBAU_stand_20261018_1740...` `IF(I3==1;0;...)`, ab `..._1748...` neu. SwPwr 2,6 → 1,5 zwischen `UMBAU_stand_20261008_2015...` und `..._2110...`.

### Flanken (Loxone-Statistik „Berechneter SG Ready", UTC + 2 = lokal)
Grid + = Bezug, Akku + = Entladung (Rohwerte 10/30 min nahe der Flanke), PV = kWh der Stunde aus `[lokaler Pfad]`, SOC = Stundenwert, Register aus Volllogger `~/hoxpi_fulllog/JJJJ-MM-TT.csv[.gz]`.
| F74-Ladung | SG ein - aus (lokal) | Dauer | PV Std. | SOC | Grid / Akku kW | 1539; 25611 kW; 1497 | Einstufung |
|---|---|---|---|---|---|---|---|
| 08.10. 12:40 | 12:36:41 - 14:02:29 | 86 min | 4,21 → 1,17 | 80 → 98 | -2,67 / - | 4; 2,95; 570 | Echte Einspeisung beim Start, Ladung danach unter Wolke [sicher] |
| 14.10. 06:20 | 06:23:41 - 07:08:51 | 45,2 min | 0,00 | 42 → 30 | -0,01 / +1,17 | 4; 4,93 → 3,60; 520 → 570 | **Dunkel**, Muster a, Ladung lief schon, Halten = MinRt [sicher] |
| 15.10. 18:25 | 13:37:20 - 19:01:24 | 324 min | 4,14 beim Start, 0,03 um 18:25 | 96-95 | +3,4 bis +5,0 / - | 4; 4,14; 570 | Start echt, abends gehalten durch Spwr = 0 (vor Fix 18.10.) [sicher] |
| 18.10. 15:45 | 12:49:09 - 15:58:45 | 190 min | 2,58 | 100 | -2,85, -0,40 / - | 4; 3,06; 570 | **Artefakt F74**: Einspeisung 2,75 kWh/h, um 15:45 lag Überschuss an [sicher] |
| 19.10. 17:30 | 17:05:31 - 18:24:16 | 79 min | 0,48 | 97 | +0,25 / +6,04 | 4; 0,60 → 4,52; 570 | **Dunkel**, Muster b, 3 min nach vorigem SG-Ende [sicher] |
| 19.10. 19:15 | 18:56:26 - 19:41:33 | 45,1 min | 0,01 | 96-95 | +0,60 → +0,05 / 0 → +0,59 | 4; 3,09; 570 | **Dunkel**, Muster b, Halten = MinRt [sicher] |
| 23.10. 16:05 | 16:03:50 - 16:49:27 | 45,6 min | 1,35 | 86 → 97 | -0,98 / -2,28 | 4; 1,26; 570 | Start echt; Wallbox ab ~16:15, Netzbezug 8-9 kW [sicher] |

Weitere dunkle Flanken ohne Ladung: 16.10. 06:10:44 (SOC 59-50, Grid +0,34, Akku +3,14, 1539 = 4, 25611 = 4,08, 1497 blieb 52, AT 6,3 °C), 22.10. 18:11:47 (Grid +2,95, Akku 0, SOC 96, 25611 = 0), 23.10. 18:05:45 und 19:06:27 (Wallbox 5,7 kW, Grid +6,5/+7,3, Akku 0, SOC 97-93). Wallbox-Energie 14.10. und 16.10. morgens 0, 19.10. ab 16 UTC 0. [sicher]
**Korrektur F74:** Der am 23.10. abends unzugeordnete Bezug von 7-8 kWh/h ist zum größten Teil die Wallbox (5,65 kWh je Stunde). [sicher]

### Muster der dunklen Flanken
- **a) Morgens bei WW-Start (14.10., 16.10.):** Flanke binnen Minuten nach Start, 25611 auf 4-5 kW, SOC unter 95, also Spwr = echte Entladung. Akku 16.10. rund 3,1 kW (zweimal gemessen). Mögliche Erklärung: Der EM rechnet IL6 als verfügbar, und kurz übersteigt 25611 die Summe aus Akku und Netz. 14.10. mit angenommenen 3,1 kW Akku: 4,93 - 3,1 ≈ 1,8 kW ≥ 1,5. Die Stunde 19.10. 04 UTC (Akku 2,74 kWh) gab keine Flanke. [Vermutung]
- **b) Abends bei SOC ≥ 93, Akku oft 0, WP aus (19., 22., 23.10.):** Netzbezug fällt kurz vorher oder Akku setzt wieder ein. Rechnerisch ist -Grid + Spwr negativ. Ursache offen; [Vermutung] Lastsprung oder Vorzeichen im Abendzweig. Akku-Stillstand trotz SOC 96 ebenfalls ungeklärt.
- 45-min-Phasen entstehen durch MinRt: ein kurzer Impuls hält 27545 und damit 1497 = 57 für 45 min. [sicher]

### Warum 57 nach 23.10. nicht mehr kommt
| Zeitraum | Zeilen mit 27545 = 1 | Werte 1497 |
|---|---|---|
| 01.-23.10. | 1.067 | 570: 1.045; 520: 22 (Deckel) |
| 26.10. / 31.10. | 27 / 22 | 500: alle |
| 29.10. | 15 | 500: 5; 520: 9; 570: 1 (Kick und Nachlade-Boost ab 12:23, kein SG) |

- Formeln `MAX(MAX(MIN(Manager;52+5*Deckel);Boost*52);Kick*57)` und `IF(I2>0;57;...)`: Mit I2 = 1 wäre 1497 ≥ 52, gemessen 50. [sicher] 24./25.10. keine SG-Flanke, die erste danach ist 26.10. 12:54.
- **Umbau:** `[lokaler Pfad]`, Abschnitt 24.10. 18:27: I2 von Verweis.Q (dessen AI = Merker.AQ, `UMBAU_stand_20261024_1813.Loxone`) auf **Merker.Q** direkt (`UMBAU_stand_20261025_1340.Loxone` Z. 16382). Merker Tp=0, Eingang OL6. Gleich umgehängt: Klimacontroller HC1/HC2 Cool-/HeatAvailable. WW Status I3 hängt an Merker.AQ. [wahrscheinlich]
- **Umbau 23.10. war es nicht:** Flanke 23.10. 19:06 gab noch 570; 19:03/19:29 änderten nur Kalender und Deckel-Freigabe. [sicher] Welchen Stand der Miniserver seit wann fährt, ist nicht direkt gelesen.

## Offen
1. Muster a und b klären: Gpwr, Spwr, Ppwr, loads feiner über eine SG-Flanke mitschreiben.
2. Merker.Q im Liveview zur nächsten SG-Phase ablesen. Das klärt Punkt 4 endgültig.
3. Vorzeichen von Spwr im Baustein: 23.10. 16:03 (Einspeisung + Ladung → Ein) passt zu „+ = Ladung", Doku nicht eingesehen.

## Was bringt uns das
| Punkt | Wirkung | Einstufung |
|---|---|---|
| PV-57 seit 24.10. tot, nicht nur gedeckelt | F74-Wert für sonnige Tage **3,5-5 kWh_el/Woche** entfällt, bis repariert. Im November klein | [Vermutung] |
| Sperre gegen dunkle Flanken | **Höchstens 2,6, eher 1-2 kWh_el/Woche** (F74), derzeit 0, weil SG 1497 nicht hebt | [Vermutung] |

Vorschlag, nichts umgesetzt, der Betreiber entscheidet (Backup und Skill `loxone-xml-umbau` zuerst): I2 und Klimacontroller zurück auf Merker.AQ (Rückweg Merker.Q), danach über PV-Sperre per UND mit „Ppwr ≥ 1,5 kW" entscheiden ([Schwellwertschalter](https://www.loxone.com/dede/kb/schwellwertschalter/)).
Skripte: `[lokaler Pfad]` bis `f76_g.py`, `f76_lib.py`.