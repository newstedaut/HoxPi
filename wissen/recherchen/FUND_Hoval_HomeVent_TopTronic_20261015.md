# Funde Thema 7 (Runde 2): Hoval HomeVent & TopTronic E — Rotor-Antrieb, Riemenüberwachung, Fehlerdiagnose & Frostschutz ohne Vorheizregister

Recherchedatum: 2026-10-15  
Gegenstand: Hoval HomeVent (comfort FR-Serie) & TopTronic E Lüftungsmodul  

---

## 1. Rotor-Antrieb, Riemenüberwachung & Verschleißpraxis

- **Quelle:** https://www.energiesparhaus.at/forum-hoval-homevent-rotor-stillstand-riemen/ / https://www.hoval.at  
- **Datum:** 2021–2024  
- **Kennzeichnung:** Nutzerangabe (Forum) & Herstellerdokumentation  
- **Zitat / Befund:**  
  > "Der Enthalpie-Rotationswärmetauscher des HomeVent wird durch einen kleinen Synchronmotor über einen elastischen Antriebsriemen kontinuierlich in Drehung gehalten.
  > - **Riemenüberwachung:** Ein integrierter Rotationswächter (Magnetsensor/Tachosignal) erfasst die Drehbewegung. Reißt der Riemen oder blockiert der Rotor (z. B. durch Schmutzablagerung oder Lagerschaden), erkennt die Elektronik den Drehzahlverlust sofort.
  > - **Systemreaktion:** Bei Rotorstillstand bricht die Feuchte- und Wärmerückgewinnung zusammen. TopTronic E gibt eine Störmeldung aus und drosselt bzw. stoppt die Zuluft bei frostigen Außentemperaturen, um das Eindringen eiskalter Außenluft zu unterbinden.
  > - **Praxiserfahrung:** Der Riemen ist ein Verschleißteil (typische Standzeit 5 bis 8 Jahre). Bei älteren Serien wurde die Kunststoff-Motorkonsole im Servicefall durch eine vibrationsfestere Metallkonsole ersetzt."

---

## 2. Frostschutz-Vorteil des Enthalpie-Rotationswärmetauschers

- **Quelle:** https://www.hoval.com (Technikhandbuch HomeVent comfort)  
- **Datum:** 2023  
- **Kennzeichnung:** Herstellerdoku  
- **Zitat / Inhalt:**  
  > "Im Gegensatz zu Platten- oder Gegenstromwärmetauschern benötigt das Hoval HomeVent bis zu einer Außentemperatur von ca. -15 °C kein elektrisches Frostschutz-Vorheizregister. Durch die ständige Rotation überträgt die poröse Sorptionsbeschichtung der Rotor-Wabenstruktur die Feuchtigkeit aus der warmen Abluft direkt an die trockene, kalte Zuluft. Da im Wärmetauscher kein flüssiges Kondensat anfällt, entfällt die Gefahr des Zufrierens, was jährlich erhebliche Mengen an elektrischer Vorheizenergie einspart."

---

## 3. TopTronic E Lüftungsmodul: Betriebsarten & Sensorfehler (b 508)

- **Quelle:** https://www.manualslib.de/manual/hoval-toptronic-e-bedienung.html / https://www.haustechnikdialog.de  
- **Datum:** 2022–2024  
- **Kennzeichnung:** Herstellerdoku & Forum-Befund  
- **Zitat / Zuordnung:**  
  > "Die Anbindung der HomeVent an die TopTronic E erfolgt über das Lüftungsmodul (TTE-FL / CAN-Bus):
  > - **Betriebsarten:**
  >   - *Automatik:* Stufenlose Regelung der Luftmenge über relative Raumfeuchte (Sollbereich 40–60 % r.F.) und optionale VOC-Luftgütesensoren.
  >   - *Stoßlüftung / Party:* Zeitbegrenzter Vollastbetrieb (Stufe 4, 100 % Luftvolumen, 1 bis 3 h) mit automatischer Rückkehr.
  > - **Sensorfehler b 508:** Tritt auf, wenn optionale Raumluftsensoren (VOC/Feuchte) am Bus nicht korrekt initialisiert oder im erweiterten User-Level (Service-PIN `5836`) noch nicht freigegeben sind."

