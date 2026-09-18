#!/usr/bin/env python3
"""build_graph_data.py - Phase30-B1 关系图谱数据构建。"""
from __future__ import annotations
import argparse, gzip, hashlib, json, sqlite3, sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = REPO_ROOT / "web" / "public" / "data" / "graph"
MODES_JSON = REPO_ROOT / "data" / "modes_data.json"
DB_PATH = REPO_ROOT / "api" / "protreptic.db"
GZIP_LEVEL = 9
TOTAL_GZIP_BUDGET_KB = 1500
PER_FILE_GZIP_BUDGET_KB = 500
TOP_N_SIMILAR = 10

def log(*a): print(*a, flush=True)
def sha256_bytes(data): return hashlib.sha256(data).hexdigest()
def dump_bytes(obj): return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
def human(n):
    if n >= 1024*1024: return f"{n/1024/1024:.2f} MB"
    if n >= 1024: return f"{n/1024:.1f} KB"
    return f"{n} B"


def flatten_concepts(val):
    """Flatten nested concept lists to flat string list."""
    if isinstance(val, str):
        try:
            val = json.loads(val)
        except:
            return []
    if not isinstance(val, list):
        return []
    result = []
    for item in val:
        if isinstance(item, str):
            result.append(item)
        elif isinstance(item, list):
            result.extend(flatten_concepts(item))
    return [c for c in result if c]

def load_modes():
    if not MODES_JSON.is_file(): raise SystemExit(f"[FAIL] 缺少 {MODES_JSON}")
    raw = json.loads(MODES_JSON.read_text(encoding="utf-8"))
    modes = raw.get("modes")
    if not isinstance(modes, list): raise SystemExit("[FAIL] modes 不是列表")
    seen, kept = set(), []
    for m in modes:
        mc = m.get("mode_code")
        if mc and mc not in seen: seen.add(mc); kept.append(m)
    return kept

def load_db_modes():
    """mode_code -> key_concepts。

    首选 data/modes_data.json：CI 里 api/protreptic.db 由 build_figures_db.py 现场重建，
    只建 figures 表，**没有 thinking_modes 表**；旧实现直接查该表会
    `sqlite3.OperationalError: no such table: thinking_modes` 并让整个 Pages 部署失败。
    DB 只作回退（本地开发库可能带该表），且任何 DB 错误都不再抛出。
    """
    result = {}
    try:
        for m in load_modes():
            mc = m.get("mode_code")
            kc = m.get("key_concepts")
            if not mc or not kc:
                continue
            if isinstance(kc, str):
                try: kc = json.loads(kc)
                except Exception: kc = []
            if isinstance(kc, list) and kc:
                result[mc] = kc
    except Exception:
        result = {}
    if result:
        return result

    if not DB_PATH.is_file():
        return result
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cur = conn.cursor()
        cur.execute("SELECT mode_code, key_concepts FROM thinking_modes WHERE key_concepts IS NOT NULL AND key_concepts != '[]'")
        for mc, kc in cur.fetchall():
            try:
                if isinstance(kc, str): kc = json.loads(kc)
                if isinstance(kc, list): result[mc] = kc
            except Exception: pass
        conn.close()
    except sqlite3.Error:
        pass
    return result

def build_mode_edges(modes):
    edge_set, nodes = set(), set()
    for m in modes:
        mc = m.get("mode_code")
        if not mc: continue
        nodes.add(mc)
        for t in (m.get("related_modes") or []):
            if t and t != mc:
                nodes.add(t)
                edge_set.add(tuple(sorted((mc, t))))
    return sorted(nodes), sorted(edge_set)

def build_concept_graph(modes, db_modes):
    fig_nodes, conc_nodes, edge_set = set(), set(), set()
    for m in modes:
        fc = m.get("figure_code")
        if not fc: continue
        fig_nodes.add(fc)
        kc = flatten_concepts(m.get("key_concepts"))
        if not kc:
            kc = db_modes.get(m.get("mode_code"), [])
        for c in kc:
            if isinstance(c, str) and c:
                conc_nodes.add(c)
                edge_set.add((fc, c))
    return sorted(fig_nodes), sorted(conc_nodes), sorted(edge_set)

def build_similar_modes(modes, top_n=TOP_N_SIMILAR):
    mode_map = {m["mode_code"]: m for m in modes if m.get("mode_code")}
    concept_to_modes = defaultdict(set)
    for m in modes:
        for c in flatten_concepts(m.get("key_concepts")):
            if isinstance(c, str) and c: concept_to_modes[c].add(m["mode_code"])
    result = {}
    for mc_a in sorted(mode_map):
        m_a = mode_map[mc_a]
        domain_a = m_a.get("domain_zh", "")
        kc_a = set(flatten_concepts(m_a.get("key_concepts")))
        if not kc_a: result[mc_a] = []; continue
        scores = {}
        for c in kc_a:
            for mc_b in concept_to_modes.get(c, set()):
                if mc_b == mc_a: continue
                scores[mc_b] = scores.get(mc_b, (0, False))
                count, _ = scores[mc_b]; scores[mc_b] = (count+1, _)
        for mc_b in list(scores):
            if domain_a and mode_map.get(mc_b, {}).get("domain_zh") == domain_a:
                count, _ = scores[mc_b]; scores[mc_b] = (count, True)
        ranked = []
        for mc_b, (shared_count, same_domain) in scores.items():
            kc_b = mode_map.get(mc_b, {}).get("key_concepts") or []
            kc_b_flat = [x for x in kc_b if isinstance(x, str)]
            shared = sorted(kc_a & set(kc_b_flat))
            ranked.append({"mode_code": mc_b, "score": shared_count + (1 if same_domain else 0),
                          "shared_concepts": shared[:5], "same_domain": same_domain})
        ranked.sort(key=lambda x: (-x["score"], x["mode_code"]))
        result[mc_a] = ranked[:top_n]
    return result

