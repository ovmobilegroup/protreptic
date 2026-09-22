# Phase 20 数据清理报告 — 程颢旧码 H-CH-001 孤儿文件清档

- 卡号：`t_6cf3089f`（assignee: elcano）；上游：`t_dbb56a30`（文档归档, pigafetta）/ `t_3f363cbe`（QA, espinosa）
- 对象：旧码 `H-CH-001`（程颢，Phase 21 基础版）→ canonical 码 `H-CHE-001`（Phase 20 入库版）
- 清理前 HEAD：`96759545`；验收脚本：`qa_chenghao_archive.py`（上游 34 项）、`verify_chenghao_orphan_cleanup.py`（本卡 23 项）
- 证据文件：`docs/research/phase20_chenghao_orphan_cleanup_evidence.json`

## 一、依据与范围

Phase 20 数据入库 `c06d438a` 用 canonical 码 `H-CHE-001` 取代旧码 `H-CH-001` 并删除 `data/figures/H-CH-001.json`，
遗留三份无归属的孤儿文件（无对应 figure 档，已成死档案）。上游 QA 报告第 3.2 节（`docs/research/phase20_chenghao_qa_report.md`）
与归档报告第 4 节（`docs/research/phase20_chenghao_archive_report.md`）已登记清单并把清理另立本卡。

本卡范围：删除下列三文件、复跑扫描确认残留收敛、确认无新增悬空、复跑上游 QA、提交说明依据。
**不涉及**：程颐（H-CHI-001）/ 陆九渊（H-LJY-001）标注为邻卡范围的旧码条目；历史报告、审计留痕与备份快照（历史不改）。

## 二、清理项（三文件已删）

| 文件 | 大小 | 行数 | SHA256（删前） | git blob | 最后提交 |
| --- | --- | --- | --- | --- | --- |
| `data/individuals/H-CH-001.json` | 13,973 B | 196 | `5a67aab9fca4…5944f0a3` | `2c2891e8` | `75d4c138` 2026-09-08 Phase 21 归档上游研究成果 |
| `data/individuals/H-CH-001_modes.json` | 35,212 B | 468 | `c781906c86d5…b8bc8868` | `9d539d2b` | `75d4c138` 同上 |
| `docs/figures/H-CH-001.md` | 21,299 B | 192 | `e1751529f502…afdc67b` | `e7d4e6ff` | `ece9b153` 2026-09-08 Phase 21 档案重建（九节结构） |

删除方式：`git rm`（三文件均为 git 跟踪文件，内容完整保留在仓库历史，可按 blob 直接取回）。

## 三、删除前核查

1. **审计引用属历史留痕（不连带修改）**：`data/audit/figure_field_defects.json`（卡 t_e3f8cf8f 快照，`generated_at=2026-09-21`）
   把 `H-CH-001.json` 记为 `empty_name` 类缺陷、`status=fixable`；`data/audit/figure_field_fix_manifest.json` 记录该文件的
   `figure_name` 补写（`9ff4cfc4… → cc500ce6…`）。两者均为定点快照报告，按「历史报告不改」保留。
2. **活跃数据层零引用**：`data/figure_names.json`、`data/code_maps.json`、`data/modes_data.json`、
   `data/scenarios_zh.json`、`data/scenarios_en.json`、`data/scenario_tags.json`、`data/figures/*.json` 均无 `H-CH-001`。
3. **canonical 资产完整**：`data/figures/H-CHE-001.json` ↔ `data/individuals/H-CHE-001.json` ↔ `docs/figures/H-CHE-001.json`
   三镜像字节一致（SHA256 `40aa4b20d188…891efc`，4,539 B）；`docs/figures/H-CHE-001.md` 29,797 B；
   `figure_names` 登记 `H-CHE-001→程颢`；`code_maps.figures.H-CHE-001` 10 条 mode_ids；主库 `M-CHE-001~010` 齐全。

## 四、删除后复跑扫描

`grep -r "H-CH-001"`（排除 `.git/`、`site_docs/`）命中 **36 个文件**，全部落在白名单类别内（`verify_chenghao_orphan_cleanup.py` 第 5 节逐类判定，越界 = 0）：

| 类别 | 文件 |
| --- | --- |
| 历史报告/汇总 | `docs/research/phase20_chenghao_{qa,merge,archive}_report.md`、`phase20_chengyi_{qa,merge}_report.md`、`phase20_lujiuyuan_merge_report.md`、`phase20_hou_xuan_archive_report.md`（仓库根）、`CHANGELOG.md`、本报告与证据 JSON |
| 审计留痕 | `data/audit/figure_field_defects.json`、`data/audit/figure_field_fix_manifest.json` |
| 备份快照 | `data/backup_merge_H-CHE-001_20260922_122743/H-CH-001.json`、`data/backup_merge_H-ZDY-001_*/code_maps.json`×3、`backups_merge_H-DZ-001_*/`×4、`backups_merge_H-SJM-001_*/`×4 |
| QA/生成脚本（检查项内的码字面量） | `qa_chenghao_archive.py`、`qa_chenghao_dangling.py`、`qa_chengyi_archive.py`、`qa_chengyi_deep.py`、`build_chengyi_archive.py`、`build_lujiuyuan_archive.py`、`verify_chenghao_orphan_cleanup.py` |
| 邻卡范围（陆九渊/程颐 流水线） | `data/individuals/H-LJY-001_modes.json`（**qa_summary 注记**，非可解析引用字段）、`docs/figures/H-LJY-001.md`、`docs/figures/H-CHI-001.md`（两处均为修复记录行） |
| 根目录遗留副本 | `code_maps.json`、`code_maps.json.backup_homer_20260922_070407`（见第七节） |

