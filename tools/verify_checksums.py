#!/usr/bin/env python3
"""
Verify checksums of the 5 authoritative data files against release v2.0.0 reference values.
"""

import hashlib
import json

TOOLS_DIR = "/opt/data/workspace/Protreptic/tools"

reference = {
    "scenarios_zh.json": "eb7f0453525e34004780ff5502ea842e510551ac338a442f3bca3e9f1a4eeb70",
    "scenarios_en.json": "107173e433bec62c909f406202c163e992382d21d071cd062fa9050d09d0b44a",
    "code_maps.json": "af6080567f2f937b00ed446f0f526074b0e9d90694878f2d055430c91464781e",
    "modes_data.json": "517d35157584dceee4533d92acfa8365a461e5fac97fe7f98c65ccdb32da6849",
    "scenario_tags.json": "24d992f148ef081c0642b94d65c26d4984426dff85e37c299c39fdf9025b87ba"
}

def compute_sha256(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

print("=== Checksum Validation ===")
all_match = True
for filename, expected in reference.items():
    path = f"{TOOLS_DIR}/{filename}"
    actual = compute_sha256(path)
    match = actual == expected
    status = "✅ MATCH" if match else "❌ MISMATCH"
    print(f"{filename}: {status}")
    if not match:
        all_match = False
        print(f"  Expected: {expected}")
        print(f"  Actual:   {actual}")

print()
if all_match:
    print("All 5 checksums match exactly!")
else:
    print("Some checksums do not match!")
    sys.exit(1)