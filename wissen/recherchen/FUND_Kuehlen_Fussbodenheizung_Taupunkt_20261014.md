# Recherche-Funde Thema 6: Kühlen über Fußbodenheizung, Taupunkt

Datum: 2026-10-14  
Rechercheagent: Antigravity  
Thema: Kühlen über Fußbodenheizung, Taupunktüberwachung, Parameter und Herstelleranforderungen (Hoval TopTronic E / UltraSource B comfort C17 & iDM AERO SLM / Navigator 2.0)

---

### Fund 1: Offizielle Hoval TopTronic E Parameter für Kühlbetrieb & Taupunkt
- **Typ:** Herstellerdokumentation (Hoval Technische Unterlagen Steuerung, Dok.-Nr. 4 214 513 / 04, S. 114–115 / S. 138–139 im PDF)
- **Quelle / URL:** `https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf` (Lokal archiviert unter `quellen/Technische_Unterlagen_Steuerung_Hoval.pdf`)
- **Konkrete Parameter & Bedeutungen:**
  - `03-036`: **Kühlgrenze Außentemperatur** [Standard 20 °C, Bereich 15,0–40,0 °C]  
    Bestimmt, ab welcher mittleren Außentemperatur die Kühlfunktion freigegeben bzw. gesperrt wird. Steigt die mittlere Außentemperatur um 0,5 K über den Einstellwert, wird die Kühlung aktiv freigegeben.
  - `03-039`: **Überhöhung Taupunktbegrenzung** [Standard 0 K, Bereich 0,0–10,0 K]  
  - `03-041`: **Abweichung Kühlen aus** [Standard 0 K, Bereich 0,0–10,0 K]  
    Einstellbare Temperaturabweichung zur Soll-Raumtemperatur, ab der der Kühlbetrieb abgeschaltet wird.
  - `03-042`: **Abweichung forciert Kühlen** [Standard 0 K, Bereich 0,0–10,0 K]  
    Temperaturabweichung zur Soll-Raumtemperatur für forcierten Kühlbetrieb.
  - `03-044`: **Einsatzpunkt Sommerkompensation** [Standard 20 °C, Bereich 20,0–30,0 °C]  
    Steigt die Außentemperatur über diesen Wert, steigt der Sollwert für die Raumtemperatur dynamisch mit der eingestellten Steilheit (Schutz vor Unterkühlung bei starker Sommerhitze).
  - `03-045`: **Steilheit Sommerkompensation** [0–100 %]  
    Bestimmt den Einfluss der Außentemperaturänderung auf die Sollwertanhebung im Raum.
  - `03-054`: **Normal Raumtemperatur Kühlbetrieb** [Standard 24 °C, Bereich 10,0–30,0 °C]
  - `03-056`: **Spar Raumtemperatur Kühlbetrieb** [Standard 26 °C, Bereich 20,0–35,0 °C]
  - `07-002`: **Vorlauf Minimaltemperatur** [Standard z. B. 18,0 °C]  
    Begrenzung der Vorlauftemperatur nach unten; verhindert zu kaltes Wasser in der Fußbodenheizung.
  - `07-014`: **Kühlbetrieb Freigabe** [0 = Abgeschaltet, 1 = Frei Mischer zu, 2 = Frei Mischer auf, 3 = Frei Mischer geregelt]

---

### Fund 2: Herstelleranforderungen iDM AERO SLM / Hoval UltraSource B comfort C17
- **Typ:** Herstellerdokumentation (iDM Montageanleitung AERO SLM, Dok.-Nr. 115, Kap. 9.1, S. 44)
- **Quelle / URL:** `https://www.siblik.com/fileadmin/mam/medias/docus/115/IDM193512u13_522u523_AERO%20SLM%203-11.pdf` (Lokal archiviert unter `quellen/IDM_AERO_SLM_3-11_Montageanleitung.pdf`)
- **Zitate & technische Vorgaben:**
  > „Die Anlage muss für die Kühlung ausgelegt sein:
  > * Der Kühlbedarf des Gebäudes und die Abgabeleistung des Verteilsystems müssen mindestens 70 % der Mindestkühlleistung der Wärmepumpe bei A35°C/W18°C betragen.
  > * Mindestvolumen und Mindestvolumenstrom zur Kühlung müssen gewährleistet werden.
  > * Eine Mindestabnahmemenge muss gewährleistet sein oder der NAVIGATOR Pro wird als Zonenregelung eingesetzt.
  > * Taupunktwächter an geeigneter Stelle platzieren.
  > 
  > Kennwerte:
  > - Mindestvolumen: **80 Liter**
  > - Mindestvolumenstrom: **1,01 m³/h**
  > - Mindestabnahmemenge: **2,4 kW**
  > 
  > Werden die angeführten Punkte nicht eingehalten, wird der Taupunktwächter ansprechen und somit einen Kühlbetrieb nicht zulassen. Im Kühlbetrieb muss ein Taupunktwächter an geeigneter Stelle platziert werden (B5 Taupunktwächter).“

---

### Fund 3: Funktionsweise & Praxis stille Kühlung über Fußbodenheizung
- **Typ:** Nutzerangabe & Fachforen (energiesparhaus.at & knx-user-forum.de)
- **Quellen / URLs:**
  - `https://www.energiesparhaus.at/`
  - `https://knx-user-forum.de/`
- **Datum der Quellen:** 2019–2025
- **Befunde:**
  - **Funktionsprinzip:** Stille Kühlung (Flächenkühlung) entzieht dem Raum Wärme über die Strahlung der Bodenfläche; keine Zugluft und geräuschlos.
  - **Taupunktproblematik:** 
    - Bei feuchtwarmer Witterung (z. B. 30 °C Außentemperatur und 65 % relativer Luftfeuchte im Raum) liegt der Taupunkt bei ca. **22,7 °C**. 
    - Sinkt die Oberflächentemperatur des Fußbodens unter diesen Wert, schlägt sich Feuchtigkeit nieder (Rutschgefahr, Parkettschäden).
    - Deshalb muss die Vorlauftemperatur gleitend über dem Taupunkt gehalten werden (Taupunkttemperatur + mindestens 1,5 bis 2,0 K Sicherheitsüberhöhung `03-039`).
  - **Zusammenspiel mit KWL:** Die Kombination mit einer kontrollierten Wohnraumlüftung mit Enthalpiewärmetauscher (Feuchterückgewinnung im Sommer hält die Außenfeuchte draußen) senkt die Raumluftfeuchte und erlaubt niedrigere Kühlvorlauftemperaturen (z. B. 18–19 °C), wodurch die Kühleffizienz deutlich ansteigt.