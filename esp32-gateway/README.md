# HoxPi-ESP32 — CAN↔Modbus-TCP-Gateway (Firmware-Projekt)

Ziel: HoxPi (Raspberry Pi) durch ein **kleines ESP32-Board mit PoE** ersetzen — ein Kabel
zum Regler, CAN rein, Modbus-TCP für Loxone raus. Der RJ45 des Hoval-Reglers selbst ist tot
(Firmware fährt netif nicht hoch, siehe HoxPi-Doku/RJ45_Netzwerk_Check.md), daher ist so ein
externes Gateway der richtige Weg.

## Hardware (Entscheidung offen, Bernhard bestellt)
- **All-in-one, isoliert:** Waveshare **ESP32-S3-POE-ETH-8DI-8DO** (CAN+RS485+PoE+8I/O), ~60–70 € landed über EU-Händler (BerryBase/reichelt). Siehe Hardware_Gateway_Optionen.md.
- **Günstig, nur CAN:** Olimex **ESP32-EVB** (CAN onboard, ~20 €) + PoE-Splitter, EU, kein Zoll.
- CAN-Transceiver muss 50 kbit/s + Wake unkritisch sein (Standard-Highspeed-CAN-Transceiver ok).

## CAN-Spezifikation (VERBATIM aus hoval_bridge.py — verifiziert live)
- **Bus:** TopTronic-E-CAN, **50 kbit/s**, **Extended IDs (29 bit)**, 64 Ω terminiert. Abgriff am WEZ-Modul (+ ⏚ H L).
- **Opcodes:** `GET=0x40`, `RESPONSE=0x42`, `SET=0x46`.
- **Arbitration-IDs:**
  - `ARB_POLL  = 0x06E40801` → WEZ (UnitId 1) **lesen**
  - `ARB_WRITE = 0x07E40801` → WEZ (UnitId 1) **schreiben**
  - `ARB_HV_POLL = 0x1FE08A08` → HomeVent/Lüftung (UnitId 520, fg=50) **lesen UND schreiben**
    (die WEZ-Schreib-ID wird von der Lüftung ignoriert!)
- **Frame-Aufbau (Datenbytes):** `[0x01, op, fg, fn, dp_hi, dp_lo] (+ value_bytes beim SET)`.
  `dp` = Bedienteilnummer ohne Bindestrich (07-044 → 7044). Antwort: Byte0 des Datenfelds = `0x42`, danach 16- oder 32-bit-Wert (big-endian, S16/U8/S32; 32-bit als High-Word@reg / Low-Word@reg+1).
- **Poll-Rhythmus:** wie die Anlage selbst; Werte nur bei Änderung senden (Modbus-Actor-Prinzip), Kalt-Cache-Schutz beachten.

## Registerkarte / Modbus-Mapping
- Die Zuordnung dp↔Modbus-Register liegt in `registers.json` (wird **lokal** aus Hovals
  Datenpunktliste generiert, NICHT im Repo — Urheberrecht; siehe tools/gen_registers.py).
- Firmware-Ansatz: dieselbe Logik — Registerkarte einmal generieren, als Header/JSON aufs ESP32
  flashen. Kanal-Exklusion (nur ein Sollwert-Register ≠ 0 je Kreis) + Whitelist fürs Schreiben übernehmen.
- Modbus-TCP-Server auf Port 502, FC 3 (lesen) / FC 6/16 (schreiben) — 1:1 wie HoxPi, damit die
  bestehenden Loxone-Hoval-Templates unverändert passen.

## Firmware-Basis (nicht bei null anfangen)
- **nliaudat/esp_canbus** (github.com/nliaudat/esp_canbus) macht Hoval-TopTronic-CAN auf ESP32
  bereits — ESPHome/HA-orientiert. Das ist die Decode-Basis.
- **Für Loxone fehlt der Modbus-TCP-Server** auf dem ESP32 → das ist unser Hauptbeitrag.
  Optionen: ESP-IDF + `esp-modbus` (offizieller Espressif-Modbus-Stack, kann TCP-Slave),
  oder Arduino + eine Modbus-TCP-Lib. TWAI-Treiber (ESP32-CAN) für 50 kbit/s konfigurieren.
- ESP32-S3 (Waveshare) vs klassischer ESP32 (Olimex): TWAI-Pins/Treiber je Board anpassen.

## Bau-Reihenfolge
1. Board bestellen (Bernhard).
2. TWAI/CAN @50k initialisieren, `candump`-Äquivalent → prüfen, dass Hoval-Frames reinkommen.
3. Decode (esp_canbus als Referenz) → Werte im RAM.
4. `esp-modbus` TCP-Slave, Registerkarte anbinden → Loxone liest.
5. Schreibpfad (SET-Frames, ARB_WRITE/ARB_HV_POLL, Whitelist, Kanal-Exklusion).
6. PoE/Netz, Auto-Start, Watchdog. Gegen HoxPi-Werte gegenlesen (beide parallel am Bus möglich, CAN ist multi-master/lauschfähig).

## Projektstruktur (ESP-IDF ≥ 5.3, Stand 02.09.2026)

