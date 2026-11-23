# FUND lox-Releases 01.11.2026 20:55 (15 neu, davon 15 skill-relevant)
Quelle: https://github.com/discostu105/lox/releases (nur gelesen). Skill-relevant = Stichwort aus config diff, config push, config pull, decompile, loxl, lox logic, simulator, mcp, loxone-config, adopt, drift, types.

## discostu105/lox v0.68.1 (2026-11-01T09:35) [SKILL-RELEVANT]
## 🐛 Bug Fixes

- **`loxl compile`** writes `Signed: off`, `Analog: off` and `CloseAfterSend: off` on virtual commands and outputs as no attribute, the way Loxone Config stores an unticked box, so a save no longer shows them as changed. A virtual input's `Analog: off` stays `Analog="false"`, which Loxone Config writes too.


## What's Changed
* loxl: off on virtual commands and outputs is no attribute by @discostu105 in https://github.com/discostu105/lox/pull/313
* Docs: hardware in scope, pairing stays in Loxone Config by @discostu105 in https://github.com/discostu105/lox/pull/325


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.68.0...v0.68.1

## discostu105/lox v0.69.0 (2026-11-01T10:59) [SKILL-RELEVANT]
Tree and Air devices, with their inputs and outputs, can now be taken over in Lox Logic. Pairing stays in Loxone Config.

## ✨ New

- **`loxl compile`** takes over existing hardware by declaration: `taster = TreeDevice("Taster", serial: "…")` and `klingel = TreeSensor("Klingel", device: taster, iname: "I0", …)`. The source owns the title, room, category and the settings it states, including `Statistics: on`/`off`. Tree and Air devices and their inputs and outputs, and the Tree and Air extensions, are supported. Removing a declaration leaves the hardware as it is.
- **`loxl adopt --uuid <device>`** declares a Tree or Air device with every input and output below it.
- **`extern … (serial: "…")`** matches a device by its own serial.

## 🚀 Improvements

- **`loxl lint`** reports bare durations also on extern port assignments (`x.TimeEnd = 120`), template value parameters and instance arguments, and `--fix` writes their units across the files of a module. The compiled config does not change.
- **Lox Logic** knows the units of the Virtual HTTP Input from Loxone's documentation: `Poll` in seconds, `Timeout` in milliseconds (`Timeout: 4s` compiles to `4000`). Modbus settings have no documented unit and stay bare numbers.

## 🐛 Bug Fixes

- **`loxl compile`** writes a 0 on a setting such as `MinVal`, `ModbusDataType` or a calendar entry's `CalType` as no attribute, the way Loxone Config stores it, so a save no longer shows it as changed. Adopt writes such a missing setting as 0 where a new object would get another default.
- **`loxl types`** and the LSP hover no longer link Greater and Less to the Comparator page of the Loxone knowledge base, which documents another block. The knowledge base has no page for these two.


## What's Changed
* loxl: a 0 on a number a save leaves out is no attribute by @discostu105 in https://github.com/discostu105/lox/pull/334
* loxl: hardware declarations take over Tree and Air devices by @discostu105 in https://github.com/discostu105/lox/pull/336
* loxl: Greater and Less link no knowledge-base page by @discostu105 in https://github.com/discostu105/lox/pull/338
* loxl: unit suffixes on extern sets, template parameters and HTTP input settings by @discostu105 in https://github.com/discostu105/lox/pull/330


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.68.1...v0.69.0

## discostu105/lox v0.70.0 (2026-11-01T11:34) [SKILL-RELEVANT]
## 🚀 Improvements

- **loxl** names each operating mode one way in rules and schedules: a built-in mode in a schedule by its day word (`mon`), a mode the module declares or externs by its slug (`when mode party`, and now `party 18:00-24:00` in a schedule), any other by its title. Another spelling is an error that names the replacement, with a quick fix in the language server; `loxl fmt` on a module directory, `decompile` and `adopt` write the one spelling. The compiled config does not change.
- **`loxl lint`**: a `dead-outputs` finding on a room controller or a Touch Pure Flex controller that drives nothing says what to wire: the heating or cooling output to the valve actuators, or the controller to the API Connector of a Touch Pure Flex.

## 🐛 Bug Fixes

- **`loxl adopt`** and **`loxl decompile`** write `Signed: off`, `Analog: off` or `CloseAfterSend: off` for an unticked box on a virtual HTTP or UDP command or a virtual output. Before, they wrote nothing, and the box came out ticked when the source was compiled onto another config.


