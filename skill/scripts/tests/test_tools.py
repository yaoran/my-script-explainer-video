"""通用脚本里纯逻辑部分的测试。运行：PYTHONDONTWRITEBYTECODE=1 uv run -q --no-project --with pytest pytest scripts/tests -q -p no:cacheprovider"""
from __future__ import annotations

import importlib
import json
import sys
import types
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent
TOOLS = SCRIPTS / "tools"
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(SCRIPTS / "gallery"))

import build_captions  # noqa: E402
import build_frames  # noqa: E402
import build_index  # noqa: E402
import make_audio  # noqa: E402
import project  # noqa: E402
from canvas import CANVASES, Box, fit_px, get_canvas, text_w, wrap  # noqa: E402
from fontlib import font  # noqa: E402
from framekit import Font, Theme, cue_time, font_faces, locate_words, render_frame, resolve_cues  # noqa: E402
from stylekit import Kit  # noqa: E402
from styles import STYLES  # noqa: E402

TEXT = "写给 AI 的规矩，有人叫 Rule，有人叫 Skill。"
WORDS = [
    {"text": "写给", "start": 1.0, "end": 1.4},
    {"text": "AI", "start": 1.5, "end": 1.8},
    {"text": "的", "start": 1.8, "end": 1.9},
    {"text": "规矩", "start": 1.9, "end": 2.3},
    {"text": "有人", "start": 2.6, "end": 2.9},
    {"text": "叫", "start": 2.9, "end": 3.0},
    {"text": "Rule", "start": 3.0, "end": 3.4},
    {"text": "有人", "start": 3.7, "end": 4.0},
    {"text": "叫", "start": 4.0, "end": 4.1},
    {"text": "Skill", "start": 4.1, "end": 4.6},
]
THEME = Theme(
    fonts=(Font("Noto Sans SC", 700, "NotoSansSC.ttf"),),
    css="#root{color:#000;}\n",
    chrome=lambda n, total: f'<div class="page">{n:02d} / {total:02d}</div>',
    ground_class="bg",
)


# ---- 出现时机 ----

def test_cue_follows_original_text_not_tts_segmentation():
    out = resolve_cues("a(@[规矩]); b(@[矩]); c(@[Rule] - 0.1);", WORDS, 1, TEXT)
    assert out == "a(1.90); b(2.10); c(3.00 - 0.1);"


def test_cue_nth_occurrence_counts_in_text():
    assert resolve_cues("@[有人#2]", WORDS, 1, TEXT) == "3.70"
    assert resolve_cues("@[叫#2]", WORDS, 1, TEXT) == "4.00"


def test_cue_on_punctuation_takes_next_word():
    assert resolve_cues("@[，]", WORDS, 1, TEXT) == "2.60"


def test_cue_missing_names_frame_and_text():
    with pytest.raises(KeyError) as err:
        resolve_cues("@[不存在]", WORDS, 7, TEXT)
    assert "镜 7" in str(err.value) and "写给 AI" in str(err.value)


def test_cue_legacy_mode_needs_exact_word():
    assert resolve_cues("@[Rule]", WORDS, 1) == "3.00"
    with pytest.raises(KeyError):
        resolve_cues("@[矩]", WORDS, 1)


def test_locate_words_survives_a_word_the_engine_rewrote():
    located = locate_words("一共 3 个", [{"text": "一共", "start": 0, "end": 1}, {"text": "三", "start": 1, "end": 2},
                                       {"text": "个", "start": 2, "end": 3}])
    assert [w["at"] for w in located] == [0, 2, 5]
    assert cue_time("个", 1, "一共 3 个", located) == 2


# ---- 镜头文件 ----

def test_render_frame_prefixes_ids_and_pads_for_transition():
    page = render_frame(THEME, 3, 9, "demo", 5.0, '<div id="§a">x</div>', 'up("#§a", @[规矩]);', WORDS, text=TEXT, pad=0.5,
                        frame_css="--k-ink:#111;")
    assert 'id="f03-a"' in page and 'up("#f03-a", 1.90);' in page
    assert 'data-duration="5.5"' in page and "tl.set({}, {}, 5.5);" in page
    assert '[data-composition-id="03-demo"][data-composition-id]{--k-ink:#111;}' in page
    assert "03 / 09" in page and "§" not in page


