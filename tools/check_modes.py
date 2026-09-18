import json
with open('modes_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
zh = data['zh']
en = data['en']
print(f'ZH max key: {max(int(k) for k in zh.keys())}')
print(f'EN max key: {max(int(k) for k in en.keys())}')
# Check keys around 518-533
for k in range(515, 540):
    ks = str(k)
    if ks in zh:
        print(f'ZH M{k}: {zh[ks][0]}')
    if ks in en:
        print(f'EN M{k}: {en[ks][0]}')