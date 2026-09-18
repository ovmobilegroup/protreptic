#!/usr/bin/env python3
"""清理人名脏值 —— Phase31-R4R5 (R4)。

定点替换, 不做 json 往返重写: data/modes_data.json 有 21 MB / 18 万行, json.dump
会重排格式并产生整文件 diff, 所以这里只在原文上做精确字符串替换, 每次替换都断言
预期命中数, 命中数不符即失败退出 —— 不猜、不静默跳过。幂等: 重复运行 = 0 处改动。

改前 -> 改后 (涉及的键/记录)
  data/modes_data.json      figure_code='HuoQuBing' 的 10 条模式 (M-HuoQuBing-001..010)
                            figure_name: '获取兵' -> '霍去病'   (10 处)
  data/figures/H-HuoQuBing-001.json
                            figure_name: '获取兵' -> '霍去病'   (1 处)
  data/figure_names.json    'H-HuoQuBing-001' / 'H-HUOQUBING-001'
                            '获取兵' -> '霍去病'                (2 处)

依据 (全部取自既有源数据原文, 未臆造任何人名)
  * 同一记录 data/figures/H-HuoQuBing-001.json 里 figure_pinyin = "Huo Qubing",
    historical_significance 原文起句「霍去病（前140—前117），字少傅将軍將，西汉代伟大的
    騎都尉…」—— 原文直书。
  * 该 10 条模式的 definition_zh 原文都写「霍去病」(如 M-HuoQuBing-001:「霍去病18岁时率
    800 轻骑兵深入匈奴腹地，单骑入阵…」)—— 原文直书。
  * data/figure_names.json 里同一人物的 code 'HuoQuBing' / 'HUOQUBING' 本来就是
    「霍去病」; 脏值只出现在没有任何 code 引用的 H- 前缀别名键上 (H-HuoQuBing-001 /
    H-HUOQUBING-001), 属于别名表遗留。
  * 「获取兵」是拼音 HuoQubing 的机器转写产物(音近字拼凑), 不是任何历史人名。

不改 (附理由)
  data/figure_names.json 'H-FEI-001' = '非人': 该记录复核为「概念主题簇」保留, 证据见
    tools/_quarantine.py 的 ADJUDICATED; '非人' 是记录自述的主题名, 不是脏值。
  data/figure_names.json 'H-SX-001' = '苏咸': 源数据按隔离规则原样保留, 公开产出层由
    tools/_quarantine.py 的 QUARANTINE 过滤。

用法: python3 tools/fix_dirty_figure_names.py
退出码: 0 成功(含幂等无改动); 1 命中数与预期不符(源数据已变, 需要人工确认)。
"""

from __future__ import annotations

import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRTY = "获取兵"
CLEAN = "霍去病"

# (文件, 预期替换次数, 说明)
TARGETS = [
    ("data/modes_data.json", 10, "figure_code='HuoQuBing' 的 10 条模式 figure_name"),
    ("data/figures/H-HuoQuBing-001.json", 1, "人物档案 figure_name"),
    ("data/figure_names.json", 2, "别名键 H-HuoQuBing-001 / H-HUOQUBING-001"),
]

OLD = '"figure_name": "%s"' % DIRTY
NEW = '"figure_name": "%s"' % CLEAN


def main() -> int:
    total_before, total_after, changed = 0, 0, []
    for rel, expect, what in TARGETS:
        path = os.path.join(REPO, rel)
        if not os.path.isfile(path):
            sys.exit("[fix-names] 缺少 %s" % path)
        text = open(path, encoding="utf-8").read()
        total_before += text.count(DIRTY)
        n = text.count(OLD)
        if rel.endswith("figure_names.json"):
            n = sum(text.count('"%s": "%s"' % (k, DIRTY)) for k in ("H-HuoQuBing-001", "H-HUOQUBING-001"))
        if n not in (0, expect):
            sys.exit("[fix-names] %s: 「%s」命中 %d 处, 预期 %d —— 源数据已变, 请人工确认后再改"
                     % (rel, DIRTY, n, expect))
        if n:
            if rel.endswith("figure_names.json"):
                for k in ("H-HuoQuBing-001", "H-HUOQUBING-001"):
                    text = text.replace('"%s": "%s"' % (k, DIRTY), '"%s": "%s"' % (k, CLEAN))
            else:
                text = text.replace(OLD, NEW)
            open(path, "w", encoding="utf-8").write(text)
        total_after += text.count(DIRTY)
        changed.append((rel, n, expect, what))
        print("  %-42s 命中 %d/%d  %s" % (rel, n, expect, what))

    print("")
    print("  「%s」总数: 改前 %d -> 改后 %d" % (DIRTY, total_before, total_after))
    if total_after:
        print("  [FAIL] 仍有残留, 请检查其它数据源"); return 1
    if total_before == 0:
        print("  (幂等: 全部已是「%s」, 无需改动)" % CLEAN)
    return 0


if __name__ == "__main__":
    print("[fix-names] 清理人名脏值 Phase31-R4R5")
    sys.exit(main())
