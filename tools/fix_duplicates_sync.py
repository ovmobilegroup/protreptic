import json

# Load data
with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)
with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)
with open('code_maps.json', 'r', encoding='utf-8') as f:
    cm = json.load(f)

# Build name-to-code mapping for Chinese
h_zh = {k: v for k, v in zh.items() if k.startswith('H-')}
name_to_code_zh = {}
for code, sc in h_zh.items():
    name = sc['name'].split('：')[0] if '：' in sc['name'] else sc['name'].split(':')[0]
    if name not in name_to_code_zh:
        name_to_code_zh[name] = code
    else:
        # Keep the one with more complete modes or lower number
        existing_code = name_to_code_zh[name]
        existing_modes = len(zh[existing_code]['modes'])
        new_modes = len(h_zh[code]['modes'])
        if new_modes > existing_modes:
            name_to_code_zh[name] = code
            print(f"Replace {name}: {existing_code} -> {code} (more modes)")
        else:
            print(f"Keep {name}: {existing_code} (remove {code})")

# Remove duplicates - keep only canonical codes
canonical_codes_zh = set(name_to_code_zh.values())
print(f"Canonical H- codes in Chinese: {len(canonical_codes_zh)}")

# Build canonical Chinese data
zh_canonical = {k: v for k, v in zh.items() if not k.startswith('H-') or k in canonical_codes_zh}

# Build English mapping from Chinese canonical names
h_en = {k: v for k, v in en.items() if k.startswith('H-')}
en_name_to_code = {}
for code, sc in en.items():
    if code.startswith('H-'):
        name = sc['name'].split(':')[0] if ':' in sc['name'] else sc['name'].split('：')[0]
        en_name_to_code[name] = code

# Find missing English entries
zh_names = set()
for code in canonical_codes_zh:
    name = zh_canonical[code]['name'].split('：')[0] if '：' in zh_canonical[code]['name'] else zh_canonical[code]['name'].split(':')[0]
    zh_names.add(name)

en_names = set(en_name_to_code.keys())
missing_in_en = zh_names - en_names
print(f"Missing in English: {len(missing_in_en)}")

# Generate English entries for missing ones (simple translation of name/description)
# We'll copy from Chinese and translate key fields
def translate_basic(name, desc):
    # Simple name translations for common historical figures
    translations = {
        '郭象': 'Guo Xiang',
        '陈云': 'Chen Yun',
        '范蠡': 'Fan Li',
        '桑弘羊': 'Sang Hongyang',
        '朱元璋': 'Zhu Yuanzhang',
        '李世民': 'Li Shimin',
        '屈原': 'Qu Yuan',
        '戚继光': 'Qi Jiguang',
        '管仲': 'Guan Zhong',
        '庄子': 'Zhuangzi',
        '陈寅恪': 'Chen Yinke',
        '武则天': 'Wu Zetian',
        '顾炎武': 'Gu Yanwu',
        '蔡伦': 'Cai Lun',
        '康有为': 'Kang Youwei',
        '戴震': 'Dai Zhen',
        '沈括': 'Shen Kuo',
        '杨朱': 'Yang Zhu',
        '诸葛亮': 'Zhuge Liang',
        '陆九渊': 'Lu Jiuyuan',
        '毛泽东': 'Mao Zedong',
        '墨子': 'Mozi',
        '郭子仪': 'Guo Ziyi',
        '钱穆': 'Qian Mu',
        '程颢程颐': 'Cheng Hao Cheng Yi',
        '刘半农': 'Liu Bannong',
        '屠呦呦': 'Tu Youyou',
        '林则徐': 'Lin Zexu',
        '刘裕': 'Liu Yu',
        '海瑞': 'Hai Rui',
        '吴有训': 'Wu Youxun',
        '张载': 'Zhang Zai',
        '葛洪': 'Ge Hong',
        '魏徵': 'Wei Zheng',
        '萧何': 'Xiao He',
        '彭德怀': 'Peng Dehuai',
        '曾国藩': 'Zeng Guofan',
        '黄炎培': 'Huang Yanpei',
        '韩非': 'Han Fei',
        '惠施': 'Hui Shi',
        '班超': 'Ban Chao',
        '班固': 'Ban Gu',
        '冯桂芬': 'Feng Guifen',
        '张謇': 'Zhang Jian',
        '成吉思汗': 'Genghis Khan',
        '欧阳修': 'Ouyang Xiu',
        '胡适': 'Hu Shi',
        '王夫之': 'Wang Fuzhi',
        '章学诚': 'Zhang Xuecheng',
        '文天祥': 'Wen Tianxiang',
        '钱玄同': 'Qian Xuantong',
        '徐霞客': 'Xu Xiake',
        '苏轼': 'Su Shi',
        '孙权': 'Sun Quan',
        '邵雍': 'Shao Yong',
        '王充': 'Wang Chong',
        '钱学森': 'Qian Xuesen',
        '吴敬梓': 'Wu Jingzi',
        '蒲松龄': 'Pu Songling',
        '黄宗羲': 'Huang Zongxi',
        '贾思勰': 'Jia Sixie',
        '韩愈': 'Han Yu',
        '王选': 'Wang Xuan',
        '嵇康': 'Ji Kang',
        '龚自珍': 'Gong Zizhen',
        '刘晏': 'Liu Yan',
        '刘少奇': 'Liu Shaoqi',
        '王安石': 'Wang Anshi',
        '颜回': 'Yan Hui',
        '老子': 'Laozi',
        '蒋介石': 'Chiang Kai-shek',
        '王艮': 'Wang Gen',
        '袁隆平': 'Yuan Longping',
        '曹雪芹': 'Cao Xueqin',
        '刘师培': 'Liu Shipei',
        '梁启超': 'Liang Qichao',
        '朱德': 'Zhu De',
        '薛暮桥': 'Xue Muqiao',
        '赵构': 'Zhao Gou',
        '魏源': 'Wei Yuan',
        '张衡': 'Zhang Heng',
        '张仪': 'Zhang Yi',
        '柳宗元': 'Liu Zongyuan',
        '辛弃疾': 'Xin Qiji',
        '邓小平': 'Deng Xiaoping',
        '雍正': 'Yongzheng',
        '叶适': 'Ye Shi',
        '王阳明': 'Wang Yangming',
        '孟子': 'Mencius',
        '鲁迅': 'Lu Xun',
        '孙思邈': 'Sun Simiao',
        '刘邦': 'Liu Bang',
        '司马懿': 'Sima Yi',
        '苏秦': 'Su Qin',
        '李贽': 'Li Zhi',
        '刘向刘歆': 'Liu Xiang Liu Xin',
        '商鞅': 'Shang Yang',
        '任正非': 'Ren Zhengfei',
        '张居正': 'Zhang Juzheng',
        '孙武': 'Sun Wu',
        '陈亮': 'Chen Liang',
        '公孙龙': 'Gongsun Long',
        '竺可桢': 'Zhu Kezhen',
        '司马迁': 'Sima Qian',
        '李悝': 'Li Kui',
        '范仲淹': 'Fan Zhongyan',
        '章太炎': 'Zhang Taiyan',
        '华罗庚': 'Hua Luogeng',
        '荀子': 'Xunzi',
        '陶渊明': 'Tao Yuanming',
        '蔡元培': 'Cai Yuanpei',
        '谭嗣同': 'Tan Sitong',
        '粟裕': 'Su Yu',
        '左宗棠': 'Zuo Zongtang',
        '张仲景': 'Zhang Zhongjing',
        '董仲舒': 'Dong Zhongshu',
        '朱熹': 'Zhu Xi',
        '严复': 'Yan Fu',
        '康熙': 'Kangxi',
        '李时珍': 'Li Shizhen',
        '宋应星': 'Song Yingxing',
        '李鸿章': 'Li Hongzhang',
        '张之洞': 'Zhang Zhidong',
        '王弼': 'Wang Bi',
        '周敦颐': 'Zhou Dunyi',
        '曹操': 'Cao Cao',
        '司马光': 'Sima Guang',
        '周恩来': 'Zhou Enlai',
        '袁世凯': 'Yuan Shikai',
        '赵匡胤': 'Zhao Kuangyin',
        '刘备': 'Liu Bei',
        '孙中山': 'Sun Yat-sen',
        '刘秀': 'Liu Xiu',
        '林彪': 'Lin Biao',
        '皇太极': 'Huang Taiji',
    }
    
    en_name = translations.get(name, name)
    en_desc = desc  # Keep description as-is for now
    return en_name, en_desc

