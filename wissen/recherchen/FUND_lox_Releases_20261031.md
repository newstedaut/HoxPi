# FUND lox-Releases 31.10.2026 21:47 (16 neu, davon 14 skill-relevant)
Quelle: https://github.com/discostu105/lox/releases (nur gelesen). Skill-relevant = Stichwort aus config diff, config push, config pull, decompile, loxl, lox logic, simulator, mcp, loxone-config, adopt, drift, types.

## eisber/lox-cli v0.12.0 (2026-04-30T17:44)
**Full Changelog**: https://github.com/eisber/lox-cli/commits/v0.12.0

## discostu105/lox v0.44.0 (2026-10-31T13:13) [SKILL-RELEVANT]
The config-as-code language has a name of its own: Lox Logic, written in `.loxl` files and run as `lox logic` or `loxl`. Its library crate is loxone-config now (formerly lxir).

## 🚀 Improvements

- **lox logic**: `lox ir` is now `lox logic` (`lox loxl` works too); the language is called Lox Logic and its files end in `.loxl` instead of `.lxir`. The standalone binary is `loxl` (was `lxir`), a new project's lockfile defaults to `logic.lock.json`, the env vars are `LOXL`/`LOXL_CORPUS`, and the editor extension and agent skill are named `loxl` and `lox-logic`. Existing lockfiles and fingerprints stay valid; rename your `.lxir` files to `.loxl`.
- **loxone-config 0.3.0** (on crates.io): the lxir crate is renamed to loxone-config (`use loxone_config::…`; the `ir` module is `logic`, `Error::IrParse` is `Error::Parse`). The last lxir release points to it.


## What's Changed
* Rename lxir to Lox Logic (lox logic, .loxl, loxl) and the crate to loxone-config by @discostu105 in https://github.com/discostu105/lox/pull/221


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.43.0...v0.44.0

## discostu105/lox v0.45.0 (2026-10-31T13:52) [SKILL-RELEVANT]
Automatic Designer rules can watch states and operating modes, combine conditions with `or` and switch modes; the *Betriebszeiten* calendar is managed from source; and `loxl scan --redact` makes a config safe to share.

## ✨ New

- **lox logic rules**: conditions on control states (`when pumpe.active == on`, `when temp.value > 25`) and operating modes (`when mode "Heizperiode"`), `or` between condition groups, and `then mode <mode> on|off`; a `then` takes every command the app offers for the block. The codes come from the Miniserver's own Automatic Designer table. Compiles keep the AutoPilot container's inputs as Loxone Config saves them.
- **lox logic**: calendar entries (*Betriebszeiten*) from source: `CalendarEntry("Sommerferien", CalType: 2, Mode: 3, From: 6393, To: 6456)`, fixed dates, Easter-relative days, periods and yearly ranges; existing entries are taken over with `adopt --uuid`.
- **lox logic scan --redact**: `loxl scan --redact <cfg> --out <copy>` writes a copy of a config with all personal data and serials replaced, to share in an issue.

## 🚀 Improvements

- **lox logic adopt --uuid**: promoting an extern keeps its room, category and schedule claims (they move to the block); only a tiles claim is still refused.

## 🐛 Bug Fixes

- **lox logic decompile --out-dir**: a page whose rules drive blocks on other pages declares them as externs instead of failing with "undeclared slug".
- **lox config push**: operating modes made in source appear in the app (`operatingModes`), and renamed or deleted ones follow.


## What's Changed
* Lox Logic: rule states, modes and or, calendar entries, scan --redact (D73–D75) by @discostu105 in https://github.com/discostu105/lox/pull/222


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.44.0...v0.45.0

## discostu105/lox v0.46.0 (2026-10-31T16:13) [SKILL-RELEVANT]
## ✨ New

- **Example library** of real Loxone Config projects in `crates/loxone-config/examples/library/`: each with its source, license, Lox Logic view and page drawings, so you can see what a config looks like as code

## 🐛 Bug Fixes

- **`loxl scan`** (and `lox logic scan`) also finds the project's creator and phone number in the document properties, and `--redact` replaces them; before, a shared copy kept both


## What's Changed
* docs: discostu105/lxir is archived by @discostu105 in https://github.com/discostu105/lox/pull/223
* External references, pinned config corpus and an example library by @discostu105 in https://github.com/discostu105/lox/pull/228


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.45.0...v0.46.0

