#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Phase21-R9 安子介落盘产出证据生成器（卡 t_58ebf9c2）
# 输入：data/audit/phase21r9_azj_landing_manifest.json + AZJ-1 素材包
# 输出：docs/research/phase21r9_azj_landing_evidence.json
import io
import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MAN = os.path.join(REPO, 'data/audit/phase21r9_azj_landing_manifest.json')
PACK = os.path.join(REPO, 'docs/research/phase21r9_anzijie_sourcing_report.json')
OUT = os.path.join(REPO, 'docs/research/phase21r9_azj_landing_evidence.json')


def jl(p):
    return json.load(io.open(p, encoding='utf-8'))


man = jl(MAN)
pack = jl(PACK)
pm = dict((m['id'], m) for m in pack['modes'])

tier_table = [dict(mode_id=m['id'], pack_name=m['name'], tier=m['tier'], boundary=m['boundary']) for m in pack['modes']]
frag_by_source = {}
for rows in man['frag_register']:
    for d in rows:
        key = '|'.join(d['sources']) if d['sources'] else 'UNSOURCED'
        frag_by_source[key] = frag_by_source.get(key, 0) + 1

ev = {
    'card': 't_58ebf9c2',
    'figure_code': 'H-AZJ-001',
    'figure_name': u'安子介',
    'date': '2026-09-24',
    'baseline_commit': man['baseline_commit'],
    'method': u'Phase21-R9 重建落盘：以 AZJ-1 素材包逐条引文重锚（零库写、疑似不升级）',
    'pack': man['pack_sha256'],
    'deliverables': man['deliverables'],
    'counts': man['counts'],
    'preflight': man['preflight'],
    'quote_table': man['quote_table'],
    'frag_whitelist': [],
    'frag_register_counts': frag_by_source,
    'frag_register_total': sum(frag_by_source.values()),
    'tier_table': tier_table,
    'identity_anchors': {
        'name_zh': u'安子介',
        'name_en': 'Ann Tse Kai',
        'life': '1912-06-26 - 2000-06-03',
        'origin': u'浙江定海（生于上海）',
        'official_titles': u'杰出的社会活动家、著名爱国人士、香港知名实业家（W01/W02/W11）',
        'posts': u'第八、九届全国政协副主席；第六、七届全国政协常委；香港立法局/行政局非官守议员（1970—1978）；工业总会主席（1970—1975）；贸易发展局主席（1975—1979）（W02/W10）',
        'works': u'《间接成本之研究》1937；《国际贸易实务》1947；《陆沉》1938/1988；《解开汉字之谜》1982；《劈文切字集》1987；《安子介现代千字文》1991—1992；《汉字易学》1995（W01/W02/W03/W08/W10）',
        'patent': u'CN85101817.3A（1985-04-01 申请；1988-03-09 公开；授权 CN1003890B）五国专利（W04/W05/W01）',
        'award': u'安子介国际贸易研究奖（1991 设立，对外经济贸易大学承办）（W01/W02/W03）',
    },
    'open_items_reference': dict(pack='AZJ-1 素材包 §五', count=len(pack['open_items']), note=u'疑似与待核项保留在本档 pending/两说口径内，不得升级'),
    'merge_card_scope': [
        u'M-AZJ-001~010 入 data/modes_data.json（modes 列表 + 顶层块「H-AZJ-001」新增，随动 total）',
        u'figure 注册：data/code_maps.json / data/figure_names.json / tools/json 镜像与 DB（api/protreptic.db）',
        u'站链复跑（既定 5 步）与 parity 复测；发布仓镜像 + push + ls-remote 回执',
    ],
    'zero_library_write': man['zero_library_write'],
    'archive_untouched': man['archive_untouched'],
    'hard_fixes': man['hard_fixes'],
    'unrelated_mentions': u'本卡产出全部新写；工作树既有未跟踪件（tools/build_phase21r9_shenfu.py 等）属他链、未触',
}

with io.open(OUT, 'w', encoding='utf-8') as f:
    json.dump(ev, f, ensure_ascii=False, indent=1)
    f.write(u'\n')
print('WROTE', OUT, os.path.getsize(OUT))
