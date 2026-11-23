# Einschaltverzögerung Heizen: Parameter und Prüfung an Heizstarts (F5, 23.10.2026)
Analyse-Agent 23.10.2026 ~20:15 · nur lesend (kein Schreibzugriff auf Anlage, Busse, Kälteregler) · Katalogfrage F5.
Vorlauf: `[lokaler Pfad]`, Vorbefund WP011 (Loop 23.10. 17:00/19:25), Firmware-Funde F26/F28/F29 (Okt., `[lokaler Pfad]`, `WP_Verhaltenskarte.md` Nachträge 09.–10.10.).
Daten:
- X26-Sniffer `~/rs485_sniff/log/rs485_2026-10-16…23.log(.gz)`: Zeilen `### ZUSTAND` (alle ~5 s, 133 378 Zeilen 16.10. 00:00 – 23.10. 19:59, **keine Lücke > 60 s**). Lokale Auszüge: `[lokaler Pfad]`. `status` = WEZ-Status (= Modbus 1539 = X26-dp 33).
- pCO-Datenbank, die die TopTronic über X26 zyklisch beim Kälteregler abfragt (Decoder `~/rs485_sniff/rs485_pcodb.py`, nur Logdatei lesen): `[lokaler Pfad]` / `.out`.
- Volllogger (5 min) für 1520/1529/18722/18723/18768: `Emulation\or_ag1_2026-10-*.csv*` + neu `Emulation\or_f5_20261023_vl23.csv`.
- HoxPi-MCP `search_registers` / `read_register`; offizielle Liste `[lokaler Pfad]`.
Skripte/Ausgaben: `[lokaler Pfad]` (+ `_8.out`, `_9.out`, `_10.out`, `_11.out`).

## Kurzbefund
1. **Die „15-min-Einschaltverzögerung nach RL = Soll − 1,5 K“ ist der Kälteregler-Parameter 33-055 = HKA59 = 15 min** (pCO-DB 0x811F, Bereich 1–240 min, Werkswert 15, nicht in der pax). Der Wert ist **live gelesen: 15 min, 199 von 199 Lesungen am 23.10. 00:01–20:03 gleich** – **sicher**.
2. **Kern der Frage: Es gibt zwei getrennte 15-min-Zeitglieder, beide im Kälteregler (HAICO), nicht in der TopTronic** – **sicher** (Messung):
   - **HKA59 (33-055)** zählt ab „Bedingung erfüllt“, unabhängig vom letzten Stopp. Beleg: 4 frische Anforderungen nach **69–173 min Stillstand** (WP011 längst abgelaufen) wurden trotzdem erst **15,8–16,4 min nach der Anforderung** freigegeben (17.10. 08:25, 17.10. 17:41, 18.10. 14:19; dazu 16.10. 13:18 nach 10,5 min Pause → 15,9 min).
   - **WP011 = 15 min** (pCO-DB 0x821C, live 15, 198/198) zählt ab Verdichterstopp. Beleg: 23.10. 18:05:54 Anforderung 9,5 min nach Stopp → Freigabe 18:11:44 = **Stopp + 15,4 min**, aber nur Anforderung + 5,8 min. Hier war HKA59 schon abgelaufen, WP011 hat begrenzt.
   - Formel, die alle 18 verzögerten Heizstarts 16.–23.10. erklärt: **Freigabe = max(Stopp + 15 min, Beginn „RL ≤ Soll − 1,5 K“ ununterbrochen + 15 min) + 0,1…0,9 min** (Abweichung −0,4…+0,9 min, 18/18) – **wahrscheinlich**.
