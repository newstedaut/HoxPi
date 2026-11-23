# Lebenszeit-Bilanz der WP aus X26 Obj 0x20 (Orchestrator 22.10.2026 07:45)

Quelle: RS485-Sniffer `~/rs485_sniff/log/rs485_2026-10-22.log`, `rs485_dump20.py` (nur lesend), Stand 22.10.2026 06:50.

## Zaehlerstaende (sicher, Bytes gelesen)

| Byte | Bedeutung | Wert | Gegenprobe |
|---|---|---|---|
| 47-50 | Waerme Heizen | 72 563 kWh | - |
| 51-54 | Waerme Kuehlen | 522 kWh | - |
| 55-58 | Waerme Warmwasser | 39 946 kWh | Modbus Q_ww 21.10. abends 39 940 |
| 59-62 | Waerme gesamt | 113 032 kWh | = 72 563 + 522 + 39 946 (+1 Rundung) |
| 63-66 | Strom el. | 30 373 kWh | Modbus 25614 E_el 21.10. abends 30 370 |
| 67-70 | Betriebsstunden Verdichter | 14 893 h | (wahrscheinlich, Reihenfolge laut `rs485_blk20.py`) |
| 71-74 | Verdichterstarts | 20 684 | (wahrscheinlich, s. o.) |
| 46 | JAZ x 10 | 38 | Modbus JAZ 3,8 |

## Auswertung seit Inbetriebnahme 08.10.2021 (1840 Tage)

- **Arbeitszahl gesamt 3,72** (113 032 / 30 373). Das Register zeigt 3,8 - wahrscheinlich andere Rechenbasis (z. B. gleitend 12 Monate); nur Vermutung.
- **Waermeanteile:** Heizen 64 %, Warmwasser 35 %, Kuehlen 0,5 %. Pro Jahr im Mittel ~22 400 kWh Waerme, ~6 000 kWh Strom.
- **Taktung:** 11,2 Starts/Tag, 8,1 h Laufzeit/Tag, **mittlere Laufzeit je Start 43 min** (14 893 h / 20 684).
- **Mittlere Leistung im Lauf:** 7,6 kW thermisch / 2,0 kW elektrisch.
- Einordnung zu Oktober 2026 (ANALYSE_Taktschutz/ANALYSE_Arbeitszahl): max. 11 Starts/Tag, AZ Okt 3,84 -> der Oktober liegt im Lebenszeit-Mittel, kein Ausreisser.

## Was bringt uns das

- Ein vom Modbus unabhaengiger, passiv lesbarer Zaehlersatz (X26) inkl. **Betriebsstunden und Starts** - ideal fuer den Winter: Starts/Tag und Laufzeit/Start als Tageswert sagen sofort, ob die Heizkurve oder die Loxone-Anforderung die WP takten laesst.
- Basis fuer einen Wintervergleich: liegt die mittlere Laufzeit je Start an kalten Tagen deutlich unter 43 min, ist das ein Taktproblem (Loxone-Stellantriebe/Holzofen pruefen), nicht die WP.

## Vorschlag (nur Vorschlag, nichts geaendert)

- Loop (lesend): je Tag um 23:59 Bytes 59-74 aus dem X26-Log notieren (Delta Waerme, Strom, Stunden, Starts -> Tages-AZ, Laufzeit/Start). Kein Anlagenzugriff noetig.
- Spaeter (der Betreiber entscheidet): Betriebsstunden/Starts als Datenpunkte in HoxPi/Loxone aufnehmen (Pi-Dienst, nicht Hoval).

## Offen

- Bytes 67-74 (Stunden/Starts) nur aus Plausibilitaet und `rs485_blk20.py`-Doku, Getter dafuer im Atlas noch nicht geprueft.

## Nachtrag 22.10.2026 08:02 (Orchestrator) - Bytes 67-82 jetzt firmwaregeprueft

- **Byte 75-78 / 79-82 = Stunden/Starts Verdichter 2** (idx 2) - an dieser Anlage 0 (einstufig).
- Nebenbei: Byte 45 = momentane Leistungszahl x10 (beim Anlauf 23,8 -> 1,2 binnen 25 s, dann normal), Byte 46 = JAZ x10 (38), Byte 25/26 = Parameter 63 C (b = 2T), Byte 90-91 = Kanal 7 / 10 (uint16, steigt beim Start 0 -> 211 in 25 s; Bedeutung offen, Kandidat el. Leistung/Strom - Vermutung).
- Damit ist der Punkt "Offen: Bytes 67-74 nur aus Plausibilitaet" erledigt. Belege `Emulation\or_stich5*_20261022_08*.out`, `or_emu_stich5*_20261022_08*.out`, `or_live5*_20261022_08*.out`.