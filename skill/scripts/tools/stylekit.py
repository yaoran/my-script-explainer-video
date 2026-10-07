"""风格和画面积木。

Style 描述一种风格（配色、字体、形状、底纹、动效气质、字幕样子），全部登记在 styles/ 里。
Kit 把一种风格和一种画幅绑在一起，提供统一的画面积木：txt / tag / card / em / num / rule / bar / cells / icon。
换风格、换画幅都不用改镜头脚本：颜色走 CSS 变量，字号和位置从 Canvas 换算。
"""
from __future__ import annotations

import html
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field

from canvas import Box, Canvas, fit_px, text_w
from colors import contrast, readable_on
from fontlib import font, latin_width, nearest_weight
from framekit import CaptionStyle, Font, Theme

SIZES = {"mega": 220, "xl": 150, "lg": 110, "md": 76, "sm": 52, "xs": 36, "label": 28}
DISPLAY_SIZES = ("mega", "xl", "lg", "md")
ROLE_CLASS = {"display": "k-d", "body": "k-b", "label": "k-l"}
FALLBACK_SANS, FALLBACK_SERIF = "Noto Sans SC", "Noto Serif SC"
MIN_FIT = 0.55
RAW_COLOR = ("#", "rgb", "var(", "color-mix")
POP_MIN_CONTRAST = 3.2  # 强调色和底色的对比度低于这个值时，强调色不能直接当文字颜色
ICONS = {
    "check": '<path d="M5 13 L10 18 L19 6" pathLength="1" stroke-dasharray="1"/>',
    "cross": '<path d="M6 6 L18 18 M18 6 L6 18" pathLength="1" stroke-dasharray="1"/>',
    "arrow": '<path d="M3 12 H20 M14 6 L20 12 L14 18" pathLength="1" stroke-dasharray="1"/>',
    "down": '<path d="M12 3 V20 M6 14 L12 20 L18 14" pathLength="1" stroke-dasharray="1"/>',
    "plus": '<path d="M12 4 V20 M4 12 H20" pathLength="1" stroke-dasharray="1"/>',
    "play": '<path d="M7 4 L20 12 L7 20 Z" pathLength="1" stroke-dasharray="1"/>',
}


@dataclass(frozen=True)
class Face:
    """一种字体角色：西文字体 + 中文字体 + 字重。tracking 的单位是 em。"""

    latin: str
    cjk: str
    weight: int = 400
    tracking: float = 0.0
    case: str = ""
    lh: float = 1.14
    fallback: str = ""  # 中文字体缺字时用谁补，留空则按衬线 / 无衬线自动选

    @property
    def families(self) -> tuple[str, ...]:
        fallback = self.fallback or (FALLBACK_SERIF if "Serif" in self.cjk else FALLBACK_SANS)
        return tuple(dict.fromkeys((self.latin, self.cjk, fallback)))

    @property
    def stack(self) -> str:
        return ",".join(f'"{f}"' for f in self.families) + ",sans-serif"

    def fonts(self) -> tuple[Font, ...]:
        return tuple(font(f, self.weight) for f in self.families)


@dataclass(frozen=True)
class Look:
    """一种配色组合。空字符串表示沿用风格的默认值。同一种风格可以有几种，用来区分章节镜或逐镜换底色。"""

    bg: str = ""
    ink: str = ""
    accent: str = ""
    accent2: str = ""
    surface: str = ""
    muted: str = ""
    line: str = ""
    on_accent: str = ""


