#!/usr/bin/env python3
import json

with open('/opt/data/workspace/Protreptic/scenarios_zh.json') as f:
    zh = json.load(f)
with open('/opt/data/workspace/Protreptic/scenarios_en.json') as f:
    en = json.load(f)

def is_scenario_entry(entry):
    return isinstance(entry, dict) and 'modes' in entry and isinstance(entry['modes'], list)

zh_dict = {k: v for k, v in zh.items() if is_scenario_entry(v)}
en_dict = {k: v for k, v in en.items() if is_scenario_entry(v)}

print('SCENARIOS_ZH total:', len(zh))
print('SCENARIOS_ZH dict:', len(zh_dict))
print('SCENARIOS_EN total:', len(en))
print('SCENARIOS_EN dict:', len(en_dict))