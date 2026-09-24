#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_w9_fclass_qa_espinosa.py -- Phase21 W9 F-class backfill: independent QA assertor.

Card: t_9ed2866a (QA, espinosa). Audited: t_0b240eb7 / commit e5ddd13f (parent ee08f5b5).
Re-derived from raw repo state, never from the audited receipts' own claims.
Read-only for both repos: writes only its temp dir (+ --json output if requested).

Groups:
  F*: audited-window facts, pinned to --at (default e5ddd13f). PASS at audit time and after any fix.
  E*: end-state assertions on the live tree. FAIL now (== defect set of the QA report); PASS after a fix.

Usage:
  python3 verify_w9_fclass_qa_espinosa.py                 # F+E groups
  python3 verify_w9_fclass_qa_espinosa.py --at <rev>      # pin another audited revision
  python3 verify_w9_fclass_qa_espinosa.py --json /tmp/x.json
  python3 verify_w9_fclass_qa_espinosa.py --with-parity   # include a live parity re-run (slow)
Exit: 0 = all executed assertions PASS, 1 = any FAIL, 2 = environment error.
"""
from __future__ import annotations

import argparse, hashlib, json, os, sqlite3, subprocess, sys, tempfile, time

WS = '/opt/data/workspace/Protreptic'
PB = '/opt/data/release/Protreptic-publish'
AT = 'e5ddd13f'
PARENT = 'ee08f5b5'
RECON = '8adbdabd'
BAKNAME = 'api/protreptic.db.backup_phase21w9_20260924_140928'
TEN = ['BW-KHA-001', 'NA-NUJ-001', 'SZ-MSW-001', 'ZW-MUG-001', 'ZA-ZUM-001', 'BW-MAS-001', 'LS-MOS-001', 'MG-RAV-001', 'NA-GEO-001', 'ZW-CHA-001']
OLD_FIG_AGG = '6391856f'
OLD_FIGIDX = '65a7cdc6'
UNIFIED_EXPECT = {'total': 1344, 'figures': 320, 'scenarios': 1024}

results = []
def chk(cid, name, ok, detail='', role='F'):
    results.append({'id': cid, 'name': name, 'ok': bool(ok), 'detail': str(detail)[:800], 'role': role})
    print(('PASS' if ok else 'FAIL') + ' [' + cid + '] ' + name + (' :: ' + str(detail)[:220] if detail else ''))
def info(cid, name, detail=''):
    results.append({'id': cid, 'name': name, 'ok': None, 'detail': str(detail)[:800], 'role': 'I'})
    print('INFO [' + cid + '] ' + name + (' :: ' + str(detail)[:220] if detail else ''))

def sh(cmd, cwd=WS, timeout=300):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=timeout)

def blob_bytes(revpath):
    p = subprocess.run(['git', 'cat-file', 'blob', revpath], cwd=WS, capture_output=True)
    if p.returncode != 0:
        return None
    return p.stdout

def blob(revpath, dest):
    b = blob_bytes(revpath)
    if b is None:
        return None
    open(dest, 'wb').write(b)
    return dest

def sha256f(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

def db_rows(p, cols='code,name_zh,name_en'):
    con = sqlite3.connect('file:' + p + '?mode=ro', uri=True)
    cur = con.cursor()
    cur.execute('select ' + cols + ' from figures order by id')
    r = cur.fetchall()
    con.close()
    return r

def db_rowhash(p):
    con = sqlite3.connect('file:' + p + '?mode=ro', uri=True)
    cur = con.cursor()
    cur.execute("select name from sqlite_master where type='table' order by name")
    out = {}
    for (t,) in cur.fetchall():
        cur.execute('select * from "%s"' % t)
        h = hashlib.sha256()
        for r in cur.fetchall():
            h.update(repr(r).encode('utf-8')); h.update(b'\n')
        out[t] = h.hexdigest()
    con.close()
    return out

def agg_tree(sub):
    d = WS + '/web/public/data/' + sub
    if not os.path.isdir(d):
        return None, 0
    h = hashlib.sha256(); n = 0
    items = []
    for f in sorted(os.listdir(d)):
        p = os.path.join(d, f)
        if os.path.isfile(p):
            items.append((sub + '/' + f, sha256f(p))); n += 1
    for rel, dig in sorted(items):
        h.update(rel.encode()); h.update(b'\0'); h.update(dig.encode()); h.update(b'\n')
    return h.hexdigest(), n

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--at', default=AT)
    ap.add_argument('--json', default=None)
    ap.add_argument('--with-parity', action='store_true')
    ap.add_argument('--with-remote', action='store_true')
    a = ap.parse_args()
    at = a.at
    if not os.path.isdir(WS):
        print('env error: workspace missing'); sys.exit(2)
    TMP = tempfile.mkdtemp(prefix='w9qa_')
    t0 = time.time()
    print('== verify_w9_fclass_qa_espinosa :: at=' + at + ' tmp=' + TMP)

    # ---------------- F1: audited commit
    p = sh(['git', 'log', '-1', '--format=%H %P %s', at])
    if p.returncode != 0:
        print('env error: rev not found: ' + at); sys.exit(2)
    parts = p.stdout.strip().split(' ', 2)
    chk('F1', 'audited commit & parent', parts[1].startswith(PARENT), 'parent=' + parts[1][:12] + ' subject=' + parts[2][:60])

    # ---------------- blobs
    db_at = blob(at + ':api/protreptic.db', TMP + '/db_at.db')
    db_par = blob(PARENT + ':api/protreptic.db', TMP + '/db_par.db')
    zh_at = blob(at + ':tools/json/scenarios_zh.json', TMP + '/zh.json')
    en_at = blob(at + ':tools/json/scenarios_en.json', TMP + '/en.json')
    man_at = blob(at + ':docs/architecture/static_data_manifest.json', TMP + '/man_at.json')
    idx_at = blob(at + ':web/public/data/figures.index.json', TMP + '/idx.json')
    uni_at = blob(at + ':web/public/data/index.unified.json', TMP + '/uni.json')
    if not all([db_at, zh_at, en_at, man_at, idx_at, uni_at]):
        print('env error: blob extraction failed'); sys.exit(2)

    zh = json.load(open(zh_at, encoding='utf-8'))
    en = json.load(open(en_at, encoding='utf-8'))
    rows = db_rows(db_at)
    named = sum(1 for c, z, e in rows if (z or '').strip())
    empty = [c for c, z, e in rows if not (z or '').strip()]
    empty_nonh = [c for c in empty if not c.startswith('H-')]
    empty_h = [c for c in empty if c.startswith('H-')]

    def legacy(code):
        z = zh.get(code)
        return (z.get('name_zh') or '') if isinstance(z, dict) else ''

    restorable = [c for c in empty_nonh if legacy(c).strip()]
    no_legacy = [c for c in empty_nonh if not legacy(c).strip()]
    restored = [c for c in restorable if c not in empty]  # named now

    # ---------------- F2/F3/F4: counts & non-backfill
    chk('F2', 'db@at counts: total=1027 named=513 empty=514 (nonH=514, H=0)',
        len(rows) == 1027 and named == 513 and len(empty) == 514 and len(empty_nonh) == 514 and len(empty_h) == 0,
        'total=%d named=%d empty=%d nonh=%d h=%d' % (len(rows), named, len(empty), len(empty_nonh), len(empty_h)))
    chk('F3', 'restorable=504 & no-legacy=10 (ten list)', len(restorable) == 504 and sorted(no_legacy) == sorted(TEN),
        'restorable=%d no_legacy=%d %s' % (len(restorable), len(no_legacy), sorted(no_legacy)[:3]))
    chk('F4', 'restored count among 504 at audited revision == 0 (defect F1)', len(restored) == 0, 'restored=%d' % len(restored))

    # ---------------- F5: db row-equality (M is layout only)
    rh_at = db_rowhash(db_at); rh_par = db_rowhash(db_par)
    bak = WS + '/' + BAKNAME
    rh_bak = db_rowhash(bak) if os.path.exists(bak) else None
    eq = (rh_at == rh_par) and (rh_bak is None or rh_at == rh_bak)
    chk('F5', 'db row content equal (at == parent == backup) -- M is sqlite layout only', eq,
        'rowhash_equal=%s shas at=%s par=%s' % (eq, sha256f(db_at)[:16], sha256f(db_par)[:16]))

    # ---------------- F6: site face empty
    site = {it['code']: (it.get('name_zh') or '') for it in json.load(open(idx_at, encoding='utf-8'))}
    site_empty_nonh = [c for c, v in site.items() if not v.strip() and not c.startswith('H-')]
    chk('F6', 'site figures.index nonH empty == 514; AE-FED-001 shard name_zh empty',
        len(site_empty_nonh) == 514 and site.get('AE-FED-001', None) == '' ,
        'site_nonh_empty=%d AE-FED-001=%r' % (len(site_empty_nonh), site.get('AE-FED-001')))

    # ---------------- F7: unified
    uni = json.load(open(uni_at, encoding='utf-8'))
    uc = uni.get('counts', {})
    uok = all(uc.get(k) == v for k, v in UNIFIED_EXPECT.items())
    chk('F7', 'index.unified counts {1344,320,1024} (at)', uok, json.dumps(uc, ensure_ascii=False))

    # ---------------- F8: deletion face
    ns = sh(['git', 'show', '--name-status', '--format=', '-M', at]).stdout
    D = [l.split('\t', 1)[1] for l in ns.splitlines() if l.startswith('D\t')]
    A = [l.split('\t', 1)[1] for l in ns.splitlines() if l.startswith('A\t')]
    clpath = WS + '/data/audit/phase21w7_classification.json'
    if os.path.exists(clpath):
        cl = json.load(open(clpath, encoding='utf-8'))
        ws_ver = {it['path']: it.get('verdict') for it in cl['items'] if it.get('repo') == 'workspace'}
        planned = {'archive_delete', 'delete'}
        unplanned = [x for x in D if ws_ver.get(x) not in planned]
        keephit = [x for x in D if ws_ver.get(x) == 'keep']
        chk('F8', 'deletion face: 1303 D (633 root+670 tools), 0 unplanned, 0 keep-hit, 1359 web adds',
            len(D) == 1303 and len([x for x in D if '/' not in x]) == 633 and len([x for x in D if x.startswith('tools/json/')]) == 670 and not unplanned and not keephit and len([x for x in A if x.startswith('web/public/data')]) == 1359,
            'D=%d root=%d tools=%d unplanned=%d keep=%d webA=%d' % (len(D), len([x for x in D if '/' not in x]), len([x for x in D if x.startswith('tools/json/')]), len(unplanned), len(keephit), len([x for x in A if x.startswith('web/public/data')])))
    else:
        info('F8', 'deletion face check skipped: classification file missing', '')

    # ---------------- F9: manifest inconsistency in commit tree
    man = json.load(open(man_at, encoding='utf-8'))
    said = man['sources']['api/protreptic.db']['sha256']
    act = sha256f(db_at)
    chk('F9', 'manifest@at says db c5eb.. but db@at is c4a8.. (stale manifest committed)', said != act, 'says=%s actual=%s' % (said[:16], act[:16]))

    # ---------------- F10: delta vs recon
    db_rec = blob(RECON + ':api/protreptic.db', TMP + '/db_rec.db')
    if db_rec:
        rrows = db_rows(db_rec)
        rec_nonh = sorted(c for c, z, e in rrows if not (z or '').strip() and not c.startswith('H-'))
        dbd = {c: (z or '') for c, z, e in rows}
        resolved = sorted(set(rec_nonh) - set(empty_nonh))
        removed = [c for c in resolved if c not in dbd]
        namedc = [c for c in resolved if c in dbd and dbd[c].strip()]
        newe = sorted(set(empty_nonh) - set(rec_nonh))
        chk('F10', 'recon 547 -> 514: resolved 33 (31 rows removed + 2 named), new-empty 0',
            len(rec_nonh) == 547 and len(resolved) == 33 and len(removed) == 31 and len(namedc) == 2 and len(newe) == 0,
            'recon=%d resolved=%d removed=%d named=%d new=%d' % (len(rec_nonh), len(resolved), len(removed), len(namedc), len(newe)))
    else:
        info('F10', 'recon blob unavailable', '')

    # ---------------- F11: H-* boundary / figures byte-stability
    fig_agg, n_fig = agg_tree('figures')
    idx_disk = WS + '/web/public/data/figures.index.json'
    m_now = json.load(open(WS + '/docs/architecture/static_data_manifest.json', encoding='utf-8'))
    ok_fig = fig_agg is not None and fig_agg.startswith(OLD_FIG_AGG) and n_fig == 1027 and m_now['products']['figures/']['sha256'][:8] == OLD_FIG_AGG and man['products']['figures/']['sha256'][:8] == OLD_FIG_AGG
    ok_idx = os.path.exists(idx_disk) and sha256f(idx_disk)[:8] == OLD_FIGIDX and m_now['products']['figures.index.json']['sha256'][:8] == OLD_FIGIDX
    pb_eq = None
    pbf = PB + '/web/public/data/figures'
    if os.path.isdir(pbf):
        same = diff = 0
        for f in sorted(os.listdir(pbf)):
            pw = WS + '/web/public/data/figures/' + f
            pf = pbf + '/' + f
            if os.path.isfile(pw) and os.path.isfile(pf):
                if sha256f(pf) == sha256f(pw):
                    same += 1
                else:
                    diff += 1
        pb_eq = (same, diff)
    chk('F11', 'H-* boundary: figures agg 6391856f (old==new==disk), figures.index 65a7cdc6, ws==pb 1027/0',
        ok_fig and ok_idx and (pb_eq is None or pb_eq == (1027, 0)),
        'fig_agg=%s n=%d idx=%s pb=%s' % ((fig_agg or '')[:8], n_fig, sha256f(idx_disk)[:8] if os.path.exists(idx_disk) else 'n/a', pb_eq))

    # ---------------- F12: push face facts (offline)
    pb_has_w9 = sh(['git', 'log', '--oneline', '--all', '--grep=Phase21-W9'], cwd=PB).stdout.strip() if os.path.isdir(PB + '/.git') else ''
    p_obj = subprocess.run(['git', 'cat-file', '-e', at], cwd=PB, capture_output=True)
    chk('F12', 'publish repo has NO W9 commit and not even object', (pb_has_w9 == '') and (p_obj.returncode != 0), 'grep_hits=%d obj_rc=%d' % (len(pb_has_w9.splitlines()), p_obj.returncode))

    # ================ E group (end-state; FAIL == defects) ================
    # E1: durability of any backfill: worktree db + rebuild-from-source
    wdb = WS + '/api/protreptic.db'
    e1a = None
    if os.path.exists(wdb):
        wrows = db_rows(wdb)
        e1a = len([c for c, z, e in wrows if not (z or '').strip() and not c.startswith('H-')])
    rb = TMP + '/rebuild.db'
    pr = sh(['python3', 'tools/build_figures_db.py', '--out', rb], timeout=300)
    e1b = None
    if pr.returncode == 0 and os.path.exists(rb):
        b_rows = db_rows(rb)
        e1b = len([c for c, z, e in b_rows if not (z or '').strip() and not c.startswith('H-')])
    chk('E1', 'end-state: worktree(=0) AND rebuild-from-source(=0) have no non-H empty names',
        e1a == 0 and e1b == 0, 'worktree_empty=%s rebuild_empty=%s rc=%d' % (e1a, e1b, pr.returncode), role='E')

    # E2: ten disposition (named in db OR registered)
    ten_un = []
    reg_files = []
    for c in TEN:
        z = dbd.get(c, '') if 'dbd' in dir() else ''
        wnamed = False
        if os.path.exists(wdb):
            wrows2 = db_rows(wdb)
            wnamed = any(cc == c and (zz or '').strip() for cc, zz, ee in wrows2)
        if not wnamed:
            ten_un.append(c)
    if ten_un:
        g = sh(['grep', '-rl', '--include=*.json', '--include=*.md', '-E', 'phase21w9', 'data/audit', 'docs/research'])
        cand = [f for f in g.stdout.splitlines() if not any(bad in f.lower() for bad in ('qa_', 'espinosa', 'verify_'))]
        for f in cand:
            try:
                txt = open(WS + '/' + f, encoding='utf-8', errors='replace').read()
            except Exception:
                continue
            if '待核名' in txt and any(c in txt for c in ten_un):
                reg_files.append(f)
    chk('E2', 'end-state: ten codes named in db OR a phase21w9 registry lists them as pending',
        (not ten_un) or bool(reg_files), 'unnamed=%d registry_files=%d' % (len(ten_un), len(reg_files)), role='E')

    # E3: W9 chain deliverable report exists
    cands = ['docs/qa/phase21w9_fclass_backfill_report.md', 'docs/research/phase21w9_fclass_backfill_report.md']
    found = [x for x in cands if os.path.exists(WS + '/' + x)]
    if not found:
        for x in cands:
            if blob_bytes(at + ':' + x) or blob_bytes('HEAD:' + x):
                found.append(x + ' (in tree)')
    chk('E3', 'end-state: W9 backfill dry-run/execution report present', bool(found), 'found=%s' % found, role='E')

    # ================ I group (info) ================
    if a.with_parity:
        pj = TMP + '/parity.json'
        pr2 = sh(['python3', 'tools/check_repo_parity.py', '--json'], timeout=900)
        try:
            d = json.loads(pr2.stdout)
            cnt = d.get('counts', {})
            info('I1', 'parity now: status=' + d['status'] + ' counts=' + json.dumps(cnt, ensure_ascii=False),
                 'diffs=' + str(len(d['diffs'])) + (' :: ' + d['diffs'][0]['path'] if d['diffs'] else ''))
        except Exception as ex:
            info('I1', 'parity parse failed', repr(ex))
    else:
        info('I1', 'parity not re-run (use --with-parity)', '')
    if a.with_remote:
        r1 = sh(['git', 'ls-remote', '--heads', 'origin'], timeout=90)
        r2 = sh(['git', 'merge-base', '--is-ancestor', at, 'origin/main'])
        info('I2', 'remote: heads=' + ' '.join(r1.stdout.split()) + ' | at-is-ancestor-of-origin/main=' + str(r2.returncode == 0))
    else:
        info('I2', 'remote not checked (use --with-remote)', '')

    dt = time.time() - t0
    nf = len([r for r in results if r['ok'] is False])
    np_ = len([r for r in results if r['ok'] is True])
    print('== summary: %d PASS / %d FAIL / %d INFO (%.1fs)' % (np_, nf, len([r for r in results if r['ok'] is None]), dt))
    if a.json:
        json.dump({'schema': 'protreptic.phase21w9_fclass.qa_verify/v1', 'at': at, 'generated_at': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 'results': results, 'pass': np_, 'fail': nf}, open(a.json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('json:', a.json)
    sys.exit(1 if nf else 0)

if __name__ == '__main__':
    main()
