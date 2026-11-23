# ANALYSE WW-Speicher Wärmekapazität – Widerspruch 495 l vs. 379 l – 23.10.2026 (Analyse-Agent, nur lesend)

> → 25.10.2026: Zwischenstand (0,514 kWh/K, 34 Ladungen inkl. Zapfungen). Ersetzt durch F1: 0,47 ± 0,04 kWh/K ≈ 405 l aus 20 zapffreien Ladungen, Fixanteil ~1,3 kWh/Ladung – `[lokaler Pfad]`.

**Frage:** Hat der WW-Speicher CombiVal ESR 400 wirksam ~0,44 kWh/K (Datenblatt 379 l) oder 0,576 kWh/K (~495 l, „gemessen“ 15./16.09., Memory/Skill `ww-speicher-combival-495l-pvstab`)?

**Ergebnis in 3 Zeilen**
1. Die 0,576 kWh/K sind ein **Rohquotient Ladewärme / Fühler-Hub**: Er enthält den festen Anteil jeder Ladung (~1,8 kWh, Leitungen/WP-Inhalt/Verluste), der nicht im Speicher landet. Ich habe ihn an denselben 4 Ladungen nachgerechnet (0,58–0,64 roh, **sicher**).
2. Zieht man diesen Fixanteil ab (Regression über 34 saubere Ladungen), bleibt **C ≈ 0,51 ± 0,05 kWh/K** (Steigung). Die 26 Kaltstarts mit 9–20 K Hub liefern im Median **0,47 kWh/K** (Streuung 0,43–0,56). Das entspricht 400–440 l Wasseräquivalent.
3. **Verbindlich: 0,46 kWh/K für den Speicherinhalt** (379 l Wasser + Stahl/Email, **wahrscheinlich**). Für die **WP-Wärme je Ladung**: **Q ≈ 0,5 kWh/K · ΔT(Fühlermittel) + 1,8 kWh**. Die 0,576 kWh/K nicht mehr als Speichergröße verwenden.

**Was bringt uns das**
- Der Widerspruch ist aufgelöst. Beide Zahlen stimmen, sie messen nur Verschiedenes. 0,576 heißt „was die WP pro Kelvin bei einer großen Ladung liefern muss“, 0,44–0,46 heißt „was im Speicher pro Kelvin steckt“.
- PV-Stab-Planung (Stab heizt direkt im Speicher, kein Fixanteil): 50 → 62 °C ≈ **5,5 kWh** (0,46 × 12 K) statt 6,9 kWh. Das sind ~2 h Stablauf statt 2,5 h (bei 2,8 kW).
- WP-Ladung planen: 45 → 52 °C (Mittel +7 K) kostet ~0,5·7 + 1,8 ≈ **5,3 kWh_th ≈ 1,7 kWh_el** (AZ 3,2). Das passt zu den Oktober-Mittelwerten (5,8 kWh_th je 50/52-°C-Ladung, `ANALYSE_WW_Ladungen_20261021.md`).
- Kleine Ladungen bleiben teuer: Bei ΔT 4–6 K ist der Fixanteil 40–50 % der Ladewärme. Das bestätigt `ANALYSE_Speicherrollen_Volumen_aus_Messdaten_20261023.md`, Abschnitt 8.2.
- Kein Hinweis auf Leckwärme in den Puffer, der nicht schon durch den Fixanteil erklärt ist.

---

## 1. Herleitung vom 15./16.09. (geprüft)
Quelle: `[lokaler Pfad]` Abschnitt 2 und `loop_journal_archiv_bis_20260919.md` (Stundenbericht 19.09. 16:35). Später übernommen als „gemessen 23.09.“ in Memory/Skill.

| WP-Ladung (alt) | `27489` Zuwachs | ΔT Speichermittel (+12 min) | alt: scheinbares V |
|---|---|---|---|
| 15.09. 05:35–06:20 | 9 kWh | +17,70 K | 437 l |
| 15.09. 11:50–12:25 | 6 kWh | +9,50 K | 543 l |
| 16.09. 06:20–07:10 | 11 kWh | +16,95 K | 558 l |
| 16.09. 11:10–11:55 | 9 kWh | +17,50 K | 442 l |
| Mittel | | | **495 l = 0,576 kWh/K** |

