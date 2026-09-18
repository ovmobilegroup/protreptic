#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
sys.path.insert(0, 'workspaces/t_99d75f2f/tools')

from test_thinking_mode_selector import (
    test_scenarios_zh, test_scenarios_en, test_modes_data, test_code_maps, 
    test_bilingual_consistency, test_modes_coverage, test_new_batch_figures, 
    test_cli_list, test_cli_query, test_cli_search, test_cli_export, test_cli_tag_filter
)

print("Running tests...")

# Test individual components
tests = [
    ("test_scenarios_zh", test_scenarios_zh),
    ("test_scenarios_en", test_scenarios_en),
    ("test_modes_data", test_modes_data),
    ("test_code_maps", test_code_maps),
    ("test_bilingual_consistency", test_bilingual_consistency),
    ("test_modes_coverage", test_modes_coverage),
    ("test_new_batch_figures", test_new_batch_figures),
    ("test_cli_list", test_cli_list),
    ("test_cli_query", test_cli_query),
    ("test_cli_search", test_cli_search),
    ("test_cli_export", test_cli_export),
    ("test_cli_tag_filter", test_cli_tag_filter),
]

passed = []
failed = []

for test_name, test_func in tests:
    try:
        test_func()
        print(f"✓ {test_name} passed")
        passed.append(test_name)
    except Exception as e:
        print(f"✗ {test_name} failed: {e}")
        failed.append(f"{test_name}: {e}")

print(f"\nResults: {len(passed)} passed, {len(failed)} failed")
if failed:
    print("\nFailed tests:")
    for failure in failed:
        print(f"  - {failure}")

print("\nAll tests completed!")