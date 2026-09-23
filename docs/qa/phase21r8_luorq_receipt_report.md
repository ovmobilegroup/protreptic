# Phase21-R8 罗瑞卿链收尾补交卡 t_2d15bd2e 完成报告(提交 / 镜像 / push / 回执)

- 卡: t_2d15bd2e(barbosa, 2026-09-24) - 「[Phase21-R8 罗瑞卿链收尾] 合并卡 t_08bbb73d 遗漏项补交: 选择性提交 + 合并报告 + 发布仓镜像 + push(零数据改动)」
- 上游: t_08bbb73d(原合并卡, done 2026-09-24 00:21, 工作树已合并未提交) <- t_bf2d9b82(A1 落盘 21edc5f8 / 收尾回执 8725ddff)
- 下游: QA t_8773cb6b(在途独立核验) -> 文档 t_d9cb98bb(登记链依赖本卡回执)
- 生成: 2026-09-24 (CST) | 边界: 零数据改动, 不重做合并, 不碰他链在途文件

## 1. 工作仓选择性提交

- 提交: **0cbf6ab63059353ab9e7f2f5d9b9d76423b6c1c1**(父 dc9fe52942e8ece57c38519763b3061176288237)
- 21 路径; 白名单逐件 git add 后 `git diff --cached --name-only` 与白名单完全一致(名单外 0, 缺失 0)
- run.log 被 .gitignore `*.log` 命中, 按白名单以 `git add -f` 纳入
- 数据内容零改动: 六件 sha256 与 merge manifest after 逐件一致(下表前六行为主库数据六件)

| 路径 | sha256 |
|---|---|
| `data/modes_data.json` | `2d3eb9eaf41bc95e7870bae98ced5eeee46ff216272d6dfa444c5441c0a6a964` |
| `data/code_maps.json` | `53154b9ddd5e2e3f4ae0bbde746d4ce6ffc41c4f7bd91ce7c9fa047ae4999d83` |
| `data/scenarios_zh.json` | `37b6c8f50746a64fb0e6e4663f6fba8cad5c97c0466b9aededb9af1f07de9baf` |
| `data/scenarios_en.json` | `a7ce4a28128febca94747279f79386b5bd6493b684f24ffa38f6d1e3b3ff4a1f` |
| `data/scenario_tags.json` | `b8311c084a21f5c6d6f2099aab5df84e3010c54c321a59b445491690771f34b3` |
| `data/figure_names.json` | `69f531fd0153fd3b762ca9641657121552a792ae420d6ba98016b209a7ddf3fd` |
| `data/audit/findings.json` | `26d166ab8b77c925106213a00e676f7be0e42bb0fd6d71beb8af44a80904341a` |
| `data/audit/phase21r8_luorq_merge_manifest.json` | `df7b35291a671a6deb8034be903dc0cfecfe93487571574323d3edabdfbcff55` |
| `data/audit/phase21r8_luorq_top_block_backup.json` | `8b9d41c4ec4cedb00850ed6d358f5459f14f660dbc05d29009cdfeffd5d2b6d8` |
| `docs/architecture/static_data_manifest.json` | `7afc3e46ffcfbefe6e150d88a45c29ea9c63a2094764981f1d8da989f33dc4ba` |
| `web/src/generated/siteCounts.ts` | `a5a47d3f2121515a091addab204827d8190aab0aab8b8ef0e2893a92bcbada90` |
| `tools/export_static_site.py` | `0166d06402ccb7c5ae7f7e587827c99450f5e004d4b1357b6da78ce92699bd0c` |
| `tools/pages_preflight.py` | `440fb33a0846bd951d5085cbb93024e7d49ff974534f461bb55f2760c5a36312` |
| `verify_phase21r8_luorq.py` | `5254fc2bcb71b8279fe9a797563358dd21c7deb3609332b860ecb2eabe9fc17d` |
| `verify_luorq_merge_indep.py` | `8c6e984a9d30d300fd76bbfa7bce1ec8788f1593395685db8d819966ed658c38` |
| `docs/research/phase21r8_luorq_merge_evidence.json` | `36a5a88b5a99defd795d0972d37ebdaf93ea5ce2f9523d3d926e0a221eca3fbf` |
| `docs/research/phase21r8_luorq_merge_evidence.txt` | `47230f1be0d5918f84bd84ba022f78996b0f9f41e89bf4890974b0eed97856be` |
| `docs/research/phase21r8_luorq_verify_evidence.json` | `41c6138d61f39667f98b4b8e52e4eff95a2aa6c26d4cfe05e22ce39335c61846` |
| `docs/research/phase21r8_luorq_verify_evidence_merged.json` | `a4c86729c5209a3341458278abddc293edba7b9ea011fc4941e6b37d573981e4` |
| `docs/qa/phase21r8_luorq_merge_verify_evidence/run.log` | `b3093d9116f12311a3e62e490f18dfbaa5db6a94c8b261066f82dc500b8bce91` |
| `docs/research/phase21r8_luorq_merge_report.md` | `4720d0a9b14181bcd11e97cf6efe8c07a77c3367e6d80c01e4be00f78cef5ad6` |