# Create English entries for missing ones
en_canonical = {k: v for k, v in en.items() if not k.startswith('H-')}
for code in canonical_codes_zh:
    sc = zh_canonical[code]
    name = sc['name'].split('：')[0] if '：' in sc['name'] else sc['name'].split(':')[0]
    if name not in en_name_to_code:
        # Create English entry
        en_name, en_desc = translate_basic(name, sc['description'])
        en_canonical[code] = {
            "name": f"{en_name}: {zh[code]['description']}",  # Keep description as-is for now
            "description": sc['description'],
            "modes": sc['modes'],
            "reason": sc['reason'],
            "steps": sc['steps'],
            "expected": sc['expected'],
            "case": sc['case']
        }
        print(f"Created English entry: {code} - {name}")

# Update code_maps
cm_canonical = {
    "CODE_MAP": {},
    "CODE_MAP_EN": {}
}
for code in canonical_codes_zh:
    sc = zh_canonical[code]
    name = sc['name'].split('：')[0] if '：' in sc['name'] else sc['name'].split(':')[0]
    cm_canonical["CODE_MAP"][code] = sc['name']
    # English name
    en_name = translate_basic(name, '') 
    # Get English name from en_canonical if exists
    if code in en_canonical:
        en_name = en_canonical[code]['name'].split(':')[0] if ':' in en_canonical[code]['name'] else en_canonical[code]['name']
    cm_canonical["CODE_MAP_EN"][code] = f"{en_name}: {en_canonical.get(code, {}).get('description', '')}"

# Save files
with open('scenarios_zh.json', 'w', encoding='utf-8') as f:
    json.dump(zh_canonical, f, ensure_ascii=False, indent=2)

with open('scenarios_en.json', 'w', encoding='utf-8') as f:
    json.dump(en_canonical, f, ensure_ascii=False, indent=2)

with open('code_maps.json', 'w', encoding='utf-8') as f:
    json.dump(cm_canonical, f, ensure_ascii=False, indent=2)

print("Files updated successfully!")
print(f"Chinese H- entries: {len([k for k in zh_canonical if k.startswith('H-')])}")
print(f"English H- entries: {len([k for k in en_canonical if k.startswith('H-')])}")
print(f"CODE_MAP entries: {len(cm_canonical['CODE_MAP'])}")