# Phase37-X2 evidence: findings.json self-check + H-SX-001 10/10 + refreshed counts

Card: `t_c39a6828` (serrano). Method: run the commands, paste raw output only.

## 0. Snapshot

| item | value |
| --- | --- |
| local time | `2026-09-19 22:35:58 ` |
| dev repo `/opt/data/workspace/Protreptic` | `f72a0d3d Phase37-X2: findings.json 自检脚本 verify_findings.py + 可复跑生成器 + 补 H-SX-001 全 10 条 + 计数刷新到当前库(2888/284;D1=60 D2=10 D3=6 D4=17 D6=40)` |
| publish repo `/opt/data/release/Protreptic-publish` | `9f95113 Phase37-X1: D3 豁免口径落地 gate + 两方向自测 + 交付报告（发布仓同步）` |
| `data/modes_data.json` sha256 (dev == pub) | `bf168171af42f8148c3adecbbc1a71258522676355357f6466acdcb25f2e61cb` |
| `data/audit/findings.json` sha256 | dev `726be6f4171d08ed253bed1170d056090cd2108471a4e08793b649e50c68abd6` |

Commands:

```bash
cd /opt/data/workspace/Protreptic && git log -1 --format='%h %s'
cd /opt/data/workspace/Protreptic && sha256sum data/modes_data.json data/audit/findings.json
```

```text
bf168171af42f8148c3adecbbc1a71258522676355357f6466acdcb25f2e61cb  data/modes_data.json
726be6f4171d08ed253bed1170d056090cd2108471a4e08793b649e50c68abd6  data/audit/findings.json
```

## 1. Deliverables

| file | role | sha256 |
| --- | --- | --- |
| `tools/verify_findings.py` | self-check script (required by the card) | `e9efdfd528bc67de6028081c870afab0240edd98342630e7762cb0f8f84acbb2` |
| `tools/build_audit_findings.py` | re-runnable findings generator (counts come from the live library) | `52ab0f1ffaa6e34a6d0f296420f2f9aba746e69dc75ea6bddb6f4119a883b610` |
| `data/audit/findings.json` | refreshed audit list, 133 entries | `726be6f4171d08ed253bed1170d056090cd2108471a4e08793b649e50c68abd6` |
| `docs/qa/phase37_x2_evidence.md` | this report | (self-reference omitted) |

## 2. verify_findings.py: positive run (exit 0)

```bash
cd /opt/data/workspace/Protreptic && python3 tools/verify_findings.py; echo EXIT=$?
```

```text
=== VERIFY FINDINGS ===
findings file: /opt/data/workspace/Protreptic/data/audit/findings.json
source library: /opt/data/workspace/Protreptic/data/modes_data.json
entries: 133
hard failures: 0
warnings: 1
  ::warning::E: these mode codes are harvested twice by get_all_modes (present both in the top-level modes array and inside a figure node): ['M-ASM-001', 'M-ASM-002', 'M-ASM-003', 'M-ASM-004', 'M-ASM-005', 'M-ASM-006', 'M-ASM-007', 'M-ASM-008', 'M-ASM-009', 'M-ASM-010']
[OK] verify_findings: all checks passed
EXIT=0
```

## 3. verify_findings.py: negative run (bogus code -> exit 1)

The injection puts a non-existent `mode_code` (and its anchor) into a **copy** of findings.json:

```bash
python3 /tmp/x2/inject.py      # writes /tmp/x2/neg/findings_bad.json with M-QA7-NONEXISTENT-999
cd /opt/data/workspace/Protreptic && python3 tools/verify_findings.py --findings /tmp/x2/neg/findings_bad.json; echo EXIT=$?
```

```text
wrote /tmp/x2/neg/findings_bad.json (injected M-QA7-NONEXISTENT-999)
=== VERIFY FINDINGS ===
findings file: /tmp/x2/neg/findings_bad.json
source library: /opt/data/workspace/Protreptic/data/modes_data.json
entries: 133
hard failures: 2
warnings: 1
  ::error::B: [M-QA7-NONEXISTENT-999] mode_code 'M-QA7-NONEXISTENT-999' does not exist in the source library (/opt/data/workspace/Protreptic/data/modes_data.json)
  ::error::C: [M-QA7-NONEXISTENT-999] anchor not found verbatim in modes_data.json: 'M-QA7-NONEXISTENT-999'
  ::warning::E: these mode codes are harvested twice by get_all_modes (present both in the top-level modes array and inside a figure node): ['M-ASM-001', 'M-ASM-002', 'M-ASM-003', 'M-ASM-004', 'M-ASM-005', 'M-ASM-006', 'M-ASM-007', 'M-ASM-008', 'M-ASM-009', 'M-ASM-010']
[FAIL] verify_findings: 2 problem(s)
EXIT=1
```

