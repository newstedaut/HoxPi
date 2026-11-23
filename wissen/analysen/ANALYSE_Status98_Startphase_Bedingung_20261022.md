# Analyse OR-21.10.b: Welche Bedingung loest WEZ-Status 98 (W:61, Fehlerreg. 124) nach Kuehlen aus? - 22.10.2026 22:00
Quelle: `~/hoxpi_fulllog/2026-07-30 ... 2026-09-14.csv(.gz)` (13 224 Proben, 5-min-Raster), Gegenprobe 1-min `~/hoxpi_fulllog/kuehltest.csv` (ab 07.09.). Nur gelesen. Skripte `Emulation\or_s98_20261022_2200*.py` (a = Wechsel finden, b = Merkmale + Schwellen-Scan ueber alle 514 Spalten, c = Zeitreihen, d = Kuehllauf, e = Tabelle, f = Wert vor Start).
Wechsel = Ende eines `1539` = 2 (Kuehlen) bis zum naechsten `1539` = 1/4 ohne Kuehlen dazwischen: **65** (wie Slot 10). Merkmalszeitpunkt = erste Probe mit `1539` = 51/98, sonst letzte Probe vor dem Start.

## Kernergebnis
**Trennmerkmal = Ruecklauf `1535` bei der Start-Anforderung.** Kein anderes der 514 Register trennt besser (Scan, Teil b).

| `1535` bei Anforderung | Wechsel | davon mit 98 |
|---|---|---|
| <= 16,5 °C | 3 (24.08., 03.09., 12.09.) | **3 (100 %)** |
| = 17,0 °C | 3 (07.09. 08:40, 10.09. 16:35, 11.09. 10:50) | 1 |
| >= 17,5 °C | 59 | **0** |

- Regel "98, wenn `1535` < 17,0 °C": **64/65 richtig (98,5 %)**, einziger Grenzfall 07.09. (Raster 0,5 K).
- 07.09. im 1-min-Log: Ruecklauf 16,5 °C bis 08:33, 17,0 ab 08:34, 98 ab 08:40 im Volllogger; WEZ-Lane hat bis 60 s Nachlauf -> Anforderung fiel wahrscheinlich noch bei 16,5/17,0. 10.09./11.09. stand RL >= 10 min stabil auf 17,0 -> Start ohne 98.
- Freigabe: 07.09. Verdichterstart 08:56 bei RL 19,5 (08:53 19,0) - passt zur dokumentierten Freigabe RL >= 19,0 °C (HV022 18,0 + HV014 1,0).
- **Wahrscheinlich: Hysterese 17,0 / 19,0 = HV022 18,0 -/+ HV014 1,0.** Sperre bei RL < 17,0, Freigabe bei RL >= 19,0. Waehrend 98 laeuft die Pumpe, VL/RL steigen ohne Verdichter (P_el 0) in 5-15 min auf ~19.
- Vorlauf `18760` trennt NICHT: 8 Starts ohne 98 hatten VL 17,0 vor dem Start (z. B. 04.08. 07:55, 06.08. 07:55, 10.09. 16:35), die 98-Faelle 15,0-17,0.

## Warum war RL in den 4 Faellen so kalt?
- **Belegt:** Nach jedem Kuehlende faellt `1535` auf 17,0-17,5 (Normalfall) bzw. 16,5 / 15,0 (98-Faelle). Alle 4 mit kurzer Pause 20-70 min, d. h. das Wasser hatte sich noch nicht erholt. Nach langen Pausen (> 2 h) war RL trotz 16,5-Minimum beim Start wieder >= 17,5 (z. B. 12.08., 14.08., 31.08. 07:05, 11.09.).
- **Belegt:** Kuehl-Soll `1524` am Kuehlende: Ende Juli/Anfang Aug. 16,5-17,0 °C, ab 29.08. meist 15,0 °C. 3 der 4 Faelle (03.09., 07.09., 12.09.) liegen im 15,0-Zeitraum, 24.08. bei 18,0 aber AT 12,7-14 °C morgens.
- **Belegt:** 03.09. war der kaelteste Kuehllauf (VL-Min 12,0, RL-Min 14,5) -> tiefster RL beim Start (15,0).
- **Wahrscheinlich:** tiefer Kuehl-Soll (15,0) + kuehle Aussenluft/Morgen + kurze Pause bis WW-/Heizanforderung = RL < 17 bei Start. Das ist eine Kombination, kein einzelner Schalter; der Regler prueft nur den RL.
- **Nicht trennend (Scan):** Aussentemperatur, WW-Ist/-Soll, SF2, Pausendauer, Tageszeit, Ziel Heizen/WW, Status 16/51 davor (16 auch bei 8 Wechseln ohne 98, 51 bei 9 ohne 98), Raumtemp (nur Tendenz: 98-Faelle Raum 20,6-21,1 = staerker abgekuehlt).
- **Nicht ermittelbar (nicht geloggt):** Ansaug-/Verdampfer-/Heissgastemperatur (`27491` "Quelle VL" folgt etwa der Aussenluft und trennt nicht, `27492` ohne Wert), echte Kuehllauf-Dauer (1539 = 2 steht im 5-min-Raster nur 1-2 Proben, Wert "5-10 min" ist Rasterartefakt).

