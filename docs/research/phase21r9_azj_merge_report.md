# Phase21-R9 安子介 H-AZJ-001 合并入主库报告（卡 t_ce457734）

日期：2026-09-24 ｜ 主库：/opt/data/workspace/Protreptic ｜ 工作区：/opt/data/kanban/boards/protreptic/workspaces/t_ce457734

## 0. 一句话
上游落盘包（卡 t_58ebf9c2，提交 602a5d47 + 回执 25176b26）的 H-AZJ-001（安子介）重建产物，已按「纯追加、零删改、可回溯」口径合并进主库六件 JSON：
modes +10（M-AZJ-001~010）、顶层块 +1、code_maps +1、figure_names +1；场景三件零写入；total 口径对齐 len(modes)（本卡写盘时为 3301）；
门禁四连与站点链条全绿；独立核验 0 FAIL。

## 1. 上游输入（冻结、复算通过）
- 落盘包：docs/scratch/legacy20_r9_azj_landing/（entries / combined / id_mapping / category_mapping / scenario_notes / top_block_proposal + figures 两件）
- 数据件：data/figures/H-AZJ-001.json、data/figures/H-AZJ-001_modes.json、data/individuals/H-AZJ-001.json、data/individuals/H-AZJ-001_modes.json
- 12 件 sha256 与 data/audit/phase21r9_azj_landing_manifest.json 一致；素材包 2 件 sha256 一致
- 三面同体：entries == combined.modes == individuals_modes.modes == figure.modes（逐字）
- 条目不变量：10/10 verification.status == pending；legacy_mode_id 全空（旧号段不复用）；图档 cross_references == []
## 2. 合并口径与写入面
| 文件 | 变更 |
| --- | --- |
| data/modes_data.json | modes 3291 -> 3301（尾部 +10 逐字等于 entries）；顶层块 H-AZJ-001 新增（23 键，位于 modes 键前）；total 3271 -> 3301（= len(modes)） |
| data/code_maps.json | figures 214 -> 215：H-AZJ-001 = {mode_ids: M-AZJ-001~010, tags: 10 条中文模式名, cross_references: []}；其余条目与顶层键零改动 |
| data/figure_names.json | 1083 -> 1084：H-AZJ-001 -> 安子介（文末）；其余零改动 |
| data/scenarios_zh.json / data/scenarios_en.json / data/scenario_tags.json | 零写入（本卡未触碰；见第 6 节链式证明） |

口径注：主库 modes 含 10 条空 mode_code 壳条目（历史基线）；export 侧去壳口径 dedup 3281 -> 3291。
旧载荷复核：H-AZJ-345 判死件 19 项代表标记，在库内本卡 10 条与素材包中零出现。

## 3. 执行与安全护栏
- 合并脚本：tools/merge_azj_hazj001.py（仓库留档；含 幂等护栏 / 序列化自检 indent=2 逐字节复写 / before-after 不变量断言 / 在途写者护栏）
- 预检：python3 tools/merge_azj_hazj001.py --dry 通过
- 备份：data/backup_merge_H-AZJ-001_20260924_092502/（六件 + backup_ledger.json；sha 与 before 一致，核验复算）
- 单次写盘：写三件 + 零写三件；写后自检（前缀全等 / 非目标键零改动 / 场景三件 sha 不变）
- 事故登记（如实）：首轮写盘后自检在 after 段因脚本别名缺陷（cm2 = cm、fn2 = fn 同体变异，比较集被污染）中断；
  数据面本身正确无损——按备份回滚三件并以 sha256 -c 验证还原（回到 3291 / 214 / 1083 口径），修正断言后以同一 TS 重跑，
  得到干净的「单次写盘」终态；此后所有 after sha 与 manifest 记录一致。

