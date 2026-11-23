# ANALYSE F60 – Legionellen-Pflichtlauf 01.11.2026: Kosten, Aufteilung, Variante WP-Vorladung 57 °C

Erstellt 01.11.2026 ~17:30 (Claude, Analyse-Agent, nur lesend). Keine Schreibzugriffe auf Anlage, Loxone oder Pi. Baut auf `[lokaler Pfad]` auf (Ablauf, Legionellen-Logik, Zählerreset dort, hier nicht wiederholt).

## Frage
1. Wie viel kWh_el kostete der Pflichtlauf (Stab) und wie viel davon war Speicheraufheizung (C × ΔT) bzw. Verlust/Zapfung?
2. Variante: WP lädt vorher mit Soll 57 °C, Stab nur für den Rest bis zum Nachweis (≥ 60 °C). kWh_el je Woche für Ist und Variante.
3. Lief der Stab aus dem Netz oder teils aus PV?

## Datenquellen
| Größe | Quelle |
|---|---|
| Heizstab-Energie | Loxone Meter „Heizstab Trinkwasser", UUID `<UUID>`, `control_statistics` Gruppe 2 diff/hour 09–16Z; `control_state` totalDay/totalWeek (ts 2026-11-01T15:58:00Z) |
| Netzbezug/Einspeisung | Loxone Meter „Hauptstromzähler", UUID `<UUID>`, Gruppe 2 (total/totalNeg) diff/hour |
| PV-Erzeugung | Loxone Meter „SÜD Hang 3,8kWp" `<UUID>`, „SÜD Balkon 2,43kWp" `<UUID>`, „OST Fassade 1,21kWp" `<UUID>`, „WEST Garage 1,62kWp" `<UUID>`, „Victron_Solar_Charger_288" `<UUID>` (je Gruppe 2 diff/hour) |
| Batterie | Loxone Meter „LiFePO4 14,34kWh" `<UUID>`, Gruppe 2 total/totalNeg |
| Speichertemperaturen, WP-WW | Volllogger auf dem Pi `/home/<user>/hoxpi_fulllog/2026-11-01.csv` (5 min, MEZ): 1500 WW oben (×10), 27483 SF2 unten (×10), 1499 WW-Soll aktiv (×10), 1504 WW-Ladung WP, 25611 P_el (×100), 27489 Wärmemenge WW (kWh, 1-kWh-Auflösung), 1477 Außen (×10). Gelesen per `py -3 [lokaler Pfad]` (awk, nur lesend) |
| Speicherkapazität | C = 0,47 ± 0,04 kWh/K (`[lokaler Pfad]`, F1) |
| Arbeitszahl WW nach Ladesoll | `[lokaler Pfad]` (MD-10, von Claude abgenommen 29.10.): Klasse 52 °C AZ 2,86 (Zähler gesamt), Klasse 57 °C Dauer 3,36 (wärmerer Außenbereich, Confounding), Grenz-AZ im Band 52→56 °C ≈ 2,85 [dort Vermutung]; Endtemperatur oben bei Soll 57 °C ≈ 55,8 °C (WP-Vorlaufgrenze 62 °C) |

## Methode
- Speicher-Mittel T_m = (1500 + 27483)/2; Speicherinhalt ΔQ = C × ΔT_m. Stab-Strom = Wärme 1:1 (ohmsch) [sicher].
- Zeitbasis: Loxone-Stundenbuckets UTC (11Z = 12:00–13:00 MEZ), Volllogger MEZ.
- Stab-Energie Phase (b): 13:40–14:00 anteilig aus 12Z (2,50 × 20/60 = 0,83) + 13Z 2,50 + 14Z 2,06 = 5,39 kWh.
- Varianten als Modellrechnung mit gemessenen Kennwerten (Wirkungsgrad Stab-Phase, C, AZ aus MD-10).

## Ergebnis 1 – Was kostete der Lauf, wohin ging die Energie?

Heizstab je Stunde (Loxone, diff/hour): 11Z 2,500 · 12Z 2,500 · 13Z 2,500 · 14Z 2,064 · 15Z 0 → **9,56 kWh_el** (= totalDay/totalWeek 9,5638) [sicher]. Leistung konstant ~2,5 kW, Stab EIN ~12:00, AUS 15:54 MEZ (F57) [sicher].
Hinweis: WW-Soll 1499 lag während der WP-Ladung bei **52,0 °C** (Rohwert 520 ab 13:05), nicht 57 °C [sicher, Volllogger].

| Phase (MEZ) | T_m Start → Ende (°C) | ΔQ Speicher = C×ΔT (kWh_th) | Zufuhr Stab (kWh_el) | Zufuhr WP-WW 27489 (kWh_th) | Rest = Zapfung + Verlust (kWh) | Einstufung |
|---|---|---|---|---|---|---|
| (b) 13:40–15:55 nur Stab | 52,00 → 61,35 (+9,35 K) | **4,39 ± 0,37** | **5,39** | 0 | **1,0 ± 0,4 (≈ 19 %)** | [sicher] |
| Summe 12:00–15:55 | 46,65 → 61,35 (+14,7 K) | 6,91 ± 0,59 | 9,56 | 4 ± 1 | 6,7 ± 1,2 | [sicher] |

