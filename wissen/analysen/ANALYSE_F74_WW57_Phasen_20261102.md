# ANALYSE F74 - WW-Soll 1497 ab 55 °C: Phasen, Auslöser, PV-Anteil, Kosten (02.11.2026)

Erstellt 02.11.2026 ~05:30 (Claude, Subagent Orchestrator, nur lesend). An Anlage, Bussen, Loxone und Pi nichts geändert.

**Kernergebnis**
1. 01.10.-02.11. (04:55): **68 Phasen** mit 1497 = 57,0 (kein anderer Wert ab 55): **33 Smart-Grid-Phasen** (87,4 h, nur 01.-23.10.) und **35 Kicks** (je 5-16 min). Seit 24.10. **nur noch Kicks**. [sicher]
3. **PV:** Smart-Grid-Ladungen 51 % PV / 26 % Akku / 23 % Netz, **7 von 28 fast ohne PV** (12,7 kWh_el, davon ~8,6 Netz, u. a. 14.10. 06:20 vor Sonnenaufgang). Kick-Ladungen 66 % Netz. [wahrscheinlich, Stundenraster]
4. **Erreicht:** SG im Mittel 55,5 °C (bei Ende ≥ 54 °C: 56,2 °C), höchstens 57,0 °C; Kick 52,6 °C; Normal 51,5 °C. **AZ nach Außentemperatur bereinigt: kein messbarer Unterschied** (SG 3,42 / Kick 3,07 / Normal 3,00; Soll-Strom nach Regression 50,7 / 83,6 / 89,5 gegen Ist 50,8 / 83,9 / 90,8 kWh_el). [wahrscheinlich]
5. **Bringt:** SG-57 an sonnigen Tagen rund **3,5-5 kWh_el/Woche** weniger Netzbezug (01.-23.10.) [Vermutung], seit 24.10. **0**. Kick **bringt 0 kWh, kostet ≤ 0,5 kWh_el/Woche**, ist Komfort [wahrscheinlich]. Sperre „SG nur mit echter PV": höchstens **2,6 kWh_el/Woche** [Vermutung].

## Frage
F74: Wie oft stand 1497 seit 01.10. auf ≥ 55 °C (Beginn, Dauer)? Was löst das aus (SG/PV, Kick, Legionellen, sonst)? Wurde echter PV-Überschuss genutzt? Welche Temperatur wird erreicht, was kostet es gegenüber 50-52 °C?

## Datenquelle (nur gelesen)
- Volllogger: `[lokaler Pfad]` ... `2026-11-01.csv`, 02.11. frisch vom Pi als `f74_2026-11-02.csv` (Original `~/hoxpi_fulllog/2026-11-02.csv`), 9.288 Zeilen, 5 min, 25.10. mit 300 Zeilen. Register 1497, 1499, 1500, 27483, 1521, 1525, 1477, 1539, 1504, 25611, 27489, 25614, 27545.
- 30-s-Log für Flanken: `~/hoxpi_fulllog/ww_hires.csv` (Kopie `...\vorhernachher_20261024\f74_ww.csv`, 71.806 Zeilen, keine Lücke > 10 min). Spalte WW_Soll = 1497 (9.229 von 9.287 Vergleichszeilen gleich).
- 1-min-P_el je WW-Ladung: `[lokaler Pfad]`.
- Stundenwerte Loxone (`control_statistics` diff/hour, Gruppe 2, nur gelesen): Hauptstromzähler `<UUID>`, Batterie `<UUID>` (total = Entladung, totalNeg = Ladung; aus dem Tagesgang abgeleitet [wahrscheinlich]), 5 PV-Zähler wie in `[lokaler Pfad]`. Ablage: `...\vorhernachher_20261024\f74_lox_hour.txt` (alle Stunden, PV nachts 0). Heizstab `<UUID>` für 01.10.
- Logik: `[lokaler Pfad] Config\Projects\Fam der Betreiber UMBAU.Loxone` (Stand 01.11.2026 23:36, 1.748.685 Byte). Die drei Kernformeln sind identisch in `...UMBAU.Loxone.backup` (25.10.). Ob der Miniserver genau diesen Stand fährt: nicht geprüft.
- Vorarbeit: `ANALYSE_F68_WW_Ladungs_AZ_20261102.md`, `ARGON_WW_Ladesoll_Kosten_Okt2026.md` (MD-10), `R120_Flanken_PV_vs_Kick_20260927_1320.md`, `ANALYSE_WWSoll1499_nach_57Ladung_20261025.md` (alle in `[lokaler Pfad]`), `[lokaler Pfad]`.
- Skripte: `[lokaler Pfad]` (`f74_lib.py`, `f74_phasen.py`, `f74_ausw.py`, `f74_final.py`).

