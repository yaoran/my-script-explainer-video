# 写镜头脚本

每镜一个 Python 函数，返回这一镜的画面和动画。不写 HTML 文件，不填像素坐标：位置从画幅的内容区算出来，颜色和字体跟着风格走。所以同一份脚本换风格、换比例都不用改。

```python
# tools/frames_a.py
from backbone import tabs
from charts import bars
from scenes import headline, join, versus
from theme import K


def frame_01():
    return headline(K, ["一条解说视频", ("怎么做出来的", "em")], ["@[一条]", "@[怎么]"], kicker="三分钟看懂")


def frame_02():
    return join(tabs(K, ["横屏", "竖屏"], (0, 1)),
                versus(K, ("16:9", "横屏", "电脑和电视"), ("9:16", "竖屏", "手机全屏"), ("@[横屏]", "@[竖屏]")))
```

文件名随意，以 `frames_` 开头；函数名必须是 `frame_NN`，镜号和 `tools/frames.json` 对应。15 镜左右分成两三个文件，每个不超过 200 行。
完整的用法示例是 `scripts/gallery/frames_demo.py`，每种现成画面各用了一次；它在 21 种风格、横竖屏下的样子在 `assets/gallery/`。

写法分三层，优先用上面的：

1. **现成画面**（`scenes.py`、`charts.py`）：一个函数就是一整块排好的画面。大部分镜头用它。
2. **纵向排版**（`flow.py`）：现成画面不合适时，把几行字、标签、数字从上到下排进一块区域。
3. **单个积木**（`K.txt`、`K.card` 等）：需要自己定位置时用，位置从 `K.c.content` 切出来，不写死数字。

## 出现时间 `@[词]`

动画的时间写成 `@[词]`，表示旁白说到这几个字的那一刻。**按这一镜文案的原文写**，不用管配音引擎怎么切词。

- 可以加减：`"@[底线] - 0.1"`。元素比语音早 0.1–0.2 秒出现最自然，不要晚于语音。
- 同样的字出现多次：`@[不会#2]` 是原文里第 2 次出现。注意“会不会乱？不会”里，“不会”第 1 次出现在“会**不会**”里。
- 文案里找不到会报错，并打印这一镜的文案。
- 想看每个词的具体时间：`.venv/bin/python tools/show_words.py 3`。

现成画面的参数里，cue 都是这样的字符串。

## 现成画面

所有函数第一个参数是 `K`，都返回 `(html, js)`，都接受 `box=`（放在哪块区域，默认整个内容区）和 `p=`（id 前缀，同一镜放两个同类画面时要不同）。

`scenes.py`：

| 函数 | 画面 | 关键参数 |
| --- | --- | --- |
| `headline(K, lines, cues, kicker, sub, sub_cue, size, align)` | 大字标题或一句结论 | `lines` 一项一行；`("词", "em")` 那一行是强调词。`cues` 和 `lines` 一一对应 |
| `big_number(K, value, cue, unit, label, note, start, decimals, prefix, comma)` | 一个大数字，从 `start` 数到 `value` | `label` 在上，`note` 在下 |
| `define(K, term, keyword, cues, label, link, note, note_cue, fill)` | “X 是 Y”：名词加一张关键词大卡片 | `cues=(名词, 关键词)` |
| `versus(K, left, right, cues, mode)` | 两方对照 | 每方是 `(小标签, 大字, 说明)`；`mode="vs"` 并列，`"to"` 从左变到右 |
| `cards(K, items, title, title_cue, numbered)` | 并列的 2–6 样东西 | `items` 每项 `(名字, 说明, cue)` |
| `ask(K, question, cue, answer, answer_cue, label)` | 输入框里逐字打出一个问题 | `answer` 是随后出现的回答 |
| `stack(K, items, title, title_cue)` | 几层东西叠起来 | `items` 每项 `(文字, cue)` |

`charts.py`：

| 函数 | 画面 | 关键参数 |
| --- | --- | --- |
| `bars(K, items, unit, title, title_cue, highlight, decimals)` | 柱状图（竖屏是横条） | `items` 每项 `(名字, 数值, cue)`；`highlight` 是用强调色的那根 |
| `grid_fill(K, total, lit, cue, lit_cue, label, value, cols)` | 一片方格点亮其中一部分 | 表示“很多”或“占多少” |
| `steps(K, items, title, title_cue, current)` | 编号圆点连成的步骤链 | `items` 每项 `(步骤名, cue)` |
| `checklist(K, items, title, title_cue, mark)` | 清单，逐条打勾或打叉 | `mark="check"` 或 `"cross"` |
| `compare(K, heads, rows, head_cue)` | 两列对照表 | `rows` 每项 `(比什么, 左, 右, cue)`，可加第 5 项作为右边的时间 |

