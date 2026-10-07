#!/usr/bin/env bash
# 把工程从“镜头脚本 + 配音”重建到可渲染状态：画面 → 字体 → 字幕 → 主时间线 → 检查。
# 用法（在工程根目录）：bash tools/rebuild.sh [--audio] [--draft] [--no-check]
#   --audio      先重新生成配音（文案、声音或留白变了才需要；没变的镜头会沿用缓存）
#   --draft      和 --audio 一起用：不联网，用占位时间先排画面
#   --no-check   跳过最后的浏览器检查（只想快速看一眼版面自检结果时用）
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY=".venv/bin/python"
REMAKE_AUDIO=0
DRAFT=""
RUN_CHECK=1

while [ $# -gt 0 ]; do
  case "$1" in
    --audio) REMAKE_AUDIO=1; shift ;;
    --draft) DRAFT="--draft"; shift ;;
    --no-check) RUN_CHECK=0; shift ;;
    *) echo "未知参数：$1" >&2; exit 2 ;;
  esac
done

step() { printf '\n== %s\n' "$1"; }

if [ "$REMAKE_AUDIO" = 1 ]; then
  step "配音"
  "$PY" tools/make_audio.py $DRAFT
  "$PY" tools/make_bgm.py
fi

step "画面"
"$PY" tools/build_frames.py
step "字幕"
"$PY" tools/build_captions.py
step "字体"
"$PY" tools/build_fonts.py
step "主时间线"
"$PY" tools/build_index.py

if [ "$RUN_CHECK" = 1 ]; then
  step "检查"
  ZONE="$("$PY" -c 'import sys; sys.path.insert(0, "tools"); from project import canvas_of, load_video; print(canvas_of(load_video()).caption_zone())')"
  bash tools/hf.sh check --caption-zone "$ZONE" --frame-check "severity=error"
fi
