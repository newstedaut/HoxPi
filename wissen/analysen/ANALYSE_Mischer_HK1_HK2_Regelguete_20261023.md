# ANALYSE Regelgüte Heizkreise HK1 (Mischer) / HK2 – 16.–23.10.2026 (Analyse-Agent, nur lesend)

**Kurz für dich, der Betreiber:** Der HK1-Mischer regelt sauber. Wenn die WP-Seite genug Temperatur liefert, hält er den Vorlauf auf ±0,3 K. Die großen Abweichungen kommen von der Versorgung, nicht vom Mischer: nach jeder WW-Ladung (HK1 wird dabei zwangsgedrosselt) und kurz vor jedem Verdichterstart, wenn der Puffer abgekühlt ist. Bis auf 3 Punkte direkt nach dem Einschalten des Heizkreises steht der Mischer nie auf 100 %. Daraus folgt **kein** Hinweis auf zu wenig Überhöhung. HK2 ist in der Hoval-Regelung abgeschaltet.

**Datenbasis:** Volllogger im 5-min-Raster, `Emulation\or_ag1_2026-10-16..21.csv.gz`, `or_ag1_2026-10-22.csv`, `or_hydraulik_20261023_raw_2026-10-23.csv`. Das sind 2196 Punkte vom 16.10. 00:00 bis 23.10. 14:55. Skripte und Ausgaben liegen unter `Emulation\or_mischer_20261023_{explore,main,ana,detail,final}.py/.out`.
**Ausgeschlossen:** Am **20.10. von 12:25 bis 17:10 war der Logger eingefroren** (58 Punkte). 1513 = 270, 1477 = 113, 1525 = 320 und 31893 = 322 sind dort identisch, obwohl 1490 sich ändert. In dieser Zeit stand der Mischerwert konstant auf 59. Das ist ein Artefakt und keine Mischer-Sättigung.

## Register (Guideline `Hoval_Modbus_Guideline_offiziell.xlsx` + `hoval_official_dp_lookup.json`)

| Reg | Bedeutung | Wert im Log |
|---|---|---|
| 1513 / 19562 | HK1 Vorlauf-Ist / Vorlauf-Soll (0,1 °C) | lebt |
| 1490 | Vorlauf-Soll Heizen HK1 (Schreibregister, Loxone) | = 19562 |
| 1501 | HK1-Status: 0 = aus, **23 = Heizbetrieb Extern/Konstantanforderung**, **6 = Zwangsdrosselung** | 0 / 23 / 6 |
| 1478 | Betriebswahl HK1 | immer 4 = Konstant |
| 19706 | HK1-Umwälzpumpe (0/1) | |
| 19658 | „Mischer“ HK1, dp1021, **S8, −100 … +100 %** (Rohwert U16, 65436 = −100) | siehe unten |
| 19610 | HK1 Rücklauf-Ist | 32768 = ungültig (kein Fühler) |
| 1514 / 19563 | HK2 Vorlauf-Ist / -Soll | 17,6–26,2 °C / immer 0 |
| 1502 / 1479 | HK2-Status / Betriebswahl | immer 0 = abgeschaltet / 0 = Standby |
| 1491 / 1494 | HK2 VL-Soll Heizen (Schreibregister) / Raum-Soll | konstant 16,5 / 5,0 °C |
| 19707 / 19659 | HK2-Pumpe / Mischer HK2 | immer 0 / immer −100 |
| 19611 | HK2 Rücklauf-Ist | ungültig |
| 19660 / 19708 | HK3 Mischer / Pumpe | immer 0 / – |
| 1539, 18726 | WP-Betriebsart (1 = Heizen, 4 = WW, 51 = Kondensatorpumpe) / Modulation | |

Bedeutung von 19658 (**wahrscheinlich, gut gestützt**): Das ist **kein Stellungswert, sondern das Stellsignal** des Mischerreglers. Es gilt 19658 ≈ −6,6 %/K × (1513 − 19562), mit P10 6,0 und P90 7,1 bei n = 283, und eine Totzone von ±0,5–0,7 K ergibt 0. Bei Überschwingen wird der Wert negativ (−4 … −17), bei abgeschaltetem Kreis ist er −100 (dauernd „Zu“). Bei einem 3-Punkt-Antrieb bedeutet das Auf/Zu-Takten. Eine echte Stellung wird nicht gemeldet. Ob der Mischer physisch am Anschlag steht, lässt sich daher nur indirekt ablesen: Das Signal bleibt dauerhaft positiv und die Abweichung bleibt trotzdem negativ.

## 1. HK1 – Kennzahlen (e = 1513 − 19562 in K, 5-min-Punkte, eingefrorener Block ausgeschlossen)

