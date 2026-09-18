import json

# Load existing code maps
with open('code_maps.json', 'r', encoding='utf-8') as f:
    code_maps = json.load(f)

CODE_MAP = code_maps['CODE_MAP']
CODE_MAP_EN = code_maps['CODE_MAP_EN']

# Add 8 new historical figures
CODE_MAP.update({
    "H-SQ-51": "商鞅：法家工程化的国家机器制造者",
    "H-SQ-52": "苏秦：合纵抗秦的战略外交架构师",
    "H-ZY-53": "张仪：连横破盟的反制外交大师",
    "H-XH-54": "萧何：萧规曹随的后勤补给与行政系统奠基者",
    "H-LY-55": "刘晏：财政金融工程的盐铁漕运大师",
    "H-QJG-56": "戚继光：军事训练体系的非对称战争大师",
    "H-LSZ-57": "李时珍：药学系统化的实证药理学巨擘",
    "H-JSX-58": "贾思勰：农业系统工程的技术标准化先驱",
    "H-WZ-59": "魏徵：政治监督的谏诤制度设计师",
})

CODE_MAP_EN.update({
    "H-SQ-51": "Shang Yang: Legalist Engineering of the State Machine",
    "H-SQ-52": "Su Qin: Strategic Diplomatic Architect of Vertical Alliance Against Qin",
    "H-ZY-53": "Zhang Yi: Horizontal Alliance Breaker Counter-Diplomacy Master",
    "H-XH-54": "Xiao He: Xiao Rules Cao Follows Logistics Supply Administrative System Founder",
    "H-LY-55": "Liu Yan: Fiscal Financial Engineering Salt Iron Canal Transport Master",
    "H-QJG-56": "Qi Jiguang: Military Training System Asymmetric Warfare Master",
    "H-LSZ-57": "Li Shizhen: Pharmaceutical Systematization Empirical Pharmacology Giant",
    "H-JSX-58": "Jia Sixie: Agricultural Systems Engineering Technical Standardization Pioneer",
    "H-WZ-59": "Wei Zheng: Political Supervision Admonition System Designer",
})

# Save
with open('code_maps.json', 'w', encoding='utf-8') as f:
    json.dump({"CODE_MAP": CODE_MAP, "CODE_MAP_EN": CODE_MAP_EN}, f, ensure_ascii=False, indent=2)

print("Code maps updated!")
print(f"CODE_MAP: {len(CODE_MAP)} entries")
print(f"CODE_MAP_EN: {len(CODE_MAP_EN)} entries")