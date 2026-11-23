# ANALYSE F96: Wer schrieb 23626 nach dem Stufentest zurueck?

Stand: 02.11.2026 ca. 18:05 MEZ, Orchestrator (selbst, kein Subagent). Nur gelesen. An Loxone, Hoval, Pi nichts geaendert.

## Ergebnis
1. **Loxone schrieb zurueck, 4 min 34 s nach dem Test** [sicher]. Aktor AMQ181 "Feuchtigkeitssollwert" schreibt Reg 23626 alle 300 s aus VI72 "KWL Max. Luftfeuchte" (55).
2. **Der kurze Sprung ist trotzdem ein Stufentest mit beiden Flanken:** 23634 fiel von 46 auf 38 und ging nach dem Zurueckschreiben auf 44 und 46, bei gleicher 23625 = 45 und Abluft 23627 = 58-59 [sicher als Messung]. So ein Sprung kam in 1.101 Vergleichsschritten nie vor. **Die Feuchteautomatik regelt in "Konstant" also** [wahrscheinlich, n 1, Ursache gefolgert]. Das widerspricht der Projektanweisung und `KWL_Feuchteautomatik_Befund_20260911.md`.
3. **Regel fuer Handtests:** Ein Schreibzugriff auf eines der 11 aktiven Register unten haelt hoechstens bis zur naechsten Wiederholung (60 oder 300 s). Solche Tests muessen ueber den Loxone-Eingang laufen.

## Belege
Bridge-Journal `journalctl -u hoval-bridge` (rollt nach ~20 h weg), Zeiten MEZ:
| Zeit | SET reg 23626 |
|---|---|
| 15:57:11 | 55 |
| 16:02:11 | 55 |
| **16:02:37,688** | **65** (Handtest, Chat 16:10) |
| **16:07:11,129** | **55** (naechste Wiederholung) |
| 16:12:11 | 55 |
| 17:52:11 | 55 (Takt laeuft weiter) |

Volllogger `~/hoxpi_fulllog/2026-11-02.csv`:
| Zeit | 23626 | 23634 | 23627 | 23625 |
|---|---|---|---|---|
| 15:55:01 | 55 | 46 | 59 | 45 |
| 16:00:02 | 55 | 46 | 59 | 45 |
| **16:05:01** | **65** | **38** | 59 | 45 |
| 16:10:01 | 55 | 44 | 58 | 45 |
| 16:15:01 | 55 | 46 | 59 | 45 |
| 16:20:02 | 55 | 46 | 59 | 45 |

Vergleich: 5-min-Schritte von 23634 mit 23626 = 55, 23625 = 45, Aenderung 23627 hoechstens 1, Volllogger-Kopien im Ordner `[lokaler Pfad]` bis 01.11.: n = 1.101, Schritte -2 (103), 0 (908), +2 (90), nichts anderes [sicher als Zaehlung]. Skript `or_f97_1755.py`.

Projektdatei `[lokaler Pfad] Config\Projects\Fam der Betreiber UMBAU.Loxone` (01.11.2026 23:36): Z. 3414 AMQ181, ModbusAddress 23626, Cmd 6, RepeatRate 300; Z. 2139 VI72 (Standard 55, 40-65, [Virtueller Eingang](https://www.loxone.com/dede/kb/virtuelle-ein-ausgaenge/)); Z. 14876 Eingangsverweis, Z. 15368 Ausgangsverweis. Der einzige Fremdpartner an Port 502 des Pi ist <LAN-IP> [sicher]; dass das der Miniserver ist, ist hier nicht nachgesehen [wahrscheinlich].

## Wer schreibt wiederholt? (Datei gegen Journal 02.11. ab 12:00)
| Reg | Titel (Loxone) | Repeat s | Journal, ca. 6 h |
|---|---|---|---|
| 1490 | Sollvorlauf Heizen HC1 | 300 | wechselnde Werte |
| 1496 | Betriebswahl WW | 300 | 72 x 4 |
| 1497 | Normal-Temperatur WW | 300 | 36 x 500, 36 x 520 |
| 23622 | Betriebsart Lueftung | 300 | 72 x 4 |
| **23623** | Modulation Normal | **60** | 358 x 45 |
| **23624** | Modulation Eco | **60** | 358 x 70 |
| 23626 | Feuchtesoll | 300 | 72 x 55, 1 x 65 |
| 27510 | Regelstrategie HC1 | 300 | 72 x 3 |
| 27545 | Smart Grid | 300 | 72 x 0 |
| 29435 | Vorlauf-Min Kuehlen HC1 | 300 | 71 x 180 |
| 29436 | Vorlauf-Min Kuehlen HC2 | 300 | 71 x 180 |

Ohne Wiederholung und seit 12:00 ohne Schreibzugriff: 19482, 28939. 07-001 (Reg 30684) hat keinen Aktor und keine Journalzeile, wird also nicht von Loxone ueberschrieben [sicher fuer Datei und Zeitraum].

## Grenzen
- Nur eine Stufe, nur eine Rasterzeile im 65-%-Zustand. Der Wert 38 passt zur Vorhersage aus F94, die Luefterleistung ist damit nicht gemessen.
- Das Meter "Wohnraumlueftung" hat fuer 4,5 min keine brauchbare Aufloesung, die 10 W aus F94 bleiben Schaetzung.
- Ob die 60-s-Wiederholung auf 23623/23624 das HomeVent belastet (CAN-Last, Speicher), ist hier nicht geprueft [offen].

## Was bringt uns das
| Punkt | Wirkung |
|---|---|
| Stufentest | Die Kernfrage aus F94 ist ohne zweiten Eingriff weitgehend beantwortet. Ein laengerer Test ueber VI72 liefert nur noch den Stromwert und die Raumwirkung |
| Handtests | Kein falscher "laeuft bis 18:35"-Vergleich mehr: Tabelle vor jedem Test ansehen |
| Hebel Feuchtesoll | VI72 ist der richtige Schalter, Soll 60 bleibt deine Entscheidung (F94, rund 0,3-0,5 kWh/Tag, Rechnung) |