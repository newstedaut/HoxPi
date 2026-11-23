# ANALYSE Speicherrollen / effektives Volumen aus Messdaten – 23.10.2026 (Analyse-Agent, nur lesend)

Frage: Passt der WW-Speicher nach den Messdaten eher zu ~283 l (EnerVal 300) oder ~379 l (CombiVal ESR 400)? Gibt es Daten zum Puffer?
Daten (Pi, nur gelesen): `~/hoxpi_fulllog/ww_hires.csv` (1 min, ab 20.09.), `~/ww_abnahme.csv` (1 min, nur während Ladungen: Flow `31708` l/min, WEZ-VL `18725`, RL `1535`, Zähler `27489` Q_WW kWh), Volllogger-Header.
Skripte: `Emulation\or_ag2_speichervolumen_20261023.py/.out`, `or_ag2_speichervolumen2_20261023.py/.out`, `or_ag2_speichervolumen3_20261023.py/.out` (Kopien unter `/tmp/or_ag2_*` auf dem Pi). Kein Bus-Zugriff, nichts geschrieben.
Grundlage: `FUND_EnerVal_CombiVal_Speicherart_Verifikation_20261023.md`, `FUND_Speicher_Bereitschaftsverlust_..._20261022.md`, `ANALYSE_WW_Ladungen_20261021.md`, `ANALYSE_WW_Speicherverlust_und_Kurzlaeufe_20261022.md`, `ANALYSE_Stale_Register_Volllogger_20261023.md`.

## 1. Methode
- Ladung = SLP (`19754`) an, ≥ 15 min. Start = Minute vor SLP an, Ende = letzte SLP-Minute.
- Speichertemperatur = Mittel aus `WW_Ist` (SF oben, `1500`) und `WW_Unten_SF2` (`27483`). ΔT = Mittel(Ende) − Mittel(Start).
- Wärme Q drei Wege: (A) Σ P_th (`25612`, ganze kW), (B) Σ Flow·(VL−RL)·c, (C) Zählerdifferenz `27489`. B/A = 102 % (Median, n = 88), C ±1 kWh. Die drei hängen am **selben** WP-Flow-/Temperaturfühler, sind also untereinander nicht unabhängig.
- V_eff = Q / (c·ΔT), c = 1,163 Wh/(l·K). Zusätzlich lineare Regression Q = k·ΔT + Q0 über alle Ladungen: k/c = Volumen, Q0 = Fixanteil je Ladung (Leitungen, Register, WP-Inhalt aufheizen, Verluste während der Ladung).

## 2. Ergebnis WW-Speicher
| Auswahl | n | ΔT-Bereich | k [kWh/K] | Q0 [kWh] | **V aus Steigung** | V Einzelladung (Median) |
|---|---|---|---|---|---|---|
| alle (inkl. Zapfung) | 79 | 3,1–18,4 K | 0,430 | 4,10 (Streuung 2,3) | 370 l | 836 l |
| ohne Zapfung | 36 | 3,4–11,8 K | 0,617 | 1,94 (Streuung 0,7) | **531 l** | 823 l |
| Kaltstart (SF2 < 30 °C) | 13 | 12,2–18,4 K | 0,561 | 1,45 (Streuung 0,9) | **482 l** | 530 l |
| ohne Zapfung, Endwert +30 min | 37 | – | – | – | – | 718 l |

Vergleichswerte (Datenblatt Q1, Wasserinhalt; Stahl/Email geschätzt +15–25 l Wasseräquivalent, **Vermutung**, Leergewicht nicht verifiziert):
| Kandidat | Wasser | erwartet k | erwartet V_eff |
|---|---|---|---|
| EnerVal 300 als WW | 283 l | 0,33 kWh/K | ~300 l |
| CombiVal ESR 400 als WW | 379 l | 0,44 kWh/K | ~400 l |
| beide zusammen | 662 l | 0,77 kWh/K | ~700 l |

Lesart:
- Einzelladungen ohne Achsenabschnitt (720–840 l) sind **zu hoch**, weil jede Ladung einen festen Anteil (Leitungen, Register-/WP-Wasser auf 50–58 °C bringen, Verluste) enthält und kleine ΔT (4–8 K) diesen Anteil aufblasen. Deshalb zählt die **Steigung**, nicht der Median.
- Die Steigung liegt bei **480–530 l**. Das ist deutlich über 283 l und 20–30 % über 379 l.
- Die Kaltstart-Ladungen (großes ΔT, kleinster relativer Fehler) liefern je Ladung 492–658 l, Median 529 l (8 von 13 zwischen 492 und 554 l). Bei allen fällt SF oben in den ersten Minuten um 3–5 K (Zapfung läuft noch bzw. Durchmischung beim Anlauf), sie sind darum oben als „Zapfung“ markiert.

