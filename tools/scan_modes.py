import json
import os

for root, dirs, files in os.walk('/opt/data/workspace/Protreptic'):
    for f in files:
        if f == 'modes_data.json':
            path = os.path.join(root, f)
            with open(path, 'r') as fp:
                d = json.load(fp)
            print(f"=== {path} ===")
            print(f"  type: {type(d)}")
            if isinstance(d, dict):
                print(f"  zh modes: {len(d.get('zh', {}))}")
                print(f"  en modes: {len(d.get('en', {}))}")
            else:
                print(f"  list len: {len(d)}")