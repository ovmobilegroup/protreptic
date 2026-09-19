# Phase33 独立复验（QA3）· L1 / L2 / L3 逐项实测

- 卡片：`t_2c300130`（[Phase33-QA3] 独立复验 L1/L2/L3）· 审查人：espinosa
- 日期：2026-09-19（CST）
- 被审对象：Phase33-L1（统一「思维模式数」口径 + 重新生成分享图，`t_493e6506` / elcano）与
  Phase33-L2L3（双仓卫生，`t_e07221d0`）
- 工作区仓：`/opt/data/workspace/Protreptic`（HEAD `724cdac8`）
- 发布仓：`/opt/data/release/Protreptic-publish`（HEAD `2c2604c`，`origin/main` 同点）
- 线上：https://ovmobilegroup.github.io/protreptic
- **取证方式：全部自建方法与自写脚本，不照抄 L1/L23 自述。**
  全站扫描用**部署产物自身**（`web/dist/**` 逐文件正则统计短语）而不是源码枚举；
  分享图自己从线上下载后用视觉模型逐字读；docs 站用**线上 mkdocs 搜索索引**
  （`/docs/search/search_index.json`，20.5 MB / 9794 页）逐页检索，不依赖本地源码；
  双仓一致性按「生产面路径」自写遍历 + 逐文件 sha256，并先把 Git 忽略项剔除后再比。
- **终审结论：不可发布（FAIL）。** L2 / L3 / 全局三块 PASS（发布仓 ahead=0，四个 workflow 全绿且真跑 job）；
  **L1 未达验收线**——「只有一个口径」在全站扫描下被证伪：线上仍有两类表面写着 `2858` /
  `2868` / `284 位`（PWA manifest ×2、docs 站工具页）。详见第 1 节与第 5 节。

## 0. 逐项结论表

| 项 | 结论 | 一句话 |
| --- | --- | --- |
| L1 · 指定表面（HTML meta / 页脚 / hero / `/api` / og 图内文字） | PASS | 全部 `2848 条思维模式 × 283 位历史人物`，线上回读一致，og 图视觉实读同值 |
| L1 · 全站「只有一个口径」 | **FAIL** | 部署产物里 `2858 条思维模式` 仍出现 **2 次**（`manifest.webmanifest` / `manifest-light.webmanifest`），线上 HTTP 200 可直取 |
| L1 · docs 站扫描（自加，超出指定表面） | **FAIL（附带）** | 线上 `/docs/02-tools/figure_library/` 仍写「**284 位历史人物 × 每人 10 条 = 2868 条**」与「2858 条」 |
| L1 · 空渲染守卫 | PASS | 线上 `/api/`、`/modes/`、首页真实浏览器读 DOM 均非空（`/modes/` 120 张卡片） |
| L2 · 双仓 `docs/architecture/web_p0_routes.json` sha256 | PASS | 两仓 + 线上直取三处同为 `088a99a1…e6d` |
| L2 · 该文件不影响线上 | PASS | sitemap 1354 条 / 0 条含空格 / 深链抽检全 200 |
| L3 · 两仓 `git status --porcelain` | PASS | 两仓均为空；发布仓 `ahead=0 behind=0` |
| L3 · 生产面逐文件 sha256 | PASS | 生产面 1565 个文件，差异 0；唯一「仅工作区」项 `tools/gc/gc` 在发布仓被 gitignore 且 CI 不引用 |
| L3 · 线上独有副本被误删/误回退 | PASS | 发布仓独有产物仍在 HEAD 且线上 200（`data/index.unified.json`、`docs/`…） |
| 全局 · ahead=0 / 四个 workflow | PASS | Pages 2 job、CI 1 job、CI/CD 6 job、Quality Gate 3 job，全 success，无 0-job 幻影 |

---

## 1. L1 · 口径统一（结论：FAIL）

### 1.1 全站扫描：用**部署产物**自身统计短语（自建方法）

不枚举源码，直接对 CI 产出的静态站点目录做短语频率统计——它才是线上那份：

