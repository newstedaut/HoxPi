# ANALYSE Heizstrom nach Tageszeit und PV-Deckung – lohnt gezieltes FBH-Vorheizen in PV-Stunden? (23.10.2026 ~18:30, Orchestrator, nur lesend)

**Frage:** Wie verteilt sich der WP-Strom im **Heizbetrieb** (ohne WW) über den Tag, wie viel davon lief bei PV-Einspeisung und wie viel aus dem Netz? Wie groß ist das Potenzial, Heizlast per Loxone in die PV-Mittagsstunden zu schieben (z. B. +2..3 K 11–15 Uhr bei Einspeisung)? Wie sieht das für den Winter aus?

**Ergebnis (3 Zeilen)**
1. **Heizstrom 12.09.–23.10.: 114,6 kWh_el (2,7 kWh/Tag).** Knapp die Hälfte läuft heute schon „billig“, also zu Grenzkosten von 8 ct. **Sicher** ist der Netzanteil von **42 %**. Zum großen Teil sind das die Läufe **05–09 Uhr**: Im Oktober liefen 26,9 kWh von 69,8 kWh zu 100 % aus dem Netz. Mittel über alles: **15,5 ct/kWh** (Sep 14,3, Okt 16,2).
2. **Wahrscheinlich bringt das Verschieben nur 1,5–4 €/Monat (Okt).** Begrenzend ist nicht der Estrich, sondern die **echte Einspeisung**. Der 14,3-kWh-Akku schluckt den Überschuss schon vorher: An Tagen mit < 25 kWh PV bleibt fast nichts zum Einspeisen (0,2–0,9 kWh am Tag).
3. **Im Winter wahrscheinlich ≈ 0–1 €/Monat.** Es gibt mehr Heizlast, aber kaum Einspeisung. Der Akku macht das „PV-Schieben“ heute schon. Eine Heizkurven-Anhebung allein wirkt außerdem kaum, weil die **Raumregler die Ventile bei Soll schließen**. Außerdem droht bei > 22,5 °C die **Kühlfalle**. **Empfehlung:** Den Umbau nur als kleinen, abschaltbaren Versuch machen, keine Priorität.

## Was bringt uns das
| Szenario | kWh_el verschoben/Tag | €/Monat | Sicherheit |
|---|---|---|---|
| Okt-Daten, Speicher konservativ (0,7 kWh_el/Tag ≈ 3,5 kWh_th, ~+0,15 K Haus) | 0,41 | **1,6** | wahrscheinlich |
| Okt-Daten, 1,4 kWh_el/Tag (~7 kWh_th, ~+0,3 K Haus) | 0,67 | **2,6** | wahrscheinlich |
| Okt-Daten, Speicher unbegrenzt (Obergrenze) | 1,06 | **4,1** | sicher als Obergrenze des Modells |
| Winter Dez–Feb (PV < 25 kWh/Tag, Einspeisung ≤ 1 kWh/Tag) | ≤ 0,2 | **≈ 0–1** | Vermutung (Hochrechnung, kein Winterdatensatz mit Akku) |

Annahmen: Netz 21 ct, Einspeisung 8 ct, also 13 ct je verschobener kWh. Der kleine AZ-Bonus mittags (wärmere Luft, Vermutung ~+5–10 %) und die Mehrverluste durch ein wärmeres Haus (~gleiche Größenordnung) heben sich grob auf. Hochrechnung aufs Jahr: wahrscheinlich **10–20 €/Jahr**, fast alles davon im Okt/Nov und März/April.

**Gemessen hat der größere Hebel nichts mit der Heizkurve zu tun:** Die Morgenläufe 05–09 Uhr kommen zu 100 % aus dem Netz. Das gilt **auch, wenn der Akku noch 41–42 % SOC hat** (Stichprobe 1 unten: 13.10. 07–08 Uhr, Bezug 3,59 kWh, Akku-Entladung 0,003 kWh). Ob dahinter eine Reserve-/SOC-Sperre steckt (Energiemanager „MinSoc“ = 95, „SOC_Freigabe“), ist **nicht ermittelt**. Eine Prüfung dort ist billiger als jeder Heizkurven-Umbau.

