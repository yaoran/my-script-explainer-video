"""画幅和版面：每种比例的像素尺寸、内容区、字幕带，以及按画幅换算字号、估算文字宽度的函数。

内容区（x0..x1, y0..y1）是画面元素可以放的范围；字幕带在它下面；竖屏最底下还留了一段给平台的标题和按钮。
镜头脚本不写死像素坐标，而是从 Canvas 取内容区再切分，所以同一份脚本换一个比例也能排得下。
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import NamedTuple

CJK_START = 0x2E80
BASE_CONTENT_W = 1728  # 16:9 的内容区宽度，字号阶梯以它为基准
SIZE_MIN, SIZE_MAX = 28, 220
SHRINK_SMALL, SHRINK_BIG = -0.3, 0.72


class Box(NamedTuple):
    """一块矩形区域，单位像素。"""

    x: int
    y: int
    w: int
    h: int

    @property
    def r(self) -> int:
        return self.x + self.w

    @property
    def b(self) -> int:
        return self.y + self.h

    @property
    def cx(self) -> int:
        return self.x + self.w // 2

    @property
    def cy(self) -> int:
        return self.y + self.h // 2

    def inset(self, dx: int, dy: int | None = None) -> "Box":
        dy = dx if dy is None else dy
        return Box(self.x + dx, self.y + dy, self.w - 2 * dx, self.h - 2 * dy)

    def cols(self, n: int, gap: int) -> list["Box"]:
        w = (self.w - gap * (n - 1)) // n
        return [Box(self.x + i * (w + gap), self.y, w, self.h) for i in range(n)]

    def rows(self, n: int, gap: int) -> list["Box"]:
        h = (self.h - gap * (n - 1)) // n
        return [Box(self.x, self.y + i * (h + gap), self.w, h) for i in range(n)]

    def split_h(self, ratio: float, gap: int) -> tuple["Box", "Box"]:
        left = int((self.w - gap) * ratio)
        return Box(self.x, self.y, left, self.h), Box(self.x + left + gap, self.y, self.w - gap - left, self.h)

    def split_v(self, ratio: float, gap: int) -> tuple["Box", "Box"]:
        top = int((self.h - gap) * ratio)
        return Box(self.x, self.y, self.w, top), Box(self.x, self.y + top + gap, self.w, self.h - gap - top)


@dataclass(frozen=True)
class Canvas:
    """一种画幅的版面。head_y 是顶部版面家具的基线，top/bottom 是内容区的上下边。"""

    key: str
    w: int
    h: int
    margin: int
    head_y: int
    top: int
    bottom: int
    cap_top: int
    cap_h: int
    cap_width: float  # 字幕最宽占画面宽度的比例
    cap_size: int  # 字幕字号

    @property
    def portrait(self) -> bool:
        return self.h > self.w

    @property
    def tall(self) -> bool:
        """内容区是否偏竖：并排的东西改成上下叠。"""
        return self.content.h > self.content.w * 0.9

    @property
    def content(self) -> Box:
        return Box(self.margin, self.top, self.w - 2 * self.margin, self.bottom - self.top)

    @property
    def gap(self) -> int:
        return round(self.content.w * 0.028)

    def sz(self, px: float) -> int:
        """把 16:9 下的字号换算到本画幅：大字按比例缩，小字在窄画面上反而略放大，保证手机上看得清。"""
        ratio = self.content.w / BASE_CONTENT_W
        if abs(ratio - 1) < 0.01:
            return round(px)
        clamped = min(max(px, SIZE_MIN), SIZE_MAX)
        t = math.log(clamped / SIZE_MIN) / math.log(SIZE_MAX / SIZE_MIN)
        return round(px * ratio ** (SHRINK_SMALL + t * (SHRINK_BIG - SHRINK_SMALL)))

    def caption_zone(self) -> str:
        """传给 hyperframes check --caption-zone 的字幕带。"""
        return f"x0=0;y0={self.cap_top / self.h:.3f};x1=1;y1={(self.cap_top + self.cap_h) / self.h:.3f};severity=error"


CANVASES = {
    "16:9": Canvas("16:9", 1920, 1080, 96, 56, 172, 872, 900, 180, 0.68, 54),
    "4:3": Canvas("4:3", 1440, 1080, 80, 56, 172, 872, 900, 180, 0.84, 52),
    "1:1": Canvas("1:1", 1080, 1080, 64, 52, 174, 862, 890, 190, 0.88, 50),
    "3:4": Canvas("3:4", 1080, 1440, 64, 60, 188, 1172, 1200, 200, 0.88, 54),
    # 9:16 给抖音、视频号：顶部让开状态栏，字幕放在 70%–81% 高度，最底下 360px 留给平台的标题和按钮
    "9:16": Canvas("9:16", 1080, 1920, 72, 150, 286, 1312, 1340, 220, 0.78, 58),
}
ALIASES = {
    "横屏": "16:9", "横版": "16:9", "landscape": "16:9", "1920x1080": "16:9",
    "竖屏": "9:16", "竖版": "9:16", "portrait": "9:16", "1080x1920": "9:16",
    "方形": "1:1", "方屏": "1:1", "square": "1:1", "1080x1080": "1:1",
    "1440x1080": "4:3", "1080x1440": "3:4",
}


def get_canvas(aspect: str) -> Canvas:
    key = ALIASES.get(aspect.strip().lower(), aspect.strip())
    if key not in CANVASES:
        raise SystemExit(f"不支持的画幅 {aspect!r}。可选：{' / '.join(CANVASES)}（也可以写 横屏、竖屏、方形）")
    return CANVASES[key]


def text_w(text: str, px: float, latin: float = 0.58, tracking: float = 0.0) -> float:
    """估算一行文字的宽度（像素）。汉字按 1 个字宽，西文按 latin 个字宽，宁可估宽不估窄。"""
    em = 0.0
    for ch in text:
        if ord(ch) >= CJK_START:
            em += 1.0
        elif ch == " ":
            em += 0.3
        elif ch.isupper() or ch.isdigit():
            em += latin * 1.12
        else:
            em += latin
    return (em + tracking * len(text)) * px


def fit_px(text: str, px: int, max_w: float, latin: float = 0.58, tracking: float = 0.0) -> int:
    """一行放不下时把字号缩到刚好放下。"""
    need = text_w(text, px, latin, tracking)
    return px if need <= max_w else max(1, int(px * max_w / need))


def wrap(text: str, px: int, max_w: float, latin: float = 0.58) -> list[str]:
    """把一段话折成几行：优先在标点后断，其次在空格处断，实在不行按宽度硬断。"""
    lines, cur = [], ""
    for piece in _pieces(text):
        if cur and text_w(cur + piece, px, latin) > max_w:
            lines.append(cur.strip())
            cur = ""
        while text_w(piece, px, latin) > max_w:
            cut = max(1, int(len(piece) * max_w / text_w(piece, px, latin)))
            lines.append(piece[:cut])
            piece = piece[cut:]
        cur += piece
    if cur.strip():
        lines.append(cur.strip())
    return lines


def _pieces(text: str) -> list[str]:
    """把文字切成不可再断的小段：每个标点跟着前面的字，西文单词不拆。"""
    out, cur = [], ""
    for ch in text:
        cur += ch
        if ch in "，。；：、！？,.;:!? ":
            out.append(cur)
            cur = ""
        elif ord(ch) >= CJK_START and len(cur) >= 4:
            out.append(cur)
            cur = ""
    if cur:
        out.append(cur)
    return out
