# Phase38-Y1 交付报告：链接源重建（按书名索引 · 全量可达核验 · 高频书名覆盖）

- 卡：`t_d76b44c3`（assignee `serrano`）。下游：`t_c0c1c380`（Y2 构建期注入）、`t_b13d6382`（QA8 独立复验）。
- 必读依据：发布仓 `docs/planning/credibility_framework.md` §2 链接源 / §3 verification schema / §7 两档门 / §9 两仓一致边界。
- 方法：**产物真实落盘、逐条命令给原始输出、解析不到的诚实标 `unverifiable`、不塞假 URL**。

复验快照（本报告的数字都可用 §8 的命令复现）：

| 项 | 值 |
| --- | --- |
| 工作仓 `/opt/data/workspace/Protreptic` | `master` @ `a7d146c5`（起始），终态见 §9 |
| 发布仓 `/opt/data/release/Protreptic-publish` | `main` @ 起始 `7eeb56a`，终态见 §9 |
| 数据输入 | `data/modes_data.json`（2868 条模式 / 2165 条含《》引文） |
| 线上 | `https://ovmobilegroup.github.io/protreptic` |

---

## 0. 先纠一条前提（原始证据，不是抬杠）

卡的侦察记录写着：

> · `data/source_links.json` 现为**裸列表** `[{url,source_type,confidence}]`，缺按书名索引的 key

**实测不成立**：本仓该文件自入库起就是**按书名索引的 dict**（键带书名号），卡里引用的那条样本
`{"url":"https://ctext.org/wiki.pl?if=gb&chapter=605807",...}` 是 **`《传习录》` 这条目的值**。

```bash
$ cd /opt/data/workspace/Protreptic
$ git log --oneline -1 -- data/source_links.json
a7d146c5 Phase36-W3: CI integrate credibility_gate + verify_source_links, fix --data-path
$ sha256sum data/source_links.json
e1e1bf71f515a6e87e7dac61c59d98240913f71521d8f516357b5d2307bddaf6  data/source_links.json
$ head -c 150 data/source_links.json
{
  "《传习录》": {
    "url": "https://ctext.org/wiki.pl?if=gb&chapter=605807",
    "source_type": "ctext",
    "confidence": 0.95
  },
```

**为什么必须写清楚**：schema 不是本轮的工作量，`tools/source_link_index.py::load_index()` 现在对裸列表
**直接报错**（防静默降级），QA 复验时应以「dict 且键为 `《…》`」为准，而不是去找一个不存在的 schema 迁移。

其余三条侦察结论复核（全部成立，逐条给出处）：

| 侦察结论 | 复核 | 证据 |
| --- | --- | --- |
| 50 条中仅 40 有 url | **成立**：40 有 url（其中 1 条 404、1 条站点不可达），10 条 url 为空（8 条《苏咸子》系列伪出处 + 2 条） | §3.1 起始态输出 |
| 抽验 5 条有 1 条 404 | **成立**：`https://archive.org/details/tienhocsinhuan` 实测 404（archive.org 检索 `title:("tien hoc sinh hoan")` = `numFound 0`） | §3.3 |
| `verification` 全 `pending` | **成立**：2868 条全 `pending`（schema 就位、未核验） | §3.4 |
| 被引书名 2169 种 / ≥3 次约 385 种 | **量级成立**：本仓实测 distinct 2174 种、≥3 次 374 种、≥5 次 163 种 | §4.1 |

---

## 1. 匹配规则（出处 → 链接，R0-R3）

规则写在唯一实现 `tools/source_link_index.py`（导出链、构建期注入、QA 全部复用它，避免三处各写一份）。
本节与代码 docstring **逐条一致**：

