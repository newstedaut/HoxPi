# Analyse Takt-Schutz V99 (Mindeststehzeit) / V101 (Mindestlaufzeit) - Orchestrator 22.10.2026 04:59
Quelle: `~/hoxpi_fulllog/ww_hires.csv` 07.10.-22.10.2026 04:54 (34 275 Zeilen, Raster ~60 s, ab 18.10. teils 10 s, keine Luecke > 180 s), nur gelesen. Skript `HoxPi-Doku\or_takt_20261022_0500.py` / `.out`.
Laufkriterium: Modulation > 0. Dauern = erster bis letzter Messpunkt im Segment, also real ~1 min laenger.

## Ergebnis
| Groesse | Wert |
|---|---|
| Verdichterlaeufe / Pausen (vollstaendig) | 114 / 115 |
| Starts je Tag | 3-11 (Median 8) |
| Pausen 6,5-14,9 min | **0** |
| kuerzeste regulaere Pause | 15 min gemessen (~16 min real), 1x; danach Haeufung bei 19 min (10x) |
| Pausen < 6,5 min | 5: 13.10. 07:09/08:37 (Abtau-Marker, je 0 + 4-5 min = Neustart nach Abtauung), **18.10. 11:11 2 min nach Fehler 222** |
| Laeufe < 6 min | 5: vier mit 4 min gemessen (= 5 min real), **20.10. 17:10 nur ~3-4 min** |
| Nacht 21./22.10. | Verdichter aus von vor 21 Uhr bis 04:22 (Heizlauf ab 04:22 bei 7,3 C) - kein Nachttakt |

## Bewertung
- **V99 (15 min Stehzeit) wahrscheinlich richtig** - 0 von 115 Pausen liegt zwischen 6,5 und 14,9 min. Ausnahmen nur mit Sonderereignis: nach Abtauung (~5,5 min, wie V102) und nach Stoerung.
- **Neu (sicher, Messung):** 18.10. 11:10:52 Fehlercode 222 fuer ~50 s, 11:11:42 alle Werte 0 bzw. -32768 (Fuehler ungueltig - sieht aus wie Neustart/Kommunikationsabbruch des Reglers), 11:13:52 Wiederanlauf mit 20 -> 37 -> 49 -> 42 % (Anlaufstuetze). Die Stehzeit gilt nach so einem Reset **nicht** - Fehler 222 trat auch 19.09. 21:11 auf. Vermutung: Spannungs-/Kommunikationseinbruch, nicht ueberbewerten.
- **V101 (5 min Mindestlaufzeit) abgeschwaecht:** 4 Kurzlaeufe passen (5 min real), aber 20.10. 17:10 lief der Verdichter nur ~3-4 min (Mod 35 %, <MAC>), zeitgleich Status_HK1 23 -> 0 (Heizkreis abgeschaltet). Wahrscheinlich: Mindestlaufzeit wird bei Wegfall der Anforderung nicht erzwungen (oder ist kuerzer als 5 min). Keine harte Sperre.
- Beobachtung (Vermutung, noch zu pruefen): beim Start 20.10. 17:10 springt die Spalte `Aussen` von 11,3 auf 16,3 C und faellt danach langsam - wirkt wie ein Fuehler am/im Geraet, der beim Luefteranlauf Abwaerme sieht. Fuer Heizkurven-Auswertungen die Aussentemperatur aus Stillstandszeiten oder Loxone nehmen.

## Was bringt uns das
- Der Takt ist harmlos: max. 11 Starts/Tag, keine Pause unter 15 min ohne Grund. Fuer den Winter keine Takt-Gegenmassnahme noetig.
- Loxone-Kick-Logik (WW-/SG-Kick) kann mit **15 min Sperre nach jedem regulaeren Stopp** planen; nach Abtauung oder Stoerung startet die WP frueher.
- Kurzlaeufe < 5 min entstehen, wenn Loxone die Anforderung (1490 / HK-Status) waehrend des Laufs wegnimmt - Stellschraube ist die Loxone-Logik (5-min-Zyklus AMQ46), nicht die Hoval.

## Fuer den Loop (nur lesend)
- Naechsten Fehler 222 im 10-s-Raster mit `~/x4_coilwatch.csv` und can0-Waechter vergleichen: echter Reglerneustart (Uptime-Zaehler) oder nur Buslücke?
- Naechsten Kurzlauf < 5 min: Reg 1490 und Status_HK1 im selben Zeitfenster - nimmt Loxone die Anforderung weg?