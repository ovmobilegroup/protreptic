import json

# Load existing code maps
with open('code_maps.json', 'r', encoding='utf-8') as f:
    code_maps = json.load(f)

CODE_MAP = code_maps['CODE_MAP']
CODE_MAP_EN = code_maps['CODE_MAP_EN']

# Add 8 new historical figures
CODE_MAP.update({
    "H-GZ-60": "管仲：霸主制造者的国家机器工程师",
    "H-SQ-61": "司马迁：究天人之际的史学方法论奠基者",
    "H-ZX-62": "朱熹：理学体系化的认知框架构建者",
    "H-LZY-63": "柳宗元：政治改革思维的批判性写作者",
    "H-WFZ-64": "王夫之：历史循环律的实学巨匠",
    "H-CYK-65": "陈寅恪：独立精神的学术方法论大师",
    "H-QM-67": "钱穆：中国史治史方法论的文化重心论者",
    "H-LQC-68": "梁启超：新史学与变法思维的启蒙先驱",
})

CODE_MAP_EN.update({
    "H-GZ-60": "Guan Zhong: Hegemon Maker's State Machine Engineer",
    "H-SQ-61": "Sima Qian: Historiography Methodology Founder of Ultimate Heaven-Human",
    "H-ZX-62": "Zhu Xi: Neo-Confucianism Systematizer of Cognitive Framework",
    "H-LZY-63": "Liu Zongyuan: Political Reform Thinker Critical Writer",
    "H-WFZ-64": "Wang Fuzhi: Historical Cycle Theory Giant of Practical Learning",
    "H-CYK-65": "Chen Yinke: Independent Spirit Academic Methodology Master",
    "H-QM-67": "Qian Mu: Chinese History Methodology Cultural Center of Gravity Theorist",
    "H-LQC-68": "Liang Qichao: New Historiography and Reform Enlightenment Pioneer",
})

# Save
with open('code_maps.json', 'w', encoding='utf-8') as f:
    json.dump({"CODE_MAP": CODE_MAP, "CODE_MAP_EN": CODE_MAP_EN}, f, ensure_ascii=False, indent=2)

print("Code maps updated!")
print(f"CODE_MAP: {len(CODE_MAP)} entries")
print(f"CODE_MAP_EN: {len(CODE_MAP_EN)} entries")