Second negative control: a stale/tampered summary count is also caught (self-consistency check D/E):

```bash
python3 /tmp/x2/inject2.py     # copy with summary.D6_orphan_reference = 999
cd /opt/data/workspace/Protreptic && python3 tools/verify_findings.py --findings /tmp/x2/neg/findings_count_bad.json; echo EXIT=$?
```

```text
wrote /tmp/x2/neg/findings_count_bad.json (summary.D6_orphan_reference=999)
=== VERIFY FINDINGS ===
findings file: /tmp/x2/neg/findings_count_bad.json
source library: /opt/data/workspace/Protreptic/data/modes_data.json
entries: 133
hard failures: 2
warnings: 1
  ::error::D: summary.D6_orphan_reference = 999 but the findings list holds 40 entries
  ::error::E: summary.D6_orphan_reference = 999 but a fresh scan of modes_data.json yields 40 (counts are stale)
  ::warning::E: these mode codes are harvested twice by get_all_modes (present both in the top-level modes array and inside a figure node): ['M-ASM-001', 'M-ASM-002', 'M-ASM-003', 'M-ASM-004', 'M-ASM-005', 'M-ASM-006', 'M-ASM-007', 'M-ASM-008', 'M-ASM-009', 'M-ASM-010']
[FAIL] verify_findings: 2 problem(s)
EXIT=1
```

The same script also flags the **stale** pre-X2 findings.json, i.e. it independently reproduces the QA6
finding #4 (counts 50/19/0/0 and 3/10 H-SX-001 rows):

```bash
git show c3da04bb:data/audit/findings.json > /tmp/x2/neg/findings_pre_x2.json
cd /opt/data/workspace/Protreptic && python3 tools/verify_findings.py --findings /tmp/x2/neg/findings_pre_x2.json; echo EXIT=$?
```

```text
=== VERIFY FINDINGS ===
findings file: /tmp/x2/neg/findings_pre_x2.json
source library: /opt/data/workspace/Protreptic/data/modes_data.json
entries: 9
hard failures: 27
warnings: 2
  ::error::A: findings[0] (M-P23F-001) missing field 'anchor'
  ::error::A: findings[1] (M-P23F-002) missing field 'anchor'
  ::error::A: findings[2] (M-P24F-001) missing field 'anchor'
  ::error::A: findings[3] (M-P25F-001) missing field 'anchor'
  ::error::A: findings[4] (M-P26F-001) missing field 'anchor'
  ::error::A: findings[5] (M-P27F-001) missing field 'anchor'
  ::error::A: findings[6] (M393) missing field 'anchor'
  ::error::A: findings[7] (M394) missing field 'anchor'
  ::error::A: findings[8] (M395) missing field 'anchor'
  ::error::C: [M-P23F-001] empty anchor
  ::error::C: [M-P23F-002] empty anchor
  ::error::C: [M-P24F-001] empty anchor
  ::error::C: [M-P25F-001] empty anchor
  ::error::C: [M-P26F-001] empty anchor
  ::error::C: [M-P27F-001] empty anchor
  ::error::C: [M393] empty anchor
  ::error::C: [M394] empty anchor
  ::error::C: [M395] empty anchor
  ::error::D: summary.D1_pseudo_figure = 50 but the findings list holds 5 entries
  ::error::D: summary.D2_fabricated_source = 10 but the findings list holds 3 entries
  ::error::D: summary.D3_source_contamination = 19 but the findings list holds 1 entries
  ::error::D: summary.total = 79 but len(findings) = 9
  ::error::E: summary.D1_pseudo_figure = 50 but a fresh scan of modes_data.json yields 60 (counts are stale)
  ::error::E: summary.D3_source_contamination = 19 but a fresh scan of modes_data.json yields 6 (counts are stale)
  ::error::E: summary.D4_empty_quote = 0 but a fresh scan of modes_data.json yields 17 (counts are stale)
  ::error::E: summary.D6_orphan_reference = 0 but a fresh scan of modes_data.json yields 40 (counts are stale)
  ::error::E: summary.total = 79 but a fresh scan yields 133
  ::warning::E: audit_meta.modes_file_sha256 differs from the current library hash; refresh with build_audit_findings.py --write
  ::warning::E: these mode codes are harvested twice by get_all_modes (present both in the top-level modes array and inside a figure node): ['M-ASM-001', 'M-ASM-002', 'M-ASM-003', 'M-ASM-004', 'M-ASM-005', 'M-ASM-006', 'M-ASM-007', 'M-ASM-008', 'M-ASM-009', 'M-ASM-010']
[FAIL] verify_findings: 27 problem(s)
EXIT=1
```

