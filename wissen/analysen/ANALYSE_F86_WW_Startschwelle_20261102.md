# ANALYSE F86 - Bei welcher Differenz fordert die Hoval eine WW-Ladung an? (02.11.2026)

Claude, Subagent, nur gelesen. An Anlage, Bussen, Loxone und Pi nichts geändert. Daten: `ww_hires.csv` bis 02.11. 11:57:51 (lokale Kopie), Stichprobe auf dem Pi bis 12:07:51, keine neue Ladung. Rohwerte /10.

## Ergebnis

1. **Regel: Anforderung, sobald der momentane Wert von `1500` (SF, oben) den aktuellen Sollwert `1499` um 5,0 K erreicht.** Reaktion auf einen Soll-Sprung binnen 10-11 s. [wahrscheinlich für genau 5,0 und für "momentan", siehe 3; sicher für die Klammer 4,9-5,0 an den Soll-Sprüngen]
2. **Maßgeblich ist `1499`, nicht `1497`.** Beide sind gleich, bis auf eine Ausnahme mit Folgen: Nach einer 57-°C-Ladung, die an der VL-Grenze endet, steht `1499` auf dem erreichten Ist (V8/V49). In dieser Zeit lag die Differenz zu `1497` 3,2 h lang bei ≥ 5,0 K ohne Anforderung, und drei Starts kamen bei `1497 - 1500` = 5,9/6,3/6,3 K, aber `1499 - 1500` = 4,8/4,9/4,8 K. [sicher]
3. **Warum die Fälle "4,7 ohne Start" (F84) und "Start bei 4,7" (F79) beide stimmen:** `1500` ist grob und unruhig. Der Wert springt im 0,1/0,2-K-Raster (es gibt kein 45,0, 45,4, 46,2 ...) und zittert im 10-s-Raster um 1-2 Stufen. Der Logger sieht vor einer Ladung nur jede Minute einen Wert. Die sichtbare Differenz beim Start ist deshalb 4,6-4,9 K (1 Fall 5,1), und eine echte Unterschreitung sieht man fast nie (siehe 2. in Belege). [sicher: Raster und Zählung; wahrscheinlich: Erklärung über Zittern]
4. **Sie ist fest und hängt nicht am Sollwert.** Die Verteilungen bei Soll 50, 52, 57 liegen im selben Band. Bei 57 kommen sichtbar 4,7er häufiger vor, vermutlich weil dort das Raster anders fällt: Von 52,3 sind es zwei Stufen bis 52,0 (52,1, 52,0), von 45,3 drei bis 44,9 (45,2, 45,1, 44,9). [sicher: Zählung; Vermutung: Rastergrund]
5. **Es schaltet SF (`1500`), nicht SF2 allein.** SF2 lag 214 h lang ≥ 5 K unter `1499` ohne Anforderung, davon 185 h mit `1500` noch über `1499` - 4,5; Minimum 16,5 °C am 27.10. 19:02:52. [sicher] Eine zusätzliche UND-Bedingung auf SF2 lässt sich nicht ausschließen, weil SF2 fast immer tiefer liegt. [Vermutung: gibt es nicht; nicht prüfbar]
6. **WP011 und laufender Verdichter verschieben die Anforderung nicht** (5 und 14 Fälle mit denselben Differenzen). Sie verschieben nur den Verdichterstart (F83). [sicher] Abtauung setzt `1499` auf 10,0, ab 01.10. kam dort keine Anforderung. Fehler, WP aus: kein Testfall, siehe Offen.
7. **Parameter: `05-000` "Einschaltdifferenz Warmwasserbereitung" (dp 5000), Bereich 0,5-20,0 K.** Live-Wert **nicht lesbar, nicht gefunden.** Die Messung passt zu 5,0 K. [sicher: Name und kein Register; wahrscheinlich: Wert 5,0]

### Formel und Trefferquote

```
Anforderung (1504 -> 1)  wenn  1500_momentan <= 1499 - 5,0 K
Für 1-min-Daten/Zwilling:      erster Wert 1500 <= 1499 - 4,9 K, Verzug 0-25 min (Median 0,8)
1499 = 1497, außer: VL-62-Abbruch bei 57 (1499 = Ist am Ladeende bis zum nächsten Loxone-Wechsel),
                    Abtauung (1499 = 10,0), bis 11.09. Zeitprogramm Woche 2 (1499 = 48/45)
```

| Prüfung (ab 01.10.) | Treffer | Ausnahmen |
|---|---|---|
| Soll-Sprung, D ≥ 4,9 K in der Sprungzeile -> Anforderung ≤ 20 s | **43 von 44** (mit September 62 von 64) | 28.10. 18:07:52 (Z. 104754) und 25.09. 00:15:53 (Z. 32007): `1497` zeigt 57 nur kurz, dann 52. Am 28.10. genau 1 Zeile, also kein gültiger Test. [sicher für 28.10., wahrscheinlich für 25.09.] |
| Soll-Sprung, D ≤ 4,8 K -> keine Anforderung ≤ 20 s | **57 von 57** (mit September 90 von 90) | keine |
| Ist-Absinken: sichtbares D in der letzten Zeile vor der Anforderung ≥ 4,7 K | **70 von 71** | 18.10. 17:23:01 (Z. 81850): 4,6 K, Ist 52,4/52,5 |
| Sichtbares D ≥ 5,0 K bei Status 0 länger als eine Zeile | **0 Fälle** (4 Episoden, zusammen 0,8 min; 3 enden in der Anforderung, die 4. ist Z. 57246, `1499` hängt nach Soll-Senkung nach) | keine |

## Belege

### 1. Alle 113 Anforderungen seit 01.10.

