import json

# Load existing code maps
with open('code_maps.json', 'r', encoding='utf-8') as f:
    code_maps = json.load(f)

CODE_MAP = code_maps['CODE_MAP']
CODE_MAP_EN = code_maps['CODE_MAP_EN']

# Add 3 new historical figures
CODE_MAP.update({
    "H-LL-48": "李悝：法家鼻祖的变法奠基者",
    "H-SW-49": "孙武：兵法集大成的战略欺诈大师",
    "H-ZZJ-50": "张仲景：医学系统论的辨证论治鼻祖",
})

CODE_MAP_EN.update({
    "H-LL-48": "Li Kui: Legalist Founder of Reform Foundation",
    "H-SW-49": "Sun Wu: Military Strategy Deception Master",
    "H-ZZJ-50": "Zhang Zhongjing: Medical Systems Theory Ancestor of Syndrome Differentiation",
})

# Save
with open('code_maps.json', 'w', encoding='utf-8') as f:
    json.dump({"CODE_MAP": CODE_MAP, "CODE_MAP_EN": CODE_MAP_EN}, f, ensure_ascii=False, indent=2)

print("Code maps updated!")
print(f"CODE_MAP: {len(CODE_MAP)} entries")
print(f"CODE_MAP_EN: {len(CODE_MAP_EN)} entries")