import json
from pathlib import Path

import pytest
from chickflow.data.schema import load_clean_bundle
from chickflow.metrics import build_facts

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def facts():
    return build_facts(load_clean_bundle(ROOT/"data/clean"))


@pytest.fixture(scope="session")
def manifest():
    return json.loads((ROOT/"data/manifest.json").read_text())
