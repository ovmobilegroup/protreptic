import json
import sys

def fix_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    fixed_count = 0
    for key, value in data.items():
        if not isinstance(value, dict):
            continue
        changed = False
        # Fix expected: if string, make it list
        expected = value.get('expected')
        if isinstance(expected, str):
            value['expected'] = [expected]
            changed = True
            fixed_count += 1
        # Ensure code is present; if missing or None, set to key
        code = value.get('code')
        if code is None:
            value['code'] = key
            changed = True
        # Ensure steps is list (should already be)
        steps = value.get('steps')
        if steps is not None and not isinstance(steps, list):
            # Convert to list if it's a string? Not expected, but just in case
            value['steps'] = [steps] if isinstance(steps, str) else list(steps)
            changed = True
        # Ensure modes are ints
        modes = value.get('modes')
        if isinstance(modes, list):
            new_modes = []
            for m in modes:
                if isinstance(m, str) and m.isdigit():
                    new_modes.append(int(m))
                    changed = True
                elif isinstance(m, int):
                    new_modes.append(m)
                else:
                    # If it's something else, try to convert to int?
                    try:
                        new_modes.append(int(m))
                        changed = True
                    except:
                        new_modes.append(m)
            if changed:
                value['modes'] = new_modes
        # If case is missing, we could add it as empty string? But correct entries have it as string.
        # We'll leave it as is; if missing, it's okay.
    
    print(f"Fixed {fixed_count} entries in {input_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    fix_file('scenarios_zh.json', 'scenarios_zh.json.fixed')
    fix_file('scenarios_en.json', 'scenarios_en.json.fixed')
