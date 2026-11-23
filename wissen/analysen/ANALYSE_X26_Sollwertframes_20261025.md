# ANALYSE X26 Sollwertframes Obj 0x20 (TopTronic -> Kaelteregler) - Katalog F34, 25.10.2026
Stand 25.10.2026 ca. 09:10 - strikt nur lesend (Sniffer-Logs, Volllogger). Nichts an Anlage/Bus geschrieben.

## Frage
Gilt die Firmware-These aus `[lokaler Pfad]` live?
M0 = Heiz-VL-Soll b*0,5 / M1 = WW-Soll b*0,5 / M10 = Aussen (b-1)*0,5-40 / M12 = Kuehl-Soll.

## Vorbefund (schon erledigt, nicht doppelt gemacht)
`[lokaler Pfad]` (22.10., 10009 Frames):
M1 = dp5051 + 4 K (nur bei Soll 52/57 belegt), M0 sicher Heiz-VL-Soll, M10 sicher (1-K-Stufen), M12 nicht pruefbar, M11 Bit6 = SG.
Dieser Lauf schliesst die Luecken: (a) M1 bei Soll 50, (b) M0 quantitativ gegen 1490 + 3 K (07-001), (c) M0 waehrend WW-Ladung ohne SG, (d) M10 gegen Reg 1477 (0,1 K), (e) WW 45/50-Wechsel, (f) M12.

## Quellen (Pi <LAN-IP>, nur gelesen)
- Sniffer: `/home/<user>/rs485_sniff/log/rs485_2026-10-24.log.gz` (9731 Frames `10 20 17 20`, alle CRC ok, alle len 23) und `/home/<user>/rs485_sniff/log/rs485_2026-10-25.log` (00:00-09:01, 4373 Frames, alle CRC ok).
- Decoder: `/home/<user>/rs485_sniff/rs485_blk20.py` (`stream`), Auswerter `/tmp/or_x26soll_20261022_2300.py` (Kopie: `[lokaler Pfad]`), gz per `zcat | ... /dev/stdin`.
- Ausgaben: `/tmp/or_x26soll_24.out`, `/tmp/or_x26soll_25.out`.
- Volllogger: `/home/<user>/hoxpi_fulllog/2026-10-24.csv`, `/home/<user>/hoxpi_fulllog/2026-10-25.csv` (5 min, x10). Spalten: 1477 Aussentemp (laut `[lokaler Pfad]`), 1490 HK1-Soll (Loxone), 1497/1499 WW-Soll, 1520 WP-Soll (Echo), 1529.
- Richtung: Kopf `82 10 20 17 20` = Master (TopTronic) -> Slave 0x10 (Kaelteregler), op 0x20 = Schreiben, len 0x17 = 23, obj 0x20. Antworten des Kaeltereglers beginnen `40 20 ..` (Statusblock 100 B, nicht Gegenstand).
- Codec: M0/M1 = b*0,5; M10/M12 = (b-1)*0,5-40, 0 bzw. 0xFF = keine Anforderung.

