# ANALYSE F54 – Lauf 01.11. 17:05–17:19: Ende durch Loxone-Anforderung, nicht durch RL-Schwelle (Orchestrator 01.11.2026 19:05)

Katalog: F54 (Pausen/Laufende bei mildem Wetter). Nur gelesen: Volllogger `/home/<user>/hoxpi_fulllog/2026-11-01.csv` (5-min-Raster), Loxone-MCP `Klimacontroller UG` (UUID <UUID>, Stand 01.11. 18:56 MEZ).

## Rohwerte Volllogger 01.11.2026 (x10 skaliert zurückgerechnet)
| Zeit | AT 1477 | HK1-Soll 1490 | 1501 | Heiz-Soll WP 1520 | WP-VL 1525 | WP-RL 1535 | 1539 | P_el 25611 |
|---|---|---|---|---|---|---|---|---|
| 17:00:02 | 5,0 | 30,0 | 23 | 32,0 | 30,5 | 30,0 | 0 | 0 |
| 17:05:01 | 5,0 | 30,0 | 23 | 32,0 | 31,5 | 30,0 | 1 | 2,14 |
| 17:10:01 | 4,9 | 27,8 | 23 | 30,0 | 34,0 | 31,0 | 1 | 1,63 |
| 17:15:02 | 4,9 | 28,0 | 23 | 30,0 | 36,0 | 32,5 | 1 | 1,72 |
| 17:20:02 | 4,9 | **0** | 23 | 30,5 | 33,5 | 33,5 | 0 | 0 |
| 17:25:01 | 4,8 | 0 | **0** | 0 | 33,0 | 33,0 | 0 | 0 |
| 18:55:02 | 4,4 | 0 | 0 | 0 | 29,5 | 24,0 | 0 | 0 |

## Befund
1. **Loxone senkte das HK1-Soll mitten im Lauf** 30,0 → 27,8 (17:10), 1520 folgte 32,0 → 30,0 [sicher]. Die Lesart des 17:54-Laufs „Stopp bei RL 34,0 = 1520 + 2,0“ rechnete mit dem alten 1520 = 32,0 – derselbe Fehler wie 12:29 (Stundenbericht 13:20) [sicher].
2. **Im Raster nach dem Stopp (17:20) ist 1490 = 0**, 1501 fällt bis 17:25 auf 0, danach bleibt die Anforderung bis mindestens 18:55 aus [sicher]. Der Lauf endete damit sehr wahrscheinlich, weil Loxone die Anforderung zurücknahm, nicht an einer RL-Schwelle der Hoval [wahrscheinlich; 5-min-Raster, Minutenauflösung fehlt].
3. **Loxone-Zustand 18:56 MEZ:** `demandHeat` 25, `threshold` 30, `stage` 0, 3 von 8 Räumen `demand` = 1 [sicher, gelesen]. Am Nachmittag (16:04 UTC) lag demandHeat bei 31–33 (ANALYSE_F61) [sicher]. → Der Klimacontroller fordert nur Wärme an, solange demandHeat ≥ threshold 30 [wahrscheinlich; Bedeutung von threshold wird in FUND_Loxone_Klimacontroller_Schwelle_20261101.md recherchiert].
4. **Nebenbefund F56:** `maximumTempHeating` = 17 (Heizgrenze Außentemperatur des Klimacontrollers) deckt sich mit der gemessenen Heizgrenze 16,6–17,4 °C aus F56 [sicher als Zahl; ob die Messung die Loxone-Grenze abbildet: wahrscheinlich].
5. **Vermutung „Stopp-Schwelle folgt jetzt 07-001 = 2,0 K“ (OR 17:54) ist damit nicht gestützt** [wahrscheinlich]; Stopp-Regel 1520 + 3,0 (V131 a') bleibt Arbeitsstand. Systematisch an ≥ 20 Läufen 24.10.–02.11. prüft MD-16 (Flash, `ARGON_Laufende_Ursache_Nov2026.md`).

## Was bringt uns das
Kurze Läufe am Abend kommen nicht von der Hoval und nicht von 07-001 = 2 K, sondern daher, dass die Raumanforderung unter die 30-%-Schwelle des Klimacontrollers fällt. Der Hebel gegen Kurzläufe liegt also in Loxone (Schwelle, Mindestlaufzeit ab echtem Verdichterstart), nicht in der Hoval – Entscheidung der Betreiber (ENTSCHEIDUNGEN_offen.md Punkt 1).

## Offen
- Minutenauflösung des Stopps (ww_hires/X26) gegen 1490 → 0: Loop 19/20.
- Bedeutung `threshold`/`demandHeat` laut Loxone-Doku: Recherche-FUND.