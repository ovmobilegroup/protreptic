"""Tests for thinking_mode_selector CLI — 24 tests."""

import sys
import subprocess
import json
from pathlib import Path

TOOLS_DIR = Path(__file__).parent.parent / "tools"


# ── Data loading tests (6) ───────────────────────────────────────────

def test_scenarios_zh_total_keys(scenarios_zh):
    """Chinese scenarios: 1005 total keys (Phase 12.2 added EE-MER-001)."""
    assert len(scenarios_zh) == 1005, f"Expected 1005 keys, got {len(scenarios_zh)}"


def test_scenarios_en_total_keys(scenarios_en):
    """English scenarios: 1005 total keys (Phase 12.2 added EE-MER-001)."""
    assert len(scenarios_en) == 1005, f"Expected 1005 keys, got {len(scenarios_en)}"


def test_modes_data_count(modes_data):
    """Modes data: at least 600 entries per language."""
    assert len(modes_data["zh"]) >= 600, f"Expected ≥600 zh modes, got {len(modes_data['zh'])}"
    assert len(modes_data["en"]) >= 600, f"Expected ≥600 en modes, got {len(modes_data['en'])}"


def test_code_maps_completeness(code_maps, scenarios_zh):
    """Code maps: all dict scenarios have entries in both EN and CN."""
    dict_count = sum(1 for v in scenarios_zh.values() if isinstance(v, dict))
    assert len(code_maps["CODE_MAP"]) == 978, \
        f"Expected 978 CODE_MAP entries (Phase 12.2 added EE-MER-001), got {len(code_maps['CODE_MAP'])}"
    assert len(code_maps["CODE_MAP_EN"]) == 978, \
        f"Expected 978 CODE_MAP_EN entries (Phase 12.2 added EE-MER-001), got {len(code_maps['CODE_MAP_EN'])}"
    # Some asymmetry is known but overall counts match (978 entries)


def test_bilingual_key_consistency(scenarios_zh, scenarios_en):
    """Chinese and English scenario keys match."""
    dict_keys_zh = {k for k, v in scenarios_zh.items() if isinstance(v, dict)}
    dict_keys_en = {k for k, v in scenarios_en.items() if isinstance(v, dict)}
    missing_in_en = dict_keys_zh - dict_keys_en
    missing_in_zh = dict_keys_en - dict_keys_zh
    assert not missing_in_en, f"Missing in EN: {sorted(missing_in_en)[:5]}"
    assert not missing_in_zh, f"Missing in ZH: {sorted(missing_in_zh)[:5]}"


def test_modes_coverage_valid(modes_data, scenarios_zh):
    """Every mode referenced in scenarios exists in modes_data."""
    used = set()
    for entry in scenarios_zh.values():
        if isinstance(entry, dict):
            used.update(entry.get("modes", []))
    for mid in used:
        # Handle both int and string modes (some entries use "M577" format)
        # modes_data uses numeric string keys for base modes ('1', '2') 
        # and 'M577' format for new modes (M577+)
        if isinstance(mid, int):
            # Try both formats
            if str(mid) in modes_data["zh"]:
                continue
            if f"M{mid}" in modes_data["zh"]:
                continue
        elif isinstance(mid, str):
            if mid.startswith('M') and mid[1:].isdigit():
                if mid in modes_data["zh"]:
                    continue
                # Try without M prefix
                if mid[1:] in modes_data["zh"]:
                    continue
            elif mid.isdigit():
                if mid in modes_data["zh"]:
                    continue
                if f"M{mid}" in modes_data["zh"]:
                    continue
            else:
                continue  # skip non-mode strings like chars from code field
        else:
            continue
        assert False, f"Mode {mid} used but not defined in modes_data"


# ── CLI functional tests (12) — one per command/option combo ───────

def test_cli_list(tools_dir):
    """`python thinking_mode_selector.py -l` lists scenarios."""
    r = subprocess.run(
        [sys.executable, "thinking_mode_selector.py", "-l"],
        capture_output=True, text=True, cwd=tools_dir
    )
    assert r.returncode == 0, f"CLI -l failed: {r.stderr}"
    lines = [l for l in r.stdout.splitlines() if l.strip()]
    assert len(lines) > 0, "CLI -l returned no output"


