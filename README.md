# DualSubtitle — Dark Souls III Chinese–English dual-language text · 中英双语文本

DARK SOULS III 1.15.0

[中文](#中文) · [English](#english)

---

## 中文

替换 `Game\msg\<语言>\` 下的 6 个文本包：`menu` / `menu_dlc1` / `menu_dlc2` / `item` / `item_dlc1` / `item_dlc2`（`.msgbnd.dcx`）。游戏里能读到的文本全部中英双语。exe、params、存档都不动。

### 安装

前提：游戏用 UXM / Nuxe 解包过（`Game\msg\` 里是散文件），并且已关闭。

```powershell
$Game = "X:\Steam\steamapps\common\DARK SOULS III\Game"

# 1) 备份原版（只做一次；menu*.dcx 和 item*.dcx 都会被替换）
robocopy "$Game\msg" "D:\ds3-msg-backup" menu*.dcx item*.dcx /S

# 2) 覆盖（在本仓库根目录执行）
robocopy msg "$Game\msg" /E
```

装完离线启动游戏。游戏更新或 Steam「验证文件完整性」会冲掉，重跑第 2 步即可（备份不用重做）。

### 卸载

把 `D:\ds3-msg-backup` 里 `zhocn\` 和 `engus\` 下的 `menu*.dcx`、`item*.dcx` 覆盖回 `$Game\msg\` 对应目录。没备份就 Steam 验证完整性，或用 UXM / Nuxe 重新解包。

### 双语范围

`tools\dualsub.config.json` 里所有类别都开着，六个包里能配上的条目全部双语：NPC 对话、过场字幕、事件文本、弹窗确认按钮、菜单、按键提示和一行帮助、系统消息、地名、道具名/说明/背景故事、血字留言。**逐条合并，不按词跳过** —— `是` / `否` / `确定` / `取消` 也照样带上另一语言。

不想让某一类双语，把它设成 `"off"`；长说明面板塞不下两种语言时可设成 `"en_only"` 只看英文。改完执行下面的重新生成。

### 重新生成

需要 **Python 3.9+** 和 [Yabber](https://github.com/JKAnderson/Yabber/releases)。包里不放 .bat / .ps1，只有一条命令：

1. 把 Yabber 解压到本包根目录，例如 `DualSubtitle\Yabber 1.3.1\`（脚本自己会找到，不用配路径）。
2. 在包根目录执行：

```
python tools\dualsub.py
```

不带参数就是默认行为：拿包里的 `source\` 当源，成品写回包里的 `msg\`，跑完按上面第 2 步覆盖进游戏。`source\` 里是原版文本包，所以重复生成不会把双语内容再合并一次。

要换路径或只重建一部分时才加参数：`--source` / `--out`（这一步的源和成品目录）、`--yabber`（Yabber 不在包内时）、`--filter "menu*"`（只重建匹配的包）、`--list`（导出分类模板到 `tools\dualsub.template.json`）、`--keep-work`（保留中间文件查错）。

配置项：`primary` / `secondary`（默认 `zhocn` / `engus`，可以对调）、`separator`（默认换行）、`default_enabled`（没在 `categories` 里列出的类别是否合并）、`keep_single`（可选，默认空：把某个词填进去就保持单语，例如固定宽度标签 `["等级"]`）、`categories`（`true` 双语 · `"off"` 原样 · `"en_only"` 只留副语言 · `"append"` 强行追加）、`files`（按包、按 FMG 覆盖分隔符，如 `{"menu": {"fmg": {"地名.fmg": {"separator": " / "}}}}`）。

分隔符是自动的：对话、字幕、说明用换行，名称、地名、按键提示、弹窗按钮用 ` / `。

### 已知限制

- 只改文本。别的 mod 也换 `msg` 时，把那个 mod 的文件放进 `source\` 再生成。
- 如果只启用了部分类别，没合并到内容的包不会被生成，游戏继续读原版的那几个包。
- 同一句话中文一行、英文可能折成两三行，个别对话会顶到对话框下沿；菜单标签和道具说明也一样会变长，个别会被截掉。
- 道具说明/背景故事的面板高度是固定的，中英两段放不下，底部会被切掉 —— 在意就把这两类设成 `"en_only"`。
- 「结束游戏」/角色选择界面的三行写死在 `menu\05_010_profileselect.gfx` 的窄文本框里（地点值约 147px、等级标签约 50px，都只有一行）：「等级 / Level」会压到右边的数字，地点只显示得出中文。位置和宽度不在文本包里，改不了；在意就在 `keep_single` 里填 `"等级"`，或把 `Place Names` 设成 `"off"`。

---

## English

This replaces the 6 text packs under `Game\msg\<language>\`: `menu` / `menu_dlc1` / `menu_dlc2` / `item` / `item_dlc1` / `item_dlc2` (`.msgbnd.dcx`). All in-game text is bilingual. Exe, params and saves are untouched.

### Install

Requires the loose-file setup (unpacked with UXM / Nuxe, so `Game\msg\` holds real files) and the game closed.

```powershell
$Game = "X:\Steam\steamapps\common\DARK SOULS III\Game"

# 1) back up the originals (once; both menu*.dcx and item*.dcx get replaced)
robocopy "$Game\msg" "D:\ds3-msg-backup" menu*.dcx item*.dcx /S

# 2) overwrite (run from this repository's root)
robocopy msg "$Game\msg" /E
```

Start the game offline afterwards. Game updates and Steam "verify integrity" overwrite these files — rerun step 2 (the backup stays valid).

### Uninstall

Copy the `menu*.dcx` and `item*.dcx` files from `D:\ds3-msg-backup\zhocn\` and `\engus\` back into the matching `$Game\msg\` folders. No backup? Use Steam's verify integrity, or re-unpack with UXM / Nuxe.

### What is bilingual

Every category in `tools\dualsub.config.json` is on, so every entry that pairs up in those six packs is bilingual: NPC dialogue, cutscene subtitles, event text, popup confirm buttons, menus, key prompts and one-line help, system messages, place names, item names/descriptions/lore, blood messages. **Nothing is skipped by word** — short answers like `是` / `否` / `确定` / `取消` carry the other language too.

Put a category at `"off"` if you do not want it bilingual; use `"en_only"` for panels that cannot fit both languages. Then rebuild below.

### Rebuild

Requires **Python 3.9+** and [Yabber](https://github.com/JKAnderson/Yabber/releases). The package ships no .bat / .ps1 — one command does it:

1. Extract Yabber anywhere under the package root, e.g. `DualSubtitle\Yabber 1.3.1\` (the script finds it, no path to configure).
2. From the package root:

```
python tools\dualsub.py
```

No arguments is the default: it reads the bundled `source\` and writes the packs back into the package's `msg\`; then install with step 2 above. `source\` holds the vanilla packs, so rebuilding never merges already-bilingual text twice.

Arguments only when you need a different path or a partial rebuild: `--source` / `--out` (source and output folders), `--yabber` (Yabber outside the package), `--filter "menu*"` (rebuild matching packs only), `--list` (write the category template to `tools\dualsub.template.json`), `--keep-work` (keep intermediate files).

Config keys: `primary` / `secondary` (default `zhocn` / `engus` — swap them freely), `separator` (default newline), `default_enabled` (whether categories missing from `categories` get merged), `keep_single` (optional, empty by default: list a word to keep it single language, e.g. `["等级"]` for a fixed-width label), `categories` (`true` bilingual · `"off"` untouched · `"en_only"` secondary language only · `"append"` force-append), `files` (per-pack, per-FMG separator override, e.g. `{"menu": {"fmg": {"地名.fmg": {"separator": " / "}}}}`).

The separator is chosen automatically: dialogue, subtitles and descriptions use a newline; names, place names, key prompts and popup buttons use ` / `.

### Known limitations

- Text only. If another mod also replaces `msg` files, drop that mod's files into `source\` and rebuild.
- Packs where nothing gets merged are not generated, so the game keeps reading the vanilla copies of those.
- A Chinese line plus an English one that wraps to two lines can sit tight against the bottom of the dialogue box; menu labels and item text grow the same way and some get clipped.
- The item description / lore panel has a fixed height and cannot fit both languages — the bottom is cut off. Set those two categories to `"en_only"` if that bothers you.
- The three rows on the quit / profile screen live in narrow single-line text fields inside `menu\05_010_profileselect.gfx` (place value ~147px, level label ~50px): `等级 / Level` covers the number to its right and the place name only shows the Chinese half. Position and width are not part of the text packs, so they cannot be changed here; add `"等级"` to `keep_single` or set `Place Names` to `"off"` if it bothers you.

---

### License

Scripts: MIT — see [LICENSE](LICENSE). The generated text is modified FromSoftware / Bandai Namco game text, included for offline single-player modding, not for commercial use. Not affiliated with FromSoftware or Bandai Namco.
