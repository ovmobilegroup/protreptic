import json, os

workspace = "<repo>/tools/json"

# Check what the previous task for Zhu Xi (H-ZZ-001) did
print("=== Checking main_data.json for H-ZZ-001 (Zhu Xi) ===")
with open(os.path.join(workspace, "main_data.json")) as f:
    main = json.load(f)

for entry in main.get("entries", []):
    code = entry.get("code","")
    if "ZZ" in code or (entry.get("name","") == "朱熹"):
        print(f"  Found: {json.dumps(entry, ensure_ascii=False)[:300]}")

print("\n=== Checking modes_data.json for H-ZZ-001 (Zhu Xi) ===")
with open(os.path.join(workspace, "modes_data.json")) as f:
    modes = json.load(f)

for entry in modes:
    code = entry.get("code","")
    if "ZZ" in code or ("朱熹" in str(entry.get("name",""))):
        print(f"  Found: code={code}, name={str(entry.get('name',''))[:60]}, core_mode={entry.get('core_mode','')[:120]}")

print("\n=== Checking code_maps.json for H-ZZ-001 (Zhu Xi) ===")
with open(os.path.join(workspace, "code_maps.json")) as f:
    maps = json.load(f)

if "H-ZZ-001" in maps.get("CODE_MAP", {}):
    print(f"  H-ZZ-001 -> {maps['CODE_MAP']['H-ZZ-001']}")
else:
    print("  H-ZZ-001 NOT in code_maps.json")

# Check scenarios_zh for Mencius-related 
print("\n=== Checking if H-MZ-001 exists in any DB ===")
for db_name, path in [("modes_data", "modes_data.json"), ("main_data", "main_data.json")]:
    with open(os.path.join(workspace, path)) as f:
        data = json.load(f)
    found = False
    
    if db_name == "modes_data":
        for entry in data:
            if entry.get("code") == "H-MZ-001":
                found = True
                break
    
    elif db_name == "main_data":
        for entry in data.get("entries", []):
            if entry.get("code") == "H-MZ-001":
                found = True
                break
    
    print(f"  {db_name}: H-MZ-001 {'FOUND' if found else 'NOT FOUND'}")

# Also check code_maps
with open(os.path.join(workspace, "code_maps.json")) as f:
    maps = json.load(f)

if "H-MZ-001" in maps.get("CODE_MAP", {}):
    print(f"  code_maps: H-MZ-001 FOUND")
else:
    print(f"  code_maps: H-MZ-001 NOT FOUND")

# Now let's see what modes_data.json looks like for a similar Chinese figure (e.g., 孔子)
print("\n=== Looking at CN-MA entries in modes_data.json ===")
with open(os.path.join(workspace, "modes_data.json")) as f:
    modes = json.load(f)

for entry in modes:
    code = entry.get("code","")
    if "CN-MA" in code:  # Confucius (Kongzi)
        print(f"  {code}: name={str(entry.get('name',''))[:80]}, core_mode={entry.get('core_mode','')[:120]}")