# ANALYSE: 1510-Nachtknick 01-04 Uhr - Einzelereignis oder jede Nacht? (16.-23.10.2026)
Orchestrator-Lauf 23.10.2026 07:55 (MEHR Stufe 1, Eigenarbeit). Nur lesend: Volllogger `~/hoxpi_fulllog/2026-10-16..23` (Skript `HoxPi-Doku\or_1510naechte_20261023.sh`, 30-min-Raster), Loxone-Meter "Wohnraumlüftung" (<UUID>, Leistung 30-min, UTC).
Folgt auf `ANALYSE_Raumknick_1510_Nacht_23Okt_20261023.md` und `ANALYSE_WZ_Override_Zeitbasis_Kuehlfalle_20261023.md` (Ursache dort offen).

## 1. Der Knick kommt fast jede Nacht - sicher
1510 (Raum, x0,1 °C), lokale Zeit:
| Nacht | 20:30-01:30 | 01:30 -> 04:30 | danach bis 07:30 | Heizstart (1490>0) |
|---|---|---|---|---|
| 16./17. | 242-258 -> 241 (Abend-Heizlauf) | 241 -> 237 (-0,4 K) | 237 -> 226 | keiner |
| 17./18. | 227 -> 237-240 | 237 -> 226 (-1,1 K) | 226 -> 221 | 07:30 |
| 18./19. | 221 -> 240 -> 237 | 237 -> 227 (-1,0 K, Hauptteil bis 03:30) | 227 -> 220 | 07:30 |
| 19./20. | 212-215 flach | 211 -> 205 (-0,6 K) | 205 -> 203 | 06:30 |
| 20./21. | 220-222 flach | 218 -> 214 (-0,4 K) | 214 flach | keiner |
| 21./22. | 212-215 flach | 211 -> 205 (-0,6 K) | 205-207 flach | 04:30 |
| 22./23. | 212-214 flach | 212 -> 204 (-0,8 K, bis 03:30) | 204-208 flach | 03:00 |
- Muster: abends flach (oder steigend nach Heizlauf), **zwischen ~01:30 und ~04:30 fällt 1510 um 0,4-1,1 K**, danach wieder flach - in 6 von 7 Nächten in diesem Fenster der stärkste Abfall (Ausnahme 16./17.: stärkster Abfall erst 04:30-07:30).
- Der Knick ist also **kein Ereignis vom 23.10.** und hängt nicht am WZ-Override (der lag 23.10. 03:00-06:59, andere Nächte ohne Override gleich).

## 2. Lüftung scheidet aus - wahrscheinlich
- KWL-Leistung (Loxone-Meter) in den Knickfenstern 23:30-02:30 UTC (= 01:30-04:30 lokal) ohne Stufenwechsel: 22./23.10. 0,040-0,046 kW, 21./22. 0,040-0,045, 19./20. 0,049-0,055, 20./21. 0,026-0,031.
- Die KWL-Wechsel liegen anders: Absenkung ~02:00 UTC (04:00 lokal), Anhebung ~04:00 UTC (06:00 lokal), Stoß 17:30-19:30 UTC. Einzelwert 22.10. 23:00Z 0,059 kW ist ein 30-min-Ausreißer, keine Stufe.
- Also: keine Nachtlüftungsstufe, die den Knick erklärt (wahrscheinlich; Zulufttemperatur nicht gemessen).

## 3. Was es sein kann - Vermutung
- Fühlerort: 1510 liest laut Doku entweder das WZ-Display oder einen Loxone-Wert; am 23.10. 05:56 lag Loxone-WZ 0,8 K höher (21,3 vs 20,5). Ein Wandfühler nahe Außenwand/Fenster zeigt solche Gewinn-Schwankungen stärker (Vermutung).
- Außentemperatur erklärt es nicht allein: 19./20. stieg AT 01:30-05:30 (8,4 -> 9,8 °C) und 1510 fiel trotzdem bis 03:30.

## 4. Was bringt uns das
- **Heizlast/Auskühlrechnung:** nicht die 01-04-Steigung nehmen (Gewinn-Abbau), sondern die Plateaus 04-07 Uhr bzw. Mittel über die ganze Nacht. Die 0,075 K/h aus `ANALYSE_Auskuehlung_Heizlast_20261023.md` bleiben als Größenordnung ok.
- **Regelung:** 1510 ist als Führungsgröße für Raumeinfluss in der Hoval-Regelung ungeeignet, falls er dort wirkt (der Fühler würde nachts 0,5-1 K "Kälte" melden, die das Haus nicht hat). Ob Raumeinfluss aktiv ist, ist offen (Werk FBH max 4, siehe FUND_Winterbetrieb).
- Die Loop-Aufgabe "1510 neben WZ tempActual" bleibt sinnvoll, um den Fühlerort zu klären; die Frage "was passiert um 01:00" ist damit erledigt: nichts Besonderes, es ist jede Nacht so.

## 5. Offen
- Wer schreibt 1510 (der Betreiber, Loxone Config / Bedienteil Raumfühler-Zuordnung)? Ist Raumeinfluss HK1 aktiv (03-0xx am Bedienteil)?
- Loxone-IRR "Wohnzimmer" hat keine Statistik (control_statistics: nicht chartbar) - Gegenkurve nur über den Loop (5-min-Abfrage tempActual).

Stichprobe (eigene Rohdaten, gleiche Ausgabe): 2026-10-23 03:30 1477=27, 1510=205, 1490=332; 2026-10-19 02:30 1477=86, 1510=231.


## Nachtrag 24.10.2026 00:00 (Orchestrator, Katalog F8): Wer schreibt 1510?
- **Kein Loxone-Baustein (sicher):** In `[lokaler Pfad]` und allen anderen `.Loxone` in `Loxone-Umbau\` gibt es **keinen** Aktor mit `ModbusAddress="1510"` (geschrieben werden u. a. 1490 `AMQ46`, 27510 `AMQ198`). Skript `Emulation\or_f8_20261024_0000.py`.
- **Kein Modbus-Schreibzugriff (sicher, 48 h):** Bridge-Journal 22.10. 00:00–24.10. 00:00: 3 794 `SET reg`-Zeilen (23623/23624 Lüftung, 1490, 29435/36, 27545, 1497, 27510, 1496 …), **0× 1510**. Skript `Emulation\or_f8b_20261024_0000.py`.
- **1510 kommt vom CAN (sicher):** `reg_age_s` 1510 = 26,8 s, also laufend vom Regler beantwortet. Im Bridge-Code nur als „extern einspeisbar“ markiert, nicht beschrieben.
- **Quelle = Raumfühler eines Hoval-Teilnehmers (wahrscheinlich):** TTE-BM (1) Wand-Bedienteil oder FRT 351 der HomeVent (TTE-HV 8). Welcher und wo er hängt: Vermutung, im Fotoalbum/Katalog nicht belegt.
- **Was bringt uns das:** Der Nachtknick ist ein Messwert eines Hoval-Fühlers, nicht ein Loxone-Signal; da Raumeinfluss (03-007 = 0) aus ist, wirkt 1510 nicht auf den Vorlauf. Keine Änderung nötig.