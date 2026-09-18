import json
import openpyxl
from collections import defaultdict

# Load data
with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)

with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)

with open('code_maps.json', 'r', encoding='utf-8') as f:
    cm = json.load(f)

# Add Mao Zedong to scenarios
mao_zh = {
    "name": "毛泽东：矛盾分析与实践论的战略大师",
    "description": "矛盾论/实践论/游击战/人民战争/长征/新民主主义革命",
    "modes": [1, 3, 4, 5, 6, 7, 14, 15, 22, 23, 25, 28, 29, 30, 31, 33, 35, 37, 38],
    "reason": "毛泽东《矛盾论》《实践论》核心思维：矛盾分析贯穿始终——识别主要矛盾（封建/帝国主义/官僚资本主义）、抓住主要矛盾的主要方面（无产阶级领导权）、运动战争→游击战争→运动战三阶段推进、农村包围城市战略路径、实事求是认识论指导军事/政治/经济实践、人民战争汇聚全民力量。",
    "steps": [
        "第1步：矛盾分析法——识别主要矛盾：半殖民地半封建社会的主要矛盾是帝国主义与中华民族、封建主义与人民大众的矛盾，次要矛盾是封建地主阶级与农民阶级、资产阶级与无产阶级矛盾",
        "第2步：抽象归纳法——提炼‘农村包围城市、武装夺取政权’战略路径：从井冈山建立根据地→中央苏区反围剿→长征转移→延安整风→抗日根据地建设→解放战争战略决战→建国",
        "第3步：系统思维法——构建‘党-军-民-政-经’五位一体革命体系：党的领导/人民军队/统一战线/根据地建设/土地改革，五大系统相互支撑形成革命合力",
        "第4步：思维模式选择——实事求是贯穿决策全过程：‘没有调查就没有发言权’、延安整风整顿作风、大跃进后‘三自一包’调整、读书运动纠正错误、文化大革命反思",
        "第5步：蛰伏积势思维——从井冈山一点星火到燎原之势：井冈山保存火种→长征二万五千里转移→延安十三年积蓄力量→三大战役决战→建国大业"
    ],
    "expected": [
        "建立新中国，完成民族独立和人民解放",
        "确立马克思主义中国化的毛泽东思想指导地位",
        "留下《矛盾论》《实践论》等哲学著作指导后世",
        "教训：大跃进/文革等错误导致严重损失，需警惕权力集中与个人崇拜"
    ],
    "case": "抗日战争时期（1937-1945）：面对日军强大攻势，毛泽东提出‘抗日民族统一战线’（统一战线法），制定‘游击战为主、运动战为辅’（运动歼灭法/灵活策略法），在敌后建立根据地（农村包围城市），实施‘百团大战’（运动歼灭法），坚持持久战（持久战思维），最终配合国际反法西斯战争取得胜利。建国后（1949-1976）：主导土地改革、抗美援朝、第一个五年计划、大跃进、人民公社化运动、文化大革命等重大历史进程，既有建国立业的丰功伟绩，也有晚年决策失误的深刻教训。"
}

mao_en = {
    "name": "Mao Zedong: Strategic Master of Contradiction Analysis and Practice Theory",
    "description": "On Contradiction/On Practice/Guerrilla Warfare/People's War/Long March/New Democratic Revolution",
    "modes": [1, 3, 4, 5, 6, 7, 14, 15, 22, 23, 25, 28, 29, 30, 31, 33, 35, 37, 38],
    "reason": "Mao Zedong's core thinking in 'On Contradiction' and 'On Practice': contradiction analysis throughout — identify principal contradiction (imperialism vs Chinese nation, feudalism vs masses), grasp principal aspect (proletarian leadership), three-stage advance (mobile war → guerrilla war → mobile war), rural encirclement strategy, seek truth from facts epistemology guiding military/political/economic practice, people's war mobilizing mass power.",
    "steps": [
        "Step 1: Contradiction Analysis — Identify principal contradiction: semi-colonial semi-feudal society's main contradiction is imperialism vs Chinese nation, feudalism vs masses; secondary: landlord vs peasants, bourgeoisie vs proletariat",
        "Step 2: Abstract Induction — Extract 'rural encirclement of cities, armed seizure of power' strategy: Jinggangshan base → Central Soviet anti-encirclement → Long March → Yan'an Rectification → Anti-Japanese bases → Liberation War strategic decisive battles → Founding",
        "Step 3: Systems Thinking — Build 'Party-Army-People-Politics-Economy' five-in-one revolutionary system: Party leadership / People's Army / United Front / Base Areas / Land Reform, five systems mutually reinforcing",
        "Step 4: Thinking Mode Selection — Seek truth from facts throughout decision-making: 'No investigation, no right to speak', Yan'an Rectification, Great Leap Forward correction with 'Three Self One Guarantee', Reading Campaign, Cultural Revolution reflection",
        "Step 5: Dormant Accumulation — From Jinggangshan spark to prairie fire: Jinggangshan preserve spark → Long March 25,000 li → Yan'an 13 years accumulation → Three Campaigns decisive battle → Founding"
    ],
    "expected": [
        "Founded PRC, achieved national independence and people's liberation",
        "Established Mao Zedong Thought as guiding ideology",
        "Left philosophical works On Contradiction/On Practice guiding later generations",
        "Lessons: Great Leap Forward/Cultural Revolution errors caused severe losses, warn against power concentration and personality cult"
    ],
    "case": "Anti-Japanese War (1937-1945): Facing powerful Japanese offensive, Mao proposed 'Anti-Japanese National United Front' (United Front), formulated 'guerrilla warfare main, mobile warfare auxiliary' (Mobile Warfare/Flexible Strategy), established base areas behind enemy lines (Rural Encirclement), implemented 'Hundred Regiments Offensive' (Mobile Warfare), insisted on Protracted War (Protracted War Thinking), ultimately cooperating with international anti-fascist war to win. Post-1949: Led Land Reform, Korean War, First Five-Year Plan, Great Leap Forward, People's Communes, Cultural Revolution — both monumental achievements in nation-building and profound lessons from late-life decision errors."
}

zh['H-MZ-141'] = mao_zh
en['H-MZ-141'] = mao_en

# Add to code_maps
cm['CODE_MAP']['H-MZ-141'] = '毛泽东：矛盾分析与实践论的战略大师'
cm['CODE_MAP_EN']['H-MZ-141'] = 'Mao Zedong: Strategic Master of Contradiction Analysis and Practice Theory'

# Save files
with open('scenarios_zh.json', 'w', encoding='utf-8') as f:
    json.dump(zh, f, ensure_ascii=False, indent=2)

with open('scenarios_en.json', 'w', encoding='utf-8') as f:
    json.dump(en, f, ensure_ascii=False, indent=2)

with open('code_maps.json', 'w', encoding='utf-8') as f:
    json.dump(cm, f, ensure_ascii=False, indent=2)

print("✅ Mao Zedong added to scenarios and code_maps")