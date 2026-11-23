# Bedienmodul Wohnzimmer: „UNKNOWN BUILD" und Startbild (14.11.2026, Claude Code)

## 1. „UNKNOWN BUILD" = Debug-Dialog des Bedienmoduls (sicher)
- Quelle: Video `[lokaler Pfad]`, Bildbögen in `[lokaler Pfad]`.
- Service › TTE-BM › System (0) › Allgemein (0) › **04-045 Kommando** → Auswahl „Debug-Dialog" öffnet ein weißes Fenster mit Titel „UNKNOWN BUILD" und den Tasten „Code dialog" / „Reset". Zugeklappt bleibt nur die verschiebbare Titelzeile stehen.
- Auswahlliste 04-045: Option 0 / Restart / Debug-Dialog / Cursor anzeigen / Cursor ausblenden / Reset LD Strings / Zurücksetzen. **Die Werte sind NICHT fortlaufend: Debug-Dialog = 10** (per CAN gelesen). Werte der anderen Einträge unbekannt → nie raten (Zurücksetzen/Reset LD Strings!).
- 14.11.2026 10:2x: BM 17 `0-0-4045` stand auf **10**, BM 1 auf 0. Per CAN auf **0** geschrieben, zurückgelesen 0 (auch 20 s später), Lebenszeichen BM 17 läuft. Rückweg: 10 schreiben.
- Offen: ob das Kästchen damit sofort verschwindet oder erst nach „Restart" des Bedienmoduls (der Betreiber schaut nach).

