# ANALYSE F15: EEV Soll/Ist im Heizbetrieb (Winter), 02.11.2026

Nur lesend ausgewertet. Keine Schreibzugriffe, keine Bus-Probes.

## Kernaussage
- [sicher] Soll (Reg 134, Schreibzugriff der Regelung auf Slave 99) und Ist (Reg 131, Lesezugriff auf Slave 99) laufen im Heizbetrieb bei AT <= 5 C 1:1: Ist/Soll = 0,97 bis 1,00 je Lauf, in 95 % der Minuten Differenz <= 2 Schritte (11 Laeufe, 377 Minuten ohne Abtauung). Mittlere Abweichung je Lauf 0,5 bis 5 Schritte; Ausreisser (> 10 Schritte, 18 Minuten) sind Anlauf-/Stoppminuten.
- [sicher] Im Heizbetrieb wird das Ventil NICHT voll geoeffnet: Soll im Heizlauf max. 247 (Minutenmax; 50 %-Wert 204, 99 %-Wert 237) von 500. Heizen bei 31.10.-02.11. insgesamt nie > 261 (AT <= 8 C).
- [sicher] Voll offen (Soll 500, Ist 480) nur in der Abtauung: 02:21-02:27 und 04:45-04:51 (je ca. 7 Min.) im Heizlauf, 06:24-06:31 am Ende der WW-Ladung. Soll steht dort konstant bei 500, Ist erreicht 480 innerhalb von ca. 1 Minute und bleibt dort. Ist/Soll = 0,96 ist also kein Nachlauf, sondern Ist-Anschlag bei 480 [wahrscheinlich: Endanschlag/Skalierung des EVD, nicht belegt].
- Bewertung "EEV-Deckel widerlegt": [sicher] fuer den Heizbetrieb bestaetigt. Es gibt keinen Deckel unterhalb des Sollwerts; Ist folgt Soll bis 240 ohne Abflachung, und in der Abtauung erreicht Ist 480 bei Soll 500. Der niedrige Heizwert (um 200) kommt von der Regelung (Soll), nicht von einer Begrenzung am Ventil.

## Zugriff und Skalierung (am Mitschnitt geprueft)
- Slave 99 = 0x63. Pro Zyklus: FC06 Write Reg 0x0086 (=134), FC03 Read Reg 0x0083 (=131), FC03 Read Reg 0x0006, dazu FC01/FC05 Coils (u.a. Coil 10). Das passt zur Registerzuordnung in der Frage.
- Skalierung: Rohwert = Schritte, keine Faktoren. Beispiele (Datei `~/x4_sniff/x4_2026-11-02.log`, Pi): Zeile 3715682 `02:24:30 63 06 00 86 01 f4` (Soll 0x01f4 = 500) und Zeile 3715685 `63 03 02 01 e0` (Ist 0x01e0 = 480); 03:10:00 Zeile 4883463 `63 06 00 86 00 cd` (Soll 205) und Zeile 4883337 `63 03 02 00 cc` (Ist 204).
- Zeitstempel im Mitschnitt haben nur 1 s Aufloesung (viele Frames tragen dieselbe Sekunde), daher wurde je Minute gemittelt. Feinere Verzoegerung Soll->Ist ist so nicht messbar.
- Reg 6 (Slave 99): Rohwert gelesen, Bedeutung (Ueberhitzung?) und Skalierung [Vermutung], nicht belegt. Beispiel: 4-6 im ruhigen Heizlauf, 16 in der Abtauung, im Stillstand ~41. Die Spalte in den Tabellen mischt Anlauf-/Stoppminuten und ist nur Rohwert.

