# ANALYSE Überhöhung WP-Soll 1529 vs. HK1-Soll 19562 – woher kommen die +3 K? (23.10.2026, Analyse-Agent, nur lesend)

**Kurz für dich, der Betreiber:** Die +3 K stammen aus dem Heizkreis-1-Parameter **07-001 „WEZ Überhöhung/Abschlag VL-Sollwert“** (Modbus **30684**), und der steht im ganzen Log fest auf **3,0 K**. Weil 1529 danach noch auf 0,5 K **abgerundet** wird, liegt der tatsächliche Aufschlag bei **2,6 bis 3,0 K**. Einen 1,5-K-Versuch würde ich vorerst **nicht** machen: Die Mischer-Reserve ist schon heute knapp, und zwar im **Stillstand vor dem WP-Start**, nicht während der Läufe.

**Daten:** `Emulation\or_ag1_2026-10-16..21.csv.gz`, `or_ag1_2026-10-22.csv`, `or_hydraulik_20261023_raw_2026-10-23.csv`, alle 5 min, zusammen 2196 Punkte von 16.10. 00:00:01 bis 23.10. 14:55:01. Die Spalten wurden über die Kopfzeile zugeordnet, die Rohwerte sind 0,1 °C/K.
**Registernamen:** `HoxPi-Doku\WEZ_Register_offiziell_UnitId1.csv`, `hoxpi-konfig-backup\bridge\reg_texts.json`, `HoxPi-Doku\Bedienteil_Katalog.csv`. In der Modbus-Guideline-xlsx stehen nur Beispielblätter: 1490, 19562 und 1561 kommen vor, 1520, 1529, 1531 und 18761 dagegen nicht.
**Skripte:** `Emulation\or_ueberh_20261023_a.py` … `_h.py`. `_e.out` ist der Volltext-Grep.

## 1. Kette der Sollwerte (Heizbetrieb, HK1)

| Schritt | Register | Name (Hoval-Liste) | Beziehung (Daten) |
|---|---|---|---|
| Loxone-Vorgabe | 1490 (07-036) | Vorlauf Soll Konstantanf. Heizen HK1 | = 19562 in 520 von 592 Punkten mit 19562 > 0. Der Rest sind Übergänge (±1…9) oder 1490 = 0, während 19562 noch nachläuft |
| HK1-Soll | 19562 | Heizkreis 1 Vorlauf-Soll | Sollwert des Mischers (1513 regelt darauf) |
| + Überhöhung | **30684 (07-001 HK1)** | **WEZ Überhöhung/Abschlag VL-Sollwert** | **konstant 30 (= 3,0 K) in 2196 von 2196 Punkten** |
| Wärmemanager-Soll | 18761 | Anlagetemp. Soll Heizen aktuell | **= 19562 + 3,0 K** in 565 von 592 Punkten. Abweichler liegen bei ±0,1…0,5 K (Übergänge, 5-min-Versatz) |
| WEZ-/HK-Soll | 1520 | Sollwert für Heizkreisbetrieb | Heizen: **⌊18761 auf 0,5 K⌋, aber mindestens 30,0 °C**. Bei WW: WW-Ladesoll (56,0/61,0) |
| WP-Soll aktiv | 1529 / 1531 | Heizung Sollwert / WEZ Sollwert | bei `1539 = 1` in 172 von 172 Punkten = 1520. Sonst ist 1529 = 0, und 1531 trägt bei WW den Ladesoll |

**Belegt durch die Endziffer:** Im Heizbetrieb ist 1529 − 19562 = 30 / 29 / 28 / 27 / 26, wenn 19562 mod 5 = 0 / 1 / 2 / 3 / 4 ist. Das trifft auf 44 / 37 / 39 / 25 / 23 Punkte zu, nur 4 Ausreißer bei Übergängen. Der Unterschied kommt also allein von der Abrundung und hängt weder von der Außentemperatur noch von der Uhrzeit ab.

## 2. Verteilung 1529 − 19562 (Frage 1)

