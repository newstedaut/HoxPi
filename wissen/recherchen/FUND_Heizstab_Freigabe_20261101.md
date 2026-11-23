# FUND Heizstab-Freigabe (F12, Recherche-Nachtrag) 01.11.2026

Katalog: F12. Orchestrator-Recherche-Agent, unbeaufsichtigt, an der Anlage **nur gelesen** (HoxPi search_registers/read_register, kein write).
Vorarbeit (nicht wiederholt): `[lokaler Pfad]` (TTE-Doku gp-joule, Technikhandbuch 4221940, Navigator-2.0-Anleitung S. 53, Datenpunktliste), `ANALYSE_Heizstab_BV_live_20261025.md`, `ANALYSE_Heizstab_Timer_Integrator_20261025.md`, `ANALYSE_Heizstab_Modus_Selektor_20261025.md`, `FUND_BV001_*_20261025.md`, `FUND_Winterbetrieb_Heizkurve_Heizstab_Abtauung_20261023.md`.

## Kurz
- Öffentlich gibt es **keine** Hoval-Quelle mit Parameternummer/Werkswert für die Freigabe des WP-internen Heizstabs (TopTronic E und UltraSource-Unterlagen). **sicher** für die geprüften Dokumente.
- Neu gegenüber Vorarbeit: iDM-Navigator-Anleitung belegt **drei weitere Freigabewege für den 2. Wärmeerzeuger** neben der Kälte-Bivalenz: Notbetrieb „Nur Bivalenz“ bei verriegelnder Störung, bivalente WW-Nachladung, Legionellenfunktion. Dazu ein Forenhinweis auf eine **Abtau-Stützung** („Bivalenz | Abtauung“, Mindest-VL 25 °C / Speicher 22 °C) bei einer baugleichen Hoval Belaria pro (= iDM ALM).
- Freigabe bei Kälte bleibt die Vorhersage aus dem Code-/Live-Stand (25.10.): **Stab erst bei AT < −10 °C (BV002 live, pCO-DB 0x8702) UND Gradminuten-Defizit ≥ 180 K·min (BV009), Mindestzeit 10 min (BV007)**. Diese Recherche ändert daran nichts.

## Belegt
1. **Notbetrieb bei WP-Störung** – iDM Navigator 2.0 Bedienungsanleitung S. 31: Parameter „Nur Bivalenz“ (Allgemeine Einstellungen) kann „im Falle einer verriegelnden Störung der Wärmepumpe, aktiviert werden“; dann übernimmt der 2. WE Heizen und WW. → **manuell** zu aktivieren, kein Automatismus laut Text.
   https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf
2. **Bivalente WW-Nachladung** – dieselbe Anleitung S. 43: die „Warmwasserladung Ausschalttemperatur“ wird „auch bei tiefen Außentemperaturen … durch Zuschaltung des zweiten oder dritten Wärmeerzeugers erreicht.“ Konkrete AT-Schwelle nicht genannt. (URL wie 1.)
3. **Legionellenfunktion über 2./3. WE** – S. 43–44: „Bei Anlagen mit zweitem oder dritten Wärmeerzeuger kann die ‚Legionellenfunktion‘ eingestellt werden“; Auswahl Aus / 2. WE / 3. WE; Ausschalttemperatur 60–67 °C; Intervall 0–7 Tage (0 = jede Ladung, 1 = täglich, 7 = wöchentlich). Werkswerte nicht angegeben. (URL wie 1.)
4. **Bivalenzpunkte** – S. 53: Bivalenzpunkt 1 (0 °C), Bivalenzpunkt 2 (−10 °C), Strategien Parallel / Alternativ / Parallel-Alternativ. (Bereits in Vorarbeit; hier nur gegengelesen.)
5. **Störung 035** – S. 70: „Erforderliche Wärmespeichertemperatur für die Abtauung wurde unterschritten.“ Ein Heizstab-Bezug steht dort **nicht**. (URL wie 1.)
6. **Hoval-Prospekt UltraSource B/T (AT)**: Heizstab nur als „Vorlauftemperatur max. (ohne/mit Einschraub-Elektroheizeinsatz) 62/65 °C“; „Legionellen haben aufgrund der thermischen Desinfektionsfunktion keine Chance.“ Keine Freigabebedingung.
   https://cdn.hoval.com/prospekt_ultrasource_b_t_at-d_de_hybris_original.pdf
