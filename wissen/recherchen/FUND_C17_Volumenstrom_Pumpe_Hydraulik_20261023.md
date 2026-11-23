# FUND: UltraSource B comfort C17 – Volumenstrom, Pumpe, Hydraulik (Web-Recherche 23.10.2026)

**Anlage:** Hoval UltraSource B comfort C17 (L/W, IBN 08.10.2021), Puffer EnerVal 300, 2 FBH-Mischerkreise (je ~100 m²), TopTronic E.
**Bereits bekannt (nicht wiederholt):** Katalog CH 2026/27 S. 37/38/43 – Puffer bei L/W-WP Pflicht, Mindestpuffer C17 = EnerVal 300, Speicherkreis Nenn 2,2 m³/h, max. 3 Starts/h.
**Hauptquelle Q1:** Hoval Katalog „UltraSource® B Luft/Wasser-Wärmepumpe" 2026/27 (CH-DE), 60 S. – https://cdn.hoval.com/ultrasource-b-cf-cp_ch-de_hybris_original.pdf (gedruckte Seitenzahl = PDF-Seite)

## Fragen
1. Nenn- und Mindest-Volumenstrom Heizwasser C17; Spreizung Heizen / Abtauen
2. Interne Umwälzpumpe (Typ, Restförderhöhe-Kennlinie), Durchflussüberwachung (Schwelle), Wasserinhalt Inneneinheit
3. Hoval-Regel Heizkreis-Durchfluss ≤ Speicherkreis-Durchfluss, Weiche vs. Puffer, Folgen bei Verstoß
4. Fachliteratur/Foren: Mischung im Puffer, erhöhte VL, JAZ-Verlust, Faustwerte

## Belegt

### Hydraulische Daten C17 (Q1, S. 17, Tabelle „Hydraulische Daten", Spalten 8 / 11 / 17)
| Zeile (wörtlich) | (8) | (11) | (17) |
|---|---|---|---|
| Max. Heizungswassermenge Heizen ΔT 5 K (A7W35) [m³/h] | 1.5 | 2.2 | **3.7** |
| Nenn-Heizungswassermenge Heizen ΔT 5 K (A7W35) [m³/h] | 0.8 | 1.2 | **2.2** |
| Max. Durchfluss Heizungsseite Kühlen, ΔT 3 K [m³/h] | 2.0 | 3.6 | **3.9** |
| Druckverlust bei Nenn-Heizungswassermenge ΔT 5 K (A7W35) [kPa] | 9 | 9 | **38** |
| Restförderhöhe Heizungspumpe bei max. Durchfluss [kPa] | 65 | 66 | **37** |
| Max. Betriebsdruck Heizungsseite [bar] | 3 | 3 | 3 |
| Max. Vorlauftemperatur (ohne/mit Einschraub-Elektroheizeinsatz) [°C] | 62/65 | 62/65 | 62/65 |
| Vor-/Rücklaufanschluss Heizung | R 1″ | R 1″ | R 1″ |

- Umrechnung (eigene Rechnung): 2,2 m³/h = **~36,7 l/min**; × 1,163 × 5 K ≈ 12,8 kW. Max. 3,7 m³/h ≈ 61,7 l/min.
- Auslegungsspreizung: **ΔT 5 K Heizen**, **ΔT 3 K Kühlen** (beides als Bezug der Tabellenzeilen, Q1 S. 17).

### Interne Komponenten (Q1, S. 5, „Inneneinheit UltraSource® B comfort C")
- „Integrierte Komponenten: - drehzahlregulierte Hocheffizienzpumpe - Durchflusssensor/Wärmemengenzähler - Elektroheizeinsatz 1 bis 6 kW - 3-Weg-Umschalt-Kugelhahn für Heizung/Warmwasser"
- „UltraSource® B comfort C (11,17) mit modulierendem Scroll-Kompressor"; „Plattenkondensator aus Edelstahl/Kupfer"
- → Es gibt einen **Durchflusssensor** (kein separater Strömungswächter als Zubehör genannt). Pumpenhersteller/-typ wird **nicht** genannt.

### Hoval-Regel Heizkreis ≤ Speicherkreis (Q1, S. 43, „Hydraulischer Abgleich/Einstellung der Durchflussmengen")
- „Die Einregulierung der Durchflussmengen erfolgt durch den Installateur. Dabei soll die empfohlene Nenndurchflussmenge der Wärmepumpe als Grundlage dienen"
- „Bei Anlagen mit Energiepufferspeicher darf die Durchflussmenge im voll geöffneten Heizkreis nicht grösser sein als die Durchflussmenge im Speicherkreis. Sonst findet eine Überströmung des kälteren Heizungswasser-Rücklaufes über den Energiepufferspeicher statt, was zu Mischtemperaturen im Vorlauf der Heizungsanlage führt."

