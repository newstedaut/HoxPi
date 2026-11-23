# FUND: Loxone Intelligente Raumregelung (IRR) + Heiz- und Kühlsteuerung (ex Klima-Controller) – Umschaltung Heizen/Kühlen

Stand: 22.10.2026, Web-Recherche (Claude Code Subagent)

## Quellenlage (wichtig)
- Die offiziellen Loxone-KB-Seiten sind am 22.10.2026 LIVE NICHT abrufbar. https://www.loxone.com/dede/kb/klima-controller/ und .../kb/intelligente-raumregelung/ zeigen nur: "Diese Funktion ist vorübergehend nicht verfügbar."
- Deshalb wurden die offiziellen Seiten über das Internet Archive (Wayback Machine) gelesen:
  - Heiz- und Kühlsteuerung, Snapshot 18.01.2026: https://web.archive.org/web/20260118200327id_/https://www.loxone.com/dede/kb/klima-controller/
  - Intelligente Raumregelung, Snapshot 12.06.2025: https://web.archive.org/web/20250612114452id_/https://www.loxone.com/dede/kb/intelligente-raumregelung/
  (= offizieller Loxone-Text, aber Archivkopie; Config-Version der Snapshots nicht angegeben.)
- Offizielle Loxone-Doku-Links (für später, wenn wieder online):
  - Heiz- und Kühlsteuerung: https://www.loxone.com/dede/kb/klima-controller/
  - Intelligente Raumregelung: https://www.loxone.com/dede/kb/intelligente-raumregelung/ (alt: /dede/kb/irr-v2/)
- Umbenennung: Config 15.1 "Klima Controller" -> "Heiz- und Kühlsteuerung" (Loxone-Blog, s. unten).

## BELEGT (wörtliche Zitate, Seite geöffnet)

### A. Heiz- und Kühlsteuerung (ex Klima-Controller) – entscheidet zentral Heizen/Kühlen
Quelle jeweils: https://web.archive.org/web/20260118200327id_/https://www.loxone.com/dede/kb/klima-controller/

| # | Thema | Wörtliches Zitat | Werkseinstellung |
|---|---|---|---|
| A1 | Grundprinzip | "Abhängig von den Anforderungen der zugewiesenen Intelligenten Raumregler wird entschieden, ob der Heiz- oder Kühlmodus aktiv ist." | – |
| A2 | Parameter Mode | "0 = Automatischer Wechsel je nach Anforderung der Intelligenten Raumregler. 1 = Nur Heizen bei genügend Anforderung. 2 = Nur Kühlen …" (-1 = abgeschaltet) | 0 |
| A3 | Otm (Außentemp.-Modus) | "0 = Deaktiviert (ϑLimH and ϑLimC werden nicht verwendet) 1 = Durchschnittliche Außentemperatur der letzten 48h 2 = Wert der Systemvariablen 'Erwartete durchschnittliche Außentemperatur 48h' 3 = Aktuelle Außentemperatur" | 2 (Prognose 48 h) |
| A4 | ϑLimH Heizgrenze | "Wenn die verwendete Außentemperatur (Parameter Otm) über (ϑLimH) liegt, wird trotz Anforderung nicht in den Heizbetrieb gewechselt." | 18 °C |
| A5 | ϑLimC Kühlgrenze | "Wenn die verwendete Außentemperatur (Parameter Otm) unter (ϑLimC) liegt, wird trotz Anforderung nicht in den Kühlbetrieb gewechselt." | 15 °C |
| A6 | Zone dazwischen | "Ist die Durchschnittstemperatur zwischen (ϑLimH) und (ϑLimC), wird die höchste Anforderung verwendet, ansonsten nur der jeweils geforderte Modus" | – |
| A7 | Entscheidungsgröße | "Die Einflussgröße für die Entscheidung ist die Summe aller Anforderung der Raumregelungen in °m2 (Temperaturdifferenz Soll/Ist * Raumgröße)." | – |
| A8 | Bewegung priorisiert | "so kann zum Beispiel der Kühlmodus aktiv werden, obwohl die Summe aller Heizanforderungen größer sind, da ausreichend Räume mit Bewegung eine Kühlanforderung stellen." | – |
| A9 | Einschaltschwelle Sot | "Die durchschnittlichen Ventilöffnungen der Intelligenten Raumregler müssen (Sot) überschreiten, um den Betrieb zu starten." | 30 % |
| A10 | MinHr | "Die Mindestlaufzeit muss eingehalten werden, bevor in den Standby … oder in den entgegengesetzten Modus gewechselt wird." | 0 min |
| A11 | Sperre Off | "Ein: Baustein ist gesperrt. Dominierender Eingang." | – |
| A12 | Ausgang ϑoa | "Zeigt die durchschnittliche Außentemperatur der letzten 48 Stunden an. Der berechnete Wert ist verfügbar, sobald die ersten 24 Stunden vergangen sind!" | – |
| A13 | Wiedereinschalten | "Immer nachdem die Ausgänge (H) oder (C) abgeschaltet wurden, ist zusätzlich zu (Fod) noch eine Verzögerung von 3 Minuten aktiv" | – |
| A14 | Wert fehlt | (zu Otm) "Wenn der Wert nicht verfügbar ist, hat dieser Parameter keine Auswirkung." | – |

