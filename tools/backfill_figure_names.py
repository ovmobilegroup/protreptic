#!/usr/bin/env python3
"""回填 11 个缺失 figure_name 的人物（证据见 references/name-backfill-2026-09.md）。

只改 `modes` 列表里对应 figure_code 且 figure_name 缺失/为空的模式；
写入格式与源文件一致（indent=1, ensure_ascii=False）。
"""
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(REPO, 'data', 'modes_data.json')

NAMES = {
    'ARR': '阿伦尼乌斯',
    'VOL': '伏打',
    'GIB': '吉布斯',
    'CAI': '蔡文姬',
    'QIU': '秋瑾',
    'ZKU': '朱可夫',
    'LIN': '林彪',
    'TDL': '李政道',
    'TIN': '丁肇中',
    'LAN': '朗道',
    'ZuXuan': '祖暅',
}


def _empty(v):
    if v is None:
        return True
    if isinstance(v, list):
        return not any(str(x).strip() for x in v)
    return not str(v).strip()


def main():
    d = json.load(open(PATH, encoding='utf-8'))
    modes = d.get('modes', [])
    filled = {}
    for m in modes:
        fc = str(m.get('figure_code') or '')
        if fc in NAMES and _empty(m.get('figure_name')):
            m['figure_name'] = NAMES[fc]
            filled[fc] = filled.get(fc, 0) + 1

    missing = [c for c in NAMES if c not in filled]
    print('回填统计:', {k: filled[k] for k in NAMES if k in filled})
    if missing:
        print('[warn] 未回填（可能已有名字或不匹配）:', missing, file=sys.stderr)

    with open(PATH, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    print(f'✅ 写入 {PATH}  ({os.path.getsize(PATH)} bytes)')

    # 复核
    d2 = json.load(open(PATH, encoding='utf-8'))
    left = sorted({str(m.get('figure_code')) for m in d2['modes']
                   if _empty(m.get('figure_name'))})
    print('仍无名的 figure_code:', left)


if __name__ == '__main__':
    main()
