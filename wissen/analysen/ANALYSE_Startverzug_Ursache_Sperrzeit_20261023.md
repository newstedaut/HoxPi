# Startverzug Heizanforderung → Verdichter: Ursache (23.10.2026)
Analyse-Agent 23.10.2026 · nur lesend · Vertiefung zu `ANALYSE_Loxone_MinHr40_Startverzug_20261023.md` und `ANALYSE_Heizlauf_Enden_Ursache_16-23Okt_20261023.md`.
Quellen: `~/hoxpi_fulllog/ww_hires.csv` ab 15.10. 22:00 (lokale Kopie `Emulation\or_startverzug_20261023_wwhires.csv`, 17 301 Zeilen, Raster 10–60 s, **keine Lücke > 180 s**) + Volllogger-Kopien `Emulation\or_ag1_2026-10-*.csv*` (5 min, für 1520/1529/1490/[Nummer]).
Skripte/Ausgaben: `Emulation\or_startverzug_20261023_{holen,a,b,c,d,e,f,g,h}.py` / `.out`.
Spalten ww_hires: Status_HK1 = 1501, Modulation = 18726, Leistung_Soll = 18767 (01-009 Sollwert Leistung WEZ, ×0,1 %; −127 % = keine Anf.), Ruecklauf ≈ 1535, WP_VL/WP_RL = WP-intern (bis 17.10. 17:41 eingefroren 30,7/29,4).
Laufkriterium: Modulation > 0. Modus am Start: SLP am ersten Laufpunkt (1 = WW).
Anforderungsblock = Status_HK1 wird 23. Im hires-Raster **36 Blöcke** (Volllogger 5 min: 32 – die 4 zusätzlichen sind < 1 min lange 23-Flacker beim WW-Start).

## Kernbefund
1. **Es gibt zwei Arten von Anforderung, und der Verzug hängt nicht an Loxone.**
   - **„Nach WW“ (1501 springt 6 → 23 beim WW-Stopp, 14 Blöcke):** Heizstart **20,0–20,9 min nach dem WW-Verdichterstopp** in 8 von 10 Blöcken mit Start (dazu 22,7 und 39,5 min). Das ist der bekannte „20-min-Verzug“.
   - **„Frisch“ (1501 springt 0 → 23, Verdichter steht):** entweder **Sofortstart nach 1 min** (6×) oder **16–44 min** (7×), **unabhängig davon, wie lange die WP schon stand** (17.10. 08:25: 85 min Stillstand → 16 min Verzug; 17.10. 17:41: 189 min → 16 min; 18.10. 14:19: 170 min → 19 min).
2. **Während des Wartens hält die Hoval-WEZ-Logik den Sollwert zurück (sicher):** 18768 = 100 (Anforderung kommt an), 1501 = 23, HK-Pumpe läuft, WP-Umwälzpumpe 27496 = **30 %**, aber **1529 WEZ-Soll = 0** und 1539 = 0. Erst am Start springt 1529 auf den HK-Soll und 27496 auf 80 %. Der Verzug sitzt also in der TTE-WEZ / im Kaskadenmanager, **nicht** in Loxone und **nicht** im Kältekreisregler (pCO bekommt gar keinen Sollwert).
3. **18767 (Leistungssollwert) ist nicht der Auslöser (sicher):** Starts erfolgten bei 18767 zwischen **−78 %** und **+80 %**; bei 18.10. 14:19 stand 18767 18 min lang auf +35…+80 % ohne Start.
4. **Bestes Modell (wahrscheinlich, passt 17 von 18 verzögerten Starts auf ±2 min):**
   **Start ≈ 15 min, nachdem RL (1535) ≤ HK-Soll 1520 − ca. 1,5 K erfüllt ist.**
   Nach WW braucht das Spülen des heißen Wassers aus dem Rücklauf 4–5 min (RL fällt von 50–59 auf 29–32 °C), plus 15 min → genau die 20 min. Bei frischer Anforderung mit stehend-warmem RL (≥ 30,5 °C) fällt der RL in 1–5 min unter die Schwelle, plus 15 min → 16–20 min. Wo der RL lange knapp am Soll blieb, kam der Start entsprechend später (16.10. 16:30 → 38 min, 17.10. 09:15 → 44 min).
   Der bisher als „V99/V13 = 15 min Mindeststillstand“ geführte Wert ist damit **wahrscheinlich eine 15-min-Einschaltverzögerung auf die Temperaturbedingung**, kein reiner Stillstands-Timer: kürzeste reguläre Pause in diesem Fenster ist **20,0 min** (8× WW→HZ), HZ→HZ-Pausen 27–37 min.
