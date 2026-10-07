"""帧 6–10：2024 后两帧、2025 三帧。每个函数返回 (html, js)。"""
from __future__ import annotations

from theme import (INK, arrow_h, arrow_v, block, box, cells, chapter_column, check, chip, ink, node, rail, tag, txt)
from frames_a import ICON_PIC


def frame_06() -> tuple[str, str]:
    rail_html, rail_js = rail(2024.1, 2024.67)
    heights = (294, 224, 154, 84, 28)
    bars = "".join(f'<div class="gw-stack §bar" style="left:{128 + i * 104}px;top:{824 - h}px;width:76px;height:{h}px"></div>'
                   for i, h in enumerate(heights))
    html = (
        rail_html + box("c1", 96, 170, 804, 670) + tag("d1", "2024 · 国内", 128, 196)
        + txt("lm", "gw-sm", "大模型", 128, 256) + txt("pw", "gw-h1", "价格战", 128, 322) + bars
        + txt("u1", "gw-h3", "元", 706, 470) + ink("s1", 690, 514, 116, 5)
        + txt("u2", "gw-h3", "分", 706, 580) + ink("s2", 690, 624, 116, 5)
        + block("u3", "gw-kwm", "厘", 690, 700)
        + box("c2", 960, 170, 864, 670) + tag("d2", "2024.09", 992, 196) + txt("o1", "gw-d2", "o1", 992, 270)
        + node("q", "问题", 992, 590, 190, 150) + arrow_h("a1", 1190, 663, 44)
        + txt("oa", "gw-lab", "先", 1262, 546) + node("th", "思考", 1262, 590, 290, 150, extra="padding-bottom:44px")
        + cells("dots", 1296, 690, 6, 1, 24, 16, "dot")
        + arrow_h("a2", 1560, 663, 44) + txt("ob", "gw-lab", "再", 1632, 546)
        + node("ans", "回答", 1632, 590, 170, 150, "solid")
    )
    js = rail_js + """
fade("#§c1", 0.15, 0.4); pop("#§d1", 0.25); up("#§lm", @[大] - 0.1, 0.5, 16); up("#§pw", @[价格战] - 0.15);
grow(".§bar", @[打], 0.5, 0.42);
up("#§u1", @[调用], 0.5, 16); wipe("#§s1", @[成本], 0.3); up("#§u2", @[成本], 0.5, 16); wipe("#§s2", @[降到], 0.3);
blk("#§u3", @[厘] - 0.15);
fade("#§c2", @[九月] - 0.5); up("#§d2", @[九月] - 0.1, 0.5, 16); up("#§o1", @[o] - 0.15, 0.8, 50);
pop("#§q", @[AI] - 0.1); wipe("#§a1", @[开始], 0.3); fade("#§a1-h", @[开始] + 0.2, 0.2);
up("#§oa", @[先], 0.4, 12); pop("#§th", @[先] + 0.05); fade("#§dots", @[先] + 0.05, 0.2); fill(".§dot", @[思考], 0.1);
wipe("#§a2", @[再] - 0.15, 0.3); fade("#§a2-h", @[再] + 0.05, 0.2); up("#§ob", @[再], 0.4, 12);
pop("#§ans", @[回答] - 0.1);
"""
    return html, js


