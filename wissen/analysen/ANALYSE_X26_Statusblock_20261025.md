# ANALYSE X26-Statusblock Obj 0x20: 100 oder 108 Byte? (Katalog F29, Orchestrator 25.10.2026 03:00)

Quelle: passiver X26-Sniffer `~/rs485_sniff/log/rs485_2026-10-22/23/24.log.gz` (Pi <LAN-IP>, nur gelesen, Decoder `~/rs485_sniff/rs485_blk20.py` → `stream`).
Skripte: `[lokaler Pfad]`, `[lokaler Pfad]` (auf dem Pi unter /tmp, Temp-Datei danach entfernt). Nichts gesendet, nichts an Bus/Anlage geschrieben.

## Ergebnis (sicher)
**Obj 0x20 ist live immer 100 Byte – wie Decoder und Firmware V1.11. Die „108 B (0x6C)“ gehören nicht zu Obj 0x20.**

| Tag | Slave-Antworten `40 20 64 20` (Obj 0x20, 100 B) | Slave-Antworten `40 20 6C xx` (108 B) | Objekte xx | `40 20 19 30` (25 B, Obj 0x30) |
|---|---|---|---|---|
| 22.10. | 86 405 (CRC ok) | 86 404 | 0x50..0x5F, je ~5 400 | 218 193 |
| 23.10. | 86 403 | 86 405 | 0x50..0x5F, je ~5 400 | 218 102 |
| 24.10. | 86 405 | 86 403 | 0x50..0x5F, je ~5 400 | 218 139 |

- Obj 0x20 kommt 1×/s (86 400/Tag), Länge in allen 259 213 Rahmen 100 B, keine einzige Abweichung.
- Die 108-B-Rahmen sind die **1-Hz-Werteblöcke Obj 0x50..0x5F** (SPEZ_X26_RS485.md Abschnitt 4: „Variablen-Pollingliste … Antwort var.“). 16 Objekte im Wechsel, jedes ~alle 16 s. Ihre Länge ist live fest 108 B.
- Ende der 108-B-Blöcke (Payload 101..107) in allen Rahmen `ad 00 00 00 80 00 80` (konstant, 2× int16 0x8000 = „ungültig“, wahrscheinlich nicht belegte Pollpaare); Byte 100 wechselt je Objekt.

## Urteil zur Katalogfrage
- Die Prämisse „live 108 statt 100 B“ ist widerlegt: Verwechslung des Längenbytes 0x6C der Objekte 0x50..0x5F mit Obj 0x20. **Kein V1.18.004-Unterschied** beim Statusblock (sicher).
- Es gibt keine 8 Zusatzbytes in Obj 0x20, also nichts zu korrelieren. „Fertig, wenn“: Länge in 3 Tageslogs gezählt ✔, Zusatzbytes als nicht vorhanden belegt ✔ → **erledigt**.
- Nachtrag für die Doku (Vorschlag, nicht ausgeführt): In `SPEZ_X26_RS485.md` bei Obj 0x50..5F die Live-Länge „108 B, 16 Objekte, je ~16 s“ eintragen.

## Was bringt uns das
- Decoder `rs485_blk20.py` und Firmware-Tabelle bleiben gültig, keine Umbauten nötig. Ein vermeintlicher Firmware-Unterschied V1.11 ↔ V1.18.004 ist vom Tisch.
- Nebenbei bestätigt: Der X26-Mitschnitt ist vollständig (86 400 ± 5 Statusrahmen/Tag, CRC ok). Er taugt als lückenlose 1-s-Quelle für F11 (Abtauung).