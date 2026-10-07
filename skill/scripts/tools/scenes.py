"""常用画面：标题、大数字、定义、对照、并列卡片、提问、叠卡。

每个函数返回 (html, js)，位置从画幅的内容区算出来，横屏并排、竖屏上下叠，不用写坐标。
参数里的 cue 是出现时间，写成字符串："@[词]"、"@[词] - 0.1" 或一个秒数。
同一镜里放两个画面时给它们不同的 box 和不同的前缀 p，再用 join() 合起来。
"""
from __future__ import annotations

import math
from collections.abc import Callable

from canvas import Box
from flow import Flow
from stylekit import Kit

Part = tuple[str, str]
NUMBER_TARGET_WIDTH = 0.6  # 大数字尽量占到区域宽度的这个比例
NUMBER_MAX_GROW = 2.2
Line = str | tuple[str, str]


def join(*parts: Part | str) -> Part:
    """把几个画面合成一镜。纯 HTML 字符串（比如主线画面）也可以直接放进来。"""
    html = "".join(p if isinstance(p, str) else p[0] for p in parts)
    js = "\n".join(p[1] for p in parts if not isinstance(p, str))
    return html, js


def _tilt(kit: Kit, i: int) -> float:
    return kit.s.tilt * (1 if i % 2 == 0 else -1)


def _room(kit: Kit, box: Box) -> Box:
    """卡片要倾斜时先往里收一点，转起来的四个角才不会顶到旁边的东西。"""
    if not kit.s.tilt:
        return box
    return box.inset(round(box.h * math.sin(math.radians(kit.s.tilt)) / 2) + 4, round(box.w * math.sin(math.radians(kit.s.tilt)) / 2) + 4)


def _fill(kit: Kit, i: int, default: str = "") -> str:
    return f"p{i}" if kit.s.palette else default or kit.s.card_fill


def filled_card(K: Kit, id_: str, box: Box, fill: str, build: Callable[[Flow, str], None], rot: float = 0,
                align: str = "left", gap: int | None = None) -> str:
    """一张卡片加里面的内容。build(flow, 文字颜色) 往卡片里排东西；内容跟着卡片一起动、一起倾斜。"""
    ink = K.on(fill)
    plain = fill in (K.s.card_fill, "surface", "transparent", "bg")
    chip = "" if plain else f"color:{ink};border:2px solid {ink};background:transparent;box-shadow:none;"
    with K.local(box) as inner:
        f = Flow(K, inner.inset(K.c.gap), align, "center", gap, chip)
        build(f, ink)
        content = f.render()
    return K.card(id_, box, fill, content, rot)