| Kollektiv | n | e Median | P10 | P90 | \|e\| Median | \|e\| P90 | e < −1 K | e < −2 K | e > +1 K |
|---|---|---|---|---|---|---|---|---|---|
| HK1 aktiv (1501 = 23), alle Punkte | 447 | −0,7 | −6,1 | +0,6 | 1,0 | 6,1 | 42 % | 27 % | 6 % |
| ohne die ersten 30 min nach dem HK-Einschalten | 278 | **−0,4** | −2,0 | +0,7 | **0,6** | **2,0** | 23 % | 9 % | 6 % |
| davon Verdichter heizt | 111 | −0,5 | −2,7 | +1,2 | 1,2 | 2,7 | 39 % | 18 % | 14 % |
| davon Verdichter aus (Puffer) | 167 | −0,4 | −1,1 | +0,3 | 0,4 | 1,2 | 12 % | 4 % | 2 % |
| ruhige Nachtblöcke 16.10. 20:35–23:50 / 18.10. 21:05–23:25 | 40 / 29 | +0,1 / −0,4 | | | Standardabweichung 0,27 / 0,16 K | | | | |

**Einschwingen nach dem HK-Einschalten** (1501 springt auf 23, 32 Fälle): Der Start liegt immer bei −6 … −16 K, weil der VL-Fühler bei stehender Pumpe abgekühlt ist. Bis |e| ≤ 0,5 K vergehen im Median **17,5 min**, maximal 55 min. **14 von 32** Fällen schaffen das nicht innerhalb von 70 min. Das sind fast immer Starts nach WW-Ladung oder bei kaltem Puffer, z. B. 20.10. 07:00 (−11,5 → −1,5 erst nach 45 min) und 23.10. 05:20 (nach 45 min noch −2,1).

**Verdichterstart bei laufendem HK1** (8 saubere Fälle, HK1 war schon > 30 min aktiv):
- 5 min vor dem Start ist e im Median **−1,85 K**. Der Puffer reicht also nicht mehr, und genau dann startet die WP.
- Bis e ≥ −0,5 K vergehen im Median **15 min** (10–20). In 2 Fällen wird das nie erreicht, das waren kurze Läufe.
- Danach folgt ein **Überschwinger** von im Median **+1,3 K** (P90 und max +2,5 K), etwa 20 min nach dem Start. In 6 von 8 Fällen liegt er über 1 K.
- 15 min nach dem Stopp ist e wieder bei −0,6 … −1,5 K.

**Schwingen:** In ruhigen Phasen ohne Verdichter gibt es **keine Eigenschwingung** (σ 0,16–0,27 K, kein Vorzeichenwechsel des Mischersignals). Die Schwankung in aktiven Blöcken hat eine Periode von **50–70 min**. Das entspricht dem WP-Takt (Unterschwingen vor dem Start, Überschwingen am Laufende) und ist **kein Reglerpendeln**. Hinweis: Das 5-min-Raster löst Schwingungen unter etwa 15 min nicht auf.

**WW-Ladung (sicher):** In allen 248 WW-Punkten ist die HK1-Pumpe 19706 = 0 und der Mischer = −100. Ist HK1 angefordert, zeigt 1501 = 6 „Zwangsdrosselung“. Das kam in 15 Blöcken zu je 10–45 min vor. Danach startet HK1 mit e ≈ −6 … −14 K und braucht 10–55 min, in mehreren Fällen über 70 min. Das ist die **größte Einzelursache** für Unterschreitungen.

**Abtauung:** Im 5-min-Raster gibt es nie `1539 = 8`. `ww_hires` hat keinen HK1-VL (1513). → **nicht ermittelbar**.

## 2. HK2

- **Sicher:** HK2 ist in der Hoval-Regelung abgeschaltet. Betriebswahl 1479 = 0 (Standby), Status 1502 = 0, VL-Soll 19563 = 0 und Pumpe 19707 = 0 gelten in allen 2196 Punkten. Die Schreibregister 1491 = 16,5 °C und 1494 = 5,0 °C stehen fest, haben aber keine Wirkung.
- 1514 (HK2-VL) liegt bei 17,6–26,2 °C (Median 19,9) und ist damit Raum- bzw. Kellerniveau. Der Fühler ist angeschlossen, aber kein Wasser fließt.
- **Wahrscheinlich ist HK2 als Mischerkreis konfiguriert:** 19659 steht dauernd auf −100 („Zu“), während HK3 bei 19660 = 0 steht, also nicht konfiguriert ist.
- Kennzahlen für HK2: **keine**, weil der Kreis nie aktiv war. Ob das OG über HK1 oder eine eigene Grundfos-Pumpe außerhalb der Hoval-Regelung läuft, ist **nicht ermittelbar** (siehe Vorbefund).

## 3. Mischerstellung / Anschlag

