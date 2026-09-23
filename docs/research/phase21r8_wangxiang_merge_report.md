# Phase21-R8 王祥重做链(2/4) · 主库合并报告 —— H-HZX-002(王祥)

- 卡：t_8c521af7(barbosa) | 日期：2026-09-23 | 链位：重做链 2/4(A1 落盘 -> A2 合并 -> A3 QA -> A4 归档)
- 上游：t_5c183962(elcano) commit 1fe4c451, 18 路径；独立核验 58 PASS/0 FAIL；主库零写入
- 先例：曾子 t_16ebe5c9(da4b240e) / R6 t_10089b19 / R6B t_f3aabe2c

## 1. 写入面与计数(六件, 全部纯追加)

| 文件 | before | after | 增量 |
|---|---|---|---|
| data/modes_data.json | 3271 | 3281 | +10(M-WX-001~010, 逐字等于 A1 entries) |
| data/code_maps.json(figures) | 212 | 213 | +1(H-HZX-002, 追加于文末) |
| data/scenarios_zh.json | 2183 | 2193 | +10(C-WX-001~010) |
| data/scenarios_en.json | 2183 | 2193 | +10(C-WX-001~010E) |
| data/scenario_tags.json | 7478 | 7498 | +20(每 mode zh+en 各一条) |
| data/figure_names.json | 1081 | 1082 | +1(H-HZX-002 -> 王祥) |

- 审计 manifest：data/audit/phase21r8_wangxiang_merge_manifest.json(before/after sha256 与规则与备份目录)
- 备份：本卡工作区 backup_merge_H-HZX-002_20260923_212150(六件 before 全量)
- 纪律核验：纯追加零删改(旧对象逐对象全等), 不碰 _duplicates 归档件, 不碰他人条目(与他人共享文件基于最新版本增改)
- 说明：初版合并脚本 after 记录段有一处字典字面量求值 bug, 已按备份整件回滚后重跑(干净单次写盘); 回滚-重跑过程留痕于卡会话。

## 2. 场景前缀裁定：C-WX-001~010 / C-WX-001~010E

A1 交接要求「C-HZX-001~010 已被 H-HZX-001(黄宗羲)占用, 须另定前缀」。裁定取 **C-WX**：

1. 现代口径为「模式前缀配对」：Phase20/21 新增的 90 组场景码均与模式前缀一一配对(M-ZX 对 C-ZX 等, H-ZX-001 先例), C-WX 对 M-WX 直接配对;
2. 图派生路线被封死：HZX 短码被黄宗羲占用, 若按 figure 派生只能造 HZX2 变体, 全库无先例;
3. 全库碰撞 0(data, docs, tools, web 全扫; C-WX, C-HZX2, C-WX2 均为 0);
4. 附注(供 QA/船长复核)：docs/qa/phase21r4_*.md 里的「王选 H-WX-001」字样不构成占用——H-WX-001 非本库人物码(仅文档语境), 且场景码空间与人物码空间独立; 若后续确有 H-WX-001 人物登记, 场景 C-WX 与其不冲突。

## 3. 结构口径(各按先例)

- scenarios：8 键 {code, mode_code, title_zh, title_en, text_zh, text_en, application_area_zh, application_area_en}(H-ZX-001 同构);
  title=模式名; application_area=模式 modern_applications_*; **text=模板拼接**(zh：模式名 + 的当代应用场景： + 中文应用以「；」连接 + 。; en：Contemporary applications of + 名 + : + 英文应用以「; 」连接 + .), 与 C-ZX-001~010 生成规则逐条一致(脚本内可复算)。
- scenario_tags: 4 键 {mode_code, tag, figure_code, language}; tag=模式中英名+_zh/_en; 每 mode 先 zh 后 en.
- code_maps: 3 键 {mode_ids(10), tags(10 中文模式名), cross_references(逐字取自图档, 目标 H-ZX-001 在册, 0 悬空)}.
- figure_names: 键级回填(R6B removed_registrations_r6b.json 留档 H-HZX-002 -> 王祥).
- modes_data.total 标量本卡零改写(3271 保持; 口径对齐属收尾卡先例); top-level figure 块不外扩(R6/曾子先例).

## 4. 核验状态纪律(卡任务 (4))与 verifstatus 门禁的登记

