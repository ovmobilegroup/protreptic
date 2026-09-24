import json, os

workspace = "/opt/data/workspace/Protreptic/tools/json"
src_main = os.path.join(workspace, "H-MZ-001.json")
src_modes_file = os.path.join(workspace, "H-MZ-001_modes.json")

# Load source files
with open(src_main) as f:
    mz_main = json.load(f)

with open(src_modes_file) as f:
    mz_modes = json.load(f)

# Extract key info from source files
figure_name = mz_main.get("name_zh", "")  # "孟子"
code = mz_main.get("code", "")  # "H-MZ-001"
core_mode = mz_main.get("core_mode", "")  # "M01性善论法/M02推恩法/..."
description_zh = mz_main.get("description_zh", "")
reason_zh = mz_main.get("reason_zh", "")

# Era info from modes file
era = mz_modes.get("era", "")  # "战国"
school = mz_modes.get("school", "")  # "儒家"

# Build modes_data.json entry
modes_entry = {
    "code": code,
    "name": f"{figure_name}/{era}/{school}",
    "core_mode": core_mode,
    "new_mode": core_mode  # All new for Mencius
}

# Build main_data.json entry (for entries array)
main_entry = {
    "code": code,
    "name": figure_name,
    "region": era,
    "core_thinking_mode": core_mode,
    "new_mode": core_mode.split("/")[0] if "/" in core_mode else core_mode
}

# Build code_maps.json entry
code_map_entry = f"{figure_name}：{core_mode}"

# Now update each DB file
print("=== BEFORE ===")
with open(os.path.join(workspace, "modes_data.json")) as f:
    modes_db = json.load(f)

print(f"  modes_data.json entries before: {len(modes_db)}")
for e in modes_db[:3]:
    print(f"    {e.get('code')}: {str(e.get('name',''))[:60]}")

with open(os.path.join(workspace, "main_data.json")) as f:
    main_db = json.load(f)

entries_before = len(main_db.get("entries", []))
print(f"  main_data.json entries before: {entries_before}")

with open(os.path.join(workspace, "code_maps.json")) as f:
    maps_db = json.load(f)

maps_before = len(maps_db.get("CODE_MAP", {}))
print(f"  code_maps.json entries before: {maps_before}")

# === Merge into modes_data.json ===
modes_db.append(modes_entry)
with open(os.path.join(workspace, "modes_data.json"), "w") as f:
    json.dump(modes_db, f, ensure_ascii=False, indent=2)
print(f"\n  modes_data.json entries after: {len(modes_db)}")

# === Merge into main_data.json ===
if "entries" not in main_db:
    main_db["entries"] = []

# Check if code already exists (replace)
found_idx = None
for i, e in enumerate(main_db["entries"]):
    if e.get("code") == code:
        found_idx = i
        break

if found_idx is not None:
    main_db["entries"][found_idx] = main_entry
else:
    main_db["entries"].append(main_entry)

with open(os.path.join(workspace, "main_data.json"), "w") as f:
    json.dump(main_db, f, ensure_ascii=False, indent=2)

entries_after = len(main_db["entries"])
print(f"  main_data.json entries after: {entries_after}")

# === Merge into code_maps.json ===
if "CODE_MAP" not in maps_db:
    maps_db["CODE_MAP"] = {}

maps_db["CODE_MAP"][code] = code_map_entry
with open(os.path.join(workspace, "code_maps.json"), "w") as f:
    json.dump(maps_db, f, ensure_ascii=False, indent=2)

maps_after = len(maps_db["CODE_MAP"])
print(f"  code_maps.json entries after: {maps_after}")

# === Merge into scenarios_zh.json (if needed) ===
print("\n=== Checking if scenarios need Mencius entries ===")
with open(os.path.join(workspace, "scenarios_zh.json")) as f:
    sc_db = json.load(f)

# Check if there are any Mencius scenarios already
mz_in_sc = 0
for entry in sc_db:
    if isinstance(entry, dict):
        code = str(entry.get("code", ""))
        name = entry.get("figure_name", "") or entry.get("name", "") or ""
        if "MZ" in code.upper() or name == figure_name:
            mz_in_sc += 1

print(f"  Mencius entries in scenarios_zh.json: {mz_in_sc}")
print("\n=== MERGE COMPLETE ===")