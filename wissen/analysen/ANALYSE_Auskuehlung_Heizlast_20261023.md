# ANALYSE Auskuehlung und Heizlast aus der ersten kalten Nacht (22./23.10.2026)

Orchestrator-Unterauftrag 23.10.2026 ~05:00, **nur lesend** (kein Schreiben an Anlage/Bus/Loxone). Datenende: 23.10. 04:55.

## Datenquellen
| Kuerzel | Pfad | Inhalt |
|---|---|---|
| [VL] | Pi `~/hoxpi_fulllog/2026-10-15..21.csv.gz`, `2026-10-22.csv`, `2026-10-23.csv` (5 min) | 1477 Aussen AF1 (0,1 C), 1490 HK1-Soll Konstantanf. (von Loxone), 1510 Raum-Ist HK1 (Hoval-Raumwert, gegen WZ kalibriert, laeuft bis 0,8 K kaelter als WZ-T_A), 1513 VL-Ist HK1, 1529 HK-Soll, 1535 RL, 18726 Modulation, 1505/1506 Waerme ges. (U32), 27484/85 Waerme Heizen (U32), 27488/89 Waerme WW (U32), 25613/14 Strom (U32), 1519 Starts |
| [WH] | Pi `~/hoxpi_fulllog/ww_hires.csv` (1 min) | Status_HK1, Modulation, P_el (10 W), P_th (ganze kW), Aussen, Vorlauf/Ruecklauf |
| [ALT] | `ANALYSE_Takt_Abtau_Nacht_22-23Okt_20261023.md`, `ANALYSE_Datenqualitaet_Volllogger_Winter-AZ_20261023.md`, `ANALYSE_Raumventile_Heizkurve_Winter_20261022.md`, `ANALYSE_Heizsoll_1490_1529_Aussen_20261022.md` | Registerbedeutungen, Loxone-Kette (Heatmixer2 HC1 Steilheit 0,9 / Max 40, Klimacontroller UG threshold 30, Heizgrenze 17 C) |
| Skripte | `or_auskuehl_20261023_a.py/.out` (Laufbeginn), `_b.py/.out` (Tagesbilanz Zaehler), `_c.py/.out` (Raum 1510 Nacht + Tagesmittel) | alles in `[lokaler Pfad]` |

Loxone-Raumregler (IRoomControllerV2) sind ueber `control_statistics` **nicht chartbar** -> Raumverlauf nur aus Hoval-Register 1510 (ein Fuehler, WZ-nah). U32-Zaehler: hi*65536+lo; High-Words 1505/27484 = 1 im ganzen Zeitraum.

## Kurzfazit
- **Auskuehlung (belegt):** 22.10. 18:59 Verdichter aus -> 23.10. 03:00 ohne jede Heizung (8 h). Raum 1510: **21,2 -> 20,6 C** (-0,6 K) bei Aussen 6,4 -> 2,8 C (Mittel ~4,3 C, dT innen-aussen ~17 K). Mittlere Rate **~0,075 K/h**, bezogen auf dT **~0,0045 K/h je K** -> effektive Zeitkonstante **~200-250 h** (schweres Haus + Estrich-Speicher). Von 19:00 bis 01:00 blieb der Raum praktisch konstant (21,2-21,4), der Abfall kam erst 01:00-03:00 (21,4 -> 20,6).
- **Erster Heizstart 23.10. (belegt):** Anforderung `Status_HK1` = 23 ab **03:00:52**, Verdichter **03:01:51 - 03:40:52 (39 min)**, VL-Soll 1490 = **33,1-33,2 C** (1529 HK-Soll 36,0 C), Modulation 47 -> 35 %, P_el ~1,8 kW, Aussen 2,8 -> 2,6 C. Ende durch `Status_HK1` -> 0 (Loxone), nicht durch Hoval. Waerme Heizen +5 kWh (03:00-04:00). Danach ab 04:30 WW-Ladung.
- **Heizlast (wahrscheinlich, grob):** WP-Heizwaerme 20.-22.10. (ohne Ofentage) 61 kWh in 72 h bei mittl. dT 10,6 K -> **~80 W/K nur WP**; mit geschaetzten inneren/solaren Gewinnen **~100-130 W/K**. Hochgerechnet auf -15 C (Annahme): **~3-5 kW** fuer den heute beheizten Bereich.
- **Vergleich C17 (Annahme ~17 kW nominal, grob):** Die WP ist fuer die heute gemessene Last **3-5-fach ueberdimensioniert**; selbst bei 35 % Mindestmodulation liefert sie 7-8 kW (P_th am 23.10. 03:40 = 8). -> Takten/Anforderungsbetrieb ist bauartbedingt, nicht Fehler.