## discostu105/lox v0.47.0 (2026-10-31T16:33) [SKILL-RELEVANT]
Automatic Designer rules can react to the weather, the day of the month, daylight, sunrise and sunset and a date, and send push notifications, mails and message-center entries with pauses in between. Existing user operating modes are taken over with `adopt --uuid`.

## ✨ New

- **lox logic rules**: conditions `when weather temperature > 25` (and the other fields of the weather service), `when day >= 15`, `when daylight [off]`, `when sunrise|sunset|dawn|dusk` and `when date "2026-12-24"`; actions `then notify "<subject>" "<text>"`, `then mail "<to>" "<subject>" "<text>"`, `then wait 2.5s` and `then message warning "<subject>" "<text>" [admins]`. Compiles wire the weather, day and daylight blocks into the AutoPilot container as Loxone Config does.

## 🚀 Improvements

- **loxone-config 0.4.0** (on crates.io): a smaller public API. Internal modules (`autopilot`, `blockdoc`, `coverage`, `periphery`, `port_meta`, `scan`, `settings`) are private now, the ones only `loxl`, lox and the tests use (`cli`, `lsp`, `library`, `observed_defaults`, the older `semantic_fingerprint_v*` forms) are hidden from the docs, and `Module`, `CompileOptions` and `DocDiff` are re-exported at the top. The program-file modules no longer depend on the Lox Logic ones (`lock::Attr`, formerly `logic::Attr`, which still re-exports it).
- **lox logic adopt --uuid**: documented for user operating modes made in Loxone Config: the mode keeps its uuid and `Mode=` number, a new title renames it.

## 🐛 Bug Fixes

- **lox logic compile**: the "past the edge of the A3 sheet" warning lists only objects the compile placed, not ones laid out that way in Loxone Config (whose `--relayout` would rearrange the page).


## What's Changed
* lox logic rules: weather, dates, notifications, mail, pauses (D76) by @discostu105 in https://github.com/discostu105/lox/pull/230
* loxone-config 0.4.0: one-way layering, smaller public API by @discostu105 in https://github.com/discostu105/lox/pull/229


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.46.0...v0.47.0

## discostu105/lox v0.48.0 (2026-10-31T17:01) [SKILL-RELEVANT]
## ✨ New

- **`lox energy flow`** breaks down the energy flow right now: production, consumption, grid import/export, battery charge/discharge and state of charge, read from the Energy Flow Monitor (`-o json` adds every node)
  - **`lox energy --top [N]`** ranks the meters by current power, highest first (default 10)
  - MCP: the new `get_energy_flow` tool returns the same breakdown; `top` adds the meter ranking
  - `lox tui` and `lox energy flow` share one interpretation of the monitor's nodes and roles (`roles:` in `~/.lox/tui.yaml` applies to both); `lox energy` now lists the flow monitor (type `EFM`) too

## 🐛 Bug Fixes

- **`lox logic compile`** no longer rewrites the Automatic Designer's watch list when no rule changed, so compiling the rules a config already has reproduces it byte for byte; `OutputAPI` of `LightController2` and `MeterAbsSt` takes wires in both directions (API links), as the public corpus shows


## What's Changed
* Energy flow breakdown and meter ranking (lox energy flow, --top) by @discostu105 in https://github.com/discostu105/lox/pull/234
* Corpus fixpoints: OutputAPI API links, rule watch list, access test by @discostu105 in https://github.com/discostu105/lox/pull/232


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.47.0...v0.48.0

## discostu105/lox v0.48.1 (2026-10-31T17:11) [SKILL-RELEVANT]
## 🐛 Bug Fixes

