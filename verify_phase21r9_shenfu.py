#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase21-R9 沈复重建落盘独立核验（卡 t_b6d4c0ee）

对 data/figures/H-SHF-001.json、data/individuals/H-SHF-001(.modes).json、
docs/scratch/legacy20_r9_shenfu_landing/**、data/audit/phase21r9_shenfu_landing_manifest.json
做独立复核：条目不变量、引文对素材包 quotes 子串、见证强归一化命中、见证 sha256、
片段白名单、禁字扫描、查重与残留、归档字节、主库零写入、落地件一致性。
结果写 docs/research/phase21r9_shenfu_verify_evidence.json；FAIL 时 exit 1。
"""
import hashlib
import io
import json
import os
import re
import subprocess
import sys
from datetime import datetime

REPO = os.path.dirname(os.path.abspath(__file__))
FIG = 'H-SHF-001'
LANDING = os.path.join(REPO, 'docs/scratch/legacy20_r9_shenfu_landing')
PACK = os.path.join(REPO, 'docs/research/phase21r9_shenfu_sourcing_report.json')
MD = os.path.join(REPO, 'docs/research/phase21r9_shenfu_sourcing_report.md')
REPORT = os.path.join(REPO, 'docs/research/phase21r9_shenfu_rebuild_report.md')
WITNESS = os.path.join(REPO, 'docs/scratch/phase21r9_shenfu/witness')
WEXCL = ('witness_sha256.txt', 'verify_quotes.py', 'quote_verification_final.json', 'README.md')
STD_CATEGORIES = [u'伦理修养', u'军事战略', u'医学养生', u'史学文献', u'哲学形而上', u'宗教修行', u'工程技术',
                  u'心理洞察', u'战略决策', u'探险发现', u'政治治理', u'教育传承', u'文艺审美', u'方法论通用',
                  u'科学方法', u'组织领导', u'经济商业', u'认识论逻辑']
FORBIDDEN = [u'沈幅', u'捕鱼记', u'随园漫录', u'东汉', u'无锡', u'1825', u'1832',
             u'《望海》', u'《雨中游山》', u'华萼', u'M351', u'M352', u'M353', u'M354',
             u'M355', u'M356', u'M357', u'M358']
MAIN_LIB = ['data/modes_data.json', 'data/code_maps.json', 'data/scenarios_zh.json',
            'data/scenarios_en.json', 'data/scenario_tags.json', 'data/figure_names.json',
            'tools/modes_data.json', 'tools/code_maps.json', 'tools/code_maps_en.json',
            'tools/scenario_tags.json', 'tools/json/scenarios_zh.json', 'tools/json/scenarios_en.json']
RESULTS = []


def check(cid, grp, desc, ok, detail=''):
    RESULTS.append(dict(id=cid, group=grp, desc=desc, status='PASS' if ok else 'FAIL', detail=detail))
    print('%s  %-5s %s%s' % ('PASS' if ok else 'FAIL', cid, desc, (' | ' + str(detail)[:160]) if detail and not ok else ''))


def warn(cid, grp, desc, ok, detail=''):
    RESULTS.append(dict(id=cid, group=grp, desc=desc, status='PASS' if ok else 'WARN', detail=detail))
    print('%s  %-5s %s%s' % ('PASS' if ok else 'WARN', cid, desc, (' | ' + str(detail)[:200]) if detail else ''))


def jl(p):
    return json.load(io.open(p, encoding='utf-8'))


def norm(s):
    return re.sub(r'[^0-9A-Za-z\u3400-\u9fff\uf900-\ufaff]', '', s)


def sha_file(p):
    return hashlib.sha256(io.open(p, 'rb').read()).hexdigest()


def fragments(text):
    out = []
    for m in re.finditer(u'[\u300c\u300e]([^\u300c\u300d\u300e\u300f]+)[\u300d\u300f]', text):
        out.append(m.group(1))
    return out


def collect_strings(obj, out):
    if isinstance(obj, dict):
        for v in obj.values():
            collect_strings(v, out)
    elif isinstance(obj, list):
        for v in obj:
            collect_strings(v, out)
    elif isinstance(obj, str):
        out.append(obj)


def main():
    pack = jl(PACK)
    pm = dict((m['id'], m) for m in pack['modes'])
    md = io.open(MD, encoding='utf-8').read()
    pack_norm = norm(md) + norm(io.open(PACK, encoding='utf-8').read())
    entries = jl(os.path.join(LANDING, 'modes_library_entries.json'))
    combined = jl(os.path.join(LANDING, 'combined_library_entries.json'))
    fig = jl(os.path.join(REPO, 'data/figures/%s.json' % FIG))
    ind = jl(os.path.join(REPO, 'data/individuals/%s.json' % FIG))
    mfj = jl(os.path.join(REPO, 'data/individuals/%s_modes.json' % FIG))
    man = jl(os.path.join(REPO, 'data/audit/phase21r9_shenfu_landing_manifest.json'))
    scen = jl(os.path.join(LANDING, 'scenario_notes.json'))
    top = jl(os.path.join(LANDING, 'top_block_proposal.json'))
    raw_entries = io.open(os.path.join(LANDING, 'modes_library_entries.json'), encoding='utf-8').read()
    raw_fig = io.open(os.path.join(REPO, 'data/figures/%s.json' % FIG), encoding='utf-8').read()
    raw_land = ''
    for root, dirs, files in os.walk(LANDING):
        for fn in files:
            raw_land += io.open(os.path.join(root, fn), encoding='utf-8', errors='ignore').read()
    wl = man.get('frag_whitelist', [])

    # A 文件与解析
    check('A01', 'files', u'landing entries 可解析且 10 条', len(entries) == 10)
    check('A02', 'files', u'combined.modes == entries', combined['modes'] == entries)
    check('A03', 'files', u'figure/individuals/modes 三件可解析', all(isinstance(x, dict) for x in (fig, ind, mfj)))
    check('A04', 'files', u'冻结副本与 data 侧逐字节一致（figure）', sha_file(os.path.join(LANDING, 'figures/%s.json' % FIG)) == sha_file(os.path.join(REPO, 'data/figures/%s.json' % FIG)))
    check('A05', 'files', u'冻结副本与 data 侧逐字节一致（individuals）', sha_file(os.path.join(LANDING, 'individuals/%s.json' % FIG)) == sha_file(os.path.join(REPO, 'data/individuals/%s.json' % FIG)))
    check('A06', 'files', u'冻结副本与 data 侧逐字节一致（modes）', sha_file(os.path.join(LANDING, 'individuals/%s_modes.json' % FIG)) == sha_file(os.path.join(REPO, 'data/individuals/%s_modes.json' % FIG)))
    check('A07', 'files', u'id_mapping.tsv 10 行数据', len(io.open(os.path.join(LANDING, 'id_mapping.tsv'), encoding='utf-8').read().strip().split('\n')) == 11)
    check('A08', 'files', u'category_mapping.tsv 10 行数据', len(io.open(os.path.join(LANDING, 'category_mapping.tsv'), encoding='utf-8').read().strip().split('\n')) == 11)
    check('A09', 'files', u'manifest deliverable 12 件且 sha 可复算', all(sha_file(os.path.join(REPO, k)) == v['sha256'] for k, v in man['deliverables'].items()))
    check('A10', 'files', u'figures 顶层 modes == entries == _modes.modes（同链布局）', fig['modes'] == entries == mfj['modes'])
    check('A11', 'files', u'individuals 为 figure 去顶层 modes（差集恰为 modes）', set(fig.keys()) - set(ind.keys()) == {'modes'} and not (set(ind.keys()) - set(fig.keys())))
    check('A12', 'files', u'figures 与 individuals sha 不同（非重复副本）', sha_file(os.path.join(REPO, 'data/figures/%s.json' % FIG)) != sha_file(os.path.join(REPO, 'data/individuals/%s.json' % FIG)))
    check('A13', 'files', u'landing_evidence 与 manifest 逐字节一致', sha_file(os.path.join(REPO, 'docs/research/phase21r9_shenfu_landing_evidence.json')) == sha_file(os.path.join(REPO, 'data/audit/phase21r9_shenfu_landing_manifest.json')))

    # B 条目不变量
    check('B01', 'entries', u'id 序列 M-SHF-001~010', [e['id'] for e in entries] == ['M-SHF-%03d' % i for i in range(1, 11)])
    check('B02', 'entries', u'legacy_mode_id 全空（全新码、零复用）', all(e['legacy_mode_id'] == '' for e in entries))
    check('B03', 'entries', u'figure_code/figure_name 一致', all(e['figure_code'] == FIG and e['figure_name'] == u'沈复' for e in entries))
    check('B04', 'entries', u'category 均在标准 18 类', all(e['category'] in STD_CATEGORIES for e in entries))
    check('B05', 'entries', u'level=核心 与 priority 1..10', all(e['level'] == u'核心' and e['priority'] == i for i, e in enumerate(entries, 1)))
    check('B06', 'entries', u'verification 全 pending + method 口径', all(e['verification']['status'] == 'pending' and e['verification']['method'] == 'phase21r9-shenfu-rebuild-landing' for e in entries))
    check('B07', 'entries', u'英文面非空（name/definition/process/cases/modern）', all(all(len(e[k]) > 8 for k in ('name_en', 'definition_en')) and all(e[k] for k in ('process_en', 'representative_cases_en', 'modern_applications_en')) for e in entries))
    check('B08', 'entries', u'key_concepts 非空且 >=4', all(len(e['key_concepts']) >= 4 for e in entries))
    check('B09', 'entries', u'related_modes 指向本组代码', all(all(r in [x['id'] for x in entries] for r in e['related_modes']) for e in entries))

    # C 引文：素材包 quotes 子串 + 全覆盖
    quote_rows = []
    for e in entries:
        num = int(e['id'].split('-')[-1])
        mid = 'M-SHF-%03d' % num
        q = pm[mid]['quotes']
        hit = [i + 1 for i, qq in enumerate(q) if e['key_quote_zh'] in qq.get('text', '')]
        quote_rows.append(dict(entry=e['id'], key_substring_of=hit, key_quote_chars=len(e['key_quote_zh'])))
        check('C%02d' % num, 'quote-pack', u'%s key_quote 为素材包 §三 quotes 子串' % e['id'], bool(hit), hit)
    tot = 0
    used = 0
    for e in entries:
        mid = e['id']
        blob = '\n'.join([e['key_quote_zh']] + e['representative_cases_zh'] + e['representative_cases_en'])
        for qq in pm[mid]['quotes']:
            tot += 1
            if qq['text'] in blob:
                used += 1
    check('C11', 'quote-pack', u'条目内 35/35 引文全覆盖（key+cases 逐字命中）', used == tot == 35, u'used=%d total=%d' % (used, tot))

    # D 引文：见证强归一化
    import html as _html
    W = {}
    for fn in sorted(os.listdir(WITNESS)):
        if fn.endswith(('.txt', '.html')) and fn not in WEXCL:
            t = io.open(os.path.join(WITNESS, fn), encoding='utf-8', errors='replace').read()
            if fn.endswith('.html'):
                t = t + '\n' + _html.unescape(re.sub(r'<[^>]+>', ' ', t))
            W[fn] = norm(t)
    wmap = dict((w['id'], w['file']) for w in pack['witnesses'])
    all_files = sorted(W.keys())
    witness_sha_rows = []
    dpass = 0
    for e in entries:
        num = int(e['id'].split('-')[-1])
        mid = 'M-SHF-%03d' % num
        q = pm[mid]['quotes']
        idx = [i for i, qq in enumerate(q) if e['key_quote_zh'] in qq.get('text', '')]
        attr = q[idx[0]]['attr'] if idx else ''
        refs = re.findall(r'W\d+', attr)
        files = []
        for r in refs:
            f = wmap.get(r, '')
            if not f:
                continue
            if '..' in f:
                pre = f.split('..')[0]
                files += [x for x in all_files if x.startswith(pre)]
            elif f in W:
                files.append(f)
            else:
                pre = f.split(u'（')[0].strip()
                files += [x for x in all_files if x.startswith(pre)] if pre else []
        dedup = []
        for f in files:
            if f not in dedup:
                dedup.append(f)
        files = dedup if dedup else all_files
        nq = norm(e['key_quote_zh'])
        hit = None
        cands = list(files) + [x for x in all_files if x not in files]
        for fn in cands:
            t = W.get(fn)
            if t is None:
                continue
            if nq in t:
                hit = fn
                break
        if not hit and nq.startswith(u'芸'):
            nq2 = nq[1:]
            for fn in cands:
                t = W.get(fn)
                if t is not None and nq2 in t:
                    hit = fn + ' (drop-)'
                    break
        md_hit = nq in norm(md)
        witness_sha_rows.append(dict(entry=e['id'], witness='/'.join(refs), files=files, hit=hit, md_hit=md_hit))
        if hit:
            dpass += 1
            check('D%02d' % num, 'quote-witness', u'%s 见证 %s 强归一化命中' % (e['id'], '/'.join(refs) or '?'), True)
        else:
            warn('D%02d' % num, 'quote-witness', u'%s 见证 %s 文件未命中（素材包 md 命中=%s）' % (e['id'], '/'.join(refs) or '?', md_hit), md_hit)
    check('D11', 'quote-witness', u'见证强归一化命中 10/10', dpass == 10, dpass)

    # E 见证文件 sha256
    rows = []
    wl_path = os.path.join(WITNESS, 'witness_sha256.txt')
    if os.path.isfile(wl_path):
        for ln in io.open(wl_path, encoding='utf-8'):
            ln = ln.strip()
            if not ln or ln.startswith('#'):
                continue
            parts = ln.split()
            if len(parts) >= 3:
                h, sz, name = parts[0], parts[1], parts[2]
                fp = os.path.join(WITNESS, name)
                rows.append(dict(file=name, expect=h, exists=os.path.isfile(fp),
                                 now=sha_file(fp) if os.path.isfile(fp) else '', size=sz))
    mism = [r for r in rows if (not r['exists']) or r['now'] != r['expect']]
    check('E01', 'witness-sha', u'见证副本 sha256 全清单逐一复核（%d 件）' % len(rows), len(rows) >= 34 and not mism, [(r['file'], r['now'][:12], r['expect'][:12]) for r in mism][:8])
    check('E02', 'witness-sha', u'清单外文件不缺失（含 ia_search_fs6j.json）', os.path.isfile(os.path.join(WITNESS, 'ia_search_fs6j.json')))

    # F 片段白名单 + 禁字
    quote_norms = set()
    for mid, m in pm.items():
        for qq in m['quotes']:
            quote_norms.add(norm(qq['text']))
    wl_norms = set(norm(w['fragment']) for w in wl)
    fails = []
    frag_total = 0
    check_objs = [(e, e['id']) for e in entries] + [(fig, FIG + '-figure')]
    for obj, tag in check_objs:
        strs = []
        collect_strings(obj, strs)
        for s in strs:
            for f in fragments(s):
                frag_total += 1
                nf = norm(f)
                if (nf in pack_norm) or any(nf in qn for qn in quote_norms) or (nf in wl_norms):
                    continue
                fails.append((tag, f))
    check('F01', 'fragments', u'全部「」/『』片段过白名单（%d 片段 / %d 条白名单登记）' % (frag_total, len(wl)), not fails, fails[:6])
    check('F02', 'fragments', u'白名单片段均可回溯素材包 md/json', all(norm(w['fragment']) in pack_norm for w in wl))
    bad = [f for f in FORBIDDEN if f in raw_entries]
    check('F03', 'forbidden', u'entries 禁字零出现（%d 项）' % len(FORBIDDEN), not bad, bad)
    raw_extra = raw_fig + io.open(os.path.join(REPO, 'data/individuals/%s.json' % FIG), encoding='utf-8').read() + raw_land
    bad2 = [f for f in FORBIDDEN if f in raw_extra]
    check('F04', 'forbidden', u'figure/individuals/landing 禁字零出现', not bad2, bad2)
    check('F05', 'forbidden', u'「沈幅」仅登记于归档键名（数据面零出现）', u'沈幅' not in (raw_entries + raw_extra))

    # G 查重与残留
    def scan(patterns):
        files = subprocess.check_output(['git', '-C', REPO, 'ls-files'], text=True).split('\n')
        files += subprocess.check_output(['git', '-C', REPO, 'ls-files', '--others', '--exclude-standard'], text=True).split('\n')
        out = {}
        for rel in sorted(set(files)):
            if not rel or rel.startswith('.git') or '/node_modules/' in rel or rel.startswith('node_modules/') or '/.venv/' in rel or '/backups' in rel or rel.startswith('backups'):
                continue
            fp = os.path.join(REPO, rel)
            if not os.path.isfile(fp) or os.path.getsize(fp) > 3000000:
                continue
            try:
                s = io.open(fp, encoding='utf-8', errors='ignore').read()
            except Exception:
                continue
            for pat in patterns:
                if pat in s:
                    out.setdefault(rel, []).append(pat)
        return out

    hits = scan(['H-SHF-001', 'M-SHF-0', 'C-SHF-'])
    allowed = set([
        'docs/research/phase21r9_shenfu_sourcing_report.md', 'docs/research/phase21r9_shenfu_sourcing_report.json',
        'docs/research/phase21r9_shenfu_landing_evidence.json', 'docs/research/phase21r9_shenfu_rebuild_report.md',
        'docs/research/phase21r9_shenfu_verify_evidence.json', 'docs/research/phase21r9_shenfu_gate.txt',
        'tools/build_phase21r9_shenfu.py', 'verify_phase21r9_shenfu.py',
        'data/figures/%s.json' % FIG, 'data/individuals/%s.json' % FIG, 'data/individuals/%s_modes.json' % FIG,
        'data/audit/phase21r9_shenfu_landing_manifest.json',
        'docs/scratch/legacy20_r9_shenfu_landing/modes_library_entries.json',
        'docs/scratch/legacy20_r9_shenfu_landing/combined_library_entries.json',
        'docs/scratch/legacy20_r9_shenfu_landing/id_mapping.tsv',
        'docs/scratch/legacy20_r9_shenfu_landing/category_mapping.tsv',
        'docs/scratch/legacy20_r9_shenfu_landing/scenario_notes.json',
        'docs/scratch/legacy20_r9_shenfu_landing/top_block_proposal.json',
        'docs/scratch/legacy20_r9_shenfu_landing/figures/%s.json' % FIG,
        'docs/scratch/legacy20_r9_shenfu_landing/individuals/%s.json' % FIG,
        'docs/scratch/legacy20_r9_shenfu_landing/individuals/%s_modes.json' % FIG,
    ])
    # Phase21-R9 合并后口径（card t_a7d233f0，合并卡 2/4）：主库六件与合并卡产物成为预期出现面
    allowed |= set([
        'data/modes_data.json', 'data/code_maps.json', 'data/figure_names.json',
        'data/scenarios_zh.json', 'data/scenarios_en.json', 'data/scenario_tags.json',
        'data/audit/phase21r9_shenfu_merge_manifest.json',
        'docs/research/phase21r9_shenfu_merge_report.md',
        'docs/research/phase21r9_shenfu_merge_evidence.json',
        'docs/research/phase21r9_shenfu_merge_evidence.txt',
        'docs/research/phase21r9_shenfu_verify_evidence_merged.json',
        'tools/merge_phase21r9_shenfu.py', 'verify_phase21r9_shenfu_merge_indep.py',
        # 站点链锚点注释（沿 R8 先例，锚点注含卡号与图码）与兄弟卡引用（安子介合并卡
        # t_ce457734 的核验脚本注释中列明本卡足迹，属链式正常占用）
        'tools/export_static_site.py', 'tools/pages_preflight.py', 'verify_phase21r9_azj.py',
    ])
    allowed_prefixes = ('data/backup_merge_H-SHF-001_',)
    outside = {k: v for k, v in hits.items() if k not in allowed and not k.startswith(allowed_prefixes)}
    check('G01', 'dedup', u'M-SHF/H-SHF 仅出现于本链/素材包/合并产物面（0 外部碰撞）', not outside, outside)

    bad_main = {}
    for rel in MAIN_LIB:
        fp = os.path.join(REPO, rel)
        if not os.path.isfile(fp):
            continue
        s = io.open(fp, encoding='utf-8', errors='ignore').read()
        h = [p for p in ('H-SHF-001', 'M-SHF-0', 'C-SHF-') if p in s]
        if h:
            bad_main[rel] = h
    # Phase21-R9 合并后口径（card t_a7d233f0）：data 六件为预期占用面；tools/ 六副本保持零命中
    MERGED_DATA = set(['data/modes_data.json', 'data/code_maps.json', 'data/figure_names.json',
                       'data/scenarios_zh.json', 'data/scenarios_en.json', 'data/scenario_tags.json'])
    data_hits = {k: v for k, v in bad_main.items() if k in MERGED_DATA}
    tools_hits = {k: v for k, v in bad_main.items() if k not in MERGED_DATA}
    check('G02', 'dedup', u'主库登记面 == 合并后预期（data 六件命中 / tools 副本 0 命中）',
          set(data_hits.keys()) == MERGED_DATA and not tools_hits, tools_hits)

    scen_bad = {}
    for rel in ['data/scenarios_zh.json', 'data/scenarios_en.json', 'data/scenario_tags.json',
                'tools/json/scenarios_zh.json', 'tools/json/scenarios_en.json', 'tools/scenario_tags.json']:
        fp = os.path.join(REPO, rel)
        if os.path.isfile(fp) and 'C-SHF' in io.open(fp, encoding='utf-8', errors='ignore').read():
            scen_bad[rel] = True
    # C-SHF 场景码载体 = zh/en 两件（scenario_tags 载 M-SHF 模式码与 H-SHF 图码，由 G02 断言）
    SCEN_DATA2 = ['data/scenarios_zh.json', 'data/scenarios_en.json']
    SCEN_TOOL3 = ['tools/json/scenarios_zh.json', 'tools/json/scenarios_en.json', 'tools/scenario_tags.json']
    check('G03', 'dedup', u'场景面 C-SHF 已启用于 data zh/en 两件；tools 副本零占用',
          all(r in scen_bad for r in SCEN_DATA2) and all(r not in scen_bad for r in SCEN_TOOL3)
          and 'data/scenario_tags.json' not in scen_bad, scen_bad)

    # H 归档与主库未动
    for i, (name, expect) in enumerate(sorted(man['archive_untouched'].items()), 1):
        check('H%02d' % i, 'archive', u'归档 %s sha256 未变' % name,
              sha_file(os.path.join(REPO, 'data/figures/_duplicates', name)) == expect)
    # Phase21-R9 合并后口径（card t_a7d233f0）：data 六件 == 合并 manifest after；
    # tools/ 六副本 == 落盘基线（未随合并改动）。
    mm = jl(os.path.join(REPO, 'data/audit/phase21r9_shenfu_merge_manifest.json'))
    mis = [rel for rel in sorted(MERGED_DATA)
           if sha_file(os.path.join(REPO, rel)) != mm['after'][rel]['sha256']]
    mis_tools = []
    for rel, v in man['mainlib_baselines'].items():
        if rel in MERGED_DATA:
            continue
        fp = os.path.join(REPO, rel)
        now = sha_file(fp) if os.path.isfile(fp) else ''
        if now != v:
            mis_tools.append(rel)
    check('H04', 'mainlib', u'主库 data 六件 == 合并后 sha（manifest after）；tools 副本未动',
          not mis and not mis_tools, {'data': mis, 'tools': mis_tools})
    KEY23 = ['schema_version', 'code', 'name_zh', 'name_en', 'era', 'historical_domains', 'domains', 'core_modes',
             'gender', 'ethnicity', 'nationality', 'civilization_sphere', 'time_period_standardized', 'primary_language',
             'intellectual_tradition', 'unique_thinking_zh', 'unique_thinking_en', 'mode_evidence', 'key_texts',
             'key_concepts', 'intellectual_lineage', 'legacy_assessment', 'scholarly_value']
    check('H05', 'mainlib', u'顶层块提案键集与 modes_data 块口径一致（23 键）', set(top['proposal'].keys()) == set(KEY23))
    check('H06', 'mainlib', u'顶层块 core_modes = M-SHF-001~010 且含合并指引', top['proposal']['core_modes'] == ['M-SHF-%03d' % i for i in range(1, 11)] and (u'合并' in json.dumps(top, ensure_ascii=False)))

    # I 场景与命题件
    n = scen['notes']
    check('I01', 'scenario', u'场景件数=0 + 无旧载荷处置（本链零搬迁）', n['scenarios_zh_new'] == 0 and n['scenarios_en_new'] == 0 and n['old_code_dispositions'] == [])
    check('I02', 'scenario', u'新前缀建议含 C-SHF-001~010（0 碰撞口径）', 'C-SHF-001~010' in n['new_prefix_suggestion'])
    check('I03', 'scenario', u'模板规则登记（modern_applications 口径）', 'modern_applications' in n['template_rule'])

    # J figure 层
    check('J01', 'figure', u'mode_ids = M-SHF-001~010', fig['mode_ids'] == ['M-SHF-%03d' % i for i in range(1, 11)] and fig['thinking_mode_count'] == 10)
    check('J02', 'figure', u'core_thoughts 10 条且与名目对齐', len(fig['core_thoughts']) == 10 and all(u'（' in c for c in fig['core_thoughts']))
    check('J03', 'figure', u'tags >= 15', len(fig['tags']) >= 15)
    check('J04', 'figure', u'caveats >= 6（含史料语境与场景口径）', len(fig['caveats']) >= 6)
    check('J05', 'figure', u'representative_works 均为可落源篇目', all(w.startswith(u'《') for w in fig['representative_works']))
    cm = jl(os.path.join(REPO, 'data/code_maps.json'))
    tgt_bad = [t['target_figure_code'] for t in fig['cross_references'] if t['target_figure_code'] not in cm.get('figures', {})]
    check('J06', 'figure', u'cross_references 目标已注册（code_maps figures）', not tgt_bad, tgt_bad)
    check('J07', 'figure', u'身份字段口径（沈复/1763/卒年 null/三白/梅逸）', fig['figure_name'] == u'沈复' and fig['birth_year'] == 1763 and fig['death_year'] is None and fig['courtesy_name'] == u'三白' and fig['style_name'] == u'梅逸')
    check('J08', 'figure', u'famous_quote 有源（主选口径）', u'布衣菜饭' in fig['famous_quote'] and 'W8' in fig['famous_quote_source'])

    # K 报告
    kk = os.path.isfile(REPORT)
    check('K01', 'report', u'重建报告存在', kk)
    rtxt = io.open(REPORT, encoding='utf-8').read() if kk else ''
    check('K02', 'report', u'报告含产物清单与核验段（>=4KB）', len(rtxt) >= 4000)
    check('K03', 'report', u'报告指向 SHF-1 素材与 H-SHF-001', ('H-SHF-001' in rtxt) and ('SHF-1' in rtxt) and kk)

    npass = len([r for r in RESULTS if r['status'] == 'PASS'])
    nfail = len([r for r in RESULTS if r['status'] == 'FAIL'])
    nwarn = len([r for r in RESULTS if r['status'] == 'WARN'])
    ev = dict(card='t_a7d233f0', figure_code=FIG, generated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
              script='verify_phase21r9_shenfu.py（合并后口径复跑，卡 t_a7d233f0）',
              counts=dict(pass_=npass, fail=nfail, warn=nwarn),
              merged_by='t_a7d233f0',
              results=RESULTS, quote_table=quote_rows, witness_hits=witness_sha_rows, witness_sha=rows,
              verdict='ALL PASS' if nfail == 0 else 'HAS FAILURES')
    out = os.path.join(REPO, 'docs/research/phase21r9_shenfu_verify_evidence_merged.json')
    with io.open(out, 'w', encoding='utf-8') as f:
        json.dump(ev, f, ensure_ascii=False, indent=1)
        f.write(u'\n')
    print('TOTAL: %d PASS / %d FAIL / %d WARN' % (npass, nfail, nwarn))
    return 0 if nfail == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
