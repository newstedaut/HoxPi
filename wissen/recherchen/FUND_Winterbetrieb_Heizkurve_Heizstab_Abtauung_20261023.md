# FUND Winterbetrieb: Heizstab-Freigabe / Abtauung / Heizkurve (23.10.2026)

Orchestrator-Recherche (Claude), ersetzt die abgebrochene Recherche vom 22.10. (die alte 134-Byte-Datei bleibt bestehen).
Anlage: Hoval UltraSource B comfort C (17), TopTronic E, FBH 2 x ca. 100 m², Alpenort (~960 m) ca. 950 m.
Methode: WebSearch/WebFetch (energiesparhaus.at war heute ERREICHBAR), dazu lokale Hoval-PDFs in quellen/ per fitz-Textlayer.
Zitate stammen wörtlich aus WebFetch-Ausgaben oder aus dem fitz-Text. „(lokal)“ heißt: nur die lokale Kopie wurde geprüft.

## 1. Heizstab / Elektroheizeinsatz / Bivalenz

### belegt
- B1 Der Heizstab ist in der Inneneinheit verbaut, 1 bis 6 kW. Technikhandbuch S. 5 (lokal): „Elektroheizeinsatz 1 bis 6 kW“.
  Datei: quellen/Hoval_UltraSource_B_Technikhandbuch.pdf (Stand 2026/27)
- B2 Für die Größe (17) ist der Anschluss 3 x 400 V, 6 kW. Technikhandbuch S. 34 (lokal): „für (11,17): 3 x 400 V/50 Hz (6 kW)“
- B3 Hoval definiert den Bivalenzpunkt nur allgemein. Technikhandbuch S. 40 (lokal): „Die Wärmepumpe heizt bis zum Zuschalt- punkt (Bivalenzpunkt) allein. Danach heizt ein zusätzlicher Wärmeerzeuger parallel dazu.“
- B4 Mit Heizstab ist eine höhere Vorlauftemperatur möglich. Hoval-Prospekt AT: „Vorlauftemperatur max. (ohne/mit Einschraub-Elektroheizeinsatz) °C 62/65“
  URL: https://cdn.hoval.com/prospekt_ultrasource_b_t_at-d_de_hybris_original.pdf
- B5 TopTronic E (Firmware-Teil, Dokument 4 214 513) hat eine Ausgangszuordnung für den Heizstab und einen Sperrkontakt, aber nur für die WW-Nachladung. S. 153/154 (lokal): „32-031 Zuo. Ausg. Elektroheizeinsatz 0=AUS“ und „30-031 Zuo. Eing. Sperr-Kontakt ELH … Elektroheizeinsatz (WW-Nachladung)“
- B6 Forum, Nutzer, keine Hoval-Aussage. Optihome, 23.4.2023: „Um den Heizstab abzuschalten solltest du einfach die Sicherung rausmachen.“
  URL: https://www.energiesparhaus.at/forum-hoval-ultrasource-lwp-allgemeiner-austausch-und-anlage-optimieren/56645_2

### wahrscheinlich
- Die Heizstab-Freigabe im Heizbetrieb (Bivalenztemperatur, Verzögerung, Notbetrieb) liegt in der WEZ-/WFA-200-Ebene des Wärmeerzeugers und nicht im allgemeinen TTE-Heizkreisteil. Im öffentlichen 4 214 513 gibt es dazu keinen Parameter. Der Hinweis „Bivalent- und Kaskadenmanagement“ (Technikhandbuch S. 6) bestätigt nur, dass die Funktion existiert.

### nicht gefunden
- Öffentlich gibt es keine Parameternummer oder Werkseinstellung für Bivalenztemperatur, Freigabeverzögerung, AT-Sperre oder Notbetrieb des Heizstabs bei der UltraSource. Gesucht wurde auf cdn.hoval.com, im Prospekt und in den energiesparhaus-Threads 56645, 69252, 70426 und 75450. Die Werte aus FUND_Warmwasser_…_Heizstab Abschnitt 3 bleiben deshalb UNBELEGT.

## 2. Abtauung

