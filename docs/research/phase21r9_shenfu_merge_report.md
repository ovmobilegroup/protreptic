# Phase21-R9 沈复（H-SHF-001）合并卡报告（t_a7d233f0）

## 1 卡片与背景

- 链位: Phase21-R9 沈复重做链 2/4 合并卡（上游素材包 t_d78053e7；重建落盘 t_b6d4c0ee，commit 59bc5471 + a515badd，19 件交付；下游 QA t_83e0d68d）。
- 先例口径: R8 王祥合并卡 t_8c521af7（d95a7b53）与罗瑞卿合并卡 t_08bbb73d；本轮同链并行卡 t_ce457734（安子介 H-AZJ-001，合并卡 1/4，在制）。
- 本卡职责: 先备份后合并（六件）/ total 随动 / 站链复跑 / parity 复测 / 镜像 + push + ls-remote 回执；单写者、零越界。

## 2 合并内容与口径（六件）

备份目录: `data/backup_merge_H-SHF-001_20260924_093849/`（六件前像 + backup_ledger.json；工作区保留，不入库，parity 排除口径）。

| 文件 | before | after | 变更 |
| --- | --- | --- | --- |
| data/modes_data.json | 顶层条目 3301 / 模式码 3291 / 空码壳 10 | 3311 / 3301 / 10 | +10 条 M-SHF-001~010 纯追加（逐字等于 A1 entries）；`total` = len(modes) = 3311；顶层块 H-SHF-001（23 键）新增于 `modes` 键前 |
| data/code_maps.json | figures 215 | 216 | H-SHF-001 注册：mode_ids = M-SHF-001~010；tags = 10 条模式名（name_zh）；cross_references 与图档逐字（3 条，0 悬空） |
| data/figure_names.json | 1084 | 1085 | H-SHF-001 -> 沈复 |
| data/scenarios_zh.json | 内层 2203 | 2213 | +10 条 C-SHF-001~010：8 键结构（code/mode_code/title_zh/title_en/text_zh/text_en/application_area_zh/application_area_en），text 由模板规则自 modern_applications_* 复算 |
| data/scenarios_en.json | 内层 2203 | 2213 | +10 条 C-SHF-001E~010E：与 zh 同体（仅 code 后缀差异） |
| data/scenario_tags.json | 内层 7518 | 7538 | +20 条：每模式 zh+en 各一条（4 键 mode_code/tag/figure_code/language，先 zh 后 en） |

合并实现: `tools/merge_phase21r9_shenfu.py`（读-改-写 + (size, mtime_ns) 乐观锁；读后被改动即中止 exit 4；`json.dump(indent=2, ensure_ascii=False)` 保留原尾换行；深拷贝防别名；幂等护栏：库中已见 M-SHF 时写盘前 ABORT）。

## 3 门禁四项

| 门禁 | 结果 |
| --- | --- |
| credibility_gate --hard-fail | exit 0（0 硬失败；D5 命中示例为存量 M-NEW-007） |
| verify_findings --hard-fail | exit 0（无新增硬失败，存量 0 条已冻结；其余警告 1 条为存量 M-ASM 双采集） |
| verify_source_links --hard-fail | exit 0（无新增坏链；UNREACHABLE 为网络波动类警告） |
| apply_verification_status --check | exit 0（库中状态与规则逐条一致，本轮零漂移；四态求和自洽：公开 3251 + 隔离 60 = 全库 3311） |

`data/audit/findings.json` 已随库刷新（audit_meta: modes_file_sha256 = 合并后 sha、top_level 3311、distinct 3301）。

## 4 站链五步（含构建前置）

前置: `web/dist` 数据面同步（cp web/public/data -> web/dist/data）+ `npm run build`（vue-tsc && vite build，产物 index-DvgMwhwc.js）——apply_site_counts 需 dist bundle 与静态 head 同文案。

1. `tools/export_static_site.py` exit 0：figures=1027 / modes(源)=3301 / published=3241 / 隔离剔除=60 / by-figure=320 / 产物 1357 文件；隔离名单零泄漏。
2. `tools/gen_web_site_counts.py` exit 0：`web/src/generated/siteCounts.ts` = 3241 x 320（sourceTotal 3301）。
3. `tools/apply_site_counts.py` exit 0：dist 扫描 1377 文件零违规；docs 产品门面 6 页零违规。
4. `tools/build_daily_index.py` exit 0：daily 3241 条。
5. `tools/pages_preflight.py --stage data` exit 0：figures=1027 modes=3301 published=3241 隔离命中=0 by-figure=320（全部断言通过）；另 `--stage dist` exit 0。

锚点更新（R9 两卡并集口径）: `tools/export_static_site.py` 与 `tools/pages_preflight.py` 的 EXPECT_MODES 3291 -> 3301、EXPECT_BY_FIGURE 319 -> 320（EXPECT_FIGURES 1027 不变）。