- Eine Mischerstellung im eigentlichen Sinn steht nicht im Log, nur das Stellsignal 19658.
- **≥ 90 % kommt in 3 von 447 Punkten vor, = 100 % in 2.** Alle drei liegen im **ersten 5-min-Punkt nach dem HK-Einschalten** (kalter Fühler): 16.10. 12:45 (96), 18.10. 14:20 (100), 22.10. 13:15 (100).
- Im Regelbetrieb ist der Median 0, der Großteil liegt zwischen −10 und +35. Ein dauerhaft hohes Signal als Zeichen für einen Anschlag gibt es außer dem eingefrorenen 20.10.-Block nicht.
- **Wahrscheinlich steht der Mischer phasenweise physisch auf „ganz auf“:** 20–40 min nach der WW-Ladung bleibt das Signal dauerhaft bei +20 … +45, während e bei −3 … −6 K hängt. Das betrifft etwa 9 % der Regelzeit (e < −2 K). Dann reicht die Versorgungstemperatur nicht. Mehr Überhöhung hilft dort nicht, weil die WP in dieser Phase noch nicht oder gerade erst im Heizbetrieb läuft.
- → **Kein Hinweis auf zu wenig Überhöhung im eingeschwungenen Betrieb.**

## 4. Stichproben (Rohwerte, °C-Register ×0,1)

| Zeit | Datei | Rohwerte | Aussage |
|---|---|---|---|
| 2026-10-20 07:20:02 | or_ag1_2026-10-20.csv.gz | 1501=23 1539=1 18726=42 **1513=254 19562=311 19658=36** 19706=1 31893=308 1525=310 | 40 min nach WW: e = −5,7 K, Signal +36 (≈ 6,3 %/K); WP-VL selbst nur 30,8 °C → Versorgung limitiert |
| 2026-10-20 08:20:02 | dto. | 1513=313 19562=311 **19658=0** 1539=1 31893=401 | eingeschwungen: e = +0,2 K, Signal 0 (Totzone) |
| 2026-10-17 10:20:02 | or_ag1_2026-10-17.csv.gz | 1539=1 **1513=321 19562=296 19658=65521 (=−15)** 1525=395 | Überschwinger +2,5 K am Laufende (Soll war von 302 auf 296 gesunken) |
| 2026-10-23 09:45:02 → 10:20:02 | or_hydraulik_20261023_raw_2026-10-23.csv | 09:45: 1513=291 19562=319 19658=17 1539=1; 10:05: 1513=316 19658=0; 10:20: **1513=329 19562=317 19658=65528 (=−8)** 31893=406 | Verdichterstart bei e = −2,8 K → nach 20 min −0,2 → nach 35 min +1,2 K |
| 2026-10-18 14:20:02 | or_ag1_2026-10-18.csv.gz | 1501=23 1539=0 **1513=200 19562=352 19658=100** | einer von 2 Punkten mit 100 %: erster Punkt nach HK-Ein, kalter Fühler |
| 2026-10-18 17:50:02 | dto. | **1501=6** 1539=4 19706=0 19658=65436 (=−100) 1513=253 1525=600 | WW-Ladung → HK1 zwangsgedrosselt, Pumpe aus, Mischer zu |
| 2026-10-16 21:00:01 | or_ag1_2026-10-16.csv.gz | 1501=23 1539=0 1513=236 19562=240 19658=0 | Ruhephase aus dem Puffer: e = −0,4 K |
| 2026-10-20 07:20:02 | or_ag1_2026-10-20.csv.gz | 1479=0 1502=0 19563=0 19707=0 19659=65436 1491=165 1514=199 | HK2 aus, Mischer HK2 dauernd zu |
| 2026-10-20 12:25:01 … 17:10:01 | or_ag1_2026-10-20.csv.gz | 1513=270 1477=113 1525=320 31893=322 19658=59 in 58 Punkten identisch | eingefrorener Logger, ausgeschlossen |

## 5. Bewertung

**Sicher**
- Der HK1-Mischer hält den Sollwert im eingeschwungenen Betrieb sehr gut (σ ≤ 0,3 K) und hat keine Eigenschwingung.
- Bei jeder WW-Ladung wird HK1 komplett abgeschaltet (Status 6 Zwangsdrosselung, Pumpe aus). Danach dauert es 10–55 min, in mehreren Fällen über 70 min, bis der Sollwert wieder erreicht ist.
- Mischersignal ≥ 90 % kommt nur in den ersten 5 min nach dem HK-Einschalten vor (3 Punkte).
- HK2 ist in der Hoval-Regelung inaktiv. Für HK1 und HK2 gibt es keinen gültigen Rücklauffühler (19610/19611 ungültig).