## Tabelle aller 65 Wechsel
Spalten: Kuehlende = letzte Probe 1539 = 2; Anf. = Merkmalszeitpunkt; Zw. = Status dazwischen (0 weggelassen); AT `1477`, VL `18760`, RL `1535` (VL/RL bei der ersten 51/98-Probe, sonst letzte Probe vor dem Verdichterstart); RLmin = Minimum RL zwischen Kuehlende und Anf.; WW `1500`/`1499`; SF2 `27483`; Raum `1510` und KSoll `1524` am Kuehlende. Alle °C.

|Nr|Kuehlende|Anf./Start|Pause min|Ziel|Zw.|98|AT|VL vor Start|**RL vor Start**|RLmin|WW Ist/Soll|SF2|Raum|KSoll|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|1|07-31 05:40|07:55|135|WW|0|-|22,1|18,0|**17,5**|17,0|42,1/50,0|36,6|20,9|16,5|
|2|07-31 11:50|12:25|35|WW|0|-|28,2|18,0|**18,0**|17,5|45,1/50,0|44,1|21,9|16,5|
|3|07-31 22:05|23:40|95|WW|0|-|20,0|18,0|**18,5**|17,0|42,8/48,0|28,6|21,7|17,0|
|4|08-01 10:10|11:05|55|WW|0|-|20,1|19,0|**19,0**|17,5|40,1/45,0|39,0|21,2|16,5|
|5|08-01 14:25|14:45|20|WW|16|-|27,1|32,0|**19,5**|18,0|44,5/50,0|42,9|22,0|-|
|6|08-01 21:20|21:40|20|WW|16|-|17,9|18,0|**18,0**|17,5|45,2/50,0|42,8|21,5|17,0|
|7|08-01 22:20|10:15|715|WW|0|-|20,2|25,0|**24,0**|17,5|39,7/45,0|35,2|21,4|16,5|
|8|08-03 03:45|05:50|125|WW|51|-|17,1|20,0|**19,0**|17,0|40,1/45,0|33,4|21,2|16,5|
|9|08-03 12:55|14:25|90|WW|0|-|28,4|19,0|**19,0**|17,5|44,7/50,0|22,3|22,2|17,0|
|10|08-03 22:50|23:25|35|WW|0|-|21,4|18,0|**18,0**|17,5|42,9/48,0|32,2|22,2|17,0|
|11|08-04 07:10|07:55|45|WW|51|-|22,1|17,0|**17,5**|17,0|41,7/50,0|31,3|21,4|16,5|
|12|08-04 11:35|11:55|20|WW|16|-|26,8|18,0|**18,0**|17,5|44,8/50,0|44,0|21,7|16,5|
|13|08-05 04:25|06:20|115|WW|0|-|18,8|19,0|**19,0**|17,0|40,0/45,0|36,2|21,5|16,5|
|14|08-05 07:00|07:55|55|WW|51|-|23,4|19,0|**19,0**|18,0|44,7/50,0|42,0|21,6|16,5|
|15|08-05 11:10|11:50|40|WW|0|-|27,4|18,0|**18,0**|17,5|44,9/50,0|43,2|22,2|17,0|
|16|08-05 15:15|15:35|20|WW|16|-|30,8|42,0|**19,0**|17,5|44,8/50,0|44,0|23,0|17,0|
|17|08-05 19:05|19:55|50|WW|0|-|20,9|17,0|**17,5**|17,0|45,1/50,0|34,0|23,2|18,0|
|18|08-06 07:20|07:55|35|WW|51|-|19,9|17,0|**17,5**|17,0|40,9/50,0|38,4|21,6|17,0|
|19|08-06 11:30|12:45|75|WW|0|-|26,3|19,0|**19,0**|17,5|44,9/50,0|43,7|22,0|17,0|
|20|08-06 18:00|19:45|105|WW|0|-|20,0|18,0|**18,5**|17,0|44,9/50,0|43,1|22,3|17,0|
|21|08-07 03:30|07:15|225|WW|0|-|17,6|21,0|**20,0**|17,0|40,0/45,0|38,2|21,5|16,5|
|22|08-07 13:30|14:40|70|WW|0|-|26,4|19,0|**19,0**|17,5|44,9/50,0|44,5|22,1|17,0|
|23|08-07 18:05|18:25|20|WW|51|-|22,8|17,0|**17,5**|17,0|45,2/50,0|44,5|22,4|17,0|
|24|08-08 00:00|00:30|30|WW|0|-|18,1|17,0|**17,5**|17,0|42,7/48,0|27,8|22,0|17,0|
|25|08-08 01:20|10:45|565|WW|0|-|20,5|25,0|**23,5**|17,5|40,1/45,0|34,8|21,7|16,5|
|26|08-08 19:10|20:05|55|WW|0|-|24,9|18,0|**18,0**|17,5|44,8/50,0|43,9|22,7|17,0|
|27|08-09 00:05|08:35|510|WW|0|-|20,5|23,0|**21,5**|17,0|40,3/45,0|39,0|22,2|16,5|
|28|08-09 20:25|21:55|90|WW|0|-|22,2|19,0|**19,0**|17,5|45,2/50,0|37,4|22,0|18,0|
|29|08-10 02:05|07:20|315|WW|0|-|18,3|23,0|**21,5**|17,0|40,0/45,0|35,6|21,7|17,0|
|30|08-10 12:20|12:40|20|WW|16|-|25,8|20,0|**18,5**|17,5|44,8/50,0|43,9|22,4|17,0|
|31|08-10 15:10|16:20|70|WW|51|-|28,9|19,0|**19,0**|17,5|45,1/50,0|44,5|22,8|17,0|
|32|08-10 23:30|00:25|55|WW|0|-|19,1|18,0|**18,0**|17,0|43,2/48,0|40,9|22,4|17,0|
|33|08-11 03:55|08:00|245|WW|0|-|18,4|19,0|**19,0**|17,0|41,7/50,0|35,5|21,8|16,5|
|34|08-11 14:45|15:10|25|WW|0|-|27,9|18,0|**18,5**|17,5|45,2/50,0|44,4|22,2|16,5|
|35|08-11 22:45|23:40|55|WW|0|-|20,2|18,0|**18,5**|17,5|44,4/50,0|41,9|22,6|16,5|
|36|08-12 03:10|08:00|290|WW|0|-|19,9|19,0|**18,5**|16,5|42,1/50,0|41,1|21,8|16,5|
|37|08-12 10:20|10:40|20|WW|16|-|23,6|18,0|**18,0**|17,5|44,8/50,0|40,4|21,9|16,5|
|38|08-12 19:40|20:25|45|WW|51|-|24,2|18,0|**18,5**|17,5|44,9/50,0|43,6|22,9|18,0|
|39|08-13 05:30|07:30|120|WW|0|-|16,0|19,0|**18,0**|16,5|39,6/45,0|29,3|21,7|16,5|
|40|08-13 22:15|23:05|50|WW|0|-|19,1|18,0|**18,5**|17,5|44,9/50,0|42,1|22,1|16,5|
|41|08-14 01:40|08:00|380|WW|0|-|18,9|22,0|**20,5**|16,5|41,3/50,0|39,0|21,6|16,5|
|42|08-15 02:40|09:00|380|WW|51|-|20,2|22,0|**20,5**|16,5|44,7/50,0|42,7|21,8|16,5|
|43|08-15 17:40|18:00|20|WW|0|-|29,3|18,0|**18,0**|17,0|44,7/50,0|19,9|23,2|18,0|
|44|08-16 03:30|09:35|365|WW|0|-|20,5|23,0|**21,5**|17,0|40,0/45,0|36,4|21,8|16,5|
|45|08-16 18:25|18:45|20|WW|16|-|25,6|18,0|**18,0**|17,5|44,5/50,0|35,2|22,9|18,0|
|46|08-17 02:20|07:50|330|WW|0|-|17,0|22,0|**20,5**|17,0|40,1/45,0|36,8|21,9|16,5|
|**47**|**08-24 07:30**|**07:50**|20|WW|16/98|**JA**|14,1|16,0|**16,5**|16,5|40,4/45,0|38,3|20,7|18,0|
|48|08-28 17:20|21:05|225|Heiz|0|-|20,9|25,0|**23,5**|23,5|51,8/50,0|39,1|22,0|16,0|
|49|08-29 12:35|12:55|20|WW|16|-|21,2|19,0|**19,0**|19,0|44,8/50,0|22,3|22,1|16,0|
|50|08-29 22:50|00:15|85|Heiz|51|-|16,9|18,0|**18,5**|17,5|49,2/45,0|27,5|21,8|15,0|
|51|08-30 18:55|20:25|90|WW|0|-|21,9|19,0|**19,0**|17,5|42,9/50,0|19,3|22,4|16,0|
|52|08-31 07:05|12:40|335|WW|0|-|21,5|18,0|**17,5**|16,5|45,1/50,0|27,0|21,2|18,0|
|53|08-31 17:15|19:20|125|WW|0|-|18,9|17,0|**17,5**|17,0|45,1/50,0|18,4|22,0|17,0|
|54|09-01 17:40|18:15|35|WW|0|-|22,1|18,0|**18,5**|17,5|45,1/50,0|26,0|21,1|15,0|
|55|09-02 15:35|16:45|70|WW|0|-|23,5|19,0|**19,0**|17,5|45,2/50,0|23,2|20,9|15,0|
|**56**|**09-03 12:10**|**12:30**|20|WW|16/98|**JA**|22,2|15,0|**15,0**|14,5|44,1/50,0|23,0|20,8|15,0|
|57|09-06 11:45|12:15|30|WW|0|-|20,7|18,0|**18,0**|17,5|43,5/50,0|25,2|21,1|15,0|
|**58**|**09-07 07:30**|**08:40**|70|WW|98|**JA**|15,0|17,0|**17,0**|16,5|45,2/50,0|18,8|21,1|15,0|
|59|09-07 15:10|15:50|40|WW|0|-|25,8|19,0|**19,0**|17,5|49,1/54,0|34,7|22,6|15,0|
|60|09-08 10:50|11:15|25|WW|0|-|20,0|18,0|**18,0**|17,5|44,8/50,0|25,9|21,0|15,0|
|61|09-09 13:10|14:55|105|WW|0|-|19,4|19,0|**19,0**|17,5|45,1/50,0|20,6|20,9|15,0|
|62|09-10 15:25|16:40|75|WW|0|-|15,7|17,0|**17,0**|17,0|44,8/50,0|28,8|24,0|15,5|
|63|09-10 17:35|20:30|175|WW|0|-|14,0|18,0|**18,0**|17,0|37,5/50,0|19,6|24,0|15,0|
|64|09-11 09:20|10:55|95|WW|0|-|12,9|17,0|**17,0**|16,5|44,8/50,0|23,3|21,4|15,0|
|**65**|**09-12 01:25**|**01:45**|20|Heiz|16/51/98|**JA**|9,7|16,0|**16,5**|16,5|46,9/45,0|30,1|20,6|15,0|

