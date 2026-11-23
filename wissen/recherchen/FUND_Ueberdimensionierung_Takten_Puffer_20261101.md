# FUND F63 Überdimensionierung / Takten / Puffer – 01.11.2026
Claude-Subagent, Lauf 01.11.2026 17:02. Nur öffentliche Seiten (WebSearch/WebFetch). Nicht wiederholt: Loxone IRR/Takten (FUND_Loxone_IRR_FBH_Takten_20261101.md) und Zuschalt-/Sperrzeiten (FUND_Zuschaltzeiten_Sperrzeiten_Takten_20261014.md).

## Frage
Was hilft bei einer überdimensionierten Inverter-L/W-WP (Mindestleistung 7–8 kW > Heizlast 1–2,5 kW bei 3–10 °C) mit FBH nachweislich gegen Takten bzw. verbessert die Effizienz? (1) Herstellervorgaben iDM/Hoval zu Puffer, Mindestvolumen, Volumenstrom; (2) Literatur: wie stark senkt Takten COP/JAZ; (3) Praxis: Kreise offen, Hysterese, größerer Puffer, Bivalenz.

## Ergebnis belegt
### (1) Hersteller / Planungsregeln
- iDM AERO SLM 3-11/6-17 Planungsunterlage (Händler-PDF): für ungeregelte Direktkreise im Kühlfall mind. 80 l Heizwasser (Zonen offen o. ä.) und mind. 1,01 m³/h Volumenstrom (offene Zonen oder Überströmventil); Mindestwärmeabnahme 70 % der kleinsten Kühlleistung. Nennvolumenstrom 6-17 bei A7/W35: 2,19 m³/h. Eine Puffer-l/kW-Vorgabe für Heizen stand im lesbaren Text nicht; Hydraulikschemen S. 44–49 nur als Grafik. [1] https://siblik.com/fileadmin/mam/medias/docus/115/IDM191871_AERO%20SLM%203-11_6-17.pdf
- Hoval UltraSource B comfort C/cf Technische Info: comfort C (17) Nenn-Heizwassermenge 2,2 m³/h (ΔT 5 K, A7W35), max. 3,7 m³/h; Zubehör Differenzdruck-Überströmventil DN 20 (0,05–0,5 bar). **Kein** Mindest-Puffervolumen, kein Mindestanlageninhalt, keine Reihen/Parallel-Vorgabe im Text. [2] https://cdn.hoval.com/ultrasource-b-cf-cp_de_hybris_original.pdf
- BWP Leitfaden Hydraulik (07/2016): Puffer zur Laufzeitoptimierung 20–25 l/kW **maximaler** WP-Heizleistung; für Sperrzeitüberbrückung 30–40 l/kW. Ohne Puffer: 3–5 l/kW umlaufendes Wasser je nach Mindestlaufzeit, bei L/W zusätzlich Herstellerangabe Abtauenergie beachten. Spreizung WP-Kreis 3–5 K. [3] https://www.diekaelte.de/sites/default/files/ulmer/file_725238.pdf
- Forum-Angabe Hoval-Support (Nutzerangabe, nicht Hersteller-Dok.): bei sehr kleinem Puffer Mindestdurchfluss ~840 l/h verlangt. [4] https://www.energiesparhaus.at/forum-hoval-ultrasource-lwp-allgemeiner-austausch-und-anlage-optimieren/56645_2

