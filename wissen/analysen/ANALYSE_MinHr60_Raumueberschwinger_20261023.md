# MinHr 60 statt 40 min – verträgt das Haus längere Heizläufe? (23.10.2026)
Subagent 23.10.2026 ~12:30 · **nur lesend**, nichts an Loxone/Hoval/CAN/Pi verändert.
Vertiefung zu `ANALYSE_Loxone_MinHr40_Startverzug_20261023.md` (Vorschlag MinHr 40→60) und `ANALYSE_Heizlauf_Enden_Ursache_16-23Okt_20261023.md` (28 Heizläufe).

## Quellen
| Kürzel | Quelle | Auflösung |
|---|---|---|
| [VL] | Volllogger-Kopien `Emulation\or_ag1_2026-10-16…23.csv(.gz)`, 2136 Zeilen 16.10. 00:00 – 23.10. 09:55 (Ortszeit CEST). 1510 Raum HK1 (×0,1 °C, 0,1 K Auflösung), 1539, 18726, 25611, 25612, 1501, 1520, 1513, 1529, 1535, 1490 | 5 min |
| [LXH] | Loxone `control_history` (je 20 Einträge) Badezimmer, Zimmer OG 2, Technikraum, abgerufen 23.10. ~11:55 – Zeitstempel UTC, hier in Ortszeit (+2 h) umgerechnet | Ereignis |
| [LX] | Loxone `control_state tempActual` aller Raumregler, 23.10. 11:56 (Momentwert; **keine Historie** im MCP-Speicher) | Moment |
| [ALT] | Holzofen-Analyse 22.10. (1510 läuft bis 0,8 K kälter als WZ-Fühler T_A), Raumventile-Analyse 22.10. | – |

## 0. Was es an Raumdaten gibt (und was nicht)
- Folge: Frage (1) wird **nur mit 1510** beantwortet. Für einzelne Räume ist der Überschwinger **nicht messbar**.

## 1. Raumtemperatur 1510 während und nach den Heizläufen [VL]
| # | Start | min | Q_th kWh | Ende durch | R0 °C | dT im Lauf | +30 | +60 | +90 | +120 | +180 | Störgröße |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | 16.10. 08:30 | 10 | 0,7 | Lox | 21,0 | +0,1 | +0,3 | +0,2 | +0,5 | +1,1 | +0,8 | Sonne Vormittag |
| 5 | 16.10. 13:35 | 25 | 5,1 | Lox | 21,7 | +0,3 | +0,4 | – | – | – | – | Nachmittag, AT 14 °C |
| 6 | 16.10. 14:50 | **40** | 7,2 | Lox | 22,2 | +0,1 | +0,1 | +0,2 | +0,4 | – | – | Nachmittag |
| 12 | 18.10. 07:55 | 25 | 3,8 | WP | 22,2 | 0,0 | +0,1 | +0,1 | −0,1 | 0,0 | 0,0 | |
| 13 | 18.10. 14:40 | 20 | 3,8 | Lox | 22,2 | 0,0 | +0,1 | +0,1 | +0,1 | +0,1 | 0,0 | |
| 15 | 19.10. 07:20 | 20 | 3,0 | Lox | 22,0 | −0,1 | −0,2 | −0,3 | −0,3 | – | – | |
| 16 | 19.10. 09:15 | 25 | 3,9 | WP | 21,7 | −0,1 | 0,0 | +0,1 | +0,6 | +0,5 | +0,6 | Sonne |
| 19 | 20.10. 10:25 | 25 | 3,7 | WP | 20,4 | +0,2 | +0,3 | +0,5 | +0,6 | +0,6 | +0,6 | Sonne |
| 21 | 21.10. 17:30 | 25 | 4,0 | WP | 21,4 | +0,1 | 0,0 | −0,1 | −0,1 | −0,1 | −0,1 | Abend |
| **22** | 22.10. 04:25 | **40** | 5,8 | Lox | 20,4 | 0,0 | +0,1 | +0,2 | +0,3 | +0,2 | – | **Nacht, sauber** |
| 24 | 22.10. 08:20 | 15 | 2,0 | Lox | 20,7 | 0,0 | 0,0 | 0,0 | +0,2 | +0,3 | +0,4 | Vormittag |
| **25** | 23.10. 03:05 | **40** | 5,7 | Lox | 20,6 | −0,1 | −0,1 | −0,1 | −0,2 | – | – | **Nacht, sauber, AT 2,7 °C** |
| 26 | 23.10. 05:40 | **105** | 13,8 | WW | 20,4 | **+0,4** | +0,6 | – | – | – | – | längster Lauf, AT 1,9 °C, ab 07:30 Sonne |
(übrige Läufe: Folgelauf < 30 min danach, keine Aussage; vollständige Liste im Skript-Output `_1215.py`.)


