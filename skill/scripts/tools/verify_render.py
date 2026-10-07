#!/usr/bin/env python3
"""出片后的验收：画幅、时长、响度、意外静音，并按每镜结尾抽一帧拼成联系表。

用法：.venv/bin/python tools/verify_render.py [renders/video.mp4]
联系表输出到成片同目录的 contact-sheet.jpg，打开这张图逐镜看画面和字幕。
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))

from contact_sheet import make_sheet  # noqa: E402
from project import canvas_of, load_video  # noqa: E402

FFMPEG = shutil.which("ffmpeg")
FFPROBE = shutil.which("ffprobe")
SILENCE_DB = -45
SILENCE_MIN_S = 2.0
TARGET_LUFS = -16.0
LUFS_TOLERANCE = 2.0
DURATION_TOLERANCE_S = 0.5
POSTER_BEFORE_LAST_WORD_END_S = 0.1


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True, check=False)


def probe(video: Path) -> dict:
    out = run([FFPROBE, "-v", "error", "-show_entries",
               "stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate:format=duration,size",
               "-of", "json", str(video)]).stdout
    return json.loads(out)


def loudness(video: Path) -> float | None:
    err = run([FFMPEG, "-hide_banner", "-nostats", "-i", str(video), "-af", "ebur128", "-f", "null", "-"]).stderr
    hits = re.findall(r"I:\s+(-?\d+(?:\.\d+)?) LUFS", err)
    return float(hits[-1]) if hits else None


def silences(video: Path) -> list[tuple[float, float]]:
    err = run([FFMPEG, "-hide_banner", "-nostats", "-i", str(video), "-af",
               f"silencedetect=noise={SILENCE_DB}dB:d={SILENCE_MIN_S}", "-f", "null", "-"]).stderr
    starts = [float(x) for x in re.findall(r"silence_start: (-?\d+(?:\.\d+)?)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: (-?\d+(?:\.\d+)?)", err)]
    return list(zip(starts, ends))


def load_meta() -> dict:
    path = ROOT / "audio_meta.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def poster_times(meta: dict, total: float) -> list[float]:
    """每镜最后一个词刚说完的时刻（元素出齐、字幕还在）；没有配音信息时均匀取 9 个。"""
    if not meta.get("voices"):
        return [round(total * (i + 0.5) / 9, 2) for i in range(9)]
    times, base = [], 0.0
    for voice in meta["voices"]:
        last_word_end = base + voice["words"][-1]["end"]
        times.append(round(min(last_word_end, total) - POSTER_BEFORE_LAST_WORD_END_S, 2))
        base += voice["duration_s"]
    return times


def contact_sheet(video: Path, times: list[float]) -> Path:
    work = video.parent / ".posters"
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir()
    for i, t in enumerate(times):
        run([FFMPEG, "-y", "-loglevel", "error", "-ss", str(t), "-i", str(video), "-frames:v", "1", str(work / f"{i:03d}.png")])
    sheet = make_sheet(sorted(work.glob("*.png")), video.parent / "contact-sheet.jpg")
    shutil.rmtree(work, ignore_errors=True)
    return sheet


def check_picture(stream: dict | None, problems: list[str]) -> None:
    if not stream:
        problems.append("没有视频流")
        return
    print(f"画面  {stream['width']}x{stream['height']}  {stream['r_frame_rate']} fps  {stream['codec_name']}")
    c = canvas_of(load_video())
    if (stream["width"], stream["height"]) != (c.w, c.h):
        problems.append(f"画幅是 {stream['width']}x{stream['height']}，video.json 里选的 {c.key} 应该是 {c.w}x{c.h}")


def check_sound(video: Path, has_audio: bool, total: float, meta: dict, problems: list[str]) -> None:
    if meta.get("draft"):
        problems.append("配音还是占位的（--draft），没有声音。去掉 --draft 重跑配音再出片")
        return
    if not has_audio:
        problems.append("没有音轨")
        return
    lufs = loudness(video)
    if lufs is not None:
        print(f"响度  {lufs:.1f} LUFS（目标 {TARGET_LUFS:.0f}）")
        if abs(lufs - TARGET_LUFS) > LUFS_TOLERANCE:
            problems.append(f"整体响度 {lufs:.1f} LUFS，偏离目标超过 {LUFS_TOLERANCE:.0f}")
    for s, e in silences(video):
        if e < total - 0.5:
            problems.append(f"{s:.1f}–{e:.1f} 秒有 {e - s:.1f} 秒静音")


def main() -> int:
    if not FFMPEG or not FFPROBE:
        raise SystemExit("找不到 ffmpeg / ffprobe，请先安装并放进 PATH")
    video = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "renders/video.mp4"
    if not video.exists():
        raise SystemExit(f"找不到成片：{video}")
    info, meta = probe(video), load_meta()
    total = float(info["format"]["duration"])
    streams = {s["codec_type"]: s for s in info["streams"]}
    problems: list[str] = []

    check_picture(streams.get("video"), problems)
    if "audio" in streams:
        print(f"声音  {streams['audio']['codec_name']}  {streams['audio']['sample_rate']} Hz")
    print(f"时长  {int(total // 60)} 分 {total % 60:.1f} 秒   大小 {int(info['format']['size']) / 1e6:.1f} MB")
    expected = sum(v["duration_s"] for v in meta.get("voices", []))
    if expected and abs(total - expected) > DURATION_TOLERANCE_S:
        problems.append(f"成片 {total:.1f} 秒，配音总长 {expected:.1f} 秒，对不上：改过文案或配音后要先 rebuild 再出片")
    check_sound(video, "audio" in streams, total, meta, problems)

    print(f"联系表  {contact_sheet(video, poster_times(meta, total))}")
    if problems:
        print("\n需要处理：")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("\n画幅、时长、响度、静音四项通过。画面和字幕请打开联系表逐镜看。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
