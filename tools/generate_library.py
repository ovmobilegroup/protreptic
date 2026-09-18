#!/usr/bin/env python3
"""
Generate historical figures thinking modes library document (Markdown).
"""
import json
from collections import defaultdict

# Load data
with open('/opt/data/workspace/Protreptic/tools/scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)
with open('/opt/data/workspace/Protreptic/tools/scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)
with open('/opt/data/workspace/Protreptic/tools/modes_data.json', 'r', encoding='utf-8') as f:
    modes = json.load(f)
with open('/opt/data/workspace/Protreptic/tools/code_maps.json', 'r', encoding='utf-8') as f:
    cm = json.load(f)

zh_modes = modes['zh']
en_modes = modes['en']

# Get all codes by category
h_codes = sorted([k for k in zh if k.startswith('H-')])
m_codes = sorted([k for k in zh if k.startswith('M-')])
p4_codes = sorted([k for k in zh if k.startswith('P4-')])
p5_codes = sorted([k for k in zh if k.startswith('P5-')])
intl_codes = sorted([k for k in zh if k.startswith(('EU-', 'UK-', 'US-', 'RU-', 'JP-', 'KR-', 'BR-'))])
base_codes = sorted([k for k in zh if k.startswith(('A-', 'B-', 'C-', 'D-'))])

# Historical + P4 + P5 for main library
all_codes = h_codes + m_codes + p4_codes + p5_codes + intl_codes

# Mode name mapping
mode_names_zh = {mid: data[0] for mid, data in zh_modes.items()}
mode_names_en = {mid: data[0] for mid, data in en_modes.items()}

# Helper to get field from entry (supports both standard and i18n formats)
def get_field(entry, field, lang='zh'):
    if field in entry:
        return entry[field]
    i18n_field = f"{field}_{lang}"
    if i18n_field in entry:
        return entry[i18n_field]
    # For KR/BR format
    alt_map = {
        'name': ['name_zh', 'name_en', 'name'],
        'description': ['description_zh', 'description_en', 'description', 'core_mode'],
        'reason': ['reason_zh', 'reason_en', 'reason', 'mode'],
        'steps': ['steps_zh', 'steps_en', 'steps'],
        'expected': ['expected_zh', 'expected_en', 'expected'],
        'case': ['case_zh', 'case_en', 'case'],
    }
    for alt in alt_map.get(field, []):
        if alt in entry:
            return entry[alt]
    return ""

# Domain mapping (1-145)
MODE_DOMAINS = {
    '1': 'Strategic', '2': 'Strategic', '3': 'Strategic', '4': 'Strategic',
    '5': 'Analytical', '6': 'Collaborative', '7': 'Strategic', '8': 'Operational',
    '9': 'Operational', '10': 'Collaborative', '11': 'Operational', '12': 'Systems',
    '13': 'Strategic', '14': 'Strategic', '15': 'Strategic', '16': 'Strategic',
    '17': 'Analytical', '18': 'Collaborative', '19': 'Analytical', '20': 'Analytical',
    '21': 'Personal', '22': 'Systems', '23': 'Creative', '24': 'Analytical',
    '25': 'Analytical', '26': 'Personal', '27': 'Systems', '28': 'Operational',
    '29': 'Analytical', '30': 'Analytical', '31': 'Systems', '32': 'Systems',
    '33': 'Strategic', '34': 'Systems', '35': 'Operational', '36': 'Personal',
    '37': 'Personal', '38': 'Operational', '39': 'Strategic', '40': 'Operational',
    '41': 'Operational', '42': 'Personal',
    '43': 'Systems', '44': 'Analytical', '45': 'Collaborative', '46': 'Strategic',
    '47': 'Collaborative', '48': 'Systems', '49': 'Strategic', '50': 'Collaborative',
    '51': 'Systems', '52': 'Strategic', '53': 'Collaborative', '54': 'Systems',
    '55': 'Creative', '56': 'Analytical', '57': 'Operational', '58': 'Analytical',
    '59': 'Analytical', '60': 'Collaborative', '61': 'Operational', '62': 'Creative',
    '63': 'Systems', '64': 'Systems', '65': 'Analytical', '66': 'Strategic',
    '67': 'Strategic', '68': 'Strategic', '69': 'Strategic', '70': 'Operational',
    '71': 'Operational', '72': 'Operational', '73': 'Collaborative', '74': 'Operational',
    '75': 'Collaborative', '76': 'Collaborative', '77': 'Analytical', '78': 'Analytical',
    '79': 'Analytical', '80': 'Analytical', '81': 'Operational', '82': 'Strategic',
    '83': 'Collaborative', '84': 'Analytical', '85': 'Creative', '86': 'Operational',
    '87': 'Strategic', '88': 'Analytical', '89': 'Creative', '90': 'Operational',
    '91': 'Creative', '92': 'Strategic', '93': 'Collaborative', '94': 'Analytical',
    '95': 'Creative', '96': 'Operational', '97': 'Strategic', '98': 'Collaborative',
    '99': 'Analytical', '100': 'Creative', '101': 'Operational', '102': 'Strategic',
    '103': 'Collaborative', '104': 'Analytical', '105': 'Creative', '106': 'Operational',
    '107': 'Strategic', '108': 'Collaborative', '109': 'Analytical', '110': 'Creative',
    '111': 'Operational', '112': 'Strategic', '113': 'Collaborative', '114': 'Analytical',
    '115': 'Creative', '116': 'Operational', '117': 'Strategic', '118': 'Collaborative',
    '119': 'Analytical', '120': 'Creative', '121': 'Operational',
    '122': 'Systems', '123': 'Analytical', '124': 'Creative', '125': 'Systems',
    '126': 'Systems', '127': 'Operational', '128': 'Systems', '129': 'Operational',
    '130': 'Systems', '131': 'Operational', '132': 'Systems', '133': 'Systems',
    '134': 'Systems', '135': 'Systems', '136': 'Collaborative', '137': 'Systems',
    '138': 'Collaborative', '139': 'Operational', '140': 'Collaborative',
    '141': 'Collaborative', '142': 'Operational', '143': 'Personal',
    '144': 'Systems', '145': 'Systems',
}

# Group by domain
domain_groups = defaultdict(list)
for code in all_codes:
    entry = zh[code]
    mode_ids = entry['modes']
    domains = set(MODE_DOMAINS[str(m)] for m in mode_ids)
    primary_domain = sorted(domains)[0] if domains else 'Other'
    domain_groups[primary_domain].append(code)

# Generate markdown
lines = []
lines.append("# 历史人物思维模式完整档案库")
lines.append("")
lines.append(f"**生成时间**: 2026-08-02  ")
lines.append(f"**历史人物 (H-/M-)**: {len(h_codes) + len(m_codes)} 位  ")
lines.append(f"**P4 专题人物**: {len(p4_codes)} 位  ")
lines.append(f"**P5 精准补位**: {len(p5_codes)} 位  ")
lines.append(f"**国际人物**: {len(intl_codes)} 位 (7国)  ")
lines.append(f"**基础场景 (A/B/C/D)**: {len(base_codes)} 位  ")
lines.append(f"**思维模式总数**: 145 种  ")
lines.append(f"**中英双语**: 100% 对齐  ")
lines.append("")
lines.append("---")
lines.append("")

# Summary statistics
lines.append("## 📊 总体统计")
lines.append("")
lines.append("| 维度 | 数量 | 说明 |")
lines.append("|------|------|------|")
lines.append(f"| 历史人物 (H-/M-) | {len(h_codes) + len(m_codes)} | 涵盖先秦至现代 |")
lines.append(f"| P4 专题人物 | {len(p4_codes)} | TECH/WOMEN/ETHNIC/MED/COMP/ENG |")
lines.append(f"| P5 精准补位 | {len(p5_codes)} | TRANS/EDU/IND/SCI/ETH/ACAD |")
lines.append(f"| 国际人物 | {len(intl_codes)} | 德/英/美/俄/日/韩/巴 7国 |")
lines.append(f"| 基础场景 | {len(base_codes)} | A/B/C/D 方向/突破/人/长期 |")
lines.append(f"| 总人物数 | {len(all_codes) + len(base_codes)} |  |")
lines.append(f"| 思维模式 | 145 | ID 1-145，中英双语 |")
lines.append(f"| 总场景数 | {len(zh)} | 501 场景 |")
lines.append("")

# Domain distribution
lines.append("### 领域分布")
lines.append("")
lines.append("| 领域 | 人数 | 核心代表人物 |")
lines.append("|------|------|--------------|")
domain_order = ['Strategic', 'Analytical', 'Collaborative', 'Operational', 'Systems', 'Creative', 'Personal']
for domain in domain_order:
    codes = domain_groups.get(domain, [])
    if codes:
        # Get top 3 representative figures
        reps = []
        for c in codes[:3]:
            name = zh[c]['name'].split('：')[0] if '：' in zh[c]['name'] else zh[c]['name'][:15]
            reps.append(name)
        lines.append(f"| {domain} | {len(codes)} | {', '.join(reps)}... |")
lines.append("")

# Country distribution for international
lines.append("### 国际人物国家分布")
lines.append("")
intl_countries = defaultdict(list)
for code in intl_codes:
    prefix = code.split('-')[0] + '-'
    if prefix == 'EU-':
        prefix = 'EU-DE-'
    country = prefix.rstrip('-')
    intl_countries[country].append(code)

country_names = {
    'EU-DE': '德国',
    'UK': '英国',
    'US': '美国',
    'RU': '俄罗斯',
    'JP': '日本',
    'KR': '韩国',
    'BR': '巴西',
}
for country, codes in sorted(intl_countries.items()):
    reps = []
    for c in codes[:2]:
        name = get_field(zh[c], 'name', 'zh').split('：')[0] if '：' in get_field(zh[c], 'name', 'zh') else get_field(zh[c], 'name', 'zh')[:15]
        reps.append(name)
    lines.append(f"- **{country_names.get(country, country)} ({country})**: {len(codes)} 位 ({', '.join(reps)}...)")
lines.append("")

# Detailed figures by domain
lines.append("---")
lines.append("")
lines.append("## 📚 详细档案（按思维领域分组）")
lines.append("")

for domain in domain_order:
    codes = domain_groups.get(domain, [])
    if not codes:
        continue
    lines.append(f"### {domain} 领域 ({len(codes)} 位)")
    lines.append("")
    
    for code in codes:
        zh_entry = zh[code]
        en_entry = en[code]
        
        name_zh = get_field(zh_entry, 'name', 'zh')
        name_en = get_field(en_entry, 'name', 'en')
        desc_zh = get_field(zh_entry, 'description', 'zh')
        desc_en = get_field(en_entry, 'description', 'en')
        mode_ids = zh_entry['modes']
        reason_zh = get_field(zh_entry, 'reason', 'zh')
        reason_en = get_field(en_entry, 'reason', 'en')
        steps_zh = get_field(zh_entry, 'steps', 'zh')
        steps_en = get_field(en_entry, 'steps', 'en')
        expected_zh = get_field(zh_entry, 'expected', 'zh')
        expected_en = get_field(en_entry, 'expected', 'en')
        case_zh = get_field(zh_entry, 'case', 'zh')
        case_en = get_field(en_entry, 'case', 'en')
        
        mode_names = [f"{mid}: {mode_names_zh.get(str(mid), 'Unknown')}" for mid in mode_ids]
        
        lines.append(f"#### {code}: {name_zh}")
        lines.append(f"*English: {name_en}*  ")
        lines.append("")
        lines.append(f"**核心思维模式**: {', '.join(mode_names)}  ")
        lines.append("")
        lines.append(f"**中文描述**: {desc_zh}  ")
        lines.append(f"**English Description**: {desc_en}  ")
        lines.append("")
        
        if reason_zh:
            lines.append(f"**核心贡献 (中文)**: {reason_zh}  ")
            lines.append(f"**Core Contribution (English)**: {reason_en}  ")
            lines.append("")
        
        if steps_zh:
            lines.append("**执行步骤 (中文)**:")
            for i, step in enumerate(steps_zh, 1):
                lines.append(f"{i}. {step}")
            lines.append("")
        
        if steps_en:
            lines.append("**Execution Steps (English)**:")
            for i, step in enumerate(steps_en, 1):
                lines.append(f"{i}. {step}")
            lines.append("")
        
        if expected_zh:
            lines.append(f"**预期成果 (中文)**: {expected_zh}  ")
            lines.append(f"**Expected Outcome (English)**: {expected_en}  ")
            lines.append("")
        
        if case_zh:
            lines.append(f"**经典案例 (中文)**: {case_zh}  ")
            lines.append(f"**Classic Case (English)**: {case_en}  ")
            lines.append("")
        
        lines.append("---")
        lines.append("")

# Mode index
lines.append("## 🧠 思维模式索引 (145 种)")
lines.append("")
lines.append("| ID | 中文名称 | English Name | 领域 | 核心口诀 |")
lines.append("|----|----------|--------------|------|----------|")
for mid in sorted(zh_modes.keys(), key=int):
    data = zh_modes[mid]
    en_data = en_modes[mid]
    domain = MODE_DOMAINS.get(mid, 'Other')
    lines.append(f"| {mid} | {data[0]} | {en_data[0]} | {domain} | {data[1]} |")
lines.append("")

# Footer
lines.append("---")
lines.append("")
lines.append("*Generated by Protreptic Historical Figures Thinking Modes Library Generator*  ")
lines.append(f"*Total: {len(h_codes) + len(m_codes)} historical, {len(p4_codes)} P4, {len(p5_codes)} P5, {len(intl_codes)} international, {len(base_codes)} base = {len(zh)} scenarios*  ")

# Save
output_path = '/opt/data/workspace/Protreptic/docs/historical_figures_thinking_modes_library.md'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f"Library saved to {output_path}")
print(f"Total lines: {len(lines)}")
print(f"Historical: {len(h_codes) + len(m_codes)}, P4: {len(p4_codes)}, P5: {len(p5_codes)}, Intl: {len(intl_codes)}, Base: {len(base_codes)}")
print(f"Total: {len(zh)}")