Kritik:
- **Fühler:** Mittel aus SF oben (`1500` / WW_Ist) und SF2 unten (`27483`). Das ist dasselbe Fühlerpaar wie heute, also in Ordnung.
- **Wärmemenge:** WP-Zähler `27489` (1 kWh Auflösung). Ich habe die Werte gegengeprüft: 15.09. 05:30 → 39245 → 39256 = **11 kWh**, nicht 9. Die alten Zählerdifferenzen sind teils um 1–2 kWh zu klein abgelesen (Fenstergrenzen). Das **verkleinert** V. Die Zahl wäre mit richtigen Fenstern noch höher.
- **PV-Stab:** nicht mitgezählt, an diesen 4 Ladungen lief er nicht (Uhrzeiten 05–07 und 11–12 Uhr, kein Temperaturanstieg ohne SLP). Das ist **in Ordnung**.
- **Hauptfehler: kein Fixanteil abgezogen.** Jede Ladung bringt zuerst WP-Inhalt, Ladeleitungen und Plattenteile von ~30 auf 50–58 °C. Dazu kommen Verluste während der Ladung. Diese Wärme zählt `27489` mit, im Speicher-Hub taucht sie aber nicht auf. Bei 17 K Hub macht das ~10 % aus, bei 9,5 K ~25 % (deshalb liegen 543 l beim kleinsten Hub am höchsten).
- **Ruheverlust** während Ladung und Nachlauf (~0,15 kWh) wurde ebenfalls nicht abgezogen. Das ist klein.
- **Schichtung/Fühlerlage:** Ein ungesehener kalter Bodenbereich unter SF2 würde V **nach oben** treiben. Nach meiner Auswertung (Abschnitt 4) ist dieser Effekt aber klein bzw. steckt im Fixanteil.
- Die Gegenprobe mit dem PV-Stab („512 l“) ist nicht belastbar. Der Loxone-Zähler „Heizstab Trinkwasser“ integriert eine Konstante 2,82 kW über das Laufsignal (`loop_journal_archiv_2026-09.md`). Der zweite Stablauf ergab 1 079 l, die Bilanz wurde am 19.09. 18:45 selbst zurückgenommen.

## 2. Methode (eigene Rechnung)
- **Daten (Pi, nur gelesen, per `hoxpi_ssh.py --get` kopiert):** `~/hoxpi_fulllog/ww_hires.csv` (1 min, Rohwerte ×10, 07.09.–23.10.2026, 93 607 Zeilen) und `~/ww_abnahme.csv` (1 min während Ladungen, Klartext, 5 212 Zeilen).
- **Skripte:** `[lokaler Pfad]`, `or_wwkap_20261023_2_auswertung.py`, `or_wwkap_20261023_3_gegenprobe.py`, jeweils mit `.out`. Kein Bus-Zugriff, nichts geschrieben.
- **Ladung:** SLP an, mindestens 15 min (Lücken bis 3 min überbrückt). Start = letzte Zeile vor SLP an.
- **ΔT:** Mittel (SF + SF2)/2, und zwar **30 min nach Ladeende** minus Start. Zum Vergleich auch am Ladeende und nach 60 min.
- **Wärme Q**, drei Wege wie in `ANALYSE_Speicherrollen_…_20261023.md`:
  - (A) Σ P_th (`25612`)
  - (B) Σ Flow (`31708`) · (WEZ-VL `18725` − RL `1535`) · 1,163 Wh/(l·K), geteilt durch die Zeilenabdeckung der Abnahme-Datei (≈ 0,9)
  - (C) Zähler `27489`

  Die Hauptrechnung verwendet B.
- **Ruheverlust:** 3,3 kWh/d = 137 W, abgezogen über Ladedauer + 30 min.
- **„Sauber“** heißt:
  - keine Zapfung während der Ladung (SF2 fällt nicht > 2 K in 3 min, SF oben nicht > 1 K unter Start)
  - keine Zapfung danach (60 min)
  - kein PV-Stab (kein Anstieg > 0,3 K ohne SLP in der Stunde davor, kein weiterer Anstieg > 0,5 K zwischen +30 und +60 min)
  - keine neue SLP im Nachlauf
  - Abdeckung ≥ 85 %
  - SF2-Standbild 16.10. 18:00 – 18.10. 11:20 ausgeschlossen