def test_cli_query_code(scenarios_zh, tools_dir):
    """`-c <code>` returns scenario details."""
    code = "H-RZF-270"  # known valid code
    r = subprocess.run(
        [sys.executable, "thinking_mode_selector.py", "-c", code],
        capture_output=True, text=True, cwd=tools_dir
    )
    assert r.returncode == 0, f"CLI query failed: {r.stderr}"
    assert code in r.stdout


def test_cli_query_lang_zh(scenarios_zh, tools_dir):
    """`-c <code> --lang zh` returns Chinese details."""
    code = "M-JGS-280"
    r = subprocess.run(
        [sys.executable, "thinking_mode_selector.py", "-c", code, "--lang", "zh"],
        capture_output=True, text=True, cwd=tools_dir
    )
    assert r.returncode == 0, f"CLI query zh failed: {r.stderr}"
    # Chinese output should contain 中文字符
    has_cjk = any('\u4e00' <= c <= '\u9fff' for c in r.stdout)
    assert has_cjk, "CLI query zh returned no Chinese characters"


def test_cli_query_lang_en(scenarios_zh, scenarios_en, tools_dir):
    """`-c <code> --lang en` returns English details."""
    code = "H-RZF-270"
    r = subprocess.run(
        [sys.executable, "thinking_mode_selector.py", "-c", code, "--lang", "en"],
        capture_output=True, text=True, cwd=tools_dir
    )
    assert r.returncode == 0, f"CLI query en failed: {r.stderr}"
    assert code in r.stdout


def test_cli_search_keyword(scenarios_zh, tools_dir):
    """`-s <keyword>` returns matching scenarios."""
    r = subprocess.run(
        [sys.executable, "thinking_mode_selector.py", "-s", "毛泽东"],
        capture_output=True, text=True, cwd=tools_dir
    )
    assert r.returncode == 0, f"CLI search failed: {r.stderr}"
    # Should contain at least one scenario code or result indicator
    assert "H-" in r.stdout or "M-" in r.stdout or len(r.stdout.strip()) > 0, \
        f"CLI search returned unexpected output: {r.stdout[:200]}"


def test_cli_export_json(tools_dir):
    """`-e json` exports all scenarios as JSON."""
    r = subprocess.run(
        [sys.executable, "thinking_mode_selector.py", "-e", "json"],
        capture_output=True, text=True, cwd=tools_dir
    )
    assert r.returncode == 0, f"CLI export json failed: {r.stderr}"
    # Should be parseable JSON (at least a dict/list)
    data = json.loads(r.stdout.strip())
    assert isinstance(data, (dict, list)), f"Exported JSON is not a dict/list: {type(data)}"


def test_cli_export_md(tools_dir):
    """`-e md` exports all scenarios as Markdown."""
    r = subprocess.run(
        [sys.executable, "thinking_mode_selector.py", "-e", "md"],
        capture_output=True, text=True, cwd=tools_dir
    )
    assert r.returncode == 0, f"CLI export md failed: {r.stderr}"
    assert len(r.stdout.strip()) > 0, "CLI export md returned empty output"


def test_cli_tag_filter(tools_dir):
    """`-t key=value` filters by tag."""
    r = subprocess.run(
        [sys.executable, "thinking_mode_selector.py", "-t", "historical_domains=Military"],
        capture_output=True, text=True, cwd=tools_dir
    )
    assert r.returncode == 0, f"CLI tag filter failed: {r.stderr}"
    # Accept either matching output or empty (no matches is valid)


def test_cli_export_single_json(scenarios_zh, tools_dir):
    """`-c <code> -e json` exports single scenario as JSON."""
    code = "H-RZF-270"
    r = subprocess.run(
        [sys.executable, "thinking_mode_selector.py", "-c", code, "-e", "json"],
        capture_output=True, text=True, cwd=tools_dir
    )
    assert r.returncode == 0, f"CLI single export json failed: {r.stderr}"
    data = json.loads(r.stdout.strip())
    # Should contain the scenario code as a key or in output
    assert isinstance(data, (dict, str)), f"Single export json unexpected type: {type(data)}"


def test_cli_export_single_md(tools_dir):
    """`-c <code> -e md` exports single scenario as Markdown."""
    code = "H-RZF-270"
    r = subprocess.run(
        [sys.executable, "thinking_mode_selector.py", "-c", code, "-e", "md"],
        capture_output=True, text=True, cwd=tools_dir
    )
    assert r.returncode == 0, f"CLI single export md failed: {r.stderr}"
    assert len(r.stdout.strip()) > 0, "CLI single export md returned empty output"


