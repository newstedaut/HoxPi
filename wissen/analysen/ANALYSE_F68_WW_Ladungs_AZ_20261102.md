# ANALYSE F68 – WW-Ladungen: Arbeitszahl je Ladung, Zusammenlegen vs. Verschieben (02.11.2026, Claude Code, nur lesend)

**Ergebnis in 5 Zeilen**
1. 109 auswertbare WW-Ladungen (01.10.–01.11.2026, 111 Blöcke, 2 ausgeschlossen). Gepoolte AZ gesamt **3,10** (704 kWh_th / 227,3 kWh_el). **[sicher]** (Summen über Zähler 27489 und 1-min-P_el; E_el gegengeprüft mit Zähler 25614: 227 kWh)
2. Die AZ hängt vor allem an der Außentemperatur: **+0,081 AZ je K AT** (±0,007, R² 0,56), Start-1500 nur −0,026 je K (±0,013). **[wahrscheinlich]**
3. **Teuer (AZ < 2,8): 26 von 109 Ladungen**, gepoolt AZ 2,56; Merkmale: kalt (AT-Mittel 6,7 °C statt 11,7) und klein (4,7 kWh_th je Ladung statt 7,0). 10 der 26 sind Morgenladungen (04:30–07:30). **[wahrscheinlich]** (Einzel-AZ grob wegen 1-kWh-Auflösung)
4. Gepoolt: Morgen **2,83** (AT 7,6 °C) – Nachmittag 12–17 **3,30** (AT 13,3 °C) – Nacht 22–04:30 **3,08**. **[sicher]** für die Summen, **[wahrscheinlich]**, dass der Unterschied fast ganz von der AT kommt.
5. **Verschieben** der Morgenladung auf den Nachmittag: ≈ **1,5 kWh_el/Woche**. **Zusammenlegen** (weniger, größere Ladungen): brutto 2,7–8,4, netto grob **1–4,5 kWh_el/Woche** (Szenario „Abstand < 4 h zusammen“). Zusammenlegen bringt **wahrscheinlich mehr**, die Untergrenzen überlappen aber. **[Vermutung]** für die Netto-Zahlen.

---

## 1. Frage
Katalogfrage F68: Arbeitszahl (AZ) je WW-Ladung gegen Starttemperatur WW oben (Reg 1500), Uhrzeit, Außentemperatur (Reg 1477) und Ladedauer. Welche Ladungen sind teuer (AZ < 2,8)? Bringt Zusammenlegen (weniger, größere Ladungen; je Ladung Fixanteil Q0 ≈ 1,3–2,2 kWh_th für Wärmetauscher/Leitungen) mehr als Verschieben der Morgenladung (04:30–07:30, Soll 52 °C) auf den Nachmittag (13:00–16:00)?

## 2. Datenquelle (nur gelesen)
- Volllogger-Kopien: `[lokaler Pfad]` … `2026-10-22.csv.gz`, `[lokaler Pfad]` … `2026-11-02.csv` (9.252 Zeilen, 5-min-Raster, 2026-10-01 00:00:02 bis 2026-11-02 01:55:01). Spalten: 1500 (WW oben ×10), 27483 (WW unten ×10), 1477 (AT ×10), 1539 (WEZ-Betriebsart, 4 = WW-Ladung), 25611 (P_el ×100 kW), 27489 (Wärmezähler WW, kWh), 25614 (elektr. Energiezähler, kWh), 1497 (WW-Soll ×10).
- 1-min-Reihe während WW-Ladung: `[lokaler Pfad]` (Spalten `25611_pel` in kW, `27489_q_ww`, `25614_e_el`).
- Vorarbeit (nur Köpfe gelesen): `[lokaler Pfad]` (111 WW-Läufe im selben Zeitraum, deckt sich mit meinen 111 Blöcken), `[lokaler Pfad]` (C = 0,47 kWh/K, Q0 ≈ 1,3 kWh, Ruheverlust).
- Skript: `[lokaler Pfad]` (Aufruf ohne Argument = Auswertung; mit Ladungsnummern, z. B. `11 57 62`, = Rohzeilen-Stichprobe). Kein Bus-, HoxPi- oder Loxone-Zugriff, nichts geschrieben außer Skript und dieser Datei.

## 3. Methode
- **Ladung** = zusammenhängende 5-min-Zeilen mit 1539 = 4 (Lücke > 10 min trennt). Beginn/Ende = erste/letzte Zeile mit 1539 = 4, Dauer = Ende − Beginn + 5 min. **[sicher]**
- **1500 Start** = Zeile vor Beginn; **1500 Ende** = Maximum der letzten Ladezeile und der zwei Folgezeilen (der obere Fühler steigt nach Ladeende noch 1–2 K nach). **AT** = Mittel 1477 über die Ladezeilen.
- **Q** = 27489 (Zeile Ende+2, höchstens bis vor die nächste Ladung) − 27489 (Zeile vor Beginn). Die +2 Zeilen fangen die bis zu 60 s alten WEZ-Werte ab. Auflösung 1 kWh → bei Q ≈ 5 kWh ±20 % auf die Einzel-AZ. **[sicher]**
- **E_el** = Integral 25611 aus `ww_abnahme.csv` (1-min, Abdeckung ≥ 85 % – bei allen 109 Ladungen erfüllt); Ersatz wäre Summe 25611 × 5 min. Gegenprobe über alle 109: 1-min 227,3 kWh, 5-min 229,6 kWh, Zähler 25614 227 kWh. **[sicher]**
- **Ausschlüsse:** (a) P_el-Mittel < 0,3 kW (PV-Stab/Legionellen) – trifft keinen Block mit 1539 = 4; (b) 01.11. ab 12:00 (Legionellen-/PV-Stab-Phase laut Auftrag) – 1 Block (01.11. 13:05, hatte aber P_el > 0, siehe Offen); (c) Rücksprung im Zähler 27489 innerhalb der Ladung – 1 Block (18.10. 10:35, siehe Stichprobe 2).
- **Pooling:** AZ je Klasse = ΣQ / ΣE_el (gleicht die 1-kWh-Auflösung aus). **Regression:** AZ = a + b·AT + c·1500Start, gewichtet mit Q, nur Q ≥ 3 kWh (n = 104); dazu E_el = α·Q + β (β = elektrischer Fixanteil je Ladung).
- **Wochenwerte** = Monatssumme × 7/32 (32 Tage, 01.10.–01.11.).

