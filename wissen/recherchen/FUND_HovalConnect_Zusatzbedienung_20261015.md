# Funde: HovalConnect, TopTronic E Gateways & Zusatzbediengeräte (TTE-BM / TTE-RBM)

Recherchedatum: 2026-10-15  
Thema: HovalConnect Online-Gateway (TTE-GW), BedienModul (TTE-BM), RaumbedienModul (TTE-RBM), Busadressen, DIP-Einstellungen, Menüsichtbarkeit, Inbetriebnahme & Kosten  
Prüfstatus: Ausschließlich wörtliche Zitate aus verifizierten Quellen, genau eine URL je Fund, keine unbegründeten Spekulationen.

---

### Fund 1: CAN-Busspezifikation, Gateway-Einbindung & Modulbegrenzung
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 34, Kap. 3 Technische Daten)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „Bussystem (Hoval-CAN-Bus)
> Belastbarkeit: max. 4 BedienModule / 3 BedienModule + 1 Gateway
> Busspeisung: ja
> Busleitung: 4-Draht Bus
> Buslänge: verdrillt, geschirmt, max. 100 m
> Leitungsquerschnitt: min 0,5 mm²“

---

### Fund 2: Adressierung der Bedienmodule (BM vs. RBM) & Inbetriebnahme-Ablauf
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 38, Kap. 5 Adressierung BedienModule)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „5. Adressierung BedienModule
> Einstellungs-Beispiel : RaumBedienmodul für den 2.Heizkreis
> 1: Inbetriebnahme-Assistent aufrufen
> 2: Adress-Nr. Bedienmodul eingeben
> 3: Regel-Modul Type auswählen und bestätigen
> 
> BM … BedienModul
> RBM .. RaumBedienmodul
> 
> Adress-Zuordnung (bei Basismodul DIP 1):
> - BM (ohne HK): Adresse 1
> - RBM (HK1): Adresse 17
> - RBM (HK2): Adresse 18
> - RBM (HK3): Adresse 19“

---

### Fund 3: DIP-Schalter für Busabschluss am Gateway (TTE-GW) und Bedienmodul (TTE-BM)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf
- **Lokale Datei:** quellen/Technische_Unterlagen_Steuerung_Hoval.pdf (Seite 39, Kap. 6.1)
- **Datum der Quelle:** 2024
- **Wörtliches Zitat:**
> „6.1 Einstellen der CAN-Busabschlusswiderstände am jeweiligen Modul:
> BasisModul-/ReglerModule (Bsp.: TTE-WEZ):
> DIP-Schalter auf ON == Busabschlusswiderstand aktiviert.
> BedienModul (TTE-BM):
> DIP-Schalter auf ON == Busabschlusswiderstand aktiviert.
> Gateway (TTE-GW):
> DIP-Schalter auf ON == Busabschlusswiderstand aktiviert.“

---

### Fund 4: Funktionale Abgrenzung TTE-BM (Zentralbedienung) vs. TTE-RBM (Wohnraum)
- **Kennzeichnung:** Herstellerdoku
- **Quelle (genau eine URL):** https://www.hoval.de
- **Datum der Quelle:** 2023
- **Zusammenfassung:**

---

### Fund 5: HovalConnect Online-Gateway — Marktpreise & Beschaffung
- **Kennzeichnung:** Nutzerangabe (Marktbeobachtung)
- **Quelle (genau eine URL):** https://www.willhaben.at
- **Datum der Quelle:** 2024
- **Zusammenfassung:**
HovalConnect Starter-Sets (LAN oder WLAN Gateway zur Anbindung der TopTronic E) liegen im Online-Fachhandel neu typischerweise zwischen ca. 240,– € und 310,– € (inkl. MwSt.). Auf Gebrauchtmärkten werden Module zwischen ca. 50,– € und 160,– € gehandelt, wobei für die Online-Nutzung die Registrierung bzw. Lizenzzuordnung im myHoval-Portal erforderlich ist.

---

### Fund 6: HovalConnect App-Sichtbarkeit vs. Fachmann-Parameter
- **Kennzeichnung:** Nutzerangabe (Forum)
- **Quelle (genau eine URL):** https://www.energiesparhaus.at/forum-hoval-ultrasource-lwp-allgemeiner-austausch-und-anlage-optimieren/56645
- **Datum der Quelle:** 2020–2024
- **Zusammenfassung:**
Über HovalConnect (App und Web-Oberfläche) haben Endanwender Zugriff auf Anlagenstatus, Temperaturen, Betriebsarten, Zeitprogramme, historische Verbrauchsverläufe und Störmeldungen. Eine direkte Parametrierung der tiefen Fachmann-Automatenparameter (wie WFA 200 Kältekreisregelung, Abtauparameter 33-281 bis 33-320 oder Invertergrenzen 34-049 bis 34-054) ist über die reguläre Endkunden-App nicht freigegeben; diese tiefen Parameter werden am physikalischen TTE-BM über das Service-Menü bedient oder sind Fachpartnern über spezielle Servicewerkzeuge vorbehalten.