# X26 Obj 0x20 Schreibframes (TopTronic -> Kaelteregler): Gegenprobe Sollwerte 22.10.2026
Orchestrator-Punkt 18.10. 01:15 · Stand 22.10.2026 23:00 · nur lesend (Sniffer-Log, Volllogger, Prometheus)
Bezug: `FW_X26_claude_20261018.md` Abschnitt 3 (These M0/M1/M10/M12). Kein Doppel zu Byte28-35 / Byte47-91 (die betreffen den Lese-Block 0x64).

## Methode
- Quelle: `~/rs485_sniff/log/rs485_2026-10-22.log` (00:00:06 - 22:57:29), Parser `rs485_blk20.stream`.
- Gefiltert: Richtung Master, Kopf `10 20 17 20` (addr 0x10, op 0x20, len 23, obj 0x20) -> M[0..22]. **10009 Frames, alle CRC ok**, alle len 23 (keine len-16-Variante gesehen).
- Skript: `Emulation\or_x26soll_20261022_2300.py` (Aenderungsliste + Stundenhistogramm), Ausgabe Pi `/tmp/or_x26soll_22.out`.
  `Emulation\or_x26soll_20261022_2300_at.py` (Volllogger Reg 1520 stuendlich).
- Gegenwerte: Prometheus `hoval_ww_soll_c` (= dp 5051, 5-min), `hoval_sg_status`, `hoval_aussentemp_c` (1-min); Loxone-Ereigniszeiten aus Auftrag.
- Dekodierung: M0/M1 = b·0,5 °C; M10/M12 = (b-1)·0,5-40 °C (0 = keine Anforderung).

## Stichprobe (selbst nachpruefbar)
Log 18:39:38.729-.790 (Frame ueber 4 raw-Zeilen verteilt):
`82 10 20 17 20 | 00 70 00 00 00 00 cd 00 64 00 5f 40 00 00 00 00 00 80 00 80 ff ff 00 | d2 4f | 03`
CRC16-KERMIT ueber `10..00` = 0x4FD2 -> passt. M0=0x00 (kein Heizen), **M1=0x70=112 -> 56,0 °C**, M8=0x64=100, M10=0x5f=95 -> 7,0 °C, M11=0x40, M12=0.
Kontext: 3 min vorher (18:36:51) gleicher Frame mit M1=0x7a=122 -> 61,0 °C; Loxone senkte 18:38 dp5051 57 -> 52.
Reproduktion (Pi): `grep -m1 -A2 '18:39:38.7' ~/rs485_sniff/log/rs485_2026-10-22.log`
bzw. komplett: `cd /tmp && nice python3 or_x26soll_20261022_2300.py ~/rs485_sniff/log/rs485_2026-10-22.log 300`

