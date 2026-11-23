# FUND F24 – Grundfos ALPHA1 25-60 180 (HK1 UG): Stufen, Leistung, Ersparnis

- Datum: 24.10.2026
- Katalog: F24
- Autor: Recherche-Agent, nur öffentliche Quellen (keine Logins, keine Downloads, PDFs nur per WebFetch gelesen)
- An der Anlage wurde nichts geändert. der Betreiber entscheidet.

## 0. Welche ALPHA1 ist das? (wichtig, sonst stimmen die Stufen nicht)

Unter dem Namen „ALPHA1 25-60 180“ gibt es drei verschiedene Pumpen:

| Generation | Stufen | P1 min–max (XX-60) | Anzeige | Quelle |
|---|---|---|---|---|
| ALPHA1 (2013, z. B. [Nummer]) | 7: PP1, PP2, CP1, CP2, I, II, III (**kein CP3**) | 5–45 W | 7-Segment W + „POWER ON“ | https://www.heizungsdiscount24.de/pdf/Grundfos-Alpha-1-EU-Datenblatt.pdf , https://www.meinhausshop.de/media/pdf/90_856_29--DBL-01-de.pdf |
| **ALPHA1 Model B** (ab ca. 2018, z. B. [Nummer]) | 9: PP1–3, CP1–3, I–III, Werk = PP2 | **3–34 W** | Display W + 9 Leuchtfelder | https://www.meinhausshop.de/media/pdf/90_856_29--DBL-03-de.pdf , https://www.rskdatabasen.se/infodocs/DOS/DOS_25_5758798.pdf |
| ALPHA1 L (z. B. [Nummer]) | I, II, III + „Radiator“ + „Fußboden“, LED, **keine W-Anzeige** | 4–45 W | nur LEDs | https://magento.waterpompshop.nl/media/wysiwyg/manual/5712607862770.pdf |

Zuordnung bei dir:
- **sicher:** Die Pumpe zeigt Watt an und hat „POWER ON“. Das zeigen die Fotos PXL_20260317_162556332.jpg (~15 W) und PXL_20260627_092615692.jpg (~22 W), siehe `[lokaler Pfad]`. Damit ist es **keine ALPHA1 L**.
- **wahrscheinlich: ALPHA1 Model B.** Die ALPHA1 von 2013 hat kein CP3. Bei der MK1-Pumpe ist außerdem „ALPHA1 B … PC-1928“ lesbar (Foto PXL_20260626_172356954.jpg, Produktion 2019, Woche 28). Gleiche Station, gleiches Baujahr.
- Prüfen: Typenschild HK1-Pumpe. Steht dort „ALPHA1 B“ bzw. „Model B“ und „P1 3–34 W“?
- Steht dort „P1 5–45 W“ (Generation 2013), kann es kein CP3 geben. Dann hat der Anzeigewert eine andere Bedeutung, z. B. CP2 oder Drehzahlstufe III.

## 1. Tabelle Stufen (ALPHA1 Model B 25-60)

Die Zahlenwerte je Stufe stehen bei Grundfos nur in Kennlinien-Grafiken. Das XX-60-Diagramm in der Anleitung ist Fig. 29 mit H 0–6 m, P1 0–35 W, Q 0–3,4 m³/h. Als Text ließen sich die Werte nicht auslesen. Die Produktseiten unter product-selection.grundfos.com sind für Abrufe gesperrt (robots), und die Grundfos-PDFs unter api.grundfos.com kamen nur als Binärdaten zurück.
**Deshalb sind alle Werte je Stufe unten geschätzt (Vermutung), nicht abgelesen.** Rechenweg siehe Abschnitt 4.

| Stufe | Förderhöhe max (Schätzung) | P1 bei ~1 m³/h (Schätzung) | Quelle-URL |
|---|---|---|---|
| CP1 | ~1,5–2 m konstant | ~8–11 W | Kurve: https://www.rskdatabasen.se/infodocs/DOS/DOS_25_5758798.pdf (Fig. 29) |
| CP2 | ~2,5–3 m konstant | ~14–16 W | ebenda |
| CP3 | ~3,5–4,5 m konstant | **~22 W (Anzeige bei dir, sicher)** | Foto PXL_20260627_092615692.jpg |
| PP1 | ~1,5–2 m bei Nullförderung, fällt mit Q | ~6–9 W | ebenda |
| PP2 (Werk) | ~2,5–3 m bei Q = 0 | ~10–13 W | ebenda |
| PP3 | ~3,5–4,5 m bei Q = 0 | ~15–19 W | ebenda |
| I | Festdrehzahl niedrig, ~2 m bei Q = 0 | ~8–10 W | ebenda |
| II | Festdrehzahl mittel, ~4 m bei Q = 0 | ~15–18 W | ebenda |
| III | Maximalkurve, 6,0 m bei Q = 0 | ~25–30 W | Hmax 6 m und P1 max 34 W: https://digitalassets.reecegroup.com.au/m/f65e403056738edc/original/Specification-Sheet-Grundfos-Alpha-1.pdf |

