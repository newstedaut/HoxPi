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

## Status
Firmware-Groundwork angelegt 01.09.2026. Hardware noch nicht bestellt. Sobald ein Board da ist
(oder als Trockenübung im Simulator), kann die Umsetzung starten — der Loop kann Schritte 2–5
inkrementell vorbereiten (Code-Skelett, esp-modbus-Beispiel, Registerkarten-Generator fürs ESP32).
