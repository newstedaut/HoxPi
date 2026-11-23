# F54 – Pausenende live beobachtet, 31.10.2026 (Orchestrator 16:54 MEZ)

Quelle: HoxPi `get_history` (Prometheus, 1-min, MEZ) `hc1_status`, `wp_ruecklauf_c`; HoxPi `read_register` 1490/1520/1535/1501/25611/1477 um 16:55; Loxone `control_state` Klimacontroller UG (<UUID>) 16:55 MEZ; Journal-Stundenbericht 13:20. Alles nur gelesen.

| Zeit (MEZ) | Ereignis | Beleg | Sicherheit |
|---|---|---|---|
| 11:00–11:25 | letzter Heizlauf, Stopp an RL = 1520 + 3,0 K | Journal 13:20 (V129r) | sicher |
| 11:30–13:07 | WW-Ladung (57er-Kick) | Journal 13:20 | sicher |
| 13:08–16:30 | hc1_status 1501 = 0, 1490 = 0 (Loxone fordert nicht) | Prometheus hc1_status 0 durchgehend | sicher |
| 13:21 | Klimacontroller UG demandHeat 12, threshold 30, 1 von 8 Räumen | Journal 13:20 | sicher |
| 13:12–16:30 | RL (Stillstand, ohne Durchfluss) 36,1 → 33,2 °C, ~0,9 K/h | Prometheus wp_ruecklauf_c | sicher |
| 16:31 | hc1_status 0 → 23 (Konstantanforderung), 1490 = 29,4 | Prometheus + read_register | sicher |
| 16:31–16:55 | RL mit HK1-Pumpe 33,2 → 30,6 °C (FBH-Wasser kühler) | Prometheus | sicher |
| 16:55 | demandHeat 30 = threshold 30, 5 von 8 Räumen demand 1; 1520 = 32,0, RL 1535 = 30,5 = Startschwelle 1520 − 1,5; Verdichter 25611 = 0,0 kW | read_register, control_state | sicher |

## Ergebnis
- Die Heizpause 11:25 → ≥ 16:55 (≥ 5,5 h bei AT 8,8–9,4 °C) wurde **von Loxone verlängert**: 1490 stand 13:08–16:30 auf 0. Die Hoval-Hysterese wäre mit RL 33,2 < 1520 hier gar nicht gefragt worden (sicher).
- Pausenende-Kette (sicher für diesen Fall): Klimacontroller-demandHeat steigt bis threshold (12 → 30, 1/8 → 5/8 Räume) → Loxone schreibt 1490 → HK1-Pumpe läuft, RL fällt auf Soll − 1,5 K → dann HKA59 15 min (F5) → Verdichterstart. Erwarteter Start frühestens ~17:10 (Vermutung, nicht zurückgelesen – Loop 19-Lauf prüft).
- Zwischen Loxone-Freigabe und Verdichterstart liegen dadurch ≥ 24 min + 15 min HKA59, weil der stehende RL-Fühler (33,2) wärmer ist als das FBH-Wasser (wahrscheinlich).

## Was bringt uns das
Der Zwilling kann Pausen bei mildem Wetter als „Loxone-Pause bis demandHeat ≥ threshold“ + „RL-Absenkung mit Pumpe“ + „HKA59“ modellieren. Hebel (nur Entscheidung der Betreiber): threshold 30 des Klimacontrollers UG – kleiner = kürzere Pausen, mehr Starts. Doku Baustein: https://www.loxone.com/dede/kb/klimacontroller/

## Offen
Verdichterstart-Zeitpunkt und 1490 in den ersten 15 min nach Start (Bitte F54 von 16:05) → Loop 19-Lauf.