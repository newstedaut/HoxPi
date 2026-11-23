# Abtauenergie je Fenster, Vorbefund zu F108 und F112 (Orchestrator 05.11.2026 19:00)

Quelle: Pi `/home/<user>/hoxpi_fulllog/ww_hires.csv` ab 01.10., Fenster `WW_Soll_eff` = 100, Skript `[lokaler Pfad]`, nur gelesen. P_th ist in ganzen kW geloggt, dt höchstens 60 s. Die kWh sind P_th-Integrale, kein Zähler.

| Start | Dauer s | AT °C | WW davor | SLP an s | SLP aus s | P_th SLP an kWh | P_th SLP aus kWh | P_el kWh | Volumenstrom l/min (SLP an / aus) |
|---|---|---|---|---|---|---|---|---|---|
| 13.10. 07:09 | 300 | 2,2 | nein | 0 | 357 | 0 | 1,40 | 0,20 | - / - |
| 13.10. 08:37 | 299 | 2,3 | nein | 0 | 357 | 0 | 1,22 | 0,18 | - / - |
| 26.10. 05:04 | 299 | 4,6 | nein | 0 | 359 | 0 | 1,35 | 0,21 | - / 39 |
| 27.10. 06:40 | 479 | 5,2 | nein | 0 | 537 | 0 | 1,86 | 0,31 | - / 40 |
| 02.11. 02:21 | 359 | 3,6 | nein | 0 | 418 | 0 | 1,09 | 0,22 | - / 41 |
| 02.11. 04:45 | 358 | 2,9 | nein | 0 | 415 | 0 | 1,45 | 0,22 | - / 39 |
| 02.11. 06:24 | 371 | 3,1 | ja | 250 | 178 | 0,27 | 1,07 | 0,21 | 44 / 39 |
| 02.11. 13:24 | 220 | 5,9 | ja | 219 | 60 | 0,72 | 0,28 | 0,11 | 37 / 42 |
| 03.11. 08:00 | 360 | 4,2 | nein | 0 | 418 | 0 | 1,76 | 0,28 | - / 40 |
| 03.11. 10:46 | 360 | 4,9 | nein | 0 | 417 | 0 | 1,83 | 0,28 | - / 39 |
| 03.11. 13:48 | 341 | 5,6 | ja | 278 | 120 | 0,99 | 0,72 | 0,24 | 40 / 41 |
| 03.11. 22:45 | 378 | 4,5 | ja | 188 | 199 | 0,37 | 0,90 | 0,22 | 36 / 42 |
| 04.11. 07:10 | 380 | 3,4 | ja | 249 | 140 | 0,59 | 0,82 | 0,16 | 44 / 40 |
| 04.11. 21:12 | 339 | 4,5 | ja | 219 | 178 | 0,68 | 1,09 | 0,20 | 41 / 41 |
| 05.11. 07:54 | 480 | 3,5 | nein | 0 | 537 | 0 | 2,13 | 0,32 | - / 39 |
| 05.11. 10:15 | 419 | 4,2 | nein | 0 | 476 | 0 | 1,83 | 0,31 | - / 40 |

## Befund
- Eine Abtauung zieht rund 1,1-2,1 kWh Wärme aus dem Wasser (P_th-Integral), bei 0,11-0,32 kWh Strom [wahrscheinlich, P_th ist ein Rechenwert].
- Bei den 6 Abbrüchen entfallen 20-72 % davon auf die SLP-Phase [wahrscheinlich]. Der Rest läuft bei SLP aus.
- Der rechnerische Volumenstrom liegt in der Abtauung bei 36-44 l/min, in der WW-Ladung im Median bei 19,4 l/min [sicher als Rechnung]. Ob das stimmt oder an der Rechenbasis von P_th liegt, ist offen.
- Bei SLP aus läuft die HK1-Pumpe in den Status-23-Fenstern durch. In den Fenstern 03.11. 22:45 und 04.11. 21:12 (Status 0) steht sie, trotzdem fließen 0,90 und 1,09 kWh [sicher als Registerwerte]. Quelle dort wahrscheinlich der Puffer, nicht gemessen.

## Was bringt uns das
Ein Abbruch kostet den Speicher wenig, eine Logik lohnt nicht. Für den Zwilling und den ersten Frost zählt die Frage F112: Reicht die Quelle, wenn Heizkreis und Puffer kalt sind? der Betreiber muss nichts tun.