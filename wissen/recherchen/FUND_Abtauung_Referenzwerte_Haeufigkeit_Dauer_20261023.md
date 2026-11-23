# FUND: Abtauung – Referenzwerte Häufigkeit, Dauer, Energie, Signatur (23.10.2026)

Anlage: Hoval UltraSource B comfort C17 (L/W-Split-Inverter, R410A, Abtauung vermutlich Kreislaufumkehr), Alpenort (~960 m) ~960 m.
Zweck: Referenz für die sekundengenaue Abtau-Messung im Winter 2026/27 (Lüfter-Merker X4, Verdichter, VL/RL).
Hinweis: Hoval-eigene Abtau-Kennwerte sind öffentlich nicht gefunden. Alle Werte unten sind fremde oder allgemeine Referenzen.

## 1. Belegt (kurzes Zitat + URL)

**Kritischer Bereich Temperatur/Feuchte**
- ORNL-Literaturreview: Reifbildung bei „ambient air temperature extremely low (-7 to 5oC) and the relative humidity is relative high (greater than 65%)“. https://info.ornl.gov/sites/publications/Files/Pub117976.pdf
- EnergieSchweiz/BFE „Betriebsoptimierung Heizung: Abtauung Luft-Wasser-Wärmepumpen“ (11/2021): kritisch ist die „Aussentemperatur um den Gefrierpunkt (minus 2 °C bis plus 5 °C)“. https://pubdb.bfe.admin.ch/de/publication/download/9977
- Vocale et al. 2014 (Zusammenfassung Earth Notes): „the frost formation is mainly affected by the relative humidity“. https://www.earth.org.uk/bibliography/vocale2014influence.html

**Häufigkeit**
- BFE-Leitfaden: Zeitgesteuerte Abtauung z. B. nach 1 h Laufzeit, auch „wenn der Verdampfer nicht eingefroren ist“. Bedarfsabtauung passt Intervall und Dauer an. Quelle wie oben (BFE 9977).
- NREL-Feldauswertung (US-Wohnhäuser): „Figure 4 shows the relationship between defrost frequency and weather which does not show a strong correlation.“ https://nrel.gov/docs/fy23osti/83616.pdf
- Forum OpenEnergyMonitor (Praxis, kein Labor): unter schlechtesten Bedingungen werden „ordinarily“ etwa 1 Abtauung/h erwartet. Ein Fall mit „4 mins defrost, run for 30 mins“ bei ~0 °C gilt als doppelt so häufig wie normal. Ursache dort: Gerät lief dauernd auf 100 %. https://community.openenergymonitor.org/t/octopus-cosy-9-heat-pump-rapid-and-frequent-defrost-cycles/29447
- Forum energiesparhaus.at (AT-Nutzer): 12-kW-Monoblock, Raum Wien, Dez–Jan „ca. 900 Abtauvorgänge pro Monat. (29 pro Tag)“, Intervall „ca. 50 Minuten“. Andere Nutzer: S2125-8 „max. 17 Enteisungen in 24 h“, andere Geräte ~3/Tag. https://www.energiesparhaus.at/forum-lwwp-abtauvorgaenge-monat/84777_2

**Dauer**
- Mitsubishi Electric (Puffer-Auslegung): „Typischerweise kann die Dauer der Abtauung zwischen 2 und 9 Minuten betragen.“ Rechenbeispiel mit 5 min und max. 5 K Temperaturabfall im Hydraulikkreis. https://www2.mitsubishi-les.com/media/download/me-pufferspeicher-pdf-web-rz.pdf
- Purdue-Labor (0 °C / 90 % rF, Kreislaufumkehr): Abtaudauern 102–150 s (~1,7–2,5 min), bei späterem Start 2,5–4,0 min. Die Vereisungszeit stieg dabei von 28 auf 64 min (zitiert nach Zhang & Hrnjak 2021). https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=3301&context=iracc
- BFE-Leitfaden: Beispiel für die max. Abtauzeit 25 min (geräteabhängig), Abtropfzeit 3 min. Quelle BFE 9977.

