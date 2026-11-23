# ANALYSE F73 – Verdichter läuft im Heizbetrieb ohne Sollwert (1490 = 0, 1501 = 0), seit 24.10.2026

Stand: 02.11.2026 05:05, Daten bis 02.11. 04:56. Nur gelesen (Volllogger, Minutenlogger, Bridge-Journal, Verdichter-Catcher, Loxone-Projektdatei). An Anlage, Pi, Loxone nichts geändert. Zeiten Ortszeit.

## Frage
Wie oft läuft der Verdichter im Heizbetrieb (keine WW-Ladung, keine Abtauung, kein Kühlen), während 1490 = 0 und 1501 = 0 stehen? Ursache (Nachlauf, Raster, Hoval-eigene Anforderung, Frostschutz)? Speziell Lauf 01.11. 20:15 (Lauf 97 aus F55). Wie viel kWh_el?

## Kurzantwort
- **Keinen einzigen Start ohne Loxone-Sollwert gefunden.** 0 von 76 WW-freien Läufen starten ohne 1490 > 0 in den 5 Minuten davor [sicher, 60-s-Daten]. Hoval-eigene Anforderung oder Frostschutz: nicht belegt, [wahrscheinlich] nicht vorhanden.
- **Menge: 7 Phasen, 18 min, 0,59 kWh_el = 0,7 % von E_el Heizen.** Energetisch bedeutungslos [sicher, Rechnung].
- **Der eigentliche Befund ist funktional:** Beim Ofen-Nachlauf heißt 1490 = 24,0 für die Hoval 1520 = 30,0. Ist der RL unter 29 °C, startet die WP. Die Sperre beendet dann das Umwälzen für 8 h, also das Gegenteil des Ziels der Logik [wahrscheinlich].

## Datenquelle
| Quelle | Pfad | Inhalt | Raster |
|---|---|---|---|
| Volllogger | Pi `/home/<user>/hoxpi_fulllog/JJJJ-MM-TT.csv`, Kopien `[lokaler Pfad]` … `2026-11-01.csv`, `f73_2026-11-02.csv` (frisch gezogen) | alle Register, 2664 Zeilen, 24.10. 00:00:02 – 02.11. 04:55:01; 25.10. mit 300 Zeilen (25 h) | 5 min |
| Minutenlogger | Pi `/home/<user>/hoxpi_fulllog/kuehltest.csv`, Auszug `...\f73_kuehltest.csv` | Status_HK1 (= 1501), Soll_1490, Aussen, Vorlauf, Ruecklauf, P_el, Modulation; 13317 Zeilen, keine Lücke > 90 s | 60 s |
| WW-Logger | Pi `/home/<user>/hoxpi_fulllog/ww_hires.csv`, Auszug `...\f73_ww_hires.csv` | WW_Status, SLP, WP_VL, WP_RL, P_el, Modulation | 60 s, bei WW dichter |
| Bridge-Journal | Pi `journalctl -u hoval-bridge`, Auszug `...\f73_set1490.txt` | jeder Schreibzugriff `SET reg 1490`, **erst ab 01.11. 10:44** vorhanden | Sekunde |
| Verdichter-Catcher | Pi `/home/<user>/verdichter_catch/runs.log`, `runs/run_20261101_201149.csv`, `run_20261029_212206.csv`, `run_20261029_104633.csv` | Start und Verlauf je Lauf | ca. 46 s |
| Loxone-Projekt | `[lokaler Pfad] Config\Projects\Fam der Betreiber UMBAU.Loxone`, Zeilen 13581–13650 | Ofen-Nachlauf-Logik, Formel 1490 | – |
| Abschaltung 29.10. | `[lokaler Pfad]`, Zeile 801 (F47) | WP von der Betreiber abgeschaltet, Standbild 08:55–10:41 | – |

Skripte: `[lokaler Pfad]`, `f73_e.py`, `f73_f.py`, `f73_g.py`, `f73_h.py`, `f73_i.py`, `f73_j.py`.

