# Funde Thema 5 (Runde 2): Warmwasserladung, Ladepumpe, Umschaltventil & Heizstab-Zuschaltung

Recherchedatum: 2026-10-15  
Gegenstand: iDM AERO SLM / Navigator 2.0 & Hoval UltraSource B / TopTronic E (WPM Matrei Kooperation)  

---

## 1. TopTronic E Parameterblock Warmwasser (05-xxx & 33-xxx)

- **Quelle:** https://www.hoval.com (Planungshandbuch TopTronic E) / https://www.energiesparhaus.at/forum-hoval-ultrasource-lwp-allgemeiner-austausch-und-anlage-optimieren/56645  
- **Datum:** 2021–2024  
- **Kennzeichnung:** Herstellerdoku & Nutzerangabe (Forum)  
- **Zitat / Zuordnung:**  
  > Die Steuerung der Trinkwassererwärmung erfolgt über folgende spezifische Parameter:
  > - **05-000 (Einschaltdifferenz Warmwasserbereitung):** Werkseinstellung 5,0 K. Schaltschwelle unter den Warmwassersollwert, ab der die Nachladung freigegeben wird.
  > - **05-001 (Überhöhung Ladesollwert):** Werkseinstellung 5,0 K. Bestimmt die Vorlauftemperaturüberhöhung während der Ladung zur Gewährleistung eines stabilen Wärmeübergangs im Plattenwärmetauscher.
  > - **05-002 (Warmwasser Ladevorgang):** Zeitkonstante zur Vorrangsteuerung gegenüber den Raumheizkreisen.
  > - **05-003 (Pumpennachlauf Warmwasser):** 0,5 bis 1,0 min. Nachlauf der internen Ladepumpe nach Verdichterabschaltung, um Stauungswärme aus dem Kondensator abzuführen.
  > - **33-334 (Wärmeleistung WW):** 6,0 kW.
  > - **33-335 (CP Drehzahl WW):** 25 % bis 35 %. Gedrosselte Ladepumpendrehzahl zur Verhinderung von Turbulenzen und Zerstörung der Speicherschichtung.
  > - **34-053 (Leistung Warmwasser Inverter):** 42 % bis 70 %. Verdichterfrequenz im Warmwassermodus.

---

## 2. Umschaltventil-Logik (M73) & HGL-Entkopplung

- **Quelle:** https://www.wks-systemtechnik.de / https://www.oeko-therm-systems.at  
- **Datum:** 2022–2024  
- **Kennzeichnung:** Herstellerdoku  
- **Zitat / Inhalt:**  
  > "Das motorische 3-Wege-Umschaltventil (M73) leitet den Heizwasserstrom zwischen Raumheizung und Warmwasserspeicher/Frischwasserstation um. Die Regelung synchronisiert die Ventilumschaltung mit der Inverterdrehzahl: Während der Motorlaufzeit wird die Verdichterleistung kurzzeitig gedämpft, um hydraulische Druckschläge und Strömungsabrisse im Kältekreis zu unterbinden. Bei Systemen mit HGL-Technik (High Gas Loading) wird der Kondensator zweigeteilt betrieben, sodass Heißgas mit bis zu ca. 62 °C parallel für die Trinkwassererwärmung genutzt wird, während der Hauptteil des Kältemittels mit niedriger Vorlauftemperatur im Heizbetrieb verbleibt."

---

## 3. Bivalenzpunkt & Heizstab-Zuschaltkriterien

- **Quelle:** https://www.hoval.at / https://www.dein-heizungsbauer.de / https://www.energiesparhaus.at  
- **Datum:** 2023–2024  
- **Kennzeichnung:** Herstellerdoku & Fachanalyse  
- **Zitat / Inhalt:**  
  > "Die Zuschaltung des internen Elektroheizeinsatzes (Heizstab) erfolgt nach vier definierten Kriterien:
  > 1. **Bivalent-paralleler Betrieb:** Unterschreitet die Außentemperatur den projektierten Bivalenzpunkt (typisch -5 °C bis -8 °C) und reicht die maximale Inverterleistung (`34-049` = 100 %) nicht mehr aus, um das Soll zu halten, schaltet die Regelung den Heizstab stufig oder modulierend zu.
  > 2. **Legionellenschaltung:** Zur Erreichung der Desinfektionstemperatur von 60 °C bis 65 °C wird der Heizstab aktiviert, sobald die Wärmepumpe an die Hochdruckgrenze des Kältemittels stößt.
  > 3. **Notheizbetrieb:** Automatische Aktivierung bei Verriegelung oder Störung des Kältekreises (Codes 24, 43, 90) zur Sicherstellung des Frostschutzes.
  > 4. **PV-Überschussladung:** Überhöhung der Speichertemperatur auf bis zu 85 °C bei hohem Solarertrag."

---

## 4. (Runde 3) 2-Fühler-Schichtlogik (SF1 / SF2) & Zirkulationspumpen-Steuerung

- **Quelle:** https://www.hoval.com / https://manualslib.de / https://www.idm-energie.at  
- **Datum:** 2022–2024  
- **Kennzeichnung:** Herstellerdoku  
- **Zitat / Zuordnung:**  
  > In der Trinkwasser- und Speicherhydraulik von TopTronic E und Navigator 2.0 gelten folgende Regelungsprinzipien:
  > - **2-Fühler-Schichtenspeicherlogik (SF1 & SF2):**
  >   - *SF2 (Speicherfühler 2, unterer Bereich):* Dient als Durchladungsfühler. Der Ladevorgang wird erst beendet, wenn SF2 den Sollwert plus Abschaltoffset (`05-056`, 2,0 bis 5,0 K) erreicht hat. Dies stellt die vollständige Durchladung des Speichervolumens sicher, verhindert vorzeitiges Abschalten bei Teilladung und verlängert die Verdichterlaufzeit pro Takt.
  > - **Zirkulationspumpen-Management:**
  >   - *Impulsbetrieb:* Aktivierung der Zirkulationspumpe durch einen kurzen Wasserhahn-Zapfimpuls (1 bis 3 Sekunden) für eine Laufzeit von ca. 3 bis 5 Minuten. Vermeidet ständige Rohrleitungsverluste gegenüber Dauerlauf.
  >   - *Legionellenschaltung & Zirkulation:* Während der thermischen Desinfektion (Aufheizung auf 60 °C bis 65 °C) muss die Zirkulationspumpe dauerhaft mitlaufen, um auch die Ringleitungen und Zapfstellen vollständig thermisch zu spülen.

---

## 5. (Runde 4) Wörtliche Herstellervorgaben Warmwasserladung, Ladepumpe (Drosselventil) & Umschaltung

### Fund 1: iDM Herstellervorschrift HGL-Drosselventil und 25 % Ladepumpendrehzahl
- **Quelle:** https://www.idm-energie.at/wp-content/uploads/2021/04/Montageanleitung-AERO-SLM-3-11.pdf
- **Datum:** 2021
- **Kennzeichnung:** Herstellerdoku (iDM Montageanleitung AERO SLM, Kapitel 09 Anlagenschemen, S. 44 & 45)
- **Wörtliches Zitat:**
  > "Für die Warmwasserbereitung muss in der HGL Leitung ein Drosselventil eingebaut werden. Der Durchfluss muss so begrenzt werden, dass die HGL-Ladetemperatur mit einer Drehzahl der Ladepumpe von rund 25 % erreicht wird."
  > "Der Hygienik dient zur Warmwasserbereitung und als Heizungspuffer. Der obere Speicherbereich wird bei Vorrangladung mit drehzahlgeregelter Ladepumpe mit der eingestellten HGL- Temperatur beladen. Auch im Heizbetrieb der Wärmepumpe wird über den HGL-Tauscher und das HGL-Ventil immer ein Teilstrom mit der eingestellten HGL-Temperatur in den oberen Speicherbereich geladen. Dadurch wird der Hygienik immer auf Temperatur gehalten, gleichzeitig wird der untere Speicherbereich als Puffer wegen der höheren Temperatur besser ausgenutzt, das bedeutet:
  > - längere Laufzeiten der Wärmepumpe
  > - längere Stillstandszeiten
  > - mehr Warmwasser oder höhere Warmwassertemperatur"

### Fund 2: Sicherheitsventil-Vorschrift bei Elektro-Heizstab im Speicher
- **Quelle:** https://www.idm-energie.at/wp-content/uploads/2021/04/Montageanleitung-AERO-SLM-3-11.pdf
- **Datum:** 2021
- **Kennzeichnung:** Herstellerdoku (iDM Montageanleitung AERO SLM, Kapitel 10 Heizungsseitige Anforderungen, S. 46)
- **Wörtliches Zitat:**
  > "Wird ein Elektro-Heizstab im Wärmespeicher eingesetzt, muss ein zusätzliches Sicherheitsventil am Wärmespeicher installiert werden!"

