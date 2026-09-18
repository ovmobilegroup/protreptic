import json

# Check what IN-ASH-001 etc look like in ZH
with open('/opt/data/workspace/Protreptic/scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)

# Check the new batch 4 entries
batch4_codes = ['IN-ASH-001', 'IN-KAU-001', 'IN-TAG-001', 'IN-GAN-001', 'IN-IGD-001', 'JP-TOK-001']
for code in batch4_codes:
    if code in zh:
        print(f"{code}: {json.dumps(zh[code], ensure_ascii=False, indent=2)[:300]}")
    else:
        print(f"{code}: NOT FOUND in ZH")

# Check the "code field" entry
if 'code field' in zh:
    print(f"\n'code field' entry: {json.dumps(zh['code field'], ensure_ascii=False, indent=2)}")