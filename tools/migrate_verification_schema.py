#!/usr/bin/env python3
"""Verification schema migration for modes_data.json.

Adds `verification` field to each mode with default status `pending`.
Idempotent: can be re-run safely (skips modes that already have verification).
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = REPO_ROOT / "data" / "modes_data.json"
BACKUP_PATH = REPO_ROOT / "data" / "modes_data.json.bak"

DEFAULT_VERIFICATION = {
    "status": "pending",
    "method": "auto-scan",
    "evidence": "",
    "checked_at": date.today().isoformat(),
    "checker": "migration"
}

def load_data() -> dict:
    """Load modes_data.json."""
    with DATA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data: dict) -> None:
    """Save modes_data.json with backup."""
    DATA_PATH.rename(BACKUP_PATH)
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_verification_to_modes(modes: list) -> tuple[int, int]:
    """Add verification to a list of mode objects. Returns (updated, skipped)."""
    updated = 0
    skipped = 0
    for mode in modes:
        if not isinstance(mode, dict):
            continue
        if "verification" in mode:
            skipped += 1
            continue
        mode["verification"] = DEFAULT_VERIFICATION.copy()
        updated += 1
    return updated, skipped

def migrate() -> tuple[int, int]:
    """Run migration on all mode arrays in the data. Returns (total_updated, total_skipped)."""
    data = load_data()
    total_updated = 0
    total_skipped = 0

    # 1. Top-level "modes" array (main mode repository: 2868 modes)
    if "modes" in data and isinstance(data["modes"], list):
        updated, skipped = add_verification_to_modes(data["modes"])
        total_updated += updated
        total_skipped += skipped
        print(f"  Top-level modes array: {updated} updated, {skipped} skipped")

    # 2. Check each figure object for "modes" arrays
    for key, value in data.items():
        if not isinstance(value, dict):
            continue
        # Skip the first figure's inline fields (they don't have modes array)
        # Check for "modes" array in figure objects
        if "modes" in value and isinstance(value["modes"], list):
            updated, skipped = add_verification_to_modes(value["modes"])
            total_updated += updated
            total_skipped += skipped
            print(f"  Figure {key} modes array: {updated} updated, {skipped} skipped")

    if total_updated > 0:
        save_data(data)
        print(f"[OK] Migration complete: {total_updated} modes updated, {total_skipped} already had verification")
    else:
        print(f"[OK] Migration complete: no changes needed ({total_skipped} modes already had verification)")

    return total_updated, total_skipped

def verify() -> bool:
    """Verify migration result."""
    data = load_data()
    total_modes = 0
    with_verification = 0
    statuses = {}

    # Check top-level modes
    if "modes" in data and isinstance(data["modes"], list):
        for mode in data["modes"]:
            if not isinstance(mode, dict):
                continue
            total_modes += 1
            ver = mode.get("verification")
            if isinstance(ver, dict) and "status" in ver:
                with_verification += 1
                status = ver.get("status", "unknown")
                statuses[status] = statuses.get(status, 0) + 1

    # Check figure modes arrays
    for key, value in data.items():
        if not isinstance(value, dict):
            continue
        if "modes" in value and isinstance(value["modes"], list):
            for mode in value["modes"]:
                if not isinstance(mode, dict):
                    continue
                total_modes += 1
                ver = mode.get("verification")
                if isinstance(ver, dict) and "status" in ver:
                    with_verification += 1
                    status = ver.get("status", "unknown")
                    statuses[status] = statuses.get(status, 0) + 1

    print(f"Verification check: {with_verification}/{total_modes} modes have verification field")
    for status, count in sorted(statuses.items()):
        print(f"  {status}: {count}")

    return with_verification == total_modes

def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Add verification schema to modes_data.json")
    parser.add_argument("--verify", action="store_true", help="Only verify, don't migrate")
    args = parser.parse_args()

    if args.verify:
        ok = verify()
        return 0 if ok else 1

    migrate()
    return 0

if __name__ == "__main__":
    sys.exit(main())
