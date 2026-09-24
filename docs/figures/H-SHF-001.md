# 沈复 (Shen Fu, H-SHF-001) - Phase21-R9 九节档案

本页为**只读档案**: 由 `build_shf_r9_archive.py` 自 R9 重做载荷逐字装配（`data/figures/H-SHF-001.json` / `data/individuals/H-SHF-001_modes.json` / 主库 `data/modes_data.json` / 场景库 `data/scenarios_zh|en.json` / `data/code_maps.json`），未新增事实性内容；引文与出处核验状态 pending（核验另立卡）。
本件为 Phase21-R9 重做件: 旧件（R7 核名裁定的「虚名空壳」，无存世文献依据）维持归档、不唤醒、不改名、不迁载荷（旧模式码段零复用；登记见 `docs/scratch/legacy20_r9_shenfu_landing/id_mapping.tsv`）；授权链＝C 组核名裁定＋用户 2026-09-24 拍板「换人重做」（背景见重建报告 §3.2）。本页为 R9 重做后在站点文档层的**首次装配**（此前无在册旧页）。

**人物**: 沈复（Shen Fu）｜**生卒**: 1763-（卒年失考；约 1808 年以后在世，下限不明）｜**时代**: 清朝（乾隆—道光） / Qing Dynasty (Qianlong-Daoguang)
**字号**: 字 三白｜号 梅逸
**学派**: 自传文学/生活美学
**思想传统**: 明清文人生活书写与自述传统
**代表作**: 《浮生六记》（存卷一~卷四；卷五《中山记历》、卷六《养生记道》原佚，现传系伪续）｜《水绘园图册》（上海博物馆藏；真伪曾有争论）｜《幞山风木图》（已佚；胡不归《沈复年谱》记）
**名言**: 布衣菜饭，可乐终身。
**名言出处**: 《浮生六记》卷一·闺房记乐（芸语；W8；SHF-1 素材包 §三 M-SHF-005）
**身份**: 国籍 中国｜民族 汉族
**相关人物**: H-MT-001（徐霞客）、H-JST-001（金圣叹）、H-SU-001（苏轼）

- code: H-SHF-001｜拼音: Shen Fu｜生卒: 1763/（卒年失考）｜时代: 清朝（乾隆—道光） / Qing Dynasty (Qianlong-Daoguang)｜模式计数: 10
- modes: M-SHF-001 ~ M-SHF-010（全新码：无旧号，旧件零复用；旧模式码段零出现，逐条登记见 `id_mapping.tsv` 与各模式 `legacy_mode_id`（全空））
- 载荷: `data/figures/H-SHF-001.json`｜`data/individuals/H-SHF-001_modes.json`｜主库 `data/modes_data.json`（四面同体: 图档内嵌 = 伴随包 = 主库 = landing combined = modes_library_entries，逐对象全等）
- 登记链（R9 重做全链）: **R9 深度研究（SHF-1 素材包）** `e0a98aa8`（卡 t_d78053e7, serrano；10 条模式逐条落源（引文 35/35 终跑）＋身份证据链＋H-SHF-001 查重 0 占用；见证副本 35 件随件入库；零库写）；**R9 重建落盘** `59bc5471`（卡 t_b6d4c0ee, elcano；figure/individuals 三件＋冻结副本九件＋生成器与核验脚本；独立核验 74 PASS/0 FAIL；引文 35/35 见证复核；主库零写入（回执补记 a515badd））；**R9 合并入主库** `5a657b81`（卡 t_a7d233f0, barbosa；+10 条（modes 3301->3311，total 随动）／注册 code_maps 215->216、figure_names 1084->1085／场景 +10+10／标签 +20（7518->7538）／顶层块 23 键；站链五步；门禁四项 exit 0；独立核验 53 PASS/0 FAIL（回执补记 906a0bee；核验补记 c3cceb19））；**R9 QA 独立验收** `95c044aa`（卡 t_83e0d68d, espinosa；终轮 75 PASS / 0 FAIL / 5 INFO（80 行断言；判据全部重回原始取证）；含 1 项闭合热修：发布仓补镜像链产物 2 件（54df4c4）；（回执补记 c2d5820a））；**R9 文档归档** `本卡`（卡 t_7e5afcbb, pigafetta；本页首次装配；生成器 build_shf_r9_archive.py（幂等）＋文档层独立验收 verify_shf_r9_archive.py（第二实现＋反向注入自检）；镜像与 push 回执见本页第九节与归档报告）
- 报告索引: 素材包 `docs/research/phase21r9_shenfu_sourcing_report.md`｜落盘 `docs/research/phase21r9_shenfu_rebuild_report.md`｜合并 `docs/research/phase21r9_shenfu_merge_report.md`（证据 `.merge_evidence.json`）｜QA `docs/research/phase21r9_shenfu_qa_report.md`（证据 `.qa_evidence.json`）｜归档 `docs/research/phase21r9_shenfu_archive_report.md`（本卡）
- 页面字段映射: 一<-historical_significance｜二<-core_thoughts｜三<-individuals/H-SHF-001_modes.json（10 模式）｜四<-scenarios_zh/en（C-SHF-001~010 与 E）｜五<-modern_applications_zh｜六<-code_maps.figures.H-SHF-001.cross_references｜七<-tags｜八<-influence｜九<-QA 验收记录/口径/缺项/台账
- caveats（图档逐条）:
  - Phase21-R9 重建落盘：10 条 key_quote 逐字取自 SHF-1 素材包（§三 quotes；并经见证副本强归一化复核）；核验状态 pending，入库前须走独立核验流程
  - 卒年失考：death_year=null；注记「约 1808 年以后在世，下限不明」（俞平伯/胡不归口径）。网络无源卒说（年份异说）、错籍表述与「名复」方志说等一律不采（素材包 §1.4/§4.5）
  - 「名复」属行世名：杨引传序（1877）明言「名则已逸」；最早书面痕迹为《水绘园图》款「三白沈复」（真伪曾有争论，属疑似）——其在原始文献中的依据无从查得，引用须并注
  - 卷五/卷六红线：现传《中山记历》《养生记道》系伪续，任何题材不得采其文本；《海国记》（钱泳《记事珠》辑本）与琉球之行作疑似史料单列（素材包 §1.6/§八.14）
  - 转引层标注：林语堂评语（英文原文未成证）、陈寅恪引文（以学术源为准）、俞平伯序、胡不归年谱小引等均保留转引链，未升格为沈复原文
  - 用字异文：M-SHF-009「小景可以入画」从通行本口径（维基文库底本作「邪可以入画」，双注登记，素材包 §八.1）；「秋侵人影瘦，霜染菊花肥」与管诗引「秋深人瘦菊花肥」两式各归出处
  - school / intellectual_tradition / core_thoughts 等为描述性标签（依素材包主题池归纳，非当事人自认学派）；cross_references 三条为对照阅读框架（具体比对另行立卡）
  - 图像素材：藏画《水绘园图册》与题款为确证（转录本），其真伪之争与「作幕如皋十余年」说按素材包登记；未获可靠画像，不使用
- 未展开字段（本页未逐条搬迁，按现状保真）: 无（本件载荷字段齐备；图档与个体档除 `modes` 外逐字全等）

