---
format: 1920x1080
duration: 170s
message: "不到四年，生成式 AI 走了四步：会说话 → 会看会想 → 会动手 → 会上班；接下来比的是你会不会用"
arc: 钩子 → 2023 会说话 → 2024 会看会听会想 → 2025 会动手 → 2026 会上班 → 四步收束 + 落点
audience: 企业老板、经营决策者和非技术岗位的职场人
mode: autonomous
structure: story-explainer（按年份的时间线叙事）
music: none
---

## Video direction

- palette system：只用 frame.md 的两色——米色纸底（paper）+ 钴蓝墨（ink）。强调靠“钴蓝实心色块 + 米色反白字”，不引入第二种颜色；次要文字用 ink-soft，分隔线用 ink-faint。
- type：大标题与数字用 display（Newsreader + 思源宋体），小标与正文用 body（Hanken Grotesk + 思源黑体），日期、页码、标签用 mono（DM Mono）。层级靠字号，不靠加粗堆叠。
- 版面家具（每帧都有）：坐标纸网格、上下两条钴蓝细线、左上片名、右下页码；第 2–14 帧右上有一条年份导轨，游标从上一帧的位置滑到本帧的月份。
- motion grammar + reveal model：缓出长尾（power3），不回弹。每个元素在旁白说到它的那一刻出现，不提前铺满；数字用计数，柱子用生长，线条用擦出或自画。镜头不推不摇。
- rhythm / held frames：每帧最后一句说完后静止读秒；第 15 帧结尾留约 2.5 秒长静帧。章节帧（2、5、8、11）用左推转场，其余用叠化。
- negative list：不出现任何公司的真实 logo（产品名一律用文字）；不用圆角、投影、渐变和第二种色相；不做呼吸缩放、不做后半段慢推；不把整句旁白印在画面上（字幕条已经在说）。
- 说明：`music: none` 只是让流程脚本不去曲库检索；配乐用的是项目内程序合成的轻钢琴（assets/bgm/bgm.wav），在 audio_meta.json 里登记。

## Frame 1 — 开场：从聊天到上班

- scene: 左边一个“聊天”气泡，右边一块“上班”色块，下面画出 2023→2026.10 的时间轴，四段各留一个问号
- voiceover: "不到四年前，AI 还只会陪你聊天。今天，它已经能替你上班。从 2023 到 2026 年 10 月，这一波生成式 AI，到底是怎么走过来的？"
- duration: 13.08s
- poster: 10.5s
- transition_in: cut
- status: animated
- src: compositions/frames/01-hook.html
- type: hook
- persuasion: Before/after 对比 + Frame-then-fill（先给时间轴，再留问号）
- beat: 好奇 + 认同
- blueprint: compose
- focal: “聊天 → 上班”这组对比词
- roles: 聊天气泡 = foreground subject · 上班色块 = foreground subject · 时间轴与问号 = supporting · 坐标纸网格 = background
- sfx: none

narrativeRole: 用一个反差把观众拉进来，再把全片的骨架（一条四年的时间轴）摆出来。
keyMessage: 不到四年，AI 从陪聊走到了上班。

Scene 1 (0.0–4.1s): 气泡轮廓自画（SVG self-draw → svg-path-draw），“不到四年前”小标先到；旁白说到“聊天”时大字升起。左右分屏，左半。
Scene 2 (4.3–6.4s): “今天”带出一条横向箭头擦出，右侧钴蓝色块擦入，“上班”二字在旁白说到时落定。split-screen。
Scene 3 (6.8–9.1s): 下方时间轴自左向右擦出，2023/2024/2025/2026 四个刻度依次立起，“2026.10”标签收尾。full-width strip。
Scene 4 (9.2–13.1s): 轴下小标“生成式 AI · 这一波”出现；四段之间依次弹出问号方块；然后静止读秒。

## Frame 2 — 2023 会说话