**无新增悬空**：`data/figures/*.json` 中 target 指向 `H-CH-001` 的引用 = **0**；
存量 47 条悬空引用（`H-Bismarck-001`/`H-Lenin-001` 等旧命名）与本次清理无关，且本卡未触碰 `data/figures/`，数量与清理前一致。

## 五、验收结果

- `python3 qa_chenghao_archive.py` → **34 项 PASS 34 / WARN 0 / FAIL 0**（退出码 0，清理后复跑）
- `python3 verify_chenghao_orphan_cleanup.py` → **23 项 PASS 23 / WARN 0 / FAIL 0**（退出码 0）
  - 覆盖：孤儿三文件（工作区 + git 索引）已删、活跃数据零残留、v6 块无旧码、无旧码可解析引用字段、
    旧码悬空 = 0、canonical 三镜像一致、残留清单白名单判定、上游 QA 复跑
- **冻结快照复核**（`git worktree add --detach … 26f0565e`，从 commit object 检出，规避同仓并发写）：
  `qa_chenghao_archive.py` 34 PASS / 0 FAIL、`verify_chenghao_orphan_cleanup.py` 23 PASS / 0 FAIL

## 六、归档前内容留存说明（重要）

删除件是 Phase 21「基础版」建档，与 canonical Phase 20 档案内容**不完全重叠**。以下字段仅存于孤儿件（清档后仅能从 git 历史取回）：

| 字段 | canonical `data/figures/H-CHE-001.json` | 孤儿 `data/individuals/H-CH-001.json` |
| --- | --- | --- |
| `mode_evidence` | 空 `[]` | 10 条（含原文摘录 + 释义） |
| `protreptic_mapping` | 空 `{}` | 5 键映射 |
| `modern_value_zh` / `_en` | 无该字段 | 各 5 条 |
| `place_of_origin` / `unique_thing` | 无该字段 | 有 |
| `cross_references` | 2 条（H-ZZ-001、H-ZDY-001） | 3 条（多 `H-GX-001` oneness_vs_independence） |
| `tags` | 10 条 | 30 条 |
| Phase 21 模式记录 | — | `M-CH-001~010` 10 条（定义/原则/典型产出等） |

取回命令（blob 已在上表）：

```
git show 2c2891e852bbff4a5142b88ce109cdb1276090ed   # data/individuals/H-CH-001.json
git show 9d539d2bf49e7f207cf5c775ef8f98b2b49b8fde   # data/individuals/H-CH-001_modes.json
git show e7d4e6ff971a66c0f0dbc5906f6c8669bbca0518   # docs/figures/H-CH-001.md
```

此外 `data/backup_merge_H-CHE-001_20260922_122743/H-CH-001.json`（**已跟踪**）是图档级孤儿件的复制备份，
与孤儿件仅差 `figure_name` 一字段，可用作免 git 历史的长驻留存。Phase 21 十条模式记录无独立备份副本。

> 是否把上述孤儿独有字段回填进 canonical 图档（会牵动三镜像与 `qa_chenghao_archive.py` 的 34 项判据，属文档归档卡范围），
> 由编排层决定；本卡按清档指令执行，不做越界改写。

## 七、范围外相邻问题（已上报，本卡未处理）

1. **根目录 `code_maps.json`（遗留扁平注册表）**：`tools/check_repo_parity.py:159` 已把它登记为「根目录遗留副本」；
   最近仍被 `2371a585`（mining phase46）追加条目。其中程颢仍登记在旧码 `H-CH-001` 下、且无 `H-CHE-001` 条目（22 处命中）。
   是否迁移为 canonical 码属该文件的整体口径问题，需编排层决策（本卡未改）。
2. **`site_docs/**`（gitignored 构建产物）**：372 个文件命中，含旧码页面 `site_docs/figures/H-CH-001/index.html`。
   该目录不入库（`.gitignore` 已登记，CI `pages.yml` 现场 `mkdocs build` 生成），源文件删除后下次构建不再生成旧码页面。
3. **同类候选（启发式扫描，需逐案裁定）**：`data/individuals/` 中 21 个基础码、`docs/figures/` 中 32 个 `.md`
   无同名 `data/figures/<code>.json`（如 `H-TYY-001.md` 对应 canonical `H-TOU-001`、`H-HZ-001`/`H-WZ-001` 等旧码族）。
   清单见证据文件 `same_class_candidates` 字段；属系统性旧码遗留，建议编排层另立专项卡，本卡不做越界清理。

## 八、复现

```
cd /opt/data/workspace/Protreptic
git ls-files -- data/individuals/H-CH-001.json data/individuals/H-CH-001_modes.json docs/figures/H-CH-001.md   # 应无输出
grep -rn "H-CH-001" . --exclude-dir=.git --exclude-dir=site_docs        # 仅白名单类别
python3 qa_chenghao_archive.py                                          # 34 PASS / 0 FAIL
python3 verify_chenghao_orphan_cleanup.py                               # 23 PASS / 0 FAIL
```
