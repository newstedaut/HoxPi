
Quellen (nur lesend): Loxone-MCP `control_find`/`control_state`/`control_statistics` (Baustein "Zirkulationspumpe", InfoOnlyDigital, Raum Zentral, UUID <UUID>, Statistik 19.-22.10.),
Pi `~/hoxpi_fulllog/ww_hires.csv` (60 s). Skript `Emulation\or_zirk_20261022_1900.py/.out`. Hoval-Register 19756 "Warmwasser-Zirkulationspumpe" = 0 (Hoval steuert sie nicht).

## Was vorhanden ist (sicher, aus Loxone)
| Baustein | Raum | Typ |
|---|---|---|
| Zirkulationspumpe (Ausgangsanzeige) | Zentral | InfoOnlyDigital |
| Zirkulation Hand (5 min, schaltet selbst aus) | Technikraum | TimedSwitch |
| WC UG / Kreis "Zirkulation" (AI2) | WC UG | Kreis im Lichtbaustein (Präsenz) |

## Laufverhalten 19.-22.10. (sicher, Loxone-Statistik)
| Tag | Pulse | Laufzeit |
|---|---|---|
| 19.10. | 47 | 215 min |
| 20.10. | 28 (Lücke 06:45-13:45) | 130 min |
| 21.10. | 37 | 164 min |
| 22.10. bis 18:55 | 23 | 99 min |
- 44 von 131 Pulsen starten < 5 min nach dem Ende des vorigen, 74 < 15 min, 84 < 20 min.

## Wirkung auf den Speicher (wahrscheinlich, Störgröße Zapfung)
30-min-Fenster 05-23 Uhr ohne Ladung/Verdichter (n = 245):
| Fenster | n | oben K/h | unten K/h |
|---|---|---|---|
| ohne Puls, ohne Zapfsprung | 83 | -0,20 | -0,40 |
| 1 Puls, ohne Zapfsprung | 52 | -0,70 | -1,20 |
| 1 Puls, mit Zapfsprung | 34 | -1,60 | -1,40 |
| ≥ 2 Pulse, mit Zapfsprung | 26 | -2,80 | -1,90 |
15 min ab Pulsbeginn: oben -0,6 K (Median, n = 76) gegen -0,1 K in gleichen Fenstern ohne Puls (n = 109).
- **Wahrscheinlich:** ein Puls kostet grob 0,3-0,5 K mehr Speicherabfall als Ruhe, also ~0,1-0,2 kWh Wärme. Bei ~35 Pulsen/Tag **~2-5 kWh Wärme/Tag (~0,7-1,5 kWh Strom bei WW-AZ 3,0)** - aber Puls und Zapfung fallen zusammen (Präsenz -> Puls -> Händewaschen), daher Obergrenze, nicht sauber getrennt.

## Vorschlag (der Betreiber entscheidet, nichts geändert)
1. **Sperrzeit nach Puls 20 min** (Loxone: Monoflop/Sperre vor dem Pumpenausgang). Die Leitung ist 5-15 min nach einem Puls noch warm; 84 von 135 Pulsen fielen in dieses Fenster. Spart Pumpenstarts (~60 %) und etwas Durchmischung im Speicher; Wärmeersparnis klein (~0,5-1 kWh/Tag, Vermutung).
3. Der große WW-Posten bleibt die Zapfung selbst (~20 kWh Wärme/Tag) -> WW-Soll 57 -> 52 °C bleibt der stärkere Hebel.

**Was bringt uns das:** Zirkulation ist kein versteckter Dauerverbraucher - sie ist schon gut bedarfsgeführt. Ein 20-min-Sperrfenster ist eine kleine, risikolose Verbesserung; das Geld liegt beim WW-Sollwert und bei der Zapfmenge.

## Offen (Loop, nur lesend)
- Welche weiteren Eingänge triggern die Pumpe (Loxone-Projektdatei, Baustein vor "Zirkulationspumpe")?
- Rücklauffühler Zirkulation vorhanden? (Hoval 19755 Zirkulationskreistemperatur = leer -> nicht an Hoval.)