| Zustand (1539) | n | 1529 − 19562 (0,1 K: Anzahl) | Bemerkung |
|---|---|---|---|
| 1 = Heizen | 172 | 30: 44 · 28: 39 · 29: 37 · 27: 25 · 26: 23 · 32: 2 · 31: 1 · 335: 1 | 2,6…3,0 K, nur durch Abrundung. 3,1/3,2 K = Übergang |
| 0 = Aus | 1772 | 0: 1440 · negativ: 332 | 1529 = 0, wenn der Verdichter aus ist. 18761 = 19562 + 3,0 K läuft weiter |
| 4 = WW | 248 | 1529 = 0 oder 560/610 | 1529/1531 = WW-Ladesoll, keine HK-Überhöhung |
| 51 (Vorspülen) | 4 | gemischt | Übergang |

- **Außentemperatur (Heizen):** Bei AT 0–3 / 3–6 / 6–9 / 9–12 / 12–15 / 15–18 °C liegen die häufigsten Werte bei 28 / 30 / 29 / 27 / 27 / 30. Das ist die Endziffer von 19562 und **keine Abhängigkeit von der AT**.
- **Uhrzeit:** 18761 − 19562 = 30 in allen vier 6-h-Blöcken (Nacht 21, Vormittag 106, Nachmittag 25, Abend 8 Punkte). Andere Werte (29, 31, 33, 35) kommen nur einzeln bei Sollwertwechseln vor.
- **HK2:** 30685 (07-001 HK2) = 3,0 K, 1491 (Konstantanf. HK2) = 16,5 °C, die Pumpe 19707 ist immer 0. HK2 fordert also nie an und trägt **nichts** zu 18761 bei.
- **Ausnahme 30-°C-Boden:** Vom 16.10. 20:05 bis 18.10. 23:25 (100 Punkte) war 19562 = 24,0 und 18761 = 27,0, aber **1520 = 30,0**. 1520 hat also eine Untergrenze von 30 °C. In dieser Zeit lief der Verdichter nicht.


| Modbus | Parameter | Name | Wert im Log | Lesbar | Schreibbar (Hoval-Liste) / Bedienteil | Wirkt hier? |
|---|---|---|---|---|---|---|
| **30684** | **07-001 HK1** | WEZ Überhöhung/Abschlag VL-Sollwert | **30 (3,0 K)** konstant | ja, geloggt | Yes, Bereich −100,0…+30,0, Schritt 10 Rohwert (= 1,0 K?) / Katalog: 3,0 °C, „verstellbar nein“ | **ja, die Ursache** |
| 30685 | 07-001 HK2 | dto. HK2 | 30 | ja | Yes | nein (HK2 inaktiv) |
| 30686 | 07-001 HK3 | dto. HK3 | 0 | ja | Yes | nein |
| 23739 | 09-037 WEZ 1 | Temperatur Überhöhung/Abschlag WEZ | 0 | ja | Yes / Katalog 0,0 K | nein (0) |
| 23740 | 09-037 Zusatzwärme | dto. | 0 | ja | Yes | nein |
| 27538 | 21-091 | Status Sollwert Erhöhung/Reduktion | 11 (beide Eingänge undefiniert) | ja | No | nein |
| 25731 | 05-001 WW | Überhöhung Ladesollwert | (nicht hier ausgewertet) | ja | siehe `ANALYSE_WW_Ladeueberhoehung_Parameter_20261022.md` | nur WW |
| 30687 | 07-002 HK1 | Vorlauf Minimaltemp. | 0 | ja | Yes | nein |
| 30690 | 07-008 HK1 | Vorlauf Maximaltemp. | 37,0 | ja | Yes | begrenzt 19562 nach oben |
| – | 07-041 HK1 | Mischer Neutralzone | 1,0 K (Katalog) | nur CAN | – | Totband des Mischers |
| ? | ? | Untergrenze 30,0 °C für 1520 | – | – | – | **Herkunft nicht gefunden** |

**Sicher:** Das Zusammenspiel 07-001 = 3,0 K → 18761 = 19562 + 3,0 K ist durch Wert und Hoval-Beschreibung belegt („Überhöhung der Vorlauf-Solltemperatur an die Wärmeerzeugeranlage; im Heizbetrieb Überhöhung, im Kühlbetrieb Abschlag“).
**Achtung Kühlen:** Derselbe Parameter wirkt im Kühlbetrieb als **Abschlag**. Das WP-Kühlsoll liegt dann 3 K **unter** dem HK1-Soll (Taupunkt!). Das ist aus der Beschreibung abgeleitet, in diesem Log gab es keine Kühlung.

