#!/usr/bin/env bash
# 逐镜截图，用来检查画面。截图在 snapshots/。
# 用法（在工程根目录）：bash tools/snapshot.sh [--mid]     --mid 再多截每镜的中点，看动画进行到一半的样子
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
rm -rf snapshots
bash tools/hf.sh snapshot --no-end --at "$(.venv/bin/python tools/snapshot_times.py "$@")"
.venv/bin/python tools/contact_sheet.py snapshots
