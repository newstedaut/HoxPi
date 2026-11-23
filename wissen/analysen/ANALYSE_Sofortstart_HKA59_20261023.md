# Sofortstart trotz HKA59 = 15 min (F17, 23.10.2026)
Analyse-Agent 23.10.2026 ~22:30 · nur lesend (keine Schreibzugriffe auf Anlage, Busse, Kälteregler) · Katalogfrage F17.
Vorlauf: `[lokaler Pfad]` (F5), `ANALYSE_Startverzug_Ursache_Sperrzeit_20261023.md`, `ANALYSE_Loxone_MinHr40_Startverzug_20261023.md`.

**Frage:** Warum starten manche Heizanforderungen sofort (Freigabe 0,4–1,0 min nach Anforderung, RL ≤ 29,5 °C), obwohl HKA59 (33-055) = 15 min? Läuft HKA59 nach Abtauung oder Reset neu?

## Ergebnis in 3 Zeilen
1. **Der HKA59-Timer läuft auch ohne Anforderung.** Er vergleicht den WP-Rücklauf (FARL) mit dem **zuletzt gültigen Heiz-Soll** (1520 des letzten Heizblocks, in der Pause gehalten) − 1,5 K. Eine WW-Ladung setzt ihn zurück. Hat die Bedingung bei der Anforderung schon ≥ 15 min gehalten und ist der letzte Stopp ≥ 15 min her, kommt die Freigabe sofort. Das gilt für **7/7 Sofortstarts** (Bedingung 61 min bis 5,7 h vorher erfüllt) und für **17/17 verzögerte Starts**. Sicherheit: **wahrscheinlich**.
2. **Ohne Ausnahme gilt das nur, wenn der Stopp ≥ 15 min her ist:** 11/11 Fälle, davon 6 sofort und 5 verzögert. Bei Anforderung innerhalb von 15 min nach einem Stopp gibt es 2 Gegenbeispiele in entgegengesetzter Richtung: 16.10. 13:18 (11,4 min **später** als vorhergesagt) und 23.10. 18:05 (9,2 min **früher**). Gesamt 24/26. Damit ist die Regel **nicht ausnahmslos bestätigt**.
3. **Nach Abtauung läuft HKA59 nicht neu** (**sicher**, Messung, n = 2, 13.10.): Wiederanlauf jeweils 5,3 min nach Abtau-Ende, die Heizanforderung blieb dabei bestehen. Für HKA59 nach Reset gibt es keinen Heizfall: der Reset am 18.10. war ein WW-Neustart nach 2,0 min. Ein Strom-Aus fällt nicht ins Fenster.

## Was bringt uns das
- **Die Sofortstarts sind kein Zufall und kein Fehler.** Sie kommen, wenn das Wasser in der Pause kalt genug geworden ist: FARL ≤ letzter Heiz-Soll − 1,5 K, und das über 15 min. Der 15-min-Leerlauf der Pumpe (Status 0/51 ohne Verdichter) fällt nur an, wenn:
  - vorher WW geladen wurde: dann immer ~19–22 min, 10/10;
  - der Rücklauf bei der Anforderung noch warm war: 5 Fälle mit 16–21 min;
  - Loxone nach einem kurzen Stopp gleich wieder anfordert.
- **Loxone kann den Start vorhersagen** (ohne Hoval-Eingriff): Freigabe ≈ max(Anforderung, Stopp + 15 min, Beginn „FARL ≤ S_letzt − 1,5 K“ + 15 min) + 0,3–0,8 min. **S_letzt** ist das letzte 1520 im Heizbetrieb, nach einer WW-Ladung zählt die Bedingung neu ab Ende der Ladung. Damit lässt sich die Mindestlaufzeit (MinHr) in Loxone ab dem echten Verdichterstart messen statt ab der Anforderung. Monoflop: https://www.loxone.com/dede/kb/monoflop/
- **Hebel ohne Hoval-Eingriff (Vermutung, nicht getestet):** Eine Heizanforderung, die kurz nach einer WW-Ladung kommt, wartet immer ~20 min. Lässt Loxone nach der WW-Ladung erst ≥ 15 min Abkühlpause (FARL unter S − 1,5 K) und fordert dann an, startet die WP sofort, ohne die ~15 min Pumpenlauf vorher. Das wäre zuerst als Beobachtung zu prüfen, Loxone bleibt unverändert.
- **Korrektur an F5:**
  - Der Fall 18.10. 07:01 war **kein** Heiz-Sofortstart, sondern ein WW-Start: HK1 → 6, 1520 = 56,0.
  - Der Fall F5-#26 (hier #25, 23.10. 18:05) widerspricht der F5-Formel selbst. Vorhergesagt war 18:20:54, gemessen 18:11:44. F5 hatte ihn als „WP011 begrenzt“ einsortiert.

