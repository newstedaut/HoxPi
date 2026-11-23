# Zirkulationspumpe: alle Auslöser in Loxone + Entwurf Sperrlogik – 22.10.2026 (Claude Code, nur lesend)

Quellen (nur gelesen, nichts geändert):
- Projektdatei `[lokaler Pfad] Config\Projects\Fam der Betreiber UMBAU.Loxone` (Stand 18.10.2026 18:07, 16 950 Zeilen). Zeilenangaben = Zeile in dieser Datei.
- Leseskripte: `Emulation\cc_zirk_ausloeser_20261022.py/.out` (Rückwärtsverfolgung ab Relais Q3), `cc_zirk_ausloeser2_…`, `cc_zirk_ausloeser3_…`.
- Loxone-MCP lesend: `control_statistics` Zirkulationspumpe 22.10. (31 Pulse), `control_history` Lichtsteuerung WC UG und Badezimmer (je letzte 20 Einträge, nur 22.10.).
- Vorgänger: `ANALYSE_Zirkulation_Loxone_20261022.md`.

## Kurzfassung
- Es gibt **genau eine Logikkette**: 6 Eingänge → Statusbaustein „Zirk: Anforderung“ → Monoflop „Zirk: Lauf 4 min“ (240 s) → Ausgangsverweis → Relais Q3 „Zirkulationspumpe“. Keine weiteren versteckten Auslöser.
- Der Kreis „Zirkulation“ im Lichtbaustein WC UG ist **nicht verdrahtet** (AQ2 leer) – wirkt nicht, Altlast.
- Eine Sperre 20 min nach Pulsende hätte am 22.10. 31 → 17 Pulse und 134 → 68 min Laufzeit gebracht. Wärmeersparnis klein: grob 0,4–0,8 kWh Wärme/Tag (Annahmen unten).

## 1. Logikkette (belegt, XML)
```
Präsenzmelder Tree WC UG  "Bewegung" (Q) ─► InputRef "Bewegung" (Z.16198) ─► I5 ┐
Präsenzmelder Tree Bad    "Bewegung" (Q) ─► InputRef "Bewegung" (Z.16208) ─► I6 │
StairwayLS "Zirkulation Hand (5 min…)" (Z.16661) ─────────────────────────► I4 ├► State "Zirk: Anforderung" (Z.16675)
(I2 frei – Sperre am 03.10.2026 entfernt, I8 frei)                             ┘          ▼
                         Monoflop "Zirk: Lauf 4 min" (Z.16711, Time 240 s, Reset/Remanenz frei)
                                   Q ─► OutputRef "Zirkulationspumpe" (Z.16923) ─► Relais Q3 (Z.6234, U=<UUID>-…)
                                   Q ─► State "Warmwasser Status" I2 (nur Anzeige)
```
Statusbaustein-Zeilen (Z.16703 ff., „erste zutreffende Zeile gewinnt“, Wert 1 = Anforderung):
| Rang | Bedingung | Wert | Text |
|---|---|---|---|
| 1 | I4 Hand = 1 | 1 | Hand-Taster |
| 3 | I3 Freigabe = 0 | 0 | Nachtruhe 23:30-05:00 |
| 4 | I5 Bewegung WC UG = 1 | 1 | Bewegung WC UG |
| 5 | I6 Bewegung Bad = 1 | 1 | Bewegung Badezimmer |
| 7 | sonst | 0 | keine Anforderung |

## 2. Auslöserliste
| # | Auslöser | Quelle / Raum | Eingang | Pulsdauer | Belegstelle |
|---|---|---|---|---|---|
| A | Bewegung WC UG | Präsenzmelder Tree, Raum „WC UG“, Ausgang **Bewegung** (Rohsignal, nicht „Präsenz“), MinTime 10 | I5 | 240 s je Flanke 0→1 | TreeSensor U=<UUID>-… Z.4879; InputRef Z.16198 |
| B | Bewegung Badezimmer | Präsenzmelder Tree, Raum „Badezimmer“ (Decke), Ausgang **Bewegung**, MinTime 10 | I6 | 240 s je Flanke | TreeSensor U=<UUID>-… Z.5041; InputRef Z.16208 |
| D | Hand (App) | Treppenlichtschalter TH = 300 s | I4 (Rang 1, übersteuert alles) | **240 s**, nicht 300 s – läuft durch den 4-min-Monoflop | U=<UUID>-… Z.16661 |
| – | Freigabe | DayTimer 05:00–23:30 (From=300 To=1410), nur sperrend | I3 | – | Z.16571/16584 |
| ✗ | Lichtbaustein WC UG, Kreis „Zirkulation“ (AI2) | NameAI1="Zirkulation", Ausgang AQ2 **ohne Verbindung** | – | wirkt nicht | LightController2 U=<UUID>-… Z.11840 |

