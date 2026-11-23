# FUND F24 – Grundfos ALPHA1 25-60 180: Kennwerte je Regelstufe (HK1 UG)

Stand: 25.10.2026, Web-Recherche (Subagent), nur öffentliche Seiten, PDFs nur per WebFetch. Nichts an der Anlage verändert.
Ausgangslage: Pumpe zeigt in CP3 = 22 W (Anzeige, von der Betreiber). HK1-Volumenstrom ungemessen.

## Kernergebnis
Für **einzelne Stufen (CP1/CP2/CP3, PP1–3, I–III) gibt KEINE der geprüften öffentlichen Textquellen Förderhöhe oder P1 als Zahl** an. Grundfos zeigt sie in allen Datenheften nur als Kennliniengrafik. Belegt sind nur Gerätegrenzwerte (P1 min/max, Nennpunkt, EEI) und die Produktnummern.

## Belegt (mit URL)
| Wert | Zahl | Quelle |
|---|---|---|
| Produktnummer ALPHA1 25-60 180 (aktuelle Generation) | 99199579 | https://onninen.fi/en/grundfos-grundfos-circulator-alpha1-25-60-180/p/CFZ582 ; Titel im Grundfos Product Center: https://product-selection.grundfos.com/us/products/alpha/alpha1/alpha1-25-60-180-99199579 (Seite selbst robots-gesperrt) |
| Nennpunkt (BEP) 25-60 180 | 1,94 m³/h bei 32,16 kPa (≈ 3,28 m) | https://onninen.fi/en/grundfos-grundfos-circulator-alpha1-25-60-180/p/CFZ582 |
| ALPHA1 **Model B**, XX-60 (Bsp. 15-60 130): P1 min / max | 3 W / 34 W; Nennförderung 1,94 m³/h, Nennhöhe 2,05 m, EEI 0,20 | https://www.solarics.de/cdn/shop/files/99160397_ALPHA1_1560_130.pdf |
| ALPHA1 25-60 N ([Nummer]), gleiche Reihe | „Power Min Speed: 3 W“, „Power Max Speed: 34 W“, Hmax 6 m, Qmax 3,4 m³/h | https://digitalassets.reecegroup.com.au/m/f65e403056738edc/original/Specification-Sheet-Grundfos-Alpha-1.pdf |
| Ältere ALPHA1-Generation (ca. 2014, EEI 0,23), 25-60 180 | P1 5–45 W; Produktnr. 98460755 bzw. 98463438 | https://www.meinhausshop.de/media/pdf/90_856_29--DBL-01-de.pdf ; https://www.buderus.com/ocsmedia/optimized/full/o455667v272_Flyer_Alpha1_DE.pdf |
| Nur Vergleich, US-Version 115 V/60 Hz (andere Pumpe!) | Konstantdruck III 39–45 W, II 14–45 W, I 8–45 W (min–max) | https://www.firstsupply.com/UserFiles/Documents/inRiver/Original/217660_Alpha1_Installation_Guide.pdf (Abschn. 10.1) |

Folgerung (sicher): Bei 22 W in CP3 ist die Pumpe sehr wahrscheinlich die **aktuelle Generation (Model B, max 34 W)**; bei der alten (max 45 W) wäre ebenfalls möglich, das Typschild entscheidet (Model-Zeile / Produktnr. 99199579 vs. 9846xxxx).

## Wahrscheinlich / Vermutung (nicht als Text belegt)
- **Konstantdruck-Höhen CP1/CP2/CP3 (XX-60):** nur als Kurve in den Datenheften. Aus der Grundfos-Kurvensystematik (CP3 knapp unter Maximalkurve, Stufen etwa gleichabständig, Hmax 6 m): CP1 ≈ 1,5–2 m, CP2 ≈ 2,5–3 m, CP3 ≈ 3,5–4 m. **Vermutung**, nicht abgelesen, Grafik war per Text-Abruf nicht auswertbar.
- **P1 je Stufe bei 0,5–1,0 m³/h:** CP3 = 22 W ist die Anzeige an deiner Pumpe (sicher, eigene Ablesung). Hydraulisch gilt bei 0,8 m³/h: 1 m Förderhöhe ≈ 2,2 W hydraulische Leistung; Wirkungsgrad Netz→Wasser bei diesen kleinen Punkten ca. 20–30 %. Daraus geschätzt: **CP2 ≈ 13–16 W, CP1 ≈ 7–10 W** (Vermutung). Die US-Vergleichswerte (I min 8 W, II min 14 W) liegen in der gleichen Größenordnung (andere Pumpe).
- PP1–3 (Proportionaldruck) liegen bei kleinem Durchfluss unter den CP-Kurven gleicher Nummer, also tendenziell nochmals weniger Watt. Für FBH empfiehlt Grundfos aber CP. Konstantkurve I/II/III = feste Drehzahl, Leistung je nach Anlagenwiderstand.
- **Mit eigener Messung ersetzen:** die Pumpe zeigt die Watt selbst an. Je Stufe 10 min laufen lassen, Watt ablesen (bei laufender Heizung, gleiche Ventilstellungen). Das schlägt jede Schätzung oben.

