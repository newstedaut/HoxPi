# ANALYSE: WZ-Override reason 6 – Zeitbasis, Startzeitoptimierung und Kühlmodus-Falle 22./23.10.2026
Orchestrator-Lauf 23.10.2026 06:54 (MEHR Stufe 1, Eigenarbeit). Nur lesend: Loxone-MCP (`control_state`, `control_history` IRR „Wohnzimmer“ <UUID>), Volllogger `~/hoxpi_fulllog/2026-10-22.csv`/`2026-10-23.csv` (Skripte `HoxPi-Doku\or_wzprep_20261023.sh`, `or_wzprep_20261023b.sh`).
Folgt auf `ANALYSE_Raumknick_1510_Nacht_23Okt_20261023.md` (Lauf 05:55) und korrigiert dort Punkt „Knickbeginn = WZ-Override 01:00:20“.

## 1. Zeitbasis – sicher
- Loxone-Aktivitätslog (MCP liefert UTC, `Z`) und Volllogger (Pi-Zeit CEST, `date` 06:55:05 CEST) passen nur mit **UTC+2** zusammen:
  | Loxone-Log (UTC) | = lokal | Volllogger (lokal) |
  |---|---|---|
  | 01:00:23Z „Vorbereitung Heizphase Komfort gestartet“, „wird zum Heizen verwendet“ | 03:00:23 | Anforderung 03:00:52, 1490 = 332 ab 03:10 (Lauf 05:55: Verdichter 03:01:51) |
  | 01:43:33Z „wird nicht mehr verwendet“ | 03:43:33 | 1490 03:40:01 = 332, 03:45:02 = 0; Verdichter aus 03:40:52 |
  | 03:00:30Z „wird zum Heizen verwendet“ | 05:00:30 | 1490 05:00:01 = 0, 05:05:01 = 332 |
- `overrideEntries.start` 561949220 = 2009-01-01 + 6504 d + 3620 s = **23.10. 01:00:20 UTC = 03:00:20 lokal** (gleiche Sekunde wie das Log). `end` 561963560 = 04:59:20 UTC = **06:59:20 lokal**.
- **Korrektur zu Lauf 05:55:** Der Override beginnt um 03:00 lokal, nicht 01:00. Er erklärt den Heizstart um 03:00, **nicht** den Abfall von 1510 zwischen 01:00 und 03:00. Die Ursache des Knicks ist damit wieder offen.

## 2. Was reason 6 hier ist – wahrscheinlich
- Gleichzeitig `prepareState` = 1 und Logtext „Vorbereitung der Heizphase für Temperatur ‚Komfort-Temperatur‘ gestartet / Setze Zieltemperatur auf den Wert des nächsten Schaltuhreintrags“, Ende 06:59 = Komfortbeginn 07:00.
  → reason 6 = **Startzeitoptimierung/Vorheizen** des IRR V2 (wahrscheinlich; Enum nicht an Loxone-Doku geprüft, loxone.com seit 18.10. offline). Vorlauf ≈ 4 h.
- Am Vortag gleiches Muster: 22.10. 02:20:57Z (= 04:20 lokal) Vorbereitung Komfort.
- **Was bringt uns das:** Der „Nacht-Heizstart 03:00“ ist gewollte Vorheizung, kein Fehler. Der Optimierer startet 4 h vor 07:00 – bei FBH sinnvoll, erzeugt aber zwei getrennte Läufe (03:01–03:41 und ab 05:05) statt eines langen. Ob ein durchgehender Lauf effizienter wäre, ist eine Vermutung (Daten fehlen).

## 3. Kühlmodus-Falle hat gestern Abend die Heizung blockiert – sicher (Log), Wirkung wahrscheinlich
- 22.10. **13:56:52Z = 15:56 lokal**: „Zwischen Heizen und Kühlen umgeschaltet – Kühlen aktiviert“, Vorbereitung Kühlphase Eco.
- 22:30 lokal Ziel 22,5 °C (= `comfortTemperatureCool`), 23.10. 01:35 lokal „Komfort-Timer beendet → 23,5 °C“ (Kühl-Eco).
- Erst 03:00 lokal wieder „zum Heizen verwendet“. Der WZ-Regler war also **ca. 11 h im Kühlmodus** – genau das Fenster „seit 22.10. 18:59 kein Verdichterlauf, HK1 fordert nicht an“ (Lauf 00:53). Die Erklärung „Haus braucht nichts“ stimmt damit nur teilweise: das WZ *durfte* nicht heizen (WZ 21,3 °C < Heiz-Komfort 21,5 °C).
- Das ist dieselbe Falle wie in `ANALYSE_Kuehlmodus_WZ_Oktober_20261022.md` (Umschaltung über „Abweichung“), jetzt mit zweitem belegtem Ereignis.
- **Folge für die Heizlast-Rechnung** (`ANALYSE_Auskuehlung_Heizlast_20261023.md`): Die 8-h-Stillstandsnacht war nicht „bedarfsfrei“, sondern **regelungsbedingt** → als Auskühlmessung weiter brauchbar, aber nicht als Beleg, dass das Haus bei 3–6 °C keine Wärme braucht.
- **Was bringt uns das:** Im Winter kann jede Nachmittags-Sonne/Ofenwärme den WZ-Regler für den Abend in den Kühlmodus kippen → keine Heizung bis zur nächsten Vorheizphase. Abhilfe bleibt des Betreibers Entscheidung: IRR-Betriebsart fest „nur Heizen“ (Mode 1) während der Heizsaison.

## 4. Stand jetzt (06:54 lokal)
- WZ: `tempActual` 21,3, `tempTarget` 21,5, `activeMode`/`currentMode` 1, Toleranz 0,5, `useOutdoor` 0 (Außentemperatur −1000 = nicht verbunden).
- Volllogger 1510 = 20,5–20,6 °C seit 03:00 flach; Außen 1477 von 4,7 (21:00) auf 1,7 °C (06:10).

## 5. Offen / nicht ermittelbar
- Ursache 1510-Abfall 01:00–03:00 (−0,8 K) – Override scheidet aus (sicher). Mögliche Quellen (Vermutung): Loxone schreibt 1510 als Mittel/anderen Raum; Außentemperatur fiel in dem Fenster 3,8 → 2,8 °C. **Loop (lesend):** 1510 und WZ `tempActual` nächste Nacht im 5-min-Raster nebeneinander.
- reason-6-Enum an der Loxone-Doku bestätigen, sobald loxone.com wieder erreichbar ist.
- **der Betreiber:** In Loxone Config IRR Wohnzimmer → Betriebsart prüfen (Auto Heizen/Kühlen vs. nur Heizen); wer 1510 schreibt.