@dataclass(frozen=True)
class Style:
    name: str
    label: str
    mood: str
    fit: str
    bg: str
    ink: str
    accent: str
    display: Face
    body: Face
    tag_face: Face
    accent2: str = ""
    surface: str = ""
    muted: str = ""
    line: str = ""
    on_accent: str = ""
    palette: tuple[str, ...] = ()
    looks: tuple[Look, ...] = ()
    look_rule: str = "none"  # none / chapter（章节镜用第 2 种）/ cycle（逐镜轮换）
    scale: float = 1.0
    radius: int = 0
    stroke: int = 3
    card: str = "border:2px solid var(--k-line);"
    card_fill: str = "surface"
    tag: str = "border:2px solid var(--k-ink);padding:0.34em 0.8em;"
    tag_radius: int = -1  # 标签的圆角，-1 表示和卡片一样
    bar: str = ""  # 柱子和条的附加样式，粗框风格给它加描边
    em: str = "block"  # block / marker / underline / outline / pill
    ground: Callable[[Canvas], str] = field(default=lambda c: "")
    chrome: str = "plain"  # plain / rules / bar / boxed / none
    align: str = "left"  # 标题类画面默认靠左还是居中
    ease: str = "power3.out"
    entrance: str = "up"
    tilt: float = 0.0
    transitions: tuple[str, str, str] = ("push-slide LEFT", "crossfade", "blur-crossfade")
    cap_plate: str = ""
    cap_active: str = ""
    cap_colors: tuple[str, str, str] = ("", "", "")
    cap_face: str = "display"
    cap_weight: int = 0  # 字幕字重，0 表示沿用 cap_face 那个角色的字重
    bgm: str = "calm"
    origin: str = "preset"


