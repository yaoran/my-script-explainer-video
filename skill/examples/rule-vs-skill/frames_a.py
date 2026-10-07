"""四镜：开场、Rule、Skill、一句话记住。全部用现成画面，横屏和竖屏共用这一份。"""
from __future__ import annotations

from backbone import tabs
from scenes import define, headline, join, versus
from theme import K

SIDES = ["RULE", "SKILL"]


def frame_01():
    top, bottom = K.c.content.split_v(0.36, K.c.gap)
    return join(
        tabs(K, SIDES),
        headline(K, ["写给 AI 的规矩"], ["@[写给]"], sub="它们到底差在哪？", sub_cue="@[它们]", size="lg", box=top, p="h"),
        versus(K, ("有人叫", "Rule", ""), ("有人叫", "Skill", ""), ("@[Rule]", "@[Skill]"), box=bottom),
    )


def frame_02():
    return join(
        tabs(K, SIDES, (0,)),
        define(K, "Rule", "底线", ("@[Rule]", "@[底线]"), label="RULE",
               note="每一次对话都生效，比如：不许泄露密钥", note_cue="@[每一次]"),
    )


def frame_03():
    return join(
        tabs(K, SIDES, (1,)),
        define(K, "Skill", "能力", ("@[Skill]", "@[能力]"), label="SKILL",
               note="遇到对应的任务才会被调用，比如：做一条解说视频", note_cue="@[遇到]", fill="accent2"),
    )


def frame_04():
    top, bottom = K.c.content.split_v(0.2, K.c.gap)
    return join(
        tabs(K, SIDES, (0, 1)),
        headline(K, ["一句话记住"], ["@[一句话]"], size="md", box=top, p="h"),
        versus(K, ("所有对话都要守的", "写成 Rule", ""), ("特定任务才用的", "写成 Skill", ""), ("@[所有]", "@[特定]"), box=bottom),
    )
