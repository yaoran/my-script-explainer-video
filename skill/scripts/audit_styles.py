#!/usr/bin/env python3
"""检查风格库里每种风格的配色看不看得清（按 WCAG 对比度）。新增或改了风格后跑它。

用法：python3 audit_styles.py [风格名 …]      有问题时逐条列出并以非零退出。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # 不在技能目录里留下 __pycache__
sys.path.insert(0, str(Path(__file__).resolve().parent / "tools"))

from canvas import get_canvas  # noqa: E402
from colors import contrast, readable_on  # noqa: E402
from stylekit import Kit, Look, Style  # noqa: E402
from styles import STYLES  # noqa: E402

BODY_MIN, LARGE_MIN = 4.5, 3.0
BACKGROUND_RE = re.compile(r"background(?:-color)?:\s*([^;]+);")


def plate_color(css: str) -> str:
    m = BACKGROUND_RE.search(css)
    return m.group(1).strip() if m else ""


def look_problems(kit: Kit, which: str) -> list[str]:
    bg, ink = kit.hex("bg"), kit.hex("ink")
    pairs = [
        ("主文字", ink, bg, BODY_MIN),
        ("次要文字 muted", kit.hex("muted"), bg, BODY_MIN),
        ("强调色上的字 on_accent", kit.hex("on_accent"), kit.hex("accent"), BODY_MIN),
        ("彩色的字 pop", kit.hex("pop"), bg, LARGE_MIN),
        ("卡片上的字", ink, kit.hex("surface"), BODY_MIN),
        ("第二强调色上的字", readable_on(kit.hex("accent2"), (ink, bg), bg), kit.hex("accent2"), BODY_MIN),
    ]
    pairs += [(f"调色板 p{i} 上的字", readable_on(color, (ink, bg), bg), color, BODY_MIN) for i, color in enumerate(kit.s.palette)]
    return [f"{which}：{label} 对比度 {contrast(text, ground, bg):.2f}，至少要 {need}（{text} 在 {ground} 上）"
            for label, text, ground, need in pairs if contrast(text, ground, bg) < need]


def caption_problems(kit: Kit, which: str) -> list[str]:
    cap, bg = kit.caption(), kit.hex("bg")
    plate = plate_color(cap.plate) or bg
    active_ground = plate_color(cap.active_css) or plate
    pairs = [("字幕·已说过的词", cap.spoken, plate, BODY_MIN), ("字幕·还没说的词", cap.upcoming, plate, LARGE_MIN),
             ("字幕·正在说的词", cap.active, active_ground, LARGE_MIN)]
    return [f"{which}：{label} 对比度 {contrast(text, ground, bg):.2f}，至少要 {need}（{text} 在 {ground} 上）"
            for label, text, ground, need in pairs if contrast(text, ground, bg) < need]


def style_problems(style: Style) -> list[str]:
    kit = Kit(style, get_canvas("16:9"))
    problems: list[str] = []
    for i, look in enumerate((Look(), *style.looks)):
        kit.look = look
        which = "默认配色" if i == 0 else f"第 {i + 1} 套配色"
        problems += look_problems(kit, which)
        if i == 0 or not plate_color(style.cap_plate):
            problems += caption_problems(kit, which)
    return problems


def main(argv: list[str]) -> int:
    failed = 0
    for name in argv or list(STYLES):
        problems = style_problems(STYLES[name])
        failed += bool(problems)
        for msg in problems:
            print(f"{name}  {msg}")
    print(f"{len(argv or STYLES)} 种风格，{failed} 种有配色问题" if failed else f"{len(argv or STYLES)} 种风格的配色都看得清")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