### B. Intelligente Raumregelung (IRR) – Raum fordert Heizen oder Kühlen an
Quelle jeweils: https://web.archive.org/web/20250612114452id_/https://www.loxone.com/dede/kb/intelligente-raumregelung/

| # | Thema | Wörtliches Zitat | Werkseinstellung |
|---|---|---|---|
| B1 | Grundprinzip | "Die Intelligente Raumregelung hält eine festgelegte Raumtemperatur und schaltet automatisch zwischen Heizen und Kühlen um." | – |
| B2 | Eingang Mode | "0=Automatik nach Schaltuhr: Heizen oder Kühlen basierend auf aktuellen Ist- und Solltemperaturen. 1=Automatik nach Schaltuhr: Nur Heizen, falls erforderlich; Kühlausgänge deaktiviert." | 0…5 |
| B3 | ϑch Komfort Heizen | "Absolute Komforttemperatur im Heizbetrieb." | 21 °C |
| B4 | ϑcc Komfort Kühlen | "Absolute Komforttemperatur im Kühlbetrieb." | 23 °C |
| B5 | Umschaltlogik (2 Komforttemp.) | "Unterschreitet die IST Temperatur die Komforttemperatur Heizen, so wechselt die Raumregelung in den Heizbetrieb. Wird die Komforttemperatur Kühlen überschritten, so wird in den Kühlbetrieb gewechselt." | – |
| B6 | Totzone | "Zwischen Kühl- und Heiz Komforttemperatur liegt die sogenannte "Floating Zone". Die Komforttemperatur Kühlen ist zwingend größer als die für Heizen." | – |
| B7 | Option 1 Komforttemp. ϑchc | "Absolute Komforttemperatur für Heizen und Kühlen" | 22 °C |
| B8 | ϑd Erlaubte Abweichung (nur bei 1 Komforttemp.) | "Wird dieser Bereich für mehr als 1 Minute überschritten, ist eine Umschaltung zwischen Heizen und Kühlen erforderlich" | 1,5 °C (0,5…5) |
| B9 | Eco | "Zieltemperatur (Eco Min) = ϑch - ϑeh." / "Zieltemperatur (Eco Max) = ϑcc + ϑec." | ϑeh = ϑec = 2 °C |
| B10 | Ohne Kühlquelle kein Kühlmodus | "Besteht Kühlanforderung aber keine Möglichkeit zu Kühlen, da keine Quelle (HVAC Controller, Heiz- und Kühlsteuerung) Kühlleistung zur Verfügung stellt, so wechselt der Raumregler im Vollautomatik Betrieb nicht mehr in den Kühl-Modus." | – |
| B11 | Quellenausgänge | "Die Quellenausgänge setzen den Regelungswert erst, wenn sich die Quelle im selben Modus, sprich Heizen oder Kühlen befindet." | – |
| B12 | Automatik-Modus nach Verdrahtung | "Stellantrieb an Heizungsausgang (H, H1) angeschlossen: Modus ist auf 1 eingestellt." / "…Heiz-/Kühlungsausgang (HC, HC1) angeschlossen: Modus ist auf 0 gesetzt." | – |
| B13 | Ausgang HCm | "Aktueller Modus: 1 = Heizmodus, -1 = Kühlmodus, 0 = aus" | – |
| B14 | ϑo am IRR | "Wird vom Eingang (Dwc) verwendet." (Außentemp. am IRR nur für Fensterkontakt-Logik) | – |
| B15 | Ideal-Zieltemperatur | "Die Standard-Zieltemperatur liegt genau in der Mitte zwischen ϑcc und ϑch." | – |
| B16 | Beschattung Heizbetrieb | ϑsh: "Temperatur ab welcher im Heizbetrieb die Beschattung aktiviert wird" | 25 °C (ϑsc 22 °C) |

