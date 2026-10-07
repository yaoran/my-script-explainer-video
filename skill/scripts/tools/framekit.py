"""镜头文件的通用内核，与配色和版式无关。

每一镜由 tools/frames_*.py 里的 frame_NN() 给出 (html, js) 或 (html, js, 底色层样式)，build_frames.py 用这里的
render_frame 包成 compositions/frames/NN-slug.html。配色、字体、版面家具和 HTML 小积木
都在工程自己的 tools/theme.py 里，换风格只改那一个文件，这个文件不用动。

html / js 里的两个占位：
  §        本镜的 id 前缀（如 f03-），避免跨镜重名
  @[词]    旁白说到这几个字的秒数，按本镜文案的原文写；@[词#2] 是它在原文里第 2 次出现
"""
from __future__ import annotations

import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field

GSAP_URL = "https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"
CUE_RE = re.compile(r"@\[([^\]#]+)(?:#(\d+))?\]")


@dataclass(frozen=True)
class Font:
    """一个字重的字体。src 是 .fonts-src 里的源文件名，缺文件时从 url 下载。"""

    family: str
    weight: int
    src: str
    url: str = ""
    axes: Mapping[str, float] = field(default_factory=dict)
    unicode_range: str = ""  # 只让这个字体负责一部分字符，其余的交给字体栈里后面的字体

    @property
    def out(self) -> str:
        return f"{self.family.replace(' ', '')}-{self.weight}.woff2"


@dataclass(frozen=True)
class Theme:
    """一条片子的视觉设定。chrome(镜号, 总镜数) 返回每镜都有的版面家具。"""

    fonts: tuple[Font, ...]
    css: str
    chrome: Callable[[int, int], str]
    width: int = 1920
    height: int = 1080
    ground_class: str = "ground"
    ease: str = "power3.out"
    entrance: str = "up"
    bg: str = "#FFFFFF"
    caption: "CaptionStyle | None" = None


@dataclass(frozen=True)
class CaptionStyle:
    """字幕的样子。三种词色对应：还没说到、正在说、已经说过。plate / active 是附加的 CSS 声明。"""

    family: str
    weight: int = 700
    upcoming: str = "rgba(0,0,0,0.45)"
    active: str = "#000000"
    spoken: str = "#000000"
    plate: str = ""
    active_css: str = ""
    tracking: str = "0"


def font_faces(fonts: tuple[Font, ...]) -> str:
    return "\n".join(
        f'@font-face{{font-family:"{f.family}";src:url("assets/fonts/{f.out}") format("woff2");'
        f"font-weight:{f.weight};font-style:normal;font-display:block;"
        f"{'unicode-range:' + f.unicode_range + ';' if f.unicode_range else ''}}}"
        for f in fonts
    )


def js_prelude(ease: str, entrance: str = "up") -> str:
    """每镜脚本开头的 GSAP 小函数。入场一律 fromTo，保证按帧拖动时结果确定。"""
    return f"""
const tl = gsap.timeline({{ paused: true }});
const E = "{ease}";
const up = (s, t, d, y) => tl.fromTo(s, {{ opacity: 0, y: y == null ? 34 : y }}, {{ opacity: 1, y: 0, duration: d || 0.7, ease: E }}, t);
const fade = (s, t, d) => tl.fromTo(s, {{ opacity: 0 }}, {{ opacity: 1, duration: d || 0.5, ease: "power2.out" }}, t);
const wipe = (s, t, d, o, st) => tl.fromTo(s, {{ scaleX: 0 }}, {{ scaleX: 1, duration: d || 0.6, ease: E, transformOrigin: o || "left center", stagger: st || 0 }}, t);
const grow = (s, t, d, st, o) => tl.fromTo(s, {{ scaleY: 0 }}, {{ scaleY: 1, duration: d || 0.6, ease: E, transformOrigin: o || "center bottom", stagger: st || 0 }}, t);
const pop = (s, t, d, st) => tl.fromTo(s, {{ opacity: 0, scale: 0.84 }}, {{ opacity: 1, scale: 1, duration: d || 0.45, ease: E, stagger: st || 0 }}, t);
const draw = (s, t, d) => tl.fromTo(s, {{ strokeDashoffset: 1 }}, {{ strokeDashoffset: 0, duration: d || 0.9, ease: "power2.inOut" }}, t);
const blk = (s, t) => {{ wipe(s + "-bg", t, 0.5); fade(s + "-t", t + 0.16, 0.4); }};
const fill = (s, t, each) => tl.fromTo(s, {{ opacity: 0.12 }}, {{ opacity: 1, duration: 0.2, ease: "none", stagger: each }}, t);
const count = (s, a, b, t, d, f) => {{
  const o = {{ v: a }};
  tl.to(o, {{ v: b, duration: d, ease: "power2.out", onUpdate: () => {{ const el = document.querySelector(s); if (el) el.textContent = f(o.v); }} }}, t);
}};
const drop = (s, t, d, st) => tl.fromTo(s, {{ opacity: 0, y: -40 }}, {{ opacity: 1, y: 0, duration: d || 0.6, ease: E, stagger: st || 0 }}, t);
const slide = (s, t, d, x, st) => tl.fromTo(s, {{ opacity: 0, x: x == null ? -60 : x }}, {{ opacity: 1, x: 0, duration: d || 0.6, ease: E, stagger: st || 0 }}, t);
const type = (s, t, d, n) => tl.fromTo(s, {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: d || 0.8, ease: "steps(" + (n || 12) + ")" }}, t);
const tint = (s, t, c, d, st) => tl.to(s, {{ backgroundColor: c, duration: d || 0.25, ease: "none", stagger: st || 0 }}, t);
const dim = (s, t, o) => tl.to(s, {{ opacity: o == null ? 0.35 : o, duration: 0.3, ease: "none" }}, t);
const ENTER = {{ up: {{ opacity: 0, y: 34 }}, pop: {{ opacity: 0, scale: 0.84 }}, drop: {{ opacity: 0, y: -40 }}, slide: {{ opacity: 0, x: -60 }}, fade: {{ opacity: 0 }} }};
const enter = (s, t, st, d) => tl.fromTo(s, ENTER["{entrance}"], {{ opacity: 1, x: 0, y: 0, scale: 1, duration: d || 0.6, ease: E, stagger: st || 0 }}, t);
"""