- scene: 左栏大字 2023 和关键词“会说话”；右侧卡片里 ChatGPT：2 个月 → 1 亿用户，底下一排越长越高的像素柱
- voiceover: "2023 年，关键词：会说话。年初，ChatGPT 上线两个月，用户破亿，成了当时增长最快的应用。"
- duration: 10.942s
- poster: 8.8s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/02-2023-speak.html
- type: product_intro
- persuasion: Coined term（年度关键词）+ Statistical proof
- beat: 定向 + 惊讶
- blueprint: compose
- focal: 关键词色块“会说话”与“1 亿”计数
- roles: 2023 大数字 = foreground subject · 关键词色块 = foreground subject · ChatGPT 卡片 = supporting · 年份导轨 = supporting
- sfx: none

narrativeRole: 立起第一章，并用一个数字说明“会说话”有多快出圈。
keyMessage: 2023：AI 会说话了，两个月一亿用户。

Scene 1 (0.0–3.8s): 右上导轨游标落到 2023；大数字 2023 升起；“关键词”小标后，“会说话”色块擦入，旁边四根声波柱长出。asymmetric 45/55，左栏。
Scene 2 (3.9–6.8s): 右侧卡片淡入，“2023 · 年初”标签、ChatGPT 字样依次到；“上线 2 个月”随旁白出现。
Scene 3 (6.8–10.0s): 箭头擦出，“用户”与计数从 0 数到 1 亿（count-up → counting-dynamic-scale）；八根像素柱逐根长高（stat-bars-and-fills），“增长最快”色块落在末尾；静止。

## Frame 3 — GPT-4 与百模大战

- scene: 左边 GPT-4 大字和三张能力卡；右边“百模大战”标题、三行国产模型名和一块逐格点亮的 10×10 方阵
- voiceover: "三月，GPT-4 发布，能写文章、写代码、看懂图片。国内同时开打“百模大战”，文心一言、通义千问、讯飞星火接连登场。"
- duration: 12.955s
- poster: 10.4s
- transition_in: crossfade
- status: animated
- src: compositions/frames/03-gpt4-hundred-models.html
- type: feature_showcase
- persuasion: Rule of three + 数量具象化（100 个格子）
- beat: 理解 + 热闹
- blueprint: compose
- focal: GPT-4 大字 → 百模方阵
- roles: GPT-4 = foreground subject · 三张能力卡 = supporting · 百模方阵 = foreground subject · 三行模型名 = supporting
- sfx: none

narrativeRole: 同一个月，海外出了 GPT-4，国内一百个模型一起下场。
keyMessage: 模型能力上了台阶，国内同时开打百模大战。

Scene 1 (0.0–2.8s): “2023.03”标签先到；GPT-4 大字升起，下划线随“发布”擦出。asymmetric 50/50，左半。
Scene 2 (2.8–5.6s): 写文章 / 写代码 / 看懂图片三张卡按旁白逐张弹出（dynamic-content-sequencing）。
Scene 3 (6.1–12.0s): 右半“国内”小标、“百模大战”标题到；10×10 方阵从第一格起逐格点亮，贯穿这一段；文心一言、通义千问、讯飞星火三行依次升起；“100+”收尾后静止。

## Frame 4 — 人人学提问

- scene: 左边两张几乎一样的画，各贴一个“真？”“假？”；右边一个输入框里逐字打出“怎么提问”
- voiceover: "Midjourney 画的图，已经真假难辨。这一年，人人都在学一件事：怎么提问。"
- duration: 7.818s
- poster: 6.3s
- transition_in: crossfade
- status: animated
- src: compositions/frames/04-how-to-ask.html
- type: benefit_highlight
- persuasion: Common-belief vs reality（真假难辨）+ Distillation（一年学一件事）
- beat: 迟疑 → 清晰
- blueprint: compose
- focal: 输入框里的“怎么提问”
- roles: 两张画 = supporting · 输入框与逐字打出的四个字 = foreground subject
- sfx: none

narrativeRole: 把 2023 收成一句话：这一年大家学的是提问。
keyMessage: 2023 的全民技能是：怎么提问。

Scene 1 (0.0–3.3s): Midjourney 字样先到；两张画先后弹出；“真？”“假？”两块色块按旁白落下。asymmetric 45/55，左半。
Scene 2 (3.6–7.8s): 右侧输入框升起，“人人都在学”小标到；光标就位，“怎么提问”四个字逐字打出（type-on with caret → discrete-text-sequence）；静止。