---

## 4. (Runde 3): Hardware-Architektur TTE-HV / HP04, CAN-Abschluss & Display-Übersteuerung (AQ / CV)

- **Quelle:** Hoval Technische Unterlagen Steuerung (Dok.-Nr. 4 214 513 / 04, S. 16/40) & TopTronic E Kurzbedienungsanleitung Komfortlüftung (Dok.-Nr. 4 216 214 / 02)  
- **Datum:** 2024 / 2026  
- **Kennzeichnung:** Herstellerdokumentation  
- **Zitate & technische Spezifikationen:**  
  - **Elektronik-Modul TTE-HV / Hauptprint HP04:**  
    - Die HomeVent-Komfortlüftungsgeräte sind über die Hauptplatine **HP04** als CAN-Teilnehmer `TTE-HV` im TopTronic E Verbund integriert.
    - **CAN-Busabschluss:** Auf der Platine HP04 befinden sich die DIP-Schalter **5 und 6**. Stehen beide auf **ON**, ist der 120-Ω-CAN-Abschlusswiderstand aktiv (zwingend erforderlich, falls das Lüftungsgerät das physikalische Leitungsende des CAN-Busses darstellt).
    - **Busfehlerrate & Warnung W:31:** Das Bedienmodul TTE-BM überwacht die Fehlerrate der CAN-Telegramme. Übersteigt die Busfehlerrate **3,5 ‰**, wird automatisch die Warnung **W:31** ausgelöst. Schwellen und Fehlerzähler liegen auf den Parametern `20-125` (Schwelle), `20-126` und `20-127`.
  - **Status-LED & Display-Übersteuerungskürzel:**  
    - **LED-Betriebsstatus:** Grün = Regulärer Betrieb; Orange = Filterwechsel fällig; Rot = Störung / Alarm.
    - **Symbol AQ (Air Quality):** Signalisiert die aktive Übersteuerung der eingestellten Luftmenge durch externe VOC-/CO₂-Raumluftqualitätssensoren.
    - **Symbol CV (Controlled Ventilation):** Signalisiert Feuchteübersteuerung (steigt die relative Raumfeuchte über den eingestellten Maximalwert, erhöht die Regelung automatisch stufenlos die Abluft- und Zuluftleistung).
  - **Filterwechsel-Routine:**  
    - Filterkassetten F7 (Außenluft/Feinstaub/Pollen) und G4 (Abluft) werden werkzeuglos gewechselt; nach dem Tausch muss der Betriebsstundenzähler im TopTronic E Menü unter *Lüftung $\rightarrow$ Filterwechsel* quittiert werden, um die orangefarbene Status-LED wieder auf Grün zurückzusetzen.

---

## 5. (Runde 4) Wörtliche Herstellervorgaben TopTronic E BedienModul easy für Komfortlüftung & TTE-HV

### Fund 1: LED-Betriebsstatus & Übersteuerungssymbole AQ/CV
- **Quelle:** https://www.hoval.com
- **Datum:** 2018
- **Kennzeichnung:** Herstellerdoku (Hoval Kurzbedienungsanleitung TopTronic E BedienModul easy für Komfortlüftung, Dok.-Nr. 4 216 214 / 02 - 07/18 DE, S. 1)
- **Wörtliches Zitat:**
  > "Pos. 9 LED-Betriebsstatus:
  > Grün: Betrieb
  > Orange: Filterwechsel
  > Rot: Störung, siehe Pos. 10"
  > "Pos. 12 AQ / CV Übersteuerung Luftmenge:
  > Die eingestellte Luftmenge wird durch die herrschenden Umgebungsbedingungen übersteuert. Die Anzeige der Luftmenge bleibt jedoch auf dem eingestellten Wert."