3. **Kein Hoval-Modbus-Register zeigt die Wartezeit** – **sicher**: in allen 340 Wartepunkten des Volllogger (HK1 = 23, Verdichter aus) stand 18722 = 1 (nicht 2/28/29), 18723 = 0 (nicht 16), 1539 = 0; im 5-s-Raster X26 ebenfalls Status 0 bis zur Freigabe (dann 51 bzw. direkt 1). HoxPi findet zu „Verzögerung/Sperrzeit/Wartezeit/delay/Hysterese/Schaltdiff“ keinen Treffer.
4. **Sofortstarts (7×, Freigabe 0,4–0,7 min nach Anforderung)** passen nicht in „Bedingung ab Anforderung“: der Timer war offenbar schon abgelaufen. Gemeinsam ist allen: stehender RL ≤ 29,5 °C vor der Anforderung (Vorlauf-Analyse, hier bestätigt). Warum der Timer vorher lief: **Vermutung** (offen seit F29/F30).
5. **Abtauung/Reset:** Reset (Fehler 222, 18.10.) → nächster Start nach 1,9 min, also ohne WP011 – **sicher** (n = 1). Nach Abtauung laut Firmware nur 30 s statt WP011, im Volllogger 13.10. Pausen 9–10 min – **wahrscheinlich**. Ob HKA59 nach Abtauung zurückgesetzt wird: im Fenster 16.–23.10. kein Fall, **nicht geprüft**.
6. **Korrektur Vorlauf-Analyse:** Dort stand „der Verzug sitzt in der TTE-WEZ, nicht im Kältekreisregler“. Das stimmt so nicht: Der Zeitgeber ist ein Kälteregler-Parameter, den die TopTronic nur als 33-055 anzeigt. 1529 = 0 in der Wartezeit ist die Folge (keine Freigabe), nicht die Ursache – **wahrscheinlich**.

## Gefundene Parameter
Live-Wert = passiv aus dem X26-Mitschnitt 23.10.2026 (die TopTronic fragt die pCO-DB alle ~6 min ab). „Rücklesen“ = alle Lesungen des Tages gleich. Min/Max aus Firmware-Tabelle `[lokaler Pfad]` bzw. Bus-Katalog `pcodb_katalog_20260902_*.csv`.

| Bedienteil-Nr. / Mnemonic | pCO-DB | Bedeutung | Live-Wert 23.10. | Einheit | Min / Max | Lesungen (gleich) | Sicherheit |
|---|---|---|---|---|---|---|---|
| **33-055 / HKA59** | 0x811F | Heizkreis-Freigabeverzögerung: Bedingung „Temp. ≤ Soll − 33-054“ muss so lange ununterbrochen gelten | **15** | min | 1 / 240 (Werkswert 15, nicht in pax) | 199/199, letzte 20:03:49 | Wert sicher, Funktion wahrscheinlich |
| **WP011** | 0x821C | Mindeststehzeit Verdichter (ab Stopp) | **15** | min | 10 / 60 (Werk 10, pax 15) | 198/198, letzte 20:04:11 | Wert sicher, Funktion sicher (Firmware + Daten) |
| 33-054 / HV012 | 0x811E | Einschaltdifferenz Heizen | 1,0 | K | 0 / 100 (DB) | 199/199 | sicher |
| 33-053 / HV011 | 0x811D | Ausschaltdifferenz Heizen | 3,0 | K | 0 / 100 (DB) | 199/199 | sicher |
| WP010 | 0x821B | Mindestlaufzeit Verdichter | 5 | min | 5 / 25 | 198/198 | sicher |
| 33-070 / HKA60 | 0x812E | zweiter Heizkreis-/Kaltstart-Zeitgeber (Timer 0x13E) | 15 | min | 1 / 240 | 199/199 | Wert sicher, hier nicht bindend |
| 33-283 / CL014 | 0x8203 | Abtau-Zeitglied | 15 | min | 10 / 35 | 199/199 | Wert sicher (frühere Angabe „17 min“ aus f3z damit widerlegt) |
| HSA35 | – (keine DB-Adresse) | 5-min-Kurzweg für HKA59 | nicht lesbar | – | 0 / 1 (Werk 0) | – | wahrscheinlich 0 (nie 5-min-Start gesehen) |

