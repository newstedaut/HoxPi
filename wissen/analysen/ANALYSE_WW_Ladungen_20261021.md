# ANALYSE Warmwasser-Ladungen Oktober + lange Abendladung 21.10. 19:26 - 21.10.2026 (Orchestrator, nur lesend)

> → Korrektur 25.10.2026 (ersetzt den Vermerk vom 23.10.): soweit hier mit 300 l / 0,349 kWh/K gerechnet wird, gilt verbindlich das wirksame WW-Volumen des CombiVal ESR 400 von ~405 l, C = 0,47 ± 0,04 kWh/K (F1, 20 zapffreie Ladungen, `[lokaler Pfad]`). Speicher-Wärmemengen und Verluste hier um Faktor 1,35 (+35 %) nach oben korrigieren, nicht +26 %. (EnerVal 300 = Puffer, CombiVal ESR 400 = WW.)

Daten: `~/hoxpi_fulllog/ww_hires.csv` (1-min, 20.09.-21.10.2026, 66 856 Zeilen) und `~/ww_abnahme.csv` (Gegenprobe 21.10.).
Skripte: `HoxPi-Doku\or_wwladung_20261021_2300.py/.out`, `or_wwladung2_20261021_2310.py/.out`.
Einheiten (gegen ww_abnahme.csv geprüft): `P_el` Roh = 10 W (433 = 4,33 kW = Reg 25611), `P_th` Roh = kW (ganzzahlig, daher Wärmemenge nur ±10 %).
Ladung = Speicherladepumpe SLP an, ≥ 5 min.

## 1. Oktober 01.-21. (72 Ladungen, 21 Tage)
| Größe | Wert |
|---|---|
| Ladungen/Tag | 3,4 (Dauer Median 45 min) |
| Strom WW | 145,9 kWh_el = **6,9 kWh_el/Tag** |
| Wärme WW (grob) | ~465 kWh_th = ~22 kWh_th/Tag |
| Arbeitszahl WW | **~3,2** |

| wirksamer Soll | n | kWh_el/Ladung | kWh_th | AZ | Dauer med | Ende-Ist | Uhrzeiten |
|---|---|---|---|---|---|---|---|
| 50 °C | 13 | 1,76 | 5,8 | 3,3 | 36 min | 50,0 | verstreut |
| 52 °C | 16 | 1,93 | 5,8 | 3,0 | 41 min | 51,9 | 03-07 Uhr (Morgenladung) |
| 57 °C | 43 | 2,14 | 6,9 | 3,2 | 49 min | 54,0 | 11-20 Uhr |

- **Sicher:** 60 % der Ladungen laufen mit wirksamem Soll 57 °C (Speicher-Soll 61), obwohl der WW-Grundsoll meist 50 °C zeigt - das ist der Boost-/Komfortpfad (Loxone dp 5051 bzw. Zeitprogramm), nicht der Grundsoll.
- **Sicher:** Bei 57 °C endet die Ladung im Mittel bei Ist 54,0 °C, nicht bei 57 - abgeschaltet wird über SF2 (unten) bzw. Speicher-Soll, nicht über SF oben.
- **Wahrscheinlich:** Die 57er-Ladungen kosten pro kWh Wärme kaum mehr (AZ 3,2 gegen 3,3) - die WP fährt dabei auf Modulation 33 % (Minimum) und gutem Hub. Der Preis ist eher der höhere Speicherverlust bei 54-56 °C (grob +1,4 kWh_th je 4 K auf 300 l), nicht schlechterer COP.

## 2. Abendladung 21.10. 19:26-20:53 (87 min, längste im Oktober)
| Zeit | SF oben | SF2 unten | WEZ-VL | Modulation | P_el |
|---|---|---|---|---|---|
| 19:25 | 45,2 | 45,0 | - | 0 | 0 |
| 19:30 | 44,5 | 40,7 | 42,4 | 72 % | 4,3 kW |
| 19:45 | 41,7 | **24,3** | 45,3 | 72 % | 4,5 kW |
| 20:10 | 45,5 | 37,6 | 53,7 | 44 % | 3,1 kW |
| 20:50 | 51,8 | 49,5 | 57,9 | 33 % | 2,7 kW |

- **Sicher:** Kurz um 19:40 stand der WW-Soll auf 57 (Speicher-Soll 61), danach wieder 52/56 - ein einzelner Boost-Impuls, ohne Einfluss auf die Dauer.
- Strom ~4,7 kWh_el, Wärme ~15 kWh_th (Q_ww 39925 → 39940) → AZ ~3,2. Alle 9 Ladungen > 60 min im Oktober liegen ähnlich (Start mit kaltem SF2 27-44 °C, meist abends 19-21 Uhr).

## Einstellvorschlag / Was bringt uns das
- **Kein Handlungsbedarf bei der WP.** Lange Abendladungen sind Zapfungen, Taktung und Arbeitszahl im WW passen.
- Optional (**der Betreiber entscheidet**, Loxone, nicht Hoval): Wenn abends regelmäßig gebadet/geduscht wird, die 57er-Ladung 11-17 Uhr nicht anfassen (PV-Fenster), aber prüfen, ob die 57er-Ladungen 19-20 Uhr nötig sind - mit 52 °C abends spart man ~0,4 kWh_el je Ladung (2,14 → ~1,8), bei ~1 Abendladung/Tag ~12 kWh_el/Monat (~2,5 €). Klein, aber gratis.
- Nebenbefund: Spalte `WP_VL` in ww_hires.csv stand bis 17.10. konstant 30,7 (Loggerspalte erst seit 17.10. gültig) - für Auswertungen vor dem 17.10. nicht verwenden.