## 4. Ergebnis

### 4.1 Alle Ladungen
Quelle je Zeile: Volllogger-Datei des Beginn-Datums (`…\vorhernachher_20261024\<Datum>.csv[.gz]`), Zeitstempel = Beginn; E_el aus `ww_abnahme.csv` im selben Zeitfenster. Temperaturen °C, Q kWh_th, E_el kWh_el.

| # | Beginn | Ende | Dauer min | 1500 Start | 1500 Ende | AT Mittel | Soll 1497 | Q kWh | E_el kWh | Quelle E | AZ | Klasse |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 01.10. 13:55 | 14:10 | 20 | 52,3 | 56,1 | 19,6 | 57,0 | 4 | 0,91 | 1min | 4,37 | Nachmittag 12-17 |
| 2 | 02.10. 16:40 | 17:20 | 45 | 46,7 | 52,1 | 19,5 | 57,0 | 9 | 2,27 | 1min | 3,97 | Nachmittag 12-17 |
| 3 | 02.10. 23:25 | 00:00 | 40 | 49,9 | 53,1 | 13,6 | 57,0 | 6 | 1,90 | 1min | 3,15 | Nacht 22-04:30 |
| 4 | 03.10. 10:50 | 11:25 | 40 | 50,0 | 53,0 | 13,9 | 57,0 | 6 | 1,73 | 1min | 3,46 | Vormittag 07:30-12 |
| 5 | 03.10. 13:25 | 13:55 | 35 | 51,3 | 56,3 | 17,4 | 57,0 | 6 | 1,50 | 1min | 3,99 | Nachmittag 12-17 |
| 6 | 04.10. 01:15 | 01:45 | 35 | 45,2 | 50,7 | 11,2 | 50,0 | 5 | 1,59 | 1min | 3,14 | Nacht 22-04:30 |
| 7 | 04.10. 10:25 | 10:45 | 25 | 45,1 | 50,4 | 13,5 | 50,0 | 5 | 1,35 | 1min | 3,72 | Vormittag 07:30-12 |
| 8 | 04.10. 12:10 | 12:55 | 50 | 49,3 | 57,0 | 16,7 | 57,0 | 7 | 2,13 | 1min | 3,29 | Nachmittag 12-17 |
| 9 | 04.10. 16:50 | 18:00 | 75 | 51,5 | 53,7 | 19,5 | 57,0 | 13 | 3,40 | 1min | 3,82 | Nachmittag 12-17 |
| 10 | 04.10. 22:25 | 23:00 | 40 | 45,6 | 50,8 | 13,6 | 50,0 | 8 | 2,17 | 1min | 3,68 | Nacht 22-04:30 |
| 11 | 05.10. 06:05 | 06:40 | 40 | 47,2 | 53,0 | 12,0 | 52,0 | 5 | 1,73 | 1min | 2,90 | Morgen 04:30-07:30 |
| 12 | 05.10. 11:50 | 12:25 | 40 | 45,5 | 53,0 | 16,6 | 57,0 | 7 | 2,05 | 1min | 3,42 | Vormittag 07:30-12 |
| 13 | 05.10. 15:10 | 15:40 | 35 | 52,1 | 56,5 | 18,7 | 57,0 | 6 | 1,46 | 1min | 4,10 | Nachmittag 12-17 |
| 14 | 05.10. 20:30 | 21:30 | 65 | 46,7 | 52,5 | 13,4 | 52,0 | 10 | 3,21 | 1min | 3,12 | Abend 17-22 |
| 15 | 06.10. 06:15 | 06:55 | 45 | 46,9 | 52,1 | 9,3 | 57,0 | 7 | 2,20 | 1min | 3,18 | Morgen 04:30-07:30 |
| 16 | 06.10. 11:50 | 12:25 | 40 | 48,0 | 56,3 | 14,4 | 57,0 | 6 | 1,80 | 1min | 3,34 | Vormittag 07:30-12 |
| 17 | 06.10. 23:45 | 00:25 | 45 | 45,2 | 52,8 | 10,1 | 52,0 | 7 | 2,24 | 1min | 3,12 | Nacht 22-04:30 |
| 18 | 07.10. 06:40 | 07:10 | 35 | 47,2 | 52,5 | 8,2 | 52,0 | 4 | 1,53 | 1min | 2,62 | Morgen 04:30-07:30 |
| 19 | 07.10. 12:15 | 13:15 | 65 | 45,2 | 56,9 | 15,6 | 50,0 | 10 | 2,84 | 1min | 3,52 | Nachmittag 12-17 |
| 20 | 07.10. 17:50 | 18:00 | 15 | 50,7 | 51,7 | 17,6 | 57,0 | 2 | 0,59 | 1min | 3,38 | Abend 17-22 |
| 21 | 07.10. 19:30 | 20:05 | 40 | 49,1 | 52,4 | 13,5 | 57,0 | 6 | 1,72 | 1min | 3,49 | Abend 17-22 |
| 22 | 08.10. 05:25 | 06:00 | 40 | 47,2 | 52,8 | 11,6 | 52,0 | 5 | 1,73 | 1min | 2,89 | Morgen 04:30-07:30 |
| 23 | 08.10. 08:05 | 08:50 | 50 | 47,5 | 52,7 | 12,0 | 57,0 | 9 | 2,60 | 1min | 3,47 | Vormittag 07:30-12 |
| 24 | 08.10. 12:40 | 13:05 | 30 | 51,7 | 56,3 | 16,9 | 57,0 | 4 | 1,22 | 1min | 3,28 | Nachmittag 12-17 |
| 25 | 08.10. 17:35 | 18:15 | 45 | 50,6 | 53,0 | 14,7 | 52,0 | 8 | 2,41 | 1min | 3,32 | Abend 17-22 |
| 26 | 09.10. 00:25 | 00:50 | 30 | 45,1 | 51,0 | 10,5 | 50,0 | 5 | 1,47 | 1min | 3,39 | Nacht 22-04:30 |
| 27 | 09.10. 06:45 | 07:25 | 45 | 47,2 | 52,7 | 9,4 | 52,0 | 5 | 1,96 | 1min | 2,55 | Morgen 04:30-07:30 |
| 28 | 09.10. 16:00 | 16:50 | 55 | 45,9 | 56,6 | 13,4 | 57,0 | 9 | 2,58 | 1min | 3,49 | Nachmittag 12-17 |
| 29 | 10.10. 00:10 | 00:50 | 45 | 46,7 | 52,5 | 9,1 | 52,0 | 7 | 2,36 | 1min | 2,96 | Nacht 22-04:30 |
| 30 | 10.10. 11:45 | 12:35 | 55 | 45,7 | 52,8 | 10,3 | 50,0 | 8 | 2,47 | 1min | 3,24 | Vormittag 07:30-12 |
| 31 | 10.10. 17:10 | 17:30 | 25 | 44,9 | 50,8 | 11,7 | 50,0 | 4 | 1,41 | 1min | 2,84 | Abend 17-22 |
| 32 | 11.10. 04:35 | 05:10 | 40 | 45,9 | 52,8 | 8,7 | 52,0 | 6 | 1,87 | 1min | 3,22 | Morgen 04:30-07:30 |
| 33 | 11.10. 11:35 | 12:10 | 40 | 45,3 | 50,6 | 11,3 | 50,0 | 5 | 1,74 | 1min | 2,88 | Vormittag 07:30-12 |
| 34 | 11.10. 18:00 | 18:30 | 35 | 45,3 | 51,1 | 10,4 | 50,0 | 4 | 1,49 | 1min | 2,69 | Abend 17-22 |
| 35 | 11.10. 20:50 | 21:50 | 65 | 47,2 | 52,4 | 9,2 | 57,0 | 11 | 3,41 | 1min | 3,22 | Abend 17-22 |
| 36 | 12.10. 07:05 | 07:35 | 35 | 47,3 | 50,6 | 7,0 | 52,0 | 5 | 1,83 | 1min | 2,73 | Morgen 04:30-07:30 |
| 37 | 12.10. 12:15 | 12:55 | 45 | 48,7 | 56,5 | 12,1 | 57,0 | 7 | 2,22 | 1min | 3,16 | Nachmittag 12-17 |
| 38 | 12.10. 19:30 | 20:15 | 50 | 46,9 | 52,7 | 8,1 | 57,0 | 7 | 2,70 | 1min | 2,59 | Abend 17-22 |
| 39 | 13.10. 05:55 | 06:40 | 50 | 47,2 | 52,4 | 2,8 | 52,0 | 6 | 2,36 | 1min | 2,54 | Morgen 04:30-07:30 |
| 40 | 13.10. 12:10 | 12:55 | 50 | 48,1 | 56,6 | 9,7 | 57,0 | 7 | 2,27 | 1min | 3,08 | Nachmittag 12-17 |
| 41 | 13.10. 20:25 | 21:10 | 50 | 45,2 | 52,7 | 10,0 | 52,0 | 8 | 2,55 | 1min | 3,14 | Abend 17-22 |
| 42 | 14.10. 06:20 | 07:05 | 50 | 47,6 | 54,5 | 9,7 | 52,0 | 8 | 2,37 | 1min | 3,38 | Morgen 04:30-07:30 |
| 43 | 14.10. 16:10 | 16:35 | 30 | 45,1 | 51,4 | 14,0 | 50,0 | 4 | 1,42 | 1min | 2,82 | Nachmittag 12-17 |
| 44 | 14.10. 19:50 | 20:35 | 50 | 45,2 | 53,0 | 10,8 | 52,0 | 9 | 2,55 | 1min | 3,53 | Abend 17-22 |
| 45 | 15.10. 05:40 | 06:25 | 50 | 47,3 | 52,7 | 9,1 | 52,0 | 7 | 2,30 | 1min | 3,04 | Morgen 04:30-07:30 |
| 46 | 15.10. 13:40 | 14:20 | 45 | 46,9 | 56,3 | 14,3 | 57,0 | 7 | 2,03 | 1min | 3,44 | Nachmittag 12-17 |
| 47 | 15.10. 18:25 | 19:20 | 60 | 50,7 | 53,1 | 12,3 | 57,0 | 9 | 2,79 | 1min | 3,22 | Abend 17-22 |
| 48 | 15.10. 21:00 | 21:55 | 60 | 49,2 | 52,3 | 9,7 | 57,0 | 10 | 3,20 | 1min | 3,12 | Abend 17-22 |
| 49 | 16.10. 06:10 | 06:40 | 35 | 47,3 | 52,3 | 6,3 | 52,0 | 5 | 1,77 | 1min | 2,83 | Morgen 04:30-07:30 |
| 50 | 16.10. 12:00 | 12:40 | 45 | 50,1 | 56,6 | 11,3 | 57,0 | 7 | 2,02 | 1min | 3,46 | Nachmittag 12-17 |
| 51 | 16.10. 16:05 | 16:25 | 25 | 52,3 | 56,2 | 15,4 | 57,0 | 4 | 1,22 | 1min | 3,27 | Nachmittag 12-17 |
| 52 | 17.10. 06:40 | 07:15 | 40 | 47,2 | 52,8 | 7,1 | 52,0 | 5 | 1,74 | 1min | 2,87 | Morgen 04:30-07:30 |
| 53 | 17.10. 11:45 | 12:15 | 35 | 45,2 | 51,0 | 12,6 | 50,0 | 6 | 1,77 | 1min | 3,38 | Vormittag 07:30-12 |
| 54 | 17.10. 14:05 | 14:45 | 45 | 48,4 | 56,3 | 15,7 | 57,0 | 6 | 1,97 | 1min | 3,05 | Nachmittag 12-17 |
| 55 | 17.10. 21:50 | 22:45 | 60 | 45,2 | 50,7 | 11,9 | 50,0 | 12 | 3,32 | 1min | 3,61 | Abend 17-22 |
| 56 | 18.10. 07:05 | 07:30 | 30 | 47,3 | 50,8 | 10,1 | 52,0 | 4 | 1,32 | 1min | 3,04 | Morgen 04:30-07:30 |
| 57 | 18.10. 10:35 | 11:45 | 75 | 45,2 | 52,8 | 11,7 | 50,0 | 5 | 3,86 | 1min | - (Zaehler 27489 Ruecksprung) | Vormittag 07:30-12 |
| 58 | 18.10. 15:45 | 15:55 | 15 | 52,4 | 54,1 | 16,6 | 57,0 | 2 | 0,67 | 1min | 3,00 | Nachmittag 12-17 |
| 59 | 18.10. 17:25 | 18:00 | 40 | 52,5 | 56,6 | 14,6 | 57,0 | 6 | 1,71 | 1min | 3,51 | Abend 17-22 |
| 60 | 19.10. 06:00 | 06:55 | 60 | 47,2 | 52,7 | 9,6 | 52,0 | 9 | 3,12 | 1min | 2,88 | Morgen 04:30-07:30 |
| 61 | 19.10. 11:30 | 11:50 | 25 | 45,2 | 50,8 | 11,3 | 50,0 | 4 | 1,32 | 1min | 3,04 | Vormittag 07:30-12 |
| 62 | 19.10. 14:00 | 14:40 | 45 | 50,0 | 56,3 | 14,6 | 57,0 | 7 | 2,03 | 1min | 3,45 | Nachmittag 12-17 |
| 63 | 19.10. 16:55 | 17:00 | 10 | 52,4 | 53,2 | 15,2 | 57,0 | 1 | 0,41 | 1min | 2,46 | Nachmittag 12-17 |
| 64 | 19.10. 17:30 | 18:30 | 65 | 52,7 | 52,8 | 13,4 | 57,0 | 9 | 2,67 | 1min | 3,37 | Abend 17-22 |
| 65 | 19.10. 19:15 | 19:40 | 30 | 52,1 | 54,5 | 11,2 | 57,0 | 4 | 1,36 | 1min | 2,93 | Abend 17-22 |
| 66 | 20.10. 06:15 | 06:55 | 45 | 47,1 | 52,3 | 8,9 | 52,0 | 7 | 2,19 | 1min | 3,19 | Morgen 04:30-07:30 |
| 67 | 20.10. 11:40 | 12:15 | 40 | 50,8 | 56,8 | 10,8 | 57,0 | 5 | 1,76 | 1min | 2,84 | Vormittag 07:30-12 |
| 68 | 21.10. 04:00 | 04:25 | 30 | 45,1 | 51,0 | 14,2 | 50,0 | 5 | 1,42 | 1min | 3,53 | Nacht 22-04:30 |
| 69 | 21.10. 06:40 | 07:05 | 30 | 47,1 | 52,5 | 14,4 | 52,0 | 4 | 1,28 | 1min | 3,12 | Morgen 04:30-07:30 |
| 70 | 21.10. 16:40 | 17:05 | 30 | 45,2 | 50,7 | 13,2 | 50,0 | 4 | 1,33 | 1min | 3,00 | Nachmittag 12-17 |
| 71 | 21.10. 19:30 | 20:50 | 85 | 45,2 | 52,8 | 10,8 | 50,0 | 15 | 4,71 | 1min | 3,18 | Abend 17-22 |
| 72 | 22.10. 05:50 | 06:35 | 50 | 47,3 | 52,7 | 6,9 | 52,0 | 6 | 2,29 | 1min | 2,62 | Morgen 04:30-07:30 |
| 73 | 22.10. 10:00 | 11:30 | 95 | 47,3 | 52,4 | 7,8 | 57,0 | 18 | 5,90 | 1min | 3,05 | Vormittag 07:30-12 |
| 74 | 22.10. 13:20 | 13:50 | 35 | 52,1 | 56,9 | 10,9 | 57,0 | 5 | 1,61 | 1min | 3,12 | Nachmittag 12-17 |
| 75 | 22.10. 18:40 | 18:55 | 20 | 52,4 | 52,1 | 6,8 | 52,0 | 2 | 0,95 | 1min | 2,11 | Abend 17-22 |
| 76 | 23.10. 04:35 | 05:15 | 45 | 46,1 | 52,4 | 2,2 | 52,0 | 6 | 2,21 | 1min | 2,71 | Morgen 04:30-07:30 |
| 77 | 23.10. 07:25 | 07:45 | 25 | 47,2 | 50,1 | 1,9 | 52,0 | 2 | 1,13 | 1min | 1,77 | Morgen 04:30-07:30 |
| 78 | 23.10. 14:15 | 14:40 | 30 | 45,1 | 51,1 | 9,1 | 50,0 | 5 | 1,37 | 1min | 3,66 | Nachmittag 12-17 |
| 79 | 23.10. 16:05 | 16:40 | 40 | 51,3 | 56,8 | 10,6 | 57,0 | 4 | 1,66 | 1min | 2,41 | Nachmittag 12-17 |
| 80 | 24.10. 05:30 | 06:05 | 40 | 45,2 | 50,7 | 5,4 | 50,0 | 6 | 2,06 | 1min | 2,91 | Morgen 04:30-07:30 |
| 81 | 24.10. 10:50 | 11:20 | 35 | 45,5 | 50,4 | 5,9 | 50,0 | 6 | 1,87 | 1min | 3,21 | Vormittag 07:30-12 |
| 82 | 24.10. 14:30 | 15:05 | 40 | 47,2 | 52,4 | 7,8 | 52,0 | 5 | 1,85 | 1min | 2,71 | Nachmittag 12-17 |
| 83 | 25.10. 01:10 | 01:40 | 35 | 45,2 | 50,7 | 3,3 | 50,0 | 4 | 1,63 | 1min | 2,45 | Nacht 22-04:30 |
| 84 | 25.10. 09:25 | 10:00 | 40 | 46,3 | 50,3 | 4,2 | 50,0 | 5 | 2,01 | 1min | 2,49 | Vormittag 07:30-12 |
| 85 | 25.10. 14:10 | 14:55 | 50 | 45,2 | 52,5 | 6,0 | 52,0 | 7 | 2,45 | 1min | 2,85 | Nachmittag 12-17 |
| 86 | 25.10. 23:00 | 23:25 | 30 | 45,5 | 50,8 | 5,4 | 50,0 | 4 | 1,56 | 1min | 2,57 | Nacht 22-04:30 |
| 87 | 26.10. 09:20 | 10:00 | 45 | 45,2 | 50,4 | 5,9 | 50,0 | 7 | 2,16 | 1min | 3,25 | Vormittag 07:30-12 |
| 88 | 26.10. 12:10 | 12:40 | 35 | 45,1 | 50,7 | 9,5 | 50,0 | 5 | 1,66 | 1min | 3,01 | Nachmittag 12-17 |
| 89 | 26.10. 16:20 | 16:50 | 35 | 45,5 | 50,7 | 9,0 | 50,0 | 5 | 1,68 | 1min | 2,97 | Nachmittag 12-17 |
| 90 | 26.10. 18:35 | 19:10 | 40 | 48,4 | 52,7 | 6,6 | 57,0 | 4 | 1,62 | 1min | 2,47 | Abend 17-22 |
| 91 | 27.10. 07:00 | 08:00 | 65 | 45,2 | 52,5 | 5,4 | 50,0 | 10 | 3,61 | 1min | 2,77 | Morgen 04:30-07:30 |
| 92 | 27.10. 12:55 | 13:25 | 35 | 45,1 | 52,8 | 10,4 | 50,0 | 6 | 1,71 | 1min | 3,52 | Nachmittag 12-17 |
| 93 | 27.10. 17:05 | 18:00 | 60 | 46,4 | 52,3 | 9,8 | 57,0 | 9 | 3,13 | 1min | 2,87 | Abend 17-22 |
| 94 | 27.10. 19:15 | 20:15 | 65 | 47,3 | 52,8 | 9,6 | 52,0 | 11 | 3,56 | 1min | 3,09 | Abend 17-22 |
| 95 | 28.10. 09:00 | 09:50 | 55 | 45,3 | 52,7 | 8,8 | 50,0 | 9 | 2,59 | 1min | 3,48 | Vormittag 07:30-12 |
| 96 | 28.10. 13:55 | 14:20 | 30 | 47,2 | 52,8 | 11,4 | 52,0 | 4 | 1,35 | 1min | 2,97 | Nachmittag 12-17 |
| 97 | 28.10. 18:15 | 18:45 | 35 | 48,1 | 52,1 | 9,1 | 57,0 | 4 | 1,54 | 1min | 2,59 | Abend 17-22 |
| 98 | 28.10. 23:20 | 00:00 | 45 | 45,3 | 52,8 | 8,0 | 52,0 | 7 | 2,14 | 1min | 3,27 | Nacht 22-04:30 |
| 99 | 29.10. 06:45 | 07:35 | 55 | 47,5 | 52,5 | 6,0 | 57,0 | 7 | 2,71 | 1min | 2,59 | Morgen 04:30-07:30 |
| 100 | 29.10. 12:25 | 13:05 | 45 | 49,2 | 52,5 | 9,3 | 57,0 | 6 | 2,09 | 1min | 2,88 | Nachmittag 12-17 |
| 101 | 29.10. 18:10 | 18:55 | 50 | 47,7 | 52,5 | 7,7 | 57,0 | 8 | 2,45 | 1min | 3,26 | Abend 17-22 |
| 102 | 30.10. 02:20 | 02:45 | 30 | 45,1 | 50,4 | 5,0 | 50,0 | 4 | 1,61 | 1min | 2,49 | Nacht 22-04:30 |
| 103 | 30.10. 09:50 | 10:20 | 35 | 44,8 | 50,7 | 7,5 | 50,0 | 5 | 1,79 | 1min | 2,80 | Vormittag 07:30-12 |
| 104 | 30.10. 15:15 | 15:50 | 40 | 46,1 | 52,7 | 8,9 | 52,0 | 6 | 1,89 | 1min | 3,18 | Nachmittag 12-17 |
| 105 | 30.10. 19:25 | 19:50 | 30 | 47,9 | 52,7 | 6,8 | 57,0 | 3 | 1,41 | 1min | 2,12 | Abend 17-22 |
| 106 | 31.10. 08:50 | 09:25 | 40 | 45,2 | 50,6 | 6,1 | 50,0 | 6 | 2,19 | 1min | 2,74 | Vormittag 07:30-12 |
| 107 | 31.10. 11:40 | 13:05 | 90 | 44,9 | 52,0 | 9,3 | 52,0 | 17 | 5,10 | 1min | 3,33 | Vormittag 07:30-12 |
| 108 | 31.10. 17:10 | 17:40 | 35 | 47,3 | 52,7 | 8,5 | 52,0 | 4 | 1,64 | 1min | 2,45 | Abend 17-22 |
| 109 | 31.10. 19:55 | 21:10 | 80 | 48,0 | 52,1 | 6,8 | 57,0 | 12 | 4,13 | 1min | 2,91 | Abend 17-22 |
| 110 | 01.11. 05:55 | 06:35 | 45 | 47,1 | 52,4 | 3,7 | 57,0 | 6 | 2,32 | 1min | 2,59 | Morgen 04:30-07:30 |
| 111 | 01.11. 13:05 | 13:35 | 35 | 47,1 | 53,2 | 6,1 | 52,0 | 4 | 1,62 | 1min | - (01.11. ab 12:00) | Nachmittag 12-17 |

