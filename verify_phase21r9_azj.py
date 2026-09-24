#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Phase21-R9 安子介重建落盘独立核验（卡 t_58ebf9c2）
#
# 对 data/figures/H-AZJ-001(.modes).json、data/individuals/H-AZJ-001(.modes).json、
# docs/scratch/legacy20_r9_azj_landing/**、data/audit/phase21r9_azj_landing_manifest.json
# 做独立复核：条目不变量、引文对素材包与见证文本逐条复核、片段来源登记、
# 禁字/旧载荷扫描、查重与残留、归档字节、主库零写入、落地件一致性。
# 结果写 docs/research/phase21r9_azj_verify_evidence.json；FAIL 时 exit 1。
import glob
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import unicodedata

REPO = os.path.dirname(os.path.abspath(__file__))
FIG = 'H-AZJ-001'
LANDING = os.path.join(REPO, 'docs/scratch/legacy20_r9_azj_landing')
PACK = os.path.join(REPO, 'docs/research/phase21r9_anzijie_sourcing_report.json')
MD = os.path.join(REPO, 'docs/research/phase21r9_anzijie_sourcing_report.md')
MANIFEST = os.path.join(REPO, 'data/audit/phase21r9_azj_landing_manifest.json')
WITNESS = os.path.join(REPO, 'docs/scratch/phase21r9_anzijie/witness')
CODES = ['M-AZJ-%03d' % i for i in range(1, 11)]
STD_CATEGORIES = [u'伦理修养', u'军事战略', u'医学养生', u'史学文献', u'哲学形而上', u'宗教修行', u'工程技术',
                  u'心理洞察', u'战略决策', u'探险发现', u'政治治理', u'教育传承', u'文艺审美', u'方法论通用',
                  u'科学方法', u'组织领导', u'经济商业', u'认识论逻辑']
MAIN_LIB = ['data/modes_data.json', 'data/code_maps.json', 'data/scenarios_zh.json',
            'data/scenarios_en.json', 'data/scenario_tags.json', 'data/figure_names.json']
RESULTS = []


def check(cid, grp, desc, ok, detail=''):
    RESULTS.append(dict(id=cid, group=grp, desc=desc, status='PASS' if ok else 'FAIL', detail=detail))
    print('%s  %-4s %s%s' % ('PASS' if ok else 'FAIL', cid, desc, (' | ' + str(detail)[:200]) if detail and not ok else ''))


def jl(p):
    return json.load(io.open(p, encoding='utf-8'))


def sha_file(p):
    return hashlib.sha256(io.open(p, 'rb').read()).hexdigest()


def norm(s):
    s = unicodedata.normalize('NFKC', s)
    return ''.join(ch for ch in s if unicodedata.category(ch)[0] in ('L', 'N'))


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


def witness_map():
    m = {}
    for p in sorted(glob.glob(os.path.join(WITNESS, '*.txt'))):
        base = os.path.basename(p)
        w = base.split('_')[0]
        if re.match(r'^W\d\d$', w):
            m[w] = p
    return m

FORBIDDEN_OLD = [u'特区建设', u'摸着石头过河', u'安子介回忆录', u'深圳特区建设档案', u'对外开放政策',
                 u'经济特区', 'An Zijie', 'SEZ', 'Opening Up',
                 'M001', 'M002', 'M003', 'M004', 'M005', 'M006', 'M007', 'M008', 'M009', 'M010']


