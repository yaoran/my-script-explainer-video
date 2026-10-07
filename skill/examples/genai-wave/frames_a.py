"""帧 1–5：开场、2023 三帧、2024 章节帧。每个函数返回 (html, js)。"""
from __future__ import annotations

from theme import (FAINT, INK, VEIL, arrow_h, block, box, cells, chapter_column, ink, node, rail, tag, txt)

ICON_DOC = f'<path d="M0 8 H76 M0 32 H76 M0 56 H48" fill="none" stroke="{INK}" stroke-width="6"/>'
ICON_CODE = f'<path d="M24 6 L4 34 L24 62 M52 6 L72 34 L52 62" fill="none" stroke="{INK}" stroke-width="6"/>'
ICON_PIC = (f'<rect x="3" y="3" width="74" height="62" fill="none" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M8 58 L30 30 L46 48 L58 36 L72 58" fill="none" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="52" y="12" width="12" height="12" fill="{INK}"/>')


def frame_01() -> tuple[str, str]:
    bubble = (
        '<svg class="gw-a" style="left:180px;top:236px" width="460" height="330" viewBox="0 0 460 330">'
        f'<path id="§bub" d="M2 2 H458 V262 H150 L90 326 V262 H2 Z" fill="{VEIL}" stroke="{INK}" '
        'stroke-width="4" pathLength="1" stroke-dasharray="1"/></svg>'
    )
    tick_x = (180, 600, 1020, 1440)
    axis = ink("ax", 180, 740, 1560, 4)
    for i, x in enumerate(tick_x):
        axis += ink(f"t{i}", x - 2, 722, 4, 40) + txt(f"y{i}", "gw-h4", str(2023 + i), x, 640)
    axis += ink("t4", 1738, 722, 4, 40) + tag("end", "2026.10", 1620, 662)
    marks = "".join(node(f"q{i}", "?", mid - 28, 714, 56, 56, extra="font-size:40px")
                    for i, mid in enumerate((390, 810, 1230, 1590)))
    html = (
        txt("ago", "gw-lab", "不到四年前", 184, 176) + bubble + txt("chat", "gw-h0", "聊天", 240, 278)
        + arrow_h("ar", 690, 412, 470) + txt("now", "gw-lab", "今天", 880, 366)
        + block("work", "gw-kwb", "上班", 1230, 262)
        + axis + marks + txt("wave", "gw-sm", "生成式 AI · 这一波", 180, 800)
    )
    js = """
draw("#§bub", 0.25, 1.3); up("#§ago", 0.45, 0.6, 20);
up("#§chat", @[聊天] - 0.2);
wipe("#§ar", @[今天], 1.1); fade("#§ar-h", @[今天] + 1.0, 0.2); up("#§now", @[今天], 0.6, 20);
wipe("#§work-bg", @[它], 0.6); up("#§work-t", @[上班] - 0.15, 0.5, 24);
wipe("#§ax", @[从], 1.8);
[0, 1, 2, 3].forEach((i) => {
  const t = @[2023 到 2026] + i * 0.35;
  grow("#§t" + i, t, 0.4); up("#§y" + i, t, 0.5, 20);
});
grow("#§t4", @[10 月] - 0.1, 0.4); pop("#§end", @[10 月] - 0.1);
up("#§wave", @[这], 0.6, 16);
[0, 1, 2, 3].forEach((i) => pop("#§q" + i, @[到底] + i * 0.25, 0.4));
"""
    return html, js


