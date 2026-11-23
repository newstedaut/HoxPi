# F17 Rest: Abend-Anforderungen mit Soll 30,0 °C ohne Freigabe, Fall #12, Herkunft 30,0 (24.10.2026)

**Auftrag:** Orchestrator 24.10.2026 14:00, Katalog F17 (Rest). Nur gelesen (X26-Mitschnitt dekodiert, Volllogger), an der Anlage nichts geschrieben.
**Baut auf:** `[lokaler Pfad]` (Modell A, 49/54 Segmente), `ANALYSE_Sofortstart_HKA59_20261023.md`, `ANALYSE_Pumpe_ohne_Verdichter_20261024.md`.
**Konventionen wie dort:** X26 M0 = Heiz-Soll ×2, B29 = WEZ-RL: (B29 − 21)/2 °C, B22 0→x = Freigabe, B33 = Verdichterstatus (1 Heizen, 4 WW, 51 Anlauf), M11 Bit 64 = SG/PV-Bit. Schwelle = S − 1,5 K.

## Befund

1. **H-A („RL lag die ganze Zeit über S − 1,5 = 28,5 °C“) ist widerlegt (sicher, Messung).** In allen vier Abendfällen lag RL beim Eintreffen der Anforderung **unter bzw. auf 28,5 °C**, und zwar für 7 s bis 90 s. Erst danach stieg RL mit dem Pumpenlauf über 28,5 und blieb oben. Die Aussage in `ANALYSE_Pumpe_ohne_Verdichter_20261024.md` („RL nie ≤ Soll − 1,5“) gilt nur ab der ersten Minute. Der Grund ist der 5-min-Raster des Volllogger. Für die Startregel reicht die Bedingung bei der Anforderung: Sofortstarts kommen 0–1 s nach M0 (z. B. 18.10. 07:01:39 → 07:01:40 bei RL 28,0).
   - Fehlen kann also nur der **abgelaufene Timer**. Er hätte schon vorher, in der Pause, 15 min laufen müssen.
2. **Was die vier Abende gemeinsam haben (sicher, Messung):** In der Pause davor fiel das SG-Bit (M11 64 → 0), 59–89 min vor der Anforderung (23.10.: im letzten Lauf, 96 s vor dem Stopp). Zwischen dieser Flanke und der Anforderung gab es keine Heizanforderung und keine WW-Ladung. Beim Gegenbeispiel 18.10. 07:01:39 lag die letzte fallende Flanke (17.10. 18:42:53) vor mehreren Heizanforderungen.
3. **Neue Modellvariante E2 (wahrscheinlich, als Datenfit; den Mechanismus im Kälteregler habe ich nicht gesehen):** Fällt das SG-Bit, während weder eine Anforderung noch ein Lauf anliegt, wird der HKA59-Timer gelöscht. Danach startet er in der Pause nicht mehr. Erst eine neue Heizanforderung oder eine WW-Ladung gibt den Start wieder frei. Sonst gilt alles wie in Modell A.
   - **E2 trifft 52/54 Segmente** (A: 49/54) und 37/39 Anforderungsblöcke (A: 34/39).
   - Es löst 16./17./18.10. Kein Sofortstart und kein anderer Fall kippt.
   - Die alte Variante E (Flanke setzt immer zurück) hatte 16.10. 06:43 und #26 gebrochen. Bei E2 fallen diese beiden Brüche weg, weil die Flanke dort mit anliegender Anforderung bzw. im Lauf kam.
4. **23.10. 20:51 bleibt offen (erklärt: nein).**
   - Die SG-Flanke kam hier **im Lauf**: 19:51:42, Entzug M0 → 0 um 19:53:17, Stopp 19:53:18. E2 wertet das nicht.
   - Variante E4 wertet jede Flanke und hält den Freigabe-Sperrzustand bis zum nächsten Anforderungsbeginn. E4 löst 23.10., bricht aber #26 (23.10. 19:07, Flanke 18:51:26 im Lauf, Stopp 18:52:14) und 16.10. 06:43. Ergebnis: 51/54.
   - Unterschied zwischen den beiden Fällen: Bei #26 ging SG um 19:06:30 wieder an, also 32 s vor der Anforderung. Um 20:51 war es aus. Ob das SG-Wiedereinschalten die Sperre aufhebt, ist eine **Vermutung**. Mit einem Fall lässt sich das nicht prüfen.