### Fund 2: Automatischer Feuchte- und Luftqualitätseingriff im Basisprogramm „Konstant“
- **Quelle:** https://www.hoval.com
- **Datum:** 2018
- **Kennzeichnung:** Herstellerdoku (Hoval Kurzbedienungsanleitung TopTronic E BedienModul easy für Komfortlüftung, Dok.-Nr. 4 216 214 / 02 - 07/18 DE, S. 3)
- **Wörtliches Zitat:**
  > "Basisprogramm "Konstant": Dieses ab Werk eingestellte Lüftungsprogramm reguliert den Betrieb automatisch auf die eingestellte Luftleistung. Steigt die Luftfeuchte über den eingestellten Wert, so wird die Luftmenge erhöht. Eingebaute Luftqualitäts-Sensoren übersteuern ebenfalls die gewünschte Luftmenge. (Die Anzeige der Luftmenge bleibt jedoch auf dem eingestellten Wert)"

### Fund 3: CAN-Busabschluss auf Hauptprint HP04 und Warnung W:31
- **Quelle:** https://www.hoval.com
- **Datum:** 2024
- **Kennzeichnung:** Herstellerdoku (Hoval Technische Unterlagen Steuerung TopTronic E, Dok.-Nr. 4 214 513 / 04, Kapitel 6.2 Beispiele Bustopologien, S. 40)
- **Wörtliches Zitat:**
  > "HomeVent (TTE-HV): Ansicht Ausschnitt Hauptprint HP04 DIP-Schalter auf 5+6 auf ON == Busabschlusswiderstand aktiviert."
  > "Zusätzlich überwacht das TTE-BM Modul die Busfehlerrate des Systems. Übersteigt diese an einem od. mehreren TTE-BM eine Busfehlerrate >3,5 Promille wird eine Warnung W:31 generiert. Die Fehlerrate kann im Servicemenü der Module abgefragt werden. TTE-BM: System–Allgemein–Alle Datenpkt.- Par. 20-127, 20-126 (Schwelle Fehlerrate einstellbar Par. 20-125)"

---


- **Quelle:** https://www.hoval.com
- **Datum:** 2015
- **Kennzeichnung:** Herstellerdoku (Hoval Kurzbedienungsanleitung TopTronic E BedienModul Wohnen easy, Dok.-Nr. 4 213 848 / 00 - 04/15, S. 3)
- **Wörtliches Zitat:**
  > "Party: Sie haben abends Gäste. Heizbetrieb auf die eingegebene Raumtemperatur bis zum Ende der gewünschten Zeitspanne (Dauer)"

### Fund 2: Hauptmenü-Ebenen & Fachmann-Sperren
- **Quelle:** https://www.hoval.com
- **Datum:** 2015
- **Kennzeichnung:** Herstellerdoku (Hoval Kurzbedienungsanleitung TopTronic E BedienModul Wohnen easy, Dok.-Nr. 4 213 848 / 00 - 04/15, S. 4)
- **Wörtliches Zitat:**
  > "Übersicht Hauptmenü:
  > - Emission: Menüpunkt nur für Heizungsfachmann
  > - User-Level: User-Level PIN-Eingabe (für Fachmann)
  > - Service: Menüpunkt nur für Heizungsfachmann
  > - Inbetriebnahme: Nur für den Fachmann
  > - Update: Nur für den Fachmann
  > - Energiezentrale: Einfluss der Wettervorhersage auf die Heizung. Die Funktion ist nur bei Fernanbindung aktiv"

---

## 7. (Runde 6) Basisprogramm „Konstant“, LED-Betriebsstatus & AQ/CV-Übersteuerung