```console
$ D=/opt/data/workspace/Protreptic/web/dist
$ grep -rEoh '[0-9]{2,4}[ ]*条思维模式|[0-9]{2,4}[ ]*位历史人物|[0-9]{2,4}[ ]*个现代场景' $D \
    | sort | uniq -c | sort -rn
     72 12 条思维模式      # 单人物模式数（每人 N 条），不是站点口径
     39 10 条思维模式      # 同上
     19 283 位历史人物
     10 2848 条思维模式
      6 1055 个现代场景
      2 2858 条思维模式   # ← 第二个口径，仍在部署产物里
```

带几位数字的只剩两类：`2848`（10 次，正确）与 `2858`（2 次，错误）。
定位这 2 次：

```console
$ grep -rlE '2858|2868' $D | grep -v '/figures/' | grep -v templates/index.html
$D/data/meta.json               # 三档内部计数键（见 1.5，属数据契约，非展示文案）
$D/manifest-light.webmanifest   # ← 展示文案
$D/manifest.webmanifest         # ← 展示文案
$D/og/manifest.json             # sha256/字节表，非文案
$D/index.html $D/404.html        # HTML 注释「不是 modes_raw=2868…」，页面不显示
$D/daily/index.html $D/figures/index.html   # 同上，预渲染头里的注释
```

即：**部署产物里真正的展示文案只有一个越界者——两份 PWA manifest。**

### 1.2 线上回读（curl 等价，HTTP 直取）

```console
$ python3 - <<'PY'   # 见第 6 节完整脚本，此处摘录输出
/ http 200 bytes 4380
   [meta] <meta property="og:image:alt" content="Protreptic 思想典藏 — 2848 条思维模式 × 283 位历史人物" />
   [meta] <meta name="twitter:image:alt" content="Protreptic 思想典藏 — 2848 条思维模式 × 283 位历史人物" />
   [meta] <meta name="description" content="2848 条思维模式 × 283 位历史人物：每条都有出处、操作步骤与现代应用。以人为鉴，明得失。" />
   [meta] <meta property="og:description" content="2848 条思维模式 × 283 位历史人物 · 中英双语" />
/modes/ http 200 bytes 19972
   …共 2848 条思维模式，每条含定义、操作步骤、出处与原话，中英双语。
   [meta] <meta property="og:image:alt" content="思维模式库 — 2848 条可执行方法" />
/figures/ http 200 bytes 16975
   …283 位历史人物 + 1055 个现代场景, 统一检索入口.
   …283 位历史人物的思维方法与 1055 个现代处境场景，汇成同一份…
/404.html http 200 bytes 4357
   [meta] <meta name="description" content="2848 条思维模式 × 283 位历史人物：…" />
/manifest.webmanifest http 200 bytes 1583
    "description": "2858 条思维模式 × 283 位历史人物：每条都有出处、操作步骤与现代应用，中英双语，可离线查阅。",   # ← FAIL
/manifest-light.webmanifest http 200 bytes 1583
    "description": "2858 条思维模式 × 283 位历史人物：…",                                                        # ← FAIL
```

指定表面（首页 description / `og:description` / `og:image:alt` / `twitter:image:alt`、页脚、
`/modes` head 与正文、`/figures` head、`/404.html`）**全部为 2848 / 283**，meta 与 alt 一致。

### 1.3 og/site.png：自己下载 + 视觉逐字读

```console
$ python3 /tmp/qa33/get_og.py
live bytes 32676 sha256 96ede786505301369af208ec1a9c932118ca63ea6be5852b3e8a61a3af9b9fe0
saved /tmp/qa33/live_og_site.png

$ sha256sum /opt/data/workspace/Protreptic/web/dist/og/site.png
96ede786505301369af208ec1a9c932118ca63ea6be5852b3e8a61a3af9b9fe0  web/dist/og/site.png   # 与线上逐字节相同
```

视觉模型对**线上 PNG** 的逐字抄录（原样，未改写数字）：

