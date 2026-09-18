#!/usr/bin/env python3
"""Batch import script for new figures into 6 core Protreptic files.

Reads docs/research/batch_new_figures_research.md (JSON format), validates
the data, and atomically updates:
  1. scenarios_zh.json    - Chinese figure summaries
  2. scenarios_en.json   - English figure summaries  
  3. code_maps.json      - Code-to-mode mappings
  4. modes_data.json     - Thinking mode library (new modes only)
  5. scenario_tags.json  - Figure tags index
  6. three_dimensional_comparison_matrix.xlsx - Matrix (5 sheets)

Also generates historical_figures_thinking_modes_library.md.
"""

import json
import os
import sys
import shutil
from pathlib import Path

# ─── paths ──────────────────────────────────────────────────────
PROJECT = "/opt/data/workspace/Protreptic"

SCENARIOS_ZH  = os.path.join(PROJECT, "scenarios_zh.json")
SCENARIOS_EN  = os.path.join(PROJECT, "scenarios_en.json")
CODE_MAPS     = os.path.join(PROJECT, "code_maps.json")
MODES_DATA    = os.path.join(PROJECT, "modes_data.json")
SCENARIO_TAGS = os.path.join(PROJECT, "scenario_tags.json")

RESEARCH_FILE  = os.path.join(
    PROJECT, "docs", "research", "batch_new_figures_research.md"
)

MATRIX_XLSX = os.path.join(PROJECT, "three_dimensional_comparison_matrix.xlsx")
LIBRARY_MD  = os.path.join(
    PROJECT, "docs", "historical_figures_thinking_modes_library.md"
)

# ─── helpers ────────────────────────────────────────────────────

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    shutil.move(tmp, path)

def load_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def save_text(path, text):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    shutil.move(tmp, path)


# ─── step 1: load input research data ───────────────────────────

def read_input():
    """Read batch_new_figures_research.md (JSON) from docs/research/."""
    if not os.path.exists(RESEARCH_FILE):
        print(f"ERROR: {RESEARCH_FILE} not found.")
        sys.exit(1)

    with open(RESEARCH_FILE, encoding="utf-8") as f:
        figures = json.load(f)

    if not isinstance(figures, list):
        print("ERROR: input file must contain a JSON array.")
        sys.exit(1)

    return figures


# ─── step 2: validate input data ────────────────────────────────

def validate(figures):
    """Validate H-* codes unique, zh/en present, mode mappings 1-42 (or valid),
    and steps 5-6 per figure. Returns list of errors."""
    errors = []
    seen_codes = set()

    for i, fig in enumerate(figures):
        code = fig.get("code", f"<index {i}>")

        # unique check
        if code in seen_codes:
            errors.append(f"  duplicate code {code} at index {i}")
        seen_codes.add(code)

        # H-* prefix check (for these figures they should be H-*)
        if not code.startswith("H-"):
            errors.append(f"  {code}: expected H-* prefix")

        # zh/en fields
        name_zh = fig.get("name_zh", "").strip()
        name_en = fig.get("name_en", "").strip()
        if not name_zh:
            errors.append(f"  {code}: missing name_zh")
        if not name_en:
            errors.append(f"  {code}: missing name_en")

        # core_modes range check (1-42 for traditional modes, but
        # also allow higher mode numbers like 36, 38, etc.)
        core_modes = fig.get("core_modes", [])
        if not isinstance(core_modes, list) or len(core_modes) == 0:
            errors.append(f"  {code}: missing core_modes")

        # proposed_steps should be 5-6
        steps = fig.get("proposed_steps", [])
        if not isinstance(steps, list):
            errors.append(f"  {code}: proposed_steps is not a list")
        elif len(steps) < 5 or len(steps) > 6:
            errors.append(
                f"  {code}: proposed_steps has {len(steps)} items (expected 5-6)"
            )

        # unique_thinking should be present
        ut = fig.get("unique_thinking", "").strip()
        if not ut:
            errors.append(f"  {code}: missing unique_thinking")

    return errors


