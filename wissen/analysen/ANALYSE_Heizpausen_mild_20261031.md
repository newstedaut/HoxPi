# ANALYSE Heizpausen bei mildem Wetter (F54) — 31.10.2026 09:25, Orchestrator (Claude)

Quelle: Volllogger `/home/<user>/hoxpi_fulllog/2026-10-24.csv.gz` … `2026-10-31.csv` (2136 Zeilen, 5-min-Raster, nur gelesen).
Skripte: `[lokaler Pfad]`, `cc_or_pausen2_20261031_0910.py`, `cc_or_pausen3_20261031_0920.py` (am Pi nur /tmp, nur lesen).
Definition: Lauf = 25611 > 0,5 kW; Heizlauf = Mehrheit 1539 = 1. „Reine Pause" = Heizlauf → Pause → Heizlauf ohne WW-Ladung/Abtauung dazwischen.
Wegen 5-min-Raster: Pausenbeginn/-ende ±5 min; „Pausenende-Wert" = letzte Pausenzeile vor dem Laufstart.

## Ergebnis
| Aussage | Sicherheit |
|---|---|
| 24.–31.10.: 84 Läufe, 56 Heizläufe, 55 Pausen vor einem Heizlauf, davon 34 rein (mit gültigem 1490). | sicher |
| **In 32 von 34 reinen Pausen startet der nächste Heizlauf, wenn der (stehende) WP-Vorlauf 1525 auf HK1-Soll 1490 abgesunken ist:** Soll−VL in der letzten Pausenzeile −1,5 … +1,3 K (Mittel ≈ −0,5 K), Laufstart in der folgenden 5-min-Zeile. Einschaltpunkt also ≈ VL = Soll (±1 K Rasterunschärfe). | wahrscheinlich (Raster 5 min, keine Durchflussmessung in der Pause) |
| Gegenstück Abschaltung (MD-04): Lauf endet bei VL ≈ Soll + 07-001 (3 K) + ~5,7 K. → Schaltfenster am WP-Vorlauf ≈ Soll … Soll+9 K. | wahrscheinlich |
| Gradminuten-Integral als Startbedingung: **verworfen** (CV 3,9 bzw. 1,2 gegen klaren Schwellwert). | sicher (für diese Daten) |
| Pausendauer hängt **nicht** messbar an der Außentemperatur: Regression Dauer = 84 − 1,1·T_aussen min, r = −0,04 (n = 33, 3–11 °C). Reine Pausen 30–100 min, Median ≈ 60 min. | sicher (Bereich 3–11 °C) |
| **2 Ausreißer = lange Nachtpausen:** 29.10. 21:30 → 30.10. 00:20 (170 min, VL fiel bis 6,7 K **unter** Soll 32,2) und 30.10. 22:10 → 31.10. 03:30 (320 min, VL 27,5 bei Soll 31,8 seit 22:20). Hier fehlte die Wärmeanforderung trotz VL < Soll. | sicher (Messung) |
| Ursache der Nachtausreißer: Anforderung kam nicht von der Hoval-Schwelle, sondern von außen — Kandidaten: Loxone (Raumregler ohne Wärmebedarf → HK1-Anforderung/Betriebswahl aus) oder 1490 = 0 (47 % aller Zeilen lesen 1490 = 0). | Vermutung |
| 1490 springt nachts mehrfach um +2 K (z. B. 30.10. 22:20 29,9 → 31,8; 31.10. 08:55 29,9 → 31,9) — Loxone-Raumkorrektur. Am 30.10. 22:20 löste der Sprung **keinen** Start aus. | sicher (Sprünge) / wahrscheinlich (Zuordnung Loxone) |

## Stichprobe (3 Pausen, Volllogger)
| Pause | Dauer | VL 1525 Beginn → Ende | 1490 Ende | Soll−VL | Aussen |
|---|---|---|---|---|---|
| 30.10. 05:15 → 05:45 | 30 min | 37,0 → 32,0 | 32,0 | 0,0 K | 5,5 °C |
| 28.10. 06:10 → 06:40 | 30 min | 35,5 → 32,5 | 31,7 | −0,8 K | 6,6 °C |
| 30.10. 22:10 → 31.10. 03:30 | 320 min | 34,5 → 27,5 | 31,8 | +4,3 K (Ausreißer) | 5,9 °C |

## Was bringt uns das
- Für den Zwilling: Einschalten bei VL ≈ Soll, Ausschalten bei ≈ Soll+9 K; Pausenlänge folgt der Auskühlung von Puffer/Leitung, nicht direkt der Außentemperatur.
- Die langen Nachtpausen sind kein Hoval-Takt, sondern fehlende Anforderung — das ist die eigentliche offene Frage (wer sperrt nachts? Loxone-Raumregler oder 1490 = 0).
- Hebel ohne Anlagenänderung erkennbar: das Schaltfenster liegt fest an 1490 + 07-001; längere Läufe/weniger Starts gingen nur über 07-001 bzw. die Loxone-Vorgabe (Entscheidung der Betreiber, nicht umgesetzt).

## Offen (nächster Schritt)
1. Nachtpausen 29./30. und 30./31.10.: HK1-Betriebsart/-Anforderung (dp 5050/1496, Code 23) und Loxone-Raumregler-Bedarf zeitgleich lesen — Klimacontroller UG hat in Loxone **keine** Aktivitätshistorie (geprüft 09:20), also Loop-Live-Beobachtung nachts nötig.
2. Warum 1490 in 947/2136 Zeilen = 0 liest (Logger-Artefakt oder echter Wert).


## Nachtrag OR 31.10.2026 10:15 - Korrektur (sicher)
- Die Zeile "2 Ausreisser = lange Nachtpausen ... VL fiel unter Soll" ist ein **Auswertefehler**: in beiden Naechten stand 1490 = 0 (Loxone hatte die HK1-Anforderung weggenommen, 1501/1520 = 0); das Skript hatte den letzten Sollwert vor dem Abschalten fortgeschrieben.
- Stichprobe Claude (Volllogger `/home/<user>/hoxpi_fulllog/2026-10-31.csv`): 03:25:02 1490 = 0, 1525 = 27,5 C, 25611 = 0; 03:30:01 1490 = 32,0, 1501 = 23, 25611 = 2,04 kW. 30.10. 21:00:02 1490 = 0 (20:55 noch 29,5).
- Ursache und Belege: `[lokaler Pfad]`, `[lokaler Pfad]`.