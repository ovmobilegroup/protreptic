import json

# Load existing data
with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)
with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)
with open('code_maps.json', 'r', encoding='utf-8') as f:
    cm = json.load(f)

# Phase 3 new figures: 45 entries (H-212 to H-256)
new_figures = [
    # H-212: 周敦颐
    {
        "code": "H-ZDY-212",
        "name_zh": "周敦颐：太极图说/理学源头/无欲/诚",
        "name_en": "Zhou Dunyi: Taiji Diagram/Neo-Confucianism Origin/Desirelessness/Sincerity",
        "desc_zh": "北宋哲学家，理学源头。著《太极图说》，立「无极而太极」本体论；以「诚」为工夫入手，建立「无欲→静→诚→动静」认知链条，完成从汉唐训诂到宋明义理的范式跃迁。",
        "desc_en": "Northern Song philosopher, originator of Neo-Confucianism. Authored 'Taiji Diagram', established 'wuji er taiji' ontology; took 'cheng' (sincerity) as cultivation entry, built 'desirelessness→stillness→sincerity→movement-stillness' cognitive chain, completing paradigm leap from Han-Tang exegesis to Song-Ming principle learning.",
        "modes": [22, 27, 21, 28, 35],
        "reason_zh": "周敦颐以《太极图说》建立宋明理学本体论，「诚」为工夫入手，完成从汉唐训诂到宋明义理的范式跃迁，其「无欲→诚→静→动静」认知链条为理学工程化奠基。",
        "reason_en": "Zhou Dunyi established Neo-Confucian ontology with 'Taiji Diagram', taking 'cheng' (sincerity) as cultivation entry, completing paradigm leap from Han-Tang exegesis to Song-Ming principle learning. His 'desirelessness→sincerity→stillness→movement-stillness' cognitive chain laid engineering foundation for Neo-Confucianism.",
        "steps_zh": ["本体锚定：确立「无极而太极」单一本体，统一阴阳/五行/鬼神/人物四大范畴", "协议标准化：提炼「诚者、圣人之本」核心算子，编码诚/静/动/无欲/寡欲五概念为修养向量空间", "工程化传承：确立「主静/立人极/无欲」三阶工夫次第，以濂溪书院规制固化传承标准", "动态校准：设计「动静无端/阴阳无始」动态平衡协议，以「诚」为锚点实现双轨并进", "系统集成：识别佛老虚无/功利科举/词章腐儒三大矛盾，以诚/静/无欲组合拳破解"],
        "steps_en": ["Ontological Anchoring: Establish 'wuji er taiji' single ontology, unify yin-yang/five elements/spirits/humans four categories", "Protocol Standardization: Extract 'cheng as sage's root' core operator, encode sincerity/stillness/movement/desirelessness/limited-desire five concepts as cultivation vector space", "Engineering Transmission: Establish 'stillness as master/standing human extreme/desirelessness' three-stage cultivation sequence, solidify transmission standards via Lianxi Academy regulations", "Dynamic Calibration: Design 'movement-stillness无端/yin-yang无始' dynamic balance protocol, dual-track parallelism anchored on 'sincerity'", "System Integration: Identify Buddhism-Daoist void/utilitarian exams/corrupt literary Confucians three contradictions, resolve with sincerity/stillness/desirelessness combination"],
        "expected_zh": "建立理学本体论框架，形成可标准化传承的修养工程体系",
        "expected_en": "Establish Neo-Confucian ontological framework, form standardized transmissible cultivation engineering system",
        "case_zh": "著《太极图说》《通书》，建濂溪书院，创「主静/无欲/寡欲」工夫法，直接影响二程/张载/朱熹/陆九渊/王阳明双系本体论共同源头。",
        "case_en": "Authored 'Taiji Diagram' and 'Tongshu', founded Lianxi Academy, created 'master stillness/desirelessness/limited desire' cultivation method, directly influencing Two Chengs/Zhang Zai/Zhu Xi/Lu Jiuyuan/Wang Yangming dual-system common ontological origin."
    },
    # H-213: 二程
    {
        "code": "H-CC-213",
        "name_zh": "二程(程颢/程颐)：理学正统/理一分殊/敬/天理/程门立雪",
        "name_en": "Two Chengs (Cheng Hao/Cheng Yi): Neo-Confucian Orthodoxy/One Principle Many Manifestations/Reverence/Heavenly Principle/Cheng Gate Standing in Snow",
        "desc_zh": "北宋哲学家，理学正统奠基人。确立「理一分殊」本体论，以「敬」为入手工夫，建立「主一无适」心法，完成从汉唐训诂到宋明义理的范式跃迁。程颢著《定性书》《认仁篇》，程颐著《伊川击壤集》《二程遗书》。",
        "desc_en": "Northern Song philosophers, founders of Neo-Confucian orthodoxy. Established 'one principle many manifestations' ontology, took 'reverence' as cultivation entry, built 'single-mindedness without deviation' heart-method, completing paradigm leap from Han-Tang exegesis to Song-Ming principle learning. Cheng Hao authored 'Dingxing Shu' and 'Renren Pian', Cheng Yi authored 'Yichuan Jipeng Ji' and 'Er Cheng Yishu'.",
        "modes": [22, 25, 27, 35, 37],
        "reason_zh": "二程确立「理一分殊」理学本体论，以「敬」为入手工夫，建立「主一无适」心法，完成从汉唐训诂到宋明义理的范式跃迁，其「主一无适/涵养/省察/力行」四阶工夫次第为理学标准入手工具。",
        "reason_en": "Two Chengs established 'one principle many manifestations' Neo-Confucian ontology, took 'reverence' as cultivation entry, built 'single-mindedness without deviation' heart-method, completing paradigm leap from Han-Tang exegesis to Song-Ming principle learning. Their 'single-mindedness/cultivation/examination/practice' four-stage cultivation sequence became standard Neo-Confucian entry tool.",
        "steps_zh": ["本体锚定：确立「理」为宇宙本体——「天地之性，即理也」，统一道/理/性/命四概念为单一本体论坐标系", "协议标准化：提炼「仁者以天地万物为一体」核心算子，将仁/义/礼/智/信五常编码为道德向量空间", "工程化传承：确立「主一无适/涵养/省察/力行」四阶工夫次第，以「程门立雪」师承仪式固化传承标准", "动态校准：设计「未发之中/发而中节/和」三层情感调节阈值，实现喜怒哀乐未发/发动态平衡", "系统集成：识别佛老虚无/词章腐儒/功利科举三大矛盾，以理气二元/心即理/敬以直内组合拳破解"],
        "steps_en": ["Ontological Anchoring: Establish 'li' as cosmic ontology—'heaven-earth nature is li', unify dao/li/xing/ming four concepts into single ontological coordinate system", "Protocol Standardization: Extract 'ren person takes heaven-earth all things as one body' core operator, encode ren/yi/li/zhi/xin five constants as moral vector space", "Engineering Transmission: Establish 'single-mindedness/cultivation/examination/practice' four-stage cultivation sequence, solidify transmission standards via 'Cheng Gate Standing in Snow' master-disciple ceremony", "Dynamic Calibration: Design 'not-yet-emitted center/emitted-hitting-center/harmony' three-layer emotional regulation thresholds, achieve joy-anger-sorrow-joy not-emitted/emitted dynamic balance", "System Integration: Identify Buddhism-Daoist void/corrupt literary Confucians/utilitarian exams three contradictions, resolve with li-qi dualism/heart-is-li/reverence-straightens-inner combination"],
        "expected_zh": "确立理学正统本体论与工夫体系，形成标准化师承传承范式",
        "expected_en": "Establish Neo-Confucian orthodox ontology and cultivation system, form standardized master-disciple transmission paradigm",
        "case_zh": "杨时/游酢/吕大临/尹焞「程门立雪」成师承仪式范式。其「理一分殊/敬/主一无适/程门立雪」四维融合，成宋明理学正统源头，朱熹/陆九渊/王阳明双系本体论共同源头。",
        "case_en": "Yang Shi/You Zuo/Lu Daling/Yin Zhi 'Cheng Gate Standing in Snow' became master-disciple ceremony paradigm. Their 'one principle many manifestations/reverence/single-mindedness/Cheng Gate Standing in Snow' four-dimensional fusion became Song-Ming Neo-Confucianism orthodox origin, Zhu Xi/Lu Jiuyuan/Wang Yangming dual-system common ontological origin."
    },
    # H-214: 朱熹
    {
        "code": "H-ZX-214",
        "name_zh": "朱熹：理学体系/四书章句集注/格物致知/理学集大成/紫阳夫子",
        "name_en": "Zhu Xi: Neo-Confucian System/Four Books Chapter-Annotation/Investigate Things Extend Knowledge/Neo-Confucianism Synthesis/Master Ziyang",
        "desc_zh": "南宋哲学家，理学集大成。编《四书章句集注》确立科举标准教材，建立「格物致知→诚意正心→修身齐家治国平天下」标准化工程流程，确立「存天理、灭人欲」道德工程化协议，建白鹿洞书院规制推广全国。",
        "desc_en": "Southern Song philosopher, synthesizer of Neo-Confucianism. Compiled 'Four Books Chapter-Annotation' establishing imperial examination standard textbook, built 'investigate things extend knowledge→make sincere rectify heart→cultivate self regulate family govern state pacify world' standardized engineering process, established 'preserve heavenly principle, extinguish human desires' moral engineering protocol, founded White Deer Grotto Academy regulations promoted nationwide.",
        "modes": [22, 25, 37, 1, 35],
        "reason_zh": "朱熹以《四书章句集注》确立科举标准教材，建立「格物致知→诚意正心→修身齐家治国平天下」标准化工程流程，确立「存天理、灭人欲」道德工程化协议，完成宋明理学集大成。",
        "reason_en": "Zhu Xi established imperial examination standard textbook with 'Four Books Chapter-Annotation', built 'investigate things extend knowledge→make sincere rectify heart→cultivate self regulate family govern state pacify world' standardized engineering process, established 'preserve heavenly principle, extinguish human desires' moral engineering protocol, completing Neo-Confucianism synthesis.",
        "steps_zh": ["本体锚定：确立「理」为宇宙本体——「理一分殊」，「理在物先」，统一太极/阴阳/五行/鬼神/人物五大范畴为单一本体论框架", "协议标准化：编《四书章句集注》确立标准教材，以大学/中庸/论语/孟子四书为核心课程体系，建立六步标准工程流程", "工程化传承：建立白鹿洞书院规制，确立讲学/藏书/祭祀/考校四职标准，推广至全国郡县学形成标准化教育网络", "动态校准：设计「存天理/灭人欲/格物/穷理/诚意/正心」六步道德工程协议，以「居敬/穷理」双轨并进", "系统集成：识别佛老虚无/陆王心学/功利科举三大矛盾，以理气二元/主敬穷理/四书正统组合拳固化正统地位"],
        "steps_en": ["Ontological Anchoring: Establish 'li' as cosmic ontology—'one principle many manifestations', 'li precedes things', unify taiji/yin-yang/five elements/spirits/humans five categories into single ontological framework", "Protocol Standardization: Compile 'Four Books Chapter-Annotation' standard textbook, take Great Learning/Doctrine of Mean/Analects/Mencius four books as core curriculum, build six-step standard engineering process", "Engineering Transmission: Establish White Deer Grotto Academy regulations, set teaching/books storage/sacrifice/examination four post standards, promote to national prefectural-county schools forming standardized education network", "Dynamic Calibration: Design 'preserve heavenly principle/extinguish human desires/investigate things/exhaust principles/make sincere/rectify heart' six-step moral engineering protocol, dual-track 'reverent abiding/exhaust principles' parallelism", "System Integration: Identify Buddhism-Daoist void/Lu-Wang heart learning/utilitarian exams three contradictions, solidify orthodox status with li-qi dualism/master reverence exhaust principles/four books orthodoxy combination"],
        "expected_zh": "完成理学标准化教材/工夫流程/道德协议/书院网络四维融合的集大成范式",
        "expected_en": "Complete synthesis paradigm of four-dimensional fusion: standardized textbook/cultivation process/moral protocol/academy network",
        "case_zh": "与陆九渊「鹅湖会议」辩论「格物/主敬/天理/人欲」，确立程朱理学正统。其「四书标准化/格物工程/存天理协议/书院网络」四维融合，成宋明理学集大成范式，影响朝鲜/日本/越南儒学圈全版图。",
        "case_en": "Debated 'investigate things/master reverence/heavenly principle/human desires' with Lu Jiuyuan at 'Ehu Meeting', establishing Cheng-Zhu Neo-Confucianism orthodoxy. Their 'four books standardization/investigate things engineering/preserve heavenly principle protocol/academy network' four-dimensional fusion became Neo-Confucianism synthesis paradigm, influencing Korea/Japan/Vietnam Confucian circles entire map."
    }
    # More figures will be added in batches...
]