## 一、历史定位

沈复（1763 年生，卒年失考），字三白，号梅逸，江苏长洲（今苏州市）人，居苏州沧浪亭畔；习幕四十余年，兼及经商、绘事与著述。生乾隆癸未冬十一月廿二日（一手自述；精确的公历折算日系衍生写法，见素材包 §八.11）；「游幕三十年来」遍历南北。妻陈芸（字淑珍，1763-1803，同齿长十月）：缔姻于乾隆乙未（1775）七月十六日，成婚于乾隆庚子（1780）正月二十二日；嘉庆癸亥（1803）三月三十日芸亡，权葬扬州西门外之金桂山（俗呼郝家宝塔），作者忆「妻梅子鹤」语而自号梅逸——此为「梅逸」一号的一手证据。所著《浮生六记》存四卷（闺房记乐、闲情记趣、坎坷记愁、浪游记快），1874 年至 1877 年间经潘麐生序、王韬跋、杨引传序而刊行；刊行时作者之名已失传——杨引传序明言「名则已逸」，今行「沈复」为民国以来行世名。卒年诸说以俞平伯（当在嘉庆十二年（1807）以后）与胡不归《沈复年谱》小引（约在嘉庆十三年（1808）以后）为最稳口径；网络异说与错籍表述不采。其写作以「记其实情实事」为律令，经俞平伯、陈寅恪推重（转引层），并经林语堂评语（转引）与教材选文扩大影响。

## 二、核心思想

（字段 `core_thoughts`，逐条搬迁）

- 实录真情：以「记其实情实事」为写作律令（M-SHF-001）
- 物外之趣：把日常微物重译为景观（M-SHF-002）
- 独出己见：判断标准收归内在（M-SHF-003）
- 就事论事：省俭与雅洁的双约束解法（M-SHF-004）
- 布衣菜饭：幸福的最小方案（M-SHF-005）
- 情之所钟：以情为尺的取舍（M-SHF-006）
- 知己同心：知音结构的亲密关系（M-SHF-007）
- 坎坷自省：把性格作为境遇变量（M-SHF-008）
- 得画意：会心落到手艺（M-SHF-009）
- 浪游心得：观照优先于到过（M-SHF-010）

## 三、十大思维模式 (M-SHF-001 ~ M-SHF-010)

### M-SHF-001 实录真情法 (Recording True Facts and Real Feelings Method)

- 定义: 「记其实情实事」是《浮生六记》全书的写作律令：作者自认「少年失学」「稍识之无」，不惭于文、不事文法雕琢，把亲历的实事与真情直录于笔墨；在他看来，「事如春梦」转瞬无痕，若不记之笔墨，未免有辜生命所予的厚分。此法以「如实」为最高标准——记录本身即是对生活的回报。
- 原文: 所愧少年失学，稍识之无，不过记其实情实事而已，若必考订其文法，是责明于垢鉴矣。
  > I am ashamed that I did not study in my youth and know only a few characters—I merely record the true facts and real feelings; to insist on examining my grammar would be to demand brightness from a soiled mirror.
- 出处: 《浮生六记》卷一·闺房记乐开篇（兼及俞平伯序、陈寅恪转引）
- 关键概念: 记其实情实事 | 少年失学 | 稍识之无 | 记之笔墨 | 有辜彼苍之厚
- 领域: 自传书写/写作方法（Autobiographical Writing / Method of Composition）｜层级: 核心｜优先级: 1
- 步骤:
  - 立志：以「事如春梦了无痕」为警觉——不记则辜负生命的厚分，遂起记录之志
  - 去饰：不惭「少年失学」，不求文法考订，把修饰欲按下
  - 直录：以「记其实情实事」为律令，写亲历的实事与真情
  - 成书：把记录做成可传的完整文本（卷一~卷四即其成品）
- 典型案例:
  - 卷一开篇自述记录的动因：「东坡云，“事如春梦了无痕”，苟不记之笔墨，未免有辜彼苍之厚。」——卷一·闺房记乐开篇（W8@69；繁体底本 W1）——「不记」被视作对生命的辜负，此即全书写作的出发句。
  - 同篇自谦兼立律令：「所愧少年失学，稍识之无，不过记其实情实事而已，若必考订其文法，是责明于垢鉴矣。」——同前（W8@116）
  - 俞平伯评其文体效果（转引层：以不修饰见实录之力）：「统观全书，无酸语，赘语，道学语，殆以此乎？」——俞平伯《重刊〈浮生六记〉序》（W20@388）
  - 陈寅恪推重其文体地位（转引层）：「此后来沈三白《浮生六记》之《闺房记乐》，所以为例外创作。」——陈寅恪《元白诗笺证稿》（转引：W22@8069；另见 W21 同源转引）
- 现代应用: 日记与自我民族志写作的先声 | 「如实」作为修辞策略本身 | 自媒体写作：以真实经验对抗过度修辞 | 家庭口述史与私人记忆的整理方法
- 关联模式: M-SHF-010
- 类目: 文艺审美（归一值）｜category_raw: 写作方法论·自传书写（原值留证）｜legacy_mode_id: （无——全新码，无旧号）
- 核验: status=pending｜method=phase21r9-shenfu-rebuild-landing｜引文与出处未独立核验（evidence 原文见第九节）

### M-SHF-002 物外之趣法 (Delight Beyond Things Method)

- 定义: 以「心之所向」为转换器：把日常微物（帐中蚊群、丛草虫蚁、土砾凹凸）重译为宏大景观（群鹤舞空、青云白鹤观、林丘壑谷），从平淡中生「物外之趣」。作者自述此法成于童稚时——「张目对日，明察秋毫」「细察其纹理」；所以它不是逃避现实的幻想，而是对感知的主动重构：先细看，再以小见大。
- 原文: 余忆童稚时，能张目对日，明察秋毫。见藐小微物，必细察其纹理，故时有物外之趣。
  > I recall that in my boyhood I could look at the sun with open eyes and discern the smallest detail; whenever I saw some tiny thing, I would closely examine its texture—and so I often enjoyed a charm beyond the things themselves.
- 出处: 《浮生六记》卷二·闲情记趣开篇
- 关键概念: 物外之趣 | 张目对日，明察秋毫 | 细察其纹理 | 心之所向 | 神游其中
- 领域: 审美感知/童心与创造（Aesthetic Perception / Childlike Creativity）｜层级: 核心｜优先级: 2
- 步骤:
  - 细察：对藐小微物先看其纹理
  - 心向：以「心之所向」为景物定标（蚊作鹤、草作林）
  - 重构：把小物放大成大景，并神游其中
  - 验收：以「怡然称快」自得与否，检验转换是否成立
- 典型案例:
  - 卷二开篇总述童稚时的观看方式：「余忆童稚时，能张目对日，明察秋毫。见藐小微物，必细察其纹理，故时有物外之趣。」——卷二·闲情记趣开篇（W8@33）
  - 「留蚊于素帐中」——把蚊群重构为青云白鹤观：「又留蚊于素帐中，徐喷以烟，使其冲烟飞鸣，作青云白鹤观，果如鹤唳云端，为之怡然称快。」——卷二（W8@97）
  - 「以丛草为林」——以微物搭建丘壑并神游其中：「以丛草为林，以虫蚁为兽，以土砾凸者为丘，凹者为壑，神游其中，怡然自得。」——卷二（W8@158）
