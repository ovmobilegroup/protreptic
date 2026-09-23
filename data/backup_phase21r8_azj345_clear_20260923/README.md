# H-AZJ-345 清除前像备份（卡 t_3669eb4a）

生成时间：2026-09-24 CST
用途：Phase21-R8 遗留清档卡对 H-AZJ-345 执行全链清除前的 byte-exact 前像。所有文件在修改前原样复制。

## 恢复法

```
cd /opt/data/workspace/Protreptic
while read sha path; do
  cp "data/backup_phase21r8_azj345_clear_20260923/$path" "$path"
done < data/backup_phase21r8_azj345_clear_20260923/MANIFEST.sha256
```

（或单件：`cp data/backup_phase21r8_azj345_clear_20260923/<path> <path>`）
追踪件亦可用 git 恢复（备份时 HEAD 见 MANIFEST.json 附注）；产品件由链重建可再生。

## 清单

- tools/json/scenarios_zh.json (3038171 B, sha256 c240aa30, tracked)
- tools/json/scenarios_en.json (2288761 B, sha256 018aadd4, tracked)
- api/data/scenarios_en.json (826335 B, sha256 782418eb, tracked)
- tools/test_full_backup.py (12324 B, sha256 6d715285, tracked)
- tools/batch2_candidates.json (22933 B, sha256 532206ef, tracked)
- tools/code_maps_en.json (86424 B, sha256 b1893a9b, tracked)
- three_dimensional_comparison_matrix.xlsx (6194 B, sha256 842ba499, tracked)
- tools/pages_preflight.py (12311 B, sha256 440fb33a, tracked)
- tools/export_static_site.py (40856 B, sha256 0166d064, tracked)
- tools/ci_data_check.py (16020 B, sha256 8efa76d4, tracked)
- docs/historical_figures_thinking_modes_library.md (1497787 B, sha256 a2b37271, tracked)
- docs/research/batch_new_figures_research.md (39778 B, sha256 eafcc559, tracked)
- docs/research/candidates_v4_research.legacy.md (3334 B, sha256 8518458e, tracked)
- docs/architecture/web_p0_routes.json (681153 B, sha256 dd5c664b, tracked)
- docs/architecture/static_data_manifest.json (3748 B, sha256 7afc3e46, tracked)
- web/public/sitemap.xml (211252 B, sha256 d15b6858, tracked)
- web/src/generated/siteCounts.ts (2656 B, sha256 a5a47d3f, tracked)
- web/public/data/meta.json (3563 B, sha256 1f35459d, untracked)
- web/public/data/figures.index.json (212513 B, sha256 f0eded8c, untracked)
- web/public/data/figures/H-AZJ-345.json (2659 B, sha256 bf39b486, untracked)
- web/dist/data/meta.json (3556 B, sha256 a1ff7edd, untracked)
- web/dist/data/figures.index.json (212513 B, sha256 f0eded8c, untracked)
- web/dist/data/figures/H-AZJ-345.json (2659 B, sha256 bf39b486, untracked)
- web/dist/data/index.unified.json (484731 B, sha256 22d22a0f, untracked)
- web/dist/sitemap.xml (211252 B, sha256 d15b6858, untracked)
- site_docs/historical_figures_thinking_modes_library/index.html (2047298 B, sha256 99ed9f38, untracked)
- site_docs/research/batch_new_figures_research/index.html (203957 B, sha256 4f0d2bf6, untracked)
- site_docs/architecture/web_p0_routes.json (681153 B, sha256 dd5c664b, untracked)
- site_docs/search/search_index.json (21379490 B, sha256 736177cd, untracked)
- docs_site/docs/historical_figures_thinking_modes_library.md (1319110 B, sha256 5f238a4e, tracked)
- docs_site/docs/scenario_tags.json (325514 B, sha256 198e96a7, tracked)

缺失（备份时不存在）：无