### belegt
- A1 Ein Puffer ist wegen der Abtauenergie Pflicht. Technikhandbuch S. 37 (lokal, schon am 19.10. geprüft): „Bei Luft/Wasser-Wärmepumpen von Hoval ist ein Energiepufferspeicher zwingend erforder- lich (Abtauenergie).“ Ausnahme: „⅔ müs­sen unabsperrbar sein“.
- A2 Kondensat pro Abtauzyklus. Technikhandbuch S. 35 (lokal): „pro Abtauzyklus inner- halb von 2 Minuten bis zu 6 Liter“
- A3 Die Leistungskurven für (17) berücksichtigen die Abtauung. Technikhandbuch S. 24 (lokal): „Maximale Heizleistung unter Berücksichtigung der Abtauverluste UltraSource® B comfort C (17)“
- A4 Prinzip der Kreislaufumkehr, allgemein (Stiebel Eltron, nicht Hoval). Wärme wird „temporarily from the water in the buffer cylinder or underfloor heating system“ entnommen.
  URL: https://www.stiebel-eltron.co.uk/en/service/faq/what-is-defrosting-by-circuit-reversal-.html
- A5 Praxis UltraSource, Forum. Optihome, 2.12.2023: „Je höher die Modulation/Leistung desto eher muss sie wieder abtauen.“
  URL: https://www.energiesparhaus.at/forum-hoval-ultrasource-lwp-allgemeiner-austausch-und-anlage-optimieren/56645_3
- A6 Forum. Optihome, 22.11.2023: „taut nur häufig (ca. alle 2 Stunden) ab, wenn sie voller Leistung (> 80 Modulation und unter -10 Grad) läuft.“ Domi90, 18.11.2023: „bei einer momentanen Ausentemperatur von 0-4Grad ca. jede Stunde einmal abtaut.“
  URL: https://www.energiesparhaus.at/forum-hoval-ultrasource-lwp-allgemeiner-austausch-und-anlage-optimieren/56645_2
- A7 Forum. Domi90, 11.12.2023: „taut die LWP … nun ca. 5-7mal ab, vorher 16-18 mal“. stogey, 21.12.2023: „taut ca. alle 1.5h Stunden ab“
  URL: https://www.energiesparhaus.at/forum-hoval-ultrasource-lwp-allgemeiner-austausch-und-anlage-optimieren/56645_3

### wahrscheinlich
- Die UltraSource taut per Kreislaufumkehr ab und holt die Energie aus dem Puffer bzw. Heizwasser. Das schließe ich aus A1 („Abtauenergie“ verlangt Puffer) zusammen mit A4. Der Wortlaut „Kreislaufumkehr“ wurde in keiner Hoval-Quelle gefunden. Abhilfe: VL/RL während des Status „Abtaubetrieb“ im HoxPi-Verlauf ansehen. Fällt der VL unter den RL, ist das ein Hinweis auf Umkehr.
- Die Abtaugrenzwerte 33-281/282/283 (36 °C / 25 °C / 15 min) stammen aus Nutzerangaben in 56645 (2020), siehe STAND 20.10. Eine Hoval-Primärquelle dafür fehlt.

### nicht gefunden
- Ob der Heizstab während der Abtauung zugeschaltet wird, steht öffentlich nirgends.
- Ein Hoval-Mindestpuffervolumen in l/kW für die Abtauung ist nicht beziffert, nur das Planungskapitel (S. 42): „Mindestgrösse Energiepufferspeicher festlegen“.
- Auch eine Mindest-Rücklauf- bzw. Puffertemperatur für die Abtauung fehlt bei Hoval. Bei iDM sind es 20 °C, siehe FUND_Abtauung Fund 1.

## 3. Heizkurve / Heizgrenze (FBH + L/W-WP)

### belegt
- H1 Die TopTronic-E-Kennlinie hat 4 Punkte und keine Steilheitszahl. 4 214 513 S. 136 (lokal), Werkseinstellungen: 03-013 „Auslegep. VL-temp. Heizkennlinie 35 °C“, 03-001 „Fussp. VL-temp. Heizkennlinie 25 °C“, 03-011 Fußpunkt AT 20 °C, 03-012 „Auslegep. AT-temp. Heizkennlinie 5 °C -30 10“.
  Achtung: Beim Vorzeichen von 03-012 kann der Textlayer ein Minus verloren haben. Am Bediengerät prüfen.
- H2 Heizgrenze 03-021. S. 137 (lokal): „03-021 Heizgrenze Aussentemperatur 18 °C“. S. 144: „sinkt die mittlere Aussentemperatur 0.5K unter den eingestellten Wert, schaltet die Heizung wieder ein“. Die Heizgrenze verschiebt sich mit dem Raumsollwert: Beispiel 17 °C bei 20 °C Raum ergibt 19 °C bei 22 °C Raum.
- H3 Raumeinfluss bei FBH. S. 137 (lokal), 03-007: „Bei Fussbodenheizungen sollte dieser Wert nicht über 4 eingestellt werden.“
- H4 suissetec-Merkblatt „Fussbodenheizung richtig nutzen“ (2011): „Vorlauftemperatur (Fussbodenheizungen): max. 35 °Celsius“
  URL: https://merkblatt.suissetec.ch/de-CH/HEIZ111/file/HEIZ111.pdf
