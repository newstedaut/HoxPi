# F54 Vertiefung: Wer beendet die Heizlaeufe und wer verlaengert die Pausen? (OR 31.10.2026 14:00, nur lesend)

**Daten:** Volllogger `~/hoxpi_fulllog/2026-10-24.csv.gz` ... `2026-10-31.csv` (5-min-Raster), Skript `[lokaler Pfad]` (am Pi nur /tmp, nur lesend).
**Methode:** Lauf = 1539 = 1 (Heizen). Ende klassifiziert nach dem ersten Wert danach: 1539 = 4 -> WW-Umschaltung, 8 -> Abtauen, 0 mit 1490 = 0 -> Loxone hat die Anforderung genommen, 0 mit 1490 > 0 -> Kaelteregler-Hysterese (RL >= 1520 + HV011, siehe `ANALYSE_F54_Hysterese_HV011_HV012_20261031.md`). Pause = Ende bis naechster Start (< 10 h).

## Ergebnis (24.-31.10.2026, 67 Heizlaeufe, AT mild ~3-11 °C)
| Ende durch | n | Lauf Median (P10-P90) | Pause danach Median |
|---|---|---|---|
| Kaelteregler RL-Hysterese | 49 (73 %) | 35 min (25-65) | 70 min |
| Loxone 1490 = 0 | 7 (10 %) | **15 min (5-50)** | 158 min |
| WW-Umschaltung | 8 | 10 min (5-20) | 90 min |
| Abtauen / 16 / 17 | 1 / 1 / 1 | - | - |

- **Laeufe je Tag 6-13** (Median 8), davon ~1/Tag von Loxone nach 10-20 min abgebrochen (sicher, Volllogger).
- **Pausen nach Hysterese-Stopp (47):** 16 davon hatten zwischendurch 1490 = 0 (Loxone) -> Median **122 min** (P90 320), Summe 2345 min; 31 reine Hysterese-Pausen -> Median **50 min** (P10 35, P90 95), Summe 1835 min. **Rund 56 % der Pausenzeit sind von Loxone verlaengert** (sicher fuer den Messzeitraum, 5-min-Raster).
- **Stichprobe Claude (Rohzeilen 28.10., Spalten 1490/1539):** 10:30-10:40 Heizen bei 1490 = 29,3 -> 10:45 1490 = 0 und 1539 = 0; 14:50-15:00 Heizen -> 15:05 1490 = 0, 1539 = 0. Beide Laeufe ~15 min, von Loxone beendet (sicher).

## Bewertung
- Der normale Takt bei mildem Wetter ist die Kaelteregler-Hysterese (35 min Lauf / 50 min Pause) - passt zu 3-5-fach ueberdimensionierter WP (sicher/wahrscheinlich).
- **Auffaellig (wahrscheinlich):** Die Loxone-Abschaltungen (Klimacontroller UG, demandHeat < 30 %) brechen Laeufe nach 10-20 min ab. Das sind zusaetzliche kurze Starts; der "Kurzlaufschutz" in der Formel "1490 inkl. Ofen-Nachlauf" verhindert sie offenbar nicht (Formel nicht neu gelesen - Vermutung zur Ursache).
- Die langen Pausen (2-5 h) kommen fast nur von Loxone, nicht von der Hoval.

## Was bringt uns das
- Zwilling: Lauf-Ende = Hysterese (Regelfall) **oder** Loxone-Schnitt (1/Tag, kurz); Pause = 50 min Hysterese, verlaengert durch 1490 = 0.
- Hebel zur Entscheidung durch der Betreiber (nichts geaendert): (a) Loxone 1490 erst nach z. B. 30 min Mindestlauf auf 0 nehmen -> ~1 kurzer Start/Tag weniger; (b) HV011 groesser (Kaelteregler, Orchestrator schreibt dort nie). (a) ist der billigere, rein Loxone-seitige Hebel.
- Offen: warum demandHeat tagsueber unter 30 % faellt (Loop: demandHeat je Pause mitschreiben).