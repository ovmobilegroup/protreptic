# 费孝通 (Fei Xiaotong, H-FXT-001) - Phase21-R6 复刻档案

本页为**只读档案**：由 `build_legacy20_r6_archive.py` 自 v6 载荷逐字装配（`data/figures/H-FXT-001.json` / `data/individuals/H-FXT-001_modes.json` / 主库 `data/modes_data.json` / 场景库 `data/scenarios_zh|en.json` / `data/code_maps.json`），未新增事实性内容；引文与出处未独立核验（核验另立卡）。
旧世代档案页（7,236 B，sha256 `c34602a4c85ffcd250e7c1029d5dab09320da01322f48928c521c35a84a0d4e6`）已按先例归档至 `data/figures/_duplicates/H-FXT-001_legacy_docs_page.md`（字节保全，未删）；本页取代其在站点文档层的展示。

**人物**: 费孝通（Fei Xiaotong）｜**生卒**: 1910-2005｜**时代**: Modern
**学派**: 中国社会学/人类学/差序格局理论
**代表作**: 《乡土中国》（1948年）｜《生育制度》（1947年）｜《中华民族多元一体格局》（1989年）｜《江村经济》（1939年）｜《乡土重建》（1948年）
**名言**: 各美其美，美人之美，美美与共，天下大同
**相关人物**: H-HZX-001

- code: H-FXT-001｜拼音: Fèi Xiàotōng｜生卒: 1910/2005｜时代: Modern｜模式计数: 10
- modes: M-FXT-001 ~ M-FXT-010（旧号 M341 ~ M350 重编；逐条对照见各模式 `legacy_mode_id`）
- 载荷: `data/figures/H-FXT-001.json`｜`data/individuals/H-FXT-001_modes.json`｜主库 `data/modes_data.json`（四面同体：图档内嵌 = 伴随包 = 主库，逐对象全等）
- 登记链（评估 → 落盘 → 合并 → QA → 归档）: `docs/research/legacy20_rev6_assessment.md`（卡 t_a060cd41, albo；提交 `ec8e5477`）→ 数据落盘**批2** `eb53a42f`（卡 t_2d5112c6, san-martin；收尾 `60a14a38`；报告 `docs/research/phase21r6_landing_batch2_report.md`）→ 合并入主库 `d0f1bb65`（卡 t_10089b19, barbosa；modes +100 纯追加 / code_maps 引用面重指 / 场景 +30+30 / 标签 +200）→ QA 独立验收 `5c3db0cd`（卡 t_cd63c892, espinosa；独立第二实现 `verify_legacy20_r6_qa_espinosa.py`，74 项断言 0 FAIL）→ 文档归档（卡 t_aad01d0e, pigafetta，本卡）
- 报告索引: 落盘 `docs/research/phase21r6_landing_batch2_report.md`｜合并 `docs/research/phase21r6_merge_report.md`｜QA `docs/qa/phase21r6_qa_report.md`｜归档 `docs/research/phase21r6_archive_report.md`｜评估 `docs/research/legacy20_rev6_assessment.md`
- 页面字段映射: 一←historical_significance｜二←unique_thinking｜三←individuals/H-FXT-001_modes.json（10 模式）｜四←scenarios_zh/en（C-FXT-001~010）｜五←modern_applications_zh｜六←code_maps.figures.H-FXT-001.cross_references｜七←tags｜八←influence｜九←QA/缺项/台账
- caveats（图档逐条）:
  - 旧世代载荷复刻落盘（样例基线沿用）；载荷内容未独立核验
  - key_quote 归属与 source_chapter 需逐条落源后方可 verified
  - 类目映射按样例（t_a060cd41）口径批量应用，属候选口径，待归并卡/船长确认
- 未展开字段（本页未逐条搬迁，按现状保真）: `figure_description`、`figure_description_en`

## 一、历史定位

