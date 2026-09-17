
import sys
import json
from pathlib import Path

def test_debug_main_data(main_data):
    """Debug what main_data contains."""
    print(f"main_data type: {type(main_data)}")
    print(f"main_data len: {len(main_data) if isinstance(main_data, dict) else 'N/A'}")
    if isinstance(main_data, dict):
        keys = list(main_data.keys())
        print(f"First 5 keys: {keys[:5]}")
        for k, v in main_data.items():
            if isinstance(v, dict) and "code" in v:
                print(f"Has code field: {k}")
                break
    assert True
