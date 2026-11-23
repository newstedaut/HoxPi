# F17-Ausnahmen #4 und #25: Warum die Freigabe 11,4 min später bzw. 9,2 min früher kam (24.10.2026)
Analyse-Agent 24.10.2026 ~11:00–12:30 · strikt nur lesend (kein Schreiben an Anlage, CAN, X26, X4, Kälteregler; keine Bus-Probes; nichts gelöscht; keine Dienste neu gestartet) · Katalogfrage F17.
Vorlauf: `[lokaler Pfad]` (inkl. Nachtrag 04:00).

**Frage:** Die Regel „HKA59 (33-055) läuft gegen den letzten Heiz-Soll, WW setzt zurück; Freigabe = max(Anf., Stopp + 15, Bed. + 15)“ erklärt 24 von 26 Heizstarts (16.–23.10.). Warum passen #4 (16.10. 13:18) und #25 (23.10. 18:05) nicht?

## Ergebnis in 4 Zeilen
1. **Beide Ausnahmen sind jetzt sekundengenau erklärt (Δ = 0 s), mit einer Regeländerung:** In der Pause ohne Heizanforderung setzt „RL zu warm“ den HKA59-Timer **nicht** zurück. Zurückgesetzt wird nur durch WW-Ladung und durch „Heizanforderung liegt an, Verdichter steht, RL > Soll − 1,5 K“. Während eines Laufs ist der Timer eingefroren. Sicherheit: **wahrscheinlich** (Messung sicher, Kälteregler-Code nicht gelesen).
2. **#4:** Die TopTronic schickte bei der Anforderung 8 s lang Soll **30,0 °C** (X26 M0 = 60), erst dann 38,5. In diesen 8 s war RL 30,5 > 28,5 → Reset. Freigabe 13:33:51 = 13:18:51 + 15:00,0 (**sicher** als Zeitbefund).
3. **#25:** Der Timer lief seit 17:22:12 (vor dem Lauf #24) und wurde in der Pause 17:56–18:06 nicht zurückgesetzt, obwohl RL (35,5 °C) über dem alten Soll 33,0 − 1,5 lag. Freigabe 18:11:15 = Stopp 17:56:15 + 15:00,0 (= WP011).
4. **„Regel jetzt 26/26?“ – nein, 25/26.** #4 und #25 passen jetzt (Δ 0,00), aber mit den genaueren X26-Zeiten fällt #12 (18.10. 18:02, nach WW) heraus: Freigabe 2,8 min **früher** als vorhergesagt. Außerdem gibt es 4 Abend-Anforderungen mit Soll 30,0 °C (16./17./18./23.10.), bei denen die Regel eine Sofort-Freigabe vorhersagt, die nicht kam. Die alte Erklärung dafür („RL steigt mit dem Pumpenlauf in 0,6–1,4 min über 28,5“) hält der 1-s-Auflösung nicht stand.

## Was bringt uns das
- Für die Startvorhersage in Loxone gilt weiter: Freigabe ≈ max(Anforderung, Stopp + 15 min, Beginn „RL ≤ S − 1,5“ + 15 min). **Neu:** Eine Pause ohne Anforderung „verliert“ den abgelaufenen Timer nicht. Kommt die nächste Anforderung mit kaltem RL (≤ neuer Soll − 1,5), entscheidet nur WP011 (Stopp + 15).
- **Praktischer Hebel (Vermutung, nicht getestet, keine Änderung vorgenommen):** Eine kurze Soll-Spitze nach unten beim Anfordern (TopTronic sendet kurz 30,0 °C) kann den Timer auf 15 min zurücksetzen. Genau das hat #4 verzögert. Ob Loxone (1490) oder die TopTronic diesen Zwischenwert erzeugt, ist offen (siehe Reste).
- Der Freigabe-Zeitpunkt ist im X26-Mitschnitt **direkt** sichtbar (Slave-Statusblock Byte 22/24 = wirksamer Soll im Kälteregler springt 0 → Soll). Damit braucht man für weitere Prüfungen keine 60-s-alten Modbus-Werte mehr.

