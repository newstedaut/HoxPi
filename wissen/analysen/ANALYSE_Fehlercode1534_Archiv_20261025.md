# ANALYSE Katalog F36 – Reg 1534 (Fehlercode) im ganzen Volllogger-Archiv (25.10.2026)

## Frage

## Quellen (nur gelesen)
- Volllogger auf dem Pi: `/home/<user>/hoxpi_fulllog/*.csv.gz` – **86 Dateien**, `2026-07-30.csv.gz` (erste Zeile 30.07. 22:26:07) bis `2026-10-23.csv.gz` (letzte Zeile 23.10. 23:55:02), 24.455 Zeilen. (Auftrag nannte 92 Dateien; vorhanden sind 86 Tage, 24./25.10. noch nicht gepackt.)
  - Kopf: Spalte `zeit` + Registernummern. Zwei Kopfvarianten (515 Spalten bis 02.08., 556 ab 03.08.), alle benötigten Spalten in beiden vorhanden.
  - `1534` steht **roh, nicht ×10** (Werte 255/0/[Nummer]). Temperaturen ×10 (z. B. `1477` = 249 → 24,9 °C).
  - Verwendete Spalten: `1539` WEZ-Status, `1540` Betriebsstatus, `1543` StatusInformation, `1536` WEZ-Leistung %, `18726` Modulation %, `1477` AT, `1525` WEZ-VL, `1535` RL, `18742` RL WEZ, `1504` Status WW, `1501` Status HK1, `18722` Zustand WEZ-Regler, `18723` Status FA, `1490` HK1-Soll, `1500` WW-Ist.
- Auswerteskripte (nur lesend, Pi): `/tmp/f36a.py` (Episoden + Lücken, Ausgabe `/tmp/f36a.out`), `/tmp/f36b.py` (Zeilen um die Episoden).
- `[lokaler Pfad]` (Z. 15–40 OR-21.10.b / OR-21.10., Z. 134 HAICO-Uhrversatz)
- `[lokaler Pfad]` (ERR.LOG, Spalte `Modbus_1534`)
- `[lokaler Pfad]`
- `[lokaler Pfad]`, `ANALYSE_Taktschutz_V99_V101_20261022.md`, `ANALYSE_Block31903_eingefroren_20261024.md` (Ereignis 18.10. 11:10)
- Registernamen: `[lokaler Pfad]`, `hoval_status.py` (Projekt)

## Gesamtverteilung `1534` (24.455 Proben)
| Wert | Proben | Anteil |
|---|---|---|
| 255 | 23.593 | 96,5 % |
| 0 | 811 | 3,3 % |
| 190 | 34 | 0,14 % |
| 124 | 10 | 0,04 % |
| 222 | 7 | 0,03 % |
Keine anderen Werte. Leere Felder: keine.

## Logger-Lücken (Abstand > 8 min)
| von | bis | Dauer | Bezug |
|---|---|---|---|
| 09.08. 22:30:01 | 09.08. 22:45:01 | 15 min | keine 1534-Episode in der Nähe |
| 03.09. 17:15:01 | 03.09. 21:00:01 | 225 min | direkt vor der 0-Episode 03.–06.09. (Bridge/Pi-Neustart, wahrscheinlich) |
Sonst lückenlos 5-min-Raster. **Grenze des Rasters (sicher):** Ereignisse < 5 min fallen durch – z. B. E:31 (222) am **18.10. 11:10:52 für ~50 s** (Reglerreset, belegt in `ANALYSE_Taktschutz_V99_V101_20261022.md`) taucht im Volllogger **nicht** auf (Proben 11:10:0x und 11:15 = 255).

