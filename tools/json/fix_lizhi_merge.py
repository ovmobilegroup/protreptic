#!/usr/bin/env python3
"""Fix Li Zhi data merge: correct H-LZ-169 to H-LZ-001 and update modes_data.json."""

import json
from pathlib import Path

BASE = Path("/opt/data/workspace/Protreptic/tools/json")

print("=" * 60)
print("李贽数据修复")
print("=" * 60)

# 1. 读取源数据
print("\n【1】读取源数据")
with open(BASE / "H-LZ-001.json", 'r', encoding='utf-8') as f:
    h_lz = json.load(f)
with open(BASE / "LZ-MODES-001.json", 'r', encoding='utf-8') as f:
    lz_modes = json.load(f)

print(f"  H-LZ-001.json: {len(h_lz)} keys")
print(f"  LZ-MODES-001.json: {len(lz_modes.get('modes', []))} modes, schema: {lz_modes.get('schema_version')}")

# 2. 修复modes_data.json - 添加H-LZ-001条目
print("\n【2】修复modes_data.json")
with open(BASE / "modes_data.json", 'r', encoding='utf-8') as f:
    modes_data = json.load(f)

# 移除旧的LZ-M01~LZ-M10条目
old_lz_codes = [f"LZ-{mid}" for mid in ['M01', 'M02', 'M03', 'M04', 'M05', 'M06', 'M07', 'M08', 'M09', 'M10']]
modes_data = [e for e in modes_data if e.get('code', '') not in old_lz_codes]
print(f"  移除旧条目: {old_lz_codes}")
print(f"  剩余条目数: {len(modes_data)}")

# 添加新的H-LZ-001条目（按孔子格式）
new_entry = {
    "code": "H-LZ-001",
    "name_zh": h_lz.get("name_zh", "李贽"),
    "name_en": h_lz.get("name_en", "Li Zhi"),
    "core_mode": h_lz.get("core_mode", ""),
    "new_mode": h_lz.get("core_mode", ""),
    "description_zh": h_lz.get("description_zh", ""),
    "description_en": h_lz.get("description_en", ""),
    "reason_zh": h_lz.get("reason_zh", ""),
    "reason_en": h_lz.get("reason_en", ""),
    "modes": lz_modes.get("modes", []),
    "steps_zh": [],
    "steps_en": [],
    "expected_zh": [],
    "expected_en": [],
    "tags": [],
    "related_mode_codes": [f"M{str(i)[1:]}" for i in range(1, 11)]
}
modes_data.append(new_entry)
print(f"  添加H-LZ-001条目")

with open(BASE / "modes_data.json", 'w', encoding='utf-8') as f:
    json.dump(modes_data, f, ensure_ascii=False, indent=2)
print(f"  保存完成，总条目数: {len(modes_data)}")

# 3. 修复code_maps.json
print("\n【3】修复code_maps.json")
with open(BASE / "code_maps.json", 'r', encoding='utf-8') as f:
    code_maps = json.load(f)

# 获取CODE_MAP
if isinstance(code_maps, dict) and 'CODE_MAP' in code_maps:
    cm = code_maps['CODE_MAP']
else:
    cm = code_maps

# 如果H-LZ-169存在，重命名为H-LZ-001
if 'H-LZ-169' in cm:
    print(f"  重命名 H-LZ-169 -> H-LZ-001")
    cm['H-LZ-001'] = cm.pop('H-LZ-169')
elif 'H-LZ-001' not in cm:
    print(f"  警告：H-LZ-001不存在，需要创建")
    # 创建新条目
    cm['H-LZ-001'] = {
        "figure": "Li Zhi (李贽)",
        "life_period": "1527-1602",
        "dynasty": "Ming Dynasty (明朝)",
        "figure_id": "H-LZ-001",
        "role_type": "Philosopher, Essayist, Historian (思想家、文学家、史学家)",
        "summary_zh": h_lz.get("description_zh", ""),
        "summary_en": h_lz.get("description_en", ""),
        "core_thinking_modes": [m['id'] for m in lz_modes.get('modes', [])],
        "modes_detail": {},
        "key_life_events": [
            "1527年：出生于福建泉州晋江，航海贸易世家",
            "早年：考取举人后多年担任低微官职",
            "中年：深受王阳明和泰州学派影响",
            "晚年：辞官，寄居湖北麻城芝佛院",
            "1602年：以'敢倡乱道、惑世诬民'罪名被捕入狱，自刎而死"
        ],
        "philosophical_contributions": [
            "童心说 (Childlike Mind Theory)",
            "穿衣吃饭即是人伦物理 (Material Ethics)",
            "不以孔子之是非为是非 (Anti-Authoritarian Epistemology)"
        ],
        "major_works": {
            "焚书 (Books That Burn)": "Essays and letters",
            "藏书 (Records to Be Hidden)": "Historical evaluations"
        }
    }

