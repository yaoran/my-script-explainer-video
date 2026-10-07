#!/usr/bin/env python3
"""工程的公共读取：tools/video.json（片名、画幅、风格、声音、转场）、tools/frames.json（逐镜文案）、audio_meta.json（配音时间）。

也是一个小命令：
    .venv/bin/python tools/project.py styles          列出风格库
    .venv/bin/python tools/project.py aspects         列出可选画幅
    .venv/bin/python tools/project.py set style=neon-night aspect=9:16     改 video.json
    .venv/bin/python tools/project.py show            看当前设定和每镜时长
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))

from canvas import CANVASES, Canvas, get_canvas  # noqa: E402
from stylekit import Kit, Style  # noqa: E402
from styles import STYLES, get_style  # noqa: E402

VIDEO_PATH = ROOT / "tools/video.json"
FRAMES_PATH = ROOT / "tools/frames.json"
META_PATH = ROOT / "audio_meta.json"
DEFAULTS = {"title": "", "aspect": "16:9", "style": "cobalt-grid", "voice": "zh-CN-YunyangNeural", "rate": "+0%",
            "transitions": {}, "bgm": {}}
TRANSITION_S = {"crossfade": 0.5, "blur-crossfade": 0.6, "push-slide": 0.5, "zoom-through": 0.4, "squeeze": 0.4}
SETTABLE = ("title", "aspect", "style", "voice", "rate")


def load_video(root: Path = ROOT) -> dict:
    path = root / "tools/video.json"
    if not path.exists():
        raise SystemExit(f"缺少 {path}：先写片名、画幅和风格（见技能的 references/pipeline.md）")
    video = {**DEFAULTS, **json.loads(path.read_text(encoding="utf-8"))}
    get_canvas(video["aspect"])
    get_style(video["style"])
    return video


def load_frames(root: Path = ROOT) -> list[dict]:
    path = root / "tools/frames.json"
    if not path.exists():
        raise SystemExit(f"缺少 {path}：先把文稿切成逐镜的 frames.json（见技能的 references/pipeline.md）")
    frames = json.loads(path.read_text(encoding="utf-8"))
    numbers = [f["n"] for f in frames]
    if numbers != list(range(1, len(frames) + 1)):
        raise SystemExit(f"frames.json 的镜号必须从 1 连续编到 {len(frames)}，现在是 {numbers}")
    for f in frames:
        missing = [k for k in ("slug", "title", "text") if not f.get(k)]
        if missing:
            raise SystemExit(f"frames.json 第 {f['n']} 镜缺少字段：{missing}")
    return frames


def load_voices(root: Path = ROOT) -> dict[int, dict]:
    path = root / "audio_meta.json"
    if not path.exists():
        raise SystemExit("缺少 audio_meta.json：先跑 tools/make_audio.py（没有网络时加 --draft 先出占位时间）")
    return {v["frame"]: v for v in json.loads(path.read_text(encoding="utf-8"))["voices"]}


def make_kit(root: Path = ROOT) -> Kit:
    video = load_video(root)
    return Kit(get_style(video["style"]), get_canvas(video["aspect"]), video["title"])


def transition_for(index: int, frame: dict, total: int, video: dict, style: Style | None) -> str:
    """第 index 镜（从 0 数）进场用什么转场。frames.json 里写了就用它的，否则章节镜、普通镜、末镜各用一种。"""
    if index == 0:
        return "cut"
    if frame.get("transition"):
        return frame["transition"]
    chapter, inner, last = style.transitions if style else ("push-slide LEFT", "crossfade", "blur-crossfade")
    custom = video.get("transitions") or {}
    if index == total - 1:
        return custom.get("last") or last
    return (custom.get("chapter") or chapter) if frame.get("chapter") else (custom.get("inner") or inner)


def parse_transition(spec: str) -> tuple[str, str, float]:
    """"push-slide LEFT 0.4" → (类型, 方向, 秒数)；cut 的秒数是 0。"""
    parts = spec.split()
    kind = parts[0].lower() if parts else "cut"
    if kind in ("cut", "none"):
        return "cut", "", 0.0
    if kind not in TRANSITION_S:
        raise SystemExit(f"不认识的转场 {spec!r}。可选：cut、{'、'.join(TRANSITION_S)}")
    direction, seconds = "LEFT", TRANSITION_S[kind]
    for p in parts[1:]:
        try:
            seconds = float(p.rstrip("s"))
        except ValueError:
            direction = p.upper()
    return kind, direction, seconds


def timeline(frames: list[dict], voices: dict[int, dict], video: dict, style: Style | None) -> list[dict]:
    """每镜在成片里的起点、时长、进场转场，以及为了让下一镜转进来而多停的尾巴 pad。"""
    missing = [f["n"] for f in frames if f["n"] not in voices]
    if missing:
        raise SystemExit(f"这些镜号还没有配音：{missing}。先跑 tools/make_audio.py")
    plan, start = [], 0.0
    for i, f in enumerate(frames):
        kind, direction, seconds = parse_transition(transition_for(i, f, len(frames), video, style))
        duration = voices[f["n"]]["duration_s"]
        seconds = min(seconds, round(duration * 0.4, 2))
        if plan and kind != "cut":
            plan[-1]["pad"] = seconds
        plan.append({"n": f["n"], "id": f"{f['n']:02d}-{f['slug']}", "start": round(start, 3), "duration": duration,
                     "pad": 0.0, "kind": kind, "direction": direction, "seconds": seconds, "track": i % 2})
        start += duration
    return plan


def kit_style(video: dict) -> Style:
    return get_style(video["style"])


def canvas_of(video: dict) -> Canvas:
    return get_canvas(video["aspect"])


def cmd_styles() -> int:
    for s in STYLES.values():
        origin = "预设" if s.origin == "preset" else "自制"
        print(f"{s.name:18s} {s.label}（{origin}）\n{'':18s} 观感：{s.mood}\n{'':18s} 适合：{s.fit}")
    print(f"\n共 {len(STYLES)} 种。每种在横屏和竖屏下的样子见技能的 assets/gallery/。")
    return 0


def cmd_aspects() -> int:
    notes = {"16:9": "横屏：B 站、视频号横版、电脑和电视", "9:16": "竖屏：抖音、视频号、快手、小红书全屏",
             "3:4": "竖版：小红书、视频号信息流", "1:1": "方形：朋友圈、信息流", "4:3": "横版：课件、老屏幕"}
    for key, c in CANVASES.items():
        print(f"{key:5s} {c.w}×{c.h}  {notes[key]}")
    return 0


def cmd_set(pairs: list[str]) -> int:
    video = json.loads(VIDEO_PATH.read_text(encoding="utf-8")) if VIDEO_PATH.exists() else {}
    for pair in pairs:
        key, _, value = pair.partition("=")
        if key not in SETTABLE or not value:
            raise SystemExit(f"用法：project.py set 键=值 …  可改的键：{'、'.join(SETTABLE)}")
        video = {**video, key: get_canvas(value).key if key == "aspect" else value}
    VIDEO_PATH.write_text(json.dumps(video, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    load_video()
    print(f"已更新 {VIDEO_PATH.relative_to(ROOT)}：{' '.join(pairs)}。改了风格或画幅后跑 bash tools/rebuild.sh。")
    return 0


def cmd_show() -> int:
    video = load_video()
    style, c = kit_style(video), canvas_of(video)
    print(f"片名 {video['title']}\n画幅 {c.key}（{c.w}×{c.h}）\n风格 {style.name} {style.label}\n声音 {video['voice']} {video['rate']}")
    if FRAMES_PATH.exists() and META_PATH.exists():
        frames = load_frames()
        plan = timeline(frames, load_voices(), video, style)
        for item, f in zip(plan, frames):
            print(f"  {item['n']:02d} {item['start']:7.2f}s  {item['duration']:6.2f}s  {item['kind']:14s} {f['title']}")
        print(f"总长 {plan[-1]['start'] + plan[-1]['duration']:.1f}s，{len(frames)} 镜")
    return 0


def main(argv: list[str]) -> int:
    commands = {"styles": cmd_styles, "aspects": cmd_aspects, "show": cmd_show}
    if argv and argv[0] in commands:
        return commands[argv[0]]()
    if argv and argv[0] == "set":
        return cmd_set(argv[1:])
    raise SystemExit(__doc__)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
