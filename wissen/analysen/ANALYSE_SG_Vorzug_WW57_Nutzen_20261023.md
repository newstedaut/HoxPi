# ANALYSE: Lohnt sich die SG-Anhebung WW auf 57 °C? (23.10.2026, Orchestrator, nur lesend)

**Frage:** Bringt die Smart-Grid-Vorzug-Anhebung des WW-Solls auf 57 °C (statt 50/52) unterm Strich etwas, und ist sie besser als der PV-Heizstab?

**Ergebnis (3 Zeilen)**
1. **Ja, knapp.** Die 57er-SG-Ladungen laufen **ohne messbaren COP-Nachteil** (AZ 3,36 gegen 3,33 normal) und schieben die nächste Netzladung im Median um **~5–6 h** (11,2 h statt 5,5 h Abstand) in die Nacht/den Morgen.
2. **Aber:** Das SG-Signal „hängt nach“: 5 von 34 SG57-Ladungen starteten nach 17 Uhr, 1× um 06:20; in 2 von 9 Stichproben lief die SG-Ladung **aus dem Netz** (heute 23.10. 16:05–16:40 mit +8,5…9,4 kW Netzbezug, Wallbox parallel).
3. **WP auf 57 schlägt den Heizstab** um Faktor ~3,4 je kWh PV. Der Heizstab lohnt nur, wenn die WP schon fertig ist **und** die Einspeisevergütung unter ~6 ct/kWh liegt.

**Was bringt uns das:** Heute grob **+1,5 bis +5 €/Monat** (≈ 15–40 €/Jahr, Annahme Einspeisung 8 ct, Netz 21 ct). Mit sauberer SG-Freigabe (nur bei echter Einspeisung, 10–16 Uhr) fallen die Netz-SG-Ladungen weg (~0,5 €/Monat). Den größeren Hebel hat der **Heizstab**: 2026 bisher **1 197 kWh** (Loxone-Zähler „Heizstab Trinkwasser“, totalYear). Bei 8 ct Einspeisung waren das **≈ −20 €** gegenüber Einspeisen, weil 1 kWh PV in der WP etwa 3,4 kWh Wärme bringt.

---

## Daten und Methode
- Volllogger `~/hoxpi_fulllog/2026-07-30.csv.gz … 2026-10-23.csv` (5-min, 24 253 Zeilen), Spalten = Registernummern, Rohwerte ×10.
- Verwendete Spalten: `1500` WW-Ist SF1 (oben), `1497` WW-Soll, `1521` Speicher-Ladesoll, `1550` SLP, `18725` WEZ-Vorlauf, `18726` Modulation %, `25611` P_el (Roh/100 = kW), `25614` E_el gesamt (kWh), `27489` Wärmemenge WW (kWh, **erst ab 01.09. 11:20 befüllt**), `27537`/`31741` Status Smart Grid (0 = aus, 1 = SG aktiv, 255 = ungültig), `1477` außen.
- Ladung: `1550` = 1 zusammenhängend, mindestens 10 min. E_el = Integral `25611`. Wärme = Differenz `27489` (1 Zeile vor Start bis 2 Zeilen nach Ende, Auflösung 1 kWh). AZ = Σ Wärme / Σ E_el je Gruppe.
- Gruppe „SG“, wenn `27537` während der Ladung = 1 war. „SG57“ = SG und Soll ≥ 56 (seit 20.09. aktiv, vorher SG-Soll 54, im August keine Anhebung).
- Strom/Netz: Loxone „Hauptstromzähler“ (Meter, bidirektional, `actual` in 10-min-Stützpunkten, + = Bezug, − = Einspeisung, Vorzeichen **wahrscheinlich**, passt zu −2,7 kW mittags). Doku: https://www.loxone.com/dede/kb/zaehler/ · Energiemanager: https://www.loxone.com/dede/kb/energiemanager-gen-2/
- Skripte: `[lokaler Pfad]` (Pi lesen), `_2_ladungen.py/.out` (alle 217 Ladungen), `_3_auswertung.py/.out`, `_4_verschiebung.py/.out`. Extrakt: `or_sg57_20261023_extrakt.csv`.
- Plausibilität: Σ E_el aus Integral 242,6 kWh gegen Zähler `25614` 225 kWh (n = 112, ab 01.09.). Das Integral liegt ~8 % höher, die AZ-Werte unten sind deshalb eher **konservativ** (mit Zähler ≈ +8 %).