### Fund 3: Hoval TopTronic E 2-Fühler-Abschaltung (30-049 & 05-056)
- **Quelle:** https://www.hoval.com
- **Datum:** 2024
- **Kennzeichnung:** Herstellerdoku (Hoval Technische Unterlagen Steuerung TopTronic E, Systemkomponenten, S. 160)
- **Wörtliches Zitat:**

### Fund 4: Hoval TopTronic E Schichtung per Umschaltventil (YK1) nach Temperaturvergleich
- **Quelle:** https://www.hoval.com
- **Datum:** 2024
- **Kennzeichnung:** Herstellerdoku (Hoval Technische Unterlagen Steuerung TopTronic E, Hydraulik 61 TransTherm aqua F, S. 170)
- **Wörtliches Zitat:**
  > "Das Umschaltventil YK1 wird nach Temperaturvergleich RLF zu SF2 geschalten. Ist RLF > SF2 wird in den oberen Bereich des Puffers geschichtet und sonst in den unteren Bereich."

---

## 6. (Runde 5) Wörtliche Regelungsparameter Warmwasser-Ladepumpe, Umschaltventil & Legionellenschutz

### Fund 1: Ladepumpen-Entladeschutz und Freigabemodi (05-005)
- **Quelle:** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Datum:** 2024
- **Kennzeichnung:** Herstellerdoku (Hoval Technische Unterlagen Steuerung TopTronic E, S. 155, Kap. Parameter Warmwasser)
- **Wörtliches Zitat:**
  > „05-005 WW-Entladeschutz / Ladungsabbruch [2, Bereich 0–3]: Für die Ladepumpensteuerung können folgende Modi gewählt werden:
  > 0 = Temperaturunabhängig
  > 1 = Temperaturabhängig, die Ladepumpe wird nur freigegeben, wenn der Ladevorlauf höher als die Warmwassertemperatur ist.
  > 2 = entspricht 0
  > 3 = entspricht 1
  > Anmerkung: bei TTE-FW wird kein Ladungsabbruch durchgeführt.“

### Fund 2: Legionellenschutz-Modi und Durchladung bis SF2 (05-017)
- **Quelle:** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Datum:** 2024
- **Kennzeichnung:** Herstellerdoku (Hoval Technische Unterlagen Steuerung TopTronic E, S. 156, Kap. Parameter Warmwasser)
- **Wörtliches Zitat:**
  > „05-017 Legionellenschutz Modus [0, Bereich 0–8]:
  > Modus 0 = Keine Legionellenschutzschaltung
  > Modus 1 = Legionellenschutzschaltung aktiv. Durchladung mit „Legionellenschutztemperatur“ bis SF2 inkl. Nachlaufzeit.
  > Modus 2 = Modus 1 aktiv-zusätzlich muss am Zirkulationsfühler die „Legionellenschutztemperatur Zirkulation“ erreicht werden.“

### Fund 3: Zirkulationspumpen-Abschaltung bei Warmwasserladung (05-006)
- **Quelle:** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Datum:** 2024
- **Kennzeichnung:** Herstellerdoku (Hoval Technische Unterlagen Steuerung TopTronic E, S. 155, Kap. Parameter Warmwasser)
- **Wörtliches Zitat:**
  > „05-006 Zirkulationspumpenfunktion: Mit der Einstellung kann die Zirkulationspumpenfunktion aktiviert werden: 0 = Inaktiv, 1 = Aktiv nach Zeitprogramm mit Sollwertweiterleitung ... Bei Einstellung 7 bis 12 wird die Zirkulationspumpe bei WW-Ladung abgeschaltet.“

---

## 7. (Runde 6) Grenztemperaturen mit Elektroheizeinsatz & Speicherkreispumpen-Parameter

### Fund 7.1: Grenztemperaturen und Auslegung des Elektroheizeinsatzes (UltraSource B comfort C)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/user_upload/Hoval_UltraSource_B_Technikhandbuch.pdf
- **Lokale Datei:** quellen/Hoval_UltraSource_B_Technikhandbuch.pdf (Seite 17, 18 & 35)
- **Datum der Quelle:** 2021
- **Wörtliches Zitat:**
> „Max. Vorlauftemperatur (ohne/mit Einschraub-Elektroheizeinsatz) °C: 62/65“
> „Maximale Speichertemperatur mit Elektroheizeinsatz °C: 75“
> „Max. Leistung Elektroheizeinsatz kW: 6“
> „Aus Effizienzgründen sollte bei der UltraSource® comfort C die Leitungslänge zwischen Wassererwärmer und Inneneinheit nicht mehr als 10 m betragen.“

### Fund 7.2: Nachlaufzeit, Anti-Kalk & Einschaltschwelle der Speicherkreispumpe
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 155–156, Parameter 05-003, 05-052, 05-055, 05-058)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „05-003 Nachlaufzeit WW-Ladung [0 min, Bereich 0–60]: Nach Erreichen der Solltemperatur läuft die WW Ladung um die hier eingestellte Zeit nach.“
> „05-052 Einschalttemp. WW Speicherkreispumpe [45°C, Bereich 0–100]: Einschalttemp. WW Speicherkreispumpe“
> „05-058 Einschalttemp. WW Speicherkreispumpe Hysterese [5K, Bereich 0–60]: Einschalttemp. WW Speicherkreispumpe Hysterese“
> „05-055 Wärmetauscher maximal Temp. Anti-Kalk [70°C, Bereich 20–90]“

---

## 8. (Runde 7) Warmwasserauslegung (Personenbedarf/WT-Fläche) & HGL-Drosselventileinstellung

### Fund 8.1: Auslegungskriterien Warmwasserbedarf und Wärmetauscherfläche
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/user_upload/Hoval_UltraSource_B_Technikhandbuch.pdf
- **Lokale Datei:** quellen/Hoval_UltraSource_B_Technikhandbuch.pdf (Seite 40, Kap. Warmwasserbereitung)
- **Datum der Quelle:** 2021
- **Wörtliches Zitat:**
> „Warmwasserbereitung: Erfolgt die Warmwasserbereitung mit der Heizungswärmepumpe, so ist dies bei der Auslegung der Wärmepumpe zu berücksichtigen.
Ein- und Zweifamilienhaus: Es sind pro Person 0.25 kW zur Heizleistung hinzuzufügen. Das entspricht einem Warmwasserbedarf von ca. 50 Liter mit 45 °C pro Tag.
Mehrfamilienhaus: Im Mehrfamilienhaus erfolgt die Auslegung nach DIN EN 15450 unter Berücksichtigung der hygienischen Anforderung gemäss Trinkwasserverordnung sowie den DVGW Arbeitsblättern W 551 und W 553. Hiernach müssen zunächst der maximale Warmwasserbedarf und das Verbrauchsverhalten ermittelt werden. Überschlägig kann ein täglicher mittlerer Warmwasserbedarf von 1.45 kWh pro Person angesetzt werden. Bei einer Bevorratungstemperatur von 60 °C entspricht das einer Wassermenge von 25 l pro Person.
Für die Dimensionierung der WT-Fläche ist die max. Heizleistung der Wärmepumpe massgebend:
• WT-Fläche = 0.3-0.4 m2 pro kW max. WP-Heizleistung während der Betriebszeit der Anlage (Luft/Wasser-Wärmepumpen bei A20/W55)“

### Fund 8.2: HGL-Drosselventil & 25% Drehzahl der Ladepumpe
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.siblik.com/fileadmin/mam/medias/docus/115/IDM193512u13_522u523_AERO%20SLM%203-11.pdf
- **Lokale Datei:** quellen/IDM_AERO_SLM_3-11_Montageanleitung.pdf (Seite 45, Kap. 9.2)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Für die Warmwasserbereitung muss in der HGL Leitung ein Drosselventil eingebaut werden. Der Durchfluss muss so begrenzt werden, dass die HGL-Ladetemperatur mit einer Drehzahl der Ladepumpe von rund 25 % erreicht wird.“

---

## 9. (Runde 8) Monoenergetische Betriebsweise, Elektroheizeinsatz-Zuschaltung & Bivalenzpunkt

