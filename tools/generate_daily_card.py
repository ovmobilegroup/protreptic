import json, random
from datetime import date
from pathlib import Path

# 1. 加载数据
zh = json.load(open('/opt/data/workspace/Protreptic/tools/scenarios_zh.json'))
en = json.load(open('/opt/data/workspace/Protreptic/tools/scenarios_en.json'))
modes = json.load(open('/opt/data/workspace/Protreptic/tools/modes_data.json'))

# 2. 获取所有历史人物 H-* 代码
h_codes = [k for k in zh if k.startswith('H-')]

# 3. 随机选择 1 位历史人物
random.seed(date.today().toordinal())  # 确保每天固定随机
code = random.choice(h_codes)
zh_entry = zh[code]
en_entry = en.get(code, {})

# 4. 选择最相关的现代场景（基于模式重叠度）
modern_codes = [k for k in zh if not k.startswith('H-') and 'modes' in zh[k] and isinstance(zh[k]['modes'], list)]
best_modern = max(modern_codes, key=lambda m: len(set(zh[m]['modes']) & set(zh_entry['modes'])))

# 5. 获取模式名称
zh_modes = modes['zh']
en_modes = modes['en']
mode_names_zh = [zh_modes[str(m)][0] for m in zh_entry['modes']]
modern_mode_names_zh = [zh_modes[str(m)][0] for m in zh[best_modern]['modes']]

# 6. 生成卡片 Markdown
today = date.today().isoformat()

reason_zh = zh_entry.get('reason', '')
reason_en = en_entry.get('reason', '')
case_zh = zh_entry.get('case', '')
case_en = en_entry.get('case', '')
desc_zh = zh[best_modern].get('description', '')
desc_en = en[best_modern].get('description', '')

card = f"""# 🧭 每日思维卡片 | {today}

## 🏛️ 历史人物：{zh_entry['name']} ({code})
> {en_entry.get('name', '')}

**核心贡献**：{reason_zh[:200]}...
**Core Contribution**: {reason_en[:200]}...

**思维模式组合** ({len(mode_names_zh)} 种)：
{' · '.join(mode_names_zh)}

---

## 💡 现代应用场景：{zh[best_modern]['name']} ({best_modern})
> {en[best_modern]['name']}

**适用情境**：{desc_zh[:150]}...
**Applicable Context**: {desc_en[:150]}...

**推荐思维模式**：
{' · '.join(modern_mode_names_zh)}

---

## 🔗 思维迁移指南

**历史洞见 → 现代实践**：
1. 从 {zh_entry['name'][:10]} 的核心算子提炼：{zh_modes[str(zh_entry['modes'][0])][0]} / {zh_modes[str(zh_entry['modes'][1])][0] if len(zh_entry['modes'])>1 else ''}
2. 映射到 {zh[best_modern]['name'][:15]} 的关键决策点
3. 形成可执行行动清单

---

## 📖 经典案例回顾
{case_zh[:200]}...

> {case_en[:200]}...

---

*数据来源：Protreptic 知识体系 (269 位历史人物 × 42 思维模式)*
*工具：`python3 thinking_mode_selector.py -c {code}` 查看详情*
"""

print(card)