费孝通（1910-2005），中国社会学家、人类学家，中国社会学和人类学的奠基人之一。他通过深入的农村田野调查，提出了'差序格局'与'中华民族多元一体格局'两大核心理论，构建了中国社会学的本土化理论框架。其代表作《乡土中国》和《江村经济》向世界输出了中国社会结构分析范式，将西方社会学理论与中国传统社会现实相结合，开创了中国社会学本土化的先河。费孝通一生关注农村发展、民族问题和区域经济学，晚年提出'文化自觉'概念，主张在全球化背景下重新认识自身文化的价值。

## 二、核心思想

（字段 `unique_thinking`，逐条搬迁）

- 差序格局理论
- 中华民族多元一体格局
- 乡土中国分析
- 实地调查研究法
- 文化自觉理论

## 三、十大思维模式 (M-FXT-001 ~ M-FXT-010)

### M-FXT-001 差序格局分析法 (Differential Mode Analysis Method)

- 定义: 运用差序格局理论分析中国传统社会结构，指出以己为中心、按亲疏远近向外推展的社会关系模式。费孝通在《乡土中国》中提出，中国传统社会不是团体格局，而是像石子投入水中形成的波纹式差序结构，每个人都是其社会影响圈的中心。
- 原文: 中国传统社会不是团体格局，而是差序格局。
  > Traditional Chinese society is not organized as groups but as differential mode.
- 出处: 《乡土中国》（1948年）
- 关键概念: 差序格局 | 波纹扩散 | 亲疏远近 | 自我中心 | 弹性边界
- 领域: 中国社会学理论（Chinese Sociological Theory）｜层级: 核心｜优先级: 1
- 步骤:
  - 识别社会网络中心节点：确定个人在社会关系中的核心位置
  - 绘制关系远近图谱：按亲疏远近划分社会关系层次
  - 分析资源分配的亲疏差异：理解人情社会的运作机制
  - 预测关系变动趋势：把握社会关系动态变化规律
- 典型案例:
  - 《乡土中国》：系统阐述差序格局理论，成为中国社会学经典
  - 江村经济研究：通过实地调查验证差序格局理论的实际应用
- 现代应用: （空）
- 关联模式: （空）
- 类目: 社会学（归一值）｜category_raw: 社会结构分析（原值留证）｜legacy_mode_id: M341
- 核验: status=pending｜method=legacy20-rev6-landing｜引文与出处未独立核验（evidence 原文见 §九）
- 缺项字段（源档即空，未补写）: `modern_applications_zh`、`modern_applications_en`

### M-FXT-002 多元一体格局理论 (Unity in Diversity Framework Theory)

- 定义: 提出中华民族多元一体格局理论，认为中国56个民族在历史长河中形成了'多元'与'一体'的辩证统一。各民族文化多样性是'多元'，中华民族共同体意识是'一体'。这一理论为多民族国家的认同建设提供了核心理论框架。
- 原文: 各美其美，美人之美，美美与共，天下大同。
  > Each culture's beauty, others' beauty, shared beauty together leads to universal harmony.
- 出处: 《中华民族多元一体格局》（1989年）
- 关键概念: 多元并存 | 一体认同 | 历史融合 | 文化多样性 | 共同体建设
- 领域: 中华民族理论（Chinese National Theory）｜层级: 核心｜优先级: 2
- 步骤:
  - 识别各民族文化的独特性：尊重和保护各民族的文化传统
  - 分析历史上民族交融的轨迹：理解中华民族形成的历史过程
  - 构建多元一体的认同框架：在多样性中寻求统一性
  - 制定兼顾差异与统一的区域政策：促进各民族共同发展
- 典型案例:
  - 《中华民族多元一体格局》：系统阐述56个民族的多元一体结构
  - 民族区域自治实践：为多民族国家治理提供理论支撑
- 现代应用: （空）
- 关联模式: （空）
- 类目: 政治治理（归一值）｜category_raw: 民族认同建构（原值留证）｜legacy_mode_id: M342
- 核验: status=pending｜method=legacy20-rev6-landing｜引文与出处未独立核验（evidence 原文见 §九）
- 缺项字段（源档即空，未补写）: `modern_applications_zh`、`modern_applications_en`

### M-FXT-003 乡土社会转型分析法 (Rural-Social Transformation Analysis Method)