| 代号 | 规则 |
| --- | --- |
| **R0** | 用正则 `《([^》]{1,60})》` 抓 `source_chapter` 中**全部**书名号跨度；每个跨度是一条「引文 citation」。没有书名号 → 0 条引文（**不猜**）。 |
| **R1** | 对引文内文 `T` 生成候选 key，按优先级命中即止：<br>**P1 精确** `《T》`（章级 key 覆盖书级 key）<br>**P2 去章名** `T` 按 `·` 逐级右截：`A·B·C` → `《A·B》` → `《A》`<br>**P3 去缀语** 去尾部括注/说明性后缀后重试 P1/P2（如 `《天工开物》及相关论著` → `《天工开物》`） |
| **R2** | 第一个存在于索引的候选 key 即命中，取其 `url`（可为空 = 已登记**不可链接**）。 |
| **R3** | 全部候选都不在索引 → `unresolved`，**保持纯文本，不伪造链接**。 |

设计要点（都是踩过的坑）：

- `·` 既可能是「书·篇」（`《史记·张仪列传》`）也可能是人名书名（`《埃隆·马斯克》`）。
  **P1 精确优先、只有精确不存在才右截**，所以人名书名不会被误拆。
- key **带书名号**、用字与 `source_chapter` 一致（简体）；`url` 可指向源站繁体标题页
  （`zh.wikisource` 的 canonical title 是繁体，「键简体、链繁体」是源站事实，不是错配）。
- `source_chapter` 实测有 **30 条是 list**（不是字符串），`_as_text()` 统一拼接，避免解析器崩在类型上。

样例（§8 复跑入口可原样执行）：

```bash
$ python3 tools/source_link_index.py --sample "《史记·张仪列传》《战国策·秦策一》；朱熹《大学章句·格物补传》、《朱子语类》卷十"
index keys: 382  (/opt/data/workspace/Protreptic/data/source_links.json)
{"citation": "史记·张仪列传", "key": "《史记》", "url": "https://zh.wikisource.org/wiki/%E5%8F%B2%E8%A8%98", "source_type": "wikisource", "confidence": 0.9, "status": "linked", "match_rule": "prefix"}
{"citation": "战国策·秦策一", "key": "《战国策》", "url": "https://zh.wikipedia.org/wiki/%E6%88%B0%E5%9C%8B%E7%AD%96", "source_type": "wikipedia", "confidence": 0.6, "status": "linked", "match_rule": "prefix"}
{"citation": "大学章句·格物补传", "key": null, "url": "", "source_type": null, "confidence": null, "status": "unresolved", "match_rule": null}
{"citation": "朱子语类", "key": "《朱子语类》", "url": "https://zh.wikisource.org/wiki/%E6%9C%B1%E5%AD%90%E8%AA%9E%E9%A1%9E", "source_type": "wikisource", "confidence": 0.9, "status": "linked", "match_rule": "exact"}
{"citation": "苏咸子·权变篇", "key": "《苏咸子·权变篇》", "url": "", "source_type": "unverifiable", "confidence": 0.0, "status": "unverifiable", "match_rule": "exact"}
```

---

## 2. schema（本轮定稿，向后兼容）

`data/source_links.json`：**顶层 dict**，键 = `《书名或事件名》`，值：

| 字段 | 必需 | 含义 |
| --- | --- | --- |
| `url` | ✅ | 权威源页面（**已 curl 实测 200 且正文含源站标题**）；不可链接时为空串 |
| `source_type` | ✅ | `wikisource` / `wikipedia` / `gutenberg` / `archive` / `ctext` / `unverifiable` |
| `confidence` | ✅ | 0–1；`wikisource` 0.8–0.9、`wikipedia`(著作条目) 0.6、`gutenberg` 0.85、`ctext` 存量原值 |
| `canonical_title` | 链接项 | 源站上的标题（繁简由源站决定），核验时用作正文命中词 |
| `provider` | 链接项 | 解析来源（`zh.wikisource` / `zh.wikipedia (wikidata P31)` / `Project Gutenberg` …） |
| `checked_at` | ✅ | 核验日期 |
| `note` | 可选 | 边界说明（如 ctext 正文被挑战页拦截） |
| `reason` | `unverifiable` | 不可链接的理由（人可读、可复核） |

结构样例：

