#!/usr/bin/env python3
"""measure_web_p0_baseline.py -- Phase30-A0 的取证脚本, 输出架构方案引用的全部体积基线.

回答三个问题的可复现证据:
  1) 预渲染: 路由数 / 每路由 HTML 体积 / 离线最小集
  2) Service Worker: app shell 与各数据分片的 raw / gzip 体积
  3) 全文检索: 全库可索引正文字符数(多口径) + 字段分布

产物: docs/architecture/web_p0_baseline.json  (机器可读, 供 A1/A4/A5/C1 卡引用)
用法: python3 tools/measure_web_p0_baseline.py [--dist web/dist] [--out <path>]
退出码: 0 成功; 1 输入缺失.
"""
from __future__ import annotations
import argparse, glob, gzip, hashlib, json, os, statistics, sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "web" / "public" / "data"


def gz(data: bytes) -> int:
    return len(gzip.compress(data, 9, mtime=0))


def fsize(path: Path):
    b = path.read_bytes()
    return {"raw_bytes": len(b), "gzip_bytes": gz(b), "sha256": hashlib.sha256(b).hexdigest()}


def flat(value) -> str:
    out = []

    def walk(o):
        if isinstance(o, str):
            out.append(o)
        elif isinstance(o, dict):
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(value)
    return "".join(out)


def measure_data():
    res = {"products": {}, "corpus": {}}
    idx = DATA / "figures.index.json"
    if idx.is_file():
        res["products"]["figures.index.json"] = fsize(idx)
    uni = DATA / "index.unified.json"
    if uni.is_file():
        u = json.loads(uni.read_text(encoding="utf-8"))
        res["products"]["index.unified.json"] = fsize(uni)
        res["products"]["index.unified.json"]["count"] = len(u["items"])
        res["products"]["index.unified.json"]["counts"] = u.get("counts")

    mode_shards = sorted(glob.glob(str(DATA / "modes" / "index-*.json")))
    per = []
    for p in mode_shards:
        per.append({"file": os.path.basename(p), **fsize(Path(p))})
    res["products"]["modes/index-*.json"] = {
        "count_shards": len(per), "shards": per,
        "raw_bytes": sum(s["raw_bytes"] for s in per),
        "gzip_bytes": sum(s["gzip_bytes"] for s in per),
    }

    fig_shards = sorted(glob.glob(str(DATA / "figures" / "*.json")))
    sizes_raw = [os.path.getsize(p) for p in fig_shards]
    fig_gz = [gz(Path(p).read_bytes()) for p in fig_shards]
    res["products"]["figures/*.json"] = {
        "count": len(fig_shards),
        "raw_bytes": sum(sizes_raw), "gzip_bytes": sum(fig_gz),
        "raw_median": statistics.median(sizes_raw) if sizes_raw else 0,
        "gzip_median": statistics.median(fig_gz) if fig_gz else 0,
        "gzip_p90": sorted(fig_gz)[int(len(fig_gz) * 0.9)] if fig_gz else 0,
    }

    bf = sorted(glob.glob(str(DATA / "modes" / "by-figure" / "*.json")))
    bf_raw = [os.path.getsize(p) for p in bf]
    bf_gz = [gz(Path(p).read_bytes()) for p in bf]
    res["products"]["modes/by-figure/*.json"] = {
        "count": len(bf),
        "raw_bytes": sum(bf_raw), "gzip_bytes": sum(bf_gz),
        "raw_median": statistics.median(bf_raw) if bf_raw else 0,
        "gzip_median": statistics.median(bf_gz) if bf_gz else 0,
        "gzip_p90": sorted(bf_gz)[int(len(bf_gz) * 0.9)] if bf_gz else 0,
    }

    # 语料口径: 逐条模式把每个字段的字符串长度累加
    fields, n_modes = {}, 0
    for p in bf:
        d = json.loads(Path(p).read_text(encoding="utf-8"))
        for m in d.get("modes", []):
            n_modes += 1
            for k, v in m.items():
                fields[k] = fields.get(k, 0) + len(flat(v))
    zh_keys = [k for k in fields if not k.endswith("_en")]
    en_keys = [k for k in fields if k.endswith("_en")]
    res["corpus"] = {
        "modes": n_modes,
        "chars_zh_fields": sum(fields[k] for k in zh_keys),
        "chars_en_fields": sum(fields[k] for k in en_keys),
        "chars_all": sum(fields.values()),
        "top_fields": sorted(fields.items(), key=lambda kv: -kv[1])[:16],
    }
    return res


