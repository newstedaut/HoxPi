# ANALYSE F57 – PV-Heizstab: kWh je Tag, Anteil an der WW-Wärme, Legionellenzähler (01.11.2026)

Erstellt 01.11.2026 ~16:00 (Claude, Analyse-Agent, nur lesend). Keine Schreibzugriffe auf Anlage, Loxone oder Pi.

## Frage
1. Wie viel kWh liefert der Heizstab im WW-Speicher je Tag seit 01.09.2026?
2. Welchen Anteil an der WW-Wärme hat er, wie viel WP-WW-Ladung spart er?
3. Setzt ein Heizstab-Lauf den Loxone-Wert „Tage seit Legionellenschutz" (UUID <UUID>) zurück, und unter welcher Bedingung?

## Datenquellen
| Größe | Quelle | Auflösung |
|---|---|---|
| Heizstab-Energie | Loxone Meter „Heizstab Trinkwasser" (UUID <UUID>), `control_statistics` Gruppe 2, diff/day und diff/hour; Gruppe 1 = Leistung | 0,001 kWh; Tagesbucket 00:00 Ortszeit |
| WP-WW-Wärme | Volllogger `~/hoxpi_fulllog/<Tag>.csv(.gz)` auf dem Pi, Reg **27489** „Wärmemenge WW (kWh)" (Zuordnung aus `[lokaler Pfad]`) | **1 kWh** (Ganzzahl) |
| WW-Ist oben | Volllogger Reg 1500 (×10), Reg 1504 (WW-Ladung WP), 25611/25612 (P_el/P_th) | 5 min, Zeitstempel CET |
| Legionellen-Logik | `[lokaler Pfad]` (neueste lokale Datei, 25.10.2026 13:03), nur gelesen (Select-String) | – |
| Legionellen-Zähler live | `loxone__control_state` UUID <UUID> | – |
| Netzbezug | Loxone Meter „Hauptstromzähler" (UUID <UUID>), diff/hour | – |

## Methode
- Heizstab: Tagesdiff des Loxone-Zählerstands. Loxone-Zeitstempel sind UTC (Bucket 22:00Z = 00:00 MESZ, ab 25.10. 23:00Z = 00:00 MEZ).
- WP-WW-Wärme: Reg 27489 erster Wert des Folgetags minus erster Wert des Tages (Volllogger, `awk` per SSH, nur lesend).
- Anteil Heizstab = Q_Stab / (Q_Stab + Q_WP,WW). Annahme: Stab-Strom = Wärme 1:1 [sicher, ohmsch]; Speicherverluste nicht abgezogen.
- Ersparnis WP-Strom: Q_Stab / Arbeitszahl WW ~3,0 (Projektwert, `ANALYSE_Arbeitszahl_Aussen_20261022.md`) [Vermutung: nur gültig, wenn jede Stab-kWh eine WP-kWh ersetzt].

## Ergebnis 1 – kWh je Tag (Heizstab) und WP-WW-Wärme

| Tag | Heizstab kWh (Loxone) | WP-WW kWh_th (Reg 27489) | Anteil Stab | Reg 1500 max °C |
|---|---|---|---|---|
| 01.09. | 1,8 | 10 | 16 % | 52,7 |
| 02.09. | 1,5 | 10 | 13 % | 53,1 |
| 03.09. | 0,7 | 9 | 7 % | 52,8 |
| 04.09. | 8,1 | 21 | 28 % | 62,0 |
| 05.09. | 0,0 | 9 | 0 % | 52,8 |
| 06.09. | 8,3 | 22 | 27 % | – (Ausreißer 3276,8) |
| 07.09. | 3,0 | 38 | 7 % | 58,3 |
| 08.09. | 3,9 | 10 | 28 % | 61,7 |
| 09.–11.09. | 0,0 | 10 / 24 / 9 | 0 % | 58,0 / 50,8 / 50,8 |
| 12.09. | 3,0 | 11 | 21 % | 54,2 |
| 13.09. | 0,3 | 7 | 4 % | 54,5 |
| 14.09. | 0,5 | 22 | 2 % | 55,5 |
| 15.09. | 4,3 | 17 | 20 % | 61,9 |
| 16.09. | 4,4 | 22 | 17 % | 55,1 |
| 17.09. | 0,3 | 19 | 1 % | 53,1 |
| 18.09. | 0,0 | 8 | 0 % | 55,5 |
| 19.09. | 3,5 | 11 | 24 % | 56,6 |
| 20.09. | 5,1 | 16 | 24 % | 61,7 |
| 21.09. | 0,0 | 10 | 0 % | 58,3 |
| 22.09. | 4,3 | 12 | 27 % | 58,7 |
| 23.09. | 6,5 | 10 | 39 % | 61,9 |
| 24.09. | 0,0 | 30 | 0 % | 53,0 |
| 25.09. | 3,3 | 10 | 25 % | 61,7 |
| 26.09. | 3,5 | 9 | 28 % | 61,9 |
| 27.09. | 3,7 | 13 | 22 % | 61,4 |
| 28.09. | 3,1 | 18 | 15 % | 61,7 |
| 29.09. | 7,3 | 25 | 23 % | 61,7 |
| 30.09. | 7,4 | 3 | 71 % | 61,9 |
| 01.10. | 7,0 | 4 | 64 % | 61,7 |
| 02.10.–31.10. | **0,0 an allen 30 Tagen** | 702 gesamt = 23,4/Tag | 0 % | 58,9 (02.10.), sonst ≤ 57,3 |
| 01.11. (bis 15:55) | **9,56** | 10 | 49 % | 62,0 |

