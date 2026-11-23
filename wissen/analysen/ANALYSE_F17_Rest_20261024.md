# F17-Rest: #12, Abendanforderungen mit 30,0 °C, Herkunft der 30,0-°C-Sollwerte, neue Starts (24.10.2026)
Analyse-Agent 24.10.2026, 15:00 bis 15:20. Strikt nur lesend: kein Schreiben an Anlage, CAN, X26, X4 oder Kälteregler, keine Bus-Probes, kein Dienst neu gestartet, nichts gelöscht. Katalogfrage F17.
Vorlauf: `[lokaler Pfad]` (Modell A, 49/54 Segmente).

## Frage
Das Modell A erklärt #4 und #25. Offen waren noch:
- (a) Fall #12 mit dem 64-s-Zwischensoll 30,0 °C,
- (b) vier Abendanforderungen mit S = 30,0 °C ohne Freigabe,
- (c) die Herkunft der kurzen 30,0-°C-Sollwerte,
- (d) die neuen Heizstarts seit 24.10. 11:00.

## Ergebnis in 5 Zeilen
1. **(b) gelöst:** Die Freigabe-Bedingung braucht zusätzlich **VL ≤ S** (WEZ-Vorlauf, X26 B17). In allen vier Abendfällen war VL beim Eintreffen der Anforderung 1,0 bis 6,0 K **über** S. Danach lag RL nach 7 bis 90 s für den Rest der Anforderung (94 bis 229 min) über 28,5 °C. Die Bedingung war also nie 15 min lang erfüllt. Mit diesem Zusatz trifft das Modell 53/54 Segmente (vorher 49/54). Messung **sicher**, Regel **wahrscheinlich**.
2. **(a) #12 bleibt offen** (Δ −2,8 min). Keine getestete Variante rettet #12, ohne andere Fälle zu brechen: Reset-Entprellung 65 bis 120 s bricht 18.10. 17:05, Reset-Hysterese 0,5 K bricht 23.10. 09:41 und 18.10. 17:05. Wahrscheinlich ein Auflösungs-Grenzfall (B29 in 0,5-K-Stufen, RL 29,0 gegen eine Schwelle von 28,5). Das ist eine **Vermutung**.
3. **(c) Herkunft:**
   - Die langen Abendwerte von 30,0 °C kommen aus dem **Ofen-Nachlauf**: Loxone schreibt 1490 = 24,0 °C, die TopTronic macht daraus 1520 = 30,0 °C (**sicher**, Volllogger).
   - Die kurzen 30,0-°C-Spitzen beim Anfordern kommen aus einem **Loxone-Zwischenwert** von 1490 ≈ 15,1 bis 15,4 °C, der 2 bis 10 s vor dem eigentlichen Soll geschrieben wird (**sicher** laut Log der Bridge ab 23.10. 19:47; dass dieser Wert die 30,0-°C-Spitze in M0 verursacht: **wahrscheinlich**).
   - Abbildung: M0 = max(30,0; 1490 + 3 K, abgerundet auf 0,5 K) (**wahrscheinlich**, 9 von 9 Stichproben).
4. **(d)** Seit 11:00 gab es 2 neue Heizfreigaben (11:43:28, 13:30:59), beide im Band: Δ −0,35 und +0,02 min. Am ganzen 24.10. waren es 5 von 5 (Modell A+VL und auch das alte Modell A).
5. **Regelstand:** Mit Modell A+VL passen **30 von 31 Heizstarts** (16.10. bis 24.10. 14:55) und **61 von 62 Segmenten**. Einziger Ausreißer ist #12.