## Tabelle: Ereignisse 22.10.2026 (CEST)
| Zeit X26 | Ereignis / dp5051-Soll (Prom.) | M1 (°C) | M0 (°C) | M8 | M10 (°C) | M11 | Aussen (Prom./Volllog) |
|---|---|---|---|---|---|---|---|
| 04:21:33 | Heizanforderung (Soll 50, ab 04:33 52) | 0 | 0 -> 34,5 | 0 -> 100 | 7,0 | 0 | - |
| 05:01:33 | Heizen aus | 0 | 34,5 -> 0 | 100 -> 0 | 7,0 | 0 | - |
| 05:48:21 | WW-Ladung, Soll 52 | **56,0** (=52+4) | 0 | 100 | 7,0 | 0 | - |
| 06:37:00 | WW-Ladung Ende | 0 | 0 | 0 | 7,0 | 0 | - |
| 07:01:33-08:34 | Heizen | 0 | 30,0 -> 34,5 / 34,0 / 33,0 | 100 | 6,0 | 0 | Reg 1520 = 34,0 (07:20, 08:20) |
| 09:56:12 | Loxone 09:55 Soll 57 | **61,0** (=57+4) | 0 | 0 -> 100 | 7,0 | 0 | - |
| 10:06:20 | Soll 57 -> 52 (Prom. 10:07) | **56,0** (=52+4) | 0 | 100 | 7,0 | 0 | - |
| 11:32:20 | Soll 52 -> 50, Ladung Ende | 0 | 0 | 0 | 9,0 | 0 | - |
| 13:14:27 | Loxone 13:14 Soll 57, SG 0 -> 1 | 0 | 0 | 0 | 11,0 | **0 -> 64** | - |
| 13:14:43 | WW-Ladung + Heiz-Anf. | **61,0** | **61,0** | 100 | 11,0 | 64 | Reg 1520 = 61,0 (13:20) |
| 13:51:15 | WW-Ladung Ende (Prom. Soll 56,1 13:53) | 0 | 38,5 | 100 | 11,0 | 64 | - |
| 13:55:07 / 14:00:04 | Heizen aus / SG 1 -> 0, Soll 50 | 0 | 0 | 0 | 11,0 | 64 -> 0 | - |
| 14:39:07 | Loxone 14:39 Soll 57, SG 1 | 0 (keine Ladung) | 0 | 0 | 11,0 | 0 -> 64 | - |
| 16:51:31 | SG 1 -> 0, Soll 50 (Prom. 16:56) | 0 | 0 | 0 | 11,0 | 64 -> 0 | - |
| 17:00:43 | Loxone 17:00 Soll 57, SG 1 | 0 (keine Ladung) | 0 | 0 | 11,0 | 0 -> 64 | - |
| 17:46:42 | SG 1 -> 0, Soll 50 (Prom. 17:48) | 0 | 0 | 0 | 9,0 | 64 -> 0 | - |
| 18:11:46 | Loxone 18:11 Soll 57, SG 1 | 0 | 0 | 0 | 8,0 | 0 -> 64 | - |
| 18:36:51 | WW-Ladung Start (Soll 57) | **61,0** | 0 | 0 -> 100 | 7,0 | 64 | - |
| 18:39:38 | Loxone 18:38 Soll 52 | **56,0** | 0 | 100 | 7,0 | 64 | - |
| 18:58:26 | Loxone 18:58 Soll 50, SG 1 -> 0 | 56,0 | 0 | 100 | 6,0 | 64 -> 0 | - |
| 18:59:06 | WW-Ladung Ende | 0 | 0 | 0 | 6,0 | 0 | - |
| 19:20 | - | 0 | 0 | 0 | **6,0** | 0 | 5,9 |
| 19:35:14 | M10 6 -> 5 | 0 | 0 | 0 | 5,0 | 0 | 5,5 |
| 21:17:30 | M10 5 -> 4 | 0 | 0 | 0 | 4,0 | 0 | 4,5 |
| 22:20 | - | 0 | 0 | 0 | **4,0** | 0 | 4,1 |
M12 war den ganzen Tag 0 (10009/10009 Frames). Stundenhistogramm: Ausgabe `/tmp/or_x26soll_22.out`.

