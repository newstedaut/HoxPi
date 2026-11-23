# Stale-Register-Inventar Volllogger (R88/R90) – 23.10.2026

Orchestrator/Analyse 23.10.2026, **nur lesend**: `zcat`/`cat` der Tagesdateien `~/hoxpi_fulllog/2026-10-09 … 22` per SSH. Es gab keine Bus-Abfragen und keine Schreibzugriffe; Dienste und Crontab wurden nicht angefasst. Skripte: `or_stale_20261023.py` (→ `.out`) und `or_stale_20261023_nachtrag.py` (→ `.out`; 65535-Ereignis, X4-Slave 5).
**Fenster:** 16.10. 00:00 bis 22.10. 23:55, 2 016 Zeilen im 5-min-Raster, 555 Register (nur Modbus-UnitId 1 der Bridge). Die Vorwoche 09.–15.10. diente nur dazu, die „letzte Änderung“ zu bestimmen.
**Namen** stammen aus `WEZ_Register_offiziell_UnitId1.csv`, für fn 7 `319xx` aus `hoval_datapoints_f2_20260904/*.csv`. 177 Register haben keinen Namen in beiden Listen und sind mit „?“ markiert.

## Kurzfazit
- **Zählung (belegt):** (a) 44 immer ungültig ([Nummer]), (b) 415 über 7 Tage konstant (davon 230 plausibel: Parameter, Fehlerslots, nicht bestückte Kreise, High-Words), (c) 13 seit einem Zeitpunkt still, (d) 83 leben. Es gab **keine einzige leere Zelle** und keine Lücke.
- **Kältekreis fn 7 seit 18.10. 11:15:01 eingefroren: bestätigt, mit Einschränkung (belegt).** Eingefroren sind `31903` Lufteintritt (116), `31905` Sauggas (101), `31907` Heißgas (785), `31913` Überhitzung (318), `31917` Hochdruck (2913), `31921` Verdichter-Istdrehzahl (0) und `31919` Flag (0). Seit diesem Zeitpunkt gab es **0 Änderungen** (vorher 260–490 pro Register im Fenster). **Nicht** eingefroren sind im selben Block `31915` Niederdruck (1 792 Änderungen, 22.10. 23:55 = 800) und `31908/31909` (Spiegel von `27495/27496` „Drehzahl CP“). Sonst verlor kein Register zum 18.10. 11:15 sein Leben.
- **Echte Messwert-Leichen gibt es außerhalb von fn 7 kaum.** Fast alle konstanten „Messwerte“ gehören zu nicht vorhandenen Kreisen/Fühlern (HK2/HK3, Grundwasser/Primär, FAV, Info-Eingänge, Sonne) oder sind High-Words. Verdächtig bleiben nur `18741/18756` Volumenstrom und `18740/18758` Drehzahl Hauptpumpe, beide konstant 0.
- **R88 betrifft nicht den Volllogger.** Slave 5 sitzt am X4-Bus und wird laut ARGON (Tabelle B76–B79) vom **Hoval-Regler selbst** gepollt. „Aus dem Poll nehmen“ ginge nur über die Firmware (Tabu). Machbar ist nur, ihn aus **unseren** Auswertungen zu nehmen.

## Methode
- **(b) konstant:** genau ein Wert über alle 2 016 Zeilen. Die Bewertung „plausibel“ gilt, wenn das Register laut Liste schreibbar ist (Parameter), wenn es ein Fehler-/Info-Slot ist oder wenn der Name nicht nach Messwert aussieht. „Verdächtig“ heißt: Der Name sieht nach Messwert aus, oder es gibt keinen Namen.
- **(c) seit Zeitpunkt still:** Im Fenster gibt es Änderungen, die letzte liegt aber **≥ 24 h** vor dem 22.10. 23:55.
- **(d) lebt:** letzte Änderung < 24 h vor Fensterende.
- **Grenze:** Die Klassifikation hängt am 7-Tage-Fenster. Ein selten schaltendes Register (z. B. `1543`, letzte Änderung 13.10.) fällt in (b), obwohl es nicht tot ist.

