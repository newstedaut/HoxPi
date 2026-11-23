

| Beleg | Stelle | Sicherheit |
|---|---|---|
| **Live-Gegenprobe:** Timer 0xCA < 0x708 (1800 Ticks) hält die 42-%-Startklemme; live X4 0x0066 am 21.10. 06:36:15–06:39:00 = **180 s** bei 1008 (LIESMICH 21./22.10.). WP011 × 600 Ticks = 15 min ↔ live 7 Pausen exakt 15,0 min (23.10.). | Live | sicher, dass die Tabelle mit 0,1 s zählt (zwei unabhängige Zeitstrecken) |

**Folgerung:** `Timer = Wert × 600` (BV007/BV008) bedeutet **Wert in Minuten**. Mit live 0x8704/05 = 10 → **10 min** Freigabe-/Sperrverzögerung (wahrscheinlich; Zuordnung 0x8704/05 ↔ BV007/008 bleibt wahrscheinlich).

| Befund | Stelle | Sicherheit |
|---|---|---|

**Folgerung:** Einheit **K·min sicher am Code bis auf den Takt; mit (a) wahrscheinlich nahe sicher**. Der Akku zählt nur Minuten mit mehr als 1 K Defizit voll (d, nicht d−1) und fällt bei Überschuss auf 0. BV009 = 180 → Stab-Freigabe nach z. B. 60 min mit 3 K Defizit oder 36 min mit 5 K.

## Was bringt uns das
Die Vorhersage für den W3-Wächter wird schärfer: **Heizstab frühestens, wenn AT < −10 °C (BV002, live) UND das VL-Defizit > 1 K so lange anhält, dass Σ Defizit ≥ 180 K·min** (bzw. 240 im zweiten Satz). Bei unserer 3- bis 5-fach überdimensionierten WP ist ein Defizit > 1 K über Stunden praktisch nur bei Störung/Abtauserie zu erwarten → weiterhin **0 Stab-Einsätze** erwartet (Vorhersage V103c).

## Offen (D-06 Rest)