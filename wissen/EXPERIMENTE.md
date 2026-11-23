# EXPERIMENTE — kurze, rückstellbare Versuche an der Anlage (ab 02.11.2026)

der Betreiber 02.11.2026: „Der stärkste Punkt ist experimentieren statt warten. Das kannst du ja immer tun. Kurz fällt es in der Regel sowieso nicht auf bei der Wärmepumpe.“
Regel im Vault `[eigene Notizen]` (Abschnitt „Wichtig“). Jeder Versuch steht VOR der Ausführung hier: Hypothese, Messgröße, Schritte, Dauer, Rückweg, Abbruchkriterium. Danach Ergebnis + Regel ins Regelwerk `REGELWERK_beobachtet.md`.

## Leitplanken
- **07.11.2026 Hand-Modus Experimente LIVE:** Vor Versuchen an 1490/1497 Hand-Modus starten (HTTP VI70 on, 3 s, off; Treppenlicht 21fab048-0020, 90 min, keine Remanenz). Loxone schreibt dann nur den rueckgelesenen Wert zurueck. Versuch trotzdem direkt nach dem letzten Loxone-SET starten (Rundumabfrage 60 s + Poll 30 s Fenster). Nach Ablauf oder Neustart schreibt Loxone seinen Sollwert = Rueckweg. 1490 > 0 schaltet HK1 ein (E18).

