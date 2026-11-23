# FUND F66 – Loxone Heatmixer2 Parameterzuordnung (01.11.2026)

Erstellt: Orchestrator-Lauf 01.11.2026 21:54 (Recherche-Subagent, Gegenprobe Claude). Nur gelesen, nichts an Loxone/Anlage geändert.

## Frage
Heatmixer2 „Vorlautemperatur HC1“ (Projektdatei `[lokaler Pfad] Config\Projects\Fam der Betreiber UMBAU.Loxone`, Z. 13350): Transconductance 0.3, Translate leer, Max 40, Gain 1, Treshold 35, PrevInc 2, BufferInc 5, UseHVAc 1, Def 0.9 am Eingang „Outer“. Welche Doku-Parameter stehen dahinter, und warum liefert AQf nur ~16–17 °C bei 4–6 °C außen?

## Quellen
- https://www.loxone.com/enen/?p=1272 – abgerufen (offizielle Doku „Flow Temperature Calculator“ = Vorlauftemperaturregler)
- https://www.loxone.com/enus/?p=273924 – abgerufen (gleicher Parametersatz, Gain-Rechenbeispiel)
- https://www.loxone.com/enen/kb/intelligent-temperature-controller/ – abgerufen (ältere Version)
- https://www.loxone.com/enen/kb/heating-curve/ – abgerufen (separater Baustein Heizkurve)
- https://www.loxone.com/dede/kb/vorlauftemperaturregler/ – nicht abrufbar (403); https://www.loxone.com/dede/kb/heizkurve/ – nicht abrufbar
- loxforum.com („Große Unbekannte Heizkurve entschlüsselt“) – gesperrt (403)

## Belegt (Doku https://www.loxone.com/enen/?p=1272)
- Eingang ϑo = Außentemperatur; unverbunden → Systemvariable Außentemperatur, sonst 0 °C [belegt].
- Str wirkt nicht, wenn alle Raumregler eines HVAC-Controllers verwendet werden; dann gilt dessen Schwelle [belegt].
- **Ohne Raumbedarf ist AQf = Min (Heizen)** bzw. Max (Kühlen); Stopp-Eingang → AQf = Min [belegt].
- Je Raum wird ein Vorlauf berechnet, AQf = höchster (Heizen) / niedrigster (Kühlen) [belegt].
- Doku-Beispiel S 0,5, N 0, 0 °C außen: Raum-Soll 20 → VL 30,9; 22 → 33,8 °C [belegt]. Explizite Formel nicht dokumentiert.

## Wahrscheinlich
- XML-Zuordnung (Defaults decken sich): Transconductance = S, Translate = N, Treshold = Str, PrevInc = I, BufferInc = B, Gain = G, UseHVAc = Bezug Klimacontroller UG [wahrscheinlich].
- **Wirksame Steilheit 0,3, nicht 0,9**; „Outer“ ist der Außentemperatur-Eingang, Def 0.9 an einem verbundenen Eingang wirkungslos [wahrscheinlich].
- Mit S 0,3 ergäbe die Kurve bei 6 °C außen ~26–27 °C (Raum 21–22 °C), mit S 0,9 ~37–39 °C (nahe Max 40) [Vermutung, Formel nachgebildet: Viessmann-Typ VL = Tr + N − S·d·(1,4347 + 0,021·d + 0,0002479·d²), d = Ta − Tr, trifft Doku-Beispiele auf 0,2 K].
- 16–17 °C passen zu **keiner** Kurvenvariante → AQf steht am **Min-Eingang** [wahrscheinlich, siehe Gegenprobe].

## Nicht gefunden
- Offizielle Formel der Loxone-Heizkurve; offizielle XML-Attribut-Zuordnung; ob Def an verbundenem Eingang je wirkt; Kühlkurven-Formel.

## Gegenprobe Claude (01.11.2026 ~22:00, nur gelesen)
- Projektdatei Z. 13358–13360: Eingang **Min ist verbunden** mit `<UUID>…` = Ausgang AQ des Bausteins **„Taupunkt + Reserve“** (Add4, Z. 13674): höchster Raum-Taupunkt UG (6 DewPoint-Bausteine → Minmax) + Konstante „Taupunkt-Reserve“ (Z. 99, AnalogConstant = 2) [sicher als Dateiinhalt]. Gleicher Min-Eingang bei HC2 (Z. 13388) [sicher].
- Eingang Outer verbunden (Z. 13351–13353), Def 0.9 nur Vorgabe [sicher als Dateiinhalt].
- Live Loxone-MCP: „HK1 Vorlauf soll (Loxone)“ = **17,2 °C** (21:00:45 UTC), gleichzeitig Reg 1490 = 0, Reg 1477 = 4,2 °C [sicher, gelesen].
- Deutung: Ohne Freigabe/Raumbedarf gibt der Heatmixer Min = max. Raum-Taupunkt + 2 K aus (Raumtaupunkt ~15 °C ist bei 22 °C und ~60 % rF plausibel) → die „16 °C bei 6 °C außen“ sind sehr wahrscheinlich der **Taupunkt-Min**, nicht die Heizkurve [wahrscheinlich; Wert des Bausteins „Taupunkt + Reserve“ selbst nicht live gelesen].
- Nebenbefund: Raumregler Badezimmer `actualOutdoorTemp` = −1000 (= kein Außenwert am Raumregler), `averageOutdoorTemp` −1,7 [sicher, gelesen; Bedeutung offen].

## Was bringt uns das
- Die niedrigen 1490-Werte kommen nicht aus einer „falschen Steilheit“ allein: ohne Wärmebedarf liefert der Baustein den Taupunktschutz (Min) – der wirkt im Heizbetrieb als Untergrenze, unschädlich.
- Wenn geheizt wird, rechnet die Kurve mit S 0,3 (nicht 0,9 wie in NDOC/Projektanweisung). Ob 0,3 gewollt ist, entscheidet der Betreiber; 0,9 ergäbe bei 6 °C außen ~37–39 °C – für FBH vermutlich zu hoch.
- MD-17 muss 1490 nur in Laufphasen (Freigabe, Qp) gegen die Kurve fitten; Werte nahe Taupunkt+2 K als „Min“ getrennt zählen.
- Doku: https://www.loxone.com/dede/kb/vorlauftemperaturregler/ (englisch abrufbar https://www.loxone.com/enen/?p=1272)