```json
{
  "《史记》": {
    "url": "https://zh.wikisource.org/wiki/%E5%8F%B2%E8%A8%98",
    "source_type": "wikisource",
    "confidence": 0.9,
    "canonical_title": "史記",
    "provider": "zh.wikisource",
    "checked_at": "2026-09-20"
  },
  "《苏咸子·权变篇》": {
    "url": "",
    "source_type": "unverifiable",
    "confidence": 0.0,
    "reason": "D2 伪造出处：《苏咸子》不存在于任何权威目录（与 data/audit/findings.json 一致）",
    "checked_at": "2026-09-20"
  }
}
```

> 不可链接项**也登记进索引**（`url` 为空）——这样构建期（Y2）能一眼判定某条出处属
> 「已登记不可链接」，从而写 `verification.status = unverifiable`，而不是「没匹配上」。

---

## 3. 全量可达核验（逐条 curl，不抽样）

核验器：`tools/verify_source_links.py`（Phase37-X3 两档门：存量冻结 / 新增即拦）。

### 3.1 起始态（重建前，50 条）

```bash
$ python3 tools/verify_source_links.py --jobs 2 --legacy-report | tail -12
Summary: 38 OK, 1 dead, 1 unreachable, 10 unverifiable
--- 存量坏链（基线内，冻结）: 1 条 ---
  ::notice::LEGACY [DEAD 404] 《天学初函》 -> https://archive.org/details/tienhocsinhuan
--- 连接层失败（警告，不计违规）: 1 条 ---
  ::warning::UNREACHABLE 《德川幕府制度研究》 -> https://openlibrary.org/search?q=Tokugawa+shogunate
[OK] legacy-report: 存量 1 / 新增 0 —— 只报告，不阻断 (exit 0)
```

### 3.2 终态（重建后，382 条）

```bash
$ python3 tools/verify_source_links.py --jobs 1 --max-time 8 --write-baseline
Checking 382 source links... (jobs=1, max-time=8s)
...
  [OK 200] 《齐民要术》 -> https://zh.wikisource.org/wiki/%E9%BD%8A%E6%B0%91%E8%A6%81%E8%A1%93

Summary: 169 OK, 0 dead, 0 unreachable, 213 unverifiable
resolved links path:    /opt/data/workspace/Protreptic/data/source_links.json
resolved baseline path: /opt/data/workspace/Protreptic/data/audit/source_links_baseline.json (exists=True)
baseline frozen at 2026-09-20T01:10:11+00:00 counts={"violations": 0, "distinct": 0}
$ echo $?
0

$ python3 tools/verify_source_links.py --jobs 2 --max-time 10 --hard-fail
Summary: 169 OK, 0 dead, 0 unreachable, 213 unverifiable

--- 存量坏链（基线内，冻结）: 0 条 ---

--- 新增坏链（基线外，必拦）: 0 条 ---

[OK] hard-fail: 无新增坏链（存量 0 条已冻结）-> exit 0
$ echo $?
0
```

**结论：失败 0** —— 两次独立全量核验均为 `169 OK / 0 dead / 0 unreachable / 213 unverifiable`
（`--jobs 1` 与 `--jobs 2` 各一遍，见 §3.5 对限流的说明）。坏链基线已按新索引**重新冻结为 0 条**
（旧的唯一存量坏链《天学初函》本轮已处置，见 3.3）。

### 3.3 404 / 超时的逐条处置

| 条目 | 起始态 | 处置 | 终态 |
| --- | --- | --- | --- |
| `《天学初函》` | `https://archive.org/details/tienhocsinhuan` **404** | archive.org 检索 `title:("tien hoc sinh hoan")` = `numFound 0`；zh.wikisource 无 `天學初函`；wikipedia 无著作条目 → **删除死链，登记 unverifiable** | `url: ""`，`reason` 见 §5 |
| `《德川幕府制度研究》` | `openlibrary.org` **主机不可达**（curl 000，重试仍 0） | 该站本环境不可达 → 依「必须 curl 200」逐条剔除；未找到可达替代源 | `url: ""`，`reason` 见 §5 |
| `《苏咸子·纵横篇》` 等 8 条 | `url: ""`（type=unverifiable） | 保持不可链接，理由写实（D2 伪造出处） | `url: ""` |