## Tabelle (Zeit X26 = Ortszeit; Volllogger-Zeile = naechste 5-min-Zeile, 1490/1520 bis 60 s alt)
| Zeit X26 | Roh M0/M1/M10/M12 (hex) | dekodiert M0 / M1 / M10 / M12 | Volllogger (1490 / 1497 / 1520 / 1477) | Vergleich | Abweichung |
|---|---|---|---|---|---|
| 24.10. 05:26:44 | 44/00/5b/00 | 34,0 / 0 / 5,0 / - | 05:30: 31,3 / 50,0 / 34,0 / 5,4 | M0 vs 1490+3 = 34,3 | -0,3 (abgerundet auf 0,5) |
| 24.10. 05:28:28 | 6c/6c/5b/00 | 54,0 / 54,0 / 5,0 / - | 05:30: 31,3 / **50,0** / 54,0 / 5,4 | M1 vs 1497 | **+4,0 K**; M0 = M1 |
| 24.10. 10:34:43 | 43/00/5d/00 | 33,5 / 0 / 6,0 / - | 10:35: 30,8 / 50,0 / 33,5 / 5,8 | 1490+3 = 33,8 | -0,3; M10 vs AT +0,2 |
| 24.10. 10:48:43 | 6c/6c/5d/00 | 54,0 / 54,0 / 6,0 / - | 10:50: 30,9 / 50,0 / 54,0 / 5,9 | M1 vs 1497 | +4,0 K |
| 24.10. 14:24:58 | 70/70/61/00 | 56,0 / 56,0 / 8,0 / - | 14:25: 30,0 / **52,0** (Kick) / 56,0 / 7,8 | M1 vs 1497 | **+4,0 K**; M10 +0,2 |
| 24.10. 14:41:30 | 00/70/61/00 | 0 / 56,0 / 8,0 / - | 14:45: 0 / 52,0 / 0 / 7,7 | Heizanf. Ende (1490 -> 0) | M0 -> 0, M1 bleibt |
| 24.10. 15:06:34 | 42/00/61/00 | 33,0 / 0 / 8,0 / - | 15:10: 30,0 / 52,0 / 33,0 / 7,9 | 1490+3 = 33,0 | 0,0 |
| 24.10. 15:18:58 | 41/00/61/00 | 32,5 / 0 / 8,0 / - | 15:20: 29,9 / 52,0 / 32,5 / 8,0 | 1490+3 = 32,9 | -0,4 |
| 24.10. 21:46:17 | 00/00/59/00 | 0 / 0 / 4,0 / - | 21:30 / 22:00: AT 4,8 / 4,2 | Stufe 5 -> 4 bei AT ~4,5 | Rundung |
| 24.10. 23:04:24 | 00/00/57<->59/00 | 0 / 0 / 3,0<->4,0 / - | 23:00 / 23:30: AT 3,6 / 3,4 | Flattern um 3,5 | Rundung |
| 25.10. 01:09:36 | 00/6c/57/00 | 0 / 54,0 / 3,0 / - | 1490 = 0, 1497 = 50,0, 1520 = 0 | M1 vs 1497 | +4,0 K; M0 = 0 (keine Heizanf.) |
| 25.10. 03:55:19 | 47/00/57/00 | 35,5 / 0 / 3,0 / - | 04:00: 32,7 / 50,0 / 35,5 / 3,0 | 1490+3 = 35,7 | -0,2; M10 0,0 |
| 25.10. 07:20:31 | 43/00/57/00 | 33,5 / 0 / 3,0 / - | 07:20: 30,8 / 50,0 / 33,5 / 3,3 | 1490+3 = 33,8 | -0,3 |
M12 = 0x00 in allen 9731 + 4373 Frames (24./25.10.), M12 nie gesetzt.
Weitere M10-Stufen 24.10. (alle bei AT = x,5): 01:57 7->6 (AT 6,5), 03:41 6<->5 (5,5-5,7), 12:15 6->7 (6,5-6,7), 13:52 7<->8 (7,5).

## Befund je Feld
| Feld | These (FW) | Live-Messung | Urteil | Sicherheit |
|---|---|---|---|---|
| M0 | Heiz-VL-Soll b*0,5 | Skala b*0,5 stimmt. Wert = **HK1-Soll 1490 + 3 K (07-001), auf 0,5 K abgerundet** (10 von 10 Heizpunkten, Abw. 0 bis -0,4). Waehrend WW-Ladung **und** laufender Heizanforderung: M0 = M1 (Ladesoll, 05:28, 10:48, 14:24 / 15:00). Ohne Heizanforderung M0 = 0, auch bei WW-Ladung (25.10. 01:09, 24.10. 14:41). | **anders**: M0 = WP-VL-Soll Heizen = floor2((1490 + 3,0)) bzw. max(..., M1) bei paralleler WW-Ladung; 0 = keine Heizanforderung | Formel 1490+3 abgerundet: **sicher**; Regel M0 = M1 bei WW: **wahrscheinlich** (4 Faelle, Mechanismus nicht aus FW belegt) |
| M1 | WW-Soll b*0,5 | Wert = **1497 + 4,0 K**, nur waehrend WW-Anforderung, sonst 0. Jetzt auch bei Soll 50 (-> 54,0, 3 Ladungen) und 52 (-> 56,0) belegt, vorher 52/57. Konstant 4,0 K, nicht 3,5. | **anders**: M1 = WW-Ladesoll = WW-Soll + 4,0 K | **sicher** (Soll 50/52/57, 8 Ladungen, 22./24./25.10.) |
| M10 | Aussen (b-1)*0,5-40 | Codec stimmt, b immer ungerade -> nur ganze Grad; Stufenwechsel exakt bei Reg 1477 = x,5 (8 Wechsel), Flattern wenn AT auf x,5 steht. | **bestaetigt**, = round(AT 1477) auf 1 K | **sicher** |
| M12 | Kuehl-Soll | in 14 104 Frames 24./25.10. immer 0x00 (kein Kuehlbetrieb) | **nicht pruefbar**, konsistent mit 0 = keine Kuehlanf. | Vermutung (bis Kuehltag) |
| 1520 | - | Volllogger 1520 = M0 (nicht M1: 14:45 1520 = 0 bei M1 = 56) | Echo von M0 | **sicher** |