- **06.11.2026 22:57 Freigabe CAN (der Betreiber: „Auf can schreiben kannst du mittlerweile. Du kennst dich da ja aus"):** CAN-SET auf TopTronic-Datenpunkte (auch ohne Modbus-Whitelist, z. B. per hoxpi_probe.py/candump-Weg) und der Kältereglerweg fg=60/fn=7 sind freigegeben - nur als Experiment nach EXPERIMENTE.md-Leitplanken: Originalwert lesen, Hypothese + Rückweg + Abbruchkriterium vorher notieren, schreiben, zurücklesen, zurückstellen, zurücklesen, Journal. Weiter tabu (nicht rückstellbar/schädlich): Opcode 0x44 (friert Datenpunkt bis WEZ-Neustart ein), CF-Karte/EEPROM/Firmware, Kälteregler-Parameter ohne belegte Bedeutung und Grenzen (iDM-Tabelle, Firmware-Analyse), X4-Slaves (Inverter/EVD/Lüfter) direkt.

- Nur Katalogbereich, nur Register in der HoxPi-Whitelist (sonst der Betreiber fragen); Rücklesen mit `schreib_pruefung`.
- Nie: ND/HD-/Heißgas-/Frostschutzgrenzen, Kälteregler (X26/X4/CAN-Schreiben), Loxone-Projektdatei (eigener Weg), Heizstab-Freigaben.
- Loxone schreibt 1490 und 1497 alle 5 min zurück → bei diesen Registern ist der Rückweg automatisch; der Versuch muss in < 5 min seine Antwort liefern (WEZ-Sweep 60 s einrechnen).
- **Schreiben gilt erst als erfolgt, wenn `SET reg <n>` im Bridge-Protokoll steht** (`journalctl -u hoval-bridge`). `write_register` und `schreib_pruefung` lesen nur die Modbus-Tabelle und melden auch abgelehnte Schreibvorgaenge als ok (E20, 06.11.2026).
- Abbruch sofort bei Fehlercode ≠ 255, WW oben < 42 °C, Raum < 20,5 °C.

## Liste
| Nr | Datum/Zeit | Frage/Regel | Status |
|---|---|---|---|
| E1 | 03.11.2026 13:31–13:35 (Claude) | Hoval-WW-Hysterese: Ladestart genau bei Soll − Ist ≥ 4,9 K? (MD-07: Median 4,90 K, P10 4,87, aus 28 Starts) | **abgeschlossen – bestätigt:** kein Start bei Δ 4,4–4,7 K (2,5 min), Start 10 s nach Δ = 5,0 K |
| E2 | ab Mo 09.11.2026 | 07-001 = 1,0 K statt 2,0 K: Vorlauf-Abstand und Arbeitszahl über einen Tag (nach der Abnahme 07.11.) | **abgeschlossen 10.11. 09:00-15:00:** Rueckweg 2,0 gelesen, kein Abbruch; AZ-Wirkung nicht belegt (Aussentemp. ungleich) |
| E5 | 06.11.2026 07:03-07:09 | Heizlauf-Abschaltung: stoppt die WP, wenn WP-VL >= 1490 + 07-001 + 5,7 K? (MD-04) | **abgeschlossen, Wert widerlegt:** 7 min ueber 5,7 K ohne Stopp; Stopp erst, als 1490 von 33,1 auf 32,9 fiel, WP-VL - 1490 - 07-001 = 6,1 K |
| E3 | 05.11.2026 mit E4 | Ladepumpen-Freigabe ΔT (VL − WW oben ≥ 5–6 K?) | **widerlegt für den Stillstand:** SLP läuft in E4 10 s nach der Anforderung bei VL 31 °C und WW oben 52,5 °C |
| E4 | 05.11.2026 19:22-19:27 | 15-min-Sperre: zeigt 1539 = 16 eine wartende Anforderung? | **abgeschlossen, bestätigt:** 1539 geht mit der Anforderung auf 16 und ohne sie zurück auf 0, kein Verdichterstart |
| E6 | ab 06.11.2026 | Heizstart: kommt er 16 min nach `Ruecklauf` ≤ 1490 − 1,5 K, auch wenn das Soll den Abstand erzeugt? | abgebrochen 06.11. (Raster, siehe E15) |
| E7 | ab 06.11.2026 | WW-Ladestopp: endet eine laufende Ladung sofort, wenn 1497 unter WW oben sinkt? | geplant |
| E9 | 06.11.2026 07:00-07:03 | Soll-Sprung im Heizlauf: wie schnell folgt die Modulation 1490? | **abgeschlossen, bestaetigt:** +2 K, Modulation 35 auf 40 % binnen hoechstens 52 s, dann bis 07:03:15 zurueck auf 35 % |
| E10 | ab 06.11.2026 | Stoppschwelle: stoppt die WP erst bei 1535 - 1529 > 3,0 K (33-053)? | geplant |
| E11 | ab 06.11.2026 | Verstaerkung: wie viel % Modulation je K Soll-Sprung (+4 K)? | geplant |
| E12 | 06.11.2026 10:01-10:07 | WW-Start auf Zuruf: startet 1497 = 1500 + 5,4 K eine Ladung, und laeuft sie nach dem Rueckschreiben weiter? | **abgeschlossen, bestaetigt:** Verdichter binnen 62 s, Ladung lief nach Rueckschreiben auf 50,0 weiter |
| E13 | ab 06.11.2026 | WW in den Heizlauf: direkter Wechsel, wenn 1497 die Startschwelle kreuzt? | geplant |
| E14 | ab 06.11.2026 | Heizanforderung in der Sperre: zeigt 1539 = 16 auch sie? | geplant |
| E15 | ab 06.11.2026 11:00 | Wiederholung E6, Schreiben direkt nach dem Loxone-Raster | abgebrochen 06.11. (Loxone binnen 15 s zurueck, F164) |
| E16 | 06.11.2026 | Spar-WW-Soll 1498 im Konstantbetrieb: wirkt es, und wer schreibt es? | **abgeschlossen:** 1499 blieb 50,0, 1498 hielt 2:44 min, Rueckweg gelesen |
| E18 | ab 06.11.2026 12:30 | 1490 im Stillstand direkt nach einem Loxone-Schreiben: haelt der Wert bis zum naechsten Takt (F164)? | geplant |
| E21 | 06.11.2026 14:58-15:01 | 1529-Stufe: kippt 1490 von x,9 auf x,0 das Heizsoll um 0,5 K? | **abgeschlossen, bestaetigt** |
| E18 | 06.11.2026 16:02-16:12 | Haelt 1490 im Stillstand direkt nach einem Loxone-Schreiben bis zum naechsten Takt? | **abgeschlossen, bestaetigt fuer Eingang 0, Nebenwirkung HK1 ein** |

## E1 — WW-Hysterese (03.11.2026)
- **Hypothese:** Die Hoval startet eine WW-Ladung, sobald `1499 − 1500 ≥ 4,9 K` (Soll aktiv minus WW oben); bei 4,5 K nicht. 1499 folgt 1497 innerhalb eines Sweeps.
- **Voraussetzungen:** 1504 = 0 (keine Ladung), kein Heizlauf-Ende in den letzten 10 min, WW oben 44–48 °C, 1497 = 50, Zeit 11:00–15:00.
- **Schritte:** (1) Ist = 1500 lesen. (2) `write_register 1497 = round((Ist + 4,5)·10)` → 3 min warten → 1504, 1499, 25611 lesen → Erwartung: kein Start. (3) `write_register 1497 = round((Ist + 5,0)·10)` → bis 3 min → Erwartung: 1504 = 1 binnen ≤ 2 Sweeps. (4) Rückweg: nichts tun, Loxone schreibt 1497 = 50 binnen 5 min; prüfen, dass 1497 wieder 50 ist. Läuft die Ladung dann weiter bis 50 + Überhöhung – normal, kostet ~0,3 kWh.
- **Messgrößen:** 1497, 1499, 1500, 1504, 19754 (SLP), 25611, Zeitstempel je Lesung; parallel ww_hires.csv.
- **Ergebnis-Regel:** „WW-Ladestart ohne Loxone: 1499 − 1500 ≥ x K“ mit x auf 0,1 K; Sicherheit sicher, wenn Schritt 2 kein Start und Schritt 3 Start.
- **Abbruch:** Fehlercode ≠ 255 oder 1504 schon 1 vor Schritt 2 (dann anderer Tag).
- **Protokoll 03.11.2026 12:26 (Claude, Erinnerung):** 1504 = 0, 1500 = 49,3 °C → außerhalb 44–48 °C, verschoben auf 13:30 (Erinnerung gesetzt). Festlegung für den 2. Anlauf: Fenster auf 44–50,0 °C erweitert, weil die Hysterese-Prüfung niveauunabhängig ist und eine Ladung bis ~54 °C ≤ 0,5 kWh kostet.
- **Protokoll 03.11.2026 (Claude, 2. Anlauf, Fenster 44–50 °C):** Ausgangslage 13:30: 1504 = 0, 1534 = 255, Verdichter seit 13:02 aus, 1500 = 49,1, **1497 = 1499 = 52,0** (Loxone stand gerade auf 52, Δ 2,9 K, seit ≥ 30 min kein Start).
  - 13:31:04 `write_register 1497 = 536` (Ist 49,1 + 4,5) → hält (schreib_pruefung 13:31:19), 1499 = 53,6 sofort.
  - 13:31:52–13:34:22 (ww_hires, 10-s-Raster): WW_Ist 48,9–49,2, WW_Soll 53,6 → **Δ 4,4–4,7 K, WW_Status 0, SLP 0, P_el 0 – kein Start** (2,5 min).
  - 13:34:20 `write_register 1497 = 539` (48,9 + 5,0) → 13:34:32 WW_Soll 53,9 sichtbar, **13:34:42 WW_Status = 1, SLP = 1** (Δ = 5,0 K bei Ist 48,9) → Start **10 s** nach dem Schreibwert; 1499 folgt erst 13:35:02 auf 53,9 (Anzeige), P_el 13:35:22 0,57 → 13:36 2,8 kW.
  - 13:35:02 Loxone schreibt 1497 = 52 zurück (Rückweg automatisch, bestätigt um 13:35:40: 1497 = 1499 = 52,0); Ladung läuft weiter bis 52 + Überhöhung (Kosten ≈ 0,3 kWh).
  - **Ergebnis-Regel W01 [sicher]:** WW-Ladestart der Hoval bei **1499 − 1500 ≥ 4,9 K (±0,1 K)**: bei 4,7 K kein Start, bei 5,0 K Start. Deckt sich mit MD-07 (Median 4,90) und der Eichung (36 Starts, Median 4,8 im 5-min-Raster).
  - **Nebenfund [sicher]:** Die WEZ reagiert auf ein neues 1497 binnen 10 s (nicht erst nach dem 60-s-Sweep); das angezeigte 1499 hinkt bis 30 s nach.

## E4 — 15-min-Sperre sichtbar machen (05.11.2026, Claude im Chat, der Betreiber: "so viele wie möglich")
- **Hypothese:** `1539 = 16` zeigt die 15-min-Sperre nur mit anliegender Anforderung. Eine WW-Anforderung in der laufenden Sperre setzt 1539 von 0 auf 16 (ANALYSE_F109). Ohne Anforderung bleibt 0.
- **Lage:** Verdichter aus 19:14/19:15, Sperre rechnerisch bis ca. 19:30, 1539 = 0, 1504 = 0, Aussen 4,4 °C, Fehler 255.
- **Schritt:** `write_register 1497 = round(1500 + 5,0)`, dann 1539/1504/1499/25611 im 15-s-Takt lesen. Erwartung: 1539 = 16 binnen eines WEZ-Sweeps (60 s), kein Start vor Sperrende.
- **Rückweg:** auto_loxone (Loxone schreibt 1497 binnen 5 min zurück), Rücklesen. Läuft danach eine Ladung, kostet sie rund 0,3 kWh wie bei E1.
- **Abbruch:** Fehlercode ≠ 255, WW oben < 42 °C, Raum < 20,5 °C.
- **Ausnahme 17:00:** Die Grenze schützt das Abendfenster. Hier läuft der Rückweg automatisch binnen 5 min, und mehr WW schadet dem Abend nicht. In der Antwort an der Betreiber offen genannt.
- **Protokoll (Zeiten vom Pi, Prometheus im 15-s-Raster, WEZ-Register bis 60 s alt):** Verdichter aus 19:14 nach einer WW-Ladung. 1500 = 52,5 °C, 1539 = 0, 1504 = 0, Fehler 255. Geschrieben wurde 1497 = 57,8 °C (Ist + 5,3 K statt der geplanten 5,0 K, als Reserve gegen einen schwankenden Fühler).
  - 19:22:41 Soll 57,8 sichtbar, schreib_pruefung hält. 19:22:51 WW_Status = 1, SLP = 1, P_el 0.
  - 19:23:45 **1539 = 16.**
  - 19:26:41 Loxone schreibt 1497 = 50 zurück. 19:26:51 WW_Status = 0. 19:27:45 **1539 = 0.** Rücklesen 1497 = 50,0.
  - Der Verdichter lief nicht, Fehler 255. SLP lief nach WW_Status = 0 noch mindestens 3 min, HK1-Pumpe ab 19:27:52 wieder an, Vorlauf bis 51,0 °C. WW oben 52,5 auf 52,3 °C.
- **Ergebnis [sicher, je 1 Flanke]:** `1539 = 16` zeigt eine wartende Anforderung in der Sperre und fällt ohne Anforderung auf 0. Damit ist die in `ANALYSE_F109_Status16_Sperre_20261105.md` wahrscheinliche Deutung per Versuch belegt.
- **Nebenfunde:** Die SLP läuft in der Sperre ohne Verdichter und nimmt damit Speicherwärme in den Kreis [sicher als Registerwerte, Menge nicht gemessen]. 3 von 8 normalen WW-Enden liegen mit Vorlauf 51-54 °C bei laufender HK1-Pumpe im selben Bereich, der Vorlauf war also nichts Neues [sicher]. Der SLP-Nachlauf von 3 min passt zu den normalen 170-230 s [sicher].
- **Was bringt uns das:** Der Zwilling und der Wächter dürfen 1539 = 16 als „Anforderung wartet" lesen. Eine WW-Anforderung in der Sperre kostet Speicherwärme, schon bevor der Verdichter läuft, das geht in MD-42 (F111) ein.

## E9, E5, E8 — Kurzversuche 06.11.2026 (Orchestrator, Zeiten vom Pi, Prometheus effektiv 30-s-Raster)
- **E9:** 07:00:23 `write_register 1490 = 351` (+2 K), schreib_pruefung 07:00:38 haelt. 07:01:00 Mod 35 %, 1,94 kW. 07:01:15 Mod 40 %, 2,25 kW. 07:01:45 38 %, 07:02:15 37 %, 07:02:45 36 %, 07:03:15 35 %. WP-VL 41,1 bis 41,4 und zurueck. Rueckweg auto_loxone: 1490 spaetestens 07:03:37 wieder 33,1 (Zeitpunkt nicht aufgeloest). Leistung_Soll steht im Heizlauf auf -100 und taugt nicht als Messgroesse.
  - **Ergebnis [sicher, 1 Flanke]:** Die Modulation folgt binnen hoechstens 52 s, also vor dem 60-s-Sweep-Ende. [wahrscheinlich] Der Rueckgang ab 07:01:45 kommt vom Loxone-Rueckschreiben, das ist nicht getrennt gemessen. **Was bringt uns das:** Der Zwilling kann im Heizlauf mit unter 1 min Totzeit und rund 1 %-Punkt je 30 s Rueckgang rechnen. E11 misst die Verstaerkung.
- **E5:** Vorab: WP-VL lag seit 06:59:30 bei 41,0-41,1, also ueber der Hypothesengrenze 33,1 + 2,0 + 5,7 = 40,8, ohne Stopp. 07:03:54 `write_register 1490 = 329` (Formel des Blocks: 41,1 - 8,2 = 32,9), schreib_pruefung 07:04:09 haelt. 07:05:00 noch Lauf 1,93 kW, Volllogger 07:05:01 schon 1539 = 0, 25611 = 0. Schritt 2 (1 K tiefer) entfiel. 1490 spaetestens 07:09 wieder 33,1.
  - **Ergebnis:** Die Grenze 5,7 K gegen WP-VL ist widerlegt [sicher, 7 min darueber ohne Stopp]. Der Stopp kam rund 1 min nach einer Senkung um nur 0,2 K [sicher]. Volllogger 07:00:03: 1529 = 35,0, 1535 = 38,0, Differenz 3,0 ohne Stopp. 1529 und 1535 stehen in 0,5-K-Stufen; [Vermutung] 32,9 + 2,0 fiel auf 1529 = 34,5, Differenz 3,5. Das passt zu „stoppt bei mehr als 3,0 K“ (WFA 33-053), 1529 ist nach dem Schreiben aber nicht abgelesen, weil es beim Stopp auf 0 faellt. Ein Vorzeichen fuer die Ruecklauf-Schwelle aus H01, nur 1 Flanke. E10 und MD-78 pruefen das.
  - **Nebenwirkung:** Der Lauf endete rund 1 min frueher als noetig, die 15-min-Sperre lief bis etwa 07:20 bei WW 45,3-45,7. Die Ladeschwelle 45,1 ist fast erreicht, die Anforderung wartet dann bis zum Sperrende, Abbruchgrenze 42 nicht beruehrt.
  - **Was bringt uns das:** Eine Soll-Aenderung von 0,2 K kann einen Lauf beenden, wenn sie eine 0,5-K-Stufe kreuzt. Das geht in die Bewertung der 1490-Schritte von Loxone (F95, F129).
- **E8:** Lage 07:09: 1490 wieder 33,1, 1504 = 0, 1539 = 0, 1500 = 45,5, 1497 = 1499 = 50,0, SG Normal, 27509 = 0. 07:09:08 `write_register 27509 = 10` (+1,0 K), schreib_pruefung 07:09:23 haelt. Ablesung rund 07:12: 27509 = 1,0, 1499 = 50,0, 1504 = 0, 1539 = 0, 1500 = 45,5. Rueckweg 07:12:09 `write_register 27509 = 0`, schreib_pruefung 07:12:24 haelt. Dauer 3 min statt 5.

## Maschinenlesbare Blöcke (für den Orchestrator, Schritt R5/R6 in `[lokaler Pfad]`)

```yaml
# Jeder Block = ein Experiment. Der Orchestrator nimmt den ersten mit status: geplant und fruehester_start <= jetzt.
# rueckweg: Zahl (Anzeigeeinheit, write_register erwartet Rohwert = Wert x 10 bei dec1) oder auto_loxone (Loxone schreibt 1490/1497 alle 5 min zurueck).
# Waehrend eines Experiments liegt /home/<user>/regelwaechter/experiment_aktiv.json auf dem Pi; der Regelwaechter prueft abbruch und Rueckweg-Frist.
- id: E1
  titel: "WW-Hysterese: Ladestart bei 1499 − 1500 ≥ 4,9 K?"
  register: 1497
  wert_formel: "round(ist_1500 + 4.5, 1)"      # Schritt 2 (kein Start erwartet); Schritt 3 mit + 5.0 (Start erwartet) im selben Lauf
  rueckweg: auto_loxone
  fruehester_start: "2026-11-03 13:30"
  dauer_min: 8
  spaetester_rueckweg: "2026-11-03 14:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1504) == 0", "r(1497) == 50.0", "44.0 <= r(1500) <= 50.0", "r(1477) >= 0", "kein_experiment_aktiv", "whitelist_enthaelt(1497)", "kein_verdichterstopp_seit_10_min"]
  beobachtete_regeln: [W01]
  abbruch: ["r('1534') != 255"]
  status: abgeschlossen
  ergebnis: "03.11.2026 13:31-13:35 von Claude im Chat gefahren: kein Start bei Delta 4,4-4,7 K (2,5 min), Start 10 s nach Delta 5,0 K; Rueckweg durch Loxone 13:35:02 bestaetigt. Regel W01 sicher: Ladestart bei 1499-1500 >= 4,9 K (+-0,1)." 
- id: E2
  titel: "07-001 = 1,0 K (statt 2,0 K): Vorlauf-Abstand und AZ über einen Tag"
  register: 30684
  wert: 1.0
  rueckweg: 2.0
  fruehester_start: "2026-11-09 09:00"      # nach der 07-001-Abnahme am 07.11.; 08.11. ist ein Sonntag und nicht erlaubt
  dauer_min: 360
  spaetester_rueckweg: "17:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "kein_experiment_aktiv", "whitelist_enthaelt(30684)"]
  beobachtete_regeln: [H01, H06, XE1]
  abbruch: ["r('1534') != 255", "r('1500') < 42.0"]
  status: abgeschlossen
  protokoll: "OR 10.11.2026 09:00 (Pi-Zeit): Voraussetzungen live 1534 255, 1477 5,3, keine Datei, 30684 in Whitelist, vorher 30684 = 2,0 (1500 48,5). ~09:00:02 write 10, schreib_pruefung 09:00:17 haelt. experiment_aktiv.json auf dem Pi, ende_spaetestens 15:00 (Start + 360 min, frueher als 17:00). XE1.wert in regeln.yaml auf 1.0 (Backup regeln_bak_20261110_0900_or.yaml), pi_deploy --tests Exit 0. Rueckweg: write 30684 = 20 + schreib_pruefung, XE1.wert zurueck auf 2.0."
  ergebnis: "Rueckweg sauber: 10.11. 15:00:23 SET reg 30684 <- 20 im Bridge-Protokoll, schreib_pruefung 15:00:39 haelt, Pi-Datei 15:01 entfernt, XE1.wert in regeln.yaml auf 2.0 (gueltig_ab 15:01, Backup regeln_bak_20261110_1501_or.yaml), pi_deploy Exit 0. Waehrend E2 kein Abbruch (1534 255, kritisch_neu leer), H01/H06/XE1 bestaetigt, H06 rechnet 1529 = 1490 + 30684 live. Wirkung auf AZ/Vorlaufabstand NICHT belegt [offen]: Grobvergleich ww_hires 09-15 Uhr (cc_or_e2_auswertung_20261110.py) ist nicht verwertbar - Aussen 4,1 (09.11.) gegen 7,5 C (10.11.), nur 102 gegen 177 Heizzeilen, Spalte Vorlauf ist kein HK1-VL und P_th im ww_hires zu grob fuer eine AZ. Was bringt uns das: die Umstellung 07-001 laesst sich sauber hin und zurueck schalten; fuer die AZ-Frage braucht es Wiederholung an zwei Tagen mit gleicher Aussentemperatur und Auswertung aus Volllogger/WMZ (Paket, wenn Kontingent da)."
- id: E5
  titel: "Heizlauf-Abschaltung: Stopp bei WP-VL >= 1490 + 07-001 + 5,7 K?"
  hypothese: "Die WP stoppt binnen 2 min, sobald WP-VL die Grenze ueberschreitet; 0,5 K darunter laeuft sie weiter."
  register: 1490
  wert_formel: "max(20.0, round(ist_WP_VL - 2.0 - 5.7 - 0.5, 1))"   # Schritt 2 mit + 1.0 tiefer; Rohwert x10
  rueckweg: auto_loxone
  fruehester_start: "2026-11-06 07:00"
  dauer_min: 6
  spaetester_rueckweg: "21:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 0", "heizlauf_seit_mindestens_10_min", "kein_experiment_aktiv", "whitelist_enthaelt(1490)"]
  messgroessen: [1490, 1539, 25611, 18726, WP_VL, Vorlauf]
  abbruch: ["r('1534') != 255", "r('1500') < 42.0"]
  status: abgeschlossen
  ergebnis: "06.11.2026 07:03-07:09: 5,7 K gegen WP-VL widerlegt (7 min darueber ohne Stopp); Stopp rund 1 min nach 1490 33,1 auf 32,9, 1529 wohl eine 0,5-K-Stufe tiefer, Differenz 1535 - 1529 von 3,0 auf vermutlich 3,5. Rueckweg durch Loxone bestaetigt. Beobachtete Regel H01 unveraendert, kein neuer Verstoss."
- id: E6
  titel: "Heizstart: 16 min nach Ruecklauf <= 1490 - 1,5 K, auch bei Soll-Sprung?"
  hypothese: "Ein Soll, das den Abstand erzeugt, startet den Heizbetrieb 16 min spaeter (F54), nicht sofort."
  register: 1490
  wert_formel: "min(40.0, round(ist_Ruecklauf + 2.0, 1))"   # alle 4 min neu schreiben, weil Loxone nach spaetestens 5 min zurueckschreibt; Ende bei Start oder nach 22 min
  rueckweg: auto_loxone
  fruehester_start: "2026-11-06 07:00"
  dauer_min: 22
  spaetester_rueckweg: "21:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 0", "r(1539) == 0", "letzter_verdichterstopp_vor_mindestens_20_min", "Ruecklauf > r(1490) - 1.0", "kein_experiment_aktiv", "whitelist_enthaelt(1490)"]
  messgroessen: [1490, 1539, 25611, Ruecklauf]
  abbruch: ["r('1534') != 255", "r('1500') < 42.0"]
  status: abgebrochen
  ergebnis: "Abgebrochen nach R5: 1490 = 34,5 um 10:54:48 geschrieben, schreib_pruefung 10:55:03 las 30,5, Loxone hat binnen 15 s zurueckgeschrieben. Kein Messwert zur Frage. Meine Erklaerung Raster (Eintrag 10:55) ist durch E15 widerlegt."
- id: E7
  titel: "WW-Ladestopp: endet die Ladung, wenn 1497 unter WW oben sinkt?"
  hypothese: "Bei 1497 < 1500 geht 1504 binnen 1 min auf 0 und der Verdichter stoppt, ohne Ueberhoehung."
  register: 1497
  wert_formel: "round(ist_1500 - 1.0, 1)"
  rueckweg: auto_loxone
  fruehester_start: "2026-11-06 07:00"
  dauer_min: 6
  spaetester_rueckweg: "21:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 1", "ladung_seit_mindestens_5_min", "r(1500) >= 47.0", "kein_experiment_aktiv", "whitelist_enthaelt(1497)"]
  messgroessen: [1497, 1499, 1500, 1504, 1539, 25611]
  abbruch: ["r('1534') != 255", "r('1500') < 42.0"]
  status: abgeschlossen
  ergebnis: "1497 von 50,0 auf 46,2 (WW oben 47,2) um <MAC>: WW_Status 0 und WW_Soll 46,2 schon im Takt 08:55:12, Modulation 0 um 08:55:42, P_el 0 um 08:55:52, also Stopp binnen hoechstens 46 s [sicher fuer 1 Fall]. Loxone schrieb 1497 um 08:56:51 zurueck auf 50,0 (rund 1:45 min nach dem Schreiben); 1504 blieb bis 09:00 auf 0, keine neue Ladung, WW oben stieg durch Nachwaerme bis 47,7. Regeln: kein Statuswechsel, Fehler 255."
- id: E8
  register: 27509
  wert_formel: "ist_27509 + 1.0"
  rueckweg: "vorher gelesener Wert von 27509, im Protokoll notieren"
  fruehester_start: "2026-11-06 07:00"
  dauer_min: 5
  spaetester_rueckweg: "17:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 0", "smart_grid_normal", "kein_experiment_aktiv", "whitelist_enthaelt(27509)"]
  messgroessen: [27509, 1497, 1499, 1504]
  abbruch: ["r('1534') != 255", "r('1504') != 0"]
  status: abgeschlossen
- id: E9
  titel: "Soll-Sprung im Heizlauf: wie schnell folgt die Modulation?"
  hypothese: "Nach +2 K auf 1490 reagieren Leistung_Soll und Modulation binnen 2 min; die Antwortzeit fehlt dem Zwilling."
  register: 1490
  wert_formel: "min(40.0, round(ist_1490 + 2.0, 1))"
  rueckweg: auto_loxone
  fruehester_start: "2026-11-06 07:00"
  dauer_min: 6
  spaetester_rueckweg: "21:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 0", "heizlauf_seit_mindestens_10_min", "kein_experiment_aktiv", "whitelist_enthaelt(1490)"]
  messgroessen: [1490, 18726, 25611, Leistung_Soll, WP_VL]
  abbruch: ["r('1534') != 255", "r('1500') < 42.0"]
  status: abgeschlossen
  ergebnis: "06.11.2026 07:00-07:03: +2 K, Modulation 35 auf 40 % binnen hoechstens 52 s, ab 07:01:45 zurueck, 07:03:15 wieder 35 %. Rueckweg durch Loxone bestaetigt."
- id: E10
  titel: "Stoppschwelle: stoppt die WP erst bei 1535 - 1529 > 3,0 K?"
  hypothese: "Die WP stoppt, sobald WP_RL (Prometheus, 0,1 K) - 1529 rund 3,0 K erreicht (MD-78: 3,0-3,1 K in 90 von 101 Stopps); ein 1490-Schritt, der 1529 um 0,5 K senkt, stoppt sie also binnen 1 min, wenn WP_RL - 1529 dadurch auf 3,0 K steigt. 1529 steht in 0,5-K-Stufen."
  register: 1490
  wert_formel: "round(ist_1490 - 0.5, 1)"   # so lange 0,5 K tiefer, bis 1535 - 1529 = 3,0 ist; 1529 alle 30 s lesen; dann 3 min; dann noch 0,5 K tiefer
  rueckweg: auto_loxone
  fruehester_start: "2026-11-06 07:00"
  dauer_min: 8
  spaetester_rueckweg: "21:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa, So]      # Chat 08.11. 11:05: der Betreiber "du kannst dich austoben", So ausserhalb 12-18 erlaubt
  sperrfenster: ["So 12:00-18:00 (ausser 2026-11-08: der Betreiber im Chat 11:20 'fuer heute kannst du ganz normal testen')"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 0", "r(1539) == 1", "heizlauf_seit_mindestens_10_min", "r(1500) >= 46.0", "kein_experiment_aktiv", "whitelist_enthaelt(1490)"]
  messgroessen: [1490, 1529, 1535, 1539, 25611, WP_RL]
  beobachtete_regeln: [H01]
  abbruch: ["r('1534') != 255", "r('1500') < 42.0"]
  status: abgebrochen
  ergebnis: "Nicht entschieden [sicher, n = 1]: Loxone schreibt 1490 etwa alle 3 min auf sein Soll zurueck (17:55:3x und zwischen 17:58:31 und 17:59:02 jeweils 30,6), dazwischen hielten 0,5-K-Schritte (schreib_pruefung haelt). 1529 folgte 1490 + 2,0 K mit 30-60 s Verzug; bis zum Rueckschreiben reichte es nur fuer 1535 - 1529 = 2,5 K (17:58:3x, 1535 32,5 / 1529 30,0), kein Stopp (1539 = 1, P_el 1,70-1,72 kW). Was bringt uns das: Schrittweises Absenken ist gegen den 3-min-Takt von Loxone zu langsam; Nachfolger E10b springt direkt nach einem Loxone-Rueckschreiben in einem Schritt auf 1529 = 1535 - 3,0."
  protokoll: "OR 08.11. 17:54-17:59: Voraussetzungen live 1534 255, 1477 3,9, 1504 0, 1539 1, Heizlauf seit 17:40 (P_el), 1500 51,5, keine experiment_aktiv.json, 1490 in Whitelist; Sonntagssperre heute aufgehoben. Start 1490 30,5 / 1529 32,5 / 1535 31,5. 17:55:0x 1490 30,0 (haelt); 17:55:4x 30,0 -> Loxone 30,6 vorher, geschrieben 29,5 (haelt); 17:56:04 1529 32,0 / 1535 32,0; 17:56:3x 29,0; 17:56:43 1529 31,5; 17:57:1x 28,5; 17:57:19 1529 31,0; 17:57:5x 28,0; 17:57:55 1529 30,5; 17:58:2x 27,5; 17:58:31 1529 30,0 / 1535 32,5 (Abstand 2,5); 17:59:02 1490 30,6 (Loxone), 1529 32,5, 1539 1; P_el 17:59 2,11. Rueckweg = Loxone-Wert 30,6 bestaetigt, Pi-Datei 17:59 geloescht."
- id: E10b
  titel: "(E10 in einem Sprung) Stoppschwelle: stoppt die WP erst bei 1535 - 1529 > 3,0 K?"
  hypothese: "Die WP stoppt, sobald WP_RL (Prometheus, 0,1 K) - 1529 rund 3,0 K erreicht (MD-78: 3,0-3,1 K in 90 von 101 Stopps); ein 1490-Schritt, der 1529 um 0,5 K senkt, stoppt sie also binnen 1 min, wenn WP_RL - 1529 dadurch auf 3,0 K steigt. 1529 steht in 0,5-K-Stufen."
  register: 1490
  wert_formel: "round(ist_1535 - 3.0 - 2.0, 1)"   # ein Sprung direkt nach einem Loxone-Rueckschreiben (1490 springt auf Loxone-Wert), 1529 = 1490 + 2,0 K -> 1535 - 1529 = 3,0; 1529/1539/P_el alle 30 s bis zum naechsten Loxone-Rueckschreiben (~3 min)
  rueckweg: auto_loxone
  fruehester_start: "2026-11-09 07:00"
  dauer_min: 8
  spaetester_rueckweg: "21:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa, So]      # Chat 08.11. 11:05: der Betreiber "du kannst dich austoben", So ausserhalb 12-18 erlaubt
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 0", "r(1539) == 1", "heizlauf_seit_mindestens_10_min", "r(1500) >= 46.0", "kein_experiment_aktiv", "whitelist_enthaelt(1490)"]
  messgroessen: [1490, 1529, 1535, 1539, 25611, WP_RL]
  beobachtete_regeln: [H01]
  abbruch: ["r('1534') != 255", "r('1500') < 42.0"]
  status: abgeschlossen
  ergebnis: "Bestaetigt [sicher fuer n = 1]: 1490 33,1 -> 28,0 (1529 35,0 -> 30,0 erwartet, WEZ-Register zeigte nach dem Stopp 0) liess den Verdichter 60-75 s nach dem Schreiben stoppen (P_el 1,75 -> 0 und wez_status 1 -> 0 zwischen 07:57:27 und 07:57:42), WP_RL stand dabei 33,0-33,1, also 3,0-3,1 K ueber dem neuen 1529. Loxone schrieb 1490 bis 07:59:5x auf 33,1 zurueck, die WP blieb aus. Was bringt uns das: Die Stoppschwelle WP_RL - 1529 >= 3,0 K (H01, MD-78) ist jetzt auch per Eingriff belegt; Loxone kann einen Heizlauf ueber einen einzigen 1490-Sprung gezielt beenden (z. B. vor einer WW-Ladung oder bei PV-Ende)."
  protokoll: "OR 09.11. 07:55-08:00 (Pi-Zeit): Voraussetzungen live 1534 255, 1477 1,4, 1504 0, 1539 1, Heizlauf seit 07:30 (hoval_p_el_kw), 1500 51,0, keine experiment_aktiv.json, 1490 in Whitelist. Vorher 1490 33,1, 1529 35,0, 1535 33,0, P_el 1,75, Modulation 35 %. ~07:56:30 write 1490 = 280; schreib_pruefung 07:56:45 haelt. 07:56:42 experiment_aktiv.json auf dem Pi. 07:57:42 P_el 0, wez_status 0; MCP danach 1539 0, 1529 0. WP_RL 07:57:27 33,0, 07:58:57 32,7. 07:58:5x 1490 noch 28,0, ~07:59:55 1490 33,1 (Loxone). Rueckweg = Loxone-Wert bestaetigt, Pi-Datei geloescht."
  angelegt: "OR 08.11.2026 18:00 (R9 Vorrat, aus E10-Versuch: Loxone-Takt 3 min zu kurz fuer 0,5-K-Schritte)"
- id: E11
  titel: "Verstaerkung: wie viel % Modulation je K Soll-Sprung?"
  hypothese: "+4 K bringen rund 10 %-Punkte Modulation (E9: +2 K ergab +5), direkt nach dem Loxone-Rueckschreiben gestartet, damit die Antwort ungestoert bleibt."
  register: 1490
  wert_formel: "min(40.0, round(ist_1490 + 4.0, 1))"
  rueckweg: auto_loxone
  fruehester_start: "2026-11-06 07:00"
  dauer_min: 6
  spaetester_rueckweg: "21:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 0", "r(1539) == 1", "heizlauf_seit_mindestens_10_min", "kein_experiment_aktiv", "whitelist_enthaelt(1490)"]
  messgroessen: [1490, 18726, 25611, WP_VL]
  abbruch: ["r('1534') != 255", "r('1500') < 42.0"]
  status: abgeschlossen
  ergebnis: "+4 K auf 1490 um 08:13:40 hob die Modulation binnen hoechstens 65 s von 47 auf 59 % (P_el 2,29 auf 3,02 kW), das sind 3 %-Punkte je K [sicher fuer 1 Flanke]. Ab 08:15:45 wieder 47 %, Loxone hatte 1490 spaetestens 08:17:10 zurueck auf 33,1, also frueher als die vorgesehenen 5 min [Rueckschreibzeit Vermutung]. Regeln: kein Statuswechsel, Fehler 255."
- id: E12
  titel: "WW-Start auf Zuruf: startet 1497 = 1500 + 5,5 K eine Ladung, und laeuft sie nach dem Rueckschreiben weiter?"
  hypothese: "1504 geht binnen 1 min auf 1, der Verdichter laeuft binnen 3 min (Sperre abgelaufen). Nach dem Loxone-Rueckschreiben auf 50 laeuft die Ladung weiter, solange 1500 unter 50 liegt."
  register: 1497
  wert_formel: "min(53.0, round(ist_1500 + 5.5, 1))"
  rueckweg: auto_loxone
  fruehester_start: "2026-11-06 10:00"
  dauer_min: 6
  spaetester_rueckweg: "16:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 0", "r(1539) == 0", "letzter_verdichterstopp_vor_mindestens_16_min", "r(1500) >= 44.0", "r(1500) <= 48.0", "kein_experiment_aktiv", "whitelist_enthaelt(1497)"]
  messgroessen: [1497, 1499, 1500, 1504, 1539, 25611]
  abbruch: ["r('1534') != 255", "r('1500') < 42.0"]
  status: abgeschlossen
  ergebnis: "1497 = 53,0 (WW oben 47,6) um rund 10:01:10: SLP 10:01:21, WW_Status 1 10:01:31, Verdichter 10:02:12, also Start binnen hoechstens 62 s [sicher fuer 1 Fall]. Loxone schrieb 1497 um 10:01:51 zurueck auf 50,0; 10:06:30 lief die Ladung weiter (1504 = 1, 1539 = 4, 1500 = 47,5) [sicher fuer 1 Fall]. Regeln: kein Statuswechsel, Fehler 255."
- id: E13
  titel: "WW in den Heizlauf: wechselt die WP direkt, wenn 1497 die Startschwelle kreuzt?"
  hypothese: "1497 = 1500 + 5,5 K im Heizlauf setzt 1504 binnen 1 min auf 1, und die WP wechselt ohne Verdichterstopp auf WW (F114: 22 Faelle direkt, 12 mit Stopp). Falsch, wenn sie stoppt und 15 min sperrt."
  register: 1497
  wert_formel: "min(53.0, round(ist_1500 + 5.5, 1))"
  rueckweg: auto_loxone
  fruehester_start: "2026-11-06 10:00"
  dauer_min: 6
  spaetester_rueckweg: "16:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 0", "r(1539) == 1", "heizlauf_seit_mindestens_10_min", "r(1500) >= 44.0", "r(1500) <= 48.0", "kein_experiment_aktiv", "whitelist_enthaelt(1497)"]
  messgroessen: [1497, 1499, 1500, 1504, 1539, 25611, WP_VL]
  abbruch: ["r('1534') != 255", "r('1500') < 42.0"]
  status: abgeschlossen
  ergebnis: "Bestaetigt [sicher, n = 1]: 1497 07:00:13 auf 52,3 (= 1500 46,8 + 5,5) im Heizlauf seit 06:44:30, schreib_pruefung 07:00:28 haelt; 1504 = 1 um 07:00:28 (Prometheus ww_status ab 07:00:45), 1539 1 -> 4 ab 07:01:15, P_el ohne Einbruch 1,71 -> 2,66 -> 5,85 kW, also Wechsel auf WW ohne Verdichterstopp und ohne 15-min-Sperre (passt zu F114). Loxone schrieb 1497 zwischen 07:00:28 und 07:01:51 auf 50,0 zurueck, die WW-Ladung lief danach bis zum Soll 50 weiter (Nebenwirkung: Morgenladung ~20 min frueher). Was bringt uns das: Ein kurzer 1497-Impuls im Heizlauf startet WW nahtlos, Loxone kann so eine WW-Ladung an einen laufenden Heizlauf haengen und einen eigenen Verdichterstart sparen."
  protokoll: |
    07.11.2026 07:00:05 Voraussetzungen live: 1534 255, 1477 2,9, 1504 0, 1539 1 (Lauf seit 06:44:30 laut Prometheus p_el), 1500 46,8, keine experiment_aktiv.json, 1497 in Whitelist
    07:00:13 write_register(1497, 523, confirm) - vorher 500; 07:00:28 schreib_pruefung haelt 523; 1504 = 1
    07:01:20 experiment_aktiv.json auf dem Pi; 07:01:3x 1539 4, 1499 52,3, 25611 1,71, 1497 52,3
    07:01:5x 1497 50,0 (Loxone-Rueckweg), 1500 46,7, 1539 4
    Prometheus 15 s (06:58-07:06): wez_status 1 bis 07:01:00, 4 ab 07:01:15; ww_status 1 ab 07:00:45; p_el 1,71 -> 2,66 (07:01:15) -> 5,85 -> 4,0-5,6 kW
    07:06:53 experiment_aktiv.json auf dem Pi geloescht (R6), Rueckweg = Loxone-Wert 50,0 bestaetigt
- id: E22
  titel: "Wiederholung E13 (n = 2): WW-Impuls 1497 im Heizlauf zu anderer Tageszeit"
  hypothese: "Wie E13: 1497 = 1500 + 5,5 K im Heizlauf setzt 1504 binnen 1 min auf 1, die WP wechselt ohne Verdichterstopp auf WW. Falsch, wenn sie stoppt und 15 min sperrt."
  register: 1497
  wert_formel: "min(53.0, round(ist_1500 + 5.5, 1))"
  rueckweg: auto_loxone
  fruehester_start: "2026-11-07 12:00"
  dauer_min: 6
  spaetester_rueckweg: "16:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 0", "r(1539) == 1", "heizlauf_seit_mindestens_10_min", "r(1500) >= 44.0", "r(1500) <= 48.0", "kein_experiment_aktiv", "whitelist_enthaelt(1497)"]
  messgroessen: [1497, 1499, 1500, 1504, 1539, 25611, WP_VL]
  abbruch: ["r('1534') != 255", "r('1500') < 42.0"]
  status: abgeschlossen
  ergebnis: "Bestaetigt [sicher, n = 2 mit E13]: 1497 12:00:00 auf 51,9 (= 1500 46,4 + 5,5) im Heizlauf seit 11:42, schreib_pruefung haelt; WW_Status 1 ab 12:00:15 (Prometheus), wez_status 1 -> 4 ab 12:00:45, P_el 1,72 -> 1,68 -> 5,21 kW ohne Einbruch auf 0, also Wechsel auf WW ohne Verdichterstopp und ohne 15-min-Sperre, auch mittags. Loxone schrieb 1497 zwischen 12:01:41 und 12:02:02 auf 50,0 zurueck (ww_hires WW_Soll 500 ab 12:02:02), die Ladung lief weiter (12:04:30 Status 4, P_el 4,6 kW). Was bringt uns das: das nahtlose WW-Anhaengen per 1497-Impuls ist reproduzierbar; ob es sich netto lohnt, klaert MD-130 (F205), erst dann ein Loxone-Vorschlag."
  protokoll: |
    07.11.2026 12:00:09 Voraussetzungen live: 1534 255, 1477 6,0, 1504 0, 1539 1 (Heizlauf seit 11:42 laut Prometheus p_el/wez_status), 1500 46,4, keine experiment_aktiv.json, 1497 in Whitelist (Hand-Modus-Test beendet, 1497 = 50,0 um 11:55)
    12:00:00 write_register(1497, 519, confirm) - vorher 500; schreib_pruefung haelt 519; 12:00:42 experiment_aktiv.json auf dem Pi; 1504 = 1
    12:01:4x 1539 4, 1497 51,9; 12:02:35 1497 50,0 (Loxone-Rueckweg, ww_hires ab 12:02:02)
    Prometheus 15 s (11:58-12:04:30): wez_status 1 bis 12:00:30, 4 ab 12:00:45; ww_status 1 ab 12:00:15; p_el 1,69-1,72 -> 1,68 (12:00:45) -> 5,21 (12:01:15) -> 4,5-5,4 kW
    12:04:44 experiment_aktiv.json auf dem Pi geloescht (R6), Rueckweg = Loxone-Wert 50,0 bestaetigt
- id: E23
  titel: "WW-Impuls im Heizlauf bei Kaelte (1477 < 3 C): wechselt die WP auch dann nahtlos?"
  hypothese: "Wie E13/E22 (n = 2, beide bei 3-6 C): 1497 = 1500 + 5,5 K im Heizlauf setzt 1504 binnen 1 min auf 1 und die WP wechselt ohne Verdichterstopp auf WW. MD-124 zeigt fuer < 3 C hoeheren kWh_el/K beim Anhaengen (n = 2); falsch, wenn sie bei Kaelte stoppt oder vorher abtaut."
  register: 1497
  wert_formel: "min(53.0, round(ist_1500 + 5.5, 1))"
  rueckweg: auto_loxone
  fruehester_start: "2026-11-08 07:00"
  dauer_min: 6
  spaetester_rueckweg: "21:00"      # OR 08.11. 10:56: 16:00 -> 21:00 (R9 17:00-Grenze: Kurzversuch 1497 auto_loxone darf 07-21), damit E23 sonntags ab 18:00 laufen kann
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa, So]
  sperrfenster: ["So 12:00-18:00 (ausser 2026-11-08: der Betreiber im Chat 11:20 'fuer heute kannst du ganz normal testen')"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1477) < 3.0", "r(1504) == 0", "r(1539) == 1", "heizlauf_seit_mindestens_10_min", "r(1500) >= 44.0", "r(1500) <= 48.0", "kein_experiment_aktiv", "whitelist_enthaelt(1497)"]
  messgroessen: [1497, 1499, 1500, 1504, 1539, 25611, WP_VL]
  beobachtete_regeln: [S02, S03, W01]
  abbruch: ["r('1534') != 255", "r('1500') < 42.0"]
  status: abgebrochen
  ergebnis: "16.11.2026 09:00:54 gefahren (1497 = 53,0, SET im Setlog), aber Hypothese NICHT geprueft: der Heizlauf endete von selbst zwischen 08:58 und 08:59 (P_el 1,91 -> 0,0), also ~2 min VOR dem Schreiben; Voraussetzung 'Heizlauf' war beim Schreiben veraltet (zuletzt 08:57 gelesen). Folge wie E12 aus dem Stillstand: 1504 = 1 binnen <= 20 s, WP in Wiedereinschaltverzoegerung (Code 16), HK1/HK2 Zwangsdrosselung WW-Vorrang. Rueckweg Loxone 09:05:35, 1497 = 50,0 gelesen 09:05:49. Wiederholung als E36 (mit P_el-Pruefung < 30 s vor dem Schreiben)."
  angelegt: "OR 07.11.2026 12:05 (R9 Vorrat, aus E22 + MD-124 Klasse < 3 C)"
- id: E24
  titel: "WW-Ladeende: endet eine laufende Ladung, wenn 1497 unter 1500 gesenkt wird?"
  hypothese: "1497 = 42,0 bei 1500 = 43,3 waehrend einer Normal-Ladung beendet die Ladung binnen 2 min (1504 -> 0)."
  register: 1497
  wert: 42.0
  rueckweg: auto_loxone
  fruehester_start: "2026-11-08 11:15"
  dauer_min: 8
  spaetester_rueckweg: "11:30"
  erlaubte_tage: [So]
  sperrfenster: []
  voraussetzungen: ["r(1534) == 255", "r(1504) == 1", "r(1500) >= 42.5", "kein_experiment_aktiv", "whitelist_enthaelt(1497)"]
  messgroessen: [1497, 1499, 1500, 1504, 1530, 25611, 18726]
  beobachtete_regeln: [W01, S02, S03]
  abbruch: ["r('1534') != 255", "r('1500') < 42.0"]
  status: abgeschlossen
  ergebnis: "08.11.2026 11:18:51 1497 = 42,0 geschrieben, schreib_pruefung haelt, 1499 folgte sofort auf 42,0, 1530 (Speicher-Soll) auf 46,0 (= 1499 + 4 K). Die Ladung lief trotzdem weiter: 1504 = 1 durchgehend, P_el 4,34 -> 4,23 -> 4,09 kW, 1500 43,3 -> 43,9 -> 44,0, also bis 2,0 K ueber dem WW-Soll. Loxone schrieb 1497 bis spaetestens 11:21:20 auf 52,0 zurueck (Rueckweg < 2,5 min). Hypothese widerlegt [sicher fuer n = 1, Fenster 2,5 min]: Das Ladeende haengt nicht an 1500 >= 1499, wahrscheinlich an 1500 >= 1530 (= 1499 + 4 K) oder am WEZ-Vorlauf. Was bringt uns das: Eine laufende Ladung laesst sich nicht per Soll-Absenkung sofort abbrechen; eine Ladung endet erst rund 4 K ueber dem WW-Soll."
  angelegt: "Claude im Chat 08.11.2026 11:18 (der Betreiber: 'ab jetzt kannst du testen wie du willst')"
- id: E25
  titel: "Kuehl-Soll 19482 bei Regelstrategie 3 und Betriebswahl Konstant (1478 = 4) im Heizwinter: reagiert die WEZ ueberhaupt?"
  hypothese: "Solange die zentrale Betriebsart Heizen ist, bewirkt 19482 = 18,0 nichts: kein Umschalten Kuehlventil (19870 bleibt 0), 1539 nie 2, 18763 bleibt 0. Widerlegt, wenn 19870 = 1 oder 1539 = 2 oder 18763 = 15,0 binnen 5 min. Nebenfrage: schreibt Loxone 19482 binnen 5 min auf 0 zurueck?"
  register: 19482
  wert: 18.0
  rueckweg: 0.0
  fruehester_start: "2026-11-08 11:25"
  dauer_min: 8
  spaetester_rueckweg: "21:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa, So]
  sperrfenster: ["So 12:00-18:00 (ausser 2026-11-08)"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 0", "r(1539) != 8", "r(19482) == 0.0", "kein_experiment_aktiv", "whitelist_enthaelt(19482)"]
  messgroessen: [19482, 18763, 19870, 1501, 1539, 25611, 1525]
  beobachtete_regeln: []
  abbruch: ["r('1534') != 255", "r('1539') == 2"]   # OR 08.11. 13:56: Ausdruck repariert (Waechter 13:50 'invalid syntax'); gemeint war 1539 = 2 laenger als 2 min -> sofort Rueckweg 0,0
  status: abgebrochen
  ergebnis: "Hypothese widerlegt [sicher, n = 1]: 19482 = 18,0 (12:55:27 geschrieben, schreib_pruefung haelt) startete im Heizwinter bei 27510 = 3/1478 = 4 echten Kuehlbetrieb: 18763 sofort 16,0, ab 12:57 19870 = 1 (Kuehlventil), 1539 51 -> 2, P_el 0,95-1,11 kW, WP-Vorlauf 1525 45,0 -> 20,5 C. Abbruchkriterium 1539 = 2 > 2 min erfuellt (12:58-13:00), Rueckweg 19482 = 0,0 13:02:25, schreib_pruefung haelt; 13:03:32 1539 = 0, 19870 = 0, P_el 0. Nebenfrage: Loxone schrieb 19482 in 7 min NICHT zurueck. Was bringt uns das: 19482 ist kein toter Sommerwert, jeder Wert > 0 im Winter laesst die WP kuehlen; Loxone/Whitelist-Schreiber muessen 19482 im Heizbetrieb auf 0 halten (Regelkandidat)."
  protokoll: "OR 08.11. 12:54-13:03: Voraussetzungen live 1534 255, 1477 8,0, 1504 0, 1539 0, 19482 0,0, keine experiment_aktiv.json, 19482 in Whitelist; Sonntagssperre heute aufgehoben (der Betreiber 11:20). Messung 12:56:08 1539 0, 18763 16,0, 19870 0; 12:57:08 1539 51, 19870 1; 12:58:08 1539 2, P_el 0,95; 12:59:08 2/0,97, 1525 23,0; 13:00:08 2/1,08, 1525 22,5 -> ABBRUCH; 13:02:52 noch 2/1,11; 13:03:32 0/0, 1525 23,5. Kuehllauf ~12:58-13:03 (~5 min, < 0,1 kWh)."
  angelegt: "Claude im Chat 08.11.2026 11:25 (der Betreiber: '19482 bei Regelstrategie 3 steht glaub ich noch offen')"
- id: E14
  titel: "Heizanforderung in der Sperre: zeigt 1539 = 16 auch sie?"
  hypothese: "Ein 1490 ueber Ruecklauf + 2 K in den ersten 8 min nach einem Verdichterstopp setzt 1539 binnen 1 min auf 16, kein Start vor Sperrende. Falsch, wenn 1539 auf 0 bleibt (dann zeigt 16 nur WW, wie in E4)."
  register: 1490
  wert_formel: "min(40.0, round(ist_Ruecklauf + 2.0, 1))"
  rueckweg: auto_loxone
  fruehester_start: "2026-11-06 10:00"
  dauer_min: 6
  spaetester_rueckweg: "21:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 0", "r(1539) == 0", "letzter_verdichterstopp_vor_hoechstens_8_min", "kein_experiment_aktiv", "whitelist_enthaelt(1490)"]
  messgroessen: [1490, 1539, 25611, Ruecklauf]
  abbruch: ["r('1534') != 255", "r('1500') < 42.0"]
  status: abgeschlossen
  ergebnis: "Widerlegt [wahrscheinlich, n = 1]: Verdichterstopp 08:53:00 (Prometheus hoval_wez_status 1->0, P_el 1,92->0); 1490 um 08:57:58 von 32,6 auf 38,0 (= RL 36,0 + 2,0), schreib_pruefung 08:58:13 haelt. 1539 blieb 0 bis 09:01:16 (Prometheus 15-s-Raster bis 08:59:37 durchgehend 0, danach MCP-Lesungen), kein Start. Loxone schrieb 1490 bis 09:01 auf 32,6 zurueck (auto_loxone-Rueckweg bestaetigt), experiment_aktiv.json geloescht. Also zeigt 1539 = 16 nur die WW-Anforderung in der Sperre (wie E4), keine Heizanforderung. Was bringt uns das: fuer den Zwilling ist 1539 = 16 ein reines WW-Signal; eine Heizanforderung in der Sperre ist am Bus nicht sichtbar."
  protokoll: "OR 07.11. 08:56-09:01: Voraussetzungen live 1534 255, 1477 3,2, 1504 0, 1539 0, Stopp vor 5 min, Datei fehlte, 1490 in Whitelist."
- id: E15
  titel: "Wiederholung E6, Schreiben direkt nach dem Loxone-Raster: Heizstart 16 min nach Ruecklauf <= 1490 - 1,5 K, auch bei Soll-Sprung?"
  hypothese: "Ein Soll, das den Abstand erzeugt, startet den Heizbetrieb rund 16 min spaeter (F54), nicht sofort. Falsch, wenn er binnen 5 min startet oder bis Minute 22 nicht startet. Vorbehalt: Loxone setzt alle 5 min kurz zurueck, das kann einen Timer neu starten."
  register: 1490
  wert_formel: "min(40.0, round(ist_Ruecklauf + 2.0, 1))"   # je 5-min-Raster rund 10-20 s nach :x0/:x5 neu schreiben; Ende bei Start oder nach 22 min
  rueckweg: auto_loxone
  fruehester_start: "2026-11-06 11:00"
  dauer_min: 22
  spaetester_rueckweg: "21:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 0", "r(1539) == 0", "letzter_verdichterstopp_vor_mindestens_20_min", "Ruecklauf > r(1490) - 1.0", "kein_experiment_aktiv", "whitelist_enthaelt(1490)"]
  messgroessen: [1490, 1539, 25611, Ruecklauf]
  abbruch: ["r('1534') != 255", "r('1500') < 42.0"]
  status: abgebrochen
  ergebnis: "Abgebrochen nach R5: 1490 = 34,0 um rund 11:00:12 geschrieben, schreib_pruefung 11:00:25 las 30,5, also wieder binnen 15 s zurueck, auch direkt nach dem Raster. Kein Messwert zur Frage, 1539 blieb 0. Die Datei experiment_aktiv.json lag wegen eines parallel abgesetzten Aufrufs rund 30 s auf dem Pi, 11:00:55 entfernt. Offen als F164."

- id: E16
  titel: "Spar-WW-Soll 1498 im Konstantbetrieb: wirkt es, und wer schreibt es?"
  hypothese: "Bei 1496 = 4 (Konstant) aendert 1498 = 46 statt 45 den aktiven WW-Soll 1499 nicht, und Loxone schreibt 1498 binnen 3 min nicht zurueck. Falsch, wenn 1499 sich bewegt oder 1498 zurueckspringt."
  register: 1498
  wert: 46          # U8 ohne Dezimalstelle, Rohwert = Grad
  rueckweg: 45
  fruehester_start: "2026-11-06 11:02"
  dauer_min: 3
  spaetester_rueckweg: "16:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1496) == 4", "r(1498) == 45", "r(1504) == 0", "kein_experiment_aktiv", "whitelist_enthaelt(1498)"]
  messgroessen: [1498, 1499, 1504, 1539]
  abbruch: ["r('1534') != 255", "r('1500') < 42.0"]
  status: abgeschlossen
  ergebnis: "1498 = 46 von 11:02:11 bis 11:04:55: 1499 blieb 50,0, 1504 = 0, 1539 = 0, Fehler 255 [sicher fuer 1 Fall, Soll-Abstand kein Ladefall]. 1498 hielt 2:44 min ohne Rueckschreiben, ein 5-min-Zeitpunkt lag nicht im Fenster. Rueckweg 45 um 11:04:55, schreib_pruefung 11:05:10 haelt."
- id: E17
  hypothese: "Bei SG-Status Vorzug (27545 = 1) hebt +1 K auf 27509 das aktive Soll 1499 binnen 1 min um 1 K (Gegenstueck zu E8, dort bei Normal keine Wirkung). Falsch, wenn 1499 gleich 1497 bleibt. Keine Ladung erwartet, solange 1499 - 1500 unter 4,9 K bleibt."
  register: 27509
  wert_formel: "ist_27509 + 1.0"
  rueckweg: "vorher gelesener Wert von 27509, im Protokoll notieren"
  fruehester_start: "2026-11-06 12:00"
  dauer_min: 4
  spaetester_rueckweg: "17:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 0", "smart_grid_vorzug", "r(1499) == r(1497)", "r(1497) + 1.0 - r(1500) < 4.5", "kein_experiment_aktiv", "whitelist_enthaelt(27509)"]
  messgroessen: [27509, 27545, 1497, 1499, 1500, 1504, 1539]
  abbruch: ["r('1534') != 255", "r('1504') != 0"]
  status: abgeschlossen
  ergebnis: "27509 = 1,0 K um 12:03:11 bei SG Vorzug (27545 = 1): 1499 stand binnen hoechstens 16 s auf 53,0 (1497 blieb 52,0), keine Ladung, weil 53,0 - 50,3 unter 4,9 K [sicher fuer 1 Fall]. Rueckweg 0 um 12:05:39, schreib_pruefung haelt, Loxone schrieb in den 2:28 min nicht zurueck. Regeln: kein Statuswechsel, Fehler 255."
- id: E18
  titel: "1490 im Stillstand direkt nach einem Loxone-Schreiben: haelt der Wert bis zum naechsten Takt?"
  hypothese: "Das Bridge-Protokoll zeigt: Loxone schreibt 1490 bei jeder Aenderung seines Eingangs, sonst alle 300 s; Lauf und Stillstand haben aehnliche Abstaende (Median 241 und 222 s, 06.11.). Direkt nach einem Loxone-Schreiben geschrieben, haelt der Wert also bis zum naechsten Takt, auch im Stillstand, meist ueber 60 s. Falsch, wenn er zweimal binnen 15 s zurueckkommt, obwohl 1477 sich nicht bewegt (dann reagiert Loxone doch auf den Stillstand oder auf das Schreiben). Wert nur 0,5 K ueber Ist, damit keine Anforderung entsteht."
  register: 1490
  wert_formel: "round(ist_1490 + 0.5, 1), bei ist_1490 = 0 fest 29.0"   # Aenderung 06.11. 15:58: Bridge-Bereich 100..1100, Wert 5 abgelehnt (15:57:05, nichts angekommen); 29,0 hat Loxone selbst 15:12-15:40 geschrieben, RL 35 = keine Anforderung; nur wenn Ruecklauf > ist_1490 + 1.0; Zeitpunkt aus `journalctl -u hoval-bridge`, binnen 20 s nach einem SET reg 1490; 2 Wiederholungen
  rueckweg: auto_loxone
  fruehester_start: "2026-11-06 12:30"
  dauer_min: 10
  spaetester_rueckweg: "21:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 0", "r(1539) == 0", "letzter_verdichterstopp_vor_mindestens_20_min", "Ruecklauf > r(1490) + 1.0", "kein_experiment_aktiv", "whitelist_enthaelt(1490)"]
  messgroessen: [1490, 1477, 1539, 25611, "SET reg 1490 im Bridge-Protokoll"]
  abbruch: ["r('1534') != 255", "r('1500') < 42.0"]
  status: abgeschlossen
  ergebnis: "Im Stillstand mit Loxone-Eingang 0 bestaetigt: 1490 = 29,0 hielt zweimal bis zum naechsten Loxone-Takt, 296 und 297 s, kein Rueckkehrer unter 15 s. Das klaert E6/E15 nicht ganz, dort lag der Eingang bei 30,5 statt 0 [wahrscheinlich]. Nebenwirkung: Der Wechsel von 0 auf 29,0 schaltete HK1 ein (1501 = 23, Pumpe 19706 = 1), weil 0 keine Anforderung bedeutet; Wert 0,5 lehnte die Bridge ab."

- id: E19
  register: 27509
  wert_formel: "min(3.0, round(ist_1500 + 5.5 - ist_1499, 1))"   # nur bei SG Vorzug und wenn der Wert > 0; Rohwert x10
  rueckweg: 0
  fruehester_start: "2026-11-06 12:55"
  dauer_min: 5
  spaetester_rueckweg: "16:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 0", "r(27545) == 1", "r(27509) == 0", "r(1500) >= 47.0", "kein_experiment_aktiv", "whitelist_enthaelt(27509)"]
  messgroessen: [27509, 1499, 1500, 1504, 1539, 25611]
  abbruch: ["r('1534') != 255", "r('1500') < 42.0", "r('27545') != 1"]
  status: abgeschlossen
- id: E20
  hypothese: "Der Pufferfuehler (62/63) ist nicht in Betrieb, der Heizkreis laeuft ueber 1490 + 07-001. 28839 = +2,0 K im Heizlauf bei SG Vorzug laesst 1529 und die Modulation unveraendert. Falsch, wenn 1529 binnen 2 min steigt, ohne dass 1490 sich aendert; dann haette Loxone bei Vorzug einen Heizhebel ohne 1490, was wichtig waere, weil 27528 tot ist."
  register: 28839
  wert: 2.0
  rueckweg: 0
  fruehester_start: "2026-11-06 13:55"
  dauer_min: 4
  spaetester_rueckweg: "21:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 0", "r(1539) == 1", "r(27545) == 1", "r(28839) == 0", "kein_experiment_aktiv", "whitelist_enthaelt(28839)"]
  messgroessen: [28839, 1490, 1529, 1535, 1539, 25611, Modulation]
  abbruch: ["r('1534') != 255", "r('1500') < 42.0", "r('27545') != 1"]
  status: abgebrochen
  ergebnis: "Nicht gefahren, keine Aussage zur Hypothese. Die Bridge lehnte beide Schreibvorgaenge ab (noch nie vom CAN gelesen, Cache kalt), an der Anlage kam nichts an. write_register und schreib_pruefung meldeten trotzdem ok und haelt."
- id: E21
  titel: "1529-Stufe: kippt 1490 von x,9 auf x,0 das Heizsoll um 0,5 K?"
  hypothese: "1529 = abgerundet auf 0,5 K von 1490 + 07-001 (Volllogger 05.-06.11.: 142 von 143 Zeilen, die eine ist E11). Bei 07-001 = 2,0: 1490 = 35,9 laesst 1529 auf 37,5, 1490 = 36,0 hebt es auf 38,0. Falsch, wenn 35,9 schon 38,0 ergibt (dann rundet die Hoval) oder 36,0 bei 37,5 bleibt."
  register: 1490
  wert_formel: "35,9, dann 36,0, je mindestens 65 s (WEZ-Register bis 60 s alt)"
  rueckweg: auto_loxone
  fruehester_start: "2026-11-06 14:58"
  dauer_min: 5
  spaetester_rueckweg: "21:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 0", "r(1539) == 1", "r(1490) == 35.8", "kein_experiment_aktiv", "whitelist_enthaelt(1490)"]
  messgroessen: [1490, 1529, 1539, 25611, Modulation, "SET reg 1490 im Bridge-Protokoll"]
  beobachtete_regeln: [H01]
  abbruch: ["r('1534') != 255", "r('1500') < 42.0", "r(1539) != 1"]
  status: abgeschlossen
  ergebnis: "Bestaetigt. 1490 = 35,9 liess 1529 auf 37,5, 1490 = 36,0 hob es binnen hoechstens 59 s auf 38,0; nach dem Rueckweg ging es wieder auf 37,5. Damit gilt 1529 = 1490 + 07-001, auf 0,5 K abgerundet [sicher: 1 Versuch plus 142 von 143 Volllogger-Zeilen]. Die Modulation stieg nur von 35 auf 36 %, kein Stopp."
- id: E26
  titel: "WW-Ladeende: bricht eine laufende Ladung ab, wenn 1530 (= 1497 + 4 K) unter 1500 faellt?"
  hypothese: "Aus E24 (n = 1): Ladeende = 1500 >= 1530. Setzt man 1497 = 1500 - 4,5 K (dann 1530 = 1500 - 0,5), endet 1504 binnen 2 min. Widerlegt, wenn 1504 mindestens 4 min auf 1 bleibt, obwohl 1530 < 1500."
  register: 1497
  wert_formel: "max(40.0, round(ist_1500 - 4.5, 1))"
  rueckweg: auto_loxone
  fruehester_start: "2026-11-09 07:00"
  dauer_min: 8
  spaetester_rueckweg: "21:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa, So]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 1", "r(1500) >= 44.5", "r(1500) <= 50.0", "kein_experiment_aktiv", "whitelist_enthaelt(1497)"]
  messgroessen: [1497, 1499, 1500, 1504, 1530, 25611, 18726]
  beobachtete_regeln: [W01, S02, S03]
  abbruch: ["r('1534') != 255", "r('1500') < 40.0"]
  status: abgeschlossen
  protokoll: "OR 09.11. 18:52-18:58 (MCP + ww_hires 10 s, Pi-Zeit): Ladung seit 18:52:22 (Loxone 1497 50->57 um 18:52:12, Abendlage, kein PV), Verdichter ab 18:53. Voraussetzungen live 1534 255, 1477 4,9, 1504 1, 1500 48,8, keine Datei, 1497 in Whitelist. ~18:55:00 write 443 (44,3), schreib_pruefung 18:55:08 haelt. 18:55:32 Speicher_Sollwert 1530 61,0 -> 48,0, WW_Ist 48,8 -> 48,3 bis 18:57:31: 1530 rund 2:00 min unter 1500. WW_Status blieb 1, SLP 1, Modulation 42 -> 79 %, P_el 2,1 -> 4,6 kW (Startrampe wie E12). Loxone schrieb 52,0 um 18:57:11 zurueck (2:10 nach dem Schreiben), 1530 ab 18:57:41 = 56,0. Pi-Datei 18:58:40 entfernt."
  ergebnis: "Hypothese nicht bestaetigt (n = 1): 1530 lag 2 min unter 1500, die Ladung lief ungebremst weiter; das 4-min-Widerlegungskriterium wurde nicht erreicht, weil Loxone nach 2:10 min zurueckschrieb. Nebenbefund [sicher, 3 Werte]: 1530 = 1497 + 4 K auf 0,5 K abgerundet (44,3 -> 48,0; 52 -> 56; 57 -> 61). Loxone schrieb 57 um 18:52:12 ohne PV (Abendfenster?), zu S03. Was bringt uns das: 1530 >= 1500 ist als Ladeende-Kriterium (E24) fraglich; Wiederholung E29 mit vollem 5-min-Fenster."
  angelegt: "OR 08.11.2026 16:56 (R9 Vorrat, aus E24-Ergebnis und F250/MD-179). Was bringt uns das: klaert das Abbruchkriterium der WW-Ladung; Grundlage, um Ladungen per 1497 gezielt kurz zu halten."
- id: E27
  titel: "Gegenprobe zu E26: laeuft die Ladung weiter, wenn 1530 knapp ueber 1500 bleibt?"
  hypothese: "1497 = 1500 - 3,5 K (1530 = 1500 + 0,5) beendet die Ladung NICHT binnen 4 min (1504 bleibt 1, 1500 steigt weiter). Widerlegt, wenn 1504 binnen 4 min auf 0 geht (dann ist das Kriterium nicht 1530)."
  register: 1497
  wert_formel: "max(40.0, round(ist_1500 - 3.5, 1))"
  rueckweg: auto_loxone
  fruehester_start: "2026-11-09 07:00"
  dauer_min: 6
  spaetester_rueckweg: "21:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa, So]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 1", "r(1500) >= 44.5", "r(1500) <= 50.0", "kein_experiment_aktiv", "whitelist_enthaelt(1497)"]
  messgroessen: [1497, 1499, 1500, 1504, 1530, 25611, 18726]
  beobachtete_regeln: [W01, S02, S03]
  abbruch: ["r('1534') != 255", "r('1500') < 40.0"]
  status: abgeschlossen
  protokoll: "OR 15.11. 10:57-11:03 (MCP, Pi-Zeit): Ladung lief seit ~10:5x (1504 1, WP WW-Laden 3,2 kW el, Mod 48 %). Voraussetzungen live 1534 255, 1477 1,7, 1504 1, 1500 46,1, 1497 50,0, keine Datei, 1497 in Whitelist; Loxone-SET 500 um 10:57:27. 10:57:39 write 426 (42,6 = 1500 - 3,5), Schreibprotokoll SET 426 angenommen, schreib_pruefung 10:57:55 haelt. 10:58:10 1504 = 0, 1530 noch 54,0 (Sweep), 1500 46,3, P_el 3,32 (WEZ-Register bis 60 s alt). 10:59:20 WP Aus, P_el 0, 1530 = 0,0, WW-Status Aus, 1500 46,4. 11:02:27 Loxone-SET 500, 11:02:40 1497 50,0, 1504 0, 1500 46,9 (kein Neustart, Delta 3,1 < 4,9 K). Pi-Datei 11:02:50 entfernt."
  ergebnis: "Hypothese widerlegt (n = 1): 1497 = 1500 - 3,5 K beendet die laufende Ladung binnen <= 31 s (1504 1 -> 0), obwohl 1530 = 1497 + 4 (46,5) knapp ueber 1500 lag. Ladeende-Kriterium ist also nicht 1530 >= 1500, sondern wahrscheinlich 1500 >= 1497 (wie E7/E32; E26 bleibt der Ausreisser). Was bringt uns das: Loxone kann eine laufende Ladung per 1497 knapp unter Ist sicher abbrechen; die Ladung endet dann mit ~46-47 C und startet erst wieder bei 1497 - 4,9 K (W01). Gegenprobe E34 (1497 = 1500 + 0,5)."
  angelegt: "OR 08.11.2026 16:56 (R9 Vorrat, Kontrollversuch zu E26; nicht am selben Ladevorgang wie E26)."
- id: E28
  titel: "(E10b Wiederholung, n = 2) Wiederanlauf nach erzwungenem Stopp: wie lange bleibt die WP aus?"
  hypothese: "Nach einem per 1490-Sprung erzwungenen Stopp (WP_RL - 1529 >= 3,0 K, H01) startet die WP fruehestens 15 min spaeter (HKA59 Einschaltverzoegerung), auch wenn Loxone 1490 binnen ~3 min zurueckschreibt. Vorbefund E10b: Stopp 07:57:42, Wiederanlauf 08:16 = rund 18 min (Prometheus p_el_kw 1-min-Raster). Widerlegt, wenn die WP nach dem Rueckschreiben binnen < 12 min wieder startet."
  register: 1490
  wert_formel: "round(ist_1535 - 3.0 - 2.0, 1)"   # wie E10b; Start direkt nach einem Loxone-Rueckschreiben
  rueckweg: auto_loxone
  fruehester_start: "2026-11-09 10:00"
  dauer_min: 8
  spaetester_rueckweg: "21:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa, So]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 0", "r(1539) == 1", "heizlauf_seit_mindestens_10_min", "r(1500) >= 46.0", "kein_experiment_aktiv", "whitelist_enthaelt(1490)"]
  messgroessen: [1490, 1529, 1535, 1539, 25611, WP_RL]
  nachbeobachtung: "p_el_kw (Prometheus) bis zum Wiederanlauf, max. 30 min, nur lesen; Wiederanlaufzeit und 1490/1529 beim Start notieren"
  beobachtete_regeln: [H01]
  abbruch: ["r('1534') != 255", "r('1500') < 42.0"]
  status: abgeschlossen
  protokoll: "OR 09.11. 10:55-11:02 (MCP + Prometheus 1 min): Voraussetzungen live 1534 255, 1477 3,5, 1504 0, 1539 1, Heizlauf seit 10:37 (P_el 1,73), 1500 48,1, 1535 32,5, 1529 32,5, 1490 30,8 (Loxone), keine Datei, 1490 in Whitelist. ~10:56:00 write 275 (27,5), schreib_pruefung 10:56:12 haelt. 10:57:14 1529 30,0, RL 33,0, 1539 1. 10:58 P_el 0 (Prometheus), 10:58:05 1539 0. 1490 noch 27,5 um 11:00:08; Loxone-Rueckschreiben 30,7 zwischen 11:00:08 und 11:01:10 (~4-5 min, langsamer als E10b ~2 min). Pi-Datei 11:02 entfernt."
  ergebnis: "Teil 1 bestaetigt H01 (n = 2): Stopp 1-2 min nach dem Sprung bei WP_RL - 1529 = 3,0 K. Teil 2 (OR 09.11. 11:56, Prometheus hoval_p_el_kw 1-min-Raster, nur gelesen): P_el 0 ab 10:59, Wiederanlauf 11:28 (2,11 kW), also rund 30 min Pause nach dem Stopp (E10b: 19 min). Hypothese >= 15 min bestaetigt (n = 2), Pause streut 19-30 min [wahrscheinlich; Ursache der Streuung offen, Startsperre HKA59 + Bedarf]. Danach Nullstellen 11:36-11:37 und 11:42-11:48 [nicht geprueft, Vermutung Takt/Abtauung]. Loxone schrieb diesmal erst nach ~4-5 min zurueck. Nebenbefund Waechter: die Abbruchausdruecke in experiment_aktiv.json standen ohne Anfuehrungszeichen (r(1534) statt r('1534')) und waren fuer den Waechter ungueltig; Abbruch war waehrend E28 also nicht ueberwacht (1534 blieb 255). Was bringt uns das: ein Loxone-Stopp per 1490 kostet 20-30 min Heizpause; vor einer WW-Ladung ist das brauchbar, als Taktbremse teuer."
  angelegt: "OR 09.11.2026 09:56 (R9 Vorrat < 3; aus E10b-Nachlauf und F17/MD-183). Was bringt uns das: zeigt, ob ein gezielter Loxone-Stopp die naechste Startsperre von ~15 min mitbringt; noetig, bevor Loxone Heizlaeufe vor WW-Ladungen gezielt beendet."
- id: E29
  titel: "(E26 Wiederholung mit vollem Fenster) WW-Ladeende bei 1530 < 1500 ueber 4 min?"
  hypothese: "Eine laufende Ladung endet NICHT, wenn 1530 (= 1497 + 4 K, auf 0,5 K abgerundet) unter 1500 liegt; E26 lief 2 min so weiter. Bestaetigt, wenn 1504 mindestens 4 min auf 1 bleibt, obwohl 1530 < 1500 (ww_hires Speicher_Sollwert/WW_Ist); widerlegt, wenn 1504 in dieser Zeit auf 0 geht."
  register: 1497
  wert_formel: "max(40.0, round(ist_1500 - 4.5, 1))"
  schreibzeit: "knapp nach einem Loxone-Rueckschreiben (E26: 18:52:12 und 18:57:11, also ~:x2:15 bzw. ~:x7:15), damit das Fenster ~5 min haelt"
  rueckweg: auto_loxone
  fruehester_start: "2026-11-10 07:00"
  dauer_min: 8
  spaetester_rueckweg: "21:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa, So]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 1", "r(1500) >= 44.5", "r(1500) <= 50.0", "kein_experiment_aktiv", "whitelist_enthaelt(1497)"]
  messgroessen: [1497, 1499, 1500, 1504, 1530, 25611]
  beobachtete_regeln: [W01, S02, S03]
  abbruch: ["r('1534') != 255", "r('1500') < 40.0"]
  status: abgeschlossen
  protokoll: "OR 12.11. 17:05-17:10 (MCP + Bridge-Journal, Pi-Zeit): Ladung durch Loxone ausgeloest (1497 520 um 17:00:00, Abendfenster; 1504 = 1 um ~17:01, 1500 46,4). Loxone 17:05:00 1497 = 57,0 (ohne PV). Voraussetzungen 1534 255, 1477 7,5, 1504 1, 1500 46,4, keine Datei, Whitelist ok. 17:05:06 SET 419 (41,9), schreib_pruefung 17:05:22 haelt. ~17:06:20: 1499 41,9, 1530 0,0, 1504 0, 25611 0,00 (Verdichter lief in dieser Ladung noch nicht). Loxone 17:09:59 1497 = 52,0 (Rueckweg auto_loxone), ~17:10:50 1504 = 1, 1530 56,0. Pi-Datei 17:10:48 entfernt."
  ergebnis: "Hypothese widerlegt (n = 1): bei 1499 41,9 < 1500 46,4 ging 1504 binnen ~75 s auf 0, 1530 fiel auf 0. Einschraenkung [wahrscheinlich]: die Ladung stand noch in der Startphase ohne Verdichter (E26 lief mit Verdichter 2 min weiter, E7 mit Verdichter endete < 1 min) - der Unterschied zu E26 ist damit nicht erklaert. Was bringt uns das: 1497 unter WW-Ist beendet eine frisch angeforderte Ladung sofort; fuer die Frage Verdichter laeuft folgt E32."
  angelegt: "OR 09.11.2026 18:58 (R9 Vorrat < 3, aus E26). Was bringt uns das: entscheidet, ob 1530 das Ladeende bestimmt oder ein anderes Kriterium (Laufzeit, WW_Unten_SF2); Grundlage, um Ladungen per 1497 gezielt zu beenden."
- id: E30
  titel: "(E1 Wiederholung, n = 2) W01-Startschwelle 4,9 K in Abendlage, danach Ladung fuer E29 nutzen"
  hypothese: "Die Hoval startet eine WW-Ladung bei 1499 - 1500 >= 4,9 K, bei 4,6 K nicht (E1 vom 03.11. mittags, n = 1; Regel W01 steht im Waechter auf offen). Bestaetigt, wenn bei 4,6 K 2 min lang 1504 = 0 bleibt und bei 5,1 K binnen 70 s 1504 = 1 kommt; widerlegt sonst."
  register: 1497
  wert_formel: "Stufe 1 round(ist_1500 + 4.6, 1) fuer 2 min, Stufe 2 round(ist_1500 + 5.1, 1) bis Start, max. 2 min; je knapp nach einem Loxone-Schreiben"
  rueckweg: auto_loxone
  fruehester_start: "2026-11-12 16:55"
  dauer_min: 8
  spaetester_rueckweg: "21:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa, So]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 0", "r(1500) >= 45.5", "r(1500) <= 47.0", "kein_experiment_aktiv", "whitelist_enthaelt(1497)"]
  messgroessen: [1497, 1499, 1500, 1504, 1539, 25611]
  beobachtete_regeln: [W01]
  abbruch: ["r('1534') != 255", "r('1500') < 40.0"]
  status: abgebrochen
  protokoll: "OR 12.11. 16:59-17:01: Voraussetzungen live 1534 255, 1477 7,5, 1504 0, 1500 46,4, 1499 50,0, keine Datei. Loxone SET 1497 500 um 16:59:30,998; 16:59:37 SET 510 (Stufe 1, Delta 4,6 K), schreib_pruefung 16:59:53 haelt, 1499 noch 50,0 (WEZ-Rundumabfrage). 17:00:00,008 Loxone SET 520 (Abendfenster 52), danach 1504 = 1 (gelesen ~17:01). Pi-Datei 16:59:40-17:03 (entfernt vor E29)."
  ergebnis: "Gestoert, kein Beleg zu W01: Stufe 1 hielt nur 23 s, dann schrieb Loxone das Abendsoll 52 (Delta 5,6 K) und startete die Ladung selbst. Lehre: Loxone schaltet 1497 um 17:00:00 auf 52 und 17:05:00 auf 57 (ohne PV); Versuche an 1497 nicht um 16:55-17:10 legen. Wiederholung als E31."
  angelegt: "OR 12.11.2026 16:57 (R9 Vorrat < 3, heute noch kein Experiment; W01 offen). Was bringt uns das: zweiter Beleg fuer die Startschwelle, auf der Loxone-Ladungen per 1497 aufbauen; die ausgeloeste Ladung kommt rund 1 K frueher als von selbst (1500 46,3 statt 45,1) und dient direkt als Ladung fuer E29."
- id: E31
  titel: "(E30 Wiederholung) W01-Startschwelle 4,9 K, n = 2, ausserhalb der Loxone-Umschaltzeiten"
  hypothese: "Wie E30: bei 1499 - 1500 = 4,6 K 2 min lang kein Start (1504 = 0), bei 5,1 K Start binnen 70 s."
  register: 1497
  wert_formel: "Stufe 1 round(ist_1500 + 4.6, 1) fuer 2 min, Stufe 2 round(ist_1500 + 5.1, 1) bis Start, max. 2 min; je knapp nach einem Loxone-Schreiben"
  rueckweg: auto_loxone
  fruehester_start: "2026-11-13 09:00"
  dauer_min: 8
  spaetester_rueckweg: "16:45"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa, So]
  sperrfenster: ["So 12:00-18:00", "taeglich 16:50-17:15", "taeglich 18:45-19:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 0", "r(1499) == r(1497)", "r(1500) >= 45.5", "r(1500) <= 47.0", "r(27545) == 0", "kein_experiment_aktiv", "whitelist_enthaelt(1497)"]
  messgroessen: [1497, 1499, 1500, 1504, 1539, 25611]
  beobachtete_regeln: [W01]
  abbruch: ["r('1534') != 255", "r('1500') < 40.0"]
  status: abgeschlossen
  ergebnis: "W01 gehalten (n = 2 mit E-Vorgaengern). Stufe 1: 1497 = 51,5 bei 1500 46,9-47,1 (Abstand 4,4-4,6 K) hielt <MAC>, 1499 folgte auf 51,5, 1504 blieb 0. Stufe 2: 1497 = 52,2 bei 1500 47,1 (5,1 K) um 11:03:35, 1504 = 1 und 1539 = 4 schon beim Lesen 11:04:07 (Start binnen 32 s); Loxone schrieb 11:06:22 wieder 50,0, Ladung lief weiter (11:06 P_el 5,12 kW). [sicher aus Bridge-Journal und MCP]"
  angelegt: "OR 12.11.2026 17:12 (R9 Vorrat, E30 gestoert). Was bringt uns das: zweiter Beleg fuer die Startschwelle, auf der Loxone-Ladungen per 1497 aufbauen."
  protokoll: "OR 13.11.2026 (Pi-Zeit): Voraussetzungen 11:00 alle erfuellt (1534 255, 1477 4,5, 1504 0, 1499 = 1497 = 50,0, 1500 46,9, 27545 0, keine experiment_aktiv.json, 1497 in Whitelist). Loxone-SET 1497 = 500 um 11:01:22. 11:01:33 SET 515, schreib_pruefung 11:01:49 haelt; experiment_aktiv.json 11:01:45 auf dem Pi. 11:02:45 1499 51,5, 1504 0, 1500 46,9. 11:03:31 1504 0, 1500 47,1. 11:03:35 SET 522, schreib_pruefung 11:03:51 haelt. 11:04:07 1504 1, 1539 4. 11:06:22 Loxone SET 500 (Rueckweg auto_loxone), 11:06:30 1497 = 50,0 gelesen, 1504 1, P_el 5,12 kW. experiment_aktiv.json ~11:06:40 entfernt, Fehlen gelesen. Was bringt uns das: Loxone kann eine Ladung mit Soll = Ist + 5,1 K zuverlaessig ausloesen, Ist + 4,6 K reicht nicht; die Schwelle liegt also zwischen 4,6 und 5,1 K (W01 4,9 K bleibt). Kosten: Ladung bei 47,1 statt ~45,1."
- id: E32
  titel: "(E26/E29 Klaerung) Endet eine Ladung MIT laufendem Verdichter, wenn 1499 unter 1500 faellt?"
  hypothese: "Mit laufendem Verdichter (25611 > 1,0 kW seit >= 3 min) endet eine WW-Ladung binnen 2 min, wenn 1497 = 1500 - 4,5 K geschrieben wird (wie E7, E29). Widerlegt, wenn 1504 >= 3 min auf 1 bleibt (wie E26)."
  register: 1497
  wert_formel: "max(40.0, round(ist_1500 - 4.5, 1))"
  schreibzeit: "knapp nach einem Loxone-Schreiben, nicht 16:50-17:15 und 18:45-19:00"
  rueckweg: auto_loxone
  fruehester_start: "2026-11-13 07:00"
  dauer_min: 8
  spaetester_rueckweg: "21:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa, So]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 1", "verdichter_laeuft_seit_3_min (25611 > 1.0)", "r(1500) >= 44.5", "r(1500) <= 50.0", "kein_experiment_aktiv", "whitelist_enthaelt(1497)"]
  messgroessen: [1497, 1499, 1500, 1504, 1530, 25611]
  beobachtete_regeln: [W01, S02, S03]
  abbruch: ["r('1534') != 255", "r('1500') < 40.0"]
  status: abgeschlossen
  ergebnis: "Hypothese gehalten (n = 1): Ladung seit 11:04 mit Verdichter (P_el 3,6-3,9 kW, Mod 52-57 %), 11:11:29 SET 1497 = 42,3 bei 1500 46,9; WW_Status 0 um 11:11:51 (<= 22 s), P_el 0 um 11:12:32 (<= 63 s). Loxone schrieb 11:16:22 wieder 50,0, keine neue Ladung (1500 47,3 > 45,1). [sicher aus ww_hires 20 s und Bridge-Setlog] Was bringt uns das: Loxone kann eine laufende Ladung auch mit Verdichter per 1497 binnen 1 min beenden (wie E7); E26 bleibt der Ausreisser."
  protokoll: "OR 13.11.2026 (Pi-Zeit): Start durch den 10:54-Lauf 11:11:29 (Setlog SET 423 nach Loxone-SET 500 um 11:11:22), experiment_aktiv.json 11:11:45. Dieser Lauf schrieb kein Ende (kein Log-Eintrag 10:54, Ursache unbekannt). Rueckweg auto_loxone 11:16:22 (Setlog SET 500), 1497 = 50,0 am 11:55 gelesen. R6 durch OR 11:54-Lauf: Datei 11:55:13 vom Pi entfernt (Kopie C:\\Users\\<user>\\Claude\\data\\regelwaechter\\experiment_aktiv_E32.json). Nebenbefund: in experiment_aktiv.json von E31/E32 stand r(1534) ohne Anfuehrungszeichen, der Waechter konnte die Abbruchausdruecke nicht auswerten (kritisch 'Schluessel muss Text sein'); Abbruchbedingungen waren laut ww_hires nie erfuellt (1534 255, 1500 >= 46,7). Kuenftig Abbruch-Ausdruecke unveraendert aus dem Block (r('1534')) uebernehmen. Kosten: Ladung endete bei 46,9 statt ~50, die naechste kommt entsprechend frueher."
  angelegt: "OR 12.11.2026 17:12 (R9 Vorrat; E29 widerlegt nur in der Startphase ohne Verdichter). Was bringt uns das: entscheidet, ob Loxone eine laufende Ladung per 1497 sauber abbrechen kann (E7 ja, E26 nein)."
- id: E33
  titel: "(E32 Wiederholung, n = 2) Ladungsende mit laufendem Verdichter bei 1497 = 1500 - 4,5 K, spaet in der Ladung"
  hypothese: "Wie E32, aber bei 1500 >= 48,5 (spaete Ladephase, Verdichter >= 10 min): 1504 geht binnen 2 min auf 0. Widerlegt, wenn 1504 >= 3 min auf 1 bleibt (wie E26)."
  register: 1497
  wert_formel: "max(40.0, round(ist_1500 - 4.5, 1))"
  schreibzeit: "knapp nach einem Loxone-Schreiben, nicht 16:50-17:15 und 18:45-19:00"
  rueckweg: auto_loxone
  fruehester_start: "2026-11-13 13:00"
  dauer_min: 8
  spaetester_rueckweg: "21:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa, So]
  sperrfenster: ["So 12:00-18:00", "taeglich 16:50-17:15", "taeglich 18:45-19:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 1", "verdichter_laeuft_seit_10_min (25611 > 1.0)", "r(1500) >= 48.5", "r(1500) <= 50.0", "r(1497) == 50.0", "kein_experiment_aktiv", "whitelist_enthaelt(1497)"]
  messgroessen: [1497, 1499, 1500, 1504, 1530, 25611]
  beobachtete_regeln: [W01, S02, S03]
  abbruch: ["r('1534') != 255", "r('1500') < 40.0"]
  status: geplant
  ergebnis: null
  angelegt: "OR 13.11.2026 11:58 (R9 Vorrat < 3). Was bringt uns das: zweiter Beleg, ob Loxone eine Ladung mit Verdichter auch kurz vor dem Ende per 1497 sauber abbricht; E26 (nein) lag spaet in der Ladung, E7/E32 (ja) frueh. Kosten gering, die Ladung ist dann fast fertig."
- id: E34
  titel: "Ladeende-Kriterium 1500 >= 1497? Gegenprobe zu E27: 1497 knapp UEBER Ist waehrend der Ladung"
  hypothese: "Ist das Ladeende 1500 >= 1497 (ohne Nachlauf-Hysterese), laeuft die Ladung bei 1497 = 1500 + 0,5 K weiter, bis 1500 die 0,5 K erreicht (1504 bleibt >= 2 min auf 1 bzw. endet erst bei 1500 >= 1497). Widerlegt, wenn 1504 binnen 1 min auf 0 geht (dann gibt es einen Abstand/Hysterese beim Ladeende)."
  register: 1497
  wert_formel: "max(40.0, round(ist_1500 + 0.5, 1))"
  schreibzeit: "knapp nach einem Loxone-Schreiben (Takt :x2:27/:x7:27), nicht 16:50-17:15 und 18:45-19:00"
  rueckweg: auto_loxone
  fruehester_start: "2026-11-15 18:00"
  dauer_min: 6
  spaetester_rueckweg: "21:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa, So]
  sperrfenster: ["So 12:00-18:00", "taeglich 16:50-17:15", "taeglich 18:45-19:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 1", "verdichter_laeuft (25611 > 1.0)", "r(1500) >= 44.0", "r(1500) <= 48.5", "r(1497) == 50.0", "kein_experiment_aktiv", "whitelist_enthaelt(1497)"]
  messgroessen: [1497, 1499, 1500, 1504, 1530, 25611]
  beobachtete_regeln: [W01, S02, S03]
  abbruch: ["r('1534') != 255", "r('1500') < 40.0"]
  status: abgeschlossen
  ergebnis: "Hypothese gehalten (n = 1): 07:05:46 1497 = 48,0 geschrieben (1500 = 47,5, Ladung lief, 1504 = 1). 1504 ging 07:07:12 auf 0, 86 s nach dem Schreiben, bei 1500 = 47,6-47,9 (10-s-Werte ww_hires schwanken +-0,3 K); P_el 0 ab 07:07:42 (~30 s Nachlauf). Kein Abstand ueber dem Soll: Ladeende = 1500 >= 1497 im Rahmen der Fuehlerschwankung (eher -0,1 K). Nebenbefund: Speicher_Sollwert folgt 1497 + 4 K mit ~55 s Verzug (54 -> 52 um 07:06:41). Rueckweg auto_loxone: Loxone schrieb 07:10:35 wieder 500, gelesen 07:10:50 = 50,0; Setlog SET 480 07:05:46 bestaetigt. Was bringt uns das: zusammen mit E27 (Senkung unter Ist beendet binnen 31 s) ist das Ladeende-Kriterium F318 belegt (n = 1 je Richtung): Loxone kann eine Ladung per 1497 auf ~0,3 K genau begrenzen (PV-Rest, Abendfenster)."
  angelegt: "OR 15.11.2026 11:05 (R9 Vorrat < 3, aus E27). Was bringt uns das: legt das Ladeende-Kriterium fest (1500 >= 1497 oder mit Abstand); damit kann Loxone Ladungen auf ein Grad genau begrenzen (PV-Rest, Abendfenster)."
- id: E35
  titel: "(E34 n = 2) Ladeende bei 1497 = 1500 + 1,0 K: endet die Ladung erst, wenn 1500 das Soll erreicht?"
  hypothese: "Wie E34: Ladeende bei 1500 >= 1497 (Toleranz <= 0,3 K). Mit 1,0 K Abstand laeuft die Ladung nach dem Schreiben weiter, bis 1500 >= 1497 - 0,3; 1504 bleibt mindestens 2 min auf 1. Widerlegt, wenn 1504 binnen 1 min auf 0 geht oder erst > 0,3 K ueber dem Soll."
  register: 1497
  wert_formel: "max(40.0, round(ist_1500 + 1.0, 1))"
  schreibzeit: "knapp nach einem Loxone-Schreiben (Takt seit 16.11. :x0:35/:x5:35, im Setlog pruefen), nicht 16:50-17:15 und 18:45-19:00"
  rueckweg: auto_loxone
  fruehester_start: "2026-11-16 07:15"
  dauer_min: 6
  spaetester_rueckweg: "21:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa, So]
  sperrfenster: ["So 12:00-18:00", "taeglich 16:50-17:15", "taeglich 18:45-19:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1504) == 1", "verdichter_laeuft (25611 > 1.0)", "r(1500) >= 44.0", "r(1500) <= 48.0", "r(1497) == 50.0", "kein_experiment_aktiv", "whitelist_enthaelt(1497)"]
  messgroessen: [1497, 1499, 1500, 1504, 1530, 25611]
  beobachtete_regeln: [W01, S02, S03]
  abbruch: ["r('1534') != 255", "r('1500') < 40.0"]
  status: geplant
  ergebnis: null
  angelegt: "OR 16.11.2026 07:12 (R9 Vorrat < 3, Wiederholung E34 mit groesserem Abstand). Was bringt uns das: zweite Messung fuer F318; zeigt, wie genau Loxone eine Ladung bei einem Zwischen-Soll beenden kann."
- id: E36
  titel: "(E23 Wiederholung) WW-Impuls im LAUFENDEN Heizlauf bei Kaelte (1477 0-3 C): nahtloser Wechsel?"
  hypothese: "Wie E13/E22 (n = 2, 3-6 C): 1497 = 1500 + 5,5 K im laufenden Heizlauf setzt 1504 binnen 1 min auf 1 und die WP wechselt ohne Verdichterstopp (25611 bleibt > 0,3) auf WW. Widerlegt, wenn der Verdichter stoppt (Code 16 Wiedereinschaltverzoegerung wie E23 aus dem Stillstand) oder vorher abtaut."
  register: 1497
  wert_formel: "min(53.0, round(ist_1500 + 5.5, 1))"
  schreibzeit: "knapp nach einem Loxone-Schreiben (:x0:35/:x5:35); unmittelbar davor (< 30 s) 25611 > 1.0 und Status 'Heizen' lesen, sonst NICHT schreiben"
  rueckweg: auto_loxone
  fruehester_start: "2026-11-16 09:30"
  dauer_min: 6
  spaetester_rueckweg: "21:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa, So]
  sperrfenster: ["So 12:00-18:00", "taeglich 16:50-17:15", "taeglich 18:45-19:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1477) < 3.0", "r(1504) == 0", "heizlauf_seit_mindestens_10_min", "verdichter_laeuft_jetzt (25611 > 1.0, < 30 s alt)", "r(1500) >= 44.0", "r(1500) <= 48.0", "r(1497) == 50.0", "kein_experiment_aktiv", "whitelist_enthaelt(1497)"]
  messgroessen: [1497, 1499, 1500, 1504, 1539, 25611, WP_VL]
  beobachtete_regeln: [S02, S03, W01]
  abbruch: ["r('1534') != 255", "r('1500') < 42.0"]
  status: geplant
  ergebnis: null
  angelegt: "OR 16.11.2026 09:07 (E23 ungueltig: Heizlauf endete 2 min vor dem Schreiben). Was bringt uns das: zeigt, ob Loxone bei Frost eine WW-Ladung an einen laufenden Heizlauf anhaengen kann, ohne einen zusaetzlichen Verdichterstart (Takt) zu erzeugen."
- id: E37
  titel: "(E11 n = 2) Verstaerkung 1490 bei Frostnaehe (1477 0-5 C): wie viel % Modulation je K Soll-Sprung?"
  hypothese: "Wie E11 (06.11., +4 K -> +12 %-Punkte binnen 65 s, 3 %/K): +4 K auf 1490 im laufenden Heizlauf heben 18726 binnen 2 min um 8-16 %-Punkte. Widerlegt, wenn < 4 %-Punkte (Modulation nahe Minimum reagiert anders) oder > 20."
  register: 1490
  wert_formel: "min(40.0, round(ist_1490 + 4.0, 1))"
  schreibzeit: "knapp nach einem Loxone-Schreiben auf 1490 (Takt :x4:11/:x9:11 laut Setlog 19.11.)"
  rueckweg: auto_loxone
  fruehester_start: "2026-11-19 08:05"
  dauer_min: 5
  spaetester_rueckweg: "21:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1477) <= 5.0", "r(1504) == 0", "r(1539) == 1", "heizlauf_seit_mindestens_10_min", "kein_experiment_aktiv", "whitelist_enthaelt(1490)"]
  messgroessen: [1490, 18726, 25611, WP_VL]
  beobachtete_regeln: [H01, H06]
  abbruch: ["r('1534') != 255", "r('1500') < 42.0"]
  status: abgeschlossen
  ergebnis: "Hypothese gehalten (n = 2 mit E11): +4 K auf 1490 (32,5 -> 36,5) um 08:18:28 hob die Modulation von 39 % (08:18:51) auf 50 % (08:19:52), P_el 1,82 -> 2,45 kW, also +11 %-Punkte = 2,75 %/K (E11: 3,0 %/K bei mildem Wetter) [sicher fuer 1 Flanke, 1-min-Raster ww_hires]. Loxone schrieb schon 08:19:33 wieder 325 (65 s Wirkdauer, nicht 5 min), 08:20:53 Modulation 40 %. Was bringt uns das: die Verstaerkung Soll -> Modulation ist bei 3,6 C aussen praktisch gleich wie bei mildem Wetter (~3 %/K, Totzeit < 85 s); der Zwilling kann eine Loxone-Raumkorrektur von 1 K mit ~3 %-Punkten bzw. ~0,15 kW el. ansetzen."
  protokoll: "OR 19.11.2026 (Pi-Zeit): Voraussetzungen 08:18 live: 1534 255, 1477 3,6, 1504 0, 1539 1, Heizlauf seit ~08:07:30 (ww_hires), keine Datei, 1490 in Whitelist. 08:18:28 SET 1490 <- 365 (Setlog), schreib_pruefung haelt. experiment_aktiv.json auf dem Pi ~08:19. 08:19:33 Loxone SET 325 (Rueckweg auto_loxone), gelesen 08:21 = 32,5. 1534 255 durchgehend, kein Abbruch. Datei 08:21 vom Pi entfernt (Kopie C:\\Users\\<user>\\Claude\\data\\regelwaechter\\experiment_aktiv_E37.json). Loxone-Takt auf 1490 heute unregelmaessig (08:13:53, 08:14:33, 08:19:33)."
  angelegt: "OR 19.11.2026 08:05 (R9: seit 17.11. kein Experiment, alle 1497-Bloecke durch Loxone-52/57 oder fehlenden Frost blockiert; R10-Abhilfe: Versuch an anderem Register). Was bringt uns das: zweiter Punkt fuer die Verstaerkung Soll->Modulation, bei tieferer Aussentemperatur; damit rechnet der Zwilling, wie stark eine Loxone-Raumkorrektur auf Leistung und Takt wirkt."
- id: E38
  titel: "(E11/E37 n = 3) Verstaerkung 1490 abends bei Frostnaehe: % Modulation je K Soll-Sprung"
  hypothese: "Wie E11 (3,0 %/K) und E37 (2,75 %/K): +4 K auf 1490 im laufenden Heizlauf heben 18726 binnen 2 min um 8-16 %-Punkte. Widerlegt, wenn < 4 oder > 20 %-Punkte."
  register: 1490
  wert_formel: "min(40.0, round(ist_1490 + 4.0, 1))"
  schreibzeit: "knapp nach einem Loxone-Schreiben auf 1490 (Setlog 20.11.: 18:50:39, 18:51:59, 18:52:39 - unregelmaessig)"
  rueckweg: auto_loxone
  fruehester_start: "2026-11-20 19:00"
  dauer_min: 5
  spaetester_rueckweg: "21:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1477) <= 5.0", "r(1504) == 0", "r(1539) == 1", "heizlauf_seit_mindestens_10_min", "kein_experiment_aktiv", "whitelist_enthaelt(1490)"]
  messgroessen: [1490, 18726, 25611, WP_VL]
  beobachtete_regeln: [H01, H06]
  abbruch: ["r('1534') != 255", "r('1500') < 42.0"]
  status: abgeschlossen
  ergebnis: "Hypothese gehalten (n = 3 mit E11/E37): +4 K auf 1490 (31,0 -> 35,0) um 19:13:49 (SET im Setlog) hob die Modulation von 35 % (19:13) auf 44 % (~19:14:50), P_el 1,76 -> 2,32 kW, also +9 %-Punkte = 2,25 %/K [sicher fuer 1 Flanke, MCP-Einzelablesungen im ~1-min-Raster]. 19:15:55 noch 43 %, 1490 hielt 35,0 mindestens 2 min (laenger als bei E37), um ~19:18 Loxone-Rueckweg 31,0 gelesen, Modulation 35 %. Was bringt uns das: drei Punkte 2,25/2,75/3,0 %/K bei 3,6-3,8 C bzw. mild - der Zwilling kann ~2,5-3 %/K je K Soll mit < 65 s Totzeit ansetzen; abends nach der 57er-Phase etwas schwaecher [Vermutung, n = 1]."
  protokoll: "OR 20.11.2026 (Pi-Zeit): Heizlauf-Beginn zwischen 18:57:30 (25611 = 0) und 19:04 (1539 = 1, 1,65 kW). Voraussetzungen 19:13-19:14 live: 1534 255, 1477 3,8, 1504 0, 1539 1, 1500 60,3, keine Datei, 1490 in Whitelist, Modulation 35 %, P_el 1,76. Letzter Loxone-SET 1490 vorher 19:12:11 (310). 19:13:49 SET 1490 <- 350, schreib_pruefung 19:14:05 haelt. experiment_aktiv.json 19:14 auf dem Pi. ~19:14:50 Modulation 44 %, P_el 2,32, 1490 35,0. ~19:15:55 43 %, 2,26 kW, 1490 35,0. ~19:18 1490 31,0 (Loxone), Modulation 35 %, 1534 255. Kein Abbruch. Datei 19:18:18 vom Pi entfernt (Kopie C:\\Users\\<user>\\Claude\\data\\regelwaechter\\experiment_aktiv_E38.json)."
  angelegt: "OR 20.11.2026 18:56 (R9: heute 0 Experimente, Vorrat E33/E35/E36 braucht WW-Ladung; Vorrat ohne WW-Bedingung ergaenzt). Was bringt uns das: dritter Punkt fuer Soll->Modulation, erstmals abends nach einer 57er-Phase; ab n = 3 kann der Zwilling die Verstaerkung als Regel H-neu fuehren."
- id: E39
  titel: "Linearitaet Soll->Modulation: +2 K auf 1490 im Heizlauf (Gegenstueck zu E11/E37/E38 mit +4 K)"
  hypothese: "Bei linearer Verstaerkung (2,25-3,0 %/K aus E11/E37/E38) heben +2 K auf 1490 die Modulation binnen 2 min um 4-6 %-Punkte. Widerlegt, wenn < 2 (Totband/Schwelle) oder > 9 %-Punkte (nicht linear)."
  register: 1490
  wert_formel: "min(40.0, round(ist_1490 + 2.0, 1))"
  schreibzeit: "knapp nach einem Loxone-Schreiben auf 1490 (Setlog 21.11.: 07:48:44, 07:53:44 - 5-min-Raster :x3:44/:x8:44)"
  rueckweg: auto_loxone
  fruehester_start: "2026-11-21 07:55"
  dauer_min: 5
  spaetester_rueckweg: "21:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1477) <= 5.0", "r(1504) == 0", "r(1539) == 1", "heizlauf_seit_mindestens_10_min", "kein_experiment_aktiv", "whitelist_enthaelt(1490)"]
  messgroessen: [1490, 18726, 25611]
  beobachtete_regeln: [H01, H06]
  abbruch: ["r('1534') != 255", "r('1500') < 42.0"]
  status: abgeschlossen
  ergebnis: "Hypothese nicht gehalten, aber nicht widerlegt (Zwischenbereich): +2 K auf 1490 (32,4 -> 34,4) um 07:58:53 (SET im Bridge-Journal) hob die Modulation von 35 % auf hoechstens 38 % (gelesen 08:00:29 und 08:01:14), P_el 1,80 -> 2,00 kW, also +3 %-Punkte = 1,5 %/K statt erwarteter 2,25-3,0 %/K [sicher fuer die Ablesungen; Spitze zwischen den ~45-s-Ablesungen kann fehlen, WEZ-Register bis 60 s alt]. 08:02:09 schon wieder 36 %, 08:03:44 Loxone-Rueckweg 324, 08:04 Modulation 35 %. Was bringt uns das: kleine Soll-Spruenge wirken unterproportional [Vermutung, n = 1] - fuer den Zwilling ab 35 % Mindestmodulation eher ~1,5 %/K bei 2 K und ~2,5 %/K bei 4 K ansetzen; eine Loxone-Raumkorrektur von 1 K bewegt die Leistung kaum (~0,1 kW el)."
  protokoll: "OR 21.11.2026 (Pi-Zeit): Heizlauf seit ~07:32 (Volllogger 07:30 1539 = 0, 07:35 = 1). Voraussetzungen 07:5x live: 1534 255, 1477 4,1, 1504 0, 1539 1, 1500 49,9, keine Datei, 1490 in Whitelist, Modulation 35 %, P_el 1,78. Loxone-SET 1490 = 324 um 07:58:44. 07:58:53 SET 1490 <- 344, schreib_pruefung 07:59:09 haelt. experiment_aktiv.json 07:59 auf dem Pi. 07:59:43 35 %, 1,80 kW, 1490 34,4. 08:00:29 38 %, 2,00 kW. 08:01:14 38 %, 1,95 kW, 1490 34,4. 08:02:09 36 %, 1,89 kW, 1534 255, 1500 49,7. 08:03:44 Loxone SET 324. 08:04 Modulation 35 %, 1490 32,4 rueckgelesen. Kein Abbruch. Datei 08:04:03 vom Pi entfernt (Kopie C:\\Users\\<user>\\Claude\\data\\regelwaechter\\experiment_aktiv_E39.json)."
  angelegt: "OR 21.11.2026 07:56 (R9: heute 0 Experimente, E33/E35 brauchen WW-Ladung, E36 Frost < 3 C; Heizlauf seit ~07:32 bei 4,1 C). Was bringt uns das: zeigt, ob der Zwilling die Verstaerkung linear (%/K) ansetzen darf oder ob kleine Loxone-Korrekturen (1-2 K) unter einer Schwelle verpuffen."
- id: E40
  titel: "Linearitaet Soll->Modulation: +3 K auf 1490 im Heizlauf (zwischen E39 +2 K und E11/E37/E38 +4 K, V177)"
  hypothese: "V177: kleine Soll-Spruenge wirken unterproportional. Erwartet +3 K -> +5 bis +8 %-Punkte (1,7-2,7 %/K). Widerlegt, wenn < 3 oder > 9 %-Punkte."
  register: 1490
  wert_formel: "min(40.0, round(ist_1490 + 3.0, 1))"
  rueckweg: auto_loxone
  fruehester_start: "2026-11-22 07:50"
  dauer_min: 5
  spaetester_rueckweg: "21:00"
  erlaubte_tage: [Mo, Di, Mi, Do, Fr, Sa, So]
  sperrfenster: ["So 12:00-18:00"]
  voraussetzungen: ["r(1534) == 255", "r(1477) >= 0", "r(1477) <= 5.0", "r(1504) == 0", "r(1539) == 1", "heizlauf_seit_mindestens_10_min", "kein_experiment_aktiv", "whitelist_enthaelt(1490)"]
  messgroessen: [1490, 18726, 25611]
  beobachtete_regeln: [H01, H06]
  abbruch: ["r('1534') != 255", "r('1500') < 42.0"]
  status: abgeschlossen
  ergebnis: "Hypothese gehalten: +3 K auf 1490 (33,0 -> 36,0, SET 07:54:34 im Schreibprotokoll) hob die Modulation von 35 % auf 42 % (ww_hires 07:55:52, <= 78 s), P_el 1,77 -> 2,19 kW; 42 % hielten bis 07:57:52, nach dem Loxone-Rueckweg (1490 = 33,0) 07:58:51 wieder 35 %, 1,81 kW [sicher, 1-min-Raster]. Das sind 2,3 %/K - zwischen E39 (1,5 %/K bei 2 K) und E11/E37/E38 (2,25-3,0 %/K bei 4 K). Was bringt uns das: V177 haelt an einem dritten Punkt; der Zwilling kann die Verstaerkung als mit der Sprunghoehe steigende Kennlinie ansetzen (ab 35 % Mindestmodulation), 1 K Loxone-Korrektur bewegt kaum etwas."
  protokoll: "OR 22.11.2026 (Pi-Zeit): Heizlauf seit 06:46. Voraussetzungen 07:54 live: 1534 255, 1477 1,9, 1504 0, 1539 1, 25611 1,77, 18726 35 %, 1500 49,7, 1490 33,0 (in Whitelist), keine experiment_aktiv.json. Letzter Loxone-SET 1490 07:52:22 (330). 07:54:34 SET 1490 <- 360, schreib_pruefung 07:54:50 haelt. experiment_aktiv.json ~07:55 auf dem Pi. ww_hires: 07:54:52 35 %/1,77 kW; 07:55:52 42 %/2,19 kW, WP_VL 37,7; 07:56:52 42 %/2,20; 07:57:52 42 %/2,18; 07:58:51 35 %/1,81. MCP ~07:58: 1490 = 33,0 (Loxone-Rueckweg), 1534 255. Kein Abbruch. Datei ~07:59 vom Pi entfernt (Kopie C:\\Users\\<user>\\Claude\\data\\regelwaechter\\experiment_aktiv_E40.json)."
  angelegt: "OR 22.11.2026 07:54 (R9: heute 0 Experimente, E36 nicht startbar wegen 1500 49,7 > 48; V177 verlangt einen 3-K-Punkt). Sonntag erlaubt ausser 12-18 (R8)."
```
Protokoll E34 (16.11.2026, ww_hires 10 s und MCP, Pi-Zeit): Vorher 07:02:56 1534 = 255, 1477 = 2,1, 1504 = 1, 25611 = 3,10 kW, 1500 = 47,1, 1497 = 50,0, kein experiment_aktiv.json, Loxone-Takt jetzt :x0:35/:x5:35 (nicht mehr :x2:27/:x7:27). 07:05:42 1500 = 47,5. 07:05:46 write 480, schreib_pruefung 07:06:02 haelt. <MAC> WW_Status 1, WW_Ist 47,5-47,9, P_el 2,96 -> 2,91, Modulation 42 %. 07:07:12 WW_Status 0 (WW_Ist 47,9). 07:07:42 P_el 0, Modulation 0. 07:07:14 MCP: 1504 = 0, 1499 = 48,0, 1500 = 47,9. 07:10:50 1497 = 50,0 (Loxone 07:10:35). Datei auf dem Pi 07:11 entfernt.

Protokoll E11 (06.11.2026, Prometheus 15 s, Pi-Zeit): Vorher 1490 = 33,1, Modulation 47 %, P_el 2,29, WP-VL 33,9, RL 29,8; Heizlauf seit 08:00:45. 08:13:40 write 371, 08:13:55 schreib_pruefung haelt. 08:14:45 Modulation 59 %, P_el 3,02, VL 34,5. 08:15:15 58 %, VL 35,1. 08:15:45 47 %, P_el 2,29, VL 35,0. <MAC> 48 %. 08:18:45-08:20 46 %, VL 35,3, RL 31,2. 1490 gelesen 08:17:10 und 08:20 = 33,1. Datei auf dem Pi 08:20:03 entfernt. Was bringt uns das: Der Zwilling rechnet mit rund 3 %-Punkte je K und unter 65 s Totzeit (E9: 2,5 je K, unter 52 s). Der kurze Sprung kostet rund 0,7 kW fuer 1 min. Eine laengere Wirkung ist hiermit nicht gemessen, weil Loxone schnell zurueckschreibt.

Protokoll E7 (06.11.2026, ww_hires 10 s und MCP, Pi-Zeit): Vorher Ladung seit 08:37, 1497 = 50,0, 1500 = 47,2, 1504 = 1, P_el 2,98, Modulation 43 %, Voraussetzungen alle erfuellt (1534 = 255, 1477 = 1,8). <MAC> write 462. schreib_pruefung 08:55:25 haelt. 08:55:12 WW_Status 0, WW_Soll 46,2, WP_VL 53,9, P_el 2,97. 08:55:42 Modulation 0. 08:55:52 P_el 0, WP_VL 51,9. MCP 08:56:40: 1539 = 0, 25611 = 0. 08:56:51 WW_Soll 50,0, 08:57:52 WW_Soll_eff 50,0. 1504 = 0 bis 08:59:53, 1500 = 47,7, 1497 = 50,0. Datei auf dem Pi rund 08:59 entfernt. Was bringt uns das: Loxone kann eine Ladung ueber 1497 binnen unter 1 min beenden, und das Rueckschreiben startet keine neue, solange 1500 ueber der Startschwelle Soll - 4,9 K liegt. Kosten des Versuchs: Diese Ladung endete bei 47,7 statt rund 50, die naechste kommt entsprechend frueher.

Protokoll E12 (06.11.2026, ww_hires 10 s und MCP, Pi-Zeit): Vorher Verdichter aus seit rund 09:45, 1497 = 50,0, 1500 = 47,6, 1504 = 0, 1539 = 0, 1534 = 255, Aussen 2,7, SG Normal, Formel ergab 53,1, gekappt auf 53,0, also Abstand 5,4 K. Rund 10:01:10 write 530. schreib_pruefung 10:01:27 haelt. 10:01:11 WW_Soll 53,0. 10:01:21 SLP 1. 10:01:31 WW_Status 1. 10:01:51 WW_Soll 50,0 (Loxone, rund 40 s nach dem Schreiben). <MAC> WW_Soll_eff 53,0, ab 10:02:12 50,0. 10:02:02 Pumpe_HK1 0. 10:02:12 P_el 0,11, Modulation 15 %. 10:02:32 P_el 2,26, Modulation 42 %. <MAC> Modulation 54, 75, 81 %, P_el bis 5,28 kW, danach 10:05:53 68 %, 4,58 kW. 10:06:30 1497 = 50,0, 1504 = 1, 1539 = 4. Datei auf dem Pi rund 10:08 entfernt. Was bringt uns das: Loxone kann eine Ladung ueber 1497 ohne Smart Grid gezielt in eine PV-Stunde legen und braucht den hohen Wert nur kurz; danach reicht das normale Soll, damit sie zu Ende laeuft. Kosten: Die Ladung kam rund bei 47,6 statt bei 45,1. Nebenfund: Das Rueckschreiben von 1497 lag bei E4 19:26:41, E7 08:56:51 und E12 10:01:51, also immer rund 1:45 nach dem 5-min-Raster [wahrscheinlich]; E1 13:35:02 passt nicht. Wer die vollen 5 min will, schreibt knapp danach.

Protokoll E6/E15/E16 (06.11.2026, MCP, Pi-Zeit): 1490 hielt bei E9 07:00:23, E5 07:03:54 und E11 08:13:40 je mindestens 15 s, alle im Heizlauf. Bei E6 10:54:48 und E15 rund 11:00:12 war der Verdichter seit 10:26 aus, Loxone setzte 1490 beide Male binnen 15 s auf 30,5. Der Stillstand als Ursache ist [Vermutung] aus 3 gegen 2 Faellen, die Uhrzeit trennt das nicht. Meine erste Erklaerung Raster ist widerlegt. E16: 1498 hat bei 1496 = 4 in 2:44 min nichts bewegt. Was bringt uns das: F164 klaert, ob Loxone 1490 im Stillstand laufend schreibt; davon haengen E14 und jeder Stillstandsversuch an 1490 ab.



Protokoll E20 (06.11.2026, Pi-Zeit; Windows-PC geht rund 33 s vor): Vorher SG Vorzug, 1539 = 1, 1504 = 0, 1490 = 35,8, 1529 = 37,5, 28839 = 0. 13:58:12 write_register 28839 = 20: Antwort ok, rohwert_sofort 20, schreib_pruefung 13:58:28 haelt. Bridge-Protokoll 13:58:12: ABGELEHNT reg 28839, noch nie vom CAN gelesen (Cache kalt), kein SET reg. Rueckweg 13:58:47 = 0: ebenfalls ABGELEHNT, Tabelle zeigt 0. experiment_aktiv.json 13:58:38 bis 13:59:51. 1529 blieb 37,5, das belegt nichts, weil nichts gesendet wurde. Die 0 vor dem Versuch ist kein CAN-Wert. [sicher aus dem Bridge-Protokoll]

Protokoll E21 (06.11.2026, Pi-Zeit, Heizlauf seit 14:43:45, SG Vorzug, 1500 51,8): 14:58:00 1490 = 35,8, 1529 = 37,5, 1535 = 34,5, Modulation 35 %. 14:58:12 SET 1490 = 359, 14:59:09 und rund 14:59:13 1529 = 37,5. 14:59:14 SET 1490 = 360, 15:00:13 1529 = 38,0, Modulation 36 %, P_el 1,85 kW. 15:00:56 Loxone SET 358, 15:01:13 1529 noch 38,0 (WEZ-Register bis 60 s alt). 15:01:16 Loxone SET 359 aus eigenem Eingang, 15:01:50 1529 = 37,5. Datei auf dem Pi 15:02:06 entfernt. Alle 3 Schreibvorgaenge und der Rueckweg stehen als SET im Bridge-Protokoll. Rueckweg war auto_loxone, nicht von mir geschrieben.

Protokoll E18 (06.11.2026, Pi-Zeit, Stillstand seit 15:13:15, 1490 von Loxone seit 15:42:01 = 0, 1477 7,1 C, 1500 49,3): 15:57:05 write 5 ABGELEHNT, Bereich 100..1100, kein SET, Modbus-Tabelle zeigte bis 16:02:01 trotzdem 5, schreib_pruefung meldete "haelt". Wert im Block auf 29,0 geaendert (15:58). 16:02:01 Loxone SET 0, 16:02:05 SET 290. 16:07:01 Loxone SET 0, 16:07:04 SET 290. 16:12:01 Loxone SET 0, Rueckweg gelesen. Datei auf dem Pi 16:12 entfernt. Dazwischen: 1529 = 0, 1539 = 0, P_el 0 durchgehend. HK1: Volllogger 16:00 1501 = 0, 19706 = 0; 16:05 1501 = 23, 19706 = 1; 1513 26,4 C um 16:05, 27,8 C um 16:12; 1535 35,0 auf 36,5 C. Was bringt uns das: 1490 > 0 ist schon die HK1-Freigabe, der Wert nicht; Versuche im Zustand 1490 = 0 duerfen nicht so gefahren werden, wenn sie keine Anforderung erzeugen sollen. Mein Entscheid, Nebenwirkung erst 16:07 gesehen, nach der zweiten Wiederholung nicht mehr korrigiert.

Hinweis E5-E9: Alle Versuche sind in R9 der `SKILL.md` geregelt. Register 1490 und 1497 setzt Loxone binnen 5 min selbst zurück.
Hinweis E2: beim Start setzt der Orchestrator in `regelwerk\regeln.yaml` `XE1.pruefung.wert` auf den Experimentwert und beim Rückweg zurück (Datenänderung, keine Anlage), danach `pi_deploy.py`.