# Changelog

## 1.0.0 — 2026-11-19

First release. Six text packs per language, every entry bilingual.

- Bilingual everywhere: NPC dialogue, cutscene subtitles, event text, popup confirm buttons, menus, key prompts, help text, system messages, place names, item names/descriptions/lore, blood messages — 124 FMGs, 40,637 merged entries per language pair.
- Ships `menu`, `menu_dlc1`, `menu_dlc2`, `item`, `item_dlc1`, `item_dlc2` under `msg/zhocn/` and `msg/engus/`.
- Nothing is filtered out by word: short answers such as 是/否 (YES/NO) are merged like any other line.
- Separator: a newline for dialogue, subtitles and descriptions; ` / ` for names, place names, key prompts and popup buttons.
- Zero-argument rebuild: `python tools\dualsub.py` reads the vanilla packs in `source/` and writes back into `msg/`; the merge is idempotent, so a rebuild never stacks the two languages.
- Per-entry edits: unpack a pack with WitchyBND and change single `.fmg` entries (see README).
- License: the scripts are MIT; the game text is FromSoftware / Bandai Namco content, offline single-player use only.
