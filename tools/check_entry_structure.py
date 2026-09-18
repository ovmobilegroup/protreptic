import json

# Check the structure of AO-NET-001 in both ZH and EN
with open('/opt/data/workspace/Protreptic/scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)

with open('/opt/data/workspace/Protreptic/scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)

print("ZH AO-NET-001:")
print(json.dumps(zh.get('AO-NET-001', {}), ensure_ascii=False, indent=2)[:500])

print("\nEN AO-NET-001:")
print(json.dumps(en.get('AO-NET-001', {}), ensure_ascii=False, indent=2)[:500])

# Also check a few others
for code in ['AF-TRI-001', 'BD-LIB-001', 'EE-MER-001']:
    print(f"\nZH {code}:")
    print(json.dumps(zh.get(code, {}), ensure_ascii=False, indent=2)[:300])
    print(f"\nEN {code}:")
    print(json.dumps(en.get(code, {}), ensure_ascii=False, indent=2)[:300])