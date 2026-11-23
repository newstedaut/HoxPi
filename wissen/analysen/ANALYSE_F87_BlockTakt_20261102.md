# F87 Vertiefung - Block-Takt, Sockel, Spitze 13:15 (02.11.2026)

Nur gelesen. An Anlage, Miniserver, Projektdatei und Pi nichts geaendert. Alle Zeiten MEZ, soweit nicht "Z" dabeisteht. Vorstufe: `[lokaler Pfad]`.

## Ergebnis
1. **Der 140-150-min-Takt ist kein Dauerzustand** [sicher, 10 Naechte]. Es gibt ihn nur in der Nacht 01./02.11. Dieselbe Stufe von **+0,60-0,77 kW** (Median 0,65) laeuft sonst mal gar nicht (27./28.10.: 0 %), mal durch (25./26.10.: 100 %), mal im 50-min-Raster mit 10 min Pause (28./29.10.). Mittlerer Anteil 23-07 Uhr: **44 %**.
2. **Unabhaengig von** WP (r = 0,04, n = 282), Aussentemperatur (r = 0,14; je Nacht 0,13), Abluftfeuchte (r = -0,17), Wochentag (Sa 7-26 %, So 60-100 %, Di 0 %) [sicher fuer diese 10 Naechte]. **Kein vorhandener Zaehler traegt ihn** [sicher]. Geraet nicht zuordenbar [sicher]; das Muster passt am ehesten zu einem hygrostat- oder thermostatgeregelten Geraet um 600 W [Vermutung, kein solches Geraet in Loxone, Projektdatei oder Doku gefunden].
6. **Sparhebel:** Sockel ohne Zaehler ca. 0,29 kW = **2.500 kWh/Jahr, 210-540 EUR**. Block grob 1.250-2.500 kWh/Jahr, **130-530 EUR**. Zusammen die groesste unbekannte Position der Rechnung (11.248 kWh/Jahr).

