"""帧 11–15：2026 四帧和收尾。每个函数返回 (html, js)。"""
from __future__ import annotations

from theme import (INK, PAPER, VEIL, arrow_h, arrow_v, block, box, chapter_column, check, ink, node, rail, tag, txt)


def frame_11() -> tuple[str, str]:
    rail_html, rail_js = rail(2025.58, 2026.0)
    badge = (
        f'<svg id="§bdg" class="gw-a" style="left:646px;top:596px" width="84" height="110" viewBox="0 0 84 110">'
        f'<rect x="3" y="14" width="78" height="93" fill="{VEIL}" stroke="{INK}" stroke-width="4"/>'
        f'<rect x="30" y="2" width="24" height="18" fill="{INK}"/><rect x="26" y="34" width="32" height="32" fill="{INK}"/>'
        f'<path d="M16 80 H68 M24 94 H60" stroke="{INK}" stroke-width="5"/></svg>'
    )
    star = (f'<svg id="§star" class="gw-a" style="left:1736px;top:526px" width="60" height="60" viewBox="0 0 60 60">'
            f'<polygon points="30,2 37,22 58,22 41,35 47,56 30,43 13,56 19,35 2,22 23,22" fill="{INK}"/></svg>')
    counter = '<div id="§sw" class="gw-a gw-d4" style="left:1306px;top:508px;font-size:112px"><span id="§stars">0</span></div>'
    html = (
        rail_html + chapter_column(4, 2026, block("kw", "gw-kw", "会上班", 96, 552)) + badge
        + box("card", 880, 170, 944, 670) + tag("d1", "2026.01", 912, 196)
        + txt("os", "gw-sm", "开源智能体", 912, 262) + txt("oc", "gw-h1", "OpenClaw", 912, 304)
        + txt("hd", "gw-d4", "100", 912, 508, "font-size:112px") + txt("day", "gw-h4", "天", 1116, 534) + arrow_h("ar", 1200, 562, 70)
        + counter + star + block("lob", "gw-kw2", "全民“养龙虾”", 912, 740)
    )
    js = rail_js + """
fade("#§ch", 0.2); up("#§yr", 0.25, 0.8, 50); fade("#§kwl", @[关键词]); blk("#§kw", @[会] - 0.1); pop("#§bdg", @[上班]);
fade("#§card", @[一月] - 0.5); up("#§d1", @[一月] - 0.1, 0.5, 16); up("#§os", @[开源], 0.5, 16);
up("#§oc", @[OpenClaw] - 0.15);
up("#§hd", @[一百] - 0.1); up("#§day", @[天], 0.5, 16); wipe("#§ar", @[拿下], 0.3); fade("#§ar-h", @[拿下] + 0.2, 0.2);
fade("#§sw", @[二十五万] - 0.15, 0.3);
count("#§stars", 0, 250000, @[二十五万], 0.7, (v) => Math.round(v).toLocaleString("en-US"));
pop("#§star", @[星] - 0.1); blk("#§lob", @[全民]);
"""
    return html, js


