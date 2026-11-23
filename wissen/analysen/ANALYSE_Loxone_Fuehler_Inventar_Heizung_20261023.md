# Loxone-Fühlerinventar für die Heizungsanalyse – Stand 23.10.2026, ca. 16:00 (MESZ)

Nur gelesen: Loxone-MCP (control_find/state/describe), Projektdatei `[lokaler Pfad] Config\Projects\Fam der Betreiber UMBAU.Loxone` (Stand 18.10.2026 18:07, per Regex durchsucht, nicht verändert) und HoxPi `read_register`/`get_status`. Nichts geschrieben.

Zum Zeitpunkt der Messung: WP aus, HK1/HK2 „Abgeschaltet“, außen 10,4 °C. Die Werte sind deshalb Stillstandswerte, keine Betriebswerte.

**Zu „lebt“:** Die Loxone-MCP-History reicht nur bis zum MCP-Start (13:57 UTC). Ich habe zwei Abfragen im Abstand von 2,5 min verglichen. „ja“ = Wert hat sich in dieser Zeit bewegt bzw. ist plausibel und folgt der Hoval. „unklar“ = konstant, kann im Stillstand trotzdem stimmen.

## 1. Fühler, die es gibt (sicher – in der App sichtbar oder in der Projektdatei belegt)

| Fühler | Raum | UUID / Name | Wert (13:57 → 13:59:30 UTC) | lebt | nutzbar für |
|---|---|---|---|---|---|
| Thermometer_HK1_UG_Vorlauf (1-Wire, ROM 28…, Loxone-eigen) | Technikraum | <UUID> | 19,25 → 19,19 °C | ja | (d)-Gegenstück HK1, Plausibilisierung Hoval VF1 |
| HK1 Vorlauf ist (Hoval VF1 über HoxPi) | Technikraum | <UUID> | 19,0 → 18,8 °C | ja | HK1 Vorlauf |
| HK2 Vorlauf ist (Hoval VF2, Reg. 1514) | Technikraum | <UUID> | 18,3 °C (HoxPi 1514 = 18,3) | ja (stimmt mit HoxPi) | **(d)** |
| Thermometer_HK2_OG_Vorlauf (1-Wire, ROM 28CE2F540D0000C3) | nur in Projektdatei, keine App-Kachel | Device <UUID>, Sensor <UUID> | nicht abrufbar (nicht visualisiert) | unklar | **(d)** zweite Quelle. Achtung: Sensor hat `MaxVal="10"` in der Datei – prüfen, ob das den Wert abschneidet |
| Thermometer_Boiler_Oben (1-Wire, ROM 2822CD770C00009D) | Technikraum | <UUID> | 50,94 °C | ja (passt zu SF1 51,3) | WW oben, Gegenprüfung SF1 |
| Warmwasserspeicher oben (Hoval SF1) | Technikraum | <UUID> | 51,4 → 51,3 °C | ja | WW |
| Warmwasserspeicher unten (Hoval SF2) | Technikraum | <UUID> | 49,3 °C | unklar (konstant) | WW-Schichtung |
| WP Rücklauf (Hoval Reg. 1535 „Rücklauftemperatur“) | Technikraum | <UUID> | 35,0 °C konstant | unklar – WP steht, Wert ist eingefroren/Stillstand | **nur WP-Rücklauf (gemeinsam), NICHT HK1/HK2** |
| WP Vorlauf ist | Technikraum | <UUID> | 41,0 → 40,5 °C | ja | WP-Spreizung |
| Aktuelle Puffertemperatur Oben [PF1] (Reg. 17386) | Technikraum | <UUID> | **0,0 °C** (HoxPi 17386 = 0) | **nein** | (b) – liefert nichts |
| Aktuelle Pufferisstemperatur Unten [PF2] (Reg. 17387) | nur Datei (InputRef + StateV, keine App-Kachel gefunden) | Sensor <UUID> | HoxPi 17387 = 0 | **nein** | (b) – liefert nichts |
| Aktuelle HZ Puffer WPF Fühler [WPF] (Reg. 27494) | nur Datei, kein Verweis | <UUID> | HoxPi 27494 = 0 | **nein** | (b) – liefert nichts |
| Raumregler tempActual (IRoomControllerV2) | Wohnzimmer | <UUID> | 22,3 °C | ja | Raum UG / (e) |
| Touch-Tree „Ofen“ (Installation „Ofen WZ“, Serial <Seriennr>), Temperatur + Luftfeuchte | Wohnzimmer | Temp <UUID>, Feuchte <UUID> | Feuchte 47,1 % (Temp nur über Verweis „Temperatur Ofen“ <UUID>, keine Kachel) | ja | **(e)** – wird schon von der Ofen-Nachlauf-Logik genutzt |
| zweiter Touch-Tree Wohnzimmer | Wohnzimmer | Temp <UUID>, Feuchte <UUID> | Feuchte 50,4 % | ja | (e)/(f) Referenz abseits vom Ofen |

