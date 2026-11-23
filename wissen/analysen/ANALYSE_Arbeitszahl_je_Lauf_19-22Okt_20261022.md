# Arbeitszahl je Verdichterlauf 19.–22.10.2026 (X26, 0,5 s) – Heizen 5,1, Warmwasser 3,0

> → Korrektur 25.10.2026 (ersetzt den Vermerk vom 23.10.): soweit hier mit 300 l / 0,349 kWh/K gerechnet wird, gilt verbindlich das wirksame WW-Volumen des CombiVal ESR 400 von ~405 l, C = 0,47 ± 0,04 kWh/K (F1, 20 zapffreie Ladungen, `[lokaler Pfad]`). Speicher-Wärmemengen und Verluste hier um Faktor 1,35 (+35 %) nach oben korrigieren, nicht +26 %. (EnerVal 300 = Puffer, CombiVal ESR 400 = WW.)
Orchestrator 22.10.2026 17:10 · nur lesend · Skript `Emulation\or_az_20261022_1710.py` (+ `or_az_run_20261022_1710.sh`, gz per Prozesssubstitution, nichts entpackt) · Ausgabe `Emulation\or_az_20261022_1710.out`
Kanäle: Byte 42–43 Wärmeleistung kW (= 25612), 90–91 P_el 10 W (= 25611), 33 WEZ-Status (1 Heizen, 4 WW), 29 RL, 45 COP-Anzeige. Integration mit dt ≤ 5 s.
**Gegenprobe gegen die Firmware-Zähler (22.10., Byte 55/63):** WW-Zähler +29 kWh vs. integriert 28,5 kWh; E_el-Zähler +12 kWh vs. integriert 12,4 kWh → Integration stimmt auf ±3 %.

| | Läufe | kWh Wärme | kWh Strom | **Arbeitszahl** |
|---|---|---|---|---|
| Heizen (19.–22.10.) | 14 | 66,8 | 13,2 | **5,06** (Einzelläufe 4,2–5,6) |
| Warmwasser (19.–22.10.) | 16 | 105,9 | 34,8 | **3,04** (Einzelläufe 2,7–3,3) |

Außen ca. 8–12 °C. Die COP-Anzeige (Byte 45) liegt je Lauf ~0,1–0,3 über der gemessenen AZ (enthält offenbar keine Pumpen/Anlaufverluste).

**Sicher (gemessen):**
- In 3,7 Tagen gingen **72 % des WP-Stroms (34,8 von 48 kWh) ins Warmwasser**, bei nur 3,0 Arbeitszahl. Heizen läuft mit 5,1 sehr effizient.
- WW-Wärme ≈ **28 kWh/Tag** (106 kWh / 3,7 d). Langzeitzähler sagt dasselbe Muster: 39,9 MWh WW seit IBN ≈ 22 kWh/Tag (`ANALYSE_X26_Obj20_Byte47-91_20261022.md`).
- Ladungen bis 59 °C RL: AZ 2,73–2,87 (19.10. 13:58 Ausnahme 3,17); Ladungen bis 52–54 °C: AZ 2,9–3,3.
- 22.10. 08:18 Heizlauf nur 16 min (AZ 4,2), 19.10. 16:53 WW-Lauf nach 10 min abgebrochen.

**Wahrscheinlich:** 28 kWh/Tag WW-Wärme ist für einen Haushalt 2–3× zu viel; der Großteil sind Speicher-/Leitungs-/Zirkulationsverluste oder ein dauerhaft zu hoher Sollwert, nicht Zapfung. **Noch zu prüfen:** Zirkulationspumpe vorhanden/Zeitprogramm; Zapfmenge aus `ww_hires.csv`.

## Was bringt uns das / Vorschlag (der Betreiber entscheidet, nichts verstellt)
1. **Jede kWh Wärme, die vom WW zum Heizen wandert, kostet 0,20 statt 0,33 kWh Strom.** Weniger WW-Verlust ist der größte Hebel der Anlage im Übergang – größer als jede Heizkurven-Feinjustierung.
2. WW-Soll 57 → 52 °C (abends) und PV-Boost-Ziel prüfen: rechnerisch ~5–10 % bessere WW-AZ plus weniger Speicherverlust. Bei ~9 kWh Strom/Tag WW grob **0,5–1,5 kWh Strom/Tag**.
3. Falls Zirkulation läuft: Zeitprogramm auf Morgen/Abend kürzen – bei 22–28 kWh/Tag WW-Wärme vermutlich der größte Einzelposten.
4. Ziel-Kennzahl für den Winter: WW-Wärme/Tag aus Byte 55 (Zähler) täglich mitschreiben → Erfolg jeder Änderung direkt messbar.
