import json

# Load existing scenarios
with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    scenarios_en = json.load(f)

# 8 final paradigm figures - English
new_en = {
    "H-GZ-60": {
        "name": "Guan Zhong: Hegemon Maker's State Machine Engineer",
        "description": "Assisted Duke Huan of Qi to Hegemony / Nine Alliances of Lords / Guanzi Light-Heavy Chapters / System Engineering / Incentive Design",
        "modes": [33, 19, 34, 40, 35],
        "reason": "Guan Zhong 'Respected Father', core mindset: systems engineering of hegemonic strategy — assisted Duke Huan of Qi, unified the realm once, nine alliances of lords, without chariots. Authored 'Guanzi' Light-Heavy Chapters, established 'Light-Heavy' economic regulation, 'Tithe Tax' system, 'Govern State by Rites' ritual system, 'Five Households as Xuan' grassroots governance. Transformed hegemony construction into replicable state operation code, became Spring-Autumn Hegemon Maker.",
        "steps": [
            "Step 1: Strategic Delegation — Assisted Duke Huan to Hegemony: 'Guan Zhong as Chancellor, Duke Huan Hegemon', clear ruler-minister division, chancellor power maximized",
            "Step 2: Marginal Thinking — Light-Heavy Regulation: 'Circulate surplus/deficit, stabilize prices, meet state needs', state regulates supply/demand, stabilizes prices",
            "Step 3: Institutional Checks — Grassroots Governance: 'Five households as Xuan, ten Xuan as Li, four Li as Lian, ten Lian as Xiang, ten Xiang as Bi, ten Bi as County', grassroots self-governance network",
            "Step 4: Incentive Mechanism — Clear Rewards Punishments: 'Merit rewarded above, crime punished below', appoint by merit, break aristocratic heredity",
            "Step 5: United Front — Respect King Repel Barbarians: 'Respect Zhou Court, Repel Four Barbarians', cohesion of lords through legitimacy, legitimacy construction"
        ],
        "expected": [
            "Duke Huan hegemony, nine alliances, one unification, institutionalized hegemony",
            "Guanzi Light-Heavy chapters became Chinese economics ancestor, grassroots governance template continued two thousand years",
            "Lessons: Guan Zhong died, Qi chaos, Duke Huan starved, system dependent on worthy minister, lacks self-correction mechanism"
        ],
        "case": "Guan Zhong Assisted Qi (685-645 BC): Duke Huan enthroned, Guan Zhong returned to Qi, three years Qi greatly governed. Light-Heavy: 'State poor then collect, state rich then disperse', state regulates grain/salt/currency prices. Tithe Tax: 'One in ten tax', replaced well-field system. Grassroots governance: Xuan-Li-Lian-Xiang-Bi-County five levels, self-governance/mutual-aid/supervision. Military Merit Rank: battle merit enfeoffment, broke hereditary nobility. Respect King Repel Barbarians: Zhaoling Meeting, Chu King asked about tripod, Duke Huan retreated him by ritual. Result: Qi Hegemon, Lords submit, Qi declined after Guan Zhong death."
    },
    "H-SQ-61": {
        "name": "Sima Qian: Historiography Methodology Founder of Ultimate Heaven-Human",
        "description": "Records of the Grand Historian / Biographical Style / Ultimate Heaven-Human Through Ancient-Modern Changes / Writing in Resentment / Humanistic Narrative",
        "modes": [22, 25, 29, 28, 35],
        "reason": "Sima Qian 'Investigate Heaven-Human boundary, penetrate ancient-present changes, form one school of thought', core mindset: historiographical narrative methodological self-awareness and humanistic concern — created Biographical Style (Basic Annals/Hereditary Houses/Biographies/Treatises/Tables), 'investigate the obscure, probe the profound', 'narrate not create', 'write in resentment'. Maps individual fate onto era changes, establishes historian subjectivity through 'Grand Historian Self-Prefation'.",
        "steps": [
            "Step 1: Abstract Induction — Biographical Style Creation: Basic Annals/Hereditary Houses/Biographies/Treatises/Tables five forms, people-centered, events as threads, breaks chronological limits",
            "Step 2: Systems Thinking — Ultimate Heaven-Human: Investigate Heaven-Human relationship, natural law & social development interaction, historical philosophy dimension",
            "Step 2: Holistic Thinking — Through Ancient Present Changes: Vertical penetrate three thousand years up-down, horizontal encompass politics/economy/culture/military, identify historical evolution laws",
            "Step 3: Thinking Mode Selection — Write in Resentment: 'King Wen confined expanded Zhou Changes, Confucius distressed made Spring Autumn', adversity transforms to creation",
            "Step 4: Thinking Mode Selection — Historian Subjectivity: 'Grand Historian Self-Prefation' establishes historian as active agent not passive recorder"
        ],
        "expected": [
            "'Records of Grand Historian' became Chinese historiography peak, biographical style continued two millennia",
            "'Investigate Heaven-Human'/'Through Ancient Present'/'Form One School' became historiography methodology three realms",
            "Lessons: Castration trauma/individual vs power/historical truth vs political pressure"
        ],
        "case": "Records of Grand Historian (104-91 BC): Li Ling incident, Sima Qian suffered castration, 'not yet completed my work, death not in my heart'. 130 chapters, 520k characters: 12 Basic Annals, 10 Tables, 8 Treatises, 30 Hereditary Houses, 70 Biographies. Biographical style: people as center, events as thread. 'Investigate Heaven-Human, penetrate ancient present, form one school'. Self-preface: 'Investigate Heaven-Human boundary, penetrate ancient present changes, become one school'. Result: Biographical style continued two millennia, 'investigate heaven-human/through ancient present/form one school' became historiography three realms."
    },
    "H-ZX-62": {
        "name": "Zhu Xi: Neo-Confucianism Systematizer of Cognitive Framework",
        "description": "Neo-Confucianism Compendium / Investigate Things Extend Knowledge / Four Books Chapter Annotations / Knowledge System Construction",
        "modes": [22, 25, 18, 28, 35],
        "reason": "Zhu Xi 'Investigate things to extend knowledge, knowledge complete then intention sincere', core mindset: cognitive framework system building and standardization — authored 'Neo-Confucianism Compendium', 'Four Books Chapter Annotations', established 'Investigate Things Extend Knowledge -> Sincere Intention -> Rectify Mind -> Cultivate Self -> Regulate Family -> Govern State -> Pacify World' cognitive chain. 'Investigate Things' as epistemological starting point, 'Extend Knowledge' as cognitive deepening, built complete ontology/epistemology/methodology system. 'Zhu Xi Learning' became imperial examination standard 600+ years.",
        "steps": [
            "Step 1: Abstract Induction — Principle Qi Theory: 'Principle one, manifestations many', 'Qi as vessel, Principle as master', built ontological foundation",
            "Step 2: Systems Thinking — Investigate Things Extend Knowledge: 'Investigate things extend knowledge, knowledge complete then intention sincere', cognitive chain: things->knowledge->intention->mind->self->family->state->world",
            "Step 3: Management by Objectives — Four Books Standardization: 'Great Learning/Doctrine of Mean/Analects/Mencius' chapter annotations, unified thought standard, imperial exam standard 600+ years",
            "Step 4: Thinking Mode Selection — Method of Reading: 'Read thoroughly, think deeply', 'step by step, read thoroughly think deeply', cognitive methodology",
            "Step 5: Dormant Accumulation — Late Year Compilation: 'Reflections on Things at Hand' with Lu Zuqian, 'Zhu Xi Language Classified', 'Song Yuan Learning Cases', knowledge system late-year fixed"
        ],
        "expected": [
            "'Four Books Chapter Annotations' became imperial exam standard 600+ years, 'Zhu Xi Learning' official orthodoxy",
            "Principle Qi/Investigate Things/Cognitive Chain built Chinese philosophy epistemology system",
            "Lessons: System closed/emphasize inner sage neglect outer king/late Ming Wang Yangming 'Mind Learning' rebellion"
        ],
        "case": "Zhu Xi Neo-Confucianism (1130-1200): Zhu Xi youth studied Cheng Brothers Neo-Confucianism, middle age compiled 'Four Books Chapter Annotations', 'Reflections on Things at Hand' with Lu Zuqian, 'Song Yuan Learning Cases'. Principle Qi: 'Principle one manifestations many', 'Qi vessel Principle master'. Investigate Things: 'Investigate things extend knowledge', cognitive chain start. Four Books: Great Learning/Doctrine of Mean/Analects/Mencius chapter annotations, imperial exam standard 1313-1905. Song Yuan Learning Cases: compiled Cheng/Zhu/Zhang/Lu/Ye/Luo etc learning cases. Result: Zhu Xi Learning official orthodoxy 600+ years, Wang Yangming 'Mind Learning' rebellion."
    },
    "H-LZY-63": {
        "name": "Liu Zongyuan: Political Reform Thinker's Critical Writer",
        "description": "Feudalism Discourse / Non-Guo Yu / Refuting Slander / System Critique / Public Policy / Intellectual Liberation",
        "modes": [30, 31, 37, 28, 35],
        "reason": "Liu Zongyuan 'This heart always faces sun, need not watch flowers bloom', core mindset: critical reconstruction and institutional design of political thought — Yongzhen Reform failed exiled to Liuzhou, wrote 'Feudalism Discourse' breaking 'Duke Zhou Rites Music' myth, arguing Commandery-County superior to Feudalism. 'Non Guo Yu' breaks 'Mandate of Heaven' myth, 'Refutation of Slander' defends political innocence. 'Heaven earth no full merit, sages no full ability, all things no full use', relativism/historicism/critical rationalism.",
        "steps": [
            "Step 1: Cognitive Bias Identification — Break Feudal Myth: 'Feudalism Discourse' 'Three generations above, governance from one; three generations below, governance from two', argue Commandery-County superior to Feudalism, systemic critique",
            "Step 2: Framing Effect — Break Mandate Myth: 'Non Guo Yu' 'Heaven produces people, must establish ruler, not for ruler produce people', people-based/contract theory雏形",
            "Step 3: Unity Knowledge Action — Refute Slander Self-Defense: Yongzhen Reform failed, exiled Liuzhou, 'Refutation' point-by-point refute slander, intellectual integrity, scholar dignity",
            "Step 4: Natural Selection — Thought Relativism: 'Heaven earth no full merit, sages no full ability, all things no full use', deny absolute truth/authority/perfection",
            "Step 5: Dormant Accumulation — Liuzhou Governance: Liuzhou Prefect, build water conservancy/schools/treat people/pacify barbarians/'Liu Hedong Collection' transmitted, unity knowledge action"
        ],
        "expected": [
            "'Feudalism Discourse' became Chinese institutional critique classic, 'Refutation of Slander' scholar dignity declaration",
            "Relativism/historicism/critical rationalism became Chinese intellectual liberation source",
            "Lessons: Reform failed/exiled life/late loneliness/thought ahead of time not adopted"
        ],
        "case": "Feudalism Discourse (803): Liu Zongyuan Yongzhen Reform failed exiled Shaozhou, later moved Liuzhou. 'Feudalism Discourse' 'Three generations above, governance from one; three generations below, governance from two', argued Commandery-County superior to Feudalism, broke 'Duke Zhou Rites Music' myth. Non Guo Yu (805): 'Heaven produces people, must establish ruler, not for ruler produce people', people-based/contract theory雏形. Refutation (814): Point-by-point refute 'Liu Zongyuan rebellion/conspiracy with reform party' slander, intellectual integrity. Liuzhou governance: water conservancy/schools/medical/pacify barbarians/'Liu Hedong Collection' transmitted. Result: Institutional critique/people-based thought/relativism became Chinese thought liberation source."
    },
    "H-WFZ-64": {
        "name": "Wang Fuzhi: Historical Cycle Theory Giant of Practical Learning",
        "description": "Chuanshan Legacy / Reading Comprehensive Mirror Treatise / Historical Cyclical Theory / Practical Learning Spirit / Indigenous Modernity",
        "modes": [7, 1, 23, 28, 35],
        "reason": "Wang Fuzhi 'rise and fall follow each other, cycle inevitable', core thinking: Historical Cycle Theory and Practical Learning Indigenous Modernity — Ming fall Qing rise survivor, wrote 'Reading Comprehensive Mirror Treatise' on historical cycles, 'Shipan Legacy' hundred volumes. 'Reading Comprehensive Mirror' 'Governance chaos alternate, cycle inevitable', 'World governance chaos, not governor merit, not chaos person fault, momentum'. 'Shipan Legacy' 'Qi monism', 'Unity Knowledge Action', 'Practical Learning'. Ming fall not serve Qing, hide write, die for will.",
        "steps": [
            "Step 1: Strategic Foresight — Historical Cycle Law: 'Rise and fall alternate, cycle inevitable', identify historical macro/meso/micro cycles, reject linear progress history",
            "Step 2: Contradiction Analysis — Momentum Not Heaven Not Earth Human Made: 'Momentum not heaven, not earth, human made', historical process human shapeable, not fatalism",
            "Step 3: Natural Selection — Six Classics Annotate Me I Annotate Six Classics: 'Six Classics annotate me, I annotate Six Classics', classic interpretation right returns subject, establish subjectivity hermeneutics",
            "Step 4: Abstract Induction — Practical Learning Spirit: 'Govern world not worry people not trust me, worry I cannot trust people', oppose empty nature talk/practical statecraft/practical learning",
            "Step 5: Dormant Accumulation — Chuan Shan Legacy Hundred Volumes: Ming fall Qing rise hide Ship Mountain, write 'Chuanshan Legacy'/'Reading Comprehensive Mirror Treatise'/'Yellow Book'/'Chu Ci Collected Annotations'/'Zhangzi Correct Meng Annotations' hundred volumes, spiritual independence"
        ],
        "expected": [
            "'Reading Comprehensive Mirror Treatise' became Chinese historical philosophy peak, Historical Cycle Theory/Momentum Theory/Practical Learning three great contributions",
            "Practical Learning Spirit/Momentum Theory/Historical Cyclical Law became late Ming early Qing thought peak, influenced Tan Sitong/Liang Qichao/Mao Zedong",
            "Lessons: Ming fall pain reflection/theory closed/lack institutional design/late year loneliness"
        ],
        "case": "Reading Comprehensive Mirror Treatise (1660s): Wang Fuzhi read Sima Guang 'Comprehensive Mirror' wrote treatise, discussed historical cycles. 'Rise: diligent frugal reverent, Decline: extravagant arrogant lustful', cycle law. Momentum: 'Momentum not heaven, not earth, human made', historical human shapeable. Six Classics Annotate Me: 'Six Classics annotate me, I annotate Six Classics', subjectivity hermeneutics. Practical Learning: 'Govern world not worry people not trust me, worry I cannot trust people', statecraft/practical. Chuan Shan Legacy: Hundred volumes/Classics/History/Philosophy/Collection/Philosophy/Literature/History/Full coverage. Result: Historical Cyclical Law/Practical Learning/Indigenous Modernity became modern thought resources."
    },
    "H-CYK-66": {
        "name": "Chen Yinke: Independent Spirit Academic Methodology Master",
        "description": "Independent Spirit Free Thought / Evidential Research and Interpretation / Liu Rushi Biography / Yuan Bai Poetry Annotations / Academic Methodology",
        "modes": [37, 22, 25, 28, 35],
        "reason": "Chen Yinke 'Independent Spirit, Free Thought', core thinking: Academic Methodology independence and freedom — 'Evidential Research and Interpretation' dual drive, 'No blind following authority, no blind following classics, no blind following habit'. 'Liu Rushi Biography' sources/literature/philosophy trilogy, 'Yuan Bai Poetry Annotations' poetry-history mutual verification, 'Sui Tang System Origins' institutional evolution. 'Gold Bright Hall Collection' 'My life work, in these two books', 'Independent Spirit, Free Thought'.",
        "steps": [
            "Step 1: Unity Knowledge Action — Evidential Research and Interpretation Dual Wheels: Evidential Research (materials collection/verification/distinguish false preserve true), Interpretation (theory building/meaning interpretation/modern transformation), dual drive/indispensable",
            "Step 2: Systems Thinking — Independent Spirit Free Thought: 'Not blind follow authority, not blind follow classics, not blind follow habit', academic autonomy/ideological freedom/methodology self-awareness",
            "Step 3: Abstract Induction — Liu Rushi Biography / Yuan Bai Poetry Annotations: Sources/Literature/Philosophy trilogy/Poetry-History Mutual Verification/Institutional Evolution/Micro History Writing/Big History Vision",
            "Step 4: Thinking Mode Selection — Academic Methodology Transmission: 'My life work, in these two books', teacher Wang Guowei/Luo Zhenyu/Break Luo Zhenyu/Teacher Chen Yuan/Cultivate Yu Jiaying/Ye Jie/Xu Fu/Gao Ming/Academic Torch Relay",
            "Step 5: Dormant Accumulation — Late Year Reflection: 'What I received from teacher, extended and expanded', Teacher Wang Guowei/Break Luo Zhenyu/Teacher Chen Yuan/Cultivate Yu Jiayi/Ye Xie/Xu Fu/Gao Ming/Academic Torch Relay"
        ],
        "expected": [
            "'Liu Rushi Biography'/'Yuan Bai Poetry Annotations'/'Sui Tang System Origins' become academic classics",
            "Independent Spirit/Free Thought/Evidential Interpretation Dual Wheels/Academic Torch Relay become Chinese Academic Methodology Benchmark",
            "Lessons: Late years blind/Home country broken/Academic loneliness/Independent Spirit Price High"
        ],
        "case": "Liu Rushi Biography (1940s): Oral/Recorded by Luo Honglin/300k chars/Source Liu Rushi life/Qian Qianyi/Southern Ming/Qing/Women/Intellectual/Three-in-one source inter-verification/Understanding Sympathy. Yuan Bai Poetry Annotations (1930s): Yuan Zhen/Bai Juyi poems/Sources/Verification/Mutual Verification/Institutional Evolution/Poetry-History Mutual Evidence. Sui Tang System Origins (1940s): Three Departments Six Ministries/Nine Temples Five Supervisors/Selection/Taxation/Military/Institutional Evolution/Institutional History. Late Years Oral/Luo Honglin Record/Zhu Weizheng Organize. Result: Independent Spirit/Free Thought/Evidential Interpretation Dual Wheels become Chinese Academic Methodology Benchmark."
    },
    "H-QM-66": {
        "name": "Qian Mu: Chinese History Methodology Cultural Center of Gravity Theorist",
        "description": "National History Outline/Three Essentials of Historiography/Cultural Center of Gravity/Chinese Dynasties Political Gains Losses/Historiography Methodology",
        "modes": [22, 25, 29, 28, 35],
        "reason": "Qian Mu 'Three Essentials of Historiography: Grasp Big Picture, Know Key Points, Understand Ancient-Present Changes', Core Thinking: Historiography Methodology and Cultural Center of Gravity Dual Contribution — Wrote 'National History Outline' became Popular History Classic. 'Chinese Historical Political Gains Losses' Analyzed Han/Tang/Song/Ming Five Dynasties Political Gains/Losses/Institutional Evolution/Gains-Losses Complementarity/No Perfect System. 'Three Essentials of Historiography: Grasp Big Picture, Know Key Points, Understand Ancient-Present Changes'. 'Reading History Makes Wise', 'Read Chinese History Makes Love China', Pioneer General Education.",
        "steps": [
            "Step 1: Abstract Induction — Historiography Three Essentials: Grasp Big Picture (Grasp Overall Pulse), Know Key Points (Master Key Turning Points/Institutions/Figures), Understand Ancient-Present Changes (Recognize Historical Evolution Logic/Causal Chains)",
            "Step 2: Systems Thinking — Cultural Center Downward Shift: Scholars->Gentry->Commoners/Political/Economic/Cultural Three Dimensions Cross-verify/Cultural Center as Historical Periodization Core Indicator",
            "Step 3: Natural Selection — Historiography Three Essentials: 'Grasp Big Picture, Know Key Points, Understand Ancient-Present Changes', Historiography Methodology Three Elements/Big Picture/Key Points/Changes",
            "Step 4: Feedback Loops — Chinese Dynasties Political Gains Losses: Han/Tang/Song/Ming Five Dynasties/Selection/Taxation/Military/Gains-Losses Complementary/Institutional Evolution/No Perfect System/Dynamic Balance",
            "Step 5: Dormant Accumulation — Late Years Taiwan/Inheritance: Moved Taiwan/'Eighty Recall Parents'/Teacher-Student Torch/Yu Yingshi/Gao Hua/Xu Zhuoyun/Ge Zhaoguang/Academic Torch Relay"
        ],
        "expected": [
            "'National History Outline'/'Three Essentials of Historiography'/'Chinese Dynasties Political Gains Losses' Became Chinese Historiography Three Cornerstones",
            "Cultural Center Downshift/Three Essentials/ Gains-Losses Argument Became Chinese Historiography Three Major Methodology Pillars/Influenced Yu Yingshi/Gao Hua/Xu Zhuoyun/Ge Zhaoguang",
            "Limitations: Idealism Lacking Implementation/Over-reliance External Forces"
        ],
        "case": "National History Outline (1940s): Cultural Center Downward Shift: Scholars->Gentry->Commoners/Political/Economic/Cultural Three Dimensions Cross-verify.
Three Essentials of Historiography (1950s): 'Grasp Big Picture, Know Key Points, Understand Ancient-Present Changes'.
Chinese Dynasties Political Gains Losses (1952): Han/Tang/Song/Ming/Qing Five Dynasties/Selection/Taxation/Military/Gains-Losses Complementary/Institutional Evolution/No Perfect System/Dynamic Balance.
Late Years Taiwan (1967): 'Eighty Recall Parents'/Teacher-Student Torch/Yu Yingshi/Gao Hua/Xu Zhuoyun/Ge Zhaoguang. Result: Historiography Methodology/Cultural Center/Gains-Losses Argument Became Chinese Historiography Three Major Pillars."
    },
    "H-LQC-68": {
        "name": "Liang Qichao: New Historiography and Reform Enlightenment Pioneer",
        "description": "Chinese History Research Method / New People Discourse / Reform Restoration / Ice Drinking Room Collection / Enlightenment Thought",
        "modes": [22, 25, 38, 28, 35],
        "reason": "Liang Qichao 'Young China Say', 'New People Say', 'Chinese History Research Method', Core Thinking: New Historiography Methodology and Reform Enlightenment Dual Breakthrough — Wrote 'Chinese History Research Method' Created 'New Historiography': 'History Is, Investigate Ancient, Verify Present, Predict Future'. 'New People Say' 'Want New China, Must First New People', Citizen Consciousness/Public Virtue/Public Spirit. 'Ice Drinking Room Collection' Hundred Volumes, 1898 Reform/ Hundred Days Reform/ Tan Sitong/Tan Yantong/Xu Fosu/Escape Japan/Run 'Clear Discourse Report''New People Monthly'. 'Revolution Not Kill Burn, Revolution Is Old System Reform'.",
        "steps": [
            "Step 1: Abstract Induction — New Historiography Three Principles: 'History Is, Investigate Ancient, Verify Present, Predict Future', Investigate/Verify/Predict Three Steps/Historiography Function Repositioning",
            "Step 2: Systems Thinking — New People System: New People/New Morality/New Knowledge/New Religion/New Literature/New Art/New Life/New State/Full-Dimensional New People Cultivation/Public Citizen Society Construction",
            "Step 3: Natural Selection — Reform Practice: 1898 Reform/Strong Learning Society/Current Affairs Report/Official/Escape/Run Newspaper/Ice Drinking Room Collection/Enlightenment/Radical/Conservative/Three Factions Struggle/Hundred Days Reform/Six Gentlemen/Exile",
            "Step 4: Feedback Loop — Ice Drinking Room Collection: Hundred Volumes/Poetry/Prose/Historiography/Philosophy/Politics/Literature/Self-Description/Reflection/Hundred Years Reprint/Influence Lu Xun/Hu Shi/Mao Zedong/Enlightenment Generation",
            "Step 5: Dormant Accumulation — Late Reflection: 'What I Received From Teacher, Extended And Expanded', Teacher Kang Youwei/Break Kang Youwei/Jinmen Death/Will 'Must Not Let China Perish In My Hands', Spiritual Legacy"
        ],
        "expected": [
            "'Chinese History Research Method' Became New Historiography Outline/'New People Discourse' Became Enlightenment Movement Outline/'Ice Drinking Room Collection' Became Modern Thought Treasure",
            "New Historiography/New People/Reform/Enlightenment Four Major Contributions/Influenced Lu Xun/Hu Shi/Mao Zedong/Generation Intellectuals",
            "Lessons: Radical vs Conservative Tension/Reform Failed/Exile Life/Thought Shift Complex/Late Years Buddhism Tendency"
        ],
        "case": "Chinese History Research Method (1922): 'Investigate Ancient, Verify Present, Predict Future', Three Steps/New Historiography Outline. New People Say (1902): New People/New Morality/New Knowledge/New Religion/New Literature/New Art/New Life/New State/Full-Dimensional New People. 1898 Reform (1898): Strong Learning Society/Current Affairs Report/Hundred Days Reform/Six Gentlemen/Liang Escape Japan. Ice Drinking Room Collection (1920s-1930s): Hundred Volumes/Poetry/Prose/Historiography/Philosophy/Politics/Literature/Self-Narration/Reflection. Late Years: 'I With Received From Teacher, Extended And Expanded', Break Kang Youwei/Jinmen Death. Result: New Historiography/New People/Reform/Enlightenment Four Contributions, Influenced Lu Xun/Hu Shi/Mao Zedong Generation Intellectuals."
    }
}

# Add to English scenarios
scenarios_en.update(new_en)

with open('scenarios_en.json', 'w', encoding='utf-8') as f:
    json.dump(scenarios_en, f, ensure_ascii=False, indent=2)

print(f"Updated scenarios_en.json: {len(scenarios_en)} total scenarios")