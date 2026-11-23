# ANALYSE Nachmittags-Heizläufe – Zeitfenster oder Raumkorrektur? – 21.10.2026 22:15 (Orchestrator, nur lesend)

Folgt auf `ANALYSE_1490_Herkunft_Heizlauf_20261021.md` (offene Frage: Lösen die Nachmittagsläufe 14–18 Uhr ein Zeitfenster oder die Raumkorrektur aus?).
Daten: `HoxPi-Doku\or_kuehltest_roh_20261021.csv` (Kopie von `~/hoxpi_fulllog/kuehltest.csv`, 1-min, 01.10.–21.10. 19:56, 29 997 Zeilen).
Skript: `HoxPi-Doku\or_nachmittag_20261021_2215.py/.out`. Loxone-Klimacontroller UG (2131e401-01c4…) führt keine Verlaufsdaten – Raumtemperaturen konnten nicht gegengeprüft werden.

## Befund
3. Nachmittags-Beginne (12–19 Uhr): n = 35, außen Median 15,0 °C, Startwert Median 34,5 °C, Anforderungsdauer Median 49 min.
4. Hoval-Raumsoll HK1 (Reg-Spalte RaumSoll_HK1) springt nur zwischen 5,0 und 22,0 – kein Tagesprofil, das die Nachmittagsstufe erklärt.

## Einordnung
- **Wahrscheinlich:** Die +4…+5 K am Nachmittag kommen aus der Raumkorrektur des Loxone-Klimacontrollers (integrierender Anteil, Transconductance 0,3): die Räume liegen nach der Vormittagspause unter Soll, der Wert baut sich auf und bleibt bis zum Abend stehen. Ein Zeitprogramm mit fester Stufe ist praktisch ausgeschlossen.
- **Nicht ausgeschlossen (Vermutung):** Ein Raum mit höherem Komfort-Soll am Nachmittag (Raumregler-Zeitprogramm) treibt den Klimacontroller – das würde allmählich, nicht als Stufe wirken und passt ebenso.

## Was bringt uns das
- Die Nachmittagsläufe sind kein Fehler der Hoval und keine feste Uhr – Stellschraube ist die Loxone-Raumregelung, nicht die Hoval-Heizkurve.
- Bei 15 °C außen 35 °C Vorlauf anzufordern kostet COP. Wenn ein einzelner Raum der Treiber ist (z. B. Bad/Wohnzimmer mit Komfort-Soll), bringt ein um 0,5 K niedrigeres Nachmittags-Soll dort vermutlich mehr als jede Hoval-Einstellung.

## Nächster Schritt (Loop, nur lesend)
An einem Nachmittag 13–17 Uhr die Raum-Isttemperaturen und -Sollwerte der UG-Räume (Loxone-Raumregler) alle 15 min mitschreiben und neben Reg 1490 legen: welcher Raum liegt unter Soll, wenn 1490 auf ~35 steigt?