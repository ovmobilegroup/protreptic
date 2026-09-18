import json
import re
import sys

pattern = re.compile(r'^[A-Z]{2}-[A-Z]{3}-\d{3}$')

def filter_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Filter keys
    filtered = {k: v for k, v in data.items() if pattern.match(k)}
    removed = [k for k in data.keys() if not pattern.match(k)]
    print(f"Removed {len(removed)} non-scenario keys: {removed[:10]}")
    print(f"Kept {len(filtered)} scenario keys")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    filter_file('scenarios_zh.json', 'scenarios_zh.json.filtered')
    filter_file('scenarios_en.json', 'scenarios_en.json.filtered')