### 3.4 `verification` 字段现状（如实：本轮**不动**它）

```bash
$ grep -o '"status": "pending"' data/modes_data.json | wc -l
2888
$ grep -o '"status": "verified"' data/modes_data.json | wc -l
0
$ grep -o '"status": "unverifiable"' data/modes_data.json | wc -l
0
$ grep -o '"status": "suspect"' data/modes_data.json | wc -l
0
```

2888 处 `"status": "pending"`（`modes[]` 数组 2868 条 + 两处嵌套分组 `H-ASM-001` / `H-ZZ-001` 各 10 条），
三态（`verified` / `unverifiable` / `suspect`）计数**均为 0** —— 与卡的侦察一致。推到 `verified/unverifiable/suspect`
是 **Y2（`t_c0c1c380`）** 的交付项（框架 §3 定义的推进规则），不是本轮；本轮只把
「出处 → 是否可链接」这条链路做成可信输入。

### 3.5 关于 HTTP 429（本轮补的机制，必须说清）

链接源从 50 条扩到 169 条后，**143 条落在 Wikimedia 主机**（zh.wikisource / zh.wikipedia）。
实测：`curl` 连打会被源站限流成 **429**；而 Phase37-X3 的两档门把 4xx 当「确定性坏链」，
一旦算违规，CI 会**被网络抖动打红**（与 §7 的说法同构，但 429 属于限流而非资源消失）。

处置（`tools/verify_source_links.py`）：

- `429 / 503` 归为**可重试**：指数退避重试 3 次；重试后仍失败 → 记 `unreachable`（**警告**，不计违规），
  并保留状态码供人工判断；
- 默认并发从 8 降到 4（`--jobs` 可调），降低触发限流的概率；
- 语义变化只影响 **429/503** 两个码；其余 4xx/5xx 仍是**确定性坏链**，照旧进「存量 / 新增」判定。

---

## 4. 覆盖率（50 → 382）

### 4.1 前后对照

| 指标 | 重建前 | 重建后 | 出处（§8 复跑） |
| --- | --- | --- | --- |
| 索引 key 数 | 50 | **382** | `python3 tools/source_link_index.py --coverage` |
| 有 url（实测 200） | 38 | **169** | §3.2 全量核验输出 |
| 登记不可链接（`unverifiable`） | 10 | **213** | 同上 |
| 引文可点击率（4 016 条《》引文） | 94 / 4 016 = **2.3%** | **1 147 / 4 016 = 28.6%** | `--coverage` |
| 模式至少一条引文可点（2 165 条含引文模式） | **0** | **911 / 2 165 = 42.1%** | `--coverage` |
| 被引 ≥3 次书名覆盖率 | 0 | **178 / 374 = 47.6%** | `--coverage` |
| 被引 ≥3 次的**书级名**（按 `·` 归并）覆盖率 | 0 | **150 / 361 = 41.6%** | `--coverage` |

`--coverage` 的原始输出：

```bash
$ python3 tools/source_link_index.py --coverage
index keys: 382  (/opt/data/workspace/Protreptic/data/source_links.json)
citations: 4016  linked=1147  registered-unlinkable=950  unresolved=1919
coverage = 1147/4016 = 28.6%

distinct cited names: 2174 | >=3: 374
names >=3 linked: 178/374 = 47.6%  (registered-unverifiable 196)
base names >=3: 361 | linked: 150 = 41.6%
modes with citations: 2165 | with >=1 linked citation: 911 = 42.1%
index keys: 382 | with url: 169 | unverifiable: 213
provider distribution: {"wikipedia": 76, "wikisource": 125, "gutenberg": 6, "ctext": 3}
unverifiable reasons: {"泛指表述，无唯一书名可指": 11, "权威源未检索到匹配条目（书名不规范或无数字化版本）": 203, "自指书名，非公开出版物，无可核验源": 1, "D2 伪造出处：《苏咸子》不存在于任何权威目录（与 data/audit/findings.json 一致）": 9}
```

