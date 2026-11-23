# F109 / F111: Status 1539 = 16 ist die 15-min-Sperre (05.11.2026 18:00, Orchestrator)

Quelle: Prometheus `hoval_wez_status` 02.09.-05.11.2026, 30-s-Raster, 184121 Punkte, Skript `[lokaler Pfad]`; Pausen aus ww_hires und Volllogger, Skripte `or_md41_pruef.py`, `or_md41_pruef2.py`. Nur gelesen.

## Belegt
- Stehzeit Lauf -> naechstes 51: n 303, keine unter 900 s, 21 genau 900 s [sicher als Messung].
- Lauf -> 0 -> 16: n 24, 19 mit 0 + 16 = genau 900 s. Rest: 3 endeten auf 0, 1 auf 17, 1 lief bei der Abfrage noch. 12 nach WW, 12 nach Heizen [sicher].
- Nach Abtauung: n 15, 0 + 16 = 270 oder 300 s, danach 12x 51, 2x 1, 1x 4 [sicher].
- Die rund 16 min Heizstart-Wartezeit laufen auf 1539 = 0. Kein Zustandsregister zeigt sie (555 Spalten, Pruefung MD-41). 18767 steigt meist in dieser Zeit, taugt aber nicht als Uhr [sicher, Zahlen im Pruefvermerk von `[lokaler Pfad]`].

## Wahrscheinlich
- 1539 = 16 heisst: Sperrzeit laeuft, eine Anforderung liegt schon an. Ohne Anforderung steht in derselben Zeit 0.

## Offen
- Ist die Heizstart-Wartezeit dieselbe 900-s-Logik plus Startphase [Vermutung]? Das 1-min-Raster trennt das nicht.
- Was die Sperre eine WW-Ladung kostet: F111, Paket MD-42.

## Was bringt uns das
Der Zwilling kann die Stehzeit hart mit 900 s rechnen. Der Waechter sieht an 1539 = 16 eine wartende Anforderung. Fuer der Betreiber ist nichts zu tun.