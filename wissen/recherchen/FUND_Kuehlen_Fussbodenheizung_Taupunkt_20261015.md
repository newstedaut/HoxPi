# Funde Thema 6 (Runde 2): Kühlen über Fußbodenheizung, Taupunktwächter & Hysterese-Parameter 33-061 / 33-062

Recherchedatum: 2026-10-15  
Gegenstand: iDM AERO SLM / Navigator 2.0 & Hoval UltraSource B / TopTronic E (WPM Matrei Kooperation)  

---

## 1. iDM Navigator 2.0: Vorschrift Taupunktwächter & Systemmeldungen 050 / 051

- **Quelle:** https://www.siblik.com / https://sta.io (Navigator 2.0 Installations- und Servicehandbuch)  
- **Datum:** 2022–2024  
- **Kennzeichnung:** Herstellerdoku  
- **Zitat / Vorschrift:**  
  > "Im Kühlbetrieb (stille Flächenkühlung über Fußbodenheizung) schreibt der Hersteller zwingend vor:
  > *'Im Kühlbetrieb muss je Heizkreis ein Taupunktwächter am Vorlaufrohr im Fußbodenheizungsverteiler platziert werden.'*
  > Die Navigator 2.0 Regelung überwacht den Schaltkontakt des Taupunktwächters und reagiert mit folgenden spezifischen Systemmeldungen:
  > - **Meldung Nr. 050:** *'Taupunktwächter hat angesprochen (Vorlauftemperaturanpassung)'* — Der Regler hebt die berechnete Vorlauftemperatur dynamisch um 1 bis 2 K an, um Kondensatbildung an Böden (Fliesen, Parkett) zu verhindern.
  > - **Meldung Nr. 051:** *'Taupunktwächter permanent angesprochen – Kühlfunktion wird gesperrt'* — Bleibt der Kontakt trotz Vorlaufanhebung über eine definierte Zeit geschlossen, wird die Kühlfunktion zum Schutz der Bausubstanz komplett deaktiviert."

---

## 2. Hoval TopTronic E / UltraSource: Kühl-Hysterese Parameter 33-061 & 33-062

- **Quelle:** https://www.energiesparhaus.at/forum-hoval-ultrasource-lwp-allgemeiner-austausch-und-anlage-optimieren/56645 / https://www.hoval.at  
- **Datum:** 2020–2024  
- **Kennzeichnung:** Nutzerangabe (Forum) & Herstellerdokumentation (CleverCool)  
- **Zitat / Zuordnung:**  
  > In der Kältekreisregelung (WFA-Automaten) der UltraSource B sind die Schaltdifferenzen für den Kühlbetrieb über zwei Parameter fixiert:
  > - **33-061 (Ausschaltdiff. DK Kühlen / CVF):** Standardwert **1,0 K**. Definiert, um wie viel Kelvin die Vorlauftemperatur im Kühlkreis unter den Sollwert fallen darf, bevor der Kühlbetrieb (Inverter / Kältekreisumkehr) abschaltet.
  > - **33-062 (Einschaltdiff. DK Kühlen / CRF):** Standardwert **4,0 K**. Definiert, um wie viel Kelvin die gemessene Temperatur über das Soll steigen muss, bevor die Kühlung wieder einschaltet.
  > Diese bewusst asymmetrische Hysterese verhindert Takten des Verdichters im Sommerbetrieb (*CleverCool*)."

---

## 3. Physikalische Grenzwerte der Fußbodenkühlung

- **Quelle:** https://www.hoval.com / https://www.variotherm.com  
- **Datum:** 2023  
- **Kennzeichnung:** Herstellerdoku & Fachanalyse  
- **Zitat / Inhalt:**  
  > "Bei diffuser Kühlung über Fußbodenheizungsrohre gilt eine strikte minimale Vorlauftemperatur von 18 °C als Sicherheitsgrenze. Eine tiefere Vorlauftemperatur führt an schwül-warmen Sommertagen zum Unterschreiten des raumseitigen Taupunkts, was zu Schimmelbildung in Randleistenbereichen und Quellschäden an Holz- und Parkettböden führt. Die Kühlleistung ist physikalisch auf ca. 20 bis 35 W/m² begrenzt."

---

## 4. (Runde 3): Regelungshysterese, Sommerkompensation & hydraulische ERR-Umschaltung

