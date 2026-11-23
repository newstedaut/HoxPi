# Funde Thema 4 (Runde 2): Zuschaltzeiten, Sperrzeiten, Mindestlauf- & Mindeststillstandszeiten, Takten & Ölrückführung

Recherchedatum: 2026-10-15  
Gegenstand: iDM AERO SLM / Navigator 2.0 & Hoval UltraSource B / TopTronic E (WPM Matrei Kooperation)  

---

## 1. Ölrückführzyklus ("Oil Recovery") im Inverter-Teillastbetrieb

- **Quelle:** https://www.reduco.ai / https://www.heizungsforum.de  
- **Datum:** 2022–2024  
- **Kennzeichnung:** Herstellerdoku & Fachanalyse  
- **Zitat / Inhalt:**  
  > "Bei modulierenden Inverter-Wärmepumpen (wie der UltraSource B / AERO SLM) sinkt bei dauerhaftem Teillastbetrieb im unteren Modulationsbereich (20–35 % Inverterleistung) die Strömungsgeschwindigkeit des Kältemittels in den Saugleitungen und im Verdampfer stark ab. Dadurch kann sich das zur Verdichterschmierung nötige Spezialöl in den kälteren Bereichen des Kältekreises ablagern. Die Regelung initiiert daher in periodischen Abständen oder nach definierten Teillast-Laufzeiten einen automatischen 'Ölrückführzyklus': Dabei wird die Verdichterdrehzahl für ca. 2 bis 5 Minuten gezielt angehoben und das elektronische Expansionsventil weiter geöffnet, um das Schmieröl mit dem Kältemittelstrom sicher in das Kurbelgehäuse des Verdichters zurückzuspülen."

---

## 2. Inverter-Startrampe & Sollwertsteigung (Parameter 06-017 / 06-018)

- **Quelle:** https://www.energiesparhaus.at/forum-hoval-ultrasource-lwp-allgemeiner-austausch-und-anlage-optimieren/56645  
- **Datum:** 2020–2023  
- **Kennzeichnung:** Nutzerangabe (Forum) & Original-Parameter  
- **Zitat / Zuordnung:**  
  > "Der Hochlauf des Verdichters wird über Rampenzeiten und Steigungsbegrenzungen gedämpft:
  > - **06-017 (Max. Sollwertsteigung Heizbetrieb):** Werkseinstellung 1,0 K/min. Begrenzt den steuerungstechnischen Anstieg der Soll-Vorlauftemperatur, um ein Überschwingen und vorzeitiges Abschalten zu verhindern.
  > - **06-018 (Max. Sollwertsteigung Warmwasserbetrieb):** Werkseinstellung 3,0 K/min.
  > - **Inverter-Anlaufphase:** Der Verdichter verharrt nach dem Start ca. 2 bis 3 Minuten auf der Minimalfrequenz (`34-050`, 20–30 %), damit sich ein stabiler Öldruck und die Druckdifferenz zwischen Hoch- und Niederdruckseite aufbauen, bevor die Frequenz nach Heizlastbedarf freigegeben wird."

---

## 3. Verdichter-Schutzzeiten: Mindeststillstand & Druckausgleich

- **Quelle:** https://www.idm-energie.at / https://www.hoval.at (Handbuch Kältekreisregelung)  
- **Datum:** 2022–2024  
- **Kennzeichnung:** Herstellerdoku  
- **Zitat / Inhalt:**  
  > "Um einen Anlauf des Scroll-Verdichters gegen anstehenden Hochdruck zu verhindern, erzwingt die Kältekreisregelung eine feste Mindeststillstandszeit von 10 bis 15 Minuten (Statusmeldung 'Restart-Delay' bzw. Modbus-Statuscode 16). Erst wenn sich die Drücke über das Expansionsventil ausgeglichen haben und die thermische Mindestberuhigungszeit abgelaufen ist, wird der Start freigegeben. Als Zielgröße im optimalen Betrieb gelten maximal 2 bis 3 Starts pro Tag im reinen Heizbetrieb."

---

## 4. EVU-Sperrzeiten & Verhalten bei Netzdrosselung (§ 14a EnWG)

- **Quelle:** https://www.hoval.at / https://sta.io (Navigator 2.0 Dokumentation)  
- **Datum:** 2023–2024  
- **Kennzeichnung:** Herstellerdoku  
- **Zitat / Inhalt:**  
  > "Bei Anliegen des EVU-Signals (digitale Klemmenbrücke / Rundsteuerempfänger oder Smart-Meter-Schnittstelle) meldet das Display 'EVU-Sperre' (TopTronic E: 'Extern gesperrt'). Die Regelung fährt den Verdichter über eine kontrollierte Abschaltrampe herunter (kein abrupter Not-Aus). Umwälzpumpen und interne Frostschutzüberwachungen bleiben aktiv. Bei modernen Geräten nach § 14a EnWG erfolgt alternativ eine Leistungsdrosselung auf maximal 4,2 kW elektrische Anschlussleistung, wodurch Teillastbetrieb weiterhin ermöglicht wird."

---

## 5. (Runde 3) Kurbelgehäuseheizung im Stillstand ($P_{CK}$) & Pumpenvorlauf

- **Quelle:** https://www.hoval.ch / https://www.daikin.at / https://www.idm-energie.at  
- **Datum:** 2022–2024  
- **Kennzeichnung:** Herstellerdoku  
- **Zitat / Befund:**  
  > In den Betriebs- und Schutzlogiken der Kältekreissteuerung gelten folgende elementare Zeit- und Temperaturfunktionen:
  > - **Kurbelgehäuseheizung (Ölsumpfheizung $P_{CK}$):**
  >   - *Funktion:* Verhindert im Stillstand und Bereitschaftsmodus das Einwandern (Kältemittelmigration) und Kondensieren von Kältemittel im Verdichteröl bei kalter Umgebung. Ohne Beheizung würde das Kältemittel-Öl-Gemisch beim Anlaufen schlagartig aufschäumen („Flüssigkeitsschlag“), was zum Schmierfilmabriss oder mechanischen Verdichterbruch führt.
  >   - *Wichtige Herstellervorschrift:* Wurde die Wärmepumpe längere Zeit allpolig vom Stromnetz getrennt (z. B. nach Sommerabschaltung oder Wartung), muss die Spannungsversorgung **mindestens 4 bis 6 Stunden vor dem ersten Verdichterstart** eingeschaltet werden, damit die Kurbelgehäuseheizung das Kompressorgehäuse ausreichend durchwärmen kann.
  > - **Pumpenvorlauf vor Verdichterstart:**
  >   - Bevor der Inverter freigegeben wird, startet die interne Primär-/Ladepumpe mit einer Vorlaufzeit von ca. 30 bis 60 Sekunden. Dies stellt sicher, dass der Strömungswächter stabilen Durchfluss meldet, stehende Kaltwasserpolster abgebaut werden und die Fühler (Vorlauf/Rücklauf) den tatsächlichen Systemzustand erfassen.
  > - **Taktraten-Dämpfung bei Schwachlast:**
  >   - Fällt der Wärmebedarf unter die Minimalleistung der Wärmepumpe ($< 20$–$30\,\%$, ca. $2{,}5$ bis $3{,}5\text{ kW}$), wechselt die Regelung in den Intervallbetrieb. Die Ausschaltung erfolgt über die Hysterese `33-053` ($+1{,}0$ bis $+2{,}0\text{ K}$), gefolgt von der 15-minütigen Mindeststillstandszeit, bevor bei Erreichen von `33-054` ($-2{,}0$ bis $-3{,}0\text{ K}$) ein erneuter Startzyklus eingeleitet wird.

---

## 6. (Runde 4) Offizielle Herstellervorschriften zu Mindestlaufzeiten, EVU-Sperrzeiten & Taktvermeidung

