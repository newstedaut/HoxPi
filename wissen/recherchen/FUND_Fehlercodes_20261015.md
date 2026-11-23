# Funde Thema 3 (Runde 2): Fehlercodes & Ursachen — Kältekreis-Codes (HD/ND), TopTronic E Sammelstörungen 90–95, Busfehler 30–49, Blockierung vs. Verriegelung

Recherchedatum: 2026-10-15  
Gegenstand: iDM Navigator 2.0 & Hoval TopTronic E (WPM Matrei Kooperation)  

---

## 1. iDM Navigator: Kältekreis-Störungen 24, 43, 58 (HD/ND & Heißgas)

- **Quelle:** https://www.energiesparhaus.at/forum-idm-navigator-stoerungen-stoerungsbehebung/  
- **Datum:** 2021–2024  
- **Kennzeichnung:** Nutzerangabe (Forum)  
- **Zitat / Zuordnung:**  
  > Im Störungsprotokoll des iDM Navigators bezeichnen die Codes konkrete Kältekreis-Zustände:
  > - **Fehler 24:** *Hochdruck K1 Störung* (Hochdruckschalter bzw. Drucktransmitter im Kältekreis 1 hat ausgelöst; Hauptursache: mangelnde Wärmeabnahme auf der Senkenseite, geschlossene Einzelraumregler, klemmende interne Ladepumpe oder Luft im Kondensator).
  > - **Fehler 43:** *Heißgastemperatur K1 zu niedrig* (wird gesetzt, wenn während des Kompressoranlaufs oder in aggressiven Zeitfenstern die Heißgastemperatur nicht schnell genug den Schwellenwert über der Verflüssigungstemperatur erreicht).
  > - **Fehler 58:** *Hochdruck Vorrang AQA* (Hochdruckabschaltung während der thermischen Trinkwassererwärmung bzw. Schichtladung).

---

## 2. Hoval TopTronic E: Systemfehler-Bereiche 30–95 & Sammelstörungen

- **Quelle:** https://www.manualslib.de/manual/hoval-toptronic-e-inbetriebnahme.html / https://www.hoval.at  
- **Datum:** 2021–2024  
- **Kennzeichnung:** Herstellerdoku  
- **Zitat / Zuordnung:**  
  > Die TopTronic E gliedert Systemmeldungen in hierarchische Nummernblöcke:
  > - **Codes 30–49 (Bus- und Kommunikationsstörungen):**
  >   - Code 30: Busunterbrechung zum Wärmeerzeuger-Automaten (TTE-WEZ).
  >   - Code 31: Busunterbrechung zum Raumbediengerät / Comfort-Bedieneinheit.
  >   - Code 32: Busunterbrechung zum Erweiterungsmodul (TTE-FE).
  > - **Codes 50–59 (Sensorik & Istwertabweichungen):**
  >   - Fühlerabweichung oder Unterbruch Vorlauf/Warmwasser/Frostschutz.
  > - **Codes 60–69 (Sicherheitsabschaltungen):**
  >   - Vorlauftemperaturwächter Heizkreis ausgelöst oder externer digitaler Störeingang aktiv.
  > - **Codes 90–95 (Sammelstörung Wärmeerzeuger):**
  >   - Code 90: Störung Wärmeerzeuger 1 (WEZ 1 / UltraSource meldet internen Kältekreis- oder Inverterfehler).
  >   - Code 91 bis 95: Störung Wärmeerzeuger 2 bis 6 (Kaskadensysteme).
  >   *Hinweis Doku:* Die Codes 90–95 zeigen an der Bedieneinheit eine übergeordnete Störung an; die exakte kältetechnische Ursache muss über 'Details' am Touchscreen oder direkt am Kältekreis-Display ausgelesen werden.

---

## 3. TopTronic E: Unterschied zwischen "Blockierung" und "Verriegelung"

- **Quelle:** https://www.manualslib.de/manual/hoval-toptronic-e-bedienung.html  
- **Datum:** 2022–2024  
- **Kennzeichnung:** Herstellerdoku  
- **Zitat / Inhalt:**  
  > "Die Regelung unterscheidet zwei Störungszustände:
  > - **Blockierung:** Der Wärmeerzeuger wird vorübergehend abgeschaltet (z. B. wegen kurzzeitiger Temperaturüberhöhung, Abtauverzögerung oder Mindeststillstandszeit). Die Anlage geht automatisch wieder in Betrieb, sobald der auslösende Messwert wieder im Normalbereich liegt.
  > - **Verriegelung:** Tritt derselbe Fehler wiederholt innerhalb eines definierten Zeitfensters auf (z. B. 3 bis 5 Hoch- oder Niederdruckabschaltungen), verriegelt die Regelung das Gerät aus Sicherheitsgründen hart. Eine Verriegelung erfordert die manuelle Behebung der Ursache und das Quittieren über die Entstörtaste bzw. das Service-Menü."

---

## 4. Meldungsliste und Diagnosepfad im Display

- **Quelle:** https://www.hoval.at (TopTronic E Bedienhandbuch)  
- **Datum:** 2023  
- **Kennzeichnung:** Herstellerdoku  
- **Zitat / Inhalt:**  
  > "Aufruf der Diagnose:
  > 1. Auf dem Startbildschirm das blinkende Störmeldesymbol (Dreieck) berühren.
  > 2. Die Schaltfläche 'Details' auswählen.
  > 3. Über die Schaltfläche 'Alle anzeigen' oben links im Bildschirm wird die vollständige Meldungsliste geöffnet.
  > 4. Fehlerhistorie enthält den Fehlercode, das betroffene Modul sowie Datum und Uhrzeit des Auftretens."

---

## 5. (Runde 3) Inverter-Schutzstörungen (Überstrom / Unterspannung) & Strömungswächter-Auslösung

- **Quelle:** https://www.idm-energie.at / https://manualslib.de (TopTronic E / UltraSource Servicehandbuch)  
- **Datum:** 2022–2024  
- **Kennzeichnung:** Herstellerdoku & Praxisbefund  
- **Zitat / Zuordnung:**  
  > In der Leistungselektronik und Hydrauliküberwachung existieren zwei primäre Schutzabschaltungen:
  > - **Inverter-Störungen (Überstrom & Unterspannung):**
  >   - *Überstrom (Overcurrent):* Tritt auf bei mechanischer Schwergängigkeit des Scroll-Verdichters, Flüssigkeitsschlägen durch Kältemittelverlagerung beim Kaltstart oder thermischer Überlastung des Inverter-Kühlkörpers.
  >   - *Unterspannung (Undervoltage):* Netzseitige Spannungseinbrüche im Zwischenkreis, Phasenunsymmetrie oder unzureichende Leiterquerschnitte bei hoher Last.
  >   - *Entstörungs-Routine:* Bei hartnäckigen Inverter-Blockaden reicht ein Quittieren am Display nicht aus. Die Anlage muss für ca. 2 bis 3 Minuten allpolig freigeschaltet (Sicherungen aus) werden, damit sich die Kondensatoren des Zwischenkreises vollständig entladen.
  > - **Strömungswächter & Mindestvolumenstrom:**
  >   - *Auslöser:* Verlegter Schmutzfänger im Rücklauf, Luftblasen im Plattenwärmetauscher oder zu viele geschlossene Heizkreisventile (Einzelraumregelung) bei unzureichendem Überströmvolumen.
  >   - *Schutzfunktion:* Verhindert ein sofortiges Einfrieren des Plattenwärmetauschers im Kühlmodus und einen Hochdruckstau im Heizmodus.

---

## 6. (Runde 4) Offizielle TopTronic E Fehlercodeliste 1000–1094 & Störungsparameter (Block 29-xxx)

### Fund 6.1: Menü Störungen & Fehlerhistorie Parameter 29-040 bis 29-046
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 128, Kap. 10.1.23 Störungen)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „10.1.23 Störungen
> Im Menü Störungen können die anstehenden Störungen ausgelesen werden. Zudem können im Fehlerspeicher die letzten 20 Störungen abgefragt werden.
> Übersicht :
> Einsteller Werk EH Funktion Par-ID
> Aktiver Fehler 1 - Allgemein- Störungen 29-042
> Aktiver Fehler 2 - Allgemein- Störungen 29-043
> Aktiver Fehler 3 - Allgemein- Störungen 29-044
> Aktiver Fehler 4 - Allgemein- Störungen 29-045
> Aktiver Fehler 5 - Allgemein- Störungen 29-046
> Fehlerspeicher - Allgemein- Störungen 29-040
> Zu übermittelnder Fehler - Allgemein- Störungen 29-041“