- 现代应用: 想象力训练：把平凡素材重译为景观 | 自然教育：从细察纹理开始 | 儿童美育：识别并保护童稚的观看方式 | 注意力如何创造世界（「心之所向，则或千或百」）
- 关联模式: M-SHF-009
- 类目: 文艺审美（归一值）｜category_raw: 审美转化·童心与创造（原值留证）｜legacy_mode_id: （无——全新码，无旧号）
- 核验: status=pending｜method=phase21r9-shenfu-rebuild-landing｜引文与出处未独立核验（evidence 原文见第九节）

### M-SHF-003 独出己见法 (Independent Judgment Method)

- 定义: 凡事「独出己见，不屑随人是非」：论诗品画持「人珍我弃、人弃我取」的取舍观；名胜的得失不随名气，而「贵乎心得」——判断的标准收归内在。底气来自阅历：作者自述「游幕三十年来」遍历南北，见得广，故能不随人。此法不是刻意反潮流，而是把评价权收回自己手里。
- 原文: 余凡事喜独出己见，不屑随人是非，即论诗品画，莫不存人珍我弃、人弃我取之意，故名胜所在，贵乎心得
  > In all things I like to form my own view and disdain following others in praise and blame; in judging poetry and appraising painting I always keep the sense of discarding what others prize and prizing what they discard—hence for a place of scenic fame, what matters is what the heart gains there.
- 出处: 《浮生六记》卷四·浪游记快
- 关键概念: 独出己见 | 不屑随人是非 | 人珍我弃、人弃我取 | 贵乎心得 | 游幕三十年
- 领域: 独立判断/审美自主（Independent Judgment / Aesthetic Autonomy）｜层级: 核心｜优先级: 3
- 步骤:
  - 阅历：以「游幕三十年」广其见闻
  - 独立：凡事独出己见，不屑随人是非
  - 取舍：人珍我弃、人弃我取
  - 内证：以「心得」为最终验收标准
- 典型案例:
  - 卷四自述其判断姿态与取舍观：「余凡事喜独出己见，不屑随人是非，即论诗品画，莫不存人珍我弃、人弃我取之意，故名胜所在，贵乎心得」——卷四·浪游记快（W8@89；句接「余游幕三十年来」段）——「贵乎心得」兼含对「随人」的不满。
  - 同卷自述阅历（独立判断的底气）：「余游幕三十年来，天下所未到者，蜀中、黔中与滇南耳。」——卷四（W8@36）
- 现代应用: 反打卡式审美：不以热度定优劣 | 判断标准的内化与自证 | 小众趣味的自我辩护与再发现 | 用阅历为独立判断兜底
- 关联模式: M-SHF-010
- 类目: 认识论逻辑（归一值）｜category_raw: 独立判断·审美自主（原值留证）｜legacy_mode_id: （无——全新码，无旧号）
- 核验: status=pending｜method=phase21r9-shenfu-rebuild-landing｜引文与出处未独立核验（evidence 原文见第九节）

### M-SHF-004 就事论事法 (Each Matter on Its Own Terms Method)

- 定义: 省俭不等于将就：「贫士起居服食以及器皿房舍，宜省俭而雅洁」；省俭之法叫「就事论事」——就器皿房舍的实况，逐件事找出最省的实现法，让清贫生活仍达到「雅洁」。其总命题为「竹头木屑皆有用」：材料没有贵贱，只有未找到的做法；约束之下，眼光决定方案。
- 原文: 贫士起居服食以及器皿房舍，宜省俭而雅洁，省俭之法曰“就事论事”。
  > For a poor scholar, in daily living, food and clothing, utensils and rooms—economy and refinement should go together; the method of economy is called "taking each matter on its own terms."
- 出处: 《浮生六记》卷二·闲情记趣
- 关键概念: 省俭而雅洁 | 就事论事 | 竹头木屑皆有用 | 逐件设法 | 贫士语境
- 领域: 生活治理/俭雅经营（Household Economy / Refinement under Constraint）｜层级: 核心｜优先级: 4
- 步骤:
  - 立双标准：省俭而雅洁，缺一不可
  - 观实况：逐件看清器皿房舍的实际条件
  - 逐件设法：给每样物事找最省而仍雅的实现法
  - 复用到物：以「竹头木屑皆有用」处理余料与旧物
- 典型案例:
  - 卷二提出省俭之法（双约束的起点）：「贫士起居服食以及器皿房舍，宜省俭而雅洁，省俭之法曰“就事论事”。」——卷二（W8@3599）
  - 同段以「竹头木屑皆有用」总括此法：「此“就事论事”之一法也。以此推之，古人所谓竹头木屑皆有用，良有以也。」——卷二（W8@3922）——同段前后即载其实例（梅花盒、竹帘代栏等，见素材包 §三 usage 登记）。
- 现代应用: 约束条件下的设计思维（节俭创新/jugaad） | 家居整理的逐件处置法 | 预算有限时的「省俭而雅洁」双目标 | 旧物再用：竹头木屑皆有用
- 关联模式: M-SHF-005
- 类目: 方法论通用（归一值）｜category_raw: 生活治理·约束下的雅洁（原值留证）｜legacy_mode_id: （无——全新码，无旧号）
- 核验: status=pending｜method=phase21r9-shenfu-rebuild-landing｜引文与出处未独立核验（evidence 原文见第九节）

### M-SHF-005 布衣菜饭法 (Plain Cloth and Simple Fare Method)

- 定义: 以「布衣菜饭，可乐终身」为幸福命题：理想生活不在远游功名，而在共同劳动与相守——图景是卜筑同居、绕屋菜园、植瓜蔬以供薪水，「君画我绣」以为诗酒之需；「不必作远游计」是把功名从幸福公式里减掉。命题出自夫妻对话，非普适宣言；此后「知己沦亡」的浩叹又为它加上悼亡的重量——亮与痛同框。
- 原文: 君画我绣，以为诗酒之需。布衣菜饭，可乐终身，不必作远游计也。
  > You paint and I will embroider, so as to pay for our verse and wine. In plain cloth and simple fare we can be happy all our lives—there is no need to plan distant journeys.
- 出处: 《浮生六记》卷一·闺房记乐（芸语；兼及林语堂评语转引）
- 关键概念: 布衣菜饭，可乐终身 | 君画我绣 | 卜筑菜园 | 不必作远游计 | 知己沦亡
- 领域: 幸福观/价值选择（View of Happiness / Choice of Values）｜层级: 核心｜优先级: 5
- 步骤:
  - 立愿景：卜筑同居、绕屋菜园（买绕屋菜园十亩）
  - 定凭依：共同劳动——君画我绣、植瓜蔬以供薪水
  - 做减法：把远游功名从幸福方程中删去（不必作远游计）
  - 承重量：后来「知己沦亡」，命题转为悼亡之叹（亮与痛同框）
