import json

# Check modes_data in tools/json - the 12 new modes
with open('modes_data.json') as fp:
    d = json.load(fp)
print(f"modes_data.json (tools/json): {type(d)}")
if isinstance(d, list):
    print(f"  list length: {len(d)}")
    for item in d:
        print(f"    {item}")