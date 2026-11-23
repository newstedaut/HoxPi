# ANALYSE Raumknick 1510 in der Nacht 22./23.10.2026 (Orchestrator 23.10.2026 05:55, nur lesend)

Frage (offen aus `ANALYSE_Auskuehlung_Heizlast_20261023.md`, Vermutung 3b): Warum faellt der Raumwert 1510 zwischen 01:00 und 03:00 mit 0,4 K/h, obwohl das Haus sonst ~0,075 K/h verliert?

## Quellen
- [VL] Pi `~/hoxpi_fulllog/2026-10-22.csv`, `2026-10-23.csv` (5 min), Spalten per Kopfzeile: 2=1477 Aussen, 15=1490 HK1-Soll, 35=1510 Raum-Ist HK1, 44=1519 Starts, 60=1535 RL, 201=18726 Modulation.
- [LX] Loxone-MCP `control_state` 23.10. 03:56:46 UTC (= 05:56 Ortszeit), IRoomControllerV2 "Wohnzimmer" <UUID> und alle tempActual.

## Messung 1510 (sicher, [VL])
| Zeitraum | 1510 | Aussen | Heizung |
|---|---|---|---|
| 22.10. 18:00-23.10. 01:00 (7 h) | 21,2-21,4 °C, praktisch flach | 8,4 -> 3,8 °C | aus (nur WW 18:40-19:00) |
| 01:00-03:00 | 21,4 -> 20,6 °C (-0,8 K, ab 01:10 stetig) | 3,8 -> 2,8 °C | aus |
| 03:00-05:55 | 20,4-20,6 °C, wieder flach | 2,8 -> 1,9 °C | Heizlauf 03:01-03:40, WW 04:35-05:20, Heizlauf ab 05:40 |

Starts heute bis 05:55: 3 (1519 20706 -> 20709).

## Vergleich Loxone (sicher, [LX], Momentaufnahme 05:56)
- WZ tempActual **21,3 °C**, 1510 zur selben Zeit **20,5 °C** -> 0,8 K Differenz (bekannt: 1510 laeuft bis 0,8 K kaelter als T_A, Holzofen-Analyse).
- WZ-IRR: Modus Heizen (currentMode 1), Soll 21,5, Toleranz 0,5, openWindow 0. `overrideEntries`: start [Nummer], end [Nummer], reason 6, level -1 -> als Loxone-Zeit (s seit 01.01.2009) = **<MAC>**.

## Bewertung
- **Sicher:** Der Knick ist ein Effekt im Signal 1510, nicht im Gebaeude: 7 h flach, 2 h -0,4 K/h, danach sofort wieder flach (schon vor Waermeankunft aus der FBH, die Stunden braucht). Der WZ-Loxone-Fuehler steht morgens 0,8 K hoeher.
- **Wahrscheinlich:** Der Knickbeginn 01:00 faellt mit dem Beginn des WZ-Override (reason 6, level -1) um 01:00:20 zusammen. Ob Loxone-Zeit hier lokal oder UTC ist, ist nicht geprueft; bei UTC laege das Fenster 03:00-06:59 und faellt dann mit dem Heizstart 03:00:52 zusammen. Beides passt zu "Loxone-Logik beeinflusst 1510/Anforderung", nicht zu Physik.
- **Vermutung:** reason 6 = zeitgesteuerter Eco-/Absenk-Eintrag (Loxone-Bedeutung der Codes hier nicht belegt).

## Was bringt uns das
- Die Heizlast-Schaetzung (62-130 W/K) stuetzt sich auf 1510; der Abschnitt 01-03 ist ein Signalartefakt und sollte aus Auskuehl-Rechnungen raus -> Haus eher noch traeger als gerechnet, Ueberdimensionierung der C17 eher groesser.
- Falls Loxone nachts um 01:00 per Override absenkt und um 03:00 Heizbedarf ausloest: genau dieses Muster erzeugt Kurzlaeufe im Winter. Abhilfe waere, den Nacht-Override im WZ zu entfernen (der Betreiber entscheidet, nichts geaendert).

## Naechste Schritte (nur lesen)
1. Loop: 1510 gegen Loxone WZ tempActual in einer zweiten Nacht nebeneinander loggen (Knick um 01:00 wieder?).
2. In der Loxone-Config nachsehen: wer schreibt Hoval 1510 (Modbus-Ausgang/HoxPi) und was ist der WZ-Override 01:00 (Zeitschaltung? Reason 6).
3. Loxone-Zeitbasis der overrideEntries (lokal/UTC) einmal am aktuellen Eintrag gegen die App pruefen.