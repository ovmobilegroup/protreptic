import json
zh = json.load(open('/opt/data/workspace/Protreptic/tools/scenarios_zh.json'))
en = json.load(open('/opt/data/workspace/Protreptic/tools/scenarios_en.json'))

# Check a historical figure
code = 'H-LB-01'
print(f"=== {code} ===")
print(json.dumps(zh[code], ensure_ascii=False, indent=2))
print()
print(json.dumps(en[code], ensure_ascii=False, indent=2))

# Check modern scenarios
modern_codes = [k for k in zh if not k.startswith('H-')]
print(f"\nModern codes: {modern_codes}")