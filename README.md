# Protreptic · 思维养成系统

> **把「历史上的人怎么想问题」变成你今天能照着做的步骤。**
> 在线站点（免安装，打开即用）：**https://ovmobilegroup.github.io/protreptic/**

[![站点](https://img.shields.io/badge/%E5%9C%A8%E7%BA%BF%E7%AB%99%E7%82%B9-GitHub%20Pages-blue.svg)](https://ovmobilegroup.github.io/protreptic/)
[![代码许可: MIT](https://img.shields.io/badge/%E4%BB%A3%E7%A0%81-MIT-yellow.svg)](LICENSE)
[![内容许可: CC BY-SA 4.0](https://img.shields.io/badge/%E5%86%85%E5%AE%B9-CC%20BY--SA%204.0-lightgrey.svg)](LICENSE-CONTENT)

---

## 这是什么

Protreptic 是一个**可检索、可核对出处的历史人物思维模式库**。
它从 **278 位历史人物**的真实决策中提炼出 **2798 条思维模式**，每一条都给出四样东西：

1. **定义**（中英双语）——这套方法到底在做什么
2. **操作步骤**——今天遇到同类处境，照着做的动作清单
3. **出处**——来自哪本书、哪一篇，能点击就点击
4. **现代应用场景**——它在你这个时代对应什么问题

- 不是「名言集」：每条模式都有可执行步骤与适用边界
- 不是「凭空生成」：每条都标注来源篇章，并带**核验状态徽章**（见下一节）
- 不是「只能看」：站点可检索、可跨人物对比、可套用复盘模板，还能离线使用（PWA）

## 规模

| 项 | 数量 | 说明 |
|---|---|---|
| 历史人物 | **278 位** | 先秦诸子到近现代科学家、企业家，跨 30 个领域 |
| 思维模式 | **2798 条** | 站点发布口径；源库去重后 2858 条 |
| 其中被隔离 | 60 条 | 核验存疑的记录不进公开产物（站点上看不到） |
| 现代处境场景 | **1055 个** | 与人物合并为同一份可检索名录 |
| 复盘模板 | **7 个** | 赤壁、隆中对、北伐、白帝城等历史决策现场 |
| 语言 | 中英双语 | 每条模式都有中英定义、步骤与原话 |

> 数字口径来源：部署产物 `data/meta.json` 的 `counts`（构建期注入站点页面，站点与本文档同源，不各写一套）。

## 可信度：不假装每条都可信

「每条都有出处」这句话要能被检验，所以站点给每条模式一枚**核验状态徽章**，四态如下：

| 徽章 | 状态 | 含义 |
|---|---|---|
| ✓ | 已核验 | 出处可达，且已解析出可点击链接 |
| ○ | 待核验 | 尚未核验（schema 缺省态） |
| ⚠ | 存疑 | 机检命中缺陷规则（如引文与原文不符、时间线矛盾），隔离或待复核 |
| — | 一手材料 | 口述、信札等本质上不可链接的文献：诚实标注，不硬造链接 |

配套的三条纪律：

- **出处可点击**：模式详情页的出处逐条给链接；无法解析到链接的会如实标成「一手材料 / 待核验」，不假装全部可点
- **存疑不进公开产物**：源库中被判定存疑的模式会被隔离，站点只呈现发布口径，源库与发布口径的差额在统计页如实交代
- **数字实时可查**：四态数量随核验进度变动，以线上统计页为准 —— https://ovmobilegroup.github.io/protreptic/credibility/

## 站点能做什么

| 功能 | 入口 | 说明 |
|---|---|---|
| 人物 × 场景统一检索 | https://ovmobilegroup.github.io/protreptic/figures/ | 278 位人物 + 1055 个现代场景，同一份名录 |
| 思维模式库 | https://ovmobilegroup.github.io/protreptic/modes/ | 定义、操作步骤、出处、原话 |
| 概念索引 | https://ovmobilegroup.github.io/protreptic/concepts/ | 按关键概念聚合，探索跨人物的思想连接 |
| 关系图谱 | https://ovmobilegroup.github.io/protreptic/graph/ | 人物 — 模式 — 概念 的关系可视化 |
| 跨人物对比 | https://ovmobilegroup.github.io/protreptic/compare/ | 选 2–4 位并排对照，链接带选中项可直接分享 |
| 每日一模式 | https://ovmobilegroup.github.io/protreptic/daily/ | 每天一条，历史日期可回看 |
| 复盘模板 | https://ovmobilegroup.github.io/protreptic/templates/ | 7 个历史案例转成可直接套用的复盘清单 |
| 可信度统计 | https://ovmobilegroup.github.io/protreptic/credibility/ | 四态数字如实公布 |
| 数据与结构说明 | https://ovmobilegroup.github.io/protreptic/api/ | 静态数据分片、字段与读取方式 |
| 离线使用（PWA） | 任意页面 | 浏览器安装一次，断网也能查 |
| 文档站 | https://ovmobilegroup.github.io/protreptic/docs/ | 方法论、工具、训练、扩展等长文 |

## 怎么用

### 路径一：直接开站点（推荐）

打开 https://ovmobilegroup.github.io/protreptic/ ，在「人物 × 场景」名录里检索你的处境关键词，点进任意人物或模式即可看到定义、步骤与出处。零安装、零配置。

### 路径二：让 AI 用这套方法分析你的问题

复制 [思维模式 Agent Prompt](https://ovmobilegroup.github.io/protreptic/docs/06-ai-collaboration/thinking_mode_agent_prompt/) 里的 System Instruction，粘进你的 AI 工具设置；之后每次提问，AI 都会按这套模式库拆解问题。

### 路径三：本地跑或读源码

```bash
git clone https://github.com/ovmobilegroup/protreptic.git
cd protreptic

# 命令行选择器（Python 3，无第三方依赖）
python3 tools/thinking_mode_selector.py            # 交互式诊断
python3 tools/thinking_mode_selector.py -c A-1-X-P # 直接查处境代码
```

### 想系统学

- 10 分钟入门：[快速启动包](https://ovmobilegroup.github.io/protreptic/docs/00-quick-start/thinking_mode_quick_start/)
- 全量工具与使用手册：[文档站索引](https://ovmobilegroup.github.io/protreptic/docs/)
- 训练与自测：[实战演练场](https://ovmobilegroup.github.io/protreptic/docs/04-training/thinking_mode_gym/)

## 怎么贡献

欢迎任何形式的修正与补充，最需要的是**指出出处错误**与**补充真实案例**。

1. 读 [CONTRIBUTING.md](CONTRIBUTING.md)（贡献类型、案例格式、新模式的提议格式）
2. 用 issue 模板提交（[Bug](.github/ISSUE_TEMPLATE/bug.md) / [Feature](.github/ISSUE_TEMPLATE/feature.md) / [案例](.github/ISSUE_TEMPLATE/case.md)）
3. 提 PR 时请按 [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md) 填写；涉及内容改动的请附出处

行为准则见 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。

## 许可：代码与内容分开授权

本仓库是「代码 + 内容」混合体，两者各归各的许可：

| 范围 | 许可 | 许可文件 |
|---|---|---|
| **代码**：`web/`、`tools/`、`api/`、`scripts/` 及构建/CI 脚本 | **MIT** | [LICENSE](LICENSE) |
| **内容与数据**：`docs/` 下的文档、`data/` 与模式数据、复盘模板文本 | **CC BY-SA 4.0** | [LICENSE-CONTENT](LICENSE-CONTENT) |

- 代码（MIT）：可自由使用、修改、分发、商用，保留版权声明即可
- 内容（CC BY-SA 4.0）：可自由共享与改编（含商用），但需**署名**并以**相同方式共享**；官方正文见 https://creativecommons.org/licenses/by-sa/4.0/legalcode
- 为什么分开：CC 官方不建议用 CC 协议授权软件，MIT 也不适合覆盖文本内容；「代码服 MIT、内容服 CC BY-SA」是这类混合仓库的标准做法

## 项目结构

```
Protreptic/
├── web/                  # Vite + Vue 3 单页应用（站点 UI，含 PWA）
├── tools/                # 数据管线、校验门与构建脚本（Python）
├── data/                 # 模式、人物、场景数据与审计基线（JSON）
├── docs/                 # 方法论 / 工具 / 训练 / 扩展 等长文（11 个分类）
├── api/                  # 可选的后端（FastAPI；站点本身走静态数据）
├── .github/              # CI：Pages 发布、质量门、markdown lint + issue/PR 模板
├── LICENSE               # 代码许可：MIT
├── LICENSE-CONTENT       # 内容许可：CC BY-SA 4.0
├── CONTRIBUTING.md       # 贡献指南
├── CODE_OF_CONDUCT.md    # 行为准则
└── CHANGELOG.md          # 逐版变更记录
```

## 研究历程

项目从 2026-07 起按阶段推进（Phase 1 → Phase 44）：先写思维方法与写作技法手册，再逐位归档历史人物档案，随后转入工程化 ——
静态数据分片、可信度四态、出处链接核验门、两仓一致性机检、CI 质量门。

逐阶段的详细记录（含每阶段的验收报告与遗留问题）见 [CHANGELOG.md](CHANGELOG.md) 与 [docs/qa/](docs/qa/)。

---

*Protreptic —— 引导人们走向智慧的劝勉。*
*站点界面支持中英文切换（右上角）。*
