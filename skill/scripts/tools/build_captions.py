#!/usr/bin/env python3
"""生成字幕 compositions/captions.html：按中文标点分行，逐词高亮，位置和字号跟着画幅走，样子跟着风格走。

一行放不下又没有标点可断时，按词的边界均分成几行，不会出现超宽的字幕。
用法：.venv/bin/python tools/build_captions.py
"""
from __future__ import annotations

import importlib
import itertools
import json
import math
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))

from canvas import Canvas  # noqa: E402
from framekit import GSAP_URL, CaptionStyle, Theme, font_faces, locate_words  # noqa: E402
from project import canvas_of, load_frames, load_video, load_voices  # noqa: E402

SENTENCE_END = "。？！"
BREAKS = "，：；"
SOFT_BREAK = "、"
TRAILING = "，。？！：；、 "
COLON_BONUS = 60.0
CJK_START = 0x2E80
LATIN_WIDTH = 0.55
PLATE_PADDING_PX = 90
GROUP_TAIL_S = 0.12
FALLBACK = CaptionStyle(family='"Noto Sans SC",sans-serif', weight=700, upcoming="rgba(255,255,255,0.5)", active="#FFFFFF",
                        spoken="#FFFFFF", plate="background:rgba(0,0,0,0.72);border-radius:8px;padding:12px 32px 14px;")


def width(s: str) -> float:
    return sum(1.0 if ord(c) >= CJK_START else LATIN_WIDTH for c in s)


def max_chars(c: Canvas) -> float:
    """一行字幕最多能放多少个汉字宽。"""
    return round((c.w * c.cap_width - PLATE_PADDING_PX) / c.cap_size, 1)


def sentences(text: str) -> list[tuple[int, int]]:
    spans, start = [], 0
    for i, ch in enumerate(text):
        if ch in SENTENCE_END:
            spans.append((start, i + 1))
            start = i + 1
    if start < len(text):
        spans.append((start, len(text)))
    return spans


def units(text: str, s: int, e: int, marks: str) -> list[tuple[int, int]]:
    """把一句切成若干小段，每段含它后面的那个标点。"""
    out, start = [], s
    for i in range(s, e):
        if text[i] in marks or text[i] in SENTENCE_END:
            out.append((start, i + 1))
            start = i + 1
    if start < e:
        out.append((start, e))
    return out


def best_lines(text: str, parts: list[tuple[int, int]], limit: float) -> list[tuple[int, int]] | None:
    """用最少的行数、尽量均衡地把小段拼成行；任何一行超宽则返回 None。"""
    n = len(parts)
    for k in range(1, n + 1):
        best, best_cost = None, float("inf")
        for cuts in itertools.combinations(range(1, n), k - 1):
            edges = (0, *cuts, n)
            lines = [(parts[a][0], parts[b - 1][1]) for a, b in zip(edges, edges[1:])]
            widths = [width(text[s:e].rstrip(TRAILING)) for s, e in lines]
            if max(widths) > limit:
                continue
            cost = sum(w * w for w in widths) - sum(COLON_BONUS for s, e in lines[:-1] if text[e - 1] == "：")
            if cost < best_cost:
                best, best_cost = lines, cost
        if best:
            return best
    return None


def split_by_words(text: str, s: int, e: int, starts: list[int], limit: float) -> list[tuple[int, int]]:
    """没有标点可断的长句：在词的边界上切成宽度接近的几行，行数从最少开始试，直到每行都放得下。"""
    cuts = [p for p in starts if s < p < e]
    if not cuts:
        return [(s, e)]
    total = width(text[s:e].rstrip(TRAILING))
    lines: list[tuple[int, int]] = [(s, e)]
    for k in range(max(2, math.ceil(total / limit)), len(cuts) + 2):
        lines, begin = [], s
        for i in range(1, k):
            options = [p for p in cuts if p > begin]
            if not options:
                break
            cut = min(options, key=lambda p: abs(width(text[s:p]) - total * i / k))
            lines.append((begin, cut))
            begin = cut
        lines.append((begin, e))
        if all(width(text[a:b].rstrip(TRAILING)) <= limit for a, b in lines):
            break
    return lines


def caption_lines(text: str, limit: float, starts: list[int] | None = None) -> list[tuple[int, int]]:
    lines: list[tuple[int, int]] = []
    for s, e in sentences(text):
        fit = (best_lines(text, units(text, s, e, BREAKS), limit)
               or best_lines(text, units(text, s, e, BREAKS + SOFT_BREAK), limit))
        if fit:
            lines.extend(fit)
            continue
        for a, b in units(text, s, e, BREAKS + SOFT_BREAK):
            if width(text[a:b].rstrip(TRAILING)) <= limit or not starts:
                lines.append((a, b))
            else:
                lines.extend(split_by_words(text, a, b, starts, limit))
    return lines


