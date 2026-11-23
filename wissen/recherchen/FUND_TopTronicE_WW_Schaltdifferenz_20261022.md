# FUND: TopTronic E – Parameter der WW-Ladung (Schaltdifferenz, Überhöhung, Ladedauer, SmartGrid)

Stand: 22.10.2026 · Web-Recherche (nur öffentliche Seiten, kein Login) · nichts an der Anlage geändert.
Zitate wörtlich; Silbentrennungen aus dem PDF-Umbruch („Warmwasserla-dung“) zusammengezogen.

## Quellen (alle tatsächlich geöffnet)

- **[Q1]** Hoval „Anleitung Kundendiensttechniker Fernwärmemodul TTE-FW“, 4 214 513 / 04 - 06/17, eingebunden in GP-Joule-PDF „Technische Unterlagen Steuerung Hoval“ (178 S.)
  https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
  Seitenangaben unten: **PDF-Seite / gedruckte Seite**.
- **[Q2]** Hoval Herstellerbescheinigung „Smart Grid Fähigkeit der Wärmepumpen“ 4218875 / 07 (21.04.2026), nennt **UltraSource B comfort (8–17)**; S. 2–3 = Auszug Installationsanleitung TopTronic E **4 213 320 / 12, S. 63–64** (Bildseiten, selbst gelesen)
  https://www.hoval.de/medias/4218875-07.pdf?context=bWFzdGVyfHJvb3R8NDQxNjY2fGFwcGxpY2F0aW9uL3BkZnxhR0U0TDJobVpTOHhNRFV6TnpJM05qWXdORFEwTmk4ME1qRTRPRGMxWHpBM0xuQmtaZ3w5YzNkYWViZTFkODMzZDk0NDg0M2VlODU2YmFjNWM0Mzc3ZDJjNTUzZDFlOWE3YzViZmMwOTQzMGEwMWJiZDFj
- **[Q3]** energiesparhaus.at, Thread „Hoval Ultrasource LWP allgemeiner Austausch und Anlage optimieren“ (Nutzerangaben, keine Herstellerdoku)
  https://www.energiesparhaus.at/forum/56645
- **[Q4]** ManualsLib, Hoval TopTronic E KDT GLT-Modul TTE-GLT (EN, 4 214 174 V00), S. 24/25
  https://www.manualslib.com/manual/1573289/Hoval-Toptronic-E.html?page=24
- **[Q5]** ManualsLib.de, Hoval TopTronic E Bedienmodul Bedienungsanleitung, S. 47/48
  https://www.manualslib.de/manual/329892/Hoval-Toptronic-E-Bedienmodul.html?page=48

### Wichtige Einschränkung zu Q1
Q1 ist die KDT-Anleitung des **Fernwärmemoduls TTE-FW**, nicht des WEZ. Die WW-Funktion ist bei TopTronic E ein gemeinsamer Funktionsblock (gleiche Par.-Nummern, z. B. 05-034 = 2,0 K deckt sich mit deiner Live-Ablesung). **Werkseinstellungen können beim TTE-WEZ abweichen** – Beispiel: 05-057 Max. WW-Sollwert = 90 °C in Q1, aber **65 °C** in Q2 (WEZ-Doku).

## A) BELEGT (URL + Seite + wörtliches Zitat)

**A1 – Schaltdifferenz = 05-000 „Einschaltdifferenz Warmwasserbereitung“, Werk 2,5 K, Bereich 0,5…20,0 K** · [Q1] PDF-S. 154 / gedr. S. 130
> „Unterschreitet die Warmwassertemperatur ihren Sollwert um den hier eingestellten Wert, wird eine Warmwasserladung gestartet.“

**A2 – Start/Ende-Logik** · [Q1] PDF-S. 158 / gedr. S. 134
> „Eine Warmwasserladung wird gestartet, wenn der aktuelle Sollwert um die Einschaltdifferenz (05-000) unterschritten wird und endet, wenn der aktuelle Sollwert erreicht wird.“
→ passt zu deiner Beobachtung: Sollsenkung während der Ladung = „aktueller Sollwert erreicht“ = Ladungsende.

**A3 – 05-001 Überhöhung Ladesollwert, Werk 5 K, Bereich −10,0…50,0 K** · [Q1] PDF-S. 154 / gedr. S. 130
> „Mit diesem Parameter kann eine Überhöhung für den Ladesollwert eingestellt werden.“