## Rechnung Jahresersparnis (Annahmen gekennzeichnet)
Annahmen: Laufzeit HK1-Pumpe 4000–5000 h/a (Annahme; nicht gemessen, WW-Vorrang schaltet sie zeitweise ab); Strompreis 21,15 ct/kWh; Wattwerte CP2/CP1 = Schätzung oben.

| Wechsel | Differenz P1 | kWh/a (4000–5000 h) | €/a |
|---|---|---|---|
| CP3 → CP2 | 6–9 W | 24–45 kWh | 5,10–9,50 € |
| CP3 → CP1 | 12–15 W | 48–75 kWh | 10,20–15,90 € |

Einordnung: im Bereich 5–16 € pro Jahr. Kleiner Hebel, kostet aber nichts, wenn der Durchfluss reicht.

## Durchfluss-Risiko
- Der HK1-Volumenstrom ist **ungemessen**. Die bekannten 16 L/min gelten für den WP-Kreis, nicht für HK1.
- Bei kleinerer Stufe sinkt der Durchfluss durch die FBH. Folge: größere Spreizung, die entferntesten bzw. längsten Kreise werden zuerst schwächer. Mit den Loxone-Stellantrieben (Teilkreise zu) steigt der Widerstand zusätzlich; CP hält dann die Höhe konstant, aber die absolute Höhe ist bei CP1 klein.
- Prüfung nach Umstellung: Spreizung HK1 Vorlauf/Rücklauf (Loxone/HoxPi) über 2–3 Tage, Raumtemperaturen der hintersten Räume, ob die Ventile länger offen stehen. Spreizung bis ca. 5–7 K bei FBH unkritisch; deutlich mehr oder kalte Räume = Stufe zurück. Rückweg: CP3.

## Nicht gefunden
- Förderhöhe in m je Stufe CP1/CP2/CP3, PP1–3, I–III als Zahl: in keiner geprüften Textquelle.
- P1 je Stufe für die EU-ALPHA1 (Model A oder B): nicht gefunden, nur min/max der Reihe.
- Grundfos Product Center (product-selection.grundfos.com): Seite für 99199579 robots-gesperrt, nicht abrufbar.
- Grundfos-Datenheft ALPHA1 Model B (api.grundfos.com, Literatur 6013016) und ALPHA1 (5235369): per WebFetch nur Binärdaten, nicht lesbar. **Diese beiden PDFs enthalten sehr wahrscheinlich die Kurven je Stufe** – bei Bedarf im Browser öffnen und die CP-Kurven bei 0,5–1,0 m³/h ablesen.
- Forenmesswerte (haustechnikdialog.de) je Stufe für ALPHA1: keine Treffer in den Suchen.

## Geprüfte URLs
1. https://www.grundfos.cn/content/dam/global/page-assets/learn/grundfos-for-installers/documents/HowToSell_Alpha1_leaflet.pdf (nur Reihe 3–50 W, EEI ≤ 0,20)
2. https://media.hornbach.at/hb/technicaldatasheet/as.181884325.pdf (ALPHA1 25-40 180, 93074166: P1 4–27 W, EEI 0,20 – andere Größe)
3. https://www.meinhausshop.de/media/pdf/90_856_29--DBL-01-de.pdf (alte Generation, 5–45 W, Produktnr.)
4. https://www.pumpa.eu/en/alpha1-25-60-180-220-240v-9h-ac0/ (P1 0,05 kW, Qmax 60 l/min, Hmax 6 m)
5. https://www.firstsupply.com/UserFiles/Documents/inRiver/Original/217660_Alpha1_Installation_Guide.pdf (US-Version, Watt je Konstantdruckstufe)
6. https://tfpumps.com/resources/grundfos/Grundos_Alpha_Datasheet_B_compressed.pdf (XX-60: 5–45 W, nur Kurven)
7. https://magento.waterpompshop.nl/media/wysiwyg/manual/5712607862770.pdf (ALPHA1 L: XX-60 4–45 W)
8. https://www.solarics.de/cdn/shop/files/99160397_ALPHA1_1560_130.pdf (Model B 15-60: 3–34 W, 1,94 m³/h / 2,05 m)
9. https://digitalassets.reecegroup.com.au/m/f65e403056738edc/original/Specification-Sheet-Grundfos-Alpha-1.pdf (25-60 N 99199593: 3–34 W)
10. https://onninen.fi/en/grundfos-grundfos-circulator-alpha1-25-60-180/p/CFZ582 ([Nummer], BEP 1,94 m³/h / 32,16 kPa)
11. https://www.bauhaus.at/heizungspumpen/grundfos-umwaelzpumpe-alpha1-25-60-180/p/33175889 (45 W, 3,06 m, 2,28 m³/h – Händlerangaben, Generation unklar)
12. https://product-selection.grundfos.com/us/products/alpha/alpha1/alpha1-25-60-180-99199579 (robots-gesperrt)
13. https://api.grundfos.com/literature/Grundfosliterature-6013016.pdf (nicht lesbar)
14. https://api.grundfos.com/literature/Grundfosliterature-5235369.pdf (nicht lesbar)
15. https://www.buderus.com/ocsmedia/optimized/full/o455667v272_Flyer_Alpha1_DE.pdf (alte Generation 5–45 W, Produktnr. [Nummer])