## Methode
- **Phase** = 1497 ≥ 55,0 in der Vereinigung aus 5-min- und 30-s-Reihe. Kurze Zacken (≤ 2 min, dann < 6 min Pause) sind mit der Folgephase zusammengefasst (vier Fälle). Die reine 5-min-Zählung gibt ebenfalls 68.
- **Klasse SG** = 27545 = 1 in der Phase und länger als 16 min. **Klasse Kick** = höchstens 16 min (Nr 62 lief parallel zu SG mit Deckel 52, zählt als Kick).
- **Ladung** wie F68 (1539 = 4, Lücke > 10 min trennt); einer Phase zugeordnet bei Überlappung, Kick bis 8 min danach. Die ganze Ladung zählt zur Phase, also auch der Teil nach Ende von 57 °C. Q = Differenz 27489, E_el = 1-min-Integral 25611. 18.10. 10:35 (Zählersprung) und 01.11. 13:05 sind wie in F68 aus den Klassensummen ausgeschlossen. Summe 109 Ladungen, 704 kWh_th, 225,5 kWh_el; F68: 704 und 227,3. [sicher]
- **Herkunft des Stroms** je Stunde anteilig: Netz : Akku-Entladung : PV direkt (PV - Einspeisung - Akkuladung). Das ist Stundenraster, keine Messung am Verdichter; Akku enthält früher geladene PV, Herkunft der Akkuladung nicht geprüft. Grenzen: Netz höchstens min(Bezug, E_WP), PV mindestens E_WP - Bezug - Entladung.
- **AZ-Bereinigung:** Regression über die 48 Normalladungen (Q ≥ 3): AZ = 2,427 + 0,0697 × AT, Streuung 0,28. Soll-Strom = Q / AZ(AT).
- **Zeit:** Log lokal, Loxone UTC. Umrechnung MESZ bis 25.10. 03:00, danach MEZ, Rücksprung erkannt. In der doppelten Stunde 25.10. liegt keine Phase. [sicher]

## Ergebnis

### 1. Logik laut Projektdatei [sicher für die Datei]
| Baustein | Zeile | Inhalt |
|---|---|---|
| Aktor „Normal-Temperatur Warmwasser" | 3311 | schreibt 1497, Wiederholung 300 s |
| Formel „WW-Soll final" | 16432 | `MAX(MAX(MIN(I1;52+5*I4);I2*52);I3*57)`, I1 Manager, I2 Boost, I3 Kick, I4 Deckel frei |
| Formel „WW-Soll Manager" | 16287 | `IF(I2>0;57;IF(I3>0;54;IF(I4>0;45;I1)))`, I2 = Smart Grid |
| ODER „WW-Deckel 57 frei" | 16802 | Außen über 9 °C (aus unter 7) ODER PV-Prognose ab 20 kWh (seit 23.10.) |
| Energiemanager, Ausgang OL6 Last „Wärmepumpe" | 7946, 7992, 8003 | Mindestlaufzeit 2.700 s, Schaltleistung 1,5 kW. Führt auf Merker Zeile 8248 und Aktor 27545 Zeile 3290 |
| Monoflop „WW Kick-Start" | 16387 | 600 s, I3 = 57 |
| UND „WW Kick nur im Freigabefenster" + Schaltuhr | 16396, 16405 | 05:00-22:00, seit 08.10. |
| Monoflop „WW Nachlade-Boost" | 16378 | 5.400 s, Soll 52, Auslöser unten |
| Schwellwertschalter SF2 40/35/30 | 16303 ff. | Flanke beim Unterschreiten; Stufe 45 seit 27.09. entfernt |
| UND „Abendfenster 17-22" + Schwelle 1500 | 16849, 16837 | 1500 unter 48 °C im Fenster, seit 25.10. (vorher 17:00-17:01) |
| Legionellen | 16859-16999 | wirkt nur auf Heizstab-Ziel 62/59, **kein Pfad zu 1497** |