Bezeichnung „Konstantkurve I/II/III“: Gemeint sind dieselben Drehzahlstufen I, II, III („Konstantkurve/Konstantdrehzahl“).

## 2. belegt (Herstellerunterlagen, öffentlich)

- **ALPHA1 Model B XX-60:** P1 min. 3 W, P1 max. 34 W (0,04–0,32 A). Hmax 6 m, Qmax 3,4 m³/h, Nennpunkt 1,94 m³/h / 3,36 m.
  - Quellen: https://www.meinhausshop.de/media/pdf/90_856_29--DBL-03-de.pdf (Abschnitt 10.5), https://res.cloudinary.com/evoleska/image/upload/v1762164993/utfqouvadyhodi3fydqt.pdf ([Nummer])
- **Model B Bedienung:** 9 Einstellungen, Werkseinstellung PP2. Reihenfolge per Taste: PP2 → PP3 → CP1 → CP2 → CP3 → III → II → I → PP1.
  - Das Display zeigt die aktuelle Leistung in W.
  - Quelle: https://www.meinhausshop.de/media/pdf/90_856_29--DBL-03-de.pdf
- **Fußbodenheizung laut Grundfos:** empfohlen Konstantdruck CP1, CP2 oder CP3, alternativ Konstantkurve I/II/III.
  - Die Wahl hängt laut Grundfos von der Anlage und vom Wärmebedarf ab.
  - Werden nicht alle Räume warm, soll man auf die nächsthöhere Stufe bzw. auf die Alternative gehen.
  - Quelle: https://www.rskdatabasen.se/infodocs/DOS/DOS_25_5758798.pdf (7.5.3 / 7.5.5)
- **ALPHA1 der Generation 2013:** Für Fußboden ist CP1 empfohlen, CP2 die Alternative.
  - Quelle: https://www.meinhausshop.de/media/pdf/90_856_29--DBL-01-de.pdf (Tab. 9.1)
  - Grundfos selbst fängt also bei Fußbodenheizung mit der **untersten** CP-Stufe an.