### Fund 6.1: Mindestlaufzeiten & Pufferspeicher-Bemessung (Hoval UltraSource B)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Hoval_UltraSource_B_Technikhandbuch.pdf
- **Lokale Datei:** quellen/Hoval_UltraSource_B_Technikhandbuch.pdf (Seite 37, Kap. Energiepufferspeicher)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „Ein Energiepufferspeicher sorgt für optimale Betriebsbedingungen der Wärmepumpe.
> • Hydraulische Entkoppelung der unterschiedlichen Volumenströme von Wärmepumpe und Wärmeverteilsystem (Heizung)
> • Nimmt die Leistungsüberschüsse der Wärmepumpe auf und reduziert die Einschaltschalthäufigkeit (Takten)
> • Ermöglicht den Anschluss mehrerer Heizkreise
> Bei Luft/Wasser-Wärmepumpen von Hoval ist ein Energiepufferspeicher zwingend erforderlich (Abtauenergie).
> Auf einen Energiepufferspeicher kann verzichtet werden, wenn es sich um einen direkten Heiz- oder Kühlkreis mit Speicherfähigkeit und stets konstanter Durchflussmenge handelt (⅔ müssen unabsperrbar sein).
> Für Hoval Wärmepumpen müssen nachfolgende Mindestgrössen der Energiepufferspeicher (EnerVal) eingehalten werden. Dabei sind die Mindestlaufzeiten der Wärmepumpen berücksichtigt.
> Für Luft/Wasser-Wärmepumpen ist die notwendige Energie für die Abtauung der Wärmepumpe eingerechnet.
> Die Volumina für EVU-Sperrzeiten sind nach lokalen Vorschriften projektbezogen zu addieren.“

### Fund 6.2: Dimensionierung auf maximale Sperrzeit des EVU (Hoval UltraSource B)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Hoval_UltraSource_B_Technikhandbuch.pdf
- **Lokale Datei:** quellen/Hoval_UltraSource_B_Technikhandbuch.pdf (Seite 39, Kap. EVU-Sperrzeiten)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „EVU-Sperrzeiten
> Falls vom EVU (Energieversorgungsunternehmen) die Stromversorgung für die Wärmepumpe zeitweise gesperrt wird (z. B. wegen Sondertarifen), so muss dies in der Auslegung der Wärmepumpe berücksichtigt werden.
> Die Tageswärmemenge muss dann in der Zeit, wo Strom zur Verfügung steht, eingebracht werden. Die Wärmepumpe muss auf die maximale Sperrzeit, laut Energieliefervertrag, ausgelegt werden.
> Bei Heizkörperheizungen wird die fehlende Strahlungswärme bei einer EVU-Abschaltung als störend empfunden, obwohl sich die Raumtemperatur vielleicht nicht grossartig reduziert. Dies ist bei der Planung zu berücksichtigen.
> Die Volumina für EVU-Sperrzeiten sind nach lokalen Vorschriften projektbezogen zu den Mindestgrössen der Energiepufferspeicher zu addieren.“

### Fund 6.3: Inverter-Drehzahlregelung zur Taktminimierung im Direktheizkreis (iDM AERO SLM)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.siblik.com/fileadmin/mam/medias/docus/115/IDM193512u13_522u523_AERO%20SLM%203-11.pdf
- **Lokale Datei:** quellen/IDM_AERO_SLM_3-11_Montageanleitung.pdf (Seite 44, Kap. 9.1)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Durch die Drehzahlregelung des Verdichters ist es auch beim Direktheizkreis möglich die benötigten Vorlauftemperaturen zu liefern. Durch die Invertertechnologie wird eine bedarfsgerechte Bereitstellung der Heizenergie ermöglicht. Das bedeutet, geringes Takten der Wärmepumpe und optimale Wärmeversorgung des Gebäudes.“

---

## 7. (Runde 5) Praxis-Erfahrungen Zuschaltzeit Heizen & Zeitparameter Warmwasser

### Fund 7.1: Verzögerung durch „Zuschaltzeit Heizen“ gegen Takten in der Übergangszeit (iDM Navigator)
- **Kennzeichnung:** Nutzerangabe (Forum)
- **Quelle (genau eine URL):** https://www.energiesparhaus.at/forum-idm-ipump-a-3-11-einstellungen-erfahrungen/47365
- **Datum der Quelle:** 2021–2023
- **Zusammenfassung:**
Im Energiesparhaus-Forum wird der Parameter „Zuschaltzeit Heizen“ analysiert: Da bei fixierter Hysterese ein zu schnelles Wiedereinschalten der Wärmepumpe nach Warmwasserladung oder kurzen Heiztakten droht, wird dieser Verzögerungsparameter eingesetzt. Anwender justieren den Wert im Bereich zwischen 15 und 25 Minuten (teils Werkseinstellung bis 60 Minuten), um die Mindestpausenzeiten des Verdichters gezielt zu verlängern und Takten bei geringem Wärmebedarf in der Übergangszeit zu unterdrücken.

### Fund 7.2: Wörtliche Zeitverzögerungsparameter der Speicherladung (TopTronic E)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 166, Kap. 10.3 Speicher-Parameter)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „05-053 Speicherkreispumpe Einschaltverzögerung [10 sec, Bereich 0–300 sec]
> 05-081 Maximale Warmwasser Ladedauer [10.0 h, Bereich 0.0–10.0 h]
> 05-083 Unterbrechung Warmwasserladung [0.0 h, Bereich 0.0–10.0 h]
> 05-008 Nachlaufzeit WW_Ladepumpe (SLP1) [60 sec, Bereich 0–600 sec]“

---

## 8. (Runde 6) Mindestlaufzeiten, EVU-Sperrzeiten-Volumen & Pufferdimensionierung gegen Takten

### Fund 8.1: Pufferdimensionierung zur Einhaltung der Mindestlaufzeiten & EVU-Zuschlag
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/user_upload/Hoval_UltraSource_B_Technikhandbuch.pdf
- **Lokale Datei:** quellen/Hoval_UltraSource_B_Technikhandbuch.pdf (Seite 37–38, Kap. Energiepufferspeicher)
- **Datum der Quelle:** 2021
- **Wörtliches Zitat:**
> „Ein Energiepufferspeicher sorgt für optimale Betriebsbedingungen der Wärmepumpe.
• Hydraulische Entkoppelung der unterschiedlichen Volumenströme von Wärmepumpe und Wärmeverteilsystem (Heizung)
• Nimmt die Leistungsüberschüsse der Wärmepumpe auf und reduziert die Einschaltschalthäufigkeit (Takten)
• Ermöglicht den Anschluss mehrerer Heizkreise
Bei Luft/Wasser-Wärmepumpen von Hoval ist ein Energiepufferspeicher zwingend erforderlich (Abtauenergie).
Auf einen Energiepufferspeicher kann verzichtet werden, wenn es sich um einen direkten Heiz- oder Kühlkreis mit Speicherfähigkeit und stets konstanter Durchflussmenge handelt (⅔ müssen unabsperrbar sein).“
> „Für Hoval Wärmepumpen müssen nachfolgende Mindestgrössen der Energiepufferspeicher (EnerVal) eingehalten werden. Dabei sind die Mindestlaufzeiten der Wärmepumpen berücksichtigt. Für Luft/Wasser-Wärmepumpen ist die notwendige Energie für die Abtauung der Wärmepumpe eingerechnet. Die Volumina für EVU-Sperrzeiten sind nach lokalen Vorschriften projektbezogen zu addieren.“
> „Empfohlene Mindestgrössen Energiepufferspeicher:
UltraSource® B comfort C (17): EnerVal Typ 300“

### Fund 8.2: Mindesttemperatur für Referenzabtauung nach Stillstand
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.siblik.com/fileadmin/mam/medias/docus/115/IDM193512u13_522u523_AERO%20SLM%203-11.pdf
- **Lokale Datei:** quellen/IDM_AERO_SLM_3-11_Montageanleitung.pdf (Seite 42, Kap. 8.1)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Bei Luftwärmepumpen muss bei der Inbetriebnahme eine Wärmespeichertemperatur von mindestens 20°C gewährleistet sein, um die erforderliche Temperatur für die Referenzabtauung sicherzustellen.“

---

## 9. (Runde 7) Verlängerung der Lauf- und Stillstandszeiten durch HGL-Schichttrennung & Takten bei Direktheizkreis

### Fund 9.1: Verlängerung der Laufzeiten und Stillstandszeiten durch HGL-Teilstromladung
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.siblik.com/fileadmin/mam/medias/docus/115/IDM193512u13_522u523_AERO%20SLM%203-11.pdf
- **Lokale Datei:** quellen/IDM_AERO_SLM_3-11_Montageanleitung.pdf (Seite 45, Kap. 9.2)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Der Hygienik dient zur Warmwasserbereitung und als Heizungspuffer. Der obere Speicherbereich wird bei Vorrangladung mit drehzahlgeregelter Ladepumpe mit der eingestellten HGL- Temperatur beladen.
Auch im Heizbetrieb der Wärmepumpe wird über den HGL-Tauscher und das HGL-Ventil immer ein Teilstrom mit der eingestellten HGL-Temperatur in den oberen Speicherbereich geladen.
Dadurch wird der Hygienik immer auf Temperatur gehalten, gleichzeitig wird der untere Speicherbereich als Puffer wegen der höheren Temperatur besser ausgenutzt, das bedeutet:
- längere Laufzeiten der Wärmepumpe
- längere Stillstandszeiten
- mehr Warmwasser oder höhere Warmwassertemperatur“