5. **#12 (18.10. 18:02, 64-s-Zwischensoll 30,0) erklärt das Modell nicht auf die Sekunde (sicher: −2,82 min in allen Varianten A/E/E2/E4/E5).**
   - Gemessen: Freigabe 18:21:35 = Timerstart 18:06:36 + 15:00 − 1 s. Um 18:06:36 erreicht RL 36,5 = 38,0 − 1,5.
   - Die 30,0-Phase 18:08:20–18:09:24 mit RL 29,0 (0,5 K über der Schwelle) hat den Timer also **nicht** zurückgesetzt. Bei #4 (16.10. 13:18:43, 8 s 30,0, RL 30,5 = 2,0 K über der Schwelle) gab es dagegen einen Reset.
   - Eine Mindestdauer erklärt das nicht: 8 s setzen zurück, 64 s nicht.
   - Eine Reset-Hysterese von 0,5 K rettet #12, bricht aber 18.10. 17:05 und 23.10. 09:41 (E2 + HY 0,5: 51/54). Bleibt: Der Kälteregler sieht RL wahrscheinlich feiner als die 0,5-K-Stufe von B29. Der echte Wert lag vermutlich bei ≤ 28,5. Das ist eine **Vermutung**.
6. **Herkunft der 30,0 °C (sicher für die langen Abendwerte, wahrscheinlich für die kurzen):**
   - **Abends schreibt Loxone 1490 = 24,0 °C.** Die TopTronic macht daraus 1520 = 30,0 °C. Das ist eine Mindestbegrenzung: 24,0 + 3 K Überhöhung = 27,0 → angehoben auf 30,0.
   - In allen vier Abenden steht im Volllogger `1490=240 1520=300 1501=23`.
   - Sonst gilt 1520 ≈ 1490 + 3 K, abgerundet auf 0,5 K: 35,7 → 38,5, 36,2 → 39,0, 29,6 → 32,5, 28,2 → 31,0.
   - Die kurzen 30,0-Werte beim Anforderungsbeginn haben zwei Ursachen.
     - 16.10. 13:18:43 (8 s): Loxone stand um 13:20:01 schon fest auf 1490 = 357. Den Wert gibt **wahrscheinlich** die TopTronic selbst aus: erst ihr Mindestwert, dann der berechnete Soll.
     - 18.10. 17:05:24 (25 s): Loxone lief eine Rampe, um 17:05:02 stand 1490 = 263 (26,3 + 3 = 29,3, also 30,0), um 17:10:02 1490 = 352. Ursache ist **wahrscheinlich** Loxone mit der TopTronic-Mindestbegrenzung.
     - 18.10. 07:01:39 und 22.10. 07:01:33 habe ich nicht weiter belegt.
   - Der 64-s-Wert bei #12 fällt in einen Loxone-Übergang (18:05:01 1490 = 353 → 18:10:02 1490 = 296). Ob Loxone kurz ≤ 27,0 geschrieben hat, sieht man im 5-min-Raster nicht (**offen**).
   - Woher die 24,0 in Loxone kommen (Ofen-Nachlauf, Klimacontroller oder Mindestwert der Formel), ist mit den vorhandenen Daten nicht belegbar. Die Loxone-Historie habe ich nicht abgefragt.


## Tabelle: vier Abendfälle und Gegenbeispiel (X26, sekundengenau; Volllogger 5 min)