with open(BASE / "code_maps.json", 'w', encoding='utf-8') as f:
    json.dump(code_maps, f, ensure_ascii=False, indent=2)
print(f"  保存完成")

# 4. 修复scenario_tags.json
print("\n【4】修复scenario_tags.json")
with open(BASE / "scenario_tags.json", 'r', encoding='utf-8') as f:
    tags = json.load(f)

if 'H-LZ-169' in tags:
    print(f"  重命名 H-LZ-169 -> H-LZ-001")
    tags['H-LZ-001'] = tags.pop('H-LZ-169')
elif 'H-LZ-001' not in tags:
    print(f"  警告：H-LZ-001不存在")

with open(BASE / "scenario_tags.json", 'w', encoding='utf-8') as f:
    json.dump(tags, f, ensure_ascii=False, indent=2)
print(f"  保存完成")

# 5. 修复scenarios_zh.json
print("\n【5】修复scenarios_zh.json")
with open(BASE / "scenarios_zh.json", 'r', encoding='utf-8') as f:
    zh = json.load(f)

if 'H-LZ-169' in zh:
    print(f"  重命名 H-LZ-169 -> H-LZ-001")
    zh['H-LZ-001'] = zh.pop('H-LZ-169')
elif 'H-LZ-001' not in zh:
    print(f"  警告：H-LZ-001不存在")

with open(BASE / "scenarios_zh.json", 'w', encoding='utf-8') as f:
    json.dump(zh, f, ensure_ascii=False, indent=2)
print(f"  保存完成")

# 6. 修复scenarios_en.json
print("\n【6】修复scenarios_en.json")
with open(BASE / "scenarios_en.json", 'r', encoding='utf-8') as f:
    en = json.load(f)

if 'H-LZ-169' in en:
    print(f"  重命名 H-LZ-169 -> H-LZ-001")
    en['H-LZ-001'] = en.pop('H-LZ-169')
elif 'H-LZ-001' not in en:
    print(f"  警告：H-LZ-001不存在")

with open(BASE / "scenarios_en.json", 'w', encoding='utf-8') as f:
    json.dump(en, f, ensure_ascii=False, indent=2)
print(f"  保存完成")

# 7. 最终验证
print("\n【7】最终验证")
with open(BASE / "modes_data.json", 'r') as f:
    md = json.load(f)
lz_md = [e for e in md if e.get('code') == 'H-LZ-001']
print(f"  modes_data.json: H-LZ-001存在={len(lz_md)>0}, modes={len(lz_md[0].get('modes', [])) if lz_md else 0}")

with open(BASE / "code_maps.json", 'r') as f:
    cm = json.load(f)
if isinstance(cm, dict) and 'CODE_MAP' in cm:
    cm = cm['CODE_MAP']
lz_cm = cm.get('H-LZ-001', None)
print(f"  code_maps.json: H-LZ-001存在={lz_cm is not None}")

with open(BASE / "scenario_tags.json", 'r') as f:
    tg = json.load(f)
lz_tg = tg.get('H-LZ-001', None)
print(f"  scenario_tags.json: H-LZ-001存在={lz_tg is not None}, tags={len(lz_tg.get('tags', [])) if lz_tg else 0}")

with open(BASE / "scenarios_zh.json", 'r') as f:
    zh2 = json.load(f)
lz_zh = zh2.get('H-LZ-001', None)
print(f"  scenarios_zh.json: H-LZ-001存在={lz_zh is not None}, steps={len(lz_zh.get('steps', [])) if lz_zh else 0}")

with open(BASE / "scenarios_en.json", 'r') as f:
    en2 = json.load(f)
lz_en = en2.get('H-LZ-001', None)
print(f"  scenarios_en.json: H-LZ-001存在={lz_en is not None}, steps={len(lz_en.get('steps', [])) if lz_en else 0}")

print("\n" + "=" * 60)
print("修复完成")
print("=" * 60)
