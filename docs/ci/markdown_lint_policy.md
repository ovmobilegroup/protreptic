# markdown-lint 口径（工作流 `CI` / `.github/workflows/markdown-lint.yml`）

本仓 markdown-lint 自 2026-09-17 起长期红，但**真实原因不是文档写错了**：`globs: "**/*.md"`
把三类**非人工维护**的 Markdown 也拉进了门，几千条格式噪声把真实信号埋掉
（Phase30-C4 终审修好的质量门失效问题原先就藏在这片红里）。

现在的口径 = **A（收敛到人工维护文档）+ B（存量清零）**：

1. **派生产物 / 镜像副本 / 归档快照不进这道门**（见 `.markdownlint-cli2.jsonc` 的 `ignores`）；
2. **剩下的人工维护文档必须零违规**（`docs/**`、`tools/**`、`data/individuals/**`、
   `CHANGELOG.md`、`README.md`、根目录的 `H-*.md`/研究笔记等，当前 212 个文件 0 违规）。

## 一、不进门的路径（及理由）

| 路径 | 类别 | 理由 |
|------|------|------|
| `**/node_modules/**`、`**/site-packages/**` | 依赖 | CI 的 lint job 不装依赖，忽略是为了本地复跑与 CI 一致 |
| `web/dist/**` | 构建产物 | `.gitignore` 已声明 `web/dist/`，历史提交仍被跟踪，按构建产物对待 |
| `web/public/templates/**` | 生成副本 | Phase30-B5 放进静态站 public 的模板下载副本，源在 SPA 侧 |
| `data/figures/**` | 数据层产物 | 人物档案的数据层产物（源：`data/figures/*.json` + 生成器） |
| `docs/figures/**` | 镜像副本 | 是 `data/figures` 的镜像，改它没有意义（下次同步即被覆盖） |
| `docs/historical_figures_thinking_modes_library.md` | 镜像文档 | 数据层图书馆的镜像（源在 `data/` + `tools/`） |
| `release/**` | 归档快照 | 冻结的 v2.0.0 发布快照，不再维护 |
| `docs_site/**`、`site_docs/**`、`_site/**` | 旧站/构建产物 | mkdocs 现场构建，不是本仓维护源 |

**纪律**：新增 `ignore` 必须能说出"谁生成它 / 谁是它的源"。不允许为了"让门变绿"
而忽略人工维护的文档 —— 那种做法正是这次要清理的病根。

## 二、.markdownlint.json 关掉的规则（规则级，非文件级）

| 规则 | 状态 | 理由 |
|------|------|------|
| `MD007` ul-indent | off | 中文列表缩进习惯与英文不同，无统一意义 |
| `MD009` br_spaces=2 | 2 | 保留"两个空格=硬换行"的合法用法 |
| `MD012` multiple-blanks | off | 模板/样例里的连续空行是排版意图，不是错误 |
| `MD013` line-length | off | 中文字符宽度与英文不可比，行长阈值没有意义 |
| `MD024` duplicate-headings | off | 模板类文档（多个 `### 周一` / `#### 核心模式1`）天然重复 |
| `MD025` single-h1 | off | 多个分篇合一的文档里 `# 第N周` 这类分节标题是有意的 |
| `MD026` trailing-punctuation | off | 中文标题常以 `：`/`？` 收尾 |
| `MD033` inline-html | off | 徽章、居中块、`<!-- -->` 注释需要行内 HTML |
| `MD034` bare-urls | off | 研究笔记里裸 URL 常见，加尖括号没有阅读价值 |
| `MD036` emphasis-as-heading | off | 模板里的加粗小标题是有意的 |
| `MD040` fenced-code-language | off | 大量纯文本/占位模板无需语言标注 |
| `MD041` first-line-h1 | off | `CHANGELOG.md` 这类片段文档首行不是 h1 |
| `MD046` code-block-style | off | 缩进式代码块在模板里是有意的 |

## 三、文件级豁免：MD029（跨标题连续编号的清单）

现象：这些文档用 `### P0/P1/P2 级`、`### Phase N` 分节，但清单编号是全篇连续的
（P0 是 1-3，P1 从 4 开始……）。markdownlint 把标题当作清单终止，于是要求"从 1 开始"。

这些编号承载**排序/优先级信息**，按 lint 要求重新编号 = 删内容，因此在文件内用
`<!-- markdownlint-disable MD029 -->` 定点豁免（markdownlint-cli2 v0.13 不对
markdownlint 规则应用 `.markdownlint-cli2.jsonc` 的 `overrides`，行内指令才是跨版本稳定的机制）：

- `docs/09-evolution/knowledge_system_audit.md`
- `docs/planning/phase4_{ART,DIP,MIL,SCI,TECH}_plan.md`
- `docs/review/consistency_review.md`
- `docs/review/phase3_review_report.md`
- 构建/剪贴板十三小提示.md

MD029 对其它所有文件照常生效。

## 四、本地复跑（与 CI 同一口径）

```bash
npx --yes markdownlint-cli2@0.13.0 "**/*.md"        # 期望 0 error
npx --yes markdownlint-cli2@0.13.0 --fix "**/*.md"  # 自动修（只修可自动修的）
```

## 五、下次红了怎么办

1. 先看**改的是哪一类文件**：若命中 `ignores` 里的路径，说明口径漏了（补 ignore + 理由）；
2. 若是人工维护文档：**改文档**，不要关规则 —— 这一节列的豁免清单应当只减不增；
3. 新增规则豁免/ignore 必须同步更新本文件。