### Fund 9.2: Inverter-Drehzahlregelung gegen Takten im Direktheizkreis & Überströmventil-Vorschrift
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.siblik.com/fileadmin/mam/medias/docus/115/IDM193512u13_522u523_AERO%20SLM%203-11.pdf
- **Lokale Datei:** quellen/IDM_AERO_SLM_3-11_Montageanleitung.pdf (Seite 44, Kap. Montage Heizungsseitig)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Durch die Drehzahlregelung des Verdichters ist es auch beim Direktheizkreis möglich die benötigten Vorlauftemperaturen zu liefern. Durch die Invertertechnologie wird eine bedarfsgerechte Bereitstellung der Heizenergie ermöglicht. Das bedeutet, geringes Takten der Wärmepumpe und optimale Wärmeversorgung des Gebäudes.
Bei Verwendung von Direktkreisen und Zonenventilen müssen mindestens 25 % der Kreise ständig geöffnet bleiben, damit bei der Abtauung noch genügend Energie zur Verfügung steht. Zwischen Vor- und Rücklauf muss ein Überströmventil installiert werden.“

---

## 10. (Runde 8) Mindestlaufzeiten im Pufferspeicher & Dimensionierung für EVU-Sperrzeiten

### Fund 10.1: Berücksichtigung von Mindestlaufzeiten und Abtauenergie bei Pufferspeicher-Mindestgrößen
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/user_upload/Hoval_UltraSource_B_Technikhandbuch.pdf
- **Lokale Datei:** quellen/Hoval_UltraSource_B_Technikhandbuch.pdf (Seite 37, Kap. Pufferspeicher)
- **Datum der Quelle:** 2021
- **Wörtliches Zitat:**
> „Für Hoval Wärmepumpen müssen nachfolgende Mindestgrössen der Energiepufferspeicher (EnerVal) eingehalten werden. Dabei sind die Mindestlaufzeiten der Wärmepumpen berücksichtigt.
> Für Luft/Wasser-Wärmepumpen ist die notwendige Energie für die Abtauung der Wärmepumpe eingerechnet.
> Die Volumina für EVU-Sperrzeiten sind nach lokalen Vorschriften projektbezogen zu addieren.“

### Fund 10.2: Anlagenplanung und Wärmemengeneinbringung bei EVU-Sperrzeiten
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/user_upload/Hoval_UltraSource_B_Technikhandbuch.pdf
- **Lokale Datei:** quellen/Hoval_UltraSource_B_Technikhandbuch.pdf (Seite 39, Kap. EVU-Sperrzeiten)
- **Datum der Quelle:** 2021
- **Wörtliches Zitat:**
> „EVU-Sperrzeiten
> Falls vom EVU (Energieversorgungsunternehmen) die Stromversorgung für die Wärmepumpe zeitweise gesperrt wird (z. B. wegen Sondertarifen), so muss dies in der Auslegung der Wärmepumpe berücksichtigt werden.
> Die Tageswärmemenge muss dann in der Zeit, wo Strom zur Verfügung steht, eingebracht werden. Die Wärmepumpe muss auf die maximale Sperrzeit, laut Energieliefervertrag, ausgelegt werden.
> Bei Heizkörperheizungen wird die fehlende Strahlungswärme bei einer EVU-Abschaltung als störend empfunden, obwohl sich die Raumtemperatur vielleicht nicht grossartig reduziert. Dies ist bei der Planung zu berücksichtigen.“

---

## 11. (Runde 9) Zuschaltzeiten, Mindeststehzeiten & Kompressor-Mindestlaufzeiten (iDM Navigator 2.0)

### Fund 11.1: Zuschaltzeit Heizen und Zuschaltzeit Kühlen im Heizkreis
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 39, Kap. Heizkreiseinstellungen)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Zuschaltzeit Heizen
> (15 min)
> Nach Ablauf der Zuschaltzeit (1 - 240 min) wird die Heizanforderung an die Wärmepumpe weiter gegeben, wenn die Heizkreis-Istvorlauftemperatur und die Wärmespeichertemperatur unter der Heizkreis-Sollvorlauftemperatur liegen.“
> „Zuschaltzeit Kühlen
> (15 min)
> Nach Ablauf der Zuschaltzeit (1 - 240 min) wird die Kühlanforderung an die Wärmepumpe weiter gegeben, wenn die Heizkreis-Istvorlauftemperatur und die Kältespeichertemperatur über der Heizkreis-Sollvorlauftemperatur liegen.“

---

### Fund 11.2: Mindeststehzeit bis zum nächsten zulässigen Wärmepumpenstart & Zuschaltzeit-Sperre
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 74, Kap. 4.2 Tipps zur Störungsbehebung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Die Mindeststehzeit bis zum nächsten zulässigen Wärmepumpenstart ist noch nicht abgelaufen.
> Warten Sie 15 Minuten.
> Schalten Sie die Anlage aus und wieder ein.“
> „Heizbetrieb: Heizkreiszuschaltzeit nicht abgelaufen Warten Sie 15 Minuten.“

---

### Fund 11.3: Mindestlaufzeit des Kompressors bei PV- und Warmwasserbetrieb
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.ekoflam.at/Dokumentation/IDM-Navigator-Technische-Dokumentation.pdf
- **Lokale Datei:** quellen/IDM_Navigator_Technische_Dokumentation.pdf (Seite 22, Kap. 1 Photovoltaik - Stromnutzung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Im Heiz- bzw. Kühlbetrieb wird die Wärmepumpe, im Gegensatz zum Warmwasserbetrieb, nach Ablauf der Mindestlaufzeit des Kompressors abgeschaltet, wenn die verfügbare PV-Leistung unter die angeforderte PV-Leistung abfällt.“
> „Die Warmwasserladung wird beendet, wenn die PV-Leistung während der Warmwasserladung unter die angeforderte (notwendige) PV-Leistung abfällt und die Mindestlaufzeit überschritten ist.“

---

## 12. (Runde 10) Smart Grid Schaltzustände, EVU-Sperre & EVU-Zeitprogramm (iDM Navigator 2.0)

### Fund 12.1: Smart Grid Digitaleingänge und Schaltzustände der EVU-Sperre
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.ekoflam.at/Dokumentation/IDM-Navigator-Technische-Dokumentation.pdf
- **Lokale Datei:** quellen/IDM_Navigator_Technische_Dokumentation.pdf (Seite 25, Kap. 3.1)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Die Kommunikation von Tarifsignalen zur NAVIGATOR-Regelung 2.0 erfolgt über zwei Digitaleingänge (Variabler Eingang und EVU-Sperre). Für die Kommunikation wird eine wichtige Netzkomponente ein Smart Meter (intelligenter Stromzähler) benötigt.“
> „Smart Grid Stromampel Variabler Eingang Eingang EVU-Sperre
> Hoher Stromtarif Rot 0 1
> Normaler Stromtarif Gelb 0 0
> Niedriger Stromtarif Grün 1 0
> „Kostenloser“ Strom Supergrün 1 1
> Mit diesen zwei Digitaleingängen können dem NAVIGATOR 2.0 vier Schaltzustände vorgegeben werden:“
> „Der Anschluss erfolgt an der Klemme 118/119 bzw. 112/113 der NAVIGATOR-Regelung 2.0.“

### Fund 12.2: Sperrzeit-Einstellung über EVU-Zeitprogramm
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 50, Kap. 2.8.8 Smart Grid)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Im Menü „Smart Grid“ kann das Einschaltverhalten der Wärmepumpe beeinflusst werden.“
> „Unter „EVU-Programm“ kann ein Zeitprogramm eingestellt werden, wo der Wärmepumpenbetrieb gesperrt wird.“
> „Die Sperrzeit kann mittels einem Zeitprogramm hinterlegt werden.“
> „Die Zeiten können durch Anwahl des Zeitbereichs hinterlegt werden.“

---

## 13. (Runde 11) Pumpennachlauf- & Mischerlaufzeiten (TopTronic E AVR) & Zuschaltverzögerungen

