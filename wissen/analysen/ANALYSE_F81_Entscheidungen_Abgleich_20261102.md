# F81 - Abgleich ENTSCHEIDUNGEN_offen.md gegen Stand 02.11.2026 09:10 (nur gelesen, an Anlage und Loxone nichts geändert)
**Kern:** Von den 5 Einträgen muss der Betreiber nur noch einen beantworten (Verbrühschutz). Punkt 1 und 2 sind seit 23.10. umgesetzt, die Datei führt sie im Kopf aber noch als offen. Punkt 3 wartet auf die Abnahme 07.11. Die offenen Fragen stehen heute woanders (Abschnitt 2).
Eigene Zählung: `[lokaler Pfad]`, `f81_b.py` über `[lokaler Pfad]` (5-min-Raster, 01.10. bis 02.11. 01:55; 02.11. morgens nur aus dem Journal). Die Zeiträume sind nicht wettergleich: 01.-23.10. AT 11,5 °C, 24.-31.10. AT 6,8 °C.

## 1. Einträge der Datei
| Nr / Titel | Stand in der Datei | Stand heute mit Beleg | Urteil | Sicherheit |
|---|---|---|---|---|
| 2 WW-Morgenladung -> Nachmittag | Kopf: Ja/Nein. Nachtrag: umgesetzt | Schaltuhr `Fam der Betreiber UMBAU.Loxone` Z. 16252 ff.: From 780 To 960 = 52. 1497 um 04:30-07:30: 01.-23.10. 813 von 828 Zeilen 52; 24.-31.10. 274 von 288 Zeilen 50 (f81_a). Morgenstarts 5,8 -> 3,8/Woche (24.10., 27.10., 29.10., 01.11., 02.11. 05:41; 29.10. und 01.11. mit 57 = Kick; F74 stuft den Kick 01.11. als Drift ein). Direkter Übergang Heizen -> WW morgens 1,5/Woche -> 2 in 9 Tagen, plus wohl 02.11. Zahl korrigiert: F68 ~1,3-1,5 kWh_el/Woche statt ~2 + 0,7 (`ANALYSE_F68_...` Abschnitt 4.6), Rechnung, keine Messung danach | **erledigt** (Verschiebung). Abnahme nur teilweise erfüllt: Ladungen und Abbrüche morgens nicht null. **Offen mit neuen Zahlen** ist nur die Folgefrage Zusammenlegen, die **wartet auf F70/MD-20** | Umsetzung [sicher], F68 [wahrscheinlich]. Komfort-Rückmeldung von dir nicht gefunden |
| 2a PV-Teil von Punkt 2 (PV-Boost 57) | "Winterdeckel aufgehoben (PV-Boost 57)" | Hebt seit 24.10. nicht mehr an: 27545 = 1 bei 1497 = 50 seit 26.10. (`ANALYSE_F76_...` Ergebnis 4), I2 auf Merker.Q (OR 02.11. 07:10) | **überholt**, siehe 2.3 | Messung [sicher], Ursache [wahrscheinlich], Liveview fehlt |
| 3 07-001 -> 2 K | Nachtrag: gesetzt 31.10. 22:01; Abnahme 07.11. | Live 30684 = 20 (gelesen 02.11. 09:05), in Whitelist, also "über HoxPi nicht ohne Weiteres" überholt. 25.10./01.11.: Abstand Laufende 8,70 -> 7,60 K, Raum 21,51 / 21,49 °C, Starts 9 -> 12, min/Start 37,8 -> 27,9, AZ 4,30 -> 4,11 (Katalog F55, OR 02.11. 04:00; `ANALYSE_F55_Zwischenstand_Tag1_20261101.md` Z. 55, 83) | **wartet auf Messung** (07.11.). Prognose COP +2-3 % bisher nicht sichtbar, eher leicht schlechter. **Abnahmetext falsch:** HK1-Ist ist Reg 1513, nicht 18760 (F55); "< 2 % unter Soll" ist unerreichbar, schon die Referenz liegt bei 69-76 % | Abstand [sicher], Raum [wahrscheinlich], AZ [wahrscheinlich, 1 Tag] |
| 5 Legionellen-Zähler Start 0 oder 10 | Ja/Nein | Start 0, Pflichtlauf 25.10. entfiel planmäßig (`loop_journal.md` Z. 846); Pflichtlauf 01.11. bestanden, Reset 15:54 (`ANALYSE_F57_...` Z. 105), live 0,68 d (02.11. 09:04) | **erledigt** | [sicher] für Reset und Wert |