class Kit:
    """一条片子的画面积木。每个积木返回一段 HTML，id 以 § 开头，位置和尺寸是像素。"""

    def __init__(self, style: Style, canvas: Canvas, title: str = "") -> None:
        self.s, self.c, self.title = style, canvas, title
        self.look = Look()
        self.boxes: list[tuple[str, Box]] = []
        self.issues: list[str] = []
        self._origin = (0, 0)

    def _rec(self, id_: str, box: Box) -> None:
        ox, oy = self._origin
        self.boxes.append((id_, Box(box.x + ox, box.y + oy, box.w, box.h)))

    @contextmanager
    def local(self, box: Box) -> Iterator[Box]:
        """在一张卡片内部排版：这段代码里的坐标以卡片左上角为原点，返回卡片内部的区域。"""
        saved = self._origin
        self._origin = (saved[0] + box.x, saved[1] + box.y)
        try:
            yield Box(0, 0, box.w, box.h)
        finally:
            self._origin = saved

    # ---- 颜色 ----
    def hex(self, tone: str) -> str:
        """色名对应的实际色值（写进 JS 用）。色名：ink accent accent2 surface muted line bg on_accent p0 p1…
        另有 pop：强调色够醒目就用强调色，否则退回主文字色，专门给“彩色的字”用。"""
        s = self.s
        if tone.startswith(RAW_COLOR) or tone == "transparent":
            return tone
        if tone[0] == "p" and tone[1:].isdigit():
            return s.palette[int(tone[1:]) % len(s.palette)] if s.palette else self.hex("accent")
        value = getattr(self.look, tone, "") or getattr(s, tone, "")
        if value:
            return value
        ink, bg = self.hex("ink"), self.hex("bg")
        fallbacks = {"accent2": self.hex("accent"), "surface": "transparent", "line": ink,
                     "muted": f"color-mix(in srgb, {ink} 62%, {bg})"}
        if tone == "on_accent":
            return readable_on(self.hex("accent"), (ink, bg), bg)
        if tone == "pop":
            accent = self.hex("accent")
            return accent if contrast(accent, bg) >= POP_MIN_CONTRAST else ink
        if tone not in fallbacks:
            raise KeyError(f"不认识的色名 {tone!r}")
        return fallbacks[tone]

    def tone(self, tone: str) -> str:
        """色名对应的 CSS 值（写进 HTML 用），随本镜的配色组合变化。变量由 build_frames 按镜写进每个镜头文件。"""
        if tone.startswith(RAW_COLOR) or tone == "transparent" or tone[0] == "p" and tone[1:].isdigit():
            return self.hex(tone)
        return f"var(--k-{tone.replace('_', '-')})"

    def on(self, fill: str) -> str:
        """放在某个底色上的文字该用什么颜色。"""
        if fill == "accent":
            return self.tone("on_accent")
        if fill == "ink":
            return self.tone("bg")
        if fill in ("surface", "transparent", "bg"):
            return self.tone("ink")
        return readable_on(self.hex(fill), (self.hex("ink"), self.hex("bg")), self.hex("bg"))

    def vars(self) -> str:
        names = ("bg", "ink", "accent", "accent2", "surface", "muted", "line", "on_accent", "pop")
        return "".join(f"--k-{n.replace('_', '-')}:{self.hex(n)};" for n in names)

    # ---- 字 ----
    def face(self, size: str | int, role: str | None = None) -> tuple[str, Face]:
        name = size.split("*")[0] if isinstance(size, str) else size
        role = role or ("display" if name in DISPLAY_SIZES or isinstance(name, int) and name >= 70 else
                        "label" if name == "label" else "body")
        return role, {"display": self.s.display, "body": self.s.body, "label": self.s.tag_face}[role]

    def px(self, size: str | int, role: str | None = None) -> int:
        """字号（像素）。size 是档位名（mega xl lg md sm xs label），可以带倍数如 "mega*1.3"，也可以直接给 16:9 下的像素数。"""
        if isinstance(size, str):
            name, _, factor = size.partition("*")
            base = SIZES[name] * float(factor or 1)
        else:
            base = size
        if self.face(size, role)[0] == "display":
            base *= self.s.scale
        return self.c.sz(base)

    def line_h(self, size: str | int, role: str | None = None) -> int:
        return round(self.px(size, role) * self.face(size, role)[1].lh)

    def width(self, text: str, size: str | int, role: str | None = None) -> int:
        face = self.face(size, role)[1]
        shown = text.upper() if face.case == "upper" else text
        return round(text_w(shown, self.px(size, role), latin_width(face.latin), face.tracking))

    def txt(self, id_: str, size: str | int, text: str, x: int, y: int, w: int | None = None,
            align: str = "left", tone: str = "ink", role: str | None = None, extra: str = "", cls: str = "",
            tail: str = "") -> str:
        """一行文字。给了 w 就保证不超过这个宽度（放不下自动缩小），并按 align 在 w 内对齐。cls 是成组做动画用的类名。
        tail 是紧跟在文字后面的一小段 HTML（比如小一号的“是”），跟着文字走，不参与宽度计算。"""
        role, face = self.face(size, role)
        px = self.px(size, role)
        shown = text.upper() if face.case == "upper" else text
        if w is not None:
            fitted = fit_px(shown, px, w, latin_width(face.latin), face.tracking)
            if fitted < px * MIN_FIT:
                self.issues.append(f"§{id_} 这行字太长（“{text[:12]}…”），缩到最小也放不进 {w}px 宽：拆成两行或删字")
            px = max(round(px * MIN_FIT), fitted)
        est = round(text_w(shown, px, latin_width(face.latin), face.tracking))
        box = f"width:{w}px;text-align:{align};" if w is not None else ""
        self._rec(id_, Box(x, y, w if w is not None else est, round(px * face.lh)))
        group = f" §{cls}" if cls else ""
        return (f'<div id="§{id_}" class="k-a {ROLE_CLASS[role]}{group}" style="left:{x}px;top:{y}px;{box}'
                f'font-size:{px}px;color:{self.tone(tone)};{extra}">{html.escape(text, quote=False)}{tail}</div>')

    def tag(self, id_: str, text: str, x: int, y: int, fill: str = "", align: str = "left", cls: str = "",
            extra: str = "", scale: float = 1.0) -> str:
        """小标签。align="center" / "right" 时 x 是标签的中心 / 右边。scale 是相对正常标签的大小。"""
        px = round(self.px("label") * scale)
        w = round(self.width(text, "label") * scale) + round(px * 1.7)
        left = x - w // 2 if align == "center" else x - w if align == "right" else x
        color = f"background:{self.tone(fill)};color:{self.on(fill)};" if fill else ""
        self._rec(id_, Box(left, y, w, round(px * 2)))
        group = f" §{cls}" if cls else ""
        return (f'<div id="§{id_}" class="k-a k-l k-tag{group}" style="left:{left}px;top:{y}px;font-size:{px}px;'
                f'{color}{extra}">{html.escape(text, quote=False)}</div>')

    def tag_h(self) -> int:
        return round(self.px("label") * 2)

    def em(self, id_: str, size: str | int, text: str, x: int, y: int, fill: str = "accent",
           w: int | None = None, align: str = "left", cls: str = "") -> str:
        """强调词：按风格渲染成色块、荧光笔、下划线或描边。动画用 blk("#§id", t)。"""
        role, face = self.face(size)
        px = self.px(size)
        pad = round(px * 0.2) if self.s.em in ("block", "pill", "outline") else 0
        if w is not None:
            px = max(round(px * MIN_FIT), fit_px(text, px, w - 2 * pad, latin_width(face.latin), face.tracking))
        est = round(text_w(text, px, latin_width(face.latin), face.tracking)) + 2 * pad
        left = x + (w - est) // 2 if w is not None and align == "center" else x
        solid = self.s.em in ("block", "pill")
        bg = f"border-color:{self.tone(fill)}" if self.s.em == "outline" else f"background:{self.tone(fill)}"
        color = self.on(fill) if solid else self.tone("ink")
        self._rec(id_, Box(left, y, est, round(px * 1.3)))
        group = f" §{cls}" if cls else ""
        return (f'<div id="§{id_}" class="k-a {ROLE_CLASS[role]} k-em k-em-{self.s.em}{group}" style="left:{left}px;top:{y}px;'
                f'font-size:{px}px;padding:0 {pad}px"><span id="§{id_}-bg" class="k-em-bg" style="{bg}"></span>'
                f'<span id="§{id_}-t" class="k-em-t" style="color:{color}">{html.escape(text, quote=False)}</span></div>')

    def em_h(self, size: str | int) -> int:
        return round(self.px(size) * 1.3)

    def num(self, id_: str, size: str | int, text: str, x: int, y: int, unit: str = "", w: int | None = None,
            align: str = "left", tone: str = "ink", cls: str = "") -> str:
        """大数字加小一号的单位。数字在 #§id-v 里，计数动画改它的文字。"""
        role, face = self.face(size, "display")
        px = self.px(size, "display")
        unit_px = round(px * 0.36)
        need = text_w(text, px, latin_width(face.latin) * 1.12, face.tracking) + text_w(unit, unit_px) + (px * 0.08 if unit else 0)
        if w is not None and need > w:
            px, unit_px = round(px * w / need), round(unit_px * w / need)
            need = w
        box = f"width:{w}px;text-align:{align};" if w is not None else ""
        tail = f'<span class="k-b" style="font-size:{unit_px}px;margin-left:0.08em">{unit}</span>' if unit else ""
        self._rec(id_, Box(x, y, w if w is not None else round(need), px))
        group = f" §{cls}" if cls else ""
        # 大号数字的字框比字形高出一截，会被检查当成和上下的小字重叠；实际没有压住，这里声明是有意的
        return (f'<div id="§{id_}" class="k-a k-d k-num{group}" data-layout-allow-overlap style="left:{x}px;top:{y}px;{box}'
                f'font-size:{px}px;color:{self.tone(tone)}"><span id="§{id_}-v" data-layout-allow-overlap>{html.escape(text, quote=False)}</span>{tail}</div>')

    # ---- 形 ----
    def card(self, id_: str, box: Box, fill: str = "", inner: str = "", rot: float = 0, cls: str = "") -> str:
        fill = fill or self.s.card_fill
        tilt = f"transform:rotate({rot}deg);" if rot else ""
        group = f" §{cls}" if cls else ""
        self._rec(id_, box)
        return (f'<div id="§{id_}" class="k-card{group}" style="left:{box.x}px;top:{box.y}px;width:{box.w}px;'
                f'height:{box.h}px;background:{self.tone(fill)};{tilt}">{inner}</div>')

    def rule(self, id_: str, x: int, y: int, length: int, tone: str = "line", vertical: bool = False,
             thick: int | None = None) -> str:
        t = thick or self.s.stroke
        w, h = (t, length) if vertical else (length, t)
        return f'<div id="§{id_}" class="k-rule" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{self.tone(tone)}"></div>'

    def bar(self, id_: str, box: Box, fill: str = "accent", cls: str = "") -> str:
        group = f" §{cls}" if cls else ""
        self._rec(id_, box)
        return (f'<div id="§{id_}" class="k-bar{group}" style="left:{box.x}px;top:{box.y}px;width:{box.w}px;'
                f'height:{box.h}px;background:{self.tone(fill)}"></div>')

    def cells(self, prefix: str, x: int, y: int, cols: int, rows: int, size: int, gap: int, cls: str = "cell") -> str:
        """一片小方格，id 为 §{prefix}0、§{prefix}1……，都带类 §{cls}。"""
        out = []
        for i in range(cols * rows):
            cx, cy = x + (i % cols) * (size + gap), y + (i // cols) * (size + gap)
            out.append(f'<div id="§{prefix}{i}" class="k-cell §{cls}" style="left:{cx}px;top:{cy}px;width:{size}px;height:{size}px"></div>')
        self._rec(prefix, Box(x, y, cols * (size + gap) - gap, rows * (size + gap) - gap))
        return "".join(out)

    def icon(self, id_: str, name: str, x: int, y: int, size: int, tone: str = "ink") -> str:
        """线条图标，可用 draw("#§id path", t) 画出来。name：check cross arrow down plus play。"""
        weight = max(2.0, round(self.s.stroke * 24 / size * 1.6, 2))
        return (f'<svg id="§{id_}" class="k-icon" width="{size}" height="{size}" '
                f'viewBox="0 0 24 24" fill="none" stroke-width="{weight}" stroke-linecap="round" stroke-linejoin="round" '
                f'style="left:{x}px;top:{y}px;stroke:{self.tone(tone)}">{ICONS[name]}</svg>')

    def circle(self, id_: str, cx: int, cy: int, r: int, fill: str = "", line: str = "ink", inner: str = "") -> str:
        bg = self.tone(fill) if fill else "transparent"
        return (f'<div id="§{id_}" class="k-circle" style="left:{cx - r}px;top:{cy - r}px;width:{2 * r}px;height:{2 * r}px;'
                f'background:{bg};border-color:{self.tone(line)}">{inner}</div>')

    # ---- 每镜的状态 ----
    def begin(self, n: int, frame: dict | None = None) -> None:
        """开始写新的一镜：清空记录，按风格的规则选本镜的配色组合。"""
        self.boxes, self.issues = [], []
        looks, frame = self.s.looks, frame or {}
        pick = frame.get("look")
        if pick is None:
            pick = {"chapter": 1 if frame.get("chapter") else 0, "cycle": (n - 1) % max(1, len(looks) + 1)}.get(self.s.look_rule, 0)
        self.look = looks[pick - 1] if looks and 0 < pick <= len(looks) else Look()

    def ground_style(self) -> str:
        return f"background-color:{self.look.bg}" if self.look.bg else ""


    def chrome(self, n: int, total: int) -> str:
        c, kind = self.c, self.s.chrome
        if kind == "none":
            return ""
        page = f"{n:02d} / {total:02d}"
        y = c.head_y
        if kind == "boxed":
            px = self.px("label")
            right = c.w - c.margin - self.width(page, "label") - round(px * 1.7)
            return (f'<div class="k-a k-l k-tag" style="left:{c.margin}px;top:{y}px;font-size:{px}px">{self.title}</div>'
                    f'<div class="k-a k-l k-tag" style="left:{right}px;top:{y}px;font-size:{px}px">{page}</div>')
        px = self.px("label")
        head = (f'<div class="k-a k-l" style="left:{c.margin}px;top:{y}px;font-size:{px}px;color:var(--k-muted)">{self.title}</div>'
                f'<div class="k-a k-l" style="left:{c.margin}px;top:{y}px;width:{c.content.w}px;text-align:right;'
                f'font-size:{px}px;color:var(--k-muted)">{page}</div>')
        line_y = y + round(px * 1.6)
        if kind == "rules":
            head += f'<div class="k-rule" style="left:{c.margin}px;top:{line_y}px;width:{c.content.w}px;height:2px;background:var(--k-line)"></div>'
        if kind == "bar":
            done = round(c.content.w * n / total)
            head += (f'<div class="k-rule" style="left:{c.margin}px;top:{line_y}px;width:{c.content.w}px;height:4px;background:var(--k-line);opacity:0.25"></div>'
                     f'<div class="k-rule" style="left:{c.margin}px;top:{line_y}px;width:{done}px;height:4px;background:var(--k-accent)"></div>')
        return head

    # ---- 导出 ----
    def fonts(self) -> tuple[Font, ...]:
        seen: dict[str, Font] = {}
        s = self.s
        cap = {"display": s.display, "body": s.body, "label": s.tag_face}[s.cap_face]
        for face in (s.display, s.body, s.tag_face, Face(cap.latin, cap.cjk, s.cap_weight or cap.weight, fallback=cap.fallback)):
            for f in face.fonts():
                seen.setdefault(f.out, f)
        return tuple(seen.values())

    def caption(self) -> CaptionStyle:
        s = self.s
        face = {"display": s.display, "body": s.body, "label": s.tag_face}[s.cap_face]
        up, act, spoken = s.cap_colors
        ink = self.hex("ink")
        return CaptionStyle(
            family=face.stack, weight=nearest_weight(face.cjk, s.cap_weight or face.weight),
            upcoming=up or f"color-mix(in srgb, {ink} 52%, transparent)", active=act or self.hex("accent"),
            spoken=spoken or ink, plate=s.cap_plate, active_css=s.cap_active,
        )

    def css(self) -> str:
        s, c = self.s, self.c
        roles = "".join(
            f".{ROLE_CLASS[r]}{{font-family:{f.stack};font-weight:{f.weight};letter-spacing:{f.tracking}em;"
            f"line-height:{f.lh};{'text-transform:' + f.case + 'case;' if f.case else ''}}}"
            for r, f in (("display", s.display), ("body", s.body), ("label", s.tag_face)))
        em = {
            "block": f".k-em-bg{{inset:0;border-radius:{min(s.radius, 12)}px;}}",
            "pill": ".k-em-bg{inset:0;border-radius:9999px;}",
            "marker": ".k-em-bg{left:-0.08em;right:-0.08em;bottom:0.08em;height:0.42em;}",
            "underline": ".k-em-bg{left:0;right:0;bottom:-0.02em;height:0.09em;}",
            "outline": f".k-em-bg{{inset:0;background:none !important;border:{max(3, s.stroke)}px solid;}}",
        }[s.em]
        return f"""#root{{position:absolute;inset:0;width:{c.w}px;height:{c.h}px;overflow:hidden;color:var(--k-ink);font-family:{s.body.stack};font-synthesis:none;}}
.k-ground{{position:absolute;inset:0;background-color:{s.bg};{s.ground(c)}}}
.k-a{{position:absolute;white-space:nowrap;margin:0;font-synthesis:none;}}
{roles}
.k-tag{{box-sizing:border-box;line-height:1;border-radius:{s.radius if s.tag_radius < 0 else s.tag_radius}px;{s.tag}}}
.k-card{{position:absolute;box-sizing:border-box;border-radius:{s.radius}px;{s.card}}}
.k-rule,.k-bar,.k-cell,.k-icon,.k-circle{{position:absolute;}}
.k-bar{{box-sizing:border-box;border-radius:{min(s.radius, 10)}px;{s.bar}}}
.k-cell{{box-sizing:border-box;border:{max(2, s.stroke - 1)}px solid var(--k-ink);border-radius:{min(s.radius, 8)}px;background:transparent;}}
.k-circle{{box-sizing:border-box;border:{s.stroke}px solid;border-radius:50%;display:flex;align-items:center;justify-content:center;}}
.k-em{{line-height:1.3;}}
.k-em-bg{{position:absolute;display:block;}}
.k-em-t{{position:relative;display:block;}}
{em}
.k-num{{line-height:1;font-variant-numeric:tabular-nums;}}
.k-num span{{display:inline-block;line-height:1;}}
"""

    def theme(self) -> Theme:
        s, c = self.s, self.c
        return Theme(fonts=self.fonts(), css=self.css(), chrome=self.chrome, width=c.w, height=c.h,
                     ground_class="k-ground", ease=s.ease, entrance=s.entrance, bg=s.bg, caption=self.caption())
