# ANALYSE F47 — Die drei 222er-Ausfälle (E:31) im Vergleich (Orchestrator 29.10.2026 11:57)

Quelle: Volllogger `/home/<user>/hoxpi_fulllog/2026-08-29.csv.gz`, `2026-09-07.csv.gz`, `2026-10-29.csv` (5-min-Raster, nur gelesen per `hoxpi_ssh.py` + awk).
Spalten: 1534 Fehler, 1539 WEZ-Status, 1540, 1543, 1477 Aussen ×10, 1525 WP-VL ×10, 25611 P_el ×100. Ausgegeben wurden nur Zeilen mit Zustandswechsel.

## Tabelle

| Fall | Beginn (erste Probe 222) | Ende (erste Probe 255) | Dauer (Raster) | Zustand davor (Probe vorher) | 1539/1540/1543 im Fehler | Werte im Fehler | Rückkehr |
|---|---|---|---|---|---|---|---|
| 29.08.2026 | 20:10 | 20:20 | 10–15 min | 19:45: 1539 = 0 (Aus), P_el 0; 19:25–19:35 vorher **1534 = 190** (1539 0, 1540 8, 1543 20), 19:40 Lauf 1539 2 (1,54 kW) | 17 / 8 / 81 | Standbild (2 Proben identisch: Aussen 20,0 °C, VL 18,5 °C, P_el 0) | 20:20 direkt 1539 = 0 |
| 07.09.2026 | 18:15 | 18:40 | 25–30 min | 17:55: 1539 = 2, 1543 4, P_el 1,85 kW, Aussen 24,3 °C | 17 / 8 / 84 | Standbild (5 Proben identisch: Aussen 23,2, VL 15,5, P_el 1,36 kW); am selben Tag 08:40–08:50 **1534 = 124**, 1539 = 98 | 18:40 direkt 1539 = 2 (Lauf, 1,67 kW) |
| 29.10.2026 | 08:55 | 10:45 | 110–115 min | 08:00–08:50: 1539 = 1 (Heizlauf), P_el 1,68–1,85 kW, Aussen ~6 °C | 17 / 8 / **1** | Standbild (22 Proben identisch: Aussen 6,3, VL 39,5, P_el 1,85 kW) | 10:45 1539 = 51, 10:50 = 1 (1,83 kW), 10:55 = 0 |

## Befunde
- **Gleiche Signatur 1539 = 17 / 1540 = 8 in allen drei Fällen** [sicher]. Die Werte im Fehler sind in allen drei Fällen ein Standbild (alle Spalten konstant), d. h. die WEZ antwortet in allen drei Fällen nicht — nicht nur am 29.10. [sicher für die gezeigten Spalten; ob X26 am 29.08./07.09. ebenfalls still war, ist noch nicht geprüft].
- **Unterschied 1543:** 81 bzw. 84 in den Sommerfällen, 1 am 29.10. [sicher]. Bedeutung von 1543 hier unklar [Vermutung: 1543 wurde am 29.10. vor dem Ausfall nicht mehr aktualisiert bzw. zeigt anderen Teilzustand].
- **Vorbote:** 29.08. 19:25 kam 35 min vorher ein anderer Fehler (1534 = 190), 07.09. morgens 1534 = 124; am 29.10. kein anderer Fehlercode im 5-min-Raster davor [sicher im Raster].
- **Ausfall aus laufendem Verdichter** in 2 von 3 Fällen (07.09., 29.10.); 29.08. aus Stillstand [sicher].
- **Keine Blockierphase nach Rückkehr:** in keinem Fall folgt nach der ersten 255-Probe noch einmal 222; 1539 = 51 vor einem Start kommt auch an normalen Tagen vor (29.08. 10:40, 07.09. 01:00, 13:35) [sicher] ⇒ 51 ist ein normaler Anlaufzustand, kein Fehlernachlauf [wahrscheinlich]. Das spricht gegen V125 (a) [wahrscheinlich, Raster 5 min].
- **Dauer wächst:** 10–15 → 25–30 → 110 min [sicher]; ob das ein Trend ist, lässt sich aus drei Fällen nicht sagen [Vermutung].

## Offen (für die nächsten Teilschritte)
1. X26-Rohlog `~/rs485_sniff/log/` für 29.08. 20:05–20:25 und 07.09. 18:10–18:45: war der Kälteregler ebenfalls still? (nur lesen)
2. Bedeutung 1534 = 222 / 190 / 124 und E31/Code 36 in der offiziellen Hoval-Datenpunktliste (Vault) und öffentlichen iDM-Fehlerlisten (Recherche).
3. Vor-Ort (Display-Fehlerhistorie) erst danach.

**Was bringt uns das:** Der 29.10. ist kein neues Fehlerbild, sondern derselbe Ausfalltyp wie im Sommer, nur deutlich länger. Ein Wächter „1534 = 222 oder WEZ-Standbild > 10 min“ würde alle drei Fälle erkennen.

