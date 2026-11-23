# Kühlmodus Wohnzimmer UG im Oktober — Datenanalyse
**Stand 22.10.2026 ~22:05 (Claude Code, Subagent). Nur gelesen: nichts an Loxone, Hoval oder Pi geändert.**

## Kurzfassung
- **Belegt:** Der WZ-Raumregler stand von **20.10. 16:14 bis 22.10. 04:20** (≈ 36 h) und erneut ab **22.10. 15:56** (bis jetzt) im **Kühlmodus**. Das Gleiche gilt für **Büro, Technikraum und Zimmer OG 1**.
- **Belegt:** **Gekühlt wurde im Oktober nie.** WEZ-Status 1539 war nie 2, HK1-Status 1501 nie im Kühlbereich, Kühlventil (UKA) nie 1, Kühl-Soll 19482 immer 0. Die zentrale Betriebsart steht auf **„Heizen“**.
- **Folge (wahrscheinlich):** Im Kühlmodus gibt der Regler **keine Heizanforderung** aus. Das WZ-Ventil bleibt zu, bis der Raum unter den Heiz-Sollwert fällt. Am 20.–22.10. fiel 1510 dabei von 22,5 auf 20,4 °C.
- **Holzofen:** Die beiden belegten Wechsel (20.10. und 22.10.) lagen **am Nachmittag ohne Ofen-Nachlauf** (1490 ≠ 24). An Ofenabenden mit 24–26 °C ist ein Wechsel aber sehr wahrscheinlich (nicht belegbar, keine Historie).
- **Vorschlag:** WZ-Regler in der Heizsaison auf **„Nur Heizen“** stellen oder **Komfort Kühlen auf 24,5 °C** anheben.

Zeiten: Loxone liefert UTC, hier umgerechnet auf **MESZ = UTC+2**. Der Volllogger und kuehltest.csv laufen in Ortszeit.

