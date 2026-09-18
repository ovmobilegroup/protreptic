#!/usr/bin/env python3
"""build_og_images.py -- Phase30-A3: 构建期生成 1200x630 社交分享图 (og:image).

背景
    GitHub Pages 上没有服务端, 分享图只能在构建期画出来. 本脚本用 Pillow 直接把
    index.unified.json / meta.json / 模板 markdown 里的真实字段画成 PNG:
      /minds/{code}       人物: 姓名 + 模式数 + 时代 (再加一句真实描述)
      /figures/{code}     场景: 名称 + 领域 + 关联模式数 (再加一句真实描述)
      /templates/{id}     模板: 标题
      /figures /modes /templates /api   列表页: 标题 + 规模数字 + 一句说明
      站点首页             一张总图
    「哪条路由用哪张图」的规则在 tools/og_image.py 里, 与 tools/prerender_routes.py
    以及前端 web/src/composables/useSeo.ts 共用同一套契约.

顺序 (CI 与本地一致)
    python3 tools/export_static_site.py
    python3 tools/build_unified_index.py
    cd web && VITE_DATA_MODE=static npm run build      # 先有 web/dist
    python3 tools/build_og_images.py                   # 本脚本: 读 dist/data, 写 dist/og
    python3 tools/prerender_routes.py                  # 读 dist/og/manifest.json 写 og:image

自检 (任一不过直接非 0 退出)
    1) 排版用字必须被 tools/assets/fonts/coverage.json 覆盖 —— 否则图上会出现豆腐块
    2) 逐张确认 PNG 落盘、魔数正确、尺寸 1200x630、体积合理
    3) 图片数量与 index.unified.json 的名录条数对齐

体积
    1200x630 真彩 PNG 单张 50-90 KB, 796 张不可接受; 分享图只有大面积平色 + 一层径向光晕,
    所以统一做 96 色中位切分 + Floyd-Steinberg 抖动, 单张降到 ~20 KB (肉眼无差).

用法
    python3 tools/build_og_images.py
    python3 tools/build_og_images.py --limit 8        # 只画前 8 张 (调版式用)
    python3 tools/build_og_images.py --only site,minds/H-WYM-001,figures/A-1-X-P
    python3 tools/build_og_images.py --colors 128 --dry-run
"""

from __future__ import annotations

import argparse
import json
import struct
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import og_image  # noqa: E402

FONT_DIR = REPO / "tools" / "assets" / "fonts"
FONTS = {
    "bold": FONT_DIR / "ProtrepticOgSerif-Bold.otf",
    "regular": FONT_DIR / "ProtrepticOgSerif-Regular.otf",
}
COVERAGE = FONT_DIR / "coverage.json"

W, H = og_image.OG_WIDTH, og_image.OG_HEIGHT
MARGIN = 88
LEFT_MAX = 862
TITLE_TOP = 196
FOOTER_RULE_Y = 540
FOOTER_TEXT_Y = 562
SEAL = (912, 196, 1112, 396)
CHIP_HEIGHT = 58

INK = (4, 6, 12)
GOLD_200 = (247, 230, 192)
GOLD_300 = (240, 215, 159)
GOLD_400 = (228, 189, 116)
GOLD_500 = (212, 162, 76)
JADE_300 = (143, 240, 221)
JADE_400 = (94, 234, 212)
PARCHMENT = (243, 236, 224)


def blend(color, alpha, bg=INK):
    return tuple(int(round(c * alpha + b * (1 - alpha))) for c, b in zip(color, bg))


def add_glow(img: Image.Image, center, radius: float, color, alpha: float) -> None:
    """低分辨率算 alpha 再双三次放大: 逐像素的 python 循环只跑 96x52 次."""
    gw, gh = 96, 52
    mask = Image.new("L", (gw, gh))
    px = mask.load()
    cx0, cy0 = center
    for y in range(gh):
        cy = (y + 0.5) / gh * H - cy0
        for x in range(gw):
            cx = (x + 0.5) / gw * W - cx0
            d = ((cx * cx + cy * cy) ** 0.5) / radius
            v = 0.0 if d >= 1 else (1.0 - d) ** 2.2
            px[x, y] = int(255 * alpha * v)
    mask = mask.resize((W, H), Image.BICUBIC)
    layer = Image.new("RGBA", img.size, color + (0,))
    layer.putalpha(mask)
    img.alpha_composite(layer)