## Vorgehen
- X4-Frames: Pi `/home/<user>/x4_sniff/x4_<datum>.log(.gz)` fuer 31.10., 01.11., 02.11. (bis 08:00), gefiltert auf Slave 99, je Minute Soll/Ist/Reg6 aggregiert (`[lokaler Pfad]`, Lauf ueber `f15_run.sh`, nice, nur lesend).
- Ergaenzt aus `~/hoxpi_fulllog/ww_hires.csv` (AT = Aussen/10, Modulation, WW_Status, Status_HK1, WW_Soll_eff) -> `f15_auswertung.py`.
- Klassifizierung je Minute: aktiv = Soll oder Ist > 0; WW = WW_Status = 1 oder Status_HK1 = 6; Abtauung = Soll >= 450 oder WW_Soll_eff = 100, jeweils +-1 Minute. Heizlauf = zusammenhaengende aktive Nicht-WW-Minuten (Luecke <= 2 Min.), mind. 8 Minuten.
- Die Laeufe enthalten die Anlauf- und Auslaufminute mit Soll 0 (daher "min 0"). Abweichung = |Mittel Soll - Mittel Ist| je Minute.
- Alle Dateien: `[lokaler Pfad]` (CSV Minutenwerte, Skripte, `f15_ergebnis.md`).
- Nicht ausgewertet: 0x44-Abo-Effekte, EVD-Interna, Kaelteregler-Sollwertlogik.

## Ergebnistabellen
## Heizlaeufe (ohne Abtauminuten) - AT <= 5 C
| Lauf (Datum Beginn-Ende) | Min | AT C | Mod % | Soll min/mittel/max | Ist min/mittel/max | abs(Soll-Ist) mittel/max | Ist/Soll | Min mit Diff<=2 | Frames | Reg6 mittel |
|---|---|---|---|---|---|---|---|---|---|---|
| 11-01 03:31-04:04 | 34 | 4.7 | 34 | 0 / 180 / 226 | 0 / 180 / 226 | 1.4 / 23 | 1.00 | 91% | 68478 | 16.7 |
| 11-01 05:09-05:49 | 41 | 4.0 | 35 | 0 / 189 / 223 | 0 / 188 / 223 | 0.7 / 25 | 1.00 | 98% | 82557 | 4.5 |
| 11-01 06:58-07:29 | 32 | 3.5 | 35 | 0 / 172 / 216 | 0 / 172 / 216 | 1.5 / 22 | 1.00 | 94% | 64156 | 6.4 |
| 11-01 08:14-08:46 | 32 | 3.4 | 33 | 0 / 173 / 218 | 0 / 173 / 218 | 1.5 / 27 | 1.00 | 94% | 64212 | 4.5 |
| 11-01 10:20-10:56 | 37 | 4.6 | 35 | 0 / 188 / 225 | 0 / 188 / 225 | 1.4 / 29 | 1.00 | 92% | 74494 | 12.9 |
| 11-01 17:04-17:18 | 15 | 4.9 | 33 | 0 / 177 / 237 | 0 / 176 / 237 | 3.3 / 29 | 1.00 | 87% | 30032 | 21.1 |
| 11-02 02:13-02:19 | 7 | 3.6 | 43 | 0 / 154 / 247 | 0 / 150 / 232 | 5.0 / 33 | 0.97 | 86% | 13924 | 10.1 |
| 11-02 02:32-03:58 | 87 | 3.2 | 35 | 0 / 199 / 240 | 0 / 199 / 240 | 0.5 / 23 | 1.00 | 98% | 175051 | 5.7 |
| 11-02 04:36-04:43 | 8 | 2.9 | 31 | 0 / 71 / 190 | 0 / 68 / 190 | 2.4 / 18 | 0.97 | 88% | 16165 | 4.9 |
| 11-02 04:57-05:39 | 43 | 3.0 | 37 | 0 / 203 / 237 | 0 / 203 / 237 | 0.6 / 21 | 1.00 | 98% | 86540 | 4.6 |
| 11-02 06:34-07:15 | 41 | 3.2 | 34 | 0 / 181 / 216 | 0 / 181 / 216 | 1.1 / 21 | 1.00 | 95% | 82550 | 5.7 |