def frame_02() -> tuple[str, str]:
    rail_html, rail_js = rail(2022.9, 2023.0)
    sound = "".join(ink("", 644 + i * 28, 730 - h, 14, h, cls="§snd") for i, h in enumerate((40, 90, 60, 110)))
    heights = (14, 28, 42, 56, 84, 112, 154, 196)
    bars = "".join(f'<div class="gw-stack §bar" style="left:{912 + i * 74}px;top:{826 - h}px;width:56px;height:{h}px"></div>'
                   for i, h in enumerate(heights))
    counter = ('<div id="§cw" class="gw-a gw-d3" style="left:1340px;top:468px"><span id="§cnt">0</span>'
               '<span style="font-size:110px;margin-left:14px">亿</span></div>')
    html = (
        rail_html + chapter_column(1, 2023, block("kw", "gw-kw", "会说话", 96, 552)) + sound
        + box("card", 880, 170, 944, 670) + tag("d1", "2023 · 年初", 912, 196)
        + txt("gpt", "gw-h2", "ChatGPT", 912, 258)
        + txt("live", "gw-sm", "上线", 912, 396) + txt("two", "gw-d3", "2", 912, 468)
        + txt("mon", "gw-h4", "个月", 1010, 538)
        + arrow_h("ar", 1170, 556, 110) + txt("usr", "gw-sm", "用户", 1340, 396) + counter
        + bars + block("fast", "gw-kw2", "增长最快", 1530, 754)
    )
    js = rail_js + """
fade("#§ch", 0.2); up("#§yr", 0.25, 0.8, 50);
fade("#§kwl", @[关键词]); blk("#§kw", @[会] - 0.1); grow(".§snd", @[说话] + 0.1, 0.5, 0.08);
fade("#§card", @[年初] - 0.5); up("#§d1", @[年初] - 0.1, 0.5, 16); up("#§gpt", @[ChatGPT] - 0.1);
up("#§live", @[上线], 0.5, 16); up("#§two", @[两] - 0.1); up("#§mon", @[个], 0.5, 16);
wipe("#§ar", @[用户] - 0.2, 0.5); fade("#§ar-h", @[用户] + 0.2, 0.2); up("#§usr", @[用户], 0.5, 16);
fade("#§cw", @[破] - 0.15, 0.3);
count("#§cnt", 0, 1, @[破], 0.6, (v) => (v >= 0.995 ? "1" : v.toFixed(1)));
grow(".§bar", @[成], 0.5, 0.12); blk("#§fast", @[最] - 0.1);
"""
    return html, js


def frame_03() -> tuple[str, str]:
    rail_html, rail_js = rail(2023.0, 2023.17)

    def skill(id_: str, x: int, icon: str, label: str) -> str:
        inner = (f'<svg class="gw-a" style="left:24px;top:26px" width="80" height="70" viewBox="0 0 80 70">{icon}</svg>'
                 f'<div class="gw-a gw-h5" style="left:24px;top:124px;font-size:46px">{label}</div>')
        return box(id_, x, 540, 250, 200, inner)

    rows = "".join(
        f'<div id="§r{i}" class="gw-a" style="left:980px;top:{430 + i * 96}px;width:480px;height:84px;'
        f'border-bottom:2px solid {FAINT}"><span class="gw-a gw-mono2" style="left:0;top:26px">0{i + 1}</span>'
        f'<span class="gw-a gw-h4" style="left:84px;top:4px">{name}</span></div>'
        for i, name in enumerate(("文心一言", "通义千问", "讯飞星火"))
    )
    html = (
        rail_html + tag("d", "2023.03", 96, 170) + txt("gpt", "gw-d2", "GPT-4", 96, 256) + ink("ul", 96, 498, 676, 4)
        + skill("c1", 96, ICON_DOC, "写文章") + skill("c2", 366, ICON_CODE, "写代码") + skill("c3", 636, ICON_PIC, "看懂图片")
        + txt("cn", "gw-lab", "国内", 984, 176) + txt("bm", "gw-h1", "百模大战", 980, 222)
        + rows + cells("grid", 1524, 430, 10, 10, 24, 6, "gc") + txt("hund", "gw-mono2", "100+", 1524, 748)
    )
    js = rail_js + """
pop("#§d", 0.2); up("#§gpt", @[GPT] - 0.15, 0.8, 50); wipe("#§ul", @[发布], 0.6);
pop("#§c1", @[写] - 0.05); pop("#§c2", @[写#2] - 0.05); pop("#§c3", @[看懂] - 0.05);
up("#§cn", @[国内], 0.5, 16); up("#§bm", @[百模] - 0.15);
fade("#§grid", @[国内], 0.4); fill(".§gc", @[百模], 0.044);
up("#§r0", @[文心] - 0.1, 0.6, 20); up("#§r1", @[通义] - 0.1, 0.6, 20); up("#§r2", @[讯] - 0.1, 0.6, 20);
up("#§hund", @[登场], 0.5, 16);
"""
    return html, js