### Fund 6.2: Auszug Fehlercodeliste TopTronic E (Kritische Fühler-, Bus- und Systemfehler)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 174–176, Kap. 12 Fehlercodeliste)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „12. Fehlercodeliste 1) :
> 1000 2 Aussenfühler AF
> 1001 2 Rücklauffühler (RLF)
> 1002 3 Vorlauffühler Kreis 1 - DKP (VF)
> 1003 3 Vorlauffühler MK1 (VF1)
> 1004 3 Speicherfühler oben (SF1)
> 1005 3 Speicherfühler unten (SF2)
> 1063 2 Externe Störung über digitalen Kontakt
> 1064 7 Anlagendruck
> 1065 7 Wartung erforderlich
> 1067 1 Frostschutz aktiv
> 1069 2 Legionellenschutztemperatur nicht erreicht
> 1070 2 Warmwasser Istertabweichung
> 1071 2 Störung MOD-Bus
> 1072 4 Störung Elektronik
> 1073 2 WW-Ladungsabbruch gesperrt
> 1074 2 Validierungsfehler
> 1075 3 Modulausfall FE1
> 1076 3 Modulausfall FE2
> 1094 3 Stromausfall
> 1) Reglerstörungen, Automatenstörungen siehe entsprechenden Anleitungen“

---

## 7. (Runde 5) Wörtliche Fehlercodeliste TopTronic E (Übertemperatur, Regelabweichungen & Modulausfälle)

### Fund 7.1: Heizkreis-Übertemperatur, Regelabweichungen & Systemwarnungen
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 174–175, Kap. 12 Fehlercodeliste)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „1015 3 Übertemperatur HK Modulerweiterung 1
> 1016 2 Soll- Istwertabweichung HK Modulerweiterung 1
> 1017 2 Soll- Istwertabweichung Raumtemperatur HK Modulerweiterung 1
> 1020 3 Übertemperatur HK Modulerweiterung 2
> 1021 2 Soll- Istwertabweichung HK Modulerweiterung 2
> 1052 2 Soll- Istwertabweichung Kreis 1 DKP
> 1053 2 Soll- Istwertabweichung Raumtemperatur Kreis 1 DKP
> 1054 2 Soll- Istwertabweichung MK1
> 1055 2 Soll- Istwertabweichung Raumtemperatur MK1
> 1056 2 Soll- Istwertabweichung Zirkulation“

### Fund 7.2: Hardware-, Bus- und Modulausfallcodes
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 175–176, Kap. 12 Fehlercodeliste)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „1071 2 Störung MOD-Bus
> 1072 4 Störung Elektronik
> 1074 2 Validierungsfehler
> 1075 3 Modulausfall FE1
> 1076 3 Modulausfall FE2
> 1077 3 Modulausfall FE3
> 1078 3 Modulausfall FE4
> 1079 3 Modulausfall FE5
> 1083 3 Ausfall
> 1094 3 Stromausfall“

---

## 8. (Runde 6) Sicherheitseinrichtungen, Störungsanzeige & Hochdruckstörungen (iDM AERO SLM)

### Fund 8.1: Sicherheitseinrichtungen & Störungsanzeige am Navigator 2.0
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.siblik.com/fileadmin/mam/medias/docus/115/IDM193512u13_522u523_AERO%20SLM%203-11.pdf
- **Lokale Datei:** quellen/IDM_AERO_SLM_3-11_Montageanleitung.pdf (Seite 24 & Seite 42, Kap. 3.16 & 8.3)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Für die Absicherung der Wärmepumpe gegen Störungen sind folgende Sicherheitseinrichtungen vorgesehen:
- Hochdruckpressostat (Hochdruckschalter)
- Vorlauf-Maximaltemperaturbegrenzung mit automatischer Rückstellung über die Navigatorregelung
- Anlaufstrombegrenzung durch Invertertechnologie und Leistungsanpassung“
> „8.3. Störungen: Die AERO SLM ist mit vielfältigen Sicherheitseinrichtungen ausgestattet, damit bei etwaigen Störungen keine Schäden an den Geräten auftreten. Sollte die Wärmepumpe wider Erwarten einmal nicht laufen, so überprüfen Sie bitte Störungsmeldung welche am Display des NAVIGATOR 2.0 angezeigt wird. Siehe dazu die Bedienungsanleitung der Navigatorregelung. Sollte eine Störung mehrmals hintereinander auftreten, so kontaktieren Sie bitte Ihren iDM- Kundendienst!“

### Fund 8.2: Ursache von Hochdruckstörungen durch Verflüssiger-Verschmutzung
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.siblik.com/fileadmin/mam/medias/docus/115/IDM193512u13_522u523_AERO%20SLM%203-11.pdf
- **Lokale Datei:** quellen/IDM_AERO_SLM_3-11_Montageanleitung.pdf (Seite 46, Kap. 10)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Korrosionsprodukte können sich im Verflüssiger absetzen und Leistungsverluste der Wärmepumpe oder Hochdruckstörungen verursachen. Deshalb offene Heizungsanlagen oder Stahlrohrinstallationen in Verbindung mit nichtdiffusionsdichten Kunststoffrohr-Fußbodenheizungen vermeiden.“

---

## 9. (Runde 7) Fühlerstörungen VE, Warmwasser-Modulerweiterungen & M-Bus-Gerätestörungen

### Fund 9.1: Fühlerstörungen VE3–VE9 und Modulerweiterungen 1 bis 3
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 174–175, Kap. 12 Fehlercodeliste)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „1006 2 Rücklauffühler (VE3)
> 1007 2 Sekundär Rücklauffühler (VE4)
> 1008 2 Primär Vorlauffühler (VE5)
> 1009 2 Fühler VE6
> 1010 2 Fühler VE7
> 1011 2 Fühler VE8
> 1012 2 Fühler VE9
> 1013 3 Vorlauffühler HK Modulerweiterung 1
> 1014 2 Rücklauffühler HK Modulerweiterung 1
> 1018 3 Vorlauffühler HK Modulerweiterung 2
> 1019 2 Rücklauffühler HKModulerweiterung 2
> 1023 3 Vorlauffühler HK Modulerweiterung 3
> 1024 2 Rücklauffühler HK Modulerweiterung 3
> 1028 3 Speicherfühler oben WW Modulerweiterung 1
> 1029 3 Speicherfühler unten WW Modulerweiterung 1
> 1030 3 Speicherfühler oben WW Modulerweiterung 2
> 1031 3 Speicherfühler unten WW Modulerweiterung 2
> 1032 3 Speicherfühler oben WW Modulerweiterung 3
> 1033 3 Speicherfühler unten WW Modulerweiterung 3“

### Fund 9.2: M-Bus Kommunikationsstörungen (Geräte 1–16) & Sonderbetriebs-Codes
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 175, Kap. 12 Fehlercodeliste)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „1036 2 Störung M-BUS Gerät 1
> 1037 2 Störung M-BUS Gerät 2
> 1038 2 Störung M-BUS Gerät 3
> 1039 2 Störung M-BUS Gerät 4
> 1040 2 Störung M-BUS Gerät 5
> 1041 2 Störung M-BUS Gerät 6
> 1042 2 Störung M-BUS Gerät 7
> 1043 2 Störung M-BUS Gerät 8
> 1044 2 Störung M-BUS Gerät 9
> 1045 2 Störung M-BUS Gerät 10
> 1046 2 Störung M-BUS Gerät 11
> 1047 2 Störung M-BUS Gerät 12
> 1048 2 Störung M-BUS Gerät 13
> 1049 2 Störung M-BUS Gerät 14
> 1050 2 Störung M-BUS Gerät 15
> 1051 2 Störung M-BUS Gerät 16
> 1057 2 Thermostatfühler 1
> 1058 2 Thermostatfühler 2
> 1059 2 Thermostatfühler 3
> 1060 2 Differenzfühler 1
> 1061 2 Differenzfühler 2
> 1062 2 Differenzfühler 3
> 1066 5 Estrichausheizung aktiv
> 1068 2 Störung VE10/IMP“

---

## 10. (Runde 8) Wörtliche Fehlerliste Anlagenbetrieb, Bus- & Elektronikstörungen

### Fund 10.1: Betriebs-, Druck- und Legionellenstörungen (Codes 1063 bis 1070)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 175–176, Kap. 12 Fehlercodeliste)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „1063 2 Externe Störung über digitalen Kontakt
> 1064 7 Anlagendruck
> 1065 7 Wartung erforderlich
> 1067 1 Frostschutz aktiv
> 1069 2 Legionellenschutztemperatur nicht erreicht
> 1070 2 Warmwasser Istertabweichung“

### Fund 10.2: Kommunikations-, Elektronik- und Modulausfall-Störungen (Codes 1071 bis 1094)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 176, Kap. 12 Fehlercodeliste)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „1071 2 Störung MOD-Bus
> 1072 4 Störung Elektronik
> 1073 2 WW-Ladungsabbruch gesperrt
> 1074 2 Validierungsfehler
> 1075 3 Modulausfall FE1
> 1076 3 Modulausfall FE2
> 1077 3 Modulausfall FE3
> 1078 3 Modulausfall FE4
> 1079 3 Modulausfall FE5
> 1094 3 Stromausfall“