Quelle: `/home/<user>/hoxpi_fulllog/ww_hires.csv`, Spalte "Zeile" = Zeilennummer dort. Ladung = zusammenhängend `WW_Status` ≥ 1, Lücke ≤ 150 s (wie F79/F83). Anforderung = erste Zeile mit Status 1. "1500 davor" = letzte Zeile mit Status 0. Bei "Sprung" ist D = neuer `1497` - `1500` in der Sprungzeile, sonst D = `1499` - `1500 davor`. `1499` hinkt beim Sprung bis 60 s nach, der Regler nicht.

Klassen: **Ist** (67) = kein Sollwechsel in den 30 min davor; **Ist n. Sprung** (4) = Soll bis 30 min vorher angehoben, D blieb dabei unter 4,9, Ist fiel danach; **Sprung** (42) = Anhebung ≤ 6 min vorher, D ≥ 4,9. Fühlerquelle: siehe Spalte SF2 und Belege 5, in keiner Zeile spricht etwas für einen anderen Fühler als SF. SF2 17./18.10. steht auf 54,4/48,5 und ist vermutlich ein Standbild. [wahrscheinlich]

| # | Zeile | Anforderung | 1497 | 1499 davor | 1500 davor | 1500 bei Anf. | D [K] | SF2 | Klasse | Sprung | Verd. lief |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 43899 | 01.10. 13:51:11 | 57,0 | 57,0 | 52,1 | 52,1 | 4,9 | 50,1 | Ist | - | - |
| 2 | 45622 | 02.10. 16:35:53 | 57,0 | 50,0 | 46,7 | 46,8 | 10,3 | 19,9 | Sprung | 50,0>57,0 | - |
| 3 | 46270 | 02.10. 23:20:32 | 57,0 | 52,0 | 49,9 | 50,0 | 7,0 | 34,6 | Sprung | 52,0>57,0 | - |
| 4 | 47167 | 03.10. 10:47:31 | 57,0 | 52,0 | 49,9 | 49,9 | 7,1 | 38,4 | Sprung | 52,0>57,0 | - |
| 5 | 47502 | 03.10. 13:10:02 | 57,0 | 57,0 | 52,1 | 52,1 | 4,9 | 48,7 | Ist | - | - |
| 6 | 48469 | 04.10. 01:11:12 | 50,0 | 50,0 | 45,2 | 45,2 | 4,8 | 41,4 | Ist | - | - |
| 7 | 49199 | 04.10. 10:19:32 | 50,0 | 50,0 | 45,2 | 45,2 | 4,8 | 42,5 | Ist | - | - |
| 8 | 49465 | 04.10. 12:05:33 | 57,0 | 50,0 | 49,2 | 49,2 | 7,8 | 45,3 | Sprung | 50,0>57,0 | - |
| 9 | 50003 | 04.10. 16:48:32 | 57,0 | 55,9 | 51,1 | 51,0 | 4,8 | 41,8 | Ist | - | - |
| 10 | 50712 | 04.10. 22:21:41 | 50,0 | 50,0 | 45,1 | 44,9 | 4,9 | 26,9 | Ist | - | - |
| 11 | 51390 | 05.10. 06:00:32 | 52,0 | 52,0 | 47,2 | 47,2 | 4,8 | 42,7 | Ist | - | - |
| 12 | 51941 | 05.10. 11:44:51 | 57,0 | 50,0 | 45,6 | 45,7 | 11,4 | 38,8 | Sprung | 50,0>57,0 | - |
| 13 | 52369 | 05.10. 15:07:01 | 57,0 | 57,0 | 52,3 | 52,3 | 4,7 | 48,1 | Ist | - | - |
| 14 | 52865 | 05.10. 20:27:12 | 52,0 | 50,0 | 46,7 | 46,7 | 5,3 | 38,5 | Sprung | 50,0>52,0 | - |
| 15 | 53786 | 06.10. 06:09:52 | 52,0 | 52,0 | 47,2 | 47,1 | 4,8 | 40,9 | Ist | - | - |
| 16 | 54358 | 06.10. 11:45:12 | 57,0 | 50,0 | 48,0 | 47,9 | 9,1 | 45,4 | Sprung | 50,0>57,0 | - |
| 17 | 55288 | 06.10. 23:41:02 | 52,0 | 50,0 | 45,1 | 45,2 | 6,9 | 39,7 | Sprung | 50,0>52,0 | - |
| 18 | 55948 | 07.10. 06:37:41 | 52,0 | 52,0 | 47,2 | 47,2 | 4,8 | 46,2 | Ist | - | - |
| 19 | 56467 | 07.10. 12:12:32 | 50,0 | 50,0 | 45,1 | 44,9 | 4,9 | 40,9 | Ist | - | - |
| 20 | 57124 | 07.10. 17:43:41 | 57,0 | 55,6 | 50,7 | 50,8 | 4,9 | 49,3 | Ist | - | - |
| 21 | 57334 | 07.10. 19:27:02 | 57,0 | 50,0 | 49,1 | 49,2 | 7,8 | 39,8 | Sprung | 50,0>57,0 | - |
| 22 | 58133 | 08.10. 05:22:42 | 52,0 | 52,0 | 47,2 | 47,2 | 4,8 | 43,9 | Ist | - | - |
| 23 | 58499 | 08.10. 08:02:51 | 57,0 | 52,0 | 47,3 | 47,3 | 9,7 | 31,8 | Sprung | 52,0>57,0 | - |
| 24 | 59043 | 08.10. 12:36:51 | 57,0 | 50,0 | 51,8 | 51,8 | 5,2 | 49,5 | Sprung | 50,0>57,0 | - |
| 25 | 59486 | 08.10. 17:29:51 | 57,0 | 52,0 | 50,6 | 50,6 | 6,4 | 30,3 | Sprung | 52,0>57,0 | - |
| 26 | 60145 | 09.10. 00:22:11 | 50,0 | 50,0 | 45,2 | 45,2 | 4,8 | 42,5 | Ist | - | - |
| 27 | 60694 | 09.10. 06:42:52 | 52,0 | 52,0 | 47,2 | 47,3 | 4,8 | 44,9 | Ist | - | - |
| 28 | 61479 | 09.10. 15:57:01 | 57,0 | 50,0 | 45,9 | 45,7 | 11,1 | 42,5 | Sprung | 50,0>57,0 | - |
| 29 | 62259 | 10.10. 00:05:22 | 52,0 | 50,0 | 46,8 | 46,7 | 5,2 | 39,2 | Sprung | 50,0>52,0 | - |
| 30 | 63207 | 10.10. 11:44:12 | 50,0 | 50,0 | 45,1 | 45,1 | 4,9 | 42,7 | Ist | - | - |
| 31 | 63801 | 10.10. 17:04:52 | 50,0 | 50,0 | 45,1 | 45,1 | 4,9 | 43,3 | Ist | - | ja |
| 32 | 64638 | 11.10. 04:30:13 | 52,0 | 50,0 | 45,9 | 45,9 | 6,1 | 41,8 | Sprung | 50,0>52,0 | - |
| 33 | 65278 | 11.10. 11:34:22 | 50,0 | 50,0 | 45,2 | 45,1 | 4,8 | 43,9 | Ist | - | - |
| 34 | 65860 | 11.10. 17:58:51 | 50,0 | 50,0 | 45,2 | 44,9 | 4,8 | 42,9 | Ist | - | - |
| 35 | 66199 | 11.10. 20:46:12 | 52,0 | 52,0 | 47,2 | 47,2 | 4,8 | 35,0 | Ist n. Sprung | 50,0>52,0 (2 min vorher) | - |
| 36 | 67149 | 12.10. 07:02:01 | 52,0 | 52,0 | 47,1 | 47,2 | 4,9 | 43,0 | Ist | - | ja |
| 37 | 67630 | 12.10. 12:09:42 | 57,0 | 50,0 | 48,5 | 48,4 | 8,6 | 46,5 | Sprung | 50,0>57,0 | - |
| 38 | 68325 | 12.10. 19:24:42 | 52,0 | 50,0 | 46,9 | 46,8 | 5,1 | 39,8 | Sprung | 50,0>52,0 | - |
| 39 | 69231 | 13.10. 05:53:11 | 52,0 | 52,0 | 47,2 | 47,1 | 4,8 | 41,8 | Ist | - | ja |
| 40 | 69851 | 13.10. 12:08:11 | 57,0 | 52,0 | 48,1 | 48,3 | 8,9 | 45,3 | Sprung | 52,0>57,0 | - |
| 41 | 70606 | 13.10. 20:22:22 | 50,0 | 50,0 | 45,1 | 44,9 | 4,9 | 39,4 | Ist | - | - |
| 42 | 71470 | 14.10. 06:18:51 | 52,0 | 52,0 | 47,2 | 47,2 | 4,8 | 43,1 | Ist | - | ja |
| 43 | 72316 | 14.10. 16:04:52 | 50,0 | 50,0 | 45,1 | 45,1 | 4,9 | 42,9 | Ist | - | - |
| 44 | 72701 | 14.10. 19:45:42 | 52,0 | 50,0 | 45,3 | 45,2 | 6,8 | 39,8 | Sprung | 50,0>52,0 | - |
| 45 | 73554 | 15.10. 05:36:11 | 52,0 | 52,0 | 47,2 | 47,3 | 4,8 | 43,4 | Ist | - | - |
| 46 | 74302 | 15.10. 13:37:32 | 57,0 | 50,0 | 46,9 | 46,9 | 10,1 | 43,9 | Sprung | 50,0>57,0 | - |
| 47 | 74823 | 15.10. 18:21:02 | 57,0 | 55,5 | 50,7 | 50,4 | 4,8 | 49,3 | Ist | - | ja |
| 48 | 75280 | 15.10. 20:58:01 | 57,0 | 52,0 | 49,1 | 49,1 | 7,9 | 30,3 | Sprung | 52,0>57,0 | - |
| 49 | 76143 | 16.10. 06:06:01 | 52,0 | 52,0 | 47,1 | 47,1 | 4,9 | 45,0 | Ist | - | ja |
| 50 | 76684 | 16.10. 11:57:01 | 57,0 | 50,0 | 50,3 | 50,3 | 6,7 | 47,0 | Sprung | 50,0>57,0 | - |
| 51 | 77167 | 16.10. 16:00:52 | 57,0 | 57,0 | 52,3 | 52,4 | 4,7 | 49,9 | Ist | - | - |
| 52 | 78194 | 17.10. 06:37:52 | 52,0 | 52,0 | 47,1 | 47,1 | 4,9 | 54,4 | Ist | - | - |
| 53 | 78702 | 17.10. 11:40:53 | 50,0 | 50,0 | 45,1 | 45,1 | 4,9 | 54,4 | Ist | - | - |
| 54 | 79036 | 17.10. 14:03:11 | 57,0 | 50,0 | 48,4 | 48,4 | 8,6 | 48,5 | Sprung | 50,0>57,0 | - |
| 55 | 79734 | 17.10. 21:45:22 | 50,0 | 50,0 | 45,2 | 45,2 | 4,8 | 48,5 | Ist | - | - |
| 56 | 80606 | 18.10. 07:01:32 | 52,0 | 52,0 | 47,3 | 47,2 | 4,7 | 48,5 | Ist | - | - |
| 57 | 80973 | 18.10. 10:34:22 | 50,0 | 50,0 | 45,1 | 45,1 | 4,9 | 48,5 | Ist | - | - |
| 58 | 81661 | 18.10. 15:42:21 | 57,0 | 57,0 | 52,3 | 52,3 | 4,7 | 50,7 | Ist | - | - |
| 59 | 81850 | 18.10. 17:23:01 | 57,0 | 57,0 | 52,4 | 52,5 | 4,6 | 49,8 | Ist | - | - |
| 60 | 82806 | 19.10. 05:54:52 | 52,0 | 52,0 | 47,2 | 47,2 | 4,8 | 27,5 | Ist | - | - |
| 61 | 83447 | 19.10. 11:25:02 | 50,0 | 50,0 | 45,2 | 45,2 | 4,8 | 44,3 | Ist | - | - |
| 62 | 83757 | 19.10. 13:57:32 | 57,0 | 50,0 | 50,0 | 50,0 | 7,0 | 47,5 | Sprung | 50,0>57,0 | - |
| 63 | 84172 | 19.10. 16:52:31 | 57,0 | 57,0 | 52,3 | 52,3 | 4,7 | 51,3 | Ist | - | - |
| 64 | 84267 | 19.10. 17:29:11 | 57,0 | 57,0 | 52,1 | 52,3 | 4,9 | 42,2 | Ist n. Sprung | 50,0>57,0 (23 min vorher) | - |
| 65 | 84679 | 19.10. 19:09:31 | 57,0 | 57,0 | 52,1 | 52,1 | 4,9 | 49,3 | Ist n. Sprung | 52,0>57,0 (13 min vorher) | - |
| 66 | 85509 | 20.10. 06:10:22 | 52,0 | 52,0 | 47,2 | 47,2 | 4,8 | 42,1 | Ist | - | - |
| 67 | 86086 | 20.10. 11:39:01 | 57,0 | 50,0 | 50,8 | 50,8 | 6,2 | 49,0 | Sprung | 50,0>57,0 | - |
| 68 | 87272 | 21.10. 03:56:42 | 50,0 | 50,0 | 45,2 | 45,2 | 4,8 | 40,7 | Ist | - | - |
| 69 | 87594 | 21.10. 06:35:22 | 52,0 | 52,0 | 47,1 | 47,2 | 4,9 | 46,2 | Ist | - | - |
| 70 | 88357 | 21.10. 16:38:22 | 50,0 | 50,0 | 45,1 | 45,2 | 4,9 | 41,7 | Ist | - | - |
| 71 | 88682 | 21.10. 19:25:52 | 50,0 | 50,0 | 45,3 | 45,1 | 4,7 | 44,9 | Ist | - | - |
| 72 | 89731 | 22.10. 05:48:12 | 52,0 | 52,0 | 47,1 | 47,1 | 4,9 | 41,4 | Ist | - | - |
| 73 | 90231 | 22.10. 09:55:42 | 57,0 | 50,0 | 47,3 | 47,3 | 9,7 | 39,6 | Sprung | 50,0>57,0 | - |
| 74 | 90919 | 22.10. 13:14:31 | 57,0 | 50,0 | 52,0 | 52,3 | 5,0 | 49,9 | Sprung | 50,0>57,0 | - |
| 75 | 91432 | 22.10. 18:36:42 | 57,0 | 57,0 | 52,1 | 52,0 | 4,9 | 49,3 | Ist n. Sprung | 50,0>57,0 (25 min vorher) | - |
| 76 | 92143 | 23.10. 04:30:13 | 52,0 | 50,0 | 46,1 | 46,0 | 5,9 | 42,1 | Sprung | 50,0>52,0 | - |
| 77 | 92560 | 23.10. 07:22:12 | 52,0 | 52,0 | 47,2 | 47,2 | 4,8 | 46,2 | Ist | - | ja |
| 78 | 93090 | 23.10. 14:11:22 | 50,0 | 50,0 | 45,1 | 45,1 | 4,9 | 43,0 | Ist | - | - |
| 79 | 93361 | 23.10. 16:04:02 | 57,0 | 50,0 | 51,4 | 51,3 | 5,6 | 49,3 | Sprung | 50,0>57,0 | - |
| 80 | 94361 | 24.10. 05:28:12 | 50,0 | 50,0 | 45,2 | 45,2 | 4,8 | 42,3 | Ist | - | ja |
| 81 | 94882 | 24.10. 10:48:21 | 50,0 | 50,0 | 45,2 | 45,1 | 4,8 | 43,0 | Ist | - | ja |
| 82 | 95284 | 24.10. 14:24:31 | 52,0 | 52,0 | 47,1 | 47,1 | 4,9 | 44,9 | Ist | - | - |
| 83 | 96143 | 25.10. 01:09:22 | 50,0 | 50,0 | 45,2 | 45,2 | 4,8 | 42,3 | Ist | - | - |
| 84 | 96880 | 25.10. 09:23:52 | 50,0 | 50,0 | 45,2 | 45,1 | 4,8 | 43,3 | Ist | - | - |
| 85 | 97376 | 25.10. 14:07:22 | 50,0 | 50,0 | 45,1 | 44,9 | 4,9 | 40,4 | Ist | - | - |
| 86 | 98164 | 25.10. 22:57:01 | 50,0 | 50,0 | 45,1 | 45,1 | 4,9 | 43,1 | Ist | - | ja |
| 87 | 98950 | 26.10. 09:18:52 | 50,0 | 50,0 | 45,1 | 45,1 | 4,9 | 41,0 | Ist | - | - |
| 88 | 99342 | 26.10. 12:05:52 | 50,0 | 50,0 | 45,1 | 45,1 | 4,9 | 42,7 | Ist | - | - |
| 89 | 99776 | 26.10. 16:18:11 | 50,0 | 50,0 | 45,2 | 45,2 | 4,8 | 40,7 | Ist | - | - |
| 90 | 100092 | 26.10. 18:34:12 | 57,0 | 50,0 | 48,0 | 48,0 | 9,0 | 45,7 | Sprung | 50,0>57,0 | - |
| 91 | 101032 | 27.10. 06:55:52 | 50,0 | 50,0 | 45,2 | 45,1 | 4,8 | 41,4 | Ist | - | ja |
| 92 | 101716 | 27.10. 12:49:51 | 50,0 | 50,0 | 45,1 | 45,1 | 4,9 | 43,9 | Ist | - | - |
| 93 | 102163 | 27.10. 17:00:12 | 52,0 | 50,0 | 46,4 | 46,4 | 5,6 | 46,1 | Sprung | 50,0>52,0 | - |
| 94 | 102602 | 27.10. 19:11:41 | 52,0 | 52,0 | 47,2 | 47,1 | 4,8 | 16,5 | Ist | - | - |
| 95 | 103763 | 28.10. 08:57:41 | 50,0 | 50,0 | 45,1 | 45,1 | 4,9 | 40,9 | Ist | - | - |
| 96 | 104338 | 28.10. 13:51:52 | 52,0 | 52,0 | 47,1 | 47,1 | 4,9 | 45,5 | Ist | - | - |
| 97 | 104764 | 28.10. 18:12:51 | 57,0 | 52,0 | 47,7 | 47,6 | 9,3 | 46,1 | Sprung | 52,0>57,0 | ja |
| 98 | 105243 | 28.10. 23:16:02 | 52,0 | 50,0 | 45,5 | 45,5 | 6,5 | 40,0 | Sprung | 50,0>52,0 | - |
| 99 | 105918 | 29.10. 06:41:01 | 57,0 | 57,0 | 47,5 | 47,3 | 9,5 | 39,4 | Sprung | 50,0>57,0 | - |
| 100 | 106536 | 29.10. 12:23:12 | 57,0 | 52,0 | 49,1 | 48,9 | 7,9 | 37,2 | Sprung | 52,0>57,0 | - |
| 101 | 107109 | 29.10. 18:07:51 | 57,0 | 52,0 | 47,7 | 47,6 | 9,3 | 43,8 | Sprung | 52,0>57,0 | ja |
| 102 | 107853 | 30.10. 02:17:42 | 50,0 | 50,0 | 45,1 | 45,1 | 4,9 | 41,8 | Ist | - | ja |
| 103 | 108457 | 30.10. 09:40:02 | 50,0 | 50,0 | 45,1 | 45,1 | 4,9 | 43,7 | Ist | - | - |
| 104 | 109000 | 30.10. 14:58:01 | 52,0 | 52,0 | 46,9 | 47,1 | 5,1 | 44,2 | Ist | - | - |
| 105 | 109551 | 30.10. 19:24:02 | 57,0 | 52,0 | 47,3 | 47,2 | 9,7 | 46,6 | Sprung | 52,0>57,0 | ja |
| 106 | 110512 | 31.10. 08:46:41 | 50,0 | 50,0 | 45,2 | 45,1 | 4,8 | 35,5 | Ist | - | ja |
| 107 | 110880 | 31.10. 11:28:51 | 57,0 | 50,0 | 45,2 | 45,2 | 11,8 | 40,0 | Sprung | 50,0>57,0 | - |
| 108 | 111718 | 31.10. 17:05:12 | 57,0 | 52,0 | 47,3 | 47,3 | 9,7 | 44,9 | Sprung | 52,0>57,0 | - |
| 109 | 112077 | 31.10. 19:54:12 | 57,0 | 52,0 | 47,5 | 47,6 | 9,5 | 28,0 | Sprung | 52,0>57,0 | - |
| 110 | 113064 | 01.11. 05:50:22 | 57,0 | 50,0 | 47,1 | 47,2 | 9,9 | 40,0 | Sprung | 50,0>57,0 | ja |
| 111 | 113728 | 01.11. 13:00:13 | 52,0 | 50,0 | 47,1 | 47,1 | 4,9 | 44,3 | Sprung | 50,0>52,0 | - |
| 112 | 114919 | 02.11. 05:40:22 | 50,0 | 50,0 | 45,1 | 45,1 | 4,9 | 23,3 | Ist | - | ja |
| 113 | 115346 | 02.11. 08:55:42 | 50,0 | 50,0 | 45,2 | 45,2 | 4,8 | 43,1 | Ist | - | - |

