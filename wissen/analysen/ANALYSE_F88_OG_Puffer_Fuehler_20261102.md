# F88 - Lebt der 1-Wire-Fühler HK2/OG, und was sagen PF1/PF2/WPF? (Analyse-Agent, 02.11.2026)

Nur gelesen. An Hoval, CAN, X26, X4, Kälteregler, Loxone und Pi-Diensten nichts geändert. Zeiten in MEZ, Loxone-Zeitstempel UTC mit Zusatz.

## Frage
Lebt "Thermometer_HK2_OG_Vorlauf" in Loxone, was sagen die Hoval-DP 17386/[Nummer], und lässt sich damit die Puffer-Schichtung oder der OG-Kreis ohne neuen Fühler sehen?

## Kurzergebnis
- **1-Wire-Fühler HK2: lebt/tot konnte ich nicht entscheiden.** Er ist per MCP nicht lesbar, weil er keine Kachel hat, und er hat keine Statistik. Einen Live-Wert und einen Verlauf von ihm gibt es hier daher nicht. Indizien sprechen für "lebt". [Vermutung]
- **Schichtung sehen: nein.** Keine dieser Quellen sitzt am Puffer. [sicher] **OG-Kreis sehen: nein.** Der Fühler sitzt wahrscheinlich im Technikraum am stehenden HK2-Rohr, nicht im OG, und das OG bekommt ohnehin keine WP-Wärme (F62). [wahrscheinlich]
- **Neuer Befund:** VF2 (1514) liegt nicht nur auf Raumniveau. Bei stehenden Pumpen, Mischer -100 % und auskühlendem WP-Vorlauf steigt er zusammen mit VF1 (1513) um 3-4 K in 1,5-2 h. Die Ursache ist offen, siehe Ergebnis 4.

## Datenquelle
| Quelle | Was |
|---|---|
| HoxPi `read_register`, `search_registers`, `diagnose`, 02.11.2026 ~13:03-13:08 | 1490, 1513, 1514, 1525, 18760, [Nummer], 19658, 19706, 19707, 27493, 27494 |
| Pi `/home/<user>/hoxpi_fulllog/20*-*.csv(.gz)`, 30.07.-02.11.2026 13:00, 27 218 Zeilen, lokale Auszüge `[lokaler Pfad]` | Spalten siehe `f88_fetch.py` |
| Pi `/home/<user>/hoval-bridge/registers.json`, `cache_last.json`, `bridge_state.json`, `/home/<user>/reg_fullcheck.csv` | Zuordnung der Register, Cache-Inhalt |
| Loxone-MCP, 02.11.2026 12:03-12:07 UTC | Thermometer_HK1_UG_Vorlauf, Thermometer_Boiler_Oben, HK2 Vorlauf ist, HK2 Mischer, Aktuelle Puffertemperatur Oben, Technikraum, Zähler Trockner/Waschmaschine |
| Projektdatei `[lokaler Pfad]`, gegengelesen mit `...\UMBAU_stand_20261101_2336.Loxone` | Verdrahtung |
| Fotos `[lokaler Pfad]` (Nr 125), `...\gp_KtzS7vr0pOGO-h4H.jpg` (Nr 149) | selbst angesehen |

Bekanntes aus `[lokaler Pfad]`, `...\ANALYSE_Loxone_Fuehler_Inventar_Heizung_20261023.md` und `...\BAUTEILE_BEKANNT.md` Z. 21-26 (TTE-PS nie in Betrieb) ist hier nicht neu hergeleitet.

## Methode
1. Fühler in Live-Struktur (MCP) und Projektdatei suchen, mit den zwei lebenden Fühlern an derselben 1-Wire-Extension vergleichen.
2. Ausgänge des Fühlers durch die Logik verfolgen: Gibt es einen sichtbaren Folgewert, aus dem er sich ableiten lässt?
3. Puffer-DP: Live-Wert, ganze Logdauer, und Herkunft im HoxPi-Cache.
4. Ersatz für den fehlenden Verlauf: VF2 (1514) über 15 Tage (19.10.-02.11.) gegen HK1-Pumpe 19706, 1513 und 1525. Das ist **der Hoval-Fühler am selben Kreis, nicht der 1-Wire-Fühler**.
5. Ursachensuche für die VF2-Anstiege nur so weit, wie die Daten reichen.

