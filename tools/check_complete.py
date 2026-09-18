import json, random
from datetime import date

zh = json.load(open('/opt/data/workspace/Protreptic/tools/scenarios_zh.json'))
en = json.load(open('/opt/data/workspace/Protreptic/tools/scenarios_en.json'))
modes = json.load(open('/opt/data/workspace/Protreptic/tools/modes_data.json'))

# 1. 获取所有历史人物 H-* 代码
h_codes = [k for k in zh if k.startswith('H-')]

# Filter for figures with complete data (reason and case not empty/placeholder)
complete_h_codes = []
for k in h_codes:
    reason = zh[k].get('reason', '')
    case = zh[k].get('case', '')
    if reason and case and reason != '待完善...' and reason != '...' and case != '待完善...' and case != '...':
        complete_h_codes.append(k)

print(f"Total H- codes: {len(h_codes)}")
print(f"Complete H- codes: {len(complete_h_codes)}")
print(f"First 20 complete: {complete_h_codes[:20]}")