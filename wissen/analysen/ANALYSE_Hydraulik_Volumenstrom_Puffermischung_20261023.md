# ANALYSE Hydraulik WP-Kreis / Puffer / Heizkreis – Volumenstrom und Puffermischung (23.10.2026, Analyse-Agent, nur lesend)

**Frage:** Wie arbeitet die Hydraulik zwischen WP-Kreis und Puffer/Heizkreisen im Heizbetrieb 16.–23.10.2026?

**Datenbasis**
- Volllogger 5-min: `~/hoxpi_fulllog/2026-10-16 … 21.csv.gz` (Kopien `Emulation\or_ag1_2026-10-1x.csv.gz`), `2026-10-22.csv` (Kopie `or_ag1_2026-10-22.csv`), `2026-10-23.csv` frisch kopiert bis 14:55 → `Emulation\or_hydraulik_20261023_raw_2026-10-23.csv`. 2196 Punkte, 16.10. 00:00 – 23.10. 14:55.
- `ww_hires.csv` ab 16.10. kopiert (`or_hydraulik_20261023_raw_ww_hires.csv`), hat **keinen** Volumenstrom → nur am Rand genutzt.
- Registerbedeutung: `hoval_official_dp_lookup.json`, `hoval_datapoints_f2_20260904\hydraulics_fg60_fn7.csv` (CAN-dp 257/258/302 ↔ Modbus 31893/[Nummer]).
- Skripte/Ausgaben: `Emulation\or_hydraulik_20261023_main.py`, `_runs.py/.out`, `_detail.py/.out`, `_proben.py/.out`, `_names.py`.

**Register (verwendet)**
| Reg | Bedeutung | Einheit |
|---|---|---|
| 31708 | Volumenstrom gemittelt (WP-Kreis, fg60/fn7 dp302) | 0,1 l/min |
| 31893 / 31895 | WP-Vorlauf / WP-Rücklauf (dp257/258; Name in Hoval-Liste verschoben) | 0,1 °C |
| 1525 / 18760 | WEZ-Temperatur / Anlagen-Vorlauf Heizen | 0,1 °C |
| 1535 (=18742) | Rücklauf WEZ | 0,1 °C |
| 1513 / 1514 | Vorlauf-Ist HK1 / HK2 | 0,1 °C |
| 19562 (=1490) | Vorlauf-Soll HK1 (= Loxone-Konstantanforderung) | 0,1 °C |
| 1520 = 1529 = 1531 | HK-/WEZ-Soll | 0,1 °C |
| 19658 / 19706 | Mischer HK1 % / Pumpe HK1 (0/1) | |
| 19659 / 19707 | Mischer HK2 / Pumpe HK2 | |
| 27496 | Drehzahl WP-Umwälzpumpe CP (−1 = aus) | % |
| 25612 / 18732 / 25611 | Q_th (ganze kW) / Leistung Heizen (0,1 kW) / P_el (0,01 kW) | kW |

**Methode:** Heizlauf = zusammenhängende 5-min-Punkte mit `1539 = 1` und `18726 > 0` (29 Läufe, 175 Punkte). Erster Punkt je Lauf (Anlauf) verworfen → 146 Punkte. Q_ber = 31708/10 × (31893 − 31895)/10 × 4,18/60 kW (≙ V̇[m³/h] × 1,16 × ΔT). WW = `1539 = 4`. Abtauung (`1539 = 8`) kommt im 5-min-Raster **nicht** vor; kurze Abtauungen sind darin nicht auflösbar.

**Wichtige Datenlücke:** `31893/31895` standen **bis 17.10. 12:25 eingefroren** auf 30,7 / 29,4 °C (erste Änderung 17.10. 12:30:01). Die 10 Läufe 16.10.–17.10. 10:20 zeigen deshalb falsch ΔT 1,3 K / Q_ber 3,1 kW. Ausgewertet wird ΔT/Q nur ab 17.10. 12:30 („live“, 19 Läufe, 106 Punkte). Für 16./17.10. gelten `1525`/`1535` als Ersatz (live-Abweichung zu 31893/31895 im Median −0,1 / +0,1 K).

## 1. Ergebnisse – WP-Kreis je Heizlauf (Mediane je Lauf, ohne Anlaufpunkt)

