#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_w9_fclass_fix_evidence.py -- Phase21-W9-fix (t_d7faccc5) evidence generator (idempotent).

Recomputes from repo state + run logs and writes:
  data/audit/phase21w9_fclass_residual_registry.json   residual registry
  docs/qa/phase21w9_fclass_fix_evidence.json           machine-readable evidence

Usage:
  python3 build_w9_fclass_fix_evidence.py [--logs DIR] [--check]
"""
from __future__ import annotations

import argparse, hashlib, json, os, sqlite3, subprocess, sys, time
from pathlib import Path

REPO = Path(__file__).resolve().parent
TEN = ['BW-KHA-001', 'NA-NUJ-001', 'SZ-MSW-001', 'ZW-MUG-001', 'ZA-ZUM-001',
       'BW-MAS-001', 'LS-MOS-001', 'MG-RAV-001', 'NA-GEO-001', 'ZW-CHA-001']
FIX_PARENT = '6f298ca1'
RECON = '8adbdabd'
AUDITED = 'e5ddd13f'
REGISTRY = REPO / 'data' / 'audit' / 'phase21w9_fclass_residual_registry.json'
EVIDENCE = REPO / 'docs' / 'qa' / 'phase21w9_fclass_fix_evidence.json'


def sha256f(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def sha16f(p):
    return sha256f(p)[:16]


def git_show(revpath, dest):
    p = subprocess.run(['git', 'show', revpath], cwd=REPO, capture_output=True)
    if p.returncode != 0:
        return None
    Path(dest).write_bytes(p.stdout)
    return dest


def db_rows(path):
    con = sqlite3.connect('file:%s?mode=ro' % path, uri=True)
    rows = {c: (z or '', e or '') for c, z, e in con.execute('select code, name_zh, name_en from figures')}
    con.close()
    return rows


def load_json(p, default=None):
    try:
        return json.load(open(p, encoding='utf-8'))
    except Exception:
        return default


def gather():
    ap = argparse.ArgumentParser()
    ap.add_argument('--logs', default='/opt/data/profiles/elcano/cache/scratch/w9fix')
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    L = Path(args.logs)

    zh = json.load(open(REPO / 'tools/json/scenarios_zh.json', encoding='utf-8'))
    en = json.load(open(REPO / 'tools/json/scenarios_en.json', encoding='utf-8'))

    def legacy(c):
        z = zh.get(c) or {}
        e = en.get(c) or {}
        return (z.get('name') or z.get('name_zh') or ''), (e.get('name') or e.get('name_en') or '')

    now_db = db_rows(REPO / 'api/protreptic.db')
    named = sorted(c for c, (z, e) in now_db.items() if z.strip())
    empty = sorted(c for c, (z, e) in now_db.items() if not z.strip())
    parent_db = L / 'db_parent.sqlite'
    if not parent_db.exists():
        git_show(FIX_PARENT + ':api/protreptic.db', parent_db)
    prows = db_rows(parent_db)
    p_empty = sorted(c for c, (z, e) in prows.items() if not z.strip())
    restorable = sorted(c for c in p_empty if legacy(c)[0])
    no_source = sorted(c for c in p_empty if not legacy(c)[0])
    code_as_name = sorted(c for c in restorable if legacy(c)[0] == c)
    true_name = sorted(c for c in restorable if legacy(c)[0] != c)
    assert no_source == empty, 'ten mismatch: %r' % (set(no_source) ^ set(empty))
    assert not (set(restorable) & set(empty)), 'restorable still empty'
    assert all(now_db[c][0] == legacy(c)[0] for c in restorable), 'restorable != legacy'

    recon_db = L / 'db_w4recon.sqlite'
    if not recon_db.exists():
        git_show(RECON + ':api/protreptic.db', recon_db)
    old = db_rows(recon_db) if recon_db.exists() else None
    recon = None
    if old:
        o_empty = {c for c, (z, e) in old.items() if not z.strip()}
        n_empty = set(empty)
        removed = sorted(set(old) - set(now_db))
        added = sorted(set(now_db) - set(old))
        named_in_place = sorted(c for c in (set(old) & set(now_db))
                                if not old[c][0].strip() and now_db[c][0].strip())
        recon = {
            'recon_period': {'commit': RECON, 'rows': len(old),
                             'empty_total': len(o_empty),
                             'empty_h': sum(1 for c in o_empty if c.startswith('H-')),
                             'empty_nonh': sum(1 for c in o_empty if not c.startswith('H-'))},
            'current': {'rows': len(now_db), 'named': len(named), 'empty': len(empty)},
            'empty_resolved': len(o_empty - n_empty),
            'attr': {'rows_removed': len(removed), 'rows_added': len(added),
                     'removed_list': removed, 'added_list': added,
                     'named_in_place': named_in_place,
                     'named_in_place_nonh': [c for c in named_in_place if not c.startswith('H-')],
                     'new_empty': sorted(n_empty - o_empty)},
            'delta_537_vs_504': {'w4_nonh_with_legacy': 537,
                                 'now_restorable': len(restorable),
                                 'diff': 537 - len(restorable),
                                 'attribution': '31 rows removed (RW-KAG-1..27 + JP-Sas-001/MY-Mah-001/SG-Lee-001/UZ-Ulu-001) + 2 rows already named (RW-KAG-001, SG-LEE-001); no new empty'},
            'row_drift': '1056 -> 1027 = -31 removed +2 added (JP-SAS-001, UZ-ULU-001)',
        }

    idx = json.load(open(REPO / 'web/public/data/figures.index.json', encoding='utf-8'))
    idxmap = {it['code']: it for it in idx}
    idx_empty = sorted(c for c, it in idxmap.items() if not (it.get('name_zh') or '').strip())
    idx_mism = [c for c in restorable if (idxmap.get(c, {}).get('name_zh') or '') != legacy(c)[0]
                or (idxmap.get(c, {}).get('name_en') or '') != legacy(c)[1]]
    shard_dir = REPO / 'web/public/data/figures'
    shard_files = [f for f in os.listdir(shard_dir) if f.endswith('.json')]
    smism, smiss = [], []
    for c in restorable:
        p = shard_dir / (c + '.json')
        if not p.exists():
            smiss.append(c)
            continue
        d = json.load(open(p, encoding='utf-8'))
        if (d.get('name_zh') or '') != legacy(c)[0] or (d.get('name_en') or '') != legacy(c)[1]:
            smism.append(c)
    uni = json.load(open(REPO / 'web/public/data/index.unified.json', encoding='utf-8'))
    umap = {it['code']: it for it in uni['items']}
    unii_mism = [c for c in restorable if (umap.get(c, {}).get('name') or '') != legacy(c)[0]]
    man = json.load(open(REPO / 'docs/architecture/static_data_manifest.json', encoding='utf-8'))
    routes = json.load(open(REPO / 'docs/architecture/web_p0_routes.json', encoding='utf-8'))
    routes_code_as = sorted(r['code'] for r in routes['routes'] if (r.get('name') or '') == r.get('code'))
    faces = {
        'db': {'rows': len(now_db), 'named': len(named), 'empty': empty,
               'sha256': sha256f(REPO / 'api/protreptic.db'),
               'name_eq_code': sum(1 for c, (z, e) in now_db.items() if z == c)},
        'figures_index': {'count': len(idx), 'empty_nonh': idx_empty, 'name_mismatch': idx_mism,
                          'sha256': sha256f(REPO / 'web/public/data/figures.index.json')},
        'shards': {'count': len(shard_files), 'name_mismatch': smism, 'missing': smiss},
        'unified': {'counts': uni.get('counts'), 'name_mismatch': unii_mism,
                    'sha256': sha256f(REPO / 'web/public/data/index.unified.json')},
        'manifest': {'db_sha_match': man['sources']['api/protreptic.db']['sha256'] == sha256f(REPO / 'api/protreptic.db'),
                     'generated_at': man.get('generated_at'),
                     'sha256': sha256f(REPO / 'docs/architecture/static_data_manifest.json')},
        'routes_name_eq_code': {'count': len(routes_code_as),
                                'expect': sorted(code_as_name + no_source) == routes_code_as},
        'sample_AE-FED-001': {'db': list(now_db.get('AE-FED-001') or ()),
                              'unified_name': (umap.get('AE-FED-001') or {}).get('name'),
                              'shard_name_zh': json.load(open(shard_dir / 'AE-FED-001.json', encoding='utf-8')).get('name_zh')},
    }
    return {'recon': recon, 'faces': faces, 'named': named, 'empty': empty, 'restorable': restorable,
            'no_source': no_source, 'code_as_name': code_as_name, 'true_name': true_name,
            'zh': zh, 'L': L}


def build_outputs(g):
    L = g['L']
    registry = {
        'schema': 'protreptic.phase21w9_fclass_residual_registry/v1',
        'card': 't_d7faccc5',
        'generated_at': time.strftime('%Y-%m-%dT%H:%M:%S%z'),
        'purpose': '\u5b8c\u6210 W9-F \u4fee\u590d\u540e\u7684\u6b8b\u7559\u767b\u8bb0',
        'ten': {
            'count': len(g['no_source']),
            'status': '\u5f85\u6838\u540d',
            'note': 'scenarios_zh/en entries carry no name keys at all (name/name_zh/name_en missing or empty); no usable source found in site scope; do not invent. Non-adopted leads: data/phase_17_7_southern_africa_modes.json holds draft names for the same codes, data/personas.json legacy files are worth a recheck; adoption needs captain ruling first.',
            'items': [],
        },
        'code_as_name': {
            'count': len(g['code_as_name']),
            'status': '\u5360\u4f4d\u5f85\u8865\u540d',
            'note': 'legacy name_zh == code (placeholder rows, desc mostly stub). After backfill DB/shard/index still show the code, no visual change; real names are a follow-up governance item (R14).',
            'codes': g['code_as_name'],
        },
    }
    ten_meta = {it['code']: it for it in (load_json(L / 'gather.json', {}) or {}).get('ten_items', [])}
    for c in g['no_source']:
        t = ten_meta.get(c, {})
        registry['ten']['items'].append({
            'code': c, 'db_id': t.get('db_id'), 'status': '\u5f85\u6838\u540d',
            'db_name_zh': '', 'db_name_en': '', 'legacy_name_zh': '', 'legacy_name_en': '',
            'nationality': t.get('nationality'), 'civilization_sphere': t.get('civilization_sphere'),
            'n_modes': t.get('n_modes'),
            'evidence': 'tools/json/scenarios_zh.json entry has no name/name_zh; scenarios_en.json has no name/name_en; DB name empty; figures.index/shard/unified all empty.',
        })

    fix_files = []
    for rel, kind in [('tools/build_figures_db.py', 'loader key fallback (name_zh/name_en)'),
                      ('tools/export_static_site.py', 'size budget re-anchor 50KB -> 80KB (W9-F backfill measured 65571B)'),
                      ('api/load_data.py', 'same-class loader key fallback (anti-regrowth)')]:
        before = L / ('before_' + rel.replace('/', '_'))
        if not before.exists():
            git_show(FIX_PARENT + ':' + rel, before)
        fix_files.append({'path': rel, 'kind': kind,
                          'before_sha16': sha16f(before) if before.exists() else None,
                          'after_sha16': sha16f(REPO / rel)})

    evidence = {
        'schema': 'protreptic.phase21w9_fclass_fix_evidence/v1',
        'card': 't_d7faccc5',
        'generated_at': registry['generated_at'],
        'chain': {'fix_parent': FIX_PARENT, 'recon': RECON, 'audited': AUDITED, 'qa_card': 't_9ed2866a'},
        'reconciliation': g['recon'],
        'decomposition': {'empty_total': len(g['empty']), 'restorable_504': len(g['restorable']),
                          'true_name_400': len(g['true_name']), 'code_as_name_104': len(g['code_as_name']),
                          'no_source_ten': g['no_source']},
        'fix': {'files': fix_files,
                'backup': {'path': 'api/protreptic.db.backup_phase21w9fix_20260924_172526',
                           'sha256': 'c4a89a2329b6690bed0f0ac71fa8740aef9f7c9843d33cee829b37fa45e167b2'},
                'order': 'backup -> dry run (copy) -> main DB rebuild x2 -> site chain -> gates/parity -> manifest with commit'},
        'dry_run': load_json(L / 'dry_run_result.json'),
        'execution': load_json(L / 'exec_main_result.json'),
        'site_chain': load_json(L / 'chain_result.json'),
        'site_refresh': load_json(L / 'site_refresh_result.json'),
        'gates': load_json(L / 'gates_final.json') or load_json(L / 'gates_result.json'),
        'faces': g['faces'],
        'web_index_face': load_json(L / 'web_index_face.json'),
        'parity_pre_mirror': load_json(L / 'parity_pre.json', {}),
        'parity_post_mirror': load_json(L / 'parity_post.json', {}),
        'receipt': load_json(L / 'receipt.json', {}),
        'verify_espinosa': load_json(L / 'espinosa_verify.json'),
        'notes': ['RNBW: rebuild from source keeps 1017/10 (dry-run copy x2 + main DB x2 + final copy re-run).',
                  'E1/F11 are assertions against the DEFECT state (0 non-H empties / figures aggregate hash); a legitimate fix necessarily flips them; recorded for t_28a29244 arbitration.'],
    }
    return registry, evidence


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--logs', default='/opt/data/profiles/elcano/cache/scratch/w9fix')
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    g = gather()
    registry, evidence = build_outputs(g)
    if args.check:
        ok = True
        for path, obj in [(REGISTRY, registry), (EVIDENCE, evidence)]:
            same = load_json(path) == obj
            print(('OK  ' if same else 'DIFF') + ' ' + str(path))
            ok &= same
        return 0 if ok else 1
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    json.dump(registry, open(REGISTRY, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(evidence, open(EVIDENCE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('wrote', REGISTRY)
    print('wrote', EVIDENCE)
    return 0


if __name__ == '__main__':
    sys.exit(main())
