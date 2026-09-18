#!/usr/bin/env python3
"""Fix H-LZ-169 in scenarios_zh.json and scenarios_en.json"""

import json
from pathlib import Path

BASE = Path("/opt/data/workspace/Protreptic/tools/json")

# Li Zhi scenario data
lizhi_scenario_zh = {
    "name": "李贽：童心说/破除儒教正统/个性解放/焚书藏书/心学异端",
    "description": "晚明异端思想家，以童心说为核心，批判程朱理学与儒教正统，主张个性解放与真情至上，被誉为中国最早的启蒙思想家。",
    "modes": [1, 5, 10, 26, 29],
    "reason": "李贽构建了以童心说为核心的反权威批判体系，将个体真实性、思想自由与物质实践有机结合，是Protreptic中反传统与思想解放的最完整案例。",
    "steps": [
        "第1步：童心奠基（M01童心法）——回归不受教条污染的'最初一念'，以绝对真诚作为价值判断的起点",
        "第2步：物质为本（M02穿衣吃饭法）——确认基本生存需求为一切价值基础，拒绝空谈心性",
        "第3步：异端立场（M03异端法）——主动拥抱边缘身份，将批判者立场转化为认知优势",
        "第4步：真情检验（M04真情法）——以内在真实情感为道德判断标准，揭露言行不一的虚伪",
        "第5步：思想解放（M05解放法）——质疑权威绝对性，恢复个人独立思考的判断权利",
        "第6步：实证验证（M06实证法）——以实际效用检验理论，强调经世致用而非空谈",
        "第7步：个性表达（M07个性法）——肯定个体独特价值，反对统一人格塑造",
        "第8步：平等原则（M08平等法）——破除等级差异，肯定女性智慧与能力",
        "第9步：顺应本性（M09自然法）——承认私欲正当性，设计顺应人性的制度",
        "第10步：动态历史观（M10反传统法）——以'与世推移'取代经典永恒论"
    ],
    "expected": [
        "建立以童心说为核心的完整反传统思想体系",
        "成为晚明思想启蒙运动的理论旗帜",
        "对日本明治维新产生深远影响",
        "为批判性思维提供系统化方法论",
        "开创中国思想史上的个性解放先河"
    ],
    "case": "李贽十二岁写《老农老圃论》，质疑孔子视农人为小人的言论；二十余年中举后多年担任低微官职，深受王阳明心学与泰州学派影响；晚年辞官寄居麻城芝佛院，著书讲学十余年；提出童心说、穿衣吃饭即是人伦物理等革命主张；在《藏书》中赞扬秦始皇为千古一帝、武则天为圣后；《焚书》猛烈抨击道学家阳为道学阴为富贵的虚伪；1602年被捕入狱后自刎而死，以'壮士不忘在沟壑，烈士不忘丧其元'明志。其思想影响晚明文人公安派、日本明治维新先驱吉田松阴，黄仁宇《万历十五年》专论其悲剧时代意义。",
    "description_zh": "【已完成】李贽（1527-1602），晚明著名思想家、文学家、史学家，初姓林后改姓李，字宏甫，号卓吾。福建泉州人，出身航海贸易世家。深受王阳明心学与泰州学派影响，以'异端'自居，提出童心说、穿衣吃饭即人伦物理等革命性主张，批判程朱理学与儒教正统，主张思想解放与个性自由。著作有《焚书》《藏书》《续焚书》《续藏书》等。1602年以'敢倡乱道、惑世诬民'罪名被捕入狱，自刎而死。其思想对晚明启蒙、日本明治维新、五四新文化运动均产生深远影响。"
}

