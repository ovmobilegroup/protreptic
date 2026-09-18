import json, sys

base = "/opt/data/workspace/Protreptic"

# Load mode catalog
for p in ["data/modes_data.json", "tools/modes_data.json"]:
    try:
        d = json.load(open(p))
        print("FILE", p, "type", type(d).__name__)
        modes = None
        if isinstance(d, dict):
            for k in ("modes", "data", "items"):
                if k in d and isinstance(d[k], list):
                    modes = d[k]
                    break
            if modes is None and d and all(isinstance(v, dict) for v in d.values()):
                modes = list(d.values())
        elif isinstance(d, list):
            modes = d
        if modes:
            for m in modes:
                if isinstance(m, dict) and m.get("id") in (34, 39, 19, 37):
                    print("  MODE", m.get("id"), "->", m.get("name") or m.get("name_zh") or m.get("name_en"))
    except Exception as e:
        print("ERR", p, e)

# Check code_maps for Singapore / Lee
print("\n=== code_maps scan ===")
try:
    cm = json.load(open(base + "/tools/json/code_maps.json"))
    print("code_maps type", type(cm).__name__, "len", len(cm) if hasattr(cm, "__len__") else "?")
    if isinstance(cm, dict):
        for k, v in cm.items():
            ks = str(k) + " " + str(v)
            if "LEE" in ks.upper() or "SINGAPORE" in ks.upper() or "SG" in ks.upper() or "李" in ks:
                print("  HIT", k, "=", v)
except Exception as e:
    print("ERR code_maps", e)
