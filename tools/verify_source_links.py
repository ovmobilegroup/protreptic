#!/usr/bin/env python3
"""Verify source_links.json URLs with curl (HTTP 200 check)."""

import json
import subprocess
import sys
from pathlib import Path

LINKS_PATH = Path(__file__).resolve().parent.parent / "data" / "source_links.json"

def check_url(url: str) -> tuple[bool, int]:
    """Check if URL returns 200. Returns (success, status_code)."""
    if not url:
        return False, 0
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", "10", url],
            capture_output=True,
            text=True,
            timeout=15
        )
        status = int(result.stdout.strip()) if result.stdout.strip().isdigit() else 0
        return status == 200, status
    except Exception as e:
        return False, 0

def main() -> int:
    with LINKS_PATH.open("r", encoding="utf-8") as f:
        links = json.load(f)

    print(f"Checking {len(links)} source links...")
    ok = 0
    failed = 0
    unverifiable = 0

    for source, info in links.items():
        url = info.get("url", "")
        source_type = info.get("source_type", "unknown")
        confidence = info.get("confidence", 0)

        if source_type == "unverifiable" or not url:
            print(f"  [UNVERIFIABLE] {source} (type={source_type})")
            unverifiable += 1
            continue

        success, status = check_url(url)
        if success:
            print(f"  [OK 200] {source} -> {url}")
            ok += 1
        else:
            print(f"  [FAIL {status}] {source} -> {url}")
            failed += 1

    print(f"\nSummary: {ok} OK, {failed} failed, {unverifiable} unverifiable")
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
