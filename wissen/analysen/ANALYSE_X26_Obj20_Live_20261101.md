# ANALYSE X26 Obj 0x20 live 01.11.2026 (Katalog F34) - natuerlicher Test 07-001 = 2,0 K
Stand 01.11.2026 ca. 18:00. Strikt nur lesend (Sniffer-Log, Volllogger). Nichts an Anlage/Bus geschrieben, auf dem Pi nichts angelegt.

## Frage
F34: Gilt live M0 = Heiz-VL-Soll b*0,5, M1 = WW-Soll b*0,5, M10 = Aussen (b-1)*0,5-40, M12 = Kuehl-Soll?
Vorstand (`[lokaler Pfad]`): M0 = floor0,5(1490 + 3 K), M1 = 1497 + 4,0 K nur bei WW-Anforderung, M10 = round(1477) auf 1 K, M12 immer 0, 1520 = M0-Echo.
Neu: Seit 31.10. 22:01 ist 07-001 = 2,0 K (vorher 3,0). Erwartung: M0 = floor0,5(1490 + 2,0) - ohne Aenderung von 1490 muss M0 um 1 K fallen.

## Datenquelle (Pi <LAN-IP>, nur gelesen)
- Sniffer: `/home/<user>/rs485_sniff/log/rs485_2026-11-01.log` (00:00-17:56, 4710 Master-Frames `82 10 20 17 20` per grep gefunden) und `/home/<user>/rs485_sniff/log/rs485_2026-10-31.log.gz` (21:40-22:30, 215 Frames).
- Volllogger: `/home/<user>/hoxpi_fulllog/2026-11-01.csv`, `/home/<user>/hoxpi_fulllog/2026-10-31.csv` (5 min, Rohwert x10; Spalten 1477 Aussen, 1490 HK1-Soll von Loxone, 1497/1499 WW-Soll, 1520 WP-VL-Soll = M0-Echo, 19870 UKA).
- Spaltenpositionen in der Kopfzeile 01.11.: 1477 = Spalte 2, 1490 = 15, 1497 = 22, 1499 = 24, 1520 = 45, 19870 = 294.

## Methode
- Der Auswerter `/tmp/or_x26soll_20261022_2300.py` (Decoder `rs485_blk20.stream`) braucht fuer 113 MB laenger als das 120-s-Limit von `hoxpi_ssh.py` -> abgebrochen.
- Ersatz: `grep -A3 '8210201720'` auf den Tageslog, die raw-Hexstuecke je Gruppe zusammengehaengt (Inline-`python3 -c`, nur stdin/stdout), Nutzdaten = 23 Byte nach dem Kopf; Ausgabe nur bei Aenderung von M0/M1/M10/M12.
- Einschraenkung: CRC nicht geprueft, Frames mit Kopf ueber eine raw-Zeilengrenze werden nicht gefunden, einzelne Zeilen mit eingestreuter `ZYK=`-Logzeile verworfen. Fuer die Werte unkritisch (jeder Zustand dutzendfach gleich gelesen) [sicher].
- Codec: M0/M1 = b*0,5; M10/M12 = (b-1)*0,5-40, 0x00 = keine Anforderung. Vergleich M0 gegen floor0,5(1490 + 2,0), M1 gegen 1497 + 4,0, M10 gegen round(1477).
- Zeitbasis: Sniffer ms-genau, Volllogger 5-min-Zeilen, Register bis 60 s alt. Bei laufenden Loxone-Rampen von 1490 gibt es daher Uebergangsabweichungen.

## Ergebnis-Tabelle
### A) Umschaltpunkt 07-001 3,0 -> 2,0 K (31.10.)
| Zeit X26 (31.10.) | M0 roh -> Wert | Volllogger 31.10. (1490 / 1520) | Erwartung | Urteil |
|---|---|---|---|---|
| 21:40:09.751 | 0x42 -> 33,0 | 21:40:01: 30,4 / 33,0 | floor(30,4 + 3) = 33,0 | passt (+3 K) [sicher] |
| 21:50:01.812 | 0x45 -> 34,5 | 21:50:01: 31,8 / 33,0; 21:55:02: 31,8 / 34,5 | floor(31,8 + 3) = 34,5 | passt (+3 K) [sicher] |
| **22:02:01.636** | **0x45 -> 0x43 = 33,5** | 22:00:02: 31,9 / 34,5; 22:05:01: 31,9 / **33,5** | floor(31,9 + 2) = 33,5 | **Sprung -1,0 K bei unveraendertem 1490 = Wirkung 07-001 = 2,0** [sicher] |
| 22:13:13.790 | 0x43 -> 33,5 | 22:15:01: 31,9 / 33,5 | 33,5 | passt (+2 K) [sicher] |
Der M0-Sprung liegt ca. 1 min nach der Parameteraenderung (22:01); das 1520-Echo folgt in der naechsten Volllogger-Zeile.