Ausgeschlossen: #57 (18.10. 10:35, Rücksprung Zähler 27489) und #111 (01.11. 13:05, Legionellen-/PV-Stab-Fenster). Damit n = 109. **[sicher]**

### 4.2 Gepoolt nach Tageszeit (ΣQ / ΣE_el)
Quelle: alle Ladungen aus 4.1, Volllogger 2026-10-01 bis 2026-11-01, E_el aus `ww_abnahme.csv`.

| Klasse | n | ΣQ kWh_th | ΣE_el kWh | AZ gepoolt | AT-Mittel °C | 1500 Start | 1500 Ende | Dauer min | Q je Ladung |
|---|---|---|---|---|---|---|---|---|---|
| Nacht 22–04:30 | 11 | 62 | 20,1 | **3,08** | 9,5 | 45,8 | 51,5 | 37 | 5,6 |
| Morgen 04:30–07:30 | 23 | 135 | 47,6 | **2,83** | 7,6 | 46,9 | 52,3 | 43 | 5,9 |
| Vormittag 07:30–12 | 18 | 134 | 42,2 | 3,18 | 10,1 | 46,3 | 52,0 | 46 | 7,4 |
| Nachmittag 12–17 | 31 | 182 | 55,2 | **3,30** | 13,3 | 48,5 | 54,4 | 39 | 5,9 |
| Abend 17–22 | 26 | 191 | 62,2 | 3,07 | 10,6 | 48,2 | 52,6 | 48 | 7,3 |
| **Alle** | **109** | **704** | **227,3** | **3,10** | 10,5 | 47,5 | 52,9 | 43 | 6,5 |

