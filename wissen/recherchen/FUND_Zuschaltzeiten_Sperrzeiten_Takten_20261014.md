# Recherche-Funde Thema 4: Zuschaltzeiten, Sperrzeiten, Mindestlauf- und Mindeststillstandszeiten, Takten

Datum: 2026-10-14  
Rechercheagent: Antigravity  
Thema: Zuschaltzeiten, Sperrzeiten, Mindestlauf- und Mindeststillstandszeiten, Takten (iDM AERO SLM / Navigator 2.0 sowie Hoval UltraSource B / TopTronic E)

---

### Fund 1: Mindestlaufzeiten des Verdichters
- **Typ:** Herstellerdokumentation (iDM Energiesysteme) & Fachforen
- **Quellen / URLs:** 
  - `https://www.idm-energie.at/`
  - `https://www.energiesparhaus.at/`
- **Datum der Quellen:** 2019–2024
- **Befunde:**
  - **Dauer:** Typischerweise **10 bis 15 Minuten** (Mindestfenster zwischen 5 und 15 Minuten je nach Firmware).
  - **Funktion:** Nach dem Start des Inverter-Verdichters erzwingt die Steuerung (Navigator 2.0 / WFA 200), dass der Kompressor mindestens für diese Zeitspanne in Betrieb bleibt, selbst wenn die Abschalttemperatur kurzzeitig überschritten wird.
  - **Zweck:** Sicherstellung der Kältemittel- und Ölrückführung im Kältekreis, thermische Einschwingung und Vermeidung von Materialermüdung durch Kurzzeitstarts.

---

### Fund 2: Mindeststillstandszeiten & Wiederanlaufsperre (Taktsperre)
- **Typ:** Herstellerdokumentation & Modbus-Spezifikation (iDM / Hoval TopTronic E)
- **Quellen / URLs:**
  - `https://www.idm-energie.at/`
  - `https://community.home-assistant.io/t/hoval-belaria-integration-gateway/692870`
- **Datum der Quellen:** 2020–2024
- **Befunde:**
  - **Dauer:** Nach dem Abschalten des Verdichters wird eine Zwangspause von **10 bis 15 Minuten** eingehalten.
  - **Statusanzeige:** Im Modbus-System der Hoval TopTronic E wird dieser Zustand über den Status-Code `16` (*Restart delay* / Wiederanlaufverzögerung) signalisiert.
  - **Zweck:** Druckausgleich zwischen Hochdruck- und Niederdruckseite im Kältekreis vor dem nächsten Kompressor-Anlauf, Schutz des Inverters und Reduktion von Anlaufstromspitzen.

---

### Fund 3: EVU-Sperrzeiten & Überbrückung
- **Typ:** Herstellerdokumentation (Hoval Planungsunterlagen UltraSource B)
- **Quelle / URL:** `https://www.hoval.com/` (Hoval UltraSource Projektierungsrichtlinien)
- **Datum der Quelle:** 2021
- **Befunde:**
  - Energieversorgungsunternehmen (EVU) können den Betrieb des Kompressors bis zu **3-mal täglich für jeweils bis zu 2 Stunden** sperren (EVU-Abschaltung / Sperrzeit über Rundsteuerempfänger oder Smart-Meter-Relais).
  - Die TopTronic E unterbricht in dieser Zeit die Verdichterfreigabe, während die Heizkreispumpen zur Wärmeverteilung aus dem Speicher oder der Gebäudemasse weiterlaufen dürfen.
  - Auslegungskriterium: Pufferspeicher oder Speichermasse der Fußbodenheizung müssen so dimensioniert sein, dass eine 2-stündige Sperrzeit ohne spürbaren Temperaturabfall im Gebäude überbrückt wird.

---

### Fund 4: Regelungsparameter gegen Takten (Hoval TopTronic E / WFA 200)
- **Typ:** Nutzerangabe & Fachforen (Forum energiesparhaus.at, Thread 56645 u.a.)
- **Quelle / URL:** `https://www.energiesparhaus.at/forum-hoval-ultrasource-lwp-allgemeiner-austausch-und-anlage-optimieren/56645`
- **Datum der Quelle:** 2020–2025
- **Konkrete Parameter:**
  - **Hysterese-Einstellungen (Schaltdifferenzen):**
    - `33-053`: Ausschaltdifferenz DK/WPF Heizen (CRF/WPF) [Standard ca. 1,0 K]  
      -> Abschaltung erfolgt bei: `Vorlauf-Soll + 1,0 K` im Rücklauf.
    - `33-054`: Einschaltdifferenz DK/WPF Heizen (CVF/WPF) [Standard ca. 2,0 bis 2,5 K]  
      -> Wiedereinschaltung erfolgt bei: `Vorlauf-Soll - 2,5 K` im Rücklauf.  
      -> Gesamte Schalthysterese beträgt ca. **3,0 bis 3,5 K**, um die Taktfrequenz in der Übergangszeit gering zu halten.
  - **Inverter-Modulationsgrenzen:**
    - `34-049`: Maximale Leistung Heizen (z. B. auf 40–45 % begrenzt, um Überschwingen in der Übergangszeit zu vermeiden).
    - `34-050`: Minimale Leistung Heizen (untere Modulationsgrenze, z. B. 20 %, um die Anlage möglichst lange auf kleinster Stufe durchlaufen zu lassen).
  - **Sollwert-Dämpfung:**
    - `06-017`: Maximale Sollwertsteigung Heizbetrieb = **1,0 K/min** (verhindert abrupte Leistungsanforderungen und nervöses Hochfahren).

---

### Fund 5: Ursachen für Takten und Optimierungserfahrungen
- **Typ:** Nutzerangabe (energiesparhaus.at Community-Erfahrungen)
- **Quelle / URL:** `https://www.energiesparhaus.at/`
- **Datum der Quelle:** 2020–2025
- **Zentrale Ursachen & Abhilfen:**
  - **Überdimensionierung:** Größere Geräte (z. B. 11–17 kW) können bei milden Außentemperaturen (> 5–10 °C) trotz Modulation nicht unter ihre Mindestleistung (oft ca. 2,5–3 kW thermisch) drosseln. Ist die Heizlast des Hauses geringer, taktet das System zwangsläufig.
  - **Geschlossene Einzelraumregler:** Reduzieren das durchströmte Wasservolumen drastisch, wodurch der Rücklauf rasant ansteigt und die Ausschalttemperatur erreicht wird. Abhilfe: Thermischer Abgleich und Offenhalten der Hauptkreise.
  - **Ziel-Taktzahl:** Anzustreben sind in der Übergangszeit ca. 3–6 Takte pro Tag (inkl. Warmwasser und Abtauzyklen), im Winter Dauerlauf mit Modulation am Stück.