## What's Changed
* loxl: one spelling per operating mode in rules and schedules by @discostu105 in https://github.com/discostu105/lox/pull/329
* loxl lint: a dead controller's finding says what to wire by @discostu105 in https://github.com/discostu105/lox/pull/343
* loxl: adopt writes off where a fresh object would tick the box by @discostu105 in https://github.com/discostu105/lox/pull/339


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.69.0...v0.70.0

## discostu105/lox v0.70.1 (2026-11-01T11:55) [SKILL-RELEVANT]
## 🐛 Bug Fixes

- **`loxl compile`** and **`loxl check`** refuse a value that Loxone Config rewrites on save, and name the value it writes: a virtual HTTP input's `Poll` below 10 or above 604800, a `Timeout` below 10, a fraction on either or on `Allowedtimeouts`, and a digital `VirtualIn`'s `MaxVal` other than 1 or `MinVal` other than 0. Before, the next save showed them as changed.


## What's Changed
* loxl: refuse a value a Loxone Config save rewrites by @discostu105 in https://github.com/discostu105/lox/pull/350


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.70.0...v0.70.1

## discostu105/lox v0.71.0 (2026-11-01T12:11) [SKILL-RELEVANT]
## ✨ New

- **`loxl lsp`** offers a quick fix on a lint finding that keeps it: `# lint: allow <kind>` above its declaration, indented like it, or the kind added to the allow already there. An `unused-allow` finding now shows on its comment and offers to remove it.


## What's Changed
* loxl lsp: quick fixes to add and remove a lint allow by @discostu105 in https://github.com/discostu105/lox/pull/347


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.70.1...v0.71.0

## discostu105/lox v0.71.1 (2026-11-01T12:45) [SKILL-RELEVANT]
## 🐛 Bug Fixes

- **`loxl compile`** and **`loxl check`** refuse a title that Loxone Config rewrites on save, and name the title it writes: `%`, `<` and `|` become `_` on most objects (other sets on lighting controllers, operating modes and calendar entries), `{`, `}`, tabs and line breaks go, and a space at either end becomes `_`. An empty title is refused too. Before, the next save showed the object as renamed. The blocks of an expression write `<=`, `<` and `%` in their labels as `≤`, `＜` and `％`, which a save keeps.


## What's Changed
* loxl: refuse a title a Loxone Config save rewrites by @discostu105 in https://github.com/discostu105/lox/pull/351


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.71.0...v0.71.1

## discostu105/lox v0.72.0 (2026-11-01T12:54) [SKILL-RELEVANT]
## 🚀 Improvements


## 🐛 Bug Fixes

- **Lox Logic** sets a virtual UDP command's receive timeout: `MaxTime: 30s`, with `DefVal:` (the value then) or `ValOT: 1` (keep the last value). Compile refuses a timeout a Loxone Config save would cut to whole milliseconds.


## What's Changed
* loxl: set a UDP command's receive timeout by @discostu105 in https://github.com/discostu105/lox/pull/353
* loxl: a calendar entry names its mode with switches: by @discostu105 in https://github.com/discostu105/lox/pull/348


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.71.1...v0.72.0

## discostu105/lox v0.73.0 (2026-11-01T13:27) [SKILL-RELEVANT]
## ✨ New

- **loxl**: a named signal takes a label of its own: `beschatten.title = "Beschatten Süd"` on the line below it sets the top block's title, which is otherwise the expression text (#288).
- **loxl decompile**, **loxl adopt**: the blocks an expression or named signal compiled to come back as that expression, signal and `let`, where they compile to the same blocks. Adopt marks them expression-owned in the lock.


## What's Changed
* loxl: signal labels, decompile lifts expressions back by @discostu105 in https://github.com/discostu105/lox/pull/354


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.72.0...v0.73.0

## discostu105/lox v0.74.0 (2026-11-01T16:40) [SKILL-RELEVANT]
## 🚀 Improvements

- **loxl** writes a calendar entry's date as a date: `on: 12-31` (a day every year), `easter: 1` (days after Easter Sunday), `from: 2026-07-04, to: 2026-09-05` (one period) and `from: 10-01, to: 04-30` (every year). The stored attributes (`Mode: 4, Month: 10, Day: 1, Month2: 4, Day2: 30`, `From: 6393`, `EasterOffset:`, `WeekDayInMonth:`) are an error that names the replacement, with a quick fix in the language server; `loxl fmt` rewrites them and `adopt` writes the date. The compiled config does not change.


## What's Changed
* loxl: a calendar entry states its date as a date by @discostu105 in https://github.com/discostu105/lox/pull/356


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.73.0...v0.74.0