```
PROTREPTIC · 思想典藏
思想典藏 · Archive of Minds
Protreptic 思想典藏
历史人物思维模式库 · 中英双语
2848 条思维模式
283 位历史人物
1055 个现代场景
每条都有出处、操作步骤与现代应用。以人为鉴，明得失。
ovmobilegroup.github.io/protreptic
思
```

图内文字 = 站点口径，且与 `og:image:alt`（"2848 条思维模式 × 283 位历史人物"）同源一致。
上一轮 QA2 抓到的 `2868` 已消失（本项是 L1 的真实修复点，确认生效）。

### 1.4 越界者 A：PWA manifest（线上可直取）

```console
$ sha256(manifest.webmanifest)       0abb7749701e4b2e006f013f7c21ca7bbc0ac67447d1f09ab75bd1d68e2c79f3
$ sha256(manifest-light.webmanifest) 72add0df5490b2b015409df15adac4657ef06bfe09213d318b24678a34ee3400
$ grep -n '2858' /opt/data/workspace/Protreptic/web/public/manifest*.webmanifest
web/public/manifest.webmanifest:4:  "description": "2858 条思维模式 × 283 位历史人物：…"
web/public/manifest-light.webmanifest:4:  "description": "2858 条思维模式 × 283 位历史人物：…"
# 发布仓同文件同内容（两份都是 2858）
```

影响面：这是 `link rel=manifest` 指向的真实资源（线上首页 `document.querySelector('link[rel=manifest]').href`
实测 = `https://ovmobilegroup.github.io/protreptic/manifest.webmanifest`），其 `description`
是 PWA 安装/应用信息界面展示的文案。它同时与站内首页/页脚/`og:image:alt` 的 2848 打架。
**根因**：L1 的扫描范围是 `web/src` + `web/index.html`，把静态资源目录 `web/public/**`
（Vite 原样拷贝进 `dist/`）漏在网外；`meta.json` 的 2858 键被有意保留，但 manifest 的文案
显然不是数据契约，而是展示文案。

### 1.5 越界者 B：docs 站工具页（自加表面）

用**线上** mkdocs 搜索索引逐页检索（20,562,022 bytes / 9794 页）：

```console
$ curl -s https://ovmobilegroup.github.io/protreptic/docs/search/search_index.json | ...
docs pages: 9794
$ python3 /tmp/qa33/docs_scan.py     # 排除 phase*/report/acceptance/qa/review 等历史报告页后
   02-tools/figure_library/         | 284 位历史人物 | 把 Protreptic 的核心资产——284 位历史人物 × 每人 10 条专属思维模式 = 2868 条——接入可查询的产品层。
   02-tools/figure_library/#_1      | 2868 条        | …而八轮挖掘沉淀的 2868 条人物专属模式一直没被产品层读到。
   02-tools/figure_library/#_2      | 2868 条        | 数据文件：data/modes_data.json（2868 条，21MB）
   02-tools/figure_library/#_5      | 2858 条        | …✅ 数据已入 thinking_modes 表（2858 条）
```

线上该页 HTTP 200（165,575 bytes），是 `02-tools` 导航下的**产品工具说明页**，不是历史归档。
它把产品规模写成 `284 位 / 2868 条`，与站上 `283 位 / 2848 条` 三处不同。

另外（**不判 FAIL**，如实记录）：`docs/architecture/web_p0_architecture`、`web_p0_evidence`、
`web_pages_migration_assessment`、`figures/H-P23F-001` 等页仍含 2858/2868/1122 等数字。
这些是**当时的实测记录**（决策/证据/人物档案的历时文本），L1 报告已把这类刻意保留写明，
本卡认可该处置——但 L1 报告没有区分出上面那条 `02-tools/figure_library` 是产品页而非历史记录。

### 1.6 空渲染守卫（自加）

真实浏览器读线上 DOM：

