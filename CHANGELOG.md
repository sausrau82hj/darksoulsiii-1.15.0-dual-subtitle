# Changelog

`msg/` holds the built packs; `tools/dualsub.py` rebuilds them from `source/`.

## 2026-11-19

- All categories are bilingual: NPC dialogue, cutscene subtitles, event text, popup confirm buttons, menus, key prompts, help text, system messages, place names, item names/descriptions/lore, blood messages. `msg/` now also ships `item*.msgbnd.dcx` — 124 FMGs, 40,637 entries.
- No word is filtered out: short answers such as 是/否 (YES/NO) are merged like any other line.
- Popup confirm windows use a one-line `是 / YES` separator; the other widgets keep their own newlines.
- README: per-entry editing documented, done with WitchyBND.
- LICENSE reduced to plain MIT; the game-text notice lives in the README.

## 2026-11-18

- First build: NPC dialogue and cutscene subtitles only, 6 packs per language (`menu`, `menu_dlc1`, `menu_dlc2`, `item`, `item_dlc1`, `item_dlc2`).
- Zero-argument rebuild: the script finds Yabber inside the package, reads `source/` and writes back into `msg/`.
- Merge is idempotent, so rebuilding from already-merged text never stacks the two languages twice.
- `--list` writes the category template instead of overwriting the active config.
