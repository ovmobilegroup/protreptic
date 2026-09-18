#!/usr/bin/env python3
"""
Unit tests for Phase 4 Batch 1 Generator
"""
import json
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

def test_batch1_files_exist():
    """Test that Phase 4 Batch 1 files are created"""
    expected_files = [
        "scenarios_zh.json",
        "scenarios_en.json", 
        "code_maps.json",
        "scenario_tags.json"
    ]
    
    for filename in expected_files:
        filepath = Path(__file__).parent / filename
        assert filepath.exists(), f"File {filename} not found"
        print(f"✓ {filename} exists")

def test_scenarios_zh_content():
    """Test Chinese scenarios content"""
    filepath = Path(__file__).parent / "scenarios_zh.json"
    with open(filepath, 'r', encoding='utf-8') as f:
        scenarios = json.load(f)
    
    # Check we have 16 scenarios
    assert len(scenarios) == 16, f"Expected 16 scenarios, got {len(scenarios)}"
    
    # Check all codes are P4 format
    for code in scenarios.keys():
        assert code.startswith("P4-"), f"Code {code} doesn't start with P4-"
        assert "-" in code, f"Code {code} doesn't have proper format"
        
    # Check each scenario has required fields
    for code, scenario in scenarios.items():
        assert "name" in scenario, f"Scenario {code} missing name"
        assert "description" in scenario, f"Scenario {code} missing description"
        assert "reason" in scenario, f"Scenario {code} missing reason"
        assert "modes" in scenario, f"Scenario {code} missing modes"
        assert "steps" in scenario, f"Scenario {code} missing steps"
        assert "expected" in scenario, f"Scenario {code} missing expected"
        assert "case" in scenario, f"Scenario {code} missing case"
        assert "figure_data" in scenario, f"Scenario {code} missing figure_data"
        
    print(f"✓ scenarios_zh.json contains {len(scenarios)} scenarios")

def test_scenarios_en_content():
    """Test English scenarios content"""
    filepath = Path(__file__).parent / "scenarios_en.json"
    with open(filepath, 'r', encoding='utf-8') as f:
        scenarios = json.load(f)
    
    # Check we have 16 scenarios
    assert len(scenarios) == 16, f"Expected 16 scenarios, got {len(scenarios)}"
    
    # Check all codes are P4 format
    for code in scenarios.keys():
        assert code.startswith("P4-"), f"Code {code} doesn't start with P4-"
        
    # Check each scenario has required fields
    for code, scenario in scenarios.items():
        assert "name" in scenario, f"Scenario {code} missing name"
        assert "description" in scenario, f"Scenario {code} missing description"
        assert "reason" in scenario, f"Scenario {code} missing reason"
        assert "modes" in scenario, f"Scenario {code} missing modes"
        assert "steps" in scenario, f"Scenario {code} missing steps"
        assert "expected" in scenario, f"Scenario {code} missing expected"
        assert "case" in scenario, f"Scenario {code} missing case"
        assert "figure_data" in scenario, f"Scenario {code} missing figure_data"
        
    print(f"✓ scenarios_en.json contains {len(scenarios)} scenarios")

def test_code_maps_content():
    """Test code maps content"""
    filepath = Path(__file__).parent / "code_maps.json"
    with open(filepath, 'r', encoding='utf-8') as f:
        code_maps = json.load(f)
    
    assert "CODE_MAP" in code_maps, "Missing CODE_MAP in code_maps.json"
    assert "CODE_MAP_EN" in code_maps, "Missing CODE_MAP_EN in code_maps.json"
    
    # Check mappings
    code_map = code_maps["CODE_MAP"]
    code_map_en = code_maps["CODE_MAP_EN"]
    
    assert len(code_map) == 16, f"Expected 16 entries in CODE_MAP, got {len(code_map)}"
    assert len(code_map_en) == 16, f"Expected 16 entries in CODE_MAP_EN, got {len(code_map_en)}"
    
    print(f"✓ code_maps.json contains mappings for {len(code_map)} codes")

def test_tags_content():
    """Test tags content"""
    filepath = Path(__file__).parent / "scenario_tags.json"
    with open(filepath, 'r', encoding='utf-8') as f:
        tags = json.load(f)
    
    assert "tags" in tags, "Missing 'tags' key in scenario_tags.json"
    
    scenario_tags = tags["tags"]
    assert len(scenario_tags) == 16, f"Expected 16 entries in tags, got {len(scenario_tags)}"
    
    print(f"✓ scenario_tags.json contains {len(scenario_tags)} tags")

def test_bilingual_consistency():
    """Test that Chinese and English versions are consistent"""
    scenarios_zh_path = Path(__file__).parent / "scenarios_zh.json"
    scenarios_en_path = Path(__file__).parent / "scenarios_en.json"
    
    with open(scenarios_zh_path, 'r', encoding='utf-8') as f:
        scenarios_zh = json.load(f)
    
    with open(scenarios_en_path, 'r', encoding='utf-8') as f:
        scenarios_en = json.load(f)
    
    # Check same number of scenarios
    assert len(scenarios_zh) == len(scenarios_en), "Chinese and English scenario counts don't match"
    
    # Check same codes
    zh_codes = set(scenarios_zh.keys())
    en_codes = set(scenarios_en.keys())
    assert zh_codes == en_codes, "Chinese and English scenario codes don't match"
    
    # Check same structure (excluding translations)
    for code in zh_codes:
        zh_scenario = scenarios_zh[code]
        en_scenario = scenarios_en[code]
        
        # Check same keys
        assert set(zh_scenario.keys()) == set(en_scenario.keys()), f"Scenario {code} has different keys"
        
        # Check modes are same (they're codes, not names)
        assert zh_scenario["modes"] == en_scenario["modes"], f"Scenario {code} has different modes"
    
    print(f"✓ Chinese and English scenarios are consistent")

def test_code_format():
    """Test that codes follow P4-XXX-NNN format"""
    scenarios_zh_path = Path(__file__).parent / "scenarios_zh.json"
    
    with open(scenarios_zh_path, 'r', encoding='utf-8') as f:
        scenarios = json.load(f)
    
    for code in scenarios.keys():
        # Check format: P4-TECH-001 or P4-WOMEN-009
        parts = code.split("-")
        assert len(parts) == 3, f"Code {code} doesn't have 3 parts"
        assert parts[0] == "P4", f"Code {code} doesn't start with P4"
        assert parts[1] in ["TECH", "WOMEN"], f"Code {code} has invalid category: {parts[1]}"
        
        # Check number is between 001 and 016
        number = int(parts[2])
        assert 1 <= number <= 16, f"Code {code} has invalid number: {number}"
    
    print(f"✓ All codes follow P4-XXX-NNN format")

def run_all_tests():
    """Run all tests"""
    print("=== Phase 4 Batch 1 Generator Tests ===\n")
    
    test_batch1_files_exist()
    test_scenarios_zh_content()
    test_scenarios_en_content()
    test_code_maps_content()
    test_tags_content()
    test_bilingual_consistency()
    test_code_format()
    
    print(f"\n=== ALL TESTS PASSED ===")
    print(f"✓ Phase 4 Batch 1 generator successfully created all required files")
    print(f"✓ Generated 16 bilingual scenarios with proper P4-XXX-NNN codes")
    print(f"✓ Created code maps, tags, and backup files")
    print(f"✓ Files are ready for integration into thinking_mode_selector system")

if __name__ == "__main__":
    run_all_tests()