September (37 Ladungen, 07.-30.09.): 17 Ist/Ist n. Sprung, ohne die Abtau-Fortsetzung 28.09., sichtbares D 4,7 (3x), 4,8 (3x), 4,9 (11x). Gleiches Bild. [sicher] Skript `f86_f_haupt.py`, `f86_n_end.py`.

### 2. Verteilung bei Ist-Absinken, je Soll

`1499` - `1500` in der letzten Zeile vor der Anforderung (Klassen Ist + Ist n. Sprung, n = 71):

| Soll 1497 | n | 4,6 | 4,7 | 4,8 | 4,9 | 5,1 |
|---|---|---|---|---|---|---|
| 50 | 36 | | 1 | 16 | 19 | |
| 52 | 22 | | 1 | 13 | 7 | 1 |
| 57 (davon 3 mit 1499 = 55,5/55,6/55,9) | 13 | 1 | 4 | 2 | 6 | |

In der ersten Zeile mit Status 1 sieht man bei Soll 50 schon 11x 4,8, 20x 4,9, 5x 5,1. [sicher]

**Wie oft führt ein sichtbarer Wert zur Anforderung?** Verweildauer bei Status 0 und Anforderungen aus diesem Wert (nur Ist-Klassen, Sprünge herausgerechnet, ab 01.10.):