## Methode
- **Phase:** 60-s-Zeile mit P_el > 0, Soll_1490 = 0, kein WW_Status/SLP im Fenster ± 30 s. Gegenprobe ± 90 s ergibt dieselben Minuten. Zusammenhängende Minuten = eine Phase. E_el = Σ P_el/100 · 1/60.
- **Weite Fassung:** Die Zeile zählt auch, wenn 1501 in dieser einen Minute noch 23 zeigt, weil 1501 dem 1490 bis zu 60 s nachläuft (WEZ-Register). Die strenge Zahl steht jeweils daneben.
- **Abtauung/Kühlen:** 1539 = 8 und 1539 = 2 treten nie zusammen mit 1490 = 0 auf (Kreuztabelle 2664 Zeilen) [sicher].
- **Nenner E_el Heizen:** 5-min-Basis 1539 = 1, 1504 = 0, 25611 ≥ 30: **81,29 kWh**. 60-s-Basis WW-freie Läufe ohne Standbild: **77,89 kWh**.
- **25.10.:** Die 2. Stunde 02:00–03:00 wird monoton gezählt, alle Zeiten bleiben Ortszeit [sicher]. Keine Phase liegt in dieser Stunde.
- **19870:** nicht verwendet. WW nur über 1504/1539 und WW_Status/SLP.
- **Hinweis zu 1501:** Das Register nimmt nur die Werte 0, 6, 23 an (5-min-Daten: 1139 / 187 / 1338) und ist damit kein Temperatur-Soll, sondern ein Status [sicher]. Der Logger führt es als `Status_HK1`, F59 nennt es "HK1 Betriebsart".

## Ergebnis

### A. Zählung
| Fassung | Anzahl | Minuten | E_el kWh | Anteil an E_el Heizen (81,29 / 77,89) |
|---|---|---|---|---|
| 5-min-Raster, streng (1539 = 1, 1504 = 0, 1490 = 0, 1501 = 0) | 3 Punkte (29.10. 10:50, 29.10. 21:25, 01.11. 20:15) | 15 (hochgerechnet) | 0,494 | 0,61 % / 0,63 % |
| 60-s-Raster, weit | 7 Phasen | 18 | **0,590** | **0,73 % / 0,76 %** |
| 60-s-Raster, streng (1501 = 0 in derselben Minute) | 5 Phasen | 15 | 0,497 | 0,61 % / 0,64 % |
| ganze Kurzläufe (P5, P6, P7) inkl. Startminute | 3 von 76 Starts (3,9 %) | 15 | 0,470 | 0,58 % / 0,60 % |

Das sind rund 0,06 kWh_el pro Tag über 9,2 Tage [sicher, Rechnung].

### B. Alle Phasen ab 24.10.
Werte aus den 5-min-Zeilen, Rohwert/10. "a→b" = Zeile davor → Zeile danach, wenn kein 5-min-Punkt in die Phase fällt.

| # | Beginn | Dauer | 1477 °C | 1520 °C | 1525 °C | 1535 °C | 1539 | 1501 | E_el kWh | Laufalter bei 1490 → 0 | Ursache | Sicherheit |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 | 25.10. 12:41:01 | ≤ 1 min | 5,2 | 33,0→0 | 37,0→34,0 | 33,5→34,0 | 1→0 | 0 | 0,029 | 17 min | Laufende: Loxone nimmt 1490 weg, Stopp binnen 60 s | Ablauf [sicher]; Kurzlauf-Schutz-Ende [wahrscheinlich] |
| P2 | 26.10. 15:43:02 | ≤ 1 min | 9,8 | 32,0→0 | 36,5→34,0 | 32,5→34,0 | 1→0 | 23 | 0,029 | 15 min | wie P1 | Ablauf [sicher]; Kurzlauf-Schutz [Vermutung], 1490 = 29,2 folgt 1513 = 30,8 nicht |
| P3 | 28.10. 10:42:01 | ≤ 1 min | 9,9 | 32,0→0 | 38,5→36,0 | 34,5→35,5 | 1→0 | 0 | 0,031 | 15 min | wie P1 | [wahrscheinlich], 1490 = 29,4 ≈ 1513 = 29,4 |
| P4 | 28.10. 15:03:02 | ≤ 1 min | 10,7 | 31,5→0 | 38,0→36,0 | 34,0→35,5 | 1→0 | 23 | 0,030 | 15 min | wie P1 | [wahrscheinlich], 1490 folgt 1513 ab 14:50 |
| P5 | 29.10. 10:47:02 | 5 min | 8,5 | 34,5→0 | 40,0 | 37,0 | 1 (10:45: 51) | 0 | 0,172 | Startminute | Wiederanlauf nach Abschaltung durch der Betreiber: Hoval hält noch das alte 31,8, Loxone überschreibt mit 0 | Abschaltung [sicher]; Ablauf [wahrscheinlich] |
| P6 | 29.10. 21:23:01 | 4 min | 5,0 | 35,0→0 | 34,5 | 31,5 | 1 | 0 | 0,131 | Startminute | Start und Loxone-Rücknahme in derselben Minute, Kurzlauf-Schutz greift nicht | Ablauf [sicher]; Reihenfolge [Vermutung] |
| | **Summe** | **18 min** | | | | | | | **0,590** | | | |

