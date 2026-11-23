# REGELWERK (beobachtet) – Stand 2026-11-23 21:50:03

Datenfenster 2026-11-09 00:00:02 – 2026-11-23 21:50:02 · bestätigt 23 · offen 1 · widerlegt 3 · nicht prüfbar 0

**Kritisch:** S02 verletzt: Das WW-Soll aktiv (1499) ist entweder ein Loxone-Wert (45 Nacht, 50 Tag, 52 Abendfenster, 54, 57 Smart Grid), 10 (Abtauung) oder ein Zwischenwert 52–57 (Hoval regelt das SG-Soll offenbar stufig ab: 55,9/55,6/55,2/54,8/54,6 gemessen, auch noch nach dem Rückfall von 1497 auf 50). (2026-11-16 07:10:02); S03 verletzt: Loxone schreibt WW-Soll (1497) nur als 45 (Nacht), 50 (normal), 52 (Abendfenster), 54 oder 57 (PV-Überschuss). Gemessen außerdem 58 in 19 Zeilen (15.09.–01.11.) – Herkunft offen. (2026-11-23 07:05:02)

## Heizkreis

| Ampel | Nr | Regel | Art | Prio | ok/verletzt/unprüfbar | Hinweis | letzter Verstoß | Quelle |
|---|---|---|---|---|---|---|---|---|
| ✅ | H01 | Im Heizbetrieb (1539 = 1 vor dem Stopp) stoppt der Verdichter erst, wenn der WEZ-Rücklauf (1535) über dem Heizsoll der WEZ (1529 = 1490 + 07-001) liegt (5-min-Raster: letzter Laufwert ≥ 1529 + 1,0 K, Median 2,5 K, P10 2,0 K, P90 3,0 K). Ausgenommen: Ende einer WW-Ladung und Verdichterpause vor einer Abtauung (1539 = 51 oder 8 im Folgetakt). Die Schwelle hängt an 1529, nicht an 1490: 07-001 von 3 auf 2 K hat sie nicht verschoben. | Messung | 1 | 129/5/0 | 134 Faelle, 5 Verstoesse | 2026-11-18 04:45:02 | Eichung 03.11.2026 (146 Stopps 15.09.-01.11.); MD-22f FUND_Regel_H01_[Nummer], von Claude 05.11. 23:05 nachgerechnet (91 von 91, vor/nach 31.10. je Median 2,5 K); WFA 33-053 = 3,0 K; FUND_Heiz_Hysterese_RL_20261101 (dort auf 1490 bezogen) |
| ✅ | H03 | Der Verdichter startet im Heizbetrieb erst, wenn der Rücklauf (1535) mindestens 1,5 K unter dem Heizsoll der WEZ (1529) liegt (5-min-Raster: Median 2,5 K, P10 2,0 K). Hoval-Doku 33-054 = 1,0 K passt nicht – Widerspruch X02 bleibt. | Messung | 2 | 192/1/0 | 193 Faelle, 1 Verstoesse | 2026-11-11 09:35:02 | Eichung 03.11.2026 (190 Starts 15.09.–01.11.); Durchbruch WFA-200 (33-054 = 1,0 K) |
| ✅ | H06 | Das Heizsoll der WEZ (1529) ist HK1-Soll (1490) + 07-001 (30684, live; 2,0 K seit 31.10.2026, in E2 1,0 K), auf 0,5 K gerastet. | Messung | 1 | 1521/4/0 | 1525 Faelle, 4 Verstoesse | 2026-11-19 08:20:01 | FUND_TopTronicE_Vorlaufueberhoehung; 02_Status_Offen 31.10. |
| ✅ | H30 | Steht der WEZ-Status 1539 auf 16 (Anforderung wartet in der Sperre), laeuft der Verdichter nicht (25611 < 0,3 kW). | Experiment | 3 | 41/0/0 | 41 Faelle, 0 Verstoesse |  | Experiment E4 05.11.2026 19:22-19:27 (1539 = 16 mit Anforderung, 0 ohne, kein Start); ANALYSE_F109_Status16_Sperre_20261105; MD-42 |

## Warmwasser

