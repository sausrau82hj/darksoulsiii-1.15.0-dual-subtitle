# Third-party notices

This repository ships no third-party code. Building the packs, and editing single entries by hand, rely on the external tools below. None of them is bundled or redistributed here — download them yourself.

| Tool | Used for | Author | License | Source |
|---|---|---|---|---|
| Yabber | Required. Unpacks and repacks `.msgbnd.dcx` / `.fmg` while rebuilding. | JKAnderson | GPL-3.0 | https://github.com/JKAnderson/Yabber |
| WitchyBND | Optional. Unpacking one pack to edit entries by hand (README → Finer edits). | ividyon | GPL-3.0 | https://github.com/ividyon/WitchyBND |
| UXM | Optional. Unpacking `Data*.bhd` / `.bdt` into the loose files the game reads. Archived upstream. | JKAnderson | GPL-3.0 | https://github.com/JKAnderson/UXM |
| Nuxe | Optional. Same job as UXM, current alternative. | JKAnderson | GPL-3.0 | https://github.com/JKAnderson/Nuxe |
| Mod Engine | Optional. Loads the `msg` packs from `Game\mod\msg` without unpacking the game (README → Install). | katalash | None stated — the repository carries no license file | https://github.com/katalash/ModEngine |
| Python 3.9+ | Runs `tools/dualsub.py`. Standard library only, no third-party packages. | Python Software Foundation | PSF-2.0 | https://www.python.org |

Yabber, WitchyBND, UXM and Nuxe are called as separate programs; Mod Engine is a DLL you drop into the game folder yourself. None of them is linked into or distributed with this repository, so their own licenses apply to them, not to the files here.

The text under `msg/` and `source/` is modified FromSoftware / Bandai Namco game content, not third-party software — see the License section of the README.
