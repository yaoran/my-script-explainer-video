"""《生成式 AI 这一波》的视觉设定：cobalt-grid 预设（米色纸底 + 钴蓝单色、坐标纸网格、零圆角）。

这是 tools/theme.py 的一个完整样例。换一条片子时照这个结构写：设计令牌 → 字体 → 公共样式 →
HTML 小积木 → 版面家具 chrome() → THEME。年份导轨 rail() 和章节栏 chapter_column() 是这条
“按年份讲”的片子专用的，别的片子按自己的主线另写。
"""
from __future__ import annotations

from fontlib import font
from framekit import CaptionStyle, Theme

W, H = 1920, 1080
INK = "#1F2BE0"
INK_SOFT = "#5560E5"
PAPER = "#F0EBDE"
VEIL = "rgba(240,235,222,0.88)"
FAINT = "rgba(31,43,224,0.18)"

RAIL_X0 = 1040
RAIL_W = 784
RAIL_YEAR0_X = 1060
RAIL_STEP = 200
YEARS = (2023, 2024, 2025, 2026)

SERIF = '"Newsreader","Noto Serif SC",serif'
SANS = '"Hanken Grotesk","Noto Sans SC",sans-serif'
MONO = '"DM Mono","Noto Sans SC",monospace'

FONTS = (
    font("Newsreader", 400), font("Newsreader", 700), font("Noto Serif SC", 400), font("Noto Serif SC", 700),
    font("Hanken Grotesk", 400), font("Hanken Grotesk", 600), font("Noto Sans SC", 400), font("Noto Sans SC", 700),
    font("DM Mono", 400),
)

CSS = f"""#root{{position:absolute;inset:0;width:{W}px;height:{H}px;overflow:hidden;color:{INK};font-family:{SANS};}}
.gw-ground{{position:absolute;inset:0;background-color:{PAPER};
  background-image:linear-gradient(rgba(31,43,224,0.10) 1px,transparent 1px),linear-gradient(90deg,rgba(31,43,224,0.10) 1px,transparent 1px);
  background-size:38.4px 38.4px;}}
.gw-a{{position:absolute;white-space:nowrap;}}
.gw-ink{{position:absolute;background:{INK};}}
.gw-box{{position:absolute;border:2px solid {INK};background:{VEIL};}}
.gw-brand{{font-family:{SANS};font-weight:700;font-size:26px;letter-spacing:0.14em;line-height:1;}}
.gw-brand span{{font-family:{MONO};font-weight:400;letter-spacing:0.06em;margin-left:22px;opacity:0.7;}}
.gw-page{{font-family:{MONO};font-size:22px;letter-spacing:0.08em;line-height:1;opacity:0.6;text-align:right;}}
.gw-yl{{font-family:{MONO};font-size:24px;letter-spacing:0.06em;line-height:1;width:84px;padding:6px 0;text-align:center;}}
.gw-yl.on{{background:{INK};color:{PAPER};}}
.gw-tag{{position:absolute;white-space:nowrap;font-family:{MONO};font-size:28px;letter-spacing:0.06em;line-height:1;padding:10px 16px;background:{INK};color:{PAPER};}}
.gw-chip{{position:absolute;white-space:nowrap;font-family:{SERIF};font-weight:400;font-size:56px;line-height:1.1;padding:12px 28px;border:2px solid {INK};background:{VEIL};}}
.gw-serif{{font-family:{SERIF};font-weight:400;}}
.gw-d0{{font-family:{SERIF};font-weight:400;font-size:380px;line-height:0.9;letter-spacing:-0.02em;}}
.gw-d1{{font-family:{SERIF};font-weight:400;font-size:280px;line-height:0.9;letter-spacing:-0.015em;}}
.gw-d2{{font-family:{SERIF};font-weight:400;font-size:240px;line-height:0.95;letter-spacing:-0.012em;}}
.gw-d3{{font-family:{SERIF};font-weight:400;font-size:170px;line-height:0.9;letter-spacing:-0.01em;}}
.gw-d4{{font-family:{SERIF};font-weight:400;font-size:130px;line-height:0.9;letter-spacing:-0.01em;}}
.gw-hero{{font-family:{SERIF};font-weight:400;font-size:196px;line-height:1.1;}}
.gw-h0{{font-family:{SERIF};font-weight:400;font-size:170px;line-height:1.1;}}
.gw-h1b{{font-family:{SERIF};font-weight:400;font-size:150px;line-height:1.05;}}
.gw-h1{{font-family:{SERIF};font-weight:400;font-size:130px;line-height:1.05;}}
.gw-h2{{font-family:{SERIF};font-weight:400;font-size:110px;line-height:1.05;}}
.gw-h3{{font-family:{SERIF};font-weight:400;font-size:84px;line-height:1.1;}}
.gw-h4{{font-family:{SERIF};font-weight:400;font-size:64px;line-height:1.1;}}
.gw-h5{{font-family:{SERIF};font-weight:400;font-size:52px;line-height:1.1;}}
.gw-soft{{color:{INK_SOFT};}}
.gw-lab{{font-family:{SANS};font-weight:700;font-size:30px;letter-spacing:0.22em;line-height:1;}}
.gw-sm{{font-family:{SANS};font-weight:400;font-size:38px;line-height:1.1;}}
.gw-mono2{{font-family:{MONO};font-size:30px;letter-spacing:0.06em;line-height:1;}}
.gw-blk{{position:absolute;white-space:nowrap;color:{PAPER};font-family:{SERIF};font-weight:700;line-height:1.15;padding:0.08em 0.22em;}}
.gw-blk i{{position:absolute;inset:0;background:{INK};}}
.gw-blk b{{position:relative;font-weight:inherit;}}
.gw-kw{{font-size:150px;}}
.gw-kwb{{font-size:170px;}}
.gw-kwb2{{font-size:140px;}}
.gw-kwm{{font-size:96px;}}
.gw-kw2{{font-size:54px;}}
.gw-kw3{{font-size:40px;}}
.gw-node{{position:absolute;box-sizing:border-box;white-space:nowrap;display:flex;align-items:center;justify-content:center;border:2px solid {INK};background:{VEIL};font-family:{SERIF};font-weight:400;font-size:52px;line-height:1;}}
.gw-node.solid{{background:{INK};color:{PAPER};font-weight:700;}}
.gw-node.left{{justify-content:flex-start;padding-left:32px;}}
.gw-cells{{position:absolute;display:grid;}}
.gw-cells i{{display:block;background:{INK};}}
.gw-stack{{position:absolute;background:repeating-linear-gradient(0deg,{INK} 0 11px,transparent 11px 14px);}}
svg.gw-a{{overflow:visible;}}
"""