## Frame 5 — 2024 会看会听会想

- scene: 左栏 2024 和三块关键词；右侧上下两张卡：Sora 把一段文字变成 1:00 的视频，GPT-4o 两排声波一来一回
- voiceover: "2024 年，关键词：会看、会听、会想。二月，Sora 用一段文字生成一分钟视频，震惊全网。五月，GPT-4o 能像真人一样实时对话。"
- duration: 15.08s
- poster: 12.1s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/05-2024-see-hear.html
- type: product_intro
- persuasion: Rule of three（会看 / 会听 / 会想）+ Demonstration
- beat: 定向 + 惊叹
- blueprint: compose
- focal: 三块关键词 → 两张事件卡
- roles: 2024 大数字 = foreground subject · 三块关键词 = foreground subject · Sora 卡 = supporting · GPT-4o 卡 = supporting
- sfx: none

narrativeRole: 立起第二章：AI 长出了眼睛、耳朵和脑子。
keyMessage: 2024：AI 会看、会听、会想。

Scene 1 (0.0–5.0s): 导轨游标滑到 2024；大数字升起；会看 / 会听 / 会想三块色块按旁白逐块擦入，各带一个小图标。左栏。
Scene 2 (5.3–10.0s): 上卡淡入：Sora 字样、文字卡、箭头、视频框依次到；计时从 0:00 数到 1:00；“震惊全网”色块落下。
Scene 3 (10.2–15.0s): 下卡淡入：GPT-4o 字样到；“人”“AI”两排声波柱先后长出（stat-bars-and-fills）；“实时对话”色块收尾，静止。

## Frame 6 — 价格战与先思考

- scene: 左卡是一排越来越矮的价格柱和“元、分、厘”；右卡是 o1 和“问题 → 思考 → 回答”的流程
- voiceover: "国内大模型打起价格战，调用成本降到了“厘”。九月，o1 出现，AI 开始先思考、再回答。"
- duration: 9.805s
- poster: 7.8s
- transition_in: crossfade
- status: animated
- src: compositions/frames/06-price-think.html
- type: feature_showcase
- persuasion: Before/after（元 → 分 → 厘）+ Causal chain（问题 → 思考 → 回答）
- beat: 理解
- blueprint: compose
- focal: “厘”色块与“思考”节点
- roles: 价格柱 = supporting · 元/分/厘 = foreground subject · o1 大字 = foreground subject · 三个流程节点 = supporting
- sfx: none

narrativeRole: 2024 的两件实事：用得起了，而且会先想再答。
keyMessage: 价格降到厘，模型学会先思考。

Scene 1 (0.0–4.5s): 左卡、“价格战”标题到；五根价格柱自高到低逐根长出；“元”“分”先后出现并被划掉，“厘”色块落定。split-screen，左半。
Scene 2 (4.7–8.9s): 右卡淡入，o1 大字升起；“问题”节点 → “先 · 思考”节点，六个小格逐格填满 → “再 · 回答”实心节点；静止。

## Frame 7 — 诺奖与基础设施

- scene: 左边两块奖牌牌匾连到“AI 相关研究”；右边“玩具”被划掉，箭头指向大色块“基础设施”和一排立柱
- voiceover: "十月，诺贝尔物理学奖和化学奖，都颁给了 AI 相关的研究。AI 从新鲜玩具，变成了基础设施。"
- duration: 9.955s
- poster: 8.0s
- transition_in: crossfade
- status: animated
- src: compositions/frames/07-nobel-infra.html
- type: social_proof
- persuasion: Citation（诺奖）+ Before/after（玩具 → 基础设施）
- beat: 信服 + 分量感
- blueprint: compose
- focal: “基础设施”大色块
- roles: 两块牌匾 = supporting · 连线与“AI 相关研究” = supporting · “基础设施”色块 = foreground subject · 立柱 = supporting
- sfx: none

