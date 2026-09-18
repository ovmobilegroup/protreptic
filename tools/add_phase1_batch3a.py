import json

# Load existing data
with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)
with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)
with open('code_maps.json', 'r', encoding='utf-8') as f:
    cm = json.load(f)

# Phase 1 Batch 3: Legalist + Mohist/Logicians + Women (12 figures)
new_entries = [
    # Legalist
    {
        "code": "H-LS-158",
        "name_zh": "李斯：秦帝国制度工程/焚书坑儒/车同轨书同文/秦制百代/制度工程化集大成者",
        "name_en": "Li Si: Qin Empire Institutional Engineering/Book Burning Scholar Burying/Unified Tracks Script/Ancient System Enduring/Institutional Engineering Master",
        "description_zh": "秦帝国/焚书坑儒/车同轨书同文/度量衡/郡县制/秦制百代/制度工程化",
        "description_en": "Qin Empire/Book Burning Scholar Burying/Unified Tracks Script/Weights Measures/Commandery-County System/Qin System Enduring/Institutional Engineering",
        "modes": [32, 34, 40, 18, 28],
        "reason_zh": "核心思维：在「六国并存、制度分裂、法家理论待落地」秦末，以「制度标准化/文字统一/度量衡统一/郡县制推行/思想统摄」五重工程化落地。",
        "reason_en": "Core Thinking: In late Qin 'Six states coexisting, systems divided, Legalist theory awaiting implementation', engineered five-dimensional engineering implementation.",
        "steps_zh": [
            "第1步：抽象归纳法——提炼「统一/标准/工程化」核心框架",
            "第2步：系统思维法——构建六系统耦合模型",
            "第3步：摸石头过河/实验主义——五大工程并行推进",
            "第4步：制度化制衡——建三级行政架构",
            "第5步：总体性思维——形成帝国级制度工程范式"
        ],
        "steps_en": [
            "Step 1: Abstract Induction — Extract 'unification/standardization/engineering' core framework",
            "Step 2: Systems Thinking — Build six-system coupling model",
            "Step 3: Crossing River by Feeling Stones — Five major projects parallel push",
            "Step 4: Institutional Checks — Built three-tier admin architecture",
            "Step 5: Systems Thinking — Empire-level institutional engineering paradigm"
        ],
        "expected_zh": [
            "推四统一，建十维度量衡标准体系",
            "推郡县制废分封，建三级行政架构",
            "建秦律法制体系，推焚书坑儒思想统摄",
            "成中国首个帝国级制度工程范式"
        ],
        "expected_en": [
            "Implemented four unifications, built 10D weights standards",
            "Implemented commandery-county system, built 3-tier admin",
            "Built Qin Law legal system, book burning thought unification",
            "China's first empire-level institutional engineering paradigm"
        ],
        "case_zh": "李斯（前280-前208），楚国上蔡人，荀子弟子，秦始皇丞相。著《谏逐客书》「泰山不让土壤/河海不择细流」，力主用人唯才。推「焚书坑儒」禁「诗书/百家语/秦记」，统摄思想。推「四统一」：车同轨/书同文/度量衡/货币。推「郡县制」废分封，建三十六郡守/尉/监三级吏。建「秦律」十八律：什伍/连坐/集体责任。其五维工程化落地，成中国首个帝国级制度工程范式，奠秦制百代制度基因。",
        "case_en": "Li Si (280-208 BCE), Chu Shangcai native, Xunzi disciple, Qin Shihuang Chancellor. Authored Memorial Against Expelling Guests 'Tai Shan not rejecting soil/Rivers not rejecting streams', advocating merit-based employment. Implemented 'book burning scholar burying' banned 'poetry/hundred schools/Qin records', unifying thought. Implemented 'four unifications': unified tracks/scripts/weights/currency. Implemented commandery-county system abolishing enfeoffment, built 36 commanderies with 3-tier officials. Built 'Qin Law' 18 statutes: squad/collective responsibility. His five-dimensional engineering became China's first empire-level institutional engineering paradigm, founding 'Qin system enduring generations' institutional genes."
    },
    {
        "code": "H-WQ-159",
        "name_zh": "吴起：变法/兵法/吴起兵法/楚国变法/法家军事化/军事工程化先驱",
        "name_en": "Wu Qi: Reform/Military Strategy/Wu Qi Art of War/Chu Reform/Legalist Militarization/Military Engineering Pioneer",
        "description_zh": "吴起兵法/楚国变法/法家军事化/军事工程化/魏武卒/六论/图国",
        "description_en": "Wu Qi Art of War/Chu Reform/Legalist Militarization/Military Engineering/Wei Wu Coelu/Six Discourses/State Mapping",
        "modes": [15, 32, 16, 28, 35],
        "reason_zh": "核心思维：在「战国弱国楚国、贵族特权横行、军事松懈」背景下，以「法家军事化/变法强军/军事工程化」三重工程。",
        "reason_en": "Core Thinking: In 'weak Chu state Warring States, noble privileges rampant, military lax', engineered 'Legalist militarization/reform strengthening military/military engineering' triple project.",
        "steps_zh": [
            "第1步：抽象归纳法——提炼「战功/选练/考核/赏罚」核心框架",
            "第2步：系统思维法——构建六级精兵体系与六维理论模型",
            "第3步：摸石头过河/实验主义——魏创武卒小规模试点",
            "第4步：制度化制衡——楚相位推五战功法废四弊",
            "第5步：总体性思维——形成中国古代军事工程化范式"
        ],
        "steps_en": [
            "Step 1: Abstract Induction — Extract 'merit/selection-training/assessment/rewards-punishments' core framework",
            "Step 2: Systems Thinking — Build six-tier elite soldier system with six-dimensional theory model",
            "Step 3: Crossing River by Feeling Stones — In Wei created Wu Coelu pilot",
            "Step 4: Institutional Checks — Chu Chancellor implemented five merit laws",
            "Step 5: Systems Thinking — Chinese ancient military engineering paradigm"
        ],
        "expected_zh": [
            "著《吴起兵法》六篇，成先秦军事理论范本",
            "创魏武卒六重标准六级体系，成精兵工程化范本",
            "楚相推五战功法废四弊，确立战功制度",
            "法家军事化/精兵工程化/战功制度化三维融合"
        ],
        "expected_en": [
            "Authored 6-chapter Wu Qi Art of War, pre-Qin military theory paradigm",
            "Created Wei Wu Coelu 6 standards 6-tier system, elite soldier engineering paradigm",
            "Chu Chancellor implemented five merit laws, established merit system",
            "Legalist militarization/elite soldier engineering/merit system 3D fusion"
        ],
        "case_zh": "吴起（前440-前381），卫国人，曾子弟子，仕鲁/齐/魏/楚。著《吴起兵法》六篇：「图国/料敌/制将/治军/应变/劝学」。魏文侯相创武卒：选中男/甲五十斤/戈矛弩五十发/箭三十/粮三日/日行五十里，建六级精兵体系。楚悼王相推楚国变法：立五战功法废四弊，迁都郢扩民充国。贵族联合刺杀吴起，矢着尸，楚王令射吴起尸者赏。其法家军事化/精兵工程化/战功制度化/变法强国四维融合，成中国古代军事工程化奠基工程。",
        "case_en": "Wu Qi (440-381 BCE), Wei native, Zengzi disciple, served Lu/Qi/Wei/Chu. Authored 6-chapter Wu Qi Art of War: 'State Mapping/Enemy Assessment/General Selection/Army Governance/Adaptation/Learning Advocacy'. Wei Wenhou Chancellor created Wu Coelu: select adult males/50-jin armor/halberd-spear/crossbow 50 bolts/30 arrows/3-day rations/50 li daily, 6 standards, 6-tier elite soldier system. Chu Daowang Chancellor implemented Chu Reform: 'nobility by merit/office by merit/salary by merit/reward by merit/punishment by merit' five merit laws; abolished four abuses; moved capital to Ying. Nobles assassinated Wu Qi, arrows struck corpse, Chu king ordered 'who shoots Wu Qi corpse rewarded', arrows exhausted then stopped. His 'Legalist militarization/elite soldier engineering/merit system/reform strengthening state' four-dimensional fusion became Chinese ancient military engineering/Legalist militarization foundational project."
    },
    {
        "code": "H-BG-160",
        "name_zh": "白圭：平籴法/粮价调控/早期宏观调控/商业数学/财政工程化先驱",
        "name_en": "Bai Gui: Pingdi Method/Grain Price Regulation/Early Macro Regulation/Commercial Mathematics/Fiscal Engineering Pioneer",
        "description_zh": "平籴法/粮价调控/宏观调控/商业数学/财政工程/洛阳/大梁/魏文侯",
        "description_en": "Pingdi Method/Grain Price Regulation/Macro Regulation/Commercial Mathematics/Fiscal Engineering/Luoyang/Daliang/Wei Wenhou",
        "modes": [19, 20, 29, 28, 34],
        "reason_zh": "核心思维：在「战国粮价暴涨暴跌、农民商人两困、国家财政失控」背景下，以「平籴法/逆周期调控/商业数学建模」三重工程。",
        "reason_en": "Core Thinking: In 'Warring States grain price volatility, peasants and merchants both suffering, state fiscal out of control', engineered 'Pingdi method/counter-cyclical regulation/commercial mathematical modeling' triple project.",
        "steps_zh": [
            "第1步：抽象归纳法——提炼「逆周期/平抑/储备/调控」核心框架",
            "第2步：系统思维法——构建四维调控模型",
            "第3步：摸石头过河/实验主义——二十年致万金商业实验",
            "第4步：制度化制衡——推平籴法纳入三政体系",
            "第5步：总体性思维——形成中国古代宏观调控范式"
        ],
        "steps_en": [
            "Step 1: Abstract Induction — Extract 'counter-cyclical/suppression/reserve/regulation' core framework",
            "Step 2: Systems Thinking — Build four-dimensional regulation model",
            "Step 3: Crossing River by Feeling Stones — Twenty years ten thousand gold commercial experiment",
            "Step 4: Institutional Checks — Promoted Pingdi Method into three systems",
            "Step 5: Systems Thinking — Chinese ancient macro regulation paradigm"
        ],
        "expected_zh": [
            "创平籴法，成宏观调控/粮价平抑奠基范式",
            "建四维粮价调控体系",
            "著《白圭》十二篇创商业数学建模",
            "二十年致万金商业经营法，成商业数学/财政工程奠基"
        ],
        "expected_en": [
            "Created Pingdi Method, macro regulation/grain price stabilization paradigm",
            "Built 4D grain price regulation system",
            "Authored 12-chapter Baigui, created commercial mathematical modeling",
            "Twenty years ten thousand gold commercial operation, commercial math/fiscal engineering foundation"
        ],
        "case_zh": "白圭（前370-前300），洛阳人，战国著名经学家/商人/财政家。著《白圭》十二篇，创「平籴法」：丰年粮贱时平籴收购入仓，歉年粮贵时散籴抛售平抑物价，建常平仓/价格上下限四维调控体系。著《白圭》十二篇：「时/势/物/势/人/势」六势商业决策模型，以「投入/产出/周转/利润/风险/杠杆」六维商业函数量化决策。魏文侯相推平籴法国家粮政，建常平仓国家储备体系，二十年而家致万金商业经营法成战国奇迹。其四维融合，成中国古代宏观调控/商业数学/财政工程化奠基工程。",
        "case_en": "Bai Gui (370-300 BCE), Luoyang native, Warring States classical scholar/merchant/fiscal expert. Authored 12-chapter Baigui, created 'Pingdi Method': bumper harvest low price purchase into granary, poor harvest high price release stabilizing prices, built ever-normal granary/price ceiling-floor 4D regulation system. Authored 12-chapter Baigui: 'time/commodity/person' six-situation commercial decision model, with 'input/output/turnover/profit/risk/leverage' six-dimensional commercial function quantifying decisions. Wei Wenhou Chancellor promoted Pingdi Method national grain administration, built ever-normal granary state reserve system, twenty years household ten thousand gold commercial operation Warring States miracle. His four-dimensional fusion became Chinese ancient macro regulation/commercial mathematics/fiscal engineering foundational project."
    }
]

# Add to zh and en
for entry in new_entries:
    code = entry["code"]
    zh[code] = {
        "name": entry["name_zh"],
        "description": entry["description_zh"],
        "modes": entry["modes"],
        "reason": entry["reason_zh"],
        "steps": entry["steps_zh"],
        "expected": entry["expected_zh"],
        "case": entry["case_zh"]
    }
    en[code] = {
        "name": entry["name_en"],
        "description": entry["description_en"],
        "modes": entry["modes"],
        "reason": entry["reason_en"],
        "steps": entry["steps_en"],
        "expected": entry["expected_en"],
        "case": entry["case_en"]
    }
    cm["CODE_MAP"][code] = entry["name_zh"]
    cm["CODE_MAP_EN"][code] = entry["name_en"]

# Save files
with open('scenarios_zh.json', 'w', encoding='utf-8') as f:
    json.dump(zh, f, ensure_ascii=False, indent=2)
with open('scenarios_en.json', 'w', encoding='utf-8') as f:
    json.dump(en, f, ensure_ascii=False, indent=2)
with open('code_maps.json', 'w', encoding='utf-8') as f:
    json.dump(cm, f, ensure_ascii=False, indent=2)

print(f"✅ Added {len(new_entries)} new figures")