# F4 Abnahme Kühlfalle – Zwischenstand 24.10.2026 06:00 (Orchestrator)

Katalogfrage F4 (`[lokaler Pfad]`). Nur gelesen: Loxone-MCP, HoxPi-Volllogger, Loxone-Raumlogger. Nichts geschrieben.
Vorlauf: `[lokaler Pfad]`

## Ergebnis bisher
- **Heizanforderung bei warmem Raum blieb bestehen:** HK1 1501 = 23 (Loxone-Anforderung) von 21:00 bis 22:45 bei Raumwert 1510 = 22,6–24,6 °C. Kein Rückfall in Kühlen. Dass Loxone dabei überhaupt anfordert, ist Katalog F18 (erledigt, nur Pumpe, ~0,08 kWh/Tag).
- **Lücke:** Zwischen 19:54 und 05:56 kein Raumlogger (Loxone-MCP-Verlauf erst ab 03:54 UTC, IRR nicht chartbar). Kühlmodus *in* der Nacht daher nicht lückenlos ausgeschlossen (Vermutung: nein, weil Mode 1 Kühlen gar nicht zulässt).

## Volllogger 23.10./24.10. (Auszug, 15-min-Raster; 1510/1520 ×10)
| Zeit | 1510 Raum | 1501 HK1 | 1520 Soll | 1539 | 31708 |
|---|---|---|---|---|---|
| 23.10. 20:45 | 22,0 | 0 | 0 | 0 | 0 |
| 23.10. 21:15 | 23,8 | 23 | 30,0 | 0 | 159 |
| 23.10. 22:15 | 24,4 | 23 | 32,5 | 0 | 161 |
| 23.10. 23:00 | 24,7 | 0 | 0 | 0 | 0 |
| 24.10. 03:00 | 23,5 | 0 | 0 | 0 | 0 |
| 24.10. 05:30 | 22,5 | 6 | 54,0 | 4 (WW) | 285 |
Hinweis: Zeilen zur vollen Stunde (17:00, 18:00, 19:00, 20:00) zeigen 1501/1520/1539 = 0 mitten in Anforderungsphasen – Verdacht auf Logger-Artefakt zur vollen Stunde, nicht als Abschaltung werten.

## Noch offen bis „erledigt“
1. Folgetag 24.10.: 0 h unter 21,0 °C im WZ, Heizanforderung kommt unter Soll wieder. **Raumlogger läuft dafür** (`py -3 [lokaler Pfad] --runden 200 --abstand 300`, gestartet 24.10. 05:56, PID 16844, Ende ~22:35) → `[lokaler Pfad]`.
2. Auswertung im nächsten Lauf nach ~22 Uhr: min. WZ-Temperatur, erste `demand` = 1 im WZ nach Abkühlen, `currentMode` nie −1.

**Was bringt uns das:** Die Kühlfalle scheint mit Mode 1 behoben – nach dem Ofenabend blieb jeder UG-Regler im Heizen. Mit dem Folgetag-Log ist die Abnahme heute Abend formal abschließbar.

## Endabnahme 24.10.2026 22:05 (Orchestrator) - Kuehlfalle behoben
Daten: `[lokaler Pfad]`, <MAC>, 192 Runden x 9 Raeume, keine Luecke > 7 min. Skript `[lokaler Pfad]` (wiederholbar). Leistung WP aus HoxPi-Prometheus `p_el_kw`.

| Raum | Zeilen | opMode/curMode | demand 1 | min Ist | max Ist | Zeilen > 22,5 C | davon nicht Heizen |
|---|---|---|---|---|---|---|---|
| Wohnzimmer | 192 | 1/1 | 113 | 20,9 (15:56) | 22,9 (05:56) | 55 | 0 |
| Buero | 192 | 1/1 | 46 | 21,2 (11:21) | 23,3 (21:51) | 17 | 0 |
| Technikraum | 192 | 1/1 | 6 | 20,2 | 20,81 | 0 | 0 |
| Zimmer OG 1 | 192 | 1/1 | 55 | 21,0 | 21,6 | 0 | 0 |
| Zimmer OG 2 | 192 | 1/1 | 91 | 20,2 | 20,9 | 0 | 0 |
| Badezimmer | 192 | 1/1 | 181 | 22,0 | 23,2 | 98 | 0 |
| WC UG | 192 | 3/4 (Sonderfall F22) | 192 | 21,5 | 22,1 | 0 | 0 |

- **Sicher:** kein UG-Raumregler (Mode 1) war je im Kuehlmodus, `demand` nie -1, auch bei 170 Zeilen ueber 22,5 C.
- **Sicher:** WZ fordert nach dem Abkuehlen wieder an: 11:31 (Ist 21,9 / Soll 21,5), 12:31 (21,7) - Anforderung dann durchgehend bis 21:26 (22,0).
- **Abweichung (Proxy-Kriterium):** WZ 20,9 C 15:56-16:06 (3 Zeilen, 15 min) trotz demand 1. Davor WW-Ladung 14:25-15:05 (P_el 2,4-4,3 kW, WW-Vorrang, HK1-Pumpe aus) und Pause 15:08-15:40 (HKA59-Wartezeit), Heizblock 15:40-16:08. Ursache = WW-Vorrang/Takt, nicht Kuehlfalle (wahrscheinlich).
- **Urteil:** F4 erledigt. Rest 21:51-22:35 nur Nachtrag.
