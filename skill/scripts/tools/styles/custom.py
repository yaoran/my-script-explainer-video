"""自己设计的风格，补预设里没有的气质：国风、深色科技、报纸、黑板、渐变玻璃、黑金、手账、蓝图。

新增风格：照下面任意一个写一个 Style，加进 CUSTOM，再跑 gallery.py 看它在横屏和竖屏下的样子。
"""
from __future__ import annotations

from stylekit import Face, Style

SANS, SERIF, KAI = "Noto Sans SC", "Noto Serif SC", "LXGW WenKai TC"


def _grid(color: str) -> str:
    """横竖两组 1px 细线，配合 background-size 就是一张网格。"""
    return f"linear-gradient({color} 1px,transparent 1px),linear-gradient(90deg,{color} 1px,transparent 1px)"


INK_WASH = Style(
    name="ink-wash", label="水墨国风", mood="宣纸底、墨色毛笔字、一方朱红印，角上有晕开的墨，沉静",
    fit="传统文化、历史人物、节气、诗词、有东方气质的品牌",
    bg="#F3EEE2", ink="#1C1B19", accent="#B3261E", muted="#6E6A60", line="#1C1B19", surface="rgba(28,27,25,0.05)",
    on_accent="#F3EEE2",
    display=Face("Ma Shan Zheng", "Ma Shan Zheng", 400, 0.02, lh=1.2, fallback=SERIF), body=Face("EB Garamond", SERIF, 500),
    tag_face=Face("EB Garamond", SERIF, 600, 0.2),
    stroke=3, card="border-left:6px solid var(--k-ink);", tag="border:2px solid var(--k-accent);color:var(--k-accent);padding:0.36em 0.7em;",
    align="center", ease="power2.out", entrance="fade", transitions=("blur-crossfade", "crossfade", "blur-crossfade"),
    ground=lambda c: (f"background-image:radial-gradient(ellipse at {c.w * 0.9:.0f}px {c.h * 0.08:.0f}px,rgba(28,27,25,0.20),transparent {c.w * 0.34:.0f}px),"
                      f"radial-gradient(ellipse at {c.w * 0.04:.0f}px {c.bottom}px,rgba(28,27,25,0.14),transparent {c.w * 0.3:.0f}px),"
                      "repeating-linear-gradient(90deg,rgba(28,27,25,0.018) 0 2px,transparent 2px 7px);"),
    cap_colors=("rgba(28,27,25,0.52)", "#B3261E", "#1C1B19"), cap_face="body", cap_weight=700, bgm="zen", origin="custom",
)

NEON_NIGHT = Style(
    name="neon-night", label="霓虹夜色", mood="深蓝夜色底，青色和品红的霓虹描边与光晕，细网格，科技感",
    fit="AI 和科技新品、互联网趋势、游戏、数码评测",
    bg="#0B0E1A", ink="#E8ECFF", accent="#00E5FF", accent2="#FF3D9A", muted="#8A93B8", line="rgba(0,229,255,0.38)",
    surface="rgba(255,255,255,0.05)", on_accent="#0B0E1A",
    display=Face("Space Grotesk", SANS, 700, -0.01, lh=1.12), body=Face("Inter", SANS, 400),
    tag_face=Face("JetBrains Mono", SANS, 500, 0.12, "upper"),
    radius=16, tag_radius=9999, card="border:2px solid var(--k-line);box-shadow:0 0 40px rgba(0,229,255,0.18),inset 0 0 30px rgba(0,229,255,0.06);",
    tag="border:2px solid var(--k-accent);color:var(--k-accent);padding:0.4em 0.9em;", em="outline", chrome="bar",
    ease="expo.out", transitions=("zoom-through", "crossfade", "blur-crossfade"),
    ground=lambda c: (f"background-image:radial-gradient(circle at {c.w * 0.82:.0f}px {c.h * 0.08:.0f}px,rgba(255,61,154,0.24),transparent {c.w * 0.42:.0f}px),"
                      f"radial-gradient(circle at {c.w * 0.08:.0f}px {c.h * 0.9:.0f}px,rgba(0,229,255,0.20),transparent {c.w * 0.42:.0f}px),"
                      f"{_grid('rgba(255,255,255,0.045)')};background-size:auto,auto,48px 48px,48px 48px;"),
    cap_plate=("background:rgba(11,14,26,0.88);border:2px solid rgba(0,229,255,0.5);border-radius:14px;"
               "box-shadow:0 0 30px rgba(0,229,255,0.25);padding:12px 34px 14px;"),
    cap_colors=("rgba(232,236,255,0.52)", "#00E5FF", "#E8ECFF"), bgm="pulse", origin="custom",
)

