import json

# Load existing code maps
with open('code_maps.json', 'r', encoding='utf-8') as f:
    code_maps = json.load(f)

CODE_MAP = code_maps['CODE_MAP']
CODE_MAP_EN = code_maps['CODE_MAP_EN']

# Add 6 new historical figures
CODE_MAP.update({
    "H-WZ-27": "武则天：破门阀立科举的权力重构者",
    "H-YZ-28": "雍正：密折军机处的极致执行力",
    "H-ZZ-29": "左宗棠：区域军工体系的边疆治理者",
    "H-ZJ-30": "张謇：状元办实业的乡土建设先驱",
    "H-FL-31": "范蠡：三迁三散的财富周期大师",
    "H-GZ-32": "郭子仪：九朝元老的危机收拾大师",
})

CODE_MAP_EN.update({
    "H-WZ-27": "Wu Zetian: Power Restructurer Who Broke Aristocracy with Imperial Exams",
    "H-YZ-28": "Yongzheng: Extreme Execution via Secret Memorials & Grand Council",
    "H-ZZ-29": "Zuo Zongtang: Regional Military-Industrial System for Frontier Governance",
    "H-ZJ-30": "Zhang Jian: Scholar-Turned-Industrialist & Rural Reconstruction Pioneer",
    "H-FL-31": "Fan Li: Three Migrations Three Distributions Wealth Cycle Master",
    "H-GZ-32": "Guo Ziyi: Nine-Dynasty Elder & Crisis Recovery Master",
})

# Save
with open('code_maps.json', 'w', encoding='utf-8') as f:
    json.dump({"CODE_MAP": CODE_MAP, "CODE_MAP_EN": CODE_MAP_EN}, f, ensure_ascii=False, indent=2)

print("Code maps updated!")
print(f"CODE_MAP: {len(CODE_MAP)} entries")
print(f"CODE_MAP_EN: {len(CODE_MAP_EN)} entries")