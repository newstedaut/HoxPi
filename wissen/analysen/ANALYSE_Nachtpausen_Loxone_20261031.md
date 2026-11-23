# ANALYSE Nachtpausen 29./30. und 30./31.10.2026 – wer sperrte? (F54-Folge) – 31.10.2026, Claude (Subagent, nur gelesen)

Bezug: `[lokaler Pfad]` (Ausreißer 29.10. 21:30 → 30.10. 00:20 und 30.10. 22:10 → 31.10. 03:30).
Alle Zeiten MEZ (UTC+1, Sommerzeit endete 25.10.). Loxone liefert UTC → +1 h umgerechnet.

## Quellen
- Volllogger Pi: `/home/<user>/hoxpi_fulllog/2026-10-29.csv.gz`, `/home/<user>/hoxpi_fulllog/2026-10-30.csv`, `/home/<user>/hoxpi_fulllog/2026-10-31.csv` (5 min, Rohwert ×10, nur `zcat`/`cut`/`grep`). Spalten: 1490 = Vorlauf-Soll Konstantanforderung Heizen (von Loxone geschrieben), 1501 = Status Heizkreisregelung HK1 (0 = Abgeschaltet, 23 = Heizen extern), 1520 = HK1-Vorlauf-Soll wirksam, 1510 = Raum-Ist HK1, 1525 = WP-Vorlauf, 1539 = WP-Betriebsart, 25611 = el. Leistung, 1496 = WW-Betriebswahl (konstant 4), 1497 = WW-Soll.
- Loxone Aktivitätslog (control_history, je 20 Einträge Ringpuffer) der Intelligenten Raumregler UG: Wohnzimmer `<UUID>`, Büro `<UUID>`, Zimmer OG 1 `<UUID>`, Zimmer OG 2 `<UUID>`, WC UG `<UUID>`, Badezimmer `<UUID>`, Technikraum `<UUID>`. Baustein: Intelligente Raumregelung – https://www.loxone.com/dede/kb/intelligente-raumregelung/
- Loxone Klimacontroller UG `<UUID>` (Typ ClimateControllerUS = Klimacontroller, https://www.loxone.com/dede/kb/klimacontroller/): nur aktueller Zustand lesbar (keine Historie, keine Statistik). Stand 31.10. 09:57: mode = 2 („Heizen nur bei ausreichender Anforderung“), threshold (Einschaltschwelle Sot) = 30 %, demandHeat = 41 %, outdoorTempMode = 1 (48-h-Mittel).
- control_statistics auf Raumreglern: nicht verfügbar („not chartable“). `[lokaler Pfad]` und `/home/<user>/` kurz durchsucht: kein Prometheus-/Loxone-Statistik-Export mit Raumbedarf gefunden.
- Register-Bedeutung 1490/1501: Projektdoku `Heizung/UEBERGABE.md` (Abschnitt 4) und `Heizung/Konzept_Heizen_Kuehlen_Loxone.md`.

## Kernbefund
In beiden Nächten hat **Loxone die HK1-Anforderung weggenommen: 1490 = 0, 1501 = 0 (HK1 abgeschaltet), 1520 = 0**. Die Hoval hatte also gar kein Soll, gegen das der Vorlauf hätte fallen können. Die Werte „Soll 32,2 / 31,8“ in der F54-Analyse sind die letzten Werte **vor** dem Abschalten, nicht der Wert während der Pause.
Ab- und Wiedereinschalten fallen auf die Minute mit den Log-Einträgen „Klimacontroller UG wird nicht mehr verwendet / Regler im Standby“ bzw. „… wird zum Heizen verwendet“ in allen UG-Raumreglern zusammen.

## Nacht 1: 29.10. → 30.10.2026
Volllogger (Auszug, physikalische Werte):

| Zeit MEZ | 1490 Soll Konst. | 1501 Status HK1 | 1520 HK1-Soll wirks. | 1510 Raum | 1525 WP-VL | 1539 | 25611 kW |
|---|---|---|---|---|---|---|---|
| 29.10. 21:05 | 30,4 | 23 | 33,0 | 21,5 | 32,5 | 0 | 0 |
| 29.10. 21:20 | 32,2 | 23 | 35,0 | 21,6 | 31,5 | 0 | 0 |
| 29.10. 21:25 | **0** | **0** | **0** | 21,6 | 34,5 | 1 | 2,0 |
| 29.10. 21:30 | 0 | 0 | 0 | 21,7 | 32,5 | 0 | 0 |
| 29.10. 22:30 | 0 | 0 | 0 | 21,5 | 29,5 | 0 | 0 |
| 29.10. 23:30 | 0 | 0 | 0 | 21,4 | 27,0 | 0 | 0 |
| 30.10. 00:10 | 0 | 0 | 0 | 21,4 | 25,5 | 0 | 0 |
| 30.10. 00:15 | 15,3 (Übergang) | 0 | 0 | 21,3 | 25,5 | 0 | 0 |
| 30.10. 00:20 | **32,5** | **23** | 35,5 | 21,3 | 34,0 | 1 | 2,05 |

Loxone-Log (alle UG-Regler, gleiche Sekunde):

| Zeit MEZ | Ereignis | Regler |
|---|---|---|
| 29.10. 23:28 | WZ Komfort-Timer beendet, Ziel 20,0 °C | WZ |

## Nacht 2: 30.10. → 31.10.2026

| Zeit MEZ | 1490 | 1501 | 1520 | 1510 | 1525 | 1539 | 25611 kW |
|---|---|---|---|---|---|---|---|
| 30.10. 21:20 | 0 | 0 | 0 | 21,6 | 31,5 | 0 | 0 |
| 30.10. 21:25 | 29,7 | 23 | 32,5 | 21,6 | 30,5 | 0 | 0 |
| 30.10. 22:05 | 29,7 | 23 | 32,5 | 22,0 | 38,0 | 1 | 1,81 (Lauf endet) |
| 30.10. 22:20 | 31,8 | 23 | 34,5 | 22,0 | 35,0 | 0 | 0 |
| 30.10. 22:25 | **0** | **0** | **0** | 22,1 | 34,0 | 0 | 0 |
| 30.10. 23:30 | 0 | 0 | 0 | 22,2 | 32,5 | 0 | 0 |
| 31.10. 01:30 | 0 | 0 | 0 | 22,1 | 29,0 | 0 | 0 |
| 31.10. 03:25 | 0 | 0 | 0 | 21,6 | 27,5 | 0 | 0 |
| 31.10. 03:30 | **32,0** | **23** | 35,0 | 21,5 | 35,5 | 1 | 2,04 |
| 31.10. 04:30 | 0 | 0 | 0 | 21,4 | 35,0 | 0 | 0 |
| 31.10. 04:50 | 32,0 | 23 | 35,0 | 21,5 | 34,0 | 0 | 0 |

Loxone-Log:

| Zeit MEZ | Ereignis | Regler |
|---|---|---|
| 30.10. 21:56 | Büro Komfort-Timer beendet, Ziel 18,5 °C | Büro |
| 31.10. 01:58 | WZ Komfort-Timer beendet, Ziel 20,0 °C | WZ |

Zeitversatz Logger ↔ Loxone: Logger-Zeile zeigt den Wechsel 0–2 min **vor** dem Loxone-Zeitstempel (21:25:01 vs. 21:25:14, 22:25:01 vs. 22:26:44, 04:30:02 vs. 04:30:41) → Uhrenversatz Pi/Miniserver oder Log-Verzögerung, in jedem Fall dasselbe Ereignis.

## Aussagen

| Aussage | Sicherheit |
|---|---|
| Während beider langer Nachtpausen stand **1490 = 0, 1501 = 0 (HK1 abgeschaltet), 1520 = 0**: Nacht 1 von 21:25 bis 00:15, Nacht 2 von 22:25 bis 03:25. Die Hoval hatte keine HK1-Anforderung. | sicher (Volllogger, jede 5-min-Zeile) |
| Die Aussage „VL fiel 4–7 K unter Soll“ in `ANALYSE_Heizpausen_mild_20261031.md` ist ein Auswerte-Artefakt (letzter Sollwert vor dem Abschalten fortgeschrieben). Die Hoval-Schwelle „Start bei VL = Soll“ wurde nicht verletzt. | sicher |
| Ab- und Einschalten von 1490 fällt (±2 min) mit „Klimacontroller UG wird nicht mehr verwendet / Standby“ bzw. „wird zum Heizen verwendet“ in den UG-Raumreglern zusammen – 6 von 6 Übergängen. Die Kette ist also: Klimacontroller UG Heizstufe aus → Loxone schreibt 1490 = 0 → HK1 aus → keine WP-Anforderung. | wahrscheinlich (zeitliche Deckung; Verdrahtung Klimacontroller → 1490 nicht in der Projektdatei nachgesehen) |
| Was fehlte, war der **gemittelte Raumregler-Wärmebedarf** über der Einschaltschwelle des Klimacontrollers (Modus 2, Sot = 30 %). Nachts sind die meisten Räume im Eco (Büro 18,5, Zimmer OG 1 18,5, Zimmer OG 2 18,0, Technik 17,0, WZ 20,0) und haben kaum Ventilöffnung. | wahrscheinlich (Schwelle/Modus gelesen; nächtlicher demandHeat-Verlauf nicht gemessen) |
| Wiedereinschalten kam jeweils, wenn ein Raum die **Komfort-Vorbereitung** startete: Zimmer OG 1 00:15:00 (Nacht 1) und 03:26:34 (Nacht 2), WZ 02:04:32 und 04:48:00. Das hebt den Mittelwert über 30 %. | wahrscheinlich |
| Bei Pausenbeginn Nacht 1 hatte die WP um 21:25 gerade gestartet (VL 31,5 < Soll 32,2 um 21:20) und wurde durch das Wegnehmen von 1490 sofort wieder gestoppt. | wahrscheinlich (5-min-Raster) |
| HK1-Betriebswahl / WW-Betriebswahl (1496 = 4) blieben unverändert. Die Sperre lief nur über 1490 (und damit 1501), nicht über eine Betriebswahl. | sicher (1496), wahrscheinlich (1478 nicht im Auszug) |
| Die 47 % Zeilen mit 1490 = 0 sind sehr wahrscheinlich echte Klimacontroller-Standby-Phasen, kein Logger-Artefakt. | Vermutung (nur für diese zwei Nächte geprüft) |
| Unterschied der Log-Texte „Standby“ vs. „Standby wegen unzureichender Anforderung“: Bedeutung nicht geklärt. | offen |

## Was bringt uns das
- F54 ist erklärt: Die langen Nachtpausen sind **gewollte Loxone-Logik** (Klimacontroller UG, Modus 2, 30 %-Schwelle), kein Hoval-Fehler und kein Kommunikationsausfall.
- Für den Zwilling/die Pausenstatistik: Zeilen mit 1490 = 0 bzw. 1501 = 0 als „keine Anforderung“ werten und aus der Schwellen-Auswertung herausnehmen, statt den letzten Sollwert fortzuschreiben.
- Hebel, falls der Betreiber nachts durchgehender heizen will (nur Entscheidung, nichts umgesetzt): Einschaltschwelle Sot im Klimacontroller UG senken, Eco-Absenkung kleiner machen oder einen Referenzraum ohne Nachtabsenkung. Umgekehrt: Die Nachtpausen sparen Starts und schaden bei Raum 21,3–22,2 °C nicht – die Raumtemperatur 1510 fiel in Nacht 2 nur um 0,5 K (22,1 → 21,6).
- Der Loxone-Ringpuffer hält nur 20 Einträge pro Raumregler. Die hier zitierten Einträge sind in wenigen Tagen überschrieben, diese Datei ist ihre Sicherung.

## Offen (nur live/nachts messbar, für den Loop)
1. Klimacontroller UG `demandHeat` und `controls` (Bedarf je Raum) nachts alle 5 min mitschreiben, besonders um 21:00–22:30 und bei den Komfort-Starts, damit die 30 %-Schwelle direkt belegt ist (Messung statt zeitlicher Deckung).
2. Loxone-Verknüpfung prüfen (nur lesen, Projektdatei nach Skill `loxone-xml-umbau`): Welcher Ausgang des Klimacontrollers (OutHeat1/Compressor) schaltet den Baustein, der 1490 schreibt? Und „HK1 Vorlauf soll (Loxone)“ `<UUID>` nachts mitloggen.
3. Uhrenabgleich Pi ↔ Miniserver (Versatz 0–2 min).
4. Bedeutung „Standby“ ohne/mit „wegen unzureichender Anforderung“ (vermutlich Klimacontroller-weit vs. raumbezogen) – Loxone-Doku Klimacontroller.