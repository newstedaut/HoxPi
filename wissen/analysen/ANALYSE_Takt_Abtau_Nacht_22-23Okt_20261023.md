# Analyse: Erste kalte Nacht 22./23.10.2026 - Taktung, Mindestlaufzeit V101, Abtauungen (D-01-Gegenprobe)
Orchestrator 23.10.2026 01:00, nur lesend. Zeitraum 22.10. 00:55 bis 23.10. 00:55:52 (letzte Zeile im Log).

**Quellen (alle nur gelesen):**
- `~/hoxpi_fulllog/ww_hires.csv` ab 21.10. 22:00 (2 666 Zeilen, Raster 10-60 s, keine Luecke > 180 s). Einheiten: Temperaturen x10, P_el x10 W (207 = 2,07 kW), Modulation %.
- X4-Sniffer `~/x4_sniff/x4_2026-10-22.log.gz` und `x4_2026-10-23.log`: Luefter-Schreibbefehl `06 06 d0 01 VV VV` (Slave 6, FC6, Reg 0xD001) sekundengenau.
- RS485/X26-Log nicht gebraucht (keine Kurzlaeufe, keine Abtauung zu zerlegen).
- Skript `HoxPi-Doku\or_takt_20261023_0100.py` / `.out`, plus einzelne gefilterte grep/awk-Abfragen (siehe Befehle unten).

## Ergebnis kurz
- **Die "kalte Nacht" war fuer die WP keine: Verdichter seit 22.10. 18:59:06 aus, bis Datenende 23.10. 00:55 (356 min).** `Status_HK1` = 0 durchgehend, Heizkreis fordert nicht an. Aussen (Geraetefuehler) faellt dabei 6,4 -> 3,8 C, Vorlauf 52 -> 31 C (Abkuehlung der Leitung, keine Waermeabgabe der WP). - **belegt**
- **7 Verdichterlaeufe** im Zeitraum, alle am 22.10.: 3x Heizen (16-40 min), 4x Warmwasser (22-96 min). Am 23.10. bis 00:55: 0 Starts. - **belegt**
- **Kurzlaeufe < 10 min: keine.** Kuerzester Lauf 16,1 min (<MAC>, X4). -> **V101 (300 s +/- 10 s) in dieser Nacht nicht pruefbar.**
- **Abtauungen: keine.** Kein `WW_Soll_eff` = 10,0, kein Luefter 0 waehrend Lauf mit anschliessendem 0x2200 / ~0xB7xx-300-s-Muster (V102). Aussen bei Laufbeginn 6,4-10,7 C, bei den Heizlaeufen 6,4-7,3 C. -> **D-01-Gegenprobe nicht moeglich.**
- **Heizstab: nein.** P_el max 5,20 kW (WW-Lauf 22.10. 05:48-06:37), nie > 7,5 kW. Fehlercode durchgehend 255 (keine Stoerung).
- **Neu, auffaellig (Beobachtung):** WW-Lauf ab 09:56:42 laeuft laut ww_hires 3,4 min mit Mod 14-48 %, waehrend X4 fuer 0xD001 durchgehend `0000` zeigt; Luefter erst 10:00:05 (`bbb6`). Alle anderen 6 Starts: Luefter 0-20 s vor/um Mod > 0.

## Verdichterlaeufe 22.10. 00:55 - 23.10. 00:55 (belegt)
Start/Ende = X4 Luefter 0xD001 >0 bzw. `0000` (sekundengenau); in Klammern erster Messpunkt Mod > 0 in ww_hires. Aussen = Spalte `Aussen` beim Start (Geraetefuehler, steigt beim Lauf durch Luefterabwaerme - nur grob).

