# Analyse WW-Speicherverlust (Ruhe) und Verdichter-Kurzläufe – 22.10.2026 18:15 (Orchestrator)

> → Korrektur 25.10.2026 (ersetzt den Vermerk vom 23.10.): soweit hier mit 300 l / 0,349 kWh/K gerechnet wird, gilt verbindlich das wirksame WW-Volumen des CombiVal ESR 400 von ~405 l, C = 0,47 ± 0,04 kWh/K (F1, 20 zapffreie Ladungen, `[lokaler Pfad]`). Speicher-Wärmemengen und Verluste hier um Faktor 1,35 (+35 %) nach oben korrigieren, nicht +26 %. (EnerVal 300 = Puffer, CombiVal ESR 400 = WW.)

Quelle: `~/hoxpi_fulllog/ww_hires.csv` auf dem Pi (07.09.–22.10.2026, 91 386 Zeilen, Abtastung 60 s), nur lesend.
Skripte: `Emulation\or_wwverlust_20261022_1800.py/.out`, `Emulation\or_wwverlust2_20261022_1815.py/.out`.

## 1. Ruheverlust Warmwasserspeicher (Enerval 300) [⚠ Korr. 23.10.2026: WW-Speicher ist der CombiVal ESR 400, ~379 l]
| | oben (WW_Ist) | unten (SF2) | Wärme (300 l, 0,349 kWh/K, Mittel oben/unten) |
|---|---|---|---|
| Median alle | −0,37 K/h | −0,19 K/h | **2,6 kWh/Tag** |
| ab 01.10. (12 Nächte) | −0,27 K/h | – | **2,6 kWh/Tag** |

Ruhige 60-min-Fenster ab 01.10. nach Tageszeit (oben, Median): 20–10 Uhr −0,3 K/h, **16–19 Uhr −1,1 bis −1,3 K/h**, 11/12/14 Uhr −0,55 bis −0,8 K/h.

- **Sicher:** nachts verliert der Speicher ~0,3 K/h, das sind grob 2,5–3 kWh Wärme/Tag (≈ 0,8–0,9 kWh Strom bei WW-AZ 3,0).
- Grenzen: zwei Fühler für 300 l, Schichtung → ±30 %. Zirkulationspumpe ist nirgends dokumentiert.

**Was bringt uns das:** Absenken des WW-Solls spart am Ruheverlust nur wenig (~0,1 kWh el/Tag je 5 K). Der große Posten liegt bei Zapfung/Zirkulation → zuerst klären, ob eine Zirkulation existiert und wann sie läuft; Zeitprogramm auf kurze Fenster (z. B. morgens/abends je 30 min) wäre der größere Hebel.

## 2. Verdichter-Laufdauern (V101 Mindestlaufzeit ~5 min?)
Ab 20.09., Lauf = Modulation > 0 (Lücke ≤ 180 s): HK 118 Läufe (min 2,9 / p10 6,0 / Median 22 / max 82 min, 12 unter 6 min), WW 93 Läufe (min 10, Median 45 min).
Kürzeste HK-Läufe messen fast alle 4,0 min (60-s-Raster → real 4–6 min) → **passt zu einer Mindestlaufzeit um 5 min (V101 plausibel)**.
Ausnahme 20.10. 17:10:55–17:13:51 (gemessen 2,9 min): vorher Fehlercode 0 statt 255 und can0-Wächter-Eintrag 16:53 → **wahrscheinlich erster Start nach Neustart/Spannungswiederkehr**, Ende 1 min nach HK1-Status 23 → 0. Nicht überbewerten.

**Was bringt uns das:** kein Kurztakten-Problem; Kurzläufe sind selten (≈ 1 von 10) und dauern ~5 min. Für den Zwilling: Mindestlaufzeit ~300 s als Arbeitsannahme, Ausnahme nach Neustart.

## Offen (Loop, nur lesend)
- 20.10. 17:10 im X26-0,5-s-Mitschnitt (gz, per zcat) auf exakte Laufdauer prüfen.
- Gibt es eine Zirkulationspumpe (Foto Speicherumfeld / Hoval-Ausgang / Loxone)? Zeitprogramm?

## Nachtrag 22.10.2026 19:10 (Orchestrator)
- **Kurzlauf 20.10. 17:10 widerlegt:** X26-Mitschnitt (Obj 0x20, 0,5 s, 3360 Punkte 16:45-17:40, `Emulation\or_kurzlauf_20261022_1915.py/.out`) zeigt den Verdichter **ab spätestens 16:45 durchgehend in Betrieb** (Mod 35 %, WEZ 1 Heizen, Fehler 255) bis 17:14:12. Der „2,9-min-Lauf" in `ww_hires.csv` war nur das Ende eines ≥ 29-min-Laufs; die Lücke/der Fehlercode 0 davor sind ein Logger-Artefakt nach dem Neustart 16:53. V101 hat damit keine Ausnahme mehr.