## Datenbasis (alles nur gelesen)
- **X26-Ereignisliste 16. bis 23.10.:** `[lokaler Pfad]` aus der Vorarbeit.
- **X26 am 24.10. (neu):** Quelle am Pi `/home/<user>/rs485_sniff/log/rs485_2026-10-24.log` (laufende Datei, 93 MB, Stand 14:56). Ausgewertet mit dem vorhandenen Parser `/home/<user>/rs485_sniff/rs485_9600parse.py`, nur CRC-gültige Rahmen. Ergebnis lokal: `[lokaler Pfad]`. Ein zweiter Lauf bis 15:04 liegt am Pi unter `/tmp/or_f17r_ev24b.txt`. Danach kam nur noch WW (15:00:58, M0 = M1 = 112), kein Heizstart.
- **Volllogger am Pi**, 5 min, Rohwerte ×10: `/home/<user>/hoxpi_fulllog/2026-10-16.csv.gz` … `2026-10-24.csv`, Register 1490, 1520, 1501, 1510. Auszug lokal: `[lokaler Pfad]`.
- **Log der Bridge (neu als Quelle):** `journalctl -u hoval-bridge`, Zeilen `SET reg 1490 … <- N (raw)` mit Millisekunden. Das Journal reicht nur zurück bis **23.10. 19:47:10**. Auszug lokal: `[lokaler Pfad]` (303 Schreibvorgänge).
- **Definitionen** wie in der Vorarbeit:
  - S = M0 · 0,5 °C,
  - RL = (B29 − 21)/2, VL = (B17 − 21)/2,
  - Freigabe = B22 0 → >0, Stopp = B33 1/4 → 0,
  - Toleranz −1,0 … +1,5 min.

## Befund (b): Abendanforderungen S = 30,0 °C ohne Freigabe
Die Hypothese „RL blieb über 28,5 °C“ stimmt für die Zeit nach der Spülung. Sie erklärt aber nicht, warum der Verdichter nicht sofort freigegeben wurde: In den ersten 7 bis 90 s lag RL unter 28,5 °C, und der Timer war abgelaufen (letzter Stopp 58 bis 115 min vorher). Den Unterschied macht der **Vorlauf**.

Ablauf in allen vier Fällen (**sicher**, X26):
- Beim Eintreffen von M0 steht im WEZ noch warmes Wasser, VL liegt über S.
- Etwa 5 s später läuft die Pumpe an. VL fällt kurz (kaltes Rücklaufwasser), dann steigen RL und VL auf 33 bis 40 °C (Pufferwasser).
- Es gibt keine Freigabe bis zum Ende der Anforderung.

| Anforderung (M0 0 → 60) | RL0 | VL0 | VL0 − S | RL ≤ 28,5 nur für | danach RL bis | Ende der Anforderung | Dauer | Stopp vorher |
|---|---|---|---|---|---|---|---|---|
| 16.10. 20:02:33 | 26,0 | 32,0 | +2,0 | 24 s (bis 20:02:57) | 36,0 | 23:51:37 | 229 min | 93,6 min |
| 17.10. 20:11:25 | 27,5 | 32,5 | +2,5 | 18 s (bis 20:11:43) | 38,0 | 21:45:48 | 94 min | 109,8 min |
| 18.10. 20:32:44 | 25,5 | 31,0 | +1,0 | 90 s (bis 20:34:14) | 33,5 | 23:28:35 | 176 min | 114,5 min |
| 23.10. 20:51:01 | 28,0 | 36,0 | +6,0 | 7 s (bis 20:51:08) | 40,0 | 22:51:17 | 120 min | 57,7 min |

Zum Vergleich alle **Sofortfreigaben** (0 bis 1 s nach M0, Timer abgelaufen). In jedem Fall lag VL0 unter S:

