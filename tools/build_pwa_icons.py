#!/usr/bin/env python3
"""build_pwa_icons.py -- Phase30-A4: 生成 PWA 图标 (web/public/icons/).

为什么不用 SVG
    manifest 的 icons 在 Android/Chrome 安装流程里必须是位图 (PNG); SVG 图标
    只在部分平台生效, 且 maskable 需要明确的位图安全区. 图标随品牌走、不随数据变,
    所以这里一次性画好入库, 生成逻辑留在脚本里可复现.

版式 (与站内印章 og 图同源: 深墨底 + 鎏金框 + 宋体字)
    - 不透明深墨底 #04060c (PWA 图标不能带 alpha 透明像素)
    - 鎏金圆角外框 + 内层细线, 底部一道短金线 (印章意象)
    - 中央单个「思」字 (Noto Serif SC 子集, 与 og 图共用同一份字体与覆盖表)

maskable
    Android 会把图标裁成圆形/水滴形, 安全区只有中心 80% 直径圆. 因此 maskable
    版本把外框收到 66% 见方, 底色铺满整张画布, 圆角不会顶到裁切边.

产物 (全部入库)
    web/public/icons/icon-192.png            192x192  purpose=any
    web/public/icons/icon-512.png            512x512  purpose=any
    web/public/icons/icon-maskable-192.png   192x192  purpose=maskable
    web/public/icons/icon-maskable-512.png   512x512  purpose=maskable
    web/public/icons/apple-touch-icon.png    180x180  iOS 主屏 (不透明)
    web/public/favicon.svg                    与图标同款的矢量版

自检
    1) 「思」必须在 tools/assets/fonts/coverage.json 覆盖表里 (缺字 = 豆腐块)
    2) 每张都得落盘, PNG 魔数正确, 尺寸与文件名一致, 且不含透明像素
    3) favicon.svg 存在

用法
    python3 tools/build_pwa_icons.py
    python3 tools/build_pwa_icons.py --check      # 只自检已有产物, 不重画
"""

from __future__ import annotations

import argparse
import json
import struct
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parent.parent
FONT_DIR = REPO / "tools" / "assets" / "fonts"
FONT_BOLD = FONT_DIR / "ProtrepticOgSerif-Bold.otf"
COVERAGE = FONT_DIR / "coverage.json"
OUT_DIR = REPO / "web" / "public" / "icons"
FAVICON = REPO / "web" / "public" / "favicon.svg"

SEAL_CHAR = "思"

INK = (4, 6, 12)
GOLD_300 = (240, 215, 159)
GOLD_500 = (212, 162, 76)
JADE_400 = (94, 234, 212)

TARGETS = {
    "icon-192.png": (192, False),
    "icon-512.png": (512, False),
    "icon-maskable-192.png": (192, True),
    "icon-maskable-512.png": (512, True),
    "apple-touch-icon.png": (180, False),
}

SS = 4  # 超采样倍数: 4x 画完再降采样, 消除圆角/文字的锯齿


def blend(color, alpha, bg=INK):
    return tuple(int(round(c * alpha + b * (1 - alpha))) for c, b in zip(color, bg))


def add_glow(img: Image.Image, center, radius: float, color, alpha: float) -> None:
    """低分辨率算 alpha 再双三次放大 (逐像素 python 循环只跑 64x64 次)."""
    size = img.size[0]
    g = 64
    mask = Image.new("L", (g, g))
    px = mask.load()
    cx0, cy0 = center
    for y in range(g):
        cy = (y + 0.5) / g * size - cy0
        for x in range(g):
            cx = (x + 0.5) / g * size - cx0
            d = ((cx * cx + cy * cy) ** 0.5) / radius
            v = 0.0 if d >= 1 else (1.0 - d) ** 2.2
            px[x, y] = int(255 * alpha * v)
    mask = mask.resize((size, size), Image.BICUBIC)
    layer = Image.new("RGBA", img.size, color + (0,))
    layer.putalpha(mask)
    img.alpha_composite(layer)


