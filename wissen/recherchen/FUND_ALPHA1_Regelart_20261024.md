# FUND: Grundfos ALPHA1 25-60 180 (HK1) – Regelart laut Anzeige (Katalog F10, Recherche 24.10.2026 07:00)

Auftrag: Orchestrator, Rechercheagent (WebSearch/WebFetch, nur öffentliche Seiten). Stichprobe selbst gegengelesen (siehe unten).
Anzeige an der Pumpe (BAUTEILE_BEKANNT.md): **rechtes Kennlinien-Symbol + alle 3 Balken, 28 W**.

## 1. Belegt
- **Drei Generationen, unterschiedliche Bedienung:**
  - ALPHA1 alt (Datenheft 12.2013, 25-60 180 = Prod.-Nr. [Nummer]): Watt-Display, 7 Leuchtfelder PP1, PP2, CP1, CP2, I, II, III; Werk PP2; P1 25-60 = 5–45 W. https://www.heizungsdiscount24.de/pdf/Grundfos-Alpha-1-EU-Datenblatt.pdf (S. 7, 9–10, 14, 16)
  - **ALPHA1 Model B:** Watt-Display, „nine light fields“; Tastenfolge ab Werk PP2 → PP3 → CP1 → CP2 → CP3 → III → II → I → PP1; P1 XX-60 = 3–34 W; FBH-Empfehlung „constant-pressure curve, CP1, CP2 or CP3“, Alternative Konstantkurve I–III; „Model B“ steht auf Typenschild/Verpackung. https://magento.waterpompshop.nl/media/wysiwyg/manual/5711495722845.pdf (S. 8, 10, 12, 20) – **selbst per WebFetch gegengelesen 24.10. 07:1x: Reihenfolge, 3–34 W und FBH-Empfehlung bestätigt.**
  - ALPHA1 L: kein Watt-Display (nur LEDs, Leistung nur über PWM-Rückmeldung). https://tm.by/sites/default/files/content/pf/202303/f568610.pdf (S. 11–12) → **unsere Pumpe (zeigt 28 W) ist keine ALPHA1 L (sicher).**
- Alte ALPHA1 deutsch: FBH-Empfehlung „Untere Konstantdruck-Kennlinie (CP1)“, Alternative CP2. https://homeperfect.de/media/4f/50/ae/1694524372/ALPHA1_Grundfos_Betriebsanleitung_web.pdf (S. 11–12)
- Konstantkurve III = Maximalkurve, u. a. zum Schnellentlüften. https://tfpumps.com/resources/grundfos/Grundos_Alpha_Datasheet_B_compressed.pdf (S. 11)
- AUTOADAPT gibt es bei keiner ALPHA1-Generation (nur ALPHA2).

## 2. Wahrscheinlich
- **Unsere Pumpe ist eine ALPHA1 Model B:** Watt-Display, 3 Balken je Regelart (PP1–3/CP1–3/I–III); 28 W unter dem Maximum 34 W.
- **Rechtes Symbol = Konstantkurve (feste Drehzahl)**, Reihenfolge der Symbole im Bedienfeld PP – CP – Konstantkurve (in allen Anleitungen so gelistet; Lage nur in Abbildungen, nicht als Text lesbar).
- → **Anzeige = Konstantkurve/Drehzahlstufe III (Maximaldrehzahl, ungeregelt).** 28 W nahe Vollausschlag stützen das; PP1/CP1 lägen deutlich tiefer.

## 3. Nicht gefunden
- Wörtlicher Beleg, welches Symbol links/Mitte/rechts sitzt (nur Grafik Abb. 14 Model B; Grundfos-Original-PDFs api.grundfos.com nur binär).
- Förderhöhe je Stufe in m, P1 je Einstellung für die EU-25-60, Prod.-Nr. Model B 25-60 180 (nur 25-60 N = 99199593 belegt).

## 4. Urteil
- **Bisheriger Eintrag „sehr wahrscheinlich Konstantdruck höchste Stufe“ ist wahrscheinlich falsch – wahrscheinlich Konstantkurve III.** Sicherheit: wahrscheinlich (Symbollage nicht textlich belegt).
- Grundfos empfiehlt für FBH Konstantdruck (CP1–CP3 Model B, CP1 alte Generation) – belegt. III ist für FBH mit Stellantrieben nicht vorgesehen.
- **Was bringt uns das:** Mit CP1/CP2 statt III sinkt der Pumpenstrom (Vermutung 5–15 W statt 28 W, ~0,1–0,2 kWh/Tag Heizsaison) und die Stellantriebe arbeiten gegen konstanten statt steigenden Druck. Volumenstrom HK1 heute ~16 L/min (F18) – nach Umstellung neu messen (31708 bei HK1 ohne Verdichter).
- **Zum Abschließen (fertig, wenn):** Typenschild ablesen („Model B“? P1 max 34 W oder 45 W?) und die Symbollage gegen Abb. 14 der Model-B-Anleitung prüfen. `Fotos_Album\_index.txt` enthält nur URLs ohne Beschreibung – kein Typenschildfoto auffindbar. Umstellen nur durch der Betreiber (Taste an der Pumpe, Rückweg: Taste bis wieder rechtes Symbol + 3 Balken).


## Nachtrag OR 24.10.2026 15:30 – Foto aus dem eigenen Album (Regel „erst selbst nachsehen“)
- Fundort: `[lokaler Pfad]` (Kontaktbogen-Nr. 10, Skript `[lokaler Pfad]`), zweites Foto `gp_9UW33XBBtT7G4e3r.jpg` (HK1 und HK2 nebeneinander).
- **Sichtbar (sicher):** Aufdruck „ALPHA1 25-60 180“, „D-A-CH“; Anzeige 28 W (zweites Foto 22 W); links drei dunkle Felder „III II I“; rechts drei Balken (alle grün) und zwei Symbole: links Viertelkreis mit schräger Linie (dunkel), rechts Viertelkreis mit **waagrechter** Linie (grün).
- **Deutung (wahrscheinlich, nahe sicher):** schräge Linie = Proportionaldruck, waagrechte Linie = Konstantdruck (Grundfos-Piktogramme); Konstantkurve I–III sind die Textfelder links. → Einstellung **CP3**, nicht Konstantkurve III. Die Aussage oben „rechtes Symbol + 3 Balken = Konstantkurve III“ ist widerlegt.
- **Folge:** CP3 liegt in der Grundfos-FBH-Empfehlung (CP1–CP3). Hebel „CP2 oder CP1“ (weniger Pumpenstrom, etwas weniger Durchfluss) bleibt des Betreibers Entscheidung; vorher Volumenstrom 31708 im Heizbetrieb als Bezug notieren.
- Offen (gering): Typenschild „Model B“ / P1 max nicht abgelesen; für die Regelart nicht mehr nötig.