# F175: Wie nehmen Regelwaechter und Auswertungen die Versuchsfenster aus? (OR 06.11.2026 16:05)

## Befund [sicher, Code gelesen auf dem Pi, nur lesen]
- `/home/<user>/regelwaechter/rw_pruefung.py` und `waechter.py` kennen keine Versuchsfenster. `rw_experiment.py` prueft nur Abbruch und Rueckweg des laufenden Versuchs.
- Folge: Ein Versuch landet als Verstoss in `verstoesse.csv` und bewegt den Regelstatus. Beispiel W01 06.11. 10:05:02 (E12), Status "offen".
- `/home/<user>/regelwaechter/experiment_aktiv.json` wird nach dem Versuch geloescht, danach ist das Fenster fuer den Waechter weg.

## Vorschlag (nicht umgesetzt, Aenderung am Waechter-Code ist nicht Teil des Orchestratorlaufs)
1. Neue Datei `/home/<user>/regelwaechter/versuchsfenster.csv` mit `id;von;bis`. Startwerte aus dem Vermerk in `[lokaler Pfad]`, korrigierte Zeiten.
2. Fensterende = Start des naechsten Verdichterlaufs nach dem Rueckweg, weil die Wirkung den Rueckweg ueberdauert (E12 bis 11:34:45).
3. In `rw_pruefung.py` in der Ereignisschleife (`for i in ev:`) und in `pruefe_dauer` (`for i in ev_von:`, `for n, i in enumerate(ev):`) je eine Abfrage: Liegt `zeilen[i]["t"]` im Fenster, `unp += 1; continue`. Kein Fall zaehlt dann als ok oder Verstoss.
4. Der Orchestrator traegt in R5/R6 das Fenster ein; das spart die Handarbeit.

## Testfall fuer `pi_deploy.py --tests`
- W01 06.11. 10:05:02 liegt laut F175 im Versuch E12. Mit dem E12-Fenster aus dem Vermerk (Ende 11:34:45, Beginn dort nachlesen) wird die Zeile unpruefbar, W01 zaehlt sie nicht mehr als Verstoss.
- A05a 06.11. 12:00:01 liegt ausserhalb aller Fenster und bleibt Verstoss.
- H01 06.11. 14:15:02 und 15:15:02 liegen ausserhalb und bleiben Verstoss.

## Offen
- Die Zaehlung der Auswertungen in den MD-Paketen ist davon nicht beruehrt; dort steht das Fenster als Ausschluss im Paket.
- Soll das so gebaut werden? Das entscheidet der Betreiber. Rueckweg: Datei leer lassen.

## Was bringt uns das
Regelstatus und Verstoesse zeigen dann die Anlage, nicht unsere Versuche. Bei rund 10 Versuchen am Tag ist das noetig, sonst verlieren bestaetigte Regeln ihre Aussage.