| Fall | Letzte SG-Flanke 64→0 (Zustand) | Stopp vorher | Anf. M0 = 60 (S 30,0) | RL bei Anf. | RL ≤ 28,5 bis | RL danach (max) | 1490 / 1520 (Volllogger) | Freigabe | A | E2 |
|---|---|---|---|---|---|---|---|---|---|---|
| 16.10. | 18:43:54 (Pause) | ~18:29 | 20:02:33 | 25,5–26,0 | 20:02:56 (24 s), 29,0 ab 20:02:57 | 36,0 (20:08:30) | 20:05:02 240 / 300 | keine (pump-only bis ~23:50) | XX | OK |
| 17.10. | 18:42:53 (Pause) | ~18:21 | 20:11:25 | 27,5 | 20:11:42 (18 s), 29,0 ab 20:11:43 | 38,0 (20:16:55) | 20:15:02 240 / 300 | keine | XX | OK |
| 18.10. | 19:05:32 (Pause) | ~18:38 | 20:32:44 | 25,5 | 20:33:42…20:34:13 (89 s), 29,0 ab 20:34:14 | 33,5 (20:38:38) | 20:35:01 240 / 300 | keine | XX | OK |
| 23.10. | 19:51:42 (**im Lauf**, Stopp 19:53:18) | 19:53:18 | 20:51:01 | 28,0 | 20:51:07 (7 s), 29,0 ab 20:51:08 | 40,0 (20:55:34) | 20:55:01 240 / 300 | keine | XX | **XX** |
| Gegenbsp. 18.10. | 17.10. 18:42:53, danach Anforderungen 17.10. 20:11 u. a. | 17.10. abends | 07:01:39 | 28,0 | – (Freigabe 1 s später) | (WW ab 07:01:55) | 07:05:01 302 / 560 (WW) | **07:01:40** | OK | OK |
| #12 18.10. | 15:58:53 / 16:04:29 an (SG an) | 18:02:13 (WW-Ende) | M0 38,0 ab 18:02:12, 30,0 18:08:20–18:09:24, dann 32,5 | 29,0 in der 30,0-Phase | nie (min 29,0) | – | 18:05:01 353 / 380, 18:10:02 296 / 325 | 18:21:35 | −2,82 | −2,82 |

In allen vier Abendfällen lief der Verdichter in der ganzen Anforderung nicht (B33 = 0, B22 = 0, **sicher**). 16.10. 20:02 hat seine Freigabe erst mit der nächsten Anforderung bekommen; die lange Pumpenepisode steht in F18.

## Belegzeilen (zum Nachschlagen)

Datei X26 dekodiert: `[lokaler Pfad]`. Format `hh:mm:ss Feld alt neu`, Abschnitt `TAG dd`. Volllogger: `[lokaler Pfad]` bzw. am Pi `~/hoxpi_fulllog/2026-10-23.csv` (Spalten 1490 = Feld 15, 1520 = Feld 45).

- 16.10. (TAG 16): `18:43:54 M11 64 0` · `20:02:33 M0 0 60` · `20:02:54 B29 77 78` (28,5) · `20:02:57 B29 78 79` (29,0) · Volllogger `2026-10-16 20:05:02 1490=240 1520=300 1501=23 1539=0`
- 17.10. (TAG 17): `18:42:53 M11 64 0` · `20:11:25 M0 0 60` · `20:11:40 B29 77 78` · `20:11:43 B29 78 79` · Volllogger `2026-10-17 20:15:02 1490=240 1520=300`
- 18.10. (TAG 18): `19:05:32 M11 64 0` · `20:32:44 M0 0 60` · `20:33:42 B29 77 78` · `20:34:14 B29 78 79` · Volllogger `2026-10-18 20:35:01 1490=240 1520=300`
- 23.10. (TAG 23): `19:51:42 M11 64 0` · `19:53:17 M0 78 0` · `19:53:18 B33 1 0` · `20:51:01 M0 0 60` · `20:51:08 B29 77 79` · Volllogger `2026-10-23 20:55:01 1490=240 1520=300 1501=23 1539=0`
- Gegenbeispiel (TAG 18): `07:01:39 M0 0 60` · `07:01:40 B22 0 60` · `07:01:40 B33 0 51` (RL B29 = 77 = 28,0)
- #12 (TAG 18): `18:06:36 B29 96 94` (36,5 = 38,0 − 1,5) · `18:08:18 B29 80 79` (29,0) · `18:08:20 M0 76 60` · `18:09:24 M0 60 65` · `18:21:35 B22 0 65`
- #26 zum E4-Konflikt (TAG 23): `18:51:26 M11 64 0` (im Lauf) · `19:06:30 M11 0 64` · Anforderung 19:07:02 · Freigabe 19:07:15 (= Stopp 18:52:14 + 15:00)

