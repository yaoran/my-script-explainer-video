"""风格库：按名字取风格。清单见 `python tools/project.py styles`。"""
from __future__ import annotations

from stylekit import Style

from .custom import CUSTOM
from .presets import PRESETS

STYLES: dict[str, Style] = {s.name: s for s in (*PRESETS, *CUSTOM)}


def get_style(name: str) -> Style:
    if name not in STYLES:
        raise SystemExit(f"没有叫 {name!r} 的风格。可选：{'、'.join(STYLES)}")
    return STYLES[name]
