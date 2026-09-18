#!/usr/bin/env python3
import json

with open('/opt/data/workspace/Protreptic/scenarios_zh.json') as f:
    zh = json.load(f)
with open('/opt/data/workspace/Protreptic/scenarios_en.json') as f:
    en = json.load(f)

print('ZH total keys:', len(zh))
print('EN total keys:', len(en))

# Count dict entries (scenarios with modes)
zh_dict = {k: v for k, v in zh.items() if isinstance(v, dict) and 'modes' in v}
en_dict = {k: v for k, v in en.items() if isinstance(v, dict) and 'modes' in v}
print('ZH dict entries:', len(zh_dict))
print('EN dict entries:', len(en_dict))

# Historical counts
zh_hist = sum(1 for k in zh_dict if k.startswith(('H-', 'M-')))
en_hist = sum(1 for k in en_dict if k.startswith(('H-', 'M-')))
print('ZH historical:', zh_hist)
print('EN historical:', en_hist)

# P4/P5 counts
zh_p4 = sum(1 for k in zh_dict if k.startswith('P4-'))
zh_p5 = sum(1 for k in zh_dict if k.startswith('P5-'))
en_p4 = sum(1 for k in en_dict if k.startswith('P4-'))
en_p5 = sum(1 for k in en_dict if k.startswith('P5-'))
print('ZH P4:', zh_p4, 'P5:', zh_p5)
print('EN P4:', en_p4, 'P5:', en_p5)

# International prefixes
intl_prefixes = ('EU-', 'UK-', 'US-', 'RU-', 'JP-', 'KR-', 'BR-', 'FR-', 'IT-', 'IN-', 'IR-', 'AT-', 'CH-', 'PL-', 'CZ-',
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
    'PY-', 'UY-', 'AR-', 'CL-', 'MX-', 'GT-', 'SV-', 'NI-', 'CU-', 'HT-', 'DO-', 'JM-', 'CA-', 'US-', 'GL-')

zh_intl = sum(1 for k in zh_dict if any(k.startswith(p) for p in intl_prefixes))
en_intl = sum(1 for k in en_dict if any(k.startswith(p) for p in intl_prefixes))
print('ZH international:', zh_intl)
print('EN international:', en_intl)

# Check for missing EN entries
missing_en = [k for k in zh if k not in en]
print('Missing EN for:', len(missing_en))
for m in missing_en[:20]:
    print(f'  - {m}')