- **Anzeigegenauigkeit:** Die Watt-Anzeige ist ganzzahlig, ±5 % (Generation 2013, https://www.buderus.com/ocsmedia/optimized/full/o455667v272_Flyer_Alpha1_DE.pdf).
- **Deine Pumpe:** Die Fotos zeigen 15 W (17.03.2026) und 22 W (27.06.2026). Welches Foto wirklich die HK1-Pumpe zeigt, ist im Fotoprotokoll nicht eindeutig.

## 3. wahrscheinlich / Vermutung

- **wahrscheinlich:** Die Pumpe ist eine ALPHA1 Model B (Begründung in Abschnitt 0).
- **Vermutung:** die Förderhöhen und P1-Werte je Stufe in der Tabelle oben. Sie sind aus Hmax 6 m und P1 max 34 W, deinem Messwert 22 W bei CP3 und üblichen Wirkungsgraden kleiner EC-Nassläufer (30–50 %) abgeleitet.
  - Rückweg zur Prüfung: Fig. 29 im Original-PDF selbst ansehen und bei Q = 1 m³/h ablesen.
  - Noch besser: Pumpe testweise umstellen und die W-Anzeige ablesen. Eine Messung schlägt jede Schätzung.
- **Achtung, 16 L/min:** Der gemessene Volumenstrom gilt **durch die WP** (Erzeugerkreis bis zum Puffer). Die HK1-Pumpe sitzt hinter Puffer und ESBE-Mischer, das ist ein eigener Kreis.
  - **Der HK1-Volumenstrom ist damit nicht gemessen (sicher).** Rechnung unten mit ~1 m³/h als Annahme.
  - Bei CP3 und offenen Stellantrieben ist der HK1-Durchfluss eher größer.

## 4. nicht gefunden

- Numerische Kennlinienwerte (H und P1 je Stufe bei 1 m³/h) als Text oder Tabelle: weder bei Grundfos noch bei Händlern oder in Foren.
- Die Seiten product-selection.grundfos.com ([Nummer], [Nummer], [Nummer]) blocken automatische Abrufe (robots).
- Die PDFs unter api.grundfos.com (Datenheft Model B 6013016, Anleitung 6014883, ALPHA1 [Nummer]) kamen als Binärdaten zurück und waren nicht lesbar.
- Für eine echte Ablesung: Fig. 29 in https://www.rskdatabasen.se/infodocs/DOS/DOS_25_5758798.pdf am Bildschirm ansehen oder Grundfos Product Center im Browser öffnen (ohne Login).

## 5. Rechnung Jahres-kWh / €

Annahmen:
- Laufzeit HK1-Pumpe 4.000–5.000 h/Jahr (**Annahme**, nicht gemessen; bei WW-Ladung ist die Pumpe aus).
- Strompreis 0,21 €/kWh.
- Rechenweg P1: Bei Konstantdruck ist P1 ≈ Grundlast (~3 W) + Anteil ∝ H·Q/η.
  - Mit CP3 = 22 W bei gleichem Q: CP2 (~0,7·H) ≈ 16 W, CP1 (~0,4·H) ≈ 11 W.
  - Sinkt Q mit der Förderhöhe mit (√-Gesetz), dann CP2 ≈ 14 W und CP1 ≈ 8 W.

| Wechsel | ΔP (Schätzung) | kWh/Jahr bei 4.000 h | kWh/Jahr bei 5.000 h | €/Jahr |
|---|---|---|---|---|
| Ist CP3 (22 W) | – | 88 kWh | 110 kWh | 18–23 € |
| CP3 → CP2 | 6–8 W | 24–32 kWh | 30–40 kWh | **5–8 €** |
| CP3 → CP1 | 11–14 W | 44–56 kWh | 55–70 kWh | **9–15 €** |

Einordnung: Das ist wenig Geld. Ein weiterer Effekt ist nicht eingerechnet: Weniger Pumpendruck heißt meist weniger Volumenstrom, damit mehr Spreizung und ein kühlerer Rücklauf. Das kann der WP etwas helfen. Nicht beziffert, Vermutung.

## 6. Reicht der Durchfluss bei CP2/CP1? (qualitativ)

- Bedarf UG (wahrscheinlich): Heizlast Haus 3–5 kW bei −15 °C, davon UG grob 1,5–2,5 kW.
  - Bei 5 K Spreizung braucht das 0,26–0,43 m³/h, bei 3 K Spreizung 0,43–0,72 m³/h.
  - **~1 m³/h ist also deutlich mehr als nötig.**
- Widerstand (typisch, Vermutung): 100 m² FBH mit ca. 8–10 Kreisen à 80–100 m (16er Rohr) und je ~0,05–0,1 m³/h.
  - Die Kreise kosten ~1–2 m, Verteiler, Mischer, Absperrungen und Rückschlag nochmal ~0,5–1 m. Zusammen ~1,5–3 m.
- **CP2 (~2,5–3 m):** reicht sehr wahrscheinlich, auch für die längsten Kreise.
- **CP1 (~1,5–2 m):** kann bei langen Kreisen oder stark gedrosselten Ventilen knapp werden. Dann bleibt der längste bzw. am stärksten gedrosselte Kreis kühler.
- Mit den Loxone-Stellantrieben (Auf/Zu) sind oft nur wenige Kreise offen. Der Konstantdruck hält dann den Druck und verteilt gut.

## 7. Entscheidungsvorlage (nichts geändert, du entscheidest)

| Option | Ersparnis/Jahr | Risiko | Rückweg |
|---|---|---|---|
| A: bleiben bei CP3 | 0 | keins | – |
| **B: CP2 (Vorschlag)** | ~25–40 kWh, ~5–8 € | gering | von CP2 aus 1× Taste → CP3 (Folge: … CP1 → CP2 → CP3 → III …) |
| C: CP1 | ~45–70 kWh, ~9–15 € | mittel: längste Kreise / kälteste Räume an kalten Tagen | Taste bis CP2/CP3 |

Wenn du B oder C testest, sollte vorher bzw. dabei Folgendes passieren:

1. Typenschild der HK1-Pumpe ablesen (Model B? P1 3–34 W?). Erst dann ist klar, dass es CP3 wirklich gibt.
2. W-Anzeige notieren: vorher bei CP3, danach in der neuen Stufe, mit Datum und Uhrzeit. Das ersetzt die Schätzwerte oben.
3. Eine kalte Woche beobachten (Loxone):
   - HK1-VL/RL-Spreizung über die OneWire-Fühler am Verteiler.
   - Raumtemperaturen UG gegen das Soll.
   - Ventilöffnungszeiten der Raumregler. Bleiben Stellantriebe dauernd offen und erreichen trotzdem das Soll nicht, ist die Stufe zu klein.
4. Optional: tatsächliche Laufzeit der HK1-Pumpe aus Loxone/HoxPi auswerten, statt der Annahme von 4.000–5.000 h.

Fazit: Die Ersparnis ist klein (einstellige Euro bis ~15 €/Jahr). CP2 ist der risikoarme Mittelweg, CP1 entspricht der Grundfos-Grundempfehlung für Fußbodenheizung, muss aber an kalten Tagen geprüft werden.