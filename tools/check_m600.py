import json
with open('modes_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
zh = data['zh']
en = data['en']
# Count numeric keys
zh_numeric = len([k for k in zh if not k.startswith('M')])
en_numeric = len([k for k in en if not k.startswith('M')])
print(f'ZH numeric: {zh_numeric}')
print(f'EN numeric: {en_numeric}')
# Check M612-M633 in EN
for k in range(612, 634):
    ks = str(k)
    if ks in en:
        print(f'EN M{k}: EXISTS - {en[ks][0]}')
    else:
        print(f'EN M{k}: MISSING')