**Energie / COP**
- Vocale 2014: Der Stunden-COP sinkt um bis zu 20 %, „the maximum decrease of SCOP … is less than 13%“. Monats-COP bis −17 % bei rF > 80 % und 0–6 °C. Quelle Earth Notes (oben).
- DOE/BTO 2024 (fasst Vocale zusammen): „Seasonal COP reduction: 1.5% - 12.7%“. https://www.energy.gov/sites/default/files/2024-11/bto-peer-2024-32275-quantifying-and-reducing-defrost-energy-use-woods.pdf
- ORNL: Kreislaufumkehr nutzt 59,4 % der zugeführten Energie zum Schmelzen. Bei ungleichmäßig abgetautem Mehrkreis-Verdampfer („mal-defrost“) sinkt der COP um bis zu 40,4 %. Quelle ORNL (oben).
- Fraunhofer ISE WP-Monitor und WPsmart im Bestand: Die „thermische Abtauenergie bei Prozessumkehr“ wurde tageweise erfasst. In den abrufbaren Textteilen ist aber kein Prozentwert zu finden. https://wp-monitoring.ise.fraunhofer.de/wpqs-im-bestand/download/Berichte/BMWi-03ET1272A-WPsmart_im_Bestand-Schlussbericht.pdf

**Puffer / Mindestvolumen**
- Mitsubishi: Bei luftgekühlten WP immer zwei Rechnungen machen (Taktschutz und Abtauung): „Das größere Volumen muss dann … berücksichtigt werden.“ Die Kälteleistung während der Abtauung wird zur Heizlast addiert. Faustregel „pro kW X Liter“ lehnt das Papier als zu ungenau ab. Quelle Mitsubishi (oben).

## 2. Wahrscheinlich (plausibel, nur Sekundärquellen oder eigene Rechnung)
- Intervall unter +5 °C etwa 30–90 min, Dauer 3–10 min, Saisonverlust 5–15 % (Argile-Blog, ohne Primärquelle). https://www.argile.ai/en/blog/degivrage-de-la-pac-air-eau-impact-sur-la-performance-hivernale
- IDM-Seite (Herstellerblog, ohne Belege): Vereisung zwischen −10 und +7 °C bei rF > ~70 %. Mindestabstand 30–45 min zwischen Abtaustarts. Not-Ende nach ~10 min. Ende bei Registertemperatur +7…+15 °C. „15+ defrost cycles per day above +3 °C“ deutet auf Fühler- oder Füllmengenproblem. Ziel < 5 % der Laufzeit. https://www.idm-energie.at/en/heat-pump-control/defrost-control/
- Bei trockener Kälte (< −10 °C, geringe absolute Feuchte) wenig Reif, also deutlich seltener abtauen. Das folgt physikalisch aus ORNL, IDM und Vocale, eine Feldzahl dazu fehlt.
- Häufigere Abtauung bei hoher Modulation bzw. Volllast: Der Verdampfer wird kälter und vereist schneller (OEM-Forum). Das ist für unseren Logger wichtig, Verdichterdrehzahl mitloggen.
- Eigene Rechnung Wärmeentnahme: Annahme ~5–10 kW Kälteleistung des Wasserkreises während der Abtauung × 3–6 min ≈ 0,25–1,0 kWh. Im 400-l-Puffer ergibt das ΔT ≈ 0,5–2 K (1 kWh ≈ 2,1 K bei 400 l). Kommt die Wärme direkt aus dem FBH-Kreis (~kleineres Volumen), ist der VL/RL-Einbruch deutlich größer. Welche Hydraulik zutrifft, ist zu prüfen.
- Mindestvolumen nach Mitsubishi-Formel V = P·t/(c·ΔT): 10 kW · 300 s / (4,19 kJ/kgK · 5 K) ≈ 145 l. Der Puffer mit ~400 l reicht damit rechnerisch, sofern er hydraulisch im Abtaupfad liegt.