Bei Kick-Soll 57 wäre die Ladung bis oben 57 möglich, durch den Abfall auf 52 nach 5-10 min endet sie bei ~52,6 °C. Der Kick ist im Log nur 1-2 Schreibzyklen lang (Schreibraster 300 s, vgl. R120). [sicher]

Auslöser der 68 Phasen:
| Auslöser | Anzahl | Beleg |
|---|---|---|
| Smart Grid (Energiemanager OL6) | 33 | 27545 = 1 während 1497 = 570, alle bis 23.10. [sicher] |
| Kick: Zapfung (SF2-Flanke) | 17 | Abfall 2,2-12 K in 15 min [wahrscheinlich] |
| Kick: Drift/Kleinzapfung ohne echte Zapfung | 6 | Nr 3, 6, 14, 16, 38, 68 (-0,4 bis -1,6 K) [wahrscheinlich] |
| Kick: SF2 fällt bei laufender Ladung durch 40 | 5 | Nr 12, 21, 55, 57, 59 [wahrscheinlich] |
| Legionellen, Party, Erhöhter Wärmebedarf | 0 | Pfad fehlt bzw. 54 °C nie im Log [sicher] |

- 3 der 35 Kicks ohne Ladung (Nr 1, 3, 38: oben über 52 °C). Bei 27 startet die Ladung mit dem Kick, bei 5 lief sie schon. [sicher]
- Vor 08.10. zwei Kicks nach 22 Uhr (Nr 5 und 14), seit dem Freigabefenster keiner mehr. [sicher]
- **8 von 33 SG-Phasen ohne WP-Ladung** (11,6 von 87,4 h): Speicher war schon über 52 °C, also nichts abgenommen. [sicher]
- Seit 24.10.: SG = 1 weiter (26.10., 29.10., 31.10.), aber 1497 nur 50-52 (Deckel) und keine Ladung ausgelöst. Einspeisung an diesen Tagen 2,0 / 1,2 / 1,6 kWh, also kaum etwas verschenkt. [sicher]

### 2. Alle Phasen
Quelle je Zeile: Volllogger des Datums, E_el aus `ww_abnahme.csv`, Netz/Akku/PV aus `f74_lox_hour.txt`. **AT** °C, **Q** kWh_th, **E** kWh_el, **N/A/PV** = Stromherkunft % der zugeordneten Ladung. „1500 Start" = vor der ersten zugeordneten Ladung. „1500 max" = Ladungsende (WP), nicht Stab.