## 5 独立核验与上游回归

- 上游脚本合并后口径复跑: `verify_phase21r9_shenfu.py` 74 PASS / 0 FAIL / 0 WARN（证据 `docs/research/phase21r9_shenfu_verify_evidence_merged.json`）。合并后改写仅 4 处：G01 白名单扩展（合并产物面）、G02/G03/H04 按合并后预期（data 六件命中 / tools 副本零占用；data 六件 == manifest.after；tools 六副本 == 落盘基线）。
- 独立核验: `verify_phase21r9_shenfu_merge_indep.py` 53 PASS / 0 FAIL（证据 `docs/research/phase21r9_shenfu_merge_verify_indep.json`；A 输入与备份九项 / B modes 九项 / C 场景五项 / D tags 四项 / E code_maps 六项 / F names+并集与残留四项 / G 站链七项 / H 门禁四态三项 / I 上游回归一项）。判据全部重回原始文件（备份前像、落盘包、主库现值、站点产物、git 清单），不采信合并卡自述。
- 关键结论: 六件均为「前像 + 增量」纯追加（其余条目逐字未动）；追加段逐字等于 A1 entries；xref 0 悬空；归档三件（H-HAN-001 系列）字节未变；M-SHF/C-SHF/H-SHF 仅出现于白名单面。

## 6 parity / 镜像 / push 回执

- 主提交: **5a657b81**（工作仓 master，24 件）。
- 发布仓镜像: **2ec3af3**（81 件: 本卡 24 件 + A1 落盘 19 件随链收敛 + 见证 39 件；逐件 cp 后 sha256 全量比对 81/81 byte-exact；对齐工作仓 5a657b81）。
- push 回执: `c646f41..2ec3af3  main -> main`；`git ls-remote origin main` == **2ec3af3f4de46bc31b31fe1d07b9a39db70564db**（复核一致）。
- 工作仓 push: 不适用（开发仓 master 非 push 目标；远端仅 main，dry-run 会触发全量历史上传被服务端拒绝，既有事实见 phase45_acceptance.md / link_coverage.md §10.1）。
- parity（镜像后实测, `tools/check_repo_parity.py --json`）: 60 条差异（58 MISSING_IN_PUBLISH + 2 CONTENT_DIFF），全部属他链在制（安子介合并链 t_ce457734 的 figures/individuals/landing/witness/证据报告 40+ 件；W4 QA 与 W8 批1 / W10 / W6 文档；素材卡 sourcing 报告；`tools/build_source_links.py`、`tools/source_link_index.py` 为他卡在制改动）；**本卡覆盖 81 件 0 残留**。

## 7 并集与在途写者说明

- 兄弟卡 t_ce457734 同时在制（其已于 09:25~09:32 落 modes/code_maps/figure_names/scenarios/tags 与站链）。本卡合并脚本以乐观锁读-改-写，读后被改动即 exit 4；实际执行为并集（M-AZJ-001~010 前 10 后 10，H-AZJ-001 图档/图名在位）。
- 站链锚点为 R9 两卡并集值（3301/320）；后续任何再跑须沿用该口径。`web/dist` 为构建产物（不入库），已同步数据面并重建 bundle。
- 备份目录 `data/backup_merge_H-SHF-001_20260924_093849/` 在工作区保留，不入库。

## 8 提交回执

- 主提交: **5a657b81**（Phase21-R9 t_a7d233f0 合并入主库，24 件）。
- 回执补记提交: 见卡回执 metadata（文件自指限制；本次回执补记含报告 §6/§8、证据 receipts 与 txt 一行）。
- 镜像提交: **2ec3af3**（发布仓）、push `c646f41..2ec3af3`、ls-remote 复核一致（详见 §6）。

## 9 附录

- 本卡产物: 六件主库 + `data/audit/findings.json` + `data/audit/phase21r9_shenfu_merge_manifest.json` + `tools/merge_phase21r9_shenfu.py` + `verify_phase21r9_shenfu.py`（合并后口径）+ `verify_phase21r9_shenfu_merge_indep.py` + 证据三件（merge_evidence.json/.txt、merge_verify_indep.json）+ `docs/research/phase21r9_shenfu_verify_evidence_merged.json` + 站链件（static_data_manifest / siteCounts / 双 manifest / docs 门面 2 页 / 锚点 2 脚本）。
- 上游 19 件随链收敛镜像（figures/individuals 三件、landing 包九件、审计 manifest、gate、landing 证据、重建报告、核验证据、生成器、核验脚本）。
- 核验脚本: `verify_phase21r9_shenfu.py`（合并后口径）、`verify_phase21r9_shenfu_merge_indep.py`（独立）。
