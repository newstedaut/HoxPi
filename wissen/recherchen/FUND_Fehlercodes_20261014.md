# Recherche-Funde Thema 3: Fehlercodes und ihre Ursachen (iDM und Hoval TopTronic E)

Datum: 2026-10-14  
Rechercheagent: Antigravity  
Thema: Fehlercodes und ihre Ursachen (iDM Navigator 2.0 / iPump / AERO SLM sowie Hoval TopTronic E / UltraSource / HomeVent)

---

### Fund 1: Offizielle Hoval TopTronic E Fehlercodeliste (1000–1094)
- **Typ:** Herstellerdokumentation (Hoval Technische Unterlagen Steuerung / Inbetriebnahmeanweisung, Dok.-Nr. 4 214 513 / 04, S. 150–152)
- **Quelle / URL:** `https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf` (Lokal archiviert unter `quellen/Technische_Unterlagen_Steuerung_Hoval.pdf`)
- **Datum der Quelle:** Revision 4 214 513 / 04
- **Wichtigste Fehlercodes & Bedeutungen:**
  - `1000`: Außenfühler AF
  - `1001`: Rücklauffühler (RLF)
  - `1002`: Vorlauffühler Kreis 1 - DKP (VF)
  - `1003`: Vorlauffühler MK1 (VF1)
  - `1004`: Speicherfühler oben (SF1)
  - `1005`: Speicherfühler unten (SF2)
  - `1006`: Rücklauffühler (VE3)
  - `1007`: Sekundär Rücklauffühler (VE4)
  - `1008`: Primär Vorlauffühler (VE5)
  - `1013 / 1018 / 1023`: Vorlauffühler HK Modulerweiterung 1 / 2 / 3
  - `1014 / 1019 / 1024`: Rücklauffühler HK Modulerweiterung 1 / 2 / 3
  - `1015 / 1020 / 1025`: Übertemperatur HK Modulerweiterung 1 / 2 / 3
  - `1016 / 1021 / 1026`: Soll-Istwertabweichung HK Modulerweiterung 1 / 2 / 3
  - `1017 / 1022 / 1027`: Soll-Istwertabweichung Raumtemperatur HK Modulerweiterung 1 / 2 / 3
  - `1028–1035`: Speicherfühler oben / unten Warmwasser Modulerweiterung 1 bis 4
  - `1036–1051`: Störung M-BUS Gerät 1 bis 16
  - `1052`: Soll-Istwertabweichung Kreis 1 DKP
  - `1053`: Soll-Istwertabweichung Raumtemperatur Kreis 1 DKP
  - `1054`: Soll-Istwertabweichung MK1
  - `1055`: Soll-Istwertabweichung Raumtemperatur MK1
  - `1056`: Soll-Istwertabweichung Zirkulation
  - `1057–1059`: Thermostatfühler 1 bis 3
  - `1060–1062`: Differenzfühler 1 bis 3
  - `1063`: Externe Störung über digitalen Kontakt
  - `1064`: Anlagendruck
  - `1065`: Wartung erforderlich
  - `1066`: Estrichausheizung aktiv
  - `1067`: Frostschutz aktiv
  - `1068`: Störung VE10/IMP
  - `1069`: Legionellenschutztemperatur nicht erreicht
  - `1070`: Warmwasser Istwertabweichung
  - `1071`: Störung MOD-Bus
  - `1072`: Störung Elektronik
  - `1073`: WW-Ladungsabbruch gesperrt
  - `1074`: Validierungsfehler
  - `1075–1079`: Modulausfall FE1 bis FE5
  - `1080–1092`: Fühlerstörungen (AF, RLF, VF, VF1, SF1, SF2, VE3–VE5)
  - `1093`: Soll-Istwertabweichung
  - `1094`: Stromausfall

---

### Fund 2: Hoval TopTronic E Basis-Funktions- und Kommunikationsstörungen (30–97)
- **Typ:** Herstellerdokumentation (Hoval Inbetriebnahmeanweisung TopTronic E)
- **Quelle / URL:** `https://www.manualslib.de/` (Hoval TopTronic E Inbetriebnahmeanweisung)
- **Datum der Quelle:** 2018–2021
- **Codes & Bedeutungen:**
  - `30`: Busunterbruch zum Automaten
  - `31–37`: Busstörung Wärmeerzeuger 2 bis 8
  - `42`: Busstörung Fernbedienung
  - `50 / 51`: Vorlauf-Istwertabweichung (VF1 / VF2)
  - `52`: Warmwasser-Istwertabweichung
  - `53`: Pumpendrehzahl entspricht nicht der Reglervorgabe
  - `54`: Legionellenschutztemperatur nicht erreicht
  - `55`: Achtung, Frostschutz aktiv
  - `56`: Solltemperatur Zirkulation nicht erreicht
  - `57`: Maximaltemperatur Zirkulation überschritten
  - `60`: Vorlauftemperaturwächter Heizkreis
  - `61`: Externe Störung über digitalen Eingang
  - `68`: Estrichausheizung aktiv
  - `69`: Reinigung notwendig
  - `70`: Wartung erforderlich
  - `71 / 73`: Fehler beim Laden von Kollektor 1 / Kollektor 2 auf Speicher
  - `90–97`: Störung Wärmeerzeuger 1 bis 8 (Ausfall des jeweiligen WEZ)

