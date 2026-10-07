#!/usr/bin/env python3
"""把一组图片拼成一张联系表，方便一眼看完所有镜头。

用法：.venv/bin/python tools/contact_sheet.py <图片目录> [输出.jpg] [--cols N] [--cell 宽度]
默认输出到该目录下的 contact-sheet.jpg；横图一行 3 张，竖图一行 5 张。
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

FFMPEG = shutil.which("ffmpeg")
FFPROBE = shutil.which("ffprobe")
SHEET_NAME = "contact-sheet.jpg"


def image_size(path: Path) -> tuple[int, int]:
    out = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                          "-of", "csv=p=0:s=x", str(path)], capture_output=True, text=True, check=True).stdout.strip()
    w, h = out.split("x")
    return int(w), int(h)


def layout(w: int, h: int, count: int) -> tuple[int, int]:
    """返回 (列数, 每格宽度)。"""
    if h > w * 1.2:
        return min(count, 5), 360
    if h > w * 0.9:
        return min(count, 4), 440
    return min(count, 3), 640


def make_sheet(images: list[Path], out: Path, cols: int = 0, cell: int = 0) -> Path:
    if not FFMPEG or not FFPROBE:
        raise SystemExit("找不到 ffmpeg / ffprobe，请先安装并放进 PATH")
    if not images:
        raise SystemExit("没有可拼的图片")
    auto_cols, auto_cell = layout(*image_size(images[0]), len(images))
    cols, cell = cols or auto_cols, cell or auto_cell
    rows = -(-len(images) // cols)
    work = out.parent / ".sheet"
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    for i, image in enumerate(images):
        shutil.copy(image, work / f"{i:03d}{image.suffix}")
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-framerate", "1", "-i", str(work / f"%03d{images[0].suffix}"),
                    "-vf", f"scale={cell}:-1,tile={cols}x{rows}:padding=6:color=white", "-frames:v", "1", "-q:v", "3", str(out)],
                   check=True)
    shutil.rmtree(work, ignore_errors=True)
    return out


def snapshot_key(path: Path) -> float:
    """截图文件名形如 frame-03-at-29.65s.png，按时间排序。"""
    try:
        return float(path.stem.rsplit("-at-", 1)[1].rstrip("s"))
    except (IndexError, ValueError):
        return 0.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--cols", type=int, default=0)
    ap.add_argument("--cell", type=int, default=0)
    args = ap.parse_args()
    folder = Path(args.folder)
    images = sorted((p for p in folder.glob("*.png")), key=lambda p: (snapshot_key(p), p.name))
    out = Path(args.out) if args.out else folder / SHEET_NAME
    print(f"联系表  {make_sheet(images, out, args.cols, args.cell)}（{len(images)} 张）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
