# Phase21-R8 罗瑞卿重做链(3/5) - 主库合并报告: H-LUORQ-001(罗瑞卿)

- 原合并卡: t_08bbb73d(barbosa, 2026-09-24 00:21 done) | 本报告补产出卡: t_2d15bd2e(收尾补交, 2026-09-24) | 链位: 重做链 3/5(A1 落盘 -> A2 合并 -> A3 QA -> A4 归档)
- 上游: t_bf2d9b82(elcano) A1 落盘 commit 21edc5f8; 其收尾回执 8725ddff 明确「镜像与 push 归合并卡 t_08bbb73d」
- 先例: 王祥合并卡 t_8c521af7(d95a7b53 提交 -> 9c4ff9e 镜像 -> push 6e38c31..9c4ff9e -> 回执 68d6e0b0)
- 说明: 本报告系**收尾补交卡 t_2d15bd2e 依原始素材整理**(原合并卡未产出该文件; verify_phase21r8_luorq.py 白名单已引用本路径, 实测原缺). 素材仅取: merge manifest / merge_evidence.json/.txt / run.log / 提交-镜像-push 留痕. 禁改数, 禁美化.

## 1. 写入面与计数(六件; 模式/场景/标签纯追加, 顶层块按裁定替换)

| 文件 | before | after | 增量 |
|---|---|---|---|
| data/modes_data.json(顶层 entries) | 3281 | 3291 | +10(M-LUORQ-001~010, 逐字等于 A1 entries, 居文末) |
| data/code_maps.json(figures) | 213 | 214 | +1(H-LUORQ-001, 追加于文末) |
| data/scenarios_zh.json | 2193 | 2203 | +10(C-LUORQ-001~010) |
| data/scenarios_en.json | 2193 | 2203 | +10(C-LUORQ-001~010E) |
| data/scenario_tags.json | 7498 | 7518 | +20(每 mode zh+en 各一条, 先 zh 后 en) |
| data/figure_names.json | 1082 | 1083 | +1(H-LUORQ-001 -> 罗瑞卿) |

- 前后像 sha256(merge manifest inputs/after, raw 文件口径): modes_data 2d732efd... -> 2d3eb9ea...; code_maps 51ab0ef1... -> 53154b9d...; scenarios_zh 4491498c... -> 37b6c8f5...; scenarios_en 0bd5cd78... -> a7ce4a28...; scenario_tags fc562f92... -> b8311c08...; figure_names b226e3db... -> 69f531fd...
- 去重/发布口径(export_static_site 实测): 去重 3271->3281; 发布 3211->3221(= 去重 - 隔离 60); by-figure 分片 317->318; figures 1057 不变; 空模式码壳 10 条口径不变; 重复丢弃 0.
- 审计 manifest: data/audit/phase21r8_luorq_merge_manifest.json(前后像 sha256 + 规则 + 备份目录); data/audit/findings.json 随库刷新(modes_file_sha256=2d3eb9ea..., top_level_modes_entries 3281->3291, distinct_mode_codes 3271->3281, total_figures 323->324, 尾部补 data_sha256).
- 纪律核验(独立核验 C01/C03/D01/E01/F01/G01/G02): 纯追加语义通过; 不碰 _duplicates 归档件(K02 四件字节未变).

## 2. 顶层旧块处置全程(先冻结后替换)

- 位置: data/modes_data.json 顶层键 H-LUORQ-001; 船长裁定「先冻结后替换(byte 级备份 -> 以 B2 提案替换)」
- 前像: raw 文件 sha256 ffb905f68572682a...(23 键; name_zh=「罗瑞卿: 安全立军·整编革新·参谋统筹」)
- 后像: raw 文件 sha256 17326104d2f73922...(23 键; name_zh=「罗瑞卿: 公安创建·军警分途·警卫思想」)
- 剥离字段: proposal_note(提案过程字段, 含旧值对照; 不入库, 保持库内 23 键口径且禁字零残留)
- 备份目录: /opt/data/kanban/boards/protreptic/workspaces/t_08bbb73d/backup_merge_H-LUORQ-001_20260923_231321(10 件: 六件 before 全量 + top_block_old/new/proposal_original + backup_ledger.json; manifest 标 dir_is_temp=true)
- 其余键口径: 顶层除 H-LUORQ-001 外与旧块逐字全等(B09); total 标量零改写(B10, 3271 保持); 新块禁字零残留(B07); 硬伤 2/3 修正落实(B08)
- 本轮收尾复核: 备份目录实测存在, 10 件齐备, ledger sha 抽复一致; 按边界未迁移(见 §7 开放项 3)

## 3. 规则与结构口径(merge manifest.rules 摘要)

- 场景前缀: C-LUORQ-001~010 / C-LUORQ-001~010E(B2 scenario_notes new_prefix_suggestion: 旧码未在主库活跃, 可直接复用; 全库 0 碰撞)
- 场景 1:1 配对 M-LUORQ-001~010(code 序号 = mode 序号, H-ZX-001/H-HZX-002 先例); 8 字段结构; text=模板拼接(与 C-ZX/C-WX 生成规则逐条一致, 脚本可复算)
- scenario_tags 4 键(tag=模式中英名+_zh/_en); code_maps 3 键(mode_ids/tags/cross_references, xref 逐字取自图档, 0 悬空, 目标 H-XFZ-001/H-HZX-001 为历史在册件); figure_names 键级追加
- 旧场景处置仅作用于归档件(_duplicates 字节冻结未动)与历史报告; 主库 0 活跃残留(改写锚已随新模式/新场景落实)

## 4. 门禁与站点链结果

