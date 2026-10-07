#!/usr/bin/env bash
# 动手前的环境体检：需要的命令在不在、配音和字体的网络通不通、字体缓存里有什么。
# 用法：bash doctor.sh        有硬性问题（缺命令）时以非零退出；网络问题只提示。
set -uo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd -P)"
CACHE="$HOME/.cache/my-script-explainer-video/fonts"
HF_VERSION="$(cat "$SKILL_DIR/scripts/HYPERFRAMES_VERSION")"
fail=0

ok() { printf '  ✓ %s\n' "$1"; }
bad() { printf '  ✗ %s\n' "$1"; fail=1; }
warn() { printf '  ! %s\n' "$1"; }

echo "命令"
for bin in node npx uv ffmpeg ffprobe; do
  if command -v "$bin" >/dev/null 2>&1; then ok "$bin"; else bad "缺少 $bin"; fi
done
if command -v node >/dev/null 2>&1; then
  major="$(node -p 'process.versions.node.split(".")[0]')"
  [ "$major" -ge 18 ] && ok "node 版本 $major" || bad "node 版本 $major 太旧，需要 18 以上"
fi

echo "网络"
if curl -s -o /dev/null --max-time 8 https://speech.platform.bing.com; then ok "配音服务可达"; else
  warn "配音服务连不上：可以先用 --draft 排画面，出片前要联网配音"; fi
if curl -s -o /dev/null --max-time 8 -r 0-1000 "https://raw.githubusercontent.com/google/fonts/main/ofl/inter/OFL.txt" \
  || curl -s -o /dev/null --max-time 8 -r 0-1000 "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/inter/OFL.txt"; then
  ok "字体下载源可达"; else warn "字体下载源连不上：只能用缓存里已有的字体"; fi

echo "字体缓存 $CACHE"
if [ -d "$CACHE" ]; then
  count="$(find "$CACHE" -name '*.ttf' | wc -l | tr -d ' ')"
  ok "已有 $count 个字体文件，新风格第一次用时会再下载它需要的字体"
else
  warn "还没有缓存，第一次建片要下载中文字体（每个 15–25MB）"
fi

echo "渲染引擎"
ok "本技能测试过的 HyperFrames 版本是 ${HF_VERSION}，新工程会钉在这个版本"

[ "$fail" = 0 ] && echo && echo "体检通过。" || { echo; echo "有硬性问题，先解决带 ✗ 的项。"; }
exit "$fail"
