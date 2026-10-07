#!/usr/bin/env bash
# 用工程里钉死的 HyperFrames 版本执行命令，避免上游更新后同一个工程表现不一样。
# 用法（在工程根目录）：bash tools/hf.sh <check|snapshot|render|preview> [参数…]
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
VERSION="$(node -e 'const s=require("./package.json").scripts.check; const m=s.match(/hyperframes@([0-9.]+)/); process.stdout.write(m?m[1]:"")')"
if [ -z "$VERSION" ]; then
  echo "package.json 里没有钉 HyperFrames 版本" >&2
  exit 1
fi
exec npx --yes "hyperframes@$VERSION" "$@"