| Nr | Beginn | Ende | min | Auslöser | 1500 Start | 1500 max | AT | Lad. | Q | E | AZ | N/A/PV |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 | 01.10. 11:38 | 18:27 | 409 | Energiemanager OL6 (27545=1) | 52,3 | 56,1 | 15,8 | 1 | 4 | 0,91 | 4,38 | 0/2/97 |
| 4 | 02.10. 16:35 | 17:20 | 45 | Energiemanager OL6 (27545=1) | 46,7 | 52,1 | 19,5 | 1 | 9 | 2,27 | 3,97 | 3/30/66 |
| 7 | 03.10. 12:17 | 17:42 | 325 | Energiemanager OL6 (27545=1) | 51,3 | 56,3 | 15,6 | 1 | 6 | 1,50 | 3,99 | 3/12/86 |
| 8 | 04.10. 12:05 | 17:03 | 298 | Energiemanager OL6 (27545=1) | 49,3 | 57,0 | 16,0 | 2 | 20 | 5,53 | 3,62 | 1/44/55 |
| 10 | 05.10. 14:02 | 17:51 | 229 | Energiemanager OL6 (27545=1) | 52,1 | 56,5 | 18,5 | 1 | 6 | 1,46 | 4,10 | 1/13/86 |
| 12 | 06.10. 06:14 | 06:24 | 10 | Ladung selbst (SF2<40, -1,7 K) | 46,9 | 52,1 | 9,5 | 1 | 7 | 2,20 | 3,18 | 100/0/0 |
| 13 | 06.10. 11:45 | 17:47 | 363 | Energiemanager OL6 (27545=1) | 48,0 | 56,3 | 13,6 | 1 | 6 | 1,80 | 3,34 | 4/13/83 |
| 15 | 07.10. 12:31 | 18:03 | 332 | Energiemanager OL6 (27545=1) | 45,2 | 56,9 | 15,2 | 2 | 12 | 3,39 | 3,54 | 3/29/68 |
| 18 | 08.10. 12:36 | 14:02 | 86 | Energiemanager OL6 (27545=1) | 51,7 | 56,3 | 16,7 | 1 | 4 | 1,22 | 3,28 | 12/82/6 |
| 20 | 09.10. 15:56 | 18:34 | 158 | Energiemanager OL6 (27545=1) | 45,9 | 56,6 | 13,3 | 1 | 9 | 2,53 | 3,56 | 2/18/80 |
| 21 | 10.10. 11:56 | 12:01 | 5 | Ladung selbst (SF2<40, -1,9 K) | 45,7 | 52,8 | 10,2 | 1 | 8 | 2,47 | 3,24 | 71/17/12 |
| 23 | 12.10. 12:09 | 17:17 | 308 | Energiemanager OL6 (27545=1) | 48,7 | 56,5 | 11,3 | 1 | 7 | 2,12 | 3,30 | 4/23/74 |
| 25 | 13.10. 12:08 | 16:09 | 242 | Energiemanager OL6 (27545=1) | 48,1 | 56,6 | 8,8 | 1 | 7 | 2,22 | 3,15 | 0/2/98 |
| 27 | 14.10. 06:23 | 07:08 | 45 | Energiemanager OL6 (27545=1) | 47,6 | 54,5 | 9,7 | 1 | 8 | 2,32 | 3,44 | 61/39/0 |
| 29 | 15.10. 13:37 | 19:08 | 331 | Energiemanager OL6 (27545=1) | 46,9 | 56,3 | 13,9 | 2 | 16 | 4,78 | 3,35 | 49/12/39 |
| 31 | 16.10. 11:57 | 13:06 | 70 | Energiemanager OL6 (27545=1) | 50,1 | 56,6 | 10,5 | 1 | 7 | 1,97 | 3,55 | 2/14/84 |
| 32 | 16.10. 13:18 | 18:43 | 325 | Energiemanager OL6 (27545=1) | 52,3 | 56,2 | 13,0 | 1 | 4 | 1,13 | 3,55 | 12/24/63 |
| 33 | 17.10. 14:03 | 14:50 | 47 | Energiemanager OL6 (27545=1) | 48,4 | 56,3 | 15,4 | 1 | 6 | 1,92 | 3,13 | 3/45/53 |
| 34 | 17.10. 15:45 | 18:42 | 177 | Energiemanager OL6 (27545=1) | 56,5 | - (keine Ladung) | 16,1 | 0 | 0 | 0,00 | - | -/-/- |
| 36 | 18.10. 12:49 | 15:58 | 189 | Energiemanager OL6 (27545=1) | 52,4 | 54,1 | 13,5 | 1 | 2 | 0,62 | 3,21 | 7/93/0 |
| 37 | 18.10. 16:04 | 19:05 | 181 | Energiemanager OL6 (27545=1) | 52,5 | 56,6 | 16,5 | 1 | 6 | 1,71 | 3,51 | 68/22/11 |
| 39 | 19.10. 13:57 | 14:44 | 46 | Energiemanager OL6 (27545=1) | 50,0 | 56,3 | 14,0 | 1 | 7 | 1,98 | 3,53 | 2/31/67 |
| 40 | 19.10. 15:15 | 16:00 | 45 | Energiemanager OL6 (27545=1) | 56,2 | - (keine Ladung) | 15,5 | 0 | 0 | 0,00 | - | -/-/- |
| 41 | 19.10. 16:17 | 17:02 | 45 | Energiemanager OL6 (27545=1) | 52,4 | 53,2 | 15,7 | 1 | 1 | 0,41 | 2,46 | 63/20/18 |
| 42 | 19.10. 17:05 | 18:24 | 78 | Energiemanager OL6 (27545=1) | 52,7 | 52,8 | 15,2 | 1 | 9 | 2,67 | 3,37 | 87/11/2 |
| 43 | 19.10. 18:56 | 19:41 | 45 | Energiemanager OL6 (27545=1) | 52,1 | 54,5 | 11,8 | 1 | 4 | 1,37 | 2,93 | 77/23/0 |
| 44 | 20.10. 11:38 | 15:57 | 259 | Energiemanager OL6 (27545=1) | 50,8 | 56,8 | 10,2 | 1 | 5 | 1,71 | 2,92 | 51/2/47 |
| 45 | 20.10. 16:14 | 19:12 | 178 | Energiemanager OL6 (27545=1) | 56,8 | - (keine Ladung) | 11,3 | 0 | 0 | 0,00 | - | -/-/- |
| 48 | 22.10. 13:14 | 14:00 | 46 | Energiemanager OL6 (27545=1) | 52,1 | 56,9 | 10,6 | 1 | 5 | 1,60 | 3,12 | 2/63/35 |
| 49 | 22.10. 14:39 | 16:51 | 132 | Energiemanager OL6 (27545=1) | 56,8 | - (keine Ladung) | 10,6 | 0 | 0 | 0,00 | - | -/-/- |
| 50 | 22.10. 17:00 | 17:46 | 46 | Energiemanager OL6 (27545=1) | 55,1 | - (keine Ladung) | 11,2 | 0 | 0 | 0,00 | - | -/-/- |
| 51 | 22.10. 18:11 | 18:39 | 27 | Energiemanager OL6 (27545=1) | 53,0 | - (keine Ladung) | 7,9 | 0 | 0 | 0,00 | - | -/-/- |
| 52 | 23.10. 16:03 | 16:49 | 46 | Energiemanager OL6 (27545=1) | 51,3 | 56,8 | 10,4 | 1 | 4 | 1,66 | 2,41 | 81/11/7 |
| 53 | 23.10. 18:05 | 18:51 | 46 | Energiemanager OL6 (27545=1) | 56,5 | - (keine Ladung) | 9,1 | 0 | 0 | 0,00 | - | -/-/- |
| 54 | 23.10. 19:06 | 19:51 | 45 | Energiemanager OL6 (27545=1) | 54,8 | - (keine Ladung) | 8,4 | 0 | 0 | 0,00 | - | -/-/- |
| 55 | 25.10. 14:08 | 14:18 | 10 | Ladung selbst (SF2<40, -1,6 K) | 45,2 | 52,5 | 6,0 | 1 | 7 | 2,45 | 2,85 | 93/5/1 |
| 56 | 26.10. 18:34 | 18:44 | 10 | Abendfenster (1500<48) | 48,4 | 52,7 | 6,8 | 1 | 4 | 1,62 | 2,47 | 100/0/0 |
| 57 | 27.10. 07:06 | 07:11 | 5 | Ladung selbst (SF2<40, -1,3 K) | 45,2 | 52,5 | 5,2 | 1 | 10 | 3,61 | 2,77 | 100/0/0 |
| 58 | 27.10. 17:05 | 17:10 | 5 | Abendfenster 17:00 (1500<48) | 46,4 | 52,3 | 10,1 | 1 | 9 | 3,13 | 2,87 | 100/0/0 |
| 59 | 28.10. 09:12 | 09:17 | 5 | Ladung selbst (SF2<40, -0,6 K) | 45,3 | 52,7 | 8,6 | 1 | 9 | 2,59 | 3,48 | 87/10/3 |
| 60 | 28.10. 18:07 | 18:17 | 10 | Abendfenster (1500<48) | 48,1 | 52,1 | 9,2 | 1 | 4 | 1,55 | 2,59 | 100/0/0 |
| 63 | 29.10. 18:07 | 18:12 | 5 | Abendfenster (1500<48) | 47,7 | 52,5 | 8,0 | 1 | 8 | 2,45 | 3,26 | 100/0/0 |
| 64 | 30.10. 19:23 | 19:28 | 5 | Abendfenster (1500<48) | 47,9 | 52,7 | 7,0 | 1 | 3 | 1,37 | 2,19 | 100/0/0 |
| 66 | 31.10. 17:05 | 17:10 | 5 | Abendfenster 17:00 (1500<48) | 47,3 | 52,7 | 8,8 | 1 | 4 | 1,64 | 2,45 | 36/64/0 |

