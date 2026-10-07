#!/usr/bin/env python3
"""按 tools/theme.py 里登记的字体，裁出只含本片用到的字符的 woff2，输出到 assets/fonts。

源字体先在工程的 .fonts-src/ 和本机的共享缓存（~/.cache/my-script-explainer-video/fonts）里找，
都没有才下载，下载一次所有工程共用。画面文字或文案一改就要重跑，否则新字会缺字。
用法：.venv/bin/python tools/build_fonts.py
"""
from __future__ import annotations

import importlib
import string
import sys
import time
import urllib.request
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))

from framekit import Font  # noqa: E402

SRC = ROOT / ".fonts-src"
CACHE = Path.home() / ".cache/my-script-explainer-video/fonts"
OUT = ROOT / "assets/fonts"
EXTRA_CHARS = "→·“”‘’？！，。：；、—…≈×％%"
DOWNLOAD_TIMEOUT_S = 300
RETRY_WAITS_S = (0, 3, 8)
RAW_PREFIX = "https://raw.githubusercontent.com/google/fonts/main/"
MIRROR_PREFIX = "https://cdn.jsdelivr.net/gh/google/fonts@main/"
CJK_START = 0x2E80
PARTIAL_MAX_MISSING = 0.7  # 缺字比例低于它才算“中文字体缺了几个字”，高于它说明这本来就是西文字体


def used_chars() -> str:
    sources = [*sorted((ROOT / "compositions").rglob("*.html")), ROOT / "tools/frames.json", ROOT / "tools/video.json"]
    text = "".join(p.read_text(encoding="utf-8") for p in sources if p.exists())
    return "".join(sorted(set(text) | set(string.printable.strip()) | set(EXTRA_CHARS) | {" "}))


def download(url: str, target: Path) -> None:
    """下载到临时文件再改名，避免中断后留下半个文件；主地址失败换镜像。"""
    if not url.startswith("https://"):
        raise SystemExit(f"字体下载地址必须是 https：{url}")
    urls = [url] + ([MIRROR_PREFIX + url[len(RAW_PREFIX):]] if url.startswith(RAW_PREFIX) else [])
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_suffix(target.suffix + ".part")
    last: Exception | None = None
    for wait in RETRY_WAITS_S:
        time.sleep(wait)
        for candidate in urls:
            try:
                with urllib.request.urlopen(candidate, timeout=DOWNLOAD_TIMEOUT_S) as resp:  # noqa: S310 - 上面已限定 https
                    partial.write_bytes(resp.read())
                TTFont(partial).close()
                partial.replace(target)
                return
            except Exception as exc:  # noqa: BLE001 - 网络和文件损坏都换下一个地址重试
                last = exc
    partial.unlink(missing_ok=True)
    raise SystemExit(f"字体 {target.name} 下载失败：{last}\n可以手动下载后放到 {CACHE}/ 再重跑。")


def ensure_source(font: Font) -> Path:
    for folder in (SRC, CACHE):
        if (folder / font.src).exists():
            return folder / font.src
    if not font.url:
        raise SystemExit(f"缺少字体源文件 {font.src}，也没有登记它的下载地址")
    print(f"下载 {font.src} …（只在第一次用到时下载）")
    download(font.url, CACHE / font.src)
    return CACHE / font.src


def build(font: Font, chars: str) -> tuple[int, set[str]]:
    """裁剪一个字体，返回 (文件大小, 它覆盖到的字符)。"""
    tt = TTFont(ensure_source(font))
    covered = {c for c in chars if ord(c) in tt.getBestCmap()}
    opts = subset.Options()
    opts.layout_features = ["*"]
    opts.flavor = "woff2"
    sub = subset.Subsetter(opts)
    sub.populate(text=chars)
    sub.subset(tt)
    if "fvar" in tt:
        present = {a.axisTag for a in tt["fvar"].axes}
        pins = {"wght": font.weight, **font.axes}
        tt = instancer.instantiateVariableFont(tt, {k: v for k, v in pins.items() if k in present})
    tt.flavor = "woff2"
    target = OUT / font.out
    tt.save(target)
    return target.stat().st_size, covered


def main() -> int:
    theme = importlib.import_module("theme").THEME
    OUT.mkdir(parents=True, exist_ok=True)
    for stale in OUT.glob("*.woff2"):
        stale.unlink()
    chars = used_chars()
    covered: set[str] = set()
    partial: dict[str, str] = {}
    for font in theme.fonts:
        size, has = build(font, chars)
        covered |= has
        cjk = [c for c in chars if ord(c) >= CJK_START]
        lacking = "".join(c for c in cjk if c not in has)
        if lacking and len(lacking) < len(cjk) * PARTIAL_MAX_MISSING:
            partial[font.family] = lacking
        print(f"{font.out:36s} {size / 1024:7.1f} KB")
    print(f"字符数 {len(chars)}")
    for family, lacking in partial.items():
        print(f"提示：{family} 里没有这 {len(lacking)} 个字，会用备用中文字体显示：{lacking[:40]}")
    missing = "".join(c for c in chars if ord(c) >= CJK_START and c not in covered)
    if missing:
        print(f"注意：这些字所有字体里都没有，画面上会是方块：{missing}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
