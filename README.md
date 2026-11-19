# DualSubtitle · DS3 中英双语文本 / Chinese–English dual-language text

DARK SOULS III 1.15.0 — 以中文显示时下方给出英文，以英文显示时下方给出中文。

---

## 中文

只替换 6 个文本包（NPC 对话、过场字幕），`Game\msg\<语言>\menu.msgbnd.dcx / menu_dlc1 / menu_dlc2`。exe、params、存档、道具文本都不动。

### 安装

前提：游戏用 UXM / Nuxe 解包过（`Game\msg\` 里是散文件），并且已关闭。

```powershell
$Game = "X:\Steam\steamapps\common\DARK SOULS III\Game"

# 1) 备份原版（只做一次）
robocopy "$Game\msg" "D:\ds3-msg-backup" menu*.dcx /S

# 2) 覆盖（在本仓库根目录执行）
robocopy msg "$Game\msg" /E
```

装完离线启动游戏。游戏更新或 Steam「验证文件完整性」会冲掉，重跑第 2 步即可（备份不用重做）。

### 卸载

把 `D:\ds3-msg-backup` 里的 6 个文件覆盖回 `$Game\msg\zhocn\` 和 `\engus\`。没备份就 Steam 验证完整性，或用 UXM / Nuxe 重新解包。

### 双语范围

| 文本 | 默认 | 说明 |
|---|---|---|
| 会話（NPC 对话） | **开** | 逐条合并，副语言为空的条目保持原样 |
| ムービー字幕（过场字幕） | **开** | 同上 |
| 菜单、按键提示、道具名/说明/背景故事、地名、帮助、血字留言、系统消息、事件文本 | 关 | 保持原版单语 |

要开别的类别，改 `tools\dualsub.config.json` 里的 `categories` 再重新生成。长说明类（道具说明、背景故事）面板放不下两种语言，建议设成 `"en_only"` 只看英文。

### 重新生成

需要 Python 3.9+ 和 [Yabber](https://github.com/JKAnderson/Yabber/releases)（解压即可）。

```
python tools\dualsub.py --out . --source source --yabber "D:\Tools\Yabber 1.3.1"
```

`--out .` 把结果写回本目录的 `msg\`，然后按上面第 2 步覆盖进游戏。`source\` 里是原版文本包，所以重复生成不会把双语内容再合并一次；只有删掉 `source\` 转去读游戏目录时，才需要先还原原版。

| 参数 | 作用 |
|---|---|
| `--out` | 输出目录，成品写在 `<out>\msg\<语言>\`；省略则写到 `tools\DualSubtitle\` |
| `--source` | 原版文本包目录（本包是 `source`）；省略则读 `--game` 指向的游戏目录 |
| `--game` | 游戏 `Game` 目录，自动定位失败时才需要 |
| `--yabber` | Yabber 目录（含 `Yabber.exe` 与 `Yabber.DCX.exe`）；也可写在配置的 `yabber_dir` 或用环境变量 `YABBER_DIR` |
| `--filter` | 只重建匹配的包，如 `--filter "menu*"` |
| `--list` | 导出一份分类配置模板到 `tools\dualsub.template.json`（不会覆盖正在用的配置） |
| `--keep-work` | 保留中间文件，方便查错 |

配置项：`primary` / `secondary`（默认 `zhocn` / `engus`）、`separator`（默认换行）、`default_enabled`、`skip_merge_texts`（永不合并的短词）、`categories`（`true` 双语 · `"off"` 原样 · `"en_only"` 只换英文 · `"append"` 强行追加）、`files`（按包、按 FMG 覆盖分隔符，如 `{"menu": {"fmg": {"地名.fmg": {"separator": " / "}}}}`）。

分隔符是自动的：对话、字幕、说明类用换行，名称、地名、按键提示用 ` / `。

### 已知限制

- 只改文本。别的 mod 也换 `msg` 时，把那个 mod 的文件放进 `source\` 再生成。
- 如果只启用了部分类别，没合并到内容的包不会被生成，游戏继续读原版的那几个包。
- 同一句话中文一行、英文可能折成两三行，个别对话会顶到对话框下沿。

---

## English

Replaces 6 text packs only — NPC dialogue and cutscene subtitles — `Game\msg\<language>\menu.msgbnd.dcx / menu_dlc1 / menu_dlc2`. Exe, params, saves and item text are untouched.

### Install

Requires the loose-file setup (unpacked with UXM / Nuxe, so `Game\msg\` holds real files) and the game closed.

```powershell
$Game = "X:\Steam\steamapps\common\DARK SOULS III\Game"

