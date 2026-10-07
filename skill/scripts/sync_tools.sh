#!/usr/bin/env bash
# 把技能里最新的通用脚本同步到一个已有工程的 tools/（不动 theme.py、video.json、frames.json 和镜头脚本）。
# 用法：bash sync_tools.sh <工程目录>
set -euo pipefail
[ $# -eq 1 ] || { echo "用法：bash sync_tools.sh <工程目录>" >&2; exit 2; }
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd -P)"
TARGET="$1"
[ -d "$TARGET/tools" ] || { echo "不是工程目录（没有 tools/）：$TARGET" >&2; exit 1; }
mkdir -p "$TARGET/tools/styles"
cp "$SKILL_DIR"/scripts/tools/*.py "$SKILL_DIR"/scripts/tools/*.sh "$TARGET/tools/"
cp "$SKILL_DIR"/scripts/tools/styles/*.py "$TARGET/tools/styles/"
echo "已同步通用脚本到 $TARGET/tools"
