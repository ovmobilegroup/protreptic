import json

# Read the current scenarios files
with open('<repo>/data/scenarios_en.json', 'r') as f:
    scenarios_en = json.load(f)

with open('<repo>/data/scenarios_zh.json', 'r') as f:
    scenarios_zh = json.load(f)

# Find the H-HZX-001 scenarios in both files
hzx_en_indices = []
hzx_zh_indices = []

for i, s in enumerate(scenarios_en):
    if s.get('id', '').startswith('H-HZX-001-scenario-en'):
        hzx_en_indices.append(i)

for i, s in enumerate(scenarios_zh):
    if s.get('id', '').startswith('H-HZX-001-scenario-zh'):
        hzx_zh_indices.append(i)

print(f"Found {len(hzx_en_indices)} EN scenarios at indices: {hzx_en_indices}")
print(f"Found {len(hzx_zh_indices)} ZH scenarios at indices: {hzx_zh_indices}")

# Define the proper scenario descriptions for each mode
scenarios_en_new = {
    "M301": {
        "title": "Scenario 1: Sovereignty of Tianxia - Reimagining Political Legitimacy",
        "description": "Applying the Sovereignty of Tianxia Method to analyze how Huang Zongxi's 'Origin of the Ruler' (原君) chapter redefines political legitimacy: tracing power's origin to public good rather than heavenly mandate, distinguishing 'public Tianxia' from 'private Tianxia,' and establishing the people's well-being as the sole criterion for evaluating governance. This framework reveals why the Ming collapse was not merely dynastic failure but systemic illegitimacy."
    },
    "M302": {
        "title": "Scenario 2: Rule-of-Law Priority - Institutional Design Over Moral Cultivation",
        "description": "Using the Rule-of-Law Priority Method to examine Huang Zongxi's 'Origin of Law' (原法) argument that 'good law must precede good governance by individuals' (有治法而后有治人). The framework contrasts 'laws of the Three Dynasties' (public law serving all) against 'laws of one family' (private despotic ordinances), showing how institutional constraints and incentive structures—not ruler virtue—determine governance outcomes. This anticipates modern constitutionalism."
    },
    "M303": {
        "title": "Scenario 3: School Deliberation - Academic Institutions as Public Sphere",
        "description": "Applying the School Deliberation Method to Huang Zongxi's vision in 'Schools' (学校) chapter: schools as political deliberation venues where 'all instruments for governing Tianxia originate,' with the Grand Learning's director holding prime-ministerial status and even the emperor participating in debates. This framework analyzes how independent academic networks can check power through public rational discourse—the closest Chinese conception to parliamentary democracy."
    },
    "M304": {
        "title": "Scenario 4: Li-Qi Monism - Materialist Metaphysics Against Dualism",
        "description": "Using the Li-Qi Monism Method to analyze Huang Zongxi's critique of Cheng-Zhu 'li prior to qi' dualism. The framework shows how 'li is simply the pattern of qi' (理即在气中) unifies cosmology, epistemology, and ethics under a materialist qi-ontology. Applied to his astronomical/calendrical work, it demonstrates how operational patterns (li) depend on material carriers (qi), prefiguring modern systems thinking and anti-essentialism."
    },
    "M305": {
        "title": "Scenario 5: One Essence Many Manifestations - Pluralistic Academic Ecology",
        "description": "Applying the One Essence Many Manifestations Method to Huang Zongxi's compilation of 'Ming Ru Xue An': acknowledging diverse schools' valid kernels ('partial views and opposing arguments'), refusing homogenization ('pouring water into water'), and extracting truth from differences. The framework analyzes how intellectual diversity—Wang Yangming, Zhu Xi, Lu Jiuyuan schools coexisting—creates a resilient knowledge ecosystem superior to enforced orthodoxy."
    },
    "M306": {
        "title": "Scenario 6: Practical Statecraft - Learning for Real-World Problem Solving",
        "description": "Using the Practical Statecraft Method to examine Huang Zongxi's insistence that 'learning must originate from classics to avoid vacuity, and be verified through history to suffice for practical affairs' (学必原本于经术而后不为蹈虚，必证明于史籍而后足以应务). The framework traces how his 40-year 'Ming Wen Hai' compilation and 'Ming Yi Dai Fang Lu' directly targeted institutional dysfunctions, embodying the unity of theory and practice against late Ming vacuous scholarship."
    },
    "M307": {
        "title": "Scenario 7: Historical Source Criticism - Empirical Verification Across Disciplines",
        "description": "Applying the Historical Source Criticism Method to Huang Zongxi's interdisciplinary verification: using Western Han and Tang dynasty calendrical astronomy to verify 'Spring and Autumn Annals' eclipse records, and applying calendrical knowledge to authenticate the Old Text 'Shangshu.' The framework demonstrates how 'seeking truth from facts' (实事求是) operates through cross-disciplinary evidence—astronomy, philology, institutional history—eliminating rumor and bias."
    },
    "M308": {
        "title": "Scenario 8: Huang Zongxi's Law - Institutional Corruption in Tax Reform Cycles",
        "description": "Using Huang Zongxi's Law Method to analyze the 'accumulated harm that cannot be reversed' (积累莫返之害) pattern: each tax simplification (Tang Two-Tax, Ming Single-Whip, Qing Head-Tax-Into-Land) briefly reduces burden, but new hidden levies soon exceed pre-reform levels. The framework reveals how rulers legitimize exploitation through 'consolidation reform,' then layer new exactions—applicable to any institutional change where surface concessions mask structural predation."
    },
    "M309": {
        "title": "Scenario 9: Yi-Xia Distinction - Cultural Identity Beyond Race",
        "description": "Applying the Yi-Xia Distinction Method to Huang Zongxi's culturalist criterion: civilization (华夏文明), not bloodline, distinguishes Xia from Yi. When Yi possess civilized order their rule is acceptable; when Xia loses civilization it equals Yi. The framework analyzes how this non-racial culturalism underpinned his lifelong refusal to serve the Qing while embracing Western astronomy—upholding cultural orthodoxy without nationalist essentialism."
    },
    "M310": {
        "title": "Scenario 10: Synthesizing the Many - Inductive Knowledge Integration",
        "description": "Using the Synthesizing the Many Method to analyze Huang Zongxi's 'Ming Ru Xue An' compilation: from each scholar's complete works, 'extract essential threads' (纂要钩玄) without erasing individuality, then find the connecting deep structure. The framework shows how 'many manifestations returning to one essence' (万殊归一本) complements M305's analytical diversity—inductive synthesis (valley→river→sea) creating higher-order unity from preserved pluralism."
    }
}