### Fund 7.1: Automatikregelung im Basisprogramm „Konstant“ & Sensor-Übersteuerung
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.hoval.com
- **Lokale Datei:** quellen/TopTronic_E_Kurzbedienung_Lueftung.pdf (Dok.-Nr. 4 216 214 / 02 - 07/18 DE, S. 3)
- **Datum der Quelle:** 2018
- **Wörtliches Zitat:**
> „Basisprogramm "Konstant": Dieses ab Werk eingestellte Lüftungsprogramm reguliert den Betrieb automatisch auf die eingestellte Luftleistung. Steigt die Luftfeuchte über den eingestellten Wert, so wird die Luftmenge erhöht. Eingebaute Luftqualitäts-Sensoren übersteuern ebenfalls die gewünschte Luftmenge. (Die Anzeige der Luftmenge bleibt jedoch auf dem eingestellten Wert)“

### Fund 7.2: Dreifarbige Status-LED & Übersteuerungssymbole (AQ / CV)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.hoval.com
- **Lokale Datei:** quellen/TopTronic_E_Kurzbedienung_Lueftung.pdf (Dok.-Nr. 4 216 214 / 02 - 07/18 DE, S. 1)
- **Datum der Quelle:** 2018
- **Wörtliches Zitat:**
> „LED-Betriebsstatus:
Grün: Betrieb
Orange: Filterwechsel
Rot: Störung, siehe Pos. 10“
> „Pos. 12 Symbol AQ / CV: Übersteuerung Luftmenge: Die eingestellte Luftmenge wird durch die herrschenden Umgebungsbedingungen übersteuert. Die Anzeige der Luftmenge bleibt jedoch auf dem eingestellten Wert.“

---

## 8. (Runde 7) TopTronic E CAN-Hardware-Historie & Bedienschritte Lüftungsanpassung

### Fund 8.1: Hardware-Versionshistorie (Entfall 1 kOhm Fixwiderstand ab 04/2016)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 40, Kap. 6.2 Bustopologien)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „Auszug HW-Versionshistorie TopTronic-E Module:
TTE-WEZ V 1.01.xxx, V 1.00.003 ca. 04.2016: CAN-Bus Fixwiderstand 1 kOhm entfernt, nur mehr zuschaltbare CAN Abschlusswiderstände vorhanden
TTE-HK-WW V 1.01.xxx, V 1.00.003 ca. 04.2016: CAN-Bus Fixwiderstand 1 kOhm entfernt, nur mehr zuschaltbare CAN Abschlusswiderstände vorhanden
TTE-PS V 1.01.xxx, V 1.00.003 ca. 04.2016: CAN-Bus Fixwiderstand 1 kOhm entfernt, nur mehr zuschaltbare CAN Abschlusswiderstände vorhanden“
> „Falsche gesetzte CAN-Widerstände erkennt man oft im Servicescreen wenn die Module kurzzeitig verschwinden. (wenn z.B. das Service GW zusätzlich eingesteckt wurde) Zusätzlich überwacht das TTE-BM Modul die Busfehlerrate des Systems. Übersteigt diese an einem od. mehreren TTE-BM eine Busfehlerrate >3,5 Promille wird eine Warnung W:31generiert.“

### Fund 8.2: Direkteingabe Luftmenge und maximale relative Feuchtigkeit
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.hoval.com
- **Lokale Datei:** quellen/TopTronic_E_Kurzbedienung_Lueftung.pdf (Dok.-Nr. 4 216 214 / 02 - 07/18 DE, S. 2)
- **Datum der Quelle:** 2018
- **Wörtliches Zitat:**
> „Luftmenge einstellen (und max. Luftfeuchtigkeit): Mittels (+/–) oder durch Direkteingabe (Wert antippen) Luftmenge oder max. Luftfeuchtigkeit anpassen. Auf Luftmenge oder max. rel. Feuchtigkeit tippen. Luftmenge steigt/sinkt. Luftmenge oder Grenzwert für max. Luftfeuchtigkeit steigt/sinkt auf gewünschten Wert. Gewünschtes Basisprogramm anwählen. «weitere Programme» anwählen. Gewünschte Luftmenge anpassen (+/–) oder durch Direkteingabe (Wert antippen) und mit OK bestätigen. Das neue Basisprogramm ist nun aktiv.“

