import json

# Load existing code maps
with open('code_maps.json', 'r', encoding='utf-8') as f:
    code_maps = json.load(f)

CODE_MAP = code_maps['CODE_MAP']
CODE_MAP_EN = code_maps['CODE_MAP_EN']

# Add 6 new historical figures
CODE_MAP.update({
    "H-CC-21": "曹操：挟天子以令诸侯的实用主义霸权",
    "H-SQ-22": "孙权：守成之主的平衡术与江东基业",
    "H-KX-23": "康熙：少年天子的权力收割与盛世奠基",
    "H-LH-24": "李鸿章：洋务派的悲剧性现代化实验",
    "H-JJ-25": "蒋介石：政军合一的权术家与战略失误",
    "H-ZD-26": "朱德：红军缔造者的军事民主与战略支撑",
})

CODE_MAP_EN.update({
    "H-CC-21": "Cao Cao: Pragmatic Hegemony via Imperial Legitimacy",
    "H-SQ-22": "Sun Quan: Balance Art of the Succession Ruler",
    "H-KX-23": "Kangxi: Boy Emperor's Power Consolidation & Golden Age Foundation",
    "H-LH-24": "Li Hongzhang: Tragic Modernization Experiment of Self-Strengthening",
    "H-JJ-25": "Chiang Kai-shek: Party-Army Fusion Politician & Strategic Blunders",
    "H-ZD-26": "Zhu De: Red Army Founder's Military Democracy & Strategic Backbone",
})

# Save
with open('code_maps.json', 'w', encoding='utf-8') as f:
    json.dump({"CODE_MAP": CODE_MAP, "CODE_MAP_EN": CODE_MAP_EN}, f, ensure_ascii=False, indent=2)

print("Code maps updated!")
print(f"CODE_MAP: {len(CODE_MAP)} entries")
print(f"CODE_MAP_EN: {len(CODE_MAP_EN)} entries")