**A4 – 05-034 Überhöhung Ladesollwert Mischerregelung, Werk 2,0 K, 0,0…20,0 K** · [Q1] PDF-S. 158 / gedr. S. 134
> „Wenn eine AVR oder eine Vorregelung aktiviert ist dann wird dieser Sollwert gegenüber dem Wärmeerzeuger noch um“ … „(05-034) erhöht.“

**A5 – 05-002 WW-Ladevorrang, Werk 0,0 h, 0,0…10,0 h (0 = absoluter Vorrang, 0,1 = Parallelbetrieb)** · [Q1] PDF-S. 154 / gedr. S. 130
> „0.1 = Absoluter Parallelbetrieb, kein Energiezwang“

**A6 – 05-003 Nachlaufzeit WW-Ladung, Werk 0 min, 0…60 min** · [Q1] PDF-S. 155 / gedr. S. 131
> „Nach Erreichen der Solltemperatur läuft die WW Ladung um die hier eingestellte Zeit nach.“

**A7 – Ladepumpen-Nachlauf 05-008 (SLP1) und 05-009 (SLP2), je Werk 60 s, 0…600 s** · [Q1] PDF-S. 156 / gedr. S. 132
> „Nachlaufzeit der WW-Ladepumpe (SLP1)“

**A8 – 05-081 Maximale WW-Ladedauer, Werk 1,0 h, 0,0…10,0 h** · [Q1] PDF-S. 156 / gedr. S. 132
> „Wird die eingestellte Maximalladedauer überschritten, wird der Ladevorgang unterbrochen“
Dazu 05-083 „Unterbrechung Warmwasserladung“, Werk 0,2 h, 0,0…10,0 h (gleiche Seite, nur Bezeichnung, keine Erklärung).


**A10 – Legionellen: 05-017 Modus (Werk 0 = aus, 0…8), 05-014 Tag (Werk 0 = täglich), 05-015 Uhrzeit (Werk 10,0 h), 05-004 Temp. (Werk 65 °C, 60…80)** · [Q1] PDF-S. 156 / gedr. S. 132
> „Modus 1 = Legionellenschutzschaltung aktiv. Durchladung mit „Legionellenschutztemperatur“ bis SF2 inkl. Nachlaufzeit.“

**A11 – 05-039 Energiezwangwahl, Werk 0 (WW reagiert nicht), 0…3** · [Q1] PDF-S. 155 / gedr. S. 131
> „0 = Warmwasserkreis reagiert nicht auf Energiezwang“

Auslöser sind digitale Eingänge (GLT-Funktion), laut [Q4] S. 24: „At present, it is implemented on the TTE-WEZ, TTE-PS and TTE-SOL modules.“ (Zitat aus Q4, eigene Zeile = eigene Quelle)


**A14 – Wirkung der SG-Zustände auf WW** · [Q2] PDF-S. 2 (= 4 213 320/12 S. 63)
und gleiche Seite: „Dies jedoch nur, wenn auch eine WW-Anforderung (Frost Sollwert zählt nicht zu den Anforderugen) vorliegt.“
und: „Ist der Zustand = Abnahmezwang, wird der WW Sollwert auf die eingestellt max. WW Temperatur erhöht“
Eingänge (gleiche Seite, Tabelle): Eing.1/2 = 0/0 Normal, 0/1 Vorzugsbetrieb, 1/0 Gesperrt (WEZ-Sperre), 1/1 Abnahmezwang.

**A15 – „Warmwasser nachladen“ (Bedienerfunktion, keine Par.-Nr.)** · [Q5] S. 48 (Abschn. 1.11.7)
> „Mit «Nachladung» kann zusätzliches Warmwasser bereitet werden.“ · „Die Dauer sowie die Warmwassertemperatur können individuell eingestellt werden.“

**A16 – Zugangsebenen** · [Q1] PDF-S. 53 / gedr. S. 29
> „Im TopTronic® E Regelsystem sind unterschiedliche Zugangsebenen vorgesehen.“ Genannt: Bediener (kein Code), Technische Betreiber, Service IBN, Fachmann, OEM.
Alle WW-Ladeparameter oben (05-000, 05-001, 05-002, 05-003, 05-034, 05-081, 05-017 …) haben in Q1 Spalte **R = 3 / W = 3**; 05-050 Betriebswahl und 05-051 Normal-WW-Temp. haben **0 / 0**.

