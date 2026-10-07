#!/usr/bin/env python3
"""程序合成背景乐（无版权问题），四种气质：calm 轻钢琴、warm 慢而暖、pulse 轻快有律动、zen 五声音阶空灵。

用哪种：tools/video.json 的 bgm.mood；留空用风格自带的；写 "none" 表示不要配乐。音量在 bgm.volume，默认 0.16。
用法：.venv/bin/python tools/make_bgm.py                     按配音总时长生成 assets/bgm/bgm.wav 并登记到 audio_meta.json
      .venv/bin/python tools/make_bgm.py <秒数> <输出.wav> [气质]   只生成文件
"""
from __future__ import annotations

import json
import sys
import wave
from dataclasses import dataclass
from pathlib import Path

import numpy as np

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))

BGM_REL = "assets/bgm/bgm.wav"
BGM_VOLUME = 0.16
BGM_EXTRA_S = 10
SR = 48000
REVERB = ((0.113, 0.35), (0.271, 0.25), (0.419, 0.18), (0.587, 0.12))


@dataclass(frozen=True)
class Mood:
    label: str
    bpm: int
    chords: tuple[tuple[int, ...], ...]  # 每小节一个和弦，MIDI 音高，第一个是根音
    arp: tuple[int, ...]  # 每半拍弹和弦里的第几个音；-1 表示这半拍不弹
    decay: float  # 音头之后衰减得多快，越大越短促
    note_amp: float
    pad_amp: float
    bass_amp: float
    kick_amp: float = 0.0


MOODS = {
    "calm": Mood("轻钢琴 lo-fi", 72, ((48, 55, 64, 71), (45, 52, 60, 67), (41, 48, 57, 64), (43, 50, 59, 64)),
                 (1, 2, 3, 2, 1, 2, 3, 2), 2.2, 0.11, 0.035, 0.30),
    "warm": Mood("慢而暖的铺底", 60, ((41, 48, 57, 64), (48, 55, 64, 67), (43, 50, 59, 62), (45, 52, 60, 64)),
                 (1, -1, 3, -1, 2, -1, 3, -1), 1.6, 0.09, 0.06, 0.26),
    "pulse": Mood("轻快拨弦", 100, ((45, 52, 60, 64), (41, 48, 57, 60), (48, 55, 64, 67), (43, 50, 59, 62)),
                  (1, 3, 2, 3, 1, 3, 2, 3), 5.5, 0.12, 0.025, 0.28, 0.16),
    "zen": Mood("五声音阶空灵", 56, ((38, 50, 57, 62), (36, 48, 55, 60), (41, 53, 57, 60), (38, 50, 55, 62)),
                (3, -1, 2, -1, 1, -1, 2, -1), 1.3, 0.13, 0.05, 0.20),
}


def hz(m: int) -> float:
    return 440.0 * 2 ** ((m - 69) / 12)


def tone(f: float, dur: float, amp: float, decay: float) -> np.ndarray:
    t = np.arange(int(SR * dur)) / SR
    env = np.exp(-t * decay) * (1 - np.exp(-t * 400))
    return amp * env * (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t) + 0.08 * np.sin(6 * np.pi * f * t))


def kick(amp: float) -> np.ndarray:
    t = np.arange(int(SR * 0.16)) / SR
    return amp * np.exp(-t * 28) * np.sin(2 * np.pi * (45 * t + 2 * (1 - np.exp(-t * 30))))  # 音高从约 105Hz 滑到 45Hz


def mix_in(buf: np.ndarray, start_s: float, sound: np.ndarray) -> None:
    s = int(start_s * SR)
    end = min(len(buf), s + len(sound))
    if s < end:
        buf[s:end] += sound[: end - s]


def bar_into(buf: np.ndarray, mood: Mood, chord: tuple[int, ...], at: float) -> None:
    beat = 60 / mood.bpm
    bar = beat * 4
    mix_in(buf, at, tone(hz(chord[0] - 12), bar, mood.bass_amp, 2.2))
    pad_t = np.arange(int(SR * bar)) / SR
    pad_env = np.minimum(1, pad_t / 0.8) * np.minimum(1, (bar - pad_t) / 0.8)
    mix_in(buf, at, sum(np.sin(2 * np.pi * hz(m) * pad_t) for m in chord[1:]) * mood.pad_amp * pad_env)
    for k, idx in enumerate(mood.arp):
        if idx >= 0:
            mix_in(buf, at + k * beat / 2, tone(hz(chord[idx] + 12), 1.6, mood.note_amp, mood.decay))
    if mood.kick_amp:
        for b in range(4):
            mix_in(buf, at + b * beat, kick(mood.kick_amp))


def synth(seconds: float, out: str, mood_name: str = "calm") -> int:
    mood = MOODS[mood_name]
    n = int(SR * seconds)
    buf = np.zeros(n + SR * 4)
    bar = 60 / mood.bpm * 4
    for i in range(int(seconds // bar) + 1):
        bar_into(buf, mood, mood.chords[i % len(mood.chords)], i * bar)
    wet = np.zeros_like(buf)
    for delay, gain in REVERB:
        d = int(delay * SR)
        wet[d:] += buf[:-d] * gain
    mix = (buf + wet)[:n]
    mix /= np.max(np.abs(mix)) + 1e-9
    pcm = (mix * 0.6 * 32767).astype(np.int16)
    with wave.open(out, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(pcm.tobytes())
    print(f"OUTPUT={out} ({seconds}s · {mood.label})")
    return 0


def auto() -> int:
    """按 audio_meta.json 里的配音总时长生成配乐，并把它登记为本片的 bgm。"""
    from project import kit_style, load_video

    meta_path = ROOT / "audio_meta.json"
    if not meta_path.exists():
        raise SystemExit("缺少 audio_meta.json：先跑 tools/make_audio.py")
    video = load_video()
    wanted = video.get("bgm") or {}
    mood = wanted.get("mood") or kit_style(video).bgm
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    if mood == "none":
        meta_path.write_text(json.dumps({**meta, "bgm": None}, ensure_ascii=False, indent=2), encoding="utf-8")
        print("本片不要配乐")
        return 0
    if mood not in MOODS:
        raise SystemExit(f"没有叫 {mood!r} 的配乐气质。可选：{'、'.join(MOODS)}、none")
    seconds = round(sum(v["duration_s"] for v in meta["voices"])) + BGM_EXTRA_S
    volume = float(wanted.get("volume", BGM_VOLUME))
    previous = meta.get("bgm") or {}
    if (previous.get("mood"), previous.get("duration_s"), previous.get("volume")) == (mood, seconds, volume) and (ROOT / BGM_REL).exists():
        print(f"配乐没变，沿用：{MOODS[mood].label}")
        return 0
    (ROOT / BGM_REL).parent.mkdir(parents=True, exist_ok=True)
    synth(float(seconds), str(ROOT / BGM_REL), mood)
    bgm = {"path": BGM_REL, "volume": volume, "mood": mood, "query": f"{MOODS[mood].label}（程序合成）", "duration_s": seconds}
    meta_path.write_text(json.dumps({**meta, "bgm": bgm}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"已登记配乐：{BGM_REL}  {MOODS[mood].label}  音量 {volume}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.exit(auto())
    if len(sys.argv) not in (3, 4):
        raise SystemExit(__doc__)
    sys.exit(synth(float(sys.argv[1]), sys.argv[2], sys.argv[3] if len(sys.argv) == 4 else "calm"))