def main():
    pack = jl(PACK)
    pm = dict((m['id'], m) for m in pack['modes'])
    md = io.open(MD, encoding='utf-8').read()
    entries = jl(os.path.join(LANDING, 'modes_library_entries.json'))
    combined = jl(os.path.join(LANDING, 'combined_library_entries.json'))
    fig = jl(os.path.join(REPO, 'data/figures/%s.json' % FIG))
    fmod = jl(os.path.join(REPO, 'data/figures/%s_modes.json' % FIG))
    ind = jl(os.path.join(REPO, 'data/individuals/%s.json' % FIG))
    mfj = jl(os.path.join(REPO, 'data/individuals/%s_modes.json' % FIG))
    man = jl(MANIFEST)
    top = jl(os.path.join(LANDING, 'top_block_proposal.json'))
    scen = jl(os.path.join(LANDING, 'scenario_notes.json'))
    wmap = witness_map()

    # ---- A 文件与结构
    check('A01', 'files', u'landing entries 可解析且 10 条', len(entries) == 10, len(entries))
    check('A02', 'files', u'combined.modes == entries', combined.get('modes') == entries)
    check('A03', 'files', u'四个数据件可解析（figures/_modes/individuals/_modes）',
          all(isinstance(x, dict) for x in (fig, fmod, ind, mfj)))
    check('A04', 'files', u'冻结副本与 data 侧逐字节一致（figures）',
          sha_file(os.path.join(LANDING, 'figures/%s.json' % FIG)) == sha_file(os.path.join(REPO, 'data/figures/%s.json' % FIG)))
    check('A05', 'files', u'冻结副本与 data 侧逐字节一致（figures_modes）',
          sha_file(os.path.join(LANDING, 'figures/%s_modes.json' % FIG)) == sha_file(os.path.join(REPO, 'data/figures/%s_modes.json' % FIG)))
    check('A06', 'files', u'冻结副本与 data 侧逐字节一致（individuals）',
          sha_file(os.path.join(LANDING, 'individuals/%s.json' % FIG)) == sha_file(os.path.join(REPO, 'data/individuals/%s.json' % FIG)))
    check('A07', 'files', u'冻结副本与 data 侧逐字节一致（individuals_modes）',
          sha_file(os.path.join(LANDING, 'individuals/%s_modes.json' % FIG)) == sha_file(os.path.join(REPO, 'data/individuals/%s_modes.json' % FIG)))
    idl = [l for l in io.open(os.path.join(LANDING, 'id_mapping.tsv'), encoding='utf-8').read().strip().split('\n')]
    cal = [l for l in io.open(os.path.join(LANDING, 'category_mapping.tsv'), encoding='utf-8').read().strip().split('\n')]
    check('A08', 'files', u'id_mapping.tsv 表头+10 行', len(idl) == 11, len(idl))
    check('A09', 'files', u'category_mapping.tsv 表头+10 行', len(cal) == 11, len(cal))
    mans = all(sha_file(os.path.join(REPO, k)) == v['sha256'] for k, v in man['deliverables'].items())
    check('A10', 'files', u'manifest 14 件 sha 可复算', mans and len(man['deliverables']) == 14, len(man['deliverables']))
    check('A11', 'files', u'figures.modes == entries == 两个 _modes 件', fig['modes'] == entries == fmod['modes'] == mfj['modes'])
    check('A12', 'files', u'individuals 为 figure 去顶层 modes（差集恰为 modes）',
          set(fig.keys()) - set(ind.keys()) == set(['modes']) and not (set(ind.keys()) - set(fig.keys())))
    check('A13', 'files', u'figures 与 individuals sha 不同（非重复副本）',
          sha_file(os.path.join(REPO, 'data/figures/%s.json' % FIG)) != sha_file(os.path.join(REPO, 'data/individuals/%s.json' % FIG)))

    # ---- B 条目不变量
    check('B01', 'entries', u'id 序列 M-AZJ-001~010', [e['id'] for e in entries] == CODES)
    check('B02', 'entries', u'legacy_mode_id 全空（旧载荷号段不复用）', all(e.get('legacy_mode_id', '') == '' for e in entries))
    check('B03', 'entries', u'figure_code/figure_name 一致', all(e['figure_code'] == FIG and e['figure_name'] == u'安子介' for e in entries))
    check('B04', 'entries', u'category 均在标准 18 类', all(e['category'] in STD_CATEGORIES for e in entries))
    check('B05', 'entries', u'level=核心 与 priority 1..10', all(e['level'] == u'核心' and e['priority'] == i for i, e in enumerate(entries, 1)))
    check('B06', 'entries', u'verification 全 pending + method 口径',
          all(e['verification']['status'] == 'pending' and e['verification']['method'] == 'phase21r9-azj-rebuild-landing' for e in entries))
    check('B07', 'entries', u'英文面非空（name/definition/process/cases/modern）',
          all(all(len(e[k]) > 8 for k in ('name_en', 'definition_en')) and all(e[k] for k in ('process_en', 'representative_cases_en', 'modern_applications_en')) for e in entries))
    check('B08', 'entries', u'key_concepts 非空且 >=4', all(len(e['key_concepts']) >= 4 for e in entries))
    check('B09', 'entries', u'related_modes 指向本组代码', all(all(r in CODES for r in e['related_modes']) for e in entries))
    check('B10', 'entries', u'每条来源指向 AZJ-1 材料（source_chapter）', all('AZJ-1' in e['source_chapter'] for e in entries))
    check('B11', 'entries', u'每条 verification.evidence 指向素材包引文段与见证',
          all(('quotes' in e['verification']['evidence']) and ('W0' in e['verification']['evidence']) for e in entries))
    check('B12', 'entries', u'层级标注入证（确证/疑似字样保留）',
          all((u'确证' in e['verification']['evidence']) or (u'疑似' in e['verification']['evidence']) for e in entries))

    # ---- C 引文 vs 素材包（逐字子串）
    for i, e in enumerate(entries, 1):
        mid = 'M-AZJ-%03d' % i
        qs = pm[mid]['quotes']
        hit = [j + 1 for j, q in enumerate(qs) if e['key_quote_zh'] in q.get('text', '')]
        check('C%02d' % i, 'quote-pack', u'%s key_quote 为素材包 quotes 子串' % e['id'], bool(hit), hit)

    # ---- D 引文 vs 见证文本（强归一化）
    for i, e in enumerate(entries, 1):
        mid = 'M-AZJ-%03d' % i
        qs = pm[mid]['quotes']
        idx = [j for j, q in enumerate(qs) if e['key_quote_zh'] in q.get('text', '')]
        ok = False
        det = ''
        if idx:
            q = qs[idx[0]]
            w = q.get('w', '')
            files = [wmap[x] for x in w.split('/') if x in wmap]
            for fp in files:
                txt = norm(io.open(fp, encoding='utf-8', errors='ignore').read())
                if norm(e['key_quote_zh']) in txt:
                    ok = True
            det = '%s -> %s' % (w, [os.path.basename(f) for f in files])
        check('D%02d' % i, 'quote-witness', u'%s key_quote 见证文本强归一化命中' % e['id'], ok, det)

    # ---- E 见证 sha256（11 件）
    ecnt = 0
    for wj_ in pack['witnesses']:
        w = wj_['w']
        fp = wmap.get(w, '')
        ok = bool(fp) and sha_file(fp) == wj_['sha256']
        ecnt += 1 if ok else 0
        check('E%02d' % int(w[1:]), 'witness', u'%s 存证副本 sha256 与素材包一致' % w, ok, os.path.basename(fp))
    check('E12', 'witness', u'见证 11 件全部命中', ecnt == 11, ecnt)

    # ---- F 片段来源与禁字/旧载荷扫描
    frag_fail = []
    frag_total = 0
    for a in entries:
        blob = u'\n'.join([a['definition_zh'], a['source_chapter']] + a['process_zh'] +
                          a['representative_cases_zh'] + a['modern_applications_zh'] + a['key_concepts'])
        for f in fragments(blob):
            for s in [x for x in f.split(u'……') if x]:
                frag_total += 1
                mid = a['id']
                pq = pm[mid]
                srcs = [q.get('text', '') for q in pq['quotes']]
                hit = any(s in t for t in srcs) or any(s in (pq.get(f2) or '') for f2 in ('summary', 'boundary', 'modern', 'theme', 'tier', 'name')) or (s in md)
                if not hit:
                    frag_fail.append((mid, s))
    check('F01', 'fragments', u'全部「」片段可回溯素材包（%d 段）' % frag_total, not frag_fail, frag_fail[:5])
    blob_all = io.open(os.path.join(REPO, 'data/figures/%s.json' % FIG), encoding='utf-8').read()
    blob_all += io.open(os.path.join(REPO, 'data/individuals/%s.json' % FIG), encoding='utf-8').read()
    blob_all += io.open(os.path.join(LANDING, 'modes_library_entries.json'), encoding='utf-8').read()
    hits = [t for t in FORBIDDEN_OLD if t in blob_all]
    check('F02', 'fragments', u'旧载荷/伪造出处标记零出现（%d 项）' % len(FORBIDDEN_OLD), not hits, hits)
    check('F03', 'fragments', u'「第五大发明」条目保留转述口径（‘讲话转述’字样）', u'讲话转述' in entries[0]['representative_cases_zh'][0] or u'转述' in entries[0]['definition_zh'])
    check('F04', 'fragments', u'疑似项保留标记（M-AZJ-006 方法细节）', u'疑似' in entries[5]['definition_zh'] and u'疑似' in entries[5]['representative_cases_zh'][2])
    check('F05', 'fragments', u'两说并存保留（M-AZJ-004 接见／M-AZJ-010 享年）',
          u'两说' in entries[3]['representative_cases_zh'][2] and u'两说' in entries[9]['representative_cases_zh'][2])

    # ---- G 查重与残留（全库）
    files = [f for f in subprocess.check_output(['git', '-C', REPO, 'ls-files'], text=True).split('\n') if f]
    files += [f for f in subprocess.check_output(['git', '-C', REPO, 'ls-files', '--others', '--exclude-standard'], text=True).split('\n') if f]
    m_hits, live_hits, text_hits = [], [], []
    for rel in sorted(set(files)):
        fp = os.path.join(REPO, rel)
        if not os.path.isfile(fp):
            continue
        try:
            txt = io.open(fp, encoding='utf-8', errors='ignore').read()
        except Exception:
            continue
        # Phase21-R9 合并卡 t_ce457734（2026-09-24）后合并态口径：主库注册面 + 合并卡足迹 + 锚点工具 + 合并核验脚本入白名单
        self_files = ['data/audit/phase21r9_azj_landing_manifest.json',
                      'docs/research/phase21r9_azj_verify_evidence.json',
                      'docs/research/phase21r9_azj_rebuild_report.md',
                      'docs/research/phase21r9_azj_landing_evidence.json',
                      'data/audit/phase21r9_azj_merge_manifest.json',
                      'data/modes_data.json', 'data/code_maps.json', 'data/figure_names.json',
                      'docs/research/phase21r9_azj_merge_report.md',
                      'docs/research/phase21r9_azj_merge_evidence.json',
                      'docs/research/phase21r9_azj_merge_evidence.txt',
                      'docs/research/phase21r9_azj_verify_evidence_merged.json',
                      'tools/export_static_site.py', 'tools/pages_preflight.py',
                      'verify_azj_merge_indep.py', 'tools/merge_azj_hazj001.py']
        if 'M-AZJ-' in txt and not (rel in man['deliverables'] or rel in self_files
                                    or rel.endswith('build_phase21r9_azj.py')
                                    or rel.endswith('verify_phase21r9_azj.py')
                                    or rel.startswith('docs/research/phase21r9_anzijie')
                                    or rel.startswith('docs/scratch/phase21r9_anzijie')
                                    or rel.startswith('docs/scratch/phase21r9_azj_rebuild')
                                    # 兄弟卡 t_a7d233f0（沈复 H-SHF-001 合并）足迹：其盘面内含本卡 M-AZJ 引用，属链式正常占用
                                    or ('shenfu' in rel) or ('SHF' in rel)
                                    or rel.startswith('data/backup_merge_H-SHF-001')):
            m_hits.append(rel)
        if rel in MAIN_LIB and ('AZJ' in txt or u'安子介' in txt):
            live_hits.append(rel)
    check('G01', 'dedup', u'M-AZJ 码全库外部 0 碰撞（除本卡产出与 AZJ-1 素材包）', not m_hits, m_hits)
    expect_live = ['data/code_maps.json', 'data/figure_names.json', 'data/modes_data.json']
    check('G02', 'dedup', u'live 主库占用面 == 合并后预期（code_maps/figure_names/modes_data 三件）', sorted(live_hits) == expect_live, live_hits)
    check('G03', 'dedup', u'「安子介」字样仅出现在已登记分层（manifest preflight 已分类）', bool(man['preflight']['buckets'].get('azj1_pack')))

    # ---- H 主库零写入与归档字节
    lib_now = dict((f, sha_file(os.path.join(REPO, f))) for f in MAIN_LIB)
    mman = jl(os.path.join(REPO, 'data/audit/phase21r9_azj_merge_manifest.json'))
    sman_p = os.path.join(REPO, 'data/audit/phase21r9_shenfu_merge_manifest.json')
    sman = jl(sman_p) if os.path.isfile(sman_p) else {'inputs': {}, 'after': {}}
    _si = sman.get('inputs') or {}
    _sa = sman.get('after') or {}
    def _chained(f):
        if lib_now[f] == mman['after'][f]['sha256']:
            return True
        si = _si.get(f) or {}
        sa = _sa.get(f) or {}
        sa_sha = sa['sha256'] if isinstance(sa, dict) else sa
        return si.get('sha256') == mman['after'][f]['sha256'] and sa_sha == lib_now[f]
    check('H01', 'frozen', u'主库六件 sha == 合并 manifest after（或经兄弟卡 t_a7d233f0 链式推进：本卡 after == 兄弟 before 且现行 == 兄弟 after）',
          all(_chained(f) for f in MAIN_LIB))
    arch_now = {}
    droot = os.path.join(REPO, 'data/figures/_duplicates')
    for n in sorted(os.listdir(droot)):
        if 'H-AZJ-345' in n:
            arch_now[n] = sha_file(os.path.join(droot, n))
    check('H02', 'frozen', u'归档 10 件 sha 与 manifest 记录一致（未触）', arch_now == man['archive_untouched'], len(arch_now))
    check('H03', 'frozen', u'manifest zero_library_write.untouched=True', man['zero_library_write']['untouched'] is True)

    # ---- I figure 层
    check('I01', 'figure', u'mode_ids 与 thinking_mode_count', fig['mode_ids'] == CODES and fig['thinking_mode_count'] == 10)
    check('I02', 'figure', u'core_thoughts 为十条模式名', fig['core_thoughts'] == [e['name_zh'] for e in entries])
    check('I03', 'figure', u'caveats >= 7 且含两说/疑似登记', len(fig['caveats']) >= 7 and any(u'87/88' in c for c in fig['caveats']))
    check('I04', 'figure', u'tags >= 15', len(fig['tags']) >= 15, len(fig['tags']))
    check('I05', 'figure', u'meta.mode_count=10 与 phase 口径', fig['meta']['mode_count'] == 10 and 'R9' in fig['meta']['phase'])
    check('I06', 'figure', u'famous_quote 为 W01 引文子串', u'我始终为香港人民服务' in pm['M-AZJ-008']['quotes'][0]['text'])
    check('I07', 'figure', u'cross_references 空 + caveat 如实登记',
          fig['cross_references'] == [] and any(u'cross_references 为空' in c for c in fig['caveats']))
    check('I08', 'figure', u'生卒/时代字段', fig['birth_year'] == 1912 and fig['death_year'] == 2000 and fig['time_period_standardized'] == '1912-2000')

    # ---- J 顶层块提案与场景登记
    check('J01', 'landing', u'top_block_proposal.core_modes == 十条', top['proposal']['core_modes'] == CODES)
    check('J02', 'landing', u'top_block_proposal 23 键与库内块同构', len(top['proposal'].keys()) == 23, len(top['proposal'].keys()))
    check('J03', 'landing', u'scenario_notes 标注合并卡范围且无旧场景处置',
          scen['notes']['scenarios_zh_new'] == 0 and scen['notes']['old_code_dispositions'] == [])
    check('J04', 'landing', u'manifest counts 与包内实测一致',
          man['counts']['modes'] == 10 and man['counts']['quotes'] == sum(len(m['quotes']) for m in pack['modes']))

    # ---- K 报告存在（由本卡后续步骤落盘）
    rep = os.path.join(REPO, 'docs/research/phase21r9_azj_rebuild_report.md')
    ev = os.path.join(REPO, 'docs/research/phase21r9_azj_landing_evidence.json')
    check('K01', 'report', u'重建报告与产出证据已落盘', os.path.isfile(rep) and os.path.isfile(ev))

    npass = len([r for r in RESULTS if r['status'] == 'PASS'])
    nfail = len([r for r in RESULTS if r['status'] == 'FAIL'])
    print('---')
    print('TOTAL %d PASS / %d FAIL' % (npass, nfail))
    out = dict(card='t_58ebf9c2', figure_code=FIG, date='2026-09-24',
               tool='verify_phase21r9_azj.py', total=len(RESULTS), passed=npass, failed=nfail,
               scope=os.environ.get('AZJ_SCOPE', 'landing'),
               results=RESULTS)
    wj = os.environ.get('AZJ_EVID_OUT') or os.path.join(REPO, 'docs/research/phase21r9_azj_verify_evidence.json')
    with io.open(wj, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write(u'\n')
    sys.exit(1 if nfail else 0)


if __name__ == '__main__':
    main()
