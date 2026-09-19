# Phase34-L1B 门面计数收口报告（PWA manifest ×2 + docs 产品页 + 单一取数源）

卡：`t_d67e0ba3`（elcano）。上游：`docs/qa/phase33_acceptance.md`（QA3 终审判 L1 FAIL）。
本卡目标：把「N 条思维模式 × M 位历史人物」这句话收敛到**唯一取数入口**，并把 QA3 实测的
两处漏网（两份 PWA manifest、docs 工具页）改到站点口径，然后在**部署产物**上全量自证归零。

## 1. 结论

- 站点口径统一为 **2848 条思维模式 × 283 位历史人物**
  （=`dist/data/meta.json` 的 `counts.mode_summaries_published` / `counts.mode_by_figure_shards`）。
- 唯一取数入口：`tools/site_counts.py`（新增）。HTML meta / og 文案 / 两份 manifest / docs 产品页
  全部经它，不再各自读 `meta.json`（QA3 判 FAIL 的根因就是「一个数字、多个表面各自读」）。
- 部署产物 `web/dist/**` 全量扫描（2731 个文件）**零违规**；docs 产品门面页 5 个**零违规**。
- 线上三处回读已改口径（第 5 节），四个 workflow 全 success（第 6 节）。

## 2. 改动清单（真实路径）

工作区 `/opt/data/workspace/Protreptic` 与发布仓 `/opt/data/release/Protreptic-publish` 同步：

| 文件 | 改动 |
| --- | --- |
| `tools/site_counts.py` | **新增**：唯一取数入口 + manifest 收口 + 产物/docs 扫描（CLI `--show/--sync/--scan`） |
| `tools/apply_site_counts.py` | 改为只调共享模块；新增 manifest（源+产物）收口、`dist/**` 全量硬门、docs 产品页硬门 |
| `web/index.html` | 说明注释不再带旧口径裸数字（它被预渲染复制进 1353 个路由页，是 2868/2858 在产物里的唯一来源） |
| `web/public/manifest.webmanifest` | `description` → 2848 × 283 |
| `web/public/manifest-light.webmanifest` | `description` → 2848 × 283 |
| `docs/02-tools/figure_library.md` | 计数改为站点口径 + 新增「计数口径（唯一来源）」一节（如实标注源库口径 284 位/2868 条） |
| `.github/workflows/pages.yml` | `paths` 补 `tools/site_counts.py`；Step B2.7 说明与职责更新 |
| `docs/architecture/web_p0_routes.json` | prerender 重生成（index.html 注释缩短，每页少 9.4 KB），两仓同值 |

## 3. 各表面同源：调用点清单

```
$ grep -rn "site_counts\." tools/apply_site_counts.py
84:    modes, figures = site_counts.load_counts(dist / "data")            # 取数（唯一来源）
85:    want_desc = site_counts.description_text(modes, figures)            # 首页 description
86:    want_ogd = site_counts.og_description_text(modes, figures)          # 首页 og:description
100:   ... site_counts.manifest_description_text(modes, figures)           # manifest description（dry-run 展示）
124:   for p, changed, old, new in site_counts.sync_manifests(dist, args.public, modes, figures)  # 源 + 产物两份 manifest
128:   checked, violations = site_counts.scan_display_surfaces(dist, modes, figures)              # dist/** 全量硬门
136:   n_docs, doc_violations = site_counts.scan_product_docs(args.docs, modes, figures)          # docs 产品门面页硬门

$ grep -n "site_counts\|apply_site_counts" .github/workflows/pages.yml
49:      - 'tools/apply_site_counts.py'          # paths 过滤
50:      - 'tools/site_counts.py'                # paths 过滤（只改共享模块也触发部署）
166:      # tools/site_counts.py（唯一来源 = dist/data/meta.json 的 counts），本步骤负责：…
175:        run: python3 tools/apply_site_counts.py
```

`site_counts.py` 的接口（唯一的「数字 → 文案」处）：

