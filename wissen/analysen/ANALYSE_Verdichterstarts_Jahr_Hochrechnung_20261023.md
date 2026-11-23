# ANALYSE Verdichterstarts pro Jahr – Hochrechnung aus dem Volllogger (Orchestrator 23.10.2026 13:00)

Quelle: Pi `~/hoxpi_fulllog/2026-07-30.csv.gz` … `2026-10-23.csv` (5-min-Raster, 86 Tage), nur lesend.
Skript `[lokaler Pfad]` (auf dem Pi unter /tmp ausgeführt), Rohausgabe `...\Emulation\or_starts_jahr_20261023_1300.out`.
Start = 18726 (Modulation) von 0 auf >0; Art nach 1539 (1 Heizen, 4 WW, 2 Kühlen). Außentemp. = 1477/10 (Tagesmittel). Keine Datenlücken außer 03.09. (1 Lücke).

## Gegenprobe (sicher)
16.–22.10.: 10/7/7/8/5/6/7 Starts – identisch mit `ANALYSE_Heizlauf_Enden_Ursache_16-23Okt_20261023.md` (anderes Skript, andere Kopie). ✔

## Starts je Tag nach Betriebsregime (sicher, gemessen)
| Regime | Tage | AT-Mittel | Starts/Tag | Laufzeit je Start |
|---|---|---|---|---|
| Kühlsommer (31.07.–16.08.) | 17 | 20–25 °C | **13,8** (≈10 Kühlen + 3 WW) | **10–12 min** |
| Mild, nur WW/etwas Heizen (18.–28.08., 12.–21.09.) | 21 | 13–20 °C | 4,8 | 25–45 min |
| Übergang Heizen (22.09.–22.10.) | 31 | 9–13 °C | 6,6 | 20–45 min |
| Kalt (13.10., 22.10., 23.10. bis 13 Uhr) | 3 | 3–8 °C | 7–9 (23.10. hochgerechnet ~10) | 40–55 min |

Heizläufe-Median: Aug 20 min, Sep 20 min, Okt 25 min; ≤ 20 min: 23/30, 38/66, 31/84 – der Anteil kurzer Heizläufe sinkt mit kälterem Wetter.

## Hochrechnung aufs Jahr (Vermutung – Klimatage Alpenort (~960 m) grob geschätzt, kein Messwert < 3 °C)
- AT < 9 °C (Nov–Mär, ~150 Tage) × 8–10 = 1.200–1.500
- 9–13 °C (Apr/Mai/Okt, ~80 Tage) × 6,6 ≈ 530
- 13–20 °C ohne Kühlen (~75 Tage) × 4,8 ≈ 360
- Kühltage wie 2026 (~60 Tage) × 13,8 ≈ 830
- **Summe ≈ 2.900–3.200 Starts/Jahr**, ohne Kühlbetrieb ≈ 2.100–2.400.

## Einordnung
- Unter dem Loop-Ziel < 4.000 und klar unter der Fraunhofer-Grenze (90 % der WP < 5.500/a, `IDM-Doku\Recherche_laufend\FUND_Verdichter_Starts_Mindestlaufzeit_Oelrueckfuehrung_20261023.md`).
- Hoval-Grenze 3 Starts/Stunde (Katalog 2026/27 S. 49/50) wird nie erreicht.
- **Wahrscheinlich:** Die meisten und kürzesten Starts des Jahres kommen vom **Kühlen** (10–12 min je Start, ~28 % aller Starts), nicht vom Heizen. Deckt sich mit Z4 (Kühltakt = Verschleiß-, kein Energiethema).
- Im Winter werden die Läufe länger (23.10.: 55 min/Start) – ein Explodieren der Startzahl bei Frost ist nach den Daten unwahrscheinlich; Abtauungen (keine im Messzeitraum) zählen hier nicht als Start.

## Was bringt uns das
Die Startzahl ist kein akutes Verschleißproblem. Der Hebel MinHr 60 / Mindestlaufzeit ab Verdichterstart verbessert vor allem die Laufzeit je Start (Effizienz, Ölrückführung), nicht die Jahresbilanz. Wenn Verschleiß sparen: im Sommer Kühlen mit längerer Mindestlaufzeit/größerer Schaltdifferenz – dort sind die 10-min-Läufe.

## Offen / nicht ermittelbar
- Starts bei < 0 °C und mit Abtauungen: ab erstem Frost nachzählen (Loop, lesend).
- Klimatage Alpenort (~960 m) nur geschätzt (keine eigene Jahresreihe).