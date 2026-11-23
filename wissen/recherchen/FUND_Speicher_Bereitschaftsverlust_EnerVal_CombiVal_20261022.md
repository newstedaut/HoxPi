# FUND: Bereitschaftsverlust EnerVal / CombiVal ESR – Datenblatt vs. Messung (22.10.2026)

Hauptquelle Q1: Hoval Katalog „Speicher Trinkwassererwärmung 2026/27“ (DE), https://cdn.hoval.com/speicher_trinkwassererwarmung_katalog_2026_de_exa_hybris_original.pdf
(PDF per WebFetch abgelehnt, per curl geladen und mit pdftotext gelesen; Zitate aus dem Volltext)
Q2: BDH Infoblatt 74, https://www.bdh-industrie.de/fileadmin/user_upload/Publikationen/Infoblaetter/Infoblatt_Nr_74_Energetische_Bewertung_Warmwasserspeicher.pdf
Q3: DBU-Abschlussbericht AZ 29647 (Einrohrzirkulation), https://opac.dbu.de/ab/DBU-Abschlussbericht-AZ-29647.pdf
Q4: SBZ Monteur, Thermosiphon, https://www.sbz-monteur.de/sites/default/files/sbzm_pdf/file_294268.pdf
Q5: SBZ Monteur, Rohrdämmung, https://www.sbz-monteur.de/sites/default/files/sbzm_pdf/file_198710.pdf

## 0. Typ-/Rollenprüfung (nur Bericht, nichts korrigiert)
BELEGT (Q1):
- EnerVal = Pufferspeicher: „Energiepufferspeicher aus Stahl für die hydraulische Einbindung von Energieerzeugern“; Artikeltext „Stahlbehälter innen roh“, Betriebsdruck 3 bar. -> kein Trinkwasserspeicher.
- CombiVal ESR = Trinkwassererwärmer: „Wassererwärmer aus Stahl innen emailliert mit fest eingebautem Glattrohrregister“, Untertitel „Wassererwärmer mit grossem Register für kombinierte Aufheizung“.
- CombiVal ESR hat laut Katalog EIN großes Register (nicht 2 Wärmetauscher/Solar). Volumina: ESR 200 = 193 l, ESR 300 = 298 l, ESR 400 = 379 l. EnerVal 300 = 283 l.
WAHRSCHEINLICH: In der Projektbeschreibung sind die Rollen vertauscht. Plausibel ist: WW-Speicher = CombiVal ESR 400 (379 l), Puffer = EnerVal 300 (283 l). Summe 662 l ≈ „ca. 700 l“ passt.
NOCH ZU PRÜFEN: Typenschilder fotografieren. Ein „EnerVal“ als WW-Speicher wäre unzulässig (innen roh, 3 bar).

## 1. Datenblattwerte (Q1, Ausgabe 2026/27)
| Typ | Volumen | Dämmung PU | U-Wert | Warmhalteverlust bei 65 °C | ErP-Klasse |
|---|---|---|---|---|---|
| CombiVal ESR (200) | 193 l | 75 mm | 0,32 W/m²K | 48 W | B |
| CombiVal ESR (300) | 298 l | 50 mm | 0,41 W/m²K | 68 W | B |
| CombiVal ESR (400) | 379 l | 75 mm | 0,32 W/m²K | 68 W | B |
| EnerVal (200) | 222 l | 50 mm | 0,359 | 53 W | B |
| EnerVal (300) | 283 l | 75 mm | 0,279 | 51 W | B |
| EnerVal (500) | 473 l | 75 mm | 0,296 | 72 W | B |
Zitat Q1 (ESR-Tabelle): „• Warmhalteverlust bei 65 °C  W  48  68  68“
Zitat Q1 (EnerVal-Tabelle): „• Warmhalteverlust bei 65 °C  W  35 53 51 72 119 130 153 185“
Klassen: Modellreihen-Tabelle Q1 „ESR (200) B / ESR (300) B / ESR (400) B“, EnerVal „(300) B“.

