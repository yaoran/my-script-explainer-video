# my-script-explainer-video

把文案或选题做成无真人出镜的解说视频，包含配音、字幕、配乐和动效画面；支持五种画幅和二十一种风格。

## 使用前准备

- 输入：选题或已确认文稿、目标时长、画幅、风格和声音要求。
- 运行依赖：Node.js 18 及以上、npx、uv、FFmpeg/ffprobe；工程脚本会配置 edge-tts、numpy、fonttools、brotli。HyperFrames 的版本由 skill/scripts/HYPERFRAMES_VERSION 锁定。配音和首次下载字体需要联网。

## 产出

分镜、可编辑工程、带配音和字幕的 MP4、逐镜检查图及验收记录。

## 安装

本仓库为私有仓库，下载与安装需要有访问权限的 GitHub 账号。运行包位于 `skill/`，入口为 [skill/SKILL.md](skill/SKILL.md)。

本机手动安装：

```bash
gh repo clone yaoran/my-script-explainer-video
cd my-script-explainer-video
# 先确认目标没有已有同名 Skill；已有版本需核对后再更新。
mkdir -p "$HOME/.agents/skills/my-script-explainer-video"
rsync -a skill/ "$HOME/.agents/skills/my-script-explainer-video/"
```

也可以把下面这段话发给 Codex、Claude Code 或其他具备终端能力的 Agent：

```text
请从 https://github.com/yaoran/my-script-explainer-video 安装 my-script-explainer-video。
先确认 GitHub 账号有该私有仓库访问权限，核对现有同名 Skill，避免覆盖已有改动。
将 skill/ 运行包放入当前 Agent 的技能目录，检查 SKILL.md、引用文件和前置依赖，并报告实际安装位置。
```

Skills CLI 命令（需已有 Node.js/npx 和该仓库访问权限）：

```bash
npx skills add https://github.com/yaoran/my-script-explainer-video --skill my-script-explainer-video --global
```

## 调用示例

> 用 my-script-explainer-video 做一条 3 分钟的竖屏解说视频，讲 AI 如何改变工作；先给我文稿和展示形式。

## 使用边界

先确认文稿和展示形式，再制作。默认完成到成片；平台发布需要单独授权。

仓库提供 Skill 规则、所需脚本、模板和随包示例。密钥、个人视频、生成成片与运行依赖不随仓库分发；使用该 Skill 时仍需按实际环境检查工具和权限。