## 4. 门禁四连（全部 exit 0）
- tools/credibility_gate.py --hard-fail -> exit 0
- tools/verify_findings.py --hard-fail -> exit 0（M-ASM 双收为存量警告）
- tools/apply_verification_status.py --check -> exit 0（四态与库一致；AZJ 10 条保持 pending，零漂移）
- tools/verify_source_links.py --hard-fail -> exit 0（无新增坏链）
- 连带刷新：data/audit/findings.json 按合并后库 sha（a3db9199...）重建，findings 165 条（D1 60 / D2 10 / D3 6 / D4 27+24 / D5 1 / D6 37 / D7 0），总档不变；
  随后兄弟卡 t_a7d233f0 又按 3311 口径重建（当前 HEAD 版本 audit_meta.modes_file_sha256 = 6f3f4580...，链式一致）。

## 5. 站点链（五步）
- 前置：web/ npm run build（vue-tsc + vite 全绿）。作用：web/dist/data 为上次 build 的陈旧快照（3221 x 318），
  本步把它刷新到当时数据面，apply_site_counts 才能取到正确目标串（与 W5 卡先例一致；dist 为构建产物不入库）。
- tools/export_static_site.py：锚点 EXPECT_MODES 3281 -> 3291、EXPECT_BY_FIGURE 318 -> 319（EXPECT_FIGURES 1027 不变）；
  实测 figures=1027 / modes=3291 / published=3231 / 隔离命中=0 / by-figure 分片=319
- tools/gen_web_site_counts.py：web/src/generated/siteCounts.ts = 3231 x 319（四态 published 949 / 1907 / 35 / 340）
- tools/apply_site_counts.py：dist 扫描 1374 文件零违规；docs 产品门面页 6 个零违规；PWA manifest（public + dist）与
  docs 门面文案收口 3231 x 319（web/public/manifest*.webmanifest、docs/index.md、docs/02-tools/figure_library.md）
- tools/build_daily_index.py：3231 条 / 319 位 / 分片 319
- tools/pages_preflight.py --stage data：全部断言通过
## 6. 并发与链式口径（重要）
- 时间线：本卡 09:25 --dry 预检 + 备份 -> 09:26~09:27 首轮写盘（随后按备份回滚）-> 09:28 重跑干净落盘（after sha 记录于 manifest）
  -> 09:32~09:34 门禁四连与站链五步 -> 09:38 兄弟卡 t_a7d233f0（沈复 H-SHF-001）落盘（+10 模式 / +1 code_map / +1 figure_name / 场景三件同步写入）
  -> 09:55 前后兄弟卡提交 5a657b81。
- 链式记录：兄弟卡 manifest 的 inputs == 本卡 after（本卡写入的三件）与 本卡 before（本卡零写的三件）；union_guard 记录 M-AZJ 10 -> 10 守恒；
  现行六件 sha == 兄弟卡 after（核验脚本复算一致）。
- 因此核验采用链式口径：本卡面以「内容判据」核验（本卡 10 条逐字在位且位于兄弟卡增量之前、前 3291 条与备份全等、注册面本卡条目逐字、其余条目零改动），
  现行 sha 以「末次写者 = 兄弟卡 after」核验；本卡写盘后自身增量面未被改写。
- 提交面说明：同一文件不可分提交——兄弟卡 5a657b81 吸收了本卡主库增量面（modes/code_maps/figure_names + 站链产物 + 锚点行），
  本卡提交补齐自己的审计 manifest / 备份 / 证据 / 报告 / 脚本面（前例：王阳明 QA 修复随章学诚提交入库，本卡以双记录留痕）。

## 7. 独立核验与证据
- verify_azj_merge_indep.py（本卡新增；直读文件与 git 实测，不采信合并卡自述；组内条数实测：A 25 / B 8 / C 7 / D 12 / E 7 / F 4 / G 11 / H 15 / I 3）：
  **92 PASS / 0 FAIL**（含四连门禁复算与站点链自洽复算；FAIL 时 exit 1）。
- 上游 verify_phase21r9_azj.py（合并后口径：G01 白名单并入主库注册面与合并卡足迹、G02 改为「主库占用面 == 合并后预期」、H01 改为链式口径）：
  复跑 **81 PASS / 0 FAIL**；原 landing 证据 docs/research/phase21r9_azj_verify_evidence.json 已恢复为提交版本（81/0，scope=landing；复跑须带 AZJ_EVID_OUT）。