```
load_counts(data_dir) -> (modes, figures)
description_text / og_description_text / manifest_description_text
sync_manifests(dist, public)           # 两份 manifest：源 web/public + 产物 dist 一起收口
scan_display_surfaces(root)            # 产物全量门面数字
scan_product_docs(docs_dir)            # docs 产品门面页（docs/index.md + docs/02-tools/**）
```

## 4. 本地产物自证（部署产物，非源码枚举）

构建链按 CI 顺序在本地跑完：`export_static_site → build_daily_index → build_search_index →
build_graph_data → build_unified_index → npm run build（VITE_DATA_MODE=static）→ build_og_images →
prerender_routes --body-persons all → apply_og_meta → apply_site_counts → build_sw → build_sitemap`。

### 4.1 硬门实跑

```
$ /opt/data/venvs/protreptic/bin/python tools/apply_site_counts.py
[counts] manifest 已一致: …/web/public/manifest.webmanifest -> 2848 条思维模式 × 283 位历史人物：…
[counts] manifest 已一致: …/web/public/manifest-light.webmanifest -> 2848 条思维模式 × 283 位历史人物：…
[counts] manifest 已一致: …/web/dist/manifest.webmanifest -> 2848 条思维模式 × 283 位历史人物：…
[counts] manifest 已一致: …/web/dist/manifest-light.webmanifest -> 2848 条思维模式 × 283 位历史人物：…
[counts] 收口完成: 2848 条模式 × 283 位人物 (来源 …/web/dist/data/meta.json)
[counts] dist 扫描 2731 个文件零违规；docs 产品门面页 5 个零违规      # rc=0
```

### 4.2 QA3 判定式的改前/改后计数

改前快照 = 当前新产物 + 把两份 manifest 换回 HEAD 版本（QA3 实测的旧态）：

```
$ cp -r web/dist /tmp/dist_before_l1b
$ git show HEAD:web/public/manifest.webmanifest > /tmp/dist_before_l1b/manifest.webmanifest
$ git show HEAD:web/public/manifest-light.webmanifest > /tmp/dist_before_l1b/manifest-light.webmanifest
$ grep -rEoh '[0-9]{2,4} *条思维模式|[0-9]{2,4} *位历史人物|[0-9]{2,4} *个现代场景' /tmp/dist_before_l1b | sort | uniq -c | sort -rn
     72 12 条思维模式
     39 10 条思维模式
     19 283 位历史人物
     10 2848 条思维模式
      6 1055 个现代场景
      2 2858 条思维模式         ← 两份 manifest，即 QA3 的越界者 A
$ grep -rEoh '[0-9]{2,4} *条思维模式|[0-9]{2,4} *位历史人物|[0-9]{2,4} *个现代场景' web/dist | sort | uniq -c | sort -rn
     72 12 条思维模式
     39 10 条思维模式
     19 283 位历史人物
     12 2848 条思维模式
      6 1055 个现代场景         ← 「2858 条思维模式」归零
```

`12 条思维模式` / `10 条思维模式` 是正文里「每人 N 条」的说法（两位数字，非门面数字），
故 `site_counts` 的门面判定式取 3-5 位数字的「N 条思维模式 / N 位历史人物」+ 门面文件的旧口径裸数字。

### 4.3 硬门正控制（证明不是空转）

```
正控制-产物层 扫描文件数 2 违规: [('manifest.webmanifest', '条数', '2858 条思维模式'),
                                  ('manifest.webmanifest', '旧口径裸数字', '2858')]
正控制-docs层 扫描页数 1 违规: [('02-tools/figure_library.md:3', '条数', '2858 条思维模式'),
                                ('02-tools/figure_library.md:3', '旧口径裸数字', '2858')]
对照-原始 docs 产品页零违规: 5 []
```

## 5. 线上回读（部署前 / 部署后）