| Start | Ende | Pkt | AT °C | V̇ l/min | CP % | WP-VL | WP-RL | ΔT K | Q_ber kW | 25612 kW | HK1-VL 1513 | 1513 − WP-VL | Mischer % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 17.10. 18:00 | 18:20 | 5 | 14,4 | 34,4 | 80 | 39,5 | 35,3 | 4,2 | 10,1 | 10 | 32,6 | −7,0 | 18 |
| 18.10. 07:55 | 08:15 | 5 | 10,1 | 34,2 | 80 | 37,4 | 33,3 | 4,1 | 9,7 | 10 | 30,3 | −7,1 | −3 |
| 18.10. 14:40 | 14:55 | 4 | 16,1 | 34,3 | 80 | 37,9 | 32,7 | 5,0 | 12,0 | 12 | 30,1 | −7,6 | 33 |
| 18.10. 18:25 | 18:35 | 3 | 13,4 | 34,4 | 80 | 36,6 | 32,4 | 4,3 | 10,2 | 10 | 29,3 | −7,4 | 4 |
| 19.10. 07:20 | 07:35 | 4 | 9,7 | 34,2 | 80 | 34,1 | 30,1 | 4,0 | 9,5 | 9 | 27,8 | −6,3 | 18 |
| 19.10. 09:15 | 09:35 | 5 | 9,9 | 34,4 | 80 | 37,2 | 33,3 | 4,0 | 9,5 | 9,5 | 30,7 | −6,6 | −1 |
| 20.10. 07:20 | 08:20 | 13 | 8,7 | 34,3 | 80 | 36,7 | 32,8 | 3,9 | 9,3 | 9 | 30,7 | −6,1 | 3 |
| 20.10. 09:00 | 09:30 | 7 | 8,8 | 34,3 | 80 | 37,6 | 33,8 | 3,8 | 9,1 | 9 | 31,1 | −6,6 | 0 |
| 20.10. 10:25 | 10:45 | 5 | 9,5 | 34,2 | 80 | 38,1 | 34,2 | 3,9 | 9,3 | 9 | 31,0 | −7,2 | 0 |
| 21.10. 17:30 | 17:50 | 5 | 12,8 | 34,2 | 80 | 36,8 | 32,6 | 4,2 | 9,9 | 10 | 29,9 | −6,9 | −3 |
| 22.10. 04:25 | 05:00 | 8 | 7,4 | 34,3 | 80 | 37,7 | 34,1 | 3,6 | 8,6 | 9 | 31,0 | −6,7 | 0 |
| 22.10. 07:25 | 07:45 | 5 | 6,5 | 34,3 | 80 | 37,6 | 34,1 | 3,5 | 8,4 | 8 | 31,4 | −6,3 | 3 |
| 22.10. 08:20 | 08:30 | 3 | 6,4 | 34,3 | 80 | 35,4 | 32,0 | 3,4 | 8,0 | 8 | 29,8 | −5,6 | 11 |
| 23.10. 03:05 | 03:40 | 8 | 2,7 | 34,2 | 80 | 36,9 | 33,0 | 3,9 | 9,3 | 9 | 30,3 | −6,7 | 21 |
| 23.10. 05:40 | 07:20 | 21 | 1,8 | 34,3 | 80 | 37,9 | 34,7 | 3,2 | 7,6 | 8 | 32,3 | −5,9 | 5 |
| 23.10. 08:10 | 08:50 | 9 | 2,3 | 34,3 | 80 | 38,5 | 35,3 | 3,2 | 7,6 | 8 | 32,2 | −6,3 | 0 |
| 23.10. 09:45 | 10:20 | 8 | 2,2 | 34,4 | 80 | 38,5 | 35,3 | 3,2 | 7,7 | 8 | 31,6 | −6,9 | 0 |
| 23.10. 11:10 | 11:35 | 6 | 4,6 | 34,1 | 80 | 38,1 | 34,7 | 3,4 | 8,1 | 8 | 31,0 | −7,1 | 0 |

(21.10. 15:30 nur 1 Punkt, weggelassen. 16./17.10. vormittags: 10 Läufe, V̇ 34,2–34,4 l/min, CP 80 %, ΔT nicht auswertbar wegen Einfrieren. Volle Tabelle inkl. dieser Läufe: `or_hydraulik_20261023_runs.out`.)

**Gesamt Heizen live (106 Punkte):** V̇ 34,3 l/min (min 33,9 / max 34,5) = **2,06 m³/h**, CP immer 80 %, WP-VL 37,65 °C, WP-RL 33,8 °C, **ΔT 3,7 K**, Q_ber 8,8 kW. Summe Q_ber / Summe 25612 = **0,995**, / 18732 = 1,056.
**WW (Verdichter an, 247 Punkte):** CP moduliert 13–80 %, V̇ 18,4–37,8 l/min (Median 22,8), ΔT 5,7 K (live), Q_ber / 25612 = 0,991.
**Stillstand mit Pumpe (1539 = 0, CP 30 %, 332 Punkte):** V̇ Median **16,4 l/min** (≈ 0,98 m³/h); CP −1 → V̇ 0 (1436 von 1438 Punkten).