def test_render_frame_ground_layer_carries_inline_style():
    page = render_frame(THEME, 1, 1, "x", 2.0, "", "", WORDS, "background-color:#FE90E8")
    assert 'class="bg clip" style="background-color:#FE90E8"' in page


def test_font_faces_use_registered_weight():
    assert "font-weight:700" in font_faces(THEME.fonts)


# ---- 画幅 ----

def test_aspect_aliases():
    assert get_canvas("竖屏").key == "9:16" and get_canvas("横屏").key == "16:9" and get_canvas("1080x1080").key == "1:1"
    with pytest.raises(SystemExit):
        get_canvas("21:9")


@pytest.mark.parametrize("key", list(CANVASES))
def test_canvas_zones_do_not_overlap(key):
    c = CANVASES[key]
    assert c.head_y < c.top < c.bottom < c.cap_top
    assert c.cap_top + c.cap_h <= c.h
    assert c.content.w > 0 and c.content.h > c.h * 0.45


def test_portrait_shrinks_big_type_and_enlarges_small_type():
    p, l = get_canvas("9:16"), get_canvas("16:9")
    assert l.sz(150) == 150 and l.sz(28) == 28
    assert p.sz(220) < 220 * 0.7 and p.sz(28) > 28


def test_fit_and_wrap_respect_width():
    assert fit_px("一二三四五六七八九十", 100, 500) == 50
    assert fit_px("短", 100, 500) == 100
    lines = wrap("每一次对话都生效，比如：不许泄露密钥。这是一段比较长的说明文字。", 40, 400)
    assert len(lines) > 1 and all(text_w(line, 40) <= 400 for line in lines)


def test_box_splits_cover_the_box():
    cols = Box(0, 0, 1000, 500).cols(3, 20)
    assert cols[0].x == 0 and cols[-1].r <= 1000 and cols[1].x == cols[0].r + 20


# ---- 风格 ----

@pytest.mark.parametrize("name", list(STYLES))
def test_every_style_builds_a_theme(name):
    kit = Kit(STYLES[name], get_canvas("16:9"), "标题")
    theme = kit.theme()
    assert theme.caption and theme.fonts and ".k-card" in theme.css
    assert all(f.url.startswith("https://") for f in theme.fonts)
    families = {f.family for f in theme.fonts}
    for face in (STYLES[name].display, STYLES[name].body, STYLES[name].tag_face):
        assert set(face.families) <= families


def test_pop_tone_falls_back_to_ink_when_accent_is_faint():
    kit = Kit(STYLES["blockframe"], get_canvas("16:9"))
    kit.begin(1)
    assert kit.hex("pop") == kit.hex("ink")
    assert Kit(STYLES["blue-professional"], get_canvas("16:9")).hex("pop") == "#1E2BFA"


def test_chapter_frame_switches_look():
    kit = Kit(STYLES["broadside"], get_canvas("16:9"))
    kit.begin(2, {"chapter": True})
    assert kit.ground_style() == "background-color:#E85D26" and "--k-ink:#111111" in kit.vars()
    kit.begin(3, {})
    assert kit.ground_style() == "" and "--k-ink:#F0ECE5" in kit.vars()


def test_static_font_takes_nearest_weight():
    assert font("Barlow", 800).weight in (700, 900)
    assert font("ZCOOL KuaiLe", 900).weight == 400


# ---- 现成画面：每种风格、每种画幅都不出框 ----

def draft_voices(frames):
    return {f["n"]: {"words": make_audio.draft_words(f["text"]), "duration_s": 9.0} for f in frames}


