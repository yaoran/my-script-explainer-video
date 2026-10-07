#!/usr/bin/env python3
"""打印检查画面用的时间点，直接喂给 `npx hyperframes snapshot --at`。

默认每镜取“最后一个词说完后 0.3 秒”（这时本镜的元素都已出齐）；
加 --mid 再多取每镜中点，用来看动画进行到一半时的样子。
用法：npx hyperframes snapshot --no-end --at "$(.venv/bin/python tools/snapshot_times.py)"
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SETTLE_AFTER_LAST_WORD_S = 0.3


def main() -> int:
    meta_path = ROOT / "audio_meta.json"
    if not meta_path.exists():
        raise SystemExit("缺少 audio_meta.json：先跑 tools/make_audio.py")
    want_mid = "--mid" in sys.argv[1:]
    times: list[float] = []
    base = 0.0
    for voice in json.loads(meta_path.read_text(encoding="utf-8"))["voices"]:
        last_word_end = voice["words"][-1]["end"]
        settled = min(last_word_end + SETTLE_AFTER_LAST_WORD_S, voice["duration_s"] - 0.05)
        if want_mid:
            times.append(round(base + voice["duration_s"] / 2, 2))
        times.append(round(base + settled, 2))
        base += voice["duration_s"]
    print(",".join(str(t) for t in times))
    return 0


if __name__ == "__main__":
    sys.exit(main())
