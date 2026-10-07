"""主线画面：贯穿全片、告诉观众“现在讲到哪了”的固定元素，放在顶部版面家具和内容区之间的那一条里。

每镜调用一次，传入这一镜的位置；rail 和 dots 还要传上一镜的位置，游标才会从上一镜滑过来。
"""
from __future__ import annotations

from stylekit import Kit

Part = tuple[str, str]


TAB_SCALE = 0.8


def _row_y(K: Kit) -> int:
    """主线画面这一条的顶边：紧贴在顶部版面家具下面。"""
    px = K.px("label")
    return K.c.head_y + round(px * (2.0 if K.s.chrome == "boxed" else 1.7)) + 8


def tabs(K: Kit, labels: list[str], active: tuple[int, ...] = ()) -> str:
    """几个标签并排，讲到哪一方哪个变实。active 里放要点亮的序号（从 0 数）。适合两方或三方对比。"""
    y, x, out = _row_y(K), K.c.margin, []
    for i, label in enumerate(labels):
        on = i in active
        w = round((K.width(label, "label") + K.px("label") * 1.7) * TAB_SCALE)
        out.append(K.tag(f"tab{i}", label, x, y, "accent" if on else "", extra=f"opacity:{1 if on else 0.4};", scale=TAB_SCALE))
        x += w + K.c.gap // 2
    return "".join(out)


def rail(K: Kit, labels: list[str], cur: int, prev: int | None = None) -> Part:
    """一条导轨，上面每个刻度一个名字（年份、阶段），游标从上一镜的位置滑到这一镜的位置。适合时间演进和流程。"""
    c = K.c
    y = _row_y(K) + 8
    label_px = round(K.px("label") * 0.86)
    n = len(labels)
    xs = [c.margin + round(c.content.w * (i + 0.5) / n) for i in range(n)]
    r = max(7, round(K.px("label") * 0.3))
    html = K.rule("rl", c.margin, y, c.content.w, "line", thick=2)
    for i, (label, x) in enumerate(zip(labels, xs)):
        w = round(c.content.w / n)
        html += K.txt(f"rt{i}", label_px, label, x - w // 2, y + 12, w, "center", "ink" if i == cur else "muted", "label")
        html += f'<div class="k-circle" style="left:{x - 4}px;top:{y - 3}px;width:8px;height:8px;border:0;background:{K.tone("line")}"></div>'
    html += (f'<div id="§rc" class="k-circle" style="left:{xs[cur] - r}px;top:{y + 1 - r}px;width:{2 * r}px;height:{2 * r}px;'
             f'border:0;background:{K.tone("accent")};box-shadow:0 0 0 3px {K.tone("ink")}"></div>')
    start = xs[cur if prev is None else prev] - xs[cur]
    js = f'tl.fromTo("#§rc", {{ x: {start} }}, {{ x: 0, duration: 0.7, ease: "power2.inOut" }}, 0.25);' if start else ""
    return html, js


def dots(K: Kit, total: int, cur: int) -> str:
    """一排小格子表示“第几条 / 共几条”，当前这条用强调色，讲过的用实心。适合清单要点。cur 从 0 数。"""
    y = _row_y(K)
    w = round(K.px("label") * 1.6)
    h = max(8, round(K.px("label") * 0.36))
    out = []
    for i in range(total):
        fill = K.tone("accent") if i == cur else K.tone("ink") if i < cur else "transparent"
        out.append(f'<div class="k-cell" style="left:{K.c.margin + i * (w + 8)}px;top:{y + 6}px;width:{w}px;height:{h}px;'
                   f'background:{fill};border-width:2px"></div>')
    return "".join(out)