NEWSPRINT = Style(
    name="newsprint", label="报纸头版", mood="新闻纸底、黑色粗衬线大标题、一处报头红，上粗下细的栏线",
    fit="时事解读、财经评论、事件复盘、深度报道口吻",
    bg="#F4F1EA", ink="#111111", accent="#C8102E", muted="#555555", line="#111111", surface="#EAE5DA", on_accent="#F4F1EA",
    display=Face("Playfair Display", SERIF, 900, -0.01, lh=1.12), body=Face("Libre Baskerville", SERIF, 400),
    tag_face=Face("Oswald", SANS, 500, 0.14, "upper"),
    card="border-top:6px solid var(--k-ink);border-bottom:2px solid var(--k-ink);", card_fill="transparent",
    tag="background:var(--k-ink);color:var(--k-bg);padding:0.36em 0.8em;", chrome="rules",
    transitions=("push-slide UP", "crossfade", "crossfade"),
    ground=lambda c: "background-image:repeating-linear-gradient(0deg,rgba(17,17,17,0.035) 0 1px,transparent 1px 6px);",
    cap_plate="background:#111111;padding:10px 32px 12px;", cap_active="background:#C8102E;box-shadow:0 0 0 0.08em #C8102E;",
    cap_colors=("rgba(244,241,234,0.52)", "#F4F1EA", "#F4F1EA"), cap_face="body", cap_weight=700, origin="custom",
)

CHALKBOARD = Style(
    name="chalkboard", label="黑板粉笔", mood="墨绿黑板、楷体粉笔字、黄色粉笔做重点，虚线框，像课堂板书",
    fit="知识讲解、学习方法、考试和课程、给学生看的科普",
    bg="#24382F", ink="#F4F1E8", accent="#FFD866", accent2="#FF9AA2", muted="rgba(244,241,232,0.72)",
    line="rgba(244,241,232,0.55)", surface="rgba(244,241,232,0.06)", on_accent="#24382F",
    display=Face("Caveat", KAI, 700, lh=1.2), body=Face("Quicksand", KAI, 700), tag_face=Face("Quicksand", SANS, 600, 0.08),
    radius=18, stroke=4, card="border:3px dashed var(--k-line);",
    tag="border:2px solid var(--k-accent);color:var(--k-accent);padding:0.4em 0.9em;", em="underline", ease="power2.out",
    ground=lambda c: ("background-image:radial-gradient(ellipse at 50% 38%,rgba(255,255,255,0.07),transparent 62%),"
                      "linear-gradient(0deg,rgba(0,0,0,0.20),transparent 32%);"),
    cap_plate="background:rgba(18,28,23,0.82);border-radius:14px;padding:10px 32px 12px;",
    cap_colors=("rgba(244,241,232,0.52)", "#FFD866", "#F4F1E8"), cap_face="body", bgm="warm", origin="custom",
)

AURORA_GLASS = Style(
    name="aurora-glass", label="极光玻璃", mood="紫蓝粉渐变底、半透明玻璃卡片、白字加一点亮黄，现代产品感",
    fit="产品发布、功能介绍、App 和 SaaS、面向大众的新事物",
    bg="#2A1A78", ink="#FFFFFF", accent="#FDE047", accent2="#5EEAD4", muted="rgba(255,255,255,0.78)",
    line="rgba(255,255,255,0.42)", surface="rgba(255,255,255,0.13)", on_accent="#1B1140",
    display=Face("Inter", SANS, 800, -0.02, lh=1.12), body=Face("Inter", SANS, 500), tag_face=Face("Inter", SANS, 600, 0.1, "upper"),
    radius=32, tag_radius=9999, card="border:2px solid rgba(255,255,255,0.36);box-shadow:0 24px 60px rgba(0,0,0,0.25);",
    tag="background:rgba(255,255,255,0.16);border:2px solid rgba(255,255,255,0.42);padding:0.42em 1em;", em="pill", chrome="bar",
    transitions=("blur-crossfade", "crossfade", "blur-crossfade"),
    ground=lambda c: "background-image:linear-gradient(135deg,#3B1C8C 0%,#1D4ED8 48%,#DB2777 100%);",
    cap_plate=("background:rgba(15,10,40,0.58);border:2px solid rgba(255,255,255,0.36);border-radius:9999px;"
               "padding:10px 40px 12px;"),
    cap_colors=("rgba(255,255,255,0.52)", "#FDE047", "#FFFFFF"), cap_face="body", cap_weight=700, bgm="pulse", origin="custom",
)

