# FUND: TopTronic E / UltraSource: Heiz-Schaltdifferenz, Takten, WW-Vorrang (Web-Recherche 2026-10-23)

Anlage: UltraSource B comfort C17, TopTronic E, FBH, EnerVal 300 Puffer (282,4 l), CombiVal ESR 400 WW (~379 l) [Korr. 23.10.2026: Rollen waren vertauscht].
Befund vor Ort: Heizlauf endet bei Rücklauf ca. +2,5 K über Soll; WW-Ladungen unterbrechen Heizläufe.
Quellenlage: Keine öffentliche Hoval-Doku mit diesen Parametern gefunden (Hoval-Katalog-PDFs ohne Regelungsdetails, eines nicht abrufbar).
Alle Parameterbelege unten stammen aus Nutzerforen (energiesparhaus.at) mit Displaytext-Abschriften. Das sind keine Herstellerangaben.

## 1. BELEGT (wörtliches Zitat + URL)

**Heiz-Schaltdifferenz = 33-053 / 33-054, nicht nur Modulation**
- „Ausschaltdiff. DK/WPF Heizen (CRF/WPF) "33-053" = 1.0K“ / „Einschaltdiff. DK/WPF Heizen (CVF/WPF) "33-054" = 2.5K“
  (ffischer, 16.02.2020; am 18.02.2020: „"33-053" = 0.2K“) https://www.energiesparhaus.at/forum/56645
- Andere Anlage: „"33-053" = 2.0K“ und „"33-054" = 3.0K“ (Domi90, 30.11.2023)
  https://www.energiesparhaus.at/forum-hoval-ultrasource-lwp-allgemeiner-austausch-und-anlage-optimieren/56645_2
- Bezug: „4k Abschaltdifferenz bedeutet, dass die Wärmepumpe abschaltet“, wenn Rücklauf 4 K über VL-Soll liegt. Einschalten: „bei einer VL Ist unter 8k VL Soll wieder einschaltet“. „als Referenz dient die Vorlauftemp SOLL“
  (MSC1, 11.12.2022, UltraSource T comfort 13) https://www.energiesparhaus.at/forum/70426
- Kühl-Gegenstück: „Ausschaltdiff. DK Kühlen (CVF) "33-061"“, „Einschaltdiff. DK Kühlen (CRF) "33-062"“ (ohne Werte)
  https://www.energiesparhaus.at/forum-hoval-ultrasource-b-comfort-11-optimierung-kuehlt-nicht/85791_1
- Wirkung laut Nutzer: „Kleinere Hysterese = mehr Starts.“ (ffischer, 18.02.2020) https://www.energiesparhaus.at/forum/56645

**Stehzeit einstellbar**
- „Zusätzlich muss auch eine Mindest Verdichter Stehzeit abgelaufen sein (auch einstellbar)“ (MSC1, 10.12.2022)
  https://www.energiesparhaus.at/forum/70426 (Parameternummer nicht genannt)

**Weitere Parameter mit Taktbezug (Forenangaben)**
- „Max. Sollwertsteigung Heizbetr. (K/min) "06-017" = 1,0“, „... WW Betrieb ... "06-018" = 3,0“ (56645, 56645_2)
- 07-001 „WEZ Überhöhung/Abschlag Vorlauf“ von 2 K auf 1 K gesenkt (Domi90, 11.12.2023) https://www.energiesparhaus.at/forum/75450_2
- „Max. Leistung Heizen "34-049" 42%“ (MSC1, 16.02.2020) https://www.energiesparhaus.at/forum/56645
- „CP Mindrehzahl "33-327" = 60%“; 33-328 CP-Drehzahl/dT (widersprüchlich zugeordnet) (56645, 56645_3)
- Abtauung zählt mit: „Die Abtauvorgänge werden tatsächlich als Schaltvorgänge gezählt.“ (sharknz, 09.02.2022) .../56645_2
- 33-320 „Abtauung Abweichungsgradminuten“ = 45 kmin. Gradminuten gibt es laut Fund nur für die Abtauung, nicht als Heiz-Startkriterium.

**WW-Zeitprogramm existiert (Nutzerpraxis)**
- „Warmwasser wird einmal in der Früh um 5:00 erwärmt auf 45Grad“, ein Techniker „hat Warmwasser auf einmal pro Tag eingestellt“
  (JohnyBravo, 09.12.2022) https://www.energiesparhaus.at/forum/70426

**Fachliteratur Takten (allgemein, nicht Hoval)**
- „Schon 2 Kelvin mehr Hysterese verlängern jeden Lauf um rund zwei Drittel.“ „Ein Pufferspeicher verlängert Laufzeiten nur, wenn er groß genug ist und richtig eingebunden wird.“ Richtwert: bis 2.000 Starts/Jahr gelten als unauffällig. https://42watt.de/magazin/taktung-warmepumpe