| Anforderung | S | RL0 | VL0 | VL0 − S | Freigabe |
|---|---|---|---|---|---|
| 16.10. 05:49:08 | 34,5 | 28,0 | 29,0 | −5,5 | 05:49:09 |
| 16.10. 14:48:50 | 38,0 | 26,5 | 34,0 | −4,0 | 14:48:51 |
| 18.10. 07:01:39 | 30,0 | 28,0 | 29,0 | −1,0 | 07:01:40 (16 s später WW, M1 = 112) |
| 19.10. 09:13:46 | 33,5 | 23,5 | 29,0 | −4,5 | 09:13:46 |
| 21.10. 15:24:39 | 32,0 | 28,5 | 29,0 | −3,0 | 15:24:40 |
| 22.10. 04:21:33 | 34,5 | 29,0 | 29,5 | −5,0 | 04:21:34 |
| 23.10. 03:00:57 | 35,5 | 27,5 | 28,0 | −7,5 | 03:00:57 |
| 24.10. 05:26:28 | **30,0** | 25,5 | 26,0 | −4,0 | 05:26:29 |
| 24.10. 10:34:43 | 33,5 | 28,0 | 28,5 | −5,0 | 10:34:44 |
| 24.10. 13:30:58 | 33,0 | 30,0 | 31,5 | −1,5 | 13:30:59 |

- **24.10. 05:26:28 ist das saubere Gegenstück** zu den Abendfällen: Bei gleichem S = 30,0 lag VL bei 26,0 °C (also unter S), und die Freigabe kam nach 1 s.
- Alle Anforderungen mit VL0 ≥ S und abgelaufenem Timer bekamen **keine** Sofortfreigabe: 16.10. 13:18, 17.10. 08:25 und 17:41, 18.10. 14:19, 23.10. 17:16 sowie die 4 Abendfälle.

**Regeländerung (Modell A+VL):** Der HKA59-Timer läuft, solange **RL ≤ S − 1,5 K und VL ≤ S** gelten. Zurückgesetzt wird er wie bisher: durch WW-Ladung, oder wenn die Bedingung bei anliegender Anforderung und stehendem Verdichter verletzt ist. Wie genau die VL-Schwelle liegt, lässt sich aus den Daten nicht eingrenzen: Jeder Wert zwischen VL ≤ S + 0,5 und VL ≤ S − 1,0 passt (**sicher** als Datenfit), ab S − 1,5 brechen 9 Wiederanläufe. Im Abendfall ist die Bedingung also schon beim Eintreffen von M0 verletzt, und der Timer wird sofort zurückgesetzt. Danach lagen RL ≤ 28,5 und VL < 30 nur kurz gemeinsam vor: 13 s am 16.10., 5 s am 17.10., 80 s am 18.10., 0 s am 23.10. Für eine Freigabe hätten es 15 min sein müssen.

Simulation `or_f17r_20261024_1500_c.py` (sekundengenau, Segmente wie in der Vorarbeit):

| Variante | 16.–23.10. | 16.–24.10. 14:55 | Ausreißer |
|---|---|---|---|
| A (RL ≤ S − 1,5), Vorarbeit | 49/54 | 57/62 | #12 und die 4 Abendfälle |
| **A+VL (zusätzlich VL ≤ S)** | **53/54** | **61/62** | #12 |
| A+VL, VL ≤ S − 1,0 / + 0,5 / − 0,5 | 53/54 | – | #12 |
| A+VL, VL ≤ S − 1,5 | 44/54 | – | 9 Wiederanläufe mit Δ −1,1 … −3,6 min, dazu 18.10. 07:01 |
| A+VL, VL ≤ S + 1,0 / + 2,0 (lockerer) | 52/54 / 51/54 | – | #12; bei + 1,0 zusätzlich 18.10. 20:32 (VL0 − S = +1,0), bei + 2,0 auch 16.10. 20:02 (+2,0) |
| B+VL (Pause setzt zurück) | 52/54 | – | #12 und #25 (Δ −10,0) |