- **Auswertung:** Regression Q_netto = C · ΔT + Q0. Die Steigung C ist die Speicherkapazität, Q0 der Fixanteil je Ladung.

## 3. Ergebnis
### 3.1 Regression (34 saubere Ladungen, ΔT 2,5–15,3 K)
| Wärme | ΔT-Zeitpunkt | C (Steigung) [kWh/K] | Q0 [kWh] | C roh Median (ohne Q0) |
|---|---|---|---|---|
| A Σ P_th | Ende | 0,569 ± 0,045 | 2,13 | 0,958 |
| A Σ P_th | +30 min | 0,511 ± 0,049 | 1,85 | 0,781 |
| **B Flow·ΔT** | **+30 min** | **0,514 ± 0,048** | **1,77** | 0,759 |
| B Flow·ΔT | +60 min | 0,511 ± 0,049 | 1,80 | 0,758 |
| C Zähler 27489 | +30 min | 0,494 ± 0,051 | 1,65 | 0,732 |

- Am Ladeende gemessen ist der Hub zu klein, weil der Speicher noch nicht durchmischt ist. Ab +30 min ist der Wert stabil (+30 und +60 min sind praktisch gleich).
- Streuung der Einzelwerte netto (Q − 1,77 kWh)/ΔT: Median **0,512**, Standardabweichung 0,13 (26 %). Die großen Ausreißer sind kleine Hübe (ΔT < 4 K), dort reicht die Auflösung nicht.
- Nach SF2-Startwert aufgeteilt ist C_netto flach: SF2 < 40 °C 0,52 · 40–45 0,49 · 45–48 0,52 · > 48 0,51. **Es gibt keinen Hinweis, dass ein kalter Bodenbereich je nach Schichtung mal gesehen wird und mal nicht.** Der Fühlerfehler wirkt im Wesentlichen additiv und landet in Q0.

### 3.2 Kaltstarts (große Hübe, kleinster relativer Fehler) – 30 Ladungen, davon 26 ohne Ausreißer
Das sind 30 Ladungen mit SF2 < 35 °C (ΔT meist 15–20 K), ohne PV-Stab und ohne neue SLP im Nachlauf, 08.09.–19.10. Die meisten tragen das Zapf-Flag, weil SF oben beim Pumpenanlauf um 0,5–3 K einbricht (Durchmischung). Eine Zapfung würde C **erhöhen**, nicht senken.
- **C_roh** (ohne Q0): 0,51–0,66, typisch **0,55–0,60**. Das ist die alte 0,576.
- **C_netto** (Q0 = 1,77 kWh): 0,41–0,56, **Median ≈ 0,47 kWh/K**.


### 3.3 Die 4 Ladungen der 495-l-Herleitung, mit meiner Methode nachgerechnet
| Ladung | SF/SF2 Start | SF/SF2 +30 min | ΔT30 | Q_B | C_roh | C_netto (Q0 1,77) |
|---|---|---|---|---|---|---|
| 15.09. 05:30–06:27 | 43,6/19,7 | 50,6/48,2 | 17,75 | 11,58 | 0,641 | 0,541 |
| 15.09. 11:48–12:31 | 49,2/38,5 | 55,5/53,5 | 10,65 | 6,81 | 0,624 | 0,457 |
| 16.09. 06:20–07:17 | 44,9/19,3 | 51,5/48,3 | 17,80 | 11,29 | 0,623 | 0,524 |
| 16.09. 11:09–12:01 | 45,1/19,4 | 52,4/48,2 | 18,05 | 10,59 | 0,576 | 0,478 |
| **Mittel** | | | | | **0,616** | **0,500** |

Ohne Fixanteil ergibt sich derselbe Befund wie am 19.09. (meine Werte liegen sogar etwas höher, weil die Wärmefenster vollständig sind). Mit Fixanteil sind es 0,50.