## Ergebnis

### 1. 1-Wire-Fühler Thermometer_HK2_OG_Vorlauf
| Punkt | Befund | Sicherheit |
|---|---|---|
| Live per MCP | `control_find` ohne Treffer, `control_describe` auf <UUID> "not found in structure", `control_state` 0 Zeilen, `control_statistics` "not found" | [sicher] |
| Warum | Der Sensor hat im `IoData` kein `Visu="true"`, HK1 und Boiler haben es (Projektdatei Z. 6212-6215 gegen Z. 6196, 6204) | [sicher] |
| Verlauf | Kein `StatsType` am Sensor, also keine Statistik. Nur der Boiler-Fühler hat `StatsType="11"` (Z. 6204) | [sicher] für die Datei |
| Verdrahtung | ROM 28CE2F540D0000C3, Poll 15 s, an 1-Wire Extension Serial 05D8EF2B. Verweis Seite "Technikraum" (Z. 10250) -> Formel "Heizen/Kühlen" `IF(I1>26;1;IF(I1<21;2;0))` (Z. 10614). AQ und TQ der Formel gehen nirgends hin | [sicher] |
| Ableitung über Folgewert | Nicht möglich: Die Formel hat keinen Verbraucher, der Fühlerwert wirkt auf nichts | [sicher] |
| `MaxVal="10"` (Doppelpunkt aus Inventar und F62) | Harmlos: alle vier 1-Wire-Sensoren haben `MaxVal="10"`, und der Boiler-Fühler liefert trotzdem 47,375 °C. Der Wert wird nicht abgeschnitten | [sicher] |
| Indizien "lebt" | Zwei Fühler an derselben Extension liefern live mit `error = 0`. In `system_status` (12:03:11 UTC) steht unter den aktiven Meldungen keine zu diesem Fühler oder zur Extension. Ob Loxone einen stummen 1-Wire-Fühler dort meldet, ist nicht geprüft | [Vermutung] |

**Urteil: nicht entschieden, Tendenz lebt. [Vermutung]** Den geforderten Live-Wert und den 7-Tage-Verlauf dieses Fühlers gibt es über die erlaubten Wege nicht.

### 2. Was der Fühler physisch misst
- Auf den Fotos Nr 125 und Nr 149: Die Rohre mit Hülse "HK2" und "HK1" steigen im Technikraum nach Mischer, Pumpe und Zeigerthermometer auf. An beiden sitzt eine Metallschelle, dazu läuft ein schwarzes Kabel. An HK2 gibt es zusätzlich ein graues Kabel mit Aufschrift "HK2". Auf der Wand darunter eine Dose "Loxone OneWire", daneben "Taupunktfühler". [sicher sichtbar]
- Welches Kabel der 1-Wire-Fühler und welches Hoval-VF2 ist, ist auf den Fotos nicht zu trennen. Zum Fühler gibt es in der Datei kein `NDOC` mit Montageort (anders als "Raumtemperatur", Z. 6188). In `[lokaler Pfad]` und im Vault steht nichts dazu.
- Deutung: Er misst den HK2-Vorlauf an diesem Rohrstück im Technikraum, und "OG" im Namen meint den Kreis, nicht den Einbauort. [wahrscheinlich] Dass die schwarze Schelle an HK2 genau dieser Fühler ist: [Vermutung]
- Weil HK2 steht, misst er dort stehendes Wasser. Er wäre also fast nur eine zweite Ablesung von VF2 (1514), und das bringt keine Durchfluss- oder OG-Information. [wahrscheinlich]

