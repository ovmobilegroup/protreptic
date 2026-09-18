import json

# Load existing data
with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)
with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)
with open('code_maps.json', 'r', encoding='utf-8') as f:
    cm = json.load(f)

# Phase 1 Batch 3: More Legalist/Political Engineering + Mohist/Logicians
new_entries = [
    {
        "code": "H-LS-158",
        "name_zh": "李斯：秦帝国制度工程/焚书坑儒/车同轨书同文/秦制百代/制度工程化集大成者",
        "name_en": "Li Si: Qin Empire Institutional Engineering/Book Burning Scholar Burying/Unified Tracks Script/Ancient System Enduring/Institutional Engineering Master",
        "description_zh": "秦帝国/焚书坑儒/车同轨书同文/度量衡/郡县制/秦制百代/制度工程化",
        "description_en": "Qin Empire/Book Burning Scholar Burying/Unified Tracks Script/Weights Measures/Commandery-County System/Qin System Enduring/Institutional Engineering",
        "modes": [32, 34, 40, 18, 28],
        "reason_zh": "核心思维：在「六国并存、制度分裂、法家理论待落地」秦末，以「制度标准化/文字统一/度量衡统一/郡县制推行/思想统摄」五重工程化落地——著《谏逐客书》以「泰山不让土壤/河海不择细流」推动人才引进；推「焚书坑儒」以「诗书/百家语/秦记」三禁实现思想统摄；推「车同轨/书同文/车同轨/度量衡」四统一，建立「尺/寸/丈/引/石/斗/升/合/斤/两/钱/两」十维度量衡标准体系；推「郡县制」废分封，建「三十六郡/守/尉/监」三级行政架构；建「秦律/十八律/什伍/连坐/集体责任」法制体系。其「标准化/统一/工程化/集权/法治」五维工程化落地，成中国历史上首个「帝国级制度工程」范式，成「秦制百代」制度基因奠基工程。",
        "reason_en": "Core Thinking: In 'Six states coexisting, systems divided, Legalist theory awaiting implementation' late Qin, engineered 'system standardization/text unification/weights unification/commandery-county implementation/thought unification' five-dimensional engineering implementation — authored Memorial Against Expelling Guests with 'Tai Shan not rejecting soil/Rivers not rejecting streams' advancing talent import; implemented 'book burning scholar burying' via 'poetry/hundred schools/Qin records' three bans achieving thought unification; implemented 'unified tracks/scripts/weights' four unifications, establishing 'chi/cun/zhang/yin/shi/dou/sheng/he/jin/liang/qian/liang' ten-dimensional weights standards; implemented 'commandery-county system' abolishing enfeoffment, building '36 commanderies/governor/professor/supervisor' three-tier admin architecture; built 'Qin Law/18 statutes/squad/collective responsibility' legal system. His 'standardization/unification/engineering/centralization/rule of law' five-dimensional engineering implementation became China's first 'empire-level institutional engineering' paradigm, foundational project of 'Qin system enduring generations' institutional genes.",
        "steps_zh": [
            "第1步：抽象归纳法——从「六国制度不一/文字不通/度量衡异」痛点中提炼「统一/标准/工程化」核心框架，生成「秦制」工程化蓝图",
            "第2步：系统思维法——构建「文字/度量衡/货币/法律/行政/思想」六系统耦合模型，将「书/车/量/币/法/郡/县/吏/民/书」十维强耦合",
            "第3步：摸石头过河/实验主义——以「焚书/坑儒/统一文字/统一度量衡/推行郡县」五大工程并行推进，以「秦律/什伍/连坐」强制落地",
            "第4步：制度化制衡——建「三十六郡/守/尉/监」三级行政架构，以「秦律/十八律/什伍/连坐」法制体系固化制度成果",
            "第5步：总体性思维——将「标准化/统一/工程化/集权/法治」五系统耦合，形成「标准化→统一→工程化→集权→法治」帝国级制度工程范式"
        ],
        "steps_en": [
            "Step 1: Abstract Induction — Extract 'unification/standardization/engineering' core framework from 'six states systems differ/scripts differ/weights differ' pain points, generating 'Qin System' engineering blueprint",
            "Step 2: Systems Thinking — Build 'text/weights/currency/law/admin/thought' six-system coupling model, strongly coupling 'script/tracks/weights/currency/law/commandery/county/official/people/script' ten dimensions",
            "Step 3: Crossing River by Feeling Stones — Five major projects 'burn books/bury scholars/unify script/unify weights/implement commanderies' parallel push, enforced via 'Qin Law/squad/collective responsibility'",
            "Step 4: Institutional Checks — Built '36 commanderies/governor/professor/supervisor' three-tier admin architecture, solidified institutional gains via 'Qin Law/18 statutes/squad/collective responsibility' legal system",
            "Step 5: Systems Thinking — Couple 'standardization/unification/engineering/centralization/rule of law' five systems into 'standardization→unification→engineering→centralization→rule of law' empire-level institutional engineering paradigm"
        ],
        "expected_zh": [
            "推「车同轨/书同文/车同轨/度量衡」四统一，建十维度量衡标准体系",
            "推「郡县制」废分封，建「三十六郡/守/尉/监」三级行政架构",
            "建「秦律/十八律/什伍/连坐」法制体系，推「焚书坑儒」思想统摄",
            "成中国首个「帝国级制度工程」范式，奠「秦制百代」制度基因"
        ],
        "expected_en": [
            "Implemented 'unified tracks/scripts/weights' four unifications, built 10-dimensional weights standards",
            "Implemented commandery-county system abolishing enfeoffment, built 36 commanderies/governor/professor/supervisor 3-tier admin",
            "Built 'Qin Law/18 statutes/squad/collective responsibility' legal system, 'book burning scholar burying' thought unification",
            "Became China's first 'empire-level institutional engineering' paradigm, founding 'Qin system enduring generations' institutional genes"
        ],
        "case_zh": "李斯（前280-前208），楚国上蔡人，荀子弟子，秦始皇丞相。著《谏逐客书》「泰山不让土壤/河海不择细流/王者不却众庶/地大/国强」，力主用人唯才。推「焚书坑儒」：禁「诗书/百家语/秦记」私藏，唯留「秦记/医药/卜筮/农桑」四类，统摄思想。推「四统一」：车同轨（车轨六尺）、书同文（小篆/隶书/草书）、度量衡（权/衡/度/量/虚/实/十度/十量/十量/十量）、货币统一（圜法/半两/-ban-liang/半两）。推「郡县制」：废分封，建三十六郡，置守/尉/监三级吏，废封建分封。建「秦律」十八律：什伍/连坐/集体责任/互保/告密/赏罚，秦二世时赵高矫诏杀李斯。其「标准化/统一/工程化/集权/法治」五维工程化落地，成中国首个「帝国级制度工程」范式，奠「秦制百代」制度基因，影响汉唐宋元明清制度建设全版图。",
        "case_en": "Li Si (280-208 BCE), Chu Shangcai native, Xunzi disciple, Qin Shihuang Chancellor. Authored Memorial Against Expelling Guests 'Tai Shan not rejecting soil/Rivers not rejecting streams/Kings not rejecting masses/land large/state strong', advocating merit-based employment. Implemented 'book burning scholar burying': banned 'poetry/hundred schools/Qin records' private possession, retained only 'Qin records/medicine/divination/agriculture' four categories, unifying thought. Implemented 'four unifications': unified tracks (6 chi gauge), unified script (small seal/clerical/cursive), unified weights (10-dimensional standards), unified currency (round coin/ban-liang). Implemented commandery-county system: abolished enfeoffment, built 36 commanderies with governor/professor/supervisor three-tier officials, abolished feudal enfeoffment. Built 'Qin Law' 18 statutes: squad/collective responsibility/mutual guarantee/informing/rewards-punishments; Zhao Gao forged edict killing Li Si under Qin Er Shi. His 'standardization/unification/engineering/centralization/rule of law' five-dimensional engineering became China's first 'empire-level institutional engineering' paradigm, founding 'Qin system enduring generations' institutional genes, influencing Han-Tang-Song-Yuan-Ming-Qing institutional construction entire landscape."
    },
    {
        "code": "H-WQ-159",
        "name_zh": "吴起：变法/兵法/吴起兵法/楚国变法/法家军事化/军事工程化先驱",
        "name_en": "Wu Qi: Reform/Military Strategy/Wu Qi Art of War/Chu Reform/Legalist Militarization/Military Engineering Pioneer",
        "description_zh": "吴起兵法/楚国变法/法家军事化/军事工程化/魏武卒/六论/图国",
        "description_en": "Wu Qi Art of War/Chu Reform/Legalist Militarization/Military Engineering/Wei Wu Coelu/Six Discourses/State Mapping",
        "modes": [15, 32, 16, 28, 35],
        "reason_zh": "核心思维：在「战国弱国楚国、贵族特权横行、军事松懈、法家理论待军事化」背景下，以「法家军事化/变法强军/军事工程化」三重工程——著《吴起兵法》六篇：「图国/料敌/制将/治军/应变/劝学」六维军事理论体系，将「地理/民心/将才/军纪/战术/学问」六维纳入量化考核；创「魏武卒」：选「中男/带甲五十斤/戈矛/弩五十发/箭三十/赍三日粮/日行五十里」六重标准，建「选/练/考/赏/罚/淘」六级精兵培育体系；楚悼王相位推「楚国变法」：以「贵以战功/官以战功/禄以战功/赏以战功/罚以战功」五战功法，废「世卿世禄/游食贵族/远亲/疏属」四弊，迁都郢/徙郢/扩民/充国。其「法家军事化/变法强军/工程化精兵/战功制度」四维融合，成中国古代军事工程化/法家军事化奠基工程。",
        "reason_en": "Core Thinking: In 'weak Chu state Warring States, noble privileges rampant, military lax, Legalist theory awaiting militarization', engineered 'Legalist militarization/reform strengthening military/military engineering' triple project — authored 6-chapter Wu Qi Art of War: 'state mapping/enemy assessment/general selection/army governance/adaptation/learning advocacy' six-dimensional military theory system, quantifying 'geography/popular sentiment/general talent/military discipline/tactics/learning' six dimensions; created 'Wei Wu Coelu': selecting 'adult males/wearing 50-jin armor/halberd-spear/crossbow 50 bolts/30 arrows/carrying 3-day rations/marching 50 li daily' six standards, building 'selection/training/assessment/reward/punishment/elimination' six-tier elite soldier cultivation system; as Chu Chancellor implemented 'Chu Reform': 'nobility by merit/office by merit/salary by merit/reward by merit/punishment by merit' five merit laws, abolished 'hereditary nobility/hereditary salary/idle nobles/distant relatives/collateral relatives' four abuses, moved capital to Ying. His 'Legalist militarization/reform strengthening military/engineering elite soldiers/merit system' four-dimensional fusion became Chinese ancient military engineering/Legalist militarization foundational project.",
        "steps_zh": [
            "第1步：抽象归纳法——从「军事松懈/贵族特权/战法陈旧」痛点中提炼「战功/选练/考核/赏罚」核心框架，生成「吴起兵法」军事理论模板",
            "第2步：系统思维法——构建「选/练/考/赏/罚/淘」六级精兵体系与「图/料/制/治/应/劝」六维理论模型",
            "第3步：摸石头过河/实验主义——在魏创「武卒」以「六重标准/六级体系」小规模试点，验证精兵模式可行性",
            "第4步：制度化制衡——楚相位推「五战功法/废四弊/迁都/扩民」四重变法，以「战功定贵/战功定官/战功定禄/战功定赏/战功定罚」固化变法成果",
            "第5步：总体性思维——将「法家/军事/变法/精兵/战功」五系统耦合，形成「法家军事化→精兵工程化→战功制度化→强国富军」中国古代军事工程化范式"
        ],
        "steps_en": [
            "Step 1: Abstract Induction — Extract 'merit/selection-training/assessment/rewards-punishments' core framework from 'military lax/noble privileges/outdated tactics' pain points, generating 'Wu Qi Art of War' military theory template",
            "Step 2: Systems Thinking — Build 'selection/training/assessment/reward/punishment/elimination' six-tier elite soldier system with 'state-map/enemy-assessment/general-selection/army-governance/adaptation/learning-advocacy' six-dimensional theory model",
            "Step 3: Crossing River by Feeling Stones — In Wei created 'Wu Coelu' via 'six standards/six-tier system' pilot, validating elite soldier model feasibility",
            "Step 4: Institutional Checks — As Chu Chancellor implemented 'five merit laws/abolish four abuses/move capital/expand populace' four reforms, solidifying reform gains via 'merit nobility/merit office/merit salary/merit reward/merit punishment'",
            "Step 5: Systems Thinking — Couple 'Legalist/military/reform/elite-soldiers/merit' five systems into 'Legalist militarization→elite soldier engineering→merit system institutionalization→strong state strong military' Chinese ancient military engineering paradigm"
        ],
        "expected_zh": [
            "著《吴起兵法》六篇，成先秦军事理论六维体系范本",
            "创「魏武卒」六重标准六级体系，成古代精兵工程化范本",
            "楚相位推「五战功法/废四弊」变法，确立「战功定贵官禄赏罚」制度",
            "「法家军事化/精兵工程化/战功制度化」三维融合，成中国古代军事工程化奠基"
        ],
        "expected_en": [
            "Authored 6-chapter Wu Qi Art of War, pre-Qin military theory 6D paradigm",
            "Created Wei Wu Coelu 6 standards 6-tier system, ancient elite soldier engineering paradigm",
            "Chu Chancellor implemented five merit laws, established 'merit determines nobility/office/salary/reward/punishment' system",
            "'Legalist militarization/elite soldier engineering/merit system institutionalization' 3D fusion, Chinese ancient military engineering foundation"
        ],
        "case_zh": "吴起（前440-前381），卫国人，曾子弟子，仕鲁/齐/魏/楚。著《吴起兵法》六篇：「图国/料敌/制将/治军/应变/劝学」，构建「地理/民心/将才/军纪/战术/学问」六维军事理论体系。魏文侯相，创「武卒」：选中男，带甲五十斤，戈/矛/弩五十发/箭三十，赍三日粮，日行五十里，六重标准，建「选/练/考/赏/罚/淘」六级精兵体系，武卒战无不胜。楚悼王相，推「楚国变法」：立「贵以战功/官以战功/禄以战功/赏以战功/罚以战功」五战功法；废「世卿世禄/游食贵族/远亲/疏属」四弊；迁都郢，徙郢扩民，充实国力。贵族联合刺杀吴起，矢着尸，楚王命「射吴起尸者赏」，矢尽乃已。其「法家军事化/精兵工程化/战功制度/变法强国」四维融合，成中国古代军事工程化/法家军事化奠基工程，影响孙武/孙膑/韩信/诸葛亮/曹操/戚继光/曾国藩/左宗棠/彭德怀/林彪/粟裕军事思想全版图。",
        "case_en": "Wu Qi (440-381 BCE), Wei native, Zengzi disciple, served Lu/Qi/Wei/Chu. Authored 6-chapter Wu Qi Art of War: 'State Mapping/Enemy Assessment/General Selection/Army Governance/Adaptation/Learning Advocacy', constructing 'geography/popular sentiment/general talent/military discipline/tactics/learning' 6D military theory system. Wei Wenhou Chancellor, created 'Wu Coelu': select adult males, wear 50-jin armor, halberd/spear/crossbow 50 bolts/30 arrows, carry 3-day rations, march 50 li daily, 6 standards, built 'selection/training/assessment/reward/punishment/elimination' 6-tier elite soldier system, Wu Coelu undefeated. Chu Daowang Chancellor, implemented 'Chu Reform': 'nobility by merit/office by merit/salary by merit/reward by merit/punishment by merit' five merit laws; abolished 'hereditary nobility/hereditary salary/idle nobles/distant relatives/collateral relatives' four abuses; moved capital to Ying, expanded populace, strengthened state. Nobles assassinated Wu Qi, arrows struck corpse, Chu king ordered 'who shoots Wu Qi corpse rewarded', arrows exhausted then stopped. His 'Legalist militarization/elite soldier engineering/merit system/reform strengthening state' four-dimensional fusion became Chinese ancient military engineering/Legalist militarization foundational project, influencing Sun Wu/Sun Bin/Han Xin/Zhuge Liang/Cao Cao/Qi Jiguang/Zeng Guofan/Zuo Zongtang/Peng Dehuai/Lin Biao/Su Yu military thought entire landscape."
    },
    {
        "code": "H-BG-160",
        "name_zh": "白圭：平籴法/粮价调控/早期宏观调控/商业数学/财政工程化先驱",
        "name_en": "Bai Gui: Pingdi Method/Grain Price Regulation/Early Macro Regulation/Commercial Mathematics/Fiscal Engineering Pioneer",
        "description_zh": "平籴法/粮价调控/宏观调控/商业数学/财政工程/洛阳/大梁/魏文侯",
        "description_en": "Pingdi Method/Grain Price Regulation/Macro Regulation/Commercial Mathematics/Fiscal Engineering/Luoyang/Daliang/Wei Wenhou",
        "modes": [19, 20, 29, 28, 34],
        "reason_zh": "核心思维：在「战国粮价暴涨暴跌、农民商人两困、国家财政失控」背景下，以「平籴法/逆周期调控/商业数学建模」三重工程——创「平籴法」：以「丰年收购/歉年抛售/价格平抑/利农惠商」四维调控模型，建「丰年平籴/歉年散籴/常平仓/价格上下限」四维粮价调控体系；著《白圭》十二篇，创「商业数学建模」：以「投入/产出/周转/利润/风险/杠杆」六维商业函数，将「农时/水旱/丰歉/价格/成本/利润」六维纳入量化决策模型；魏文侯相位，推「二十年而家致万金」商业经营法，以「时/势/物/势/人/势」六势商业决策模型。其「平籴法/逆周期/商业数学/宏观调控」四维融合，成中国古代宏观调控/商业数学/财政工程化奠基工程。",
        "reason_en": "Core Thinking: In 'Warring States grain price volatility, peasants and merchants both suffering, state fiscal out of control', engineered 'Pingdi method/counter-cyclical regulation/commercial mathematical modeling' triple project — created 'Pingdi Method': 'bumper harvest purchase/poor harvest release/price suppression/benefit farmers and merchants' four-dimensional regulation model, built 'bumper purchase/poor harvest release/ever-normal granary/price ceiling-floor' four-dimensional grain price regulation system; authored 12-chapter Baigui, created 'commercial mathematical modeling': 'input/output/turnover/profit/risk/leverage' six-dimensional commercial function, incorporating 'agricultural timing/drought-flood/bumper-poor/price/cost/profit' six dimensions into quantified decision model; as Wei Chancellor achieved 'twenty years household ten thousand gold' commercial operation, with 'timing/situation/commodity/situation/person/situation' six-situation commercial decision model. His 'Pingdi method/counter-cyclical/commercial mathematics/macro regulation' four-dimensional fusion became Chinese ancient macro regulation/commercial mathematics/fiscal engineering foundational project.",
        "steps_zh": [
            "第1步：抽象归纳法——从「粮价暴涨暴跌/农商两困/财政失控」痛点中提炼「逆周期/平抑/储备/调控」核心框架，生成「平籴法」调控模型模板",
            "第2步：系统思维法——构建「丰年收购/歉年抛售/常平仓/价格上下限」四维调控模型，将「收购/抛售/储备/价格/成本/利润」六维强耦合",
            "第3步：摸石头过河/实验主义——以「二十年致万金」商业实验验证平籴法可行性，建「常平仓/价格上下限」制度化落地",
            "第4步：制度化制衡——推动「平籴法」纳入「国家财政/粮政/商政」三政体系，以「常平仓/价格上下限/收购抛售标准」制度化落地",
            "第5步：总体性思维——将「平籴法/逆周期/商业数学/宏观调控/商业经营」五系统耦合，形成「调控模型→数学建模→商业验证→制度落地」中国古代宏观调控范式"
        ],
        "steps_en": [
            "Step 1: Abstract Induction — Extract 'counter-cyclical/suppression/reserve/regulation' core framework from 'grain price volatility/peasants-merchants both suffering/fiscal out of control' pain points, generating 'Pingdi Method' regulation model template",
            "Step 2: Systems Thinking — Build 'bumper purchase/poor harvest release/ever-normal granary/price ceiling-floor' four-dimensional regulation model, strongly coupling 'purchase/release/reserve/price/cost/profit' six dimensions",
            "Step 3: Crossing River by Feeling Stones — Validated Pingdi Method feasibility with 'twenty years ten thousand gold' commercial experiment, institutionalizing 'ever-normal granary/price ceiling-floor'",
            "Step 4: Institutional Checks — Promoted 'Pingdi Method' into 'state fiscal/grain administration/commercial administration' three systems, institutionalizing 'ever-normal granary/price ceiling-floor/purchase-release standards'",
            "Step 5: Systems Thinking — Couple 'Pingdi method/counter-cyclical/commercial math/macro regulation/commercial operation' five systems into 'regulation model→math modeling→commercial validation→institutional implementation' Chinese ancient macro regulation paradigm"
        ],
        "expected_zh": [
            "创「平籴法」，成中国古代宏观调控/粮价平抑奠基范式",
            "建「丰年平籴/歉年散籴/常平仓/价格上下限」四维粮价调控体系",
            "著《白圭》十二篇，创「商业数学建模」：六维商业函数量化决策",
            "「二十年致万金」商业经营法，成中国古代商业数学/财政工程奠基"
        ],
        "expected_en": [
            "Created 'Pingdi Method', Chinese ancient macro regulation/grain price stabilization foundational paradigm",
            "Built 'bumper purchase/poor harvest release/ever-normal granary/price ceiling-floor' 4D grain price regulation system",
            "Authored 12-chapter Baigui, created 'commercial mathematical modeling': 6D commercial function quantifying decisions",
            "'Twenty years ten thousand gold' commercial operation, Chinese ancient commercial mathematics/fiscal engineering foundation"
        ],
        "case_zh": "白圭（前370-前300），洛阳人，战国著名经学家/商人/财政家。著《白圭》十二篇，创「平籴法」：丰年粮贱时「平籴」收购入仓，歉年粮贵时「散籴」抛售平抑物价，建「常平仓/价格上下限」四维调控体系。著《白圭》十二篇：「时/势/物/势/人/势」六势商业决策模型：时势（农时/季节）、物势（丰歉/物价）、人势（需求/心理），以「投入/产出/周转/利润/风险/杠杆」六维商业函数量化决策。魏文侯相，推「平籴法」国家粮政，建「常平仓」国家储备体系，「二十年而家致万金」商业经营法成战国奇迹。其「平籴法/逆周期/商业数学/宏观调控」四维融合，成中国古代宏观调控/商业数学/财政工程化奠基工程，影响桑弘羊/刘晏/王安石/张居正/曾国藩/李鸿章/张之洞/薛暮桥/李先念/朱镕基宏观调控思想全版图。",
        "case_en": "Bai Gui (370-300 BCE), Luoyang native, Warring States classical scholar/merchant/fiscal expert. Authored 12-chapter Baigui, created 'Pingdi Method': bumper harvest low price 'pingdi' purchase into granary, poor harvest high price 'san di' release stabilizing prices, built 'ever-normal granary/price ceiling-floor' four-dimensional regulation system. Authored 12-chapter Baigui: 'time/commodity/person' six-situation commercial decision model: timing (agricultural seasons), commodity situation (bumper-poor/prices), person situation (demand/psychology), with 'input/output/turnover/profit/risk/leverage' six-dimensional commercial function quantifying decisions. Wei Wenhou Chancellor, promoted 'Pingdi Method' national grain administration, built 'ever-normal granary' state reserve system, 'twenty years household ten thousand gold' commercial operation Warring States miracle. His 'Pingdi method/counter-cyclical/commercial mathematics/macro regulation' four-dimensional fusion became Chinese ancient macro regulation/commercial mathematics/fiscal engineering foundational project, influencing Sang Hongyang/Liu Yan/Wang Anshi/Zhang Juzheng/Zeng Guofan/Li Hongzhang/Zhang Zhidong/Xue Muqiao/Li Xiannian/Zhu Rongji macro regulation thought entire landscape."
    },
    # ============ 墨家/名家/逻辑学派 (3) ============
    {
        "code": "H-MZB-161",
        "name_zh": "墨子后学技术派：孟胜/田俅/相里勤/腹谮/胡非/离朱/徐无鬼/耕柱/胡子/邓陵——几何/光学/力学/技术标准化先驱",
        "name_en": "Mohist Later Technical School: Meng Sheng/Tian Qiu/Xiang Liqin/Fu Zhen/Hu Fei/Li Zhu/Xu Wugui/Geng Zhu/Hu Zi/Deng Ling — Geometry/Optics/Mechanics/Technical Standardization Pioneers",
        "description_zh": "墨家后学/几何/光学/力学/技术标准化/墨经/小取/经上/经下/大取",
        "description_en": "Mohist Later School/Geometry/Optics/Mechanics/Technical Standardization/Mojing/Xiaoqu/Jingshang/Jingxia/Daqu",
        "modes": [19, 24, 25, 28, 35],
        "reason_zh": "核心思维：在「墨家兼爱非攻/逻辑/几何/光学/力学」理论基础上，以「实验/标准化/工程化/量化」四重工程化推进——《墨经》「小取/经上/经下/大取」四编，系统记载「定/说/由/过/等/长/短/方/圆/平/直/重/轻/同/异/合/离/动/止/快/慢/并/散/聚/合/离/同/异」五十余核心概念，建立「定义/公理/定理/推理/实验/验证」六步几何/光学/力学理论体系；实测「小孔成像/凸透镜聚焦/杠杆原理/滑轮/齿轮/弹簧/弓弩/云梯/攻城器」十大物理/工程实验，建「假设/实验/测量/计算/验证/标准化」六步实验科学范式；创「墨家机关/攻城器/防御工事/测量仪器」四大工程化交付物。其「定义/公理/定理/实验/标准化」五步法，成中国古代实验科学/工程技术/技术标准化奠基工程。",
        "reason_en": "Core Thinking: On 'Mohist universal love non-aggression/logic/geometry/optics/mechanics' theoretical foundation, advanced 'experiment/standardization/engineering/quantification' quadruple engineering — Mojing 'Xiaoqu/Jingshang/Jingxia/Daqu' four volumes, systematically recording 'definition/explanation/derivation/over/equal/long/short/square/round/flat/straight/heavy/light/same/different/combine/separate/move/stop/fast/slow/parallel/disperse/gather/combine/separate/same/different' fifty-plus core concepts, establishing 'definition/axiom/theorem/reasoning/experiment/verification' six-step geometry/optics/mechanics theory system; empirically tested 'pinhole imaging/convex lens focusing/lever principle/pulley/gear/spring/bow-crossbow/cloud ladder/siege engines' ten major physics/engineering experiments, establishing 'hypothesis/experiment/measurement/calculation/verification/standardization' six-step experimental science paradigm; created 'Mohist mechanisms/siege engines/defense fortifications/surveying instruments' four major engineering deliverables. His 'definition/axiom/theorem/experiment/standardization' five-step method became Chinese ancient experimental science/engineering technology/technical standardization foundational project.",
        "steps_zh": [
            "第1步：抽象归纳法——从《墨经》五十余概念中提炼「定/说/由/过/等/长/短/方/圆/平/直/重/轻/同/异」核心概念簇，生成几何/光学/力学理论框架",
            "第2步：系统思维法——构建「定义/公理/定理/推理/实验/验证」六步理论体系与「假设/实验/测量/计算/验证/标准化」六步实验范式",
            "第3步：摸石头过河/实验主义——实测「小孔成像/凸透镜/杠杆/滑轮/齿轮/弹簧/弓弩/云梯/攻城器」十大实验，建实验科学范式",
            "第4步：制度化制衡——推动《墨经》四编成「定义/公理/定理/推理/实验/验证」标准化教材，以文本固化技术防失传",
            "第5步：总体性思维——将「几何/光学/力学/实验/标准化/工程化」六系统耦合，形成中国古代实验科学/技术标准化/工程技术奠基范式"
        ],
        "steps_en": [
            "Step 1: Abstract Induction — Extract 'definition/explanation/derivation/over/equal/long/short/square/round/flat/straight/heavy/light/same/different' core concept cluster from Mojing fifty-plus concepts, generating geometry/optics/mechanics theory framework",
            "Step 2: Systems Thinking — Build 'definition/axiom/theorem/reasoning/experiment/verification' six-step theory system with 'hypothesis/experiment/measurement/calculation/verification/standardization' six-step experimental paradigm",
            "Step 3: Crossing River by Feeling Stones — Empirically tested 'pinhole imaging/convex lens/lever/pulley/gear/spring/bow-crossbow/cloud ladder/siege engines' ten experiments, establishing experimental science paradigm",
            "Step 4: Institutional Checks — Promoted Mojing four volumes as 'definition/axiom/theorem/reasoning/experiment/verification' standardized textbook, solidifying technology via text preventing loss",
            "Step 5: Systems Thinking — Couple 'geometry/optics/mechanics/experiment/standardization/engineering' six systems into Chinese ancient experimental science/technical standardization/engineering technology foundational paradigm"
        ],
        "expected_zh": [
            "《墨经》四编系统记载五十余核心概念，成中国古代几何/光学/力学理论奠基",
            "实测十大物理/工程实验，建「假设/实验/测量/计算/验证/标准化」六步实验范式",
            "创「墨家机关/攻城器/防御工事/测量仪器」四大工程化交付物",
            "「定义/公理/定理/实验/标准化」五步法，成中国古代实验科学/技术标准化奠基"
        ],
        "expected_en": [
            "Mojing four volumes systematically record fifty-plus core concepts, founding Chinese ancient geometry/optics/mechanics theory",
            "Empirically tested ten major physics/engineering experiments, establishing 'hypothesis/experiment/measurement/calculation/verification/standardization' six-step experimental paradigm",
            "Created 'Mohist mechanisms/siege engines/defense fortifications/surveying instruments' four engineering deliverables",
            "'Definition/axiom/theorem/experiment/standardization' five-step method, Chinese ancient experimental science/technical standardization foundation"
        ],
        "case_zh": "墨子后学技术派（前350-前200），墨子弟子及再传弟子：孟胜/田俅/相里勤/腹谮/胡非/离朱/徐无鬼/耕柱/胡子/邓陵等十子。著《墨经》「小取/经上/经下/大取」四编，系统定义「节/幂/求/尽/称/任/胜/亏/盈/虚/实/满/空/盈/虚/等/不等/长/短/方/圆/平/直/重/轻/同/异/并/散/合/离/动/止/快/慢/并/散/聚/合/离/同/异/过/不及/参/半/倍/什/百/千/万/亿」五十余核心概念，建立「定义/公理/定理/推理/实验/验证」六步理论体系。实测「小孔成像（光学）/凸透镜聚焦（光学）/杠杆原理（力学）/滑轮组（力学）/齿轮传动（力学）/弹簧弹性（力学）/弓弩机械（工学）/云梯攻城（工学）/测量仪器（工学）」十大实验，建「假设/实验/测量/计算/验证/标准化」六步实验范式。创「墨家机关/攻城器/防御工事/测量仪器」四大工程化交付物。其「定义/公理/定理/实验/标准化」五步法，成中国古代实验科学/工程技术/技术标准化奠基工程，影响张衡/沈括/郭守敬/宋应星/徐光启/李时珍/朱载堉/华罗庚/钱学森/竺可桢科学工程化传统全版图。",
        "case_en": "Mohist Later Technical School (350-200 BCE), Mozi disciples and second-gen: Meng Sheng/Tian Qiu/Xiang Liqin/Fu Zhen/Hu Fei/Li Zhu/Xu Wugui/Geng Zhu/Hu Zi/Deng Ling. Authored Mojing 'Xiaoqu/Jingshang/Jingxia/Daqu' four volumes, systematically defining 'node/endpoint/seeking/exhaustive/measure/burden/victory/deficit/surplus/empty/full/empty/full/surplus/empty/equal/unequal/long/short/square/round/flat/straight/heavy/light/same/different/parallel/disperse/gather/combine/separate/move/stop/fast/slow/parallel/disperse/gather/combine/separate/same/different/over/under/half/half/double/ten/hundred/thousand/ten-thousand/hundred-million' fifty-plus core concepts, establishing 'definition/axiom/theorem/reasoning/experiment/verification' six-step theory system. Empirically tested 'pinhole imaging (optics)/convex lens focusing (optics)/lever principle (mechanics)/pulley system (mechanics)/gear transmission (mechanics)/spring elasticity (mechanics)/bow-crossbow mechanism (engineering)/cloud ladder siege (engineering)/surveying instruments (engineering)' ten experiments, establishing 'hypothesis/experiment/measurement/calculation/verification/standardization' six-step experimental paradigm. Created 'Mohist mechanisms/siege engines/defense fortifications/surveying instruments' four engineering deliverables. Their 'definition/axiom/theorem/experiment/standardization' five-step method became Chinese ancient experimental science/engineering technology/technical standardization foundational project, influencing Zhang Heng/Shen Kuo/Guo Shoujing/Song Yingxing/Xu Guangqi/Li Shizhen/Zhu Zaiyu/Hua Luogeng/Qian Xuesen/Zhu Kezhen scientific engineering tradition entire landscape."
    },
    {
        "code": "H-YW-162",
        "name_zh": "尹文/彭蒙/田骈：名家/辩论/白马非马/坚白同异/逻辑分类学/概念工程先驱",
        "name_en": "Yin Wen/Peng Meng/Tian Bian: Logicians School/Debate/White Horse Not Horse/Hard-White Identity-Difference/Logical Taxonomy/Concept Engineering Pioneers",
        "description_zh": "名家/辩论/白马非马/坚白同异/逻辑分类/概念工程/公孙龙/惠施/尹文/彭蒙/田骈",
        "description_en": "Logicians School/Debate/White Horse Not Horse/Hard-White Identity-Difference/Logical Taxonomy/Concept Engineering/Gongsun Long/Hui Shi/Yin Wen/Peng Meng/Tian Bian",
        "modes": [24, 31, 37, 28, 35],
        "reason_zh": "核心思维：在「战国百家争鸣、概念混淆、辩论无标准、分类学缺失」背景下，以「概念澄清/分类构建/辩论标准化/逻辑工程化」四重工程——尹文著《尹子》：「物/类/同/异/是/非/可/否/知/不知/辩/不辩」十二核心范畴，建「概念/命题/推理/辩论」四维逻辑框架；彭蒙著《彭蒙子》：「坚/白/同/异/离/合/动/止/新/故/始/终」十二范畴，破「公孙龙白马非马」与「惠施十事」辩论僵局，确立「属性/实体/关系/过程」四维本体论分类；田骈著《田子》：「大/小/多/少/长/短/方/圆/平/直/重/轻/同/异」十二范畴，建「量/质/关/度」四维度量分类学。其「概念澄清/分类构建/辩论标准化/逻辑工程化」四重工程，成中国古代逻辑学/概念工程/分类学奠基工程。",
        "reason_en": "Core Thinking: In 'Warring States hundred schools contending, conceptual confusion, debate without standards, taxonomy missing', engineered 'concept clarification/taxonomy construction/debate standardization/logic engineering' quadruple project — Yin Wen authored Yinsi: 'thing/category/same/different/is/not/can/not/know/unknow/debate/not-debate' twelve core categories, building 'concept/proposition/reasoning/debate' four-dimensional logic framework; Peng Meng authored Pengmengzi: 'hard/white/same/different/separate/combine/move/stop/new/old/begin/end' twelve categories, breaking 'Gongsun Long white horse not horse' and 'Hui Shi ten matters' debate deadlock, establishing 'attribute/entity/relation/process' four-dimensional ontology classification; Tian Bian authored Tianzi: 'large/small/many/few/long/short/square/round/flat/straight/heavy/light/same/different' twelve categories, establishing 'quantity/quality/relation/degree' four-dimensional measurement taxonomy. Their 'concept clarification/taxonomy construction/debate standardization/logic engineering' quadruple project became Chinese ancient logic/concept engineering/taxonomy foundational project.",
        "steps_zh": [
            "第1步：抽象归纳法——从「白马非马/坚白同异/十事」辩论中提炼「属性/实体/关系/过程/量/质/关/度」核心本体论范畴",
            "第2步：系统思维法——构建「概念/命题/推理/辩论/分类/度量」六维逻辑工程框架",
            "第3步：摸石头过河/实验主义——以「辩论/分类/度量」实战验证逻辑工程可行性，在稷下学宫公开辩论验证",
            "第4步：制度化制衡——推动《尹子/彭蒙子/田子》纳入「名家经典」，以著述固化逻辑工程标准",
            "第5步：总体性思维——将「概念/命题/推理/辩论/分类/度量」六系统耦合，形成中国古代逻辑学/概念工程/分类学奠基范式"
        ],
        "steps_en": [
            "Step 1: Abstract Induction — Extract 'attribute/entity/relation/process/quantity/quality/relation/degree' core ontology categories from 'white horse not horse/hard-white identity-difference/ten matters' debates",
            "Step 2: Systems Thinking — Build 'concept/proposition/reasoning/debate/classification/measurement' six-dimensional logic engineering framework",
            "Step 3: Crossing River by Feeling Stones — Validate logic engineering feasibility via 'debate/classification/measurement' practice, public debates at Jixia Academy",
            "Step 4: Institutional Checks — Promoted Yinshi/Pengmengzi/Tianzi into 'Logicians classics', solidifying logic engineering standards via writings",
            "Step 5: Systems Thinking — Couple 'concept/proposition/reasoning/debate/classification/measurement' six systems into Chinese ancient logic/concept engineering/taxonomy foundational paradigm"
        ],
        "expected_zh": [
            "《尹子/彭蒙子/田子》确立「属性/实体/关系/过程/量/质/关/度」本体论分类学",
            "破「白马非马/坚白同异/十事」辩论僵局，确立「辩论标准化/分类学」范式",
            "建「属性/实体/关系/过程」四维本体论与「量/质/关/度」四维度量分类学",
            "成中国古代逻辑学/概念工程/分类学奠基工程"
        ],
        "expected_en": [
            "Yinshi/Pengmengzi/Tianzi established 'attribute/entity/relation/process/quantity/quality/relation/degree' ontology taxonomy",
            "Broke 'white horse not horse/hard-white identity-difference/ten matters' debate deadlock, established 'debate standardization/taxonomy' paradigm",
            "Built 'attribute/entity/relation/process' 4D ontology and 'quantity/quality/relation/degree' 4D measurement taxonomy",
            "Became Chinese ancient logic/concept engineering/taxonomy foundational project"
        ],
        "case_zh": "尹文/彭蒙/田骈（前350-前280），齐/宋/赵人，稷下学宫学者。尹文著《尹子》：「物/类/同/异/是/非/可/否/知/不知/辩/不辩」十二范畴，建「概念/命题/推理/辩论」逻辑框架，主张「大/小/同/异/是/非」六对范畴互为条件。彭蒙著《彭蒙子》：「坚/白/同/异/离/合/动/止/新/故/始/终」十二范畴，破「公孙龙白马非马/惠施十事」僵局，确立「坚/白」属性、「马」实体，「坚白」关系，「同/异」过程四维本体论。田骈著《田子》：「大/小/多/少/长/短/方/圆/平/直/重/轻」十二范畴，建「量/质/关/度」四维度量分类学，主张「物无非大/物无非小/物无非多/物无非少」量无绝对。三子并列稷下，与公孙龙/惠施/慎到/环渊并称「稷下八大」，其「概念澄清/分类构建/辩论标准化/逻辑工程化」四重工程，成中国古代逻辑学/概念工程/分类学奠基工程，影响张载/朱熹/王阳明/戴震/段玉裁/钱大昕/章学诚/严复/胡适/冯友兰逻辑思想全版图。",
        "case_en": "Yin Wen/Peng Meng/Tian Bian (350-280 BCE), Qi/Song/Zhao natives, Jixia Academy scholars. Yin Wen authored Yinshi: 'thing/category/same/different/is/not/can/not/know/unknow/debate/not-debate' twelve categories, building 'concept/proposition/reasoning/debate' logic framework, proposing 'large/small/same/different/is/not' six pairs mutually conditional. Peng Meng authored Pengmengzi: 'hard/white/same/different/separate/combine/move/stop/new/old/begin/end' twelve categories, breaking 'Gongsun Long white horse not horse/Hui Shi ten matters' deadlock, establishing 'hard/white' attribute, 'horse' entity, 'hard-white' relation, 'same/different' process four-dimensional ontology. Tian Bian authored Tianzi: 'large/small/many/few/long/short/square/round/flat/straight/heavy/light' twelve categories, building 'quantity/quality/relation/degree' four-dimensional measurement taxonomy, proposing 'no thing not large/no thing not small/no thing not many/no thing not few' quantity non-absolute. Three scholars at Jixia, alongside Gongsun Long/Hui Shi/Shen Dao/Huan Yuan as 'Jixia Eight', their 'concept clarification/taxonomy construction/debate standardization/logic engineering' quadruple project became Chinese ancient logic/concept engineering/taxonomy foundational project, influencing Zhang Zai/Zhu Xi/Wang Yangming/Dai Zhen/Duan Yucai/Qian Daxin/Zhang Xuecheng/Yan Fu/Hu Shi/Feng Youlan logic thought entire landscape."
    },
    # ============ 女性人物 (4) ============
    {
        "code": "H-CWJ-163",
        "name_zh": "蔡文姬：汉末女史/胡笳十八拍/文献学/书法/女性文化传承/悲剧美学大师",
        "name_en": "Cai Wenji: Late Han Female Scholar/Hujia Shibapai/Bibliography/Calligraphy/Female Cultural Transmission/Tragic Aesthetics Master",
        "description_zh": "胡笳十八拍/文献学/书法/女性文化传承/悲剧美学/曹操/董祀/卫氏/归汉",
        "description_en": "Hujia Shibapai/Bibliography/Calligraphy/Female Cultural Transmission/Tragic Aesthetics/Cao Cao/Dong Si/Wei Shi/Return to Han",
        "modes": [25, 37, 28, 35, 38],
        "reason_zh": "核心思维：在「汉末战乱、典籍散佚、女性无书可读、文化断层」背景下，以「记忆复原/文化传承/悲剧升华/女性自我建构」四重工程——背诵《后汉书》等四百余卷典籍，为曹操复原《后汉书》失传篇目，成中国最早「口述史/记忆复原」文献学范式；作《胡笳十八拍》十八首，以「单于/汉地/生离/死别/母子/夫妻/归汉/思乡」八大母题，将「生离死别/文化认同/性别创伤/民族融合」四重创伤升华为悲剧美学经典；作《悲愤诗》五言，以「生死/存亡/忠孝/节义」四大伦理张力，完成女性从「才女/妻妾/俘虏/归汉」四重身份的自我重构。其「记忆复原/文化传承/悲剧升华/女性自我建构」四重工程，成中国女性文化传承/文献学/悲剧美学三位一体奠基范式。",
        "reason_en": "Core Thinking: In 'late Han warfare, scattered classics, women without books, cultural rupture', engineered 'memory restoration/cultural transmission/tragedy sublimation/female self-construction' quadruple project — recited 400+ volumes of Hou Han Shu from memory, restored lost chapters for Cao Cao, becoming China's earliest 'oral history/memory restoration' bibliography paradigm; composed 18-movement Hujia Shibapai with 'Chanyu/Han territory/life-death separation/mother-son/husband-wife/return to Han/homesickness' eight themes, sublimating 'life-death separation/cultural identity/gender trauma/ethnic fusion' quadruple trauma into tragic aesthetic classic; composed Five-Character Bei Fen Shi with 'life-death/survival/loyalty-filial piety/chastity' four ethical tensions, completing female self-reconstruction from 'talented woman/wife-concubine/captive/returnee' quadruple identity. Her 'memory restoration/cultural transmission/tragedy sublimation/female self-construction' quadruple project became Chinese female cultural transmission/bibliography/tragic aesthetics trinity foundational paradigm.",
        "steps_zh": [
            "第1步：抽象归纳法——从记忆中提炼《后汉书》四百余卷框架，建「记忆复原/口述记录/版本校勘」文献学方法模板",
            "第2步：摸石头过河/实验主义——作《胡笳十八拍》十八首，以「单于/汉地/生离/死别/母子/夫妻/归汉/思乡」八母题，以亲历验证悲剧美学可行性",
            "第3步：知行合一/致良知——以《悲愤诗》完成女性从「才女/妻妾/俘虏/归汉」四重身份自我重构",
            "第4步：制度化制衡——推动《胡笳十八拍/悲愤诗/归田赋》纳入「乐府/诗集/文集」三大文本体系，以文本固化女性文化传承",
            "第5步：总体性思维——将「记忆复原/文化传承/悲剧升华/女性自我建构」四系统耦合，成中国女性文献学/文化传承/悲剧美学三位一体奠基范式"
        ],
        "steps_en": [
            "Step 1: Abstract Induction — Extract Hou Han Shu 400+ volumes framework from memory, building 'memory restoration/oral recording/version collation' bibliography methodology template",
            "Step 2: Crossing River by Feeling Stones — Composed 18-movement Hujia Shibapai with 'Chanyu/Han/life-death separation/mother-son/husband-wife/return to Han/homesickness' eight themes, validating tragic aesthetics feasibility with lived experience",
            "Step 3: Unity of Knowledge and Action — Completed female self-reconstruction from 'talented woman/wife-concubine/captive/returnee' quadruple identity via Five-Character Bei Fen Shi",
            "Step 4: Institutional Checks — Promoted Hujia Shibabei/Bei Fen Shi/Gui Tian Fu into 'Yuefu/Poetry Collections/Anthologies' three text systems, solidifying female cultural transmission via texts",
            "Step 5: Systems Thinking — Coupled 'memory restoration/cultural transmission/tragedy sublimation/female self-construction' four systems into Chinese female bibliography/cultural transmission/tragic aesthetics trinity foundational paradigm"
        ],
        "expected_zh": [
            "背诵《后汉书》四百余卷，为曹操复原失传篇目，成中国最早「口述史/记忆复原」文献学范式",
            "《胡笳十八拍》十八首，八大母题升华「生离死别/文化认同/性别创伤/民族融合」四重创伤",
            "《悲愤诗》完成女性从「才女/妻妾/俘虏/归汉」四重身份自我重构",
            "成中国女性文化传承/文献学/悲剧美学三位一体奠基范式"
        ],
        "expected_en": [
            "Recited 400+ volumes Hou Han Shu from memory, restored lost chapters for Cao Cao, China's earliest 'oral history/memory restoration' bibliography paradigm",
            "Hujia Shibapai 18 movements, eight themes sublimating 'life-death separation/cultural identity/gender trauma/ethnic fusion' quadruple trauma",
            "Bei Fen Shi completed female self-reconstruction from 'talented woman/wife-concubine/captive/returnee' quadruple identity",
            "Became Chinese female cultural transmission/bibliography/tragic aesthetics trinity foundational paradigm"
        ],
        "case_zh": "蔡文姬（177-？），陈留圉人，蔡邕女，博学多才，善书法/数学/天文/音律。建安中匈奴南下，文姬被掳北地，嫁左贤王生二子。曹操统一北方后，重金赎回，嫁董祀。曹操问：「闻君家旧藏书四百余卷，今尚存几何？」文姬曰：「昔亡乱，不复记忆，唯有《后汉书》四百余卷，今为君诵之。」为曹操口诵复原《后汉书》失传篇目，成中国最早记忆复原文献学范式。作《胡笳十八拍》十八首：「单于/汉地/生离/死别/母子/夫妻/归汉/思乡」八大母题，以「单调/重复/递进/高潮」十八拍结构，写尽「生离死别/文化认同/性别创伤/民族融合」四重创伤。作《悲愤诗》五言：「生死/存亡/忠孝/节义」四大伦理张力，完成女性从「才女/妻妾/俘虏/归汉」四重身份自我重构。成中国女性文化传承/文献学/悲剧美学三位一体奠基范式。",
        "case_en": "Cai Wenji (177-?), Chenliu Yu native, Cai Yong daughter, broad learning, skilled calligraphy/mathematics/astronomy/music. Jian'an period Xiongnu southward, Wenji captured north, married Left Virtuous King bore two sons. Cao Cao unified north, ransomed back, married Dong Si. Cao Cao asked: 'Heard your family stored 400+ volumes, how many remain?' Wenji replied: 'Lost in chaos, only remember Hou Han Shu 400+ volumes, will recite for you.' Recited Hou Han Shu 400+ volumes from memory, restored lost chapters for Cao Cao, China's earliest memory restoration bibliography paradigm. Composed Hujia Shibapai 18 movements: 'Chanyu/Han/life-death separation/mother-son/husband-wife/return to Han/homesickness' eight themes, with 'monotone/repetition/progression/climax' 18-beat structure, writing 'life-death separation/cultural identity/gender trauma/ethnic fusion' quadruple trauma. Composed Five-Character Bei Fen Shi: 'life-death/survival/loyalty-filial piety/chastity' four ethical tensions, completing female self-reconstruction from 'talented woman/wife-concubine/captive/returnee' quadruple identity. Became Chinese female cultural transmission/bibliography/tragic aesthetics trinity foundational paradigm."
    },
    {
        "code": "H-SGB-164",
        "name_zh": "上官婉儿：唐代女宰相/宫廷文学/制诰/书法/女性政治参与/文治政治桥梁",
        "name_en": "Shangguan Wan'er: Tang Female Chancellor/Palace Literature/Edicts/Calligraphy/Female Political Participation/Literary-Political Bridge",
        "description_zh": "女宰相/宫廷文学/制诰/书法/女性政治/唐中宗/韦后/李隆基/制诰体/婉约派",
        "description_en": "Female Chancellor/Palace Literature/Edicts/Calligraphy/Female Politics/Emperor Zhongzong/Empress Wei/Li Longji/Edict Style/Wanyue School",
        "modes": [33, 20, 28, 34, 35],
        "reason_zh": "核心思维：在「武周/唐初权力更迭、女性禁从政、宫廷文学宦官垄断」背景下，以「文学入政/制诰标准化/女性政治合法化/文治桥梁」四重工程——武则天赏识，入宫为「才人」，掌「制诰/批奏/宫廷文学」三大权柄，成中国首位「女宰相」实质权力者；创「制诰体」标准化：以「典故/辞藻/格律/用典」四维标准，将「诏/制/敕/诰/敕/表/启/疏/状/奏」十大公文标准化，成唐代公文规范范本；推「婉约派」宫廷文学，以「柔美/含蓄/典雅/深情」四美学范畴，打破「宦官/外戚/权臣」文学垄断，为李白/杜甫/王维等盛唐诗坛铺路；辅佐中宗/韦后/睿宗/玄宗四朝，以「文治/制诰/批奏/宫廷文学」四重身份，完成女性从「才人/女官/女相/文人」四重身份跃迁。其「文学入政/公文标准化/女性政治合法化/文治桥梁」四重工程，成中国女性政治参与/公文标准化/宫廷文学三位一体奠基范式。",
        "reason_en": "Core Thinking: In 'Wu Zhou/Tang power transition, women banned from politics, palace literature eunuch monopolized', engineered 'literature into politics/edict standardization/female political legitimization/literary-political bridge' quadruple project — Wu Zetian favored, entered palace as 'Cairen', controlled 'edicts/memorial review/palace literature' three powers, becoming China's first substantive 'female chancellor'; created 'Edict Style' standardization: 'allusion/literary grace/metrics/allusion usage' four-dimensional standard, standardizing 'edict/decree/imperial order/grant/imperial edict/memorial/letter/petition/statement/memorial' ten official document types, becoming Tang official document paradigm; promoted 'Wanyue School' palace literature with 'gentle/subtle/elegant/deep' four aesthetic categories, breaking 'eunuch/relatives/powerful ministers' literature monopoly, paving way for Li Bai/Du Fu/Wang Wei High Tang poetry; assisted Zhongzong/Wei Empress/Ruizong/Xuanzong four reigns, achieving 'Cairen/female official/female chancellor/literati' quadruple identity leap. Her 'literature into politics/document standardization/female political legitimization/literary-political bridge' quadruple project became Chinese female political participation/document standardization/palace literature trinity foundational paradigm.",
        "steps_zh": [
            "第1步：格局授权思维——以「才人/女官/女相」三级授权跃迁，获取政治合法性与文学解释权",
            "第2步：摸石头过河/实验主义——创「制诰体」标准化：以「典故/辞藻/格律/用典」四维标准，十大公文标准化",
            "第3步：制度化制衡——推「婉约派」宫廷文学，以「柔美/含蓄/典雅/深情」四美学范畴，打破垄断",
            "第4步：摸石头过河/实验主义——辅佐中宗/韦后/睿宗/玄宗四朝，以「文治/制诰/批奏/宫廷文学」四重身份验证女性政治可行性",
            "第5步：总体性思维——将「文学/政治/公文/女性/宫廷」五系统耦合，成中国女性政治/公文标准化/宫廷文学三位一体奠基范式"
        ],
        "steps_en": [
            "Step 1: Authority Delegation — Three-level authorization leap 'Cairen/female official/female chancellor', securing political legitimacy and literary interpretive authority",
            "Step