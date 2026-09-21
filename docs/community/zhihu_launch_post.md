# 知乎首发长文草稿（Phase45-B）

> **发布状态**：草稿，**尚未发布**。待用户审核后由用户手动发布到知乎（本卡不发帖、不投递）。
> **落盘路径**：`docs/community/zhihu_launch_post.md`
> **数字口径**：2798 条思维模式 / 278 位历史人物，与线上站点数据文件 `data/meta.json` 的 `counts` 字段一致（见附录一）。
> **正文里的例子**：逐字取自本库 `data/modes_data.json`（源 JSON 片段见附录二），无二次创作。

---

## 一、标题候选（三选一）

1. **道理都懂，轮到自己还是不会用：我把 278 位历史人物的思维模式拆成了能照做的步骤**
2. **278 位历史人物 × 2798 条思维模式：我做了一个每条都能点开出处的知识库**
3. **王阳明的「致良知」到底怎么做？他的档案里其实写着 5 个步骤**

怎么选：

- 建议 **第 1 个**：前半句是痛点，后半句给方法；不承诺结果、不夸覆盖；
- 第 2 个偏「产品向」，适合发在效率 / 工具类话题下；
- 第 3 个偏「历史向」，受众更窄但更精准。

## 二、正文

### 道理都懂，但轮到自己还是不会用

「知行合一」「实事求是」「知己知彼」——这些词我们都背过，也不难懂。

难的是：明天早上开会、跟人谈条件、做一个让你犹豫好几天的决定时，你具体该做什么？

讲思维方法的文章有个通病：给你一个漂亮的概念，配一句名言，然后结束。你读的时候点头，第二天还是老样子。真正缺的其实是个很朴素的东西 —— **具体的人，在具体的处境里，当时是怎么想的、按什么顺序做的**。

所以我把这件事做成了一个打开就能用的站点：**https://ovmobilegroup.github.io/protreptic/**

### 这是什么

它叫 Protreptic，是一个**可检索、可核对出处的历史人物思维模式库**：

- **278 位历史人物**，从先秦诸子到近现代科学家、企业家，跨 30 个领域；
- **2798 条思维模式**，每一条都给出四样东西：**定义**（中英双语）→ **操作步骤**（今天遇到同类处境照着做的动作清单）→ **出处**（来自哪本书、哪一篇）→ **现代应用场景**；
- 不是「名言集」：每条都带可执行步骤，不是一句漂亮话；
- 不是「凭空生成」：每条都标注来源篇章，并带一枚**核验状态徽章**（下面会讲这枚徽章有多诚实）；
- 不是「只能看」：站点能检索、能跨人物对比、能套复盘模板，装一次还能断网用。

### 一个你现在就能核对的例子

下面这一条，字段**逐字**取自数据文件，没有润色、没有补写。在线对应页面：https://ovmobilegroup.github.io/protreptic/minds/H-WYM-001/

**人物**：王阳明（1472—1529），明代心学集大成者。

**条目**：致良知法 / Conscience Cultivation Method

**定义**（原文）：

> 心之本体即良知，人人皆有良知，只需去除私欲遮蔽，使良知自然呈现。良知是判断是非善恶的根本标准，是道德自觉的源泉。

**操作步骤**（原文，共 5 步）：

1. 认识到人人皆有良知
2. 在具体事事物物中体认良知
3. 去除私欲对良知的遮蔽
4. 在道德实践中展现良知
5. 通过反省加深对良知的理解

**现代应用**（原文）：

> 在道德判断中信任良知，在日常生活中践行良知，在困境中坚守良知。

它对应到今天的问题域（原文）：

> 现代道德心理学中的道德直觉、良知教育、品格养成教育

**原话**（原文）：

> 「知善知恶是良知，为善去恶是格物」

**出处**：《传习录》—— 而且这个出处是**能点开的**：https://zh.wikisource.org/wiki/%E5%82%B3%E7%BF%92%E9%8C%84

**核验状态**：`verified` （已核验）；核验方式 `link-resolved` （把「出处」解析到了可访问的原文链接）；核验时间 2026-09-21。

这条东西的价值不在于王阳明说得对不对，而在于：**当你遇到一个说不清对错的处境时，手上有一条别人真用过的做法，而不是一句正确但没法执行的话**。

数据来源：本库 `data/modes_data.json` （mode_code 为 M381，figure_code 为 H-WYM-001；生卒年取自 `data/figures/H-WYM-001.json`）。源 JSON 片段见附录二，可逐字比对。

