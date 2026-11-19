#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dark Souls III dual-language text tool (default: Chinese primary, English secondary).

How it works (UXM loose-file setup):
  1. read the text packs from <game>/msg/<lang>/*.msgbnd.dcx (zhocn + engus)
  2. unpack DCX -> BND4 -> FMG with Yabber, giving <lang>/msg/<LANG>/64bit/*.fmg
  3. merge both languages entry by entry into "Chinese\\nEnglish" and write it into both
     language slots (the Chinese client shows English underneath, and vice versa)
  4. the config decides which FMGs (area titles / dialogue / items / menus / tutorials ...)
     take part
  5. repack into .msgbnd.dcx into the mod folder for UXM loose-file loading

Usage:
  python dualsub.py --list                        # write the category template
  python dualsub.py                               # build everything from the config
  python dualsub.py --filter menu_dlc1            # only one pack (debugging)
  python dualsub.py --game "D:\\...\\Game" --out <folder>
"""
from __future__ import annotations

import argparse
import fnmatch
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

YABBER_DIR = os.environ.get("YABBER_DIR", "")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Package root: when the script lives in <package>/tools/ this is the package root,
# and the output defaults to <package>/msg/
PACK_ROOT = os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR).lower() == "tools" else SCRIPT_DIR
# Default output is DualSubtitle/ next to the script (only used when the script was moved
# out on its own and has no source/ next to it)
DEFAULT_OUT = os.path.join(SCRIPT_DIR, "DualSubtitle")
DEFAULT_CONFIG = os.path.join(SCRIPT_DIR, "dualsub.config.json")

YABBER_HELP = (
    "Yabber not found.\n"
    "  Extract Yabber anywhere under this package's root folder, or pass --yabber <dir>,\n"
    "  set \"yabber_dir\" in the config, or set the YABBER_DIR environment variable.\n"
    "  The folder must hold both Yabber.exe and Yabber.DCX.exe.\n"
    "  Download: https://github.com/JKAnderson/Yabber/releases"
)


def find_yabber(hint: str = "") -> str:
    """Locate the Yabber folder (must hold both Yabber.exe and Yabber.DCX.exe)."""
    cands = []
    if hint:
        cands.append(hint)
    if YABBER_DIR:
        cands.append(YABBER_DIR)
    exe = shutil.which("Yabber.exe") or shutil.which("Yabber")
    if exe:
        cands.append(os.path.dirname(os.path.abspath(exe)))
    # Look inside the package first: <package>\Yabber*, <package>\tools\Yabber*,
    # <package>\<any subfolder>\Yabber.exe (extracting Yabber into the package root is enough)
    roots = [
        PACK_ROOT, os.path.join(PACK_ROOT, "tools"),
        r"D:\game\TOOL", r"D:\Tools", r"D:\tool", r"C:\Tools", r"C:\tool",
        os.environ.get("LOCALAPPDATA", ""), os.path.expanduser("~\\Downloads"),
        os.path.expanduser("~"),
    ]
    for root in roots:
        if not root or not os.path.isdir(root):
            continue
        for pat in ("Yabber*", os.path.join("*", "Yabber*")):
            cands.extend(sorted(glob.glob(os.path.join(root, pat))))
    for c in cands:
        if c and os.path.isfile(os.path.join(c, "Yabber.exe")) \
                and os.path.isfile(os.path.join(c, "Yabber.DCX.exe")):
            return os.path.abspath(c)
    raise SystemExit(YABBER_HELP)


def default_game() -> str:
    """Locate the DS3 Game folder (environment variable -> Steam library -> usual paths)."""
    env = os.environ.get("DS3_GAME_DIR", "")
    if env and os.path.isfile(os.path.join(env, "DarkSoulsIII.exe")):
        return env
    roots = []
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam") as k:
            steam = winreg.QueryValueEx(k, "SteamPath")[0]
        roots.append(steam)
        vdf = os.path.join(steam, "steamapps", "libraryfolders.vdf")
        if os.path.isfile(vdf):
            with open(vdf, encoding="utf-8", errors="replace") as fh:
                for m in re.finditer(r'"path"\s+"([^"]+)"', fh.read()):
                    roots.append(m.group(1).replace("\\\\", "\\"))
    except Exception:
        pass
    roots += [r"D:\steam\steamapps\common", r"E:\steam\steamapps\common",
              r"F:\steam\steamapps\common", r"C:\Program Files (x86)\Steam\steamapps\common"]
    for r in roots:
        cand = os.path.join(r, "DARK SOULS III", "Game")
        if os.path.isfile(os.path.join(cand, "DarkSoulsIII.exe")):
            return cand
    return r"D:\steam\steamapps\common\DARK SOULS III\Game"

NULL_MARKERS = {"%null%", "null", ""}

def norm(t: str) -> str:
    return re.sub(r"\s+", "", t or "").lower()


def is_null(t) -> bool:
    return t is None or t.strip().lower() in NULL_MARKERS


def is_already_merged(t1: str, t2: str, sep: str) -> bool:
    """True when this text pair is already merged (A+sep+B / B+sep+A), so a rebuild skips it."""
    if not sep:
        return False
    if t1.endswith(sep + t2) or t2.endswith(sep + t1):
        return True
    a, b = t1.split(sep), t2.split(sep)
    # The merged pair holds the same fragments in opposite order; multiline text splits into
    # three or more pieces, so compare the sorted fragment sets
    return len(a) > 1 and len(b) > 1 and sorted(a) == sorted(b)


class Yabber:
    def __init__(self, directory: str):
        self.exe = os.path.join(directory, "Yabber.exe")
        self.dcx = os.path.join(directory, "Yabber.DCX.exe")
        for p in (self.exe, self.dcx):
            if not os.path.exists(p):
                raise SystemExit(f"Yabber not found in: {directory}\n{YABBER_HELP}")

    def run(self, tool: str, path: str) -> None:
        proc = subprocess.run([tool, path], capture_output=True, text=True,
                              encoding="utf-8", errors="replace")
        if proc.returncode != 0:
            raise RuntimeError(f"Yabber failed: {path}\n{proc.stdout}\n{proc.stderr}")


class FmgXml:
    """Yabber XML of an FMG: <fmg><entries><text id=\"...\">text</text>..."""

    def __init__(self, path: str):
        self.path = path
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        self.entries = {}
        parent = self.root.find("entries")
        if parent is None:
            raise RuntimeError(f"Not a valid FMG XML: {path}")
        for el in parent:
            self.entries[el.attrib.get("id")] = el

    def write(self) -> None:
        self.tree.write(self.path, xml_declaration=True, encoding="utf-8")

    def merge(self, other: "FmgXml", sep, log) -> int:
        """Append every text of other behind self, and self behind other.
        sep=None picks per entry: a newline when the source has one, otherwise ' / '
        (single-line widgets). Every entry is merged, short answers such as yes/no included.
        Returns the number of edits."""
        changed = 0
        for key, el in self.entries.items():
            other_el = other.entries.get(key)
            if other_el is None:
                continue
            t1, t2 = el.text, other_el.text
            if is_null(t1) or is_null(t2):
                continue
            if norm(t1) == norm(t2):
                continue
            use_sep = sep
            if use_sep is None:
                use_sep = "\n" if ("\n" in t1 or "\n" in t2) else " / "
            # Idempotent: entries that are already merged (A+sep+B / B+sep+A) are skipped, so a
            # rebuild never stacks the two languages twice
            if is_already_merged(t1, t2, use_sep):
                continue
            new1, new2 = t1 + use_sep + t2, t2 + use_sep + t1
            el.text, other_el.text = new1, new2
            changed += 1
            if len(new1) > 400:
                log(f"  ! entry {key} is long after merge ({len(new1)} chars)")
        return changed

    def replace_texts_from(self, other: "FmgXml") -> int:
        """en_only mode: replace the text of this file with the other language."""
        changed = 0
        for key, el in self.entries.items():
            other_el = other.entries.get(key)
            if other_el is None:
                continue
            if is_null(other_el.text):
                continue
            # Fill in the secondary language even when this language is empty (%null%), otherwise the
            # player still sees a blank line
            if not is_null(el.text) and norm(el.text) == norm(other_el.text):
                continue
            el.text = other_el.text
            changed += 1
        return changed


def find_fmg_dir(unpacked: str) -> str:
    for root, _dirs, files in os.walk(unpacked):
        if any(f.lower().endswith(".fmg") for f in files):
            return root
    raise RuntimeError(f"No FMG found in unpacked dir: {unpacked}")


def stem_of(path: str) -> str:
    name = os.path.basename(path)
    for suffix in (".msgbnd.dcx", ".msgbnd"):
        if name.lower().endswith(suffix):
            return name[: -len(suffix)]
    return os.path.splitext(name)[0]


def load_config(path: str) -> dict:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return {"primary": "zhocn", "secondary": "engus", "separator": "\n",
            "default_enabled": True, "categories": dict(DEFAULT_CATEGORIES)}


# English category names -> internal FMG filename patterns (first match wins)
CATEGORY_RULES = [
    ("Dialogue", ["会話*"]),
    ("Cutscene Subtitles", ["ムービー字幕*"]),
    ("Dialogue Boxes", ["ダイアログ*", "FDP_ダイアログ*"]),
    ("Event Text", ["イベントテキスト*"]),
    ("Menu Text", ["*メニューテキスト*", "メニューその他*", "メニュー共通テキスト*", "インゲームメニュー*"]),
    ("Key Prompts", ["キーガイド*", "FDP_キーガイド*"]),
    ("Help Text", ["*一行ヘルプ*", "項目ヘルプ*"]),
    ("System Messages", ["FDP_システムメッセージ*"]),
    ("Place Names", ["地名*"]),
    ("Item Lore", ["*うんちく*"]),
    ("Item Descriptions", ["*説明*"]),
    ("Item Names", ["*名.fmg", "*名_dlc*.fmg", "NPC名*"]),
    ("Blood Messages", ["血文字*"]),
]

DEFAULT_CATEGORIES = {
    "Dialogue": True,
    "Cutscene Subtitles": True,
    "Dialogue Boxes": True,
    "Event Text": True,
    "Menu Text": True,
    "Key Prompts": True,
    "Help Text": True,
    "System Messages": True,
    "Place Names": True,
    "Item Names": True,
    "Item Descriptions": True,
    "Item Lore": True,
    "Blood Messages": True,
    "Other": True,
}

def category_of(fmg: str) -> str:
    base = os.path.basename(fmg)
    for name, pats in CATEGORY_RULES:
        if any(fnmatch.fnmatchcase(base, p) for p in pats):
            return name
    return "Other"


def _cat_value(cfg: dict, fmg: str):
    cats = cfg.get("categories")
    if not cats:
        return None
    return cats.get(category_of(fmg))


def _value_mode(v) -> str:
    """Normalise a category value into a mode: append / off / en_only"""
    if isinstance(v, dict):
        if v.get("mode"):
            return str(v["mode"])
        return "append" if v.get("enabled", True) else "off"
    if isinstance(v, str):
        return v
    return "append" if v else "off"


def enabled_for(cfg: dict, msgbnd: str, fmg: str) -> bool:
    v = _cat_value(cfg, fmg)
    if v is not None:
        return _value_mode(v) != "off"
    node = cfg.get("files", {})
    for key in (msgbnd, stem_of(msgbnd)):
        if key in node:
            entry = node[key]
            if not entry.get("enabled", cfg.get("default_enabled", True)):
                return False
            rules = entry.get("fmg", {})
            for pat, val in rules.items():
                if fnmatch.fnmatchcase(fmg, pat):
                    if isinstance(val, dict):
                        return bool(val.get("enabled", True))
                    return bool(val)
    # Unlisted files fall back to the default; FMG-level rules apply globally
    rules = cfg.get("fmg", {})
    for pat, val in rules.items():
        if fnmatch.fnmatchcase(fmg, pat):
            if isinstance(val, dict):
                return bool(val.get("enabled", True))
            return bool(val)
    return cfg.get("default_enabled", True)


def mode_for(cfg: dict, pack: str, fmg: str) -> str:
    """Merge modes:
      append  - append the other language (default)
      off     - do not merge (the default for long descriptions, which would not fit)
      en_only - replace this language with English (for text you want to read in English)
    """
    v = _cat_value(cfg, fmg)
    if v is not None:
        return _value_mode(v)
    entry = cfg.get("files", {}).get(stem_of(pack), {}).get("fmg", {})
    v = entry.get(fmg)
    if isinstance(v, dict) and v.get("mode"):
        return v["mode"]
    base = os.path.splitext(fmg)[0]
    if any(m in base for m in ("説明", "うんちく")):
        return "off"
    return "append"


def discover(game: str, primary: str, secondary: str) -> list[str]:
    """Text packs that exist in both languages and can be paired."""
    a = os.path.join(game, "msg", primary)
    b = os.path.join(game, "msg", secondary)
    if not os.path.isdir(a) or not os.path.isdir(b):
        raise SystemExit(f"msg language dirs not found: {a} / {b}")
    names = {f.lower(): f for f in os.listdir(a) if f.lower().endswith(".msgbnd.dcx")}
    have = {f.lower() for f in os.listdir(b)}
    return sorted(names[k] for k in names if k in have)


def separator_for(cfg: dict, pack: str, fmg: str) -> str:
    """Pick the separator between the two languages: ' / ' for single-line widgets
    (names / place names / prompts), a newline for multiline ones (dialogue and
    descriptions). The config can override it per FMG."""
    stem = stem_of(pack)
    entry = cfg.get("files", {}).get(stem, {}).get("fmg", {})
    v = entry.get(fmg)
    if isinstance(v, dict) and v.get("separator") is not None:
        return v["separator"]
    base = os.path.splitext(fmg)[0]
    # Popup confirm windows: buttons are one line, message rows keep their own newline
    if base.startswith("FDP_ダイアログ"):
        return None
    # Multiline widgets: dialogue / subtitles / long descriptions -> newline
    multiline_marks = ("会話", "ムービー字幕", "説明", "うんちく", "ダイアログ")
    if any(m in base for m in multiline_marks):
        return "\n"
    # Single-line widgets: names / place names / menus / prompts -> one line
    one_line_marks = (
        "名.fmg", "地名", "一行ヘルプ", "キーガイド", "システムメッセージ",
        "メニューテキスト", "インゲームメニュー", "項目ヘルプ",
    )
    if any(m in base for m in one_line_marks) or base.endswith("名"):
        return " / "
    # Everything else is decided per entry (short labels one line, long text a newline)
    return None


def build_one(game: str, out: str, cfg: dict, name: str, log, keep_work: bool,
              yabber_dir: str = "") -> dict:
    primary, secondary = cfg["primary"], cfg["secondary"]
    sep = cfg.get("separator", "\n")
    if sep == "\\n":
        sep = "\n"
    stem = stem_of(name)
    work = os.path.join(out, "_work", stem)
    if os.path.isdir(work):
        shutil.rmtree(work)
    os.makedirs(work, exist_ok=True)

    y = Yabber(yabber_dir or cfg.get("yabber_dir") or find_yabber())
    stats = {"file": name, "fmg_total": 0, "fmg_merged": 0, "entries": 0, "skipped_fmg": 0}

    results = {}  # lang -> final dcx path
    for lang in (primary, secondary):
        src = os.path.join(game, "msg", lang, name)
        wdir = os.path.join(work, lang)
        os.makedirs(wdir, exist_ok=True)
        dcx = os.path.join(wdir, name)
        shutil.copy2(src, dcx)
        y.run(y.dcx, dcx)                      # DCX -> msgbnd
        msgbnd = dcx[:-4]
        y.run(y.exe, msgbnd)                   # BND4 -> folder
        unpacked = os.path.join(wdir, f"{stem}-msgbnd")
        fmg_dir = find_fmg_dir(unpacked)
        results[lang] = {"dcx": dcx, "msgbnd": msgbnd, "unpacked": unpacked, "fmg_dir": fmg_dir}

    fmg_dirs = {lang: results[lang]["fmg_dir"] for lang in results}
    all_fmg = sorted({f for d in fmg_dirs.values() for f in os.listdir(d) if f.lower().endswith(".fmg")})
    stats["fmg_total"] = len(all_fmg)

    primary_fmgs = set(os.listdir(fmg_dirs[primary]))
    secondary_fmgs = set(os.listdir(fmg_dirs[secondary]))

    for fmg in all_fmg:
        if fmg not in primary_fmgs or fmg not in secondary_fmgs:
            log(f"  - skip {fmg} (missing on one side)")
            stats["skipped_fmg"] += 1
            continue
        if not enabled_for(cfg, name, fmg):
            log(f"  - off {fmg}")
            stats["skipped_fmg"] += 1
            continue
        fmg_mode = mode_for(cfg, name, fmg)
        if fmg_mode == "off":
            log(f"  - skip {fmg} (long text, keep original)")
            stats["skipped_fmg"] += 1
            continue
        p1 = os.path.join(fmg_dirs[primary], fmg)
        p2 = os.path.join(fmg_dirs[secondary], fmg)
        y.run(y.exe, p1)                       # fmg -> xml
        y.run(y.exe, p2)
        x1, x2 = FmgXml(p1 + ".xml"), FmgXml(p2 + ".xml")
        if fmg_mode == "en_only":
            n = x1.replace_texts_from(x2)
        else:
            fmg_sep = separator_for(cfg, name, fmg)
            n = x1.merge(x2, fmg_sep, log)
        if n:
            x1.write(); x2.write()
            y.run(y.exe, p1 + ".xml")          # xml -> fmg
            y.run(y.exe, p2 + ".xml")
            stats["fmg_merged"] += 1
            stats["entries"] += n
            log(f"  + {fmg}: {n} entries")
        else:
            log(f"  = {fmg}: nothing to merge")

    if not stats["entries"]:
        # Nothing merged -> the pack is identical to vanilla, so shipping it only adds risk: skip it
        log(f"  = nothing merged in {name}, not installed")
        if not keep_work:
            shutil.rmtree(work, ignore_errors=True)
        return stats

    for lang in (primary, secondary):
        r = results[lang]
        y.run(y.exe, r["unpacked"])            # folder -> msgbnd
        y.run(y.dcx, r["msgbnd"])              # msgbnd -> dcx
        dst = os.path.join(out, "msg", lang, name)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(r["msgbnd"] + ".dcx", dst)
        log(f"  -> {dst}")

    if not keep_work:
        shutil.rmtree(work, ignore_errors=True)
    return stats


def do_list(cfg_path: str, primary: str, secondary: str) -> None:
    """Write a category template (needs no game folder and no Japanese file names)."""
    template = {
        "primary": primary,
        "secondary": secondary,
        "separator": "\n",
        "default_enabled": True,
        "categories": dict(DEFAULT_CATEGORIES),
    }
    with open(cfg_path, "w", encoding="utf-8") as fh:
        json.dump(template, fh, ensure_ascii=False, indent=2)
    print(f"Wrote category config: {cfg_path}")
    print("Available categories:")
    for name in list(DEFAULT_CATEGORIES):
        print(f"  - {name}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Dark Souls III dual-language text pack builder")
    ap.add_argument("--game", default=None, help="game folder holding msg/ (auto-detected by default)")
    ap.add_argument("--out", default=None, help="output folder (default: the package's msg/)")
    ap.add_argument("--config", default=DEFAULT_CONFIG, help="config file to read")
    ap.add_argument("--yabber", default="", help="folder holding Yabber.exe and Yabber.DCX.exe")
    ap.add_argument("--primary", default=None, help="primary language folder (default zhocn)")
    ap.add_argument("--secondary", default=None, help="secondary language folder (default engus)")
    ap.add_argument("--filter", default=None, help="only build packs whose name matches this wildcard")
    ap.add_argument("--source", default=None, help="vanilla msg folder (default: same as --game)")
    ap.add_argument("--list", action="store_true", help="write the category template to tools/dualsub.template.json")
    ap.add_argument("--keep-work", action="store_true", help="keep the intermediate files")
    args = ap.parse_args(argv)
    # When run with no arguments (e.g. double-clicked in Explorer) keep the window open at the end
    interactive = not (argv if argv is not None else sys.argv[1:])

    cfg = load_config(args.config)
    if args.primary:
        cfg["primary"] = args.primary
    if args.secondary:
        cfg["secondary"] = args.secondary
    primary, secondary = cfg.get("primary", "zhocn"), cfg.get("secondary", "engus")

    if args.list:
        # Template export only: no game folder needed, and the active config is not overwritten by default
        if os.path.abspath(args.config) == os.path.abspath(DEFAULT_CONFIG):
            args.config = os.path.join(os.path.dirname(DEFAULT_CONFIG), "dualsub.template.json")
        do_list(args.config, primary, secondary)
        return 0

    # With a bundled source\ the default is an in-place rebuild: read source\, write <package>/msg\
    pack_src = os.path.join(PACK_ROOT, "source")
    use_pack_src = args.source is None and os.path.isdir(os.path.join(pack_src, "msg"))
    src_game = (pack_src if use_pack_src else None) or args.source or args.game or default_game()
    if not os.path.isdir(src_game):
        raise SystemExit(f"Text pack directory not found: {src_game}\n"
                         "Point --source at the package's source folder, or --game at the game's Game folder.")

    if not args.out:
        args.out = PACK_ROOT if use_pack_src else DEFAULT_OUT
        print(f"Writing to {args.out}")

    names = discover(src_game, primary, secondary)
    # ngword holds the profanity list and never takes part in the dual-language display
    names = [n for n in names if not stem_of(n).lower().startswith("ngword")]
    if args.filter:
        names = [n for n in names if fnmatch.fnmatchcase(stem_of(n), args.filter)]
    if not names:
        raise SystemExit("No text packs to process (base text may not be unpacked)")

    t0 = time.time()
    print(f"Source: {src_game}")
    print(f"Output: {args.out}")
    print(f"Languages: {primary} + {secondary}, {len(names)} packs\n")
    all_stats = []
    for name in names:
        print(f"[{name}]")
        all_stats.append(build_one(src_game, args.out, cfg, name, print, args.keep_work, args.yabber))
        print()

    # Base-game text files: without a loose copy the game falls back to the archived original
    # of menu.msgbnd / item.msgbnd, so base-game text would not apply. Copy the result of the
    # cumulative DLC2 (or DLC1) build under the base file name, for the packs that really
    # merged something this run (a pack that merged nothing is not shipped).
    built = {stem_of(s["file"]) for s in all_stats if s["entries"]}
    for base in ("menu", "item"):
        for lang in (primary, secondary):
            for cand in (f"{base}_dlc2.msgbnd.dcx", f"{base}_dlc1.msgbnd.dcx"):
                if stem_of(cand) not in built:
                    continue
                src = os.path.join(args.out, "msg", lang, cand)
                if os.path.exists(src):
                    dst = os.path.join(args.out, "msg", lang, f"{base}.msgbnd.dcx")
                    shutil.copy2(src, dst)
                    print(f"[base] {lang}\\{base}.msgbnd.dcx <- {cand}")
                    break

    total_fmg = sum(s["fmg_merged"] for s in all_stats)
    total_entries = sum(s["entries"] for s in all_stats)
    print(f"Done: {len(all_stats)} packs, {total_fmg} FMGs, {total_entries} entries, "
          f"in {time.time() - t0:.1f}s")
    print(f"Mod files in: {args.out}")
    if interactive and sys.stdin is not None and sys.stdin.isatty():
        try:
            input("\nPress Enter to close")
        except EOFError:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