def frame_04() -> tuple[str, str]:
    rail_html, rail_js = rail(2023.17, 2023.8)

    def picture(id_: str, x: int) -> str:
        return (
            f'<svg id="§{id_}" class="gw-a" style="left:{x}px;top:372px" width="320" height="320" viewBox="0 0 320 320">'
            f'<rect x="2" y="2" width="316" height="316" fill="{VEIL}" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M20 270 L110 150 L170 220 L220 170 L300 270 Z" fill="none" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="220" y="50" width="44" height="44" fill="{INK}"/>'
            f'<path d="M20 290 H300" stroke="{INK}" stroke-width="4"/></svg>'
        )

    typed = ('<div id="§ask" class="gw-a gw-h1" style="left:944px;top:420px">'
             + "".join(f'<span class="§c">{ch}</span>' for ch in "怎么提问") + "</div>")
    html = (
        rail_html + tag("d", "2023", 96, 170) + txt("mj", "gw-h3", "Midjourney", 96, 228)
        + picture("p1", 96) + picture("p2", 446)
        + block("q1", "gw-kw2", "真？", 96, 716) + block("q2", "gw-kw2", "假？", 446, 716)
        + txt("ev", "gw-sm", "人人都在学", 904, 318) + box("pb", 900, 380, 924, 230)
        + typed + ink("caret", 1480, 432, 14, 128) + txt("pl", "gw-mono2", "PROMPT", 904, 634)
    )
    js = rail_js + """
pop("#§d", 0.2); up("#§mj", @[Midjourney] - 0.25, 0.7);
pop("#§p1", @[画] - 0.1, 0.5); pop("#§p2", @[图] - 0.05, 0.5);
blk("#§q1", @[真假] - 0.1); blk("#§q2", @[难辨] - 0.15);
up("#§pb", @[这] - 0.2, 0.6, 24); up("#§pl", @[这], 0.5, 12); up("#§ev", @[人人], 0.5, 16);
fade("#§caret", @[这] + 0.3, 0.2);
tl.fromTo("#§caret", { x: -536 }, { x: 0, duration: 0.6, ease: "steps(4)" }, @[怎么]);
tl.fromTo(".§c", { opacity: 0 }, { opacity: 1, duration: 0.08, stagger: 0.15, ease: "none" }, @[怎么]);
"""
    return html, js


