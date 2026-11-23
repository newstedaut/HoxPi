# FUND Loxone Klima Controller: demandHeat / threshold / currentStatus (F59) – 01.11.2026
Recherche-Subagent, nur öffentliche Seiten, nur gelesen. Nichts an Loxone, HoxPi oder Anlage geändert.
Ergänzt `[lokaler Pfad]` (Sot 30 %, MinHr 0, ϑd 1,5 K, LimH/LimC dort schon belegt, hier nicht wiederholt).

## Frage
Was bedeuten am Klima Controller (API-Typ `ClimateControllerUS`) die Zustände `demandHeat` (25), `threshold` (30), `stage` (0), `maximumTempHeating` (17), `minimumTempCooling` (19), `mode` (2), `outdoorTempMode` (1), `currentStatus` (8192) und `controls[].demand`? Schaltet der Controller erst bei demandHeat ≥ threshold, mit Hysterese oder Mindestlaufzeit? Anlass: WP-Heizlauf endete 01.11.2026 17:19 nach 14 min, gleichzeitig HK1-Soll (Reg 1490) = 0; 18:56: 3 von 8 Räumen demand=1, demandHeat 25, threshold 30, stage 0.

## Ergebnis – belegt
Hauptquelle: offizielle Loxone-API-Doku „Structure File“ Version 17.1, https://www.loxone.com/dede/wp-content/uploads/sites/2/2021/10/1701_Structure-File.pdf, Abschnitt `ClimateControllerUS` (seit Miniserver 12.1). Dort steht in `details.ctype` (seit 15.1), dass derselbe Typ als „Climate Controller“ oder „HVAC Controller“ visualisiert wird → unser Klima Controller UG meldet sich deshalb als ClimateControllerUS. (sicher)

| Zustand | live | Bedeutung laut Structure File 17.1 |
|---|---|---|
| `demandHeat` | 25 | Heizanforderung aller Raumregler zusammen, in Prozent 0–100 |
| `threshold` | 30 | Mindest-Anforderung in % (0–100), ab der Heizen/Kühlen startet = Parameter Sot |
| `stage` | 0 | aktive Stufe: 0 = aus, 1 = Stufe 1, 2 = Stufe 2 → um 18:56 **heizt der Controller nicht** |
| `mode` | 2 | 0 aus, 1 Heizen+Kühlen, 2 **nur Heizen**, 3 nur Kühlen (Achtung: API-Zählung, nicht die Parameter-Zählung Mode −1…2 im Baustein) |
| `outdoorTempMode` | 1 | 0 nicht verwendet, 1 **48-h-Mittel der Vergangenheit**, 2 Systemvariable „erwartete 48 h“, 3 aktuelle Außentemp. |
| `maximumTempHeating` | 17 | max. (Außen-)Temperatur, bei der Heizen erlaubt ist = ϑLimH = **17 °C** (Standard wäre 18) |
| `minimumTempCooling` | 19 | min. Temperatur, ab der Kühlen erlaubt ist = ϑLimC = **19 °C** (Standard wäre 15) |
| `controls[].demand` | 0/1 | je verknüpfter Intelligenter Raumregelung: −1 Kühlen, 0 keine, 1 Heizen (nur Richtung, kein Betrag) |