- **`lox logic decompile`** no longer prints a stale constant under a wire as a second argument for the same port (`Input1: 2, Input1: x.AQ`): the wire stays the argument and the constant becomes a comment on it, and `lox logic compile` keeps it in the config. **`lox logic check`** refuses a port bound to both a value and a wire, with the error on the port in the call (#226)


## What's Changed
* lox logic: a stale constant under a wire is a comment, not a duplicate argument (D77) by @discostu105 in https://github.com/discostu105/lox/pull/233


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.48.0...v0.48.1

## discostu105/lox v0.49.0 (2026-10-31T17:28) [SKILL-RELEVANT]
## ✨ New

- **lox mcp serve**: `get_wiring` takes `live: true` and fills in the current value on every wire whose source the app streams, plus the control's own value in its app format (`22000lx`), so an assistant answers "why is this light on?" in one call
  - One WebSocket state read for all wires; a wire without a streamed source gets no value, and a failed read leaves the config wiring with a `live_error`


## What's Changed
* MCP get_wiring: live values on the wires by @discostu105 in https://github.com/discostu105/lox/pull/231


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.48.1...v0.49.0

## discostu105/lox v0.50.0 (2026-10-31T17:55) [SKILL-RELEVANT]
## ✨ New

- **loxone-config** example library: five typical scenarios made for this repository with Loxone Config 17.2 from its factory default project (lighting with presence and moods, automatic shading with weather station and wind alarm, an intelligent room controller with window contact, an NFC Code Touch with users and access codes, an energy flow monitor with PV surplus to a heating rod), each with its Lox Logic view and page drawing
- **`loxl scan --redact`** gives each distinct name its own placeholder (`redacted`, `redacted-2`, …), so redacted users stay apart and their access rights still lift


## What's Changed
* Example library: five scenarios made for this repository by @discostu105 in https://github.com/discostu105/lox/pull/235


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.49.0...v0.50.0

## discostu105/lox v0.50.1 (2026-10-31T18:23) [SKILL-RELEVANT]
## ✨ New

- **loxone-client 0.1.1** (on crates.io): typed reads of the system state — `LoxClient::system_status()` (firmware, PLC state, heap), `heap()`, `diagnostics()` (CPU and PLC load, tasks, interrupts, context switches) and `value(path)` for any `LL` value, with the parsers public in `loxone_client::system`.

## 🚀 Improvements

- **loxone-config 0.5.0** (on crates.io): the D76 rule conditions and actions (weather, day, daylight, sun, date; notify, mail, wait, message) and D77 (a stale constant under a wire) for library users. The rule enums in `logic` gained variants, so exhaustive matches need new arms.
- **lox status --diag**: shows the PLC's CPU share next to the CPU load; the JSON reports `cpu`, `sps`, `tasks` and the counters as numbers (`null` when the Miniserver leaves them empty). `lox status`, the TUI, `lox otel` and the MCP `system_status` tool now read the system state through the same loxone-client calls.

## 🐛 Bug Fixes

- **loxl decompile/adopt**: the *Rest* meter an energy flow monitor creates for itself is part of the monitor, no longer a top-level `rest = MeterAbsBi()` block; adopting it alone is refused (D78, #236).
- **lox otel**: `loxone.system.cpu` is recorded again on current firmware (`CPU:12 SPS:26` read as no value).


## What's Changed
* loxone-config 0.5.0 by @discostu105 in https://github.com/discostu105/lox/pull/237
* loxl: an energy flow monitor's own meter stays with it (D78) by @discostu105 in https://github.com/discostu105/lox/pull/240
* loxone-client: typed system reads, shared by CLI, TUI, MCP and OTel by @discostu105 in https://github.com/discostu105/lox/pull/238


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.50.0...v0.50.1

## discostu105/lox v0.51.0 (2026-10-31T18:52) [SKILL-RELEVANT]
## ✨ New

- **`lox config push`** keeps the push settings of registered phones: when someone changes which notifications their phone receives in the Loxone app, the Miniserver holds that as a custom change, and the push used to refuse (or, with `--discard-custom-changes`, silently reset the phone, which then got no notifications). Now the push carries these changes into the upload (`custom_changes_kept` in `-o json`); other custom changes still refuse


## What's Changed
* inventory.rs: shared reads out of commands/, and the front-end rule in AGENTS.md by @discostu105 in https://github.com/discostu105/lox/pull/239
* config push: keep the push settings of registered phones by @discostu105 in https://github.com/discostu105/lox/pull/243


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.50.1...v0.51.0

## discostu105/lox v0.52.0 (2026-10-31T19:08)
## ✨ New

- **`lox input set/pulse`** reach virtual inputs that are not shown in the app by name: a name that matches no control is looked up among the virtual inputs of the config (config repo or cached download), e.g. `lox input pulse "Test Frostwarnung"`


## What's Changed
* lox input: virtual inputs not shown in the app, by name by @discostu105 in https://github.com/discostu105/lox/pull/241


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.51.0...v0.52.0

## discostu105/lox v0.52.1 (2026-10-31T19:55) [SKILL-RELEVANT]
## ✨ New

- **loxone-client 0.1.2** (on crates.io): more typed reads — `LoxClient::network()` (IP, mask, gateway, DNS, MAC, DHCP, NTP), `bus_stats()` (CAN bus counters), `lan_stats()` (LAN counters), `sdtest()` (the parsed SD card test) and `log()` (the system log, with a clear error when the user isn't an administrator), plus `check_ll()` for the `Code` of a command's answer. `lox status`, the TUI and `lox otel` now read these through the client instead of each keeping its own list of endpoints.

## 🚀 Improvements

- **`lox status --bus/--lan -o json`**: the counters are numbers (`"overruns": 0`), and `null` when the Miniserver leaves one empty, as with `--diag`.


## What's Changed
* loxone-client: network, bus, LAN, SD card and log reads, shared by CLI, TUI and OTel by @discostu105 in https://github.com/discostu105/lox/pull/244
* Move each command's clap enum next to its handler; shrink main.rs by @discostu105 in https://github.com/discostu105/lox/pull/245
* loxone-config: split compile, validate, parse and decompile into phases by @discostu105 in https://github.com/discostu105/lox/pull/247


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.52.0...v0.52.1

## discostu105/lox v0.53.0 (2026-10-31T20:07) [SKILL-RELEVANT]
## ✨ New

- **`lox logic test --trace`** (also `loxl test --trace`) prints each test cycle by cycle: what a step sets, every change of the ports its expectations depend on, named by slug, and each `expect` with its actual value. A failing run without it points to the flag.


## What's Changed
* loxl test --trace: each test cycle by cycle by @discostu105 in https://github.com/discostu105/lox/pull/246


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.52.1...v0.53.0

## discostu105/lox v0.54.0 (2026-10-31T20:22) [SKILL-RELEVANT]
## ✨ New

- **`lox logic test`** (also `loxl test`) simulates more of a real house: the push switch (`Switch2Button`), pulse at a time of day (`PulseAt`), the fixed value meter, meter and bidirectional meter (power and meter reading), automatic shading (`AutoJalousie`: complete open/close by run time, position, wind alarm, window contact, Off/lock, slightly open) and the lighting controller (`LightController2`: its motion mood from motion or presence below the brightness threshold, the extend time, Off/lock and the automatic timeout after a manual off). What Loxone does not document, such as the sun automatic, slats or mood stepping, stops the test with an error naming the input
- **`loxl types`** shows the canvas labels of these blocks' inputs (`EndUp` is Co, complete open), read off Loxone Config

## 🐛 Bug Fixes

- **`loxl types MeterDig`** describes the fixed value meter it is, not a pulse meter; `Switch2Button` is the push switch (a pulse on each edge), not a toggle


## What's Changed
* Simulator: push switch, pulse at, meters, automatic shading, lighting controller by @discostu105 in https://github.com/discostu105/lox/pull/252


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.53.0...v0.54.0

## discostu105/lox v0.55.0 (2026-10-31T20:39) [SKILL-RELEVANT]
## ✨ New

- **`lox logic`: a PulseAt's fire time in the source** — `At: 19:00` (or `06:58:30`) on a `PulseAt` sets the time of day it fires, which used to come only from Loxone Config (#248)
  - `adopt` and `decompile` write it out, `fmt` normalizes it (`6:58` → `06:58`), `lox logic types PulseAt` lists it, and `diff` shows a change as `At: 18:58 -> 06:58`; `drift` now sees a changed fire time too
  - Without `At:` the time is carried from the base as before, so existing sources compile unchanged. A block set to a time function (sunrise, hour pulse) in Loxone Config refuses `At:`
- **`lox logic coverage`** lists, per managed block type, the attributes the compile still carries from the base instead of writing them from source, with the parameter that claims one where Lox Logic has it
- **loxone-client 0.1.3** (on crates.io): `loxone_client::system::code_of()` reads the `Code` of a parsed `LL` answer in both forms (Gen 1 string, Gen 2 number); `lox`'s commands, MCP server, user management and NFC learning use it instead of their own copies.

## 🐛 Bug Fixes

- **`lox set`**: a Gen 2 Miniserver's answer (`"Code": 200` as a number) is no longer reported as `Error ?`.


## What's Changed
* One reader for the Code of an LL answer; lox set on Gen 2 fixed by @discostu105 in https://github.com/discostu105/lox/pull/255
* Lox Logic: PulseAt fire time from source (At: HH:MM); carried attributes in coverage by @discostu105 in https://github.com/discostu105/lox/pull/254


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.54.0...v0.55.0