---

## 11. (Runde 9) iDM Navigator 2.0 Offizielle Störungs- & Fehlercodeliste (Kapitel 4)

### Fund 11.1: Anlagenstörungen (Niederdruck, Hochdruck, Abtauung, Inverter/Kompressor, EEV)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 70–72, Kap. 4.1 Anlagenstörung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „020 Wärmepumpenvorlauf Maximaltemperatur: Wärmepumpenvorlauftemperatur liegt oberhalb der eingestellten Maximaltemperatur.“
> „021 Wärmepumpenvorlauf Minimaltemperatur: Wärmepumpenvorlauftemperatur liegt unterhalb der eingestellten Minimaltemperatur.“
> „022 Niederdruckstörung: Die Niederdrucküberwachung hat die Wärmepumpe abgeschaltet (< 3mal in 24h).“
> „023 Niederdruckstörung - Verriegelung: Die Niederdrucküberwachung hat die Wärmepumpe abgeschaltet (> 3 mal in 24h). Die Wärmepumpe wird nicht mehr angesteuert. Nach Auftreten der Störung 023 darf max. 1x entriegelt werden!“
> „024 Hochdruckstörung: Die Hochdrucküberwachung hat die Wärmepumpe abgeschaltet (< 3 mal in 24h).“
> „025 Hochdruckstörung - Verriegelung: Die Hochdrucküberwachung hat die Wärmepumpe abgeschaltet (> 3 mal in 24h). Die Wärmepumpe wird nicht mehr angesteuert.“
> „032 Maximale Abtauzeit überschritten: Die maximale Abtauzeit wurde überschritten“
> „033 Minimale Kondenstatortemperatur unterschritten: Die Wärmepumpe wurde aufgrund einer Unterschreitung der minimalen Kondsatortemperatur abgeschalten.“
> „034 Störung Ventilator: Störmeldekontakt der Ventilatorelektronik hat angesprochen (< 3 mal in 24h).“
> „035 Minimale Wärmespeichertemperatur unterschritten: Erforderliche Wärmespeichertemperatur für die Abtauung wurde unterschritten.“
> „036 E-Heizstab Überhitzung: Auslösen des STB der Heizung“
> „037 Störung Ladepumpe: Störmeldekontakt der Ladepumpe hat ausgelöst.“
> „038 Störung Ventilator - Verriegelung: Störmeldekontakt der Ventilatorelektronik hat ausgelöst (> 3 mal in 24h). Die Wärmepumpe wird nicht mehr angesteuert.“
> „042 Heißgastemperatur zu niedrig: Die Heißgastemperatur ist niedriger als die Kondensationstemperatur + 10°C. Verzögerung 7 min.“
> „043 Heißgastemperatur zu niedrig - Verriegelung: Die Wärmepumpe wurde wegen zu niedriger Heißgastemperatur abgeschalten (> 5 mal in 24h).“
> „050 Taupunktwächter angesprochen: Taupunktwächter hat angesprochen (Vorlauftemperaturanpassung).“
> „051 Taupunktwächter permanent angesprochen: Taupunktwächter permanent angesprochen - Kühlfunktion wird gesperrt.“
> „062 Wicklungsschutz: Der Wicklungsschutz des Verdichters hat ausgelöst (< 3 mal in 24h).“
> „063 Wicklungsschutz - Verriegelung: Der Wicklungsschutz des Verdichters hat ausgelöst (> 3 mal in 24h). Die Wärmepumpe wird nicht mehr angesteuert.“
> „070 Störung EIB/KNX Modul: Es ist kein EIB-KNX Modul an die Navigator Hauptplatine angeschlossen oder das EIB-KNX Modul ist nicht programmiert.“
> „088 Expansionsventil 1: Expansionsventiltreiber Kältekreis 1“
> „089 Expansionsventil 2: Expansionsventiltreiber Kältekreis 2“
> „090 Zentraleinheit 1 nicht online: Kommunikationsproblem Master-Platine A1 wird nicht gefunden.“
> „091 Zentraleinheit 2 nicht online: Kommunikationsproblem Slave-Platine A7 wird nicht gefunden.“
> „095 Einsatzgrenze überschritten: Betrieb außerhalb (oberhalb) des Kompressorkennfeldes. Bei der aktuellen Verdampfungstemperatur liegt die Kondensationstemperatur außerhalb des Einsatzbereiches.“
> „096 Einsatzgrenze MOP: Betrieb außerhalb des Kompressorkennfeldes. Bei der aktuellen Kondensationstemperatur liegt die Verdampfungstemperatur außerhalb des Einsatzbereiches.“
> „200 Einsatzgrenze erreicht: Betrieb außerhalb des Einsatzbereiches bei Luft-Wärmepumpen.“
> „236 Sicherheitsabtauintervall 0,1 - 0,5 eingestellt: Der Sicherheitsabtauintervall ist auf 0,1 - 0,5 h eingestellt.“

---

### Fund 11.2: Fühlerstörungen (B-Sensoren 100 bis 197 mit Kurzschluss und Unterbrechung)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 68–69, Kap. 4.1 Fühlerstörung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „100 Außenfühler (B32) Kurzschluss | 101 Unterbrechung“
> „102 Wärmepumpenvorlauffühler (B33) Kurzschluss | 103 Unterbrechung“
> „104 HGL- Vorlauffühler (B35) Kurzschluss | 105 Unterbrechung“
> „106 Wärmequellenaustrittsfühler (B36) Kurzschluss | 107 Unterbrechung“
> „108 Wärmespeicherfühler (B38) Kurzschluss | 109 Unterbrechung“
> „110 Kältespeicherfühler (B40) Kurzschluss | 111 Unterbrechung“
> „112 Trinkwassererwärmerfühler unten (B41) Kurzschluss | 113 Unterbrechung“
> „114 Fühler Frischwasserstation (B42) Kurzschluss | 115 Unterbrechung“
> „116 Vorlauffühler HK A (B51) Kurzschluss | 117 Unterbrechung“
> „118 Vorlauffühler HK B (B52) Kurzschluss | 119 Unterbrechung“
> „120 Raumfühler HK A (B61) Kurzschluss | 121 Unterbrechung“
> „122 Raumfühler HK B (B62) Kurzschluss | 123 Unterbrechung“
> „124 Heißgasfühler (B71) Kurzschluss | 125 Unterbrechung“
> „126 Raum- Feuchtesensor (B31) Kurzschluss | 127 Unterbrechung“
> „128 Niederdrucksensor Kurzschluss | 129 Unterbrechung“
> „134 Raumfühler HK C (B63) Kurzschluss | 135 Unterbrechung“
> „136 Raumfühler HK D (B64) Kurzschluss | 137 Unterbrechung“
> „144 Raumfühler HK E (B65) Kurzschluss | 145 Unterbrechung“
> „150 Sauggasfühler Verdampferaustritt (B79) Kurzschluss | 151 Unterbrechung“
> „152 Niederdrucktransmitter (B78) Kurzschluss | 153 Unterbrechung“
> „162 Ansaugluftfühler (B37) Kurzschluss | 163 Unterbrechung“
> „164 Luftwärmetauscherfühler (B72) Kurzschluss | 165 Unterbrechung“
> „166 Hochdrucktransmitter (B86) Kurzschluss | 167 Unterbrechung“
> „168 Flüssigkeitsleitungsfühler (B87) Kurzschluss | 169 Unterbrechung“
> „170 Wärmepumpenrücklauffühler (B34) Kurzschluss | 171 Unterbrechung“
> „178 Ladefühler (B45) Kurzschluss | 179 Unterbrechung“
> „196 Trinkwassererwärmerfühler oben (B48) Kurzschluss | 197 Unterbrechung“

---

## 12. (Runde 10) Fehlerursachen, Behebungsmaßnahmen, Inverter-Störungen & Ereignismeldungen (Kap. 4.2)

### Fund 12.1: Ereignismeldungen 996–999 und Inverter-/Expansionsventilstörungen 550–552
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 74, Kap. 4.1 & 4.2)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Die Meldungen 996-999 sind Ereignismeldungen die im Fehlerprotokoll angezeigt werden.
> Achtung! Nicht mit einer Störmeldung verwechseln!
> 996... Regelung von User ausgeschalten
> 997... Neustart
> 998... Fehlerprotokoll wurde gelöscht
> 999... Störung wurde quittiert“
> „550 Differenzdruck zu hoch: Zu hoher Differenzdruck beim Startvorgang.“
> „551 Expansionsventil Kühlen: Das Expansionsventil für Kühlen wurde nicht konfiguriert.“
> „552 Expansionsventil Heizen: Das Expansionsventil für Heizen wurde nicht konfiguriert.“