## Nachtrag Orchestrator 29.10.2026 12:59 - X26 je Minute (Teilschritt 1) und Abgleich 19.09.
Skripte `[lokaler Pfad]`, `or_f47f17b_20261029_1300.py`, `or_f47c_20261029_1300.py` (nur lesen, am Pi in /tmp).

| Fall | X26 Rohrahmen | X26-Zustand im 222-Fenster | Deutung |
|---|---|---|---|
| 29.08. | 0/min 20:08-20:17 (10 min), passt zu 222 20:10-20:20; dazu 0/min 19:53-19:54 vor Sniffer-Neustart 19:55 | - | beide Busse still wie 29.10. -> Inneneinheit stromlos/haengt [wahrscheinlich] |
| 07.09. | vor 18:39:53 loggte der Sniffer nur ZUSTAND (keine Rohzeilen) -> Stille nicht pruefbar | aendert sich laufend: Start 17:52 (mod 10 %), Stopp 18:36:40, Start 18:38:42, ZYK 20405 -> 20407, AT 24,3 -> 21,5 C | Kaelteregler und X26 aktiv, nur CAN-Antworten der WEZ fehlten -> **anderer Typ** als 29.08./29.10. [wahrscheinlich] |
| 29.10. | 0/min 08:55-10:41 (108 min), ab 10:42:28 wieder | Standwerte (ZUSTAND laeuft mit alten Werten weiter) | des Betreibers Abschaltung [sicher] |
| 19.09. ~21:11 (des Betreibers Strom-Aus/Ein laut F17) | keine Stille, nur 21:10/21:11 weniger Rahmen (1319/998 statt ~1930) | - | Volllogger 20:45-21:45 durchgehend 1534 = 255, 1539 = 0 -> kein 222-Fall, Inneneinheit nicht (oder < 1 min) stromlos [sicher im Raster] |

- **ZUSTAND-Zeilen des X26-Sniffers sind kein Ausfallindikator:** am 29.10. liefen sie in der Stille alle 30 s mit Standwerten weiter [sicher]. Waechter muessen Rohrahmen je Minute zaehlen.
- 222 mit 1539 = 17 / 1540 = 8 tritt sowohl bei stromloser Inneneinheit (29.10., sehr wahrscheinlich 29.08.) als auch bei laufendem X26 (07.09.) auf -> E:31 ist kein reines "Strom weg"-Signal [wahrscheinlich].
- Offen nur noch: Bedeutung E31/Code 36 aus oeffentlicher Quelle (Recherche als MD-13 nach Argon-Reset 02.11.), danach erst Vor-Ort (Fehlerhistorie).

**Was bringt uns das:** Der Ausfallwaechter muss "X26-Rohrahmen = 0 fuer >= 2 min" (Inneneinheit weg) und "WEZ-Standbild auf CAN bei laufendem X26" (07.09.-Typ) getrennt melden; die ZUSTAND-Zeile taugt dafuer nicht.

## Nachtrag Orchestrator 29.10.2026 13:56 - Bedeutung E:31 / Code 36 (Teilschritt 2, F47 damit erledigt)
- **Zuordnung lokal [sicher]:** `[lokaler Pfad]` Zeile `18,0x12,E:31,222,36,2,0,1` = Alarm-Idx 18, Errlog `E:31`, Modbus 1534 = 222, Kennung 36 (deckt sich mit der Kopfzeile von F47).
- **Hoval-Wortlaut:** oeffentlich nicht auffindbar (R33 Abschn. 3, sicher). Dass Hoval die iDM-Kennung 36 umgewidmet hat, ist nicht belegt [Vermutung, unwahrscheinlich].
- **Deutung fuer unsere Faelle [Vermutung]:** E:31 meldet "STB-Kette der Heizung offen". Bei Abschaltung von Hand (29.10., sehr wahrscheinlich 29.08. Fachmann-Durchgang) faellt die Spannung am STB-Eingang (Heizstab hat eigene Sicherung) oft kurz vor der Steuerung weg -> E:31 als Abschalt-Artefakt, danach beide Busse still. Der 07.09.-Typ (X26 lief weiter, nur CAN-Standbild) passt dazu nicht und bleibt ungeklaert.
- **MD-13 (E31-Recherche fuer Argon) entfaellt** - Argon-Kontingent bleibt fuer MD-01.

**Was bringt uns das:** E:31 heisst nicht "Kommunikationsfehler", sondern STB/Heizstab-Kette. Nach einer Abschaltung von Hand ist es harmlos (Regel Strom-Aus). Tritt E:31 im Winter bei laufender WP ohne Abschaltung auf (07.09.-Typ), dann STB und Sicherung des 6-kW-Heizstabs pruefen lassen - nicht am Bus suchen. Nichts an der Anlage geaendert.