## 1. Heiz-kWh_el je Ortsstunde (12.09.–23.10., 42 Tage; Okt = 01.–23.10.)
Spalte „PV-netto %“: Dieser Anteil der Heiz-kWh fiel in eine Stunde, in der der Hauptstromzähler netto **nicht** bezogen hat (Formel `min(WP, Bezug−Einsp)` als Netzanteil). Spalte „billig %“: das Grenzkosten-Modell aus Abschnitt 2, also der Anteil, den eine zusätzliche kWh in dieser Stunde nur 8 ct kostet.

| h | Heiz kWh_el | je Tag | PV-netto % | billig % (Grenzkosten) | Ø ct/kWh | Okt kWh | Okt billig % |
|---|---|---|---|---|---|---|---|
| 0 | 0,45 | 0,011 | 0 | 0 | 21 | 0,45 | 0 |
| 1 | 0,00 | 0,000 | – | – | – | 0,00 | – |
| 2 | 0,33 | 0,008 | 66¹ | 0 | 21 | 0,00 | – |
| 3 | 3,90 | 0,093 | 52¹ | 0 | 21 | 1,37 | 0 |
| 4 | 4,80 | 0,114 | 42¹ | 0 | 21 | 2,54 | 0 |
| 5 | 7,74 | 0,184 | 20¹ | 0 | 21 | 4,57 | 0 |
| 6 | 8,31 | 0,198 | 6 | 0 | 21 | 3,58 | 0 |
| **7** | **13,20** | **0,314** | 0 | **0** | 21 | **9,29** | 0 |
| **8** | **12,58** | **0,299** | 0 | 29 | 17,3 | **9,42** | 13 |
| 9 | 7,80 | 0,186 | 31 | 87 | 9,7 | 5,09 | 80 |
| 10 | 4,11 | 0,098 | 57 | 82 | 10,4 | 3,05 | 76 |
| 11 | 3,50 | 0,083 | 79 | 67 | 12,4 | 1,37 | 65 |
| 12 | 2,71 | 0,065 | 100 | 100 | 8,0 | 0,97 | 100 |
| 13 | 6,22 | 0,148 | 91 | 91 | 9,2 | 4,69 | 88 |
| 14 | 4,86 | 0,116 | 99 | 100 | 8,0 | 2,53 | 100 |
| **15** | **10,80** | **0,257** | 98 | 87 | 9,7 | 6,70 | 79 |
| 16 | 8,36 | 0,199 | 94 | 76 | 11,1 | 4,30 | 64 |
| 17 | 8,80 | 0,209 | 75 | 42 | 15,6 | 5,41 | 31 |
| 18 | 3,92 | 0,093 | 50 | 0 | 21 | 2,31 | 0 |
| 19 | 1,45 | 0,035 | 0 | 0 | 21 | 1,45 | 0 |
| 20–23 | 0,74 | 0,018 | 0 | 0 | 21 | 0,74 | 0 |
| **Σ** | **114,6** | **2,73** | **47,2** | **42,5** | **15,5** | **69,8** (3,04/Tag) | **37,0** |

¹ Nachts ist „PV-netto“ ein Akku-Effekt: Der Akku deckt die Last, der Zähler zeigt nur ~55 Wh/h Grundbezug. Das Grenzkosten-Modell bewertet das trotzdem mit 21 ct, weil der Akku in diesen Nächten ohnehin bis zum Boden (SOC ~30–31 %) leer läuft. Jede kWh mehr kommt dann am Morgen aus dem Netz. **Sicher** (SOC-Verlauf), Bewertung **wahrscheinlich**.

