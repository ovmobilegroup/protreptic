# Phase21 W4 补正·R2 zh 扩展位落盘·执行报告 (卡 t_33240de8)

- 卡号: t_33240de8 (单写者执行卡); 背景: 船长核验 (09-24) 发现 t_536073f4 报告 §2.2 声称未落盘; 依据: manifest §八-1 待复核第 1 项 (船长裁定: 采纳执行)
- 上游: t_ee203180 (done); 下游: t_8bad8d98 (独立 QA) -> t_616e4991 (文档)
- 证据 JSON: docs/research/phase21w4_fix2_report.json | 备份: data/backup_phase21w4_fix2_20260924/ | 见证器: verify_w4fix2_lxn.py

## 一, 结论速览 (全部实测)

| 项 | 值 |
|---|---|
| 落盘 | tools/json/scenarios_zh.json $.H-LXN-001 4 扩展位 (name_zh/description_zh/reason_zh/case_zh) 毛先念 -> 李先念 |
| 最小 diff | 文件 2981559 B 不变; sha256 9727c8eaaf96ab92 -> 8b218e717cdb8cb5; 字节级差异 8 字节 = 4 窗口 x 2 字节; 其余 1039 条目零变更 |
| 全链复跑 | 18 步 rc=0 (数据链 8 + 门禁四连 4 + 构建链 6); preflight --stage data/dist 双 PASS |
| 计数零变化 | figures 1027 / routes 1358 / sitemap 1359 / unified 1342(318+1024) / 发布模式 3221 / by-figure 318 |
| 差异面 | 原始重跑出现 26 项差异, 全部内容级归因 (24 件仅 generated_at 戳记 + DB 仅 sqlite 布局字节 + manifest 戳记); 按零差异契约归一化基线后, 终态差异 = 仅目标 4 字段 |
| 门禁 | credibility rc=0 / source_links rc=0 / findings rc=0 (存量 M-ASM warning 1) / ci_data_check 24/24 PASS |
| 活跃面残扫 | 目标串命中 = 0 (tools/web/api/docs/architecture/data 等活跃面); 余量全落豁免类 (见 §五) |
| 见证器 | verify_w4fix2_lxn.py: 全量 26/26 PASS (含镜像面 1383+2765 byte-identical); --quick 23/23 PASS |
| 镜像/回执 | 见 §七 |

## 二, 落盘与字节级证据

覆盖字段与终值 (backup/fields_before.json 载 before 全文 + before_sha256 + after_expected + 字节偏移):

| 字段 | before | after | 窗口 (字节偏移) |
|---|---|---|---|
| name_zh | 毛先念 | 李先念 | 645895..645904 |
| description_zh | 毛先念(1901-1997)... | 李先念(1901-1997)... | 646237..646246 |
| reason_zh | ... 毛先念通过战略预判法... | ... 李先念通过战略预判法... | 647666..647675 |
| case_zh | ...毛先念带领经济团队... | ...李先念带领经济团队... | 651341..651350 |

- 字节结构: 4 个窗口各 9 字节 (毛先念 / 李先念, 首字节 E6 共享), 实际差异 run = 4 x 2 字节 (AF9B -> 9D8E), 逐一落在上述窗口内; 窗口外零字节变更。
- 全文计数: 毛先念 4 -> 0; 李先念 30 -> 34 (其余 30 处为既有正确引用, 零触碰)。
- JSON 有效性: json.loads PASS; 除 H-LXN-001 外其余 1039 条目逐条全等 (script 断言 other_entries_changed=0)。
- 备份: data/backup_phase21w4_fix2_20260924/ (payload 全文件 byte-exact + fields_before.json + backup_manifest.json + README + MANIFEST.sha256); sha256sum -c 4/4 PASS。

## 三, 全链复跑证据 (18 步, 日志: 工作区外 scratch/w4fix2/chain_logs/)

