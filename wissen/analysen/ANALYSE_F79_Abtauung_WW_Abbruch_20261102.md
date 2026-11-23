# ANALYSE F79 - Abtauung beendet WW-Ladung (02.11.2026) - Stand 02.11.2026 08:05

Datum der Auswertung: 02.11.2026 08:05 (Daten bis 08:03:52). Nur lesend gerechnet. Ersteller: Claude (Subagent F79).

## Kernaussage

1. **Abtauungen in einer WW-Ladung sind selten:** seit 01.10.2026 **1 von 112 WW-Ladungen** (02.11. 06:24:41), seit 07.09. **2 von 148** (zusaetzlich 28.09. 04:39:31). [sicher, selbst gezaehlt, `ww_hires`-Marker `WW_Soll_eff` = 10,0; Querpruefung ueber `1539` = 51 direkt nach Status 4 und ueber `cc_abtau.py` (Status 8) liefert dieselben Faelle]
2. **Bei Kaelte steigt das Risiko:** Ladungen mit Aussen am Ladungsende < 3,5 C: 5 (davon 1 durch Abtauung beendet = 02.11.); < 6 C: 12 (1 Treffer). Zahlen klein. [sicher fuer die Zaehlung, Haeufigkeitsaussage nur wahrscheinlich]
3. **Warum nicht fortgesetzt:** Die Ladung wird nach der Abtauung nur fortgesetzt, wenn WW-Ist dann <= Soll - ca. 4,7 K liegt. 02.11.: Ist 48,8 vs Schwelle 45,3 -> kein Neustart (richtig im Sinne der Regel). 28.09.: Ist 41,9 vs Schwelle 47,3 -> Ladung lief **20 s nach Abtauende** weiter (WW_Status 1 um 04:45:02) und wurde ordentlich bis 52,0 fertig. [sicher fuer beide Faelle, Regel "Start bei Ist <= Soll - 4,7..4,9" ist durch 111 von 111 Starts seit 01.10. gestuetzt (nie ein Start bei Ist - Soll > -4,5); dass es *dieselbe* Regel ist, die nach der Abtauung greift, ist wahrscheinlich]
4. **Kosten 02.11.:** Die Ladung endete bei 48,7-48,8 statt ueblich 49,7 (ca. 1,0-1,3 K = ca. 0,5 kWh thermisch, ca. 0,15-0,2 kWh_el Nachladebedarf). Tiefster Ist-Wert seit der Abtauung 47,7 (08:02:52), noch ueber dem ueblichen Tiefstwert vor einer Ladung (45,1). Kein Komfort- oder Hygiene-Defizit gegenueber dem Normalbetrieb. [sicher fuer Zahlen; "kein Defizit" ist Bewertung gegen das Normalband 45,1-49,7, wahrscheinlich]
5. **"Ladung endete unter Soll" ist sonst nie die Abtauung:** Bei Soll 50 und 52 enden alle uebrigen 91 Ladungen bei Soll -0,4 bis +4,2 (Median -0,1/-0,2). Die 20 Ladungen mit Soll 57 (PV) enden 0,8-3,6 K unter 57 (Median -1,4) - das ist die PV-Ladung, die mit dem Ueberschuss abbricht, nicht Abtauung. 02.11. ist die einzige Ladung mit Soll 50/52, die > 0,5 K unter Soll endet. [sicher]

## Tabelle: Abtauungen in/an WW-Ladungen (Zeitraum 07.09.-02.11.)

| Datum / Abtau-Start | Aussen | WW-Ist am Abbruch | 1497 Soll | Ladesoll | Ist beim Ladungsstart | Abtau-Dauer | Was danach kam | naechste WW | WW-Ist-Tiefstwert bis dahin |
|---|---|---|---|---|---|---|---|---|---|
| 28.09. 04:39:31 | 9,6 | 41,9 (fiel danach weiter bis Min 36,0 um 04:57) | 52,0 | 56 | 45,9 | ca. 5,7 min (bis 04:45:12) | **Ladung lief ohne Heizpause weiter** (WW_Status 1 um 04:45:02, +20 s) | gleiche Ladung, fertig 05:49 bei Ist 52,0 | 36,0 (04:57) |
| 02.11. 06:24:41 | 3,1 | 48,8 (Rohwert 488, Ladung begann 05:40:22 bei 45,1) | 50,0 | 54 | 45,1 | 6,2 min (Marker bis 06:30:52) | Heizen ab 06:25:42 (UKA 1, Pumpe an), Verdichter-Stopp zwischen 06:30:52 und 06:33:52, Heizlauf 06:36-07:15; **keine WW** | Stand 08:03: **noch keine** | 47,7 (08:02:52), faellt ca. 0,5 K/h |