提交后 git status --short: 他链在途文件维持未提交(未作处理)。

## 2. 发布仓镜像

- 提交: **ec0a06bfadd455aec01920c9e0412e744d81eed2**(父 dab8213d5bfd8834c8cc380534ac80541acfd777)
- 39 路径 = 白名单 21 件 + A1 落盘包 18 件随链收敛(figures / individuals / landing 冻结副本 / 证据报告 / gate)
- 逐件 cp 后 sha256 全量比对: **39/39 byte-same**(无抽查, 全量)

| 路径 | sha256 |
|---|---|
| `data/audit/findings.json` | `26d166ab8b77c925106213a00e676f7be0e42bb0fd6d71beb8af44a80904341a` |
| `data/audit/phase21r8_luorq_landing_manifest.json` | `dca1d33ca1ace6310a907be74c4ee481d08f4b27e87a6ef9a79ec6bc822f3aa9` |
| `data/audit/phase21r8_luorq_merge_manifest.json` | `df7b35291a671a6deb8034be903dc0cfecfe93487571574323d3edabdfbcff55` |
| `data/audit/phase21r8_luorq_top_block_backup.json` | `8b9d41c4ec4cedb00850ed6d358f5459f14f660dbc05d29009cdfeffd5d2b6d8` |
| `data/code_maps.json` | `53154b9ddd5e2e3f4ae0bbde746d4ce6ffc41c4f7bd91ce7c9fa047ae4999d83` |
| `data/figure_names.json` | `69f531fd0153fd3b762ca9641657121552a792ae420d6ba98016b209a7ddf3fd` |
| `data/figures/H-LUORQ-001.json` | `d609b968a8d324eacb2a52ae6f9b03cba512d644ef6c4ae4ab167961b5056640` |
| `data/individuals/H-LUORQ-001.json` | `91efb1b79a672bef9196d04e926c8ee3c2f9154b895e84f74534165f85d9c73f` |
| `data/individuals/H-LUORQ-001_modes.json` | `a75decd03f71d7447c9a220d06b6a71fa379942200615b176cb01e17b68f3e8f` |
| `data/modes_data.json` | `2d3eb9eaf41bc95e7870bae98ced5eeee46ff216272d6dfa444c5441c0a6a964` |
| `data/scenario_tags.json` | `b8311c084a21f5c6d6f2099aab5df84e3010c54c321a59b445491690771f34b3` |
| `data/scenarios_en.json` | `a7ce4a28128febca94747279f79386b5bd6493b684f24ffa38f6d1e3b3ff4a1f` |
| `data/scenarios_zh.json` | `37b6c8f50746a64fb0e6e4663f6fba8cad5c97c0466b9aededb9af1f07de9baf` |
| `docs/architecture/static_data_manifest.json` | `7afc3e46ffcfbefe6e150d88a45c29ea9c63a2094764981f1d8da989f33dc4ba` |
| `docs/qa/phase21r8_luorq_merge_verify_evidence/run.log` | `b3093d9116f12311a3e62e490f18dfbaa5db6a94c8b261066f82dc500b8bce91` |
| `docs/research/phase21r8_luorq_gate.txt` | `10fea1ffe293d962829a2f646f3f4929b55c4cb578f91fd1289920eb5d34477b` |
| `docs/research/phase21r8_luorq_landing_evidence.json` | `dca1d33ca1ace6310a907be74c4ee481d08f4b27e87a6ef9a79ec6bc822f3aa9` |
| `docs/research/phase21r8_luorq_merge_evidence.json` | `36a5a88b5a99defd795d0972d37ebdaf93ea5ce2f9523d3d926e0a221eca3fbf` |
| `docs/research/phase21r8_luorq_merge_evidence.txt` | `47230f1be0d5918f84bd84ba022f78996b0f9f41e89bf4890974b0eed97856be` |
| `docs/research/phase21r8_luorq_merge_report.md` | `4720d0a9b14181bcd11e97cf6efe8c07a77c3367e6d80c01e4be00f78cef5ad6` |
| `docs/research/phase21r8_luorq_rebuild_report.md` | `7937f27283c0a8db2e91090f2d73f33566208a6b88f35e06990b7f19848e71a4` |
| `docs/research/phase21r8_luorq_sourcing_report.json` | `76eef98da508915d39105de043d4a74383eb310e84900b3b4a38d052a66260cb` |
| `docs/research/phase21r8_luorq_sourcing_report.md` | `c74b53044a331ff736cdc692f5b6f8051ffda1b611e8e92d1ab43665212b0016` |
| `docs/research/phase21r8_luorq_verify_evidence.json` | `41c6138d61f39667f98b4b8e52e4eff95a2aa6c26d4cfe05e22ce39335c61846` |
| `docs/research/phase21r8_luorq_verify_evidence_merged.json` | `a4c86729c5209a3341458278abddc293edba7b9ea011fc4941e6b37d573981e4` |
| `docs/scratch/legacy20_r8_luorq_landing/category_mapping.tsv` | `582085e67f3794988e56eb7689df5f00b2e6fcfe90e8890227034c4fd5e337d2` |
| `docs/scratch/legacy20_r8_luorq_landing/combined_library_entries.json` | `4b3498e3a6362e03a12e64a93516032bdeaf2d5866d585535d6a0bb56d3ad4c8` |
| `docs/scratch/legacy20_r8_luorq_landing/figures/H-LUORQ-001.json` | `d609b968a8d324eacb2a52ae6f9b03cba512d644ef6c4ae4ab167961b5056640` |
| `docs/scratch/legacy20_r8_luorq_landing/id_mapping.tsv` | `81e145a2683517a96202cdc4ce28f66d7817d4eb7f15896f2f8954584aa806cc` |
| `docs/scratch/legacy20_r8_luorq_landing/individuals/H-LUORQ-001.json` | `91efb1b79a672bef9196d04e926c8ee3c2f9154b895e84f74534165f85d9c73f` |
| `docs/scratch/legacy20_r8_luorq_landing/individuals/H-LUORQ-001_modes.json` | `a75decd03f71d7447c9a220d06b6a71fa379942200615b176cb01e17b68f3e8f` |
| `docs/scratch/legacy20_r8_luorq_landing/modes_library_entries.json` | `c960b0716397cfa9eb23c55affc76ee3f42578262f6f82a4b006a3321acf337f` |
| `docs/scratch/legacy20_r8_luorq_landing/scenario_notes.json` | `370abdb329f2b9e453778d8640144049729487a7c662a1b05dfd094a3081c92b` |
| `docs/scratch/legacy20_r8_luorq_landing/top_block_proposal.json` | `dd43241369ddc7a431e160aa644a11a1ea970fc4ece433fa23e29ee7f84ac2f9` |
| `tools/export_static_site.py` | `0166d06402ccb7c5ae7f7e587827c99450f5e004d4b1357b6da78ce92699bd0c` |
| `tools/pages_preflight.py` | `440fb33a0846bd951d5085cbb93024e7d49ff974534f461bb55f2760c5a36312` |
| `verify_luorq_merge_indep.py` | `8c6e984a9d30d300fd76bbfa7bce1ec8788f1593395685db8d819966ed658c38` |
| `verify_phase21r8_luorq.py` | `5254fc2bcb71b8279fe9a797563358dd21c7deb3609332b860ecb2eabe9fc17d` |
| `web/src/generated/siteCounts.ts` | `a5a47d3f2121515a091addab204827d8190aab0aab8b8ef0e2893a92bcbada90` |