```console
/api/  → 正文非空：数据与 API / 静态数据接口 / “/data/modes/index-{0..7}.json  思维模式摘要（8 分片，共 2848 条）”
                  页脚：Protreptic · 2848 条思维模式 × 283 位历史人物 · 中英双语
首页    → 283 位历史人物的思维方法，与 1055 个现代处境场景 … | 人物 283 | 场景 1055 | 1302 条含模式
/modes/ → articles=120，正文“2848 条思维模式实例，源自 283 位历史人物”，分类计数 2848
```

无空渲染。

### 1.7 L1 判定

**FAIL。** 验收线要求「列出各表面数值，确认**只有一个**口径」。实测：指定表面 5 项全部 PASS 且
og 图已修好；但全站扫描（部署产物 + 线上 docs 站）仍存在 `2858`（manifest ×2）与
`2868 / 284 位`（docs 工具页）两个独立口径，共 3 个线上 URL。属于「同一份数据的多个门面数字」，
不是 L1 报告结论里「只剩历史记录页」的那个收口状态。

---

## 2. L2 · 路由登记产物双仓一致性（结论：PASS）

```console
$ sha256 工作区 docs/architecture/web_p0_routes.json
088a99a10476986524d84f7886bfb1dd981f93d23dc1fed6d37e34c532e80e6d   (684094 bytes)
$ sha256 发布仓 docs/architecture/web_p0_routes.json
088a99a10476986524d84f7886bfb1dd981f93d23dc1fed6d37e34c532e80e6d   (684094 bytes)
$ 线上直取 https://ovmobilegroup.github.io/protreptic/docs/architecture/web_p0_routes.json
live routes http 200 bytes 684094 sha256 088a99a10476986524d84f7886bfb1dd981f93d23dc1fed6d37e34c532e80e6d
```

三处同值（QA2 记录的 `803eb6ae…`/`915d3378…` 两个旧副本已被 L23 收口为当前态）。

「不影响线上」独立验证——sitemap 与路由仍然正确：

```console
$ curl -s https://ovmobilegroup.github.io/protreptic/sitemap.xml
sitemap http 200 locs 1354
prefix counts: {'api':1,'compare':1,'concepts':1,'daily':1,'figures':1056,'graph':1,'minds':283,'modes':1,'templates':8}
raw-space locs (should be 0): 0
$ 深链抽检
   200 .../minds/AMP/   200 .../minds/AMU/   200 .../minds/ARR/
   200 .../modes/       200 .../figures/     200 .../figures/A-1-X-P/
```

---

## 3. L3 · 双仓卫生 / 无「线上唯一副本被误删回退」（结论：PASS）

### 3.1 两个工作树

```console
$ git -C /opt/data/workspace/Protreptic status --porcelain
（空）
$ git -C /opt/data/release/Protreptic-publish status --porcelain
（空）
$ git -C /opt/data/release/Protreptic-publish status -sb
## main...origin/main
$ git -C /opt/data/release/Protreptic-publish rev-list --left-right --count origin/main...HEAD
0 0     # 左＝origin/main 领先数，右＝HEAD 领先数（即 ahead=0 behind=0）
```

### 3.2 生产面逐文件 sha256（自写遍历，先剔除 git 忽略项）

比较路径：`web/src`、`web/index.html`、`web/tailwind.config.js`、`web/postcss.config.js`、
`web/package.json`、`web/vite.config.ts`、`web/public`、`tools`、`data/modes_data.json`、
`data/figure_names.json`、`data/figures`、`.github/workflows`、`mkdocs.pages.yml`、`lighthouserc.json`。

```console
counts: 1565 1564
ONLY WORKSPACE(1):
   - tools/gc/gc
ONLY PUBLISH(0):
DIFFERS(0):
```

即**生产面 1565 个文件在两仓逐字节相同，零差异**。

一处差异的处置说明（非阻断，已实测）：`tools/gc/gc` 是 GoatCounter 自托管二进制，工作区把它
纳入版本控制，发布仓被 `.gitignore` 排除；两个工作树上文件都存在（`os.path.exists` 均 True），
且 `.github/workflows/*` 与 `tools/*.py` 中**没有任何引用**（`grep -rn 'tools/gc'` 零命中）。
它不参与 Pages 产物，不构成「唯一副本被误删」。