### 3. Hoval-DP 17386, 17387, 27494
| Reg | Name (registers.json) | Unit | Live 02.11. ~13:03 | Gesamte Logdauer (27 218 Zeilen, 1 Zeile leer) | Bedeutung |
|---|---|---|---|---|---|
| 17384/17385 | Status/Soll Puffer | PS, 143 | 0 / 0 | immer 0 | Modul nicht am Bus, nicht im `cache_last.json`, `reg_fullcheck.csv` Status NULL [sicher] |
| 17386 | Buffer PF/KPF2 actual | PS, 143 | 0 | immer 0 | dito: **0 ist kein Messwert** [sicher] |
| 17387 | Buffer PF2/KPF actual | PS, 143 | 0 | immer 0 | dito [sicher] |
| 27493 | HPBS sensor_high | WEZ, 1 (DP 1570) | Cache 32768, MCP `null` | nicht geloggt | im Cache, Alter 28,8 s, also frische WEZ-Antwort [sicher] |

- Die WEZ meldet für den WPF ausdrücklich "kein Wert" statt einer Temperatur. Das passt zu einem nicht angeschlossenen Fühler. [wahrscheinlich] Das bestätigt und schärft die Inventar-Aussage "liefert nichts".
- Die Loxone-Kachel "Aktuelle Puffertemperatur Oben" zeigt deshalb 0 °C (12:03:14 UTC). Das sieht wie ein Messwert aus, ist aber keiner. [sicher]
- Aktive Bus-Abfragen waren nicht nötig und wurden nicht gemacht.

### 4. VF2 (1514) im Verlauf, als Ersatz
Tagestabelle aus `f88_log.csv` (Rohwert/10):

| Tag | 1514 min/Mittel/max °C | HK1-Pumpe 19706 an % | HK2-Pumpe 19707 an % | 1513 Mittel bei Pumpe an °C | 1525 max °C |
|---|---|---|---|---|---|
| 19.10. | 18,7 / 22,2 / 26,2 | 8 | 0 | 27,9 | 61,5 |
| 20.10. | 19,5 / 20,6 / 24,1 | 40 | 0 | 28,4 | 61,5 |
| 21.10. | 19,4 / 19,9 / 20,4 | 8 | 0 | 28,4 | 58,0 |
| 22.10. | 18,4 / 19,3 / 20,4 | 10 | 0 | 29,6 | 62,0 |
| 23.10. | 17,6 / 18,6 / 19,9 | 50 | 0 | 30,3 | 61,5 |
| 24.10. | 17,5 / 18,5 / 19,5 | 44 | 0 | 29,5 | 57,0 |
| 25.10. | 17,0 / 18,4 / 21,6 | 51 | 0 | 29,9 | 57,0 |
| 26.10. | 18,0 / 20,0 / 24,3 | 57 | 0 | 29,1 | 57,5 |
| 27.10. | 17,2 / 18,7 / 20,0 | 28 | 0 | 29,2 | 57,5 |
| 28.10. | 17,0 / 18,5 / 19,6 | 37 | 0 | 29,6 | 58,0 |
| 29.10. | 17,3 / 18,7 / 20,7 | 58 | 0 | 30,0 | 57,5 |
| 30.10. | 17,7 / 18,8 / 19,6 | 75 | 0 | 29,6 | 57,5 |
| 31.10. | 18,0 / 19,3 / 21,6 | 43 | 0 | 29,8 | 57,0 |
| 01.11. | 18,8 / 19,6 / 22,2 | 67 | 0 | 29,6 | 57,5 |
| 02.11. bis 13:00 | 18,4 / 19,3 / 20,0 | 72 | 0 | 29,5 | 55,5 |