> 口径说明：`citations` 的 `linked=1147` 是「按引文逐条判定」；`registered-unlinkable=950` 指引文命中的是
> **已登记不可链接**条目（构建期据此写 `unverifiable`）；`unresolved=1919` 是索引里根本没有的书名
> （构建期**保持纯文本**，状态留 `pending`）。

### 4.2 来源类型分布（169 个可点击链接）

| source_type | 数量 | 说明 |
| --- | --- | --- |
| `wikisource`（zh） | 125 | 中文公版古籍/文集，**正文可回读**，confidence 0.8–0.9 |
| `wikipedia`（zh，Wikidata P31 = 著作） | 76 | 书目级条目（无免费全文的西方/现代著作），confidence 0.6 |
| `gutenberg` | 6 | 西文公版（含 Proj. Gutenberg 作者页） |
| `ctext` | 3 | **存量保留**（见 §6.1，正文被挑战页拦截，已加 `note`） |

---

## 5. 不可链接清单与典型原因

共 **213 条** `unverifiable`（机读全清单：`data/audit/source_link_coverage.json` 的 `entries[]`）。
理由分四类：

| 理由 | 条数（按被处理名） | 典型例子 |
| --- | --- | --- |
| 权威源未检索到匹配条目（书名不规范或无数字化版本） | 203 | `《普通语言学教程》`、`《民主主义与教育》`、`《华罗庚传》`、`《竺可桢日记》`、`《晏阳初全集》` |
| 泛指表述，无唯一书名可指 | 11 | `《自传》`、`《历史》`、`《南极》`、`《巴黎评论》`、`《评注》`、`《通论》`、`《词论》` |
| D2 伪造出处（《苏咸子》不存在于任何权威目录） | 9 | `《苏咸子》`、`《苏咸子·权变篇》` …（与 `data/audit/findings.json` 的 D2 同集合） |
| 自指书名，非公开出版物 | 1 | `《卓特思维模式考辨》` |
| **合计** | **224** | 其中**索引里登记为 `unverifiable`（`url: ""`）的是 213 条**；差额来自「章级名未解析、但书级名已命中链接」的情况（如 `《旧唐书·李靖传》` 经 `《旧唐书》` 落链），不额外占索引 key |

**典型原因归纳**（给后续挖矿卡的启示，不是借口）：

1. **现代在版著作**（伊萨克森《埃隆·马斯克》、李光耀回忆录、稻盛和夫《活法》）——
   无公版全文/开放权威页；框架 §2 允许的 OpenLibrary 在本环境**主机不可达**，故只登记不链接。
2. **中文近现代文集/日记/演讲录**（《竺可桢日记》《胡志明全集》《晏阳初全集》）——
   未数字化或未开放，属一手材料。
3. **非唯一指称**（`《自传》` `《历史》` `《南极》`）——书名号里写的是泛指，不存在唯一权威源，**拒绝对号入座**。
4. **书名写法与权威目录不一致但仍可定位者已尽量救回**：如 `《史记·张仪列传》` 靠 R1-P2 落到 `《史记》`。

---

## 6. 本轮发现的既有缺陷与处置（原始证据）

### 6.1 ctext 章节深链：HTTP 200，但正文是 Cloudflare 挑战页

实测（本机 `curl` 与**真实浏览器**都验了）：

```bash
$ curl -s -o /dev/null -w "%{http_code}\n" -L -A "Mozilla/5.0" \
    "https://ctext.org/wiki.pl?if=gb&chapter=605807"
200
$ curl -s -L -A "Mozilla/5.0" "https://ctext.org/wiki.pl?if=gb&chapter=605807" | head -c 120
<html xmlns="http://www.w3.org/1999/xhtml" ...><title>Chinese Text Project</title>...
Checking the security of your connection...
```

即：**链接可达（200）但正文不可回读**（浏览器同结果：`document.body.innerText` 只有
「Checking the security of your connection...」与订阅提示）。因此：