Nach Ursache:
| Ursache | Phasen | E_el kWh | Anteil an 0,590 |
|---|---|---|---|
| Laufende, Stopp binnen 60 s nach 1490 → 0 (Nachlauf/Raster) | P1–P4 | 0,119 | 20 % |
| Wiederanlauf nach Abschaltung 29.10. | P5 | 0,172 | 29 % |
| Rücknahme genau beim Start | P6 | 0,131 | 22 % |
| Ofen-Nachlauf-Impuls | P7 | 0,168 | 28 % |
| Hoval-eigene Anforderung, Frostschutz | – | 0 | 0 % |

**Nicht mitgezählt:**
- **Standbild 29.10.:** 09:52–10:42 zeigt der Minutenlogger 51 Minuten P_el = 185 mit Soll_1490 = 0 (rechnerisch 1,573 kWh). Das ist nicht echt. Alle Register außer 1490 stehen seit 08:55 still, X4 ebenfalls seit 08:54, und die WP war abgeschaltet (F47) [sicher]. In dieser Zeit zeigen die Rohdaten 1539 = 17. Wer ab jetzt über P_el summiert, muss 08:55–10:43 ausschließen (5-min: 3,238 kWh Scheinenergie).
- **27.10. 18:00:** 1539 = 4, 1504 = 0, also Ende einer WW-Ladung, kein Heizbetrieb [sicher].

### C. Lauf 01.11. 20:15 im Detail
| Zeit | Quelle | Ereignis |
|---|---|---|
| 20:10:01,990 | Journal | `SET reg 1490 <- 0` (regulärer 300-s-Takt) |
| 20:10:02 | Volllogger | 1490 = 0, 1501 = 0, 1520 = 0, 1525 = 27,5, **1535 = 24,0**, P_el = 0 |
| **20:10:27,008** | Journal | **`SET reg 1490 <- 240`** |
| 20:11:01 | Minutenlogger | Soll_1490 = 240, Status 23, P_el = 0 |
| **20:11:49** | Catcher | Modulation 44, VL_Soll **30,0**, Start erkannt |
| **20:11:49,607** | Journal | **`SET reg 1490 <- 0`** |
| 20:12:35 | Catcher | VL_Soll 0,0, Modulation 42, Verdichter läuft weiter |
| 20:15:02 | Volllogger | 1490 = 0, 1501 = 0, 1520 = 0, 1539 = 1, P_el = 2,10 kW |
| 20:15:39 | Catcher | Modulation 35 |
| 20:17:10 | Catcher | Modulation 0, Lauf zu Ende |

Einordnung:
1. **Kein Lauf ohne Sollwert, sondern ein Rasterloch.** Der Volllogger sieht 20:10:02 und 20:15:02 jeweils 1490 = 0, der 82-s-Impuls liegt dazwischen [sicher, Journal und Minutenlogger]. Der Schreibtakt springt danach von :01,99 auf :49,6, passend zum Loxone-Aktor, der bei Wertänderung sofort schreibt und dann alle 300 s wiederholt [wahrscheinlich].
2. **Der Wert 24,0 passt nur zum Ofenzweig.** Formel `IF(I2>0;MAX(I1;24);IF(I1>0;I1;IF(I3>0;MAX(I4;20);0)))`: Der Kurzlauf-Zweig hätte 1513 = 24,3 geschrieben, der Heizkurven-Zweig lag zuletzt bei 16,05 (F59), der Ofenzweig ergibt genau 24,0 [wahrscheinlich]. Die Ofentemperatur ist nirgends aufgezeichnet, die Bedingung selbst (Ofen > Raum + 5 K, Raum ≥ 22,5 °C) kann ich also nicht zurücklesen. Reg 1510 zeigte 22,1 °C; ob das der Wohnzimmer-Fühler der Formel ist, ist nicht geprüft.
3. **Warum die WP startete:** Bei 1490 = 240 setzt die Hoval 1520 = 300. Belegt am 26.10. 21:20–22:50 und am Catcher-Wert 30,0 [sicher]. Mit RL 24,0 ist die Startbedingung RL ≤ 1520 − 1,0 K = 29,0 weit erfüllt [wahrscheinlich].
5. **Warum der Verdichter weiterlief:** Alle drei Kurzläufe P5, P6, P7 zeigen im Catcher dasselbe Bild: 7 Snapshots mit Modulation > 0, 321 s vom ersten bis zum ersten Null-Snapshot, Modulation 42 → 35 [sicher]. Das passt zu einer Mindestlaufzeit von rund 5 min in der Hoval [wahrscheinlich]. Die RL-Stoppregel 1520 + 3,0 K kann nicht greifen, 1520 steht auf 0.