- **Sicher:** Die Heizung läuft in zwei Blöcken, **03–09 Uhr (51 kWh, 44 %)** und **13–17 Uhr (39 kWh, 34 %)**. Zwischen 20 und 02 Uhr läuft fast nichts.
- **Sicher:** Der Nachmittagsblock liegt schon zu 76–100 % in billigen Stunden. Der HK1-Soll 1490 liegt 12–17 Uhr im Median bei **34–36 °C**, gegen 30–31 °C am Vormittag (Okt, `_7_profil.out`). Das ist faktisch schon eine „Nachmittags-Anhebung“. Ihre Ursache ist laut `ANALYSE_Nachmittagslaeufe_20261021.md` wahrscheinlich die Raumkorrektur des Klimacontrollers.
- **Sicher:** Teuer sind die **Morgenläufe 05–09 Uhr**: im Okt 26,9 kWh, also 1,17 kWh/Tag × 21 ct ≈ 7,4 €/Monat. Sie sind der einzige nennenswerte verschiebbare Block.

## 2. Grenzkosten-Modell (Netz / Akku / Einspeisung)
Je Stunde (Loxone-Stundendifferenzen, Ortszeit = UTC+2) die Frage: Was kostet **eine kWh mehr** in dieser Stunde?
- Netto-Einspeisung (Einsp − Bezug > 0,05 kWh) → **8 ct**.
- Akku lädt (> 0,2 kWh/h) und später am selben Tag wird noch > 0,5 kWh eingespeist → 8 ct. Kommt danach keine Einspeisung mehr, wird der Akku nicht voll → **21 ct**.
- Akku entlädt und erreicht vor dem nächsten Laden den Boden (SOC ≤ 32 %) → 21 ct, sonst 8,9 ct (8 ct / 0,9 Akkuverlust, Annahme).
- sonst Netz → 21 ct.

| Klasse der Heiz-kWh | 12.09.–23.10. | Anteil |
|---|---|---|
| Netz | 48,2 | 42 % |
| Einspeisung (direkt) | 35,3 | 31 % |
| Akku lädt, später Einspeisung (= billig) | 13,2 | 11 % |
| Akku entlädt, wird leer (= Netz) | 9,1 | 8 % |
| Akku lädt, wird nicht voll (= Netz) | 8,6 | 7 % |
| Akku entlädt, reicht | 0,3 | 0 % |

Heizstromkosten im Modell: **17,73 € in 42 Tagen**. Wäre alles im Netz gelaufen, wären es 24,07 € gewesen. Sep: 44,7 kWh, 51 % billig. Okt: 69,8 kWh, 37 % billig. **Der Trend zum Winter ist sicher:** mehr Heizstrom, weniger billiger Anteil.

## 3. Nach Außentemperatur-Klasse (Tagesmittel 1477), 41 volle Tage
„Teuer“ = Heiz-kWh zu 21 ct. „Pot“ = verschiebbar je Tag = `min(teure Heiz-kWh, Tages-Einspeisung, Speichergrenze)`.

| außen | Tage | Heiz kWh_el/Tag | teuer/Tag | PV kWh/Tag | Einsp kWh/Tag | Tage mit Einsp < 2 kWh | Pot 0,7 / 1,4 / unbegr. | €/Monat | Heiz-Starts/Tag | P_el im Lauf |
|---|---|---|---|---|---|---|---|---|---|---|
| ≥ 12 °C | 23 | 1,79 | 0,80 | 39,6 | 7,5 | 4 | 0,34 / 0,51 / 0,77 | 1,3 / 2,0 / 3,0 | 2,7 | 1,75 kW |
| 9–12 °C | 16 | 3,42 | 2,09 | 33,8 | 6,3 | **7** | 0,46 / 0,78 / 1,03 | 1,8 / 3,0 / 4,0 | 4,6 | 1,77 kW |
| 6–9 °C | 2 | 5,26 | 3,99 | 37,5 | 11,7 | 0 | 0,70 / 1,40 / 3,99 | 2,7 / 5,5 / 15,6 | 5,0 | 1,83 kW |
| < 6 °C | 0 | – | – | – | – | – | – | – | – | – |
| Sep (19 Tage) | | 2,36 | 1,15 | | 9,0 | | 0,40 / 0,65 / 0,99 | 1,6 / 2,5 / 3,9 | | |
| Okt (22 Tage) | | 2,80 | 1,72 | | 5,7 | | 0,41 / 0,67 / 1,06 | 1,6 / 2,6 / 4,1 | | |

