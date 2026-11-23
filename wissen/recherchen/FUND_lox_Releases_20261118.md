# FUND lox-Releases 18.11.2026 07:55 (4 neu, davon 2 skill-relevant)
Quelle: https://github.com/discostu105/lox/releases (nur gelesen). Skill-relevant = Stichwort aus config diff, config push, config pull, decompile, loxl, lox logic, simulator, mcp, loxone-config, adopt, drift, types.

## discostu105/lox v0.86.0 (2026-11-15T20:06) [SKILL-RELEVANT]
## ✨ New

- **`loxl adopt --uuid` on the project or the Miniserver** writes their settings into the source as they stand (location, time zone, automatic updates, security switches, where the Miniserver is mounted), so taking them over needs no typing and changes nothing on the next compile.
- **`lox logic adopt --uuid` takes over a Touch Pure Flex and a device whose output is driven from several places.** A declared `TreeDevice` carries its `.tiles` claim, and several `<-` onto one port become a list (`I: [alarm.Silent, brand.PreAlarmSignal]`). Adopting devices one by one no longer writes a `defaults` in front of declarations that have none.
- **Lox Logic: plugins from source.** `mcp = Plugin("MCP Server", gid: "McpServer", custom_local_url: "…")` creates the MCP Server or Matter plugin in the Network Periphery; `uuid:` takes over any plugin Loxone Config made. Settings are the package's parameters, checked by name and type, and a Miniserver's limit per package is honoured. `loxl adopt --uuid … --as <slug>` writes the declaration.
- **Lox Logic: rooms and categories from source.** `werkstatt = Place("Werkstatt", PType: 6)` and `garten = Category("Garten")` create a room and a category the way Loxone Config does, with their permission group and their app entry. `.room = werkstatt` names one by slug. A rename renames the group; a removal takes it along. Existing ones are externs or `adopt --uuid`.


## What's Changed
* Lox Logic: rooms, categories, plugins, Flex/Nano IO Air and the Miniserver's settings by adopt by @discostu105 in https://github.com/discostu105/lox/pull/411
* Fix the macOS CI failure of #399: ~/.lox through a symlinked home by @discostu105 in https://github.com/discostu105/lox/pull/407


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.85.0...v0.86.0

## discostu105/lox v0.86.1 (2026-11-15T20:49)
## 🚀 Improvements

- Dependency updates: base64, dirs, lz4_flex, hmac, tokio-tungstenite, opentelemetry (#412)


## What's Changed
* Dependency updates: base64, dirs, lz4_flex, hmac, tokio-tungstenite, opentelemetry by @discostu105 in https://github.com/discostu105/lox/pull/412
* Bump hmac from 0.12.1 to 0.13.0 by @dependabot[bot] in https://github.com/discostu105/lox/pull/400
* Bump tokio-tungstenite from 0.24.0 to 0.30.0 by @dependabot[bot] in https://github.com/discostu105/lox/pull/401
* Bump base64 from 0.22.1 to 0.23.1 by @dependabot[bot] in https://github.com/discostu105/lox/pull/403
* Bump dirs from 5.0.1 to 7.0.0 by @dependabot[bot] in https://github.com/discostu105/lox/pull/404
* Bump lz4_flex from 0.13.1 to 0.14.0 by @dependabot[bot] in https://github.com/discostu105/lox/pull/405
* Bump opentelemetry from 0.31.0 to 0.33.1 by @dependabot[bot] in https://github.com/discostu105/lox/pull/406

## New Contributors
* @dependabot[bot] made their first contribution in https://github.com/discostu105/lox/pull/400

**Full Changelog**: https://github.com/discostu105/lox/compare/v0.86.0...v0.86.1

## discostu105/lox v0.87.0 (2026-11-15T22:27) [SKILL-RELEVANT]
## ✨ New

- **Miniserver and extension I/O as hardware declarations**: the Miniserver's own relay outputs, digital inputs and overtemperature shutdown, Relay and DI Extensions, Intercoms, and the API connectors and overtemperature shutdowns of Tree and Air devices can be declared in source. `loxl adopt --uuid` takes such an I/O alone once its device is declared


## What's Changed
* Miniserver and extension I/O as hardware declarations (D139) by @discostu105 in https://github.com/discostu105/lox/pull/413


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.86.1...v0.87.0

## discostu105/lox v0.88.0 (2026-11-15T22:45)
## ✨ New

- **`lox hw ls`, `lox hw search` and `lox hw identify`** use the Miniserver's device search, as the Loxone App does in expert mode
  - `hw ls` lists the paired Tree, Air and Link devices with serial, base, room and online state
  - `hw search tree|air|<base>` shows unpaired devices in learn mode as they turn up, without pairing them
  - `hw identify <serial>` lets a device flash; search and identify always end, also on Ctrl-C


## What's Changed
* lox hw ls / search / identify via the livelearn API by @discostu105 in https://github.com/discostu105/lox/pull/414


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.87.0...v0.88.0