Quellen je Spalte siehe „Datenquellen". Reg 27489 hat nur 1-kWh-Auflösung, Einzeltage daher ±1 kWh [sicher].

**Summen [sicher, aus obigen Zählern]:**
- September (30 Tage): Heizstab **87,9 kWh = 2,9 kWh/Tag**, WP-WW 445 kWh = 14,8 kWh/Tag → Stab-Anteil **16,5 %**.
- 01.09.–01.10. (31 Tage): Stab 94,9 kWh, WP-WW 449 kWh → **17,5 %**.
- 02.10.–31.10.: Stab **0 kWh**, WP-WW 23,4 kWh/Tag (+8,6 kWh/Tag ggü. September).
- Loxone-Jahreszähler Heizstab 2026: 1206,6 kWh, Gesamtzählerstand 3354,1 kWh (control_state 01.11. 14:53Z).
- Reg 1500 erreicht ~62 °C praktisch nur an Stab-Tagen (04., 08., 15., 20., 23., 25.–30.09., 01.10., 01.11.) [sicher]; die WP allein kommt im Oktober nicht über 58,9 °C.

**Ersparnis WP-WW-Ladung:**
- Im September hat der Stab ~88 kWh_th WW-Wärme geliefert, die sonst die WP hätte liefern müssen → bei AZ_WW ~3,0 rund **29 kWh WP-Strom/Monat ≈ 1 kWh_el/Tag** gespart [wahrscheinlich, Obergrenze: ein Teil der Stab-Wärme ist Mehrverlust durch 59–62 °C statt 50 °C].
- Das „Sparen" lohnt nur, wenn der Stab mit PV-Überschuss läuft: Stab-kWh (COP 1) kostet sonst 3× so viel Netzstrom wie die WP [sicher, physikalisch].
- Seit 01.10. sperrt die Tarifformel „PV-Heizstab lohnt" (`IF(I1*100<21,15/MAX(2;2,34+0,071*I2);1;0)`, Einspeisetarif vs. Netzpreis/COP) den PV-Zweig. Das erklärt die 30 Null-Tage im Oktober [wahrscheinlich – Tarifverlauf nicht nachgelesen].

## Ergebnis 2 – 01.11.2026, der Lauf heute
Zeiten Volllogger = MEZ, Loxone = UTC (+1 h).

| Zeit (MEZ) | Ereignis | Quelle |
|---|---|---|
| ~12:00 | Heizstab EIN, 2,5 kW | Loxone Meter Leistung, Stundendiff 11Z = 2,50 kWh |
| 13:05–13:35 | WP-WW-Ladung (Reg 1504 = 1), 46,8 → 51,4 °C, Reg 27489 +4 kWh | Volllogger |
| 13:40–15:50 | WP aus WW (1504 = 0), Reg 1500 52,4 → 62,0 °C nur durch Stab; P_el > 0 nur in Heiz-Takten (11:55, 14:25, 15:35) | Volllogger |
| ~15:20 | Reg 1500 ≥ 60 °C (60,4) | Volllogger |
| 15:54:07 | Heizstab AUS (0 kW) | Loxone Meter Leistung, 14:54:07Z |
| 15:54:21 | „Tage seit Legionellenschutz" 7,92 → **0** | control_state, 14:54:21Z |

- Heizstab heute: **9,56 kWh** (11Z 2,50 + 12Z 2,50 + 13Z 2,50 + 14Z 2,06) [sicher].
- **Das war kein PV-Lauf, sondern der Legionellen-Pflichtlauf** (Sonntag 12–18 UND Zähler ≥ 6,5 d). Netzbezug Hauptstromzähler 12–16 Uhr MEZ: 4,97 / 6,01 / 5,56 / 3,48 kWh, Einspeisung ~0 → Stab lief **aus dem Netz** [sicher für Bezug, wahrscheinlich für Ursache].
- Die Aussage „52,0 → 58,5 °C von 13:39–14:54 ohne WP" deckt sich mit dem Volllogger, wenn die Zeiten MEZ sind (13:40 52,4; 14:55 58,5) [sicher].

