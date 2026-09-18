import json

with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh_data = json.load(f)

with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    en_data = json.load(f)

zh_codes = set(zh_data.keys())
en_codes = set(en_data.keys())

print(f"ZH codes: {len(zh_codes)}")
print(f"EN codes: {len(en_codes)}")

only_zh = zh_codes - en_codes
only_en = en_codes - zh_codes

print(f"Only in ZH: {len(only_zh)}")
if only_zh:
    for c in sorted(only_zh)[:20]:
        print(f"  {c}")
    if len(only_zh) > 20:
        print(f"  ... and {len(only_zh) - 20} more")

print(f"Only in EN: {len(only_en)}")
if only_en:
    for c in sorted(only_en)[:20]:
        print(f"  {c}")
    if len(only_en) > 20:
        print(f"  ... and {len(only_en) - 20} more")