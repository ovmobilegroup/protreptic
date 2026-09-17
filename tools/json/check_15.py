import json

# Check the 15 items in tools/json/scenarios_zh.json
with open('scenarios_zh.json') as fp:
    d = json.load(fp)
print(f"scenarios_zh.json (tools/json): {type(d)}, length={len(d)}")
if isinstance(d, list):
    for item in d:
        print(f"  {item}")
elif isinstance(d, dict):
    for k, v in d.items():
        print(f"  {k}: {v}")

print()

# Check the 15 items in tools/json/scenarios_en.json
with open('scenarios_en.json') as fp:
    d = json.load(fp)
print(f"scenarios_en.json (tools/json): {type(d)}, length={len(d)}")
if isinstance(d, list):
    for item in d:
        print(f"  {item}")
elif isinstance(d, dict):
    for k, v in d.items():
        print(f"  {k}: {v}")

print()

# Check the 15 keys in tools/json/code_maps.json
with open('code_maps.json') as fp:
    d = json.load(fp)
print(f"code_maps.json (tools/json): {type(d)}, length={len(d)}")
if isinstance(d, dict):
    for k, v in d.items():
        print(f"  {k}: {v}")