| D sichtbar | Soll 50: Ist | min | Anf. | je h | Soll 52: Ist | min | Anf. | je h | Soll 57: Ist | min | Anf. | je h | alle je h |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4,5 | 45,5 | 416 | 0 | 0 | 47,5 | 222 | 0 | 0 | 52,5 | 63 | 0 | 0 | 0 |
| 4,6 | - | - | - | - | - | - | - | - | 52,4 | 60 | 1 | 1,0 | 0,9 |
| 4,7 | 45,3 | 422 | 1 | 0,14 | 47,3 | 195 | 1 | 0,31 | 52,3 | 42 | 4 | 5,7 | 0,54 |
| 4,8 | 45,2 | 311 | 16 | 3,1 | 47,2 | 93 | 13 | 8,4 | - | - | - | - | 4,5 |
| 4,9 | 45,1 | 55 | 19 | 20,8 | 47,1 | 17 | 7 | 24,2 | 52,1 | 6 | 5 | 50 | 23,7 |
| ≥ 5,0 | 44,9 | 0 | 0 | - | 46,9 | 0,1 | 1 | - | 52,0 | 0 | 0 | - | - |

Bei D 3,9-4,5: 0 Anforderungen in zusammen 3 187 min. [sicher] Skript `f86_n_end.py`.