## 4. Mischer-Reserve heute und was 1,5 K bedeuten würden (Frage 4)

Ab 17.10. 12:30 sind 31893/31895 live. Werte als Quantile 0/5/25/50/75/95/100 % in K.

| Größe | Quantile | Lesart |
|---|---|---|
| Heizen (n = 126): 1529 − 1513 | 0,7 / 1,5 / 2,6 / 4,0 / 5,4 / 8,6 / 13,3 | ≤ 1 K: 2 Pkt, ≤ 2 K: 15, ≤ 3 K: 42 |
| Heizen: WP-VL 31893 − 19562 | −0,8 / 0,5 / 3,5 / 5,1 / 6,7 / 8,8 / 9,4 | während des Laufs reichlich Reserve, knapp nur in den ersten 5 min |
| Heizen: 1513 − 19562 | −10,4 / −6,0 / −2,5 / −1,3 / 0,2 / 1,2 / 2,0 | Laufbeginn: HK1 ist noch unter Soll (Nachholen aus dem Stillstand) |
| **Stillstand, HK1-Pumpe an (n = 331): 1513 − 19562** | −15,2 / −8,9 / −6,7 / **−0,9** / −0,2 / 0,4 / 2,6 | **45 % > 1 K unter Soll, 36 % > 2 K unter Soll** |
| WP-Start (Punkt davor, n = 17): WP-RL − 1520 | −8,9 / … / −3,1 (Median) / … / −2,1 | die WP startet bei RL ≈ 1520 − 3 K ≈ **19562 − 0,5 K** |
| WP-Start: 1513 − 19562 | −6,7 / … / **−2,4** (Median) / … / −1,0 | **HK1 liegt vor jedem Start schon 1…7 K unter Soll** |
| WP-Stopp (letzter Laufpunkt, n = 18): WP-RL − 1529 | −3,9 / −1,0 / **+1,8** / +2,2 / +2,9 | Stopp bei RL ≈ 1529 + 2…3 K |
| WW (n = 86): 1513 − 19562 | Median −10,1 | HK1 wird bei WW-Ladung praktisch nicht versorgt (bekannt) |

**Was das heißt:**
- Die WP regelt ihren **Rücklauf**, der stellvertretend für den Puffer steht, in einem Band um 1520: Start bei etwa 1520 − 3 K, Stopp bei etwa 1520 + 2…3 K. 07-001 verschiebt **das ganze Band** nach oben. Die Spreizung ändert sich dadurch nicht.
- **Engpass ist die Unterkante des Bands.** Kurz vor dem Start ist der Puffer etwa so warm wie 19562, und HK1 kommt schon dann nicht mehr auf Soll (Median −2,4 K). Während der Läufe ist dagegen genug Reserve da (WP-VL − 19562 Median 5,1 K).
- **Mit 1,5 K statt 3 K** (wahrscheinlich, abgeleitet): Das ganze Band sinkt um 1,5 K, der WP-VL also ebenfalls um ~1,5 K, und der COP steigt grob um 3–4 %. Gleichzeitig startet die WP erst bei Puffer ≈ 19562 − 2 K. HK1 liegt dann im Stillstand vor dem Start etwa **3,5–4 K** statt 2,4 K unter Soll, und das betrifft rund 45 % der Stillstandszeit mit Anforderung. Während der Läufe wäre 1529 − 1513 in ~25 von 126 Punkten (≈ 20 %) unter 1 K. Der Mischer würde dort voll aufmachen und trotzdem nicht ganz auf Soll kommen.
- **Schrittweite:** Laut Hoval-Liste hat 30684 die Schrittweite 10 Rohwert. Bei 1 Dezimale heißt das **1,0 K**, damit wären nur 2,0 K oder 1,0 K einstellbar, nicht 1,5 K. Das ist **zu prüfen** am Bedienteil. **+3,0 K ist zugleich der Maximalwert** (Max 300).

## 5. Stichproben (Rohwerte, exakte Zeitstempel)