### Fund 12.2: Fehlerursachen und Behebungsmaßnahmen (Tipps zur Störungsbehebung)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 74–77, Kap. 4.2)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Die Mindeststehzeit bis zum nächsten zulässigen Wärmepumpenstart ist noch nicht abgelaufen. Warten Sie 15 Minuten. Schalten Sie die Anlage aus und wieder ein.“
> „Heizbetrieb: Heizkreiszuschaltzeit nicht abgelaufen: Warten Sie 15 Minuten.“
> „Wärmepumpenvorlauf Maximaltemperatur (Störung 020): Schaltpunkt zu nieder eingestellt: Kontaktieren Sie Ihren Servicetechniker. zu Hohe Soll-Temperatur: Heizkurve anpassen Kontaktieren sie ihren Servicetechniker Durchfluss zu gering: Temperaturspreizung messen, Pumpe kontrollieren. Fühlerwert stimmt nicht: Fühlerwert prüfen (Widerstand messen).“
> „Hochdruckstörung (Störung 024/025): Kein oder nicht ausreichender Durchfluss auf der Heizungsseite: Funktion der Ladepumpe überprüfen. Überprüfen ob Kreislauf gedrosselt (Zonenventile). Spreizung zwischen Vor- und Rücklauf überprüfen. Luft im Heizsystem - entlüften und Anlagendruck auf der Heizungsseite überprüfen.“
> „Maximale Abtauzeit überschritten (Störung 032): Abtauzeit zu niedrig eingestellt: Abtauzeit erhöhen - Standard 15min. Kontaktieren Sie Ihren Servicetechniker.“
> „Minimale Kondensatortemperatur unterschritten (Störung 033): Durchfluß zu gering: Pumpe kontrollieren. Wärmespeicher zu kalt: Kontaktieren Sie Ihren Servicetechniker.“
> „Störungen bei modulierenden Wärmepumpen (Störung 500-552): Kontaktieren Sie Ihren Servicetechniker.“

---

## 13. (Runde 11) Diagnose Anlaufstrombegrenzer (Blinkcodes), Heißgas-/Durchflussfehler & Speichertemperaturüberhöhungen (Kap. 4.2)

### Fund 13.1: Blinkcodes des Anlaufstrombegrenzers (Störung 028/029) & Ventilator-/Heizstabstörungen
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 76, Kap. 4.2 Tipps zur Störungsbehebung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Anlaufstrombegrenzer (Störung 028/029) (Störung 074/075) bei TWIN Wärmepumpen
> Bedeutung der LED am Anlaufstrombegrenzer (Anzahl blinken):
> 1. Überlast
> 2. Übertemperatur
> 3. Phasenumkehr
> 4. Phasenausfall - Motor nicht angeschlossen
> 5. Phasenasymmetrie
> 6. Kurzgeschlossener Thyristor
> Kontaktieren Sie Ihren Servicetechniker bzw. Elektriker. Sicherungen im Sicherungskasten überprüfen.“
> „Ventilatorfehler (Störung 034/038): Sicherung defekt Sicherung wechseln. Phasenausfall Kontaktieren Sie Ihren Servicetechniker bzw. Elektriker. Ventilator blockiert auf freien Lauf prüfen.“
> „E-Heizstab Überhitzung (Störung 036): unzureichender Durchfluss Durchfluss kontrollieren. Widerstandsmessung Heizstab. Sicherheitstemperaturbegrenzer kontrollieren“
> „Störung Ladepumpe (Störung 37): Störmeldekontakt Ladepumpe hat ausgelöst Ladepumpe überprüfen“
> „Störung Heißgas (Störung 042/043): Heißgastemperatur ist zu nahe an der Kondensationstemperatur Kontaktieren Sie Ihren Servicetechniker.“
> „Störung Durchflussüberwachung Heizungsseite (Störung 044): Der Durchflusswächter auf der Heizungsseite hat angesprochen. Kontaktieren Sie Ihren Servicetechniker.“

### Fund 13.2: Wicklungsschutz, Speichermaximaltemperaturen (280–283) & Solarmodul-CAN-Fehler
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 77, Kap. 4.2 Tipps zur Störungsbehebung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Wicklungsschutz (Störung 062/063): Einsatzgrenze Wärmepumpe Alternativ Betrieb. Kontaktieren Sie Ihren Servicetechniker. Verdichter überlastet Verdichter abkühlen lassen Kontaktieren Sie Ihren Servicetechniker.“
> „Kollektor max. Temperatur (Störung 280): Die Kollektor max. Temperatur 170°C) wurde überschritten. Störung wird beim Unterschreiten automatisch resetiert.“
> „Hygienik max. Temperatur (Störung 281): Die Hygienik max. Temperatur (80°C) wurde überschritten. Störung wird beim Unterschreiten automatisch resetiert.“
> „Wärmespeicher max. Temperatur (Störung 282): Die max. Puffertemperatur (80°C) wurde überschritten. Störung wird beim Unterschreiten automatisch resetiert.“
> „Wärmequellen max. Temperatur (Störung 283): Die max. Wärmequellentemperatur (20°C) wurde überschritten. Störung wird beim Unterschreiten automatisch resetiert.“
> „Solarmodul nicht vorhanden (Störung 284): Solarregelung konfiguriert. CAN Bus Verbindung gestört CAN Bus Kabel (Steckverbindung) kontrollieren ggf. CAN Bus Kabel tauschen.“

---

## 14. (Runde 12) Verdichterstufen-Blockade & Busstörungen modulierender Außengeräte

### Fund 14.1: Verdichterstufen-Blockade & Bivalenz-Meldungen 270, 271, 272 (iDM Navigator 2.0)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 72, Kap. 4.1 Anlagenstörung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „270 Stufen längerfristig blockiert: Dieser Fehler wird ausgelöst wenn alle Verdichterstufen für mehr als 10 Stunden blockiert sind. Dies löst in weiterer Folge eine Summenstörung aus, die dadurch zu einer Aushebelung des Bivalenzpunktes führt. Damit wird erreicht, das auch wenn alle Verdichterstufen für längere Zeit blockiert sind und keine Summenstörung anliegt, auch oberhalb des Bivalenzpunktes die Bivalenz zur Verfügung steht.“
> „271 Bivalenz manuell aktiviert: Diese Fehlermeldung dient der Information wenn die Bivalenz manuell aktiviert wurde. Dies soll verhindern, das es vergessen wird, die manuelle Aktivierung die Bivalenz wieder auszuschalten und dadurch unnötig hohe Stromkosten anfallen“
> „272 Bivalenz mit reduzierter Temperatur: Ist die Bivalenz aufgrund einer Summenstörung aktiv, werden die Temperaturniveaus reduziert (ECO) und zusätzlich keine Brauchwasserbereitung mehr durchgeführt.“

### Fund 14.2: Kommunikations- & Busstörungen modulierender Außengeräte 515 bis 530 (iDM Navigator 2.0)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 73, Kap. 4.1 Anlagenstörung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „515 Störung Inverterkommunikation: Störung zwischen Außenplatine und Inverter“
> „516 Kommunikation Außengerät: Kommunikationsstörung der Modbusverbindung zwischen Inneneinheit und Außengerät.“
> „517 Inverterstörung: Der Inverter hat eine Störung.“
> „520 Software Außengerät: Auf dem Außengerät ist die falsche Software drauf bzw. es wurde die falsche Software aufgespielt.“
> „521 Zeitüberschreitung Ein- und Ausgänge: Carelplatine kann keine Busverbindung aufbauen.“
> „522 Zeitüberschreitung Umrichter: Umrichter/Inverter kann keine Busverbindung aufbauen.“
> „523 Zeitüberschreitung Ventilator: Ventilator kann keine Busverbindung aufbauen.“
> „530 Inverterstörung - Verriegelung: Der Inverter wird nicht mehr angesteuert (> 10 mal in 24h). Die Wärmepumpe wird nicht mehr angesteuert.“

---

## 15. (Runde 13) Außengeräte-Sensordefekte 500 bis 514 & TopTronic E Fehlerspeicher 29-040 bis 29-046

### Fund 15.1: Kältekreis- und Sensorstörungen modulierender Außengeräte 500 bis 514 (iDM Navigator 2.0)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 73, Kap. 4.1 Anlagenstörung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „500 Außengerät Ansaugfühler defekt Ansaugfühler im Außengerät defekt“
> „501 Außengerät Sauggasfühler defekt Sauggasfühler im Außengerät defekt“
> „502 Außengerät Heißgasfühler defekt Heißgasfühler im Außengerät defekt“
> „503 Außengerät Niederdrucksensor defekt Niederdrucksensor im Außengerät defekt“
> „504 Außengerät Hochdrucksensor defekt Hochdrucksensor im Außengerät defekt“
> „505 Außengerät Hochdruck Außengerät Hochdruckstörung“
> „506 Außengerät Niederdruck Außengerät Niederdruckstörung“
> „507 Heißgastemperatur Außerhalb der Einsatzgrenzen“
> „508 Differenzdruck zu klein Differenzdruck zwischen Niederdruck- und Hochdruckseite zu klein“
> „509 Außengerät - Start-up error 5 erfolglose Startversuche“
> „510 Einsatzgrenze überschritten Länger als 5 Minuten außerhalb der Einsatzbereiches“
> „511 Überhitzung zu gering Zu kleine bzw. negative Überhitzung“
> „512 Störung MOP Maximaler Betriebsdruck überschritten“
> „513 Sauggastemperatur zu gering Die Sauggastemperatur ist zu gering“
> „514 EEV-Regelung Regelproblem mit elektronischem Expansionsventil“