- 10 条新条目 **verification 全 pending**(与 A1 落盘逐字一致, 三面同体); 本卡**不回填**.
- tools/apply_verification_status.py --check 因此报 **9 条漂移**(exit 1): 机械规则对 M-WX-001~010 除 003 判 verified/link-resolved, 因出处《晋书》在 source_links.json 已登记(wikisource 可链接); M-WX-003(《孝经》)未登记, pending 与规则一致.
- 未跑 --write 的理由: (1) 本卡纪律明文不回填; (2) --write 属**全库重签**(3281 条 verification 块包含他人条目 checked_at/checker 一并改写) 与公开侧四态计数变化, 按 phase21r2/phase21R 先例属**船长授权面**("任何线上可见变化先列清单").
- 影响面: 站点四态发布口径 已核验 931 / 待核验 1906 / 存疑 34 / 一手材料 340(王祥 10 条计入待核验); 若授权回填则为 940/1897/34/340.
- 一行修复(待授权): python3 tools/apply_verification_status.py --write, 随后重跑站点链条五步.

## 5. 门禁四连(复算)

| 门禁 | 结果 |
|---|---|
| tools/credibility_gate.py --hard-fail | exit 0(新增硬失败 0; D4 10 条 unchecked / D5 0 如实记账) |
| tools/verify_findings.py --hard-fail | exit 0(findings.json 先经 build_audit_findings.py --write 随库刷新 sha, total 164 不变) |
| tools/apply_verification_status.py --check | exit 1: 9 条漂移(上文第 4 节登记, 纪律 (4) 所致) |
| tools/verify_source_links.py --hard-fail | exit 0(387 链接核验 3m23s, 新增坏链 0) |

## 6. 站点链条五步与锚点(EXPECT 口径以实测为准)

1. tools/export_static_site.py: 去重 3271 / 发布 3211 / by-figure 分片 317 / figures 1057 / 隔离 60(零泄漏)
2. tools/gen_web_site_counts.py: siteCounts.ts = 3211 x 317; 四态 931/1906/34/340
3. tools/apply_site_counts.py: dist/manifest 收口; 扫描 1367 文件零违规
4. tools/build_daily_index.py: 3211 条 / 317 位 / 317 分片
5. tools/pages_preflight.py --stage data: 全部断言通过(figures=1057 modes=3271 published=3211 隔离命中=0)
- 锚点更新: EXPECT_MODES 3261 -> 3271, EXPECT_BY_FIGURE 316 -> 317(tools/export_static_site.py, tools/pages_preflight.py 各一处与注释块); EXPECT_FIGURES 1057 不变.

## 7. 独立核验(verify_wx_merge_indep.py)

- 结果: **66 PASS / 0 FAIL**(A 输入完整性 10 / B modes 10 / C scenarios 10 / D tags 6 / E code_maps 7 / F figure_names 3 / G 三面同体 3 / H 门禁复算 7 / I 站点链 7 / J 上游回归 2)
- 上游回归: verify_phase21r8_wangxiang.py 按**合并后口径**更新 3 处(E 组"非预期占用"白名单并入主库六件与锚点工具与站点构建产物面与本卡核验脚本; F 组改为"主库占用面 == 合并后预期"; 合并态证据另写 _merged.json), 复跑 **59 PASS / 0 FAIL**; A1 原证据文件保持 commit 1fe4c451 版本(sha 复核一致, 首次过渡态覆盖已按 git 恢复).
- 证据: docs/research/phase21r8_wangxiang_merge_evidence.json / .txt; docs/research/phase21r8_wangxiang_verify_evidence_merged.json

## 8. 两仓 parity / 镜像 / push

- 工作仓提交: **见第 9 节补记**
- 发布仓镜像与 push: **见第 9 节补记**

## 9. 收尾回执 v2(补记)

(本卡第二提交在此补记: 工作仓/发布仓 commit, push 回执, 镜像后 parity 结果, 交付清单.)

## 10. 待裁定 / 开放项

1. 第 4 节的 9 条 verifstatus 漂移: 授权回填(--write)或维持 pending 至核验卡裁定.
2. figure 层 A1 遗留待核项(卒年异说 / wiki_id / 别名残留)按 A1 边界由后续卡处置, 本卡未动.
3. 场景前缀 C-WX 已按先例裁定并落地, 如船长另有口径, 改前缀为 20 键重命名(成本低, 可逆).