# Only process if not already present
for fig in new_figures:
    code = fig["code"]
    if code not in zh:
        zh[code] = {
            "name": fig["name_zh"],
            "description": fig["desc_zh"],
            "modes": fig["modes"],
            "reason": fig["reason_zh"],
            "steps": fig["steps_zh"],
            "expected": fig["expected_zh"],
            "case": fig["case_zh"]
        }
        en[code] = {
            "name": fig["name_en"],
            "description": fig["desc_en"],
            "modes": fig["modes"],
            "reason": fig["reason_en"],
            "steps": fig["steps_en"],
            "expected": fig["expected_en"],
            "case": fig["case_en"]
        }
        cm["CODE_MAP"][code] = fig["name_zh"]
        cm["CODE_MAP_EN"][code] = fig["name_en"]

# Save
with open('scenarios_zh.json', 'w', encoding='utf-8') as f:
    json.dump(zh, f, ensure_ascii=False, indent=2)
with open('scenarios_en.json', 'w', encoding='utf-8') as f:
    json.dump(en, f, ensure_ascii=False, indent=2)
with open('code_maps.json', 'w', encoding='utf-8') as f:
    json.dump(cm, f, ensure_ascii=False, indent=2)

print(f"Added {len(new_figures)} new figures")
print(f"Total ZH: {len(zh)}")
print(f"Total EN: {len(en)}")
print(f"ZH H-: {sum(1 for k in zh if k.startswith('H-'))}")
print(f"EN H-: {sum(1 for k in en if k.startswith('H-'))}")
print(f"CODE_MAP: {len(cm['CODE_MAP'])}")
print(f"CODE_MAP_EN: {len(cm['CODE_MAP_EN'])}")