## 3. push 回执

| 仓 | 结果 |
|---|---|
| 发布仓 main | `dab8213..ec0a06b  main -> main`(已 push; `git ls-remote origin main` == ec0a06bfadd455aec01920c9e0412e744d81eed2 复核一致) |
| 工作仓 master | **不适用**(未执行, 如实登记) |

工作仓 push 证据(环境事实, 非本卡过错):

1. `git ls-remote origin` 仅 1 条: `refs/heads/main`(远端无 master);
2. `git push origin master --dry-run` -> `* [new branch] master -> master`(远端无该分支 = 全量历史上传);
3. master 历史含 **440.19MB** blob(`1ff8dcb9:api/triton/_C/libtriton.so` = 461572032 B) -> GitHub 100MB 上限 pre-receive 拒绝(phase45_acceptance.md 双仓同步节实测原文在案);
4. docs/qa/link_coverage.md §10.1: 开发仓 master 不是 push 目标; 全量上传 15 分钟未完成(无 pack 落盘), 已放弃该路径; 发布路径为发布仓 main.

## 4. parity 复核(tools/check_repo_parity.py --json; 镜像1 后实测 2026-09-24 01:07 CST)

- 计数: both_sides 1880 / identical 1874 / only_workspace 307 / only_publish 0; 差异合计 **313**
- 6 条 CONTENT_DIFF: `data/audit/source_texts.json`, `data/source_links.json`, `tools/credibility_gate.py`, `tools/fetch_source_texts.py`, `tools/source_text_cache.py`, `tools/test_credibility_d45.py`(全部 = W5 t_f09365bb 在制)
- 307 条 MISSING_IN_PUBLISH: docs/scratch/phase21w5_wangchong 271 / docs/qa 25 / docs/research 8 / data/audit/source_texts 2 / docs/figures/H-HZX-002.md 1
- **本卡覆盖 39 件在 parity 中 0 差异**; 与 luorq 相关者仅 QA t_8773cb6b 在制 6 件(docs/qa/phase21r8_luorq_qa_*)
- 结论: 313 条全部为他链在制/未镜像(W5/W4/王祥 QA t_b92cc1cf/QA t_8773cb6b/王祥归档/王崇 scratch) -> 「整体差异不为本卡新增」成立

