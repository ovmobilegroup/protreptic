#!/usr/bin/env python3
"""
Mode Coverage Tracker — 追踪规划模式 vs 实际生成模式
用法: python mode_tracker.py
"""
import json
import sys
from pathlib import Path

TOOLS_DIR = Path("/opt/data/workspace/Protreptic/tools")

# Phase 17 规划模式 (来自 albo 的 modes_expansion_proposal_v5.md)
PLANNED_MODES = {
    # Phase 17.1: Pakistan (6)
    **{str(i): "Pakistan" for i in range(357, 363)},
    # Phase 17.2: Bangladesh/Sri Lanka/Nepal/Bhutan (10)
    **{str(i): "South Asia Deep" for i in range(363, 373)},
    # Phase 17.3: Yemen/Oman/Gulf (13)
    **{str(i): "Gulf/Yemen" for i in range(373, 386)},
    # Phase 17.4: West Africa/Sahel (12)
    **{str(i): "West Africa" for i in range(386, 398)},
    # Phase 17.5: Central Africa (9)
    **{str(i): "Central Africa" for i in range(398, 407)},
    # Phase 17.6: East Africa (10)
    **{str(i): "East Africa" for i in range(407, 417)},
    # Phase 17.7: Southern Africa (12)
    **{str(i): "Southern Africa" for i in range(417, 429)},
    # Phase 17.8: Andes/Southern Cone (13)
    **{str(i): "Andes/Southern Cone" for i in range(429, 442)},
    # Phase 17.9: Central America/Caribbean (14)
    **{str(i): "Central America/Caribbean" for i in range(442, 456)},
    # Phase 18-20 (remaining to 500)
    **{str(i): "Future Phases" for i in range(456, 501)},
}

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def track_coverage():
    modes_data = load_json(TOOLS_DIR / "modes_data.json")
    zh_modes = modes_data.get('zh', {})
    en_modes = modes_data.get('en', {})
    
    actual_modes = set(zh_modes.keys()) | set(en_modes.keys())
    planned_modes = set(PLANNED_MODES.keys())
    
    # 覆盖分析
    covered = planned_modes & actual_modes
    missing = planned_modes - actual_modes
    extra = actual_modes - planned_modes
    
    # 按阶段统计
    phase_stats = {}
    for mode_id, phase in PLANNED_MODES.items():
        if phase not in phase_stats:
            phase_stats[phase] = {'planned': 0, 'covered': 0}
        phase_stats[phase]['planned'] += 1
        if mode_id in covered:
            phase_stats[phase]['covered'] += 1
    
    print("=" * 60)
    print("MODE COVERAGE TRACKER")
    print("=" * 60)
    print(f"Planned total: {len(planned_modes)}")
    print(f"Actual total:  {len(actual_modes)}")
    print(f"Covered:       {len(covered)} ({len(covered)/len(planned_modes)*100:.1f}%)")
    print(f"Missing:       {len(missing)}")
    print(f"Extra:         {len(extra)}")
    print()
    
    print("By Phase:")
    print("-" * 60)
    for phase, stats in sorted(phase_stats.items()):
        pct = stats['covered'] / stats['planned'] * 100 if stats['planned'] > 0 else 0
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        print(f"  {phase:25s} {stats['covered']:3d}/{stats['planned']:3d} ({pct:5.1f}%) {bar}")
    
    print()
    if missing:
        print("Missing Modes (first 30):")
        for m in sorted(missing)[:30]:
            print(f"  M{m}: {PLANNED_MODES[m]}")
        if len(missing) > 30:
            print(f"  ... and {len(missing) - 30} more")
    
    print()
    if extra:
        print(f"Extra modes (not in plan): {sorted(extra)[:20]}")
    
    # 生成 CSV 报告
    report_path = TOOLS_DIR / "mode_coverage_report.csv"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("mode_id,phase,status\n")
        for mode_id in sorted(planned_modes, key=int):
            status = "COVERED" if mode_id in covered else "MISSING"
            f.write(f"{mode_id},{PLANNED_MODES[mode_id]},{status}\n")
    print(f"\nCSV report saved to: {report_path}")
    
    return len(missing) == 0

if __name__ == '__main__':
    import json
    ok = track_coverage()
    sys.exit(0 if ok else 1)