def frame_07() -> tuple[str, str]:
    rail_html, rail_js = rail(2024.67, 2024.75)

    def plaque(id_: str, x: int, label: str) -> str:
        medal = (f'<svg class="gw-a" style="left:24px;top:24px" width="80" height="80" viewBox="0 0 80 80">'
                 f'<rect x="3" y="3" width="74" height="74" fill="none" stroke="{INK}" stroke-width="5"/>'
                 f'<rect x="24" y="24" width="32" height="32" fill="{INK}"/></svg>')
        return box(id_, x, 400, 330, 250, medal + f'<div class="gw-a gw-h4" style="left:24px;top:150px">{label}</div>')

    links = (
        '<svg class="gw-a" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">'
        f'<path id="§ln1" d="M261 652 V700 H446 V742" fill="none" stroke="{INK}" stroke-width="4" pathLength="1" stroke-dasharray="1"/>'
        f'<path id="§ln2" d="M631 652 V700 H446" fill="none" stroke="{INK}" stroke-width="4" pathLength="1" stroke-dasharray="1"/></svg>'
    )
    toy_icon = (
        f'<svg id="§ticon" class="gw-a" style="left:1230px;top:262px" width="90" height="80" viewBox="0 0 90 80">'
        f'<rect x="2" y="42" width="36" height="36" fill="none" stroke="{INK}" stroke-width="4"/>'
        f'<rect x="44" y="42" width="36" height="36" fill="none" stroke="{INK}" stroke-width="4"/>'
        f'<rect x="23" y="4" width="36" height="36" fill="{INK}"/></svg>'
    )
    pillars = "".join(ink("", 980 + i * 86, 768, 60, 72, cls="§pl") for i in range(9))
    html = (
        rail_html + tag("d", "2024.10", 96, 170) + txt("nb", "gw-h2", "诺贝尔奖", 96, 244)
        + plaque("p1", 96, "物理学奖") + plaque("p2", 466, "化学奖") + links
        + block("ai", "gw-kw2", "AI 相关研究", 296, 742)
        + txt("ai2", "gw-mono2", "AI", 984, 196) + txt("toy", "gw-h2", "玩具", 980, 240) + toy_icon
        + ink("st", 968, 300, 244, 5) + arrow_v("av", 1040, 388, 84)
        + block("infra", "gw-kwb", "基础设施", 980, 520) + pillars
    )
    js = rail_js + """
pop("#§d", 0.2); up("#§nb", @[诺贝尔] - 0.15);
pop("#§p1", @[物理学] - 0.1); pop("#§p2", @[化学] - 0.1);
draw("#§ln1", @[颁给] - 0.1, 0.6); draw("#§ln2", @[颁给] - 0.1, 0.6); blk("#§ai", @[AI] - 0.1);
up("#§ai2", @[AI#2], 0.4, 12); up("#§toy", @[新鲜] - 0.1); pop("#§ticon", @[玩具]);
wipe("#§st", @[变成], 0.35); grow("#§av", @[变成] + 0.1, 0.35, 0, "center top"); fade("#§av-h", @[变成] + 0.4, 0.15);
wipe("#§infra-bg", @[基础] - 0.15, 0.55); fade("#§infra-t", @[基础], 0.4);
grow(".§pl", @[设施], 0.45, 0.06);
"""
    return html, js


def frame_08() -> tuple[str, str]:
    rail_html, rail_js = rail(2024.75, 2025.05)
    pointer = (f'<svg id="§ptr" class="gw-a" style="left:646px;top:640px" width="62" height="90" viewBox="0 0 62 90">'
               f'<path d="M4 4 L4 70 L22 54 L34 84 L46 79 L34 50 L58 50 Z" fill="{INK}"/></svg>')
    ripple = f'<div id="§rip" class="gw-a" style="left:600px;top:594px;width:100px;height:100px;border:3px solid {INK}"></div>'
    html = (
        rail_html + chapter_column(3, 2025, block("kw", "gw-kw", "会动手", 96, 552)) + ripple + pointer
        + box("card", 880, 170, 944, 670) + tag("d1", "2025 · 春节", 912, 196) + txt("ds", "gw-h1", "DeepSeek", 912, 252)
        + chip("f1", "开源", 912, 430) + chip("f2", "便宜", 1112, 430) + chip("f3", "好用", 1312, 430)
        + txt("first", "gw-sm", "第一次用上", 912, 566) + cells("ppl", 912, 626, 20, 3, 26, 12, "pp")
        + block("reason", "gw-kw2", "会推理的 AI", 912, 762)
    )
    js = rail_js + """
fade("#§ch", 0.2); up("#§yr", 0.25, 0.8, 50); fade("#§kwl", @[关键词]); blk("#§kw", @[会] - 0.1);
pop("#§ptr", @[动手]);
tl.fromTo("#§rip", { opacity: 0, scale: 0.3 }, { opacity: 0.9, duration: 0.05 }, @[动手] + 0.4);
tl.to("#§rip", { scale: 1.3, opacity: 0, duration: 0.6, ease: "power2.out" }, @[动手] + 0.45);
tl.to("#§ptr", { scale: 0.86, duration: 0.12 }, @[动手] + 0.4).to("#§ptr", { scale: 1, duration: 0.22 }, @[动手] + 0.52);
fade("#§card", @[春节] - 0.5); up("#§d1", @[春节] - 0.1, 0.5, 16); up("#§ds", @[DeepSeek] - 0.15);
pop("#§f1", @[开源] - 0.05); pop("#§f2", @[便宜] - 0.05); pop("#§f3", @[还好] - 0.05);
fade("#§ppl", @[让], 0.3); fill(".§pp", @[很多], 0.028); up("#§first", @[第一] - 0.1, 0.5, 16);
blk("#§reason", @[会#2] - 0.1);
"""
    return html, js