## 2. Ergebnisse – Heizkreis-Seite

| Größe (Heizen live, Median) | Wert |
|---|---|
| HK1-VL-Ist 1513 | 31,0 °C |
| HK1-VL-Soll 19562 (= Loxone 1490) | 31,1–33,2 °C; 1513 − 19562 = −0,7 K |
| WEZ-/HK-Soll 1529 = 1520 | jeweils 19562 + 2,9–3,0 K (311→340, 315→345, 330→360) |
| WP-VL − 1529 | +2,7 K; WP-RL 1535 − 1529 = −1,0 K |
| 1513 − WP-VL | **−6,2 K** (alle Läufe −5,6 … −7,6 K) |
| 1513 − WP-RL | **−2,8 K**; HK1-VL < WP-RL in **106 von 106** Punkten |
| 18760 Anlagen-VL − WP-VL | 0,0 K (sitzt im WP-Vorlauf, nicht am Pufferaustritt) |
| Pumpe HK1 19706 | an in 146/146 Heizpunkten; bei WW 0/247; außerhalb Heizen/WW 360 von 1777 Punkten an |
| Mischer HK1 19658 | Median 5 %, Werte −10 … +33, häufigster Wert 0 |
| HK2: 1514 / 19707 / 19659 | 1514 ≈ 19–20 °C (lebt, aber Raumniveau), Pumpe immer 0, Mischer immer −100 → HK2 in der Hoval-Regelung **nicht aktiv** |
| HK-Rücklauf | **kein Register** am Bus geloggt (kein HK-RL-Fühler) |

## 3. Volumenstrom WW vs. Heizen, Wartezeit vor Start

| Zustand | CP % | V̇ l/min (Median) | Quelle |
|---|---|---|---|
| Heizen, Verdichter an | 80 (fix) | 34,3 | 146 Pkt |
| WW-Ladung, CP = 80 % | 80 | **37,5** (n = 21) | z. B. 18.10. 17:50–18:00: 375/375/373 |
| WW-Ladung, CP = 13 % (Endphase) | 13 | 18,7 (n = 70) | |
| Stillstand, Heizanforderung aktiv | 30 | 16,4 (15,2–17,1) | 332 Pkt, HK1-Pumpe in 331 davon an |
| Pumpe aus | −1 | 0 | 1436 Pkt |

- Vor **23 von 29** Heizstarts lief die WP-Pumpe ≥ 15 min mit CP 30 % (V̇ 15,6–16,6 l/min, Verdichter aus, `1539 = 0`, HK1-Pumpe an). Vor den übrigen 6 (16.10. 05:50, 14:50; 19.10. 09:15; 21.10. 15:25; 22.10. 04:25; 23.10. 03:05) stand die Pumpe (CP −1) – das sind Starts direkt nach Wiederkehr der Loxone-Anforderung.
- Nach Laufende: CP 30 % läuft weiter, solange `1501 = 23` bleibt; fällt die Loxone-Anforderung weg, folgt CP −1 / V̇ 0 innerhalb ≤ 10 min.
- `1539 = 51` (Kondensatorpumpe) 4× gesehen, jeweils CP 80 %, V̇ 27–37 l/min (Vorspülen vor Start, z. B. 23.10. 11:05:02).
- Gleiche Pumpenstufe 80 %: WW 37,5 l/min, Heizen 34,3 l/min → der Heizweg hat einen **höheren Widerstand** als der WW-Weg (−3,2 l/min, −9 %). Das ist ein Hinweis, dass das Umschaltventil zwei hydraulisch getrennte Wege schaltet (belegt: unterschiedlicher Durchfluss; Ventiltyp selbst nicht ermittelbar).

## 4. Zwei Stichproben zum Gegenprüfen (Rohwerte, Registerrohwerte ×0,1 wo °C/l/min)