Sonst kein Baustein in der Datei mit „Zirk“ im Namen, kein Merker/Formel/Virtueller Eingang auf der Kette (Rückwärtsverfolgung vollständig, `cc_zirk_ausloeser_20261022.out`).

Auffälligkeiten (belegt):
- NDOC des Hand-Schalters sagt noch „übersteuert Sperre / setzt selbst die Sperre“ – die Sperre gibt es seit 03.10. nicht mehr (Text veraltet).
- Hand liefert 4 min statt der angezeigten 5 min (Monoflop dahinter).
- Monoflop-NDOC sagt „nicht retriggerbar“; die Statistik zeigt aber Läufe von 6:57–7:35 min (07:53:53–08:01:28, 08:15:53–08:23:00, 17:39:35–17:46:32 UTC) → **wahrscheinlich doch retriggert** (neue Flanke während des Laufs verlängert).

## 3. Abgleich Pulse ↔ Auslöser, 22.10.2026 (Ortszeit MESZ)

| Auslöser | Pulse | Zeiten (Pulsbeginn) | Sicherheit |
|---|---|---|---|
| Hand | 0 erkennbar | – | nicht ermittelbar (Hand-Historie erst ab MCP-Start 20:59) |
| **Summe** | **31** | 133,7 min Laufzeit | |


## 4. Entwürfe (nur Vorschlag – nichts eingebaut)
Doku-Links (offizielle Loxone-KB; URLs nach Schema, heute nicht einzeln aufgerufen):
Monoflop https://www.loxone.com/dede/kb/monoflop/ · Statusbaustein https://www.loxone.com/dede/kb/status/ · Treppenlichtschalter https://www.loxone.com/dede/kb/treppenlichtschalter/ · Schaltuhr https://www.loxone.com/dede/kb/schaltuhr/ · Ausschaltverzögerung https://www.loxone.com/dede/kb/ausschaltverzoegerung/ · Lichtsteuerung https://www.loxone.com/dede/kb/lichtsteuerung/ · Präsenzmelder Tree https://www.loxone.com/dede/kb/praesenzmelder-tree/ · Schwellwertschalter https://www.loxone.com/dede/kb/schwellwertschalter/

### V1 – Sperre „nach Puls 20 min kein neuer Puls“ (empfohlen, minimal)
- Neuer Monoflop „Zirk: Sperre“, Time = **1440 s** (4 min Lauf + 20 min Sperre), Trigger = Q von „Zirk: Lauf 4 min“ (steigende Flanke, also 1× je Lauf).
- Q „Zirk: Sperre“ → **I2** von „Zirk: Anforderung“ (ist frei, war früher die Sperre). Neue Statuszeile **direkt nach Rang 2/3**, vor den Bewegungszeilen: „I2 = 1 → 0, Text ‚Sperre 20 min‘“. Hand bleibt Rang 1 und übersteuert.
- Zusätzlich Q „Zirk: Sperre“ → „Warmwasser Status“ I4 (Eingang „Sperre“ existiert schon laut NDOC) für die App-Anzeige.
- Verhalten: Während Lauf+Sperre ist AQ = 0 → keine Flanke, kein Nachtrigger. Ist nach Sperrende noch Bewegung da, entsteht sofort eine neue Flanke → ein Puls (gewollt: Person ist noch im Bad).
- Hinweis: Nachtrigger während des Laufs entfallen damit auch (Lauf bleibt sauber 4 min).
- Simulation 22.10. (Sperre ab Pulsende): 10 min → 22 Pulse/88 min · 15 min → 19/76 · **20 min → 17/68** · 30 min → 15/60 (Ist: 31/134).

### V2 – „Präsenz“ statt „Bewegung“ als Auslöser
- I5/I6 statt vom Rohsignal „Bewegung“ vom Präsenz-Ausgang (Präsenzmelder mit Nachlauf bzw. Präsenz der Lichtsteuerung) speisen → 1 Puls je Aufenthalt.
- 22.10. geschätzt: die 12 Bad-Nachtrigger fallen weg → ~19 Pulse. Nachteil: Präsenz kommt evtl. Sekunden später; langer Aufenthalt (86 min Bad) bekommt nur 1 Puls – meist reicht das, Leitung bleibt bei Zapfung ohnehin warm.
- Kombinierbar mit V1 (Sperre 15 min) → geschätzt ~15–17 Pulse.