## (a) Immer leer / ungültig – 44 Register (belegt)
| Register | Name | Wert | Bewertung |
|---|---|---|---|
| `1509` | AF2 Außenfühler 2 | 32768 | nicht bestückt, plausibel |
| `1511`, `1512` | Raum-Ist HK2/HK3 | 32768 | kein Raumfühler am Hoval-Bus (Raumregelung macht Loxone), plausibel |
| `1515`, `19610`, `19611` | Vorlauf-Ist fn2, Rücklauf-Ist fn0/fn1 | 32768 | Kreis bzw. Fühler nicht vorhanden, plausibel |
| `1524`, `1526`, `1527`, `1538` | fn 254: Soll Kühlen, Abgastemp. RS485, Umschalttemp., Wasserdruck | 32768 | über diesen Pfad nicht geliefert; Abgas bei WP ohnehin sinnlos |
| `18738` | Wasserdruck fn1 | 32768 | kein Drucksensor geliefert, plausibel |
| `18746`, `18759` | WEZ-Ist / Rücklauf WEZ fn0 | 32768 | fn0 im WEZ-Block nicht belegt (die WP liefert unter fn1 bzw. `1525/1535`) |
| `19049–19053`, `25515–25517` | Info 1–5, Info 0–10 V | 32768 | freie Eingänge, plausibel |
| `19755`, `19820` | Zirkulation, FAV Vorlauf-Ist | 32768 | nicht vorhanden |
| `27492` | Sonden-RL/Verdampferoberfl. | 32768 | bei Luft-WP nicht vorhanden |
| `27493`, `27497`, `27499`, `31705`, `31709` | WPF-Pufferfühler, Drehzahl WQP/GWP (High-Words) | 32768 | S32-Ungültig. Die Low-Words `27494/27498/31706/31710` stehen auf 0 (Klasse b) |
| `27535` | Sonneneinstrahlung | 32768 | kein Sensor |
| `19279–19283`, `31772`, `31780`, `31896`, `31898`, `31900`, `31910` | ? | 32768 | ohne Namen; bei `319xx` **Vermutung**: High-Hälften der S32-Paare von fn 7 |
| `28941–28943` | ? | 65535 | ohne Namen |

## (c) Seit einem Zeitpunkt still – 13 Register (belegt)
| Register | Name | letzte Änderung | vorher → Standwert | Änd. im Fenster | Bewertung |
|---|---|---|---|---|---|
| `31903` | Lufteintritt Außengerät (0,1 °C) | **18.10. 11:15:01** | 115 → **116** | 403 | **eingefroren** (Messwert) |
| `31905` | Sauggastemperatur | **18.10. 11:15:01** | 100 → **101** | 428 | **eingefroren** |
| `31907` | Heißgastemperatur | **18.10. 11:15:01** | 783 → **785** | 260 | **eingefroren** |
| `31913` | Sauggas-Überhitzung (0,01 K) | **18.10. 11:15:01** | 669 → **318** | 491 | **eingefroren** |
| `31917` | Hochdruck (0,01 bar) | **18.10. 11:15:01** | 3064 → **2913** | 437 | **eingefroren** |
| `31921` | Verdichter-Istdrehzahl (0,1 %) | **18.10. 11:15:01** | 466 → **0** | 56 | **eingefroren** auf 0. Gefährlich, weil es wie „steht“ aussieht |
| `31919` | Flag (unbekannt; laut f2 „seit Power-on 1“) | **18.10. 11:15:01** | 1 → **0** | 2 | **wahrscheinlich** ein Gültigkeits-/Verbindungsflag des Blocks, siehe unten |
| `1554` | VA2-FE1 HW-Ausgang | 18.10. 11:20:02 | 1 → 0 | 2 | Statuswechsel beim Regler-Reset; danach plausibel konstant |
| `17331` | ? | 18.10. 11:20:02 | 1 → 0 | 2 | wie `1554`, gleicher Zeitpunkt |
| `31904` | ? | 17.10. 08:50 | 65535 → 0 | 4 | unklar, kein Messwert erkennbar |
| `28938` | ? | 19.10. 00:05 | 24 → 23 | 1 | Ereignis-/Zählerwert, kein Defekt erkennbar |
| `1534` | Fehlercode vom Automaten | 20.10. 17:15 | 0 → 255 | 2 | 255 = kein Fehler. Die 0 stammte aus dem CAN-Ausfall 20.10. 12:23–17:10; Ereignisregister, lebt |
| `23631` | ? | 21.10. 07:05 | 1 → 3 | 14 | Statuswert, schaltet selten; lebt |