## 3. Nicht gefunden
- Hoval-spezifisch für UltraSource B: Abtau-Intervalle, Dauer, Startkriterium, Lüfterverhalten und Mindestvolumen (öffentlich nicht dokumentiert).
- Belastbare Feldtabelle „Abtauungen/h je Außentemperatur- und Feuchteband“ aus ISE, SPF/OST oder BFE-Feldtest. ISE erfasst die Abtauenergie, veröffentlicht sie aber nicht in den frei lesbaren Textteilen. ScienceDirect und Springer (z. B. Energy & Buildings 2023, S[Nummer]) waren nicht abrufbar.
- Prozentualer Anteil der Abtauenergie an der gemessenen JAZ aus deutschsprachigen Feldtests.

## 4. Referenztabelle (Arbeitswerte, keine Hoval-Norm)
| Außentemp.-Band | rF | erwartete Abtauungen/h | Dauer je Abtauung | Bewertung / Quelle |
|---|---|---|---|---|
| > +7 °C | egal | ~0 | – | keine Reifbildung (IDM, ORNL); jede Abtauung auffällig |
| +3 … +7 °C | > 80 % / Nebel | 0–0,5 | 2–6 min | gelegentlich normal; > 15/Tag auffällig (IDM) |
| −2 … +3 °C | > 80 % | 0,7–1,5 (Intervall 40–90 min) | 2–8 min | Hauptbereich (BFE, Argile, OEM, Forum AT) |
| −2 … +3 °C | < 65 % | 0,2–0,7 | 2–6 min | weniger Reif (ORNL rF-Schwelle) |
| −7 … −2 °C | > 70 % | 0,5–1 | 3–10 min | Dauer steigt wegen kalter Luft (Vermutung) |
| < −7 … −10 °C | trocken | 0–0,3 | 4–10 min | wenig Feuchte; häufig dann auffällig |
| beliebig | beliebig | > 2 (Intervall < 30 min) | – | auffällig (OEM-Fall, IDM-Mindestabstand) |
| beliebig | beliebig | – | > 10–12 min | auffällig: Not-Ende oder unvollständig (IDM, Mitsubishi 2–9 min) |

## 5. Was bringt uns das
- Wir haben einen Rahmen: Unter ~0 °C bei Nebel bzw. hoher Feuchte sind ~1 Abtauung/h und 2–8 min normal. Das gilt nicht als Fehler.
- Auffällig ist nicht die absolute Zahl, sondern ein Widerspruch zum Wetter: häufig bei trockener Kälte, Abtauung über +7 °C, steigender Trend bei gleichem Wetter.
- Der 400-l-Puffer reicht rechnerisch für die Abtauung, wenn er im Abtaupfad liegt. Starker VL-Einbruch an der FBH deutet sonst auf Entnahme direkt aus dem Heizkreis hin.
- Die Verdichterdrehzahl beeinflusst die Häufigkeit. Volllast-Phasen (z. B. WW-Ladung, Kaltstart) gesondert auswerten.

## 6. Auswerte-Kriterien für unseren Logger
**Ereigniserkennung (alle Bedingungen gemeinsam, nicht einzeln, wie esp32.co.uk warnt: Dip oder Spike allein ist kein Beweis)**
- Start: Lüfter-Merker X4 → 0 bei laufendem Verdichter UND VL fällt innerhalb von ≤ 60 s um > 2 K oder VL < RL (Kreislaufumkehr entzieht dem Wasser Wärme).
- Ende: Lüfter wieder an UND VL steigt wieder. Abtaudauer = Lüfter-aus bis Lüfter-an. Getrennt davon die Erholzeit bis VL-Soll − 1 K erfassen (Erholzeit ≠ Abtaudauer).
- Abtropfpause (Verdichter aus, Lüfter aus, ~1–3 min) als eigene Phase loggen.
- Pro Ereignis speichern: Start, Dauer, Erholzeit, ΔVL min, ΔRL min, Puffer oben/unten vorher/nachher, Außentemp., rF (Loxone-Wetter oder Außenfühler), Verdichterdrehzahl in den 30 min davor, Abstand zur vorigen Abtauung.

**Kennzahlen pro Tag**
- Abtauungen/h Verdichterlaufzeit je Außentemp.-Band (Tabelle Abschnitt 4).
- Anteil Abtauzeit an der Verdichterlaufzeit: Ziel < 5 % (IDM, unbelegt), > 10 % prüfen.
- Entnommene Wärme ≈ 400 l × 1,163 Wh/(l·K) × ΔT_Puffer. Erwartung 0,25–1 kWh je Abtauung.

