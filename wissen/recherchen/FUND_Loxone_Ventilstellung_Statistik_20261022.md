# FUND: Loxone Ventilstellung je Raum historisieren (IRR + Stellantrieb Tree/Air)

Stand: 22.10.2026, Web-Recherche (nur öffentliche Live-Seiten, kein Login, kein archive.org).
Kontext: Miniserver Gen. 2, Intelligente Raumregelung (IRR, Config 15/16), Loxone-Stellantriebe Tree/Air, FBH je Raum.
Problem: Ventilstellung ist über die API nicht als eigener Control lesbar, IRR hat keine Statistik -> Öffnungsanteil über 14 Tage nicht auswertbar.

## WICHTIGE EINSCHRÄNKUNG ZUR QUELLENLAGE

- Loxone meldet einen Cyberangriff am 18.10.2026; viele Doku-Seiten zeigen derzeit nur "Diese Funktion ist vorübergehend nicht verfügbar." Betroffen (heute geprüft): 
  - https://www.loxone.com/dede/kb/intelligente-raumregelung/
  - https://www.loxone.com/enen/kb/intelligent-room-controller/
  - https://www.loxone.com/dede/kb/stellantrieb-tree/
  - https://www.loxone.com/dede/kb/stellantrieb-air/
  - https://www.loxone.com/dede/kb/inbetriebnahme-stellantrieb-tree/
  - https://www.loxone.com/dede/kb/merker/
  - Hinweis auf der Startseite: "On October 18, 2026, we detected a cyberattack on our internal company systems." (https://www.loxone.com/dech/kb/intelligente-raumregelung/ leitet auf die Startseite um)
- loxforum.com liefert für Forenthreads 403 Forbidden (Bot-Sperre) -> Threads nur als Titel aus der Suche bekannt, Inhalt NICHT gelesen, daher nicht als Beleg verwendet.
- Die exakte Ausgangsliste der IRR (Namen + Wertebereich) konnte deshalb heute NICHT aus der offiziellen Doku belegt werden. Nachholen, sobald die Seite wieder online ist.

## 1. BELEGT

### 1.1 Loxone-Statistik: wie sie funktioniert (offizielle Doku, online)
Quelle: https://www.loxone.com/dede/kb/statistiken/ (englisch: https://www.loxone.com/enen/kb/statistics/)
- Aktivierung je Objekt: "setzen Sie den Haken bei Statistik und stellen anschließend ein Intervall ein".
- Abtastung: "ausgehend von einer vollen Stunde im eingestellten Intervall der jeweils aktuelle Wert in die Statistik geschrieben" -> Momentanwert, kein Mittelwert.
- "Statistiken mit Mittelwert stehen seit Loxone Config 12.0 nicht mehr zur Verfügung." Alternative laut Doku: Empfindlichkeit am Eingang bzw. "Baustein gleitender Mittelwert".
- Richtwert: "für Raumtemperaturen 10 Minuten mehr als ausreichend"; kurze Intervalle belasten die SD-Karte.
- Export: In Config Peripheriebaum -> Miniserver -> "Statistiken laden" -> markierte Statistiken "als .csv Dateien exportieren".
- Browser: "http://MiniserverIP/stats/" listet Statistiken, Klick zeigt die Daten als .xml.
- Per Mail: Intervall + Mailer zuordnen -> Statistik als .csv per Mail.
- Ablage: "Für jede Statistik wird pro Monat eine Datei abgelegt." SD-Belegung prüfen über "http://miniserver/dev/sys/sdtest" (Wert "usage", ab >60 % alte Statistiken löschen).

### 1.2 Stellantriebe fahren stetig (0-100 %), nicht nur auf/zu
- Offizieller Loxone Use Case: "Unlike conventional on/off solutions, the Valve Actuators are adjustable between 0-100%." und "The Intelligent Room Controller calculates what proportion the valve needs to open to" 
  Quelle: https://www.loxone.com/enen/kb/zoned-heating-comfort/
- Datenblatt Stellantrieb Tree 100602: Hub 5,0 mm, 150 N, Laufzeit ca. 20 s für 0 % -> 100 % und ca. 21 s für 100 % -> 0 %.
  Quelle: https://pim.loxone.com/datasheet/100602-valve-actuator-tree
- LoxWiki: "Die Loxone Stellantriebe Air/Tree verhalten sich als Stetigregler." (Spindelmotor statt thermisch)
  Quelle: https://loxwiki.atlassian.net/wiki/spaces/LOX/pages/1516635059/Elektrische+Stellantriebe
- Nach Stromausfall/Neustart Rekalibrierung (Referenzfahrt); Diagnosemeldungen "Kein Ventil erkannt", "Ventil steckt fest", "Mechanischer Defekt" über Systemstatus bzw. Diagnose-Eingänge.
  Quelle: https://www.loxone.com/dede/kb/diagnose-stellantrieb/

### 1.3 IRR kann wahlweise PWM (Auf/Zu) ausgeben, Basis 5 Minuten
- Andras Gaal (Loxone-Community, 20.12.2018): "IRCv2 can do PWM (5 minute base time) as well."
  Quelle: https://groups.google.com/g/loxone-english/c/aenh2J81IfE
- Duncan (14.12.2019): "the timebase for the IRC is 5 minutes" (20 % Bedarf = 1 min an, 4 min aus); bei digitalem Aktor "you need to use the Q pwm digital output".
  Quelle: https://groups.google.com/g/loxone-english/c/b-74E29NDow
- Duncan (19.02.2022): "the H output needs to be used but set to 'Enable pwm outputs' in the settings"; IRC hat "an analog 0-10 output which would be used for analog actuators".
  Quelle: https://groups.google.com/g/loxone-english/c/qRGfWXIYUf0
- Andras Gaal (14.01.2019): "There are dedicated Qh and Qc outputs as well to retrieve the discrete heating/cooling output." Ausgang HC = Heizen/Kühlen kombiniert.
  Quelle: https://groups.google.com/g/loxone-english/c/aenh2J81IfE
- Folge: Bei Loxone-Stellantrieben (stetig) ist PWM normalerweise AUS, der Stellwert ist ein Analogwert.

### 1.4 Externe Historisierung (InfluxDB/Grafana) ist ein etablierter Weg
- LoxWiki: "Vom Loxone Miniserver aus werden die Daten per virtuelle Ausgang mit einem HTTP Post Request gesendet." Alternative UDP; Speicherung in InfluxDB, Visualisierung Grafana; Nachteil interne Statistik: "zum einen wird die SD-Card zu stark belastet".
  Quelle: https://loxwiki.atlassian.net/wiki/spaces/LOX/pages/1605272942/Statistiken+extern+speichern+und+visualisieren

### 1.5 Erfahrungen FBH / Ventile (öffentliche Community-Threads)
- Peter Holden (18.02.2022): "the App is reporting that the actuators are open somewhere between 0-100% usually 20%." (Heizkörper/Verteiler, kein FBH-Richtwert)
  Quelle: https://groups.google.com/g/loxone-english/c/qRGfWXIYUf0
- Thread "IRC overshooting target temperature" (2019/2020): Überschwingen bei Sonne mit FBH; Empfehlung Vorlauf runter, hydraulischer Abgleich, Vorlauf nach IRC-Heizlast modulieren: "To avoid overshooting you need to modulate the UFH LWT based on the IRC's heating load." (Rob_in, 21.12.2019); Kritik: "The IRC should take temperature inertia into account" (Sungray, Dez. 2019).
  Quelle: https://groups.google.com/g/loxone-english/c/3h2tMI5dQKM
- Gleicher Thread, Duncan (08.10.2020): "you really dont need proportional valve for UFH because the 5 mins pwm on/off of the 240v ones achieves the same thing."
- LoxWiki Heizungssteuerung: FBH träge, "oft kommt die Temperatur erst nach vielen Stunden im Raum an" -> Nachtabsenkung meist nicht sinnvoll.
  Quelle: https://loxwiki.atlassian.net/wiki/spaces/LOX/pages/1576271864/Heizungssteuerung

## 2. WAHRSCHEINLICH (nicht aus offizieller Doku belegbar, da offline)

- Der Heiz-Stellwert der IRR (Ausgang "H" bzw. in älteren Versionen "AQ") läuft im Bereich 0..10 und entspricht 0..100 % Ventilöffnung. Indizien: "analog 0-10 output" (https://groups.google.com/g/loxone-english/c/qRGfWXIYUf0), "a 10.0 signal to the valves" beim Aufheizen (Andras Gaal, 18.12.2018, https://groups.google.com/g/loxone-english/c/aenh2J81IfE), Leserkommentar "Ausgang AQ der Raumregelung nur 0-10" (https://meintechblog.de/2017/09/25/smart-home-basics-in-3-schritten-zur-soliden-temperaturregelung/). -> In des Betreibers Config am Liveview prüfen (Wert 0..10 oder 0..100?).
- Ausgangsnamen der IRRv2 laut Community: H / C (analog Heizen/Kühlen), Qh / Qc (digital bzw. PWM), HC (kombiniert); Forum erwähnt nummerierte Varianten "C2, H3" (https://groups.google.com/g/loxone-english/c/qRGfWXIYUf0). Genaue Namen in Config 15/16 per Mouseover am Baustein verifizieren.
- Der Stellwert ist eine BERECHNETE Vorgabe; die tatsächliche Ventilposition kann bei Rekalibrierung, "Ventil steckt fest" oder Hub-Begrenzung abweichen (Ableitung aus https://www.loxone.com/dede/kb/diagnose-stellantrieb/). Für die 14-Tage-Auswertung reicht der Stellwert.
- Ein Merker/Virtueller Status, der in der Visualisierung verwendet wird, erscheint als eigener Control in der Struktur (LoxAPP3.json) und ist dann per API lesbar; mit aktivierter Statistik ist auch dessen Verlauf abrufbar (Ableitung: Statistik ist laut https://www.loxone.com/dede/kb/statistiken/ "bei allen Objekten, die in der Visualisierung verwendet werden, und deren Statistik aktiviert wurde" anzeigbar).
- meintechblog-Autor legt Ventilöffnung zur Übersicht auf einen "Virtueller Status"-Baustein (https://meintechblog.de/2017/09/25/smart-home-basics-in-3-schritten-zur-soliden-temperaturregelung/) -> genau das Muster, das wir brauchen.

## 3. NICHT GEFUNDEN

- Offizielle Ausgangsliste der IRR mit Wertebereichen: Doku-Seite derzeit offline (https://www.loxone.com/dede/kb/intelligente-raumregelung/ "vorübergehend nicht verfügbar").
- Offizielle Funktionsbaustein-Doku Stellantrieb Tree/Air (Ein-/Ausgänge, ob es einen Positions-Rückmeldeausgang gibt, ob das Aktor-Objekt selbst eine Statistik-Checkbox hat): offline (https://www.loxone.com/dede/kb/stellantrieb-tree/).
- IRRv2-States in der Structure-File-Doku: PDF (https://www.loxone.com/dede/wp-content/uploads/sites/2/2021/10/1701_Structure-File.pdf) nur bis S. 55 lesbar, Abschnitt IntelligentRoomControllerV2 nicht erreicht -> kein Beleg, ob ein Ventil-/Stellwert-State existiert. des Betreibers eigene API-Beobachtung (kein eigener Control) bleibt maßgeblich.
- Loxforum-Threads (u. a. "Statistik Stellantrieb Heizung" https://www.loxforum.com/forum/german/software-konfiguration-programm-und-visualisierung/84513-statistik-stellantrieb-heizung, "Stellantrieb Tree Ventil position" .../209065, "Hysterese der Ventilstellung" .../354196, "Intelligente Raumregelung für Fußbodenheizung - Parametervorschläge" .../127020): 403, Inhalt nicht gelesen.
- Belastbare Zahlen zu "typischen" Ventil-Öffnungsanteilen bei FBH im Niedrigenergiehaus: nichts Konkretes gefunden (nur "usually 20%" aus einem Heizkörper-Thread).
- knx-user-forum: kein passender Treffer zu Loxone-IRR + Auskühlen.
- Konkreter Beleg zu "Raumregler schließt wegen Ofen/Fremdwärme, Boden kühlt aus" mit Loxone: nur indirekt (Sonnen-Überschwingen-Thread oben), keine direkte Ofen-Erfahrung gefunden.

## 4. WAS BRINGT UNS DAS (Vorschlag – der Betreiber entscheidet und baut selbst)

Ziel: Je Raum den Heiz-Stellwert der IRR alle 5 min mitschreiben, 14 Tage sammeln, dann Öffnungsanteil (Mittelwert, Anteil Zeit > 0 %, Anteil Zeit = 0 %) auswerten – und gleichzeitig per API lesbar machen.

Variante A – nur Loxone-Bordmittel (empfohlen, wenig Aufwand):
1. In Loxone Config je Raum den Ausgang der IRR suchen, der zum Stellantrieb-Baustein/Aktor geht (vermutlich "H"; per Mouseover prüfen). PWM-Einstellung der IRR prüfen: muss bei Loxone-Stellantrieben AUS sein, sonst kommt nur 0/1.
2. Diesen Ausgang ZUSÄTZLICH (Abzweig, nichts abklemmen) auf einen neuen Analogmerker oder "Virtueller Status" legen, Name z. B. "Ventil_Stellwert_<Raum>".
3. Eigenschaften des Merkers: Statistik anhaken, Intervall 5 min (10 min reicht notfalls; laut Doku Momentanwert-Abtastung). Einheit/Format z. B. "<v.1>" und Raum/Kategorie "Heizung" zuordnen.
4. "In Visualisierung verwenden" aktivieren -> wird eigener Control, damit auch über API/Statistik abrufbar.
5. Optional zusätzlich: Wert auf Baustein "Gleitender Mittelwert" (z. B. 24 h) legen und dessen Ausgang ebenfalls als Merker mit Statistik loggen -> Tagesmittel direkt sichtbar.
6. In den Miniserver speichern. Nach 14 Tagen: Config -> Miniserver -> "Statistiken laden" -> CSV-Export, oder Browser http://<MiniserverIP>/stats/.
7. Vorher SD-Auslastung prüfen: http://<MiniserverIP>/dev/sys/sdtest ("usage" < 60 %). Bei ca. 8–10 Räumen x 5 min ist die Datenmenge unkritisch, trotzdem nicht unter 5 min gehen.

Gleich mitloggen (gleiches Muster, falls noch nicht vorhanden), damit die Auswertung Sinn ergibt:
- IRR-Ist- und Zieltemperatur je Raum (Zieltemperatur-Ausgang laut LoxWiki "AQt", https://loxwiki.atlassian.net/wiki/spaces/LOX/pages/1520762947/Intelligente+Raumregelung).
- Vorlauf/Rücklauf je Heizkreis (Hoval/HoxPi) und Außentemperatur.
- Wohnzimmer UG: Ofenbetrieb erkennbar machen (z. B. Raumtemperatur-Anstieg oder eigener Fühler), um die Phasen "Ventil 0 % wegen Ofen" sauber abzugrenzen.

Variante B – extern (mehr Aufwand, nur wenn ohnehin InfluxDB/Grafana läuft):
- Virtueller Ausgang mit HTTP-Post bzw. UDP an InfluxDB, Grafana-Dashboard (Anleitung: https://loxwiki.atlassian.net/wiki/spaces/LOX/pages/1605272942/Statistiken+extern+speichern+und+visualisieren). Vorteil: keine SD-Last, Messreihen kombinierbar. Für 14 Tage Auswertung ist Variante A ausreichend.

Auswertung nach 14 Tagen (wir können die CSV dann auswerten):
- Je Raum: Mittelwert Stellwert, Anteil Zeit mit 0 %, Anteil Zeit mit 100 %, längste ununterbrochene 0-%-Phase.
- Wohnzimmer UG gegen Ofenzeiten legen: Lange 0-%-Phasen nach Ofenbetrieb = Bestätigung "Raumfühler schließt, Boden kühlt aus" (bisher nur Vermutung).
- Raum dauerhaft nahe 100 % = Raum unterversorgt (Vorlauf zu niedrig / Durchfluss / Abgleich). Alle Räume dauerhaft niedrig (z. B. < 30 %) = Vorlauf eher zu hoch (Indiz aus https://groups.google.com/g/loxone-english/c/3h2tMI5dQKM).

Hinweis: Nichts davon ändert die Regelung – es sind reine Abzweige auf Merker. Vor Speichern in den Miniserver Projektdatei sichern.