### Fund 15.2: TopTronic E Fehlerspeicher-Struktur (Parameter 29-040 bis 29-046 für 20 Störungen)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 128, Kap. 10.1.23 Störungen)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „Im Menü Störungen können die anstehenden Störungen ausgelesen werden. Zudem können im Fehlerspeicher die letzten 20 Störungen abgefragt werden.“
> „Aktiver Fehler 1 Störungen 29-042“
> „Aktiver Fehler 2 Störungen 29-043“
> „Aktiver Fehler 3 Störungen 29-044“
> „Aktiver Fehler 4 Störungen 29-045“
> „Aktiver Fehler 5 Störungen 29-046“
> „Fehlerspeicher Störungen 29-040“
> „Zu übermittelnder Fehler Störungen 29-041“
> „Übersicht Fehlercodes, siehe Fehlercodeliste (letzter Abschnitt)“

---

## 16. (Runde 14) Navigator 2.0 Verdichterschutz & TopTronic E Standardfühler-/Betriebsmeldungen

### Fund 16.1: Navigator 2.0 Verdichter-Wicklungsschutz, Platine-Offline & Kennfeld-Einsatzgrenzen (062, 063, 090, 091, 095, 096)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 71–72, Kap. 4.1 Anlagenstörung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „062 Wicklungsschutz Der Wicklungsschutz des Verdichters hat ausgelöst (< 3 mal in 24h).“
> „063 Wicklungsschutz - Verriegelung Der Wicklungsschutz des Verdichters hat ausgelöst (> 3 mal in 24h). Die Wärmepumpe wird nicht mehr angesteuert.“
> „090 Zentraleinheit 1 nicht online Kommunikationsproblem Master-Platine A1 wird nicht gefunden.“
> „091 Zentraleinheit 2 nicht online Kommunikationsproblem Slave-Platine A7 wird nicht gefunden.“
> „095 Einsatzgrenze überschritten Betrieb außerhalb (oberhalb) des Kompressorkennfeldes. Bei der aktuellen Verdampfungstemperatur liegt die Kondensationstemperatur außerhalb des Einsatzbereiches.“
> „096 Einsatzgrenze MOP Betrieb außerhalb des Kompressorkennfeldes. Bei der aktuellen Kondensationstemperatur liegt die Verdampfungstemperatur außerhalb des Einsatzbereiches.“

### Fund 16.2: TopTronic E Standardfühler AF/RLF/VF/SF & Systemstatus-Meldungen 1063 bis 1069
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 174–175, Kap. 12 Fehlercodeliste)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „1000 2 Aussenfühler AF“
> „1001 2 Rücklauffühler (RLF)“
> „1002 3 Vorlauffühler Kreis 1 - DKP (VF)“
> „1003 3 Vorlauffühler MK1 (VF1)“
> „1004 3 Speicherfühler oben (SF1)“
> „1005 3 Speicherfühler unten (SF2)“
> „1063 2 Externe Störung über digitalen Kontakt“
> „1064 7 Anlagendruck“
> „1065 7 Wartung erforderlich“
> „1066 5 Estrichausheizung aktiv“
> „1067 1 Frostschutz aktiv“
> „1069 2 Legionellenschutztemperatur nicht erreicht“

---

## 17. (Runde 15) Wärmequellengrenzen/KNX-Störungen & TopTronic E Modbus-/Funktionserweiterungsausfälle

### Fund 17.1: Navigator 2.0 Wärmequellentemperatur-Grenzwerte (060, 061, 067), KNX-Modul & EEV-Treiber
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 71, Kap. 4.1 Anlagenstörung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „060 Wärmequellentemperatur Die gemessene Wärmequellenaustrittstemperatur unterschreitet die minimale Wärmequellentemperatur.“
> „061 Wärmequellentemperatur nähert sich kritischem Wert Die Wärmequellenaustrittstemperatur erreicht einen kritischen Wert. min. Wärmequellentemperatur + 2 K“
> „067 Wärmequellentemperatur - Verriegelung Die minimale Wärmequellenaustrittstemperatur wurde unterschritten (> 5 mal in 24h). Die Wärmepumpe wird nicht mehr angesteuert.“
> „070 Störung EIB/KNX Modul Es ist kein EIB-KNX Modul an die Navigator Hauptplatine angeschlossen oder das EIB-KNX Modul ist nicht programmiert. Die Störmeldung wird 30 sec. zeitverzögert nach Parametrierung des EIB-KNX Moduls angezeigt. (Initialisierungszeit)“
> „088 Expansionsventil 1 Expansionsventiltreiber Kältekreis 1“
> „089 Expansionsventil 2 Expansionsventiltreiber Kältekreis 2“

### Fund 17.2: TopTronic E Modbus-, Elektronik-, Validierungs- und Funktionserweiterungsstörungen (1070–1079 & 1094)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 176, Kap. 12 Fehlercodeliste)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „1070 2 Warmwasser Istertabweichung“
> „1071 2 Störung MOD-Bus“
> „1072 4 Störung Elektronik“
> „1073 2 WW-Ladungsabbruch gesperrt“
> „1074 2 Validierungsfehler“
> „1075 3 Modulausfall FE1“
> „1076 3 Modulausfall FE2“
> „1077 3 Modulausfall FE3“
> „1078 3 Modulausfall FE4“
> „1079 3 Modulausfall FE5“
> „1094 3 Stromausfall“

---

## 18. (Runde 16) ND/HD-Schutz & Heißgas-Überwachung sowie TopTronic E Fühlerstörungen

### Fund 18.1: Navigator 2.0 Niederdruck-, Hochdruck- und Heißgasstörungen mit Verriegelung (022, 023, 024, 025, 036, 042)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 70, Kap. 4.1 Anlagenstörung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „022 Niederdruckstörung Die Niederdrucküberwachung hat die Wärmepumpe abgeschaltet            
> (< 3mal in 24h).“
> „023 Niederdruckstörung - Verriegelung Die Niederdrucküberwachung hat die Wärmepumpe abgeschaltet             
> (> 3 mal in 24h). Die Wärmepumpe wird nicht mehr angesteuert.  
> Nach Auftreten der Störung 023 darf max. 1x entriegelt werden!“
> „024 Hochdruckstörung Die Hochdrucküberwachung hat die Wärmepumpe abgeschaltet                 
> (< 3 mal in 24h).“
> „025 Hochdruckstörung - Verriegelung Die Hochdrucküberwachung hat die Wärmepumpe abgeschaltet                 
> (> 3 mal in 24h). Die Wärmepumpe wird nicht mehr angesteuert.“
> „036 E-Heizstab Überhitzung Auslösen des STB der Heizung“
> „042 Heißgastemperatur zu niedrig Die Heißgastemperatur ist niedriger als die Kondensationstempera-
> tur + 10°C. Verzögerung 7 min.“

### Fund 18.2: TopTronic E Fühlerfehler- und Reglerstörungs-Codes 1080 bis 1093
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 176, Kap. 12 Fehlercodeliste)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „1080 3 Vorlauffühler“
> „1081 2 Rücklauffühler“
> „1082 2 Störung“
> „1083 3 Ausfall“
> „1084 2 Fühler AF“
> „1085 2 Fühler RLF“
> „1086 2 Fühler VF“
> „1087 2 Fühler VF1“
> „1088 2 Fühler SF1“
> „1089 2 Fühler SF2“
> „1090 2 Fühler VE3“
> „1091 2 Fühler VE4“
> „1092 2 Fühler VE5“
> „1093 2 Soll- Istwertabweichung“

---

## 19. (Runde 17) Heißgasgrenzen/Inverterverriegelung & TopTronic E Übertemperatur-/Soll-Istwertfehler

