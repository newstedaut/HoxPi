# FUND: FBH-Heizkreispumpe – Regelart, Volumenstrom, Einzelraumregelung (Recherche 23.10.2026)

Anlage: Hoval UltraSource B comfort C17, Puffer EnerVal 300 [Korr. 23.10.2026, stand „CombiVal ESR 400“], 2 FBH-Kreise je ca. 100 m², je eigene Grundfos-Pumpe (Typ NICHT bekannt), HK1 Mischerkreis, Loxone-Stellantriebe je Raum. WP-Speicherkreis ca. 34 l/min (aus Projektkontext, nicht neu geprüft).
Nur öffentliche Quellen, Zitate wörtlich (<15 Wörter), PDF-Inhalte per WebFetch extrahiert (Seitenangaben laut Extrakt, Tabellenlayout teils verloren).

---

## 1. BELEGT

### 1.1 Grundfos-Empfehlung Regelart Fußbodenheizung

| Pumpe | Empfehlung FBH | Zitat | Quelle |
|---|---|---|---|
| ALPHA2 (Generation mit 8 Leuchtfeldern) | AUTOADAPT, Alternative CP2 oder CP1 | Tabelle Abschn. 7.1: „Fußbodenheizung – AUTOADAPT – Obere/Untere Konstantdruck-Kennlinie“ | https://www.ava-berlin.de/assets/downloads/grundfos/betriebsanleitung_alpha2.pdf |
| ALPHA2 | AUTOADAPT erst eine Woche laufen lassen | „Pumpeneinstellung AUTOADAPT mindestens eine Woche beizubehalten“ | ebd., S. 16 |
| ALPHA2 (älteres Datenheft) | AUTOADAPT = Proportionaldruck-basiert | „Bei der Einstellung AUTOADAPT läuft die Pumpe mit Proportionaldruckregelung.“ | https://www.loebbeshop.de/Media/Default/Uploaded/static/doc/datenheft-alpha2_1819.pdf (S. 6) |
| ALPHA2 GO | Konstantdruck für FBH | „Diese Regelungsart eignet sich besonders für Fußbodenheizungen“ | https://www.heizungsdiscount24.de/pdf/Grundfos-Alpha2Go-Montage-und-Betriebsanleitung.pdf (S. 14) |
| ALPHA2 GO | Werkseinstellung | „werkseitig auf Proportionaldruck, AUTOADAPT, voreingestellt“ | ebd., S. 13 |
| UPM3 (Datenheft) | FBH mit variablem Durchfluss: Konstantdruck/AUTOADAPT | „can be used in underfloor heating systems“ (UPM3 AUTO, CP-AUTOADAPT) | https://renewableheatinghub.co.uk/wp-content/uploads/wpforo/attachments/6370/11251-Grundfos-UPM3-Pump.pdf |
| UPM3 AUTO (Oilon-Blatt) | Konstantdruck-AUTOADAPT „in most cases“ | „the bulk of the pressure loss can be attributed to the actual heating circuit“ | https://shop.eu.oilon.com/wp-content/uploads/sites/3/2021/08/TBEA-00006-2350EN-Heating-circuit-pump-Grundfos-UPM3-AUTO.pdf |

### 1.2 Warum Konstantdruck bei FBH (Physik der Regelart)

- Proportionaldruck: Förderhöhe sinkt mit sinkendem Bedarf – „Die Förderhöhe (der Druck) sinkt mit abnehmendem … Wärmebedarf“ (Datenheft ALPHA2, S. 12, URL s. o.).
- Konstantdruck: „Die Förderhöhe (der Druck) bleibt dabei unabhängig vom Wärmebedarf konstant.“ (ebd., S. 12)
- Xylem/Bell&Gossett: „Constant pressure control is ideal for systems in which the distribution pipe is non-existent or very short.“ – https://www.xylem.com/en-029/resources/tip-sheets/how-to-choose-the-correct-speed-control-for-heating-systems/
- Proportionaldruck ist für Netze gedacht, wo „about half of your pressure loss … will be in the distribution pipe“ (ebd.).

### 1.3 Anzeige an der Pumpe (was der Endkunde ablesen kann)