### Stichproben-Rohzeilen (wörtlich aus dem Extrakt, Spaltenfolge wie Kopf)
```
zeit,1477,1497,1499,1500,1504,1521,1550,18725,18726,25611,25614,27489,27537,31741,1513,1535
2026-10-23 16:20:02,106,570,570,517,1,610,1,580,33,262,30397,39985,1,1,209,540
2026-10-13 12:30:02,96,570,570,500,1,610,1,570,33,250,30273,39735,1,1,207,515
```
Gelesen: 23.10. 16:20 → außen 10,6 °C, Soll 57,0, WW-Ist 51,7, Ladesoll 61,0, SLP an, VL 58,0, Mod 33 %, **P_el 2,62 kW**, SG = 1. 13.10. 12:30 → WW 50,0, VL 57,0, Mod 33 %, P_el 2,50 kW, SG = 1.

## 1. Ladungen nach Gruppe (ab 01.09.2026, mit Wärmezähler)
| Gruppe | n | Dauer min | T0 SF1 | T_end SF1 | kWh_el/Ladung | kWh_th/Ladung | **AZ** | VL max | Mod % | außen | Abstand zur nächsten Ladung (Median) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SG57 (Soll 57) | 34 | 46 | 50,4 | 55,7 | 1,88 | 6,3 | **3,36** | 60,5 | 34 | 14,6 | 7,0 h |
| SG54 (01.–19.09.) | 9 | 53 | 46,2 | 54,6 | 2,25 | 8,6 | 3,81 | 59,6 | 35 | 18,7 | 17,8 h |
| SG50–52 | 5 | 39 | 46,8 | 52,3 | 1,64 | 6,2 | 3,78 | 57,5 | 37 | 16,6 | 9,6 h |
| normal, Soll 57 (Boost ohne SG) | 22 | 57 | 48,0 | 52,8 | 2,75 | 8,4 | 3,05 | 57,5 | 40 | 11,2 | 6,6 h |
| normal, Soll 50–52 | 53 | 45 | 45,7 | 51,5 | 2,15 | 7,2 | **3,33** | 56,4 | 42 | 11,8 | 5,8 h |

Nur Tagladungen mit Start 10–17 Uhr, ab 20.09.: SG57 n = 28, AZ 3,38, T_end 56,1 · normal 50–52 n = 8, AZ 3,34, T_end 51,1 · normal 57 n = 6, AZ 2,88.

## 2. AZ gegen Endtemperatur (ab 01.09., Σ Wärme / Σ Strom je Klasse)
| T_end SF1 | n | AZ | VL max | außen | SG-Anteil |
|---|---|---|---|---|---|
| < 50,5 | 4 | 3,84 | 51,0 | 11,8 | 0 % |
| 50,5–52,5 | 45 | 3,44 | 56,7 | 13,0 | 16 % |
| 52,5–54,5 | 41 | 3,11 | 57,6 | 12,0 | 17 % |
| 54,5–56,0 | 10 | 3,44 | 59,4 | 15,2 | 90 % |
| ≥ 56,0 | 25 | 3,40 | 61,6 | 14,6 | 100 % |
| nur außen 8–16 °C: ≤ 52,5 / 52,5–55 / ≥ 55 | 31 / 32 / 20 | 3,40 / 3,04 / 3,34 | | 11,9 / 11,3 / 13,2 | |

- **Belegt:** Eine höhere Endtemperatur kostet in diesen Daten **kaum Arbeitszahl**. Bei gleicher Außentemperatur sind es −2 % (3,40 → 3,34). Die schlechteste Klasse (52,5–54,5) besteht aus langen Zapf-/Boost-Ladungen ohne SG mit Modulation 40–44 %.
- **Wahrscheinlich:** Die SG57-Ladungen sind effizient, weil sie warm starten (T0 50,4), nur ~5 K nachladen, auf Modulation 33 % (Minimum) laufen und mittags bei 14–15 °C Außentemperatur stattfinden. Die Vorteile Außenluft und kleine Leistung gleichen den höheren Hub aus.
- **Einschränkung:** `27489` ist die von Hoval **errechnete** Wärmemenge (kein echter WMZ) mit 1 kWh Auflösung. Pro einzelner Ladung ±15 %, in der Gruppensumme brauchbar.