`backbone.py`（主线画面，放在顶部版面家具下面那一条，每镜都调用）：

| 函数 | 画面 | 适合 |
| --- | --- | --- |
| `tabs(K, labels, active)` | 几个小标签，讲到谁谁变实 | 两方或三方对比 |
| `rail(K, labels, cur, prev)` | 一条导轨，游标从上一镜的位置滑到这一镜 | 时间演进、流程 |
| `dots(K, total, cur)` | 一排小格子，表示第几条 | 清单要点 |

`tabs` 和 `dots` 返回 HTML 字符串，`rail` 返回 `(html, js)`，都可以直接放进 `join()`。

### 一镜放两块

```python
from scenes import big_number, headline, join


def frame_05():
    top, bottom = K.c.content.split_v(0.4, K.c.gap)        # 上 40%，下 60%
    return join(headline(K, ["价格降了多少"], ["@[价格]"], size="lg", box=top, p="a"),
                big_number(K, 90, "@[九成]", unit="%", box=bottom, p="b"))
```

区域的切法：`box.split_h(比例, 间距)` 左右切，`box.split_v(比例, 间距)` 上下切，`box.cols(n, 间距)`、`box.rows(n, 间距)` 等分，`box.inset(dx, dy)` 往里收。
横竖屏要用不同切法时看 `K.c.tall`（内容区偏竖时为真）：`a, b = box.split_v(0.5, g) if K.c.tall else box.split_h(0.5, g)`。

## 纵向排版 Flow

```python
from flow import Flow


def frame_06():
    f = Flow(K, K.c.content, align="left", valign="center")
    f.tag("k", "第二章").txt("h", "xl", "会看会听").space(20).em("kw", "lg", "多模态")
    f.para("s", "sm", "同一个模型，能看图、能听声音、能说话。", "muted")
    js = """
enter("#§k", 0.3); enter("#§h", @[会看] - 0.15); blk("#§kw", @[多模态] - 0.1); enter(".§s", @[同一个], 0.08);
"""
    return f.render(), js
```

`Flow(K, 区域, align, valign, gap)`，然后链式加内容：`.txt(id, 字号, 文字, 颜色)`、`.para(id, 字号, 一段话, 颜色)`（自动折行，每行带类 `§id`）、`.em(id, 字号, 强调词, 底色)`、`.tag(id, 文字, 底色)`、`.num(id, 字号, 数字, 单位)`、`.rule(id, 长度)`、`.space(像素)`、`.add(高度, 画在y处的函数)`。最后 `.render()`。
放不下时文字自动缩小、间距自动收紧。

## 单个积木

| 积木 | 说明 |
| --- | --- |
| `K.txt(id, 字号, 文字, x, y, w, align, tone)` | 一行字。给了 `w` 就保证不超宽，并在 `w` 内对齐 |
| `K.em(id, 字号, 文字, x, y, fill, w, align)` | 强调词。按风格渲染成色块、荧光笔、下划线或描边 |
| `K.tag(id, 文字, x, y, fill, align)` | 小标签 |
| `K.num(id, 字号, 数字, x, y, unit, w, align, tone)` | 大数字加单位，数字在 `#§id-v` 里 |
| `K.card(id, box, fill, inner, rot)` | 卡片。里面的内容用 `scenes.filled_card()` 排 |
| `K.rule(id, x, y, 长度, tone, vertical, thick)` | 线 |
| `K.bar(id, box, fill)`、`K.cells(prefix, x, y, cols, rows, size, gap)` | 柱子、方格阵 |
| `K.icon(id, name, x, y, size, tone)` | 线条图标：`check cross arrow down plus play` |
| `K.circle(id, cx, cy, r, fill, line, inner)` | 圆 |

- **id**：都写不带 `§` 的短名，生成时自动加上本镜前缀。JS 里选它要写 `"#§名字"`，类写 `".§名字"`。
- **字号**：档位名 `mega xl lg md sm xs label`，可带倍数如 `"mega*1.3"`。档位会按画幅换算：竖屏上大字缩小、小字略放大。
- **颜色**：色名 `ink`（主文字）`accent`（强调色）`accent2` `muted`（次要文字）`surface`（卡片底）`line` `bg` `on_accent`，以及调色板 `p0 p1 …`。
  - 要“彩色的字”用 `pop`：强调色够醒目就用强调色，否则自动退回主文字色。不要直接用 `accent` 写字，有的风格强调色是亮黄。
  - 放在色块上的字用 `K.on(底色名)` 取颜色。
  - JS 里要用实际色值时用 `K.hex("accent")`。
