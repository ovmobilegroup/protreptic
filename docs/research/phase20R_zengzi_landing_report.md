# Phase20R landing report: Zengzi (H-ZX-001) - card t_4a9c2c2e (elcano)

## 1. Deliverables (real paths)

- data/figures/H-ZX-001.json
- data/individuals/H-ZX-001.json
- docs/figures/H-ZX-001.json
- data/individuals/H-ZX-001_modes.json
- data/figures/H-ZX-001_modes.json
- docs/figures/H-ZX-001.md
- data/figure_names.json
- scenarios_zh_add.json
- scenarios_en_add.json
- data/audit/phase20R_zengzi_landing_manifest.json
- docs/research/phase20R_zengzi_landing_evidence.txt
- verify_hzx_landing.py

## 2. v6 landing

- Figure doc aligned to v6: figure-level fields (gender/ethnicity/time_period_standardized/primary_language/intellectual_tradition/core_thoughts/famous_quote/influence/thinking_mode_count/mode_evidence/tags/cross_references/protreptic_mapping/modern_value_zh+en/unique_thing/modes/id/phase20) added; 10 embedded mode records upgraded to v6 field names (mode_code/category/domain_zh/domain_en/level/priority/process_zh+en/representative_cases_zh+en/modern_applications_zh+en), legacy aliases process/modern_applications kept for the upstream script.
- New data/individuals/H-ZX-001_modes.json carries the 10 v6 records (merge-card input); companion H-ZX-001_modes.json gains thinking_modes_v6_phase20.
- Three-mirror convention: data/figures, data/individuals, docs/figures identical sha256.
- Main library NOT written by this card: modes_data.json / code_maps.json / scenarios_*.json / scenario_tags.json -> merge card t_16ebe5c9.

## 3. Legacy-code disposition (quarantine, evidence kept)

- data/individuals/H-ZS-001.json -> data/figures/_duplicates/H-ZS-001_genf_individuals.json sha256=0a5de88c16358ffb
- data/individuals/H-ZS-001_modes.json -> data/figures/_duplicates/H-ZS-001_genf_individuals_modes.json sha256=58f637c1be1e52cf
- docs/figures/H-ZS-001.md -> data/figures/_duplicates/H-ZS-001_genf_docs_page.md sha256=af7044fafd48286e
- docs/figures/H-ZX-001.md.bak_zengzi_fix -> data/figures/_duplicates/H-ZX-001_legacy_docs_page.bak_zengzi_fix.md sha256=623d1c31e6f852ef
- H-ZX-001.json -> data/figures/_duplicates/H-ZX-001_root_copy.json sha256=4f371d8c99bdf15d
- H-ZX-001_modes.json -> data/figures/_duplicates/H-ZX-001_modes_root_copy.json sha256=546cc1b759cf035e
- docs/figures/H-ZX-001.md -> data/figures/_duplicates/H-ZX-001_legacy_docs_page.md sha256=220dead2f89cc127
- tools/update_zengzi_db.py -> data/figures/_duplicates/zengzi_legacy_scripts/update_zengzi_db.py sha256=2a88a03c3c2eec10
- tools/verify_zengzi.py -> data/figures/_duplicates/zengzi_legacy_scripts/verify_zengzi.py sha256=3252e20a2ecc6fa7
- verify_zengzi_data.py -> data/figures/_duplicates/zengzi_legacy_scripts/verify_zengzi_data.py sha256=561b3eddd868b908
- check_zengzi.py -> data/figures/_duplicates/zengzi_legacy_scripts/check_zengzi.py sha256=75cd6946aa156e62
- scenarios_zh_add.json -> data/figures/_duplicates/zengzi_genf_staging/scenarios_zh_add.json sha256=9a73077099ebab99
- scenarios_zh_new.json -> data/figures/_duplicates/zengzi_genf_staging/scenarios_zh_new.json sha256=16bf7598a91ddeab
- scenarios_en_add.json -> data/figures/_duplicates/zengzi_genf_staging/scenarios_en_add.json sha256=b4d7ba46079afeca
- verify_zengzi.py -> data/figures/_duplicates/zengzi_legacy_scripts/verify_zengzi_root.py sha256=877b58fd9f5cf008
- data/figure_names.json: H-ZS-001 key removed (1099 -> 1098); H-ZX-001* keys kept.
- staging: Gen-F HS-ZS-001/ES-ZS-001 quarantined; re-coded C-ZX-001~010 / C-ZX-001E~010E submitted.

## 4. Verification

- verify_hzx_phase20R.py: == RESULT: 31 PASS / 0 FAIL ==
- verify_hzx_landing.py: == RESULT: 26 PASS / 0 FAIL ==

## 5. Record-only (other cards)

- web H-ZZ-166/H-ZZ-222 remap or takedown (web card); H-LJY-001_modes.json:478 and H-PGR-001.json cross-reference checks (other cards).