**Wahrscheinlich**
- 19658 ist das Stellsignal eines P-artigen Reglers für einen 3-Punkt-Antrieb (≈ 6,6 %/K, Totzone ±0,5 K). Eine Position wird nicht gemeldet.
- Unterschwinger vor dem Verdichterstart (−1,9 K) und nach WW (−3 … −6 K) entstehen, weil die **Versorgung zu kalt** ist und der Mischer dann ganz offen steht. Die Mischerregelung selbst ist nicht die Ursache.
- Der Überschwinger von +1,3 K am Laufende entsteht, weil WP-VL bzw. Puffer schnell steigen (3,5–4 K je 20 min) und der Mischer mit kleinem Signal (−7 %/K) langsam zufährt. Teilweise sinkt auch der Loxone-Soll während des Laufs.

**Vermutung**
- Bei einer Fußbodenheizung mit ~100 m² Estrich wirken sich ±1–2 K VL-Abweichung für 15–30 min kaum auf den Raum aus. Die 30–60 min Unterversorgung nach jeder WW-Ladung (etwa 2× täglich) sind dagegen spürbar, zumindest im Energieeintrag.

## 6. Einstellvorschlag (nur Vorschlag – nichts geändert)

1. **Mischerparameter von HK1 (Laufzeit, P-Band) nicht anfassen.**
   *Was bringt uns das:* Nichts zu verlieren. Der Regler ist stabil und präzise, und eine schärfere Einstellung würde nur die Überschwinger vergrößern.
2. **Überhöhung (die +3,0 K zwischen 19562 und 1520/1529) nicht auf 1,5 K senken, sondern höchstens auf 2,0 K testen.** Das war Vorschlag 1 im Hydraulik-Vorbefund. Die Daten zeigen, dass die Unterschreitungen genau dann auftreten, wenn die Versorgung zu knapp ist. Eine niedrigere Überhöhung verschärft das tendenziell.
   - Test: 3–4 Tage mit 2,0 K am Bedienteil, Menüname **zu prüfen**.
   - Rückweg: zurück auf 3,0 K. Den aktuellen Wert vorher fotografieren.
   - Abbruchkriterium: Der Anteil e < −1 K (ohne die ersten 30 min nach dem Einschalten) steigt von heute **23 %** auf über 35 %, oder die Raumtemperaturen fallen.
   - *Was bringt uns das:* WP-VL etwa 1 K tiefer, COP grob +2–3 %. Das Risiko ist mehr Unterversorgung. Der Effekt ist nur durch den Test sicher bestimmbar.
3. **Größerer Hebel liegt bei der WW-Ladung:** Die Zwangsdrosselung kommt von der WW-Vorrangschaltung, und die ist bei einer WP mit einem Verdichter sinnvoll. Zwei Optionen über Loxone bzw. das Zeitprogramm:
   - WW-Ladungen in Zeiten legen, in denen HK1 ohnehin aus ist oder kaum Bedarf hat (Mittag oder Nachmittag).
   - Vermutung, zu prüfen in der Loxone-Logik: Loxone fordert nach dem HK-Einschalten teils 35–36 °C an (z. B. 16.10. 12:45 und 20.10. 12:20 1490 = 359, 18.10. 14:20 1490 = 352). Ob das gewollt ist, ist offen, denn ein hoher Soll direkt nach WW zieht den Puffer schneller leer.
   - *Was bringt uns das:* Weniger und kürzere Unterversorgungsphasen (heute 15 Blöcke à 10–45 min plus 10–55 min Aufholen pro Woche), ohne die WP-VL anzuheben.
   - Rückweg: altes Zeitprogramm bzw. alte Loxone-Logik sichern.
4. **Ohne Änderung, nur messen:** Logger-Raster für 1513, 19658 und 1539 auf 1 min verdichten, rein lesend und nur Pollrate. *Was bringt uns das:* Abtauung und Schwingen unter 15 min werden sichtbar, und man erkennt, ob der Mischer nach WW wirklich am Anschlag steht.

## 7. Nicht ermittelbar

- Physische Mischerstellung, nur das Stellsignal 19658 liegt vor. Damit auch nicht, ob und wie lange der Mischer am Anschlag steht.
- HK1- und HK2-Rücklauf (19610/19611 ungültig) sowie der Durchfluss im HK.
- Verhalten bei Abtauung (kein `1539 = 8` im 5-min-Raster, kein 1513 in `ww_hires`).
- Schwingungen mit einer Periode unter etwa 15 min (5-min-Raster).
- Regelkennzahlen HK2 (der Kreis war nie aktiv). Außerdem, wie das OG hydraulisch versorgt wird.
- Mischer-Laufzeit, P-Band und Menüname der Überhöhung (nicht auf dem Bus geloggt).
- Daten vom 20.10. 12:25–17:10 (Logger eingefroren).