| # | 步骤 | rc | 关键实测 |
|---|---|---|---|
| 01 | build_figures_db | 0 | figures 表重建 1027 行 |
| 02 | export_static_site | 0 | 产物 1355 文件 (索引 1 + figures 1027 + modes 8 + by-figure 318 + meta 1); 隔离零泄漏; modes 发布 3221 |
| 03 | gen_web_site_counts | 0 | siteCounts.ts 已最新 (3221 x 318), 未改动 |
| 04 | build_daily_index | 0 | 模式 3221 / 人物 318 / 分片 318 |
| 05 | pages_preflight --stage data | 0 | [OK] 全部断言通过 (figures=1027 modes=3281 published=3221 隔离命中=0) |
| 06 | build_search_index | 0 | docs=3221 tokens=102291 postings=296937; 16 分片 |
| 07 | build_graph_data | 0 | 模式图 3658 节点; 概念图 318 人物 / 14786 概念 |
| 08 | build_unified_index | 0 | total=1342 figures=318 scenarios=1024 |
| 09 | credibility_gate --hard-fail | 0 | 无基线外硬失败 |
| 10 | verify_source_links --hard-fail | 0 | 无新增坏链 |
| 11 | verify_findings | 0 | 0 硬失败 / 1 存量 warning (M-ASM 双采) |
| 12 | ci_data_check | 0 | 24 条断言 0 失败; 路由 1358 / sitemap 1359 |
| 13 | npm run build | 0 | vue-tsc + vite rc=0 |
| 14 | pages_preflight --stage dist | 0 | [OK] 全部断言通过 |
| 15 | prerender_routes --body-persons all | 0 | routes=1358 (预渲染 1358 页) |
| 16 | apply_site_counts | 0 | dist 扫描 2739 文件零违规 |
| 17 | build_sw | 0 | 预缓存清单写出 OK |
| 18 | build_sitemap | 0 | sitemap 1359 条 (来自路由 1358 + 首页) |

计数自洽: figures 1027 = DB 行 = 分片 = 轻索引 = meta; sitemap 1359 = 路由 1358 + 首页; unified 1342 = 318 + 1024; 发布模式 3221 / by-figure 318 口径不变。

## 四, 差异面归因与归一化 (实测曾出现差异, 全数归因)

原始重跑 (编辑后全链) 与开工前基线相比出现 26 项字节差异, 逐项归因如下 (机器可读见证据 JSON attribution):

| 类别 | 件数 | 内容级归因 | 处置 |
|---|---|---|---|
| 构建戳记 (generated_at) | 24 | 仅 generated_at 字段 (及派生 sha256/gzip_bytes/sw 版本戳), 逐件语义 diff 未见过滤外差异 | 恢复基线 |
| api/protreptic.db | 1 | 仅 sqlite 布局字节; canonical 行级转储 sha 全等 (figures 1027 + thinking_modes 2858 行逐行相等), schema 全等 | 恢复基线 |
| static_data_manifest.json | 1 | generated_at + 所载 db sha 字段 (随 DB 重写滚动) | 恢复基线 |

- 24 件戳记分布: web/public/data 11 件 (meta / daily x2 / graph x6 / search x1 等) + web/dist 13 件 (data 同名 11 + sw.js + sw.build.json)。
- 归一化依据: 卡契约「预期差异面=零 (纯文本字段不进构建图)」; 上述 26 项均属重建重打性质, 无内容语义变化。
- 归一化执行: tracked 2 件 git checkout HEAD 复原 (db c5eb126e / manifest f832f46e); 24 件自发布仓基线副本复原 (复原源先验 4148/4148 逐字节等于基线)。
- 终态复核: snap0 (开工前) vs snap4 (归一化后) 全量快照比对 = 仅 tools/json/scenarios_zh.json 1 件差异 (即目标编辑)。
- 归因原始记录: scratch/w4fix2/attribution_raw.txt + analyze_diffs.py 可复跑。

## 五, 验证

1. 活跃面残扫 (bytes 级): 目标串活跃面命中 = 0; 豁免类 26 件 (备份 8 / 报告与研究文档 9 / site_docs 陈旧构建 6 / 其他既定 3: CHANGELOG 1 + 根副本 4 + figures 注记 2; 精确清单见证据 JSON rescan)。全部豁免类均属既定口径 (备份类 / 报告类 / 历史条目 / W7 待办根副本 / figures 纠错注记 / 陈旧构建产物)。
2. 关键豁免项定向断言 (见证器 D2-D4): 根副本 = 4 处 (W7 待办, 未触碰) / CHANGELOG = 1 处 (历史条目) / docs/figures/H-LXN-001.md = 2 处 (R-c 纠错注记)。
3. ws 与发布仓全树比对: web/public/data 1383/1383 + web/dist 2765/2765 逐字节全等。
4. 备份面: MANIFEST.sha256 4/4 PASS; payload copy byte-exact。
5. 门禁四连 + ci_data_check 24/24: 见 §三 (09-12)。
6. 见证器复跑: python3 verify_w4fix2_lxn.py (全量) = 26/26 PASS (含镜像面)。

