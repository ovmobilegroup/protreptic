import json

# Load existing scenarios
with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    scenarios_zh = json.load(f)

with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    scenarios_en = json.load(f)

# 3 final paradigm figures - Chinese
new_zh = {
    "H-LL-48": {
        "name": "李悝：法家鼻祖的变法奠基者",
        "description": "法经六篇/平籴法/尽力地力/战国变法鼻祖/富国强兵",
        "modes": [32, 19, 20, 28, 34],
        "reason": "李悝'法经'六篇（盗/贼/囚/捕/杂/具），核心思维：法治国家的制度化奠基——魏文侯任相，推'平籴法'（丰年平价收粮、荒年平价粜粮）、'尽力地力'（按地力高低定税、奖励垦荒）、'教战法'（军功授爵、明赏罚）。'以法为教'、'废私学、以法吏为师'，为商鞅/韩非/秦始皇法治体系奠基。",
        "steps": [
            "第1步：程序正义法——立法公开、执法严明、司法独立、普遍平等，'法不阿贵、绳不挠曲'",
            "第2步：边际思维——平籴法：丰年高价收粮保农、荒年低价粜粮惠民、国家调节粮价稳定、防商人囤积居奇",
            "第3步：激励机制——尽力地力：按地力高下定税额、超额奖励、不及减免、激励农民垦荒增产",
            "第4步：制度化制衡——军功爵制：以首级数授爵/赏田/赐宅、废世卿世禄、建立'以功取贵'选拔机制",
            "第5步：格局授权——专业分工：李悝掌政、吴起掌兵、翟璜掌外交、魏文侯'择人任势'、君臣分工明确"
        ],
        "expected": [
            "魏国称霸中原、'魏氏兵、天下劲'、为秦统六国奠基",
            "'法经'成中国成文法典鼻祖、平籴/尽力地力/军功制成历代变法标配",
            "教训：法家重刑轻德、吴起变法触动贵族利益被迫出奔、魏国后期衰落"
        ],
        "case": "李悝变法（前400s）：魏文侯任李悝相，推行：1)法经六篇：盗/贼/囚/捕/杂/具，废除贵族特权、法律面前人人平等。2)平籴法：丰年官府高价收粮入仓、荒年低价粜粮平物价、杜绝商人囤积。3)尽力地力：按土地肥瘠定税、上田亩税多、下田亩税少、垦荒免税三年、超产奖励。4)军功爵制：斩首一级爵一级、赏田十亩、宅一区、废除世卿世禄。结果：魏国富国强兵、兵精粮足、称霸中原百年、为秦统一奠基。"
    },
    "H-SW-49": {
        "name": "孙武：兵法集大成的战略欺诈大师",
        "description": "兵者诡道/知己知彼/以正合以奇胜/不战而屈人之兵/九地九变",
        "modes": [13, 1, 11, 14, 35],
        "reason": "孙武'兵者、国之大死生之地、存亡之道、不可不察也'，核心思维：战略欺诈与全胜思维的集大成——'兵者诡道也'、'能而示不能、用而示不用、近而示远、远而示近'、'知己知彼百战不殆'、'不战而屈人之兵善之善者也'。'以正合、以奇胜'、'攻其无备、出其不意'、'九地九变、因利而制权'。将战争抽象为博弈模型、心理战/谋略战/战略欺诈系统化。",
        "steps": [
            "第1步：全胜思维——不战而胜：'百战百胜非善之善、不战而屈人之兵善之善者'、以谋略/外交/心理/经济手段达成战略目标",
            "第2步：矛盾分析法——知己知彼：'知彼知己百战不殆、不知彼知己一胜一负、不知彼不知己每战必殆'、情报先行、研判敌我优劣",
            "第3步：全胜思维——以正合以奇胜：'战正合、胜奇'、正兵牵制、奇兵致胜、虚实转化、出其不意",
            "第4步：战争重心法——攻其无备：'避实击虚、攻其不备、出其不意'、九地九变、因地制宜、因利而制权",
            "第5步：蛰伏积势——示形诱敌：'能而示不能、用而示不用、近而示远、远而示近'、诱敌深入、以逸待劳、以主待客"
        ],
        "expected": [
            "《孙子兵法》成世界军事经典、影响东亚/欧美军事/商业/竞争战略",
            "全胜/知己知彼/以正奇/虚实/攻心成战略思维通用词汇",
            "教训：过度强调欺诈/心理战、轻视后勤/工程/技术硬实力、后世易曲解为纯谋略"
        ],
        "case": "孙子兵法应用：吴王阖闾用孙子练兵、破楚入郢（前506）；田忌赛马'以下驷对上驷、上驷对中驷、中驷对下驷'、以奇制胜；越王勾践卧薪尝胆、范蠡用孙子水战策灭吴；曹操赤壁前'孙子兵法'研习、赤壁败因轻视'虚实'、'铁索连舟'成奇兵被火攻；现代商业：乔布斯'现实扭曲力场'、马云'以奇制胜'、张一鸣'算法推荐'为奇兵。"
    },
    "H-ZZJ-50": {
        "name": "张仲景：医学系统论的辨证论治鼻祖",
        "description": "伤寒杂病论/辨证论治/方证对应/系统医学/方药对症",
        "modes": [12, 1, 25, 28, 35],
        "reason": "张仲景'伤寒杂病论'六卷（伤寒/杂病各三卷），核心思维：系统医学的辨证论治体系——'辨阴阳、别表里、察虚实、辨寒热'、'六经辨证'（太阳/阳明/少阴/太阴/少阳/厥阴）、'方证对应'（证候决定方药、同病异治/异病同治）。'上工治未病、中工治欲病、下工治已病'。建立'望闻问切'四诊合参、'辨证论治'临床思维闭环。为中医乃至系统医学奠基。",
        "steps": [
            "第1步：系统思维法——六经辨证：太阳/阳明/少阴/太阴/少阳/厥阴六经传变规律、表里寒热虚实辨识、建立疾病演进动态模型",
            "第2步：矛盾分析法——辨证论治：'辨阴阳、别表里、察虚实、辨寒热'、找主要矛盾（寒/热/虚/实/表/里）、对症下药",
            "第3步：抽象归纳法——方证对应：同病异治（同伤寒、表实用麻黄汤、表虚用桂枝汤）、异病同治（霍乱/伤寒同属阳明腑实、同用大承气汤）",
            "第4步：反馈回路法——四诊合参：望/闻/问/切四诊合参、证候确立→方药选用→服药观察→证候变化→调整方药、临床闭环",
            "第5步：蛰伏积势——上工治未病：'上工治未病、中工治欲病、下工治已病'、预防医学/亚健康干预/早期干预、系统工程思维"
        ],
        "expected": [
            "《伤寒杂病论》成中医临床圣经、方剂学/临床诊断学基石",
            "辨证论治/六经辨证/方证对应成中医核心方法论、影响日/韩/越医学",
            "教训：理论体系封闭/缺解剖解剖/缺微生物学/近代需结合现代医学验证"
        ],
        "case": "伤寒论六经辨证：太阳病（表证）、阳明病（里实热）、少阴病（里寒虚）、太阴病（脾胃虚寒）、少阳病（半表半里）、厥阴病（阴阳两竭）。经方：麻黄汤/桂枝汤/大青龙汤/白虎汤/大承气汤/小柴胡汤/四逆汤/乌梅丸等113方。辨证论治：同病异治（伤寒表实用麻黄、表虚用桂枝）、异病同治（伤寒/霍乱同属阳明腑实、同用大承气汤）。结果：中医临床诊断/治疗标准化、方剂学建立。"
    }
}