## 2. Adressschema am CAN (neu, belegt durch Antworten)
- Ziel: 0x001 = WEZ, 0x208 = HV (UnitId 520), **0x400 + n = Bedienmodul n** (0x411 = BM 17, 0x401 = BM 1, 0x421 = HoxPi), 0x7FF = alle.
- Bedienmodul-eigene Datenpunkte sind per GET lesbar und per SET schreibbar. TTE-HV antwortet auf 0-0-4045 auch bei fremdem Ziel (eigener dp „Kommandos").
- Werkzeuge (nur Lesen / ein Byte schreiben): `[lokaler Pfad]`, `cc_bm_scan.py`, `cc_bm_set_u8.py` (auf dem Pi unter `/home/<user>/cc_tmp_skripte/`).

## 3. Einstellungen des Bedienmoduls (fg 80), Namen aus dem Video
- fn 0 Darstellung: Skin `00-001 Hintergrund` (0 = Schwarz) · Widgets `00-024 HomeScreen Links` (0 = Heizkreise; weitere: Wärmeerzeuger, Solar, Lüftung, Liste geht weiter) · `00-025 HomeScreen Mitte` (0 = Information) · System `00-101 gemeinsamer Betriebsmodus`, `00-110 Sonne Mondphase`, `00-111 Mondphase`, `00-010 Seite Menu`.
- Weitere fn: Helligkeit (1), Touchscreen (2), Zeit (4), ScreenVariablen (5), Piezo (6), Koordinaten (7), Leds (8), System (10).
- Live BM 17 (14.11.): 80-0-24 = 0, 80-0-25 = 0, 80-0-26 = 1, 80-0-27 = 1, 80-0-20 = 3, 80-0-21 = 26, 80-0-50 = 3. BM 1: 80-0-20 = 0, 80-0-21 = 3, 80-0-26/27 = 0, 80-0-50 = 10, 80-0-51 = 2.

## 4. Startbild links: „Soll 31,3 °C" statt Raumtemperatur
- Sicher: 31,3 °C = Reg 1490 (Vorlauf-Soll Konstantanforderung, von Loxone). Raumfühler im Bedienmodul lebt: Reg 1510 = 22,3 °C.
- Sicher aus alten Fotos: 09.01.2026 (Betriebsart „Früh+Abend") und 17.03.2026 („Konstant") zeigte dasselbe Feld **Raum-Ist** 21,9 / 21,7 °C. Seit der externen Anforderung („Externe Anf.", ab 29.08.2026) zeigt es den Vorlauf-Soll.
- Betriebswahl HK1 (Reg 1478) steht weiter auf 4 = Konstant; „Externe Anf." kommt von der laufenden Anforderung über 1490.
- Offen: ob die Liste „HomeScreen Links" einen Eintrag hat, der die Raumtemperatur zeigt (im Video nur bis „Lüftung" sichtbar).


## 5. Mitschnitt 14.11.2026 10:38–11:18 (der Betreiber am Display, Videos im Album)
- Dateien: Pi `/home/<user>/bm_rec/mitschnitt_20261114/` (candump + Einstellungen BM 17 alle 25 s), Videos `[lokaler Pfad]` (nur 512×288, Zahlen kaum lesbar), Auswertung `[lokaler Pfad]`.
- **10:44:14 „Restart" über 04-045** → Display startet neu, **„UNKNOWN BUILD" ist danach weg** (Video gpv_01, Startseite bei 1:00 ohne Kästchen). Der Debug-Dialog überlebt also das Zurücksetzen von 04-045, aber keinen Neustart.
- Beim Hochfahren hat der Betreiber den Bildschirm berührt → Touch-Kalibrierung („Tap and hold screen to calibrate") → danach Frage „Auf Werkseinstellungen zurücksetzen?" → **Abbrechen** gedrückt. Einstellungen danach unverändert (fg 80 verglichen), nur 80-0-4: 0 → 255.
- Am CAN beim Neustart: Rahmen mit Opcode 0x30 von WEZ/HV an 0x411 und von BM 17 an 0x401; danach schreibt BM 17 `1-0-58 = 0x8000`, `1-0-57 = 0x8000`, `1-0-1 = 226` und `1-0-505 = "Konstant"`.
- **Raumfühler:** BM 17 schreibt seine Raumtemperatur als `1-0-1` (= Reg 1510) an die WEZ, bei jeder Änderung um 0,1 K (22,6 → 22,5 → 22,6 → 22,5 → 22,4 °C zwischen 10:44 und 10:58).
- `80-0-24 HomeScreen Links`: 10:46:22 von 0 auf 2, 10:48:14 auf 1 gestellt (steht jetzt auf 1; vorher 0 = Heizkreise). `80-0-10` = „Seite Menu" (zuletzt offene Menüseite, wechselt beim Blättern).
- Neu gesehen (Video gpv_03, Darstellung › Alle Datenpkt.): Sprache, Hintergrund, **„Startbildschirm Type"**, Seite Menu. Nummer nicht lesbar, wahrscheinlich 80-0-2 (Wert 1 an beiden Bedienmodulen).
- Vorsicht bei „von 17" im candump: Bridge und `hoval_dp.py` senden mit Absender 17 (ID 1FE08A08 / 1FE08801). Die Minuten-SETs an 0x208 (50-0-[Nummer]) sind Loxone über die Bridge, die 5-Minuten-SETs 1-0-30046/30057/30066/3032 kommen vom Pi, nicht vom Display.


## 6. Nachtrag 14.11.2026 abends: Videos in voller Auflösung (1080p)
- Google-Photos-Freigaben liefern mit `=dv` nur 512×288. Mit `=m37` kommt 1080p (`[lokaler Pfad]` nimmt jetzt zuerst m37). Dateien: `[lokaler Pfad]`. **Regel: erst vorhandene Videos in voller Auflösung auswerten, bevor der Betreiber um neue Aufnahmen gebeten wird.**
- Sicher gelesen (Darstellung › Alle Datenpkt., fg 80 fn 0): `00-000 Sprache`, `00-001 Hintergrund`, **`00-002 Startbildschirm Type`** (live 1 an BM 17 und BM 1), `00-010 Seite Menu`.
- `00-024 HomeScreen Links`, vollständige Liste: 0 = Heizkreise, 1 = Wärmeerzeuger, 2 = Solar, 3 = Lüftung, 4 = leer. Kein Eintrag „Raumtemperatur". Belegt: Anzeige „Solar" bei Wert 2. Stand jetzt: 1 = Wärmeerzeuger.
- `00-025 HomeScreen Mitte`: 0 = Information.
- Offen: Auswahlliste von „Startbildschirm Type" (einziger verbliebener Kandidat für Raum-Ist auf der Startseite).


## 7. Selbstauskunft der Bedienmodule, nur gelesen (14.11.2026 22:05–22:15)
- Rohdaten: Pi `/home/<user>/bm_rec/mitschnitt_20261114/bm_selbstauskunft.txt`. Achtung: `cc_bm_scan.py` filtert bei Ziel 0x401 nur auf Absender 1 und mischt deshalb Antworten der WEZ (ebenfalls Absender 1) hinein; sicher vom Bedienmodul sind nur Antworten mit ID-Kopf 1FE0/1F60.
- **BM 1 (an der Wärmepumpe)** antwortet auf 0-0-20000…20204: ProductionDate [Nummer], S/N [entfernt], Typ „MMI4,3-1.4", Bootloader 1.22.002, Software 2.19.049, `20-005` = „D0C10000-FC1A0009-00211013-59154E45" (Bedeutung offen, wahrscheinlich Chip-Kennung), **`20-020` Bootloader Status = 0, `20-021` Fortschritt = 0**, VMLib 2.11.000, HW 04-093 = 205,00.
- **BM 17 (Wohnzimmer)** antwortet am Abend nur noch auf 0-0-4045 und fg 80 – nicht mehr auf 0-0-4093 und 91-0-0, die es am Vormittag beantwortet hat. Einziger Unterschied: Vormittags war der Debug-Dialog aktiv (bis zum Neustart 10:44). **Vermutung: Der Debug-Dialog öffnet zusätzliche Datenpunkte am Bus.** Nicht gegengeprüft.
- Kein Lesebefehl für Speicherinhalte gefunden; danach wurde auch nicht aktiv gesucht (nur GET auf Datenpunkte).
- der Betreiber 14.11. 22:03: Für aktive Versuche das Wohnzimmer-Display (BM 17) nehmen, nicht das an der Wärmepumpe („sicher schwieriger zu bekommen").


## 8. Startbildschirm Type (80-0-2) live durchprobiert, 14.11.2026 22:22 (BM 17, der Betreiber am Display)
Werte per CAN gesetzt und am Display fotografiert, danach zurück auf 1:
- **1** = Standard/Heizkreis „Untergeschoss" (oben links Soll/Raum, Haus-Symbol, WW) — der gewohnte, Werkszustand
- **2** = Lüftung groß (Bogenanzeige) + WW rechts
- **3** = Wärmeerzeuger (Vorlauf-Ist groß, Soll, Modulations-Tacho, Betriebsstunden 15095 h)
- **4** = Primär/Sekundär (Wärmetauscher, bei dieser Anlage leer „---")
- **5** = leer/ungültig (blauer Bildschirm, nur Icons)
→ **Ergebnis:** KEIN Startbildschirm-Typ zeigt eine reine Raumtemperatur. 80-0-2 wählt nur, WELCHES Teilsystem groß dargestellt wird.

**Damit ist belegt, dass der Startbildschirm-Typ NICHT der Hebel für die Raumtemperatur ist.** Der Typ-1-Bildschirm zeigte früher (Fotos 09.01. und 17.03.2026) Raum-Ist + Raum-Soll; er zeigt jetzt den Vorlauf-Soll (Reg 1490), **weil der Heizkreis auf „externe Anforderung" läuft (Loxone führt)**. Was oben links steht, hängt also an der Betriebsart/Führung des Heizkreises, nicht am Startbildschirm-Typ. Raum-Ist wieder auf die Startseite zu bekommen hieße, die externe Anforderung zu beenden — das wollen wir nicht, weil Loxone den Kreis regeln soll. Offener Rest-Hebel (unbelegt): ob es am Heizkreis selbst einen Darstellungs-/Anzeigeparameter gibt, der Ist statt Soll zeigt, ohne die Führung zu ändern.

**Zurückgestellt 22:25:** 80-0-2 (Startbildschirm Type) = 1, 80-0-24 (HomeScreen Links) = 0 (Heizkreise). Display zeigt wieder „Untergeschoss / Soll / Externe Anf.". „Soll 0,0" ist der aktuelle Vorlauf-Soll (HK UG fordert gerade nichts an), kein Fehler. Einziger noch nicht zurückgestellter Wert: 80-0-25 (HomeScreen Mitte) stand immer auf 0 (Information), unverändert.


## 9. Marktrecherche Ersatz-Bedienmodul (14.11.2026 22:35)
Ziel: ein Opfergerät zum Aufschrauben/Chip-Auslesen (Firmware), damit das einzige Wohnzimmer-Display nicht riskiert wird.
- **willhaben.at** „hoval toptronic bedienmodul" = 0 Treffer; „hoval toptronic" = 30, aber alle alte Generation (TopTronic 3, RS-10/RS-30, 233B), NICHT TopTronic E.
- **eBay.at** „hoval toptronic e bedienmodul" = 0 exakte Treffer (nur WEZ-Grundmodul, FW-Basismodul).
- **eBay.de — PASSENDER FUND:** „Hoval Bedienpanel Art.-Nr. **6049532** Bediengerät/Interface Typ 2-TTE R2 BM", Zustand **Nur Ersatzteile**, **49,99 € oder Preisvorschlag**, Privat, aus Deutschland. Link: https://www.ebay.de/itm/960040025984
  - Kauf trifft der Betreiber selbst (keine Bestellung durch Claude).
- Weitere Hoval-E-Module auf eBay.de (nur zur Einordnung, nicht gesucht): E-FE 6031164, E-PS 6037082, E-HKWW 6037081, SolarModul 6037058, je ~99 €.


## 10. Marktrecherche Fortsetzung (15.11.2026 13:45) — Verkäufer 6049532 liefert nicht nach AT
- Das 50-€-Defektteil (6049532, eBay [Nummer]) versendet NICHT nach Österreich → raus.
- **eBay — „Hoval 2 TTE BM 4,3"**, gebraucht (vermutl. funktionsfähig), 200 € o. Preisvorschlag, Kirkel/DE, Rücknahme aus. Versand-AT unklar (Verkäufer fragen). https://www.ebay.de/itm/187529887323 — das ist exakt unser 4,3"-MMI-BedienModul.
- **Kleinanzeigen — „Hoval TopTronic E Bedientableau Comfort"**, 160 € VB, „Versand möglich", Egling/Bayern, Anzeige vom 14.08.2026 (evtl. verkauft). https://www.kleinanzeigen.de/s-anzeige/hoval-toptronic-e-bedientableau-comfort/3484693410-168-7037 — Comfort-Variante, gleiche Farb-Touch-Plattform.
- Alle alten „TopTronic"-Treffer (T / 2B / 23B / 233B / RS-30) sind die VORGÄNGERgeneration, inkompatibel — beim Suchen „TopTronic E" bzw. „TTE BM" / „Bedientableau" verwenden, nicht nur „TopTronic".
- Bewertung: 160–200 € ist viel für ein reines Ausschlacht-/Firmware-Opfer. Sinnvoll nur, wenn ein funktionierendes Zweitdisplay gewünscht ist; fürs Chip-Auslesen besser auf ein billiges Defektteil warten. Kauf trifft der Betreiber selbst.