# F72: Raumregler averageOutdoorTemp -1,7 C gegen 48-h-Mittel (OR 02.11.2026 05:10, nur gelesen)

## Frage
Die Raumregler zeigten um 02:04Z averageOutdoorTemp -1,7 C (Bitte an den Loop im OR-Eintrag 03:30). Greift dieser Wert in die Kuehlfallen-Logik ein, und stimmt die 48-h-Aussentemperatur, an der die Heizsaison haengt?

## Datenquelle
- Loxone-MCP `control_state`, 02.11. 04:09-04:11Z: averageOutdoorTemp aller Raumregler, operatingMode aller Raumregler, Klimacontroller UG (`<UUID>`).
- Volllogger `~/hoxpi_fulllog/2026-10-31.csv` bis `2026-11-02.csv`, Spalte 1477, letzte 576 Punkte (31.10. 05:15 bis 02.11. 05:10), Script `[lokaler Pfad]`.
- Verdrahtung: `[lokaler Pfad]`, `ANALYSE_HK1_Anforderungspause_20261024.md`.

## Ergebnis
| Regler | averageOutdoorTemp | operatingMode | Mode-Eingang Heizsaison |
|---|---|---|---|
| Wohnzimmer, Buero, Zimmer OG 1, Zimmer OG 2, Technikraum, Huette | -1000 | 1 | verbunden |
| Badezimmer | -1,7 | 1 | nicht in der Liste der sechs |
| WC UG, Garage | -1,7 | 4 | nicht verbunden (WC UG: Umbau 01.11. Def=4) |

- Klimacontroller UG `actualOutdoorTemp` 5,64375 C gegen selbst gerechnetes 48-h-Mittel 1477 = 5,66 C: Differenz 0,02 K. Der Klimacontroller rechnet das 48-h-Mittel korrekt. **[sicher, dieser Zeitpunkt]**
- Heizsaison-Schwelle 18/19 C auf diesem Mittel: 5,64 C liegt klar darunter, Modus 2 = nur Heizen, stage 2, demandHeat 49. **[sicher]**
- -1000 steht genau bei den sechs Reglern mit Heizsaison-Eingang, -1,7 bei den drei anderen. **[sicher als Muster, ein Zeitpunkt]**
- -1,7 C ist nicht das 48-h-Mittel (5,66) und nicht die Aussentemperatur (3,0 C um 05:10); der Wert stand um 02:04Z und 04:10Z gleich. **[sicher]** Herkunft: **[Vermutung]** interner Wert der Regler ohne eigene Modusvorgabe.
- Kein Regler laeuft im freien Automatik-Modus: operatingMode 1 und 4 sind beide heiz-gebunden (1 = Automatik nur Heizen, 4 = manuell Heizen, Bedeutung laut Structure File). **[wahrscheinlich]** Damit greift -1,7 C nicht in Heizen/Kuehlen ein. **[wahrscheinlich]**

## Was bringt uns das
Die Kuehlfallen-Logik haengt am richtigen Wert (5,64 C vom Klimacontroller), die -1,7 C sind kein Fehler der Heizsaison. Die Loop-Bitte vom 03:30 ist damit erledigt. Doku Klimacontroller: https://www.loxone.com/dede/kb/klima-controller/

## Offen
- Verlauf von -1,7 C (eingefroren oder langsam) ist nur mit einem zweiten Tag belegbar; `history` lieferte keine Aenderungen.
- Vor dem ersten Kuehltag 2027 pruefen, ob Bad/WC UG/Garage (kein Heizsaison-Eingang) den Wert im Modus 0 je nutzen wuerden (F22).