- 定义: 从乡土社会的土地依附关系出发，分析中国农村向现代社会转型的内在动力与路径。费孝通认为乡土中国的核心特征是'贴着地皮生活'，土地是农民的根本依托。现代化进程中的农村转型需要在理解乡土文化逻辑的基础上推进。
- 原文: 现代化不是简单地用城市模式取代农村模式。
  > Modernization is not simply replacing rural models with urban models.
- 出处: 《乡土中国》《乡土重建》（1948年）
- 关键概念: 土地依附 | 乡土逻辑 | 渐进转型 | 文化延续 | 城乡协调
- 领域: 乡村发展理论（Rural Development Theory）｜层级: 核心｜优先级: 3
- 步骤:
  - 分析乡土社会的内在特征：理解传统农村的社会结构和文化特征
  - 识别现代化冲击下的文化断裂点：发现传统与现代的冲突
  - 设计渐进式转型方案：尊重乡土文化逻辑的现代化路径
  - 建立城乡协调的发展机制：避免简单照搬城市模式
- 典型案例:
  - 江村土地制度改革研究：探索符合中国国情的农村转型路径
  - 乡镇企业发展实践：验证农村工业化的可行性
- 现代应用: （空）
- 关联模式: （空）
- 类目: 经济商业（归一值）｜category_raw: 农村现代化（原值留证）｜legacy_mode_id: M343
- 核验: status=pending｜method=legacy20-rev6-landing｜引文与出处未独立核验（evidence 原文见 §九）
- 缺项字段（源档即空，未补写）: `modern_applications_zh`、`modern_applications_en`

### M-FXT-004 实地调查研究法 (Field Research Methodology)

- 定义: 开创中国社会学实地调查研究范式，强调'脚板底下出学问'。费孝通在江苏开弦弓村（江村）进行的长期田野调查，成为中国社会学实地研究的经典范例。该方法主张研究者必须深入实际生活场景，从直接观察和访谈中获取第一手资料。
- 原文: 脚板底下出学问，田野调查出真知。
  > Knowledge comes from walking the ground, truth emerges from field research.
- 出处: 《江村经济》（1939年）
- 关键概念: 实地深入 | 第一手资料 | 参与观察 | 长期跟踪 | 理论联系实际
- 领域: 社会学人类学（Sociology Anthropology）｜层级: 核心｜优先级: 4
- 步骤:
  - 选择具有代表性的研究场域：确定典型的研究对象和地点
  - 进行长期参与观察：深入生活实际，建立信任关系
  - 系统收集访谈与文献资料：多角度获取研究数据
  - 从实际数据中提炼理论：形成具有普遍意义的理论概念
- 典型案例:
  - 江村经济调查：通过长期田野调查获得第一手农村数据
  - 少数民族地区研究：将西方人类学理论应用于中国实际
- 现代应用: （空）
- 关联模式: （空）
- 类目: 科学方法（归一值）｜category_raw: 研究方法论（原值留证）｜legacy_mode_id: M344
- 核验: status=pending｜method=legacy20-rev6-landing｜引文与出处未独立核验（evidence 原文见 §九）
- 缺项字段（源档即空，未补写）: `modern_applications_zh`、`modern_applications_en`

### M-FXT-005 文化自觉理论 (Cultural Self-Awareness Theory)

- 定义: 晚年提出'文化自觉'概念，强调在全球化背景下重新认识自身文化的价值与局限。费孝通认为文化自觉不是文化复古，而是'各美其美，美人之美，美美与共，天下大同'——在认识自身文化的基础上，理解并尊重其他文化的价值。
- 原文: 文化自觉是当今时代发展的精神基础。
  > Cultural self-awareness is the spiritual foundation for contemporary development.
- 出处: 费孝通晚年系列论述
- 关键概念: 自我认知 | 文化反思 | 多元尊重 | 天下大同 | 文明对话
- 领域: 文化研究（Cultural Studies）｜层级: 核心｜优先级: 5
- 步骤:
  - 梳理本文化的历史脉络与核心价值：建立文化主体意识
  - 识别文化在现代社会中的挑战与机遇：反思传统文化的现代意义
  - 建立与其他文明的对话机制：促进不同文明间的交流互鉴
  - 在实践中探索文化创新：推动传统文化的创造性转化