- 典型案例:
  - 卷一·芸语中的生活图景（卜筑、菜园、植瓜蔬）：「他年当与君卜筑于此，买绕屋菜园十亩，课仆妪植瓜蔬，以供薪水。」——卷一（芸语，W8@4970）
  - 全篇命名的两句：君画我绣与布衣菜饭（幸福命题）：「君画我绣，以为诗酒之需。布衣菜饭，可乐终身，不必作远游计也。」——卷一（W8@4996）
  - 同篇的追忆之叹（命题的悼亡重量）：「余深然之。今即得有境地，而知己沦亡，可胜浩叹！」——卷一（W8@5021）
  - 林语堂评陈芸（转引层：中译版本多样，英文原文未成证）：「（芸）是中国文学中所记的女子中最为可爱的一个」——林语堂（转引：W16@509 区）
  - 林语堂评其容貌（转引层；与一手「唯两齿微露」呼应）：「虽非西施面目，并且前齿微露，我却觉得是中国第一美人」——林语堂（转引：W16@530 区；「前齿微露」与一手「唯两齿微露」呼应，W8 卷一@458）
- 现代应用: 减法生活：幸福的最小方案 | 以日常性为价值锚（可乐终身） | 共同劳动作为关系的基础 | 理想与易逝：亮与痛一并呈现
- 关联模式: M-SHF-007 | M-SHF-003
- 类目: 伦理修养（归一值）｜category_raw: 幸福观·价值选择（原值留证）｜legacy_mode_id: （无——全新码，无旧号）
- 核验: status=pending｜method=phase21r9-shenfu-rebuild-landing｜引文与出处未独立核验（evidence 原文见第九节）

### M-SHF-006 情之所钟法 (Where Affection Settles Method)

- 定义: 偏好不必服从「理」：作者以「始恶而终好之，理之不可解也」承认情感转变无法论证；芸以「情之所钟，虽丑不嫌」给出以情为尺的取舍原则——所钟爱者不因外形之「丑」被裁掉。它是对物、对人的一种态度资源：情感的强度可以覆盖外形的标准；但边界在于它不是无条件的包容律。
- 原文: 余曰：“始恶而终好之，理之不可解也。”芸曰：“情之所钟，虽丑不嫌。”
  > I said, "To hate a thing at first and come to love it in the end—that is what reason cannot explain." Yun said, "Where affection settles, even ugliness is not minded."
- 出处: 《浮生六记》卷一·闺房记乐
- 关键概念: 始恶而终好之 | 理之不可解 | 情之所钟 | 虽丑不嫌 | 以情为尺
- 领域: 情感判断/审美偏好（Affective Judgment / Aesthetic Preference）｜层级: 核心｜优先级: 6
- 步骤:
  - 觉察：注意到偏好从「始恶」到「终好」的转变
  - 承认不可解：不以「理」强求解释
  - 以情为尺：对所钟之物/人，不以外形之丑裁掉
  - 守边界：勿引申为无条件包容（对象含物/人，属态度资源）
- 典型案例:
  - 卷一问答：以情为尺的取舍原则：「余曰：“始恶而终好之，理之不可解也。”芸曰：“情之所钟，虽丑不嫌。”」——卷一（W8@3955）——出自芸语对「丑」的接纳，勿无限引申。
- 现代应用: 审美主观性的合法性 | 「心证」式偏好的自我理解 | 与侘寂式「丑学」的相通 | 关系中从外形标准到情感标准的转移
- 关联模式: M-SHF-003
- 类目: 心理洞察（归一值）｜category_raw: 情感判断·审美偏好（原值留证）｜legacy_mode_id: （无——全新码，无旧号）
- 核验: status=pending｜method=phase21r9-shenfu-rebuild-landing｜引文与出处未独立核验（evidence 原文见第九节）

### M-SHF-007 知己同心法 (One Heart with a Kindred Spirit Method)

- 定义: 夫妻以「同癖好、同耳目」的知音结构相处：「其癖好与余同」，且能「察眼意，懂眉语」，「一举一动，示之以色」皆能会通；共享「化女为男」的游历想象与「来世」之约；作者以「具男子之襟怀才识」评芸。同时附反例：卷三末提醒「恩爱夫妻不到头」——同一关系在现实重压下走向悼亡，不可读作无冲突的童话。
- 原文: 其癖好与余同，且能察眼意，懂眉语，一举一动，示之以色，无不头头是道。
  > Her tastes were the same as mine, and she could read the meaning in my eyes and understand the words of my brows; in every movement, shown but by a glance, there was nothing she did not fully grasp.
- 出处: 《浮生六记》卷一·闺房记乐（兼及卷三·坎坷记愁反例）
- 关键概念: 同癖好 | 察眼意，懂眉语 | 化女为男 | 来世 | 恩爱夫妻不到头
- 领域: 亲密关系/伙伴结构（Intimate Partnership / Companionship）｜层级: 核心｜优先级: 7
- 步骤:
  - 同癖好：建立共同趣味与共同语言
  - 通暗码：察眼意、懂眉语（非语言的相互读取）
  - 共想象：化女为男之游、来世相从之约
  - 并置反例：以「恩爱夫妻不到头」标示同一关系的现实极限
- 典型案例:
  - 卷一：知音结构的定义句（同癖好、察眼意懂眉语）：「其癖好与余同，且能察眼意，懂眉语，一举一动，示之以色，无不头头是道。」——卷一（W8@4150）
  - 卷一：共享的游历想象（化女为男）：「惜卿雌而伏，苟能化女为男，相与访名山，搜胜迹，遨游天下，不亦快哉！」——卷一（W8@4181）
  - 卷一：来世之约：「来世卿当作男，我为女子相从。」——卷一（W8@4270）
  - 同段：今生与来世的并置（不昧今生）：「必得不昧今生，方觉有情趣。」——卷一（W8@4284）
  - 卷三：作者对芸的评价（知己的重量）：「芸一女流，具男子之襟怀才识。」——卷三（W8@4716）——「女扮男装」等属清代语境，引用勿简单套用。
  - 卷三末尾反例：恩爱夫妻不到头（同卡附反例）：「奉劝世间夫妇，固不可彼此相仇，亦不可过于情笃。话云“恩爱夫妻不到头”，如余者，可作前车之鉴也。」——卷三（反例，W8@4789）——家变、贫困、离散俱在（卷三），不可读作无冲突童话。
- 现代应用: 平等伙伴关系的早期样本 | 「知己」作为亲密关系的度量 | 共享想象与约定对关系的维护 | 以反例承认关系的现实极限
- 关联模式: M-SHF-005 | M-SHF-008
- 类目: 伦理修养（归一值）｜category_raw: 亲密关系·伙伴关系（原值留证）｜legacy_mode_id: （无——全新码，无旧号）
- 核验: status=pending｜method=phase21r9-shenfu-rebuild-landing｜引文与出处未独立核验（evidence 原文见第九节）

### M-SHF-008 坎坷自省法 (Self-Reflection in Adversity Method)

- 定义: 对命运不公，作者的处置是性格自省——「多情重诺，爽直不羁，转因之为累」：把坎坷中的自我因素找出来，而非只归咎外部。同时冷静记录世情规则（「处家人情，非钱不行」），以反语引痛（「女子无才便是德」一句须按反语与语境读），并把判断落为行动（「因易儒为贾」）。自省不等于自罪：悲悯与批判并存。
- 原文: 人生坎坷何为乎来哉？往往皆自作孽耳，余则非也，多情重诺，爽直不羁，转因之为累。
  > Whence come the hardships of a life? Often they are self-made—but not with me: I was too full of feeling, too ready to make promises, too frank and unbridled; and these very traits became my burden.