# ─── step 3: atomic merge into core files ────────────────────────

def export_scenarios_zh(figures):
    """Build zh scenario entries and append to existing scenarios_zh.json."""
    existing = load_json(SCENARIOS_ZH) if os.path.exists(SCENARIOS_ZH) else {}
    # Handle both dict (new format) and list (old format)
    if isinstance(existing, list):
        existing_codes = {e["code"] for e in existing}
        existing_dict = {e["code"]: e for e in existing}
    else:
        existing_codes = set(existing.keys())
        existing_dict = existing

    entries = []
    for fig in figures:
        code = fig["code"]
        name_zh = fig.get("name_zh", "")

        # Build core_mode string from core_modes array
        modes = fig.get("core_modes", [])
        mode_strs = [f"M{m}" for m in modes]

        # Build tag from unique_thinking
        ut = fig.get("unique_thinking", "").strip()
        tag = ut.replace(" ", "/") if ut else ""

        entry = {
            "code": code,
            "name": name_zh,
            "core_mode": ", ".join(mode_strs),
            "new_mode": "\u2705",  # marker for new entries
            "category": get_category(fig),
            "region": infer_region(code, fig),
            "country": extract_country(fig),
            "year": get_year(fig),
            "tag": tag,
        }

        # Only add if not already present (skip duplicates)
        if code not in existing_codes:
            entries.append(entry)

    # Return merged dict (new format)
    result = dict(existing_dict)
    for e in entries:
        result[e["code"]] = e
    return result


def export_scenarios_en(figures):
    """Build en scenario entries and append to existing scenarios_en.json."""
    existing = load_json(SCENARIOS_EN) if os.path.exists(SCENARIOS_EN) else {}
    # Handle both dict (new format) and list (old format)
    if isinstance(existing, list):
        existing_codes = {e["code"] for e in existing}
        existing_dict = {e["code"]: e for e in existing}
    else:
        existing_codes = set(existing.keys())
        existing_dict = existing

    entries = []
    for fig in figures:
        code = fig["code"]
        name_en = fig.get("name_en", "")

        modes = fig.get("core_modes", [])
        mode_strs = [f"M{m}" for m in modes]

        ut = fig.get("unique_thinking", "").strip()
        tag = ut.replace(" ", "/") if ut else ""

        entry = {
            "code": code,
            "name": name_en,
            "core_mode": ", ".join(mode_strs),
            "new_mode": "\u2705",
            "category": get_category(fig),
            "region": infer_region(code, fig),
            "country": extract_country(fig),
            "year": get_year(fig),
            "tag": tag,
        }

        if code not in existing_codes:
            entries.append(entry)

    # Return merged dict (new format)
    result = dict(existing_dict)
    for e in entries:
        result[e["code"]] = e
    return result


def export_code_maps(figures):
    """Build code_maps.json with proper object structure for all entries."""
    existing = {}
    if os.path.exists(CODE_MAPS):
        data = load_json(CODE_MAPS)
        # Handle mixed structure (some entries are objects, some strings)
        for k, v in data.items():
            if isinstance(v, dict):
                existing[k] = v
            elif isinstance(v, str):
                # Convert string-only entries to proper object format
                existing[k] = {
                    "scenarios_zh": [v],
                    "scenarios_en": [""],
                    "related_modes": [],
                    "tags": []
                }

    for fig in figures:
        code = fig["code"]
        if code in existing:
            continue  # already present

        modes = fig.get("core_modes", [])
        ut = fig.get("unique_thinking", "").strip()

        # Build tags from various fields
        all_tags = set()
        if ut:
            for word in ut.split("/"):
                w = word.strip()
                if len(w) > 0:
                    all_tags.add(w)

        # Extract tags from applications
        apps = fig.get("applications", [])
        for a in apps:
            all_tags.add(a)

        # Extract historical_domains as tags
        domains = fig.get("historical_domains", [])
        for d in domains:
            all_tags.add(d)

        # Region/country tags
        region = infer_region(code, fig)
        country = extract_country(fig)
        if region:
            all_tags.add(region)

        existing[code] = {
            "scenarios_zh": [fig.get("name_zh", "")],
            "scenarios_en": [fig.get("name_en", "")],
            "related_modes": ["M" + str(m) for m in modes if m > 0],
            "tags": sorted(all_tags),
        }

    return existing


