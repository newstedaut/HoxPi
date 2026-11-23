# ANALYSE: Welcher Hoval-Parameter macht die WW-Ladeüberhöhung +4 K? (22.10.2026)

Stand 22.10.2026 · nur lesend (lokale Doku auf Windows-PC), nichts an der Anlage geändert, kein Bus-Zugriff.

## Frage
Am X26 (RS485, Obj 0x20) schickt die TopTronic dem Kälteregler als WW-Ladesoll **M1 = dp5051 + 4,0 K**, nur während einer WW-Ladung (22.10.: 52→56, 57→61; Quelle `HoxPi-Doku\ANALYSE_X26_Obj20_Sollwerte_Gegenprobe_20261022.md` Z. 26–54). Welcher Parameter bestimmt die +4 K?

## Kernergebnis
**05-001 „Überhöhung Ladesollwert“** (dp 5001, TTE-WEZ fg=2 fn=0, S16, 0,1 K, −10,0…+30,0 K, Schritt 0,5 K). Live-Wert seit 08.09.2026 17:10 = **35 (3,5 K)** laut CAN-Mitschnitt. Gemessen werden aber **+4,0 K** – die letzten 0,5 K sind **nicht geklärt**.

M1 am X26 ist dasselbe wie Modbus-Reg **1521 „Sollwert für Speicherbetrieb“** (beide = Soll + 4 während der Ladung, 0 sonst).

## Fundstellen

### F1 – Parameterdefinition (offiziell, Hoval-Modbus-Datenpunktliste)
`[lokaler Pfad]` Z. 14358–14376 (Eintrag `2_0_5001`, Reg 25731):
> "name": "überhöhung Ladesollwert" … "min": -100, "max": 300 … "unit": "K", "comm": "Mit diesem Parameter kann eine Überhöhung für den Ladesollwert eingestellt werden."

### F2 – Hoval-KDT-Anleitung (TTE-FW, gleicher WW-Funktionsblock)
`[lokaler Pfad]` Z. 32–33 (Quelle Q1, PDF-S. 154 / gedr. S. 130):
> „A3 – 05-001 Überhöhung Ladesollwert, Werk 5 K, Bereich −10,0…50,0 K“ – „Mit diesem Parameter kann eine Überhöhung für den Ladesollwert eingestellt werden.“
Werkswert in anderen Quellen: 2 K (Walter Meier SE 6024 WPC, `Hoval-Doku\walter-meier-se6024wpc-parameterliste-05-001-20260910.md` Z. 13), UltraSource-Nutzer im Forum 5,0 K (FUND-Datei A17).

### F3 – Formel Ladesoll = WW-Soll + 05-001
`[lokaler Pfad]` Z. 91:
> „Die validierte Regel lautet `1521 = min(1497 + 05-001 ; 62,0)`.“

### F4 – Historie von 05-001 an deiner Anlage (Kausalbeleg: Wert geändert → Überhöhung geändert)
`[lokaler Pfad]` Z. 5088–5089 (Tabelle Reg 1521):
> „30.07.–05.09. | **WW-Soll + 3,5 K** (53,5 bei Soll 50,0; 51,5 bei Soll 48,0)“ / „seit 06.09. 12:15 | **WW-Soll + 10,0 K**“
Gleiche Datei Z. 2558: „**Live = `0x0064` = 100 → 10,0 K.** Das erklärt `1521` = WW-Soll + 10 K.“ (05-001 per CAN nach dem Bedienteil-Vorfall 06.09.)

`[lokaler Pfad]` Z. 12 und 17:
> „`17:10:44 SET 1FE08801 fg=2 fn=0 dp=5001 val=0023` (= 35 = 3,5 K)“
> „**Wirkung (Volllogger 09.09. 14:55-15:40):** `1521` = **540** bei `1497` = 500 → Überhöhung **+4,0 K**“
Dort auch: „540 ≠ 535: die Formel … hat evtl. einen +0,5-Anteil oder rundet - offen“.

### F5 – +4,0 K seitdem stabil (Stichproben)
- `[lokaler Pfad]` Z. 16: „Soll **57,0** … `1521` **61,0** = Soll + 4,0 K“
- `[lokaler Pfad]` Z. 210: „20.09. 12:25 zeigt Ladesoll `1521` = Soll + 4 K (58 -> 62)“; Z. 420: „23.09. … `1521` = 56,0 (= Soll + 4 K …)“
- 22.10. am X26: 5 Ladungen, alle +4,0 K (ANALYSE_X26 Z. 54).

