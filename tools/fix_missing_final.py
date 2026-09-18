import json

# Load existing scenarios
with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    scenarios_zh = json.load(f)

with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    scenarios_en = json.load(f)

# Add missing Chinese scenarios
missing_zh = {
    "H-CYK-66": {
        "name": "陈寅恪：独立精神的学术方法论大师",
        "description": "独立之精神自由之思想/考据与解释/柳如是传/元白诗笺/学术方法论",
        "modes": [30, 25, 29, 28, 35],
        "reason": "陈寅恪'独立之精神、自由之思想'，核心思维：学术方法论的理论自觉与独立人格——'不信仰、不迷信、不盲从、不盲动'、'不以人废言、不以言废人'。著《柳如是传》《金明馆丛稿二编》《隋唐制度渊源论略》《唐代政治史论草稿》。'以诗证史、以史证诗'、'理解之同情'、多语言/多证据/多方法三重验证。'学问无第二、只是求真'、学术良心典范。",
        "steps": [
            "第1步：抽象归纳法——多元证据法：文献/碑志/敦煌遗书/诗词/绘画/钱币/墓志/多源互证、三重验证",
            "第2步：系统思维法——理解之同情：'读史者、必有理解之同情'、设身处地还原历史现场/主观意图/结构制约",
            "第3步：总体性思维法——敦煌学开创：敦煌遗书/佛教文献/社会经济/民族关系/多学科交叉/开创敦煌学",
            "第4步：思维模式选择——独立精神：'不信仰、不迷信、不盲从、不盲动'、'不以人废言、不以言废人'、学术良心/思想自由",
            "第5步：蛰伏积势——晚年著述：抗战迁徙/香港/广州/贵州/失明/口述《柳如是传》/《陈寅恪先生遗著》/学术遗产"
        ],
        "expected": [
            "《柳如是传》/《元白诗笺证稿》/《隋唐制度渊源论略》成学术经典",
            "多元证据法/理解之同情/独立精神成现代人文学科方法论标杆",
            "教训：晚年失明/家国破碎/学术孤独/思想自由代价高昂"
        ],
        "case": "柳如是传（1940s）：口述/罗香林记录/三十万字/考证柳如是生平/钱谦益/南明/清初/女性/知识分子/多源互证/理解之同情。元白诗笺（1930s）：元稹/白居易诗作/史料/考证/互证/制度演变/诗史互证。隋唐制度渊源论略（1940s）：三省六部/九寺五监/选举/赋税/兵制/制度演变/制度史学。晚年口述、罗香林记录、朱维铮整理。结果：独立精神/自由思想/多元证据法成学术标杆。"
    },
    "H-LQC-68": {
        "name": "梁启超：新史学与变法思维的启蒙先驱",
        "description": "中国历史研究法/新民说/变法维新/饮冰室合集/启蒙思想",
        "modes": [22, 25, 38, 28, 35],
        "reason": "梁启超'少年中国说'、'新民说'、'中国历史研究法'，核心思维：新史学方法论与变法启蒙的双重突破——著《中国历史研究法》创'新史学'：'史者、考之于古、以验之今、以征之未来'。《新民说》'欲新中国、必先新民'、公民意识/公德/公共精神。《饮冰室合集》百卷、戊戌变法/百日维新/谭嗣同/谭延闿/徐佛苏/逃亡日本/办《清议报》《新民丛报》。'革命非杀人放火、革命乃旧制改良'。",
        "steps": [
            "第1步：抽象归纳法——新史学三纲：'史者、考之于古、以验之今、以征之未来'、考/验/征三步法/史学功能再定位",
            "第2步：系统思维法——新民说体系：新民/新道德/新学问/新宗教/新文学/新艺术/新生活/新国家/全方位新民培育/公民社会建构",
            "第3步：自然选择法——变法实践：戊戌变法/强学会/时务报/当官/逃亡/办报/新民丛报/启蒙/激进/保守/三派博弈/百日维新/六君子/流亡",
            "第4步：反馈回路法——饮冰室合集：百卷/诗文/论说/史学/哲学/政治/文学/自述/反思/百年再版/影响鲁迅/胡适/毛泽东/启蒙一代",
            "第5步：蛰伏积势——晚年反思：'吾以所受于先生者、推而广之'、师承康有为/决裂康有为/津门病逝/遗嘱'必不使中国亡于吾手'、精神遗产"
        ],
        "expected": [
            "《中国历史研究法》成新史学纲领/《新民说》成启蒙运动纲领/《饮冰室合集》成近代思想宝库",
            "新史学/新民说/变法/启蒙四大贡献/影响鲁迅/胡适/毛泽东/一代知识分子",
            "教训：激进与保守张力/变法失败/流亡生涯/思想转向复杂/晚年佛教倾向"
        ],
        "case": "中国历史研究法（1922）：'考之于古、验之于今、征之于未来'、三步法/新史学纲领。新民说（1902）：新民/新道德/新学问/新宗教/新文学/新艺术/新生活/新国家/全方位新民。戊戌变法（1898）：强学会/时务报/百日维新/六君子/梁逃日本。饮冰室合集（1920s-1930s）：百卷/诗文/论说/史学/哲学/政治/文学/自述/反思。晚年：'吾以所受于先生者、推而广之'、决裂康有为/津门病逝。结果：新史学/新民说/变法/启蒙四大贡献、影响鲁迅/胡适/毛泽东一代知识分子。"
    }
}