```
esp32-gateway/
├── CMakeLists.txt, sdkconfig.defaults
├── main/
│   ├── hoval_proto.[ch]     Protokoll, reine C-Bibliothek: GET/SET-Frames, Reassembly (Einzel-/Mehrfachframe,
│   │                        CRC), Dekodierung U8/S8/U16/S16/U32/S32/LIST, 32-bit → 2 Modbus-Wörter,
│   │                        Tabellenzugriff, Whitelist, Kanal-Exklusion — 1:1 aus bridge/hoval_bridge.py
│   ├── hoval_can.[ch]       TWAI @ 50 kbit/s, RX-Task → Reassembly → Register; Poll-Tasks (WEZ 30 s, HomeVent 5 s),
│   │                        Bus-Off-Recovery, „schon vom CAN gelesen"-Bitmap (Kalt-Cache-Schutz)
│   ├── hoval_modbus.[ch]    esp-modbus TCP-Slave :502, ein Holding-Bereich je Registerblock, Schreibpfad =
│   │                        HoxPi-on_write (Whitelist → Kalt-Cache → min/max → Rate-Limit → SET; Exklusion)
│   ├── main.c               Ethernet (RMII-PHY oder W5500/SPI per Kconfig) → IP → Modbus → CAN → Status-Log
│   ├── Kconfig.projbuild    Board (Olimex ESP32-EVB / Waveshare S3-POE / eigenes), Pins, Poll, Port, Schreibfreigabe
│   ├── regmap.c             bindet regmap_gen.h (generiert, nicht im Repo) oder regmap_example.h ein
│   └── regmap_example.h     20 allgemein bekannte Register, damit das Projekt ohne Hoval-Liste kompiliert
├── test/                    Host-Test ohne ESP-IDF: `make test` (gcc) und `make syntax` (Stub-Header)
└── ../tools/gen_esp32_regmap.py   registers.json (+ whitelist.json) → main/regmap_gen.h
```

### Registerkarte erzeugen (lokal, wie bei HoxPi)
```bash
python3 tools/gen_registers.py TTE-GW-Modbus-datapoints.xlsx          # → registers.json (nicht im Repo)
python3 tools/gen_esp32_regmap.py registers.json -w whitelist.json -o esp32-gateway/main/regmap_gen.h
```
Ergebnis bei der aktuellen Liste: **555 Register, 58 davon Low-Wörter von 32-bit-Paaren (strukturell
erkannt, wie in der Bridge), 27 Modbus-Bereiche = 1,5 KB RAM.** `--stats` zeigt nur die Kennzahlen,
`--merge-gap N` fasst Lücken bis N Wörter zu einem Bereich zusammen (Standard 32).

### Bauen
```bash
idf.py set-target esp32        # Olimex ESP32-EVB   (oder: esp32s3 für Waveshare S3-POE-ETH)
idf.py menuconfig              # „HoxPi Gateway": Board, CAN-Pins, Ethernet, Schreibfreigabe
idf.py build flash monitor
```
Ohne `regmap_gen.h` baut CMake mit Warnung die Beispieltabelle ein.

### Testen ohne Hardware
```bash
cd esp32-gateway/test
make test                                # Frames/Dekodierung gegen bridge/hoval_bridge.py (Python-Referenz) + Assertions
make REGMAP=../main/regmap_gen.h test    # dasselbe mit der echten Tabelle
make syntax                              # gcc -fsyntax-only der IDF-Module gegen test/idf_stubs/
```
Stand 02.09.2026: Referenzvergleich **29/29 Zeilen identisch** mit der Python-Bridge (GET/SET-Bytes,
Arbitration-IDs, alle Typen inkl. S16-Negativ, 32-bit-Split), Reassembly-Tests (Einzel-, Mehrfachframe,
Timeout/Verdrängung, Fremd-Devkey) und Tabellen-Tests (Sortierung, Low-Wort-Ausschluss, Bereiche) grün —
mit Beispiel- **und** echter 555er-Tabelle.

## Status / Ehrlichkeit
- **Kein Board vorhanden → kein Hardware-Test.** Protokollkern ist gegen die laufende HoxPi-Bridge
  verifiziert; TWAI-, Ethernet- und esp-modbus-Aufrufe sind nach ESP-IDF-5.3-/esp-modbus-1.0.x-API
  geschrieben und nur per Stub-Syntaxprüfung abgesichert. Erster echter `idf.py build` wird Details zeigen.
- **Pins Waveshare ESP32-S3-POE-ETH(-8DI-8DO) sind Vorbelegungen** aus den Waveshare-ESP32-S3-ETH-Beispielen
  (W5500: MISO 12 / MOSI 11 / SCLK 13 / CS 14 / INT 10 / RST 9; CAN TX 17 / RX 18) — vor dem Flashen mit
  Wiki/Schaltplan abgleichen. Olimex ESP32-EVB: CAN TX 5 / RX 35, LAN8710 PHY 0, MDC 23, MDIO 18.
- **esp-modbus 2.x** hat eine Handle-basierte API (`mbc_slave_create_tcp`, `mbc_slave_start(handle)` …);
  `idf_component.yml` pinnt deshalb `^1.0.15`.
- Offen für die nächsten Schritte: Whitelist zur Laufzeit (NVS statt Kompilat), Web-Status-Seite,
  MQTT/HA-Discovery wie bei HoxPi, OTA.

## Historie
- 01.09.2026 Firmware-Groundwork (dieses README).
- 02.09.2026 Code-Skelett komplett (Protokollkern, CAN, Modbus, Netz, Kconfig), Registerkarten-Generator,
  Host-Testsuite mit Python-Referenzvergleich.
