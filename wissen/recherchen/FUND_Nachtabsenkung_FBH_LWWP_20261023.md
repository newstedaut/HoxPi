# FUND Nachtabsenkung/Heizpause bei FBH + L/W-WP (23.10.2026)
Rechercheagent im Orchestratorlauf 23.10.2026 01:54 (MEHR Stufe 2). Stichprobe Claude: Effizienznetzwerke-Zitat per WebFetch wortgleich bestätigt.

## belegt
- **Effizienznetzwerke-Factsheet (Netzwerkinitiative):** WP + FBH für Nachtabsenkung oft ungeeignet; bei WP Absenkzeiten morgens verkürzen; Reaktionszeit FBH 3–4 h; allgemein ~2 %/K Ersparnis bei 8–9 h Absenkung, lohnt erst, wenn der Raum nachts ≥ 3 K auskühlen würde. – https://www.effizienznetzwerke.org/fileadmin/user_upload/2023/07/Netzwerkinitiative_Factsheet_Absenkung_der_Vorlauftemperatur_und_Anpassung_der_Heizkurve.pdf – „Wärmepumpen in Kombination mit Fußbodenheizung sind hingegen für eine Nachtabsenkung oft ungeeignet.“
- **BFE/EnergieSchweiz-Massnahmenblatt:** WP+Bodenheizung heizt morgens im schlechteren Betriebspunkt nach, Ersparnis kann verloren gehen oder ins Minus drehen; VL max. 2 K absenken; Reaktionszeit FBH 2–3 h. – https://pubdb.bfe.admin.ch/de/publication/download/9975 – „muss der Sinn einer Nachtabsenkung oft hinterfragt werden“
- **ewz Faktenblatt WP-Heizkurve:** Nachtabsenkung deaktivieren, stattdessen Heizkurve ~2 K tiefer durchgehend; VL in Schritten ≤ 2–3 K/Woche ändern; Spreizung 2–4 K. – https://www.ewz.ch/content/dam/stzh/energie/Startseite/beratung-froerderung/Faktenblatt_Waermepumpe-Heizkurve.pdf
- **energie-experten.org:** FBH = geringe Ersparnis durch Absenkung; L/W-WP-Wirkungsgrad sinkt beim morgendlichen Aufheizen. – https://www.energie-experten.org/heizung/heizungstechnik/heizungssteuerung/nachtabsenkung
- **Uni Innsbruck TheBat (Simulation, OTTI PV 2017):** Gebäudemasse + Speicher als thermische Batterie: Eigenverbrauch 7 % → bis 44 %, Netzbezug WP bis −54 % (20 m² PV); Raum im Mittel ~+1 K, etwas mehr Verluste. – https://www.uibk.ac.at/media/filer_public/9c/03/<UUID>/thebat_otti-pv-2017_thuer.pdf
- **energiesparhaus.at (2 Jahre Eigendaten L/W-WP + FBH):** Tagbetrieb hebt mittlere Außentemperatur der Laufzeit nur um 0,6–1,7 K; AZ-Gewinn niedriger einstelliger Prozentbereich; gut gedämmtes Haus verliert ~1 K/24 h ohne Heizung. – https://www.energiesparhaus.at/forum-nachtabsenkung-lwp-der-versuch-einer-erklaerung/47048_1
- Gegenbeleg UK (nur Heizkörper, kein FBH-Fall): Setback spart 5–6 kWh/Nacht, Wiederaufheizen 0,24–1,2 kWh. – https://renewableheatinghub.co.uk/forums/renewable-heating-air-source-heap-pumps-ashps/do-setbacks-save-energy-without-compromising-comfort

## wahrscheinlich
- FBH + gut gedämmtes Haus ohne PV/Tarifanreiz: netto bestenfalls ~1–3 %; Aufheizspitze (höherer VL, kälteste Stunde, Abtauung) kann das auffressen.
- Tagbetrieb mit Pause ~23–8 h kann funktionieren, wenn die WP im Winter nur ~50 % der Zeit läuft (Forenberichte, anekdotisch). – https://www.energiesparhaus.at/forum-waermepumpe-bei-starken-aussentemperaturschwankungen-effizient-nutzen/82570_1
- Einzelraumregelung bei WP: FBH-Kreise möglichst offen, wenig drosseln (Forenwissen). – https://www.energiesparhaus.at/forum-fussbodenheizung-einzelne-raeume-nicht-regelbar/62755_1
- Viessmann laut Utopia: moderate Einstellungen statt großer Sprünge (nur Sekundärquelle). – https://utopia.de/ratgeber/nachtabsenkung-bei-der-waermepumpe-ist-das-sinnvoll-und-wann-lohnt-es-sich-v2_915838/

## nicht gefunden
- Kontrollierter Feldtest (ISE/OST/BWP) JAZ mit vs. ohne Absenkung bei FBH + L/W-WP (ISE „WPsmart im Bestand“ geprüft: nichts dazu).
- Hoval-/Vaillant-/Bosch-Primärquelle zur Nachtabsenkung.
- Belastbare Zahlen zum Abtau-Mehraufwand in den Morgenstunden.

## Was bringt uns das
1. Keine WP-Heizpause nachts als Grundeinstellung; erst Heizkurve senken (0,9 → 0,8, 1–2 K/Woche), dann über Absenkung nachdenken.
2. Wenn testen: max. 1–2 K, Fenster eher 22–04 h, nicht bis in den Morgen. A/B mit HoxPi je 1–2 Wochen bei ähnlicher Außentemperatur: Wärme, Strom, Starts, Abtauungen (7-Tage-AZ, siehe `HoxPi-Doku\ANALYSE_Datenqualitaet_Volllogger_Winter-AZ_20261023.md`).
3. Alpenort (~960 m): kalte Talnächte, oft sonnige Nachmittage → Tagbetrieb hier eher sinnvoll als im Flachland (Vermutung; mit Außentemperaturverläufen prüfen).
4. Absenken nicht über „alle Ventile zu“ – Stellantriebe in FBH-Räumen überwiegend offen, Raumsoll-Toleranzen eng.
5. Holzofenraum nicht auf 0 % Ventil – sonst Estrich nachts kalt und morgens Aufheizspitze (passt zu `ANALYSE_Holzofen_UG_Raumregelung_20261022.md`).
6. Mit PV/Zeittarif: Raumsoll mittags +0,5–1 K, Estrich laden.

Hinweis: Zitate aus WebFetch-Auszügen; vor Weitergabe Original prüfen.