Einzel-AZ grob (27489 hat nur 1 kWh Auflösung, bei Q = 4 etwa ±25 %). Nr 2: Stab 01.10. brachte danach 1500 auf 61,7 °C, in der Tabelle steht die WP-Ladung. Nr 35: Ladung seit 10:35, Zählersprung, wie F68 ausgeschlossen. [sicher]

### 3. Klassen (Summen, ohne die 2 Ausschlüsse)
| Klasse | n | Q kWh_th | E kWh_el | AZ | AT (Q-gew.) | 1500 Start | 1500 Ende | P_el kW | Soll-E Regression | Netz / Akku / PV kWh_el | Netz max / PV min |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SG-57 (01.-23.10.) | 28 | 174 | 50,8 | 3,42 | 14,6 | 50,1 | 55,5 | 2,65 | 50,7 | 11,8 / 13,1 / 26,0 | 15,7 / 19,8 |
| Kick 01.-23.10. | 17 | 152 | 47,2 | 3,22 | 11,0 | 47,3 | 52,7 | 3,08 | 47,7 | 27,2 / 13,3 / 6,7 | 30,1 / 7,9 |
| Kick 24.10.-01.11. | 14 | 106 | 36,7 | 2,88 | 7,6 | 47,0 | 52,4 | 3,00 | 35,9 | 27,8 / 3,2 / 5,8 | 29,1 / 4,9 |
| Kick gesamt | 31 | 258 | 83,9 | 3,07 | 9,6 | 47,1 | 52,6 | 3,04 | 83,6 | 55,0 / 16,5 / 12,5 | 59,2 / 12,7 |
| Normal 50-52 01.-23.10. | 33 | 176 | 58,4 | 3,01 | 9,8 | 46,4 | 51,7 | 2,85 | 56,8 | 36,3 / 18,3 / 3,8 | 42,3 / 3,5 |
| Normal 50-52 24.10.-01.11. | 17 | 96 | 32,4 | 2,97 | 7,4 | 45,7 | 51,3 | 2,96 | 32,7 | 21,0 / 6,6 / 4,7 | 26,0 / 2,4 |
| Normal gesamt | 50 | 272 | 90,8 | 3,00 | 9,0 | 46,2 | 51,5 | 2,89 | 89,5 | 57,3 / 24,9 / 8,5 | 68,3 / 5,9 |