**Sicher (1510):**
- Kein Heizlauf hat 1510 **im Lauf** um mehr als **+0,4 K** angehoben (der 105-min-Lauf 23.10.); typische 20–40-min-Läufe: **−0,1 … +0,3 K**.
- In den 2 h nach Laufende ohne Sonne/Ofen: **−0,3 … +0,3 K**. Alle größeren Anstiege (+0,5 … +3,2 K) fallen in Sonnenstunden oder auf Ofenabende.
- Die **sauberen Nachtläufe mit 40 min** (#22, #25) zeigen den Effekt: statt −0,25 … −0,35 K Abkühlung in 2 h bleibt 1510 bei +0,2 bzw. −0,2 K → Wirkung eines 40-min-Laufs (5,7–5,8 kWh_th) ≈ **+0,15 … +0,45 K**, verteilt über **1,5–2 h** (FBH-Nachlauf: Maximum #22 erst 90 min nach Laufende).
- Zwischen 40-min-Läufen (5,7–7,2 kWh) und 20–25-min-Läufen (3–4 kWh) ist bei 1510 (0,1 K Auflösung) **kein klarer Unterschied im Überschwinger** sichtbar.
**Wahrscheinlich:** Faustwert **0,03–0,08 K pro kWh_th** am 1510, Wirkung verzögert 1–2 h. Plausibel: Estrich UG ~100 m² × 6–7 cm ≈ 3,5–4 kWh/K, dazu Puffer 400 l ≈ 0,46 kWh/K [⚠ Korr. 23.10.2026: Puffer = EnerVal 300, 282,4 l — zu hoch angesetzt]; der Boden gibt die Wärme über Stunden ab.
**Nicht ermittelbar:** Überschwinger je Raum (WZ, Bad, Büro …) – keine Historie.

## 2. Abschätzung MinHr 60 – Energie und Überschwinger
**Wichtige Bremse (sicher aus [VL] und Heizlauf-Enden-Analyse):** Die WP schaltet selbst bei **RL 1535 ≈ Soll 1529 + 2,5 K** ab. MinHr 60 verlängert einen Lauf also nur bis zu diesem Punkt, nicht blind um 20 min.
Betroffen sind die Loxone-beendeten Läufe, deren Anforderungsblock 1501 = 23 genau 35–45 min lang war (MinHr abgelaufen): **11 Läufe in 7,4 Tagen (~1,5/Tag)**.
| # | Block | Verzug | RL−Soll am Ende | RL-Anstieg K/5 min | Zeit bis Soll+2,5 (linear) | Verlängerung bei MinHr 60 (Schätzung) |
|---|---|---|---|---|---|---|
| 5 | 16.10. 13:20–13:55 | 15 | −4,0 | +1,50 | 22 | 20 min |
| 6 | 16.10. 14:50–15:25 | 0 | +2,5 | +0,83 | 0 | 0 (WP war fertig) |
| 9 | 17.10. 08:30–09:00 | 15 | +1,0 | +1,17 | 6 | 6 |
| 11 | 17.10. 17:45–18:20 | 15 | −1,0 | +1,17 | 15 | 15 |
| 13 | 18.10. 14:20–14:55 | 20 | −4,0 | +1,33 | 24 | 20 |
| 14 | 18.10. 18:05–18:35 | 20 | +0,5 | +1,50 | 7 | 7 |
| 15 | 19.10. 07:00–07:35 | 20 | −2,0 | +1,17 | 19 | 19 |
| 22 | 22.10. 04:25–05:00 | 0 | +1,5 | +0,67 | 8 | 8 |
| 23 | 22.10. 07:05–07:45 | 20 | +1,0 | +0,83 | 9 | 9 |
| 24 | 22.10. 07:55–08:30 | 25 | −1,5 | +0,75 | 27 | 20 |
| 25 | 23.10. 03:05–03:40 | 0 | −1,0 | +0,67 | 26 | 20 |
Summe 144 min/Woche, **Ø ~13 min je betroffenem Lauf** (0–20 min).

- **Zusätzliche Energie je Lauf (Schätzung):** 13 min × 8–9 kW (mittlere Q_th dieser Läufe 7,4–12 kW) ≈ **~1,8 kWh_th, Spanne 0–2,9 kWh_th** ≈ 0,4–0,7 kWh_el bei AZ ~4–4,5. Das ist **keine Mehrverbrauch pro Tag** – die Tages-Heizlast bleibt gleich, die Wärme kommt nur in weniger, längeren Portionen. Leichter Mehrverlust durch etwas höheres Temperaturniveau: < 1 % (Vermutung).
- **Erwarteter Überschwinger (wahrscheinlich):** 1,8 kWh × 0,03–0,08 K/kWh ≈ **+0,05 … +0,15 K** am 1510, schlimmster Fall (2,9 kWh) **+0,1 … +0,25 K**, Maximum 1–2 h nach Laufende. Gegenprobe Physik: 2,9 kWh in ~4 kWh/K Estrich → Estrich +0,7 K → ~+0,7 kW mehr Abgabe über einige Stunden bei 3–5 kW Heizlast → Raum steigt um wenige Zehntel. Passt.
- **Risiko Komfort + 0,5 K (WZ 21,5 → 22,0):** **gering**. Gründe: (a) Überschwinger ≤ 0,25 K selbst im ungünstigsten Fall; (b) die Raumregler (Intelligente Raumregelung, PI) schließen das Ventil eines Raums über Soll – Zusatzwärme geht vor allem in Räume unter Soll (heute Bad 22,6 bei 23,5; Zimmer OG 2 20,7) (wahrscheinlich, Ventilstellung nicht messbar); (c) WZ/Büro liegen schon **ohne** Heizlauf bei 21,8–22,1 °C [LX] – Überschreitungen kommen dort aus Sonne/Ofen, nicht aus dem Heizlauf (sicher aus Tabelle 1: alle Anstiege > +0,5 K in Sonnen-/Ofenzeiten).

## 3. Wie viele Starts fallen weg? (Abschätzung, nicht gemessen)
Basis: 28 Heiz-Starts in 7,4 Tagen = **3,8/Tag** (zusätzlich ~3,6 WW-Starts/Tag, unberührt).
Ein Start fällt sicher weg, wenn der nächste Anforderungsblock **≤ 20 min** nach dem Ende eines MinHr-begrenzten Blocks kam – mit 60 min wäre die Anforderung durchgehend gestanden:
| Block-Ende | nächster Block | Lücke | nächster Heizstart |
|---|---|---|---|
| 16.10. 13:05 | 13:20 | 15 min | #5 13:35 → **entfällt** |
| 17.10. 09:00 | 09:20 | 20 min | #10 10:00 → **entfällt** |
| 22.10. 07:45 | 07:55 | 10 min | #24 08:20 → **entfällt** |
| 16.10. 13:55 | 14:50 | 55 min | #6 → **vielleicht** (Mehrwärme ~2 kWh verschiebt die nächste Anforderung um grob 25–40 min) |
| 19.10. 07:35 | 09:15 | 100 min | #16 → wahrscheinlich nicht |
⇒ **3 sicher + 0–1 möglich in 7,4 Tagen ≈ 0,4–0,6 Heiz-Starts/Tag weniger** (~10–15 % der Heiz-Starts). Die frühere Schätzung „~1 Start/Tag“ ist **zu optimistisch**.
Vorbehalt: Der Hoval-seitige Startverzug (~20 min) kann bei durchgehender Anforderung trotzdem eine Pause erzwingen, wenn die WP selbst bei Soll + 2,5 K abgeschaltet hat (Mindeststehzeit) – dann bleibt der Start, nur später. Kälter werdende Tage (mehr lange Blöcke) senken den Effekt weiter, weil dort MinHr seltener begrenzt.

## 4. Sind die Stellantriebe während der Läufe offen?
- **Nicht ermittelbar:** die **Stellung** der einzelnen Tree-Stellantriebe (keine Controls, keine Historie). „Aktiviert“ heißt freigegeben; ein Raum über Soll steht trotzdem auf 0 (wahrscheinlich, PI-Regler).

## 5. Zusammenfassung nach Sicherheit
- **Wahrscheinlich:** MinHr 60 verlängert diese Läufe im Mittel um ~13 min, also um ~1,8 kWh_th (0–2,9). Der Raum schwingt dabei um +0,05 … +0,25 K über, mit 1–2 h Verzögerung. Das Risiko, Komfort + 0,5 K zu überschreiten, ist gering. Es fallen 0,4–0,6 Heiz-Starts pro Tag weg.
- **Vermutung:** Die Zusatzwärme landet vor allem im Bad und in Zimmer OG 2, also in den Räumen unter Soll. Der Mehrverlust liegt unter 1 %. An Ofenabenden ist der Effekt vernachlässigbar.
- **Nicht ermittelbar:** der Raumverlauf je Raum, die Stellung der Stellantriebe und warum die Loxone-Heizphasen am 22.10. nachmittags keine Hoval-Anforderung ausgelöst haben.

## 6. Empfehlung
**MinHr 60 einstellen (Klimacontroller HC1, Parameter Mindestlaufzeit/TimePump 40 → 60), eine Woche testen.** Eine Zwischenstufe 50 bringt nichts: Bei typisch 20 min Startverzug blieben nur ~30 min Lauf, und die Läufe mit 0 min Verzug würden ohnehin schon vorher an RL + 2,5 K enden. Die Daten zeigen bei 60 kein Überheizrisiko, das eine Zwischenstufe rechtfertigen würde. Doku: https://www.loxone.com/enen/kb/climate-controller/ (Klimacontroller), https://www.loxone.com/dede/kb/intelligente-raumregelung/
**Abbruchkriterien für den Test (lesend prüfbar):**
1. 1510 steigt nach einem Nachtlauf (ohne Sonne, ohne Ofen) innerhalb von 2 h um mehr als +0,5 K.
2. WZ- oder Büro-`tempActual` liegt morgens zwischen 05 und 08 Uhr über 22,0 °C, ohne dass am Vorabend der Ofen lief.
3. Ventile fahren hin und her (LoxForum-Hinweis zu MinHr > 0 unter V13).
**Gegenprobe:** Anteil der 1501 = 23-Blöcke mit ≥ 35 min Verdichterlauf (bisher 4 von 32), Heiz-Starts pro Tag (bisher 3,8) und Lücken ≤ 20 min zwischen Blöcken (bisher 3 pro Woche, sollen auf 0 fallen).
**Rückweg:** den Wert am selben Baustein zurück auf **40**. Es ist kein Eingriff an der WP nötig.

## Was bringt uns das
- Etwa **0,4–0,6 Heiz-Starts pro Tag weniger**, also ~3–4 pro Woche. Die Läufe dauern im Mittel ~13 min länger (25 → ~38 min), weil die Läufe mit 20 min Verzug nicht mehr nach ~20 min abgewürgt werden.
- Strom: Pro eingespartem Start entfällt grob eine Anlaufphase mit ~0,3–0,4 kWh_el schlechter Arbeitszahl. Das sind **~1–1,5 kWh_el pro Woche**, also weniger als die früher genannten 3–5 kWh_el (Schätzung). Der Hauptnutzen ist **Verschleiß**, also weniger Takte, und nicht die Stromrechnung.
- Komfort: unverändert. Der erwartete Überschwinger von ≤ 0,25 K liegt innerhalb der Toleranz von 0,5 K. Bad und Zimmer OG 2 bekommen eher etwas mehr Wärme.

## Prüfbare Stichprobe