Die Zeile 6–9 °C hat nur n = 2 (13.10. mit 20 kWh Einspeisung und 22.10.). Sie ist **nicht belastbar** und taugt nur als Tendenz: Je kälter, desto mehr teure Morgen-kWh.

**PV-Tagesertrag gegen Einspeisung** (`_6_potenzial.out`, sicher):
| PV kWh/Tag | Tage | Einsp kWh/Tag | Tage mit Akku voll (SOC ≥ 97) |
|---|---|---|---|
| 0–15 | 5 | **0,2** | 0 |
| 15–25 | 4 | **0,9** | 2 |
| 25–35 | 7 | 2,7 | 7 |
| > 35 | 25 | 10,9 | 25 |

→ **Wahrscheinlich:** Im Dez/Jan (16 kWp gemischt ausgerichtet auf 960 m, tiefe Sonne, Schnee auf Modulen) liegen die meisten Tage bei < 25 kWh PV. Dann ist der Überschuss **im Akku**, nicht im Netz, und Vorheizen spart nichts. Es leert nur den Akku früher, und der Abend läuft dann aus dem Netz. Ausnahme sind klare, kalte Tage mit freien Modulen. An denen wäre der Effekt sogar am größten (siehe 13.10.: 8,1 kWh Heizung, 20 kWh Einspeisung).

## 4. Potenzial-Rechnung: Speichermasse, Überschwinger, Takt
**Speicher Haus/Estrich** (wahrscheinlich, grob):
- Aus `ANALYSE_Auskuehlung_Heizlast_20261023.md`: Zeitkonstante ~200–250 h, Verlust ~80–130 W/K → **wirksame Wärmekapazität ~16–30 kWh_th/K** (ganzes Haus, Estrich + Bauteile).
- Estrich allein: Geheizt ist heute nur HK1/UG mit ~100 m². 6–7 cm Zementestrich ≈ 130 kg/m² × 0,28 Wh/(kg·K) ≈ **3,5 kWh_th/K**. Mit OG wären es ~7 kWh_th/K, aber wie das OG versorgt wird, ist ungeklärt.
- Erlaubter Raumhub mittags +0,3 K (Komfort, Kühlfalle!) → **~5–9 kWh_th ≈ 1,1–2,0 kWh_el** (AZ ~4,5). Das reicht für das Potenzial oben **locker** (Bedarf ≤ 1,06 kWh_el/Tag). **Die Speichermasse ist also nicht der Engpass, sondern die Einspeisung.**