- **Temperatur:** Mit SG-Ladungen, die oben ≥ 54 °C erreichen (22 von 28): im Mittel 56,2 °C, Maximum 57,0 (04.10. 12:10 Ladung, Reg 1500). WP-VL am Ladungsende im Mittel 61,2 °C, Hub VL - 1500 = 6,4 K, Maximum 1525 = 62,0 °C. Passt zu `FUND_CombiVal_Waermetauscher_20261102.md` (Hub 6,3-6,6 K): **57,0 °C oben ist die Obergrenze** und wird nur selten erreicht. [sicher]
- **AZ:** SG-Ladungen zeigen trotz höherem VL keinen messbaren Nachteil zur Außentemperatur-Geraden der Normalladungen (+0,1 kWh_el auf 50,7). MD-10 rechnet im Band 52 → 55,8 °C mit -0,25 bis -0,35 AZ [dort Vermutung]. Dieses Band ist nur ein Teil der Ladung, die Streuung der Geraden (0,28) und die Extrapolation bis 19 °C außen decken das nicht auf. Also: Nachteil klein, nicht null. [wahrscheinlich]
- **Kick-Zuschlag:** +0,3 kWh_el auf 83,6 in 4,6 Wochen, innerhalb der Streuung (Normal selbst +1,3). Kick-Ladungen sind nur deshalb teurer, weil sie Zapfung mitbezahlen (8,3 kWh_th statt 5,4). [wahrscheinlich]

