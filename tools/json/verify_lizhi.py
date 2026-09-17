#!/usr/bin/env python3
"""Verify Li Zhi merge results."""

import json
from pathlib import Path

BASE = Path("<repo>/tools/json")

with open(BASE / "modes_data.json", 'r') as f:
    md = json.load(f)

lz_entries = [e for e in md if 'LZ-' in e.get('code', '')]
print(f"modes_data.json: {len(md)} total entries, {len(lz_entries)} Li Zhi")
for e in lz_entries:
    print(f"  {e['code']}: core_mode={e.get('core_mode', '')[:50]}")

with open(BASE / "code_maps.json", 'r') as f:
    cm = json.load(f)

lz169 = cm.get("H-LZ-169", {})
print(f"\ncode_maps.json: {len(cm)} figures, H-LZ-169 exists: {'H-LZ-169' in cm}")
if lz169:
    print(f"  Figure: {lz169.get('figure', 'unknown')}")
    print(f"  Modes detail count: {len(lz169.get('modes_detail', {}))}")
    print(f"  Major works: {list(lz169.get('major_works', {}).keys())}")
    print(f"  Key events: {len(lz169.get('key_life_events', []))} events")
    print(f"  Philosophy contributions: {len(lz169.get('philosophical_contributions', []))}")

import os
for fn in ['modes_data.json', 'code_maps.json']:
    sz = os.path.getsize(BASE / fn)
    print(f"\n  {fn}: {sz:,} bytes")