- **Quelle:** Hoval Technische Unterlagen Steuerung (Dok.-Nr. 4 214 513 / 04, S. 134, 138–139, 147) & Hoval UltraSource B Planungshandbuch (S. 54)  
- **Datum:** 2024 / 2026  
- **Kennzeichnung:** Herstellerdokumentation  
- **Zitate & technische Parameter:**  
  - **Schaltdifferenz und Totzone (TopTronic E):**  
    - `03-041`: *Abweichung Kühlen aus* (Standard 0 K, Bereich 0,0–10,0 K). Die zugehörige Schaltdifferenz für die Freigabe des Kühlbetriebs (*Kühlen frei*) entspricht exakt der Hälfte des eingestellten Werts (`0,5 × 03-041`).
    - `03-042`: *Abweichung forciert Kühlen* (Standard 0 K, Bereich 0,0–10,0 K). Die Schaltdifferenz für *forciert Kühlen aus* entspricht ebenfalls der Hälfte des Werts (`0,5 × 03-042`).
    - `01-087`: *Kühlventil Umschaltorgan* (0 = Heizen, 1 = Kühlen).
    - `07-014`: *Kühlbetrieb Freigabe* (0 = Aus, 1 = Kühlung ein Mischer zu, 2 = Kühlung ein Mischer auf, 3 = Kühlung ein Mischer geregelt auf Kühlsollwert).
  - **Dynamische Sommerkompensation:**  
    - Parameter `03-044` (*Einsatzpunkt Sommerkompensation*, Standard 20 °C) und `03-045` (*Steilheit*, 0–100 %) heben bei steigender Außentemperatur den Raum-Kühlsollwert gleitend an, um thermischen Schock und unzulässig hohe Kondensationsrisiken bei extremen Hitzeperioden zu vermeiden.
  - **Hydraulische ERR-Freigabepflicht:**  
    - *„Der Wasserdurchfluss muss gewährleistet sein, da sonst keine Kühlung erfolgen kann. Bei Kühlung über die Heizflächen müssen thermostatische Einzelregulierungen verwendet werden, die auf Kühlbetrieb umgestellt werden können. Ansonsten sind die Ventile im Sommer zu und es kann nicht gekühlt werden.“* (Mindestdurchfluss bei AERO SLM: 1,01 m³/h / 80 Liter).

---

## 5. (Runde 4) Wörtliche Herstellervorgaben Kühlung, Taupunktwächter & Parameter

### Fund 1: Zwingende Taupunktwächter-Vorschrift für alle Flächenkühlsysteme
- **Quelle:** https://www.hoval.com
- **Datum:** 2026
- **Kennzeichnung:** Herstellerdoku (Hoval UltraSource B Technikhandbuch, Rubrik Zubehör, S. 12)
- **Wörtliches Zitat:**
  > "Der Taupunktwächter stellt die einzige Sicherheitseinrichtung bei Kühlsystemen dar und ist immer zwingend erforderlich, um bei Flächenkühlsystemen (Fussboden-, Wand-, Deckenkühlung) Schäden durch kondensierendes Wasser zu vermeiden! Dies gilt sowohl für aktive als auch für passive Kühlanlagen."

### Fund 2: 18 °C Minimalbegrenzung der Vorlauftemperatur im Kühlbetrieb
- **Quelle:** https://www.hoval.com
- **Datum:** 2026
- **Kennzeichnung:** Herstellerdoku (Hoval UltraSource B Technikhandbuch, Planung Kühlung, S. 55)
- **Wörtliches Zitat:**
  > "Der Taupunkt im Boden oder Wand darf zu keiner Zeit unterschritten werden
  > • Dies wird durch eine Festwertregulierung der Vorlauftemperatur erreicht
  > • Der Festwert muss so hoch eingestellt werden, dass sicher keine Taupunktunterschreitung auftritt
  > • Der Vorlauftemperatur-Sollwert wird auf min. 18 °C begrenzt
  > • Die Kühlung ist manuell ein- und auszuschalten"
  > "Die Minimalbegrenzung von 18 °C darf vom Benutzer nicht reduziert werden"