Aufteilung der 9,56 kWh Stab-Strom:
- Phase (b): 4,39 kWh in den Speicher (Hub 52 → 61,35 °C), 1,0 kWh Verlust (Ruheverlust bei ~57 °C mittel ≈ 0,16 kW × 2,25 h ≈ 0,4 kWh, Rest ~0,6 kWh Zirkulation/Kleinzapfung) [sicher für Summe, Vermutung für Aufteilung des Rests].
- Phase (a): 4,17 kWh liefen parallel zu einer Zapfung und zur normalen WP-Ladung auf 52 °C. Nur ~1,3 kWh davon blieben rechnerisch im Speicher (anteilig 2,51/8,17), ~2,9 kWh deckten Zapfung/Verlust [Vermutung, proportionale Zuordnung]. Diese 4,17 kWh sind **normale WW-Deckung mit COP 1** statt mit der WP (AZ 2,86 → 1,46 kWh_el): **~2,7 kWh_el Mehrstrom** nur durch die Reihenfolge [wahrscheinlich].
- Gesamt: ~5,7 kWh (60 %) Speicheraufheizung, ~3,9 kWh (40 %) Zapfung + Verlust [wahrscheinlich].

Netto-Mehrkosten gegenüber normalem Betrieb (52 °C): Die 4,39 kWh_th über 52 °C werden danach gezapft und ersetzen WP-Wärme; abzüglich Mehr-Ruheverlust bei höherem Niveau (~0,5 kWh_th, Vermutung) spart das ~3,9/2,86 ≈ 1,4 kWh_el WP-Strom. Netto Ist ≈ (5,39 − 1,36) + 2,71 ≈ **6,7 kWh_el** [wahrscheinlich].

## Ergebnis 2 – Varianten je Woche (1 Pflichtlauf/Woche)

Annahmen: Ziel wie heute T_m ≈ 61,35 °C (Nachweis = MIN(1-Wire oben, 1500) ≥ 60 °C für 30 min); Ausgangslage nach normaler WP-Ladung T_m = 52 °C; Stab-Wirkungsgrad wie Phase (b) (≈ 0,45 kW Verlust während des Laufs); C = 0,47 ± 0,04.
WP mit Soll 57 °C erreicht oben ≈ 55,8 °C (MD-10, V44); angesetzt T_m 55,5 ± 0,5 °C. Grenz-AZ im Band 52 → 55,5 °C: **2,5 (2,3–2,85)** – Quelle MD-10 (2,85 bei ~10 °C außen, dort Vermutung), für Winter/~5 °C außen abgemindert [Vermutung].

| Variante | Stab kWh_el | WP-Mehrstrom kWh_el | Brutto kWh_el/Woche | Netto-Mehr ggü. 52 °C-Betrieb kWh_el/Woche | Quelle / Einstufung |
|---|---|---|---|---|---|
| **Ist 01.11.** (Stab ab 12:00, parallel zu WP-52-Ladung) | 9,56 | 0 (WP-Ladung 4 kWh_th ≈ 1,4 kWh_el ist Normalbetrieb) | **9,56** | **≈ 6,7** | Loxone-Zähler [sicher]; Netto [wahrscheinlich] |
| A' Stab erst nach WP-52-Ladung (nur Reihenfolge) | 5,4 | 0 | **5,4** | ≈ 4,0 | Phase (b) gemessen [sicher]; Netto [wahrscheinlich] |
| **B** WP-Ladung Soll 57 °C, dann Stab 55,5 → 61,35 | 2,75 th + ~0,6 Verlust = **3,35 (2,9–3,8)** | 1,65 kWh_th / 2,5 = **0,66 (0,58–0,72)** | **4,0 (3,5–4,5)** | **≈ 2,6** | Modell aus C, Phase (b), MD-10 [wahrscheinlich] |