**Rohwert-Raster** (`f86_g.out`, Zeile A): vorhanden 44,9, 45,1, 45,2, 45,3, 45,5; nie 45,0, 45,4, 46,2, 47,0, 47,4, 50,9, 51,2, 52,2, 52,6. Gleicher Ist im 10-s-Raster während der Ladung: meist nur 10-20 s (Z. 84674-84679: 52,1, 52,1, 52,1, 52,3, 52,1, 52,1). [sicher]

### 3. Gegenprobe: D gleich groß oder größer, keine Anforderung

Zusammenhängende Episoden bei Status 0, `1499` ≠ 10,0, ab 01.10. (`f86_n.out`; alle einzeln in `f86_g.out`, Abschnitt C):

| D ≥ | Episoden | mit Anforderung am Ende | ohne | längste ohne | Summe ohne | davon ≥ 2 min | davon mit laufendem Verdichter | mit Fehlercode |
|---|---|---|---|---|---|---|---|---|
| 4,7 | 235 | 78 | 157 | 24,0 min | 430 min | 61 | 22 | 0 |
| 4,8 | 203 | 68 | 135 | 12,0 min | 266 min | 47 | 15 | 0 |
| 4,9 | 111 | 36 | 75 | 5,3 min | 66 min | 8 | 12 | 0 |
| 5,0 | 4 | 3 | 1 (Z. 57246, kein gültiger Fall) | 0,3 min | 0,3 min | 0 | 1 | 0 |