scenarios_zh_new = {
    "M301": {
        "title": "场景 1：天下主权法——重构政治合法性",
        "description": "运用天下主权法分析黄宗羲《原君》篇如何重新定义政治合法性：将权力起源追溯至公共利益而非天命，区分'公天下'与'私天下'，确立天下万民福祉为评判政治制度的唯一标准。该框架揭示明朝灭亡非仅是王朝更替，而是系统性合法性的丧失。"
    },
    "M302": {
        "title": "场景 2：治法优先法——制度设计优于道德教化",
        "description": "运用治法优先法考察黄宗羲《原法》篇'有治法而后有治人'论断。框架对比'三代以上之法'(服务天下的公法)与'一家之法'(专制私法/非法之法)，展示制度约束与激励结构——而非君主德行——决定治理成效。这预见了现代宪政主义的核心逻辑。"
    },
    "M303": {
        "title": "场景 3：学校议政法——学术机构作为公共领域",
        "description": "运用学校议政法分析黄宗羲《学校》篇愿景：学校为政治议政场所，'治天下之具皆出于学校'，太学祭酒地位相当宰相，皇帝亦须参与讨论。该框架探讨独立学术网络如何通过公共理性话语制约权力——中国思想史上最接近议会民主的制度构想。"
    },
    "M304": {
        "title": "场景 4：理气一元法——反二元论的唯物主义本体论",
        "description": "运用理气一元法分析黄宗羲对程朱'理在气先'二元论的批判。框架展示'理即在气中'如何将宇宙论、认识论、伦理学统一于唯物气本原。应用于其天文学/历算研究，表明运行规律(理)依赖物质载体(气)，预示现代系统思维与反本质主义。"
    },
    "M305": {
        "title": "场景 5：一本万殊法——多元学术生态观",
        "description": "运用一本万殊法分析黄宗羲编纂《明儒学案》：承认各派合理内核('一偏之见'与'相反之论')，拒绝同质化('以水济水')，在差异中萃取真理。框架分析王学、朱学、陆学共存的学术多元性如何构建比强制正统更具韧性的知识生态系统。"
    },
    "M306": {
        "title": "场景 6：经世应务法——为解决现实问题的学问",
        "description": "运用经世应务法考察黄宗羲'学必原本于经术而后不为蹈虚，必证明于史籍而后足以应务'主张。框架追溯其耗时四十年的《明文海》编纂与《明夷待访录》著述如何直指制度弊病，体现知行合一，直指晚明王学末流空疏之弊。"
    },
    "M307": {
        "title": "场景 7：史料考辨法——跨学科实证验证",
        "description": "运用史料考辨法分析黄宗羲跨学科验证实践：以西汉三统历、唐代授时历推算验证《春秋》日食记录，以历法知识参与辨伪古文《尚书》。框架展示'实事求是'如何通过天文学、文献学、制度史等跨学科证据链，去除传闻谬误与偏见，存真去伪。"
    },
    "M308": {
        "title": "场景 8：黄宗羲定律法——税制改革中的制度性腐败循环",
        "description": "运用黄宗羲定律法分析'积累莫返之害'规律：唐两税法、明一条鞭法、清摊丁入亩每次改革虽短期减负，但新增隐性摊派使负担反弹超越改革前。框架揭示统治者以'并税改革'合法化隐性剥削后再叠加新盘剥的逻辑——适用于任何表面让利实则结构性掠夺的制度变革分析。"
    },
    "M309": {
        "title": "场景 9：夷夏之辨法——超越种族的文化认同标准",
        "description": "运用夷夏之辨法分析黄宗羲以文化文明度而非血统区分华夏与夷狄：夷狄具文明秩序可接受其统治，华夏丧失文明则等同夷狄。框架解析这一非种族主义文化主义如何支撑其终身不仕清朝、同时主张'会通中西之学'——坚守文化正统而不陷入狭隘民族主义。"
    },
    "M310": {
        "title": "场景 10：会众合一法——从差异中归纳的知识综合",
        "description": "运用会众合一法分析黄宗羲《明儒学案》编纂方法：从各家全集'纂要钩玄'提炼核心宗旨不抹杀个性，再寻找贯通深层结构。框架展示'万殊归一本'如何与一本万殊法互为表里——归纳综合(由谷达川、由川达海)在保留多元差异基础上构建更高层次的统一理解。"
    }
}