### V3 – nur ein Auslöser (z. B. nur Bad)
- Spart die ~6 WC-Pulse/Tag, aber im WC UG gibt es dann beim Händewaschen länger kaltes Wasser. **Nicht empfohlen** – das Problem ist der Bad-Melder, nicht das WC.

### V4 – temperaturgeführt über Zirkulations-Rücklauffühler
- Voraussetzung: Fühler am Zirk-Rücklauf. **Nicht vorhanden** in Loxone (kein Baustein dazu in der Datei) und nicht an Hoval (Reg. 19755 leer). Bräuchte z. B. Tree/1-Wire-Anlegefühler.
- Logik: Anforderung (Bewegung/Präsenz) UND T_Rück < 40 °C → Lauf; Abbruch wenn T_Rück > 45 °C oder nach max. 4 min (Schwellwertschalter + UND + Monoflop als Zeitbegrenzung).
- Vorteil: läuft nur, wenn die Leitung wirklich kalt ist, unabhängig von Uhrzeit; kürzere Läufe (oft 1–2 min statt 4). Höchste Einsparung, aber Hardware + Montage.

### Einsparung – Annahmen offen
- Annahme Leitung: ~20 m Zirk-Kreis Cu 15×1 gedämmt (Länge **unbekannt**). Wärmekapazität Wasser+Kupfer ≈ 0,7 kJ/(K·m) → Aufheizen kalt (≈25 → 55 °C) ≈ 0,12 kWh; Verlust warm ≈ 8–10 W/m → ~0,2 kW.
- Ein Puls < 20 min nach dem vorigen findet die Leitung noch warm (Abkühlung grob 5–15 K) → er kostet nur ~0,03–0,06 kWh (Nachheizen + 4 min Verlust).
- V1: 14 Pulse/Tag weniger × 0,03–0,06 kWh ≈ **0,4–0,8 kWh Wärme/Tag** ≈ 0,15–0,3 kWh Strom (WW-AZ ~3) ≈ 50–100 kWh Strom/Jahr. Pumpenstrom selbst (5–8 W, ~1 h/Tag weniger) ≈ 2–3 kWh/Jahr – vernachlässigbar.
- Passt zur Obergrenze aus der Vorgänger-Analyse (0,5–1 kWh/Tag); die dort genannten 2–5 kWh/Tag für *alle* Pulse sind mit Zapfung vermischt.
- Nebeneffekt: weniger Durchmischung oben im Speicher, weniger Pumpenstarts (~45 % weniger).

**Was bringt uns das:** V1 ist ein Zehn-Minuten-Umbau ohne Komfortverlust und halbiert die Pumpenstarts; Geld bringt es wenig (~10–20 €/Jahr). V2 ist die sauberere Ursachenbehebung (Bad-Melder-Lücken). V4 nur, wenn ohnehin ein Fühler montiert wird. Der große WW-Hebel bleibt Sollwert/Zapfmenge.

## 5. Einordnung
**Belegt (XML / Loxone-Daten)**
- Vollständige Kette und Eingänge I1–I7 wie in Abschnitt 1/2; I2 und I8 frei; Monoflop 240 s; Hand TH 300 s; Morgen 05:20–05:23; Freigabe 05:00–23:30.
- Melder: I5 = TreeSensor „Bewegung“ Raum WC UG, I6 = TreeSensor „Bewegung“ Raum Badezimmer (IoData Pr).
- Lichtbaustein-Kreis „Zirkulation“ WC UG unverdrahtet.
- 22.10.: 31 Pulse; 14 Pulsbeginne sekundengenau = Präsenzbeginn Bad (9) bzw. WC UG (5); 1 = Morgen-Vorlauf.

**Wahrscheinlich**
- Monoflop retriggert entgegen NDOC (Läufe bis 7:35 min).
- Miniserver läuft mit dem Stand dieser Datei (Namen/UUIDs stimmen mit MCP überein; Ladezeit nicht geprüft).

**Vermutung**
- Einsparung 0,4–0,8 kWh Wärme/Tag (Leitungslänge/Dämmung unbekannt).

**Nicht ermittelbar (mit den lesenden Mitteln)**
- Hand-Betätigungen (keine Historie vor 20:59).
- Rohsignal „Bewegung“ zeitlich (nicht historisiert); Activity-Log nur 20 Einträge → Tage vor dem 22.10. nicht zuordenbar.
- Leitungslänge, Pumpentyp, Zirk-Rücklauftemperatur.

Nächster Schritt (falls gewünscht): V1 per Skript nach Skill `loxone-xml-umbau` als TEST-Datei bauen, der Betreiber prüft in Loxone Config und lädt selbst.