### (2) Literatur / Feldtests: Wie viel kostet Takten?
- Uhlmann & Bertsch (NTB Buchs), Int. J. Refrigeration 35 (2012) 2138–2149, Labor + Feld: Luft-WP verlieren durch kurzes Takten nur **ca. 1–2 %** Leistungszahl; EN-14511-Messwerte bilden Teillast realistisch ab. [5] https://iifiir.org/en/fridoc/theoretical-and-experimental-investigation-of-startup-and-shutdown-135447
- Dongellini & Morini, Energy Conv. Mgmt 196 (2019) 966–978, Simulation reversible L/W-WP: Taktverluste merklich nur bei On/Off-Geräten (SPF **bis −12 %**); Inverter vermeiden Takten über große Teile der Saison, Verlust gering. [6] https://cris.unibo.it/handle/11585/699402
- Fraunhofer ISE WP-QS Schlussbericht (77 Anlagen): Starts/Jahr 550–15.800, **90 % < 5.500**, ~1/3 ≤ 2.000; auch Anlagen mit > 2× Heizlast bei −7 °C blieben < 4.000 Starts. Ursachen vieler Kurzläufe: Regelung auf VL, kleine Hysterese, schlechte Modulationsnutzung, hydraulische Weiche, kleine Parallelspeicher, schnelle Kreise. Parallelspeicher: VL-Differenz WP→Heizkreis meist < 2 K (Einzelfälle bis 5 K); Reihenspeicher gleiche Größenordnung. Kein Zusammenhang Starts↔JAZ ausgewiesen; Effizienz korreliert vor allem mit Heizkreistemperatur. [7] https://www.ise.fraunhofer.de/content/dam/ise/de/documents/projekte/WP-QS_Schlussbericht.pdf
- Fraunhofer ISE WPsmart im Bestand Schlussbericht: von allen Einflussgrößen hebt sich nur die Heizkreistemperatur deutlich ab; Mindestlauf-/Pausenzeiten verhindern Kurzsignal-Takten. [8] https://wp-monitoring.ise.fraunhofer.de/wpqs-im-bestand/download/Berichte/BMWi-03ET1272A-WPsmart_im_Bestand-Schlussbericht.pdf
- Piechurski et al., E3S Web Conf. 44 (2018): Normwert Cd = 0,9 (EN 14825) für L/W oft unzutreffend; Feldmodell vorgeschlagen, Zahlen nur im Volltext. [9] https://www.e3s-conferences.org/10.1051/e3sconf/20184400139
- Sekundär (42watt, zitiert EA Technology 2012): ältere Sole-WP bei 1,6 min Laufzeit COP 2,87→2,44 (~−15 %); Effizienz sinkt erst unter ~6 min Laufzeit. Primärquelle nicht gelesen. [10] https://42watt.de/magazin/taktung-warmepumpe

### (3) Praxis / Foren (Nutzerangaben, keine Messreihen)
- Hoval UltraSource-Nutzer: Stellantriebe teilweise ausgebaut für Mindestdurchfluss → längere Läufe, Estrich wärmer, COP etwas höher, aber **Zyklen nicht weniger, Verbrauch eher höher**. Andere: 10–12 Takte/Tag, Abtauungen zählen als Starts; Empfehlung Einschaltdifferenz auf 4 K. 800-l-Hoval-Puffer-Besitzer glaubt nicht an Verbesserung durch größeren Puffer. [4] (URL oben)
- Hoval Belaria 15 überdimensioniert, Parallelpuffer: Hoval-Support begrenzte Leistung (u. a. „minimale Inverter Leistung“ verstellt), JAZ 3,6 vs. SCOP 5,6; Entkopplung Puffer vorgeschlagen, Wirkung nicht belegt. [12] https://www.energiesparhaus.at/forum-ueberdimensionierte-luft-wasser-wp-zuegeln/80465_2
- Benchmark-Thread modulierende WP: Startzahlen 850–6.000/Jahr; Fall mit Puffer ~80 Starts/Tag, nach Pufferentfernung + Hydraulikkorrektur deutlich weniger. Abtauungen zählen mit (iDM Aero 2–3 Starts je Abtauung). [13] https://www.energiesparhaus.at/forum-benchmark-takte-von-modulierenden-waermepumpen/54272_4
- iDM SLM 6-17 + 800/1000-l-Puffer-Frage: Mehrheit gegen großen Puffer (höhere VL, je K ~2,5 % Strom, Herstellerfaustregel); Heizlastberechnung zuerst. [14] https://www.energiesparhaus.at/forum-waermepumpen-puffer-dimensionierung/71744
- Nibe S2125: gleiche Mindestleistung 8/12/16er → Überdimensionierung ändert Taktrate bei mildem Wetter nicht; Empfehlung FBH direkt, höchstens Reihenpuffer im Rücklauf, Kombipuffer verschlechtern; ~800 Takte/Jahr nach Optimierung. [15] https://www.energiesparhaus.at/forum-nibe-s2125-16-parallelpuffer-zur-vermeidung-von-taktungen/82665_2

