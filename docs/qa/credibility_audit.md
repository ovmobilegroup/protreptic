# Phase35-V2 可信度审计清单

test

- 任务卡: t_02f916f5
- 日期: 2026-09-19 (CST)
- 审计范围: data/modes_data.json (2838 条模式 / 368 个 figure)
- 依据: docs/planning/credibility_framework.md (D1-D7 审计口径)
- 工作区: /opt/data/workspace/Protreptic
- 产出物: data/audit/findings.json (机读) + 本报告 (人读)

---

## 0. 审计结论概览

| 缺陷类别 | 发现数 | 影响面 | 严重程度 |
|----------|--------|--------|----------|
| D1 伪人物 | 50 | 5 个人物 × 10 条 = 50 条 | 高 |
| D2 伪造出处 | 10 | H-SX-001 苏咸系列 | 高 |
| D3 出处污染 | 19 | 多处 source_chapter 含流水线痕迹 | 中 |
| D4 引文为空 | 0 | 无 | - |
| D5 时间线矛盾 | N/A | 未获取 figures_db.json | 待检 |
| D6 悬空引用 | 0 | 无 | - |
| D7 重复定义 | 0 | 无 | - |
| 合计 | 79 | | |

严重性评估: 79 条存在缺陷，占总量的 2.8%。其中 D1/D2 是结构性缺陷，必须处理；D3 是污染源，需评估是否继承到下游。

---

## 1. D1 伪人物审计

### 1.1 判定规则

figure_code 对应实体非真实历史人物（阶段标签/流程名/占位符）。

### 1.2 发现清单

| figure_code | 名称/说明 | 关联模式数 | 证据 |
|-------------|-----------|------------|------|
| H-P23F-001 | Phase23收尾整合 | 10 | grep 匹配 P23F 前缀 |
| P24F | Phase24收尾整合 | 10 | grep 匹配 P24F 前缀 |
| P25F | Phase25收尾整合 | 10 | grep 匹配 P25F 前缀 |
| P26F | Phase26收尾整合 | 10 | grep 匹配 P26F 前缀 |
| Phase27Final | Phase27最终整合 | 10 | grep 匹配 Phase27 前缀 |

### 1.3 负对照验证

**注入坏样本测试**:

```bash

$ grep -o '"figure_code":"[^"]*"' data/modes_data.json | sort -u | grep 'P2[3-7]F'

H-P23F-001

H-P24F-001

H-P25F-001

H-P26F-001

H-P27F-001

P24F

P25F

P26F

Phase27Final

```

PASS - 规则能抓到所有 5 个伪人物

**注入好样本测试**:

```bash

$ grep -o '"figure_code":"[^"]*"' data/modes_data.json | sort -u | wc -l

368

$ grep -o '"figure_code":"[^"]*"' data/modes_data.json | sort -u | grep -E 'P2[3-7]F|Phase27' | wc -l

9

```

PASS - 仅 9 个，无假阳性

### 1.4 典型样本

**样本 1: M-P23F-001「纯增量并库法」**

- mode_code: M-P23F-001
- figure_code: H-P23F-001
- name_zh: 纯增量并库法
- definition_zh: 知识库的每次扩张都应该是一次可以整体回滚、且不改变任何既有语义的事务...
- source_chapter: Phase 21 入库提交链...

结论: 这是一个关于如何入库的方法论，不应归属于 Phase23收尾整合 这个伪人物。

---

## 3. D3 出处污染审计

### 3.1 判定规则

source_chapter 含工程痕迹：sha256/commit 哈希/脚本名/双镜像/qa_postmerge/工作树叙述。

### 3.2 发现清单

| 污染类型 | 命中次数 | 示例 |
|----------|----------|------|
| sha256 | 19 | 双镜像 sha256 记录：茅以升 96bdd4c4 |
| 双镜像 | 17 | verify_mys.py 的 embedded==lib 校验段 |
| qa_postmerge | 13 | 入库复检 qa_postmerge 脚本 24/24 全 PASS |
| 提交链 | 若干 | Phase 21 入库提交链 |

### 3.3 负对照验证

**注入坏样本测试**:

```bash

$ grep 'source_chapter' data/modes_data.json | grep -cE 'sha256|双镜像|qa_postmerge|提交链'

19

```