## Episodentabelle (alle Werte != 255)
| # | Wert | Beginn | Ende (letzte Probe) | n | Dauer | Zustand in der Episode ([Nummer], Mod., AT, VL/RL) | vorher → nachher (1539) |
|---|---|---|---|---|---|---|---|
| 1 | 190 | 15.08. 11:50 | 15.08. 14:20 | 31 | 150–160 min | 17/8/81, 0 %, AT 24,9, VL=RL 36,5 – **Standbild** bis 13:55 (AT, VL, RL, WW 50,1 °C 2 h konstant); ab 14:10 frische Werte 0/8/20, AT 28,0, VL/RL 18,5 | 0 Aus → 2 Kühlen (14:25, 42 %) |
| 2 | 124 | 24.08. 07:55 | 24.08. 08:00 | 2 | 5–15 min | 98/0/1, 0 %, AT 15,0, VL/RL 16,5, WW-Status 3, FA 98 | 98 (07:50, 1534 noch 255) → 4 WW, 62 % |
| 3 | 190 | 29.08. 19:25 | 29.08. 19:35 | 3 | 10–20 min | 0/8/20, 0 %, AT 21,6, VL/RL 19,5 | 0 → 2 Kühlen (19:40, 42 %) |
| 4 | 222 | 29.08. 20:10 | 29.08. 20:15 | 2 | 5–15 min | 17/8/81, 0 %, AT 20,0, VL/RL 18,5 | 0 → 0 (kein Start) |
| 5 | 124 | 03.09. 12:30 | 03.09. 12:40 | 3 | 10–20 min | 98/0/1, 0 %, AT 22,2, VL/RL 15,0, WW-Status 3 | 16 Sperre → 4 WW, 42 % |
| 6 | 0 | 03.09. 21:00 | 06.09. 11:40 | 753 | 62,7 h | Bridge ohne WEZ-Daten: 21:00–21:10 fast alle Spalten 0, danach `1535` = 0 durchgehend, `1539` = 0 | Lücke 17:15–21:00 davor → 2 Kühlen (06.09. 11:45) |
| 7 | 124 | 07.09. 08:40 | 07.09. 08:50 | 3 | 10–20 min | 98/0/1, 0 %, AT 15,0, VL/RL 17,0, WW-Status 3 | 0 → 4 WW, 42 % |
| 8 | 222 | 07.09. 18:15 | 07.09. 18:35 | 5 | 20–30 min | 17/8/84, Mod. 35 % **eingefroren**, AT 23,2 konstant – Standbild aus laufendem Kühlbetrieb | 2 Kühlen 35 % → 2 Kühlen (18:40, 42 % = Neuanlauf) |
| 9 | 124 | 12.09. 01:50 | 12.09. 01:55 | 2 | 5–15 min | 98/0/1, 0 %, AT 9,7, VL/RL 16,5, HK1-Status 6 | 51 Startvorb. → 0 (kein Start, HK1 Standby) |
| 10 | 0 | 20.10. 12:25 | 20.10. 17:10 | 58 | 285–295 min | Standbild: AT 11,3, VL 32,0, RL 33,5, `1539` 0, HK1-Soll fällt 35,9→35,0 (andere Einheit lebt) | 4 WW (12:10) → 0 (17:15, frische Werte AT 16,2) |

## Formel-Deutung je Wert
| Wert | Formel | Code | ERR.LOG (`errlog_idm_klartext.csv`, Spalte Modbus_1534) | Bedeutung im Archiv | Sicherheit |
|---|---|---|---|---|---|
| 124 | 124−63 = 61 | **W:61** | W:61 → 124, 13× nur unter V1.18, letzter Eintrag 24.08.2026 06:40:50 | Startphasen-Hinweis: 10/10 Proben mit `1539` = 98, kein Verdichter, danach Start oder Abbruch | Zuordnung 124 = W:61: **sicher** (Formel + ERR.LOG-Tabelle + 24.08. zeitgleich bei ~75 min HAICO-Uhrversatz). „Startphase/Status 98“ als Inhalt: **wahrscheinlich** (iDM-Klartext lautet „Wärmequellentemperatur nähert sich kritischem Wert“) |
| 190 | 190−127 = 63 | **B:63** | B:63 → 190 (iDM-Kennung 604), 36×, letzter 29.08.2026 20:06:53 | Blockierung rund um Reglereingriff/Neustart; Vorher Aus, nachher immer Neuanlauf (42 %) | Code: **sicher**; Ursache „Service-/Parametereingriff bzw. Neustart“: **wahrscheinlich** |
| 222 | 222−191 = 31 | **E:31** | E:31 → 222 (Kennung 36), 76×, 49 davon nach Neustart; letzter 29.08.2026 20:07:18 | Verriegelung direkt nach Reset/Neustart, ohne B-Vorlauf | Code: **sicher**; als echte E-Heizstab-Überhitzung (iDM-Text): **unwahrscheinlich** – Muster „E:31 nach Neustart“, Heizstab bisher nie im Einsatz |
| 0 | < 64, keine Klasse | – | nicht vorhanden | Kein Fehlercode, sondern Bridge-Initwert/Standbild (WEZ-Block nicht empfangen) | **sicher** für 03.–06.09. (alle Spalten 0, Lücke davor); **wahrscheinlich** für 20.10. (Werte 4,75 h eingefroren, Bridge läuft laut `ANALYSE_Block31903_eingefroren_20261024.md` seit 20.10. 17:10 neu – genau Ende der Episode) |
| 255 | 255−191 = 64 | (E:64) | – | Ruhewert „kein Fehler“ | **sicher** |

