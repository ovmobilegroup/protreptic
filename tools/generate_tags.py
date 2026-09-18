#!/usr/bin/env python3
"""
Generate scenario tags index for filtering API.
Creates scenario_tags.json with domain/core_mode/application tags for each figure.
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

zh_modes = modes['zh']
en_modes = modes['en']

# Domain mapping
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
    '41': 'Operational', '42': 'Personal'
}

# Application scenarios mapping (based on mode categories)
MODE_APPLICATIONS = {
    '1': ['Strategic Planning', 'Crisis Decision'],
    '2': ['Policy Making', 'Product Development'],
    '3': ['Entrepreneurship', 'Long-term Competition'],
    '4': ['Market Entry', 'Startup Positioning'],
    '5': ['Scientific Decision', 'Academic Research'],
    '6': ['Business Cooperation', 'Resource Integration'],
    '7': ['Strategic Planning', 'Risk Management'],
    '8': ['Organizational Change', 'Product Iteration'],
    '9': ['Enterprise Development', 'Tech Breakthrough'],
    '10': ['Team Building', 'Organizational Management'],
    '11': ['Crisis Management', 'Product Strategy'],
    '12': ['Complex Systems', 'Strategic Planning'],
    '13': ['Business Competition', 'Negotiation'],
    '14': ['Strategic Planning', 'Crisis Management'],
    '15': ['Market Competition', 'Startup Strategy'],
    '16': ['Weak Competition', 'Limited Resources'],
    '17': ['Investment Decision', 'Business Analysis'],
    '18': ['Team Management', 'Organizational Design'],
    '19': ['Resource Allocation', 'Personal Choice'],
    '20': ['Game Theory', 'Mechanism Design'],
    '21': ['Self-cultivation', 'Personal Growth'],
    '22': ['Knowledge Systems', 'Theoretical Construction'],
    '23': ['Artistic Creation', 'Aesthetic Judgment'],
    '24': ['Classification', 'Concept Engineering'],
    '25': ['Empirical Research', 'Historical Analysis'],
    '26': ['Mind Training', 'Self-realization'],
    '27': ['Ontology', 'Metaphysics'],
    '28': ['Engineering Practice', 'Standardization'],
    '29': ['Philology', 'Textual Criticism'],
    '30': ['Source Verification', 'Evidence Chain'],
    '31': ['System Design', 'Architecture'],
    '32': ['Institutional Design', 'Governance'],
    '33': ['Nation Building', 'Imperial Governance'],
    '34': ['Constitutional Design', 'Legal Framework'],
    '35': ['Implementation', 'Execution'],
    '36': ['Moral Cultivation', 'Character Building'],
    '37': ['Epistemology', 'Mind-Nature'],
    '38': ['Operational Management', 'Process Control'],
    '39': ['Economic Reform', 'Price Theory'],
    '40': ['Military Operations', 'Tactical Command'],
    '41': ['Information Systems', 'Communication'],
    '42': ['Leadership', 'Statecraft']
}

# Historical domain classification
HISTORICAL_DOMAINS = {
    'Philosophy': ['Confucianism', 'Daoism', 'Buddhism', 'Legalism', 'Mohism', 'Neo-Confucianism', 'Heart-Mind'],
    'Historiography': ['Annals', 'Biographical', 'Institutional', 'Evidential', 'Theoretical'],
    'Military': ['Strategy', 'Tactics', 'Operations', 'Logistics', 'Naval', 'Guerrilla'],
    'Science_Tech': ['Mathematics', 'Astronomy', 'Mechanics', 'Medicine', 'Agriculture', 'Geology', 'Physics', 'Chemistry'],
    'Governance': ['Institutional', 'Economic', 'Legal', 'Administrative', 'Diplomatic'],
    'Literature_Arts': ['Poetry', 'Prose', 'Calligraphy', 'Painting', 'Drama', 'Music', 'Aesthetics'],
    'Religion': ['Buddhism', 'Daoism', 'Confucianism', 'Folk', 'Syncretic'],
    'Education': ['Imperial Exams', 'Academy', 'Modern', 'Vocational'],
    'Economics': ['Fiscal', 'Monetary', 'Trade', 'Industrial', 'Agricultural'],
    'Ethics': ['Virtue', 'Duty', 'Consequence', 'Care', 'Liberation']
}

# Build tags for each historical figure
scenario_tags = {}

for code, entry in zh.items():
    if not code.startswith('H-'):
        continue
    
    mode_ids = entry['modes']
    
    # Domain tags (from modes)
    domains = list(set(MODE_DOMAINS.get(str(m), 'Unknown') for m in mode_ids))
    
    # Application tags (from modes)
    applications = []
    for m in mode_ids:
        apps = MODE_APPLICATIONS.get(str(m), [])
        applications.extend(apps)
    applications = list(set(applications))
    
    # Core mode tags (the most representative mode)
    core_modes = [str(m) for m in mode_ids]
    
    # Historical domain classification (based on name/description)
    historical_domains = []
    name = entry['name']
    desc = entry['description']
    text = name + ' ' + desc
    
    if any(kw in text for kw in ['理学', '心学', '儒家', '道家', '佛教', '法家', '墨家', '名家', '玄学', '经学', '考据', '性理', '气论', '太极', '格物', '致良知', '知行', '童心']):
        historical_domains.append('Philosophy')
    if any(kw in text for kw in ['史通', '通志', '文献通考', '廿二史', '十七史商榷', '纪事本末', '史学', '考据', '辨伪', '目录', '编年', '纪传', '制度史', '史论', '史评', '史体']):
        historical_domains.append('Historiography')
    if any(kw in text for kw in ['兵法', '军事', '将', '战', '歼灭', '游击', '抗金', '抗清', '长征', '三大战役', '反击战', '边境', '军区', '元帅', '上将', '背嵬军', '岳家军', '白杆兵', '黄天荡']):
        historical_domains.append('Military')
    if any(kw in text for kw in ['数学', '天文', '历法', '地质', '物理', '化学', '医学', '本草', '农业', '水利', '机械', '仪器', 'π', '测度', '交食', '浑天仪', '大衍历', '授时历', '几何', '代数', '微积分', '核', '导弹', '航天', '两弹', '卫星', '激光', '杂交', '青蒿素', '气象', '地质力学', '实验物理', '数学工程']):
        historical_domains.append('Science_Tech')
    if any(kw in text for kw in ['制度', '改革', '变法', '税制', '科举', '选举', '职官', '法律', '行政', '外交', '宰相', '行省', '孟安谋克', '三省', '六部', '鸟笼经济', '价格', '货币', '金融', '央行', '所有制', '产权', '供给侧', '调整']):
        historical_domains.append('Governance')
    if any(kw in text for kw in ['诗', '词', '文', '书法', '绘画', '戏曲', '音乐', '美学', '文学', '小说', '辞赋', '山水', '田园', '隐逸', '性灵', '神韵', '风骨', '兰亭', '永字', '兰亭集序', '聊斋', '红楼', '儒林外史']):
        historical_domains.append('Literature_Arts')
    if any(kw in text for kw in ['佛教', '道教', '天师', '全真', '禅宗', '天台', '净土', '密宗', '格鲁', '西行', '取经', '翻译', '符箓', '斋醮', '内丹', '金丹', '止观', '三观', '显密']):
        historical_domains.append('Religion')
    if any(kw in text for kw in ['教育', '书院', '科举', '太学', '国子监', '大学', '新学', '留学', '物理系', '物理教育', '人才培养']):
        historical_domains.append('Education')
    if any(kw in text for kw in ['经济', '财政', '赋税', '钱币', '市舶', '盐铁', '漕运', '平籴', '价格', '货币', '金融', '央行', '改革', '所有制', '产权', '供给侧', '调整']):
        historical_domains.append('Economics')
    if any(kw in text for kw in ['仁', '义', '礼', '智', '信', '忠', '孝', '廉', '耻', '德', '修身', '齐家', '治国', '平天下', '三省', '童心', '良知', '致良知', '格物', '诚意', '正心', '养生', '任诞', '超越', '自由']):
        historical_domains.append('Ethics')
    
    historical_domains = list(set(historical_domains))
    
    # Era tag (simplified)
    if any(p in code for p in ['H-GGZ', 'H-LZ', 'H-ZZ', 'H-KZ', 'H-MZ', 'H-XZ', 'H-ZS', 'H-SQ', 'H-FL', 'H-LL', 'H-SH', 'H-MZ-167', 'H-MZ-169', 'H-MZB', 'H-SBH', 'H-SD', 'H-LS', 'H-WQ', 'H-BG', 'H-YW', 'H-MZB-165']):
        era = 'Pre-Qin'
    elif any(p in code for p in ['H-LB', 'H-XH', 'H-LS-03', 'H-ZG', 'H-SB', 'H-HF', 'H-LS-158', 'H-GZ', 'H-ZK', 'H-ZY']):
        era = 'Qin-Han'
    elif any(p in code for p in ['H-ZL', 'H-CC', 'H-SQ-22', 'H-LB-15', 'H-JSX', 'H-TYM', 'H-RJ', 'H-TYM-220']):
        era = 'Three-Kingdoms-Jin'
    elif any(p in code for p in ['H-ZCZ', 'H-YX', 'H-THJ', 'H-WZY', 'H-QCJ', 'H-XLY', 'H-XZ']):
        era = 'Northern-Southern'
    elif any(p in code for p in ['H-LJ', 'H-WXZ', 'H-CL', 'H-LZY', 'H-FZY', 'H-SY', 'H-QXK', 'H-LD', 'H-LDB', 'H-ZLQ', 'H-QCJ-245']):
        era = 'Sui-Tang'
    elif any(p in code for p in ['H-SMG', 'H-WB', 'H-OYX', 'H-WAS', 'H-ZJ', 'H-ZDY', 'H-SD-46', 'H-ZDY-212', 'H-EC', 'H-ZX', 'H-LJY', 'H-WY', 'H-QCJ-155', 'H-YS-261', 'H-QQ']):
        era = 'Song-Yuan'
    elif '2' in code[:3] or '3' in code[:3] or '16' in code[:3] or '17' in code[:3] or '18' in code[:3] or '19' in code[:3] or '20' in code[:3] or '21' in code[:3] or '22' in code[:3] or '23' in code[:3] or '24' in code[:3] or '25' in code[:3]:
        era = 'Ming-Qing'
    elif any(p in code for p in ['H-TS', 'H-ZJ', 'H-ZD-26', 'H-ZG-19', 'H-ZZD-35', 'H-HLG', 'H-HYP', 'H-ZKZ', 'H-ZTY', 'H-LBN', 'H-FML', 'H-WJZ', 'H-CXQ', 'H-YF', 'H-KYW', 'H-LH', 'H-XMQ', 'H-SMX', 'H-LGJ', 'H-PDH', 'H-ZEL', 'H-LXN', 'H-LSQ', 'H-CY', 'H-YM', 'H-YLP', 'H-TYY', 'H-DJX', 'H-QSQ', 'H-QM', 'H-WMS', 'H-GZP', 'H-LZX', 'H-ZXC', 'H-WYS', 'H-YG', 'H-LH', 'H-SMX', 'H-LGJ', 'H-WJL', 'H-ZRB']):
        era = 'Modern-Early'
    else:
        era = 'Modern'
    
    # Gender tag
    gender = 'Unknown'
    female_names = ['蔡文姬', '上官婉儿', '武则天', '李清照', '秦良玉', '秋瑾', '邓颖超', '宋庆龄', '蔡畅', '康克清', '班昭']
    if any(name in entry['name'] for name in female_names):
        gender = 'Female'
    else:
        gender = 'Male'
    
    # Nationality/ethnicity tag
    ethnicity = 'Han'
    minority_keywords = ['契丹', '女真', '蒙古', '回回', '番', '术', '西藏', '维吾尔', '哈萨克', '蒙古族', '满族', '回族', '藏族', '壮族', '彝族', '苗族']
    if any(kw in text for kw in minority_keywords):
        ethnicity = 'Minority'
    
    # Build tags object
    scenario_tags[code] = {
        'code': code,
        'name_zh': entry['name'],
        'name_en': en[code]['name'],
        'era': era,
        'gender': gender,
        'ethnicity': ethnicity,
        'domains': domains,
        'core_modes': core_modes,
        'applications': applications,
        'historical_domains': historical_domains,
        'mode_count': len(mode_ids)
    }

# Save
output = {
    'metadata': {
        'generated': '2025-07-24',
        'total_scenarios': len(scenario_tags),
        'domains': list(set(d for tags in scenario_tags.values() for d in tags['domains'])),
        'eras': sorted(set(tags['era'] for tags in scenario_tags.values())),
        'historical_domains': list(set(d for tags in scenario_tags.values() for d in tags['historical_domains'])),
        'genders': list(set(tags['gender'] for tags in scenario_tags.values())),
        'ethnicities': list(set(tags['ethnicity'] for tags in scenario_tags.values()))
    },
    'tags': scenario_tags
}

with open('/opt/data/workspace/Protreptic/tools/scenario_tags.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Scenario tags saved: {len(scenario_tags)} figures")
print(f"Domains: {output['metadata']['domains']}")
print(f"Eras: {output['metadata']['eras']}")
print(f"Historical domains: {output['metadata']['historical_domains']}")
print(f"Genders: {output['metadata']['genders']}")
print(f"Ethnicities: {output['metadata']['ethnicities']}")