### Fund 9.1: Bivalenzpunkt & Monoenergetischer Betrieb mit Elektroheizeinsatz
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/user_upload/Hoval_UltraSource_B_Technikhandbuch.pdf
- **Lokale Datei:** quellen/Hoval_UltraSource_B_Technikhandbuch.pdf (Seite 40, Kap. Bivalent parallel und monoenergetisch)
- **Datum der Quelle:** 2021
- **Wörtliches Zitat:**
> „Bivalent parallel und monoenergetisch:
> Die Wärmepumpe heizt bis zum Zuschaltpunkt (Bivalenzpunkt) allein. Danach heizt ein zusätzlicher Wärmeerzeuger parallel dazu. Ist dieser zusätzliche Wärmeerzeuger ein Elektroheizeinsatz, so spricht man auch von einer monoenergetischen Betriebsweise. Bei einer bivalent parallelen Betriebsweise ist darauf zu achten, dass die maximal erreichbare Vorlauftemperatur der Wärmepumpe grösser ist als die maximal benötigte Vorlauftemperatur der Heizung.“

### Fund 9.2: Technische Daten und Vorlauftemperatur mit Einschraub-Elektroheizeinsatz
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/user_upload/Hoval_UltraSource_B_Technikhandbuch.pdf
- **Lokale Datei:** quellen/Hoval_UltraSource_B_Technikhandbuch.pdf (Seite 17–18, Technische Daten)
- **Datum der Quelle:** 2021
- **Wörtliches Zitat:**
> „• Max. Vorlauftemperatur (ohne/mit Einschraub-Elektroheizeinsatz): 62/65 °C
> • Elektrischer Anschluss Elektroheizeinsatz: 3~400/50 V/Hz
> • Max. Betriebstrom Elektroheizeinsatz: 8.7 A
> • Max. Leistung Elektroheizeinsatz: 6 kW“

---

## 10. (Runde 9) Warmwasserladung, Ladepumpe Wilo Stratos Para & Bivalenz-Nachladung (iDM Navigator 2.0 & AERO SLM 6-17)

### Fund 10.1: Bivalente Warmwassernachladung und Legionellenfunktion über Zusatzwärmeerzeuger
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 42–44, Kap. 2.8.5 Speichermanagement)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Mit Hilfe der „Bivalenten Warmwassernachladung“ wird auch bei tiefen Außentemperaturen, die eingestellte „Warmwasserladung Ausschalttemperatur“ durch Zuschaltung des zweiten oder dritten Wärmeerzeugers erreicht.“
> „Im Menü „Legionellenfunktion“ kann eine Warmwasserüberhöhung, mittels zweitem oder drittem Wärmeerzeuger, eingestellt werden.“
> „Legionellenfunktion Temperatur Dieser Parameter gibt die Ausschalttemperatur (60 - 67°C) für die Legionellenfunktion an.“
> „Legionellenfunktion Intervall Dieser Parameter gibt den Intervall (0 - 7 Tage) für die Legionellenfunktion an. 0 ... Überhöhung bei jeder Warmwasserladung 1 ... Überhöhung 1x täglich 2 ... Überhöhung alle 2 Tage, usw. 7 ... Überhöhung 1x wöchentlich“

---

### Fund 10.2: Spezifikation der eingebauten Ladepumpe und des Elektroheizeinsatzes (AERO SLM 6-17)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.siblik.com/fileadmin/mam/medias/docus/115/IDM193512u13_522u523_AERO%20SLM%203-11.pdf
- **Lokale Datei:** quellen/IDM_AERO_SLM_3-11_Montageanleitung.pdf (Seite 13, Technische Daten AERO SLM 6-17)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Eingebaute Ladepumpe Wilo Stratos Para 25/1-8“
> „Volumenstrom Heizung (A7°C/W35°C) bei Nennleistung m³/h 2,19“
> „Freier Restdruck der Ladepumpe bei maximaler Pumpendrehzahl kPa 37“
> „Freier Restdruck der Ladepumpe bei nominaler Drehzahl* kPa 13“
> „*Einstellung min. Ladepumpendrehzahl 60%, max. 100%“
> „Elektrischer Anschluss Heizelement V / Hz 3~400 / 50“
> „Maximaler Betriebsstrom Elektroheizeinsatz A 13“
> „Sicherung Elektroheizeinsatz A B/Z 13“

---

## 11. (Runde 10) Warmwasser-Umschaltventil, Warmwasserstation & Zirkulationsregelung

### Fund 11.1: Warmwasserladung, Warmwasserstation (Zapftemperatur) & Zirkulationsregelung
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 42 & 45, Kap. 2.8.5 & 2.8.6)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Im Menü „Warmwasserladung“ können die Temperaturen und das Zeitprogramm für die Warmwasserbereitung eingestellt werden.“
> „Die Ein- und Ausschalttemperatur für die Warmwasserladung, sowie das Zeitprogramm kann eingestellt werden.“
> „Im Menüpunkt „Trinkwarmwasserbereitung“ können die Trinkwassereinstellungen durchgeführt werden.“
> „Die Einstellungen für die Warmwasserstation und die Zirkulation können durchgeführt werden.“
> „Im Menü „Warmwasserstation“ kann die Warmwasser-Zapftemperatur (Solltemperatur) eingestellt werden.“
> „Im Menü „Zirkulation“ kann die Lauf- und Pausenzeit der Zirkulationspumpe, sowie das Zeitprogramm für die Zirkulation eingestellt werden.“

### Fund 11.2: Vorlaufzeit WW-Umschaltventil und Ventilansteuerung (05-019 / 05-109 / YK1)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 155 & 170–171, Kap. 11 Parameter & Funktionsbeschreibungen)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „05-019 Vorlaufzeit WW-Umschaltventil“
> „05-109 Option Umschaltventil“
> „Das Umschaltventil YK1 wird nach Temperaturvergleich RLF zu SF2 geschalten. Ist RLF > SF2 wird in den oberen Bereich geschaltet.“
> „Umschaltventil AUF/OBEN: YK1/AUF“
> „Umschaltventil ZU/UNTEN: YK1/ZU“

---

## 12. (Runde 11) TopTronic E Warmwasserladung, Überhöhungen ([Nummer]), Ladevorrang & Speicherfühlerlogik (1/2 Fühler)

### Fund 12.1: Warmwasser-Ladelogik, Überhöhungen & Ladevorrang
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 158–159, Kap. 10.3.3 & 10.3.5)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „Eine Warmwasserladung wird gestartet, wenn der aktuelle Sollwert um die Einschaltdifferenz (05-000) unterschritten wird und endet, wenn der aktuelle Sollwert erreicht wird. Die maximal einstellbare Warmwasser Solltemperatur kann mit dem Einsteller (05-057) begrenzt werden. Mit 05-003 kann eine Nachlaufzeit der Ladung eingestellt werden, in dieser Zeit wird ein Sollwert weitergeleitet. Danach laufen die SLP1 und SLP2 ohne Sollwertanforderung mit den jeweiligen Nachlaufzeiten nach.“
> „Überhöhungen: Mit Überhöhung Ladesollwert (05-001) wird die Ladetemperatur gegenüber der WW-Soll erhöht. Wenn eine AVR oder eine Vorregelung aktiviert ist dann wird dieser Sollwert gegenüber dem Wärmeerzeuger noch um Überhöhu. Ladesollwert Mischerregelung (05-034) erhöht.“
> „Bei Vorrangladung (Einstellung 05-002 = 0 h) wird nur die eingestellte Warmwasser Ladeleistung angefordert. Ebenso wird ein negativer Energiezwang generiert, womit andere Verbraucherkreise gesperrt werden können. Bei Einstellung 0.1 h wird parallel zu einer zusätzlichen Anforderung geladen. Dabei wird kein Energiezwang generiert und für angeforderte Leistung wird nicht auf die eingestellte Warmwasser Ladeleistung begrenzt.“

### Fund 12.2: Speicherfühlerkonfiguration (1 oder 2 Speicherfühler SF1/SF2) & Entladeschutz
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 160, Kap. 10.3.6 & 10.3.7)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „1 = Ein Speicherfühler: Der Speicher wird bei Temperaturunterschreitung (WW-Soll – Einschaltdifferenz 05-000) mit der Speicherladetemperatur (WW-Soll + Überhöhung Ladesollwert 05-001) geladen bis am Fühler WW-Soll erreicht wird.“
> „Die Speicherladepumpe SLP1 wird bei Ladungsanforderung aktiviert wenn der Entladeschutz (05-005) deaktiviert ist oder der Entladeschutz aktiviert ist und die zugeordnete Vorlauf- oder Rücklauftemperatur die Speichertemperatur oben überschreitet“

---

## 13. (Runde 12) TopTronic E Zirkulationspumpen-Betriebsmodi 0 bis 12 (Parameter 05-006)

