#!/usr/bin/env python3
"""check_og_mirror.py -- Phase30-A3: 校验前端 og:image 镜像规则与 Python 侧完全一致.

为什么必须校验
    路由 -> 分享图路径的规则写了两份: tools/og_image.py (Python, 构建期真正画图/写 meta)
    与 web/src/composables/useSeo.ts (TypeScript, SPA 站内跳转时改 head).
    两份只要有一点不一致, 就会出现「静态直连是 A 图、站内跳转后是 B 图」的错位.

做法
    用 web/node_modules 里的 esbuild 把真实的 useSeo.ts 打包成 ESM (import.meta.env 用
    --define 注入 BASE_URL), 在 node 里跑一遍 ogImagePath / ogImageUrl / ogTypeForPath,
    再把结果与 og_image.py 的输出逐条比对. 测的是真实源码, 不是复制品.

用法
    python3 tools/check_og_mirror.py        # 需要 node + web/node_modules (npm ci 之后)
退出码: 0 一致; 1 有不一致 / 环境缺失.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import og_image  # noqa: E402

WEB = REPO / "web"
BUNDLE = Path(tempfile.gettempdir()) / "pt_useseo_mirror.mjs"
DRIVER = Path(tempfile.gettempdir()) / "pt_og_mirror_driver.mjs"

# 覆盖契约里的每一条分支 + 边界: 空 / 列表页 / 人物 / 场景 / 模板 / 空格编码 / 未知
PATHS = [
    "", "/", "daily", "figures", "modes", "templates", "api",
    "minds/H-WYM-001", "figures/A-1-X-P", "templates/chibi",
    "figures/Sun Quan", "figures/未知场景-01", "nope",
]


def build_bundle() -> None:
    subprocess.run(
        ["npx", "esbuild", "src/composables/useSeo.ts", "--bundle", "--format=esm",
         "--outfile=%s" % BUNDLE,
         '--define:import.meta.env={"BASE_URL":"/protreptic/"}'],
        cwd=WEB, check=True, capture_output=True,
    )
    DRIVER.write_text(
        "import { ogImagePath, ogImageUrl, ogTypeForPath } from '%s'\n"
        "const paths = %s\n"
        "const out = {}\n"
        "for (const p of paths) out[p] = [ogImagePath(p), ogImageUrl(p), ogTypeForPath(p)]\n"
        "console.log(JSON.stringify(out))\n" % (BUNDLE, json.dumps(PATHS)),
        encoding="utf-8",
    )


def main() -> int:
    if not (WEB / "node_modules").is_dir():
        sys.exit("[mirror] 缺少 web/node_modules, 先 cd web && npm ci")
    try:
        build_bundle()
    except FileNotFoundError:
        sys.exit("[mirror] 找不到 node/npx")
    result = subprocess.run(["node", str(DRIVER)], check=True, capture_output=True, text=True)
    got = json.loads(result.stdout)

    bad = []
    for path in PATHS:
        want = [og_image.og_rel_path(path), og_image.og_url(path), og_image_og_type(path)]
        have = got.get(path)
        if have != want:
            bad.append("%r: TS=%s Python=%s" % (path, have, want))
    print("[mirror] 校验 %d 条路由规则, %d 条不一致" % (len(PATHS), len(bad)))
    for line in bad[:10]:
        print("  " + line)
    return 1 if bad else 0


def og_image_og_type(path: str) -> str:
    """og:type 规则 (与 useSeo.ogTypeForPath 同构): 人物 profile / 模板 article / 其余 website."""
    clean = str(path or "").strip("/")
    if clean.startswith("minds/"):
        return "profile"
    if clean.startswith("templates/"):
        return "article"
    return "website"


if __name__ == "__main__":
    raise SystemExit(main())
