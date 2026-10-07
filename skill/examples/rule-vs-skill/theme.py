"""本片的视觉设定。

风格和画幅不在这里改，在 tools/video.json 里选（.venv/bin/python tools/project.py set style=… aspect=…）。
K 是本片的画面积木，镜头脚本里 `from theme import K` 来用。
只属于这一条片子的东西写在这个文件下面：主线画面的固定参数、反复出现的小组合。
"""
from __future__ import annotations

from project import make_kit

K = make_kit()
THEME = K.theme()
