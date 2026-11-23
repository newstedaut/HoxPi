# F59 Abschluss: Loxone-Raumregelung und Takten (02.11.2026, nur gelesen)

Nichts an Anlage, Loxone oder Pi geändert. Alles unten sind Vorschläge, der Betreiber entscheidet.
Messbasis: Volllogger-Kopien `[lokaler Pfad]` bis `2026-11-02.csv` (dazu `f54_pi_2026-11-01.csv`, `f54_pi_2026-11-02.csv`), 24.10. 00:00 bis 02.11. 09:55, 2.718 Zeilen, 5-min-Raster, Heizlauf = 25611 > 0,5 kW und Mehrheit 1539 = 1. Volle Tage: 24.10. bis 01.11. Rechnung nur im Speicher, kein Skript abgelegt.
Projektdatei: `[lokaler Pfad] Config\Projects\Fam der Betreiber UMBAU.Loxone` (01.11. 23:36; laut F67 noch nicht im Miniserver, die genannten Werte decken sich aber mit live, soweit gelesen).

## Ergebnis
1. **Eine offizielle Loxone-Empfehlung „Ventile offen gegen Takten" gibt es in den gelesenen Seiten nicht** [sicher für diese Seiten]. Loxone nennt nur Einschaltschwelle Sot, Mindestlaufzeit MinHr und die daran hängende Mindestöffnung. „Ventile offen, Kurve senken" ist Forenmeinung ohne Messreihe [sicher].
2. **Die üblichen Hebel gelten bei uns schon oder bringen nach unseren Messungen nichts** (Tabellen unten). 71 Heizläufe an 9 vollen Tagen = 7,9/Tag, 34 min/Lauf, 1,02 kWh_el/Lauf [sicher]. Takten kostet laut F63 nur ~1-2 % des Heizstroms [wahrscheinlich]. Am Takt ist wenig zu holen.
3. **Neuer Befund: 1490 hat zwei Stufen, rund 2 K auseinander, nach Uhrzeit** [Stufe und Zeiten sicher, Umrechnung Vermutung]. Von 23 bis 07 Uhr steht 1490 bei gleicher Außentemperatur höher als von 10 bis 21 Uhr. Das erklärt die schwache Regression aus F66/MD-17 (R² 0,28-0,52) besser als eine allgemeine Raumkorrektur [wahrscheinlich]. MD-17 nannte nachts +1,0 K; das dürfte der Mittelwert über die Stufe sein [wahrscheinlich]. 57 % der Heizlauf-Zeilen und 49 kWh_el liegen auf der hohen Stufe [sicher].
4. **Einziger durch Messung gestützter Hebel: diese Stufe klären und, wenn sie unnötig ist, wegnehmen** (V1, V2). Das zielt auf die Vorlauftemperatur, nicht auf die Startzahl. Fraunhofer fand Effizienz-Zusammenhänge nur bei den Heizkreistemperaturen.

## Quellen
Heute gelesen = per WebFetch über ein Auszugsmodell abgerufen; Zitate sind daher nur so genau wie der Auszug.

