# FUND: TopTronic E – Vorlauf-Überhöhung Wärmeerzeuger ggü. Mischerkreis (+3,0 K)

Stand: 23.10.2026 · Recherche nur öffentliche Quellen (kein Login) plus Abgleich mit eigenen Projektdaten.
Anlage: Hoval UltraSource B comfort C17, TopTronic E, Puffer + Mischer-FBH-Kreise.
Bereits bekannt und hier nicht wiederholt: 33-053/33-054, 03-007, 05-001, 00-302.

## Kernergebnis (kurz)

Die fixen +3,0 K kommen mit hoher Sicherheit von **Parameter 07-001 „WEZ Überhöhung/Abschlag VL-Sollwert“** (Heizkreis-Parameter, Datenpunkt 7001).
Modbus-Register HK1 = **30684**, HK2 = **30685**, HK3 = **30686**. Laut eigenem Register-Dump stehen HK1 und HK2 auf **30 = 3,0 K**, HK3 auf 0.
Einstellbereich laut Hoval-Datenpunktliste: **−100,0 … +30,0 K**, Schrittweite 1,0 K. Einen Werkswert nennt keine öffentliche Quelle.
Daneben gibt es eine zweite Überhöhung direkt auf WEZ-Ebene: Datenpunkt 9037 „Temperatur Überhöhung/Abschlag WEZ“ (Register [Nummer], im Bedienteil wahrscheinlich 09-037). Bei dir steht sie auf 0,0 K.

---

## 1. Belegt (öffentliche Quelle + Zitat)

| # | Aussage | Quelle | Zitat (<15 Wörter) |
|---|---|---|---|
| B1 | Datenpunkt 7001 (Heizkreis 1–3) heißt „WEZ Überhöhung/Abschlag VL-Sollwert“, Register 30684/[Nummer], Bereich −1000…300 (×0,1 = −100…+30 K), schreibbar | Hoval TTE-Modbus-Datenpunktliste (XLSX), Blatt „Deutsch“, verlinkt auf https://hoval.com/en/Modbus-integration-for-Hoval-systems-made-easy/modbus → https://cdn.hoval.com/toptronice-gateway-modbus-datapoints_hybris_original.xlsx | „Überhöhung/Abschlag der Vorlauf Solltemperatur an die Wärmeerzeugeranlage“ |
| B2 | Wirkung je nach Betriebsart: Heizen = Überhöhung, Kühlen = Abschlag | dieselbe XLSX, Kommentar zu 30684 | „Im Heizbetrieb wirkt der eingestellte Wert als Überhöhung.“ |
| B3 | Englischer Name von 7001 | dieselbe XLSX, Blatt „English“ | „H-GEN incr./red. flow setpoint“ |
| B5 | Den Parameter gibt es schon in der Vorgänger-Regelung TopTronic T als Heizkreis-Parameter 14 | TopTronic T Technical Manual: https://www.specifiedby.com/hoval-limited/toptronic-online/hoval_TopTronic-online_Operations_TopTronicT-Technical-Manual.pdf | „If a heat generator temperature elevation is parameterised (HC-Par. 14)“ |
| B8 | Effizienz: je 1 K weniger Vorlauf etwa 2–2,5 % (Luft/Wasser-WP) | ingenieur.de: https://www.ingenieur.de/technik/fachbereiche/gebaeudetechnik/waermepumpe-optimal-einstellen-vorlauftemperatur-und-pufferspeicher-beachten/ | „Effizienz der Anlage um etwa 2 bis 2,5 Prozent steigern“ |
| B9 | gleiche Größenordnung beim Hersteller Bosch | https://www.bosch-homecomfort.com/de/de/wohngebaeude/wissen/heizungsratgeber/waermepumpe/vorlauftemperatur-waermepumpe/ | „Jedes Grad weniger senkt den Stromverbrauch … um bis zu 2,5 Prozent.“ |
| B10 | Der Heizkreistyp (07-005) lässt sich auf „Pumpenkreis ohne Mischer“ stellen | energiesparhaus.at (ash31): https://www.energiesparhaus.at/forum/81367 | „Wenn man 07-005 auf 2 stellt, steuert die TopTronic-E keinen Mischer mehr.“ |