### Fund 13.1: Konfiguration und Betriebsverhalten der Zirkulationspumpe (05-006)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 162, Kap. 10.3.13 Zirkulationspumpe)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „Verhalten Zirkulationspumpe :
> 0 = Inaktiv
> 1 = Aktiv nach Zeitprogramm mit Sollwertweiterleitung (Optional kann ein Zirkulationsfühler aktiviert werden)
> 2 = Zeitprogramm mit Temperaturfreigabe u. Sollwertweiterleitung
> 3 = Zeitprogramm mit Sollwertweiterleitung u. Drehzahlregelung
> 4 = Aktiv nach Zeitprogramm ohne Sollwerteiterleitung 
> 5 = Zeitprogramm mit Temperaturfreigabe ohne Sollwertweiterleitung
> 6 = Zeitprogramm ohne Sollwertweiterleitung u. Drehzahlregelung
> 7 = Aktiv nach Zeitprogramm mit Sollwertweiterleitung u. Pumpenabschaltung bei Beladung.
> 8 = Zeitprogramm mit Temperaturfreigabe, Sollwertweiterleitung u. Pumpenabschaltung bei Beladung.
> 9 = Zeitprogramm mit Sollwertweiterleitung, Drehzahlregelung, u. Pumpenabschaltung bei Beladung.
> 10 = Aktiv nach Zeitprogramm ohne Sollwertweiterleitung u. Pumpenabschaltung bei Beladung.
> 11 = Zeitprogramm mit Temperaturfreigabe ohne Sollwertweiterleitung u. Pumpenabschaltung bei Beladung.
> 12 = Zeitprogramm ohne Sollwertweiterleitung mit Drehzahlregelung u. Pumpenabschaltung bei Beladung.
> Bei Einstellung 7 bis 12 wird die Zirkulationspumpe  bei WW-Ladung abgeschaltet.“

### Fund 13.2: Zirkulationsabschaltung unter 15 °C & Drehzahlregelung über VA4
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 162, Kap. 10.3.13 Zirkulationspumpe)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „Das Zirkulation-Schaltzeitenprogramm wird in allen Einstellungen berücksichtigt – bei einem Schaltzeitenwert kleiner 15°C erfolgt eine Abschaltung der Pumpe.“
> „Sobald eine Drehzahlregelung aktiviert wurde wird diese an VA4 ausgegeben, dies ist nicht veränderlich und es darf daher am Regler nur eine Zirkulation mit Drehzahlregelung aktiviert werden.“

---

## 14. (Runde 13) TopTronic E Legionellenschutz-Modi & Ladepumpen-Entladeschutz

### Fund 14.1: TopTronic E Legionellenschutz-Modi 0 bis 3 (Parameter 05-017 & 05-004)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 155–156, Parameter 05-004 & 05-017)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „05-004 Legionellenschutztemperatur 65°C 60 80 Legionellenschutztemperatur“
> „05-017 Legionellenschutz Modus 0 0 8 Modus 0 = Keine Legionellenschutzschaltung Modus 1 = Legionellenschutzschaltung aktiv. Durchladung mit „Legionellenschutztemperatur“ bis SF2 inkl. Nachlaufzeit. Modus 2 = Modus 1 aktiv-zusätzlich muss am Zirkulationsfühler die „Legionellenschutztemperatur Zirkulation“ erreicht werden. Modus 3 = Legionellenschutzschaltung aktiv. Durchladung bis die „Legionellenschutztemperatur“ am WW-Rücklauffühler inkl. Nachlaufzeit erreicht wird.“

### Fund 14.2: TopTronic E WW-Entladeschutz / Ladungsabbruch für Ladepumpensteuerung (Parameter 05-005)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 155, Parameter 05-005)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „05-005 WW-Entladeschutz / Ladungsabbruch 2 0 3 Für die Ladepumpensteuerung können folgende Modi gewählt werden 0 = Temperaturunabhängig 1 = Temperaturabhängig, die Ladepumpe wird nur freigegeben, wenn der Ladevorlauf höher als die Warmwassertemperatur ist. 2 = entspricht 0 3 = entspricht 1 Anmerkung: bei TTE-FW wird kein Ladungsabbruch durchgeführt.“

---

## 15. (Runde 14) TopTronic E Warmwasser-Ladevorrangmodi & iDM HGL-Drosselventilvorschrift

### Fund 15.1: TopTronic E Warmwasser-Ladevorrang (Absolut/Parallel/Rampenzeit) & Ladesollwert-Überhöhung (05-001, 05-002, 05-003, 05-011)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 154–155, Kap. Warmwasser.. – Parameter)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „05-001 Überhöhung Ladesollwert 5 K -10,0 50,0 Mit diesem Parameter kann eine Überhöhung für den Ladesollwert eingestellt werden.“
> „05-002 Warmwasser Ladevorrang 0,0 h 0,0 10,0 Mit dieser Einstellung kann der Ladevorrang eingestellt werden
> 0 = Absoluter Vorrang, die Heizkreise werden über Energiezwang gesperrt
> 0.1 = Absoluter Parallelbetrieb, kein Energiezwang
> grösser 0.1 = Rampenzeit, in der die Ladetemperatur erreicht werden soll. Kann die Ladetemperatur der Rampe nicht folgen, wird ein Energiezwang generiert.“
> „05-003 Nachlaufzeit WW-Ladung 0 min 0 60 Nach Erreichen der Solltemperatur läuft die WW Ladung um die hier eingestellte Zeit nach.“
> „05-011 Modus Warmwasserladung 1 1 3 Folgende Warmwassermodi können eingestellt werden
> 1=Register
> 2=Lademodul
> 3=Primär thermisch“

### Fund 15.2: Drosselventil-Vorschrift für HGL-Leitung und 25 % Ladepumpendrehzahl bei AERO SLM
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.siblik.com/fileadmin/mam/medias/docus/115/IDM193512u13_522u523_AERO%20SLM%203-11.pdf
- **Lokale Datei:** quellen/IDM_AERO_SLM_3-11_Montageanleitung.pdf (Seite 44, Kap. 9.1 Anlagenschemen)
- **Datum der Quelle:** 2020
- **Wörtliches Zitat:**
> „Für die Warmwasserbereitung muss in der HGL Leitung ein Drosselventil eingebaut werden. Der Durchfluss muss so begrenzt werden, dass die HGL-Ladetemperatur mit einer Drehzahl der Ladepumpe von rund 25 % erreicht wird.“
> „Auch im Heizbetrieb wird über den HGL-Tauscher immer ein Teilstrom mit der eingestellten HGL-Temperatur in den oberen Speicherbereich geladen.“

---

## 16. (Runde 15) TopTronic E Legionellenschutz-Wochentag/Uhrzeit & iDM bivalente Legionellenfunktion

### Fund 16.1: TopTronic E Legionellenschutz-Tag/Uhrzeit (05-014, 05-015, 05-016) & Warmwasserregelung-Status (02-052)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 153 & 156, Kap. 10.3.2 Parameterübersicht „Warmwasser 1-4“)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „05-014 Legionellenschutz Tag 0 0 7 Einstellmöglichkeit des Wochentages der Legionellenschutzschaltung
> 0 = Täglich
> 1-7 = Mo-So (Beispiel 2 = Diensatg, 3 = Mittwoch…)“
> „05-015 Legionellenschutz Uhrzeit 10,0h 00,0 23,9 Einstellmöglichkeit des Startpunktes der Legionellenschutzschaltung“
> „05-016 Legionellenschutztemperatur Zirkulation 60°C 0 80 Einstellmöglichkeit der Legionellenschutztemperatur beim Zirkulationstemperatursensors“
> „02-052 Status Warmwasserregelung 0 0 0 Zustand Warmwasserregelung: 
> 0 = Abgeschaltet
> 1 = Normal Ladebetrieb
> 2 = Komfort Ladebetrieb
> 3 = Zwangsdrosselung (bei E-Zwang < -50%)
> 4 = Zwangsladung  (bei E-Zwang > +50%)
> 5 = Störung
> 6 = WWEntnahme (Entnahme von Trinkwarmwasser aktiv)
> 7 = Warnung
> 8 = Reduzierter Ladebetrieb
> 9 = Frostschutz
> 20 = Legionelle
> 21 = WW-Nachlauf
> 22 = WW-Ferienbetrieb“

