import json
import os
import sys

def validate_scenarios(filepath, name):
    """Validate scenarios_zh.json or scenarios_en.json"""
    print(f"\n=== Validating {name} ===")
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    errors = []
    warnings = []
    
    # Expected keys for scenario entries
    expected_keys = {'name', 'description', 'modes', 'reason', 'steps', 'expected', 'case'}
    
    for key, value in data.items():
        if not isinstance(value, dict):
            errors.append(f"{key}: not a dict (type={type(value).__name__})")
            continue
        
        # Check required fields
        for req_key in expected_keys:
            if req_key not in value:
                warnings.append(f"{key}: missing field '{req_key}'")
        
        # Check modes are integers
        modes = value.get('modes', [])
        if not isinstance(modes, list):
            errors.append(f"{key}: modes is not a list")
        else:
            for i, m in enumerate(modes):
                if not isinstance(m, int):
                    errors.append(f"{key}: modes[{i}] = {m!r} is not an integer")
        
        # Check steps is list of strings
        steps = value.get('steps', [])
        if not isinstance(steps, list):
            errors.append(f"{key}: steps is not a list")
        
        # Check expected is list of strings
        expected = value.get('expected', [])
        if not isinstance(expected, list):
            errors.append(f"{key}: expected is not a list")
    
    print(f"  Total entries: {len(data)}")
    print(f"  Errors: {len(errors)}")
    print(f"  Warnings: {len(warnings)}")
    
    for e in errors:
        print(f"    ERROR: {e}")
    for w in warnings[:10]:
        print(f"    WARN: {w}")
    if len(warnings) > 10:
        print(f"    ... and {len(warnings) - 10} more warnings")
    
    return errors, warnings

def validate_code_maps(filepath, name):
    """Validate code_maps.json"""
    print(f"\n=== Validating {name} ===")
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    errors = []
    warnings = []
    
    # Should have CODE_MAP and CODE_MAP_EN as dicts
    expected_top = {'CODE_MAP', 'CODE_MAP_EN'}
    for k in expected_top:
        if k not in data:
            errors.append(f"Missing top-level key: {k}")
        elif not isinstance(data[k], dict):
            errors.append(f"Top-level key {k} is not a dict")
    
    # Check for unexpected keys
    for k in data:
        if k not in expected_top:
            warnings.append(f"Unexpected top-level key: {k}")
    
    print(f"  Top-level keys: {list(data.keys())}")
    print(f"  Errors: {len(errors)}")
    print(f"  Warnings: {len(warnings)}")
    
    for e in errors:
        print(f"    ERROR: {e}")
    for w in warnings:
        print(f"    WARN: {w}")
    
    return errors, warnings

def validate_tags(filepath, name):
    """Validate scenario_tags.json"""
    print(f"\n=== Validating {name} ===")
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    errors = []
    warnings = []
    
    expected_top = {'metadata', 'tags'}
    
    for k in expected_top:
        if k not in data:
            errors.append(f"Missing top-level key: {k}")
    
    # Check for unexpected keys
    for k in data:
        if k not in expected_top:
            warnings.append(f"Unexpected top-level key: {k}")
    
    if 'tags' in data and isinstance(data['tags'], dict):
        print(f"  Tag entries: {len(data['tags'])}")
        for tk, tv in list(data['tags'].items())[:3]:
            if not isinstance(tv, dict):
                errors.append(f"tags.{tk}: not a dict")
            else:
                expected_tag_keys = {'code', 'name_zh', 'name_en', 'era', 'gender', 'ethnicity', 'domains', 'core_modes', 'applications', 'historical_domains', 'mode_count'}
                for req in expected_tag_keys:
                    if req not in tv:
                        warnings.append(f"tags.{tk}: missing field '{req}'")
    
    print(f"  Top-level keys: {list(data.keys())}")
    print(f"  Errors: {len(errors)}")
    print(f"  Warnings: {len(warnings)}")
    
    for e in errors:
        print(f"    ERROR: {e}")
    for w in warnings[:10]:
        print(f"    WARN: {w}")
    
    return errors, warnings

def validate_modes_data(filepath, name):
    """Validate modes_data.json"""
    print(f"\n=== Validating {name} ===")
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    errors = []
    warnings = []
    
    expected_top = {'zh', 'en'}
    
    for k in expected_top:
        if k not in data:
            errors.append(f"Missing top-level key: {k}")
        elif not isinstance(data[k], dict):
            errors.append(f"Top-level key {k} is not a dict")
    
    if 'zh' in data and isinstance(data['zh'], dict):
        print(f"  ZH modes: {len(data['zh'])}")
        for k, v in list(data['zh'].items())[:3]:
            if not isinstance(v, list) or len(v) != 4:
                errors.append(f"zh.{k}: expected list of 4 elements, got {type(v)}")
    
    if 'en' in data and isinstance(data['en'], dict):
        print(f"  EN modes: {len(data['en'])}")
        for k, v in list(data['en'].items())[:3]:
            if not isinstance(v, list) or len(v) != 4:
                errors.append(f"en.{k}: expected list of 4 elements, got {type(v)}")
    
    print(f"  Top-level keys: {list(data.keys())}")
    print(f"  Errors: {len(errors)}")
    print(f"  Warnings: {len(warnings)}")
    
    for e in errors:
        print(f"    ERROR: {e}")
    for w in warnings:
        print(f"    WARN: {w}")
    
    return errors, warnings

