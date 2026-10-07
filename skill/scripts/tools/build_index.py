#!/usr/bin/env python3
"""生成主时间线 index.html：把每镜的画面、配音、配乐、字幕按时间排好，并写入镜头之间的转场。

转场在 tools/video.json 的 transitions 里按“章节镜 / 普通镜 / 末镜”各定一种，留空用风格自带的；
某一镜想单独指定，在 frames.json 那一镜里加 "transition"。可选：cut、crossfade、blur-crossfade、
push-slide <LEFT|RIGHT|UP|DOWN>、zoom-through、squeeze。
用法：.venv/bin/python tools/build_index.py
"""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))

from project import canvas_of, kit_style, load_frames, load_video, load_voices, timeline  # noqa: E402

GSAP = ('<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js" '
        'integrity="sha384-sG0Hv1tP1lZCk9KQmrIbY/XNwi+OY84GQqhMscbnsoBFqAz8KNCil1kvfL3Hbbk2" crossorigin="anonymous"></script>')
VOICE_TRACKS, BGM_TRACK, CAPTION_TRACK = (10, 12), 11, 2  # 相邻两镜的配音放在不同轨道，首尾相接也不算重叠


def transition_js(old: str, new: str, item: dict, w: int, h: int) -> list[str]:
    """一处转场的两条补间：old 是退出的那一镜，new 是进来的那一镜。"""
    t, d, kind = item["start"], item["seconds"], item["kind"]
    a, b = f'"#el-{old}"', f'"#el-{new}"'
    if kind == "crossfade":
        return [f'tl.to({a}, {{ opacity: 0, duration: {d}, ease: "power2.inOut" }}, {t});',
                f'tl.fromTo({b}, {{ opacity: 0 }}, {{ opacity: 1, duration: {d}, ease: "power2.inOut" }}, {t});']
    if kind == "blur-crossfade":
        return [f'tl.to({a}, {{ filter: "blur(10px)", scale: 1.03, opacity: 0, duration: {d}, ease: "power2.inOut" }}, {t});',
                f'tl.fromTo({b}, {{ filter: "blur(10px)", scale: 0.97, opacity: 0 }}, '
                f'{{ filter: "blur(0px)", scale: 1, opacity: 1, duration: {d}, ease: "power2.inOut" }}, {t});']
    if kind == "zoom-through":
        return [f'tl.to({a}, {{ scale: 2.5, opacity: 0, filter: "blur(8px)", duration: {d}, ease: "power3.in" }}, {t});',
                f'tl.fromTo({b}, {{ scale: 0.5, opacity: 0, filter: "blur(8px)" }}, '
                f'{{ scale: 1, opacity: 1, filter: "blur(0px)", duration: {d}, ease: "power3.out" }}, {t});']
    if kind == "squeeze":
        return [f'tl.to({a}, {{ scaleX: 0, transformOrigin: "left center", duration: {d}, ease: "power3.inOut" }}, {t});',
                f'tl.fromTo({b}, {{ scaleX: 0, transformOrigin: "right center", opacity: 1 }}, '
                f'{{ scaleX: 1, transformOrigin: "right center", opacity: 1, duration: {d}, ease: "power3.inOut" }}, {t});']
    axis, travel = ("y", h) if item["direction"] in ("UP", "DOWN") else ("x", w)
    sign = -1 if item["direction"] in ("LEFT", "UP") else 1
    return [f'tl.to({a}, {{ {axis}: {sign * travel}, duration: {d}, ease: "power3.inOut" }}, {t});',
            f'tl.fromTo({b}, {{ {axis}: {-sign * travel}, opacity: 1 }}, {{ {axis}: 0, opacity: 1, duration: {d}, ease: "power3.inOut" }}, {t});']


def clip(id_: str, src: str, start: float, duration: float, track: int, extra: str = "") -> str:
    return (f'      <div id="el-{id_}" class="scene" data-composition-id="{id_}" data-composition-src="{src}" '
            f'data-start="{start}" data-duration="{duration}" data-track-index="{track}"{extra}></div>')


def audio(id_: str, src: str, start: float, duration: float, track: int, volume: float) -> str:
    return (f'      <audio id="el-{id_}" src="{src}" data-start="{start}" data-duration="{duration}" '
            f'data-track-index="{track}" data-volume="{volume}"></audio>')


def build(root: Path = ROOT) -> str:
    video, frames, voices = load_video(root), load_frames(root), load_voices(root)
    c = canvas_of(video)
    theme = importlib.import_module("theme").THEME
    plan = timeline(frames, voices, video, kit_style(video))
    total = round(plan[-1]["start"] + plan[-1]["duration"], 3)
    body, tweens = [], []
    for i, item in enumerate(plan):
        body.append(clip(item["id"], f"compositions/frames/{item['id']}.html", item["start"],
                         round(item["duration"] + item["pad"], 3), item["track"]))
        body.append(audio(f"{item['id']}-voice", voices[item["n"]]["path"], item["start"], item["duration"], VOICE_TRACKS[i % 2], 1))
        if i and item["kind"] != "cut":
            tweens += transition_js(plan[i - 1]["id"], item["id"], item, c.w, c.h)
    meta = json.loads((root / "audio_meta.json").read_text(encoding="utf-8"))
    bgm = meta.get("bgm")
    if bgm and (root / bgm["path"]).exists():
        body.append(audio("bgm", bgm["path"], 0, total, BGM_TRACK, bgm.get("volume", 0.16)))
    if (root / "compositions/captions.html").exists():
        body.append(clip("captions", "compositions/captions.html", 0, total, CAPTION_TRACK, ' data-track-kind="captions"'))
    tween_block = "\n        ".join(tweens)
    return f"""<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={c.w}, height={c.h}" />
    {GSAP}
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {c.w}px; height: {c.h}px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: {c.w}px; height: {c.h}px; overflow: hidden; background: {theme.bg}; }}
      .scene {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="{c.w}" data-height="{c.h}">
{chr(10).join(body)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      (function () {{
        var tl = gsap.timeline({{ paused: true }});
        {tween_block}
        tl.to({{}}, {{ duration: {total} }}, 0);
        window.__timelines["main"] = tl;
      }})();
    </script>
  </body>
</html>
"""


def main() -> int:
    html = build()
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    video, frames, voices = load_video(), load_frames(), load_voices()
    plan = timeline(frames, voices, video, kit_style(video))
    used = sorted({p["kind"] for p in plan[1:]})
    print(f"index.html  {canvas_of(video).w}×{canvas_of(video).h}  {plan[-1]['start'] + plan[-1]['duration']:.2f}s  "
          f"{len(plan)} 镜  转场：{'、'.join(used) or '无'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