## Quellen
| Kürzel | Quelle |
|---|---|
| [LXH] | Loxone `control_history` (je Regler die letzten 20 Einträge, abgefragt am 22.10. ~21:56). WZ reicht zurück bis 20.10. 16:14, Zimmer OG 1 bis 19.10. 18:56 |
| [LXS] | Loxone `control_state`, Momentwerte 22.10. 21:56–22:00 |
| [XML] | `Documents\Loxone\Loxone Config\Projects\Fam der Betreiber UMBAU.Loxone`, gelesen mit `Emulation\or_kuehl_xml*_20261022_2200.py` |
| [VL] | Volllogger `~/hoxpi_fulllog/2026-10-01…22.csv(.gz)`, 5 min, Spalten = Registernummern, Skala ×0,1 °C. Auswertung: `or_kuehl_r1/r2/r3_20261022_2200.py`, Ausgabe `or_kuehl_r3_20261022_2200.out` |
| [KT] | `~/hoxpi_fulllog/kuehltest.csv`, 1 min, Spalten `Status_HK1, Kuehlventil_UKA, Soll_19482, AnlageSoll_Kuehl, Strategie …`, 01.–22.10. = 31 560 Zeilen |
| [DOC] | Loxone-KB „Intelligent Room Controller“ (lokale Kopie `Loxone-Umbau\loxone-skill\extern\lox-cli\docs\kb\intelligent-room-controller.md`, Quelle https://www.loxone.com/enen/kb/intelligent-room-controller/) |

## 1. Welche Regler standen wann im Kühlmodus?
**Wo man es sieht:** Am Raumregler zeigen es der Ausgang **AQs „Heiz-/Kühlmodus“** (1 = Heizen, −1 = Kühlen, 0 = aus; laut [DOC]) und in der App bzw. MCP der Zustand **`currentMode`** [LXS].
Im Aktivitätslog [LXH] stehen die Einträge „Zwischen Heizen und Kühlen umgeschaltet → Kühlen aktiviert“ und „'Klimacontroller UG' wird zum Kühlen verwendet“.
`currentMode` 1 bzw. 2 passt zu den Einträgen „Heizen“ bzw. „Kühlen“ im Log. Diese Zuordnung ist **wahrscheinlich**, aber nicht offiziell dokumentiert. Den Wert 4 (WC UG, Garage) konnte ich nicht zuordnen.

| Regler (UUID) | Kühlmodus (MESZ) | Rückkehr zu Heizen | `currentMode` 22.10. 21:56 | Quelle |
|---|---|---|---|---|
| **Wohnzimmer** `<UUID>` | **20.10. 16:14:54** („wird zum Kühlen verwendet“) | **22.10. 04:20:57** („Vorbereitung Heizphase Komfort“, „zum Heizen verwendet“) | 2 | [LXH] |
| Wohnzimmer | **22.10. 15:56:52** („Zwischen Heizen und Kühlen umgeschaltet → Kühlen aktiviert“) | — (Ziel 23,5 = Eco Kühlen) | 2, `tempTarget` 23,5, `tempActual` 22,1 | [LXH], [LXS] |
| Zimmer OG 1 `<UUID>…` | 19.10. 19:39 – 20.10. 14:00; 20.10. 16:14 – (spätestens) 22.10. 09:37 | 22.10. 09:37:34 „Heizen aktiviert“ | 1 | [LXH] |
| Büro `<UUID>…` | 22.10. 13:57, 14:39, 17:00, 18:11 (wiederholt „zum Kühlen verwendet“) | — | 2 | [LXH] |
| Technikraum `<UUID>…` | 22.10. 13:14 bis jetzt („Vorbereitung der Kühlphase“ 19:00) | — | 2 | [LXH] |
| WC UG, Garage | im Log nur Heizen bzw. Standby | — | 4 (Bedeutung unklar) | [LXH], [LXS] |

- **01.–19.10. lässt sich nicht ermitteln.** Die Historie umfasst nur 20 Einträge, für IRoomControllerV2 gibt es keine Statistik („isn't chartable“), und der Ofenlogger zeichnet keinen Modus auf.
- **Indiz (Vermutung):** Laut [VL] lag 1510 an folgenden Tagen in Summe so viele Stunden ≥ 22,5 °C: 08.10. 1 h, 10.10. 6 h, 11.10. 9 h, 12.10. 2 h, 16.10. 7 h, **17.10. 13 h**, 18.10. 9 h, 19.10. 6 h, 20.10. 2 h. Dort dürfte das WZ ebenfalls in den Kühlmodus gewechselt haben.
- **Auslöser** laut [DOC]: Mit zwei Komforttemperaturen wechselt der Regler in den Kühlmodus, sobald die Komfort-Kühltemperatur **überschritten** wird. Erst unter der Heiztemperatur wechselt er zurück, der Bereich dazwischen ist die „Floating Zone“.
  Beim WZ ist diese Zone nur **21,5–22,5 °C** breit [LXS `comfortTemperature` / `comfortTemperatureCool`]. In der Eco-Zeit reicht sie sogar von **20,0 bis 23,5 °C** (`absentMinOffset` 1,5, `absentMaxOffset` 1,0).
- Die **Außentemperatur-Logik wird nicht genutzt**: Beim WZ gilt `useOutdoor` = 0 und `actualOutdoorTemp` = −1000 [LXS]. Der Klimacontroller UG hingegen sperrt Kühlen über das 48-h-Mittel: `outdoorTempMode` = 1, `minimumTempCooling` = 19, `maximumTempHeating` = 17, außen aktuell 10,9 [LXS]. Laut [XML]-NDOC sind dort 15/18 °C eingestellt; der Livewert weicht davon ab.

## 2. Wurde tatsächlich gekühlt? — Nein (belegt)
| Prüfung | Ergebnis 01.–22.10. | Quelle |
|---|---|---|
| WEZ-Status `1539` (2 = Kühlen) | **0-mal 2.** Vorkommende Werte: 0, 1 (Heizen), 4 (WW), 8, 16, 51. Beispiel 20.10.: {0: 246, 4: 17, 1: 25} | [VL] r1 |
| HK1-Status `1501` / `Status_HK1` (9/10/11/14/22 = Kühlen) | nur **0, 23 (Heizen extern), 6** — kein Kühlwert | [KT], [VL] r3 |
| `Kuehlventil_UKA` (Reg. 19870) | **31 560 von 31 560 Zeilen = 0** | [KT] |
| `Soll_19482` (Kühl-Soll von Loxone) / `AnlageSoll_Kuehl` | immer 0 / immer 0 | [KT] |
| Betriebswahl WEZ `1561` | immer 1 (Automatik), nie 5 (Manuell Kühlen) | [VL] r2 (01., 19.–22.10.) |
| VL < RL − 0,5 K bei laufendem Verdichter | 6 Einzelproben (07.10. 2×, 10., 11., 19., 20.10.). Geprüft: 19.10. 17:30 und 20.10. 11:40, beide mit 1539 = 4 (WW-Ladung, VL/RL am WP-Ausgang), also keine Kühlung | [VL] r1/r2 |
| Zentrale Betriebsart (Radio `<UUID>…`) | `activeOutput` = 2 → „Heizen“ (Umsetzung: 1 Standby / 2 Heizen / 3 Kühlen / 4 Automatik) | [LXS], [XML] |
| Klimacontroller UG `<UUID>…` | `mode` 2, `demandCool` 0, `demandHeat` 25 (22.10. 21:56) | [LXS] |

- **Belegt:** Die Wärmepumpe hat im Oktober nicht gekühlt. Auch Loxone hat keinen Kühlbefehl an die Hoval geschickt.
- Im WZ-Log steht bei Kühlende „**Kühlen wird vom Regler nicht erlaubt**“ (20.10. 19:12). Der Kühlmodus blieb also **reine Regler-Logik**.
- Am 20.10. 16:14 meldeten WZ, Zimmer OG 1 und Technikraum **gleichzeitig** (±2 s) „zum Kühlen verwendet“, am 20.10. 19:12 ebenso gleichzeitig „nicht mehr verwendet“ (auch Zimmer OG 2). Der Auslöser lag also beim Klimacontroller, nicht im Raum.
  Was dort umschaltete, **lässt sich nicht ermitteln**, weil der Klimacontroller keine Historie führt.

## 3. Folgen: Ventil zu, Fußboden kühlt aus?
- **Belegt [DOC]:** „The source outputs only set the control value when the source is in the same mode.“ Der Klimacontroller heizt, der Raum steht auf Kühlen. Damit gibt `AQhc1` im WZ **0** aus.
- **Wahrscheinlich:** Der Regler bleibt im Kühlmodus, bis der Raum unter den **Heiz**-Sollwert fällt. In der Eco-Zeit sind das 20,0 °C. Am 20.–22.10. dauerte das ~36 h. Zurück zu Heizen ging es erst mit der Vorbereitung der Komfortphase (22.10. 04:20).

| Zeit (MESZ) | WZ-Modus [LXH] | 1510 Raum (Hoval) [VL] | außen 1477 Ø [VL] | 1490 HK1-Soll max [VL] | Bemerkung |
|---|---|---|---|---|---|
| 20.10. 18:00 | Kühlen | 22,3–22,5 | 13,5 | 0,0 | |
| 21.10. 03:00 | Kühlen | 21,4–21,5 | 14,3 | 0,0 | |
| 21.10. 14:00 | Kühlen | **20,9–21,0** | 15,2 | 0,0 | |
| 21.10. 15–18 h | Kühlen | 21,0–21,5 | 12,4–14,3 | 29,3–29,5 | HK1 heizt für andere Räume, WZ zu |
| 22.10. 04:00 | → Heizen (04:20) | **20,4–20,6** (Minimum) | 7,5 | 31,5 | |
| 22.10. 15:00 | → Kühlen (15:56) | 22,0–22,3 | 11,2 | 0,0 | Nachmittag |
| 22.10. 21:00 | Kühlen, Ziel 23,5 | 21,3–21,4 | 4,4 | 0,0 | `tempActual` 22,1 [LXS] |

- **Komfortverlust: belegt klein.** 1510 fiel auf höchstens 20,4 °C. T_A (Loxone) liegt bis 0,8 K über 1510, siehe Holzofen-Analyse. Die Bodentemperatur ist **nicht messbar**, weil es keinen Bodenfühler gibt.
- **Bei kaltem Wetter (Vermutung):** Liegt es nachts deutlich unter 0 °C und war tagsüber Ofen oder Sonne, ist das WZ dann bis 20,0 °C ohne Heizung. Erst danach öffnet das Ventil wieder, und der träge Estrich braucht Stunden bis zur Erholung.
- **Holzofen:** Am 20.10. und 22.10. gab es **keinen Ofen-Nachlauf** (1490 nie 24,0 [VL]). Beide Wechsel geschahen nachmittags, wahrscheinlich durch Sonne oder interne Gewinne. **Wahrscheinlich** wechselt der Regler auch an jedem Ofenabend mit T_A > 22,5 °C in den Kühlmodus (Max-Werte 16.–18.10. 24,0–25,8 °C). Belegen lässt sich das mangels Historie aber nicht.
  Die `Ofen_An_Formel` (2,5 = 25 % bei T_B − T_A > 5 K) überbrückt diesen Zustand **teilweise**: I3 = 0 wird dann durch 2,5 ersetzt [XML, Holzofen-Analyse]. Nach dem Ofen (Differenz < 5 K) bleibt das Ventil zu.
- **Nebenbefund [XML]:** Die Formel „Heizen/Kühlen“ `IF(I1>26;1;IF(I1<21;2;0))` hängt am **HK1-Vorlauf (1-Wire)** und nicht am Raumregler. Sie liefert I4 der `Ofen_An_Formel`.
  Fällt der HK1-Vorlauf unter 21 °C, erzwingt `IF(I4>1;0;…)` das WZ-Ventil auf 0, auch gegen den Regler und den Ofen-Zweig. Ob das im Oktober vorkam, ist **nicht geprüft**, weil der 1-Wire-VL für 20.–22.10. nicht geloggt ist.

## 4. Einstellvorschlag Loxone (nur Vorschlag, nichts geändert)
Doku: Intelligente Raumregelung https://www.loxone.com/dede/kb/intelligente-raumregelung/ (die Seite meldete am 22.10. „vorübergehend nicht verfügbar“; EN: https://www.loxone.com/enen/kb/intelligent-room-controller/ bzw. www.loxone.com/help/intelligent-room-controller). Klimacontroller: www.loxone.com/help/hvac-controller.

| Nr | Wo | Parameter | Ist | Vorschlag | Was bringt uns das |
|---|---|---|---|---|---|
| 1 (zuerst) | Raumregler **Wohnzimmer** (in der App: Einstellungen → Betriebsmodus; in Config: Eingang/Parameter **Mode**) | **Mode** | 0 = Automatik (Heizen *oder* Kühlen) [`operatingMode` 0] | **1 = Automatik, nur Heizen** (Okt.–Apr.) | Der Raum kann nicht mehr in den Kühlmodus fallen. Das Ventil öffnet wieder, sobald der Raum unter 21,5 (Komfort) bzw. 20,0 (Eco) fällt, statt bis 36 h zu bleiben. Laut [DOC] sind die Kühlausgänge dabei aus. Im Sommer zurück auf 0 |
| 1b | Büro, Technikraum, Zimmer OG 1, Zimmer OG 2 (alle hängen am Klimacontroller UG) | **Mode** | 0 | 1 im Winterhalbjahr | Dasselbe Verhalten in allen UG-Räumen. Die Umschaltung ließe sich an die zentrale Betriebsart koppeln: Radio Q2 „Heizen“ → Mode 1 |
| 2 (Alternative) | Raumregler Wohnzimmer | **ϑcc Komfort Kühlen** (`TComfortC`) | 22,5 °C | **24,5 °C** (Loxone-Default) | Die Floating Zone wird 21,5–24,5 statt 21,5–22,5 breit, und Nachmittagssonne löst keinen Wechsel mehr aus. Ofenabende (bis 25,8 °C) lösen trotzdem noch aus, deshalb ist Nr. 1 besser |
| 3 | Raumregler Wohnzimmer | **ϑec Eco Kühlen** (`TSaveU`) | 1,0 → 23,5 °C | bei Nr. 2 egal; bei Mode 1 wirkungslos | — |
| 4 | Klimacontroller UG | `TempLimitC` (Min. Außentemp. Kühlen) / `TOm` | Live 19 / 48-h-Mittel | lassen | Blockiert das echte Kühlen im Herbst bereits zuverlässig (belegt: nie gekühlt) |

Die Sommerkühlung (Kühlen 22,0–22,5 °C, Taupunktschutz) bleibt unberührt, wenn Mode im Mai wieder auf 0 gestellt wird. Die Kühltemperatur gehört dann eher auf 22,5–23,0 °C, damit die Floating Zone ≥ 1 K bleibt.

## 5. Noch offen / nicht ermittelbar
- Kühlmodus-Zeiten 01.–19.10.: es gibt keine Loxone-Historie. **Ab jetzt mitloggen:** `currentMode` aller Raumregler (`control_state`, z. B. 5-minütlich im Ofenlogger).
- Was am 20.10. 16:14 und 19:12 im Klimacontroller UG umschaltete: Er führt keine Historie, `currentStatus` 8192 ist undokumentiert.
- Bedeutung von `currentMode` = 4 (WC UG, Garage).
- 1510 stand am 20.10. von 12 bis 16 h exakt konstant auf 21,0. Die Ursache (Ersatzwert?) ist nicht geprüft.