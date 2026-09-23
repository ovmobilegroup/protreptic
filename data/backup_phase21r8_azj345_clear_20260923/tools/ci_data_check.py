#!/usr/bin/env python3
"""ci_data_check.py -- Phase30-C1 数据校验门 (index.unified.json schema + sitemap/数据条数一致).

三层断言, 任何一条失败即 exit 1:

  1) index.unified.json schema 断言 (公开名录是前端唯一数据入口, 形状坏了整站渲染空)
     * schema == protreptic.unified_index/v1
     * counts.total/figures/scenarios/with_modes 与 items 逐项重算一致
     * 每条 item: 必需字段齐全 + 类型正确 + code 唯一非空 + type 属于 {figure, scenario}
                + n_modes 为非负整数 + 描述/年代等为字符串
     * 隔离名单 (QUARANTINE, 见 tools/_quarantine.py) 的数据不得出现在公开名录

  2) 路由清单 与 名录 双向一致 (docs/architecture/web_p0_routes.json)
     * count == len(routes); counts_by_type 与实际重算一致
     * 每个 person/scenario 路由的 code 都能在名录里找到, 反之每个名录条目都有对应路由
     * name / n_modes 两处必须一致 (同一事实两个来源不允许打架)

  3) sitemap 与 路由清单/名录 一致 (web/public/sitemap.xml)
     * loc 无重复; 全部以 <origin><base> 开头且带尾斜杠 (线上无尾斜杠是 301)
     * 集合 == 路由清单 canonical 并上 {站点首页}
     * 全站目录 (人物 + 场景) 100% 覆盖; 条目数 >= 1300 (A1 验收线)

用法:
  python3 tools/ci_data_check.py
  python3 tools/ci_data_check.py --index web/public/data/index.unified.json --sitemap web/public/sitemap.xml
  python3 tools/ci_data_check.py --sitemap ""        # 跳过 sitemap 层 (仅本地排查用)

退出码: 0 全部通过; 1 有失败; 2 输入缺失.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

SITE_ORIGIN = "https://ovmobilegroup.github.io"
DEFAULT_BASE = "/protreptic/"
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
SCHEMA = "protreptic.unified_index/v1"
ROUTES_SCHEMA = "protreptic.prerendered_routes/v1"
# 隔离名单的唯一来源是 tools/_quarantine.py (图谱层 build_graph_data.py 共用同一份),
# 这里不复制副本 —— 复制过的副本正是 Phase30 里最外层与图谱层口径分裂的成因.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _quarantine import QUARANTINE as _QUARANTINE  # noqa: E402

QUARANTINED = set(_QUARANTINE)  # 已确证虚构: 不得出现在公开名录
CODE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ._+\-]*$")
MIN_SITEMAP_ENTRIES = 1300

REQUIRED_FIELDS = {
    "code": str,
    "name": str,
    "type": str,
    "era": str,
    "domains": list,
    "historical_domains": list,
    "gender": str,
    "ethnicity": str,
    "n_modes": int,
    "description": str,
    "href": str,
}
TYPES = ("figure", "scenario")
# 路由清单用 person/scenario 命名, 名录用 figure/scenario; 同一套东西两个名字, 这里显式对齐
ROUTE_TYPE_TO_INDEX = {"person": "figure", "scenario": "scenario"}


class Gate:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.warnings: list[str] = []
        self.notes: list[str] = []
        self.checks = 0

    def ok(self, label: str) -> None:
        self.checks += 1

    def fail(self, label: str, detail: str) -> None:
        self.checks += 1
        self.failures.append(f"{label}: {detail}")

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def note(self, msg: str) -> None:
        self.notes.append(msg)

    def finish(self) -> int:
        for n in self.notes:
            print(f"  · {n}")
        if self.warnings:
            print(f"  ! 警告 {len(self.warnings)} 条 (不判失败, 但必须跟进):")
            for w in self.warnings[:20]:
                print(f"    ! {w}")
        print(f"数据校验: {self.checks} 条断言, 失败 {len(self.failures)} 条")
        if self.failures:
            print("数据校验: FAIL")
            for f in self.failures[:40]:
                print(f"    - {f}")
            if len(self.failures) > 40:
                print(f"    ... 另有 {len(self.failures) - 40} 条未列出")
            return 1
        print("数据校验: PASS")
        return 0


URL_BAD_CHARS = re.compile(r'[\s<>"{}|\\^`\x00-\x1f\x7f]')


def url_is_escaped(url: str) -> bool:
    """URL 里不得出现裸空格/控制字符 —— sitemap 规范要求 <loc> 是转义后的 URL,
    裸空格是非法 URL, 爬虫解析会失败 (实测线上 %XX 形式 200, 裸形式 curl 直接 000)."""
    return not URL_BAD_CHARS.search(url)


def url_key(url: str) -> str:
    """比较 URL 集合时按「解码后」比较: 上游无论在哪一层转义 (canonical 或 sitemap),
    只要指向同一资源就算一致; 是否转义由 url_is_escaped 单独断言."""
    return urllib.parse.unquote(url)


PLACEHOLDER_RE = re.compile(r"^(code|name|description|title|era)\s+field$", re.I)


def load_json(path: Path, gate: Gate, label: str):
    if not path.is_file():
        gate.fail(label, f"文件不存在: {path}")
        return None
    try:
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as exc:  # noqa: BLE001
        gate.fail(label, f"JSON 解析失败: {path}: {type(exc).__name__}: {exc}")
        return None


def check_unified(index: dict, gate: Gate) -> dict[str, dict]:
    by_code: dict[str, dict] = {}
    if index.get("schema") != SCHEMA:
        gate.fail("index.schema", f"{index.get('schema')!r} != {SCHEMA!r}")
    else:
        gate.ok("index.schema")

    items = index.get("items")
    if not isinstance(items, list) or not items:
        gate.fail("index.items", f"items 缺失/为空: {type(items).__name__}")
        return by_code
    gate.ok("index.items")

    counts = index.get("counts") or {}
    type_count: dict[str, int] = {t: 0 for t in TYPES}
    with_modes = 0
    for i, item in enumerate(items):
        where = f"items[{i}]"
        if not isinstance(item, dict):
            gate.fail("index.item.type", f"{where} 不是对象")
            continue
        code = item.get("code")
        if not isinstance(code, str) or not code.strip():
            gate.fail("index.item.code", f"{where} code 缺失/非字符串: {code!r}")
            continue
        for field, ftype in REQUIRED_FIELDS.items():
            if field not in item:
                gate.fail("index.item.field", f"{where}({code}) 缺字段 {field}")
                continue
            value = item[field]
            if ftype is int:
                if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                    gate.fail("index.item.type", f"{where}({code}) {field} 应为非负整数, 实为 {value!r}")
            elif not isinstance(value, ftype):
                gate.fail("index.item.type", f"{where}({code}) {field} 应为 {ftype.__name__}, 实为 {type(value).__name__}")
        if not CODE_RE.match(code):
            gate.fail("index.item.code", f"{where} code 形态可疑: {code!r}")
        if item.get("type") not in TYPES:
            gate.fail("index.item.type", f"{where}({code}) type={item.get('type')!r} 不在 {TYPES}")
        else:
            type_count[item["type"]] += 1
        if isinstance(item.get("n_modes"), int) and item["n_modes"] > 0:
            with_modes += 1
        if code in QUARANTINED:
            gate.fail("index.quarantine", f"{where} 隔离数据 {code} 出现在公开名录")
        if URL_BAD_CHARS.search(str(code)):
            gate.warn(f"index.code.hygiene: {where} code 含空白/控制字符 {code!r} -> URL 里必须转义")
        for field in ("code", "name", "description"):
            value = item.get(field)
            if isinstance(value, str) and PLACEHOLDER_RE.match(value.strip()):
                gate.warn(f"index.placeholder: {where} {field}={value!r} 是模板占位符, 疑似脏数据泄漏进公开名录")
        if code in by_code:
            gate.fail("index.item.unique", f"code 重复: {code}")
        else:
            by_code[code] = item

    for t in TYPES:
        expect = counts.get(f"{t}s")
        if expect != type_count[t]:
            gate.fail("index.counts", f"counts.{t}s={expect!r} != 实际 {type_count[t]}")
        else:
            gate.ok("index.counts")
    if counts.get("total") != len(items):
        gate.fail("index.counts", f"counts.total={counts.get('total')!r} != len(items)={len(items)}")
    else:
        gate.ok("index.counts.total")
    if counts.get("with_modes") != with_modes:
        gate.fail("index.counts", f"counts.with_modes={counts.get('with_modes')!r} != 实际 {with_modes}")
    else:
        gate.ok("index.counts.with_modes")

    nameless = [c for c, it in by_code.items() if not (it.get("name") or "").strip()]
    no_desc = [c for c, it in by_code.items() if not (it.get("description") or "").strip()]
    gate.note(f"名录 {len(by_code)} 条 (人物 {type_count['figure']} / 场景 {type_count['scenario']}, "
              f"带模式 {with_modes}); 无名字 {len(nameless)} 条, 无描述 {len(no_desc)} 条")
    return by_code


def check_routes(routes: dict, by_code: dict[str, dict], gate: Gate) -> dict[str, dict]:
    """校验路由清单, 并与名录做双向一致; 返回 {code: route}"""
    if routes.get("schema") != ROUTES_SCHEMA:
        gate.fail("routes.schema", f"{routes.get('schema')!r} != {ROUTES_SCHEMA!r}")
    else:
        gate.ok("routes.schema")
    rlist = routes.get("routes")
    if not isinstance(rlist, list) or not rlist:
        gate.fail("routes.routes", "routes 缺失/为空")
        return {}
    if routes.get("count") != len(rlist):
        gate.fail("routes.count", f"count={routes.get('count')!r} != len(routes)={len(rlist)}")
    else:
        gate.ok("routes.count")

    base = routes.get("base", DEFAULT_BASE)
    by_type: dict[str, int] = {}
    seen_paths: set[str] = set()
    canon_by_code: dict[str, dict] = {}
    for i, r in enumerate(rlist):
        p = r.get("path")
        if not isinstance(p, str) or not p:
            gate.fail("routes.path", f"routes[{i}] path 缺失")
            continue
        if p in seen_paths:
            gate.fail("routes.unique", f"path 重复: {p}")
        seen_paths.add(p)
        t = r.get("type")
        by_type[t] = by_type.get(t, 0) + 1
        canon = r.get("canonical") or ""
        if not canon.startswith(f"{SITE_ORIGIN}{base}") or not canon.endswith("/"):
            gate.fail("routes.canonical", f"{p}: canonical 形态不对: {canon!r}")
        if canon and not url_is_escaped(canon):
            gate.fail("routes.canonical.escape", f"{p}: canonical 含未转义字符 (裸空格等): {canon!r}")
        code = r.get("code")
        if t in ROUTE_TYPE_TO_INDEX:
            if not code:
                gate.fail("routes.code", f"{p}: {t} 路由缺 code")
                continue
            if code in canon_by_code:
                gate.fail("routes.code", f"code 重复路由: {code}")
            canon_by_code[code] = r
    for t, n in by_type.items():
        expect = (routes.get("counts_by_type") or {}).get(t)
        if expect != n:
            gate.fail("routes.counts_by_type", f"{t}: {expect!r} != 实际 {n}")
        else:
            gate.ok("routes.counts_by_type")
    gate.note(f"路由 {len(rlist)} 条 {dict(sorted(by_type.items()))}, base={base!r}")

    missing_route = sorted(set(by_code) - set(canon_by_code))
    missing_entry = sorted(set(canon_by_code) - set(by_code))
    if missing_route:
        gate.fail("cross.coverage", f"{len(missing_route)} 条名录数据没有路由, 例: {missing_route[:5]}")
    else:
        gate.ok("cross.coverage.index_to_routes")
    if missing_entry:
        gate.fail("cross.coverage", f"{len(missing_entry)} 条路由不在名录里, 例: {missing_entry[:5]}")
    else:
        gate.ok("cross.coverage.routes_to_index")

    mismatch = []
    for code, r in canon_by_code.items():
        item = by_code.get(code)
        if not item:
            continue
        if (r.get("name") or "") != (item.get("name") or ""):
            mismatch.append(f"{code} name 路由={r.get('name')!r} 名录={item.get('name')!r}")
        elif r.get("n_modes") != item.get("n_modes"):
            mismatch.append(f"{code} n_modes 路由={r.get('n_modes')!r} 名录={item.get('n_modes')!r}")
    if mismatch:
        gate.fail("cross.fields", f"{len(mismatch)} 条 name/n_modes 两处打架, 例: {mismatch[:5]}")
    else:
        gate.ok("cross.fields")
    return canon_by_code


def check_sitemap(path: Path, routes: dict, gate: Gate) -> None:
    if not path.is_file():
        gate.fail("sitemap.exists", f"文件不存在: {path} (先跑 tools/build_sitemap.py)")
        return
    gate.ok("sitemap.exists")
    try:
        root = ET.parse(path).getroot()
    except Exception as exc:  # noqa: BLE001
        gate.fail("sitemap.parse", f"{path}: {type(exc).__name__}: {exc}")
        return
    gate.ok("sitemap.parse")
    locs = [(el.text or "").strip() for el in root.iter(f"{{{SITEMAP_NS}}}loc")]
    if not locs:
        gate.fail("sitemap.loc", "sitemap 里没有任何 loc")
        return
    if len(set(locs)) != len(locs):
        gate.fail("sitemap.unique", f"{len(locs) - len(set(locs))} 条重复 URL")
    else:
        gate.ok("sitemap.unique")

    base = routes.get("base", DEFAULT_BASE)
    prefix = f"{SITE_ORIGIN}{base}"
    bad_shape = [u for u in locs if not u.startswith(prefix) or not u.endswith("/")]
    if bad_shape:
        gate.fail("sitemap.shape", f"{len(bad_shape)} 条 URL 未带 {prefix} 前缀或尾斜杠, 例: {bad_shape[:3]}")
    else:
        gate.ok("sitemap.shape")

    unescaped = [u for u in locs if not url_is_escaped(u)]
    if unescaped:
        gate.fail("sitemap.escape", f"{len(unescaped)} 条 <loc> 含未转义字符 (裸空格等), "
                                     f"爬虫无法解析: {unescaped[:3]}")
    else:
        gate.ok("sitemap.escape")

    expected = {r["canonical"] for r in routes.get("routes", []) if r.get("canonical")}
    expected.add(prefix)  # 站点首页
    loc_keys = {url_key(u) for u in locs}
    expected_keys = {url_key(u) for u in expected}
    extra = sorted(loc_keys - expected_keys)
    short = sorted(expected_keys - loc_keys)
    if extra:
        gate.fail("sitemap.set", f"{len(extra)} 条 URL 不在路由清单里 (凭空多出): {extra[:5]}")
    else:
        gate.ok("sitemap.set.no_orphan")
    if short:
        gate.fail("sitemap.set", f"{len(short)} 条路由没进 sitemap: {short[:5]}")
    else:
        gate.ok("sitemap.set.coverage")
    if len(locs) != len(expected):
        gate.fail("sitemap.count", f"条目 {len(locs)} != 路由 {len(routes.get('routes', []))} + 首页 1 = {len(expected)}")
    else:
        gate.ok("sitemap.count")
    if len(locs) < MIN_SITEMAP_ENTRIES:
        gate.fail("sitemap.min", f"条目 {len(locs)} < {MIN_SITEMAP_ENTRIES}")
    else:
        gate.ok("sitemap.min")
    gate.note(f"sitemap {len(locs)} 条 URL (期望 {len(expected)} = 路由 {len(routes.get('routes', []))} + 首页)")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Phase30-C1 数据校验门")
    ap.add_argument("--index", default="web/public/data/index.unified.json")
    ap.add_argument("--routes", default="docs/architecture/web_p0_routes.json")
    ap.add_argument("--sitemap", default="web/public/sitemap.xml")
    args = ap.parse_args(argv)

    gate = Gate()
    index = load_json(Path(args.index), gate, "index")
    routes = load_json(Path(args.routes), gate, "routes")
    by_code = check_unified(index, gate) if index else {}
    if routes:
        check_routes(routes, by_code, gate)
        if args.sitemap == "":
            gate.note("sitemap 校验被 --sitemap 空串跳过 (仅限本地排查, CI 不允许)")
        else:
            check_sitemap(Path(args.sitemap), routes, gate)
    return gate.finish()


if __name__ == "__main__":
    sys.exit(main())
