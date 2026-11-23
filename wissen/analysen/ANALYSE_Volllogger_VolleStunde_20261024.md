# ANALYSE: Volllogger – „volle Stunde 1501/1520/1539 = 0“ ein Artefakt? (Katalog F20, OR 24.10.2026 07:00)

Anlass: Nebenbefund OR 24.10. 06:00 – Volllogger-Zeilen 23.10. 17:00/18:00/19:00 zeigten 1501/1520/1539 = 0 mitten in Anforderungsphasen.
Skript: `[lokaler Pfad]` (Pi: `/home/<user>/or_f20_20261024_0700.py`), nur lesen, `~/hoxpi_fulllog/` 10.10.–24.10. (4117 Zeilen, 556 Spalten).

## Ergebnis
- **Kein Logger-Artefakt (wahrscheinlich, nahe sicher).**
  - Die Zeilen sind vollständig (0 leere Felder, 556 Spalten), Zeitstempel :00:01/:00:02 wie alle anderen.
  - Keine Einzel-Null zur vollen Stunde: Muster „1501 = 0 zwischen zwei Nicht-Null-Zeilen“ 10.–24.10. genau 1×, und zwar 22.10. 07:50 (nicht :00) – dort 1501/1520/1539/18722 gleichzeitig 0, 31708 = 343 (sicher).
  - 23.10. sind es **mehrzeilige Pausen**, nicht einzelne Stundenzeilen (sicher, Rohzeilen):

| Pause 23.10. | Dauer | 1501 / 1520 / 18722 | 31708 Volumenstrom |
|---|---|---|---|
| 16:55–17:15 | 5 Zeilen (~25 min) | 0 / 0 / 0 | 0 |
| 18:00–18:05 | 2 Zeilen (~10 min) | 0 / 0 / 0 | 0 |
| 18:55–19:05 | 3 Zeilen (~15 min) | 0 / 0 / 0 | 0 |

  - Unabhängige Größen fallen konsistent mit: Volumenstrom 31708 = 0 und 18722 = 0 → HK1-Pumpe wirklich aus, also echte Anforderungspausen (sicher, dass es kein reiner Anzeigefehler einer Spalte ist).
  - Kurze 0-Phasen 1501 (23 → 0 → 23, ≤ 40 min) 10.–24.10.: **9**, Startminuten verteilt (:00, :05, :10, :30, :40, :45, :50, 2× :55) → kein Stundentakt; die Häufung um die volle Stunde am 23.10. ist Zufall (wahrscheinlich). 3 der 9 Phasen mit 31708 ≈ 340 (17.10., 18.10., 22.10.) = Volumenstrom ohne HK1 → WW-Ladung o. Ä. (Vermutung, 1539 dort nicht geprüft).
- **Auslöser der Pausen:** 1520 (HK1-Soll) = 0 zusammen mit 1501 = 0 → die HK1-Anforderung an die Hoval war in diesen Minuten weg (sicher aus 1520).

## Was bringt uns das
Der Volllogger ist an dieser Stelle verlässlich; Auswertungen müssen die Stundenzeilen nicht filtern. Kurze Anforderungspausen (10–25 min) sind real und erzeugen zusätzliche WP-Stopps → für F17 (Startvorhersage) relevant.