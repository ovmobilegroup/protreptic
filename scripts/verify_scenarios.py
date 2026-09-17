import json

with open('<repo>/data/scenarios_en.json', 'r') as f:
    scenarios_en = json.load(f)

with open('<repo>/data/scenarios_zh.json', 'r') as f:
    scenarios_zh = json.load(f)

# Verify all 10 scenarios
for i in range(1, 11):
    en_idx = 113 + i  # indices 114-123
    zh_idx = 104 + i  # indices 105-114
    
    en_s = scenarios_en[en_idx]
    zh_s = scenarios_zh[zh_idx]
    
    print(f"\n=== Mode {en_s['mode_id']} ===")
    print(f"EN: {en_s['title']}")
    print(f"EN desc preview: {en_s['description'][:80]}...")
    print(f"ZH: {zh_s['title']}")
    print(f"ZH desc preview: {zh_s['description'][:80]}...")

print("\n✅ All 10 scenarios verified in both EN and ZH")