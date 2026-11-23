# FUND: Winter-Check – Abtauung, Kondensatablauf, Luftseite (Hoval UltraSource B comfort C 17)

- **Datum:** 23.10.2026 (Recherche-Agent, Web + lokale Quellen-PDFs)
- **Anlage:** Hoval UltraSource B comfort C 17, Inbetriebnahme 10/2021, Alpenort (~960 m) ca. 1000 m
- **Frage:** Was muss vor/im Winter geprüft werden, damit Abtauung, Kondensatablauf und Luftseite funktionieren? (1) Bauart/Herstellervorgaben, (2) typische Winterprobleme + Betreiber-Prüfungen + Intervalle, (3) Erkennen schlechter Abtauung in Betriebsdaten.

**Abgrenzung / nicht wiederholt:** Kondensatmenge 6 l/2 min, Wannenheizung + Heizband, Pufferpflicht (EnerVal 300), 20 °C Mindest-Puffertemperatur, Schneefreiheit Verdampfer, Frostgefahr Ausblasseite, Abtau-Parameter 33-28x / 34-054, iDM-Störcodes 032/033/[Nummer], Kreislaufumkehr-Prinzip, Abtaudauer 5–15 min (iDM) → alles schon in `FUND_Abtauung_20261015.md` (Funde 3–57, v. a. 6, 7, 10, 17, 19, 26, 27, 38, 39, 46, 47).
Hinweis: `FUND_Winterbetrieb_Heizkurve_Heizstab_Abtauung_20261022.md` enthält beim Lesen am 23.10. nur 2 Zeilen (Kopf, Text bricht nach „Recherche-Agent im" ab) → Datei vermutlich unvollständig geschrieben, bitte prüfen.

---

## 1. BELEGT

### B1 Bauart: Split mit Außen- und Inneneinheit, keine Luftkanäle
- Quelle: https://cdn.hoval.com/prospekt_ultrasource_b_t_at-d_de_hybris_original.pdf (S. 4)
- Zitat: „Luft/Wasser-Wärmepumpe in Split-Bauweise mit Innen- und Außeneinheit"
- Kältemittelleitungen (C 17: Sauggas 18x1, Flüssig 12x1), max. 16 m, Kondensatanschluss unten: Montage-Produktinfo 4221941/02 (s. B2), S. 6–7.
- Folge: Die Außeneinheit (C 17: 1546 x 1090 x 745 mm, Prospekt S. 6) ist das einzige luftseitige Bauteil; Abtauung, Kondensat, Schnee betreffen nur sie. Luftkanäle gibt es bei dieser Bauart nicht (keine Kanal-Angaben in Prospekt/Montageinfo gefunden).

### B2 Mindestabstände Außeneinheit (neu gegenüber FUND_Abtauung)
- Quelle: Hoval Produktinformation 4221941/02 „Wichtige Produktinformationen UltraSource B comfort C (8-17)", Stand 2025-07, S. 2. Öffentliche URL: https://www.hoval.at/medias/4221941-02-DE.pdf?context=bWFzdGVyfHJvb3R8Mzk3NDAxM3xhcHBsaWNhdGlvbi9wZGZ8YURFekwyZ3pOUzh4TURNME5EUTJNamszTlRBd05pODBNakl4T1RReExUQXlMVVJGTG5Ca1pnfDEzNjIzMDI0N2I4YzE0ZjA0ZTNhNDNmMzg5NzcyNDkxMjFjMWJhM2E0YTJiNDFlZTE2MDJmOGIxZThkMDE0NjI (gelesen aus lokaler Kopie `quellen/Hoval_UltraSource_B_4221941-02-DE.pdf`)
- Zitate: „Die Luftansaug- und Luftausblasseite dürfen nicht verengt oder zugestellt werden."
- „Ausblasseite 2000 mm, Seitenabstand links und rechts 400 mm, Rückseite 400 mm" (oben 600 mm für Wartung)
- „Die Luftausblasseite muss die vom Gebäude abgewandte Seite und frei (> 2 m) sein."
- Zeichnung S. 2 enthält Pfeil „Zu erwartende Windrichtung" → Ausrichtung zur Windrichtung ist planungsrelevant (Text dazu nicht vorhanden).

### B3 Kondensatablauf: Ausführung laut Hoval (Ergänzung zu FUND_Abtauung F27/F39)
- Quelle: wie B2, S. 5–7
- „Der Kondensatablauf muss frostsicher ausgeführt werden."
- „Bei Frostgefahr muss unmittelbar vor der Einführung des Kondensatablaufs in das Fallrohr im Schacht ein Siphon installiert werden."
- „Die Kondensatablaufleitung muss mit Gefälle verlegt werden."
- S. 5: „Oberkante Kondensatablauf 50-100 mm über Bodenniveau Alternativ: Ohne Ablauf. Versickerung des Kondensat im Boden." S. 6: Varianten „Schacht/Kieskoffer" oder „Ableitung in die Kanalisation"; Anschluss Rp 1″ auf Abflussrohr DN 100.
- S. 6 Zeichnung: „Schneehöhe beachten! Höhe Verdampfer"; S. 9: eigene Zuleitung „Begleitheizband 3-pol 230 V".

### B4 Abtauung durch Kreislaufumkehr (iDM-Basis, bereits belegt)
- Siehe FUND_Abtauung F12/F19 (https://www.idm-energie.at/waermepumpen-technologie/abtauung/). EnergieSchweiz nennt das Verfahren „Abtauen mit Prozessumkehr": „Dabei wird der Kältekreislauf umgekehrt." (https://pubdb.bfe.admin.ch/de/publication/download/9977)
- Für Hoval selbst: im Prospekt kein Abtauverfahren genannt (s. Nicht gefunden).

### B5 Typische Winterprobleme (allgemeine Fachquellen)
- Bosch: Dünne Eisschicht normal – „Solange sich bei niedrigen Außentemperaturen nur eine dünne Eisschicht bildet, stellt das kein Problem dar." Problem erst: „wenn der Kondensatablauf, Ventilator oder Außenrohre einfrieren." Prüfen, „ob Lufteinlass und -auslass durch Laub, Schnee oder Staub blockiert sind." Bei Resteis „etwa 30 bis 90 Minuten" abwarten; „Entfernen Sie das Eis niemals gewaltsam!" – https://www.bosch-homecomfort.com/de/de/wohngebaeude/wissen/heizungsratgeber/waermepumpe/waermepumpe-vereist/
- EnergieSchweiz: „Die Eisbildung auf dem Verdampfer ist ein verlässlicher Hinweis, wie gut der Abtauvorgang funktioniert." Warnzeichen: „Bildet sich eine ungleichmässige Eisschicht und gibt es stärker vereiste Stellen" → Abtauung prüfen. – https://pubdb.bfe.admin.ch/de/publication/download/9977
- Akkudoktor-Forum (redhot, 18.12.2025, v. a. Split-Klima/LWWP): Wannen-/Ablauflöcher frieren zu, dann wächst Eis rasch: „Sind das / die Löcher erstmal zu - geht es sehr schnell und das Eis wächst…" – https://akkudoktor.net/t/ideensammlung-luft-waermepumpen-llwp-lwwp-abtauwanne-beheizen-um-vereisung-zu-verhindern/35265
- 42watt: Vereisungsursachen u. a. „gestörter Kondensatablauf" und defekter Ventilator; „Ein verschmutzter oder vereister Verdampfer vergrößert diesen Abstand." (Abstand Quelle–Verdampfungstemperatur) – https://42watt.de/magazin/verdampfer-warmepumpe

### B6 Intervalle
- Verdampfer reinigen: „Reinigen Sie den Verdampfer alle 2 Jahre." Am besten im Herbst, „wenn die Blätter der Bäume schon gefallen sind" (EnergieSchweiz, ca. 2021) – https://pubdb.bfe.admin.ch/de/publication/download/9978
- Abtauung prüfen lassen: „Überprüfen Sie die Abtauung alle 3 bis 5 Jahre." – https://pubdb.bfe.admin.ch/de/publication/download/9977
- Kondensatwanne/-ablauf: „müssen regelmäßig auf Verschmutzungen kontrolliert und gegebenenfalls gereinigt werden" (iDM AERO SLM, baugleiche Basis; FUND_Abtauung F11) – ohne konkretes Intervall.
- Hochdruckreiniger: 42watt: „Ein Hochdruckstrahl kann die Lamellen verbiegen und Wasser in die Elektronik drücken."

### B7 Abtau-Kennwerte (Dauer/Häufigkeit) – nur Richtwerte, keine Grenzwerte
- Dauer: Bosch „etwa 3 bis 10 Minuten", Zyklus wiederholt sich „mehrmals täglich"; iDM 5–15 min (FUND_Abtauung F18, ausdrücklich kein Grenzwert); Hoval-Parameter max. Abtauzeit 33-283 = 15 min (Forum, F6).
- EnergieSchweiz-Beispiel: Abtauung unter 5 °C „nach 1 Stunde Laufzeit", Abtauung ideal im Bereich ca. -2 bis +5 °C; Heißgas-Bypass-Laufzeit „10 bis 15 Prozent der Laufzeit" (anderes Verfahren!). Zu viel Abtauen: „Wird jedoch zu oft abgetaut, steigt der Energieverbrauch für die Abtauung und die Jahresarbeitszahl der Wärmepumpe sinkt." – https://pubdb.bfe.admin.ch/de/publication/download/9977
- Hoval-UltraSource-Nutzer (energiesparhaus, Thread 56645): bei 0–4 °C „ca. jede Stunde einmal" (Domi90, 18.11.2023); „ca. alle 2 Stunden" (Optihome, 22.11.2023); „16-18 pro Tag", nach Stromausfall „ca. 5-7mal" (Domi90, 11.12.2023). Laut Hoval-Kundendienst: „Die Abtauvorgänge werden tatsächlich als Schaltvorgänge gezählt." (sharknz, 09.02.2022) – https://www.energiesparhaus.at/forum-hoval-ultrasource-lwp-allgemeiner-austausch-und-anlage-optimieren/56645_2
- Vergleichsfall Ausreißer (anderes Gerät, Wien): „ca. 900 Abtauvorgänge pro Monat. (29 pro Tag)", von anderen als „absolut nicht normal" bewertet – https://www.energiesparhaus.at/forum-lwwp-abtauvorgaenge-monat/84777_3

### B8 Widerspruch Enteisen mit Wasser
- iDM ALM-Doku: Abtauung darf „unter zu Hilfenahme von Wasser beschleunigt werden", mechanisch verboten (FUND_Abtauung F46).
- 42watt/Bosch: „Entfernen Sie Eis nie mit Werkzeug oder heißem Wasser." → Konsens nur: kein Werkzeug, keine Gewalt. Heißes Wasser vermeiden; lauwarmes Wasser nur nach iDM zulässig.

---

## 2. WAHRSCHEINLICH (Schluss aus Belegen, nicht wörtlich belegt)
- W1: Abtauverfahren der UltraSource B = Kreislaufumkehr wie iDM AERO SLM (OEM-Basis, gleiche Kältedaten 4,8 kg R410A; Parameter „Leistung Abtauen", „Temperatur Abtauende 36°" deuten auf Wärmeentzug aus Heizwasser). Hoval selbst sagt es im Prospekt nicht.
- W2: Alpenort (~960 m) (1000 m, viel Schnee, Nebel/Hochnebel um 0 °C) liegt im ungünstigsten Vereisungsbereich (-2 bis +5 °C, hohe Feuchte) → Abtauhäufigkeit ~1/h bei 0–4 °C ist dort erwartbar und kein Fehler.
- W3: Häufigste reale Winterstörung bei dieser Bauart ist nicht die Abtaulogik, sondern Eisaufbau von unten: Kondensatablauf/Versickerung zugefroren oder Heizband nicht korrekt im Ablauf (Überlänge ca. 1 m muss im Rohr liegen) bzw. Begleitheizband ohne Spannung (eigene 230-V-Zuleitung, z. B. Sicherung aus).
- W4: Schnee: Hoval nennt keine cm-Zahl; iDM AERO SLM fordert 20 cm über erwarteter Schneehöhe (F45). Für Alpenort (~960 m) heißt das: Unterkante Verdampfer über der realen Maximal-Schneehöhe inkl. Dachlawinen/Räumschnee + 20 cm.
- W5: Windrichtung: Ausblas gegen Hauptwind kann Kaltluft zurück auf die Ansaugung drücken (Luftkurzschluss) → mehr Vereisung. Hoval zeichnet die Windrichtung ein, erklärt sie aber nicht.
- W6: Sinkende Verdampfungstemperatur (bzw. größerer Abstand Außenluft–Verdampfung) bei gleicher Leistung zwischen zwei Abtauungen ist der physikalische Vereisungsindikator (42watt qualitativ). Eine Grenze in Kelvin ist nicht belegt.

---

## 3. NICHT GEFUNDEN
- Öffentliche Hoval-Bedienungsanleitung (Betreiber) mit Winter-/Reinigungshinweisen für UltraSource B.
- Hoval-Aussage zum Abtauverfahren (Kreislaufumkehr vs. Heißgas) – weder Prospekt noch Produktinfo 4221941/02.
- Hoval-Angabe in cm zur Schneehöhe (nur „Schneehöhe beachten!" und Empfehlung ≥300 mm Erhöhung).
- Leistung der Wannenheizung / des Begleitheizbands (W) und deren Ansteuerlogik bei Hoval (nur Parameter „Laufzeit Kondensatablaufheizung Abtauung" 20–25 min aus Forum).
- Belegte Kennwerte in Kelvin für „schlechte Abtauung" (z. B. ΔT Luft–Verdampfung, Abfall Verdampfungstemperatur pro Zeit) – keine belastbare Quelle gefunden.
- Belegte Normwerte für Abtauungen/Tag oder Energieanteil der Abtauung bei Kreislaufumkehr-Geräten.
- Heizstab-Einsatz während/nach Abtauung bei Hoval UltraSource (ob Regler den 6-kW-Heizeinsatz dafür freigibt).
- Luftkanal-/Innenaufstellungsvariante: existiert für diese Baureihe nicht (nur Split mit Außeneinheit).
- Kein Abruf möglich: hoval.ch-Montageanleitung und gp-joule-Technikhandbuch (client_error am 23.10.2026); Inhalte stattdessen über lokale Kopien bzw. FUND_Abtauung.

---

## 4. BETREIBER-CHECKLISTE VOR DEM WINTER (Außeneinheit UltraSource B C 17)
1. **Freiräume prüfen:** Ansaug- und Ausblasseite frei, nichts zugestellt (Brennholz, Mülltonnen, Pflanzen, Schneeräumhaufen). Ausblas ≥ 2 m frei, seitlich/hinten ≥ 0,4 m (B2).
2. **Laub & Schmutz:** Lamellen auf der Ansaugseite sichtprüfen, Laub/Grobschmutz von außen von Hand oder weicher Bürste entfernen; kein Hochdruckreiniger (B6). Gründliche Verdampferreinigung (Deckel ab, stromlos) alle ca. 2 Jahre durch Fachbetrieb.
3. **Kondensatablauf testen:** Kübel Wasser (5–6 l, entspricht einer Abtauung, F5/F17) langsam in die Kondensatwanne/den Ablauf gießen – muss zügig ablaufen, kein Rückstau, kein Stehwasser im Schacht/Kieskoffer (B3).
4. **Heizband prüfen:** Sichtprüfen, ob das Heizband (Überlänge ca. 1 m) wirklich im Ablaufrohr liegt; Sicherung der Begleitheizband-Zuleitung (230 V) ein. Bei Frost nach einer Abtauung fühlen, ob Ablaufbereich nicht vereist ist.
5. **Schneehöhe/Dachlawine:** Unterkante Verdampfer gegen die reale Maximal-Schneehöhe am Standort prüfen (Ziel: ≥20 cm darüber, W4). Abstand zu Dachtraufe/Dachlawine; Räumschnee nie vor die Ansaugung schieben.
6. **Ausblasseite:** Kein Gehweg, keine Dachrinne/Wasserleitung direkt im Ausblas (Frostgefahr, F38) – Glatteis im Ausblasbereich einplanen.
7. **Im Winter regelmäßig (nach Schneefall/Nebeltagen):** Sichtkontrolle: dünner, gleichmäßiger Reif = normal; Eis nur unten, ungleichmäßig oder nach Abtauung bleibend = melden (B5). Eis nie mit Werkzeug entfernen; 30–90 min auf nächste Abtauung warten.
8. **Puffer-/Heizkreis-Voraussetzung:** Puffer im Winter nie unter 20 °C, genügend Heizkreise offen (Loxone-Stellantriebe!) – sonst fehlt Abtauenergie (FUND_Abtauung F2/F26/F42).
9. **Datenbasis anlegen:** Abtauungen/Tag, Abtaudauer, Außentemperatur/-feuchte mitloggen (HoxPi), siehe Abschnitt 5.

---

## 5. WAS BRINGT UNS DAS
- **Sicher:** Die UltraSource B C 17 ist Split, nur die Außeneinheit ist luftseitig kritisch. Winterrisiken liegen bei Schnee vor/unter der Einheit, zugefrorenem Kondensatablauf und blockierter Ansaugung – nicht bei Kanälen.
- **Sofort umsetzbar:** Checkliste Punkte 1–6 einmal jetzt vor dem ersten Schnee (Kübeltest + Heizband + Sicherung), Foto der Außeneinheit von vorne/unten/Ablauf als Referenz für den Winter.
- **Bewertungsrahmen für Abtauung (vorläufig, Richtwerte, keine Grenzwerte):**
  - Dauer typ. 3–15 min; deutlich darüber oder Abbruch bei 15 min (33-283) = auffällig.
  - Häufigkeit bei 0–4 °C/feucht ~1/h bei hoher Leistung = laut Hoval-Nutzern normal; bei < -5 °C trockener Luft eher alle 2–3 h.
  - Auffällig: Eis bleibt nach Abtauung, Eis wächst von unten, ungleichmäßige Vereisung, Abtauung bei trockener Kälte deutlich häufiger als an feuchten 0-°C-Tagen.
- **HoxPi-Auswertung (Vorschlag):** pro Tag Abtau-Anzahl, mittlere/max. Dauer, Außentemperatur/-feuchte, Puffer-/Rücklauf-Temperatur zu Abtaubeginn und Verdampfungstemperatur vs. Außenluft im Zyklus zwischen Abtauungen. Ein stetig wachsender Abstand Außenluft–Verdampfung bei gleicher Verdichterleistung zeigt Vereisung (W6); ein Heizstab-Einsatz direkt nach Abtauung oder Rücklauf < ~20 °C deutet auf fehlende Abtauenergie (Puffer/Stellantriebe).
- **Offen für der Betreiber:** Foto Kondensatablauf/Schacht und Heizband, Abstand Unterkante Verdampfer–Boden, Ausrichtung Ausblas vs. Hauptwind, Prüfung ob Begleitheizband separat abgesichert ist.

---

## 6. QUELLEN
1. Hoval Prospekt UltraSource B (AT/DE): https://cdn.hoval.com/prospekt_ultrasource_b_t_at-d_de_hybris_original.pdf
2. Hoval Produktinformation 4221941/02 (Stand 2025-07): https://www.hoval.at/medias/4221941-02-DE.pdf?context=bWFzdGVyfHJvb3R8Mzk3NDAxM3xhcHBsaWNhdGlvbi9wZGZ8YURFekwyZ3pOUzh4TURNME5EUTJNamszTlRBd05pODBNakl4T1RReExUQXlMVVJGTG5Ca1pnfDEzNjIzMDI0N2I4YzE0ZjA0ZTNhNDNmMzg5NzcyNDkxMjFjMWJhM2E0YTJiNDFlZTE2MDJmOGIxZThkMDE0NjI (lokal: quellen/Hoval_UltraSource_B_4221941-02-DE.pdf)
3. EnergieSchweiz/BFE „Betriebsoptimierung Heizung: Abtauung Luft-Wasser-Wärmepumpen" (11.2021): https://pubdb.bfe.admin.ch/de/publication/download/9977
4. EnergieSchweiz/BFE „Verdampfer von Wärmepumpen regelmässig reinigen": https://pubdb.bfe.admin.ch/de/publication/download/9978
5. Bosch Home Comfort „Wärmepumpe vereist": https://www.bosch-homecomfort.com/de/de/wohngebaeude/wissen/heizungsratgeber/waermepumpe/waermepumpe-vereist/
6. 42watt „Verdampfer Wärmepumpe": https://42watt.de/magazin/verdampfer-warmepumpe
7. energiesparhaus.at Hoval-UltraSource-Thread S. 2/3: https://www.energiesparhaus.at/forum-hoval-ultrasource-lwp-allgemeiner-austausch-und-anlage-optimieren/56645_2 und …/56645_3
8. energiesparhaus.at „LWWP Abtauvorgänge/Monat": https://www.energiesparhaus.at/forum-lwwp-abtauvorgaenge-monat/84777_3
9. akkudoktor.net Abtauwanne-Thread: https://akkudoktor.net/t/ideensammlung-luft-waermepumpen-llwp-lwwp-abtauwanne-beheizen-um-vereisung-zu-verhindern/35265
10. haustechnikdialog SHKwissen „Abtauen Wärmepumpe" (nur allgemein, keine Kennwerte): https://www.haustechnikdialog.de/SHKwissen/3797/Abtauen-Waermepumpe
11. Verweis: FUND_Abtauung_20261015.md (iDM-AERO-SLM-Montageanleitung, Hoval-Technikhandbuch, iDM-Abtauseite, Navigator 2.0)

> Claude-Pruefvermerk 23.10.2026 04:20: Zitat 'Ueberpruefen Sie die Abtauung alle 3 bis 5 Jahre.' per WebFetch pubdb.bfe.admin.ch/.../9977 wortgleich bestaetigt. Satz 'Reinigen Sie den Verdampfer alle 2 Jahre.' im selben Dokument per WebFetch NICHT gefunden -> bis Gegenbeleg nur 'wahrscheinlich'.