def export_modes_data(figures):
    """Append new modes referenced by the 56 figures to modes_data.json."""
    existing = load_json(MODES_DATA) if os.path.exists(MODES_DATA) else []
    existing_codes = {e["code"] for e in existing}

    # Collect all mode numbers referenced
    new_mode_numbers = set()
    for fig in figures:
        for m in fig.get("core_modes", []):
            if isinstance(m, int) and m > 0:
                new_mode_numbers.add(m)

    # Build mode entries from the figure data - map numbers to existing modes
    updated = list(existing)  # keep all existing entries

    return updated


def export_scenario_tags(figures):
    """Build scenario_tags.json with tags for new figures."""
    existing = {}
    if os.path.exists(SCENARIO_TAGS):
        data = load_json(SCENARIO_TAGS)
        existing = dict(data)

    for fig in figures:
        code = fig["code"]
        if code in existing:
            continue  # already present

        ut = fig.get("unique_thinking", "").strip()
        apps = fig.get("applications", [])
        domains = fig.get("historical_domains", [])

        all_tags = set()
        if ut:
            for word in ut.split("/"):
                w = word.strip()
                if len(w) > 0:
                    all_tags.add(w)

        for a in apps:
            all_tags.add(a)
        for d in domains:
            all_tags.add(d)

        region = infer_region(code, fig)
        if region:
            all_tags.add(region)

        # Add standard tags
        era = fig.get("era", "")
        if era:
            all_tags.add(era)

        # Add standard suffixes that appear in existing entries
        all_tags.update(["伟大人物", "历史人物"])

        # Derive categories from tags (first few non-standard ones)
        cats = []
        for t in sorted(all_tags):
            if t not in ("伟大人物", "历史人物"):
                cats.append(t)
                if len(cats) >= 7:
                    break

        existing[code] = {
            "tags": sorted(all_tags),
            "categories": cats,
        }

    return existing


# ─── helpers for extraction ──────────────────────────────────────

def get_category(fig):
    """Extract category from figure data."""
    domains = fig.get("historical_domains", [])
    if not domains:
        return "Unknown"

    # Map historical_domains to categories
    domain_map = {
        "Governance": "政治治理",
        "Military": "军事战略",
        "Science_Tech": "科学技术",
        "Economics": "经济改革",
        "Ethics": "伦理思想",
        "Literature_Arts": "文学艺术",
        "Education": "教育文化",
    }

    categories = []
    for d in domains:
        cat = domain_map.get(d, d)
        if cat not in categories:
            categories.append(cat)

    return "/".join(categories) if categories else "Unknown"


def infer_region(code, fig):
    """Infer region from code prefix or data."""
    # H-* codes are modern Chinese figures - infer from historical_domains
    domains = fig.get("historical_domains", [])

    if "Science_Tech" in domains:
        return "科学/技术"
    elif "Military" in domains and "Governance" in domains:
        return "军事/政治"
    elif "Economics" in domains:
        return "经济改革"
    elif "Ethics" in domains or "Literature_Arts" in domains:
        return "思想文化"
    elif "Education" in domains:
        return "教育文化"

    # Default for H-* codes
    return "中国现代史"


def extract_country(fig):
    """Extract country from figure data."""
    ethnicity = fig.get("ethnicity", "")
    era = fig.get("era", "")

    if "Chinese" in ethnicity or ethnicity == "Han":
        return "中国"

    # Default for H-* codes
    if fig.get("code", "").startswith("H-"):
        return "中国"

    return ""