### 3.4 Tabelle aller 34 sauberen Ladungen (Q_B korrigiert, Verlust abgezogen)
| Start | Ende | min | SF/SF2 Start | SF/SF2 +30 | ΔT30 [K] | Q_A | Q_B | `27489` | Verlust | C_roh | C_netto |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 12.09. 07:41 | 08:22 | 42 | 45,2/30,3 | 51,3/48,9 | 12,35 | 6,6 | 6,82 | 6 | 0,16 | 0,539 | 0,396 |
| 15.09. 11:48 | 12:31 | 44 | 49,2/38,5 | 55,5/53,5 | 10,65 | 6,7 | 6,81 | 6 | 0,17 | 0,624 | 0,457 |
| 18.09. 13:59 | 14:51 | 52 | 46,7/32,0 | 55,4/53,8 | 15,25 | 8,7 | 8,52 | 8 | 0,19 | 0,547 | 0,431 |
| 25.09. 00:21 | 00:41 | 21 | 52,1/44,7 | 52,4/49,3 | 2,45 | 2,3 | 2,01 | 2 | 0,12 | 0,771 | 0,049 |
| 25.09. 07:39 | 08:07 | 28 | 50,6/45,1 | 52,7/50,6 | 3,80 | 3,2 | 3,06 | 3 | 0,13 | 0,769 | 0,304 |
| 25.09. 11:37 | 12:13 | 37 | 51,8/49,9 | 57,3/55,9 | 5,75 | 4,5 | 4,43 | 4 | 0,15 | 0,744 | 0,436 |
| 28.09. 11:37 | 12:18 | 42 | 51,3/44,1 | 56,5/55,4 | 8,25 | 6,4 | 6,27 | 6 | 0,16 | 0,740 | 0,526 |
| 04.10. 01:11 | 01:47 | 37 | 45,2/41,4 | 51,3/47,9 | 6,30 | 5,4 | 5,44 | 5 | 0,15 | 0,839 | 0,558 |
| 04.10. 12:05 | 12:57 | 52 | 49,2/45,3 | 57,2/55,8 | 9,25 | 7,7 | 8,03 | 7 | 0,19 | 0,847 | 0,656 |
| 05.10. 11:44 | 12:31 | 47 | 45,6/38,8 | 53,2/50,5 | 9,65 | 7,5 | 7,44 | 7 | 0,18 | 0,752 | 0,569 |
| 06.10. 11:45 | 12:29 | 45 | 48,0/45,4 | 56,5/55,6 | 9,35 | 6,2 | 6,03 | 6 | 0,17 | 0,626 | 0,437 |
| 06.10. 23:40 | 00:29 | 49 | 45,1/39,7 | 53,1/51,1 | 9,70 | 6,9 | 6,95 | 7 | 0,18 | 0,698 | 0,516 |
| 07.10. 06:37 | 07:15 | 38 | 47,2/46,2 | 52,8/51,6 | 5,50 | 4,5 | 4,37 | 4 | 0,16 | 0,766 | 0,445 |
| 07.10. 12:12 | 13:18 | 66 | 45,1/40,9 | 57,0/55,4 | 13,20 | 10,1 | 9,98 | 10 | 0,22 | 0,739 | 0,605 |
| 08.10. 12:36 | 13:07 | 31 | 51,8/49,5 | 56,3/55,6 | 5,30 | 4,3 | 4,10 | 4 | 0,14 | 0,747 | 0,414 |
| 09.10. 00:22 | 00:56 | 35 | 45,2/42,5 | 51,3/49,0 | 6,30 | 4,6 | 4,67 | 5 | 0,15 | 0,718 | 0,437 |
| 09.10. 06:43 | 07:29 | 47 | 47,2/44,9 | 53,0/51,4 | 6,15 | 5,7 | 5,70 | 5 | 0,18 | 0,899 | 0,611 |
| 10.10. 17:04 | 17:36 | 32 | 45,1/43,3 | 51,0/48,7 | 5,65 | 5,0 | 4,67 | 4 | 0,14 | 0,802 | 0,489 |
| 11.10. 04:30 | 05:13 | 44 | 45,9/41,8 | 53,0/50,3 | 7,80 | 5,5 | 5,59 | 6 | 0,17 | 0,695 | 0,468 |
| 12.10. 12:09 | 13:01 | 52 | 48,4/46,5 | 57,0/56,1 | 9,10 | 6,6 | 6,70 | 6 | 0,19 | 0,715 | 0,521 |
| 12.10. 19:24 | 20:21 | 57 | 46,8/39,8 | 52,7/50,3 | 8,20 | 8,0 | 7,53 | 7 | 0,20 | 0,894 | 0,678 |
| 13.10. 12:08 | 13:00 | 53 | 48,3/45,3 | 56,9/55,9 | 9,60 | 7,0 | 7,01 | 7 | 0,19 | 0,711 | 0,526 |
| 13.10. 20:22 | 21:16 | 54 | 44,9/39,4 | 53,1/51,1 | 9,95 | 8,4 | 7,97 | 8 | 0,19 | 0,782 | 0,604 |
| 14.10. 06:18 | 07:11 | 53 | 47,2/43,1 | 54,2/52,7 | 8,30 | 7,7 | 7,72 | 7 | 0,19 | 0,907 | 0,694 |
| 15.10. 13:37 | 14:25 | 48 | 46,9/43,9 | 56,6/55,8 | 10,80 | 7,1 | 7,19 | 7 | 0,18 | 0,649 | 0,486 |
| 16.10. 11:57 | 12:45 | 49 | 50,1/47,0 | 56,3/54,4 | 6,80 | 6,8 | 6,61 | 7 | 0,18 | 0,946 | 0,686 |
| 16.10. 16:01 | 16:31 | 31 | 52,3/50,1 | 56,3/55,5 | 4,70 | 4,2 | 4,36 | 4 | 0,14 | 0,898 | 0,521 |
| 19.10. 11:25 | 11:56 | 32 | 45,1/44,3 | 51,5/49,3 | 5,70 | 4,1 | 4,02 | 4 | 0,14 | 0,680 | 0,370 |
| 19.10. 19:09 | 19:44 | 36 | 52,1/49,3 | 54,5/53,1 | 3,10 | 4,3 | 4,35 | 4 | 0,15 | 1,356 | 0,786 |
| 20.10. 11:39 | 12:21 | 42 | 50,8/49,0 | 56,8/54,8 | 5,90 | 5,3 | 4,93 | 5 | 0,17 | 0,808 | 0,508 |
| 21.10. 03:56 | 04:30 | 34 | 45,2/40,7 | 51,5/49,3 | 7,45 | 4,9 | 4,75 | 5 | 0,15 | 0,618 | 0,380 |
| 21.10. 06:36 | 07:08 | 33 | 47,1/46,2 | 52,8/49,7 | 4,60 | 4,3 | 4,57 | 4 | 0,14 | 0,962 | 0,577 |
| 22.10. 13:14 | 13:53 | 40 | 52,0/49,9 | 57,0/54,9 | 5,00 | 4,7 | 4,94 | 5 | 0,16 | 0,956 | 0,603 |
| 23.10. 16:04 | 16:44 | 41 | 51,3/49,3 | 56,8/56,1 | 6,15 | 5,0 | 4,97 | 4 | 0,16 | 0,782 | 0,494 |

