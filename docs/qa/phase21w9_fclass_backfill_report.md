# Phase21-W9-F 回填报告 - F 类名称回填 (干跑对账 + 执行 + 持久性)

- 日期: 2026-09-24
- 卡: t_d7faccc5 (W9 F 类修复卡); 闭合 t_9ed2866a 缺件 ① (回填干跑对账报告)
- 结论: 504 条可回填真名已全部落库并到达四面 (DB, figures.index, 分片, 统一名录); 干跑与终态双重复核; 重建不回落.

## 一, 对账口径 (W4 勘定 537 -> 现值 504 / 10)

- 8adbdabd 勘定: 1056 行 / 空名 563 (H 16 + 非 H 547); 非 H 有 legacy 名者 537.
- e5ddd13f/6f298ca1 现值: 1027 行 / 空名 514 = 504 + 10.
- 33 差 = 31 行移除 (RW-KAG-1..27, JP-Sas-001, MY-Mah-001, SG-Lee-001, UZ-Ulu-001) + 2 行已命名 (RW-KAG-001, SG-LEE-001).
- 514 分解: 504 可回填 (400 真名 + 104 legacy name==code), 10 无来源.
- 口径注记: 源侧可回填集合 = 修复前 DB 空名集 (504) 与 scenarios legacy 名的交集; 逐条与 legacy 全等比对, 零自造.

## 二, 干跑 (副本先行)

- 副本 db_dry.sqlite = 主库拷贝; build_figures_db.py --out 副本, 连跑两次:
  - rc=0 / rc=0; 两次行内容全等 (幂等 true).
  - named=1017, empty=10 (==ten); changed_rows=504 (==restorable); 变更列仅 name_zh/name_en; 0 mismatch vs legacy; 104 行 name==code.

## 三, 执行与持久性

- 主库重建 x2 (rc=0/0): 两次均 1017/10; db sha16 90227b16 -> d7d5a228 (页面布局幂等, 行内容稳定).
- 终态副本复跑: rows 全等 true; 1017/10 -- 重建不回落.
- 结论: 回填是数据源侧 (scenarios) + 装载器 (双读回退) 的联合结果, 任何一次合法重建后名字保持.

## 四, 到达面核验 (504/504)

- DB: named 1017 (513 原有 + 504 回填); empty 10.
- figures.index.json: 非 H 空 10; 与 legacy 0 mismatch.
- 分片 figures/*.json (1027 件): 0 mismatch, 0 missing.
- index.unified.json: 名字 0 mismatch.
- 样张 AE-FED-001 四面一致 (真名).

## 五, 残留登记 (不臆造)

- ten = 待核名: 无来源; 登记于 data/audit/phase21w9_fclass_residual_registry.json (ten.items, status=待核名).
- 104 = 占位待补名 (legacy name_zh == code): 登记于同文件 code_as_name.codes.
- 机读证据: docs/qa/phase21w9_fclass_fix_evidence.json (decomposition 段).
