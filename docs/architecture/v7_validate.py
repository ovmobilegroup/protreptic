import json, os, glob
from collections import Counter

BASE = "<repo>"
SCHEMA = os.path.join(BASE, "docs/architecture/v7_schema.json")
SKIP = {"main_data.json","modes_data.json","code_maps.json","scenario_tags.json",
        "scenarios_en.json","scenarios_zh.json","verification_check.json",
        "code_maps_en.json","phase2_candidates_summary.json"}

schema = json.load(open(SCHEMA))
required = set(schema["required"])
props = schema["properties"]
enum_map = {k: v["enum"] for k, v in props.items() if "enum" in v}
pat = props.get("code", {}).get("pattern")
DEPRECATED = set(schema.get("deprecated", {}).get("fields", []))
COND = schema["allOf"]

# ---- load corpus ----
recs = []
for f in glob.glob(os.path.join(BASE, "*.json")) + glob.glob(os.path.join(BASE, "data", "*.json")):
    if os.path.basename(f) in SKIP:
        continue
    try:
        d = json.load(open(f))
    except Exception:
        continue
    items = [d] if isinstance(d, dict) else (d if isinstance(d, list) else [])
    for it in items:
        if isinstance(it, dict) and "code" in it and ("name_zh" in it or "name_en" in it):
            recs.append((f, it))

ERRORS = []        # list of (code, field, msg)
MISSING_DEP = Counter()
NONENUM = Counter()
DEAD_V6 = Counter()

for f, r in recs:
    code = r.get("code", "?")
    # required core
    for fld in required:
        v = r.get(fld)
        if v in (None, "", [], {}):
            ERRORS.append((code, fld, "missing required"))
    # code pattern
    if pat and "code" in r and not __import__("re").fullmatch(pat, str(r["code"])):
        ERRORS.append((code, "code", "pattern mismatch"))
    # enums (only complain when non-empty & not in enum)
    for fld, allowed in enum_map.items():
        v = r.get(fld)
        if v in (None, "", []):
            continue
        if isinstance(v, list):
            for x in v:
                if str(x) not in allowed:
                    NONENUM[(fld, str(x))] += 1
        else:
            if str(v) not in allowed:
                NONENUM[(fld, str(v))] += 1
    # deprecated v6 still present
    for dd in DEPRECATED:
        if dd in r and r[dd] not in (None, "", []):
            DEAD_V6[dd] += 1
    # conditional entity_type
    et = r.get("entity_type")
    if et is None:
        # infer from code for gap analysis
        et = "figure" if not str(r.get("code","")).startswith("M") else "mode"
    for cond in COND:
        if cond["if"]["properties"]["entity_type"]["const"] == et:
            for fld in cond["then"]["required"]:
                if r.get(fld) in (None, "", []):
                    MISSING_DEP[(et, fld)] += 1

print(f"CORPUS RECORDS VALIDATED: {len(recs)}")
print(f"HARD ERRORS (missing required/pattern): {len(ERRORS)}")
bycode = Counter(e[0] for e in ERRORS)
print(f"  records with >=1 hard error: {len(bycode)}")
for c, n in bycode.most_common(10):
    print(f"    {c}: {n} error(s)")

print("\n=== CONDITIONAL REQUIRED GAPS (entity_type-derived) ===")
for (et, fld), n in MISSING_DEP.most_common():
    print(f"  [{et}] missing {fld}: {n} records")

print("\n=== NON-ENUM VALUES (must be normalized for v7) ===")
for (fld, val), n in NONENUM.most_common(20):
    print(f"  {fld} = {val!r}: {n}")

print("\n=== DEPRECATED v6 FIELDS STILL PRESENT (retire/migrate) ===")
for fld, n in DEAD_V6.most_common():
    print(f"  {fld}: {n} records (retire in v7)")

# gap vs legacy_type enum
print("\n=== legacy_type current values (v7 adds economic/spiritual/unknown) ===")
lt = Counter(str(r.get("legacy_type")) for f in recs for _, r in [(f, None)] if False)
lt = Counter()
for f, r in recs:
    lt[str(r.get("legacy_type"))] += 1
for k, n in lt.most_common():
    print(f"  {k!r}: {n}")