| Zeit | Datei | 1539 | 1477 | 1490 | 19562 | 30684 | 18761 | 1520 | 1529 | 1531 | 1513 | 31893 | 31895 | 19658 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-20 07:40:01 | or_ag1_2026-10-20.csv.gz | 1 | 87 | 311 | 311 | 30 | **341** | 340 | **340** | 340 | 286 | 349 | 309 | 15 |
| 2026-10-23 06:30:01 | or_hydraulik_20261023_raw_2026-10-23.csv | 1 | 19 | 330 | 330 | 30 | **360** | 360 | **360** | 360 | 323 | 378 | 346 | 5 |
| 2026-10-17 18:10:01 | or_ag1_2026-10-17.csv.gz | 1 | 145 | 353 | 353 | 30 | **382** | 380 | **380** | 380 | 321 | 389 | 347 | 21 |
| 2026-10-22 04:40:01 | or_ag1_2026-10-22.csv | 1 | 75 | 315 | 315 | 30 | **345** | 345 | **345** | 345 | 308 | 370 | 333 | 4 |

Rechnung: 311 + 30 = 341, abgerundet auf 340. 353 + 30 = 383, im Log steht 382 (Übergang um 0,1 K), abgerundet auf 380. 315 + 30 = 345, bleibt 345. Damit liegt der Aufschlag auf 1529 einmal bei 2,9, einmal bei 3,0, einmal bei 2,7 und einmal bei 3,0 K.
30-°C-Boden: im Zeitraum 16.10. 20:05:02 bis 18.10. 23:25:01 (Dateien or_ag1_2026-10-16/17/18.csv.gz), zum Beispiel 19562 = 240, 18761 = 270, 1520 = 300, 1529 = 0 (1539 = 0).

## 6. Befund

**Sicher (belegt)**
- 1529 = 1520 = ⌊(19562 + 30684) auf 0,5 K⌋, wenn der Verdichter im Heizbetrieb läuft. 30684 (07-001 HK1) = 3,0 K, konstant über 7 Tage.
- Der effektive Aufschlag 1529 − 19562 beträgt **2,6–3,0 K** (Median 2,8 K) und folgt nur der Endziffer von 19562, nicht der AT, Uhrzeit oder HK2.
- 18761 („Anlagetemp. Soll Heizen aktuell“) ist der Wärmemanager-Soll = 19562 + 3,0 K **ohne** Rundung. Er wird auch im Stillstand berechnet.
- 19562 ist der **HK1-Mischersoll** (= Loxone-Konstantanforderung 1490), nicht das Maximum aller Kreise.
- 09-037 (23739) als zweite, WEZ-seitige Überhöhung steht auf 0 und wirkt nicht.

**Wahrscheinlich**
- 18761 ist das Maximum über alle Heizkreise von (VL-Soll + 07-001 des Kreises). Das ist nicht prüfbar, weil HK2 nie anfordert.
- Der Start der WP hängt am Rücklauf (1535/31895) relativ zu 1520 (≈ −3 K), der Stopp liegt bei ≈ 1529 + 2…3 K. Bei 5-min-Raster sind das nur ungefähre Schwellen.
- Die Mischer-Reserve ist im Stillstand vor dem Start schon heute zu klein (HK1 1–7 K unter Soll). Eine kleinere Überhöhung verschärft das.

**Vermutung**
- Der 30,0-°C-Boden von 1520 ist eine WEZ- oder Wärmemanager-Mindesttemperatur (09-xxx/10-xxx). Welcher Parameter es ist, ist unklar. 1487 (Handbetrieb 30,0) hat wahrscheinlich nichts damit zu tun.
- 3,0 K ist bei Hoval möglicherweise Werkseinstellung bzw. das Maximum von 07-001, also keine gezielte Wahl des Installateurs.

## 7. Was bringt uns das

- Die +3 K sind kein Rätsel mehr. Es ist **ein** Parameter (07-001 HK1, Modbus 30684), lesbar und laut Hoval-Liste schreibbar. Er ist ein direkter Hebel für die WP-Vorlauftemperatur, ~2–2,5 % COP je K.
- Der Hebel lohnt sich aber erst, wenn das **Stillstandsloch** behoben ist (HK1 fällt vor dem Start unter Soll). Sonst kostet er Komfort. Dann reagiert Loxone mit höherem 1490, und die Ersparnis ist weg.
- Für Kühlen gilt dasselbe als Abschlag (−3 K auf das WP-Kühlsoll). Beim Taupunkt-Thema solltest du das mitdenken.