# Add missing English scenarios
missing_en = {
    "H-CYK-66": {
        "name": "Chen Yinke: Independent Spirit Academic Methodology Master",
        "description": "Independent Spirit Free Thought / Evidential Research and Interpretation / Liu Rushi Biography / Yuan Bai Poetry Annotations / Academic Methodology",
        "modes": [30, 25, 29, 28, 35],
        "reason": "Chen Yinke 'independent spirit, free thought', core mindset: academic methodology theoretical self-awareness and independent personality - 'no belief, no superstition, no blind following, no blind action', 'not discard words because of person, not discard person because of words'. Wrote 'Liu Rushi Biography', 'Gold Bright Hall Collection Second Edition', 'Sui Tang System Origins Brief', 'Tang Political History Draft'. 'Use poetry verify history, use history verify poetry', 'understanding sympathy', multi-language/multi-evidence/multi-method triple verification. 'Learning no second, only seek truth', academic conscience model.",
        "steps": [
            "Step 1: Abstract Induction - Multi-source Evidence: documents/inscriptions/Dunhuang documents/poetry/pain/painting/coins/epitaphs/multi-source mutual verification/triple verification",
            "Step 2: Systems Thinking - Understanding Sympathy: 'history readers must have understanding sympathy', empathize restore historical scene/subjective intent/structural constraints",
            "Step 3: Holistic Thinking - Dunhuang Studies Founding: Dunhuang documents/Buddhist literature/social economy/ethnic relations/multi-discipline crossover/founded Dunhuang studies",
            "Step 4: Thinking Mode Selection - Independent Spirit: 'no belief, no superstition, no blind following, no blind action', 'not discard words because of person, not discard person because of words', academic conscience/ideological freedom",
            "Step 5: Dormant Accumulation - Late Authorship: war relocation/Hong Kong/Guangzhou/Guizhou/blindness/oral 'Liu Rushi Biography'/'Chen Yinke Teacher Legacy'/academic heritage"
        ],
        "expected": [
            "'Liu Rushi Biography'/'Yuan Bai Poetry Annotations'/'Sui Tang System Origins' become academic classics",
            "Multi-evidence method/understanding sympathy/independent spirit become modern humanities methodology benchmark",
            "Lessons: late years blind/home country broken/academic loneliness/independent spirit price high"
        ],
        "case": "Liu Rushi Biography (1940s): oral/Luo Honglin record/300k chars/source Liu Rushi life/Qian Qianyi/Southern Ming/Qing/women/intellectual/three-in-one source inter-verification/understanding sympathy. Yuan Bai Poetry Annotations (1930s): Yuan Zhen/Bai Juyi poems/sources/verification/mutual verification/institutional evolution/poetry-history mutual evidence. Sui Tang System Origins (1940s): three departments six ministries/nine temples five supervisions/selection/taxation/military/institutional evolution/institutional history. Late years oral/Luo Honglin record/Zhu Weizheng organize. Result: independent spirit/free thought/multi-evidence method become Chinese academic methodology benchmark."
    },
    "H-LQC-68": {
        "name": "Liang Qichao: New Historiography Reform Enlightenment Pioneer",
        "description": "Chinese History Research Method / New People Discourse / Reform Restoration / Ice Drinking Room Collection / Enlightenment Thought",
        "modes": [22, 25, 38, 28, 35],
        "reason": "Liang Qichao 'Young China Say', 'New People Say', 'Chinese History Research Method', core mindset: new historiography methodology and reform enlightenment dual breakthrough - wrote 'Chinese History Research Method' created 'new historiography': 'history is, investigate ancient, verify present, predict future'. 'New People Say' 'want new China, must first new people', citizen consciousness/public virtue/public spirit. 'Ice Drinking Room Collection' hundred volumes, 1898 reform/hundred days reform/Tan Sitong/Tan Yantong/Xu Fosu/escape Japan/run 'clear discourse report''new people monthly'. 'revolution not kill burn, revolution is old system reform'.",
        "steps": [
            "Step 1: Abstract Induction - New Historiography Three Principles: 'history is, investigate ancient, verify present, predict future', investigate/verify/predict three steps/historiography function repositioning",
            "Step 2: Systems Thinking - New People System: new people/new morality/new knowledge/new religion/new literature/new art/new life/new state/full-dimensional new people cultivation/public citizen society construction",
            "Step 3: Natural Selection - Reform Practice: 1898 reform/strong learning society/current affairs report/official/escape/run newspaper/ice drinking room collection/enlightenment/radical/conservative/three factions struggle/hundred days reform/six gentlemen/exile",
            "Step 4: Feedback Loop - Ice Drinking Room Collection: hundred volumes/poetry/prose/historiography/philosophy/politics/literature/self-description/reflection/hundred years reprint/influence Lu Xun/Hu Shi/Mao Zedong/enlightenment generation",
            "Step 5: Dormant Accumulation - Late Reflection: 'what I received from teacher, extended and expanded', teacher Kang Youwei/break Kang Youwei/Jinmen death/will 'must not let China perish in my hands', spiritual legacy"
        ],
        "expected": [
            "'Chinese History Research Method' became new historiography outline/'New People Discourse' became enlightenment movement outline/'Ice Drinking Room Collection' became modern thought treasure",
            "New historiography/new people/reform/enlightenment four major contributions/influence Lu Xun/Hu Shi/Mao Zedong/generation intellectuals",
            "Lessons: radical vs conservative tension/reform failed/exile life/thought shift complex/late years Buddhism tendency"
        ],
        "case": "Chinese history research method (1922): 'investigate ancient, verify present, predict future', three steps/new historiography outline. New people say (1902): new people/new morality/new knowledge/new religion/new literature/new art/new life/new state/full-dimensional new people. 1898 reform (1898): strong learning society/current affairs report/hundred days reform/six gentlemen/Liang escape Japan. Ice drinking room collection (1920s-1930s): hundred volumes/poetry/prose/historiography/philosophy/politics/literature/self-narration/reflection. Late years: 'I with received from teacher, extended and expanded', break Kang Youwei/Jinmen death. Result: new historiography/new people/reform/enlightenment four contributions, influence Lu Xun/Hu Shi/Mao Zedong generation intellectuals."
    }
}

# Add to scenarios
scenarios_zh.update(missing_zh)
scenarios_en.update(missing_en)

# Save
with open('scenarios_zh.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios_zh, f, ensure_ascii=False, indent=2)

with open('scenarios_en.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios_en, f, ensure_ascii=False, indent=2)

print(f'Updated scenarios_zh.json: {len(scenarios_zh)} total scenarios')
print(f'Updated scenarios_en.json: {len(scenarios_en)} total scenarios')