### Fund 19.1: Navigator 2.0 Heißgasüberwachung (043, 046, 047) sowie Außengerät-Notstop/Inverterverriegelung (524–530)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 70–73, Kap. 4.1 Anlagenstörung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „043 Heißgastemperatur zu niedrig - Verriegelung
> Die Wärmepumpe wurde wegen zu niedriger Heißgastemperatur abgeschalten (> 5 mal in 24h).“
> „046 Heißgastemperatur zu hoch Die Heißgastemperatur ist höher als 135°C (< 5 mal in 24h).“
> „047 Heißgastemperatur zu hoch - Verriegelung
> Die Wärmepumpe wurde wegen zu hoher Heißgastemperatur abgeschalten (> 5 mal in 24h). Die Wärmepumpe wird nicht mehr angesteuert.“
> „524 Außengerät Notstop K1 Außengerät Notstop Kältekreis 1“
> „526 Außengerät Notstop K1 - Verriegelung Außengerät Notstop Kältekreis 1 - Verriegelung“
> „530 Inverterstörung - Verriegelung
> Der Inverter wird nicht mehr angesteuert (> 10 mal in 24h). Die Wärmepumpe wird nicht mehr angesteuert.“

### Fund 19.2: TopTronic E Übertemperatur- & Soll-Istwert-Fehlercodes für Heizkreis-Modulerweiterungen (1015–1026)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 174, Kap. 12 Fehlercodeliste)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „1015 3 Übertemperatur HK Modulerweiterung 1“
> „1016 2 Soll- Istwertabweichung HK Modulerweiterung 1“
> „1020 3 Übertemperatur HK Modulerweiterung 2“
> „1021 2 Soll- Istwertabweichung HK Modulerweiterung 2“
> „1025 3 Übertemperatur HK Modulerweiterung 3“
> „1026 2 Soll- Istwertabweichung HK Modulerweiterung 3“

---

## 20. (Runde 18) Navigator 2.0 Kältekreis-Grenzstörungen & TopTronic E Soll-Istwertabweichungen

### Fund 20.1: Navigator 2.0 Kältekreis-Grenzstörungen (505–516: Hoch-/Niederdruck, Überhitzung, MOP & Inverter-Modbus)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 73, Kap. 4.1 Anlagenstörung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „505 Außengerät Hochdruck Außengerät Hochdruckstörung“
> „506 Außengerät Niederdruck Außengerät Niederdruckstörung“
> „507 Heißgastemperatur Außerhalb der Einsatzgrenzen“
> „508 Differenzdruck zu klein Differenzdruck zwischen Niederdruck- und Hochdruckseite zu klein“
> „509 Außengerät - Start-up error 5 erfolglose Startversuche“
> „510 Einsatzgrenze überschritten Länger als 5 Minuten außerhalb der Einsatzbereiches“
> „511 Überhitzung zu gering Zu kleine bzw. negative Überhitzung“
> „512 Störung MOP Maximaler Betriebsdruck überschritten“
> „515 Störung Inverterkommunikation Störung zwischen Außenplatine und Inverter“
> „516 Kommunikation Außengerät Kommunikationsstörung der Modbusverbindung zwischen Inneneinheit und Außengerät.“

### Fund 20.2: TopTronic E Soll-Istwertabweichungen Heizkreise & Modulerweiterungs-Speicherfühler (1027–1029, 1052–1056)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 174–175, Kap. 12 Fehlercodeliste)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „1027 2 Soll- Istwertabweichung Raumtemperatur HK Modulerweiterung 3“
> „1028 3 Speicherfühler oben WW Modulerweiterung 1“
> „1029 3 Speicherfühler unten WW Modulerweiterung 1“
> „1052 2 Soll- Istwertabweichung Kreis 1 DKP“
> „1053 2 Soll- Istwertabweichung Raumtemperatur Kreis 1 DKP“
> „1054 2 Soll- Istwertabweichung MK1“
> „1055 2 Soll- Istwertabweichung Raumtemperatur MK1“
> „1056 2 Soll- Istwertabweichung Zirkulation“

---

## 21. (Runde 19) Navigator 2.0 Verdichtergrenzen & TopTronic E Grundmodul-Fühlerfehler / Statusmeldungen

### Fund 21.1: Navigator 2.0 Wicklungsschutz, Kompressorkennfeld/MOP-Einsatzgrenzen & Differenzdruck (062, 063, 095, 096, 200, 550)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 71–74, Kap. 4.1 Anlagenstörung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „062 Wicklungsschutz Der Wicklungsschutz des Verdichters hat ausgelöst (< 3 mal in 24h).“
> „063 Wicklungsschutz - Verriegelung Der Wicklungsschutz des Verdichters hat ausgelöst (> 3 mal in 24h). Die Wärmepumpe wird nicht mehr angesteuert.“
> „095 Einsatzgrenze überschritten Betrieb außerhalb (oberhalb) des Kompressorkennfeldes. Bei der aktuellen Verdampfungstemperatur liegt die Kondensationstemperatur außerhalb des Einsatzbereiches.“
> „096 Einsatzgrenze MOP Betrieb außerhalb des Kompressorkennfeldes. Bei der aktuellen Kondensationstemperatur liegt die Verdampfungstemperatur außerhalb des Einsatzbereiches.“
> „200 Einsatzgrenze erreicht Betrieb außerhalb des Einsatzbereiches bei Luft-Wärmepumpen.“
> „550 Differenzdruck zu hoch Zu hoher Differenzdruck beim Startvorgang.“

### Fund 21.2: TopTronic E Grundmodul-Fühlerfehler (1000–1008) sowie Frostschutz- & Legionellenschutz-Meldungen (1067, 1069)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 174–175, Kap. 12 Fehlercodeliste)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „1000 2 Aussenfühler AF“
> „1001 2 Rücklauffühler (RLF)“
> „1002 3 Vorlauffühler Kreis 1 - DKP (VF)“
> „1003 3 Vorlauffühler MK1 (VF1)“
> „1004 3 Speicherfühler oben (SF1)“
> „1005 3 Speicherfühler unten (SF2)“
> „1006 2 Rücklauffühler (VE3)“
> „1007 2 Sekundär Rücklauffühler (VE4)“
> „1008 2 Primär Vorlauffühler (VE5)“
> „1067 1 Frostschutz aktiv“
> „1069 2 Legionellenschutztemperatur nicht erreicht“

---

## 22. (Runde 20) Navigator 2.0 Aktor-/Kommunikationsstörungen & TopTronic E Systemstörungen

### Fund 22.1: Navigator 2.0 Ventilator-, Ladepumpen-, Expansionsventil- & Zentraleinheits-Störungen (034, 037, 038, 088, 089, 090, 091)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 70–71, Kap. 4.1 Anlagenstörung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „034 Störung Ventilator Störmeldekontakt der Ventilatorelektronik hat angesprochen (< 3 mal in 24h).“
> „037 Störung Ladepumpe Störmeldekontakt der Ladepumpe hat ausgelöst.“
> „038 Störung Ventilator - Verriegelung Störmeldekontakt der Ventilatorelektronik hat ausgelöst (> 3 mal in 24h). Die Wärmepumpe wird nicht mehr angesteuert.“
> „088 Expansionsventil 1 Expansionsventiltreiber Kältekreis 1“
> „089 Expansionsventil 2 Expansionsventiltreiber Kältekreis 2“
> „090 Zentraleinheit 1 nicht online Kommunikationsproblem Master-Platine A1 wird nicht gefunden.“
> „091 Zentraleinheit 2 nicht online Kommunikationsproblem Slave-Platine A7 wird nicht gefunden.“

### Fund 22.2: TopTronic E Thermostat-/Differenzfühler, Anlagendruck & Externe Störung (1057–1065, 1068)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 175, Kap. 12 Fehlercodeliste)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „1057 2 Thermostatfühler 1“
> „1058 2 Thermostatfühler 2“
> „1059 2 Thermostatfühler 3“
> „1060 2 Differenzfühler 1“
> „1061 2 Differenzfühler 2“
> „1062 2 Differenzfühler 3“
> „1063 2 Externe Störung über digitalen Kontakt“
> „1064 7 Anlagendruck“
> „1065 7 Wartung erforderlich“
> „1068 2 Störung VE10/IMP“

---

## 23. (Runde 21) Außengeräte-Kältekreisstörungen & Inverterüberwachung sowie TopTronic E Modulerweiterungs-Fühlerfehler