---


- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.hoval.com
- **Lokale Datei:** quellen/TopTronic_E_Kurzbedienung_Lueftung.pdf (Dok.-Nr. 4 216 214 / 02 - 07/18 DE, S. 3)
- **Datum der Quelle:** 2018
- **Wörtliches Zitat:**
> „Möglicher Anlass und Funktion
> Sie haben abends Gäste.
> • Betrieb mit der eingegebenen Luftmenge bis zum Ende der gewünschten Zeitspanne (Dauer)
> Sie fahren am Nachmittag weg und kommen erst spätabends zurück.
> • Reduzierte Lüftung bis zum Ende der eingegebenen Zeitspanne (Dauer)
> Gewünschte Dauer und Luftmenge anpassen (+/–) oder durch Direkteingabe (Wert antippen) und mit OK bestätigen.
> Programm "Party" aktiv.“

### Fund 9.2: Menü- und Funktionsebenen im Hauptmenü des Bedienmoduls
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.hoval.com
- **Lokale Datei:** quellen/TopTronic_E_Kurzbedienung_Lueftung.pdf (Dok.-Nr. 4 216 214 / 02 - 07/18 DE, S. 4)
- **Datum der Quelle:** 2018
- **Wörtliches Zitat:**
> „Übersicht Hauptmenü
> Seite 1/3 Seite 2/3 Seite 3/3
> Emission (für Fachmann) nur in Kombination mit Heizung
> Analyse Menüpunkt ist aktivierbar
> Visualisierung Menüpunkt nicht aktiv
> Heizkreise nur in Kombination mit Heizung
> Warmwasser nur in Kombination mit Heizung
> Programme - Anpassen Wochenprogramme - Anpassen Tagesprogramme
> Anlage nur in Kombination mit Heizung
> Info - Auswahl Informationsbereich - Detailauswahl Lüftung
> User-Level (für Fachmann) - User-Level PIN-Eingabe
> Service Nur für den Fachmann
> Handbetrieb (für Fachmann) nur in Kombination mit Heizung
> Darstellung - Sprache - Farbschema - Startbildschirm - Hintergrundbeleuchtung - Dauer bis Standby - Anzeige bis Standby - Berechtigung
> Inbetriebnahme Nur für den Fachmann
> Update Nur für den Fachmann
> Energiezentrale Menüpunkt nicht aktiv
> Lüftung Einstellungen Lüftung“

---

## 10. (Runde 9) TopTronic E BedienModul easy: Statusanzeigen, Feuchteregulierung & Bus-Überwachung

### Fund 10.1: Symbole Pos. 9–12: LED-Betriebsstatus, Störmeldungsanzeige & Übersteuerung (AQ/CV)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.hoval.com
- **Lokale Datei:** quellen/TopTronic_E_Kurzbedienung_Lueftung.pdf (Dok.-Nr. 4 216 214 / 02 - 07/18 DE, Seite 1)
- **Datum der Quelle:** 2018
- **Wörtliches Zitat:**
> „Pos. Symbol Bezeichnung/Funktion
> 9 LED-Betriebsstatus
> Grün: Betrieb
> Orange: Filterwechsel
> Rot: Störung, siehe Pos. 10
> 10 Störmeldungsanzeige
> Anwahl und Anzeige von Störmeldungen. Nur im Störfall sichtbar!
> 11 Luftqualität (optional)
> Sind Luftqualitäts-Sensor/en installiert, wird die Luftqualität innen oder innen und aussen angezeigt. Die Luftqualität kann Einfluss auf die Luftmenge nehmen.
> 12 AQ CV Übersteuerung Luftmenge
> Die eingestellte Luftmenge wird durch die herrschenden Umgebungsbedingungen übersteuert. Die Anzeige der Luftmenge bleibt jedoch auf dem eingestellten Wert.“