| 门禁 | 结果 |
|---|---|
| tools/credibility_gate.py --hard-fail | exit 0(新增硬失败 0) |
| tools/verify_findings.py --hard-fail | exit 0(存量冻结/新增 0; findings 随库刷新见 §1) |
| tools/apply_verification_status.py --check | exit 1: 9 条漂移(前链 M-WX, 非本链; 纪律不回填, --write 属全库重签=船长授权面) |
| tools/verify_source_links.py --hard-fail | exit 0(新增坏链 0) |

- 站点链条: 去重 3281 / 发布 3221 / by-figure 分片 318 / figures 1057 / 隔离 60(零泄漏); siteCounts.ts 3221x318 + 四态自洽; pages_preflight --stage data 全断言通过; 锚点 EXPECT_MODES 3271->3281, EXPECT_BY_FIGURE 317->318(tools/export_static_site.py, tools/pages_preflight.py, 注释含 t_08bbb73d)
- 四态(发布口径): 已核验 931 / 待核验 1916 / 存疑 34 / 一手材料 340; 源库口径 931/1948/51/351
- 附注(如实标注): docs/research/phase21r8_luorq_verify_evidence.json 现值 generated_at=2026-09-24 00:02:47, 为合并后口径复跑(verify_phase21r8_luorq.py)就地落盘; 与 _merged.json 内容一致(仅 generated_at 不同). 该次就地覆盖未见于 merge manifest/证据的正式登记, 原卡完成摘要亦未提及 -- 按「未登记覆盖」口径如实登记于此, 随本卡纳入提交, 供 QA(t_8773cb6b)复核.

## 5. 独立核验(verify_luorq_merge_indep.py): 83 PASS / 2 FAIL

- 分组(PASS): A 输入完整性 17 / B 顶层旧块处置 10 / C modes 8 / D scenarios 7 / E tags 5 / F code_maps 7 / G figure_names 3 / H 三面同体 4 / I 门禁复算 5 / J 站点链 7 / K 残留与归档 8 / L 上游回归 2
- FAIL 2 条(B02/B05, SHA 登记口径差, 非数据完整性问题):
  - B02「旧块 canonical sha == ledger + audit」: computed(json.dumps indent=2 canonical 口径)=4a40dcd76fae519b... vs ledger/manifest 登记(raw 文件口径)=ffb905f68572682a...
  - B05「新块 canonical sha == manifest.after + audit」: computed=a7dab5177718b5ba... vs 登记=17326104d2f73922...
  - 本轮收尾复核(只读复算): raw 文件 sha 与登记值逐件相符(ffb905f6... / 17326104...); 主库现行顶层块逐字等于新块冻结值(canonical 复算 a7dab517... 与 B05 computed 一致). 按卡裁定: 不改 audit/manifest/ledger 登记, 留 QA t_8773cb6b 裁定.
  - 留痕附注: verify_luorq_merge_indep.py 工作树现值(mtime 2026-09-24 00:17)已将 B02/B05 判据改为「raw 文件 sha 直比」; 证据文件保持首跑(00:02:47)83/2 原样, 未复跑(避免覆盖初跑留痕). 以工作树现值纳入提交.
- 上游回归 L01: verify_phase21r8_luorq.py(合并后口径) 0 FAIL(69 PASS/0 FAIL); L02 原判据(「未被覆盖」)实际仅断言文件非空, 属判据弱点 -- 见 §4 附注.
- 证据: docs/research/phase21r8_luorq_merge_evidence.json / .txt; docs/qa/phase21r8_luorq_merge_verify_evidence/run.log

## 6. 提交 / 镜像 / push 回执(本卡补记)

- 工作仓提交: **0cbf6ab6**(21 路径, 卡 t_2d15bd2e 收尾补交; 父 dc9fe529; 白名单逐件 add, 名单外 0; 数据内容零改动)
- 发布仓镜像: **ec0a06bf**(39 路径: 白名单 21 件 + A1 落盘包 18 件随链收敛; 逐件 cp 后 sha256 全量比对 39/39; 对应工作仓 0cbf6ab6)
- push 回执: dab8213..ec0a06b  main -> main(ls-remote origin main == ec0a06bfadd455aec01920c9e0412e744d81eed2 复核一致)
- 工作仓 push: **不适用**(开发仓 master 非 push 目标: 远端仅 main; dry-run 显示 new branch = 全量历史上传; master 历史含 440.19MB blob(461572032 B) 触发服务端 pre-receive 拒绝, 既有事实见 phase45_acceptance.md / link_coverage.md §10.1) -- 未执行, 如实登记
- parity(镜像1 后实测, tools/check_repo_parity.py --json): 313 条差异(6 内容差 + 307 仅工作仓), 全部属他链在制(W5/W4/王祥 QA t_b92cc1cf/QA t_8773cb6b/王祥归档/王崇 scratch); **本卡覆盖 39 件 0 残留**
- 回执补记: docs/research/phase21r8_luorq_merge_evidence.json/.txt(two_repo 块/行); 完成报告 docs/qa/phase21r8_luorq_receipt_report.md; 二次提交/镜像/推送回执见卡回执 metadata(文件自指限制)

## 7. 开放项 / 待裁定

1. B02/B05 canonical vs raw 口径差: QA t_8773cb6b 裁定; audit/manifest/ledger 登记未改(本轮不动数).
2. verifstatus 9 条漂移(前链 M-WX): 维持 pending 至授权/核验卡裁定.
3. 备份目录 dir_is_temp=true(卡工作区): 存在随卡工作区清理风险, 本轮未迁移; 如需长期留档, 可由后续卡按 data/backup_merge_H-LUORQ-001_* 惯例收档(该模式在 parity 中属排除口径).
4. verify_evidence.json 就地覆盖未登记(§4 附注): 本轮如实标注并纳入提交, 供 QA 复核.
5. 旧场景处置与历史报告留痕: _duplicates 字节冻结未动; 主库 0 活跃.