- 出处: 《浮生六记》卷三·坎坷记愁（兼及卷四·浪游记快）
- 关键概念: 多情重诺，爽直不羁 | 转因之为累 | 处家人情，非钱不行 | 易儒为贾 | 反语
- 领域: 自我认知/逆境归因（Self-Knowledge / Attributing Adversity）｜层级: 核心｜优先级: 8
- 步骤:
  - 归因：从境遇中先找出自我因素（多情重诺，爽直不羁）
  - 实录世情：把「非钱不行」这类规则照实写下
  - 反语处置：不可直言之痛以反语引之（并标反语）
  - 落实行动：把判断变成转向（易儒为贾）
- 典型案例:
  - 卷三开篇：自省式归因（多情重诺，爽直不羁）：「人生坎坷何为乎来哉？往往皆自作孽耳，余则非也，多情重诺，爽直不羁，转因之为累。」——卷三·坎坷记愁开篇（W8@33）
  - 同卷：冷静记录世情规则（非钱不行）：「处家人情，非钱不行。」——卷三（W8@131）
  - 同卷：反语引痛（须按反语与语境读）：「“女子无才便是德”，真千古至言也！」——卷三（反语，W8@151）
  - 卷四：把判断落为行动（易儒为贾）：「余自绩溪之游，见热闹场中卑鄙之状不堪入目，因易儒为贾。」——卷四（W8@4032）
- 现代应用: 把「性格」作为境遇变量复盘 | 逆境叙事中的自我归因尺度 | 反语的阅读伦理：时代局限须标注 | 从自省到行动：易儒为贾式转向
- 关联模式: M-SHF-007
- 类目: 心理洞察（归一值）｜category_raw: 自我认知·逆境归因（原值留证）｜legacy_mode_id: （无——全新码，无旧号）
- 核验: status=pending｜method=phase21r9-shenfu-rebuild-landing｜引文与出处未独立核验（evidence 原文见第九节）

### M-SHF-009 得画意法 (Attaining the Pictorial Idea Method)

- 定义: 插花盆景以「会心者得画意」为标尺：能不能得「画意」，全看会心；并戒「匠气」——「若留枝盘如宝塔，扎枝曲如蚯蚓者，便成匠气矣」；「小景可以入画，大景可以入神」；审美原则最终落在具体手艺（点缀盆中花石、作活花屏等做法）。判据在会心，成事在做法：标准不能停在趣味，必须落成可复制的工序。
- 原文: 全在会心者得画意乃可。
  > It all depends on whether the one whose heart understands can attain the pictorial idea.
- 出处: 《浮生六记》卷二·闲情记趣（兼及潘麐生序）
- 关键概念: 会心者得画意 | 匠气 | 小景可以入画，大景可以入神 | 点缀盆中花石 | 活花屏
- 领域: 审美经营/技艺（Aesthetic Cultivation / Craft）｜层级: 核心｜优先级: 9
- 步骤:
  - 立标尺：以「会心者得画意」为验收标准
  - 戒匠气：拒绝宝塔式、蚯蚓式的机械盘扎
  - 分景处置：小景入画、大景入神
  - 落手艺：把标准做成具体做法（点缀盆中花石、作活花屏）
- 典型案例:
  - 卷二：全篇的验收标尺（会心得画意）：「全在会心者得画意乃可。」——卷二（W8@793）
  - 同卷：去匠气的判例（宝塔式、蚯蚓式）：「若留枝盘如宝塔，扎枝曲如蚯蚓者，便成匠气矣。」——卷二（W8@1297）
  - 同卷：大小二景的分级口径（通行本口径；底本作异文，双注登记）：「点缀盆中花石，小景可以入画，大景可以入神。」——卷二（通行本口径：W27@270；维基文库底本作「邪可以入画」（W8@1322），差异登记见 §八）——底本作「邪可以入画」（W8），本引从通行本（W27），异文裁定见素材包 §八.1。
  - 潘麐生序诗句（序文层；与卷二「活花屏」技艺互文）：「移春槛是活花屏。」——潘麐生序中诗句（W18@893 区；与卷二「活花屏」技艺互文）
  - 卷二：活花屏的做法实例：「乡居院旷，夏日逼人，劳教其家，作活花屏法甚妙。」——卷二（W8@2924 区）
- 现代应用: 审美判断力→可操作的手艺 | 去匠气的当代设计语言 | 园艺/盆景中的画意标准 | 建立个人审美工序：会心必须落到做法
- 关联模式: M-SHF-002
- 类目: 文艺审美（归一值）｜category_raw: 审美经营·技艺（原值留证）｜legacy_mode_id: （无——全新码，无旧号）
- 核验: status=pending｜method=phase21r9-shenfu-rebuild-landing｜引文与出处未独立核验（evidence 原文见第九节）

### M-SHF-010 浪游心得法 (Insight Gained in Wandering Method)

- 定义: 以「游幕三十年」的行走为样本：随人征逐（「轮蹄征逐，处处随人」）使山水变成「云烟过眼」，只能「领略其大概」而「不能探僻寻幽」——这是一句遗憾，不是宣言；名胜的得失在「心得」（与 M-SHF-003 呼应）；并以具体场面演示观照瞬间——「冒雪登楼」时的琼花飞舞与江上小艇的颠簸，直到「名利之心至此一冷」。游的价值不在到过，而在心得。
- 原文: 惜乎轮蹄征逐，处处随人，山水怡情，云烟过眼，不道领略其大概，不能探僻寻幽也。
  > A pity that, driven on by wheel and hoof, everywhere following others, I took the joy of hills and waters as clouds and smoke passing before the eyes—I cannot claim to have grasped even the general outline, nor to have sought out the hidden and secluded spots.
- 出处: 《浮生六记》卷四·浪游记快
- 关键概念: 轮蹄征逐 | 云烟过眼 | 探僻寻幽 | 心得 | 观照瞬间
- 领域: 观察方法/行旅（Method of Observation / Travel）｜层级: 核心｜优先级: 10
- 步骤:
  - 看清游的模式：轮蹄征逐，处处随人
  - 承认遗憾：只领略大概、不能探僻寻幽（遗憾句，非宣言）
  - 改换标尺：名胜所在，贵乎心得
  - 记录观照瞬间：把冒雪登楼、名利之心一冷写成场面
- 典型案例:
  - 卷四：行走模式的遗憾句（随人征逐、云烟过眼）：「惜乎轮蹄征逐，处处随人，山水怡情，云烟过眼，不道领略其大概，不能探僻寻幽也。」——卷四（W8@57）
  - 同卷：观照瞬间之一（冒雪登楼，琼花飞舞）：「余与琢堂冒雪登焉，俯视长空，琼花飞舞，遥指银山玉树，恍如身在瑶台。」——卷四（W8@10368）——琢堂同游段可与素材包 §四.3 交游表互见。
  - 同卷：观照瞬间之二（江上小艇，名利之心至此一冷）：「江中往来小艇，纵横掀播，如浪卷残叶，名利之心至此一冷。」——卷四（W8@10396）
