# FUND F69: Glattrohr-Register CombiVal ESR (400) – Fläche, Leistung, nötiger Vorlauf-Überhub (02.11.2026)

## Frage
Welche Fläche und Leistung hat das Glattrohr-Register des Hoval CombiVal ESR (400) laut Hoval? Welcher Überhub (Vorlauf minus WW) ist bei 2,5–3 kW Ladeleistung für 50 / 55 / 57 °C nötig? Erklärt das die Ladeüberhöhung (Ladesoll = WW-Soll +4 K) und ~62 °C Vorlauf am Ladeende?

Quellen:
- Q1: Hoval Katalog „Speicher Trinkwassererwärmung 2026/27“ (DE), https://cdn.hoval.com/speicher_trinkwassererwarmung_katalog_2026_de_exa_hybris_original.pdf – am 02.11.2026 per curl geladen, pdftotext; Diagramme S. 13 (PDF-Seite 36) als Bild gerendert und abgelesen.
- Q2: Messung [lokaler Pfad] (1-min-Werte).
- Lokal: [lokaler Pfad] und ...\FUND_Speicher_Bereitschaftsverlust_EnerVal_CombiVal_20261022.md (Typ/Rolle CombiVal = WW-Speicher, 3,8 m², Art.-Nr. 7015 967).
- Kein lokal per pdftotext erzeugter Hoval-Katalog unter [lokaler Pfad] gefunden (Suche *.txt nach „CombiVal ESR“: nur Orchestrator-Logs).

## Belegt (Q1, Katalog 2026/27)
- [sicher] Register: „Grosses Glattrohrregister emailliert, fest eingebaut“.
- [sicher] Technische Daten ESR (400): Heizfläche 3,8 m², Heizungswasser 34 l, Durchflusswiderstand z = 6 (mbar = (m³/h)² · z), max. 110 °C, 8/13 bar (SVGW). Volumen 379 l.
  -> Druckverlust Register bei 1,1 m³/h ≈ 7 mbar, bei 2,2 m³/h ≈ 30 mbar: vernachlässigbar.
- [sicher] NL-Zahl ESR (400) bei WW 45 °C (DIN 4708, „Comfort“): 6 bei 60 °C Vorlauf, 14 bei 70 °C, 18 bei 80 °C. „Standard“ (TU Dresden): 6 / 17 / 22.
- [sicher] Keine Tabelle in kW für 80/60 oder 55/45; Hoval gibt die Dauerleistung nur als Diagramm über dem Volumenstrom der Ladepumpe (1–3 m³/h), Kaltwasser 10 °C.

### Dauerleistung ESR (400) aus Diagramm S. 13 abgelesen [wahrscheinlich, Ablesegenauigkeit ±1 kW]
| WW | Heizungsvorlauf | 1,0 m³/h (16,7 l/min) | 1,5 m³/h (25 l/min) | 2,8 m³/h |
|---|---|---|---|---|
| 45 °C | 55 °C | 17,8 kW | 21,8 kW | 29 kW |
| 45 °C | 60 °C | 23,5 kW | 29 kW | 38,5 kW |
| 45 °C | 70 °C | 38 kW | 46 kW | 61 kW |
| 45 °C | 80 °C | 48 kW | 59 kW | 80,5 kW |
| 55 °C | 60 °C | 16,4 kW | 20,0 kW | 26,7 kW |
| 60 °C | 70 °C | 29,5 kW | 35 kW | 47,5 kW |
(Diagramme für 55 °C WW nur mit Kurve 60 °C Vorlauf; 80/60- oder 55/45-Tabellenwerte gibt es im Katalog nicht.)

## Wahrscheinlich
- [wahrscheinlich] Aus den Hoval-Dauerleistungen (Gegenstrom-Ansatz Kaltwasser 10 °C -> WW) zurückgerechnet: kA ≈ 1,0–1,2 kW/K, also k ≈ 260–320 W/m²K bei 3,8 m². Beispiel 55/45 bei 1,0 m³/h: 17,8 kW, RL 39,7 °C, ΔT_log 18,1 K -> kA 0,98 kW/K.
- [wahrscheinlich] Aus der eigenen Messung (Ladungsende, siehe unten, Bezug = Fühler WW oben 1500) ergibt sich ein effektives kA ≈ 2,0–2,5 kW/K. Das ist eine Obergrenze: Ist das Wasser am Register (unten) kälter als oben am Fühler, ist das echte kA kleiner und die echte ΔT_log größer.
- [Vermutung] Für die Rechnung unten daher kA 1,0 (Hoval-Datenblatt) bis 2,0 kW/K (Messung) als Bandbreite. Kein Literatur-k für Glattrohr in Speicher mit freier Konvektion übernommen; der Wert ist aus Hoval-Diagramm bzw. Messung abgeleitet, nicht aus Fremdquelle.