# Add to Chinese scenarios
scenarios_zh.update(new_zh)

# Save
with open('scenarios_zh.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios_zh, f, ensure_ascii=False, indent=2)

print(f"Updated scenarios_zh.json: {len(scenarios_zh)} total scenarios")

# English versions
new_en = {
    "H-LL-48": {
        "name": "Li Kui: Legalist Founder of Reform Foundation",
        "description": "Six Chapters of Book of Law / Equal Transport Law / Exhaust Land Power / Warring States Reform Ancestor / Enrich State Strengthen Army",
        "modes": [32, 19, 20, 28, 34],
        "reason": "Li Kui 'Book of Law' six chapters (theft/bandit/imprisonment/arrest/miscellaneous/tools), core mindset: institutionalized foundation of rule of law state — served as Wei Wenhou's chancellor, promoted 'Equal Transport Law' (state purchases grain at stable price in harvest, sells at stable price in famine), 'Exhaust Land Power' (tax by land fertility, reward reclamation), 'Teaching Warfare Law' (military merit enfeoffment, clear rewards punishments). 'Law as teaching', 'abolish private learning, make legal officials teachers', laid foundation for Shang Yang/Han Fei/Qin Shi Huang legal system.",
        "steps": [
            "Step 1: Procedural Justice — Public legislation, strict enforcement, independent judiciary, universal equality, 'law does not favor nobility, rope does not bend for curves'",
            "Step 2: Marginal Thinking — Equal Transport Law: bumper year state buys grain at high price protecting farmers, famine year sells at low price benefiting people, state regulates grain price stability, prevents merchant hoarding",
            "Step 3: Incentive Mechanism — Exhaust Land Power: tax set by land fertility, over-production rewarded, under-production reduced, incentivizes farmers to reclaim wasteland increase yield",
            "Step 4: Institutional Checks — Military Merit Rank System: enfeoffment by enemy heads count, reward land/grant residence, abolish hereditary nobility/salaries, establish 'merit-based ennoblement' selection mechanism",
            "Step 5: Strategic Delegation — Professional Division: Li Kui manages civil, Wu Qi manages military, Zhai Huang manages diplomacy, Wei Wenhou 'select people assign situations', clear君臣分工"
        ],
        "expected": [
            "Wei dominated Central Plains, 'Wei army, world's elite', laid foundation for Qin unification",
            "'Book of Law' became China's first written code ancestor, Equal Transport/Exhaust Land Power/Military Merit became standard reform tools for dynasties",
            "Lessons: Legalism heavy punishment light virtue, Wu Qi reform touched noble interests forced to flee, Wei later declined"
        ],
        "case": "Li Kui Reform (400s BC): Wei Wenhou appointed Li Kui chancellor, implemented: 1) Book of Law six chapters: theft/bandit/imprisonment/arrest/miscellaneous/tools, abolished noble privileges, equality before law. 2) Equal Transport Law: bumper year state buys high stores in granary, famine year sells low stabilizes prices, eliminates merchant hoarding. 3) Exhaust Land Power: tax by land fertility, upper field more tax, lower field less tax, reclamation tax-free three years, over-production rewarded. 4) Military Merit Rank: one head one rank, reward ten mu land, one residence, abolished hereditary nobility. Result: Wei rich state strong army, elite soldiers, dominated Central Plains century, laid foundation for Qin unification."
    },
    "H-SW-49": {
        "name": "Sun Wu: Military Strategy Deception Master",
        "description": "Warfare Is Deception / Know Self Know Enemy / Win by Orthodox and Unorthodox / Subdue Enemy Without Fighting / Nine Grounds Nine Changes",
        "modes": [13, 1, 11, 14, 35],
        "reason": "Sun Wu 'Warfare is the great affair of state, ground of life and death, way of survival and extinction, cannot be unexamined'. Core mindset: strategic deception and total victory thinking culmination — 'Warfare is deception', 'able show unable, use show not use, near show far, far show near', 'know self know enemy hundred battles not peril', 'subdue enemy without fighting is supreme excellence'. 'Win by orthodox, victory by unorthodox', 'strike unprepared, appear unexpected', 'nine grounds nine changes, adapt advantage control authority'. Abstracted war as game model, psychological/strategic/deception systematized.",
        "steps": [
            "Step 1: Total Victory Mindset — Victory Without Fighting: 'Hundred battles hundred victories not best, subdue enemy without fighting is best', achieve strategic goals via strategy/diplomacy/psychology/economy",
            "Step 2: Contradiction Analysis — Know Self Know Enemy: 'Know enemy know self hundred battles not peril, unknown enemy know self one win one loss, unknown enemy unknown self every battle peril', intelligence first, assess strengths weaknesses",
            "Step 3: Total Victory Mindset — Orthodox Unorthodox: 'Battle by orthodox, win by unorthodox', orthodox troops pin down, unorthodox troops win, virtual real transform, strike unexpected",
            "Step 4: Center of Gravity — Strike Unprepared: 'Avoid real strike void, strike unprepared, appear unexpected', nine grounds nine changes, adapt to terrain, adapt advantage control authority",
            "Step 5: Dormant Accumulation — Deceive Appearance: 'Able show unable, use show not use, near show far, far show near', lure enemy deep, await leisure, host await guest"
        ],
        "expected": [
            "'Art of War' became world military classic, influenced East Asia/West military/business/competition strategy",
            "Total Victory/Know Self Know Enemy/Orthodox Unorthodox/Virtual Real/Strike Heart became strategic thinking universal vocabulary",
            "Lessons: overemphasis deception/psychological war, neglect logistics/engineering/technical hard power, later generations misinterpret as pure strategy"
        ],
        "case": "Art of War applications: Wu King Helu used Sun Wu train troops, broke Chu entered Ying (506 BC); Tian Ji horse racing 'inferior vs superior, superior vs middle, middle vs inferior' win by unorthodox; Goujian slept on firewood tasted gall, Fan Li used Sun Wu naval strategy destroyed Wu; Cao Cao before Red Cliff studied 'Art of War', Red Cliff defeat due to neglecting 'virtual real', 'chained ships' became unorthodox weapon burned; Modern business: Jobs 'reality distortion field', Ma Yun 'win by unorthodox', Zhang Yiming 'algorithmic recommendation' as unorthodox weapon."
    },
    "H-ZZJ-50": {
        "name": "Zhang Zhongjing: Medical Systems Theory Ancestor of Syndrome Differentiation",
        "description": "Treatise on Cold Damage and Miscellaneous Diseases / Syndrome Differentiation Treatment / Formula-Syndrome Correspondence / Systems Medicine / Formula-Symptom Matching",
        "modes": [12, 1, 25, 28, 35],
        "reason": "Zhang Zhongjing 'Treatise on Cold Damage and Miscellaneous Diseases' six volumes (Cold Damage/Miscellaneous three each), core mindset: systems medicine syndrome differentiation system — 'differentiate yin yang, distinguish exterior interior, examine deficiency excess, differentiate cold heat', 'Six Channels Differentiation' (Taiyang/Yangming/Shaoyin/Taiyin/Shaoyang/Jueyin), 'Formula-Syndrome Correspondence' (syndrome determines formula, same disease different treatment/different diseases same treatment). 'Superior doctor treats pre-disease, middle doctor treats impending disease, inferior doctor treats manifest disease'. Established 'inspection auscultation inquiry palpation' four diagnostics integration, 'syndrome differentiation treatment' clinical thinking loop. Foundation for Chinese medicine and systems medicine.",
        "steps": [
            "Step 1: Systems Thinking — Six Channels Differentiation: Taiyang/Yangming/Shaoyin/Taiyin/Shaoyang/Jueyin six channels transmission rules, exterior/interior/cold/heat/deficiency/excess identification, established disease progression dynamic model",
            "Step 2: Contradiction Analysis — Syndrome Differentiation: 'Differentiate yin yang, distinguish exterior interior, examine deficiency excess, differentiate cold heat', find principal contradiction (cold/heat/deficiency/excess/exterior/interior), treat accordingly",
            "Step 3: Abstract Induction — Formula-Syndrome Correspondence: Same disease different treatment (same cold damage, exterior real use Ma Huang Tang, exterior deficiency use Gui Zhi Tang), Different diseases same treatment (Cholera/Cold Damage both Yangming fu real, both use Da Cheng Qi Tang)",
            "Step 4: Feedback Loops — Four Diagnostics Integration: Inspection/Auscultation/Inquiry/Palpation four diagnostics combined, syndrome established -> formula selection -> medication observation -> syndrome change -> formula adjustment, clinical loop",
            "Step 5: Dormant Accumulation — Superior Doctor Treats Pre-Disease: 'Superior doctor treats pre-disease, middle doctor treats impending disease, inferior doctor treats manifest disease', preventive medicine/sub-health intervention/early intervention, systems engineering thinking"
        ],
        "expected": [
            "'Treatise on Cold Damage and Miscellaneous Diseases' became Chinese medicine clinical bible, formula science/clinical diagnosis foundation",
            "Syndrome Differentiation/Six Channels/Formula-Syndrome became Chinese medicine core methodology, influenced Japan/Korea/Vietnam medicine",
            "Lessons: theoretical system closed/lack anatomy/lack microbiology/modern needs combine modern medicine verification"
        ],
        "case": "Cold Damage Six Channels: Taiyang (exterior), Yangming (interior real heat), Shaoyin (interior cold deficiency), Taiyin (spleen stomach deficiency cold), Shaoyang (half exterior half interior), Jueyin (yin yang both exhausted). Classic Formulas: Ma Huang Tang/Gui Zhi Tang/Da Qing Long Tang/Bai Hu Tang/Da Cheng Qi Tang/Xiao Chai Hu Tang/Si Ni Tang/Wu Mei Wan etc 113 formulas. Syndrome Differentiation: Same disease different treatment (Cold Damage exterior real Ma Huang, exterior deficiency Gui Zhi), Different diseases same treatment (Cold Damage/Cholera both Yangming fu real, both use Da Cheng Qi Tang). Result: Chinese medicine clinical diagnosis/treatment standardized, formula science established."
    }
}

# Add to Chinese scenarios
scenarios_zh.update(new_zh)

# Save
with open('scenarios_zh.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios_zh, f, ensure_ascii=False, indent=2)

print(f"Updated scenarios_zh.json: {len(scenarios_zh)} total scenarios")

# English versions
new_en = {
    "H-LL-48": {
        "name": "Li Kui: Legalist Founder of Reform Foundation",
        "description": "Six Chapters of Book of Law / Equal Transport Law / Exhaust Land Power / Warring States Reform Ancestor / Enrich State Strengthen Army",
        "modes": [32, 19, 20, 28, 34],
        "reason": "Li Kui 'Book of Law' six chapters (theft/bandit/imprisonment/arrest/miscellaneous/tools), core mindset: institutionalized foundation of rule of law state — served as Wei Wenhou's chancellor, promoted 'Equal Transport Law' (state purchases grain at stable price in harvest, sells at stable price in famine), 'Exhaust Land Power' (tax by land fertility, reward reclamation), 'Teaching Warfare Law' (military merit enfeoffment, clear rewards punishments). 'Law as teaching', 'abolish private learning, make legal officials teachers', laid foundation for Shang Yang/Han Fei/Qin Shi Huang legal system.",
        "steps": [
            "Step 1: Procedural Justice — Public legislation, strict enforcement, independent judiciary, universal equality, 'law does not favor nobility, rope does not bend for curves'",
            "Step 2: Marginal Thinking — Equal Transport Law: bumper year state buys grain at high price protecting farmers, famine year sells at low price benefiting people, state regulates grain price stability, prevents merchant hoarding",
            "Step 3: Incentive Mechanism — Exhaust Land Power: tax set by land fertility, over-production rewarded, under-production reduced, incentivizes farmers to reclaim wasteland increase yield",
            "Step 4: Institutional Checks — Military Merit Rank System: enfeoffment by enemy heads count, reward land/grant residence, abolish hereditary nobility/salaries, establish 'merit-based ennoblement' selection mechanism",
            "Step 5: Strategic Delegation — Professional Division: Li Kui manages civil, Wu Qi manages military, Zhai Huang manages diplomacy, Wei Wenhou 'select people assign situations', clear division of labor"
        ],
        "expected": [
            "Wei dominated Central Plains, 'Wei army, world's elite', laid foundation for Qin unification",
            "'Book of Law' became China's first written code ancestor, Equal Transport/Exhaust Land Power/Military Merit became standard reform tools for dynasties",
            "Lessons: Legalism heavy punishment light virtue, Wu Qi reform touched noble interests forced to flee, Wei later declined"
        ],
        "case": "Li Kui Reform (400s BC): Wei Wenhou appointed Li Kui chancellor, implemented: 1) Book of Law six chapters: theft/bandit/imprisonment/arrest/miscellaneous/tools, abolished noble privileges, equality before law. 2) Equal Transport Law: bumper year state buys high stores in granary, famine year sells low stabilizes prices, eliminates merchant hoarding. 3) Exhaust Land Power: tax by land fertility, upper field more tax, lower field less tax, reclamation tax-free three years, over-production rewarded. 4) Military Merit Rank: one head one rank, reward ten mu land, one residence, abolished hereditary nobility. Result: Wei rich state strong army, elite soldiers, dominated Central Plains century, laid foundation for Qin unification."
    },
    "H-SW-49": {
        "name": "Sun Wu: Military Strategy Deception Master",
        "description": "Warfare Is Deception / Know Self Know Enemy / Win by Orthodox and Unorthodox / Subdue Enemy Without Fighting / Nine Grounds Nine Changes",
        "modes": [13, 1, 11, 14, 35],
        "reason": "Sun Wu 'Warfare is the great affair of state, ground of life and death, way of survival and extinction, cannot be unexamined'. Core mindset: strategic deception and total victory thinking culmination — 'Warfare is deception', 'able show unable, use show not use, near show far, far show near', 'know self know enemy hundred battles not peril', 'subdue enemy without fighting is supreme excellence'. 'Win by orthodox, victory by unorthodox', 'strike unprepared, appear unexpected', 'nine grounds nine changes, adapt advantage control authority'. Abstracted war as game model, psychological/strategic/deception systematized.",
        "steps": [
            "Step 1: Total Victory Mindset — Victory Without Fighting: 'Hundred battles hundred victories not best, subdue enemy without fighting is best', achieve strategic goals via strategy/diplomacy/psychology/economy",
            "Step 2: Contradiction Analysis — Know Self Know Enemy: 'Know enemy know self hundred battles not peril, unknown enemy know self one win one loss, unknown enemy unknown self every battle peril', intelligence first, assess strengths weaknesses",
            "Step 3: Total Victory Mindset — Orthodox Unorthodox: 'Battle by orthodox, win by unorthodox', orthodox troops pin down, unorthodox troops win, virtual real transform, strike unexpected",
            "Step 4: Center of Gravity — Strike Unprepared: 'Avoid real strike void, strike unprepared, appear unexpected', nine grounds nine changes, adapt to terrain, adapt advantage control authority",
            "Step 5: Dormant Accumulation — Deceive Appearance: 'Able show unable, use show not use, near show far, far show near', lure enemy deep, await leisure, host await guest"
        ],
        "expected": [
            "'Art of War' became world military classic, influenced East Asia/West military/business/competition strategy",
            "Total Victory/Know Self Know Enemy/Orthodox Unorthodox/Virtual Real/Strike Heart became strategic thinking universal vocabulary",
            "Lessons: overemphasis deception/psychological war, neglect logistics/engineering/technical hard power, later generations misinterpret as pure strategy"
        ],
        "case": "Art of War applications: Wu King Helu used Sun Wu train troops, broke Chu entered Ying (506 BC); Tian Ji horse racing 'inferior vs superior, superior vs middle, middle vs inferior' win by unorthodox; Goujian slept on firewood tasted gall, Fan Li used Sun Wu naval strategy destroyed Wu; Cao Cao Red Cliff studied 'Art of War', Red Cliff defeat due to neglecting 'virtual real', 'chained ships' became unorthodox weapon burned; Modern business: Jobs 'reality distortion field', Ma Yun 'win by unorthodox', Zhang Yiming 'algorithmic recommendation' as unorthodox weapon."
    },
    "H-ZZJ-50": {
        "name": "Zhang Zhongjing: Medical Systems Theory Ancestor of Syndrome Differentiation",
        "description": "Treatise on Cold Damage and Miscellaneous Diseases / Syndrome Differentiation Treatment / Formula-Syndrome Correspondence / Systems Medicine / Formula-Symptom Matching",
        "modes": [12, 1, 25, 28, 35],
        "reason": "Zhang Zhongjing 'Treatise on Cold Damage and Miscellaneous Diseases' six volumes (Cold Damage/Miscellaneous three each), core mindset: systems medicine syndrome differentiation system — 'differentiate yin yang, distinguish exterior interior, examine deficiency excess, differentiate cold heat', 'Six Channels Differentiation' (Taiyang/Yangming/Shaoyin/Taiyin/Shaoyang/Jueyin), 'Formula-Syndrome Correspondence' (syndrome determines formula, same disease different treatment/different diseases same treatment). 'Superior doctor treats pre-disease, middle doctor treats impending disease, inferior doctor treats manifest disease'. Established 'inspection auscultation inquiry palpation' four diagnostics integration, 'syndrome differentiation treatment' clinical thinking loop. Foundation for Chinese medicine and systems medicine.",
        "steps": [
            "Step 1: Systems Thinking — Six Channels Differentiation: Taiyang/Yangming/Shaoyin/Taiyin/Shaoyang/Jueyin six channels transmission rules, exterior/interior/cold/heat/deficiency/excess identification, established disease progression dynamic model",
            "Step 2: Contradiction Analysis — Syndrome Differentiation: 'Differentiate yin yang, distinguish exterior interior, examine deficiency excess, differentiate cold heat', find principal contradiction (cold/heat/deficiency/excess/exterior/interior), treat accordingly",
            "Step 3: Abstract Induction — Formula-Syndrome Correspondence: Same disease different treatment (same cold damage, exterior real use Ma Huang Tang, exterior deficiency use Gui Zhi Tang), Different diseases same treatment (Cholera/Cold Damage both Yangming fu real, both use Da Cheng Qi Tang)",
            "Step 4: Feedback Loops — Four Diagnostics Integration: Inspection/Auscultation/Inquiry/Palpation four diagnostics combined, syndrome established -> formula selection -> medication observation -> syndrome change -> formula adjustment, clinical loop",
            "Step 5: Dormant Accumulation — Superior Doctor Treats Pre-Disease: 'Superior doctor treats pre-disease, middle doctor treats impending disease, inferior doctor treats manifest disease', preventive medicine/sub-health intervention/early intervention, systems engineering thinking"
        ],
        "expected": [
            "'Treatise on Cold Damage and Miscellaneous Diseases' became Chinese medicine clinical bible, formula science/clinical diagnosis foundation",
            "Syndrome Differentiation/Six Channels/Formula-Syndrome became Chinese medicine core methodology, influenced Japan/Korea/Vietnam medicine",
            "Lessons: theoretical system closed/lack anatomy/lack microbiology/modern needs combine modern medicine verification"
        ],
        "case": "Cold Damage Six Channels: Taiyang (exterior), Yangming (interior real heat), Shaoyin (interior cold deficiency), Taiyin (spleen stomach deficiency cold), Shaoyang (half exterior half interior), Jueyin (yin yang both exhausted). Classic Formulas: Ma Huang Tang/Gui Zhi Tang/Da Qing Long Tang/Bai Hu Tang/Da Cheng Qi Tang/Xiao Chai Hu Tang/Si Ni Tang/Wu Mei Wan etc 113 formulas. Syndrome Differentiation: Same disease different treatment (Cold Damage exterior real Ma Huang, exterior deficiency Gui Zhi), Different diseases same treatment (Cold Damage/Cholera both Yangming fu real, both use Da Cheng Qi Tang). Result: Chinese medicine clinical diagnosis/treatment standardized, formula science established."
    }
}

# Add to scenarios
scenarios_zh.update(new_zh)

# Save
with open('scenarios_zh.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios_zh, f, ensure_ascii=False, indent=2)

print(f"Updated scenarios_zh.json: {len(scenarios_zh)} total scenarios")

# English versions
new_en = {
    "H-LL-48": {
        "name": "Li Kui: Legalist Founder of Reform Foundation",
        "description": "Six Chapters of Book of Law / Equal Transport Law / Exhaust Land Power / Warring States Reform Ancestor / Enrich State Strengthen Army",
        "modes": [32, 19, 20, 28, 34],
        "reason": "Li Kui 'Book of Law' six chapters (theft/bandit/imprisonment/arrest/miscellaneous/tools), core mindset: institutionalized foundation of rule of law state — served as Wei Wenhou's chancellor, promoted 'Equal Transport Law' (state purchases grain at stable price in harvest, sells at stable price in famine), 'Exhaust Land Power' (tax by land fertility, reward reclamation), 'Teaching Warfare Law' (military merit enfeoffment, clear rewards punishments). 'Law as teaching', 'abolish private learning, make legal officials teachers', laid foundation for Shang Yang/Han Fei/Qin Shi Huang legal system.",
        "steps": [
            "Step 1: Procedural Justice — Public legislation, strict enforcement, independent judiciary, universal equality, 'law does not favor nobility, rope does not bend for curves'",
            "Step 2: Marginal Thinking — Equal Transport Law: bumper year state buys grain at high price protecting farmers, famine year sells at low price benefiting people, state regulates grain price stability, prevents merchant hoarding",
            "Step 3: Incentive Mechanism — Exhaust Land Power: tax set by land fertility, over-production rewarded, under-production reduced, incentivizes farmers to reclaim wasteland increase yield",
            "Step 4: Institutional Checks — Military Merit Rank System: enfeoffment by enemy heads count, reward land/grant residence, abolish hereditary nobility/salaries, establish 'merit-based ennoblement' selection mechanism",
            "Step 5: Strategic Delegation — Professional Division: Li Kui manages civil, Wu Qi manages military, Zhai Huang manages diplomacy, Wei Wenhou 'select people assign situations', clear division of labor"
        ],
        "expected": [
            "Wei dominated Central Plains, 'Wei army, world's elite', laid foundation for Qin unification",
            "'Book of Law' became China's first written code ancestor, Equal Transport/Exhaust Land Power/Military Merit became standard reform tools for dynasties",
            "Lessons: Legalism heavy punishment light virtue, Wu Qi reform touched noble interests forced to flee, Wei later declined"
        ],
        "case": "Li Kui Reform (400s BC): Wei Wenhou appointed Li Kui chancellor, implemented: 1) Book of Law six chapters: theft/bandit/imprisonment/arrest/miscellaneous/tools, abolished noble privileges, equality before law. 2) Equal Transport Law: bumper year state buys high stores in granary, famine year sells low stabilizes prices, eliminates merchant hoarding. 3) Exhaust Land Power: tax by land fertility, upper field more tax, lower field less tax, reclamation tax-free three years, over-production rewarded. 4) Military Merit Rank: one head one rank, reward ten mu land, one residence, abolished hereditary nobility. Result: Wei rich state strong army, elite soldiers, dominated Central Plains century, laid foundation for Qin unification."
    },
    "H-SW-49": {
        "name": "Sun Wu: Military Strategy Deception Master",
        "description": "Warfare Is Deception / Know Self Know Enemy / Win by Orthodox and Unorthodox / Subdue Enemy Without Fighting / Nine Grounds Nine Changes",
        "modes": [13, 1, 11, 14, 35],
        "reason": "Sun Wu 'Warfare is the great affair of state, ground of life and death, way of survival and extinction, cannot be unexamined'. Core mindset: strategic deception and total victory thinking culmination — 'Warfare is deception', 'able show unable, use show not use, near show far, far show near', 'know self know enemy hundred battles not peril', 'subdue enemy without fighting is supreme excellence'. 'Win by orthodox, victory by unorthodox', 'strike unprepared, appear unexpected', 'nine grounds nine changes, adapt advantage control authority'. Abstracted war as game model, psychological/strategic/deception systematized.",
        "steps": [
            "Step 1: Total Victory Mindset — Victory Without Fighting: 'Hundred battles hundred victories not best, subdue enemy without fighting is best', achieve strategic goals via strategy/diplomacy/psychology/economy",
            "Step 2: Contradiction Analysis — Know Self Know Enemy: 'Know enemy know self hundred battles not peril, unknown enemy know self one win one loss, unknown enemy unknown self every battle peril', intelligence first, assess strengths weaknesses",
            "Step 3: Total Victory Mindset — Orthodox Unorthodox: 'Battle by orthodox, win by unorthodox', orthodox troops pin down, unorthodox troops win, virtual real transform, strike unexpected",
            "Step 4: Center of Gravity — Strike Unprepared: 'Avoid real strike void, strike unprepared, appear unexpected', nine grounds nine changes, adapt to terrain, adapt advantage control authority",
            "Step 5: Dormant Accumulation — Deceive Appearance: 'Able show unable, use show not use, near show far, far show near', lure enemy deep, await leisure, host await guest"
        ],
        "expected": [
            "'Art of War' became world military classic, influenced East Asia/West military/business/competition strategy",
            "Total Victory/Know Self Know Enemy/Orthodox Unorthodox/Virtual Real/Strike Heart became strategic thinking universal vocabulary",
            "Lessons: overemphasis deception/psychological war, neglect logistics/engineering/technical hard power, later generations misinterpret as pure strategy"
        ],
        "case": "Art of War applications: Wu King Helu used Sun Wu train troops, broke Chu entered Ying (506 BC); Tian Ji horse racing 'inferior vs superior, superior vs middle, middle vs inferior' win by unorthodox; Goujian slept on firewood tasted gall, Fan Li used Sun Wu naval strategy destroyed Wu; Cao Cao Red Cliff studied 'Art of War', Red Cliff defeat due to neglecting 'virtual real', 'chained ships' became unorthodox weapon burned; Modern business: Jobs 'reality distortion field', Ma Yun 'win by unorthodox', Zhang Yiming 'algorithmic recommendation' as unorthodox weapon."
    },
    "H-ZZJ-50": {
        "name": "Zhang Zhongjing: Medical Systems Theory Ancestor of Syndrome Differentiation",
        "description": "Treatise on Cold Damage and Miscellaneous Diseases / Syndrome Differentiation Treatment / Formula-Syndrome Correspondence / Systems Medicine / Formula-Symptom Matching",
        "modes": [12, 1, 25, 28, 35],
        "reason": "Zhang Zhongjing 'Treatise on Cold Damage and Miscellaneous Diseases' six volumes (Cold Damage/Miscellaneous three each), core mindset: systems medicine syndrome differentiation system — 'differentiate yin yang, distinguish exterior interior, examine deficiency excess, differentiate cold heat', 'Six Channels Differentiation' (Taiyang/Yangming/Shaoyin/Taiyin/Shaoyang/Jueyin), 'Formula-Syndrome Correspondence' (syndrome determines formula, same disease different treatment/different diseases same treatment). 'Superior doctor treats pre-disease, middle doctor treats impending disease, inferior doctor treats manifest disease'. Established 'inspection auscultation inquiry palpation' four diagnostics integration, 'syndrome differentiation treatment' clinical thinking loop. Foundation for Chinese medicine and systems medicine.",
        "steps": [
            "Step 1: Systems Thinking — Six Channels Differentiation: Taiyang/Yangming/Shaoyin/Taiyin/Shaoyang/Jueyin six channels transmission rules, exterior/interior/cold/heat/deficiency/excess identification, established disease progression dynamic model",
            "Step 2: Contradiction Analysis — Syndrome Differentiation: 'Differentiate yin yang, distinguish exterior interior, examine deficiency excess, differentiate cold heat', find principal contradiction (cold/heat/deficiency/excess/exterior/interior), treat accordingly",
            "Step 3: Abstract Induction — Formula-Syndrome Correspondence: Same disease different treatment (same cold damage, exterior real use Ma Huang Tang, exterior deficiency use Gui Zhi Tang), Different diseases same treatment (Cholera/Cold Damage both Yangming fu real, both use Da Cheng Qi Tang)",
            "Step 4: Feedback Loops — Four Diagnostics Integration: Inspection/Auscultation/Inquiry/Palpation four diagnostics combined, syndrome established -> formula selection -> medication observation -> syndrome change -> formula adjustment, clinical loop",
            "Step 5: Dormant Accumulation — Superior Doctor Treats Pre-Disease: 'Superior doctor treats pre-disease, middle doctor treats impending disease, inferior doctor treats manifest disease', preventive medicine/sub-health intervention/early intervention, systems engineering thinking"
        ],
        "expected": [
            "'Treatise on Cold Damage and Miscellaneous Diseases' became Chinese medicine clinical bible, formula science/clinical diagnosis foundation",
            "Syndrome Differentiation/Six Channels/Formula-Syndrome became Chinese medicine core methodology, influenced Japan/Korea/Vietnam medicine",
            "Lessons: theoretical system closed/lack anatomy/lack microbiology/modern needs combine modern medicine verification"
        ],
        "case": "Cold Damage Six Channels: Taiyang (exterior), Yangming (interior real heat), Shaoyin (interior cold deficiency), Taiyin (spleen stomach deficiency cold), Shaoyang (half exterior half interior), Jueyin (yin yang both exhausted). Classic Formulas: Ma Huang Tang/Gui Zhi Tang/Da Qing Long Tang/Bai Hu Tang/Da Cheng Qi Tang/Xiao Chai Hu Tang/Si Ni Tang/Wu Mei Wan etc 113 formulas. Syndrome Differentiation: Same disease different treatment (Cold Damage exterior real Ma Huang, exterior deficiency Gui Zhi), Different diseases same treatment (Cold Damage/Cholera both Yangming fu real, both use Da Cheng Qi Tang). Result: Chinese medicine clinical diagnosis/treatment standardized, formula science established."
    }
}

# Add to scenarios
scenarios_zh.update(new_zh)

# Save
with open('scenarios_zh.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios_zh, f, ensure_ascii=False, indent=2)

print(f"Updated scenarios_zh.json: {len(scenarios_zh)} total scenarios")

# English versions
new_en = {
    "H-LL-48": {
        "name": "Li Kui: Legalist Founder of Reform Foundation",
        "description": "Six Chapters of Book of Law / Equal Transport Law / Exhaust Land Power / Warring States Reform Ancestor / Enrich State Strengthen Army",
        "modes": [32, 19, 20, 28, 34],
        "reason": "Li Kui 'Book of Law' six chapters (theft/bandit/imprisonment/arrest/miscellaneous/tools), core mindset: institutionalized foundation of rule of law state — served as Wei Wenhou's chancellor, promoted 'Equal Transport Law' (state purchases grain at stable price in harvest, sells at stable price in famine), 'Exhaust Land Power' (tax by land fertility, reward reclamation), 'Teaching Warfare Law' (military merit enfeoffment, clear rewards punishments). 'Law as teaching', 'abolish private learning, make legal officials teachers', laid foundation for Shang Yang/Han Fei/Qin Shi Huang legal system.",
        "steps": [
            "Step 1: Procedural Justice — Public legislation, strict enforcement, independent judiciary, universal equality, 'law does not favor nobility, rope does not bend for curves'",
            "Step 2: Marginal Thinking — Equal Transport Law: bumper year state buys grain at high price protecting farmers, famine year sells at low price benefiting people, state regulates grain price stability, prevents merchant hoarding",
            "Step 3: Incentive Mechanism — Exhaust Land Power: tax set by land fertility, over-production rewarded, under-production reduced, incentivizes farmers to reclaim wasteland increase yield",
            "Step 4: Institutional Checks — Military Merit Rank System: enfeoffment by enemy heads count, reward land/grant residence, abolish hereditary nobility/salaries, establish 'merit-based ennoblement' selection mechanism",
            "Step 5: Strategic Delegation — Professional Division: Li Kui manages civil, Wu Qi manages military, Zhai Huang manages diplomacy, Wei Wenhou 'select people assign situations', clear division of labor"
        ],
        "expected": [
            "Wei dominated Central Plains, 'Wei army, world's elite', laid foundation for Qin unification",
            "'Book of Law' became China's first written code ancestor, Equal Transport/Exhaust Land Power/Military Merit became standard reform tools for dynasties",
            "Lessons: Legalism heavy punishment light virtue, Wu Qi reform touched noble interests forced to flee, Wei later declined"
        ],
        "case": "Li Kui Reform (400s BC): Wei Wenhou appointed Li Kui chancellor, implemented: 1) Book of Law six chapters: theft/bandit/imprisonment/arrest/miscellaneous/tools, abolished noble privileges, equality before law. 2) Equal Transport Law: bumper year state buys high stores in granary, famine year sells low stabilizes prices, eliminates merchant hoarding. 3) Exhaust Land Power: tax by land fertility, upper field more tax, lower field less tax, reclamation tax-free three years, over-production rewarded. 4) Military Merit Rank: one head one rank, reward ten mu land, one residence, abolished hereditary nobility. Result: Wei rich state strong army, elite soldiers, dominated Central Plains century, laid foundation for Qin unification."
    },
    "H-SW-49": {
        "name": "Sun Wu: Military Strategy Deception Master",
        "description": "Warfare Is Deception / Know Self Know Enemy / Win by Orthodox and Unorthodox / Subdue Enemy Without Fighting / Nine Grounds Nine Changes",
        "modes": [13, 1, 11, 14, 35],
        "reason": "Sun Wu 'Warfare is the great affair of state, ground of life and death, way of survival and extinction, cannot be unexamined'. Core mindset: strategic deception and total victory thinking culmination — 'Warfare is deception', 'able show unable, use show not use, near show far, far show near', 'know self know enemy hundred battles not peril', 'subdue enemy without fighting is supreme excellence'. 'Win by orthodox, victory by unorthodox', 'strike unprepared, appear unexpected', 'nine grounds nine changes, adapt advantage control authority'. Abstracted war as game model, psychological/strategic/deception systematized.",
        "steps": [
            "Step 1: Total Victory Mindset — Victory Without Fighting: 'Hundred battles hundred victories not best, subdue enemy without fighting is best', achieve strategic goals via strategy/diplomacy/psychology/economy",
            "Step 2: Contradiction Analysis — Know Self Know Enemy: 'Know enemy know self hundred battles not peril, unknown enemy know self one win one loss, unknown enemy unknown self every battle peril', intelligence first, assess strengths weaknesses",
            "Step 3: Total Victory Mindset — Orthodox Unorthodox: 'Battle by orthodox, win by unorthodox', orthodox troops pin down, unorthodox troops win, virtual real transform, strike unexpected",
            "Step 4: Center of Gravity — Strike Unprepared: 'Avoid real strike void, strike unprepared, appear unexpected', nine grounds nine changes, adapt to terrain, adapt advantage control authority",
            "Step 5: Dormant Accumulation — Deceive Appearance: 'Able show unable, use show not use, near show far, far show near', lure enemy deep, await leisure, host await guest"
        ],
        "expected": [
            "'Art of War' became world military classic, influenced East Asia/West military/business/competition strategy",
            "Total Victory/Know Self Know Enemy/Orthodox Unorthodox/Virtual Real/Strike Heart became strategic thinking universal vocabulary",
            "Lessons: overemphasis deception/psychological war, neglect logistics/engineering/technical hard power, later generations misinterpret as pure strategy"
        ],
        "case": "Art of War applications: Wu King Helu used Sun Wu train troops, broke Chu entered Ying (506 BC); Tian Ji horse racing 'inferior vs superior, superior vs middle, middle vs inferior' win by unorthodox; Goujian slept on firewood tasted gall, Fan Li used Sun Wu naval strategy destroyed Wu; Cao Cao Red Cliff studied 'Art of War', Red Cliff defeat due to neglecting 'virtual real', 'chained ships' became unorthodox weapon burned; Modern business: Jobs 'reality distortion field', Ma Yun 'win by unorthodox', Zhang Yiming 'algorithmic recommendation' as unorthodox weapon."
    },
    "H-ZZJ-50": {
        "name": "Zhang Zhongjing: Medical Systems Theory Ancestor of Syndrome Differentiation",
        "description": "Treatise on Cold Damage and Miscellaneous Diseases / Syndrome Differentiation Treatment / Formula-Syndrome Correspondence / Systems Medicine / Formula-Symptom Matching",
        "modes": [12, 1, 25, 28, 35],
        "reason": "Zhang Zhongjing 'Treatise on Cold Damage and Miscellaneous Diseases' six volumes (Cold Damage/Miscellaneous three each), core mindset: systems medicine syndrome differentiation system — 'differentiate yin yang, distinguish exterior interior, examine deficiency excess, differentiate cold heat', 'Six Channels Differentiation' (Taiyang/Yangming/Shaoyin/Taiyin/Shaoyang/Jueyin), 'Formula-Syndrome Correspondence' (syndrome determines formula, same disease different treatment/different diseases same treatment). 'Superior doctor treats pre-disease, middle doctor treats impending disease, inferior doctor treats manifest disease'. Established 'inspection auscultation inquiry palpation' four diagnostics integration, 'syndrome differentiation treatment' clinical thinking loop. Foundation for Chinese medicine and systems medicine.",
        "steps": [
            "Step 1: Systems Thinking — Six Channels Differentiation: Taiyang/Yangming/Shaoyin/Taiyin/Shaoyang/Jueyin six channels transmission rules, exterior/interior/cold/heat/deficiency/excess identification, established disease progression dynamic model",
            "Step 2: Contradiction Analysis — Syndrome Differentiation: 'Differentiate yin yang, distinguish exterior interior, examine deficiency excess, differentiate cold heat', find principal contradiction (cold/heat/deficiency/excess/exterior/interior), treat accordingly",
            "Step 3: Abstract Induction — Formula-Syndrome Correspondence: Same disease different treatment (same cold damage, exterior real use Ma Huang Tang, exterior deficiency use Gui Zhi Tang), Different diseases same treatment (Cholera/Cold Damage both Yangming fu real, both use Da Cheng Qi Tang)",
            "Step 4: Feedback Loops — Four Diagnostics Integration: Inspection/Auscultation/Inquiry/Palpation four diagnostics combined, syndrome established -> formula selection -> medication observation -> syndrome change -> formula adjustment, clinical loop",
            "Step 5: Dormant Accumulation — Superior Doctor Treats Pre-Disease: 'Superior doctor treats pre-disease, middle doctor treats impending disease, inferior doctor treats manifest disease', preventive medicine/sub-health intervention/early intervention, systems engineering thinking"
        ],
        "expected": [
            "'Treatise on Cold Damage and Miscellaneous Diseases' became Chinese medicine clinical bible, formula science/clinical diagnosis foundation",
            "Syndrome Differentiation/Six Channels/Formula-Syndrome became Chinese medicine core methodology, influenced Japan/Korea/Vietnam medicine",
            "Lessons: theoretical system closed/lack anatomy/lack microbiology/modern needs combine modern medicine verification"
        ],
        "case": "Cold Damage Six Channels: Taiyang (exterior), Yangming (interior real heat), Shaoyin (interior cold deficiency), Taiyin (spleen stomach deficiency cold), Shaoyang (half exterior half interior), Jueyin (yin yang both exhausted). Classic Formulas: Ma Huang Tang/Gui Zhi Tang/Da Qing Long Tang/Bai Hu Tang/Da Cheng Qi Tang/Xiao Chai Hu Tang/Si Ni Tang/Wu Mei Wan etc 113 formulas. Syndrome Differentiation: Same disease different treatment (Cold Damage exterior real Ma Huang, exterior deficiency Gui Zhi), Different diseases same treatment (Cold Damage/Cholera both Yangming fu real, both use Da Cheng Qi Tang). Result: Chinese medicine clinical diagnosis/treatment standardized, formula science established."
    }
}

# Add to scenarios
scenarios_zh.update(new_zh)

# Save
with open('scenarios_zh.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios_zh, f, ensure_ascii=False, indent=2)

print(f"Updated scenarios_zh.json: {len(scenarios_zh)} total scenarios")

# English versions
new_en = {
    "H-LL-48": {
        "name": "Li Kui: Legalist Founder of Reform Foundation",
        "description": "Six Chapters of Book of Law / Equal Transport Law / Exhaust Land Power / Warring States Reform Ancestor / Enrich State Strengthen Army",
        "modes": [32, 19, 20, 28, 34],
        "reason": "Li Kui 'Book of Law' six chapters (theft/bandit/imprisonment/arrest/miscellaneous/tools), core mindset: institutionalized foundation of rule of law state — served as Wei Wenhou's chancellor, promoted 'Equal Transport Law' (state purchases grain at stable price in harvest, sells at stable price in famine), 'Exhaust Land Power' (tax by land fertility, reward reclamation), 'Teaching Warfare Law' (military merit enfeoffment, clear rewards punishments). 'Law as teaching', 'abolish private learning, make legal officials teachers', laid foundation for Shang Yang/Han Fei/Qin Shi Huang legal system.",
        "steps": [
            "Step 1: Procedural Justice — Public legislation, strict enforcement, independent judiciary, universal equality, 'law does not favor nobility, rope does not bend for curves'",
            "Step 2: Marginal Thinking — Equal Transport Law: bumper year state buys grain at high price protecting farmers, famine year sells at low price benefiting people, state regulates grain price stability, prevents merchant hoarding",
            "Step 3: Incentive Mechanism — Exhaust Land Power: tax set by land fertility, over-production rewarded, under-production reduced, incentivizes farmers to reclaim wasteland increase yield",
            "Step 4: Institutional Checks — Military Merit Rank System: enfeoffment by enemy heads count, reward land/grant residence, abolish hereditary nobility/salaries, establish 'merit-based ennoblement' selection mechanism",
            "Step 5: Strategic Delegation — Professional Division: Li Kui manages civil, Wu Qi manages military, Zhai Huang manages diplomacy, Wei Wenhou 'select people assign situations', clear division of labor"
        ],
        "expected": [
            "Wei dominated Central Plains, 'Wei army, world's elite', laid foundation for Qin unification",
            "'Book of Law' became China's first written code ancestor, Equal Transport/Exhaust Land Power/Military Merit became standard reform tools for dynasties",
            "Lessons: Legalism heavy punishment light virtue, Wu Qi reform touched noble interests forced to flee, Wei later declined"
        ],
        "case": "Li Kui Reform (400s BC): Wei Wenhou appointed Li Kui chancellor, implemented: 1) Book of Law six chapters: theft/bandit/imprisonment/arrest/miscellaneous/tools, abolished noble privileges, equality before law. 2) Equal Transport Law: bumper year state buys high stores in granary, famine year sells low stabilizes prices, eliminates merchant hoarding. 3) Exhaust Land Power: tax by land fertility, upper field more tax, lower field less tax, reclamation tax-free three years, over-production rewarded. 4) Military Merit Rank: one head one rank, reward ten mu land, one residence, abolished hereditary nobility. Result: Wei rich state strong army, elite soldiers, dominated Central Plains century, laid foundation for Qin unification."
    },
    "H-SW-49": {
        "name": "Sun Wu: Military Strategy Deception Master",
        "description": "Warfare Is Deception / Know Self Know Enemy / Win by Orthodox and Unorthodox / Subdue Enemy Without Fighting / Nine Grounds Nine Changes",
        "modes": [13, 1, 11, 14, 35],
        "reason": "Sun Wu 'Warfare is the great affair of state, ground of life and death, way of survival and extinction, cannot be unexamined'. Core mindset: strategic deception and total victory thinking culmination — 'Warfare is deception', 'able show unable, use show not use, near show far, far show near', 'know self know enemy hundred battles not peril', 'subdue enemy without fighting is supreme excellence'. 'Win by orthodox, victory by unorthodox', 'strike unprepared, appear unexpected', 'nine grounds nine changes, adapt advantage control authority'. Abstracted war as game model, psychological/strategic/deception systematized.",
        "steps": [
            "Step 1: Total Victory Mindset — Victory Without Fighting: 'Hundred battles hundred victories not best, subdue enemy without fighting is best', achieve strategic goals via strategy/diplomacy/psychology/economy",
            "Step 2: Contradiction Analysis — Know Self Know Enemy: 'Know enemy know self hundred battles not peril, unknown enemy know self one win one loss, unknown enemy unknown self every battle peril', intelligence first, assess strengths weaknesses",
            "Step 3: Total Victory Mindset — Orthodox Unorthodox: 'Battle by orthodox, win by unorthodox', orthodox troops pin down, unorthodox troops win, virtual real transform, strike unexpected",
            "Step 4: Center of Gravity — Strike Unprepared: 'Avoid real strike void, strike unprepared, appear unexpected', nine grounds nine changes, adapt to terrain, adapt advantage control authority",
            "Step 5: Dormant Accumulation — Deceive Appearance: 'Able show unable, use show not use, near show far, far show near', lure enemy deep, await leisure, host await guest"
        ],
        "expected": [
            "'Art of War' became world military classic, influenced East Asia/West military/business/competition strategy",
            "Total Victory/Know Self Know Enemy/Orthodox Unorthodox/Virtual Real/Strike Heart became strategic thinking universal vocabulary",
            "Lessons: overemphasis deception/psychological war, neglect logistics/engineering/technical hard power, later generations misinterpret as pure strategy"
        ],
        "case": "Art of War applications: Wu King Helu used Sun Wu train troops, broke Chu entered Ying (506 BC); Tian Ji horse racing 'inferior vs superior, superior vs middle, middle vs inferior' win by unorthodox; Goujian slept on firewood tasted gall, Fan Li used Sun Wu naval strategy destroyed Wu; Cao Cao Red Cliff studied 'Art of War', Red Cliff defeat due to neglecting 'virtual real', 'chained ships' became unorthodox weapon burned; Modern business: Jobs 'reality distortion field', Ma Yun 'win by unorthodox', Zhang Yiming 'algorithmic recommendation' as unorthodox weapon."
    },
    "H-ZZJ-50": {
        "name": "Zhang Zhongjing: Medical Systems Theory Ancestor of Syndrome Differentiation",
        "description": "Treatise on Cold Damage and Miscellaneous Diseases / Syndrome Differentiation Treatment / Formula-Syndrome Correspondence / Systems Medicine / Formula-Symptom Matching",
        "modes": [12, 1, 25, 28, 35],
        "reason": "Zhang Zhongjing 'Treatise on Cold Damage and Miscellaneous Diseases' six volumes (Cold Damage/Miscellaneous three each), core mindset: systems medicine syndrome differentiation system — 'differentiate yin yang, distinguish exterior interior, examine deficiency excess, differentiate cold heat', 'Six Channels Differentiation' (Taiyang/Yangming/Shaoyin/Taiyin/Shaoyang/Jueyin), 'Formula-Syndrome Correspondence' (syndrome determines formula, same disease different treatment/different diseases same treatment). 'Superior doctor treats pre-disease, middle doctor treats impending disease, inferior doctor treats manifest disease'. Established 'inspection auscultation inquiry palpation' four diagnostics integration, 'syndrome differentiation treatment' clinical thinking loop. Foundation for Chinese medicine and systems medicine.",
        "steps": [
            "Step 1: Systems Thinking — Six Channels Differentiation: Taiyang/Yangming/Shaoyin/Taiyin/Shaoyang/Jueyin six channels transmission rules, exterior/interior/cold/heat/deficiency/excess identification, established disease progression dynamic model",
            "Step 2: Contradiction Analysis — Syndrome Differentiation: 'Differentiate yin yang, distinguish exterior interior, examine deficiency excess, differentiate cold heat', find principal contradiction (cold/heat/deficiency/excess/exterior/interior), treat accordingly",
            "Step 3: Abstract Induction — Formula-Syndrome Correspondence: Same disease different treatment (same cold damage, exterior real use Ma Huang Tang, exterior deficiency use Gui Zhi Tang), Different diseases same treatment (Cholera/Cold Damage both Yangming fu real, both use Da Cheng Qi Tang)",
            "Step 4: Feedback Loops — Four Diagnostics Integration: Inspection/Auscultation/Inquiry/Palpation four diagnostics combined, syndrome established -> formula selection -> medication observation -> syndrome change -> formula adjustment, clinical loop",
            "Step 5: Dormant Accumulation — Superior Doctor Treats Pre-Disease: 'Superior doctor treats pre-disease, middle doctor treats impending disease, inferior doctor treats manifest disease', preventive medicine/sub-health intervention/early intervention, systems engineering thinking"
        ],
        "expected": [
            "'Treatise on Cold Damage and Miscellaneous Diseases' became Chinese medicine clinical bible, formula science/clinical diagnosis foundation",
            "Syndrome Differentiation/Six Channels/Formula-Syndrome became Chinese medicine core methodology, influenced Japan/Korea/Vietnam medicine",
            "Lessons: theoretical system closed/lack anatomy/lack microbiology/modern needs combine modern medicine verification"
        ],
        "case": "Cold Damage Six Channels: Taiyang (exterior), Yangming (interior real heat), Shaoyin (interior cold deficiency), Taiyin (spleen stomach deficiency cold), Shaoyang (half exterior half interior), Jueyin (yin yang both exhausted). Classic Formulas: Ma Huang Tang/Gui Zhi Tang/Da Qing Long Tang/Bai Hu Tang/Da Cheng Qi Tang/Xiao Chai Hu Tang/Si Ni Tang/Wu Mei Wan etc 113 formulas. Syndrome Differentiation: Same disease different treatment (Cold Damage exterior real Ma Huang, exterior deficiency Gui Zhi), Different diseases same treatment (Cold Damage/Cholera both Yangming fu real, both use Da Cheng Qi Tang). Result: Chinese medicine clinical diagnosis/treatment standardized, formula science established."
    }
}

# Add to English scenarios
scenarios_en.update(new_en)

with open('scenarios_en.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios_en, f, ensure_ascii=False, indent=2)

print(f"Updated scenarios_en.json: {len(scenarios_en)} total scenarios")