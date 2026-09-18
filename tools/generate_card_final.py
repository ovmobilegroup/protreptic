import json, random
from datetime import date

zh = json.load(open('/opt/data/workspace/Protreptic/tools/scenarios_zh.json'))
en = json.load(open('/opt/data/workspace/Protreptic/tools/scenarios_en.json'))
modes = json.load(open('/opt/data/workspace/Protreptic/tools/modes_data.json'))

# 1. 获取所有有完整数据的历史人物 H-* 代码
h_codes = [k for k in zh if k.startswith('H-')]
complete_h_codes = []
for k in h_codes:
    reason = zh[k].get('reason', '')
    case = zh[k].get('case', '')
    # Filter out placeholders: "待完善", "待完善...", "..."
    if (reason and case and 
        reason not in ['待完善', '待完善...', '...'] and
        case not in ['待完善', '待完善...', '...']):
        complete_h_codes.append(k)

print(f"Total H- codes: {len(h_codes)}")
print(f"Complete H- codes: {len(complete_h_codes)}")

# 2. 随机选择 1 位历史人物（仅从完整数据中选）
code = random.choice(complete_h_codes)
zh_entry = zh[code]
en_entry = en[code]

# 3. 选择最相关的现代场景 - 仅从 A/B/C/D 基础场景中选择
modern_codes = [k for k in zh if not k.startswith('H-') and (k.startswith('A-') or k.startswith('B-') or k.startswith('C-') or k.startswith('D-'))]
best_modern = max(modern_codes, key=lambda m: len(set(zh[m]['modes']) & set(zh_entry['modes'])))

# 4. 获取模式名称
zh_modes = modes['zh']
en_modes = modes['en']

hist_mode_names_zh = [zh_modes[str(m)][0] for m in zh_entry['modes']]
hist_mode_names_en = [en_modes[str(m)][0] for m in zh_entry['modes']]
modern_mode_names_zh = [zh_modes[str(m)][0] for m in zh[best_modern]['modes']]
modern_mode_names_en = [en_modes[str(m)][0] for m in zh[best_modern]['modes']]

today = date.today().isoformat()

card = f"""# 🧭 每日思维卡片 | {today}

## 🏛️ 历史人物：{zh_entry['name']} ({code})
> {en_entry['name']}

**核心贡献**：{zh_entry.get('reason', '')[:200]}...
**Core Contribution**: {en_entry.get('reason', '')[:200]}...

**思维模式组合** ({len(hist_mode_names_zh)} 种)：
{' · '.join(hist_mode_names_zh)}

---

## 💡 现代应用场景：{zh[best_modern]['name']} ({best_modern})
> {en[best_modern]['name']}

**适用情境**：{zh[best_modern].get('description', '')[:150]}...
**Applicable Context**: {en[best_modern].get('description', '')[:150]}...

**推荐思维模式**：
{' · '.join(modern_mode_names_zh)}

---

## 🔗 思维迁移指南

**历史洞见 → 现代实践**：
1. 从 {zh_entry['name'][:10]} 的核心算子提炼：{hist_mode_names_zh[0]} / {hist_mode_names_zh[1] if len(hist_mode_names_zh)>1 else ''}
2. 映射到 {zh[best_modern]['name'][:15]} 的关键决策点
3. 形成可执行行动清单

---

## 📖 经典案例回顾
{zh_entry.get('case', '')[:200]}...

> {en_entry.get('case', '')[:200]}...

---

*数据来源：Protreptic 知识体系 (269 位历史人物 × 42 思维模式)*
*工具：`python3 thinking_mode_selector.py -c {code}` 查看详情*
"""

print(card)