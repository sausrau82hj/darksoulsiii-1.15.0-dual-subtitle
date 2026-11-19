# DualSubtitle — Dark Souls III Chinese–English dual-language text · 中英双语文本

DARK SOULS III 1.15.0

[中文](#中文) · [English](#english)

---

## 中文

### 安装

前提：游戏用 UXM / Nuxe 解包过（`Game\msg\` 里是散文件），并且已关闭。
1.替换 `msg` 文件夹。
2.离线启动游戏。

### 卸载

替换 `msg` 文件夹，原文件夹: `...source/msg`。

### 重新生成

需要 **Python 3.9+** 和 [Yabber](https://github.com/JKAnderson/Yabber/releases)。

1. 把 Yabber 解压到本包根目录，例如 `DualSubtitle\Yabber 1.3.1\`（脚本自己会找到，不用配路径）。
2. 在包根目录执行：

```
python tools\dualsub.py
```

不带参数就是默认行为：拿包里的 `source\` 当源，成品写回包里的 `msg\`，跑完按上面第 2 步覆盖进游戏。
要换路径或只重建一部分时才加参数：`--source` / `--out`（这一步的源和成品目录）、`--yabber`（Yabber 不在包内时）、`--filter "menu*"`（只重建匹配的包）、`--list`（导出分类模板到 `tools\dualsub.template.json`）、`--keep-work`（保留中间文件查错）。

配置项：`primary` / `secondary`（默认 `zhocn` / `engus`，可以对调）、`separator`（默认换行）、`default_enabled`（没在 `categories` 里列出的类别是否合并）、`categories`（`true` 双语 · `"off"` 原样 · `"sec_only"` 只留副语言 · `"append"` 强行追加）、`files`（按包、按 FMG 覆盖分隔符，如 `{"menu": {"fmg": {"地名.fmg": {"separator": " / "}}}}`）。

分隔符是自动的：对话、字幕、说明类用换行，名称、地名、按键提示用 ` / `。

### 已知限制

- 只改文本。别的 mod 也换 `msg` 时，把那个 mod 的文件放进 `source\` 再生成。
- 同一句话中文一行、英文可能折成两三行，个别对话会顶到对话框下沿。

### 更精细的修改

[WitchyBND](https://github.com/ividyon/WitchyBND/releases) ：解包，修改，打包，替换。

---

## English

### Install

Requires the loose-file setup (unpacked with UXM / Nuxe, so `Game\msg\` holds real files) and the game closed.
1.Replace the `msg` folder.
2.Start the game offline afterwards.

### Uninstall

Replace the `msg` folder.The orignal folder: `...source/msg`.

### Rebuild

Requires **Python 3.9+** and [Yabber](https://github.com/JKAnderson/Yabber/releases). 

1. Extract Yabber anywhere under the package root, e.g. `DualSubtitle\Yabber 1.3.1\` (the script finds it, no path to configure).
2. From the package root:

```
python tools\dualsub.py
```

No arguments is the default: it reads the bundled `source\` and writes the packs back into the package's `msg\`; then install with step 2 above. 

Arguments only when you need a different path or a partial rebuild: `--source` / `--out` (source and output folders), `--yabber` (Yabber outside the package), `--filter "menu*"` (rebuild matching packs only), `--list` (write the category template to `tools\dualsub.template.json`), `--keep-work` (keep intermediate files).

Config keys: `primary` / `secondary` (default `zhocn` / `engus` — swap them freely), `separator` (default newline), `default_enabled` (whether categories missing from `categories` get merged), `categories` (`true` bilingual · `"off"` untouched · `"en_only"` secondary language only · `"append"` force-append), `files` (per-pack, per-FMG separator override, e.g. `{"menu": {"fmg": {"地名.fmg": {"separator": " / "}}}}`).

The separator is chosen automatically: dialogue, subtitles and descriptions use a newline; names, place names and key prompts use ` / `.

### Known limitations

- Text only. If another mod also replaces `msg` files, drop that mod's files into `source\` and rebuild.
- A Chinese line plus an English one that wraps to two lines can sit tight against the bottom of the dialogue box.

### Finer edits

[WitchyBND](https://github.com/ividyon/WitchyBND/releases): unpack, edit, pack, replace.

---

## License / 许可证

The MIT license in [LICENSE](LICENSE) covers only the Python scripts and the other original files written for this project — `tools/dualsub.py`, `tools/dualsub.config.json`, this README, the changelog. It does not cover the text packs under `msg/` and `source/` (modified FromSoftware / Bandai Namco game text, included for offline single-player modding, not for commercial use), nor the external tools listed in [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md). Not affiliated with FromSoftware or Bandai Namco.
Change history: [CHANGELOG.md](CHANGELOG.md).