def letterspaced(draw: ImageDraw.ImageDraw, xy, text: str, font, fill, spacing: float) -> float:
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + spacing
    return x - spacing


def wrap(draw, text: str, font, max_w: float) -> list:
    """有空格就按词折行 (拉丁人名/英文短语), 否则逐字折行 (中文)."""
    if " " in text.strip():
        words, sep = text.split(), " "
    else:
        words, sep = list(text), ""
    lines, cur = [], ""
    for word in words:
        cand = (cur + sep + word) if cur else word
        if draw.textlength(cand, font=font) <= max_w or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_title(draw, text: str, max_w: float, hi: int = 68, lo: int = 44, max_lines: int = 2):
    for size in range(hi, lo - 1, -2):
        font = ImageFont.truetype(str(FONTS["bold"]), size)
        lines = wrap(draw, text, font, max_w)
        if len(lines) <= max_lines:
            return font, lines, size
    font = ImageFont.truetype(str(FONTS["bold"]), lo)
    lines = wrap(draw, text, font, max_w)[:max_lines]
    lines[-1] = lines[-1][:-1] + "…"
    return font, lines, lo


def ellipsize(draw, text: str, font, max_w: float) -> str:
    if draw.textlength(text, font=font) <= max_w:
        return text
    while text and draw.textlength(text + "…", font=font) > max_w:
        text = text[:-1]
    return text + "…"


def draw_chips(draw, x, y, chips, max_right: float) -> int:
    font = ImageFont.truetype(str(FONTS["regular"]), 26)
    pad_x, gap = 22, 14
    cursor = x
    for chip in chips:
        text = ellipsize(draw, chip, font, 330)
        width = draw.textlength(text, font=font) + pad_x * 2
        if cursor + width > max_right:
            draw.text((cursor, y + 4), "…", font=font, fill=blend(GOLD_300, 0.7))
            break
        draw.rounded_rectangle((cursor, y, cursor + width, y + CHIP_HEIGHT), radius=CHIP_HEIGHT // 2,
                               fill=blend(GOLD_400, 0.08), outline=blend(GOLD_500, 0.38), width=2)
        draw.text((cursor + pad_x, y + (CHIP_HEIGHT - 34) / 2), text, font=font,
                  fill=blend(GOLD_200, 0.94))
        cursor += width + gap
    return y + CHIP_HEIGHT


def draw_seal(draw: ImageDraw.ImageDraw, char: str, center_y: float) -> None:
    half = (SEAL[2] - SEAL[0]) / 2
    cy = min(max(center_y, 150 + half), FOOTER_RULE_Y - 120 - half)
    x0, x1 = SEAL[0], SEAL[2]
    y0, y1 = cy - half, cy + half
    draw.rounded_rectangle((x0, y0, x1, y1), radius=26, fill=blend(GOLD_500, 0.06),
                           outline=blend(GOLD_500, 0.36), width=3)
    draw.rounded_rectangle((x0 + 12, y0 + 12, x1 - 12, y1 - 12), radius=18,
                           outline=blend(GOLD_500, 0.18), width=1)
    if char:
        font = ImageFont.truetype(str(FONTS["bold"]), 104)
        draw.text(((x0 + x1) / 2, (y0 + y1) / 2 - 4), char, font=font,
                  fill=blend(GOLD_300, 0.92), anchor="mm")
    draw.rectangle((x0 + 40, y1 - 26, x1 - 40, y1 - 22), fill=blend(GOLD_500, 0.32))