| Ampel | Nr | Regel | Art | Prio | ok/verletzt/unprüfbar | Hinweis | letzter Verstoß | Quelle |
|---|---|---|---|---|---|---|---|---|
| ❌ | S02 | Das WW-Soll aktiv (1499) ist entweder ein Loxone-Wert (45 Nacht, 50 Tag, 52 Abendfenster, 54, 57 Smart Grid), 10 (Abtauung) oder ein Zwischenwert 52–57 (Hoval regelt das SG-Soll offenbar stufig ab: 55,9/55,6/55,2/54,8/54,6 gemessen, auch noch nach dem Rückfall von 1497 auf 50). | Messung | 2 | 4291/4/0 | 4 Verstoesse von 4295 (0 %) | 2026-11-16 07:10:02 | Eichung 03.11.2026 (1499-Werteverteilung 15.09.–01.11.); Memory ww-zeitprogramm-nachtabsenkung-45; ANALYSE_F48 |
| ⏳ | W01 | Eine WW-Ladung beginnt, wenn WW-Soll aktiv (1499) minus WW oben (1500) mindestens 4,9 K beträgt (5-min-Raster: ≥ 4,2 K im Wert vor dem Start, Median 4,8); gilt für Hoval-eigene Starts bei stehenden Sollwerten (1497 ≤ 50, keine Flanke von 1497/1499). | Messung | 1 | 10/1/0 | 11 von 15 Faellen, 1 Verstoesse | 2026-11-20 06:15:02 | E1 03.11.2026 13:31–13:35 [sicher]: kein Start bei Δ 4,4–4,7 K, Start 10 s nach Δ 5,0 K (EXPERIMENTE.md); MD-07 (28 Starts, Median 4,90 K); Eichung 03.11.2026 (36 stabile Starts, Median 4,8, P10 4,4, min 3,7) |
| ✅ | W02 | Am regulaeren Ende einer normalen WW-Ladung (Soll ≤ 52, ohne Abtau-Abbruch und ohne Soll-Absenkung durch Loxone) liegt WW oben (1500) zwischen Soll − 1,5 K und Soll + 0,5 K (gemessen Median −0,5, P10 −0,9, P90 −0,3 K); Ladesoll 1521 liegt dabei 4,5 K über 1499. | Messung | 2 | 40/0/0 | 40 Faelle, 0 Verstoesse |  | Eichung 03.11.2026 (102 Ladeenden); Rohstoff W-Teil (30-049/05-056) |
| ✅ | W04 | Endet eine WW-Ladung nahe am Soll (1500 davor >= 1499 - 1,5 K, also kein Abtau-Abbruch), lag der WP-Vorlauf (1525) in der letzten Ladezeile mindestens 4,0 K ueber WW oben (1500). | Messung | 2 | 49/2/0 | 51 Faelle, 2 Verstoesse | 2026-11-18 19:00:02 | FUND_CombiVal_Waermetauscher_20261102; Rohstoff W04; MD-23, geprueft OR 05.11.2026 (erste Fassung >= 4,5 K widerlegt: 28.10. 18:45 und 29.10. 13:05 je 4,3 K bei 1525 = 56,0 auf dem Ladesoll; 03.11. 22:45 und 04.11. 07:05 sind Abtau-Abbrueche, jetzt ausgeschlossen) |
| ✅ | W10 | Während einer WP-Ladung (1504 = 1) überschreitet WW oben (1500) nie 57,0 °C - die 57-°C-Ladung (SG oder Legionellen-WP-Phase) endet an der 62-°C-Vorlaufgrenze bei 55,4-56,8 °C; nach Ladeende steigt 1500 durch Nachwärme noch bis ca. 58,3 °C. (Ohne Ladung bringt der PV-Heizstab den Speicher bis 62-64 °C.) | Messung | 2 | 4295/0/0 | 4295 Faelle, 0 Verstoesse |  | Rohstoff W-Teil (Überhub 6,3–6,6 K konstant); Eichung 03.11.2026 (max 1500 = 62,0 ohne Ladung, 0 Zeilen > 56 mit Ladung) |

## Abtauung