- 现代应用: 旅行与观照的关系 | 「云烟过眼」式遗憾的正当性 | 观察笔记：把瞬间写成场面 | 职业流动中的在地观看
- 关联模式: M-SHF-003 | M-SHF-001
- 类目: 方法论通用（归一值）｜category_raw: 观察方法·行旅（原值留证）｜legacy_mode_id: （无——全新码，无旧号）
- 核验: status=pending｜method=phase21r9-shenfu-rebuild-landing｜引文与出处未独立核验（evidence 原文见第九节）

## 四、现代场景应用 (C-SHF-001 ~ C-SHF-010)

### C-SHF-001 / C-SHF-001E - 实录真情法

- **C-SHF-001**: 实录真情法的当代应用场景：日记与自我民族志写作的先声；「如实」作为修辞策略本身；自媒体写作：以真实经验对抗过度修辞；家庭口述史与私人记忆的整理方法。
- 应用领域: 日记与自我民族志写作的先声 / 「如实」作为修辞策略本身 / 自媒体写作：以真实经验对抗过度修辞 / 家庭口述史与私人记忆的整理方法
- **C-SHF-001E**: Contemporary applications of Recording True Facts and Real Feelings Method: A forerunner of diary writing and auto-ethnography; "Truthfulness" itself as a rhetorical strategy; Self-media writing: real experience against over-ornament; Methods for family oral history and the ordering of private memory.
- 应用领域（EN）: A forerunner of diary writing and auto-ethnography / "Truthfulness" itself as a rhetorical strategy / Self-media writing: real experience against over-ornament / Methods for family oral history and the ordering of private memory

### C-SHF-002 / C-SHF-002E - 物外之趣法

- **C-SHF-002**: 物外之趣法的当代应用场景：想象力训练：把平凡素材重译为景观；自然教育：从细察纹理开始；儿童美育：识别并保护童稚的观看方式；注意力如何创造世界（「心之所向，则或千或百」）。
- 应用领域: 想象力训练：把平凡素材重译为景观 / 自然教育：从细察纹理开始 / 儿童美育：识别并保护童稚的观看方式 / 注意力如何创造世界（「心之所向，则或千或百」）
- **C-SHF-002E**: Contemporary applications of Delight Beyond Things Method: Training the imagination: re-translating ordinary material into a scene; Nature education: it begins with closely examining texture; Children's aesthetic education: recognize and protect the boyhood way of seeing; How attention creates a world ("where the mind inclines, one sees a thousand or a hundred").
- 应用领域（EN）: Training the imagination: re-translating ordinary material into a scene / Nature education: it begins with closely examining texture / Children's aesthetic education: recognize and protect the boyhood way of seeing / How attention creates a world ("where the mind inclines, one sees a thousand or a hundred")

### C-SHF-003 / C-SHF-003E - 独出己见法

- **C-SHF-003**: 独出己见法的当代应用场景：反打卡式审美：不以热度定优劣；判断标准的内化与自证；小众趣味的自我辩护与再发现；用阅历为独立判断兜底。
- 应用领域: 反打卡式审美：不以热度定优劣 / 判断标准的内化与自证 / 小众趣味的自我辩护与再发现 / 用阅历为独立判断兜底
- **C-SHF-003E**: Contemporary applications of Independent Judgment Method: Against check-in aesthetics: worth is not set by popularity; Internalizing and self-verifying one's standard of judgment; Self-defense and rediscovery of minority tastes; Letting experience underwrite independent judgment.
- 应用领域（EN）: Against check-in aesthetics: worth is not set by popularity / Internalizing and self-verifying one's standard of judgment / Self-defense and rediscovery of minority tastes / Letting experience underwrite independent judgment

### C-SHF-004 / C-SHF-004E - 就事论事法

- **C-SHF-004**: 就事论事法的当代应用场景：约束条件下的设计思维（节俭创新/jugaad）；家居整理的逐件处置法；预算有限时的「省俭而雅洁」双目标；旧物再用：竹头木屑皆有用。
- 应用领域: 约束条件下的设计思维（节俭创新/jugaad） / 家居整理的逐件处置法 / 预算有限时的「省俭而雅洁」双目标 / 旧物再用：竹头木屑皆有用
- **C-SHF-004E**: Contemporary applications of Each Matter on Its Own Terms Method: Design thinking under constraints (frugal innovation / jugaad); Item-by-item handling in home organization; The twin goals of economy and refinement on a tight budget; Reusing old objects: bamboo ends and wood shavings are all useful.
- 应用领域（EN）: Design thinking under constraints (frugal innovation / jugaad) / Item-by-item handling in home organization / The twin goals of economy and refinement on a tight budget / Reusing old objects: bamboo ends and wood shavings are all useful

### C-SHF-005 / C-SHF-005E - 布衣菜饭法

- **C-SHF-005**: 布衣菜饭法的当代应用场景：减法生活：幸福的最小方案；以日常性为价值锚（可乐终身）；共同劳动作为关系的基础；理想与易逝：亮与痛一并呈现。
- 应用领域: 减法生活：幸福的最小方案 / 以日常性为价值锚（可乐终身） / 共同劳动作为关系的基础 / 理想与易逝：亮与痛一并呈现
- **C-SHF-005E**: Contemporary applications of Plain Cloth and Simple Fare Method: The minimal plan of a good life: subtractive living; Anchoring value in the everyday ("happy all our lives"); Shared labor as the ground of a relationship; Ideals and their fragility: brightness and pain shown together.
- 应用领域（EN）: The minimal plan of a good life: subtractive living / Anchoring value in the everyday ("happy all our lives") / Shared labor as the ground of a relationship / Ideals and their fragility: brightness and pain shown together

### C-SHF-006 / C-SHF-006E - 情之所钟法

- **C-SHF-006**: 情之所钟法的当代应用场景：审美主观性的合法性；「心证」式偏好的自我理解；与侘寂式「丑学」的相通；关系中从外形标准到情感标准的转移。
- 应用领域: 审美主观性的合法性 / 「心证」式偏好的自我理解 / 与侘寂式「丑学」的相通 / 关系中从外形标准到情感标准的转移
- **C-SHF-006E**: Contemporary applications of Where Affection Settles Method: The legitimacy of aesthetic subjectivity; Self-understanding of preferences held "by inner warrant"; Its affinity with wabi-sabi aesthetics of imperfection; Moving from standards of appearance to standards of feeling in relationships.
- 应用领域（EN）: The legitimacy of aesthetic subjectivity / Self-understanding of preferences held "by inner warrant" / Its affinity with wabi-sabi aesthetics of imperfection / Moving from standards of appearance to standards of feeling in relationships

### C-SHF-007 / C-SHF-007E - 知己同心法

