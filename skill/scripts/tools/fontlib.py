"""字体库：风格里用到的每个字体从哪里下载、西文平均字宽是多少。

全部取自 google/fonts 仓库的单个 TTF 文件。可变字体登记一个文件，字重由 build_fonts.py 钉死；
静态字体按字重各登记一个文件。新增字体前先确认仓库里有这个文件。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from urllib.parse import quote

from framekit import Font

GF = "https://raw.githubusercontent.com/google/fonts/main/ofl"
NOT_CJK_PUNCT = "U+0-2FFF,U+3040-FEFF"  # 除了中文标点（U+3000–303F）和全角符号（U+FF00–FFEF）以外的所有字符


@dataclass(frozen=True)
class Source:
    """一个字体家族的来源。files 的键是字重；键为 0 表示可变字体，一份文件覆盖所有字重。"""

    files: dict[int, str]
    latin: float = 0.58
    cjk: bool = False
    axes: dict[str, float] = field(default_factory=dict)
    centered_punct: bool = False  # 繁体字形的字体，逗号句号排在字框正中；标点改用后面的简体字体


def _vf(path: str, latin: float = 0.58, cjk: bool = False, **axes: float) -> Source:
    return Source({0: path}, latin, cjk, axes)


SOURCES: dict[str, Source] = {
    # 中文
    "Noto Sans SC": _vf("notosanssc/NotoSansSC[wght].ttf", cjk=True),
    "Noto Serif SC": _vf("notoserifsc/NotoSerifSC[wght].ttf", cjk=True),
    "ZCOOL XiaoWei": Source({400: "zcoolxiaowei/ZCOOLXiaoWei-Regular.ttf"}, cjk=True),
    "ZCOOL KuaiLe": Source({400: "zcoolkuaile/ZCOOLKuaiLe-Regular.ttf"}, cjk=True),
    "ZCOOL QingKe HuangYou": Source({400: "zcoolqingkehuangyou/ZCOOLQingKeHuangYou-Regular.ttf"}, latin=0.5, cjk=True),
    "Ma Shan Zheng": Source({400: "mashanzheng/MaShanZheng-Regular.ttf"}, cjk=True),
    "Long Cang": Source({400: "longcang/LongCang-Regular.ttf"}, cjk=True),
    "LXGW WenKai TC": Source({400: "lxgwwenkaitc/LXGWWenKaiTC-Regular.ttf", 700: "lxgwwenkaitc/LXGWWenKaiTC-Bold.ttf"}, cjk=True,
                             centered_punct=True),
    # 西文衬线
    "Newsreader": _vf("newsreader/Newsreader[opsz,wght].ttf", 0.5, opsz=60),
    "Instrument Serif": Source({400: "instrumentserif/InstrumentSerif-Regular.ttf"}, 0.46),
    "Libre Baskerville": _vf("librebaskerville/LibreBaskerville[wght].ttf", 0.6),
    "Bodoni Moda": _vf("bodonimoda/BodoniModa[opsz,wght].ttf", 0.56, opsz=28),
    "Playfair Display": _vf("playfairdisplay/PlayfairDisplay[wght].ttf", 0.54),
    "EB Garamond": _vf("ebgaramond/EBGaramond[wght].ttf", 0.48),
    "Source Serif 4": _vf("sourceserif4/SourceSerif4[opsz,wght].ttf", 0.54, opsz=48),
    "Cormorant Garamond": _vf("cormorantgaramond/CormorantGaramond[wght].ttf", 0.46),
    "DM Serif Display": Source({400: "dmserifdisplay/DMSerifDisplay-Regular.ttf"}, 0.54),
    "Shrikhand": Source({400: "shrikhand/Shrikhand-Regular.ttf"}, 0.64),
    # 西文无衬线
    "Inter": _vf("inter/Inter[opsz,wght].ttf", 0.6, opsz=32),
    "Hanken Grotesk": _vf("hankengrotesk/HankenGrotesk[wght].ttf", 0.56),
    "Space Grotesk": _vf("spacegrotesk/SpaceGrotesk[wght].ttf", 0.58),
    "Archivo": _vf("archivo/Archivo[wdth,wght].ttf", 0.58, wdth=100),
    "Archivo Black": Source({400: "archivoblack/ArchivoBlack-Regular.ttf"}, 0.68),
    "Barlow": Source({400: "barlow/Barlow-Regular.ttf", 700: "barlow/Barlow-Bold.ttf", 900: "barlow/Barlow-Black.ttf"}, 0.56),
    "Bebas Neue": Source({400: "bebasneue/BebasNeue-Regular.ttf"}, 0.42),
    "Oswald": _vf("oswald/Oswald[wght].ttf", 0.46),
    "Fredoka": _vf("fredoka/Fredoka[wdth,wght].ttf", 0.6, wdth=100),
    "Quicksand": _vf("quicksand/Quicksand[wght].ttf", 0.58),
    "Orbitron": _vf("orbitron/Orbitron[wght].ttf", 0.74),
    "Caveat": _vf("caveat/Caveat[wght].ttf", 0.42),
    # 等宽
    "DM Mono": Source({400: "dmmono/DMMono-Regular.ttf", 500: "dmmono/DMMono-Medium.ttf"}, 0.62),
    "JetBrains Mono": _vf("jetbrainsmono/JetBrainsMono[wght].ttf", 0.62),
    "IBM Plex Mono": Source({400: "ibmplexmono/IBMPlexMono-Regular.ttf", 500: "ibmplexmono/IBMPlexMono-Medium.ttf"}, 0.62),
    "Space Mono": Source({400: "spacemono/SpaceMono-Regular.ttf", 700: "spacemono/SpaceMono-Bold.ttf"}, 0.62),
}


def source(family: str) -> Source:
    if family not in SOURCES:
        raise KeyError(f"字体库里没有 {family!r}，先在 fontlib.py 的 SOURCES 里登记它的下载路径")
    return SOURCES[family]


def nearest_weight(family: str, weight: int) -> int:
    """静态字体只有登记过的字重，取最接近的；可变字体原样返回。"""
    files = source(family).files
    if 0 in files:
        return weight
    return min(files, key=lambda w: abs(w - weight))


def font(family: str, weight: int) -> Font:
    src = source(family)
    real = nearest_weight(family, weight)
    path = src.files.get(0) or src.files[real]
    return Font(family, real, path.rsplit("/", 1)[-1], f"{GF}/{quote(path)}", dict(src.axes),
                NOT_CJK_PUNCT if src.centered_punct else "")


def latin_width(family: str) -> float:
    return source(family).latin