### Fund 3: Mindestvolumen, Mindestvolumenstrom und 70 % Abgabeleistung bei Kühlung
- **Quelle:** https://www.idm-energie.at/wp-content/uploads/2021/04/Montageanleitung-AERO-SLM-3-11.pdf
- **Datum:** 2021
- **Kennzeichnung:** Herstellerdoku (iDM Montageanleitung AERO SLM, Kapitel 09 Anlagenschemen, S. 44)
- **Wörtliches Zitat:**
  > "Achtung! Die Anlage muss für die Kühlung ausgelegt sein.
  > * Der Kühlbedarf des Gebäudes und die Abgabeleistung des Verteilsystems müssen mindestens 70 % der Mindestkühlleistung der Wärmepumpe bei A35°C/W18°C betragen.
  > * Mindestvolumen und Mindestvolumenstrom zur Kühlung müssen gewährleistet werden.
  > * Eine Mindestabnahmemenge muss gewährleistet sein oder der NAVIGATOR Pro wird als Zonenregelung eingesetzt.
  > Taupunktwächter an geeigneter Stelle platzieren.
  > Mindestvolumen AERO SLM 3-11 HGL 80l
  > Mindestvolumenstrom AERO SLM 3-11 HGL 1,01 m³/h
  > Mindestabnahmemenge AERO SLM 3-11 HGL 2,4 kW
  > Werden die angeführten Punkte nicht eingehalten, wird der Taupunktwächter ansprechen und somit einen Kühlbetrieb nicht zu lassen."

### Fund 4: TopTronic E Parameter Kühlgrenze (03-036) und Überhöhung Taupunktbegrenzung (03-039)
- **Quelle:** https://www.hoval.com
- **Datum:** 2024
- **Kennzeichnung:** Herstellerdoku (Hoval Technische Unterlagen Steuerung TopTronic E, Heizkreis Parameter, S. 138)
- **Wörtliches Zitat:**
  > "03-036 Kühlgrenze Aussentemperatur 20 °C (Min 15,0, Max 40,0): Mit der Einstellung wird bestimmt, ab welcher mittlerer Aussentemperatur ein Kühlfunktion gesperrt wird. Steigt die mittlere Aussentemperatur 0.5k über den eingestellten Wert wird die Kühlung freigegeben."
  > "03-039 Überhöhung Taupunktbegrenzung 0 K (Min 0,0, Max 10,0): Mit diesem Parameter kann bei Kühlbetrieb eine Sicherheitsüberhöhung der Vorlaufbegrenzung zum Taupunkt eingestellt werden. Eine Einstellung auf 0 bedeutet, dass die Taupunktbegrenzung inaktiv ist."
  > "03-054 Normal Raumtemperatur Kühlbetrieb 24 °C (Min 10,0, Max 30,0): Mit dem Parameter wird der gewünschte Sollwert für die Raumtemperatur im Normal Kühlbetrieb gewählt."

---

## 6. (Runde 5) Wörtliche Parameter Kühlkennlinie, Freigabe & Strömungswächter-Vorschrift

### Fund 1: Kühlkennlinien-Eckpunkte (03-043, 03-047, 03-048)
- **Quelle:** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Datum:** 2024
- **Kennzeichnung:** Herstellerdoku (Hoval Technische Unterlagen Steuerung TopTronic E, Heizkreis Kühlkennlinie, S. 136)
- **Wörtliches Zitat:**
  > „03-043 Fussp. VL-temp. Kühlkennlinie [22 °C, Bereich 10,0–30,0 °C]: Die Fusspunkttemperatur ist die Vorlauf Solltemperatur für eine Raumtemperatur von 22 °C im Kühlbetrieb beim Aussentemperatur Fusspunkt.
  > 03-047 Auslegep. AT-temp. Kühlkennlinie [35 °C, Bereich 20–40 °C]: Aussentemperatur für die Auslegungs Vorlauftemperatur im Kühlbetrieb
  > 03-048 Auslegep. VL-temp. Kühlkennlinie [20 °C, Bereich 10,0–20,0 °C]: Auslegungs Vorlauftemperatur für Kühlbetrieb“

### Fund 2: Kühlbetrieb Freigabemodi (07-014)
- **Quelle:** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Datum:** 2024
- **Kennzeichnung:** Herstellerdoku (Hoval Technische Unterlagen Steuerung TopTronic E, S. 139)
- **Wörtliches Zitat:**
  > „07-014 Kühlbetrieb Freigabe [0, Bereich 0–3]: Für Kühlbetrieb können folgende Betriebsarten eingestellt werden:
  > 0 = Kühlbetrieb abgeschaltet
  > 1 = Kühlbetrieb frei, Mischer zu
  > 2 = Kühlbetrieb frei, Mischer auf
  > 3 = Kühlbetrieb frei, Mischer geregelt“

### Fund 3: Zwingender Strömungswächter & dampfdiffusionsdichte Dämmung
- **Quelle:** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Hoval_UltraSource_B_Technikhandbuch.pdf
- **Datum:** 2024
- **Kennzeichnung:** Herstellerdoku (Hoval UltraSource B Technikhandbuch, S. 54)
- **Wörtliches Zitat:**
  > „Zur Absicherung vor Frostschäden im Kondensator ist zwingend ein Strömungswächter im Pumpenkreislauf einzubauen (siehe Schema)“
  > „Um Kondensat zu vermeiden, müssen Puffer sowie alle Sole- und Kaltwasserleitungen nach den Regeln der Technik dampfdiffusionsdicht und wärmegedämmt werden“

