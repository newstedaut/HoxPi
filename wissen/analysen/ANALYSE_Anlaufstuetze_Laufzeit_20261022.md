# ANALYSE Anlaufstütze 42 % und Laufzeiten je Start — 22.10.2026 00:10 (Orchestrator)

Quelle: `~/hoxpi_fulllog/ww_hires.csv` 20.09.–21.10.2026 (66 916 Zeilen; Raster 10 s während WW-Ladung, sonst 60 s), nur lesend.
Skripte: `HoxPi-Doku\or_anlauf_20261022_0000.py/.out`, `HoxPi-Doku\or_anlauf2_20261022_0010.py/.out`.
Frage: D-02-Gegenprobe Teil 2 aus `02_Status_Offen.md` — greift die 42-%-Anlaufstütze sichtbar? (Teil 1, HD-Haltepunkt R35 = 88, braucht X4-Slave-5-Daten und bleibt offen.)

## Ergebnis (sicher, aus Messdaten)
| | WW-Starts | Heiz-Starts |
|---|---|---|
| Starts | 86 | 123 |
| 42 % erreicht nach | Median 20 s, max 30 s (Hochlauf 10–28 % → kurzer Überschwinger 43–49 % → 42) | sofort (1-min-Raster) |
| Plateau ≥ 42 % endet nach | Median 711 s (p10 220 s, p90 2000 s) — danach steigt/fällt nach WW-Bedarf | **Median 180 s, p10/p90 179/240 s** → dann 35 % |
| Laufdauer | Median 42,6 min | Median 23 min |
| Läufe < 10 min / < 6 min | 2 / 1 | **21 / 12** |

- **Anlaufstütze bestätigt:** Nach dem Hochlauf (≈ 20–30 s) fällt die Modulation in keinem der 209 Starts unter 42 %, bevor 180 s um sind. Im Heizbetrieb endet die Stütze sehr genau nach **3 min** und die Modulation geht auf den Heizboden 35 %. Passt zur Loop-Vorhersage **V98 (Startboden 42 % für 180–210 s)** — jetzt an 123 Heizstarts gestützt (1-min-Raster, ±60 s).
- Die „< 42 %“-Treffer in den ersten Sekunden der WW-Starts sind der Hochlauf selbst (erste 10-s-Probe 9–28 %), keine Verletzung der Stütze.

## Neu (wahrscheinlich, Vermutung zur Prüfung)
- **Mindestlaufzeit ≈ 5 min:** Die kürzesten Heizläufe enden auffällig oft genau nach **5,0 min** (10 von 12 Läufen < 6 min; nur ein WW-Lauf mit 4,3 min, gleich nach einer 8,5-min-Ladung). Zusammen mit **V99 (Mindeststehzeit 15 min)** sieht das nach einem festen Takt-Schutz 5 min an / 15 min aus aus. Nur 1-min-Raster — nicht belegt.
- Kurzläufe treten gehäuft bei milder Außentemperatur auf (13–19 °C) und morgens in Serien (26.09. 06:55/07:15/07:36 je 5 min bei 5,8 °C).

## Was bringt uns das
- Der Zwilling/Loxone kann jeden Start sicher mit **3 min × 42 %** rechnen (Strom- und Wärmespitze am Anfang), danach 35 % im Heizbetrieb.
- Etwa **10 % der Heizläufe sind Kurzläufe (≤ 5 min)** — das ist der Bereich, wo die offene Überhöhung 30684/30685 (3,0 → 1,5 K, **der Betreiber entscheidet**) und die Loxone-Kurzlauf-Formel greifen müssten. Kein Handlungsbedarf an der Hoval selbst.
- Für die Loop-Messung: V98 ist im Heizbetrieb erledigt; offen bleibt nur die genaue Dauer in Sekunden (X4 `0x0066`, wenn der Sniffer am Start nicht ausfällt).