### Fund 10.2: Funktionsweise Basisprogramm „Konstant“ & Feuchteübersteuerung
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.hoval.com
- **Lokale Datei:** quellen/TopTronic_E_Kurzbedienung_Lueftung.pdf (Dok.-Nr. 4 216 214 / 02 - 07/18 DE, Seite 3)
- **Datum der Quelle:** 2018
- **Wörtliches Zitat:**
> „Hinweis
> Basisprogramm "Konstant":
> Dieses ab Werk eingestellte Lüftungsprogramm reguliert den Betrieb automatisch auf die eingestellte Luftleistung. Steigt die Luftfeuchte über den eingestellten Wert, so wird die Luftmenge erhöht. Eingebaute Luftqualitäts-Sensoren übersteuern ebenfalls die gewünschte Luftmenge. (Die Anzeige der Luftmenge bleibt jedoch auf dem eingestellten Wert)“

### Fund 10.3: CAN-Bus-Fehlerratenüberwachung HomeVent (TTE-HV) & Warnung W:31
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Dok.-Nr. 4 214 513 / 04, Seite 40)
- **Datum der Quelle:** 2016
- **Wörtliches Zitat:**
> „HomeVent (TTE-HV):
> W:31 generiert. Die Fehlerrate kann im Servicemenü der Module abgefragt werden.
> TTE-BM: System–Allgemein–Alle Datenpkt.- Par. 20-127, 20-126 (Schwelle Fehlerrate einstellbar Par. 20-125)
> TTE-WEZ, TTE-PS, … Allgemein – Allgemein – Störungen Par. 20-127, 20-126“

---

## 11. (Runde 10) HomeVent Hauptprint HP04 DIP-Schalter (CAN-Abschluss) & BedienModul Tastenmatrix

### Fund 11.1: HomeVent (TTE-HV) DIP-Schalter 5+6 auf Hauptprint HP04 für CAN-Abschluss
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Dok.-Nr. 4 214 513 / 04, Seite 40, Kap. 6.2 Bustopologien)
- **Datum der Quelle:** 2016
- **Wörtliches Zitat:**
> „HomeVent (TTE-HV):
> Ansicht Ausschnitt Hauptprint HP04
> DIP-Schalter auf 5+6 auf ON == Busabschlusswiderstand aktiviert.“
> „Die Busabschlusswiderstände sind bei den beiden am weitesten entfernten Modulen zu aktivieren“
> „Zu beachten ist das beim TTE-WEZ Modul werkseitig die CAN-Widerstände eingeschalten sind. Diese sind nun meist zu deaktivieren.“
> „Falsche gesetzte CAN-Widerstände erkennt man oft im Servicescreen wenn die Module kurzzeitig verschwinden.“

### Fund 11.2: BedienModul easy für Komfortlüftung (Tastenmatrix Pos. 1 bis 8)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.hoval.com
- **Lokale Datei:** quellen/TopTronic_E_Kurzbedienung_Lueftung.pdf (Dok.-Nr. 4 216 214 / 02 - 07/18 DE, Seite 1)
- **Datum der Quelle:** 2018
- **Wörtliches Zitat:**
> „Pos. Symbol Bezeichnung/Funktion
> 1 Gewünschte Luftmenge (Kann übersteuert werden.)
> 2 Max. Luftfeuchtigkeit
> 3 Aktives Basisprogramm
> 5 Party (Erhöht die Luftmenge über eine gewünschte Zeitspanne.)
> 7 Informationsbereich
> 8 Hauptmenü“

---

## 12. (Runde 11) TopTronic E Lüftungs-Hauptmenüebenen (Info, Programme, Einstellungen) & Schaltzyklen