| # | Start | Ende | Dauer | Betrieb | Mod min-max (Mittel) | Aussen | VL/RL Start -> Ende | P_el max | Was beendete den Lauf |
|---|---|---|---|---|---|---|---|---|---|
| - | 21.10. vor 21:00 | - | Pause bis 04:21 | - | - | 7,4 | - | - | (Pause 381 min seit 22:00) |
| 1 | 04:21:56 (04:22:52) | 05:01:34 | 39,6 min | HZ | 35-42 (36) | 7,3 | 34,0/32,0 -> 39,0/36,0 | 2,07 kW | `Status_HK1` 23 -> 0 (05:01:52) |
| 2 | 05:48:44 (05:48:52) | 06:37:02 | 48,3 min | WW | 17-79 (41) | 7,0 | WW 47,1 -> 52,0 C | 5,20 kW | `WW_Status` 1 -> 0 um 06:36:32 (WW_Ist 52,0 = Soll 52,0), Mod 0 ab 06:37:11 |
| 3 | 07:21:27 (07:21:52) | 07:49:57 | 28,5 min | HZ | 35-46 (36) | 6,5 | 32,0/31,5 -> 39,0/36,0 | 2,26 kW | `Status_HK1` 23 -> 0 (Zeile 07:49:52, Mod noch 35) |
| 4 | 08:18:32 (08:18:51) | 08:34:38 | 16,1 min | HZ | 32-42 (36) | 6,4 | 31,0/30,5 -> 36,0/33,0 | 2,13 kW | `Status_HK1` 23 -> 0 (Zeile 08:34:52) |
| 5 | 09:56:42 (hires; X4-Luefter erst 10:00:05) | 11:32:21 | 95,7 min | WW | 14-78 (56) | 7,0 | WW 47,2 -> 51,7 C | 5,09 kW | `WW_Status` 1 -> 0 um 11:31:52 |
| 6 | 13:15:05 (13:15:12) | 13:51:15 | 36,2 min | WW | 2-52 (34) | 10,7 | WW 52,0 -> 56,2 C | 3,67 kW | `WW_Status` 1 -> 0 um 13:51:02 (WW_Soll_eff danach 56,1) |
| 7 | 18:37:12 (18:37:22) | 18:59:06 | 21,9 min | WW | 17-67 (38) | 7,1 | WW -> 51,5 C | 4,71 kW | `WW_Status` 1 -> 0 um 18:58:41 |
| - | 18:59:06 | (23.10. 00:55 noch aus) | >= 356 min | - | 0 | 6,4 -> 3,8 | VL 52 -> 31 C | 0 | `Status_HK1` = 0 durchgehend |

Summe Verdichterlaufzeit: ~286 min (HZ 84 min, WW 202 min). Starts: 22.10. = 7, 23.10. (bis 00:55) = 0. Pausen zwischen Laeufen: 47 / 44 / 27 / 82 / 103 / 286 / >356 min - keine unter 15 min.

Ende-Muster (belegt an 7/7):
- **Heizlaeufe enden mit `Status_HK1` 23 -> 0** im selben 1-min-Messpunkt wie Mod -> 0. Also Anforderung weg, nicht Soll-VL erreicht und nicht Mindestlaufzeit.
- **WW-Laeufe enden 30-50 s nach `WW_Status` 1 -> 0** (WW_Ist erreicht WW_Soll_eff), SLP laeuft noch nach.

## V101 (Mindestlaufzeit 300 s +/- 10 s)
- **Nicht ermittelbar in diesem Zeitraum** - kein Lauf unter 16 min. Status unveraendert: "wahrscheinlich ~5 min, wird bei Wegfall der Anforderung nicht erzwungen" (aus `ANALYSE_Taktschutz_V99_V101_20261022.md`).
- Neu belegt: Heizlaeufe enden **genau dann, wenn `Status_HK1` auf 0 geht** (3/3). Damit bestimmt die Anforderung (Loxone/HK-Logik) die Laufdauer, nicht ein Hoval-Laufzeitzaehler.
- V99 (15 min Stehzeit): nicht verletzt, kuerzeste Pause 27 min (07:49:57 -> 08:18:32).

## Abtauungen / D-01-Gegenprobe
- **Keine Abtauung** seit 22.10. 00:55 - **belegt** doppelt: (a) `WW_Soll_eff` nie 100 (Skriptausgabe: `Marker WW_Soll_eff==100 Zeilen: []`); (b) X4 0xD001 springt waehrend keines Laufs auf `0000` und nie auf `2200` (Klassenwechsel-Liste unten; die kurzen `b7xx`-Werte 05:51-05:56, 10:28-10:30, 18:40-18:41 liegen mitten in WW-Laeufen bei laufendem Verdichter = normale Luefterstufe, kein 300-s-Nachlaufen nach Stopp).
- **Warum keine:** Aussen waehrend aller Laeufe >= 6,4 C (Abtauungen bisher nur bei 2,2-2,3 C im Heizbetrieb bzw. 1x bei 9,6 C in WW-Ladung 28.09.), und in der eigentlich kalten Phase (ab 19 Uhr, 6,4 -> 3,8 C) **lief der Verdichter gar nicht**.
- **Was der Tag fuer D-01 trotzdem hergibt (wahrscheinlich):** ~286 min Verdichterlaufzeit an einem Tag (davon 96 min am Stueck, WW, Mod bis 78 %) bei 6,4-10,7 C ohne Abtauung. Eine **rein zeitgesteuerte Abtauung nach 30 min kumulierter Laufzeit (CL005 als Ausloeser) ist damit ausgeschlossen**; 30 min kann hoechstens eine Mindestzeit zwischen zwei Abtauungen sein, ausgeloest wird ueber Verdampfer-/Bedarfsbedingung. Deckt sich mit der Abtau-Analyse 22.10. (13.10. 07:09 schon 8 min nach Start).
- Kumulierte Laufzeit seit der letzten echten Abtauung (13.10. 08:37): **nicht ermittelt** (ausserhalb des Auftrags-Zeitraums; Loop kann das aus ww_hires summieren).