Die längsten Fälle ohne Anforderung, alle enden dadurch, dass `1500` wieder um eine Stufe steigt:

| Zeit | Zeilen | sichtbar | Dauer | Danach |
|---|---|---|---|---|
| 08.10. <MAC> | 58077-58100 | 47,3/47,2 bei Soll 52 | 24 min | Anforderung erst 05:22:42 bei 47,2/47,2 |
| 04.10. <MAC> | 48444-48455 | 45,2 bei Soll 50 | 12 min | Anforderung 01:11:12 |
| 24.10. <MAC> | 94341-94352 | 45,2/45,1 bei Soll 50 | 12 min | Anforderung 05:28:12 |
| 30.10. <MAC> | 107843-107849 | durchgehend 45,1, Verdichter lief | 5,3 min | Anforderung 02:17:42 |
| 21.10. <MAC> | 88349-88352 | 45,1 bei Soll 50 | 4,0 min | Anforderung 16:38:22 |

Die F84-Fälle passen: 02.11. <MAC> (Z. [Nummer]) lag `1500` bei 47,3, D = 4,7 K, danach fiel `1497` auf 50, also Abstand wieder 2,7 K. 31.10. 03:10 stand ebenfalls 47,3 (F84). Das ist unter der Schwelle, kein Sonderfall. [sicher]

**Sperren einzeln:**

| Zustand | Befund | Sicherheit |
|---|---|---|
| WP011 (< 15 min nach Stopp) | 5 Ist-Anforderungen, sichtbares D 4,8-5,1, Status 1 kommt normal, nur der Verdichter wartet (F83) | sicher |
| Heizlauf (P_el ≥ 20) | 14 Ist-Anforderungen, D 4,8/4,9. Rate bei 4,9: an 25,0/h, aus 24,3/h (`f86_i.out`, mit Sprungzeilen) | sicher |
| Abtauung | `1499` = 10,0 in 54 Zeilen (48 min), Status nie 1. `1497 - 1500` dort nie ≥ 4,9, also kein Testfall für eine echte Blockade. 28.09. 04:44:52 kam Status 1 bei noch geloggtem 10,0 (Ist 39,9, Abtauende): `1499` hinkt nach | sicher für Zählung; Blockade ungeprüft |
| Fehlercode ≠ 255 | fc 222: D max 4,7; fc 0 (18.-20.10.): D max 4,5. Keine Episode ab 4,7 fällt hinein | kein Testfall |
| WP aus 29.10. 08:55-10:50 | `1500` 50,1-51,5 bei Soll 50 | kein Testfall |

### 4. Soll-Sprünge: die sauberste Messung

Sprung auf `1497` (Loxone) bei Status 0, D = neu - `1500` in der Sprungzeile (`f86_j.out`). Sprünge mit D < 0 (3 ab 01.10., 28 im September) sind nicht gezählt:

| D [K] | ab 01.10. n | Anforderung ≤ 20 s | später (bis 15 min, Ist fiel) | keine | September n / ≤ 20 s |
|---|---|---|---|---|---|
| 0-3,4 | 34 | 0 | 1 | 33 | 25 / 0 |
| 3,5-4,4 | 18 | 0 | 0 | 18 | 4 / 0 |
| 4,5-4,6 | 0 | - | - | - | 2 / 0 |
| 4,7 | 4 | 0 | 1 | 3 | 1 / 0 |
| 4,8 | 1 | 0 | 1 | 0 | 1 / 0 |
| 4,9 | 1 | **1** | 0 | 0 | 0 / - |
| 5,0 | 1 | **1** | 0 | 0 | 3 / 2 |
| 5,1-5,4 | 4 | **4** | 0 | 0 | 1 / 1 |
| 5,5-6,9 | 11 | **11** | 0 | 0 | 9 / 9 |
| ≥ 7 | 27 | **26** | 0 | 1 | 7 / 7 |

