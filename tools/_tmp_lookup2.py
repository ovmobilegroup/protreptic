import json

base = "/opt/data/workspace/Protreptic"

# modes_data.json list
d = json.load(open(base + "/data/modes_data.json"))
print("modes_data.json is list, len", len(d))
# inspect first element keys
if isinstance(d, list) and d:
    print("sample keys:", list(d[0].keys()) if isinstance(d[0], dict) else type(d[0]))
    for m in d:
        if isinstance(m, dict) and m.get("id") in (34, 39, 19, 37):
            print("MODE", m.get("id"), "->", json.dumps({k: m.get(k) for k in ("id","name","name_zh","name_en","cn","en") if k in m}, ensure_ascii=False))

# Also check tools/modes_data.json dict
dm = json.load(open(base + "/tools/modes_data.json"))
print("\ntools/modes_data.json type", type(dm).__name__)
if isinstance(dm, dict):
    for k in ("modes","data","items"):
        if k in dm:
            print("  key", k, "len", len(dm[k]))
    # maybe top-level has mode list
    if "mode" in dm or "modes" in dm:
        print("  has modes key")
