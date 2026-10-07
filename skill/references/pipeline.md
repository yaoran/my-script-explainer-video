# 逐步命令和文件格式

`<技能>` 指本技能目录（`SKILL.md` 所在的目录）。第 1 步在任意位置运行，其余命令都在工程根目录下运行。
本技能只依赖 HyperFrames 的命令行（版本钉在 `scripts/HYPERFRAMES_VERSION`），不依赖别的技能目录里的脚本。

## 1. 体检和建工程

```bash
bash <技能>/scripts/doctor.sh                 # 命令、网络、字体缓存
bash <技能>/scripts/new_project.sh videos/<片名> --aspect 9:16 --style neon-night --title "<画面左上角的片名>"
```

体检通过但后面的步骤报了看不懂的错（比如换了机器、升了 HyperFrames 版本之后），先跑一次自检，它用占位配音把一套示例镜头从头建到浏览器检查，约半分钟：

```bash
python3 <技能>/scripts/gallery.py --out /tmp/selftest --styles cobalt-grid --aspects 16:9 --check
```

自检过了说明环境和脚本都没问题，问题在这条片子自己的文件里；自检不过，把它的报错原样告诉用户。

- `<片名>` 用英文短横线，取自选题，不用日期或序号。工程放在当前项目的 `videos/` 下。
- `--aspect`：`16:9` `9:16` `3:4` `1:1` `4:3`，也可以写 `横屏` `竖屏` `方形`。
- `--style`：风格名，清单见 `form-selection.md`。
- 之后要改：`.venv/bin/python tools/project.py set style=coral aspect=16:9 title="新片名"`；`project.py show` 看当前设定。

工程里的文件：

| 文件 | 内容 | 谁写 |
| --- | --- | --- |
| `user_script.txt` | 用户确认过的文稿，逐字 | 手写 |
| `tools/video.json` | 片名、画幅、风格、声音、转场、配乐 | `project.py set`，转场和配乐手改 |
| `tools/frames.json` | 逐镜的文案和留白 | 手写 |
| `tools/frames_*.py` | 逐镜的画面 | 手写 |
| `tools/theme.py` | 本片专用的积木（一般不用动） | 模板 |
| `tools/` 下其余文件 | 通用脚本，从技能复制来的 | 不改 |
| `audio_meta.json`、`assets/`、`compositions/`、`index.html` | 生成物 | 脚本 |

## 2. 写入文稿

`user_script.txt`：确认过的文稿，逐字，不带表格和时间。

`tools/frames.json`，每镜一条：

```json
[
  {"n": 1, "slug": "hook", "title": "开场", "lead": 1.1, "tail": 0.95, "text": "这一镜的旁白，从文稿逐字切出来。"},
  {"n": 2, "slug": "what-is-rule", "title": "Rule 是什么", "chapter": true, "lead": 1.1, "tail": 0.95, "text": "……"}
]
```

- `n`：从 1 连续编号。`slug`：英文短横线。`title`：给自己看的镜头名。
- `text`：这一镜的旁白。所有镜的 `text` 连起来应该等于 `user_script.txt`。
- `lead`：开口前的留白。首镜、章节镜、末镜 1.1 秒，其余 0.65 秒。
- `tail`：说完后的留白。0.95 秒，末镜 2.8 秒。
- `chapter`：章节镜标 `true`。
- 可选 `transition`（只改这一镜的进场转场）、`look`（指定这一镜用风格的第几套配色，0 是默认那套）。

`tools/video.json` 里可以手改的两项：

```json
{
  "transitions": {"chapter": "push-slide LEFT", "inner": "crossfade", "last": "blur-crossfade"},
  "bgm": {"mood": "calm", "volume": 0.16}
}
```

都可以不写，不写就用风格自带的。配乐气质：`calm` 轻钢琴、`warm` 慢而暖、`pulse` 轻快有律动、`zen` 五声音阶空灵、`none` 不要配乐。

## 3. 配音

```bash
.venv/bin/python tools/make_audio.py       # 逐镜配音，最后一行打印总时长
.venv/bin/python tools/make_bgm.py         # 生成配乐并登记
```

- 总时长和目标差得多时，调留白或回头增删文稿，**不要用 `--rate` 放慢来凑时长**。
- 文案、声音、留白都没变的镜头会沿用上次的结果，不重新合成；联网失败会自动重试三次。
- 换声音：`project.py set voice=zh-CN-XiaoxiaoNeural`，再重跑。先试听：`make_audio.py --voice <名字>` 只影响这一次。
- 没有网络或想先排画面：`make_audio.py --draft` 用占位时间，没有声音；出片前必须去掉 `--draft` 重跑。

## 4. 写镜头脚本

