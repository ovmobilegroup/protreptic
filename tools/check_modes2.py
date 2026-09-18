import json

# Check tools modes_data.json more carefully
with open('/opt/data/workspace/Protreptic/tools/modes_data.json', 'r', encoding='utf-8') as f:
    tools_modes = json.load(f)

if isinstance(tools_modes, dict) and 'zh' in tools_modes:
    zh_modes = tools_modes['zh']
    print(f"Total zh keys: {len(zh_modes)}")
    
    numeric_keys = [k for k in zh_modes.keys() if not k.startswith('M') and k.isdigit()]
    m_keys = [k for k in zh_modes.keys() if k.startswith('M')]
    
    print(f"Numeric keys: {len(numeric_keys)}")
    print(f"M-prefixed keys: {len(m_keys)}")
    
    if numeric_keys:
        print(f"Max numeric key: {max(int(k) for k in numeric_keys)}")
    if m_keys:
        print(f"M keys: {m_keys[:20]}")
    
    # Check en as well
    en_modes = tools_modes['en']
    en_numeric = [k for k in en_modes.keys() if not k.startswith('M') and k.isdigit()]
    en_m = [k for k in en_modes.keys() if k.startswith('M')]
    print(f"\nEN total keys: {len(en_modes)}")
    print(f"EN numeric: {len(en_numeric)}, M: {len(en_m)}")
    if en_numeric:
        print(f"EN max numeric: {max(int(k) for k in en_numeric)}")

# Check root modes_data.json
with open('/opt/data/workspace/Protreptic/modes_data.json', 'r', encoding='utf-8') as f:
    root_modes = json.load(f)

if isinstance(root_modes, dict):
    print(f"\nRoot keys: {root_modes.keys()}")
    if 'zh' in root_modes:
        zh = root_modes['zh']
        print(f"Root zh total: {len(zh)}")
        zh_numeric = [k for k in zh.keys() if not k.startswith('M') and k.isdigit()]
        zh_m = [k for k in zh.keys() if k.startswith('M')]
        print(f"Root zh numeric: {len(zh_numeric)}, M: {len(zh_m)}")
        if zh_numeric:
            print(f"Root zh max numeric: {max(int(k) for k in zh_numeric)}")
    if 'en' in root_modes:
        en = root_modes['en']
        print(f"Root en total: {len(en)}")
        en_numeric = [k for k in en.keys() if not k.startswith('M') and k.isdigit()]
        en_m = [k for k in en.keys() if k.startswith('M')]
        print(f"Root en numeric: {len(en_numeric)}, M: {len(en_m)}")
        if en_numeric:
            print(f"Root en max numeric: {max(int(k) for k in en_numeric)}")