Hoval-Modbus (HoxPi, `read_register`, 23.10. ~20:00, alle nur lesend):
| Reg | Name | Live | Einheit | Bemerkung |
|---|---|---|---|---|
| 18722 | Status Wärmeerzeugerregelung | 0 | – | kennt 2 „Vorlaufzeit Heizbetrieb“, 28 „Minimale Auszeit“, 29 „Minimale Einzeit“ – in Wartezeiten **nie** gesehen (immer 1) |
| 18723 | FA-Status (WFA) | 0 | – | kennt 16 „Wiedereinschaltverzögerung“ – in Wartezeiten **nie** gesehen (immer 0) |
| 1539 | WEZ-Status | 0 | – | 16 erscheint nur, wenn der Kälteregler schon eine Anforderung hat (Sept.: WW/Kühlen); bei Heiz-Wartezeiten 0 |
| 19873 | Sequenzwechsel (Zeit) | 0 | – | nicht relevant |
| 27541 | Zeitfilter Leistung gedämpft | 0,0 | min | Smart-Grid-Filter, nicht relevant |
Suchbegriffe ohne Treffer in HoxPi: Verzögerung, delay, Sperrzeit, Wartezeit, Schaltdiff, Hysterese (nur SG), Mindest (nur SG/Kühlen), Takt. Die offizielle Datenpunktliste enthält keinen Zeitparameter für den Heizstart. 33-055 ist im HoxPi-Katalog nicht als Register vorhanden; der Bedienteil-Katalog (`~/Bedienteil_Katalog.csv`) führt 33-055 nur als „Erweiterte Modulparameter = 0“ (CAN 06.09., als die FA-Datenpunkte nach dem Stromausfall stumm waren) – dieser Eintrag ist damit **überholt**.

## Heizstarts 16.–23.10. (alle Heiz-Anforderungen mit Start)
Spalten (alle Zeiten aus X26-`ZUSTAND`, ~5 s): **Anforderung** = HK1 springt auf 23 (Spalte `HK1`, = Modbus 1501; also Loxone-Heizruf). „vorher 6“ = Anforderung beginnt beim WW-Stopp. **Freigabe** = erster `status` 51 oder 1 (bei „nach WW“ = Verdichterstart, weil dort Status 4 noch ansteht). **Bed. ab** = Minute nach Anforderung, ab der `FARL` (WP-Rücklauf) ≤ 1520 − 1,5 K **ununterbrochen** bis zur Freigabe gilt (1520 aus Volllogger, 5 min). **Rest HKA59** = Freigabe − (Bed. + 15 min). **Rest WP011** = Freigabe − (Stopp + 15 min). Verdichterstart = `mod%` > 0.