- Summen **[sicher]**. Morgen-Soll 1497 bei Ladebeginn: 19 × 52 °C, 2 × 50 °C, 2 × 57 °C (Smart Grid) **[sicher]**.
- Der Abstand Morgen–Nachmittag (0,47 AZ) passt fast genau zum AT-Unterschied 5,7 K × 0,081 = 0,46 **[wahrscheinlich]**. Die 57-°C-PV-Ladungen am Nachmittag (1500 Ende 54,4 im Mittel) drücken die Nachmittags-AZ nicht sichtbar.

### 4.3 Gepoolt nach AT, Start-1500 und Ladungsgröße
| AT-Klasse | n | ΣQ | ΣE_el | AZ | | Start-1500 | n | ΣQ | ΣE_el | AZ | | Q je Ladung | n | AZ | AT-Mittel |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| < 3 °C | 3 | 14 | 5,7 | 2,45 | | 42–45 °C | 3 | 26 | 8,3 | 3,13 | | < 3 kWh | 5 | 2,40 | 11,6 |
| 3–6 °C | 10 | 59 | 21,5 | 2,74 | | 45–48 °C | 73 | 483 | 158,4 | 3,05 | | 3–5 kWh | 21 | 2,78 | 10,6 |
| 6–9 °C | 22 | 141 | 48,9 | 2,88 | | 48–51 °C | 19 | 125 | 39,9 | 3,13 | | 5–7 kWh | 39 | 3,05 | 9,9 |
| 9–12 °C | 38 | 263 | 84,7 | 3,10 | | ≥ 51 °C | 14 | 70 | 20,8 | 3,37 | | 7–9 kWh | 23 | 3,17 | 10,5 |
| ≥ 12 °C | 36 | 227 | 66,5 | 3,41 | | | | | | | | ≥ 9 kWh | 21 | 3,25 | 11,4 |