### Fund 13.1: Nachlaufzeit der Primär-/Anlagenpumpe AVP und Mischerlaufzeit YAV
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 96, Parameter 06-065 & 06-066)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „06-065 Nachlaufzeit Pumpe AVP 5 min 0,5 99,0 Im Nachlauf bleibt die Pumpe eingeschaltet und der Mischer mit dem letzten Sollwert weiter geregelt. Nach dem Nachlauf wird Pumpe ausgeschaltet, der Mischer wird während der doppelten Mischerlaufzeit zugefahren.“
> „06-066 Laufzeit Mischer YAV 120 sec 0,0 6000,0 Laufzeit des Ventiles in Sekunden. Die Laufzeit muss für die Ventilberechnung exakt eingestellt werden.“

### Fund 13.2: Nachlaufzeit Warmwasserladung und Umschaltventil-Vorlaufzeit
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 155, Parameter 05-003 & 05-019)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „05-003 Nachlaufzeit WW-Ladung [0 min, Bereich 0–60]: Nach Erreichen der Solltemperatur läuft die WW Ladung um die hier eingestellte Zeit nach.“
> „05-019 Vorlaufzeit WW-Umschaltventil“

---

## 14. (Runde 12) Maximale Warmwasser-Ladedauer, Unterbrechungspause & Pumpennachlaufzeiten (TopTronic E)

### Fund 14.1: Maximale Warmwasser-Ladedauer & Zwangspause bei Zeitüberschreitung
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 156, Parameter 05-081 & 05-083)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „05-081 Maximale Warmwasser Ladedauer 1,0 h 0,0 10,0 Wird die eingestellte Maximalladedauer überschritten, wird der Ladevorgang unterbrochen und erst wieder gestartet, wenn die Einschaldifferenz (05-00) zur aktuellen Warmwassertemperatur unterschritten wird.“
> „05-083 Unterbrechung Warmwasserladung 0,2h 0,0 10,0 Unterbrechung Warmwasserladung“

### Fund 14.2: Nachlaufzeit der Warmwasser-Ladepumpen SLP1 und Brauchwasserpumpe SLP2
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 156, Parameter 05-008 & 05-009)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „05-008 Nachlaufzeit WW_Ladepumpe 60sec 0 600 Nachlaufzeit der WW-Ladepumpe (SLP1)“
> „05-009 Nachlaufzeit Brauchwasserpumpe BWP 60sec 0 600 Nachlaufzeit der Brauchwasserpumpe (SLP2)“

---

## 15. (Runde 13) TopTronic E Zeitverzögerungen für Temperaturwächter & Störmeldeausgänge

### Fund 15.1: Verzögerungszeiten für Vorlauftemperaturwächter & Raumüberwachung (07-048 & 07-114)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 139–140, Parameter 07-048 & 07-114)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „07-048 Verzögerungszeit VL-Temp. Wächter 1 min 0,0 30,0 Verzögerungszeit Blockierungsmeldung B1 VL-Temp. Wächter“
> „07-114 Meldung Raum Verzögerung 120min 0 1440 Einstellmöglichkeit der Verzögerungszeit. Bei Wert „0“ ist die Überprüfung deaktivert.“

### Fund 15.2: Auslöseverzögerungszeiten für Sammelstörmelde-Ausgang und externen Eingang (04-017 & 04-018)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 91, Parameter 04-017 & 04-018)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „04-017 Verzögerung Ausgang Sammelstörung 1,0 min 0,0 60,0 Verzögerungzeit Auslösen Ausgang Sammelstörung“
> „04-018 Verzögerung Eingang externe Störmeldung 0,2 min 0,0 60,0“

---

## 16. (Runde 14) TopTronic E Startoptimierungs-Vorhaltezeit, Temperatur-Zeitkonstanten & Pumpennachlauf

### Fund 16.1: Startoptimierungs-Vorhaltezeit & Zeitkonstanten für Außentemperatur- und Raumdämpfung (03-006, 03-019, 03-020, 03-024)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 137, Kap. Heizkreis.. – Parameter)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „03-006 Startoptimierung Vorhaltezeit 90 min 0,0 900,0 Damit kann eine Vorverschiebung des Einschaltzeitpunkts im Automatikbetrieb erreicht werden. Die Vorhaltezeit gibt die Aufheizzeit an, die nötig ist um die Raumtemperatur um 5 K bei -10 °C Aussentemperatur anzuheben. Die Zeit wird automatisch bei ändernden Aussentemperaturen korrigiert.“
> „03-019 Zeitkonstante für Aussentemp. MW-Ber. HK-Grenze 0h 0 24,0 Zeitkonstante zur Berechnung des Aussentempearaturmittelwertes (für Heizgrenze)“
> „03-020 Zeitkonstante für Aussentemp. MW-Ber. 2 h 0 50 Zeitkonstante zur Berechnung des Aussentempearaturmittelwertes (für Heizkurve): Schwere Bauweise 20 - 30 h Mittlere Bauweise 10 - 15 h“
> „03-024 Zeitkonstante für Raumtemp. MW-Ber. 10 min 0 60 Mit dieser Zeitkonstante wird die Dämpfung der Raumtemperatur für die Raumheizgrenze eingestellt: 0 min = direkte Heizgrenzenfunktion > 20 min = Verzögerte Heizgrenzenfunktion“

### Fund 16.2: Heizkreis-Pumpennachlauf & Fehlerdauer für Vorlauftemperatur-Störung (07-003 & 07-006)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 139, Kap. Heizkreis.. – Konfiguration)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „07-003 Pumpennachlauf 0 min 0,0 30,0 Nach Abschaltung des Heizbetriebs bleibt die Mischerregelung für die eingestellte Zeit in Betrieb. Danach schliesst der Mischer und nach einem weiteren Ablauf der Zeit schalten Mischer und Pumpenausgänge ab.“
> „07-006 Fehlerdauer Vorlauf Störung 0,2 h 0,0 20,0 Unterschreitet die Vorlauftemperatur den Sollwert um mehr als die Abweichung (07-007) und ist die Fehlerdauer überschritten, wird die Störung 1016 generiert.“

---

## 17. (Runde 15) TopTronic E Raumheizgrenzen (forciert Heizen / Heizen aus) & Nachstellzeit des Raumreglers

### Fund 17.1: Einschaltheizgrenze forciert & Ausschaltheizgrenze mit Schaltdifferenzen (03-025 & 03-026)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 137 & 147, Kap. 10.2.8 Heiz- und Kühlgrenzen)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „03-025 Abweichung forciert Heizen 0 K 0,0 10,0 Mit diesem Parameter kann die Abweichung zur Soll Raumtemperatur für forcierten Heizbetrieb eingestellt werden.“
> „03-026 Abweichung Heizen aus 0 K 0,0 10,0 Mit diesem Parameter kann die Abweichung zur Soll Raumtemperatur für die Abschaltung des Heizbetriebs eingestellt werden.“
> „Für die Raumtemperatur Heizgrenzen wird ein Raumtemperatur-Mittelwert mit einer Zeitkonstante von 0.5 Stunden gebildet.“
> „Die Abweichung für „forciert Heizen“ zum Heizsollwert kann mit der Einschaltheizgrenze (03-025) eingestellt werden. Die dazugehörende Schaltdifferenz für „forciert Heizen“ aus entspricht der Hälfte der Einschaltheizgrenze.“
> „Die Abweichung für „Heizen aus“ zum Heizsollwert kann mit der Ausschaltheizgrenze (03-026) eingestellt werden. Die dazugehörende Schaltdifferenz für „Heizen frei“ entspricht der Hälfte der Ausschaltheizgrenze.“

### Fund 17.2: Nachstellzeit des Raumreglers zur Kompensation von Proportionalfehlern (03-030)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 137, Kap. Heizkreis.. – Parameter)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „03-030 Nachstellzeit Raumregler 1,5 min 0,0 200,0 Falls der Heizkreis raumgeführt geregelt wird, kann hiermit eine Nachstellzeit eingestellt werden. Die Nachstellzeit bewirkt, dass ein Proportionalfehler auf Grund der Raumkompensation ausgeglichen wird.“

---

## 18. (Runde 16) TopTronic E Außentemperatur-Heizgrenze/Dämpfung & Navigator 2.0 Mindeststehzeit/Zuschaltzeit