> 说明：本卡第一版比较误把 `web/public/data/**`（导出产物）算进差异——实为**两仓均被
> `.gitignore:39 web/public/data/` 排除**的本地构建残留，不属仓库状态。修正为「先 `git check-ignore`
> 剔除再比」后差异归零。此处如实记录，避免下游误读。

### 3.3 发布仓独有产物是否仍在（防「误删/误回退」）

```console
$ git -C /opt/data/release/Protreptic-publish ls-tree -r HEAD | 独有项仍在，例如
data/intl_figures/**（1057）、docs/index.md、docs/archive/research/**、docs/_config.yml、web/dist/assets/**
$ 线上抽检
   200 data/figures.index.json (212513 bytes)
   200 data/index.unified.json (448703 bytes)
   200 data/meta.json (3114 bytes)
   200 docs/ （161789 bytes）
```

---

## 4. 全局 · ahead 与四个 workflow（结论：PASS）

```console
$ git -C /opt/data/release/Protreptic-publish rev-parse HEAD      2c2604c827b552b8033eacf3d342f94c9acfe4b7
$ git -C /opt/data/release/Protreptic-publish rev-parse origin/main 2c2604c827b552b8033eacf3d342f94c9acfe4b7
$ git -C /opt/data/release/Protreptic-publish status -sb            ## main...origin/main     # 无 [ahead N]

$ gh run list --repo ovmobilegroup/protreptic --limit 10
Quality Gate           35414732657 workflow_run success 2026-09-19T02:07:33Z
Protreptic CI/CD       35414514520 push         success 2026-09-19T02:03:08Z
Deploy to GitHub Pages 35414514493 push         success 2026-09-19T02:03:08Z
CI                     35414514486 push         success 2026-09-19T02:03:08Z

$ 逐个 run 取 head_sha 与 jobs（防 0-job 幻影）
35414514493 Deploy to GitHub Pages  head_sha=2c2604c  jobs=2  构建 SPA + 文档站 success / 部署 success
35414514486 CI                      head_sha=2c2604c  jobs=1  markdown-lint success
35414514520 Protreptic CI/CD        head_sha=2c2604c  jobs=6  Test success / API Docker success / Web Docker success / Notify success
                                                              / Deploy to Staging skipped / Deploy to Production skipped
35414732657 Quality Gate            head_sha=2c2604c  jobs=3  数据校验 success / Lighthouse 预算门 success / 线上死链检测 success
```

四个 run 的 `head_sha` 都等于发布仓 HEAD（`2c2604c`），Quality Gate 是**真跑 3 个 job** 的
`workflow_run` success，无 `name == path` 的 0-job 幻影。CI/CD 的两个 Deploy job 是
`if: github.ref == ...` 条件下的 skipped（预期行为），不是失败。

---

## 5. 结论与可执行修复清单

**不可发布（FAIL）。**

- 达标：L2（登记产物三处同 sha256 且不影响线上）、L3（两仓干净、ahead=0、生产面 1565 文件零差异、
  无线上独有副本被误删回退）、全局（四个 workflow 真跑且全 success）。
- 不达标：**L1 的「只有一个口径」被证伪**，两处线上展示文案仍是旧口径：

| # | 线上 URL | 现文案 | 应为 | 根因 | 修复点 |
| --- | --- | --- | --- | --- | --- |
| A1 | `/manifest.webmanifest` | `2858 条思维模式 × 283 位历史人物` | `2848 …` | L1 扫描漏了 `web/public/**` | `web/public/manifest.webmanifest` 第 4 行 `description` |
| A2 | `/manifest-light.webmanifest` | 同上 | 同上 | 同上 | `web/public/manifest-light.webmanifest` 第 4 行 |
| A3 | `/docs/02-tools/figure_library/` | `284 位历史人物 × 每人 10 条专属思维模式 = 2868 条`、另 `2868 条`×2、`2858 条`×1 | 与站上口径一致（2848 / 283），或明确改写为「源数据 2868 条，站上发布 2848 条」 | L1 只扫了 `web/src` + `docs/index.md`，未扫 docs 其余产品页 | `docs/02-tools/figure_library.md` 第 3/8/13/66 行 |

