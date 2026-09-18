#!/usr/bin/env python3
"""Verify H-HLG-001 merge status"""
import json
import sys
sys.path.insert(0, '.')

from thinking_mode_selector import SCENARIOS_ZH, SCENARIOS_EN, MODES_DATA, CODE_MAP, CODE_MAP_EN

print(f"SCENARIOS_ZH entries: {len(SCENARIOS_ZH)}")
print(f"SCENARIOS_EN entries: {len(SCENARIOS_EN)}")
print(f"H-HLG-001 in zh: {'H-HLG-001' in SCENARIOS_ZH}")
print(f"H-HLG-001 in en: {'H-HLG-001' in SCENARIOS_EN}")

h_count_zh = sum(1 for k in SCENARIOS_ZH if k.startswith('H-') or k.startswith('M-'))
h_count_en = sum(1 for k in SCENARIOS_EN if k.startswith('H-') or k.startswith('M-'))
print(f"H/M count in zh: {h_count_zh}")
print(f"H/M count in en: {h_count_en}")

# Check if H-HLG-001 entry is a dict
if 'H-HLG-001' in SCENARIOS_ZH:
    entry = SCENARIOS_ZH['H-HLG-001']
    print(f"H-HLG-001 type: {type(entry).__name__}")
    if isinstance(entry, dict):
        print(f"H-HLG-001 keys: {list(entry.keys())}")
        print(f"H-HLG-001 modes: {entry.get('modes')}")

# Check CODE_MAP
print(f"CODE_MAP entries: {len(CODE_MAP)}")
print(f"H-HLG-001 in CODE_MAP: {'H-HLG-001' in CODE_MAP}")
print(f"H-HLG-001 in CODE_MAP_EN: {'H-HLG-001' in CODE_MAP_EN}")