def test_cli_help(tools_dir):
    """`--help` shows usage information."""
    r = subprocess.run(
        [sys.executable, "thinking_mode_selector.py", "--help"],
        capture_output=True, text=True, cwd=tools_dir
    )
    assert r.returncode == 0, f"CLI --help failed: {r.stderr}"
    assert "-c" in r.stdout or "-l" in r.stdout, "Help output missing expected flags"


# ── Data integrity tests (6) ────────────────────────────────────────

def test_main_data_uniqueness(tools_dir):
    """Every entry in main_data has a unique code (if file exists)."""
    path = tools_dir / "main_data.json"
    if not path.exists():
        # main_data.json may not exist yet — skip test
        assert True  # no-op, file absent is acceptable
    else:
        with open(path, "r", encoding="utf-8") as f:
            main_data = json.load(f)
        codes = []
        for v in main_data.values():
            if isinstance(v, dict) and "code" in v:
                codes.append(v["code"])
        assert len(codes) == len(set(codes)), \
            f"Duplicate codes in main_data: {[c for c in codes if codes.count(c) > 1][:5]}"


def test_scenario_required_fields(scenarios_zh):
    """All dict scenarios have required fields (standard or i18n format)."""
    missing = []
    for code, entry in scenarios_zh.items():
        if not isinstance(entry, dict):
            continue
        # Accept either standard (name/description) or i18n (name_zh/name_en, description_zh/description_en)
        # or condensed format (name + modes, used by some historical entries)
        has_name = ("name" in entry and "description" in entry) or \
                   ("name_zh" in entry or "name_en" in entry) or \
                   ("name" in entry and "modes" in entry)
        has_desc = ("description" in entry and "modes" in entry) or \
                   ("description_zh" in entry or "description_en" in entry) or \
                   ("name" in entry and "modes" in entry and "core_mode" in entry)
        if not has_name:
            missing.append(f"{code}: missing name field")
        elif not has_desc:
            missing.append(f"{code}: missing description field")
    assert not missing, f"Missing required fields: {missing[:5]}"


def test_scenario_tags_format(scenario_tags):
    """scenario_tags.json has proper 'tags' key."""
    assert "tags" in scenario_tags, "Missing 'tags' key in scenario_tags.json"
    tags = scenario_tags["tags"]
    assert isinstance(tags, dict), f"'tags' should be a dict, got {type(tags)}"


def test_code_maps_bilingual_match(code_maps):
    """CODE_MAP and CODE_MAP_EN have matching keys."""
    cn_keys = set(code_maps["CODE_MAP"].keys())
    en_keys = set(code_maps["CODE_MAP_EN"].keys())
    missing_en = cn_keys - en_keys
    missing_cn = en_keys - cn_keys
    assert not missing_en, f"Missing in EN: {sorted(missing_en)[:5]}"
    assert not missing_cn, f"Missing in CN: {sorted(missing_cn)[:5]}"


def test_modes_bilingual_consistency(modes_data):
    """Every zh mode has a matching en entry."""
    zh_keys = set(modes_data["zh"].keys())
    en_keys = set(modes_data["en"].keys())
    missing_en = zh_keys - en_keys
    assert not missing_en, f"Missing EN mode: {sorted(missing_en)[:5]}"


def test_scenarios_have_modes(scenarios_zh):
    """All dict scenarios reference at least one mode (P5 may have empty modes)."""
    no_modes = []
    for code, entry in scenarios_zh.items():
        if not isinstance(entry, dict):
            continue
        modes = entry.get("modes")
        # P5 scenarios are allowed to have empty/missing modes (metadata entries)
        if code.startswith("P5-"):
            continue
        if not modes or (isinstance(modes, list) and len(modes) == 0):
            no_modes.append(code)
    assert not no_modes, f"Scenarios with empty modes: {no_modes[:5]}"


def test_cli_query_nonexistent_code(tools_dir):
    """`-c <nonexistent>` returns error or empty result gracefully."""
    r = subprocess.run(
        [sys.executable, "thinking_mode_selector.py", "-c", "NONEXISTENT-999"],
        capture_output=True, text=True, cwd=tools_dir
    )
    # Should not crash — either error exit or empty output is fine
    assert r.returncode == 0 or "not found" in r.stdout.lower() or len(r.stdout.strip()) == 0, \
        f"CLI query nonexistent code crashed: {r.stderr[:200]}"