### 4. Echter PV-Überschuss?
- **Ja bei den meisten SG-Tagesladungen** (z. B. 13.10. 12:10: Bezug 0,00, Einspeisung 4,15-6,12 kWh/h). Über alle 28: 51 % PV direkt, 26 % Akku, 23 % Netz. Untergrenze PV direkt 39 %, Obergrenze Netz 31 %. [wahrscheinlich]
- **Nein bei 7 von 28 SG-Ladungen** (PV direkt unter 10 %): 08.10. 12:40, 14.10. 06:20, 15.10. 18:25, 18.10. 15:45, 19.10. 17:30, 19.10. 19:15, 23.10. 16:05. Zusammen 40 kWh_th, 12,7 kWh_el, davon ~8,6 Netz. [wahrscheinlich]
  - **14.10. 06:25** SG = 1 vor Sonnenaufgang: Stunde 04Z PV 0,00 kWh, Bezug 1,95 kWh, Akku 1,65 kWh entladen. Die 45 min sind die OL6-Mindestlaufzeit. [sicher für die Daten, Ursache offen]
- **Kick nie PV-gesteuert.** Kick-Ladungen 66 % Netz, seit 24.10. 76 %. Nachtladung nur bis 08.10. Morgen und Abend sind Netzzeiten. [wahrscheinlich]

### 5. 01.11. 05:50 (offener Punkt aus `ANALYSE_X26_Obj20_Live_20261101.md`)

### 6. Stichprobe Rohzeilen
Volllogger, Spalten zeit; 1497; 1499; 1500; 27483; 1521; 1525; 1477; 1539; 1504; 25611; 27489; 25614; 27545:
```
~/hoxpi_fulllog/2026-11-01.csv
2026-11-01 05:50:02;500;500;471;400;0;385;37;1;0;183;40184;30538;0
2026-11-01 05:55:02;570;570;467;400;610;500;37;4;1;449;40185;30538;0
2026-11-01 06:05:01;520;520;475;417;560;535;37;4;1;312;40187;30539;0
~/hoxpi_fulllog/2026-10-14.csv.gz
2026-10-14 06:25:02;570;570;467;430;610;525;97;4;1;360;39749;30281;1
~/hoxpi_fulllog/2026-10-15.csv.gz
2026-10-15 13:40:02;570;570;468;441;610;450;141;4;1;249;39775;30295;1
2026-10-15 14:25:02;570;555;558;530;0;585;147;0;0;0;39782;30297;1
```
Loxone Stunde 14.10. 04Z (imp, exp, PV, Akku Ent, Akku Lad, kWh): 1,95 / 0,01 / 0,00 / 1,65 / 0,00. Heizstab 01.10. (Tag) 7,00 kWh.