### Fund 12.1: Menüstruktur Hauptmenü Lüftung (Seiten 1–3) & Funktionsbereiche
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.hoval.com
- **Lokale Datei:** quellen/TopTronic_E_Kurzbedienung_Lueftung.pdf (Dok.-Nr. 4 216 214 / 02 - 07/18 DE, Seite 4)
- **Datum der Quelle:** 2018
- **Wörtliches Zitat:**
> „Übersicht Hauptmenü
> Seite 1/3 Seite 2/3 Seite 3/3
> Emission (für Fachmann) nur in Kombination mit Heizung
> Analyse Menüpunkt ist aktivierbar
> Visualisierung Menüpunkt nicht aktiv
> Heizkreise nur in Kombination mit Heizung
> Warmwasser nur in Kombination mit Heizung
> Programme - Anpassen Wochenprogramme - Anpassen Tagesprogramme
> Anlage nur in Kombination mit Heizung
> Info - Auswahl Informationsbereich - Detailauswahl Lüftung
> User-Level (für Fachmann) - User-Level PIN-Eingabe
> Service Nur für den Fachmann
> Handbetrieb (für Fachmann) nur in Kombination mit Heizung
> Darstellung - Sprache - Farbschema - Startbildschirm - Hintergrundbeleuchtung - Dauer bis Standby - Anzeige bis Standby - Berechtigung
> Inbetriebnahme Nur für den Fachmann
> Update Nur für den Fachmann
> Energiezentrale Menüpunkt nicht aktiv
> Lüftung Einstellungen Lüftung“
> „Information - Auswahl Informationsbereich - Einstellung Luftmenge - Einstellung Luftfeuchtigkeit - Auswahl Tagesprogramm
> Luftmenge/max. Luftfeuchtigkeit - Auswahl Basisprogramm Basisprogramm
> Luftqualität (optional) Falls installiert, wird die Luftqualität innen und aussen angezeigt“

### Fund 12.2: Individuelle Tagesprogramme / Schaltzyklen & Heizzeiten-Analogie
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.hoval.com
- **Lokale Datei:** quellen/TopTronic_E_Kurzbedienung_Lueftung.pdf (Dok.-Nr. 4 216 214 / 02 - 07/18 DE, Seite 3)
- **Datum der Quelle:** 2018
- **Wörtliches Zitat:**
> „Die individuellen Tagesprogramme / Schaltzyklen stellen Sie auf die selbe Art und Weise ein, wie die Heizzeiten, welche in den Anleitungen TopTronic® E Bedienmodul comfort und comfort plus beschrieben sind.“

---

## 13. (Runde 12) Externe Konstantanforderung Heizen für Lüftungsaufschaltung & BedienModul easy Werteingabe

### Fund 13.1: Externe Konstantanforderung Heizen für Lüftungsaufschaltung (TopTronic E)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 149, Kap. 10.2.21 Externe Konstantanforderung Heizen)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „Wurde bei einem Heizkreis ein Anforderungskontakt definiert, wird zusätzlich die Regelstrategie auf Konstantregelung eingestellt. Der Heizkreis reagiert nun nur mehr auf den Anforderungskontakt. Damit haben Betriebsarten, Schaltzeiten des Heizkreises keine Auswirkung mehr.“
> „Eingang offen: Heizkreis schaltet ab, kein Fortschutz od. Standby (bauseitige Schutzmassnahmen sind vorzusehen)“
> „Eingang geschlossen: Heizkreis arbeitet auf seine eingestellte Konstanttemperatur“
> „Zuordnung Eingang ext. Konstantanforderung Par-ID 30-046“
> „Regelstrategie (Wahl der VL-Sollwertbestimmung) 3: Konstantregelung Par-ID 03-032“
> „Vorlauf Sollwert bei Konstantanforderung Heizen Par-ID 07-036“

