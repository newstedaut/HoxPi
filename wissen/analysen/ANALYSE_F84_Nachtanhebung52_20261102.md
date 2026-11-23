# ANALYSE F84 - "Nachtanhebung 52 °C" auf Register 1497 (02.11.2026)

Claude, Subagent, nur gelesen. An Anlage, Bussen, Loxone und Pi nichts geändert. Daten bis 02.11. 10:56.

## Kernaussage
3. **Seit 24.10.: 3 von 9 Nächten, 1 Ladung, 2,12 kWh_el. Keine spätere Ladung entfiel.** [sicher: Zählung; wahrscheinlich: kein Entfall] Der Bericht klang öfter, als es war: Journal Z. 35 und Z. 60 meinen beide dieselbe Nacht 01./02.11.
4. **Weglassen spart netto etwa nichts.** Lassen und im Stundenbericht umbenennen. [wahrscheinlich]

## Kette im Projekt
`[lokaler Pfad]` (Zeile für Zeile gleich mit `[lokaler Pfad] Config\Projects\Fam der Betreiber UMBAU.Loxone`). Der Miniserver fährt laut Z. 155 einen älteren Stand, die Kette ist dort gleich. [wahrscheinlich: Stand; sicher: gleiche Kette in den Dateien]

| Zeile | Baustein | Wirkung |
|---|---|---|
| 16303 | [Schwellwertschalter](https://www.loxone.com/dede/kb/schwellwertschalter/) "WW unten fällt unter 40 (Impuls)", dazu Stufen 35/30 (ODER Z. 16348) | Impuls bei SF2 unter Schwelle |
| 16339, 16357 | [ODER](https://www.loxone.com/dede/kb/logik/) "Zapfung-Impulse (40) + Abendfenster 17-22", "gesamt" | sammelt die Impulse |
| 16378, 16384 | [Monoflop](https://www.loxone.com/dede/kb/monoflop/) "WW Nachlade-Boost aktiv (90 min)", `Time Def="5400"` | Q = 1 für 90 min, **ohne Zeitfenster** |
| 16396, 16405-16428 | [UND](https://www.loxone.com/dede/kb/und/) + [Schaltuhr](https://www.loxone.com/dede/kb/schaltuhr/) "WW Kick-Freigabe" 300-1320 | Kick 57 nur 05:00-22:00 (seit 08.10.) |
| 16432 | [Formel](https://www.loxone.com/dede/kb/formel/) "WW-Soll final": `MAX(MAX(MIN(I1;52+5*I4);I2*52);I3*57)` | I2 = Boost -> 52 |
| 17027 | Ausgangsverweis "Normal-Temperatur Warmwasser" | schreibt 1497 |

Der Monoflop läuft rund um die Uhr, nur der Kick hat ein Fenster. Nachts kommt deshalb 52 ohne 57. Geladen wird dann nur, wenn 1500 schon bei etwa 47 °C oder darunter liegt (Start bei 1497 - 4,7 bis -5 K, F75/F79). [sicher: Logik; wahrscheinlich: Schwelle]

## Nacht-Tabelle (22:00-05:00, `ww_hires.csv`, Rohwerte /10)
| Nacht | 1497 = 52 von-bis | 1500 Beginn | SF2 Beginn | Ladung durch 52? | kWh_el | Nächste Ladung | Entfiel dadurch eine? |
|---|---|---|---|---|---|---|---|
| 24./25.10. | keine | - | - | nein (01:09 bei Soll 50, 45,2 °C) | 1,63 (Soll 50) | - | - |
| 25./26.10. | keine | - | - | nein (22:57 bei Soll 50, 45,1 °C) | 1,52 (Soll 50) | - | - |
| 26./27.10. | keine | - | - | keine Ladung | 0 | - | - |
| 27./28.10. | keine | - | - | keine Ladung | 0 | - | - |
| **28./29.10.** | **<MAC>** | **45,5** | 40,0 | **ja, <MAC>, 45,5 -> 51,7** | **2,12** | 29.10. 06:41 (Kick 57, SF2-Impuls 06:40:53) | nein [wahrscheinlich] |
| 29./30.10. | keine | - | - | nein (02:17 bei Soll 50, 45,1 °C) | 1,60 (Soll 50) | - | - |
| **30./31.10.** | **<MAC>** | **47,7** | 40,0 | nein (Minimum 47,3) | 0 | 31.10. 08:46 (Soll 50, 45,1 °C) | nein [sicher] |
| 31.10./01.11. | keine | - | - | keine Ladung | 0 | - | - |
| **01./02.11.** | **<MAC>** | **48,7** | 40,0 | nein (Minimum 47,3) | 0 | 02.11. 05:40 (Soll 50, 45,1 °C) | nein [sicher] |

- Alle drei Beginne: SF2 steht genau bei 40,0 °C. [sicher]
- Volllogger-Gegenprobe: 01.11. 23:25:01 1497 = 500, 1500 = 492, 27483 = 426; 23:30:01 1497 = 520, 1500 = 488, 27483 = 389, 1539 = 0, 25611 = 0. 02.11. 01:05:02 1497 = 520; 01:10:01 1497 = 500, 1500 = 473. 28.10. 23:15:02 1497 = 500; 23:20:02 1497 = 520, 1500 = 451, 1539 = 4, 25611 = 468. [sicher]
- 28.10.: kWh_el aus P_el integriert (1-min-Raster), Q 27489 von 40099 auf 40106 = 7 kWh_th, also AZ grob 3,3 (Zähler nur ganze kWh). [wahrscheinlich]
- 01.-23.10. gab es 5 weitere Phasen mit Beginn 22:00-04:30, nicht einzeln geprüft (f84_f_detail.py). [sicher: Anzahl]

## Warum 100 statt 90 min in der Nacht 01./02.11.
Der Monoflop läuft **doch nach**: jede weitere Stufe startet die 90 min neu. 01.11.: letzte Querung SF2 < 30 um 23:39:51, Ende 01:08:51 = 89 min. In 7 von 8 Phasen mit mehreren Stufen liegt das Ende 88,3-90,3 min nach der letzten Querung (18.10., 21.10., 22.10., 27.10., 29.10., 31.10. 11:28, 01.11.). [sicher: Messung] Ausnahme 31.10. 19:49: Ende 89 min nach Beginn. Dort stand das Abendfenster schon auf 1 und verschluckt die Impulse (Notiz Z. 16849). [wahrscheinlich] Die Notiz Z. 16378 "Nicht retriggerbar" stimmt damit nicht. Die Loxone-Doku dazu konnte ich nicht abrufen (403 auf Monoflop und Schwellwertschalter; nur die Formel-Seite war lesbar, die anderen Links stammen aus der Projektdoku).

## Abweichungen vom Projekttext (Soll 50, nachts 45, PV 57)
- **Dazu tagsüber 52** 13:00-16:00 aus dem Kalender. Das fehlt im Projekttext. [sicher]
- **PV 57:** seit 24.10. keine Smart-Grid-Phase, 57 nur noch als Kick (F74, F76). [sicher nach F74]
- **Veraltete Notizen in der Datei:** Z. 16252 "Nachlade-Boost 52, 05-22 Uhr" (nur der Kick hat das Fenster), Z. 17027 "45 Nacht". Z. 16378 siehe oben. [sicher]

## Was bringt uns das
- **Die Meldung ist kein Fehler.** Vorschlag für den Stundenbericht: "Boost 52 nach Zapfung (SF2 < 40), ohne Kick". Das spart die wiederkehrende Nachfrage.
- **Weglassen (nur Vorschlag, nichts umgesetzt):** UND mit Schaltuhr "WW Kick-Freigabe" vor den Monoflop-Trigger Z. [Nummer], dann kein Boost 22:00-05:00.
  - 2 von 3 Nächten seit 24.10.: keine Änderung, es lud ohnehin nichts. [sicher]
  - 28.10.: 1500 stand bei 45,5-45,6, Start bei Soll 50 ab etwa 45,3. Die Ladung käme bei 0,55-0,83 K/h (F79) etwa 15-30 min später und endete bei rund 49,7 statt 51,7. Das sind etwa 0,9 kWh_th (0,47 kWh/K, F1) oder etwa 0,3 kWh_el einmalig, die dann früher nachgeladen werden. Netto etwa 0. [Vermutung]
- **Empfehlung: lassen.** Rückweg, falls doch umgebaut: Eingang Z. 16380 wieder direkt auf `<UUID>`. Vorher Backup und Skill `loxone-xml-umbau`.

## Offen
- Projektanweisung "nachts 45" und die Notizen Z. 16252, 16378, 17027 korrigieren: nicht geändert, Entscheidung bei der Betreiber.
- Knappe Fälle: 02.11. 01:05-01:11 und 31.10. 03:10 stand 1500 bei 47,3 unter Soll 52 ohne Start. Die genaue Schwelle bleibt offen (4,7 K reicht nicht immer, F79).
- Zapfungen sind aus SF2 abgeleitet, nicht direkt gemessen.
- Miniserver-Stand nicht zurückgelesen; `system_status` zeigt keinen Projektstand.

## Quellen (nur gelesen)
- Pi: `/home/<user>/hoxpi_fulllog/ww_hires.csv`, Kopie `[lokaler Pfad]`; Volllogger `[lokaler Pfad]` ... `2026-11-02.csv`; `[lokaler Pfad]`.
- Skripte: `[lokaler Pfad]`.