Hinweis zur Einordnung: Die Vorarbeit hatte als Fühler RL, VL, Mittelwert und Max jeweils **einzeln** gegen eine gemeinsame Schwelle getestet. Neu ist hier die **Kombination** zweier Bedingungen mit verschiedenen Schwellen. Ein Schwellenparameter kommt dazu. Der Fit-Gewinn (4 Segmente) beruht auf einer physikalisch plausiblen Regel: Steht der Vorlauf schon über dem Soll, besteht kein Wärmebedarf. Sicherheit: **wahrscheinlich**.

## Befund (a): Fall #12 (18.10. 18:02:13, nach WW)
| Zeit (X26) | Ereignis | RL | VL | S |
|---|---|---|---|---|
| 18:02:12–13 | WW-Ende (M1 122 → 0), M0 = 76 | 59,0 | 62,0 | 38,0 |
| 18:06:36 | RL erreicht 36,5 = S − 1,5 (Timerstart, aus der Freigabe zurückgerechnet) | 36,5 | ~34 | 38,0 |
| 18:08:20 | **M0 76 → 60** (30,0 °C für 64 s) | 29,0 | 29,0 | 30,0 |
| 18:09:24 | M0 60 → 65 | 29,0 | 29,0 | 32,5 |
| 18:21:35 | **Freigabe** B22 0 → 65 | 29,5 | 29,5 | 32,5 |

- Gemessene Freigabe = 18:06:35 + 15:00. Der Kälteregler hat den 64-s-Einbruch also **nicht** als Reset gewertet. Das Modell setzt dort zurück (RL 29,0 > 28,5) und sagt 18:24:24 voraus (Δ −2,82 min). VL (29,0 ≤ 30,0) war in der Lücke erfüllt; verletzt war nur RL, und das um eine B29-Stufe (0,5 K).
- Geprüft (`or_f17r_20261024_1500_d.py`), keine Variante ohne Nebenwirkung:

| Variante | Wirkung auf #12 | Nebenwirkung |
|---|---|---|
| Reset-Entprellung 10–30 s | bleibt −2,8 | bricht #4 (Δ +11,0) und 3 Abendfälle (ohne Sofortreset bei Anforderungsbeginn) |
| Entprellung 10–30 s + Sofortreset bei Anforderungsbeginn | bleibt −2,8 | 53/54 |
| Entprellung 70–120 s + Sofortreset | **passt** | bricht 18.10. 17:05 (Freigabe vorhergesagt, keine) |
| Entprellung 300 s + Sofortreset | passt | bricht 18.10. 17:05 und 23.10. 09:41 (Δ +7,6) |
| Reset-Hysterese 0,5 K auf RL (mit/ohne VL) | passt | bricht 18.10. 17:05 und 23.10. 09:41 |
| Reset-Hysterese 1,0 K | passt | bricht zusätzlich 17.10. 09:16 (Δ +17,6) |
- **Passt #12 ins Modell?** Nein, Δ −2,8 min, knapp außerhalb des Bandes. Der Unterschied zu #4 (dort setzte ein 8-s-Zwischenwert zurück): Bei #4 kam der 30,0-°C-Wert **mit Beginn der Anforderung**, RL und VL lagen beide über der Schwelle (30,5/31,0). Bei #12 kam er **mitten in der Anforderung**, verletzt war nur RL, und das um eine einzige B29-Stufe. **Vermutung:** Der Kälteregler misst RL feiner als B29 (Auflösung 0,5 K). Wahrscheinlich lag sein Wert bei ≤ 28,5 °C, B29 zeigt ihn als 29,0 an. Auch der neue Start am 24.10. 11:43:28 kam 21 s **vor** der B29-Vorhersage. Die Richtung ist dieselbe: Der Kälteregler sieht RL etwas kälter, als B29 anzeigt.

## Befund (c): Woher kommen die 30,0-°C-Sollwerte?
**1. Lange Werte am Abend: Ofen-Nachlauf (sicher).** Der Volllogger zeigt in allen vier Fällen 1490 = 240 (24,0 °C, Untergrenze der Loxone-Formel „1490 inkl. Ofen-Nachlauf (min. 24 °C)“) und 1520 = 300 (30,0 °C). Gleichzeitig steigt 1510 von 22,0 auf 24,4 °C (Ofenabend):