## Heizlaeufe AT > 5 C (nur zur Einordnung)
| Lauf (Datum Beginn-Ende) | Min | AT C | Mod % | Soll min/mittel/max | Ist min/mittel/max | abs(Soll-Ist) mittel/max | Ist/Soll | Min mit Diff<=2 | Frames | Reg6 mittel |
|---|---|---|---|---|---|---|---|---|---|---|
| 10-31 03:25-04:01 | 36 | 5.6 | 34 | 0 / 200 / 261 | 0 / 200 / 253 | 1.8 / 38 | 1.00 | 92% | 72619 | 38.0 |
| 10-31 05:09-06:10 | 62 | 5.7 | 34 | 0 / 207 / 248 | 0 / 207 / 248 | 1.0 / 37 | 1.00 | 97% | 124485 | 36.0 |
| 10-31 06:47-07:15 | 29 | 5.7 | 33 | 0 / 187 / 237 | 0 / 187 / 237 | 2.1 / 34 | 1.00 | 90% | 58310 | 32.2 |
| 10-31 08:35-08:45 | 11 | 5.8 | 34 | 0 / 178 / 246 | 0 / 175 / 246 | 3.0 / 20 | 0.98 | 82% | 22223 | 35.0 |
| 10-31 09:45-10:21 | 37 | 6.5 | 34 | 0 / 200 / 259 | 0 / 200 / 259 | 1.9 / 42 | 1.00 | 92% | 74563 | 44.7 |
| 10-31 10:59-11:24 | 26 | 7.8 | 33 | 0 / 217 / 287 | 0 / 217 / 287 | 2.8 / 45 | 1.00 | 92% | 52314 | 76.8 |
| 10-31 21:31-22:30 | 60 | 6.2 | 35 | 0 / 206 / 258 | 0 / 206 / 257 | 0.9 / 33 | 1.00 | 97% | 120478 | 36.3 |
| 10-31 23:19-23:57 | 39 | 5.7 | 33 | 0 / 187 / 244 | 0 / 187 / 243 | 1.6 / 36 | 1.00 | 92% | 78554 | 33.2 |
| 11-01 00:54-01:26 | 33 | 5.4 | 34 | 0 / 188 / 238 | 0 / 188 / 237 | 1.8 / 34 | 1.00 | 94% | 66537 | 30.1 |
| 11-01 02:31-02:45 | 14 | 5.0 | 30 | 0 / 150 / 230 | 0 / 149 / 230 | 3.3 / 29 | 0.99 | 86% | 28179 | 22.0 |
| 11-01 11:52-12:29 | 38 | 5.5 | 34 | 0 / 190 / 239 | 0 / 189 / 239 | 1.4 / 22 | 1.00 | 89% | 76329 | 22.8 |
| 11-01 14:24-14:53 | 30 | 6.1 | 35 | 0 / 193 / 249 | 0 / 192 / 249 | 1.9 / 33 | 1.00 | 93% | 60576 | 32.5 |
| 11-01 15:31-16:08 | 38 | 5.6 | 34 | 0 / 200 / 247 | 0 / 200 / 246 | 1.6 / 34 | 1.00 | 92% | 76436 | 26.8 |

## Abtauminuten in Heizlaeufen (Soll>=450 oder WW_Soll_eff=100, +-1 min)
| Lauf (Datum Beginn-Ende) | Min | AT C | Mod % | Soll min/mittel/max | Ist min/mittel/max | abs(Soll-Ist) mittel/max | Ist/Soll | Min mit Diff<=2 | Frames | Reg6 mittel |
|---|---|---|---|---|---|---|---|---|---|---|
| 11-02 02:20-02:27 | 8 | 3.6 | 37 | 0 / 395 / 500 | 0 / 382 / 480 | 40.1 / 107 | 0.97 | 12% | 16015 | 82.7 |
| 11-02 04:44-04:52 | 9 | 2.9 | 36 | 0 / 362 / 500 | 0 / 349 / 480 | 36.2 / 141 | 0.96 | 22% | 18113 | 77.2 |

