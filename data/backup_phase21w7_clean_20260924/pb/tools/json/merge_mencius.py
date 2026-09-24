import json, os, sys

workspace = "/opt/data/workspace/Protreptic/tools/json"
src_main = os.path.join(workspace, "H-MZ-001.json")
src_modes = os.path.join(workspace, "H-MZ-001_modes.json")

# Load source files
with open(src_main) as f:
    mz_main = json.load(f)

with open(src_modes) as f:
    mz_modes = json.load(f)

print("=== H-MZ-001.json keys ===")
for k in mz_main:
    v = mz_main[k]
    if isinstance(v, list) and len(str(v)) > 100:
        print(f"  {k}: list[{len(v)}] (truncated)")
    elif isinstance(v, str) and len(str(v)) > 100:
        print(f"  {k}: str[{len(str(v))}]")
    else:
        print(f"  {k}: {v}")

print("\n=== H-MZ-001_modes.json keys ===")
for k in mz_modes:
    v = mz_modes[k]
    if isinstance(v, list):
        print(f"  {k}: list[{len(v)}]")
    elif isinstance(v, str) and len(str(v)) > 100:
        print(f"  {k}: str[{len(str(v))}]")
    else:
        print(f"  {k}: {v}")

# Check existing DB files for H-MZ-001
for db in ["modes_data.json", "main_data.json", "code_maps.json"]:
    path = os.path.join(workspace, db)
    with open(path) as f:
        data = json.load(f)
    found = False
    
    if db == "modes_data.json":
        for entry in data:
            if entry.get("code") == "H-MZ-001":
                print(f"\n=== {db}: H-MZ-001 found ===")
                print(f"  code={entry.get('code')}, name={str(entry.get('name',''))[:80]}, core_mode={entry.get('core_mode','')[:120]}")
                found = True
    
    elif db == "main_data.json":
        for entry in data.get("entries", []):
            if entry.get("code") == "H-MZ-001":
                print(f"\n=== {db}: H-MZ-001 found ===")
                print(f"  code={entry.get('code')}, name={str(entry.get('name',''))[:80]}")
                found = True
    
    elif db == "code_maps.json":
        if "H-MZ-001" in data.get("CODE_MAP", {}):
            print(f"\n=== {db}: H-MZ-001 found ===")
            print(f"  H-MZ-001 -> {data['CODE_MAP']['H-MZ-001'][:120]}")
            found = True
    
    if not found:
        print(f"\n=== {db}: H-MZ-001 NOT FOUND ===")

# Check if there's a 4th DB file (scenarios)
print("\n=== Checking scenarios_zh.json for H-MZ-001 ===")
with open(os.path.join(workspace, "scenarios_zh.json")) as f:
    sc = json.load(f)
found_sc = 0
for entry in sc:
    if isinstance(entry, dict):
        code = entry.get("code", "") or entry.get("figure_code", "") or ""
        if "MZ" in code.upper() or entry.get("figure_name", "") == "孟子":
            found_sc += 1
print(f"  Found {found_sc} Mencius entries in scenarios_zh.json")

# Also check for H-MZ-001 specifically
for entry in sc:
    if isinstance(entry, dict):
        code = str(entry.get("code", ""))
        name = entry.get("figure_name", "") or entry.get("name", "") or ""
        if "MZ" in code.upper():
            print(f"  Found: {code} / {name}")

# Check what the previous successful merge (Zhu Xi) did
print("\n=== Checking Zhu Xi (H-ZX-001?) or similar recent merges ===")
for db in ["modes_data.json", "main_data.json"]:
    path = os.path.join(workspace, db)
    with open(path) as f:
        data = json.load(f)
    
    if db == "modes_data.json":
        for entry in data:
            code = entry.get("code", "")
            if "MZ" in code or (entry.get("core_mode","").find("性善") != -1):
                print(f"  {db}: Found Mencius-related: code={code}, core_mode={entry.get('core_mode','')[:100]}")

    elif db == "main_data.json":
        for entry in data.get("entries", []):
            code = entry.get("code","")
            if "MZ" in code:
                print(f"  {db}: Found Mencius-related: code={code}")

# Check modes_data for any H-MZ entries
print("\n=== Scanning all of modes_data.json for MZ ===")
with open(os.path.join(workspace, "modes_data.json")) as f:
    modes = json.load(f)
for i, entry in enumerate(modes):
    code = entry.get("code", "")
    if "MZ" in code:
        print(f"  [{i}] {code}: core_mode={entry.get('core_mode','')[:100]}")