# F164: Wann schreibt Loxone 1490 zurueck? (Orchestrator 06.11.2026 11:54)

Quellen: Projektdatei `[lokaler Pfad]` (nur gelesen, Skript `[lokaler Pfad]`), Bridge-Protokoll `journalctl -u hoval-bridge` ab 05.11. 23:03 (`or_f164b_pi.py`), HoxPi `schreiblast`, Volllogger.
Vorbehalt: Ob die Datei genau dem Stand im Miniserver entspricht, ist hier nicht geprueft. Der Aktor ist seit Langem unveraendert [wahrscheinlich].

## Ergebnis
1. **Baustein [sicher aus der Datei]:** Der Aktor `Sollvorlauftemperatur Heizen HC1` (AMQ46, ModbusAddress 1490, RepeatRate 300) haengt an der Formel `1490 inkl. Ofen-Nachlauf` <- `Sollwert Heizen 1490` (Multiplexer) <- `Vorlautemperatur HC1` (Heatmixer2 AQf) <- Aussentemperatur 1477. Doku: https://www.loxone.com/dede/kb/heizkurve/ (Heatmixer), https://www.loxone.com/dede/kb/formel/, https://www.loxone.com/dede/kb/analog-multiplexer/, https://www.loxone.com/dede/kb/klimacontroller/
2. **Takt [sicher aus 216 Abstaenden 05.11. 23:03 - 06.11. 11:55]:** 50 % der Abstaende liegen bei 295-305 s, der Rest kuerzer (unteres Quartil 120 s). Also zwei Ausloeser: Wiederholung nach 300 s und ein frueheres Schreiben. Die kurzen Abstaende sind Vielfache von rund 20 s, und der gerundete Wert bleibt dabei oft gleich (<MAC> fuenfmal 331).
3. **Frueheres Schreiben kommt bei einer Aenderung des Eingangs [wahrscheinlich]:** Der Aktor sendet, sobald sich der ungerundete Wert aendert, also vor allem, wenn 1477 sich bewegt. Einzeln gegen 1477 belegt ist das nicht, 1477 liegt nur im 5-min-Raster vor (MD-92).
4. **Stillstand ist nicht der Ausloeser [wahrscheinlich]:** 06.11. Median Abstand im Lauf 241 s (n 116), im Stillstand 222 s (n 61). Die Vermutung aus E6/E15 ist damit ohne Stuetze.
5. **Rueckkehr nach den 5 eigenen Schreibvorgaengen (Bridge-Zeiten):**

| Versuch | Eigener Wert, Zeit | Loxone danach | Abstand | Zustand |
|---|---|---|---|---|
| E9 | 351, 07:00:21 | 331, 07:02:54 | 153 s | Lauf |
| E5 | 329, 07:03:53 | 331, 07:07:54 | 241 s | Lauf, endete dadurch |
| E11 | 371, 08:13:39 | 331, 08:14:41 | 62 s | Lauf |
| E6 | 345, 10:54:47 | 305, 10:54:55 | 8 s | Stillstand |
| E15 | 340, 11:00:09 | 305, 11:00:15 | 6 s | Stillstand |

**Offen:** Zweimal unter 10 s bei rund 222 s Median-Abstand ist als Zufall unwahrscheinlich (grob 1 % bei 5 Versuchen). Das widerspricht Punkt 4 nicht sicher, erklaert ist es aber nicht. 10:54:55 war zugleich ein Wertwechsel 306 auf 305. E18 prueft das mit Wiederholungen. F164 bleibt darum `teilweise`.

**1497 zum Vergleich [sicher]:** 97 % der 158 Abstaende bei 295-305 s, reine Wiederholung. Die Beobachtung "immer rund 1:45 nach dem 5-min-Raster" (E4, E7, E12) ist nur die Phase dieses Takts: 08:56:45 und 10:01:46 liegen genau 13 x 300 s auseinander, die Phase verschiebt sich, sobald Loxone den Wert aendert. E7 hielt 96 s, E12 35 s.

## Was bringt uns das
- Fuer Versuche an 1490 und 1497: Schreibzeit nicht ans Uhr-Raster legen, sondern direkt nach dem letzten `SET reg` im Bridge-Protokoll. Bei 1497 haelt das rund 5 min. Bei 1490 ist es bei ruhiger Aussentemperatur am laengsten, bei steigender oft nur 2-3 min.
- Die Versuche E6/E14 sind damit fahrbar, wenn das Schreiben nach jedem Loxone-Takt wiederholt wird. E6 wird dabei den Timer pruefen muessen: Jeder Rueckschreibwert liegt kurz unter der Schwelle.
- Fuer die Regelkette: 1490 aendert sich in Schritten von 0,1 K mit der Aussentemperatur und wird dabei bis zu dreimal je 5 min gesendet (Schreiblast gering, 0,4 je min).
- der Betreiber muss nichts tun.