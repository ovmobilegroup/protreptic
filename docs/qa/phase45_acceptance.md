# Phase45-QA10 独立复验报告：统计注入正确性 + 知乎草稿事实性

- 卡片：`t_b4488d02`（[Phase45-QA10] 复验：统计注入正确性 + 知乎草稿事实性）
- 复验人：espinosa（QA，独立跑命令，只贴原始输出）
- 时间：2026-09-21（CST）
- 复验对象：
  - 项目仓 `/opt/data/workspace/Protreptic`（HEAD `342007e3`，`git status -sb` 为 `## master`，干净）
  - 发布仓 `/opt/data/release/Protreptic-publish`（HEAD `5113530`）
  - 线上站点 `https://ovmobilegroup.github.io/protreptic/`
  - 知乎草稿 `docs/community/zhihu_launch_post.md`（sha256 `215f3d50a99a3a4e20852d0a9f5a0c5800112807ab8bc94efe4a32f76328bf3c`，246 行）
- 卡片给定的判据：谎报或空渲染一律 FAIL；每条结论给命令与输出。

## 结论

**可发布（PASS）**。

A 组（统计注入）4 项全过；B 组（知乎草稿）4 项全过。
另有 3 条**非阻断观察**（见文末「观察」节），不影响发布判定，供船长决定是否在发布前顺手改一两个字的措辞。

---

## 【A 统计】

### A-1 无 code 构建 → dist/index.html 无 goatcounter 【PASS】

复现方式：临时把 `web/goatcounter.json` 的 `code` 置空 → 构建 → 计数 → 还原（还原后确认 `code` 仍为 `protreptic`）。

命令与输出（脚本 `/tmp/qa10_a1.py`，核心即 `cd web && VITE_DATA_MODE=static npm run build`）：

```text
[A1] goatcounter.json code set to EMPTY (temporary)
[A1] build exit: 0
[A1] build tail: ['dist/index.html                   3.84 kB │ gzip:   2.28 kB', 'dist/assets/index-uLX7QpAY.css   50.37 kB │ gzip:   9.43 kB', 'dist/assets/index-CALgjOtJ.js  354.46 kB │ gzip: 130.20 kB', '✓ built in 4.60s']
[A1] dist/index.html grep -c -i goatcounter = 0
[A1] dist/index.html sha256 = fa2af346b3e5b23792a1cfb544661987ecd2e2f7c5b1975246a2599f4a46f21a
[A1] dist/404.html grep -c -i goatcounter = 0
[A1] dist/404.html sha256 = fa2af346b3e5b23792a1cfb544661987ecd2e2f7c5b1975246a2599f4a46f21a
[A1] restored goatcounter.json code = protreptic
```

判据核对：`grep -c -i goatcounter dist/index.html` = **0**，且与 t_eb3de8e7 自述的 sha256 `fa2af346…` **逐字节一致**。缺口最小化成立：缺省态一个字节都不注入。

### A-2 有 code 构建 → data-goatcounter URL 正确 【PASS】

命令（`VITE_GOATCOUNTER_CODE=abc123` 覆盖文件开关，脚本 `/tmp/qa10_a2.py`）：

```text
[A2] build exit: 0 | ✓ built in 4.40s
[A2] ---- dist/index.html lines containing goatcounter ----
  82: <script data-goatcounter="https://abc123.goatcounter.com/count" async src="/protreptic/count.js"></script>
[A2] ---- dist/404.html lines containing goatcounter ----
  82: <script data-goatcounter="https://abc123.goatcounter.com/count" async src="/protreptic/count.js"></script>
```

说明：卡片⑵原文写的判据是 `gc.zgo.at`，但当前仓库已把 count.js 自托管（`web/public/count.js`，ISC），注入的 `src` 是 `${BASE_PATH}count.js`。按「以当前仓库代码为判据」，端点 `data-goatcounter="https://abc123.goatcounter.com/count"` **正确**，与站点码一致，且 `404.html` 与 `index.html` 同源（预渲染深链的壳即 `dist/index.html`，见 A-4 证据）。

### A-3 「缺省上线态：线上首页 curl 确认无分析脚本」【PASS（判据已更新为两态实测）】

**卡片此条前提已过期**（实现方 acurio 已在评论中提示）：线上窗口内被并行提交 `cd14ba6` 激活（`web/goatcounter.json` 的 `code = protreptic`，用户已注册）。因此线上**不是** inert 态，无法用线上 curl 观察「无脚本」。按「不复读自述、自己取证」的要求，本项拆成两段各自实测：