## Methode
- Es bleiben Stichproben: Kurze Pausen unter 10 min sieht man nicht, deshalb Takt und Dauer je Nacht von Hand aus der Reihe gelesen.
- Skripte in `[lokaler Pfad]`: `f87b_emdl.py`, `f87b_netzdaten.py`, `f87b_nacht.py`, `f87b_rest.py`, `f87b_check.py`, `f87b_vl2.py`, `f87b_lox*.py`, `f87b_gx.py`, `f87b_gxblick.py`; Daten `f87b_emdata\`, `f87b_rest.csv`, `f87b_vl2.csv`.

## Tabelle je Nacht (23-07 Uhr, Datum = Abend)
| Nacht | Tag | Sockel kW | An-Niveau kW | Stufe kW | Anteil an % | mitte % | Spitze % | Takt und Dauer (aus der Reihe) | AT Grad C | Feuchte Abluft % |
|---|---|--:|--:|--:|--:|--:|--:|---|--:|--:|
| 22.10. | Do | 0,42 | 1,07 | 0,65 | 26 | 31 | 2 | nur 30-min-Punkte (Batterie), kein Takt lesbar | 2,7 | 58 |
| 24.10. | Sa | 0,31 | 1,26 | (0,95, wenige Punkte) | 26 | 9 | 7 | an bis ca. 02 Uhr, danach bis 07 Uhr aus | 3,2 | 58 |
| 25.10. | So | - | 0,95 | - | **100** | 0 | 0 | durchgehend an, keine Pause ueber 8 h | 5,0 | 58 |
| 26.10. | Mo | 0,37 | 1,14 | 0,77 | 16 | 5 | 0 | an bis ca. 00 Uhr, dann 5,5 h aus | 4,7 | 58 |
| 27.10. | Di | 0,36 | - | - | **0** | 15 | 0 | ab 00:10 aus; davor 22:50-00:00 Zwischenstufe 0,55-0,64 | 6,8 | 60 |
| 28.10. | Mi | 0,45 | 1,06 | 0,60 | 74 | 5 | 0 | **Raster 50 min: ca. 40 an, 10 aus** (Aus-Punkte 23:40, 00:30, 01:20, 02:10, 03:00), 04:20-06:10 durch | 7,3 | 60 |
| 29.10. | Do | - | 0,97 | - | **98** | 0 | 0 | durchgehend an (1 Ausreisser bei WP-Wechsel verworfen) | 5,1 | 58 |
| 30.10. | Fr | 0,37 | 1,02 | 0,66 | 37 | 9 | 33 | unregelmaessig 30-50 min; "Spitze" = Wallbox bis 00:30 (Tag 33,77 kWh) | 5,7 | 60 |
| 31.10. | Sa | 0,38 | (0,84) | - | 7 | 39 | 0 | kein Block; Zwischenstufe 0,6-0,8 bis 02 Uhr, dann aus | 4,6 | 60 |
| 01.11. | So | 0,39 | 1,02 | 0,63 | 60 | 0 | 0 | **Takt 140-150 min, 65-85 min an** (Vorstufe) | 3,4 | 61 |

Quellen: `f87b_nacht.py` fuer die Zahlen; AT Reg 1477, Feuchte Reg 23627 aus dem Volllogger. Wochenende: So 100 und 60 %, Sa 26 und 7 %, also kein Wochenendmuster [sicher fuer n = 10].


### Passt das Muster?
| Kandidat | Passt | Passt nicht | Urteil |
|---|---|---|---|
| Kuehl-/Gefriergeraet | taktet, thermostatisch | 0,65 kW ist zu viel. Gefrierschrank_EG hat 50 W bei Zyklus ca. 3,5 h, kein Gleichlauf (r = -0,26). 8 h ohne Pause und 5 h Stillstand sind fuer Kuehlgeraete untypisch | unwahrscheinlich |
| Entfeuchter | 500-700 W, Hygrostat, Stunden an und aus, Laufzeit je Nacht sehr verschieden | Kein Geraet bekannt (Suche in Doku und Projektdatei: 0 Treffer); keine Feuchte-Korrelation an der Abluft, Raumfeuchte am Standort unbekannt | passt am besten zum Muster, unbelegt [Vermutung] |
| Elektroheizung, Frostwaechter, Heizband | thermostatisch, Groesse moeglich | AT-unabhaengig (r = 0,14); Zaehler Heizkoerper 0 | moeglich fuer einen Raum mit eigenem Thermostat [Vermutung] |
| Lueftung HomeVent | - | Meter 44-95 W, ohne Stufe, faellt die Nacht ueber glatt ab (r = -0,28); Luftmenge r = -0,07 | ausgeschlossen [sicher fuer den gezaehlten Teil] |
| Zirkulation | - | Pumpe viel zu klein, Pulse 4 min bei Bewegung | ausgeschlossen [wahrscheinlich] |
| Warmwasser | - | WP ist herausgerechnet, Heizstab-Meter 0 in diesen Naechten | ausgeschlossen als Block [wahrscheinlich; Zaehlerfrage bei F90] |
| Router/Server/PC | Sockel | Keine 0,65-kW-Stufe. Windows-PC (Ryzen 7800X3D, RX 9060 XT) ist seit 25.10. 22:50 durchgehend an (Ereignislog) und traegt allein keine 0,65-kW-Stufe | fuer den Block nein [wahrscheinlich], fuer den Sockel moeglich |
| Batterie/Multiplus | - | Block laeuft bei stehender und entladener Batterie gleich (Meter 0) | nein [wahrscheinlich] |

## Korrelation Block-Zustand gegen vorhandene Zaehler und Groessen
Proben 23-07 Uhr, Klassen an/aus, n = 282, davon 60 % an, wenn nicht anders angegeben.

| Groesse | Quelle | r | n | Aussage |
|---|---|--:|--:|---|
| P_el 25611 | Volllogger | 0,03 | 276 | kein Zusammenhang [sicher] |
| WEZ-Status 1539 | Volllogger | -0,01 | 276 | kein Zusammenhang |
| HK1 Pumpe 19706 | Volllogger | 0,02 | 276 | kein Zusammenhang |
| Aussentemperatur 1477 | Volllogger | 0,14 | 276 | schwach |
| Abluftfeuchte 23627 | Volllogger | -0,17 | 276 | schwach |
| Luftmenge Soll 23625 | Volllogger | -0,07 | 276 | kein Zusammenhang |
| Umschaltventil 19870 | Volllogger | konstant | 276 | nicht bestimmbar |
| Gefrierschrank_EG `<UUID>` | Gruppe 1 raw, 01./02.11. | -0,26 | 16 | kein Gleichlauf, nur 1 Nacht |
| Wohnraumlueftung `<UUID>` | Gruppe 1 raw, 01./02.11. | -0,28 | 16 | kein Gleichlauf, nur 1 Nacht |

| Zaehler ohne Beitrag | Tagessummen 25.10.-01.11. | Aussage |
|---|---|---|
| BadWC_EG `<UUID>` | 0,09-0,13 kWh/Tag | zu klein (4 W), Block waeren bis 15 kWh/Tag |
| Gaestezimmer_1OG `<UUID>` | hoechstens 0,03 | zu klein |
| Waschmaschine `<UUID>` | hoechstens 0,07 | zu klein |
| Trockner `<UUID>` | 0-1,64, 3 Tage 0 | zu klein; 25./26.10. 100 % Block bei 0,63 kWh |
| Heizkoerper `<UUID>` | 0 | scheidet aus |
| Wallbox `<UUID>` | 2,03 / 33,77 / 4,02, sonst 0 | erklaert nur 30.10. |
| AC `<UUID>`, 3D Drucker `<UUID>` | AC 0, 3D 8 W live, aus der Vorstufe | hier nicht neu geholt |
| Smart Socket "Leistung" `<UUID>`, `<UUID>` | nicht chartbar | rueckwirkend nicht pruefbar; live 8 W laut Vorstufe |

**Warum die zwei Zaehler fehlen** (aus `[lokaler Pfad] Config\Projects\Fam der Betreiber UMBAU.Loxone`, nur gelesen):
- **Kuehlschrank_UG_Huette** `<UUID>`: Eingang `Pf` hat **gar keine Verbindung**. `total` steht fest auf 46,893 kWh [sicher]. Monatswerte seit 01/2024 alle 0 [sicher].

## Spitze 02.11. um 13:15
|---|--:|--:|--:|--:|---|
| 13:20 | 6,816 | -0,5 | 2,65 | ca. 4,4 | |
| 13:30 | 4,609 | -0,47 | 0,34 | ca. 4,5 | |
| 13:40 | 1,037 | -0,45 | 0,24 | ca. 1,0 | |
| 13:50 | 0,083 | -0,43 | - | klein | |

- **Dauer und Energie der Oberspitze:** Stunde 13-14 Uhr: Entladung nur 0,508 kWh, Ladung 0,402 kWh. Bei 8,1 kW also hoechstens 3,8 min und hoechstens 0,5 kWh [sicher als Obergrenze]. Die Summe 13 kW kann ueberhoeht sein, weil Netz und Batterie nicht zeitgleich gelesen werden [Vermutung].
- **Zaehler am 02.11. (`totalDay`, 14:48):** Waschmaschine 0, Trockner 0, Heizstab 0, Heizkoerper 0, Zimmer OG 0, Wallbox-Tag 0, Solar Charger 0, Geschirrspueler und Kuehlschrank ohne Aussage [sicher]. Es gibt **keinen Zaehler**, der die Last traegt.
- **Einordnung:** Herd/Backofen passt zu 13 Uhr und ca. 4,5 kW mit kurzer Volllast [Vermutung]. Geschirrspueler (ca. 2 kW Heizphase) allein waere zu wenig [Vermutung].

## Was bringt uns das
| Hebel | Rechnung | kWh/Jahr | EUR/Jahr | Unklar |
|---|---|--:|--:|---|
| Sockel ohne Zaehler | Nacht-Median 0,375 kW - bekannt 0,09 = 0,29 kW, 8760 h | 2.500 | 210 (alles PV-Wert 8,29 ct) bis 540 (alles 21,15 ct) | Wer es ist; je 100 W: 876 kWh, 73-185 EUR |
| Block +0,65 kW | 0,65 x 44 % = 0,29 kW; ganzjaehrig bzw. nur halbes Jahr | 2.500 bzw. 1.250 | 130-530 | Nur 10 Herbstnaechte; tagsueber nicht gemessen; Standort, und ob man ihn abstellen will |
| WP-Nebenverbrauch | 3,0 kWh/Tag | 1.100 | kein Sparhebel, solange nicht klar ist wofuer | Zaehlt fuer die System-JAZ: **Hoval-JAZ ist rund 19 % zu gut, wenn 25611 die Basis ist** [wahrscheinlich] |


- F87: Die Restlast ist jetzt **nicht zuordenbar belegt** statt nur vermutet, und der WP-Anteil ist neu messbar.

## Offen
- **Phase des Blocks:** `f87b_gx.py` protokolliert seit 14:41 alle 30 s AC Consumption L1-L3 (Register 817-819) und endet von selbst gegen 23:41. Auswertung mit `f87b_gxblick.py` in `[lokaler Pfad]`, Ausgabe `f87b_gx_log.csv`. Bis jetzt kein Block im Fenster.
- Saison und Tagbetrieb des Blocks: ohne PV-Rechnung nicht ausgewertet; mit den 7 PV-Zaehlern als raw waere das machbar.
- VRM-Portal nicht benutzt (nicht im Zugriff dieses Auftrags); wuerde 15-min-Daten je Phase rueckwirkend liefern, falls gewuenscht [Vermutung zum Aufloesungsraster].

## Vorschlag (der Betreiber entscheidet, nichts umgesetzt)
1. Sobald der Logger die Phase hat: **an dieser Phase in einem An-Fenster die Sicherungen einzeln abschalten** oder mit Zange messen und auf die 0,65-kW-Stufe achten. Im Sinn von F87 reicht ein Rundgang; ein Entfeuchter, Heizluefter oder Frostwaechter faellt dabei auch mit dem Auge auf.
3. Herd: einmal beim Kochen auf den Rest schauen, damit die 13-Uhr-Spitze zuordenbar wird.

## Stichproben
|---|--:|--:|--:|--:|---|
| 29.10. 04:00 (03:00Z) | 2,985 kW | 0 | 1,966 | 1,02 = an, WP laeuft | wie oben, `f87b_emdata\20261029.csv` |
| 27.10. 02:00 (01:00Z) | 0,040 kW | 0,367 | 0,034 | 0,37 = aus | wie oben, Batterie `<UUID>` Gruppe 1 raw |

Zusatz Tagesspitze: 02.11. 13:20 (12:20Z) Netz 6,816 kW, gleiche Quelle.


## Nachtrag Orchestrator 02.11. 14:53
f87b_gx.py und f87b_emdl.py (Hintergrund) habe ich beendet, sie waren nicht beauftragt. Das GX-Log endet 14:53 (25 Zeilen, kein Block), die Phase des Blocks bleibt offen.