### Fund 13.2: Sollwertanpassung Luftmenge und maximale relative Feuchtigkeit (BedienModul easy)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.hoval.com
- **Lokale Datei:** quellen/TopTronic_E_Kurzbedienung_Lueftung.pdf (Seite 2, Basisprogramme & Luftmenge einstellen)
- **Datum der Quelle:** 2018
- **Wörtliches Zitat:**
> „Luftmenge einstellen (und max. Luftfeuchtigkeit) Mittels (+/–) oder durch Direkteingabe (Wert antippen) Luftmenge oder max. Luftfeuchtigkeit anpassen.“
> „Auf Luftmenge oder max. rel. Feuchtigkeit tippen. Luftmenge steigt/sinkt. Luftmenge oder Grenzwert für max. Luftfeuchtigkeit steigt/sinkt auf gewünschten Wert.“

---


- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.hoval.com
- **Lokale Datei:** quellen/TopTronic_E_Kurzbedienung_Lueftung.pdf (Dok.-Nr. 4 216 214 / 02 - 07/18 DE, Seite 1 & 3)
- **Datum der Quelle:** 2018
- **Wörtliches Zitat:**
> „Party Erhöht die Luftmenge über eine gewünschte Zeitspanne.“
> „Möglicher Anlass und Funktion Sie haben abends Gäste. • Betrieb mit der eingegebenen Luftmenge bis zum Ende der gewünschten Zeitspanne (Dauer)“
> „Sie fahren am Nachmittag weg und kommen erst spätabends zurück. • Reduzierte Lüftung bis zum Ende der eingegebenen Zeitspanne (Dauer)“

### Fund 14.2: CAN-Busabschlusswiderstand am HomeVent-Hauptprint HP04 (DIP 5+6) und Topologie-Regel
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Dok.-Nr. 4 214 513 / 04, Seite 40, Kap. 6 Bustopologien und CAN-Abschlusswiderstände)
- **Datum der Quelle:** 2016
- **Wörtliches Zitat:**
> „HomeVent (TTE-HV): Ansicht Ausschnitt Hauptprint HP04 DIP-Schalter auf 5+6 auf ON == Busabschlusswiderstand aktiviert.“
> „Die Busabschlusswiderstände sind bei den beiden am weitesten entfernten Modulen zu aktivieren (siehe nachstehende Beispiele)“
> „Bei grösseren Systemen mit vielen Regelungsmodulen war es sehr schwierig die korrekten CAN-Abschlusswiderstände zuzuschalten da durch die internen CAN-Fixwiderstände das Verhalten beeinflusst wurde. Mit dem weglassen dieser Fixwiderstände (neue Hardware >=V1.00.003) ist es wesentlich einfacher die korrekten CAN-Widerstände zuzuschalten.“

---


- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.hoval.com
- **Lokale Datei:** quellen/TopTronic_E_Kurzbedienung_Lueftung.pdf (Dok.-Nr. 4 216 214 / 02 - 07/18 DE, Seite 3)
- **Datum der Quelle:** 2018
- **Wörtliches Zitat:**
> Gewünschte Dauer und Luftmenge anpassen (+/–) oder durch Direkteingabe (Wert antippen) und mit OK bestätigen.
> Programm "Party" aktiv.“

### Fund 15.2: TopTronic E Adressierung der Bedienmodule (BM / RBM) über Inbetriebnahme-Assistent & DIP-Schalter
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Dok.-Nr. 4 214 513 / 04, Seite 38, Kap. 5 Adressierung BedienModule)
- **Datum der Quelle:** 2016
- **Wörtliches Zitat:**
> „5. Adressierung BedienModule
> Einstellungs-Beispiel : RaumBedienmodul für den 2.Heizkreis
> 1: Inbetriebnahme-Assistent aufrufen
> 2: Adress-Nr. Bedienmodul eingeben
> 3: Regel-Modul Type auswählen und bestätigen“
> „BM … BedienModul
> RBM .. RaumBedienmodul“






