# Phase21-W7 清档分类裁定（t_d24e11bc）

- 日期：2026-09-24 ｜ 方法：逐件（路径/追踪态/引用扫描[文件名与 code 两向；构建步骤·web/src·tools·docs·api·CI]/字节孪生对照/裁定）
- 明细（逐件记录，含 sha256 前像）：`data/audit/phase21w7_classification.json`（1351 条）

## 计数

| face | 裁定 | 件数 |
|---|---|---|
| abnormal_name | delete | 6 |
| backup_dir | keep_registered | 33 |
| r7_disposed | already_disposed | 5 |
| root_json | archive_delete | 632 |
| root_json | keep | 2 |
| tools_json | archive_delete | 670 |
| tools_json | keep | 3 |

## 裁定口径

- **保留**：live 读者存在（配置 2 件：.markdownlint.json/lighthouserc.json）；live 输入 3 件（tools/json/scenarios_zh|en.json、scenario_tags.json）
- **归档后删**：零构建价值（不在 build_figures_db find() 读序/parity 现役集）＋零指向该件读者＋字节孪生存在（publish 镜像或字节相等）
- **删（备份后）**：异常名字面量名杂物（d）；前像全部 byte-exact 入 `data/backup_phase21w7_clean_20260924/`
- **登记不动**：backup 目录（f，33 个；其中 30 已入库按先例保持，3 未入库为他卡在途，本卡不夹带）；R7 已处置 4+1 件（g，只读复核）

## 逐面

### 根面（634 json + `, ` + 5 异常目录）

- 保留 2：.markdownlint.json、lighthouserc.json
- 归档后删 632：数据件（AE-FED-001 式，code 现役于 scenarios 而根副本零读者）/ 旧稿（MENG/ZHANG 系）/ 报告件 / code_maps 系旧副本 / scenarios·scenario_tags 根旧副本（读者解析均非根）/ test 杂物
- 删：`, `（2 字节）与 5 个 shell 误操作目录树（$(echo …/$(printf …/(echo #! …/<parameter=path>…/$(echo 单引号 …，内容=破碎命令片段）
- H-LXN-001.json：同族数据件（14 处历史提及均 docs/登记类，无读者）→ 归档后删；无错名残留（「错名残留」指 tools/json 内错名件，本卡逐件扫描 0 命中）

### tools/json 面（673 件 recursive）

- 保留 3：scenarios_zh.json、scenarios_en.json、scenario_tags.json（构建读序第一候选；parity TOOL_DATA_FILES）
- 归档后删 670：figure 草稿 613（code 现役于 scenarios）/ 一次性脚本 33 / schema 文档 2 / backup 1（ZA-MAN-001.json.bak）/ 陈旧目录 21（AU-NZ 8 · IL 1 · NO 4 · TR-UZ-KZ 8）
- 全部 673 件在发布仓同路径 byte-equal（逐件已证）；删前逐件前像入备份

### 其余面

- backup 目录 33 个：30 已入库（按先例保持）；3 未入库（W5FIX/W8B1/H-SHF-001，他卡在途产物，登记移交不夹带）
- R7 已处置件（tools/json/main_data.json 等 5 项）：原路径不存在，只读复核
