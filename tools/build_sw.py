#!/usr/bin/env python3
"""build_sw.py -- Phase30-A4: 把 service worker 模板注入构建期版本号, 产出 dist/sw.js.

为什么要在构建期注入
    SW 必须知道「本次构建的产物是哪一版」, 才能做到两件事:
      1) 预缓存清单里放的是本次构建真实存在的文件名 (assets/ 带内容哈希);
      2) 升级后 activate 时能删掉上一版的缓存, 不会出现「旧缓存卡死」.
    纯静态托管没有服务端, 这两件事只能在构建期把事实写进 sw.js.

双版本号 (见 docs/architecture/web_p0_architecture.md 第 3 节)
    BUILD_ID  = dist/assets/* 文件名串接后的 sha256 前 12 位 —— 任何 JS/CSS 变化都会变
    DATA_REV  = dist/data/meta.json 的 generated_at (纯数字 14 位) —— 数据重导才会变
    缓存名: protreptic-shell-<BUILD_ID> / protreptic-data-<DATA_REV>

产物
    <dist>/sw.js            线上 /protreptic/sw.js (scope 就是 /protreptic/)
    <dist>/sw.build.json    本次注入的版本与清单元数据 (排查「为什么没更新」用)

自检 (任一不过直接非 0 退出)
    1) dist/assets 里必须有 JS 与 CSS —— 空 assets 说明 index.html 的入口 script 又被吞了
    2) 预缓存清单里每个 URL 必须真实存在于 dist (写错路径 = 安装期 404)
    3) 注入后 sw.js 里不允许残留 __XXX__ 占位符

用法
    cd web && VITE_DATA_MODE=static npm run build
    python3 tools/build_sw.py                       # 默认读 web/dist, base=/protreptic/
    python3 tools/build_sw.py --check               # 只比对已有 sw.js 是否与当前 dist 一致
    python3 tools/build_sw.py --base=/ --dist=/tmp/dist    # 根路径部署 (docker/nginx)
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_TEMPLATE = REPO / "web" / "sw.template.js"

# 与 web/public/data 里的实际文件名绑定; 少一个就在这里显式写清楚
SOFT_PRECACHE = [
    "data/figures.index.json",
    "data/index.unified.json",
    "data/meta.json",
    # Phase30-B4: 首页「今日一模式」的定位索引 (12 KB gzip). 预缓存它, 装好 SW 后
    # 首屏那个模块离线也能出内容; 名称表 (175 KB) 不预缓存, 由 /daily 首次访问时按需进 DATA_CACHE.
    "data/daily/index.json",
]
PLACEHOLDERS = ("__BUILD_ID__", "__DATA_REV__", "__BASE__", "__SHELL_ENTRY__",
                "__PRECACHE_CRITICAL__", "__PRECACHE_SHELL_SOFT__", "__PRECACHE_DATA__",
                "__WARM_URLS__")


def normalize_base(value: str) -> str:
    base = value.strip()
    if not base.startswith("/"):
        base = "/" + base
    if not base.endswith("/"):
        base += "/"
    return base


SELF_CLOSED_SCRIPT = re.compile(r"<script\b[^>]*?/>", re.I)


def check_mountable(dist: Path, base: str) -> None:
    """外壳 / 预渲染页必须真的能挂载.

    踩过的坑: HTML 解析器把 <script> 当 raw text 元素, 自闭合 <script .../> 会被忽略,
    它后面的标签(含入口 script)全部被吞成脚本文本 -> body 空、Vue 挂不上、页面一片空白.
    SW 离线回退用的是 dist/index.html, 在线深链用的是预渲染页, 两份都必须可挂载.
    """
    targets = [dist / "index.html"]
    for rel in ("figures/index.html", "modes/index.html"):
        if (dist / rel).is_file():
            targets.append(dist / rel)
    for path in targets:
        html = path.read_text(encoding="utf-8")
        if '<div id="app">' not in html:
            sys.exit("[sw] %s 里没有 <div id=\"app\">: 该页面无法挂载" % path)
        hit = SELF_CLOSED_SCRIPT.search(html)
        if hit:
            sys.exit("[sw] %s 出现自闭合 %s —— HTML 解析器会把它后面的入口 script 吞成文本, "
                     "页面空白. 改成 <script ...></script>" % (path, hit.group(0)[:80]))


def build_id_from_assets(assets_dir: Path) -> tuple:
    if not assets_dir.is_dir():
        sys.exit("[sw] %s 不存在: 先跑 cd web && npm run build" % assets_dir)
    names = sorted(p.name for p in assets_dir.iterdir() if p.is_file())
    if not names:
        sys.exit("[sw] %s 是空的: index.html 的入口 script 可能被自闭合 <script/> 吞了" % assets_dir)
    if not any(n.endswith(".js") for n in names):
        sys.exit("[sw] %s 里没有 .js 产物" % assets_dir)
    if not any(n.endswith(".css") for n in names):
        sys.exit("[sw] %s 里没有 .css 产物" % assets_dir)
    digest = hashlib.sha256("\n".join(names).encode("utf-8")).hexdigest()
    return digest[:12], names


def data_rev_from_meta(dist: Path) -> tuple:
    meta = dist / "data" / "meta.json"
    if not meta.is_file():
        sys.exit("[sw] 缺少 %s: 静态数据分片没进 dist (tools/export_static_site.py)" % meta)
    raw = meta.read_bytes()
    try:
        generated_at = json.loads(raw.decode("utf-8")).get("generated_at") or ""
    except (ValueError, UnicodeDecodeError):
        generated_at = ""
    digits = re.sub(r"[^0-9]", "", generated_at)
    if len(digits) >= 14:
        return digits[:14], generated_at
    # 回退: 数据文件的哈希 (仍然满足「数据变了版本就变」)
    return hashlib.sha256(raw).hexdigest()[:12], generated_at


def check_exists(dist: Path, base: str, urls: list) -> None:
    missing = []
    for url in urls:
        rel = url[len(base):] if url.startswith(base) else url.lstrip("/")
        if not (dist / rel).is_file():
            missing.append("%s -> %s" % (url, dist / rel))
    if missing:
        sys.exit("[sw] 预缓存清单里有 %d 个文件不存在:\n  %s" % (len(missing), "\n  ".join(missing)))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dist", default=str(REPO / "web" / "dist"))
    ap.add_argument("--base", default="/protreptic/")
    ap.add_argument("--template", default=str(DEFAULT_TEMPLATE))
    ap.add_argument("--check", action="store_true", help="只校验已有 sw.js 与当前 dist 是否一致")
    args = ap.parse_args()

    dist = Path(args.dist).resolve()
    base = normalize_base(args.base)
    template_path = Path(args.template).resolve()

    check_mountable(dist, base)
    build_id, asset_names = build_id_from_assets(dist / "assets")
    data_rev, generated_at = data_rev_from_meta(dist)

    critical = [base + "index.html"] + [base + "assets/" + n for n in asset_names]
    for rel in ("favicon.svg", "manifest.webmanifest", "manifest-light.webmanifest"):
        if (dist / rel).is_file():
            critical.append(base + rel)
        else:
            sys.exit("[sw] 缺少 %s (%s)" % (rel, dist / rel))
    icons = sorted(p.name for p in (dist / "icons").glob("*.png")) if (dist / "icons").is_dir() else []
    if not icons:
        sys.exit("[sw] %s 里没有图标 PNG" % (dist / "icons"))
    critical += [base + "icons/" + n for n in icons]

    soft = []
    for rel in SOFT_PRECACHE:
        if (dist / rel).is_file():
            soft.append(base + rel)
        else:
            print("[sw] 警告: 软预缓存缺 %s, 跳过 (离线索引可能不完整)" % rel)

    # 复盘模板 markdown 很小(7 个共 ~104 KB raw), 属于常驻外壳内容 -> shell 缓存
    shell_soft = [base + "templates/" + p.name
                  for p in sorted((dist / "templates").glob("*.md"))]
    if not shell_soft:
        sys.exit("[sw] 没有 dist/templates/*.md: 复盘模板没进产物")

    warm = [base + "data/modes/" + p.name
            for p in sorted((dist / "data" / "modes").glob("index-*.json"))]
    if not warm:
        sys.exit("[sw] 没有 data/modes/index-*.json 可预热: 静态数据分片缺失")

    check_exists(dist, base, critical + shell_soft + soft + warm)

    if not template_path.is_file():
        sys.exit("[sw] 模板不存在: %s" % template_path)
    source = template_path.read_text(encoding="utf-8")

    out = source
    for token, value in (
        ("__BUILD_ID__", build_id),
        ("__DATA_REV__", data_rev),
        ("__BASE__", base),
        ("__SHELL_ENTRY__", base + "index.html"),
        ("__PRECACHE_CRITICAL__", json.dumps(critical, ensure_ascii=False, indent=0)),
        ("__PRECACHE_SHELL_SOFT__", json.dumps(shell_soft, ensure_ascii=False, indent=0)),
        ("__PRECACHE_DATA__", json.dumps(soft, ensure_ascii=False, indent=0)),
        ("__WARM_URLS__", json.dumps(warm, ensure_ascii=False, indent=0)),
    ):
        if token not in out:
            sys.exit("[sw] 模板缺少占位符 %s" % token)
        out = out.replace(token, value)

    leftover = re.findall(r"__[A-Z][A-Z_]{2,}__", out)
    if leftover:
        sys.exit("[sw] 注入后仍残留占位符: %s" % sorted(set(leftover)))

    sw_path = dist / "sw.js"
    build_path = dist / "sw.build.json"
    meta = {
        "schema": "protreptic.service_worker_build/v1",
        "generator": "tools/build_sw.py",
        "base": base,
        "build_id": build_id,
        "data_rev": data_rev,
        "data_generated_at": generated_at,
        "version": "%s.%s" % (build_id, data_rev),
        "shell_cache": "protreptic-shell-%s" % build_id,
        "data_cache": "protreptic-data-%s" % data_rev,
        "shell_entry": base + "index.html",
        "precache_critical": critical,
        "precache_shell_soft": shell_soft,
        "precache_data": soft,
        "warm": warm,
        "counts": {"critical": len(critical), "shell_soft": len(shell_soft),
                   "data": len(soft), "warm": len(warm)},
    }

    if args.check:
        fails = []
        if not sw_path.is_file():
            fails.append("缺少 %s" % sw_path)
        elif sw_path.read_text(encoding="utf-8") != out:
            fails.append("dist/sw.js 与当前 dist 不一致 (构建期注入的版本号/清单已过期)")
        if not build_path.is_file():
            fails.append("缺少 %s" % build_path)
        else:
            on_disk = json.loads(build_path.read_text(encoding="utf-8"))
            for key in ("build_id", "data_rev", "precache_critical", "precache_shell_soft",
                        "precache_data", "warm"):
                if on_disk.get(key) != meta[key]:
                    fails.append("sw.build.json 的 %s 过期" % key)
        if fails:
            for line in fails:
                print("[sw] FAIL %s" % line)
            return 1
        print("[sw] OK  sw.js 与 dist 一致 (version=%s, shell=%d, templates=%d, data=%d, warm=%d)"
              % (meta["version"], len(critical), len(shell_soft), len(soft), len(warm)))
        return 0

    sw_path.write_text(out, encoding="utf-8")
    build_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    gz = len(gzip.compress(out.encode("utf-8")))
    print("[sw] BUILD_ID=%s DATA_REV=%s (data generated_at=%s)"
          % (build_id, data_rev, generated_at or "-"))
    print("[sw] %-28s %7d B (%d B gzip)" % ("dist/sw.js", len(out.encode("utf-8")), gz))
    print("[sw] 预缓存 关键 %d 项 / 模板 %d 项 / 索引 %d 项 / 后台预热 %d 项"
          % (len(critical), len(shell_soft), len(soft), len(warm)))
    print("[sw] shell=%s" % meta["shell_cache"])
    print("[sw] data =%s" % meta["data_cache"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
