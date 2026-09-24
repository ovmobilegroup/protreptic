# -*- coding: utf-8 -*-
"""Phase21-R9 引文复跑脚本（卡片 t_d78053e7）
用法: python3 verify_quotes.py   （在 witness/ 目录内运行或任意 cwd，脚本自定位）
核验: 报告内全部 "> 「…」——…" 引文行 × 本目录全部见证副本（强归一：仅保留汉字/字母/数字）。
输出: 命中统计 + quote_verification_final.json
"""
import os, re, json, html as _html
HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.abspath(os.path.join(HERE, '..', '..', '..'))  # = <repo>/docs
MD = os.path.join(DOCS, 'research', 'phase21r9_shenfu_sourcing_report.md')
def norm(s): return re.sub(r'[^0-9A-Za-z\u3400-\u9fff\uF900-\uFAFF]', '', s)
def loadnorm(fp):
    t = open(fp, encoding='utf-8', errors='replace').read()
    if fp.endswith('.html'):
        t = t + '\n' + _html.unescape(re.sub(r'<[^>]+>', ' ', t))
    return norm(t)
W = {}
for fn in sorted(os.listdir(HERE)):
    if fn.endswith(('.txt', '.html')) and fn not in ('witness_sha256.txt',):
        W[fn] = loadnorm(os.path.join(HERE, fn))
md = open(MD, encoding='utf-8').read()
qre = re.compile(r'^\s*> 「(.+)」——(.+)$', re.M)
res = []; ok = 0
for i, m in enumerate(qre.finditer(md), 1):
    q, attr = m.group(1), m.group(2); nq = norm(q); hit = None
    for fn, t in W.items():
        p = t.find(nq)
        if p >= 0: hit = f'{fn}@{p}'; break
    if not hit and nq.startswith('芸'):
        for fn, t in W.items():
            p = t.find(nq[1:])
            if p >= 0: hit = f'{fn}@{p} (drop-)'; break
    if hit: ok += 1
    res.append({'n': i, 'text': q, 'attr': attr, 'found': hit})
print(f'QUOTES {ok}/{len(res)} OK')
for r in res:
    if not r['found']: print('FAIL:', r['n'], r['text'][:40])
json.dump(res, open(os.path.join(HERE, 'quote_verification_final.json'), 'w'), ensure_ascii=False, indent=1)