## 2. WAHRSCHEINLICH (abgeleitet, nicht belegt)
- Der Abbruch bei Rücklauf ca. +2,5 K passt zu **33-053 (Ausschaltdiff., Fühler CRF = Rücklauf)**. Bei dir steht dort vermutlich 2,0 bis 2,5 K. 33-054 (Einschalt, CVF = Vorlauf) legt fest, wann sie wieder startet.
- „DK/WPF“ heißt vermutlich Direktkreis / Wärmepumpen-Pufferfühler. Bei Pufferbetrieb (06-050) beziehen sich dieselben 33-053/054 dann wohl auf den Pufferfühler statt auf CRF/CVF. Das ist eine Vermutung aus dem Displaytext.
- Bezug ist das VL-Soll aus Heizkurve plus 07-001 Überhöhung, nicht das Raumsoll. Mehr Überhöhung (07-001) verschiebt den Abschaltpunkt nach oben, und zwar bei gleicher Hysterese.
- Bei einer Heizlast von 3–5 kW und 7,4 kW Mindestleistung hilft nur, mehr Energie pro Takt zu speichern: größere 33-054 plus Puffer als Speicher. Feinere Modulation geht nicht, 34-050 ist schon am Boden.

## 3. NICHT GEFUNDEN (öffentlich)
- Werkswerte und Einstellbereiche von 33-053/33-054 (die Forenwerte 0,2 / 1,0 / 2,0 / 3,0 K bzw. 2,5 / 3,0 K sind Installateur- oder Nutzerwerte).
- Parameternummer für Mindeststehzeit und Kompressor-Mindestlaufzeit, Heiz-Gradminuten oder Integral als Startkriterium.
- Parameter, mit dem sich der WW-Vorrang abschalten lässt, oder ein Parallelbetrieb Heizen/WW. Bei Einkreis-WP mit Umschaltventil wäre das physikalisch auch nicht möglich, Vorrang ist dort systembedingt.
- Puffer-Schaltdifferenz 06-xxx (außer [Nummer]) und Unterschied 1-Fühler/2-Fühler-Pufferregelung.
- Offizielle Hoval-Empfehlung gegen Takten bei Überdimensionierung (Hoval verlangte laut Nutzern Mindestdurchfluss bzw. 40-l-Puffer im Rücklauf, siehe 75450_1 und 85791_1).

## 4. Was bringt uns das
- Stellhebel Nr. 1 ist **33-054 (Einschaltdiff.)**: Wird er größer, startet sie später und es kommen weniger Starts. Den Laufabbruch bestimmt **33-053**. Mehr Ausschaltdifferenz heißt längere Läufe, aber höherer RL und VL, also schlechtere COP.
- Bei aktivem Puffer (06-050) zählen dieselben Differenzen am Pufferfühler. 400 l x 5 K ergeben ca. 2,3 kWh je Takt [⚠ Korr. 23.10.2026: Puffer hat 282,4 l, nicht 400 l], das sind rund 18 min Laufzeit bei 7,4 kW. Erst eine größere Pufferhysterese bringt richtig lange Läufe.
- WW-Unterbrechungen: Ein abschaltbarer Vorrang wurde nicht gefunden. Der praktikable Weg ist das WW-Zeitprogramm, also 1–2 Ladefenster am Tag (z. B. Mittag mit PV und hoher Außentemperatur) statt ständiger Freigabe, dazu 05-000 nicht zu klein.
- Starts und Laufzeit getrennt nach Heizen/WW/Abtauen zählen, bevor etwas geändert wird.
  (Zur Puffer-Rechnung: Die 18 min gelten ohne gleichzeitige Abnahme. Läuft die FBH mit 4 kW mit, reicht es für ca. 40 min.)

## 5. Ablese-Aufträge für der Betreiber (NUR LESEN, nichts verstellen)
1. 33-053 und 33-054 am Bedienteil: Wert, Bereich (min/max) und Werkswert, falls angezeigt. Klartext genau abschreiben (DK/WPF, CRF/CVF).
2. 33-061 und 33-062 (Kühlen) zum Vergleich, ebenso 07-001 (WEZ Überhöhung/Abschlag Vorlauf).
3. 06-050 (Puffer aktiv?): Welcher Fühler ist als Puffer- bzw. WP-Fühler zugeordnet (Fühlerbezeichnung)? Alle angrenzenden 06-0xx-Werte mit „Puffer“ oder „Diff“ im Namen.
4. Im Menü 33-xxx nach „Stehzeit“, „Laufzeit“, „Sperrzeit“ und „Mindest“ suchen und Nummer, Wert und Einheit notieren.
5. WW-Zeitprogramm: Wann ist die WW-Freigabe aktiv (Tage, Uhrzeiten)? Und wann der Komfort- bzw. Eco-Sollwert?
6. Betriebsdaten der WEZ: Starts gesamt, Betriebsstunden Heizen, WW und Abtauen, falls getrennt. Zweimal im Abstand von 24 h ablesen, mit Datum und Uhrzeit.
7. Beim nächsten Heizabbruch: VL-Soll, VL-Ist, RL-Ist und Puffertemperatur im Moment des Stopps fotografieren. So lässt sich prüfen, ob der Abbruch bei RL = VL-Soll + 33-053 liegt.