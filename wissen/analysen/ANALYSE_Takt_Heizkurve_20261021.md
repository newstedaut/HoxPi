# ANALYSE Taktung + Vorlauf-Überhöhung Heizbetrieb – 21.10.2026 (Orchestrator, nur lesend)

Daten: `~/hoxpi_fulllog/kuehltest.csv` (1-min-Raster, 20.09.–21.10.2026, 45 837 Zeilen, keine Lücke > 10 min) und Volllogger `~/hoxpi_fulllog/2026-10-13…21` (5-min).
Skripte: `HoxPi-Doku\or_takt_heizkurve_20261021_2000.py/.out`, `or_wezsoll_20261021_2010.py/.out/b.out`.

## 1. Taktung (Verdichter an = Modulation > 0, Heizen + WW zusammen)
| Größe | Wert |
|---|---|
| Läufe 20.09.–21.10. | 208 (≈ 6,5/Tag, davon ~3/Tag WW-Ladungen laut Loop) |
| Laufdauer | <10 min: 24 · 10–15: 3 · 15–30: 73 · 30–60: 90 · 60–120: 18 · >120: 0 |
| Pause zwischen Läufen (Okt.) | Median 88 min, < 20 min nur 17 von 143 |
| kältester Tag (13.10., Ø 7,5 °C) | 11 Starts, 6,9 h Laufzeit |

**Sicher:** Kein Takt-Problem. 6–11 Starts/Tag liegen weit unter dem, was man bei einer 17-kW-Maschine im Übergang befürchtet.
**Wahrscheinlich:** Die 24 Kurzläufe < 10 min sind überwiegend Abbrüche/Kurzanforderungen (z. B. 15:25–15:34 am 21.10.) – Zuordnung Heizen/WW/Abtauung ist mit diesen Spalten nicht trennbar.

## 2. Vorlauf über Soll im Heizbetrieb (Oktober, Pumpe HK1 an, Verdichter läuft)
| Außen (°C, 2-K-Klassen) | n (min) | VL | RL | ΔT | HK-Soll Reg 1490 | Modulation |
|---|---|---|---|---|---|---|
| 2 | 132 | 35,6 | 33,4 | 2,2 | 32,8 | 39 % |
| 6 | 118 | 36,9 | 34,0 | 3,0 | 31,2 | 37 % |
| 10 | 493 | 36,8 | 33,0 | 3,8 | 30,3 | 36 % |
| 14 | 190 | 39,1 | 34,7 | 4,5 | 33,2 | 37 % |
| 18 | 117 | 38,3 | 34,1 | 4,2 | 32,1 | 36 % |

- **Sicher (Volllogger):** WEZ-Soll Reg 18724 = HK-Soll Reg 1490 („Vorlauf Soll Konstantanf. Heizen") **+ 2,6…3,0 K** – das ist die WEZ-Überhöhung Reg 30684/30685 = **3,0 K**.
- **Sicher:** Der gemessene VL liegt im Mittel **~6 K über 1490**, also nochmals ~3 K über dem WEZ-Soll.
- **Sicher:** Die Modulation klebt bei 35–39 % – praktisch am unteren Rand. Die Maschine kann nicht weiter herunter und schiebt den VL hoch, bis sie abschaltet.
- **Auffällig:** Reg 1490 (Konstantanforderung, wahrscheinlich von Loxone gesetzt) steigt bei Kälte kaum (2 °C: 32,8 / 10 °C: 30,3) – es verhält sich nicht wie eine Heizkurve. Wer 1490 schreibt, ist hier nicht geprüft.

## 3. Einstellvorschlag (nur Vorschlag, nichts geschrieben)
1. **WEZ-Überhöhung Reg 30684/30685 von 3,0 K auf 1,5 K** (über Bedienteil/Fachmann, nicht in der HoxPi-Whitelist). Eine Woche beobachten: Raumtemperaturen UG/OG, Laufzeit, Starts.
2. Danach ggf. auf 1,0 K. Nicht auf 0: der Puffer EnerVal 300 (282,4 l) [Korr. 23.10.2026, stand „CombiVal-Puffer (400 l)“] sitzt zwischen WP und Heizkreisen, etwas Überhöhung gleicht Mischung/Verluste aus.
3. Prüfen, woher 1490 kommt (Loxone-Baustein?). Wenn Loxone eine feste Anforderung schickt, wäre eine echte außentemperaturgeführte Kurve (kälter → höher, 10 °C → ~28 °C) sinnvoller als ein fast konstanter Wert.

**Was bringt uns das:** Je 1 K weniger Vorlauf grob 2–3 % weniger Strom. 1,5 K weniger Überhöhung ≈ 3–4 % im Heizbetrieb – im Winter spürbar, ohne Komfortverlust, solange die Räume ihr Soll halten. Risiko: Wird ein Raum zu kalt, Überhöhung wieder hoch – vollständig umkehrbar.

**Noch zu prüfen (Loop, lesend):** VL-Verlauf eines einzelnen Heizlaufs im 1-min-Raster (steigt VL bis Abschaltung = Überschwingen am Modulationsminimum?), und welcher Teilnehmer Reg 1490 schreibt.