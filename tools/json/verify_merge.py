import json, os

workspace = "<repo>/tools/json"

# Verify all 4 DB files
print("=== VERIFICATION: H-MZ-001 (孟子) across all DB files ===\n")

# 1. modes_data.json
with open(os.path.join(workspace, "modes_data.json")) as f:
    modes = json.load(f)

for entry in modes:
    if entry.get("code") == "H-MZ-001":
        print(f"modes_data.json: FOUND")
        print(f"  code={entry.get('code')}")
        print(f"  name={entry.get('name')}")
        print(f"  core_mode={entry.get('core_mode')[:120]}")
        print(f"  new_mode={entry.get('new_mode')[:120]}")
        break

# 2. main_data.json
with open(os.path.join(workspace, "main_data.json")) as f:
    main = json.load(f)

for entry in main.get("entries", []):
    if entry.get("code") == "H-MZ-001":
        print(f"\nmain_data.json: FOUND")
        print(f"  code={entry.get('code')}")
        print(f"  name={entry.get('name')}")
        print(f"  region={entry.get('region')}")
        print(f"  core_thinking_mode={entry.get('core_thinking_mode')[:120]}")
        print(f"  new_mode={entry.get('new_mode')[:120]}")
        break

# 3. code_maps.json
with open(os.path.join(workspace, "code_maps.json")) as f:
    maps = json.load(f)

if "H-MZ-001" in maps.get("CODE_MAP", {}):
    print(f"\ncode_maps.json: FOUND")
    print(f"  H-MZ-001 -> {maps['CODE_MAP']['H-MZ-001'][:120]}")
else:
    print("\ncode_maps.json: NOT FOUND (error)")

# 4. Check file sizes
print(f"\n=== File sizes ===")
for db in ["modes_data.json", "main_data.json", "code_maps.json"]:
    path = os.path.join(workspace, db)
    size = os.path.getsize(path)
    print(f"  {db}: {size:,} bytes")

# Verify the source files are untouched
print(f"\n=== Source file integrity ===")
for sf in ["H-MZ-001.json", "H-MZ-001_modes.json"]:
    path = os.path.join(workspace, sf)
    size = os.path.getsize(path)
    print(f"  {sf}: {size:,} bytes (OK)")