lizhi_scenario_en = {
    "name": "Li Zhi: Childlike Mind Theory/Anti-Authority/Individual Liberation/Heterodox Thinker",
    "description": "Late Ming heterodox thinker who centered his thought on the Childlike Mind Theory, critiqued Cheng-Zhu Neo-Confucianism and Confucian orthodoxy, advocated individual liberation and authentic emotion as supreme values, hailed as China's earliest Enlightenment thinker.",
    "modes": [1, 5, 10, 26, 29],
    "reason": "Li Zhi constructed a comprehensive anti-authority critical system centered on the Childlike Mind Theory, integrating individual authenticity, intellectual freedom, and material practice. He is the most complete case in Protreptic for anti-tradition and thought liberation.",
    "steps": [
        "Step 1: Childlike Mind Foundation (M01) — Return to the 'first unfiltered thought' uncorrupted by dogma, use absolute authenticity as the starting point for value judgment",
        "Step 2: Material Foundation (M02) — Confirm basic survival needs as the foundation of all values, reject empty speculation about metaphysical principles",
        "Step 3: Heterodox Stance (M03) — Actively embrace marginal identity, transform critic's position into cognitive advantage",
        "Step 4: Authenticity Test (M04) — Use inner genuine emotion as moral judgment standard, expose hypocrisy of inconsistent words and deeds",
        "Step 5: Thought Liberation (M05) — Question the absolute authority of established norms, restore individual right to independent thinking",
        "Step 6: Practical Verification (M06) — Test theories by actual utility, emphasize statecraft over empty talk",
        "Step 7: Individual Expression (M07) — Affirm individual unique value, oppose standardized personality molding",
        "Step 8: Equality Principle (M08) — Break down hierarchical distinctions, affirm women's wisdom and capabilities",
        "Step 9: Conforming to Nature (M09) — Acknowledge legitimacy of natural desires, design systems that conform to human nature",
        "Step 10: Dynamic History (M10) — Replace classical eternalism with 'progressive history' worldview"
    ],
    "expected": [
        "Establish a complete anti-tradition thought system centered on Childlike Mind Theory",
        "Become the theoretical banner of late Ming intellectual enlightenment movement",
        "Profoundly influence Japan's Meiji Restoration",
        "Provide systematic methodology for critical thinking",
        "Pioneer individual liberation in Chinese intellectual history"
    ],
    "case": "Li Zhi wrote 'On Old Farmers and Gardeners' at age twelve, satirizing Confucius's view that farmers are petty people; passed the provincial exam in his twenties but held low-ranking posts for decades, deeply influenced by Wang Yangming's philosophy and the Taizhou School; retired late in life and settled at Zhifo Monastery in Macheng, writing and teaching for over a decade; propounded revolutionary ideas including Childlike Mind Theory and 'dressing and eating constitute human ethics'; praised Qin Shi Huang as 'emperor of the ages' and Wu Zetian as 'sage queen' in 'Records to Be Hidden'; vehemently attacked Neo-Confucian hypocrites in 'Books That Burn'; arrested in 1602 for 'propagating subversive doctrines' and committed suicide with a razor, saying 'a hero remembers not to lie unburied in ditches.' His thought influenced the late Ming Gong'an School, Japan's Meiji Restoration pioneer Yoshida Shoin, and Ray Huang's '1587, A Year of No Significance.'",
    "description_en": "[Completed] Li Zhi (1527-1602), prominent Ming Dynasty thinker, writer, and historian. Originally surnamed Lin, later changed to Li, courtesy name Hongfu, pseudonym Zhuo Wu. From Jinjiang, Quanzhou, Fujian, born into a maritime trade family. Deeply influenced by Wang Yangming's philosophy and the Taizhou School, he openly identified as a 'heterodox' thinker, propounding the Childlike Mind Theory and 'dressing and eating constitute human ethics,' critiquing Cheng-Zhu Neo-Confucianism and Confucian orthodoxy, advocating intellectual freedom and individual expression. Major works include 'Books That Burn,' 'Records to Be Hidden,' etc. Arrested in 1602 for 'subversive doctrines,' he committed suicide aged 76. His thought profoundly influenced late Ming enlightenment, Japan's Meiji Restoration, and China's May Fourth Movement."
}

# Update scenario_tags.json
with open(BASE / "scenario_tags.json", "r", encoding="utf-8") as f:
    scenario_tags = json.load(f)

scenario_tags["H-LZ-169"] = {
    "tags": [
        "童心说", "异端", "个性解放", "焚书藏书", "心学异端", "反权威",
        "思想解放", "批判性思维", "求真", "真实性", "自由意志",
        "女性平等", "男女平等", "反禁欲主义", "唯物主义",
        "经世致用", "晚明启蒙", "日本明治维新", "五四运动",
        "阳明心学", "泰州学派", "思想家", "文学家", "史学家",
        "明朝", "万历", "泉州", "福建", "历史人物", "伟大人物"
    ],
    "categories": [
        "思想家", "文学", "史学", "心学", "哲学", "社会批判",
        "思想启蒙", "明朝", "中国", "东亚", "中华文明",
        "历史人物", "伟大人物"
    ]
}
with open(BASE / "scenario_tags.json", "w", encoding="utf-8") as f:
    json.dump(scenario_tags, f, ensure_ascii=False, indent=2)
print("[OK] Updated scenario_tags.json with H-LZ-169")

# Update scenarios_zh.json
with open(BASE / "scenarios_zh.json", "r", encoding="utf-8") as f:
    scenarios_zh = json.load(f)

scenarios_zh["H-LZ-169"] = lizhi_scenario_zh
with open(BASE / "scenarios_zh.json", "w", encoding="utf-8") as f:
    json.dump(scenarios_zh, f, ensure_ascii=False, indent=2)
print("[OK] Updated scenarios_zh.json with H-LZ-169")

# Update scenarios_en.json
with open(BASE / "scenarios_en.json", "r", encoding="utf-8") as f:
    scenarios_en = json.load(f)

scenarios_en["H-LZ-169"] = lizhi_scenario_en
with open(BASE / "scenarios_en.json", "w", encoding="utf-8") as f:
    json.dump(scenarios_en, f, ensure_ascii=False, indent=2)
print("[OK] Updated scenarios_en.json with H-LZ-169")

# Verification
print("\n=== Verification ===")
with open(BASE / "scenario_tags.json") as f:
    tags = json.load(f)
    print(f"  scenario_tags.json: H-LZ-169 = {len(tags.get('H-LZ-169', {}).get('tags', []))} tags")

with open(BASE / "scenarios_zh.json") as f:
    zh = json.load(f)
    e = zh.get("H-LZ-169", {})
    print(f"  scenarios_zh.json: H-LZ-169 = {len(e.get('steps', []))} steps, case={'已完成' if e.get('description_zh', '').startswith('【已完成】') else 'missing'}")

with open(BASE / "scenarios_en.json") as f:
    en = json.load(f)
    e = en.get("H-LZ-169", {})
    print(f"  scenarios_en.json: H-LZ-169 = {len(e.get('steps', []))} steps, case={'OK' if 'Li Zhi' in e.get('case', '') else 'missing'}")

print("\n=== Done ===")
