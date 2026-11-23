# Loxone-Mindestlaufzeit MinHr 40 min wird vom WP-Startverzug aufgefressen (23.10.2026)
Orchestrator 23.10.2026 11:25 · nur lesend · Vertiefung zu `ANALYSE_Heizlauf_Enden_Ursache_16-23Okt_20261023.md` (15 von 27 Heizläufen endet Loxone).
Quellen: Loxone-Projektdateien `Loxone-Umbau\UMBAU_*.Loxone` (gelesen, nicht verändert), Volllogger-Kopien `Emulation\or_ag1_2026-10-*.csv*` (16.10. 00:00 – 23.10. 09:55, 5-min-Raster).
Skripte: `Emulation\or_klimactl_20261023_1100.py`, `or_klimactl2_20261023_1110.py`, `or_klimactl3_20261023_1120.py`.

## Befund
**Sicher (Projektdatei):** Klimacontroller HC1 (`HVACController` „Klimacontroller HC1“) hat `TimePump` = **40** (= MinHr, Mindestlaufzeit). Notiz im Baustein: „08.10.2026: Mindestlaufzeit MinHr 40 min (vorher 0)“. Gleicher Wert in allen Ständen ab des Betreibers Upload 11.10. 00:34 bis 18.10. 18:03. Einschaltschwelle `OnThreshold` 30 %, Takten (MaxTp) nicht gesetzt. Ausgang `OutHeat1` geht auf Mux „Sollwert Heizen 1490“ und „Verdichterstart bei offenem Heizfenster“.
Offizielle Doku: MinHr Standard 0, „minimum runtime must be met before switching to standby“, Sot Standard 30 %, nach Abschalten 3 min Sperre — https://www.loxone.com/enen/kb/climate-controller/ (DE-Seite https://www.loxone.com/dede/kb/klima-controller/ derzeit „vorübergehend nicht verfügbar“).

**Sicher (Volllogger, 32 Anforderungsblöcke 1501 = 23):**
| Merkmal | Ergebnis |
|---|---|
| Anforderung dauert genau 40 min (±5, Raster) | **12 von 32** Blöcken (35–40 min) → MinHr läuft ab, dann fällt H |
| Verzug Anforderung → Heiz-Verdichter (18726 > 0, 1539 = 1) | 20 min: 11× · 15 min: 3× · 25 min: 1× · 5 min: 1× · 40 min: 2× · **0 min: 5×** |
| Heizlauf innerhalb eines 40-min-Blocks | bei 15–25 min Verzug nur **15–25 min**; bei 0 min Verzug volle **40 min** (16.10. 14:50, 19.10. 09:15, 22.10. 04:25, 23.10. 03:05) |
| Anforderung ohne jeden Heiz-Verdichterlauf | 9 Blöcke (meist abends 10–295 min, RL/Puffer vermutlich warm genug) |

**Wahrscheinlich:** MinHr zählt ab Loxone-Ausgang H, die WP startet aber typisch erst ~20 min nach der Anforderung. Von 40 min Mindestlaufzeit bleiben so ~20 min Verdichterlauf → genau die 15–25-min-Läufe der Klasse c-Lox (Median 25 min). Der 20-min-Verzug sitzt auf Hoval-Seite (Zuschalt-/Einschaltverzögerung für externe Anforderung oder Mindeststehzeit; iDM/Hoval-Belege in STAND.md nennen 15 min Zuschaltzeit) — **Vermutung**, welcher Parameter genau.
**Nicht ermittelbar:** ob die Live-Config = Stand 18.10. ist (keine Datei vom Miniserver gelesen); exakter Verzug < 5 min.

## Einstellvorschlag (nur Vorschlag – nichts verstellt, der Betreiber entscheidet)
1. **MinHr am Klimacontroller HC1 von 40 auf 60 min** (Parameter „Mindestlaufzeit“/TimePump). Wirkung: ~40 min Verdichterlauf statt ~20 min bei gleicher Anforderung. Rückweg: Wert zurück auf 40.
2. Sauberer, aber mehr Arbeit: Mindestlaufzeit ab **echtem Verdichterstart** statt ab Anforderung – Monoflop (https://www.loxone.com/dede/kb/monoflop/) auf steigende Flanke „Verdichter läuft im Heizen“ (1539 = 1 und Modulation > 0), 40 min, ODER-verknüpft mit H vor dem „Heizen extern“-Schreibwert.
3. Den Hoval-seitigen Verzug am Bedienteil klären (nur ablesen): welcher Parameter verzögert den Start nach externer Anforderung um ~20 min?
- **Was bringt uns das:** Bei ~20 min Anlauf mit schlechter Arbeitszahl (Anlaufphase COP 1,4–2,8) verdoppelt MinHr 60 die nutzbare Laufzeit pro Start; grob 1 Start/Tag weniger und 3–5 kWh_el/Woche (Schätzung aus der Heizlauf-Enden-Analyse). Kein Eingriff an der WP nötig, nur ein Loxone-Wert.
- **Achtung:** LoxForum 310713 berichtet unter V13 bei MinHr > 0 hin- und herfahrende Ventile; MinHr 40 läuft bei uns seit 11.10. ohne bekannten Effekt – trotzdem nach Umstellung Ventilstellungen beobachten.

## Gegenprobe für den Loop (lesend)
Nach einer Änderung: Anteil der 1501=23-Blöcke mit ≥ 35 min Verdichterlauf; Verzug-Verteilung unverändert ~20 min?