---

### Fund 3: Hoval UltraSource Kältekreis- und Modbus-Statusfehler
- **Typ:** Nutzerangabe & Community-Integration (energiesparhaus.at, Home Assistant)
- **Quellen / URLs:**
  - `https://www.energiesparhaus.at/forum-hoval-ultrasource-lwp-allgemeiner-austausch-und-anlage-optimieren/56645`
  - `https://community.home-assistant.io/t/hoval-belaria-integration-gateway/692870`
- **Datum der Quellen:** 2020–2024
- **Befunde:**
  - **Niederdruckstörung (ND-Störung) beim Verdichteranlauf:**
    - Tritt bei der UltraSource gelegentlich beim schnellen Hochmodulieren des Verdichters auf (z. B. nach Umschalten von WW auf Heizen oder bei PV-Anforderung).
    - Ursache: Starker Abfall des Saugdrucks, wenn das elektronische Expansionsventil zu träge nachregelt; führt zur vorübergehenden Sicherheitsabschaltung.
  - **Modbus TCP Kältekreis Status- und Fehlercodes:**
    - `11`: HD fault (Hochdruck-Störung Kältekreis)
    - `12`: Low pressure fault (Niederdruck-Störung Kältekreis)
    - `44`: MOP (Maximum Operating Pressure)
    - `49`: Unsuccessful defrost (Abtauung fehlgeschlagen)
    - `6`: HP temperature too low (Wärmepumpentemperatur zu niedrig)
    - `7`: HP flow too high (Wärmepumpendurchfluss zu hoch)
    - `16`: Restart delay (Wiederanlaufverzögerung)

---

### Fund 4: iDM Navigator 2.0 Kältekreis-Fehlercodes (iPump / AERO / Terra)
- **Typ:** Nutzerangabe & Fachforen (energiesparhaus.at)
- **Quelle / URL:** `https://www.energiesparhaus.at/forum-erfahrungsbericht-idm-ipump-a-3-11/47365`
- **Datum der Quelle:** 2018–2024
- **Fehlercodes & Ursachen:**
  - **Fehler 24 – Hochdruck K1 Störung:**
    - Auslösung des Hochdruckschalters (Pressostat) im Kältekreis 1.
    - Ursachen: Mangelnder Wärmeentzug auf der Heizungsseite (abgeregelte/geschlossene Einzelraumthermostate, Heizkreispumpe bringt zu wenig Durchfluss, Luft im System, Schlamm-/Schmutzansammlung im Verflüssiger).
  - **Fehler 43 – Heißgastemperatur K1 zu niedrig (Verriegelung):**
    - Die Heißgastemperatur nach dem Verdichter unterschreitet den zulässigen Grenzwert.
    - Führt zur Sicherheitsverriegelung der Wärmepumpe zum Verdichterschutz.
    - Ursachen: Sensorfehler, Kältemittelmangel oder unpassende Expansionsventilregelung bei Kaltstart.
  - **Fehler 58 – Hochdruck Vorrang AQA:**
    - Tritt während der Warmwasserbereitung (AQA-Ladefunktion) auf.
    - Ursache: Sehr hohe geforderte Vorlauftemperatur bei gleichzeitig zu geringem Volumenstrom im Speicherladekreis, führt zu raschem Druckanstieg im Kältekreis und Abschaltung über Hochdruck.
  - **Fehler 21 & 22:**
    - Kältekreis-Sicherheitszustände (Niederdruck- und Frostschutzüberwachung).

---

### Fund 5: Hoval HomeVent Störungen und Filteranzeigen
- **Typ:** Herstellerdokumentation (Hoval HomeVent RS-250 / Komfortlüftung)
- **Quellen / URLs:** `https://www.hoval.com/` / `https://www.ersatzfilter-shop.ch/`
- **Datum der Quelle:** 2021
- **Störungs- und Wartungsmeldungen:**
  - **LED Orange:** Filterverschmutzung (Zuluft- / Abluftfilter verschmutzt, Filterwechsel fällig).
  - **LED Rot:** Sammelstörmeldung (Gerät steht still; Ursache: Lüfter-/Motorausfall, thermische Überwachung, Feinsicherung ausgelöst, Frostschutzabschaltung).
  - **Bediengerät bleibt dunkel:** Bus-Kabel (RJ45) unterbrochen oder Gerät stromlos.
  - **Service-Code:** `5836` zur Freischaltung erweiterter Fachmann-Menüs in Verbindung mit TopTronic E.