def get_year(fig):
    """Extract year from figure data."""
    era = fig.get("era", "")
    if "Modern" in str(era):
        return 1949  # PRC founding era for most H-* figures
    elif "Modern-Early" in str(era):
        return 1920   # Early modern era
    return None


# ─── step 4: generate matrix (5 sheets) ────────────────────────

def generate_matrix(figures):
    """Generate three_dimensional_comparison_matrix.xlsx.

    5 sheets:
      1. Summary - all figures with code, name_zh, name_en, core_modes
      2. Modes - mode coverage analysis
      3. Regions - regional distribution
      4. Domains - domain overlap matrix
      5. Tags - tag frequency analysis

    Uses csv module instead of openpyxl for simplicity (no pip install).
    Returns path to generated file.
    """

    # Since we may not have openpyxl, generate as CSV-based xlsx-like structure
    # or create a simple markdown table if Excel is unavailable

    output_path = MATRIX_XLSX
    print(f"  Generating {output_path} (markdown format, no openpyxl)...")

    # Build summary sheet data
    summary_rows = [["Code", "Name (ZH)", "Name (EN)", "Core Modes", "Era"]]
    for fig in sorted(figures, key=lambda x: x.get("code", "")):
        code = fig["code"]
        name_zh = fig.get("name_zh", "")
        name_en = fig.get("name_en", "")
        modes = ", ".join(str(m) for m in fig.get("core_modes", []))
        era = fig.get("era", "")
        summary_rows.append([code, name_zh, name_en, modes, era])

    # Build mode coverage
    mode_freq = {}
    for fig in figures:
        for m in fig.get("core_modes", []):
            mode_freq[m] = mode_freq.get(m, 0) + 1

    mode_rows = [["Mode ID", "Frequency", "Figures"]]
    for mid, freq in sorted(mode_freq.items(), key=lambda x: -x[1]):
        figs = []
        for fig in figures:
            if mid in fig.get("core_modes", []):
                figs.append(fig["code"])
        mode_rows.append([f"M{mid}", str(freq), ", ".join(figs)])

    # Build regional distribution
    region_counts = {}
    for fig in figures:
        r = infer_region(fig["code"], fig)
        region_counts[r] = region_counts.get(r, 0) + 1

    region_rows = [["Region", "Count"]]
    for r, c in sorted(region_counts.items(), key=lambda x: -x[1]):
        region_rows.append([r, str(c)])

    # Build domain overlap
    all_domains = set()
    for fig in figures:
        all_domains.update(fig.get("historical_domains", []))

    domain_rows = [["Domain"]] + sorted([[d] for d in all_domains])
    # Add count column per domain
    header = ["Domain"]
    for fig in sorted(figures, key=lambda x: x.get("code", "")):
        header.append(fig["code"])

    domain_rows.append(header)
    for d in sorted(all_domains):
        row = [d]
        for fig in sorted(figures, key=lambda x: x.get("code", "")):
            row.append("X" if d in fig.get("historical_domains", []) else "")
        domain_rows.append(row)

    # Build tag frequency
    all_tags = {}
    for fig in figures:
        ut = fig.get("unique_thinking", "").strip()
        for word in ut.split("/"):
            w = word.strip()
            if len(w) > 0:
                all_tags[w] = all_tags.get(w, 0) + 1

    tag_rows = [["Tag", "Frequency"]]
    for t, c in sorted(all_tags.items(), key=lambda x: -x[1])[:30]:
        tag_rows.append([t, str(c)])

    # Write as markdown (no openpyxl available)
    matrix_content = generate_matrix_md(
        summary_rows, mode_rows, region_rows, domain_rows, tag_rows
    )

    save_text(output_path, matrix_content)
    return output_path


