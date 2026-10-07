"""纵向排版：把几行字、标签、强调词从上到下排进一块区域，自动算每一项的 y，不用手写坐标。

用法：
    f = Flow(K, K.c.content, align="left", valign="center")
    f.tag("k", "第一章"); f.txt("h", "xl", "会说话"); f.space(24); f.em("kw", "lg", "ChatGPT")
    html = f.render()
"""
from __future__ import annotations

from collections.abc import Callable

from canvas import Box, wrap
from fontlib import latin_width
from stylekit import Kit

Render = Callable[[int], str]
OVERFLOW_TOLERANCE_PX = 12


class Flow:
    def __init__(self, kit: Kit, box: Box, align: str = "left", valign: str = "center", gap: int | None = None,
                 chip: str = "") -> None:
        """chip 是给这块区域里的小标签附加的样式，放在有底色的卡片里时用它保证标签看得清。"""
        self.k, self.box, self.align, self.valign, self.chip = kit, box, align, valign, chip
        self.gap = kit.c.gap if gap is None else gap
        self.items: list[tuple[int, int, Render]] = []  # (前面的间距, 高度, 画在 y 处)
        self._pending = 0
        self._first = ""

    def add(self, height: int, render: Render, gap: int | None = None) -> "Flow":
        """加一项自定义内容：height 是它占的高度，render(y) 返回它的 HTML。"""
        before = 0 if not self.items else (self.gap if gap is None else gap)
        self.items.append((before + self._pending, height, render))
        self._pending = 0
        return self

    def space(self, px: int) -> "Flow":
        self._pending += px
        return self

    def _x(self, w: int) -> int:
        if self.align == "center":
            return self.box.x + (self.box.w - w) // 2
        return self.box.r - w if self.align == "right" else self.box.x

    def txt(self, id_: str, size: str | int, text: str, tone: str = "ink", role: str | None = None,
            gap: int | None = None, cls: str = "") -> "Flow":
        k, b = self.k, self.box
        self._first = self._first or id_
        return self.add(k.line_h(size, role), lambda y: k.txt(id_, size, text, b.x, y, b.w, self.align, tone, role, cls=cls), gap)

    def para(self, id_: str, size: str | int, text: str, tone: str = "ink", role: str | None = None, cls: str = "") -> "Flow":
        """一段话，自动折行。每行的 id 是 §{id}0、§{id}1……，都带类 §{id}，可以成组做动画。"""
        k = self.k
        face = k.face(size, role)[1]
        lines = wrap(text, k.px(size, role), self.box.w, latin_width(face.latin))
        for i, line in enumerate(lines):
            self.txt(f"{id_}{i}", size, line, tone, role, gap=None if i == 0 else round(k.px(size, role) * 0.12), cls=cls or id_)
        return self

    def em(self, id_: str, size: str | int, text: str, fill: str = "accent", gap: int | None = None, cls: str = "") -> "Flow":
        k, b = self.k, self.box
        align = "center" if self.align == "center" else "left"
        return self.add(k.em_h(size), lambda y: k.em(id_, size, text, b.x, y, fill, b.w, align, cls), gap)

    def tag(self, id_: str, text: str, fill: str = "", gap: int | None = None, cls: str = "") -> "Flow":
        k, b = self.k, self.box
        x = b.cx if self.align == "center" else b.r if self.align == "right" else b.x
        return self.add(k.tag_h(), lambda y: k.tag(id_, text, x, y, fill, self.align, cls, "" if fill else self.chip), gap)

    def num(self, id_: str, size: str | int, text: str, unit: str = "", tone: str = "ink", gap: int | None = None,
            cls: str = "") -> "Flow":
        k, b = self.k, self.box
        pad = round(k.px(size, "display") * 0.1)
        return self.add(k.px(size, "display") + 2 * pad, lambda y: k.num(id_, size, text, b.x, y + pad, unit, b.w, self.align, tone, cls), gap)

    def rule(self, id_: str, length: int, tone: str = "accent", gap: int | None = None) -> "Flow":
        k = self.k
        return self.add(k.s.stroke * 2, lambda y: k.rule(id_, self._x(length), y, length, tone, thick=k.s.stroke * 2), gap)

    @property
    def height(self) -> int:
        return sum(before + h for before, h, _ in self.items)

    def render(self) -> str:
        total, b = self.height, self.box
        squeeze = 1.0
        gaps = sum(before for before, _, _ in self.items)
        if total > b.h and gaps:
            squeeze = max(0.3, 1 - (total - b.h) / gaps)
            total = sum(round(before * squeeze) + h for before, h, _ in self.items)
        if total > b.h + OVERFLOW_TOLERANCE_PX:
            self.k.issues.append(f"§{self._first or '这一块'} 所在的区域放不下：内容要 {total}px 高，区域只有 {b.h}px。减内容或拆成两镜")
        y = b.y + (b.h - total) // 2 if self.valign == "center" else b.b - total if self.valign == "bottom" else b.y
        out = []
        for before, h, render in self.items:
            y += round(before * squeeze)
            out.append(render(y))
            y += h
        return "".join(out)
