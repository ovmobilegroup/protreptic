import json
zh = json.load(open('/opt/data/workspace/Protreptic/tools/scenarios_zh.json'))
h_codes = [k for k in zh if k.startswith('H-')]
print(f'Total H- codes: {len(h_codes)}')
print(f'First 10: {h_codes[:10]}')