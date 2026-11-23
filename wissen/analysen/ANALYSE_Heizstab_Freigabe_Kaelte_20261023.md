# Analyse F12: Wann gibt die Anlage den WP-internen 6-kW-Heizstab frei? (23.10.2026, ~21:30-22:00)

Hilfsskripte: `[lokaler Pfad]`, `..._dpl.py`, `..._log.py`, `..._bv.py`.
Vorarbeit: `[lokaler Pfad]`, `[lokaler Pfad]` (öffentliche Recherche dort schon erschöpft, hier nicht wiederholt).

## Kurzantwort
- **Die Freigabe des internen Heizstabs ist über die Hoval-Datenpunkte NICHT einstellbar oder sichtbar.** In der offiziellen Datenpunktliste (Stand April 2026) gibt es keinen Bivalenzpunkt, keine Heizstab-Verzögerung und keinen Heizstab-Status für die UltraSource. **sicher** (Liste vollständig durchsucht).
- Die TopTronic-E-Funktion „Zusatzwärme“ (WEZ, Funktionsnummer 0) ist **aus**: Betriebswahl `19485` = 0 („Wärmeerzeuger aus“), Status `18743` = 0 („Abgeschaltet“) in **allen 23 880 Logger-Zeilen 30.07.–21.10.2026**, Stunden/Schaltzyklen/Wärmemenge = 0. **sicher** (Messung). Dass diese Funktion der WP-interne Stab ist: **wahrscheinlich**.
- Die eigentliche Heizstab-Logik sitzt sehr wahrscheinlich im **Kälteregler HAICO** (iDM-Navigator-Logik): Die Firmware V1.11 enthält die iDM-Bivalenz-Parameter `BV001…BV313` (u. a. BV002/BV003 = Bivalenzpunkt 1/2 nach iDM-Registerliste). **Vermutung (V1.11, nicht V1.18.004 geprüft)**. Werte daraus sind ohne Busschreiben/Servicemenü nicht lesbar.
- Damit ist die geforderte Belegung „Parameternummer + Live-Wert der Heizstab-Freigabe“ **nicht erreichbar**. **Status: teilweise.**
- Arbeitsvorhersage für den Winter (iDM-Analogie, siehe unten): **Heizstab nur bei AT < Bivalenzpunkt (iDM-Werk 0 °C) UND erst nachdem die WP ≥ 180 K·min unter VL-Soll lag (bei 3 K Defizit = 60 min), Mindeststehzeit 10 min, oder bei verriegelnder WP-Störung.** Bei deiner 3–5-fach überdimensionierten WP entsteht dieses Defizit praktisch nie → **erwartet: 0 Heizstab-Einsätze im Winter 2026/27 bei störungsfreier WP.**

