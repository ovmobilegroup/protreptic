# Phase35-V1FIX 计数源收敛报告

- 任务卡: t_3e0d222c (elcano)
- 日期: 2026-09-19 (CST)
- 结论: 已完成. 原 5 个伪人物 /minds/* URL 线上全部 404; 站点口径 2798 条思维模式 x 278 位历史人物
  从 meta.json 到首页 head / 两份 manifest / sitemap / docs 产品页全站自洽;
  Deploy to GitHub Pages / CI / Quality Gate / Protreptic CI/CD 四个 workflow 全绿.

## 1 根因 (Pages run 35428849131)

V1 (d8c809c) 隔离 5 个伪人物 / 60 条模式后, 静态门面 (dist/index.html 的 meta, 两份 PWA manifest)
由 tools/apply_site_counts.py 在**构建之后**跟着 meta.json 走, 而 SPA 运行时文案
(web/src/composables/useSeo.ts 的默认 description, App.vue 页脚, FiguresView / ApiDocsView /
DailyView 的条数) 是**构建期编译进 dist/assets/*.js 的字面量**, 构建之后改不了:

```text
[counts] dist/assets/*.js 里找不到 description 目标串
2798 条思维模式 x 278 位历史人物: ...
静态 head 与 SPA 运行时文案已分叉 (见 web/src/composables/useSeo.ts)
-> exit 1 -> 构建失败 -> 部署跳过 -> 线上照旧
```

## 2 改动

1. 新增 tools/gen_web_site_counts.py (npm run build **之前**跑): 读部署产物 data/meta.json,
   用 tools/site_counts.py 的同一套取数与模板生成 web/src/generated/siteCounts.ts (纯字面量).
   SPA 全部改为 import 它, 不再各写各的数字; 字面量会原样进 dist/assets/*.js,
   apply_site_counts 的交叉校验因此成立. pages.yml 增加该步骤 (生成物入库,
   干净 checkout 与 Docker 构建也有类型与兜底值).
2. tools/apply_site_counts.py 补两处漏网门面:
   - dist/404.html: 未预渲染深链的回落外壳, 与 index.html 同一份 head, 此前只改 index.html;
   - docs 产品门面页: 先对齐再体检 (判定规则与扫描完全一致, 历史报告页不在此列).
3. tools/site_counts.py: DOC_SOURCE_LABELS 去掉 "口径". 豁免的本意是 "如实交代源库与站上发布数的
   差别", 而 "站上发布口径 2848 条" 恰恰是在声称站上发布多少, 属于门面. 不堵这个洞,
   docs/02-tools/figure_library.md 同一页会同时写着 2798 与 2848.
4. mkdocs.pages.yml 的 docs 站 site_description, docs/index.md, docs/02-tools/figure_library.md
   同步到 2798 / 278; 源库口径 (284 位 / 2868 条 / 2858 条去重) 原样保留.
5. 顺带修 docs/qa/credibility_audit.md 的 markdown-lint (仅加空行, 无内容改动):
   CI (.github/workflows/markdown-lint.yml) 自 10c8dfc 起一直失败, 挡着 CI 全绿.

## 3 本地验证 (命令 + 原始输出)

```console
$ cd web && VITE_DATA_MODE=static npm run build
dist/index.html                   3.66 kB | gzip:   2.07 kB
dist/assets/index-Dwd55UPV.css   49.64 kB | gzip:   9.32 kB
dist/assets/index-DyYMlABQ.js   339.80 kB | gzip: 124.30 kB
built in 5.86s

$ python3 tools/apply_site_counts.py
[counts] manifest 已一致: web/public/manifest.webmanifest -> 2798 条思维模式 x 278 位历史人物 ...
[counts] manifest 已一致: web/public/manifest-light.webmanifest -> 2798 条思维模式 x 278 位历史人物 ...
[counts] manifest 已一致: web/dist/manifest.webmanifest -> 2798 条思维模式 x 278 位历史人物 ...
[counts] manifest 已一致: web/dist/manifest-light.webmanifest -> 2798 条思维模式 x 278 位历史人物 ...
[counts] 收口完成: 2798 条模式 x 278 位人物 (来源 web/dist/data/meta.json)
[counts] dist 扫描 1365 个文件零违规; docs 产品门面页 5 个零违规
ACCEPTANCE EXIT=0
```

完整流水线 (export -> gen -> daily -> unified -> npm build -> prerender_routes -> apply_site_counts)
同样 exit 0: dist 扫描 2711 个文件零违规 (含 1348 个预渲染路由页与 404.html).

```console
$ python3 tools/ci_data_check.py
数据校验: 24 条断言, 失败 0 条
数据校验: PASS

$ python3 tools/pages_preflight.py --stage data      # [OK] stage=data 全部断言通过
$ python3 tools/pages_preflight.py --stage dist      # [OK] stage=dist 全部断言通过
$ cd tools && python3 test_thinking_mode_selector.py # === ALL TESTS PASSED (11) ===
$ npx --yes markdownlint-cli2 --config .markdownlint.json "**/*.md"
Linting: 225 file(s) / Summary: 0 error(s)
```

## 4 线上回读 (curl, 2026-09-19 部署 2e3e7a6 之后)

```console
$ for u in minds/H-P23F-001 minds/P24F minds/P25F minds/P26F minds/Phase27Final; do
    curl -s -o /dev/null -w "%{http_code}\n" "https://ovmobilegroup.github.io/protreptic/$u/"; done