**Verlauf um den Reset (Rohdaten, Spalten `31903/05/07/13/15/17/19/21`):**
- 18.10. 11:05: 110 / 89 / 765 / 707 / 752 / 3000 / 1 / 545
- 18.10. 11:10: 115 / 100 / 783 / 669 / 797 / 3064 / 1 / 466
- 18.10. 11:15: 116 / 101 / 785 / 318 / 636 / 2913 / **0** / **0** (letzte frische Lesung, Verdichter läuft aus)
- 18.10. 11:20 bis 22.10. 23:55: alles identisch, **außer `31915` Niederdruck** (804, 865, 873 … 800). Am 23.10. 02:55 ist der Block weiter unverändert (31903 = 116, 31917 = 2913), `31915` = 755.

**Bestätigt / widerlegt:** Die Aussage „Kältekreisblock 31903–31921 seit Regler-Reset 18.10. 11:15 eingefroren“ ist für **7 von 8 benannten Registern bestätigt** (belegt). `31915` Niederdruck ist **widerlegt**: Er lebt durchgehend (1 792 Änderungen im Fenster, davon viele nach dem 18.10.). Außerdem leben im Bereich `31892–31921` die namenlosen `31893` (1 406 Änd.) und `31895` (1 245 Änd.) sowie `31908/31909` (Spiegel von `27495/27496` „Drehzahl CP“). **Kein anderes** der 555 Register hat zum 18.10. 11:15 aufgehört sich zu ändern (Prüfung über Klasse c: außer dem Block nur `1554/17331`, die um 11:20 einmal von 1 auf 0 gehen).

## (b) Über 7 Tage konstant – 415 Register (belegt)
Mit Ausnahme von `1543` (StatusInformation, letzte Änderung 13.10. 08:45) hat sich **keines** davon seit dem 09.10. geändert.

### (b1) Plausibel konstant – Parameter, Fehlerslots, nicht bestückt, High-Words (≈ 390)
| Gruppe | Register | Wert | Warum plausibel |
|---|---|---|---|
| Parameter/Sollwerte HK1/WW | `1478–1498` (ohne `1490/1493/1497`), `1532/1533`, `1541/1542`, `1561–1563`, `19482–19486`, `27510–27534`, `27548–27552`, `29437`, `30580–30583`, `30612–30620`, `30684–30692`, `31711–31715`, `31796–31801` | z. B. 1481 = 220, 1532 = 630, 30615 = 355, 31796 = 230 | schreibbar bzw. Konfiguration, ändert sich nur bei Bedienung |
| Aktive Fehler 1–5 (dp 29042–29046) | `1565–1609` | 65280 / 255 | „kein Fehler“. Ereignisregister, ohne Störung zu Recht konstant |
| Fehlerslot-Muster ohne Namen | `17339–17383`, `24150–24194` | 65280 / 255 im selben 9er-Raster | **wahrscheinlich** weitere Fehler-/Historienslots (gleiches Muster wie `1565ff`) |
| High-Words von U32/S32 | `1505` = 1, `1507`, `1516`, `1518`, `18727`, `18729`, `18731`, `25613`, `27484` = 1, `27486`, `27488`, `31707` | 0 bzw. 1 | ändern sich erst beim Übertrag über 65 536. **Nicht ausgrauen**, sie gehören zum Zähler |
| Kühlen in der Heizsaison | `27487` = 522 (Q Kühlen low), `18735/18736` Leistung Kühlen, `18763` Anlagetemp.-Soll Kühlen, `19870/19871` Status Kühlventil | konstant | Kühlbetrieb aus, plausibel. Im Sommer wieder lebendig |
| Zusatzwärme/Heizstab | `18747–18753` | 0 | **wahrscheinlich** korrekt: Stab nicht gelaufen |
| Nicht vorhandene Kreise/Quellen | HK2/HK3 `19563/19564`, `19612`, `19707/19708`, `19756`; Primär/Grundwasser fn3 `31651–31668`; WPF/WQP/GWP Low-Words `27494/27498/31706/31710`; FAV `19804`; Kaskade fn1–7 `18769–18782` (64266/0); SG-/Verfügbarkeitsblock `27536–27547` (ohne `27537/27545`) | 0 bzw. 64266 | Luft-WP, nur ein HK. 64266 = −1270 als S16, **wahrscheinlich** ein Ungültig-Wert |
| Firmware/Konfig ohne Namen | `32148` = 3215, `32139` = 0, `23622/23624/23626` = 4/70/55, `28934–28946` | konstant | `3215` = Applikationsversion (passt zu `appl3215`), **wahrscheinlich** Konfig-/Identblock |
| Unbekannte Nullen | `17326–17338`, `17384–17387`, `23628–23630`, `28839/28840`, `31764–31771`, `31788`, `31892/97/99`, `31901/02/06/11/12/14/16/18/20` | 0 / 255 | ohne Namen; im fn-7-Block **Vermutung**: High-Hälften bzw. unbelegte Paare |

