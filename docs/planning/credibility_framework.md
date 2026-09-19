# Protreptic 可信度体系（Credibility Framework）

> 目标：把对外承诺「**每条都有出处**」从**断言**变成**可点击、可核验、有分级、有 CI 门守着的机制**。
> 状态：规划中（Phase 35 起分阶段落地）
> 依据：对本仓 `data/modes_data.json`（2858 条有效模式 / 283 位人物）的实测侦察

---

## 0. 为什么做（实测证据，非推测）

| # | 类别 | 实例 | 影响面 | 证据 |
|---|---|---|---|---|
| E1 | **伪人物**（figure 非真实历史人物） | `H-P23F-001`「Phase23收尾整合」/ `P24F` / `P25F` / `P26F` / `Phase27Final` | **5 个"人物" / 50 条模式** | 线上 `/minds/P24F` 等 5 个 URL 均 200，标题即「Phase2x收尾整合」；已进入 `index.unified.json` 名录 |
| E2 | **出处字段污染**（塞入流水线内部痕迹） | `M-P23F-002`「双镜像同构法」出处=「Phase 21 入库与修复提交链（双镜像 sha256 记录：茅以升 96bdd4c4…）」 | ≥42 条含 sha256/提交哈希/脚本名 | grep `sha256\|qa_postmerge\|双镜像\|入库复检` 命中 56 条 |
| E3 | **伪造出处**（引不存在的书） | `H-SX-001`「苏咸」引《苏咸子》 | 10 条（已隔离） | 检索证实《苏咸子》不存在 |
| E4 | 出处粒度不足 | 仅书名级（无篇/章/卷） | 1041 / 2858 = 36% | 字段统计 |
| E5 | 无页码 | 出处带页码 | 仅 25 / 2858 | 字段统计 |
| E6 | 引用面巨大且无人核对 | 被引书名 | **2169 种** | 字段统计 |
| E7 | **无核验状态字段** | — | 全部 2858 条 | schema 中不存在 verification 类字段 |

**结论**：产品最核心的承诺上，目前已确认存在 2 类真实缺陷（E1/E2 尚未止血），且缺少任何"可信度"表达机制（E7）。

---

## 1. 审计口径（Defect Taxonomy）

对每条模式定义可机检的缺陷类别：

| 代号 | 缺陷 | 判定规则（机检） | 处置 |
|---|---|---|---|
| **D1** | 伪人物 | `figure_code` 对应实体非真实历史人物（阶段标签 / 流程名 / 占位符） | 出库 + 隔离 |
| **D2** | 伪造出处 | 书名不存在于任何权威目录；或自引伪造（《X氏子》型） | 隔离 + 复核 |
| **D3** | 出处污染 | `source_chapter` 含工程痕迹：`sha256` / commit 哈希 / 脚本名 / `双镜像` / `qa_postmerge` / 工作树叙述 | 重写或隔离 |
| | | **豁免条款**：已隔离（D1）的伪人物 figure 允许保留源库工程痕迹，以导出期过滤为准。豁免名单：`H-P23F-001`、`P24F`、`P25F`、`P26F`、`Phase27Final`。机检方式：D3 gate 跳过 quarantined figure 的模式，仅对公开人物进行 source_chapter 扫描。 |
| **D4** | 引文不符 | `key_quote_zh` 文本不出现于所标出处的原文 | 复核 |
| **D5** | 时间线矛盾 | 引文年代 > 人物卒年（或 < 生年） | 复核 |
| **D6** | 悬空引用 | `cross_references` / `related_modes` 指向不存在的 `mode_code` | 自动修 |
| **D7** | 重复/近重复 | 同 figure 内 definition 相似度 > 阈值；或跨 figure 文本重复 | 合并/标注 |

**审计产出物**：`docs/qa/credibility_audit.md` + 机读 `data/audit/findings.json`
（每条：`mode_code` / `figure_code` / `defect` / `evidence` / `suggested_action`），**全部可复核**。

---

## 2. 引文可点击化 · 链接源清单（Link Sources）