Alle uebrigen Abtau-Marker seit 07.09. lagen **ausserhalb** einer WW-Ladung (Heizlauf, WW_Status davor 0): 19.09. 21:11 (Einzelzeile), 13.10. 07:09 und 08:37, 26.10. 05:04, 27.10. 06:40, 02.11. 02:21 und 04:45. Energie je Abtau-Cluster (P_el integriert, inkl. Wiederanlauf): 0,18-0,33 kWh_el, 02.11. 06:24: 0,21 kWh_el. [sicher]

Keine andere Ladung wurde unterbrochen und nach < 15 min Pause fortgesetzt als 28.09. (Luecken-Suche: Ladungen seit 07.09. mit <= 15 min Luecke zusammengefasst: 149 Bloecke -> 148 Ladungen, also genau 1 Fortsetzung = 28.09.). [sicher]

## Vergleich: wie enden WW-Ladungen sonst (ab 01.10., 112 Ladungen, Datei `ww_hires.csv`)

| Soll (1497) | Ladungen | Ist_Ende - Soll (min / Median / max) | Bemerkung |
|---|---|---|---|
| 50 | 35 (+02.11.) | -0,4 / -0,1 / +4,2 | normales Ende bei Ist = Soll - 0,3 (49,6-49,9); +4,2 = Soll wurde waehrend der Ladung gesenkt |
| 52 | 56 | -0,3 / -0,2 / +2,2 | Ende bei 51,7-52,0 |
| 57 (PV, Ladesoll 61) | 20 | -3,6 / -1,4 / -0,8 | Ende bei 53,4-56,2, PV-Ende, nicht Abtauung |
| 50, 02.11. | 1 | **-1,3** (48,7) | Abtauung |

Pausen: Naechster Start bei Ist - Soll_neu: min -11,8, Median -4,9, **max -4,5** (n = 111; 53 Starts bei -4,8 bis -4,9, 7 bei -4,7). Ein Start bei Ist > Soll - 4,5 kam nie vor. Werte unter -5,3 stammen wahrscheinlich von Soll-Erhoehungen (Loxone/PV), nicht von Verzoegerung (nicht einzeln geprueft). Das bestaetigt F75 (Start bei 1497 - 5 K) mit Toleranz: Start bei Soll - 4,5..-5,0. [sicher fuer Zahlen, wahrscheinlich als Mechanismus]
`1497` im Volllogger gleich `WW_Soll` in `ww_hires` in 9289 von 9325 Minutenpunkten (Rest Zeitversatz). Rohwert 1497 = 500 am 02.11. 06:25:01 bis 07:35:01 (Volllogger), 1500 = 489/492/485/481 (06:25/06:30/06:35/06:50), 1539 = 51 um 06:25:01, 1477 = 31/32. [sicher]

## Ablauf 02.11. (Rohwerte, `ww_hires.csv`, x10)

| Zeit | WW_Ist | Status | Bemerkung |
|---|---|---|---|
| 05:40:42 | 45,1 | WW_Status 1 | Start, Soll 50, Ladesoll 54, Aussen 3,0 |
| 05:50:23 | 42,8 | 1 | Ist-Minimum der Ladung (Ursache nicht untersucht), wieder > 45,3 um 06:05:22 |
| 06:24:21 | 48,7 | letzte Zeile mit WW_Status 1 (06:24:11: P_el 268, Mod 38 %) | |
| 06:24:41 | 48,8 | WW_Status 0, WW_Soll_eff 10,0, P_el 0 | Abtaubeginn (Marker; Volllogger 06:25:01: 1539 = 51, P_el 0) |
| 06:25:42 | 48,9 | UKA 1 (Heizen), P_el 41 | kurzer Heizlauf mit Anlauframpe bis 06:30 (P_el 388, Mod 65 %) |
| 06:33:52 | 48,8 | P_el 0 | Stillstand |
| 06:36:51-07:15 | 48,5 -> 48,0 | Heizlauf Mod 35 %, P_el 130-183 | WW kuehlt ab, kein WW-Start |
| 07:25 | 48,1 | | |
| 08:02:52 | 47,7 | | Min bisher, Soll 50 |

Ladung selbst: 44 min, 2,92 kWh_el, WW_Ist +3,7 K (45,1 -> 48,8). Das ist deutlich mehr als eine uebliche Ladung 45,1 -> 49,7 (Median 1,64 kWh_el, 34 min, n = 25): Kaeltephase (Aussen 3 C) und Ladesoll 54. [sicher fuer Zahlen]

## Was bringt uns das