def frame_12() -> tuple[str, str]:
    rail_html, rail_js = rail(2026.0, 2026.17)
    towers = "".join(
        f'<div id="§tw{i}" class="gw-stack" style="left:{x}px;top:{826 - h}px;width:150px;height:{h}px"></div>'
        for i, (x, h) in enumerate(((96, 266), (276, 378), (456, 322)))
    )
    phone_inner = ink("", 65, 14, 60, 8) + '<div class="gw-a gw-mono2" style="left:20px;top:46px;font-size:26px">微信</div>'
    link = (f'<div id="§lk" class="gw-a" style="left:1000px;top:626px;width:270px;height:4px;'
            f'background:repeating-linear-gradient(90deg,{INK} 0 14px,transparent 14px 24px)"></div>'
            f'<svg id="§lk-h" class="gw-a" style="left:1262px;top:613px" width="26" height="30" viewBox="0 0 26 30">'
            f'<path d="M0 0 L26 15 L0 30 Z" fill="{INK}"/></svg>')
    tasks = "".join(check(f"k{i}", 1320, 506 + i * 80, 40) + ink("", 1380, 520 + i * 80, w, 12)
                    for i, w in enumerate((300, 240, 280)))
    monitor = ('<div id="§pcw" class="gw-a" style="left:0;top:0">' + box("pc", 1290, 470, 460, 290)
               + ink("", 1490, 762, 60, 36) + ink("", 1430, 798, 180, 6) + tasks + "</div>")
    html = (
        rail_html + tag("d", "2026", 96, 170) + txt("bf", "gw-h3", "大厂跟进", 96, 240) + towers
        + tag("d2", "2026.03 · 腾讯", 760, 170) + txt("wb", "gw-h1", "WorkBuddy", 760, 246)
        + box("ph", 800, 440, 190, 380, phone_inner) + block("say", "gw-kw3", "发句话", 818, 640) + link + monitor
    )
    js = rail_js + """
pop("#§d", 0.2); up("#§bf", @[大厂] - 0.25);
grow("#§tw0", @[大厂]); grow("#§tw1", @[迅速]); grow("#§tw2", @[跟进]);
pop("#§d2", @[三月] - 0.05); up("#§wb", @[WorkBuddy] - 0.15);
pop("#§ph", @[在] - 0.1); blk("#§say", @[发] - 0.1);
wipe("#§lk", @[电脑] - 0.35, 0.4); fade("#§lk-h", @[电脑], 0.2); pop("#§pcw", @[电脑] - 0.05);
draw("#§k0", @[就], 0.25); draw("#§k1", @[干活], 0.25); draw("#§k2", @[干活] + 0.3, 0.25);
"""
    return html, js


def frame_13() -> tuple[str, str]:
    rail_html, rail_js = rail(2026.17, 2026.5)
    counter = ('<div id="§bw" class="gw-a gw-d0" style="left:1030px;top:296px"><span id="§bn">0</span>'
               '<span style="font-size:170px;margin-left:20px">亿</span></div>')
    html = (
        rail_html + tag("d", "2026.07", 96, 170) + box("app", 380, 230, 540, 570) + txt("gp", "gw-h4", "ChatGPT", 410, 252)
        + node("r1", "聊天", 410, 350, 480, 90, "left") + node("r2", "办公", 410, 460, 480, 90, "left")
        + node("r3", "写代码", 410, 570, 480, 90, "left")
        + node("cx", "Codex", 96, 575, 200, 80, "solid", "font-size:44px")
        + block("one", "gw-kw2", "一个应用", 410, 694)
        + txt("wl", "gw-lab", "周活跃用户", 1044, 196) + counter
        + ink("br", 1040, 668, 700, 4) + txt("bm", "gw-mono2", "1,000,000,000 / WEEK", 1040, 694)
    )
    js = rail_js + """
pop("#§d", 0.2); pop("#§cx", @[Codex] - 0.1);
fade("#§app", @[并入] - 0.4); up("#§gp", @[ChatGPT] - 0.1, 0.5, 16);
tl.to("#§cx", { x: 576, duration: 0.7, ease: "power3.inOut" }, @[并入]);
pop("#§r1", @[聊天] - 0.05); pop("#§r2", @[办公] - 0.05); pop("#§r3", @[写] - 0.05);
blk("#§one", @[合成] + 0.1);
up("#§wl", @[周] - 0.05, 0.5, 16); fade("#§bw", @[突破] - 0.3, 0.3);
count("#§bn", 0, 10, @[突破], 0.6, (v) => String(Math.round(v)));
tl.fromTo("#§bw", { scale: 0.8 }, { scale: 1, duration: 0.6, ease: E, transformOrigin: "left bottom" }, @[突破]);
wipe("#§br", @[十亿] + 0.2, 0.6); up("#§bm", @[十亿] + 0.4, 0.5, 12);
"""
    return html, js