### Fund 18.1: TopTronic E Außentemperatur-Heizgrenze (03-021), Zeitkonstante (03-019), 0,5 K Schaltdifferenz & Frostschutz unter 2 °C
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 144, Kap. 10.2.7 Aussentemperatur Heizgrenze)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „10.2.7 Aussentemperatur Heizgrenze
> (Die Einstellung der Heizgrenze)
> (03-021) bestimmt wann die Heizkreisregelung abgeschaltet wird. Für die Heizgrenzenabschaltung wird ein gewichteter Aussentemperaturwert berechnet. Die Zeitkonstante (03-019) kann bei Bedarf eingestellt werden.“
> „Mit der Einstellung wird die Heizgrenze für eine Basis - Raumtemperatur von 20 °C bestimmt. Wenn die mittlere Aussentemperatur den Wert übersteigt, schaltet die Heizung aus, sinkt die mittlere Aussentemperatur 0.5K unter den eingestellten Wert, schaltet die Heizung wieder ein. Wird der Wert unter 2 °C eingestellt, ist Frostschutz aktiviert.“
> „Wird die Soll Raumtemperatur durch Betriebswahl oder Behaglichkeit verstellt, schiebt sich die Heizgrenze automatisch mit. Die Differenz zwischen Raum Solltemperatur und Heizgrenze (03-021) bleibt bestehen.“

### Fund 18.2: iDM Navigator 2.0 Zuschaltzeit Heizen (1–240 min) & 15-Minuten-Mindeststehzeit
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 39, Kap. 2.8.4 & Seite 74, Kap. 4.2)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Zuschaltzeit Heizen (15 min)
> Nach Ablauf der Zuschaltzeit (1 - 240 min) wird die Heizanforderung an die Wärmepumpe weiter gegeben, wenn die Heizkreis-Istvorlauftemperatur und die Wärmespeichertemperatur unter der Heizkreis-Sollvorlauftemperatur liegen.“
> „Die Mindeststehzeit bis zum nächsten zulässigen Wärmepumpenstart ist noch nicht abgelaufen. Warten Sie 15 Minuten. Schalten Sie die Anlage aus und wieder ein.“
> „Heizbetrieb: Heizkreiszuschaltzeit nicht abgelaufen: Warten Sie 15 Minuten.“

---

## 19. (Runde 17) TopTronic E Aufheizoptimierungs-Vorhaltezeit & Navigator 2.0 SmartGrid EVU-Sperrzeitprogramm

### Fund 19.1: TopTronic E Aufheizoptimierung / Vorhaltezeit (03-006) für Fußboden- und Radiatorsysteme
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 143, Kap. 10.2.6 Aufheizoptimierung)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „10.2.6 Aufheizoptimierung
> Der Raumtemperatur-Sollwert wird abhängig von der Vorhaltezeit (03-006) vor dem programmierten Schaltpunkt Auf-
> heizen auf Normaltemperatur gesetzt. Die Vorhaltezeit Aufheizen gibt die Aufheizzeit für die Raumtemperatur um 5 K 
> bei -10 °C Aussentemperatur an. Für träge Fussbodensysteme liegt diese bei ~200 bis 400 Minuten. Für Radiatorsys-
> teme dementsprechend bei 100 bis 200 Minuten. Die wirksame aktuelle Vorhaltezeit errechnet sich aus der Aussen-
> temperatur und der Raumtemperaturabweichung. Ist keine Raumtemperatur aktiv, wird nur nach Aussentemperatur 
> gerechnet“

### Fund 19.2: iDM Navigator 2.0 Smart Grid EVU-Sperrzeitprogramm & Einschaltbeeinflussung
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 50, Kap. 2.8.8 Smart Grid)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „2.8.8. Smart Grid
> Im Menü „Smart Grid“ kann das Einschaltverhalten der Wärmepumpe beeinﬂ usst werden.
> Unter „EVU-Programm“ kann ein Zeitprogramm eingestellt werden, wo der Wärmepumpenbetrieb gesperrt wird.
> Die Sperrzeit kann mittels einem Zeitprogramm hinterlegt werden.
> Die Zeiten können durch Anwahl des Zeitbereichs hinterlegt werden.“

---

## 20. (Runde 18) Hoval Pufferspeicher-Taktvermeidung/Sperrzeiten & Navigator 2.0 Kompressor-Mindestlaufzeiten

### Fund 20.1: Hoval Energiepufferspeicher zur Taktvermeidung, Mindestlaufzeiten & EVU-Sperrzeit-Auslegung
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/user_upload/Hoval_UltraSource_B_Technikhandbuch.pdf
- **Lokale Datei:** quellen/Hoval_UltraSource_B_Technikhandbuch.pdf (Seite 37 & 39, Kap. Energiepufferspeicher & EVU-Sperrzeiten)
- **Datum der Quelle:** 2026/27
- **Wörtliches Zitat:**
> „Ein Energiepufferspeicher sorgt für optimale Betriebsbedingungen der Wärmepumpe.
> • Hydraulische Entkoppelung der unterschiedlichen Volumenströme von Wärmepumpe und Wärmeverteilsystem (Heizung)
> • Nimmt die Leistungsüberschüsse der Wärmepumpe auf und reduziert die Einschaltschalthäufigkeit (Takten)
> • Ermöglicht den Anschluss mehrerer Heizkreise“
> „Für Hoval Wärmepumpen müssen nachfolgende Mindestgrössen der Energiepufferspeicher (EnerVal) eingehalten werden. Dabei sind die Mindestlaufzeiten der Wärmepumpen berücksichtigt.“
> „EVU-Sperrzeiten Falls vom EVU (Energieversorgungsunternehmen) die Stromversorgung für die Wärmepumpe zeitweise gesperrt wird (z. B. wegen Sondertarifen), so muss dies in der Auslegung der Wärmepumpe berücksichtigt werden. Die Tageswärmemenge muss dann in der Zeit, wo Strom zur Verfügung steht, eingebracht werden. Die Wärmepumpe muss auf die maximale Sperrzeit, laut Energieliefervertrag, ausgelegt werden.“

### Fund 20.2: iDM Navigator 2.0 Kompressor-Mindestlaufzeit bei Heizen/Kühlen/WW & Fußboden-Überhöhung
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.ekoflam.at/Dokumentation/IDM-Navigator-Technische-Dokumentation.pdf
- **Lokale Datei:** quellen/IDM_Navigator_Technische_Dokumentation.pdf (Seite 22, Kap. 1 Photovoltaik - Stromnutzung)
- **Datum der Quelle:** 2021
- **Wörtliches Zitat:**
> „Im Heiz- bzw. Kühlbetrieb wird die Wärmepumpe, im Gegensatz zum Warmwasserbetrieb, nach Ablauf der Mindestlaufzeit des Kompressors abgeschaltet, wenn die verfügbare PV-Leistung unter die angeforderte PV-Leistung abfällt.“
> „Die Warmwasserladung wird beendet, wenn die PV-Leistung während der Warmwasserladung unter die angeforderte (notwendige) PV-Leistung abfällt und die Mindestlaufzeit überschritten ist.“
> „Mit diesem Parameter kann bei entsprechender Temperatureinstellung zusätzlich Energie in der Fußbodenheizung gespeichert werden. Der Parameter gibt an, um welchen Wert (0.0 - 6.0 K) die Fußbodenheizung überhöht werden soll. Voraussetzung ist, dass sich das System im Heizbetrieb beﬁ ndet, d.h. die Heizgrenze unterschritten ist.“

---

## 21. (Runde 19) TopTronic E Außentemperatur-Zeitkonstanten & Navigator 2.0 Mindeststehzeit / Zuschaltzeiten

### Fund 21.1: TopTronic E Zeitkonstanten für Außentemperatur-Mittelwertbildung (03-019 Heizgrenze, 03-020 Heizkurve, 03-033 Gewichtung)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 116–117, Kap. 10.1.11 Aussentemperatur / Mittelwert)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „Mit dem Einsteller 03-019 „Zeitkonstante für Aussentemp. MW-Ber. HK- Grenze“ wird der gewichtete Mittelwert zeitlich gemittelt und somit die Aussentemperatur Heizkreis (00-000) festgelegt.“
> „Mit dem Einsteller 03-020 „Zeitkonstante für Aussentemp. MW-Ber.“ wird der gewichtete Mittelwert zeitlich gemittelt.“
> „Für die Bestimmung der Vorlauftemperatur über die Heizkennlinie, werden die gemittelte Aussentemperatur Heizkreis und der gemittelte Langzeitwert zu gleichen Teilen gemittelt verwendet: AT-HK = (ATgmW + AT-Mittel) / 2“
> „Für die Bestimmung der Heizgrenzen wird die Aussentemperatur Heizkreis (AT-HK) verwendet.“

