"""风格样张：把每一种现成画面各用一次，用来看一种风格在某个画幅下的样子。也是各个画面函数的用法示例。"""
from __future__ import annotations

from backbone import dots, rail, tabs
from charts import bars, checklist, compare, grid_fill, steps
from scenes import ask, big_number, cards, define, headline, join, stack, versus
from theme import K

STAGES = ["文案", "风格", "配音", "出片"]


def frame_01():
    return headline(K, ["一条解说视频", ("怎么做出来的", "em")], ["@[一条]", "@[怎么]"], kicker="三分钟看懂",
                    sub="从一份文案，到一条成片", sub_cue="@[出来]")


def frame_02():
    return define(K, "文案", "骨架", ("@[文案]", "@[骨架]"), label="第一步", note="画面跟着文案走", note_cue="@[画面]")


def frame_03():
    return big_number(K, 720, "@[七百]", unit="字", label="三分钟的片子", note="按每秒大约 4 个字估算")


def frame_04():
    return bars(K, [("1 分钟", 240, "@[一分钟]"), ("2 分钟", 480, "@[两分钟]"), ("3 分钟", 720, "@[三分钟]")],
                unit="字", title="时长和字数")


def frame_05():
    return join(tabs(K, ["横屏", "竖屏"], (0, 1)),
                versus(K, ("16:9", "横屏", "电脑和电视"), ("9:16", "竖屏", "手机全屏"), ("@[横屏]", "@[竖屏]")))


def frame_06():
    return versus(K, ("以前", "手工排版", "一个个填坐标"), ("现在", "积木自动排", "换比例也不乱"), ("@[以前]", "@[现在]"), mode="to")


def frame_07():
    return cards(K, [("配音", "云扬原速", "@[配音]"), ("字幕", "逐词高亮", "@[字幕]"), ("配乐", "程序合成", "@[配乐]")],
                 title="三样都是自动生成的", title_cue="@[三样] - 0.2")


def frame_08():
    return steps(K, [("写文稿", "@[先]"), ("定风格", "@[再]"), ("配音", "@[然后]"), ("出片", "@[最后]")], current=3)


def frame_09():
    return join(dots(K, 4, 1),
                checklist(K, [("画面不出框", "@[画面]"), ("字幕不超宽", "@[字幕]"), ("声音不断档", "@[声音]"), ("时长对得上", "@[时长]")],
                          title="出片前检查四件事", title_cue="@[出片]"))


def frame_10():
    return grid_fill(K, 21, 8, "@[风格库]", lit_cue="@[八种]", label="是自己设计的风格", value="8 / 21", cols=7)


def frame_11():
    return ask(K, "换一个比例，画面会乱吗？", "@[那]", answer="不会", answer_cue="@[不会#2]", label="常被问到")


def frame_12():
    return compare(K, ("以前", "现在"), [("比例", "一种", "五种", "@[比例]", "@[五种]"), ("风格", "两种", "二十一种", "@[风格]", "@[二十一种]"),
                                    ("声音", "云扬", "可以换", "@[声音]", "@[也可以]")])


def frame_13():
    return stack(K, [("文案", "@[一层]"), ("画面", "@[一层#2]"), ("字幕和声音", "@[再]")], title="一层一层叠起来")


def frame_14():
    return join(rail(K, STAGES, 1, 0), headline(K, ["怎么选风格"], ["@[怎么]"], kicker="第二部分"))


def frame_15():
    return headline(K, ["文案定了", ("画面就定了", "em")], ["@[文案]", "@[画面]"], kicker="记住一句话")