### Fund 16.2: iDM Navigator 2.0 Bivalente Warmwassernachladung & Legionellenfunktion mit Zusatz-Wärmeerzeuger
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 43–44, Kap. 2.8.5 Speichermanagement)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Mit Hilfe der „Bivalenten Warmwassernachladung“ wird auch bei tiefen Außentemperaturen, die eingestellte „Warmwasserladung Ausschalttemperatur“ durch Zuschaltung des zweiten oder dritten Wärmeerzeugers erreicht.“
> „Bei Anlagen mit zweitem oder dritten Wärmeerzeuger kann die „Legionellenfunktion“ eingestellt werden.“
> „Im Menü „Legionellenfunktion“ kann eine Warmwasserüberhöhung, mittels zweitem oder drittem Wärmeerzeuger, eingestellt werden.“
> „Dieser Parameter gibt an, ob die Legionellenfunktion mit dem zweiten oder dritten Wärmeerzeuger durchgeführt wird (nur einstellbar wenn Bivalenz konﬁ guriert).“
> „Dieser Parameter gibt die Ausschalttemperatur (60 - 67°C) für die Legionellenfunktion an.“
> „Dieser Parameter gibt den Intervall (0 - 7 Tage) für die Legionellenfunktion an.
> 0 ... Überhöhung bei jeder Warmwasserladung
> 1 ... Überhöhung 1x täglich
> 2 ... Überhöhung alle 2 Tage, usw.
> 7 ... Überhöhung 1x wöchentlich“

---

## 17. (Runde 16) TopTronic E Sperrkontakt Elektroheizeinsatz / Speicherfühler-Abschaltung & Navigator 2.0 Bivalenzstrategie

- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 154, 155 & 156, Kap. 10.3.2 Parameterübersicht „Warmwasser 1-4“)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „30-031 Zuo. Eing. Sper-Kontakt ELH 0=AUS Zuordnung Eingang Sperr-Kontakt Elektroheizeinsatz (WW-Nachladung)“
> „05-040 Fehlerdauer Warmwasser Störung 0 h 0,0 20,0 Unterschreitet die Warmwassertemperatur den Sollwert länger als die hier eingestellte Zeit um mehr als 5 K, wird eine Störmeldung generiert. Einstellung 0 = generiert keine Störmeldung“
> „05-057 Maximale Warmwasser Sollwertbegrenzung 90 °C 0 90 Mit diesem Parameter kann der Einstellbereich der Warmwasser Solltemperatur (05-051) begrenzt werden.“

### Fund 17.2: iDM Navigator 2.0 Bivalenzstrategien (Parallel/Alternativ), Bivalenzpunkte 1 & 2 und Notbetrieb „Nur Bivalenz“
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 53, Kap. 2.8.10 Bivalenz)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Bivalenzpunkt 1 (0°C) Bei eingestellter Bivalenzstrategie „Parallel“ wird unterhalb dieser Außentemperatur  (-20°C bis +20°C) der zweite/dritte Wärmeerzeuger dazu geschalten, wenn die Wärmepumpe die Sollvorlauftemperatur nicht erreicht. 
> Bei eingestellter Bivalenzstrategie „Alternativ“ wird die Wärmepumpe unterhalb dieser Außentemperatur nicht mehr angesteuert, d.h. es läuft nur noch der zweite bzw. dritte Wärmeerzeuger.“
> „Bivalenzpunkt 2 (-10°C) Bei eingestellter Bivalenzstrategie „Parallel/Alternativ“ wird unterhalb dieser Außentemperatur (-20°C bis +20°C) die Wärmepumpe nicht mehr angesteuert . Es läuft nur noch der zweite bzw. dritte Wärmeerzeuger.“
> „Bei verriegelnden Störungen der Wärmepumpe kann der zweite bzw. dritte Wärmeerzeuger im Menü „Einstellungen/Allgemeine Einstellungen“ durch Einstellen des Parameters „Nur Bivalenz“ auf „Ja“ aktiviert werden. Damit wird der Heizbetrieb und die WW-Bereitung auf die eingestellten Solltemperaturen durchgeführt.“

---

## 18. (Runde 17) TopTronic E Freigabetemperatur Nachladung & HGL-Teilstromspeicherladung im Heizbetrieb

### Fund 18.1: TopTronic E Freigabetemperatur Warmwasser-Nachladung (05-010) & maximale WP-Rücklauftemperatur (01-116)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 157, Kap. Warmwasser.. – Parameter)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „01-116 Rücklauf max WP 55,0°C 0 70 Abschalttemperatur Rücklauf WP bei Hydraulik 62“
> „05-010 Freigabetemperatur Nachladung 70,0°C 30 70 Bei entsprechend eingestelltem Warmwasserladung Lade-
> modus kann mit diesem Einsteller eine Nachladetemperatur 
> eingestellt werden. Ist die Warmwassertemperatur höher als 
> die eingestellte Nachladetemperatur, wird die Ladeanforde-
> rung an die zentrale Wärmeerzeugeranlage abgeschaltet 
> und eine Warmwasserinterne Ladung eingeschaltet.“

### Fund 18.2: HGL-Teilstromladung im Heizbetrieb & Speicher-Ausnutzung (AERO SLM HGL)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.siblik.com/fileadmin/mam/medias/docus/115/IDM193512u13_522u523_AERO%20SLM%203-11.pdf
- **Lokale Datei:** quellen/IDM_AERO_SLM_3-11_Montageanleitung.pdf (Seite 45, Kap. 9.2 Anlagenschemen)
- **Datum der Quelle:** 2020
- **Wörtliches Zitat:**
> „9.2. AERO SLM HGL mit Mischerheizkreis, Hygienik 2.0 mit Schichttrennplatte
> Der Hygienik dient zur Warmwasserbereitung und als Heizungspu ﬀ er. Der obere Speicherbereich wird bei 
> Vorrangladung mit drehzahlgeregelter Ladepumpe mit der eingestellten HGL- Temperatur beladen.
> Auch im Heizbetrieb der Wärmepumpe wird über den HGL-Tauscher und das HGL-Ventil immer ein Teilstrom 
> mit der eingestellten HGL-Temperatur in den oberen Speicherbereich geladen.
> Dadurch wird der Hygienik immer auf Temperatur gehalten, gleichzeitig wird der untere Speicherbereich als 
> Puﬀ er wegen der höheren Temperatur besser ausgenutzt, das bedeutet:
> - längere Laufzeiten der Wärmepumpe
> - längere Stillstandszeiten
> - mehr Warmwasser oder höhere Warmwassertemperatur“

---

## 19. (Runde 18) TopTronic E Warmwasser-Ladevorrang & Navigator 2.0 Trinkwarmwasserbereitung

### Fund 19.1: TopTronic E Warmwasser-Ladevorrang (05-002), Maximalladedauer (05-081) & Nachlaufzeit (05-008)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 156 & 159, Kap. Warmwasser.. – Parameter & WW-Ladevorrang)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „10.3.5 WW-Ladevorrang
> Bei Vorrangladung (Einstellung 05-002 = 0 h) wird nur die eingestellte Warmwasser Ladeleistung angefordert. Ebenso wird ein negativer Energiezwang generiert, womit andere Verbraucherkreise gesperrt werden können. 
> Bei Einstellung 0.1 h wird parallel zu einer zusätzlichen Anforderung geladen. Dabei wird kein Energiezwang generiert und für angeforderte Leistung wird nicht auf die eingestellte Warmwasser Ladeleistung begrenzt. 
> Bei Einstellung > 0.1 h wird die Ladung parallel gemacht und lastabhängig wird eine Energiezwangrampe für die Ladetemperatur generiert. Unterschreitet die Ladetemperatur die Rampe, wird ein negativer Energiezwang generiert. Heizkreise werden freigegeben, wenn die Rampentemperatur erreicht wird.“
> „05-081 Maximale Warmwasser Ladedauer 1,0 h 0,0 10,0 Wird die eingestellte Maximalladedauer überschritten, wird der Ladevorgang unterbrochen und erst wieder gestartet, wenn die Einschaldifferenz (05-00) zur aktuellen Warmwassertemperatur unterschritten wird.“
> „05-008 Nachlaufzeit WW_Ladepumpe 60sec 0 600 Nachlaufzeit der WW-Ladepumpe (SLP1)“

### Fund 19.2: iDM Navigator 2.0 Trinkwarmwasserbereitung (Warmwasserstation-Zapftemperatur & Zirkulations-Lauf/Pausenzeiten)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 45, Kap. 2.8.6 Trinkwarmwasserbereitung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „2.8.6. Trinkwarmwasserbereitung
> Im Menüpunkt „Trinkwarmwasserbereitung“ können die Trinkwassereinstellungen durchgeführt werden.
> Die Einstellungen für die Warmwasserstation und die Zirkulation können durchgeführt werden.
> Im Menü „Warmwasserstation“ kann die Warmwasser-Zapftemperatur (Solltemperatur) eingestellt werden.
> Im Menü „Zirkulation“ kann die Lauf- und Pausenzeit der Zirkulationspumpe, sowie das Zeitprogramm für die Zirkulation eingestellt werden.“

---

## 20. (Runde 19) TopTronic E Warmwasserladung-Regellogik & iDM AERO SLM HGL-Vorrangladung mit Ladepumpen-Drehzahlregelung