def frame_14() -> tuple[str, str]:
    rail_html, rail_js = rail(2026.5, 2026.67)
    wrench = (f'<svg id="§tic" class="gw-a" style="left:1350px;top:256px" width="80" height="80" viewBox="0 0 80 80">'
              f'<path d="M10 70 L48 32" stroke="{INK}" stroke-width="10"/>'
              f'<rect x="44" y="6" width="30" height="30" fill="none" stroke="{INK}" stroke-width="6"/></svg>')
    badge_inner = ink("", 61, 30, 68, 68) + ink("", 30, 130, 130, 10) + ink("", 46, 160, 98, 10)
    big = "font-size:72px"
    html = (
        rail_html + tag("d", "2026.09", 96, 170)
        + node("c1", "GPT-6", 96, 230, 560, 130, "left", big) + node("c2", "Gemini 4", 176, 390, 560, 130, "left", big)
        + node("c3", "新一代 Claude", 256, 550, 560, 130, "left", big) + block("pile", "gw-kw2", "扎堆发布", 96, 740)
        + txt("ai", "gw-mono2", "AI", 1104, 196) + txt("tool", "gw-h2", "工具", 1100, 240) + wrench
        + ink("st", 1088, 300, 244, 5) + arrow_v("av", 1160, 388, 84)
        + block("mate", "gw-kwb", "同事", 1100, 520) + box("bd", 1550, 520, 190, 223, badge_inner)
    )
    js = rail_js + """
pop("#§d", 0.2);
up("#§c1", @[GPT] - 0.1, 0.6, -40); up("#§c2", @[Gemini] - 0.1, 0.6, -40); up("#§c3", @[新] - 0.1, 0.6, -40);
tl.to("#§c1", { y: 50, duration: 0.5, ease: E }, @[扎堆]); tl.to("#§c3", { y: -50, duration: 0.5, ease: E }, @[扎堆]);
blk("#§pile", @[扎堆] + 0.1);
up("#§ai", @[AI], 0.4, 12); up("#§tool", @[工具] - 0.1); pop("#§tic", @[工具] + 0.1);
wipe("#§st", @[变成], 0.35); grow("#§av", @[变成] + 0.1, 0.35, 0, "center top"); fade("#§av-h", @[变成] + 0.4, 0.15);
wipe("#§mate-bg", @[同事] - 0.25, 0.55); fade("#§mate-t", @[同事] - 0.1, 0.4); pop("#§bd", @[同事] + 0.2);
"""
    return html, js


def frame_15() -> tuple[str, str]:
    steps = ""
    for i, (year, word, h) in enumerate(((2023, "会说话", 170), (2024, "会看会想", 260), (2025, "会动手", 350), (2026, "会上班", 440))):
        x, top = i * 432, 470 - h
        steps += ink(f"s{i}", x, top, 400, h)
        steps += (f'<div id="§sx{i}" class="gw-a" style="left:{x + 24}px;top:{top + 18}px;color:{PAPER}">'
                  f'<div class="gw-mono2">{year}</div>'
                  f'<div class="gw-serif" style="font-size:66px;font-weight:700;line-height:1.2;margin-top:8px">{word}</div></div>')
    stairs = f'<div id="§st" class="gw-a" style="left:96px;top:196px;width:1728px;height:470px">{steps}</div>'
    qr_cells = "".join(
        f'<i style="opacity:{1 if (i * 7 + (i // 8) * 3) % 5 < 3 else 0.12}"></i>' for i in range(64)
    )
    qr = (f'<div id="§qr" class="gw-cells" style="left:1616px;top:206px;grid-template-columns:repeat(8,22px);'
          f'grid-auto-rows:22px;gap:4px">{qr_cells}</div>')
    html = (
        txt("k", "gw-lab", "不到四年 · 四步", 100, 148) + stairs + qr
        + txt("nx", "gw-lab", "接下来的问题", 100, 450)
        + txt("q1", "gw-h2 gw-soft", "AI 能不能", 96, 508) + ink("qs", 86, 566, 510, 6)
        + txt("q2", "gw-hero", "你会不会用？", 96, 648)
    )
    js = """
up("#§k", 0.3, 0.6, 16);
[[0, @[会]], [1, @[会#2]], [2, @[会#4]], [3, @[会#5]]].forEach(([i, t]) => {
  grow("#§s" + i, t - 0.2, 0.6); up("#§sx" + i, t, 0.5, 20);
});
tl.to("#§st", { scale: 0.5, opacity: 0.45, duration: 0.9, ease: "power3.inOut", transformOrigin: "left top" }, @[接下来] - 0.3);
up("#§nx", @[接下来] + 0.3, 0.5, 12); pop("#§qr", @[问题]);
up("#§q1", @[不再], 0.6); wipe("#§qs", @[不能] + 0.3, 0.4);
up("#§q2", @[你会不会] - 0.2, 0.8, 40);
"""
    return html, js