- **C-SHF-007**: 知己同心法的当代应用场景：平等伙伴关系的早期样本；「知己」作为亲密关系的度量；共享想象与约定对关系的维护；以反例承认关系的现实极限。
- 应用领域: 平等伙伴关系的早期样本 / 「知己」作为亲密关系的度量 / 共享想象与约定对关系的维护 / 以反例承认关系的现实极限
- **C-SHF-007E**: Contemporary applications of One Heart with a Kindred Spirit Method: An early sample of egalitarian partnership; "Kindred spirit" as a measure of intimacy; Sustaining a bond through shared imaginings and vows; Admitting a bond's real limits through its counter-example.
- 应用领域（EN）: An early sample of egalitarian partnership / "Kindred spirit" as a measure of intimacy / Sustaining a bond through shared imaginings and vows / Admitting a bond's real limits through its counter-example

### C-SHF-008 / C-SHF-008E - 坎坷自省法

- **C-SHF-008**: 坎坷自省法的当代应用场景：把「性格」作为境遇变量复盘；逆境叙事中的自我归因尺度；反语的阅读伦理：时代局限须标注；从自省到行动：易儒为贾式转向。
- 应用领域: 把「性格」作为境遇变量复盘 / 逆境叙事中的自我归因尺度 / 反语的阅读伦理：时代局限须标注 / 从自省到行动：易儒为贾式转向
- **C-SHF-008E**: Contemporary applications of Self-Reflection in Adversity Method: Reviewing "character" as a variable of circumstance; The measure of self-attribution in narratives of adversity; An ethics of reading irony: mark the limits of the age; From reflection to action: the scholar-to-trader turn.
- 应用领域（EN）: Reviewing "character" as a variable of circumstance / The measure of self-attribution in narratives of adversity / An ethics of reading irony: mark the limits of the age / From reflection to action: the scholar-to-trader turn

### C-SHF-009 / C-SHF-009E - 得画意法

- **C-SHF-009**: 得画意法的当代应用场景：审美判断力→可操作的手艺；去匠气的当代设计语言；园艺/盆景中的画意标准；建立个人审美工序：会心必须落到做法。
- 应用领域: 审美判断力→可操作的手艺 / 去匠气的当代设计语言 / 园艺/盆景中的画意标准 / 建立个人审美工序：会心必须落到做法
- **C-SHF-009E**: Contemporary applications of Attaining the Pictorial Idea Method: Aesthetic judgment into operable craft; A contemporary design language free of mannerism; The standard of pictorial idea in gardening and bonsai; Build a personal aesthetic procedure: understanding must land in doing.
- 应用领域（EN）: Aesthetic judgment into operable craft / A contemporary design language free of mannerism / The standard of pictorial idea in gardening and bonsai / Build a personal aesthetic procedure: understanding must land in doing

### C-SHF-010 / C-SHF-010E - 浪游心得法

- **C-SHF-010**: 浪游心得法的当代应用场景：旅行与观照的关系；「云烟过眼」式遗憾的正当性；观察笔记：把瞬间写成场面；职业流动中的在地观看。
- 应用领域: 旅行与观照的关系 / 「云烟过眼」式遗憾的正当性 / 观察笔记：把瞬间写成场面 / 职业流动中的在地观看
- **C-SHF-010E**: Contemporary applications of Insight Gained in Wandering Method: The relation between travel and contemplation; The legitimacy of "clouds and smoke passing by" regret; Observation notes: writing the moment as a scene; Seeing locally amid professional mobility.
- 应用领域（EN）: The relation between travel and contemplation / The legitimacy of "clouds and smoke passing by" regret / Observation notes: writing the moment as a scene / Seeing locally amid professional mobility

## 五、现代应用

- 实录真情法——日记与自我民族志写作的先声
- 实录真情法——「如实」作为修辞策略本身
- 实录真情法——自媒体写作：以真实经验对抗过度修辞
- 实录真情法——家庭口述史与私人记忆的整理方法
- 物外之趣法——想象力训练：把平凡素材重译为景观
- 物外之趣法——自然教育：从细察纹理开始
- 物外之趣法——儿童美育：识别并保护童稚的观看方式
- 物外之趣法——注意力如何创造世界（「心之所向，则或千或百」）
- 独出己见法——反打卡式审美：不以热度定优劣
- 独出己见法——判断标准的内化与自证
- 独出己见法——小众趣味的自我辩护与再发现
- 独出己见法——用阅历为独立判断兜底
- 就事论事法——约束条件下的设计思维（节俭创新/jugaad）
- 就事论事法——家居整理的逐件处置法
- 就事论事法——预算有限时的「省俭而雅洁」双目标
- 就事论事法——旧物再用：竹头木屑皆有用
- 布衣菜饭法——减法生活：幸福的最小方案
- 布衣菜饭法——以日常性为价值锚（可乐终身）
- 布衣菜饭法——共同劳动作为关系的基础
- 布衣菜饭法——理想与易逝：亮与痛一并呈现
- 情之所钟法——审美主观性的合法性
- 情之所钟法——「心证」式偏好的自我理解
- 情之所钟法——与侘寂式「丑学」的相通
- 情之所钟法——关系中从外形标准到情感标准的转移
- 知己同心法——平等伙伴关系的早期样本
- 知己同心法——「知己」作为亲密关系的度量
- 知己同心法——共享想象与约定对关系的维护
- 知己同心法——以反例承认关系的现实极限
- 坎坷自省法——把「性格」作为境遇变量复盘
- 坎坷自省法——逆境叙事中的自我归因尺度
- 坎坷自省法——反语的阅读伦理：时代局限须标注
- 坎坷自省法——从自省到行动：易儒为贾式转向
- 得画意法——审美判断力→可操作的手艺
- 得画意法——去匠气的当代设计语言
- 得画意法——园艺/盆景中的画意标准
- 得画意法——建立个人审美工序：会心必须落到做法
- 浪游心得法——旅行与观照的关系
- 浪游心得法——「云烟过眼」式遗憾的正当性
- 浪游心得法——观察笔记：把瞬间写成场面
- 浪游心得法——职业流动中的在地观看

## 六、跨引用

- H-MT-001 (comparison): 徐霞客为晚明旅行考察家（其档属行旅—考察一系）；沈复卷四浪游记快同写行旅，一为探险考察之游、一为幕职流动之游——两档在行旅与观察方法的意义上可作对照阅读（具体比对另行立卡）。
- H-JST-001 (comparison): 金圣叹为明末清初的文学批评家（其档含小说戏曲评点与文人生活题材）；沈复《浮生六记》以日常生活入文——两档在文人生活书写的意义上可作对照阅读（具体比对另行立卡）。
- H-SU-001 (comparison): 苏轼（东坡）「事如春梦了无痕」句为《浮生六记》卷一开篇所援引，是其记录动因的出发句；两档在以文字安顿人生经验的意义上可作对照阅读（具体比对另行立卡）。

（对照登记: 本件图档 `cross_references` 与 `code_maps` 同名条目逐字全等（3/3 条），本节采 `code_maps` 口径。）

## 七、标签

自传文学、浮生六记、生活美学、布衣菜饭、陈芸、闺房记乐、闲情记趣、坎坷记愁、浪游记快、幕僚、苏州、沧浪亭、梅逸、三白、物外之趣、画意、活花屏、伪续事件、清中叶

## 八、独特成就