Im Fenster 19.10.-02.11. (4201 Punkte):
- Korrelation 1514 zu 1513 = 0,05, zu 1525 = 0,18. VF2 folgt also weder dem HK1-Betrieb noch dem WP-Vorlauf. [sicher]
- Mittelwert 1514 bei HK1-Pumpe an 19,01 °C (n = 1781), aus 19,63 °C (n = 2420). Der HK1-Betrieb heizt das Rohr nicht. [sicher]
- Über 54 HK1-Laufblöcke ab 30 min steigt 1513 im Mittel um 6,12 K, 1514 um 0,32 K. [sicher]
- 19707 = 1 in 10 von 27 218 Zeilen, immer nur Einzelpunkte im Abstand von Stunden bis Wochen, zuletzt 29.10. 10:45:01 mit 1514 = 18,9 °C (10:40 18,4, 10:50 18,7). Sieht nach kurzem Pumpenlauf als Festsitzschutz aus. [Vermutung] Der Kreis bewegt dabei kein warmes Wasser in VF2. [wahrscheinlich]

**Anstiege im Stillstand** (19706 = 0, 19707 = 0, 19659 und 19658 = -100 %, 1490 = 0):
| Zeit | 1513 °C | 1514 °C | 1525 °C |
|---|---|---|---|
| 31.10. 01:15:02 | 19,4 | 18,1 | 29,5 |
| 31.10. 03:00:01 | 23,7 | 21,4 | 28,0 |
| 01.11. 19:00:02 | 21,7 | 19,0 | 29,0 |
| 01.11. 20:00:01 | 24,4 | 21,0 | 27,5 |

- Der WP-Vorlauf kühlt dabei aus, ist also nicht die Quelle. Der Trockner- und der Waschmaschinenzähler zeigen in beiden Fenstern 0 kWh je Stunde (der Trocknerzähler zählt sonst: 29.10. 1,64 kWh). Damit sind diese Lasten als Raumwärmequelle wahrscheinlich raus. [wahrscheinlich] Der Holzofen ist nicht geprüft.
- Bei Pumpe aus: Pegelkorrelation 1514 zu 1513 = 0,50 (n = 2420), Korrelation der 30-min-Änderungen 0,29 (n = 2034). Anteil 1514 ab 22 °C: 6,2 %, ab 25 °C: 0,8 %. Spannweite 17,0-26,2 °C. [sicher]
- Deutung: warmes Wasser kommt im Stillstand über Schwerkraft durch die "zu" gemeldeten Mischer oder den Verteilerbalken an beide Fühler. [Vermutung] Alternative: Der Technikraum selbst wird wärmer. Das lässt sich nicht prüfen, weil es für den Raum keine Statistik gibt (`control_statistics` auf den Raumregler: "isn't chartable"). Live 12:07:45 UTC: Raum 20,0 °C, VF2 19,5 °C.
- Die Aussage der Vorbefunde "VF2 auf Raumniveau" gilt also nur meistens, nicht für die Spitzen bis 26,2 °C.

### 5. Antwort auf "ohne neuen Fühler sehen"
| Ziel | Mit dem Vorhandenen? | Warum |
|---|---|---|
| Puffer-Schichtung | **Nein** [sicher] | PF1/PF2/WPF liefern nichts. Kein anderer Fühler sitzt am Puffer (Inventar) |
| OG-Kreis in Betrieb | **Nein, und zurzeit gibt es nichts zu sehen** [wahrscheinlich] | HK2 steht seit Logbeginn (1479 und 1502 immer 0), OG ohne WP-Wärme (F62) |
| HK2-Rohr im Stillstand | **Ja, mit 1514** [sicher] | VF2 lebt, 5-min-Verlauf seit 30.07. liegt vor. Das zeigt die Anstiege aus Abschnitt 4 |

