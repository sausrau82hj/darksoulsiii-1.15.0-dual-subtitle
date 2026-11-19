# DualSubtitle — Dark Souls III Chinese–English dual-language text · 中英双语文本

DARK SOULS III 1.15.0

[中文](#中文) · [English](#english)

---

## 中文

### 安装

前提：游戏用 UXM / Nuxe 解包过（`Game\msg\` 里是散文件），并且已关闭。
1. 替换 `msg` 文件夹。
2. 离线启动游戏。

### 卸载

替换 `msg` 文件夹，原文件夹: `...source/msg`。

### 重新生成

需要 **Python 3.9+**。发布包里已经带了 Yabber 1.3.1（就在包根目录），不用另外下载。

1. 在包根目录执行：

```
python tools\dualsub.py
```

Yabber 文件夹被删掉、或者换了位置时，把它解压回包根目录就行（如 `Yabber 1.3.1\`），脚本自己会找到，不用配路径。

不带参数就是默认行为：拿包里的 `source\` 当源，成品写回包里的 `msg\`，跑完按上面「安装」那两步覆盖进游戏。
要换路径或只重建一部分时才加参数：`--source` / `--out`（这一步的源和成品目录）、`--yabber`（Yabber 不在包内时）、`--filter "menu*"`（只重建匹配的包）、`--keep-work`（保留中间文件查错）。

配置项：`primary` / `secondary`（默认 `zhocn` / `engus`，可以对调）、`separator`（单行文本的分隔符，默认 `" / "`）、`categories`（取值 `true` 合并双语 · `"off"` 原样不动 · `"sec_only"` 只留副语言）、`files`（例外清单，按包、按 FMG 单独设 `mode` / `enabled` / `separator`，优先级最高，如 `"files": {"menu_dlc2": {"fmg": {"地名.fmg": {"separator": " ~ "}, "アイテムうんちく.fmg": "sec_only"}}}`。

分隔符：原本就带换行的固定用换行，不提供自定义；单行的默认用 ` / `，把 `separator` 改成 `" ~ "` 之类就跟着换。

### 已知限制

- 只改文本。别的 mod 也换 `msg` 时，把那个 mod 的文件放进 `source\` 再生成。
- 同一句话中文一行、英文可能折成两三行，个别对话会顶到对话框下沿。

### 更精细的修改

[WitchyBND](https://github.com/ividyon/WitchyBND/releases) ：解包，修改，打包，替换。

---

## English

### Install

Requires the loose-file setup (unpacked with UXM / Nuxe, so `Game\msg\` holds real files) and the game closed.
1. Replace the `msg` folder.
2. Start the game offline afterwards.

### Uninstall

Replace the `msg` folder.The orignal folder: `...source/msg`.

### Rebuild

Requires **Python 3.9+**. The release zip already includes [Yabber](https://github.com/JKAnderson/Yabber/releases) 1.3.1 in the package root, so there is nothing extra to download.

1. From the package root:

```
python tools\dualsub.py
```

If the Yabber folder was deleted or moved, extract it back under the package root (e.g. `Yabber 1.3.1\`) — the script finds it, no path to configure.

No arguments is the default: it reads the bundled `source\` and writes the packs back into the package's `msg\`; then install as described under Install above. 

Arguments only when you need a different path or a partial rebuild: `--source` / `--out` (source and output folders), `--yabber` (Yabber outside the package), `--filter "menu*"` (rebuild matching packs only), `--keep-work` (keep intermediate files).

Config keys: `primary` / `secondary` (default `zhocn` / `engus` — swap them freely), `separator` (the separator inside one line, default `" / "`), `categories` (`true` merge both · `"off"` untouched · `"sec_only"` secondary language only), `files` (the exception list: per-pack, per-FMG `mode` / `enabled` / `separator`, highest priority, e.g. ` "files": {"menu_dlc2": {"fmg": {"地名.fmg": {"separator": " ~ "}, "アイテムうんちく.fmg": "sec_only"}}}`

Separators: text that already wraps keeps a newline and is not configurable; single-line text uses ` / ` by default, and `separator` changes it to something like `" ~ "`.

### Known limitations

- Text only. If another mod also replaces `msg` files, drop that mod's files into `source\` and rebuild.
- A Chinese line plus an English one that wraps to two lines can sit tight against the bottom of the dialogue box.

### Finer edits

[WitchyBND](https://github.com/ividyon/WitchyBND/releases): unpack, edit, pack, replace.

---

## License / 许可证

The MIT license in [LICENSE](LICENSE) covers only the Python scripts and the other original files written for this project — `tools/dualsub.py`, `tools/dualsub.config.json`, this README, the changelog. It does not cover the text packs under `msg/` and `source/` (modified FromSoftware / Bandai Namco game text, included for offline single-player modding, not for commercial use), nor the external tools listed in [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md). Not affiliated with FromSoftware or Bandai Namco.
Change history: [CHANGELOG.md](CHANGELOG.md).