## 8. Vorschlag (nur Vorschlag, nichts geändert)

1. **Zuerst nur ablesen:** Am Bedienteil HK1 → 07-001 anschauen und notieren, welche Schritte möglich sind (1,0 oder 0,5 K) und welche Bedienebene nötig ist. Dazu den 30-°C-Boden suchen (WEZ-Menü 09-/10-xxx).
2. **Erst danach, wenn überhaupt:** einen Test mit **2,0 K** (nicht 1,5 K, siehe Schrittweite) über 3–5 Heiztage mit ähnlicher AT.
   - Abbruchkriterium: Der Median von 1513 − 19562 im Stillstand mit HK1-Pumpe wird schlechter als −1,5 K (heute −0,9 K), oder Loxone hebt 1490 an.
   - Erfolgskriterium: WP-VL im Lauf sinkt um ~1 K, die Laufzahl pro Tag bleibt etwa gleich.
   - **Rückweg:** 07-001 HK1 wieder auf 3,0 K (Rohwert 30), Wert vorher fotografieren.
3. **Besser zuerst:** das Stillstandsloch angehen, also prüfen, ob die WP-Startschwelle bzw. Hysterese (Rücklauf vs. 1520) verstellbar ist und ob der Puffer überhaupt einen gültigen Fühler hat (27493/27494 ungültig). Das ist der eigentliche Engpass.

## 9. Nicht ermittelbar (mit diesen Daten)

- Schrittweite und Bedienebene von 07-001 am Bedienteil (Hoval-Liste: Step 10 Rohwert, Katalog: „verstellbar nein“).
- Herkunft der 30,0-°C-Untergrenze von 1520.
- Ob 18761 wirklich das Maximum über die Heizkreise bildet (HK2 fordert nie an).
- Genaue Start-/Stoppschwellen und Hysterese der WP (5-min-Raster, keine Puffertemperatur).
- Puffer-Austrittstemperatur zum Mischer und HK-Rücklauf (kein Fühler). Damit lässt sich die Mischer-Reserve nur über 1513 vs. 19562 indirekt bewerten.
- Bedeutung von 19658 (Mischer, Werte −10…+70 % bei Heizen): Stellung oder Stellbefehl.
- Wirkung im Kühlbetrieb (kein Kühlen im Log).


## Nachtrag 23.10.2026 21:05 (Orchestrator, Katalog F6): Schrittweite und Bereich von 07-001
| Quelle | Wert |
|---|---|
| HoxPi `read_register 30684` (23.10. ~21:00) | Rohwert 30 = **3,0 °C**, S16, 1 Dezimale, katalog_schreibbar ja, Whitelist nein. HoxPi liefert **keine** Min/Max/Step-Felder. |
| Offizielle Datenpunktliste `[lokaler Pfad] Heating & Cooling\Hoval Modbus Datenpunktliste Stand April 2026 (1).xlsx`, Blatt Deutsch, Zeile 30684 (DP 7001) | Steps **10**, Min **-1000**, Max **300**, Decimal 1, Einheit °C -> **Schritt 1,0 K**, Bereich -100,0 ... +30,0 (Untergrenze vermutlich Platzhalter) |
| Gegenprobe Lesart Steps | 23739 'Temperatur Ueberhoehung/Abschlag WEZ' (DP 9037): Steps 5, Dec 1 -> 0,5 K; 1490: Steps 10 -> 1 K. Steps ist also in Rohwert-Einheiten. |

- **Ergebnis (sicher laut offizieller Liste, live nicht pruefbar ohne Schreiben):** 07-001 geht nur in **ganzen Kelvin** (3 / 2 / 1). **1,5 K ist nicht einstellbar.** Der Test aus `ENTSCHEIDUNGEN_offen.md` Punkt 3 bleibt also **3,0 -> 2,0 K**.
- HK2/HK3 ([Nummer]) gleich aufgebaut; 30685 steht live auf 3,0, 30686 auf 0,0.
- **Was bringt uns das:** Die Entscheidung 07-001 hat nur die Stufen 2 K (ca. -2 bis -2,5 % Heizstrom) oder 1 K; Zwischenstufen fallen weg.