### 可信度：我不打算假装每条都可信

「每条都有出处」这句话，得能被检验才算数。所以站点给每条模式一枚**核验状态徽章**，一共四态：

| 徽章 | 状态 | 含义 |
|---|---|---|
| ✓ | 已核验 | 出处可达，且已解析出可点击链接 |
| ○ | 待核验 | 尚未核验（schema 缺省态） |
| ⚠ | 存疑 | 机检命中缺陷规则（如引文与原文不符、时间线矛盾） |
| — | 一手材料 | 口述、信札等本质上不可链接的文献：诚实标注，不硬造链接 |

**当前真实的分布**（截至 2026-09-21，取自线上数据文件 `data/meta.json` 的 `counts.verification.published`）：

- 已核验 **888** 条
- 待核验 **1547** 条
- 存疑 **23** 条
- 一手材料 **340** 条

合计 2798 条。也就是说，**大约三分之一已经核验过，其余三分之二如实标着「还没核到」**。它不是一个「全部考证完毕」的权威典籍，而是一个把进度摊开给你看的开放工程 —— 统计页随时可以对照：https://ovmobilegroup.github.io/protreptic/credibility/

「出处」这一项也一样摊开说：

- 2798 条里，**2758 条**（98.6%）填了具体的来源篇章；
- 其中**911 条**能解析成可点击的链接；
- 解析不到链接的，保留原文并标成「一手材料 / 待核验」，**不假装全部可点**。

（这几个数字的取数命令见附录一，你可以自己重跑。）

### 站点能做什么

| 功能 | 入口 | 说明 |
|---|---|---|
| 人物 × 场景统一检索 | 站点 /figures/ | 278 位人物 + 上千个现代处境场景，同一份名录 |
| 思维模式库 | 站点 /modes/ | 定义、操作步骤、出处、原话 |
| 概念索引 | 站点 /concepts/ | 按关键概念聚合，看跨人物的思想连接 |
| 关系图谱 | 站点 /graph/ | 人物 — 模式 — 概念 的关系可视化 |
| 跨人物对比 | 站点 /compare/ | 选 2 到 4 位并排对照，链接带选中项可直接分享 |
| 每日一模式 | 站点 /daily/ | 每天一条，历史日期可回看 |
| 复盘模板 | 站点 /templates/ | 把历史决策现场转成可直接套用的复盘清单 |
| 可信度统计 | 站点 /credibility/ | 四态数字如实公布 |
| 离线使用（浏览器 PWA） | 任意页面 | 装一次，断网也能查 |

完整链接与实测状态码见附录一。

### 最后

站点在这里，免安装、打开即用：

**https://ovmobilegroup.github.io/protreptic/**

它是开源的，也欢迎你来拆台：**指出出处错误、补充真实案例、提出新的思维模式**，都比点赞有用。

- 贡献指南：https://github.com/ovmobilegroup/protreptic/blob/main/CONTRIBUTING.md
- 仓库：https://github.com/ovmobilegroup/protreptic

---

## 附录一 · 数据来源与复核方式（发布时可删）

**门面数字 2798 / 278，以及四态数字**，本地一条命令即可复核（读部署产物 `data/meta.json`，不联网）：

```bash
python3 tools/site_counts.py --show
```

本次实际输出（逐字）：

```text
[counts] 口径来源: 本仓 web/dist/data/meta.json 的 counts.mode_summaries_published / counts.mode_by_figure_shards
[counts] description          : 2798 条思维模式 × 278 位历史人物：每条都有出处、操作步骤与现代应用。以人为鉴，明得失。
[counts] og:description       : 2798 条思维模式 × 278 位历史人物 · 中英双语
[counts] manifest description : 2798 条思维模式 × 278 位历史人物：每条都有出处、操作步骤与现代应用，中英双语，可离线查阅。
[counts] 可信度四态             : 发布口径 2798（已核验 888 / 待核验 1547 / 存疑 23 / 一手材料 340），源库口径合计 2858
```

线上同一个文件可直取对照：https://ovmobilegroup.github.io/protreptic/data/meta.json （本次回读 `counts.mode_summaries_published` 为 2798、`counts.mode_by_figure_shards` 为 278、`counts.verification.published` 为 888 / 1547 / 23 / 340）。

**注**：源库 `modes_raw` 为 2868、去重后 2858，另有 60 条隔离记录不进公开产物 —— 这三个数**不是**站点点名的口径，正文与标题一律不用它们。