# Update EN scenarios
for idx in hzx_en_indices:
    s = scenarios_en[idx]
    mode_id = s.get('mode_id')
    if mode_id in scenarios_en_new:
        s['title'] = scenarios_en_new[mode_id]['title']
        s['description'] = scenarios_en_new[mode_id]['description']

# Update ZH scenarios
for idx in hzx_zh_indices:
    s = scenarios_zh[idx]
    mode_id = s.get('mode_id')
    if mode_id in scenarios_zh_new:
        s['title'] = scenarios_zh_new[mode_id]['title']
        s['description'] = scenarios_zh_new[mode_id]['description']

# Write back
with open('<repo>/data/scenarios_en.json', 'w') as f:
    json.dump(scenarios_en, f, ensure_ascii=False, indent=2)

with open('<repo>/data/scenarios_zh.json', 'w') as f:
    json.dump(scenarios_zh, f, ensure_ascii=False, indent=2)

print("\nUpdated scenarios successfully!")
print(f"Updated {len(hzx_en_indices)} EN scenarios and {len(hzx_zh_indices)} ZH scenarios")

# Verify
print("\nVerifying first EN scenario:")
print(json.dumps(scenarios_en[hzx_en_indices[0]], indent=2))
print("\nVerifying first ZH scenario:")
print(json.dumps(scenarios_zh[hzx_zh_indices[0]], indent=2))