#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_w9_fclass_fix.py - 终态断言 A-H for card t_d7faccc5 (idempotent, read-only besides temp copies).

A DB end state (1027/1017/10==ten)
B restorable 504 == legacy (from fix-parent snapshot 6f298ca1), 104 code_as_name, 400 true names
C faces: figures.index / shards / unified names match legacy; counts stable
D rebuild-no-regress on a copy (build x1 -> rows equal, 1017/10)
E residual registry: ten 10 (待核名) + code_as_name 104, values consistent
F web index face: before-list 1359 lines, git ls-files web/public/data == 0, all listed paths on disk
G reports + evidence exist and carry expected schema
H routes name==code == 114 (104 + 10), manifest db sha == db sha
"""
from __future__ import annotations
import hashlib, json, os, shutil, sqlite3, subprocess, sys, tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent
CARD = 't_d7faccc5'
FIX_PARENT = '6f298ca1'
TEN = ['BW-KHA-001', 'BW-MAS-001', 'LS-MOS-001', 'MG-RAV-001', 'NA-GEO-001',
       'NA-NUJ-001', 'SZ-MSW-001', 'ZA-ZUM-001', 'ZW-CHA-001', 'ZW-MUG-001']
FAILS = []


def check(name, cond, detail=''):
    ok = bool(cond)
    print(('PASS ' if ok else 'FAIL ') + name + ((' | ' + detail) if detail else ''))
    if not ok:
        FAILS.append(name)
    return ok


def sha256f(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def db_rows(p):
    con = sqlite3.connect('file:%s?mode=ro' % p, uri=True)
    rows = {c: (z or '', e or '') for c, z, e in con.execute('select code, name_zh, name_en from figures')}
    con.close()
    return rows


def run_ab():
    zh = json.load(open(REPO / 'tools/json/scenarios_zh.json', encoding='utf-8'))
    en = json.load(open(REPO / 'tools/json/scenarios_en.json', encoding='utf-8'))

    def legacy(c):
        z = zh.get(c) or {}
        e = en.get(c) or {}
        return (z.get('name') or z.get('name_zh') or ''), (e.get('name') or e.get('name_en') or '')

    db = db_rows(REPO / 'api/protreptic.db')
    named = sorted(c for c, (z, e) in db.items() if z.strip())
    empty = sorted(c for c, (z, e) in db.items() if not z.strip())
    check('A db rows==1027', len(db) == 1027, 'rows=%d' % len(db))
    check('A db named==1017', len(named) == 1017, 'named=%d' % len(named))
    check('A db empty==ten', empty == TEN, 'empty=%r' % (empty[:12],))

    tmpd = Path(tempfile.mkdtemp(prefix='w9fix_verify_'))
    parent_db = tmpd / 'db_parent.sqlite'
    parent_db.write_bytes(subprocess.run(['git', 'show', FIX_PARENT + ':api/protreptic.db'],
                                         cwd=REPO, capture_output=True).stdout)
    prows = db_rows(parent_db)
    p_empty = sorted(c for c, (z, e) in prows.items() if not z.strip())
    restorable = sorted(c for c in p_empty if legacy(c)[0])
    no_source = sorted(c for c in p_empty if not legacy(c)[0])
    code_as_name = sorted(c for c in restorable if legacy(c)[0] == c)
    true_name = sorted(c for c in restorable if legacy(c)[0] != c)
    check('B restorable==504', len(restorable) == 504, 'n=%d' % len(restorable))
    check('B true==400 / code_as==104', len(true_name) == 400 and len(code_as_name) == 104)
    check('B no_source==ten', no_source == TEN)
    bad = [c for c in restorable if db[c][0] != legacy(c)[0] or db[c][1] != legacy(c)[1]]
    check('B 504 names == legacy', not bad, 'bad=%r' % bad[:5])
    check('B 104 still name==code', all(db[c][0] == c for c in code_as_name))
    for c in TEN:
        check('B ten %s still empty' % c, db[c][0] == '' and db[c][1] == '')
    return tmpd


def faces_and_rest(tmpd):
    db = db_rows(REPO / 'api/protreptic.db')
    zh = json.load(open(REPO / 'tools/json/scenarios_zh.json', encoding='utf-8'))
    en = json.load(open(REPO / 'tools/json/scenarios_en.json', encoding='utf-8'))

    def legacy(c):
        z = zh.get(c) or {}
        e = en.get(c) or {}
        return (z.get('name') or z.get('name_zh') or ''), (e.get('name') or e.get('name_en') or '')

    prows = db_rows(tmpd / 'db_parent.sqlite')
    p_empty = sorted(c for c, (z, e) in prows.items() if not z.strip())
    restorable = sorted(c for c in p_empty if legacy(c)[0])
    code_as_name = sorted(c for c in restorable if legacy(c)[0] == c)

    idx = json.load(open(REPO / 'web/public/data/figures.index.json', encoding='utf-8'))
    idxmap = {it['code']: it for it in idx}
    idx_empty = sorted(c for c, it in idxmap.items() if not (it.get('name_zh') or '').strip())
    idx_mism = [c for c in restorable if (idxmap.get(c, {}).get('name_zh') or '') != legacy(c)[0]]
    check('C index non-H empty==ten', idx_empty == TEN, 'n=%d' % len(idx_empty))
    check('C index names == legacy', not idx_mism, 'bad=%d' % len(idx_mism))

    shard_dir = REPO / 'web/public/data/figures'
    shard_files = [f for f in os.listdir(shard_dir) if f.endswith('.json')]
    smism = [c for c in restorable
             if (json.load(open(shard_dir / (c + '.json'), encoding='utf-8')).get('name_zh') or '') != legacy(c)[0]]
    check('C shards 1027 + 0 mismatch', len(shard_files) == 1027 and not smism,
          'files=%d bad=%d' % (len(shard_files), len(smism)))

    uni = json.load(open(REPO / 'web/public/data/index.unified.json', encoding='utf-8'))
    umap = {it['code']: it for it in uni['items']}
    umism = [c for c in restorable if (umap.get(c, {}).get('name') or '') != legacy(c)[0]]
    check('C unified names + counts', not umism and uni.get('counts', {}).get('total') == 1344,
          'bad=%d counts=%r' % (len(umism), uni.get('counts')))

    copy_db = tmpd / 'db_rebuild.sqlite'
    shutil.copy2(REPO / 'api/protreptic.db', copy_db)
    p = subprocess.run(['python3', str(REPO / 'tools/build_figures_db.py'), '--out', str(copy_db)],
                       cwd=REPO, capture_output=True, text=True)
    r2 = db_rows(copy_db)
    check('D rebuild no-regress', p.returncode == 0 and r2 == db,
          'rc=%d rows_equal=%s named=%d' % (p.returncode, r2 == db, sum(1 for c, (z, e) in r2.items() if z.strip())))

    reg = json.load(open(REPO / 'data/audit/phase21w9_fclass_residual_registry.json', encoding='utf-8'))
    reg_ten = [it['code'] for it in reg['ten']['items']]
    check('E registry ten 10 + 待核名', reg['ten']['count'] == 10 and reg['ten']['status'] == '待核名' and sorted(reg_ten) == TEN)
    check('E registry code_as_name 104', reg['code_as_name']['count'] == 104 and sorted(reg['code_as_name']['codes']) == code_as_name)
    check('E registry no invented names', all(not it.get('db_name_zh') and not it.get('legacy_name_zh') for it in reg['ten']['items']))

    lst = REPO / 'data/audit/phase21w9_web_public_data_index_before.txt'
    paths = [l.split('  ', 1)[1] for l in open(lst, encoding='utf-8').read().splitlines() if '  ' in l]
    ls_files = [l for l in subprocess.run(['git', 'ls-files', 'web/public/data'], cwd=REPO,
                                          capture_output=True, text=True).stdout.splitlines() if l.strip()]
    missing = [q for q in paths if not (REPO / q).exists()]
    check('F before-list 1359 + on disk', len(paths) == 1359 and not missing, 'n=%d missing=%d' % (len(paths), len(missing)))
    check('F ls-files == 0', len(ls_files) == 0, 'n=%d' % len(ls_files))

    for rel in ['docs/qa/phase21w9_fclass_fix_report.md', 'docs/qa/phase21w9_fclass_backfill_report.md',
                'docs/qa/phase21w9_fclass_fix_evidence.json']:
        check('G exists %s' % rel, (REPO / rel).exists())
    ev = json.load(open(REPO / 'docs/qa/phase21w9_fclass_fix_evidence.json', encoding='utf-8'))
    check('G evidence schema', ev.get('schema') == 'protreptic.phase21w9_fclass_fix_evidence/v1'
          and ev.get('decomposition', {}).get('restorable_504') == 504)

    routes = json.load(open(REPO / 'docs/architecture/web_p0_routes.json', encoding='utf-8'))
    rcode = sorted(r['code'] for r in routes['routes'] if (r.get('name') or '') == r.get('code'))
    check('H routes name==code 114', len(rcode) == 114 and rcode == sorted(code_as_name + TEN),
          'n=%d' % len(rcode))
    man = json.load(open(REPO / 'docs/architecture/static_data_manifest.json', encoding='utf-8'))
    check('H manifest db sha == db', man['sources']['api/protreptic.db']['sha256'] == sha256f(REPO / 'api/protreptic.db'))

    shutil.rmtree(tmpd, ignore_errors=True)


def main():
    tmpd = run_ab()
    faces_and_rest(tmpd)
    print('---')
    if FAILS:
        print('RESULT: FAIL (%d) -> %s' % (len(FAILS), ', '.join(FAILS)))
        return 1
    print('RESULT: PASS (A-H)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