（a）**线上实测 = 激活态**（curl 原始输出）：

```text
$ curl -s -o /tmp/qa10_live_index.html -w "%{http_code}\n" https://ovmobilegroup.github.io/protreptic/
200
$ grep -n -o 'data-goatcounter="[^"]*"' /tmp/qa10_live_index.html
72:data-goatcounter="https://protreptic.goatcounter.com/count"
$ grep -c -i goatcounter /tmp/qa10_live_index.html
1

$ curl -s -o /tmp/qa10_live_minds.html -w "minds/H-WYM-001 HTTP=%{http_code}\n" https://ovmobilegroup.github.io/protreptic/minds/H-WYM-001/
minds/H-WYM-001 HTTP=200
$ grep -o 'data-goatcounter="[^"]*"' /tmp/qa10_live_minds.html   # 深链预渲染页
data-goatcounter="https://protreptic.goatcounter.com/count"
$ grep -o 'src="[^"]*count.js"' /tmp/qa10_live_minds.html
src="/protreptic/count.js"

$ curl -s -o /tmp/qa10_live_404.html -w "404.html HTTP=%{http_code}\n" https://ovmobilegroup.github.io/protreptic/404.html
404.html HTTP=200
$ grep -o 'data-goatcounter="[^"]*"' /tmp/qa10_live_404.html
data-goatcounter="https://protreptic.goatcounter.com/count"

$ curl -s -o /tmp/qa10_live_countjs.js -w "count.js HTTP=%{http_code}\n" https://ovmobilegroup.github.io/protreptic/count.js
count.js HTTP=200
$ sha256sum /tmp/qa10_live_countjs.js /opt/data/workspace/Protreptic/web/public/count.js
792b7abd26c1fb6ae62906833e09a301251e2641816e69e4f95aba518f3fe3f0  /tmp/qa10_live_countjs.js
792b7abd26c1fb6ae62906833e09a301251e2641816e69e4f95aba518f3fe3f0  /opt/data/workspace/Protreptic/web/public/count.js
```

线上：首页 / 404.html / 深链页**各 1 条** `data-goatcounter`，站点码正确（`protreptic`，非占位域名）；自托管 count.js 线上字节与本地同源一致。

（b）**inert 态实测 = 本地构建复现**（线上窗口已错过，只能本地取证；即 A-1）：`grep -c -i goatcounter dist/index.html` = **0**，sha256 `fa2af346…` 与实现方自述一致。

（c）**浏览器行为实测（自己跑，不采信自述）**：把 A-1 的 inert 产物与激活产物分别用 `python3 -m http.server` 起在 127.0.0.1:4178 / :4179，用真实浏览器打开 `/protreptic/`，`Page.addScriptToEvaluateOnNewDocument` 预挂 error/unhandledrejection 钩子：

```json
// inert（4178）
ROOT: {"url": "http://127.0.0.1:4178/protreptic/figures",
 "title": "🐴 历史人物库 - 统一名录 | Protreptic 思想典藏",
 "scriptTag": false, "gcType": "undefined",
 "canonical": "https://ovmobilegroup.github.io/protreptic/figures/",
 "errs": [], "appTextLen": 1257,
 "gcRes": []}
```

即：inert 态**没有** `script[data-goatcounter]`、`window.goatcounter` 为 `undefined`、**零条** goatcounter/count.js 资源请求、控制台零错误、应用正常渲染（同时证明 `/` → `/figures` 重定向路径本身工作正常）。

激活态同法实测见 A-4。

### A-4 无占位域名/404 脚本残留 + SPA 路由钩子未破坏 SEO/路由 【PASS】

（a）残留扫描（在 `web/dist` 内）：

```text
grep -rl -i 'YOUR_INSTANCE' dist      -> exit 1 | (no match)
grep -rl -i 'gc.zgo.at' dist          -> exit 1 | (no match)
grep -rl -i 'https://.goatcounter' dist -> exit 1 | (no match)
grep -rl -i 'placeholder' dist        -> exit 0 | dist/data/modes/by-figure/Khwarizmi.json
                                                  dist/assets/index-uLX7QpAY.css
                                                  dist/assets/index-CALgjOtJ.js
[A4] count.js present in dist: True
```