## 5. 门禁复跑(工作仓; 2026-09-24 01:09 CST)

| 门禁 | 结果 |
|---|---|
| `tools/credibility_gate.py --hard-fail` | exit 0(新增硬失败 0) |
| `tools/verify_findings.py --hard-fail` | exit 0(存量冻结/新增 0; 非阻断警告: summary.total 计数过期 164 vs 143、M-ASM-001~010 双收割, 均非本卡) |
| `tools/apply_verification_status.py --check` | exit 1: 19 条漂移(示例 M-WC-001~005; 无 M-LUORQ 命中); --write 属全库重签 = 船长授权面 |
| `tools/verify_source_links.py --hard-fail` | exit 0(新增坏链 0; 3 条 UNREACHABLE 警告非阻断) |

## 6. 二次提交(回执补记)与镜像

- 二次提交内容(4 件): `docs/research/phase21r8_luorq_merge_evidence.json` / `.txt`(two_repo 块/行) + `docs/research/phase21r8_luorq_merge_report.md`(§6 回执) + 本报告
- 二次提交 sha / 发布仓镜像 sha / push 回执: 见卡回执 metadata(文件自指限制: 本报告不收录自身提交的 sha)

## 7. 开放项 / 待裁定

1. B02/B05 canonical vs raw 口径差: QA t_8773cb6b 裁定; audit/manifest/ledger 登记未改。
2. verifstatus 19 条漂移(M-WC/M-WX 等他链): 维持 pending, 回填属授权面。
3. 备份目录 dir_is_temp=true(卡工作区)存在随卡清理风险, 未迁移; 如需长期留档按 data/backup_merge_H-LUORQ-001_* 惯例收档。
4. verify_evidence.json 就地覆盖未登记: 已如实标注(合并报告 §4 附注)。
5. 工作仓 master push 属环境事实(非 push 目标), 如需变更远端分支策略 = 船长裁定面。

## 附: 相关证据路径

- 合并报告: docs/research/phase21r8_luorq_merge_report.md | 合并证据: docs/research/phase21r8_luorq_merge_evidence.json/.txt
- 独立核验证据/日志: docs/research/phase21r8_luorq_verify_evidence_merged.json; docs/qa/phase21r8_luorq_merge_verify_evidence/run.log
- 审计: data/audit/phase21r8_luorq_merge_manifest.json; data/audit/phase21r8_luorq_top_block_backup.json
- 本轮 scratch(barbosa cache): mirror_sha.json / precommit_sha256.txt / parity_run1.json / gate_*.txt(非交付物)
