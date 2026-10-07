"""带结构的画面：柱状图、方格占比、步骤链、清单、对照表。用法和 scenes.py 一样，返回 (html, js)。"""
from __future__ import annotations

from canvas import Box
from flow import Flow
from stylekit import Kit

Part = tuple[str, str]


def _titled(K: Kit, box: Box | None, title: str, cue: str, p: str) -> tuple[Box, str, list[str]]:
    """可选的小标题，返回剩下的区域。"""
    b = box or K.c.content
    if not title:
        return b, "", []
    used = K.line_h("md") + K.c.gap
    return (Box(b.x, b.y + used, b.w, b.h - used), K.txt(f"{p}h", "md", title, b.x, b.y, b.w),
            [f'enter("#§{p}h", {cue});'])


def bars(K: Kit, items: list[tuple[str, float, str]], unit: str = "", title: str = "", title_cue: str = "0.3",
         highlight: int = -1, decimals: int = 0, box: Box | None = None, p: str = "b") -> Part:
    """柱状图。items 每项是 (名字, 数值, cue)；highlight 是要用强调色的那一根（从 0 数，-1 表示最后一根）。
    横屏是竖着的柱子，竖屏是横着的条。"""
    b, html, js = _titled(K, box, title, title_cue, p)
    top = max(v for _, v, _ in items) or 1
    hot = highlight % len(items)
    label_h, value_h = K.line_h("xs"), K.line_h("sm")
    if K.c.tall:
        rows = b.rows(len(items), K.c.gap)
        for i, ((name, value, cue), r) in enumerate(zip(items, rows)):
            bar_h = max(24, min(r.h - label_h - 8, round(K.px("md"))))
            value_w = K.width(f"{value:.{decimals}f}{unit}", "sm") + K.c.gap
            length = max(12, round((r.w - value_w) * value / top))
            y = r.y + label_h + 8
            html += (K.txt(f"{p}l{i}", "xs", name, r.x, r.y, r.w, tone="muted")
                     + K.bar(f"{p}r{i}", Box(r.x, y, length, bar_h), "accent" if i == hot else "ink")
                     + K.txt(f"{p}v{i}", "sm", f"{value:.{decimals}f}{unit}", r.x + length + K.c.gap // 2, y + (bar_h - value_h) // 2))
            js += [f'fade("#§{p}l{i}", {cue} - 0.3);', f'wipe("#§{p}r{i}", {cue} - 0.1, 0.7);', f'fade("#§{p}v{i}", {cue} + 0.45);']
        return html, "\n".join(js)
    cols = b.cols(len(items), K.c.gap * 2)
    base_y = b.b - label_h - 12
    full = base_y - b.y - value_h - 12
    for i, ((name, value, cue), c) in enumerate(zip(items, cols)):
        w = min(c.w, round(K.px("lg") * 1.6))
        h = max(12, round(full * value / top))
        x = c.x + (c.w - w) // 2
        html += (K.bar(f"{p}r{i}", Box(x, base_y - h, w, h), "accent" if i == hot else "ink")
                 + K.txt(f"{p}v{i}", "sm", f"{value:.{decimals}f}{unit}", c.x, base_y - h - value_h - 6, c.w, "center")
                 + K.txt(f"{p}l{i}", "xs", name, c.x, base_y + 12, c.w, "center", "muted"))
        js += [f'fade("#§{p}l{i}", {cue} - 0.3);', f'grow("#§{p}r{i}", {cue} - 0.1, 0.7);', f'fade("#§{p}v{i}", {cue} + 0.45);']
    html += K.rule(f"{p}x", b.x, base_y, b.w, "line")
    js.append(f'wipe("#§{p}x", 0.3, 0.6);')
    return html, "\n".join(js)


def grid_fill(K: Kit, total: int, lit: int, cue: str, lit_cue: str = "", label: str = "", value: str = "",
              cols: int = 10, box: Box | None = None, p: str = "g") -> Part:
    """一片方格里点亮其中一部分，表示“很多”或“占多少”。value 是旁边的大字（如 "7/10"），label 是它下面的说明。"""
    b = box or K.c.content
    gap = K.c.gap * 2
    grid_box, text_box = b.split_v(0.62, gap) if K.c.tall else b.split_h(0.56, gap)
    rows = -(-total // cols)
    space = max(6, round(grid_box.w * 0.016))
    size = min((grid_box.w - space * (cols - 1)) // cols, (grid_box.h - space * (rows - 1)) // rows)
    gx = grid_box.x + (grid_box.w - cols * (size + space) + space) // 2
    gy = grid_box.y + (grid_box.h - rows * (size + space) + space) // 2
    cells = "".join(
        f'<div id="§{p}{i}" class="k-cell §{p}c{" §" + p + "on" if i < lit else ""}" style="left:{gx + (i % cols) * (size + space)}px;'
        f'top:{gy + (i // cols) * (size + space)}px;width:{size}px;height:{size}px"></div>' for i in range(total))
    js = [f'pop(".§{p}c", {cue} - 0.2, 0.3, {min(0.05, 1.2 / total):.3f});',
          f'tint(".§{p}on", {lit_cue or cue + " + 0.9"}, "{K.hex("accent")}", 0.2, {min(0.06, 1.0 / max(1, lit)):.3f});']
    f = Flow(K, text_box, "center" if K.c.tall else "left", "center")
    if value:
        f.num(f"{p}v", "xl", value, tone="ink")
        js.append(f'enter("#§{p}v", {lit_cue or cue + " + 0.9"});')
    if label:
        f.para(f"{p}t", "sm", label, "muted")
        js.append(f'enter(".§{p}t", {lit_cue or cue + " + 0.9"} + 0.3, 0.08);')
    return cells + f.render(), "\n".join(js)


def steps(K: Kit, items: list[tuple[str, str]], title: str = "", title_cue: str = "0.3", current: int = -1,
          box: Box | None = None, p: str = "s") -> Part:
    """步骤链：一串编号圆点用线连起来。items 每项是 (步骤名, cue)；current 是要标成强调色的那一步（从 0 数，-1 表示不标）。
    横屏横着排，竖屏竖着排。"""
    b, html, js = _titled(K, box, title, title_cue, p)
    n = len(items)
    r = round(K.px("md") * 0.62)
    num_px = round(r * 0.9)
    if K.c.tall:
        rows = b.rows(n, 0)
        x = b.x + r
        for i, ((name, cue), row) in enumerate(zip(items, rows)):
            if i:
                html += K.rule(f"{p}c{i}", x - K.s.stroke // 2, rows[i - 1].cy + r, row.cy - rows[i - 1].cy - 2 * r, "line", True)
                js.append(f'grow("#§{p}c{i}", {cue} - 0.4, 0.35, 0, "center top");')
            html += _node(K, f"{p}n{i}", x, row.cy, r, num_px, i, i == current)
            html += K.txt(f"{p}t{i}", "md", name, x + r + K.c.gap, row.cy - K.line_h("md") // 2, b.r - x - r - K.c.gap)
            js += [f'pop("#§{p}n{i}", {cue} - 0.15);', f'enter("#§{p}t{i}", {cue} - 0.05);']
        return html, "\n".join(js)
    cols = b.cols(n, K.c.gap)
    y = b.cy - K.line_h("sm") // 2
    for i, ((name, cue), col) in enumerate(zip(items, cols)):
        if i:
            html += K.rule(f"{p}c{i}", cols[i - 1].cx + r, y - K.s.stroke // 2, col.cx - cols[i - 1].cx - 2 * r, "line")
            js.append(f'wipe("#§{p}c{i}", {cue} - 0.4, 0.35);')
        html += _node(K, f"{p}n{i}", col.cx, y, r, num_px, i, i == current)
        html += K.txt(f"{p}t{i}", "sm", name, col.x, y + r + K.c.gap // 2, col.w, "center")
        js += [f'pop("#§{p}n{i}", {cue} - 0.15);', f'enter("#§{p}t{i}", {cue} - 0.05);']
    return html, "\n".join(js)


def _node(K: Kit, id_: str, cx: int, cy: int, r: int, num_px: int, i: int, hot: bool) -> str:
    fill = "accent" if hot else "bg"
    return K.circle(id_, cx, cy, r, fill, "ink",
                    f'<span class="k-l" style="font-size:{num_px}px;letter-spacing:0;color:{K.on(fill)}">{i + 1}</span>')


def checklist(K: Kit, items: list[tuple[str, str]], title: str = "", title_cue: str = "0.3", mark: str = "check",
              box: Box | None = None, p: str = "k") -> Part:
    """清单：一行一个方框，说到哪条就把哪条的勾（或叉）画出来。items 每项是 (文字, cue)；mark 是 "check" 或 "cross"。"""
    b, html, js = _titled(K, box, title, title_cue, p)
    size = "md" if len(items) <= 4 else "sm"
    line = K.line_h(size)
    row_h = min(round(line * 1.9), b.h // len(items))
    side = round(line * 0.82)
    y0 = b.y + (b.h - row_h * len(items)) // 2
    for i, (text, cue) in enumerate(items):
        y = y0 + i * row_h + (row_h - line) // 2
        box_y = y + (line - side) // 2
        html += (f'<div id="§{p}b{i}" class="k-cell" style="left:{b.x}px;top:{box_y}px;width:{side}px;height:{side}px"></div>'
                 + K.icon(f"{p}m{i}", mark, b.x + round(side * 0.1), box_y + round(side * 0.1), round(side * 0.8), "pop")
                 + K.txt(f"{p}t{i}", size, text, b.x + side + K.c.gap, y, b.w - side - K.c.gap))
        js += [f'pop("#§{p}b{i}", {cue} - 0.35);', f'enter("#§{p}t{i}", {cue} - 0.2);', f'draw("#§{p}m{i} path", {cue} + 0.1, 0.4);']
    return html, "\n".join(js)


def compare(K: Kit, heads: tuple[str, str], rows: list[tuple], head_cue: str = "0.3",
            box: Box | None = None, p: str = "t") -> Part:
    """对照表：两列各有一个表头，每行是 (比的是什么, 左边的说法, 右边的说法, cue)，可以再加第 5 项作为右边单独的出现时间。"""
    b = box or K.c.content
    label_w = round(b.w * (0.24 if K.c.tall else 0.2))
    gap = K.c.gap
    col_w = (b.w - label_w - 2 * gap) // 2
    xs = (b.x + label_w + gap, b.x + label_w + 2 * gap + col_w)
    head_h = K.tag_h() + gap
    row_h = min((b.h - head_h) // len(rows), round(K.line_h("md") * 2.2))
    y0 = b.y + (b.h - head_h - row_h * len(rows)) // 2
    html = K.tag(f"{p}h0", heads[0], xs[0], y0) + K.tag(f"{p}h1", heads[1], xs[1], y0, "accent")
    js = [f'enter("#§{p}h0", {head_cue});', f'enter("#§{p}h1", {head_cue} + 0.15);']
    for i, (label, left, right, cue, *rest) in enumerate(rows):
        right_cue = rest[0] if rest else f"{cue} + 0.25"
        y = y0 + head_h + i * row_h
        ty = y + (row_h - K.line_h("sm")) // 2
        html += (K.rule(f"{p}r{i}", b.x, y, b.w, "line", thick=2)
                 + K.txt(f"{p}l{i}", "xs", label, b.x, y + (row_h - K.line_h("xs")) // 2, label_w, tone="muted")
                 + K.txt(f"{p}a{i}", "sm", left, xs[0], ty, col_w)
                 + K.txt(f"{p}b{i}", "sm", right, xs[1], ty, col_w, tone="pop"))
        js += [f'wipe("#§{p}r{i}", {cue} - 0.4, 0.4);', f'fade("#§{p}l{i}", {cue} - 0.3);',
               f'enter("#§{p}a{i}", {cue} - 0.15);', f'enter("#§{p}b{i}", {right_cue});']
    return html, "\n".join(js)