def locate_words(text: str, words: list[dict]) -> list[dict]:
    """给每个词标出它在原文里的位置 at。配音引擎偶尔会改写个别词，找不到时沿用当前位置，不中断。"""
    pos, located = 0, []
    for w in words:
        idx = text.find(w["text"], pos)
        if idx < 0:
            idx = text.find(w["text"].strip(), pos)
        at = idx if idx >= 0 else pos
        located.append({**w, "at": at})
        pos = at + (len(w["text"]) if idx >= 0 else 0)
    return located


def _find_nth(text: str, token: str, nth: int) -> int:
    idx = -1
    for _ in range(nth):
        idx = text.find(token, idx + 1 if idx < 0 else idx + len(token))
        if idx < 0:
            return -1
    return idx


def cue_time(token: str, nth: int, text: str, located: list[dict]) -> float | None:
    """原文里第 nth 次出现的 token 被说到的秒数；落在一个词中间时按字数比例插值。"""
    idx = _find_nth(text, token, nth)
    if idx < 0:
        return None
    for w in located:
        size = max(1, len(w["text"]))
        if w["at"] <= idx < w["at"] + size:
            return w["start"] + (idx - w["at"]) / size * (w["end"] - w["start"])
    later = [w for w in located if w["at"] > idx]
    return later[0]["start"] if later else located[-1]["end"]


def resolve_cues(src: str, words: list[dict], frame_no: int, text: str | None = None) -> str:
    """把 @[词] 换成秒数。给了本镜文案 text 就按原文位置找（不受配音切词影响）；没给则要求和切词一字不差。"""
    located = locate_words(text, words) if text else []

    def repl(m: re.Match) -> str:
        token, nth = m.group(1), int(m.group(2) or 1)
        if text:
            t = cue_time(token, nth, text, located)
            if t is None:
                raise KeyError(f"镜 {frame_no}: 文案里找不到第 {nth} 个 {token!r}。本镜文案：{text}")
            return f"{t:.2f}"
        hits = [w for w in words if w["text"] == token]
        if len(hits) < nth:
            available = " | ".join(w["text"] for w in words)
            raise KeyError(f"镜 {frame_no}: 旁白里找不到第 {nth} 个 {token!r}。本镜可用的词：{available}")
        return f"{hits[nth - 1]['start']:.2f}"

    return CUE_RE.sub(repl, src)


def render_frame(theme: Theme, n: int, total: int, slug: str, duration: float,
                 html: str, js: str, words: list[dict], ground_style: str = "",
                 text: str | None = None, pad: float = 0.0, frame_css: str = "") -> str:
    """ground_style 是这一镜底色层的内联样式；pad 是为了给转场留出的尾巴；frame_css 是只对这一镜生效的 CSS 声明。"""
    comp_id = f"{n:02d}-{slug}"
    prefix = f"f{n:02d}-"
    span = round(duration + pad, 3)
    body = (theme.chrome(n, total) + html).replace("§", prefix)
    style = f' style="{ground_style}"' if ground_style else ""
    ground = (f'<div id="{prefix}ground" class="{theme.ground_class} clip"{style} data-start="0" '
              f'data-duration="{span}" data-track-index="0"></div>')
    script = resolve_cues(js, words, n, text).replace("§", prefix)
    scoped = f'[data-composition-id="{comp_id}"][data-composition-id]{{{frame_css}}}\n' if frame_css else ""
    return f"""<template>
<script src="{GSAP_URL}"></script>
<style>
{font_faces(theme.fonts)}
{theme.css}{scoped}</style>
<div id="root" data-composition-id="{comp_id}" data-width="{theme.width}" data-height="{theme.height}">
{ground}
{body}
</div>
<script>
(function () {{
{js_prelude(theme.ease, theme.entrance)}
{script}
tl.set({{}}, {{}}, {span});
window.__timelines = window.__timelines || {{}};
window.__timelines["{comp_id}"] = tl;
}})();
</script>
</template>"""
