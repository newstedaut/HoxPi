# ANALYSE F71 - Startsperre 98 (W:61, Fehlerreg. 124) im Heizbetrieb: wie nah liegt der Ruecklauf an der Sperrgrenze? - 02.11.2026 04:30

Bearbeitet vom Orchestrator-Subagent, nur gelesen (Volllogger lokal + Pi, ERR.LOG). Nichts an der Anlage geschrieben.

## Frage
Die Startsperre WEZ-Status `1539` = 98 (W:61, Fehlerreg. `1534` = 124) greift laut `ANALYSE_Status98_Startphase_Bedingung_20261022.md`, wenn der Ruecklauf `1535` bei der Startanforderung unter ~17,0 C liegt (Freigabe RL >= 19,0 C). Im Sommer kam sie nur nach Kuehllaeufen. Im HAICO-ERR.LOG steht W:61 aber auch 8x im Winter 2025/26 ohne Kuehlbetrieb. Frage: Trat 98 seit Beginn der Heizsaison (01.10.2026) auf, wie tief faellt `1535` vor Starts, in Stillstaenden ohne Durchfluss und nach Abtauungen, und wie gross ist der Abstand zur Sperrgrenze fuer den Winter?

## Datenquelle
- Volllogger lokal, 5-min, Rohwerte x10: `[lokaler Pfad]` ... `2026-10-22.csv.gz`, `[lokaler Pfad]` ... `2026-11-02.csv` (bis 02.11. 01:55; 9 252 Proben).
- Pi-Volllogger `/home/<user>/hoxpi_fulllog/2026-11-02.csv` (Zeilen 01:50-03:55, gelesen 02.11. ~04:00 ueber `[lokaler Pfad]`, nur `head`/`tail`/`cut`).
- HAICO-Fehlerlog `[lokaler Pfad]` (Eintraege W:61).
- Vorarbeit: `[lokaler Pfad]`, `[lokaler Pfad]` (1539 = 8 = Abtauen), `[lokaler Pfad]`.
- Register: `1539` WEZ-Status (0 aus, 1 Heizen, 4 WW, 8 Abtauen, 16 Wiedereinschaltsperre, 17, 51 Startvorbereitung, 98 Startphase), `1534` Fehlercode, `1535` Ruecklauf WEZ, `18760` Vorlauf WEZ, `31708` Volumenstrom, `1477` Aussen, `1490` HK1-Soll Loxone, `1513` HK1-Vorlauf, `25611` P_el.

## Methode
1. Werteverteilung von `1539` und `1534` ueber alle 9 252 Proben 01.10.-02.11.
2. Starts = Uebergang `1539` von nicht 1/4/8 auf 1 oder 4 (263 Starts); `1535` in der Probe davor.
3. Stillstandsbloecke ohne Durchfluss (`31708` = 0, Verdichter aus, >= 60 min): Minimum `1535` je Block (112 Bloecke).
4. Abtauungen = `1539` = 8 bzw. `1499` = 100; Minimum `1535` in den 25 min ab Beginn.
5. ERR.LOG nach W:61 durchsucht.
Skripte liefen als Einweg-Aufruf (`py -3 -`); einzig `[lokaler Pfad]` (Werteverteilung) liegt als Datei vor.

