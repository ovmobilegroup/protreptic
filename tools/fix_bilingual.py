import json

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved: {path}")

# Fix EN entries to have proper i18n format (name_zh/name_en, description_zh/description_en)
# They should mirror the ZH structure

with open('/opt/data/workspace/Protreptic/scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)

with open('/opt/data/workspace/Protreptic/scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)

# The missing EN codes
missing_en_codes = [
    'AF-TRI-001', 'AO-NET-001', 'BD-LIB-001', 'BT-GNH-001',
    'CF-BOG-001', 'CM-AHM-001', 'EE-MER-001', 'IL-HAVR-001-TEST',
    'LK-CIV-001', 'MO-NAT-001', 'MV-ISL-001', 'NP-HIM-001',
    'PK-ISL-001', 'PK-SUF-001', 'QA-ENE-001', 'ST-CAC-001',
    'TD-HIS-001', 'TN-DEM-001'
]

# Also include JP-TOK-001
all_codes = missing_en_codes + ['JP-TOK-001']

for code in all_codes:
    if code in zh and code in en:
        zh_entry = zh[code]
        en_entry = en[code]
        
        # Check if ZH uses standard format (name, description) or i18n (name_zh, description_zh)
        zh_has_standard = 'name' in zh_entry and 'description' in zh_entry
        zh_has_i18n = 'name_zh' in zh_entry and 'description_zh' in zh_entry
        
        # Check EN format
        en_has_standard = 'name' in en_entry and 'description' in en_entry
        en_has_i18n = 'name_en' in en_entry and 'description_en' in en_entry
        
        print(f"\n{code}:")
        print(f"  ZH: standard={zh_has_standard}, i18n={zh_has_i18n}")
        print(f"  EN: standard={en_has_standard}, i18n={en_has_i18n}")
        
        # Fix EN to match ZH format
        if zh_has_i18n and not en_has_i18n:
            # ZH uses i18n, make EN use i18n too
            if 'name' in en_entry and 'name_en' not in en_entry:
                en_entry['name_en'] = en_entry['name']
            if 'description' in en_entry and 'description_en' not in en_entry:
                en_entry['description_en'] = en_entry['description']
            # Remove standard fields if they exist (to force i18n)
            if 'name' in en_entry:
                del en_entry['name']
            if 'description' in en_entry:
                del en_entry['description']
            print(f"  -> Fixed EN to i18n format")
        elif zh_has_standard and not en_has_standard:
            # ZH uses standard, make EN use standard
            if 'name_en' in en_entry and 'name' not in en_entry:
                en_entry['name'] = en_entry['name_en']
            if 'description_en' in en_entry and 'description' not in en_entry:
                en_entry['description'] = en_entry['description_en']
            # Remove i18n fields
            if 'name_en' in en_entry:
                del en_entry['name_en']
            if 'description_en' in en_entry:
                del en_entry['description_en']
            print(f"  -> Fixed EN to standard format")

save_json('/opt/data/workspace/Protreptic/scenarios_en.json', en)
save_json('/opt/data/workspace/Protreptic/tools/scenarios_en.json', en)