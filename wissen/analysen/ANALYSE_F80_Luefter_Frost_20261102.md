# F80 - Lüftergesetz bei Frostnähe und Lüfter bei Abtauung (Stand 02.11.2026 ca. 09:05)
**Kernaussage:** V25 ist 3/3 widerlegt (in der Karte schon seit 13.10.2026 widerlegt; Nachfolger V63 hält hier 3/3): der Lüfter steht nicht bis zum Abtauende, sondern läuft die letzten ~2 min mit festen 1,36 V. V26 ist formal noch nicht widerlegt (02.11.: genau 3 Punkte > 4 %-Punkte, Grenze ist "mehr als 3"), aber inhaltlich zu steil: unter ca. 4,5 °C außen liegt der Lüfter systematisch 0,2-0,5 V unter der Formel. Echter Frost (1477 < 2,9 °C) ist noch nicht gemessen.
## (a) V25: Lüfter in den 3 Abtauungen 02.11. (X4 s-genau, Status 8 nur 48-s-Raster)
| Abtauung | Run 1→0 | D001→0 | Run=1 (Abtaulauf) | Status 8 erste-letzte Probe | D001=0x2200 (1,36 V) | vor letzter Status-8-Probe | 0xB799 (7,34 V) ab | Nachlauf bis | Run neu |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 02:21:25 | 02:21:26 | 02:22:24 | <MAC> | <MAC> | 102 s | 02:27:27 | 02:32:28 (301 s) | 02:32:49 |
| 2 | 04:45:41 | 04:45:42 | 04:46:40 | <MAC> | <MAC> | 115 s | 04:51:59 | 04:56:59 (300 s) | 04:57:20 |
| 3 | 06:24:23 | 06:24:22 | 06:25:22 | <MAC> | <MAC> | 118 s | 06:31:07 | 06:36:07 (300 s) | 06:36:28 |

