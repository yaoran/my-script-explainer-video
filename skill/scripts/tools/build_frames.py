#!/usr/bin/env python3
"""把 tools/frames_*.py 里的 frame_NN() 渲染成 compositions/frames/NN-slug.html，并做版面自检。

镜头清单来自 tools/frames.json，逐词时间来自 audio_meta.json，视觉设定来自 tools/theme.py。
自检不过（元素出框、落进字幕区、动画选中了不存在的元素）会列出问题并以非零退出。
用法：.venv/bin/python tools/build_frames.py
"""
from __future__ import annotations

import importlib
import re
import sys
from collections.abc import Callable
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))

from framekit import render_frame  # noqa: E402
from project import load_frames, load_video, load_voices, kit_style, timeline  # noqa: E402

FRAME_FN_RE = re.compile(r"frame_(\d+)")
SELECTOR_RE = re.compile(r"([#.])§([\w-]+)")
EDGE_TOLERANCE_PX = 6
FrameBuilder = Callable[[], tuple]


def load_builders(tools: Path) -> dict[int, FrameBuilder]:
    """收集所有 frames_*.py 里定义的 frame_NN；同一镜号出现两次直接报错。"""
    builders: dict[int, FrameBuilder] = {}
    for path in sorted(tools.glob("frames_*.py")):
        module = importlib.import_module(path.stem)
        for name, fn in vars(module).items():
            m = FRAME_FN_RE.fullmatch(name)
            if not m or getattr(fn, "__module__", None) != module.__name__:
                continue
            n = int(m.group(1))
            if n in builders:
                raise LookupError(f"frame_{n:02d} 定义了两次（第二次在 {path.name}）")
            builders[n] = fn
    return builders


def missing_targets(html: str, js: str) -> list[str]:
    """动画里选中、但画面里没有的元素。JS 里用 "#§t" + i 拼出来的选择器，只要有以它开头的 id 就算找到。"""
    out = []
    for m in dict.fromkeys((m.group(1), m.group(2), js[m.end():m.end() + 4].replace(" ", "").startswith('"+'))
                           for m in SELECTOR_RE.finditer(js)):
        kind, name, spliced = m
        if kind == "#":
            found = f'id="§{name}"' in html or (spliced and f'id="§{name}' in html)
        else:
            found = re.search(rf'class="[^"]*§{re.escape(name)}{"" if spliced else "[ " + chr(34) + "]"}', html)
        if not found:
            out.append(f"{kind}§{name}")
    return out


def out_of_bounds(kit) -> list[str]:
    """超出画面左右、或者伸进字幕区的元素。"""
    c, out = kit.c, []
    for id_, box in kit.boxes:
        if box.x < -EDGE_TOLERANCE_PX or box.r > c.w + EDGE_TOLERANCE_PX:
            out.append(f"§{id_} 横向出框（x {box.x}–{box.r}，画面宽 {c.w}）")
        if box.b > c.cap_top + EDGE_TOLERANCE_PX:
            out.append(f"§{id_} 伸进字幕区（底边 y={box.b}，字幕区从 y={c.cap_top} 开始）")
    return out


def main() -> int:
    theme_mod = importlib.import_module("theme")
    theme, kit = theme_mod.THEME, getattr(theme_mod, "K", None)
    video, frames, voices = load_video(), load_frames(), load_voices()
    plan = {item["n"]: item for item in timeline(frames, voices, video, kit_style(video))}
    builders = load_builders(TOOLS)
    missing = [f["n"] for f in frames if f["n"] not in builders]
    if missing:
        raise SystemExit(f"这些镜号还没有写 frame_NN()：{missing}")

    out_dir = ROOT / "compositions/frames"
    out_dir.mkdir(parents=True, exist_ok=True)
    for stale in out_dir.glob("*.html"):
        stale.unlink()
    problems: list[str] = []
    for f in frames:
        n, voice = f["n"], voices[f["n"]]
        if kit:
            kit.begin(n, f)
        html, js, *rest = builders[n]()
        ground_style = rest[0] if rest else (kit.ground_style() if kit else "")
        frame_css = kit.vars() if kit else ""
        page = render_frame(theme, n, len(frames), f["slug"], voice["duration_s"], html, js, voice["words"],
                            ground_style, f["text"], plan[n]["pad"], frame_css)
        path = out_dir / f"{n:02d}-{f['slug']}.html"
        path.write_text(page, encoding="utf-8")
        lost = missing_targets(html, js)
        issues = [f"动画选中了不存在的元素：{'、'.join(lost)}"] if lost else []
        issues += out_of_bounds(kit) + kit.issues if kit else []
        problems += [f"镜 {n:02d}：{msg}" for msg in issues]
        print(f"{path.relative_to(ROOT)}  {voice['duration_s']}s  {len(page) // 1024}KB")
    if problems:
        print("\n版面自检没过：", file=sys.stderr)
        for msg in problems:
            print(f"  - {msg}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