后三条 `placeholder` 命中经上下文核对与统计无关，不是占位脚本：

```text
input::placeholder,textarea::placeholder{opacity:1;color:#9c…          （Tailwind 生成物）
x.placeholder=re.el / if(e.placeholder)return e.placeholder;…          （Vue 运行时生成物）
…give it a definite symbol and placeholder rule so ambiguity dies;…    （data 里「零」这条模式的英文正文）
```

即：无 Phase30-C3 那类 `YOUR_INSTANCE` 占位符、无指向第三方 CDN 的坏脚本、无 `https://.goatcounter` 空码 URL；预渲染深链（`/minds/H-WYM-001/`）现场回读带的是**完整正确端点**（见 A-3(a) 的深链 grep），说明 `tools/prerender_routes.py` 以 `dist/index.html` 为壳的做法确实让注入自动覆盖深链与 404。

（b）构建与路由/SEO 回归：

```text
本轮共 4 次 `cd web && VITE_DATA_MODE=static npm run build` → exit 0（inert×2 / abc123×1 / protreptic×1）
web/package.json 的 scripts 只有 dev/build/preview/lint —— 仓库内没有前端单测入口，故按卡片「跑现有测试或构建」以构建 + 浏览器行为验证为闸门。
```

浏览器实测（激活产物 4179，脚本预挂了错误钩子与 goatcounter.count 打桩）：

```json
ROOT: {"url": "http://127.0.0.1:4179/protreptic/figures",
 "title": "🐴 历史人物库 - 统一名录 | Protreptic 思想典藏",
 "scriptTag": true,
 "tag": "<script data-goatcounter=\"https://protreptic.goatcounter.com/count\" async=\"\" src=\"/protreptic/count.js\"></script>",
 "srcAttr": "/protreptic/count.js",
 "gcType": "object", "stubbed": true, "errs": [],
 "hitsOnLoad": [{"path": "/protreptic/figures", "title": "历史人物库 - 统一名录 | Protreptic 思想典藏"}],
 "gcRes": ["http://127.0.0.1:4179/protreptic/count.js"]}
```

```json
// 站内跳转 /figures → /minds/H-MIY-001（SPA history 模式）
click: {"clicked": "/protreptic/minds/H-MIY-001", "before": "http://127.0.0.1:4179/protreptic/figures"}
AFTER: {"url": "http://127.0.0.1:4179/protreptic/minds/H-MIY-001",
 "title": "宫崎骏 - 思维模式档案 10 条 | Protreptic 思想典藏",
 "hits": [{"path": "/protreptic/figures", "title": "历史人物库 - 统一名录 | Protreptic 思想典藏"},
          {"path": "/protreptic/minds/H-MIY-001", "title": "人物模式档案 | Protreptic 思想典藏"}],
 "errs": []}
```

结论：

- 激活态**恰好 1 条**注入标签，`src` 为自托管 `/protreptic/count.js`（本地实测资源请求只有它一条，**没有**对 `gc.zgo.at` 的请求），`window.goatcounter` 为 object；
- 首屏不重复计数：进入时 `/` 由 count.js 计一次，路由改写后补报 `/protreptic/figures` 一次（`hitsOnLoad` 仅 1 条）；
- 站内跳转补报 +1 条、路径正确、**零控制台错误**；
- 路由与 SEO 未被破坏：`document.title` 与 `link[rel=canonical]` 均为本路由值，线上全部 11 个入口 200（见 B-6），深链页 title/canonical 正确（`王阳明 - 思维模式档案 10 条 | Protreptic 思想典藏` / `…/minds/H-WYM-001/`）。

---

## 【B 知乎草稿】

草稿 sha256 `215f3d50a99a3a4e20852d0a9f5a0c5800112807ab8bc94efe4a32f76328bf3c`。

### B-5 正文例子的逐字回对（`data/modes_data.json`，`mode_code` = M381）【PASS】

脚本 `/tmp/qa10_m381.py`：把草稿全文读入，逐字段查「该字段值是否原样出现在草稿里」。