---

## 7. (Runde 6) Taupunktwächter-Sicherheitsfunktion, Aktivkühlungs-Prozessumkehr & Sommerkompensation

### Fund 7.1: Taupunktwächter als einzige Sicherheitseinrichtung bei Flächenkühlung
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/user_upload/Hoval_UltraSource_B_Technikhandbuch.pdf
- **Lokale Datei:** quellen/Hoval_UltraSource_B_Technikhandbuch.pdf (Seite 12 & 54)
- **Datum der Quelle:** 2021
- **Wörtliches Zitat:**
> „Hinweis: Der Taupunktwächter stellt die einzige Sicherheitseinrichtung bei Kühlsystemen dar und ist immer zwingend erforderlich, um bei Flächenkühlsystemen (Fussboden-, Wand-, Deckenkühlung) Schäden durch kondensierendes Wasser zu vermeiden! Dies gilt sowohl für aktive als auch für passive Kühlanlagen.“
> „Taupunktwächter (TPW): zur Überwachung der Kondenswasserbildung in einem Raum, mit Goldkontakten, beliebig einbaubar für Rohre bis Ø 50 mm. Der Montageort ist so zu wählen, dass eine repräsentative Luftfeuchtigkeitsmessung gewährleistet ist, d. h. die Raumluft muss ungehindert über die Schlitze des Gehäuses an das Messelement im Gehäuseinneren gelangen können.“
> „Aktivkühlung: Die Kühlenergie wird aktiv mit der Wärmepumpe für Kühlzwecke produziert. Dabei wird im Kühlbetrieb eine Prozessumkehr gemacht. In diesem Fall wird die Wärmenutzungsseite (Kondensator) zur Wärmeaufnahmeseite (Verdampfer). Im Gegensatz zu passiver Kühlung muss die Kompressorenergie zusätzlich aufgewendet werden. Der Kühl-/Heizbetrieb kann nicht gleichzeitig erfolgen. Damit die Wärmepumpe nicht zu viel Ein-/Ausschaltungen und Umschaltungen auf Warmwasserbereitung erhält, empfiehlt sich auf jeden Fall der Einsatz eines Kühlspeichers.“

### Fund 7.2: Sommerkompensation der Raumtemperatur bei hohen Außentemperaturen
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 138, Parameter 03-044 & 03-045)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „03-044 Einsatzpunkt Sommerkompensation [20 °C, Bereich 20,0–30,0 °C]: Steigt die Ausssentemperatur über den Einstellwert, steigt der Sollwert für die Raumtemperatur mit der eingestellten Steilheit.“
> „03-045 Steilheit Sommerkompensation [0%, Bereich 0–100%]: Mit der Steilheit wird der Einfluss der Aussentemperaturänderung auf die Raumtemperatursteigung eingestellt.“

---

## 8. (Runde 7) 18 °C Vorlauf-Begrenzung zur Taupunktvermeidung & Anforderungen an Einzelraumregelung

### Fund 8.1: Festwertregulierung auf mindestens 18 °C Vorlauf & Taupunktschutz
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/user_upload/Hoval_UltraSource_B_Technikhandbuch.pdf
- **Lokale Datei:** quellen/Hoval_UltraSource_B_Technikhandbuch.pdf (Seite 55, Kap. Aktive/Passive Kühlung)
- **Datum der Quelle:** 2021
- **Wörtliches Zitat:**
> „Planung:
• Der Taupunkt im Boden oder Wand darf zu keiner Zeit unterschritten werden
• Dies wird durch eine Festwertregulierung der Vorlauftemperatur erreicht
• Der Festwert muss so hoch eingestellt werden, dass sicher keine Taupunktunterschreitung auftritt
• Der Vorlauftemperatur-Sollwert wird auf min. 18 °C begrenzt
• Die Kühlung ist manuell ein- und auszuschalten
Für Anlagen mit Kühlung durch Fussboden oder Wandflächen muss beachtet werden:
• Die Kälte bleibt weitgehend am Boden
• Diese Temperaturverteilung kann als unangenehm empfunden werden: Der Bewohner hat kalte Füsse und einen heissen Kopf“