- 本轮把**有可回读替代源**的存量章节级 ctext 链**换成书级 wikisource 链**。口径：起始索引
  （`git show a7d146c5:data/source_links.json`）的 50 个 key 里，**20 个在终态索引中消失**
  （19 个落到书级 wikisource 链，1 个是带缀语的复合 key，由 R1-P3 后缀规则覆盖），逐条见
  `data/audit/source_link_coverage.json` 的 `chapter_keys_replaced_from_baseline[]`：

```bash
$ git show a7d146c5:data/source_links.json > /tmp/idx0.json
$ python3 -c "
import json
a=json.load(open('/tmp/idx0.json')); b=json.load(open('data/source_links.json'))
print(len([k for k in a if k not in b]), 'keys removed')"
20 keys removed
$ # 逐条映射见 chapter_keys_replaced_from_baseline[]，例如：
$ #   《史记·卫将军骠骑列传》 -> 《史记》   https://zh.wikisource.org/wiki/史記
$ #   《正蒙·太和篇》         -> 《正蒙》   https://zh.wikisource.org/wiki/正蒙
$ #   《商君书·垦令》         -> 《商君书》 https://zh.wikisource.org/wiki/商君書
```

- 只有 **2+1 = 3 条**没有替代源时保留 ctext（`《史记》多篇综合`、`《天工开物》及相关论著`、`《焚书》《藏书》`），
  并在条目里加 `note`；这 3 个 key 的三种写法都不是任何一条引文的内文（引文侧由 `《史记》`/`《天工开物》`/
  `《焚书》`+`《藏书》` 各自命中），因此不会把「不可回读正文」的链接送进 `verification.evidence`。
- **给 Y2/QA 的提醒**：`ctext` 条目的 `url` 可用于展示，但**不要**把它们当「正文已核验」的
  `verification.evidence`（QA8 抽查「evidence url 内容相关」时会被挑战页绊倒）。

### 6.2 「同标题 ≠ 同著作」误命中：2 例，已剔除并留证

自动解析靠「标题精确匹配」，对**短标题**会撞车。人工复核全部 169 条命中时抓到 2 例：

| 书名 | 误命中页 | 分类证据（源站 `wgCategories`） | 处置 |
| --- | --- | --- | --- |
| `《野鸭》` | zh.wikisource `野鴨` | `["75%","李群玉","唐朝","唐诗","五言絕句"]` —— 唐代李群玉的**同名诗**，非易卜生剧作 | 剔除，登记 `unverifiable` |
| `《忏悔录》` | zh.wikisource `懺悔錄` | `["黃遠生","1915年議論性散文","中華民國4年"]` —— 黄远生 1915 年散文，非奥古斯丁《忏悔录》 | 剔除，登记 `unverifiable` |

两例已写进 `tools/build_source_links.py::REJECT_HITS`（带理由），重复跑不会复活。

### 6.3 消歧义页过滤（本轮补的）

- wikisource/wikipedia 的 `pageprops.disambiguation` 标记，**以及**标题含 `消歧義/消歧义/(消歧義)` 的页，
  一律不算命中。修前实测漏网一例：`《三国志通俗演义》` → `三國演義 (消歧義)`（`wgPageLength=1000`
  的导航页）；修后落到 zh.wikipedia 的 `三国演义` 条目。

### 6.4 命中质量的两道闸（不是「标题对上就算」）

1. **书级回落**：`《旧唐书·李靖传》` 这类章级写法，先试全名，再按 `·` 回落书级名（`《旧唐书》`）。
2. **Wikipedia 条目必须被 Wikidata 认定为「著作」**：读条目 `pageprops.wikibase_item` → 查 `P31`，
   命中 `Q571`(book)/`Q47461344`(written work)/`Q7725634`(literary work)/`Q8261`(novel)/… 才算数。
   这条闸把「书名挂到同名人物/组织/事件条目」的误命中挡在门外（实测有效：`《野鸭》` 在 zh.wikipedia
   会 redirect 到动物条目 `鸭`，`P31=Q3736439`，直接被拒）。

---