### Puffer-Funktion / Weiche / Direkteinbindung
- Q1 S. 37: Puffer bewirkt „Hydraulische Entkoppelung der unterschiedlichen Volumenströme von Wärmepumpe und Wärmeverteilsystem (Heizung)" und „Ermöglicht den Anschluss mehrerer Heizkreise".
- Q1 S. 37: Verzicht nur, „wenn es sich um einen direkten Heiz- oder Kühlkreis mit Speicherfähigkeit und stets konstanter Durchflussmenge handelt (⅔ müssen unabsperrbar sein)."
- Q1 S. 42 (Checkliste): „Direkteinbindung ins Heizungsnetz vermeiden, wenn dann nur mittels Differenzdruck-Überströmventil (Mindestvolumenstrom) und Vorschaltgefäss (Mindestwasservolumen)"
- Q1 S. 48: „Da die Wärmetauscher der Wärmepumpe sehr geringe Wasserinhalte aufweisen, führt der ständig wechselnde Heizleistungsbedarf … zu überhöhten Schalthäufigkeiten." Kriterien: „Richtiger Volumenstrom über die Wärmepumpe während der gesamten Nutzungszeit" und „Genügend Speicherfähigkeit und ein Mindestwasservolumen der Wärmenutzungsseite".
- Q1 S. 35: „Falsche Durchflussmengen aufgrund von falscher Dimensionierung der Verrohrung … unsachgemässen Pumpenbetrieb können Schäden an der Wärmepumpe verursachen." (gekürzt) · „In den Heizungsrücklauf ist vor der Wärmepumpe unbedingt ein Schlammabscheider einzubauen."
- Q1 S. 36: „Die Leitungsdimensionierung muss nach den erforderlichen Durchflussmengen erfolgen."
- Q1 S. 12 (Zubehör): „Differenzdruck-Überströmventil DN 20".
- Hydraulik-Begriffe „hydraulische Weiche", „Vierleiter/Zweileiter" kommen im Katalog **nicht** vor; Hoval spricht nur von „Energiepufferspeicher" (Trennspeicher-Funktion).

