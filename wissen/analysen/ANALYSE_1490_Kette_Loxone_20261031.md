# F54 Rest: Welcher Loxone-Ausgang schreibt Reg 1490? (Orchestrator 31.10.2026 11:00)

Quelle: `[lokaler Pfad]` (neuester Projektstand, 25.10.2026 11:05), nur gelesen.

## Kette (Projektdatei, sicher)
| Schritt | Baustein (Zeile) | UUID Ausgang/Eingang | Rolle |
|---|---|---|---|
| 1 | HVACController "Klimacontroller UG" / Titel "Klimacontroller HC1" (Z. 13279) | Ausgang `OutHeat1` 21fab011-0110 (Z. 13315) | Heizanforderung 1 |
| 2 | AnalogMultiplexer "Sollwert Heizen 1490" (Z. 13465) | Select <- OutHeat1 (FLG 2); Input1 <- Heatmixer AQf 21fab011-00c6 | OutHeat1 = 0 -> AQ = 0; = 1 -> Heatmixer-Soll |
| 3 | Heatmixer2 "Vorlautemperatur HC1 - Fussboden Heizen+Kuehlen" (Z. 13350) | AQf 21fab011-00c6 (Z. 13370) | Vorlauf-Soll aus Heizkurve |
| 4 | Formel "1490 inkl. Ofen-Nachlauf (min. 24 C)" (Z. 13772) | I1 <- Multiplexer AQ 21fab011-00bb; I2 Ofen; I3 Monoflop Kurzlaufschutz 21fab040-0045; I4 VL-Ist 21fab040-0053 | `IF(I2>0;MAX(I1;24);IF(I1>0;I1;IF(I3>0;MAX(I4;20);0)))` |
| 5 | OutputRef "Sollvorlauftemperatur Heizen HC1" (Z. 13826) | AQ 21fab011-010f | Verweis auf AMQ46 |
| 6 | ModbusAActor AMQ46 (Z. 3448) | ModbusAddress 1490, Cmd 6, RepeatRate 300 s | schreibt Reg 1490 |

## Folgerung
- **sicher (Projektdatei):** 1490 = 0 genau dann, wenn Klimacontroller UG `OutHeat1` = 0 UND kein Ofen (I2) UND kein laufender Kurzlaufschutz (I3). Die Nachtpausen 29./30. und 30./31.10. (1490/1501/1520 = 0) sind damit der Klimacontroller-Ausgang OutHeat1 = 0.
- **wahrscheinlich:** Live-Miniserver entspricht dem Stand 25.10. (seitdem kein neuer UMBAU_stand_*.Loxone im Ordner).
- **offen (Loop, nachts, nur lesen):** warum OutHeat1 nachts 0 wird - demandHeat/Bedarf je Raum gegen Schwelle (Modus 2, 30 %).

## Was bringt uns das
Der Pausen-Ausloeser ist eindeutig ein einzelner Loxone-Ausgang. Fuer den Zwilling reicht ein Signal: OutHeat1 (bzw. 1490 > 0). Ein Hebel waere nur die Klimacontroller-Schwelle/der Modus - Entscheidung der Betreiber, nichts geaendert.

Loxone-Doku: Klimacontroller https://www.loxone.com/dede/kb/klimacontroller/ · Analog-Multiplexer https://www.loxone.com/dede/kb/analogmultiplexer/ · Formel https://www.loxone.com/dede/kb/formel/ · Mischerregler (Heatmixer) https://www.loxone.com/dede/kb/mischerregler/