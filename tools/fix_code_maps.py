import json

# Read existing code_maps.json
with open('/opt/data/workspace/Protreptic/tools/code_maps.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

CODE_MAP = data['CODE_MAP']
CODE_MAP_EN = data['CODE_MAP_EN']

# Remove the extra H-LB-17 entry
if 'H-LB-17' in CODE_MAP:
    del CODE_MAP['H-LB-17']
    print("Removed H-LB-17 from CODE_MAP")
if 'H-LB-17' in CODE_MAP_EN:
    del CODE_MAP_EN['H-LB-17']
    print("Removed H-LB-17 from CODE_MAP_EN")

# Write back
data['CODE_MAP'] = CODE_MAP
data['CODE_MAP_EN'] = CODE_MAP_EN

with open('/opt/data/workspace/Protreptic/tools/code_maps.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"CODE_MAP: {len(CODE_MAP)}, CODE_MAP_EN: {len(CODE_MAP_EN)}")