## Tabelle: alle Heizanforderungen 16.–23.10. (X26-ZUSTAND, ~5 s)
Spaltenbedeutung:
- **vorher:** 0 = Ruhe, 6 = Anforderung schließt direkt an eine WW-Ladung an.
- **S:** Heiz-Soll 1520 des Blocks. **S_letzt:** zuletzt gültiger Heiz-Soll vor der Anforderung.
- **Bed. seit:** Beginn von „FARL ≤ S(t) − 1,5 K“, ununterbrochen bis zur Freigabe. In der Pause gilt S_letzt, eine WW-Ladung unterbricht.
- **Vorh.:** Vorhersage = max(Anf., Stopp + 15, Bed. + 15). **Δ** = Freigabe − Vorhersage.
- **(a)** = Hypothese a erfüllt (Δ zwischen −1,0 und +1,5 min).

| # | Anforderung | vorher | letzter Stopp | Stopp→Anf min | S / S_letzt °C | FARL@Anf | Bed. seit | Bed.→Anf min | Freigabe | Anf→Frg min | Vorh. | Δ min | Klasse | (a) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 16.10. 05:48:48 | 0 | 15.10. ~22:03 (WW) | ~465 | 34,5 / 37,0 | 28,5 | 16.10. 00:03:52 | 344,9 | 05:49:24 | 0,6 | 05:48:48 | +0,6 | **sofort** | ja |
| 2 | 16.10. 06:43:52 | 6 | 06:43:27 | 0,4 | 40,0 / 34,5 | 54,0 | 06:47:41 | −3,8 | 07:02:53 | 19,0 | 07:02:41 | +0,2 | nach WW | ja |
| 3 | 16.10. 12:43:51 | 6 | 12:43:20 | 0,5 | 38,5 / 40,0 | 59,0 | 12:47:30 | −3,6 | 13:02:56 | 19,1 | 13:02:30 | +0,4 | nach WW | ja |
| 4 | 16.10. 13:18:28 | 0 | 13:07:56 | 10,5 | 38,5 / 38,5 | 30,5 | 12:47:30 | 31,0 | 13:34:21 | 15,9 | 13:22:56 | **+11,4** | Stopp < 15, Vorlauf nur 4,9 min | **nein** |
| 5 | 16.10. 14:48:34 | 0 | 13:59:07 | 49,5 | 38,0 / 38,0 | 26,5 | 12:47:30 | 121,1 | 14:49:00 | 0,4 | 14:48:34 | +0,4 | **sofort** | ja |
| 6 | 16.10. 16:30:00 | 6 | 16:29:29 | 0,5 | 37,0 / 38,0 | 59,0 | 16:53:02 | −23,0 | 17:08:07 | 38,1 | 17:08:02 | +0,1 | nach WW | ja |
| 7 | 17.10. 08:25:08 | 0 | 07:16:41 (WW) | 68,5 | 34,5 / 30,0 | 35,0 | 08:26:29 | −1,4 | 08:41:34 | 16,4 | 08:41:29 | +0,1 | verzögert | ja |
| 8 | 17.10. 09:15:46 | 0 | 09:05:45 | 10,0 | 33,5…34,0 / 34,5 | 31,5 | 09:43:22 | −27,6 | 09:58:54 | 43,1 | 09:58:24 | +0,5 | verzögert, Stopp < 15 | ja (nur mit zeitvariablem S) |
| 9 | 17.10. 17:41:06 | 0 | 14:49:21 (WW) | 171,8 | 37,5 / 33,5 | 38,5 | 17:41:57 | −0,8 | 17:57:30 | 16,4 | 17:56:57 | +0,6 | verzögert | ja |
| 10 | 18.10. 07:31:39 | 6 | 07:31:08 | 0,5 | 33,0 / 30,0 | 51,5 | 07:36:02 | −4,4 | 07:51:19 | 19,7 | 07:51:02 | +0,3 | nach WW | ja |
| 11 | 18.10. 14:19:31 | 0 | 11:48:47 (WW) | 150,7 | 38,0 / 33,0 | 35,5 | 14:19:31 | 0,0 | 14:35:22 | 15,8 | 14:34:31 | +0,8 | verzögert | ja |
| 12 | 18.10. 18:02:47 | 6 | 18:02:21 | 0,4 | 38,0 / 38,0 | 59,0 | 18:06:40 | −3,9 | 18:22:04 | 19,3 | 18:21:40 | +0,4 | nach WW | ja |
| 13 | 19.10. 06:56:03 | 6 | 06:55:58 | 0,1 | 33,5 / 30,0 | 54,0 | 07:00:26 | −4,4 | 07:15:44 | 19,7 | 07:15:26 | +0,3 | nach WW | ja |
| 14 | 19.10. 09:13:26 | 0 | 07:36:21 | 97,1 | 33,5 / 33,5 | 23,5 | 07:00:26 | 133,0 | 09:14:07 | 0,7 | 09:13:26 | +0,7 | **sofort** | ja |
| 15 | 20.10. 06:59:38 | 6 | 06:59:18 | 0,3 | 34,0 / 38,5 | 52,0 | 07:03:36 | −4,0 | 07:18:37 | 19,0 | 07:18:36 | 0,0 | nach WW | ja |
| 16 | 21.10. 15:24:20 | 0 | 07:05:43 (WW) | 498,6 | 32,0 / 38,5 | 28,5 | 08:32:04 | 412,3 | 15:24:45 | 0,4 | 15:24:20 | +0,4 | **sofort** | ja |
| 17 | 21.10. 17:08:29 | 6 | 17:08:08 | 0,3 | 32,0 / 32,0 | 51,5 | 17:12:57 | −4,5 | 17:27:45 | 19,3 | 17:27:57 | −0,2 | nach WW | ja |
| 18 | 22.10. 04:21:10 | 0 | 21.10. 20:50:32 (WW) | 450,6 | 34,5 / 32,0 | 29,0 | 02:45:19 | 95,8 | 04:21:45 | 0,6 | 04:21:10 | +0,6 | **sofort** | ja |
| 19 | 22.10. 07:01:16 | 0 | 06:37:06 (WW) | 24,2 | 34,5 / 34,5 | 35,0 | 07:06:05 | −4,8 | 07:21:32 | 20,3 | 07:21:05 | +0,5 | verzögert | ja |
| 20 | 22.10. 07:52:30 | 0 | 07:50:03 | 2,5 | 34,5 / 34,5 | 36,0 | 08:03:07 | −10,6 | 08:18:14 | 25,7 | 08:18:07 | +0,1 | verzögert, Stopp < 15 | ja |
| 21 | 23.10. 03:00:36 | 0 | 22.10. 18:59:17 (WW) | 481,3 | 36,0 / 34,5 | 27,5 | 22.10. 22:01:12 | 299,4 | 03:01:06 | 0,5 | 03:00:36 | +0,5 | **sofort** | ja |
| 22 | 23.10. 05:18:00 | 6 | 05:18:00 | 0,0 | 36,0 / 36,0 | 53,0 | 05:22:25 | −4,4 | 05:37:47 | 19,8 | 05:37:25 | +0,4 | nach WW | ja |
| 23 | 23.10. 07:45:41 | 6 | 07:45:21 | 0,3 | 36,0 / 36,0 | 50,5 | 07:52:11 | −6,5 | 08:07:24 | 21,7 | 08:07:11 | +0,2 | nach WW | ja |
| 24 | 23.10. 17:15:53 | 0 | 16:42:09 (WW) | 33,7 | 33,0 / 39,0 | 33,0 | 17:22:13 | −6,3 | 17:36:50 | 20,9 | 17:37:13 | −0,4 | verzögert | ja |
| 25 | 23.10. 18:05:54 | 0 | 17:56:22 | 9,5 | 39,5 / 33,0 | 33,0 | 18:05:54 | 0,0 | 18:11:44 | 5,8 | 18:20:54 | **−9,2** | Stopp < 15, Freigabe = Stopp + 15,4 | **nein** |
| 26 | 23.10. 19:06:44 | 0 | 18:52:29 | 14,2 | 39,0 / 39,5 | 29,5 | 18:05:54 | 60,8 | 19:07:45 | 1,0 | 19:07:29 | +0,3 | **sofort** (WP011 bindet) | ja |

