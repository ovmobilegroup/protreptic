import json

# Check scenarios zh and en counts
with open('/opt/data/workspace/Protreptic/scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)

with open('/opt/data/workspace/Protreptic/scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)

print(f"ZH total keys: {len(zh)}")
print(f"EN total keys: {len(en)}")

# Find missing EN entries
zh_keys = set(zh.keys())
en_keys = set(en.keys())
missing_en = zh_keys - en_keys
extra_en = en_keys - zh_keys
print(f"\nMissing EN entries ({len(missing_en)}): {sorted(missing_en)}")
print(f"Extra EN entries ({len(extra_en)}): {sorted(extra_en)}")

# Check code_maps
with open('/opt/data/workspace/Protreptic/code_maps.json', 'r', encoding='utf-8') as f:
    code_maps = json.load(f)

print(f"\nCODE_MAP entries: {len(code_maps.get('CODE_MAP', {}))}")
print(f"CODE_MAP_EN entries: {len(code_maps.get('CODE_MAP_EN', {}))}")

# Find scenario codes that need code_map
scenario_codes = [k for k, v in zh.items() if isinstance(v, dict) and 'modes' in v]
print(f"Scenario codes with modes: {len(scenario_codes)}")

missing_codemap = [c for c in scenario_codes if c not in code_maps.get('CODE_MAP', {})]
missing_codemap_en = [c for c in scenario_codes if c not in code_maps.get('CODE_MAP_EN', {})]
print(f"Missing CODE_MAP: {len(missing_codemap)}")
if missing_codemap:
    print(f"  First 20: {missing_codemap[:20]}")
print(f"Missing CODE_MAP_EN: {len(missing_codemap_en)}")
if missing_codemap_en:
    print(f"  First 20: {missing_codemap_en[:20]}")