## 1. Belegt (Messung)

### 1a Nachtverlauf ohne Heizung [VL], Auszug (5-min-Raster, hier 1/h)
| Zeit | Aussen 1477 | Raum 1510 | VL-Ist HK1 1513 | 1490 | Mod |
|---|---|---|---|---|---|
| 22.10. 18:00 | 8,4 | 21,3 | 19,9 | 0 | 0 |
| 22.10. 19:00 | 6,4 | 21,2 | 20,1 | 0 | 0 |
| 22.10. 21:00 | 4,7 | 21,3 | 19,6 | 0 | 0 |
| 22.10. 23:00 | 4,3 | 21,4 | 18,9 | 0 | 0 |
| 23.10. 01:00 | 3,8 | 21,4 | 18,2 | 0 | 0 |
| 23.10. 02:00 | 3,5 | 21,0 | 18,1 | 0 | 0 |
| 23.10. 03:00 | 2,8 | 20,6 | 18,0 | 0 | 0 |
| 23.10. 03:30 | 2,7 | 20,5 | 30,5 | 33,2 | 37 |
| 23.10. 04:00 | 2,5 | 20,5 | 26,2 | 0 | 0 |
| 23.10. 04:45 | 2,3 | 20,5 | 22,5 | 0 | 44 (WW) |

- Rate gesamt 19:00 -> 03:00: -0,6 K / 8 h = **0,075 K/h** bei dT ~17 K -> **0,0044 K/(h*K)** -> tau = 1/0,0044 **~225 h** (~9 Tage).
- Teilabschnitt 01:00 -> 03:00: -0,8 K / 2 h = 0,4 K/h. Das ist fuer ein Haus mit tau > 100 h **zu schnell** als reine Gebaeudeauskuehlung (siehe Vermutung 3b).
- Nach dem 39-min-Lauf stieg 1510 **nicht** messbar (20,6 -> 20,5 -> 20,5): typisch fuer Fussboden, die Waerme steckt im Estrich.

### 1b Erster Heizlauf 23.10. [WH]
Ablauf aus `ww_hires.csv` (Zeilen mit Zustandswechsel): 03:00:52 `Status_HK1`=23, `Pumpe_HK1`=1, noch Mod 0 -> 03:01:51 Mod 42, P_el 1,79 kW -> 03:40:52 Mod 35, P_el 1,82 kW, P_th 8, Status_HK1 -> 0 -> 03:41:52 Mod 0.
Zaehler [VL]: 27485 (Heizen lo) 7033 -> 7038 (+5 kWh), 25614 Strom 30383 -> 30384 (+1 kWh, 1-kWh-Aufloesung), Starts 1519 20706 -> 20707.

### 1c Tagesbilanzen [VL] (00:00-24:00, Zaehler-Differenz, U32)
| Tag | Aussen Mittel (min/max) | Raum 1510 Mittel (max) | dT | Waerme HZ kWh | Waerme WW kWh | Strom kWh | Starts |
|---|---|---|---|---|---|---|---|
| 16.10. | 9,75 (5,5/15,4) | 22,05 (**25,8**) | 12,3 | 27 | 16 | 11 | 10 |
| 17.10. | 10,96 | 22,82 (24,2) | 11,9 | 10 | 29 | 10 | 7 |
| 18.10. | 11,91 | 22,59 (24,0) | 10,7 | 11 | 17 | 8 | 8 |
| 19.10. | 11,15 | 22,17 (23,9) | 11,0 | 7 | 34 | 12 | 8 |
| 20.10.* | 10,87 | 21,15 (22,5) | 10,3 | 44 | 15 | 13 | 10 |
| 21.10. | 13,42 | 21,47 (22,1) | 8,1 | 5 | 28 | 10 | 6 |
| 22.10. | 7,75 (4,1/11,7) | 21,16 (22,3) | 13,4 | 12 | 31 | 13 | 7 |
| **Summe 7 Tage** | **10,83** | | **11,1** | **116** | **170** | **77** | 56 |
\* 20.10. CAN-Ausfall 12:23-17:10, Zaehler holen danach nach (Tagessumme gueltig, Verteilung nicht).