narrativeRole: 用诺奖给这一年盖章，再给出 2024 的结论。
keyMessage: AI 不再是玩具，成了基础设施。

Scene 1 (0.0–5.5s): “2024.10”与“诺贝尔奖”到；物理学奖、化学奖两块牌匾按旁白弹出；两条连线画到“AI 相关研究”色块。split-screen，左半。
Scene 2 (6.1–10.0s): 右半“玩具”升起，随“变成”被一条线划掉，向下箭头长出；“基础设施”大色块擦入，九根立柱逐根长起；静止。

## Frame 8 — 2025 会动手

- scene: 左栏 2025 和“会动手”，一个鼠标指针点了一下；右卡 DeepSeek 三个标签，下面一片人头方格被点亮
- voiceover: "2025 年，关键词：会动手。春节，DeepSeek 横空出世，开源、便宜、还好用，让很多人第一次用上了会推理的 AI。"
- duration: 12.543s
- poster: 10.0s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/08-2025-deepseek.html
- type: product_intro
- persuasion: Coined term + Rule of three（开源 / 便宜 / 好用）
- beat: 定向 + 兴奋
- blueprint: compose
- focal: “会动手”色块 → DeepSeek 卡
- roles: 2025 大数字 = foreground subject · 关键词色块 = foreground subject · DeepSeek 卡 = supporting · 人头方格 = supporting
- sfx: none

narrativeRole: 立起第三章，并说明春节那一波为什么是全民级的。
keyMessage: 2025：AI 会动手了；DeepSeek 让很多人第一次用上会推理的 AI。

Scene 1 (0.0–3.8s): 导轨游标滑到 2025；大数字升起；“会动手”色块擦入，指针弹出并点击（cursor click + ripple → cursor-click-ripple）。左栏。
Scene 2 (3.9–8.5s): 右卡淡入，“2025 · 春节”、DeepSeek 字样到；开源 / 便宜 / 好用三个标签逐个弹出。
Scene 3 (8.7–12.5s): 60 个人头方格从左上起逐格点亮，“第一次用上”小标到，“会推理的 AI”色块收尾；静止。

## Frame 9 — 智能体出圈

- scene: 左边 Manus 和被三层方框向外扩散的“智能体”；右边一个编辑器窗口，代码一段一段地冒出来
- voiceover: "三月，Manus 刷屏，“智能体”这个词出了圈。Claude Code、Codex 这样的编程智能体，开始整段整段地替程序员写代码。"
- duration: 11.718s
- poster: 9.4s
- transition_in: crossfade
- status: animated
- src: compositions/frames/09-agents.html
- type: feature_showcase
- persuasion: Coined term（智能体出圈）+ Demonstration（代码整段出现）
- beat: 着迷
- blueprint: compose
- focal: “智能体”色块与扩散方框
- roles: Manus = supporting · “智能体”色块 + 三层方框 = foreground subject · 编辑器窗口 = foreground subject · 代码条 = supporting
- sfx: none

narrativeRole: “智能体”从一个产品词变成了大众词，并且先在写代码上落了地。
keyMessage: 智能体出圈，编程智能体开始整段写代码。

Scene 1 (0.0–4.2s): “2025.03”、Manus 到；“智能体”色块擦入；说到“出了圈”时三层方框由内向外扩开（center-outward-expansion）。asymmetric 45/55，左半。
Scene 2 (4.4–11.7s): 编辑器淡入，Claude Code、Codex 两个标签先后弹出；状态行“编程智能体 · 写入中”到；四段代码条按旁白一段一段擦出；静止。

## Frame 10 — 智能体元年

- scene: 左边 GPT-5 和“图片”“视频”两张卡贴着“以假乱真”；右边“智能体元年”，“建议”被划掉，旁边清单逐项打勾
- voiceover: "八月，GPT-5 发布；图片和视频生成，也到了以假乱真的程度。这一年被叫做“智能体元年”：AI 不再只给建议，它开始自己把事做完。"
- duration: 13.23s
- poster: 10.6s
- transition_in: crossfade
- status: animated
- src: compositions/frames/10-agent-year.html
- type: branding
- persuasion: Coined term（智能体元年）+ Before/after（建议 → 做完）
- beat: 确信
- blueprint: compose
- focal: “智能体元年”与打勾的清单
- roles: GPT-5 = supporting · 两张卡 = supporting · “智能体元年”标题 = foreground subject · 清单 = foreground subject
- sfx: none