- **AT:** klare Stufe von 2,45 (< 3 °C) bis 3,41 (≥ 12 °C). **[sicher]** als Befund, **[wahrscheinlich]** als Ursache.
- **Start-1500:** die scheinbar bessere AZ bei warmem Start ist durch die AT überlagert (≥ 51 °C: AT 14,8 °C). Bereinigt durch die Regression kehrt sich das Vorzeichen um. **[wahrscheinlich]**
- **Ladungsgröße:** bei fast gleicher AT (10,6 vs. 11,4 °C) steigt die AZ von 2,78 (3–5 kWh) auf 3,25 (≥ 9 kWh). Das ist der Fixanteil je Ladung. **[wahrscheinlich]**

### 4.4 Regression
Quelle: Ladungen aus 4.1, Skript-Ausgabe `cc_or_f68_20261102.py` (Lauf 02.11.2026).
- **AZ = 3,51 + 0,081·AT − 0,026·1500Start** (Standardfehler 0,57 / 0,007 / 0,013; gewichtet mit Q, n = 104, R² = 0,56). AT ist klar signifikant **[sicher]**; der Start-Effekt (−0,026 je K, etwa 2 σ) ist **[wahrscheinlich]** und physikalisch plausibel (höherer Kondensationsdruck).
- **E_el = 0,286·Q + 0,235** (n = 109): Grenz-AZ 3,49, elektrischer Fixanteil **0,24 kWh_el je Ladung**. Mit AT: E_el = 0,289·Q + 0,699 − 0,0453·AT. **[wahrscheinlich]**
- Das Modell trifft die Größenklassen: Q = 4 kWh → AZ 2,90 (gemessen 2,78), Q = 11 kWh → AZ 3,25 (gemessen 3,25).

