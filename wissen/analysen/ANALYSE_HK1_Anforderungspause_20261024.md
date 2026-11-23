# ANALYSE: Warum fällt die HK1-Anforderung 5–25 min weg, obwohl Räume demand = 1 melden? (Katalog F21, OR 24.10.2026 08:00)

Nur gelesen: Projektdatei `[lokaler Pfad]`, Volllogger `~/hoxpi_fulllog/` 18.–24.10., Loxone-MCP `control_state` Klimacontroller UG, Raumlogger `[lokaler Pfad]`. Skripte `[lokaler Pfad]`.

## 1. Signalkette zu Reg 1490 (sicher, Projektdatei)
`ModbusAActor 'Sollvorlauftemperatur Heizen HC1'` (ModbusAddress 1490, RepeatRate 300 s) ← `Formula '1490 inkl. Ofen-Nachlauf (min. 24 °C)'`
`IF(I2>0; MAX(I1;24); IF(I1>0; I1; IF(I3>0; MAX(I4;20); 0)))` mit
- I1 = `AnalogMultiplexer 'Sollwert Heizen 1490'`, Select ← **`HVACController 'Klimacontroller HC1'` (Visu „Klimacontroller UG“) Ausgang OutHeat1** (Input1 = Heatmixer2 „Vorlautemperatur HC1“),
- I2 = Ofen-Nachlauf aktiv, I3 = Monoflop „Kurzlauf-Schutz 15 min“ (nach Verdichterstart), I4 = VF1.
→ 1490 = 0 genau dann, wenn OutHeat1 = 0 und weder Ofen-Nachlauf noch Kurzlauf-Schutz aktiv sind. Die Pausen kommen also aus dem **Klimacontroller UG**, nicht aus Raumreglern, Ofenlogik oder Hoval.

