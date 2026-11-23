# ANALYSE F18 – Volumenstrom ohne Verdichter (24.10.2026, Orchestrator 01:54)

Frage (Katalog F18): 23.10. 20:51–22:51 lief Volumenstrom (31708) ohne Wärmezählung, VL ≈ RL ≈ 36 °C. Wer/was, wie oft, was kostet es?
Quelle: Volllogger `/home/<user>/hoxpi_fulllog/<tag>.csv` (5 min, Rohwerte ×10, 31708 in 0,1 L/min), nur gelesen.
Skripte: `[lokaler Pfad]` (Fenster/Episoden), `or_f18_20261024_0215_summe.py` (Tagessummen).

## Ergebnis
**Auslöser = Loxone-Heizanforderung an HK1, bei der die WP (noch) nicht startet (sicher).** Kein Frostschutz, kein Kühl-/Taupunktbetrieb, keine WW-Ladung.

| Zeit 23.10. | 31708 (L/min) | 19706 HK1-Pumpe | 1501 HK1-Status | 18722 WE-Status | 1539 WEZ | 1520 Soll | 1525 VL | 1535 RL | 1504 WW |
|---|---|---|---|---|---|---|---|---|---|
| 20:50 | 0 | 0 | 0 | 0 | 0 | 0 | 36,0 | 28,0 | 0 |
| 20:55 | 15,8 | 1 | 23 (Heizbetrieb extern) | 1 (Heizbetrieb) | 0 | 30,0 | 40,0 | 39,5 | 0 |
| 21:30 | 16,1 | 1 | 23 | 1 | 0 | 32,5 | 36,5 | 36,0 | 0 |
| 22:20 | 16,1 | 1 | 23 | 1 | 0 | 32,5 | 34,5 | 34,0 | 0 |
| 22:50 | 16,0 | 1 | 23 | 1 | 0 | 30,0 | 35,0 | 35,0 | 0 |
| 22:55 | 0 | 1 | 0 | 0 | 0 | 0 | 35,0 | 34,5 | 0 |

- Loxone schaltet HK1 auf „Heizbetrieb extern/Konstant“ (23) mit Soll 30–32,5 °C; Hoval-WE-Regelung meldet Heizbetrieb, HK1-Pumpe läuft.
- Verdichter startet nicht, weil RL (34–40 °C) nie ≤ Soll − 1,5 K (28,5–31 °C) fällt → HKA59-Bedingung (F5/F17) nie erfüllt. **Passt ohne Ausnahme zur Startregel aus F5/F17 (sicher, Gegenprobe).**
- Die Wärme kommt aus dem gespeicherten Wasser (Puffer/WP nach dem Lauf 19:07, 46 min): RL fällt in 2 h von 39,5 auf 34,0 °C. Sie geht in die FBH, ist also nicht verloren.
- Durchfluss ohne Verdichter ≈ 16 L/min (≈ 0,96 m³/h), WEZ-Pumpe 18739 = 0 %. Bei Verdichterlauf ≈ 34 L/min (F16). **Die HK1-Pumpe drückt also allein Wasser durch den WP-Wärmetauscher / WFA200-Durchflussmesser (wahrscheinlich: WP hydraulisch im HK1-Weg, Puffer nicht trennend).** Kurze Werte 23–34 L/min am Rand einer Episode = Übergang zu/aus einem Verdichterlauf.

## Häufigkeit (sicher, Volllogger 25.09.–23.10., 29 Tage)
Bedingung: 31708 > 5 L/min und 1539 = 0. In 98 % dieser Punkte steht HK1 auf 23.
- Summe 81,4 h, **Ø 2,8 h/Tag** (0 bis 7,5 h; Maxima 20.10. 7,5 h, 16.10. 6,8 h, 23.10. 5,2 h).
- Fast jede Heizanforderung hat solche Phasen: vor dem Start (Wartezeit HKA59 bis zu 15 min + RL über Schwelle) und lange Abend-Episoden, wenn Loxone nach einem Lauf weiter Wärme anfordert (16.10. 20:05–23:50, 18.10. 20:35–23:25, 23.10. 20:55–22:50).

## Kosten
ALPHA1 25-60 ≈ 28 W (`BAUTEILE_BEKANNT.md`): 2,8 h × 28 W ≈ **0,08 kWh/Tag ≈ 2,4 kWh/Monat** (wahrscheinlich; Pumpenleistung nicht gemessen). Vernachlässigbar.

## Was bringt uns das
- Die Episoden sind kein Fehler und keine Verschwendung: Loxone holt die Restwärme aus Puffer/WP in die FBH, bevor die WP neu startet. Das verlängert den Abstand zwischen Starts.
- Für Auswertungen: „Volumenstrom > 0 ohne Wärmezählung“ = HK1-Pumpe allein, kein Messfehler. WP-Laufzeit nie aus 31708 ableiten, sondern aus 1539/X4.