### 4.5 Teure Ladungen (AZ < 2,8)
| | n | ΣQ | ΣE_el | AZ gepoolt | AT-Mittel | 1500 Start | 1500 Ende | Dauer min | Q je Ladung |
|---|---|---|---|---|---|---|---|---|---|
| AZ < 2,8 | 26 | 123 | 48,0 | **2,56** | 6,7 | 47,3 | 52,0 | 38 | 4,7 |
| AZ ≥ 2,8 | 83 | 581 | 179,3 | 3,24 | 11,7 | 47,5 | 53,1 | 45 | 7,0 |

- Verteilung der 26 nach Tageszeit: Morgen 10 (von 23 = 43 %), Abend 7, Nacht 3, Vormittag 3, Nachmittag 3 (von 31 = 10 %). **[sicher]**
- Teuer heißt hier: **kalt und klein**. Start-1500 unterscheidet sich nicht (47,3 vs. 47,5). **[wahrscheinlich]**
- Einzel-AZ sind wegen der 1-kWh-Auflösung von 27489 grob (bei Q = 4–5 kWh ±20–25 %). Einzelne Ladungen knapp unter 2,8 können Rundungsartefakte sein. **[sicher]**

### 4.6 Rechnung Zusammenlegen vs. Verschieben (kWh_el/Woche, Oktober-Niveau)
Basis (Monat × 7/32): **23,8 Ladungen/Woche, 154 kWh_th, 49,7 kWh_el** für WW. Ladungen je Tag: 2 × 1, 3 × 2, 10 × 3, 15 × 4, 1 × 5, 1 × 6. Pausen zwischen zwei Ladungen < 4 h: 33 im Monat (7,2/Woche), < 6 h: 60. **[sicher]**