| 出处类型 | 数量级 | 首选链接源 | 备注 |
|---|---|---|---|
| 中文古籍（经史子集） | 868 条含古籍书名 | **ctext.org** / 维基文库 `zh.wikisource.org` | 章节级深链；《史记》《资治通鉴》《论语》等直接可定位 |
| 西文经典 | 733 条含英文 | **Project Gutenberg** / **Internet Archive** / `en.wikisource.org` | 公版书可全文定位 |
| 现代著作 | 一批 | **OpenLibrary** / 豆瓣 / 出版社页 | 仅做到书目级 |
| 事件 / 档案 | 一批（如康熙废太子、朗道考试） | 维基百科 / 博物馆·档案馆 | 链接到条目，非全文 |
| 口述 / 访谈 / 信札 | 一批 | **标注 `unverifiable` / `primary-source`** | **诚实标注不可链接，不硬造链接** |

**实现**：`data/source_links.json` —— `{book_or_event: {url, source_type, confidence}}`，
构建期把出处文本解析 → 匹配 → 生成可点击引用；解析不了的**保持纯文本并标记**。

> ⚠️ 铁律：**链接必须真实可达**（构建期 curl 校验 200），禁止猜测 URL。解析失败的**不得伪造链接**。

---

## 3. `verification_status` Schema

每条模式新增（向后兼容，缺省 `pending`）：

```json
"verification": {
  "status": "verified | pending | suspect | unverifiable",
  "method": "auto-scan | link-resolved | quote-matched | manual-review",
  "evidence": "https://ctext.org/... 或复核说明",
  "checked_at": "2026-09-19",
  "checker": "<worker-id 或 'ci'>"
}
```

| status | 含义 | UI 展示 |
|---|---|---|
| `verified` | 出处可达 + （如适用）引文匹配 | ✓ 已核验（可点击出处） |
| `pending` | 未核验（缺省） | ○ 待核验 |
| `suspect` | 命中 D1–D5 之一，待复核 | ⚠ 存疑 |
| `unverifiable` | 属口述/信札等本质不可链接类型 | — 一手材料（不可链接） |

**UI**：模式卡片 + 人物页加可信度徽章；**"存疑"比"假装全对"更可信**。
统计页诚实公布：已核 X / 待核 Y / 存疑 Z。

---

## 4. CI 门设计（防回流）

在现有预检（`EXPECT_FIGURES` 等断言）旁**并列**新增 `credibility_gate`：

```
tools/credibility_gate.py：
  D1 伪人物      → 硬 FAIL（新增即拦）
  D2 伪造出处    → 硬 FAIL
  D3 出处污染    → 硬 FAIL（正则扫描 source_chapter，**豁免已隔离 figure**）
  | | *豁免逻辑*：跳过 quarantined figure（H-P23F-001/P24F/P25F/P26F/Phase27Final）的模式，仅对公开人物扫描
  D6 悬空引用    → 硬 FAIL
  D4/D5         → WARN（写审计清单，不阻断）
```

- 接入发卡流水线：**挖矿卡入库前**必须先过 gate；不过直接 auto-block。
- 与现有 `preflight` 一样，gate 自身要有**负对照测试**（故意注入一条 D3 → 必须 exit 1）。

---

## 5. 分阶段路线

| 阶段 | 内容 | 产出 |
|---|---|---|
| **P35-A 止血** | 清掉 D1 伪人物（≥5 个 / 50 条）+ D3 污染出处重写 | 线上不再有「Phase2x收尾整合」人物 |
| **P35-B 审计** | 全量扫 D1–D7，出 `credibility_audit.md` + `findings.json` | 可复核的坏数据全清单 |
| **P35-C 机制** | schema 定稿 + `source_links.json` + `credibility_gate.py`（含负对照） | 机制就位 |
| **P35-D 落地** | 构建期解析出处 → 生成可点击引用 + 写入 `verification` | 线上每条出处可点 |
| **P35-E 展示** | UI 可信度徽章 + 统计页 | 「已核 X/待核 Y/存疑 Z」 |
| **P35-QA** | 独立复验（含负对照、线上实测） | 可发布/不可发布结论 |

---

## 6. 铁律（承接项目既有纪律）

1. 归因/结论必须出示原始证据；查不到就说"根因未查明"；**禁用流利故事填补证据空白**。
2. 链接必须真实可达（构建期 curl 200 校验）；**解析不了就诚实标注，不伪造**。
3. 「存疑」要如实展示，**不假装 100% 干净**。
4. 任何机检规则都要有**负对照测试**（能抓到坏样本）。
5. 两仓同步、字节级一致；push 后 `ahead=0`；CI 自证。
