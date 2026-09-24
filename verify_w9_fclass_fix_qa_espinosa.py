#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_w9_fclass_fix_qa_espinosa.py -- adjudicated independent QA verifier, card t_28a29244.

Scope: re-verification of the W9-F fix chain (parent 6f298ca1 -> HEAD b7a6bfad; fix card t_d7faccc5),
successor of verify_w9_fclass_qa_espinosa.py (card t_9ed2866a). Read-only for both repos: it only
writes its own temp dir (and --json output when asked).

Groups
  W: fix-chain window facts (commit set / per-commit staged sets / before-list / allowlist).
  R: rebuild-no-regress replay - fresh-from-source x2, same-file idempotence, copy-of-main rebuild,
     old-loader (parent blob) causal test on identical sources.
  S: stratified sampling (100 true-name + 26 code-as-name + spotlight) through DB / shard /
     figures.index / index.unified, plus a global no-invention scan over all 1027 rows.
  G: residual registry (ten=no-source, code_as_name=placeholder) vs independent re-derivation.
  B: boundary face - H-* zero movement, W7 deletion face not rolled back, web/public/data index face.
  C: closure face - parity, manifest consistency, gzip budget, routes, isolated unified rebuild,
     optional isolated site re-export and remote (ls-remote == publish HEAD).
  E: ADJUDICATED end-state assertions (E1'/F11'/F12' below); upstream E1/F11/F12 stay in the old
     verifier, marked superseded.

Adjudication (differences vs upstream verifier classify_w9_fclass_qa_espinosa.py; full rationale in
docs/qa/phase21w9_fclass_fix_qa_report_espinosa.md section 5):
  1. upstream F11 asserted figures-tree aggregate == 6391856f and figures.index == 65a7cdc6 (a
     no-change-state hash invariance). A legitimate backfill of 504 non-H names must change both.
     Replaced by: H-* face zero movement (DB rows / 372 shards / index entries) + parity-boundary
     ws<->pb byte equality + manifest self-consistency.
  2. upstream F12 asserted the publish repo "never references and does not hold" e5ddd13f. That is
     a string/object-presence check whose result varies with sibling-card history (pb local master
     snapshot carries the object; fix-chain receipts legitimately mention the hash). Substantive
     invariant kept: e5ddd13f is not an ancestor of the publish line (origin/main). Object/message
     presence is recorded as INFO.
  3. upstream E1 demanded non-H empty == 0 in worktree AND rebuild-from-source. The 10 no-source
     codes (registered as 待核名) can never reach 0 without inventing names (forbidden). Replaced by:
     worktree empty set == TEN exactly AND fresh rebuild-from-source empty set == TEN exactly.
Exit: 0 = all executed assertions PASS; 1 = any FAIL; 2 = environment error.
"""
from __future__ import annotations

import argparse, hashlib, json, os, shutil, sqlite3, subprocess, sys, tempfile, time

WS = os.path.dirname(os.path.abspath(__file__))
PB_DEFAULT = '/opt/data/release/Protreptic-publish'
PARENT = '6f298ca1'
HEAD = 'b7a6bfad'
CHAIN = ['108e2826', '47f9852d', '49ac3832', 'b7a6bfad']
AUDITED = 'e5ddd13f'
TEN = ['BW-KHA-001', 'BW-MAS-001', 'LS-MOS-001', 'MG-RAV-001', 'NA-GEO-001',
       'NA-NUJ-001', 'SZ-MSW-001', 'ZA-ZUM-001', 'ZW-CHA-001', 'ZW-MUG-001']
BEFORE_LIST = 'data/audit/phase21w9_web_public_data_index_before.txt'
BEFORE_SHA = 'b123f3f066366eeb5af16ce95ef6133dd42d01ea3c56ec4f28984d690a133924'
ALLOWLIST = {
    'api/load_data.py', 'api/protreptic.db', 'build_w9_fclass_fix_evidence.py',
    'data/audit/phase21w9_fclass_residual_registry.json',
    'data/audit/phase21w9_web_public_data_index_before.txt',
    'docs/architecture/static_data_manifest.json', 'docs/architecture/web_p0_routes.json',
    'docs/qa/phase21w9_fclass_backfill_report.md', 'docs/qa/phase21w9_fclass_fix_evidence.json',
    'docs/qa/phase21w9_fclass_fix_report.md', 'tools/build_figures_db.py',
    'tools/export_static_site.py', 'verify_w9_fclass_fix.py', 'web/src/generated/siteCounts.ts',
}
STATUS_PENDING = '\u5f85\u6838\u540d'          # "pending name review"
STATUS_PLACEHOLDER = '\u5360\u4f4d\u5f85\u8865\u540d'  # "placeholder, name pending"

R = []

def chk(cid, name, ok, detail=''):
    R.append({'id': cid, 'name': name, 'ok': bool(ok), 'detail': str(detail)[:400]})
    print(('PASS' if ok else 'FAIL') + ' [' + cid + '] ' + name + ((' :: ' + str(detail)[:220]) if detail else ''))

def info(cid, name, detail=''):
    R.append({'id': cid, 'name': name, 'ok': None, 'detail': str(detail)[:400]})
    print('INFO [' + cid + '] ' + name + ((' :: ' + str(detail)[:220]) if detail else ''))

def sh(cmd, cwd=WS, timeout=900, binary=False):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=not binary, timeout=timeout)

def sha256f(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

def dbmap(p):
    con = sqlite3.connect('file:%s?mode=ro' % p, uri=True)
    r = {c: (z or '', e or '') for c, z, e in con.execute('select code,name_zh,name_en from figures')}
    con.close()
    return r

def dbrows(p):
    con = sqlite3.connect('file:%s?mode=ro' % p, uri=True)
    r = con.execute('select * from figures order by code').fetchall()
    con.close()
    return r

def nameset(paths):
    return sorted(os.path.basename(p)[:-5] if p.endswith('.json') else p for p in paths)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', default=None)
    ap.add_argument('--with-reexport', action='store_true')
    ap.add_argument('--with-remote', action='store_true')
    ap.add_argument('--pb', default=PB_DEFAULT)
    a = ap.parse_args()
    TMP = tempfile.mkdtemp(prefix='w9fixqa_')
    t0 = time.time()
    print('== verify_w9_fclass_fix_qa_espinosa :: ws=' + WS + ' tmp=' + TMP)

    # ---------------- W group: fix-chain window ----------------
    lg = sh(['git', 'log', '--format=%h', PARENT + '..' + HEAD]).stdout.split()[::-1]
    chk('W1', 'fix chain == 4 commits, 108e2826 parent == 6f298ca1',
        lg == CHAIN and sh(['git', 'rev-parse', '108e2826^']).stdout.strip() == sh(['git', 'rev-parse', PARENT]).stdout.strip(),
        'chain=' + ','.join(lg))
    import collections
    ns_head = sh(['git', 'diff', '--name-status', '-M', PARENT + '..' + HEAD]).stdout
    rows_h = [l.split('\t') for l in ns_head.splitlines() if l.strip()]
    c_h = collections.Counter(r[0] for r in rows_h)
    chk('W2', 'range diff parent..HEAD == M7 A7 D1359', c_h == collections.Counter({'M': 7, 'A': 7, 'D': 1359}), dict(c_h))
    # per-commit staged sets
    def fileset(rev):
        out = sh(['git', 'show', '--name-status', '--format=', '-M', rev]).stdout.splitlines()
        rows = [l.split('\t') for l in out if l.strip()]
        return {(r[0], r[-1]) for r in rows}
    fs1 = fileset('108e2826')
    import collections
    c1 = collections.Counter(s for s, _ in fs1)
    chk('W2a', '108e2826 = M7 A7 D1359', c1 == collections.Counter({'M': 7, 'A': 7, 'D': 1359}), dict(c1))
    fs2 = fileset('47f9852d'); fs3 = fileset('49ac3832'); fs4 = fileset('b7a6bfad')
    chk('W2b', 'receipt commits touch only generator/registry/evidence/report',
        {p for _, p in fs2} <= {'build_w9_fclass_fix_evidence.py', 'data/audit/phase21w9_fclass_residual_registry.json', 'docs/qa/phase21w9_fclass_fix_evidence.json', 'docs/qa/phase21w9_fclass_fix_report.md'}
        and {p for _, p in fs3} <= {'docs/qa/phase21w9_fclass_fix_evidence.json', 'docs/qa/phase21w9_fclass_fix_report.md'}
        and {p for _, p in fs4} <= {'data/audit/phase21w9_fclass_residual_registry.json'},
        'v2=%d v3=%d v4=%d files' % (len(fs2), len(fs3), len(fs4)))
    am = {p for s, p in fs1 if s in 'AM'}
    chk('W3', 'A/M union == 14-file allowlist (explicit paths, no smuggling)',
        am == ALLOWLIST and all(p in ALLOWLIST for _, p in fs2) and all(p in ALLOWLIST for _, p in fs3) and all(p in ALLOWLIST for _, p in fs4),
        'n=%d extra=%r missing=%r' % (len(am), sorted(am - ALLOWLIST)[:3], sorted(ALLOWLIST - am)[:3]))
    Dset = {p for s, p in fs1 if s == 'D'}
    bl = WS + '/' + BEFORE_LIST
    blsha = sha256f(bl)
    lines = open(bl, encoding='utf-8').read().splitlines()
    blp = [l.split('  ', 1)[1] for l in lines if '  ' in l]
    chk('W4', 'removed index set == before-list set (1359); before-list sha256 pinned',
        Dset == set(blp) and len(blp) == 1359 and blsha == BEFORE_SHA,
        'D=%d list=%d sha=%s' % (len(Dset), len(blp), blsha[:12]))

    # ---------------- R group: rebuild-no-regress replay ----------------
    RP = TMP + '/replay'
    os.makedirs(RP)

    def build(tool, out):
        p = sh(['python3', tool, '--out', out], timeout=900)
        return p.returncode, (p.stdout or '')[-80:]
    rc1, o1 = build(WS + '/tools/build_figures_db.py', RP + '/fz_a.db')
    rc2, o2 = build(WS + '/tools/build_figures_db.py', RP + '/fz_b.db')
    r_a = dbrows(RP + '/fz_a.db'); r_b = dbrows(RP + '/fz_b.db')
    m_a = dbmap(RP + '/fz_a.db')
    empt = sorted(c for c, (z, e) in m_a.items() if not z.strip())
    chk('R1', 'fresh-from-source rebuild x2: 1027 rows / 1017 named / empty == TEN',
        rc1 == 0 and rc2 == 0 and len(m_a) == 1027 and sum(1 for c, (z, e) in m_a.items() if z.strip()) == 1017 and empt == sorted(TEN),
        'n=%d named=%d empty=%d' % (len(m_a), sum(1 for c, (z, e) in m_a.items() if z.strip()), len(empt)))
    chk('R2', 'fresh rebuild deterministic (a == b)', r_a == r_b)
    shutil.copy2(WS + '/api/protreptic.db', RP + '/main_copy.db')
    rc3, o3 = build(WS + '/tools/build_figures_db.py', RP + '/main_copy.db')
    r_main = dbrows(RP + '/main_copy.db')
    r_ground = dbrows(WS + '/api/protreptic.db')
    chk('R3', 'rebuild into main-DB copy: no-regress (== main) and == fresh-from-source',
        rc3 == 0 and r_main == r_ground and r_main == r_a)
    # old loader causal test (parent blob) with identical sources, inside TMP
    od = TMP + '/oldloader/tools/json'
    os.makedirs(od)
    for f in ('scenarios_zh.json', 'scenarios_en.json', 'scenario_tags.json'):
        src = WS + '/tools/json/' + f
        if os.path.exists(src):
            os.symlink(src, od + '/' + f)
    otool = TMP + '/oldloader/tools/build_figures_db_old.py'
    open(otool, 'w').write(sh(['git', 'show', PARENT + ':tools/build_figures_db.py']).stdout)
    rc4, o4 = build(otool, RP + '/old_out.db')
    m_old = dbmap(RP + '/old_out.db')
    old_empty = sorted(c for c, (z, e) in m_old.items() if not z.strip())
    src_changed = [f for f in ('tools/json/scenarios_zh.json', 'tools/json/scenarios_en.json', 'tools/json/scenario_tags.json')
                   if sh(['git', 'diff', '--quiet', PARENT + '..' + HEAD, '--', f]).returncode != 0]
    chk('R4', 'durability source is loader key-fallback: parent loader on identical sources -> 514 empty; sources unmodified',
        rc4 == 0 and len(old_empty) == 514 and not src_changed,
        'old_empty=%d src_changed=%r' % (len(old_empty), src_changed))

    # ---------------- S group: stratified sampling + no-invention ----------------
    open(TMP + '/parent_snapshot.db', 'wb').write(sh(['git', 'show', PARENT + ':api/protreptic.db'], binary=True).stdout)
    pm = dbmap(TMP + '/parent_snapshot.db')
    zh = json.load(open(WS + '/tools/json/scenarios_zh.json', encoding='utf-8'))
    en = json.load(open(WS + '/tools/json/scenarios_en.json', encoding='utf-8'))

    def legz(c):
        z = zh.get(c) or {}
        return z.get('name') or z.get('name_zh') or ''

    def lege(c):
        e = en.get(c) or {}
        return e.get('name') or e.get('name_en') or ''

    p_empty = sorted(c for c, (z, e) in pm.items() if not z.strip() and not c.startswith('H-'))
    restorable = sorted(c for c in p_empty if legz(c).strip())
    true_n = [c for c in restorable if legz(c) != c]
    code_n = [c for c in restorable if legz(c) == c]
    no_src = sorted(c for c in p_empty if not legz(c).strip())
    chk('S1', 'parent decomposition re-derived: restorable 504 = true 400 + code 104; no-source == TEN',
        len(restorable) == 504 and len(true_n) == 400 and len(code_n) == 104 and no_src == sorted(TEN),
        'restorable=%d true=%d code=%d nosrc=%d' % (len(restorable), len(true_n), len(code_n), len(no_src)))

    def spread(lst, k):
        n = len(lst)
        return list(lst) if k >= n else [lst[round(i * (n - 1) / (k - 1))] for i in range(k)]
    sample = sorted(spread(true_n, 100) + spread(code_n, 26) + ['AE-FED-001'])
    chk('S2', 'stratified sample >=100 (100 true-name + 26 code-as-name + spotlight)', len(sample) >= 100, 'n=%d' % len(sample))
    cm = dbmap(WS + '/api/protreptic.db')
    idx = {it['code']: it for it in json.load(open(WS + '/web/public/data/figures.index.json', encoding='utf-8'))}
    uni = {it['code']: it for it in json.load(open(WS + '/web/public/data/index.unified.json', encoding='utf-8'))['items']}
    sd = WS + '/web/public/data/figures'
    bad = []
    for c in sample:
        ez, ee = legz(c), lege(c)
        okd = cm.get(c) == (ez, ee)
        ok_s = os.path.exists(sd + '/' + c + '.json') and (json.load(open(sd + '/' + c + '.json', encoding='utf-8')).get('name_zh') or '') == ez and (json.load(open(sd + '/' + c + '.json', encoding='utf-8')).get('name_en') or '') == ee
        ok_i = (idx.get(c, {}).get('name_zh') or '') == ez
        ok_u = (uni.get(c, {}).get('name') or '') == ez
        if not (okd and ok_s and ok_i and ok_u):
            bad.append((c, okd, ok_s, ok_i, ok_u))
    chk('S2b', 'sample faces match source-side legacy names (DB/shard/index/unified)', not bad, 'bad=%r' % bad[:4])
    badz = [c for c, (z, e) in cm.items() if z.strip() and z != legz(c)]
    bade = [c for c, (z, e) in cm.items() if e.strip() and e != lege(c)]
    inv = [c for c, (z, e) in cm.items() if not z.strip() and legz(c).strip()]
    chk('S3', 'global no-invention: all 1027 rows == source-side names (or empty where source has none)',
        not badz and not bade and not inv, 'zh=%d en=%d empty-with-source=%d' % (len(badz), len(bade), len(inv)))
    pm_bad = [c for c in code_n if not (cm.get(c, ('', ''))[0] == c and (idx.get(c, {}).get('name_zh') or '') == c and (uni.get(c, {}).get('name') or '') == c)]
    ten_leak = []
    for c in TEN:
        vals = [cm.get(c, ('', ''))[0], cm.get(c, ('', ''))[1], idx.get(c, {}).get('name_zh') or '',
                uni.get(c, {}).get('name') or '', ((json.load(open(sd + '/' + c + '.json', encoding='utf-8')).get('name_zh') or '') if os.path.exists(sd + '/' + c + '.json') else '')]
        if [v for v in vals if v and v != c]:
            ten_leak.append((c, vals))
    chk('S4', 'placeholder/masquerade guard: 104 stay name==code; ten show no real name anywhere',
        not pm_bad and not ten_leak, 'code_bad=%d ten_leak=%d' % (len(pm_bad), len(ten_leak)))

    # ---------------- G group: residual registry ----------------
    reg = json.load(open(WS + '/data/audit/phase21w9_fclass_residual_registry.json', encoding='utf-8'))
    ten_it = reg['ten']['items']
    chk('G1', 'registry.ten: count 10 / status pending / codes == TEN / all name fields empty',
        reg['ten']['count'] == 10 and reg['ten']['status'] == STATUS_PENDING and sorted(it['code'] for it in ten_it) == sorted(TEN)
        and all(not (it.get('db_name_zh') or '') and not (it.get('legacy_name_zh') or '') and not (it.get('db_name_en') or '') and not (it.get('legacy_name_en') or '') for it in ten_it))
    chk('G2', 'registry.code_as_name: count 104 / status placeholder / codes == re-derived 104',
        reg['code_as_name']['count'] == 104 and reg['code_as_name']['status'] == STATUS_PLACEHOLDER and sorted(reg['code_as_name']['codes']) == code_n)
    bcommit = sh(['git', 'show', HEAD + ':' + BEFORE_LIST], binary=True).stdout
    rdisk = open(WS + '/' + BEFORE_LIST, 'rb').read()
    regc = sh(['git', 'show', HEAD + ':data/audit/phase21w9_fclass_residual_registry.json'], binary=True).stdout
    regd = open(WS + '/data/audit/phase21w9_fclass_residual_registry.json', 'rb').read()
    chk('G3', 'registry + before-list committed == disk', regc == regd and bcommit == rdisk)

    # ---------------- B group: boundary face ----------------
    def hrows(p):
        con = sqlite3.connect('file:%s?mode=ro' % p, uri=True)
        r = {c: (z or '', e or '') for c, z, e in con.execute("select code,name_zh,name_en from figures where code like 'H-%'")}
        con.close()
        return r
    hp = hrows(TMP + '/parent_snapshot.db'); hh = hrows(WS + '/api/protreptic.db')
    hdiff = [c for c in hp if hp[c] != hh.get(c)]
    hfiles = sorted(f for f in os.listdir(sd) if f.startswith('H-') and f.endswith('.json'))
    hmis = [f for f in hfiles if sh(['git', 'show', PARENT + ':web/public/data/figures/' + f], binary=True).stdout != open(sd + '/' + f, 'rb').read()]
    ib = {it['code']: (it.get('name_zh') or '') for it in json.loads(sh(['git', 'show', PARENT + ':web/public/data/figures.index.json'], binary=True).stdout)}
    ii = {it['code']: (it.get('name_zh') or '') for it in json.load(open(WS + '/web/public/data/figures.index.json', encoding='utf-8'))}
    hidx = [c for c in ib if c.startswith('H-') and ib[c] != ii.get(c)]
    chk('B1', 'H-* face zero movement: DB rows parent==HEAD; 372 shards parent blob == disk; index entries equal',
        not hdiff and not hmis and not hidx, 'db=%d shard=%d idx=%d' % (len(hdiff), len(hmis), len(hidx)))
    Dall = [l.split('\t', 1)[1] for l in sh(['git', 'show', '--name-status', '--format=', '-M', AUDITED]).stdout.splitlines() if l.startswith('D\t')]
    am_ints = am & set(Dall)
    smp = Dall[::max(1, len(Dall) // 40)][:40]
    onsk = [p for p in smp if os.path.exists(WS + '/' + p)]
    intree = sh(['git', 'ls-tree', '-r', '--name-only', HEAD, '--', *smp[:10]]).stdout.strip()
    chk('B2', 'W7 deletion face not rolled back: fix A/M does not intersect the 1303; sample absent on disk/tree',
        len(Dall) == 1303 and not am_ints and not onsk and not intree, 'D=%d int=%d disk=%d tree=%d' % (len(Dall), len(am_ints), len(onsk), len(intree.splitlines()) if intree else 0))
    lsf = sh(['git', 'ls-files', 'web/public/data']).stdout.splitlines()
    miss = [p for p in blp if not os.path.exists(WS + '/' + p)]
    chk('B3', 'web index face: ls-files == 0; all 1359 before-list paths still on disk; .gitignore actively ignores',
        len(lsf) == 0 and not miss and sh(['git', 'check-ignore', 'web/public/data/figures/AE-FED-001.json']).returncode == 0,
        'lsf=%d missing=%d' % (len(lsf), len(miss)))

    # ---------------- C group: closure face ----------------
    pq = sh(['python3', 'tools/check_repo_parity.py', '--json'], timeout=600)
    try:
        pd = json.loads(pq.stdout)
        cc = pd.get('counts', {})
        chk('C1', 'parity: rc=0 / status OK / all boundary files identical / 0 single-side (boundary >= fix-state 4593)',
            pq.returncode == 0 and pd.get('status') == 'OK'
            and cc.get('identical') == cc.get('both_sides') == cc.get('workspace_in_boundary') == cc.get('publish_in_boundary')
            and isinstance(cc.get('both_sides'), int) and cc.get('both_sides') >= 4593
            and cc.get('only_workspace', -1) == 0 and cc.get('only_publish', -1) == 0 and not pd.get('diffs'),
            json.dumps(cc))
    except Exception as ex:
        chk('C1', 'parity run', False, 'rc=%d parse=%r' % (pq.returncode, ex))
    man = json.load(open(WS + '/docs/architecture/static_data_manifest.json', encoding='utf-8'))
    def agg(sub):
        d = WS + '/web/public/data/' + sub; h = hashlib.sha256(); n = 0; items = []
        for f in sorted(os.listdir(d)):
            p = os.path.join(d, f)
            if os.path.isfile(p):
                items.append((sub + '/' + f, sha256f(p))); n += 1
        for rel, dig in sorted(items):
            h.update(rel.encode()); h.update(b'\0'); h.update(dig.encode()); h.update(b'\n')
        return h.hexdigest(), n
    fa, fn = agg('figures')
    import gzip
    gz = len(gzip.compress(open(WS + '/web/public/data/figures.index.json', 'rb').read(), 9))
    chk('C2', 'manifest self-consistent (db sha, figures agg, index sha) + gzip <= 80KB',
        man['sources']['api/protreptic.db']['sha256'] == sha256f(WS + '/api/protreptic.db')
        and man['products']['figures/']['sha256'] == fa and fn == 1027
        and man['products']['figures.index.json']['sha256'] == sha256f(WS + '/web/public/data/figures.index.json')
        and gz <= 80 * 1024,
        'fig=%s n=%d gzip=%d' % (fa[:8], fn, gz))
    routes = json.load(open(WS + '/docs/architecture/web_p0_routes.json', encoding='utf-8'))
    rcodes = sorted(r['code'] for r in routes['routes'] if (r.get('name') or '') == r.get('code'))
    chk('C3', 'routes name==code == 104 placeholder + 10 pending == 114', rcodes == sorted(code_n + TEN), 'n=%d' % len(rcodes))
    uo = TMP + '/unified.json'
    pu = sh(['python3', 'tools/build_unified_index.py', '--out', uo], timeout=600)
    chk('C4', 'isolated unified rebuild byte-equal to disk; counts {1344,320,1024}',
        pu.returncode == 0 and os.path.exists(uo) and open(uo, 'rb').read() == open(WS + '/web/public/data/index.unified.json', 'rb').read()
        and json.load(open(uo, encoding='utf-8'))['counts'] == {'total': 1344, 'figures': 320, 'scenarios': 1024, 'with_modes': 1308})
    if a.with_reexport:
        # NOTE: tools/export_static_site.py always rewrites docs/architecture/static_data_manifest.json
        # (line MANIFEST_PATH.write_bytes) even with --out, so snapshot and restore it around the run.
        MANP = WS + '/docs/architecture/static_data_manifest.json'
        man_snap = open(MANP, 'rb').read()
        REE = TMP + '/reexport'
        os.makedirs(REE)
        pr = sh(['python3', 'tools/export_static_site.py', '--out', REE], timeout=1800)
        if open(MANP, 'rb').read() != man_snap:
            open(MANP, 'wb').write(man_snap)
        same = diff = only = 0
        dset = []
        for root, _, files in os.walk(REE):
            for f in files:
                rel = os.path.relpath(os.path.join(root, f), REE)
                wp = WS + '/web/public/data/' + rel
                if not os.path.exists(wp):
                    only += 1
                    continue
                a1 = open(os.path.join(root, f), 'rb').read(); b1 = open(wp, 'rb').read()
                if a1 == b1:
                    same += 1
                    continue
                try:
                    ja = json.loads(a1); jb = json.loads(b1)
                    if isinstance(ja, dict) and isinstance(jb, dict):
                        for tk in ('generated_at', 'generated_at_local'):
                            ja.pop(tk, None); jb.pop(tk, None)
                        if ja == jb:
                            same += 1
                            continue
                except Exception:
                    pass
                diff += 1; dset.append(rel)
        chk('C5', 'isolated site re-export equal to disk (byte-equal or equal modulo generated_at)',
            pr.returncode == 0 and diff == 0 and only == 0 and same > 1300,
            'rc=%d same=%d diff=%d only=%d %s' % (pr.returncode, same, diff, only, dset[:3]))
        chk('C5b', 'export side-effect on docs/architecture/static_data_manifest.json undone (restored byte-exact)',
            open(MANP, 'rb').read() == man_snap)
    else:
        info('C5', 'isolated re-export not run (use --with-reexport)', '')
    pb = a.pb
    if a.with_remote and os.path.isdir(pb + '/.git'):
        lr = sh(['git', 'ls-remote', 'origin', 'main'], cwd=pb, timeout=120).stdout.split()
        ph = sh(['git', 'rev-parse', 'HEAD'], cwd=pb).stdout.strip()
        chk('C6', 'publish line: ls-remote origin main == pb HEAD (LOCAL)', bool(lr) and lr[0] == ph, 'ls=%s head=%s' % (lr[0][:12] if lr else '?', ph[:12]))
    else:
        info('C6', 'remote/publish-line check not run (use --with-remote)', '')

    # ---------------- E group: adjudicated end-state ----------------
    wm = dbmap(WS + '/api/protreptic.db')
    w_empty = sorted(c for c, (z, e) in wm.items() if not z.strip())
    rb = dbmap(RP + '/fz_a.db')
    rb_empty = sorted(c for c, (z, e) in rb.items() if not z.strip())
    chk('E1p', "E1-RESOLVED: worktree empty == TEN AND rebuild-from-source empty == TEN (supersedes upstream '==0')",
        w_empty == sorted(TEN) and rb_empty == sorted(TEN), 'worktree=%d rebuild=%d' % (len(w_empty), len(rb_empty)))
    chk('E2', 'E2: ten registered as pending in a phase21w9 residual registry',
        reg['ten']['status'] == STATUS_PENDING and sorted(it['code'] for it in ten_it) == sorted(TEN))
    chk('E3', 'E3: backfill + fix reports + evidence present with schema',
        os.path.exists(WS + '/docs/qa/phase21w9_fclass_backfill_report.md')
        and os.path.exists(WS + '/docs/qa/phase21w9_fclass_fix_report.md')
        and json.load(open(WS + '/docs/qa/phase21w9_fclass_fix_evidence.json', encoding='utf-8')).get('schema') == 'protreptic.phase21w9_fclass_fix_evidence/v1')
    chk('F11p', 'F11-RESOLVED: H-face zero movement + parity-boundary equality (supersedes old-hash invariance)',
        not hdiff and not hmis and not hidx)
    if os.path.isdir(pb + '/.git'):
        anc = sh(['git', 'merge-base', '--is-ancestor', AUDITED, 'origin/main'], cwd=pb).returncode
        obj = sh(['git', 'cat-file', '-e', AUDITED], cwd=pb).returncode
        chk('F12p', 'F12-RESOLVED: e5ddd13f is NOT an ancestor of the publish line (origin/main)',
            anc != 0, 'is_ancestor_rc=%d' % anc)
        info('F12x', 'time-varied facts (recorded, not defect): object-present in pb clone=%s (local master snapshot branch)' % (obj == 0))
    else:
        info('F12p', 'publish repo missing at ' + pb, '')

    info('ADJ1', 'upstream verifier at fix state: 12 PASS / 3 FAIL (E1/F11/F12) - all three superseded above',
         'python3 verify_w9_fclass_qa_espinosa.py')
    dt = round(time.time() - t0, 1)
    nf = len([r for r in R if r['ok'] is False]); np_ = len([r for r in R if r['ok'] is True])
    print('== summary: %d PASS / %d FAIL / %d INFO (%.1fs)' % (np_, nf, len([r for r in R if r['ok'] is None]), dt))
    if a.json:
        json.dump({'schema': 'protreptic.phase21w9_fclass_fix.qa_verify_espinosa/v1', 'card': 't_28a29244',
                   'generated_at': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 'results': R, 'pass': np_, 'fail': nf},
                  open(a.json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('json:', a.json)
    shutil.rmtree(TMP, ignore_errors=True)
    return 1 if nf else 0

if __name__ == '__main__':
    sys.exit(main())