narrativeRole: 给 2025 下结论：从给建议变成把事做完。
keyMessage: 2025 是智能体元年：AI 开始自己把事做完。

Scene 1 (0.0–6.2s): “2025.08”、GPT-5 大字到；图片、视频两张卡先后弹出；“以假乱真”色块落下。split-screen，左半。
Scene 2 (6.6–8.7s): 右半“这一年”小标、“智能体元年”标题升起，下划线擦出。
Scene 3 (8.7–13.2s): “建议”气泡弹出后被划掉；箭头指向清单，三项依次打勾（svg-path-draw）；“把事做完”色块收尾，静止。

## Frame 11 — 2026 会上班

- scene: 左栏 2026 和“会上班”，旁边一张工牌；右卡 OpenClaw：100 天 → 250,000 颗星，底下“全民养龙虾”
- voiceover: "2026 年，关键词：会上班。一月，开源智能体 OpenClaw 爆火，一百天拿下二十五万颗星，全民“养龙虾”。"
- duration: 10.792s
- poster: 8.6s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/11-2026-openclaw.html
- type: product_intro
- persuasion: Coined term + Statistical proof（100 天 → 25 万）
- beat: 定向 + 震动
- blueprint: compose
- focal: “会上班”色块 → 250,000 计数
- roles: 2026 大数字 = foreground subject · 关键词色块 = foreground subject · OpenClaw 卡与计数 = foreground subject · 工牌 = supporting
- sfx: none

narrativeRole: 立起第四章，并给出今年开年最响的一个数字。
keyMessage: 2026：AI 会上班了；OpenClaw 一百天二十五万星。

Scene 1 (0.0–3.8s): 导轨游标滑到 2026；大数字升起；“会上班”色块擦入，工牌弹出。左栏。
Scene 2 (3.9–6.6s): 右卡淡入，“2026.01”、“开源智能体”、OpenClaw 字样依次到。
Scene 3 (6.7–10.7s): “100 天”升起，箭头擦出，计数从 0 数到 250,000（count-up → counting-dynamic-scale），星形弹出；“全民养龙虾”色块收尾，静止。

## Frame 12 — 大厂跟进

- scene: 左边三栋楼依次拔起；右边 WorkBuddy：手机里一句“发句话”，虚线连到电脑，屏幕上三项任务逐个打勾
- voiceover: "大厂迅速跟进。三月，腾讯推出 WorkBuddy，在微信里发句话，电脑就能干活。"
- duration: 8.405s
- poster: 6.7s
- transition_in: crossfade
- status: animated
- src: compositions/frames/12-workbuddy.html
- type: feature_showcase
- persuasion: Demonstration（手机发话 → 电脑干活）
- beat: “原来这么用”
- blueprint: compose
- focal: 手机 → 电脑这条链路
- roles: 三栋楼 = supporting · WorkBuddy 字样 = supporting · 手机、虚线、电脑 = foreground subject
- sfx: none

narrativeRole: 大厂跟进之后，这件事离普通人有多近。
keyMessage: 在微信里发句话，电脑就能干活。

Scene 1 (0.0–2.1s): “大厂跟进”到，三栋像素楼按旁白逐栋长起。asymmetric 35/65，左侧。
Scene 2 (2.4–4.5s): “2026.03 · 腾讯”标签、WorkBuddy 字样到。
Scene 3 (4.7–8.4s): 手机弹出，“发句话”色块落进手机；虚线擦到电脑，电脑弹出，三项任务依次打勾；静止。

## Frame 13 — 合成一个应用，周活十亿