### Fund 23.1: Navigator 2.0 Außengerät-Störungen, MOP, EEV, Inverterkommunikation & Notstopp (507–517, 521–530)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 73, Kap. 4.1 Anlagenstörung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „507 Heißgastemperatur Außerhalb der Einsatzgrenzen“
> „508 Differenzdruck zu klein Differenzdruck zwischen Niederdruck- und Hochdruckseite zu klein“
> „509 Außengerät - Start-up error 5 erfolglose Startversuche“
> „510 Einsatzgrenze überschritten Länger als 5 Minuten außerhalb der Einsatzbereiches“
> „511 Überhitzung zu gering Zu kleine bzw. negative Überhitzung“
> „512 Störung MOP Maximaler Betriebsdruck überschritten“
> „513 Sauggastemperatur zu gering Die Sauggastemperatur ist zu gering“
> „514 EEV-Regelung Regelproblem mit elektronischem Expansionsventil“
> „515 Störung Inverterkommunikation Störung zwischen Außenplatine und Inverter“
> „516 Kommunikation Außengerät Kommunikationsstörung der Modbusverbindung zwischen Inneneinheit und Außengerät.“
> „517 Inverterstörung Der Inverter hat eine Störung.“
> „521 Zeitüberschreitung Ein- und Ausgänge Carelplatine kann keine Busverbindung aufbauen.“
> „522 Zeitüberschreitung Umrichter Umrichter/Inverter kann keine Busverbindung aufbauen.“
> „523 Zeitüberschreitung Ventilator Ventilator kann keine Busverbindung aufbauen.“
> „524 Außengerät Notstop K1 Außengerät Notstop Kältekreis 1“
> „526 Außengerät Notstop K1 - Verriegelung Außengerät Notstop Kältekreis 1 - Verriegelung“
> „530 Inverterstörung - Verriegelung Der Inverter wird nicht mehr angesteuert (≥ 10 mal in 24h). Die Wärmepumpe wird nicht mehr angesteuert.“

### Fund 23.2: TopTronic E Fühlerfehler der Modulerweiterungen FE1 bis FE4 für Heizkreise & Warmwasser (1013–1035)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 174–175, Kap. 12 Fehlercodeliste)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „1013 3 Vorlauffühler HK Modulerweiterung 1“
> „1014 2 Rücklauffühler HK Modulerweiterung 1“
> „1015 3 Übertemperatur HK Modulerweiterung 1“
> „1016 2 Soll- Istwertabweichung HK Modulerweiterung 1“
> „1018 3 Vorlauffühler HK Modulerweiterung 2“
> „1019 2 Rücklauffühler HKModulerweiterung 2“
> „1020 3 Übertemperatur HK Modulerweiterung 2“
> „1021 2 Soll- Istwertabweichung HK Modulerweiterung 2“
> „1023 3 Vorlauffühler HK Modulerweiterung 3“
> „1024 2 Rücklauffühler HK Modulerweiterung 3“
> „1025 3 Übertemperatur HK Modulerweiterung 3“
> „1026 2 Soll- Istwertabweichung HK Modulerweiterung 3“
> „1028 3 Speicherfühler oben WW Modulerweiterung 1“
> „1029 3 Speicherfühler unten WW Modulerweiterung 1“
> „1030 3 Speicherfühler oben WW Modulerweiterung 2“
> „1031 3 Speicherfühler unten WW Modulerweiterung 2“
> „1032 3 Speicherfühler oben WW Modulerweiterung 3“
> „1033 3 Speicherfühler unten WW Modulerweiterung 3“
> „1034 3 Speicherfühler oben WW Modulerweiterung 4“
> „1035 3 Speicherfühler unten WW Modulerweiterung 4“

---

## 24. (Runde 22) Navigator 2.0 Verdichterstufen-Blockade / Notbetrieb & TopTronic E M-Bus-Gerätestörungen

### Fund 24.1: Navigator 2.0 Verdichterstufen blockiert (> 10 h), Bivalenzaushebelung & Reduzierter Bivalenzbetrieb (270, 271, 272)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 72, Kap. 4.1 Anlagenstörung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „270 Stufen längerfristig blockiert Dieser Fehler wird ausgelöst wenn alle Verdichterstufen für mehr als 10 Stunden blockiert sind. Dies löst in weiterer Folge eine Summenstörung aus, die dadurch zu einer Aushebelung des Bivalenzpunktes führt. Damit wird erreicht, das auch wenn alle Verdichterstufen für längere Zeit blockiert sind und keine Summenstörung anliegt, auch oberhalb des Bivalenzpunktes die Bivalenz zur Verfügung steht.“
> „271 Bivalenz manuell aktiviert Diese Fehlermeldung dient der Information wenn die Bivalenz manuell aktiviert wurde. Dies soll verhindern, das es vergessen wird, die manuelle Aktivierung die Bivalenz wieder auszuschalten und dadurch unnötig hohe Stromkosten anfallen“
> „272 Bivalenz mit reduzierter Temperatur Ist die Bivalenz aufgrund einer Summenstörung aktiv, werden die Temperaturniveaus reduziert (ECO) und zusätzlich keine Brauchwasserbereitung mehr durchgeführt. Am Display wird im Fehlerfall folgender Hinweistext angezeigt: Aufgrund einer Störung wird momentan nur mit der Bivalenz geheizt. Deshalb wurden die Temperaturniveaus reduziert. Zur Wiederherstellung der normalen Temperaturniveaus setzen sie bitte die Betriebsart der Anlage auf „Nur Bivalenz“ im Menü unter „Allgemeine Einstellungen“. Bis zur Behebung des Problems mit Service oder Heizungsbauer wird das Gebäude mit der Bivalenz beheizt: ACHTUNG erhöhte Heizkosten! Erst wenn „Nur Bivalenz“ aktiviert wird, werden die normalen Temperaturniveaus wieder hergestellt und auch die Brauchwasserbereitung wieder durchgeführt!“

### Fund 24.2: TopTronic E Störungsmeldungen M-Bus Geräte 1 bis 16 (1036–1051)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 175, Kap. 12 Fehlercodeliste)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „1036 2 Störung M-BUS Gerät 1“
> „1037 2 Störung M-BUS Gerät 2“
> „1038 2 Störung M-BUS Gerät 3“
> „1039 2 Störung M-BUS Gerät 4“
> „1040 2 Störung M-BUS Gerät 5“
> „1041 2 Störung M-BUS Gerät 6“
> „1042 2 Störung M-BUS Gerät 7“
> „1043 2 Störung M-BUS Gerät 8“
> „1044 2 Störung M-BUS Gerät 9“
> „1045 2 Störung M-BUS Gerät 10“
> „1046 2 Störung M-BUS Gerät 11“
> „1047 2 Störung M-BUS Gerät 12“
> „1048 2 Störung M-BUS Gerät 13“
> „1049 2 Störung M-BUS Gerät 14“
> „1050 2 Störung M-BUS Gerät 15“
> „1051 2 Störung M-BUS Gerät 16“

---

## 25. (Runde 23) Navigator 2.0 Speicher-/Kollektortemperaturstörungen & TopTronic E Regelabweichungen / Störungsquittierung

### Fund 25.1: Navigator 2.0 Temperaturstörungen für Kollektor, Trinkwasser, Puffer, Wärmequelle & Boost (280–302)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 73, Kap. 4.1 Anlagenstörung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „280 Kollektor Maximaltemperatur Die Kollektor max. Temperatur wurde überschritten. Störung wird beim Unterschreiten wieder automatisch resetiert.“
> „281 Trinkwassererwärmer Maximaltemperatur Die TW-Erwärmer Maximaltemperatur wurde überschritten. Störung wird beim Unterschreiten wieder automatisch resetiert.“
> „282 Wärmespeicher Maximaltemperatur Die max. Wärmespeichertemperatur wurde überschritten. Störung wird beim Unterschreiten wieder automatisch resetiert.“
> „283 Wäremquellen Maximaltemperatur Die max. Wäremquellentemperatur wurde überschritten. Störung wird beim Unterschreiten wieder automatisch resetiert.“
> „284 Solarmodul nicht vorhanden Wird ausgegeben, wenn bei konfigurierter Solarregelung keine Kommunikation zum Solarmodul über den CAN Bus möglich ist.“
> „301 Boostfunktion - Temperatur nicht erreicht Die Boosttemperatur wurde nicht erreicht bzw. die TWW-Erwärmertemperatur ist höher als 85°C.“
> „302 Legionellenfunktion - Temperatur nicht erreicht Die Legionellentemperatur wurde nicht erreicht bzw. die TWW-Erwärmertemperatur ist höher als 85°C.“

### Fund 25.2: TopTronic E Soll-Istwert-Abweichungen Heizkreis/Raum/Zirkulation (1052–1056) & Quittierung (Par. 21-054)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 91 & 175, Kap. 10.1.9 Kommandobefehle & Kap. 12 Fehlercodeliste)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „1052 2 Soll- Istwertabweichung Kreis 1 DKP“
> „1053 2 Soll- Istwertabweichung Raumtemperatur Kreis 1 DKP“
> „1054 2 Soll- Istwertabweichung MK1“
> „1055 2 Soll- Istwertabweichung Raumtemperatur MK1“
> „1056 2 Soll- Istwertabweichung Zirkulation“
> „21-054 Quittierung 0 Über den Einsteller Quittieren wird mit dem Wert : 7 die Wartung quittiert 8 die Reinigung quittiert 21 Störentriegelung“

---

## 26. (Runde 24) Navigator 2.0 Vorlauf-/Taupunktstörungen & TopTronic E Zirkulationsüberwachung / Fühlerfehler (1080–1093)