WW-Wechsel 45 -> 50: im Volllogger 24.10. 00:00 bis 25.10. 09:00 steht 1497 = 1499 = **50,0 auch nachts**, kein 45. Ein 45->50-Wechsel kommt nicht vor (sicher, Datenstand). Statt dessen geprueft: 50 -> 52 (Kick 24.10. 13:00-16:00, 1497 = 52,0 von 13:00 bis 15:55) -> M1 56,0 statt 54,0.

## Was bringt uns das
- Die TopTronic gibt dem Kaelteregler **nicht** das HK1-Soll, sondern 1490 + 3 K. Wer den FBH-Vorlauf senken will, muss auch die 3 K Ueberhoehung (07-001) im Blick haben: bei 1490 = 30,0 bekommt der Verdichter 33,0 C.
- Die WW-Ladeueberhoehung ist **4,0 K** und nicht 3,5 K (Notiz CAN-SET 08.09.). 52 C Soll -> 56 C Ladesoll am Kaelteregler, 50 -> 54, 57 -> 61.
- Faellt eine WW-Ladung in eine Heizanforderung, steht auch M0 auf dem Ladesoll (54-56 C). Das erklaert hohe WP-VL-Sollwerte ohne SG.
- Die Aussentemperatur kommt beim Kaelteregler nur in 1-K-Stufen an (Rundung auf ganze Grad, Wechsel bei x,5). Fuer Einsatzgrenzen und Kennfeld-Analysen mit der Stufe rechnen.
- Reg 1520 im Volllogger ist das M0-Echo: fuer die Heizseite reicht der Volllogger, fuer WW-Ladestarts braucht man X26 M1 (1520 zeigt sie nicht, wenn keine Heizanforderung laeuft).

## Sicherheit
- sicher: M1 = 1497 + 4,0 K (WW-Anforderung), M0 = 1490 + 3 K auf 0,5 K abgerundet (Heizanforderung), M10 = AT gerundet auf 1 K, 1520 = M0-Echo, Richtung/CRC der Frames.
- wahrscheinlich: M0 = M1, wenn WW-Ladung und Heizanforderung gleichzeitig laufen (4 Faelle 24.10., Ursache in der TopTronic, nicht aus FW belegt).
- Vermutung: M12 = Kuehl-Soll im Codec (b-1)*0,5-40 (nie ungleich 0 gesehen).
- Zeitbasis: 25.10. war Zeitumstellung (Volllogger 02:00-02:59 doppelt). Die verglichenen 25.10.-Punkte liegen danach (01:09 davor); Sniffer und Volllogger passen zur Minute (03:55 beide), also gleiche Ortszeit.

## Offene Reste
1. M12 an einem Kuehltag 2027 (bleibt offen, siehe `[lokaler Pfad]`).
2. 05-001 (dp 5001) einmal lesen: 35 oder 40? Messung sagt 4,0 K. Falls 3,5 drinsteht, kommt das halbe Kelvin woanders her (Rundung nach oben?).
3. WW 45 -> 50: zurzeit nicht im Programm (1497 nachts 50,0). Erst pruefbar, wenn Loxone wieder ein Nachtsoll 45 schreibt.
4. M0 = M1 bei paralleler WW-Ladung: TopTronic-Logik nicht belegt. Pruefen, ob dann das Umschaltventil (19870) auf WW steht und der HK nur "mitlaeuft".

## Gegenpruefbare Stichprobe
Datei: `/home/<user>/rs485_sniff/log/rs485_2026-10-24.log.gz`, Zeit 14:24:58.919-.960 (Frame ueber 3 raw-Zeilen):
```
14:24:58.919 raw[ 11] 8210201720707000000000
14:24:58.939 raw[ 10] cd006400610000000000
14:24:58.960 raw[ 10] 00800080ffff002ec303
```
= `82 | 10 20 17 20 | 70 70 00 00 00 00 cd 00 64 00 61 00 00 ... | 2e c3 | 03`. CRC16-KERMIT ueber `10 .. 00` = 0xC32E -> passt.
M0 = 0x70 = 112 -> 56,0 C; M1 = 0x70 -> 56,0 C; M8 = 0x64 = 100; M10 = 0x61 = 97 -> (97-1)*0,5-40 = 8,0 C; M12 = 0x00.
Vergleich Volllogger `/home/<user>/hoxpi_fulllog/2026-10-24.csv` Zeile 14:25:02: 1497 = 520 (52,0 C, 52-C-Kick), 1520 = 560 (56,0), 1477 = 78 (7,8 C).
-> M1 = 52,0 + 4,0; M10 = round(7,8) = 8.
Reproduktion (Pi, lesend): `zcat ~/rs485_sniff/log/rs485_2026-10-24.log.gz | grep -m1 -A3 '^14:24:58.9'`