**A) Heizen, `~/hoxpi_fulllog/2026-10-20.csv.gz`, Zeile `2026-10-20 07:40:01`:**
`1539=1 1501=23 18726=35 27496=80 31708=344 31893=349 31895=309 1525=350 18760=350 1535=310 1513=286 19658=15 19706=1 25612=9 18732=94 25611=166 1477=87 1490=311 1520=340 1529=340 19562=311`
→ 34,4 l/min × (34,9 − 30,9) K × 4,18/60 = **9,6 kW** (25612 = 9, 18732 = 9,4). HK1-VL 28,6 °C < WP-RL 30,9 °C < WP-VL 34,9 °C.

**B) Heizen, `~/hoxpi_fulllog/2026-10-23.csv`, Zeile `2026-10-23 06:30:01`:**
`1539=1 1501=23 18726=35 27496=80 31708=344 31893=378 31895=346 1525=380 18760=380 1535=345 1513=323 19658=5 19706=1 25612=8 18732=76 25611=182 1477=19 1490=330 1520=360 1529=360 19562=330`
→ 34,4 × 3,2 × 4,18/60 = **7,7 kW** (25612 = 8, 18732 = 7,6). HK1-VL 32,3 °C < WP-RL 34,6 °C < WP-VL 37,8 °C. HK1-Soll 33,0, WEZ-Soll 36,0.

Ergänzend Stillstand: `2026-10-20 07:10:01` `1539=0 27496=30 31708=165 31893=264 31895=263 1513=268 19706=1` (Pumpe 30 %, 16,5 l/min, ΔT 0,1 K).
Prüfbefehl: `zcat ~/hoxpi_fulllog/2026-10-20.csv.gz | awk -F, 'NR==1||/^2026-10-20 07:(10|40)/'` und Spalten per Header-Name suchen.

## 5. Bewertung

**Belegt**
- `31708` ist der WP-Kreis-Durchfluss in **0,1 l/min**: Q = V̇ × ΔT × 4,18/60 trifft die gemeldete Wärmeleistung 25612 auf **99,5 %** (Heizen) bzw. 99,1 % (WW). 18741/18756 (Volumenstrom) bleiben tot = 0.
- Im Heizbetrieb läuft die WP-Pumpe **fest auf 80 %** → **34,3 l/min ≈ 2,06 m³/h** (≈ 94 % der Hoval-Nennmenge 2,2 m³/h). Die Spreizung ist dadurch klein: **3,2–5,0 K** (Median 3,7 K) bei 7,6–12 kW.
- HK1 ist ein **Mischerkreis**: HK1-VL 1513 folgt dem Loxone-Sollwert 19562 (−0,7 K) und liegt **6,2 K unter WP-VL** und **2,8 K unter WP-RL** – in allen 106 Live-Punkten.
- Die Hoval-Regelung schlägt auf den HK-Sollwert **+3,0 K** auf (1529 = 19562 + 3,0) und hält den WP-**Rücklauf** an diesem Wert (1535 − 1529 = −1,0 K). Ergebnis: WP-VL ≈ HK-Bedarf + 6–7 K.
- HK2 ist in der Hoval-Regelung nicht aktiv (Pumpe 19707 immer 0, Mischer 19659 immer −100). Einen HK-Rücklauf- oder Pufferfühler gibt es am Bus nicht (27493/27494 ungültig, siehe Stale-Analyse).
- Korrektur zu `ANALYSE_Speicherrollen…`: `1513` steigt bei WW-Ladung **nicht** mit (18.10. 17:50: 1513 = 25,3 °C bei WP-VL 59,9 °C). Der in ww_hires „Vorlauf“ genannte Wert ist der Anlagen-VL ([Nummer]), nicht HK1.

**Physikalisch zwingend (aus belegten Werten)**
- Der HK-Rücklauf ist im Heizbetrieb kälter als der HK-Vorlauf (≤ 31 °C). Der WP-Rücklauf (33,8 °C) liegt also **mindestens 2,8 K über dem HK-Rücklauf**. Das Wasser, das zur WP zurückkommt, ist nicht reiner HK-Rücklauf, sondern enthält WP-Vorlaufwasser, das durch den Puffer direkt zurückläuft.
- Damit ist die Hoval-Regel „HK-Durchfluss ≤ Speicherkreis“ **eingehalten** (eher übererfüllt): Der Mischer zieht weniger aus dem Puffer, als die WP hineindrückt. Wäre es umgekehrt, läge WP-RL ≈ HK-RL < HK-VL – das kommt in keinem Punkt vor.

