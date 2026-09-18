# 思维模式知识体系审计+精简方案

<!-- markdownlint-disable MD029 -->
<!-- 本文件的优先级/步骤清单跨标题连续编号（如 P0=1-3、P1 从 4 起），编号即排序信息，
     重新编号会丢失内容。MD029 对其它文件照常生效；口径见 docs/ci/markdown_lint_policy.md。 -->


> **生成日期**：2026-07-11
> **审计范围**：docs/ 目录下全部 51 个 .md 文件 + 本体系/ 目录
> **总存储占用**：~4.1MB
> **核心目标**：合并重叠、统一格式、提炼价值、保留5个核心文件（每个≤50KB）+ 附录体系

---

## 一、审计发现：文件全景与重叠分析

### 1.1 文件总量统计

| 类别 | 文件数 | 总大小 | 代表文件 |
|------|--------|--------|---------|
| 核心方法论 | 1 | 32KB | ultimate_thinking_methods_handbook.md |
| 问题诊断/选择 | 3 | 118KB | selector(42KB), decision_tree(34KB), quick_start(11KB) |
| 错题/体检/日志 | 3 | 89KB | mistake_book(45KB), health_check(26KB), journal(17KB) |
| 训练计划 | 2 | 125KB | daily(57KB), weekly(68KB) |
| 对比/矩阵/词典 | 3 | 83KB | comparison_matrix(42KB), bilingual(44KB), dictionary(7KB) |
| 应用/教练/案例 | 4 | 220KB | user_manual(92KB), coach_guide(48KB), case_library(74KB), game(63KB) |
| 跨领域扩展 | 7 | 238KB | cross_domain_expansion v1-v7 |
| 历史人物分析 | 18 | 844KB | maozedong系列(412KB), four_writers(24KB), world_communist(18KB), linbiao系列(36KB), ccp系列(20KB), huqiaomu系列(35KB) |
| 技能指南/更新 | 2 | 20KB | skills_usage_guide(7KB), update_guide(12KB) |
| 知识库目录 | 2 | 11KB | README + quick_reference |

**总计：51个文件，~4.1MB**

### 1.2 重叠内容矩阵

| 重叠组 | 涉及文件 | 重叠程度 | 说明 |
|--------|---------|---------|------|
| **A. 问题诊断工具** | selector.md, decision_tree.md, quick_start.md, user_manual.md(前3章) | 🔴 高度重叠 | selector和decision_tree使用完全相同的4个问题诊断框架(A1X/P等编码体系)，内容几乎逐字重复。quick_start是selector的精简版。user_manual前3章也是诊断+使用指南。 |
| **B. 思维模式定义** | handbook.md, dictionary.md, comparison_matrix.md, bilingual.md, cross_domain_expansion v1-v7 | 🟡 中度重叠 | 同一批思维模式在不同文件中以不同格式重复定义。dictionary是最紧凑的表格版(7KB)，handbook是完整版(32KB)，matrix是评分版(42KB)，bilingual是中英双语版(44KB)。v1-v7跨域扩展中的经济学/心理学/工程学等模式与bilingual/dictionary高度重合。 |
| **C. 训练/游戏化** | daily_training.md, weekly_training.md, game.md | 🟡 中度重叠 | daily(57KB)和weekly(68KB)的训练题目有大量重复场景（持久战备考、农村包围城市插画师等案例完全一样）。game(63KB)将daily的内容包装成游戏关卡，本质是同一批练习的不同呈现。 |
| **D. 错题/体检/日志** | mistake_book.md, health_check.md, journal.md | 🟢 低度重叠 | 三者功能互补：mistake_book是模式误用记录，health_check是自测问卷，journal是应用日志。但mistake_book中部分案例与user_manual的"用了没效果"章节重复。 |
| **E. 教练/案例/对比** | coach_guide.md, case_library.md, four_writers_comparison.md | 🟢 低度重叠 | case_library(74KB)的50个案例与daily/weekly训练场景有30%重合。coach_guide的教练话术库与mistake_book的纠正方法有部分重叠。 |

### 1.3 核心发现