按 `frame-authoring.md` 写 `tools/frames_*.py`。

## 5. 重建和检查

```bash
bash tools/rebuild.sh            # 改了画面、风格或画幅
bash tools/rebuild.sh --audio    # 改了文案、声音或留白（会顺带重做配乐）
```

依次做：画面（带版面自检）→ 字幕 → 字体 → 主时间线 → 浏览器检查。任何一步失败都会停下来并说明原因。
检查要求 0 错误；字幕区被占、元素出框都算错误。信息级的 `content_overlap` 发生在转场那一瞬间两镜叠在一起，可以忽略。

常见报错：

| 报错 | 原因和处理 |
| --- | --- |
| `文案里找不到第 N 个 '词'` | `@[词]` 和这一镜的文案对不上，按报错里打印的文案改 |
| `§xx 横向出框` / `伸进字幕区` | 这一镜放的东西太多或手写的坐标超了；减内容，或改用现成画面 |
| `这行字太长` / `所在的区域放不下` | 这一镜的字太多；拆成两行、删字，或者把这一镜拆成两镜。竖屏下最常见 |
| `动画选中了不存在的元素` | JS 里的 id 写错了 |
| `这一行字幕超宽` | 一个词本身比一行还长（少见）；在文案里加逗号或换说法 |
| `这些字所有字体里都没有` | 生僻字或特殊符号；换一个字，或换风格 |
| 字体下载失败 | 网络问题；重跑，或手动把字体放到 `~/.cache/my-script-explainer-video/fonts/` |

然后看画面：

```bash
bash tools/snapshot.sh            # 输出 snapshots/contact-sheet.jpg
bash tools/snapshot.sh --mid      # 再加每镜中点
```

打开联系表这张图逐镜看，要找什么见 `frame-authoring.md` 的“看画面”。

## 6. 出片和验收

```bash
bash tools/hf.sh render --quality high --output renders/video.mp4
.venv/bin/python tools/verify_render.py
```

三分钟的片子渲染约 5–10 分钟，放后台跑。`verify_render.py` 检查画幅、时长、响度（目标 -16 LUFS）、意外静音，并输出 `renders/contact-sheet.jpg`。打开联系表，确认每镜画面完整、字幕在、和旁白对得上。

HyperFrames 的命令一律用 `bash tools/hf.sh <命令>` 来调，它会用工程里钉死的版本；直接敲 `npx hyperframes` 会用到最新版，表现可能不一样。

## 同一条片子出另一种比例

镜头脚本用的是现成画面和 `Flow` 时，不用改脚本：

```bash
.venv/bin/python tools/project.py set aspect=9:16
bash tools/rebuild.sh
bash tools/snapshot.sh                       # 竖屏一定要重新看一遍画面
bash tools/hf.sh render --quality high --output renders/video-9x16.mp4
.venv/bin/python tools/verify_render.py renders/video-9x16.mp4
```

配音不用重做。竖屏下常见的调整：一行太长的标题拆成两行；一镜里 4 张以上的卡片减到 3 张。
两版都要留的话，出完一版先把成片改名，再切比例。

## 换风格

```bash
.venv/bin/python tools/project.py set style=broadside
bash tools/rebuild.sh --audio     # 带 --audio 是为了让配乐换成新风格自带的气质；配音没变会沿用
bash tools/snapshot.sh
```

## 返修

| 用户要改 | 做法 |
| --- | --- |
| 某一镜的画面 | 改镜头脚本 → `rebuild.sh` → `snapshot.sh` → 出片 |
| 文案 | 改 `frames.json` 和 `user_script.txt` → `rebuild.sh --audio` → 出片。只有改过的镜头会重新配音 |
| 声音 | 先在 `renders/voice-samples/` 出同一段话的几种声音让用户挑，再 `project.py set voice=…` → `rebuild.sh --audio` → 出片 |
| 节奏太赶或太拖 | 调 `frames.json` 的 `lead` / `tail` → `rebuild.sh --audio` |
| 风格 / 比例 | 见上面两节 |
| 配乐 | 改 `video.json` 的 `bgm` → `rebuild.sh --audio` |

重新出片前把旧成片改名留底（如 `video-v1.mp4`）。

## 老工程

- 技能更新后想让老工程用上新脚本：`bash <技能>/scripts/sync_tools.sh <工程目录>`，再 `bash tools/rebuild.sh`。
- 2026 年 10 月 6 日之前建的工程（有 `STORYBOARD.md`、没有 `tools/video.json`）是旧流程，成片不受影响；要再改它，按 `examples/genai-wave/` 的样子补一个 `tools/video.json`、给 `theme.py` 加上字幕样式，再同步脚本。