## Ergebnis 3 – Was setzt den Legionellenzähler zurück?
Kette laut `[lokaler Pfad]` (Abschnitt „10. LEGIONELLEN-WAECHTER (24.10.2026)") [sicher für die Datei, wahrscheinlich für den laufenden Miniserver – Datei ist der Stand 25.10.]:

1. Formel „Legionellen: kühlerer oberer Fühler" = `MIN(I1;I2)` aus 1-Wire-Fühler „Warmwasserspeicher oben" und Hoval SF1 „Aktuelle Warmwasserspeichertemperatur Oben" (= Reg 1500).
2. Schwellwertschalter „kühlerer Fühler ab 60 °C (aus unter 59,5)".
3. Einschaltverzögerung „Legionellen-Nachweis: 30 min ab 60 °C" (Time 1800 s).
4. Ausgang → Reset des Betriebsstundenzählers „Legionellenschutz: Zeit seit letztem Nachweis" (Wartungsintervall 864000 s = 10 d).
5. „Tage seit Legionellenschutz" = `MAX(0;10-AQr)` → Merker UUID 21fab044-0070-… (das InfoOnlyAnalog in der App).
6. Folgen: ≥ 6,5 d → „fällig" → Pflichtlauf So 12–18 (Schaltuhr „Heizstab Legionellen-Pflichtfenster (So 12-18)"), Heizstab-Ziel 62 statt 59 °C; ≥ 3 d UND PV-Prognose ≥ 26 kWh → PV-Legionellen-Tag; > 10 d → Push „Legionellenschutz überfällig". Nachweis triggert außerdem 10 min Zirkulationsspülung.

**Befund:**
- **Ja, der Heizstab setzt den Zähler zurück – aber nicht weil er der Heizstab ist**, sondern weil er den Speicher oben auf ≥ 60 °C (kühlerer der zwei Fühler) für 30 min bringt. Jede Wärmequelle, die das schafft, würde zurücksetzen; die WP schafft es nicht (Oktober-Max Reg 1500 = 58,9 °C) [sicher für Logik in der Datei, sicher für Oktober-Daten].
- Heute belegt: Reg 1500 ab ~15:20 MEZ ≥ 60 °C, Reset um 15:54:21 MEZ = ~30 min später, Zähler 7,92 → 0 [sicher: Live-Wert 0 seit 14:54:21Z; Zeitlücke passt zur 30-min-Verzögerung].
- Stab-AUS 14 s vor dem Reset (15:54:07): wahrscheinlich hat der 2-Punkt-Regler (1-Wire oben, Ziel 62, Hyst 2 K) abgeschaltet bzw. „fällig" fiel – Reihenfolge aus den Loxone-Zeitstempeln nicht sicher trennbar [Vermutung].
- Rückrechnung: 7,92 d am 01.11. 13:55 → Zählerstart ≈ 24.10. ~12 Uhr = Einbau des Wächters. Seitdem kein Nachweis bis heute, also war der heutige Pflichtlauf der erste Reset [wahrscheinlich].

## Stichprobe (nachprüfbar)
01.11.2026: Loxone „Heizstab Trinkwasser" (UUID <UUID>) totalDay = **9,5638 kWh** (control_state, ts 2026-11-01T14:53:57Z); Stundendiff 11Z/12Z/13Z/14Z = 2,50/2,50/2,50/2,06 kWh (control_statistics diff/hour, Gruppe 2). Gegenprobe Volllogger `~/hoxpi_fulllog/2026-11-01.csv` Reg 1500: 13:40 = 524, 15:50 = 620 (×10), Reg 1504 = 0 dazwischen.

## Offen
- Laufende Miniserver-Konfiguration nicht direkt gelesen; Logik stammt aus der lokalen Datei vom 25.10. – nach späteren Umbauten erneut prüfen.
- Einspeisetarif im Oktober nicht ausgelesen → Sperre durch Tarifformel nur wahrscheinlich.
- Stab-Wärme ist nicht von Mehrverlust (höhere Speichertemperatur) trennbar; netto-Ersparnis daher Obergrenze.
- Heutiger Pflichtlauf aus Netzstrom: ~9,6 kWh_el für eine Ladung, die die WP mit ~3,2 kWh_el bis 58 °C hätte machen können.

## Was bringt uns das
- PV-Stab brachte im September 2,9 kWh/Tag (16,5 % der WW-Wärme) und sparte ≈ 1 kWh WP-Strom/Tag – im Oktober nichts, weil gesperrt.
- Der Legionellen-Wächter funktioniert: erster Reset heute nach 30 min ≥ 60 °C. Er hängt am Heizstab, weil die WP 60 °C nicht erreicht.
- Kostenhebel: Pflichtlauf So 12–18 läuft im Winter aus dem Netz (heute 9,6 kWh). Option zur Entscheidung (der Betreiber): Pflichtlauf erst nach WP-Vorladung auf 57 °C starten oder Intervall prüfen (aktuell fällig ab 6,5 d).