import json

# Load existing code maps
with open('code_maps.json', 'r', encoding='utf-8') as f:
    code_maps = json.load(f)

CODE_MAP = code_maps['CODE_MAP']
CODE_MAP_EN = code_maps['CODE_MAP_EN']

# Add new historical figures
CODE_MAP.update({
    "H-LY-18": "刘裕：寄奴北伐的自然选择",
    "H-ZG-19": "赵构：偏安求存的权力平衡术",
    "H-YS-20": "袁世凯：北洋体系的现代化陷阱",
})

CODE_MAP_EN.update({
    "H-LY-18": "Liu Yu: Natural Selection of the Northern Expeditions",
    "H-ZG-19": "Zhao Gou: Power Balance Art of Compromised Survival",
    "H-YS-20": "Yuan Shikai: Modernization Trap of the Beiyang System",
})

# Save
with open('code_maps.json', 'w', encoding='utf-8') as f:
    json.dump({"CODE_MAP": CODE_MAP, "CODE_MAP_EN": CODE_MAP_EN}, f, ensure_ascii=False, indent=2)

print("Code maps updated!")
print(f"CODE_MAP: {len(CODE_MAP)} entries")
print(f"CODE_MAP_EN: {len(CODE_MAP_EN)} entries")