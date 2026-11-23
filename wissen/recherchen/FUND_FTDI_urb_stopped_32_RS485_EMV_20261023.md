# FUND: ftdi_sio `urb stopped: -32` am X4-Sniffer, EMV-Verdacht (23.10.2026)

Kontext: Pi liest X4 (Modbus RTU) passiv über FTDI-USB-RS485. Sporadisch `ftdi_sio ... urb stopped: -32`, danach 3-8 min keine Frames. ~10 von 10 Ausfällen fallen auf WW-Umschaltung (Ventil, Verdichterstart, Lüfter).
Nur Recherche, am Pi nichts ausgeführt.

## 1. Belegt (Zitat + URL)

**B1: Was die Meldung im Kernel auslöst** - Linux `drivers/usb/serial/generic.c`, `usb_serial_generic_read_bulk_callback`:
`case -EPIPE:` -> `dev_err(&port->dev, "%s - urb stopped: %d\n", ...)` -> `stopped = true;`
Danach `if (stopped) return;`, d.h. der Lese-URB wird **nicht neu eingereicht**. ENOENT/ECONNRESET/ESHUTDOWN loggen nur auf dev_dbg, EPIPE als einziger Fall auf Fehlerstufe.
https://github.com/torvalds/linux/blob/master/drivers/usb/serial/generic.c
-> -32 = EPIPE = Bulk-IN-Endpoint meldet STALL. Der Kernel liest danach auf diesem Port nichts mehr, bis der Port neu geöffnet wird.

**B2: Neu öffnen startet das Lesen wieder** - gleiche Datei, `usb_serial_generic_open`:
`result = usb_serial_generic_submit_read_urbs(port, GFP_KERNEL);`
In generic.c gibt es **kein** `usb_clear_halt`.
https://github.com/torvalds/linux/blob/master/drivers/usb/serial/generic.c

**B3: Exakt dieselbe Meldung, Ursache war Netz/Kabel** - openHAB, RFXCom an FTDI/Pi:
"ftdi_sio ttyUSB0: usb_serial_generic_read_bulk_callback - urb stopped: -32", dazu am Hub "disabled by hub (EMI?), re-enabling".
Fehler immer zu denselben Uhrzeiten (Tarifumschaltung, Warmwasserbereiter schaltet ein). **Neues USB-Kabel hat es behoben**, ein anderer Port (USB 3) und ein Hub nicht.
https://community.openhab.org/t/rfxcom-stops-sending-or-receiving-any-message-with-error-in-syslog/99339

**B4: RS485/VFD, EMV-Abbrüche** - LinuxCNC, FTDI-RS485 neben Frequenzumrichter:
"usb usb5-port1: disabled by hub (EMI?)". Anderer Adapter half nicht, Ferrit allein half nicht.
**Geschirmtes Kabel, Schirm auf GND am Wandler, plus Ferrit hat es gelöst.**
https://www.forum.linuxcnc.org/38-general-linuxcnc-questions/42943-hy-vfd-ttyusb0-disconnects-reconnects-as-ttyusb1

**B5: Ferrit/Schirmung/Strom** - FHEM USB-Kompendium: "Bad shielding of cables or devices might lead to interferences", Ferritring an den Kabelenden "(semi-confirmed)", aktiver Hub bei Stromproblemen.
https://fhem.de/USB.html

**B6: Isolierter Adapter, Beispiel** - Waveshare USB TO RS232/485 (B): "Onboard original FT232RNL chip", Strom- und Signalisolation, TVS, "15KV ESD protection", 120 Ohm per Jumper. **Isolationsspannung nicht angegeben.**
https://www.waveshare.com/product/usb-to-rs232-485-b.htm

**B7: Abschluss/Bias/Schirm/Hub** - industrialmonitordirect (FTDI Modbus RTU am Pi): "120 Ω at each end", Fail-safe-Bias (Pull-up A, Pull-down B; bei vielen isolierten Boards intern), Schirm nur an einer Seite erden, "Isolated hub plus isolated RS-485 adapter removes ground loops". Ein busgespeister Hub hilft nicht, weil er "draws from the same marginal 5 V rail".
https://industrialmonitordirect.com/it/blogs/knowledgebase/troubleshooting-ftdi-usb-serial-modbus-rtu-rs-485-on-raspberry-pi

**B8: Autosuspend** - kernel.org: "Setting the initial default idle-delay to -1 will prevent any autosuspend of any USB device." Laut Doku steht `power/control` aber schon standardmäßig auf `on` "for all devices other than hubs".
https://www.kernel.org/doc/html/latest/driver-api/usb/power-management.html

**B9: pyserial bei echtem Abstecken** - serialposix.py wirft SerialException: "device reports readiness to read but returned no data (device disconnected or multiple access on port?)".
https://github.com/pyserial/pyserial/blob/master/serial/serialposix.py

**B10: unbind/bind** - rebind-devices: "writing the BUS ID of the device to the unbind and bind files" des Treibers. Elprotronic zeigt dasselbe für den Host-Controller über `sudo tee /sys/bus/pci/drivers/xhci_hcd/unbind`.
https://github.com/bulletmark/rebind-devices
https://elprotronic.atlassian.net/wiki/spaces/GANGFLASHERST/pages/66060293/How+to+reset+USB+devices+-+Linux

