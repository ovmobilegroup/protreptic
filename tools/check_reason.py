import json

zh = json.load(open('/opt/data/workspace/Protreptic/tools/scenarios_zh.json'))

# Check a few "complete" codes
for code in ['H-LB-01', 'H-WJL-199', 'H-LX-02', 'H-LS-03']:
    entry = zh[code]
    print(f"=== {code} ===")
    print(f"name: {entry['name']}")
    print(f"reason: '{entry.get('reason', '')[:100]}'")
    print(f"case: '{entry.get('case', '')[:100]}'")
    print()