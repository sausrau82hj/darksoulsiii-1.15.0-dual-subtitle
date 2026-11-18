# DualSubtitle · 中英双语文本 / Chinese–English dual-language text

DARK SOULS III 1.15.0 — 以中文显示时下方给出英文，以英文显示时下方给出中文。

**中文 · English**

---

## 中文

把游戏显示语言**再加一份另一语言的文本**：显示简体中文时，英文跟在后面（换行或 `中文 / English`）；显示英文时，中文跟在后面。只改 `msg\` 下的文本包，不动 exe、params、存档，可随时还原。

### 前提

- 游戏为**松散文件**环境（用 UXM / Nuxe 解包过，`Game\msg\` 里是散开的文本包）。没解包的话，替换进去的文件根本不会被读取。
- 安装前**关闭游戏**，装完**离线**启动（改过文本文件，避免联机风险）。
- 若另有 mod 也改 `msg`，两者会互相覆盖。

### 安装

前提：游戏已用 UXM / Nuxe 解包（`Game\msg\` 里是散文件），且已关闭。

先备份原版，**只做一次**，再覆盖 —— 每语言 6 个包，`menu.msgbnd.dcx` / `item.msgbnd.dcx` 是本体文件名，必须有

### 卸载

```powershell
$game = "D:\steam\steamapps\common\DARK SOULS III\Game"
foreach ($l in 'zhocn','engus') { Copy-Item "$game\.dualsub-backup\msg\$l\*.msgbnd.dcx" "$game\msg\$l\" -Force }
```

这 12 个文件本来是游戏自带的，覆盖回原版即可，不用删。没备份就用 UXM / Nuxe 重新解包，或 Steam「验证文件完整性」（会连别的 mod 一起清掉）。

### 成品实际覆盖哪些文本

以 `tools\dualsub.config.json` 为准，默认只开两类，其余保持游戏原本的单语显示：

| 文本类别 | 默认 | 说明 |
|---|---|---|
| 会話（NPC 对话） | **开** | 逐条合并，副语言为空的条目保持原样 |
| ムービー字幕（过场字幕） | **开** | 同上 |
| イベントテキスト（事件文本）、对话框、菜单、按键提示、道具名/说明/背景故事、地名、帮助文本、血文字、系统消息 | 关 | 保持游戏原本的单语显示 |

道具包（`item*.msgbnd.dcx`）照样替换，但默认配置在道具文本上一条都没合并，内容与原版一致 —— 之所以要装，是因为本体文件名那份必须存在。

想让别的类别也双语，改配置后重新生成（见下）。长描述类受界面高度限制，建议用 `"en_only"` 只换成英文。

### 重新生成

需要 **Python 3.9+** 和 **Yabber**（[https://github.com/JKAnderson/Yabber/releases](https://github.com/JKAnderson/Yabber/releases)，解压即可，不用安装）。

在包根目录执行：

```
python tools\dualsub.py --config tools\dualsub.config.json --out . --source source --yabber "D:\Tools\Yabber 1.3.1"
```

`--out .` 表示把结果写回本目录的 `msg\`；跑完按上面的安装步骤覆盖进游戏。

| 参数 | 作用 |
|---|---|
| `--config` | 配置文件，默认 `tools\dualsub.config.json` |
| `--out` | 输出目录（成品写在 `<out>\msg\<语言>\`） |
| `--source` | 原始文本包所在目录（本包是 `source`；不给就与 `--game` 相同） |
| `--game` | 游戏 `Game` 目录，只在没给 `--source` 时需要（自动定位失败时手动传） |
| `--yabber` | Yabber 所在文件夹（含 `Yabber.exe` 与 `Yabber.DCX.exe`）；也可写在配置的 `yabber_dir`，或用环境变量 `YABBER_DIR` |
| `--primary` / `--secondary` | 主/副语言目录，默认 `zhocn` / `engus` |
| `--filter` | 只重建名称匹配的包，如 `--filter "menu*"` |
| `--keep-work` | 保留中间文件，方便查错 |
| `--list` | 列出游戏里的文本包并生成一份中文分类配置模板；**会写到 `--config` 指定的路径**，别指向正在用的配置（用 `--list --config tools\template.json`） |

配置项：

| 键 | 作用 |
|---|---|
| `yabber_dir` | Yabber 所在文件夹 |
| `primary` / `secondary` | 主/副语言目录，默认 `zhocn` / `engus` |
| `separator` | 默认分隔符，默认换行（多行控件如对话、字幕用这个） |
| `default_enabled` | 未在 `categories` 里列出的类别是否默认合并 |
| `skip_merge_texts` | 永不合并的短词（是 / 否 / 确定 / 取消），避免菜单错位 |
| `categories` | 每类开关：`true` 双语 · `"off"`/`false` 保持原样 · `"en_only"` 只换英文 · `"append"` 强行追加 |
| `files` | 按文本包、按 FMG 覆盖分隔符，如 `{"menu": {"fmg": {"地名.fmg": {"separator": " / "}}}}` |

分隔符是自动的：多行控件（会話、ムービー字幕、说明类）用换行，单行控件（名称、地名、按键提示）用 ` / `。要改就用 `files` 段单独覆盖。

生成时以 `source\` 里的原版文本包为源，所以**不需要先卸载**。只有把 `source\` 删了、脚本转去读游戏目录时，才要先还原，否则会把已经双语的内容再合并一次。

### 文件

```
msg\zhocn\menu.msgbnd.dcx     ← 生成物（内容同 menu_dlc2 累积版，游戏读本体文件名时用）
msg\zhocn\menu_dlc1.msgbnd.dcx
msg\zhocn\menu_dlc2.msgbnd.dcx
msg\zhocn\item*.msgbnd.dcx     同样生成，但默认配置不合并道具文本（内容同原版）
msg\engus\...                 同上，英文槽
source\msg\...                原版文本包副本，重新生成时作为源
tools\dualsub.py              生成器
tools\dualsub.config.json     类别开关 + Yabber 路径
```

### 已知限制

- 道具说明面板高度固定，中文 + 英文塞不下；`Item Descriptions` / `Item Lore` 默认关闭，想看英文就设成 `"en_only"`。
- 游戏更新或 Steam「验证文件完整性」会覆盖这些文件，重装一遍即可（备份不用重做）。
- 只改文本。别的 mod 也换 `msg` 时，请以那个 mod 的文件为源重新生成。

---

## English

Adds the *other* language underneath the one you already display: with Simplified Chinese selected, English follows (on a new line, or `中文 / English` on one line); with English selected, Chinese follows. Only the text packs under `msg\` are replaced — exe, params and saves are untouched, and everything can be removed again.

### Requirements

- The game must be in the **loose-file setup** (unpacked with UXM / Nuxe, so `Game\msg\` holds real files). Without it, the replaced packs are never read.
- Close the game before installing, and start it **offline** afterwards (text files are modified — avoid online play).
- If another mod also replaces `msg` files, the two overwrite each other.

### Install

Requires the loose-file setup (unpacked with UXM / Nuxe, so `Game\msg\` holds real files) and the game closed.

Back up the vanilla packs **once**, then overwrite — 6 packs per language; `menu.msgbnd.dcx` / `item.msgbnd.dcx` carry the base filenames and must be present

### Uninstall

```powershell
$game = "D:\steam\steamapps\common\DARK SOULS III\Game"
foreach ($l in 'zhocn','engus') { Copy-Item "$game\.dualsub-backup\msg\$l\*.msgbnd.dcx" "$game\msg\$l\" -Force }
```

Those 12 files ship with the game, so restoring the originals is enough — nothing to delete. No backup? Re-unpack with UXM / Nuxe, or use Steam's "verify integrity" (which also wipes other mods' changes).

### What is actually bilingual in the shipped build

The shipped `tools\dualsub.config.json` decides this — by default two categories are on, everything else stays single-language as in the base game:

| Category | Default | Notes |
|---|---|---|
| 会話 (NPC dialogue) | **on** | merged entry by entry; entries with no secondary text stay as they are |
| ムービー字幕 (cutscene subtitles) | **on** | same |
| イベントテキスト (event text), dialogue boxes, menus, key prompts, item names/descriptions/lore, place names, help text, blood messages, system messages | off | unchanged |

The item packs (`item*.msgbnd.dcx`) are replaced as well, but the default config merges nothing in the item text — their content matches the base game. They are installed because the base-filename copy has to exist.

Enable more categories in `tools\dualsub.config.json` and rebuild (below). Long description panels cannot fit both languages — prefer `"en_only"` for those.

### Rebuild

Requires **Python 3.9+** and **Yabber** ([https://github.com/JKAnderson/Yabber/releases](https://github.com/JKAnderson/Yabber/releases), just extract it).

From the package root:

```
python tools\dualsub.py --config tools\dualsub.config.json --out . --source source --yabber "D:\Tools\Yabber 1.3.1"
```

`--out .` writes the result back into this folder's `msg\`; then install as above.

| Argument | Meaning |
|---|---|
| `--config` | config file, defaults to `tools\dualsub.config.json` |
| `--out` | output folder (results land in `<out>\msg\<lang>\`) |
| `--source` | folder with the vanilla packs (here: `source`; defaults to `--game`) |
| `--game` | the game's `Game` folder — only needed when `--source` is not given (or auto-detection fails) |
| `--yabber` | folder holding `Yabber.exe` and `Yabber.DCX.exe`; alternatively `yabber_dir` in the config, or the `YABBER_DIR` environment variable |
| `--primary` / `--secondary` | language folders, default `zhocn` / `engus` |
| `--filter` | rebuild only matching packs, e.g. `--filter "menu*"` |
| `--keep-work` | keep intermediate files for debugging |
| `--list` | list the packs and write a Chinese category template; **it writes to the `--config` path**, so don't point it at your live config (use `--list --config tools\template.json`) |

Configuration keys:

| Key | Meaning |
|---|---|
| `yabber_dir` | folder holding `Yabber.exe` and `Yabber.DCX.exe` |
| `primary` / `secondary` | language folders, default `zhocn` / `engus` |
| `separator` | default join separator, a newline (used by multi-line controls: dialogue, subtitles) |
| `default_enabled` | merge categories that are not listed under `categories` |
| `skip_merge_texts` | short strings never merged (是 / 否 / 确定 / 取消), so menus don't break |
| `categories` | per-category switch: `true` bilingual · `"off"`/`false` untouched · `"en_only"` English only · `"append"` force-append |
| `files` | per-pack, per-FMG separator override, e.g. `{"menu": {"fmg": {"地名.fmg": {"separator": " / "}}}}` |

The separator is chosen automatically: multi-line controls (dialogue, cutscene subtitles, descriptions) use a newline, single-line controls (names, place names, key prompts) use ` / `. Override one with the `files` section.

The build reads the vanilla packs from `source\`, so **uninstalling first is not necessary**. Only if you delete `source\` and the script falls back to the game folder do you have to restore first — otherwise already-bilingual files get merged twice.

### Files

```
msg\zhocn\menu.msgbnd.dcx     generated (same content as the cumulative menu_dlc2, used for the base filename)
msg\zhocn\menu_dlc1.msgbnd.dcx
msg\zhocn\menu_dlc2.msgbnd.dcx
msg\zhocn\item*.msgbnd.dcx     generated too, but the default config merges no item text (matches vanilla)
msg\engus\...                 the same for the English slot
source\msg\...                pristine copies of the vanilla packs, used as the build source
tools\dualsub.py              generator
tools\dualsub.config.json     category switches + Yabber path
```

### Known limitations

- The item description panel has a fixed height: Chinese + English never fits. `Item Descriptions` / `Item Lore` default to off; use `"en_only"` to read the English instead.
- Game updates and Steam "verify integrity" overwrite these files; install again (the backup stays valid).
- Text only. If another mod also replaces `msg` files, regenerate from that mod's files as the source.

### License

Scripts: MIT — see [LICENSE](LICENSE). The generated text is modified FromSoftware / Bandai Namco game text, included for offline single-player modding, not for commercial use. Not affiliated with FromSoftware or Bandai Namco.