## 六, 边界与登记 (不静默)

- B-a 新发现 (登记): scenarios_zh.json H-LXN-001 的 en 侧扩展位 (name_en/description_en/reason_en/case_en) 现仍为 Mao Xiannian 4 处 (拉丁文), 与 scenarios_en 已修正的 Li Xiannian 不一致; 该点未见于 manifest §3.2/§八-1 任何清单 (先前扫描只覆盖中文串)。本卡边界限定 zh 4 字段, 未触碰; 建议归后续卡裁定 (同 §八-1 模式: 先登记后裁定)。live 面现状: DB name_en 取 scenarios_en.name = Li Xiannian, 站点面不受影响。
- B-b 根目录 H-LXN-001.json (8 处: zh 4 + en 4): W7 卡 (t_d24e11bc) 处置; marker_scan record 124 已登记。
- B-c docs/figures/H-LXN-001.md (2 处): R-c 纠错注记 (设计保留, 改之反错)。
- B-d CHANGELOG.md (1 处): 历史条目不改写 (manifest 既定)。
- B-e 父证据 r2_scenarios_zh_extras 记录 after=before 为落盘前实录; 落盘后实际后像以本卡证据 JSON 为准; 父报告 §2.2 已加补正注记 (本卡提交)。
- B-f site_docs 6 件 (figures/recon/manifest 渲染页): 陈旧构建产物 (gitignore, mkdocs 未装不重建, CI 重建), 保留登记 (同 t_ee203180 E-b 口径)。
- B-g data/backup_* 六盘: 备份类留存。

## 七, 回执 (提交/镜像/push/parity/raw)

- 工作仓 commit (v1): 00bc34a2 (10 files changed, +799 / -1; 数据编辑 + 报告 + 备份 + 见证器, 无他卡混入)
- 发布仓镜像 (v1): commit 0517b38 (10 files byte-exact 10/10)
- push: 332188d..0517b38 main -> main (rc=0); remote main = 0517b387d21382307ecba168f88c6d78b542fa69 (= 本地)
- 远端 raw 抽验 (4 件 @0517b38): fix2_report.md 037583f8 / scenarios_zh.json 8b218e71 / fix2_report.json ebce64fe / verify_w4fix2_lxn.py 6c22a82a — 逐字节 OK
- 见证器全量 (镜像后): 26/26 PASS (E1 镜像面 1383+2765 全等; E2 镜像集 byte-exact)
- parity (镜像后): 共同件 2395 全逐字节一致; content_diff 0 / only_publish 0; missing_in_publish 6 = R-a 他链文档 (recon x2 / manifest x2 / marker_scan x2; 同 t_536073f4 / t_ee203180 登记口径, rc=1 已知)
- 回执终版 (v3): v2 工作仓 489b72c3 / 镜像 8e4d3e6 / push 0517b38..8e4d3e6 / remote main = 8e4d3e676038a3f1888daaf8fd80d859e0d6e611 / raw 4/4 OK @8e4d3e6 (md 7fffaaf9 / json e07c91b8 / scenarios_zh 8b218e71 / verify 6c22a82a); v3 自身 commit/push 见卡 t_33240de8 metadata

## 八, QA 复跑指引

- 见证器: python3 verify_w4fix2_lxn.py (默认全量; --quick 跳过镜像面; --publish DIR 指定发布仓)。
- 链日志: scratch/w4fix2/chain_logs/01..18 (*.out 各步全量输出)。
- 快照与归因: scratch/w4fix2/snap0..4.json + snapdiff.py + analyze_diffs.py + attribution_raw.txt。
- 备份: data/backup_phase21w4_fix2_20260924/ (cd 后 sha256sum -c MANIFEST.sha256)。