7. **HoxPi live (01.11.2026, nur gelesen):** kein Register zu „Elektro“, „Bivalenz“, „Legionell(a)“, „Notbetrieb“. Treffer nur: 31657–31660 „Betriebsst./Einschaltungen Zusatzhzg.“ = 0 (laut Vorarbeit ECR461-Block, von der UltraSource nicht befüllt → ohne Aussagekraft), 18743 Status WEZ-Regelung = 0, 27549 „Aussentemperatur Freigabe WEZ“ (09-012, zu 09-011 bedingte Freigabe) = −50,0 °C, 19485 Betriebswahl Zusatzwärme = 0. Werte unverändert zu 23.10. **sicher**.

## Wahrscheinlich
- **Abtau-Stützung existiert als Einstellung** in der iDM-Logik: Nutzer chriswege (energiesparhaus, 11.11.2024, #81): „Es gibt eine Einstellung unter Bivalenz | Abtauung die die folgenden Mindest-Temperaturen angeben“ – 25 °C Vorlauf / 22 °C Wärmespeicher; dazu „Frostschutzfunktion … Wärmespeicher im Abtaubetrieb auf 20 Grad“. Kontext: Exalibur (#83) mit Hoval Belaria pro 2-8 (= iDM ALM 2-8), 6-kW-Stab, Bivalenzpunkte −15/−20 °C, sah 2,7 kWh „Elektrische Energie E-Heizstab“ bei Abtauung; coolfranz (#84) zweifelt, ob der Stab bei Abtauung überhaupt laufen sollte (Anzeige ist berechnet).
  https://www.energiesparhaus.at/forum/76163_5
  → Für die C17 (HAICO statt Navigator) nur **Analogie**; ob dieser Abtau-Zweig in V1.18.004 existiert und welche Werte er hat: offen. Prüfbar mit W3 bei Frost (Stab während/direkt nach Abtauung bei RL < ~22–25 °C).
- Notbetrieb bei Störung ist bei iDM **manuell** („Nur Bivalenz“ setzen); daneben belegt die Vorarbeit eine automatische Bivalenzpunkt-Aushebelung nach > 10 h Verdichtersperre (dort als Navigator S. 72 / Störung 270 zitiert). **Achtung:** Bei der heutigen Abfrage endet die Störungstabelle der Navigator-2.0-Anleitung bei Nr. 221 – die Fundstelle „Störung 270“ ist damit nicht gegengeprüft (evtl. andere Ausgabe). Vermerk für Loop-Prüfung.
- Legionellen: Hoval wirbt mit „thermischer Desinfektionsfunktion“. Bei max. WP-VL 62 °C (Stab: 65 °C) und WW-Soll 50/57 °C ist eine Desinfektion > 60 °C mit der WP allein knapp; ob die TTE oder der HAICO dafür den Stab nimmt: offen. Bei dir bisher 0 Stab-Einsätze (W3 seit 24.09., Vorarbeit) → eine aktive Legionellenfunktion mit Stab ist **wahrscheinlich aus** oder nie ausgelöst.

## Nicht gefunden
- Hoval-Parameternummern (Gruppe 08/09/33 o. ä.) für Heizstab-Freigabe, Bivalenzpunkt, Freigabeverzögerung, Sperrzeit, Legionellen-WEZ-Wahl, Abtau-Stützung bei UltraSource/TopTronic E.
- AT-Schwelle der bivalenten WW-Nachladung; Werkswerte der Legionellenfunktion (iDM).
- Gesucht: „Hoval UltraSource Elektroheizeinsatz Freigabe Bivalenztemperatur TopTronic E Parameter“, „iDM Navigator Heizstab Freigabe Bivalenzpunkt Notbetrieb Störung AERO SLM“, „iDM Navigator Zuschaltzeit Heizen Heizstab Bivalenz Abtauung“, „UltraSource Montageanleitung Elektroheizeinsatz Notbetrieb Kälteregler Bivalenzpunkt“, „iDM AERO SLM Navigator 1.7 Bivalenzpunkt Notbetrieb pdf“, „iDM Navigator Legionellen Heizstab Abtauung Mindesttemperatur“, „Hoval TopTronic E Legionellenschutz Elektroheizeinsatz UltraSource“.
- Geöffnet ohne neue Heizstab-Aussage: energiesparhaus 85791_2 (UltraSource B comfort 11), 56645_2 (nur Abtau-Par. 33-283/33-281/33-320 und „Sicherung rausmachen“, bekannt). Hoval-Katalog Wärmepumpen 2026 (cdn.hoval.com) nicht abrufbar (client_error).

## Parameterliste (Stand 01.11.2026)
| Parameter | Bedeutung | Werk (Quelle) | Istwert | Sicherheit |
|---|---|---|---|---|
| BV002 (pCO-DB 0x8702) | Bivalenzpunkt 1, 2. WE | iDM 0 °C (Navigator S. 53) | −10 °C (X26 passiv 24.10.) | Wert sicher, Zuordnung wahrscheinlich |
| BV003 (0x8703) | Bivalenzpunkt 2 | iDM −10 °C | −20 °C | wie oben |
| BV007/BV008 (0x8704/05) | Min. Lauf-/Stehzeit Bivalenz | iDM-Anlage 10 min | 10 / 10 min | wie oben |
| BV009 (0x8706) | Abweichungsgradminuten Heizen | iDM-Anlage 180 K·min | 180 | wie oben |
| BV010 (0x8707) | Abweichungsgradminuten WW | iDM-Anlage 240 K·min | 240 | wie oben |
| BV001 | Selektor/Modus 2. WE | – | 4 (außerhalb V1.11 0..2) | Bedeutung offen |
| CF008 | Modus AT-Merker | – | 3 | Code sicher (V1.11) |
| „Nur Bivalenz“ (iDM) | Notbetrieb bei verriegelnder Störung | manuell, Werk vermutl. Nein | nicht lesbar | Funktion belegt (iDM) |
| Legionellen-WE (iDM) | Aus/2./3. WE, 60–67 °C, 0–7 Tage | nicht genannt | nicht lesbar | Funktion belegt (iDM) |
| Bivalenz/Abtauung (iDM) | Mindest-VL 25 °C / Speicher 22 °C | Forum, Werk unklar | nicht lesbar | wahrscheinlich |
| 09-011 / 09-012 = Reg 27549 | Bedingte Freigabe / AT-Freigabe WEZ (WP selbst) | – | −50,0 °C | sicher, betrifft nicht den Stab (wahrscheinlich) |
| Reg 19485 / 18743 | Betriebswahl / Status Zusatzwärme TTE | – | 0 / 0 | sicher |

## Folgerung F12
- „fertig, wenn“ (Freigabebedingung mit Parameternummer + Live-Wert + Vorhersage) ist für die **Kälte-Freigabe** über die Vorarbeit 25.10. inhaltlich erreicht (BV002 = −10 °C, BV009 = 180 K·min, BV007 = 10 min, Vorhersage V103b/c); offen bleiben BV001 = 4 und die W3-Winterbestätigung. Öffentliche Recherche ist damit **erschöpft** – nicht wiederholen.
- Neu in die W3-Vorhersage aufnehmen: Stab-Einsatz auch möglich (1) während/nach Abtauung bei tiefem RL/Puffer (Abtau-Stützung), (2) bei WW-Ladung unter Bivalenzpunkt, (3) zyklisch bei aktiver Legionellenfunktion (WW > 60 °C). Treffer nach Muster zuordnen.