- 典型案例:
  - 费孝通晚年文化自觉论述：系统阐述文化自觉的理论内涵
  - 跨文化交流实践：推动中西文化的深度对话
- 现代应用: （空）
- 关联模式: （空）
- 类目: 文艺审美（归一值）｜category_raw: 文化认同（原值留证）｜legacy_mode_id: M345
- 核验: status=pending｜method=legacy20-rev6-landing｜引文与出处未独立核验（evidence 原文见 §九）
- 缺项字段（源档即空，未补写）: `modern_applications_zh`、`modern_applications_en`

### M-FXT-006 社区综合研究法 (Comprehensive Community Study Method)

- 定义: 将社区作为完整的社会系统来研究，从微观到宏观层层展开分析。费孝通主张以具体社区为切入点，通过经济、社会、文化、政治等多维度综合分析，揭示中国农村社会的整体结构及其与外部世界的联系。
- 原文: 社区是社会的基本单位，也是社会研究的切入点。
  > Community is the basic unit of society and also the entry point for social research.
- 出处: 费孝通社区研究系列
- 关键概念: 系统思维 | 微观切入 | 多维分析 | 内外联系 | 整体把握
- 领域: 社区治理（Community Governance）｜层级: 应用｜优先级: 6
- 步骤:
  - 选择典型社区作为研究样本：确定具有代表性的研究对象
  - 从经济、社会、文化多维度展开调查：全面收集社区信息
  - 分析社区与外部环境的联系：理解社区发展的外部条件
  - 总结社区发展的一般规律：形成具有普遍意义的理论
- 典型案例:
  - 江村系列研究：建立从微观社区到宏观社会的分析框架
  - 小城镇研究：探索城乡结合部的发展模式
- 现代应用: （空）
- 关联模式: （空）
- 类目: 社会学（归一值）｜category_raw: 社区研究（原值留证）｜legacy_mode_id: M346
- 核验: status=pending｜method=legacy20-rev6-landing｜引文与出处未独立核验（evidence 原文见 §九）
- 缺项字段（源档即空，未补写）: `modern_applications_zh`、`modern_applications_en`

### M-FXT-007 区域协调发展法 (Regional Coordinated Development Method)

- 定义: 从地理经济学角度分析中国区域发展的不平衡性，提出小城镇建设作为城乡协调的中介机制。费孝通晚年关注中国区域发展差距问题，提出通过小城镇建设带动农村工业化，实现城乡协调发展。
- 原文: 小城镇大问题，小城镇大战略。
  > Small towns, big problems; small towns, big strategy.
- 出处: 费孝通区域发展论述
- 关键概念: 区域平衡 | 小城镇中介 | 城乡协调 | 农村工业化 | 梯度发展
- 领域: 区域经济学（Regional Economics）｜层级: 应用｜优先级: 7
- 步骤:
  - 识别区域发展的关键瓶颈：分析制约区域发展的主要因素
  - 规划小城镇的功能定位：确定小城镇在区域发展中的作用
  - 推动农村工业化与城镇化同步发展：促进城乡产业融合
  - 建立区域协调的政策机制：为区域发展提供制度保障
- 典型案例:
  - 苏南乡镇企业研究：探索农村工业化的发展路径
  - 区域协调发展实践：为区域政策制定提供理论支撑
- 现代应用: （空）
- 关联模式: （空）
- 类目: 经济商业（归一值）｜category_raw: 区域发展（原值留证）｜legacy_mode_id: M347
- 核验: status=pending｜method=legacy20-rev6-landing｜引文与出处未独立核验（evidence 原文见 §九）
- 缺项字段（源档即空，未补写）: `modern_applications_zh`、`modern_applications_en`

### M-FXT-008 民族政策综合评估法 (Comprehensive Ethnic Policy Assessment Method)