## discostu105/lox v0.75.0 (2026-11-01T17:12) [SKILL-RELEVANT]
`lox config push` now guards against deleting rules edited in the app, and `lox config sync` checks a project
against the Miniserver. `lox hw status` finds missing, offline and replaced devices.

Four kinds of Tree device can now be created from Lox Logic, unpaired, ready for a Tree search in Loxone Config.

## ✨ New

- **`lox logic`** creates and adopts 13 more block types: virtual status (`StateV`), wiping relay, the four arithmetic blocks (`Add`, `Sub`, `Mult`, `Div`), moving average, integer, up counter, up-down counter, runtime counter, pulse by text and analog memory. They cover about 84% of the page blocks in the public test configs, up from 62%. `loxl test` simulates the wiping relay, integer, analog memory and both counters.
- **`lox config push`** refuses `--force` when the Automatic Designer's rules changed since the last verified push, since the upload would delete rules edited in the app. It records the change time in `autopilot.changed`; `--allow-app-changes` overrides. The saved lock now matches the verified download.
- **`lox config sync`** checks, read-only, that a project's source, lock and the live config agree, and exits 1 when they don't.
- **`lox hw status`** compares the devices on the bus (`/data/status`) with the program file: missing, offline, replaced (serial changed) or not in the program. Table or `-o json`.
- **`lox mcp`** gets read-only tools for hardware and config as code: `hw_status`, `logic_check`, `logic_diff`, `logic_drift`, `logic_lint`, `logic_compile` (into a scratch directory), `logic_test`, `config_sync`, `config_push_dry_run` and more.
- **`loxl compile`** creates Tree devices: `melder = TreeDevice("Melder", kind: "PresenceSensorTree", tree: tree1)` adds an unpaired device to the Tree extension `tree1`. Touch Tree, Presence Sensor Tree, LED Ceiling Light RGBW Tree and Valve Actuator Tree are supported. Pair it in Loxone Config; the compile prints a note until then. `removed melder` deletes it, and no compile deletes other hardware.

## 🐛 Bug Fixes

- **loxl adopt** takes over a calendar entry whose operating mode is gone from the config (a deleted user mode). It writes a comment instead of `switches:`, and the entry keeps its mode number until `switches:` names one. Before, adopt refused the entry.


## What's Changed
* Push guards, config sync, hw status, MCP config-as-code tools by @discostu105 in https://github.com/discostu105/lox/pull/331
* loxl: admit StateV, WipingRelay, arithmetic and counter blocks by @discostu105 in https://github.com/discostu105/lox/pull/327
* loxl adopt: a calendar entry whose operating mode is gone by @discostu105 in https://github.com/discostu105/lox/pull/360
* loxl: create Tree devices from source by @discostu105 in https://github.com/discostu105/lox/pull/340


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.74.0...v0.75.0

## discostu105/lox v0.75.1 (2026-11-01T17:29) [SKILL-RELEVANT]
## ✨ New

- **Lox Logic block settings** come from source: the name the app shows (`Desc:`), a memory flag's type (`Type: "text"`), when a PulseAt fires (`Pulse: "sunset"`), a blind's sunshine flag (`Sun: on`), a DayTimer's on/off texts and a meter's units. `loxl decompile` and `loxl adopt` lift them, and `loxl types <Type>` lists them
  - `loxl coverage` names the parameter that claims each carried attribute and no longer lists values a save writes on its own

## 🐛 Bug Fixes

- **`loxl compile`** writes no `Def="0"` on a block input, as Loxone Config saves it: a comparison with 0 (`x.Q < 0`), a parameter of 0 and `x.Port = 0` no longer show as changed after a save. `loxl test` reads an unset parameter as 0, as Loxone Config does, and `loxl decompile` states it (`Time: 0`) where Config's default is not 0.


## What's Changed
* Lox Logic: block settings from source by @discostu105 in https://github.com/discostu105/lox/pull/337
* loxl: a connector's 0 is no Def= by @discostu105 in https://github.com/discostu105/lox/pull/363


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.75.0...v0.75.1

## discostu105/lox v0.76.0 (2026-11-01T18:06) [SKILL-RELEVANT]
## ✨ New

- **`loxl test`** simulates more shading and meter behavior: push & hold, long and double click, toggle and Pos on Automatic Shading, the central shading block, the meters' day, month and year readings and their reset, and on the Lighting Controller a mix's brighter value and DisP during motion.
- **`lox logic compile`** sets up light controller circuits from source: `Circuit1: "dimmer"` (or `"switch"`) on a `LightController2` names the circuit after the actuator `AQ1` drives and makes its moods dim, as the mood editor in Loxone Config does. `lox logic lint` warns when a mood sets a percentage on a circuit that is no dimmer.
- **`lox logic decompile`** and **`lox logic adopt`** lift push notifications (`OutputRefLM`) and their recipients, and circuits, so a config with notifications can be taken over from a real file.

