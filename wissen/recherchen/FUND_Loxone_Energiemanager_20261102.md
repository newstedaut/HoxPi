# FUND F78 - Loxone Energiemanager: Rechnung, Vorzeichen, Versionen (02.11.2026)
Claude, Rechercheagent. Nur gelesen: Web, Projektdatei, Loxone-MCP (Zustände). An Anlage, Loxone und Pi nichts geändert. Keine Empfehlung umgesetzt.
Hintergrund: `[lokaler Pfad]`

## Kernaussage
1. **Unser Baustein ist die neue Version** (`Type="EnergyManager2"`). [sicher]
2. **Die Doku sagt: Spwr negativ = Laden. Unser Spwr kommt aus Victron-Reg 842, laut F76 negativ = Entladung, ohne Invertierung.** Damit sieht der Energiemanager (EM) eine Akku-Entladung als Ladung, also als Überschuss. [Doku und Verdrahtung sicher; Vorzeichen 842 nur aus F76, nicht live bestätigt]
3. **Der Spwr-Fix vom 18.10. gibt die Entladung abends genau so an den EM weiter.** Das passt dazu, dass er die dunklen Flanken nicht beseitigt hat. [wahrscheinlich]
4. **Ppwr geht nicht in die Rechnung ein** (nur Anzeige). Der EM kennt keine PV-Bedingung. [sicher laut Doku]
5. **Ausschalten bei der WP erst, wenn der Netzbezug 5,4 kW übersteigt** (6,9 - 1,5) und MinRt abgelaufen ist. Das erklärt das lange Halten. [Doku-Regel sicher; Anwendung auf uns wahrscheinlich]