## WW-Laeufe (zur Einordnung, Abtau-Minuten getrennt)
| Lauf (Datum Beginn-Ende) | Min | AT C | Mod % | Soll min/mittel/max | Ist min/mittel/max | abs(Soll-Ist) mittel/max | Ist/Soll | Min mit Diff<=2 | Frames | Reg6 mittel |
|---|---|---|---|---|---|---|---|---|---|---|
| 10-31 08:46-09:25 | 40 | 6.1 | 49 | 0 / 213 / 361 | 0 / 213 / 361 | 0.6 / 11 | 1.00 | 95% | 80749 | 37.8 |
| 10-31 11:39-13:07 | 89 | 9.4 | 54 | 0 / 250 / 352 | 0 / 249 / 351 | 0.9 / 47 | 1.00 | 97% | 179310 | 88.5 |
| 10-31 17:05-17:41 | 37 | 8.5 | 38 | 0 / 165 / 327 | 0 / 164 / 327 | 1.6 / 44 | 0.99 | 95% | 74462 | 61.9 |
| 10-31 20:00-21:11 | 72 | 6.8 | 49 | 0 / 195 / 332 | 0 / 196 / 331 | 0.2 / 7 | 1.00 | 99% | 144896 | 44.5 |
| 11-01 05:50-06:36 | 47 | 3.7 | 44 | 0 / 160 / 358 | 0 / 160 / 358 | 0.5 / 13 | 1.00 | 96% | 94557 | 4.6 |
| 11-01 13:00-13:37 | 38 | 6.1 | 38 | 0 / 136 / 259 | 0 / 135 / 256 | 1.4 / 33 | 0.99 | 92% | 76328 | 30.4 |
| 11-02 05:40-06:22 | 43 | 3.0 | 61 | 137 / 242 / 368 | 137 / 241 / 365 | 0.5 / 12 | 1.00 | 95% | 86412 | 4.8 |

Gesamt HEIZ AT<=5, ohne Abtau: 377 Minuten, Soll max 247, Ist max 240, mittl. Diff Soll-Ist 0.40, |Diff|<=2: 95%, |Diff|>10: 18 Minuten
Gesamt Abtau-Heiz-Minuten: 24, Soll max 500, Ist max 480, mittl. Soll-Ist 10.6
Heiz-Soll (Minutenmax) Perzentile 50/90/99/100: [204.0, 218.0, 237.0, 247.0]

## Aussage je Punkt
- Heizen AT <= 5 C, Soll = Ist: [sicher] (selbst gerechnet, 11 Laeufe, 3 Tage, davon 5 mit AT <= 3,6 C am 02.11. bzw. 01.11.).
- Heizen erreicht nie voll offen (max 247 von 500): [sicher].
- Abtauung: Soll 500 konstant, Ist 480: [sicher]; Grund fuer 480 statt 500 [Vermutung].
- Abtauung ist im Heizlauf genau 2x aufgetreten (02:21, 04:45), 06:24 zaehlt zur WW-Ladung. 31.10. und 01.11. (AT 3,4-8 C) hatten gar keine Abtauung mit Soll >= 400: [sicher] fuer diese Erkennungsregel; ob die Erkennung andere Abtauformen uebersieht [Vermutung, WW_Soll_eff = 100 wurde mitgenutzt].
- WW-Laeufe: Soll/Ist ebenfalls 1:1 bis max 368; kein Deckel: [sicher].

## Was bringt uns das
- Der Winterbetrieb zeigt, dass die EEV-Position im Heizen eine reine Reglerausgabe ist (um 200 Schritte = ca. 40 % von 500) und nicht begrenzt wird. Eine Optimierung am Ventil ist daher nur ueber die Sollwertlogik des Kaelte-/Ueberhitzungsreglers denkbar, nicht ueber ein "Deckel loesen".
- Die Rohdaten (Reg 134/131) genuegen als Mess-Ersatz fuer die Ventilstellung: Ist braucht keine eigene Pruefung, Soll reicht.
- Abtaudauer und Zeitpunkt lassen sich aus dem Soll-500-Block direkt ablesen (ca. 7 Min. je Abtauung bei AT ~3 C).

## Offen
- Skalierung/Bedeutung Reg 6 (Ueberhitzung?) und die Frage, warum Ist bei 480 stoppt.
- Heizlaeufe bei AT <= 0 C fehlen (Zeitraum war 2,9-4,9 C); dort kann sich das Bild aendern.
- Auswertung auf Minutenbasis; Sekunden-Verzoegerung Soll->Ist nicht ermittelt (Mitschnitt hat nur 1 s Zeitstempel, `~/x4_sniff/*.raw` hat gar keinen).
- `~/eev_845e_watch.log` (Trigger Reg134 1..30 bei Pel >= 1 kW) wurde nicht ausgewertet; Eintraege nur Dateinamen-Zeilen bis 14.09. gesichtet.