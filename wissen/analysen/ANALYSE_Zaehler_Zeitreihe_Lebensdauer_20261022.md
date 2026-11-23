# Firmware-Zähler als Zeitreihe: Lebensdauer-Bilanz belastbar, WW ~20 kWh Wärme/Tag
Orchestrator 22.10.2026 20:10 · nur lesend · Pi: `Emulation\or_zaehler_tage_20261022_2000.py/.out` (Volllogger `~/hoxpi_fulllog/` 30.07.–22.10., 85 Tage, Tagesdifferenzen 27484/85, 27488/89, 25613/14, 1517, 1519) · Fotos: `Bildanalyse_05_2026-01-09.md`, `Bildanalyse_06/07_2026-03-17*.md` · CAN: `Bedienteil_Katalog.md` (Mitschnitt 06.09.2026) · 2021-Fotos `IMG_20211107_*` zeigen nur den Technikraum, keine Zählerstände.

## Stützstellen (alle Zähler in kWh bzw. h)
| Datum | Quelle | Wärme gesamt | E_el | Betriebsstd. | Starts |
|---|---|---|---|---|---|
| 09.01.2026 | Display-Foto | 97 511 („Wärmemenge Heizen“) | – | 13 058 | 17 100 |
| 17.03.2026 | Display-Foto | 104 116 („Wärmemenge Heizen“) | 28 250 | 13 919 | 18 476 |
| 06.07.2026 | Modbus (review_all_out) | Heizen allein 71 824 | 29 696 | – | – |
| 06.09.2026 | CAN dp 59/63/67/71 | 111 560 | 30 012 | 14 743 | 20 373 |
| 22.10.2026 | Volllogger/X26 | 113 062 (72 569 + 522 + 39 971) | 30 383 | 14 896 | 20 688 |

**Sicher:** Die Display-Zeile „Wärmemenge Heizen“ ist **nicht** dp 47 (Heizen allein, im Juli 71,8 MWh), sondern passt lückenlos zur **Summe dp 59** (104,1 → 111,6 → 113,1 MWh). Wahrscheinlich ist das Display-Etikett irreführend; jedenfalls lassen sich Fotowerte und Mitschnitt nur so zu einer stetigen Reihe verbinden.

## Raten je Abschnitt
| Abschnitt | Tage | Wärme/Tag | Strom/Tag | AZ | Laufzeit/Tag | Starts/Tag | min/Start |
|---|---|---|---|---|---|---|---|
| 09.01.–17.03. (Winter) | 67 | 98,6 kWh | – | – | 12,9 h | 20,5 | 38 |
| 17.03.–06.09. | 173 | 43,0 kWh | 10,2 kWh | 4,22 | 4,8 h | 11,0 | 26 |
| 06.09.–22.10. | 46 | 32,6 kWh | 8,1 kWh | 4,05 | 3,3 h | 6,8 | 29 |
| 19.09.–22.10. (Logger lückenlos) | 33 | Heizen 15,4 + WW 19,7 | 9,0 kWh | 3,91 | – | – | – |

- **WW-Wärme:** 01.09.–22.10. 928 kWh / 51 Tage = **18,2 kWh/Tag**, 19.09.–22.10. **19,7 kWh/Tag**, Lebensdauer 39 971 kWh / 1 840 Tage = **21,7 kWh/Tag**. Die Größenordnung ist also seit Jahren gleich – kein neues Problem, sondern ein Dauerzustand.
- **Gegenprobe zur Lauf-Analyse** (`ANALYSE_Arbeitszahl_je_Lauf_19-22Okt_20261022.md`, AZ Heizen 5,06 / WW 3,04): 507/5,06 + 649/3,04 = 313 kWh Strom gegen gemessen 296 kWh (−6 %) → die Lauf-AZ passen zu den Zählern. **~72 % des WP-Stroms gehen ins WW** (213 von 296 kWh in 33 Tagen ≈ 6,5 kWh/Tag ≈ 1,35 €/Tag bei 21,15 ct).
- **Lebensdauer-Plausibilität (IBN 08.10.2021):** Jahreswärme aus den 2026-Raten grob 21 MWh (Lücke 22.10.–09.01. mit ~70 kWh/Tag geschätzt) × 5,04 Jahre ≈ 106 MWh gegen 113 MWh Zählerstand → **wahrscheinlich liefen die Zähler ab IBN bei ~0** (keine große Vorbelegung). Eine Vorbelegung < ~10 MWh ist damit nicht ausgeschlossen (Vermutung, Winter 2021/22–2024/25 unbekannt).
- **Winter-Taktung:** Jan.–März 2026 20,5 Starts/Tag bei 38 min je Start – im Winter fast doppelt so viele Starts wie im Lebensschnitt (11/Tag). Kein Kurztakten, aber für den kommenden Winter Taktschutz (V99/V101) im Auge behalten.