| Ampel | Nr | Regel | Art | Prio | ok/verletzt/unprüfbar | Hinweis | letzter Verstoß | Quelle |
|---|---|---|---|---|---|---|---|---|
| ✅ | A01 | Während einer Abtauung (1539 = 8) steht das WW-Soll aktiv (1499) auf 10 °C. | Messung | 2 | 32/0/0 | 32 Faelle, 0 Verstoesse |  | ANALYSE_F48_WWSoll10_Abtauung_20261029 (4/4) |
| ❌ | A05a | Keine Abtauung ohne Lufteintritt (27491) <= 4,0 °C und, wenn davor ein Lauf-Abtastpunkt liegt, Niederdruck (31915) <= 7,00 bar (R410A-Sättigung etwa <= 0 °C) in den 15 min davor. | Messung | 2 | 24/8/0 | 8 Verstoesse von 32 (25 %) | 2026-11-20 14:25:01 | MD-28 FUND_Regel_A05a_[Nummer], geprüft OR 05.11.2026: 16 von 16 Abtauungen 13.10.-05.11. erfüllt, davon 5 außerhalb der Ableitung (13.10. zwei, 04./05.11. drei). Nur notwendige Bedingung: 76 % der Laufzeilen haben ND <= 7 bar, 58 % Luft <= 4 °C. 27492 bleibt tot (32768). |
| ✅ | A05b | Eine Abtauung kann weniger als 20 min nach einem Verdichterstart beginnen (widerlegt feste Startsperren 20/30 min). | Messung | 2 | 8/24/0 | erwarteter Fall trat 24-mal ein | 2026-11-23 17:55:02 | Rohstoff A-Teil (13.10.: Abtauung 1,5 min nach Start) |

## Verdichter

| Ampel | Nr | Regel | Art | Prio | ok/verletzt/unprüfbar | Hinweis | letzter Verstoß | Quelle |
|---|---|---|---|---|---|---|---|---|
| ✅ | H05 | Zwischen Verdichterstopp und nächstem Start vergehen mindestens 15 min (Mindeststehzeit); Pausen um eine Abtauung (1539 = 8) sind ausgenommen – dort startet der Verdichter nach ca. 5 min wieder. | Messung | 2 | 199/0/41 | 199 Faelle, 0 Verstoesse |  | STAND 21.10. (V99, 7× exakt 15,0 min); BV008 = 10 min live laut iDM-Tabelle – Widerspruch; Live 03.11.2026: 10 Pausen zu 5 min, alle um Abtauungen (z. B. 03.11. 08:00/08:10) |
| ✅ | H28 | Höchstens 3 Verdichterstarts je Stunde. | Herstellerdoku | 2 | 240/0/1 | 240 Faelle, 0 Verstoesse |  | Technikhandbuch Hoval 2026/27 S.49/50 (Sole-Beispiel) |
| ✅ | V02 | Im stationären Lauf (P_el ≥ 1,5 kW) liegt die Modulation (18726) nie unter 30 % (Minimum 34-050 = 35 %); Rampen mit < 1,5 kW sind ausgenommen. | Herstellerdoku | 2 | 4295/0/0 | 4295 Faelle, 0 Verstoesse |  | Durchbruch WFA-200 (34-050 = 35 %) |

## Heizstab

| Ampel | Nr | Regel | Art | Prio | ok/verletzt/unprüfbar | Hinweis | letzter Verstoß | Quelle |
|---|---|---|---|---|---|---|---|---|
| ✅ | B01 | Die elektrische Leistung WEZ (25611) ueberschreitet nie 8,0 kW (Verdichter laut Hoval maximal 7,6 kW, gemessen maximal 5,96 kW). Kein Heizstab-Nachweis: 25611 ist nahe am Inverter, der Stab hat eine eigene Zuleitung; Nachweis ueber B02a/B02b. | Herstellerdoku | 2 | 4295/0/0 | 4295 Faelle, 0 Verstoesse |  | MD-22e, FUND_Regel_B01_20261105; Hoval Technikhandbuch S. 18, 25; ANALYSE_PelVergleich_X4_Hoval_20261030; geaendert OR 05.11.2026 (vorher 5,5 kW, 05.11. 06:50 Fehlalarm) |
| ✅ | B02a | Die Außentemperatur-Freigabe der Zusatzheizung 09-012 (Register 27549) steht fest auf -50,0 °C (Heizstab über TopTronic E gesperrt). | Messung | 1 | 4295/0/0 | 4295 Faelle, 0 Verstoesse |  | FUND_Heizstab_Freigabe_20261101; Projektanweisung; Rohstoff B02 |
| ✅ | B02b | Die Betriebsstunden- und Einschaltzähler der Zusatzheizung (31657 bis 31660) sowie die Betriebsartenwahl (19485) bleiben dauerhaft auf 0 (kein Heizstab-Einsatz; realer Frosttest erst bei AT < -10 °C). | Messung | 1 | 4295/0/0 | 4295 Faelle, 0 Verstoesse |  | FUND_Heizstab_Freigabe_20261101; Rohstoff B02 |
| ✅ | B09 | Das WEZ-Statusregister (18743) zeigt nie den Zustand 3 (Extern gesperrt / EVU-Sperre), da kein unterbrechbarer Tarif aktiv ist. | Vermutung | 2 | 4295/0/0 | 4295 Faelle, 0 Verstoesse |  | FUND_EVU_Sperre; FUND_TopTronicE_Startverzug; Rohstoff B09 |