## 3. Effekt: zusätzliche Energie im Speicher, Verschiebung, Mehrverlust
| Größe | Wert | Sicherheit |
|---|---|---|
| T_end SF1 SG57 / normal (Median, ab 20.09.) | 56,5 / 52,5 °C → ΔT 4,0 K | belegt |
| Zusatzwärme im Speicher je SG57-Ladung | 379 l × 1,163 Wh/(l·K) × 4,0 K ≈ **1,8 kWh_th ≈ 0,52 kWh_el** (bei AZ 3,36) | wahrscheinlich (setzt voll durchmischten Speicher voraus, Schichtung macht es eher weniger) |
| Ganze SG57-Ladung | Ø 1,88 kWh_el / 6,3 kWh_th, Start bei T0 50,4 (normal startet bei ~46,7) → wird **nur durch die Anhebung ausgelöst** | belegt |
| Abstand SG57 → nächste Normalladung | Median **11,2 h** (Q1 6,6 / Q3 15,5), n = 33 | belegt |
| Abstand Normalladung → nächste Ladung | Median **5,5 h**, n = 61 | belegt |
| Mehrverlust durch höhere Temperatur | UA ≈ 3,3 kWh/d ÷ (50 − 20 K) = 0,11 kWh/(d·K). Ø ~3 K Überhöhung über ~11 h → **≈ 0,15 kWh_th je SG-Ladung** (≈ 0,05 kWh_el) | **Annahme** (linear mit ΔT, Aufstellraum 20 °C) |
| Eingesparter Netzstrom je SG57-Ladung | konservativ nur Zusatzwärme: (1,8 − 0,15) ÷ 3,33 ≈ **0,5 kWh_el**. Optimistisch, wenn die ganze Ladung eine spätere Netzladung ersetzt: (6,3 − 0,15) ÷ 3,33 ≈ **1,85 kWh_el** | wahrscheinlich (Spanne) |
| Häufigkeit | 34 SG57-Ladungen in 34 Tagen (20.09.–23.10.) ≈ **1 pro Tag** | belegt |

## 4. Lief die SG-Ladung wirklich aus PV? (Loxone Hauptstromzähler, 10-min, Zeiten UTC+2 umgerechnet)
| SG57-Ladung (Ortszeit) | Netz `actual` während der Ladung | Einordnung |
|---|---|---|
| 27.09. 12:15–13:25 | +0,05 … −0,04, Spitzen −2,7 | ≈ 0 → PV/Akku |
| 04.10. 16:50–18:00 | −0,01 … +0,09 | ≈ 0 → PV/Akku (17–18 Uhr eher Akku) |
| 07.10. 12:15–13:15 | −0,31 … +0,28 | ≈ 0 → PV/Akku |
| 09.10. 16:00–16:55 | +0,02 … +0,15 | ≈ 0 → PV/Akku |
| **13.10. 12:10–13:00** | **−2,8 … −6,6 kW** | **echte Einspeisung, Idealfall** |
| 17.10. 14:05–14:50 | −0,18 … +0,32 | ≈ 0 → PV/Akku |
| **19.10. 17:30–18:30** | **+3,2 … +5,5 kW** | **Netzbezug** |
| 22.10. 13:15–13:50 | −2,9 → ≈ 0 | ≈ 0 → PV/Akku |
| **23.10. 16:05–16:40** | −1,0 / 0,0, **dann +8,5 … +9,4 kW** (Wallbox 5,7 kW parallel) | **überwiegend Netz** |

- **Belegt:** In 1 von 9 Stichproben gab es echte Einspeisung, in 6 von 9 lag das Netz bei ≈ 0, in 2 von 9 kam der Strom aus dem Netz.
- **Nicht ermittelbar:** Ob „Netz ≈ 0“ PV oder Hausakku war. Es gibt einen Akku (Energiemanager: `Ssoc` 96 %, `MinSoc` 95 %), aber im Loxone keine Statistik für die Akku- oder PV-Leistung. Akkustrom für die WW-Ladung fehlt abends und ist dann indirekt Netzstrom (plus ~10 % Akkuverlust).
- **Belegt:** SG = 1 steht oft bis in den Abend an. SG57-Starts: 17:25, 17:30, 17:45, 18:30, 19:10 und **14.10. 06:20**. Diese Ladungen bringen nichts und kosten den Mehrverlust.