**Wahrscheinlich**
- Abschätzung Primärentnahme HK1 (Annahme HK-RL, nicht gemessen; Puffer-Aufladung vernachlässigt): HK-RL 26 / 28 / 30 °C → Anteil (37,65 − 33,8)/(37,65 − RL) = 33 / 40 / 50 % → **11–17 l/min**, d. h. **~17–23 l/min der 34,3 l/min laufen über den Puffer direkt zurück** in die WP.
- Folge: Der Rücklauf steigt im Lauf schnell, die WP erreicht ihre Abschaltschwelle (RL ≥ Soll + 2…2,5 K) früh → kurze Läufe; die Hydraulik verstärkt den in `ANALYSE_Heizlauf_Enden…` beschriebenen „b-Typ“-Abschaltgrund.
- Die Pumpe läuft im Stillstand mit 30 % (16 l/min), weil es keinen gültigen Pufferfühler gibt: Die WP „misst“ den Puffer über den eigenen Rücklauf. Nebenwirkung: Der Puffer wird dabei durchmischt (ΔT 0,1 K im Stillstand, Stichprobe 20.10. 07:10).
- WP-VL 6–7 K über dem HK-Bedarf kostet Effizienz. Faustregel 2–2,5 % COP je K → **Größenordnung 10–15 %**, davon ist nur ein Teil vermeidbar (der Mischer braucht etwas Überhöhung).

## 6. Vorschlag (nur Vorschlag, nichts geändert)

1. **Überhöhung Mischerkreis am Bedienteil ablesen.** Im HK1-Parametermenü den Wert suchen, der die +3,0 K zwischen 19562 und 1529 erzeugt (bei Hoval TopTronic E typisch „Überhöhung Vorlauf Mischerkreis“ o. ä. – genauer Name **zu prüfen**). Probeweise 3 → 1,5 K.
   *Was bringt uns das:* WP-VL sinkt um ~1,5 K bei gleicher Raumwärme → COP grob +3–4 %. Kontrolle: 1513 muss weiter 19562 erreichen (Abweichung < 0,5 K), sonst zurück.
2. **Grundfos-Pumpen ablesen** (Typ, Regelart, Stufe, angezeigter Durchfluss/Leistung – Foto vom Display/Typenschild). Besonders: wo hängt die OG-Pumpe hydraulisch, da HK2 in Hoval nicht aktiv ist?
   *Was bringt uns das:* Erst damit ist der HK-Durchfluss bekannt und die Abschätzung „17–23 l/min Kurzschluss über den Puffer“ prüfbar.
3. **Zwei Anlegefühler** (Loxone oder Thermometer) an HK1-Rücklauf und an den Puffer-Abgang zum Mischer.
   *Was bringt uns das:* HK-RL und Puffer-Austrittstemperatur werden messbar; Mischanteil, Pufferschichtung und der echte Bedarf an Überhöhung lassen sich dann rechnen statt schätzen.
4. **Hydraulikschema/Foto Puffer-Anschlüsse** (welche Stutzen WP-VL/RL, HK-VL/RL; Trennspeicher 4-Rohr oder Weiche?).
   *Was bringt uns das:* Klärt, ob der beobachtete Rücklauf-Kurzschluss bauartbedingt (Trennspeicher, gewollt) oder ein Anschlussproblem ist.
5. **Nicht empfohlen ohne Punkt 2–3:** WP-Pumpe im Heizbetrieb drosseln (falls ein Parameter dafür existiert). Weniger WP-Durchfluss würde den Kurzschluss verringern, aber bei Rücklaufregelung den WP-VL anheben – Netto-Effekt **nicht ermittelbar**.

## 7. Nicht ermittelbar (mit diesen Daten)

- HK1-/HK2-Rücklauftemperatur und HK-Durchfluss (kein Register, kein Fühler).
- Puffertemperaturen oben/unten (27493/27494 ungültig, kein anderer Fühler).
- Bedeutung der Mischerwerte 19658 (Stellung oder Stellbefehl? Werte −10 … +33 % bei erreichtem Sollwert).
- Ob die OG-Fußbodenheizung über HK1 läuft (HK2 inaktiv; 1514 ≈ Raumniveau).
- ΔT/Q der Läufe 16.10.–17.10. 10:20 (31893/31895 eingefroren bis 17.10. 12:25).
- Abtauungen (im 5-min-Raster nie `1539 = 8`); Volumenstrom während Abtauung.
- Typ/Leckage des Umschaltventils (nur der unterschiedliche Durchfluss 34,3 vs. 37,5 l/min bei 80 % ist belegt).
- Name/Menüort des Parameters für die +3 K Überhöhung und ob die Pumpendrehzahl Heizen (fix 80 %) verstellbar ist.