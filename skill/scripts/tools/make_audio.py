#!/usr/bin/env python3
"""按 tools/frames.json 逐镜生成旁白（edge-tts），输出 assets/voice/NN.wav 和 audio_meta.json。

每镜的 wav 已经带上开头留白（lead）和结尾留白（tail），所以镜头时长 = wav 时长。
要拉长成片就加留白，不要放慢语速：云扬放慢后听起来不自然。
文案、声音、留白都没变的镜头直接用上次的结果，不重新合成；联网失败会自动重试。
用法：.venv/bin/python tools/make_audio.py [--voice 名字] [--rate +0%] [--draft] [--force]
  --draft  不联网，按每秒约 4.3 个字估出占位时间和静音文件，用来先排画面；正式出片前要去掉它重跑
  --force  忽略缓存，全部重新合成
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))

from project import load_frames, load_video  # noqa: E402

FFMPEG = shutil.which("ffmpeg")
FFPROBE = shutil.which("ffprobe")
DEFAULT_LEAD_S = 0.65
DEFAULT_TAIL_S = 0.95
HEAD_KEEP_S = 0.05
TAIL_KEEP_S = 0.18
TICKS_PER_S = 10_000_000
RETRY_WAITS_S = (2, 5, 10)
DRAFT_CJK_S, DRAFT_LATIN_S, DRAFT_PAUSE_S = 0.23, 0.38, 0.28
DRAFT_TOKEN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9.\-+%]*|[⺀-￿]{1,2}|[，。；：、！？,.;:!?]")
PUNCT = "，。；：、！？,.;:!?"


async def synth(text: str, voice: str, rate: str, mp3: Path) -> list[dict]:
    import edge_tts

    com = edge_tts.Communicate(text, voice, rate=rate, boundary="WordBoundary")
    words: list[dict] = []
    with mp3.open("wb") as fh:
        async for chunk in com.stream():
            if chunk["type"] == "audio":
                fh.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                start = chunk["offset"] / TICKS_PER_S
                words.append({"text": chunk["text"], "start": start, "end": start + chunk["duration"] / TICKS_PER_S})
    return words


def synth_with_retry(text: str, voice: str, rate: str, mp3: Path, label: str) -> list[dict]:
    last: Exception | None = None
    for attempt, wait in enumerate((0, *RETRY_WAITS_S)):
        if wait:
            print(f"镜 {label} 合成失败（{last}），{wait} 秒后重试第 {attempt} 次…", file=sys.stderr)
            time.sleep(wait)
        try:
            words = asyncio.run(synth(text, voice, rate, mp3))
            if words:
                return words
            last = RuntimeError("没有拿到逐词时间")
        except Exception as exc:  # noqa: BLE001 - 网络、服务端各种错误都值得重试
            last = exc
    raise SystemExit(f"镜 {label} 配音失败：{last}\n检查网络后重跑；只想先排画面可以加 --draft。")


def probe_s(path: Path) -> float:
    out = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return float(out)


def draft_words(text: str) -> list[dict]:
    """不联网时的占位切词：两个汉字一组，西文一个词一组，标点处停顿。"""
    words, t = [], 0.0
    for token in DRAFT_TOKEN_RE.findall(text):
        if token in PUNCT:
            t += DRAFT_PAUSE_S
            continue
        span = DRAFT_LATIN_S if token[0].isascii() else DRAFT_CJK_S * len(token)
        words.append({"text": token, "start": t, "end": t + span})
        t += span
    return words


def render_voice(frame: dict, voice: str, rate: str, work: Path, draft: bool) -> dict:
    nn = f"{frame['n']:02d}"
    lead = float(frame.get("lead", DEFAULT_LEAD_S))
    tail = float(frame.get("tail", DEFAULT_TAIL_S))
    wav_rel = f"assets/voice/{nn}.wav"
    if draft:
        raw = draft_words(frame["text"])
        total = lead + raw[-1]["end"] + tail
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-t", f"{total:.3f}",
                        str(ROOT / wav_rel)], check=True)
        shift = lead
    else:
        mp3 = work / f"{nn}.mp3"
        raw = synth_with_retry(frame["text"], voice, rate, mp3, nn)
        cut_from = max(0.0, raw[0]["start"] - HEAD_KEEP_S)
        cut_to = min(probe_s(mp3), raw[-1]["end"] + TAIL_KEEP_S)
        subprocess.run(
            [FFMPEG, "-y", "-loglevel", "error", "-i", str(mp3), "-af",
             f"atrim={cut_from:.3f}:{cut_to:.3f},asetpts=PTS-STARTPTS,loudnorm=I=-16:TP=-1.5:LRA=11,"
             f"adelay={round(lead * 1000)}:all=1,apad=pad_dur={tail}",
             "-ar", "48000", "-ac", "1", str(ROOT / wav_rel)],
            check=True,
        )
        shift = lead - cut_from
    return {
        "frame": frame["n"], "path": wav_rel, "duration_s": round(probe_s(ROOT / wav_rel), 3),
        "words": [{"id": f"w{nn}-{i}", "text": w["text"], "start": round(w["start"] + shift, 3),
                   "end": round(w["end"] + shift, 3)} for i, w in enumerate(raw)],
    }


def cache_key(frame: dict, voice: str, rate: str, draft: bool) -> str:
    parts = [frame["text"], voice, rate, frame.get("lead", DEFAULT_LEAD_S), frame.get("tail", DEFAULT_TAIL_S), draft]
    return hashlib.sha1(json.dumps(parts, ensure_ascii=False).encode()).hexdigest()


def cached_voice(frame: dict, key: str, work: Path) -> dict | None:
    record = work / f"{frame['n']:02d}.json"
    if not record.exists():
        return None
    saved = json.loads(record.read_text(encoding="utf-8"))
    return saved["voice"] if saved.get("key") == key and (ROOT / saved["voice"]["path"]).exists() else None


def script_mismatch(frames: list[dict]) -> str:
    """分镜文案连起来应该等于 user_script.txt（忽略空白）。不一致时返回第一处差异的说明，一致或没有该文件则返回空。"""
    path = ROOT / "user_script.txt"
    if not path.exists():
        return ""
    squash = lambda text: "".join(text.split())  # noqa: E731
    want, got = squash(path.read_text(encoding="utf-8")), squash("".join(f["text"] for f in frames))
    if want == got:
        return ""
    at = next((i for i, (a, b) in enumerate(zip(want, got)) if a != b), min(len(want), len(got)))
    return f"分镜文案和 user_script.txt 对不上，第一处不同在：原稿“…{want[max(0, at - 8):at + 12]}…”，分镜“…{got[max(0, at - 8):at + 12]}…”"


def main() -> int:
    if not FFMPEG or not FFPROBE:
        raise SystemExit("找不到 ffmpeg / ffprobe，请先安装并放进 PATH")
    video = load_video()
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", default=video["voice"])
    ap.add_argument("--rate", default=video["rate"])
    ap.add_argument("--draft", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    frames = load_frames()
    work = ROOT / ".tts"
    work.mkdir(exist_ok=True)
    (ROOT / "assets/voice").mkdir(parents=True, exist_ok=True)
    voices = []
    for frame in frames:
        key = cache_key(frame, args.voice, args.rate, args.draft)
        voice = None if args.force else cached_voice(frame, key, work)
        note = "（沿用）" if voice else ""
        if voice is None:
            voice = render_voice(frame, args.voice, args.rate, work, args.draft)
            (work / f"{frame['n']:02d}.json").write_text(json.dumps({"key": key, "voice": voice}, ensure_ascii=False), encoding="utf-8")
        voices.append(voice)
        print(f"{frame['n']:02d} {voice['duration_s']:6.2f}s  {len(voice['words']):3d} 词  {frame['title']}{note}")

    meta_path = ROOT / "audio_meta.json"
    prev = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    meta = {"bgm": prev.get("bgm"), "bgm_pending": False, "draft": args.draft, "voice": args.voice, "rate": args.rate,
            "voices": voices, "sfx": []}
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    total = sum(v["duration_s"] for v in voices)
    chars = sum(len(f["text"]) for f in frames)
    print(f"TOTAL {total:.2f}s（{int(total // 60)} 分 {total % 60:.0f} 秒）· {chars} 字 · {len(frames)} 镜 → audio_meta.json")
    mismatch = script_mismatch(frames)
    if mismatch:
        print(f"注意：{mismatch}", file=sys.stderr)
    if args.draft:
        print("这是占位时间，没有声音。正式出片前去掉 --draft 重跑。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