def headline(K: Kit, lines: list[Line], cues: list[str], kicker: str = "", sub: str = "", sub_cue: str = "",
             size: str = "xl", align: str = "", box: Box | None = None, p: str = "h") -> Part:
    """大字标题或一句结论。lines 一项一行；写成 ("词", "em") 的那一行渲染成强调词。cues 和 lines 一一对应。"""
    if len(lines) != len(cues):
        raise ValueError(f"headline：lines 有 {len(lines)} 行，cues 有 {len(cues)} 个，要一一对应")
    f = Flow(K, box or K.c.content, align or K.s.align, "center", gap=round(K.px(size) * 0.14))
    js = []
    if kicker:
        f.tag(f"{p}k", kicker)
        f.space(K.c.gap // 2)
        js.append(f'enter("#§{p}k", Math.max(0.2, {cues[0]} - 0.4));')
    for i, (line, cue) in enumerate(zip(lines, cues)):
        if isinstance(line, tuple):
            f.em(f"{p}{i}", size, line[0])
            js.append(f'blk("#§{p}{i}", {cue} - 0.1);')
        else:
            f.txt(f"{p}{i}", size, line)
            js.append(f'enter("#§{p}{i}", {cue} - 0.15);')
    if sub:
        f.space(K.c.gap)
        f.para(f"{p}s", "sm", sub, "muted")
        js.append(f'enter(".§{p}s", {sub_cue or cues[-1] + " + 0.5"}, 0.08);')
    return f.render(), "\n".join(js)


def big_number(K: Kit, value: float, cue: str, unit: str = "", label: str = "", note: str = "", note_cue: str = "",
               start: float = 0, decimals: int = 0, prefix: str = "", comma: bool = False, size: str = "mega",
               align: str = "", box: Box | None = None, p: str = "n") -> Part:
    """一个大数字，从 start 数到 value。label 在数字上面，note 在下面。"""
    shown = f"{value:,.{decimals}f}" if comma else f"{value:.{decimals}f}"
    b = box or K.c.content
    f = Flow(K, b, align or K.s.align, "center")
    js = []
    if label:
        f.tag(f"{p}l", label)
        js.append(f'enter("#§{p}l", Math.max(0.2, {cue} - 0.5));')
    natural = K.width(prefix + shown, size, "display") + (K.px(size, "display") * 0.4 * len(unit) if unit else 0)
    grow = min(NUMBER_MAX_GROW, b.w * NUMBER_TARGET_WIDTH / natural, b.h * 0.42 / K.px(size, "display"))
    f.num(f"{p}v", f"{size}*{max(1.0, grow):.2f}", prefix + shown, unit, "pop")
    fmt = (f'v => "{prefix}" + v.toLocaleString("en-US", {{ minimumFractionDigits: {decimals}, maximumFractionDigits: {decimals} }})'
           if comma else f'v => "{prefix}" + v.toFixed({decimals})')
    js += [f'fade("#§{p}v", {cue} - 0.2, 0.3);', f'count("#§{p}v-v", {start}, {value}, {cue} - 0.1, 1.2, {fmt});']
    if note:
        f.space(K.c.gap // 2)
        f.para(f"{p}t", "sm", note, "muted")
        js.append(f'enter(".§{p}t", {note_cue or cue + " + 1.0"}, 0.08);')
    return f.render(), "\n".join(js)


def define(K: Kit, term: str, keyword: str, cues: tuple[str, str], label: str = "", link: str = "是", note: str = "",
           note_cue: str = "", fill: str = "accent", box: Box | None = None, p: str = "d") -> Part:
    """“X 是 Y”：左边（竖屏在上）是名词，右边（竖屏在下）是一张写着关键词的大卡片。"""
    b = box or K.c.content
    gap = K.c.gap * 2
    a, c = b.split_v(0.42, gap) if K.c.tall else b.split_h(0.46, gap)
    f = Flow(K, a, "left", "center")
    js = []
    if label:
        f.tag(f"{p}l", label)
        js.append(f'enter("#§{p}l", Math.max(0.2, {cues[0]} - 0.45));')
    tail = (f'<span id="§{p}i" class="k-b" style="font-size:{K.px("sm")}px;margin-left:0.3em;letter-spacing:0;'
            f'color:{K.tone("muted")}">{link}</span>')
    f.add(K.line_h("lg"), lambda y: K.txt(f"{p}t", "lg", term, a.x, y, tail=tail))
    js += [f'enter("#§{p}t", {cues[0]} - 0.15);', f'fade("#§{p}i", {cues[0]} + 0.3);']
    if note:
        f.space(K.c.gap // 2)
        f.para(f"{p}n", "sm", note, "muted")
        js.append(f'enter(".§{p}n", {note_cue or cues[1] + " + 0.6"}, 0.08);')
    side = min(c.h, round(c.w * 0.62)) if K.c.tall else min(c.h, round(c.w * 0.7))
    width = min(c.w, round(side * 1.5))
    card = Box(c.x + (c.w - width) // 2, c.y + (c.h - side) // 2, width, side)
    html = f.render() + filled_card(K, f"{p}c", _room(K, card), fill, lambda fl, ink: fl.txt(f"{p}w", "mega", keyword, ink),
                                    -_tilt(K, 0), "center")
    js.append(f'enter("#§{p}c", {cues[1]} - 0.15);')
    return html, "\n".join(js)


def versus(K: Kit, left: tuple[str, str, str], right: tuple[str, str, str], cues: tuple[str, str], mode: str = "vs",
           box: Box | None = None, p: str = "v") -> Part:
    """两方对照。left / right 各是 (小标签, 大字, 一句说明)。mode="vs" 并列对比；mode="to" 是从左变到右，右边出现时左边变暗。"""
    b = box or K.c.content
    gap = round(K.px("md") * 1.5)
    boxes = b.rows(2, gap) if K.c.tall else b.cols(2, gap)
    fills = (_fill(K, 1, "surface"), "accent")
    html, js = "", []
    for i, (side, bx, fill, cue) in enumerate(zip((left, right), boxes, fills, cues)):
        g = f"{p}{i}"

        def build(f: Flow, ink: str, side: tuple[str, str, str] = side, g: str = g) -> None:
            if side[0]:
                f.tag(f"{g}k", side[0])
            f.txt(f"{g}t", "lg", side[1], ink)
            if side[2]:
                f.para(f"{g}s", "sm", side[2], ink)

        html += filled_card(K, g, _room(K, bx), fill, build, _tilt(K, i))
        js.append(f'enter("#§{g}", {cue} - 0.15);')
    mid_x, mid_y = (b.cx, boxes[0].b + gap // 2) if K.c.tall else (boxes[0].r + gap // 2, b.cy)
    r = round(gap * 0.42)
    if mode == "to":
        size = r * 2
        html += K.icon(f"{p}a", "down" if K.c.tall else "arrow", mid_x - r, mid_y - r, size, "ink")
        js += [f'draw("#§{p}a path", {cues[1]} - 0.45, 0.5);', f'dim("#§{p}0", {cues[1]} + 0.1, 0.4);']
    else:
        html += K.circle(f"{p}a", mid_x, mid_y, r, "ink", "ink",
                         f'<span class="k-l" style="font-size:{round(r * 0.62)}px;color:{K.tone("bg")}">VS</span>')
        js.append(f'pop("#§{p}a", {cues[1]} - 0.4);')
    return html, "\n".join(js)


def _grid_boxes(K: Kit, box: Box, n: int) -> list[Box]:
    """n 张卡片怎么排：横屏尽量排成一行，超过 4 张排两行；竖屏排成一列，超过 4 张排两列。"""
    gap = K.c.gap
    if K.c.tall:
        cols = 1 if n <= 4 else 2
    else:
        cols = n if n <= 4 else (n + 1) // 2
    rows = -(-n // cols)
    return [cell for row in box.rows(rows, gap) for cell in row.cols(cols, gap)][:n]


def cards(K: Kit, items: list[tuple[str, str, str]], title: str = "", title_cue: str = "0.3", numbered: bool = True,
          box: Box | None = None, p: str = "c") -> Part:
    """并列的几样东西，一样一张卡片。items 每项是 (名字, 一句说明, cue)，2–6 项。"""
    b = box or K.c.content
    html, js = "", []
    if title:
        html += K.txt(f"{p}h", "md", title, b.x, b.y, b.w)
        js.append(f'enter("#§{p}h", {title_cue});')
        b = Box(b.x, b.y + K.line_h("md") + K.c.gap, b.w, b.h - K.line_h("md") - K.c.gap)
    for i, ((name, sub, cue), bx) in enumerate(zip(items, _grid_boxes(K, b, len(items)))):
        g = f"{p}{i}"

        def build(f: Flow, ink: str, i: int = i, name: str = name, sub: str = sub, g: str = g) -> None:
            if numbered:
                f.txt(f"{g}n", "sm", f"{i + 1:02d}", ink, "label")
            f.txt(f"{g}t", "md", name, ink)
            if sub:
                f.para(f"{g}s", "xs", sub, ink)

        html += filled_card(K, g, _room(K, bx), _fill(K, i), build, _tilt(K, i) * 0.5, gap=K.c.gap // 2)
        js.append(f'enter("#§{g}", {cue} - 0.15);')
    return html, "\n".join(js)


def ask(K: Kit, question: str, cue: str, answer: str = "", answer_cue: str = "", label: str = "", box: Box | None = None,
        p: str = "q") -> Part:
    """一个提问：输入框里逐字打出问题。answer 是下面跟着出现的一句回答。"""
    b = box or K.c.content
    pad = K.c.gap
    size = "md" if K.width(question, "md") <= b.w - 4 * pad else "sm"
    avail = b.w - 2 * pad
    fits = K.width(question, size) <= avail
    box_h = K.line_h(size) + 2 * pad
    total = box_h + (K.c.gap + K.line_h("md") if answer else 0) + (K.tag_h() + K.c.gap // 2 if label else 0)
    y = b.y + (b.h - total) // 2
    html, js = "", []
    if label:
        html += K.tag(f"{p}l", label, b.x, y)
        js.append(f'enter("#§{p}l", Math.max(0.2, {cue} - 0.6));')
        y += K.tag_h() + K.c.gap // 2
    field = Box(b.x, y, b.w, box_h)
    text_w = min(K.width(question, size), avail)
    html += (K.card(f"{p}c", field, "surface")
             + K.txt(f"{p}t", size, question, field.x + pad, field.y + pad, None if fits else avail)
             + K.rule(f"{p}u", field.x + pad + text_w + 8, field.y + pad, K.line_h(size), "accent", True, 6))
    js += [f'fade("#§{p}c", Math.max(0.1, {cue} - 0.5), 0.3);', f'type("#§{p}t", {cue}, {max(0.6, len(question) * 0.09):.2f}, {len(question)});',
           f'fade("#§{p}u", {cue} + {max(0.6, len(question) * 0.09):.2f}, 0.1);']
    if answer:
        html += K.em(f"{p}a", "md", answer, b.x, field.b + K.c.gap, "accent", b.w)
        js.append(f'blk("#§{p}a", {answer_cue or cue + " + 1.6"});')
    return html, "\n".join(js)


def stack(K: Kit, items: list[tuple[str, str]], title: str = "", title_cue: str = "0.3", box: Box | None = None,
          p: str = "k") -> Part:
    """几样东西一层层叠起来：每张卡片比上一张往右下错开一点。items 每项是 (文字, cue)。"""
    b = box or K.c.content
    html, js = "", []
    if title:
        html += K.txt(f"{p}h", "md", title, b.x, b.y, b.w)
        js.append(f'enter("#§{p}h", {title_cue});')
        b = Box(b.x, b.y + K.line_h("md") + K.c.gap, b.w, b.h - K.line_h("md") - K.c.gap)
    n = len(items)
    step_y = min(round(K.line_h("md") * 1.15), (b.h - K.line_h("md") * 2) // max(1, n - 1))
    step_x = round(b.w * 0.05)
    w, h = b.w - step_x * (n - 1), b.h - step_y * (n - 1)
    for i, (text, cue) in enumerate(items):
        fill, g = _fill(K, i), f"{p}{i}"
        fill = "bg" if fill == "transparent" else fill
        bx = Box(b.x + i * step_x, b.y + i * step_y, w, h)
        with K.local(bx) as inner:
            label = K.txt(f"{g}t", "md", text, K.c.gap, max(8, (step_y - K.line_h("md")) // 2), inner.w - 2 * K.c.gap, tone=K.on(fill))
        html += K.card(g, bx, fill, label)
        js.append(f'drop("#§{g}", {cue} - 0.15);')
    return html, "\n".join(js)