- 定义: 从民族学角度综合评估中国民族政策的理论与实践效果，提出在尊重文化多样性的基础上构建中华民族共同体。费孝通通过对西南少数民族的长期田野调查，形成了对民族政策效果的系统性评估框架。
- 原文: 各民族共同繁荣是民族政策的根本目标。
  > Common prosperity of all ethnic groups is the fundamental goal of ethnic policies.
- 出处: 费孝通民族研究
- 关键概念: 文化尊重 | 区域自治 | 共同体建设 | 平等发展 | 文化保护
- 领域: 民族学（Ethnology）｜层级: 应用｜优先级: 8
- 步骤:
  - 评估各民族文化的生存状况：了解民族文化的发展现状
  - 分析民族政策的实际效果：评价政策实施的实际影响
  - 识别文化保护与发展的关键问题：找出政策制定中的不足
  - 提出兼顾差异与统一的政策建议：完善民族政策体系
- 典型案例:
  - 西南少数民族社会历史调查：为民族政策制定提供实证基础
  - 民族区域自治制度评估：完善民族治理体系
- 现代应用: （空）
- 关联模式: （空）
- 类目: 政治治理（归一值）｜category_raw: 民族政策（原值留证）｜legacy_mode_id: M348
- 核验: status=pending｜method=legacy20-rev6-landing｜引文与出处未独立核验（evidence 原文见 §九）
- 缺项字段（源档即空，未补写）: `modern_applications_zh`、`modern_applications_en`

### M-FXT-009 知识生产田野转化法 (Field-to-Knowledge Production Method)

- 定义: 将田野调查获得的经验材料转化为理论知识的系统方法。费孝通主张从具体社会现象出发，通过科学的分析框架提炼出具有普遍意义的理论概念。其'差序格局''多元一体'等核心概念均源于田野调查的理论升华。
- 原文: 理论源于实践，又指导实践。
  > Theory originates from practice and guides practice.
- 出处: 费孝通学术方法论
- 关键概念: 从现象到本质 | 经验理论化 | 概念创造 | 实践检验 | 理论创新
- 领域: 社会科学方法论（Social Science Methodology）｜层级: 方法｜优先级: 9
- 步骤:
  - 深入田野获取经验材料：通过实地调查获得第一手资料
  - 从具体现象中发现理论问题：识别现象背后的理论意义
  - 提炼具有概括性的核心概念：形成具有普遍解释力的理论
  - 通过更多案例验证理论的适用性：检验理论的解释力
- 典型案例:
  - 差序格局概念提出：从江村调查中提炼出核心理论概念
  - 多元一体理论建构：从民族研究中形成系统理论框架
- 现代应用: （空）
- 关联模式: （空）
- 类目: 科学方法（归一值）｜category_raw: 知识生产（原值留证）｜legacy_mode_id: M349
- 核验: status=pending｜method=legacy20-rev6-landing｜引文与出处未独立核验（evidence 原文见 §九）
- 缺项字段（源档即空，未补写）: `modern_applications_zh`、`modern_applications_en`

### M-FXT-010 跨文化比较分析法 (Cross-Cultural Comparative Analysis Method)

- 定义: 将中国社会置于世界文明比较的视野中，通过中西社会结构对比揭示中国社会的独特性。费孝通早年留学英国伦敦大学，师从马林诺夫斯基学习功能主义人类学，回国后将西方理论框架与中国社会实际相结合，开创了中西比较社会学的先河。
- 原文: 中西结合，推陈出新。
  > Combine Chinese and Western, innovate from tradition.
- 出处: 费孝通比较研究
- 关键概念: 中西对比 | 文明对话 | 理论本土化 | 比较视野 | 理论创新
- 领域: 比较社会学（Comparative Sociology）｜层级: 方法｜优先级: 10
- 步骤:
  - 掌握西方理论框架的核心逻辑：理解西方理论的基础原理
  - 将其与中国社会实际进行对照分析：识别中西社会的异同
  - 识别中西社会的结构性差异：发现中国社会的独特性
  - 提炼具有普遍意义的理论贡献：为世界社会科学贡献中国智慧
- 典型案例:
  - 《江村经济》中西比较研究：成功运用西方理论分析中国农村
  - 功能主义人类学本土化：将西方理论框架与中国实际相结合