## Logger-Auffälligkeiten (für den Loop)
- 27488/89 (WW-Zähler) im Volllogger bis 31.08. immer 0 → WW erst ab 01.09. auswertbar.
- 25613/14 (E_el) 09.–18.09. eingefroren bzw. 0 (Stand springt 30 027 → 0 → 30 087). Passt zeitlich zu den Umbauten am Logger; Tagesbilanzen in diesem Fenster nicht verwenden.
- Spalte 1477 (Außen) steht in 0,1 °C.

## Byte 83/86/88/89 (X26 Obj 0x20) – Namenssuche
In der offiziellen Modbus-Liste (`WEZ_Register_offiziell_UnitId1.csv`) und im Guideline-Excel gibt es für fg 60/fn 254 **keine** dp 83/86/87/88/89. Im `SPEZ_CAN_Datenpunkte.csv` stehen sie nur als „Istwerte / Fühler (00-083 … 00-089)“, CAN-Mitschnitt 06.09.: dp 83 = 10, dp 86/87/89 = 0, dp 88 = 0 (2 Byte). **Rolle bleibt offen.** Einziger billiger Weg zum Namen: am Bedienteil Service › TTE-WEZ › FA Allgemein die Zeilen 00-083 bis 00-089 fotografieren (Text steht dort im Klartext).

## Was bringt uns das
- Die Lebensdauerzahlen (JAZ 3,7, WW 35 % der Wärme, ~20 kWh WW-Wärme/Tag) sind jetzt **mehrfach belegt** – Fotos, CAN und Mitschnitt ergeben eine stetige Reihe. Die WW-Entscheidung (Soll 57 → 52, Ladungen bündeln) steht damit auf festem Boden.
- Grobe Größenordnung (Vermutung, je nach Ursache Verlust vs. Zapfung): 30 % weniger WW-Wärme ≈ 2 kWh Strom/Tag ≈ 150 €/Jahr.
- Für Vergleiche Winter 2026/27 gegen 2025/26 gibt es jetzt Referenzraten (Jan.–März: 98,6 kWh Wärme/Tag, 12,9 h, 20,5 Starts).


## Nachtrag 24.10.2026 – F16 dp 83
Orchestrator 24.10.2026 01:00–01:45 · nur lesend · Backup `HoxPi-Doku\ANALYSE_Zaehler_Zeitreihe_Lebensdauer_20261022_bak_20261024_0100_or.md` · Skripte `Emulation\or_f16_20261024_0100.py/.out` (Hauptauswertung), `Emulation\or_f16_20261024_0130_ww.py` (WW/Heizen je Lauf über Zähler), `Emulation\or_f16_20261024_0140_stichprobe.sh` (Einzelprüfung). Daten: X26-Sniffer `~/rs485_sniff/log/rs485_2026-10-21/22/23.log.gz` (Obj 0x20, ~1 Frame/s, Byte 83 = Payload[83] = body[87]) gegen Volllogger `~/hoxpi_fulllog/2026-10-21/22/23.csv(.gz)`, je Volllogger-Stempel Mittel von Byte 83 über die 60 s davor (wegen WEZ-Alter ≤ 60 s). Je Lauf nur Punkte ab 2 min nach Start bis 1 min vor Ende.