```text
[B5] name_zh: '致良知法'                        in_draft=True
[B5] name_en: 'Conscience Cultivation Method'    in_draft=True
[B5] definition_zh: '心之本体即良知，人人皆有良知，只需去除私欲遮蔽，使良知自然呈现。良知是判断是非善恶的根本标准，是道德自觉的源泉。'  in_draft=True
[B5] application_zh: '在道德判断中信任良知，在日常生活中践行良知，在困境中坚守良知。'  in_draft=True
[B5] modern_parallel_zh: '现代道德心理学中的道德直觉、良知教育、品格养成教育'  in_draft=True
[B5] key_quote_zh: '知善知恶是良知，为善去恶是格物'  in_draft=True
[B5] source_chapter: '《传习录》'                 in_draft=True
[B5] process_zh steps:
      '认识到人人皆有良知'          in_draft=True
      '在具体事事物物中体认良知'    in_draft=True
      '去除私欲对良知的遮蔽'        in_draft=True
      '在道德实践中展现良知'        in_draft=True
      '通过反省加深对良知的理解'    in_draft=True
[B5] figure H-WYM-001 birth_year/death_year = 1472 1529 | in_draft: True
[B5] verification = {"status": "verified", "method": "link-resolved", "evidence": "https://zh.wikisource.org/wiki/%E5%82%B3%E7%BF%92%E9%8C%84", "checked_at": "2026-09-21", "checker": "phase38-y2"}
      status='verified'      in_draft=True
      method='link-resolved' in_draft=True
      checked_at='2026-09-21' in_draft=True
      evidence='https://zh.wikisource.org/wiki/%E5%82%B3%E7%BF%92%E9%8C%84' in_draft=True
```

对照草稿原文（`docs/community/zhihu_launch_post.md` 第 46–82 行）：定义 blockquote、5 步编号清单、现代应用、现代问题域、原话、出处、核验三态（`verified` / `link-resolved` / 2026-09-21）**全部与源 JSON 逐字一致**，无二次创作；生卒年 1472—1529 与 `data/figures/H-WYM-001.json` 的 `birth_year`/`death_year` 一致；`mode_code` M381 / `figure_code` H-WYM-001 / `figure_name` 王阳明 亦一致。

补充（线上交叉证据）：线上预渲染深链 `/minds/H-WYM-001/` 页面正文可检索到「致良知法」「传习录」「知善知恶是良知，为善去恶是格物」「认识到人人皆有良知」与「已核验」徽章，草稿给的在线页与数据同源。

### B-6 文中全部外链亲自 curl 【PASS】

脚本 `/tmp/qa10_links2.py`：正则抽出草稿里所有 http(s) URL，逐条 `curl -sSL -o /dev/null --max-time 30 -w "%{http_code}"`（失败重试至多 4 次；先看状态码再判正文）。

```text
distinct URLs: 16
200  https://ovmobilegroup.github.io/protreptic/
200  https://ovmobilegroup.github.io/protreptic/minds/H-WYM-001/
200  https://zh.wikisource.org/wiki/%E5%82%B3%E7%BF%92%E9%8C%84
200  https://ovmobilegroup.github.io/protreptic/credibility/
200  https://github.com/ovmobilegroup/protreptic/blob/main/CONTRIBUTING.md
200  https://github.com/ovmobilegroup/protreptic
200  https://ovmobilegroup.github.io/protreptic/data/meta.json
200  https://ovmobilegroup.github.io/protreptic/modes/
200  https://ovmobilegroup.github.io/protreptic/figures/
200  https://ovmobilegroup.github.io/protreptic/concepts/
200  https://ovmobilegroup.github.io/protreptic/graph/
200  https://ovmobilegroup.github.io/protreptic/compare/
200  https://ovmobilegroup.github.io/protreptic/daily/
200  https://ovmobilegroup.github.io/protreptic/templates/
200  https://ovmobilegroup.github.io/protreptic/api/
200  https://ovmobilegroup.github.io/protreptic/docs/
```

**16/16 全部 200**（`-L` 跟随重定向；本机 curl 偶发 TLS 抖动，个别 URL 重试 2~3 次即过 —— 本轮 `/figures/`、`/compare/` 各重试过，两次独立运行结论一致）。草稿附录一列的 16 行与实测**逐条对齐**，无多列、无漏列、无 404。

### B-7 夸大 / 未证实断言 【PASS（无「全部已考证」式夸大）+ 2 条非阻断观察】

按卡片点名的失效模式逐条查：