Hinweise zur Tabelle:
- **S_letzt** ist der erste 1520-Wert des vorigen Heizblocks. Mit dem letzten Wert des Blocks weicht er um bis zu 0,5 K ab, bei keinem Fall ändert das das Urteil (a).
- **#1:** S_letzt = 37,0 °C ist das letzte Heiz-1520 vom 15.10. 18:20 (Volllogger `~/hoxpi_fulllog/2026-10-15.csv.gz`). Danach lief bis 22:03 WW.
- **#21:** S_letzt = 34,5 °C, das letzte echte Heiz-Soll vom 22.10. 07:52. Der Block 22.10. 13:51 mit 1520 = 61 war eine WW-Ladung und zählt nicht. Die automatische Latch-Logik im Skript hatte dort 61 übernommen.

Nicht als Heizstart gewertet:

| Anforderung | Was passiert ist | Warum nicht gewertet |
|---|---|---|
| 18.10. 07:01:16 | Freigabe nach 0,5 min, aber HK1 → 6 und 1520 = 56,0 (07:05) | WW-Start. In F5 fälschlich als Heiz-Sofortstart #10 gezählt |
| 19.10. 13:57:40, 22.10. 13:14:27 | Freigabe nach 0,8 bzw. 0,4 min, dann Status 4 und HK1 = 6 | WW-Starts. WW kennt kein HKA59 |
| 19.10. 18:56:39 | ging in einen WW-Start über | – |
| 20.10. 12:19:23 | Daten 12:25–17:05 eingefroren | – |
| 16.10. 20:02:21, 17.10. 20:11:12, 18.10. 20:32:25 (S = 30,0, 1490 = 24,0) | **keine Heiz-Freigabe**. FARL lag vorher 73–89 min unter S − 1,5 K = 28,5, stieg aber mit dem Pumpenlauf in 0,6–1,4 min über 28,5 und blieb darüber. 17.10. erst 21:45:55 ein WW-Start | passt zur Regel: die Bedingung muss noch gelten, wenn die Anforderung beim Kälteregler ankommt (Freigabe sonst nach 0,4–0,7 min). Wahrscheinlich |

