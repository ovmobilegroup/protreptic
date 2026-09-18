import json

# Load existing code maps
with open('code_maps.json', 'r', encoding='utf-8') as f:
    code_maps = json.load(f)

CODE_MAP = code_maps['CODE_MAP']
CODE_MAP_EN = code_maps['CODE_MAP_EN']

# Add 8 new historical figures
CODE_MAP.update({
    "H-SHY-40": "桑弘羊：国家财政宏观调控的奠基者",
    "H-SMG-41": "司马光：资治通鉴的史学治国大师",
    "H-GYW-42": "顾炎武：经世致用的实学巨擘",
    "H-SB-43": "沈括：梦溪笔谈的科学实证通才",
    "H-LZX-44": "林则徐：睁眼看世界的危机外交家",
    "H-BC-45": "班超：以少驭多的丝路经营大师",
    "H-SD-46": "苏轼：审美抗压的民本文人首相",
    "H-ZXC-47": "章学诚：文史通义的史学理论自觉大师",
})

CODE_MAP_EN.update({
    "H-SHY-40": "Sang Hongyang: Founder of State Fiscal Macroeconomic Regulation",
    "H-SMG-41": "Sima Guang: Master of History-Based Governance",
    "H-GYW-42": "Gu Yanwu: Giant of Practical Statecraft Learning",
    "H-SB-43": "Shen Kuo: Dream Pool Essays Scientific Empiricism Polymath",
    "H-LZX-44": "Lin Zexu: Opening Eyes to See the World Crisis Diplomat",
    "H-BC-45": "Ban Chao: Silk Road Operator Who Ruled Many with Few",
    "H-SD-46": "Su Shi: Aesthetic Resilience Prime Minister of People-Oriented Literati",
    "H-ZXC-47": "Zhang Xuecheng: Master of Theoretical Self-Awareness in Historiography",
})

# Save
with open('code_maps.json', 'w', encoding='utf-8') as f:
    json.dump({"CODE_MAP": CODE_MAP, "CODE_MAP_EN": CODE_MAP_EN}, f, ensure_ascii=False, indent=2)

print("Code maps updated!")
print(f"CODE_MAP: {len(CODE_MAP)} entries")
print(f"CODE_MAP_EN: {len(CODE_MAP_EN)} entries")