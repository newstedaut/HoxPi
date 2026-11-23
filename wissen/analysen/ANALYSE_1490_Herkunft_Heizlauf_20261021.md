# ANALYSE Reg 1490 – wer schreibt es, und wie verläuft ein Heizlauf – 21.10.2026 (Orchestrator, nur lesend)

Folgt auf `ANALYSE_Takt_Heizkurve_20261021.md` (offene Fragen: Schreiber von 1490, VL-Verlauf im Lauf).
Daten: Loxone-Projektdatei `Loxone-Umbau\UMBAU_nur_schaltschrank_20261018_TEST.Loxone` (neueste, UUIDs stimmen mit dem Live-Miniserver überein: `HK1 Vorlauf soll (Loxone)` = 21fab011-0173 gefunden), `~/hoxpi_fulllog/kuehltest.csv` 01.–21.10. (1-min, 29 997 Zeilen), Loxone-Livewerte 21.10. 20:57.
Skripte: `HoxPi-Doku\or_1490kette_20261021_2105.py/.out`, `or_1490herkunft_20261021_2115.py/.out`.

## 1. Wer schreibt 1490 – geklärt (sicher)
Loxone, über diese Kette:
1. **Heatmixer2** „Vorlautemperatur HC1 – Fußboden Heizen+Kühlen“ (ControllerMode 1, an den Klimacontroller HC1 gekoppelt): Steilheit **0,9**, Max **40 °C**, Min ← „Taupunkt + Reserve“; weitere Parameter PrevInc 2, BufferInc 5, Transconductance 0,3, Treshold 35, Gain 1. Eingänge Boost/InBuffer **nicht** beschaltet.
2. **AnalogMultiplexer** „Sollwert Heizen 1490“ – gibt den Heatmixer-Wert nur weiter, wenn der Klimacontroller Heizen anfordert, sonst 0.
3. **Formel** „1490 inkl. Ofen-Nachlauf (min. 24 °C)“ – Ofen-Nachlauf ⇒ max(Wert; 24); Kurzlauf-Schutz (seit 18.10.) ⇒ HK1-VL-Ist (min. 20), solange der Verdichter < 15 min läuft.
4. **Modbus-Aktor AMQ46** → Hoval-Register **1490** (FC6, RepeatRate 300 s). Hoval: Regelstrategie 3 „Konstant“ (Reg 27510).

**Folge:** Die Hoval-eigene Heizkurve ist bei euch abgeschaltet. 1490 ist die Loxone-Kurve **nach** Raumkorrektur durch den Klimacontroller. Deshalb steigt 1490 bei Kälte kaum: bei 2 °C außen wären es nach reiner Kurve (Raum 22 + 0,9 × (22 − außen)) 39,4 °C, Loxone schickt 32,8 °C.

| Außen (2-K-Klasse) | min mit 1490 > 0 | 1490 Median | reine Kurve 0,9 | Differenz |
|---|---|---|---|---|
| 2 | 270 | 32,8 | 39,4 | −6,6 |
| 6 | 249 | 31,4 | 35,9 | −4,5 |
| 8 | 1617 | 30,9 | 33,4 | −2,5 |
| 10 | 1089 | 30,2 | 31,8 | −1,6 |
| 12 | 822 | 33,7 | 30,1 | +3,6 |
| 14 | 743 | 35,0 | 28,2 | +6,8 |
| 18 | 490 | 30,2 | 24,4 | +5,8 |

**Wahrscheinlich:** Die +4…+7 K bei 12–20 °C außen (Nachmittagsläufe 14–18 Uhr, 1490 ≈ 35) kommen aus der Raumkorrektur des Klimacontrollers (Räume unter Soll nach Morgenpause). **Nicht geprüft:** ob ein Heizfenster/Zeitprogramm diese Nachmittagsläufe auslöst.

## 2. Verlauf eines Heizlaufs (sicher, 70 Läufe Okt.)
- Modulation steht vom Start bis zum Ende auf **35 %** (Minimum) – in fast jedem Lauf.
- VL steigt im Lauf stetig: +5 min ≈ 34–36 °C → Abschaltung bei **VL ≈ 1490 + 10 K** (30 → 40/41, 35 → 45, 32,9 → 40–42). RL am Ende ≈ VL − 4…5 K.
- Laufdauer Median 24 min. VL − 1490 im Mittel +5,1 K (vor 18.10.) / +5,6 K (nach 18.10., n = 8) – **kein Hinweis**, dass der Kurzlauf-Schutz (1490 = VL-Ist) die Läufe verlängert oder den VL hochtreibt; n noch zu klein.

**Bedeutung:** Die Maschine ist im Übergang zu groß für den Bedarf, fährt am Modulationsminimum und lädt Puffer/Estrich, bis der WP-Vorlauf ~10 K über dem Loxone-Wunsch liegt (sicher: 3 K Überhöhung 30684/30685; wahrscheinlich: ~7 K Abschalt-Hysterese der Hoval, nicht vom Nutzer verstellbar – Wert nicht am Register belegt). Die Überhöhung ist der einzige Teil davon, den man selbst verkleinern kann – der Vorschlag 3,0 → 1,5 K aus der Vor-Analyse bleibt richtig.

## 3. Was bringt uns das / Vorschläge (nur Vorschläge, nichts geschrieben)
1. **Loop-Frage „wer schreibt 1490“ ist erledigt** – keine Messung mehr nötig.
2. **Winter-Check (der Betreiber, Loxone Config):** Bei < 0 °C außen wird die Raumkorrektur weiter abziehen. Solange die Räume ihr Soll halten, ist das gut (niedriger VL = besserer COP). Wenn es bei Frost zu kalt wird: zuerst **Steilheit 0,9 → 1,0** am Heatmixer HC1, nicht die Hoval anfassen.
3. **Überhöhung 30684/30685 3,0 → 1,5 K** (Bedienteil): senkt Ein- und Abschaltpunkt um 1,5 K, ~3–4 % weniger Strom im Heizbetrieb. Umkehrbar.
4. Optional später: Max 40 °C am Heatmixer ist für Fußboden ok; nicht erhöhen.

Loxone-Doku: Intelligente Raumregelung/Klimacontroller und Heizungsmischer – https://www.loxone.com/dede/kb/ (Bausteine „Klimacontroller“, „Mischerregler“).