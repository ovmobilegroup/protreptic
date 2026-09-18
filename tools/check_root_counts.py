import json

# Check ROOT directory files (actual main data)
with open('/opt/data/workspace/Protreptic/scenarios_zh.json') as f:
    szh = json.load(f)
with open('/opt/data/workspace/Protreptic/scenarios_en.json') as f:
    sen = json.load(f)
with open('/opt/data/workspace/Protreptic/modes_data.json') as f:
    modes = json.load(f)
with open('/opt/data/workspace/Protreptic/code_maps.json') as f:
    cm = json.load(f)
with open('/opt/data/workspace/Protreptic/code_maps_en.json') as f:
    cme = json.load(f)

print(f'root/scenarios_zh.json: {len(szh)} entries (dict)')
print(f'root/scenarios_en.json: {len(sen)} entries (dict)')
print(f'root/modes_data.json: {len(modes)} entries (list)')
print(f'root/code_maps.json CODE_MAP: {len(cm.get("CODE_MAP", {}))} entries')
print(f'root/code_maps_en.json CODE_MAP_EN: {len(cme.get("CODE_MAP_EN", {}))} entries')

def is_scenario_entry(entry):
    return isinstance(entry, dict) and 'modes' in entry and isinstance(entry['modes'], list)

zh_dict = {k: v for k, v in szh.items() if is_scenario_entry(v)}
en_dict = {k: v for k, v in sen.items() if is_scenario_entry(v)}

print(f'root scenarios_zh dict entries: {len(zh_dict)}')
print(f'root scenarios_en dict entries: {len(en_dict)}')

h_zh = sum(1 for k in zh_dict if k.startswith(('H-', 'M-')))
h_en = sum(1 for k in en_dict if k.startswith(('H-', 'M-')))
print(f'H/M count ZH: {h_zh}')
print(f'H/M count EN: {h_en}')

p4_zh = sum(1 for k in zh_dict if k.startswith('P4-'))
p4_en = sum(1 for k in en_dict if k.startswith('P4-'))
print(f'P4 count ZH: {p4_zh}')
print(f'P4 count EN: {p4_en}')

p5_zh = sum(1 for k in zh_dict if k.startswith('P5-'))
p5_en = sum(1 for k in en_dict if k.startswith('P5-'))
print(f'P5 count ZH: {p5_zh}')
print(f'P5 count EN: {p5_en}')

# International count
INTL_PREFIXES = (
    'EU-', 'UK-', 'US-', 'RU-', 'JP-', 'KR-', 'BR-', 'FR-', 'IT-', 'IN-', 'IR-', 'AT-', 'CH-', 'PL-', 'CZ-',
    'MX-', 'AR-', 'CL-', 'CO-', 'IL-', 'SE-', 'NO-', 'DK-', 'FI-', 'ZA-', 'NG-', 'KE-', 'EG-', 'SG-', 'TH-',
    'VN-', 'ID-', 'PH-', 'AU-', 'NZ-', 'TR-', 'UZ-', 'KZ-', 'MN-', 'TW-', 'SA-', 'IQ-', 'SY-', 'LB-', 'JO-',
    'PS-', 'CA-', 'GL-', 'INU-', 'CA-SMI-', 'UA-', 'BY-', 'RS-', 'HR-', 'SI-', 'HU-', 'RO-', 'BG-', 'ET-',
    'GH-', 'TZ-', 'CD-', 'SN-', 'CI-', 'MZ-', 'AO-', 'PE-', 'VE-', 'CU-', 'BO-', 'EC-', 'UY-', 'PY-', 'KG-',
    'TJ-', 'TM-', 'MM-', 'KH-', 'LA-', 'BN-', 'ID-', 'PH-', 'TL-', 'PG-', 'FJ-', 'WS-', 'TO-', 'VU-', 'JM-',
    'HT-', 'DO-', 'TT-', 'BB-', 'AR-', 'CL-', 'PK-', 'BD-', 'LK-', 'NP-', 'AF-', 'MV-', 'BT-', 'AE-', 'QA-',
    'KW-', 'BH-', 'SA-', 'JO-', 'PS-', 'ML-', 'BF-', 'NE-', 'MR-', 'SN-', 'GM-', 'GW-', 'CI-', 'LR-', 'SL-',
    'ZA-', 'ZW-', 'BW-', 'NA-', 'SZ-', 'CO-', 'EC-', 'PE-', 'BO-', 'PY-', 'UY-', 'AR-', 'ES-', 'PT-', 'GR-',
    'AL-', 'MK-', 'BA-', 'SI-', 'MT-', 'NO-', 'SE-', 'DK-', 'FI-', 'EE-', 'LV-', 'LT-', 'PL-', 'GE-', 'AM-',
    'AZ-', 'MD-', 'RO-', 'KZ-', 'UZ-', 'KG-', 'TJ-', 'TM-', 'VN-', 'LA-', 'KH-', 'TH-', 'MM-', 'MY-', 'ID-',
    'PH-', 'SG-', 'BN-', 'TL-', 'NP-', 'BT-', 'LK-', 'MV-', 'YE-', 'OM-', 'KW-', 'BH-', 'QA-', 'AE-', 'JO-',
    'LB-', 'SY-', 'IQ-', 'NG-', 'KE-', 'TZ-', 'ZW-', 'ZA-', 'ET-', 'GH-', 'SN-', 'CI-', 'CO-', 'EC-', 'BO-',
    'PY-', 'UY-', 'AR-', 'CL-', 'MX-', 'GT-', 'SV-', 'NI-', 'CU-', 'HT-', 'DO-', 'JM-', 'CA-', 'US-', 'GL-'
)

intl_zh = sum(1 for k in zh_dict if any(k.startswith(p) for p in INTL_PREFIXES))
intl_en = sum(1 for k in en_dict if any(k.startswith(p) for p in INTL_PREFIXES))
print(f'International count ZH: {intl_zh}')
print(f'International count EN: {intl_en}')

# Check modes_data structure (it's a list in root)
print(f'modes_data is list of {len(modes)} entries')
if modes:
    print(f'First entry keys: {list(modes[0].keys())}')