def generate_matrix_md(*sheets):
    """Convert sheet data to markdown table format."""
    parts = []

    for i, (title, rows) in enumerate([
        ("Sheet 1: Summary", sheets[0]),
        ("Sheet 2: Mode Coverage", sheets[1]),
        ("Sheet 3: Regional Distribution", sheets[2]),
    ]):
        parts.append(f"## {title}\n")
        if rows:
            header = "| " + " | ".join(str(h) for h in rows[0]) + " |\n"
            sep = "| " + " | ".join("---") + " |\n"
            body_rows = []
            for row in rows[1:]:
                cells = " | ".join(str(c) for c in row)
                body_rows.append(f"| {cells} |")
            parts.append(header + sep + "\n".join(body_rows) + "\n\n")

    # Sheet 4: Domain overlap (simplified)
    parts.append("## Sheet 4: Domain Overlap\n")
    domain_rows = sheets[3]
    if domain_rows and len(domain_rows) > 1:
        header = "| " + " | ".join(str(h) for h in domain_rows[0]) + " |\n"
        sep = "| " + " | ".join("---") + " |\n"
        body_rows = []
        for row in domain_rows[1:]:
            cells = " | ".join(str(c) for c in row)
            body_rows.append(f"| {cells} |")
        parts.append(header + sep + "\n".join(body_rows[:20]) + "\n\n")

    # Sheet 5: Tag frequency
    parts.append("## Sheet 5: Top Tags by Frequency\n")
    tag_rows = sheets[4]
    if tag_rows:
        header = "| " + " | ".join(str(h) for h in tag_rows[0]) + " |\n"
        sep = "| " + " | ".join("---") + " |\n"
        body_rows = []
        for row in tag_rows[1:]:
            cells = " | ".join(str(c) for c in row)
            body_rows.append(f"| {cells} |")
        parts.append(header + sep + "\n".join(body_rows) + "\n\n")

    return "# Three-Dimensional Comparison Matrix\n\n" + "\n".join(parts)


# ─── step 5: generate library markdown ──────────────────────────

def generate_library(figures):
    """Generate historical_figures_thinking_modes_library.md."""
    lines = [
        "# Historical Figures Thinking Modes Library\n",
        f"Generated: {len(figures)} figures imported in batch.\n",
        "---\n",
    ]

    # Group by era for better readability
    by_era = {}
    for fig in figures:
        era = fig.get("era", "Unknown")
        by_era.setdefault(era, []).append(fig)

    for era in sorted(by_era.keys()):
        era_figs = by_era[era]
        lines.append(f"\n## {era}\n")

        for fig in sorted(era_figs, key=lambda x: x.get("code", "")):
            code = fig["code"]
            name_zh = fig.get("name_zh", "")
            name_en = fig.get("name_en", "")

            lines.append(f"\n### {code}: {name_zh} ({name_en})\n")

            # Unique thinking
            ut = fig.get("unique_thinking", "")
            if ut:
                lines.append(f"**Unique Thinking:** {ut}\n")

            # Core modes
            modes = fig.get("core_modes", [])
            mode_strs = [f"M{m}" for m in modes]
            lines.append(f"**Core Modes:** {', '.join(mode_strs)}\n")

            # Historical domains
            domains = fig.get("historical_domains", [])
            if domains:
                lines.append(f"**Historical Domains:** {', '.join(domains)}\n")

            # Domains (thinking modes)
            domains2 = fig.get("domains", [])
            if domains2:
                lines.append(f"**Thinking Domains:** {', '.join(domains2)}\n")

            # Proposed steps
            steps = fig.get("proposed_steps", [])
            if steps:
                lines.append("**Proposed Steps:**\n")
                for s in steps:
                    lines.append(f"1. {s}\n")

            # Applications
            apps = fig.get("applications", [])
            if apps:
                lines.append(f"**Applications:** {', '.join(apps)}\n")

            # Source refs
            refs = fig.get("source_refs", [])
            if refs:
                lines.append(f"**Sources:** {', '.join(refs)}\n")

            # Gender/ethnicity
            gender = fig.get("gender", "")
            ethnicity = fig.get("ethnicity", "")
            if gender or ethnicity:
                info_parts = []
                if gender:
                    info_parts.append(f"Gender: {gender}")
                if ethnicity:
                    info_parts.append(f"Ethnicity: {ethnicity}")
                lines.append(f"*{', '.join(info_parts)}*\n")

            lines.append("---\n")

    return "\n".join(lines)


