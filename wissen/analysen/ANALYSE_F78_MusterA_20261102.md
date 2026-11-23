# ANALYSE F78 - Rest Muster a: dunkle Morgenflanken 14.10. und 16.10. (02.11.2026)
Claude, Subagent, nur lesend. An Anlage, Miniserver, Projektdatei und Pi nichts geändert. Ergänzt `[lokaler Pfad]`.
Zeiten lokal (MESZ), Z = UTC. Akku + = Entladung, Netz + = Bezug.

## Ergebnis
3. **Wahrscheinliche Kette:** Akku trägt WW-Start, [Energiemanager](https://www.loxone.com/dede/kb/energiemanager-2/) liest Entladung als Überschuss, schaltet zuerst den Heizkörper (Schwelle 0,5 kW), der erhöht die Entladung um 1,3 kW und zählt zusätzlich als abwerfbare niedrigere Last, dann überschreitet die WP-Schwelle 1,5 kW. Selbstverstärkung durch den Vorzeichenfehler. [wahrscheinlich; EM-Formel nicht veröffentlicht, Ausgang OL3 historisch nicht gelesen]
4. **Damit ist auch „seither keine Morgenflanke" erklärt:** Nicht der Fix vom 18.10., sondern der Heizkörper lief ab 17.10. nicht mehr. Warum, ist offen. [wahrscheinlich]
5. **Vorschlag Z. 8308 `MIN(I1;0)` -> `MAX(-I1;0)` ändert Muster a nicht.** Beide Flanken liegen im Zweig I3 = 0. [sicher für die Formel, siehe unten]
6. **Rest unerklärt:** Die 2-3 min Verzug bis zur Flanke, und am 16.10. rechnet das Modell im Schaltaugenblick nur rund 1,0 kW statt über 1,5. [sicher: Rechnung; Modell Vermutung]

## Tabelle: Flanken und Gegenproben
|---|---|---|---|---|---|---|---|---|---|
| **14.10. 06:23:41** | 42 -> 30 | 5,35 (Spitze 6,77) | 1,18 | -0,01 (04:20 Z, vor Rampe) | **ja, 1,3** | 0,53 | **1,83** | ja | **erklärt** [wahrscheinlich] |
| **16.10. 06:10:44** | 50 -> 31 | 5,15 (Spitze 6,64) | 1,18 | 0,34 | **ja, 1,35** | -0,35 | **1,00** (06:09: rund 2) | ja | **Mechanismus erklärt, Zeitpunkt nicht** [wahrscheinlich] |
| 19.10. 06:05 | 49 -> 30 | 5,02 | 0,94 | 0,04 | nein | -0,1 | -0,1 | nein | passt [wahrscheinlich] |
| 30.10. 02:30 | ≈ 49 | 3,14 | 1,12 | -0,10 | nein | -1,54 | -1,54 | nein | passt; Spitze 02:19 lief übers Netz (6,44 kW 02:20) [sicher] |
| 15.10. 05:36-05:40 | - | 5,06 | ≈ 1 | 0,13 | nein | ≈ 0 | ≈ 0 | nein | passt, Heizkörper lief in dieser Woche [Vermutung, H geschätzt] |
| 23.10. 04:34 | - | 5,82 | ≈ 0,5-1 | -0,08 bis -0,49 | nein | ≈ 0,5-1,0 | gleich | nein | **schwach**: am Rand der 0,5-Schwelle, aber ohne Stecker keine Wirkung [Vermutung] |
| 24.10. 05:36 | - | 5,69 | ≈ 0,3-1 | 0,08 | nein | ≈ 0-0,7 | gleich | nein | passt [Vermutung] |
| 02.11. 13:15:55 | 44 | Spwr -8,147 | - | 5,0-6,8 (12:10, 12:20 Z) | nein | ≤ -3 | ≤ -3 | nein | kein Widerspruch: Netz trug mit [wahrscheinlich] |

Dunkle Morgenflanken seit 01.08.: nur diese 2 (Statistik „Berechneter SG Ready" ab 01.08. gesichtet). [sicher]

### Hypothesen einzeln
| Hypothese | Prüfung | Urteil |
|---|---|---|
| Multiplexing, Zeitfenster | EM-Eingänge ohne Zeitlogik (Stand 11.10. Z. 8078 ff.). Flanken nicht auf einem Raster: Sekunde 44 und 221 von 300. Gleiche Uhrzeit an anderen Tagen ohne Flanke | **nein** [wahrscheinlich] |
| MinSoc | SOC 42-50 unter 95 an allen Morgen, auch ohne Flanke. Verlauf von SOC_Freigabe nicht lesbar | **kein Unterscheider** [wahrscheinlich] |
| MinRt | Vorige Abschaltung 13.10. 16:09 und 15.10. 19:01. Beide Phasen enden nach 45,2 min. Wirkt aufs Halten | **nur Haltezeit** [sicher] |
| IL6 (25611) | 14.10. 3,95, 16.10. 3,69, aber 19.10. 4,82 ohne Flanke | **kein Unterscheider** [sicher] |
| Lastprioritäten | Wallbox 0 (F76). Heizstab-Zähler 14.-16.10. 0. **Heizkörper an** | **Heizkörper ist der Unterscheider** [sicher Messung, Kette wahrscheinlich] |
| Reset Wallbox-Logik | Braucht Wallbox OL1 > 2 (Formel O63508, Stand 11.10. Z. 8258); Wallbox 0 | **nein** [wahrscheinlich] |
| Miniserver-Neustart, Speicherung | Kein Stand in `[lokaler Pfad]` zwischen 11.10. 00:34 und 18.10. 16:53. Keine Lücke in den 10-min-Punkten. Kein Neustart-Protokoll lesbar, Pi-Journal erst ab 01.11. | **kein Hinweis, nicht ausgeschlossen** [wahrscheinlich] |
| Sprung Akkuzustand | 14.10. 04 Z: 12 % = 1,72 kWh gegen Entladung 1,65. 16.10. 04 Z: 19 % = 2,72 gegen 2,89 | **nein** [sicher] |
| Akku-Stopp bei SOC 30 | 14.10. Stopp erst ca. 06:28-06:30, 16.10. nach 06:40, 19.10. ohne Flanke | **nein** [wahrscheinlich] |

## Belege

| Tag | L3 kW | Heizkörper ein | Flanke | Heizkörper aus |
|---|---|---|---|---|
| 12.10. | 0,04 -> 1,28 | 12:01, Pause 12:06-12:07 | 12:09:35 (PV echt) | 12:16 |
| 13.10. | 0,03 -> 1,27 | 11:19:50 | 11:22:01 | 11:27:00 |
| **14.10.** | 1,90 -> 3,2 (bei laufender WP) | **06:20:40** | **06:23:41** | 06:28:38 |
| 15.10. | 0,10 -> 1,32 | 17:13:30 | SG schon an | 17:19 |
| **16.10.** | 1,69 -> 2,92 | **06:08:37** | **06:10:44** | 06:17:45 |

Am Tag gibt es auch Flanken ohne vorherigen Heizkörper (15.10. 13:37, 16.10. 11:56 und 13:18). Dort lag echter PV-Überschuss an. Der Heizkörper ist also nur im Dunkeln nötig. [sicher: Zeiten; Deutung wahrscheinlich]

**Zuordnung zum Zähler** (`control_statistics` „Heizkörper" `<UUID>`, Gruppe 2, Tag):
| Tag | Zähler kWh | L3-Block min × kW |
|---|---|---|
| 12.10. | 0,286 | 13 × 1,36 = 0,29 |
| 13.10. | 1,332 | 66 × 1,3 = 1,4 |
| 14.10. | 0,161 (Stunde 04 Z) | 8 × 1,35 = 0,18 |
| 15.10. | 0,113 | 5 × 1,33 = 0,11 |
| 16.10. | 0,186 (Stunde 04 Z) | 9 × 1,37 = 0,21 |
| 20.09.-11.10., 17.10.-02.11. | 0,000 | die späteren L3-Blöcke sind rund 2 kW und nicht auf diesem Zähler |

Die 2-kW-Blöcke ab 17.10. sind ein anderes Gerät (F87). [wahrscheinlich]


**Spitzen ab 5,5 kW** (`[lokaler Pfad]`): Mit Akku als Träger und über 6,4 kW nur 14.10. und 16.10. Übrige über 6 kW liefen übers Netz (13.10., 23.10. 07:23, 30.10. 19:24, 01.11., 02.11.) oder mit PV (12.10., 26.10.). [sicher für diese Liste; Akku nur als Stundenenergie und 30-min-Punkt]

**Formel Z. 8308:** `IF(I3==1;MIN(I1;0);IF(I2<I4;I1;IF(I1<0;0;I1)))`. I3 = `IF(I1>=(I2-180);1;0)`, I1 = Minuten seit Mitternacht (Stand 11.10. Z. ab 8304). 06:23 = Minute 383, I3 wäre erst bei Sonnenuntergang vor 09:23 gleich 1. Zustand am 14./16.10. noch `IF(I3==1;0;...)`, gleicher Morgenzweig: `IF(I2<I4;I1;...)`, Spwr = -D. [sicher]

## Vorschlag Z. 8308 gesondert
- **`MIN(I1;0)` -> `MAX(-I1;0)`: keine Wirkung auf Muster a.** Der Abendzweig wird morgens nicht durchlaufen. [sicher]
- Wirkung hätte nur der andere Zweig (`I2<I4;I1` -> `-I1`, also F81 Punkt 2.2). Dann mindert Entladung den Überschuss, und A läge morgens tief im Negativen. [Vermutung, nicht getestet] Das betrifft auch die Tagesstarts, F78 riet deshalb zur getrennten Entscheidung.

## Was bringt uns das
| Punkt | Wirkung | Einstufung |
|---|---|---|
| Muster a, solange der Heizkörper nicht läuft | **0** seit 17.10. | wahrscheinlich |
| Kosten 14.10. und 16.10. | Heizkörper 0,35 kWh zusammen. WW auf 57 °C nur 14.10. (2,32 kWh_el, 61 % Netz, Ladung lief sowieso, F74 Nr 27); 16.10. blieb 52 | sicher für die Zahlen |
| Wenn der Heizkörper im Winter wieder läuft | Muster a kann wiederkommen, also je Vorfall rund **0,2 kWh Heizstrom** plus 45 min SG-Anforderung, bei repariertem I2 mit 57 °C | Vermutung |
| Akku | Heizkörper entlädt unnötig, je Vorfall 0,2 kWh | wahrscheinlich |

**der Betreiber (nichts umgesetzt):**
2. Falls wieder gebraucht: Entscheidung F81 2.2 (Vorzeichen auch im Morgenzweig) wird dringender. Sonst besteht kein Handlungsbedarf für Muster a. Rückweg und Backup wie dort, Skill `loxone-xml-umbau`.

## Offen
1. Verzug: Warum 2-3 min nach dem Heizkörper, nicht sofort? Kandidat RT 300 der WP [Vermutung]. Rechenintervall weiter unbekannt.
2. OL3 und IL3 im Oktober nicht aufgezeichnet. Der Heizkörper könnte auch am Stecker oder per App geschaltet worden sein; zweimal im Dunkeln passend 1:20 und 1:55 min nach WP-Rampe spricht dagegen [wahrscheinlich]. Nicht bewiesen.
3. Nachweis nur n = 2. Gegenproben gibt es, die Regel wurde aber nach den Daten gesucht. Die direkte Probe wäre `control_state` Energiemanager über einen Morgen mit Heizkörper; ohne des Betreibers Antwort zu Punkt 1 nicht zu erwarten.
4. Akku-Rohwerte 30 min nicht vollständig gegen die Schwelle gescannt (Datenmenge). Einzelne Entladespitzen ohne Flanke sind also nicht ausgeschlossen.
5. Nicht in diesem Lauf geklärt: Ausreißer 26.10. 15:36:09 (F78). Kein Heizkörper-Zähler, kein L3-Block ≥ 4 min in dieser Zeit; Muster nicht erklärt.
6. Miniserver-Neustart nicht direkt prüfbar, siehe Hypothesen.

## Stichproben zum Gegenlesen
| Zeit | Wert | Quelle |
|---|---|---|
| 14.10. 06:20 / 06:21 / 06:29 lokal | L3 2,32 / 3,07 / 1,14 kW; Minute 06:20 max 3,23 min 1,90; Rechnung `c_total_act_energy` × 60 / 1000 | `[lokaler Pfad]` |
| 14.10. 04:00 Z / 16.10. 04:00 Z | Zähler „Heizkörper" Stunde 0,1614 / 0,1860 kWh; Vortage 12.10. 0,286, 11.10. 0, 17.10. 0 | Loxone `<UUID>`, Gruppe 2, diff hour/day |

Skripte: `[lokaler Pfad]` bis `f78c_h.py`.