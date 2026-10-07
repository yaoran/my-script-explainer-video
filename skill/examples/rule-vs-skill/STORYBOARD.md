---
format: 1920x1080
duration: 32s
message: "所有对话都要守的写成 Rule，特定任务才用的写成 Skill"
arc: 钩子 → Rule 是底线 → Skill 是能力 → 一句话记住
audience: 刚开始给 AI 写规则和技能的人
mode: autonomous
structure: comparison（两方对比）
music: none
---

## Video direction

- palette system：blockframe 的五种糖果色轮流做满屏底色（粉、蓝、绿、黄），结构色只有黑、白、米白。Rule 一方固定用蓝，Skill 一方固定用绿。
- type：标题和关键词用 Inter 900 + 思源黑体 900；标签和页码用 Space Grotesk 600 大写。
- 版面家具：左上片名、右上页码；顶部两个标签（RULE / SKILL）是主线画面，讲到哪一方哪个变实，最后一镜两个都亮。
- motion grammar + reveal model：卡片带一点回弹弹出，文字上移淡入。每个元素在旁白说到它时出现。
- rhythm / held frames：每镜说完后静止约 1 秒；最后一镜留约 2.5 秒。
- negative list：不用圆角卡片、不用模糊投影、不加第六种颜色；不放任何 logo。
- 说明：`music: none` 只是让流程脚本不去曲库检索；配乐是程序合成的轻钢琴，在 audio_meta.json 里登记。

## Frame 1 — 开场：差在哪

- scene: 标题下两张歪着的卡片，一张写 Rule、一张写 Skill，右上角弹出“差在哪？”
- voiceover: "写给 AI 的规矩，有人叫 Rule，有人叫 Skill。它们到底差在哪？"
- duration: 7.48s
- transition_in: cut
- status: animated
- src: compositions/frames/01-hook.html
- type: hook
- persuasion: 提问钩子
- beat: 好奇
- blueprint: compose
- focal: Rule 和 Skill 两张卡
- roles: 两张卡 = foreground subject · “差在哪？”徽章 = supporting · 糖果色底 = background
- sfx: none

## Frame 2 — Rule 是底线

- scene: 左栏“Rule 是 底线”，右上一排对话格子全部点亮，右下“比如：不许泄露密钥”
- voiceover: "Rule 是底线。每一次对话都生效，比如：不许泄露密钥。"
- duration: 6.867s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/02-rule.html
- type: explain
- persuasion: 定义 + 例子
- beat: 明白
- blueprint: compose
- focal: “底线”关键词卡
- roles: 关键词卡 = foreground subject · 对话格子 = supporting · 例子卡 = supporting
- sfx: none

## Frame 3 — Skill 是能力

- scene: 和上一镜同构：左栏“Skill 是 能力”，右上一排格子只亮一个，右下“比如：做一条解说视频”
- voiceover: "Skill 是能力。遇到对应的任务，才会被调用，比如：做一条解说视频。"
- duration: 8.08s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/03-skill.html
- type: explain
- persuasion: 同构对比（全部亮 对 只亮一个）
- beat: 对上了
- blueprint: compose
- focal: “能力”关键词卡
- roles: 关键词卡 = foreground subject · 任务格子 = supporting · 例子卡 = supporting
- sfx: none

## Frame 4 — 一句话记住

- scene: 左右两张大卡并排：所有对话都要守的 → 写成 Rule；特定任务才用的 → 写成 Skill
- voiceover: "一句话记住：所有对话都要守的，写成 Rule；特定任务才用的，写成 Skill。"
- duration: 9.905s
- transition_in: crossfade
- status: animated
- src: compositions/frames/04-remember.html
- type: takeaway
- persuasion: 并排收束
- beat: 记住
- blueprint: compose
- focal: 两个“写成……”按钮
- roles: 两个按钮 = foreground subject · 两张卡的条件句 = supporting
- sfx: none
