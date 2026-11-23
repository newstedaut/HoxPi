# ANALYSE F110: Arbeitet die Feuchteregelung der KWL in "Konstant"? (05.11.2026, Orchestrator)

## Ergebnis
**Ja, die Feuchteregelung arbeitet [sicher als Registerwert].** Die Projektaussage "regelt in Konstant nicht" stammt aus dem Vergleich 23625 gegen 23623. Das ist laut Hoval-Zitat ein Echo der Anzeige: "Die Anzeige der Luftmenge bleibt jedoch auf dem eingestellten Wert" (`IDM-Doku\Recherche_laufend\FUND_Hoval_HomeVent_TopTronic_20261015.md` Zeile 84).

Das Register, das antwortet, ist **23634 "Ventilator Fortluft soll"**. Volllogger 01.10.-05.11.2026, 10 297 Zeilen, Feuchte-Soll 23626 = 55 %.

| Delta = 23627 - 23626, bei 23625 = 45 % | Zeilen | 23634 Median |
|---|---|---|
| <= 0 | 564 | 38 (immer genau 38) |
| 1 | 778 | 40 |
| 2 | 782 | 42 |
| 3 | 703 | 44 |
| 4 | 374 | 46 |
| 6 | 109 | 50 |
| 8 | 29 | 54 |
| 10 | 2 | 58 |
| 12 | 4 | 62 |

- **Gesetz bei 23625 = 45: 23634 = 38 + 2 je Prozentpunkt Feuchte ueber Soll,** r = 1,0 bei n 3024 [sicher].
- Bei 23625 = 35: unter Soll genau 31, darueber Median 40, bis 57 [sicher].
- Bei 23625 von 58 bis 85 meist 63, also vermutlich ein Deckel [wahrscheinlich]; bei 100 % stehen 78.
- **In 92 % der Zeilen lag die Abluftfeuchte ueber dem Soll 55 %** (9450 von 10 297) [sicher]. Live 05.11. gegen 17:00: 23627 = 57, 23625 = 45, 23634 = 42, passt zum Gesetz.

## Grenzen
23634 ist ein Soll, keine gemessene Drehzahl. Ob der Luefter ihm folgt, ist hier nicht gemessen; `10_Wissen\Loxone\Wohnraumlueftung-Feuchteregelung.md` im Vault zeigt im Sommer Laufzeiten auf ~170 W bei unerreichbarem Soll, das spricht dafuer [wahrscheinlich].

## Was bringt uns das
Die KWL laeuft fast immer ueber ihrer Grundstufe, weil 55 % meist ueberschritten ist. Das kostet Luefterstrom und Waerme. der Betreiber kann entscheiden, ob der Feuchte-Sollwert (Loxone-Schieber, Reg 23626) angehoben wird. Nichts geaendert.

Skripte: `[lokaler Pfad]`, `or_kwl_feuchte2.py`.