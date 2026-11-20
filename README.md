# DualSubtitle — Dark Souls III Chinese–English dual-language text · 中英双语文本

DARK SOULS III 1.15.0

[中文](#中文) · [English](#english)

---

## 中文

### 安装

先关游戏，装完离线启动。两种方式任选：

- **替换文件**：游戏需用 UXM / Nuxe 解包过（`Game\msg\` 里是散文件），用本包的 `msg` 文件夹替换 `Game\msg`。
- **Mod Engine**：不用解包。把 Mod Engine 的 `dinput8.dll` 和 `modengine.ini` 放进 `DARK SOULS III\Game`，本包的 `msg` 放进 `Game\mod\msg`（即 `Game\mod\msg\zhocn\...`、`Game\mod\msg\engus\...`），`modengine.ini` 里保持 `modOverrideDirectory="\mod"`，然后正常启动游戏。Mod Engine 会挡住联网、另存一份 mod 存档，本体文件一个不动；别的 mod 也走 Mod Engine 时，文件放同一个 `Game\mod` 里就行。

### 卸载

替换文件安装的，把 `msg` 文件夹换回去，原文件夹在 `...source/msg`；Mod Engine 安装的，删掉 `Game\mod` 里的文件（整个 `Game\mod` 一起删也行），`modengine.ini` 那行不用动，要彻底还原再把 `dinput8.dll` 删掉。

### 重新生成

需要 **Python 3.9+** 和 [Yabber](https://github.com/JKAnderson/Yabber/releases)。

1. 把 Yabber 解压到本包根目录，例如 `DualSubtitle\Yabber 1.3.1\`（脚本自己会找到，不用配路径）。
2. 在包根目录执行：

```
python tools\dualsub.py
```

不带参数就是默认行为：拿包里的 `source\` 当源，成品写回包里的 `msg\`，跑完按上面第 2 步覆盖进游戏。
要换路径或只重建一部分时才加参数：`--source` / `--out`（这一步的源和成品目录）、`--yabber`（Yabber 不在包内时）、`--filter "menu*"`（只重建匹配的包）、`--keep-work`（保留中间文件查错）。

配置项：`primary` / `secondary`（默认 `zhocn` / `engus`，可以对调）、`separator`（单行文本的分隔符，默认 `" / "`）、`categories`（取值 `true` 合并双语 · `"off"` 原样不动 · `"sec_only"` 只留副语言）、`files`（例外清单，按包、按 FMG 单独设 `mode` / `enabled` / `separator`，优先级最高，如 `"files": {"menu_dlc2": {"fmg": {"地名.fmg": {"separator": " ~ "}, "アイテムうんちく.fmg": "sec_only"}}}`。

分隔符：原本就带换行的固定用换行，不提供自定义；单行的默认用 ` / `，把 `separator` 改成 `" ~ "` 之类就跟着换。

### 已知限制

- 只在1.15.0验证过。
- 只改文本。别的 mod 也换 `msg` 时，把那个 mod 的文件放进 `source\` 再生成。
- 同一句话中文一行、英文可能折成两三行，个别对话会顶到对话框下沿。

### 更精细的修改

[WitchyBND](https://github.com/ividyon/WitchyBND/releases) ：解包，修改，打包，替换。

### 致谢

受到此项目启发而制。[ER-Dualsub-Tool](https://github.com/matyamod/ER-Dualsub-Tool)

---

## English

### Install

Close the game first, start it offline afterwards. Two routes, either one:

- **Replace the files**: requires the loose-file setup (unpacked with UXM / Nuxe, so `Game\msg\` holds real files) — replace `Game\msg` with this package's `msg` folder.
- **Mod Engine**: no unpacking needed. Put Mod Engine's `dinput8.dll` and `modengine.ini` into `DARK SOULS III\Game` and this package's `msg` into `Game\mod\msg` (so `Game\mod\msg\zhocn\...` and `Game\mod\msg\engus\...`), keep `modOverrideDirectory="\mod"` in `modengine.ini`, and start the game normally. Mod Engine blocks online play and keeps a separate mod save file; nothing in the base game is touched. If another mod also runs through Mod Engine, put its files in the same `Game\mod`.

### Uninstall

Installed by replacing files: put the `msg` folder back — the original one is in `...source/msg`. Installed through Mod Engine: delete the files under `Game\mod` (or the whole folder); the `modengine.ini` line stays as it is, and remove `dinput8.dll` if you want the game fully vanilla again.

### Rebuild

Requires **Python 3.9+** and [Yabber](https://github.com/JKAnderson/Yabber/releases). 

1. Extract Yabber anywhere under the package root, e.g. `DualSubtitle\Yabber 1.3.1\` (the script finds it, no path to configure).
2. From the package root:

```
python tools\dualsub.py
```

No arguments is the default: it reads the bundled `source\` and writes the packs back into the package's `msg\`; then install with step 2 above. 

Arguments only when you need a different path or a partial rebuild: `--source` / `--out` (source and output folders), `--yabber` (Yabber outside the package), `--filter "menu*"` (rebuild matching packs only), `--keep-work` (keep intermediate files).

Config keys: `primary` / `secondary` (default `zhocn` / `engus` — swap them freely), `separator` (the separator inside one line, default `" / "`), `categories` (`true` merge both · `"off"` untouched · `"sec_only"` secondary language only), `files` (the exception list: per-pack, per-FMG `mode` / `enabled` / `separator`, highest priority, e.g. ` "files": {"menu_dlc2": {"fmg": {"地名.fmg": {"separator": " ~ "}, "アイテムうんちく.fmg": "sec_only"}}}`

Separators: text that already wraps keeps a newline and is not configurable; single-line text uses ` / ` by default, and `separator` changes it to something like `" ~ "`.

### Known limitations

- Verified on 1.15.0 only.
- Text only. If another mod also replaces `msg` files, drop that mod's files into `source\` and rebuild.
- A Chinese line plus an English one that wraps to two lines can sit tight against the bottom of the dialogue box.

### Finer edits

[WitchyBND](https://github.com/ividyon/WitchyBND/releases): unpack, edit, pack, replace.

### Credits

Inspired by this one.[ER-Dualsub-Tool](https://github.com/matyamod/ER-Dualsub-Tool)

---

## License / 许可证

The MIT license in [LICENSE](LICENSE) covers only the Python scripts and the other original files written for this project — `tools/dualsub.py`, `tools/dualsub.config.json`, this README, the changelog. It does not cover the text packs under `msg/` and `source/` (modified FromSoftware / Bandai Namco game text, included for offline single-player modding, not for commercial use), nor the external tools listed in [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md). Not affiliated with FromSoftware or Bandai Namco.
Change history: [CHANGELOG.md](CHANGELOG.md).