Zeitabgleich ERR.LOG ↔ Volllogger 29.08.: E:31 20:07:18 ↔ erste 222-Probe 20:10 (passt, **sicher**). B:63 steht im ERR.LOG erst 20:06:53, die 190-Proben liegen aber 19:25–19:35; um 19:25:35 steht im ERR.LOG ein **W:41** (104). Ob `1534` bei mehreren gleichzeitigen Alarmen den höchsten Rang zeigt oder die ERR.LOG-Zeiten verschoben sind, ist offen (**Vermutung**: Rangfolge B vor W). Vorhersagen aus OR-21.10. (74 = W:11, 128 = B:01, 192 = E:01) kamen im Archiv **nie** vor.

## Häufung / Muster
- **Echte Codes nur 15.08.–12.09.** (8 Episoden), danach im Volllogger keiner mehr bis 23.10. (das 50-s-E:31 vom 18.10. fällt durchs Raster). **Sicher.**
- **190/222 = Neustart-Signatur:** In allen vier Episoden steht `1540` = 8 und `1539` = 17 mit `1543` = 81/84 (Störzustand) oder `1539` = 0 mit `1543` = 20 (Blockierphase vor Wiederanlauf). Bei #1 und #8 friert der WEZ-Block während der Episode ein (AT, VL, RL, Modulation konstant) – typisch für Reglerneustart. Danach jeweils Neuanlauf mit Anlaufstütze 42 %. **Wahrscheinlich** Strom-Aus/Reset bzw. Service-Eingriff (15.08., 29.08. Fachmann-Durchgang laut `Recherche_Punkt6_Stoercode_1534_20260911.md`); 07.09. 18:15 Ursache nicht belegt. Nach Projektregel nicht überbewerten.
- **124 = nur in der Startphase nach Kühlbetrieb:** 4 Ereignisse 24.08.–12.09., immer `1539` = 98 und 0 % Modulation, 5–15 min; 3× folgt ein WW-Start, 1× (12.09.) kein Start. Seit 12.09. kein Kühlbetrieb mehr, kein 124 (deckt sich mit Loop-Antwort 21.10. 11:00). **Sicher** (Messung).
- **0-Episoden** sind Datenqualität, keine Anlagenstörung: zusammen 811 Proben (66,9 h). Für Störmelde-Logik muss 0 als „ungültig“, nicht als Fehler gelten.
- Keine einzige Episode mit Verdichter in Betrieb und gültigem Code außer #8 (Standbild aus laufendem Kühlbetrieb).

## Was bringt uns das
- Die Anlage hatte im ganzen Archiv **keine echte Kältekreis-Störung** (kein B:01 HD, kein B:02 ND, kein E-Code außer E:31-nach-Neustart). Die Takt-/Startprobleme sind keine Fehlerfolge.
- Für Loxone/HoxPi-Störmeldung: `1534` ∈ {255} = OK; ∈ {0} = Bridge ungültig (Datenalarm, nicht Anlagenalarm); 64–127 W = Hinweis (124 unterdrücken oder nur protokollieren); 128–190 B und ≥ 191 E = melden, aber innerhalb ~30 min nach Strom-Aus/Reset nur als „Neustart-Folge“ einstufen.
- Die Formel n+63/n+127/n+191 ist an drei realen Werten (124, 190, 222) gegen die ERR.LOG-Tabelle bestätigt; die Skepsis aus OR-21.10. („Indizes wirken zu groß“) betraf den Tabellenindex, nicht die Formel – n ist die Alarmnummer.
- 5-min-Raster ist für Kurzstörungen zu grob: ein Ereignis-Logger auf `1534`-Wechsel (Sekundenauflösung, nur lesen) würde Fälle wie 18.10. 11:10 erfassen – Vorschlag, nicht umgesetzt.

## Bewertung gegen „fertig, wenn“
„Alle Werte != 255 im ganzen Archiv mit Zeitpunkt, Dauer, Betriebszustand tabelliert und je Wert gedeutet“:
- Archiv vollständig durchsucht (86/86 Dateien, 30.07.–23.10.), alle 10 Episoden mit Zeit, Dauer, Zustand, Lücken: **erfüllt.**
- Je Wert gedeutet (124, 190, 222, 0): **erfüllt**, Codes sicher; Inhalt von W:61 als Startphase und Ursache von #8 (07.09. 18:15) nur wahrscheinlich bzw. offen.
- **Status-Vorschlag: erledigt.** Rest (optional, eigener Punkt): Rangfolge bei Mehrfachalarm (29.08. 19:25 W:41 im ERR.LOG vs. 190 im Modbus) und Auslöser 07.09. 18:15 – nur mit ERR.LOG-Kopie nach 29.08. klärbar (vor Ort/CF-Karte).