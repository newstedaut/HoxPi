# Analyse: Abtauungen und Heizstab seit 07.09.2026 (Orchestrator 22.10.2026 01:00-01:30)

Quellen (nur lesend): `~/hoxpi_fulllog/ww_hires.csv` + `ww_hires_bis20260907_171521.csv` (1-min, 90 124 Zeilen, 07.09. 11:17 - 22.10. 00:55),
`~/x4_sniff/x4_2026-10-13.log.gz` (X4, Lüfter `0xD001` an Slave 6, FC6), `~/heizstab_watch.log` (W3-Wächter).
Skripte: `HoxPi-Doku\or_abtau_20261022_0100.py/.out`, `or_abtau2_20261022_0110.py/.out`, `or_abtau3_20261022_0125.py/.out`.

## Ergebnis kurz
- **Echte Abtauungen bisher: 3** (Marker `WW_Soll_eff` = 10,0 bei laufendem Verdichter): 28.09. 04:40 (WW-Ladung, außen 9,6 °C, schon bekannt) und **zwei neue im Heizbetrieb am 13.10. um 07:09 und 08:37 (außen 2,2-2,3 °C)**.
  Die „6-min-Pausen vom 13.10.“ aus dem Stundenbericht 21.10. 22:20 **sind diese Abtauungen** — Loop-Frage erledigt.
- 19.09. 21:11 (Marker 1 min, Verdichter aus, direkt nach Fehler 222) ist **keine** Abtauung. Die übrigen 12 Kandidaten (P_th ≤ 1 kW bei P_el > 2,5 kW für 1 min) sind Startminuten mit nachhängendem P_th, keine Abtauung.
- **Heizstab / interne Zusatzheizung: kein Einsatz.** W3-Wächter seit 24.09. ohne Auslösung; P_el > 5,5 kW nur 8 Minuten (13.10. 05:54-05:55, 16.10. 06:08) bei Modulation 78-84 % = Verdichter im WW-Start nach Heizbetrieb, nicht der 6-kW-Stab (der gäbe > 7,5 kW).
- Kälteste Stunden bisher: 456 min unter 3 °C (13.10. Minimum 2,1 °C); 2 982 min 3-7 °C. Die Abtau-Statistik ist also noch dünn.

## Ablauf einer Abtauung im Heizbetrieb (13.10., 2 Fälle, sekundengenau aus X4) — belegt
| Phase | 07:09-Abtauung | 08:37-Abtauung | Merkmal |
|---|---|---|---|
| Lüfter 0xD001 → 0 (Abtaubeginn) | 07:08:52 | 08:37:05 | Lüfter aus, `WW_Soll_eff` = 10,0, VL fällt unter RL (bis 23 °C bei RL 30-37) |
| Abtauen mit Lüfter 0 | 4,5 min | 4,8 min | Mod 42 → 65 %, P_el bis 4,1 kW, HK1-Pumpe läuft weiter |
| Lüfter 13,6 % (0x2200) | <MAC> (2,0 min) | <MAC> (1,6 min) | Endphase, Verdichter noch an |
| Lüfter 73,4 % bei Verdichter aus | <MAC> (5,0 min) | <MAC> (5,0 min) | Nachlüften/Abtrocknen, genau 300 s |
| Neustart | 07:20:44 | 08:48:53 | **~5,5 min nach Abtauende — die 15-min-Stehzeit (V99) gilt nach Abtauung nicht** |

Unterbrechung der Heizleistung je Abtauung ≈ **12 min** (6,5 min Abtauen + 5 min Pause). Laufzeit vor der Abtauung: 07:09 nur 8 min nach Start (davor langer Lauf bis 06:41 ohne Abtauung), 08:37 nach 75 min. → Auslöser ist wahrscheinlich **nicht** eine Laufzeit je Lauf (passt zum Bedarfsintegrator `0x0B25` aus V1-Nachtrag), Abstand der beiden Abtauungen 88 min.

## Vorhersagen
- **V25 (Lüfter = 0 während Abtauung):** Teil 1 **bestätigt** (2/2, Lüfter 0 binnen ≤ 1 min um den Marker). Teil 2 „bleibt 0 bis Abtauende“ **widerlegt**: in den letzten 1,6-2,0 min der Abtauung läuft der Lüfter mit 13,6 %. Präzisierung siehe unten.
- **V1 (b) Dauer 4-9 min:** gestützt (6,1 / 6,4 min Lüfter-aus + Endphase).
- **Neu V102 (notiert 22.10.2026 01:30, vor den Ereignissen):** Jede Abtauung zeigt am X4-Bus die Folge `0xD001`: >0 → **0 (4-5 min) → 0x2200 (1,5-2 min) → 0 → ~0xB799 für 300 ± 5 s bei Verdichter aus → 0** → Neustart 20-25 s später. Widerlegt, wenn bei einer Abtauung die 300-s-Nachlüftphase fehlt oder der Neustart > 8 min nach Abtauende kommt.

## Was bringt uns das
- **Abtauzähler ohne Hoval-Register:** Das Lüftermuster ist eindeutig und sekundengenau. Der Loop kann daraus diesen Winter Anzahl, Dauer und Außentemperatur jeder Abtauung zählen (nur X4-Log lesen).
- **Kosten einschätzen:** Je Abtauung ~0,25 kWh_el + Wärme aus dem Heizkreis (VL fällt 7-10 K unter RL, die HK1-Pumpe läuft weiter — die Abtauenergie kommt aus dem Fußboden/Heizwasser). Bei ~1 Abtauung je 1,5 h Laufzeit unter 3 °C ist das ein messbarer, aber normaler Winterposten.
- **Kein Heizstab** bis jetzt: keine versteckten Stromkosten; W3-Wächter bleibt die Frostwache.
- **Handlungsbedarf an der Hoval: keiner.** Offen (nur Vermutung, der Betreiber entscheidet später): ob die HK1-Pumpe während der Abtauung laufen muss — wenn das Heizwasser dafür den Puffer statt den Estrich nutzen könnte, wäre das hydraulisch günstiger. Dazu fehlt das Hydraulikschema.

## Für den Loop (nur lesend)
1. Bei jedem Tag mit außen < 4 °C: X4-Log nach dem V102-Muster durchsuchen, Abtauungen je Tag + Dauer + außen ins Journal.
2. ND-Minimum und Dauer unter 4,7 bar während der Abtauung (V18) an der nächsten Abtauung notieren.