def render(size: int, maskable: bool, font_path: Path) -> Image.Image:
    s = size * SS
    img = Image.new("RGBA", (s, s), INK + (255,))
    add_glow(img, (s * 0.18, s * 0.12), s * 0.95, GOLD_500, 0.16)
    add_glow(img, (s * 0.92, s * 0.30), s * 0.80, JADE_400, 0.09)
    add_glow(img, (s * 0.50, s * 1.05), s * 0.85, GOLD_500, 0.10)

    draw = ImageDraw.Draw(img)
    inset = s * (0.165 if maskable else 0.075)
    x0, y0, x1, y1 = inset, inset, s - inset, s - inset
    radius = (x1 - x0) * 0.14
    draw.rounded_rectangle((x0, y0, x1, y1), radius=radius,
                           fill=blend(GOLD_500, 0.07) + (255,),
                           outline=GOLD_500 + (120,), width=max(2, int(s * 0.012)))
    pad = (x1 - x0) * 0.075
    draw.rounded_rectangle((x0 + pad, y0 + pad, x1 - pad, y1 - pad),
                           radius=radius * 0.7,
                           outline=GOLD_500 + (52,), width=max(1, int(s * 0.004)))

    font = ImageFont.truetype(str(font_path), int((y1 - y0) * 0.52))
    draw.text(((x0 + x1) / 2, (y0 + y1) / 2 - (y1 - y0) * 0.03), SEAL_CHAR,
              font=font, fill=GOLD_300 + (240,), anchor="mm")

    lw = (x1 - x0) * 0.34
    draw.rectangle(((x0 + x1) / 2 - lw / 2, y1 - pad * 1.9,
                    (x0 + x1) / 2 + lw / 2, y1 - pad * 1.9 + max(2, s * 0.008)),
                   fill=GOLD_500 + (95,))

    return img.convert("RGB").resize((size, size), Image.LANCZOS)


FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" role="img" aria-label="Protreptic">
  <defs>
    <radialGradient id="glow" cx="18%" cy="12%" r="95%">
      <stop offset="0%" stop-color="#d4a24c" stop-opacity=".30"/>
      <stop offset="60%" stop-color="#d4a24c" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glow2" cx="92%" cy="30%" r="80%">
      <stop offset="0%" stop-color="#5eead4" stop-opacity=".18"/>
      <stop offset="70%" stop-color="#5eead4" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="64" height="64" rx="12" fill="#04060c"/>
  <rect width="64" height="64" rx="12" fill="url(#glow)"/>
  <rect width="64" height="64" rx="12" fill="url(#glow2)"/>
  <rect x="6.5" y="6.5" width="51" height="51" rx="9" fill="none" stroke="#d4a24c" stroke-opacity=".55" stroke-width="1.4"/>
  <rect x="11" y="11" width="42" height="42" rx="6" fill="none" stroke="#d4a24c" stroke-opacity=".22" stroke-width="0.8"/>
  <line x1="25" y1="47" x2="39" y2="47" stroke="#d4a24c" stroke-opacity=".45" stroke-width="1.6"/>
</svg>
"""


def png_size(path: Path) -> tuple:
    with open(path, "rb") as fh:
        head = fh.read(26)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("不是 PNG: %s" % path)
    return struct.unpack(">II", head[16:24])


def check() -> int:
    fails = 0
    for name, (size, _maskable) in TARGETS.items():
        path = OUT_DIR / name
        if not path.exists():
            print("[icons] 缺失 %s" % path)
            fails += 1
            continue
        try:
            w, h = png_size(path)
        except ValueError as exc:
            print("[icons] %s" % exc)
            fails += 1
            continue
        img = Image.open(path)
        has_alpha = img.convert("RGBA").getextrema()[3][0] < 255
        ok = (w, h) == (size, size) and not has_alpha
        print("[icons] %-24s %dx%d alpha=%s bytes=%d %s"
              % (name, w, h, has_alpha, path.stat().st_size, "OK" if ok else "FAIL"))
        if not ok:
            fails += 1
    if not FAVICON.exists():
        print("[icons] 缺失 %s" % FAVICON)
        fails += 1
    if fails:
        print("[icons] 自检失败 %d 项" % fails)
        return 1
    print("[icons] 自检通过: %d 张图标 + favicon.svg" % len(TARGETS))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="只自检, 不重画")
    args = ap.parse_args()

    if args.check:
        return check()

    if not FONT_BOLD.exists():
        sys.exit("[icons] 缺少字体 %s" % FONT_BOLD)
    if not COVERAGE.exists():
        sys.exit("[icons] 缺少 %s: 先跑 python3 tools/subset_og_font.py" % COVERAGE)
    covered = set(json.loads(COVERAGE.read_text(encoding="utf-8")).get("chars") or "")
    if SEAL_CHAR not in covered:
        sys.exit("[icons] 字体子集缺字 %r: 跑 python3 tools/subset_og_font.py 重建" % SEAL_CHAR)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, (size, maskable) in TARGETS.items():
        img = render(size, maskable, FONT_BOLD)
        path = OUT_DIR / name
        img.save(path, format="PNG", optimize=True)
        print("[icons] %-24s %dx%d maskable=%s bytes=%d"
              % (name, size, size, maskable, path.stat().st_size))
    FAVICON.write_text(FAVICON_SVG, encoding="utf-8")
    print("[icons] favicon.svg bytes=%d" % FAVICON.stat().st_size)
    return check()


if __name__ == "__main__":
    raise SystemExit(main())
