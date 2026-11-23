# F54 Rest – warum ist OutHeat1 (→ Reg 1490) zeitweise 0? Live-Momentaufnahme 31.10.2026 ~11:55 MEZ

Orchestrator 31.10.2026 11:54-Lauf, nur lesend (Loxone-MCP `control_state`, HoxPi-MCP `read_register`). Nichts geändert.
Vorlauf: `[lokaler Pfad]` (Kette OutHeat1 → Multiplexer → Formel → AMQ46/Reg 1490),
`[lokaler Pfad]`.
Loxone-Doku Klimacontroller: https://www.loxone.com/dede/kb/klimacontroller/

## Messung (Zeitstempel Loxone-State 31.10.2026 10:55:10 UTC = 11:55:10 MEZ; HoxPi gelesen ~11:57 MEZ)

| Größe | Wert | Quelle |
|---|---|---|
| Klimacontroller UG `mode` | 2 (Heizen nur bei ausreichender Anforderung) | Loxone `control_state` <UUID> |
| `threshold` | 30 | dto. |
| `demandHeat` | **13** | dto. |
| `demandCool` / `stage` | 0 / 0 | dto. |
| `maximumTempHeating` / `actualOutdoorTemp` | 17 / 6,8 °C | dto. |
| Raumregler mit demand = 1 | **WC UG (21,9 °C), Büro (21,4 °C)** – 2 von 8 | `controls`-Liste + `tempActual` |
| Raumregler mit demand = 0 | WZ 22,3 · Bad 23,5 · Zimmer OG 1 21,4 · Zimmer OG 2 20,9 · Hütte 18,1 · Technik 20,7 | dto. |
| Reg 1490 (HK1-Soll Konstantanf.) | **0,0** | HoxPi `read_register` |
| Reg 1501 (Status HK-Regelung) | 0 = Abgeschaltet | HoxPi |
| Reg 1525 (WEZ-/WP-VL) | 43,5 °C (Nachlauf nach Heizlauf ab ~11:00) | HoxPi |

## Befund
- **sicher (Momentaufnahme):** demandHeat 13 < threshold 30 im Modus 2 ⇒ Klimacontroller gibt keine Heizanforderung, 1490 = 0, 1501 = 0. Genau das Bild der Nachtpausen, jetzt am Tag.
- **wahrscheinlich:** Das ist der allgemeine Pausenmechanismus bei mildem Wetter: Heizung läuft nur, solange die Raumregler zusammen ≥ 30 % Anforderung liefern. Fallen genug Räume (nach Heizlauf/Sonne) aus der Anforderung, setzt Loxone 1490 = 0, unabhängig von der Hoval-Hysterese (V129).
- **Vermutung:** WC UG (Raumregler AMode fest 3, siehe F22) liefert dauerhaft Anforderung und trägt so einen Grundanteil zu demandHeat bei. Wie Loxone demandHeat genau gewichtet (Räume gleich oder nach Bedarfsstärke), ist offen: 2/8 Räume = 25 %, gemeldet 13.

## Was bringt uns das
Für den Zwilling: Pausenbeginn/-ende = demandHeat kreuzt 30 % (Loxone) **oder** VL-Hysterese der Hoval (V129), je nachdem, was zuerst greift. Die Schwelle 30 % ist der Hebel für Pausenlänge – Entscheidung nur durch der Betreiber, nichts geändert.

## Offen (für „fertig, wenn“)
Zeitreihe demandHeat/threshold gegen 1490 über mindestens eine Nacht (Loop, nur lesen) – der Loxone-MCP hat für ClimateControllerUS keine History (`control_history` abgelehnt), also nur per Mitschreiben.