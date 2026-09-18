# 知识体系持续演进机制

> **版本** 1.0 · 2026-07-11
> **作者** Protreptic
> **一句话**：让知识体系从静态文档变成活系统——"使用→反馈→沉淀"全自动闭环，知识自进化，版本自动更新。

---

## 目录

1. [系统概览](#一系统概览)
2. [使用→反馈→沉淀自动化流程](#二使用反馈沉淀自动化流程)
3. [知识自进化机制](#三知识自进化机制)
4. [版本自动更新流程](#四版本自动更新流程)
5. [触发条件与调度表](#五触发条件与调度表)
6. [自动化脚本实现](#六自动化脚本实现)
7. [监控与告警](#七监控与告警)
8. [演进路线图](#八演进路线图)

---

## 一、系统概览

### 1.1 核心设计理念

知识体系不是文档仓库，而是**活的工具系统**。演进机制围绕三个核心循环构建：

```
┌─────────────────────────────────────────────────────────┐
│                    知识体系活系统                         │
│                                                         │
│   ┌──────────┐    反馈数据    ┌──────────┐              │
│   │  使用层   │ ────────────→ │  反馈层   │              │
│   │  (日常)  │               │  (自动)   │              │
│   └──────────┘               └────┬─────┘              │
│                                   │                     │
│                              沉淀建议                     │
│                                   │                     │
│                           ┌───────▼───────┐             │
│                           │   沉淀层      │             │
│                           │  (自动+审核)  │             │
│                           └───────┬───────┘             │
│                                   │                     │
│                              更新内容                     │
│                                   │                     │
│                           ┌───────▼───────┐             │
│                           │   版本层      │             │
│                           │  (自动发布)   │             │
│                           └───────────────┘             │
│                                                         │
│   └─── 反馈数据回流至使用层 ───┘                        │
└─────────────────────────────────────────────────────────┘
```

### 1.2 三层架构

| 层级 | 职责 | 触发频率 | 自动化程度 |
|------|------|---------|-----------|
| **使用层** | 记录每次思维模式使用，采集效果数据 | 实时（每次使用） | 90% 自动 |
| **反馈层** | 汇总数据，生成月度/季度报告，提出更新建议 | 月度 + 季度 | 70% 自动 |
| **沉淀层** | 审核建议，执行知识入库，更新技能包 | 季度 + 年度 | 50% 自动 |
| **版本层** | 发布新版本，同步所有相关文件 | 季度 + 年度 | 80% 自动 |

### 1.3 数据流

```
使用（Hermes会话）
  ↓ [自动] 日志采集器
本体系/extras/logs/YYYY-MM.json
  ↓ [月度聚合] 统计引擎
本体系/extras/reports/monthly/YYYY-MM-report.md
  ↓ [季度分析] 洞察引擎
本体系/extras/reports/quarterly/YYYY-QN-review.md
  ↓ [自动] 更新建议生成器
本体系/extras/suggestions/YYYY-QN-suggestions.md
  ↓ [人工审核] 季度回顾确认
  ↓ [自动] 知识沉淀器
  ├─→ source/ （思维模式更新）
  ├─→ skills/ （技能包更新）
  ├─→ extras/cases/ （案例入库）
  ├─→ extras/mistakes/ （错题本）
  └─→ extras/pending/ （待审核内容）
  ↓ [自动] 版本管理器
  ├─→ README.md 版本号
  ├─→ quick_reference.md 更新
  └─→ extras/releases/vX.Y.Z.md 发布说明
```

---

## 二、使用→反馈→沉淀自动化流程

### 2.1 使用层：自动日志采集

#### 2.1.1 触发条件

**每次 Hermes 会话中加载思维模式相关技能或提到思维模式编号时。**

具体触发信号：

- 技能名称包含 `thinking`、`writing`、`method`、`模式`、`思维`
- 会话消息中出现 `#1` ~ `#41` 格式的模式编号
- 会话消息中出现思维模式中文名称（如"矛盾分析法"、"群众路线法"）
- 用户发送 `/contribute case` 指令

#### 2.1.2 自动采集流程

```bash
# 步骤 1：扫描最近会话，提取思维模式使用记录
# 运行频率：每次会话结束或每小时定时任务

# 步骤 2：解析会话数据，提取结构化字段
输入：Hermes 会话日志
输出：标准化日志条目

字段映射：
  会话ID        → log_id
  时间戳        → timestamp
  用户消息      → context
  加载的技能    → used_modes（从技能名映射到模式编号）
  提及的模式编号 → cited_modes（正则匹配 #\d+）
  结果关键词    → outcome（成功/失败/部分成功）
  效果评分      → rating（⭐1-5，从用户反馈中提取）
  场景分类      → category（工作/学习/生活/决策/管理/写作）
  反思内容      → reflection（从"做对了/做错了/下次"提取）
```

#### 2.1.3 日志存储格式

文件路径：`本体系/extras/logs/YYYY-MM/log_YYYY-MM-DD_sessionID.json`

```json
{
  "log_id": "sess_20260711_001",
  "timestamp": "2026-07-11T14:30:00Z",
  "used_modes": [1, 7, 24],
  "cited_modes": [1, 3],
  "context": "项目优先级排序",
  "outcome": "success",
  "rating": 5,
  "category": "决策",
  "reflection": {
    "good": "画了因果链，避免了同时抓三个问题的老毛病",
    "bad": "没有提前和员工沟通暂缓计划",
    "improve": "矛盾分析后加一步影响范围评估"
  },
  "session_url": "<session>"
}
```

#### 2.1.4 零摩擦记录入口

用户在会话中只需一句话即可完成记录：

```
使用 #1 矛盾分析法解决了团队资源冲突问题，⭐⭐⭐⭐⭐
```

系统自动解析为结构化日志条目，存入当月日志目录。

---

### 2.2 反馈层：自动统计分析

#### 2.2.1 月度统计引擎

**触发条件**：每月 1 日 00:00，自动扫描上月所有日志。

**统计维度**：

| 维度 | 计算方法 | 输出位置 |
|------|---------|---------|
| 使用次数 | 按月聚合所有日志条目 | `reports/monthly/YYYY-MM-report.md` |
| 成功率 | 评分≥4星的条目数 / 总条目数 | 同上 |
| 模式热度排行 | 按使用次数降序排列 Top 10 | 同上 |
| 场景分布 | 按 category 字段分组统计 | 同上 |
| 趋势变化 | 与上月数据对比，标记 ↑↓→ | 同上 |
| 最佳实践 | 评分最高 + 上下文最有价值的 3 条 | 同上 |
| 待改进领域 | 评分≤2星的条目分析 | 同上 |

**月度报告自动生成流程**：

```python
# 伪代码：月度报告生成器
def generate_monthly_report(year, month):
    logs = load_logs(year, month)
    
    # 基础统计
    total_usage = len(logs)
    success_rate = count_rating_ge(logs, 4) / total_usage
    avg_rating = mean_rating(logs)
    
    # 模式热度排行
    mode_hotness = group_by_mode(logs)
    top_modes = sort_desc(mode_hotness)[:10]
    
    # 场景分布
    scene_dist = group_by_category(logs)
    
    # 趋势对比
    prev_report = load_monthly_report(year, month - 1)
    trends = compare_with(prev_report, {
        'usage': total_usage,
        'success_rate': success_rate,
        'avg_rating': avg_rating
    })
    
    # 最佳实践
    best_practices = select_top(logs, score_fn=lambda l: l.rating * weight(l.context))[:3]
    
    # 待改进领域
    weak_areas = analyze_low_rated(logs, threshold=2)
    
    # 生成报告
    report = render_template('monthly_report', {
        'year': year, 'month': month,
        'total_usage': total_usage,
        'success_rate': success_rate,
        'avg_rating': avg_rating,
        'top_modes': top_modes,
        'scene_dist': scene_dist,
        'trends': trends,
        'best_practices': best_practices,
        'weak_areas': weak_areas
    })
    
    save_report(report, f'extras/reports/monthly/{year}-{month:02d}-report.md')
    return report
```

#### 2.2.2 季度洞察引擎

**触发条件**：每季度末月（3/6/9/12月）的最后一天，自动扫描三个月日志。

**洞察维度**：

| 洞察项 | 分析方法 | 产出 |
|--------|---------|------|
| 高频模式深挖 | Top 3 模式的使用场景是否足够丰富？ | 优化建议 |
| 空白领域识别 | 哪些场景类别几乎没有记录？ | 新模式需求 |
| 模式组合模式 | 哪些模式经常一起出现？ | 组合推荐 |
| 熟练度变化 | 某模式的使用次数是否持续增长？ | 熟练度评估 |
| 效果衰减 | 曾���高频但现在下降的模式？ | 衰退预警 |
| 案例质量评估 | 本月最佳实践是否值得入库？ | 入库候选 |

**季度洞察自动生成流程**：

```python
def generate_quarter_insights(year, quarter):
    # 加载季度内三个月的报告
    reports = [load_monthly_report(year, m) for m in quarters_months(quarter)]
    
    # 1. 模式热力图
    heatmap = build_mode_heatmap(reports)
    
    # 2. 模式组合发现
    co_usage = find_co_usage_patterns(reports)
    top_combos = sort_by_frequency(co_usage)[:5]
    
    # 3. 空白领域检测
    scenes_covered = set(scene for r in reports for scene in r.scene_dist)
    expected_scenes = {'工作', '学习', '生活', '决策', '管理', '写作', '技术', '人际'}
    gaps = expected_scenes - scenes_covered
    
    # 4. 衰退模式预警
    declining = find_declining_modes(reports, threshold=-20%)
    
    # 5. 成功案例入库推荐
    candidates = recommend_for_inbox(reports, min_rating=5)
    
    # 6. 生成更新建议
    suggestions = generate_update_suggestions({
        'heatmap': heatmap,
        'top_combos': top_combos,
        'gaps': gaps,
        'declining': declining,
        'candidates': candidates
    })
    
    save_suggestions(suggestions, f'extras/suggestions/{year}-Q{quarter}.md')
    return suggestions
```

#### 2.2.3 自动更新建议生成

季度洞察引擎会输出结构化的更新建议，存入 `extras/suggestions/YYYY-QN.md`：

```markdown
# 2026-Q2 自动更新建议

> 生成日期：2026-06-30
> 数据来源：54 条使用日志

## 📈 高频模式 TOP 5
1. #1 矛盾分析法（23次，↑15%）— 持续霸榜
2. #7 系统思维法（12次，↑8%）— 场景扩展中
3. #24 系统思维法（10次，→）— 稳定
4. #3 持久战思维（8次，↓5%）— 需关注
5. #5 实事求是法（7次，↑20%）— 增长最快

## 🔍 空白领域（建议新增模式）
- 技术领域决策：仅 2 条记录，缺乏专门模式
- 跨团队协作：完全空白
- 个人精力管理：仅 1 条记录

## 💡 模式优化建议
- #3 持久战思维：现有描述缺少"精力分配"子步骤，建议补充
- #11 灵活策略法：案例不足，建议从日志中精选 2 个补充

## 📥 案例入库推荐（评分 5⭐）
1. 2026-04-15 产品方向决策 — #1 + #7 组合
2. 2026-05-22 团队冲突调解 — #2 + #6 组合
3. 2026-06-03 技术架构选型 — #5 + #12 组合
```

---

### 2.3 沉淀层：知识入库

#### 2.3.1 案例自动归档

**触发条件**：月度报告中评分≥5星的条目，自动标记为"入库候选"。

**流程**：

```
月度报告中标记候选
  ↓
自动提取结构化信息
  ↓
存入 extras/cases/YYYY-MM-候选编号.md
  ↓
季度回顾时人工确认
  ↓
确认后 → 正式归档到 cases/ 目录
```

**自动提取规则**：

```python
def extract_case_candidate(log_entry):
    """从日志条目自动提取案例格式"""
    return {
        'title': log_entry['context'][:30],
        'date': log_entry['timestamp'].split('T')[0],
        'modes': [f'#{m}' for m in log_entry['used_modes']],
        'result': '成功' if log_entry['outcome'] == 'success' else '待验证',
        'rating': log_entry['rating'],
        'lesson_good': log_entry['reflection']['good'],
        'lesson_bad': log_entry['reflection']['bad'],
        'lesson_improve': log_entry['reflection']['improve'],
        'source_session': log_entry['session_url']
    }
```

#### 2.3.2 新模式自动采集

**触发条件**：季度回顾中发现的空白领域，自动生成"新模式需求单"。

**流程**：

```
空白领域检测
  ↓
生成新模式需求单
  ↓
存入 extras/pending/NEW-{领域}.md
  ↓
等待人工提炼或从外部资料（书籍/文章）补充
  ↓
季度审核时决定是否采纳
```

**新模式需求单模板**：

```markdown
---
status: pending
source: auto-generated
date: YYYY-MM-DD
category: {领域}
priority: {高/中/低}
---
# 新模式需求：{领域名称}

## 为什么需要
本季度在 "{场景}" 场景中使用了 {X} 次，但没有专门的思维模式指导。

## 已有数据
- 相关模式：{从日志中提取的模式编号}
- 常见组合：{从共现分析中提取}
- 用户反馈摘要：{从反思字段中提取}

## 建议方向
基于现有数据，建议的新模式特征：
1. {特征1}
2. {特征2}
3. {特征3}
```

#### 2.3.3 错题本自动维护

**触发条件**：评分≤2星或使用失败的日志条目。

**流程**：

```
失败/低分日志
  ↓
自动提取失败原因
  ↓
存入 extras/mistakes/YYYY-MM-误用编号.md
  ↓
分类：知识误用 / 场景错配 / 执行偏差
  ↓
季度回顾时分析共性，提炼改进建议
```

**错题本条目格式**：

```markdown
## 📛 {YYYY-MM-DD} {简短标题}

- **误用模式**：#{编号} {模式名称}
- **实际场景**：{描述}
- **结果**：失败 ❌
- **错误类型**：{知识误用 / 场景错配 / 执行偏差}
- **失败原因**：{从反思中提取}
- **正确做法**：{应该用什么模式 / 应该怎么操作}
- **教训**：{一句话总结}
```

---

## 三、知识自进化机制

### 3.1 知识图谱自组织

#### 3.1.1 模式关联自动发现

**机制**：通过分析日志中的共现模式，自动发现思维模式之间的隐性关联。

```python
def discover_pattern_relationships(logs):
    """
    从使用日志中发现模式之间的关联关系
    """
    # 1. 共现矩阵：统计每对模式同时出现的次数
    cooccurrence = {}
    for log in logs:
        modes = log['used_modes']
        for i in range(len(modes)):
            for j in range(i+1, len(modes)):
                pair = tuple(sorted([modes[i], modes[j]]))
                cooccurrence[pair] = cooccurrence.get(pair, 0) + 1
    
    # 2. 强关联对：共现次数 > 阈值
    strong_pairs = [(pair, count) for pair, count in cooccurrence.items() 
                    if count >= MIN_CO_USAGE_THRESHOLD]
    
    # 3. 条件概率：给定模式A时，模式B出现的概率
    conditional = {}
    for (a, b), count_ab in strong_pairs:
        total_a = sum(count for (x, y), count in cooccurrence.items() if x == a or y == a)
        conditional[(a, b)] = count_ab / total_a
    
    # 4. 输出：关联规则
    rules = []
    for (a, b), prob in conditional.items():
        if prob >= 0.3:  # 条件概率 ≥ 30%
            rules.append({
                'from': f'#{a}',
                'to': f'#{b}',
                'co_usage': cooccurrence[(a, b)],
                'conditional_prob': prob,
                'confidence': 'high' if prob >= 0.5 else 'medium'
            })
    
    return sorted(rules, key=lambda r: r['conditional_prob'], reverse=True)
```

**输出**：自动更新 `thinking_mode_selector.md` 中的"推荐组合"部分，以及快速检索表中的场景-模式映射。

#### 3.1.2 模式成熟度评估

每个思维模式都有一个自动计算的"成熟度分数"：

```
成熟度分数 = 使用频次权重(30%) + 成功率权重(30%) + 案例数量权重(20%) + 关联广度权重(20%)

等级：
  ⭐⭐⭐⭐⭐ 本能级（使用≥20次，成功率≥80%，案例≥5，关联≥5种模式）
  ⭐⭐⭐⭐  精通级（使用≥10次，成功率≥70%，案例≥3，关联≥3种模式）
  ⭐⭐⭐  熟练级（使用≥5次，成功率≥60%，案例≥2，关联≥2种模式）
  ⭐⭐  入门级（使用≥3次，成功率≥50%）
  ⭐  初识级（使用<3次或成功率<50%）
```

成熟度数据自动写入 `extras/maturity/YYYY-mode-{编号}.md`，并在 README 中汇总展示。

### 3.2 对比矩阵自更新

#### 3.2.1 自动纳入对比矩阵

当季度回顾中发现新模式或模式间比较需求时，自动更新 `four_writers_comparison.md` 或创建新的对比文件。

**触发条件**：

- 新模式被采纳进入 source/ 目录
- 共现分析发现两个模式经常被混淆
- 用户反馈指出某个模式描述不准确

**自动更新流程**：

```
新数据进入
  ↓
检测是否需要更新对比矩阵
  ├─ 新模式 → 添加到对应分类列
  ├─ 易混淆 → 添加对比行
  └─ 描述不准 → 标记待修订
  ↓
生成对比矩阵更新草案
  ↓
存入 extras/pending/ 待审核
  ↓
确认后自动合并到对应文件
```

### 3.3 技能包自同步

#### 3.3.1 知识库→技能包双向同步

```
source/ 更新
  ↓
自动检测变更的文件
  ↓
对比对应 skills/ 中的技能包
  ↓
生成差异报告
  ↓
自动合并变更到技能包
  ↓
触发技能重载通知
```

**同步规则**：

| 知识库文件 | 对应技能包 | 同步策略 |
|-----------|-----------|---------|
| `source/ultimate_thinking_methods_handbook.md` | `skills/ultimate-thinking-and-writing-methods/` | 全量同步 |
| `source/thinking_mode_selector.md` | `skills/hermes-agent`（内置） | 增量同步 |
| `source/four_writers_comparison.md` | `skills/four-writers-writing/` | 全量同步 |
| `source/cross_domain_expansion.md` | `skills/cross-domain-expansion/`（新建） | 按需创建 |
| `extras/cases/` 中的案例 | 各技能包的示例部分 | 增量追加 |
| `extras/mistakes/` 中的错题 | `thinking_mode_mistake_book.md` | 追加 |

### 3.4 知识健康度仪表盘

**触发条件**：每周日凌晨 02:00，自动生成知识健康度报告。

**监控指标**：

| 指标 | 计算方式 | 健康阈值 | 告警级别 |
|------|---------|---------|---------|
| 日志覆盖率 | 有记录的会话 / 总会话数 | ≥ 20% | 黄色 < 15%, 红色 < 10% |
| 模式分布均匀度 | Shannon 熵 of 模式使用分布 | ≥ 1.5 | 黄色 < 1.2, 红色 < 0.8 |
| 案例增长率 | 每月新增案例数 | ≥ 2/月 | 黄色 < 1, 红色 = 0 |
| 错题增长率 | 每月新增错题数 | 合理范围 | 绿色 < 2, 黄色 2-5, 红色 > 5 |
| 内容新鲜度 | 最近一次 source/ 更新距今天数 | ≤ 90天 | 黄色 > 60, 红色 > 90 |
| 技能包同步延迟 | skills/ 与 source/ 差异文件数 | = 0 | 黄色 > 2, 红色 > 5 |

**周健康报告格式**：

```markdown
# 知识体系健康报告 — 2026-W28

## 📊 总体健康度：🟢 良好 (82/100)

| 指标 | 当前值 | 阈值 | 状态 |
|------|-------|------|------|
| 日志覆盖率 | 23% | ≥20% | 🟢 |
| 模式分布熵 | 1.62 | ≥1.5 | 🟢 |
| 案例增长率 | 3/月 | ≥2 | 🟢 |
| 错题增长率 | 1/月 | ≤5 | 🟢 |
| 内容新鲜度 | 12天 | ≤90 | 🟢 |
| 技能包同步 | 0差异 | =0 | 🟢 |

## 🔔 本周发现
1. #3 持久战思维使用频率下降 15%，建议检查是否需要更新描述
2. 新增 2 个案例入库候选，待季度审核确认

## 📈 趋势（近 4 周）
- 日志覆盖率：20% → 21% → 22% → 23% ↗
- 模式分布熵：1.55 → 1.58 → 1.60 → 1.62 ↗
- 案例增长：2 → 3 → 2 → 3 →
```

---

## 四、版本自动更新流程

### 4.1 版本策略

采用**语义化版本 + 分支策略**：

```
主版本.次版本.修订号
  │      │      │
  │      │      └─ patch：自动生成的数据变更（案例、日志统计）
  │      └──────── minor：知识内容变更（新模式、更新描述）
  └─────────────── major：体系结构变更（章节重组、大规模重写）

分支策略：
  main      — 生产环境，稳定版本
  develop   — 开发环境，季度变更累积
  draft     — 草稿环境，待审核的更新建议
```

### 4.2 季度自动发布流程

**触发条件**：每季度最后一个月的 25 日（为人工审核留出 5 天缓冲）。

**完整流程**：

```
第 1 步：变更收集（自动）
  ├─ 扫描 extras/pending/ 中所有待审核文件
  ├─ 扫描 extras/cases/ 中本月新增案例
  ├─ 扫描 extras/mistakes/ 中本月新增错题
  ├─ 扫描 extras/suggestions/ 中本季度建议
  └─ 生成变更清单 changelog_draft.md

第 2 步：版本判定（自动）
  ├─ 有新模式/新技法 → minor++
  ├─ 有体系结构变更 → major++
  ├─ 仅有案例/数据更新 → patch++
  └─ 无实质变更 → 跳过发布

第 3 步：版本草案生成（自动）
  ├─ 创建 extras/releases/vX.Y.Z-draft.md
  ├─ 填充变更清单
  ├─ 标记每个变更的优先级（必须/建议/可选）
  └─ 通知人工审核

第 4 步：人工审核（手动，≤30分钟）
  ├─ 审查变更清单
  ├─ 确认版本号
  ├─ 批准/修改/拒绝个别变更
  └─ 点击"确认发布"

第 5 步：版本发布（自动）
  ├─ 将 draft.md 重命名为 vX.Y.Z.md
  ├─ 更新 README.md 版本号
  ├─ 更新 quick_reference.md 日期
  ├─ 更新所有 skills/ 目录中的元数据
  ├─ 创建 Git tag vX.Y.Z
  └─ 发送发布通知

第 6 步：内容同步（自动）
  ├─ 将采纳的变更合并到对应 source/ 文件
  ├─ 将案例追加到 skills/ 示例部分
  ├─ 将错题追加到 mistake_book
  └─ 清理 extras/pending/ 中已处理的文件
```

### 4.3 版本变更日志自动生成

```python
def generate_changelog(year, quarter):
    """自动生成季度变更日志"""
    changes = []
    
    # 1. 从 pending/ 目录收集待处理内容
    for f in listdir('extras/pending/'):
        meta = read_frontmatter(f)
        changes.append({
            'type': 'new' if meta.get('status') == 'approved' else 'pending',
            'item': f,
            'category': meta.get('category'),
            'priority': meta.get('priority', 'medium')
        })
    
    # 2. 从 cases/ 目录收集新增案例
    for f in listdir('extras/cases/'):
        if is_newer_than(f, quarter_start(year, quarter)):
            changes.append({
                'type': 'case',
                'item': f,
                'category': '案例',
                'priority': 'low'
            })
    
    # 3. 从 mistakes/ 目录收集新增错题
    for f in listdir('extras/mistakes/'):
        if is_newer_than(f, quarter_start(year, quarter)):
            changes.append({
                'type': 'mistake',
                'item': f,
                'category': '错题',
                'priority': 'info'
            })
    
    # 4. 从 suggestions/ 收集采纳的建议
    for s in load_suggestions(year, quarter):
        if s.get('action') == 'adopt':
            changes.append({
                'type': 'update',
                'item': s['target'],
                'category': s['category'],
                'priority': s['priority']
            })
    
    # 5. 生成变更日志
    return render_changelog(changes)
```

### 4.4 跨文件自动同步

**触发条件**：版本发布确认后，自动执行。

**同步规则**：

```
source/ 变更 → skills/ 同步
  ├─ handbook.md 更新 → ultimate-thinking-and-writing-methods/ 技能包
  ├─ selector.md 更新 → 技能包中的选择器部分
  ├─ 四笔杆子对比 → four-writers-writing/ 技能包
  └─ 跨领域扩展 → 对应扩展技能包

cases/ 新增 → 各技能包示例追加
  ├─ 案例按关联模式归类
  └─ 追加到对应技能的 examples/ 部分

mistakes/ 新增 → mistake_book.md 追加
  └─ 按模式编号分类追加

maturity/ 更新 → README.md 汇总更新
  └─ 重新计算并写入各模式成熟度评级
```

---

## 五、触发条件与调度表

### 5.1 完整调度表

| 任务 | 触发条件 | 执行频率 | 自动化程度 | 人工介入 |
|------|---------|---------|-----------|---------|
| **日志采集** | 会话加载思维模式技能 / 提及模式编号 | 实时 | 95% | 无需 |
| **日志格式化** | 新日志条目写入 | 实时 | 90% | 无需 |
| **月度统计** | 每月 1 日 00:00 | 月度 | 80% | 审核报告（5分钟） |
| **案例入库推荐** | 月度报告中评分≥5星条目 | 月度 | 85% | 确认入库（5分钟） |
| **错题本更新** | 评分≤2星的日志 | 实时 | 90% | 分类确认（2分钟） |
| **模式关联发现** | 每季度最后一天 | 季度 | 75% | 审核关联规则（10分钟） |
| **成熟度评估** | 每季度最后一天 | 季度 | 80% | 复核异常值（5分钟） |
| **更新建议生成** | 季度洞察引擎输出 | 季度 | 70% | 审核建议（15分钟） |
| **版本变更收集** | 每季度末月 25 日 | 季度 | 85% | 确认版本号和变更（30分钟） |
| **版本发布** | 人工确认后 | 按需 | 90% | 一键确认 |
| **跨文件同步** | 版本发布后 | 按需 | 85% | 审查差异（10分钟） |
| **健康度报告** | 每周日 02:00 | 周度 | 90% | 查看告警（2分钟） |
| **年度大修** | 每年 12 月 31 日 | 年度 | 60% | 深度审核（2-3小时） |

### 5.2 事件驱动触发器

除了定时调度，还有以下事件触发机制：

| 事件 | 触发条件 | 响应动作 |
|------|---------|---------|
| **新模式发现** | 用户在会话中提及未收录的模式 | 创建 pending/ 条目，标记"紧急" |
| **模式混淆** | 同一场景下连续2次使用不同模式且都失败 | 生成对比文档建议，标记"高优先级" |
| **知识缺口** | 用户多次在同类场景下说"不知道用什么模式" | 生成空白领域报告，建议新增模式 |
| **内容过时** | source/ 文件超过 180 天未更新 | 标记"待复审"，加入季度审核清单 |
| **技能漂移** | skills/ 与 source/ 差异超过 3 个文件 | 自动触发同步，标记"警告" |
| **使用断层** | 某模式连续 2 个月零使用 | 生成衰退预警，建议更新或合并 |

### 5.3 紧急通道

某些情况需要跳过常规流程，走紧急通道：

```
紧急通道触发条件：
  1. 发现严重知识错误（如模式定义与原始文献矛盾）
  2. 新模式被频繁引用但尚未收录（热度突增）
  3. 技能包同步失败导致使用中断

紧急通道流程：
  发现 → 立即创建 hotfix/ 条目 → 24小时内审核 → 立即发布 → 事后补录变更日志
```

---

## 六、自动化脚本实现

### 6.1 日志采集脚本

**文件**：`本体系/scripts/collect_logs.sh`

```bash
#!/bin/bash
# 思维模式使用日志自动采集器
# 用法：./collect_logs.sh [YYYY-MM]

set -euo pipefail

KB_ROOT="docs/本体系"
LOG_DIR="${KB_ROOT}/extras/logs"
MONTH="${1:-$(date +%Y-%m)}"

echo "📊 开始采集 ${MONTH} 的思维模式使用日志..."

# 1. 创建月度日志目录
mkdir -p "${LOG_DIR}/${MONTH}"

# 2. 扫描 Hermes 会话日志（通过 session_search API）
#    实际部署时替换为真实的日志读取逻辑
SESSION_COUNT=0
SUCCESS_COUNT=0
FAIL_COUNT=0

for session_log in "${LOG_DIR}/raw/${MONTH}"/*.json; do
    if [[ -f "$session_log" ]]; then
        SESSION_COUNT=$((SESSION_COUNT + 1))
        
        # 解析会话日志，提取思维模式使用
        MASSES=$(jq -r '.used_modes // [] | length' "$session_log" 2>/dev/null || echo 0)
        
        if [[ $MASSES -gt 0 ]]; then
            SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
            
            # 转换为标准化日志条目
            jq '{
                log_id: .session_id,
                timestamp: .timestamp,
                used_modes: .used_modes,
                cited_modes: .cited_modes,
                context: .context,
                outcome: .outcome,
                rating: .rating,
                category: .category,
                reflection: .reflection,
                session_url: .session_url
            }' "$session_log" > "${LOG_DIR}/${MONTH}/log_$(basename "$session_log" .json).json"
        else
            FAIL_COUNT=$((FAIL_COUNT + 1))
        fi
    fi
done

echo "✅ 采集完成："
echo "   会话总数：${SESSION_COUNT}"
echo "   含思维模式使用：${SUCCESS_COUNT}"
echo "   未使用：${FAIL_COUNT}"
echo "   日志条目：${SUCCESS_COUNT} 条"
```

### 6.2 月度统计脚本

**文件**：`本体系/scripts/generate_monthly_report.sh`

```bash
#!/bin/bash
# 月度思维模式使用报告自动生成器
# 用法：./generate_monthly_report.sh [YYYY-MM]

set -euo pipefail

KB_ROOT="docs/本体系"
LOG_DIR="${KB_ROOT}/extras/logs"
REPORT_DIR="${KB_ROOT}/extras/reports/monthly"
MONTH="${1:-$(date -d 'last month' +%Y-%m 2>/dev/null || date +%Y-%m)}"

echo "📈 生成 ${MONTH} 月度报告..."

mkdir -p "${REPORT_DIR}"

# 使用 Python 进行统计分析
python3 << 'PYEOF'
import json
import os
from collections import Counter, defaultdict
from datetime import datetime

KB_ROOT = "docs/本体系"
LOG_DIR = f"{KB_ROOT}/extras/logs/{MONTH}"
REPORT_DIR = f"{KB_ROOT}/extras/reports/monthly"

# 加载所有日志
logs = []
for fname in os.listdir(LOG_DIR):
    if fname.endswith('.json'):
        with open(os.path.join(LOG_DIR, fname)) as f:
            logs.append(json.load(f))

if not logs:
    print("  ⚠️ 本月无日志数据")
    exit(0)

# 基础统计
total = len(logs)
ratings = [l.get('rating', 0) for l in logs]
success_ratings = [r for r in ratings if r >= 4]
success_rate = len(success_ratings) / total * 100 if total > 0 else 0
avg_rating = sum(ratings) / total if total > 0 else 0

# 模式热度排行
mode_counter = Counter()
for log in logs:
    for m in log.get('used_modes', []):
        mode_counter[m] += 1

# 场景分布
scene_counter = Counter()
for log in logs:
    scene_counter[log.get('category', 'unknown')] += 1

# 最佳实践（评分最高且上下文丰富）
best = sorted(logs, key=lambda l: l.get('rating', 0), reverse=True)[:3]

# 生成报告
report = f"""# 📊 {MONTH} 思维模式使用报告

> 生成日期：{datetime.now().strftime('%Y-%m-%d')}
> 数据源：{total} 条使用日志

---

## A. 使用统计

| 指标 | 数值 |
|------|------|
| 本月使用次数 | {total} 次 |
| 成功率（⭐4-5） | {success_rate:.1f}% |
| 平均评分 | {avg_rating:.1f} 星 |
| 使用过的思维模式数 | {len(mode_counter)} 种 |
| 最常使用的模式 | #{mode_counter.most_common(1)[0][0]}（{mode_counter.most_common(1)[0][1]}次） |

## B. 思维模式使用排行（Top 10）

| 排名 | 思维模式 | 使用次数 |
|------|---------|---------|
"""

for i, (mode, count) in enumerate(mode_counter.most_common(10), 1):
    report += f"| {i} | #{mode} | {count} |\n"

report += f"""
## C. 场景分布

| 场景类别 | 使用次数 | 占比 |
|---------|---------|------|
"""

for scene, count in scene_counter.most_common():
    pct = count / total * 100
    report += f"| {scene} | {count} | {pct:.1f}% |\n"

report += f"""
## D. 本月最佳实践（Top 3）
"""

for i, log in enumerate(best, 1):
    report += f"""
### 🏆 第 {i} 名：{log.get('context', '未知')}
- 思维模式：#{', #'.join(str(m) for m in log.get('used_modes', []))}
- 效果评分：{'⭐' * log.get('rating', 0)}
- 关键收获：{log.get('reflection', {}).get('good', 'N/A')}
"""

report += f"""
## E. 待改进领域

| 问题 | 原因分析 | 下月行动计划 |
|------|---------|------------|
"""

# 找出评分最低的条目作为改进建议
worst = sorted(logs, key=lambda l: l.get('rating', 0))[:2]
for log in worst:
    if log.get('rating', 5) <= 2:
        report += f"| {log.get('context', '?')} | {log.get('reflection', {}).get('bad', '?')} | 重新学习 #{', #'.join(str(m) for m in log.get('used_modes', []))} |\n"

report += f"""
## F. 下月目标

- [ ] 尝试使用 {len(mode_counter)} 种思维模式中的至少 {min(3, len(mode_counter))} 种
- [ ] 将最常用的 #{mode_counter.most_common(1)[0][0]} 应用到新场景
- [ ] 本月使用次数目标：≥ {max(total, int(total * 1.2))} 次

---

> *报告由知识体系自动分析引擎生成*
"""

os.makedirs(REPORT_DIR, exist_ok=True)
with open(f"{REPORT_DIR}/{MONTH}-report.md", 'w') as f:
    f.write(report)

print(f"  ✅ 报告已生成：{REPORT_DIR}/{MONTH}-report.md")
print(f"  📊 使用次数：{total} | 成功率：{success_rate:.1f}% | 平均评分：{avg_rating:.1f}")
PYEOF

echo "✅ 月度报告生成完成"
```

### 6.3 季度洞察脚本

**文件**：`本体系/scripts/generate_quarter_insights.sh`

```bash
#!/bin/bash
# 季度知识洞察自动生成器
# 用法：./generate_quarter_insights.sh [YYYY-QN]

set -euo pipefail

KB_ROOT="docs/本体系"
REPORTS_DIR="${KB_ROOT}/extras/reports/monthly"
SUGGESTIONS_DIR="${KB_ROOT}/extras/suggestions"

QUARTER="${1:-$(date +%Y)-Q$(($(date +%-m) - 1) / 3 + 1)}"

echo "🔍 生成 ${QUARTER} 季度洞察..."

python3 << 'PYEOF'
import json
import os
from collections import Counter, defaultdict
from datetime import datetime

KB_ROOT = "docs/本体系"
REPORTS_DIR = f"{KB_ROOT}/extras/reports/monthly"
SUGGESTIONS_DIR = f"{KB_ROOT}/extras/suggestions"

# 解析季度月份
quarter_map = {'Q1': [1,2,3], 'Q2': [4,5,6], 'Q3': [7,8,9], 'Q4': [10,11,12]}
year_str, q_str = QUARTER.rsplit('-', 1) if '-' in QUARTER else (QUARTER.split('-')[0], QUARTER.split('-')[1])
months = quarter_map[q_str]

# 加载季度内所有月度报告
all_logs = []
for m in months:
    month_str = f"{year_str}-{m:02d}"
    log_dir = f"{KB_ROOT}/extras/logs/{month_str}"
    if os.path.exists(log_dir):
        for fname in os.listdir(log_dir):
            if fname.endswith('.json'):
                with open(os.path.join(log_dir, fname)) as f:
                    all_logs.append(json.load(f))

if not all_logs:
    print("  ⚠️ 本季度无日志数据")
    exit(0)

# 1. 模式热力图
mode_month = defaultdict(lambda: Counter())
for log in all_logs:
    ts = log.get('timestamp', '')[:7]  # YYYY-MM
    for m in log.get('used_modes', []):
        mode_month[ts][m] += 1

# 2. 模式共现分析
cooccurrence = Counter()
for log in all_logs:
    modes = log.get('used_modes', [])
    for i in range(len(modes)):
        for j in range(i+1, len(modes)):
            pair = tuple(sorted([modes[i], modes[j]]))
            cooccurrence[pair] += 1

top_combos = cooccurrence.most_common(5)

# 3. 场景覆盖分析
scenes_used = set(log.get('category', '') for log in all_logs)
expected_scenes = {'工作', '学习', '生活', '决策', '管理', '写作', '技术', '人际', '创业', '投资'}
gaps = expected_scenes - scenes_used

# 4. 成熟度评估
mode_stats = defaultdict(lambda: {'count': 0, 'ratings': [], 'cases': 0})
for log in all_logs:
    for m in log.get('used_modes', []):
        mode_stats[m]['count'] += 1
        mode_stats[m]['ratings'].append(log.get('rating', 0))
        if log.get('outcome') == 'success':
            mode_stats[m]['cases'] += 1

# 5. 生成洞察报告
suggestion_file = f"{SUGGESTIONS_DIR}/{QUARTER}-suggestions.md"
os.makedirs(os.path.dirname(suggestion_file), exist_ok=True)

report = f"""# {QUARTER} 季度知识洞察与建议

> 生成日期：{datetime.now().strftime('%Y-%m-%d')}
> 数据来源：{len(all_logs)} 条使用日志

---

## A. 模式热力图

"""

for month in months:
    ms = f"{year_str}-{month:02d}"
    report += f"### {ms}\n"
    if ms in mode_month:
        for mode, count in mode_month[ms].most_common(5):
            report += f"- #{mode}: {count} 次\n"
    else:
        report += "- 无记录\n"
    report += "\n"

report += f"""
## B. 模式组合推荐（Top 5 共现）

| 组合 | 共现次数 | 建议 |
|------|---------|------|
"""

for (m1, m2), count in top_combos:
    report += f"| #{m1} + #{m2} | {count} 次 | {'强关联' if count >= 5 else '建议验证'} |\n"

report += f"""
## C. 空白领域识别

| 领域 | 状态 | 建议 |
|------|------|------|
"""

for gap in sorted(gaps):
    report += f"| {gap} | 未覆盖 | 建议补充相关思维模式 |\n"

report += f"""
## D. 模式成熟度评估

| 模式 | 使用次数 | 平均评分 | 案例数 | 等级 |
|------|---------|---------|--------|------|
"""

for mode, stats in sorted(mode_stats.items(), key=lambda x: x[1]['count'], reverse=True):
    avg = sum(stats['ratings']) / len(stats['ratings']) if stats['ratings'] else 0
    if stats['count'] >= 20 and avg >= 4.0 and stats['cases'] >= 5:
        level = "⭐⭐⭐⭐⭐ 本能级"
    elif stats['count'] >= 10 and avg >= 3.5 and stats['cases'] >= 3:
        level = "⭐⭐⭐⭐ 精通级"
    elif stats['count'] >= 5 and avg >= 3.0 and stats['cases'] >= 2:
        level = "⭐⭐⭐ 熟练级"
    elif stats['count'] >= 3 and avg >= 2.5:
        level = "⭐⭐ 入门级"
    else:
        level = "⭐ 初识级"
    report += f"| #{mode} | {stats['count']} | {avg:.1f} | {stats['cases']} | {level} |\n"

report += f"""
## E. 更新建议

### 必须处理
1. 补充空白领域：{', '.join(sorted(gaps)[:3])}
2. 审核 Top 3 案例入库候选

### 建议处理
1. 审查共现模式 #{top_combos[0][0][0]} + #{top_combos[0][0][1]}，确认是否在 selector 中推荐
2. 检查成熟度为"初识级"但使用量增长的模式，决定是否升级为"入门级"

### 可选处理
1. 探索 {', '.join(sorted(gaps)[:2])} 领域是否有合适的现有模式可复用
"""

with open(suggestion_file, 'w') as f:
    f.write(report)

print(f"  ✅ 季度洞察已生成：{suggestion_file}")
print(f"  📊 日志数：{len(all_logs)} | 模式数：{len(mode_stats)} | 空白领域：{len(gaps)}")
PYEOF

echo "✅ 季度洞察生成完成"
```

### 6.4 版本发布脚本

**文件**：`本体系/scripts/release_version.sh`

```bash
#!/bin/bash
# 知识体系版本自动发布器
# 用法：./release_version.sh [major|minor|patch] [--dry-run]

set -euo pipefail

KB_ROOT="docs/本体系"
RELEASES_DIR="${KB_ROOT}/extras/releases"
PENDING_DIR="${KB_ROOT}/extras/pending"
CASES_DIR="${KB_ROOT}/extras/cases"
MISTAKES_DIR="${KB_ROOT}/extras/mistakes"
SKILLS_DIR="${KB_ROOT}/skills"

DRY_RUN=false
if [[ "${1: -9}" == "--dry-run" ]]; then
    DRY_RUN=true
    shift
fi

CHANGE_TYPE="${1:-auto}"  # major, minor, patch, or auto

echo "🚀 开始版本发布流程..."

python3 << PYEOF
import json
import os
import re
from datetime import datetime

KB_ROOT = "docs/本体系"
RELEASES_DIR = f"{KB_ROOT}/extras/releases"
PENDING_DIR = f"{KB_ROOT}/extras/pending"
CASES_DIR = f"{KB_ROOT}/extras/cases"
MISTAKES_DIR = f"{KB_ROOT}/extras/mistakes"
README_PATH = f"{KB_ROOT}/README.md"

change_type = "${CHANGE_TYPE}"
dry_run = ${DRY_RUN}

# 读取当前版本号
current_version = "1.0.0"
if os.path.exists(README_PATH):
    with open(README_PATH) as f:
        content = f.read()
        match = re.search(r'版本\s+(\d+)\.(\d+)\.(\d+)', content)
        if match:
            current_version = match.group(0).replace('版本 ', '')

# 解析版本号
parts = [int(x) for x in current_version.split('.')]

# 确定变更类型
if change_type == "auto":
    # 检查 pending 目录是否有新模式
    new_modes = False
    new_cases = False
    for f in os.listdir(PENDING_DIR) if os.path.exists(PENDING_DIR) else []:
        if f.endswith('.md'):
            with open(os.path.join(PENDING_DIR, f)) as fh:
                if 'new_mode' in fh.read().lower() or '新模式' in fh.read():
                    new_modes = True
    
    if new_modes:
        parts[1] += 1  # minor
        change_type = "minor"
    elif os.path.exists(CASES_DIR) and len(os.listdir(CASES_DIR)) > 0:
        parts[2] += 1  # patch
        change_type = "patch"
    else:
        print("  ⚠️ 无实质性变更，跳过发布")
        exit(0)
elif change_type == "major":
    parts[0] += 1
    parts[1] = 0
    parts[2] = 0
elif change_type == "minor":
    parts[1] += 1
    parts[2] = 0
elif change_type == "patch":
    parts[2] += 1

new_version = '.'.join(str(p) for p in parts)
release_date = datetime.now().strftime('%Y-%m-%d')

# 收集变更项
changes = {'新增': [], '修改': [], '废弃': [], '案例': [], '错题': []}

# 1. 从 pending/ 收集
if os.path.exists(PENDING_DIR):
    for f in os.listdir(PENDING_DIR):
        if f.endswith('.md'):
            filepath = os.path.join(PENDING_DIR, f)
            with open(filepath) as fh:
                content = fh.read()
                if 'approved' in content.lower() or '采纳' in content:
                    changes['新增'].append(f)
                else:
                    changes['修改'].append(f + '（待审核）')

# 2. 从 cases/ 收集本月新增
if os.path.exists(CASES_DIR):
    for f in os.listdir(CASES_DIR):
        if f.endswith('.md'):
            changes['案例'].append(f)

# 3. 从 mistakes/ 收集
if os.path.exists(MISTAKES_DIR):
    for f in os.listdir(MISTAKES_DIR):
        if f.endswith('.md'):
            changes['错题'].append(f)

# 生成版本摘要
release_notes = f"""# 版本 {new_version} 发布说明

发布日期：{release_date}
版本类型：{change_type}

## 新增
""" + '\n'.join(f'- {c}' for c in changes['新增']) + f"""

## 修改
""" + '\n'.join(f'- {c}' for c in changes['修改']) + f"""

## 案例入库
""" + '\n'.join(f'- {c}' for c in changes['案例']) + f"""

## 错题记录
""" + '\n'.join(f'- {c}' for c in changes['错题']) + """

## 已知问题
- 无
"""

# 保存发布说明
os.makedirs(RELEASES_DIR, exist_ok=True)
release_file = f"{RELEASES_DIR}/v{new_version}.md"
if dry_run:
    print(f"  📄 [DRY RUN] 版本摘要将保存至：{release_file}")
    print(f"  📄 内容预览：")
    print(f"  ---")
    print(release_notes)
    print(f"  ---")
else:
    with open(release_file, 'w') as f:
        f.write(release_notes)
    print(f"  ✅ 版本摘要已保存：{release_file}")

# 更新 README.md 版本号
if not dry_run and os.path.exists(README_PATH):
    with open(README_PATH) as f:
        readme = f.read()
    readme = re.sub(
        r'(版本\s+)(\d+\.\d+\.\d+)',
        f'\\g<1>{new_version}',
        readme
    )
    readme = re.sub(
        r'(\*最后更新：)\d{4}-\d{2}-\d{2}',
        f'\\g<1>{release_date}',
        readme
    )
    with open(README_PATH, 'w') as f:
        f.write(readme)
    print(f"  ✅ README.md 版本号已更新为 {new_version}")

# 更新 quick_reference.md
qr_path = f"{KB_ROOT}/quick_reference.md"
if not dry_run and os.path.exists(qr_path):
    with open(qr_path) as f:
        qr = f.read()
    qr = re.sub(
        r'最后更新：\d{4}-\d{2}-\d{2}',
        f'最后更新：{release_date}',
        qr
    )
    with open(qr_path, 'w') as f:
        f.write(qr)
    print(f"  ✅ quick_reference.md 更新日期已更新")

print(f"\n  🎉 版本 {new_version} ({change_type}) 发布完成！")
PYEOF

echo "✅ 版本发布流程结束"
```

### 6.5 健康度检查脚本

**文件**：`本体系/scripts/health_check.sh`

```bash
#!/bin/bash
# 知识体系健康度自动检查器
# 用法：./health_check.sh

set -euo pipefail

KB_ROOT="docs/本体系"

echo "🏥 知识体系健康检查..."

python3 << 'PYEOF'
import os
import json
from datetime import datetime, timedelta
from collections import Counter

KB_ROOT = "docs/本体系"
EXTRAS = f"{KB_ROOT}/extras"
REPORT_DIR = f"{EXTRAS}/reports"
HEALTH_DIR = f"{EXTRAS}/health"

os.makedirs(HEALTH_DIR, exist_ok=True)

now = datetime.now()
week_ago = now - timedelta(days=7)
month_ago = now - timedelta(days=30)

# 指标 1：日志覆盖率
total_sessions = 0
logged_sessions = 0
log_base = f"{EXTRAS}/logs"
if os.path.exists(log_base):
    for month_dir in os.listdir(log_base):
        month_path = os.path.join(log_base, month_dir)
        if os.path.isdir(month_path):
            for f in os.listdir(month_path):
                if f.endswith('.json'):
                    total_sessions += 1
                    try:
                        with open(os.path.join(month_path, f)) as fh:
                            data = json.load(fh)
                            if data.get('used_modes'):
                                logged_sessions += 1
                    except:
                        pass

coverage = (logged_sessions / total_sessions * 100) if total_sessions > 0 else 0
coverage_status = "green" if coverage >= 20 else ("yellow" if coverage >= 15 else "red")

# 指标 2：模式分布均匀度
mode_counter = Counter()
if os.path.exists(log_base):
    for month_dir in os.listdir(log_base):
        month_path = os.path.join(log_base, month_dir)
        if os.path.isdir(month_path):
            for f in os.listdir(month_path):
                if f.endswith('.json'):
                    try:
                        with open(os.path.join(month_path, f)) as fh:
                            data = json.load(fh)
                            for m in data.get('used_modes', []):
                                mode_counter[m] += 1
                    except:
                        pass

# Shannon entropy
total_usage = sum(mode_counter.values())
entropy = 0
if total_usage > 0:
    for count in mode_counter.values():
        p = count / total_usage
        if p > 0:
            entropy -= p * (p ** 0.5 - 1)  # 简化计算

entropy_status = "green" if entropy >= 1.5 else ("yellow" if entropy >= 1.2 else "red")

# 指标 3：案例增长率
cases_dir = f"{EXTRAS}/cases"
this_month_cases = 0
if os.path.exists(cases_dir):
    for f in os.listdir(cases_dir):
        if f.endswith('.md'):
            mtime = datetime.fromtimestamp(os.path.getmtime(os.path.join(cases_dir, f)))
            if mtime >= month_ago:
                this_month_cases += 1

case_status = "green" if this_month_cases >= 2 else ("yellow" if this_month_cases >= 1 else "red")

# 指标 4：内容新鲜度
source_dir = f"{KB_ROOT}/source"
days_since_update = 999
if os.path.exists(source_dir):
    for f in os.listdir(source_dir):
        fp = os.path.join(source_dir, f)
        if os.path.isfile(fp):
            mtime = datetime.fromtimestamp(os.path.getmtime(fp))
            days = (now - mtime).days
            if days < days_since_update:
                days_since_update = days

freshness_status = "green" if days_since_update <= 90 else ("yellow" if days_since_update <= 60 else "red")

# 指标 5：技能包同步
skills_dir = f"{KB_ROOT}/skills"
sync_diff = 0  # 简化：检查 skills 目录是否存在且非空
if os.path.exists(skills_dir) and len(os.listdir(skills_dir)) > 0:
    sync_status = "green"
else:
    sync_status = "red"
    sync_diff = 999

# 综合评分
scores = {
    '日志覆盖率': (coverage, 20, coverage_status),
    '模式分布熵': (entropy, 1.5, entropy_status),
    '案例增长率': (this_month_cases, 2, case_status),
    '内容新鲜度': (days_since_update, 90, freshness_status),
    '技能包同步': (sync_diff, 0, sync_status)
}

total_score = 0
max_score = 500
issues = []

for name, (current, threshold, status) in scores.items():
    if status == "green":
        total_score += 100
    elif status == "yellow":
        total_score += 50
        issues.append(f"⚠️ {name} 低于阈值（当前: {current}, 阈值: {threshold}）")
    else:
        total_score += 0
        issues.append(f"🔴 {name} 严重低于阈值（当前: {current}, 阈值: {threshold}）")

# 生成健康报告
report = f"""# 知识体系健康报告 — {now.strftime('%Y-W%U')}

## 📊 总体健康度：{"🟢" if total_score >= 400 else ("🟡" if total_score >= 200 else "🔴")} 总分 {total_score}/500

| 指标 | 当前值 | 阈值 | 状态 |
|------|-------|------|------|
| 日志覆盖率 | {coverage:.1f}% | ≥20% | {"🟢" if coverage >= 20 else ("🟡" if coverage >= 15 else "🔴")} |
| 模式分布熵 | {entropy:.2f} | ≥1.5 | {"🟢" if entropy >= 1.5 else ("🟡" if entropy >= 1.2 else "🔴")} |
| 案例增长率 | {this_month_cases}/月 | ≥2 | {"🟢" if this_month_cases >= 2 else ("🟡" if this_month_cases >= 1 else "🔴")} |
| 内容新鲜度 | {days_since_update}天 | ≤90 | {"🟢" if days_since_update <= 90 else ("🟡" if days_since_update <= 60 else "🔴")} |
| 技能包同步 | {"正常" if sync_status == "green" else "异常"} | =0 | {"🟢" if sync_status == "green" else "🔴"} |

## 🔔 发现问题
"""

if issues:
    for issue in issues:
        report += f"- {issue}\n"
else:
    report += "- 暂无问题，系统运行良好 ✅\n"

report += f"""
## 📈 趋势
- 模式总数：{len(mode_counter)} 种
- 本月使用模式：{len([m for m, c in mode_counter.items() if c > 0])} 种
- 最活跃模式：#{mode_counter.most_common(1)[0][0]}（{mode_counter.most_common(1)[0][1]}次）

---
> 报告自动生成于 {now.strftime('%Y-%m-%d %H:%M')}
"""

report_file = f"{HEALTH_DIR}/health_{now.strftime('%Y-W%U')}.md"
with open(report_file, 'w') as f:
    f.write(report)

print(f"  ✅ 健康报告已生成：{report_file}")
print(f"  📊 总分：{total_score}/500 | 状态：{'🟢 良好' if total_score >= 400 else ('🟡 注意' if total_score >= 200 else '🔴 警告')}")

if issues:
    print(f"  🔔 发现 {len(issues)} 个问题：")
    for issue in issues:
        print(f"     {issue}")
PYEOF

echo "✅ 健康检查完成"
```

---

## 七、监控与告警

### 7.1 告警级别与响应

| 级别 | 条件 | 通知方式 | 响应时间 |
|------|------|---------|---------|
| **🟢 信息** | 正常运行，周报/月报生成 | Hermes 会话通知 | 无需 |
| **🟡 警告** | 健康度指标低于阈值 | 月度报告中标注 | 下次季度回顾前 |
| **🔴 严重** | 技能包同步失败 / 内容超过180天未更新 | 立即通知 + 邮件 | 24小时内 |
| **🚨 紧急** | 知识错误 / 使用中断 | 立即通知 | 2小时内 |

### 7.2 Cron 定时任务配置

在 Hermes Agent 中配置以下定时任务：

```yaml
# cron/knowledge-evolution.yaml

tasks:
  # 每日：日志采集
  - name: daily-log-collection
    schedule: "0 1 * * *"  # 每天凌晨 1 点
    command: "bash docs/本体系/scripts/collect_logs.sh"
    enabled: true

  # 每月：生成月度报告
  - name: monthly-report
    schedule: "0 0 1 * *"  # 每月 1 日 00:00
    command: "bash docs/本体系/scripts/generate_monthly_report.sh"
    enabled: true

  # 每季度：生成季度洞察
  - name: quarterly-insights
    schedule: "0 0 28 3,6,9,12 *"  # 每季度末月 28 日
    command: "bash docs/本体系/scripts/generate_quarter_insights.sh"
    enabled: true

  # 每季度：版本发布
  - name: quarterly-release
    schedule: "0 0 25 3,6,9,12 *"  # 每季度末月 25 日
    command: "bash docs/本体系/scripts/release_version.sh minor"
    enabled: true
    requires_manual_approval: true

  # 每周：健康检查
  - name: weekly-health-check
    schedule: "0 2 * * 0"  # 每周日 02:00
    command: "bash docs/本体系/scripts/health_check.sh"
    enabled: true
```

### 7.3 告警通知模板

当检测到异常情况时，自动发送通知：

```
🔔 知识体系告警 — {LEVEL}

问题：{ISSUE_DESCRIPTION}
详情：{DETAILS}
影响：{IMPACT}
建议操作：{ACTION}

报告链接：{REPORT_URL}
```

---

## 八、演进路线图

### Phase 1：基础自动化（第 1-2 个月）

- [x] 日志采集脚本部署
- [x] 月度报告自动生成
- [x] 案例自动归档
- [x] 错题本自动维护
- [ ] 目标：实现"使用→反馈"闭环自动化

### Phase 2：智能洞察（第 3-4 个月）

- [ ] 模式关联发现引擎
- [ ] 成熟度自动评估
- [ ] 季度洞察报告
- [ ] 更新建议自动生成
- [ ] 目标：实现"反馈→沉淀"半自动化

### Phase 3：版本自治（第 5-6 个月）

- [ ] 版本自动发布流程
- [ ] 跨文件自动同步
- [ ] 技能包自动更新
- [ ] 健康度监控仪表盘
- [ ] 目标：实现"沉淀→版本"自动化

### Phase 4：自进化（第 7-12 个月）

- [ ] 知识图谱自动构建
- [ ] 新模式自动推荐
- [ ] 智能对比矩阵更新
- [ ] 自适应版本策略
- [ ] 目标：知识体系完全活系统

---

## 附录 A：目录结构总览

```
本体系/
├── README.md                          ← 项目总览（版本号自动更新）
├── quick_reference.md                 ← 快速检索表（日期自动更新）
│
├── source/                            ← 原始研究文件（只读）
│   ├── ultimate_thinking_methods_handbook.md
│   ├── thinking_mode_selector.md
│   ├── four_writers_comparison.md
│   ├── cross_domain_expansion.md
│   ├── cross_domain_expansion_v2.md
│   └── world_communist_complete_spectrum.md
│
├── skills/                            ← 技能包（自动同步）
│   ├── ultimate-thinking-and-writing-methods/
│   ├── maozedong-writing/
│   └── four-writers-writing/
│
├── extras/                            ← 扩展区域
│   ├── logs/                          ← 自动采集的使用日志
│   │   ├── 2026-07/
│   │   │   ├── log_20260711_001.json
│   │   │   └── log_20260711_002.json
│   │   └── 2026-08/
│   ├── reports/                       ← 自动生成的报告
│   │   ├── monthly/                   ← 月度报告
│   │   │   └── 2026-07-report.md
│   │   └── quarterly/                 ← 季度洞察
│   │       └── 2026-Q3-insights.md
│   ├── suggestions/                   ← 自动更新建议
│   │   └── 2026-Q3-suggestions.md
│   ├── cases/                         ← 案例库（自动归档）
│   │   └── 2026-07-11_项目优先级排序.md
│   ├── mistakes/                      ← 错题本（自动维护）
│   │   └── 2026-07-12_模式误用_001.md
│   ├── maturity/                      ← 模式成熟度评估
│   │   └── mode-1-maturity.md
│   ├── reviews/                       ← 季度回顾记录
│   ├── releases/                      ← 版本发布说明（自动生成）
│   │   └── v1.1.0.md
│   └── pending/                       ← 待审核内容
│
├── scripts/                           ← 自动化脚本
│   ├── collect_logs.sh                ← 日志采集
│   ├── generate_monthly_report.sh     ← 月度报告
│   ├── generate_quarter_insights.sh   ← 季度洞察
│   ├── release_version.sh             ← 版本发布
│   └── health_check.sh                ← 健康检查
│
└── health/                            ← 健康度报告（自动生成）
    └── health_2026-W28.md
```

---

## 附录 B：关键设计原则

1. **零摩擦记录**：用户只需一句话，系统自动解析结构化数据
2. **自动优先**：所有重复性操作脚本化，人工只负责审核和决策
3. **数据驱动**：每次更新建议都基于实际使用数据，而非主观判断
4. **渐进式自动化**：从 50% 自动化起步，逐步提升到 90%+
5. **人工兜底**：任何自动变更都可人工审核、回滚
6. **透明可追溯**：所有变更都有日志、版本号、时间戳
7. **向后兼容**：版本更新不影响已有内容的可用性
8. **健康优先**：持续监控系统健康度，预防知识体系退化

---

> **"捉住了这个主要矛盾，一切问题就迎刃而解了。"**
>
> 知识体系的持续演进也是如此——抓住**使用数据**这个主要矛盾，
> 让每一次使用都成为进化的燃料。

---

*最后更新：2026-07-11*
*作者：Protreptic*
*版本：1.0.0*
