import json

for f in ['scenarios_zh.json', 'scenarios_en.json', 'code_maps.json', 'scenario_tags.json', 'modes_data.json']:
    with open(f) as fp:
        d = json.load(fp)
    if isinstance(d, dict):
        print(f'{f}: {len(d)} keys')
        if 'zh' in d:
            print(f'  zh: {len(d["zh"])}')
        if 'en' in d:
            print(f'  en: {len(d["en"])}')
        if 'CODE_MAP' in d:
            print(f'  CODE_MAP: {len(d["CODE_MAP"])}')
        if 'CODE_MAP_EN' in d:
            print(f'  CODE_MAP_EN: {len(d["CODE_MAP_EN"])}')
    elif isinstance(d, list):
        print(f'{f}: {len(d)} items')