- 7-Tage-Mittel: 116 kWh / 168 h = 0,69 kW Heizwaerme bei dT 11,1 K -> **62 W/K** (nur WP-Waerme). AZ gesamt 286/77 = **3,7**.
- Tage mit Ofen erkennbar: **16.-19.10.** (1510 max 23,9-25,8 C, Tagesmittel 22,2-22,8). An diesen Tagen ist die WP-Heizwaerme klein (7-11 kWh, 16.10. 27). Am 22.10. abends **kein** Ofen-Anstieg in 1510 sichtbar.

### 1d Rohdatenbelege (woertlich)
1. `~/hoxpi_fulllog/ww_hires.csv`, 2026-10-23 03:01:51 (erster Verdichter-Datenpunkt des Heizlaufs). Kopf:
   `zeit,WW_Status,SLP,SLP_HW_Ausgang,WW_Ist,WW_Betriebswahl,WW_Soll,WW_Soll_eff,Speicher_Sollwert,AnlageSoll_WW,WW_Warmhalte,Vorlauf,Ruecklauf,WP_VL,WP_RL,P_el,P_th,Modulation,WEZ_Leistung,Leistung_Soll,Status_HK1,Kuehlventil_UKA,Pumpe_HK1,Aussen,Fehlercode,WW_Unten_SF2`
   `2026-10-23 03:01:51,0,0,0,464,4,500,500,0,0,45,270,265,277,267,179,1,42,1000,170,23,0,1,28,255,426`
2. `~/hoxpi_fulllog/2026-10-23.csv`, 2026-10-23 03:05:01, Spaltenauswahl `cut -d, -f1,2,15,30,31,38,39,44,54,60,201,273,363,365,366`:
   `zeit,1477,1490,1505,1506,1513,1514,1519,1529,1535,18726,19562,25611,25613,25614`
   `2026-10-23 03:05:01,28,331,1,47004,227,180,20707,360,300,42,331,198,0,30383`
3. `~/hoxpi_fulllog/2026-10-23.csv`, 2026-10-23 03:00:01 (letzter Punkt vor dem Lauf, Spalten zeit/1477/1510/1513/1490/18726 aus `_c.out`):
   `2026-10-23 03:00:01,A=28,R1510=206,VL1513=180,S1490=0,Mod=0`

## 2. Wahrscheinlich
- **Heizlast-Kennwert ohne Ofentage:** 20.-22.10.: 61 kWh / 72 h = 0,85 kW bei dT 10,6 K -> **~80 W/K** WP-Anteil. Dazu kommen innere Gewinne (Personen, Geraete, ~0,3-0,5 kW) und Sonne (Oktober tagsueber relevant). Damit **H gesamt ~100-130 W/K** fuer den heute beheizten Bereich.
- **Gegenprobe ueber tau:** tau ~225 h und H ~100-130 W/K ergibt eine wirksame Speichermasse von ~22-29 kWh/K. Fuer 2 x 100 m2 mit Estrich + massiven Waenden plausibel -> die beiden Wege widersprechen sich nicht.
- **Hochrechnung Normaussentemperatur (ANNAHME -15 C fuer Alpenort (~960 m) ~960 m, nicht geprueft), Raum 21 C -> dT 36 K:** 80 W/K -> 2,9 kW; 130 W/K -> 4,7 kW. **Heizlast ~3-5 kW** (ohne WW, ohne Ofen).
- **Vergleich C17 (ANNAHME ~17 kW nominal, bei A-7/W35 grob 13-17 kW):** Nennleistung ~3-5x Heizlast. Mindestmodulation 33-35 % ergibt hier real 7-8 kW thermisch -> auch bei -15 C liegt die Last unter der kleinsten Stufe. Die WP wird auch im Kernwinter im Ein/Aus-Betrieb laufen (Puffer 400 l [⚠ Korr. 23.10.2026: Puffer = EnerVal 300, 282,4 l] + Estrich puffern das).
- Der 03:00-Start kam, weil die Loxone-Raumanforderung (Summe `demandHeat` >= threshold 30, [ALT]) bei 1510 = 20,6 C ueberschritten wurde; der Lauf endete ebenfalls durch Loxone.