| Status/HW-Ausgänge ruhend, Sonstiges | `1502/1503`, `1523`, `1540`, `1543–1545`, `1549`, `1551–1553`, `1555–1560`, `1564`, `18733/34/39/43/44/57`, `18766` = 64536, `19659/19660`, `19836`, `19852`, `19872/19873`, `23739/40/55/56`, `27500–27509`, `30572` | meist 0 | Ausgänge/Status nicht genutzter Funktionen. `1543` hat zuletzt am 13.10. geschaltet |
| Jahreskennzahl | `27467` = 38 (JAZ 3,8) | konstant | ändert sich nur langsam (Jahreswert), plausibel |

### (b2) Verdächtig konstant – Messwerte, die sich ändern müssten
| Register | Name | Wert | Bewertung |
|---|---|---|---|
| `18741`, `18756` | Volumenstrom (fn1/fn0) | 0 | **wahrscheinlich** über diesen dp nicht geliefert. Der echte Durchfluss lebt in `31708` „Volumenstrom gemittelt low“ (504 Änd.). Ausgrauen, nicht reparieren |
| `18740`, `18758` | Drehzahl Hauptpumpe (fn1/fn0) | 0 | **Vermutung:** die Pumpendrehzahl kommt hier nicht an. Die lebende Alternative ist `27495/27496` „Drehzahl CP“ (S32; −1 = 65535/65535 bei Verdichter aus) |
| `18754/18755` | Aktuelle Leistung Heizen fn0 | 0 | fn0 unbelegt; die lebende Größe ist `18732` (fn1) |
| `18745` | Sollwert Leistung WEZ fn0 | 0 | ebenso; lebend ist `18767` |
| Rest der Liste „VERDAECHTIG“ in `.out` | HK2/HK3, Primär-/Grundwasser, WPF/WQP/GWP | 0 | per Name „Messwert“, physikalisch aber nicht vorhanden → in (b1) eingeordnet |

**Ergebnis (b):** Außerhalb von fn 7 gibt es **keinen** Messwert, der laut Daten eigentlich leben müsste und eingefroren ist. Alle verdächtigen Nullen haben eine lebende Parallelgröße (belegt über die Klasse-(d)-Liste) oder gehören zu nicht vorhandener Hardware (wahrscheinlich).

## (d) Lebt – 83 Register (belegt)
Mit Namen u. a.: `1477` AF1, `1500` WW-Ist, `1513/1514` Vorlauf-Ist, `1525` WEZ-Temp., `1535` Rücklauf, `1536/1537` Leistung, `18725/18726` WEZ-Ist/Modulation, `18742`, `18760–18768`, `19562` Vorlauf-Soll, `19658` Mischer, `19706` Pumpe, `19754` SLP, `19868/19869`, `25611/25612/25614`, `27483` WW-Ist SF2, `27485/27489` Wärmemengen, `27490` COP, `27491` Ansaugtemp., `27495/27496` Drehzahl CP, `27537/27545/31741` Smart Grid, `29435/29436`, `31708` Volumenstrom, `31712/31716` Laufzeiten, `31915` Niederdruck.
Ohne Namen, lebend: `23623`, `23625`, `23627`, `23632–23634`, `31893`, `31895`, `31908`, `31909`.
**Hinweis (belegt):** `27495/27496` und `31908/31909` springen bei Verdichter-Stopp auf 65535/65535 (S32 = −1), z. B. am 22.10. 18:55 → 19:00 (`18726` 33 → 0). Das ist ein Aus-Marker, kein Stale-Wert. In Grafana sollte er als „aus“ bzw. null dargestellt werden, nicht als 4 Mrd. %.

