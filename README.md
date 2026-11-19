# DualSubtitle · DS3 中英双语文本 / Chinese–English dual-language text

DARK SOULS III 1.15.0 — 以中文显示时下方给出英文，以英文显示时下方给出中文。

---

## 中文

默认配置下替换 6 个文本包（NPC 对话、过场字幕），`Game\msg\<语言>\menu.msgbnd.dcx / menu_dlc1 / menu_dlc2`。exe、params、存档、道具文本都不动。

### 安装

前提：游戏用 UXM / Nuxe 解包过（`Game\msg\` 里是散文件），并且已关闭。

```powershell
$Game = "X:\Steam\steamapps\common\DARK SOULS III\Game"

# 1) 备份原版（只做一次；menu*.dcx 是本次要换的，item*.dcx 给以后开道具文本留的）
robocopy "$Game\msg" "D:\ds3-msg-backup" menu*.dcx item*.dcx /S

# 2) 覆盖（在本仓库根目录执行）
robocopy msg "$Game\msg" /E
```

装完离线启动游戏。游戏更新或 Steam「验证文件完整性」会冲掉，重跑第 2 步即可（备份不用重做）。

### 卸载

把 `D:\ds3-msg-backup` 里 `zhocn\` 和 `engus\` 下的 `menu*.dcx` 覆盖回 `$Game\msg\` 对应目录（备份里还有 item 包，没装就不用管）。没备份就 Steam 验证完整性，或用 UXM / Nuxe 重新解包。

### 双语范围

| 文本 | 默认 | 说明 |
|---|---|---|
| 会話（NPC 对话） | **开** | 逐条合并，副语言为空的条目保持原样 |
| ムービー字幕（过场字幕） | **开** | 同上 |
| 菜单、按键提示、道具名/说明/背景故事、地名、帮助、血字留言、系统消息、事件文本 | 关 | 保持原版单语 |

要开别的类别，改 `tools\dualsub.config.json` 里的 `categories` 再重新生成。开了道具名/说明/背景故事，成品里就会多出 `item*.msgbnd.dcx`，照第 2 步一起覆盖即可（上面备份已经把 item 包一起备下）。长说明类（道具说明、背景故事）面板放不下两种语言，建议设成 `"en_only"` 只看英文。

### 重新生成

需要 **Python 3.9+** 和 [Yabber](https://github.com/JKAnderson/Yabber/releases)。包里不放 .bat / .ps1，只有一条命令：

1. 把 Yabber 解压到本包根目录，例如 `DualSubtitle\Yabber 1.3.1\`（脚本自己会找到，不用配路径）。
2. 在包根目录执行：

```
python tools\dualsub.py
```

不带参数就是默认行为：拿包里的 `source\` 当源，成品写回包里的 `msg\`，跑完按上面第 2 步覆盖进游戏。`source\` 里是原版文本包，所以重复生成不会把双语内容再合并一次。

要换路径或只重建一部分时才加参数：`--source` / `--out`（这一步的源和成品目录）、`--yabber`（Yabber 不在包内时）、`--filter "menu*"`（只重建匹配的包）、`--list`（导出分类模板到 `tools\dualsub.template.json`）、`--keep-work`（保留中间文件查错）。

配置项：`primary` / `secondary`（默认 `zhocn` / `engus`）、`separator`（默认换行）、`default_enabled`、`skip_merge_texts`（永不合并的短词）、`categories`（`true` 双语 · `"off"` 原样 · `"en_only"` 只换英文 · `"append"` 强行追加）、`files`（按包、按 FMG 覆盖分隔符，如 `{"menu": {"fmg": {"地名.fmg": {"separator": " / "}}}}`）。

分隔符是自动的：对话、字幕、说明类用换行，名称、地名、按键提示用 ` / `。

### 已知限制

- 只改文本。别的 mod 也换 `msg` 时，把那个 mod 的文件放进 `source\` 再生成。
- 如果只启用了部分类别，没合并到内容的包不会被生成，游戏继续读原版的那几个包。
- 同一句话中文一行、英文可能折成两三行，个别对话会顶到对话框下沿。

---

## English

With the default config this replaces 6 text packs — NPC dialogue and cutscene subtitles — `Game\msg\<language>\menu.msgbnd.dcx / menu_dlc1 / menu_dlc2`. Exe, params, saves and item text are untouched.

### Install

Requires the loose-file setup (unpacked with UXM / Nuxe, so `Game\msg\` holds real files) and the game closed.

```powershell
$Game = "X:\Steam\steamapps\common\DARK SOULS III\Game"