## 4. H-SX-001: all 10 rows, grep evidence

```bash
for c in M393 M394 M395 M396 M397 M398 M399 M400 M401 M402; do
  echo "--- $c"; grep -n -A10 "\"mode_code\": \"$c\"" data/modes_data.json | grep -E 'mode_code|source_chapter';
done
```

```text
--- M393
3882:      "mode_code": "M393",
3890-      "source_chapter": "《苏咸子·权变篇》",
--- M394
3949:      "mode_code": "M394",
3957-      "source_chapter": "《苏咸子·纵横篇》",
--- M395
4016:      "mode_code": "M395",
4024-      "source_chapter": "《苏咸子·言术篇》",
--- M396
4083:      "mode_code": "M396",
4091-      "source_chapter": "《苏咸子·权变篇》",
--- M397
4150:      "mode_code": "M397",
4158-      "source_chapter": "《苏咸子·虚实篇》",
--- M398
4217:      "mode_code": "M398",
4225-      "source_chapter": "《苏咸子·利益篇》",
--- M399
4284:      "mode_code": "M399",
4292-      "source_chapter": "《苏咸子·情报篇》",
--- M400
4351:      "mode_code": "M400",
4359-      "source_chapter": "《苏咸子·主动篇》",
--- M401
4418:      "mode_code": "M401",
4426-      "source_chapter": "《苏咸子·合纵篇》",
--- M402
4485:      "mode_code": "M402",
4493-      "source_chapter": "《苏咸子·时势篇》",
```

findings.json rows for H-SX-001 (10 D2 rows with real codes + the 10 D1 rows of the same quarantined figure):

```text
20 rows
  M393 D1_pseudo_figure
  M394 D1_pseudo_figure
  M395 D1_pseudo_figure
  M396 D1_pseudo_figure
  M397 D1_pseudo_figure
  M398 D1_pseudo_figure
  M399 D1_pseudo_figure
  M400 D1_pseudo_figure
  M401 D1_pseudo_figure
  M402 D1_pseudo_figure
  M393 D2_fabricated_source
  M394 D2_fabricated_source
  M395 D2_fabricated_source
  M396 D2_fabricated_source
  M397 D2_fabricated_source
  M398 D2_fabricated_source
  M399 D2_fabricated_source
  M400 D2_fabricated_source
  M401 D2_fabricated_source
  M402 D2_fabricated_source
```

## 5. Counts before/after

```bash
python3 /tmp/x2/read_summary.py c3da04bb          # BEFORE: committed file at c3da04bb
cd /opt/data/workspace/Protreptic && python3 tools/build_audit_findings.py    # AFTER: live scan
```

```text
BEFORE (c3da04bb): {"D1_pseudo_figure": 50, "D2_fabricated_source": 10, "D3_source_contamination": 19, "D4_empty_quote": 0, "D5_timeline_conflict": "N/A - no figures_db.json available", "D6_orphan_reference": 0, "D7_duplicate_definition": 0, "total": 79}
BEFORE audit_meta.total_modes_count=2838 total_figures=368

AFTER (live scan): {"D1_pseudo_figure": 60, "D2_fabricated_source": 10, "D3_source_contamination": 6, "D4_empty_quote": 17, "D5_timeline_conflict": "N/A - no figures_db.json available", "D6_orphan_reference": 40, "D7_duplicate_definition": 0, "total": 133}
AFTER audit_meta.total_modes_count=2888 total_figures=284

rev c3da04bb
summary: {"D1_pseudo_figure": 50, "D2_fabricated_source": 10, "D3_source_contamination": 19, "D4_empty_quote": 0, "D5_timeline_conflict": "N/A - no figures_db.json available", "D6_orphan_reference": 0, "D7_duplicate_definition": 0, "total": 79}
audit_meta.total_modes_count: 2838
audit_meta.total_figures: 368
findings entries: 9
H-SX-001 rows: 3 ['M393', 'M394', 'M395']

=== findings scan ===
findings entries: 133
  D1_pseudo_figure: 60
  D2_fabricated_source: 10
  D3_source_contamination: 6
  D4_empty_quote: 17
  D5_timeline_conflict: N/A - no figures_db.json available
  D6_orphan_reference: 40
  D7_duplicate_definition: 0
  total: 133
modes sha256: bf168171af42f8148c3adecbbc1a71258522676355357f6466acdcb25f2e61cb
(dry-run; pass --write to write the file)
```

