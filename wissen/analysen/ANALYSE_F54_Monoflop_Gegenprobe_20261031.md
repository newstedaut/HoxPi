# F54 Gegenprobe: Wirkt der Kurzlauf-Schutz (Monoflop 900 s) live? (OR 31.10.2026 15:54)

**Frage:** Die 14:54-Analyse (`[lokaler Pfad]`) erklärte die ~15-min-Läufe mit dem Monoflop „Kurzlauf-Schutz 15 min“ aus der Projektdatei – Miniserver-Stand war nicht zurückgelesen. Hält Loxone live 1490 ≥ 20 bis 15 min nach Verdichterstart?

**Quelle (nur gelesen):** Volllogger `/home/<user>/hoxpi_fulllog/2026-10-01 … 31.csv(.gz)` (5-min-Raster, Rohwerte ×10), Skripte
`[lokaler Pfad]` und `cc_f54zeilen_20261031_1605.py` (am Pi nur /tmp).

## Ergebnis 1: Dauer der Loxone-beendeten Heizläufe (1539 1→0 bei 1490 = 0)
| Zeitraum | n | Dauern (min, 5-min-Raster) | < 15 min |
|---|---|---|---|
| 01.–17.10. (vor Einbau) | 24 | 4 4 5 5 5 5 10 10 15 15 19 20 20 20 20 24 24 25 25 25 25 35 39 49 | 8 (33 %) |
| 18.–31.10. (nach Einbau) | 17 | 5 5 14 14 15 15 15 19 19 20 20 25 40 40 40 45 50 | 4 (24 %, davon 2× „14“ = Raster-Jitter ≈ 15) |

→ Kaum Unterschied vor/nach 18.10. (sicher für die Zählung). Kein Beleg, dass der Schutz die Verteilung verschoben hat.

## Ergebnis 2: Rohzeilen der zwei echten Kurzläufe nach 18.10.
| Zeit | 1539 | 1490 | 25611 P_el | 1525 VL | 1535 RL | 1520 | 1501 |
|---|---|---|---|---|---|---|---|
| 29.10. 21:20 | 0 | 32,2 | 0 | 31,5 | 31,5 | 35,0 | 23 |
| **29.10. 21:25** | **1** | **0** | **2,00 kW** | 34,5 | 31,5 | 0 | 0 |
| 29.10. 21:30 | 0 | 0 | 0 | 32,5 | 32,5 | 0 | 0 |
| 29.10. 10:45 | 51 | 31,8 | 0 | 37,0 | 36,0 | 34,5 | 23 |
| **29.10. 10:50** | **1** | **0** | **1,83 kW** | 40,0 | 37,0 | 0 | 0 |
| 29.10. 10:55 | 0 | 0 | 0 | 38,0 | 37,5 | 0 | 0 |

- Verdichter läuft mit 1,8–2,0 kW, 1490 steht aber schon im selben Raster auf 0 und bleibt 0 → der Lauf endet nach < 10 min. Nach der Dateilogik (`IF(I1>0;I1;IF(I3>0;MAX(I4;20);0))`) müsste 1490 hier ≥ 20 stehen. **Der Kurzlauf-Zweig hat live nicht gegriffen** (sicher für diese 2 Fälle).
- Die 15-min-Läufe 28.10. 10:30–10:45 / 14:50–15:05 zeigen während des Laufs 1490 = 29,3/28,4/29,3 = normaler Klimacontroller-Sollwert (I1 > 0), nicht HK1-VL-Ist → dort war der Schutz-Zweig gar nicht im Spiel; „genau 15 min“ ist dort Zufall/Fenster (wahrscheinlich).
- 10:50 war der Wiederanlauf nach des Betreibers Abschaltung 08:54–10:42 (Sonderfall); 21:25 ist ein normaler Abendfall.

## Deutung
- **Wahrscheinlich ist der Kurzlauf-Schutz vom 18.10. auf dem Miniserver nicht wirksam** – entweder läuft dort eine Projektdatei ohne ihn, oder die Startflanke (25611 > 0,5 kW, Wert bis 60 s alt) kommt zu spät/gar nicht. Loxone-MCP sieht den Monoflop nicht (`control_find` „Kurzlauf“ = 0 Treffer; nicht visualisiert).
- Die Aussage 14:54 „erklärt den Lauf-Median 15 min exakt“ ist damit **zurückgenommen** (war „wahrscheinlich“, jetzt widerlegt für die Kurzläufe).
- Der Hebel „Monoflop 900 → 1800 s“ bringt nichts, solange der Schutz nicht greift.

## Was bringt uns das
- Bevor der Betreiber am Monoflop dreht: in Loxone Config prüfen (Miniserver-Stand), ob die Formel „1490 inkl. Ofen-Nachlauf“ den Eingang I3 (Kurzlauf-Schutz) live hat und der Monoflop beim Start einen Impuls bekommt (Liveview). Doku: https://www.loxone.com/dede/kb/monoflop/ · https://www.loxone.com/dede/kb/formel/
- Zwilling: Loxone-Schnitte **ohne** 15-min-Mindestlauf modellieren (Lauf kann 5 min sein).
- Status F54 bleibt **teilweise** (Rest: demandHeat nachts, Miniserver-Stand des Schutzes).