### C. Loxone-Releasenotes / Blog (live geöffnet)
| # | Zitat | URL |
|---|---|---|
| C1 | "Um mehr Klarheit zu schaffen, haben wir den Klima Controller in Heiz- und Kühlsteuerung umbenannt." | https://www.loxone.com/dede/blog/config-app-15-1/ |
| C2 | "Entscheidungen werden ab sofort standardmäßig auf Basis der Vorhersage für die kommenden 48 Stunden getroffen." | https://www.loxone.com/dede/blog/config-app-15-1/ |
| C3 | "Wir empfehlen eigene Komforttemperaturen für heizen und kühlen vorzugeben." | https://www.loxone.com/dede/blog/config-app-15-1/ |
| C4 | "Switching between heating and cooling happens when exceeding the set deviation" (Config 15.1, 08/07/2024, Option eine Komforttemp.) | https://devicebase.net/en/loxone-config/updates/renaming-of-some-climate-blocks/4x2 |
| C5 | V10 (alt): "Der neue Config Baustein "Klima Controller" entscheidet abhängig von den einzelnen Raumreglern ob geheizt, gekühlt oder nichts gemacht werden muss." | https://www.loxone.com/dede/blog/release-os-config-app-10/ |

### D. Forum (live geöffnet, Nutzeraussagen, nicht offiziell)
| # | Zitat | URL |
|---|---|---|
| D1 | (12.05.2021, 12.1 Beta) "No more annoying 48h outdoor temperature limits (just present on the Klima Controller as an option)" – d. h. die Außentemp.-Grenzen sitzen seit 12.1 im Klima-Controller, nicht mehr im IRR | https://www.loxforum.com/forum/german/software-konfiguration-programm-und-visualisierung/294943-neue-v12-intelligente-raumregelung-irr-mit-temperaturgrenzen-heizen-k%C3%BChlen |
| D2 | (06.03.2021) Nutzer vermutet Fehler: "Es soll der Mittelwert der letzten 48 Stunden als Eingangstemperatur genommen werden. Mein Eindruck ist jedoch, er nimmt dafür die letzten 48 Minuten" | gleiche URL |

## WAHRSCHEINLICH (technisch abgeleitet, nicht wörtlich belegt)
1. Frage 2 (Herbst, Holzofen): Der IRR-Baustein selbst kennt keine Außentemperatur-Grenze (B14, D1). Steigt ein Raum über ϑcc (Werk 23 °C), stellt der IRR eine Kühlanforderung (B5). Ob tatsächlich gekühlt wird, entscheidet die Heiz- und Kühlsteuerung: bei Otm ≠ 0 und Außentemp.-Wert < ϑLimC (Werk 15 °C) wird "trotz Anforderung nicht in den Kühlbetrieb gewechselt" (A5). Bei 5–15 °C im Oktober ist Kühlen damit mit Werkseinstellung praktisch gesperrt – SOFERN Otm aktiv ist und der Wert verfügbar ist (A14).
2. Zwischen 15 und 18 °C (Werte-Zone ϑLimC…ϑLimH) entscheidet die "höchste Anforderung" (A6). Ein großer, warmer Ofenraum (°m² = ΔT × Fläche, A7) mit Bewegung (A8) kann dort den Kühlmodus für die GANZE Anlage auslösen – das ist der eigentliche Risikobereich (Übergangszeit, föhnige Tage).
3. Ohne zugewiesene Kühlquelle wechselt ein IRR nicht in den Kühlmodus (B10). Hat des Betreibers IRR keine Heiz- und Kühlsteuerung als Quelle, sondern steuert nur Stellantriebe am Ausgang HC, ist unklar, was HCm im Herbst zeigt – das ist zu prüfen (Wert HCm live lesen).
4. Gefahr bei Stellantrieben am HC-Ausgang: Bei Kühlanforderung im Raum (HCm = -1) dürfte der Raum seine Ventile für "Kühlen" öffnen, während die Wärmepumpe noch heiß fährt – dann heizt der Raum noch mehr. Bei Quellenausgängen HC1–3 verhindert Loxone das (B11), beim einfachen HC-Ausgang ist das nicht belegt.
5. Otm = 1 (Vergangenheit 48 h) ist im Herbst robuster gegen Prognosefehler als Otm = 2 (Prognose), braucht aber 24 h nach Neustart/Speichern (A12); bis dahin "keine Auswirkung" (A14) = Grenzen wirkungslos.

