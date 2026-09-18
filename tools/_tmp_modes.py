import json
base = "/opt/data/workspace/Protreptic"
for p in ["tools/json/modes_data.json", "tools/modes_data.json", "data/modes_data.json"]:
    try:
        d = json.load(open(base + "/" + p))
        print("FILE", p, type(d).__name__, len(d) if hasattr(d, "__len__") else "")
        modes = None
        if isinstance(d, list):
            modes = d
        elif isinstance(d, dict):
            for k in ("modes", "data", "items"):
                if isinstance(d.get(k), list):
                    modes = d[k]; break
            if modes is None:
                # maybe mode dict indexed by id
                modes = [v for v in d.values() if isinstance(v, dict)]
        if modes:
            hits = [m for m in modes if isinstance(m, dict) and m.get("id") in (34, 39, 19, 37)]
            if hits:
                print("  HITS:", json.dumps(hits, ensure_ascii=False)[:1500])
    except Exception as e:
        print("ERR", p, e)