1. **selector.md 和 decision_tree.md 是同一内容的两种呈现**，诊断框架（4问编码体系）完全相同，推荐组合表高度重叠。**应合并**。
2. **cross_domain_expansion v1-v7** 中的思维模式定义与 dictionary.md、bilingual.md 高度重复，且v1-v7之间也有大量内容重叠（如经济学模式在v1和v2中重复出现）。**应合并为一个文件**。
3. **daily_training.md 和 weekly_training.md** 有30%+的题目场景完全重复，game.md 是 daily 的游戏化包装。**应精简合并**。
4. **maozedong系列**（412KB，8个文件）是最大的冗余源，同一人物分析被拆分成多个时间段版本，内容大量重复。
5. **user_manual.md**（92KB）是最大的单体文件，远超50KB限制，需要拆分或精简。

---

## 二、精简方案：5个核心文件 + 附录体系

### 2.1 5个核心文件（保留，每个≤50KB）

| # | 核心文件 | 目标大小 | 来源合并 | 说明 |
|---|---------|---------|---------|------|
| 1 | **core_methodology.md** | ≤30KB | handbook.md + dictionary.md + cross_domain合并 | 32种思维模式+10种写作技法的统一定义，每个模式包含：一句话、核心公式、操作步骤、适用场景、使用边界 |
| 2 | **problem_diagnosis.md** | ≤25KB | selector.md + decision_tree.md + quick_start.md | 统一的问题诊断工具：4问编码体系 + 20种场景推荐组合 + 操作步骤。去除重复的对照表 |
| 3 | **mistakes_and_growth.md** | ≤35KB | mistake_book.md + health_check.md + journal.md | 错题本+体检表+日志模板合一。保留错误类型分类、反面案例、纠正方法、自测问卷、日志模板 |
| 4 | **training_plan.md** | ≤40KB | daily_training.md + weekly_training.md + game.md | 统一训练计划：30天+8周+41关的精华版，去除重复场景，保留最具代表性的练习 |
| 5 | **cases_and_coaching.md** | ≤45KB | case_library.md + coach_guide.md + four_writers_comparison(精华) | 实战案例精选(20个) + 教练指南精华 + 四大笔杆子写作范式。去除重复案例 |

### 2.2 附录体系（保留原样，建立交叉引用）

#### 附录A：跨领域扩展参考

| 文件 | 处理方式 | 说明 |
|------|---------|------|
| cross_domain_expansion.md ~ v7.md | **合并为 1 个文件** `appendix_cross_domain.md` (~50KB) | 提取各扩展中独有的模式定义，去除与核心文件重复的内容 |
| world_communist_complete_spectrum.md | **保留**，移入附录 | 30人谱系，独立价值高 |
| world_communist_thinking_modes.md | **合并到谱系文件** | 补充材料 |
| world_communist_thinking_modes_supplement.md | **合并到谱系文件** | 补充材料 |

#### 附录B：历史人物深度分析

| 文件 | 处理方式 | 说明 |
|------|---------|------|
| maozedong_full_analysis.md | **保留**，移入附录 | 412KB最大文件，但内容独特 |
| maozedong_1940-1945_analysis.md | **合并**到 full_analysis | 时间段分析可整合 |
| maozedong_1946-1957_analysis.md | **合并**到 full_analysis | 时间段分析可整合 |
| maozedong_deep_analysis.md | **合并**到 full_analysis | 深度分析可整合 |
| maozedong_analysis_complete.md | **合并**到 full_analysis | 重复分析可整合 |
| maozedong_thinking_and_writing_style.md | **合并**到 full_analysis | 风格分析可整合 |
| maozedong_style_demo.md | **保留** | 风格演示，独立价值 |
| four_writers_comparison.md | **精华提取**到 core #5 | 写作范式移入cases_and_coaching |
| zhonggong_four_writers.md | **合并**到 four_writers | 重复内容 |
| linbiao_analysis.md + linbiao_analysis_complete.md | **合并**为 1 个文件 | 重复分析 |
| linbiao_style_demo.md | **保留** | 风格演示 |
| huqiaomu_deep_analysis.md + huqiaomu_thinking_and_writing_style.md | **合并**为 1 个文件 | 重复分析 |
| huqiaomu_biography.md | **保留** | 传记，独立价值 |
| ccp_leaders_thinking_modes.md | **保留**，移入附录 | 独立价值 |
| ccp_thinking_modes_extraction.md | **合并**到 ccp_leaders | 重复内容 |
| thinking_modes_methodology.md + thinking_modes_methodology_complete.md | **合并**为 1 个文件 | 重复内容 |
| thinking_mode_api.md | **保留**，移入附录 | API参考，独立价值 |
| thinking_mode_bilingual.md | **精华提取**，移入核心#1 | 中英对照定义并入core_methodology |
| thinking_skills_usage_guide.md | **合并**到 update_guide | 技能加载说明 |

