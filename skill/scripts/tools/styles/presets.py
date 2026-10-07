"""HyperFrames 自带的 13 套预设，按各自 FRAME.md 的配色、字体和形状规则写成 Style。

西文字体照预设，中文字体是这里配的。每套的 looks 是它的第二种（或更多）配色，用在章节镜或逐镜轮换。
"""
from __future__ import annotations

from urllib.parse import quote

from stylekit import Face, Look, Style

SANS, SERIF = "Noto Sans SC", "Noto Serif SC"


def _grid(color: str, cell: int) -> str:
    return (f"background-image:linear-gradient({color} 1px,transparent 1px),linear-gradient(90deg,{color} 1px,transparent 1px);"
            f"background-size:{cell}px {cell}px;")


def _svg(body: str, size: int) -> str:
    return "url(\"data:image/svg+xml," + quote(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 100 100">{body}</svg>') + "\")"


DAISY = _svg("".join(
    f'<ellipse cx="50" cy="22" rx="11" ry="20" fill="#FFFFFF" stroke="#2D2D2D" stroke-width="3" transform="rotate({a} 50 50)"/>'
    for a in range(0, 360, 45)) + '<circle cx="50" cy="50" r="13" fill="#FDE68A" stroke="#2D2D2D" stroke-width="3"/>', 200)

COBALT_GRID = Style(
    name="cobalt-grid", label="钴蓝坐标纸", mood="米色坐标纸加钴蓝单色，细线，零圆角，冷静克制",
    fit="行业回顾、趋势梳理、给决策者看的解读",
    bg="#F0EBDE", ink="#1F2BE0", accent="#1F2BE0", muted="#3F4BDF", line="#1F2BE0", surface="#E6E0CE", on_accent="#F0EBDE",
    display=Face("Newsreader", SERIF, 400, -0.01, lh=1.1), body=Face("Hanken Grotesk", SANS, 400),
    tag_face=Face("DM Mono", SANS, 400, 0.06, "upper"),
    looks=(Look(bg="#1F2BE0", ink="#F0EBDE", accent="#F0EBDE", muted="#C9CCF5", line="#F0EBDE",
                surface="rgba(240,235,222,0.10)", on_accent="#1F2BE0"),),
    look_rule="chapter", stroke=2, card="border:2px solid var(--k-ink);", chrome="rules",
    ground=lambda c: _grid("rgba(31,43,224,0.10)", 40),
    cap_plate="background:#F0EBDE;border:2px solid #1F2BE0;padding:12px 34px 14px;",
    cap_active="background:#1F2BE0;box-shadow:0 0 0 0.08em #1F2BE0;",
    cap_colors=("rgba(31,43,224,0.62)", "#F0EBDE", "#1F2BE0"),
)

BLOCKFRAME = Style(
    name="blockframe", bar="border:6px solid var(--k-ink);", label="糖果粗框", mood="粗黑边框加硬投影，五色糖果色，逐镜换底色，活泼",
    fit="面向年轻人的科普、轻松话题、概念对比",
    bg="#FFFDF5", ink="#000000", accent="#F7CB46", accent2="#FE90E8", surface="#FFFFFF", on_accent="#000000",
    palette=("#FE90E8", "#C0F7FE", "#99E885", "#F7CB46", "#FFDC8B"),
    display=Face("Inter", SANS, 900, -0.02, lh=1.1), body=Face("Inter", SANS, 700),
    tag_face=Face("Space Grotesk", SANS, 600, 0.08, "upper"),
    looks=(Look(bg="#FE90E8"), Look(bg="#C0F7FE"), Look(bg="#99E885"), Look(bg="#F7CB46", accent="#FE90E8")),
    look_rule="cycle", stroke=6, card="border:8px solid var(--k-ink);box-shadow:14px 14px 0 var(--k-ink);",
    tag="border:5px solid var(--k-ink);box-shadow:6px 6px 0 var(--k-ink);background:#FFFFFF;padding:0.4em 0.9em;",
    tag_radius=9999, chrome="boxed", ease="back.out(1.5)", entrance="pop", tilt=2.0,
    ground=lambda c: "background-image:radial-gradient(#000 1.6px,transparent 1.8px);background-size:32px 32px;",
    cap_plate="background:#FFFFFF;border:5px solid #000;box-shadow:8px 8px 0 #000;padding:10px 30px 12px;",
    cap_active="background:#F7CB46;box-shadow:0 0 0 0.08em #F7CB46;",
    cap_colors=("rgba(0,0,0,0.52)", "#000000", "#000000"), bgm="pulse",
)

BLUE_PROFESSIONAL = Style(
    name="blue-professional", label="奶油钴蓝商务", mood="奶油底加一处钴蓝，圆角浅色卡片，稳重干净",
    fit="企业培训、产品说明、汇报口吻",
    bg="#FDFAE7", ink="#111111", accent="#1E2BFA", muted="#6B6B6B", line="rgba(30,43,250,0.22)",
    surface="rgba(30,43,250,0.05)", on_accent="#FDFAE7",
    display=Face("Space Grotesk", SANS, 700, -0.02, lh=1.12), body=Face("Inter", SANS, 400),
    tag_face=Face("Space Grotesk", SANS, 600, 0.04),
    radius=14, card="border:2px solid var(--k-line);",
    tag="border:2px solid var(--k-line);background:var(--k-surface);color:var(--k-accent);padding:0.4em 0.9em;",
    tag_radius=9999, chrome="bar",
    cap_plate="background:#FFFFFF;border:2px solid rgba(30,43,250,0.22);border-radius:14px;padding:12px 34px 14px;",
    cap_colors=("rgba(17,17,17,0.52)", "#1E2BFA", "#111111"),
)

BOLD_POSTER = Style(
    name="bold-poster", label="番茄红海报", mood="白底、番茄红、海报感粗字，红色左边条卡片",
    fit="活动预告、号召类、情绪强的开场",
    bg="#FFFFFF", ink="#1C1410", accent="#D8000F", surface="#F5F2EF", on_accent="#FFFFFF",
    display=Face("Shrikhand", SERIF, 900, lh=1.14), body=Face("Libre Baskerville", SERIF, 400),
    tag_face=Face("Space Grotesk", SANS, 600, 0.1, "upper"),
    looks=(Look(bg="#D8000F", ink="#FFFFFF", accent="#1C1410", surface="rgba(255,255,255,0.14)", line="#FFFFFF",
                muted="rgba(255,255,255,0.95)", on_accent="#FFFFFF"),),
    look_rule="chapter", stroke=4, card="border-left:10px solid var(--k-accent);",
    tag="border-bottom:3px solid var(--k-accent);padding:0.3em 0;", chrome="bar", ease="power4.out", entrance="slide",
    transitions=("push-slide UP", "crossfade", "crossfade"),
    cap_plate="background:#FFFFFF;border:3px solid #1C1410;padding:10px 30px 12px;",
    cap_colors=("rgba(28,20,16,0.52)", "#D8000F", "#1C1410"), cap_face="body", cap_weight=700,
)

BROADSIDE = Style(
    name="broadside", label="黑底火橙", mood="黑底加火橙，超大粗体字当图形用，章节镜整屏翻成橙色",
    fit="强观点、警示、反常识",
    bg="#111111", ink="#F0ECE5", accent="#E85D26", muted="#888880", line="#3A3A36", surface="#1A1A18", on_accent="#111111",
    display=Face("Barlow", SANS, 900, -0.03, "lower", lh=1.06), body=Face("Barlow", SANS, 400),
    tag_face=Face("IBM Plex Mono", SANS, 500, 0.14, "upper"),
    looks=(Look(bg="#E85D26", ink="#111111", accent="#111111", muted="rgba(17,17,17,0.90)", line="rgba(17,17,17,0.30)",
                surface="rgba(17,17,17,0.08)", on_accent="#E85D26"),),
    look_rule="chapter", scale=1.06, stroke=2, card="border-top:2px solid var(--k-line);", card_fill="transparent",
    tag="color:var(--k-accent);padding:0.3em 0;", ease="expo.out",
    transitions=("squeeze", "cut", "crossfade"),
    cap_plate="background:#111111;border:1px solid #E85D26;padding:14px 38px 16px;",
    cap_active="background:#E85D26;box-shadow:0 0 0 0.06em #E85D26;",
    cap_colors=("rgba(240,236,229,0.52)", "#111111", "#F0ECE5"),
)

CAPSULE = Style(
    name="capsule", bar="border:3px solid var(--k-ink);", label="胶囊糖果", mood="胶囊圆角、细描边、糖果九色、柔和投影，轻盈时髦",
    fit="生活方式、消费、入门向",
    bg="#F5F5F0", ink="#1A1A1A", accent="#E85D4E", accent2="#A06CE8", surface="#FFFFFF",
    palette=("#C4D94E", "#C5B5E0", "#8BB4F7", "#F2D160", "#F5B895", "#A8E6CF"),
    display=Face("Bodoni Moda", SERIF, 700, -0.01, lh=1.14), body=Face("Space Grotesk", SANS, 500),
    tag_face=Face("Space Grotesk", SANS, 600, 0.08, "upper"),
    radius=36, tag_radius=9999, card="border:3px solid var(--k-ink);box-shadow:8px 8px 0 rgba(26,26,26,0.10);",
    tag="border:2px solid var(--k-ink);background:#F2D160;padding:0.42em 1em;", em="pill", chrome="boxed", align="center",
    ease="back.out(1.3)", entrance="pop",
    ground=lambda c: ("background-image:radial-gradient(circle at 14% 18%,rgba(197,181,224,0.55),transparent 38%),"
                      "radial-gradient(circle at 88% 70%,rgba(168,230,207,0.55),transparent 40%);"),
    cap_plate=("background:#FFFFFF;border:2px solid #1A1A1A;border-radius:9999px;box-shadow:6px 6px 0 rgba(26,26,26,0.08);"
               "padding:10px 40px 12px;"),
    cap_colors=("rgba(26,26,26,0.52)", "#E85D4E", "#1A1A1A"), cap_face="body", cap_weight=700, bgm="warm",
)

CARTESIAN = Style(
    name="cartesian", label="暖灰细线", mood="暖灰石色，极细线和几何圆环，无投影无填充，极克制",
    fit="方法论、思考框架、哲理类",
    bg="#EDE8E0", ink="#1A1A1A", accent="#8A8178", muted="#5A5A5A", line="#B8B0A4", surface="rgba(255,255,255,0.30)",
    display=Face("Playfair Display", SERIF, 400, lh=1.14), body=Face("Inter", SANS, 400),
    tag_face=Face("Inter", SANS, 500, 0.14, "upper"),
    stroke=2, card="border:1px solid var(--k-line);", tag="border-bottom:1px solid var(--k-line);padding:0.3em 0;color:var(--k-muted);",
    em="underline", ease="power2.out", entrance="fade", transitions=("crossfade", "crossfade", "blur-crossfade"),
    ground=lambda c: (f"background-image:radial-gradient(circle at {c.w - c.margin}px {c.content.cy}px,transparent 0,"
                      f"transparent {c.w * 0.16:.0f}px,#B8B0A4 {c.w * 0.16 + 1:.0f}px,transparent {c.w * 0.16 + 2.5:.0f}px,"
                      f"transparent {c.w * 0.24:.0f}px,rgba(184,176,164,0.6) {c.w * 0.24 + 1:.0f}px,transparent {c.w * 0.24 + 2.5:.0f}px);"),
    cap_active="box-shadow:0 0.12em 0 #8A8178;", cap_colors=("rgba(26,26,26,0.52)", "#1A1A1A", "#5A5A5A"),
    cap_face="body", cap_weight=500,
)

CODE_EDITORIAL = Style(
    name="code-editorial", label="奶油赤陶代码", mood="奶油纸加一点赤陶色，衬线标题配等宽标签，章节镜翻成深色代码底",
    fit="技术原理、工具教程、开发者向",
    bg="#FAF9F5", ink="#141413", accent="#CC785C", surface="#EFE9DE", line="rgba(20,20,19,0.20)",
    display=Face("EB Garamond", SERIF, 500, -0.01, lh=1.12), body=Face("Inter", SANS, 400),
    tag_face=Face("JetBrains Mono", SANS, 500, 0.02),
    looks=(Look(bg="#181715", ink="#FAF9F5", accent="#CC785C", surface="#252320", line="rgba(250,249,245,0.22)",
                muted="rgba(250,249,245,0.66)", on_accent="#181715"),),
    look_rule="chapter", radius=10, tag_radius=6, card="border:1px solid var(--k-line);",
    tag="border:1px solid var(--k-line);background:var(--k-surface);padding:0.42em 0.8em;", em="marker",
    cap_plate="background:#181715;border-radius:8px;padding:12px 34px 14px;",
    cap_colors=("rgba(250,249,245,0.52)", "#CC785C", "#FAF9F5"), cap_face="body", cap_weight=500,
)

CORAL = Style(
    name="coral", label="珊瑚硬切", mood="珊瑚红、黑、奶油三色硬切，窄体大字，斜线纹，节奏快",
    fit="快节奏盘点、新闻速读",
    bg="#F5F0E8", ink="#1A1A1A", accent="#E85D5D", muted="#5E5E5E", surface="#E8E0D4",
    display=Face("Bebas Neue", "ZCOOL QingKe HuangYou", 400, 0.02, "upper", lh=1.1), body=Face("Inter", SANS, 600),
    tag_face=Face("Inter", SANS, 700, 0.12, "upper"),
    looks=(Look(bg="#E85D5D", ink="#1A1A1A", accent="#1A1A1A", surface="rgba(255,255,255,0.22)", line="#1A1A1A",
                muted="rgba(26,26,26,0.94)", on_accent="#F5F0E8"),),
    look_rule="chapter", scale=1.08, stroke=4, card="border:0;", tag="background:var(--k-ink);color:var(--k-bg);padding:0.4em 0.8em;",
    ease="power4.out", entrance="slide", transitions=("push-slide UP", "cut", "crossfade"),
    ground=lambda c: (f"background-image:repeating-linear-gradient(45deg,rgba(0,0,0,0.10) 0 3px,transparent 3px 16px),"
                      f"linear-gradient(#E85D5D,#E85D5D);background-size:100% {max(24, c.head_y - 20)}px;background-repeat:no-repeat;"),
    cap_plate="background:#1A1A1A;padding:12px 34px 14px;", cap_colors=("rgba(245,240,232,0.52)", "#E85D5D", "#F5F0E8"),
    cap_face="body", cap_weight=700, bgm="pulse",
)

CREATIVE_MODE = Style(
    name="creative-mode", bar="border:5px solid var(--k-ink);", label="奶油粗框四色", mood="奶油底、粗黑框、硬投影，绿粉橙黄四色点缀，手作感",
    fit="创意方法、头脑风暴、工具推荐",
    bg="#EFE9D9", ink="#0F0F0F", accent="#F06CA8", accent2="#2FA862", surface="#FBF7EA", on_accent="#0F0F0F",
    palette=("#F5C518", "#F06CA8", "#2FA862", "#E85A1F"),
    display=Face("Archivo Black", SANS, 900, -0.01, "upper", lh=1.08), body=Face("Space Grotesk", SANS, 500),
    tag_face=Face("JetBrains Mono", SANS, 500, 0.08, "upper"),
    stroke=5, card="border:5px solid var(--k-ink);box-shadow:10px 10px 0 var(--k-ink);",
    tag="border:3px solid var(--k-ink);background:#F5C518;padding:0.4em 0.8em;", ease="back.out(1.2)", entrance="drop", tilt=1.5,
    cap_plate="background:#0F0F0F;padding:10px 30px 12px;", cap_colors=("rgba(239,233,217,0.52)", "#F5C518", "#EFE9D9"),
    cap_face="body", cap_weight=700, bgm="pulse",
)

DAISY_DAYS = Style(
    name="daisy-days", bar="border:3px solid var(--k-ink);", label="花园粉彩", mood="花园系粉彩、圆润字体、炭色描边，角上有小雏菊，逐镜换底色",
    fit="亲子、情感、轻松日常",
    bg="#F5F0E6", ink="#2D2D2D", accent="#F8635F", surface="#FFFFFF", muted="#454545",
    palette=("#7ECDC0", "#F7C8D4", "#FDE68A", "#A8E6CF", "#D4A5E8", "#FFCBA4", "#A8D8F0"),
    display=Face("Fredoka", "ZCOOL KuaiLe", 600, lh=1.2), body=Face("Quicksand", SANS, 600),
    tag_face=Face("Quicksand", SANS, 600, 0.04),
    looks=(Look(bg="#7ECDC0"), Look(bg="#FDE68A"), Look(bg="#F7C8D4"), Look(bg="#A8D8F0")),
    look_rule="cycle", radius=28, tag_radius=9999, stroke=4,
    card="border:3px solid var(--k-ink);box-shadow:6px 6px 0 var(--k-ink);",
    tag="border:3px solid var(--k-ink);background:#FDE68A;box-shadow:4px 4px 0 var(--k-ink);padding:0.42em 1em;",
    em="pill", chrome="boxed", align="center", ease="back.out(1.8)", entrance="pop",
    ground=lambda c: (f"background-image:{DAISY},{DAISY};background-repeat:no-repeat;"
                      f"background-position:-70px -70px,{c.w - 150}px {c.bottom - 150}px;background-size:200px 200px,220px 220px;"),
    cap_plate=("background:#FFFFFF;border:3px solid #2D2D2D;border-radius:9999px;box-shadow:5px 5px 0 #2D2D2D;"
               "padding:10px 40px 12px;"),
    cap_colors=("rgba(45,45,45,0.52)", "#F8635F", "#2D2D2D"), cap_face="body", cap_weight=700, bgm="warm",
)

EDITORIAL_FOREST = Style(
    name="editorial-forest", label="墨绿编辑部", mood="墨绿、粉、奶油三色，衬线大标题，章节镜翻成奶油底",
    fit="人物、品牌故事、读书笔记",
    bg="#2E4A2A", ink="#EFE7D4", accent="#E89CB1", muted="rgba(239,231,212,0.72)", line="rgba(239,231,212,0.36)",
    surface="#3A5A36", on_accent="#243A21",
    display=Face("Source Serif 4", SERIF, 500, -0.01, lh=1.12), body=Face("Source Serif 4", SERIF, 400),
    tag_face=Face("JetBrains Mono", SANS, 500, 0.1, "upper"),
    looks=(Look(bg="#EFE7D4", ink="#2E4A2A", accent="#2E4A2A", accent2="#D27E96", surface="#E6DCC4",
                line="rgba(46,74,42,0.36)", muted="rgba(46,74,42,0.88)", on_accent="#EFE7D4"),),
    look_rule="chapter", radius=8, tag_radius=6, stroke=2, card="border:2px solid var(--k-line);",
    tag="border:2px solid var(--k-line);padding:0.4em 0.8em;", chrome="rules",
    cap_plate="background:#243A21;border:2px solid rgba(239,231,212,0.36);border-radius:8px;padding:12px 34px 14px;",
    cap_colors=("rgba(239,231,212,0.52)", "#E89CB1", "#EFE7D4"),
)

BIENNALE_YELLOW = Style(
    name="biennale-yellow", label="羊皮纸日光黄", mood="羊皮纸底、靛蓝字、一团日光黄的光晕，细线，文气",
    fit="文化、设计、观点评论",
    bg="#E9E5DB", ink="#1B2566", accent="#F1EE2E", accent2="#E26B4A", surface="#DCD6C4", line="#1B2566", on_accent="#1B2566",
    muted="color-mix(in srgb, #1B2566 78%, #E9E5DB)",
    display=Face("Instrument Serif", SERIF, 400, -0.01, lh=1.12), body=Face("Archivo", SANS, 400),
    tag_face=Face("JetBrains Mono", SANS, 400, 0.1, "upper"),
    stroke=2, card="border:1px solid var(--k-line);", tag="border-top:1px solid var(--k-ink);padding:0.5em 0 0;",
    em="marker", ease="power2.out",
    ground=lambda c: (f"background-image:radial-gradient(circle at {c.w * 0.3:.0f}px {c.content.cy}px,rgba(241,238,46,0.85) 0,"
                      f"rgba(241,238,46,0.38) {c.w * 0.12:.0f}px,transparent {c.w * 0.26:.0f}px),"
                      f"radial-gradient(circle at {c.w * 0.92:.0f}px {c.bottom}px,rgba(226,107,74,0.22),transparent {c.w * 0.18:.0f}px);"),
    cap_plate="background:rgba(233,229,219,0.94);border:1px solid #1B2566;padding:12px 34px 14px;",
    cap_active="background:#F1EE2E;box-shadow:0 0 0 0.08em #F1EE2E;",
    cap_colors=("rgba(27,37,102,0.52)", "#1B2566", "#1B2566"),
)

PRESETS = (COBALT_GRID, BLUE_PROFESSIONAL, CARTESIAN, EDITORIAL_FOREST, CODE_EDITORIAL, BIENNALE_YELLOW, BROADSIDE,
           CORAL, BOLD_POSTER, BLOCKFRAME, CREATIVE_MODE, CAPSULE, DAISY_DAYS)