## Nicht gefunden
- Datenblatt-Tabelle mit kW bzw. l/h bei 80/60 oder 55/45 °C für ESR (400) (nur Diagramme).
- Katalogausgabe Baujahr 2020/2021 (Werte von 2026/27 verwendet; Register 3,8 m² und Art.-Nr. 7015 967 sehr wahrscheinlich unverändert).
- Herstellerangabe zum kA bei reiner Speicherladung ohne Zapfung (Dauerleistung gilt bei fließendem Kaltwasser = erzwungene Strömung am Register, besser als reine Ladung).
- Web-Suche hoval.at/.de/.ch nicht mehr nötig: der Hoval-Originalkatalog (Q1) liefert alle verfügbaren Werte direkt.

## Rechnung
Ansatz [sicher als Methode]: Speicherwasser am Register gleichmäßig auf T_WW (Ladungsende). Q = ṁ·c·(VL − RL), RL = T_WW + (VL − T_WW)·e^(−kA/ṁc)
-> nötiger Überhub VL − T_WW = Q / (ṁc · (1 − e^(−kA/ṁc))). ΔT_log = (VL − RL) / ln((VL − T_WW)/(RL − T_WW)).
Der Überhub hängt NICHT von der WW-Temperatur ab (nur von Q, Durchfluss, kA); 50/55/57 °C verschieben nur den Vorlauf.

| Ladeleistung | Durchfluss | Spreizung VL−RL | Überhub VL−WW bei kA 1,0 / 1,5 / 2,0 kW/K |
|---|---|---|---|
| 2,5 kW | 18 l/min | 2,0 K | 3,6 / 2,9 / 2,5 K |
| 2,5 kW | 28 l/min | 1,3 K | 3,2 / 2,4 / 2,0 K |
| 3 kW | 18 l/min | 2,4 K | 4,4 / 3,4 / 3,0 K |
| 3 kW | 28 l/min | 1,5 K | 3,8 / 2,9 / 2,4 K |
| 6,5 kW | 18 l/min | 5,2 K | 9,4 / 7,4 / 6,5 K |
| 9 kW | 18 l/min | 7,2 K | 13,1 / 10,3 / 9,0 K |
| 9 kW | 37 l/min | 3,5 K | 10,9 / 7,9 / 6,5 K |
(ΔT_log entspricht etwa Überhub minus halbe Spreizung: bei 3 kW ≈ 1,5–3 K.)

Nötiger Vorlauf bei 3 kW, 18–28 l/min [wahrscheinlich]:
| WW | kA 2,0 (Messung) | kA 1,0 (Hoval) |
|---|---|---|
| 50 °C | 52,5–53,0 °C | 53,8–54,4 °C |
| 55 °C | 57,5–58,0 °C | 58,8–59,4 °C |
| 57 °C | 59,5–60,0 °C | 60,8–61,4 °C |
Bei der real gefahrenen Ladeleistung 6,5–9 kW (siehe Messung): WW + 6,5…13 K -> 57 °C WW bräuchte 63,5–70 °C Vorlauf, also über WP-Max 62 °C.

## Abgleich Messung (Q2, letzte Minute der Ladung) [sicher = Messwerte; Auflösung VL/RL 0,5 K]
| Zeitpunkt | WW oben 1500 | WW-Soll 1499 | Ladesoll 1521 | VL 18725 | RL 1535 | Flow 31708 | Q = ṁ·c·ΔT | pth 25612 | Pel 25611 | VL−WW |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-07 13:15 | 55,4 | 57,0 | 61,0 | 62,0 | 58,5 | 37,4 l/min | 9,1 kW | 9 kW | 2,88 kW | 6,6 K |
| 2026-10-24 06:05 | 49,6 | 50,0 | 54,0 | 56,0 | 51,0 | 18,7 l/min | 6,5 kW | 7 kW | 2,46 kW | 6,4 K |
| 2026-10-04 01:45 | 49,7 | 50,0 | 54,0 | 56,0 | 50,0 | 18,7 l/min | 7,8 kW | 8 kW | 2,45 kW | 6,3 K |
Entwicklung 13:01–13:15 am 07.10.: WW 52,8 -> 55,4 °C, VL 58,5 -> 62,0 °C, Überhub konstant ~5,7–6,6 K, Pel steigt 2,64 -> 2,88 kW bei Modulation 33 %.