def draw_corner_ticks(draw: ImageDraw.ImageDraw) -> None:
    inset, arm = 30, 56
    color = blend(GOLD_500, 0.55)
    for (x, y), (dx, dy) in (
        ((inset, inset), (1, 1)), ((W - inset, inset), (-1, 1)),
        ((inset, H - inset), (1, -1)), ((W - inset, H - inset), (-1, -1)),
    ):
        draw.line((x, y, x + dx * arm, y), fill=color, width=2)
        draw.line((x, y, x, y + dy * arm), fill=color, width=2)


def render(spec: dict) -> Image.Image:
    img = Image.new("RGBA", (W, H), INK + (255,))
    add_glow(img, (150, 30), 760, GOLD_500, 0.16)
    add_glow(img, (1160, 690), 780, JADE_400, 0.11)
    add_glow(img, (1010, 300), 420, GOLD_400, 0.07)
    draw = ImageDraw.Draw(img)
    draw_corner_ticks(draw)

    # 顶部字标
    word_font = ImageFont.truetype(str(FONTS["bold"]), 30)
    next_x = letterspaced(draw, (MARGIN, 58), "PROTREPTIC", word_font, blend(GOLD_300, 0.95), 3.4)
    draw.text((next_x + 20, 64), "· 思想典藏", font=ImageFont.truetype(str(FONTS["regular"]), 24),
              fill=blend(JADE_300, 0.85))

    # 类别行
    letterspaced(draw, (MARGIN, 134), spec["kicker"],
                 ImageFont.truetype(str(FONTS["regular"]), 25), blend(PARCHMENT, 0.78), 1.6)

    # 标题 (自适应字号, 最多两行)
    title_font, lines, size = fit_title(draw, spec["title"], LEFT_MAX - MARGIN)
    line_h = round(size * 1.2)
    y = TITLE_TOP
    title_color = blend(GOLD_200, 0.98) if spec["kind"] == "site" else blend(PARCHMENT, 0.97)
    for line in lines:
        draw.text((MARGIN, y), line, font=title_font, fill=title_color)
        y += line_h
    cursor = y - line_h + size + 16  # 标题块下沿 + 空隙

    if spec.get("subtitle"):
        sub_font = ImageFont.truetype(str(FONTS["regular"]), 28)
        draw.text((MARGIN, cursor), ellipsize(draw, spec["subtitle"], sub_font, LEFT_MAX - MARGIN),
                  font=sub_font, fill=blend(PARCHMENT, 0.74))
        cursor += 46

    # 分隔线 (金线 + 玉点): 明确是设计元素, 不是残留的下划线
    div_y = cursor + 20
    draw.rectangle((MARGIN, div_y, MARGIN + 120, div_y + 4), fill=blend(GOLD_500, 0.62))
    draw.polygon([(MARGIN + 138, div_y + 2), (MARGIN + 146, div_y - 6),
                  (MARGIN + 154, div_y + 2), (MARGIN + 146, div_y + 10)], fill=blend(JADE_300, 0.85))

    chips_bottom = draw_chips(draw, MARGIN, div_y + 34, spec.get("chips") or [], LEFT_MAX)

    # 摘要: 只在剩余空间够时画 (两行标题 + 副题时自然不画, 避免压到页脚)
    summary = spec.get("summary") or ""
    avail = FOOTER_RULE_Y - 16 - (chips_bottom + 20)
    if summary and avail >= 34:
        sfont = ImageFont.truetype(str(FONTS["regular"]), 27)
        line_h_s = 37
        max_lines = max(1, min(2, avail // line_h_s))
        s_lines = wrap(draw, summary, sfont, LEFT_MAX - MARGIN)
        if len(s_lines) > max_lines:
            s_lines = s_lines[:max_lines]
            s_lines[-1] = ellipsize(draw, s_lines[-1], sfont, LEFT_MAX - MARGIN - 24)
        for i, line in enumerate(s_lines):
            draw.text((MARGIN, chips_bottom + 20 + i * line_h_s), line, font=sfont,
                      fill=blend(PARCHMENT, 0.72))

    draw_seal(draw, spec.get("seal") or "", (TITLE_TOP + chips_bottom) / 2)

    # 页脚: 发丝线 + 站点地址 + 编码
    draw.rectangle((MARGIN, FOOTER_RULE_Y, W - MARGIN, FOOTER_RULE_Y + 1),
                   fill=blend(GOLD_500, 0.18))
    draw.text((MARGIN, FOOTER_TEXT_Y), og_image.SITE_HOST_LABEL,
              font=ImageFont.truetype(str(FONTS["regular"]), 23), fill=blend(PARCHMENT, 0.76))
    if spec.get("code"):
        draw.text((W - MARGIN, FOOTER_TEXT_Y), spec["code"],
                  font=ImageFont.truetype(str(FONTS["regular"]), 24),
                  fill=blend(JADE_300, 0.95), anchor="ra")
    return img


def png_header_ok(path: Path) -> tuple:
    """只读文件头判断 PNG 合法性与尺寸, 不重新解码."""
    try:
        head = path.read_bytes()[:33]
    except OSError:
        return False, 0, 0
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        return False, 0, 0
    width, height = struct.unpack(">II", head[16:24])
    return True, width, height
def auto_subset(specs) -> bool:
    """缺字形时现场重建字体子集.

    CI 里新数据带来没见过的字是常态 (实测: 场景从 501 增到 1055 时冒出 4 个生僻字),
    与其让人手跑一遍脚本, 不如在这里自愈. 需要 fonttools; 源字体不在
    tools/assets/fonts/.cache/ 时会联网从 CDN 下载 (11-12 MB × 2, 一次性).
    重建失败就老实失败 —— 宁可不发图, 也不发带豆腐块的分享图.
    """
    try:
        import subset_og_font
    except Exception as exc:  # 缺 fonttools 或脚本不存在
        print("[og] 无法导入 subset_og_font (%s)" % exc)
        return False
    chars = subset_og_font.charset_for(specs, subset_og_font.DEFAULT_PAD_TOP)
    print("[og] 自动重建字体子集: %d 字 (需要 fonttools + 源字体)" % len(chars))
    try:
        code = subset_og_font.main([], chars=chars)
    except SystemExit as exc:
        code = exc.code or 0
    except Exception as exc:
        print("[og] 重建失败: %s" % exc)
        return False
    if code:
        return False
    covered = set(og_image.load_json(COVERAGE).get("chars") or "")
    return not (og_image.spec_chars(specs) - covered)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dist", default=str(REPO / "web" / "dist"))
    ap.add_argument("--base", default=og_image.DEFAULT_BASE)
    ap.add_argument("--limit", type=int, default=0, help="只画前 N 张 (调版式)")
    ap.add_argument("--only", default="", help="只画这些路由 (逗号分隔, site 表示站点首页)")
    ap.add_argument("--colors", type=int, default=96, help="PNG 调色板颜色数 (0 = 真彩)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-auto-subset", action="store_true",
                    help="缺字形时不自动重建子集, 直接失败")
    args = ap.parse_args()

    dist = Path(args.dist)
    index_path = dist / "data" / "index.unified.json"
    if not index_path.exists():
        sys.exit("[og] 缺少 %s: 先跑 export_static_site.py + build_unified_index.py + npm run build"
                 % index_path)
    index = og_image.load_json(index_path)
    meta_path = dist / "data" / "meta.json"
    meta = og_image.load_json(meta_path) if meta_path.exists() else None
    specs = og_image.build_specs(index, meta, dist / "templates")
    print("[og] 路由 %d 条, 文案来自 dist/data/index.unified.json + dist/templates/*.md" % len(specs))

    if args.only:
        wanted = {("" if p.strip().strip("/") == "site" else p.strip().strip("/"))
                  for p in args.only.split(",") if p.strip()}
        specs = [s for s in specs if s["route"] in wanted]
        if not specs:
            sys.exit("[og] --only 没有匹配到任何路由")
    if args.limit:
        specs = specs[: args.limit]

    # 自检 1: 字形覆盖 (缺字形 = 图上豆腐块, 必须构建期失败)
    for name, path in FONTS.items():
        if not path.exists():
            sys.exit("[og] 缺少子集字体 %s: 跑 python3 tools/subset_og_font.py" % path)
    if not COVERAGE.exists():
        sys.exit("[og] 缺少 %s: 跑 python3 tools/subset_og_font.py" % COVERAGE)
    covered = set(og_image.load_json(COVERAGE).get("chars") or "")
    need = og_image.spec_chars(specs)
    missing = sorted(need - covered)
    if missing:
        print("[og] 排版用字 %d, 子集覆盖 %d, 缺 %d 个: %s"
              % (len(need), len(covered), len(missing), "".join(missing[:60])))
        if args.no_auto_subset or not auto_subset(specs):
            sys.exit("[og] 缺字形且自动重建未成功: %s" % "".join(missing[:60]))

    if args.dry_run:
        for spec in specs[:12]:
            print("  %-30s -> %-44s %s" % (spec["route"] or "(site)", spec["image"], spec["title"]))
        print("[og] dry-run, 未写盘 (可画 %d 张)" % len(specs))
        return 0

    images = {}
    for spec in specs:
        target = dist / spec["image"]
        target.parent.mkdir(parents=True, exist_ok=True)
        out = render(spec).convert("RGB")
        if args.colors:
            out = out.quantize(colors=args.colors, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG)
        out.save(target, "PNG", optimize=True, compress_level=9)
        images[spec["route"]] = {
            "image": spec["image"],
            "url": og_image.og_url(spec["route"], args.base),
            "alt": spec["alt"],
            "kind": spec["kind"],
            "code": spec.get("code") or "",
            "bytes": target.stat().st_size,
        }

    # 自检 2: 逐张确认落盘 + PNG 魔数 + 尺寸 + 体积下限 (空白图会小于 2 KB)
    bad, total = [], 0
    for route, info in images.items():
        ok, width, height = png_header_ok(dist / info["image"])
        if not ok:
            bad.append("%s(魔数/文件)" % info["image"])
        elif (width, height) != (W, H):
            bad.append("%s(尺寸 %dx%d)" % (info["image"], width, height))
        elif info["bytes"] < 2000:
            bad.append("%s(仅 %d 字节)" % (info["image"], info["bytes"]))
        total += info["bytes"]

    # 自检 3: 数量与统一名录对齐 —— 少画一张都说明路由集合变了而这里没跟上
    counts = og_image.unified_counts(index, meta)
    expect_min = counts["register"] + 5  # 名录 + 站点首页 + 4 个列表页
    if not (args.limit or args.only) and len(images) < expect_min:
        bad.append("图片 %d 张 < 预期下限 %d 张" % (len(images), expect_min))

    manifest = {
        "schema": "protreptic.og_images/v1",
        "generator": "tools/build_og_images.py",
        "base": args.base if args.base.endswith("/") else args.base + "/",
        "width": W,
        "height": H,
        "palette_colors": args.colors,
        "count": len(images),
        "total_bytes": total,
        "font_subset": {k: v.name for k, v in FONTS.items()},
        "font_license": "SIL OFL 1.1 — tools/assets/fonts/OFL-NotoSerifSC.txt",
        "kinds": {},
        "images": dict(sorted(images.items())),
    }
    for info in images.values():
        manifest["kinds"][info["kind"]] = manifest["kinds"].get(info["kind"], 0) + 1
    og_root = dist / og_image.OG_DIR
    og_root.mkdir(parents=True, exist_ok=True)
    (og_root / og_image.MANIFEST_NAME).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")

    if bad:
        print("[og] 自检失败 %d 项: %s" % (len(bad), bad[:6]))
        return 1

    print("[og] 已生成 %d 张 (%s), 共 %.1f MB, 单张 %.0f-%.0f KB"
          % (len(images), ", ".join("%s %d" % kv for kv in sorted(manifest["kinds"].items())),
             total / 1e6, min(i["bytes"] for i in images.values()) / 1024,
             max(i["bytes"] for i in images.values()) / 1024))
    print("[og] manifest -> %s" % (og_root / og_image.MANIFEST_NAME))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