### currentStatus = 8192 (sicher)
Bitmaske, im Structure File **ab 1 nummeriert** (Bit 1 = Wert 1 … Bit 14 = Wert 8192). 8192 = 2^13 = **nur Bit 14 gesetzt = „Heating demand but too less“** → Heizbedarf vorhanden, aber unter der Einschaltschwelle. Passt exakt zu demandHeat 25 < threshold 30 und stage 0.
Weitere Bits (Wert in Klammern): 1 Heizen Stufe 1 aktiv (1), 2 Heizen Stufe 2 (2), 3 Notheizung (4), 4 Kühlen Stufe 1 (8), 5 Kühlen Stufe 2 (16), 6 Umschalten auf Kühlen (32), 7 Umschalten auf Heizen (64), 8 verzögert durch Umschaltventil (128), 9 verzögert durch Lüfternachlauf (256), 10 verzögert durch Mindest-Aus-Zeit (512), 11 Heizbedarf aber außen zu warm (1024), 12 Kühlbedarf aber außen zu kalt (2048), 13 Kühlbedarf zu gering (4096), 14 Heizbedarf zu gering (8192).
Gegencheck: Beim alten Typ `ClimateController` gibt es analog `standbyReason` 2 = Anforderung unter Schwelle (gleiche PDF). Die Werte in Klammern sind von mir aus der 1-basierten Zählung umgerechnet; wäre die Zählung 0-basiert, hieße 8192 „Kühlbedarf zu gering“ – das passt bei mode 2 (nur Heizen) nicht, daher sicher Bit 14.