## 2. Parameter Klimacontroller HC1 (sicher, Projektdatei + live)
OnThreshold (Sot) **30 %** (live `threshold` = 30), TimePump (MinHr) **60** (Stand 23.10. 19:29; vorher 40), TimePulseOn 750 / TimePulseOff 300 s, PulseThreshold (MaxTp) nicht gesetzt = 0 = Taktung aus, FanDelay 180 s.
Loxone-Doku (https://www.loxone.com/enen/kb/climate-controller/, DE: https://www.loxone.com/dede/kb/klima-controller/): „Average valve openings of the Intelligent Room Controllers must exceed (Sot) in order to start operation“; MinHr muss vor Standby erfüllt sein; nach dem Abschalten 3 min Sperre zusätzlich zu Fod.

## 3. Mechanismus (wahrscheinlich, nahe sicher)
Der Controller mittelt die **Ventilöffnung über alle 8 UG-Raumregler** (live-State `demandHeat`). `demand = 1` eines Raumreglers heißt nur „will heizen“, nicht „Ventil weit offen“. Liegen 3–4 Räume knapp unter Soll (kleine Öffnung) und der Rest bei 0, bleibt der Mittelwert < 30 % → nach Ablauf von MinHr fällt OutHeat1 → 1490 = 0. Steigt der Mittelwert wieder > 30 % (frühestens nach 3 min Sperre + 3 min FanDelay), kommt die Anforderung zurück.

## 4. Belege
| Zeitpunkt | Beleg | Ergebnis |
|---|---|---|
| 24.10. 07:50 | Volllogger: Block 05:30–07:50 endet (1520 → 0) | Pause beginnt |
| 24.10. 07:56:48 (State-ts 05:56:48Z) | Loxone live `demandHeat` = **26**, `threshold` = 30, `stage` = 0 | **26 % < 30 % → aus (sicher)** |

Blockmuster Volllogger 18.–24.10. (5-min-Raster, 25 Anforderungsblöcke): 17 Blöcke dauern 40–50 min (= MinHr 40 + Raster), Pausen ≤ 25 min danach 5× (19.10. 19:00, 22.10. 07:55, 23.10. 17:20 / 18:10 / 19:10). Das ist die Signatur „MinHr abgelaufen, Mittelwert < Sot“.

## 5. Nebenbefund WC UG operatingMode 3 / currentMode 4 (Vermutung)
WC UG steht als einziger Raum nicht auf 1/1. Bedeutung laut IRC-V2-Statusliste nicht belegt (Vermutung: manueller Modus) — bleibt offen, beeinflusst den Mittelwert nur über seine Ventilöffnung.

## 6. Bewertung / Was bringt uns das
- Kein Fehler, sondern die eingebaute Einschaltschwelle. Startvorhersage für Loxone/MinHr: Anforderung endet frühestens nach MinHr und dann, sobald `demandHeat` < 30.
- Hebel (nur Vorschlag, Entscheidung der Betreiber): Sot 30 → 20 % hielte die Anforderung bei 3 offenen Räumen; Gegenwirkung: mehr Laufzeit bei kleinem Bedarf, ggf. Überheizen. Seit MinHr 60 (23.10.) sollten die Kurzpausen ohnehin seltener werden — erst die MinHr-60-Abnahme (1 Woche) abwarten.
- Für die zweite Live-Bestätigung: `demandHeat` des Klimacontrollers UG (UUID <UUID>) im Raumlogger mitschreiben (nur lesen) und bei der nächsten Pause mit Zeitstempel festhalten.

Status F21: **teilweise** — Logik mit Objektname/Parameter benannt (sicher), 1 Pause live mit demandHeat < Sot bestätigt, 2. Pause nur über demand-Zählung.



### 7.1 Zweite Pause aus dem Loxone-Aktivitätsprotokoll (sicher)
Quelle: `control_history` Raumregler WC UG (UUID <UUID>), Volllogger `~/hoxpi_fulllog/2026-10-23.csv` / `2026-10-24.csv` (Skript `Emulation\or_f21i_20261024_0900.py`, nur lesen).

| Zeit lokal (Loxone-ts UTC) | Loxone-Aktivitätsprotokoll | Volllogger 1490 / 1520 / 1501 | Bewertung |
|---|---|---|---|
| 24.10. 05:26:03 (03:26:03Z) | "'Klimacontroller UG' wird zum Heizen verwendet" | 05:30 313/540/6 (WW-Ladung, danach Heizblock) | Blockstart |
| 24.10. 07:52:14 (05:52:14Z) | "'Klimacontroller UG' wird nicht mehr verwendet" - Ventile geschlossen, Standby | 07:45 311/340/23 -> 07:50 0/0/0 | Pause; live demandHeat 26 < 30 (siehe §4) |

Damit sind **zwei Pausen mit Zeitstempel** belegt (22:23 mit Loxone-eigenem Grund "unzureichende Anforderung", 07:52 mit demandHeat 26 < threshold 30). Versatz: Volllogger zeigt 07:50:02 schon 0, Loxone-Eintrag 07:52 - Miniserver-Uhr bzw. Protokolleintrag ~2-3 min hinter dem Pi (Vermutung; 22:23 vs. 22:25 passt).


### 7.2 WC UG operatingMode 3 / currentMode 4 (sicher für Mode, wahrscheinlich für currentMode)
- Loxone-KB Intelligente Raumregelung (per WebFetch gelesen: https://www.loxone.com/enen/kb/intelligent-room-controller/ - die dede-Fassung unter loxone.com/dede/kb/ nicht geprüft): Mode 0 = Automatik Heizen+Kühlen, **1 = Automatik nur Heizen**, 2 = Automatik nur Kühlen, **3 = Festsollwert (ϑt), Heizen ODER Kühlen je nach Ist/Soll**, 4 = Festsollwert nur Heizen, 5 = Festsollwert nur Kühlen.
- Projektdatei `[lokaler Pfad]` (und `UMBAU_wwprognose_20261023_NEU.Loxone`), Eingang AMode (Skript `Emulation\or_f21h_20261024_0900.py`):

| Raumregler | AMode | Quelle |
|---|---|---|
| Wohnzimmer, Büro, Technikraum, Zimmer OG 1, Zimmer OG 2, Hütte | verbunden | InputRef "Heizsaison (Mode UG-Raumregler)" (Kühlfallen-Umbau) |
| Badezimmer | **fest 1** (nicht verbunden) | Automatik nur Heizen - unkritisch |
| **WC UG** | **fest 3** (nicht verbunden) | Festsollwert, Heizen **und Kühlen** erlaubt |
| Garage | fest 4 | Festsollwert nur Heizen, kein Klimacontroller |

- Live WC UG: operatingMode 3, tempTarget 22,5 (Festsollwert), tempActual 21,7, demand 1. currentMode 4 tritt auch bei der Garage (Mode 4) auf -> wahrscheinlich Temperaturmodus "manuell/Festwert", nicht Kühlen (Vermutung zur genauen Zuordnung).
- **Folge:** WC UG hängt nicht am Kühlfallen-Umbau. Steigt es über Soll + Toleranz, darf es laut Mode 3 in den Kühlmodus wechseln (wahrscheinlich, noch nie beobachtet). Außerdem fordert WC UG mit festen 22,5 °C fast dauernd Wärme an und hebt demandHeat - es ist einer der zwei Räume, die jetzt die Anforderung tragen.

### 7.3 Was bringt uns das
- F21 ist abgeschlossen: Pausen = Klimacontroller UG nach MinHr bei mittlerer Anforderung < Sot 30 %; bei Ofenabenden hält die Ofen-Nachlauf-Formel 1490 noch ~30 min auf 24 °C. Startvorhersage: neuer Block erst, wenn demandHeat >= 30.
- Neu F22 (Entscheidung der Betreiber): WC UG AMode wie die anderen an "Heizsaison (Mode UG-Raumregler)" hängen oder fest auf 1 stellen - schließt die Kühlfalle auch für WC UG. Nichts geändert.

Status F21: **erledigt** (OR 24.10. 09:00).