**A17 – Praxiswerte UltraSource (Nutzer, nicht Werk)** · [Q3] Beitrag ffischer #3 (16.2.2020)
> „Einschaltdifferenz Warmwasserbereitung "05-000" = 5,0K“
Zweiter Nutzer (MSC1 #4) postet dieselbe Zeile 5,0 K; beide 05-001 = 5,0 K, 05-002 = 0,1 h.

## B) WAHRSCHEINLICH (abgeleitet, nicht wörtlich belegt)

- **Ebene:** R/W-Ziffer 0 = Bediener (passt zu 05-050/05-051, die du am Bedienteil ohne Code änderst). Ziffer 3 ist damit **nicht Bedienerebene** → 05-000 & Co. brauchen einen Code (Service-IBN oder Fachmann). Die Zuordnung Ziffer → Ebenenname steht in Q1 nicht.
- **Deine ~5 K Startschwelle** = 05-000 wurde bei der IBN von 2,5 K (Werk lt. Q1) auf ~5 K gestellt; zwei UltraSource-Nutzer in Q3 haben ebenfalls 5,0 K → vermutlich Hoval-IBN-Standard bei UltraSource. Live-Wert von 05-000 noch per HoxPi lesen.
- **„Endet 1–2 K unter Soll“** – Kandidaten, Reihenfolge nach Plausibilität:
  1. 05-081 Max. Ladedauer (Werk 1,0 h) bricht ab; danach Neustart erst bei Soll − 05-000 (A8). Prüfen: Ladungsdauer in den Logs ≈ 60 min?
  2. Ende nach SF2-Kriterium (A9), wenn 30-049 = 2: Ende bei SF2 ≥ Soll − 05-056, oberer Fühler SF kann dann noch unter Soll liegen.
  3. Loxone-Sollwertänderung während der Ladung (A2).
  4. WP-VL-Grenze/Hochdruck – in dieser Doku **nicht belegt**, nur Vermutung.
- **SG-Vorzugsbetrieb startet allein keine Ladung**, sondern hebt nur den Soll, wenn „WW-Anforderung“ vorliegt (A14). Ob „Anforderung“ = Zeitprogramm aktiv oder = laufende Ladung bedeutet, ist offen. Abnahmezwang hebt dagegen „unabhängig davon“ auf 05-057.
- **06-050 wirkt auf den Puffer, nicht aufs WW** (A13). Falls ihr bisher 06-050 als „WW-PV-Überhöhung“ geführt habt → umbenennen.

## C) NICHT GEFUNDEN

- Eigener Parameter „Warmwasser-Ladung einmalig“ mit 05-Nummer – nur die Bedienfunktion „Nachladung“ (A15). Kein Par.-Nr. belegt.
- WEZ-spezifische Werkseinstellungen für 05-000/05-001/05-081 (die WEZ-KDT-Anleitung 4 213 320 ist öffentlich nur als SG-Auszug S. 63–64 auffindbar; Hoval-Medienlinks 4212600-05 liefern 404).
- WP-seitige WW-VL-Grenze (Verdichter-Max.-VL bei WW) in TopTronic-E-Doku – nicht gefunden.
- 29-xxx: in Q1 nur Allgemein-Thermostat/Differenzsteuerung (29-063 ff., z. B. „Thermostat 1 Schaltdifferenz“ 3 K) – **kein** WW-Bezug.
- Beschreibung 05-083 „Unterbrechung Warmwasserladung“ (nur Name + Werk 0,2 h).

## D) Übersichtstabelle

| Parameter | Nr. | Werk (Q1/Q2) | Bereich | Ebene (R/W) | Quelle |
|---|---|---|---|---|---|
| Einschaltdifferenz WW (Schaltdifferenz) | 05-000 | 2,5 K | 0,5…20,0 K | 3/3 | Q1 S.154/130 |
| Überhöhung Ladesollwert | 05-001 | 5 K | −10…50 K | 3/3 | Q1 S.154/130 |
| WW-Ladevorrang | 05-002 | 0,0 h | 0…10 h | 3/3 | Q1 S.154/130 |
| Nachlaufzeit WW-Ladung | 05-003 | 0 min | 0…60 min | 3/3 | Q1 S.155/131 |
| Überhöhung Ladesoll Mischerregelung | 05-034 | 2,0 K | 0…20 K | 3/3 | Q1 S.155/131 |
| Energiezwangwahl WW | 05-039 | 0 | 0…3 | 3/3 | Q1 S.155/131 |
| Max. WW-Sollwertbegrenzung | 05-057 | 65 °C (Q2) / 90 °C (Q1) | 10…90 °C | 3/3 | Q2 S.3 |
| Max. WW-Ladedauer | 05-081 | 1,0 h | 0…10 h | 3/3 | Q1 S.156/132 |
| Unterbrechung WW-Ladung | 05-083 | 0,2 h | 0…10 h | 3/3 | Q1 S.156/132 |
| Nachlauf SLP1 / SLP2 | 05-008 / 05-009 | 60 s | 0…600 s | 3/3 | Q1 S.156/132 |
| Sollwert-Erhöhung / -Reduktion WW (GLT) | 05-078 / 05-079 | 0 K | −80…80 / −80…0 K | 3/3 | Q1 S.156/132 |
| Legionellenschutz Modus / Tag / Uhrzeit | 05-017 / 05-014 / 05-015 | 0 / 0 / 10,0 h | 0…8 / 0…7 / 0…23,9 | 3/3 | Q1 S.156/132 |
| Legionellenschutztemperatur | 05-004 | 65 °C | 60…80 °C | 3/3 | Q1 S.155/131 |
| Fühleranzahl WW | 30-049 | 1 | 0…2 | 3/3 | Q1 S.154/130 |

## E) Vorschlag: WW-Ladungen bündeln (nur Vorschlag – nichts geändert)

**Schritt 0 – erst lesen (HoxPi, nur lesen):** 05-000, 05-001, 05-056, 05-081, 05-083, 30-049, 05-077. Dann aus den Logs: typische Ladedauer (≈ 60 min? → 05-081 greift) und ob das Ende am SF2 liegt.

**Variante 1 – über Loxone, ohne Codeebene (bevorzugt):**
2. **Ein bis zwei feste Ladefenster** (z. B. Nachmittag mit höchster Außentemperatur, bzw. PV-Fenster): Soll auf 52 °C (PV: 57 °C) heben. Ein Sprung ≥ 05-000 über die Ist-Temperatur startet sofort eine Ladung (A2).
3. **Den Soll während der Ladung nicht senken** – sonst endet sie sofort (A2). Erst zurück auf Halte-Soll, wenn Status 02-052 wieder 0 bzw. SLP aus ist.
4. Für PV besser **05-077 + SG-Vorzugsbetrieb** statt Sollwert-Umschreiben prüfen (A13/A14) – aber nur, wenn die SG-Eingänge (30-052/30-053) vorhanden/beschaltbar sind; sonst bei der bestehenden Modbus-Lösung bleiben.

**Variante 2 – über Parameter (Fachmann/Code nötig):**
- 05-000 von ~5 K auf **7–8 K**: weniger, dafür längere Ladungen. Risiko: oberer Speicher fällt tiefer, bevor nachgeladen wird → Komfort am Halte-Soll prüfen.
- 05-081 von 1,0 h auf **1,5–2,0 h**, falls die Logs Abbrüche nach 60 min zeigen (sonst „Ladung endet 1–2 K unter Soll“ + später Zweitladung).
- 05-001 **nicht** erhöhen: höhere Ladetemperatur = höherer VL der WP = schlechterer COP.

**Was bringt uns das?**
- Weniger Verdichterstarts und weniger Umschaltungen Heizen ↔ WW (Schaltzyklen-Zähler stand 01/2026 bei 17 100 auf 13 058 h).
- Längere, gleichmäßige Ladungen statt Nachladen von 2–3 K – weniger Anfahrverluste und Taktung, Ladung fällt in das wärmste Tagesfenster/PV-Zeit → besserer COP pro kWh WW.
- Heizkreise werden seltener durch Vorrang/Energiezwang unterbrochen (05-002).
- Größenordnung der Einsparung **nicht belegt** – erst nach 1–2 Wochen Vergleich (Starts/Tag, kWh el. für WW) bewerten.