Prüfbedingungen (Q2): „Dabei wird das Wasser im Speicher mit einem elektrischen Heizelement auf eine Temperatur von 65 ± 3 °C erwärmt.“ und „bezieht sich immer auf eine Temperaturdifferenz von 45 K.“ Umrechnung Q2: „1 W entsprechen 0,024 kWh/d.“
Wichtig (Q2): Prüfung ohne Anlage, Speicher „weder an das Trinkwassernetz noch an einen Wärmeerzeuger angeschlossen“. Rohr-/Einrohrzirkulationsverluste sind also NICHT in S enthalten.
-> Datenblatt in kWh/24h bei ΔT 45 K: ESR 400 und ESR 300: 68 W·24 h = 1,63 kWh/d; EnerVal 300: 51 W = 1,22 kWh/d.
Hinweis: Die Werte stammen aus dem Katalog 2026/27. Werte für das Baujahr 2021 (älterer Katalog/EPREL-Blatt) habe ich nicht gefunden, sie können abweichen (z. B. 50 vs. 75 mm Dämmung).

## 2. Rechnung: Messung vs. Datenblatt
Ansatz: Datenblattverlust ist proportional zu ΔT -> Verlustkoeffizient UA = S / 45 K.
- ESR 400 / ESR 300: UA = 68/45 = 1,51 W/K. EnerVal 300: 51/45 = 1,13 W/K.
- Unser Betrieb: Speicher 52–57 °C, Raum 20 °C -> ΔT 32–37 K (Mitte 34,5 K).
- ESR 400 laut Datenblatt: 1,51·32 = 48 W (1,16 kWh/d) bis 1,51·37 = 56 W (1,34 kWh/d); Mitte 52 W = 1,25 kWh/d.
- EnerVal 300 bei 34,5 K: 39 W = 0,94 kWh/d.

Messung: Abfall oben 0,3 K/h. Energie bei gleichmäßiger Abkühlung: Q = V·1,163 Wh/(l·K)·0,3 K/h
- 298 l -> 104 W = 2,50 kWh/d | 379 l (ESR 400) -> 132 W = 3,17 kWh/d | 283 l -> 99 W = 2,37 kWh/d
- Eure Schätzung 2,6 kWh/d = 108 W -> UA_gemessen = 108/34,5 = 3,1 W/K.

Ergebnis: Gemessen ~2,6 kWh/d, Datenblatt (ESR 400, auf ΔT umgerechnet) ~1,25 kWh/d -> etwa Faktor 2. Wenn der WW-Speicher wirklich der ESR 400 mit 379 l ist und der ganze Inhalt mit 0,3 K/h abkühlt, wäre es sogar Faktor 2,5.
Differenz ≈ 108 − 52 = ~56 W ≈ 1,35 kWh/d ≈ 490 kWh/a Wärme.
Einschränkungen der Messung:
- Der Fühler oben sieht nicht den Mittelwert. Kühlt nur die obere Zone ab oder gibt sie Wärme nach unten ab, ist der echte Verlust kleiner.
- Läuft nachts die Zirkulation, wird die WW-Zone zusätzlich gemischt und gekühlt. Es zählt dann nicht nur der Speicherverlust.
- Thermosiphon über das Register (WP-Ladekreis VL/RL ohne Schwerkraftbremse oder Rückschlagventil) würde direkt Wärme aus dem Speicher in die Leitungen bzw. zur WP tragen.
Bewertung: Eine Abweichung um Faktor ~2 ist in realen Anlagen typisch und nicht dramatisch. Rund die Hälfte des gemessenen Verlusts ist aber anlagenbedingt, nicht durch den Speicher selbst.

## 3. Zusatzverluste
BELEGT:
- Einrohrzirkulation (ERZ) an Anschlüssen ohne Thermosiphon (Q3): „Typische Speicherverluste mit Rohrdimensionen wie im Einfamilienhaus üblich fallen mit ERZ um etwa die Hälfte höher aus“. Für Speicher bis 300 l werden 200–400 kWh/a genannt. Je waagrechtem 22-mm-Cu-Anschluss: „im Bereich von 0,05 bis 0,3 W/K“.
  -> bei ΔT 34,5 K sind das 1,7–10 W pro Anschluss. Bei 5 Anschlüssen (KW, WW, Zirk, Register-VL/RL) kommen 9–52 W zusammen. Das allein kann die Differenz von ~56 W fast erklären.
