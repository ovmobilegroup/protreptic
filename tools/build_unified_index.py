#!/usr/bin/env python3
"""构建统一索引 web/public/data/index.unified.json

合并两套体系：
  1) 人物（284）  —— data/modes_data.json 按 figure_code 聚合 + data/figures/*.json 元数据
  2) 场景（N）    —— api/protreptic.db 的 figures 表（源自 tools/json/scenarios_*.json）

统一形状（前端只读这一个文件即可同时浏览人物与场景）：
  {
    "code": "H-INM-001", "name": "稻盛和夫", "type": "figure",
    "era": "Modern", "domains": [...], "historical_domains": [...],
    "gender": "...", "ethnicity": "...", "n_modes": 10,
    "description": "...", "href": "/minds/H-INM-001"
  }

用法：python3 tools/build_unified_index.py [--out web/public/data/index.unified.json]
依赖：data/modes_data.json（必需）、api/protreptic.db（可选，缺失则只输出人物）
"""
import argparse
import json
import os
import sqlite3
import sys
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 隔离名单：已确证为虚构记录，不进入公开名录（保留在源数据，可复核回滚）
# H-SX-001「苏咸」：全部 10 条模式皆引《苏咸子·权变篇/纵横篇/…》——该人物与该书均不存在
# （检索仅得「苏秦」；《汉书·艺文志》纵横家著录为《苏子》31 篇，无《苏咸子》）。判为虚构，隔离。
QUARANTINE = {
    'H-SX-001': '引证伪造典籍《苏咸子》，人物与书皆不存在',
}


def _norm(v):
    if isinstance(v, list):
        return str(v[0]).strip() if v else ''
    return str(v or '').strip()


def load_names():
    """多源人名 + 元数据（只取既有数据，不臆造）：figure_names.json → data/figures/*.json

    返回 (names, meta)：names[code]=中文名，meta[code]=人物档案 dict（era/domains/…）
    """
    names, meta = {}, {}

    fn_path = os.path.join(REPO, 'data', 'figure_names.json')
    if os.path.exists(fn_path):
        try:
            for k, v in json.load(open(fn_path, encoding='utf-8')).items():
                n = _norm(v)
                if n:
                    names[k] = n
        except Exception:
            pass

    fig_dir = os.path.join(REPO, 'data', 'figures')
    if os.path.isdir(fig_dir):
        for fn in os.listdir(fig_dir):
            if not fn.endswith('.json'):
                continue
            try:
                d = json.load(open(os.path.join(fig_dir, fn), encoding='utf-8'))
            except Exception:
                continue
            code = str(d.get('figure_code') or d.get('code') or fn[:-5])
            meta[code] = d
            n = _norm(d.get('figure_name_zh')) or _norm(d.get('figure_name'))
            if n and code not in names:
                names[code] = n
    return names, meta


def load_persons():
    md_path = os.path.join(REPO, 'data', 'modes_data.json')
    md = json.load(open(md_path, encoding='utf-8'))
    modes = md.get('modes', [])

    groups = {}
    for m in modes:
        fc = str(m.get('figure_code') or '').strip()
        if not fc or fc in QUARANTINE:
            continue
        g = groups.setdefault(fc, {'n': 0, 'definition': '', 'name': ''})
        g['n'] += 1
        if not g['name']:
            g['name'] = _norm(m.get('figure_name'))
        if not g['definition']:
            g['definition'] = _norm(m.get('definition_zh')) or _norm(m.get('definition_en'))

    named, meta = load_names()
    out = []
    for fc, g in groups.items():
        d = meta.get(fc, {})
        out.append({
            'code': fc,
            'name': g['name'] or named.get(fc, ''),
            'type': 'figure',
            'era': d.get('era') or '',
            'domains': d.get('domains') or [],
            'historical_domains': d.get('historical_domains') or [],
            'gender': d.get('gender') or '',
            'ethnicity': d.get('ethnicity') or '',
            'n_modes': g['n'],
            'description': (g['definition'] or '')[:140],
            'href': f'#/minds/{fc}',
        })
    return out


def load_scenarios():
    db = os.path.join(REPO, 'api', 'protreptic.db')
    if not os.path.exists(db):
        print('[warn] api/protreptic.db 不存在，跳过场景', file=sys.stderr)
        return []

    def j(v):
        if not v:
            return []
        try:
            return json.loads(v)
        except Exception:
            return []

    con = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
    rows = con.execute(
        'SELECT code, name_zh, name_en, description_zh, era, historical_domains, domains, '
        'gender, ethnicity, modes FROM figures'
    ).fetchall()
    con.close()

    out = []
    for code, nz, ne, desc, era, hd, dm, gd, et, modes in rows:
        if not str(code).strip():
            continue
        out.append({
            'code': code,
            'name': nz or ne or code,
            'type': 'scenario',
            'era': era or '',
            'domains': j(dm),
            'historical_domains': j(hd),
            'gender': gd or '',
            'ethnicity': et or '',
            'n_modes': len(j(modes)),
            'description': (desc or '')[:140],
            'href': f'#/figures/{code}',
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.join(REPO, 'web', 'public', 'data', 'index.unified.json'))
    args = ap.parse_args()

    persons = load_persons()
    scenarios = load_scenarios()
    merged = persons + scenarios

    # 去重：同一 code 只保留一次（人物优先）
    seen, dedup = set(), []
    for e in merged:
        if e['code'] in seen:
            continue
        seen.add(e['code'])
        dedup.append(e)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    payload = {
        'schema': 'protreptic.unified_index/v1',
        'counts': {
            'total': len(dedup),
            'figures': sum(1 for e in dedup if e['type'] == 'figure'),
            'scenarios': sum(1 for e in dedup if e['type'] == 'scenario'),
            'with_modes': sum(1 for e in dedup if e['n_modes'] > 0),
        },
        'items': dedup,
    }
    json.dump(payload, open(args.out, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))

    size = os.path.getsize(args.out)
    print(f'✅ 统一索引: {args.out}')
    print(f"   total={payload['counts']['total']}  figures={payload['counts']['figures']}  "
          f"scenarios={payload['counts']['scenarios']}  with_modes={payload['counts']['with_modes']}")
    print(f'   体积: {size/1024:.1f} KB')
    eras = Counter(e['era'] for e in dedup if e['type'] == 'figure' and e['era'])
    print(f"   人物时代分布 top6: {eras.most_common(6)}")


if __name__ == '__main__':
    main()
