# Phase21 W4 补正-B-a en 扩展位落盘 执行报告 (卡 t_def07a84)

日期: 2026-09-24 (CST) | 工作仓: /opt/data/workspace/Protreptic | 发布仓: /opt/data/release/Protreptic-publish
上游: t_33240de8 (fix2, R2 zh 扩展位) -> t_8bad8d98 (W4 QA) -> 本卡 -> t_616e4991 (W4 文档归档)

## 一, 结论速览

1. 落盘: tools/json/scenarios_zh.json 的 H-LXN-001 条目 en 侧 4 扩展位 (name_en / description_en / reason_en / case_en) 各 1 处, Mao Xiannian -> Li Xiannian.
   真字节窗口 645917 / 646781 / 648210 / 651925 (raw bytes.find 实测); 全文 2981559 -> 2981555 B (-4B);
   sha256 8b218e717cdb... -> e6777e7a556f...; 语义 diff 仅该 4 字段, 其余 1039 条目零变更 (字节级 shift 对位 + JSON 级双断言).
2. 补记: docs/research/phase21w4_fix2_report.md 与 .json 的 B-a 条目加补记 (船长裁定 + 本卡落盘 + sha 变迁; en 残留状态作废, 终态以本报告为准).
3. 备份: data/backup_phase21w4_fix3_20260924/ (payload byte-exact + fields_before.json 4 字段 before/after_expected + 真字节偏移; MANIFEST.sha256 4/4 PASS).
4. 全链 18 步复跑 (同 fix2 口径): 17/18 rc=0; 第 12 步 (ci_data_check) 首跑 rc=1, 实证 R9 半链滞后 (routes person=318 对 unified 320, 点名 H-AZJ-001 / H-SHF-001);
   第 15/18 步 (prerender_routes / build_sitemap) 补齐后, 第 12 步复跑 24/24 PASS.
5. 终态门禁复跑全绿: ci_data_check 24/24 / preflight data+dist / credibility_gate / verify_findings / verify_source_links 全 rc=0.
6. 残扫: ws 活跃面 Mao Xiannian 命中 = 0 (豁免类逐类登记); 两仓构建树 (web/public/data + web/dist) 命中 = 0; pb 侧 data/intl_figures 惰性档 4 处另案登记 (第6节).
7. 计数: figures 1027 / modes 3241 x by-figure 320 / unified 1344 (320+1024) 与开工实测零变化;
   routes 1358 -> 1360 / sitemap 1359 -> 1361 = R9 合并后口径补齐 (非本卡语义引入; 逐条归因见第4节).
8. 提交 / 镜像 / push / parity 回执: 见第7节 (v2 补记).

## 二, 落盘与字节级证据

- 编辑面: $.H-LXN-001 {name_en, description_en, reason_en, case_en}; 每处 "Mao Xiannian"(12B) -> "Li Xiannian"(11B), 全文 -4B.
- 开工基线: 2981559 B / sha256 8b218e71... / 命中 x4 (窗口经船长实测, 本卡复算一致; 见下 "偏移口径勘误").
- 落盘后: 2981555 B / sha256 e6777e7a... / 命中 x0; Li Xiannian 全文 5 处 = 既有 1 处 + 本卡新增 4 处.
- 映射复验 (见证器 A10-A13): before 文件 4 窗口逐字节 = "Mao Xiannian"; after 文件新增 4 窗口位置 = {632100, 645917, 646780, 648208, 651922} (既有 1 处随 shift -1..-4 移动);
  显式拼接重建 (before + 4x LI 替换) == after 全文; 区域外全部字节按累计 -1x/-2x/-3x/-4x shift 对位逐字节相等 (bad=0).
- JSON 级零越界 (见证器 A14/A15): 变更字段集合 == 恰好 4 个 en 字段; 其余 1039 条目全等.
- 偏移口径勘误 (防呆, 卡面点名): 上游 fix2 / QA 曾把码点偏移误标为 occurrence_byte_offsets.
  本卡备份 fields_before.json 同时载: occurrence_byte_offsets = [645917, 646781, 648210, 651925] (真字节, raw bytes.find, 本卡实测)
  与 occurrence_codepoint_offsets_informational = [286335, 286795, 287938, 290609] (参考, 非字节口径); 见证器 A9b/A9c 对双口径分别断言.
  勘误记录: 真实字节偏移与码点偏移相差约 355-361K (中文文本 UTF-8 多字节累积), 此前 QA 报告的窗口值按字节口径采信, 一致.
- 备份核对: MANIFEST.sha256 4/4 PASS; payload copy sha == before pin; backup_manifest.json 载 sha256_copy 与 copy_byte_exact=true.