## Was bringt uns das
| Hebel | Wirkung kWh_el/Woche | Einstufung |
|---|---|---|
| SG-57 lassen wie es ist, sonnige Tage (01.-23.10.) | **rund 3,5-5 weniger Netzbezug** | [Vermutung] |
| SG-57 Winter (seit 24.10., Deckel) | **0** (keine Phase, Einspeisung kaum) | [sicher für 9 Tage] |
| Drift-Kick weg (Nr 68 u. a., etwa 1,3/Woche) | **unter 0,5** (Ladung fällt später ohnehin an) | [Vermutung] |
| SG-Pfad nur bei echter PV | **höchstens 2,6**, eher 1-2 | [Vermutung] |

Rechnung SG-57: PV direkt 26,0 kWh_el (Untergrenze 19,8) × AZ 3,42 = 89 (68) kWh_th. Ersatzladung normal AZ 3,01 mit 62 % Netz: 18,3 (14,0) kWh_el Netz. Abzug Mehrverlust: 22 Ladungen × ~26 W (6,7 W/K × 3,9 K) × ~12 h = 6,9 kWh_th = 2,3 kWh_el. Netto 11,7-16,0 kWh_el in 3,3 Wochen. Einspeisevergütung ist nicht gegengerechnet, und ob die Wärme sonst wirklich aus Netz käme, ist Annahme.

**Vorschläge (nur Vorschlag, nichts geändert, der Betreiber entscheidet; vor Umbau Backup und Skill `loxone-xml-umbau`):**
1. **SG-Pfad zu 57 mit PV absichern:** Formel „WW-Soll Manager" I2 nicht direkt vom Merker „Smart Grid Auslösen", sondern über UND mit „PV aktuell ≥ 1,5 kW" (Ppwr) bzw. „Sonne über Horizont". Rückweg: I2 wieder direkt. Doku [Energiemanager](https://www.loxone.com/dede/kb/energiemanager/), [Merker](https://www.loxone.com/dede/kb/). Mindestens zuerst Ursache der dunklen SG-Phasen klären (Offen 1).
2. **Kick behalten.** Kostet praktisch nichts, die Hysterese wäre sonst das Problem (F39). Für Drift-Kicks SF2-Schwelle mit Gradient ergänzen ist möglich, lohnt in kWh aber nicht. Doku [Monoflop](https://www.loxone.com/dede/kb/monoflop/), [Schwellwertschalter](https://www.loxone.com/dede/kb/schwellwertschalter/).
3. **Nichts am Deckel ändern.** Im November gibt es dafür kaum Einspeisung.

Hinweis Links: Die Unterseiten waren aus dem Skript nicht prüfbar (HTTP 403), Einstieg ist https://www.loxone.com/dede/kb/.

**Korrektur zu `ANALYSE_F57_PV_Heizstab_20261101.md`:** Dort „Oktober-Max Reg 1500 = 58,9 °C". Tatsächlich 01.10. 15:30:02 Reg 1500 = 617 (61,7 °C), Stab 7,00 kWh an dem Tag. Die Aussage „WP schafft keine 60 °C" bleibt richtig (WP-Maximum 57,0 °C). [sicher]

## Offen
1. **Warum OL6 ohne PV schaltet** (14.10. 06:25, 16.10. 06:15 mit Soll 52, 19.10. 18:56, 22.10. 18:11 und 18:40, 23.10. 18:05 und 19:06). Prüfweg: Energiemanager-Eingänge Gpwr/Spwr/Soc in der Loxone-Statistik zu diesen Zeiten, Wirkung Spwr-Fix.
2. **PV-Prognose historisch** nicht gelesen: 26.10. waren es 22,9 kWh PV bei Deckel 52, also lag die Prognose vermutlich unter 20 kWh [Vermutung].
3. **Kick-Verzögerung** 16 min statt 5 min (01.10., 02.10., 06.10., 14.10.) nicht geklärt.
4. **Stromherkunft** nur Stundenraster, Herkunft der Akkuladung offen. Spotpreis/Tarife nicht bewertet (F60, Spotpreis-Optimierer).
5. **Winter ab 24.10.** nur 9 Tage Daten; Winter-Wochenwerte für SG-57 noch nicht belastbar.