- Die Abtauung wirkt als **Unterbrechung ohne Gedaechtnis**: Die Ladung wird nur wiederaufgenommen, wenn WW-Ist <= Soll - 4,7. Das ist beim Ladungsstart (Ist faellt in den ersten Minuten unter den Startwert: 02.11. 45,1 -> 42,8 und ueber 25 min unter 45,3; 28.09. 45,9 -> 36,0) fast immer der Fall, spaeter nicht mehr. [wahrscheinlich]
- Das Risiko eines "nicht fertigen" WW ist klein (1/112) und selbst dann liegt WW bei ca. 48-49 C, nur ca. 1 K unter dem Normalende. Kein Eingriff noetig. Tipp bei Bedarf: Vor einem kaelteren Morgen mit Abtauung die Ladung nicht in den Abtau-Tagesgang legen (8 von 9 Abtauungen seit 07.09. lagen zwischen 02:21 und 08:42, Aussen 2,2-9,6 C, 7 davon <= 5,2 C). [Vermutung, 9 Faelle]
- Einsparbar ist nichts Nennenswertes: Abtau-Zusatzverbrauch 0,2-0,3 kWh_el je Abtauung. Fuer den Zwilling: Abtauung in Ladung = Dauer ca. 6 min, Ladungsende vorgezogen, Folge-WW erst bei Ist <= Soll - 4,7.

## Vorhersagen (vor dem Ereignis, ueberpruefbar, ww_hires 1-min-Raster)

**F79-V1 (nach naechster Abtauung in einer WW-Ladung):** WW_Status geht binnen <= 30 s auf 0 und `WW_Soll_eff` auf 10,0. Die Ladung wird **genau dann in <= 2 min nach Marker-Ende fortgesetzt (WW_Status 1)**, wenn WW_Ist zum Marker-Ende <= Soll - 4,7 (Toleranz +-0,3) liegt; sonst **kein WW-Start** bis WW_Ist <= Soll - 4,5..-5,0 (bei Soll 50 also <= 45,3). Praktisch: Abtauung in den ersten ca. 25 min einer Ladung ab Ist 45,1 -> Fortsetzung; danach -> Abbruch ohne Fortsetzung. **Widerlegt**, wenn bei Ist > Soll - 4,3 die Ladung nach der Abtauung wieder anlaeuft, oder bei Ist <= Soll - 5,0 nach 5 min keine WW kommt (ohne anderen Grund wie Sperrzeit).

## Offen

- Querpruefung erledigt: `cc_abtau.py --ab 2026-10-01` (Status 8 aus `verdichter_catch`, Ausgabe auf dem Pi `/tmp/f79_abtau.out`) findet **7 Abtau-Runs seit 01.10.** (13.10. 07:10 und 08:38, 26.10. 05:05, 27.10. 06:41, 02.11. 02:22, 04:47, 06:25) = exakt die 7 Marker-Cluster; in einer WW-Ladung nur 02.11. 06:25 (Abtau-Run <MAC>, Luefter aus seit 06:24:22). [sicher]
- Laufzeit bis zur Abtauung (cc_abtau, kumuliert seit letzter Abtauung): 151, 75, 164, 99, 87, 90 und **86,5 min** (02.11. 06:24; Lauf <MAC> inkl. WW-Ladung). Streuung 75-164 min: ob eine Abtauung in eine Ladung faellt, haengt an der Gesamtlaufzeit, nicht an der Ladung. Nach Abtauende 06:31:11 sind bis 08:03 ca. 45 min Laufzeit kumuliert (V134 erwartet 60-120 min). [sicher fuer Zahlen]
- `1539` = 51 tritt auch ohne Abtauung auf (18 Zeilen seit 01.10., meist nach Heizstopp, P_el 0); nur "Status 4 -> 51" ist abtaukennzeichnend (2 Faelle). Bedeutung von 51 nicht geklaert.
- Ob die Fortsetzung der Ladung (28.09.) die normale Anlauffreigabe oder eine Sonderlogik ist, unbekannt; nur ein Fall.
- Hygiene: Eine Legionellenfunktion/Mindesttemperatur der Hoval wurde hier nicht geprueft.
- V134 (Verhaltenskarte): Naechste Abtauung 60-120 min Laufzeit nach 06:31:11; bis 08:03 noch keine neue (Lauf 06:36-07:15 = 39 min + ca. 3 min), also bisher weder bestaetigt noch widerlegt.

## Vorgehen und Dateien

- Daten: `~/hoxpi_fulllog/ww_hires.csv` (72 221 Zeilen ab 01.10., keine Luecken > 10 min), `~/hoxpi_fulllog/2026-11-02.csv`, Volllogger 2026-10/11 fuer 1497/1539.
- Ladung = zusammenhaengende Zeilen `WW_Status` = 1 (Luecke <= 150 s; fuer die Fortsetzungssuche <= 15 min). Abtauung = `WW_Soll_eff` = 10,0 (Cluster, Luecke <= 150 s). Nur Lesen auf dem Pi.
- Skripte (alle lesend): `[lokaler Pfad]` (Ausgabe `f79_cases.out`), `f79_stats.py` (`f79_stats.out`), `f79_rate.py`, `f79_kwh.py`, `f79_status51.py`, `f79_fulllog_check.py`, `f79_explore.py`; auf dem Pi unter `/tmp/f79_*.py`.
- Vorlauf: `[lokaler Pfad]`, `ANALYSE_F75_SF2_Tiefstand_20261102.md`, `WP_Verhaltenskarte.md` (V1, V25, V130, V134).