**Reg 31708 offiziell (sicher):** `WEZ_Register_offiziell_UnitId1.csv` Zeile 359/360 und `SPEZ_CAN_Datenpunkte.csv` Zeile 1094: dp **60-7-302 „Volumenstrom gemittelt“** (Automat, WFA200), S32 über 31707 (high) / 31708 (low), 1 Dezimale, **L/min**. 31707 war in allen Laufpunkten 0, also ist 31708 allein der volle Wert (Rohwert 342 = 34,2 L/min). 31708 lebt (85 verschiedene Werte 2–378 in den Läufen, 0 im Stillstand) – kein eingefrorenes Register. Die beiden anderen „Volumenstrom“-Register 18741/18756 (Energiebilanzierung, 10-1/10-0-21105) stehen dauerhaft auf 0.

### Ergebnis je Lauf (Lauf = Byte 83 > 0, Lücke ≤ 60 s)
WW/Heizen aus den Volllogger-Zählerdifferenzen 27485 (Heizen) und 27489 (WW); Reg 19870 (UKA) steht im Volllogger durchgehend auf 0 und taugt hier nicht.

| Lauf | Art (Zähler) | Dauer min | n 5-min | Byte 83 Mittel | 31708 Mittel (0,1 L/min) | Verhältnis | r im Lauf |
|---|---|---|---|---|---|---|---|
| 21.10. 03:57–04:28 | WW (27489 +5) | 31,7 | 6 | 13,32 | 219,8 | 16,51 | +0,999 |
| 21.10. 06:35–07:05 | – | 30,0 | 5 | 13,97 | 231,4 | 16,56 | +0,988 |
| 21.10. 16:38–18:16 | Heizen+WW (+3/+4) | 97,2 | 18 | 13,89 | 230,4 | 16,59 | +0,999 |
| 21.10. 19:26–20:50 | – | 84,5 | 16 | 13,91 | 232,4 | 16,71 | +0,997 |
| 22.10. 04:21–05:01 | Heizen (+6/0) | 40,2 | 8 | 20,72 | 342,6 | 16,54 | +0,310 ¹ |
| 22.10. 07:01–07:50 | – | 48,6 | 9 | 15,68 | 261,3 | 16,67 | +1,000 |
| 22.10. 09:56–11:32 | WW (27489 +18, VL 51–53 °C) | 96,4 | 19 | 13,65 | 227,5 | 16,67 | +0,994 |
| 22.10. 13:14–13:55 | WW (+5, VL 59–60 °C) | 40,4 | 7 | 19,29 | 323,0 | 16,74 | +0,996 |
| 23.10. 03:01–03:41 | Heizen (+5/0) | 40,5 | 8 | 20,64 | 341,9 | 16,57 | +0,124 ¹ |
| 23.10. 04:30–12:01 | Heizen (+28), WW (+8) | 450,9 | 90 | 15,64 | 260,5 | 16,65 | +0,991 |
| 23.10. 16:04–16:53 | – | 49,4 | 9 | 17,48 | 291,4 | 16,67 | +0,998 |
| 23.10. 18:06–18:52 | Heizen (+6/0) | 46,2 | 9 | 19,43 | 321,8 | 16,56 | +1,000 |
| 23.10. 19:07–19:53 | Heizen (+7/0) | 46,5 | 9 | 20,72 | 342,8 | 16,54 | +0,324 ¹ |
| 23.10. 20:51–22:51 | keiner (0/0, VL ≈ RL) ² | 120,2 | 24 | 9,92 | 160,0 | 16,14 | +0,603 ¹ |