def rail_x(year_frac: float) -> float:
    return RAIL_YEAR0_X + (year_frac - YEARS[0]) * RAIL_STEP


def txt(id_: str, cls: str, text: str, x: int, y: int, extra: str = "") -> str:
    return f'<div id="§{id_}" class="gw-a {cls}" style="left:{x}px;top:{y}px;{extra}">{text}</div>'


def tag(id_: str, text: str, x: int, y: int) -> str:
    return f'<div id="§{id_}" class="gw-tag" style="left:{x}px;top:{y}px">{text}</div>'


def chip(id_: str, text: str, x: int, y: int) -> str:
    return f'<div id="§{id_}" class="gw-chip" style="left:{x}px;top:{y}px">{text}</div>'


def block(id_: str, cls: str, text: str, x: int, y: int) -> str:
    return (f'<div id="§{id_}" class="gw-blk {cls}" style="left:{x}px;top:{y}px">'
            f'<i id="§{id_}-bg"></i><b id="§{id_}-t">{text}</b></div>')


def box(id_: str, x: int, y: int, w: int, h: int, inner: str = "", extra: str = "") -> str:
    return (f'<div id="§{id_}" class="gw-box" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;{extra}">'
            f"{inner}</div>")


def ink(id_: str, x: int, y: int, w: int, h: int, cls: str = "", extra: str = "") -> str:
    ident = f'id="§{id_}" ' if id_ else ""
    return f'<div {ident}class="gw-ink {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;{extra}"></div>'


def node(id_: str, text: str, x: int, y: int, w: int, h: int, cls: str = "", extra: str = "") -> str:
    return (f'<div id="§{id_}" class="gw-node {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;{extra}">'
            f"{text}</div>")


def cells(id_: str, x: int, y: int, cols: int, rows: int, size: int, gap: int, cell_cls: str) -> str:
    items = "".join(f'<i class="§{cell_cls}"></i>' for _ in range(cols * rows))
    return (f'<div id="§{id_}" class="gw-cells" style="left:{x}px;top:{y}px;'
            f'grid-template-columns:repeat({cols},{size}px);grid-auto-rows:{size}px;gap:{gap}px">{items}</div>')