## Ergebnis
- **Keine Startsperre in der Heizsaison:** `1539` = 98 kam 01.10.-02.11. 0x vor, `1534` = 124 ebenfalls 0x (9 252 Proben). Vorkommende Status: 0 (7 227), 1 (1 007), 4 (960), 17 (22), 51 (17), 16 (13), 8 (6). [sicher, Volllogger]
- **Ruecklauf vor Starts:** 263 Starts, `1535` vor dem Start Minimum 20,5 C (30.10. 00:15, aussen 3,9 C), Median 30,5 C. Abstand zur Sperrgrenze 17,0 C mindestens 3,5 K. [sicher, Volllogger; Grenze 17/19 = wahrscheinlich aus Analyse 22.10.]
- **Stillstand ohne Durchfluss:** In 112 Bloecken >= 60 min faellt `1535` binnen ~45-60 min nach Stopp auf ein Plateau und bleibt dort, egal wie lang die Pause ist. Tiefster Wert 20,0 C (29.10. 22:30-23:40), 01./02.11. 20,5 C um 21:15, danach sogar Anstieg auf 22,0 C bis 02:10, waehrend HK1-Vorlauf `1513` weiter auf 19,3 C faellt. Fruehere Oktober-Bloecke: Plateaus meist 24-30 C. [sicher, Volllogger]
- **Deutung Plateau:** Der WEZ-RL-Fuehler gleicht sich ohne Durchfluss an seine Umgebung (Inneneinheit im Technikraum) an; das Plateau ~20-22 C ist sehr wahrscheinlich die Temperatur im Aufstellraum bzw. im stehenden Wasser der Inneneinheit, nicht die Aussenluft (Aussen dabei 3,6-4,3 C). [wahrscheinlich; Technikraum-Temperatur nicht als Loxone-Verlauf gefunden]
- **Trend:** Das Plateau sinkt mit der Jahreszeit (Anfang Oktober 22,5-30 C, Ende Oktober/Anfang November 20,0-20,5 C). [sicher fuer die Werte, Ursache wahrscheinlich kuehlerer Technikraum]
- **Abtauungen:** 5 Abtauungen im Heizbetrieb (13.10. 07:10 und 08:40, 26.10. 05:05, 27.10. 06:45, 02.11. 02:25). `1535` fiel dabei nur auf 27,5-32,5 C (VL `18760` bis 23,0 C), die Pumpe laeuft weiter. Abstand zur Sperre >= 10 K. Abtauung loest 98 heute nicht aus. [sicher, Volllogger + Pi 02.11.]
- **Letzter Winter:** ERR.LOG zeigt W:61 am 14.12.2025 19:41, 25.12.2025 12:41, 09.01.2026 08:57, 27.01.2026 18:46, 26.02.2026 09:30/09:31/09:34, 01.03.2026 20:41 - also 6 Tage in 3,5 Monaten, ohne Kuehlbetrieb. [sicher, ERR.LOG; HAICO-Uhr ~75 min Versatz moeglich]
- **Folgerung:** Fuer 98 im Winter muss der RL beim Start unter ~17 C liegen. Im Heizbetrieb geht das nach heutigen Daten nur, wenn das Stillstandsplateau (Aufstellraum) unter ~17 C faellt. Bei heute 20,0-20,5 C fehlen dafuer ~3 K. Die Winterfaelle 2025/26 passen zu einem Technikraum, der an kalten Tagen unter 17 C kam, oder zu einem anderen Ausloeser (z. B. Netz-Aus/N [entfernt]). [Vermutung - fuer letzten Winter gibt es keinen Volllogger]
- **Kosten bei Auftreten:** 98 kostet keinen Strom (P_el 0, nur Pumpe), nur 5-15 min Startverzoegerung, bis RL >= 19 C. [wahrscheinlich, aus Analyse 22.10.]

## Stichprobe
| Datei | Zeit | 1539 | 1535 (RL) | 18760 (VL) | 31708 | 1477 | 1490 | 25611 | Rechnung |
|---|---|---|---|---|---|---|---|---|---|
| `...\2026-10-29.csv` | 2026-10-29 22:30:01 | 0 | 200 | 290 | 0 | 43 | 0 | 0 | RL 20,0 C, Abstand zu 17,0 = 3,0 K, kein Durchfluss |
| `...\2026-10-30.csv` | 2026-10-30 00:15:02 | 0 | 205 | 250 | 0 | 39 | 153 | 0 | letzter Wert vor Start: RL 20,5 C |
| `...\2026-10-30.csv` | 2026-10-30 00:20:01 | 1 | 310 | 340 | 341 | 38 | 325 | 205 | Start ohne 98, P_el 2,05 kW |
| Pi `2026-11-02.csv` | 2026-11-02 02:25:01 | 8 | 315 | 260 | 397 | 36 | 325 | - | Abtauung |
| Pi `2026-11-02.csv` | 2026-11-02 02:35:01 | 1 | 280 | 300 | 342 | 35 | 325 | - | RL-Min nach Abtauung 28,0 C (02:30 = 28,5 bei Status 16) |
Rohwerte /10 = C bzw. kW bzw. L/min-Rohwert.

## Offen
- Technikraum-Temperatur (Aufstellraum WEZ) als Verlauf: kein passendes Loxone-Control gefunden (`control_find "Technik Temperatur"` lieferte nur Puffer-Infos). Wenn es einen Fuehler gibt: gegen das `1535`-Plateau legen.
- Ob die Sperre im Heizbetrieb dieselbe Grenze 17/19 hat wie nach Kuehlen (nur im Sommer gemessen).
- Was die W:61-Faelle 2025/26 genau ausloeste (kein Volllogger damals).
- Beobachtungsregel fuer den Loop: sobald das Stillstandsplateau `1535` unter 18,5 C faellt, Vorwarnung; 98/124 dann mit Zeit, Aussen, Pausendauer notieren.

## Was bringt uns das
- Heute keine Handlung noetig: Die Startsperre spielt im Heizbetrieb keine Rolle, Abtauungen ziehen den RL nicht annaehernd an die Grenze. [sicher fuer 01.10.-02.11.]
- Ein 98/124 im Winter ist kein Defekt und kostet keinen Strom, nur einige Minuten Verzoegerung. Damit muss der Betreiber bei einer W:61-Meldung im Winter nichts unternehmen.
- Fruehwarner gefunden: Das RL-Plateau im Stillstand (heute 20-22 C) zeigt indirekt, wie kalt der Technikraum ist. Faellt es unter ~18 C, kommen Startsperren und vermutlich auch hoehere Waermeverluste der Inneneinheit/Leitungen - dann lohnt ein Blick auf Daemmung/Tueren im Technikraum.