@pytest.mark.parametrize("aspect", list(CANVASES))
@pytest.mark.parametrize("name", list(STYLES))
def test_demo_frames_stay_inside_every_canvas(name, aspect, monkeypatch):
    kit = Kit(STYLES[name], get_canvas(aspect), "样张")
    fake = types.ModuleType("theme")
    fake.K, fake.THEME = kit, kit.theme()
    monkeypatch.setitem(sys.modules, "theme", fake)
    demo = importlib.reload(importlib.import_module("frames_demo"))
    frames = json.loads((SCRIPTS / "gallery/frames.json").read_text(encoding="utf-8"))
    voices = draft_voices(frames)
    for f in frames:
        kit.begin(f["n"], f)
        html, js = getattr(demo, f"frame_{f['n']:02d}")()
        assert build_frames.missing_targets(html, js) == [], f"镜 {f['n']}"
        assert build_frames.out_of_bounds(kit) == [], f"镜 {f['n']}"
        assert kit.issues == [], f"镜 {f['n']}"
        render_frame(fake.THEME, f["n"], len(frames), f["slug"], 9.0, html, js, voices[f["n"]]["words"], text=f["text"])


def test_missing_targets_reports_typos():
    assert build_frames.missing_targets('<div id="§a" class="x §grp"></div>', 'up("#§a", 1); pop(".§grp", 2); fade("#§b", 3);') == ["#§b"]


# ---- 字幕 ----

def test_caption_lines_break_at_punctuation_within_limit():
    text = "一分钟两百四十字，两分钟四百八十字，三分钟七百二十字。"
    lines = build_captions.caption_lines(text, 13)
    assert len(lines) == 3
    assert all(build_captions.width(text[s:e].rstrip(build_captions.TRAILING)) <= 13 for s, e in lines)


def test_long_clause_without_punctuation_splits_on_word_boundaries():
    text = "这是一句完全没有任何标点可以用来断行的非常长的旁白"
    starts = list(range(0, len(text), 2))
    lines = build_captions.caption_lines(text, 10, starts)
    assert len(lines) >= 3
    assert all(build_captions.width(text[s:e]) <= 10 for s, e in lines)
    assert "".join(text[s:e] for s, e in lines) == text


def test_caption_groups_keep_spaces_and_times():
    frames = [{"n": 1, "text": TEXT}]
    groups, total = build_captions.build_groups(frames, {1: {"words": WORDS, "duration_s": 6.0}}, 22)
    assert total == 6.0
    assert groups[0]["words"][0]["text"] == "写给 " and groups[0]["words"][0]["start"] == 1.0
    assert "".join(w["text"] for g in groups for w in g["words"]).replace("，", "") .startswith("写给 AI 的规矩")


def test_portrait_captions_are_narrower():
    assert build_captions.max_chars(get_canvas("9:16")) < build_captions.max_chars(get_canvas("16:9"))


# ---- 时间线和转场 ----

FRAMES = [{"n": 1, "slug": "a", "title": "a", "text": "x"}, {"n": 2, "slug": "b", "title": "b", "text": "x", "chapter": True},
          {"n": 3, "slug": "c", "title": "c", "text": "x"}, {"n": 4, "slug": "d", "title": "d", "text": "x", "transition": "cut"},
          {"n": 5, "slug": "e", "title": "e", "text": "x"}]
VOICES = {n: {"duration_s": 5.0} for n in range(1, 6)}


def test_timeline_picks_transition_by_frame_role_and_pads_the_outgoing_frame():
    plan = project.timeline(FRAMES, VOICES, {"transitions": {}}, STYLES["cobalt-grid"])
    assert [p["kind"] for p in plan] == ["cut", "push-slide", "crossfade", "cut", "blur-crossfade"]
    assert [p["pad"] for p in plan] == [0.5, 0.5, 0.0, 0.6, 0.0]
    assert [p["start"] for p in plan] == [0.0, 5.0, 10.0, 15.0, 20.0]


def test_video_json_overrides_style_transitions():
    plan = project.timeline(FRAMES, VOICES, {"transitions": {"inner": "cut", "chapter": "squeeze"}}, STYLES["cobalt-grid"])
    assert [p["kind"] for p in plan][:3] == ["cut", "squeeze", "cut"]