### Raumtemperatur und Feuchte (f)


| Raum | Regler-UUID | Temp | Feuchte (UUID) | Taupunkt berechnet | lebt |
|---|---|---|---|---|---|
| Wohnzimmer | <UUID> | 22,3 °C | 50,4 % (<UUID>) / 47,1 % Ofen-Tree | 11,5 / 10,5 °C | ja |
| Badezimmer | <UUID> | 22,2 °C | 58,7 % (<UUID>) | 13,7 °C | ja |
| Büro | <UUID> | 21,5 °C | 50,2 % (<UUID>) | 10,7 °C | ja |
| Zimmer OG 1 | <UUID> | 21,6 °C | 53,7 % (<UUID>) | 11,8 °C | ja |
| Zimmer OG 2 | <UUID> | 20,8 °C | 56,3 % (<UUID>) | 11,8 °C | ja |
| WC UG | <UUID> | 21,5 °C | 53,1 % (<UUID>) | 11,5 °C | ja |
| Hütte | <UUID> | 18,1 °C | 49,5 % (<UUID>) | 7,4 °C | ja |
| Technikraum | <UUID> | 19,6 °C | – | – | ja |
| Garage | <UUID> | 16,1 °C | – (nur Taupunkt-Baustein in Datei) | – | ja |

Welcher Raum in welchem Stockwerk liegt, geht aus den Loxone-Daten nicht hervor – OG-Wohnraum/Küche habe ich **nicht** als eigenen Raum gefunden.

## 2. Wahrscheinlich (nicht voll belegt)

- **WP Rücklauf 35,0 °C** ist der gemeinsame Rücklauf am Wärmeerzeuger (Reg. 1535), kein Heizkreis-Rücklauf. Im Stillstand steht er auf 35,0 – wahrscheinlich letzter Wert/Stillstandswert, Aussage nur bei laufendem Verdichter.
- **Pufferfühler PF1/PF2/WPF = 0** in der Hoval: wahrscheinlich ist am Heizungspuffer (EnerVal 300) kein Hoval-Pufferfühler angeschlossen bzw. nicht konfiguriert. Das ist kein Loxone-Fehler – die Register liefern schlicht nichts.
- **Thermometer_HK2_OG_Vorlauf** ist als 1-Wire-Gerät eingelernt (Device + Sensor + Verweis, Verweis an Px 1824/Py 20064). Ob er physisch am HK2-Vorlauf sitzt und Werte liefert, konnte ich ohne Kachel nicht prüfen. Die Grenze `MaxVal="10"` am Sensor ist auffällig – nur Vermutung, dass es eine Fehlkonfiguration ist.
- 1-Wire-Extension hat laut Datei genau **3 Fühler**: HK1 UG Vorlauf, HK2 OG Vorlauf, Boiler oben.

## 3. Ergebnis je Punkt

| Punkt | Vorhanden? | Quelle |
|---|---|---|
| (a) Rücklauf HK1 / HK2 | **fehlt** | nur gemeinsamer WP-Rücklauf 1535 |
| (b) Puffer oben/unten / Abgang | **fehlt praktisch** – Datenpunkte existieren, liefern 0 | 17386/17387/27494 |
| (c) Zirkulations-Rücklauf | **fehlt** | nur Zirkulationspumpe (Aktor) + Zeitprogramme |
| (d) Vorlauf HK2 | **vorhanden** – Hoval VF2 (lebt), zusätzlich 1-Wire HK2 OG (Status unklar) | 1514, <UUID> |
| (e) Holzofen / Wohnzimmer UG | **vorhanden** – Touch-Tree „Ofen WZ“ + zweiter Tree + Raumregler | <UUID> |
| (f) Taupunkt/Feuchte je Raum | **vorhanden** für 7 Räume + Taupunkt-Bausteine in der Datei (ohne Kachel) | siehe Tabelle |

