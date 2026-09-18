#!/usr/bin/env python3
"""subset_og_font.py -- Phase30-A3: 把 Noto Serif SC 子集化成分享图专用字体.

为什么需要子集化
    Noto Serif SC 完整版单个字重 11-12 MB, 入库不可接受; 分享图只用到固定的一小撮字
    (人名 / 时代 / 领域 / 标签 / 数字, 实测 ~2900 个码位), 子集化后只剩 ~800 KB.
    字体本身 (SIL OFL 1.1, 无 Reserved Font Name) 允许子集化与再分发, 条件是把许可证
    一起带上, 因此脚本会把 OFL 文本一起写进 tools/assets/fonts/.

产物 (构建期只读这几个文件, 不需要 fontTools)
    tools/assets/fonts/ProtrepticOgSerif-<Weight>.otf   子集字体
    tools/assets/fonts/coverage.json                   该子集覆盖的字符表 (供字形自检)
    tools/assets/fonts/OFL-NotoSerifSC.txt             许可证

谁来调用
    1) 人工/本地: python3 tools/subset_og_font.py
    2) tools/build_og_images.py: 发现排版用字没被覆盖时自动调 main(chars=...),
       现场重建 (CI 里新数据带来没见过的字是常态, 这样就不用人工干预).

用法
    python3 tools/subset_og_font.py                 # 两个字重, 按当前数据取字
    python3 tools/subset_og_font.py --weights bold  # 只做粗体
    python3 tools/subset_og_font.py --pad-top 0     # 不补高频字 (最小子集)
    python3 tools/subset_og_font.py --check         # 只自检当前子集是否覆盖排版用字

依赖: pip install fonttools (构建期工具, CI 的分享图步骤会一起装)
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import og_image  # noqa: E402

FONT_DIR = REPO / "tools" / "assets" / "fonts"
CACHE_DIR = FONT_DIR / ".cache"
SOURCE_URLS = {
    "regular": "https://cdn.jsdelivr.net/gh/notofonts/noto-cjk@main/Serif/SubsetOTF/SC/NotoSerifSC-Regular.otf",
    "bold": "https://cdn.jsdelivr.net/gh/notofonts/noto-cjk@main/Serif/SubsetOTF/SC/NotoSerifSC-Bold.otf",
}
LICENSE_URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/notoserifsc/OFL.txt"
# 排版会用到的标点/符号 (spec 文案之外还要显示的全角与半角符号)
EXTRA_PUNCT = "　 、。，；：？！“”‘’（）《》〈〉【】—…·×~!@#$%^&*()_+[]{}\\|;:'\",.<>/?`-=°′″№§"
CORPUS = REPO / "data" / "modes_data.json"
# 自动重建时的默认余量: 补入语料高频字, 让新数据里的常见字不必再重跑子集化
DEFAULT_PAD_TOP = 2500


def current_specs():
    """当前数据下所有分享图的文案规格 (与 build_og_images.py 同一份来源)."""
    index = og_image.load_json(REPO / "web" / "public" / "data" / "index.unified.json")
    meta_path = REPO / "web" / "public" / "data" / "meta.json"
    meta = og_image.load_json(meta_path) if meta_path.exists() else None
    return og_image.build_specs(index, meta, REPO / "web" / "public" / "templates")


def charset_for(specs, pad_top: int = 0) -> set:
    """给定 specs 需要的字符 = 排版用字 + 常用标点 + 全部可打印 ASCII (+ 高频字余量)."""
    chars = og_image.spec_chars(specs) | set(EXTRA_PUNCT) | {chr(c) for c in range(0x20, 0x7F)}
    if pad_top:
        chars |= corpus_frequent_chars(pad_top)
    return chars


def spec_charset(pad_top: int = 0) -> set:
    return charset_for(current_specs(), pad_top)


def corpus_frequent_chars(top: int) -> set:
    """从 data/modes_data.json 里按词频取前 N 个汉字, 为将来的新数据留余量."""
    if not CORPUS.exists():
        print("[subset] 警告: %s 不存在, 跳过高频字补足" % CORPUS)
        return set()
    counter = Counter()
    for ch in CORPUS.read_text(encoding="utf-8"):
        if "\u4e00" <= ch <= "\u9fff":
            counter[ch] += 1
    return {ch for ch, _ in counter.most_common(top)}


def ensure_source(weight: str, url: str) -> Path:
    path = CACHE_DIR / Path(url).name
    if path.exists() and path.stat().st_size > 1_000_000:
        return path
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    print("[subset] 下载源字体 %s" % url)
    with urllib.request.urlopen(url, timeout=180) as resp, path.open("wb") as fh:
        fh.write(resp.read())
    print("[subset] -> %s (%.1f MB)" % (path, path.stat().st_size / 1e6))
    return path


def ensure_license() -> Path:
    path = FONT_DIR / "OFL-NotoSerifSC.txt"
    if path.exists():
        return path
    with urllib.request.urlopen(LICENSE_URL, timeout=60) as resp:
        path.write_bytes(resp.read())
    return path


def build_one(weight: str, chars: set, source: Path) -> dict:
    from fontTools import subset

    out = FONT_DIR / ("ProtrepticOgSerif-%s.otf" % weight.capitalize())
    args = [
        str(source),
        "--text=%s" % "".join(sorted(chars)),
        "--output-file=%s" % out,
        "--no-hinting",
        "--desubroutinize",
        "--drop-tables+=GSUB,GPOS,GDEF,vhea,vmtx,VORG",
        "--name-IDs=*",
        "--notdef-outline",
        "--recalc-bounds",
    ]
    subset.main(args)
    return {"out": out, "bytes": out.stat().st_size}


def main(argv=None, chars=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--weights", default="regular,bold")
    ap.add_argument("--pad-top", type=int, default=DEFAULT_PAD_TOP,
                    help="额外补入 data/modes_data.json 的高频汉字数量 (留余量, 0 = 只用排版用字)")
    ap.add_argument("--check", action="store_true", help="只自检 coverage.json 与当前排版用字")
    args = ap.parse_args(argv)

    if chars is None:
        chars = spec_charset(args.pad_top)
    cov_path = FONT_DIR / "coverage.json"

    if args.check:
        if not cov_path.exists():
            print("[subset] coverage.json 缺失, 先跑一次本脚本")
            return 1
        covered = set(og_image.load_json(cov_path).get("chars") or "")
        missing = sorted(chars - covered)
        print("[subset] 排版用字 %d, 子集覆盖 %d, 缺 %d" % (len(chars), len(covered), len(missing)))
        if missing:
            print("[subset] 缺字: %s" % "".join(missing[:80]))
            return 1
        return 0

    FONT_DIR.mkdir(parents=True, exist_ok=True)
    ensure_license()
    from fontTools.ttLib import TTFont

    covered = set()
    for weight in [w.strip() for w in args.weights.split(",") if w.strip()]:
        if weight not in SOURCE_URLS:
            print("[subset] 未知字重: %s" % weight)
            return 1
        source = ensure_source(weight, SOURCE_URLS[weight])
        font = TTFont(source)
        cmap = set(font.getBestCmap().keys())
        missing_ord = sorted(ord(ch) for ch in chars if ord(ch) not in cmap)
        print("[subset] %s: 源字体码位 %d, 需要 %d, 源字体缺 %d 个"
              % (weight, len(cmap), len(chars), len(missing_ord)))
        if missing_ord:
            print("[subset] 源字体缺这些字符 (不会进图): %s" % "".join(chr(c) for c in missing_ord[:60]))
        usable = {ch for ch in chars if ord(ch) in cmap}
        info = build_one(weight, usable, source)
        print("[subset] %s -> %s (%.0f KB, 来自 %.1f MB 源字体)"
              % (weight, info["out"].name, info["bytes"] / 1024, source.stat().st_size / 1e6))
        covered |= usable

    cov_path.write_text(json.dumps({
        "schema": "protreptic.og_font_coverage/v1",
        "generator": "tools/subset_og_font.py",
        "source": SOURCE_URLS,
        "license": "SIL OFL 1.1 (OFL-NotoSerifSC.txt)",
        "chars": "".join(sorted(covered)),
        "count": len(covered),
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("[subset] coverage -> %s (%d 字符)" % (cov_path, len(covered)))

    missed = sorted(chars - covered)
    if missed:
        print("[subset] 警告: %d 个排版用字未被子集覆盖: %s" % (len(missed), "".join(missed[:60])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