Skripte und Ausgaben (alle neu, nur lesend):
- `[lokaler Pfad]` → `_win.out`: Fenster −90/+30 min um die sechs Fälle.
- `[lokaler Pfad]` → `_g2.out`: Blockmodell (Kopie von `or_f17x_..._g.py`), Varianten A, P, E, E2, E3. Ergebnis A 34/39, P 29/39, E 36/39, E2 37/39.
- `[lokaler Pfad]` → `_h2.out`: Segmentmodell (Kopie von `or_f17x_..._h.py`), Aufruf `RL 1.5 E2,E4,E5 0`, viertes Argument = Reset-Hysterese.
- Ergebnis mit HY = 0: A 49, E 51, **E2 52**, E4 51, E5 51 von 54. Mit HY = 0,5: E2 51/54, mit HY = 1,0: E2 50/54.
- `[lokaler Pfad]`: liest die Volllogger-Spalten 1490/1520/1501/1539/1535/1525 in Zeitfenstern.
- Variante P (in der Pause weder Start noch Reset) ist **widerlegt**: Sie bricht 5 Sofortstarts (16.10. 05:49, 18.10. 07:01, 21.10. 15:24, 22.10. 04:21, 23.10. 03:00). Der Timer läuft in der Pause also normal; nur nach einer SG-Abschaltung läuft er nicht.

## Offene Reste

1. **23.10. 20:51** (SG-Flanke im Lauf) gegen **#26** (SG-Flanke im Lauf, aber SG 32 s vor der Anforderung wieder an): Welche Regel trennt die beiden? Kandidat: Das Wiedereinschalten von SG hebt die Sperre auf (**Vermutung**). Prüfen lässt sich das am nächsten Abend, an dem SG endet, während der Verdichter läuft.
2. **#12:** Der Kälteregler setzt bei RL 29,0 (B29) nicht zurück, bei 30,5 aber schon. Wahrscheinlich löst er RL feiner auf als B29. Prüfweg, nur lesend: die 1-Hz-Werteblöcke Obj 0x50–0x5F im X26-Mitschnitt um 18.10. 18:08 nach einem RL-Wert mit 0,1-K-Auflösung durchsuchen.
4. **Was M11 (Bit 64) genau ist:** Nach der bisherigen Doku das SG-/PV-Bit der TopTronic. Die Flanken passen zu „PV-Überschuss endet“ (abends 18:42–19:51). Dass der Kälteregler daran den HKA59-Timer koppelt, ist aus dem Fit **erschlossen und nicht belegt**.

## Was bringt uns das

- **Die Startregel wird deutlich besser:** 52 von 54 Segmenten statt 49. Die Abendfälle sind kein Messfehler. Nach dem Ende von PV/SG wartet die WP einfach 15 min mit kaltem RL, bevor sie wieder anlaufen darf. Abends kommt dieser Zustand nie zustande: Loxone fordert mit 24,0 → 30,0 °C an, die HK1-Pumpe hebt RL in Sekunden über 28,5, also bleibt der Verdichter aus.
- **Praktisch ist das sogar erwünscht:** Abends mit Soll 30,0 holt die FBH die Restwärme aus dem Puffer, ohne einen Kurzlauf der WP (siehe F18, Pumpenkosten ~0,08 kWh am Tag). Wer abends wirklich einen Start will, braucht einen Soll mit Schwelle über dem RL, also 1520 ≥ RL + 1,5 K, oder eine Anforderung, die länger als 15 min ansteht, während RL unter der Schwelle liegt.
- **Für die Startvorhersage in Loxone:**
  - Freigabe ≈ max(Anforderung, Stopp + 15 min, Timerstart + 15 min).
  - Eine Anforderung nach einer SG-Abschaltung in der Pause startet nie sofort.
  - 1490 unter etwa 27 °C wirkt in der Hoval wie 30,0 °C, wegen der +3 K Überhöhung und der Mindestbegrenzung.
- Nichts an der Anlage geändert. Kein Parameter verstellt.