import json
import os

# Check all the regional modes files
modes_files = [
    '/opt/data/workspace/Protreptic/data/arctic/arctic_modes.json',
    '/opt/data/workspace/Protreptic/data/latam/latam_modes.json',
    '/opt/data/workspace/Protreptic/data/oceania/oceania_modes.json',
    '/opt/data/workspace/Protreptic/data/africa/africa_modes.json',
]

for fpath in modes_files:
    if os.path.exists(fpath):
        print(f"\n=== {fpath} ===")
        with open(fpath, 'r') as f:
            data = json.load(f)
        print(f"Type: {type(data)}")
        if isinstance(data, dict):
            print(f"Keys: {list(data.keys())}")
            if 'modes' in data:
                print(f"modes is array of {len(data['modes'])} items")
                for i, mode in enumerate(data['modes'][:2]):
                    print(f"  [{i}]: {type(mode)} - keys: {list(mode.keys()) if isinstance(mode, dict) else 'not dict'}")
            for k, v in data.items():
                if k != 'modes':
                    print(f"  {k}: {type(v)}")
        elif isinstance(data, list):
            print(f"Array of {len(data)} items")
            for i, item in enumerate(data[:2]):
                print(f"  [{i}]: {type(item)} - keys: {list(item.keys()) if isinstance(item, dict) else 'not dict'}")
    else:
        print(f"\n=== {fpath} === NOT FOUND")