def frame_05() -> tuple[str, str]:
    rail_html, rail_js = rail(2023.8, 2024.1)
    keywords = (block("k1", "gw-kwm", "会看", 96, 560) + block("k2", "gw-kwm", "会听", 346, 560)
                + block("k3", "gw-kwm", "会想", 596, 560))
    eye = (f'<svg id="§i1" class="gw-a" style="left:173px;top:708px" width="80" height="40" viewBox="0 0 80 40">'
           f'<path d="M2 20 L40 2 L78 20 L40 38 Z" fill="none" stroke="{INK}" stroke-width="4"/>'
           f'<rect x="32" y="12" width="16" height="16" fill="{INK}"/></svg>')
    ear = (f'<svg id="§i2" class="gw-a" style="left:423px;top:708px" width="80" height="40" viewBox="0 0 80 40">'
           + "".join(f'<rect x="{6 + i * 15}" y="{20 - h // 2}" width="8" height="{h}" fill="{INK}"/>'
                     for i, h in enumerate((12, 28, 40, 22, 34)))
           + "</svg>")
    mind = (f'<svg id="§i3" class="gw-a" style="left:673px;top:708px" width="80" height="40" viewBox="0 0 80 40">'
            f'<rect x="4" y="24" width="10" height="10" fill="{INK}"/><rect x="24" y="16" width="18" height="18" fill="{INK}"/>'
            f'<rect x="52" y="6" width="28" height="28" fill="{INK}"/></svg>')
    text_lines = "".join(ink("", 22, 26 + i * 30, w, 8, cls="§tl") for i, w in enumerate((150, 130, 156, 90)))
    play = (f'<svg class="gw-a" style="left:96px;top:46px" width="54" height="62" viewBox="0 0 54 62">'
            f'<path d="M0 0 L54 31 L0 62 Z" fill="{INK}"/></svg>')
    h1 = (18, 34, 52, 30, 60, 44, 22, 48, 64, 36, 20, 42, 58, 30, 50, 24, 40, 62, 34, 18, 46, 28)
    h2 = tuple(reversed(h1))
    wave1 = "".join(ink("", 1400 + i * 18, 664 - h, 10, h, cls="§w1") for i, h in enumerate(h1))
    wave2 = "".join(ink("", 1400 + i * 18, 794 - h, 10, h, cls="§w2") for i, h in enumerate(h2))
    html = (
        rail_html + chapter_column(2, 2024, keywords) + eye + ear + mind
        + box("c1", 880, 170, 944, 330) + tag("d1", "2024.02", 912, 194) + txt("sora", "gw-h2", "Sora", 912, 250)
        + box("tc", 1210, 226, 200, 150, text_lines) + arrow_h("a1", 1428, 300, 80)
        + box("film", 1552, 226, 240, 150, play) + txt("tm", "gw-mono2", "0:00", 1634, 392)
        + block("shock", "gw-kw2", "震惊全网", 912, 402)
        + box("c2", 880, 530, 944, 310) + tag("d2", "2024.05", 912, 554) + txt("4o", "gw-h2", "GPT-4o", 912, 612)
        + txt("wl1", "gw-mono2", "人", 1340, 620) + wave1 + txt("wl2", "gw-mono2", "AI", 1340, 750) + wave2
        + block("rt", "gw-kw2", "实时对话", 912, 762)
    )
    js = rail_js + """
fade("#§ch", 0.2); up("#§yr", 0.25, 0.8, 50); fade("#§kwl", @[关键词]);
blk("#§k1", @[会] - 0.1); pop("#§i1", @[看], 0.4);
blk("#§k2", @[会#2] - 0.1); pop("#§i2", @[听], 0.4);
blk("#§k3", @[会#3] - 0.1); pop("#§i3", @[想], 0.4);
fade("#§c1", @[二月] - 0.5); up("#§d1", @[二月] - 0.1, 0.5, 16); up("#§sora", @[Sora] - 0.15);
pop("#§tc", @[一段] - 0.1); wipe(".§tl", @[文字], 0.4, null, 0.08);
wipe("#§a1", @[生成] - 0.3, 0.4); fade("#§a1-h", @[生成], 0.2); pop("#§film", @[生成]);
fade("#§tm", @[一分钟] - 0.2, 0.3);
count("#§tm", 0, 60, @[一分钟], 0.7, (v) => { const s = Math.round(v); return s >= 60 ? "1:00" : "0:" + String(s).padStart(2, "0"); });
blk("#§shock", @[震惊] - 0.1);
fade("#§c2", @[五月] - 0.5); up("#§d2", @[五月] - 0.1, 0.5, 16); up("#§4o", @[GPT] - 0.15);
up("#§wl1", @[真人] - 0.1, 0.4, 10); grow(".§w1", @[真人], 0.4, 0.03);
up("#§wl2", @[实时] - 0.1, 0.4, 10); grow(".§w2", @[实时], 0.4, 0.03);
blk("#§rt", @[对话] - 0.15);
"""
    return html, js