def build_groups(frames: list[dict], voices: dict[int, dict], limit: float) -> tuple[list[dict], float]:
    groups, base = [], 0.0
    for frame in frames:
        text, voice = frame["text"], voices[frame["n"]]
        words = locate_words(text, voice["words"])
        for s, e in caption_lines(text, limit, [w["at"] for w in words]):
            end_at = s + len(text[s:e].rstrip(TRAILING))
            inside = [w for w in words if s <= w["at"] < end_at]
            if not inside:
                continue
            gi = len(groups)
            pieces = []
            for i, w in enumerate(inside):
                piece_start = s if i == 0 else w["at"]
                piece_end = inside[i + 1]["at"] if i + 1 < len(inside) else end_at
                pieces.append({"id": f"caption-word-{gi}-{i}", "text": text[piece_start:piece_end],
                               "start": round(base + w["start"], 3), "end": round(base + w["end"], 3)})
            groups.append({"id": f"caption-group-{gi}", "frame": frame["n"], "start": pieces[0]["start"],
                           "end": round(pieces[-1]["end"] + GROUP_TAIL_S, 3), "text": text[s:end_at].strip(), "words": pieces})
        base += voice["duration_s"]
    return groups, round(base, 3)


RUNTIME = """
  (function () {
    var stage = document.getElementById("caption-stage");
    GROUPS.forEach(function (group, g) {
      var groupEl = document.createElement("div");
      groupEl.className = "caption-group";
      groupEl.id = "caption-group-" + g;
      var pill = document.createElement("div");
      pill.className = "caption-pill";
      var line = document.createElement("div");
      line.className = "caption-line";
      group.words.forEach(function (w, i) {
        var span = document.createElement("span");
        span.className = "caption-word";
        span.id = "caption-word-" + g + "-" + i;
        span.textContent = String(w.text);
        line.appendChild(span);
      });
      pill.appendChild(line);
      groupEl.appendChild(pill);
      stage.appendChild(groupEl);
    });
    var tl = gsap.timeline({ paused: true });
    GROUPS.forEach(function (group, g) {
      var groupEl = document.getElementById("caption-group-" + g);
      var next = GROUPS[g + 1];
      var start = Math.max(0, group.start);
      var end = next ? Math.min(next.start, group.end + 0.3) : Math.min(DURATION, group.end + 0.6);
      if (end <= start) end = start + 0.01;
      tl.set(groupEl, { opacity: 1 }, start);
      tl.set(groupEl, { opacity: 0 }, end);
      group.words.forEach(function (w, i) {
        var el = document.getElementById("caption-word-" + g + "-" + i);
        var at = Math.max(start, w.start);
        tl.set(el, { className: "caption-word" }, start);
        tl.set(el, { className: "caption-word is-active" }, at);
        var after = group.words[i + 1];
        tl.set(el, { className: "caption-word is-spoken" }, after ? Math.max(start, after.start) : Math.min(end, w.end + 0.1));
      });
    });
    tl.to({}, { duration: DURATION }, 0);
    window.__timelines = window.__timelines || {};
    window.__timelines["captions"] = tl;
  })();
"""


def render(theme: Theme, c: Canvas, groups: list[dict], total: float) -> str:
    cap = theme.caption or FALLBACK
    return f"""<template id="captions-template" data-composition-id="captions" data-width="{c.w}" data-height="{c.h}">
<script src="{GSAP_URL}"></script>
<style>
{font_faces(theme.fonts)}
#captions-root{{position:absolute;inset:0;pointer-events:none;}}
.caption-stage{{position:absolute;left:0;right:0;top:{c.cap_top}px;height:{c.cap_h}px;z-index:20;}}
.caption-group{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:0;}}
.caption-pill{{box-sizing:border-box;max-width:{c.cap_width * 100:.0f}%;{cap.plate}}}
.caption-line{{white-space:pre;font-family:{cap.family};font-weight:{cap.weight};font-size:{c.cap_size}px;line-height:1.25;letter-spacing:{cap.tracking};font-synthesis:none;}}
.caption-word{{display:inline-block;white-space:pre;color:{cap.upcoming};}}
.caption-word.is-active{{color:{cap.active};{cap.active_css}}}
.caption-word.is-spoken{{color:{cap.spoken};}}
</style>
<div id="captions-root" data-composition-id="captions" data-timeline-locked data-start="0" data-duration="{total}" data-fps="30" data-width="{c.w}" data-height="{c.h}">
  <div id="caption-stage" class="caption-stage" aria-hidden="true"></div>
</div>
<script>
  var GROUPS = {json.dumps(groups, ensure_ascii=False)};
  var DURATION = {total};
{RUNTIME}</script>
</template>
"""


def main() -> int:
    video, frames, voices = load_video(), load_frames(), load_voices()
    c = canvas_of(video)
    theme = importlib.import_module("theme").THEME
    limit = max_chars(c)
    groups, total = build_groups(frames, voices, limit)
    out = ROOT / "compositions/captions.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(theme, c, groups, total), encoding="utf-8")
    (ROOT / "caption_groups.json").write_text(
        json.dumps({"total_duration_s": total, "width": c.w, "height": c.h, "groups": groups}, ensure_ascii=False, indent=2), encoding="utf-8")
    shim = ROOT / "caption-overrides.json"
    if not shim.exists():
        shim.write_text("[]\n", encoding="utf-8")
    widest = max(groups, key=lambda g: width(g["text"]))
    print(f"{len(groups)} 行字幕 · 一行最多 {limit} 字宽 · 最宽的一行 {width(widest['text']):.1f} 字：{widest['text']}")
    too_wide = [g for g in groups if width(g["text"]) > limit + 0.5]
    for g in too_wide:
        print(f"注意：镜 {g['frame']:02d} 这一行字幕超宽，请在文案里加逗号或拆句：{g['text']}", file=sys.stderr)
    return 1 if too_wide else 0


if __name__ == "__main__":
    sys.exit(main())
