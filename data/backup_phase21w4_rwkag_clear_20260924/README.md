# 备份盘: RW-KAG-1..27 模板废件全链清档前像 (卡 t_ee203180)

- 来源卡: kanban t_ee203180 (Phase21 W4, 下游 QA t_8bad8d98)
- 依据: docs/research/phase21w4_fix_manifest.md §3.6 R10 + 卡步1; 备份模板 60 件 (6 共享 + 27 草稿 + 27 分片)
- 时点: 2026-09-24 (编辑前; head_at_backup = 37545ac770d6b0d3c0be4ffb40c9a404b47f70b1)

## 内容 (payload 89 件, 结构保真)

| 组 | 件数 | 说明 |
|---|---|---|
| shared | 6 | code_maps_en.json / scenarios_zh.json / scenarios_en.json / protreptic.db / web_p0_routes.json / sitemap.xml (编辑/重建前像) |
| draft | 27 | tools/json/RW-KAG-1..27.json (草稿本体; 修复链为 R100 移动归档, 不删字节) |
| shard | 27 | web/public/data/figures/RW-KAG-1..27.json (重建链重建后消失, 前像在此) |
| aggregate (超模板) | 2 | web/public/data/figures.index.json / index.unified.json (聚合前像) |
| root_legacy (超模板) | 27 | 根目录 RW-KAG-1..27.json 双胞 (逐字节与草稿相同; 归档移出) |

- MANIFEST.sha256: 标准 `sha256sum -c` 格式, 覆盖 payload 89 件 (本 README 与 extract 脚本为附属说明件, 不在清单内):
  `cd data/backup_phase21w4_rwkag_clear_20260924 && sha256sum -c MANIFEST.sha256`
- backup_manifest.json: 逐件 bytes/sha256 (源前像与拷贝双记) + root 双胞逐字节相等表 + 发布仓 intl 副本 27 件引用 (equals_draft=true, 字节归档复用草稿备份).

## 超模板说明 (显式登记, 见卡报告)

1. root_legacy 27 件: 根目录同码双胞, manifest R10 字面未点名; 依卡步7 (全仓 0 残留) + W7 卡 (t_d24e11bc) 「RW-KAG-1..27 面由 W4 t_ee203180 先行处置」口径, 归档移出 (git R100 移动, 原 blob 在史)。
2. aggregate 2 件: 全链前像完整性补强 (figures.index / index.unified 均含 27 码条目)。
3. 发布仓独有 data/intl_figures/RW-KAG-1..27.json (27 件): 逐字节与草稿相同; 在发布仓镜像阶段归档移除, 字节归档引用草稿备份 (不重复占盘)。

## 回放

- 字节级片段提取/校验: `python3 extract_rwkag_fragments.py` (校验) / `--extract RW-KAG-1 --out DIR` (落盘)。
- 全链还原: 逐件拷回原相对路径 (tracked 件亦可由 git 历史恢复; 场景条目为键级删除, 依前像整键回填)。
- 归档 JSON: docs/research/_archive/RW-KAG_1-27_archive.json (per_code_fragments 27x6 片段 sha256)。
