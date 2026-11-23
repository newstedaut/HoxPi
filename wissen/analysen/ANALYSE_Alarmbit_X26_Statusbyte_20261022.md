# ANALYSE Alarm-Sammelbit 0x10 im X26-Statusbyte - 22.10.2026 (Orchestrator, nur lesend, offline)

Skript: `HoxPi-Doku\or_alarmbit_20261022_0620.py/.out`.

## Ergebnis
- **Sicher (Tabelle):** Formel Modbus 1534 = n + 63 (W:n), n + 127 (B:n), n + 191 (E:n) passt an allen 103 Tabelleneintraegen mit Code, 0 Abweichungen.
- **Sicher (Firmware + Tabelle):** Bit 0x10 im Obj-0x20-Statusbyte wird nur aus den Alarmen Index 0x33..0x9C gebildet (106 Eintraege, 77 davon ohne ERR.LOG-Code).
  Darin: B:03, B:04, B:10, B:20-B:26, B:33, B:34, B:54, B:55, E:04, E:27-E:30, W:19-W:22, W:25-W:27, W:63.
- **Sicher:** Alle bisher im Feld gesehenen Codes liegen **ausserhalb**: E:31 (=222, Idx 0x12), B:63 (=190), B:01, B:02, W:38, W:58; W:61 (=124) steht gar nicht in der Tabelle.
  B:03 und B:10 kommen doppelt vor (je ein Eintrag innerhalb und ausserhalb).
- **Wahrscheinlich:** Bit 0x10 ist ein Sammelbit fuer eine Teilgruppe (Kaeltekreis-/Sensorgruppe der iDM-Kennungen 95-241), keine allgemeine Stoermeldung.

## Was bringt uns das
- Fuer Loxone/HoxPi: **Bit 0x10 aus dem X26-Mitschnitt nicht als Sammelstoerung verwenden** - es haette keinen der bisherigen Fehler (222, 190, 124) gezeigt. Stoermeldung weiter aus Reg 1534 (255 = kein Fehler) ableiten.
- Fehler 222 vom 18.10. 11:11 ist E:31 (Kennung 36) - passt zum bekannten Muster "E:31 nach Neustart" (49 von 76 im ERR.LOG), keine neue Stoerung.

## Offen (Loop, nur lesend)
- Bei der naechsten 1534 != 255-Meldung im RS485-Sniffer (`~/rs485_sniff/log/`) das Obj-0x20-Statusbyte ansehen: Bit 0x10 muss 0 bleiben (Vorhersage).