## Pumpen

| Ampel | Nr | Regel | Art | Prio | ok/verletzt/unprüfbar | Hinweis | letzter Verstoß | Quelle |
|---|---|---|---|---|---|---|---|---|
| ✅ | H09 | Steht die HK1-Sollanforderung (1490) seit mindestens 10 min unter 5 °C und melden HK1-Status 1501 = 0 und WEZ-Status 1539 = 0, ist die HK1-Pumpe (19706) aus. | Messung | 2 | 497/0/2 | 497 Faelle, 0 Verstoesse |  | Technische_Unterlagen_Steuerung_Hoval.pdf Kap. 10.2.21, 10.2.16; MD-22c, FUND_Regel_H09_20261104; uebernommen OR 05.11.2026 (Abschaltlatenz 5-10 min und zwei Standbilder 20.10./29.10.; Stichprobe 01.11. 17:20-17:30). Grenze: Eine Pumpe, die bei eingefrorenem 1501 = 23 weiterlaeuft, sieht die Karte nicht. |
| ✅ | H22 | Waehrend einer laufenden WW-Ladung ab der zweiten 5-min-Zeile (1504 = 1 und 5 min davor 1504 = 1) steht die HK1-Pumpe (19706 = 0, 1501 = 6 Zwangsdrosselung). | Messung | 2 | 496/0/0 | 496 Faelle, 0 Verstoesse |  | Projektanweisung + TTE-Doku Kap. 10.2.18, 10.3.5; MD-22d, FUND_Regel_H22_20261104; uebernommen OR 05.11.2026 (alle Verstoesse bei t = 0 min der Ladung; Stichprobe 03.11. 13:35-13:40, 30.10. 19:25-19:30) |

## Loxone

| Ampel | Nr | Regel | Art | Prio | ok/verletzt/unprüfbar | Hinweis | letzter Verstoß | Quelle |
|---|---|---|---|---|---|---|---|---|
| ✅ | H12 | Loxone schreibt fuer HK1-Soll (1490) nie einen Wert ueber 40,0 C (Maximalbegrenzung Heatmixer2). | Messung | 2 | 4295/0/0 | 4295 Faelle, 0 Verstoesse |  | FUND_F66; Rohstoff H12; MD-23, geprueft OR 05.11.2026 (Rueckblick 20.10.-01.11.: 3756/0) |
| ❌ | S03 | Loxone schreibt WW-Soll (1497) nur als 45 (Nacht), 50 (normal), 52 (Abendfenster), 54 oder 57 (PV-Überschuss). Gemessen außerdem 58 in 19 Zeilen (15.09.–01.11.) – Herkunft offen. | Messung | 2 | 4288/7/0 | 7 Verstoesse von 4295 (0 %) | 2026-11-23 07:05:02 | Eichung 03.11.2026 (1497-Werteverteilung); Memory loxone-pvboost-ueber-1497; 02_Status_Offen 28.10. |

## Experiment

| Ampel | Nr | Regel | Art | Prio | ok/verletzt/unprüfbar | Hinweis | letzter Verstoß | Quelle |
|---|---|---|---|---|---|---|---|---|
| ✅ | XE1 | 07-001 (30684) steht auf 2,0 K (Experimentstand seit 31.10.2026 22:01; Rückweg 3,0 K). | Messung | 1 | 3826/0/0 | 3826 Faelle, 0 Verstoesse |  | 02_Status_Offen 31.10.2026 |

## Sonstiges

| Ampel | Nr | Regel | Art | Prio | ok/verletzt/unprüfbar | Hinweis | letzter Verstoß | Quelle |
|---|---|---|---|---|---|---|---|---|
| ✅ | S01 | Der WP-Vorlauf (1525) überschreitet nie 62,0 °C (Typenschild max. VL). | Herstellerdoku | 1 | 4295/0/0 | 4295 Faelle, 0 Verstoesse |  | Memory geraetedaten-typenschild-grenzwerte |

---
Diese Datei wird erzeugt (regelwerk_md.py) – Änderungen in regeln.yaml, nicht hier. Widerlegte Regeln bleiben mit Beleg stehen.