## Wahrscheinlich
- Bei Inverter-L/W kostet Takten im Bereich 30-min-Läufe nur ~1–2 % (Heizanteil); Effizienzhebel Nr. 1 ist die Vorlauftemperatur, nicht die Startzahl [5][6][7][8].
- Größere Puffer verlängern Läufe/Pausen, senken aber Starts nur proportional und erhöhen tendenziell VL und Mischverluste; Wirkung auf JAZ netto ≈ 0 bis negativ [7][14][15].
- Offene Kreise erhöhen Masse und Laufzeit, senken Starts in der Praxis nicht sicher, können Verbrauch erhöhen (Überheizen) [4].

## Nicht gefunden / nicht erreichbar
- Keine Hoval- oder iDM-Vorgabe „Puffer x l/kW“ für UltraSource B / AERO SLM im lesbaren Text [1][2]; iDM-Hydraulikschemen S. 44–49 nur Grafik. Manualslib-Fassung ebenfalls ohne Werte: https://www.manualslib.de/manual/1242658/Idm-Aero-Slm-3-11.html
- Fraunhofer WP-Effizienz Kurzfassung: nicht erreichbar (robots_disallowed) http://wp-effizienz.ise.fraunhofer.de/download/wp_effizienz_endbericht_kurzfassung.pdf
- Fraunhofer WP-QS Kap. 6.3/6.4 (Schalthäufigkeit, Speicher, S. 98 ff.) im abrufbaren Text nicht enthalten.
- OST/WPZ Buchs Feldmessung 2020: keine Taktzahlen/Puffer-Ergebnisse https://www.ost.ch/fileadmin/dateiliste/3_forschung_dienstleistung/institute/ies/projekte/projekte_tes/publikationen/paper_feldmessung_waermepumpen_final.pdf
- Volltexte Dongellini/Morini, Bagarella (unipd), Piechurski: Paywall bzw. keine Datei → nur Abstracts.
- photovoltaikforum.com, diy-wärmepumpe: in der Suche keine passenden Treffer; nicht gezielt abgerufen.

## Abgleich mit unserer Anlage (EnerVal 282 l, Mindestleistung 7–8 kW)
| Prüfpunkt | Unsere Anlage | Referenz | Bewertung | Sicherheit |
|---|---|---|---|---|
| Puffer l/kW (BWP 20–25 l/kW max. Leistung) | 282 l / 14,8 kW = 19 l/kW; bezogen auf 7,5 kW Mindestleistung 38 l/kW | 296–370 l (max.) bzw. 150–190 l (min.) [3] | knapp unter BWP-Regel auf Maximalleistung, für Mindestleistung reichlich | sicher (Rechnung) |
| Starts/Jahr | ~3.000 | 90 % < 5.500; > 2× überdimensioniert meist < 4.000 [7] | typisch, unauffällig | sicher |
| Laufzeit je Start | ~30 min | Verluste erst < ~6 min deutlich [10]; L/W 1–2 % [5] | Taktverlust heute vermutlich ≤ 1–2 % des Heizstroms | wahrscheinlich |
| Speicherinhalt Hub −1,5/+3 K = 4,5 K | 282 l × 1,163 Wh/(l·K) × 4,5 K ≈ 1,5 kWh | – | 1,5 kWh / 1–2,5 kW Last ≈ 36–90 min Pause → passt zu gemessenen 20–70 min | wahrscheinlich |
| Laufzeit aus Puffer allein | 1,5 kWh / (7,5 − 2) kW ≈ 16 min | gemessen ~30 min | Estrich/FBH-Wasser nehmen mit auf, oder reale Leistung < 7,5 kW | Vermutung |
| VL-Abstand WP→FBH | 6–7 K (davon +3 K aus 07-001) | Parallelspeicher meist < 2 K [7] | 4–5 K mehr als üblich; bei ~2,5 %/K ≈ 10 % Heizstrom | wahrscheinlich (Faustregel, nicht gemessen) |
| Mindestdurchfluss | zu prüfen (HoxPi) | iDM 1,01 m³/h Kühlfall [1]; Hoval-Forum ~0,84 m³/h [4]; Nenn 2,2 m³/h [2] | bei zugefahrenen Stellantrieben kritisch | offen |
- Heizen ist nur ~30 % des WP-Stroms (WW ~70 %) → jede Taktverbesserung wirkt auf die Gesamt-JAZ höchstens mit ~0,3–0,6 %.

