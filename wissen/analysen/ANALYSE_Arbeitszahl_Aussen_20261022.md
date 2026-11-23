# ANALYSE Arbeitszahl Heizen / WW gegen Außentemperatur (Orchestrator 22.10.2026 02:00)

> → Korrektur 25.10.2026 (ersetzt den Vermerk vom 23.10.): soweit hier mit 300 l / 0,349 kWh/K gerechnet wird, gilt verbindlich das wirksame WW-Volumen des CombiVal ESR 400 von ~405 l, C = 0,47 ± 0,04 kWh/K (F1, 20 zapffreie Ladungen, `[lokaler Pfad]`). Speicher-Wärmemengen und Verluste hier um Faktor 1,35 (+35 %) nach oben korrigieren, nicht +26 %. (EnerVal 300 = Puffer, CombiVal ESR 400 = WW.)

Quellen (nur lesend): `~/hoxpi_fulllog/<Tag>.csv(.gz)` (5 min, Zähler), `~/hoxpi_fulllog/ww_hires.csv` (10 s/1 min, P_el, SLP).
Skript/Ausgabe: `[lokaler Pfad]` / `.out`.

## Zähler (sicher, aus Daten abgeleitet)
| Reg | Bedeutung | Beleg |
|---|---|---|
| 1505:1506 | Wärmemenge gesamt Heizen + WW (kWh, 32 bit) | 111 384 = 27484:27485 (72 062) + 27489 (39 322) exakt, 20.09. |
| 27484:27485 | Wärmemenge Heizen (kWh) | Katalog 60_254_47 |
| 27489 | Wärmemenge WW (kWh) | Katalog 60_254_55, = Q_ww im Journal |
| 27487 | Wärmemenge Kühlen (kWh) = 522, seit 12.09. fest | |
| 25614 | E_el gesamt (kWh) | = E_el im Journal (30 365 → 30 370) |
| 1507:1508 | Betriebsstunden Verdichter | Archiv 19.09. |
Kalibrierung: P_el-Integral aus ww_hires 306 kWh gegen Zähler 25614 298 kWh über 38 Tage (Faktor 0,97) → Aufteilung E_el nach SLP ist brauchbar.
Vorbehalt: Die Wärmemengen sind **Hoval-intern gerechnet** (kein geeichter Wärmezähler belegt) und ganzzahlig kWh → Einzeltage streuen stark, nur Summen/Bins verwenden.

## Ergebnis 01.–21.10.2026 (21 Tage)
| | Wärme kWh | Strom kWh | Arbeitszahl |
|---|---|---|---|
| Heizen | 332 | ~61 | **~5,5** |
| Warmwasser | 462 | ~146 | **~3,2** |
| Gesamt | 794 | 207 | **3,84** (passt zu 27467 = 3,8) |

**Strom: ~9,9 kWh/Tag, davon ~70 % Warmwasser (7,0 kWh/Tag).** WW-Wärme 22 kWh_th/Tag.

Bins nach Tagesmittel außen (ohne Kühltage, Q_heiz ≥ 5 kWh):
| außen | Tage | Q_heiz/Tag | E_el Heizen/Tag | AZ Heizen | AZ WW | Verdichter Heizen h/Tag |
|---|---|---|---|---|---|---|
| 5–8 °C | 1 | 35 | 7,7 | 4,5 | 2,9 | 4,4 |
| 8–11 °C | 11 | 20 | 3,9 | 5,1 | 3,2 | 2,0 |
| 11–14 °C | 11 | 15 | 2,2 | 7,0* | 3,1 | 1,5 |
| 14–17 °C | 7 | 11 | 1,7 | 6,5* | 3,5 | 1,0 |
*bei wenig Heizwärme dominiert die kWh-Rundung, Wert zu hoch.

## Bewertung
- **Sicher:** Heizbetrieb läuft sehr effizient (AZ ~5 bei 8–11 °C, VL ~30–35 °C, Modulation 35 %). Die WW-Bereitung ist im Oktober der Hauptverbraucher.
- **Wahrscheinlich:** Heizlast steigt grob um ~3 kWh_th/Tag je K kälter (11 Tage 8–11 °C: 20 kWh, 1 Tag 7,5 °C: 35 kWh). Hochgerechnet bei 0 °C ~50–60 kWh_th/Tag, AZ eher 3,5–4 → ~15 kWh_el/Tag nur Heizen (Vermutung, nur 1 Tag unter 8 °C).


## Was bringt uns das
1. Größter Hebel im Übergang ist **WW, nicht die Heizkurve**: 57 → 52 °C abends (Vorschlag 21.10., der Betreiber entscheidet). Die Zirkulation ist nach der Abkühlrate wahrscheinlich schon sparsam – dort ist wenig zu holen. 1 Punkt WW-AZ (3,2 → 3,5) spart ~0,6 kWh_el/Tag.
2. Für den Winter Bezugswert: AZ Heizen ~5 bei 8–11 °C. Fällt sie bei Frost unter ~3,5, lohnt die Prüfung Überhöhung 30684/30685 (3,0 → 1,5 K) und VL-Kurve.
3. Loop (lesend): an den ersten Frosttagen dieselbe Rechnung (Skript wiederverwendbar) und die Zirkulations-Laufzeit messen: `Zirkulationspumpe` (UUID <UUID>) über einen Tag alle 5 min lesen und gegen WW-Ist/SF2-Abfall in ww_hires halten. Läuft sie dauernd in der Freigabe, wäre Takt-/Bedarfsbetrieb (der Betreiber entscheidet) der billigste WW-Hebel.