### Berechnung von demandHeat (belegt, zwei Quellen)
- Klima Controller (EN, https://www.loxone.com/enen/kb/climate-controller/): Start nur, wenn die **durchschnittliche Ventilöffnung** der Raumregler Sot übersteigt; Raumbedarf für die Heiz/Kühl-Wahl = (Soll − Ist) × Raumfläche.
→ demandHeat ist **kein Zähler „x von 8 Räumen“**, sondern ein flächengewichtetes Mittel der Ventilöffnungen. 3 von 8 Räumen hätte ungewichtet 37,5 % ergeben, live waren es 25 %.

### Hysterese / Mindestlaufzeit (belegt, soweit dokumentiert)
- Eine Hysterese um die Einschaltschwelle ist in **keiner** der Quellen dokumentiert (Structure File, Klima-Controller-KB, HVAC-KB). Die einzigen Zeitglieder: MinHr (Mindestlaufzeit, Std. 0 min), 3 min Sperre nach Abschalten zusätzlich zu Fod, Pulsbetrieb MaxTp (Std. aus).
- IRR-Doku DE (https://www.loxone.com/dede/kb/intelligente-raumregelung/, schon in Teil 2): wird die Einschaltschwelle unterschritten, kann eine Mindestöffnung erzwungen werden, bis die Mindestlaufzeit abgelaufen ist und das Gerät ausschaltet → Unterschreiten von Sot im Lauf **führt zum Ausschalten**, verzögert nur um MinHr.

## Ergebnis – wahrscheinlich
- **Ein-/Aus an derselben Schwelle:** Weil keine Hysterese dokumentiert ist und die IRR-Doku das Ausschalten nach MinHr beschreibt, schaltet der Controller mit hoher Wahrscheinlichkeit ein bei demandHeat > Sot und aus, sobald demandHeat < Sot fällt – bei MinHr = 0 **sofort**. Wiedereinschalten frühestens nach 3 min + Fod und erst wieder über 30 %.
- **Rückkopplung:** Läuft die WP, schließen Räume, die Soll erreichen, ihre Ventile → flächengewichtetes Mittel sinkt unter 30 % → Controller aus. Ein kurzer Lauf (14 min) ist damit plausibel, wenn demandHeat beim Start nur knapp über 30 % lag.
- `maximumTempHeating` 17 / `minimumTempCooling` 19 mit `outdoorTempMode` 1: zwischen 17 und 19 °C 48-h-Mittel weder Heizen noch Kühlen (Totband) – entspricht dem Umbau vom 23.10.2026 gegen die Kühlfalle. Am 01.11. um 18:56 blockiert das nicht: Bit 11 (außen zu warm) war nicht gesetzt (sicher aus 8192); Wert des 48-h-Mittels selbst nicht geprüft.

## Ergebnis – nicht gefunden
- Genaue Formel von demandHeat (Ventilöffnung analog oder nur 0/100 %? Raumfläche aus welchem Feld? Mittel über alle 8 Räume oder nur über Räume mit Heizbedarf?). Nicht dokumentiert.
- Hysterese/Abschaltschwelle unter Sot, Verhalten bei Unterschreiten im Lauf außerhalb der IRR-Notiz.
- Loxforum (DE) 364244 „Unzureichender Heiz- oder Kühlbedarf“, 477528 „Loxone Log Klimacontroller“, 310713, 375420: aus der Cloud nicht erreichbar (client_error). `https://www.loxone.com/dede/kb/klima-controller/` und `/dede/kb/hvac-controller/`: ebenfalls client_error, EN-Fassungen gelesen.
- Ein Zustand „Mindestlaufzeit“ existiert in der API nicht; nur Parameter-Bit „minimum off time“ und Status-Bit 10.

## Bedeutung für die Anlage
- **Zustand 18:56 (sicher aus API-Doku):** Klima Controller UG steht in Standby, Grund „Heizbedarf zu gering“ (Bit 14), weil demandHeat 25 % < threshold 30 %. stage 0 = Ausgang H aus.
- **Heizlauf-Ende 17:19 (wahrscheinlich):** Wenn die 1490-Logik in Loxone vom Klima-Controller-Ausgang H (oder stage > 0) abhängt, erklärt demandHeat < 30 % bei MinHr = 0 das sofortige Ende nach 14 min und HK1-Soll = 0. Teil 1/2 ging davon aus, dass H nicht zur WP verdrahtet ist – das gleichzeitige Fallen von 1490 auf 0 spricht dagegen. **Prüfen** (nur lesen): in Loxone Config, woher AQ 1490 seine 0 bekommt; per Loxone-MCP `control_history` den Verlauf von demandHeat, currentStatus und stage um 17:00–17:25 lesen. Erst die Messung entscheidet.
- **Hebel (nur Vorschlag, der Betreiber entscheidet, nichts umgesetzt):**

| # | Vorschlag | erwartete Wirkung | Sicherheit |
|---|---|---|---|
| 1 | MinHr am Klima Controller UG von 0 auf z. B. 60–120 min | Lauf bleibt nach Start mindestens MinHr an, IRR halten Mindestöffnung | sicher (Funktion), wahrscheinlich (Wirkung) |
| 2 | Sot von 30 auf z. B. 15–20 % senken | Start und Halten auch bei 2–3 offenen Räumen; bei FBH mit trägem Estrich unkritisch | wahrscheinlich |
| 3 | Alternativ 1490 nicht an H/stage koppeln, sondern Heizkurve dauerhaft liefern und WP-Takt über Hoval-Hysterese laufen lassen | Loxone-Schwelle wirkt nicht mehr als Ein/Aus | Vermutung (Verdrahtung unbekannt) |
| 4 | Wirkung messen: Starts/Tag, Laufdauer, demandHeat-Verlauf 7 Tage vorher/nachher | Messung statt Theorie | – |

## Quellen (geprüft)
1. https://www.loxone.com/dede/wp-content/uploads/sites/2/2021/10/1701_Structure-File.pdf (Structure File 17.1, Hauptbeleg, nur gelesen)
2. https://www.loxone.com/dede/wp-content/uploads/sites/2/2021/03/1200_Structure-File.pdf (12.0, nur ClimateController ohne US)
3. https://www.loxone.com/dede/wp-content/uploads/sites/2/2016/08/loxone-structure-file.pdf (8.1, kein Klima Controller)
4. https://www.loxone.com/enen/kb/climate-controller/
5. https://www.loxone.com/enen/kb/hvac-controller/
6. https://www.loxone.com/dede/kb/intelligente-raumregelung/ (aus Teil 2, Bezug)
7. https://www.loxforum.com/forum/software-configuration-user-interface/375307-intelligent-room-controller-gen1-keeps-activating-my-heat-pump (nur Gen1, nicht übertragbar)
Nicht erreichbar: https://www.loxone.com/dede/kb/klima-controller/ ; https://www.loxone.com/dede/kb/hvac-controller/ ; Loxforum 364244, 477528, 310713, 375420 (Links in WebSearch, client_error).