- 证据：docs/research/phase21r9_azj_merge_evidence.json / .txt；docs/research/phase21r9_azj_verify_evidence_merged.json；
  data/audit/phase21r9_azj_merge_manifest.json（before/after/counts/backup/added/rules/inputs_after_write）；备份 ledger 可复算。

## 8. 复跑指引
- 独立核验：python3 verify_azj_merge_indep.py（约 5~8 分钟，含门禁与站点链复算；FAIL 时 exit 1）
- 上游核验：AZJ_EVID_OUT=/tmp/azj.json AZJ_SCOPE=merged python3 verify_phase21r9_azj.py（默认输出路径会覆盖 landing 证据，勿裸跑）
- 合并脚本（幂等，重跑只会 ABORT 不入库）：python3 tools/merge_azj_hazj001.py --dry
- 一致性工具：python3 tools/check_repo_parity.py --json（两仓构建图字节一致机检）

## 9. 附录（本卡产物与随链收敛）
- 本卡新增：data/audit/phase21r9_azj_merge_manifest.json、data/backup_merge_H-AZJ-001_20260924_092502/（六件 + ledger）、
  docs/research/phase21r9_azj_merge_report.md、phase21r9_azj_merge_evidence.json/.txt、phase21r9_azj_verify_evidence_merged.json、
  tools/merge_azj_hazj001.py、verify_azj_merge_indep.py；改写：verify_phase21r9_azj.py（合并后口径）。
- 主库与站链面（本卡写盘那一手）：data/modes_data.json、data/code_maps.json、data/figure_names.json、data/audit/findings.json、
  docs/architecture/static_data_manifest.json、web/src/generated/siteCounts.ts、web/public/manifest*.webmanifest、docs/index.md、
  docs/02-tools/figure_library.md、tools/export_static_site.py、tools/pages_preflight.py（上述已随兄弟卡 5a657b81 入库）。
- 镜像收敛（发布仓）：R9 AZJ 链 41 件（上游落盘包与数据件、sourcing 素材包与见证、landing 审计/证据/报告、本卡审计/证据/脚本）。

## 10. 回执补记（提交 / 镜像 / push）
（回执补记 2026-09-24）

- 工作仓提交：**a96302f1**（本卡审计 manifest / 备份目录 / 报告与证据三件 / tools/merge_azj_hazj001.py / verify_azj_merge_indep.py / verify_phase21r9_azj.py 合并后口径；主库增量面已随兄弟卡 5a657b81 入库）
- 提交后复跑：上游 verify_phase21r9_azj.py（合并后口径）**81 PASS / 0 FAIL**；独立 verify_azj_merge_indep.py **92 PASS / 0 FAIL**（含门禁四项与站链自洽复算）
- 发布仓镜像：**fe250fd**（45 件：AZJ 链随链收敛——上游 sourcing 素材与见证、落盘包与数据件、landing 审计与证据与生成器、本卡审计/证据/脚本），对齐工作仓 a96302f1
- push 回执：3b6874f..fe250fd  main -> main（git ls-remote origin main == fe250fddb388f401106718d08a697529998f444e，与本地 HEAD 复核一致）
- 两仓 parity：镜像前 63 条差异（本链 41 + 他链在制 22）-> 镜像后 22 条，全部为他链在制（W4/W6/W8/W10 与 shenfu sourcing、source-link 工具），**本链残留 0**
- 备份目录 data/backup_merge_H-AZJ-001_20260924_092502/：随本卡入库（六件 + ledger；与既有 data/backup_merge_H-CHE / H-HRD / H-ZDY 先例一致）；发布仓侧按 parity 排除规则驻留开发仓
- 复跑提示：verify_phase21r9_azj.py 默认输出会覆盖 landing 证据（已恢复为提交版本），复跑须带 AZJ_EVID_OUT