def validate_regional_modes(filepath, name):
    """Validate regional modes files (arctic, latam, oceania, africa)"""
    print(f"\n=== Validating {name} ===")
    if not os.path.exists(filepath):
        print(f"  FILE NOT FOUND")
        return ["File not found"], []
    
    if os.path.getsize(filepath) == 0:
        print(f"  FILE IS EMPTY (0 bytes)")
        return ["File is empty"], []
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"  INVALID JSON: {e}")
        return [f"Invalid JSON: {e}"], []
    
    errors = []
    warnings = []
    
    if not isinstance(data, dict):
        errors.append(f"Root is not a dict, got {type(data)}")
    else:
        if 'modes' not in data:
            errors.append("Missing 'modes' key")
        elif not isinstance(data['modes'], list):
            errors.append("'modes' is not a list")
        else:
            print(f"  Modes count: {len(data['modes'])}")
            for i, mode in enumerate(data['modes']):
                if not isinstance(mode, dict):
                    errors.append(f"modes[{i}]: not a dict")
                else:
                    expected_keys = {'id', 'name_zh', 'name_en', 'definition_zh', 'definition_en', 'steps', 'figures'}
                    for req in expected_keys:
                        if req not in mode:
                            warnings.append(f"modes[{i}]: missing field '{req}'")
    
    print(f"  Top-level keys: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
    print(f"  Errors: {len(errors)}")
    print(f"  Warnings: {len(warnings)}")
    
    for e in errors:
        print(f"    ERROR: {e}")
    for w in warnings[:10]:
        print(f"    WARN: {w}")
    
    return errors, warnings

def main():
    all_errors = []
    all_warnings = []
    
    # Validate core files
    errors, warnings = validate_scenarios('/opt/data/workspace/Protreptic/tools/scenarios_zh.json', 'scenarios_zh.json')
    all_errors.extend([f"scenarios_zh: {e}" for e in errors])
    all_warnings.extend([f"scenarios_zh: {w}" for w in warnings])
    
    errors, warnings = validate_scenarios('/opt/data/workspace/Protreptic/tools/scenarios_en.json', 'scenarios_en.json')
    all_errors.extend([f"scenarios_en: {e}" for e in errors])
    all_warnings.extend([f"scenarios_en: {w}" for w in warnings])
    
    errors, warnings = validate_code_maps('/opt/data/workspace/Protreptic/tools/code_maps.json', 'code_maps.json')
    all_errors.extend([f"code_maps: {e}" for e in errors])
    all_warnings.extend([f"code_maps: {w}" for w in warnings])
    
    errors, warnings = validate_tags('/opt/data/workspace/Protreptic/tools/scenario_tags.json', 'scenario_tags.json')
    all_errors.extend([f"scenario_tags: {e}" for e in errors])
    all_warnings.extend([f"scenario_tags: {w}" for w in warnings])
    
    errors, warnings = validate_modes_data('/opt/data/workspace/Protreptic/tools/modes_data.json', 'modes_data.json')
    all_errors.extend([f"modes_data: {e}" for e in errors])
    all_warnings.extend([f"modes_data: {w}" for w in warnings])
    
    # Validate regional modes
    errors, warnings = validate_regional_modes('/opt/data/workspace/Protreptic/data/arctic/arctic_modes.json', 'arctic_modes.json')
    all_errors.extend([f"arctic_modes: {e}" for e in errors])
    all_warnings.extend([f"arctic_modes: {w}" for w in warnings])
    
    errors, warnings = validate_regional_modes('/opt/data/workspace/Protreptic/data/latam/latam_modes.json', 'latam_modes.json')
    all_errors.extend([f"latam_modes: {e}" for e in errors])
    all_warnings.extend([f"latam_modes: {w}" for w in warnings])
    
    errors, warnings = validate_regional_modes('/opt/data/workspace/Protreptic/data/oceania/oceania_modes.json', 'oceania_modes.json')
    all_errors.extend([f"oceania_modes: {e}" for e in errors])
    all_warnings.extend([f"oceania_modes: {w}" for w in warnings])
    
    errors, warnings = validate_regional_modes('/opt/data/workspace/Protreptic/data/africa/africa_modes.json', 'africa_modes.json')
    all_errors.extend([f"africa_modes: {e}" for e in errors])
    all_warnings.extend([f"africa_modes: {w}" for w in warnings])
    
    # Summary
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    print(f"Total Errors: {len(all_errors)}")
    print(f"Total Warnings: {len(all_warnings)}")
    
    if all_errors:
        print("\nALL ERRORS:")
        for e in all_errors:
            print(f"  - {e}")
    
    if all_warnings:
        print("\nALL WARNINGS (first 30):")
        for w in all_warnings[:30]:
            print(f"  - {w}")
        if len(all_warnings) > 30:
            print(f"  ... and {len(all_warnings) - 30} more warnings")
    
    # Write report
    report = {
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "total_errors": len(all_errors),
        "total_warnings": len(all_warnings),
        "errors": all_errors,
        "warnings": all_warnings,
        "pass": len(all_errors) == 0
    }
    
    with open('/opt/data/workspace/Protreptic/tools/validation_report.json', 'w') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\nReport written to /opt/data/workspace/Protreptic/tools/validation_report.json")
    
    return len(all_errors) == 0

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)