**「出处」覆盖**：发布口径 2798 条里，2758 条（98.6%）填了具体的来源篇章；其中 911 条至少解析出一条可点击链接（与线上 `data/meta.json` 的 `citation_links.modes_with_link` 一致）。复核：

```bash
python3 tools/source_link_index.py --coverage
```

输出里 `modes with citations: 2165 | with >=1 linked citation: 911 = 42.1%` 一行即对应后者；`source_chapter` 非空条数用下面这段（只读本仓数据）复核，输出应为 `2798 2758 98.6`：

```bash
python3 - <<PY
import json, sys
sys.path.insert(0, "tools")
from _quarantine import drop_quarantined_modes
d = json.load(open("data/modes_data.json"))
pub, _ = drop_quarantined_modes(d["modes"])
pub = [m for m in pub if m.get("mode_code")]
have = [m for m in pub if str(m.get("source_chapter", "")).strip()]
print(len(pub), len(have), round(100 * len(have) / len(pub), 1))
PY
```

**正文例子**的各字段逐字取自 `data/modes_data.json` 中 `mode_code` 为 M381 的记录（附录二贴出源片段）；生卒年取自 `data/figures/H-WYM-001.json`（`birth_year` 1472、`death_year` 1529）。

**外链实测**（逐条 curl 跟随重定向，全部 200；测试时间 2026-09-21）：

```text
200  https://ovmobilegroup.github.io/protreptic/
200  https://ovmobilegroup.github.io/protreptic/modes/
200  https://ovmobilegroup.github.io/protreptic/figures/
200  https://ovmobilegroup.github.io/protreptic/concepts/
200  https://ovmobilegroup.github.io/protreptic/graph/
200  https://ovmobilegroup.github.io/protreptic/compare/
200  https://ovmobilegroup.github.io/protreptic/daily/
200  https://ovmobilegroup.github.io/protreptic/templates/
200  https://ovmobilegroup.github.io/protreptic/credibility/
200  https://ovmobilegroup.github.io/protreptic/api/
200  https://ovmobilegroup.github.io/protreptic/docs/
200  https://ovmobilegroup.github.io/protreptic/minds/H-WYM-001/
200  https://ovmobilegroup.github.io/protreptic/data/meta.json
200  https://github.com/ovmobilegroup/protreptic
200  https://github.com/ovmobilegroup/protreptic/blob/main/CONTRIBUTING.md
200  https://zh.wikisource.org/wiki/%E5%82%B3%E7%BF%92%E9%8C%84
```

**本卡没做、也不该由本卡做的事**：不发帖、不注册账号、不代投递；不承诺「权威认证」；不把未核验的部分说成已核验；不使用 2868 / 2858 这类源库内部计数当门面数字。

## 附录二 · 例子字段的源 JSON 片段（`data/modes_data.json`，`mode_code` 为 M381）

```json
{
  "id": "M381",
  "mode_code": "M381",
  "figure_code": "H-WYM-001",
  "figure_name": "王阳明",
  "name_zh": "致良知法",
  "name_en": "Conscience Cultivation Method",
  "category": "伦理修养",
  "definition_zh": "心之本体即良知，人人皆有良知，只需去除私欲遮蔽，使良知自然呈现。良知是判断是非善恶的根本标准，是道德自觉的源泉。",
  "process_zh": [
    "认识到人人皆有良知",
    "在具体事事物物中体认良知",
    "去除私欲对良知的遮蔽",
    "在道德实践中展现良知",
    "通过反省加深对良知的理解"
  ],
  "application_zh": "在道德判断中信任良知，在日常生活中践行良知，在困境中坚守良知。",
  "modern_parallel_zh": "现代道德心理学中的道德直觉、良知教育、品格养成教育",
  "source_chapter": "《传习录》",
  "key_quote_zh": "知善知恶是良知，为善去恶是格物",
  "verification": {
    "status": "verified",
    "method": "link-resolved",
    "evidence": "https://zh.wikisource.org/wiki/%E5%82%B3%E7%BF%92%E9%8C%84",
    "checked_at": "2026-09-21",
    "checker": "phase38-y2"
  }
}
```

以上片段即正文例子中定义、5 个操作步骤、现代应用、原话、出处的逐字来源。复核方式（在本仓执行）：

```bash
grep -n M381 data/modes_data.json | head -3
```