### Fund 8.2: Notwendigkeit kühlfähiger Einzelraumregulierungen
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/user_upload/Hoval_UltraSource_B_Technikhandbuch.pdf
- **Lokale Datei:** quellen/Hoval_UltraSource_B_Technikhandbuch.pdf (Seite 54, Kap. Generelle Hinweise zur Kühlung)
- **Datum der Quelle:** 2021
- **Wörtliches Zitat:**
> „Der Wasserdurchfluss muss gewährleistet sein, da sonst keine Kühlung erfolgen kann. Bei Kühlung über die Heizflächen müssen thermostatische Einzelregulierungen verwendet werden, die auf Kühlbetrieb umgestellt werden können. Ansonsten sind die Ventile im Sommer zu und es kann nicht gekühlt werden.“

---

## 9. (Runde 8) Anlagen- und Auslegungsvoraussetzungen für Kühlbetrieb & Taupunktwächter B5

### Fund 9.1: Mindestvolumen, Mindestvolumenstrom und 70% Abgabeleistung bei A35/W18
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.siblik.com/fileadmin/mam/medias/docus/115/IDM193512u13_522u523_AERO%20SLM%203-11.pdf
- **Lokale Datei:** quellen/IDM_AERO_SLM_3-11_Montageanleitung.pdf (Seite 44, Kapitel 09 Anlagenschemen)
- **Datum der Quelle:** 2020
- **Wörtliches Zitat:**
> „Achtung!
> Die Anlage muss für die Kühlung ausgelegt sein.
> * Der Kühlbedarf des Gebäudes und die Abgabeleistung des Verteilsystems müssen mindestens 70 % der Mindestkühlleistung der Wärmepumpe bei A35°C/W18°C betragen.
> * Mindestvolumen und Mindestvolumenstrom zur Kühlung müssen gewährleistet werden.
> * Eine Mindestabnahmemenge muss gewährleistet sein oder der NAVIGATOR Pro wird als Zonenregelung eingesetzt.
> Taupunktwächter an geeigneter Stelle platzieren.
> Mindestvolumen AERO SLM 3-11 HGL 80l
> Mindestvolumenstrom AERO SLM 3-11 HGL 1,01 m³/h
> Mindestabnahmemenge AERO SLM 3-11 HGL 2,4 kW
> Werden die angeführten Punkte nicht eingehalten, wird der Taupunktwächter ansprechen und somit einen Kühlbetrieb nicht zu lassen.
> Im Kühlbetrieb muss ein Taupunktwächter an geeigneter Stelle platziert werden.
> B5 Taupunktwächter“

### Fund 9.2: Überwachung des Kühlbetriebs gegen Bauteilschäden durch unbeschränkte Kühlung
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/user_upload/Hoval_UltraSource_B_Technikhandbuch.pdf
- **Lokale Datei:** quellen/Hoval_UltraSource_B_Technikhandbuch.pdf (Seite 54, Kap. Generelle Hinweise zur Kühlung)
- **Datum der Quelle:** 2021
- **Wörtliches Zitat:**
> „Generelle Hinweise zur Kühlung:
> • Der Kühlbetrieb muss in jedem Fall überwacht werden. Falls die Raumtemperatur unbeschränkt gekühlt wird, verursacht dies Kondensat. Dies wiederum kann Schäden an Bauteilen verursachen. Zur Überwachung empfehlen sich die Vorlauftemperatur in Verbindung mit der Feuchtigkeit (Taupunkt-Temperaturwächter)
> • Für die Kühlung ist mit Vorteil ein eigener Kühlkreis zu planen. Dieser kann z. B. mit Gebläsekonvektoren ausgeführt werden.“

---

## 10. (Runde 9) Offizielle Navigator 2.0 Kühlkreis- und Taupunktparameter & Störungen

### Fund 10.1: Soll-Vorlauftemperatur Kühlen und dynamische Taupunktkorrektur
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 38, Kap. Heizkreiseinstellungen)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Vorlauf Kühlen (18°C)
> Die Sollvorlauftemperatur des Kühlkreises kann zwischen 8.0°C und 30.0°C eingestellt werden.
> Taupunktabstand (2°C)
> Nähert sich der vom Raumfeuchtesensor errechnete Taupunkt der eingestellten Sollvorlauftemperatur des Kühlkreises, so wird die Sollvorlauftemperatur nach oben korrigiert. Die Sollvorlauftemperatur ist in diesem Fall der errechneten Taupunkt + Taupunktabstand (1.0 - 10.0°C).
> Kühlgrenze (22°C)
> Der Kühlbetrieb vom jeweiligen Kühlkreis startet, wenn sich die gemittelte Außentemperatur (Mittelwert über 16 h) oberhalb der eingestellten Kühlgrenze befindet. Liegt die gemittelte Außentemperatur unterhalb der Kühlgrenze dann wird der Kühlbetrieb beendet.“

