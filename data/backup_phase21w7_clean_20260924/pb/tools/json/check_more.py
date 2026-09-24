import json

# Check scenario_tags in tools/json
with open('scenario_tags.json') as fp:
    d = json.load(fp)
print(f"scenario_tags.json (tools/json): {type(d)}")
if isinstance(d, dict):
    print(f"  keys: {list(d.keys())}")
    for k, v in d.items():
        if isinstance(v, (list, dict)):
            print(f"    {k}: {len(v)}")
        else:
            print(f"    {k}: {type(v)} = {v}")
elif isinstance(d, list):
    print(f"  list length: {len(d)}")

# Check modes_data in tools
with open('../modes_data.json') as fp:
    d = json.load(fp)
print(f"\nmodes_data.json (tools): {type(d)}")
if isinstance(d, dict):
    print(f"  keys: {list(d.keys())}")
    for k, v in d.items():
        if isinstance(v, (list, dict)):
            print(f"    {k}: {len(v)}")

# Check modes_data in tools/json
with open('modes_data.json') as fp:
    d = json.load(fp)
print(f"\nmodes_data.json (tools/json): {type(d)}")
if isinstance(d, dict):
    print(f"  keys: {list(d.keys())}")
    for k, v in d.items():
        if isinstance(v, (list, dict)):
            print(f"    {k}: {len(v)}")
elif isinstance(d, list):
    print(f"  list length: {len(d)}")