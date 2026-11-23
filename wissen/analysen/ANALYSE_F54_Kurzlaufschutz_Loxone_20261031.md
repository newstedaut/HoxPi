# F54 Teilschritt: Warum dauern die von Loxone beendeten Heizläufe ~15 min? (OR 31.10.2026 14:54)

**Frage:** ANALYSE_F54_Laufende_Ursachen_KW44_20261031.md fand 7 von 67 Heizläufen (10 %) durch Loxone 1490 = 0 beendet, Lauf-Median **15 min** (5–50). Vorschlag 14:05 war „1490 erst nach Mindestlauf (z. B. 30 min) auf 0“. Gibt es so etwas schon?

**Quelle (nur gelesen):** `[lokaler Pfad]` (neueste Projektdatei, 25.10.2026 13:03), Skript `[lokaler Pfad]`.

## Befund
| Baustein | Inhalt | Sicherheit |
|---|---|---|
| Formel „1490 inkl. Ofen-Nachlauf (min. 24 °C)“ | `IF(I2>0; MAX(I1;24); IF(I1>0; I1; IF(I3>0; MAX(I4;20); 0)))` — I1 Sollwert Heizen 1490 (Klimacontroller), I2 Ofen-Nachlauf, I3 Kurzlauf-Schutz, I4 HK1-Vorlauf-Ist | sicher (Datei) |
| Schwellwertschalter „Verdichter laeuft (Kurzlauf-Schutz)“ | auf 25611 (P_el): EIN > 0,5 kW, AUS < 0,3 kW, steigende Flanke = Verdichterstart | sicher (Datei) |
| Monoflop „Kurzlauf-Schutz 15 min“ | Time = **900 s** ab Verdichterstart, nicht nachtriggernd | sicher (Datei) |
| Eingebaut | 18.10.2026 (Claude), Rückweg in der NDOC: Formel wieder `IF(I2>0;MAX(I1;24);I1)` | sicher (Datei) |

## Deutung
- Schließt der Klimacontroller UG das Heizfenster (demandHeat < 30 %), hält Loxone 1490 bis 15 min nach Verdichterstart auf HK1-VL-Ist (min. 20 °C) und setzt dann 1490 = 0. Das erklärt den **Lauf-Median 15 min** der Loxone-beendeten Läufe exakt (wahrscheinlich; ob genau diese Datei auf dem Miniserver läuft, ist nicht zurückgelesen).
- Ausreißer 5 min: Start-Flanke erst bei 25611 > 0,5 kW bzw. Fenster schloss vor dem Start; 50 min: Fenster schloss erst spät (Vermutung, nicht einzeln geprüft).
- **Der Vorschlag 14:05 („Mindestlauf 30 min“) heißt konkret:** Monoflop-Zeit 900 → 1800 s. Kein neuer Baustein nötig.

## Was bringt uns das
- Der Zwilling kann Loxone-Schnitte als „Lauf = max(Fensterzeit, 15 min)“ abbilden (sicher als Regel der Datei).
- Hebel für der Betreiber (nichts geändert): Monoflop „Kurzlauf-Schutz 15 min“ auf 1800 s → die ~1 kurzen Läufe/Tag werden 30 min lang; Nebenwirkung: bis 15 min mehr Wärme in schon warme Räume (Raum ~22,7 °C am 31.10. 13:20). Vorher Backup + Skill `loxone-xml-umbau`. Doku Monoflop: https://www.loxone.com/dede/kb/monoflop/
- Status F54 bleibt **teilweise** (Rest: demandHeat-Zeitreihe nachts, Loop).