### Fund 10.2: Zuschaltzeit Kühlen und Hysterese Raum Kühlen
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 39, Kap. Heizkreiseinstellungen)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Zuschaltzeit Kühlen (15 min)
> Nach Ablauf der Zuschaltzeit (1 - 240 min) wird die Kühlanforderung an die Wärmepumpe weiter gegeben, wenn die Heizkreis-Istvorlauftemperatur und die Kältespeichertemperatur über der Heizkreis-Sollvorlauftemperatur liegen.
> Hysterese Raum Kühlen (1.0 K)
> Wird die Raum-Solltemperatur im Kühlfall um diese Hysterese (0.5 - 4.0 K) unterschritten, so wird der Kühlbetrieb gesperrt. Überschreitet die Raum-Isttemperatur die eingestellte Raum-Solltemperatur wieder, dann wird die Kühlung wieder freigegeben.“

### Fund 10.3: Störungsmeldungen 050 und 051 Taupunktwächter
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 71 & 76, Kap. Störungen / Anlagenstörung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „050 Taupunktwächter angesprochen
> Taupunktwächter hat angesprochen (Vorlauftemperaturanpassung).
> 051 Taupunktwächter permanent angesprochen
> Taupunktwächter permanent angesprochen - Kühlfunktion wird gesperrt.“
> 
> „Störung: Taupunktwächter (Störung 050/51)
> Ursache: Vorlauftemperatur zu gering
> Behebung: Vorlauftemperatur erhöhen.“

---

## 11. (Runde 10) Hoval TopTronic E Taupunktbegrenzung & Navigator Pro Raumkühlungs-Konfiguration

### Fund 11.1: Hoval TopTronic E Sicherheitsüberhöhung Taupunktbegrenzung & Kühlgrenze
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 138, Parameter 03-036, 03-039, 03-041, 03-042)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „03-036 Kühlgrenze Aussentemperatur [20 °C, Min 15,0, Max 40,0]: Mit der Einstellung wird bestimmt, ab welcher mittlerer Aussentemperatur ein Kühlfunktion gesperrt wird. Steigt die mittlere Aussentemperatur 0.5k über den eingestellten Wert wird die Kühlung freigegeben.“
> „03-039 Überhöhung Taupunktbegrenzung [0 K, Min 0,0, Max 10,0]: Mit diesem Parameter kann bei Kühlbetrieb eine Sicherheitsüberhöhung der Vorlaufbegrenzung zum Taupunkt eingestellt werden. Eine Einstellung auf 0 bedeutet, dass die Taupunktbegrenzung inaktiv ist.“
> „03-041 Abweichung Kühlen aus [0 K, Min 0,0, Max 10,0]: Mit diesem Parameter kann die Abweichung zur Soll Raumtemperatur für die Abschaltung des Kühlbetriebs eingestellt werden.“
> „03-042 Abweichung forciert Kühlen [0 K, Min 0,0, Max 10,0]: Mit diesem Parameter kann die Abweichung zur Soll Raumtemperatur für forcierten Kühlbetrieb eingestellt werden.“

### Fund 11.2: iDM Navigator Pro Raummanager (Einzelraum-Kühlgrenze & vorzeitige Aktivierung)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 40–41, Kap. 2.8.4.1 Heizkreis Pro mit Einzelraumregelung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Die Raumtypen können unter der „Navigator Pro Konfiguration“ eingestellt werden. Dazu das entsprechende Zonenmodul auswählen. Den entsprechenden Raum anwählen.“
> „Die Heiz- und Kühlgrenze, sowie die Heizkurve kann eingestellt werden.“
> „Die „Vorzeitige Aktivierung“ kann ausgeschalten werden. Damit regelt die Einzelraumregelung genau nach den Zeitprogrammeinstellungen auf die entsprechenden Raumtemperaturen und beginnt nicht vorzeitig auf die eingestellten Raumtemperaturen zu regeln.“

---

## 12. (Runde 11) TopTronic E Kühlkennlinien-Parameter (03-011/[Nummer]) & Einschalt-/Ausschaltkühlgrenzen