### Abgleich mit eigenen Projektdaten (keine Web-Quelle, aber sicher)

| Datum/Quelle | Register | Wert | Bedeutung |
|---|---|---|---|
| Register-Dump `Heizung/review_all_out.txt` | 30684 (HK1, dp 7001) | **30 → 3,0 K** | ergibt genau deine gemessenen +3,0 K |
| dto. | 30685 (HK2, dp 7001) | **30 → 3,0 K** | gilt auch im zweiten Heizkreis |
| dto. | 30686 (HK3) | 0 | HK3 nicht belegt |
| Bedienteil 19.08.2026 (`Heizung/Hoval_Parameter_Fachmann.md`) | 07-001 „WEZ Überhöhung/Abschlag VL Sollwert“ | *(leer)* | das Display hat den Wert damals nicht angezeigt. Der Bus liefert 3,0 K. |

Der Pfad im Bedienteil lautet `Service → TTE-WEZ … → Heizkreis (1) → Heizkreis 1 (0) → Parameter (7)` und ist nur mit Fachmann-Code zugänglich (laut eigener Doku).

---

## 2. Wahrscheinlich (begründet, aber nicht wörtlich belegt)

- **Bedienebene:** Die Einstellung liegt in der **Fachmann-Ebene**. Belegt ist das nur durch deinen eigenen Bedienteil-Pfad, nicht durch eine öffentliche Hoval-Seite. In der Endkunden-Ebene taucht 07-001 nicht auf.
- **Werkswert:** öffentlich nicht gefunden. 3,0 K in HK1 und HK2 sind entweder der Werkswert für Mischerkreise oder bei der Inbetriebnahme gesetzt. HK3 (nicht konfiguriert) hat 0. Das deutet eher auf einen bewusst gesetzten oder typabhängigen Wert hin, ist aber nur eine Vermutung.
- **Schrittweite 1,0 K:** Die XLSX nennt „Steps 10“ bei 1 Dezimalstelle. Deshalb sind wahrscheinlich nur ganze K einstellbar.
- **Untergrenze in der Praxis:** Ein Forumsnutzer mit Puffer und Mischer misst an der WP „ca. 2-3 Grad höher als der Heizkreis VL“ (https://www.energiesparhaus.at/forum/53714, ohio012). Im selben Thread rät JanRi: „Im Idealfall bleibt der Mischer dann komplett offen.“ Daraus folgt: Die Überhöhung muss mindestens den Temperaturverlust im Puffer (Mischung, Schichtung) und die Regelreserve des Mischers abdecken. Bei einem parallel eingebundenen Puffer und FBH-Vorlauf um 30 °C sind 1–2 K wahrscheinlich ausreichend. Unter 0 K kann der Mischer den Sollwert nicht mehr erreichen.

## 3. Vergleich mit anderen Herstellern (Plausibilisierung)

| Hersteller | Parameter | Werkswert | Quelle | Zitat |
|---|---|---|---|---|
| Hoval TopTronic T (Vorgänger) | HC-Par. 14 „Elevation heat generator“ | nicht genannt | specifiedby (B5) | „heat generator temperature elevation is parameterised (HC-Par. 14)“ |
| Viessmann Vitotronic (Kessel) | Codieradresse 9F, Differenz Kessel-Soll zu Mischerkreis-VL-Soll | 8 K (Forum) | https://www.energiesparhaus.at/forum/21177 | „Die ist standardmäßig auf 8°K eingestellt.“ |
| Viessmann (Praxis) | Ein Nutzer mit FBH-Mischerkreis senkt 9F auf 2 K | – | gleiche Quelle | „9F:8 (Werkseinstellung)“ |
| Vaillant, iDM | kein öffentlich belegter, gleichwertiger Parameter gefunden | – | – | – |

Einordnung: Kessel-Regelungen arbeiten traditionell mit 5–8 K Überhöhung. Bei einer Wärmepumpe kostet jedes K Effizienz (B8/B9). 3 K sind für eine WP schon „sparsam“, lassen sich aber wahrscheinlich noch auf 1–2 K senken.

## 4. Nicht gefunden

- Öffentliche Hoval-Dokumentation (PDF) zu TopTronic E mit **Werkswert und Bedienebene von 07-001**. Der Öl-Katalog 2026 (https://cdn.hoval.com/oel_katalog_2026_de_exa_hybris_original.pdf) und die Thermalia-dual-Unterlagen enthalten nur Funktionslisten.
- Haustechnikdialog „Parameter Hoval TopTronic 233“ und docplayer (TopTronic T Fachmannebene): für den Abruf gesperrt (robots).
- Vaillant (sensoCOMFORT) und iDM (Navigator): kein Parameter mit dieser Funktion öffentlich dokumentiert gefunden.
- Ein Hoval-Hinweis, wie klein die Überhöhung bei WP mit Puffer sein darf: nicht gefunden.

---

## 5. Was bringt uns das

- **Ursache geklärt:** Deine +3,0 K stammen von **07-001 = 3,0 K** in HK1 (und HK2). Das ist kein Fehler und kein Rechenfehler der WP, sondern ein eingestellter Wert.
- **Einsparung:** Bei ungefähr 2–2,5 % je K bringen 3 → 1 K etwa **4–5 % weniger Strom im Heizbetrieb**. Das ist eine Schätzung. Sie gilt nur, wenn die WP-Vorlauftemperatur dann wirklich sinkt und der Mischer nicht dauernd voll offen steht und trotzdem zu wenig liefert.
- **Vorschlag zum Testen:** HK1 und HK2 von 3 auf **2 K** stellen, 2–3 kalte Tage beobachten, danach auf **1 K** gehen. Prüfen:
  1. Erreicht der HK-Vorlauf-Ist sein Soll (Abweichung < 0,5 K im Mittel)?
  2. Steht der Mischer ([Nummer]) dauernd auf 100 %? Das ist okay, solange der Vorlauf trotzdem passt. Fehlen dabei Grad, ist die Überhöhung zu knapp.
  3. Steigen die Taktzahlen (Schaltzyklen) nicht spürbar?
- **Nicht auf 0 oder negativ gehen:** Der Puffer verliert durch Mischung immer etwas Temperatur. Ohne Reserve erreicht der Mischerkreis sein Soll nicht, und Loxone fordert dann mehr an.
- **Achtung Kühlbetrieb:** Im Kühlen wirkt derselbe Wert als **Abschlag**. Die WP fährt dann 3 K kälter als der Kreis-Sollwert. Senkst du 07-001, wird der WP-Kühlvorlauf wärmer. Für Taupunkt und Kondensat ist das eher günstig, die Kühlung wird aber etwas schwächer. Das Loxone-„Kühl-Min“ und 07-044 (19 °C) bleiben die eigentliche Untergrenze.
- **Wie ändern:** Am besten am Bedienteil mit Fachmann-Code (Heizkreis 1 → Parameter → 07-001). Über Modbus ([Nummer]) ist er laut Liste schreibbar. Er gehört aber nicht zu den 20 Registern, die im Langzeittest stabil gehalten haben. Er könnte nach rund 35 s vom Bedienteil zurückgeschrieben werden. Deshalb vorher und nachher Voll-Logger-Snapshot ziehen und den Wert nach 5 min erneut lesen.
- **Alternative, nur zur Info:** 07-005 = 2 (Pumpenkreis ohne Mischer, B10) würde den Mischer ganz aus der Regelung nehmen. Das ändert aber die Hydraulik-Logik, auch beim Kühlen. Erst die Überhöhung senken, das ist der kleinere Eingriff.