## Parameter und Live-Werte (gelesen 23.10.2026 ~21:55-22:00 MESZ, AT 7,7 °C, WP aus)
| Register | Hoval-Nr. / DP-ID | Name | Live-Wert | Logger 30.07.–21.10. | Quelle | Bedeutung für F12 |
|---|---|---|---|---|---|---|
| 19485 | DP 9075, WEZ fn 0 | Betriebswahl Wärmeerzeuger (Zusatzwärme) | **0 = aus** | immer 0 | HoxPi + Datenpunktliste | TTE-Zusatzwärme deaktiviert (sicher) |
| 18743 | DP 2053, fn 0 | Status Wärmeerzeugerregelung (Zusatzwärme) | **0 = Abgeschaltet** | 23 880× 0 | HoxPi + Logger | nie aktiv (sicher); Code 26 = „Bivalenzabschaltung“ existiert, nie gesehen |
| 18745 | DP 1009, fn 0 | Sollwert Leistung Zusatzwärme | 0 % | immer 0 | HoxPi + Logger | keine Anforderung |
| 18744 / 18746 | fn 0 | Soll / Ist Zusatzwärme | 0,0 °C / n. v. (32768) | 0 | HoxPi | kein eigener Fühler |
| 18748 / 18750 / 18753 | fn 0 | Betriebsstunden / Schaltzyklen / Wärmemenge Zusatzwärme | 0 h / 0 / 0 MWh | immer 0 | HoxPi + Logger | nie gelaufen (seit Zählerstart) |
| 27549 | **09-012** (DP 9012), WEZ fn 1 | Aussentemperatur Freigabe WEZ | **-50,0 °C** (roh 65036) | 23 875× -50,0 | HoxPi + Liste | gilt für den **WEZ 1 = WP selbst**, zusammen mit 09-011 „bedingte Freigabe“ (nicht im Modbus). -50 °C = keine AT-Sperre. Betrifft NICHT den Stab (wahrscheinlich) |
| 1561 | DP 9075, fn 1 | Betriebswahl WEZ 1 (WP) | 1 = Automatik | 99,98 % = 1 | HoxPi | WP normal freigegeben |
| 31657–31660 | ECR461 DP 1029/1030 | Betriebsst./Einschaltungen „Zusatzhzg.“ | 0 / 0 | immer 0 | HoxPi | **ohne Aussagekraft**: auch 31662 „Betriebsst. Heizung“ = 0 → ECR461-Block wird von der UltraSource nicht befüllt (sicher) |
| – | 32-031 / 30-031 | Zuo. Ausg. Elektroheizeinsatz / Sperr-Kontakt ELH | nicht im Modbus | – | TTE-Doku 4 214 513 S. 153/154 | nur WW-Nachladung (Speicher-Heizstab), nicht der WP-Stab (sicher laut Text) |

