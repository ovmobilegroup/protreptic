#!/usr/bin/env python3
"""在 CI 中从已提交的 JSON 重建 api/protreptic.db 的 figures 表（纯标准库，无需 sqlalchemy）。

与 api/load_data.py 的装载规则一致：只装载同时具备中英文数据的条目。
用法：  python3 tools/build_figures_db.py [--out api/protreptic.db]
"""
import argparse
import json
import os
import sqlite3
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DDL = """
CREATE TABLE IF NOT EXISTS figures (
    id INTEGER PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    name_zh VARCHAR(200) NOT NULL,
    description_zh TEXT, reason_zh TEXT, steps_zh TEXT, expected_zh TEXT, case_zh TEXT,
    name_en VARCHAR(200) NOT NULL,
    description_en TEXT, reason_en TEXT, steps_en TEXT, expected_en TEXT, case_en TEXT,
    modes TEXT, era VARCHAR(50),
    historical_domains TEXT, domains TEXT,
    gender VARCHAR(20), ethnicity VARCHAR(20)
);
CREATE INDEX IF NOT EXISTS idx_figure_code ON figures(code);
CREATE INDEX IF NOT EXISTS idx_figure_era ON figures(era);
"""


def ser(v):
    if v is None:
        return "[]"
    if isinstance(v, (list, dict)):
        return json.dumps(v, ensure_ascii=False)
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)


def find(*cands):
    for c in cands:
        p = os.path.join(REPO, c)
        if os.path.exists(p):
            return p
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(REPO, "api", "protreptic.db"))
    args = ap.parse_args()

    zh_path = find("tools/json/scenarios_zh.json", "tools/scenarios_zh.json")
    en_path = find("tools/json/scenarios_en.json", "tools/scenarios_en.json")
    tags_path = find("tools/scenario_tags.json", "tools/json/scenario_tags.json")
    if not zh_path or not en_path:
        print("[FAIL] 缺少 scenarios_zh/en.json", file=sys.stderr)
        return 1

    zh = json.load(open(zh_path, encoding="utf-8"))
    en = json.load(open(en_path, encoding="utf-8"))
    tags = {}
    if tags_path:
        tags = json.load(open(tags_path, encoding="utf-8")).get("tags", {})

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    conn = sqlite3.connect(args.out)
    conn.executescript(DDL)
    conn.execute("DELETE FROM figures")

    n = 0
    for code, z in zh.items():
        if not isinstance(z, dict) or not str(code).strip():
            continue
        e = en.get(code)
        if not str(code).strip():
            continue
        if not isinstance(e, dict) or not e:
            continue  # 规则同 load_data.py：无英文数据跳过
        t = tags.get(code, {}) if isinstance(tags.get(code, {}), dict) else {}
        conn.execute(
            """INSERT OR REPLACE INTO figures
               (code, name_zh, name_en, description_zh, description_en,
                reason_zh, reason_en, steps_zh, steps_en, expected_zh, expected_en,
                case_zh, case_en, modes, era, historical_domains, domains, gender, ethnicity)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            # 键接驳（W4 §三）: 新 schema 用 name; legacy 批次仅存 name_zh/name_en —— 双读回退，防重建回落
            (code, z.get("name") or z.get("name_zh") or "",
             e.get("name") or e.get("name_en") or "",
             ser(z.get("description", "")), ser(e.get("description", "")),
             ser(z.get("reason", "")), ser(e.get("reason", "")),
             ser(z.get("steps", [])), ser(e.get("steps", [])),
             ser(z.get("expected", [])), ser(e.get("expected", [])),
             ser(z.get("case", "")), ser(e.get("case", "")),
             ser(z.get("modes", [])), t.get("era"),
             ser(t.get("historical_domains", [])), ser(t.get("domains", [])),
             t.get("gender"), t.get("ethnicity")))
        n += 1
    conn.commit()
    total = conn.execute("SELECT COUNT(*) FROM figures").fetchone()[0]
    conn.close()
    print(f"✅ figures 表重建完成: {total} 行 -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