**Raumüberschwinger / Kühlfalle** (sicher als Risiko):
- Raum 1510 liegt im Okt 15–17 Uhr schon im Median bei **21,9–22,0 °C**. Ein Vorheizen 11–15 Uhr hebt das auf ~22,3–22,5 °C. Das ist genau die Schwelle, ab der die Raumregler früher in den **Kühlmodus** fielen und keine Wärme mehr anforderten. Der 48-h-Umbau gilt erst nach Abnahme.
- Die Raumregler ([Intelligente Raumregelung](https://www.loxone.com/dede/kb/intelligente-raumregelung/)) schließen die Stellantriebe bei Raum-Soll. **Eine reine Vorlauf-/Heizkurven-Anhebung um +2..3 K bringt deshalb wenig Wärme in den Estrich** (wahrscheinlich). Wirksam wird sie erst, wenn mittags auch das **Raum-Soll** um +0,3..0,5 K steigt.

**Takt / Mindeststehzeit** (wahrscheinlich):
- Heizläufe heute: 3–8 Starts/Tag, P_el im Lauf Median **1,75–1,85 kW** (≈ 8 kW_th bei Mindestmodulation), Lauf ~30–40 min.
- Ein Mittagsfenster mit Anhebung verlängert die Läufe (gut) und ersetzt im besten Fall 1–2 Morgenstarts. Die Starts nehmen wahrscheinlich **ab**, nicht zu.
- Die Hoval-Mindeststehzeit 15 min bleibt unberührt. Risiko: Fällt die Anhebung um 15 Uhr abrupt weg, endet ein Lauf vorzeitig und startet ggf. nach 15 min neu. Deshalb Rampe bzw. Lauf zu Ende laufen lassen (siehe Vorschlag).
- Ein Lauf braucht ~1,8 kW. Die Einspeisung liegt im Okt 11–16 Uhr im Mittel bei nur ~1,0–1,3 kWh pro Stunde. Ein Teil eines Mittagslaufs kommt deshalb aus dem Akku. Das ist nur dann billig, wenn der Akku bis zum Abend noch voll wird. Das Modell rechnet das über die Tages-Einspeisung mit ein.

## 5. Loxone-Vorschlag (nur Vorschlag, nichts umgesetzt)
Vor jeder Änderung: Backup der Projektdatei anlegen und den Skill `loxone-xml-umbau` befolgen. Alles hängt an **einem Merker „PV-Vorheizen Freigabe“**. Steht er auf 0, ist der heutige Zustand bitgenau zurück. **Das ist der Rückweg.**

**Schritt 0 (vor jedem Umbau, billiger):** Klären, warum der Akku am 13.10. 07–08 Uhr bei SOC 42 % nicht entlud (Energiemanager „MinSoc“ = 95 gesperrt, Merker „SOC_Freigabe“). Bei einer Reserve-Logik geht es um die 05–09-Uhr-Netzläufe (Okt ~7 €/Monat zu 21 ct), also um mehr als beim Vorheizen. Docs: [Energiemanager Gen. 2](https://www.loxone.com/dede/kb/energiemanager-gen-2/), [Zähler](https://www.loxone.com/dede/kb/zaehler/).

**Variante A, empfohlen als Test: Raum-Soll statt Heizkurve**
1. Bedingung „echter Überschuss“: Hauptstromzähler `actual` < −1,5 kW **seit ≥ 15 min** ([Schwellwertschalter](https://www.loxone.com/dede/kb/schwellwertschalter/) + [Monoflop](https://www.loxone.com/dede/kb/monoflop/)/Einschaltverzögerung) **UND** Akku-SOC ≥ 95 % **UND** Uhrzeit 11–15 Uhr ([Schaltuhr](https://www.loxone.com/dede/kb/schaltuhr/)) **UND** Betriebsart Heizen (48-h-Außentemperatur) **UND** Merker Freigabe.
2. Wirkung: In den UG-Raumreglern ([Intelligente Raumregelung](https://www.loxone.com/dede/kb/intelligente-raumregelung/)) die Komforttemperatur um **+0,3 K** heben, **Deckel 22,2 °C**, damit die Kühlfalle bei 22,5 °C nicht greift.
3. Ende: Fällt die Bedingung weg, das Raum-Soll **langsam** zurücknehmen (z. B. −0,1 K je 30 min). So kann der laufende Verdichterlauf zu Ende laufen und es gibt keinen Neustart nach 15 min.
4. Optional: Morgens 05–09 Uhr das Raum-Soll um −0,3 K senken, **nur wenn** `PV_Forecast_Tomorrow` am Vorabend ≥ 30 kWh war. Das zielt direkt auf die teuren Morgenläufe. Risiko Komfort am Morgen: Bei einer Zeitkonstante von ~200 h fällt der Raum in 4 h nur ~0,3 K.

**Variante B, wie gefragt: Vorlauf-Anhebung**
- Allein **wahrscheinlich wirkungsarm**, weil die Ventile bei Soll zu sind. Sinnvoll nur zusammen mit A.2. Am [Klimacontroller](https://www.loxone.com/dede/kb/klimacontroller/) nichts ändern.

**Erfolgskontrolle:** 2–3 Wochen lang Tage abwechselnd mit Merker 1/0. Danach dieses Skript-Set erneut laufen lassen (`_4` bis `_6`). Kriterien: Heiz-Grenzkosten ct/kWh, Netz-kWh 05–09 Uhr, Starts/Tag, Raum-Max 1510 < 22,3 °C. **Abbruch**, wenn ein Raumregler in den Kühlmodus geht.

## 6. Daten und Methode
- Volllogger auf dem Pi: `~/hoxpi_fulllog/2026-07-30.csv.gz … 2026-10-23.csv` (5 min, Rohwerte ×10, `25611` Roh/100 = kW). Auswertefenster **12.09. 00:00 – 23.10. 16:55** (12 012 Zeilen). Ab dann wird durchgehend geheizt, davor nur einzelne Augusttage.
- Klassifizierung je 5-min-Zeile: **Heizen** = `1539` = 1 und `1550` ≠ 1. **WW** = `1539` = 4 oder `1550` = 1. Energie = `25611`/100 × 5/60.
- Loxone (nur `control_statistics`/`control_state`/`control_describe` gelesen, kein Befehl):
  - [Hauptstromzähler](https://www.loxone.com/dede/kb/zaehler/) `<UUID>`, group 2 diff/hour: `total` = Bezug, `totalNeg` = Einspeisung.
  - Akku „LiFePO4 14,34kWh“ `<UUID>`: `total` = Entladung, `totalNeg` = Ladung (Zuordnung **wahrscheinlich**, passt zum SOC-Verlauf), SOC aus group 3 raw.
  - 8 PV-Zähler + „Victron_Solar_Charger_288“ summiert. Zusätzlich „WP Stromzähler“ `<UUID>`.
  - Energiemanager `<UUID>` als Zustand.
- **Zeitbezug sicher:** Die Korrelation WP-Stundenenergie gegen Netto-Bezug ist bei Logger = UTC+2 am höchsten (0,31 gegen 0,12 bei +1 h und 0,00 bei 0 h). Ortszeit = UTC+2 (MESZ).
- **Plausibilität sicher:** Der Loxone-WP-Zähler zeigt 355,9 kWh, das HoxPi-Integral `25611` 357,9 kWh (−0,6 %). Prüfsummen der Loxone-Abschriften sind gegen die Abfrage geprüft: Bezug 456,9, Einspeisung 298,0, PV 1544,1, Akku 454,2/477,4 kWh.
- Skripte und Ausgaben, alle unter `[lokaler Pfad]`:
  - `or_pvheiz_20261023_1_extrakt.py` → `or_pvheiz_20261023_extrakt.csv` (Pi, nur lesen; Vorbild `or_sg57_20261023_1_extrakt.py`)
  - `or_pvheiz_20261023_2_status.py/.out` (Statuscodes 1539)
  - `or_pvheiz_20261023_3_tage.py/.out` (Heiz-/WW-kWh je Tag ab 30.07.)
  - `or_pvheiz_20261023_4_auswertung.py/.out` (Stundentabelle netto, Zeitzonen-Test)
  - `or_pvheiz_20261023_5_bilanz.py/.out` (Akku/PV-Bilanz, Grenzkosten-Modell)
  - `or_pvheiz_20261023_6_potenzial.py/.out` (Tage, Außenklassen, Potenzial)
  - `or_pvheiz_20261023_7_profil.py/.out` (Stundenprofil 1490/1510, Stichproben)
  - Loxone-Abschriften: `or_pvheiz_20261023_loxone_netz_stunde.txt`, `or_pvheiz_20261023_loxone_pv_bat_stunde.txt`
  - Zwischenstände: `or_pvheiz_20261023_hh.pkl`, `or_pvheiz_20261023_L.pkl`

### Stichproben-Rohzeilen (wörtlich aus `or_pvheiz_20261023_extrakt.csv`, Spaltenfolge wie Kopf)
```
zeit,1477,1539,1550,1504,18725,18726,25611,25614,1490,1513,1510,1497
2026-10-13 07:30:01,25,1,0,0,320,45,205,30268,328,264,206,500
2026-10-13 14:40:02,128,1,0,0,385,42,232,30274,357,313,221,570
2026-10-22 04:25:01,74,1,0,0,350,42,205,30370,315,226,204,500
```
| Zeit | außen | Status | WEZ-VL | Mod | P_el | 1490 Soll | HK1-VL | Raum | Loxone-Stunde | Klasse |
|---|---|---|---|---|---|---|---|---|---|---|
| 13.10. 07:30 | 2,5 °C | Heizen | 32,0 | 45 % | 2,05 kW | 32,8 | 26,4 | 20,6 | 07–08: Bezug 3,589, Einsp 0, PV 0,034, Akku-Ent 0,003, SOC 42 | Netz 21 ct |
| 13.10. 14:40 | 12,8 °C | Heizen | 38,5 | 42 % | 2,32 kW | 35,7 | 31,3 | 22,1 | 14–15: Bezug 0,001, Einsp 4,527, PV 5,899, SOC 100 | Einspeisung 8 ct |
| 22.10. 04:25 | 7,4 °C | Heizen | 35,0 | 42 % | 2,05 kW | 31,5 | 22,6 | 20,4 | 04–05: Bezug 1,110, Einsp 0, Akku-Ent 0,653, SOC 41 | Netz 21 ct |

**Belegt:** Am 13.10. lag der Soll bei 12,8 °C außen am Nachmittag **höher** (35,7) als morgens bei 2,5 °C (32,8). Der Nachmittagslauf lief vollständig auf Einspeisung, der Morgenlauf vollständig auf Netz, obwohl der Akku noch 42 % hatte.

## 7. Nicht ermittelbar / offen
- **Warum der Akku morgens bei SOC 41–42 % nicht oder nur teilweise entlädt.** Mögliche Ursachen: Reserve, Leistungsgrenze, „MinSoc“ 95 (Energiemanager, gesperrt), „SOC_Freigabe“. Nicht untersucht, nur Zustände gelesen.
- Echte Abregelung der PV (Einspeiselimit). Ist die PV abgeregelt, wäre Überschuss 0 ct wert und das Potenzial etwas größer. Keine Daten.
- Raumtemperaturen je Raum: Die IRoomControllerV2 sind über `control_statistics` nicht chartbar, verfügbar ist nur Hoval 1510 (ein Fühler, WZ-nah).
- Wie das OG versorgt wird (HK2 in der Hoval aus). Davon hängt die nutzbare Estrichmasse ab (100 oder 200 m²).
- Heiz-AZ je Stunde: Für die Heizwärme wurde in diesem Lauf kein Wärmezähler ausgewertet. Der AZ-Vorteil mittags ist nur eine **Vermutung** (+5–10 %).
- Winterverhalten mit Akku: Es gibt keinen Winter-Datensatz mit Akku-Statistik. Die Winterzahlen sind eine **Hochrechnung** aus PV-Ertragsklassen.
- Der Tarif ist angenommen: 21 / 8 ct. Laut `claude/Warmwasser_Regeln_belegt.md` (TIWAG 17.09.2026) sind es 21,15 / 8,29 ct, im Sommerfenster netto 13,64 ct. Die Größenordnung ändert sich dadurch nicht.


---
## Korrektur 23.10.2026 ~18:10 (der Betreiber, sicher)
Die Akku-Reserve ist **gewollt**: Der Akku „LiFePO4 14,34kWh“ dient auch als **Blackout-Reserve** und wird nie ganz entladen. Eine Logik rechnet aus, wann wieder Sonne kommt und wie viel im Akku bleiben muss (MinSoc / SOC_Freigabe gehören dazu).
- Der Abschnitt „Größerer Hebel: Morgenläufe aus dem Netz“ und der Vorschlag „Akku-Reserve prüfen“ **entfallen**. Die ~7 €/Monat (Okt.) aus dem Netz sind der Preis der Notstrom-Reserve, kein Sparpotenzial.
- Bleibt gültig: PV-Vorheizen der FBH lohnt kaum (Okt. ~1,6–4 €/Monat, Winter ~0–1 €/Monat, wahrscheinlich).