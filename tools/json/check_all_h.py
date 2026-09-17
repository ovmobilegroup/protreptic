import json, os

workspace = "<repo>/tools/json"

# Check all H-* files in DBs
print("=== Checking modes_data.json for ALL H-* entries ===")
with open(os.path.join(workspace, "modes_data.json")) as f:
    modes = json.load(f)

h_entries = []
for entry in modes:
    code = entry.get("code","")
    if code.startswith("H-"):
        h_entries.append(entry)

print(f"  Found {len(h_entries)} H-* entries in modes_data.json:")
for e in h_entries[:20]:  # First 20
    print(f"    {e.get('code')}: name={str(e.get('name',''))[:50]}, core_mode={str(e.get('core_mode',''))[:80]}")
if len(h_entries) > 20:
    print(f"    ... and {len(h_entries)-20} more")

print("\n=== Checking main_data.json for ALL H-* entries ===")
with open(os.path.join(workspace, "main_data.json")) as f:
    main = json.load(f)

h_main = []
for entry in main.get("entries", []):
    code = entry.get("code","")
    if code.startswith("H-"):
        h_main.append(entry)

print(f"  Found {len(h_main)} H-* entries in main_data.json:")
for e in h_main[:20]:
    print(f"    {e.get('code')}: name={str(e.get('name',''))[:50]}")
if len(h_main) > 20:
    print(f"    ... and {len(h_main)-20} more")

print("\n=== Checking code_maps.json for H-* entries ===")
with open(os.path.join(workspace, "code_maps.json")) as f:
    maps = json.load(f)

h_maps = {k:v for k,v in maps.get("CODE_MAP",{}).items() if k.startswith("H-")}
print(f"  Found {len(h_maps)} H-* entries in code_maps.json:")
for k,v in list(h_maps.items())[:20]:
    print(f"    {k} -> {v[:80]}")

# Check scenarios_zh.json for Mencius
print("\n=== Checking scenarios_zh.json for H-MZ ===")
with open(os.path.join(workspace, "scenarios_zh.json")) as f:
    sc = json.load(f)

mz_sc = 0
for entry in sc:
    if isinstance(entry, dict):
        code = str(entry.get("code",""))
        name = entry.get("figure_name", "") or ""
        if "MZ" in code.upper():
            mz_sc += 1

print(f"  Found {mz_sc} Mencius entries in scenarios_zh.json")