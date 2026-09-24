# Phase21-W9-F 修复报告 - web/public/data 索引面 + 名称回填链 (卡 t_d7faccc5)

- 日期: 2026-09-24
- 角色: elcano (W9 F 类修复卡)
- 输入链: 8adbdabd (W4 勘定锚) -> e5ddd13f (被审执行链提交) -> 6f298ca1 (本卡开工基线)
- 关联卡: t_d7faccc5 (本卡), t_9ed2866a (QA 卡, 父 ee08f5b5), t_28a29244 (F 类回填卡)
- 结论: F 类残余两处 (浏览器面 514 空名, web/public/data 1359 件被误纳入 git 索引) 均已修复. 504 条真名回填到 DB, figures.index.json, 分片, 统一名录四面; 重建不回落; 五闸 rc=0; 残留 ten (待核名) 与 104 (占位待补名) 已登记在案. 零臆造来源.

## 一, 问题域与对账口径

1. W4 勘定 (8adbdabd) 与现值对账:
   - 勘定时点: figures 1056 行 / 空名 563 (H 类 16 + 非 H 547); 非 H 且有 legacy 名者 537.
   - 现值 (修复前): figures 1027 行 / 空名 514 = 504 (可回填) + 10 (无来源).
   - 33 差归因: 31 行移除 (RW-KAG-1..27 + JP-Sas-001 / MY-Mah-001 / SG-Lee-001 / UZ-Ulu-001) + 2 行已命名 (RW-KAG-001, SG-LEE-001).
   - 行漂移: 1056 -> 1027 = -31 移除 +2 新增 (JP-SAS-001, UZ-ULU-001 规范码).
2. 514 分解: 504 = 可回填 (scenarios_zh/en 的 legacy 名在); 其中 400 真名 + 104 legacy name==code (占位行); 10 = 无来源 (scenarios 条目无任何名字键, 不得臆造).
3. 根因 (键漂移): tools/build_figures_db.py 与 api/load_data.py 只读 scenarios 的 `name` 键, 而 legacy 批次 (tools/json 中 504 条) 存的是 `name_zh` / `name_en`; 重建时读空 -> 名字回落为空串.

## 二, 修复实现

1. `tools/build_figures_db.py`: INSERT 前双读回退 `name -> name_zh` (en: `name -> name_en`). sha16: 223c572960556dd9 -> 4eace91290adec2d
2. `api/load_data.py`: 同类装载器键接驳 (防再生). sha16: eb6e88ca5a90438f -> 9dcc83b27bfd5f56
3. `tools/export_static_site.py`: figures.index.json gzip 预算重锚 50KB -> 80KB (回填后实测 gzip 65571B; 名字空值口径 34796B; 余量约 20%). sha16: 0d860d5e79328943 -> f069fe822724736e
4. 备份: api/protreptic.db.backup_phase21w9fix_20260924_172526 (sha256 c4a89a23..., 与修复前主库等同).
5. 执行序: 备份 -> 干跑 (副本) -> 主库重建 x2 -> 站链 -> 门禁/parity -> 清单随提交.

## 三, 干跑 (副本) 与主库执行

- 干跑 (scratch/db_dry.sqlite): build x2 幂等 (行全等 true); 1017/10; changed_rows=504 == restorable; 变更列仅 name_zh/name_en; 名字与 legacy 逐条全等 (0 mismatch); 104 行仍 name==code.
- 主库: build x2 (rc=0/0); 两次均 1017/10; db sha16 90227b16 (run1) -> d7d5a228 (run2, 与干跑后一致).
- 终态副本复跑 (verify_state): rows 全等 true; 1017/10 -- 重建不回落 (RNBW).

## 四, 站链复跑 (8 步全绿)

export_static_site rc=0 (1357 件) -> gen_web_site_counts rc=0 -> build_daily_index rc=0 -> pages_preflight --stage data rc=0 (figures=1027 modes=3301 published=3241 隔离命中=0; daily 3241) -> build_search_index rc=0 -> build_graph_data rc=0 -> build_unified_index rc=0 (counts: total 1344 / figures 320 / scenarios 1024 / with_modes 1308) -> ci_data_check rc=0 (24/24 PASS).

## 五, 三面核验 (回填到达面)