## Datenquellen (alle nur gelesen)
- **X26-Sniffer roh** am Pi (<LAN-IP>): `/home/<user>/rs485_sniff/log/rs485_2026-10-16.log.gz` … `rs485_2026-10-23.log.gz`. Dekodiert mit dem vorhandenen Parser `/home/<user>/rs485_sniff/rs485_9600parse.py` (`frames_from_log`), nur CRC-gültige Rahmen.
  - Master → Kälteregler, Obj 0x20 (23 B, Sollwertvektor): **M0** = Heiz-VL-Soll (b·0,5 °C, 0 = keine Heizanforderung), **M1** = WW-Ladesoll, **M11** Bit 6 = SG-Ready. Belegung laut `[lokaler Pfad]` und `SPEZ_X26_RS485.md`.
  - Kälteregler → Master, Obj 0x20 Selektor 0x64 (100 B Statusblock, ~1 s): **B22/B24** = Hauptregler-VL-Soll / wirksamer Soll (0 = nicht freigegeben), **B29** = WEZ-Rücklauf ((b−21)/2 °C, = FARL), **B17** = WEZ-Vorlauf, **B31** = Leistung %, **B33** = Status (= Modbus 1539: 0/51/1/4), **B88** = Mindestlaufzeit-Zähler (30-s-Schritte, 10 → 0 = 5 min).
- **X26 ZUSTAND-Auszüge** (Modbus-Werte, bis 60 s alt): `[lokaler Pfad]` … `_23.txt`.
- **Volllogger** (5 min): `[lokaler Pfad]`, `or_f5_20261023_vl23.csv` (1490, 1520, 1501, 1529, 1539).
- `~/hoxpi_fulllog/ww_hires.csv` (10 s) geprüft: enthält WP_VL/WP_RL/Status_HK1/Modulation, aber **weder 1520 noch 1490** – für H2 nicht nötig, weil X26 B29 und M0 sekundengenau sind.

## Methode
- `[lokaler Pfad]` (am Pi, nohup, gz direkt gelesen, keine Temp-Kopie): Änderungsliste M0, M1, M11, B17, B22, B29, B31, B33 für 16.–23.10. → lokal `or_f17x_20261024_1100_ev3.txt` (23 108 Zeilen; `_ev.txt`/`_ev2.txt` = Vorstufen).
- `_pi2.py` (Fensteranalyse aller Bytes des Statusblocks um ein Ereignis), `_pi4.py` + `_pi4.out` (kompletter Statusblock zu Stichzeitpunkten), `_a.py`/`_b.py` (ZUSTAND- und Volllogger-Fenster), `_c.py/.out` (Ereignisse je Anforderung).
- `_d.py`, `_e.py`, `_f.py`, `_g.py`, `_h.py` (+ `.out`): sekundengenaue Simulation des HKA59-Timers gegen die gemessene Freigabe (B22 0 → x). Varianten: A (Pause setzt nicht zurück), B (Pause setzt zurück = alte F17-Regel), C/D (ohne WW-Reset), E (SG-Flanke setzt zurück), Hysterese H, Fühler RL/VL/Mittel/Max, Schwelle 1,0/1,25/1,5/2,0 K.
- Definitionen: **Anforderung** = M0 0 → > 0 bei M1 = 0. **Freigabe** = B22 0 → > 0. **Stopp** = B33 1/4 → 0. **Toleranz** −1,0 … +1,5 min wie in F17.
- Die Hilfsskripte liegen am Pi zusätzlich unter `/tmp/or_f17x_*` (klein, Arbeitsdateien).

