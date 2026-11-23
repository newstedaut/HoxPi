# ANALYSE 29.10.2026 - F48: "WW-Soll 10 °C" am 26./27.10. = Abtauung, kein Loxone-Fehler

Orchestrator 29.10.2026 15:57 MEZ, MEHR Stufe 2. Alles nur gelesen (Prometheus localhost:9090 per GET, Volllogger, HoxPi `read_register`, Bridge-Journal, Exporter-Quelltext). Nichts geschrieben.
Herkunft: `[lokaler Pfad]` Z. 144 (Chat 27.10. 21:45: "1497 stand ~8 min auf 10 °C, Ursache offen: Miniserver-Neustart, Loxone-Logik oder Modbus-Fehllesung").
Skripte: `[lokaler Pfad]` (am Pi nur unter /tmp, lesend).

## Befund

| Prüfung | Ergebnis | Sicherheit |
|---|---|---|
| Exporter `/home/<user>/hoval-exporter/hoval_exporter.py` Z. 11 | `hoval_ww_soll_c` = **Reg 1499**, nicht 1497 | sicher |
| Reg 1499 (HoxPi `read_register`, offizielle Liste) | "Warmwasser-Soll / Solltemperatur", **berechneter** Sollwert, nur lesbar; live 15:5x = 50,0 | sicher |
| Volllogger 27.10. 06:40/06:45/06:50 | 1497 = 500/500/500 (Loxone-Vorgabe unverändert), 1539 = 1 → **8** → 16 | sicher |
| Prometheus 1499 < 40 °C seit 01.10. | genau 4 Phasen: 13.10. 06:10-06:15, 13.10. 07:38-07:44, 26.10. 05:04-05:10, 27.10. 06:40-06:49 MEZ | sicher |
| Phasen `hoval_wez_status` = 8 seit 01.10. | genau dieselben 4 Phasen → **4/4 deckungsgleich** | sicher |
| Bedeutung Status 8 (offizielle Hoval-Datenpunktliste, Reg 18723 = gleiche Codes wie 1539) | **8 = Abtauen** | sicher |
| Ablauf 26.10. (15-s-Raster) | 05:03:45 Lauf → 05:04:15 Mod 0, 1499 50→10 → 05:04:45 Status 51, Pumpe 100 %, ND 6,9→10,7 bar, VL 35→28 → 05:05:15 Status 8 | sicher |
| Ende 27.10. | 05:49:15 UTC Status 8→16 (Wiedereinschaltsperre), 30 s später 1499 10→50 | sicher |

## Folgerung
- Die Hoval setzt den **berechneten** WW-Soll 1499 während jeder Abtauung auf 10 °C (Frostschutzwert) und danach wieder auf die Loxone-Vorgabe (sicher als Messbefund; *warum* intern = Vermutung: WW-Anforderung wird für die Abtauung gesperrt).
- **Kein** Miniserver-Neustart, **keine** Loxone-Logik, **keine** Modbus-Fehllesung: Loxone hat 1497 durchgehend auf 50,0 geschrieben (Volllogger sicher; Bridge-Journal reicht nur bis 28.10. 19:14 zurück, für 27.10. nicht prüfbar).
- Die Notiz "1497 = 10 °C" in 02_Status_Offen war eine Verwechslung: Prometheus `hoval_ww_soll_c` ist 1499.
- Nebenbefund: Die Legende im Exporter (`hoval_exporter.py` Z. 112) kennt Status 8 nicht - laut offizieller Liste 8 = Abtauen (nur Doku, Exporter nicht geändert).

## Was bringt uns das
- Offener Punkt 27.10. ohne Eingriff geschlossen; nichts an Loxone zu ändern.
- **Zweiter Abtau-Marker** für F11 (Winter-Messreihe) und den Zwilling: `1539 = 8` oder `1499 = 10` (Prometheus 15 s) markiert jede Abtauung sicher - unabhängig vom ND-Verlauf.
- Für Auswertungen: `hoval_ww_soll_c` niemals als Loxone-Vorgabe lesen; die Vorgabe ist 1497 (Volllogger).