## 三, 全链复跑证据 (18 步, 同 fix2 口径)

序号 / 步骤 / rc / 结果摘要:

01 build_figures_db rc=0 (0.2s) | 02 export_static_site rc=0 (2.5s) | 03 gen_web_site_counts rc=0 (0.0s, 已一致)
04 build_daily_index rc=0 (0.4s) | 05 preflight_data rc=0 (0.2s, figures=1027 modes=3301 published=3241 隔离命中=0 by-figure=320)
06 build_search_index rc=0 (2.5s, 16 分片 + meta) | 07 build_graph_data rc=0 (0.8s, 模式图 3678 节点/7162 边; 概念图 320 人物/14886 概念)
08 build_unified_index rc=0 (0.5s, total=1344 figures=320 scenarios=1024 with_modes=1308)
09 credibility_gate rc=0 (5.1s, 存量 524 冻结 / 新增 0)
10 verify_source_links rc=0 (259.8s, 383 链接; 无新增坏链, UNREACHABLE 属网络波动警告)
11 verify_findings rc=0 (6.0s, 无新增硬失败, 存量 0 冻结)
12 ci_data_check rc=1 (0.1s) 首跑失败 = R9 半链滞后实证: cross.coverage 2 条名录无路由 [H-AZJ-001, H-SHF-001]
13 npm_build rc=0 (11.2s, assets/index-DvgMwhwc.js 342.05 kB)
14 preflight_dist rc=0 (0.0s) | 15 prerender_routes rc=0 (1.4s, routes=1360, 正文快照 330 条, 1360 index.html)
16 apply_site_counts rc=0 (2.5s, dist 扫描 2743 文件零违规; 6 门面零违规)
17 build_sw rc=0 (0.0s, shell=protreptic-shell-e873f2b47495, data 版本 20260924024900)
18 build_sitemap rc=0 (0.2s, entries=1361)

终态门禁复跑 (链后 + 非语义归一化后):

工具 / rc / 结果:

ci_data_check rc=0 | 24 断言 / 失败 0 (名录 1344 = 人物 320 + 场景 1024; 路由 1360; sitemap 1361)
pages_preflight --stage data rc=0 | figures=1027 modes=3301 published=3241 隔离命中=0 by-figure=320
pages_preflight --stage dist rc=0 | dist index.html + 404.html 逐字节相同 + data/ + /protreptic/ 前缀
credibility_gate --hard-fail rc=0 | 存量 524 冻结 / 新增 0
verify_findings --hard-fail rc=0 | 无新增硬失败
verify_source_links --hard-fail rc=0 (217.2s) | 无新增坏链

链日志: scratch/w4fix3/chain_logs/01..18 (*.out + *.rc) + R05/R09/R10/R11/R12/R14_final_* (终态门禁).
说明: 第 12 步首跑 rc=1 -> 15/18 补齐 -> 复跑 24/24 是本次复跑最重要的新实证 (见第4节).

## 四, 差异面归因与归一化 (逐条, 不静默)

A. 开工态背景: 板面处于 R9 合并后 "半链" 状态: 数据面已到 R9 口径 (by-figure 320 / published 3241),
   而 routes/sitemap 仍为 R9 前口径 (person 318 / count 1358 / sitemap 1359); index.unified.json 缺席
   (R9 站链五步 = export + gen + apply + daily + preflight, 不含 06/07/08/15/18 步; export 会清空 web/public/data).
   -> 12 步首跑失败即此滞后的实证 (exact 点名 [H-AZJ-001, H-SHF-001]).
B. 本链产出与归因:
   - web/public/data: 1360 -> 1385 件 (+25 = search 17 + graph 7 + index.unified.json 1; -0; 改 3 = daily/index.json, daily/names.json, meta.json 重生成, 计数不变, 戳记更新).
   - web/dist: 1382 -> 2769 件 (+1387 = 1360 预渲染页 + 25 数据 + 2 其余; -0; 改 4 = data/daily/index.json, data/daily/names.json, data/meta.json, sitemap.xml).
   - docs/architecture/web_p0_routes.json: 1358 -> 1360; 增 minds/H-AZJ-001, minds/H-SHF-001 两条路由; 无删除;
     3 条文案随口径更新 (credibility 3221->3241 / pending 1897->1917; figures 318->320; modes 3221->3241).
   - web/public/sitemap.xml: 1359 -> 1361; 仅新增上述 2 条 URL; 既有 1359 条逐条不变.
   - web/src/generated/siteCounts.ts: 零变化 (gen_web_site_counts rc=0 且未写).
