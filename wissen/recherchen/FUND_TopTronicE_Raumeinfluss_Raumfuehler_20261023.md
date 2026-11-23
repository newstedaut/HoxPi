# FUND: TopTronic E Raumeinfluss / Raumfühler / Raum-Ist über Modbus (23.10.2026)
Claude Orchestrator, Recherche 11:54. Vertieft Fund 23.1 aus `FUND_Navigator_Fachmann_Parameter_20261015.md` und H3 aus `FUND_Winterbetrieb_Heizkurve_Heizstab_Abtauung_20261023.md`.
Quellen: (Q1) Hoval TopTronic E Technische Unterlagen 4 214 513/04, lokal `quellen\Technische_Unterlagen_Steuerung_Hoval.pdf` (pdftotext neu ausgewertet, S. [Nummer]), online https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf (per WebFetch erreichbar, aber nur Inhaltsverzeichnis lesbar: „10.2.11 Raumtemperatur Kompensation" → S. 122 bestätigt; Volltext nur lokal geprüft).
(Q2) Hoval Modbus-Datenpunktliste Stand April 2026, lokal `Loxone-Templates\Hoval Heating & Cooling\Hoval Modbus Datenpunktliste Stand April 2026 (1).xlsx`, Blatt „Deutsch".
(Q3) Hoval RBM/BM-Doku https://cdn.hoval.com/toptronic-e-control-module_room-control-module_exa-cee-en_hybris_original.pdf (WebFetch geprüft).
(Q4) Hoval-Blog Loxone https://www.hoval.com/en/blog/loxone-smart-home-integrierung (WebFetch geprüft).
(Q5) energiesparhaus 69911 https://www.energiesparhaus.at/forum-hoval-ultrasource-mit-toptronic-e-raumeinfluss-einstellbar/69911 (WebFetch geprüft).
Eigene Daten: `Hoval_Parameter_Fachmann.md` (19.08.), `Hoval_Heizkreis_Datenpunkte_29-08-2026.txt` (Bus), `ANALYSE_Heizsoll_1490_1529_Aussen_20261022.md`.

## 1. Belegt
| Nr | Name | Inhalt (Q1, lokal wortgleich) | Bei dir |
|---|---|---|---|
| **03-007** | Raumtemperatur Kompensation (= Raumeinfluss-Faktor) | Textlayer zeigt in den Spalten „1 … 50" (Werkswert/Max nicht sicher trennbar, evtl. Werk 1, Max 5,0 oder 50). „Die eingestellte Kompensation multipliziert mit der Abweichung der Raumtemperatur ergibt die Korrektur der Vorlauftemperatur." Stufen 1-3 schwach, 4-6 mittel, 7-10 stark. „Bei Fussbodenheizungen sollte dieser Wert nicht über 4 eingestellt werden." (S. 113) | **0,0** (Bedienteil 19.08., Bus 29.08. roh 0000) → **Raumeinfluss AUS** |
| Formel | 10.2.11, S. 122 | „(03-007)*Raumtemperaturabweichung = VL-Sollwertkorrektur"; Beispiel 2 x 3 K = 6 K. Niedertemperatur 2…5, Hochtemperatur 4…8. Voraussetzung: „Dazu muss eine gültige Raumtemperatur vorhanden sein." | – |
| Raum-Heizgrenzen | 10.2.12, S. 122 | „Ist ein Raumeinfluss (03-007) grösser als 0 eingestellt…" werden Raum-Heizgrenzen aktiv: Raum zu warm → Heizkreis aus (03-026), zu kalt → forciert Heizen (03-025). Mittelwert-Zeitkonstante 0,5 h laut Text. | bei 03-007 = 0 **inaktiv** |
| 03-024 | Zeitkonstante Raumtemp. MW-Ber. | Dämpfung der Raumtemperatur „für die Raumheizgrenze"; 0 min direkt, > 20 min verzögert (Bereich bis 60) | 5 min |
| 03-030 | Nachstellzeit Raumregler | „Falls der Heizkreis raumgeführt geregelt wird" – I-Anteil gegen Proportionalfehler der Raumkompensation | 0,0 |
| **03-032** | Regelstrategie | 0 reine Witterungsführung · **1 Witterungsführung mit Raumaufschaltung** · 2 reine Raumregelung · **3 Konstantregelung - Externe Anforderung** (S. 123; Q2 kennt zusätzlich 4 = Witterung Heizen + Konstant Kühlen) | **3** (Bus 29.08.; Loxone schreibt 27510 = 3 zyklisch) |
| **30-051** | Zuo. Eing. Raumfühler | „0=BM" (Bedienmodul) Werk, alternativ AF/RLF/VF/SF/VE1…VE9/FE-Eingänge | nicht abgelesen |
| 10.2.21 | Externe Konstantanforderung | Bei Anforderungskontakt: „Der Heizkreis reagiert nun nur mehr auf den Anforderungskontakt." Betriebsarten/Schaltzeiten ohne Wirkung. | Loxone gibt 1490 (07-036) vor |
| **Modbus 1510** | Raum-Ist HK1 (Q2) | Zeile: 1510, WEZ, Funktionsgruppe 1/0, **DatapointId 1 = 00-001 „Raum-Ist"**, S16, 1 Dezimale, **Writable = Yes**, °C. HK2 = 1511, HK3 = 1512; weitere Instanzen 1643…, 1776…. | wird extern beschrieben (Schreiber laut ANALYSE_1510 noch offen) |
| Modbus 27510 | Regelstrategie (Q2) | Writable Yes, 0-5, Text wie oben | 3 |
| 03-007 in Modbus? | Q2 | In der Datenpunktliste April 2026 **kein** Eintrag „Raumtemperatur Kompensation" (Suche Name/Kommentar) | nur Bedienteil/CAN |

Weitere Belege:
- Q3 (RBM/BM-Doku, S. 6/17): Raumbedienmodul „can only be allocated to a heating circuit" (easy); Fühler an Innenwand, ca. 1,6 m, „No thermostatic valves are allowed to be used in the same room". → Hoval-Raumeinfluss setzt einen Führungsraum ohne Einzelraumventile voraus; das widerspricht einer Loxone-Einzelraumregelung mit Stellantrieben.
- Q4 (Hoval-Blog Loxone): „The Loxone Intelligent Room Controller specifies the target flow temperature" → Hovals eigenes Integrationskonzept: Loxone gibt den Vorlauf-Sollwert vor, nicht die Raumtemperatur als Korrekturgröße.
- Q5 (energiesparhaus 69911, Nov. 2022): Nutzer fragt, ob Raumeinfluss bei UltraSource + TopTronic E einstellbar ist; der Menüvorschlag „Raumtemp.-Stufe" stammt von der Belaria, keine Antwort mit Parameter. → öffentlich keine Praxiserfahrung.
- Eigene Daten (sicher): 1529 (00-022 HK-Soll) = 1490 + 2,6…3,0 K, auf 0,5 K gerastet, r(1490, Außen) = +0,05 (`ANALYSE_Heizsoll_1490_1529_Aussen_20261022.md`). Eine Raumkorrektur aus 1510 ist darin nicht erkennbar: Die Nachtknicke von 1510 um 0,4…1,1 K (`ANALYSE_1510_Nachtknick_Wiederkehr_20261023.md`) müssten sonst bei 03-007 = 2 als +0,8…2,2 K im VL-Soll auftauchen.

## 2. Wahrscheinlich
- **Ein extern geschriebener 1510 verschiebt den VL-Sollwert derzeit NICHT.** Gründe: 03-007 = 0 (Raumeinfluss aus, damit auch keine Raum-Heizgrenzen) und 03-032 = 3 Konstantregelung (Q1 10.2.21: Heizkreis reagiert nur auf die Anforderung). Wahrscheinlich, weil Hoval nicht ausdrücklich schreibt, ob 03-007 bei 03-032 = 3 ignoriert wird. Die eigenen Daten (1529 = 1490 + Überhöhung) stützen das.
- 1510 ist als „Raum-Ist" auch Anzeige/Status-Wert (Bedienteil zeigt ihn, 1501-Logik). Ob die TTE 1510 als „gültige Raumtemperatur" im Sinne von 10.2.11 akzeptiert, wenn 30-051 = 0 (BM) und kein RBM dem HK zugeordnet ist, ist nicht dokumentiert. Vermutlich ja, weil der Datenpunkt beschreibbar ist (Q2 „Writable Yes"); das ist aber eine Vermutung.
- Bei 03-032 = 1 (Witterung + Raumaufschaltung) oder 2 (reine Raumregelung) würde 03-007 wirken: Korrektur = 03-007 × (Raum-Soll 1493 − Raum-Ist 1510). Bei FBH laut Hoval ≤ 4; mit dem Holzofen würde jeder K Überwärme im WZ den Vorlauf für das ganze Geschoss um 03-007 K senken. Genau das ist das bekannte Ofen-Problem, nur in die Hoval verlagert.
- 03-024 = 5 min (deine Einstellung) ist sehr kurz; für Raum-Heizgrenzen mit FBH wären > 20 min (verzögert) sinnvoll, falls 03-007 jemals > 0 gesetzt wird.

## 3. Nicht gefunden
- Ausdrückliche Hoval-Aussage, ob 03-007 bei Regelstrategie 3 (Konstant/extern) wirkt oder ignoriert wird.
- Hoval-Empfehlung für FBH mit Einzelraumregelung (Loxone/KNX) zu 03-007; nur indirekt Q3 (kein Thermostatventil im Führungsraum).
- 03-007 als Modbus-Datenpunkt (nicht in Liste April 2026); 30-051 ebenfalls nicht als Modbus-Register gefunden.
- Gültigkeits-Timeout für extern geschriebenes Raum-Ist (wie lange 1510 ohne Neuschreiben als gültig gilt).
- Forenberichte mit Raum-Ist über Modbus + Raumeinfluss in der TTE.

## 4. Empfehlung FBH + Loxone-Einzelraumregelung
- **Raumeinfluss 03-007 auf 0 lassen** (ist schon so). Bei Einzelraumregelung mit Stellantrieben regelt Loxone die Räume; ein zweiter Raumregler in der Hoval auf einen einzelnen Führungsraum (WZ mit Holzofen) würde gegen die Stellantriebe arbeiten und bei Ofenbetrieb den Vorlauf für das ganze Geschoss senken. Hoval selbst verlangt für den Raumfühler einen Raum ohne Thermostatventile (Q3).
- Regelstrategie 3 (Konstant/extern) bleibt passend, solange Loxone 1490 sinnvoll vorgibt. Raumkorrektur, falls gewünscht, besser in Loxone (Vorlauf-Formel: Kurve nach Außen + kleiner Zuschlag, wenn mehrere Räume unter Soll / Ventile weit offen), nicht über 03-007.
- 1510 schadet bei 03-007 = 0 nach heutigem Stand nicht, ist aber als Führungsgröße ungeeignet (Nachtknick, Fühlerort). Vor jedem Umstellen auf 03-032 = 1 zuerst den Fühlerort/Schreiber klären.
- Alternative zu Loxone-Kurve: 03-032 = 1 mit 03-007 = 0 wäre faktisch reine Witterungsführung (= 0); das wäre ein eigener Versuch, nicht Teil dieser Frage.

## Was der Betreiber am Bedienteil ablesen soll (nur lesen)
Pfad wie `Hoval_Parameter_Fachmann.md`: Service → TTE-WEZ → Heizkreis 1 → Parameter / Konfiguration. 2-3 s warten, bis Werte geladen sind.
1. 03-007 Raumtemperatur Kompensation (erwartet 0,0) – Bestätigung.
2. 03-032 Regelstrategie (erwartet 3).
3. **30-051 Zuo. Eing. Raumfühler** (Konfiguration, Werk 0 = BM) – neu, noch nie abgelesen.
4. 03-024, 03-025, 03-026 (Raum-Heizgrenzen; nur relevant falls 03-007 > 0).
5. Anzeige „Raum-Ist" am Bedienteil HK1 und gleichzeitig Loxone WZ tempActual notieren (Uhrzeit) – zeigt, ob das Bedienteil den extern geschriebenen 1510 oder seinen eigenen Fühler anzeigt.
6. Ob ein Raumbedienmodul (TTE-RBM, Adr 17 laut Anlagendoku) dem HK1 zugeordnet ist und wo es hängt.
Nichts verstellen.

## Was bringt uns das
- Klärt die offene Frage aus `ANALYSE_1510_Nachtknick_Wiederkehr_20261023.md`: Der 1510-Nachtknick wirkt mit 03-007 = 0 und Regelstrategie 3 sehr wahrscheinlich nicht auf den Vorlauf. Die Sollwertkette bleibt 1490 → +3 K → 1529 (eigene Daten bestätigen das).
- Damit muss man 1510 nicht „reparieren", um die Heizung zu verbessern. Der Hebel ist 1490 in Loxone (außentemperaturgeführt statt Tagesfestwert).
- Falls später doch Raumeinfluss gewünscht: Formel, Grenzen (FBH ≤ 4) und Nebenwirkung (Raum-Heizgrenzen 03-025/03-026 werden aktiv) sind jetzt belegt. Modbus kann 03-007 nicht setzen; nur Bedienteil/CAN.