| # | Anforderung | vorher | letzter Stopp | Stopp→Anf min | RL@Anf °C | 1520 °C | Freigabe | Anf→Frg min | Bed. ab min | **Rest HKA59** | **Rest WP011** | Verdichter | Klasse |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 16.10. 05:48:48 | 0 | – | – | 28,5 | 34,5 | 05:49:24 | 0,6 | 0,0 | −14,4 | – | 05:49:39 | sofort |
| 2 | 16.10. 06:43:52 | 6 | 06:43:27 | 0,4 | 54,0 | 40,0 | 07:03:08 | 19,3 | 3,8 | +0,4 | +4,7 | 07:03:08 | nach WW |
| 3 | 16.10. 12:43:51 | 6 | 12:43:20 | 0,5 | 59,0 | 38,5 | 13:03:01 | 19,2 | 3,6 | +0,5 | +4,7 | 13:03:01 | nach WW |
| 4 | 16.10. 13:18:28 | 0 | 13:07:56 | 10,5 | 30,5 | 38,5 | 13:34:21 | 15,9 | 0,0 | **+0,9** | +11,4 | 13:34:21 | frisch, HKA59 ab Anf. |
| 5 | 16.10. 14:48:34 | 0 | 13:59:07 | 49,5 | 26,5 | 38,0 | 14:49:00 | 0,4 | 0,0 | −14,6 | +34,9 | 14:49:20 | sofort |
| 6 | 16.10. 16:30:00 | 6 | 16:29:29 | 0,5 | 59,0 | 37,0 | 17:08:23 | 38,4 | 23,0 | +0,3 | +23,9 | 17:08:23 | nach WW, RL lange über Schwelle |
| 7 | 17.10. 08:25:08 | 0 | 07:16:41 | 68,5 | 35,0 | 34,5 | 08:41:34 | 16,4 | 1,4 | **+0,1** | +69,9 | 08:41:55 | frisch, lange Pause |
| 8 | 17.10. 09:15:46 | 0 | 09:05:45 | 10,0 | 31,5 | 33,5 | 09:58:54 | 43,1 | 27,6 | +0,5 | +38,1 | 09:59:09 | frisch, RL knapp am Soll |
| 9 | 17.10. 17:41:06 | 0 | 14:49:21 | 171,8 | 38,5 | 37,5 | 17:57:30 | 16,4 | 0,8 | **+0,6** | +173,2 | 17:57:35 | frisch, lange Pause |
| 10 | 18.10. 07:01:16 | 0 | 17.10. 22:46:52 | 494 | 28,0 | – | 07:01:46 | 0,5 | 0,0 | −14,5 | – | 07:02:07 | sofort |
| 11 | 18.10. 07:31:39 | 6 | 07:31:08 | 0,5 | 51,5 | 33,0 | 07:51:19 | 19,7 | 4,4 | +0,3 | +5,2 | 07:51:19 | nach WW |
| 12 | 18.10. 14:19:31 | 0 | 11:48:47 | 150,7 | 35,5 | 38,0 | 14:35:22 | 15,8 | 0,0 | **+0,8** | +151,6 | 14:38:30 | frisch, lange Pause |
| 13 | 18.10. 18:02:47 | 6 | 18:02:21 | 0,4 | 59,0 | 38,0 | 18:22:04 | 19,3 | 4,5 | −0,2 | +4,7 | 18:22:04 | nach WW |
| 14 | 19.10. 06:56:03 | 6 | 06:55:58 | 0,1 | 54,0 | 33,5 | 07:15:49 | 19,8 | 4,4 | +0,4 | +4,9 | 07:15:49 | nach WW |
| 15 | 19.10. 09:13:26 | 0 | 07:36:21 | 97,1 | 23,5 | 33,5 | 09:14:07 | 0,7 | 0,0 | −14,3 | +82,8 | 09:14:22 | sofort |
| 16 | 20.10. 06:59:38 | 6 | 06:59:18 | 0,3 | 52,0 | 34,0 | 07:19:02 | 19,4 | 4,0 | +0,4 | +4,7 | 07:19:02 | nach WW |
| 17 | 21.10. 15:24:20 | 0 | 07:05:43 | 498,6 | 28,5 | 32,0 | 15:24:45 | 0,4 | 0,0 | −14,6 | – | 15:25:10 | sofort |
| 18 | 21.10. 17:08:29 | 6 | 17:08:08 | 0,3 | 51,5 | 32,0 | 17:28:05 | 19,6 | 4,5 | +0,1 | +4,9 | 17:28:05 | nach WW |
| 19 | 22.10. 04:21:10 | 0 | 21.10. 20:50:32 | 450,6 | 29,0 | 34,5 | 04:21:45 | 0,6 | 0,0 | −14,4 | – | 04:22:10 | sofort |
| 20 | 22.10. 07:01:16 | 0 | 06:37:06 | 24,2 | 35,0 | 34,5 | 07:21:32 | 20,3 | 4,8 | +0,4 | +29,4 | 07:21:37 | frisch |
| 21 | 22.10. 07:52:30 | 0 | 07:50:03 | 2,5 | 36,0 | 34,5 | 08:18:14 | 25,7 | 10,6 | +0,1 | +13,2 | 08:18:40 | frisch, kurz nach Stopp |
| 22 | 23.10. 03:00:36 | 0 | 22.10. 18:59:17 | 481 | 27,5 | 36,0 | 03:01:06 | 0,5 | 0,0 | −14,5 | – | 03:01:26 | sofort |
| 23 | 23.10. 05:18:00 | 6 | 05:18:00 | 0,0 | 53,0 | 36,0 | 05:37:47 | 19,8 | 4,4 | +0,4 | +4,8 | 05:37:47 | nach WW |
| 24 | 23.10. 07:45:41 | 6 | 07:45:21 | 0,3 | 50,5 | 36,0 | 08:07:34 | 21,9 | 6,5 | +0,4 | +7,2 | 08:07:34 | nach WW, RL langsamer |
| 25 | 23.10. 17:15:53 | 0 | 16:42:09 | 33,7 | 33,0 | 33,0 | 17:36:50 | 20,9 | 6,3 | −0,4 | +39,7 | 17:37:16 | frisch |
| 26 | 23.10. 18:05:54 | 0 | 17:56:22 | 9,5 | 33,0 | 39,5 | 18:11:44 | 5,8 | 0,0 | −9,2 | **+0,4** | 18:11:49 | **WP011 begrenzt** |
| 27 | 23.10. 19:06:44 | 0 | 18:52:29 | 14,2 | 29,5 | 39,0 | 19:07:45 | 1,0 | 0,0 | −14,0 | **+0,3** | 19:07:45 | sofort, zugleich Stopp + 15,3 |
Nicht gewertet: 19.10. 18:56:39 (endete als WW-Start, HK1 → 6), 20.10. 12:19:23 (Daten 12:25–17:05 eingefroren). Ausgabe: `[lokaler Pfad]` und `_10.out`.

