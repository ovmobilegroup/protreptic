import json
import re
with open('../scenarios_zh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
print(f"Total top-level keys: {len(data)}")
# Check first 10 keys
keys = list(data.keys())[:20]
print("First 20 keys:", keys)
# Check if they match scenario pattern
pattern = re.compile(r'^[A-Z]{2}-[A-Z]{3}-\d{3}$')
scenario_keys = []
other_keys = []
for k in data.keys():
    if pattern.match(k):
        scenario_keys.append(k)
    else:
        other_keys.append(k)
print(f"Scenario keys: {len(scenario_keys)}")
print(f"Other keys: {len(other_keys)}")
if other_keys:
    print("Other keys:", other_keys[:10])