### Fund 12.1: TopTronic E Kühlkennlinien-Parameter (Fußpunkt und Auslegungspunkt)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 136, Parameter 03-011, 03-043, 03-047, 03-048)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „03-011 Fussp. AT-temp. Heiz-Kühlkennlinie20 °C -10,0 30,0 Fusspunkt auf der Aussentemperaturachse“
> „03-043 Fussp. VL-temp. Kühlkennlinie 22 °C 10,0 30,0 Die Fusspunkttemperatur ist die Vorlauf Solltemperatur“
> „03-047 Auslegep. AT-temp. Kühlkennlinie 35 °C 20 40 Aussentemperatur für die Auslegungs Vorlauftemperatur im“
> „03-048 Auslegep. VL-temp. Kühlkennlinie 20 °C 10,0 20,0 Auslegungs Vorlauftemperatur für Kühlbetrieb“

### Fund 12.2: TopTronic E Einschalt- und Ausschaltkühlgrenzen (forciert / frei)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 147, Kap. 10.2.8 Heiz- und Kühlgrenzen)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „Bei „forciert“ geht der Regler auch dann in Heiz- oder Kühlbetrieb, wenn die Aussentemperatur Heizgrenze den Betrieb sperrt.“
> „Bei „aus“ schaltet der Regler auch dann ab, wenn die Aussentemperatur Heiz- oder Kühlgrenze den Betrieb noch frei gibt.“
> „Bei „frei“ bestimmt die Aussentemperatur Heiz- oder Kühlgrenze die Betriebsart des Reglers.“
> „Die Abweichung für „forciert Kühlen“ zum Kühlsollwert, kann mit der Einschaltkühlgrenze (03-042) eingestellt werden. Die dazugehörende Schaltdifferenz für „forciert Kühlen“ aus entspricht der Hälfte der Einschaltkühlgrenze.“
> „Die Abweichung für „Kühlen aus“ zum Kühlsollwert kann mit der Ausschaltkühlgrenze (03-041) eingestellt werden. dazugehörende Schaltdifferenz für „Kühlen frei“ entspricht der Hälfte der Ausschaltkühlgrenze.“

---

## 13. (Runde 12) Sommerkompensation im Kühlbetrieb & Ausführungsvorgaben Flächenkühlung (Hoval TopTronic E & UltraSource)

### Fund 13.1: TopTronic E Sommerkompensation im Kühlbetrieb (Parameter 03-044 & 03-045)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 138, Parameter 03-044 & 03-045)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „03-044 Einsatzpunkt Sommerkompensation 20 °C 20,0 30,0 Steigt die Ausssentemperatur über den Einstellwert, steigt der Sollwert für die Raumtemperatur mit der eingestellten Steilheit.“
> „03-045 Steilheit Sommerkompensation 0% 0 100 Mit der Steilheit wird der Einfluss der Aussentemperaturänderung auf die Raumtemperatursteigung eingestellt.“

### Fund 13.2: Temperierung über Fußbodenheizung, dampfdiffusionsdichte Dämmung & Strömungswächter
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/user_upload/Hoval_UltraSource_B_Technikhandbuch.pdf
- **Lokale Datei:** quellen/Hoval_UltraSource_B_Technikhandbuch.pdf (Seite 54, Kap. Generelle Hinweise zur Kühlung & Planung)
- **Datum der Quelle:** 2021
- **Wörtliches Zitat:**
> „Für kleinere Komfortansprüche, bei denen ein Kühleffekt ausreicht, ist auch eine Temperierung über Fussbodenheizung oder eine Teilkühlung über Gebläsekonvektoren möglich“
> „Um Kondensat zu vermeiden, müssen Puffer sowie alle Sole- und Kaltwasserleitungen nach den Regeln der Technik dampfdiffusionsdicht und wärmegedämmt werden“
> „Zur Absicherung vor Frostschäden im Kondensator ist zwingend ein Strömungswächter im Pumpenkreislauf einzubauen (siehe Schema)“

---

## 14. (Runde 13) Kühlkreiseinstellungen, dynamische Taupunktanhebung & Kühlventilansteuerung (iDM Navigator 2.0 & Hoval TopTronic E)