| # | URL | Was steht dort | Gelesen |
|---|---|---|---|
| 1 | https://www.loxone.com/enen/kb/climate-controller/ | MinHr vor Standby; „Minimum openings ... are ensured"; Sot = mittlere Ventilöffnung; MaxTp 0 = aus. Takten kein Thema | ja, heute |
| 2 | https://www.loxone.com/enen/kb/irc-v2/ | Mindestöffnung unter der Schwelle bis Ablauf Mindestlaufzeit; Pwm 0 = automatisch, 10-60 min; ϑd = Heiz/Kühl-Umschaltgrenze; keine Ventil-Hysterese | ja, heute |
| 3 | https://www.loxone.com/dede/kb/intelligente-raumregelung/ | Dasselbe auf Deutsch, Mindestöffnung ohne eigenen Zahlenwert | ja, heute |
| 4 | https://www.loxone.com/enen/kb/hvac-controller/ | Sot gegen arithmetisches Mittel aus Öffnung × Raumgröße, Standard 30 %; minO 300 s | ja, heute |
| 5 | https://www.loxone.com/enen/kb/zoned-heating-comfort/ | Stetige Antriebe sollen „short cycling" vermeiden; Schwelle 30 % startet Kessel/Luft-WP; zu Mindestlaufzeit nichts | ja, heute |
| 6 | https://www.loxone.com/enen/?p=1272 | Vorlauftemperaturregler: ohne Bedarf AQf = Min; Str wirkungslos bei allen Raumreglern am Controller; I hebt Raumsoll im Heizen, I = 0 nimmt das weg; Standard S 0,5, N 0 | ja, heute |
| 7 | https://knx-user-forum.de/forum/%C3%B6ffentlicher-bereich/knx-eib-forum/knx-einsteiger/1539375-fussbodenheizung-w%C3%A4rmepumpe-knx | Stellantriebe „möglichst weit offen", Kurve in 1-K-Schritten senken; keine Messwerte | ja, heute |
| 8 | https://www.energiesparhaus.at/forum/70145 | Mehrheit gegen Einzelraumregelung bei FBH + WP, eine Gegenstimme; Meinungen | ja, heute |
| 9 | https://www.energiesparhaus.at/forum-lwp-taktet-und-taktet-und-taktet/69988 | Vaillant, alle Kreise offen, trotzdem Start alle 30 min, 7-8 min Lauf; Ursache Mindestleistung (Forum, nicht verifiziert) | ja, heute |
| 10 | https://www.energiesparhaus.at/forum-hoval-ultrasource-lwp-allgemeiner-austausch-und-anlage-optimieren/56645_2 | Hoval: Stellantriebe abgeschraubt für ~840 l/h; 10-20 Takte/Tag; Test Einschaltdiff. 4 K ohne Ergebnis | ja, heute |
| 11 | https://www.energiesparhaus.at/forum-ueberdimensionierte-waermepumpe/24763 | Heizfenster: Takte „von Anfangs 30 auf 12-13"; Forum 2011, Einzelfall | ja, heute |
| 12 | https://www.idm-energie.at/en/heat-pump-control/zone-control/ | iDM-Artikel: Zonen senken Starts 10-20 %, zu „Zonen offen" und Mindestabnahme nichts. Allgemeintext ohne Messbeleg, widerspricht den Foren | ja, heute |
| 13 | https://www.idm-energie.at/en/heat-pump-control/on-off-control/ | Mindestlauf 2-5 min, Mindeststillstand 3-10 min, max. 4-6 Starts/h | ja, heute |
| 14 | https://www.ise.fraunhofer.de/content/dam/ise/de/documents/projekte/WP-QS_Schlussbericht.pdf | 90 % unter 5.500 Starts/a; Auslegung allein entscheidet nicht; Effizienz nur mit Heizkreistemperatur korreliert | ja, heute |
| 15 | https://forum.buildhub.org.uk/topic/43478-ashp-weather-compensation-and-zoning | Einzelne offene Zone taktet eher; Puffer/Volumiser; Erfahrungen, keine Messreihe | ja, heute |
| 16 | https://www.loxone.com/dede/wp-content/uploads/sites/2/2021/10/1701_Structure-File.pdf | demandHeat, threshold, stage, currentStatus | Vorlauf (`FUND_Loxone_Klimacontroller_Schwelle_20261101.md`), heute nicht neu |
| 17 | https://iifiir.org/en/fridoc/theoretical-and-experimental-investigation-of-startup-and-shutdown-135447 | Luft-WP verlieren durch Takten ~1-2 % | Vorlauf (`FUND_Ueberdimensionierung_Takten_Puffer_20261101.md`), heute nicht neu |