- **版面数据**：`K.c.content`（内容区）、`K.c.gap`（标准间距）、`K.c.tall`、`K.px(字号)`、`K.line_h(字号)`、`K.width(文字, 字号)`。

## 动画函数

每镜的 JS 里可以直接用，`tl` 是本镜的时间线。都用 `fromTo` 实现，按帧拖动时结果确定。

| 函数 | 效果 |
| --- | --- |
| `enter(sel, t, stagger, dur)` | 这种风格的默认入场（上移、弹出、落下、滑入或淡入，随风格变）。**优先用它** |
| `up(sel, t, dur, y)`、`drop(sel, t, dur, stagger)`、`slide(sel, t, dur, x, stagger)` | 上移、落下、滑入 |
| `fade(sel, t, dur)`、`pop(sel, t, dur, stagger)` | 淡入、弹出 |
| `wipe(sel, t, dur, origin, stagger)`、`grow(sel, t, dur, stagger, origin)` | 横向擦出、纵向长出 |
| `blk(sel, t)` | 强调词：先擦出底，再显出字 |
| `draw(sel, t, dur)` | 画出图标的线条，选择器写 `"#§id path"` |
| `count(sel, from, to, t, dur, fmt)` | 数字计数 |
| `type(sel, t, dur, n)` | 逐字打出，`n` 是字数 |
| `tint(sel, t, color, dur, stagger)`、`dim(sel, t, opacity)` | 变色、变暗 |

## 必须守的规则

1. **出现时机跟旁白走**。元素在说到它的那一刻出现，不要开场就铺满。
2. **不做退场**。元素出现后留到镜头结束，换镜交给转场。
3. **一镜一个主体**，其余元素明显小一号或颜色浅一档。
4. **只放旁白里说了的东西**。不加旁白没提的数据和结论；不把整句旁白印在画面上，字幕已经在说了。
5. **不用** `Math.random()`、`Date.now()`、`repeat: -1`、`yoyo`、网络请求。
6. **不直接写颜色值和字体名**，用色名和字号档位，否则换风格时这一镜不会跟着变。

`build_frames.py` 每次都会自检：元素横向出框、伸进字幕区、一行字缩到最小也放不下、一块区域里的内容放不下、动画选中了不存在的元素，都会报错并指出是哪一镜的哪个 id。

## 看画面

```bash
bash tools/snapshot.sh          # 每镜元素出齐的时刻各截一张，拼成 snapshots/contact-sheet.jpg
bash tools/snapshot.sh --mid    # 再加每镜中点，看动画进行到一半的样子
```

打开联系表这张图，重点找：

- 文字互相压住，或压在线和图标上。
- 主体偏在一角，另一半空着。
- 字被自动缩得太小（说明这一镜放的东西太多，拆镜或删内容）。
- 强调词、强调色用得太多，没有主次。
- 竖屏下一行字太长被缩小：把它拆成两行（`lines` 里多写一项）。

## 这条片子专用的东西

写在 `tools/theme.py` 里（`K` 下面），比如主线画面的固定参数、反复出现的组合：

```python
from backbone import rail
from project import make_kit

K = make_kit()
THEME = K.theme()

YEARS = ["2023", "2024", "2025", "2026"]


def year_rail(cur: int, prev: int | None = None):
    return rail(K, YEARS, cur, prev)
```

## 完全自己写主题

风格库里没有想要的风格、又不想往库里加时，`tools/theme.py` 可以不用 `K`，自己用 `framekit.Theme` 写全套 CSS 和小积木，镜头脚本返回手写的 `(html, js)`。`examples/genai-wave/` 就是这样写的。这样写的片子画幅固定，换比例要重排坐标。

## 往风格库里加一种风格

1. 在 `scripts/tools/styles/custom.py` 里照现有的写一个 `Style`，加进 `CUSTOM`。用到新字体先在 `fontlib.py` 的 `SOURCES` 里登记（先确认 `google/fonts` 仓库里有这个文件）。
2. `python3 scripts/audit_styles.py <新风格名>`：按对比度检查配色看不看得清，有问题会逐条列出要改哪个颜色。
3. `python3 scripts/gallery.py --out /tmp/gallery --styles <新风格名> --check`，打开 `/tmp/gallery/sheets/` 里的联系表，横屏竖屏都要看。
4. `PYTHONDONTWRITEBYTECODE=1 uv run -q --no-project --with pytest pytest scripts/tests -q -p no:cacheprovider`。
5. 更新总览图：`python3 scripts/gallery.py --out /tmp/gallery --overview`（全部风格重拍一遍，约 10 分钟），把输出的 `overview-*.jpg` 复制到 `assets/gallery/`，并在 `references/form-selection.md` 的风格表里加一行。
