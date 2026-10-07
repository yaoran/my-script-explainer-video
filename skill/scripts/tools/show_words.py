#!/usr/bin/env python3
"""列出每镜旁白的逐词时间，想知道某个字具体在第几秒说到时看这个。

@[词] 按文案原文写就行，不必和这里的切词一致；这里只是给你看时间，方便判断两个元素隔多久出现。
用法：.venv/bin/python tools/show_words.py [镜号]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    meta_path = ROOT / "audio_meta.json"
    if not meta_path.exists():
        raise SystemExit("缺少 audio_meta.json：先跑 tools/make_audio.py")
    only = int(sys.argv[1]) if len(sys.argv) > 1 else None
    for voice in json.loads(meta_path.read_text(encoding="utf-8"))["voices"]:
        if only is not None and voice["frame"] != only:
            continue
        print(f"\n镜 {voice['frame']:02d}  时长 {voice['duration_s']}s")
        for w in voice["words"]:
            print(f"  {w['start']:6.2f} – {w['end']:5.2f}  {w['text']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
