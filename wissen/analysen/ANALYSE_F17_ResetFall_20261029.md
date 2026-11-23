# ANALYSE F17 - Reset-Fall: Start nach Strom-Ein der Inneneinheit (Orchestrator 29.10.2026 12:59)

Anlass: der Betreiber hat die WP am 29.10. ~08:54 selbst abgeschaltet (Wasser ablassen fuer UG-Kueche) und ~10:42 wieder eingeschaltet - mitten im Heizbetrieb (HK1-Anforderung stand an). Das ist der fehlende Reset-Fall von F17.
Quellen (nur gelesen): X26-Log `/home/<user>/rs485_sniff/log/rs485_2026-10-29.log` (ZUSTAND + Rohrahmen je Minute), Volllogger `/home/<user>/hoxpi_fulllog/2026-10-29.csv`. Skripte `[lokaler Pfad]` und `or_f47f17b_20261029_1300.py` (Ausgaben `.out` daneben), am Pi nur `/tmp`.

## Ablauf (X26, Uhrzeit MEZ)
| Zeit | Ereignis | Werte |
|---|---|---|
| 08:54:05 | letzter X26-Rahmen, danach 0 Rohzeilen/min bis 10:41 | vorher Heizlauf status 1, HK1 23, mod 35 %, 1,85 kW |
| 10:42:28 | erste neue X26-Rahmen (10:42 = 702 Rohzeilen, ab 10:43 ~1930/min) | AT 6,3 -> 8,5 C |
| 10:43:19 / 10:43:24 | status 0 -> 51 (Anlaufphase) | HK1 23 (TopTronic-Anforderung stand durch) |
| Volllogger 10:45 | 1501 = 23, 1520 = 34,5 C, 1534 = 255, 1539 = 51 | - |
| 10:46:27 | status 1, Verdichter an (P_el 0,07 -> 1,58 kW um 10:46:42) | RL 36,5, VL 37,0 C |
| 10:46:42 | HK1 23 -> 0 (Anforderung weg; Volllogger 10:50 1501 = 0, 1520 = 0, 1493 = 5,0) | Verdichter laeuft weiter, Plateau 42 % 10:47-10:49 |
| 10:47:23 | ZYK 20777 -> 20778 | - |
| 10:51:26 | Verdichter aus (mod 0) -> Laufzeit 5,0 min | RL 37,5 |

## Befund
- Verdichterstart **4,0 min nach Rueckkehr** des Busses, ohne 15-min-Wartezeit HKA59 und obwohl die Freigabebedingung A+VL **nicht** erfuellt war: RL 36,5 > Soll 34,5 - 1,5 = 33,0 und VL 37,0 > Soll 34,5 [sicher, X26 + Volllogger].
- Die Anforderung fiel 15 s nach dem Start weg; der Lauf ging trotzdem bis zur Mindestlaufzeit 300 s (V101) [sicher].
- Regel: Nach Strom-Ein startet der Kaelteregler bei anstehender Heizanforderung nach der Anlaufphase (status 51, ~3 min) sofort; HKA59 und die RL/VL-Bedingung greifen dabei nicht [sicher fuer diesen Fall, als Regel wahrscheinlich - 1 Fall].
- Loop-Vorhersage V125: (a) Blockierphase >= 30 min **widerlegt**; (b) Start fruehestens 5 min nach Rueckkehr knapp verfehlt (4,0 min), Anlaufplateau ~42 % **bestaetigt**; (c) Schaltzyklen +1 **bestaetigt**.
- Damit sind fuer F17 Abtau-Fall (2/2) und Reset-Fall (1/1) belegt -> "fertig, wenn" erfuellt.

**Was bringt uns das:** Startvorhersage fuer Loxone/Zwilling ist vollstaendig: nach jedem Strom-Aus (z. B. Abschaltungen beim Kuechenbau) gibt es einen Sofortstart mit 5-min-Mindestlauf, auch wenn die Anforderung gleich wegfaellt - ein Kurzlauf je Abschaltung, ~0,15 kWh, unkritisch.