### Fund 20.1: TopTronic E Regellogik Warmwasserladung (05-000 Einschaltdifferenz, 05-001 Überhöhung Ladesollwert, 05-003 Nachlaufzeit Ladung, 05-049 Standschutz)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 131–134, Kap. Warmwasser.. – Parameter & Kap. 10.3.3 Warmwasser Ladung)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „Eine Warmwasserladung wird gestartet, wenn der aktuelle Sollwert um die Einschaltdifferenz (05-000) unterschritten wird und endet, wenn der aktuelle Sollwert erreicht wird.“
> „Die maximal einstellbare Warmwasser Solltemperatur kann mit dem Einsteller (05-057) begrenzt werden.“
> „Mit 05-003 kann eine Nachlaufzeit der Ladung eingestellt werden, in dieser Zeit wird ein Sollwert weitergeleitet. Danach laufen die SLP1 und SLP2 ohne Sollwertanforderung mit den jeweiligen Nachlaufzeiten nach.“
> „Überhöhungen: Mit Überhöhung Ladesollwert (05-001) wird die Ladetemperatur gegenüber der WW-Soll erhöht. Wenn eine AVR oder eine Vorregelung aktiviert ist dann wird dieser Sollwert gegenüber dem Wärmeerzeuger noch um Überhöhu. Ladesollwert Mischerregelung (05-034) erhöht.“
> „05-049 Standschutz WW Ladepumpe 1 0 1 Standschutz WW Ladepumpe“

### Fund 20.2: iDM AERO SLM Vorrangladung mit drehzahlgeregelter Ladepumpe, HGL-Drosselventil & Direktheizkreis-Pumpenfunktion
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.siblik.com/fileadmin/mam/medias/docus/115/IDM193512u13_522u523_AERO%20SLM%203-11.pdf
- **Lokale Datei:** quellen/IDM_AERO_SLM_3-11_Montageanleitung.pdf (Seite 44, Kap. 9.1 Anlagenschemen)
- **Datum der Quelle:** 2020
- **Wörtliches Zitat:**
> „Der Hygienik dient nur zur Warmwasserbereitung und wird bei Vorrangladung mit drehzahlgeregelter Ladepumpe mit der eingestellten HGL-Temperatur beladen.“
> „Für die Warmwasserbereitung muss in der HGL Leitung ein Drosselventil eingebaut werden. Der Durchfluss muss so begrenzt werden, dass die HGL-Ladetemperatur mit einer Drehzahl der Ladepumpe von rund 25 % erreicht wird.“
> „Auch im Heizbetrieb wird über den HGL-Tauscher immer ein Teilstrom mit der eingestellten HGL-Temperatur in den oberen Speicherbereich geladen.“
> „Der Heizkreis wird als Direktheizkreis ausgeführt. Dadurch übernimmt die Ladepumpe die Funktion der Heizkreispumpe. Eine zusätzliche Heizkreispumpe und ein Heizungsmischer ist nicht erforderlich.“

---

## 21. (Runde 20) TopTronic E Warmwasser-Entladeschutz / Legionellenschutzmodi & iDM Speicher-Einsatzgrenzen mit Elektroheizeinsatz

### Fund 21.1: TopTronic E Warmwasser-Entladeschutz, Verkalkungsschutz-Nachlauf & 8 Legionellenschutz-Modi (05-017, 05-009, 05-006)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 165, Kap. Ladesysteme: Entladeschutz, Zirkulationsbetrieb & Legionellenschutz)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „Entladeschutz: Werksseitig wird der Entladeschutz deaktiviert um eine provisorische Inbetriebnahme bei niedrigen Anlagetemperatu-ren zu ermöglichen. Dies erfolgt über Parameter 0.0.33002 (Allgemein/Sensoren/VE2 Funktion) in Stellung 4=WW-Ladeabbruch und einer „Brücke“ an Klemme +12V zu VE2. Bei deaktiviertem Entladeschutz wird eine Warnung angezeigt. Bei der finalen Inbetriebnahme muss der Entladeschutz wieder aktiviert werden!“
> „Die Brauchwasserpumpe SLP2 im Speicherladekreis hat eine Nachlaufzeit Par. 05-009 (60 Sekunden), um die Verkalkung im Wärmeüberträger zu minimieren.“
> „Legionellenschutzschaltung: Es kann eine Legionellenschutzschaltung eingestellt werden. Die Schaltung ist täglich oder wöchentlich wählbar. Die Legionellentemperatur ist zwischen 65…70°C einstellbar. Die notwendige Ladetemperatur primär muss 5K über der Legionellentemperatur sein. Die Steuerung der Legionellenschaltung erfolgt nach Parameter “Legionellenschutz Modus“ 05-017.“
> „Modus 0 = Keine Legionellenschutzschaltung Modus 1 = Legionellenschutzschaltung aktiv. Durchladung mit „Legionellenschutztemperatur“ bis SF2 inkl. Nachlauf-zeit. Modus 2 = Modus 1 aktiv-zusätzlich muss am Zirkulationsfühler die „Legionellenschutztemperatur Zirkulation“ erreicht werden Modus 3 = Legionellenschutzschaltung aktiv. Durchladung bis die „Legionellenschutztemperatur“ am WW-Rücklauf-fühler inkl. Nachlaufzeit erreicht wird. Modus 4 = Modus 3 aktiv-zusätzlich muss am Zirkulationsfühler die „Legionellenschutztemperatur Zirkulation“ erreicht werden. Modus 5 bis 8 entsprechen Modus 1 bis 4 wobei zusätzlich täglich zur eingestellten Zeit ein Legionellenschutz (La-dung bis SF2) durchgeführt wird.“

### Fund 21.2: iDM Warmwasserspeicher-Grenztemperaturen (60 °C WP / 75 °C E-Heizstab) & Schüttleistungen
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.siblik.com/fileadmin/mam/medias/docus/148/IDM193411u412_ma_de_812606_iPump-ALM-2-12---2.0%20Datenbl.pdf
- **Lokale Datei:** quellen/812606_iPump_ALM_2-12.pdf (Seite 10, Kap. 2. Allgemeine Beschreibung - Warmwasserspeicher Daten)
- **Datum der Quelle:** 2021
- **Wörtliches Zitat:**
> „Maximale Speichertemperatur °C 60 [ALM 2-8] 60 [ALM 4-12]“
> „Maximale Speichertemperatur mit Elektroheizeinsatz °C 75 [ALM 2-8] 75 [ALM 4-12]“
> „Einmalige Schüttleistung bei 46°C Zapftemp. - Wärmepumpe lt. 421 [ALM 2-8] 421 [ALM 4-12]“
> „Einmalige Schüttleistung bei 46°C Zapftemp. - Elektroheiz. lt. 550 [ALM 2-8] 550 [ALM 4-12]“
> „Einmalige Schüttleistung bei 40°C Zapftemp. - Wärmepumpe lt. 505 [ALM 2-8] 505 [ALM 4-12]“
> „Einmalige Schüttleistung bei 40°C Zapftemp. - Elektroheiz. lt. 660 [ALM 2-8] 660 [ALM 4-12]“
> „Maximale Betriebsdruck Brauchwasserseite bar 10 [ALM 2-8] 10 [ALM 4-12]“
> „Trinkwarmwasserspeicher lt. 270 [ALM 2-8] 270 [ALM 4-12]“

---

## 22. (Runde 21) TopTronic E WW-Ladevorrang & Energiezwangrampe sowie Navigator 2.0 Bivalenz-Warmwassernachladung & Boost-Funktion

### Fund 22.1: TopTronic E Ladevorrang-Strategien (Absolut, Parallel, Energiezwangrampe) & Fühleranzahl (05-002, 30-049)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 154 & 159–160, Kap. 10.3.5 WW-Ladevorrang & Kap. 10.3.6 Fühleranzahl)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „Bei Vorrangladung (Einstellung 05-002 = 0 h) wird nur die eingestellte Warmwasser Ladeleistung angefordert. Ebenso wird ein negativer Energiezwang generiert, womit andere Verbraucherkreise gesperrt werden können.“
> „Bei Einstellung 0.1 h wird parallel zu einer zusätzlichen Anforderung geladen. Dabei wird kein Energiezwang generiert und für angeforderte Leistung wird nicht auf die eingestellte Warmwasser Ladeleistung begrenzt.“
> „Bei Einstellung > 0.1 h wird die Ladung parallel gemacht und lastabhängig wird eine Energiezwangrampe für die Ladetemperatur generiert. Unterschreitet die Ladetemperatur die Rampe, wird ein negativer Energiezwang generiert. Heizkreise werden freigegeben, wenn die Rampentemperatur erreicht wird.“
> „Fühleranzahl (Konfiguration 30-049): 0 = Kontakt Der Speicher wird über einen potentialfreien Kontakt (an SF1) mit der Speicherladetemperatur (WW-Soll + Überhöhung Ladesollwert 05-001) geladen.“
> „1 = Ein Speicherfühler Der Speicher wird bei Temperaturunterschreitung (WW-Soll – Einschaltdifferenz 05-000) mit der Speicherladetemperatur (WW-Soll + Überhöhung Ladesollwert 05-001) geladen bis am Fühler WW-Soll erreicht wird.“

