<img src="logo.svg" alt="HoxPi" width="240">

# HoxPi — open gateway for Hoval® TopTronic® E

[![Buy Me a Coffee](https://img.shields.io/badge/☕-Buy%20me%20a%20coffee-ffdd00)](https://buymeacoffee.com/bernhardsu9)

**Raspberry Pi + USB-CAN adapter = a drop-in replacement for the Hoval Modbus gateway.**
HoxPi passively reads the CAN bus of a Hoval® TopTronic® E system (heat pump, ventilation, buffer module) and exposes every datapoint as **Modbus-TCP (port 502)** — exactly like the original HovalConnect Modbus gateway. The official **Loxone Hoval templates work 1:1**, Home Assistant gets a ready-made config, and an optional **Grafana stack** provides long-term charts. Entirely local, no cloud.

> **Disclaimer:** Independent open-source project, **not affiliated with Hoval AG**. Hoval® and TopTronic® are trademarks of Hoval AG. Use at your own risk — you are interfacing with your own heating system.

## Features

- **Modbus-TCP gateway emulation** — register numbers match the official Hoval datapoint list, so the official Loxone Library templates (Heating & Cooling, Ventilation, Energy Management) work without modification
- **Safe writing**: default read-only; writes require an explicit per-register whitelist **plus** value-range check, rate limit and cold-cache protection
- **Web dashboard** (port 80, DE/EN): live values in plain language, all registers with descriptions (hover tooltips), sortable/searchable register table with **write-permission checkboxes**, integration guide, network/IP configuration
- **Home Assistant**: auto-generated Modbus package (`hoxpi.yaml` download) + optional MQTT with auto-discovery
- **Grafana statistics** (optional, can be toggled on/off in the dashboard): Prometheus exporter → Prometheus (400 days retention) → provisioned Grafana dashboard (temperatures, power, COP, Smart Grid, daily energy)
- **SG-Ready / PV surplus**: full support for Hoval's Smart Grid offset registers (Use Case 8 of the Hoval Modbus guideline)

## Hardware

| Part | Note |
|---|---|
| Raspberry Pi 4 | 2 GB RAM is plenty |
| USB-CAN adapter | tested: DSD-TECH SH-C30G |
| microSD ≥ 16 GB, PSU 5 V/3 A | PoE splitter works too |

CAN wiring: tap the bus **in parallel** at the Hoval **WEZ module**, terminal "+ ⏚ H L" (H/L/GND). The existing bus keeps running — HoxPi listens passively and polls politely. **Do not** use terminal X4 (that is RS-485, not CAN).

## Install

```bash
git clone <this repo> && cd hoxpi
sudo bash install.sh
```

The installer asks to download the **official Hoval datapoint list** (xlsx) from hoval.com — it is **not** included in this repository for copyright reasons. Two small generators (`tools/gen_registers.py`, `tools/gen_reg_texts.py`) build `registers.json` (register map) and `reg_texts.json` (names + descriptions DE/EN) from it locally.

## Security notes

- Run **only in a trusted home network**: the dashboard has no login (yet); the register write-permission page and the IP configuration would otherwise be exposed
- Writing starts disabled except for a small, curated whitelist; every write is additionally validated (range, rate limit, cold-cache)
- Nothing leaves your network — no cloud, no telemetry

## Credits

Protocol knowledge builds on the great reverse-engineering work of
[hpoeckl/hoval-exporter](https://github.com/hpoeckl/hoval-exporter) (MIT),
[zittix/Hoval-GW](https://github.com/zittix/Hoval-GW),
[chrishrb/hoval-gateway](https://github.com/chrishrb/hoval-gateway) (Apache-2.0) and
[parren/hoval-ultrasource-agent](https://github.com/parren/hoval-ultrasource-agent) (MIT).
No code was copied from these projects; HoxPi is an independent implementation.

## Support

HoxPi is free and develops in my spare time. If it saves you the commercial gateway, consider [buying me a coffee ☕](https://buymeacoffee.com/bernhardsu9) — it funds test hardware and keeps the project going.

## License

[MIT](LICENSE)

---

# HoxPi — offenes Gateway für Hoval® TopTronic® E (Deutsch)

**Raspberry Pi + USB-CAN-Adapter = Ersatz für den Hoval-Modbus-Gateway.**
HoxPi liest den CAN-Bus einer Hoval® TopTronic® E-Anlage (Wärmepumpe, Wohnraumlüftung, Puffermodul) passiv mit und stellt alle Datenpunkte als **Modbus-TCP (Port 502)** bereit — exakt wie der originale HovalConnect-Modbus-Gateway. Die offiziellen **Loxone-Hoval-Templates laufen 1:1**, Home Assistant bekommt eine fertige Konfiguration, optional gibt es einen **Grafana-Stack** für Langzeit-Diagramme. Komplett lokal, keine Cloud.

> **Hinweis:** Unabhängiges Open-Source-Projekt, **nicht mit der Hoval AG verbunden**. Hoval® und TopTronic® sind Marken der Hoval AG. Nutzung auf eigene Gefahr — es geht um deine Heizung.

## Funktionen

- **Modbus-TCP-Gateway-Emulation** — Registernummern exakt nach offizieller Hoval-Datenpunktliste, offizielle Loxone-Templates (Heating & Cooling, Ventilation, Energy Management) passen ohne Anpassung
- **Sicheres Schreiben**: standardmäßig read-only; Schreiben nur per Register-Whitelist **plus** Wertebereichsprüfung, Rate-Limit und Kalt-Cache-Schutz
- **Web-Dashboard** (Port 80, DE/EN): Live-Werte in Klartext, alle Register mit Beschreibung (Maus-Tooltip), sortier- und durchsuchbare Registertabelle mit **Schreibfreigabe-Checkboxen**, Integrations-Anleitung, Netzwerk-/IP-Konfiguration
- **Home Assistant**: automatisch erzeugtes Modbus-Package (`hoxpi.yaml`-Download) + optional MQTT mit Auto-Discovery
- **Grafana-Statistik** (optional, im Dashboard ein-/ausschaltbar): Exporter → Prometheus (400 Tage) → fertiges Grafana-Dashboard (Temperaturen, Leistung, COP, Smart Grid, Tagesenergie)
- **SG-Ready / PV-Überschuss**: volle Unterstützung der Hoval-Smart-Grid-Offset-Register (Use Case 8 der Hoval-Modbus-Guideline)

## Installation

```bash
git clone <dieses Repo> && cd hoxpi
sudo bash install.sh
```

Der Installer fragt nach der **offiziellen Hoval-Datenpunktliste** (xlsx) von hoval.com — sie ist aus Urheberrechtsgründen **nicht** im Repo enthalten. Zwei Generatoren (`tools/`) erzeugen daraus lokal `registers.json` und `reg_texts.json` (Namen + Beschreibungen DE/EN).

## Sicherheit

- **Nur im vertrauenswürdigen Heimnetz betreiben** — das Dashboard hat (noch) keine Anmeldung
- Schreiben ist ab Werk auf eine kleine, geprüfte Whitelist beschränkt; jeder Write wird zusätzlich validiert
- Es verlässt nichts dein Netzwerk — keine Cloud, keine Telemetrie

## Danksagung

Das Protokoll-Wissen baut auf der Reverse-Engineering-Arbeit von
[hpoeckl/hoval-exporter](https://github.com/hpoeckl/hoval-exporter) (MIT),
[zittix/Hoval-GW](https://github.com/zittix/Hoval-GW),
[chrishrb/hoval-gateway](https://github.com/chrishrb/hoval-gateway) (Apache-2.0) und
[parren/hoval-ultrasource-agent](https://github.com/parren/hoval-ultrasource-agent) (MIT) auf.
Es wurde kein Code übernommen — HoxPi ist eine eigenständige Implementierung.

## Unterstützen

HoxPi ist kostenlos und entsteht in meiner Freizeit. Wenn es dir den kommerziellen Gateway erspart: [Spendier mir einen Kaffee ☕](https://buymeacoffee.com/bernhardsu9) — das finanziert Test-Hardware und hält das Projekt am Leben.

## Lizenz

[MIT](LICENSE)
