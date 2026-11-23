# Verdichterlaeufe aus X26 Obj 0x20 (0,5-s-Takt) — 22.10.2026 00:00–14:57 (Orchestrator 15:30)

Daten: `~/rs485_sniff/log/rs485_2026-10-22.log` (53 910 Antworten Obj 0x20), nur lesend. Skript `Emulation\or_takt_20261022_1530.py`, Ausgabe `.out`.
Kanaele (firmwaregeprueft 15:20, Atlas Status 3): Byte 30 = Modulation %, 29 = Ruecklauf ((b-1)*0,5-10), 33 = WEZ-Status (1 Heizen, 4 WW), 90-91 = P_el.
Lauf = Modulation > 0, Lauf endet nach > 60 s mit 0. Die 21.10.-Datei ist gz — `rs485_blk20.stream` liest sie nicht (0 Punkte) → nur heute.

| Start | Ende | min | Art (Status) | Mod min/med/max % | RL Start → Ende °C | P_el med W | kWh el | Pause davor min |
|---|---|---|---|---|---|---|---|---|
| 04:22:00 | 05:01:34 | 39,6 | Heizen (1) | 13/35/50 | 30,0 → 36,0 | 1810 | 1,20 | – |
| 05:48:46 | 06:37:01 | 48,2 | WW (4) | 9/37/79 | 28,0 → 53,5 | 2600 | 2,32 | 47 |
| 07:21:27 | 07:49:57 | 28,5 | Heizen (1) | 1/35/49 | 31,5 → 36,0 | 1800 | 0,86 | 44 |
| 08:18:32 | 08:34:38 | 16,1 | Heizen (1) | 3/35/49 | 30,5 → 33,0 | 1720 | 0,47 | 29 |
| 09:56:37 | 11:32:20 | 95,7 | WW (4) | 9/60/78 | 24,0 → 53,5 | 3990 | 5,92 | 82 |
| 13:15:07 | 13:51:17 | 36,2 | WW-Boost SG Vorzug (4)* | 2/33/52 | 35,5 → 59,0 | 2740 | 1,65 | 103 |

*Skript hat diesen Lauf als „HK" gezaehlt (Byte 22 > 0 waehrend Boost); nach Status 4 und RL 59 °C ist es eine WW-Ladung. Sicher.

## Befund
- **Sicher:** 6 Starts in 15 h, davon 3 Heizlaeufe (16–40 min, Pausen 29–47 min) bei Aussen ~7–11 °C. Kein Kurztakten im engeren Sinn (< 10 min) heute.
- **Sicher:** Heizlaeufe modulieren im Median 35 % (Maximum ~50 %), P_el ~1,8 kW. Die Minima 1–13 % sind die Abregelrampe am Laufende.
- **Wahrscheinlich:** Heizlaeufe enden, wenn der Ruecklauf ~36 °C erreicht (2 von 3 Laeufen exakt 36,0; HK-Soll 1529 = 34,5) → Abschaltung ueber Ruecklauf ≈ Soll + 1,5 K. Der 08:18-Lauf endete schon bei RL 33,0 (16 min) — Ursache offen (Raum-/Loxone-Abschaltung?).
- **Vermutung:** Der kurze 08:18-Lauf und die 29-min-Pause passen zu einer Loxone-Freigabe, die die Anforderung abschaltet, nicht zur WP-Hysterese.

## Was bringt uns das
- Taktung ist bei Uebergangswetter unkritisch; die Heizlaeufe sind lang genug. Fuer den Winter ist die Frage, ob die feste 1490-Vorgabe (keine Heizkurve, siehe `ANALYSE_Heizsoll_1490_1529_Aussen_20261022.md`) bei Frost zu kurze Laeufe/zu tiefen VL bringt — dieselbe Auswertung im ersten Frostlauf wiederholen.
- **Einstellvorschlag (der Betreiber entscheidet, nichts gesetzt):** keiner neu. Die schon vorgeschlagene aussentemperaturgefuehrte 1490-Kurve wuerde die Laeufe bei Waerme kuerzer/seltener und bei Frost laenger machen — das ist erwuenscht.
- Werkzeug: diese Auswertung braucht keinen Modbus mehr und ist sekundengenau. Fuer Vortage muss `rs485_blk20.stream` .gz lesen koennen (oder vorher entpacken nach /tmp) — Aufgabe fuer den Loop.

## Offen fuer den Loop (nur lesend)
- 08:18–08:34: Loxone-Anforderung/Raumfuehler gegen Laufende legen (warum Ende bei RL 33?).
- Gleiche Tabelle fuer 19.–21.10. aus den .gz (zcat nach /tmp).