## 4. Was fehlt – Hardware-Vorschlag (nur Vorschlag, nichts bestellt/verbaut)

Die 1-Wire-Extension ist schon da und hat erst 3 Fühler. Am günstigsten ist daher: **weitere DS18B20-Anlegefühler (Edelstahlhülse, Kabel) an denselben 1-Wire-Bus**, mit Wärmeleitpaste, Kabelbinder/Spannband und über die Rohrisolierung isoliert.

| Fehlt | Vorschlag | Einbauort |
|---|---|---|
| (a) Rücklauf HK1 UG | 1-Wire-Anlegefühler | Rücklaufrohr HK1 nach dem Verteiler, vor dem Puffer/Mischer |
| (a) Rücklauf HK2 OG | 1-Wire-Anlegefühler | Rücklaufrohr HK2 |
| (b) Puffer oben / unten | 2× 1-Wire-Tauchfühler in freie Tauchhülsen am EnerVal 300 (falls frei), sonst Anlegefühler am Pufferabgang zu den HK und am Puffer-Rücklauf zur WP | Puffer oben = Abgang HK, unten = Rücklauf WP |
| (c) Zirkulations-Rücklauf | 1-Wire-Anlegefühler | Zirkulationsleitung kurz vor dem Wiedereintritt in den Speicher (nach Rückschlagventil) |
| (d) Vorlauf HK2 – zweite Quelle | vorhandenen Thermometer_HK2_OG_Vorlauf prüfen (Kachel anlegen, `MaxVal` kontrollieren) | – |
| (f) Taupunkt-Kacheln | keine Hardware nötig: vorhandene `DewPoint`-Ausgänge visualisieren | – |

Hinweis: Anlegefühler messen 0,5–2 K unter der Mediumtemperatur – für Spreizungen und Trends reicht das, für absolute Werte HK1-1-Wire gegen Hoval VF1 kalibrieren (heute 19,19 vs 18,8 °C).

Loxone-Doku (Links nicht einzeln aufgerufen, bitte bei 404 über die KB-Suche gehen):
- 1-Wire Extension: https://www.loxone.com/dede/kb/1-wire-extension/
- Taupunkt-Baustein: https://www.loxone.com/dede/kb/taupunkt/
- Intelligente Raumregelung: https://www.loxone.com/dede/kb/intelligente-raumregelung/
- Klima-Controller: https://www.loxone.com/dede/kb/klima-controller/
- Modbus-Server/TCP: https://www.loxone.com/dede/kb/modbus-server/
- Touch Tree: https://www.loxone.com/dede/kb/touch-tree/

## 5. Was bringt uns das

- **HK-Rückläufe (a):** Spreizung je Heizkreis → sieht man, ob ein Kreis überströmt ist (kleine Spreizung = Pumpe zu stark / Stellantriebe zu) oder unterversorgt. Direkt nutzbar für Pumpenstufe Grundfos und für die Holzofen-Frage (Rücklauf UG steigt, wenn die Stellantriebe zu sind).
- **Puffer (b):** Heute ist der Puffer für Loxone und Hoval blind. Mit oben/unten sieht man Schichtung, Ladezustand und ob die WP taktet, weil der Puffer zu schnell „voll“ ist – passt zu den 20 713 Schaltzyklen bei 14 888 h.
- **Zirkulations-Rücklauf (c):** Beweis, ob der Rücklauf bei WW-Soll 50–52 °C über **50 °C** bleibt (Legionellen-Kriterium) und ob die Zirkulationszeiten reichen. Ohne Fühler ist das nur geraten.
- **HK2-Vorlauf (d):** Haben wir über Hoval schon; der 1-Wire-Fühler wäre eine unabhängige Gegenprobe zu VF2.
- **Ofen (e):** Ist vorhanden und schon in der Ofen-Nachlauf-Logik verbaut – hier fehlt nichts.
- **Taupunkt (f):** Fürs Kühlen reicht, was da ist. Bad liegt aktuell mit 13,7 °C am höchsten – Vorlauf-Min Kühlen muss darüber liegen (+ Reserve). Sinnvoll: die vorhandenen `DewPoint`/`Minmax`-Ausgänge als Kachel sichtbar machen.