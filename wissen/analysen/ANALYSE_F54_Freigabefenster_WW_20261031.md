# F54 - Freigabefenster 16:31 ging an die WW-Abendladung (31.10.2026, OR 17:54)

Quelle: Prometheus am HoxPi (hoval_p_el_kw, hc1_status, uka, wp_vorlauf_c, wp_ruecklauf_c, ww_ist_c, ww_soll_c), read_register 1490, Loxone control_state demandHeat. Alles nur gelesen.

| Zeit | p_el kW | hc1_status | WP-VL/RL C | WW ist/soll C | Deutung |
|---|---|---|---|---|---|
| 16:31-17:05 | 0,0 | 23 | 31,2->30,3 / 31,0->30,0 | 47,3 / 50 | Heizfreigabe (OR 16:54), aber kein Start (sicher) |
| 17:00 | 0,0 | 23 | 30,6 / 30,4 | 47,3 / 52 | WW-Soll 50->52 |
| 17:06-17:10 | 2,6-5,1 | 23->6 | 43->49,6 / 41->43,8 | 47,5 / 57 | Verdichterstart als WW-Ladung (57er-Kick 5 min) |
| 17:11-17:41 | 2,4-3,8 | 6 | 52->57,4 / 46->53,3 | 47,1->52,0 / 52 | WW-Ladung, HK1 im Vorrang aus |
| 17:40-17:54 | 0,0 | 0 | 57->49,6 / 53->35,6 | 52,3->52,8 / 52 | Ende WW; 1490 = 0 (17:54 gelesen), demandHeat UG 29 < threshold 30 |

## Ergebnis
- Der einzige Verdichterlauf nach der Freigabe 16:31 war eine WW-Ladung (17:06-17:41, 36 min, ~1,6 kWh_el grob aus p_el), kein Heizlauf (sicher: VL 57, WW +5 K, hc1_status 6).
- Meine Vermutung 16:54 "Heizstart fruehestens ~17:10" ist widerlegt: die WW-Anforderung (Soll 52/57 ab 17:00/17:06) kam vorher und hatte Vorrang.
- Nach der WW-Ladung fiel demandHeat auf 29 (< 30) -> 1490 = 0 ab ~17:40 (sicher fuer 17:54). Heizpause seit 11:25 damit >= 6,5 h bei AT ~9 C, Raum 22,4 (16:21).
- 1490 in den ersten 15 min nach einem HEIZstart bleibt offen (kein Heizstart).

## Was bringt uns das
- Bei mildem Wetter liegt demandHeat knapp um den threshold 30; ein Freigabefenster von ~70 min kann komplett an die WW-Abendladung gehen. Zwilling: WW-Vorrang verbraucht Heizfreigaben, Heizpause = Loxone-Fenster minus WW-Zeit.
- Komfort unkritisch (Raum 22,4). Kein Handlungsbedarf; Hebel bleibt threshold im Klimacontroller UG (Entscheidung der Betreiber, https://www.loxone.com/dede/kb/klimacontroller/).
- 57er-Kick um 17:06 ohne PV (Dunkelheit) - Herkunft (WW-Abend-Logik UMBAU_wwabend 25.10. oder SG) offen; geht an Loop (dp 5051 lesen).