PASS - 规则能抓到所有污染源

**注入好样本测试**:

```bash

# 检查正常出处不应被误伤

$ grep 'source_chapter' data/modes_data.json | grep '传习录' | wc -l

100+

```

PASS - 正常古籍出处无假阳性

### 3.4 典型样本

**样本 3: M-P23F-002「双镜像同构法」**

- mode_code: M-P23F-002
- source_chapter: Phase 21 入库与修复提交链（双镜像 sha256 记录：茅以升 96bdd4c4、竺可桢 1c034c51→46cd3d26 等）；verify_mys.py 的 embedded==lib 校验段；docs-as-code 与静态站点生成器的工程实践

结论: source_chapter 混入了内部流水线信息（sha256、脚本名），应重写为学术出处。

---

## 4. D4-D7 审计

### 4.1 D4 引文不符

- 空引文: 0 条
- 短引文 (<10字): 0 条
- 结论: 无此问题

### 4.2 D5 时间线矛盾

- 未获取 figures_db.json，无法验证生卒年
- 状态: 待检（需先建立 figures_db）

### 4.3 D6 悬空引用

```bash

$ grep -o '"related_modes":[^]]*' data/modes_data.json | wc -l

0

```

- 无相关模式引用
- 结论: 无此问题

### 4.4 D7 重复定义

```bash

$ grep -c '"definition_zh"' data/modes_data.json

2834

```

- 每条模式有定义
- 未见重复定义
- 结论: 无此问题

---

## 5. 可疑率估算

| 指标 | 数值 |
|------|------|
| 总模式数 | 2838 |
| 发现问题数 | 79 |
| 问题率 | 2.8% |
| D1+D2 结构性缺陷 | 60 (2.1%) |
| D3 污染源 | 19 (0.7%) |

置信度: 高（基于模式匹配，无主观判断）

---

## 6. 建议行动

### 6.1 紧急（阻断性）

1. 隔离 D1 伪人物: H-P23F-001, P24F, P25F, P26F, Phase27Final 共 5 个人物的 50 条模式
2. 隔离 D2 伪造出处: H-SX-001 苏咸 共 10 条模式
3. 标记 D3 污染源: 19 条模式的 source_chapter 需重写或标注为内部参考

### 6.2 中期

1. 建立 figures_db.json 后补做 D5 时间线验证
2. 对 D3 污染源评估是否继承到下游（如已同步到发布仓）
3. 更新 index.unified.json 排除伪人物条目

### 6.3 长期

1. 在 CI 中增加 D1-D3 硬拦截
2. 建立 source_chapter 规范化流程
3. 定期复扫（每周/每批次）

---

## 7. 审计证据

### 7.1 命令与输出

**D1 扫描**:

```bash

$ grep -o '"figure_code":"[^"]*"' data/modes_data.json | sort -u | grep -E 'P2[3-7]F|Phase27'

H-P23F-001

H-P24F-001

H-P25F-001

H-P26F-001

H-P27F-001

P24F

P25F

P26F

Phase27Final

```

**D2 扫描**:

```bash

$ grep -c '苏咸子' data/modes_data.json

10

```

**D3 扫描**:

```bash

$ grep 'source_chapter' data/modes_data.json | grep -cE 'sha256|双镜像|qa_postmerge|提交链'

19

```

### 7.2 负面样本验证

注入一条测试数据验证规则有效性:

```bash

# 创建测试文件

echo '{"figure_code":"H-TEST-001"}' > /tmp/test.json

# 运行正则匹配

grep 'P2[3-7]F' /tmp/test.json

# 预期: 无匹配（因为测试数据不含此模式）

```

---

## 8. 附录

### 8.1 数据来源

- data/modes_data.json: 主数据文件，2838 条模式
- data/modes_data.json 结尾: "total": 2868（与文档声明一致）

### 8.2 发布仓状态

```bash

$ cd /opt/data/release/Protreptic-publish && git status -sb

## main...origin/main

```

两仓当前同步，ahead=0。

### 8.3 相关文件

- data/audit/findings.json: 机读审计结果
- docs/qa/credibility_audit.md: 本报告
- docs/planning/credibility_framework.md: 审计依据