```
# 部署前（QA3 复现）
$ curl -sL …/protreptic/manifest.webmanifest | grep -o '"description": "[^"]*"'
"description": "2858 条思维模式 × 283 位历史人物：…"
$ curl -sL …/protreptic/docs/02-tools/figure_library/ | grep -c '2868'   → 3

# 部署后（本次 db827b0 发布）
$ curl -sL …/protreptic/manifest.webmanifest | grep -o '"description": "[^"]*"'
"description": "2848 条思维模式 × 283 位历史人物：每条都有出处、操作步骤与现代应用，中英双语，可离线查阅。"
$ curl -sL …/protreptic/manifest-light.webmanifest | grep -o '"description": "[^"]*"'
"description": "2848 条思维模式 × 283 位历史人物：每条都有出处、操作步骤与现代应用，中英双语，可离线查阅。"
$ curl -sL …/protreptic/ | grep -oE '<meta name="description" content="[^"]*"|<meta property="og:description" content="[^"]*"'
<meta name="description" content="2848 条思维模式 × 283 位历史人物：每条都有出处、操作步骤与现代应用。以人为鉴，明得失。"
<meta property="og:description" content="2848 条思维模式 × 283 位历史人物 · 中英双语"
$ curl -sL …/protreptic/docs/02-tools/figure_library/ → 判定式短语统计
      1 10 条思维模式
      2 283 位历史人物
      2 2848 条思维模式                 ← 无 2858 / 2868 短语
```

线上该 docs 页剩余的 `2868` 命中（`grep -c` = 4 行） 全部落在**逐行标注了「源库 / 原始记录 / 口径」的句子**里
（如「源库 `data/modes_data.json` 的原始记录口径是 284 位 / 2868 条」），是如实交代源库与
站上发布口径的差别，不是第二种门面数字 —— 这正是本卡选择的处置方式（QA3 亦允许）。

## 6. CI 实况（head db827b0）

```
$ gh run list --repo ovmobilegroup/protreptic --limit 4 --json databaseId,name,status,conclusion --jq …
35417113999 Quality Gate completed/success
35416909517 Protreptic CI/CD completed/success
35416909492 CI completed/success
35416909490 Deploy to GitHub Pages completed/success
$ git -C /opt/data/release/Protreptic-publish push origin main
To https://github.com/ovmobilegroup/protreptic.git
   5b1936b..db827b0  main -> main
$ git -C /opt/data/release/Protreptic-publish status -sb
## main...origin/main            # 无 [ahead N]
```

## 7. 刻意保留的范围与理由（未归零的地方，逐项交代）

1. `web/dist/**`：**零例外**。全量扫描 2731 个文件，`2858 条思维模式` / `2868` / `284 位`
   在门面文件里全部归零（裸数字扫描覆盖 html/webmanifest/txt/xml/svg）。
2. `data/**`（产物里的数据文件）：允许出现 `modes_raw=2868` / `mode_summaries=2858` 这类
   **内部计数键**（`data/meta.json` 的 `counts`，数据契约，页面不展示）；正文里「1122 条模式」
   之类的**别的规模**（人物档案/入库记录的史实文本）也不判违规 —— 门面判定式只认
   「N 条思维模式 / N 位历史人物」。
3. docs 站的历时页面（`docs/qa/phase3*_acceptance.md`、`docs/architecture/*`、`docs/phase3*_final_report.md`、
   `docs/review/*`、`docs/figures/*` 等）：保留当时的实测数字，属历史记录而非当前产品门面，
   QA3 已认可该处置；本卡的门面硬门只覆盖 `docs/index.md` + `docs/02-tools/**`（产品门面页）。
4. `api/protreptic.db` 的 `thinking_modes` 表 2858 行：这是 API 层（本地 FastAPI）的库内行数，
   页面上已按「源库去重口径」标注。

## 8. 坑（本卡踩到的，值得记住）

- **`pymdownx.betterem`（smart 模式）+ CJK**：`是**原始记录**口径` 这种「强调符两侧紧贴汉字」
  的写法**不会渲染成粗体**（线上实测字面输出 `**原始记录**`）。写 docs 时把粗体挪到标点旁，
  或直接用「」。
- 预渲染会把 `web/index.html` 的 HTML 注释复制进每一个路由页：一句注释里的旧口径裸数字会
  变成 1353 个页面里的残留（本卡正是靠删掉注释里的数字才让产物裸数字归零）。
- 共享模块改动也要进 workflow 的 `paths` 过滤，否则「只改共享模块」的 push 不触发部署。
