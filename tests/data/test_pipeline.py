from pathlib import Path

import pytest

from chickflow.data.clean import clean
from chickflow.data.generate import allocate_discount, generate
from chickflow.data.validate import validate_files

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("gross,discount,expected", [
    ([25000,10000],3500,[2500,1000]),
    ([1,1,1],2,[1,1,0]),
    ([10,11,12],0,[0,0,0]),
    ([10,11,12],33,[10,11,12]),
])
def test_discount_reconciles(gross, discount, expected):
    assert allocate_discount(gross,discount) == expected


def test_validated_assignment_snapshot():
    report = validate_files(ROOT/"data/clean")
    assert report["passed"], report["errors"]
    assert report["rows"]["orders"] == 3600
    assert report["completed_paid_orders"] >= 500
    assert report["reconciliation_abs_idr"] == {
        "gross_amount_idr":0,"discount_amount_idr":0,"net_amount_idr":0,
    }
    assert report["minimum_running_stock"] >= 0


def test_default_seed_reproduces_snapshot(tmp_path, manifest):
    raw = tmp_path/"raw"
    generate(ROOT/"config/simulation.yaml",raw)
    replay = clean(raw,tmp_path/"clean",ROOT/"config/menu.yaml")
    assert replay["sha256"] == manifest["sha256"]
    assert validate_files(tmp_path/"clean")["passed"]


def test_changed_file_fails_manifest(tmp_path):
    import shutil
    shutil.copytree(ROOT/"data/clean",tmp_path/"clean")
    shutil.copy(ROOT/"data/manifest.json",tmp_path/"manifest.json")
    path = tmp_path/"clean"/"orders.csv"
    with path.open("a") as handle:
        handle.write("\n")
    with pytest.raises(ValueError,match="Hash"):
        validate_files(tmp_path/"clean")