- H5 Energieberatung Stadt Zürich, Faktenblatt WP-Heizkurve (2023): „Tagesheizgrenze deaktivieren und Sommer / Winter-Heizgrenze auf 18 ° C einstellen.“ Vorgehen dort: bei FBH einmal um 3 °C senken, danach höchstens 1x pro Woche 2 bis 3 °C ändern.
  URL: https://www.ewz.ch/content/dam/stzh/energie/Startseite/beratung-froerderung/Faktenblatt_Waermepumpe-Heizkurve.pdf
- H6 Forum UltraSource. Optihome, 28.11.2023: „Bei steht die Kurve auf 35 bei -10 Grad und 20 bei +20 Grad.“ Marty, 21.12.2023: „Deine Normaußentemperatur laut EA … ist -13,2°“ (er meint: Kurve auf die Normaußentemperatur auslegen)
  URL: https://www.energiesparhaus.at/forum-hoval-ultrasource-lwp-allgemeiner-austausch-und-anlage-optimieren/56645_2 (Optihome) bzw. …/56645_3 (Marty)

### wahrscheinlich
- Für eine FBH in einem ordentlich gedämmten Haus sind etwa 30 bis 35 °C VL bei rund -15 °C realistisch, mit Fußpunkt ca. 20 bis 23 °C VL bei +20 °C AT. Das entspricht einer Steilheit von etwa 0,3 bis 0,4. Die Steilheit ist von mir aus H4/H6 abgeleitet und keine Herstellerzahl.
- Die Zürcher Tabelle (35–40 °C bei -7,5 °C, Steilheit 0,7) ist ein Startwert für alle Heizflächen und für FBH eher zu hoch.

### nicht gefunden
- Es gibt keine Hoval-Empfehlung für eine Steilheit oder Heizkurve speziell im Alpenraum.
- Die Normaußentemperatur für Alpenort (~960 m) wurde nicht recherchiert (ÖNORM B 8110-5 bzw. Energieausweis prüfen). Die -15 °C sind eine Annahme.

## Was bringt uns das (des Betreibers Anlage)
1. Der Heizstab hat 6 kW (3 x 400 V) und steckt in der Inneneinheit. Wann er im Heizbetrieb freigegeben wird, ist öffentlich nicht dokumentiert. Das ist eine WEZ-/Fachmann-Einstellung.
   Vorgehen: Den Heizstab-Status (Relais/Leistung) im HoxPi-Verlauf an kalten Tagen und bei Abtauungen beobachten. Daraus lassen sich Freigabeschwelle und -verzögerung empirisch bestimmen, statt Werte zu raten.
2. Wenn der Heizstab nie laufen soll, ist die Sicherung der praktischste Weg (Forum, B6). Das kostet aber die Reserve bei Störung oder Notbetrieb. Davon rate ich im Winter in 950 m eher ab.
3. Abtauung: Der Puffer ist laut Hoval wegen der Abtauenergie Pflicht. Der Puffer (laut Speicherart-Fund wahrscheinlich EnerVal) sollte also im Winter nicht kalt laufen.
   Die Loxone-Stellantriebe sollten bei einer Abtauung nicht alle zu sein. Bei iDM ist die Regel „25 % der Kreise offen“ belegt, bei Hoval ist sie nur sinngemäß zu übertragen.
4. Abtauhäufigkeit: Ca. 1x pro Stunde bei 0–4 °C und feuchter Luft ist bei der UltraSource laut Forum normal. Höhere Modulation bedeutet mehr Abtauen. Ein Grund mehr für eine flache Heizkurve und niedrige Leistung.
5. Heizkurve: Die Werkseinstellung (Fuß 25/20, Auslegung 35 °C) ist für eine FBH eher zu hoch angesetzt. Den Wert 03-012 am Gerät ablesen und auf die Normaußentemperatur von Alpenort (~960 m) setzen.
   VL-Ziel ≤ 35 °C, eher ~32 °C. Absenken in 1–2 K-Schritten pro Woche. Raumeinfluss 03-007 ≤ 4, das ist wichtig wegen des Holzofens. Heizgrenze 03-021 um 15–17 °C sinnvoll (Werk 18 °C).
6. Offen: Typenschild/Bediengerät für 03-012 (Vorzeichen), Heizstab-Statusregister im HoxPi suchen, Normaußentemperatur Alpenort (~960 m) aus dem Energieausweis.