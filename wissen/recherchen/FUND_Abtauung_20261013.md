# Recherche-Funde Thema 1: Abtauung

Datum: 2026-10-13  
Rechercheagent: Antigravity  
Thema: Abtauung (Gradminuten, Referenzabtauung, Abtaufreigabe, Zwangsabtauung, Abtauintervall)

---

### Fund 1: Mindestanforderungen für Referenzabtauung und Kondensatmenge
- **Typ:** Herstellerdoku (iDM)
- **Quelle / URL:** `https://www.siblik.com/fileadmin/mam/medias/docus/115/IDM193512u13_522u523_AERO%20SLM%203-11.pdf` (Lokal archiviert unter `quellen/IDM_AERO_SLM_3-11_Montageanleitung.pdf`)
- **Datum der Quelle:** 2019 / Revision 115
- **Zitate:**
  > „Bei Luftwärmepumpen muss bei der Inbetriebnahme eine Wärmespeichertemperatur von mindestens 20°C gewährleistet sein, um die erforderliche Temperatur für die Referenzabtauung sicherzustellen.“ (S. 42, Kap. 8.1)
  > „Luftwärmepumpen produzieren im Betrieb Kondensatwasser. Das können beim AERO SLM Außengerät pro Abtauzyklus innerhalb von 2 Minuten, bis zu 6 Liter sein. Der Kondensatablauf muss frostsicher ausgeführt werden.“ (S. 31, Kap. 5.5)
  > „Bei Verwendung von Direktkreisen und Zonenventilen müssen mindestens 25 % der Kreise ständig geöffnet bleiben, damit bei der Abtauung noch genügend Energie zur Verfügung steht. Zwischen Vor- und Rücklauf muss ein Überströmventil installiert werden.“ (S. 44, Kap. 9.1)

---

### Fund 2: Inbetriebnahmeanforderung Raum- und Speichertemperatur bei Hoval UltraSource
- **Typ:** Herstellerdoku (Hoval)
- **Quelle / URL:** `https://www.hoval.at/medias/4221941-02-DE.pdf` (Lokal archiviert unter `quellen/Hoval_UltraSource_B_4221941-02-DE.pdf`)
- **Datum der Quelle:** 2021 / Dok-Nr. 4 221 941 / 02
- **Zitate:**
  > „Bei der Inbetriebnahme muss die Raumtemperatur der beheizten Räume mindestens 15 °C betragen (unter dieser Temperatur ist ein Kompressor-Betrieb nicht möglich, da zu wenig Energie für eine Abtauung vorhanden wäre). Falls ein Energiepufferspeicher vorhanden ist, darf dessen Heizwassertemperatur bei der Inbetriebnahme nicht unter 20 °C liegen.“ (S. 10)
  > „Luftwärmepumpen produzieren im Betrieb Kondensat. Das können bei der Ausseneinheit der UltraSource® B pro Abtauzyklus innerhalb von 2 Minuten bis zu 6 Liter sein.“ (S. 7)

---

### Fund 3: Service- und Regelungsparameter für Abtauung (WFA 200 / Navigator)
- **Typ:** Nutzerangabe (Forum energiesparhaus.at)
- **Quelle / URL:** `https://www.energiesparhaus.at/forum-hoval-ultrasource-lwp-allgemeiner-austausch-und-anlage-optimieren/56645`
- **Datum der Quelle:** 16.02.2020 / Beitrags-ID 56645
- **Zitate:**
  > „Service -> TTE-WEZ -> Automat -> WFA 200 -> Wärmepumpe  
  > Max. Abtauzeit "33-283" = 15min  
  > Temperatur Abtauende "33-281" = 36°  
  > Abtaufreigabetemperatur "33-282" = 25°  
  > Abtauung Abweichungsgradminuten "33-320" = 45kmin  
  > Laufzeit Kondensatablaufheizung Abtauung "33-292" = 20min  
  > Pumpen T-Anteil [P-Anteil] "33-324" = 1,0%/°C  
  > Pumpen I-Anteil "33-325" = 25,0s  
  > Pumpen D-Anteil "33-326" = 18,0s  
  > CP Mindrehzahl "33-327" = 60%“

---

### Fund 4: Modbus TCP Register Betriebsart & Status Abtauung (Navigator 2.0 & TopTronic E)
- **Typ:** Herstellerdoku & Nutzerangabe (GitHub / Modbus-Spezifikation 812170 / Home Assistant)
- **Quellen / URLs:** 
  - `https://community.home-assistant.io/t/hoval-belaria-integration-gateway/692870`
  - iDM Navigator 2.0 Modbus TCP Spezifikation Dok.-Nr. 812170
- **Datum der Quelle:** 2022–2024
- **Zitate / Definitionen:**
  > iDM Register 1090 (Betriebsart Wärmepumpe):
  > 0 = Aus / Standby
  > 1 = Heizbetrieb
  > 2 = Kühlbetrieb
  > 4 = Warmwasser
  > 8 = Abtauung (Defrost)
  >
  > Hoval TopTronic E Wärmeerzeuger Status-Codes (Modbus):
  > 8 = 'Defrost'
  > 16 = 'Restart delay'
  > 18 = 'Primary lead time'
  > 19 = 'Primary run-on time'
  > 44 = 'MOP'
  > 49 = 'Unsuccessful defrost'

---

### Fund 5: Einfluss des Elektroheizstabs beim Abtauen
- **Typ:** Nutzerangabe (Forum energiesparhaus.at)
- **Quelle / URL:** `https://www.energiesparhaus.at/forum-erfahrungsbericht-idm-ipump-a-3-11/47365`
- **Datum der Quelle:** 20.11.2017 bis 2025
- **Zitate:**
  > Diskussion über hohen Stromverbrauch während der Abtauphase, wenn der interne Elektro-Heizstab standardmäßig als Unterstützung zur Abtauung im Kreislaufumkehr-Betrieb hinzugeschaltet wird; Reiner Verdichter-Abtauzyklus liegt bei ca. 0,3 bis 0,4 kWh pro Zyklus.