- DB: 1027 / named 1017 / empty 10 (==ten)
- figures.index.json: 1027 条 / 非 H 空 10 (==ten) / 与 legacy 0 mismatch / sha256 3c99c19a...
- 分片 figures/*.json: 1027 件 / 0 mismatch / 0 missing
- index.unified.json: 名字 0 mismatch; counts 同前
- 样张 AE-FED-001: DB, 分片, 统一名录均含真名 (阿拉伯联合酋长国..., 与 legacy 全等)

## 六, web/public/data 索引面处置 (登记节, 按指示新增)

- T0 (e5ddd13f 内扫入): git ls-files 1359 == 盘上 1359; 逐件 sha256 清单落档 data/audit/phase21w9_web_public_data_index_before.txt (1359 行, sha256 b123f3f0...).
- 处置: git update-index --force-remove --stdin (仅索引面; bulk cached-removal 变体在本环境返 -1).
- T1: ls-files 1359 -> 0; 盘上 1385 件 (新增 26 = daily 2 + search 17 + graph 7, 均为站链产物); T0 清单全部仍在盘上 (0 缺失).
- 影响面: 站点/gate 只依赖盘上产物 (web/public/data 为准), 索引面处置对构建与运行时零影响.

## 七, 门禁与 parity

- 五闸 (终态): credibility_gate rc=0; verify_source_links rc=0; verify_findings rc=0; apply_verification_status --check rc=0 (四态一致); ci_data_check rc=0.
- 站链外补跑 (回填后路由名字陈旧 400 条, 先红后修): cp public->dist/data; prerender_routes rc=0 (1360 路由); build_sitemap rc=0 (1361 条). 效果: web_p0_routes.json 名字刷新 (name==code 由 514 -> 114 = 104 占位 + 10 待核名); siteCounts.ts 刷新 (verified 1019 / suspect 37; citations 4504 等).
- parity (修复后, 镜像前): DIFF 6 件 (内容差: build_figures_db / export_static_site / manifest / routes / siteCounts; 单侧: before 清单). api/protreptic.db 与 api/load_data.py 不在边界, 符合角色排除.
- 镜像 + push 后复跑 parity 应为 0 -- 见 v2 回执.

## 八, 背景归因 (勿回滚)

e5ddd13f 内扫入的 W7 删除面 (RW-KAG-1..27 legacy 清理等 31 项) 为本卡勘定差的组成部分 (537 -> 504 的 33 差中的 31): 按背景登记处理, 不回滚, 不重做 W7.

## 九, 边界与遗留

- 边界 (未动): H-* 16 件 (另治); W7 删除面; 非本卡 W8/合并面; api/protreptic.db 内容仅名字面变化.
- 遗留:
  1. ten = 待核名 (BW-KHA-001, BW-MAS-001, LS-MOS-001, MG-RAV-001, NA-GEO-001, NA-NUJ-001, SZ-MSW-001, ZA-ZUM-001, ZW-CHA-001, ZW-MUG-001) -- 候选线索未采纳 (data/phase_17_7_southern_africa_modes.json 草稿名等), 待裁定.
  2. 104 占位待补名 (registry.code_as_name) -- 回填后显示仍为代码 (无视觉变化).
  3. E1/F11 口径差: QA 校验器面向缺陷态的断言 (非 H 空名==0 / figures 聚合 hash) 在合法修复后必然翻转; 供 t_28a29244 裁定.
  4. 隔离面 (quarantined / H) 未纳入本卡.
  5. F12 口径: pb 无 e5ddd13f 对象 (ws 执行链提交未镜像) -- QA 审计既有发现, 非本卡范围.
  6. 仲裁项 (t_28a29244): E1 终态断言要求非 H 空名==0 与 ten 无来源现实冲突; F11 断言缺陷态 figures 聚合 hash 不变; 二者皆因合法修复翻转.

## 十, 复现

    cd /opt/data/workspace/Protreptic
    python3 build_w9_fclass_fix_evidence.py            # 重生成 registry + evidence (幂等)
    python3 build_w9_fclass_fix_evidence.py --check    # 校验产物与重算一致
    python3 verify_w9_fclass_fix.py                    # 终态断言 A-H
    python3 tools/build_figures_db.py --out /tmp/x.db  # 重建不回落 (副本)
    python3 tools/ci_data_check.py                     # 24/24 PASS

- 留痕 (scratch): /opt/data/profiles/elcano/cache/scratch/w9fix/ (dry_run_result.json, exec_main_result.json, chain_result.json, gates_final.json, verify_state.json, web_index_face.json, parity_pre.json)

## 十一, 提交/镜像/push 回执

- ws commit: 108e2826 (1373 files changed: 14 件改动 + 1359 移出)
- pb 镜像 commit: ac33cba5 (13 件 byte-exact)
- push: a7ba7f29..ac33cba5 -> origin main; ls-remote main = ac33cba53eb5b293bc9a51cf27e3c1b93f2c9a2c
- parity (镜像后): rc=0 -- 构建图 4593 件两仓逐字节一致, 单侧 0
- 独立校验: verify_w9_fclass_fix.py A-H 全过 (34 断言); espinosa QA 校验器 12 PASS / 3 FAIL (E1, F11, F12 为缺陷态口径, 登记待裁)
- v2 回执: ws 47f9852d -> pb 2586040c -> push ac33cba5..2586040c; ls-remote main = 2586040c...; parity (v2 后) rc=0 (4593 件逐字节一致)