- 现代应用: （空）
- 关联模式: （空）
- 类目: 跨文化治理（归一值）｜category_raw: 跨文化研究（原值留证）｜legacy_mode_id: M350
- 核验: status=pending｜method=legacy20-rev6-landing｜引文与出处未独立核验（evidence 原文见 §九）
- 缺项字段（源档即空，未补写）: `modern_applications_zh`、`modern_applications_en`

## 四、现代场景应用 (C-FXT-001 ~ C-FXT-010)

（本件场景源档仅含标题——描述、关键概念、应用领域等字段空，按现状保真，未补写。）

### C-FXT-001 / C-FXT-001E - 差序格局——中国传统社会结构分析案例

### C-FXT-002 / C-FXT-002E - 多元一体——中华民族认同建构案例

### C-FXT-003 / C-FXT-003E - 乡土中国——从土地到社会转型分析案例

### C-FXT-004 / C-FXT-004E - 实地调查——从江村到乡村治理的方法论案例

### C-FXT-005 / C-FXT-005E - 文化自觉——全球化背景下的身份认同案例

### C-FXT-006 / C-FXT-006E - 社区研究——从微观到宏观的社会分析案例

### C-FXT-007 / C-FXT-007E - 区域发展——从沿海到内地的经济地理案例

### C-FXT-008 / C-FXT-008E - 民族政策——多元文化治理的理论与实践案例

### C-FXT-009 / C-FXT-009E - 知识生产——从田野到理论的学术建构案例

### C-FXT-010 / C-FXT-010E - 跨文化比较——东西方社会结构对比分析案例

## 五、现代应用

（缺项登记：10/10 条 `modern_applications_zh` 空（源档即空）——按现状保真，未补写。）

## 六、跨引用

- H-HZX-001 (methodology): 费孝通的实地调查方法与黄宗智的'过密化'理论形成互补：前者从社会结构角度分析乡村，后者从经济生产角度揭示内卷化问题。两者共同构成了理解中国农村问题的双重框架。

## 七、标签

社会学、人类学、差序格局、多元一体、乡土中国、江村经济、文化自觉、实地调查、民族研究、农村发展

## 八、独特成就

费孝通的社会学理论为中国农村改革、民族区域发展和文化政策制定提供了重要的理论基础。他的差序格局理论成为理解中国传统社会结构的核心分析工具，多元一体格局理论为多民族国家的认同建设提供了框架。其学术成果被广泛应用于社会学、人类学、民族学、公共政策等领域，对中国现代化进程产生了深远影响。

## 九、QA 验收记录

- 登记链: 见头部（评估 → 落盘 → 合并 → QA → 归档；各段卡号/执行者/提交号与报告路径齐备）。
- 核验口径（诚实登记）: 本件 10/10 条 `verification.status=pending`；evidence 明写「引文与出处未独立核验」；0 条自称 verified，核验另立卡。
- 逐条 evidence（去重后 1 条）:
  - （10 条）旧世代载荷复刻落盘（自样例基线沿用（仅 provenance 字段更新，内容未改））；引文与出处未独立核验，核验另立卡
- 缺项登记（按现状保真，未补写）: 模式级 `modern_applications_zh` 10/10 空（§三/现代应用）；模式级 `related_modes` 10/10 空（§三/关联模式）。
- 口径备注: §二 取自 `unique_thinking`（本件无 `core_thoughts`）；§八 取自 `influence`。
- 归档时点计数台账（canonical, md↔报告互证）: modes=3271; total=3162; code_maps=212; scenarios_zh=2183; scenarios_en=2183; scenario_tags=7478; figure_names=1083
- 归档动作（本卡）: 旧世代档案页（7,236 B，sha256 `c34602a4c85ffcd250e7c1029d5dab09320da01322f48928c521c35a84a0d4e6`）字节归档至 `data/figures/_duplicates/H-FXT-001_legacy_docs_page.md`（未删字节）；本页由 `build_legacy20_r6_archive.py`（幂等，内置逐字断言）生成，文档层独立验收 `verify_legacy20_r6_archive.py`（逐页断言全过，明细见归档报告 §三）。