- Einsparung B gegenüber Ist: **≈ 5,5 kWh_el/Woche brutto, ≈ 4 kWh_el netto** [wahrscheinlich]; davon ~2,7 kWh allein durch die Reihenfolge (A'), ~1,4 kWh durch die WP-Vorladung auf 57 °C [wahrscheinlich].
- Hochgerechnet auf ~26 Winterwochen ohne PV-Legionellen-Tag: Ist ≈ 250 kWh_el, B ≈ 105 kWh_el [Vermutung: gleiche Startbedingungen jede Woche angenommen].
- Unsicherheit C ±8,5 % wirkt gleichsinnig auf alle Varianten; die Reihenfolge der Varianten bleibt [sicher innerhalb des Modells].

## Ergebnis 3 – Netz oder PV?

| Stunde (UTC / MEZ) | Netzbezug kWh | Einspeisung kWh | PV gesamt kWh (4 Strings + Victron) | Batterie total / totalNeg kWh | Stab kWh |
|---|---|---|---|---|---|
| 11Z / 12–13 | 4,97 | 0,00 | 0,64 | 0,29 / 0,59 | 2,50 |
| 12Z / 13–14 | 6,01 | 0,00 | 0,81 | 0,89 / 0,65 | 2,50 |
| 13Z / 14–15 | 5,56 | 0,00 | 0,48 | 0,31 / 0,52 | 2,50 |
| 14Z / 15–16 | 3,67 | 0,01 | 0,16 | 1,72 / 0,11 | 2,06 |
| Summe | **20,21** | 0,01 | **2,09** | 3,21 / 1,87 | 9,56 |

- Keine Einspeisung, PV nur 2,09 kWh in 4 h → kein PV-Überschuss [sicher].
- Selbst wenn alle PV dem Stab zugerechnet wird: **≥ 78 % Netz**; bei anteiliger Zuordnung zum Hausverbrauch ≈ 90 % Netz [sicher für die Untergrenze, Vermutung für die anteilige Zahl].
- Batterie: Richtung von total/totalNeg nicht geprüft; ob Batterieentladung (früher geladene PV) den Stab mitversorgte, ist **nicht ermittelbar** aus diesen Daten.
- Fazit: Stab lief **im Wesentlichen aus dem Netz** [sicher].

## Stichprobe (nachprüfbar)
1. Volllogger `/home/<user>/hoxpi_fulllog/2026-11-01.csv`, Zeile `2026-11-01 13:40:02`: 1500 = **524**, 27483 = **516**, 1499 = 520, 1504 = 0, 25611 = 0, 27489 = 40194 → T_m 52,0 °C, WP-WW-Ladung beendet.
2. Volllogger gleiche Datei, Zeile `2026-11-01 15:55:02`: 1500 = **616**, 27483 = **611**, 1504 = 0, 25611 = 173 (Heiztakt), 27489 = 40194 → T_m 61,35 °C; ΔT 9,35 K × 0,47 = 4,39 kWh_th.
3. Loxone „Heizstab Trinkwasser" `<UUID>`, diff/hour Gruppe 2, Bucket `2026-11-01T12:00:00Z` = **2,5000 kWh**; totalDay = 9,5638 kWh (ts 2026-11-01T15:58:00Z).

## Vorschlag (nur Vorschlag, keine Umsetzung – Entscheidung der Betreiber)
1. **Reihenfolge**: Heizstab im Pflichtfenster erst freigeben, wenn keine WP-WW-Ladung läuft/ansteht und T_m bzw. 1500 ≥ Endwert der WP-Ladung (z. B. Stab-Freigabe erst ab 1500 ≥ 55 °C oder nach Ende 1504 = 1). Spart ≈ 2,7 kWh_el/Woche ohne Hygieneverlust [wahrscheinlich].
2. **WP-Vorladung 57 °C**: Am Pflichttag zum Fensterbeginn das vorhandene 57-°C-Soll (Smart-Grid-Pfad/1497) als WW-Ladung anstoßen, danach Stab nur für den Rest. Weitere ≈ 1,4 kWh_el/Woche [wahrscheinlich]. Rückweg: Daytimer/Logik wie Stand 25.10. (`[lokaler Pfad]`). Vor Umbau Backup und Skill `loxone-xml-umbau`.
4. Netto-Kostenblick: Die Wärme über 52 °C ist nicht verloren, sie wird gezapft; echte Mehrkosten sind die Netto-Spalte, nicht die Stab-kWh.

## Offen
- Grenz-AZ der WP im Band 52 → 56 °C bei Winter-Außentemperatur nicht gemessen (nur MD-10-Vermutung 2,85 bei ~10 °C). Messbar an der nächsten 57-°C-Dauerladung ohne Zapfung (25611-Integral gegen ΔT_m × C) [offen].
- Tatsächliche Endtemperatur bei WP-Soll 57 °C im Winter (oben ~55,8 °C laut MD-10, Oktober-Max 58,9 °C) – bestimmt den Stab-Rest direkt.
- Batterie-Richtung (total/totalNeg beim Meter „LiFePO4 14,34kWh") nicht verifiziert → PV-Anteil über Batterie nicht ermittelbar.
- Phase (a): Trennung Zapfung vs. Verlust nicht möglich (kein Durchflussmesser); proportionale Zuordnung ist Vermutung.
- Reg 27489 hat 1-kWh-Auflösung (±1 kWh in Phase a).
- Ob der Pflichtlauf wirklich jede Woche fällt (Zähler ≥ 6,5 d, außer PV-Legionellen-Tag), erst ab 08.11. belegbar.