### Fund 21.2: iDM Navigator 2.0 Mindeststehzeit (15 min) & Zuschaltzeit Heizen/Kühlen zur Taktvermeidung
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 39 & 74, Kap. 2.8.2 Heizkreiseinstellungen & 4.2 Tipps zur Störungsbehebung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Die Mindeststehzeit bis zum nächsten zulässigen Wärmepumpenstart ist noch nicht abgelaufen. • Warten Sie 15 Minuten. • Schalten Sie die Anlage aus und wieder ein.“
> „Heizbetrieb: Heizkreiszuschaltzeit nicht abgelaufen Warten Sie 15 Minuten.“
> „Zuschaltzeit Heizen (15 min) Nach Ablauf der Zuschaltzeit (1 - 240 min) wird die Heizanforderung an die Wärmepumpe weiter gegeben, wenn die Heizkreis-Istvorlauftemperatur und die Wärmespeichertemperatur unter der Heizkreis-Sollvorlauftemperatur liegen.“
> „Zuschaltzeit Kühlen (15 min) Nach Ablauf der Zuschaltzeit (1 - 240 min) wird die Kühlanforderung an die Wärmepumpe weiter gegeben, wenn die Heizkreis-Istvorlauftemperatur und die Kältespeichertemperatur über der Heizkreis-Sollvorlauftemperatur liegen.“

---

## 22. (Runde 20) TopTronic E Heizgrenzen-Schalthysterese / Mitführung & Navigator 2.0 PV-Mittelwertbildung / Leistungsprognose

### Fund 22.1: TopTronic E Heizgrenzenabschaltung mit 0,5 K Hysterese, Raumsolltemperatur-Mitführung & Vorlaufsollwert-Abschaltung (03-021, 03-002, 03-008)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 144–145, Kap. 10.2.7 Aussentemperatur Heizgrenze & Kap. 10.2.9 Sonderheizgrenzen)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „(03-021) bestimmt wann die Heizkreisregelung abgeschaltet wird. Für die Heizgrenzenabschaltung wird ein gewichteter Aussentemperaturwert berechnet. Die Zeitkonstante (03-019) kann bei Bedarf eingestellt werden.“
> „Mit der Einstellung wird die Heizgrenze für eine Basis - Raumtemperatur von 20 °C bestimmt. Wenn die mittlere Aussentemperatur den Wert übersteigt, schaltet die Heizung aus, sinkt die mittlere Aussentemperatur 0.5K unter den eingestellten Wert, schaltet die Heizung wieder ein. Wird der Wert unter 2 °C eingestellt, ist Frostschutz aktiviert.“
> „Wird die Soll Raumtemperatur durch Betriebswahl oder Behaglichkeit verstellt, schiebt sich die Heizgrenze automatisch mit. Die Differenz zwischen Raum Solltemperatur und Heizgrenze (03-021) bleibt bestehen.“
> „Eine weitere Heizgrenze wird abgeleitet aus dem Vorlauftemperatur-Sollwert. Sinkt der Sollwert unter den Einstellwert unter die aktuelle Raum Solltemperatur plus Vorlaufsollwert Heizgrenze (03-008), schaltet der Heizbetrieb aus. D. h. wenn der Vorlaufsollwert auf Grund einer hohen aktuellen Aussentemperatur sinkt und unter die eingestellte Schwelle sinkt, schaltet die Heizung aus, obwohl die Heizgrenzenabschaltung noch nicht erreicht ist. Steigt der Sollwert wieder um 2 K an, geht die Heizungsregelung wieder in Betrieb.“

### Fund 22.2: iDM Navigator 2.0 PV-Mittelwert-Zeitkonstante (PV 011), Verbrauchsoffset & Leistungsaufnahme-Prognose im Stillstand
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.ekoflam.at/Dokumentation/IDM-Navigator-Technische-Dokumentation.pdf
- **Lokale Datei:** quellen/IDM_Navigator_Technische_Dokumentation.pdf (Seite 21 & 23, Kap. 1 Photovoltaik - Stromnutzung)
- **Datum der Quelle:** 2021
- **Wörtliches Zitat:**
> „PV 011 Zeitkonstante Mittelwert [2 min] Dieser Parameter gibt den Zeitintervall (0.1 - 360 min) für die Mittelwertbildung der PV-Leistung an.“
> „PV 015 PV-Verbrauchsoffset Mit diesem Parameter kann der Wert der „momentan / prognostizierten Leistungsaufnahme“ erhöht bzw. verringert werden und somit das Einschalten der Wärmepumpe mit PV-Stromnutzung beeinflusst werden.“
> „Bei der Berechnung der prognostizierten Aufnahmeleistung (bei Stillstand der Wärmepumpe) fließen die Außentemperatur, die Wärmespeichertemperatur / Wärmepumpenrücklauftemperatur, die min. Drehzahl und die TWW-Erwärmer-Maximaltemperatur mit ein.“

---

## 23. (Runde 21) TopTronic E Heizkreis-Standschutz & Mischerregelung sowie Navigator 2.0 Mindestlaufzeit bei PV-Abschaltung

### Fund 23.1: TopTronic E Standschutz für Heizkreispumpe und Mischer sowie PI-Mischerdynamik (07-016, 07-020, 07-021, 07-022)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 139 & 148, Kap. 10.2.17 Mischerregelung & Kap. 10.2.19 Standschutz)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „Um das Festsitzen der Pumpe zu verhindern, wird im Ausbetrieb täglich ein Standschutzzyklus eingeschaltet. Die Pumpe schaltet jeweils um 12:00 mittags für 30 Sekunden ein. Der Mischer öffnet jeweils um 12:00 mittags für 10 Sekunden und schliesst danach für 20 Sekunden.“
> „Die Mischerregelung erfolgt über einen PI-Regler (proportional–integral controller). Ein PI-Regler besteht aus 2 Teilen, einem P-Anteil und einem I-Anteil. Dieser hat somit den Vorteil des P-Reglers, nämlich schnelle Reaktion, mit dem Vorteil des I-Reglers, der exakten Ausregelung. Der PI-Regelkreis ist somit genau und schnell. Für den P- Anteil kann das P-Band (07-021), den I-Anteil die Nachstellzeit (07-020) und für das Abtastintervall die Laufzeit (07-022 Laufzeit Regler) je Regelkreis eingestellt werden.“
> „Laufzeit des Mischer-Regelkreises. Beispiel: Die Laufzeit des Motors beträgt 120 Sekunden. Der eingestellte Wert 30 ist dann ¼ der gesamten Laufzeit, somit wird die Berechnung alle 30 Sekunden durchgeführt. Der eingestellte Wert sollte üblicherweise immer ¼ der Gesamtlaufzeit betragen.“

### Fund 23.2: Navigator 2.0 PV-Leistungsabschaltung nach Kompressor-Mindestlaufzeit & Nenndrehzahl-Voraussetzung
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.ekoflam.at/Dokumentation/IDM-Navigator-Technische-Dokumentation.pdf
- **Lokale Datei:** quellen/IDM_Navigator_Technische_Dokumentation.pdf (Seite 18 & 22, Kap. 2.3 Prioritäten & Kap. 2.5 Einstellungen)
- **Datum der Quelle:** 2021
- **Wörtliches Zitat:**
> „Der Parameter „PV Leistung“ zeigt die zuvor angegebenen PV- und Wärmepumpenleistungen an. Nach Übermittlung des Signals vom Wechselrichter bzw. Energieverbrauchsregler an die NAVIGATOR-Regelung 2.0 startet die Wärmepumpe. Im Heiz- bzw. Kühlbetrieb wird die Wärmepumpe, im Gegensatz zum Warmwasserbetrieb, nach Ablauf der Mindestlaufzeit des Kompressors abgeschaltet, wenn die verfügbare PV-Leistung unter die angeforderte PV-Leistung abfällt.“
> „Wenn dieser Parameter auf „Ja“ eingestellt ist, dann wird der Trinkwarmwasserspeicher mit PV-Strom geladen. Dies geschieht unabhängig von der Einstellung des Warmwasserzeitprogrammes. Die Warmwasserladung wird beendet, wenn die PV-Leistung während der Warmwasserladung unter die angeforderte (notwendige) PV-Leistung abfällt und die Mindestlaufzeit überschritten ist.“
> „Damit die Wärmepumpe die Warmwasserbereitung durchführen kann, muss diese zumindest mit Nenndrehzahl betrieben werden. Die entsprechende Leistungsaufnahme der Wärmepumpe bei Nenndrehzahl kann den Leistungsdaten entnommen werden.“

