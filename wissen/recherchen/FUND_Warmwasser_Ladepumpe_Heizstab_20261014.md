# Recherche-Funde Thema 5: Warmwasserladung, Ladepumpe, Umschaltventil, Heizstab-Zuschaltung

Datum: 2026-10-14  
Rechercheagent: Antigravity  
Thema: Warmwasserladung, Ladepumpe, Umschaltventil, Heizstab-Zuschaltung (iDM AERO SLM 6-17 / Navigator 2.0 sowie Hoval UltraSource B comfort C17 / TopTronic E)

---

### Fund 1: Warmwasserladung & Heißgasladetechnik (HGL vs. Vorrangladung)
- **Typ:** Herstellerdokumentation (iDM Energiesysteme & Hoval)
- **Quellen / URLs:**
  - `https://www.idm-energie.at/`
  - `https://www.siblik.com/fileadmin/mam/medias/docus/115/IDM193512u13_522u523_AERO%20SLM%203-11.pdf` (S. 44–45)
  - `https://www.hoval.com/`
- **Datum der Quellen:** 2019–2024
- **Befunde:**
  - **HGL-Technik (Heißgasladung):** 
    - Ca. 15 % der thermischen Energie wird direkt nach dem Verdichter auf hohem Temperaturniveau (bis zu ca. 60–62 °C) abgezweigt und über den HGL-Wärmetauscher in den oberen Speicherbereich (Trinkwasserzone, z. B. Hygienik) eingeschichtet.
    - Die verbleibenden ca. 85 % fließen gleichzeitig mit niedrigerer Vorlauftemperatur (z. B. 30–35 °C) direkt in den Heizkreis.
    - Ermöglicht paralleles Heizen und Warmwasserbereiten ohne ständiges Umschalten und ohne Wirkungsgradverlust des Gesamtsystems.
  - **Vorrangladung:** 
    - Umschaltung der Wärmepumpe rein auf die Trinkwassererwärmung.
    - Inverter-Leistung wird fest oder modulierend vorgegeben (Parameter `34-053` = z. B. 42 % oder konstante Leistung `33-334` = 6,0 kW).

---

### Fund 2: Ladepumpe (Drehzahl, PID-Regelung, Drosselventil)
- **Typ:** Herstellerdokumentation & Fachforen (Forum energiesparhaus.at, Thread 56645)
- **Quellen / URLs:**
  - `https://www.siblik.com/fileadmin/mam/medias/docus/115/IDM193512u13_522u523_AERO%20SLM%203-11.pdf` (Kapitel 9)
  - `https://www.energiesparhaus.at/forum-hoval-ultrasource-lwp-allgemeiner-austausch-und-anlage-optimieren/56645`
- **Datum der Quellen:** 2020–2024
- **Konkrete Parameter & Vorgaben:**
  - **Drosselventil in der HGL-Leitung:** Muss so eingestellt werden, dass die HGL-Ladetemperatur bei einer Drehzahl der Ladepumpe von ca. **25 %** erreicht wird (verhindert Durchmischung der Speicherschichtung).
  - **Parameter `33-335`:** CP Drehzahl Warmwasser = **25 %**
  - **Parameter `33-334`:** Wärmeleistung Warmwasser = **6,0 kW**
  - **PID-Regelung der Ladepumpe (WFA 200 / TopTronic E):**
    - `33-324`: Pumpen P-Anteil = **1,0 %/°C**
    - `33-325`: Pumpen I-Anteil = **25,0 s**
    - `33-326`: Pumpen D-Anteil = **18,0 s**
    - `33-327`: CP Mindestdrehzahl = **30 % bis 60 %**
    - `33-328`: CP Maximaldrehzahl = **50 % bis 100 %**
  - **Schalt- und Nachlaufparameter:**
    - `05-000`: Einschaltdifferenz Warmwasserbereitung = **5,0 K**
    - `05-001`: Überhöhung Ladesollwert = **5,0 K**
    - `05-002`: Warmwasser Ladevorgang = **0,1 h**
    - `05-003`: Pumpennachlauf = **0,5 min**

---

### Fund 3: Umschaltventil (3-Wege-Umschaltkugelhahn)
- **Typ:** Herstellerdokumentation (Hoval UltraSource B comfort)
- **Quelle / URL:** `https://www.hoval.com/` (Hoval UltraSource B Ausführungsunterlagen)
- **Datum der Quelle:** 2021
- **Befunde:**
  - Bei der **Hoval UltraSource B comfort** (baugleich mit iDM AERO SLM Inneneinheit) ist zur Umschaltung zwischen Direktheizkreis und Warmwasserspeicher ein **elektromotorischer 3-Wege-Umschaltkugelhahn** (Schema-Kürzel M73) als Grundausstattung bzw. Warmwasserset vorgesehen.
  - Das Umschaltventil wird potentialfrei bzw. 230V direkt von der Steuerung (TopTronic E / TTE-WEZ) bei Wärmeanforderung umgesteuert.
  - Bei Umschaltung greifen definierte Nachlaufzeiten der Ladepumpe (`05-003` = 0,5 min) und Rampenfunktionen zur Dämpfung der Sollwertsteigung (`06-018` = 3,0 K/min für WW), um hydraulische Schläge und plötzliche Druckspitzen im Kältekreis zu unterbinden.

---

### Fund 4: Heizstab-Zuschaltung (Elektroheizeinsatz / Bivalenz)
- **Typ:** Herstellerdokumentation & Fachforen (Hoval TopTronic E & energiesparhaus.at)
- **Quellen / URLs:**
  - `https://www.hoval.at/`
  - `https://www.energiesparhaus.at/`
- **Datum der Quellen:** 2020–2025
- **Befunde:**
  - **Freigabelogik in TopTronic E / Fachmannebene:**
    - Der Elektroheizeinsatz (EFHK) kann in der Systemkonfiguration selektiv für *Nur Heizen*, *Nur Warmwasser* oder *Heizen + Warmwasser* freigegeben werden.
  - **Zuschaltkriterien bei Warmwasser:**
    1. **Bivalenzpunkt / Außentemperatursperre:** Unterhalb einer parametrierten Grenztemperatur schaltet der Heizstab bei unzureichender Verdichterleistung zur Unterstützung zu.
    2. **Maximaltemperaturgrenze der Wärmepumpe:** Erreicht die Wärmepumpe ihre Verdichter-Einsatzgrenze (ca. 60–62 °C bei R410A) und wird eine höhere Solltemperatur angefordert (z. B. Legionellenschutzprogramm / thermische Desinfektion auf 65 °C, Fehlercode `1069` bei Nichterreichen), übernimmt der E-Heizstab die Nacherwärmung.
    3. **Notbetrieb / Störung:** Bei Verriegelung des Kältekreises (z. B. Fehler 24 Hochdruck oder Fehler 43) übernimmt der Heizstab die Notversorgung.
  - **PV-Überschuss / Smart Grid:**
    - In Verbindung mit Photovoltaik (iDM iON / TopTronic E Modbus Register `76` E-Heizstab-Leistung) kann der Speicher über den Heizstab bei starkem Solarüberschuss bis auf maximal zulässige Speichertemperaturen (z. B. 80–85 °C über externen Sicherheitstemperaturbegrenzer STB) überhitzt werden.