C. 非语义 churn 归一化 (fix2 同口径): api/protreptic.db 行级全等 (仅 sqlite 布局字节) -> git checkout HEAD 复原 (c5eb126e);
   docs/architecture/static_data_manifest.json 仅 generated_at + db sha 链 -> 复原 (9bf53ce4).
D. 保留链后态、未提交 (边界判定): routes/sitemap 的 R9 口径补齐是本链 15/18 步的产出, 非本卡语义面
   (4 处文本替换不可能产生计数变化; 归因为 R9 数据 + R9 站链缺步). 按边界② (不碰构建图) 与④ (不夹带), 本卡
   不将其纳入提交面; 工作区保留链后一致态 (12 步 24/24 以该态达成), 提交面 = 第7节清单.
   如需收口入库, 请 R9 链或 W4 归档卡按其口径处置 (一条 git add 即可: docs/architecture/web_p0_routes.json + web/public/sitemap.xml).
E. 计数口径对照 (开工实测 vs 链后 vs 卡面):
   面 / 开工实测 / 链后终态 / 卡面预期 / 判定:
   figures 1027 / 1027 / 1027 / 零变化 OK
   modes (published x by-figure) 3241 x 320 / 3241 x 320 / 3221 (R9 前口径) / 零变化 OK (卡面 3221 为 R9 前; R9 anchor 3301/320 保持)
   unified 缺席 (R9 半链瞬态) / 1344 (320+1024) / 1342 (318+1024, R9 前) / 链后重建 = R9 口径; 卡面值为 R9 前
   routes 1358 (318 person) / 1360 (320 person) / 1358 / +2 = R9 口径补齐 (第4节 A/B; 12 步失败实证)
   sitemap 1359 / 1361 / 1359 / 同上 +2