## Empfehlung R90 – Grafana ausgrauen (VORSCHLAG, nichts umgesetzt)
1. **Dynamisch statt Liste, für fn 7:** `31903/05/07/13/17/21` mit einem Stale-Kennzeichen versehen, wenn sich **`31917` Hochdruck ≥ 2 h nicht ändert, obwohl `18726` Modulation > 0**. Im Lauf ändert sich der Hochdruck praktisch jede 5-min-Zeile. **Wahrscheinlich** taugt auch `31919` = 0 als Kennzeichen („Flag seit Power-on 1“ ist mit dem Freeze auf 0 gefallen). Das ist nur über **einen** Reset belegt und deshalb nicht allein verwenden.
2. **Statisch ausblenden bzw. grau** (Klasse a, 44 Register): alle 32768/65535-Register aus der Tabelle (a). Sie haben keinen Informationswert.
3. **Grau mit Tooltip „nicht geliefert, siehe X“:** `18740/18758` (→ `27496`), `18741/18756` (→ `31708`), `18754/18755` (→ `18732`), `18745` (→ `18767`).
4. **Nicht ausgrauen:** die High-Words (`1505`, `27484` usw.), weil sie zum Zähler gehören. Ebenso Fehler- und Statusslots, deren Konstanz die gute Nachricht ist, und die Kühlregister (saisonal).
5. **Darstellung `27495/27496`, `31908/31909`:** 65535/65535 als „aus“ bzw. null zeigen.

## Empfehlung R88 – „Karteileichen aus Poll“ (VORSCHLAG)
- **Der ursprüngliche R88 (X4-Slave 5, Adr. 1–4) ist nicht durch uns lösbar.** Den Slave pollt laut `ARGON_BERICHT.md` (B-02, Tabelle B76–B79, live bestätigt 19.10.) der **Hoval-Regler selbst** auf X4. Ein Eingriff hieße Firmware/EEPROM (**Tabu**). Vorschlag: R88 umformulieren in „Slave 5 aus unseren Auswertungen bzw. dem Sniff-Parser ignorieren“ und so schließen. Stand im Mitschnitt 16.–22.10.: siehe unten.
- **Volllogger (unsere eigene Poll-Liste):** Kandidaten zum Herausnehmen sind die **44 Register der Klasse (a)** und die unbenannten Nullblöcke `17326–17338`, `17384–17387`, `28839/28840`, `31764–31771`, `31788` sowie die nicht vorhandenen Kreise (`19563/19564`, `19612`, `31651–31668`, `18769–18782`, `18754/18755`, `18740/18741`, `18756/18758`). Zusammen **≈ 110 von 555** Spalten.
  - **Behalten:** fn 7 (auch eingefroren, denn genau daran erkennt man den Freeze), alle High-Words, Fehlerslots `1565–1609` (vielleicht reicht Slot 1) und Parameter (Änderungs-Audit).
  - **Ob das Herausnehmen CAN-Last spart, lässt sich nicht ermitteln:** Ob die Bridge diese Register aktiv per CAN-GET holt oder aus dem Cache bedient, geht aus dem Volllogger nicht hervor. Ohne diesen Nachweis ist der Gewinn nur Dateigröße und Übersicht.

## Was bringt uns das
**Sicher (belegt aus den Rohdaten)**
- Seit 18.10. 11:15 sind Lufteintritt, Sauggas, Heißgas, Überhitzung, Hochdruck und Verdichter-Istdrehzahl aus fn 7 **Standbilder**, auch noch am 23.10. 02:55. Jede Auswertung seit dem 18.10. (Hochdruck-Kurven, Überhitzung, Abtau-/Taktanalysen über 319xx) ist **ungültig**. Ersatz: `31915` Niederdruck (lebt), `18726` Modulation statt `31921`, für Hoch-/Heißgas RS485 `0207/0108`.
- Im selben Block lebt `31915` Niederdruck weiter. Der Freeze trifft also **nicht den ganzen fn-7-Datenpunkt-Block**, sondern eine Teilmenge.
- Die AZ-Grundlagen (`1505/06`, `25613/14`, `27484–89`, `1518/19`) und die HK/WW-Temperaturen leben. Die Daten für die Winter-AZ sind durch den Freeze **nicht** betroffen.
- Von 555 Spalten tragen nur **83** echte Dynamik; 44 sind reine Ungültig-Marker.

