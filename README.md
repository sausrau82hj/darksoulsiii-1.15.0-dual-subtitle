# DualSubtitle — Dark Souls III Chinese–English dual-language text · 中英双语文本

DARK SOULS III 1.15.0

[中文](#中文) · [English](#english)

---

## 中文

替换 `Game\msg\<语言>\` 下的 4 个文本包：`menu_dlc1` / `menu_dlc2` / `item_dlc1` / `item_dlc2`（`.msgbnd.dcx`），游戏里能读到的文本全部中英双语。原版这 4 个包本身就是累积包 —— `*_dlc2` 里包含本体、DLC1、DLC2 的全部文本，本体没有单独的 `menu.msgbnd.dcx` / `item.msgbnd.dcx`。exe、params、存档都不动。

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

`tools\dualsub.config.json` 里所有类别都开着：NPC 对话、过场字幕、事件文本、弹窗确认按钮、菜单、按键提示、帮助文本、系统消息、地名、道具名/说明/背景故事、血字留言。逐条合并，不按词跳过 —— `是` / `否` / `确定` / `取消` 也照样带上另一语言。

不想让某一类双语，把它设成 `"off"`；长说明类（道具说明、背景故事）面板放不下两种语言，可设成 `"en_only"` 只看英文。改完重新生成即可。

### 重新生成

需要 **Python 3.9+** 和 [Yabber](https://github.com/JKAnderson/Yabber/releases)。包里不放 .bat / .ps1，只有一条命令：

1. 把 Yabber 解压到本包根目录，例如 `DualSubtitle\Yabber 1.3.1\`（脚本自己会找到，不用配路径）。
2. 在包根目录执行：

```
python tools\dualsub.py
```

不带参数就是默认行为：拿包里的 `source\` 当源，成品写回包里的 `msg\`，跑完按上面第 2 步覆盖进游戏。`source\` 里是原版文本包，所以重复生成不会把双语内容再合并一次。

要换路径或只重建一部分时才加参数：`--source` / `--out`（这一步的源和成品目录）、`--yabber`（Yabber 不在包内时）、`--filter "menu*"`（只重建匹配的包）、`--list`（导出分类模板到 `tools\dualsub.template.json`）、`--keep-work`（保留中间文件查错）。

配置项：`primary` / `secondary`（默认 `zhocn` / `engus`，可以对调）、`separator`（默认换行）、`default_enabled`（没在 `categories` 里列出的类别是否合并）、`categories`（`true` 双语 · `"off"` 原样 · `"en_only"` 只留副语言 · `"append"` 强行追加）、`files`（按包、按 FMG 覆盖分隔符，如 `{"menu": {"fmg": {"地名.fmg": {"separator": " / "}}}}`）。

分隔符是自动的：对话、字幕、说明类用换行，名称、地名、按键提示用 ` / `。

### 已知限制

- 只改文本。别的 mod 也换 `msg` 时，把那个 mod 的文件放进 `source\` 再生成。
- 如果只启用了部分类别，没合并到内容的包不会被生成，游戏继续读原版的那几个包。
- 同一句话中文一行、英文可能折成两三行，个别对话会顶到对话框下沿。

### 更精细的修改

成品是整包替换。个别界面的框子是写死的（比如角色选择那栏的地点、等级，以及道具说明面板），两种语言塞进去会挤到一起或被切掉。想逐条取舍，用 [WitchyBND](https://github.com/ividyon/WitchyBND/releases) 解包：直接把 `msg\zhocn\` 里的 `.msgbnd.dcx` 拖上去，会拆成一个个 `.fmg`；再对 `.fmg` 跑一次，得到可读的 `.xml`。改完按原路径反向跑一遍封回去，覆盖进游戏的 `Game\msg\` 即可。

---

## English

This replaces the 4 text packs under `Game\msg\<language>\`: `menu_dlc1` / `menu_dlc2` / `item_dlc1` / `item_dlc2` (`.msgbnd.dcx`), so all in-game text is bilingual. These packs are cumulative — `*_dlc2` already holds the base game, DLC1 and DLC2 text, and there is no standalone `menu.msgbnd.dcx` / `item.msgbnd.dcx` in the retail game. Exe, params and saves are untouched.

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

Every category in `tools\dualsub.config.json` is on: NPC dialogue, cutscene subtitles, event text, popup confirm buttons, menus, key prompts, help text, system messages, place names, item names/descriptions/lore, blood messages. Merged entry by entry, nothing skipped by word — short answers like `是` / `否` / `确定` / `取消` carry the other language too.

Put a category at `"off"` if you do not want it bilingual; long description panels cannot fit both languages, so `"en_only"` is there to read the English instead. Then rebuild.

### Rebuild

Requires **Python 3.9+** and [Yabber](https://github.com/JKAnderson/Yabber/releases). The package ships no .bat / .ps1 — one command does it:

1. Extract Yabber anywhere under the package root, e.g. `DualSubtitle\Yabber 1.3.1\` (the script finds it, no path to configure).
2. From the package root:

```
python tools\dualsub.py
```

No arguments is the default: it reads the bundled `source\` and writes the packs back into the package's `msg\`; then install with step 2 above. `source\` holds the vanilla packs, so rebuilding never merges already-bilingual text twice.

Arguments only when you need a different path or a partial rebuild: `--source` / `--out` (source and output folders), `--yabber` (Yabber outside the package), `--filter "menu*"` (rebuild matching packs only), `--list` (write the category template to `tools\dualsub.template.json`), `--keep-work` (keep intermediate files).

Config keys: `primary` / `secondary` (default `zhocn` / `engus` — swap them freely), `separator` (default newline), `default_enabled` (whether categories missing from `categories` get merged), `categories` (`true` bilingual · `"off"` untouched · `"en_only"` secondary language only · `"append"` force-append), `files` (per-pack, per-FMG separator override, e.g. `{"menu": {"fmg": {"地名.fmg": {"separator": " / "}}}}`).

The separator is chosen automatically: dialogue, subtitles and descriptions use a newline; names, place names and key prompts use ` / `.

### Known limitations

- Text only. If another mod also replaces `msg` files, drop that mod's files into `source\` and rebuild.
- Packs where nothing gets merged are not generated, so the game keeps reading the vanilla copies of those.
- A Chinese line plus an English one that wraps to two lines can sit tight against the bottom of the dialogue box.

### Finer edits

The shipped packs replace whole files. A few widgets have fixed-size boxes — the location and level rows on the character screen, the item description panel — so both languages can crowd together or get clipped there. To pick entries by hand, unpack with [WitchyBND](https://github.com/ividyon/WitchyBND/releases): drop a `.msgbnd.dcx` from `msg\engus\` on it and it splits into the individual `.fmg` files; run it again on a `.fmg` to get readable `.xml`. Edit, run it once more to pack the file back, then copy the packs into the game's `Game\msg\`.

---

## License / 许可证

The MIT license in [LICENSE](LICENSE) covers only the Python scripts and the other original files written for this project — `tools/dualsub.py`, `tools/dualsub.config.json`, this README, the changelog. It does not cover the text packs under `msg/` and `source/` (modified FromSoftware / Bandai Namco game text, included for offline single-player modding, not for commercial use), nor the external tools listed in [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md). Not affiliated with FromSoftware or Bandai Namco.

**中文**：[LICENSE](LICENSE) 里的 MIT 许可证只覆盖本项目原创的 Python 脚本和其他原创文件 —— `tools\dualsub.py`、`tools\dualsub.config.json`、本 README、CHANGELOG。它不覆盖 `msg/` 和 `source/` 下的文本包（属于修改过的 FromSoftware / Bandai Namco 游戏文本，仅供离线单人游戏 mod 使用，不得商用），也不覆盖 [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md) 里列出的第三方工具。与 FromSoftware、Bandai Namco 无关。

改动记录 / Change history: [CHANGELOG.md](CHANGELOG.md).