- 未暗示「全部已考证」：草稿第 84–102 行专门开「可信度：我不打算假装每条都可信」，并**如实公布四态**「已核验 888 / 待核验 1547 / 存疑 23 / 一手材料 340」，还写明「大约三分之一已经核验过，其余三分之二如实标着『还没核到』」「它不是一个『全部考证完毕』的权威典籍」。**与数据一致**（见 B-8），且方向是**自我克制**而非夸大。
- 数字类断言全部可复现（B-8），且草稿把取数命令写进附录一供读者重跑。
- 出处覆盖率写的是「2758 条（98.6%）」而**不是**「全部」，并注明「解析不到链接的，保留原文并标成『一手材料 / 待核验』，不假装全部可点」。

遗留 2 条**非阻断**观察，均在草稿正文里，原文与数据并列如下（不是谎报——数字全真，属继承自仓库既有口径的一般化措辞）：

1. 第 39 行与原句「**2798 条思维模式**，每一条都给出四样东西：**定义**（中英双语）→ **操作步骤** → **出处** → **现代应用场景**」，以及第 41 行「不是『凭空生成』：**每条都标注来源篇章**」。
   实测发布口径 2798 条的字段填充数（脚本 `/tmp/qa10_odanobun.py`，`drop_quarantined_modes` + 非空判定）：

   ```text
   published 2798: src 2758 | app(any 'applic' key) 2568 | process 2748 | def_en 2758 | quote 2758
   ```

   即「定义（中英双语）」2758/2798、「操作步骤」2748/2798、「出处」2758/2798、「现代应用」2568/2798，**不是 100%**。草稿第 106 行自己也写了「2798 条里，2758 条（98.6%）填了具体的来源篇章」，两句在同一篇里轻微打架。
   溯源：该措辞**不是本卡新增**，与 `README.md:15`「每一条都给出四样东西」、`README.md:23`「每条都标注来源篇章」，以及站点自身生成的 `web/src/generated/siteCounts.ts` 描述的「2798 条思维模式 × 278 位历史人物：每条都有出处、操作步骤与现代应用」同源。
   建议（不强制）：发布前把第 39/41 行的「每一条都」改成「绝大多数（98%+）都」，或直接沿用后文 98.6% 的表述，消除同篇自相矛盾的把柄。

2. 第 38 行「278 位历史人物，从先秦诸子到近现代科学家、企业家，**跨 30 个领域**」。
   该口径**无法从 `data/` 数据文件复现**：发布口径模式记录的 `domain_zh` 清洗后仍是非受控自由文本（首段去重 2237 个不同值），`category` 仅 18 个，前端 `histDomainLabels` 只有 10 个、`DOMAINS` 只有 7 个，均非 30。
   溯源：同样**不是本卡新增**，与 `README.md:30` 同句一致，可追到 `docs/05-expansion/cross_domain_expansion_v7.md:346`「思维模式体系已从最初的 12 种核心模式扩展至 78 种以上，覆盖 30 个领域」与 `docs/04-training/thinking_mode_certification.md:944`（「42-78 | 跨领域扩展思维模式 | 30个领域」）—— 那是**思维模式体系**的领域数，挂到「278 位人物的领域跨度」上属于借用口径。
   建议（不强制）：若想零把柄，可改为「覆盖哲学、军事、治理、科技、文艺等 30 类领域（口径见库内跨领域研究）」，或干脆删掉「跨 30 个领域」五字。

### B-8 数字口径 2798 / 278 【PASS】

本地（读部署产物 `web/dist/data/meta.json`，不联网）：

```text
$ python3 tools/site_counts.py --show
[counts] 口径来源: /opt/data/workspace/Protreptic/web/dist/data/meta.json 的 counts.mode_summaries_published / counts.mode_by_figure_shards
[counts] description          : 2798 条思维模式 × 278 位历史人物：每条都有出处、操作步骤与现代应用。以人为鉴，明得失。
[counts] og:description       : 2798 条思维模式 × 278 位历史人物 · 中英双语
[counts] manifest description : 2798 条思维模式 × 278 位历史人物：每条都有出处、操作步骤与现代应用，中英双语，可离线查阅。
[counts] 可信度四态             : 发布口径 2798（已核验 888 / 待核验 1547 / 存疑 23 / 一手材料 340），源库口径合计 2858

mode_summaries_published = 2798
mode_by_figure_shards = 278
verification = {"published": {"verified": 888, "pending": 1547, "suspect": 23, "unverifiable": 340}, "published_total": 2798, "all": {"verified": 888, "pending": 1579, "suspect": 40, "unverifiable": 351}, "all_total": 2858, "quarantined_total": 60}
```