Wärme in kWh_th, Temperaturen in °C. C = (Q_B − Verlust [− Q0]) / ΔT30.

## 4. Warum 0,576 abweicht
- **Hauptgrund (sicher, gerechnet): Fixanteil Q0 ≈ 1,65–1,85 kWh je Ladung** (je nach Wärmeweg) ist nicht abgezogen. Bei einem 18-K-Kaltstart hebt das C um ~0,10 kWh/K (0,47 → 0,57), bei 10 K um ~0,17.
- **Was in Q0 steckt (wahrscheinlich):**
  - WP-Inhalt, Plattenwärmetauscher und Ladeleitungen von ~30 auf 50–58 °C. Nach Ladeende kühlen sie in den Technikraum bzw. ins Heizungsnetz ab. Der gemeinsame Vorlauffühler steht +20 min noch +13 K über dem Start (Speicherrollen-Analyse, Abschnitt 5).
  - Zirkulation während der Ladung.
  - Rest-Fühlerfehler (Bodenzone unter SF2, Fühlerträgheit).
- **Schichtung/Fühlerlage (Vermutung, Effekt klein):** C_netto hängt nicht vom SF2-Startwert ab (Abschnitt 3.1). Ein großer ungesehener Kaltbereich müsste bei warmem SF2-Start ein deutlich höheres C liefern als bei kaltem. Das ist nicht der Fall.
- **Restliche Differenz 0,51 (Regression) bzw. 0,47 (Kaltstarts) gegen 0,46 (379 l + Stahl):** Sie liegt innerhalb ±1 σ der Steigung. Dazu kommt die Unsicherheit der Hoval-Durchflussmessung, nicht geeicht, vermutlich ±5–10 %. **Nicht weiter auflösbar** mit diesen Fühlern.