Nicht erreichbar heute (nichts daraus verwendet): Loxforum 310713, 214228, 407501; https://www.loxone.com/dede/blog/einzelraumregelung-fussbodenheizung-stellantrieb/ ; https://www.loxone.com/dede/?p=337740 . Ohne Inhalt zum Thema: https://community.simon42.com/t/fussbodenheizung-bei-waermepumpe-steuern/34105?page=2 .

**Korrekturen an den Vorläufer-FUND:**
- „Loxone-Mitarbeiter hält dagegen": auf energiesparhaus 70145 nicht gefunden [sicher für diese Seite]; 58625 heute nicht gelesen.
- „Loxone rät bei Luft/Wasser mit Puffer vom Auto-Wechsel ab": auf der EN-Seite nicht vorhanden, nur Teil 1 aus der ES-Fassung [sicher für EN].
- „Ausgang H nicht zur WP verdrahtet, MinHr wirkungslos" (Teil 1/2): widerlegt, `ANALYSE_F59_Quelle_1490_20261101.md` [sicher].

## Abgleich mit unserer Kette
Kette [sicher als Dateiinhalt]: Raumregler → Klimacontroller UG (`OutHeat1`) → Select Multiplexer „Sollwert Heizen 1490", Input1 = Heatmixer2 AQf → Formel Ofen-Nachlauf → Modbus-Aktor Reg 1490. Danach 1520 = 1490 + 07-001, Stopp bei RL = 1520 + 3,0 K, Start ~16 min nach RL < 1520 − 1,0 K (F54).

Live 02.11. 14:41 UTC (Loxone-MCP): demandHeat 36, threshold 30, stage 2, mode 2, 48-h-Außen 5,03 °C, AQf 29,89 °C.

| Raum | Soll jetzt | Ist | demand |
|---|---|---|---|
| Bad | 23,5 | 23,1 | 1 |
| WC UG | 22,5 | 22,0 | 1 |
| Wohnzimmer | 21,5 | 21,5 | 1 |
| Zimmer OG 1 | 21,0 | 21,2 | 1 |
| Zimmer OG 2 | 20,5 | 20,6 | 1 |
| Büro | 18,5 | 22,1 | 0 |
| Technikraum | 19,5 | 20,1 | 0 |
| Hütte | 12,0 | 18,1 | 0 |

Zimmer OG 1 und Zimmer OG 2 melden demand 1 über Soll: passt zur Mindestöffnung während MinHr oder zu I [Vermutung].

**Was bei uns schon so ist:**
| Best Practice | Stand | Beleg | Sicherheit |
|---|---|---|---|
| Mindestlaufzeit | schon so: MinHr 60 min | Projektdatei Z. 13173; wirkt laut F81 (Blöcke < 60 min 33/65 → 3/33) | sicher |
| Heizkreis-Mindestanforderung | schon so: Sot 30 % | Z. 13169, live threshold 30 | sicher |
| Mindestöffnung | schon so, kein eigener Parameter, folgt aus Sot + MinHr | Quellen 1-3 | wahrscheinlich |
| Kein Heiz/Kühl-Wechsel im Winter | schon so: mode 2, 48-h-Mittel | live; F72 | sicher |
| Kein kurzes PWM | schon so: TPWM ohne Wert (0 = automatisch, 10-60 min) | Z. 6688 Bad, andere Räume nicht einzeln geprüft | wahrscheinlich |
| Flache Wetterkurve, 1-K-Schritte | schon so: S 0,3, nicht 0,9; Projektanweisung ist hier veraltet | Z. 13231; F66 | sicher als Datei |
| Heizfenster | schon so durch 1490 = 0: 55 % der Zeit (MD-17), Blockdauer Median 145 min (eigene Zählung) | Volllogger | sicher |
| Breite Hysterese | schon so: 3,0 + 1,0 K + 15 min am Kälteregler | F65 | sicher |
| Überhöhung senken | läuft: 07-001 = 2,0 K, Abnahme 07.11., hier kein Urteil | F55 | sicher |