#### 附录C：管理与维护

| 文件 | 处理方式 | 说明 |
|------|---------|------|
| thinking_knowledge_update_guide.md | **保留** | 更新迭代指南 |
| 本体系/README.md | **保留** | 知识库说明 |
| 本体系/quick_reference.md | **精华提取**到 core #2 | 快速检索表并入problem_diagnosis |
| thinking_mode_user_manual.md | **精华提取** | 拆分后内容分别并入核心#1和#3 |
| thinking_mode_coach_guide.md | **精华提取**到 core #5 | 教练指南精华 |
| thinking_mode_case_library.md | **精华提取**到 core #5 | 案例精选 |

---

## 三、统一格式标准

### 3.1 核心文件统一结构

所有5个核心文件遵循以下格式模板：

```markdown
# [文件标题]

> 一句话定位 | 版本 | 更新日期

---

## 目录
1. [章节1](#章节1)
2. [章节2](#章节2)
...

---

## [章节名]

### [子章节]

**一句话定位**：[核心要义，≤20字]

**核心公式**：`步骤A → 步骤B → 步骤C → 结果`

**操作步骤**：
1. 第一步说明
2. 第二步说明
3. 第三步说明

**适用场景**：场景1、场景2、场景3

**使用边界**：
- ✅ 适用：...
- 🚫 不适用：...

**交叉引用**：详见 `[相关核心文件](../文件名.md#章节)`
```

### 3.2 思维模式卡片统一格式

每个思维模式使用统一卡片格式：

| 字段 | 格式 | 示例 |
|------|------|------|
| 编号 | `#N` | `#1` |
| 名称 | 中文 | `矛盾分析法` |
| 一句话 | ≤20字 | `抓住主要矛盾，带动全局解决` |
| 核心公式 | 箭头链 | `识别矛盾→区分主次→解决关键→带动全局` |
| 操作步骤 | 编号列表 | 3-5步 |
| 适用场景 | 逗号分隔 | `复杂问题分析、战略决策、危机处理` |
| 使用边界 | ✅/🚫 对照 | `✅系统性问题 / 🚫紧急事件` |
| 常见误用 | 错误类型+纠正 | `🔴过度使用→限时间内输出行动` |

### 3.3 附录文件统一格式

```markdown
# [附录标题]

> 来源说明 | 最后更新

---

## 目录

---

## [章节]

[内容...]

---

**交叉引用**：相关内容见 `[核心文件](../核心文件名.md#章节)`
```

---

## 四、执行步骤

### Phase 1：合并重叠文件（预计2小时）

1. **合并 selector + decision_tree + quick_start → problem_diagnosis.md**
   - 保留4问编码体系和20种场景对照表
   - 删除重复的诊断流程说明
   - 整合quick_start的"3→10→60极速路径"为使用指南
   - 目标：≤25KB

2. **合并 cross_domain_expansion v1-v7 → appendix_cross_domain.md**
   - 提取v1-v7中所有独特模式定义
   - 去除与dictionary/bilingual重复的模式
   - 按领域分组（经济学、心理学、工程学、教育学、社会学、人工智能、法学）
   - 目标：≤50KB

3. **合并 maozedong 系列 → maozedong_full_analysis.md**
   - 按时间段整合分析内容
   - 保留风格演示文件独立
   - 目标：≤400KB（仍为大文件，但去重后显著减少）

4. **合并 linbiao/huqiaomu/ccp 系列**
   - 每人名下重复分析合并为1个文件
   - 保留风格演示/传记文件
   - 目标：每个名人≤50KB

### Phase 2：提炼5个核心文件（预计3小时）

5. **创建 core_methodology.md**（≤30KB）
   - 从 handbook.md 提取32种思维模式完整定义
   - 从 bilingual.md 提取中英双语对照
   - 从 dictionary.md 提取紧凑表格版
   - 从 cross_domain 提取领域模式定义
   - 统一格式为标准卡片
   - 从 user_manual 提取"什么时候用/什么时候不用"

6. **创建 problem_diagnosis.md**（≤25KB）
   - 从 selector/decision_tree 提取诊断流程
   - 从 quick_start 提取极速路径
   - 从 user_manual 提取急救指南
   - 统一格式

7. **创建 mistakes_and_growth.md**（≤35KB）
   - 从 mistake_book 提取错误类型分类和纠正方法
   - 从 health_check 提取20道自测题和计分规则
   - 从 journal 提取日志模板和月/年度报告格式
   - 统一格式

8. **创建 training_plan.md**（≤40KB）
   - 从 daily_training 提取30天精华（去重后约15天）
   - 从 weekly_training 提取8周框架
   - 从 game 提取41关挑战框架
   - 保留最具代表性的练习场景
   - 统一格式

9. **创建 cases_and_coaching.md**（≤45KB）
   - 从 case_library 精选20个最佳案例（每领域3-4个）
   - 从 coach_guide 提取教练角色定位、话术库、五步流程
   - 从 four_writers 提取四大写作范式精华
   - 统一格式

### Phase 3：建立交叉引用（预计1小时）

10. **在每个核心文件中添加交叉引用**
    - 每个思维模式卡片底部添加"详见附录X"
    - 每个章节顶部添加"相关：核心文件Y章节Z"
    - 创建统一的索引表

11. **更新 本体系/README.md**
    - 添加新的文件结构说明
    - 添加核心文件→附录文件的映射关系
    - 添加快速导航

12. **更新 thinking_knowledge_update_guide.md**
    - 添加精简后的维护流程
    - 添加核心文件更新规范

### Phase 4：清理与验证（预计1小时）

13. **标记待删除文件**
    - 列出所有已被合并/提取的文件
    - 备份后删除重复文件
    - 保留历史版本记录

14. **验证文件大小**
    - 确保5个核心文件均≤50KB
    - 确保附录文件结构清晰
    - 验证交叉引用链接可用

15. **生成最终文件清单**
    - 输出精简后的完整文件目录
    - 标注每个文件的用途和大小

---

## 五、精简前后对比

| 指标 | 精简前 | 精简后 | 变化 |
|------|--------|--------|------|
| 文件总数 | 51个 | ~25个 | ↓51% |
| 核心文件 | 分散在12+个文件中 | 5个统一文件 | 集中化 |
| 总存储 | ~4.1MB | ~2.8MB | ↓32% |
| 重叠内容 | 多处重复定义 | 统一标准卡片 | 消除 |
| 查找效率 | 需跨多个文件 | 5个核心文件覆盖 | 提升 |
| 维护成本 | 51个文件需维护 | 5个核心+附录 | ↓80% |

---

## 六、精简后文件结构

```
docs/
├── 【核心文件】（5个，每个≤50KB）
│   ├── core_methodology.md              ← 32种思维模式+10种写作技法（≤30KB）
│   ├── problem_diagnosis.md             ← 4问诊断+20场景推荐（≤25KB）
│   ├── mistakes_and_growth.md           ← 错题本+体检+日志（≤35KB）
│   ├── training_plan.md                 ← 30天+8周+41关训练（≤40KB）
│   └── cases_and_coaching.md            ← 案例+教练+写作范式（≤45KB）
│
├── 【附录A：跨领域扩展】
│   ├── appendix_cross_domain.md         ← v1-v7合并（≤50KB）
│   ├── world_communist_spectrum.md      ← 30人谱系
│   ├── thinking_mode_api.md             ← API参考
│   └── 本体系/         ← README + quick_ref
│
├── 【附录B：历史人物分析】
│   ├── maozedong_analysis.md            ← 整合后（≤200KB）
│   ├── maozedong_style_demo.md          ← 风格演示
│   ├── linbiao_analysis.md              ← 整合后（≤50KB）
│   ├── linbiao_style_demo.md            ← 风格演示
│   ├── huqiaomu_analysis.md             ← 整合后（≤50KB）
│   ├── huqiaomu_biography.md            ← 传记
│   ├── ccp_leaders_thinking_modes.md    ← CCP领导人思维
│   ├── four_writers_summary.md          ← 四大笔杆子精华
│   └── thinking_modes_methodology.md    ← 方法论汇总
│
├── 【附录C：管理与维护】
│   ├── thinking_knowledge_update_guide.md ← 更新指南
│   └── thinking_skills_usage_guide.md     ← 技能加载指南
│
└── 【待清理】（标记为已合并，备份后删除）
    ├── thinking_mode_selector.md         → merged into problem_diagnosis.md
    ├── thinking_mode_decision_tree.md    → merged into problem_diagnosis.md
    ├── thinking_mode_quick_start.md      → merged into problem_diagnosis.md
    ├── ultimate_thinking_methods_handbook.md → merged into core_methodology.md
    ├── thinking_mode_dictionary.md       → merged into core_methodology.md
    ├── thinking_mode_bilingual.md        → merged into core_methodology.md
    ├── thinking_mode_mistake_book.md     → merged into mistakes_and_growth.md
    ├── thinking_mode_health_check.md     → merged into mistakes_and_growth.md
    ├── thinking_mode_journal.md          → merged into mistakes_and_growth.md
    ├── daily_thinking_training.md        → merged into training_plan.md
    ├── weekly_thinking_training.md       → merged into training_plan.md
    ├── thinking_mode_game.md             → merged into training_plan.md
    ├── thinking_mode_case_library.md     → merged into cases_and_coaching.md
    ├── thinking_mode_coach_guide.md      → merged into cases_and_coaching.md
    ├── four_writers_comparison.md        → merged into cases_and_coaching.md
    ├── cross_domain_expansion*.md        → merged into appendix_cross_domain.md
    ├── thinking_mode_user_manual.md      → merged into core_methodology.md + mistakes_and_growth.md
    └── [maozedong/linbiao/huqiaomu/ccp系列重复文件]
```

---

## 七、核心价值提炼

### 7.1 五个核心文件各自不可替代的价值

| 核心文件 | 不可替代价值 | 使用场景 |
|---------|-------------|---------|
| **core_methodology.md** | 完整的思维模式定义库，统一格式，中英双语 | "我需要用哪种思维模式？" |
| **problem_diagnosis.md** | 快速定位问题的诊断工具，4问编码体系 | "我现在面临什么问题？" |
| **mistakes_and_growth.md** | 避免误用的错题本 + 自我体检 + 成长追踪 | "我用错了没有？我进步了吗？" |
| **training_plan.md** | 系统化的刻意练习路径 | "我怎么才能熟练掌握？" |
| **cases_and_coaching.md** | 真实案例验证 + 教练式引导 + 写作范式 | "别人怎么用？我怎么教别人？" |

### 7.2 附录体系的独立价值

| 附录类别 | 核心价值 |
|---------|---------|
| 跨领域扩展 | 补充核心文件未覆盖的领域模式（教育学、社会学、AI等） |
| 历史人物分析 | 深度案例研究，展示思维模式在历史人物身上的实际应用 |
| 管理与维护 | 确保知识体系持续更新的方法论 |

---

## 八、风险提示

1. **maozedong_full_analysis.md**（412KB）即使合并后仍远超50KB。建议：
   - 方案A：拆分为 `maozedong_analysis.md`（≤50KB精华版）+ `maozedong_archive/`（完整资料归档）
   - 方案B：保留为大文件但移至独立的 `archive/` 目录，不计入核心文件

2. **cross_domain_expansion v1-v7** 合并后可能超过50KB。建议：
   - 提取与核心文件重复的模式定义
   - 保留各扩展中独有的领域模式
   - 若仍超限，拆分为 `appendix_cross_domain_part1.md` 和 `part2.md`

3. **游戏化内容**（game.md）的独特价值在于趣味性，建议保留一个精简版游戏框架（≤10KB）作为附录，而非完全合并。

---

*审计完成日期：2026-07-11*
*下一步：执行Phase 1合并操作*
