import json

with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)
with open('code_maps.json', 'r', encoding='utf-8') as f:
    cm = json.load(f)
with open('scenario_tags.json', 'r', encoding='utf-8') as f:
    st = json.load(f)

cm_zh = set(cm.get('CODE_MAP', {}).keys())
st_codes = set(st.get('tags', {}).keys())

# Find entries in zh but not in cm_zh
missing_cm = [k for k in zh.keys() if k not in cm_zh]
print(f"Entries in zh but not in code_maps CODE_MAP ({len(missing_cm)}):")
for k in missing_cm[:30]:
    print(f"  {k}")

print(f"\nEntries in zh but not in scenario_tags ({len([k for k in zh.keys() if k not in st_codes])}):")
missing_st = [k for k in zh.keys() if k not in st_codes]
for k in missing_st[:30]:
    print(f"  {k}")

# Check structure of missing entries
print("\n=== STRUCTURE OF MISSING ENTRIES ===")
for k in missing_cm[:5]:
    v = zh[k]
    print(f"\n{k}:")
    print(f"  Type: {type(v)}")
    print(f"  Keys: {list(v.keys()) if isinstance(v, dict) else 'N/A'}")
    if isinstance(v, dict):
        for fk, fv in v.items():
            if isinstance(fv, str):
                print(f"  {fk}: {fv[:80]}...")
            else:
                print(f"  {fk}: {fv}")

# Check a few entries that ARE in code_maps
print("\n=== STRUCTURE OF PRESENT ENTRIES (in code_maps) ===")
present = [k for k in zh.keys() if k in cm_zh]
for k in present[:5]:
    v = zh[k]
    print(f"\n{k}:")
    print(f"  Type: {type(v)}")
    print(f"  Keys: {list(v.keys()) if isinstance(v, dict) else 'N/A'}")
    if isinstance(v, dict):
        for fk, fv in v.items():
            if isinstance(fv, str):
                print(f"  {fk}: {fv[:80]}...")
            else:
                print(f"  {fk}: {fv}")

# Check modes issue
print("\n=== NON-INTEGER MODES ===")
for k, v in zh.items():
    if isinstance(v, dict) and 'modes' in v:
        for m in v['modes']:
            if not isinstance(m, int):
                print(f"  {k}: mode {m} is {type(m)}")
                
# Check empty strings
print("\n=== EMPTY STRING FIELDS ===")
for k, v in zh.items():
    if isinstance(v, dict):
        for fk, fv in v.items():
            if isinstance(fv, str) and fv.strip() == '':
                print(f"  {k}.{fk} = ''")
                break