### D. Ausschluss der übrigen Ursachen
- **Hoval-eigene Anforderung:** 0 von 76 WW-freien Läufen ohne 1490 > 0 in den 5 min vor dem Start [sicher als Messung]. Bei 60-s-Abtastung könnte ein Impuls < 60 s durchrutschen; der Catcher zeigt bei P5–P7 aber jeweils VL_Soll > 0 beim Start [sicher]. Ergebnis: keine Eigenanforderung erkennbar [wahrscheinlich].
- **Frostschutz:** Außen 4,4–10,7 °C, 1513 nie unter 24,3 °C in den Phasen [sicher]. Frostschutz scheidet aus [wahrscheinlich].
- **Volllogger-Raster:** Ja, bei P7 die Hauptursache und bei P1–P4 der Grund, warum man sie im 5-min-Raster gar nicht sieht [sicher].
- **Nachlauf bis RL-Schwelle:** Bei keiner Phase. P1–P4 stoppen binnen 60 s nach 1490 → 0, P5–P7 nach rund 5 min unabhängig vom RL [wahrscheinlich].

### E. P5 und P6
- **P5 (29.10. 10:47):** der Betreiber hatte die WP ab 08:55 abgeschaltet (F47, ORCHESTRIERUNG_LOG.md Zeile 801) [sicher]. Bei der Rückkehr 10:43 steht im Register wieder 318, obwohl Loxone zuletzt 0 wollte; 1539 = 51 ist laut F47 der normale Anlauf. Der Verdichter startet 10:46:33 mit VL_Soll 34,5, Soll_1490 = 0 ab 10:47:02 [sicher]. Bedienereingriff, einmalig. Nebenbefund: 1506 fällt von 47397 auf 47391 [sicher]; Standbild plus Neustart, Ursache nicht weiter geprüft.
- **P6 (29.10. 21:23):** 1490 > 0 lief seit 14:11 (432 min). Letzter Wert 322 um 21:22:01, Catcher erkennt Modulation 10 um 21:22:06, Soll_1490 = 0 um 21:23:01 [sicher]. Danach bleibt 1490 bis etwa 00:15 auf 0 (Nachtpause, ORCHESTRIERUNG_LOG). Ablauf: Der Kurzlauf-Schutz braucht Verdichterstart und OutHeat1 = 1 gleichzeitig. Ist OutHeat1 schon weg, bevor 25611 in Loxone über 0,5 kW steht, greift er nicht [Vermutung; 25611 ist bis 60 s alt, Loxone-Historie reicht nicht zurück]. Warum die Hoval erst um 21:22 startet, obwohl die RL-Bedingung schon länger erfüllt war: 1520 sprang um 21:07 auf 35,0, also genau 15 min vorher. Passt zum 15-min-Bild aus dem Arbeitsstand [Vermutung].