5. **Sofortstart (0–1 min) – was ist anders (sicher, n = 15 frische Blöcke):** RL **stehend kalt ≤ 29,5 °C** vor der Anforderung (23,5–29,5) **und** Stillstand ≥ 50 min. Alle frischen Blöcke mit RL ≥ 30,5 °C vor der Anforderung starteten **nie** sofort. Warum der Timer dort schon „abgelaufen“ ist: **Vermutung** – die WEZ wertet die Bedingung auch ohne Anforderung gegen einen Grund-/Mindestsoll (~31 °C) aus, der Timer lief also schon vorher. Nicht prüfbar ohne Parameterliste.

## Alle Anforderungsblöcke (ww_hires, 16.10. 00:00 – 23.10. 11:55)
Legende: vorher = 1501 vor dem Block (0 Aus, 6 Zwangsreduktion = WW lief). „Stopp“ = letzter Verdichterstopp (beliebiger Modus). RL vor = Ruecklauf 1 Punkt vor Anforderung (stehendes Wasser). 1490/1520 = erster Volllogger-Punkt nach der Anforderung. „Bed. ab“ = Minute nach Anforderung, ab der RL ≤ 1520 − 1,5 K; „Modell“ = Bed. ab + 15 min.
| # | Anforderung | Dauer min | vorher | letzter Stopp (Modus) | Stopp→Anf min | Heizstart | **Verzug min** | Stopp→Start min | RL vor °C | 1490 / 1520 | Bed. ab / Modell | Klasse / Bemerkung |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 16.10. 05:48:52 | 18 | 0 | – (Nacht) | lang | 05:49:51 | **1,0** | – | 28,5 | 31,7 / 34,5 | – | **sofort**; 18 min später WW-Umschaltung |
| 2 | 16.10. 06:43:51 | 112 | 6 | 06:43:21 WW | 0,5 | 07:03:52 | **20,0** | 20,5 | 54,0 | 37,5 / 40,0 | 5 / 20 | nach WW |
| 3 | 16.10. 11:57:11 | 0,3 | 0 | 08:36 HZ | 200 | – | – | – | 22,0 | – | – | 23-Flacker beim WW-Start 11:57:51 |
| 4 | 16.10. 12:43:51 | 23 | 6 | 12:43:11 WW | 0,7 | 13:03:52 | **20,0** | 20,7 | 59,0 | 35,9 / 38,5 | 4 / 19 | nach WW (Lauf nur 4 min, Loxone weg) |
| 5 | 16.10. 13:18:52 | 39 | 0 | 13:07:52 HZ | 11,0 | 13:34:52 | **16,0** | 27,0 | 30,5 | 35,7 / 38,5 | 0 / 15 | frisch, kurz nach Stopp |
| 6 | 16.10. 14:48:52 | 39 | 0 | 13:58:52 HZ | 50,0 | 14:49:51 | **1,0** | 51,0 | 26,5 | 35,0 / 38,0 | – | **sofort** |
| 7 | 16.10. 16:30:53 | 117 | 6 | 16:29:21 WW | 1,5 | 17:08:52 | **38,0** | 39,5 | 59,0 | 34,4 / 37,0 | 23 / 38 | nach WW, RL blieb 35,5–37 ≈ Soll |
| 8 | 16.10. 20:02:52 | 228 | 0 | 18:28:51 HZ | 94 | – | – | – | 26,0 | 24,0 / 30,0 | nie | kein Start: RL = Soll + 4…6 K (Abendsoll 30) |
| 9 | 17.10. 08:25:52 | 39 | 0 | 07:16:32 WW | 69,3 | 08:41:52 | **16,0** | 85,3 | 35,0 | 31,5 / 34,5 | 1 / 16 | frisch, RL stehend warm |
| 10 | 17.10. 09:15:53 | 64 | 0 | 09:04:52 HZ | 11,0 | 09:59:52 | **44,0** | 55,0 | 32,5 | 30,5 / 33,5 | 29 / 44 | frisch, RL lange nur −1…−1,5 K |
| 11 | 17.10. 17:41:51 | 39 | 0 | 14:49:11 WW | 172,7 | 17:57:52 | **16,0** | 188,7 | 38,5 | 34,9 / 37,5 | 1 / 16 | frisch, RL stehend warm |
| 12 | 17.10. 20:11:52 | 94 | 0 | 18:20:52 HZ | 111 | – | – | – | 27,5 | 24,0 / 30,0 | nie | kein Start: RL = Soll + 6…7,5 K |
| 13 | 18.10. 07:01:22 | 0,8 | 0 | 17.10. 22:46 WW | 495 | – | – | – | 28,0 | – | – | 23-Flacker beim WW-Start 07:02:11 |
| 14 | 18.10. 07:31:41 | 64 | 6 | 07:31:01 WW | 0,7 | 07:51:52 | **20,2** | 20,9 | 51,5 | 30,4 / 33,0 | 5 / 20 | nach WW; Start bei 18767 = −78 % |
| 15 | 18.10. 14:19:51 | 39 | 0 | 11:48:41 WW | 151,2 | 14:38:51 | **19,0** | 170,2 | 35,5 | 35,2 / 38,0 | 0–1 / 16 | frisch; **einziger Ausreißer** (+3 min) |
| 16 | 18.10. 15:59:52 | 29 | 6 | 15:59:32 WW | 0,3 | – | – | – | 56,5 | 28,4 / 31,5→38,0 | 16 / 31 | Soll erst 16:15 auf 38; Anf. endet 16:28 vor Modell-Start |
| 17 | 18.10. 17:05:53 | 18 | 0 | 15:59:32 WW | 66,3 | – | – | – | 32,0 | 35,2 / 38,0 | 0–4 / 15–19 | Anf. endet 17:23:42, WW startet 17:23:52 |
| 18 | 18.10. 18:02:51 | 34 | 6 | 18:02:11 WW | 0,7 | 18:22:51 | **20,0** | 20,7 | 59,0 | 35,3 / 38,0 | 5 / 20 | nach WW |
| 19 | 18.10. 20:32:52 | 175 | 0 | 18:37:52 HZ | 115 | – | – | – | 25,5 | 24,0 / 30,0 | nie | kein Start: RL = Soll + 0,5…3 K |
| 20 | 19.10. 06:56:12 | 39 | 6 | 06:55:52 WW | 0,3 | 07:15:52 | **19,7** | 20,0 | 54,0 | 30,6 / 33,5 | 5 / 20 | nach WW |
| 21 | 19.10. 09:13:52 | 39 | 0 | 07:35:52 HZ | 98,0 | 09:14:52 | **1,0** | 99,0 | 23,5 | 30,8 / 33,5 | – | **sofort** |
| 22 | 19.10. 13:57:42 | 0,7 | 0 | 11:54:42 WW | 123 | – | – | – | 35,0 | – | – | 23-Flacker beim WW-Start 13:58:32 |
| 23 | 19.10. 18:31:52 | 11 | 6 | 18:30:33 WW | 1,3 | – | – | – | 52,0 | 28,6 / 31,0 | – | Anf. nach 11 min weg |
| 24 | 19.10. 18:56:52 | 14 | 0 | 18:30:33 WW | 26,3 | – | – | – | 31,0 | 35,5 / 38,5 | 0 / 15 | WW startet 19:10:13 (13 min) vor Modell-Start |
| 25 | 20.10. 06:59:41 | 280 | 6 | 06:59:11 WW | 0,5 | 07:19:52 | **20,2** | 20,7 | 52,0 | 31,1 / 34,0 | 4 / 19 | nach WW |
| 26 | 20.10. 12:19:31 | 293 | 6 | 12:18:52 WW | 0,7 | (17:10:55) | – | – | 59,0 | 35,9 / 38,5 | – | **Daten eingefroren** 12:25–17:05 (hires: 2 verschiedene Zeilen in 280; Volllogger 1535/1477 konstant) → nicht auswertbar |
| 27 | 21.10. 15:24:52 | 39 | 0 | 07:05:33 WW | 499 | 15:25:52 | **1,0** | 500 | 28,5 | 29,2 / 32,0 | – | **sofort** |
| 28 | 21.10. 17:08:31 | 66 | 6 | 17:08:01 WW | 0,5 | 17:28:52 | **20,4** | 20,9 | 51,5 | 29,4 / 32,0 | 5 / 20 | nach WW |
| 29 | 22.10. 04:21:52 | 39 | 0 | 21.10. 20:50 WW | 451 | 04:22:52 | **1,0** | 452 | 29,0 | 31,5 / 34,5 | – | **sofort** |
| 30 | 22.10. 07:01:52 | 47 | 0 | 06:37:01 WW | 24,9 | 07:21:52 | **20,0** | 44,9 | 35,0 | 31,5 / 34,5 | 5 / 20 | frisch, RL stehend warm (WW-Rest) |
| 31 | 22.10. 07:52:52 | 41 | 0 | 07:49:52 HZ | 3,0 | 08:18:51 | **26,0** | 29,0 | 36,0 | 31,5 / 34,0 | 11 / 26 | frisch, 3 min nach Loxone-Abwurf |
| 32 | 22.10. 13:14:31 | 0,5 | 0 | 11:32 WW | 102 | – | – | – | 35,5 | – | – | 23-Flacker beim WW-Start 13:15:12 |
| 33 | 22.10. 13:51:42 | 2 | 6 | 13:51:22 WW | 0,3 | – | – | – | 59,0 | – | – | Anf. nach 2 min weg |
| 34 | 23.10. 03:00:52 | 39 | 0 | 22.10. 18:59 WW | 482 | 03:01:51 | **1,0** | 483 | 27,5 | 33,1 / 36,0 | – | **sofort** |
| 35 | 23.10. 05:18:01 | 125 | 6 | 05:17:52 WW | 0,1 | 05:37:52 | **19,9** | 20,0 | 53,0 | 33,2 / 36,0 | 5 / 20 | nach WW; Lauf endet 07:22 mit WW-Umschaltung |
| 36 | 23.10. 07:45:42 | 250 | 6 | 07:45:12 WW | 0,5 | 08:07:52 | **22,2** | 22,7 | 50,5 | 33,0 / 36,0 | 7 / 22 | nach WW, RL langsamer gefallen |