### B) 01.11.2026, Heizlaeufe und WW-Ladungen (M12 = 0x00 in allen Zeilen)
| Zeit X26 | Roh M0/M1/M10/M12 | M0 / M1 / M10 | Volllogger (Zeile: 1490 / 1497 / 1520 / 1477) | Erwartung | Urteil |
|---|---|---|---|---|---|
| 00:00:01.437 | 44/00/5d/00 | 34,0 / 0 / 6,0 | 00:00:01: 32,0 / 50,0 / 34,0 / 5,6 | M0 = 32,0+2 = 34,0; M10 = round(5,6) = 6 | passt [sicher] |
| 03:09:12.821 | 44/00/5b/00 | 34,0 / 0 / 5,0 | 03:15:01: 32,2 / 50,0 / 34,0 / 4,9 | floor(34,2) = 34,0; M10 5 | passt [sicher] |
| 05:33:20.367 | 45/00/59/00 | 34,5 / 0 / 4,0 | 05:30:01: 32,4 / 34,0 -> 05:35:02: 32,5 / 34,5 / 3,9 | floor(34,5) = 34,5 | passt (1490 springt 32,4->32,5 dazwischen) [sicher] |
| 05:50:48.186 | 7a/7a/59/00 | **61,0 / 61,0** / 4,0 | 05:55:02: 32,5 / **57,0** / 61,0 / 3,7 | M1 = 57+4 = 61; M0 = M1 | passt; WW-Ladung mit 57 C [sicher] |
| 06:00:56.330 | 70/70/59/00 | 56,0 / 56,0 / 4,0 | 06:15:02: 32,5 / 52,0 / 56,0 / 3,7 | M1 = 52+4 = 56 | passt [sicher] |
| 06:36:40.044 | 45/00/59/00 | 34,5 / 0 / 4,0 | 06:40:02: 32,6 / 52,0 / 34,5 / 3,5 | floor(34,6) = 34,5 | passt, WW-Ende -> M1 = 0 [sicher] |
| 07:08:56.034 | 41/00/57/00 | 32,5 / 0 / 3,0 | 07:10:02: 30,5 / 52,0 / 32,5 / 3,5 | floor(32,5) = 32,5 | passt [sicher] |
| 08:43:43.726 | 40/00/57/00 | 32,0 / 0 / 3,0 | 08:45:01: 30,4 / 50,0 / 32,0 / 3,4 | floor(32,4) = 32,0 | passt [sicher] |
| 12:20:47.043 | 3f/00/5d/00 | 31,5 / 0 / 6,0 | 12:20:02: 30,0 / 32,0; 12:25:02: 29,9 / 31,5 / 5,7 | floor(31,9) = 31,5 | passt (Flattern 3f/40 um 1490 = 30,0) [sicher] |
| **13:00:31.031** | 70/70/5d/00 | **56,0 / 56,0** / 6,0 | 13:05:01: 30,2 / **52,0** / 56,0 / 6,0 | M1 = 52+4 = 56; M0 = M1 | passt, WW-Ladung 13:00-13:37 [sicher] |
| 13:37:42.796 | 3f/00/5d/00 | 31,5 / 0 / 6,0 | 13:40:02: 29,9 / 52,0 / 31,5 / 6,1 | floor(31,9) = 31,5 | passt, Ladeende [sicher] |
| 17:05:50.221 | 3c/00/5b/00 | 30,0 / 0 / 5,0 | 17:15:02: 28,0 / 50,0 / 30,0 / 4,9 | 28,0+2 = 30,0 | passt [sicher] |
| 17:20:46.108 | 00/00/5b/00 | 0 / 0 / 5,0 | 17:20:02: 1490 = 0, 1520 noch 30,5; 17:25:01: 0 / 0 | 0 = keine Heizanforderung | passt [sicher] |
M10-Stufenwechsel 01.11. (Auswahl): 00:10-00:27 5<->6 bei AT 5,5; 04:06 5->4 (AT 4,5); 06:37 4<->3 (AT 3,5); 09:17 3->4; 10:29 4->5 (AT 4,6); 12:08 5<->6 (AT 5,5); 15:56 6->5 (AT 5,6/5,5). Alle bei AT ~x,5 [sicher].

Uebergangsphasen ohne sauberen Abgleich (5-min-Raster zu grob): 02:36-02:48 M0 31,0 -> 31,5 -> 32,0 -> 0 (Volllogger 02:40: 1490 29,5 / 1520 31,0; 02:45: 29,9 / 31,5; 02:50: 0 / 0) und 17:16-17:20 M0 30,5 -> 31,0 -> 0 (17:15: 28,0 / 30,0; 17:20: 0 / 30,5). 1520 laeuft dabei mit M0 mit, 1490 laeuft ueber eine Loxone-Rampe dazwischen. Keine Gegenaussage zur Formel [wahrscheinlich].

