"""Shared pytest fixtures for cli_tests."""
import sys
import os
import json
from pathlib import Path

import pytest

TOOLS_DIR = Path(__file__).parent.parent / "tools"


@pytest.fixture(scope="session")
def tools_dir():
    return TOOLS_DIR


@pytest.fixture(scope="session")
def scenarios_zh(tools_dir):
    path = tools_dir / "scenarios_zh.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def scenarios_en(tools_dir):
    path = tools_dir / "scenarios_en.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def code_maps(tools_dir):
    path = tools_dir / "code_maps.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def modes_data(tools_dir):
    path = tools_dir / "modes_data.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def scenario_tags(tools_dir):
    path = tools_dir / "scenario_tags.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def main_data(tools_dir):
    path = tools_dir / "json" / "main_data.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