def arrow_h(id_: str, x: int, y: int, w: int) -> str:
    """横向箭头：线 §id + 箭头 §id-h。"""
    head = (f'<svg id="§{id_}-h" class="gw-a" style="left:{x + w - 2}px;top:{y - 13}px" width="26" height="30" '
            f'viewBox="0 0 26 30"><path d="M0 0 L26 15 L0 30 Z" fill="{INK}"/></svg>')
    return ink(id_, x, y, w, 4) + head


def arrow_v(id_: str, x: int, y: int, h: int) -> str:
    """纵向箭头：线 §id + 箭头 §id-h。"""
    head = (f'<svg id="§{id_}-h" class="gw-a" style="left:{x - 13}px;top:{y + h - 2}px" width="30" height="26" '
            f'viewBox="0 0 30 26"><path d="M0 0 L30 0 L15 26 Z" fill="{INK}"/></svg>')
    return ink(id_, x, y, 4, h) + head


def check(id_: str, x: int, y: int, size: int = 44) -> str:
    """方形勾选框：框恒在，勾 §id 是可描边的路径。"""
    return (f'<svg class="gw-a" style="left:{x}px;top:{y}px" width="{size}" height="{size}" viewBox="0 0 44 44">'
            f'<rect x="2" y="2" width="40" height="40" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>'
            f'<path id="§{id_}" d="M10 23 L19 32 L35 12" fill="none" stroke="{INK}" stroke-width="5" '
            f'pathLength="1" stroke-dasharray="1"/></svg>')


def chrome(n: int, total: int) -> str:
    """每帧都有的版面家具：上下细线、左上片名、右下页码。"""
    return (
        ink("", 96, 124, 1728, 2) + ink("", 96, 884, 1728, 2)
        + '<div class="gw-a gw-brand" style="left:96px;top:60px">生成式 AI 这一波<span>2023 → 2026.10</span></div>'
        + f'<div class="gw-a gw-page" style="left:1624px;top:856px;width:200px">{n:02d} / {total}</div>'
    )


def rail(prev: float, cur: float) -> tuple[str, str]:
    """右上角的年份导轨：游标从上一帧的位置滑到这一帧的位置。返回 (html, js)。"""
    active = int(cur)
    parts = [ink("", RAIL_X0, 97, RAIL_W, 2, extra="opacity:0.25"), ink("rf", RAIL_X0, 96, RAIL_W, 4)]
    for year in YEARS:
        x = rail_x(year)
        parts.append(ink("", int(x) - 1, 88, 2, 20))
        on = " on" if year == active else ""
        parts.append(f'<div class="gw-a gw-yl{on}" style="left:{int(x) - 42}px;top:48px">{year}</div>')
    parts.append(ink("rm", RAIL_X0 - 8, 89, 16, 18))
    p0, p1 = rail_x(prev) - RAIL_X0, rail_x(cur) - RAIL_X0
    js = (
        f'tl.fromTo("#§rf", {{ scaleX: {p0 / RAIL_W:.4f} }}, {{ scaleX: {p1 / RAIL_W:.4f}, duration: 0.9, '
        f'ease: "power3.inOut", transformOrigin: "left center" }}, 0.1);\n'
        f'tl.fromTo("#§rm", {{ x: {p0:.1f} }}, {{ x: {p1:.1f}, duration: 0.9, ease: "power3.inOut" }}, 0.1);\n'
    )
    return "".join(parts), js


def chapter_column(index: int, year: int, keywords_html: str) -> str:
    """章节帧左栏：章节序号、大年份、“关键词”小标，关键词色块由调用方给。"""
    return (
        txt("ch", "gw-mono2", f"CHAPTER {index:02d} / 04", 100, 168)
        + txt("yr", "gw-d1", str(year), 90, 236)
        + txt("kwl", "gw-lab", "关键词", 100, 508)
        + keywords_html
    )


CAPTION = CaptionStyle(
    family=SERIF, weight=400, upcoming="color-mix(in srgb, #1F2BE0 42%, #F0EBDE)", active=PAPER, spoken=INK,
    plate=f"background:{PAPER};border-top:2px solid {INK};border-bottom:2px solid {INK};padding:16px 44px 20px;",
    active_css=f"background:{INK};box-shadow:0 0 0 0.06em {INK};",
)
THEME = Theme(fonts=FONTS, css=CSS, chrome=chrome, width=W, height=H, ground_class="gw-ground", ease="power3.out",
              bg=PAPER, caption=CAPTION)
