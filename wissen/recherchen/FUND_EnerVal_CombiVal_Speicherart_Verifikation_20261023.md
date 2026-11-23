# FUND: Speicherart EnerVal / CombiVal ESR – Verifikation (23.10.2026)

Anlass: Projektdoku sagt „Enerval 300 = Warmwasserspeicher, CombiVal ESR 400 = Puffer“. FUND_Speicher_Bereitschaftsverlust_EnerVal_CombiVal_20261022.md sagte aus dem Katalog 2026 das Gegenteil. Hier unabhängig gegengeprüft.

Quellen:
- Q1: Hoval Katalog „Speicher Trinkwassererwärmung 2026/27“ (DE), https://cdn.hoval.com/speicher_trinkwassererwarmung_katalog_2026_de_exa_hybris_original.pdf (40 MB; diesmal per curl geladen und mit pdftotext komplett durchsucht, nicht nur übernommen)
- Q2: Hoval Prospekt UltraSource B/T, Österreich-Ausgabe, Druckvermerk „4217308 | 2021 - 04“, https://cdn.hoval.com/prospekt_ultrasource_b_t_at-d_de_hybris_original.pdf (1,5 MB, per WebFetch lesbar)
- Q3: energiesparhaus.at-Forum, Thread „Hoval UltraSource B comfort 11 Optimierung / kühlt nicht“, https://www.energiesparhaus.at/forum/85791

## Belegt
1. EnerVal = Energiepufferspeicher (Heizungswasser), kein Trinkwasserspeicher.
   - Q1, Produktbeschreibung: „Energiepufferspeicher aus Stahl für die hydraulische Einbindung von Energieerzeugern“
   - Q1, Techn. Daten: max. Betriebs-/Prüfdruck „3/4“ bar (alle Größen), kein Register, keine Emaillierung, keine Anode.
   - Größe 300 gibt es: Q1 „(300) B 283 3“ (Typ, Klasse, Inhalt l, Betriebsdruck bar).
2. CombiVal ESR = Trinkwassererwärmer (Speicher-Wassererwärmer) mit EINEM großen Glattrohr-Register.
   - Q1: „Wassererwärmer aus Stahl innen emailliert mit fest eingebautem Glattrohrregister.“
   - Q1, Untertitel: „Wassererwärmer mit grossem Register für kombinierte Aufheizung“
   - Q1: Magnesium-Schutzanode, Flansch für E-Heizeinsatz, Betriebsdruck Trinkwasser 6 bar (SVGW) / 10 bar (DVGW).
   - Größe 400 gibt es: Q1 Artikelnummern „(400) 379 3.8 7015 967“ (Inhalt l, Heizfläche m², Art.-Nr.).
3. Hoval selbst kombiniert UltraSource mit CombiVal ESR als WW-Speicher (Systemlösung, Prospekt AT 2021).
   - Q2: „erwärmt das Brauchwasser, welches der CombiVal speichert.“
   - Q2, Komponentenleiste „Schema PV/HomeVent“: „UltraSource® B/T comfort“ – „CombiVal ESR (300)“ – „HomeVent® comfort FR (351)“.

5. Datenblattwerte (Q1, Ausgabe 2026/27; deckungsgleich mit FUND vom 22.10.):
| Typ | Inhalt | Dämmung PU | Warmhalteverlust 65 °C | ≈ kWh/24h | ErP | Register |
|---|---|---|---|---|---|---|
| CombiVal ESR (300) | 298 l | 50 mm | 68 W | 1,63 | B | 2,6 m², 16 l, z = 17 |
| CombiVal ESR (400) | 379 l | 75 mm | 68 W | 1,63 | B | 3,8 m², 34 l, z = 6 |
| EnerVal (300) | 283 l | 75 mm | 51 W | 1,22 | B | keines |
   Zitat Q1 ESR: „Warmhalteverlust bei 65 °C W 48 68 68“; EnerVal: „Warmhalteverlust bei 65 °C W 35 53 51 72 …“
6. Anschlüsse / Fühler (Q1, Massblätter):
   - CombiVal ESR (400): Kaltwasser und Warmwasser G 1″ AG; Register-Vorlauf/-Rücklauf „Typ (400) G 1¼″ (AG)“; Zirkulation G ¾″ AG; Thermometer; Handloch-Flansch Ø 180 (E-Heizeinsatz); Anodenmuffe Rp 1″.
     Fühler: EIN „Fühlerkanal Innen-Ø 11 mm“ mit abnehmbarer Kappe „zur Positionierung des Fühlers im Fühlerkanal“ → WW-Fühlerhöhe ist frei wählbar, also nicht aus dem Katalog ablesbar.
   - EnerVal (300): „(300): 8 x Anschluss-Muffen Rp 1½″“, „1 x Muffe Rp ½″ mit Thermometer und Tauchhülse“, „(200,300): 2 x Fühlerkanal“. Kein Register, Anschlüsse frei belegbar (WE-VL/RL, Heizkreis-VL/RL), E-Heizeinsatz-Muffe G 1½″ „Positionierung abhängig von der Anlage“.
   - Masse ESR (400): D 750 mm, H 1629 mm, Kippmass 1788 mm. Masse EnerVal (300): nicht sauber aus Text extrahierbar.
