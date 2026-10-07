# 这个工程怎么改

这是用技能 `my-script-explainer-video` 做的解说视频工程。要改画面、文案、声音、风格或画幅，先调用这个技能，按它的流程来。
不要走 `hyperframes` 入口技能的意图访谈，也不要手改 `index.html` 和 `compositions/` 下的文件，它们都是生成的。

- 文案和每镜留白：`tools/frames.json`
- 片名、画幅、风格、声音、转场、配乐：`tools/video.json`（用 `.venv/bin/python tools/project.py set …` 改）
- 每镜的画面：`tools/frames_*.py`
- 改完重建：`bash tools/rebuild.sh`（改了文案或声音加 `--audio`）
- 看画面：`bash tools/snapshot.sh`，再打开 `snapshots/contact-sheet.jpg`
- 出片：`bash tools/hf.sh render --quality high --output renders/video.mp4`，然后 `.venv/bin/python tools/verify_render.py`