- 19.10. 18:56:52 (Z. 84663): 52 -> 57 bei 52,3 (D = 4,7): nichts. Anforderung erst 19:09:31 (Z. 84679), 759 s später, bei 52,1. [sicher]
- 11.10. 20:43:51 (Z. 66195): 50 -> 52 bei 47,2 (D = 4,8): nichts. Anforderung 20:46:12, 141 s später, nach sichtbaren 47,1. [sicher]
- 01.11. 13:00:02 (Z. 113727): 50 -> 52 bei 47,1 (D = 4,9): Status 1 um 13:00:13 (Z. 113728), `1499` steht da gerade erst auf 52. Zwei Zeilen vorher (12:58:51) zeigte `1500` 46,9. Das passt zu einem momentanen Wert unter 47,0. [sicher: Werte; wahrscheinlich: Deutung]
- 22.10. 13:14:21 (Z. 90918): 50 -> 57 bei 52,0 (D = 5,0): Status 1 nach 10 s. [sicher]

### 5. Fühlerquelle


### 6. Parameter: wo gesucht wurde

| Quelle | Ergebnis |
|---|---|
| `[lokaler Pfad]` Z. 55, offizielle Liste | `05-000` "Unterschreitet die Warmwassertemperatur ihren Sollwert um den hier eingestellten Wert, wird eine Warmwasserladung gestartet." 0,5-20,0 K |
| `[lokaler Pfad]` Z. 25-29 | Start, wenn der **aktuelle** Sollwert um `05-000` unterschritten wird. Das passt zu `1499`. Werk 2,5 K, aber Anleitung des TTE-FW, nicht WEZ |
| Forum energiesparhaus (in Recherche_05-002 Z. 84) | zwei fremde UltraSource: 5,0 K und 3,0 K |
| HoxPi-MCP `search_registers` "Schaltdifferenz", "differenz", "Einschalt", "Hysterese", "Warmwasser", "hot water" | kein WW-Treffer für diese Größe |
| `[lokaler Pfad]` | dp 5000 nicht vorhanden |
| `[lokaler Pfad]` Z. 14279 | dp 5000 nur für Unit FW (Reg 25727, UID 193). Bewusst nicht abgefragt: anderes Gerät, Unit passt nicht zur WEZ |
| `[lokaler Pfad]` | kein Treffer |
| `[lokaler Pfad]` (06.09.) | Antworten für 2_0_5001, 5002, 5056, **nicht** für 5000 |
| `[lokaler Pfad]` | Zeilen für 05-001/002/003/..., keine für 05-000 |
| `[lokaler Pfad]` Z. 112 | CAN-Scan fg 2, dp 5000-5260: nur 05-050/051/077/086 antworten |
| Pi `/home/<user>`: grep `dp=5000` in *.log, *.txt, *.csv (Timeout 35 s) | kein Treffer; Suche ggf. nicht vollständig |

Live-Wert nur am Bedienteil: `Service -> TTE-WEZ -> Warmwasser -> Parameter` (Menüpfad aus dem Forumsbeitrag). Ältere Aussage in `BACKLOG.md` Z. 112 "Schwelle in der Applikation fest" betraf wahrscheinlich die SLP-Freigabe; dass `05-000` nicht antwortet, sagt nichts über den Wert.

### 7. Zur Einordnung früherer Aussagen

- F79 "Start bei Soll - 4,5 bis -5,0", F84 "4,7 reicht nicht immer", F75 "1497 - 5 K": alle mit dieser Regel erklärt. Die Referenz ist `1499`. [sicher]
- V23 (Verhaltenskarte Z. 131, "widerlegt bei Start > Soll - 4,7") ist nach Wortlaut 2x verletzt: 16.10. 16:00:52 (Z. 77167, D 4,7 davor, 4,6 bei Anf.) und 18.10. 17:23:01 (Z. 81850, 4,6/4,5). Das ist Zittern im 1-min-Raster, nicht eine andere Schwelle. [wahrscheinlich] Nicht geändert, das macht der Orchestrator.
- Projekttext und Notizen "Start bei 1497 - 5 K" gelten nur, solange `1499` = `1497`.

## Vorhersage für den Zwilling

**V-F86, notiert 02.11.2026 12:10, vor dem Ereignis, `1500` = 48,3 (12:07:51):** Bei `1499` = 50,0 ohne Soll-Sprung davor kommt `1504` = 1 bei sichtbarem `1500` ≤ 45,3, erwartet in der Zeile davor 45,1 oder 45,2, und in der ersten Zeile mit Status 1 höchstens 45,3. Sprung auf 52 oder 57 mit D ≥ 4,9: Status 1 in ≤ 20 s.

**Widerlegt, wenn eines davon eintritt (ohne Abtauung, Fehler, Soll-Wechsel):**
- Anforderung, obwohl in den 30 min davor nie `1500` ≤ 45,3 sichtbar war.
- `1500` ≤ 44,9 in zwei aufeinanderfolgenden Zeilen mit Status 0 und Abstand ≥ 60 s.
- Nach dem ersten sichtbaren 45,1 mehr als 30 min keine Anforderung (bisher max. 24,8 min).
- Sprung mit D ≥ 5,0 und Soll-Dauer > 60 s ohne Status 1 in ≤ 60 s.


Zwilling, 1-min-Takt: Start beim ersten Wert ≤ `1499` - 4,9. Verzug bei Soll 50: Median 0,8 min, 90 % ≤ 12,5 min, max. 24,8 min; 2 von 36 starten, bevor 45,1 sichtbar wird. Eine Schwelle von 4,8 wäre schlechter: Median 3,5 min, max. 82,8 min. [sicher] Dazu die `1499`-Regel oben übernehmen.