7. Hoval-Planungsseite (Q1, Projektierung): Bei WP: „Vorwärmung mit Wärmepumpe und Nach­wärmung mit Elektroheizeinsatz ist möglich.“ und Hinweis „Speicher-Wassererwärmer mit grossem Wasserinhalt“ für periodische Nachheizung.

## Wahrscheinlich
- In der Projektdoku sind die Rollen VERTAUSCHT. Richtig ist sehr wahrscheinlich: CombiVal ESR 400 (379 l) = Warmwasserspeicher (Register von der WP geladen), EnerVal 300 (283 l) = Heizungs-/Kühlpuffer. Summe 662 l passt zu „ca. 700 l“.
- Begründung: Ein EnerVal darf nach Datenblatt kein Trinkwasser führen (3 bar, keine Emaillierung/Anode). Ohne Frischwasserstation kann der EnerVal kein Warmwasser liefern.
- Genau diese Kombination (UltraSource + CombiVal ESR für WW + EnerVal als Puffer) ist bei Hoval-Anlagen in AT üblich (Q2 Systemlösung, Q3 Praxisanlage). Die HomeVent comfort FR in Q2 passt außerdem zur vorhandenen Hoval-KWL (Modell bei der Betreiber noch offen).
- Der 22.10.-FUND ist damit bestätigt, nicht widerlegt.

## Nicht gefunden
- EPREL-Produktdatenblatt (Fiche) für Hoval CombiVal ESR oder EnerVal. Die Suche liefert nur fremde Fiches (Kermi x-buffer combi Nr. 135329, Vaillant VIH S 300/3 BR Nr. 86438, VIH R 150/6 B Nr. 662454).
- Katalogwerte aus 2021 (Baujahr der Anlage). Die Werte oben stammen aus 2026/27, der Prospekt Q2 von 2021 nennt nur Typen, keine Verluste.
- Offizielles Hoval-Hydraulikschema UltraSource B comfort C mit EnerVal als Puffer (das Schema-Dokument aus Q2 zeigt nur Icons, keine Leitungsführung).
- Höhenangaben der Fühlerkanäle bzw. Fühlerposition (Katalog: Position im Kanal frei wählbar).

## Was bringt uns das
1. Projektdoku korrigieren (Projektanweisung „Bekannte Heizungsanlage“ und alle Docs, die den Enerval als WW-Speicher führen): WW = CombiVal ESR 400 (379 l, Register 3,8 m²), Puffer = EnerVal 300 (283 l, 3 bar). Vorher noch Typenschild-Fotos abwarten (siehe 2), dann korrigieren.
2. der Betreiber soll fotografieren:
   - Typenschild beider Speicher (meist oben am Mantel oder hinten unten): Typ, Art.-Nr. (ESR 400 = 7015 967), Inhalt, Betriebsdruck. Ein „3 bar“ auf dem Schild = Puffer.
   - Welche Leitung Kaltwasser/Warmwasser/Zirkulation trägt (Speicher mit Kaltwasser-Anschluss und Sicherheitsgruppe = WW-Speicher).
   - Steckplatz und Höhe des WW-Fühlers im Fühlerkanal des CombiVal (Kappe Ø 60 mm oben); beim EnerVal beide Fühlerkanäle und welcher Fühler (Pufferfühler oben/unten) wo steckt.
   - Ob ein Flansch-Elektroheizeinsatz im CombiVal (Handloch-Flansch) oder eine Einschraub-Heizpatrone im EnerVal steckt (offene Frage „Heizstab vorhanden?“).
3. Rechnungen im 22.10.-FUND (Bereitschaftsverlust WW mit 379 l und 68 W bzw. 1,51 W/K) bleiben gültig, wenn die Typenschilder die Rollen bestätigen.
4. Für die Kühlung: Der Puffer (EnerVal, ohne Register, 283 l) ist der Speicher, der im Kühlbetrieb kalt wird. Der Taupunkt an den Puffer-Anschlüssen ist zu beachten (EnerVal min. Betriebstemperatur laut Q1 5 °C).