def measure_shell(dist: Path):
    out = {"files": {}}
    total_raw = total_gz = 0
    for rel in ("index.html", "404.html"):
        f = dist / rel
        if f.is_file():
            info = fsize(f)
            out["files"][rel] = info
            total_raw += info["raw_bytes"]
            total_gz += info["gzip_bytes"]
    for f in sorted((dist / "assets").glob("*")) if (dist / "assets").is_dir() else []:
        info = fsize(f)
        out["files"]["assets/" + f.name] = info
        total_raw += info["raw_bytes"]
        total_gz += info["gzip_bytes"]
    out["app_shell_raw_bytes"] = total_raw
    out["app_shell_gzip_bytes"] = total_gz
    prerendered = [p for p in dist.rglob("index.html") if p.parent != dist]
    out["prerendered_route_dirs"] = len(prerendered)
    out["prerendered_total_raw_bytes"] = sum(p.stat().st_size for p in prerendered)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dist", default=str(REPO / "web" / "dist"))
    ap.add_argument("--out", default=str(REPO / "docs" / "architecture" / "web_p0_baseline.json"))
    args = ap.parse_args()

    if not DATA.is_dir():
        sys.exit("[baseline] missing %s, run tools/export_static_site.py first" % DATA)

    report = {
        "schema": "protreptic.web_p0_baseline/v1",
        "generated_by": "tools/measure_web_p0_baseline.py",
        "data_dir": str(DATA.relative_to(REPO)),
        "data": measure_data(),
        "dist": measure_shell(Path(args.dist)),
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

    d = report["data"]["products"]
    print("[baseline] figures.index.json      %6.1f KB raw / %6.1f KB gzip" % (d["figures.index.json"]["raw_bytes"] / 1024, d["figures.index.json"]["gzip_bytes"] / 1024))
    if "index.unified.json" in d:
        print("[baseline] index.unified.json      %6.1f KB raw / %6.1f KB gzip" % (d["index.unified.json"]["raw_bytes"] / 1024, d["index.unified.json"]["gzip_bytes"] / 1024))
    print("[baseline] modes/index-*.json      %6.1f KB raw / %6.1f KB gzip" % (d["modes/index-*.json"]["raw_bytes"] / 1024, d["modes/index-*.json"]["gzip_bytes"] / 1024))
    print("[baseline] modes/by-figure/*.json  %6.1f MB raw / %6.1f MB gzip  median %5.1f KB gzip" % (d["modes/by-figure/*.json"]["raw_bytes"] / 1e6, d["modes/by-figure/*.json"]["gzip_bytes"] / 1e6, d["modes/by-figure/*.json"]["gzip_median"] / 1024))
    print("[baseline] figures/*.json          %6.1f MB raw / %6.1f MB gzip  median %5.1f KB gzip" % (d["figures/*.json"]["raw_bytes"] / 1e6, d["figures/*.json"]["gzip_bytes"] / 1e6, d["figures/*.json"]["gzip_median"] / 1024))
    s = report["dist"]
    print("[baseline] app shell               %6.1f KB raw / %6.1f KB gzip" % (s["app_shell_raw_bytes"] / 1024, s["app_shell_gzip_bytes"] / 1024))
    print("[baseline] prerendered route dirs  %d (%6.1f KB raw)" % (s["prerendered_route_dirs"], s["prerendered_total_raw_bytes"] / 1024))
    print("[baseline] -> %s" % out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
