"""颜色计算：解析 CSS 颜色、叠色、按 WCAG 算对比度。用来给色块上的字挑颜色，以及检查一种风格的配色看不看得清。"""
from __future__ import annotations

import re

RGBA_RE = re.compile(r"rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*(?:,\s*([\d.]+)\s*)?\)")
MIX_RE = re.compile(r"color-mix\(in srgb,\s*(.+?)\s+([\d.]+)%\s*,\s*(.+?)\s*\)$")
Rgba = tuple[float, float, float, float]


def parse(color: str) -> Rgba | None:
    """把 #RRGGBB、rgb()、rgba()、color-mix(in srgb, A P%, B) 解析成 (r, g, b, a)；不认识的返回 None。"""
    color = color.strip()
    if color == "transparent":
        return (0.0, 0.0, 0.0, 0.0)
    if color.startswith("#") and len(color) == 7:
        return (int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16), 1.0)
    m = RGBA_RE.fullmatch(color)
    if m:
        return (float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4) or 1))
    m = MIX_RE.fullmatch(color)
    if m:
        a, b, share = parse(m.group(1)), parse(m.group(3)), float(m.group(2)) / 100
        if a and b:
            alpha = a[3] * share + b[3] * (1 - share)
            if alpha == 0:
                return (0.0, 0.0, 0.0, 0.0)
            mix = tuple((a[i] * a[3] * share + b[i] * b[3] * (1 - share)) / alpha for i in range(3))
            return (*mix, alpha)
    return None


def over(top: str, under: str) -> str:
    """半透明的 top 叠在不透明的 under 上，得到的不透明颜色（#RRGGBB）。解析不了时返回 under。"""
    t, u = parse(top), parse(under)
    if not t or not u:
        return under
    return "#" + "".join(f"{round(t[i] * t[3] + u[i] * (1 - t[3])):02X}" for i in range(3))


def luminance(color: str) -> float:
    rgba = parse(color)
    if not rgba:
        return 0.5
    channels = [c / 255 for c in rgba[:3]]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(text: str, ground: str, under: str = "#FFFFFF") -> float:
    """文字色和底色的对比度（1–21）。底色半透明时先叠到 under 上，文字半透明时再叠到底色上。"""
    solid_ground = over(ground, under)
    a, b = luminance(over(text, solid_ground)), luminance(solid_ground)
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)


def readable_on(ground: str, preferred: tuple[str, ...], under: str = "#FFFFFF", enough: float = 4.5) -> str:
    """在 preferred 里按顺序找第一个够清楚的；都不够就在它们加黑白里挑对比度最高的。"""
    for color in preferred:
        if contrast(color, ground, under) >= enough:
            return color
    return max((*preferred, "#FFFFFF", "#111111"), key=lambda color: contrast(color, ground, under))
