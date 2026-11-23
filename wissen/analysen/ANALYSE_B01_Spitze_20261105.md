# ANALYSE B01: 25611 = 5,66 kW am 05.11.2026 06:50 — Heizstab oder Verdichter? (F100, Orchestrator 05.11.2026 08:00)

## Ergebnis
**Kein Heizstab, Verdichter bei 82 % Modulation** [sicher]. Die Regel B01 ist falsch geeicht: 5,5 kW liegt unter dem, was der Verdichter allein zieht.

## Belege
- **Ablauf** (`/home/<user>/hoxpi_fulllog/ww_hires.csv`): Heizlauf mit 1,7 kW und 35 % Modulation, 06:47:42 Beginn WW-Ladung, 06:48:32 Rampe, 06:48:52–06:50:12 Modulation 75–82 %, P_el 5,26–5,86 kW, Spitze 5,86 kW um 06:49:11. Bis 07:00 zurück auf 2,86 kW bei 41 %. [belegt]
- **Strom folgt der Modulation:** P_el/Modulation bleibt 6,74–7,15 W/% in allen 10 Zeilen ≥ 5,0 kW (06:48:52–06:50:22). Auch der Rückgang auf 73 % (5,09 kW) passt. Ein zugeschalteter Stab wäre ein Sprung um ~6 kW ohne Modulationsänderung. [belegt]
- **Hoval-Register** (`/home/<user>/hoxpi_fulllog/2026-11-05.csv`, 06:40–07:00): 27549 = 65036 (−50,0 °C), 31657 = 0, 19485 = 0, 19871 = 0, 18743 = 0, durchgehend unverändert. [belegt]
- **Lange Reihe:** Volllogger ab 30.07. (28.020 Zeilen, 5-min-Raster): Maximum 5,66 kW, nächste 5,47 und 5,36 kW. `ww_hires.csv` (123.116 Zeilen, ganze Datei): Maximum 5,96 kW bei 84 % (23.10. 07:23:21), kein Wert ≥ 8 kW. Die Überschreitung gab es also schon vorher im 10-s-Raster, das 5-min-Raster hat sie nur erstmals getroffen. [belegt]

## Vorschlag für die Karte (Entscheidung nach MD-22e)
Bei ~6,9 W/% ergäbe 100 % rechnerisch ~6,9 kW [Rechnung, 100 % nicht gemessen]. Verdichter bei kleinster Last ~1,7 kW plus Stab ~6 kW = ~7,7 kW [Rechnung, der Stab lief noch nie, seine Leistung ist die Angabe aus der Projektdoku].
Schwelle daher **`r('25611') > 7.2`** [wahrscheinlich]. Der Abstand ist mit 0,3–0,5 kW knapp. Der eigentliche Heizstabnachweis sind die Karten B02a und B02b (seit 05.11. aktiv).
Bis zur Änderung kann B01 bei kalten Ladestarts weitere Fehlalarme auslösen.

## Was bringt uns das
Der Heizstab war nicht an: keine Mehrkosten, nichts zu tun. Offen bleibt nur die Schwelle der Regel, damit der Wächter nicht bei jedem kalten WW-Start Alarm schlägt.

## Offen
- Verifikation im echten Stabbetrieb steht aus (noch nie gelaufen; 1477 war um 06:50 bei 3,6 °C).
- Modulationsspitzen beim WW-Start als eigene Frage: F101 / MD-31.