**Gegenrechnung Einzelfall 20.09.2026 05:31–06:32 (Kaltstart, Rohdaten unten):** Start oben 44,5 / unten 19,2 °C (Mittel 31,9), Q = 11,2 kWh (Zähler 39322 → 39333 = 11 kWh). Nach Abzug Q0 ≈ 1,5 kWh bleiben ~9,7 kWh im Speicher.
- 283 l (+Stahl, 0,34 kWh/K): Mittel müsste um ~29 K auf **~61 °C** steigen. Gemessen: 52,3 / 48,3, nach 30 min 53,1 / 50,7 °C. Das ist mit 283 l **nicht vereinbar**. Dafür müsste eine große, kalte Zone vom Fühlerpaar völlig ungesehen bleiben.
- 379 l (+Stahl, 0,46 kWh/K): Anstieg ~21 K auf **~53 °C**. Gemessen (Mittel +30 min) 51,9 °C. Das **passt** innerhalb der Fehler.

## 3. Fehlerquellen (ehrlich)
- **Zwei Fühler für den ganzen Speicher.** Die Fühlerhöhe ist im ESR-Fühlerkanal frei wählbar und bei dir unbekannt. Schichtung über bzw. unter den Fühlern wird nicht gesehen. Nach Ladeende gleicht sich das noch aus: Der Endwert +30 min senkt den Median von 823 auf 718 l. Die Fühler unterschätzen ΔT also eher, und das treibt V nach **oben**.
- **Zapfung während der Ladung:** Die abgezapfte Wärme fehlt im Speicher, V wird nach oben verfälscht (Extremfälle 2 100–3 000 l). Der Filter fängt kleine Zapfungen nicht sicher.
- **Q0 1,5–1,9 kWh je Ladung** ist mehrdeutig. Darin stecken Leitungen, Registerwasser (34 l) und WP-Inhalt, die von ~30 auf 50–58 °C gebracht werden (≈ 60–80 l·20 K ≈ 1,4–1,9 kWh, **plausibel**), dazu Fühler-Trägheit.
- **Wärmemessung:** Hoval-Flow/VL/RL sind nicht unabhängig geeicht. Die Genauigkeit liegt **vermutlich** bei ±5–10 %, das entspricht ±25–50 l.
- **Stahl-/Emailmasse und Registerinhalt** sind geschätzt, das Leergewicht ESR 400 ist nicht verifiziert.
- Alle Fehler außer der Durchflussmessung verschieben V eher nach **oben**. Deshalb sind 480–530 l **mit 379 l verträglich**, mit 283 l aber kaum.

## 4. Abkühlrate im Stillstand vs. Katalog – unterscheidet NICHT
- Katalog umgerechnet auf ΔT 34,5 K: ESR 400 1,51 W/K → 52 W → **0,118 K/h** bei 379 l; EnerVal 300 1,13 W/K → 39 W → **0,119 K/h** bei 283 l. Beide Speicher sollten praktisch **gleich schnell** abkühlen. Das Kriterium trennt also nicht.
- Mit 379 l statt 300 l steigt der gemessene Ruheverlust von 2,6 auf **~3,3 kWh_th/Tag (~137 W)**, das ist ~2,6× Datenblatt. Der Mehrverlust steckt **wahrscheinlich** in Anschlüssen, Einrohrzirkulation und Thermosiphon (siehe FUND 22.10.), nicht im Mantel.

## 5. Puffer (EnerVal) – nicht ermittelbar
- Der einzige Pufferfühler-Datenpunkt am Bus (`27493/27494` WPF-Pufferfühler) ist **immer ungültig** (32768 bzw. 0, Stale-Inventar 23.10.). Es gibt keinen weiteren Puffer-Temperaturwert.
- `Vorlauf` in ww_hires (bzw. `1513/1514`) steigt während der WW-Ladung auf die WP-Vorlauftemperatur (52–59 °C) und fällt danach wieder ab (+20 min Median noch +13 K über Start). Der Fühler sitzt **wahrscheinlich** in der gemeinsamen WP-Leitung vor dem Umschaltventil. Über den Puffer sagt er nichts.
- HK1-Pumpe läuft während WW-Ladungen 0–10 % der Zeit, Volumen und Abkühlung des Puffers lassen sich so nicht bestimmen.
- **Vermutung (schwach):** Die Steigung (480–530 l) liegt über 379 l. Ein Teil der Ladewärme könnte also auch ins Heizungswasser gehen (Umschaltventil nicht ganz dicht, Puffer hydraulisch in Reihe). Dagegen spricht: Ein ganzer 283-l-Puffer würde k auf ~0,77 kWh/K heben, gemessen sind 0,56–0,62. Die Fühlerfehler aus 3. erklären die Differenz ebenso gut. **Offen.**

## 6. Nebenbefund: SF2-Standbild
`WW_Unten_SF2` (`27483`) stand **16.10. 18:04 – 17.10. 12:25 auf 54,4 °C** und **17.10. 13:04 – 18.10. 11:13 auf 48,5 °C** (≥ 6 h unverändert trotz Ladungen). Es endet 2 min vor dem Regler-Reset 18.10. 11:15 (**wahrscheinlich** derselbe Zusammenhang). Auswertungen mit SF2 aus diesem Fenster (Ladeende, Hysterese, Ruheverlust unten) sind **ungültig**.

