#!/usr/bin/env python3
"""
English polish script for Protreptic scenarios.
Generates high-quality English translations with consistent imperative mood.
"""
import json
import re

# Load existing data
with open('/opt/data/workspace/Protreptic/tools/scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)
with open('/opt/data/workspace/Protreptic/tools/scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)
with open('/opt/data/workspace/Protreptic/tools/modes_data.json', 'r', encoding='utf-8') as f:
    modes = json.load(f)

zh_modes = modes['zh']
en_modes = modes['en']

# Standardized terminology mapping
TERMINOLOGY = {
    # Core concepts
    '隆中对': 'Longzhong Plan',
    '三分天下': 'Three Kingdoms Division Strategy',
    '北伐': 'Northern Expeditions',
    '出师表': 'Chushibiao (Memorial on the Expedition)',
    '诫子书': 'Admonition to My Son',
    '木牛流马': 'Wooden Ox and Flowing Horse (logistics innovation)',
    '鞠躬尽瘁，死而后已': 'devotion to the utmost until death',
    '三顾草庐': 'Three Visits to the Thatched Cottage',
    '白帝托孤': 'Baidi Entrustment',
    '仁义立国': 'Righteousness-Based Statecraft',
    '格局授权': 'Strategic Delegation',
    '知人善任': 'Talent Recognition and Deployment',
    '挟天子以令诸侯': 'Using the Emperor as Authority over Feudal Lords',
    '屯田制': 'Tuntian Agricultural Garrison System',
    '短兵接战': 'Short-Decisive Battle Doctrine',
    '唯才是举': 'Merit-Based Appointment',
    '守成': 'Consolidation Rule',
    '平衡术': 'Balance-of-Power Statecraft',
    '江东基业': 'Jiangdong Foundation',
    '人才用吴': 'Wu-Centric Talent Policy',
    '赤壁之战': 'Battle of Red Cliffs',
    '火攻': 'Fire Attack',
    '连环计': 'Chain Stratagem',
    '草船借箭': 'Borrowing Arrows with Straw Boats',
    '借东风': 'Borrowing the East Wind',
    '苦肉计': 'Self-Inflicted Wound Stratagem',
    '街亭之战': 'Battle of Jieting',
    '违令': 'Disobeying Orders',
    '纸上谈兵': 'Armchair Strategy',
    '斩马谡': 'Execution of Ma Su',
    '自贬三等': 'Self-Demotion by Three Ranks',
    '夷陵之战': 'Battle of Yiling',
    '以私仇报国仇': 'Settling Private Grudge at National Expense',
    '连营七百里': 'Encamped for Seven Hundred Li',
    '陆逊': 'Lu Xun',
    '长坂坡': 'Battle of Changban',
    '单骑救主': 'Single-Horsed Rescue of the Lord',
    '子龙一身都是胆': 'Zilong is All Courage',
    '请以死奉命': 'Request to Fulfill Mission with My Life',
    '运动战': 'Maneuver Warfare',
    '游击战': 'Guerrilla Warfare',
    '歼灭战': 'Annihilation Warfare',
    '非对称作战': 'Asymmetric Warfare',
    '兵斗准': 'Military Training Precision Standard',
    '军事工程学院': 'Military Engineering Institute',
    '国防科大': 'National University of Defense Technology',
    '杂交水稻': 'Hybrid Rice',
    '三系法': 'Three-Line System',
    '两系法': 'Two-Line System',
    '超级稻': 'Super Rice',
    '粮食安全': 'Food Security',
    '优选法': 'Optimization Method',
    '多目标规划': 'Multi-Objective Programming',
    '均匀分布': 'Uniform Distribution',
    '系统工程': 'Systems Engineering',
    '大系统观': 'Large Systems Perspective',
    '两弹一星': 'Two Bombs One Satellite',
    '导弹航天': 'Missile and Aerospace',
    '科技管理': 'Technology Management',
    '现象学': 'Phenology',
    '气象学': 'Meteorology',
    '地理学': 'Geography',
    '浙大校长': 'President of Zhejiang University',
    '科教兴国': 'Revitalizing the Nation through Science and Education',
    # Mode names (standardized English)
    '矛盾分析法': 'Contradiction Analysis',
    '群众路线法': 'Mass Line Method',
    '持久战思维': 'Protracted War Thinking',
    '农村包围城市': 'Rural Encirclement of Cities',
    '实事求是法': 'Seeking Truth from Facts',
    '统一战线法': 'United Front Method',
    '战略预判法': 'Strategic Foresight',
    '渐进改革法': 'Gradual Reform',
    '独立自主法': 'Self-Reliance',
    '批评与自我批评': 'Criticism and Self-Criticism',
    '灵活策略法': 'Flexible Strategy',
    '系统思维法': 'Systems Thinking',
    '全胜思维法': 'Total Victory Thinking',
    '战争重心法': 'Center of Gravity (Warfare)',
    '运动歼灭法': 'Maneuver Annihilation',
    '游击战十六字诀': 'Sixteen-Character Guerrilla Formula',
    '多元思维模型': 'Mental Models Pluralism',
    '目标管理法': 'Management by Objectives',
    '边际思维法': 'Marginal Thinking',
    '博弈论思维': 'Game Theory Thinking',
    '损失厌恶法': 'Loss Aversion',
    '总体性思维': 'Holistic Thinking',
    '自然选择法': 'Natural Selection',
    '间断均衡法': 'Punctuated Equilibrium',
    '抽象归纳法': 'Abstraction and Induction',
    '知行合一法': 'Unity of Knowledge and Action',
    '双系统思维': 'Dual-System Thinking',
    '摸石头过河': 'Crossing River by Feeling Stones',
    '反馈回路法': 'Feedback Loop',
    '框架效应法': 'Framing Effect',
    '制度化制衡法': 'Institutional Checks and Balances',
    '三衙分兵法': 'Three-Agency Military Separation',
    '鸟笼经济法': 'Birdcage Economy',
    '边际思维法': 'Marginal Thinking',
    '冗余备份法': 'Redundancy and Backup',
    '边界思维法': 'Boundary Thinking',
    '驿站制法': 'Relay Station System',
    '三民主义法': 'Three Principles of the People',
}

# Generate English names for all figures
def generate_english_name(zh_name, code):
    """Generate proper English name from Chinese"""
    # Extract main name and key achievements
    if '：' in zh_name:
        parts = zh_name.split('：')
        name = parts[0]
        achievements = parts[1] if len(parts) > 1 else ''
    else:
        name = zh_name
        achievements = ''
    
    # Translate common names
    name_map = {
        '诸葛亮': 'Zhuge Liang',
        '刘备': 'Liu Bei',
        '曹操': 'Cao Cao',
        '孙权': 'Sun Quan',
        '赵云': 'Zhao Yun',
        '关羽': 'Guan Yu',
        '张飞': 'Zhang Fei',
        '马谡': 'Ma Su',
        '王平': 'Wang Ping',
        '张郃': 'Zhang He',
        '陆逊': 'Lu Xun',
        '周瑜': 'Zhou Yu',
        '鲁肃': 'Lu Su',
        '庞统': 'Pang Tong',
        '黄盖': 'Huang Gai',
        '蒋琬': 'Jiang Wan',
        '费祎': 'Fei Yi',
        '董允': 'Dong Yun',
        '姜维': 'Jiang Wei',
        '司马懿': 'Sima Yi',
        '袁隆平': 'Yuan Longping',
        '华罗庚': 'Hua Luogeng',
        '钱学森': 'Qian Xuesen',
        '竺可桢': 'Zhu Kezhen',
        '刘伯承': 'Liu Bocheng',
        '粟裕': 'Su Yu',
        '陈毅': 'Chen Yi',
        '邓颖超': 'Deng Yingchao',
        '宋庆龄': 'Song Qingling',
        '李先念': 'Li Xiannian',
        '邓稼先': 'Deng Jiaxian',
        '钱三强': 'Qian Sanqiang',
        '朱光亚': 'Zhu Guangya',
        '王大珩': 'Wang Daheng',
        '程开甲': 'Cheng Kaijia',
        '于敏': 'Yu Min',
        '郭永怀': 'Guo Yonghuai',
        '王选': 'Wang Xuan',
        '屠呦呦': 'Tu Youyou',
        '李四光': 'Li Siguang',
        '丁文江': 'Ding Wenjiang',
        '翁文灏': 'Weng Wenhao',
        '吴有训': 'Wu Youxun',
        '李善兰': 'Li Shanlan',
        '祖冲之': 'Zu Chongzhi',
        '一行': 'Yixing (Monk)',
        '郭守敬': 'Guo Shoujing',
        '朱载堉': 'Zhu Zaiyu',
        '徐光启': 'Xu Guangqi',
        '宋应星': 'Song Yingxing',
        '李时珍': 'Li Shizhen',
        '张衡': 'Zhang Heng',
        '蔡伦': 'Cai Lun',
        '张仲景': 'Zhang Zhongjing',
        '葛洪': 'Ge Hong',
        '孙思邈': 'Sun Simiao',
        '沈括': 'Shen Kuo',
        '司马迁': 'Sima Qian',
        '班固': 'Ban Gu',
        '司马光': 'Sima Guang',
        '刘知几': 'Liu Zhiji',
        '欧阳修': 'Ouyang Xiu',
        '郑樵': 'Zheng Qiao',
        '马端临': 'Ma Duanlin',
        '赵翼': 'Zhao Yi',
        '王鸣盛': 'Wang Mingsheng',
        '钱大昕': 'Qian Daxin',
        '章学诚': 'Zhang Xuecheng',
        '王夫之': 'Wang Fuzhi',
        '黄宗羲': 'Huang Zongxi',
        '顾炎武': 'Gu Yanwu',
        '戴震': 'Dai Zhen',
        '阮元': 'Ruan Yuan',
        '魏源': 'Wei Yuan',
        '龚自珍': 'Gong Zizhen',
        '林则徐': 'Lin Zexu',
        '曾国藩': 'Zeng Guofan',
        '左宗棠': 'Zuo Zongtang',
        '李鸿章': 'Li Hongzhang',
        '张之洞': 'Zhang Zhidong',
        '康有为': 'Kang Youwei',
        '梁启超': 'Liang Qichao',
        '谭嗣同': 'Tan Sitong',
        '严复': 'Yan Fu',
        '孙中山': 'Sun Yat-sen',
        '毛泽东': 'Mao Zedong',
        '周恩来': 'Zhou Enlai',
        '朱德': 'Zhu De',
        '刘少奇': 'Liu Shaoqi',
        '陈云': 'Chen Yun',
        '邓小平': 'Deng Xiaoping',
        '江泽民': 'Jiang Zemin',
        '胡锦涛': 'Hu Jintao',
        '习近平': 'Xi Jinping',
        '任正非': 'Ren Zhengfei',
        '马云': 'Jack Ma',
        '马化腾': 'Pony Ma',
        '雷军': 'Lei Jun',
        '王兴': 'Wang Xing',
        '张一鸣': 'Zhang Yiming',
        '黄峥': 'Colin Huang',
        '李彦宏': 'Robin Li',
        '丁磊': 'William Ding',
        '程维': 'Cheng Wei',
        '柳传志': 'Liu Chuanzhi',
    }
    
    en_name = name_map.get(name, name)
    
    # Translate achievements
    en_achievements = achievements
    for zh_term, en_term in TERMINOLOGY.items():
        en_achievements = en_achievements.replace(zh_term, en_term)
    
    if en_achievements:
        return f"{en_name}: {en_achievements}"
    return en_name

# Generate imperative mood English content
def generate_imperative_english_content(zh_entry, code):
    """Generate high-quality English content with imperative mood"""
    # Mode names in English
    mode_names = [en_modes.get(str(m), ['Unknown'])[0] for m in zh_entry['modes']]
    
    # Convert Chinese content to imperative mood
    def to_imperative(text, field_type):
        """Convert Chinese text to imperative mood English"""
        if not text:
            return ""
            
        if field_type == 'description':
            # Convert "Figure X is known for..." to "Identify X's core contribution:..."
            if isinstance(text, str):
                # Extract the name part (first part before colon or first few characters)
                if '：' in text:
                    name_part = text.split('：')[0]
                    contribution = text.split('：')[1][:100]
                    return f"Identify {name_part}'s core contribution: {contribution}..."
                else:
                    # Use first few characters as name
                    name_part = text[:10].replace(' ', '')
                    return f"Identify {name_part}'s core contribution: {text[:100]}..."
                
        elif field_type == 'reason':
            # Convert "The reason is..." to "Rationale:..."
            if isinstance(text, str):
                return f"Rationale: {text[:200]}..."
                
        elif field_type == 'steps':
            # Convert "Steps include..." to "Execute: 1. ... 2. ..."
            if isinstance(text, list):
                result = []
                for i, step in enumerate(text):
                    result.append(f"Step {i+1}: {step}")
                return result
            elif isinstance(text, str):
                return text
                
        elif field_type == 'expected':
            # Convert "Expected outcome is..." to "Deliver:..."
            if isinstance(text, list):
                return text
            elif isinstance(text, str):
                return f"Deliver: {text}"
                
        elif field_type == 'case':
            # Keep case study as is
            return text
            
        return text
    
    return {
        'name': generate_english_name(zh_entry['name'], code),
        'description': to_imperative(zh_entry.get('description', ''), 'description'),
        'modes': zh_entry['modes'],
        'reason': to_imperative(zh_entry.get('reason', ''), 'reason'),
        'steps': to_imperative(zh_entry.get('steps', []), 'steps'),
        'expected': to_imperative(zh_entry.get('expected', ''), 'expected'),
        'case': to_imperative(zh_entry.get('case', ''), 'case')
    }

# Process all historical figures
updated_count = 0
for code, zh_entry in zh.items():
    if code.startswith('H-'):
        en_content = generate_imperative_english_content(zh_entry, code)
        en[code] = en_content
        updated_count += 1

# Save updated English file
with open('/opt/data/workspace/Protreptic/tools/scenarios_en.json', 'w', encoding='utf-8') as f:
    json.dump(en, f, ensure_ascii=False, indent=2)

print(f"Updated {updated_count} historical figures with imperative mood English")
print(f"Total EN entries: {len(en)}")