《浮生六记》以「布衣菜饭，可乐终身」等段落成为近现代流传最广的古典生活文本之一：俞平伯 1923/24 年作《重刊序》推重其文体；陈寅恪《元白诗笺证稿》以《闺房记乐》为例外创作（转引）；林语堂评语（转引层，英文原文未成证）与教材选文《兒時記趣》（原文即卷二童趣段）共同扩大其影响；1935 年世界书局《美化文学名著丛刊》「足本」托出后二记伪作（伪续事件，见素材包 §八.12/§八.14）；英法德俄等多语译本行世（W29），使其进入世界文学流通。

## 九、QA 验收记录

- 登记链: 见头部（R9 重做全链: 深度研究 → 重建落盘 → 合并入主库 → QA 独立验收 → 文档归档；各段卡号/执行者/提交号与报告路径齐备；QA 段含 1 项闭合热修（发布仓补镜像链产物 2 件，提交 54df4c4）；本卡（归档段）镜像与 push 回执见归档报告第七节与 kanban 卡回执（快照以 git 实测为准）。
- 核验口径（诚实登记）: 本件 10/10 条 `verification.status=pending`；evidence 明写素材包逐字口径；0 条自称 verified，核验另立卡。
- 逐条 evidence（去重后 10 条）:
  - （1 条）引文逐字取自 SHF-1 素材包（§三 quotes；同前（W8@116））；核验 pending，入库前须走独立核验流程
  - （1 条）引文逐字取自 SHF-1 素材包（§三 quotes；卷二·闲情记趣开篇（W8@33））；核验 pending，入库前须走独立核验流程
  - （1 条）引文逐字取自 SHF-1 素材包（§三 quotes；卷四·浪游记快（W8@89；句接「余游幕三十年来」段））；核验 pending，入库前须走独立核验流程
  - （1 条）引文逐字取自 SHF-1 素材包（§三 quotes；卷二（W8@3599））；核验 pending，入库前须走独立核验流程
  - （1 条）引文逐字取自 SHF-1 素材包（§三 quotes；卷一（W8@4996））；核验 pending，入库前须走独立核验流程
  - （1 条）引文逐字取自 SHF-1 素材包（§三 quotes；卷一（W8@3955））；核验 pending，入库前须走独立核验流程
  - （1 条）引文逐字取自 SHF-1 素材包（§三 quotes；卷一（W8@4150））；核验 pending，入库前须走独立核验流程
  - （1 条）引文逐字取自 SHF-1 素材包（§三 quotes；卷三·坎坷记愁开篇（W8@33））；核验 pending，入库前须走独立核验流程
  - （1 条）引文逐字取自 SHF-1 素材包（§三 quotes；卷二（W8@793））；核验 pending，入库前须走独立核验流程
  - （1 条）引文逐字取自 SHF-1 素材包（§三 quotes；卷四（W8@57））；核验 pending，入库前须走独立核验流程
- 独立核验与 QA（照实登记）: 落盘卡第二实现 `verify_phase21r9_shenfu.py` 74 PASS / 0 FAIL；合并卡独立核验 `verify_phase21r9_shenfu_merge_indep.py` 53 PASS / 0 FAIL；QA 卡第二实现 `verify_shenfu_qa_espinosa.py` 终轮 **75 PASS / 0 FAIL / 5 INFO**（80 行断言；判据全部重回原始取证；修复前 E01/E02 FAIL 留痕 `evidence_before_fix.json`；判据校准 v1.1 前后两轮全量留痕）。
- QA 闭合修复记录（照实登记）: 发布仓缺链自身产物 2 件（`docs/research/phase21r9_shenfu_sourcing_report.json` / `.md`，parity MISSING_IN_PUBLISH x2）；以 QA 闭合热修补镜像，提交 **54df4c4**（byte-exact）；修复后链集合 83/83、parity 链面 0 命中。
- 残留与观察项（如实登记）: parity 终轮 53 条，沈复链面 0 命中——16 条为 QA 产物（提交/镜像后消除）、37 条为他卡在制（W8 Stage2 批1／W4／W6、W10 文档／tools）；X01、X02 链自有脚本白名单漂移（73/1、51/2，非数据缺陷；本卡不扩展白名单，按观察项登记）；docs/index.md 存量行「283 位人物…2848 条」为前像同文、非本链引入；H-BG-001→H-HAN-001 悬空互引已由 R8 卡 t_8183b8fd 清除（0 残留）。
- 红线与口径（历史语境照实登记；同图档 caveats 8 条）:
  - 卷五、卷六红线: 现传《中山记历》《养生记道》系伪续，任何题材不得采其文本；《海国记》（钱泳《记事珠》辑本）与琉球之行作疑似史料单列。
  - 卒年失考口径: `death_year=null`；注记「约 1808 年以后在世，下限不明」（俞平伯/胡不归口径）；网络无源卒说（年份异说）、错籍表述与「名复」方志说等一律不采。
  - 「名复」并注: 属行世名；杨引传序（1877）明言「名则已逸」；最早书面痕迹《水绘园图》款「三白沈复」（真伪曾有争论，属疑似），引用须并注。
  - 转引层标注: 林语堂评语（英文原文未成证）、陈寅恪引文（以学术源为准）、俞平伯序、胡不归年谱小引等保留转引链，未升格为沈复原文。
  - 用字异文双注: M-SHF-009「小景可以入画」（维基文库底本作「邪可以入画」）；「秋侵人影瘦，霜染菊花肥」与管诗引「秋深人瘦菊花肥」两式各归出处。
  - 描述性标签声明: school / intellectual_tradition / core_thoughts 为依素材包主题池归纳的描述性标签（非当事人自认学派）；cross_references 三条为对照阅读框架（具体比对另行立卡）。
  - 图像素材: 未获可靠画像，不使用；藏画《水绘园图册》与题款为确证（转录本），其真伪之争与「作幕如皋十余年」说按素材包登记。
- 缺项登记（按现状保真，未补写）: 图档 `key_positions` 为空（按现状保真）；图档 `birth_place` 为空（按现状保真）；图档 `primary_language` 为空（按现状保真）；图档 `civilization_sphere` 为空（按现状保真）；图档 `death_year` 为空（按现状保真；头部按素材包口径注记卒年失考）。
- 口径备注: 第二节 取自 `core_thoughts`（本件无 `unique_thinking`）；第四节 场景 `text` 为合并卡按模板逐字复算（QA D 组 10 条复算命中）；第六节 图档与 `code_maps` 同名条目逐字全等；敏感表述（本件涉卷五六伪续与卒年失考）按史料表述保留原文并加注 caveats，不作价值判断（评估报告口径）。
- 归档时点计数台账（canonical, md 与报告互证）: modes=3311; total=3311; code_maps=216; scenarios_zh=2213; scenarios_en=2213; scenario_tags=7538; figure_names=1085
- 归档动作（本卡）: R7 核名裁定旧件（虚名空壳、无存世文献依据）维持归档、不唤醒、不改名、不迁载荷（旧模式码段零复用）；此前无在册旧页；本页由 `build_shf_r9_archive.py`（幂等，内置逐字断言）首次装配，文档层独立验收 `verify_shf_r9_archive.py`（第二实现＋反向注入自检）；本卡交付（照实登记）: 页、报告、证据三件提交与发布仓镜像回执见归档报告第七节；双仓 parity 与发布面复核快照记于归档报告第六节（精确 SHA 以 git 实测为准）。
