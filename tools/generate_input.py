#!/usr/bin/env python3
"""Generate batch_new_figures_research.md from candidate JSON files.

Reads batch2_candidates.json and batch3_candidates.json, combines them into
a single JSON array and writes it as docs/research/batch_new_figures_research.md.
This file is the expected input for import_batch_56.py.
"""

import json
import os
import sys

PROJECT = "/opt/data/workspace/Protreptic"

def main():
    batch2_path = os.path.join(PROJECT, "tools", "batch2_candidates.json")
    batch3_path = os.path.join(PROJECT, "tools", "batch3_candidates.json")

    all_figures = []
    for path in [batch2_path, batch3_path]:
        if not os.path.exists(path):
            print(f"WARNING: {path} not found, skipping")
            continue
        with open(path) as f:
            data = json.load(f)
        all_figures.extend(data)

    # Sort by code to maintain consistent ordering
    all_figures.sort(key=lambda x: x.get("code", ""))

    output_dir = os.path.join(PROJECT, "docs", "research")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "batch_new_figures_research.md")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_figures, f, ensure_ascii=False, indent=2)

    print(f"Generated {output_path} with {len(all_figures)} figures")
    codes = [fig["code"] for fig in all_figures]
    print(f"Ccodes: {', '.join(codes)}")

if __name__ == "__main__":
    main()