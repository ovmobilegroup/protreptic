#!/usr/bin/env python3
"""
Protreptic Daily Thinking Card Generator

Generates a bilingual (Chinese/English) daily thinking mode card
for Matrix push at 8 AM. Pairs 1 historical figure (H-*) with
1 modern scenario (A-D) based on thinking mode overlap.

Cron usage:
    0 8 * * * cd /opt/data/workspace/Protreptic && python3 tools/generate_card.py
"""

import json
import os
import random
import sys
from datetime import date
from pathlib import Path


def load_data():
    """Load all data sources."""
    # Load figures from individual JSON files
    figures_dir = Path('/opt/data/workspace/Protreptic/data/figures')
    h_files = [f for f in os.listdir(figures_dir) 
               if f.startswith('H-') and f.endswith('.json') and not f.endswith('_modes.json')]
    
    figures = {}
    for f in sorted(h_files):
        path = figures_dir / f
        try:
            with open(path, 'r', encoding='utf-8') as fp:
                data = json.load(fp)
            
            name_zh = data.get('figure_name_zh', data.get('figure_name', data.get('name', 'N/A')))
            name_en = data.get('figure_name_en', data.get('figure_name', 'See reference'))
            code = data.get('code', data.get('figure_code', f.replace('.json', '')))
            
            # Load modes
            modes_path = path.with_name(path.stem + '_modes.json')
            modes_list = []
            if modes_path.exists():
                with open(modes_path, 'r', encoding='utf-8') as mp:
                    modes_data = json.load(mp)
                modes_list = modes_data.get('modes', [])
            
            # Extract case and reason from first mode
            case_zh = ''
            reason_zh = ''
            case_en = ''
            for m in modes_list[:3]:
                cases_zh = m.get('representative_cases_zh', '')
                if isinstance(cases_zh, list) and cases_zh:
                    case_zh = cases_zh[0]
                elif isinstance(cases_zh, str) and cases_zh:
                    case_zh = cases_zh
                
                if m.get('definition_zh'):
                    reason_zh = m['definition_zh'][:250]
                
                cases_en = m.get('representative_cases_en', '')
                if isinstance(cases_en, list) and cases_en:
                    case_en = cases_en[0]
            
            # Get mode IDs (numeric)
            mode_ids = set()
            for m in modes_list:
                mode_code = m.get('mode_code', m.get('id', ''))
                if '-' in mode_code:
                    parts = mode_code.split('-')
                    if len(parts) >= 3:
                        try:
                            num = int(parts[-1])
                            mode_ids.add(num)
                        except:
                            pass
            
            figures[code] = {
                'name_zh': name_zh,
                'name_en': name_en,
                'modes': list(mode_ids),
                'reason': reason_zh,
                'case': case_zh,
                'case_en': case_en,
                'modes_list': modes_list,
                'mode_count': len(modes_list)
            }
        except Exception as e:
            print(f"Error loading {f}: {e}", file=sys.stderr)
            continue
    
    # Load modern scenarios
    scenarios_zh_path = Path('/opt/data/workspace/Protreptic/release/v2.0.0/protreptic-core/scenarios_zh.json')
    scenarios_en_path = Path('/opt/data/workspace/Protreptic/release/v2.0.0/protreptic-core/scenarios_en.json')
    
    with open(scenarios_zh_path, 'r', encoding='utf-8') as f:
        zh_scenarios = json.load(f)
    with open(scenarios_en_path, 'r', encoding='utf-8') as f:
        en_scenarios = json.load(f)
    
    # Load modes data
    modes_path = Path('/opt/data/workspace/Protreptic/tools/modes_data.json')
    with open(modes_path, 'r', encoding='utf-8') as f:
        modes_data = json.load(f)
    
    return figures, zh_scenarios, en_scenarios, modes_data


def is_complete_entry(v):
    """Check if entry has real content (not placeholder) for reason and case."""
    reason = v.get('reason', '')
    case = v.get('case', '')
    placeholders = ['待完善', '待完善...', '...', '']
    return (reason and case and 
            reason not in placeholders and 
            case not in placeholders and
            len(reason) > 50 and len(case) > 20)


def get_mode_names(mode_ids, zh_modes, max_count=5):
    """Get mode names from mode IDs."""
    names = []
    for mid in sorted(mode_ids)[:max_count]:
        if str(mid) in zh_modes:
            names.append(zh_modes[str(mid)][0])
        else:
            names.append(f'M{mid}')
    return names


