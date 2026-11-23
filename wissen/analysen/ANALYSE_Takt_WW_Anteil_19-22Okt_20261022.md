# Verdichterläufe 19.–22.10.2026 aus X26 (0,5 s) – Warmwasser frisst den Strom
Orchestrator 22.10.2026 16:40 · nur lesend · Quelle: `~/rs485_sniff/log/rs485_2026-10-19..21.log.gz` (per `<(zcat …)`, nichts nach /tmp entpackt) und `rs485_2026-10-22.log`
Skript: Pi `/tmp/or_takt_20261022_1530.py` (unverändert), Ausgabe `Emulation\or_takt3_20261022_1600.out` bzw. `Emulation\or_takt_20261022_1530.out` (22.10.)
Kanäle: Byte 30 Modulation, 29 RL, 33 WEZ-Status (1 = Heizen, 4 = WW), 90-91 P_el (10 W). kWh = mittlere P_el × Laufdauer (elektrisch, ±10 %).

**Korrektur am Skript-Etikett:** Läufe mit WEZ-Status 4 und RL bis ~59 °C sind WW-Ladungen, auch wenn das Skript „HK“ schreibt (19.10. 13:58, 22.10. 13:15). Unten nach Status 4 umsortiert.

| Tag | WW-Ladungen | WW kWh el | HK-Läufe | HK kWh el | WW-Anteil | Bemerkung |
|---|---|---|---|---|---|---|
| 19.10. | 6 (05:55, 11:25, 13:58, 16:53, 17:29, 19:10) | ~11,1 | 2 (20, 24 min) | ~1,3 | **~90 %** | 3 WW-Ladungen in 2,5 h am Abend; 16:53 nach 10 min abgebrochen, 17:29 neu |
| 20.10. | 3 (06:11, 11:39, 15:01) | ~5,1 | 7 (19–66 min) | ~8,4 | ~38 % | einziger „Heiztag“; nach 17:14 kein Lauf mehr |
| 21.10. | 4 (03:57, 06:36, 16:39, 19:26 – 84 min) | ~8,8 | 2 (9, 24 min) | ~1,0 | **~90 %** | 07:05–15:25 über 8 h Stillstand |
| 22.10. bis 15 Uhr | 3 (05:48, 09:56 – 96 min, 13:15 SG-Vorzug/PV) | ~9,9 | 3 (16–40 min) | ~2,5 | ~80 % | 13:15 laut Loop PV-Boost auf 57 °C |

**Sicher (gemessen):** Im Übergang (Außen ~8–12 °C) gehen 4 von 4 Tagen ein Drittel bis neun Zehntel des WP-Stroms in Warmwasser – 5 bis 11 kWh el pro Tag, bei COP ~2,6–3,0 (X26 Byte 45) also 15–30 kWh Wärme ins WW. Kein Kurztakten der Heizung: HK-Läufe 9–66 min, Pausen ≥ 20 min.
**Wahrscheinlich:** Die WW-Menge ist größer als der tatsächliche Zapfbedarf eines Haushalts (typisch 6–10 kWh Wärme/Tag); Treiber sind die hohen Sollwerte (57 °C abends, PV-Boost 57 °C) plus Speicherverluste Enerval 300 [⚠ Korr. 23.10.2026: WW-Speicher ist der CombiVal ESR 400, ~379 l] + Zirkulation (falls vorhanden – **noch zu prüfen**).
**Vermutung:** Der Abbruch 19.10. 16:53 → Neustart 17:29 ist eine Sperre/Unterbrechung (SG, EVU oder Heizanforderung). Nicht belegt.

**Was bringt uns das / Vorschlag (der Betreiber entscheidet, nichts verstellt):**
1. Abend-WW-Soll 57 → 52 °C (steht schon als offene Entscheidung im Log). Je Ladung 5 K weniger Hub = grob 10–15 % weniger Strom pro WW-kWh und weniger Speicherverlust → bei 5–10 kWh el/Tag WW ca. 0,5–1,5 kWh el/Tag.
2. WW-Ladungen aus Netzstrom auf ein Zeitfenster bündeln (z. B. eine Ladung 12–15 Uhr, PV/wärmste Luft = besserer COP), statt 3–6 verteilter Ladungen. PV-Boost (SG Vorzug) bleibt.
3. Prüfen, ob eine Zirkulationspumpe läuft und mit welchem Zeitprogramm – sonst erklärt sie einen Teil der Abendladungen.