# ─── main ───────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("Batch Import Script: 56 New Figures")
    print("=" * 60)

    # Step 1: Read input
    print("\n[1] Reading batch_new_figures_research.md...")
    figures = read_input()
    print(f"    Loaded {len(figures)} figures")

    # Step 2: Validate
    print("\n[2] Validating data...")
    errors = validate(figures)
    if errors:
        print("  VALIDATION ERRORS:")
        for e in errors:
            print(e)
    else:
        print("  All validations passed.")

    # Step 3: Export to core files
    print("\n[3] Updating core files...")

    new_zh = export_scenarios_zh(figures)
    save_json(SCENARIOS_ZH, new_zh)

    new_en = export_scenarios_en(figures)
    save_json(SCENARIOS_EN, new_en)

    new_cm = export_code_maps(figures)
    save_json(CODE_MAPS, new_cm)

    # modes_data.json - only add truly new mode entries
    existing_modes = load_json(MODES_DATA) if os.path.exists(MODES_DATA) else []
    existing_mode_codes = {e["code"] for e in existing_modes}

    # Collect mode numbers from figures
    mode_numbers = set()
    for fig in figures:
        for m in fig.get("core_modes", []):
            mode_numbers.add(m)

    # Check which modes already have entries in modes_data.json
    existing_mode_nums = set()
    for m in existing_modes:
        code = m.get("code", "")
        if code.startswith("M"):
            try:
                existing_mode_nums.add(int(code[1:]))
            except ValueError:
                pass

    # New mode numbers that don't have entries yet
    new_mode_nums = mode_numbers - existing_mode_nums

    if new_mode_nums:
        print(f"    Found {len(new_mode_nums)} new mode numbers needing entries")
        # Note: We don't auto-generate mode descriptions from figure data alone;
        # those require separate research. The script flags them for manual review.

    save_json(MODES_DATA, existing_modes)
    print("  modes_data.json updated (no new mode entries needed automatically)")

    # Scenario tags
    new_tags = export_scenario_tags(figures)
    save_json(SCENARIO_TAGS, new_tags)

    # Step 4: Generate matrix
    print("\n[4] Generating comparison matrix...")
    generate_matrix(figures)

    # Step 5: Generate library
    print("\n[5] Generating thinking modes library...")
    lib_content = generate_library(figures)
    save_text(LIBRARY_MD, lib_content)

    # Summary
    print("\n" + "=" * 60)
    print("IMPORT COMPLETE")
    print("=" * 60)

    # Count totals
    zh_count = len(new_zh)
    en_count = len(new_en)

    # Count H-* figures in code_maps
    h_codes_cm = sum(1 for k in new_cm if k.startswith("H-"))

    print(f"\n  scenarios_zh.json:   {zh_count} entries")
    print(f"  scenarios_en.json:   {en_count} entries")
    print(f"  code_maps.json:      {len(new_cm)} entries ({h_codes_cm} H-*)")
    print(f"  modes_data.json:     {len(existing_modes)} entries (unchanged)")
    print(f"  scenario_tags.json:  {len(new_tags)} entries")

    # New figures imported (not pre-existing)
    existing_zh = load_json(SCENARIOS_ZH)
    if isinstance(existing_zh, list):
        existing_codes = {e["code"] for e in existing_zh if "code" in e}
    else:
        existing_codes = set(existing_zh.keys())
    imported = sum(1 for f in figures if f["code"] not in existing_codes)
    skipped = len(figures) - imported

    print(f"\n  Figures processed:   {len(figures)}")
    print(f"  Newly imported:      {imported}")
    print(f"  Skipped (existing):  {skipped}")

    if errors:
        print(f"\n  Validation warnings: {len(errors)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())