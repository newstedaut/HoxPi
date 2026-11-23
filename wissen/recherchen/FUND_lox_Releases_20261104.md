# FUND lox-Releases 04.11.2026 07:55 (3 neu, davon 3 skill-relevant)
Quelle: https://github.com/discostu105/lox/releases (nur gelesen). Skill-relevant = Stichwort aus config diff, config push, config pull, decompile, loxl, lox logic, simulator, mcp, loxone-config, adopt, drift, types.

## discostu105/lox v0.80.0 (2026-11-03T23:27) [SKILL-RELEVANT]
The Lox Logic language starts its third revision: readable port names, bare block names for a block's
default output, and `let` aliases of ports. `loxl fmt --write` migrates a v2 module.

## 🚀 Improvements

- **Lox Logic v3, part 1: ports have source names.** A port is named by a readable name instead of the connector key Loxone Config stores: `In1`/`In2` on every two-input block, `Trigger`, `Enable`, `Disable`, `Power`, `LedRed`, … (`loxl types <Type>` lists them, with the stored key where it differs). A v2 key is an error that names the port; `loxl fmt --write` rewrites a v2 module.
- **Lox Logic: a bare block name is its default output.** `sonne and aussentemp >= 28` reads the outputs of `sonne` and `aussentemp`; `pumpe.On <- wp_bedarf` wires the signal. A block with several meaningful outputs still takes `x.Port`. Decompile and adopt write the bare form.
- **Lox Logic: `let` aliases a port.** `let aussen = sensor.AQ` names the port wherever a port may stand.


## What's Changed
* Lox Logic v3 part 1: port names, default outputs, let aliases by @discostu105 in https://github.com/discostu105/lox/pull/391


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.79.1...v0.80.0

## discostu105/lox v0.81.0 (2026-11-04T00:30) [SKILL-RELEVANT]
Externs take port bindings, fan-in is a list, expressions wrap and compute arithmetic under
comparisons and gates, `page` heads a file, a leftover `removed` or `moved` is a lint, and `every:`,
`°` and `step` replace `on:`, bare degrees and `tick <n>`.

## 🚀 Improvements

- **Lox Logic v3, part 2: a leftover `removed` or `moved` is a lint, not an error.** Once the removal has reached the deployed config or the rename is applied, the statement compiles to nothing and `loxl lint` reports it as `stale-lifecycle` with the line to delete. A misspelt slug is the same finding.
- **Lox Logic: `step` counts program cycles, `tick` takes a duration.** `step 3` (was `tick 3`), `tick 5min`. A bare number after `tick` is an error naming `step`; `loxl fmt --write` rewrites a v2 module.
- **Lox Logic: a calendar entry's day every year is `every: 12-31`** (was `on: 12-31`). `on:` is an error naming `every:`; `loxl fmt --write` rewrites it.
- **Lox Logic: `°` is a unit suffix** (`Dir: 180°`, `TComfort: 21°`), accepted on a port documented in degrees like `%` and `K` on theirs.
- **Lox Logic v3, part 2: externs take port bindings.** `extern jal = AutoJalousie(title: "Süd", AutoShade: beschatten, TargetPos: 70)` wires and sets like the same bindings on a block. `<-` and `=` work on every sink; on a block the module declares they fold into its argument list and `loxl lint` reports `remote-binding`.
- **Lox Logic: fan-in is a list.** `In1: [a, b]` puts several sources on one input; `fmt` writes it for a repeated key.
- **Lox Logic: expressions wrap and compute.** A long `and`/`or` chain continues on the next line, and `fmt` breaks one past 100 columns. `x.AQ + 1 >= 5` compiles to one `Formula` block, `a and x.AQ + 1` feeds the gate from one.
- **Lox Logic: `page` is the file's header.** At most one per file, before every other statement. A file with two pages becomes two files; `decompile` prints several pages as several files, and `adopt --out-module` refuses a config with blocks on several pages.


## What's Changed
* Lox Logic v3 part 2: extern bindings, expressions, page header, lifecycle lint, renames by @discostu105 in https://github.com/discostu105/lox/pull/392


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.80.0...v0.81.0

## discostu105/lox v0.82.0 (2026-11-04T01:33) [SKILL-RELEVANT]
Templates are block types: named like one, called like a block, with declared outputs, typed value
parameters and input parameters. This completes Lox Logic v3.

## 🚀 Improvements

- **Lox Logic v3, part 3: templates are block types.** A template is named like a type and called like a block (`sued = Fassade("Süd", jalousie: jal_sued)`). Its header declares the outputs (`-> (Q: beschatten.Q)`, read as `sued.Q`), its value parameters their type (`pos: number = 70`, `nachlauf: duration`), and an input parameter (`sonne: input`) is how a call feeds a port of the body. The primary block and call-site port bindings are gone; `loxl fmt --write` migrates a v2 template. New: the label string, nested instances, body-local `let`, `loxl types <Template>`.


## What's Changed
* Lox Logic v3 part 3: templates are block types by @discostu105 in https://github.com/discostu105/lox/pull/393


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.81.0...v0.82.0
