#!/usr/bin/env python3
"""临时探针: 打印两仓的数据基线差异 (非交付物, 用完即删)."""
import json
from pathlib import Path

for label, root in [("workspace", Path("/opt/data/workspace/Protreptic")),
                    ("publish", Path("/opt/data/release/Protreptic-publish"))]:
    print("=== %s ===" % label)
    for rel in ["web/public/data/index.unified.json",
                "docs/architecture/web_p0_routes.json",
                "web/public/data/figures.index.json",
                "web/public/data/meta.json"]:
        p = root / rel
        if not p.exists():
            print("  MISSING %s" % rel)
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(d, dict):
            keys = {k: (len(v) if isinstance(v, list) else v) for k, v in d.items() if not isinstance(v, dict)}
            print("  %s -> %s" % (rel, keys))
        else:
            print("  %s list len=%d" % (rel, len(d)))
    tm = root / "web/public/templates"
    print("  templates=%s" % (sorted(q.stem for q in tm.glob("*.md")) if tm.is_dir() else "NO DIR"))
    print("  robots.txt=%s sitemap.xml=%s" % ((root / "web/public/robots.txt").exists(),
                                              (root / "web/public/sitemap.xml").exists()))