## Heizstab
- **Nein.** P_el max 520 (= 5,20 kW) im WW-Lauf 05:48-06:37; kein Wert > 7,5 kW. - **belegt** (Skriptausgabe `P_el max gesamt: 520`). `WEZ_Leistung` = 1000 bei jedem Lauf ist die Leistungsfreigabe 100 %, kein Heizstab-Hinweis (Vermutung zur Bedeutung, Wert war bei allen frueheren Laeufen gleich).

## Beobachtung 09:56 - Luefter spaeter als Verdichter (Vermutung, offen)
- ww_hires: Mod 14 % ab 09:56:42, 42 % ab 09:57:12, 68-78 % ab 09:59:52. X4: 0xD001 = `0000` von 09:55:00 bis 10:00:04 (8 439 Schreibframes im Fenster, Bus also aktiv), `bbb6` ab 10:00:05.
- Kein Abtau-Muster (kein `2200`, kein `WW_Soll_eff` 10,0, Aussen 7,0 C). Moeglich: Luefter-Anlaufverzoegerung bei WW-Start nach langer Pause (82 min), oder 0xD001 ist nicht der einzige Luefterweg. **Nur Vermutung** - an den anderen 6 Starts heute kam der Luefter 0-20 s nach bzw. vor Mod > 0.

## Was bringt uns das
- Takt ist unkritisch: 7 Starts/Tag, keine Pause < 27 min, kein Lauf < 16 min, kein Heizstab, keine Stoerung. **An der Hoval nichts aendern.**
- Die Heizlaufdauer wird von der Anforderung (`Status_HK1`) bestimmt. Wer kuerzere/laengere Heizlaeufe will, muss an der Loxone-/HK-Anforderung drehen, nicht an Hoval-Parametern.
- Dass der Verdichter bei 3,8-6,4 C sechs Stunden ohne Heizanforderung steht, ist fuer Effizienz und Abtauung gut (keine Abtauung bei kalter Nacht = kein Waermeentzug aus dem Estrich). Ob die Raeume dabei warm genug bleiben, zeigt dieses Log nicht (Loxone-Raumtemperaturen pruefen, v. a. UG mit Holzofen).
- **Vorschlag (nur Vorschlag, der Betreiber entscheidet):** Wenn die naechsten kalten Naechte zeigen, dass der Estrich morgens auskuehlt und die WP dann bei der kaeltesten Aussentemperatur (04-07 Uhr) lange laufen muss, waere eine Loxone-Freigabe "Heizen bevorzugt am spaeten Abend/Nachmittag, solange Aussen > 5 C" sinnvoll - waermere Luft, bessere COP, weniger Abtaurisiko. Keine Aenderung an Hoval-Parametern.
- Fuer die Gegenproben (D-01, V101) brauchen wir einen Lauf bei Aussen < 3 C bzw. einen Kurzlauf - beides kam heute nicht vor.

## Offen fuer den Loop (nur lesend)
1. Naechster Heizlauf bei Aussen < 3 C: X4 0xD001-Klassenwechsel (Befehl unten) nach `0000` waehrend Lauf -> `2200` -> `b7xx` 300 s absuchen; Laufzeit seit Start und seit letzter Abtauung (13.10. 08:37) aus ww_hires summieren -> D-01.
2. Naechster Lauf < 10 min: Ende in X4 sekundengenau, `Status_HK1` im selben Fenster -> V101.
3. 09:56-Effekt: an weiteren WW-Starts nach > 60 min Pause pruefen, ob 0xD001 erst 3-4 min nach Mod > 0 kommt.
4. Warum `Status_HK1` = 0 ab 18:59 die ganze Nacht? Loxone-Anforderung/Raumtemperaturen (nicht aus Pi-Logs ermittelbar).

## Befehle zum Wiederfinden (PowerShell auf Windows-PC, nur lesend)
- Ende Lauf 4 (Anforderung weg): `py -3 ...\hoxpi_ssh.py "grep -E '^2026-10-22 08:3[34]:5' ~/hoxpi_fulllog/ww_hires.csv"`
- X4 Luefter-Klassenwechsel: `py -3 ...\hoxpi_ssh.py "zcat -f ~/x4_sniff/x4_2026-10-22.log.gz ~/x4_sniff/x4_2026-10-23.log | grep ' 06 06 d0 01 ' | awk '{v=$6$7; c=4; if(v~/^0000/)c=0; else if(v~/^2200/)c=2; else if(v~/^b7/)c=7; if(c!=p){print $1, c, v; p=c}}'"` (in PowerShell `$` als `` `$ `` schreiben)