Hinweis Tabelle: AT bei fehlender 51/98-Probe am Start-Sample (Aussenfuehler sieht beim Luefteranlauf Abwaerme, vgl. Takt-Analyse) - fuer die Trennung unerheblich.

## Vorhersage (Verhaltenskarte-Format, Vorschlag V105)
- [ ] **V105 (Nr 14, notiert 22.10.2026 22:00, VOR dem naechsten Kuehlsommer):** Wenn eine Start-Anforderung (Heizen, WW oder nach Abtauung) kommt, waehrend `1535` (Ruecklauf) **<= 16,5 °C** steht, dann geht `1539` auf **98** und `1534` auf **124** (W:61); Pumpe laeuft, Verdichter bleibt aus, bis `1535` >= ~19,0 °C (5-15 min), danach Start. Bei `1535` >= 17,5 °C kommt **nie** 98. 17,0 °C = Grenzfall. Widerlegt, wenn 98 bei `1535` >= 17,5 oder ein Start ohne 98 bei `1535` <= 16,5 (1-min-Raster, Probe vor Start) auftritt. Pruefung: passiv, Volllogger + `ww_hires`/`kuehltest`, naechster Kuehlbetrieb mit Kuehl-Soll 15 °C; im Winter auch nach Abtauungen (8 W:61 im ERR.LOG Dez-Maerz).
- Ableitung (wahrscheinlich): Risiko hoch bei Kuehl-Soll **15,0** und/oder kuehlem Morgen (AT < 15) **und** Start-Anforderung < 1 h nach Kuehlende. Belegt: Nr 1-46 (30.07.-17.08., Kuehl-Soll 16,5-18,0, AT meist > 16) 0 von 46; Nr 47-65 (ab 24.08.) 4 von 19. 24.08. hatte Soll 18,0, aber AT 12,7 -> Kuehl-Soll allein ist nicht die Ursache.
- Vermutung: "auch nach Abtauung" in V105 ist aus den 8 Winter-W:61 (ERR.LOG) abgeleitet, im Volllogger nicht geprueft.