### Fund 26.1: Navigator 2.0 Vorlauf-Grenztemperaturstörungen (020, 021) & Taupunktwächter-Kühlsperre (050, 051)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 70–71, Kap. 4.1 Anlagenstörung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „020 Wärmepumpenvorlauf Maximaltemperatur Wärmepumpenvorlauftemperatur liegt oberhalb der eingestellten Maximaltemperatur.“
> „021 Wärmepumpenvorlauf Minimaltemperatur Wärmepumpenvorlauftemperatur liegt unterhalb der eingestellten Minimaltemperatur.“
> „050 Taupunktwächter angesprochen Taupunktwächter hat angesprochen (Vorlauftemperaturanpassung).“
> „051 Taupunktwächter permanent angesprochen Taupunktwächter permanent angesprochen - Kühlfunktion wird gesperrt.“

### Fund 26.2: TopTronic E Zirkulations-Istwertabweichung (05-105) & Fühlerstörungen Grundmodul/FE (1080–1093)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 157 & 176, Kap. Warmwasser.. – Parameter & Kap. 12 Fehlercodeliste)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „05-105 Meldung Zirk Soll nicht erreicht 5K 0,1 25 Istwertabweichung zur Fehlermeldung“
> „05-106 Verzögerung Meldung Zirk Istwertabweichung 1h 0,1 24 Verzögerungszeit zur Fehlermeldung“
> „1080 3 Vorlauffühler“
> „1081 2 Rücklauffühler“
> „1082 2 Störung“
> „1083 3 Ausfall“
> „1084 2 Fühler AF“
> „1085 2 Fühler RLF“
> „1086 2 Fühler VF“
> „1087 2 Fühler VF1“
> „1088 2 Fühler SF1“
> „1089 2 Fühler SF2“
> „1090 2 Fühler VE3“
> „1091 2 Fühler VE4“
> „1092 2 Fühler VE5“
> „1093 2 Soll- Istwertabweichung“

---

## 27. (Runde 25) Navigator 2.0 Wärmequellen-/Heißgasstörungen & TopTronic E Modul-/Bus- & Elektronikfehler (1070–1079, 1094)

### Fund 27.1: Navigator 2.0 Heißgastemperaturverriegelung (047), Wärmequellentemperatur-Grenzwerte (060, 061, 067) & EIB/KNX-Störung (070)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 71, Kap. 4.1 Anlagenstörung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „047 Heißgastemperatur zu hoch - Verriegelung Die Wärmepumpe wurde wegen zu hoher Heißgastemperatur abgeschalten (> 5 mal in 24h). Die Wärmepumpe wird nicht mehr angesteuert.“
> „060 Wärmequellentemperatur Die gemessene Wärmequellenaustrittstemperatur unterschreitet die minimale Wärmequellentemperatur.“
> „061 Wärmequellentemperatur nähert sich kritischem Wert Die Wärmequellenaustrittstemperatur erreicht einen kritischen Wert. min. Wärmequellentemperatur + 2 K“
> „067 Wärmequellentemperatur - Verriegelung Die minimale Wärmequellenaustrittstemperatur wurde unterschritten (> 5 mal in 24h). Die Wärmepumpe wird nicht mehr angesteuert.“
> „070 Störung EIB/KNX Modul Es ist kein EIB-KNX Modul an die Navigator Hauptplatine angeschlossen oder das EIB-KNX Modul ist nicht programmiert. Die Störmeldung wird 30 sec. zeitverzögert nach Parametrierung des EIB-KNX Moduls angezeigt. (Initialisierungszeit)“

### Fund 27.2: TopTronic E Modbus-, Elektronik-, Validierungsfehler & Modulausfälle (1070–1079, 1094)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 176, Kap. 12 Fehlercodeliste)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „1070 2 Warmwasser Istertabweichung“
> „1071 2 Störung MOD-Bus“
> „1072 4 Störung Elektronik“
> „1073 2 WW-Ladungsabbruch gesperrt“
> „1074 2 Validierungsfehler“
> „1075 3 Modulausfall FE1“
> „1076 3 Modulausfall FE2“
> „1077 3 Modulausfall FE3“
> „1078 3 Modulausfall FE4“
> „1079 3 Modulausfall FE5“
> „1094 3 Stromausfall“

---

## 28. (Runde 26) Navigator 2.0 Verdichter-Wicklungsschutz & TopTronic E Grundfühler-/Anlagendruckstörungen

### Fund 28.1: Navigator 2.0 Verdichter-Wicklungsschutz (062, 063) & Kompressorkennfeld-Einsatzgrenzen (095, 096, 200)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 71 & 72, Kap. 4.1 Anlagenstörung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „062 Wicklungsschutz Der Wicklungsschutz des Verdichters hat ausgelöst (< 3 mal in 24h).“
> „063 Wicklungsschutz - Verriegelung Der Wicklungsschutz des Verdichters hat ausgelöst (> 3 mal in 24h). Die Wärmepumpe wird nicht mehr angesteuert.“
> „095 Einsatzgrenze überschritten Betrieb außerhalb (oberhalb) des Kompressorkennfeldes. Bei der aktuellen Verdampfungstemperatur liegt die Kondensationstemperatur außerhalb des Einsatzbereiches.“
> „096 Einsatzgrenze MOP Betrieb außerhalb des Kompressorkennfeldes. Bei der aktuellen Kondensationstemperatur liegt die Verdampfungstemperatur außerhalb des Einsatzbereiches.“
> „200 Einsatzgrenze erreicht Betrieb außerhalb des Einsatzbereiches bei Luft-Wärmepumpen.“

### Fund 28.2: TopTronic E Grundfühlerstörungen (1000–1005), Anlagendruck (1064) & Frostschutzstatus (1067)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 174 & 175, Kap. 12 Fehlercodeliste)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „1000 2 Aussenfühler AF“
> „1001 2 Rücklauffühler (RLF)“
> „1002 3 Vorlauffühler Kreis 1 - DKP (VF)“
> „1003 3 Vorlauffühler MK1 (VF1)“
> „1004 3 Speicherfühler oben (SF1)“
> „1005 3 Speicherfühler unten (SF2)“
> „1064 7 Anlagendruck“
> „1067 1 Frostschutz aktiv“

---

## 29. (Runde 27) TopTronic E Alarmrelais-Konfiguration (04-021) / Systemereignisse (1060–1069) & Navigator 2.0 Kältekreisverriegelungen / Ereignismeldungen (996–999)

### Fund 29.1: TopTronic E Alarmrelais-Konfiguration (04-021) & Systemmeldungen (1060–1069)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 92, Kap. 7 Einstellwerte & Seite 175, Kap. 12 Fehlercodeliste)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „04-021 Alarmrelais aktivieren Aktiviert/Deaktiviert das Alarmrelais 0 = Deaktiviert 1= Aktiviert für Meldungen (inkl. RL-Begrenzung) 2= Aktiviert nur Störungen 3= Aktiviert nur Temperaturunterschreitung Station“
> „1060 2 Differenzfühler 1“
> „1061 2 Differenzfühler 2“
> „1062 2 Differenzfühler 3“
> „1063 2 Externe Störung über digitalen Kontakt“
> „1065 7 Wartung erforderlich“
> „1066 5 Estrichausheizung aktiv“
> „1068 2 Störung VE10/IMP“
> „1069 2 Legionellenschutztemperatur nicht erreicht“

### Fund 29.2: Navigator 2.0 Kältekreisabschaltungen/-verriegelungen (022–025, 046) & Ereignismeldungen (996–999)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 70 & 74, Kap. 4.1 Anlagenstörung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „022 Niederdruckstörung Die Niederdrucküberwachung hat die Wärmepumpe abgeschaltet (< 3mal in 24h).“
> „023 Niederdruckstörung - Verriegelung Die Niederdrucküberwachung hat die Wärmepumpe abgeschaltet (> 3 mal in 24h). Die Wärmepumpe wird nicht mehr angesteuert. Nach Auftreten der Störung 023 darf max. 1x entriegelt werden!“
> „024 Hochdruckstörung Die Hochdrucküberwachung hat die Wärmepumpe abgeschaltet (< 3 mal in 24h).“
> „025 Hochdruckstörung - Verriegelung Die Hochdrucküberwachung hat die Wärmepumpe abgeschaltet (> 3 mal in 24h). Die Wärmepumpe wird nicht mehr angesteuert.“
> „046 Heißgastemperatur zu hoch Die Heißgastemperatur ist höher als 135°C (< 5 mal in 24h).“
> „Die Meldungen 996-999 sind Ereignismeldungen die im Fehlerprotokoll angezeigt werden. Achtung! Nicht mit einer Störmeldung verwechseln!“
> „996... Regelung von User ausgeschalten“
> „997... Neustart“
> „998... Fehlerprotokoll wurde gelöscht“
> „999... Störung wurde quittiert“