BLACK_GOLD = Style(
    name="black-gold", label="黑金", mood="纯黑底、细衬线、香槟金细线和强调，大量留白，贵气",
    fit="高端品牌、年度盘点、颁奖和榜单、金融和奢侈品",
    bg="#0E0E0E", ink="#F2EDE4", accent="#C9A45C", muted="#9A948A", line="rgba(201,164,92,0.55)", surface="#171614",
    on_accent="#0E0E0E",
    display=Face("Cormorant Garamond", SERIF, 600, 0.01, lh=1.16), body=Face("Cormorant Garamond", SERIF, 500),
    tag_face=Face("Inter", SANS, 500, 0.24, "upper"),
    stroke=2, card="border:1px solid var(--k-line);",
    tag="border-top:1px solid var(--k-accent);border-bottom:1px solid var(--k-accent);color:var(--k-accent);padding:0.5em 0.2em;",
    em="underline", align="center", ease="power2.out", entrance="fade",
    transitions=("blur-crossfade", "crossfade", "blur-crossfade"),
    ground=lambda c: f"background-image:radial-gradient(ellipse at 50% 0%,rgba(201,164,92,0.16),transparent {c.h * 0.6:.0f}px);",
    cap_colors=("rgba(242,237,228,0.52)", "#C9A45C", "#F2EDE4"), cap_face="body", cap_weight=600, origin="custom",
)

KRAFT_NOTES = Style(
    name="kraft-notes", label="牛皮纸手账", mood="牛皮纸底、贴上去的便签纸、楷体手写感、红笔圈重点，微微歪斜",
    fit="个人经验分享、读书笔记、清单攻略、生活技巧",
    bg="#C9A77A", ink="#2B2118", accent="#C4381F", accent2="#2F6F8F", muted="#42311F", line="#2B2118", surface="#FBF6EA",
    on_accent="#FBF6EA", palette=("#F6D365", "#A8D8B9", "#F4B6C2", "#FBF6EA"),
    display=Face("Caveat", KAI, 700, lh=1.2), body=Face("Quicksand", KAI, 700), tag_face=Face("Quicksand", SANS, 600, 0.06),
    radius=4, stroke=4, card="box-shadow:0 10px 24px rgba(43,33,24,0.24);",
    tag="background:rgba(246,211,101,0.92);padding:0.42em 0.9em;", em="marker", ease="back.out(1.2)", entrance="drop", tilt=1.5,
    ground=lambda c: ("background-image:repeating-linear-gradient(8deg,rgba(43,33,24,0.045) 0 2px,transparent 2px 9px),"
                      "radial-gradient(ellipse at 50% 50%,transparent 55%,rgba(43,33,24,0.20));"),
    cap_plate="background:#FBF6EA;box-shadow:0 6px 16px rgba(43,33,24,0.26);padding:10px 32px 12px;",
    cap_colors=("rgba(43,33,24,0.52)", "#D9442B", "#2B2118"), cap_face="body", bgm="warm", origin="custom",
)

BLUEPRINT = Style(
    name="blueprint", label="工程蓝图", mood="深蓝图纸底、白色细线网格、等宽标注字，像一张施工图",
    fit="系统架构、工作原理、流程拆解、工程和制造",
    bg="#0F3D7A", ink="#EAF2FF", accent="#FFD23F", muted="rgba(234,242,255,0.72)", line="rgba(234,242,255,0.62)",
    surface="rgba(234,242,255,0.07)", on_accent="#0F3D7A",
    display=Face("JetBrains Mono", SANS, 700, -0.02, lh=1.16), body=Face("Inter", SANS, 500),
    tag_face=Face("JetBrains Mono", SANS, 500, 0.08, "upper"),
    scale=0.9, stroke=2, card="border:2px dashed var(--k-line);", tag="border:2px solid var(--k-line);padding:0.4em 0.8em;",
    em="outline", chrome="rules", ease="power2.out", entrance="fade",
    ground=lambda c: (f"background-image:{_grid('rgba(234,242,255,0.16)')},{_grid('rgba(234,242,255,0.06)')};"
                      "background-size:160px 160px,160px 160px,32px 32px,32px 32px;"),
    cap_plate="background:rgba(8,36,74,0.90);border:2px solid rgba(234,242,255,0.62);padding:10px 32px 12px;",
    cap_colors=("rgba(234,242,255,0.52)", "#FFD23F", "#EAF2FF"), cap_face="body", cap_weight=700, origin="custom",
)

CUSTOM = (INK_WASH, NEWSPRINT, BLACK_GOLD, NEON_NIGHT, AURORA_GLASS, BLUEPRINT, CHALKBOARD, KRAFT_NOTES)