| Volllogger-Zeile (Rohwerte ×10: 1490 [Nummer]) | Bezug |
|---|---|
| `2026-10-16 20:00:01 0 0 0 225` → `2026-10-16 20:05:02 240 300 23 227` … `23:50:01 240 300 23 243` → `23:55:02 0 0 0 242` | Anforderung 20:02:33 – 23:51:37 |
| `2026-10-17 20:15:02 240 300 23 223` … `21:45:02 240 300 23 238` → `21:50:02 0 0 0 239` | 20:11:25 – 21:45:48 |
| `2026-10-18 20:35:01 240 300 23 222` … `23:25:01 240 300 23 240` → `23:30:01 0 0 0 240` | 20:32:44 – 23:28:35 |
| `2026-10-23 20:55:01 240 300 23 224`, Bridge: `2026-10-23 20:50:44.882 1490 <- 240` | 20:51:01 |

Bewertung: Im Ofen-Nachlauf fordert Loxone nur einen Mindest-Vorlauf an, damit die HK1-Pumpe läuft. Der Puffer ist wärmer (RL steigt auf 33 bis 40 °C), also startet die WP richtigerweise nicht. Das ist **kein Fehler**, sondern so gewollt (**wahrscheinlich**).

**2. Kurze Spitzen bei Anforderungsbeginn: Zwischenwert von Loxone (Beleg ab 23.10. 19:47).** Beim Übergang 0 → Soll schreibt Loxone 1490 zuerst auf rund 15 °C und 2 bis 10 s später auf den eigentlichen Wert (Bridge-Log, Millisekunden):

| 1490 (Bridge-Log) | M0 im X26 | Verzögerung | Wirkung |
|---|---|---|---|
| 24.10. 05:26:03.545 ← 151, 05:26:13.374 ← 313 | 05:26:28 M0 = 60 (30,0), 05:26:44 M0 = 68 (34,0) | 25 s / 31 s | Zwischenwert **kam an** (16 s 30,0 °C) |
| 24.10. 10:34:10.851 ← 151, 10:34:12.662 ← 308 | 10:34:43 M0 = 67 (33,5) | 31 s | kam nicht an (lag nur 1,8 s an) |
| 24.10. 13:30:14.222 ← 153, 13:30:23.619 ← 302 | 13:30:58 M0 = 66 (33,0) | 35 s | kam nicht an (9,4 s) |
| 24.10. 15:00:15.936 ← 154, 15:00:22.482 ← 300 | 15:00:58 M0 = 112 (WW) | – | WW hat Vorrang |