## 7. Einstufung
**Sicher (aus Rohdaten)**
- Die WW-Ladewärme pro Kelvin Fühler-Mittel liegt bei **0,56–0,62 kWh/K** (Steigung, n = 13 bzw. 36). Ein Speicher mit 283 l Wasser (0,33 kWh/K) kann das nicht aufnehmen, ohne dass beide Fühler deutlich über die gemessenen Endwerte steigen.
- Die drei Wärmemessungen (P_th, Flow·ΔT, Zähler `27489`) stimmen auf ±3 % überein.
- Es gibt keinen gültigen Pufferfühler am Bus.
- SF2 war vom 16.10. 18:04 bis 18.10. 11:13 eingefroren.

**Wahrscheinlich**
- Der WW-Speicher ist der **CombiVal ESR 400 (379 l)**, nicht der EnerVal 300. Das deckt sich mit dem Datenblatt-Befund (Rollen in der Projektdoku vertauscht).
- Das effektive WW-Volumen inklusive Stahl liegt bei ~400 l. Die gemessenen 480–530 l liegen wegen der Fühlerlage und kleiner Zapfungen eher zu hoch.
- Jede Ladung hat einen Fixanteil von ~1,5–1,9 kWh_th (Leitungen/Register/WP aufheizen und Verluste).

**Vermutung**
- Ein Teil der Ladewärme geht in Heizungswasser bzw. Puffer (Umschaltventil). Die Daten sind schwach und durch Fühlerfehler ebenso erklärbar.
- Stahl-Wasseräquivalent 15–25 l (Leergewicht nicht geprüft).

**Nicht ermittelbar (aus diesen Daten)**
- Puffer-Volumen, Puffer-Abkühlung und Puffer-Rolle im Kühlbetrieb (kein Fühler).
- Speicherart allein aus der Abkühlrate (beide Kandidaten ~0,12 K/h laut Katalog).
- Genaue Fühlerhöhen und damit ein Volumen besser als ±20 %.

## 8. Was bringt uns das
1. **Dokumentation:** Die Messdaten stützen unabhängig vom Katalog die Korrektur. **WW = CombiVal ESR 400 (379 l, Register 3,8 m²), Puffer = EnerVal 300 (283 l).** Endgültig erst nach Typenschild-Foto (Art.-Nr. 7015 967 bzw. „3 bar“ am Puffer). In allen WW-Rechnungen **0,44 kWh/K** (bzw. 0,46 mit Stahl) statt 0,349 kWh/K (300 l) verwenden. Frühere kWh-Angaben zum Ruheverlust steigen um ~26 % (2,6 → ~3,3 kWh_th/Tag).
2. **WW-Hysterese (05-000 = 5 K):** Eine 5-K-Nachladung kostet ~2,3 kWh Speicherwärme + ~1,5–1,9 kWh Fixanteil. Der Fixanteil macht bei kleinen Ladungen **35–45 %** aus. Die vielen kurzen 57-°C-Boost-Ladungen (ΔT 4–8 K, 11–20 Uhr) haben das schlechteste Verhältnis. Weniger, dafür größere Ladungen sparen **wahrscheinlich** mehr als ein niedrigeres Soll. Der Fixanteil ist aber nur teilweise Verlust: Wärme im Register bleibt im Speicher. Umsetzung nur über Loxone bzw. Hoval-Einstellung, **der Betreiber entscheidet**.
3. **Reserve:** Mit ~380 statt 300 l stehen zwischen 45 und 52 °C nur ~0,65 kWh mehr Wärme bereit (80 l · 7 K), insgesamt ~3,1 statt ~2,4 kWh. Für die Bewertung „reicht abends eine Ladung“ ist das klein, aber nicht null.
4. **Für den Zwilling/Emulator:** WW-Speicher als ~400 l mit Q0 ≈ 1,7 kWh je Ladestart ansetzen. SF2-Fenster 16.–18.10. ausfiltern.

## Rohdaten-Stichproben zum Gegenprüfen
- `ww_hires.csv` `2026-09-20 05:30:02`: SLP 0, WW_Ist 445, SF2 192 → `2026-09-20 06:32:52`: SLP 1, 523 / 483 (→ 06:33:51 SLP 0, 524/486). `ww_abnahme.csv` `27489_q_ww`: 05:31:01 = 39322, 06:29:02 = 39333 (+11 kWh), Flow 05:45 = 28,3 l/min.
- `ww_hires.csv` `2026-10-13 05:53:31`: SLP 0, 472 / 418 → `2026-10-13 06:42:52`: SLP 1, 521 / 497. `ww_abnahme.csv`: 05:54:02 `27489` = 39726, 06:40:02 = 39732 (+6 kWh). ΔT Mittel 6,4 K → ohne Q0 836 l, mit Q0 1,9 kWh ~580 l.
- Prüfbefehl: `grep -E '^2026-09-20 (05:30|06:3[23])' ~/hoxpi_fulllog/ww_hires.csv | cut -d, -f1,3,5,26`