## 🚀 Improvements

- **loxl** knows the documented units, canvas labels and ranges of the alarms, the room controller, the meters, the NFC Code Touch, the intercom, the irrigation and the math and counter blocks. `adopt` and `decompile` write their time parameters with a suffix (`PulseTime: 3s`), and `loxl lint` flags bare numbers there; `loxl lint --fix` rewrites them without changing the compiled output.
- **Lox Logic** knows the units of the Modbus and UDP timing settings, read off Loxone Config: a Modbus server's `Timeout` in milliseconds, a Modbus sensor's `ModbusPollingCycle` in seconds and `MaxTime` in milliseconds, a virtual UDP command's `MinTime` in milliseconds (`MaxTime: 5min` compiles to `300000`). `loxl lint --fix` and adopt write them with a suffix. A Modbus sensor's `MinTime` stays a bare number.
- **`loxl check`** (and `lox logic check`) reports every independent error in one run, sorted by file and line, instead of stopping at the first. One missing name or unknown block type is reported once, not at every use. `--json` gives each error its own `path` and `line`; the language server shows each one as its own diagnostic.


## What's Changed
* loxl: regenerate port_meta for the later-admitted block types by @discostu105 in https://github.com/discostu105/lox/pull/364
* Lox Logic: light controller circuits from source, lift notifications by @discostu105 in https://github.com/discostu105/lox/pull/366
* loxl check: report every independent error at once by @discostu105 in https://github.com/discostu105/lox/pull/311
* loxl: units of the Modbus and UDP timing settings by @discostu105 in https://github.com/discostu105/lox/pull/345
* Simulator: shading push buttons, central shading, meter periods by @discostu105 in https://github.com/discostu105/lox/pull/328


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.75.1...v0.76.0

## discostu105/lox v0.77.0 (2026-11-01T18:16) [SKILL-RELEVANT]
## 🚀 Improvements

- **loxl fmt**: a call with more than three arguments goes on one line when they are all numbers, unit values, times or `on`/`off` and it fits in 100 columns (`ModbusASensor(…)`, `defaults …`). A whole-line comment stays right above the statement it was written above, and a blank line below a comment is kept.
- **loxl lint --fix** respells only the values it fixes and leaves the rest of the file as written.
- **loxl drift** reports the config the last compile started from as in sync (its output is not pushed yet) instead of as changed, so `examples/ci.sh` no longer prints a drift note for the shipped examples.
- **loxl lsp**: argument-key completion leaves out the keys the call binds already, and hover on a block in a template body shows the `defaults` values it takes.


## What's Changed
* loxone-config 0.20.0 by @discostu105 in https://github.com/discostu105/lox/pull/367
* loxl: fmt short-value calls and comments, lint --fix in place, LSP keys and hover, drift on the source config by @discostu105 in https://github.com/discostu105/lox/pull/358


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.76.0...v0.77.0

## discostu105/lox v0.78.0 (2026-11-01T18:38) [SKILL-RELEVANT]
## ✨ New

- **lox logic lint**: `implicit-zero` names an existing block whose port is 0 only because nothing sets it, while a new block would get a default (an adopted `Irrigation` without `Tv1`). `--fix` writes `Port: 0`, and the compile output stays the same.

## 🚀 Improvements

- **lox logic**: a block the compiler creates gets the defaults Loxone Config places it with on the ports the source leaves out, so a new `Monoflop` without `Time` pulses for 2 s instead of 0 s. Blocks that already exist keep their values.


## What's Changed
* loxl: a new block gets Loxone Config's defaults; lint implicit-zero by @discostu105 in https://github.com/discostu105/lox/pull/368


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.77.0...v0.78.0

## discostu105/lox v0.79.0 (2026-11-01T19:03) [SKILL-RELEVANT]
## ✨ New

- **`lox logic` central block members**: `alle.members = (licht_eg, licht_og)` sets the lighting controllers of a `CentralLight`, or the blinds of a `CentralShade`, in the order the app lists them. `adopt` and `decompile` lift the lists, and `diff` compares them.
- **`lox logic` energy flow units**: `Un1:`, `Un2:` and `UnSt:` on an `EFM` set its power, energy and storage units. The settings of room controllers, irrigation and alarm member lists stay with Loxone Config, refused by name with the reason.


## What's Changed
* Lox Logic: central block members and energy flow units from source by @discostu105 in https://github.com/discostu105/lox/pull/371


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.78.0...v0.79.0