**Auswertung der Tabelle**
- **HKA59 (Bedingung + 15 min):** 18 von 18 verzögerten Starts (#2–4, 6–9, 11–14, 16, 18, 20, 21, 23–25) mit Rest **−0,4 … +0,9 min** – **sicher als Messung**, Zuordnung zu HKA59 **wahrscheinlich**. Mit der Firmware-Schwelle 1,0 K statt 1,5 K liegen nur 13/18 in ±1 min (#6 +4,1, #8 +9,4, je dreimal +1,1). Die gemessene Schwelle ist also ~1,5 K gegen 1520, die eingestellte 1,0 K (33-054). Die 0,5 K Unterschied: **Vermutung** – der Kälteregler vergleicht einen anderen Fühler oder einen eigenen Soll (X26-dp 0 in 0,5-K-Schritten) als FARL/1520.
- **Strikt „Start = Anforderung + 15 min ± 1“** (Bedingung schon bei Anforderung erfüllt, letzter Stopp > 15 min her): #4 +0,9, #12 +0,8 (Freigabe), dazu #7 und #9 mit +1,4, weil der RL dort erst 0,8–1,4 min nach der Anforderung unter die Schwelle fiel (gegen Bedingungsbeginn +0,1 / +0,6). Verdichterstart je nach Länge von Status 51 weitere 0,1–3,2 min später (#12: 3,1 min).
- **WP011 (Stopp + 15 min):** keine Freigabe vor Stopp + 15 min in 27 Fällen (kleinster Rest +0,3, #27). #26 ist der einzige Fall, in dem WP011 und nicht HKA59 begrenzt hat: Anforderung + 5,8 min = Stopp + 15,4 min – **sicher** (n = 1, #27 ist mit dem Sofortstart nicht trennbar).
- **„Nach WW“ = 19,2–21,9 min nach WW-Stopp** ist kein eigener Parameter: RL spült in 3,6–6,5 min unter die Schwelle, dann HKA59 15 min – **wahrscheinlich** (9/9 auf −0,2…+0,5). WP011 (Stopp + 15) liegt dort immer 4,7–7,2 min früher und bindet nie.
- **Sofort (#1, 5, 10, 15, 17, 19, 22, 27):** Freigabe 0,4–1,0 min nach Anforderung, stehender RL 23,5–29,5 °C. Rest HKA59 −14 bis −14,6 heißt: der 15-min-Timer war bei der Anforderung schon abgelaufen. Wie er ohne Anforderung laufen kann: **Vermutung** (Firmware: Timer 0x91 wird nur unter bestimmten Bedingungen zurückgesetzt, F29; der Auslöser „Lauf endete durch Loxone-Entzug“ trennt hier nicht – von den Sofortstarts folgten 4 von 5 auf einen Lauf mit Entzugsende, von den 8 frischen verzögerten aber auch 5 von 8, `or_f5_20261023_11.out`).
- **Warten ohne Statuscode:** Zwischen Anforderung und Freigabe stand `status` durchgehend 0 (z. B. #26 18:05:54–18:11:39, #12 14:19:31–14:35:17), danach 51 (Pumpen-Vorlauf, 0,1–3,2 min) oder direkt 1. Status 16 „Wiedereinschaltsperre“ trat im Heizfall nie auf – **sicher**.

## Ausnahmen „nach Abtauung / Reset“ (Teil der Frage)
| Ereignis | Beobachtung | Quelle | Sicherheit |
|---|---|---|---|
| Reset nach Fehler 222, 18.10. | Stopp 11:11:59 → Start 11:13:51 = **1,9 min** (weder WP011 noch HKA59) | X26 `ZUSTAND` 18.10. | sicher (n = 1) |
| Abtauung | Firmware: nach Betriebsart 8 nur 30 s statt WP011; Volllogger 13.10. 07:10–07:25 und 08:40–08:50: Status 8 → 16 (≤ 5 min) → 1, Pausen 9–10 min | `~/wez_status_evidenz/evidenz.csv`, `WP_Verhaltenskarte.md` Nachtrag 23.10. 17:00 | wahrscheinlich (5-min-Raster, 2 Fälle) |
| HKA59 nach Abtauung | kein Heizstart direkt nach Abtauung im Fenster 16.–23.10. | – | nicht geprüft |

## Einordnung
| Aussage | Stufe |
|---|---|
| 33-055 (HKA59) = 15 min, WP011 = 15 min, 33-054 = 1,0 K, 33-053 = 3,0 K, WP010 = 5 min (live, X26 23.10., alle Lesungen gleich) | **sicher** |
| Neben WP011 gibt es ein zweites 15-min-Zeitglied ab Anforderung/Bedingung (4 Starts nach 69–173 min Stillstand mit 15,8–16,4 min Wartezeit) | **sicher** |
| Dieses Zeitglied ist HKA59 (33-055) | **wahrscheinlich** (Firmware F26/F28 + 18/18 Starts auf −0,4…+0,9 min) |
| Beide Zeitglieder sitzen im Kälteregler, nicht in der TopTronic | **wahrscheinlich** (Parameter nur in der pCO-DB, kein TTE-Register, kein TTE-Statuscode) |
| WP011 kann allein begrenzen (23.10. 18:11:44 = Stopp + 15,4, Anforderung + 5,8) | **sicher** (n = 1) |
| Gemessene Schwelle ≈ Soll − 1,5 K (FARL gegen 1520); eingestellt 1,0 K | Messung sicher, Ursache des Versatzes **Vermutung** |
| Sofortstarts: Timer schon abgelaufen; Grund | **Vermutung** |
| Reset hebt die Sperren auf | **sicher** (n = 1) |
| Nach Abtauung nur kurze Sperre | **wahrscheinlich** |

## Was bringt uns das
- **Die Ursache ist benannt:** Der ~16–20-min-Startverzug nach einer Heizanforderung ist **33-055 = 15 min** (Bedingung muss 15 min halten) plus die Spülzeit des Rücklaufs. Nach WW sind das immer ~20 min, bei frischer Anforderung mit warmem Wasser ~16 min. WP011 bindet nur, wenn Loxone innerhalb von 15 min nach einem Stopp wieder anfordert.
- **Loxone kann den Verzug vorhersagen** (ohne Hoval-Eingriff): Verdichterstart ≈ max(Stopp + 15 min, Zeitpunkt „RL ≤ Soll − 1,5 K“ + 15 min) + 0,5–3 min. Damit lässt sich die Mindestlaufzeit ab echtem Verdichterstart rechnen (Vorschlag aus der Vorlauf-Analyse, Monoflop https://www.loxone.com/dede/kb/monoflop/ an „1539 = 1“). **Was bringt uns das:** Von MinHr 40 min bleiben nicht mehr nur ~20 min Lauf übrig, sondern volle 40 min; grob ~1 Start pro Tag weniger (Schätzung, nicht gemessen).
- **Hebel an der Anlage (nur Hoval-Service, nicht selbst):** 33-055 kürzer (z. B. 5 min) würde jeden Heizstart um ~10 min vorziehen und ~10 min Pumpenlauf ohne Verdichter je Start sparen. Der Taktschutz bliebe durch WP011 = 15 min erhalten. Das ist ein Kälteregler-Parameter: **niemals selbst schreiben** (Projektregel), nur mit des Betreibers Freigabe über den Hoval-Service, Rückweg 15 min. Ob 33-055 am Bedienteil in der Fachmannebene verstellbar ist: offen.
- **Monitoring:** Die Wartezeit ist in keinem Hoval-Register sichtbar. Wer sie sehen will, braucht X26 `ZUSTAND` (status 0 → 51/1) oder die Rechnung oben. 18722/18723 sind dafür wertlos.

## Fertig, wenn …?
- „Parameter mit Nummer und Live-Wert gelesen (Rücklesen)“: **erfüllt** – 33-055 (HKA59) = 15 min, 199 gleiche Lesungen; WP011 = 15 min, 198 gleiche Lesungen. Einschränkung: passiv mitgelesen (Abfragen der TopTronic über X26), kein eigenes aktives Lesen; über HoxPi/Modbus gibt es dafür kein Register.
- „Verhalten an ≥ 3 Heizstarts bestätigt (Start = Anforderung + Parameterzeit ± 1 min)“: **erfüllt** in der präzisierten Form: bei Bedingung schon zur Anforderung #4 (+0,9) und #12 (+0,8) strikt; #7/#9 +1,4 gegen Anforderung, aber +0,1/+0,6 gegen Bedingungsbeginn; insgesamt 18/18 verzögerte Starts auf −0,4…+0,9 min gegen „Bedingung + 15 min“.
- **Offen** (eigene Punkte, kein F5-Blocker): Klartext von 33-055 am Bedienteil abschreiben (Fachmann › WEZ › WFA-200/Kältekreis-Parameter, nur ansehen); Grund der Sofortstarts; Schwelle 1,0 vs. 1,5 K; HKA59 nach Abtauung.

## Rohdaten-Stichprobe zum Gegenprüfen
- `[lokaler Pfad]`: Zeile `20:03:49.648,811f,15` (33-055 = 15 min) und `20:04:11.505,821c,15` (WP011 = 15 min). Quelle `~/rs485_sniff/log/rs485_2026-10-23.log`, Decoder `~/rs485_sniff/rs485_pcodb.py --series 811f,821c`.
- `[lokaler Pfad]` (WP011-Fall #26): `17:56:22.207 … status=1 mod%=0 … HK1=0` (Stopp) → `18:05:54.374 … status=0 … FARL=33.0 … HK1=23` (Anforderung) → `18:11:44.616 … status=1 … HK1=23` (Freigabe = Stopp + 15:22) → `18:11:49.693 … mod%=17`.
- HKA59-Fall #12 im Volllogger `~/hoxpi_fulllog/2026-10-18.csv.gz`: 14:25/14:30/14:35 → 1501 = 23, 18768 = 100, 1529 = 0, 18722 = 1, 18723 = 0, 1539 = 0; X26 `or_f5_20261023_x26z_18.txt` 14:35:22 `status=51`.