## Offen

- **Live-Wert `05-000` nicht gelesen** (Tabelle oben). Solange ist 5,0 K eine Messung, keine Ablesung.
- **"≤" oder "<" und "momentan":** nicht aufgelöst. Der interne Reglerwert ist nicht lesbar, das Logger-Raster vor der Ladung ist 60 s. 52,0 löst aus (3 gültige Fälle: 22.10., 25.09., 26.09.), 45,0 gibt es im Raster nicht. Ob ein einzelner Ausreißer reicht oder eine kurze Filterung läuft, ist offen. [Vermutung: einzelner Wert]
- **Abtauung, Fehler, WP aus:** kein Fall mit D ≥ 4,9. Blockade dort nicht getestet.
- **SF2 UND SF** nicht trennbar, siehe oben. SF2 17./18.10. Standbild nicht separat belegt.
- **Sprung-Spitzen 28.10. und 25.09.:** warum `1497` kurz 57 zeigt, dann 52, nicht untersucht (passt zur Stufenfolge des Kicks).
- **Registeralter:** Während der Ladung ändert sich `1500` im 10-s-Takt, also nicht 60 s alt. Bei Status 0 nur in kurzen 10-s-Abschnitten geprüft.

## Was bringt uns das

- **Die offene Frage aus F84/F79 ist beantwortet:** Die "knappen Fälle" sind kein Sonderverhalten. Für den Stundenbericht reicht: "Start bei `1499` - 5 K, sichtbar ab 4,7-4,9 K".
- **Soll-Anhebungen sind jetzt planbar:** Ein Sprung mit D ≥ 4,9 startet binnen 20 s, D ≤ 4,8 nicht. Das gilt auch für die 52 ab 13:00 oder den Kick. [sicher]
- **Schutz vor Fehldeutung nach VL-62-Abbruch:** Nach einer abgebrochenen 57er-Ladung liegt die Startschwelle bei Ist am Ende - 5, also 1,1-2,4 K unter `1497` - 5 (`1499` seit 01.10. um 1,1-2,4 K tiefer). [sicher, 3 Starts]

**Ladungen je Woche (F68, Fixanteil):**

| Größe | Wert | Sicherheit |
|---|---|---|
| Ladungen seit 01.10. | 113 in 32,5 Tagen = **24,3/Woche** | sicher |
| davon Ist-Absinken / Sprung | 15,3 / 9,0 je Woche | sicher |
| Wärme je Ladung (F68-Zähler, 108 zugeordnet) | Ist: 5,9 kWh_th, Sprung: 7,1 kWh_th im Mittel | sicher, 1-kWh-Auflösung |
| Hub Ist-Klasse (Spitze nach Ende bis Start) | Median 6,0 K, Pause Median 6,44 h, Rate 0,93 K/h (p25-p75: 0,67-1,57) | sicher |
| Formel N/Woche = 168 / (Hub/r + 0,68 h) | 23,6 mit Median-r; 17 bei p25, 37 bei p75 | wahrscheinlich; **kein unabhängiger Test**, r stammt aus denselben Daten |
| Fixanteil mit F68 (0,37-0,86 kWh_el je Ladung) | 24,3 x = 9-21 kWh_el/Woche von rund 50, also 18-42 % | Vermutung, F68-Q0 übernommen |

- **Antwort: Ja für den Rahmen, nein für eine Prognose.** Die Schwelle legt den Hub fest (rund 6 K). Die Wochenzahl hängt dann an der Abkühl-/Zapfrate, die wir nicht unabhängig kennen. [wahrscheinlich]
- **Die Sprung-Ladungen sind nicht einfach überzählig.** Sie tragen mehr Wärme je Ladung. Überschlag, ohne Sprünge alle Ladungen wie Ist-Ladungen: (684 - 108 x Q0) / (5,86 - Q0) = **119-122 statt 108 Ladungen** bei Q0 = 1,3-2,2 kWh_th, also eher mehr Ladungen. [Vermutung, kein Test, Verluste bei höherem Soll nicht gerechnet] Damit ist kein Sparvorschlag belegt.

**Vorschläge an der Betreiber (nichts umgesetzt):**
1. `05-000` einmal am Bedienteil ablesen und melden: `Service -> TTE-WEZ -> Warmwasser -> Parameter`. Nur lesen. Das schließt die letzte Lücke dieser Frage.
2. `05-000` nicht ändern. Dafür fehlt der Beleg, dass es netto spart.

## Vorgehen und Dateien

Alle in `[lokaler Pfad]`:
- Daten: `f86_ww_hires.csv` (Kopie F83 + 62 neue Zeilen). Zeilennummern = Pi-Datei, Stichprobe mit `sed` in `f86_n.out` bestätigt 10 von 10.
- Skripte: `f86_a_suche.py` bis `f86_c_suche.py`, `f86_l_can.py`, `f86_k_par.py`, `f86_m_cand.py` (Parameter); `f86_d_holen.py`, `f86_e_lade.py`; `f86_f_haupt.py` (Tabelle); `f86_g_gegen.py` (Verweil, Episoden, Sprünge, SF2); `f86_i_spur.py` (Spur, Raster, 1499-Phasen); `f86_j_rest.py` (Sprung-Tabelle, Verzug, Pausen, F68-Abgleich); `f86_n_end.py` (Endzahlen); dieser Bericht `f86_o_bericht.py`.
- Vorlauf: `[lokaler Pfad]`, `ANALYSE_F84_Nachtanhebung52_20261102.md`, `ANALYSE_F79_Abtauung_WW_Abbruch_20261102.md`, `ANALYSE_F68_WW_Ladungs_AZ_20261102.md`, `WP_Verhaltenskarte.md` (V3, V8, V23, V49, V121).