修复成本极低（两份 manifest 各 1 行 + 一份 docs 4 处文案），且**必须两仓同步**
（manifest 在 `web/public/` → 影响线上；docs md 在发布仓 `docs/` → 影响 docs 站）。

建议顺序：改源码 → `cd web && VITE_DATA_MODE=static npm run build` 通过 → 两仓同步并各自提交 →
发布仓 `git push origin main` → 等 Pages 后**肉眼/curl 回读**这三个 URL。

> 刻意保留、本卡不视为违规的历史文本：`docs/architecture/*`、`docs/phase2*_final_report.md`、
> `docs/qa/phase3*_acceptance.md`、`data/figures/H-P23F-001.json` 等**当时实测记录**里的
> 2858/2868/501/1122；以及 `web/public/data/meta.json` 的 `modes_raw=2868`/`mode_summaries=2858`
> 两个**内部计数键**（数据契约，页面不展示）。理由是它们记录的是历史事实而非当前产品门面。

---

## 6. 复现命令清单

```bash
# L1-a 部署产物短语统计（无需网络）
D=/opt/data/workspace/Protreptic/web/dist
grep -rEoh '[0-9]{2,4}[ ]*条思维模式|[0-9]{2,4}[ ]*位历史人物|[0-9]{2,4}[ ]*个现代场景' $D | sort | uniq -c | sort -rn
grep -rlE '2858|2868' $D | head -60

# L1-b 线上 meta/alt/manifest 回读（脚本见附录 A.1）
python3 /tmp/qa33/live_scan.py

# L1-c 分享图自下载 + 视觉读图
python3 /tmp/qa33/get_og.py            # 落地 /tmp/qa33/live_og_site.png 并打印 sha256
# 再对 /tmp/qa33/live_og_site.png 调 vision_analyze，逐字读数字

# L1-d docs 站全量扫描（走线上搜索索引，不依赖本地源码）
python3 /tmp/qa33/docs_scan.py

# L2 sha256 三处
sha256sum /opt/data/workspace/Protreptic/docs/architecture/web_p0_routes.json \
          /opt/data/release/Protreptic-publish/docs/architecture/web_p0_routes.json
curl -s https://ovmobilegroup.github.io/protreptic/docs/architecture/web_p0_routes.json | sha256sum
curl -s https://ovmobilegroup.github.io/protreptic/sitemap.xml | grep -c '<loc>'

# L3 双仓
git -C /opt/data/workspace/Protreptic status --porcelain
git -C /opt/data/release/Protreptic-publish status --porcelain
git -C /opt/data/release/Protreptic-publish rev-list --left-right --count origin/main...HEAD
python3 /tmp/qa33/two_repo_compare.py  # 生产面逐文件 sha256（先剔除 git check-ignore）

# 全局
HOME=/opt/data/home /opt/data/home/.local/bin/gh run list --repo ovmobilegroup/protreptic --limit 10
HOME=/opt/data/home /opt/data/home/.local/bin/gh api repos/ovmobilegroup/protreptic/actions/runs/<id>/jobs --jq '.total_count'
```

---

## 附录 A · 原始输出

### A.1 线上表面扫描（`/tmp/qa33/live_scan.py` 输出，节选）