**ALPHA2 (8 Leuchtfelder + Display)** – https://www.ava-berlin.de/assets/downloads/grundfos/betriebsanleitung_alpha2.pdf
- „Die aktuelle Pumpeneinstellung wird durch acht unterschiedliche Leuchtfelder angezeigt.“ (S. 15)
- Felder (Tastendruck-Reihenfolge laut Anleitung): AUTOADAPT (Werk) → PP1 → PP2 → CP1 → CP2 → III → II → I (Konstantkennlinie = feste Drehzahl).
- Eigenes Leuchtfeld für Nachtabsenkung; „Werkseinstellung: Automatische Nachtabsenkung = nicht aktiv.“ (S. 15)
- Display dieser Generation zeigt Leistungsaufnahme in Watt (Extrakt Abschn. 6.2).
- Älteres ALPHA2-Datenheft: Display umschaltbar „aktuelle Leistungsaufnahme in Watt“ / „aktuelle Förderstrom in m3/h“ (loebbeshop-Datenheft, S. 9) – d. h. je nach Baujahr kann die Pumpe sogar den Förderstrom anzeigen.

**ALPHA2 GO** – Display kann W, Förderhöhe m, Förderstrom m³/h und Fehlercode zeigen; „Die LEDs zeigen die Regelungsart, die Einstellung und den Betriebsstatus an.“ (S. 13, heizungsdiscount24-PDF)

**UPM3 (1 Taste, 5 LEDs: LED1 grün/rot, LED2–5 gelb)** – renewableheatinghub-PDF (Datenheft)
- Kurz drücken = Anzeige der Einstellung: „The settings view shows which mode controls the pump.“
- Im Betrieb: „The four yellow LEDs indicate the current power consumption (P1).“
- Störung: „the bicoloured LED 1 switches from green to red.“
- Einstellung ändern nur 2–10 s halten (wenn entsperrt); >10 s = Tastensperre umschalten. → **der Betreiber soll nur kurz drücken!**
- Oilon-Blatt UPM3 AUTO: CP-AUTOADAPT aktiv „when the second LED from the left is green“ (Oilon-PDF, URL s. o.). Die genaue LED-Zuordnung PP1–3/CP1–3/CC1–4 ist im Extrakt nicht sauber erhalten (siehe „nicht gefunden“).

### 1.4 Volumenstrom-Formel FBH

- Danfoss-Datenblatt SSM-Verteiler: Durchfluss [l/h] = W/m² × m² / (ΔT × 1,16); Beispiel 50 W/m² × 25 m² bei 5 K ≈ 216 l/h. – https://assets.danfoss.com/documents/84735/AI195986472412de-DE0401.pdf
- haustechnikdialog SHK-Wissen: „V = (Q · 0,86) / (θV – θR)“; für stark belastete Kreise „relativ enge Spreizung von z. B. 5 K“; Kreis-Druckverlust ohne Armaturen „2 mWS nicht übersteigen“. – https://www.haustechnikdialog.de/SHKwissen/818/Berechnung-des-Rohrnetzes-Fussbodenheizung

### 1.5 Heizkreis-Volumenstrom > WP-/Speicherkreis-Volumenstrom (Parallelpuffer)

- energiesparhaus-Forum (dyarne, 3.1.2026): bei größerem Sekundärstrom „kann nicht alles zur wärmepumpe zurück drücken“; Puffer wirkt als Mischer: „wertvoller vorlauf wird heruntergemischt.“ WP muss „höher raufdrücken als es die heizkreise eigentlich benötigen“; Faustzahl „4K kosten 10% COP, 10K kosten 25% COP“. – https://www.energiesparhaus.at/forum-wp-puffer-liebe-oder-hass-teil-ii/84533 (Forum, keine Norm)
- elektronik-zeit.de: am Heizkreis kommt „nur eine Mischtemperatur von 32 oder 30 °C an“ (statt 35); „rund 10 bis 12 Prozent COP-Verlust pro 5 Kelvin“. – https://elektronik-zeit.de/waermepumpe/reihenpuffer-trennpuffer-vergleich/
- ingenieur.de / Wolf: 1 K weniger Vorlauf bei L/W-WP → „Effizienz der Anlage um etwa 2 bis 2,5 Prozent steigern“. – https://www.ingenieur.de/technik/fachbereiche/gebaeudetechnik/waermepumpe-optimal-einstellen-vorlauftemperatur-und-pufferspeicher-beachten/

### 1.6 Hydraulischer Abgleich bei Einzelraumregelung

