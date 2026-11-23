# ANALYSE F19 — Welches Register zeigt das Umschaltventil Heizen/WW? (Orchestrator 24.10.2026 03:00)

Anlass: Nebenbefund F9 (OR 24.10. 00:54): Reg 19870 heißt offiziell „Status Kühlventil aktiv UKA" und ist bei WW-Ladung nie 1. Die Projektanweisung führt 19870 als „Umschaltventil Heizen/WW (UKA), funktioniert".
Nur gelesen: offizielle Liste `[lokaler Pfad]`, Volllogger `~/hoxpi_fulllog/2026-07-30.csv.gz` … `2026-10-24.csv` (87 Tage, 5-min, 24 591 Zeilen), HoxPi `read_register` live 24.10. ~03:00.
Skript: `[lokaler Pfad]` (auf dem Pi nach `/tmp/or_f19.py`, nur lesend).

## Offizielle Namen (sicher, Datenpunktliste)
| Reg | dp | Name | Gruppe |
|---|---|---|---|
| 19870 | 3/0/22024 | Status Kühlventil aktiv UKA | Wärmemanager |
| 19871 | 3/0/22121 | Status Kühlventil Allg. UHKA | Wärmemanager |
| 19754 | 2/0/1066 | SLP Warmwasser-Ladepumpe | Warmwasser 1 |
| 1550 | 0/0/21035 | SLP HW-Ausgang (Status Ausgang 0/1) | Allgemein |

## Volllogger 30.07.–24.10.2026 (sicher, Zählung)
| Zustand | Zeilen | 19870 = 1 | 19754 = 1 | 1550 = 1 |
|---|---|---|---|---|
| WW-Ladung (1539 = 4) | 1 736 | **0** | **1 682 (96,9 %)** | 1 681 |
| sonst | 22 855 | 6 548 | 156 (meist Nachlauf/Übergang, 1539 = 0/16/51) | 153 |

- 19870 = 1 nur 30.07.–12.09.2026 (letzter Wert 12.09. 01:25), fast ausschließlich bei HK1-Status 1501 = 9 „Normal Kühlbetrieb", 22 „Kühlbetrieb Extern/Konstant" oder 27 (nicht in Liste, laut F9 vermutlich Kühl-Variante). Seit Heizbeginn immer 0.
- 19871 immer 0.
- 19754 und 1550 laufen gleich; die 54 WW-Zeilen mit 0 sind Rand-Zeilen (Beginn/Ende der Ladung im 5-min-Raster) — wahrscheinlich.
- Live ~03:00: 19870 = 0, 19754 = 0, 1539 = 0 (keine Ladung) — passt.

## Ergebnis
- **19870 ist das Kühlventil (Umschaltung Kühlen), nicht das WW-Umschaltventil** (sicher: Name + 0 von 1 736 WW-Zeilen + nur im Kühlsommer aktiv).
- **Die WW-Umschaltung zeigt 19754 „SLP Warmwasser-Ladepumpe" bzw. 1550 „SLP HW-Ausgang"** (wahrscheinlich): bei einer WP ohne eigene Ladepumpe schaltet der SLP-Ausgang das 3-Wege-Umschaltventil; 97 % Deckung mit WW-Ladung. Physisch (Kabel SLP → Ventil) nicht belegt → nur per Foto der Klemmleiste/Ventil-Anschluss sicher.
- Projektanweisung „Umschaltventil Heizen/WW = Reg 19870 (UKA)" ist damit **falsch**; „funktioniert" stimmt für das Kühlventil (schaltete im Sommer).

## Was bringt uns das
WW-Ladung in Auswertungen und Loxone künftig an 19754/1550 (oder 1539 = 4) erkennen, nicht an 19870. 19870 bleibt der Marker für Kühlbetrieb (Taupunkt-/Kühlauswertungen im Sommer).

## Offen
- der Betreiber: Projektanweisung und ggf. Vault/Skill `hoxpi-heizung` korrigieren (Orchestrator ändert die Projektanweisung nicht selbst).
- Physischer Beleg SLP-Ausgang → Umschaltventil: zuerst `[lokaler Pfad]` nach Klemmleiste/Umschaltventil durchsuchen (nächster Lauf), erst dann Foto anfragen.