### Abtauung / Inbetriebnahme
- Q1 S. 35: Kondensat „pro Abtauzyklus innerhalb von 2 Minuten bis zu 6 Liter".
- Q2 = Hoval Produktinformation 4 221 941 / 02 „Wichtige Produktinformationen zu UltraSource® B comfort C (8-17)", S. 9/10 – https://www.hoval.ch/medias/4221941-02-DE.pdf : Raumtemperatur bei IBN „mindestens 15 °C … da zu wenig Energie für eine Abtauung vorhanden wäre"; „Falls ein Energiepufferspeicher vorhanden ist, darf dessen Heizwassertemperatur bei der Inbetriebnahme nicht unter 20 °C liegen."
  (Hinweis: der funktionierende Link trägt einen langen `?context=…`-Parameter; per Websuche „4221941-02-DE.pdf hoval" findbar.)

### Fachliteratur / Foren (Frage 4)
- Q3 Wolf Heiztechnik (Krawietz/Bauer) via baulinks.de, 30.10.2023 – https://www.baulinks.de/webplugin/2023/1178.php4 : „Ein Trennspeicher trennt die Volumenströme zur Wärmepumpe von denen innerhalb des Gebäudes." Senkung VL um 1 K steigert Effizienz L/W-WP „um ca. 2 – 2,5%".
- Q4 elektronik-zeit.de (M. Amato, 10.05./04.10.2026) – https://elektronik-zeit.de/waermepumpe/reihenpuffer-trennpuffer-vergleich/ : „Jede Mischung mit kühlerem Wasser zwingt die Wärmepumpe, eine höhere Vorlauftemperatur zu erzeugen"; „Klassischer Trennpuffer mit gegenläufigen Anschlüssen: 2 bis 5 Kelvin". ⚠ Blog, Werte als „Fachforen-Konsens" ohne Einzelbeleg, JAZ-Zahlen intern widersprüchlich (4–15 % / 10–15 %) → nur als Größenordnung verwenden.
- Q5 energiesparhaus.at, Thread „Hoval UltraSource LWP – allgemeiner Austausch", S. 3 – https://www.energiesparhaus.at/forum-hoval-ultrasource-lwp-allgemeiner-austausch-und-anlage-optimieren/56645_3 :
  - Optihome 03.12.2023: Volumenstrom „00-302" = 15,0–30,0 l/min; „CP Maximaldrehzahl "33-328": 44%"; „Drehzahl CP "00-271" = 44%".
  - Domi90 11.12.2023: WP-Volumenstrom (33-328 auf 48 %) „bestmöglich an den fbh volumenstrom angepasst".
  - Optihome 06.01.2024: nach Erhöhen dT-Heizen auf 8 K „lagen weiterhin 5k auseinander"; Marty 31.01.2024: „dT Heizen wird ignoriert." / CP-Maximaldrehzahl = feste Drehzahl im Heizbetrieb; im WW-Betrieb Pumpe 100 %.
- Q6 energiesparhaus.at, Thread „UltraSource B comfort 11 – kühlt nicht", S. 1 – https://www.energiesparhaus.at/forum-hoval-ultrasource-b-comfort-11-optimierung-kuehlt-nicht/85791_1 : sharknz 25.07.2026: „Hoval hat bei mir auch ohne Kühlung auf einem Puffer im Rücklauf bestanden" (u. a. wegen Abtauen).

## Wahrscheinlich
- **Spreizung real ≈ 5 K**: Pumpe läuft im Heizbetrieb mit fester Drehzahl (33-328), nicht ΔT-geregelt (Forum Q5, 2 Nutzer übereinstimmend; nicht von Hoval belegt). Spreizung ergibt sich dann aus Leistung/Volumenstrom, nicht aus dem dT-Parameter.
- **Abtauung**: Kreisumkehr – Wärme wird dem Heizwasser/Puffer entzogen; deshalb Puffer „zwingend (Abtauenergie)" (Q1 S. 37). Eine eigene Abtau-Spreizung nennt Hoval nicht.
- **Volumenstrom-Anzeige** in TopTronic E: Datenpunkt 00-302 „Volumenstrom" (aus Forum; in unserer Register-Doku gegenprüfen), Pumpendrehzahl 00-271.
- **Restförderhöhe C17 relativ knapp**: 37 kPa bei 3,7 m³/h; bei Nenn 2,2 m³/h liegt sie höher (Pumpenkennlinie), aber die WP selbst frisst dort bereits 38 kPa Druckverlust. Rohrnetz zum Puffer + Schlammabscheider + Umschaltventil müssen da hineinpassen.
- **Mischverlust** bei HK-Durchfluss > WP-Durchfluss: Größenordnung 1–5 K höhere WP-Vorlauftemperatur nötig, ~2–2,5 % Effizienz je K (Q3/Q4) – Werte nicht anlagenspezifisch.

## Nicht gefunden (öffentlich, ohne Login)
- **Mindest-Volumenstrom** Heizwasser C17 und Abschaltschwelle des Durchflusssensors (Fehler „Durchfluss zu gering") – weder Katalog 2026/27 noch Produktinfo 4 221 941 noch Foren.
- **Pumpenhersteller/-typ** der internen Heizungspumpe und **Restförderhöhe-Kennlinie** (nur ein Punkt: 37 kPa bei 3,7 m³/h).
- **Wasserinhalt der Inneneinheit** (Katalog nennt nur „sehr geringe Wasserinhalte" der WP-Wärmetauscher, S. 48).
- **Abtau-Spreizung / Abtau-Volumenstrom**.
- Begriffe „hydraulische Weiche", „Vierleiter-/Zweileiteranbindung" in Hoval-Unterlagen zur UltraSource B.
- Nicht erreichbar: AT-Katalog 2025/26 (cdn.hoval.com/ultrasource-b-comfort-c-compact-c-at-d-25-hybris-original.pdf → Fehler), Bedienungsanleitung 4217234-02 (leer geliefert), haustechnikdialog-Threads (blockiert).
- Nächste Quelle dafür: Montage-/Installationsanleitung der Inneneinheit (Pumpenkennlinie, Durchfluss-Alarm) – z. B. vom Hoval-Service oder aus dem Geräteordner; alternativ Live-Wert 00-302 bei Abtau und bei Heizbetrieb mitloggen.

## Bedeutung für des Betreibers Anlage („Was bringt uns das")
Zielwert für den WP-Kreis C17 ist **~2,2 m³/h (~37 l/min) bei 5 K**; laut Hoval (Katalog S. 43) dürfen beide FBH-Mischerkreise zusammen bei voll offenem Mischer **nicht mehr fördern als der Speicherkreis**, sonst strömt kalter Rücklauf durch den EnerVal 300 nach oben, der Heizkreis-Vorlauf wird gemischt und die WP muss höher fahren (Größenordnung 2–2,5 % Effizienzverlust je K). Prüfen: WP-Volumenstrom (00-302 / Pumpendrehzahl 00-271, CP-Maximaldrehzahl 33-328) gegen die Summe der Durchflüsse der beiden Grundfos-ALPHA1-Kreise; praktischer Indikator ist ein Unterschied von mehr als 1–2 K zwischen WP-Vorlauf und Heizkreis-Vorlauf vor dem Mischer. Ist der Heizkreis stärker, entweder die ALPHA1-Stufen/Strangventile reduzieren oder die CP-Maximaldrehzahl anheben (Restförderhöhe C17 ist aber knapp: 38 kPa Eigenverlust bei Nenndurchfluss).