**A) Verschieben der Morgenladung auf den Nachmittag**
- Morgenladungen: 5,0/Woche, 29,5 kWh_th, 10,4 kWh_el (AZ 2,83).
- Mit Nachmittags-AZ 3,30: 29,5 / 3,30 = 8,9 kWh_el → **Ersparnis ≈ 1,5 kWh_el/Woche**. Mit Regression (AT +5,7 K, Start-1500 +1,6 K): AZ 3,25 → 1,3 kWh_el/Woche. **[wahrscheinlich]**
- Das ist ein reiner AT-Gewinn. Im Winter kann der Tag-Nacht-Unterschied der AT kleiner oder größer sein. **[Vermutung]**

**B) Zusammenlegen (weniger, größere Ladungen)**
- Ersparnis je eingesparter Ladung: untere Grenze nur Q0 bei Grenz-AZ: 1,3…2,2 / 3,49 = **0,37…0,63 kWh_el**; obere Grenze Q0 plus elektrischer Fixanteil: 0,286 · Q0 + 0,235 = **0,61…0,86 kWh_el**. **[wahrscheinlich]**
- Szenario B1 „Pausen < 4 h entfallen“ (7,2 Ladungen/Woche weniger): brutto **2,7…6,2 kWh_el/Woche**.
- Szenario B2 „höchstens 2 Ladungen/Tag“ (23,8 → 14, also 9,8 weniger): brutto **3,6…8,4 kWh_el/Woche**.
- Gegenrechnung, je nachdem wie zusammengelegt wird:
  - **Später nachladen** (Speicher tiefer auskühlen lassen, eine größere Ladung von tieferem Start): kein Temperaturnachteil, eher Vorteil (−0,026 AZ je K Start ⇒ tieferer Start hilft leicht), Ruheverlust sinkt etwas. Netto ≈ brutto, also B1 **2,7…6,2**. **[Vermutung]**
  - **Vorladen** (höheres Soll, damit die nächste Ladung entfällt): Mehr-Ruheverlust grob +7–10 % von 3,3 kWh_th/Tag ⇒ 0,5…0,75 kWh_el/Woche, dazu höhere Kondensationstemperatur grob 6 % auf ~94 kWh_th/Woche ⇒ ~1,8 kWh_el/Woche. Netto B1 nur **≈ 0…4 kWh_el/Woche**. **[Vermutung]**

**Vergleich**
| Maßnahme | kWh_el/Woche | Anteil am WW-Strom (49,7) | Sicherheit |
|---|---|---|---|
| Verschieben Morgen → Nachmittag | 1,3…1,5 | 3 % | [wahrscheinlich] |
| Zusammenlegen B1, später nachladen | 2,7…6,2 | 5–12 % | [Vermutung] |
| Zusammenlegen B1, vorladen | 0…4 | 0–8 % | [Vermutung] |
| Verschieben + dabei mit Nachmittagsladung zusammenlegen | ≈ 3,4…5,8 (1,5 + 5 × 0,37…0,86) | 7–12 % | [Vermutung] |

- **Zusammenlegen bringt wahrscheinlich mehr als Verschieben**, solange es über späteres Nachladen geschieht, nicht über ein höheres Soll. **[wahrscheinlich]** für die Richtung, **[Vermutung]** für die Höhe.
- Beides schließt sich nicht aus: Fällt die Morgenladung weg und wird am Nachmittag in eine ohnehin fällige Ladung mitgenommen, addieren sich AT-Gewinn und ein eingesparter Fixanteil.
- **Vorschlag für der Betreiber:** Ob WW oben morgens tiefer als heute (Start-1500 morgens im Mittel 46,9 °C) für euch reicht, kannst nur du entscheiden. Wenn ja, wäre eine Testwoche mit weniger Ladungen die sauberste Messung; dieselbe Auswertung (Skript oben) zeigt dann vorher/nachher.

## 5. Stichprobe (Rohzeilen, Volllogger, Rohwerte ungeskaliert)
Spalten: 1500/27483/1477 ×10 °C, 1539 Betriebsart, 25611 ×100 kW, 27489 kWh, 25614 kWh, 1497 ×10 °C.