## 3. Vermutung
- **3a** Dass `Status_HK1` genau zwischen 02:59:52 und 03:00:52 kam, kann Zufall sein oder ein Loxone-Zeitpunkt (Nachtabsenkung-Ende / Zeitprogramm 03:00). Nicht geprueft.
- **3c** Ob das OG heute schon ueber HK1 mitbeheizt wird, ist aus den Pi-Daten nicht sicher; falls nur UG: Heizlast nach OG-Inbetriebnahme grob x1,7-2 -> **~5-9 kW** bei -15 C - immer noch klar unter C17.

## 4. Nicht ermittelbar
- Raumtemperaturen der einzelnen Loxone-Raeume als Zeitreihe (IRoomControllerV2 nicht chartbar, Ofenlogger nur 11.-17.10.).
- Ofen-Waermemenge (kein Zaehler) -> Ofentage verfaelschen H nach unten.
- Strom nur des Heizlaufs (25614 hat 1-kWh-Aufloesung; P_el x 39 min ~1,2 kWh -> AZ des Laufs grob ~4, unsicher).
- Echte Normaussentemperatur Alpenort (~960 m) (OENORM-Wert nicht nachgeschlagen).

## 5. Einstellvorschlag (nur Vorschlag, der Betreiber entscheidet)
Kette laut [ALT]: Loxone **Heizungsmischer** "Heatmixer2 HC1" (Steilheit 0,9, Max 40 C) + Klimacontroller UG -> Reg 1490. Doku: https://www.loxone.com/dede/kb/heizungsmischer/ , https://www.loxone.com/dede/kb/klimacontroller/ , https://www.loxone.com/dede/kb/intelligente-raumregelung/

1. **Heizkurve nicht anheben.** 33 C VL-Soll bei 2,8 C aussen hat gereicht: 8 h ohne Heizung kostet nur ~0,6-1 K, ein 39-min-Lauf deckt das. Steilheit 0,9 bleibt.
2. **Heizgrenze (Klimacontroller `maximumTempHeating`) 17 C lassen.** Bei H ~100-130 W/K und inneren Gewinnen liegt die echte Heizgrenze eher bei ~14-16 C; eine Absenkung auf 15 C waere moeglich, bringt aber wenig, weil die Raumanforderung (threshold 30) ohnehin nur bei Bedarf startet.
3. **Optional, Test 1 Woche: Heizen in die warmen Stunden schieben.** Komfort-Soll WZ/UG tagsueber 12-18 Uhr +0,5 K, nachts 22-06 Uhr -0,5 K (Intelligente Raumregelung, Zeitschaltprogramm). Bei tau ~225 h haelt der Estrich das locker. Abbruch, wenn 1510 morgens < 20,3 C.

### Was bringt uns das
- Punkt 1/2: keine hoeheren VL-Temperaturen -> AZ bleibt bei ~3,7+, keine Ueberheizung zusaetzlich zum Ofen.
- Punkt 3: Laeufe bei z. B. 10 C statt 3 C aussen -> grob **10-15 % weniger Strom pro kWh Waerme** (Vermutung, Erfahrungswert Luft-WP), **weniger Abtauungen** (bisher nur bei 2-3 C beobachtet), mehr PV-Eigenverbrauch, und nachts kein Verdichter (Laerm).
- Die Heizlast-Zahl (~3-5 kW) erklaert, warum die C17 taktet: sie ist fuer dieses Haus zu gross. Statt Fehlersuche am Takten lohnt eher, Laeufe **lang und selten** zu halten (Puffer nutzen, Anforderung buendeln).

## 6. Naechste Messung
- Naechste Nacht < 0 C: dieselbe Auswertung (`or_auskuehl_20261023_c.py` Datum anpassen) -> tau und W/K mit groesserem dT bestaetigen.
- Eine ofenfreie Woche mit Aussen-Mittel < 5 C liefert den belastbarsten W/K-Wert.