- scene: 左边 Codex 小块滑进 ChatGPT 的大框，框里三行合成“一个应用”；右边巨大的“10 亿”从 0 数上来
- voiceover: "七月，Codex 并入 ChatGPT，聊天、办公、写代码合成一个应用，周活跃用户突破十亿。"
- duration: 9.555s
- poster: 7.6s
- transition_in: crossfade
- status: animated
- src: compositions/frames/13-chatgpt-billion.html
- type: social_proof
- persuasion: Demonstration（并入）+ Statistical proof（10 亿）
- beat: 分量感
- blueprint: compose
- focal: “10 亿”计数
- roles: Codex 小块与 ChatGPT 大框 = supporting · 三行功能 = supporting · “10 亿” = foreground subject
- sfx: none

narrativeRole: 说明今年夏天的两件事：产品合一，用户到十亿。
keyMessage: 聊天、办公、写代码合成一个应用，周活十亿。

Scene 1 (0.0–3.1s): “2026.07”到；Codex 实心块弹出，随“并入”滑进刚淡入的 ChatGPT 大框（card-morph-anchor 的位移部分）。asymmetric 50/50，左半。
Scene 2 (3.3–6.5s): 聊天 / 办公 / 写代码三行逐行弹出，“一个应用”色块落下。
Scene 3 (6.7–9.5s): 右半“周活跃用户”小标到，数字从 0 数到 10 并放大（counting-dynamic-scale），底线擦出，小字到；静止。

## Frame 14 — 从工具到同事

- scene: 左边三张模型卡叠着落下再挤成一堆；右边“工具”被划掉，箭头指向大色块“同事”和一张工牌
- voiceover: "九月，GPT-6、Gemini 4、新一代 Claude 扎堆发布。AI 从工具，变成了同事。"
- duration: 9.143s
- poster: 7.3s
- transition_in: crossfade
- status: animated
- src: compositions/frames/14-colleague.html
- type: benefit_highlight
- persuasion: Rule of three + Before/after（工具 → 同事）
- beat: 笃定
- blueprint: compose
- focal: “同事”大色块
- roles: 三张模型卡 = supporting · “工具” = supporting · “同事”色块与工牌 = foreground subject
- sfx: none

narrativeRole: 给 2026 下结论，也是全片的转折落点。
keyMessage: AI 从工具变成了同事。

Scene 1 (0.0–5.7s): “2026.09”到；GPT-6、Gemini 4、新一代 Claude 三张卡按旁白逐张落下；说到“扎堆”时上下两张向中间挤，“扎堆发布”色块落下。asymmetric 50/50，左半。
Scene 2 (6.1–9.1s): 右半“工具”升起，被划掉，向下箭头长出；“同事”大色块擦入，工牌弹出；静止。

## Frame 15 — 四步与落点

- scene: 四级越来越高的台阶，每级写着年份和关键词；然后台阶缩到左上角，下面打出“AI 能不能”被划掉、“你会不会用？”
- voiceover: "不到四年，四步：会说话，会看会想，会动手，会上班。接下来的问题，不再是 AI 能不能，而是你会不会用。"
- duration: 13.505s
- poster: 10.8s
- transition_in: blur-crossfade
- status: animated
- src: compositions/frames/15-four-steps.html
- type: cta
- persuasion: Callback（回到开场的时间轴）+ Distillation
- beat: 了然 + 被点名
- blueprint: compose
- focal: 收尾大字“你会不会用？”
- roles: 四级台阶 = foreground subject（前半）→ supporting（后半）· “AI 能不能” = supporting · “你会不会用？” = foreground subject · 方格图章 = supporting
- sfx: none

narrativeRole: 把四年压成四步，再把问题交还给观众。
keyMessage: 接下来比的不是 AI 能不能，而是你会不会用。

Scene 1 (0.0–6.1s): “不到四年 · 四步”小标先到；四级台阶按旁白逐级长高，每级顶上落下年份和关键词（stat-bars-and-fills）。full-width strip。
Scene 2 (6.4–9.6s): 台阶整体缩到左上并变淡（scale-swap-transition 的让位动作）；“接下来的问题”小标、“AI 能不能”升起，随后被划掉。
Scene 3 (9.7–13.5s): “你会不会用？”大字升起并定住；最后留约 2.5 秒静止读秒（全片唯一的长静帧）。