```console
/ http 200 bytes 4380
   [meta] <meta property="og:image:alt" content="Protreptic 思想典藏 — 2848 条思维模式 × 283 位历史人物" />
   [meta] <meta name="twitter:image:alt" content="Protreptic 思想典藏 — 2848 条思维模式 × 283 位历史人物" />
   [meta] <meta name="description" content="2848 条思维模式 × 283 位历史人物：每条都有出处、操作步骤与现代应用。以人为鉴，明得失。" />
   [meta] <meta property="og:description" content="2848 条思维模式 × 283 位历史人物 · 中英双语" />
/modes/ http 200 bytes 19972
   [meta] <meta name="description" content="2848 条历史人物思维模式实例, 含定义, 操作步骤, 出处与原话." />
/figures/ http 200 bytes 16975
   [meta] <meta name="description" content="283 位历史人物 + 1055 个现代场景, 统一检索入口." />
/daily/ http 200 bytes 5191     # 无数字口径（英文文案，路由级）
/api/ http 200 bytes 4731       # head 无数字；渲染后正文/footer 为 2848（见 1.6）
/docs/ http 200 bytes 161789
   <strong>2848 条思维模式 · 283 位历史人物 · 中英双语</strong>
   [meta] <meta name="description" content="Protreptic · 思想典藏 —— 2848 条历史人物思维模式 × 283 位人物 · 中英双语">
/manifest.webmanifest http 200 bytes 1583      → "2858 条思维模式 × 283 位历史人物：…"   FAIL
/manifest-light.webmanifest http 200 bytes 1583 → 同上                                  FAIL
/404.html http 200 bytes 4357   → 2848 / 283
```

### A.2 线上数据契约（非展示文案，记录备查）

```console
live meta.json counts: {"figures":1057,"figure_shards":1057,"mode_summaries":2858,
 "mode_summaries_published":2848,"modes_quarantined":10,"mode_index_shards":8,
 "mode_by_figure_shards":283,"modes_raw":2868,"modes_deduped":2858,
 "modes_duplicates_dropped":0,"modes_empty_mode_code_dropped":10,"modes_without_figure_code":0}
live search/meta.json doc_count: 2848
```

### A.3 视觉读图原始答复（对线上 `/og/site.png`）

```
PROTREPTIC · 思想典藏 / 思想典藏 · Archive of Minds / Protreptic 思想典藏 /
历史人物思维模式库 · 中英双语 / 2848 条思维模式 / 283 位历史人物 / 1055 个现代场景 /
每条都有出处、操作步骤与现代应用。以人为鉴，明得失。 / ovmobilegroup.github.io/protreptic / 思
```

---

## 附录 B · 本报告自身的 CI 实况（提交 `6f6d972`）

本报告落盘 → 推送到发布仓 `main` 后，同一提交上四个 workflow 的实况（自取自 gh api）：

```console
$ git -C /opt/data/release/Protreptic-publish status -sb
## main...origin/main                     # 无 [ahead N] → ahead=0 behind=0
$ git -C /opt/data/release/Protreptic-publish rev-list --left-right --count origin/main...HEAD
0 0     # 左＝origin/main 领先数，右＝HEAD 领先数

$ gh run list --repo ovmobilegroup/protreptic --limit 6   # headSha = 6f6d972
Quality Gate           35415794772 success   3 jobs: 数据校验 / Lighthouse 预算门 / 线上死链检测
Protreptic CI/CD       35415578174 success   6 jobs: Test(Python+TS) / Build API Docker / Build Web Docker /
                                                    Notify 全 success；Deploy to Staging / Production skipped（条件未命中，预期）
CI                     35415578135 success   1 job : markdown-lint
Deploy to GitHub Pages 35415578125 success   2 jobs: 构建 SPA + 文档站 / 部署
```

本报告页面线上可读（渲染非空，标题与关键 sha256 均命中）：

```console
$ 线上回读 https://ovmobilegroup.github.io/protreptic/docs/qa/phase33_acceptance/
http 200 bytes 215588
title: Phase33 独立复验（QA3）· L1 / L2 / L3 逐项实测 - Protreptic · 思想典藏
contains "Phase33 独立复验"                                  -> True
contains "不可发布（FAIL）"                                  -> True
contains "96ede786505301369af208ec1a9c932118ca63ea…"        -> True
contains "088a99a10476986524d84f7886bfb1dd981f93d…"        -> True
```

提交前本地 Markdown 预检（与 CI 同工具同配置）：

```console
$ npx --yes markdownlint-cli2 'docs/qa/phase33_acceptance.md'
Summary: 0 issues in 0 files
```