## 7. 与下游（Y2）的接口 · 本轮**没有**改站点数据

- 供 Y2 直接 import 的 API（`tools/source_link_index.py`）：
  `load_index()` / `extract_refs(source_chapter)` / `candidate_keys(inner)` /
  `resolve_source_chapter(source_chapter, index)` → 每条引文返回
  `{citation, key, url, source_type, confidence, status, match_rule}`，
  其中 `status ∈ {linked, unverifiable, unresolved}`：
  `linked` → 写 `verification.status = verified`（`method=link-resolved`, `evidence=url`）；
  `unverifiable` → 写 `unverifiable`；`unresolved` → 保持**纯文本**、状态留 `pending`。
- **本轮不改站点数据**，证据（`source_links.json` 目前没有任何构建步骤读取）：

```bash
$ grep -rn "source_links" tools/*.py web/src/**/*.ts web/src/**/*.vue .github/workflows/*.yml \
    | grep -v "^tools/build_source_links.py\|^tools/source_link_index.py\|^tools/verify_source_links.py"
.github/workflows/pages.yml:36:      - 'data/source_links.json'    # on.push.paths 触发器
.github/workflows/pages.yml:105:     run: python3 tools/verify_source_links.py --legacy-report
```

  即：只有「门」和「触发器」引用它，**没有导出/渲染步骤消费它**。
  故 §5 的构建顺序（`build_figures_db → export_static_site → build_unified_index → apply_site_counts`）
  **本轮无需重跑**（重跑不会改变任何产物）；接线在 Y2 做，那时再按该顺序重建并过 `npm run build`。

---

## 8. 复跑入口（一句话一条）

```bash
# 0) 前置：从仓内已提交的索引出发（本轮交付就是把这条命令跑出来的结果并入）
cd /opt/data/workspace/Protreptic

# 1) 重建索引 + 覆盖报告（会写 data/source_links.json 与 data/audit/source_link_coverage.json）
python3 tools/build_source_links.py                 # 加 --dry-run 只解析不写；--review 打印命中清单

# 2) 逐条可达核验（200 + 正文含源站标题）
python3 tools/verify_source_links.py --jobs 3 --write-baseline   # 全量核验并重冻基线
python3 tools/verify_source_links.py --jobs 3 --hard-fail        # CI 口径

# 3) 匹配规则自检 / 覆盖率自算
python3 tools/source_link_index.py --sample "《史记·张仪列传》；《焚书》《藏书》"
python3 tools/source_link_index.py --coverage                     # 全库引文命中 + 覆盖率对照

# 4) 两仓一致（边界 = 构建图，含 data/**、docs/**、构建脚本）
python3 tools/check_repo_parity.py
```

**复现性声明（如实）**：解析要打源站 API，单次运行的命中数受**源站限流**影响，实测同一命令
相邻两次可有 ±10 条浮动（如 150 → 169）。索引更新语义是**单调保底**的：已经实测 200 的链接会被
保留（`--links-path` 既作输入又作输出），新一轮解析结果并入，不会把可点链接改回不可点。

---

## 9. 交付与同步

| 文件 | 说明 |
| --- | --- |
| `data/source_links.json` | 按书名索引（382 key / 169 可点 / 213 不可链接） |
| `data/audit/source_link_coverage.json` | **机读覆盖报告**（逐条：name/key/status/citations/url/provider/reason；含 provider 分布、起始索引里被书级链替代的 20 个 key、存量链接重测结果） |
| `data/audit/source_links_baseline.json` | 坏链基线（本轮重冻为 **0 条**） |
| `tools/source_link_index.py` | 匹配规则 R0-R3 唯一实现（新增） |
| `tools/build_source_links.py` | 索引重建器（新增，可复跑） |
| `tools/verify_source_links.py` | 加 429/503 重试与非违规归类；默认并发 4 |
| `tools/check_repo_parity.py` | 把上面两个新工具纳入两仓一致边界 |
| `docs/qa/link_coverage.md` | 本报告 |

同步台账与 push 回读见 §10（**提交后**追加，避免自指哈希失效）。