# 1) back up the originals (once)
robocopy "$Game\msg" "D:\ds3-msg-backup" menu*.dcx /S

# 2) overwrite (run from this repository's root)
robocopy msg "$Game\msg" /E
```

Start the game offline afterwards. Game updates and Steam "verify integrity" overwrite these files — rerun step 2 (the backup stays valid).

### Uninstall

Copy the 6 files from `D:\ds3-msg-backup` back into `$Game\msg\zhocn\` and `\engus\`. No backup? Use Steam's verify integrity, or re-unpack with UXM / Nuxe.

### What is bilingual

| Text | Default | Notes |
|---|---|---|
| 会話 (NPC dialogue) | **on** | merged entry by entry; entries with no secondary text stay as they are |
| ムービー字幕 (cutscene subtitles) | **on** | same |
| Menus, key prompts, item names/descriptions/lore, place names, help text, blood messages, system messages, event text | off | vanilla single language |

Turn more on under `categories` in `tools\dualsub.config.json` and rebuild. Long description panels cannot fit both languages — set those to `"en_only"` to read the English instead.

### Rebuild

Requires **Python 3.9+** and [Yabber](https://github.com/JKAnderson/Yabber/releases) (just extract it).

```
python tools\dualsub.py --out . --source source --yabber "D:\Tools\Yabber 1.3.1"
```

`--out .` writes the result back into this folder's `msg\`; then install with step 2 above. `source\` holds the vanilla packs, so rebuilding never merges already-bilingual text twice — only if you delete `source\` and read the game folder instead do you need to restore the originals first.

| Argument | Meaning |
|---|---|
| `--out` | output folder, results land in `<out>\msg\<language>\`; defaults to `tools\DualSubtitle\` |
| `--source` | folder with the vanilla packs (here: `source`); defaults to the game folder given by `--game` |
| `--game` | the game's `Game` folder — only needed when auto-detection fails |
| `--yabber` | folder holding `Yabber.exe` and `Yabber.DCX.exe`; alternatively `yabber_dir` in the config or the `YABBER_DIR` environment variable |
| `--filter` | rebuild only matching packs, e.g. `--filter "menu*"` |
| `--list` | write a category template to `tools\dualsub.template.json` (never overwrites your live config) |
| `--keep-work` | keep intermediate files for debugging |

Config keys: `primary` / `secondary` (default `zhocn` / `engus`), `separator` (default newline), `default_enabled`, `skip_merge_texts` (short strings never merged), `categories` (`true` bilingual · `"off"` untouched · `"en_only"` English only · `"append"` force-append), `files` (per-pack, per-FMG separator override, e.g. `{"menu": {"fmg": {"地名.fmg": {"separator": " / "}}}}`).

The separator is chosen automatically: dialogue, subtitles and descriptions use a newline; names, place names and key prompts use ` / `.

### Known limitations

- Text only. If another mod also replaces `msg` files, drop that mod's files into `source\` and rebuild.
- Packs where nothing gets merged are not generated, so the game keeps reading the vanilla copies of those.
- A Chinese line plus an English one that wraps to two lines can sit tight against the bottom of the dialogue box.

---

### License

Scripts: MIT — see [LICENSE](LICENSE). The generated text is modified FromSoftware / Bandai Namco game text, included for offline single-player modding, not for commercial use. Not affiliated with FromSoftware or Bandai Namco.