---

## 24. (Runde 22) TopTronic E Aufheizoptimierung / Vorhaltezeiten & iDM Smart Grid 4-Zustands-Tarifsteuerung

### Fund 24.1: TopTronic E Aufheizoptimierung & Vorhaltezeit für Fußboden- vs. Radiatorsysteme (03-006)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 137 & 143, Kap. 10.2.6 Aufheizoptimierung & Kap. Heizkreis.. – Parameter)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „Der Raumtemperatur-Sollwert wird abhängig von der Vorhaltezeit (03-006) vor dem programmierten Schaltpunkt Aufheizen auf Normaltemperatur gesetzt. Die Vorhaltezeit Aufheizen gibt die Aufheizzeit für die Raumtemperatur um 5 K bei -10 °C Aussentemperatur an. Für träge Fussbodensysteme liegt diese bei ~200 bis 400 Minuten. Für Radiatorsysteme dementsprechend bei 100 bis 200 Minuten. Die wirksame aktuelle Vorhaltezeit errechnet sich aus der Aussentemperatur und der Raumtemperaturabweichung. Ist keine Raumtemperatur aktiv, wird nur nach Aussentemperatur gerechnet“
> „Damit kann eine Vorverschiebung des Einschaltzeitpunkts im Automatikbetrieb erreicht werden. Die Vorhaltezeit gibt die Aufheizzeit an, die nötig ist um die Raumtemperatur um 5 K bei -10 °C Aussentemperatur anzuheben. Die Zeit wird automatisch bei ändernden Aussentemperaturen korrigiert. Erfahrungswerte: Fussbodenheizung = 210 min Radiatoren = 150 min 0 = ausser Funktion.“

### Fund 24.2: iDM Smart Grid 4-Zustands-Matrix über EVU-Sperre & Variabler Eingang sowie Lastverschiebung
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.ekoflam.at/Dokumentation/IDM-Navigator-Technische-Dokumentation.pdf
- **Lokale Datei:** quellen/IDM_Navigator_Technische_Dokumentation.pdf (Seite 25–26, Kap. 3.1 Tarifsignal & Kap. 3.2 Stundenvariable Stromtarife)
- **Datum der Quelle:** 2021
- **Wörtliches Zitat:**
> „Die Kommunikation von Tarifsignalen zur NAVIGATOR-Regelung 2.0 erfolgt über zwei Digitaleingänge (Variabler Eingang und EVU-Sperre).“
> „Mit diesen zwei Digitaleingängen können dem NAVIGATOR 2.0 vier Schaltzustände vorgegeben werden: Smart Grid: Hoher Stromtarif | Stromampel: Rot | Variabler Eingang: 0 | Eingang EVU-Sperre: 1 Normaler Stromtarif | Stromampel: Gelb | Variabler Eingang: 0 | Eingang EVU-Sperre: 0 Niedriger Stromtarif | Stromampel: Grün | Variabler Eingang: 1 | Eingang EVU-Sperre: 0 „Kostenloser“ Strom | Stromampel: Supergrün | Variabler Eingang: 1 | Eingang EVU-Sperre: 1“
> „Wenn der Strompreis niedrig ist, dann überhöht die NAVIGATOR-Regelung 2.0 die Temperatur im Wärmespeicher (thermische Speicherung). Aufgrund der thermischen Speicherung kann die Wärmepumpe bei hohen Stromtarifen im Absenkbetrieb laufen und dadurch Energiekosten sparen.“

---

## 25. (Runde 23) TopTronic E Leistungsbegrenzung & Navigator 2.0 EVU-Sperrzeitenprogramm

### Fund 25.1: TopTronic E Leistungsbegrenzungs-Dynamik über M-Bus Zähler (00-099, 01-208, 01-209)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 125–126, Kap. 10.1.20 Leistungsbegrenzung)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „Zusätzlich zur hydraulischen Begrenzung der Abnahmemenge, wird durch den Regler ein Vergleich der aktuellen Leistung zur maximal zulässigen Leistung der Anlage durchgeführt. Die Regelung erfolgt wie bei der Rücklaufbegrenzung durch Absenken der Solltemperatur. Ist die Leistungsbegrenzung aktiv, so wird das in der Serviceebene Parameter 00-099 angezeigt.“
> „01-208 Maximalleistung 100kW 0 10000 Angabe des zulässigen Wärmebezuges. Übersteigt der momentane Verbrauch, der durch den/die Wärmezähler gemessen wird, diesen Wert, so wird die Solltemperatur und damit die Vorlauftemperatur des Sekundärkreises gesenkt.“
> „01-209 Leistungsbegrenzung P-Faktor 10% 0 100 Gibt an, wieviel eine 100%ige Leistungsüberschreitung die Vorlauftemperatur pro Berechnungsschritt absenkt.“
> „Diese Berechnung und somit Leistungsreduzierung wird laufend wiederholt, bis die Leistung stabil bei der Maximalleistung von 10kW liegt. Bei einer Unterschreitung der Maximalleistung von 10kW, wird die Begrenzung wieder schrittweise auf dieselbe Art und Weise aufgehoben und stufenweise erhöht.“

### Fund 25.2: Navigator 2.0 Zeitprogramm EVU-Sperre (Sperrzeiten für Wärmepumpenbetrieb)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 50, Kap. 2.8.8 Smart Grid)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Im Menü „Smart Grid“ kann das Einschaltverhalten der Wärmepumpe beeinflusst werden.“
> „Unter „EVU-Programm“ kann ein Zeitprogramm eingestellt werden, wo der Wärmepumpenbetrieb gesperrt wird.“
> „Die Sperrzeit kann mittels einem Zeitprogramm hinterlegt werden. Die Zeiten können durch Anwahl des Zeitbereichs hinterlegt werden.“

---

## 26. (Runde 24) Hoval Pufferspeicher-Mindestgrößen / Mindestlaufzeiten & iDM Inverter-Modulation gegen Takten

### Fund 26.1: Hoval Pufferspeicher-Mindestgrößen zur Vermeidung von Takten unter Berücksichtigung von Mindestlaufzeiten & EVU-Sperrzeiten
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.hoval.ch/de_CH/medias/sys_master/celum_assets/4219416_UltraSource-B-Katalog_de.pdf
- **Lokale Datei:** quellen/hoval_US-B-cf-cp_Katalog.pdf (Seite 36–38, Kap. Projektierung Wärmepumpen Allgemein)
- **Datum der Quelle:** 2026
- **Wörtliches Zitat:**
> „Ein Energiepufferspeicher sorgt für optimale Betriebsbedingungen der Wärmepumpe.“
> „Nimmt die Leistungsüberschüsse der Wärmepumpe auf und reduziert die Einschaltschalthäufigkeit (Takten)“
> „Für Hoval Wärmepumpen müssen nachfolgende Mindestgrössen der Energiepufferspeicher (EnerVal) eingehalten werden. Dabei sind die Mindestlaufzeiten der Wärmepumpen berücksichtigt. Für Luft/Wasser-Wärmepumpen ist die notwendige Energie für die Abtauung der Wärmepumpe eingerechnet. Die Volumina für EVU-Sperrzeiten sind nach lokalen Vorschriften projektbezogen zu addieren.“
> „UltraSource® B comfort C (17) 300“
> „Falls vom EVU (Energieversorgungsunternehmen) die Stromversorgung für die Wärmepumpe zeitweise gesperrt wird (z. B. wegen Sondertarifen), so muss dies in der Auslegung der Wärmepumpe berücksichtigt werden. Die Tageswärmemenge muss dann in der Zeit, wo Strom zur Verfügung steht, eingebracht werden. Die Wärmepumpe muss auf die maximale Sperrzeit, laut Energieliefervertrag, ausgelegt werden.“