## 5. Rohwert-Stichproben (wörtlich, zum Gegenprüfen)
Spalten `ww_hires.csv`:
`zeit,WW_Status,SLP,SLP_HW_Ausgang,WW_Ist,WW_Betriebswahl,WW_Soll,WW_Soll_eff,Speicher_Sollwert,AnlageSoll_WW,WW_Warmhalte,Vorlauf,Ruecklauf,WP_VL,WP_RL,P_el,P_th,Modulation,WEZ_Leistung,Leistung_Soll,Status_HK1,Kuehlventil_UKA,Pumpe_HK1,Aussen,Fehlercode,WW_Unten_SF2`
Spalten `ww_abnahme.csv`:
`zeit,1504_wez_ww,1550_slp,1500_sf,1499_ww_soll,1521_ladesoll,18725_wez_vl,1535_rl,18760_sys_vl,18726_modul,25611_pel,25612_pth,1506_q_wez,25614_e_el,27489_q_ww,19706_hk1p,19870_uka,31708_flow,1477_aussen,delta_vl_minus_ww`

**Stichprobe 1: 12.09.2026 07:41–08:22 (saubere Ladung, SF2-Start 30 °C)**
```
ww_hires  2026-09-12 07:41:21,0,0,0,452,4,500,500,0,0,45,330,315,329,316,0,0,0,0,-1270,0,0,0,95,255,303
ww_hires  2026-09-12 07:41:31,1,1,0,452,4,500,500,0,0,45,330,315,329,316,0,0,0,0,-1270,0,0,0,95,255,303
ww_hires  2026-09-12 08:22:51,0,1,1,506,4,500,500,0,0,45,510,475,516,474,0,0,0,0,-1270,0,0,0,102,255,462
ww_hires  2026-09-12 08:52:52,0,0,0,513,4,500,500,0,0,45,450,355,450,355,0,0,0,0,-1270,0,0,0,106,255,489
ww_abnahme 2026-09-12 07:42:02,1,1,45.2,50.0,54.0,32.5,30.5,33.0,0,0.0,0,45668,0,39205,0,0,36.7,9.5,-12.7
ww_abnahme 2026-09-12 08:19:01,1,1,49.6,50.0,54.0,56.5,50.5,56.0,33,2.47,7,45673,0,39211,0,0,19.0,10.1,6.9
```
Lesart:
- Mittel Start (45,2 + 30,3)/2 = 37,75 °C, nach +30 min (51,3 + 48,9)/2 = 50,1 °C, also **ΔT 12,35 K**.
- `27489` 39205 → 39211 = **6 kWh**, Q_B = 6,82 kWh.
- C_roh = (6,82 − 0,16)/12,35 = **0,54**, netto (−1,77) = **0,40 kWh/K**.

**Stichprobe 2: 15.09.2026 05:30–06:27 (Kaltstart, eine der 4 Ladungen der 495-l-Herleitung)**
```
ww_hires  2026-09-15 05:30:12,1,0,0,436,4,500,500,0,0,45,390,355,396,354,183,10,35,1000,-40,23,0,1,109,255,197
ww_hires  2026-09-15 05:30:22,1,1,1,436,4,500,500,0,0,45,390,355,397,355,183,10,35,1000,-40,23,0,1,108,255,197
ww_hires  2026-09-15 06:27:51,0,1,0,508,4,500,500,0,0,45,490,495,492,493,0,0,0,1000,-1000,23,0,1,110,255,459
ww_hires  2026-09-15 06:57:52,0,0,0,506,4,500,500,0,0,45,380,340,378,336,175,10,35,1000,-860,23,0,1,108,255,482
ww_abnahme 2026-09-15 05:31:01,1,1,43.6,50.0,54.0,34.5,27.5,37.0,70,3.61,17,45720,0,39245,1,0,37.3,10.9,-9.1
ww_abnahme 2026-09-15 06:24:02,1,1,50.4,50.0,54.0,56.0,50.0,56.0,33,2.45,8,45731,0,39256,0,0,18.7,11.0,5.6
```
Lesart:
- Mittel Start (43,6 + 19,7)/2 = 31,65 °C, nach +30 min (50,6 + 48,2)/2 = 49,4 °C, also **ΔT 17,75 K**.
- `27489` 39245 → 39256 = **11 kWh** (alt abgelesen: 9), Q_B = 11,58 kWh.
- C_roh = **0,64**, netto = **0,54 kWh/K**.
- Die WP lief vorher schon im Heizbetrieb (P_el 1,83 kW, Status HK1 23). Der WP-Kreis war also warm, der Fixanteil dürfte hier kleiner als 1,77 sein. Das ist der höchste Kaltstartwert.