**Wahrscheinlich**
- Wie beim Vorfall 20.08.–03.09. (BACKLOG R6) wird der Block erst nach dem nächsten Strom-Aus/Ein bzw. Regler-Neustart wieder lebendig.
- `31919` (Flag 1 → 0) markiert den Zustand „fn-7-Werte nicht mehr aktuell“ und könnte als Freeze-Detektor dienen.
- `65280/255`-Blöcke ohne Namen (`17339ff`, `24150ff`) sind Fehler-/Historienslots weiterer Busteilnehmer.

**Vermutung**
- Dass gerade Niederdruck weiterläuft, die übrigen Kältekreiswerte aber nicht, deutet auf getrennte Bezugswege im Regler hin (z. B. ein Wert direkt vom Druckaufnehmer, die anderen über den Kälteregler/Carel-Link). Das ist **nicht** geprüft.
- `1554` (VA2-FE1 HW-Ausgang) und `17331`, beide 1 → 0 um 11:20, sind Folgen desselben Resets. Was VA2-FE1 schaltet, ist offen.

**Nicht ermittelbar (aus diesen Daten)**
- Warum der Regler-Reset den Teilblock einfriert, und ob ein Eingriff ohne Strom-Aus möglich ist.
- Ob die Bridge die tot-Register aktiv per CAN abfragt, also ob ein Herausnehmen Buslast spart.
- Bedeutung der 177 Register ohne Namen (siehe `.out`), darunter die lebenden `23623–23634`, `31893`, `31895`.

## Nachtrag R88: X4-Slave 5 im passiven Mitschnitt 16.–22.10. (belegt, `or_stale_20261023_nachtrag.out`)
| Tag | Antworten FC3 R1 n4 | davon ≠ 0 | Antworten FC3 R35 n3 |
|---|---|---|---|
| 16.10. | 706 161 | 0 | 727 705 |
| 17.10. | 684 025 | 0 | 705 043 |
| 18.10. | 688 857 | 0 | 709 889 |
| 19.10. | 694 886 | 0 | 715 952 |
| 20.10. | 706 473 | 0 | 727 885 |
| 21.10. | 698 491 | 0 | 719 958 |
| 22.10. | 703 130 | 0 | 724 413 |
- **R1–R4 (Adr. 1–4) sind über 7 Tage zu 100 % null: 4 882 023 Antworten, keine einzige ≠ 0** (belegt). Das deckt sich mit R92 (12.09.: 617 160 Antworten).
- **R35–R37 leben** (wechselnde Wertetripel, z. B. `005e 005f 0061` = 94/95/97). An 16.–18.10. dominiert `0001 0000 0000`, ab 19.10. kaum noch. Die Bedeutung ist **nicht ermittelt**. Slave 5 ist also kein toter Teilnehmer, nur seine Adressen 1–4 sind leer.
- **Konsequenz:** Den Poll macht der Hoval-Master. Für uns bleibt nur, R1–R4 im Sniff-Parser und in Grafana zu ignorieren. R35–R37 sind ein Kandidat für eine eigene Untersuchung (Vorschlag, nicht Teil dieses Auftrags).

## Stichprobe zum Selbst-Nachprüfen
`~/hoxpi_fulllog/2026-10-22.csv`, Zeile `2026-10-22 12:00:02`: `31903=116`, `31907=785`, `31913=318`, `31917=2913`, `1477=98`, `18726=0`. Im Header dieser Datei liegen sie in den Feldern 536/540/546/550/2/201. Zum Vergleich vor dem Freeze `2026-10-18.csv.gz`, `2026-10-18 11:05:01`: 110/765/707/3000/116/55.
Prüfbefehl (nur lesend): `head -1 2026-10-22.csv | tr , '\n' | grep -n -x -E '31903|31917'`, danach `grep '^2026-10-22 12:00' 2026-10-22.csv | cut -d, -f536,550`.