Insgesamt 20 Läufe in 3 Tagen (Rest in `.out`). ¹ r klein, weil Byte 83 im Lauf fast konstant (20–21 bzw. 10) ist – das Verhältnis passt trotzdem. ² Pumpe läuft 2 h ohne Wärmezählung, VL 36,0 / RL 35,5 °C: wahrscheinlich Pumpenlauf ohne (nennenswerten) Verdichter; „Lauf“ heißt hier also Pumpe, nicht Verdichter. „–“ = nicht per Zähler geprüft.

**Gesamt (sicher, gemessen):** 853 gemeinsame Punkte r = +0,990; nur Laufpunkte (n = 290) r = +0,932, Ursprungsgerade **31708 = 16,56 × Byte 83** (Median 16,58, p10 16,13, p90 17,00). Nur 2 von 853 Punkten widersprechen sich beim An/Aus (je der Stempel direkt nach Laufende, 31708 schon 0 – Mittelung/Alter). Heiz- und WW-Läufe liefern dasselbe Verhältnis – es hängt nicht an Betriebsart oder Pumpenstufe.

**Skalierung (wahrscheinlich):** 16,67 × 0,1 L/min = 1,667 L/min = 100 l/h. Byte 83 ist also sehr wahrscheinlich der **Volumenstrom in 0,1 m³/h** (ganzzahlig): 11 ≈ 1,1 m³/h ≈ 18 L/min, 21 ≈ 2,1 m³/h ≈ 35 L/min. Abweichung des gemessenen Faktors 16,56 vom runden 16,67 = −0,6 % (Rundung auf ganze Byte-Schritte + „gemittelt“ in 31708). Dass Byte 83 statt des Durchflusses eine Pumpenstellgröße (PWM) ist, ist unwahrscheinlich: die wäre kaum in Heiz- und WW-Betrieb mit demselben Faktor proportional (wahrscheinlich, nicht bewiesen).

**Name (Vermutung → offen):** In keiner Datenpunktliste steht dp 00-083 mit Klartext (siehe Abschnitt oben). Der Name „Volumenstrom“ ist aus den Daten abgeleitet, nicht abgelesen. Endgültig nur per Foto Bedienteil Service › TTE-WEZ › FA Allgemein Zeile 00-083.

**Stichprobe (sicher, nachprüfbar):** 23.10.2026 05:45:02 – Byte 83 in allen 61 Frames 05:44:02–05:45:02 = 20 (Mittel 20,43 inkl. Rand), Volllogger Spalte 500 (= 31708) Rohwert 340 → 34,0 L/min; 20 × 1,667 = 33,3 L/min. Prüfbefehl: `sh /tmp/or_f16_stichprobe.sh` auf dem Pi (Kopie `Emulation\or_f16_20261024_0140_stichprobe.sh`, Laufzeit ~1,5 min).

### Was bringt uns das
- **F16 erledigt (wahrscheinlich, Faktor gemessen):** Byte 83 = Volumenstrom in 0,1 m³/h, sekundengenau vom X26-Sniffer – viel feiner als 31708 (gemittelt, bis 60 s alt, 5-min-Raster im Volllogger).
- Damit lässt sich aus dem Sniffer allein die **Wärmeleistung sekundengenau** rechnen: Q = Byte83 × 100 l/h × 1,16 Wh/(l·K) × (VL − RL) mit Byte 17/29 (0,5-K-Auflösung, daher eher als Mittel über Minuten sinnvoll).
- Beobachtung für die Optimierung: Volumenstrom je Lauf schwankt zwischen ~1,0 und 2,1 m³/h (16–34 L/min); reine Heizläufe lagen meist bei ~2,0–2,1 m³/h, WW-Läufe bei 1,3–1,9 m³/h (sicher gemessen). Ursache (Pumpenansteuerung/Ventilstellung) offen (Vermutung: drehzahlgeregelte WEZ-Pumpe).
- Der 2-h-Pumpenlauf 23.10. 20:51–22:51 ohne Wärmezählung ist eine eigene Frage (Pumpennachlauf? Frostschutz? Loxone-Anforderung ohne Verdichterstart?) – Kandidat für den Katalog.