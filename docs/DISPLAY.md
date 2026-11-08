# Remote console `/display` / Remote-Konsole `/display`

*Deutsch weiter unten.*

## English

`/display` is a wall-panel style page of the HoxPi dashboard. It is an independent HoxPi view (own drawings, free fonts) and is not affiliated with Hoval AG.

**Without extra setup** it is read-only: values come from the bridge's warm cache (`cache_last.json`, ages from `bridge_state.json`), the parameter catalogue is generated from `registers.json` (official datapoint list). Values older than 10 minutes are greyed out; nothing is ever shown without its age.

**Optional panel daemon** (`panel/hoxpi_panel.py`, service `hoxpi-panel`, files in `~/hoxpi_panel/`): the Pi registers as an additional operating panel on the CAN bus and can query datapoints that are not in the Modbus list. Settings in `config.json`:

| Key | Default | Meaning |
|---|---|---|
| `modus` | `trocken` | `trocken` = sends nothing at all; `live` = panel on the bus |
| `adresse` | `2` | panel address 0–31 — must not be used by a real panel. A foreign heartbeat on this address stops the daemon at once (emergency stop) |
| `nachts_senden` | `false` | cyclic frames 23:00–07:00 |
| `abo_0x44` | `false` | 0x44 subscriptions. **Leave off**: on TopTronic E a subscription can freeze a datapoint until the controller restarts |
| `schreiben_erlaubt` | `false` | allow writes at all |
| `fachmann_code` | empty | code for the page; empty = writing impossible |
| `nachts_schreiben` | `false` | writes 23:00–07:00 |

Writes are limited to the HC1 room setpoints 03-051, 03-053, 03-054 (range-checked), need the code, the dashboard login (2FA, if enabled), are rate-limited, read back with 0x40 and logged in `audit_writes.log`. If the CAN interface is re-created (USB re-enumeration, `can0` restart) the daemon reopens its socket by itself.

Your own catalogue: put a `bedienteil_katalog.csv` (`;`-separated, columns `Pfad;Parameter;Bezeichnung;Wert;Einheit;CAN_Key`) into `~/hoxpi_panel/` — it replaces the generated one.

## Deutsch

`/display` ist eine Seite im Stil eines Wandbedienteils. Eigenständige HoxPi-Ansicht (eigene Zeichnungen, freie Schriften), nicht mit Hoval AG verbunden.

**Ohne weitere Einrichtung** nur lesend: Werte aus dem Warm-Cache der Bridge (`cache_last.json`, Alter aus `bridge_state.json`), der Parameterkatalog wird aus `registers.json` (offizielle Datenpunktliste) erzeugt. Werte älter als 10 Minuten werden grau; kein Wert erscheint ohne sein Alter.

**Optionaler Panel-Dienst** (`panel/hoxpi_panel.py`, Dienst `hoxpi-panel`, Dateien in `~/hoxpi_panel/`): Der Pi meldet sich als zusätzliches Bedienteil am CAN-Bus und kann Datenpunkte abfragen, die nicht in der Modbus-Liste stehen. Einstellungen in `config.json`:

| Schlüssel | Standard | Bedeutung |
|---|---|---|
| `modus` | `trocken` | `trocken` = sendet gar nichts; `live` = Bedienteil am Bus |
| `adresse` | `2` | Bedienteil-Adresse 0–31 — darf von keinem echten Bedienteil belegt sein. Ein fremdes Lebenszeichen auf dieser Adresse schaltet den Dienst sofort ab (Notabschaltung) |
| `nachts_senden` | `false` | zyklische Rahmen 23–7 Uhr |
| `abo_0x44` | `false` | 0x44-Abos. **Aus lassen**: an der TopTronic E kann ein Abo einen Datenpunkt einfrieren, bis der Regler neu startet |
| `schreiben_erlaubt` | `false` | Schreiben überhaupt erlauben |
| `fachmann_code` | leer | Code für die Seite; leer = Schreiben unmöglich |
| `nachts_schreiben` | `false` | Schreiben 23–7 Uhr |

Schreiben geht nur auf die Raum-Sollwerte HK1 03-051, 03-053, 03-054 (mit Bereichsprüfung), braucht den Code und die Dashboard-Anmeldung (2FA, falls aktiv), ist gedrosselt, wird mit 0x40 zurückgelesen und in `audit_writes.log` protokolliert. Wird das CAN-Interface neu angelegt (USB neu erkannt, `can0` neu gestartet), öffnet der Dienst seinen Socket selbst neu.

Eigener Katalog: eine `bedienteil_katalog.csv` (`;`-getrennt, Spalten `Pfad;Parameter;Bezeichnung;Wert;Einheit;CAN_Key`) nach `~/hoxpi_panel/` legen — sie ersetzt den erzeugten.
