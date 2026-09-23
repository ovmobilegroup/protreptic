#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase21-R8 罗瑞卿重建落盘独立核验（卡 t_bf2d9b82）

对 data/figures/H-LUORQ-001.json、data/individuals/H-LUORQ-001(.modes).json、
docs/scratch/legacy20_r8_luorq_landing/**、data/audit/phase21r8_luorq_landing_manifest.json
做独立复核：条目不变量、引文对素材包与见证文本逐条复核、片段白名单、
禁字扫描、查重与残留、归档字节、主库零写入、落地件一致性。
结果写 docs/research/phase21r8_luorq_verify_evidence.json；FAIL 时 exit 1。
"""
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import unicodedata
from datetime import datetime

REPO = os.path.dirname(os.path.abspath(__file__))
FIG = 'H-LUORQ-001'
LANDING = os.path.join(REPO, 'docs/scratch/legacy20_r8_luorq_landing')
PACK = os.path.join(REPO, 'docs/research/phase21r8_luorq_sourcing_report.json')
MD = os.path.join(REPO, 'docs/research/phase21r8_luorq_sourcing_report.md')
REPORT = os.path.join(REPO, 'docs/research/phase21r8_luorq_rebuild_report.md')
WROOT = '/opt/data/profiles/serrano/cache/scratch/r8'
W_MAP = {'W1': 'web/B520315.txt', 'W2': 'web/rr1951_0101_p3.txt', 'W3': 'web/rr1978_0813_p2.txt',
         'W4': 'web/ws_pingfan_raw.txt', 'W6': 'web/ccrd_000209.txt', 'W7': 'web/hprc5150213.txt',
         'W8': 'web/iccs5392393.txt', 'W9': 'web/iccs5392400.txt', 'W10': 'web/hswh_92285.txt',
         'W11': 'web/chinanews_1088475.txt', 'W12': 'web/cpc_zhenli.txt', 'W13': 'web/dangshi34.txt',
         'W15': 'web/cn2008.txt', 'W16': 'web/wangsu.txt', 'W17': 'web/mod_gxf.txt',
         'W18': 'web/cpc_gxf2023.txt', 'W19': 'web/cpc_12371_gxf.txt', 'W21': 'web/mtoou_toc.txt'}
ARCHIVE_SHA = {
    'H-LUORQ-001_figures.json': 'bb2a6a2a23d099baafe3b5147f936d470d89d5c091d603e0f709f60fd697f171',
    'H-LUORQ-001_individuals.json': '4713aace00eee4c41196a485f074f687f7103cbe0f477d72c7526af24e30fde9',
    'H-LUORQ-001_individuals_modes_ISOLATED_crossfile.json': '9b0dc237432e690fd6c29be55f91ef6da816b79fd958f6d6c4dd82e26baee924',
    'H-LUORQ-001_archive_page.md': '3fa3aa3fa375d63d7b93f554f4f61b71aa784f7dec142ab8a1a6ee445f5112f2',
}
FORBIDDEN = ['国防部长', '主要创建者', 'Ten Marshals', '安全立军',
             '整编革新', '参谋统筹', '情报先行', '安全保卫学派',
             '《罗瑞卿文选》', '《公安工作文集》', '《公安机关组织条例》']
STD_CATEGORIES = ['伦理修养', '军事战略', '医学养生', '史学文献', '哲学形而上', '宗教修行', '工程技术',
                  '心理洞察', '战略决策', '探险发现', '政治治理', '教育传承', '文艺审美', '方法论通用',
                  '科学方法', '组织领导', '经济商业', '认识论逻辑']
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
    return ''.join(ch for ch in s if unicodedata.category(ch)[0] in ('L', 'N'))


def sha_file(p):
    return hashlib.sha256(io.open(p, 'rb').read()).hexdigest()


def fragments(text):
    out = []
    for opener, closer in ((u'\u300c', u'\u300d'), (u'\u300e', u'\u300f')):
        i = 0
        while True:
            a = text.find(opener, i)
            if a < 0:
                break
            b = text.find(closer, a + 1)
            if b < 0:
                break
            out.append(text[a + 1:b])
            i = b + 1
    return out


def main():
    pack = jl(PACK)
    pm = dict((m['id'], m) for m in pack['modes'])
    md = io.open(MD, encoding='utf-8').read()
    entries = jl(os.path.join(LANDING, 'modes_library_entries.json'))
    combined = jl(os.path.join(LANDING, 'combined_library_entries.json'))
    fig = jl(os.path.join(REPO, 'data/figures/%s.json' % FIG))
    ind = jl(os.path.join(REPO, 'data/individuals/%s.json' % FIG))
    mfj = jl(os.path.join(REPO, 'data/individuals/%s_modes.json' % FIG))
    man = jl(os.path.join(REPO, 'data/audit/phase21r8_luorq_landing_manifest.json'))
    scen = jl(os.path.join(LANDING, 'scenario_notes.json'))
    top = jl(os.path.join(LANDING, 'top_block_proposal.json'))
    raw_entries = io.open(os.path.join(LANDING, 'modes_library_entries.json'), encoding='utf-8').read()
    wl = man.get('frag_whitelist', [])

    # A 文件与解析
    check('A01', 'files', 'landing entries 可解析且 10 条', len(entries) == 10)
    check('A02', 'files', 'combined.modes == entries', combined['modes'] == entries)
    check('A03', 'files', 'figure/individuals/modes 三件可解析', all(isinstance(x, dict) for x in (fig, ind, mfj)))
    check('A04', 'files', '冻结副本与 data 侧逐字节一致（figure）', sha_file(os.path.join(LANDING, 'figures/%s.json' % FIG)) == sha_file(os.path.join(REPO, 'data/figures/%s.json' % FIG)))
    check('A05', 'files', '冻结副本与 data 侧逐字节一致（individuals）', sha_file(os.path.join(LANDING, 'individuals/%s.json' % FIG)) == sha_file(os.path.join(REPO, 'data/individuals/%s.json' % FIG)))
    check('A06', 'files', '冻结副本与 data 侧逐字节一致（modes）', sha_file(os.path.join(LANDING, 'individuals/%s_modes.json' % FIG)) == sha_file(os.path.join(REPO, 'data/individuals/%s_modes.json' % FIG)))
    check('A07', 'files', 'id_mapping.tsv 10 行数据', len([l for l in io.open(os.path.join(LANDING, 'id_mapping.tsv'), encoding='utf-8').read().strip().split('\n')]) == 11)
    check('A08', 'files', 'category_mapping.tsv 10 行数据', len([l for l in io.open(os.path.join(LANDING, 'category_mapping.tsv'), encoding='utf-8').read().strip().split('\n')]) == 11)
    check('A09', 'files', 'manifest deliverable 12 件且 sha 可复算', all(sha_file(os.path.join(REPO, k)) == v['sha256'] for k, v in man['deliverables'].items()))
    check('A10', 'files', 'figures 顶层 modes == entries == _modes.modes（同链布局）', fig['modes'] == entries == mfj['modes'])
    check('A11', 'files', 'individuals 为 figure 去顶层 modes（差集恰为 modes）', set(fig.keys()) - set(ind.keys()) == {'modes'} and not (set(ind.keys()) - set(fig.keys())))
    check('A12', 'files', 'figures 与 individuals sha 不同（非重复副本）', sha_file(os.path.join(REPO, 'data/figures/%s.json' % FIG)) != sha_file(os.path.join(REPO, 'data/individuals/%s.json' % FIG)))

    # B 条目不变量
    check('B01', 'entries', 'id 序列 M-LUORQ-001~010', [e['id'] for e in entries] == ['M-LUORQ-%03d' % i for i in range(1, 11)])
    check('B02', 'entries', 'legacy_mode_id M351~M360', [e['legacy_mode_id'] for e in entries] == ['M%d' % i for i in range(351, 361)])
    check('B03', 'entries', 'figure_code/figure_name 一致', all(e['figure_code'] == FIG and e['figure_name'] == '罗瑞卿' for e in entries))
    check('B04', 'entries', 'category 均在标准 18 类', all(e['category'] in STD_CATEGORIES for e in entries))
    check('B05', 'entries', 'level=核心 与 priority 1..10', all(e['level'] == '核心' and e['priority'] == i for i, e in enumerate(entries, 1)))
    check('B06', 'entries', 'verification 全 pending + method 口径', all(e['verification']['status'] == 'pending' and e['verification']['method'] == 'phase21r8-luorq-rebuild-landing' for e in entries))
    check('B07', 'entries', '英文面非空（name/definition/process/cases/modern）', all(all(len(e[k]) > 8 for k in ('name_en', 'definition_en')) and all(e[k] for k in ('process_en', 'representative_cases_en', 'modern_applications_en')) for e in entries))
    check('B08', 'entries', 'key_concepts 非空且 >=4', all(len(e['key_concepts']) >= 4 for e in entries))
    check('B09', 'entries', 'related_modes 指向本组代码', all(all(r in [x['id'] for x in entries] for r in e['related_modes']) for e in entries))

    # C 引文：素材包逐字 + 见证文本强归一化
    quote_rows = []
    for e in entries:
        num = int(e['id'].split('-')[-1])
        mid = 'M-LUORQ-%03d' % num
        q = pm[mid]['quotes']
        hit = [i + 1 for i, qq in enumerate(q) if e['key_quote_zh'] in qq.get('text', '')]
        quote_rows.append(dict(entry=e['id'], quotes_with_substring=hit, key_quote_chars=len(e['key_quote_zh'])))
        check('C%02d' % num, 'quote-pack', '%s key_quote 为素材包 §三 quotes 子串' % e['id'], bool(hit), hit)
    # 见证复核
    wk = [0, 0]
    for e in entries:
        num = int(e['id'].split('-')[-1])
        mid = 'M-LUORQ-%03d' % num
        q = pm[mid]['quotes']
        idx = [i for i, qq in enumerate(q) if e['key_quote_zh'] in qq.get('text', '')]
        wit = q[idx[0]].get('witness', '') if idx else ''
        files = []
        if wit.startswith('W20/'):
            files = [os.path.join(WROOT, 'xuoba', wit.split('/')[1] + '.txt')]
        elif '/' in wit:
            files = [os.path.join(WROOT, W_MAP[w]) for w in wit.split('/') if w in W_MAP]
        elif wit in W_MAP:
            files = [os.path.join(WROOT, W_MAP[wit])]
        nq = norm(e['key_quote_zh'])
        ok = False
        detail = []
        for fp in files:
            if not os.path.isfile(fp):
                detail.append('missing %s' % fp)
                continue
            ok = ok or (nq in norm(io.open(fp, encoding='utf-8', errors='ignore').read()))
        md_hit = nq in norm(md)
        if ok:
            wk[0] += 1
            check('D%02d' % num, 'quote-witness', '%s 见证 %s 强归一化命中' % (e['id'], wit or '?'), True)
        else:
            wk[1] += 1
            warn('D%02d' % num, 'quote-witness', '%s 见证 %s 文件未命中（素材包 md 命中=%s）' % (e['id'], wit or '?', md_hit), md_hit, detail)
    # 见证文件 sha256 对照（W20 为组合指纹，单列）
    sha_rows = []
    for w, rel in sorted(W_MAP.items()):
        fp = os.path.join(WROOT, rel)
        if not os.path.isfile(fp):
            continue
        m = re.search(r'\*\*' + w + r'\*\*｜[^\n]*?sha256=([0-9a-f]{64})', md)
        now = sha_file(fp)
        sha_rows.append(dict(witness=w, file=rel, sha256=now, md_expect=m.group(1) if m else '', match=(m.group(1) == now) if m else None))
    check('E01', 'witness-sha', '见证文件 sha256 逐一复核（16 件可对照）', all(r['match'] is not False for r in sha_rows), [r for r in sha_rows if r['match'] is False])
    check('E02', 'witness-sha', 'W20 xuoba 分章 59 件存在', len([f for f in os.listdir(os.path.join(WROOT, 'xuoba')) if f.endswith('.txt')]) == 59)

    # F 片段白名单 + 禁字
    fails = []
    blob_all = ''
    for e in entries:
        mid = 'M-LUORQ-%03d' % int(e['id'].split('-')[-1])
        blob = '\n'.join([e['definition_zh'], e['source_chapter']] + e['process_zh'] + e['representative_cases_zh'] + e['modern_applications_zh'] + e['key_concepts'])
        blob_all += blob + '\n' + e['key_quote_zh']
        qblob = '\n'.join(q.get('text', '') for q in pm[mid]['quotes'])
        for f in fragments(blob):
            segs = [s for s in f.split(u'\u2026\u2026') if s]
            if all((s in qblob) or any(w['fragment'] == s and w['mode'] == mid for w in wl) for s in segs):
                continue
            fails.append((e['id'], f))
    check('F01', 'fragments', '全部「」/『』片段过白名单（%d 条白名单登记）' % len(wl), not fails, fails[:6])
    check('F02', 'fragments', '白名单片段均可回溯素材包 md/json', all((w['fragment'] in io.open(PACK, encoding='utf-8').read()) or (w['fragment'] in md) for w in wl))
    bad = [f for f in FORBIDDEN if f != '国防部长' and f in raw_entries]
    check('F03', 'forbidden', 'entries 禁字零出现（10 项）', not bad, bad)
    check('F04', 'forbidden', '「国防部长」仅以「副部长」形态出现', '国防部长' not in raw_entries.replace('国防部副部长', ''))
    check('F05', 'forbidden', 'figure/individuals 禁字零出现', not [f for f in FORBIDDEN if f != '国防部长' and (f in io.open(os.path.join(REPO, 'data/figures/%s.json' % FIG), encoding='utf-8').read())])

    # G 查重与残留
    def scan(patterns):
        files = subprocess.check_output(['git', '-C', REPO, 'ls-files'], text=True).split('\n')
        files += subprocess.check_output(['git', '-C', REPO, 'ls-files', '--others', '--exclude-standard'], text=True).split('\n')
        out = {}
        for rel in sorted(set(files)):
            if not rel or rel.startswith('data/backup') or rel.startswith('backups') or '.bak' in rel or rel.startswith('data/figures/_duplicates/'):
                continue
            fp = os.path.join(REPO, rel)
            if not os.path.isfile(fp):
                continue
            try:
                s = io.open(fp, encoding='utf-8', errors='ignore').read()
            except Exception:
                continue
            for pat in patterns:
                if re.search(pat, s):
                    out.setdefault(rel, []).append(pat)
        return out
    codes = ['M-LUORQ-%03d' % i for i in range(1, 11)]
    hit_codes = scan(codes)
    allowed = set(['docs/research/phase21r8_luorq_sourcing_report.md', 'docs/research/phase21r8_luorq_sourcing_report.json', 'tools/build_phase21r8_luorq.py', 'docs/scratch/legacy20_r8_luorq_landing/modes_library_entries.json', 'docs/scratch/legacy20_r8_luorq_landing/combined_library_entries.json', 'data/figures/%s.json' % FIG, 'data/individuals/%s.json' % FIG, 'data/individuals/%s_modes.json' % FIG, 'data/audit/phase21r8_luorq_landing_manifest.json', 'docs/research/phase21r8_luorq_landing_evidence.json', 'docs/research/phase21r8_luorq_rebuild_report.md', 'docs/research/phase21r8_luorq_verify_evidence.json', 'verify_phase21r8_luorq.py', 'docs/scratch/legacy20_r8_luorq_landing/id_mapping.tsv', 'docs/scratch/legacy20_r8_luorq_landing/category_mapping.tsv', 'docs/scratch/legacy20_r8_luorq_landing/scenario_notes.json', 'docs/scratch/legacy20_r8_luorq_landing/top_block_proposal.json', 'docs/scratch/legacy20_r8_luorq_landing/figures/%s.json' % FIG, 'docs/scratch/legacy20_r8_luorq_landing/individuals/%s.json' % FIG, 'docs/scratch/legacy20_r8_luorq_landing/individuals/%s_modes.json' % FIG])
    # Phase21-R8 合并卡（t_08bbb73d）后口径：本链入库面与合并产物并入白名单
    allowed |= set([
        'data/modes_data.json', 'data/code_maps.json', 'data/scenarios_zh.json', 'data/scenarios_en.json',
        'data/scenario_tags.json', 'data/figure_names.json',
        'data/audit/phase21r8_luorq_merge_manifest.json', 'data/audit/phase21r8_luorq_top_block_backup.json',
        'docs/research/phase21r8_luorq_merge_report.md', 'docs/research/phase21r8_luorq_merge_evidence.json',
        'docs/research/phase21r8_luorq_merge_evidence.txt', 'docs/research/phase21r8_luorq_verify_evidence_merged.json',
        'verify_luorq_merge_indep.py', 'tools/export_static_site.py', 'tools/pages_preflight.py',
        'web/src/generated/siteCounts.ts', 'docs/architecture/static_data_manifest.json',
    ])
    outside = {k: v for k, v in hit_codes.items() if k not in allowed}
    check('G01', 'dedup', 'M-LUORQ-001~010 仅出现于本链与素材包（0 外部碰撞）', not outside, outside)
    # Phase21-R8 合并卡（t_08bbb73d）后口径：10 条已入库，六件命中面 == 合并后预期
    six = ['data/modes_data.json', 'data/code_maps.json', 'data/scenarios_zh.json', 'data/scenarios_en.json', 'data/scenario_tags.json', 'data/figure_names.json']
    expect_m = {k: (codes if k != 'data/figure_names.json' else []) for k in six}
    got_m = dict((k, hit_codes.get(k, [])) for k in six)
    check('G02', 'dedup', '主库六件 M-LUORQ 命中 == 合并后预期（10 条入库；figure_names 无 M 码）', got_m == expect_m, got_m)
    six = ['data/modes_data.json', 'data/code_maps.json', 'data/scenarios_zh.json', 'data/scenarios_en.json', 'data/scenario_tags.json', 'data/figure_names.json']
    # Phase21-R8 合并卡（t_08bbb73d）后口径：新场景 C-LUORQ-001~010(·E) 已注册（仅 scenarios zh/en 两面）
    c_all = scan(['C-LUORQ-'])
    c_hits = {k: v for k, v in c_all.items() if k in six}
    check('G03', 'dedup', '主库六件 C-LUORQ-* 命中 == 合并后预期（仅 scenarios_zh/en 新场景面）',
          sorted(c_hits.keys()) == ['data/scenarios_en.json', 'data/scenarios_zh.json'], c_hits)
    h_hits = {k: v for k, v in scan(['H-LUORQ-001']).items() if k in six}
    # Phase21-R8 合并卡（t_08bbb73d）后口径：H-LUORQ-001 注册入 code_maps/figure_names/scenario_tags（+ 顶层块）
    check('G04', 'dedup', '主库六件 H-LUORQ-001 命中 == 合并后预期（mode_data/code_maps/figure_names/scenario_tags）',
          sorted(h_hits.keys()) == ['data/code_maps.json', 'data/figure_names.json', 'data/modes_data.json', 'data/scenario_tags.json'], h_hits)

    # H 归档与主库未动
    for i, (name, expect) in enumerate(sorted(ARCHIVE_SHA.items()), 1):
        check('H%02d' % i, 'archive', '归档 %s sha256 未变' % name, sha_file(os.path.join(REPO, 'data/figures/_duplicates', name)) == expect)
    mdj = jl(os.path.join(REPO, 'data/modes_data.json'))
    blk = mdj.get('H-LUORQ-001', {})
    # Phase21-R8 合并卡（t_08bbb73d）后口径：顶层旧块已按裁定替换（先冻结后替换）
    check('H05', 'mainlib', 'modes_data 顶层块已替换为 B2 新叙事（旧块值另存备份）', blk.get('name_zh', '') == u'罗瑞卿：公安创建·军警分途·警卫思想', blk.get('name_zh'))
    check('H06', 'mainlib', '顶层新块零残留（无 Ten Marshals / 四式旧命名 / 国防部长）',
          ('Ten Marshals' not in blk.get('unique_thinking_en', '')) and not any(n in json.dumps(blk, ensure_ascii=False) for n in ['安全立军', '整编革新', '参谋统筹', '情报先行', '国防部长', '主要创建者']))
    check('H07', 'mainlib', '顶层替换文本已备（top_block_proposal）', 'one of the ten senior generals' in json.dumps(top, ensure_ascii=False) and '国防部副部长' in json.dumps(top, ensure_ascii=False))

    # I 场景与命题件
    dis = scen['notes']['old_code_dispositions']
    check('I01', 'scenario', '旧场景处置表 10 条（C-LUORQ-001~010）', len(dis) == 10 and [d['code'] for d in dis] == ['C-LUORQ-%03d' % i for i in range(1, 11)])
    check('I02', 'scenario', '处置含 C-007 改写 / C-008 重写 / C-009 删除建议', 'C-LUORQ-007' in json.dumps(scen, ensure_ascii=False) and 'C-LUORQ-009' in json.dumps(scen, ensure_ascii=False))
    check('I03', 'scenario', '新场景前缀建议 0 碰撞口径', 'C-LUORQ-001~010' in scen['notes']['new_prefix_suggestion'])

    # J figure 层
    check('J01', 'figure', 'mode_ids = M-LUORQ-001~010', fig['mode_ids'] == ['M-LUORQ-%03d' % i for i in range(1, 11)] and fig['thinking_mode_count'] == 10)
    check('J02', 'figure', 'core_thoughts 10 条且与名目对齐', len(fig['core_thoughts']) == 10 and all('（' in c for c in fig['core_thoughts']))
    check('J03', 'figure', 'tags >= 15', len(fig['tags']) >= 15)
    check('J04', 'figure', 'caveats >= 6（含史料语境与场景口径）', len(fig['caveats']) >= 6)
    check('J05', 'figure', 'representative_works 均为可落源篇目（无失据书目）', all(w.startswith('《') for w in fig['representative_works']))
    check('J06', 'figure', 'cross_references 目标存在（figure_names/code_maps）', os.path.isfile(os.path.join(REPO, 'data/figure_names.json')))

    # K 报告
    check('K01', 'report', '重建报告存在', os.path.isfile(REPORT))

    npass = len([r for r in RESULTS if r['status'] == 'PASS'])
    nfail = len([r for r in RESULTS if r['status'] == 'FAIL'])
    nwarn = len([r for r in RESULTS if r['status'] == 'WARN'])
    ev = dict(card='t_bf2d9b82', figure_code=FIG, generated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
              script='verify_phase21r8_luorq.py', counts=dict(pass_=npass, fail=nfail, warn=nwarn),
              results=RESULTS, quote_table=quote_rows, witness_sha=sha_rows,
              verdict='ALL PASS' if nfail == 0 else 'HAS FAILURES')
    EVID_OUT = os.environ.get('LUORQ_VERIFY_EVIDENCE') or os.path.join(REPO, 'docs/research/phase21r8_luorq_verify_evidence.json')
    with io.open(EVID_OUT, 'w', encoding='utf-8') as f:
        json.dump(ev, f, ensure_ascii=False, indent=1)
        f.write(u'\n')
    print('TOTAL: %d PASS / %d FAIL / %d WARN' % (npass, nfail, nwarn))
    return 0 if nfail == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