## Prüfung der drei Hypothesen
| Hypothese | Ergebnis | Belege | Sicherheit |
|---|---|---|---|
| **(a)** Bedingung „RL ≤ Soll − 1,5 K“ war ≥ 15 min vor der Anforderung erfüllt, der Timer läuft unabhängig von der Anforderung | **bestätigt, mit 2 Ausnahmen.** Alle 7 Sofortstarts hatten die Bedingung 60,8–412 min (#1: 345 min) vorher erfüllt. Gemessen wird gegen S_letzt (letzter Heiz-Soll), WW setzt zurück. Kein verzögerter Start hatte die Bedingung ≥ 15 min vor der Anforderung, außer #4. Gesamt 24/26, Δ −0,4…+0,8 min. Bei Stopp ≥ 15 min vorher: 11/11 ohne Ausnahme | Tabelle oben; `Emulation\or_f17_20261023_11.out` | **wahrscheinlich**. Die Messung ist sicher, die Ursache im Kälteregler-Code ist nicht gelesen |
| Variante „Timer startet erst mit der Anforderung“ (F5-Lesart) | **widerlegt.** Damit wäre kein einziger Sofortstart möglich. Reset bei Anforderungsbeginn ergibt 14/32 | `or_f17_20261023_6.py` | sicher |
| Variante „Hysterese: Bedarf erst aus bei FARL ≥ S + A“ (A = 1…3 K) | **schlechter**, 19–20 von 26 | `or_f17_20261023_10.out` | sicher (als Datenfit) |
| Variante „Sofort bei großem Defizit S − FARL ≥ X“ | **widerlegt.** #11 (18.10. 14:19) hatte nach 0,8 min ein Defizit ≥ 5 K und wartete trotzdem 15,8 min. #16 startete sofort mit nur 3,5 K Defizit | `or_f17_20261023_5.out` | sicher |
| **(b)** Timer startet nach Abtauung / Reset / Strom-Aus neu oder entfällt | **Abtauung: läuft nicht neu** (2/2, Abschnitt unten). Reset und Strom-Aus: kein Heizfall im Fenster | 13.10. X26 | Abtauung sicher (n = 2), Reset/Strom-Aus offen |
| **(c)** Sofortstart nur, wenn der Stopp > 15 min her ist | **notwendig, aber nicht hinreichend.** Keine Freigabe vor Stopp + 15 min in 26/26 (knappster Fall #26 mit +0,3). Aber 5 Gegenbeispiele mit langer Pause und trotzdem ~16–21 min Wartezeit: #7 (68,5 min), #9 (171,8), #11 (150,7), #19 (24,2), #24 (33,7) | Tabelle | sicher |

**Die zwei Ausnahmen (offen):**
- **#4, 16.10. 13:18:28:** Bedingung seit 12:47:30, Stopp 13:07:56. Vorhergesagt 13:22:56 (WP011-Ende), gemessen 13:34:21 (Anf. + 15,9).
  - Vorher lief nur ein 4,9-min-Heizlauf nach WW (13:03:01–13:07:56).
  - Auffällig: Start-zu-Start 13:03:01 → 13:34:21 = **31,3 min ist der kleinste Abstand aller 63 Starts** 16.–23.10. Der nächste ist #25 mit 34,5 min. Ein Mindestabstand ~30 min zwischen zwei Starts würde #4 erklären (Vorhersage dann 13:33:01, Δ +1,3) und keinem anderen Fall widersprechen. Das ist eine **Vermutung**: n = 1, Parameter nicht gefunden (WP010 = 5 min Mindestlaufzeit, WP011 = 15 min Mindeststehzeit).
- **#25, 23.10. 18:05:54:** Vorher 19,5-min-Heizlauf mit S = 33,0, FARL nach dem Stopp 33–36 °C, also über 31,5. Danach hätte HKA59 erst ab der Anforderung zählen dürfen (Vorhersage 18:20:54). Die Freigabe kam aber schon 18:11:44 = **Stopp + 15,4 min**.
  - Mit dem, was HoxPi und X26-ZUSTAND zeigen, nicht erklärbar. Der eigentliche Soll im X26-Datenpunkt 0 ist nicht dekodiert.
  - **Vermutung:** Der Kälteregler hält nach einem Lauf, der durch Entzug der Anforderung endete, seinen letzten Freigabezustand. Das widerspricht aber #4.

## Abtauung und Reset
In den X26-ZUSTAND-Zeilen 16.–23.10. kommen nur die Status 0, 1, 4 und 51 vor, es gibt also keine Abtauung (8) und keine Sperre (16). Status 8 findet sich im Zeitraum 01.–15.10. nur am 13.10. (131 Zeilen). Status 16 gibt es am 03., 07. und 13.10. Zählung: `Emulation\or_f17_20261023_12.py`.

| Ereignis | Ablauf (X26 ZUSTAND) | Dauer bis Wiederanlauf | Aussage | Sicherheit |
|---|---|---|---|---|
| Abtauung 1, 13.10. | Heizlauf, HK1 = 23 durchgehend. 07:09:00 Stopp → 07:10:06 Start in Abtauung → Status 8 bis 07:15:31 → Status 16 bis 07:20:41 → 51 → Verdichter 07:20:52 | **5,3 min** nach Abtau-Ende, 1,1 min vom Stopp bis zum Abtaustart | HKA59 läuft **nicht** neu (sonst ≥ 15 min). Statt WP011 gilt eine Sperre von ~5 min (Status 16) | sicher (Messung) |
| Abtauung 2, 13.10. | 08:37:17 Stopp → 08:38:13 Start → Status 8 bis 08:43:39 → Status 16 → Verdichter 08:49:00 | **5,35 min** | wie oben | sicher (Messung), n = 2 |
| Reset, 18.10. (Fehler 222 laut F5) | WW-Lauf (Status 4) 11:11:49 Stopp → 11:13:51 wieder WW-Start | 2,0 min | WP011 entfällt nach Reset (wie in F5). Zu HKA59 sagt der Fall nichts, weil es ein WW-Lauf war | WP011: sicher (n = 1); HKA59 nach Reset: **nicht belegt** |
| Strom-Aus | im Fenster keiner. Die kleinen Logs am 09./10.10. stammen vom Pi, nicht von der WP | – | – | offen |

Hinweis: Fehler nach Strom-Aus/Ein nicht überbewerten (Projektregel). Für HKA59 nach einem Reset im Heizbetrieb muss erst ein Fall abgewartet werden.

## Methode und Pfade
Daten:
- X26-Sniffer `~/rs485_sniff/log/rs485_2026-10-16…23.log(.gz)`, Zeilen `### ZUSTAND` (alle 5 s).
  - Erzeugt von `~/rs485_sniff/rs485_marker.py` aus dem HoxPi-Exporter `127.0.0.1:9101`, also **Modbus-Werte, bis 60 s alt**, nicht X26-Telegramme.
  - Felder: status = WP-Detailstatus, FARL = `hoval_fa_ruecklauf_c`, HK1 = Modbus 1501.
  - Lokale Auszüge (aus F5): `[lokaler Pfad]`.
  - Neu: `Emulation\or_f17_20261023_x26z_13_0630-1030.txt` (Abtauung).
- Volllogger (5 min), Soll 1520 / 1490 / 1501 / 1529:
  - `Emulation\or_ag1_2026-10-16…22.csv(.gz)` und `or_f5_20261023_vl23.csv`;
  - für den 15.10. `~/hoxpi_fulllog/2026-10-15.csv.gz` direkt auf dem Pi gelesen.

Skripte und Ausgaben, alle nur lesend:
- `or_f17_20261023_1.py`: Verlauf um eine Anforderung.
- `_2.py`: Einlesen in `or_f17_20261023_R.pkl`.
- `_3.py/.out`: Vorgeschichte FARL.
- `_4.py/.out`: 1490/1520/1529 um jede Anforderung.
- `_5.py/.out`: Defizit-Modell.
- `_6.py/.out`: Reset-Varianten.
- `_7.py/.out`: Start-zu-Start-Abstände.
- `_8.py/.out`: Endmodell mit Block-Soll, plus `_8_dk10.out` für 1,0 K.
- `_10.py/.out`: Hysterese.
- **`_11.py/.out`**: Endmodell mit zeitvariablem Soll. Daraus stammt die Tabelle.
- `_12.py`: Statuszählung 01.–15.10.
- `_13.py/.out`: Abtauungen 13.10.

Alle Dateien liegen unter `[lokaler Pfad]`.

Definitionen:
- **Anforderung:** HK1 springt von 0 oder 6 auf 23.
- **Freigabe:** erster Status 51 oder 1, oder mod% > 0.
- **Stopp:** mod% > 0 → 0.
- **Bedingung:** FARL ≤ S(t) − 1,5 K.
  - S(t) im Heizblock ist der letzte Volllogger-Wert 1520 ≤ t, davor der erste Wert im Block.
  - In der Pause gilt der zuletzt gültige Heiz-Soll. WW (HK1 = 6 oder Status 4) unterbricht die Bedingung.
- **Toleranz:** Δ zwischen −1,0 und +1,5 min, wegen der Modbus-Alterung und des Pumpenvorlaufs (Status 51).
- Mit 1,0 K statt 1,5 K und konstantem Block-Soll passen 21/26 (`_8_dk10.out`), die 1,5 K aus F5 bleiben also.

## Lücken
- **Welchen Soll der Kälteregler in der Pause wirklich benutzt, ist nicht direkt gemessen.** Die TopTronic zeigt in der Pause 1520 = 0. S_letzt ist aus dem Datenfit erschlossen. Prüfen ließe sich das am X26-Datenpunkt 0 (Heiz-Soll an den Kälteregler) in den Roh-Telegrammen. Der Decoder dafür fehlt, nur passiv lesen.
- **Die zwei Ausnahmen #4 und #25 sind ungeklärt.** Die Vermutung „Mindestabstand ~30 min zwischen zwei Starts“ für #4 beruht auf n = 1, ein Parameter dafür wurde nicht gesucht (keine Firmware-Prüfung, laut Auftrag).
- **Zeitauflösung:** Die ZUSTAND-Werte sind Modbus-Werte, bis 60 s alt. FARL ist auf 0,5 K gestuft, S auf 5 min. Bei Grenzfällen um S − 1,5 K, etwa #8, entscheidet das den Fit: mit konstantem Block-Soll +9,4 min, mit zeitvariablem +0,5 min.
- **Die 1,5 K Schwelle statt der eingestellten 1,0 K (33-054)** bleibt wie in F5 unerklärt. Vermutung: anderer Fühler oder Soll-Versatz im Kälteregler.
- **HKA59 nach Reset und nach Strom-Aus:** kein Heizfall vorhanden.
- **Abtauung:** nur 13.10. mit 2 Fällen, beide mitten in einem Heizlauf. Ein Fall „Anforderung kommt kurz nach einer Abtauung“ fehlt.

## Fertig, wenn …?
| Kriterium | Stand |
|---|---|
| Regel für Sofortstart benannt | **ja**: „HKA59 zählt unabhängig von der Anforderung gegen den letzten Heiz-Soll, WW setzt zurück; Bedingung ≥ 15 min erfüllt und Stopp ≥ 15 min her → Freigabe sofort“ |
| Bestätigung an ≥ 5 Fällen (sofort + verzögert) ohne Ausnahme | **teilweise**. Ohne Ausnahme bei Stopp ≥ 15 min vorher: 11/11, davon 6 sofort und 5 verzögert. Über alle 26 Heizstarts: 24/26, Ausnahmen #4 und #25 (beide Stopp < 15 min) |
| Abtau-Fall belegt | **ja**, 2× am 13.10.: HKA59 läuft nicht neu, Wiederanlauf nach 5,3 min |
| Reset-Fall belegt | **teilweise**: Reset 18.10. hebt WP011 auf (2,0 min), aber im WW-Betrieb, also ohne Aussage zu HKA59 |

## Rohdaten-Stichprobe zum Gegenprüfen (Sofortstart #5, 16.10.)
- Volllogger: am 16.10. um 13:55 steht 1520 = 380 (S_letzt = 38,0, Schwelle 36,5), von 14:00 bis 14:45 steht 1520 = 0.
- X26: ab 14:03:21 FARL = 34,5 und weiter fallend bei HK1 = 0. Um 14:48:34 HK1 = 23 mit FARL = 26,5. Um 14:49:00 status = 51, um 14:49:20 mod% = 14.
- Befehl, nur lesend, auf Windows-PC in PowerShell:
  `Select-String -Path [lokaler Pfad] -Pattern '^14:03:21|^14:48:34|^14:49:00|^14:49:20'`


## Nachtrag Orchestrator 24.10.2026 ~04:00 — Ausnahme #4: "Mindestabstand ~30 min Start-zu-Start" widerlegt
**Frage:** Erklärt ein Mindestabstand von ~30 min zwischen zwei Verdichterstarts die Ausnahme #4 (16.10. 13:18, +11,4 min)?
**Daten:** alle X26-ZUSTAND-Statuswechsel 25.09. 00:00 – 24.10. 03:54 (`~/rs485_sniff/log/rs485_2026-09-25 … 10-24`, nur gelesen), 197 Verdichterläufe (Status 1 oder 4).
Auszug `[lokaler Pfad]`, Skript `or_f17_20261024_0400.py`, Ausgabe `or_f17_20261024_0400.out`.

| Fall | Lauf 1 | Stopp | Start 2 | Start-zu-Start | Stopp→Start | dazwischen |
|---|---|---|---|---|---|---|
| 26.09. Heiz→Heiz | 06:55:41 (4,8 min, Pel ~2,0 kW) | 07:00:26 | 07:15:52 | **20,2 min** | 15,4 min | 0/51 |
| 26.09. Heiz→Heiz | 07:15:52 (5,1 min) | 07:20:58 | 07:37:01 | **21,1 min** | 16,1 min | 0/51 |
| 16.10. #4 | 13:03:11 (4,8 min) | 13:08:01 | 13:34:26 | 31,2 min | 26,4 min | 0 |
| 23.10. #25 | 17:37:21 (19,4 min) | 17:56:42 | 18:11:44 | 34,4 min | 15,0 min | 0 |

- **Ergebnis (sicher, Messung):** Zwei echte Heiz-Kurzläufe hintereinander am 26.09. (Verdichter lief, Pel 1,9–5,3 kW, mod% 42–95) mit nur 20–21 min Start-zu-Start. Einen Mindestabstand ~30 min gibt es nicht. Kleinster Abstand ohne Abtauung/Sperre über alle 191 Paare: 20,2 min = 5 min Mindestlaufzeit (V101) + 15 min Mindeststehzeit (WP011). Kleinstes Stopp→Start Heiz→Heiz ohne Abtauung: 15,0 min (n = 64).
- Die Vermutung aus dem Abschnitt „Die zwei Ausnahmen" zu #4 ist damit **gestrichen**; #4 und #25 bleiben **offen**. Gemeinsam ist beiden nur: Stopp < 15 min vor der Anforderung und dazwischen nur Status 0 (kein 51).
- **Neue Fälle 24.10. 00:00–03:54:** kein Statuswechsel, also kein Start (sicher).
- **Was bringt uns das:** Für die Startvorhersage in Loxone gilt weiter nur „Stopp + 15 min" und HKA59; eine zusätzliche 30-min-Sperre muss nicht eingeplant werden. Takt-Untergrenze der C17 = ~20 min Start-zu-Start (3 Starts/h möglich).


## Nachtrag Orchestrator 24.10.2026 ~21:00 - 4 neue verzoegerte Freigaben im Dauer-Anforderungsblock (Modell A+VL)
Daten: X26 `~/rs485_sniff/log/rs485_2026-10-24.log` bis 20:56 (nur gelesen, Parser `rs485_9600parse.py`), Ereignisliste `[lokaler Pfad]`; Skripte `or_f17_20261024_2100_c.py` / `_d.py`, Ausgaben `_c.out` / `_d.out`.

| Freigabe (B22 0->x) | S | RL | VL | Stopp vorher | Bedingung RL<=S-1,5 und VL<=S seit | Wartezeit | Abw. vom Modell (15 min) |
|---|---|---|---|---|---|---|---|
| 15:38:28 | 32,5 | 30,5 | 30,5 | 31,9 min | 15:24:22 | 14,1 min | -0,9 |
| 16:51:31 | 33,0 | 31,0 | 31,5 | 43,1 min | 16:36:17 | 15,2 min | +0,2 |
| 18:27:06 | 33,0 | 31,0 | 31,0 | 60,7 min | 18:10:16 | 16,8 min | +1,8 |
| 20:09:33 | 33,0 | 31,0 | 31,5 | 73,9 min | 19:53:10 | 16,4 min | +1,4 |

- **Ergebnis:** Alle vier passen zu A+VL (3 im Band -1/+1,5 min, 18:27 mit +1,8 knapp darueber). Die M0-Anforderung lief durchgehend <MAC>, die Starts kamen also allein ueber die RL-Bedingung + 15 min (sicher, Messung; Regel wahrscheinlich).
- Mit strengem "<" (B29 zeigt 31,0) laege die Wartezeit nur bei 4-6 min -> die Schwelle ist "<=" bzw. der interne Fuehler kreuzt S-1,5 kurz nach dem 0,5-K-Sprung von B29 (Vermutung; erklaert die spaete Tendenz und vielleicht #12).
- VL <= S war heute nie der begrenzende Teil (VL 0,5-2,0 K unter S).
- Stand: 34 von 35 Heizstarts 16.-24.10. passen (Ausreisser #12, 18:27 grenzwertig). Abtau-/Reset-Fall weiter offen.
- **Was bringt uns das:** Startvorhersage fuer Loxone bei Dauer-Anforderung: Start ~15-17 min, nachdem der WP-Ruecklauf (B29) auf Soll-1,5 K gefallen ist; Takt heute 25-35 min Lauf / 60-90 min Pause bei Soll 33 C.


## Nachtrag OR 24.10.2026 23:00 - zweiter Reset (19.09.)
- Strom-Aus/Ein 19.09. ~21:11 (Fehler 222, `ANALYSE_Datenqualitaet_Volllogger_Winter-AZ_20261023.md`): X26 ZUSTAND 20:30-23:59 = 2474 Zeilen, durchgehend status 0, HK1 0, mod 0 (AT 14,9 C) -> keine Heizanforderung, kein HKA59-Fall (**sicher**). Skript/Ausgabe `[lokaler Pfad]`, Rohzeilen `or_f17_20261024_2300_x26z_0919.txt`.
- Damit sind beide Resets im X26-Archiv (19.09., 18.10.) ohne Heizfall. HKA59 nach Reset bleibt offen, bis ein Reset/Strom-Aus waehrend HK1-Anforderung vorkommt. Katalog F17 -> `wartet`.