**Starts je Tag (eigene Zählung):**
| Tag | AT °C | Heizläufe | Laufzeit min | 1490 = 0 % | Raum 1510 °C | kWh_el Heizen |
|---|---|---|---|---|---|---|
| 24.10. | 5,8 | 7 | 230 | 51 | 22,05 | 6,9 |
| 25.10. | 4,6 | 8 | 330 | 40 | 21,51 | 9,9 |
| 26.10. | 6,5 | 7 | 260 | 39 | 21,84 | 7,9 |
| 27.10. | 7,8 | 5 | 205 | 67 | 21,79 | 6,4 |
| 28.10. | 8,5 | 7 | 235 | 56 | 21,39 | 7,1 |
| 29.10. | 7,3 | 8 | 220 | 40 | 21,18 | 6,6 |
| 30.10. | 6,8 | 11 | 365 | 17 | 21,34 | 11,0 |
| 31.10. | 7,1 | 7 | 280 | 47 | 21,67 | 8,2 |
| 01.11. | 4,7 | 11 | 290 | 29 | 21,49 | 8,6 |

- r(Starts, 1490 = 0) = −0,92; r(Starts, AT) = −0,49; r(kWh_el, 1490 = 0) = −0,79; r(Raum, 1490 = 0) = +0,45; bereinigt um kWh_el −0,83 [sicher als Rechnung, n = 9]. Die Richtung ist offen: warme Räume erzeugen 1490 = 0, nicht umgekehrt [wahrscheinlich]. Kein Beleg, dass eine höhere Sot Starts spart.
- Änderung von 1490 im Lauf bestimmt die Laufzeit nicht: von 68 Läufen ohne Loxone-Schnitt nur 5 mit ≤ −1 K (Median 30 min, sonst 35 min), r = 0,14 [sicher, n klein]. Darunter ist ein echter Kurzlauf: 01.11. 02:35, 10 min, −2,6 K.
- Lauf nach Loxone-Pause: Median 35 min (n = 19), sonst 35 min [sicher]. Längere Vorpause ergibt keinen längeren Lauf.
- Läufe ≤ 20 min: 15 von 77. Davon 8 mit Loxone-Ende, 7 ohne, darunter 02.11. 02:15 und 04:40 direkt vor Abtauung [sicher im Raster]. Die Gruppen sind grob, WW-Übergänge sind nicht getrennt.

**Die zwei Stufen (neu):** Aus 1490 und 1477 rückgerechnetes Raumsoll mit der Näherungsformel aus `FUND_F66_Heatmixer2_Parameter_20261101.md` (S 0,3; Formel nachgebildet, nicht offiziell [Vermutung]).

| Rückgerechnetes Raumsoll | 23,5 | 24,0 | 24,5 | 25,0 | 25,5 | andere |
|---|---|---|---|---|---|---|
| Zeilen mit 1490 > 0, ohne 24,0 | 210 | 493 | 189 | 25 | 632 | 10 |

| Uhrzeit | Zeilen hohe Stufe (≥ 24,75) | Zeilen niedrige Stufe |
|---|---|---|
| 23-07 | 486 | 4 |
| 07-10 | 145 | 186 |
| 10-21 | 6 | 687 |
| 21-23 | 21 | 24 |

- Abstand 25,5 zu 23,5-24,0 = 1,5-2 K Raumsoll. Das liegt in der Größe von `PrevInc` = 2 (Z. 13225, Doku-Parameter I) [Vermutung, kein Ursachenbeleg].
- Gegenrichtung zur Erwartung: Wenn Räume in Komfort gehen, fällt 1490, wenn sie in Eco gehen, steigt es [sicher als Zeitmuster]. Warum, ist nicht geklärt. Laut Quelle 6 zählt je Raum ein Vorlauf, ausgegeben wird der höchste; das erklärt die Richtung nicht direkt.
- Nachts ist die Luft kälter, die höhere Stufe trifft also die schlechtere Arbeitszahl (F68: AZ steigt mit AT) [wahrscheinlich].