### Fund 22.2: Navigator 2.0 Bivalente Warmwassernachladung bei tiefen Außentemperaturen, Boost-Temperatur & Einmalladung
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 19 & 42–43, Kap. 2.6.2 Bedienfeld „Warmwasser“ & Kap. 2.8.5 Speichermanagement)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Mit Hilfe der „Bivalenten Warmwassernachladung“ wird auch bei tiefen Außentemperaturen, die eingestellte „Warmwasserladung Ausschalttemperatur“ durch Zuschaltung des zweiten oder dritten Wärmeerzeugers erreicht.“
> „Bei Anlagen mit zweitem oder dritten Wärmeerzeuger kann die „Bivalente Warmwassernachladung“ eingestellt werden.“
> „TWW-Erwärmer Solltemperatur [50°C] Dieser Parameter gibt die Ausschalttemperatur für die Warmwasserladung an.“
> „TWW-Erwärmer Nachladetemperatur [46°C] Dieser Parameter gibt die Einschalttemperatur für die Warmwasserladung an.“
> „Boost-Temperatur [60°C] Dieser Parameter gibt die Ausschalttemperatur für die Boost-Ladung an (nur bei iPump konfigurierbar).“
> „Im Menü „System/Warmwasser“ kann eine „Einmalige Warmwasserladung“ und bei der iPump eine „Einmalige Boost-Ladung“ gestartet werden.“

---

## 23. (Runde 22) TopTronic E Zirkulationspumpen-Steuerungsmodi & Navigator 2.0 PV-Warmwasserspeicherung

### Fund 23.1: TopTronic E Zirkulationspumpen-Steuerungsmodi (0–12) mit Ladeabschaltung & Drehzahlregelung (05-006, 07-020, 07-021)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 155 & 162, Kap. 10.3.13 Zirkulationspumpe)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „Mit der Einstellung kann die Zirkulationspumpenfunktion aktiviert werden: 0 = Inaktiv 1 = Aktiv nach Zeitprogramm mit Sollwertweiterleitung 2 = Zeitprogramm mit Temperaturfreigabe u. Sollwertweiterleitung 3 = Zeitprogramm mit Sollwertweiterleitung u. Drehzahlregelung 4 = Aktiv nach Zeitprogramm ohne Sollwerteiterleitung 5 = Zeitprogramm mit Temperaturfreigabe ohne Sollwertweiterleitung 6 = Zeitprogramm ohne Sollwertweiterleitung u. Drehzahlregelung 7 = Aktiv nach Zeitprogramm mit Sollwertweiterleitung u. Pumpenabschaltung 8 = Zeitprogramm mit Temperaturfreigabe, Sollwertweiterleitung u. Pumpenabschaltung 9 = Zeitprogramm mit Sollwertweiterleitung, Drehzahlregelung, u. Pumpenabschaltung 10 = Aktiv nach Zeitprogramm ohne Sollwertweiterleitung u. Pumpenabschaltung 11 = Zeitprogramm mit Temperaturfreigabe ohne Sollwertweiterleitung u. Pumpenabschaltung 12 = Zeitprogramm ohne Sollwertweiterleitung mit Drehzahlregelung u. Pumpenabschaltung“
> „Bei Einstellung 7 bis 12 wird die Zirkulationspumpe bei WW-Ladung abgeschaltet.“
> „Das Zirkulation-Schaltzeitenprogramm wird in allen Einstellungen berücksichtigt – bei einem Schaltzeitenwert kleiner 15°C erfolgt eine Abschaltung der Pumpe.“
> „Sobald eine Drehzahlregelung aktiviert wurde wird diese an VA4 ausgegeben, dies ist nicht veränderlich und es darf daher am Regler nur eine Zirkulation mit Drehzahlregelung aktiviert werden.“

### Fund 23.2: Navigator 2.0 PV-Trinkwarmwasserladung & Maximaltemperaturbegrenzung (PV 002, PV 005)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.ekoflam.at/Dokumentation/IDM-Navigator-Technische-Dokumentation.pdf
- **Lokale Datei:** quellen/IDM_Navigator_Technische_Dokumentation.pdf (Seite 22, Kap. 2.5 Einstellungen)
- **Datum der Quelle:** 2021
- **Wörtliches Zitat:**
> „PV 002 Trinkwarmwasserbereitung [Ja/Nein] Wenn dieser Parameter auf „Ja“ eingestellt ist, dann wird der Trinkwarmwasserspeicher mit PV-Strom geladen. Dies geschieht unabhängig von der Einstellung des Warmwasserzeitprogrammes. Die Warmwasserladung wird beendet, wenn die PV-Leistung während der Warmwasserladung unter die angeforderte (notwendige) PV-Leistung abfällt und die Mindestlaufzeit überschritten ist.“
> „PV 005 TWW-Erwärmer Maximaltemperatur [50 °C] Dieser Parameter gibt die Maximaltemperatur vom Trinkwarmwasser-Erwärmer an. Der einstellbare Bereich ist abhängig von der Wärmepumpenmaximaltemperatur.“
> „Der von der PV-Anlage zur Verfügung gestellte Solarstrom wird genutzt um die Warmwasserbereitung durchzuführen, die Heizungsanlage zu bewirtschaften/überhöhen bzw. die Kühlung durchzuführen.“

---

## 24. (Runde 23) TopTronic E WW-Ladedauerbegrenzung / Unterbrechung & Navigator 2.0 Zirkulationszeiten-Taktung

### Fund 24.1: TopTronic E Maximale Warmwasser-Ladedauer (05-081) & Unterbrechung (05-083) zur Heizsicherung
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 156, Kap. Warmwasser .. – Parameter)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „05-081 Maximale Warmwasser Ladedauer 1,0 h 0,0 10,0 Wird die eingestellte Maximalladedauer überschritten, wird der Ladevorgang unterbrochen und erst wieder gestartet, wenn die Einschaldifferenz (05-00) zur aktuellen Warmwassertemperatur unterschritten wird.“
> „05-083 Unterbrechung Warmwasserladung 0,2h 0,0 10,0 Unterbrechung Warmwasserladung“
> „05-008 Nachlaufzeit WW_Ladepumpe 60sec 0 600 Nachlaufzeit der WW-Ladepumpe (SLP1)“
> „05-009 Nachlaufzeit Brauchwasserpumpe BWP 60sec 0 600 Nachlaufzeit der Brauchwasserpumpe (SLP2)“

### Fund 24.2: Navigator 2.0 Zirkulationspumpen-Taktung (Laufzeit 0–60 min / Pausenzeit 0–240 min)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 20 & 45, Kap. 2.6.2 Warmwasserzirkulation & Kap. 2.8.6 Trinkwarmwasserbereitung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Laufzeit Zirkulation (10 min) Dieser Parameter gibt die Laufzeit (0 - 60 min) der Zirkulationspumpe an.“
> „Pausenzeit Zirkualtion (30 min) Dieser Parameter gibt die Pausenzeit (0 - 240 min) der Zirkulationspumpe an.“
> „Bei Anwahl von „Zeitprogramm Zirkulation“ kann die Laufzeit und die Pausenzeit der Warmwasser-Zirkulationspumpe eingestellt werden. Durch Anwählen des Wochentages und eines oder mehrerer Zeitabschnitte (0-24h) kann das Zeitprogramm eingestellt werden.“
> „Im Menü „Zirkulation“ kann die Lauf- und Pausenzeit der Zirkulationspumpe, sowie das Zeitprogramm für die Zirkulation eingestellt werden.“

---

## 25. (Runde 24) TopTronic E WW-Lademodi / Freigabetemperatur Nachladung & iDM bivalente Frostschutz-Ladepumpenschaltung / Sole-Zwischenkreis

