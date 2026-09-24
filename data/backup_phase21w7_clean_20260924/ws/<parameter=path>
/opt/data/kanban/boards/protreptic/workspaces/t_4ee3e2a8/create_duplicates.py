import json
import os

# IL-SCI-001 duplicates
il_sci_path = '/opt/data/workspace/Protreptic/IL/IL-SCI-001.json'
with open(il_sci_path, 'r', encoding='utf-8') as f:
    il_sci_data = json.load(f)

# DE-PHYS-001
de_data = il_sci_data.copy()
de_data['code'] = 'DE-PHYS-001'
de_data['nationality'] = '德国'
de_data['ethnicity'] = '德国'
# Keep civilization_sphere as is (欧美国)
with open('/opt/data/workspace/Protreptic/IL/DE-PHYS-001.json', 'w', encoding='utf-8') as f:
    json.dump(de_data, f, ensure_ascii=False, indent=2)

# US-PHYS-001
us_data = il_sci_data.copy()
us_data['code'] = 'US-PHYS-001'
us_data['nationality'] = '美国'
us_data['ethnicity'] = '美国'
# Keep civilization_sphere as is (欧美国)
with open('/opt/data/workspace/Protreptic/IL/US-PHYS-001.json', 'w', encoding='utf-8') as f:
    json.dump(us_data, f, ensure_ascii=False, indent=2)

# IR-MED-001 duplicates
ir_med_path = '/opt/data/workspace/Protreptic/tools/json/IR-MED-001.json'
with open(ir_med_path, 'r', encoding='utf-8') as f:
    ir_med_data = json.load(f)

# IR-MED-002 (Iran)
ir_data = ir_med_data.copy()
ir_data['code'] = 'IR-MED-002'
ir_data['nationality'] = '伊朗'
ir_data['ethnicity'] = '伊朗'
# Keep civilization_sphere as is (其他)
with open('/opt/data/workspace/Protreptic/tools/json/IR-MED-002.json', 'w', encoding='utf-8') as f:
    json.dump(ir_data, f, ensure_ascii=False, indent=2)

# ISLAM-MED-001 (Islamic civilization)
islam_data = ir_med_data.copy()
islam_data['code'] = 'ISLAM-MED-001'
islam_data['nationality'] = '伊斯兰文明'
islam_data['ethnicity'] = '伊斯兰文明'
# Keep civilization_sphere as is (其他)
with open('/opt/data/workspace/Protreptic/tools/json/ISLAM-MED-001.json', 'w', encoding='utf-8') as f:
    json.dump(islam_data, f, ensure_ascii=False, indent=2)

print('Created duplicate records:')
print('- IL/DE-PHYS-001.json')
print('- IL/US-PHYS-001.json')
print('- tools/json/IR-MED-002.json')
print('- tools/json/ISLAM-MED-001.json')