## Vorschläge (ohne Umsetzung)
Regel aus `ENTSCHEIDUNGEN_offen.md`: eine Änderung je Woche. Vor Loxone-Änderung Backup und Skill `loxone-xml-umbau`. Loxone-Doku: [Vorlauftemperaturregler](https://www.loxone.com/dede/kb/vorlauftemperaturregler/), [Intelligente Raumregelung](https://www.loxone.com/dede/kb/intelligente-raumregelung/), [Klima Controller](https://www.loxone.com/dede/kb/klima-controller/), [Monoflop](https://www.loxone.com/dede/kb/monoflop/), [Formel](https://www.loxone.com/dede/kb/formel/), [Analog-Multiplexer](https://www.loxone.com/dede/kb/analog-multiplexer/). Nur die IRR-Seite heute geöffnet, die übrigen Slugs ungeprüft.

| # | Was | Erwarteter Effekt und Beleg | Risiko | Rückweg | Kollision F55 / F67 |
|---|---|---|---|---|---|
| V1 | Nur lesen: Loop schreibt um 06:55-07:20, 09:25-09:40 und 21:00-22:30 an je 2 Tagen AQf, tempTarget, demand aller Räume, demandHeat mit | Klärt die Stufe. Beleg: Zeitmuster oben. Entscheidet, ob V2 oder V3 der richtige Hebel ist [sicher als Prüfweg] | keins | entfällt | nein / nein |
| V2 | Test `PrevInc` HC1 2 → 0 (Z. 13225), nur wenn V1 ihn als Ursache stützt | Hohe Stufe ~2 K tiefer. 49 kWh_el in 9,4 Tagen × 2,5 %/K × 2 K ≈ 2 kWh_el/Woche [Vermutung, Faustregel aus F63]. Vermutlich fallen auch die Sprünge weg (20 abwärts in 9,4 Tagen; 5 Läufe mit ≤ −1 K) | Räume morgens kälter, weniger Reserve bei Frost (unter 2,9 °C an 1477 keine Daten). Abbruch: Raum mit Ventil offen > 0,5 K unter Soll | Wert wieder 2 | **ja F55**: erst nach Abnahme 07.11., da 1490 die Bezugsgröße ist. **ja F67**: auf der Datei aufbauen, die dann im Miniserver ist |
| V3 | Test Bad Komfort 23,5 → 22,5 °C | Bad ist höchster Sollraum, laut Quelle 6 setzt der höchste Raum den Vorlauf. 1 K Raumsoll ≈ 1,25 K 1490 (rückgerechnete Tabelle). Erwartung tagsüber ~−1,2 K, sonst ist die These widerlegt. Bad trieb am 22.10. die Heizphasen (`ANALYSE_Raumventile_Heizkurve_Winter_20261022.md`) [wahrscheinlich] | Bad kühler; Komfortfrage für der Betreiber | Wert wieder 23,5 | **ja F55**, gleicher Grund; F67 nein (App-Wert, kein Umbau) [Vermutung, Weg nicht geprüft] |
| V4 | Nur prüfen, nichts verstellen: Liveview, ob Eingang I3 (Kurzlauf-Schutz) der Formel am Miniserver Impulse bekommt | Offen aus `ANALYSE_F54_Monoflop_Gegenprobe_20261031.md`. 8 Läufe ≤ 20 min mit Loxone-Ende in 9,4 Tagen, 2 davon Sonderfälle (29.10. 10:50, 01.11. 20:15). Nutzen klein, Takt kostet ~1-2 % [wahrscheinlich] | keins | entfällt | nein / nein |
| V5 | Nur lesen: demandHeat und stage je Pause mitschreiben | Einziger bisher fehlender Beleg zu „Ventile offen": r streut bei gleicher Luft 7,1-11,2 K/h, Pause hängt mit r = 0,86 an der Rate (F54). Vorhandenes `[lokaler Pfad]` hat nur 7 Zeilen vom 07.09. | keins | entfällt | nein / nein |

**Bewusst nicht vorgeschlagen:**
| Idee | Warum nicht |
|---|---|
| Stellantriebe dauerhaft offen, Grundlastkreise | Keine Messung bei uns, Ventilreihe nur WZ 12.-14.10. (69 % offen, Hub ~50 %). Quelle 9: alle Kreise offen, taktet trotzdem. Quelle 10 und F63: mehr Laufzeit, Zyklen nicht weniger. Erst V5 |
| Sot senken oder heben | Kein Kausalbeleg (siehe r oben). Senken verkleinert die Pausen, Heben riskiert Raumtemperatur. Nutzen höchstens Anteil an 1-2 % |
| Rampe auf 1490 | Nur 5 von 68 Läufen betroffen, Wirkung auf Laufzeit nicht nachweisbar. Die Sprünge wären mit V2 ohnehin weg |
| Hysterese vergrößern | Kälteregler wird nie beschrieben. +1 K Stopp: Hub 4,5 → 5,5 K, ~18 % weniger Starts ≈ 0,2-0,4 % Heizstrom gespart, aber RL im Mittel ~+0,5 K ≈ −1,25 % [Vermutung, Rechnung] |
| Monoflop verlängern | Wirkung des Schutzes live nicht belegt, erst V4 |
| Heizfenster, größerer Puffer, Steilheit ändern | Fenster schon so; Puffer F63; Kurve laut `ANALYSE_Raumventile_Heizkurve_Winter_20261022.md` nicht zu niedrig, eher ~1 K Luft (Stand 22.10., rechnete noch mit 0,9), Rest siehe V2/V3 |

## Was bringt uns das
F59 kann zu: Am Takt selbst ist kein Vorschlag messbar lohnend. Offen bleibt ein kleiner Effizienzhebel von grob 2 kWh_el/Woche [Vermutung] und ein unverstandenes Stufenmuster in 1490, das auch den Zwilling betrifft (1490 nicht als Funktion der Außentemperatur allein modellieren).

## Offen
- Ursache der Stufe: V1. Vorschlag: eigene Katalogzeile, F59 selbst damit abgeschlossen.
- Volumenstrom bei zugefahrenen Antrieben gegen ~840 l/h (Quelle 10, Nutzerangabe): nicht geprüft.
- Zählung Loxone-Enden uneinheitlich: F81/Katalog 2 von 70, MD-16 6 von 70, hier 9 von 77 (6 Ende + 3 im Lauf, grobes Raster). Für die Vorschläge unerheblich, für den Zwilling zu klären.
- Live `currentStatus` 257 bei stage 2: laut Bitliste aus FUND Heizen Stufe 1 + Lüfternachlauf; passt nicht glatt zu stage 2, nicht geklärt.
- Projektanweisung nennt Steilheit 0,9, Datei und MD-17 zeigen 0,3: Text anpassen, wenn der Betreiber zustimmt (hier nicht geändert).
- Nur 9 volle Tage, AT 4,6-8,5 °C Tagesmittel, 07-001-Wechsel mittendrin (31.10. 22:01). Frost fehlt.

## Stichproben zum Gegenlesen
1. https://www.loxone.com/enen/kb/hvac-controller/ : „The arithmetic mean of the demand (degree of opening * room size)"
2. https://www.loxone.com/enen/kb/climate-controller/ bei MinHr: „Minimum openings of the room controllers are ensured."
3. `[lokaler Pfad]`, Zeile 09:35: 1490 = 293 (davor 09:30: 316), 1477 = 70. Dazu Projektdatei Z. 7136: Büro `Entry From="570" To="1140"` (09:30-19:00).