### 5.1 Ladung #11 – Morgen, 05.10.2026 06:05 (Datei `[lokaler Pfad]`)
| zeit | 1500 | 27483 | 1477 | 1539 | 25611 | 27489 | 25614 | 1497 |
|---|---|---|---|---|---|---|---|---|
| 2026-10-05 06:00:01 | 472 | 427 | 121 | 0 | 0 | 39547 | 30188 | 520 |
| 2026-10-05 06:05:01 | 465 | 425 | 121 | 4 | 456 | 39547 | 30188 | 520 |
| 2026-10-05 06:10:02 | 464 | 425 | 120 | 4 | 303 | 39548 | 30188 | 520 |
| 2026-10-05 06:15:01 | 476 | 430 | 120 | 4 | 261 | 39549 | 30188 | 520 |
| 2026-10-05 06:20:02 | 484 | 441 | 119 | 4 | 240 | 39549 | 30188 | 520 |
| 2026-10-05 06:25:02 | 493 | 451 | 119 | 4 | 245 | 39550 | 30189 | 520 |
| 2026-10-05 06:30:01 | 503 | 465 | 120 | 4 | 251 | 39551 | 30189 | 520 |
| 2026-10-05 06:35:01 | 511 | 475 | 120 | 4 | 255 | 39551 | 30189 | 520 |
| 2026-10-05 06:40:01 | 518 | 486 | 121 | 4 | 262 | 39552 | 30189 | 520 |
| 2026-10-05 06:45:01 | 527 | 497 | 121 | 0 | 0 | 39552 | 30189 | 520 |
| 2026-10-05 06:50:01 | 530 | 505 | 121 | 0 | 0 | 39552 | 30189 | 520 |

Q = 39552 − 39547 = **5 kWh**; Σ25611 = 2273 → 22,73 kW × 5 min = 1,89 kWh (5-min), 1-min-Integral `ww_abnahme.csv` **1,73 kWh** → **AZ 2,90**. 1500 Start 47,2 → Ende 53,0 °C, AT 12,0 °C, Soll 52 °C. **[sicher]**

### 5.2 Ladung #62 – Nachmittag (Smart Grid 57 °C), 19.10.2026 14:00 (Datei `[lokaler Pfad]`)
| zeit | 1500 | 27483 | 1477 | 1539 | 25611 | 27489 | 25614 | 1497 |
|---|---|---|---|---|---|---|---|---|
| 2026-10-19 13:55:02 | 500 | 479 | 140 | 0 | 0 | 39876 | 30340 | 500 |
| 2026-10-19 14:00:02 | 496 | 474 | 142 | 4 | 277 | 39877 | 30340 | 570 |
| 2026-10-19 14:05:01 | 491 | 471 | 143 | 4 | 278 | 39877 | 30341 | 570 |
| 2026-10-19 14:10:01 | 497 | 471 | 144 | 4 | 249 | 39878 | 30341 | 570 |
| 2026-10-19 14:15:01 | 507 | 477 | 145 | 4 | 253 | 39879 | 30341 | 570 |
| 2026-10-19 14:20:02 | 517 | 486 | 146 | 4 | 259 | 39879 | 30341 | 570 |
| 2026-10-19 14:25:02 | 524 | 497 | 147 | 4 | 265 | 39880 | 30341 | 570 |
| 2026-10-19 14:30:02 | 534 | 507 | 149 | 4 | 273 | 39881 | 30342 | 570 |
| 2026-10-19 14:35:01 | 541 | 517 | 150 | 4 | 279 | 39882 | 30342 | 570 |
| 2026-10-19 14:40:01 | 551 | 527 | 151 | 4 | 286 | 39882 | 30342 | 570 |
| 2026-10-19 14:45:02 | 559 | 537 | 152 | 0 | 0 | 39883 | 30342 | 500 |
| 2026-10-19 14:50:02 | 563 | 547 | 153 | 0 | 0 | 39883 | 30342 | 500 |

Q = 39883 − 39876 = **7 kWh**; Σ25611 = 2419 → 2,02 kWh (5-min), 1-min **2,03 kWh** → **AZ 3,45** bei AT 14,6 °C und Ende 56,3 °C. Trotz 4 K höherem Ende als #11 besser – AT 2,6 K höher, Ladung größer. **[sicher]** für die Werte, **[wahrscheinlich]** für die Deutung.

### 5.3 Ladung #57 – ausgeschlossen, 18.10.2026 10:35 (Datei `[lokaler Pfad]`, Auszug)
| zeit | 1500 | 27483 | 1477 | 1539 | 25611 | 27489 | 25614 | 1497 |
|---|---|---|---|---|---|---|---|---|
| 2026-10-18 10:30:01 | 452 | 485 | 113 | 0 | 0 | 39850 | 30330 | 500 |
| 2026-10-18 10:50:01 | 397 | 485 | 114 | 4 | 435 | 39854 | 30330 | 500 |
| 2026-10-18 11:10:01 | 452 | 485 | 116 | 4 | 323 | 39858 | 30332 | 500 |
| 2026-10-18 11:15:01 | 463 | 385 | 117 | 4 | 290 | 39850 | 30330 | 520 |
| 2026-10-18 11:45:01 | 513 | 478 | 122 | 4 | 259 | 39855 | 30331 | 520 |
| 2026-10-18 11:55:02 | 528 | 503 | 125 | 0 | 0 | 39855 | 30331 | 520 |


## 6. Offen
- **#111 (01.11. 13:05)** ist nur wegen des vorgegebenen Fensters „01.11. ab 12:00“ ausgeschlossen; P_el lief (E_el 1,62 kWh, Q 4 kWh, AZ ≈ 2,5). Mit ihr gesamt 708/228,9 = 3,09 statt 3,10 – ohne Einfluss auf das Ergebnis. **[sicher]**
- **Nur Oktober** (AT 2–20 °C). Winterwerte (Morgen-AT unter 0 °C, Abtauungen in der Ladung) fehlen; Rechnung 4.6 im Jänner wiederholen. **[sicher]**
- **Abtauung** während der Ladung ist nicht getrennt ausgewiesen; sie dürfte einen Teil des AZ-Abfalls bei kalter AT erklären. **[Vermutung]**
- **Q0** (1,3–2,2 kWh_th) ist aus der Vorgabe bzw. F1-Analyse übernommen, nicht neu bestimmt; die Daten liefern nur den elektrischen Fixanteil 0,24 kWh_el. Hydraulische Gegenprobe (31708 × (18725 − 1535)) nicht gerechnet.
- **Ruheverlust- und Temperaturaufschlag** beim Vorladen nur grob abgeschätzt. **[Vermutung]**
- **Komfort:** Wie weit WW oben morgens sinken darf, ist des Betreibers Entscheidung; davon hängt ab, wie viele Ladungen wirklich wegfallen können.