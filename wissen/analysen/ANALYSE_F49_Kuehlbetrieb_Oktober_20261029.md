# ANALYSE F49 – Wurde seit September real gekühlt? (OR 29.10.2026 17:00)

Frage (02_Status_Offen Z. 138, OR 22.10. 20:54): Der WZ-Raumregler UG stand am 20.10. 14:14 und 22.10. 13:56 im Kühlmodus (Komfort Kühlen 22,5 °C). Hat die WP im Oktober wirklich gekühlt?

Methode (nur lesen): Volllogger `~/hoxpi_fulllog/2026-07-30.csv.gz` … `2026-10-27.csv.gz` (90 Dateien, 5-min), Spalten 27487 (Wärmemenge Kühlen_low, Roh = kWh), 18736 (Aktuelle Leistung Kühlen_low), 1539 (WP-Status). Live 29.10. ~17:00: `read_register 27487`.
Skript `[lokaler Pfad]`, Ausgabe `…\Emulation\or_f49kuehl_20261029_1700.out`.

## Ergebnis
| Zeitraum | 27487 (kWh Kühlen) | 1539 = 2 (5-min-Zeilen) |
|---|---|---|
| 30.07.–31.08. | 0 (Spalte vor 01.09. nicht befüllt – wahrscheinlich) | täglich 1–19 |
| 01.09.–12.09. | 432 → 522 (+90 kWh in 12 Tagen) | 06.–08.09. 16–30, 12.09. 1 |
| 13.09.–27.10. | **522 konstant** | **0** |
| 29.10. live | 0,522 MWh = 522 | – |

- **Sicher:** Seit 12.09.2026 keine Kühlenergie mehr (Zähler steht 47 Tage auf 522 kWh, live bestätigt). Im Oktober wurde **nicht** gekühlt, auch nicht am 20.10./22.10.
- **Wahrscheinlich:** 1539 = 2 ist der Kühlbetrieb (verschwindet am selben Tag, an dem der Zähler stehen bleibt).
- **Sicher:** 18736 „Aktuelle Leistung Kühlen“ ist in allen 90 Dateien 0, auch während der Zähler im September stieg → totes/ungenutztes Register, nicht als Kühl-Indikator verwenden.
- Folge: Die Kühlfalle (F4) hat im Oktober nur Wärmeanforderung unterdrückt, keinen Kühlstrom verursacht.

## Was bringt uns das
Kein versteckter Kühlverbrauch im Oktober; die Oktober-Energiebilanz (MD-08) braucht keine Kühlkorrektur. Wächter-Vorschlag für den Loop: Kühlen = Anstieg 27487 bzw. 1539 = 2, nicht 18736.
Nichts an der Anlage, Loxone oder Pi-Diensten geändert.