### Fund 26.2: iDM Inverter-Drehzahlregelung zur Taktvermeidung & Pufferspeicherausnutzung für längere Laufzeiten
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.siblik.com/fileadmin/mam/medias/docus/115/IDM193512u13_522u523_AERO%20SLM%203-11.pdf
- **Lokale Datei:** quellen/IDM_AERO_SLM_3-11_Montageanleitung.pdf (Seite 44–45, Kap. 9 Anlagenschemen)
- **Datum der Quelle:** 2020
- **Wörtliches Zitat:**
> „Durch die Drehzahlregelung des Verdichters ist es auch beim Direktheizkreis möglich die benötigten Vorlauftemperaturen zu liefern. Durch die Invertertechnologie wird eine bedarfsgerechte Bereitstellung der Heizenergie ermöglicht. Das bedeutet, geringes Takten der Wärmepumpe und optimale Wärmeversorgung des Gebäudes.“
> „Der Hygienik dient zur Warmwasserbereitung und als Heizungspuffer. Der obere Speicherbereich wird bei Vorrangladung mit drehzahlgeregelter Ladepumpe mit der eingestellten HGL- Temperatur beladen. Auch im Heizbetrieb der Wärmepumpe wird über den HGL-Tauscher und das HGL-Ventil immer ein Teilstrom mit der eingestellten HGL-Temperatur in den oberen Speicherbereich geladen.“
> „Dadurch wird der Hygienik immer auf Temperatur gehalten, gleichzeitig wird der untere Speicherbereich als Puffer wegen der höheren Temperatur besser ausgenutzt, das bedeutet: - längere Laufzeiten der Wärmepumpe - längere Stillstandszeiten - mehr Warmwasser oder höhere Warmwassertemperatur“

---

## 27. (Runde 25) TopTronic E Heizkreis-Abschalthysterese (03-110, 03-111) & Hoval Scroll-Kompressor Modulationsband (C17)

### Fund 27.1: TopTronic E Heizkreisabschaltung bei geringer Anlagentemperatur & 2 K Wiedereinschaltdifferenz (03-110, 03-111)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 138 & 146, Kap. Heizkreis.. – Parameter & Kap. 10.2.10 Abschaltung bei zu geringer Anlagentemperatur)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „03-110 Minimale Anlagetemperatur 15 °C 1,0 90,0 Mit der Heizgrenze Anlagetemperatur kann eine Abschaltung des Heizkreises erreicht werden.Sinkt die Anlagetemperatur unter die berechnete Vorlauf Solltemperatur, wird die Heizung abgeschaltet. Steigt die Anlagetemperatur wieder um 2 K an, geht die Heizungsregelung wieder in Betrieb.“
> „03-111 Abschaltdifferenz Anlagetemperatur 0 K -100,0 30,0 Mit der Heizgrenze Anlagetemperatur Diffferenz kann eine Abschaltung des Heizkreises erreicht werden.Sinkt die Anlagetemperatur unter die berechnete Vorlauf Solltemperatur plus Einstellwert, wird die Heizung abgeschaltet. Steigt die Anlagetemperatur Differenz wieder um 2 K an, geht die Heizungsregelung wieder in Betrieb.“
> „(03-110) Minimale Anlagentemperatur Sinkt die Anlagentemperatur unter die berechnete Vorlauf-Solltemperatur wird die Heizung abgeschaltet. Steigt die Anlagentemperatur wieder um 2 K an, geht die Heizungsregelung wieder in Betrieb.“
> „(03-111) Abschaltdifferenz Anlagentemperatur Sinkt die Anlagentemperatur unter die berechnete Vorlauf-Solltemperatur plus Einstellwert, wird die Heizung abgeschaltet. Steigt die Anlagentemperatur-Differenz wieder um 2 K an, geht die Heizungsregelung wieder in Betrieb.“

### Fund 27.2: Hoval UltraSource B comfort C (17) modulierender Scroll-Kompressor & Teillast-Modulationsbereiche
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.hoval.ch/de_CH/medias/sys_master/celum_assets/4221940_UltraSource-B-Technikhandbuch_de.pdf
- **Lokale Datei:** quellen/Hoval_UltraSource_B_Technikhandbuch.pdf (Seite 5 & 7, Kap. Hoval UltraSource B comfort C (8-17) Technische Daten)
- **Datum der Quelle:** 2026
- **Wörtliches Zitat:**
> „UltraSource® B comfort C (11,17) mit modulierendem Scroll-Kompressor“
> „UltraSource® B comfort C (17) Heizleistung 1) A-7W35: 7.1-14.8 kW | A2W35: 7.4-17.4 kW | Kühlleistung 1) A35W18: 8.2-13.6 kW“
> „1) Modulationsbereich“
> „UltraSource® B comfort C (11) Heizleistung 1) A-7W35: 4.1-10.0 kW | A2W35: 4.1-10.2 kW | Kühlleistung 1) A35W18: 6.0-12.7 kW“

---

## 28. (Runde 26) TopTronic E Aufheiz-Vorhaltezeit / Pumpennachlauf & Navigator 2.0 Anforderungs-Zuschaltzeiten

### Fund 28.1: TopTronic E Startoptimierung Vorhaltezeit (03-006) & Pumpennachlauf Mischer/Heizkreis (07-003)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 137 & 139, Kap. Heizkreis.. – Parameter)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „03-006 Startoptimierung Vorhaltezeit 90 min 0,0 900,0 Damit kann eine Vorverschiebung des Einschaltzeitpunkts im Automatikbetrieb erreicht werden. Die Vorhaltezeit gibt die Aufheizzeit an, die nötig ist um die Raumtemperatur um 5 K bei -10 °C Aussentemperatur anzuheben. Die Zeit wird automatisch bei ändernden Aussentemperaturen korrigiert. Erfahrungswerte: Fussbodenheizung = 210 min Radiatoren = 150 min 0 = ausser Funktion.“
> „07-003 Pumpennachlauf 0 min 0,0 30,0 Nach Abschaltung des Heizbetriebs bleibt die Mischerregelung für die eingestellte Zeit in Betrieb. Danach schliesst der Mischer und nach einem weiteren Ablauf der Zeit schalten Mischer und Pumpenausgänge ab.“

### Fund 28.2: Navigator 2.0 Zuschaltzeit Heizen & Kühlen (1–240 min)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 39, Kap. 2. Bedienung – Heizkreiseinstellungen)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „Zuschaltzeit Heizen (15 min) Nach Ablauf der Zuschaltzeit (1 - 240 min) wird die Heizanforderung an die Wärmepumpe weiter gegeben, wenn die Heizkreis-Istvorlauftemperatur und die Wärmespeichertemperatur unter der Heizkreis-Sollvorlauftemperatur liegen.“
> „Zuschaltzeit Kühlen (15 min) Nach Ablauf der Zuschaltzeit (1 - 240 min) wird die Kühlanforderung an die Wärmepumpe weiter gegeben, wenn die Heizkreis-Istvorlauftemperatur und die Kältespeichertemperatur über der Heizkreis-Sollvorlauftemperatur liegen.“

---

## 29. (Runde 27) TopTronic E Pumpenregelung/Nachlauf (10.2.16) / Standschutz & Navigator 2.0 Mindeststehzeit (15 min)

### Fund 29.1: TopTronic E Umwälzpumpen-Dauerlauf im Heizbetrieb, Mischer-Nachlaufzeit (07-003) & täglicher Standschutzzyklus
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 148, Kap. 10.2.16 Pumpenregelung & Kap. 10.2.17 Mischerregelung)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „10.2.16 Pumpenregelung Die Umwälzpumpe läuft im Heizbetrieb immer. Nach Abschalten des Heizbetriebs läuft die Mischerregelung noch um die eingestellte Nachlaufzeit (07-003) nach.“
> „Um das Festsitzen der Pumpe zu verhindern, wird im Ausbetrieb täglich ein Standschutzzyklus eingeschaltet. Die Pumpe schaltet jeweils um 12:00 mittags für 30 Sekunden ein. Der Mischer öffnet jeweils um 12:00 mittags für 10 Sekunden und schliesst danach für 20 Sekunden.“

### Fund 29.2: Navigator 2.0 Mindeststehzeit (15 min Schutzpause vor Verdichterstart) & Heizkreiszuschaltzeit
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
- **Lokale Datei:** quellen/IDM_Navigator_2.0_Bedienungsanleitung.pdf (Seite 74, Kap. 4.2 Tipps zur Störungsbehebung)
- **Datum der Quelle:** 2019
- **Wörtliches Zitat:**
> „4.2. Tipps zur Störungsbehebung“
> „Die Mindeststehzeit bis zum nächsten zulässigen Wärmepumpenstart ist noch nicht abgelaufen. • Warten Sie 15 Minuten. • Schalten Sie die Anlage aus und wieder ein.“
> „Heizbetrieb: Heizkreiszuschaltzeit nicht abgelaufen Warten Sie 15 Minuten.“