404
404
404
404
404
```

不带尾斜杠的形式同为 404; 已隔离的 H-SX-001 亦为 404.

```console
$ curl -s "https://ovmobilegroup.github.io/protreptic/data/meta.json"
mode_summaries_published=2798  mode_by_figure_shards=278  mode_summaries(源去重)=2858  modes_quarantined=60

$ curl 线上 /data/index.unified.json
counts: {"total": 1333, "figures": 278, "scenarios": 1055, "with_modes": 1297}
code H-P23F-001 -> 0 条   code P24F -> 0 条   code P25F -> 0 条
code P26F -> 0 条         code Phase27Final -> 0 条   code H-SX-001 -> 0 条
```

门面文案与 meta.json 逐字节自洽:

```text
/ 首页 description   : 2798 条思维模式 x 278 位历史人物 ...  => OK
/ 首页 og:description: 2798 条思维模式 x 278 位历史人物 - 中英双语 => OK
/manifest.webmanifest       => OK
/manifest-light.webmanifest => OK
/sitemap.xml loc 数 1349, 5 个伪人物 code 出现 0 次
docs 站 /docs/ 与 /docs/02-tools/figure_library/ 门面数字只出现 2798 / 278
```

## 5 CI (job 名 + conclusion, commit 2e3e7a6)

```text
Deploy to GitHub Pages #73  success
    构建 SPA + 文档站   success
    部署                success
CI (markdown-lint)   #81    success
    markdown-lint       success
Quality Gate         #61    success
    数据校验 (schema + sitemap 一致性)      completed successfully  (1m27s)
    线上死链检测 (sitemap + 站内链接)       completed successfully  (19s)
    Lighthouse 预算门                      completed successfully  (1m58s)
Protreptic CI/CD     #81    success
```

发布仓状态: `git -C /opt/data/release/Protreptic-publish status -sb` -> `## main...origin/main` (无 ahead).

## 6 遗留 (不在本卡范围, 供后续卡决策)

1. docs 站的 docs/figures/H-P23F-001/ 仍为 200 (伪人物的 "人物档案" 页仍被 mkdocs 收录并发布).
   SPA 侧 /minds/* 已 404, 名录已剔除; 其余 4 个伪人物只有 .json (不入 mkdocs, 实测 404).
   删该页属于内容层面处置, 留给可信度体系卡.
2. api/protreptic.db (38 MB) 可以移出 git 跟踪, 但要配套改 CI:
   - 它由 tools/build_figures_db.py 从已提交的 tools/json/scenarios_*.json 重建 (本卡实测:
     重建后行内容不变, 仅 sqlite 文件内部字节不同);
   - 但 tools/build_unified_index.py 把 db 当**可选**输入, db 缺失只输出人物 -- 只把文件从索引里
     摘除而不给 ci-cd.yml 的 test job 补一步 build_figures_db, tools/test_thinking_mode_selector.py
     会因场景缺失失败. 建议处置: 单文件 git rm --cached + .gitignore 增补 + ci-cd.yml test job
     增加 "重建 figures 数据库" 步骤 + 文档说明; 历史里的 38 MB blob 需要 filter-repo 才能瘦身
     (另开卡).
3. 双仓 data/modes_data.json 存在差异: 项目仓每条模式多了 verification 字段
   (status=pending / method=auto-scan 的迁移产物), 发布仓尚无. 本卡未同步该字段
   (属可信度体系卡的范围, 避免把未定稿 schema 带上线).
4. 发布仓的 web/dist 有 5 个历史遗留文件被 git 跟踪 (.gitignore 已写 web/dist/), 本地构建会
   把它们改脏; 建议 hygiene 卡把该目录整体从索引里摘除.
