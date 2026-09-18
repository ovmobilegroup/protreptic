import json, re
with open('scenarios_zh.json', 'r') as f:
    d = json.load(f)
h_codes = []
for k, v in d.items():
    code = v.get('code', '')
    m = re.search(r'H-([A-Z]+)-(\d+)', code)
    if m:
        h_codes.append((k, code, int(m.group(2))))
h_codes.sort(key=lambda x: x[2])
print(f'Total H-codes (Chinese historical): {len(h_codes)}')
if h_codes:
    print(f'H-code range: {h_codes[0][2]} to {h_codes[-1][2]}')
phase3 = [(k, c, n) for k, c, n in h_codes if 212 <= n <= 256]
print(f'\nPhase 3 H-codes (212-256): {len(phase3)} found')
for k, c, n in sorted(phase3, key=lambda x: x[2]):
    print(f'  {c} (#{n}) - key: {k}')
missing = [n for n in range(212, 257) if not any(n == num for _, _, num in h_codes)]
if missing:
    print(f'\nMissing H-code numbers: {missing}')
else:
    print('\nNo missing in 212-256.')
