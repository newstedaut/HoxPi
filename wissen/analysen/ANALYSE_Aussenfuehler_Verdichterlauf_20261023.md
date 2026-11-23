# Analyse: Beeinflusst der Verdichter-/Lüfterlauf den Außenfühler? — Orchestrator 23.10.2026 14:00
Anlass: Vermutung in `ANALYSE_Taktschutz_V99_V101_20261022.md` („Aussen springt beim Start 20.10. 17:10 von 11,3 auf 16,3 °C – Fühler sieht Abwärme?“). Für die Winter-Heizkurve wichtig: Die Hoval rechnet den VL-Soll aus diesem Außenwert.
Quelle: Kopie `~/hoxpi_fulllog/ww_hires.csv` (07.09.–23.10.2026 13:55, 93 071 Zeilen, Raster 60 s/teils 10 s), nur gelesen → `[lokaler Pfad]`.
Skript/Ausgabe: `[lokaler Pfad]` / `.out`.
Methode: Lauf = Modulation > 0. Bezug = Mittel Aussen der 5 min vor Start. Differenz bei +2/+5/+10/+20/+30/+45 min Lauf und nach Stopp (+5…+30 min, nur solange kein neuer Lauf). Eingefrorene Blöcke (≥ 10 identische Zeilen, 444 Zeilen) ausgeschlossen.

## Ergebnis (302 Läufe: 181 Heizen, 115 WW, 6 sonst)
| | +2 min | +5 | +10 | +20 | +30 | nach Stopp +10 |
|---|---|---|---|---|---|---|
| Heizen Median ΔA | 0,0 K | 0,0 | +0,1 | +0,1 | +0,1 | 0,0 |
| WW Median ΔA | 0,0 K | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 |
- **Kein Sprung beim Start** (Median 0,0 K nach 2 und 5 min, Spannweite ±0,3–0,5 K) und **kein Rücksprung nach Stopp** (Median 0,0 K). Ein Abwärme-/Kaltluft-Effekt des Außengeräts würde beides zeigen.
- Die größeren Einzelwerte (bis ±1,9 K nach 45 min) folgen dem Tagesgang: morgens/vormittags steigend (Sonne), abends fallend – und laufen nach dem Stopp in gleicher Richtung weiter. Beispiel 23.10. 11:05: Außen stieg schon vor dem Start (3,6 → 3,7 → 3,8 °C) und nach dem Stopp weiter (+1,1 K in 30 min).
- Auch unter 3 °C außen (n = 8 Heizläufe, u. a. 23.10. 03:01 bei 2,8 °C) nach 10 min nur +0,2 K Median.
- Stichprobe gegen Pi-Rohdatei (selbst): 23.10. 03:00:52–03:03:52 Mod 0→42, Aussen 28 = 2,8 °C konstant ✓; 11:02:52–11:09:51 Aussen 36→40 bei Mod 0→46→35, Anstieg beginnt vor dem Start ✓.

## Bewertung
- **Sicher (Messung):** Der Hoval-Außenfühler wird durch den Verdichter-/Lüfterlauf nicht messbar beeinflusst (< 0,1 K, unter der Auflösung).
- **Sicher:** Der „Sprung 11,3 → 16,3 °C“ am 20.10. 17:10 ist das Ende eines eingefrorenen Datenblocks (12:25–17:05, siehe `ANALYSE_Startverzug_Ursache_Sperrzeit_20261023.md` Punkt 4), kein Fühlereffekt. Die Vermutung aus der Taktschutz-Analyse ist damit **widerlegt**.
- Nicht geprüft: Abgleich gegen einen unabhängigen Außenfühler (Loxone/Wetter) – Montageort und Sonnenschutz des Hoval-Fühlers bleiben offen (Vormittagsanstieg kann teils Sonneneinstrahlung sein).

## Was bringt uns das
- Heizkurven- und Arbeitszahl-Auswertungen dürfen die Hoval-Spalte `Aussen` auch während der Läufe nehmen – kein Umweg über Stillstandszeiten oder Loxone nötig.
- Die Heizkurve wird im Winter nicht durch einen „warm gerechneten“ Außenwert während des Laufs abgesenkt; Taktursachen liegen woanders (Loxone-Anforderung, Schaltdifferenz).
- Offen nur noch: Sonneneinfluss am Fühler (Foto vom Montageort, Nordseite?) – kleiner Punkt, nur bei auffälligen Vormittagswerten nachgehen.