## 2. Wahrscheinlich (eigene Ableitung, nicht direkt belegt)
- Der STALL auf dem Bulk-IN kommt sehr wahrscheinlich von einer Störung auf der USB-Strecke (Pi, Kabel, FTDI), nicht vom RS485-Bus. Ein gestörter RS485-Bus liefert Frame-/CRC-Fehler, aber keinen USB-STALL.
- Die Kopplung erfolgt wahrscheinlich über die gemeinsame Masse (GND des X4/Reglers, FTDI, Pi-Netzteil) bei Schaltflanken von Ventil, Verdichter und Lüfter. Galvanische Trennung im Adapter unterbricht genau diesen Pfad.
- pyserial wirft bei `urb stopped` **keine** Exception: Der Port bleibt offen, `read()` liefert nach dem Timeout nur `b''`. Der Hänger ist also nur über "keine Bytes seit X s" erkennbar.
- Die 3-8 min Pause sind wahrscheinlich die Zeit, bis unser eigenes Programm (Timeout, Neustart, systemd-Restart) den Port neu öffnet, siehe B2. Das am Sniffer-Code prüfen.
- Autosuspend ist wahrscheinlich nicht die Ursache, siehe B8. Prüfen: `cat /sys/bus/usb/devices/<dev>/power/control` sollte `on` zeigen.
- Falls das Neuöffnen nicht reicht, weil der Endpoint im Halt bleibt (kein clear_halt in generic.c), hilft ein Gerätereset: `usbreset` (usbutils), `authorized` 0/1 oder unbind/bind. Alle drei brauchen root bzw. sudo, oder eine udev-Regel bzw. sudoers-Eintrag für genau diesen Befehl.

## 3. Nicht gefunden
- Keine offizielle FTDI- oder Kernel-Aussage, *warum* ein FT232 seinen Bulk-IN auf STALL setzt (EMV-Reset des Chips? Glitch auf D+/D-?).
- Ob ftdi_sio beim Open zusätzlich etwas tut, das einen Endpoint-Halt löscht: nicht geprüft.
- Isolationsspannung des Waveshare (B): nicht angegeben.
- Kein Beleg speziell für Hoval-Anlagen bzw. Wärmepumpen als Störquelle (nur analoge Fälle: Warmwasserbereiter, Frequenzumrichter).
- Ob `usbreset` auf Raspberry Pi OS vorinstalliert ist: nicht geprüft.

## 4. Was bringt uns das
- Die Meldung ist eindeutig: Der Kernel stoppt den Lese-URB endgültig. Ohne Neuöffnen kommen keine Daten mehr. Das passt exakt zum Ausfallbild.
- Der Zeitbezug zum Schaltvorgang ist wie beim openHAB-Fall (B3). EMV bzw. Netzstörung über USB-Kabel oder Masse ist der Hauptverdacht.
- Man kann zwei Ebenen getrennt angehen: (a) Störung verhindern (Hardware), (b) schneller erholen (Software, Sekunden statt Minuten).

## 5. Maßnahmen, priorisiert (billig zuerst, nur Vorschläge)
1. **Watchdog im Sniffer**: X4 hat Dauerverkehr. Wenn N s (z.B. 10 s) lang 0 Bytes kommen, `close()` und `open()` des Ports (B2), loggen mit Zeitstempel. Kostet 0 Euro und verkürzt den Ausfall auf Sekunden.
2. **dmesg/journal mitloggen**: `journalctl -k -f` auf `urb stopped`, `disabled by hub (EMI?)`, `disconnect` filtern und mit Hoval-Zeitpunkten korrelieren. Zeigt, ob nur STALL oder auch Port-Reset/Re-Enumeration auftritt.
3. **Kurzes, gutes USB-Kabel** (geschirmt, mit Ferrit) bzw. den Adapter direkt am Pi. Im Fall B3 war das allein die Lösung (ca. 5 EUR).
4. **Klappferrite** auf das USB-Kabel (Pi-seitig) und auf die RS485-Leitung nahe am Adapter (ca. 5 EUR). Allein oft unzureichend (B4).
5. **RS485-Leitung**: verdrillt und geschirmt, Schirm nur einseitig erden (B4/B7), Leitung nicht parallel zu Verdichter-, Lüfter- oder Ventilleitungen führen. Als Sniffer **keinen** zusätzlichen 120-Ohm-Abschluss setzen, wenn der Bus schon terminiert ist (Jumper prüfen). Bias nur, wenn der Bus keinen hat.
6. **Pi-Netzteil**: offizielles 5,1-V-Netzteil, Pi und Adapter möglichst nicht an derselben Steckdosenleiste wie die WP-Steuerspannung.
7. **Galvanisch getrennter USB-RS485-Adapter** (ca. 20-30 EUR), z.B. Waveshare USB TO RS232/485 (B), FT232RNL, Strom- und Signalisolation, TVS (B6). Kriterien: echter FTDI, Isolation von Daten **und** Versorgung, TVS/ESD, schaltbarer Abschluss, GND/Schirm-Klemme.
8. **Alternativ USB-Isolator** (ADuM4160-Klasse, Full Speed 12 Mbit reicht für FTDI) zwischen Pi und dem vorhandenen Adapter, oder aktiver Hub mit eigenem Netzteil (B7). Busgespeist bringt nichts.
9. **Wenn Neuöffnen nicht reicht**: im Watchdog als Stufe 2 `usbreset <VID:PID>` oder unbind/bind über `/sys/bus/usb/drivers/usb/{unbind,bind}` mit der Bus-ID (root nötig, per sudoers auf genau diesen Befehl beschränken).
10. `usbcore.autosuspend=-1` nur als Nebenmaßnahme (B8). Vorher `power/control` prüfen; steht es schon auf `on`, bringt der Parameter nichts.