**Zusammenfassung:** 23 Blöcke mit Heizstart (ohne #26). Davon **6 sofort** (1 min), **11× 19,7–20,4 min**, 3× 16 min, je 1× 22, 26, 38, 44 min. Modell „Bed. + 15 min“: 16 von 17 verzögerten Starts auf ±1 min, 1× +3 min (#15). Die 3 abendlichen Blöcke ohne Start (#8, #12, #19) haben RL ≥ Soll – dort schaltet die WP richtigerweise gar nicht ein. Die 4 Fälle, in denen die Anforderung vor dem Modell-Start endete (#16, #17, #23, #24), passen dazu.

## Antworten auf die drei Fragen
**(1) Korreliert der Verzug mit der Zeit seit dem letzten Verdichterstopp?**
- **Nach WW: ja, scheinbar (sicher als Messung).** Start = WW-Stopp + 20,0–20,9 min (8 von 10, Rest 22,7 / 39,5). Die Pause ist so konstant, weil die Anforderung immer genau am WW-Stopp beginnt.
- **Bei frischer Anforderung: nein (sicher).** 85, 170, 189 min Stillstand → trotzdem 16–19 min Verzug; 50 min Stillstand → 1 min. Eine feste Sperrzeit „letzter Stopp + X“ erklärt die Daten **nicht**.
- Kürzeste reguläre Pause im ganzen Fenster: **20,0 min** (nur 18.10. 11:13 = 2,3 min nach Fehler 222/Reglerreset, ausgenommen). Histogramm Pausen < 40 min: 20 min 8×, 22/26/27/29/35/36/37 min je 1×, 39 min 2×. Eine Pause zwischen 15 und 20 min kam in diesem Fenster **nie** vor.

**(2) Hängt der Start an RL/VL gegen Soll?**
- **Teilweise – aber nicht als reine Schwelle (sicher).** Der RL fällt nach Anforderungsbeginn binnen 1–6 min um 4–8 K unter den Soll (z. B. 18.10. 14:25: RL 29,5 bei Soll 38,0), und trotzdem startet die WP erst 13 min später. Eine Bedingung „RL < Soll − x“ allein würde Starts nach 2–6 min ergeben.
- **Wahrscheinlich:** Bedingung RL ≤ Soll − ~1,5 K **plus 15 min Verzögerung**. Wo der RL lange knapp über der Schwelle blieb (#7, #10, #31), hat der Start genau so viel länger gedauert. Die Schwelle 1,5 K liegt nahe an 33-054 „Einschaltdiff. Heizen“ = 1,0 K (laut Bedienteil-Katalog unbestätigt). Im Raster (RL 0,5 K, 1520 5 min) sind 1,0 und 1,5 K **nicht trennbar**.
- Spiegelbildlich dazu die Abschaltung: RL ≈ Soll + 2,5 K (Heizlauf-Enden-Analyse).
- **Welcher Fühler genau, nicht ermittelbar:** 1535 und WP_RL liefen in den Wartephasen auf ±0,3 K gleich. Der hires-„Vorlauf“ ist bis 17.10. eingefroren.

**(3) Was ist bei den 0-min-Fällen anders?**
- **Sicher (6/6 gegen 9/9):** RL vor der Anforderung (stehendes Wasser) **≤ 29,5 °C** (23,5 / 26,5 / 27,5 / 28,5 / 28,5 / 29,0). Alle frischen Blöcke mit **≥ 30,5 °C** (30,5–38,5) starteten verzögert. Dazu war die Stillstandszeit ≥ 50 min.
- **Nicht trennend:** Tageszeit (03:00–15:24), Außentemperatur, 18767 vor der Anforderung (−127 % in beiden Gruppen), Pumpenstatus vor der Anforderung (27496 = aus in beiden Gruppen).
- Die 0-min-Fälle sind genau die Blöcke, in denen Loxones MinHr 40 voll als Laufzeit ankommt (16.10. 14:49, 19.10. 09:14, 22.10. 04:22, 23.10. 03:01: je ~38–40 min).
- **Vermutung:** Die 15-min-Verzögerung läuft auch ohne Anforderung gegen einen Grund-Sollwert (~31 °C). Bei lange kaltem Rücklauf ist sie dann beim Eintreffen der Anforderung schon abgelaufen. Prüfbar nur über die Parameterliste oder einen gezielten Versuch.

## Einordnung
| Aussage | Stufe |
|---|---|
| Während des Wartens: 18768 = 100, 1501 = 23, 27496 = 30 %, aber 1529 = 0 → Hoval-WEZ hält den Sollwert zurück | **sicher** |
| 18767 (Leistungssollwert KM) ist nicht der Startauslöser | **sicher** |
| Kein fester Timer „ab letztem Stopp“ bei frischer Anforderung | **sicher** |
| Nach WW: Start = Stopp + ~20 min; nie eine Pause < 20 min ohne Reset | **sicher** (Fenster 16.–23.10.) |
| Sofortstart nur bei stehendem RL ≤ 29,5 °C | **sicher** (n = 15, empirisch) |
| Mechanismus „RL ≤ Soll − 1,5 K, dann 15 min“ | **wahrscheinlich** (16/17 auf ±1 min) |
| „V99/V13 = 15 min Mindeststillstand“ ist in Wahrheit diese Einschaltverzögerung | **wahrscheinlich** |
| Timer läuft auch ohne Anforderung (Erklärung der Sofortstarts) | **Vermutung** |
| Parametername/-nummer der 15 min, Fühler (1535 oder WP-intern), Schwelle 1,0 vs. 1,5 K | **nicht ermittelbar** aus den Logs |
| Block 20.10. 12:19–17:10 | **nicht auswertbar** (Daten eingefroren) |

## Vorschlag (nur Vorschlag – nichts verstellt, der Betreiber entscheidet)
1. **Loxone: Mindestlaufzeit ab echtem Verdichterstart statt ab Anforderung.** Monoflop 40 min (https://www.loxone.com/dede/kb/monoflop/) auf steigende Flanke „1539 = 1 UND 18726 > 0“, ODER-verknüpft mit dem Ausgang des Klimacontrollers HC1 (https://www.loxone.com/dede/kb/klima-controller/) vor dem Schreibwert „Heizen extern“. Einfachere Variante: MinHr am Klimacontroller von 40 auf **60 min**.
   - **Was bringt uns das:** Der Verzug ist auf Hoval-Seite fest (15 min nach Erreichen der Einschaltbedingung, nach WW also 20 min). Loxone kann ihn nicht verkürzen, aber aufhören, ihn von der Laufzeit abzuziehen. 11 der 17 verzögerten Blöcke bekämen statt ~20 min wieder ~40 min Verdichterlauf. Grob ~1 Start/Tag weniger und 3–5 kWh_el/Woche (Schätzung aus der Heizlauf-Enden-Analyse, nicht gemessen).
   - **Rückweg:** Monoflop entfernen bzw. MinHr zurück auf 40.
2. **Loxone-Anforderung nicht „früher“, sondern „nicht zu kurz“.** Eine frühere Anforderung bringt nur dann etwas, wenn sie danach auch stehen bleibt: Der 15-min-Timer startet erst mit der Anforderung bzw. dem Spülen. Wird die Anforderung binnen 20 min nach einem WW-Stopp oder einem Loxone-Abwurf wieder weggenommen (#16, #17, #23, #24, #33), läuft die HK-Pumpe ohne Verdichterlauf.
   - **Was bringt uns das:** keine „Leer-Anforderungen“ und keine Heizläufe unter 5 min mehr (#4: 4 min). Das kostet nichts.
3. **Am Bedienteil nur ablesen** (Service > TTE-WEZ bzw. WFA-200-/Kältekreis-Parameter): den Parameter mit **15 min** suchen, der als Einschaltverzögerung, Wartezeit, Mindeststillstand oder Verdichter-Sperrzeit bezeichnet ist (bisher als V99 geführt). Dazu **33-054 Einschaltdiff. Heizen** (1,0 K?) und die zugehörige Ausschaltdifferenz (~2,5 K?) gegen den Katalog prüfen und abfilmen.
   - **Was bringt uns das:** Mit Name und Nummer wird aus „wahrscheinlich“ ein „sicher“. Dann lässt sich auch entscheiden, ob z. B. 10 min statt 15 min vertretbar wären. Nicht selbst verstellen, das ist Takt-/Verdichterschutz; nur mit Hoval-Service.
4. **Loop/Monitoring:** Der Block 20.10. 12:25–17:05 war in hires **und** Volllogger eingefroren (5 h, Außentemp. konstant 11,3 °C). Das passt zum „Außen-Sprung 11,3 → 16,3 °C um 17:10“ aus der Taktschutz-Analyse: dort war es kein Fühlereffekt, sondern der Datenstrom, der wieder anlief. Für weitere Auswertungen ein Stale-Flag (alle Spalten unverändert > 15 min) vorsehen.

## Gegenprobe (lesend)
- Nächster Heizstart nach einer WW-Ladung: Liegt der Start bei WW-Stopp + 20 min ± 1? Und fällt der RL 4–5 min nach dem Stopp unter Soll − 1,5?
- Nächste frische Anforderung bei stehend warmem RL (≥ 31 °C): Start ≈ (erster Zeitpunkt RL ≤ 1520 − 1,5) + 15 min?
- Nächster Sofortstart: RL vor der Anforderung ≤ 29,5 °C?

## Rohdaten-Stichprobe zum Nachprüfen
`~/hoxpi_fulllog/ww_hires.csv`, 18.10.2026 (frische Anforderung nach 170 min Stillstand):
- 14:18:52 Status_HK1 = 0, Modulation = 0, Ruecklauf = 355, Leistung_Soll = −1270
- 14:19:51 Status_HK1 = **23**, Pumpe_HK1 = 1, Modulation = 0, Ruecklauf = 355, Leistung_Soll = 0
- 14:25:53 … 14:35:5x: Status_HK1 = 23, Modulation = 0, Ruecklauf = **295**, Leistung_Soll = 540 … 800 (+54 … +80 %)
- 14:38:51 Modulation = **43**, Ruecklauf = 300, P_el = 197, Leistung_Soll = 800 (Start, 19 min nach der Anforderung)
- Volllogger `2026-10-18.csv.gz`: 14:25 / 14:30 / 14:35 → 1501 = 23, 18768 = 100, 1520 = 380, **1529 = 0**, 27496 = **30**; 14:40 → 1529 = **380**, 27496 = **80**, 1539 = 1.
- Gegenbeispiel Sofortstart: `ww_hires.csv` 19.10. 09:13:52 Status_HK1 0 → 23, Ruecklauf **235**; 09:14:52 Modulation = **42**.