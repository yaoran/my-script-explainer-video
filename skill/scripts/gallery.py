#!/usr/bin/env python3
"""风格样张：用同一份示例镜头，把每种风格在每种画幅下的样子截出来。

新增或改了风格之后跑它来验收；也可以给用户看，帮他挑风格。不联网配音，用占位时间。
用法：python3 gallery.py --out <输出目录> [--styles a,b] [--aspects 16:9,9:16] [--work <临时工程目录>] [--check] [--overview]
输出：<输出目录>/sheets/<风格>-<画幅>.jpg（15 镜联系表）和 <输出目录>/strips/<画幅>-<风格>.jpg（6 镜横条）。
加 --overview 时，把输出目录里已有的横条拼成带风格名的总览图 overview-<画幅>-N.jpg。
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.dont_write_bytecode = True  # 不在技能目录里留下 __pycache__
sys.path.insert(0, str(SCRIPTS / "tools"))

from contact_sheet import make_sheet, snapshot_key  # noqa: E402
from styles import STYLES  # noqa: E402

STRIP_FRAMES = (0, 1, 3, 4, 6, 13)  # 标题、定义、柱状图、对照、卡片、章节镜
STRIP_CELL = {"16:9": 320, "9:16": 216, "1:1": 240, "4:3": 280, "3:4": 216}
OVERVIEW_ROWS = {"16:9": 7, "9:16": 4, "1:1": 5, "4:3": 6, "3:4": 4}
LABEL_H, LABEL_SIZE = 56, 28
LABEL_FONT = Path.home() / ".cache/my-script-explainer-video/fonts/NotoSansSC[wght].ttf"


def run(cmd: list[str], cwd: Path) -> str:
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    if result.returncode:
        keep = [line for line in result.stdout.splitlines() if "content_overlap" not in line and "Fix: Give each" not in line]
        raise SystemExit(f"命令失败：{' '.join(cmd)}\n" + "\n".join(keep[-60:]) + f"\n{result.stderr[-1500:]}")
    return result.stdout


def prepare(work: Path) -> None:
    if not (work / "tools").exists():
        run(["bash", str(SCRIPTS / "new_project.sh"), str(work), "--title", "样张"], SCRIPTS)
    run(["bash", str(SCRIPTS / "sync_tools.sh"), str(work)], SCRIPTS)
    for old in (work / "tools").glob("frames_*.py"):
        old.unlink()
    shutil.copy(SCRIPTS / "gallery/frames.json", work / "tools/frames.json")
    shutil.copy(SCRIPTS / "gallery/frames_demo.py", work / "tools/frames_demo.py")


def shoot(work: Path, out: Path, style: str, aspect: str, check: bool) -> None:
    py = str(work / ".venv/bin/python")
    label = STYLES[style].label
    run([py, "tools/project.py", "set", f"style={style}", f"aspect={aspect}", f"title={label} · {style}"], work)
    log = run(["bash", "tools/rebuild.sh", "--audio", "--draft"] + ([] if check else ["--no-check"]), work)
    faint = [line.strip() for line in log.splitlines() if line.strip().startswith("✗")]
    run(["bash", "tools/snapshot.sh"], work)
    tag = aspect.replace(":", "x")
    shots = sorted((work / "snapshots").glob("frame-*.png"), key=snapshot_key)
    (out / "sheets").mkdir(exist_ok=True)
    (out / "strips").mkdir(exist_ok=True)
    shutil.copy(work / "snapshots/contact-sheet.jpg", out / f"sheets/{style}-{tag}.jpg")
    picked = [shots[i] for i in STRIP_FRAMES if i < len(shots)]
    make_sheet(picked, out / f"strips/{tag}-{style}.jpg", cols=len(picked), cell=STRIP_CELL[aspect])
    print(f"{style:18s} {aspect}  完成" + (f"  对比度提示 {len(faint)} 条：{' | '.join(faint[:4])}" if faint else ""), flush=True)


def overview(out: Path, aspect: str) -> None:
    """把一种画幅下所有风格的横条摞起来，每条上面写风格名和一句观感。"""
    tag = aspect.replace(":", "x")
    work = out / ".overview"
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir()
    labeled = []
    for name, style in STYLES.items():
        strip = out / f"strips/{tag}-{name}.jpg"
        if not strip.exists():
            continue
        note = work / f"{name}.txt"
        note.write_text(f"{name}  {style.label}  ·  {style.mood}", encoding="utf-8")
        target = work / f"{len(labeled):03d}.png"
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(strip), "-vf",
             f"pad=iw:ih+{LABEL_H}:0:{LABEL_H}:white,drawtext=fontfile='{LABEL_FONT}':textfile='{note}':x=14:y=12:"
             f"fontsize={LABEL_SIZE}:fontcolor=black", str(target)], out)
        labeled.append(target)
    per = OVERVIEW_ROWS[aspect]
    for old in out.glob(f"overview-{tag}-*.jpg"):
        old.unlink()
    for i in range(0, len(labeled), per):
        group = labeled[i:i + per]
        inputs = [arg for path in group for arg in ("-i", str(path))]
        stack = f"vstack=inputs={len(group)}" if len(group) > 1 else "null"
        run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", stack, "-q:v", "4",
             str(out / f"overview-{tag}-{i // per + 1}.jpg")], out)
    shutil.rmtree(work, ignore_errors=True)
    print(f"总览 {aspect}：{-(-len(labeled) // per)} 张")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--styles", default=",".join(STYLES))
    ap.add_argument("--aspects", default="16:9,9:16")
    ap.add_argument("--work", default="")
    ap.add_argument("--check", action="store_true", help="每个组合都跑一遍浏览器检查（慢）")
    ap.add_argument("--overview", action="store_true", help="拍完后拼带风格名的总览图")
    ap.add_argument("--overview-only", action="store_true", help="不拍，只用已有的横条拼总览图")
    args = ap.parse_args()
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    aspects = args.aspects.split(",")
    if not args.overview_only:
        work = Path(args.work).resolve() if args.work else Path(tempfile.mkdtemp(prefix="style-gallery-")) / "project"
        prepare(work)
        for style in args.styles.split(","):
            if style not in STYLES:
                raise SystemExit(f"没有叫 {style!r} 的风格")
            for aspect in aspects:
                shoot(work, out, style, aspect, args.check)
    if args.overview or args.overview_only:
        for aspect in aspects:
            overview(out, aspect)
    print(f"样张在 {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