F. 他卡在制/外来面 (登记, 未触碰): W8 stage2 批1 (tools/build_source_links.py / fetch_source_texts.py / source_link_index.py 改动 + data/audit/source_texts/* 23 件);
   R9 QA 链 (docs/research/phase21r9_azj_qa_evidence.json/.txt 等); W6 marker_scan; 素材卡报告. 均不在本卡提交面.

## 五, 验证 (残扫 / 见证器 / 备份 / 门禁)

1. 活跃面残扫 (bytes 级, ws): Mao Xiannian 活跃面命中 = 0; 豁免类逐类登记 (备份 11 件 / 报告 10 / QA 3 / site_docs 5 / 根副本 4 / 见证器类 1).
   定向 pin: 根 H-LXN-001.json = 4 (W7 在途, 未触碰); CHANGELOG.md = 0 (其历史条目属中文串, 拉丁目标零命中);
   docs/figures/H-LXN-001.md = 0 (R-c 注记属中文串); verify_phase21w4_qa_espinosa.py = 3 (他卡 QA 见证器自带样本, 同 W4 QA verifier 豁免口径).
2. 构建面残扫: 两仓 web/public/data + web/dist 全树零命中 (含预渲染页 1360 件).
3. 备份面: MANIFEST.sha256 4/4 PASS + payload byte-exact (见第2节).
4. 门禁四连 + 双 preflight + ci_data_check 24/24: 见第3节 (终态全绿).
5. 见证器复跑: python3 verify_w4fix3_lxn_en.py (--quick = A-D 段 34 PASS / 0 FAIL; 全量含镜像面见第7节).
6. 字节级全量校验: 区域外 shift 对位逐字节相等 (bad=0); JSON 级零越界; 见证器 A10-A15 覆盖.

## 六, 边界与登记 (不静默)

- B-a 终态翻转: fix2 报告第6节 B-a 条目的 en 残留状态作废 (已补记); 终态 = 源面 0 残留 (本报告).
- E-a (新登记, 惰性档): pb 侧 data/intl_figures/H-LXN-001.json 含 Mao Xiannian x4. 该目录为 pb 独有 (610 件), 开工基线与
  ws 均无, parity 规则排除 (parity 文档: 无任何构建步骤/前端读取), pages.yml 亦不部署; 属未进构建图的惰性档.
  本卡边界外未触碰; 建议按 W7/R-b 同类 "先登记后裁定" 处置 (候选: 后续卡统一清理, 或在 parity 排除清单加注).
- E-b (登记): verify_phase21w4_qa_espinosa.py 承载 QA 扫描样本串 (3 处), 属见证器类豁免 (W4 QA 口径 verifier 同类).
- E-c (登记): CHANGELOG.md 与 docs/figures/H-LXN-001.md 的既有豁免针对中文错名串 (毛先念), 对拉丁目标 Mao Xiannian 为零命中; 两文件本次零变更.
- E-d (登记): routes/sitemap 保留链后态未提交 (见第4节 D); 本卡提交面不含构建图文件.
- E-e (登记): W8 / R9 QA / 他卡在制面零触碰 (第4节 F); 链日志中 UNREACHABLE 1 条为网络波动警告 (存量冻结口径, 非新增坏链).
- E-f (登记): 开工时板面半链态 (unified 缺席 / routes 滞后) 为 R9 站链五步口径的自然结果, 非缺陷引入; 本链已补齐 (12 步 FAIL -> 24/24).

## 七, 回执 (提交 / 镜像 / push / parity) 与见证器全量

- 工作仓 commit (v1): 3f102ee1 (12 files changed, +916 / -2; 目标编辑 + fix2 补记 + fix3 报告/证据 + 备份 5 件 + 见证器; 无他卡混入; db/manifest 已归一化复原).
- 发布仓镜像 (v1): 0dda13a (12 files byte-exact 12/12; 对齐工作仓 3f102ee1).
- push: 78bac29..0dda13a main -> main (rc=0); remote main = 0dda13abc4f8f371139141a340fca5f411fdd548 (= 本地).
- 远端 raw 抽验 (6 件 @0dda13a): scenarios_zh.json e6777e7a / fix3_report.md 986cf699 / fix3_report.json c497ceeb / fix3_evidence.json 1901d65f / fix2_report.md 14312ff8 / 见证器 288c75e8; http=200 且逐字节 SAME (6/6).
- 见证器全量 (镜像后): 39 PASS / 0 FAIL (E1 镜像 12 件 byte-exact; E2 两仓构建树零命中; E3 pb live 面 0; E4 intl 惰性档 pin).
- parity (镜像后, tools/check_repo_parity.py --json): 边界内共同件 2530 / 逐字节一致 2525; 差异 42 条全部归因:
  CONTENT_DIFF 5 = 本卡链后态保留未提交 2 (docs/architecture/web_p0_routes.json, web/public/sitemap.xml) + W8 在制 3 (tools/build_source_links.py, tools/fetch_source_texts.py, tools/source_link_index.py);
  MISSING_IN_PUBLISH 37 = W8 stage2 批1 27 件 (data/audit/source_texts/* 20 + source_texts_w8_stage2_batch1.json + recount x2 + sourcing_report x2 + booklist x2) + W4 QA 产物 2 件 (docs/qa/phase21w4_qa_report.md, docs/qa/phase21w4_qa_evidence.json; 其卡未见镜像) + 早期卡文档 8 件 (fix_manifest x2 / r8 names_recon x2 / w6 marker_scan x2 / w10 coverage x1 / candidates_v5 x1);
  only_publish 0; 本卡覆盖 12 件 0 残留 (全部 identical). 原始: scratch/w4fix3/parity_post.json (镜像前 64 条: parity_pre.json).
- 回执终版 (v3): v2 工作仓 a8ec9afe (3 件, +100 / -3) / 镜像 3cb64c3 / push 0dda13a..3cb64c3 main -> main (rc=0);
  远端复核 3cb64c3eb3333d52c5aff586b7187079eef6c5ee (= 本地, ls-remote 一致); v3 本条的提交/镜像/push/远端 raw 终跑记录在 kanban 回执 (t_def07a84 comment 与完成 metadata).

## 八, QA 复跑指引

- 见证器: python3 verify_w4fix3_lxn_en.py (默认全量; --quick 跳过镜像面; --publish DIR 指定发布仓).
- 链日志: scratch/w4fix3/chain_logs/01..18 + R05/R09/R10/R11/R12/R14_final_*.
- 快照与归因: scratch/w4fix3/snap0/1/2.json + analyze_chain.py + deltas.py + scan_mao.py + parity_pre.json.
- 备份: data/backup_phase21w4_fix3_20260924/ (sha256sum -c MANIFEST.sha256).
- 计数与规格钉住: 本报告第4节 E 对照表; 见证器 C 段断言 (含 R9 后口径注记).

## 九, 与前序链关系

- fix2 / W4 QA 的 pin (scenarios_zh after sha 8b218e71 / en 残留 x4 / B-a 未处理) 由本卡翻新为: e6777e7a / x0 / 已处理;
  fix2 报告已补记; W4 QA 报告第9/10节的 B-a 未处理记载以本报告为准 (QA v3 见证器 pin 8b218e71 属其窗口 pin, 本卡为合法后继写者).
- R9 双链 (t_ce457734 / t_a7d233f0 / t_b6d4c0ee 等) 的站链锚点 3301/320 由本链保持 (05 步实测); routes/sitemap 滞后补齐见第4节.
- 下游 t_616e4991 (W4 文档归档): 建议将本报告 + fix3 证据 + fix2 补记纳入归档面; routes/sitemap 未提交项请一并裁定.