## 6. D1-D7 rescan (no missing rows)

```text
{
 "scan_date": "2026-09-19",
 "modes_file": "data/modes_data.json",
 "modes_file_sha256": "bf168171af42f8148c3adecbbc1a71258522676355357f6466acdcb25f2e61cb",
 "total_modes_count": 2888,
 "top_level_modes_entries": 2868,
 "distinct_mode_codes": 2858,
 "modes_empty_mode_code": 10,
 "embedded_figure_mode_entries": 20,
 "total_figures": 284,
 "quarantined_figures": [
  "H-P23F-001",
  "H-SX-001",
  "P24F",
  "P25F",
  "P26F",
  "Phase27Final"
 ],
 "by_scope": {
  "D1_pseudo_figure": {
   "total": 60,
   "quarantined_figure": 60,
   "public_figure": 0
  },
  "D2_fabricated_source": {
   "total": 10,
   "quarantined_figure": 10,
   "public_figure": 0
  },
  "D3_source_contamination": {
   "total": 6,
   "quarantined_figure": 6,
   "public_figure": 0
  },
  "D4_quote_without_source": {
   "total": 17,
   "quarantined_figure": 17,
   "public_figure": 0
  },
  "D6_orphan_reference": {
   "total": 40,
   "quarantined_figure": 0,
   "public_figure": 40
  }
 },
 "methodology": "full regex/grep scan of data/modes_data.json; gate semantics shared with tools/credibility_gate.py; D1 list from tools/_quarantine.py; D3 is a strict scan (no exemption)",
 "notes": [
  "annotated references ('M-XXX-001(comment)' with an existing prefix code): 417 entries, not counted as D6 per library convention",
  "get_all_modes total 2888 = top-level modes 2868 + embedded figure-node duplicates 20; distinct mode_code 2858 (plus 10 entries with an empty mode_code, dropped at export)",
  "D5 not machine-checkable: figures_db.json (birth/death years) is absent",
  "D1/D2/D3/D4/D6 的 by_scope 见 audit_meta.by_scope: quarantined_figure 指该条 mode 的 figure_code 在隔离名单中"
 ]
}
```

Notes on the rescan:

- D1: 6 quarantined figures x 10 modes = 60 (the old list held 5 representative rows and claimed 50).
- D2: M393-M402, all 10 rows now enumerated (was 3/10). M402 was missed by a naive single-name filter
  because its source is 《苏咸子·时势篇》 while KNOWN_FAKE_SOURCES in the gate lists only the exact
  《苏咸子·xxx篇》 strings; build_audit_findings.py matches the book prefix 《苏咸子 instead.
- D3: 6 strict hits (unchanged vs QA6); all 6 sit on quarantined figures, so the gate exemption (X1,
  commit 15446dd6 / publish 9f95113) scores D3 = 0 for the CI gate while the audit list stays honest.
- D4: 17 rows with a quote but an empty source_chapter (all on quarantined figures); recorded as WARN-level
  rows instead of the previous hard 0.
- D5: N/A, figures_db.json (birth/death years) does not exist.
- D6: 40 bare-code dangling references, across 32 distinct modes and 25 distinct target codes (previously recorded as 0; the 417 annotated refs whose prefix code exists are NOT counted).
- D7: 0 (no duplicated mode_code in the top-level array, no duplicated definition_zh inside a figure).
- annotated references (417, prefix code exists) are excluded from D6 per library convention; they are
  counted in audit_meta.notes.

## 7. Two-repo sync + push

```bash
cd /opt/data/workspace/Protreptic && cp tools/verify_findings.py tools/build_audit_findings.py tools/  # etc.
```

(filled in after the push - see section 7.1 below)