## Stichprobe
| Zeit | Quelle | Wert |
|---|---|---|
| 02.11. 13:03 | HoxPi 17386 / 17387 / 27494 | Rohwert 0 / 0 / 0 |
| 02.11. | Pi `/home/<user>/hoval-bridge/cache_last.json` | `regs/27493` = 32768, `regs/27494` = 0, keine Einträge für 17384-17387 |
| 02.11. 13:03 UTC+1 | HoxPi 1514 / 1513 / 1525 / 19706 / 19707 | 19,5 °C / 31,0 °C / 49,0 °C / 0 / 0 |
| 02.11. 12:07:17 UTC | Loxone Thermometer_Boiler_Oben | 47,375 °C, error 0 |
| 02.11. 12:07:19 UTC | Loxone Thermometer_HK1_UG_Vorlauf | 31,3125 °C (error 0 um 12:03:22 UTC) |
| 31.10. 03:00:01 | Volllogger `2026-10-31.csv.gz`, 1513 / 1514 / 1525 / 19706 | 237 / 214 / 280 / 0 |
| 29.10. 10:45:01 | Volllogger `2026-10-29.csv.gz`, 19707 / 1514 | 1 / 189 |

## Nebenbefund zum Auftrag
- **Reg 18760 ist nicht der HK1-Vorlauf-Ist.** Sie heißt "Anlage Vorlauftemperatur Heizen". Im Fenster liegt sie im Mittel 0,32 K an 1525 und 11,51 K neben 1513, bei laufender HK1-Pumpe 0,36 K zu 5,27 K (n = 1781). Live 02.11. 13:03: 18760 = 49,0, 1525 = 49,0, 1513 = 31,0. Der HK1-Ist ist 1513. [sicher]
- Das betrifft die Abnahme von 07-001 in `[lokaler Pfad]` ("HK1-Vorlauf-Ist (18760) < Soll"). Das Kriterium misst dort den falschen Fühler und sollte vor dem 07.11. auf 1513 umgestellt werden. [wahrscheinlich] Nur Hinweis, nichts geändert.

## Offen
1. Lebt der 1-Wire-Fühler? Gesucht wurde in Loxone-MCP (Struktur, Zustand, Statistik), `lox`-Werkzeug (auf diesem Rechner nicht installiert), Projektdateien, Doku, Fotos. Klären kann das nur die Live-Ansicht in Loxone Config oder eine Kachel.
2. Welches Kabel am HK2-Rohr ist welcher Fühler? Nur vor Ort zu klären.
3. Ursache der Stillstands-Anstiege: Schwerkraft durch den Mischer oder Raumwärme? Holzofen und Raumtemperatur im Technikraum fehlen im Verlauf.

## Was bringt uns das
- **Vorschläge, nichts davon umgesetzt:**
  1. Für die Puffer-Schichtung bleiben nur neue Fühler: 2 × 1-Wire (Vorschlag aus dem Inventar Abschnitt 4), oder das TTE-PS-Modul reaktivieren (Entscheidung der Betreiber, siehe `BAUTEILE_BEKANNT.md`).
  2. Den Anlegefühler "Rücklauf HK2 OG" aus dem Inventar streichen, solange HK2 stillliegt. Das spart einen Fühler ohne Informationsverlust.
  3. Beim nächsten Loxone-Umbau `Thermometer_HK2_OG_Vorlauf` sichtbar machen (Kachel, Statistik) und eine Woche gegen 1514 vergleichen. Dann ist lebt/tot entschieden und es gibt einen zweiten Stillstandsfühler. Kosten fast null. Skill `loxone-xml-umbau`, Backup vorher.
  4. Die Kacheln und Eingänge PF1/PF2/WPF ausblenden oder als "kein Fühler" beschriften, denn 0 °C führt in die Irre.
  5. Die zwei Formeln "Heizen/Kühlen" (Z. 10604, 10614) sind ohne Verbraucher und könnten beim Aufräumen weg.
- Die Stillstands-Anstiege lohnen eine Beobachtung, falls es Schwerkraft ist: Dann geht Pufferwärme ungeplant in die Rohre. Die Menge lässt sich aus diesen Daten nicht beziffern.

Loxone-Doku: [1-Wire Extension](https://www.loxone.com/dede/kb/1-wire-extension/), [Formel](https://www.loxone.com/dede/kb/formel/), [Intelligente Raumregelung](https://www.loxone.com/dede/kb/intelligente-raumregelung/), [Klima-Controller](https://www.loxone.com/dede/kb/klima-controller/). Links nicht einzeln aufgerufen.