## Befund je Feld
| Feld | Live 01.11. | Urteil | Sicherheit |
|---|---|---|---|
| M0 | = floor auf 0,5 K von (1490 + 07-001); seit 31.10. 22:02 mit **+2,0 K** (10 von 10 Heizpunkten 01.11., Abw. 0 bis -0,4 durch Abrunden). Umschaltung 3 -> 2 K live gesehen: 22:02:01 Sprung 34,5 -> 33,5 bei unveraendertem 1490 = 31,9. Bei WW-Ladung waehrend Heizanforderung M0 = M1 (05:50, 06:00, 13:00). 0 = keine Heizanforderung. | Firmware-Skala bestaetigt, Inhalt = WP-VL-Soll inkl. Ueberhoehung 07-001 | **sicher** (Formel + Umschaltpunkt); M0 = M1 bei WW: sicher fuer 01.11. (3 Ladungen, jetzt 7 Faelle gesamt) |
| M1 | = 1497 + 4,0 K nur waehrend WW-Anforderung: 57 -> 61,0 (05:50), 52 -> 56,0 (06:00, 13:00); sonst 0 | bestaetigt (WW-Ladesoll = WW-Soll + 4 K) | **sicher** |
| M10 | = round(1477) in 1-K-Stufen, Wechsel bei x,5 | bestaetigt | **sicher** |
| M12 | 0x00 in allen 4710 Frames 01.11. und 215 Frames 31.10. abends | kein Kuehlbetrieb -> 0 = keine Kuehlanforderung; Kuehl-Soll weiter unbelegt | Vermutung (bis Kuehltag) |
| 1520 | folgt M0 auf 0,5 K (z. B. 31.10. 22:05 33,5; 01.11. 05:55 61,0) | M0-Echo | **sicher** |

WW-Sollwerte am 01.11. (Volllogger 1497): 50,0 bis 05:50, **57,0** um 05:55-06:00, 52,0 von 06:15 bis ca. 07:25, 50,0 bis 13:00, **52,0** von 13:00 bis 15:55, dann 50,0. Eine Legionellen-Ladung um ~15 Uhr (60 C) kam am 01.11. **nicht** vor: zwischen 13:37:42 und 17:56 steht M1 = 0 und 1497 nie > 52,0 [sicher, Datenstand]. Die 57-C-Ladung lief um 05:50 (Ursache SG/Legionellen/Loxone hier nicht geprueft) [Vermutung zur Ursache].

## Stichprobe (nachpruefbar)
Pi, lesend: `grep -m1 -A3 '^13:00:31.0' ~/rs485_sniff/log/rs485_2026-11-01.log`
```
13:00:31.031 raw[ 10] 06c08210201720707000
13:00:31.051 raw[ 11] 000000cd0064005d000000
13:00:31.072 raw[ 10] 000000800080ffff0082
```
-> Kopf `82 10 20 17 20`, M0 = 0x70 = 112 -> 56,0 C, M1 = 0x70 -> 56,0 C, M8 = 0x64, M10 = 0x5d = 93 -> (93-1)*0,5-40 = 6,0 C, M12 = 0x00.
Volllogger `/home/<user>/hoxpi_fulllog/2026-11-01.csv` Zeile 13:05:01: 1497 = 520 (52,0), 1520 = 560 (56,0), 1477 = 60 (6,0), 1490 = 302.
-> M1 = 52,0 + 4,0; M10 = 6.
Umschaltpunkt: `zcat ~/rs485_sniff/log/rs485_2026-10-31.log.gz | grep -A3 8210201720 | grep -m1 -A3 '^22:02:01'` -> M0 0x43 (33,5); Volllogger 31.10. 22:05:01: 1490 = 319, 1520 = 335.

## Offen
1. M12 an einem Kuehltag 2027 (einziger offener Rest von F34) -> `[lokaler Pfad]`.
2. Uebergangsrampen 02:36-02:48 / 17:16-17:20: nur mit 1490 in Sekundenaufloesung (Loxone-Statistik) sauber abzugleichen; fuer F34 nicht noetig.
3. Ursache der 57-C-WW-Ladung 05:50 (SG? Loxone-Kick?) gehoert nicht zu F34.
4. Optional: Volllauf von `/tmp/or_x26soll_20261022_2300.py` mit CRC-Pruefung auf dem Pi im Hintergrund (dauert > 120 s), falls exakte Frame-Zahlen gebraucht werden.

## Fazit F34
M0, M1, M10 live an je >= 6 Zeitpunkten belegt, M0 zusaetzlich am natuerlichen Test 07-001 3 -> 2 K. F34 ist **erledigt bis auf M12** (Kuehl-Soll erst im Kuehlbetrieb pruefbar).