def write_json_gzip(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = dump_bytes(obj); path.write_bytes(raw)
    gz = gzip.compress(raw, GZIP_LEVEL, mtime=0)
    gz_path = path.with_suffix(path.suffix + ".gz")
    gz_path.write_bytes(gz)
    return {"path": str(path.relative_to(REPO_ROOT)), "raw_bytes": len(raw), "gzip_bytes": len(gz), "sha256": sha256_bytes(raw)}

def run(out_dir, assert_budget=True, quiet=False):
    if len(out_dir.parts) < 4: raise SystemExit(f"[FAIL] 路径太浅: {out_dir}")
    if not quiet: log(f"仓库根: {REPO_ROOT}  输出: {out_dir}")
    modes = load_modes()
    db_modes = load_db_modes()
    if not quiet: log(f"  modes: {len(modes)}, db_modes: {len(db_modes)}")
    mode_nodes, mode_edges = build_mode_edges(modes)
    mode_graph = {"schema": "protreptic.mode_graph/v1", "generated_at": datetime.now(timezone.utc).isoformat(),
                  "nodes": mode_nodes, "edges": mode_edges, "stats": {"n_nodes": len(mode_nodes), "n_edges": len(mode_edges)}}
    mode_stat = write_json_gzip(out_dir / "mode_edges.json", mode_graph)
    fig_nodes, conc_nodes, conc_edges = build_concept_graph(modes, db_modes)
    concept_graph = {"schema": "protreptic.concept_graph/v1", "generated_at": datetime.now(timezone.utc).isoformat(),
                     "figure_nodes": fig_nodes, "concept_nodes": conc_nodes, "edges": conc_edges,
                     "stats": {"n_figures": len(fig_nodes), "n_concepts": len(conc_nodes), "n_edges": len(conc_edges)}}
    concept_stat = write_json_gzip(out_dir / "concept_graph.json", concept_graph)
    similar = build_similar_modes(modes)
    similar_data = {"schema": "protreptic.similar_modes/v1", "generated_at": datetime.now(timezone.utc).isoformat(),
                    "top_n": TOP_N_SIMILAR, "modes": similar, "stats": {"n_modes": len(similar), "total_neighbors": sum(len(v) for v in similar.values())}}
    similar_stat = write_json_gzip(out_dir / "similar_modes.json", similar_data)
    stats = {"generated_at": datetime.now(timezone.utc).isoformat(), "products": [mode_stat, concept_stat, similar_stat],
             "total_raw_bytes": mode_stat["raw_bytes"]+concept_stat["raw_bytes"]+similar_stat["raw_bytes"],
             "total_gzip_bytes": mode_stat["gzip_bytes"]+concept_stat["gzip_bytes"]+similar_stat["gzip_bytes"],
             "counts": {"mode_nodes": len(mode_nodes), "mode_edges": len(mode_edges), "figure_nodes": len(fig_nodes),
                        "concept_nodes": len(conc_nodes), "concept_edges": len(conc_edges), "similar_modes_entries": len(similar)}}
    (out_dir / "meta.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    if not quiet:
        log(""); log("== 产出 ==")
        for s in [mode_stat, concept_stat, similar_stat]: log(f"  {s['path']}: raw={human(s['raw_bytes'])} gzip={human(s['gzip_bytes'])}")
        log(f"  总计 gzip: {human(stats['total_gzip_bytes'])}")
        log(f"  模式图: {stats['counts']['mode_nodes']} 节点, {stats['counts']['mode_edges']} 边")
        log(f"  概念图: {stats['counts']['figure_nodes']} 人物, {stats['counts']['concept_nodes']} 概念, {stats['counts']['concept_edges']} 边")
    if assert_budget:
        failures = []
        if stats["total_gzip_bytes"] > TOTAL_GZIP_BUDGET_KB * 1024: failures.append(f"总 gzip {human(stats['total_gzip_bytes'])} > {TOTAL_GZIP_BUDGET_KB} KB")
        for s in [mode_stat, concept_stat, similar_stat]:
            if s["gzip_bytes"] > PER_FILE_GZIP_BUDGET_KB * 1024: failures.append(f"{s['path']} gzip {human(s['gzip_bytes'])} > {PER_FILE_GZIP_BUDGET_KB} KB")
        if failures:
            for f in failures: log(f"  [FAIL] {f}")
            return 1
    return 0

def main(argv=None):
    ap = argparse.ArgumentParser(description="构建关系图谱数据")
    ap.add_argument("--out", default=str(DEFAULT_OUT)); ap.add_argument("--no-assert-budget", action="store_true")
    ap.add_argument("--quiet", action="store_true"); ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv); out = Path(args.out); out = (REPO_ROOT / out).resolve() if not out.is_absolute() else out
    if args.self_test:
        log("自检..."); modes = load_modes(); db_modes = load_db_modes()
        mn, me = build_mode_edges(modes); fn, cn, ce = build_concept_graph(modes, db_modes); sim = build_similar_modes(modes)
        checks = [("mode_nodes>0", len(mn)>0), ("mode_edges>0", len(me)>0), ("fig_nodes>0", len(fn)>0),
                  ("conc_nodes>0", len(cn)>0), ("conc_edges>0", len(ce)>0), ("similar>=0", all(len(v)>=0 for v in sim.values()))]
        ok = True
        for name, r in checks: log(f"  [{'PASS' if r else 'FAIL'}] {name}"); ok = ok and r
        return 0 if ok else 1
    return run(out, assert_budget=not args.no_assert_budget, quiet=args.quiet)

if __name__ == "__main__": sys.exit(main())
