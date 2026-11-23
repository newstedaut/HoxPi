# FUND lox-Releases 15.11.2026 20:56 (2 neu, davon 2 skill-relevant)
Quelle: https://github.com/discostu105/lox/releases (nur gelesen). Skill-relevant = Stichwort aus config diff, config push, config pull, decompile, loxl, lox logic, simulator, mcp, loxone-config, adopt, drift, types.

## discostu105/lox v0.84.0 (2026-11-14T23:17) [SKILL-RELEVANT]
## ✨ New

- **`lox update install`** waits until the Miniserver runs the new firmware and prints progress. `--no-wait` returns right away.
- **`lox update check`** names the matching Loxone Config download and warns about a Remote Connect deadline. In a Lox Logic project it warns when the base was saved by another Loxone Config version.
- **`lox update check`** finds the serial without `lox setup set --serial`: from `lox.toml`, or from the Miniserver's MAC address.

## 🚀 Improvements

- **Release binaries** are a quarter smaller: they ship without symbols.

## 🐛 Bug Fixes

- **`verify_ssl: true`** works. The HTTPS client had no root certificates, so a verified connection always failed. `lox update check` and `lox otel` with an HTTPS endpoint failed for the same reason.
- **Commands are sent once.** After a lost answer lox sent `pulse` and other commands again, up to three times. `lox reboot`, `lox update install` and the restart of `lox config push` are sent once too.
- **A refused command is an error.** `lox on`, `off`, `blind`, `gate` and the other control commands printed `✗` and exited 0 when the Miniserver answered with a code other than 200.
- **`lox ctx add`** keeps a single-Miniserver config: it asks for `lox ctx migrate` first instead of replacing it. `lox ctx` and `lox setup set` leave a config they cannot read as it is.
- **`lox setup set`** with another host or user drops the structure cache and the token of the old one.
- **`lox otel serve`** stops on SIGTERM and sends what is pending, and reconnects when the Miniserver stalls during login.
  - The SD card test runs every 10 minutes at most. It ran on every export and wrote to the card each time.
  - `--interval 0` is rejected.
- **`lox config pull`, `push` and `download`** no longer hang on a Miniserver that stops answering over FTP. A failed listing is an error instead of "no configs", and a rejected login is tried once.
- **`lox reboot`, `lox update install` and `lox music`** honour `--dry-run`.
- **`lox update check -o json`** prints JSON only.
- **`lox history`** reports an answer that is not a statistics file instead of crashing.
- **`lox light color`** rejects a malformed value. `#1ä234` crashed.
- **`lox schema`** names flags as the command line takes them (`--all-in-room`) and lists every global flag.
- **`lox --help`** lists `tui`.
- **`lox logic … | head`** and `loxl … | head` end quietly instead of panicking.
- **`lox watch -i 0`** is rejected instead of polling without a pause.
- **`lox logic compile`** finds the ports of an extern by the names `lox logic adopt` writes. On block types such as AnalogScaler, RSFlipFlop or Memory it failed with "has no port `In`", although the list it printed named `In`.
- **`lox logic compile`** keeps `Valid="true"` on a formula whose text did not change. Loxone Config checks a formula only when its text is edited, so every compiled formula showed as invalid.
- **`LOX_HOST`, `LOX_USER`, `LOX_PASS` and `LOX_SERIAL`** work for every command, as documented. They were read by `lox setup set` only. Without a config file the first three are enough, for containers and CI. Commands that save the config never write them into it.
- **`lox update check`** reads the release version from Loxone's answer. It printed "Update available: 1.0" or "check Loxone Config for details" instead of the version on offer.
- **The global `~/.lox/config.yaml`** is no longer mistaken for a project-local config when the home directory path contains a symlink, as on macOS under `/var`.

## 🔒 Security

- **`lox mcp`** keeps every command on its control. A value such as `../<uuid>/open`, given as a color, a raw command or an alarm code, reached another control or a system endpoint without the confirmation. `lox send`, `lox light color` and the TUI are covered too.
- **`lox run`** and the MCP `run_scene` tool take a scene name only. A path ran any YAML file as a scene.
- **`lox cache refresh`** honours `verify_ssl: true`. It sent the password without checking the certificate.
- **Dependencies** are updated to patched versions of rustls, tokio, rmcp and others. `cargo audit` runs in CI.
- **`install.ps1`** checks the download against the release's SHA256 file before it installs.
- **`config.yaml`**, the token and the caches are written readable by you only, in one step. Before, the config was readable by others for a moment each time it was saved, and the cached program file stayed readable.


## What's Changed
* Review: security, stability, dependencies, CI; fix #397 and #398 by @discostu105 in https://github.com/discostu105/lox/pull/399
* update: read the real update-server answer, wait for the new firmware by @discostu105 in https://github.com/discostu105/lox/pull/408


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.83.0...v0.84.0

## discostu105/lox v0.85.0 (2026-11-15T18:52) [SKILL-RELEVANT]
## ✨ New

- **Lox Logic: project and Miniserver settings from source.** `extern haus = Document(…)` and `extern ms = LoxLIVE(…)` take settings: location and time zone, time server, currency, the automatic updates (`haus.Updates = "confirm"`, `haus.UpdateTime = 02:00`), the application firewall, password reset, extended login, the LOXONE Log, and where the Miniserver is mounted. Withdrawn, each goes back to what it was.


## What's Changed
* Lox Logic: project and Miniserver settings from source by @discostu105 in https://github.com/discostu105/lox/pull/410


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.84.0...v0.85.0