# 1) back up the originals (once; menu*.dcx is what gets replaced now, item*.dcx for enabling item text later)
robocopy "$Game\msg" "D:\ds3-msg-backup" menu*.dcx item*.dcx /S

# 2) overwrite (run from this repository's root)
robocopy msg "$Game\msg" /E
```

Start the game offline afterwards. Game updates and Steam "verify integrity" overwrite these files — rerun step 2 (the backup stays valid).

### Uninstall

Copy the `menu*.dcx` files from `D:\ds3-msg-backup\zhocn\` and `\engus\` back into the matching `$Game\msg\` folders (the backup also holds the item packs — ignore them if you never installed them). No backup? Use Steam's verify integrity, or re-unpack with UXM / Nuxe.

### What is bilingual

| Text | Default | Notes |
|---|---|---|
| 会話 (NPC dialogue) | **on** | merged entry by entry; entries with no secondary text stay as they are |
| ムービー字幕 (cutscene subtitles) | **on** | same |
| Menus, key prompts, item names/descriptions/lore, place names, help text, blood messages, system messages, event text | off | vanilla single language |

Turn more on under `categories` in `tools\dualsub.config.json` and rebuild: enabling item names/descriptions/lore also produces `item*.msgbnd.dcx`, which you then copy over with step 2 (the backup above already covers the item packs). Long description panels cannot fit both languages — set those to `"en_only"` to read the English instead.

### Rebuild

Requires **Python 3.9+** and [Yabber](https://github.com/JKAnderson/Yabber/releases). The package ships no .bat / .ps1 — one command does it:

1. Extract Yabber anywhere under the package root, e.g. `DualSubtitle\Yabber 1.3.1\` (the script finds it, no path to configure).
2. From the package root:

```
python tools\dualsub.py
```

No arguments is the default: it reads the bundled `source\` and writes the packs back into the package's `msg\`; then install with step 2 above. `source\` holds the vanilla packs, so rebuilding never merges already-bilingual text twice.

Arguments only when you need a different path or a partial rebuild: `--source` / `--out` (source and output folders), `--yabber` (Yabber outside the package), `--filter "menu*"` (rebuild matching packs only), `--list` (write the category template to `tools\dualsub.template.json`), `--keep-work` (keep intermediate files).

Config keys: `primary` / `secondary` (default `zhocn` / `engus`), `separator` (default newline), `default_enabled`, `skip_merge_texts` (short strings never merged), `categories` (`true` bilingual · `"off"` untouched · `"en_only"` English only · `"append"` force-append), `files` (per-pack, per-FMG separator override, e.g. `{"menu": {"fmg": {"地名.fmg": {"separator": " / "}}}}`).

The separator is chosen automatically: dialogue, subtitles and descriptions use a newline; names, place names and key prompts use ` / `.

### Known limitations

- Text only. If another mod also replaces `msg` files, drop that mod's files into `source\` and rebuild.
- Packs where nothing gets merged are not generated, so the game keeps reading the vanilla copies of those.
- A Chinese line plus an English one that wraps to two lines can sit tight against the bottom of the dialogue box.

---

### License

Scripts: MIT — see [LICENSE](LICENSE). The generated text is modified FromSoftware / Bandai Namco game text, included for offline single-player modding, not for commercial use. Not affiliated with FromSoftware or Bandai Namco.