线上 `data/meta.json`（curl 200 后回读）：

```text
live generated_at = 2026-09-21T07:55:40+00:00
mode_summaries_published = 2798
mode_by_figure_shards = 278
verification = {"published": {"verified": 888, "pending": 1547, "suspect": 23, "unverifiable": 340}, "published_total": 2798, "all": {...}, "all_total": 2858, "quarantined_total": 60}
citation_links = {"modes_with_citations": 2154, "modes_with_link": 911, ...}
```

即：草稿门面数字 **2798 / 278**、四态 **888 / 1547 / 23 / 340**（合计 2798）、`modes_with_link` **911**，本地与线上一一致。

出处覆盖两条也逐字复现：

```text
$ python3 tools/source_link_index.py --coverage
index keys: 382  (/opt/data/workspace/Protreptic/data/source_links.json)
citations: 4016  linked=1147  registered-unlinkable=950  unresolved=1919
coverage = 1147/4016 = 28.6%
distinct cited names: 2174 | >=3: 374
names >=3 linked: 178/374 = 47.6%  (registered-unverifiable 196)
base names >=3: 361 | linked: 150 = 41.6%
modes with citations: 2165 | with >=1 linked citation: 911 = 42.1%
...

$ python3 /tmp/qa10_src.py（草稿附录一的 source_chapter 片段原样重跑）
2798 2758 98.6
```

草稿附录一引用的那句「`modes with citations: 2165 | with >=1 linked citation: 911 = 42.1%`」与 `tools/source_link_index.py --coverage` 的**实际输出逐字一致**；`2798 2758 98.6` 也一致。（附注：`data/meta.json` 的 `citation_links.modes_with_citations` 是 2154，与索引工具的 2165 差 11 —— 两者是不同生成器口径，草稿引的是它自己列出的那个工具，不存在错引。）

---

## 双仓同步与一致性（自查）

```text
$ python3 tools/check_repo_parity.py
[stats] 两仓都有 1440 条（其中逐字节一致 1440）｜仅单侧 0 条（仅工作仓 0 · 仅发布仓 0）
[OK] 零差异：1440 个构建图文件两仓逐字节一致（sha256）
```

- 工作仓 `git status -sb` = `## master`（干净）。
- 发布仓 `git status -sb` = `## main...origin/main`（**无 `[ahead N]`**）。发布仓工作树残留 `web/dist` 的 4 删 1 改（历史 tracked 构建产物，parity 已列为排除项、不参与判定），非本卡产生、本卡未触碰。
- 本报告 `docs/qa/phase45_acceptance.md` 已同步两仓并推送（构建图内文件，parity 要求两仓逐字节一致）。

## 本卡未做的事（如实声明）

- 未发帖、未注册账号、未代投递（按下卡约定，草稿仍是草稿）。
- 未改任何被测产物：临时清空 `web/goatcounter.json` 的 `code` 只为复现 inert 态，构建后**已逐字节还原**为 `protreptic`（A-1 输出末行可证）。
- 未触碰发布仓工作树里那份历史 tracked `web/dist`。

## 观察（非阻断，供船长裁量）

1. **【统计·上报标题滞后】** 站内跳转上报的 `title` 是路由级静态标题，不是数据加载后的具体标题。实测：跳 `/protreptic/minds/H-MIY-001` 时上报 `{"path": "/protreptic/minds/H-MIY-001", "title": "人物模式档案 | Protreptic 思想典藏"}`，而跳转完成后 `document.title` 已是 `宫崎骏 - 思维模式档案 10 条 | Protreptic 思想典藏`。
   影响面：**只影响统计报表里的 title 字段可读性**，`path` 正确、计数不重不漏、页面零报错，SEO 标题最终正确。与 `web/src/composables/useAnalytics.ts` 头注里「上报时 `document.title` 已经是本路由的标题」的断言不完全相符（该注释描述的是 useSeo 的**路由 meta** 标题，数据驱动的具体标题是异步后到的）。要不要顺手修，由船长定。
2. B-7 的「每一条都给出四样东西 / 每条都标注来源篇章」（98%+ 而非 100%）。
3. B-7 的「跨 30 个领域」（口径来自思维模式体系文档，数据文件复现不出 30）。

以上 3 条都不改变**可发布**判定：三处都不是编造数字或空渲染，且第 2、3 条的措辞在工作仓 README 与站点自带描述里**已经在线存在**（本卡之前就在线）。