## NICHT GEFUNDEN
- Kein offizieller Hinweis auf einen separaten "Sommerperiode/Kühlperiode"-Parameter im aktuellen IRR (frühere Perioden-Logik nur in alten Forenthreads erwähnt, Thread 97674 nicht abrufbar).
- Kein Beleg für eine Hysterese/Mindestdauer bei der Umschaltung um ϑLimH/ϑLimC herum (außer MinHr, A10, und 3 min Sperre, A13).
- Keine Angabe, ob im IRR-Modus 0 mit nur HC-Ausgang (ohne Quelle) der Kühlmodus angezeigt/ausgegeben wird.
- Live-Version der offiziellen KB (Config 16/17) – Seiten aktuell "vorübergehend nicht verfügbar"; Parameterwerte können sich seit den Snapshots geändert haben.

## WAS BRINGT UNS DAS – Einstellempfehlung gegen "Kühlen im Oktober"

Priorität 1 – zentral in der Heiz- und Kühlsteuerung (Klima-Controller):
1. Otm prüfen: muss 1, 2 oder 3 sein. Bei Otm = 0 sind die Grenzen AUS (A3) – dann kann ein Ofenraum im Oktober Kühlen auslösen.
2. ϑLimC (Kühlgrenze) auf 18–20 °C anheben (Werk 15 °C). Alpenort (~960 m): Kühlen ist erst bei echter Sommerlage sinnvoll.
3. Werkseinstellung ϑLimH 18 / ϑLimC 15 erzeugt eine Überlappung 15–18 °C, in der BEIDES erlaubt ist und die "höchste Anforderung" gewinnt (A6) – genau der Herbst-Bereich. Empfehlung: ϑLimH = 18 °C lassen, ϑLimC = 20 °C. Dann laut A4/A5: unter 18 °C kein Kühlen (unter ϑLimC), 18–20 °C weder Heizen noch Kühlen, über 20 °C nur Kühlen. (Wahrscheinlich – dass ϑLimC > ϑLimH zulässig ist und so wirkt, folgt aus A4/A5, ist aber nicht ausdrücklich dokumentiert; nach dem Speichern ϑoa/Modus beobachten.)
4. Otm = 1 (letzte 48 h) bevorzugen statt 2 (Prognose), wenn föhnige Prognosen Fehlentscheidungen bringen. Nach jedem Speichern/Neustart 24 h ohne Wirkung (A12/A14) – im Oktober dann zusätzlich Punkt 6.
5. MinHr z. B. 60–120 min setzen (Werk 0), damit kein Pendeln Heizen/Kühlen (A10).

Priorität 2 – saisonale harte Sperre (am sichersten):
6. Mode der Heiz- und Kühlsteuerung von Oktober bis April auf 1 = "Nur Heizen" (A2) – z. B. per Jahresschaltuhr/Merker am Mode-Eingang bzw. manuell in der App. Damit ist Kühlen unabhängig von Prognose und Raumtemperatur ausgeschlossen.
7. Alternativ/zusätzlich IRR-Eingang Mode = 1 im Winterhalbjahr (B2: "Kühlausgänge deaktiviert").

Priorität 3 – Raumebene (Holzofen-Wohnzimmer UG):
8. Komforttemperaturen getrennt lassen (C3): ϑch = 21,5 °C, ϑcc = 23,0–24,0 °C im Ofenraum (statt 22,0–22,5 °C wie in anderen Räumen). Größere Floating Zone (B6) = Ofenwärme löst später Kühlanforderung aus.
9. Option "Eine Komforttemperatur verwenden" NICHT aktivieren – sonst Umschaltung schon bei ϑchc ± ϑd (B7/B8).
10. Prüfen, an welchem IRR-Ausgang die Stellantriebe hängen (H / HC / HC1). Bei HC ohne Quelle: Verhalten bei Kühlanforderung live testen (HCm beobachten), siehe "wahrscheinlich" 3+4.

Noch zu prüfen (Loxone-Daten live, nicht Web):
- In des Betreibers Config: Werte Otm, ϑLimH, ϑLimC, Mode, MinHr, Sot der Heiz- und Kühlsteuerung; Ausgang ϑoa.
- Je IRR: ϑch, ϑcc, Option "Eine Komforttemperatur", angeschlossener Ausgang, HCm-Verlauf an Ofentagen.