- suissetec Merkblatt „Hydraulischer Abgleich in neuen Heizungsanlagen“: „In Anlagen, z. B. mit Einzelraumregulierungen, sind automatische Durchflussregler einzubauen“; mehr Förderhöhe „bringt so gut wie nichts“; FBH bei −50 % Volumenstrom: „steht immer noch 85 % der Wärmeleistung zur Verfügung“. – https://merkblatt.suissetec.ch/de-CH/HEIZ203/file/HEIZ203.pdf
- Danfoss: „Der hydraulische Abgleich ist entscheidend für das Erreichen der Komforttemperatur“ (URL s. 1.4).
- Praxis-Vorgehen Forum (cacer, energiesparhaus 2/2025): „erstmal alle Kreise voll geöffnet“; „so wenig drosseln wie möglich, aber so viel wie nötig“; Kreise mit höherem RL stärker drosseln. – https://www.energiesparhaus.at/forum-hilfe-bei-der-einstellung-meiner-fbh-mit-waermepumpe/81866_1

---

## 2. WAHRSCHEINLICH (abgeleitet, eigene Rechnung/Fachlogik)

- **Konstantdruck (CP1 bzw. CP-AUTOADAPT) ist für deine beiden FBH-Kreise die passende Regelart.** Begründung: Druckverlust sitzt fast nur in den FBH-Schleifen + Verteiler (Pumpe sitzt direkt an Mischer/Verteiler, kurze Zuleitung) → genau der Fall, den Xylem/Grundfos für Konstantdruck nennen. Mit Loxone-Stellantrieben: schließen einzelne Räume, hält CP den Differenzdruck am Verteiler → die offenen Räume behalten ihren abgeglichenen Durchfluss. Bei Proportionaldruck sinkt die Förderhöhe beim Schließen → offene Räume bekommen weniger Durchfluss als abgeglichen (Effekt klein bei FBH, vgl. suissetec 50 %/85 %).
- **Fixe Drehzahlstufe (I/II/III bzw. CC)** ist bei Einzelraumregelung am ungünstigsten: Schließen Räume, steigt der Differenzdruck an den offenen Kreisen (Geräusche, Überversorgung, steigende Mischtemperatur im Puffer).
- **Wirkung auf Spreizung/Puffer/WP-Rücklauf:** Höhere Förderstufe → mehr Durchfluss → kleinere Spreizung im HK (z. B. 3 K statt 5–7 K) → höherer Heizkreis-RL in den Puffer, aber vor allem: Summe HK-Durchfluss kann den Speicherkreis-Durchfluss überholen → Puffer mischt RL in den VL → Mischer (HK1) macht weiter auf bzw. HK2 bekommt kälteren VL → Regler verlangt höheren WP-Vorlauf → COP sinkt (Größenordnung 2–2,5 %/K, Quellen 1.5).
- **Faustrechnung für dich (nicht gemessen!):** 100 m² × 40 W/m² = 4 kW je Stockwerk.
  - Spreizung 5 K: 4000 / (1,163 × 5) ≈ 690 l/h ≈ **11,5 l/min je Kreis**, beide ≈ 23 l/min.
  - Spreizung 7 K: ≈ 490 l/h ≈ **8,2 l/min je Kreis**, beide ≈ 16 l/min.
  - Bei 60 W/m² und 5 K: ≈ 17 l/min je Kreis, beide ≈ 34 l/min = Speicherkreis-Niveau → Grenzfall.
  - → Mit 5–7 K Spreizung bleibt die Summe der Heizkreise deutlich unter ~34 l/min Speicherkreis. Risiko entsteht praktisch nur, wenn Pumpen auf hoher Fixstufe/CP-max laufen und die Spreizung auf 2–3 K zusammenfällt.
- **Ziel-Indikator ohne Durchflussmesser:** HK-Spreizung (VL nach Mischer – RL) 5–7 K bei Dauerlast; Puffer oben ≈ WP-VL (kein Heruntermischen); Leistungsaufnahme der Pumpe bei Teillast niedrig (einstellige bis niedrige zweistellige Watt bei ALPHA2/UPM3 – nur Erfahrungswert, nicht belegt).
- **HK1 (Mischer) vs. HK2:** Beim Mischerkreis ist der Effekt „zu viel Durchfluss“ teils durch den Mischer gedämpft (Rückführung aus eigenem RL), beim direkten Kreis HK2 schlägt er voll auf den Puffer durch. Ob HK2 wirklich ungemischt ist: **noch zu prüfen**.

---

## 3. NICHT GEFUNDEN / OFFEN