### Fund 25.1: TopTronic E Warmwasserlademodi (Register, Lademodul, Nachladung 05-010) & Sperr-Kontakt Elektroheizeinsatz (30-031)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 153, 157 & 160, Kap. Warmwasser.. – Konfiguration / Parameter & Kap. 10.3.7 Modus Warmwasserladung)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „30-031 Zuo. Eing. Sperr-Kontakt ELH 0=AUS Zuordnung Eingang Sperr-Kontakt Elektroheizeinsatz (WW-Nachladung)“
> „05-010 Freigabetemperatur Nachladung 70,0°C 30 70 Bei entsprechend eingestelltem Warmwasserladung Lademodus kann mit diesem Einsteller eine Nachladetemperatur eingestellt werden. Ist die Warmwassertemperatur höher als die eingestellte Nachladetemperatur, wird die Ladeanforderung an die zentrale Wärmeerzeugeranlage abgeschaltet und eine Warmwasserinterne Ladung eingeschaltet.“
> „10.3.7 Modus Warmwasserladung (Parameter 05-011): Register Die Speicherladepumpe SLP1 wird bei Ladungsanforderung aktiviert wenn der Entladeschutz (05-005) deaktiviert ist oder der Entladeschutz aktiviert ist und die zugeordnete Vorlauf- oder Rücklauftemperatur die Speichertemperatur oben überschreitet oder Sollwertanforderungstyp (05-087) auf „keine“ gestellt ist oder Speicherfühler auf „0“ eingestellt ist Lademodul die SLP1 wird geschalten wie bei Register, die SLP2 wird geschalten wenn die zugeordnete Vorlauf- oder Rücklauftemperatur über die „Einschalttemp. WW Speicherkreispumpe“ (05-052) steigt (Bei Wert „0“ wird auf Überschreitung gegenüber dem WW-Sollwert geprüft). Wenn die Temperaturen um eine eingestellte Hysterese (05-058) sinken dann wird die SLP2 wieder abgeschalten. Primär thermisch Bei Ladungsanforderung werden SLP1 und SLP2 ohne Temperaturprüfung geschalten (zB für Verwendung thermischer Ventile) Register + Nachladung Wie „Register“ jedoch mit Nachladung (Paramter 05-010) Lademodul + Nachladung Wie „Lademodul“ jedoch mit Nachladung (Paramter 05-010)“

### Fund 25.2: iDM Frostschutz-Ladepumpenschaltung für Verbindungsleitungen & PWM-Signal für Sole-Zwischenkreispumpe
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.siblik.com/fileadmin/mam/medias/docus/148/IDM193411u412_ma_de_812606_iPump-ALM-2-12---2.0%20Datenbl.pdf
- **Lokale Datei:** quellen/812606_iPump_ALM_2-12.pdf (Seite 37, Kap. 5.7 Frostschutzfunktion & Kap. 5.8 Sole-Zwischenkreis)
- **Datum der Quelle:** 2021
- **Wörtliches Zitat:**
> „Für Wärmepumpen die bivalent-alternativ betrieben werden, oder bei denen längere Stehzeiten auftreten können, steht zusätzlich eine Frostschutzfunktion für die Außeneinheit zur Verfügung. Unterschreitet die Außentemperatur die im Navigator einstellbare Frostschutzaußentemperatur und die Vorlauftemperatur der Wärmepumpe die einstellbare Minimaltemperatur, wird die Ladepumpe gestartet bis die Verbindungsleitungen wieder auf Temperatur sind.“
> „Es wird ein Solekreis mit einem bauseitigem Zwischenwärmetauscher, einer Zwischenkreispumpe, einer Sicherheitsgruppe, sowie einen Ausdehnungsgefäß ausgeführt. Dabei muss darauf geachtet werden, dass die eingesetzte Ladepumpe (M73-1) und die zusätzliche bauseitige Zwischenkreispumpe (M73-2) mit dem gleichen Steuersignal (PWM-Heizen) betrieben werden können. Die Ladepumpe und die Zwischenkreispumpe werden mit dem selben Steuersignal der Ladepumpe M73 geregelt.“

---

## 26. (Runde 25) Hoval Glattrohr-Wärmetauscherdimensionierung & Navigator 2.0 Bivalenz-Legionellenüberhöhung

### Fund 26.1: Hoval Wärmetauscherflächen-Dimensionierung für Warmwasserspeicher & E-Heizeinsatz-Einsatzbereiche
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.hoval.ch/de_CH/medias/sys_master/celum_assets/4221940_UltraSource-B-Technikhandbuch_de.pdf
- **Lokale Datei:** quellen/Hoval_UltraSource_B_Technikhandbuch.pdf (Seite 19 & 40, Kap. Technische Daten Diagramme Einsatzbereich & Projektierung Allgemein)
- **Datum der Quelle:** 2026
- **Wörtliches Zitat:**
> „Idealerweise kommen Wassererwärmer mit grossen innen liegenden Glattrohrregistern (CombiVal ESR und ESSR) zum Einsatz. Für die Dimensionierung der WT-Fläche ist die max. Heizleistung der Wärmepumpe massgebend: • WT-Fläche = 0.3-0.4 m2 pro kW max. WP-Heizleistung während der Betriebszeit der Anlage (Luft/Wasser-Wärmepumpen bei A20/W55) • Bei 2-stufigen Wärmepumpen kann die Leistung der ersten Stufe eingesetzt werden“
> „Erweiterter Einsatzbereich Heizen Wärmepumpe inklusive E-Heizeinsatz“
> „Erweiterter Einsatzbereich Warmwasser Wärmepumpe inklusive E-Heizeinsatz“
> „Es sind pro Person 0.25 kW zur Heizleistung hinzuzufügen. Das entspricht einem Warmwasserbedarf von ca. 50 Liter mit 45 °C pro Tag.“

### Fund 26.2: Navigator 2.0 Legionellenfunktion mit zweitem/drittem Wärmeerzeuger (60–67 °C Ausschalttemperatur & Intervall 0–7 Tage)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 43–44, Kap. 2.8.5 Speichermanagement - Legionellenfunktion)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Bei Anlagen mit zweitem oder dritten Wärmeerzeuger kann die „Legionellenfunktion“ eingestellt werden. Im Menü „Legionellenfunktion“ kann eine Warmwasserüberhöhung, mittels zweitem oder drittem Wärmeerzeuger, eingestellt werden.“
> „Legionellenfunktion [Aus / Zweiter Wärmeerzeuger / Dritter Wärmeerzeuger] Dieser Parameter gibt an, ob die Legionellenfunktion mit dem zweiten oder dritten Wärmeerzeuger durchgeführt wird (nur einstellbar wenn Bivalenz konfiguriert).“
> „Legionellenfunktion Temperatur Dieser Parameter gibt die Ausschalttemperatur (60 - 67°C) für die Legionellenfunktion an.“
> „Legionellenfunktion Intervall Dieser Parameter gibt den Intervall (0 - 7 Tage) für die Legionellenfunktion an. 0 ... Überhöhung bei jeder Warmwasserladung 1 ... Überhöhung 1x täglich 2 ... Überhöhung alle 2 Tage, usw. 7 ... Überhöhung 1x wöchentlich“

---

## 27. (Runde 26) TopTronic E Speicherfühler-Schichtlogik / Entladeschutz & Navigator 2.0 Bivalenz-WW-Nachladung / Zirkulationstakt

### Fund 27.1: TopTronic E Speicherfühler-Konfiguration (30-049: 1 Fühler SF1 vs. 2 Fühler SF1/SF2) & Entladeschutz (05-005)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 160, Kap. 10.3.6 Fühleranzahl & 10.3.7 Modus Warmwasserladung)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „10.3.7 Modus Warmwasserladung (Parameter 05-011): Register Die Speicherladepumpe SLP1 wird bei Ladungsanforderung aktiviert wenn der Entladeschutz (05-005) deaktiviert ist oder der Entladeschutz aktiviert ist und die zugeordnete Vorlauf- oder Rücklauftemperatur die Speichertemperatur oben überschreitet oder Sollwertanforderungstyp (05-087) auf „keine“ gestellt ist oder Speicherfühler auf „0“ eingestellt ist“

### Fund 27.2: Navigator 2.0 Bivalente Warmwassernachladung bei tiefen Außentemperaturen & Zirkulations-Lauf-/Pausenzeiten
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 42–45, Kap. 2.8.5 Speichermanagement & 2.8.6 Trinkwarmwasserbereitung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Mit Hilfe der „Bivalenten Warmwassernachladung“ wird auch bei tiefen Außentemperaturen, die eingestellte „Warmwasserladung Ausschalttemperatur“ durch Zuschaltung des zweiten oder dritten Wärmeerzeugers erreicht.“
> „Im Menü „Warmwasserstation“ kann die Warmwasser-Zapftemperatur (Solltemperatur) eingestellt werden. Im Menü „Zirkulation“ kann die Lauf- und Pausenzeit der Zirkulationspumpe, sowie das Zeitprogramm für die Zirkulation eingestellt werden.“













