# FUND lox-Releases 08.11.2026 20:56 (1 neu, davon 0 skill-relevant)
Quelle: https://github.com/discostu105/lox/releases (nur gelesen). Skill-relevant = Stichwort aus config diff, config push, config pull, decompile, loxl, lox logic, simulator, mcp, loxone-config, adopt, drift, types.

## discostu105/lox v0.83.0 (2026-11-04T22:37)
## ✨ New

- **`lox config merge`** takes over what changed on the Miniserver since the base, so the next push loses nothing: rules edited or deleted in the app become source, other changes the source doesn't own (a plugin added in Loxone Config) stay as they are, and the download becomes the base.


## What's Changed
* lox config merge: take over rules edited in the app before a push by @discostu105 in https://github.com/discostu105/lox/pull/395


**Full Changelog**: https://github.com/discostu105/lox/compare/v0.82.0...v0.83.0