def frame_09() -> tuple[str, str]:
    rail_html, rail_js = rail(2025.05, 2025.17)
    rings = "".join(
        f'<div class="gw-a §ring" style="left:{391 - w // 2}px;top:{640 - h // 2}px;width:{w}px;height:{h}px;'
        f'border:2px solid {INK}"></div>'
        for w, h in ((560, 270), (660, 370), (760, 460))
    )
    paragraphs = (
        (296, ((0, 520), (0, 640), (0, 440))),
        (426, ((0, 600), (40, 360), (40, 560), (0, 300))),
        (596, ((0, 480), (40, 620), (0, 380))),
        (726, ((0, 540), (0, 420))),
    )
    code = "".join(
        ink("", 1000 + indent, top + j * 30, width, 14, cls=f"§p{i + 1}")
        for i, (top, lines) in enumerate(paragraphs) for j, (indent, width) in enumerate(lines)
    )
    editor_inner = ink("", 0, 70, 900, 2) + ink("", 56, 90, 2, 500, extra="opacity:0.25")
    html = (
        rail_html + tag("d", "2025.03", 96, 170) + txt("manus", "gw-h1b", "Manus", 96, 232)
        + rings + block("agent", "gw-kwb2", "智能体", 150, 546)
        + box("ed", 920, 180, 904, 660, editor_inner) + tag("t1", "Claude Code", 944, 196) + tag("t2", "Codex", 1190, 196)
        + code + txt("st", "gw-mono2", "编程智能体 · 写入中", 944, 794)
    )
    js = rail_js + """
pop("#§d", 0.2); up("#§manus", @[Manus] - 0.2); blk("#§agent", @[智能体] - 0.1);
tl.fromTo(".§ring", { opacity: 0, scale: 0.7 }, { opacity: (i) => [0.7, 0.45, 0.25][i], scale: 1, duration: 0.7, ease: E, stagger: 0.14 }, @[出]);
fade("#§ed", @[Claude] - 0.5); pop("#§t1", @[Claude] - 0.05); pop("#§t2", @[Codex] - 0.05);
up("#§st", @[编程], 0.5, 12);
wipe(".§p1", @[整段], 0.35, null, 0.07); wipe(".§p2", @[整段#2], 0.35, null, 0.07);
wipe(".§p3", @[替程], 0.35, null, 0.07); wipe(".§p4", @[代码], 0.35, null, 0.07);
"""
    return html, js


def frame_10() -> tuple[str, str]:
    rail_html, rail_js = rail(2025.17, 2025.58)

    def tile(id_: str, x: int, icon: str, label: str) -> str:
        inner = (f'<svg class="gw-a" style="left:24px;top:26px" width="110" height="96" viewBox="0 0 80 70">{icon}</svg>'
                 f'<div class="gw-a gw-h5" style="left:24px;top:168px">{label}</div>')
        return box(id_, x, 540, 240, 250, inner)

    play = f'<rect x="3" y="3" width="74" height="62" fill="none" stroke="{INK}" stroke-width="5"/><path d="M30 18 L56 34 L30 50 Z" fill="{INK}"/>'
    widths = (300, 240, 280)
    todo = "".join(check(f"k{i}", 1410, 480 + i * 68) + ink("", 1474, 496 + i * 68, w, 12) for i, w in enumerate(widths))
    html = (
        rail_html + tag("d", "2025.08", 96, 170) + txt("g5", "gw-d2", "GPT-5", 96, 256)
        + tile("t1", 96, ICON_PIC, "图片") + tile("t2", 366, play, "视频") + block("real", "gw-kw2", "以假乱真", 640, 628)
        + txt("ty", "gw-lab", "这一年", 984, 176) + txt("ay", "gw-h1", "智能体元年", 980, 244) + ink("ul", 980, 398, 650, 4)
        + node("sg", "建议", 980, 480, 280, 170, extra="font-size:80px") + ink("ss", 960, 563, 320, 5)
        + arrow_h("ar", 1290, 563, 70)
        + f'<div id="§list" class="gw-a" style="left:0;top:0">{todo}</div>'
        + block("done", "gw-kw2", "把事做完", 1410, 700)
    )
    js = rail_js + """
pop("#§d", 0.2); up("#§g5", @[GPT] - 0.15, 0.8, 50);
pop("#§t1", @[图片] - 0.1); pop("#§t2", @[视频] - 0.1); blk("#§real", @[以假乱真] - 0.1);
up("#§ty", @[这], 0.5, 12); up("#§ay", @[智能] - 0.15); wipe("#§ul", @[体元年] + 0.2, 0.6);
pop("#§sg", @[AI]); wipe("#§ss", @[建议], 0.35);
wipe("#§ar", @[它], 0.3); fade("#§ar-h", @[它] + 0.2, 0.2); fade("#§list", @[开始], 0.35);
draw("#§k0", @[自己], 0.3); draw("#§k1", @[把事], 0.3); draw("#§k2", @[做完], 0.3);
blk("#§done", @[做完] + 0.15);
"""
    return html, js