## Einordnung
- **Belegt:** Trennmerkmal RL `1535` bei Anforderung; <= 16,5 -> 3/3 mit 98, >= 17,5 -> 0/59; 17,0 Grenzfall 1/3. 98 endet, wenn RL ~19 erreicht (07.09. 1-min).
- **Wahrscheinlich:** Sperre RL < 17,0 / Freigabe RL >= 19,0 (HV022 18,0 -/+ HV014 1,0); die 98-Phase ist ein Schutz gegen Start mit zu kaltem Wasserkreis (Verfluessiger/Kondensation), kein Defekt. 124 im Fehlerreg. = Abbild W:61.
- **Vermutung:** Ob VL (>= 18,0) zusaetzlich in die Freigabe eingeht, ist aus 5-min-Daten nicht zu trennen (VL und RL steigen gemeinsam). Ob die Sperrschwelle exakt 17,0 ist oder 16,8/16,9 (Fuehler fein, Modbus 0,5 K) - nicht aufloesbar.
- **Nicht ermittelbar:** Verdampfer-/Ansaug-/Heissgastemperatur zum Startzeitpunkt (nicht im Volllogger); Firmware-Stelle (V1.18 nicht vorhanden).

## Was bringt uns das
- OR-21.10.b ist geklaert: Nicht der Abstand zum Kuehllauf, sondern **der Ruecklauf unter 17 °C bei Start-Anforderung** loest 98/W:61/124 aus. Kein Fehlerfall, nur 5-15 min Verzoegerung der WW-Ladung.
- Stellschraube fuer naechsten Sommer: Kuehl-Soll nicht unter ~16,5 °C (30.07.-17.08. mit 16,5-18,0 und warmen Naechten: 0 von 46; das ist eine Tendenz, kein Beweis) oder WW-Ladung nicht direkt (< 1 h) auf einen Kuehllauf am kuehlen Morgen legen. Nebeneffekt: 16,5 statt 15,0 reduziert auch Kondensationsgefahr am Fussboden.
- Loxone/Dashboard kann 98 jetzt erklaeren: "Startphase: Wasserkreis zu kalt (RL < 17 °C), wartet bis RL 19 °C".
- Winter: gehaeufte 124 nach Abtauung = RL nach Abtauung < 17 -> Hinweis auf Puffer/Abtauenergie (Nr 7), mit derselben Regel pruefbar.

## Pruefpunkte fuer den Pruefer (Rohdaten Volllogger)
1. `~/hoxpi_fulllog/2026-09-03.csv.gz`, Zeile 2026-09-03 12:30: `1539` = 98, `1534` = 124, `1535` = 150 (15,0 °C); 12:45 `1539` = 4 bei `1535` = 310.
2. `~/hoxpi_fulllog/2026-09-10.csv.gz`, Zeile 2026-09-10 16:35: `1539` = 0, `1535` = 170 (17,0 °C, Grenzfall ohne 98); 16:40 `1539` = 4. Gegenfall: 2026-08-04 07:55 `1539` = 51, `1535` = 175 -> 08:00 `1539` = 4 ohne 98.
3. 1-min `~/hoxpi_fulllog/kuehltest.csv` 2026-09-07 08:33/08:34: Ruecklauf 165 -> 170; Modulation 42 erst 08:56 bei Ruecklauf 195.