Ergebnis:
- [sicher] Die Ladeleistung am Ladeende ist 6,5–9 kW (pth und ṁ·c·ΔT stimmen überein), NICHT 2,5–3 kW. Grund: Mindestmodulation des Verdichters (~33 %) – passt zur bekannten Überdimensionierung.
- [wahrscheinlich] Rückrechnung mit Bezug WW oben: kA_eff ≈ 2,0 (07.10./24.10.) bis ~2,5 kW/K (04.10.). Damit sagt das Modell für alle drei Fälle 6,5 K Überhub vorher; gemessen 6,3–6,6 K. Konsistent.
- [wahrscheinlich] Der Überhub von ~6,5 K am Ladeende ist also physikalisch durch Register 3,8 m² + Mindestleistung 6,5–9 kW erklärt, nicht durch eine Fehleinstellung.
- [sicher] Der Vorlauf überschreitet das Ladesoll (WW-Soll +4 K) am Ende um 1–2 K (62 statt 61, 56 statt 54). Die +4 K Ladeüberhöhung reichen bei dieser Leistung NICHT; die WP fährt einfach höher.
- [wahrscheinlich] 07.10.: Ladung endet bei WW 55,4 °C obwohl Soll 57 °C, genau als VL 62,0 °C = WP-Maximum erreicht. Für 57 °C bräuchte es bei 9 kW/37 l/min ~63,5 °C (kA 2,0) -> 57 °C ist mit dieser Leistung nicht erreichbar; die Ladung wird vermutlich über die VL-Grenze beendet (Abbruchgrund nicht direkt geloggt).
- [wahrscheinlich] Für die Frage „~62 °C bei 55 °C WW“: passt genau (55,4 + 6,6). Bei 3 kW wären nur ~58–59 °C nötig.
- [Vermutung] Zwei Durchflussstufen: 37,4 l/min (07.10., Modulation 33, Smart-Grid-Ladung 57 °C) und 18,7 l/min (Nachtladungen 50 °C). Der höhere Durchfluss senkt den Überhub bei 9 kW nur um ~2,5 K gegenüber 18 l/min.

## Antwort auf F69 (kurz)
- [sicher] Register ESR (400): 3,8 m² Glattrohr, 34 l, z = 6; NL (45 °C WW) 6 / 14 / 18 bei 60 / 70 / 80 °C Vorlauf; Dauerleistung nur als Diagramm (z. B. 17,8 kW bei 55 °C VL / 45 °C WW / 1 m³/h; 16,4 kW bei 60 °C VL / 55 °C WW / 1 m³/h).
- [wahrscheinlich] Bei 2,5–3 kW wären nur 2–4,5 K Überhub nötig (ΔT_log ≈ 1,5–3 K); die +4 K Ladeüberhöhung wäre dann passend.
- [wahrscheinlich] Real lädt die WP aber mit 6,5–9 kW (Mindestmodulation). Dafür braucht das 3,8-m²-Register ~6,5 K Überhub (gemessen 6,3–6,6 K). Das erklärt 62 °C VL bei ~55 °C WW und den Abbruch der 57-°C-Ladung an der 62-°C-Grenze.

## Offen
- Abbruchgrund der Ladung 07.10. 13:15 (VL-Max 62 °C? HD-Grenze? WW-Hysterese?) im Volllogger / Fehlerspeicher prüfen.
- Fühlerhöhe des WW-Fühlers 1500 im Fühlerkanal (Bezugstemperatur der kA-Rückrechnung). Mit einem Fühler unten am Register wäre kA sauber bestimmbar.
- Warum zwei Durchflussstufen (18,7 vs. 37,4 l/min)? Ladepumpe/WEZ-Pumpenstufe je Betriebsart prüfen (nur lesen).
- Option zur Diskussion (nur mit des Betreibers Freigabe, nichts verstellt): 57 °C Smart-Grid-Soll senken auf ~55 °C oder Ladung am Ende mit geringerer Leistung fahren; Heizstab-Nachheizung für >55 °C. Größere Registerfläche ist baulich nicht änderbar.
- Katalog 2020/21 zum Abgleich der Diagrammwerte (Baujahr) nicht gefunden.