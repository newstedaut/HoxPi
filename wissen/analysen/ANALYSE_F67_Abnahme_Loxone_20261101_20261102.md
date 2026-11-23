# ANALYSE F67 - Abnahme Loxone-Umbau 01.11.2026 23:36 (02.11.2026 06:10)
Claude, Orchestrator, nur gelesen. An Anlage, Loxone und Pi nichts geaendert.

## Ergebnis
**Der Umbau ist im Miniserver noch nicht aktiv.** [sicher fuer den Zirkulations-Teil]
- In der Umbau-Datei `[lokaler Pfad]` fehlt diese Schaltuhr, im Stand davor `UMBAU_stand_20261101_2336.Loxone` ist sie drin. [sicher]
- Stimmt zum Eintrag in `02_Status_Offen.md`: "Datei getauscht, Miniserver noch offen".
- Der Merker "HomeVent Filter: Restwochen" ist live nicht gefunden; "Restzeit Filtertausch HomeVent" zeigt 147,49 und ist der alte Wert. [wahrscheinlich: alter Stand]

## Korrektur am Abnahmekriterium
Der SF2-Knick taugt nicht als Kriterium. [sicher]
| Tag | Pumpe 05:20:00 | 27483 05:15 / 05:20 / 05:25 / 05:30 / 05:35 | Knick |
|---|---|---|---|
| 31.10. | ja | 36,3 / 36,5 / 36,5 / 36,6 / 36,5 | nein |
| 01.11. | ja | 40,5 / 40,4 / 40,6 / 40,5 / 40,4 | nein |
Quelle: Volllogger `~/hoxpi_fulllog/2026-10-31.csv.gz`, `2026-11-01.csv`, `2026-11-02.csv`.

## Was bringt uns das
Die 0,4-0,5 kWh Waerme je Tag aus dem 05:20-Puls (MD-06) laufen weiter, und die Abnahme kann erst nach dem Speichern starten. der Betreiber: in Loxone Config "In Miniserver speichern". Zuvor kurz pruefen, ob die offene Datei die Umbau-Datei ist.

## Offen
Merker-Wert (~21 Wochen) und WC UG Def=4 nach dem Speichern erneut lesen.