- Offizielle Hoval-Textstelle zur Regel „Heizkreis-Durchfluss ≤ Speicherkreis-Durchfluss“ in dieser Recherche nicht verifiziert (Regel aus Projektkontext übernommen).
- Exakte LED-Muster des UPM3 für PP1–3 / CP1–3 / CC1–4: Tabelle im PDF-Extrakt verloren. Bedeutung bei des Betreibers Pumpe am Foto + Typenschild (Variante: UPM3 AUTO, UPM3 AUTO L, UPM3 Hybrid haben unterschiedliche Menüs!) zu klären.
- Öffentliche Grundfos-Seite mit expliziter Aussage „Mischerkreis + Stellantriebe → CP“: nicht gefunden; nur über FBH-Empfehlung und Druckverlust-Logik abgeleitet.
- BFE/Fraunhofer-Feldtest-Zahl speziell zu Heizkreispumpen-Regelart vs. JAZ: nicht gefunden.
- haustechnikdialog-Forumsseiten (robots-gesperrt) nicht abrufbar.
- ALPHA3: nicht gesondert recherchiert (Bedienung per App/GO, keine Endkunden-LED-Logik relevant).

---

## 4. WAS BRINGT UNS DAS

1. Klare Soll-Einstellung: beide FBH-Pumpen auf **Konstantdruck** (CP1 als Start, CP2 nur wenn Räume nicht warm werden) oder CP-AUTOADAPT; **keine Fixstufe III**.
2. Prüfgröße für Effizienz ist die **Spreizung je Heizkreis (5–7 K)** und ob der Puffer den WP-Vorlauf herunter mischt – nicht die Pumpenstufe an sich.
3. Rechnerisch liegen die zwei Kreise bei 5–7 K Spreizung mit ~16–23 l/min klar unter ~34 l/min Speicherkreis → die Hoval-Regel ist im Normalbetrieb erfüllbar, aber nur mit moderater Pumpeneinstellung.
4. Loxone-Einzelraumregelung ersetzt den Abgleich nicht: erst Abgleich mit allen Stellantrieben offen, dann Loxone regeln lassen. Holzofen-Raum (UG) nicht komplett zufahren lassen, sonst kühlt der Estrich aus (siehe Projektwissen).
5. Wenn HoxPi/Hoval VL-/RL-Werte je HK liefern: Spreizung lässt sich direkt loggen → objektiver Vorher/Nachher-Test bei Pumpenumstellung.

---

## 5. WAS DU AN DER PUMPE NUR ABLESEN/FOTOGRAFIEREN SOLLST

Bitte **nichts umstellen**, nur dokumentieren – je Pumpe (HK1 Mischerkreis, HK2):

1. **Typenschild** komplett scharf fotografieren (Typ z. B. „ALPHA2 25-60“, „UPM3 AUTO L 25-70“, Produktnummer, Baujahr/PC-Code).
2. **Bedienfeld im Ruhezustand** fotografieren: welche Leuchtfelder/LEDs leuchten, welcher Wert steht im Display (Watt? m³/h?).
3. **Nur bei UPM3:** Taste **einmal kurz** drücken (nicht halten!) → LEDs zeigen ca. 2 s die aktive Einstellung → genau dann fotografieren oder kurzes Video. Halten ≥2 s würde in den Einstellmodus wechseln.
4. **Bei ALPHA2:** NICHT drücken – die Einstellung ist dauerhaft über die Leuchtfelder sichtbar (AUTOADAPT / PP1 / PP2 / CP1 / CP2 / I / II / III); jeder Druck schaltet sofort weiter. Nachtabsenkungs-Feld mitfotografieren.
5. **Leistungsaufnahme / Förderstrom** ablesen (Display bzw. gelbe LEDs beim UPM3) – einmal, wenn viele Räume offen sind, einmal, wenn die meisten Loxone-Stellantriebe zu sind.
6. Gleichzeitig am Verteiler: **Durchflussanzeiger** (falls vorhanden, Schaugläser l/min) je Kreis fotografieren und VL/RL-Thermometer am Verteiler bzw. Hoval-Anzeige HK-Vorlauf.
7. Notieren: Uhrzeit, Außentemperatur, ob Holzofen gerade läuft.

Daraus lässt sich dann sicher sagen, welche Regelart aktiv ist, und mit VL/RL je Kreis, ob der Durchfluss zu hoch ist.