## 5. WP auf 57 °C oder PV-Heizstab?
| Je 1 kWh PV-Überschuss | WP (SG57) | Heizstab |
|---|---|---|
| Wärme in den Speicher | **3,36 kWh_th** (gemessen, AZ SG57) | 1,0 kWh_th |
| Ersetzt spätere WP-Netzladung (AZ 3,33) | 1,0 kWh_el | 0,30 kWh_el |
| Wert bei 21 ct Netz | **21 ct** | **6,3 ct** |
| Entgangene Einspeisung (**Annahme 8 ct**, bitte echten Tarif prüfen) | 8 ct | 8 ct |
| **Netto je kWh PV** | **+13 ct** | **−1,7 ct** (bei < 6,3 ct Einspeisung positiv) |

- Heizstab 2026: **1 197 kWh** (totalYear), Oktober 7 kWh. Bewertet: 1 197 ÷ 3,33 × 21 ct ≈ 75 € Heizwert gegenüber 96 € Einspeisung (8 ct) ≈ **−20 €**. Bei 5 ct Einspeisung wären es +15 €. Die Bilanz hängt also am Einspeisetarif. **Wahrscheinlich:** Der Heizstab bringt den Speicher über 57 °C. Das ist Zusatzwärme mit Mehrverlust, deshalb hier eher ungünstig gerechnet.
- Die WP-Kappe liegt bei 62 °C VL (Ladesoll 61 = Soll 57 + 05-001). Über ~57 °C SF1 kommt nur der Heizstab.

## Einstellvorschlag (nur Vorschlag, der Betreiber entscheidet; Loxone-Änderung nur mit Backup und Skill `loxone-xml-umbau`)
1. **SG57 behalten**, aber das SG-Vorzug-Signal in Loxone nur setzen, wenn **Hauptstromzähler `actual` < −2,0 kW über ≥ 10 min (echte Einspeisung) UND 10:00–16:30 Uhr**. Abschalten erst bei Bezug > 0 kW über 10 min. Die Abend- und Morgen-SG-Ladungen fallen dann weg. Akkuladung vorher abwarten (z. B. `Ssoc` ≥ `MinSoc`), damit die WW-Ladung den Akku nicht leert.
   **Rückweg:** alte Loxone-Datei aus dem Backup zurückspielen bzw. den bisherigen SG-Auslöser wieder verbinden. **Prüfen:** 2 Wochen SG57-Startzeiten (alle 10–17 Uhr?) und den Netzwert während der Ladung.
2. **Heizstab als 2. Stufe:** Freigabe nur, wenn WW ≥ 56 °C (WP fertig) **und** Einspeisung > 3 kW. Bleibt der Einspeisetarif ≥ 7 ct, den Heizstab ganz aus lassen bzw. auf ein kleineres Max-Soll (z. B. 60 °C) begrenzen. **Rückweg:** Daytimer „Heizstab Zeitfenster (leer = nur PV)“ und die Energiemanager-Prio unverändert lassen und die Bedingung wieder entfernen.

## Was bringt uns das (grob)
| Posten | Rechnung | €/Monat |
|---|---|---|
| SG57 heute (≈ 30 Ladungen/Monat, 7 von 9 aus PV oder Akku) | konservativ 0,5 × 21 − 0,52 × 8 ≈ 6 ct, optimistisch 1,85 × 21 − 1,88 × 8 ≈ 24 ct je Ladung | **+1,5 … +5,5** |
| Netz-SG-Ladungen streichen (Vorschlag 1) | ~5–7 Ladungen/Monat × (Mehrverlust + Akkuverlust) ≈ 0,1–0,2 kWh_el | ≈ +0,3 … +0,5 |
| Heizstab hinter die WP stellen bzw. nur bei billiger Einspeisung | 2026 bisher −20 € (bei 8 ct) | im Sommer ≈ +2 … +4 |

**Fazit:** Die 57er-Anhebung lohnt sich, solange sie wirklich auf PV-Überschuss läuft. Sie kostet keine Effizienz, und der Speicher dient als billiger Wärmeakku für etwa 5–6 h. Mehr als ein paar Euro im Monat bringt sie aber nicht. Wichtiger sind ein sauberer SG-Auslöser und die richtige Rangfolge WP vor Heizstab.

## Offen
- Echter Einspeisetarif (Annahme 8 ct). Wenn bekannt, die Heizstab-Zeile neu rechnen.
- Akku- und PV-Leistung sind im Loxone nicht als Statistik abrufbar. Ohne sie ist der PV-Anteil der „Netz ≈ 0“-Ladungen nicht ermittelbar.
- Wie das SG-Signal in Loxone entsteht (Auslöser Reg 27546 = 2, Logik im Projekt) und warum es abends und um 06:20 anliegt, ist nicht geprüft.