# Phase31-R7 归档目录过期模板副本：处置报告

- 卡片：`t_a55bd669` (Phase31-R7)
- 日期：2026-09-19
- 结论：采用**选项 (a) 同步**。`docs_site/docs/templates/*.md` 7 份已与源 `templates/*.md` **逐字节一致** (cmp 7/7 相同、sha256 7/7 相同)。
- 影响面：**线上零影响**。发布仓 `/opt/data/release/Protreptic-publish` 里没有 `docs_site/`，Pages 产物由 `mkdocs.pages.yml` ( `docs_dir: docs` ) 生成，`docs_site/` 不参与构建。
- 配套改动：`docs_site/mkdocs.yml` 的「复盘模板」nav 组加了镜像规则注释 (源在哪、怎么校验)，防止下次再漂移。

## 1. Root Cause

docs_site/docs/templates/*.md (English slug filenames) are old text from 2026-07, while root templates/*.md (Chinese filenames) are the current source.
The archive directory never followed source updates — for example, longzhong: archive 10505 B vs source 12040 B, text diff 111 lines, not just formatting: missing emoji prefix, H-SQ-22 corrected to H-SQ-52 in source, source also added Final Batch related archive table.

## 2. Why Choose (a) Sync, Not (b) Delete

1. Deleting would create new defects. docs_site is a self-contained and currently buildable old documentation site project: docs_site/mkdocs.yml has 33 file references in nav, 33/33 exist; docs_site/docs has 47 markdown files. Deleting these 7 files would make all 7 nav references in the "Review Template" group dangling (mkdocs reports warnings, broken links), trading one defect for another.
2. The archive directory is not a build artifact and not in the publishing chain. The publish repo has no docs_site/, no root templates/; no workflow builds or copies docs_site/, grep -rn docs_site .github/ tools/ only hits descriptive comments in mkdocs.pages.yml. It is neither an online content source nor a reproducible build artifact, but a retained historical documentation project. For such directories, non-destructive "align with source" is better than "delete 7 files, leave incomplete snapshot".

## 3. Acceptance Evidence: Source vs Archive (After Sync, Byte Count per File)

| slug | source file | source bytes | archive file | archive bytes | sha256 prefix (source=archive) | cmp |
|---|---|---|---|---|---|---|
| longzhong | templates/隆中对复盘.md | 12040 | docs_site/docs/templates/longzhong.md | 12040 | 732403f63b88 | identical |
| baidi | templates/白帝托孤离职.md | 8809 | docs_site/docs/templates/baidi.md | 8809 | 16be7789555b | identical |
| chibi | templates/赤壁之战复盘.md | 13166 | docs_site/docs/templates/chibi.md | 13166 | 8fa8f593dd74 | identical |
| beifa | templates/北伐复盘.md | 14530 | docs_site/docs/templates/beifa.md | 14530 | 98957478c6d8 | identical |
| jieting | templates/街亭之战复盘.md | 13998 | docs_site/docs/templates/jieting.md | 13998 | 259efe012ba9 | identical |
| yiling | templates/夷陵之战复盘.md | 15851 | docs_site/docs/templates/yiling.md | 15851 | df208c801427 | identical |
| changban | templates/长坂坡复盘.md | 16384 | docs_site/docs/templates/changban.md | 16384 | 609067e39c16 | identical |

Archive bytes before and after sync (positive numbers indicate archive filled in missing content):

| slug | archive bytes before | archive bytes after | delta |
|---|---|---|---|
| longzhong | 10505 | 12040 | +1535 |
| baidi | 8400 | 8809 | +409 |
| chibi | 12302 | 13166 | +864 |
| beifa | 13677 | 14530 | +853 |
| jieting | 13134 | 13998 | +864 |
| yiling | 14990 | 15851 | +861 |
| changban | 15516 | 16384 | +868 |

## 4. Original Commands and Output

Byte count and sha256 per file (source and archive have same names and hashes in pairs):

```console
$ cd /opt/data/workspace/Protreptic
$ sha256sum templates/*.md docs_site/docs/templates/*.md | sort -k2
16be7789555b6121e76b1e5560150c05992a2c56e93f3ba6896ffe35fed65ecf  docs_site/docs/templates/baidi.md
98957478c6d82a45f76b80ba835b1e63564628bfda43b5dfd0ec27ecc15d738c  docs_site/docs/templates/beifa.md
609067e39c16b785425fa6f1e15286d236e43e78fea52e1dea4a836b4dfb9499  docs_site/docs/templates/changban.md
8fa8f593dd74441928ba7060d3672532a57cfe0be63b35baa0a8faad945845a0  docs_site/docs/templates/chibi.md
259efe012ba9d91d6c67054cfa6167be46eff64a2ed73ce9c0b97d01adbc65a0  docs_site/docs/templates/jieting.md
732403f63b888769fb9125e60a0da5c716701440bdb68ff492691c984cdb4652  docs_site/docs/templates/longzhong.md
df208c8014274dfc650c7776d6b95b9a6e84f2fe77cecfd961b801f5f4797398  docs_site/docs/templates/yiling.md
98957478c6d82a45f76b80ba835b1e63564628bfda43b5dfd0ec27ecc15d738c  templates/北伐复盘.md
df208c8014274dfc650c7776d6b95b9a6e84f2fe77cecfd961b801f5f4797398  templates/夷陵之战复盘.md
16be7789555b6121e76b1e5560150c05992a2c56e93f3ba6896ffe35fed65ecf  templates/白帝托孤离职.md
259efe012ba9d91d6c67054cfa6167be46eff64a2ed73ce9c0c97d01adbc65a0  templates/街亭之战复盘.md
8fa8f593dd74441928ba7060d3672532a57cfe0be63b35baa0a8faad945845a0  templates/赤壁之战复盘.md
609067e39c16b785425fa6f1e15286d236e43e78fea52e1dea4a836b4dfb9499  templates/长坂坡复盘.md
732403f63b888769fb9125e60a0da5c716701440bdb68ff492691c984cdb4652  templates/隆中对复盘.md
```

Per-file `cmp` (7/7 byte-identical):

```console
$ for p in "longzhong:隆中对复盘" "baidi:白帝托孤离职" "chibi:赤壁之战复盘" \\
    "beifa:北伐复盘" "jieting:街亭之战复盘" "yiling:夷陵之战复盘" "changban:长坂坡复盘"; do
    s="${p%%:*}"; t="${p##*:}"
    cmp -s "templates/$t.md" "docs_site/docs/templates/$s.md" \\
      && echo "cmp identical: templates/$t.md <-> docs_site/docs/templates/$s.md" \\
      || echo "cmp DIFF: $s"
  done
cmp identical: templates/隆中对复盘.md <-> docs_site/docs/templates/longzhong.md
cmp identical: templates/白帝托孤离职.md <-> docs_site/docs/templates/baidi.md
cmp identical: templates/赤壁之战复盘.md <-> docs_site/docs/templates/chibi.md
cmp identical: templates/北伐复盘.md <-> docs_site/docs/templates/beifa.md
cmp identical: templates/街亭之战复盘.md <-> docs_site/docs/templates/jieting.md
cmp identical: templates/夷陵之战复盘.md <-> docs_site/docs/templates/yiling.md
cmp identical: templates/长坂坡复盘.md <-> docs_site/docs/templates/changban.md
```

## 5. Supporting Changes: Mirror Rules in Nav Configuration

Added 4 lines of comments under the "Review Template" group in docs_site/mkdocs.yml: these 7 files are byte-level mirrors of root templates/*.md. When modifying templates, first change root templates/ then overwrite this directory file by file. The comments include verification command `cmp <source> <mirror>`.

Configuration is still parseable, nav has no duplicate keys (parsed docs_site/mkdocs.yml using web/node_modules/js-yaml in repo):

```console
$ node .tmp_yamlchk.mjs
top-level nav entries: 10
unique: true
templates items: 7
missing files: 0
```

## 6. Sibling Copy Scan (Why Only These 7 Files)

Full repo scan of 7 template title copies (excluding node_modules/web/dist/.git):

| Location | Nature | Action |
|---|---|---|
| templates/*.md | Current source (SPA download chain and prerendered body source) | No change |
| docs_site/docs/templates/*.md | Old documentation site mirror (R7 defect point) | Now synced to byte-level mirror |
| web/public/templates/*.md | SPA download copy (online /protreptic/templates/<id>.md is it) | No change: content matches source, only formatting differences (2 fewer standalone >, line-end whitespace, no newline at file end); publish repo same-name files are byte-identical to workspace |
| web/dist/templates/*.md | Build artifact | No change |
| release/v2.0.0/protreptic-templates/*.md | v2.0.0 frozen release snapshot (see docs/ci/markdown_lint_policy.md: release/** frozen, no longer maintained) | Retain, not considered expired copy under freeze semantics |

## 7. Publish Repo Status

Changes in this card to archive (docs_site/**) are NOT in the publish repo, so zero impact on live site. The publish repo only synced this report (docs/** is in Pages trigger path), push output in card handoff summary.

```console
$ git -C /opt/data/release/Protreptic-publish status -sb
## main...origin/main
```