## Belegt
### Versionen
- Es gibt zwei Bausteine. Alt: [energy-manager](https://www.loxone.com/enen/kb/energy-manager/), Eingänge AIp, AIb, AIt, Tr1-12, Ausgänge Q1-12, AQr, Rechnung einmal pro Minute. Neu: [energy-manager-2](https://www.loxone.com/enen/kb/energy-manager-2/), DE: [energiemanager-2](https://www.loxone.com/dede/kb/energiemanager-2/).
- Generation 2 kam mit Config 13.1. Neu sind steuerbare Lasten wie Wallboxen und die priorisierte Mindestladung des Speichers. Der alte Baustein wird nicht automatisch umgewandelt: [Blog 13.1](https://www.loxone.com/enus/blog/config-app-13-1/).
- „Power Flow" ist keine EM-Version. Der Blog nennt den getrennten Baustein Energy Flow Monitor.
- **Bei uns:** `[lokaler Pfad]` Z. 8078 `Type="EnergyManager2"`; Live-Schema `control_type_id 515`, Hilfelink www.loxone.com/help/energy-manager.

### Eingänge und Vorzeichen (Quelle: [energy-manager-2](https://www.loxone.com/enen/kb/energy-manager-2/), [DE](https://www.loxone.com/dede/kb/energiemanager-2/))
| Eingang | Doku | Bei uns |
|---|---|---|
| Gpwr | kW, negativ bei Einspeisung | Victron Grid, Summe / 1000 (Z. 11343 ff.) |
| Ppwr | „Only used for the user interface" | PV-Total, ohne Wirkung auf die Rechnung |
| Spwr | „Negative value when charging the storage" | Formel O64266 aus Reg 842 |
| Soc | % | Victron |
| L1-L12 (Datei IL1-12) | Status digital oder Leistung analog in kW | IL1 Wallbox, IL3 Heizkörper, IL6 = 25611; IL2 Heizstab frei |
| Prio / Recalc | Startet Last sofort / rechnet sofort neu | Nicht verdrahtet (Z. 8087 f.) |
| Off (Datei Reset) | Impuls setzt zurück, Dauer-Ein sperrt | Wallbox-Logik |
| MinSoc | Unter MinSoc hat Speicherladen höchste Priorität | SOC_Freigabe, live 95 |
| MaxSpwr | Max. Ladeleistung des Speichers | 6 kW, live gelesen |

Verdrahtung Reg 842: `ModbusAddress="842"`, Skalierung 1000 → 1, keine Invertierung (Z. 2936). [sicher]

### Einschalten und Ausschalten
- Ein: „Loads will switch on when there is more surplus energy than the defined switch-on power" ([Quelle](https://www.loxone.com/enen/?p=270737)). Reihenfolge nach Priorität 1 bis 12.
- Aus, nach Doku (dieselben KB-Seiten):
  - Digital, Einschaltleistung ≥ Maximalleistung: wenn der Überschuss unter die Maximalleistung fällt.
  - **Digital, Einschaltleistung < Maximalleistung: wenn der Netzbezug die Differenz beider Werte übersteigt. Das ist unsere WP** (`SwPwr 1,5`, `MaxPwr 6,9`, ohne `An="true"`, Z. 8135).
  - Analog: wenn der verfügbare Überschuss unter die Einschaltleistung fällt.
- „loads are only switched off after their minimum run-time has elapsed" ([Quelle](https://www.loxone.com/enen/?p=270737)). Abschaltung in umgekehrter Reihenfolge ([CZ-KB](https://www.loxone.com/cscz/kb/energeticky-manager/)).
- Unter MinSoc: Laden mit MaxSpwr hat Vorrang, danach nur noch aus Überschuss. Lasten erst, wenn MinSoc erreicht ist oder die Speicherleistung MaxSpwr übersteigt ([CZ-KB](https://www.loxone.com/cscz/kb/energeticky-manager/), sinngemäß übersetzt).
- Ohne angeschlossenen Status nimmt der EM an: Last ein, verbraucht Ausgangswert bzw. Maximalleistung. Mit Status nutzt er den gemeldeten Wert ([energy-manager-2](https://www.loxone.com/enen/kb/energy-manager-2/)).
- Tagesmindestlaufzeit kann Lasten ohne Überschuss starten ([Quelle](https://www.loxone.com/enen/?p=270737)). Bei uns zeigt die Last WP kein solches Attribut (Z. 8135), also [wahrscheinlich] nicht die Ursache.

### Live gelesen (Loxone-MCP, ts 02.11. 06:00 Z)
`Gpwr 2,377`, `Spwr 0`, `Ssoc 33`, `MinSoc 95`, `MaxSpwr 6`. Im Zustand `loads` steht die WP mit `pwr 1,77`, `hasActual true`, `active false`. Der EM übernimmt also den kW-Wert von IL6 auch bei digitaler Last und unterscheidet ihn vom eigenen Schaltzustand. [sicher] Akku stand still, daher kein Vorzeichentest. Keine Verlaufsdaten im MCP.

## Wahrscheinlich
- **Formel der Rechnung** (nirgends veröffentlicht, eigene Herleitung aus den Doku-Sätzen):
  `A = -Gpwr - Spwr + Istleistung eigener und niedriger priorisierter Lasten - (Soc < MinSoc ? MaxSpwr : 0) - O`; Einschalten bei `A > SwPwr`. Die Teile „Istleistung" und „Reserve" sind [Vermutung], der Rest folgt aus den Vorzeichen.
- **Rechenintervall:** Standard 60 s laut Forenbeitrag ([loxforum 442821](https://loxforum.com/forum/faqs-tutorials-howto-s/442821-ems-simulation-im-anlagenschema)). Unsere leeren Lasten stehen auf `RT="60"`, die WP auf 300. RT ist daher vermutlich das Intervall in Sekunden; in der Doku fehlt das Kürzel. [Vermutung]
- **Hysterese:** Kein eigener Parameter. Sie entsteht aus MinRt und dem Abstand SwPwr/MaxPwr.

## Nicht gefunden
- Offizielle Formel, Rolle von RT, Verrechnung der Istlast mit dem Überschuss.
- Offizielles Victron-Dokument mit dem Vorzeichen von Reg 842. Die Registerliste nennt nur „Battery power (System)", W, signed ([aggsoft](https://www.aggsoft.com/modbus-data-logging/victron.htm)). Victron-Forum: „Negative is discharge - Positive is charge", aber für VE.Bus charge power, nicht für 842 ([Thread](https://communityarchive.victronenergy.com/questions/186940/vebus-charge-power-system.html)).
- Structure-File: [1701](https://www.loxone.com/dede/wp-content/uploads/sites/2/2021/10/1701_Structure-File.pdf) führt EnergyManager2 im Inhaltsverzeichnis (S. 57), der gelesene Text enthielt den Abschnitt nicht.
- [LoxWiki](https://loxwiki.atlassian.net/wiki/spaces/LOXEN/pages/1358594276/Energy+manager): nur eine Frage, kein Inhalt.
- **Bekannte Fehlschaltungen: nicht belegt.** Die Foren-Threads waren für Claude nicht abrufbar (Site-Fehler). Nur die Titel sind bekannt, Inhalt [ungeprüft]:
  - [Energiemanager schaltet manchmal falsch](https://www.loxforum.com/forum/german/software-konfiguration-programm-und-visualisierung/419923-energiemanager-schaltet-manchmal-falsch)
  - [schaltet umverständlich ein/aus](https://www.loxforum.com/forum/german/software-konfiguration-programm-und-visualisierung/473072-energiemanager-schaltet-umverst%C3%A4ndlich-ein-aus)
  - [berechnet die überschüssige Energie nicht korrekt](https://www.loxforum.com/forum/german/software-konfiguration-programm-und-visualisierung/469597-der-energiemanager-berechnet-die-überschüssige-energie-nicht-korrekt)
  - [gibt zu viel Überschuss frei](https://www.loxforum.com/forum/german/software-konfiguration-programm-und-visualisierung/442348-pv-%C3%BCberschussladen-energiemanager-gibt-zu-viel-%C3%BCberschuss-frei)
  - [Energiemanager und Speicher](https://www.loxforum.com/forum/german/software-konfiguration-programm-und-visualisierung/424652-energiemanager-und-speicher)
  - [falsche Last am Ausgang L1](https://www.loxforum.com/forum/german/software-konfiguration-programm-und-visualisierung/431538-energiemanager-gibt-falsche-last-am-ausgang-l1-aus)
  - [Neuer Energiemanager - Recalc?](https://www.loxforum.com/forum/german/software-konfiguration-programm-und-visualisierung/368659-neuer-energiemanager-recalc)
  Kann der Betreiber im eigenen Browser öffnen, falls gewünscht.

## Abgleich mit unseren dunklen Flanken
### Was O64266 mit dem Vorzeichen macht
`IF(I3==1;MIN(I1;0);IF(I2<I4;I1;IF(I1<0;0;I1)))` mit I1 = Reg 842. Annahme aus F76: + = Ladung, - = Entladung.
| Zweig | Entladung | Ladung | Was der EM laut Doku daraus liest |
|---|---|---|---|
| Abend (ab 180 min vor Sonnenuntergang) | Durchgereicht, negativ | 0 | Entladung = „Ladung" = Überschuss |
| Tag, SOC < MinSoc | Durchgereicht, negativ | Durchgereicht, positiv | Beides verkehrt |
| Tag, SOC ≥ MinSoc | 0 | Durchgereicht, positiv | Ladung = „Entladung", mindert Überschuss |

Die Notiz im Baustein spricht von „negativer Ladeleistung", ging also von der Doku-Konvention aus. Der Eingang liefert laut F76 die umgekehrte. Die Absicht „Verbraucher vor 100 % freigeben" wird dann in ihr Gegenteil verkehrt. [wahrscheinlich]

### Nachrechnung mit dem Modell aus „Wahrscheinlich"
g = Netz (+ Bezug), a = Akku (+ Entladung), IL = 25611, Werte aus F76 (10-/30-min-Rohwerte, nicht der Schaltaugenblick). Schwelle 1,5 kW. „Verdrahtet" = Spwr wie in der Datei, „Korrigiert" = Spwr nach Doku-Vorzeichen.
| Flanke | g / a / IL | Reserve 6 kW? | A verdrahtet | A korrigiert | Passt |
|---|---|---|---|---|---|
| a 14.10. 06:23 | -0,01 / 1,17 (F76-Annahme 3,1) / 4,93 | ja, SOC 42 | 0,11 (2,04) | -2,23 (-4,16) | Verdrahtet nur mit a = 3,1 |
| a 16.10. 06:10 | 0,34 / 3,14 / 4,08 | ja, SOC 59-50 | 0,88; ohne Reserve 6,88 | -5,40; ohne Reserve 0,60 | Keine mit Reserve; verdrahtet ohne Reserve |
| b 19.10. 17:05 | 0,25 / 6,04 / 0,60 | nein, SOC 97 | **6,39** | -5,69 | **Nur verdrahtet** |
| b 19.10. 18:56 | 0,05 / 0,59 / 3,09 | nein | 3,63 | 2,45 | Beide |
| b 22.10. 18:11 | 2,95 / 0 / 0 | nein | -2,95 | -2,95 | Keine |
| b 23.10. 18:05 | 6,5 / 0 / Wallbox 5,7 | nein | -0,80 | -0,80 | Keine |
| b 23.10. 19:06 | 7,3 / 0 / Wallbox 5,7 | SOC 97-93 | -1,60 | -1,60 | Keine |

Gegenprobe 23.10. 16:03 (Start „echt", F76 Offen 3): Bei Sonnenuntergang um ~18 Uhr lag das schon im Abendzweig [wahrscheinlich], die Ladung wurde also auf 0 gesetzt. A = 0,98 + 1,26 = 2,24, sofern SOC ≥ 95 (Stunde 86 → 97). Diese Flanke beweist daher nicht „+ = Ladung" im EM und widerspricht der Doku nicht.

### Halten und Ausschalten
| Fall | Messung F76 | Regel Netzbezug > 5,4 kW nach MinRt |
|---|---|---|
| 15.10. SG bis 19:01 | Bezug +3,4 bis +5,0 | Stets unter 5,4, bleibt ein. Passt |
| 23.10. 16:03-16:49 | Wallbox, Bezug 8-9 kW | Aus genau zum MinRt-Ende (45,6 min). Passt |
| 45-min-Phasen | Kurzer Impuls | Halten durch MinRt, wie F76 |

### Bewertung der Vermutungen aus F76
- **Muster a (morgens, „IL6 zählt als verfügbar"): gestützt, aber nicht bewiesen und in F76-Form nicht ausreichend.** `hasActual true` zeigt, dass der EM IL6 als Istwert führt. Mit richtigem Vorzeichen bleibt 16.10. aber auch ohne Reserve bei 0,60 kW, unter der Schwelle. F76 rechnet mit 4,93 - 3,1 auf 1,8, das gilt nur für 14.10. Mit verdrahtetem Vorzeichen kommt der Akku dazu statt ab, das erklärt den Einschaltwunsch besser. Die Reserve von 6 kW passt nur knapp. Ob sie so wirkt, ist offen. [Vermutung]
- **Muster b (abends, „Lastsprung oder Vorzeichen im Abendzweig"): Vorzeichen für 19.10. 17:05 gestützt, Lastsprung bleibt für 22.10. und 23.10.** Dort war der Akku 0, das Vorzeichen spielt keine Rolle. Wallbox-Lastsprung bzw. kurz fallender Bezug ist möglich, mit den vorhandenen Werten aber nicht belegbar. [Vermutung]
- **Offen 3 aus F76 (Vorzeichen Spwr): Doku-Teil geklärt, negativ = Laden.** Damit ist die Formel ein Vorzeichenkandidat.

## Noch zu prüfen (nur Lesen)
1. Spwr im Baustein während einer echten Entladung ablesen (`control_state`, Zustand `Spwr`) und mit Akku-Zähler vergleichen. Das entscheidet Kernaussage 2 in einem Schritt.
2. F76 Offen 1: Gpwr, Spwr, loads feiner über eine SG-Flanke mitschreiben, vor allem für 22./23.10.-Muster.

Falls Spwr bestätigt falsch herum ist, wäre die Korrektur eine der Betreiber-Entscheidung mit Backup und Skill `loxone-xml-umbau`. Nichts umgesetzt. Bausteine: [Energiemanager](https://www.loxone.com/dede/kb/energiemanager-2/).