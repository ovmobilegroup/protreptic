import json

# Check the modes_data.json in t_99d75f2f/tools
with open('<internal>') as fp:
    d = json.load(fp)
print(f"modes_data.json (t_99d75f2f/tools): {type(d)}")
if isinstance(d, dict):
    for k, v in d.items():
        if isinstance(v, dict):
            print(f"  {k}: {len(v)} entries")
            # Find modes M480-M494
            for mode_key in v:
                if mode_key.startswith('M4') and int(mode_key[1:]) >= 480 and int(mode_key[1:]) <= 494:
                    print(f"    M480-M494: {mode_key}")

# Check scenarios_zh.json
with open('<internal>') as fp:
    d = json.load(fp)
print(f"\nscenarios_zh.json (t_99d75f2f/tools): {len(d)} entries")

# Check scenarios_en.json
with open('<internal>') as fp:
    d = json.load(fp)
print(f"scenarios_en.json (t_99d75f2f/tools): {len(d)} entries")

# Check code_maps.json
with open('<internal>') as fp:
    d = json.load(fp)
print(f"code_maps.json (t_99d75f2f/tools): CODE_MAP={len(d.get('CODE_MAP', {}))}, CODE_MAP_EN={len(d.get('CODE_MAP_EN', {}))}")

# Check scenario_tags.json if exists
import os
tags_path = '<internal>'
if os.path.exists(tags_path):
    with open(tags_path) as fp:
        d = json.load(fp)
    print(f"scenario_tags.json (t_99d75f2f/tools): {type(d)}, keys={len(d)}")