- **Teil 1 "binnen ≤ 10 s auf 0": gehalten 3/3** [sicher]. D001 ist bei der ersten Status-8-Probe schon 78-92 s lang 0.
- **Teil 2 "bleibt 0 bis Ende": widerlegt 3/3** [sicher]. D001 = 0x2200 ab 102-118 s vor der letzten Status-8-Probe.
- **V63 gehalten 3/3** [sicher]: Status 8 4,6-5,4 min (3-9), Teilwiederanlauf 1,7-2,0 min vor Ende (1-3) und < 0x4000, Nachlauf 300-301 s (4-6 min), Lüfter aus bis Neustart 11,4 / 11,6 / 12,1 min (10-15). Das schließt den Karten-Vermerk "Zeitlage nicht ausgewertet".
- **Abweichung vom V63-Wortlaut** [sicher, nur X4-Sicht]: D001 fällt innerhalb ±1 s mit Run (0x64) 1→0, nicht vorher. "Bei noch laufendem Verdichter" gibt der Run-Befehl nicht her; tatsächliche Drehzahl hier nicht geprüft.
- **Feste Werte** [sicher, 3/3]: 0x2200 und 0xB799 gleich bei allen drei, unabhängig von der Vorlage. 0x2200 kommt am 01./02.11. nur in Abtauungen vor; 0xB799 auch einmal im Normallauf (06:11:11).
## (b) Heizläufe bei Luft ≤ 3 °C (D001 ohne erste 120 s und ohne 0; Abw = D001 - V26 aus 5-min-Punkten, Median)
| Start | Dauer min | Art | Luft 0106 °C | Außen 1477 °C | 0x66 Median | D001 V Med / Min / Max | Abw V |
|---|---|---|---|---|---|---|---|
| 01. 02:31 | 12,1 | H | 2,2 | 5,0-5,1 | 840 | 7,02 / 7,01 / 7,16 | -0,05 |
| 01. 03:32 | 32,2 | H | 1,6-1,8 | 4,6-4,8 | 840 | 7,05 / 7,04 / 7,19 | -0,07 |
| 01. 05:09 | 87,1 | H+WW | 0,3-0,9 | 3,6-4,5 | 840 | 7,10 / 7,05 / 7,86 | -0,17 |
| 01. 06:58 | 31,4 | H | 0,5-0,7 | 3,5 | 840 | 7,09 / 7,07 / 7,23 | -0,20 |
| 01. 08:16 | 30,0 | H | 0,4-0,5 | 3,4 | 840 | 7,09 / 7,09 / 7,23 | -0,21 |
| 01. 10:20 | 35,6 | H | 1,2-1,4 | 4,4-4,8 | 840 | 7,06 / 7,05 / 7,21 | -0,06 |
| 01. 11:53 | 35,9 | H | 2,1-2,5 | 5,3-5,7 | 840 | 7,02 / 6,99 / 7,17 | +0,01 |
| 01. 15:31 | 36,6 | H | 2,5-2,8 | 5,5-5,8 | 840 | 6,98 / 6,96 / 7,12 | -0,01 |
| 01. 17:04 | 14,1 | H | 2,1-2,2 | 4,9-5,0 | 840 | 7,03 / 7,02 / 7,17 | -0,07 |
| 01. 20:11 | 5,0 | H | ~1,8-2,2 (Umfeld) | 4,4 | 1008 | 7,17 / 7,01 / 7,18 | -0,19 |
| 02. 02:13 | 8,2 | H | 1,0 | 3,6 | 1015 | 7,22 / 7,19 / 7,25 | -0,20 |
| 02. 02:32 | 85,6 | H | 0,2-1,5 | 3,0-3,6 | 840 | 7,10 / 7,07 / 7,20 | -0,23 |
| 02. 04:38 | 7,4 | H | 0,5 | 2,9 | 1007 | 7,23 / 7,10 / 7,24 | -0,28 |
| 02. 04:57 | 87,0 | H+WW | 0,3-0,6 | 3,0-3,1 | 960 | 7,20 / 7,09 / 7,87 | -0,27 |
| 02. 06:36 | 39,1 | H | 0,5-0,8 | 3,2 | 840 | 7,09 / 7,08 / 7,22 | -0,24 |
| 02. 08:08 | 39,5 | H | keine Probe | 3,0-3,4 | 840 | 7,07 / 7,06 / 7,22 | -0,25 |

Nicht in der Tabelle: 01. 00:54 (keine 0106-Probe), 01. 13:00 und 14:24 (Luft 3,0-3,4), die drei Abtauläufe.

**Modulationsboden (Mod 33-37), 5-min-Punkte:** Außen 5,5-6,5: 6,97 V, Abw +0,01 (n=24) | 4,5-5,5: 7,04 V, -0,06 (n=19) | 3,5-4,5: 7,09 V, -0,17 (n=19) | 2,5-3,5: 7,09 V, -0,24 (n=37).