## Belege im Einzelnen
1. **Datenpunktliste** `[lokaler Pfad] Heating & Cooling\Hoval Modbus Datenpunktliste Stand April 2026 (1).xlsx`, Suche nach „Bivalen|Zusatzh|Elektro|ELH|E-Heiz|Notbetrieb|Monoenerg“: Treffer nur 18743 (Statustext mit „26 = Bivalenzabschaltung“), 27549ff (09-012) und ECR461-Zähler 31657ff. Kein Heizstab-Parameter. **sicher**
2. **Volllogger** `~/hoxpi_fulllog/2026-*.csv.gz` (5 min, 30.07.–21.10.2026, 23 880 Zeilen): Werteverteilung siehe Tabelle. Fun fact: 18722 (Status WEZ 1) einmal = 44 am 23.08. 12:00 (Bedienvorgang, 1561 = 5 zur selben Zeit). **sicher**
3. **W3-Wächter** `~/heizstab_watch.log`: 0 ALARM-Zeilen seit 24.09.2026 (Stand 23.10. 21:58). Erkennung über P_el mit Modulations-Tor (Stab = hohe Leistung bei stehendem/schwach modulierendem Verdichter). **sicher**
4. **TTE-Doku 4 214 513** (`[lokaler Pfad]`, öffentlich unter https://www.gp-joule.com/fileadmin/content/PDF-Dateien/Technische_Unterlagen_Steuerung_Hoval.pdf): ELH nur S. 153/154 im WW-Block. Keine Bivalenz-/Zusatzheizungsparameter für WP-WEZ. **sicher**
5. **Technikhandbuch UltraSource B** (lokal `...\quellen\Hoval_UltraSource_B_Technikhandbuch.pdf`, öffentlich https://www.hoval.ch/de_CH/medias/sys_master/celum_assets/4221940_UltraSource-B-Technikhandbuch_de.pdf): „Elektroheizeinsatz 1 bis 6 kW“, (17) = 3×400 V/6 kW, S. 6 „Bivalent- und Kaskadenmanagement“, S. 40 Bivalenzpunkt nur allgemein. Keine Werte. **sicher**
6. **iDM Navigator 2.0 Bedienungsanleitung** (lokal `...\quellen\IDM_Navigator_2.0_Bedienungsanleitung.pdf`, öffentlich https://assets.sta.io/site_media/u/files/2019/01/22/IDM_Navigator_2.0_Bedienungsanleitung.pdf):
   - S. 53: „Bivalenzpunkt 1 (0 °C) … unterhalb dieser Außentemperatur … der zweite/dritte Wärmeerzeuger dazu geschalten, wenn die Wärmepumpe die Sollvorlauftemperatur nicht erreicht.“ Bivalenzpunkt 2 (-10 °C): darunter nur noch 2. WEZ (bei Strategie Parallel/Alternativ).
   - S. 72, Störung 270: „wenn alle Verdichterstufen für mehr als 10 Stunden blockiert sind … Aushebelung des Bivalenzpunktes“ → Stab auch oberhalb des Bivalenzpunkts. Störung 271/272: manuelle Bivalenz, Bivalenz mit reduzierter Temperatur (ECO, kein WW).
   - Gilt für iDM; Übertragung auf die HAICO-Firmware der UltraSource: **wahrscheinlich** (baugleich AERO SLM 6-17).
7. **iDM-Menütabelle einer realen Anlage** (`[lokaler Pfad]`, iPump T 2-8, SW 20.22/20.23): Bivalenz-Block „Minimale Stehzeit 10 Min“, „Minimale Laufzeit 10 Min“, „**Abweichungsgradminuten Heizen 180 °Km**“, „Abweichungsgradminuten Warmwasser 240 °Km“, „Umschalttemperatur Verdichter/Bivalenz 52 °C“, Bivalenzpunkte dort -90/-40 °C (= praktisch aus). Werte einer fremden Anlage → **Vermutung** für deine.
9. Web-Nachsuche heute: energiesparhaus-Thread 69911 (Raumeinfluss) ohne Heizstab-Aussage (https://www.energiesparhaus.at/forum-hoval-ultrasource-mit-toptronic-e-raumeinfluss-einstellbar/69911). Threads 56645/69252/70426/75450 bereits am 23.10. geprüft (FUND_Winterbetrieb). Forumszitat Optihome: „Um den Heizstab abzuschalten solltest du einfach die Sicherung rausmachen.“ (https://www.energiesparhaus.at/forum-hoval-ultrasource-lwp-allgemeiner-austausch-und-anlage-optimieren/56645_2)

## Deutung
- **sicher:** Bisher kein Einsatz. Die TTE schickt keine Zusatzwärme-Anforderung (18745 = 0 immer).
- **wahrscheinlich:** Der WP-Stab wird vom HAICO autonom gesteuert (Bivalenz, Notbetrieb nach Störung, evtl. Frostschutz). Die TTE sieht ihn nur über die Wärmeerzeugerleistung, nicht über einen eigenen Datenpunkt. Darum taucht er in keinem Hoval-Wärmezähler auf (passt zum Projektwissen).
- **wahrscheinlich:** Hoval hat bei der Inbetriebnahme 2021 Werkswerte im HAICO belassen. Bei iDM-Werk wäre Bivalenzpunkt 1 = 0 °C (sehr „früh“). Weil der Stab aber zusätzlich eine Soll-Unterschreitung (Gradminuten) braucht, läuft er bei deiner überdimensionierten WP trotzdem nicht.
- **Vermutung:** Abtauungen erzeugen kein ausreichendes Defizit: am 13.10. fiel VL 7–10 K für ~6,5 min → grob 50–65 K·min, deutlich unter 180 K·min. Zudem lag AT dort bei 2 °C (> 0 °C).

## Vorhersage für den Winter-Wächter (notiert 23.10.2026 22:00, vor den Ereignissen)
**V103 (Heizstab-Freigabe):** Im Winter 2026/27 meldet W3 nur dann einen Heizstab-Einsatz, wenn mindestens eine der Bedingungen erfüllt ist:
- (a) **AT < 0 °C** (vermuteter Bivalenzpunkt 1) **und** WP-VL lag vorher **≥ 180 K·min unter dem WEZ-Soll** (z. B. ≥ 3 K für ≥ 60 min), und die WP lief dabei mit hoher Modulation (≥ 90 %);
- (b) eine **verriegelnde WP-Störung** (Fehlercode ≠ 255 über längere Zeit, Notbetrieb).
- Erwartung: **0 Einsätze** bei störungsfreier WP und AT ≥ -15 °C. 18743 bleibt 0, 19485 bleibt 0, 27549 bleibt -50,0.

**Widerlegt, wenn:** W3 ALARM (oder P_el ≥ 7 kW / Sprung um ~6 kW) auftritt (1) ohne Störung bei AT ≥ 0 °C, oder (2) ohne vorherige 60-min-Soll-Unterschreitung, oder (3) während/direkt nach einer Abtauung. Dann ist die Logik anders (z. B. Abtau-Stützung oder reine AT-Schwelle) und die Ereignisdaten zeigen den echten Schwellwert.

**Prüfrezept (nur lesend), je Tag mit AT-Minimum < 0 °C:**
1. `~/heizstab_watch.log` nach `ALARM` greppen.
2. Im Volllogger 18743, 18745, 19485, 27549 auf Werte ≠ Ruhewert prüfen (Skript `[lokaler Pfad]`, Glob auf neue Tage anpassen).
3. Bei einem Treffer: AT, VL-Soll/Ist (Gradminuten der letzten 2 h), Modulation, Fehlercode, Abtau-Muster X4 (V102) der 2 h davor notieren → daraus Bivalenzpunkt und Verzögerung empirisch ableiten.

## Was bringt uns das (Stromkosten)
- Stab = Arbeitszahl 1. Eine Stunde Stab = 6 kWh Strom. Dieselbe Wärme mit der WP bei Arbeitszahl ~3 (kalt) = 2 kWh. **Mehrkosten ca. 4 kWh je Stab-Stunde**, bei angenommenen 0,25 €/kWh ≈ **1 € pro Stunde** (Preis ist Annahme, nicht deiner).
- Weil die WP 3–5-fach überdimensioniert ist, reicht ihre Leistung auch bei -15 °C. Ein Stab-Einsatz wäre also kein Leistungsmangel, sondern ein **Fehlersignal** (Störung, Durchfluss, falsche Einstellung). Genau dafür ist W3 da.
- **Kein Handlungsbedarf** an der Hoval. Die Sicherung ziehen (Forum) spart nichts, solange er nicht läuft, und nimmt dir die Notreserve bei Störung. Empfehlung: drin lassen.

## Offene Reste
1. Echte Werte BV002/BV003 (Bivalenzpunkt), Gradminuten und Strategie im HAICO V1.18.004: nur über Servicemenü/Hoval-Techniker oder passiv aus einem echten Ereignis. Frage an Hoval-Service beim nächsten Termin: „Bivalenzpunkt und Freigabeverzögerung Elektroheizeinsatz UltraSource, Werkseinstellung?“
2. 09-011 „bedingte Freigabe“ (Modus zu 09-012) ist nicht im Modbus. Am Bediengerät ablesbar (WEZ-Parameter 09-011), der Betreiber bei Gelegenheit.
3. Volllogger-Dateien ab 22.10. wurden vom Glob `2026-*.csv.gz` nicht erfasst (vermutlich noch nicht gepackt). Für den Zeitraum bis 21.10. ist die Aussage vollständig.
4. Ob der Stab beim Abtauen stützt (Forum-Hinweis haustechnikdialog): bisher 3 Abtauungen ohne Stab (ANALYSE_Abtauung 22.10.), aber alle bei AT > 0 °C.

## Status-Vorschlag
**teilweise:** Mechanismus und TTE-Seite belegt, Live-Werte gelesen. Die eigentlichen Heizstab-Schwellwerte im HAICO sind nicht lesbar; Vorhersage V103 ist als prüfbare Arbeitshypothese formuliert.