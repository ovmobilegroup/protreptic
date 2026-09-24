#!/usr/bin/env python3
"""Merge Li Zhi (李贽) M01-M10 data into 5 core database files."""

import json
from pathlib import Path

BASE = Path("/opt/data/workspace/Protreptic/tools/json")

def load_json(path):
    with open(BASE / path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(BASE / path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Load source files
modes_data = load_json("modes_data.json")  # flat list of mode entries
code_maps = load_json("code_maps.json")    # dict keyed by figure code

# Load Li Zhi source data
with open(BASE / "H-LZ-001.json", 'r', encoding='utf-8') as f:
    h_lz = json.load(f)

with open(BASE / "LZ-MODES-001.json", 'r', encoding='utf-8') as f:
    lz_modes = json.load(f)

print("=== Source Data Summary ===")
modes_list = lz_modes.get("modes", [])
print(f"Li Zhi has {len(modes_list)} modes: {[m['id'] for m in modes_list]}")
print(f"H-LZ-001 core_mode: {h_lz.get('core_mode', '')[:80]}...")
print(f"Current modes_data.json has {len(modes_data)} entries")

# Step 1: Append Li Zhi modes to modes_data.json (flat list)
print("\n=== Step 1: Appending Li Zhi entries to modes_data.json ===")
new_entries = []
for m in modes_list:
    mid = m['id']  # M01, M02, ..., M10
    name_zh = m.get('name_zh', '')
    code = f"LZ-{mid}"  # LZ-M01, LZ-M02, etc.
    
    entry = {
        "code": code,
        "name": f"李贽/{mid}: {name_zh}",
        "core_mode": f"M{mid[1:]} 李贽/{name_zh}",
        "new_mode": f"M{mid[1:]} 李贽/{name_zh}"
    }
    new_entries.append(entry)

modes_data.extend(new_entries)
save_json("modes_data.json", modes_data)
print(f"  -> Added {len(new_entries)} entries to modes_data.json")
for e in new_entries:
    print(f"     {e['code']}: {e['name']}")

# Step 2: Create/update H-LZ-169 in code_maps.json
print("\n=== Step 2: Creating/updating H-LZ-169 in code_maps.json ===")

lz_entry = {
    "figure": "Li Zhi (李贽)",
    "life_period": "1527-1602",
    "dynasty": "Ming Dynasty (明朝)",
    "figure_id": "H-LZ-169",
    "role_type": "Philosopher, Essayist, Historian (思想家、文学家、史学家)",
    "summary_zh": h_lz.get("description_zh", ""),
    "summary_en": h_lz.get("description_en", ""),
    "core_thinking_modes": [m['id'] for m in modes_list],
    "modes_detail": {},
    "key_life_events": [
        "1527年：出生于福建泉州晋江，航海贸易世家",
        "早年：考取举人后多年担任低微官职（河南辉县教谕、南京国子监博士等）",
        "中年：深受王阳明和泰州学派（罗汝芳）影响",
        "晚年：辞官，寄居湖北麻城芝佛院，从事写作和讲学十余年",
        "1602年：以'敢倡乱道、惑世诬民'罪名被捕入狱，自刎而死",
    ],
    "philosophical_contributions": [
        "童心说 (Childlike Mind Theory)",
        "穿衣吃饭即是人伦物理 (Material Ethics)",
        "不以孔子之是非为是非 (Anti-Authoritarian Epistemology)",
    ],
    "major_works": {
        "焚书 (Books That Burn)": "Essays and letters, radical critiques of Neo-Confucianism",
        "藏书 (Records to Be Hidden)": "Historical evaluations, redefining heroes and villains",
        "续焚书 (Continued Books That Burn)": "Further essays after first collection",
        "续藏书 (Continued Records to Be Hidden)": "Supplementary historical records"
    },
    "historical_impact_zh": h_lz.get("reason_zh", "")[:200] + "...",
    "historical_impact_en": h_lz.get("reason_en", "")[:200] + "...",
    "modern_relevance_zh": "对晚明思想启蒙、日本明治维新、五四新文化运动均产生深远影响",
    "modern_relevance_en": "Profoundly influenced late Ming intellectual enlightenment, Japan's Meiji Restoration, and China's May Fourth Movement",
    "relationships_zh": {
        "王阳明": "心学影响 - 思想来源",
        "罗汝芳": "泰州学派师承",
    },
}

# Add detailed mode mappings from LZ-MODES-001.json modes list
for m in modes_list:
    mid = m['id']  # M01, etc.
    lz_entry["modes_detail"][mid] = {
        "name_zh": m.get('name_zh', ''),
        "name_en": m.get('name_en', ''),
        "definition_zh": m.get('definition_zh', '')[:300],  # truncated for readability
        "key_concepts": m.get('key_concepts', []),
        "process_steps": m.get('process_steps', m.get('process', [])),
        "modern_applications": m.get('modern_applications', []),
        "source_chapter": m.get('source_chapter', ''),
    }

# Now update code_maps.json
if "H-LZ-169" in code_maps:
    print("  H-LZ-169 already exists, updating...")
else:
    print("  H-LZ-169 does not exist, creating new entry...")

code_maps["H-LZ-169"] = lz_entry
save_json("code_maps.json", code_maps)
print(f"  -> H-LZ-169 saved to code_maps.json")

# Step 3: Check scenario files (Li Zhi is historical/philosophical, not business)
print("\n=== Step 3: Checking scenario files ===")

try:
    with open(BASE / "scenario_tags.json", 'r', encoding='utf-8') as f:
        scenario_tags = json.load(f)
    print(f"  Current scenarios: {len(scenario_tags)} categories")
except (FileNotFoundError, json.JSONDecodeError):
    print("  No existing scenario_tags.json")

try:
    with open(BASE / "scenarios_zh.json", 'r', encoding='utf-8') as f:
        scenarios_zh = json.load(f)
    li_zi_refs = [k for k in scenarios_zh.keys() if 'LZ' in str(k)]
    print(f"  scenarios_zh.json: {len(scenarios_zh)} entries, Li Zhi refs: {li_zi_refs}")
except (FileNotFoundError, json.JSONDecodeError):
    print("  No existing scenarios_zh.json")

try:
    with open(BASE / "scenarios_en.json", 'r', encoding='utf-8') as f:
        scenarios_en = json.load(f)
    li_zi_refs_en = [k for k in scenarios_en.keys() if 'LZ' in str(k)]
    print(f"  scenarios_en.json: {len(scenarios_en)} entries, Li Zhi refs: {li_zi_refs_en}")
except (FileNotFoundError, json.JSONDecodeError):
    print("  No existing scenarios_en.json")

# Final verification
print("\n=== Verification ===")
modes_data = load_json("modes_data.json")
code_maps = load_json("code_maps.json")

li_zhi_modes = [e for e in modes_data if 'LZ-' in e.get('code', '')]
print(f"  Li Zhi entries in modes_data.json: {len(li_zhi_modes)}")
for e in li_zhi_modes[:3]:  # Show first 3 as sample
    print(f"     {e['code']}: {e['name']}")

print(f"  H-LZ-169 in code_maps.json: {'H-LZ-169' in code_maps}")
if 'H-LZ-169' in code_maps:
    print(f"  Figure: {code_maps['H-LZ-169'].get('figure', 'unknown')}")
    print(f"  Modes: {code_maps['H-LZ-169'].get('core_thinking_modes', [])}")
    print(f"  Modes detail keys: {list(code_maps['H-LZ-169'].get('modes_detail', {}).keys())}")

print("\n=== Done! Files Updated ===")