def test_parse_transition():
    assert project.parse_transition("push-slide UP 0.3") == ("push-slide", "UP", 0.3)
    assert project.parse_transition("cut") == ("cut", "", 0.0)
    with pytest.raises(SystemExit):
        project.parse_transition("wobble")


def test_transition_js_moves_in_the_right_direction():
    item = {"start": 5.0, "seconds": 0.5, "kind": "push-slide", "direction": "LEFT"}
    out_js, in_js = build_index.transition_js("01-a", "02-b", item, 1080, 1920)
    assert '"#el-01-a", { x: -1080' in out_js and '{ x: 1080, opacity: 1 }' in in_js
    item = {**item, "direction": "UP"}
    assert "y: -1920" in build_index.transition_js("01-a", "02-b", item, 1080, 1920)[0]


# ---- 配音 ----

def test_draft_words_are_all_findable_in_the_text():
    words = make_audio.draft_words(TEXT)
    assert [w["text"] for w in words][:3] == ["写给", "AI", "的规"]
    assert all(w["end"] > w["start"] for w in words)
    assert all(w["at"] >= 0 for w in locate_words(TEXT, words))


def test_cache_key_changes_with_text_voice_and_padding():
    base = {"n": 1, "text": "你好", "lead": 0.65, "tail": 0.95}
    key = make_audio.cache_key(base, "v", "+0%", False)
    assert key == make_audio.cache_key(dict(base), "v", "+0%", False)
    assert key != make_audio.cache_key({**base, "text": "你好。"}, "v", "+0%", False)
    assert key != make_audio.cache_key(base, "w", "+0%", False)
    assert key != make_audio.cache_key({**base, "tail": 2.8}, "v", "+0%", False)


# ---- 版面自检 ----

def test_overlong_line_and_overfull_block_are_reported():
    from flow import Flow

    kit = Kit(STYLES["cobalt-grid"], get_canvas("9:16"))
    kit.begin(1)
    kit.txt("long", "xl", "这是一行长到无论如何都放不进两百像素宽度里的标题文字", 0, 0, 200)
    assert any("§long" in msg for msg in kit.issues)
    kit.begin(2)
    flow = Flow(kit, Box(0, 0, 900, 200))
    for i in range(6):
        flow.txt(f"t{i}", "lg", "很多行")
    flow.render()
    assert any("放不下" in msg for msg in kit.issues)


def test_text_is_escaped_but_tail_html_is_kept():
    kit = Kit(STYLES["cobalt-grid"], get_canvas("16:9"))
    out = kit.txt("a", "md", "A&B <C>", 0, 0, tail='<span id="§x">是</span>')
    assert "A&amp;B &lt;C&gt;" in out and '<span id="§x">是</span>' in out


def test_headline_rejects_mismatched_cues():
    from scenes import headline

    with pytest.raises(ValueError):
        headline(Kit(STYLES["cobalt-grid"], get_canvas("16:9")), ["一行", "两行"], ["@[一]"])


# ---- 配色看得清 ----

@pytest.mark.parametrize("name", list(STYLES))
def test_style_colors_are_readable(name):
    sys.path.insert(0, str(SCRIPTS))
    import audit_styles

    assert audit_styles.style_problems(STYLES[name]) == []


def test_text_on_a_fill_is_picked_by_contrast():
    from colors import contrast, readable_on

    assert readable_on("#E85D4E", ("#FFFFFF", "#1A1A1A")) == "#1A1A1A"
    assert readable_on("#1F2BE0", ("#F0EBDE", "#1F2BE0")) == "#F0EBDE"
    assert round(contrast("#FFFFFF", "#000000"), 1) == 21.0
    assert contrast("rgba(0,0,0,0.5)", "#FFFFFF") < contrast("#000000", "#FFFFFF")


def test_traditional_kai_font_leaves_punctuation_to_the_next_font():
    faces = font_faces((font("LXGW WenKai TC", 700), font("Noto Sans SC", 700)))
    assert faces.count("unicode-range:U+0-2FFF,U+3040-FEFF;") == 1