## Urteil je These
| These (FW) | Messung | Urteil |
|---|---|---|
| M1 = WW-Soll (b·0,5) | M1 ist **nicht** der dp5051-Sollwert, sondern das **Ladesoll = dp5051 + 4,0 K**, und nur ≠0 solange eine WW-Anforderung laeuft (5 Ladungen: 52->56, 57->61, 52->56, 57->61, 52->56). Bei Soll 57 ohne Ladebedarf (14:39, 17:00, 18:11) bleibt M1 = 0. Sollsenkung waehrend Ladung wird nachgefuehrt (10:06, 18:39), Senkung auf 50 beendet die Anforderung (18:59:06, M1 -> 0). | **sicher** (Skala 0,5 und "≠0 = Anforderung"); "M1 = Soll" **widerlegt**, richtig: Soll + 4 K |
| Verzoegerung M1 | Loxone 09:55 -> 09:56:12; 18:38 -> 18:39:38; 18:58 -> 18:59:06 (Loxone-Sekunde unbekannt) | **wahrscheinlich ≤ ~1,5 min** (TopTronic-Zyklus); sekundengenau erst mit Loxone-/HoxPi-Schreibzeitstempel |
| M0 = Heiz-VL-Soll (b·0,5) | Heizen: 30,0 -> 34,5 / 34,0 / 33,0 °C bei AT 6-7 °C (plausibel Heizkurve FBH), aus = 0. Volllogger Reg 1520 zeigt dasselbe (34,0 / 61,0 / 0) -> Reg 1520 = Echo von M0. | **sicher** |
| M0 bei SG-Ready | 13:14:43 M0 = M1 = 61,0 bei SG=1 (Heizkreis/Puffer mit WW-Ladesoll angehoben); 13:51 M0 38,5, 13:55 0 | **wahrscheinlich** SG-Anhebung; Mechanismus offen |
| M10 = Aussen ((b-1)·0,5-40) | 19:2x M10 6,0 / AT 5,9; 22:2x 4,0 / 4,1. Wechsel 6->5 bei AT 5,5 (19:35), 5->4 bei AT 4,5 (21:17). Werte immer ganze °C (b immer ungerade), Flattern 11<->12 um 15:36-15:40. | **sicher**; Aufloesung faktisch **1 K** (TopTronic rundet auf ganze Grad, keine Hysterese) |
| M12 = Kuehl-Soll | ganzer Tag 0 - kein Kuehlbetrieb | **nicht pruefbar** (Kuehltag noetig); konsistent mit "0 = keine Anforderung" |
| M8 = Leistungsbegrenzung % | 100 genau dann, wenn M0 oder M1 ≠ 0, sonst 0 | **wahrscheinlich** "Leistungsfreigabe %" (heute nur 0/100) |
| M11 Bit7 (FW) | Bit7 nie gesetzt. **Bit6 (0x40) = SG-Ready-Status**: 4 von 4 Ein-/Aus-Flanken treffen `hoval_sg_status` auf die Minute (13:14/14:00, 14:39/16:51, 17:00/17:46, 18:11/18:58) | Bit6 = SG **sicher (Zeitkorrelation)**; Bit7 offen |

## Was bringt uns das
- Die WW-Ladeueberhoehung ist **4 K**: wer 57 °C will, bekommt am Kaelteregler 61 °C Ladesoll. Fuer die Hochdruck-/Heissgas-Grenze ist 61 °C die relevante Zahl, nicht 57.
- WW-Anforderung sekundengenau sichtbar (M1 ≠ 0), ohne Modbus-Polling - Start, Nachfuehrung und Abbruch (z. B. 18:58 durch Loxone) sind direkt im Sniffer belegbar.
- SG-Ready-Status kommt nachweislich beim Kaelteregler an (M11 0x40). Damit laesst sich pruefen, ob SG=1 tatsaechlich Laufzeit erzeugt (heute: nur 13:14 und 18:36 Ladungen, 14:39/17:00 ohne Wirkung, weil Speicher warm).
- M0 = Reg 1520: Heiz-VL-Soll ist schon im Volllogger da; X26 liefert ihn zusaetzlich sekundengenau.
- Aussentemperatur an die WP nur in ganzen Grad - fuer Regelanalysen am Kaelteregler mit 1-K-Stufen rechnen.

## Offene Punkte
1. M12 an einem Kuehltag pruefen (Kuehl-Soll, Codec (b-1)·0,5-40?).
3. 13:14-13:55: warum M0 = 61 (SG-Anhebung Heizkreis?) und `hoval_ww_soll_c` 56,1 um 13:53 - mit hc1_status / Pufferfuehler abgleichen.
4. Exakte Verzoegerung: Loxone-Schreibzeitstempel (Sekunde) gegen Frame-Zeit.
5. M8 bei Teillast/Leistungsbegrenzung (Werte ≠ 0/100) und M11 Bit7 bisher nie gesehen; M6 = 0xCD und M17/M19 = 0x80, M20/21 = 0xFF konstant - Rolle laut FW ohne Leser.