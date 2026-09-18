import json

# Load existing data
with open('scenarios_zh.json', 'r', encoding='utf-8') as f:
    zh = json.load(f)
with open('scenarios_en.json', 'r', encoding='utf-8') as f:
    en = json.load(f)
with open('code_maps.json', 'r', encoding='utf-8') as f:
    cm = json.load(f)

# 10 P0-level figures from candidates_shortlist.md
new_entries = [
    {
        "code": "H-KZ-160",
        "name_zh": "孔子：儒家创始人/仁礼中庸/教育思想/正名/君子人格",
        "name_en": "Confucius: Confucianism Founder/Benevolence-Ritual-Mean/Education/Rectification of Names/Junzi Persona",
        "description_zh": "儒家创始人/仁礼中庸/教育思想/正名/君子人格/四教/七十二贤人/春秋笔法",
        "description_en": "Confucianism Founder/Benevolence-Ritual-Mean/Education/Rectification of Names/Junzi Persona/Four Teachings/Seventy-Two Disciples/Spring and Autumn Brushwork",
        "modes": [1, 5, 6, 22, 37],
        "reason_zh": "孔子创立「仁礼中庸」三位一体伦理本体论，将「克己复礼为仁」转化为可操作的「格物致知→诚意正心→修身齐家治国平天下」八目标准动作；首创「有教无类、因材施教」教育工程化体系，建立「诗书礼乐」四教标准化课程，确立「正名」作为社会治理的语言-制度校准协议——将抽象道德律令编译为可执行、可考核、可传承的标准作业程序（SOP）。",
        "reason_en": "Confucius established the 'Benevolence-Ritual-Mean' triune ethical ontology, transforming 'restraining self and returning to ritual is benevolence' into actionable 'investigating things-extending knowledge→sincere intention-rectifying mind→cultivating self-regulating family-governing state-pacifying world' eight-step standard procedure; pioneered 'education for all, teaching according to aptitude' educational engineering system, establishing 'poetry-book-ritual-music' four-teaching standardized curriculum, establishing 'rectification of names' as language-institution calibration protocol for social governance—compiling abstract moral decrees into executable, assessable, inheritable standard operating procedures (SOPs).",
        "steps_zh": [
            "第1步：本体锚定（矛盾分析法·模式 1）：识别「人欲横流、礼崩乐坏」为春秋乱世主要矛盾，锁定「仁」为破解主要矛盾的核心杠杆——仁者爱人，以爱人为己任，将私利让位于公义。",
            "第2步：协议标准化（实事求是·模式 5）：制定「正名」语言-制度协议——「名不正则言不顺，言不顺则事不成」，将君臣父子兄弟夫妇五伦关系编码为可验证的行为规范（SOP），消除解释歧义空间。",
            "第3步：系统集成（总体性思维·模式 22）：构建「仁-礼-中-庸-孝-悌-忠-信」八维美德向量空间，设计「克己复礼→仁」为核心算子的道德运算系统，实现个体修养→家庭治理→国家治理→天下平治的递归放大。",
            "第4步：工程化传承（统一战线法·模式 6）：建立「有教无类、因材施教」人才筛选-培养-部署流水线：三千弟子→七十二贤人→《论语》语料库标准化→儒家学派组织化，形成「师承-文本-共同体」三位一体传承协议。",
            "第5步：人格校准（知行合一/致良知·模式 37）：设定「君子」人格基准——「君子喻于义，小人喻于利」；建立「吾日三省吾身」（为人谋而不忠乎、与朋友交而不信乎、传不习乎）高频自检机制，将道德抽象指标转化为可量化的日常行为审计清单。"
        ],
        "steps_en": [
            "Step 1: Ontological Anchoring (Contradiction Analysis·Mode 1): Identify 'human desires rampant, rites collapsing' as Spring-Autumn chaos primary contradiction, lock 'benevolence' as core lever to resolve primary contradiction—benevolent loves others, takes loving others as mission, subordinating private interest to public righteousness.",
            "Step 2: Protocol Standardization (Seeking Truth from Facts·Mode 5): Establish 'rectification of names' language-institution protocol—'if names not correct, speech not smooth; speech not smooth, affairs not accomplished', encode five cardinal relationships (ruler-minister, father-son, elder-younger brothers, husband-wife, friends) as verifiable behavioral norms (SOPs), eliminating interpretive ambiguity space.",
            "Step 3: System Integration (Holistic Thinking·Mode 22): Build 'benevolence-ritual-mean-mid-filial-fraternal-loyal-trust' eight-dimensional virtue vector space, design 'restraining self returning to ritual→benevolence' core operator moral computation system, achieving individual cultivation→family governance→state governance→world pacification recursive amplification.",
            "Step 4: Engineering Transmission (United Front·Mode 6): Establish 'education for all, teaching according to aptitude' talent screening-cultivation-deployment pipeline: 3000 disciples→72 worthies→Analects corpus standardization→Confucian school organization, forming 'master-disciple transmission-text-community' trinity transmission protocol.",
            "Step 5: Personality Calibration (Unity of Knowledge and Action·Mode 37): Set 'junzi' personality benchmark—'junzi understands righteousness, small man understands profit'; establish 'I examine myself three times daily' (planning for others not loyal? interacting with friends not trustworthy? transmitting not practiced?) high-frequency self-audit mechanism, transforming abstract moral indicators into quantifiable daily behavioral audit checklist."
        ],
        "expected_zh": [
            "「仁礼中庸」三位一体伦理本体论，成儒家两千年正统基石",
            "「正名」语言-制度协议，成中国政治哲学核心方法论",
            "「有教无类、因材施教」教育工程化，成中国教育思想源头",
            "「克己复礼→仁」核心算子，成道德运算标准操作程序",
            "《论语》语料库标准化，成儒家知识工程首个标准化知识库"
        ],
        "expected_en": [
            "'Benevolence-Ritual-Mean' triune ethical ontology, foundation of Confucian two-thousand-year orthodoxy",
            "'Rectification of names' language-institution protocol, core methodology of Chinese political philosophy",
            "'Education for all, teaching according to aptitude' educational engineering, source of Chinese educational thought",
            "'Restraining self returning to ritual→benevolence' core operator, moral computation standard operating procedure",
            "Analects corpus standardization, first standardized knowledge base of Confucian knowledge engineering"
        ],
        "case_zh": "孔子（前551–前479），鲁国陬邑人。少孤贫，十五志于学，三十而立，四十而不惑，五十知天命，六十耳顺，七十从心所欲不逾矩。
早年仕鲁，为中都宰/司空/大司寇，推行「礼」治理。鲁定公十年，主「郊饮酒」礼，以「正名」整顿官场。后因「三桓」专权，周游列国十四年（齐/宋/郑/陈/蔡/楚），遇陈蔡之厄「绝粮」，「弦歌不辍」。
晚年归鲁，删《诗》《书》，定《礼》《乐》，修《春秋》，订《诗》《书》，训《礼》《乐》，以《春秋》笔法「微言大义」评判历史。
弟子三千，贤者七十二，编《论语》语录，成儒家核心经典。其「仁礼中庸/教育工程/正名协议/师承传承」四维工程，成中国两千年文明操作系统内核。",
        "case_en": "Confucius (551-479 BCE), Qufu Lu native. Orphaned young, poor, set heart on learning at 15, established at 30, no doubts at 40, knew Heaven's mandate at 50, obedient ear at 60, followed heart's desire without transgression at 70.
Early served Lu as Zhongdu magistrate/Sikong/Grand Minister of Justice, implemented 'ritual' governance. Duke Ding 10th year, presided 'suburban drinking rite', rectified officialdom with 'rectification of names'. Later due to Three Huan clan monopoly, wandered states 14 years (Qi/Song/Zheng/Chen/Cai/Chu), suffered Chen-Cai starvation 'cut off grain', 'string song not ceasing'.
Late years returned to Lu, edited Poetry/Books, fixed Rites/Music, revised Spring and Autumn Annals, settled Poetry/Books, taught Rites/Music, with Spring and Autumn brushwork 'subtle words great meaning' judging history.
3000 disciples, 72 worthies, compiled Analects sayings, became Confucian core classic. His 'benevolence-ritual-mean/education engineering/rectification of names protocol/master-disciple transmission' four-dimensional engineering became Chinese two-thousand-year civilization OS kernel."
    },
    {
        "code": "H-DZS-161",
        "name_zh": "董仲舒：天人感应/汉儒正统/独尊儒术/春秋决狱/三纲五常",
        "name_en": "Dong Zhongshu: Heaven-Man Resonance/Han Confucian Orthodoxy/Sole Confucianism/Spring-Autumn Judging/Three Bonds Five Constants",
        "description_zh": "天人感应/独尊儒术/春秋决狱/三纲五常/汉儒正统/天人三策/制度化制衡",
        "description_en": "Heaven-Man Resonance/Sole Confucianism/Spring-Autumn Judging/Three Bonds Five Constants/Han Confucian Orthodoxy/Three Strategies/Institutional Checks",
        "modes": [22, 32, 34, 28, 35],
        "reason_zh": "董仲舒构建「天人感应-春秋决狱-三纲五常」三位一体政治神学体系，将儒家伦理从「道德说教」重构为「国家治理操作系统」：以「天人三策」对策入主流，确立「春秋决狱」以经断法司法标准化协议，推动「罢黜百家独尊儒术」完成意识形态基础设施国家标准化，奠定两千年儒学正统地位——将分散经学转化为可部署、可考核、可传承的国家治理标准库。",
        "reason_en": "Dong Zhongshu constructed 'Heaven-Man Resonance-Spring Autumn Judging-Three Bonds Five Constants' triune political theology system, transforming Confucian ethics from 'moral preaching' to 'state governance operating system': via 'Three Strategies on Heaven and Man' entered mainstream, established 'Spring Autumn Judging' using classics to judge law judicial standardization protocol, promoted 'suppress hundred schools exclusively honor Confucianism' completing ideological infrastructure national standardization, founding two-thousand-year Confucian orthodoxy—transforming scattered classical studies into deployable, assessable, inheritable national governance standard library.",
        "steps_zh": [
            "第1步：本体绑定（总体性思维·模式 22）：建立「天-君-相-民」四层本体映射——「天不变、道亦不变」，将皇帝权力合法性锚定于「承天意、行天罚」的宇宙论契约，把道德律令上升为本体论必然，消除政权合法性解释空间。",
            "第2步：协议标准化（程序正义法·模式 32）：设计「春秋决狱」司法解释协议——「春秋者、经世之大典也、以经断法」，将《春秋》微言大义编译为可操作的判例法库：君为臣纲、父为子纲、夫为妻纲（三纲）+ 仁义礼智信（五常）= 8 条核心判决规则，实现「以经断法」的司法标准化。",
            "第3步：制度制衡（制度化制衡/杯酒释兵权·模式 34）：推动「三纲五常」编入律令，构建「君权-相权-法权-伦权」四权制衡架构：天子奉天承运（权力来源合法化）、丞相辅政（行政执行标准化）、御史监察（监督程序化）、儒生讲经（意识形态生产机制化），形成「不防人、防制度漏洞」的治理闭环。",
            "第4步：人才管道（冗余备份法·模式 28）：建立「太学-五经博士-贤良方正」三级人才选拔-认证-部署流水线：太学教授标准化课程（五经）→ 博士授予官方认证（学位制雏形）→ 贤良方正对策入仕（考试+推荐双轨）→ 地方推举考核（绩效考核），实现意识形态人才的规模化复制与部署。",
            "第5步：动态校准（蛰伏秩势思维·模式 35）：设计「灾异-策免-修省」负反馈调节机制——天变（日食、地震、水旱）→ 策免三公（问责机制）→ 皇帝修省（自我纠错）→ 诏书宽恤（释放压力）→ 制度微调（参数优化），将宇宙论信号转化为治理系统的自适应调参协议。"
        ],
        "steps_en": [
            "Step 1: Ontological Binding (Holistic Thinking·Mode 22): Establish 'Heaven-Ruler-Minister-People' four-layer ontological mapping—'Heaven unchanging, Dao unchanging', anchoring emperor power legitimacy to 'receiving Heaven's will, executing Heaven's punishment' cosmological contract, elevating moral decrees to ontological necessity, eliminating regime legitimacy interpretation space.",
            "Step 2: Protocol Standardization (Procedural Justice·Mode 32): Design 'Spring Autumn Judging' judicial interpretation protocol—'Spring Autumn is the great classic of governing the world, judging law by classics', compiling Spring Autumn subtle words great meaning into operable case law library: ruler guides minister, father guides son, husband guides wife (Three Bonds) + benevolence-righteousness-ritual-wisdom-trust (Five Constants) = 8 core judgment rules, realizing 'judging law by classics' judicial standardization.",
            "Step 3: Institutional Checks (Institutional Checks/Cup Wine Releasing Military Power·Mode 34): Promote 'Three Bonds Five Constants' into statutes, build 'imperial power-chancellor power-legal power-ethical power' four-power checks architecture: Son of Heaven receives Heaven's mandate (power source legitimized), Chancellor assists governance (administrative execution standardized), Censors supervise (supervision proceduralized), Confucians lecture classics (ideology production mechanized), forming 'not guarding against people, guarding against institutional loopholes' governance closure.",
            "Step 4: Talent Pipeline (Redundancy Backup·Mode 28): Establish 'Imperial Academy-Five Classics Erudites-Worthy and Good' three-tier talent selection-certification-deployment pipeline: Imperial Academy teaches standardized curriculum (Five Classics)→ Erudites grant official certification (degree prototype)→ Worthy and Good enter service via policy essays (exam+recommendation dual-track)→ Local recommendation assessment (performance evaluation), realizing ideological talent mass replication and deployment.",
            "Step 5: Dynamic Calibration (Dormant Accumulation·Mode 35): Design 'calamity-dismissal-self-cultivation' negative feedback regulation—heavenly anomalies (eclipse, earthquake, flood/drought)→ dismiss three dukes (accountability)→ emperor self-reflection (self-correction)→ edict pardon (pressure release)→ institutional fine-tuning (parameter optimization), converting cosmological signals into governance system adaptive parameter tuning protocol."
        ],
        "expected_zh": [
            "「天人三策」对策入主流，奠定汉儒正统两千年地位",
            "「春秋决狱」确立「以经断法」司法标准化协议",
            "「罢黜百家独尊儒术」完成意识形态基础设施国家标准化",
            "「三纲五常」编入律令，构建「君权-相权-法权-伦权」四权制衡架构",
            "「太学-五经博士-贤良方正」三级人才管道，成意识形态人才规模化复制模板"
        ],
        "expected_en": [
            "Three Strategies on Heaven and Man entered mainstream, founding Han Confucian orthodoxy for two millennia",
            "Spring Autumn Judging established 'judging law by classics' judicial standardization protocol",
            'Suppressing hundred schools exclusively honoring Confucianism completed ideological infrastructure national standardization',
            "Three Bonds Five Constants entered statutes, building 'imperial-chancellor-legal-ethical' four-power checks architecture",
            "Imperial Academy-Five Classics Erudites-Worthy and Good three-tier talent pipeline, ideological talent mass replication template"
        ],
        "case_zh": "董仲舒（前179–前104），广川人。少治《春秋》，景帝时以博士待诏，武帝元光元年（前134）上「天人三策」：一策论天人感应、二策论正统正统、三策论改革制度。武帝采纳，罢黜百家独尊儒术。董仲舒推「春秋决狱」：以《春秋》经义断案，创「以经断法」司法标准化；立「三纲五常」：君为臣纲/父为子纲/夫为妻纲+仁义礼智信，成伦理-法律融合标准库；推「罢黜百家独尊儒术」，设五经博士，建太学，确立儒学正统地位。其「天人感应/春秋决狱/独尊儒术/三纲五常」四维体系，成两千年儒学正统奠基工程，奠「汉儒正统/天人感应/春秋决狱/三纲五常/制度化制衡」五维制度基因。",
        "case_en": "Dong Zhongshu (179-104 BCE), Guangchuan native. Youth studied Spring Autumn, Emperor Jing as Erudite awaited edict, Emperor Wu Yuan Guang 1st year (134 BCE) presented 'Three Strategies on Heaven and Man': 1) Heaven-Man resonance, 2) orthodoxy, 3) institutional reform. Emperor Wu adopted, suppressed hundred schools exclusively honored Confucianism. Dong promoted 'Spring Autumn Judging': judged cases by Spring Autumn classic meaning, created 'judging law by classics' judicial standardization; established 'Three Bonds Five Constants': ruler guides minister/father guides son/husband guides wife + benevolence-righteousness-ritual-wisdom-trust, forming ethics-law fusion standard library; promoted 'suppress hundred schools exclusively honor Confucianism', established Five Classics Erudites, built Imperial Academy, founding Confucian orthodoxy status. His 'Heaven-Man resonance/Spring Autumn Judging/exclusive Confucianism/Three Bonds Five Constants' four-dimensional system became two-thousand-year Confucian orthodoxy foundational engineering, founding 'Han Confucian orthodoxy/Heaven-Man resonance/Spring Autumn Judging/Three Bonds Five Constants/institutional checks' five-dimensional institutional genes."
    }
]

# Add remaining 8 figures similarly...
# For brevity, I'll add them in the next step

print("First 2 figures ready to add")