- **V26 formal:** 129 Punkte, 126 innerhalb ±4 %-Punkte. 01.11.: 0 von 78 darüber; 02.11.: 3 von 51 (05:45, 05:50, 05:55, alle WW bei Mod 73-84, bis -0,52 V). Kriterium "mehr als 3 an einem Tag" nicht erfüllt, aber der Tag läuft noch (letzter Punkt 08:45) [sicher].
- **V26 inhaltlich:** Bei 4,5-6,2 °C hält die Formel (Abw ≤ 0,06 V am Boden) [sicher]. Darunter überschätzt sie, und die Abweichung wächst mit sinkender Außentemperatur; bei 3-4,5 °C bleibt der Boden auf 7,09 V stehen [sicher für die Messwerte; "Plateau" als Deutung wahrscheinlich].
- **Neufit nur für diesen Bereich:** Lüfter % = 66,8 + 0,163 × Mod - 0,45 × Außen (n=116, Außen 2,9-6,2, rms 0,21 %-Punkte, in-sample) [wahrscheinlich]. Passt nicht auf den Herbst (06.10., Mod 33 / 14 °C: 65,9 % statt gemessen 57,2 %), also ist der Verlauf über das ganze Jahr wohl nicht linear [wahrscheinlich].
- **Führungsgröße:** 1477 erklärt den Lüfter besser als Luft 0106 (rms 0,21 gegen 0,41) [wahrscheinlich]. Passt zur Karte (Sollwert kommt über X26 von der Regelung) [Vermutung]. Die Formel mit 0106 statt 1477 einzusetzen ist falsch (Abw bis -8,7 %-Punkte) [sicher].
- **0x66:** 0x66/24 = Modulation 18726 (Median-Abw 0, max 2,7) [sicher]; 0x66 und Modulation sind hier also dieselbe Information.
- **Obergrenze:** Maximum 01./02.11. 7,87 V (05:48:07, Mod 84), die in der Karte genannte 80-%-Schwelle wurde nicht erreicht [sicher].
## (c) Vorschlag V135 (nur Vorschlag, nicht in der Karte; Nummer vor Eintrag prüfen)
An einem Tag mit 1477 zwischen -5 und 0 °C gilt: (a) 5-min-Punkte am Boden (Mod 33-37, ohne Anlauf/Stopp/Status 8) liegen bei D001 **6,9-7,6 V**. V26 sagt dort 7,8-8,5 V. **Widerlegt**, wenn mehr als 3 Punkte eines Tages außerhalb liegen. (b) Abtauungen behalten 0x2200 (1,36 V) und 0xB799 (7,34 V, 300 ± 2 s). **Widerlegt** bei einem anderen Wert oder einer anderen Nachlaufdauer. Prüfung: `[lokaler Pfad]` (Daten-Dateien/Tage anpassen).
## Was bringt uns das
- Abtauungen sind am X4-Bus sekundengenau erkennbar: 0x2200 war in diesen 2 Tagen eindeutig [sicher für 01./02.11., sonst ungeprüft]. Das ist genauer als Status 8 im 48-s-Raster.
- Der Zwilling sollte für den Lüfter unter 4,5 °C nicht V26 nehmen, sondern den Bereichsfit, und ihn nicht nach unten extrapolieren.
- Kein Handlungsbedarf an der Anlage: Das Verhalten ist unauffällig, keine Grenze erreicht [wahrscheinlich].
## Offen
- Kein Punkt mit 1477 < 2,9 °C; "Frost" ist hier nur Luft 0106 bis 0,2 °C. Aussage für echten Frost: nicht ermittelbar.
- Nur 2 Tage, ein Wetterlagentyp. 0106 fehlt 01.11. 00:00-01:47 und 02.11. 07:25-08:59.
- Ausgewertet ist nur der D001-**Sollwert**; Ist-Drehzahl (Rückmeldung Slave 6) und Lüfterleistung nicht. Ob Reif den Lüfter vor der Abtauung sichtbar beeinflusst: nicht geprüft.
- 02.11. nur bis ca. 09:03; ein 4. Punkt > 4 %-Punkte heute würde V26 formal widerlegen.
## Quellen (nur lesend)
Pi: `/home/<user>/x4_sniff/x4_2026-11-01.log.gz`, `/home/<user>/x4_sniff/x4_2026-11-02.log`, `/home/<user>/hoxpi_fulllog/2026-11-01.csv`, `/home/<user>/hoxpi_fulllog/2026-11-02.csv`, `/home/<user>/verdichter_catch/runs/run_20261102_022244.csv`, `/home/<user>/verdichter_catch/runs/run_20261102_044714.csv`, `/home/<user>/verdichter_catch/runs/run_20261102_062549.csv`, `/home/<user>/rs485_sniff/log/rs485_2026-11-01.log.gz`, `/home/<user>/rs485_sniff/log/rs485_2026-11-02.log`, `/tmp/cc_frostlauf_20261102/`.
PC: `[lokaler Pfad]`; Skripte und Auszüge `[lokaler Pfad]` (Ergebnis `f80_ausw_out.txt`). CRC aller X4-Auszugszeilen geprüft: 0 Fehler.