#!/usr/bin/env bash
# 新建一条解说视频的工程：目录骨架 + Python 环境 + 通用工具脚本 + 画幅和风格设定。
# 用法：bash new_project.sh <工程目录> [--aspect 16:9] [--style cobalt-grid] [--title "片名"]
#   例：bash new_project.sh videos/rule-vs-skill --aspect 9:16 --style blockframe --title "RULE × SKILL"
# 目录名用英文短横线，取自选题，不用日期或序号。画幅和风格之后可以用 tools/project.py set 改。
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "用法：bash new_project.sh <工程目录> [--aspect 16:9] [--style cobalt-grid] [--title 片名]" >&2
  exit 2
fi

TARGET="$1"; shift
ASPECT="16:9"
STYLE="cobalt-grid"
TITLE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --aspect) ASPECT="$2"; shift 2 ;;
    --style) STYLE="$2"; shift 2 ;;
    --title) TITLE="$2"; shift 2 ;;
    *) echo "未知参数：$1" >&2; exit 2 ;;
  esac
done

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd -P)"
HF_VERSION="$(cat "$SKILL_DIR/scripts/HYPERFRAMES_VERSION")"
NAME="$(basename "$TARGET")"

for bin in npx uv ffmpeg ffprobe node; do
  command -v "$bin" >/dev/null 2>&1 || { echo "缺少命令：${bin}（先跑 bash ${SKILL_DIR}/scripts/doctor.sh）" >&2; exit 1; }
done
if [ -e "$TARGET" ] && [ -n "$(/bin/ls -A "$TARGET" 2>/dev/null)" ]; then
  echo "目录已存在且非空：$TARGET" >&2
  exit 1
fi

mkdir -p "$TARGET"
cd "$TARGET"
mkdir -p tools/styles compositions/frames assets/voice assets/bgm assets/fonts renders
cp "$SKILL_DIR"/scripts/tools/*.py "$SKILL_DIR"/scripts/tools/*.sh tools/
cp "$SKILL_DIR"/scripts/tools/styles/*.py tools/styles/
cp "$SKILL_DIR"/scripts/templates/theme.py tools/theme.py
cp "$SKILL_DIR"/scripts/templates/AGENTS.md AGENTS.md
cp "$SKILL_DIR"/scripts/templates/AGENTS.md CLAUDE.md
printf '.venv/\n.tts/\n.fonts-src/\nnode_modules/\nsnapshots/\n__pycache__/\n' > .gitignore

cat > package.json <<JSON
{
  "name": "$NAME",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "npx --yes hyperframes@$HF_VERSION preview",
    "check": "npx --yes hyperframes@$HF_VERSION check",
    "render": "npx --yes hyperframes@$HF_VERSION render",
    "publish": "npx --yes hyperframes@$HF_VERSION publish"
  }
}
JSON
cat > hyperframes.json <<'JSON'
{
  "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
  "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
  "paths": { "blocks": "compositions", "components": "compositions/components", "assets": "assets" },
  "media": { "autoProxy": true }
}
JSON
printf '{\n  "id": "%s",\n  "name": "%s",\n  "createdAt": "%s"\n}\n' "$NAME" "$NAME" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > meta.json

uv venv .venv -q
uv pip install -q --python .venv/bin/python edge-tts numpy fonttools brotli

printf '{}\n' > tools/video.json
.venv/bin/python tools/project.py set "aspect=$ASPECT" "style=$STYLE" "title=${TITLE:-$NAME}" >/dev/null

echo "工程已建好：$(pwd)"
.venv/bin/python tools/project.py show
echo "下一步：写 user_script.txt 和 tools/frames.json，再配音（见技能的 references/pipeline.md）。"