**Auffällig, gezielt prüfen**
1. Intervall < 30 min oder > 2 Abtauungen/h über mehrere Stunden.
2. Abtauungen bei > +7 °C oder bei trockener Kälte (< −7 °C, rF < 60 %) im gleichen Takt wie bei Nebel. Verdacht auf Fühler (Verdampfer/Außen) oder ein Zeitsteuer-Fallback.
3. Dauer > 10 min oder regelmäßig am selben Maximalwert (Not-Ende, also Abtauung unvollständig). Danach kürzere Intervalle = Resteis baut sich auf. Sichtkontrolle: Eis unten am Register, Kondensatwanne/Ablauf.
4. Zunahme der Abtauungen/h bei gleichem Wetterband über Wochen (Verschmutzung, Füllmenge, Fühlerdrift).
5. Puffer fällt pro Abtauung > 3 K oder VL an der FBH bricht stark ein. Prüfen, ob die Abtauung aus dem FBH-Kreis statt aus dem Puffer zieht.
6. Heizstab-Freigabe zeitlich an Abtauungen gekoppelt: deutet auf zu wenig verfügbare Wärme im Abtaupfad hin.
7. Nach Strom-Aus/Ein gehäufte Abtauungen nicht überbewerten (Kaltstart bei Volllast, siehe OEM-Fall).

**Vorbehalt:** Die Referenzwerte stammen aus anderen Geräten, Labor und Foren. Nach dem ersten Winter durch eigene Bandstatistik ersetzen.


## Pruefvermerk Loop 23.10.2026 13:3x (Slot 13, angehaengt)
- **BFE 9977 ✔** (PDF lokal ausgelesen): "Aussentemperatur um den Gefrierpunkt (minus 2 °C bis plus 5 °C)", max. Abtauzeit "z. B. 25 Minuten", Abtropfzeit "z. B. 3 Minuten", Zeitabtauung "nach 1 Stunde Laufzeit, fix 10 Minuten ... auch wenn der Verdampfer nicht eingefroren ist" – alle wörtlich da.
- **OpenEnergyMonitor ✔**: "ordinarily expect ... a defrost cycle around once per hour" (Nutzer jakeymd1, Praxis) und "4 mins defrost, run for 30 mins, repeat" (Thread-Ersteller) – stimmt.
- **IDM-Blog ✔ mit Korrektur**: alle sechs Werte stehen dort; die 10 min sind nur ein *Beispiel* für die Zeitgrenze ("e.g., 10 minutes"), kein festes Not-Ende.
- Nicht prüfbar (Abruf scheiterte): Mitsubishi (Verbindung verweigert), NREL (DNS), Purdue (403).
- **Korrektur 1 – Max-Dauer:** Für unsere Anlage gilt laut Forum 33-283 = 15 min max. Abtauzeit (STAND 14./15.10., Nutzerangabe), iDM-Standard ebenfalls 15 min. Auffälligkeitskriterium "Dauer > 10–12 min" daher ersetzen durch **"Dauer ≥ 14 min bzw. wiederholt am selben Maximalwert = Zeitende 33-283"**.
- **Korrektur 2 – Puffervolumen:** Abschnitt 2/5/6 rechnet mit "400-l-Puffer". Laut Orchestrator 13:03 (Hoval-Katalog S. 38) ist für C17 EnerVal 300 vorgesehen, und der 400er ist sehr wahrscheinlich der WW-Speicher (CombiVal ESR 400, Messung 10:15). Mit ~300 l: 1 kWh ≈ 2,9 K statt 2,1 K; Mitsubishi-Minimum 145 l bleibt erfüllt. Wahrscheinlich, bis Typenschild-Foto.
- Was bringt uns das: Der Abtau-Auswerter bekommt die richtige Grenze (15 min statt 10) und die richtige Puffer-Umrechnung – sonst würden normale lange Abtauungen als Fehler markiert und die Abtauenergie um ~30 % unterschätzt.