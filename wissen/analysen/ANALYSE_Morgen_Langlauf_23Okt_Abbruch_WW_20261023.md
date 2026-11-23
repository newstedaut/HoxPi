# Morgen-Langlauf 23.10.2026 – 105 min am Modulationsboden, von WW-Ladung abgebrochen
Orchestrator 23.10.2026 09:05 · nur lesend · Skripte `Emulation\or_langlauf_20261023_0900.py` (X26 Obj 0x20, 5-min-Profil + Status-Segmente) und `HoxPi-Doku\or_langlauf_20261023.sh` (Volllogger 1477/1490/[Nummer]); zusätzlich `or_az_20261022_1710.py` auf `rs485_2026-10-23.log`.

## Messung (sicher)
| Segment | Zeit | min | kWh_th | kWh_el | AZ | RL Start→Ende | Bemerkung |
|---|---|---|---|---|---|---|---|
| Heizen | 05:37:40–07:22:32 | 105 | 13,86 | 3,31 | **4,19** | 31,0 → 37,0 | ab 06:10 konstant Mod 35 %, 8,0 kW, 1,79–1,89 kW el |
| WW | 07:22:33–07:45:12 | 23 | 2,93 | 1,18 | **2,48** | 37,0 → 50,5 | direkt aus dem Heizlauf umgeschaltet, Mod 53 % |
| Pause | 07:45–08:07 | 22 | – | – | – | | > 15 min Mindeststehzeit |
| Heizen | 08:07:28–08:53:13 | 46 | 5,69 | 1,43 | **3,98** | 32,5 → 38,0 | Ende bei 1535 = 37,5 °C, 1529 = 35,0 °C |

Außen (1477) 1,7–2,4 °C, HK-Soll 1490 = 33,0 → 32,1 °C, WEZ-VL-Soll 1529 = 36,0 (Heizen) → 35,0 ab 08:25, 56,0 während WW. Raum 1510: 20,4 → 21,0 °C (05:30–08:00), danach flach.
Anlauf je Start ~10 min mit COP 1,4–2,8 (05:35–05:45, 08:05–08:15): kostet je Start grob 0,3–0,4 kWh el bei nur ~1,5 kWh th.

## Bewertung
- **Sicher:** Am Modulationsboden steigt RL nur ~0,1 K je 5 min → bei +2 °C laufen Heizläufe 1,5–2 h. Das ist kein Takten; die WP läuft bei 8,0 kW / 1,8 kW / COP 4,3 genau auf dem Datenblatt-Minimum A2/W35 (7,4 kW / 1,8 kW / COP 4,4, siehe `IDM-Doku\Recherche_laufend\FUND_C17_Leistung_Modulation_Ueberdimensionierung_20261023.md`).
- **Sicher:** Der lange Lauf endete nicht am Heizbedarf, sondern durch die WW-Anforderung 07:22 (WW war nach der 04:30-Ladung von 51,7 auf ~47 °C gefallen, Soll 52). Nach 22 min Pause musste die Heizung neu starten → ein zusätzlicher Start inkl. 10 min schlechtem Anlauf.
- **Wahrscheinlich:** Abschaltkriterium Heizen = RL 1535 ≥ Soll 1529 + 2,5 K (08:53: 37,5 vs 35,0). Lauf 1 hätte ohne WW noch ~15–20 min bis dahin gebraucht (RL 37,0 um 07:20, +0,1 K/5 min).
- **Vermutung:** Mindestmodulation 35 % ist ein Inbetriebnahme-Parameter (Datenblatt: 40 % Pflicht erst bei > 12 m Kältemittelleitung; Forum: 34-050 „Mindestleistung“).

## Was bringt uns das / Vorschlag (der Betreiber entscheidet, nichts verstellt)
1. **Langläufe sind bei +2 °C schon da** – der Hebel gegen Starts ist nicht die Heizkurve, sondern WW-Ladungen nicht mitten in einen Heizlauf fallen zu lassen.
3. Schaltdifferenz Heizen (Parameter 33-053/33-054 laut Forum, nur ablesen) notieren – größere Differenz = längere Pausen, aber am Modulationsboden schon ~2 h Lauf.
**Loop (lesend):** je Tag zählen, wie viele Heizläufe durch WW-Umschaltung (Status 1→4 ohne Pause) enden statt durch RL ≥ Soll+2,5; Hypothese „+2,5 K“ an 3 weiteren Heizlauf-Enden prüfen.