## Vorschläge (ohne Umsetzung)
1. **VL-Abstand WP→FBH senken** (07-001 Überhöhung prüfen, z. B. +3 → +1 K; Rückweg 3 K; nur mit Freigabe, Rücklesen). Erwartung: WP-VL −2 K → ~5 % weniger Heizstrom; Risiko: FBH-Soll bei parallelem Puffer nicht mehr erreicht. Sicherheit: wahrscheinlich (Faustregel 2,5 %/K, Fraunhofer: Temperatur dominiert [7][8]).
2. **Keinen größeren Puffer nachrüsten.** Doppeltes Volumen halbiert Starts (~1.500/a), spart ≤ 1 % Heizstrom, kostet Platz/Wärmeverlust und eher höhere VL. Sicherheit: wahrscheinlich [5][6][14][15].
3. **Stellantriebe nicht pauschal offen lassen.** Nur sicherstellen, dass ein Referenzkreis offen bleibt und der Durchfluss ≥ ~0,8–1,0 m³/h bleibt (HoxPi-Volumenstrom bei Verdichterlauf lesen). Erwartung: Schutz Abtauung/Hochdruck, kaum Effizienzgewinn. Sicherheit: wahrscheinlich [1][4].
4. **Hysterese nicht weiter öffnen.** Stopp +3 → +4 K brächte ~−20 % Starts, aber höhere mittlere VL → netto ≈ 0. Sicherheit: Vermutung.
5. **Heizfenster in die warmen Stunden/PV-Zeit** (Loxone 1490 tagsüber höher, nachts tiefer). Erwartung: weniger Starts (Forum: 30 → 12–13/Tag [11]) und COP-Vorteil durch höhere Lufttemperatur; Komfort über Estrichmasse prüfen. Sicherheit: Vermutung für Effizienz, Forumsbeleg für Startzahl.
6. **Startzähler bereinigen:** prüfen, ob unsere ~3.000 Starts Abtauungen enthalten (iDM/Hoval zählen Abtau-Starts mit [4][13]). Erwartung: realistischere Taktbewertung. Sicherheit: sicher als Prüfschritt.
7. **Bivalenz/Heizstab** bringt gegen Takten nichts (Problem ist Überleistung, nicht Unterleistung). Sicherheit: sicher (Logik).
8. **Größerer Hebel liegt beim WW** (~70 % Strom, AZ ~3,0): WW-Soll/Hysterese/Zeitfenster separat untersuchen (nicht Teil F63). Sicherheit: wahrscheinlich.

## Quellen (15)
[1] siblik iDM AERO SLM PDF · [2] cdn.hoval.com UltraSource B TI · [3] BWP Leitfaden Hydraulik (diekaelte.de) · [4] energiesparhaus 56645_2 · [5] IIR Uhlmann/Bertsch · [6] unibo Dongellini/Morini · [7] Fraunhofer WP-QS · [8] Fraunhofer WPsmart · [9] E3S Piechurski · [10] 42watt · [11] energiesparhaus 24763 · [12] energiesparhaus 80465_2 · [13] energiesparhaus 54272_4 · [14] energiesparhaus 71744 · [15] energiesparhaus 82665_2 – URLs je Punkt oben.