Prüfbefehl Pi: `grep -E '^2026-09-1[25] (07:41|08:2[2]|08:52|05:30|06:2[7]|06:57)' ~/hoxpi_fulllog/ww_hires.csv`

## 6. Einstufung
**Belegt (aus Rohdaten gerechnet)**
- Der Rohquotient Ladewärme / ΔT (Fühlermittel +30 min) liegt bei Kaltstarts reproduzierbar bei **0,55–0,64 kWh/K**. Die 0,576 vom 15./16.09. sind korrekt **gerechnet**, aber eine andere Größe als die Speicherkapazität.
- Über 34 saubere Ladungen gilt Q = C·ΔT + Q0 mit **C = 0,49–0,57 kWh/K** (je nach Wärmeweg und Zeitpunkt, ±0,05) und **Q0 = 1,65–2,1 kWh**. Ab +30 min nach Ladeende ist das Ergebnis stabil.
- Die drei Wärmewege (P_th, Flow·ΔT, `27489`) stimmen auf ±5 % überein. Sie sind nicht unabhängig, gleicher Durchflussgeber.
- An den 4 Ladungen der alten Herleitung sind die `27489`-Differenzen teils 1–2 kWh zu klein abgelesen (Fenster zu kurz).

**Wahrscheinlich**
- Die wirksame Speicherkapazität beträgt **0,46–0,51 kWh/K** (≈ 400–440 l Wasseräquivalent). Das ist mit **379 l Wasser + Stahl/Email (Datenblatt, ~0,46 kWh/K)** vereinbar. **Verbindlicher Rechenwert: 0,46 kWh/K** für Speicherinhalt, Stablauf und Ruheverlust.
- Für WP-Ladungen gilt: **Q_WP ≈ 0,5 kWh/K · ΔT + 1,8 kWh**.
- Q0 ist überwiegend Wärme in WP-Kreis und Ladeleitungen, die nach der Ladung nicht im Speicher bleibt.

**Vermutung**
- Die Restdifferenz (0,51 gegen 0,46) stammt aus der Hoval-Durchflussmessung (±5–10 %) und einer kleinen ungesehenen Bodenzone unter SF2.

**Nicht ermittelbar (mit diesen Daten)**
- C genauer als ±10 %: Es gibt nur 2 Fühler mit unbekannter Höhe, ungeeichten Durchfluss und `27489` mit 1-kWh-Auflösung.
- Wie sich Q0 auf WP-Inhalt, Leitungen und Zirkulation aufteilt.
- Eine unabhängige Gegenprobe mit dem PV-Stab: Der Loxone-Zähler misst keinen Strom (Konstante 2,82 kW). Möglich wäre sie nur mit echtem Stromzähler am Stab (der Betreiber entscheidet).

## 7. Empfehlung Dokumentation (der Betreiber entscheidet / Orchestrator)
- Memory/Skill `ww-speicher-combival-495l-pvstab`: Die 495 l / 0,576 kWh/K umdeuten in „WP-Ladewärme je K bei Kaltstart **inkl.** Fixanteil ~1,8 kWh“. Als Speicherkapazität 0,46 kWh/K eintragen.
- `02_Status_Offen.md`, Abschnitt „OR-23.10. – Widerspruch WW-Speicher wirksames Volumen“: kann mit Verweis auf diese Datei geschlossen werden.
- Folgerechnungen mit 0,576 neu bewerten, etwa die Verlust-Obergrenze 510 W in `loop_journal.md` → mit 0,46 ≈ 405 W, und „50 → 62 °C = 6,9 kWh“ → ~5,5 kWh. Die Rechnungen mit 0,44 aus `ANALYSE_Speicherrollen_…` bleiben gültig.