- Die TopTronic übernimmt 1490 nach etwa 25 bis 35 s in M0. Ein Zwischenwert erscheint nur dann in M0, wenn er beim Abtasten noch anliegt (**wahrscheinlich**, 1 von 3 kam an).
- **Abbildung 1490 → M0 (wahrscheinlich, 9/9 Stichproben):** M0 = max(30,0; 1490 + 3,0 K, abgerundet auf 0,5 K). Stichproben: 15,1 → 30,0; 24,0 → 30,0; 28,2 → 31,0; 29,6 → 32,5; 30,2 → 33,0; 30,8 → 33,5; 31,3 → 34,0. Volllogger: 35,3 → 38,0 und 35,7 → 38,5. Die Untergrenze von 30,0 °C für die WP-Anforderung liegt also in der TopTronic. Den Parameter dazu habe ich nicht nachgeschlagen.
- **Ältere Spitzen** (16.10. 13:18:43 bei #4, 18.10. 18:08:20 bei #12, 22.10. 07:01:33): Das Bridge-Journal reicht nicht so weit zurück, ein direkter Beleg fehlt. Dass auch dort ein 15-°C-Zwischenwert oder ein Absinken auf ≤ 27 °C dahintersteckt, ist eine **Vermutung**. Belegt ist nur, dass das Muster seit 23.10. 19:47 auftritt.
- **Woher der Zwischenwert in Loxone kommt** (vermutlich Klimacontroller UG / Heatmixer beim Einschalten, Ausgang OutHeat1 im ersten Zyklus): **offen**. Die Projektdatei habe ich dafür nicht ausgewertet.

## Befund (d): Heizstarts seit 24.10. 11:00 (und der ganze 24.10.)
Vorhersage = max(Anforderung, Stopp + 15 min, Bedingungsbeginn + 15 min), Modell A+VL. Quelle: `or_f17r_20261024_1500_c24.out`.

| Anforderung / Segment | S | Stopp vorher | Bedingung ab | Vorhersage | Freigabe (B22) | Δ | |
|---|---|---|---|---|---|---|---|
| 24.10. 05:26:28 (M0 erst 30,0, nach 16 s 34,0) | 30,0 | 573 min | – (abgelaufen) | 05:26:28 | 05:26:29 | +0,02 | OK |
| 06:07:00 (nach WW, Stopp 06:07:00) | 34,0 | WW | – | 06:26:55 | 06:26:40 | −0,25 | OK |
| 10:34:43 | 33,5 | 213 min | – | 10:34:43 | 10:34:44 | +0,02 | OK |
| **11:23:47 (nach WW)** | 33,5 | WW 11:23:47 | RL ≤ 32,0 ab 11:28:49 | 11:43:49 | **11:43:28** | −0,35 | OK |
| **13:30:58** | 33,0 | 64 min (12:26:57) | – | 13:30:58 | **13:30:59** | +0,02 | OK |
| 07:01:16, 12:26:57, 14:04:55 (Kälteregler-Stopp, Anforderung bleibt) | – | – | – | keine | keine | – | OK |

- **Seit 11:00: 2 von 2 Heizfreigaben passen**. Bis 15:04 kam kein weiterer Heizstart: 14:24:58 und 15:00:58 waren WW (M1 = 112).
- **Ganzer 24.10.: 5 von 5 Freigaben** und 8 von 8 Segmenten passen, in A+VL wie in A.
- Bei 11:43:28 griff weder Stopp + 15 (11:38:47) noch die Anforderung, sondern die Bedingung + 15: RL fiel nach der WW-Ladung erst um 11:28:49 auf 32,0 °C (B29 = 85). Die Freigabe kam 21 s früher als vorhergesagt.

## Regelstand
**Gültige Regel (Stand 24.10. 15:20, wahrscheinlich):**
- **Timer:** Der HKA59-Timer (15 min) läuft, solange **RL ≤ S − 1,5 K und VL ≤ S** gelten. Für die VL-Schwelle passt jeder Wert von S − 1,0 bis S + 0,5. S ist das aktuelle M0, in der Pause das letzte Heiz-M0.
- **Reset:** durch WW-Ladung, oder wenn die Bedingung bei anliegender Heizanforderung und stehendem Verdichter verletzt ist. Kurze Sollwertspitzen zählen dabei mit. Während eines Laufs ist der Timer eingefroren, in einer Pause ohne Anforderung bleibt er stehen.
- **Freigabe** = max(Anforderung, Stopp + 15 min (WP011), Timerstart + 15 min).

| Zählung | Modell A (Vorarbeit) | Modell A+VL (neu) |
|---|---|---|
| Heizstarts 16.–23.10. (F17-Zählung) | 25/26 | 25/26 (#12) |
| Heizstarts 24.10. (bis 15:04) | 5/5 | 5/5 |
| **Heizstarts gesamt** | 30/31 | **30/31** |
| Segmente 16.–23.10. (mit Wiederanläufen und Anforderungen ohne Freigabe) | 49/54 | **53/54** |
| Segmente 16.–24.10. 14:55 | 57/62 | **61/62** |

Neu ist vor allem: Die vier Fälle **ohne** Start sind jetzt erklärt. Damit sagt das Modell auch richtig voraus, wann die WP **nicht** startet.

## Was bringt uns das
- **Startvorhersage in Loxone:** Eine Anforderung startet die WP sofort nur, wenn der Timer abgelaufen ist **und** der WEZ-Vorlauf beim Eintreffen nicht über dem Soll liegt. Im Ofen-Nachlauf (1490 = 24 → WP-Soll 30 °C) startet die WP bei warmem Puffer nie. Das ist so gewollt und kostet nichts.
- **Kurzlauf-Hebel (Vermutung, nicht getestet, nichts geändert):** Loxone schreibt beim Einschalten von 1490 zuerst etwa 15 °C. Kommt das in M0 an (1 von 3 Fällen am 24.10.), sieht der Kälteregler kurz S = 30,0. Liegt RL dabei über 28,5 °C, setzt das den HKA59-Timer auf 15 min zurück, und der Start verzögert sich um bis zu 15 min (so bei #4, Wirkung belegt). Ein glatter Übergang 0 → Soll in der Loxone-Logik würde das vermeiden. Änderung nur mit des Betreibers Freigabe, mit Backup und nach dem Skill `loxone-xml-umbau`.
- **Neue Datenquelle:** Das Journal von `hoval-bridge` protokolliert jeden Schreibvorgang auf 1490 mit Millisekunden. Es reicht aber nur etwa 19 h zurück. Wer es länger braucht, muss es regelmäßig sichern. Das wäre eine Änderung am Pi, hier nicht gemacht.

## Offene Reste
1. **#12 (Δ −2,8 min):** Am wahrscheinlichsten ist ein Auflösungs-Grenzfall bei RL (B29 in 0,5-K-Stufen). Klären lässt sich das nur mit einem feiner aufgelösten RL-Wert aus dem Kälteregler (Werteblöcke Obj 0x50–0x5F im X26, noch nicht dekodiert) oder durch Lesen des Codes.
2. **Wo genau die VL-Schwelle liegt** (S − 1,0 … S + 0,5), und ob der Kälteregler B17 oder einen anderen Vorlauffühler nimmt. Eingrenzen lässt sich das nur mit weiteren Anforderungen, bei denen VL0 nahe an S liegt.
3. **Ursache des 15-°C-Zwischenwerts** in Loxone. Prüfbar mit der Projektdatei `[lokaler Pfad]` (Klimacontroller HC1 / Heatmixer2 / AnalogMultiplexer „Sollwert Heizen 1490“), nur lesen.
4. Für die Fälle vor dem 23.10. 19:47 fehlt ein Beleg, dass die Spitzen von Loxone kamen (Journal zu kurz).
5. `FRAGENKATALOG.md` ist laut Auftrag nicht geändert.

## Rohbelege zum Gegenprüfen
- **Abendfall ohne Freigabe**, `[lokaler Pfad]` (TAG 16):
  - Zeile 2505: `20:02:33 M0 0 60`. Dabei gilt B17 = 85 (VL 32,0 > S 30,0) und B29 = 73 (RL 26,0).
  - Zeile 2506: `20:02:38 B17 85 84`
  - Zeile 2522: `20:02:57 B29 78 79` (RL 28,5 → 29,0, ab hier dauerhaft über der Schwelle)
  - Bis zum Tagesende kommt kein `B22 0 …`.
  - Volllogger dazu: `2026-10-16 20:05:02 240 300 23 227` (1490 [Nummer]).
- **Gegenstück mit gleichem S, sofort freigegeben**, `[lokaler Pfad]`:
  - Zeile 314: `05:26:28 M0 0 60` (RL 25,5, VL 26,0 < 30,0)
  - Zeile 315: `05:26:29 B22 0 60`
  - Zeile 325: `05:26:44 M0 60 68`
- **Loxone-Zwischenwert**, `[lokaler Pfad]`:
  - Zeile 137: `2026-10-24 05:26:03.545 151`
  - Zeile 138: `2026-10-24 05:26:13.374 313`
  - Zeile 267: `2026-10-24 13:30:14.222 153`
  - Zeile 268: `2026-10-24 13:30:23.619 302`
  - Original am Pi: `journalctl -u hoval-bridge -o cat --since '2026-10-24 05:25' --until '2026-10-24 05:27' | grep 'SET reg 1490'`
- **Neuer Start**, ev24:
  - `13:30:58 M0 0 66`, `13:30:59 B22 0 66`
  - `11:23:47 B33 4 0`, `11:28:49 B29 86 85`, `11:43:28 B22 0 67`

## Verwendete Skripte (alle nur lesend)
Alle Skripte liegen unter `[lokaler Pfad]`:
- `or_f17r_20261024_1500_a.py`: Fensterausgabe mit X26-Ereignissen samt RL/VL-Kontext (ev3 + ev24).
- `or_f17r_20261024_1500_b.py`: Tabelle je Anforderung (RL0, VL0, Freigabe, Bedingungssekunden). Ausgaben `_b.out` (16.–23.10.) und `_b24.out` (24.10.).
- `or_f17r_20261024_1500_mk.py` erzeugt `or_f17r_20261024_1500_c.py`: Timersimulation abgeleitet von `or_f17x_20261024_1100_h.py`, plus Fühler RLVL (RL ≤ S − dK und VL ≤ S − dK2) und mehrere ev-Dateien. Ausgabe `_c24.out`.
- `or_f17r_20261024_1500_mk2.py` erzeugt `or_f17r_20261024_1500_d.py`: dazu Reset-Entprellung DB, Sofortreset bei Anforderungsbeginn (EDGE) und Reset-Hysterese (Umgebungsvariablen FH/FH2).
- `or_f17r_20261024_1500_pi.py`: Kopie von `or_f17x_20261024_1100_pi3.py`. Am Pi `/tmp/or_f17r_pi.py`, Ausgaben `/tmp/or_f17r_ev24.txt` (bis 14:56) und `/tmp/or_f17r_ev24b.txt` (bis 15:04).
- `or_f17r_20261024_1500_vl.py`: Volllogger-Fenster am Pi (`/tmp/or_f17r_vl.py`). Ausgabe `_vl.out`.
- `or_f17r_20261024_1500_set1490.txt`: Schreibvorgänge auf 1490 aus `journalctl -u hoval-bridge` ab 23.10. 19:40.

## Stand gegen „fertig, wenn“ (F17)
| Kriterium | Stand |
|---|---|
| Regel für den Sofortstart benannt | **erfüllt.** Timer abgelaufen, RL ≤ S − 1,5 und VL ≤ S beim Eintreffen der Anforderung, Stopp liegt mindestens 15 min zurück |
| an mindestens 5 Fällen bestätigt (sofort und verzögert) | **erfüllt für den Sofortstart:** 10/10 sofort, 4/4 „keine Freigabe“. Bei den verzögerten Starts gibt es eine Ausnahme (#12, −2,8 min); streng genommen also nicht „ohne Ausnahme“ |
| Reset-Fall mindestens 1× belegt | erfüllt (WW-Reset mehrfach, z. B. 24.10. 11:23:47 → 11:43:28; Reset durch Sollspitze bei #4) |
| Abtau-Fall mindestens 1× belegt | **nicht geprüft.** Diese Analyse hat keine Abtauung ausgewertet |

Der Orchestrator sollte F17 daher auf **„fast erledigt“** setzen. Es fehlen noch der Abtau-Fall und die Entscheidung, ob #12 als Auflösungs-Grenzfall hingenommen wird.