def main():
    # Load data
    figures, zh_scenarios, en_scenarios, modes_data = load_data()
    zh_modes = modes_data.get('zh', {})
    en_modes = modes_data.get('en', {})
    
    # Filter to complete entries only
    complete_codes = [k for k, v in figures.items() if is_complete_entry(v)]
    print(f"Available complete historical figures: {len(complete_codes)}", file=sys.stderr)
    
    # Modern scenarios: A/B/C/D-*P patterns
    modern_codes = [k for k in zh_scenarios.keys() 
                    if any(k.startswith(p) for p in ['A-', 'B-', 'C-', 'D-']) 
                    and k.endswith('-P')
                    and 'modes' in zh_scenarios[k]]
    
    if not complete_codes or not modern_codes:
        print("Error: No valid figures or modern scenarios found!", file=sys.stderr)
        sys.exit(1)
    
    # Deterministic daily seed
    random.seed(date.today().toordinal())
    
    # Pick historical figure
    code = random.choice(complete_codes)
    fig_entry = figures[code]
    
    # Match to best modern scenario by mode overlap
    best_modern = max(
        modern_codes,
        key=lambda m: len(set(fig_entry['modes']) & set(zh_scenarios[m].get('modes', [])))
    )
    
    # Get mode names - use the mode codes from the figure's modes list
    fig_mode_names = []
    for m_code in fig_entry.get('modes_list', []):
        mode_name_zh = m_code.get('name_zh', m_code.get('mode_code', 'N/A'))
        fig_mode_names.append(mode_name_zh)
        if len(fig_mode_names) >= 5:
            break
    if not fig_mode_names and fig_entry['modes']:
        fig_mode_names = [zh_modes.get(str(m), ['', ''])[0] for m in sorted(fig_entry['modes'])[:5]]
    
    sc_mode_ids = zh_scenarios[best_modern].get('modes', [])
    sc_mode_names = get_mode_names(sc_mode_ids, zh_modes, 5)
    
    # Truncated fields
    reason_zh = fig_entry['reason'][:200] + '...' if len(fig_entry['reason']) > 200 else fig_entry['reason']
    case_zh = fig_entry['case'][:250] + '...' if len(fig_entry['case']) > 250 else fig_entry['case']
    case_en = fig_entry['case_en'][:250] + '...' if len(fig_entry['case_en']) > 250 else fig_entry['case_en']
    
    # Names
    zh_name = fig_entry['name_zh']
    
    # Clean name (remove trailing descriptions)
    def clean_name(name):
        if '：' in name:
            return name.split('：')[0].strip()
        if ':' in name:
            return name.split(':')[0].strip()
        return name.strip()
    
    zh_name_clean = clean_name(zh_name)
    
    today = date.today().isoformat()
    
    # Scenario names
    modern_name_zh = zh_scenarios[best_modern].get('name', 'N/A')
    modern_name_en = en_scenarios[best_modern].get('name', 'N/A')
    modern_desc_zh = zh_scenarios[best_modern].get('description', 'N/A')[:150] + '...'
    modern_desc_en = en_scenarios[best_modern].get('description', 'N/A')[:150] + '...'
    
    # Core modes (first two from the figure's mode list)
    fig_mode_names_for_core = [m.get('name_zh', m.get('mode_code', '')) for m in fig_entry.get('modes_list', [])[:2]]
    core_mode_1 = fig_mode_names_for_core[0] if fig_mode_names_for_core else ''
    core_mode_2 = fig_mode_names_for_core[1] if len(fig_mode_names_for_core) > 1 else ''
    
    # Render card
    en_name = fig_entry.get('name_en', 'See reference')
    card = f"""# 🧭 每日思维卡片 | {today}

## 🏛️ 历史人物：{zh_name_clean} ({code})
> {en_name}

**核心贡献**：{reason_zh}
**Core Contribution**: {fig_mode_names[0] if fig_mode_names else 'N/A'}

**思维模式组合** ({len(fig_mode_names)} 种)：
{' · '.join(fig_mode_names)}

---

## 💡 现代应用场景：{modern_name_zh} ({best_modern})
> {modern_name_en}

**适用情境**：{modern_desc_zh}
**Applicable Context**: {modern_desc_en}

**推荐思维模式**：
{' · '.join(sc_mode_names)}

---

## 🔗 思维迁移指南

**历史洞见 → 现代实践**：
1. 从 {zh_name_clean[:10]} 的核心算子提炼：{core_mode_1} / {core_mode_2}
2. 映射到 {modern_name_zh[:15]} 的关键决策点
3. 形成可执行行动清单

---

## 📖 经典案例回顾
{case_zh}

> {case_en}

---

*数据来源：Protreptic 知识体系 (269 位历史人物 × 42 思维模式)*
*工具：`python3 thinking_mode_selector.py -c {code}` 查看详情*
"""
    
    print(card)


if __name__ == '__main__':
    main()