## 2. Offen, aber nicht in der Datei (alles Vorschläge, nichts beschlossen; vor jedem Loxone-Umbau Backup und Skill `loxone-xml-umbau`)
| # | Thema | Alt -> Neu | Nutzen | Risiko | Rückweg | Doku |
|---|---|---|---|---|---|---|
| 2.2 | Vorzeichen Energiemanager I1 in O64266 (F78) | I1 = Reg 842 -> -Reg 842, **erst nach Entladungs-Ablesung** | Dunkle Flanken weniger, betrifft alle Lasten (WP, Wallbox, Heizkörper). Derzeit 0 kWh bei 1497, weil 2.3 tot ist; danach max. 2,6, eher 1-2 kWh_el/Woche [Vermutung] | Falsch, wenn 842 doch anders liegt. 22./23.10. erklärt es nicht | Formel zurück | [Energiemanager](https://www.loxone.com/dede/kb/energiemanager-2/) |
| 2.3 | I2 "WW-Soll Manager" (F76) | Merker.Q -> Merker.AQ, ebenso Klimacontroller Cool-/HeatAvailable prüfen | PV-57 wieder da: 3,5-5 kWh_el/Woche an Sonnentagen, im November klein [Vermutung]. Nutzen von 57 °C an sich fraglich (F69) | Dunkle Flanken kommen zurück, daher erst 2.2; Liveview fehlt | Merker.Q | [Merker](https://www.loxone.com/dede/kb/) |
| 2.4 | SG nur mit echter PV (F74) | I2 über UND mit Ppwr >= 1,5 kW | Max. 2,6, eher 1-2 kWh_el/Woche [Vermutung], nur nach 2.3 | Halbe Wolkentage fallen weg | I2 direkt | [Schwellwertschalter](https://www.loxone.com/dede/kb/schwellwertschalter/), [UND](https://www.loxone.com/dede/kb/und/) |
| 2.5 | Monoflop Ofen-Sperre (F77) | 28800 s -> 3600 s, oder nichts tun | Umwälzen bleibt am Abend; kein Energiehebel (0,21 % kWh_el) [sicher] | Evtl. ein Kurzlauf je Stunde | 28800 s | [Monoflop](https://www.loxone.com/dede/kb/monoflop/) |
| 2.6 | Legionellen Reihenfolge (F60) | Stab erst nach WP-Ladung (A'), oder WP 57 + Stab-Rest (B) | Netto ~6,7 -> ~4,0 -> ~2,6 kWh_el/Woche [wahrscheinlich]. **Mein Vorbehalt:** 01.11. war Feiertag, die Schaltuhr hat für Sonntag keinen 52-Eintrag, wohl aber für Feiertag; die Parallelladung kann also Sonderfall sein [Vermutung]. Erst Pflichtlauf So 08.11. ansehen | Ablauf komplexer | Stand 25.10. | [Schaltuhr](https://www.loxone.com/dede/kb/schaltuhr/) |
| 2.7 | Heizkurve S (F66) | S 0,3 lassen oder anheben; kein Zielwert belegt | Frost: ~37-38 °C bei -15 °C statt 40 [wahrscheinlich]. Erst bei Frost entscheiden (MD-21) | 0,9 wäre bei 6 °C ~37-39 °C, zu hoch | Parameter zurück | [Vorlauftemperaturregler](https://www.loxone.com/dede/kb/vorlauftemperaturregler/) |
| 2.8 | Zirkulation 20-min-Sperre V1 (F64) | Keine Sperre -> 20 min nach Puls | 0,3-0,7 kWh_th/Tag, gerechnet ~0,7-1,6 kWh_el/Woche [Vermutung] | Warmwasser an der Zapfstelle später | Baustein raus | [Monoflop](https://www.loxone.com/dede/kb/monoflop/) |
| 2.9 | 07-001 am 07.11. | 2 K halten oder zurück auf 3 K (30684 = 30) | Siehe Punkt 3 | - | 30684 = 30 | - |

Vom Tisch, nicht mehr vorlegen: Monoflop Kurzlauf 900 -> 1800 s (greift live nicht, `ANALYSE_F54_Monoflop_Gegenprobe_20261031.md`); Ofenzweig ab RL >= 30 °C (zurückgezogen, F77); HV011/HV012 (Kälteregler, wird nie beschrieben); Puffer größer (F63). Sot 30 % bleibt ein Hebel, die Nachtpausen schaden aber nicht (`ANALYSE_Nachtpausen_Loxone_20261031.md` Z. 89), daher kein Vorschlag.
Neu zu 2.2 (09:07, selbst gelesen): Spwr +0,407 bei SOC 36; SOC war 07:29-08:07 noch 33 (Journal). SOC steigt bei positivem Spwr, also positiv = Laden [wahrscheinlich, stärker als OR 08:09]. Entladung weiter nicht abgelesen.
Doku-Korrekturen ohne Entscheidung: Projektanweisung "Steilheit 0,9" -> wirksam S 0,3 [wahrscheinlich]; "FBH 2 Stockwerke" -> nur UG an HK1 (`ANALYSE_F62_OG_Versorgung_20261101.md` Z. 63). Loxone-Links aus dieser Umgebung und vom PC mit HTTP 403 nicht geöffnet, Adressen aus früheren Analysen übernommen.

## 3. Vorschlag Neutext für ENTSCHEIDUNGEN_offen.md (nicht eingetragen)
```
# Offene Entscheidungen Heizung (Stand 02.11.2026)
Regel: eine Änderung pro Woche. Verlauf bis 02.11.: Backup der alten Fassung behalten.
## Erledigt
- MinHr 60 min: umgesetzt 23.10., wirkt (1490-Blöcke Median 50 -> 115 min). Läufe enden zu ~66/70 an der Hoval-RL-Schwelle.
- WW-Kalender: 13:00-16:00 = 52, morgens 50: umgesetzt 23.10. Rechnung ~1,3-1,5 kWh_el/Woche.
- Legionellen-Zähler: Start 0, Pflichtlauf 01.11. bestanden (1500 max. 61,7 °C).
## Wartet auf Messung
- 07-001 = 2,0 K (30684 = 20, seit 31.10. 22:01): Abnahme 07.11., ~30 Läufe je Band, Kennzahlen min/Start, AZ, Anteil 1513 < 1490 - 1 K gegen 32-44 %, Raum 1510. Rückweg 30684 = 30.
- Weniger WW-Ladungen (Zusammenlegen, 0-6 kWh_el/Woche, Vermutung): nach F70/MD-20.
- Vorzeichen Energiemanager I1: nach Spwr-Ablesung bei Entladung.
- Legionellen-Reihenfolge: nach Pflichtlauf So 08.11. (kein Feiertag).
- Heizkurve S 0,3: bei Frost, nach MD-21.
## Deine Antwort
1. "In Miniserver speichern" für Umbau 01.11. 23:36: bitte ausführen.
2. Verbrühschutz: Mischer an den Zapfstellen vorhanden? Wenn nein: Ziel 62 -> 61 °C. Ja/Nein
3. PV-57 (I2 Merker.Q -> Merker.AQ): im Frühjahr wieder? Erst nach Vorzeichen. Ja/Nein
4. Monoflop Ofen-Sperre 8 h -> 1 h oder lassen?
5. Zirkulation 20-min-Sperre: ~0,7-1,6 kWh_el/Woche (Vermutung). Ja/Nein
```

## 4. Was bringt uns das
- Du beantwortest statt 5 alter Ja/Nein-Fragen nur noch 5 echte, davon 2 ohne Rechenarbeit (Speichern, Mischer).
- Keine Doppelentscheidung: MinHr und Morgenladung standen noch als offen da, obwohl sie seit 10 Tagen laufen.
- Die Abnahme 07.11. scheitert nicht an einem falschen Register und einer unerreichbaren 2-%-Grenze.
- Größter noch offener Sparhebel laut Rechnung: Legionellen (bis ~4 kWh_el/Woche) und Zusammenlegen (0-6). Beides ist nicht gemessen, und nichts davon ist beschlossen. Die Entscheidung bleibt bei dir.

**Nicht belegt:** TimePump live (Wert nur aus Datei, Wirkung aus 1490-Blöcken); Mode der Schaltuhr am 01.11. (Feiertag nur aus Kalender und Eintrag gefolgert); Liveview I2; Spwr bei Entladung; dein Komfort-Urteil morgens; Einsparung von Punkt 1 und 2 nach Umsetzung (AT nicht vergleichbar). Tabellen aus F54/F55/F60/F68/F74 nicht nachgerechnet, nur übernommen.