## Tabelle: beide Fälle mit X26-Zeitstempeln (Quelle: `rs485_2026-10-16.log.gz` / `rs485_2026-10-23.log.gz`)
| Schritt | #4 (16.10.) | #25 (23.10.) |
|---|---|---|
| Vorheriger Lauf Freigabe (B22 0→x) | 13:02:30 (Soll 38,5, nach WW, Bed.+15) | 17:36:45 (Soll 33,0, #24) |
| Verdichter an (B33 51→1) | 13:02:52 | 17:37:06 |
| SG-Ready (M11) | 64 → 0 um 13:06:11 (im Lauf) | 0 (ganzer Lauf) |
| Anforderungsentzug (M0 → 0) | 13:07:39 | 17:56:14 |
| Verdichter aus (B33 1→0) | **13:07:52** = Start + 5:00 (Mindestlaufzeit hielt 13 s, B88 lief auf 0) | **17:56:15** (1 s nach Entzug) |
| Laufzeit | 5,0 min | 19,1 min |
| RL (B29) nach Stopp | 30,0–30,5 °C | 36,0 → 33,0 °C |
| SG-Ready vor Anf. | 0 → 64 um 13:18:11 | 0 → 64 um 18:05:50 |
| Neue Anforderung (M0) | **13:18:43 M0 = 60 (30,0 °C)**, 13:18:51 M0 = 77 (38,5 °C) | 18:06:14 M0 = 79 (39,5 °C) |
| RL bei Anforderung | 30,5 °C (B29 = 82) | 32,5–33,0 °C |
| Bedingung RL ≤ S − 1,5 bei Anf. | 13:18:43–51: 30,5 > 28,5 **falsch** (8 s); ab 13:18:51: 30,5 ≤ 37,0 wahr | 33,0 ≤ 38,0 wahr |
| Freigabe (B22 0→x) | **13:33:51** = 13:18:51 + 15:00 | **18:11:15** = 17:56:15 + 15:00 |
| Verdichter an | 13:34:12 | 18:11:37 |
| Modbus-Zeiten aus F17 (zum Vergleich) | Anf. 13:18:28, Stopp 13:07:56, Frg 13:34:21 | Anf. 18:05:54, Stopp 17:56:22, Frg 18:11:44 |
| Modell A (diese Analyse) | Vorh. 13:33:51, **Δ 0 s** | Vorh. 18:11:15, **Δ 0 s** |
| Alte F17-Regel (B) | Δ 0 s (der 8-s-Reset war mit 5-min-Volllogger nicht sichtbar, daher damals +11,4) | Vorh. 18:21:14, **Δ −10,0 min** |

Volllogger zum Gegenlesen: 16.10. 13:05:01 `1490=358 1520=385 1501=23 1539=1`, 13:10/13:15 alles 0, 13:20:01 `1490=357 1520=385 1501=23`. 23.10. 17:55:01 `1490=301 1520=330`, 18:00/18:05 alles 0, 18:10:01 `1490=365 1520=395`. In beiden Fällen ging die Anforderung über Loxone (1490 = 0) weg.

## Prüfung je Hypothese
| Hypothese | Ergebnis | Belege | Sicherheit |
|---|---|---|---|
| **H1** Die Art des Laufendes entscheidet (Entzug → nur WP011 ab Stopp; sonst HKA59 ab Anforderung) | **widerlegt.** Alle Heizläufe vor Anforderungen mit Stopp < 30 min endeten durch Entzug (M0 → 0, Stopp 0–1 s danach): #8, #20, #25, #26. Nur #4 hielt 13 s über die Mindestlaufzeit. #8 (Stopp 09:05:36, Anf. 09:16:07) und #20 (Stopp 07:49:57, Anf. 07:52:44) endeten durch Entzug und warteten trotzdem auf die RL-Bedingung (Frg 09:58:36 bzw. 08:18:09, nicht Stopp + 15). Eine Soll-erreicht-Abschaltung durch den Kälteregler mit liegender Anforderung kommt vor (Wiederanläufe im Block), ändert die Regel aber nicht | `or_f17x_20261024_1100_c.out`, `_ev3.txt` | **sicher** (Messung) |
| **H2** Entscheidend ist, wann RL ≤ Soll − 1,5 K galt | **bestätigt mit Zusatz**: zählt mit dem aktuellen M0, in der Pause mit dem letzten Heiz-M0. **Reset nur mit anliegender Anforderung** (oder WW), in der Pause nicht (Variante A). #4: Reset durch den 8-s-Zwischenwert 30,0 °C. #25: kein Reset in der Pause → Stopp + 15. Variante A trifft 49/54 Segmente, B (alte Regel) 48/54. Der einzige Unterschied A ↔ B ist #25 | `_g.out`, `_h.out` | Ablauf **sicher**; Regel **wahrscheinlich** |
| H2-Varianten | Ohne WW-Reset (C, D): 33/38 bzw. 36/38, schlechter (z. B. #11 18.10. 14:19 Δ +15,4). SG-Flanke als Reset (E): bricht #26 (Δ −14,8) und 16.10. 06:43 (Δ −8,3) → **verworfen**. Schwelle 1,0 K (RL): 40/54; 2,0 K: 15/38. Hysterese 0,5 K beim Reset: rettet #12, bricht aber 23.10. 09:41 (Δ +7,6) | `_f.out`, `_e.out`, `_d_dk.out`, `_g.out` | sicher (als Datenfit) |
| **H3** X26 zeigt eine Freigabe-/Timer-Variable | **teilweise.** Die Freigabe ist sekundengenau sichtbar: B22/B24 (wirksamer Soll) 0 → Soll, gleichzeitig B31 0 → 100, B33 0 → 51, B89 0 → 1 (alle 38 Freigaben). **Ein HKA59-Restzeit- oder Zählerwert ist im 100-B-Statusblock nicht enthalten.** B88 ist der Mindestlaufzeit-Zähler (10 → 0 in 30-s-Schritten ab Verdichterstart). Die 1-Hz-Werteblöcke Obj 0x50–0x5F wurden nicht ausgewertet. Byte-Vergleich Freigabe vs. Nicht-Freigabe (16.10. 20:02, 18.10. 07:01, 23.10. 18:06/19:07/20:51) zeigt kein unterscheidendes Status-Flag | `_pi2.py`-Ausgaben, `_pi4.out` | Freigabe-Variable **sicher**; „kein Timer im Statusblock“ **sicher** für Obj 0x20 / 0x64 |

## Gegenprobe an weiteren Fällen (Stopp < 30 min vor der Anforderung, Modell A, RL, 1,5 K)
| Fall | Stopp (B33) | Anf. (M0) | S | Ende vorher | Freigabe gemessen | Vorhersage A | Δ |
|---|---|---|---|---|---|---|---|
| #8, 17.10. | 09:05:36 | 09:16:07 | 33,5 (danach 33,0 … 34,0) | Entzug, 23,8 min | 09:58:36 | 09:58:23 (Bed. ab 09:43:23) | +0,22 min |
| #19, 22.10. | 06:37:01 (WW) | 07:01:33 (erst 30,0, nach 7 s 34,5) | 34,5 | WW-Ende | 07:21:04 | 07:21:01 | +0,05 min |
| #20, 22.10. | 07:49:57 | 07:52:44 | 34,5 | Entzug, 28,5 min | 08:18:09 | 08:18:03 (Bed. ab 08:03:03) | +0,10 min |
| #26, 23.10. | 18:52:14 | 19:07:02 | 39,0 | Entzug, 40,6 min | 19:07:15 | 19:07:14 (Stopp + 15) | +0,02 min |
| #4, 16.10. | 13:07:52 | 13:18:43 | 30,0 → 38,5 | Mindestlaufzeit, 5,0 min | 13:33:51 | 13:33:51 | 0,00 |
| #25, 23.10. | 17:56:15 | 18:06:14 | 39,5 | Entzug, 19,1 min | 18:11:15 | 18:11:15 | 0,00 |

Zusätzlich die Wiederanläufe innerhalb einer liegenden Anforderung (Kälteregler hatte abgeschaltet, z. B. 16.10. 08:29, 18.10. 16:29, 20.10. 08:59/10:23/14:06/16:33, 23.10. 09:41/11:05): alle 10 im Toleranzband, Δ −0,6 … +1,4 min.

**Fehlschläge von Modell A (5 von 54 Segmenten):**
- **#12, 18.10. 18:02:12** (nach WW): Freigabe 18:21:35, Vorhersage 18:24:24 (**−2,8 min**). Ursache: Die TopTronic senkte M0 um 18:08:20 für 64 s auf 30,0 °C (danach 32,5). RL lag bei 29,0 °C (B29 = 79), also 0,5 K über 28,5. Das Modell setzt dort zurück, der Kälteregler offenbar nicht. Die Freigabe passt exakt zu einem Timerstart 18:06:35 (B29 erreicht 36,5 = 38,0 − 1,5 um 18:06:36). Ein Grenzfall an der 0,5-K-Stufe von B29 (Vermutung: feinerer Fühlerwert oder kleine Hysterese im Kälteregler).
- **4 Abend-Anforderungen mit S = 30,0 °C** (16.10. 20:02:33, 17.10. 20:11:25, 18.10. 20:32:44, 23.10. 20:51:01): Das Modell sagt eine Sofort-Freigabe voraus (Timer abgelaufen, Stopp > 57 min her, RL 26,0–28,0 ≤ 28,5 für 7–22 s nach M0). Es kam keine Freigabe; danach stieg RL mit dem Pumpenlauf auf 29–39 °C und blieb über 28,5. Die alte Erklärung „Bedingung muss noch gelten, wenn die Anforderung ankommt“ reicht nicht: Sofortstarts werden 0–1 s nach M0 freigegeben (z. B. 16.10. 14:48:50 → 14:48:51, 21.10. 15:24:39 → 15:24:40). Gegenbeispiel mit gleichem S = 30,0: **18.10. 07:01:39 → Freigabe 07:01:40** bei RL 28,0 °C.
  - Geprüft und **nicht** unterscheidend: SG-Bit (M11), Außentemperatur (M10 = 10,0 °C in beiden Fällen 16.10. 20:02 und 18.10. 07:01), Leistungsfreigabe M8 (= 100), alle 100 Statusbytes (`_pi4.out`).
  - Mit Fühler = Mittel aus VL und RL und Schwelle 1,25 K passen 52/54 (nur #12 und 18.10. 20:32 daneben). Das ist ein Zwei-Parameter-Fit an 54 Segmenten → **Vermutung**, könnte aber die ungeklärte 1,5-K-statt-1,0-K-Frage aus F5 betreffen (anderer Fühler).

## Fazit: Regel jetzt 26/26?
**Nein, 25/26** (Modell A, RL, 1,5 K, Toleranz −1,0 … +1,5 min).
- #4 und #25 sind **erklärt**, beide mit Δ = 0 s gegen die X26-Freigabe. Sicherheit: **wahrscheinlich**. Die Zeitstempel sind sicher (Rohrahmen, CRC ok), der Mechanismus im Kälteregler ist aus dem Datenfit erschlossen.
- #12 kippt mit X26-Auflösung auf −2,8 min. Vorher stand er mit Modbus-Daten auf +0,4, weil die 5-min-Volllogger-Werte den 64-s-Zwischenwert 30,0 °C nicht zeigten.
- Über alle 54 Heiz-Segmente 16.–23.10. (Erstanforderungen, Wiederanläufe, Anforderungen ohne Freigabe): A 49/54, alte Regel B 48/54.

**Gültige Regel (Stand 24.10., wahrscheinlich):**
- Der HKA59-Timer startet, sobald RL ≤ S − 1,5 K gilt. S ist das aktuelle M0, in der Pause das letzte Heiz-M0.
- Zurückgesetzt wird er nur durch:
  - eine WW-Ladung;
  - RL > S − 1,5 K, während eine Heizanforderung anliegt und der Verdichter steht. Das gilt auch für kurze Zwischenwerte des Solls, etwa M0 = 30,0 °C für 8 s.
- Während eines Laufs ist der Timer eingefroren. In der Pause ohne Anforderung bleibt er stehen und wird nicht gelöscht.
- Freigabe = max(Anforderung, Stopp + 15 min, Timerstart + 15 min).

## Offene Reste
1. **Abend-Anforderungen mit S = 30,0 °C ohne Freigabe** (4 Fälle): unerklärt. Gegenbeispiel 18.10. 07:01:39 mit gleichem S wurde sofort freigegeben. Nächster Schritt (nur lesend): die 1-Hz-Werteblöcke Obj 0x50–0x5F im X26-Mitschnitt um 16.10. 20:02 und 18.10. 07:01 vergleichen.
2. **#12-Grenzfall (−2,8 min):** ob der Kälteregler RL feiner als 0,5 K auflöst oder eine kleine Reset-Hysterese hat, ist mit B29 nicht zu entscheiden.
3. **Herkunft der kurzen 30,0-°C-Werte in M0** (16.10. 13:18:43, 18.10. 18:08:20, 22.10. 07:01:33, 23.10. 16:50/20:51/22:21): von Loxone über 1490 oder TopTronic-intern (Mindest-VL beim Anlauf des Heizkreises)? Zu prüfen ist das mit der Loxone-Historie von 1490 (sekundengenau). Ist es Loxone, kann ein glatter 1490-Übergang solche HKA59-Resets vermeiden. Das ist eine **Vermutung** und nicht getestet.
4. **Fühlerfrage** (RL vs. Mittel VL/RL mit 1,25 K): Vermutung. Klären ließe sie sich mit mehr Grenzfällen oder durch Lesen des Kälteregler-Codes (Firmware, nicht Teil dieses Auftrags).
5. Laut Auftrag nicht geändert: `FRAGENKATALOG.md` und `ANALYSE_Sofortstart_HKA59_20261023.md`. Dort sind „#4/#25 offen“ und die Erklärung der 20:02-Fälle zu korrigieren, sobald diese Analyse abgenommen ist.

## Rohdaten-Stichprobe zum Gegenlesen
- `~/rs485_sniff/log/rs485_2026-10-16.log.gz` (Pi), dekodiert in `[lokaler Pfad]` (Abschnitt TAG 16):
  - `13:07:39 M0 77 0`
  - `13:07:52 B33 1 0`
  - `13:18:43 M0 0 60`
  - `13:18:51 M0 60 77`
  - `13:33:51 B22 0 77`
- Dasselbe für 23.10. (TAG 23):
  - `17:56:14 M0 66 0`
  - `17:56:15 B33 1 0`
  - `18:05:50 M11 0 64`
  - `18:06:14 M0 0 79`
  - `18:11:15 B22 0 79`
  - `18:11:37 B33 51 1`
- Gegenbeispiel Abend (TAG 16):
  - `20:02:33 M0 0 60`, dabei B29 = 73 (RL 26,0 °C) bis 20:02:41
  - kein `B22 0 …` bis zum Tagesende
- Befehl (Windows-PC, PowerShell, nur lesend):
  `Select-String -Path [lokaler Pfad] -Pattern '^(13:07:39|13:07:52|13:18:43|13:18:51|13:33:51|17:56:1[45]|18:06:14|18:11:15) '`