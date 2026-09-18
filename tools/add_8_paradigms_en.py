import json

# Load existing scenarios
with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    scenarios_en = json.load(f)

# 8 unique thinking paradigm figures - English
new_en = {
    "H-SHY-40": {
        "name": "Sang Hongyang: Founder of State Fiscal Macroeconomic Regulation",
        "description": "Equal Transport Price Stabilization / State Monopolies / Asset Tax / Monetary Policy / Price Stability",
        "modes": [19, 20, 29, 28, 34],
        "reason": "Sang Hongyang 'agriculture as root, commerce as branch' yet went against convention. Core mindset: state monopoly capitalism fiscal macro-control — created Equal Transport Price Stabilization (state purchase/sale stabilizing prices), state monopolies on salt/iron/alcohol (high-profit industries), Suanminqian asset/capital gains tax precursor, cast Wuzhu coins unifying currency. Used 'commercial profit' to supplement 'agricultural root', used 'Suanmin' to suppress annexation, built China's most complete state fiscal regulation system.",
        "steps": [
            "Step 1: Marginal Thinking — Suanminqian: taxed merchants/artisans/lenders assets, 'Suanmin' as capital gains tax prototype, suppressed disorderly capital expansion",
            "Step 2: Game Theory — Equal Transport Price Stabilization: Equalization officials buy/store/sell, accumulate in harvest, release in famine, gaming with merchants to stabilize prices/benefit state/benefit people",
            "Step 3: Institutional Checks — State Monopolies: salt/iron/alcohol state-operated, monopoly revenue direct to central, bypassing local separatism, financial power centralized",
            "Step 4: Feedback Loops — Price Stability Mechanism: monitor grain/price fluctuations, dynamically adjust purchase/release rhythm, forming negative feedback stabilization system",
            "Step 5: Strategic Delegation — Professional Division: Sang as Grand Agricultural/Finance Minister, dedicated to finance, not military/politics, professionals doing professional work"
        ],
        "expected": [
            "Emperor Wu reign fiscally abundant, supported massive wars/territorial expansion",
            "Equal Transport/State Monopolies/Suanminqian became standard fiscal policies for dynasties",
            "Lessons: over-monopoly stifled private vitality, state-commerce imbalance triggered rebellions, fiscal dependence on monopoly profits unsustainable"
        ],
        "case": "Equal Transport (110 BC): Equalization officials in Chang'an/prefectures, buy high when prices low, sell low when prices high, stabilized prices, cracked hoarding. State Monopolies: salt pools/iron mountains state-owned, monopoly revenue direct to Grand Agricultural Treasury, annual huge revenue. Suanminqian (115 BC): ordered people self-report assets, merchants self-declare capital, 2% tax rate, under-reporting confiscated half to county. Cast Wuzhu: unified currency, banned private minting, facilitated circulation. Result: state fiscally rich, supported Wei Qing/Huo Qubing north campaigns, Zhang Qian opened Western Regions."
    },
    "H-SMG-41": {
        "name": "Sima Guang: Master of History-Based Governance",
        "description": "Comprehensive Mirror for Aid in Government / History as Mirror / Past as Lesson / Conservative Reform / Gentleman vs Petty Person Theory",
        "modes": [22, 7, 1, 28, 35],
        "reason": "Sima Guang 'learn from past events, resource for governance'. Core mindset: historical analogy decision-making and conservative reformism — compiled 'Comprehensive Mirror for Aid in Government' over 19 years, 294 volumes, 3M characters, 'events as warp, years as weft', providing historical analogy library for decisions with 'past as lesson'. Advocated 'follow ancestors, keep established constitutions', opposed Wang Anshi radical reform, proposed 'gentlemen love with virtue, petty persons love with indulgence' personnel philosophy. History as mirror, prevent trouble before it sprouts.",
        "steps": [
            "Step 1: Holistic Thinking — Chronological General History: broke biographical figure-limits, time as warp/events as weft, presented political/economic/military/cultural full causal chains",
            "Step 2: Strategic Foresight — History as Mirror: built 'historical scenario-decision-outcome' case library, decision-making retrieves similar historical scenarios, avoids repeating mistakes",
            "Step 3: Contradiction Analysis — Gentleman vs Petty Person: identify 'gentlemen love with virtue, petty persons love with indulgence', employ by virtue-first/talent-second, prevent petty persons using reform for private gain",
            "Step 4: Gradual Reform — Conservative Reform: 'follow ancestors, keep established constitutions', oppose radical reform, advocate 'none who rush succeed', micro-adjust within existing framework",
            "Step 5: Dormant Accumulation — Luoyang Faction/Memorials: during Xining Reform submitted 'Request to Abolish Three Departments Conditions Bureau' five times ignored, retired to Luoyang 15 years wrote 'Comprehensive Mirror for Aid in Government', influenced posterity through writing"
        ],
        "expected": [
            "'Comprehensive Mirror for Aid in Government' became must-read for emperors/ministers, influenced Song/Yuan/Ming/Qing/Republic decision-makers",
            "History as mirror became core gene of Chinese decision culture, case teaching method ancestor",
            "Lessons: conservatism misjudged reform necessity, hindered institutional innovation, ultimately failed to save Northern Song collapse"
        ],
        "case": "Zizhi Tongjian compilation (1065-1084): Sima Guang petitioned Shenzong 'take former sages deeds... compile into book', granted title 'Zizhi Tongjian'. Recruited Liu Ban/Liu Shu/Fan Zuyu etc to assist, verified differences/corrected errors, abridged complexity. Used 'chronological' format, 'summary' headings, 'textual criticism' corrected errors. Personnel philosophy: 'talent/wisdom complete = sage, talent/wisdom half = gentleman, talent more wisdom less = fool, talent less wisdom more = petty person'. Opposed New Policies: submitted 'Request to Abolish Three Departments Conditions Bureau' five times, argued New Policies 'disturb people, harm state, invite chaos'. Result: though couldn't stop New Policies, 'Tongjian' became millennial history/decision classic."
    },
    "H-GYW-42": {
        "name": "Gu Yanwu: Giant of Practical Statecraft Learning",
        "description": "Practical Statecraft / Every Man's Duty / Evidential Scholarship / Perished State / Prefectures Govern / Practical Statecraft",
        "modes": [5, 22, 25, 28, 35],
        "reason": "Gu Yanwu 'preserving the world is the responsibility of even the humblest commoner'. Core mindset: unity of evidential scholarship and patriotic action — after Ming fell to Qing, lived in seclusion writing, authored 'Record of Daily Knowledge' 32 vols, 'Prefectures Govern' criticizing centralization evils. Proposed 'perished state vs perished world', 'prefectures govern the world' decentralization advocacy. Evidential scholarship: phonology/exegesis/geography/institutions/epigraphy/numismatics, 'investigate credible history, distinguish forged books, correct errors'. Practical learning: 'Six Classics annotate me, I annotate Six Classics', 'seek practical utility, not empty fame'.",
        "steps": [
            "Step 1: Seek Truth from Facts — Evidential Empiricism: phonology/exegesis/geography/institutions/epigraphy/numismatics/editions, 'broadly observe, selectively take; deeply accumulate, thinly release', evidence speaks",
            "Step 2: Holistic Thinking — Prefectures Govern System: criticized Qin-onward prefecture system 'world as one family, whole world serving one person', advocated 'prefectures govern the world', decentralization",
            "Step 3: Systems Thinking — Perished State vs Perished World Distinction: 'perished state' = dynasty change, 'perished world' = order collapse, 'preserving world is responsibility of even humblest commoner', clarified responsibility levels",
            "Step 4: Natural Selection — Practical Statecraft: 'Six Classics annotate me, I annotate Six Classics', learning must solve real problems (water conservancy/salt law/military system/grain transport/taxation), reject empty nature/moral talk",
            "Step 5: Dormant Accumulation — Secluded Authorship: after Ming fell, never served Qing, footsteps covered half China, authored 'Record of Daily Knowledge' 32 vols, 'Prefectures Govern', 'World Prefectures Benefits and Harms', 'Five Books on Phonology' etc massive works"
        ],
        "expected": [
            "'Record of Daily Knowledge' became Qing evidential scholarship/practical learning peak, influenced Qian-Jia School/late Qing New Learning",
            "'Prefectures Govern' thought influenced late Qing/Republic local self-governance/modern federalism concepts",
            "Lessons: evidential scholarship excessive easily trivial, political proposals not adopted, Ming-Qing transition scholar-official collective martyrdom"
        ],
        "case": "'Record of Daily Knowledge' compilation (1630s-1682): Gu Yanwu after Ming fall footsteps covered North China/Jiangnan/Guanzhong, recorded observations/readings as essays, 32 vols, 1000+ entries. Covered phonology/exegesis/geography/institutions/epigraphy/agriculture/military/grain transport/taxation/calendar. 'Prefectures Govern': argued Qin-onward prefecture system evils, advocated 'prefectures govern the world', decentralization. Phonology: ancient no tones, medieval has tones, divided 36 initials, built rhyme charts. Result: Qian-Jia School (Dai Zhen/Duan Yucai/Wang Niansun/Wang Yinzhi) inherited evidential method, Tan Sitong/Liang Qichao/Zhang Taiyan inherited patriotic spirit, became modern practical learning/revolutionary thought dual source."
    },
    "H-SB-43": {
        "name": "Shen Kuo: Dream Pool Essays Scientific Empiricism Polymath",
        "description": "Dream Pool Essays / Empirical Science / Polymath / Falsifiable / Knowledge Management",
        "modes": [25, 24, 29, 28, 35],
        "reason": "Shen Kuo 'principle exhaustively investigated, matter exhaustively studied'. Core mindset: pre-modern scientific empiricism culmination — authored 'Dream Pool Essays' 26 vols, 609 entries, covering astronomy/geography/physics/chemistry/biology/medicine/math/engineering/military/humanities/arts. Advocated 'principle exhaustively investigated, matter exhaustively studied, know not only what but why', falsifiable, reproducible, heavy on measurement, light on speculation. Discovered magnetic declination/petroleum/movable type printing/geological structure/climate change/relative humidity measurement, built knowledge classification/indexing/retrieval system.",
        "steps": [
            "Step 1: Abstract Induction — Empirical Observation: personally measured magnetic needle declination/measured mountain heights/investigated strata/observed solar eclipse/experimented movable type printing/collected fossils/recorded meteorology, data-based",
            "Step 2: Systems Thinking — Knowledge Classification System: divided 609 notes into 17 categories (astronomy/geography/physics/chemistry/medicine/math/engineering/military/arts etc), built index/cross-references",
            "Step 3: Punctuated Equilibrium — Scientific Discovery Pattern: long accumulation (observation/recording/experiment) -> sudden insight (magnetic declination/petroleum origin/geological change) -> new theory established",
            "Step 4: Feedback Loops — Knowledge Management: built note classification/index/cross-references/searchable system, 'Dream Pool Essays' became pre-modern knowledge base model",
            "Step 5: Dormant Accumulation — Frontier Practice: Xihe fortification/Yongle city tuntian/Liao River fortification/hydrological survey/military maps, converted scientific knowledge into engineering effectiveness"
        ],
        "expected": [
            "'Dream Pool Essays' became Chinese science history peak, led Europe by centuries (magnetic declination/movable type/petroleum/geological structure)",
            "Empirical scientific method/knowledge classification management/cross-disciplinary integration became modern science/knowledge management precursor",
            "Lessons: technology not institutionalized/not systematized/not converted to productivity, Song fall cut off scientific tradition"
        ],
        "case": "Magnetic Declination Discovery (1088): Shen Kuo recorded in 'Dream Pool Essays' 'magnet points south, not due south, always eastward deviation', through extensive measurement discovered magnetic needle deviates east, 400+ years before Europe. Movable Type Printing (1041-1048): saw Bi Sheng carve clay chars, fire into movable types, typeset printing, reusable, recorded full process. Petroleum Discovery: Yan'an/Fu Yan underground 'water like lacquer, burns very bright', predicted 'later generations must use this for lamps'. Geological Structure: observed Taihang fossils/sea shells, deduced 'this place was once seashore'. Movable type/magnetic declination/petroleum/geological structure all centuries before Europe."
    },
    "H-LZX-44": {
        "name": "Lin Zexu: Opening Eyes to See the World Crisis Diplomat",
        "description": "Humen Opium Destruction / Opening Eyes to See World / Practical Diplomacy / Coastal Defense Planning / Practical Learning Saves Nation",
        "modes": [1, 5, 11, 28, 35],
        "reason": "Lin Zexu 'if it benefits the nation, I'll risk life and death, how can I avoid disaster or seek fortune'. Core mindset: crisis diplomacy and practical learning saving nation with eyes open to world — Imperial Commissioner Humen destroyed opium 2.37M kg, built coastal defense/formed navy/trained artillerymen/translated foreign languages/compiled 'Four Continents Record'/translated 'Complete Map of Great Britain'/compiled 'Chinese Law Compilation'. 'Learn barbarian skills to control barbarians', 'open eyes to see world', 'practical learning saves nation'. Practical attitude facing Western shock: opium ban/coastal defense/diplomacy/translation/law/tech simultaneous push. Though Daoguang compromised and exiled, left 'open eyes to see world' eternal lesson.",
        "steps": [
            "Step 1: Contradiction Analysis — Humen Opium Destruction: identified opium as principal contradiction, 23 days destroyed 2.37M kg opium, established strict prohibition, unyielding",
            "Step 2: Seek Truth from Facts — Open Eyes to See World: ordered translation of 'Complete Map of Great Britain', 'Four Continents Record', 'Chinese Law Compilation', 'International Law', 'Learn barbarian skills to control barbarians', shattered 'Celestial Empire' illusion",
            "Step 3: Institutional Checks — Coastal Defense System: coastal forts/warships/naval training/artillery/military telegraph/sea charts/sailor training, built modern coastal defense embryo",
            "Step 4: Flexible Strategy — Practical Diplomacy: mastered international law/treaty law/territorial waters/consular jurisdiction, negotiated with Elliot/Pottinger, defended sovereignty bottom line",
            "Step 5: Dormant Accumulation — Ili Tuntian: exiled to Xinjiang Ili, developed water conservancy/planted forests/established schools/dug canals/wrote 'Ili Notes', late life still concerned coastal defense"
        ],
        "expected": [
            "Humen Opium Destruction became modern China anti-imperialism starting point, 'open eyes to see world' became modern enlightenment core proposition",
            "Coastal defense/translation/international law/customs/postal/telegraph modern institutions embryonic form",
            "Lessons: individual cannot reverse decline alone, court compromised/sold out, personal tragedy reflects institutional deadlock"
        ],
        "case": "Humen Opium Destruction (1839): Lin Zexu imperial commissioner Guangdong, seized opium merchants, forced surrender 20,283 chests, 2.37M kg, Humen beach dug pools, lime/salt decomposition, 23 days completed destruction. Translation: established Four Directions Hall translating 'Complete Map of Great Britain', 'Four Continents Record', 'International Law', 'International Law', 'Chinese Law Compilation', 'open eyes to see world'. Coastal Defense: Guangdong/Fujian/Zhejiang/Jiangsu/Shandong coastal forts/warships/artillery/translated arms books. Ili Tuntian: exiled, developed water/forests/schools/canals/wrote 'Ili Notes'. Result: though exiled, left 'if it benefits the nation, I'll risk life and death' eternal lesson."
    },
    "H-BC-45": {
        "name": "Ban Chao: Silk Road Operator Who Ruled Many with Few",
        "description": "Threw Pen for Sword / Ruled Many with Few / Silk Road Operation / Used Barbarians to Control Barbarians / Cut Off Northern Xiongnu",
        "modes": [4, 23, 11, 28, 35],
        "reason": "Ban Chao 'a real man has no other ambition, establish merit in foreign lands, to gain marquis title'. Core mindset: asymmetric infiltration and cultural soft power frontier governance — threw pen for sword, 36 men to Western Regions, cut off Northern Xiongnu Western Regions links, ruled many with few (36 men took 50+ states: Shule/Yutian/Suoche/Shule/Qiuci/Yanqi/Wensu etc), 'used barbarians to control barbarians', opened Silk Road/protected merchants/established Protector General/tuntian garrisoned, 'not love death, to repay state'. 31 years operating Western Regions, 'Han banner flew again, Western Regions震服', enfeoffed Dingyuan Marquis.",
        "steps": [
            "Step 1: Encircle Cities from Countryside — Smart Capture of Shule: Ban Chao led 36 men night raid Xiongnu envoys, beheaded presented to Protector, Western Regions震动, Shule returned to Han",
            "Step 2: Natural Selection — Ruled Many with Few: facing Qiuci/Yanqi/Weitou allied tens of thousands, Ban Chao 'strike unexpectedly, attack unprepared', night raid Yanqi, fire burned Qiuci, won with fewer",
            "Step 3: United Front — Used Barbarians to Control Barbarians: recruited Western Regions states soldiers, formed 'Western Regions Righteous Army', Western Regions people govern Western Regions, reduced Han troop burden, built lasting rule",
            "Step 4: Flexible Strategy — Cut Off Northern Xiongnu: beheaded Northern Xiongnu envoys, burned their supplies, cut off Northern Xiongnu right arm in Western Regions, forced Northern Xiongnu flee far, Western Regions situation reversed",
            "Step 5: Institutional Checks — Protector General System: established Western Regions Protector/Deputy Protector/Interpreter Chief/Sima/Qin Hou, tuntian garrisoned/protected commerce/document exchange, built lasting administrative system"
        ],
        "expected": [
            "36 men operated Western Regions 31 years, 50+ states submitted, Silk Road open, Han banner flew again Western Regions",
            "Protector General/tuntia/Colonel/Interpreter became Western Regions governance standard model, influenced Tang/Qing Western Regions governance",
            "Lessons: over-reliance on personal charisma, Ban Yong death led Western Regions chaos again, needs institutionalized succession"
        ],
        "case": "Ban Chao Smart Capture Shule (73): Ban Chao led 36 men to Western Regions, Shule King under Xiongnu coercion killed Han envoy. Ban Chao 'not enter tiger den, how get tiger cub', night led strong men beheaded Xiongnu envoy head presented to Shule King, Shule震服 returned to Han. Yutian Siege (80): Ban Chao led 20k Western Regions troops besieged Yutian, Qiuci/Wensu/Weitou relief tens of thousands arrived. Ban Chao 'strike unexpectedly' night raid Yanqi, fire burned Qiuci. Cut Off Northern Xiongnu: beheaded Northern Xiongnu envoys, burned their supplies, Northern Xiongnu lost Western Regions right arm fled far. 97 AD Ban Chao sent Gan Ying reach Daqin (Rome), Silk Road reached Mediterranean. Enfeoffed Dingyuan Marquis."
    },
    "H-SD-46": {
        "name": "Su Shi: Aesthetic Resilience Prime Minister of People-Oriented Literati",
        "description": "People's Livelihood Concern / Aesthetic Life / Pressure Resistance Psychology / Literati Politics / Know Self Know Others",
        "modes": [5, 27, 21, 28, 35],
        "reason": "Su Shi 'people have joys and sorrows, moon waxes and wanes'. Core mindset: aesthetic resilience and people-oriented concern literati political wisdom — three exiles three returns (Huangzhou/Huizhou/Danzhou), 'belly full of untimeliness' yet 'heart at peace'. Huangzhou farmed/wrote Red Cliff Rhapsody/Hanshi Tie/created Dongpo Pork/wrote 'Ding Feng Bo' 'chilly spring wind sobers wine, slight cold mountain slanting sun greets'. Huizhou 'daily eat 300 lychees, not refuse long be Lingnan man'. Danzhou 'nine deaths southern wilds I do not regret', built water conservancy/ran schools/treated commoners. 'Wrote to revive eight generations decline', 'writings eternal matter, gain loss inch heart knows'. Aesthetic against suffering, people-oriented against power, humor dissolving suffering.",
        "steps": [
            "Step 1: Framing Effect — Restructure Suffering: 'life everywhere what like, should resemble flying swan stepping snow mud', 'bamboo staff straw sandals light win horse, who fears, one straw raincoat misty rain roam freely', exile restructured as travel, poverty restructured as elegance",
            "Step 2: Unity of Knowledge and Action — People-Oriented Practice: Huangzhou built Dongpo/farmed/saved starving, Huizhou built schools/medical/drought relief, Danzhou built water conservancy/ran schools/treated commoners",
            "Step 3: Wu Wei — Aesthetic Life: 'life knowing words worry begins', 'daily eat 300 lychees, not refuse long be Lingnan man', constructed spiritual fortress with poetry/calligraphy/food/gardens/tea",
            "Step 4: Cognitive Bias Identification — Know Self Know Others: 'writings eternal matter, gain loss inch heart knows', saw through power game essence, not follow waves/not flatter, maintain true self",
            "Step 5: Dormant Accumulation — Three Exiles Three Returns: each exile became creative peak/people's livelihood practice peak, 'nine deaths southern wilds I do not regret', with life-death heart achieved eternal writer/honest official/good doctor"
        ],
        "expected": [
            "Poetry/prose/calligraphy/painting/food/gardens became Chinese aesthetic culture peak, influenced Song/Yuan/Ming/Qing/modern",
            "'Dongpo Culture' became pressure resistance psychology/aesthetic life/people-oriented sentiment trinity exemplar",
            "Lessons: literati politics fragile before power, reformers cannot escape faction struggle fate, late years lonely"
        ],
        "case": "Wutai Poetry Case (1079): Su Shi imprisoned for poetry 'recklessly discussing state affairs', nearly died, exiled Huangzhou. Huangzhou (1080-1086): farmed/wrote Red Cliff Rhapsody前后/Hanshi Tie/created Dongpo Pork/wrote 'Ding Feng Bo chilly spring wind sobers wine'. Huizhou (1094-1097): 'daily eat 300 lychees, not refuse long be Lingnan man', wrote 'Chaoran Tai Ji'. Danzhou (1097-1100): 'nine deaths southern wilds I do not regret', built water conservancy/ran schools/treated commoners/wrote 'Hainanzi'. Reinstated (1100): Huizong ascended recalled, died at Changzhou. Throughout used poetry/food/gardens/medical/education against suffering, became 'Dongpo Culture' eternal."
    },
    "H-ZXC-47": {
        "name": "Zhang Xuecheng: Master of Theoretical Self-Awareness in Historiography",
        "description": "General Principles of Literature and History / All Classics Are History / Historiography Theory / Metacognition / Methodological Self-Awareness",
        "modes": [22, 25, 29, 28, 35],
        "reason": "Zhang Xuecheng 'All Classics Are History', 'History is that which carries the Way'. Core mindset: theoretical self-awareness and metacognitive breakthrough in historiography — authored 'General Principles of Literature and History' Inner/Outer/Misc chapters, proposed 'All Classics Are History' (classics essentially historical documents), 'Three Meanings of Historiography' (carry Way/resolve doubts/preserve past know future), 'Three Virtues of Historians' (virtue/talent/insight), 'Ancient and Modern Different Systems' (historical change/institutional evolution/suit time). Built historiography methodology system: source criticism/historical argument/historical interpretation/historiography procedures. 'Understand ancient-present change, form one school of thought' as historiography highest realm.",
        "steps": [
            "Step 1: Abstract Induction — All Classics Are History: broke 'classics-history dichotomy', argued 'Poetry/Book/Rite/Music/Changes/Spring Autumn' essentially all history books, historical materials, historical records, not abstruse philosophy",
            "Step 2: Systems Thinking — Three Meanings of Historiography: Carry Way (moral/political/institutional core), Resolve Doubts (correct errors/distinguish true-false/clarify right-wrong), Preserve Past Know Future (learn from history/govern by history/Comprehensive Mirror for Aid in Government)",
            "Step 3: Holistic Thinking — Three Virtues of Historians: Historian Virtue (character/benevolence/righteousness/loyalty), Historian Talent (writing/evidential/organizational), Historian Insight (penetration/vision/realm), 'Insight leads Talent, Virtue roots Insight'",
            "Step 4: Thinking Mode Selection — Ancient Modern Different Systems: 'Three generations above, governance from one; three generations below, governance from two', historical periodization/institutional evolution/suit time/eternal no pattern",
            "Step 5: Dormant Accumulation — Late Authorship: after 50 wrote 'General Principles' 10 years, feet not out door, hand not release scroll, 'hand copy heart repay, eyes send spirit travel', dying still hand corrected manuscript"
        ],
        "expected": [
            "'General Principles of Literature and History' became Chinese historiography theory peak, built historiography methodological self-awareness system",
            "'All Classics Are History'/'Three Meanings of Historiography'/'Three Virtues of Historians' became modern historiography/humanities methodology cornerstones",
            "Lessons: unknown in life, recognized posthumously, theory ahead of time, did not directly influence policy"
        ],
        "case": "'General Principles of Literature and History' authorship (1786-1795): Zhang Xuecheng after 50 closed door 10 years wrote 'General Principles' Inner/Outer/Misc three chapters. Inner: Original History/Historical Comprehension/Literature History/All Classics Are History/Three Meanings/Three Virtues/Ancient Modern Different Systems/Historical Method. Outer: Historical Criticism/Figures/Book Catalogs/Schools. Misc: Q&A/Notes/Poetry. Core claims: 'All Classics Are History' breaks classics-history dichotomy; 'Three Meanings' positions historiography function; 'Three Virtues' sets historian standards; 'Ancient Modern Different Systems' establishes historical evolution view. Late years 'hand copy heart repay, eyes send spirit travel', dying still corrected manuscript. Influence: Zhang Xiqing/Liu Yiyun/Qian Daxin/Wang Mingsheng etc Qing historians, modern Liang Qichao/Hu Shi/Fu Sianian/Gu Jiegang etc New Historiography all inherited his theory."
    }
}

# Add to scenarios
scenarios_en.update(new_en)

with open('scenarios_en.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios_en, f, ensure_ascii=False, indent=2)

print(f"Updated scenarios_en.json: {len(scenarios_en)} total scenarios")