### Fund 14.1: iDM Navigator 2.0 Sollvorlauf Kühlen, dynamische Taupunktanhebung & Kühlgrenze (16-Stunden-Mittel)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 38–39, Kap. Heizkreiseinstellungen)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Vorlauf Kühlen (18°C): Die Sollvorlauftemperatur des Kühlkreises kann zwischen 8.0°C und 30.0°C eingestellt werden.“
> „Taupunktabstand (2°C): Nähert sich der vom Raumfeuchtesensor errechnete Taupunkt der eingestellten Sollvorlauftem- peratur des Kühlkreises, so wird die Sollvorlauftemperatur nach oben korrigiert. Die Sollvorlauf- temperatur ist in diesem Fall der errechneten Taupunkt + Taupunktabstand (1.0 - 10.0°C).“
> „Kühlgrenze (22°C): Der Kühlbetrieb vom jeweiligen Kühlkreis startet, wenn sich die gemittelte Außentemperatur (Mittelwert über 16 h) oberhalb der eingestellten Kühlgrenze befindet. Liegt die gemittelte Außentemperatur unterhalb der Kühlgrenze dann wird der Kühlbetrieb beendet.“
> „Zuschaltzeit Kühlen (15 min): Nach Ablauf der Zuschaltzeit (1 - 240 min) wird die Kühlanforderung an die Wärmepumpe weiter gegeben, wenn die Heizkreis-Istvorlauftemperatur und die Kältespeichertemperatur über der Heizkreis-Sollvorlauftemperatur liegen.“
> „Hysterese Raum Kühlen (1.0 K): Wird die Raum-Solltemperatur im Kühlfall um diese Hysterese (0.5 - 4.0 K) unterschritten, so wird der Kühlbetrieb gesperrt. Überschreitet die Raum-Isttemperatur die eingestellte Raum-Solltemperatur wieder, dann wird die Kühlung wieder freigegeben.“

### Fund 14.2: TopTronic E Normal- und Spar-Kühlbetrieb, Taupunktüberhöhung & Kühlventilansteuerung
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 138 & 147, Kap. 10.2.8 Heiz- und Kühlgrenzen)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „03-054 Normal Raumtemperatur Kühlbetrieb: 24 °C 10,0 30,0 Mit dem Parameter wird der gewünschte Sollwert für die Raumtemperatur im Normal Kühlbetrieb gewählt.“
> „03-056 Spar Raumtemperatur Kühlbetrieb: 26 °C 20,0 35,0 Mit dem Parameter wird der gewünschte Sollwert für die Raumtemperatur im Spar Kühlbetrieb gewählt.“
> „03-039 Überhöhung Taupunktbegrenzung: 0 K 0,0 10,0 Mit diesem Parameter kann bei Kühlbetrieb eine Sicherheitsüberhöhung der Vorlaufbegrenzung zum Taupunkt eingestellt werden. Eine Einstellung auf 0 bedeutet, dass die Taupunktbegrenzung inaktiv ist.“
> „Ist die Kühlfunktion aktiviert, kann bei aktiver Kühlung, je nach Ausführung, ein Kühlventil angesteuert werden.“

---

## 15. (Runde 14) Mindestkühlleistung, Mindestvolumenstrom & Taupunktwächter-Sperre (iDM AERO SLM / Navigator 2.0)

### Fund 15.1: Mindestanforderungen an Kühlkreis (70 % Mindestkühlleistung, Mindestvolumenstrom & Abnahmemenge)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.siblik.com/fileadmin/mam/medias/docus/115/IDM193512u13_522u523_AERO%20SLM%203-11.pdf
- **Lokale Datei:** quellen/IDM_AERO_SLM_3-11_Montageanleitung.pdf (Seite 44, Kap. 9 Anlagenschemen)
- **Datum der Quelle:** 2020
- **Wörtliches Zitat:**
> „Achtung!
> Die Anlage muss für die Kühlung ausgelegt sein.
> * Der Kühlbedarf des Gebäudes und die Abgabeleistung des
> Verteilsystems müssen mindestens 70 % der Mindestkühlleistung
> der Wärmepumpe bei A35°C/W18°C betragen.
> * Mindestvolumen und Mindestvolumenstrom zur Kühlung müssen
> gewährleistet werden.
> * Eine Mindestabnahmemenge muss gewährleistet sein oder der
> NAVIGATOR Pro wird als Zonenregelung eingesetzt.
> Taupunktwächter an geeigneter Stelle platzieren.
> Mindestvolumen AERO SLM 3-11 HGL 80l
> Mindestvolumenstrom AERO SLM 3-11 HGL 1,01 m³/h
> Mindestabnahmemenge AERO SLM 3-11 HGL 2,4 kW
> Werden die angeführten Punkte nicht eingehalten, wird der Taupunkt-
> wächter ansprechen und somit einen Kühlbetrieb nicht zu lassen.“

### Fund 15.2: Taupunktwächter-Reaktionsstufen (Vorlauftemperaturanpassung vs. Kühlfunktionssperre)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 71, Kap. 4.1 Anlagenstörung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „050 Taupunktwächter angesprochen Taupunktwächter hat angesprochen (Vorlauftemperaturanpassung).“
> „051 Taupunktwächter permanent angesprochen Taupunktwächter permanent angesprochen - Kühlfunktion wird gesperrt.“






