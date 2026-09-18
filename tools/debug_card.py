import json
from datetime import date
import random

# 1. 加载数据
zh = json.load(open('/opt/data/workspace/Protreptic/tools/scenarios_zh.json'))
en = json.load(open('/opt/data/workspace/Protreptic/tools/scenarios_en.json'))
modes = json.load(open('/opt/data/workspace/Protreptic/tools/modes_data.json'))

zh_modes = modes['zh']
en_modes = modes['en']

# Filter: only keep entries that are dicts with 'modes' key
def is_figure_entry(k, v):
    return isinstance(v, dict) and 'modes' in v and isinstance(v['modes'], list)

# 2. 获取所有历史人物 H-* 代码
h_codes = [k for k, v in zh.items() if k.startswith('H-') and is_figure_entry(k, v)]
print(f"Historical figures: {len(h_codes)}")

# 3. 随机选择 1 位历史人物
random.seed(date.today().toordinal())
code = random.choice(h_codes)
zh_entry = zh[code]
en_entry = en.get(code, {})

print(f"Selected: {code} - {zh_entry.get('name', zh_entry.get('name_zh', 'NO NAME'))}")

# 4. 选择最相关的现代场景（基于模式重叠度） - 只使用基础 20 个场景 A-1-X-P 到 D-3-Z-P
basic_modern_codes = ['A-1-X-P', 'A-1-X-R', 'A-1-Y-P', 'A-1-Y-S', 'A-1-Y-Q', 
                       'A-2-X-P', 'A-2-Y-P', 'A-2-Y-R', 'A-3-Y-R',
                       'B-2-Y-S', 'B-1-Z-S', 'C-2-Y-P', 'C-2-Z-P', 'C-3-Y-S',
                       'D-1-Y-R', 'D-2-Y-R', 'D-3-Z-P', 'B-1-Y-S', 'C-1-Y-P', 'D-2-Z-P']

modern_codes = [k for k in basic_modern_codes if k in zh and is_figure_entry(k, zh[k])]
print(f"Basic modern scenarios: {len(modern_codes)}")

if modern_codes:
    best_modern = max(modern_codes, key=lambda m: len(set(zh[m]['modes']) & set(zh_entry['modes'])))
    print(f"Best modern: {best_modern} - {zh[best_modern].get('name', zh[best_modern].get('name_zh', 'NO NAME'))}")
    
    # 5. 获取模式名称
    mode_names_zh = [zh_modes[str(m)][0] for m in zh_entry['modes']]
    modern_mode_names_zh = [zh_modes[str(m)][0] for m in zh[best_modern]['modes']]
    
    # 6. 截断长文本
    reason_zh = zh_entry.get('reason', zh_entry.get('reason_zh', ''))
    reason_en = en_entry.get('reason', en_entry.get('reason_en', ''))
    reason_zh_short = (reason_zh[:180] + '...') if len(reason_zh) > 180 else reason_zh
    reason_en_short = (reason_en[:180] + '...') if len(reason_en) > 180 else reason_en
    
    modern_desc_zh = zh[best_modern].get('description', zh[best_modern].get('description_zh', ''))
    modern_desc_en = en[best_modern].get('description', en[best_modern].get('description_en', ''))
    modern_desc_zh_short = (modern_desc_zh[:150] + '...') if len(modern_desc_zh) > 150 else modern_desc_zh
    modern_desc_en_short = (modern_desc_en[:150] + '...') if len(modern_desc_en) > 150 else modern_desc_en
    
    case_zh = zh_entry.get('case', zh_entry.get('case_zh', ''))
    case_en = en_entry.get('case', en_entry.get('case_en', ''))
    case_zh_short = (case_zh[:200] + '...') if len(case_zh) > 200 else case_zh
    case_en_short = (case_en[:200] + '...') if len(case_en) > 200 else case_en
    
    # 核心模式前两个
    core_modes = zh_entry['modes']
    core_mode_1 = zh_modes[str(core_modes[0])][0] if core_modes else ''
    core_mode_2 = zh_modes[str(core_modes[1])][0] if len(core_modes) > 1 else ''
    
    today = date.today().isoformat()
    
    # 7. 生成卡片 Markdown
    zh_name = zh_entry.get('name', zh_entry.get('name_zh', ''))
    en_name = en_entry.get('name', en_entry.get('name_en', ''))
    modern_name_zh = zh[best_modern].get('name', zh[best_modern].get('name_zh', ''))
    modern_name_en = en[best_modern].get('name', en[best_modern].get('name_en', ''))
    
    card = f"""# 🧭 每日思维卡片 | {today}

## 🏛️ 历史人物：{zh_name} ({code})
> {en_name}

**核心贡献**：{reason_zh_short}
**Core Contribution**: {reason_en_short}

**思维模式组合** ({len(mode_names_zh)} 种)：
{' · '.join(mode_names_zh)}

---

## 💡 现代应用场景：{modern_name_zh} ({best_modern})
> {modern_name_en}

**适用情境**：{modern_desc_zh_short}
**Applicable Context**: {modern_desc_en_short}

**推荐思维模式**：
{' · '.join(modern_mode_names_zh)}

---

## 🔗 思维迁移指南

**历史洞见 → 现代实践**：
1. 从 {zh_name[:10]} 的核心算子提炼：{core_mode_1} / {core_mode_2}
2. 映射到 {modern_name_zh[:15]} 的关键决策点
3. 形成可执行行动清单

---

## 📖 经典案例回顾
{case_zh_short}

> {case_en_short}

---

*数据来源：Protreptic 知识体系 (269 位历史人物 × 42 思维模式)*
*工具：`python3 thinking_mode_selector.py -c {code}` 查看详情"""
    
    print(card)