### F6 – Andere Kandidaten geprüft und ausgeschlossen
| Parameter | Live | Warum nicht |
|---|---|---|
| 05-034 Überhöhung Ladesoll Mischerregelung (Werk 2,0 K) | nicht gelesen | wirkt laut Q1 nur „wenn eine AVR oder eine Vorregelung aktiviert ist“ (FUND-Datei Z. 35); 2,0 K passt nicht zu 4 bzw. 0,5 K |
| 07-001 WEZ Überhöhung VL-Soll (Reg [Nummer]) | 3,0 K | wirkt auf Heizkreis-VL (Reg 18724 = 1490 + 3 K), nicht auf 1521; lt. Journal Z. 5096–5097 „stehen unverändert auf 3,0 und sind es nicht“ |
| 09-037 Temperatur Überhöhung/Abschlag WEZ (Reg [Nummer]) | 0,0 K | 0 – kann nichts beitragen (`HoxPi-Doku\Bedienteil_Katalog.csv` Z. 444–445) |
| 05-078/05-079 Sollwert-Erhöhung/-Reduktion (GLT) | 0 / 0 | 0 (Bedienteil_Katalog.csv Z. 978–979) |

## Einordnung

**Sicher**
- Der zuständige Parameter ist **05-001 „Überhöhung Ladesollwert“**: offizieller Name/Text (F1, F2), Formel 1521 = 1497 + 05-001 (F3), und an deiner Anlage zweimal kausal belegt: 05-001 = 100 → +10 K (06.–08.09.), SET 05-001 = 35 → +4 K (ab 08.09., F4).
- Die +4 K stehen seit 09.09. konstant, über Sollwerte 48…58 °C (F5).
- 07-001, 09-037, 05-077, 05-078/079 tragen nichts bei (F6).

**Wahrscheinlich**
- 05-001 steht weiter auf 35 (3,5 K). Ein späterer SET auf dp 5001 ist in der Doku nicht vermerkt. Letzter CAN-Beleg ist der SET vom 08.09. 17:10, eine **Rücklesung danach gibt es nicht**.
- Die zusätzlichen +0,5 K entstehen in der TopTronic-Berechnung (Rundung/fester Anteil). Das ist nur eine Vermutung. Vor dem Vorfall gab es dieselbe Differenz zwischen 1521 (+3,5 K) und Reg **18762 „Anlagetemp. Soll WW“ (+4 K)** (Journal Z. 5088).

**Nicht gefunden / offen**
- Woher die 0,5 K zwischen 05-001 = 3,5 K und gemessenen +4,0 K kommen. Möglich: 05-001 steht real auf 40 (nicht rückgelesen), oder die TopTronic rechnet einen festen Zuschlag/rundet.
- In den lokalen TopTronic-PDFs (`IDM-Doku\Recherche_laufend\quellen\TopTronic_E_Kurzbedienung_*.pdf`) gibt es keinen Treffer zu „Überhöhung“/„05-001“/„Ladesoll“ (pypdf-Volltext).
- `HoxPi-Doku\Bedienteil_Katalog.csv` Z. 966 führt 05-001 noch mit **10,0 K** (Stand CAN 06.09.). Das ist **veraltet** und sollte bei Gelegenheit auf 3,5 K (SET 08.09.) korrigiert werden. Nicht geändert, weil dieser Auftrag nur lesend ist.

## Was bringt uns das
- **Der Hebel ist bekannt:** Den Hub bei der WW-Ladung bestimmt die Summe aus WW-Soll (dp5051, Loxone) und 05-001. Bei Soll 57 fährt der Kälteregler auf 61 °C Ladesoll. Bei Soll 52 sind es 56 °C.
- **Vorschlag (der Betreiber entscheidet):** 05-001 in **einem** Schritt von 3,5 auf **2,0 K** senken (Hoval-Werk lt. Walter-Meier-Liste, Schritt 0,5 K). Erwartung: Ladesoll 1,5 K tiefer, also etwa 2–4 % weniger Strom je WW-Ladung. Das ist nur eine Faustregel (1 K VL ≈ 2–3 %) und nicht gemessen.
- **Risiko:** Mit weniger Überhöhung erreicht der Speicherfühler das Soll langsamer oder gar nicht. Die Ladung kann länger dauern oder knapp unter dem Soll enden (siehe FUND-Datei, „endet 1–2 K unter Soll“). Hinzu kommt die WP-Kappe 62 °C bzw. die WW-Leistungsregelung um ~55 °C (Journal `cc_monat_sonnet_20261018_b.txt` Z. 319). **Prüfen:** Ladedauer, Endtemperatur SF1, Pel je Ladung, eine Woche vorher/nachher.
- **Gleichwertige Alternative ohne Codeebene:** Statt 05-001 zu ändern, das Loxone-Soll um 1–2 K senken (z. B. PV 57 → 55). Das senkt das Ladesoll genauso und ist sofort umkehrbar.
- **Vor einem SET** (falls gewünscht): zuerst `grep dp=5001` im bm_rec der letzten Tage. Dann 05-001 einmal **nur lesen** (CAN GET 2-0-5001), damit die 0,5-K-Frage geklärt ist: Steht dort 35 oder 40? Max. ein Konfig-SET je 60 min, nie zusammen mit einem anderen Parameter.