### F. Stichprobe Rohzeilen
Journal, `journalctl -u hoval-bridge`:
```
2026-11-01 20:10:01,990 INFO SET reg 1490 (Flow setpoint constant req. heating) <- 0 (raw)
2026-11-01 20:10:27,008 INFO SET reg 1490 (Flow setpoint constant req. heating) <- 240 (raw)
2026-11-01 20:11:49,607 INFO SET reg 1490 (Flow setpoint constant req. heating) <- 0 (raw)
2026-11-01 20:16:49,678 INFO SET reg 1490 (Flow setpoint constant req. heating) <- 0 (raw)
```
Volllogger `/home/<user>/hoxpi_fulllog/2026-11-01.csv`, Spalten zeit, 1477, 1490, 1501, 1504, 1510, 1513, 1520, 1525, 1535, 1539, 25611, 25612:
```
2026-11-01 20:10:02 44 0 0 0 221 243 0 275 240 0   0 0
2026-11-01 20:15:02 44 0 0 0 222 244 0 365 340 1 210 7
2026-11-01 20:20:01 44 0 0 0 222 249 0 345 340 0   0 0
```
Minutenlogger `/home/<user>/hoxpi_fulllog/kuehltest.csv`, Spalten zeit, Status_HK1, Pumpe_HK1, Mischer_HK1, Soll_1490, Aussen, Vorlauf, Ruecklauf, P_el, Modulation:
```
2026-11-01 20:10:03  0 0 -100   0 44 270 240   0  0
2026-11-01 20:11:01 23 1   -4 240 44 270 240   0  0
2026-11-01 20:12:02 23 1    0   0 44 330 320 204 42
2026-11-01 20:13:02  0 1    0   0 44 360 335 205 42
2026-11-01 20:16:02  0 1 -100   0 44 370 340 175 35
2026-11-01 20:17:01  0 1 -100   0 44 350 345   0  0
```
Nachrechnung P7: (204+205+211+210+175)/100/60 = 10,05/60 = **0,168 kWh** [sicher].

## Was bringt uns das
1. **Kein Hoval-Geheimnis:** Die WP startet im Heizbetrieb nicht von sich aus. Die Kette Loxone → 1490 → Hoval stimmt, F55/F59 müssen nicht korrigiert werden, nur F55 "Lauf 97 Ursache unklar" ist erledigt [wahrscheinlich].
2. **Energie kein Hebel:** 0,59 kWh in 9,2 Tagen, 0,7 % [sicher]. Das rechtfertigt allein keine Änderung.
4. **Auswerteregel:** Für alles, was 1490 am Lauf misst, reicht das 5-min-Raster nicht; Minutenlogger `kuehltest.csv` und ab 01.11. das Bridge-Journal verwenden [sicher]. 29.10. 08:55–10:43 aus P_el-Summen ausschließen [sicher].

Loxone-Bausteine, offizielle Doku (URLs nach dem üblichen Muster, nicht einzeln geöffnet [wahrscheinlich]):
- Formel: https://www.loxone.com/dede/kb/formel/
- Monoflop: https://www.loxone.com/dede/kb/monoflop/
- Schwellwertschalter: https://www.loxone.com/dede/kb/schwellwertschalter/
- Klimacontroller: https://www.loxone.com/dede/kb/klimacontroller/
- UND: https://www.loxone.com/dede/kb/und/

## Offen
- **Ofenzweig direkt belegen:** Ofentemperatur und Sperr-Monoflop sind nicht aufgezeichnet, die Loxone-MCP-Historie liefert für den 01.11. nichts (`tempActual` Wohnzimmer ohne Verlauf, Raumregler nicht chartbar). Prüfweg beim nächsten Ofenabend: Journal auf `<- 240` und Loxone-Merker lesend mitschreiben.
- **Stand der Datei:** Ob die UMBAU-Datei genau auf dem Miniserver läuft, ist nur [wahrscheinlich] (F59; ORCHESTRIERUNG_LOG Zeile 446 nennt die Prüfung von Eingang I3 als offen). Die 1490-≈-1513-Verläufe in P3/P4 sprechen dafür, dass der Kurzlauf-Zweig aktiv ist.
- **P2:** Laufende bei exakt 15 min, obwohl 1490 nicht 1513 folgt. Zufall oder anderer Mechanismus, offen.
- **P6:** Reihenfolge OutHeat1 / 25611-Flanke nicht belegbar; erst wiederholt prüfen, wenn es erneut auftritt. Das Journal für 1490 reicht nur bis 01.11. 10:44 zurück (älteste Einträge, Grund nicht geprüft).
- **Mindestlaufzeit:** Rund 5 min aus 3 Läufen [wahrscheinlich]; Hoval-Parameter dazu nicht gesucht.
- **Start ohne Wartezeit:** P7 startet binnen höchstens 82 s nach dem Sollwert, P6 erst nach langer Soll-Phase. Das 15-min-Bild gilt also nicht pauschal; Bedingung offen [sicher als Beobachtung, Deutung offen].