- Thermosiphon (Q4): 2 m DN 25 gedämmt bei 60 °C ohne Siphon „ca. 0,28 W/K“, mit 25 cm Siphon „nur einen Wärmeverlust von 0,05 W/K“. Das sind rund 80 % weniger.
- Hoval-Vorgabe (Q1, Planung): „Die Warmwasserleitung ist wärmegedämmt und siphoniert (Minimum ≥ 200 mm) zu montieren.“
- Gedämmte Zirkulations-/WW-Leitung (Q3): 22-mm-Cu mit 25 mm Dämmung „ergibt sich z. B. ein Wert für UL,R von 0,19 W/(mK)“.
  -> bei 55 °C und 20 °C Raum: 0,19·35 = 6,7 W/m. 20 m Zirkulationsschleife im Dauerbetrieb: 134 W ≈ 3,2 kWh/d. Das ist mehr als der ganze Speicherverlust.
- Vergleich (Q5): 15-mm-Rohr mit 60 °C, 27 mm Dämmung WLG 040, „reduziert sich die Leistung auf 6 Watt je laufenden Meter“. Ungedämmt sind es „fast 50 Watt“.
- Dämmpflicht (Q5, EnEV = GEG 100 %): „Rohrleitungen mit einem Innendurchmesser bis 22 mm müssen mit einer Dämmschichtdicke von 20 mm gedämmt werden.“
NICHT GEFUNDEN:
- EPREL-Produktblatt (Fiche) für Hoval CombiVal ESR / EnerVal ohne Login. Die Suche lieferte nur fremde Fiches (Kermi, Vaillant).
- Ältere Hoval-Kataloge mit Werten für das Baujahr 2021.
- Ein offizieller GEG-Tabellenwert in W/m (GEG regelt nur Dämmdicken, keine W/m).

## 4. Was bringt uns das
- WW-Soll 57 -> 52 °C: Nach Datenblatt (1,51 W/K · 5 K) sind das ~7,5 W ≈ 0,18 kWh/d ≈ 66 kWh/a Wärme. Mit dem real gemessenen UA (3,1 W/K · 5 K) sind es ~16 W ≈ 0,38 kWh/d ≈ 137 kWh/a Wärme, also nur ~45–55 kWh/a Strom bei WW-COP 2,5–3. Dazu kommt ein etwas besserer COP beim Laden. Das spart wenig. Mindestens einmal pro Woche sollten 60 °C erreicht werden (Legionellen, Rechtslage AT/ÖNORM B 5019 selbst prüfen).
- Speichermantel nachdämmen: lohnt kaum. Es gibt schon 75 mm PU (ESR 400) bzw. U = 0,32. Das Potenzial liegt bei einigen W.
- Größerer Hebel: Anschlüsse. Zuerst prüfen, ob WW-Austritt, Zirk-Eintritt und Register-VL/RL einen Siphon (≥ 200 mm nach unten) oder eine Schwerkraftbremse haben. Stutzen, Flansch, Fühlerkanal und Thermometer bis an den Mantel lückenlos dämmen. Möglich sind ~20–50 W ≈ 175–440 kWh/a Wärme.
- Größter möglicher Hebel: Zirkulation (falls vorhanden). Pro 10 m gedämmter Leitung im Dauerbetrieb ~1,6 kWh/d. Zeitprogramm oder Bedarfstaster spart mehr als alle Speichermaßnahmen zusammen.
- Messvorschlag: Nachts Zirkulation sicher aus, WW-Fühler oben und (falls vorhanden) unten loggen. Mit der Fühler-Mitteltemperatur und V = 379 l neu rechnen. Danach dieselbe Nacht mit Zirkulation an vergleichen.