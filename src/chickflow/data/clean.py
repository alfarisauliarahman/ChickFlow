import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yaml

from .generate import read_yaml
from .schema import TABLES, TIME_FIELDS, file_hash, local_timestamps, write_csv


def clean(raw, output, catalog):
    if raw.resolve() == output.resolve():
        raise ValueError("Gunakan folder terpisah untuk data mentah dan bersih.")
    config = read_yaml(raw / "simulation.yaml")
    truth = {row["menu_id"]: row["category"] for row in read_yaml(catalog)}
    canonical = {v.casefold(): v for v in truth.values()}
    log = {}
    hashes = {}
    rows = {}
    for name, columns in TABLES.items():
        table = pd.read_csv(raw / f"{name}.csv", keep_default_na=False, na_values=[""])
        if list(table.columns) != columns.split():
            raise ValueError(f"Kolom data mentah tidak cocok: {name}")
        initial_count = len(table)
        for field in TIME_FIELDS.get(name, ()):
            table[field] = local_timestamps(table[field]).map(
                lambda value: value.isoformat() if pd.notna(value) else ""
            )
        if name == "orders":
            timestamp_variants = pd.read_csv(raw / "orders.csv", usecols=["ordered_at"])["ordered_at"]
            log["format_timestamp"] = int((~timestamp_variants.str.endswith("+07:00")).sum())
            table = table.drop_duplicates()
            if table["order_id"].duplicated().any():
                raise ValueError("ID pesanan duplikat berisi nilai yang berbeda.")
            log["duplicate_orders"] = initial_count - len(table)
        elif name == "menu":
            old = table["category"]
            restored = old.str.strip().str.casefold().map(canonical)
            restored = restored.where(old.notna(), table["menu_id"].map(truth))
            if restored.isna().any():
                raise ValueError("Kategori menu tidak dikenali.")
            log["category_missing"] = int(old.isna().sum())
            log["category_normalized"] = int((old.notna() & (old != restored)).sum())
            table["category"] = restored
        elif name == "feedback":
            log["review_text_missing"] = int(table["review_text"].isna().sum())
            table["review_text"] = table["review_text"].fillna("")
        path = output / f"{name}.csv"
        write_csv(path, table)
        rows[name] = len(table)
        hashes[path.name] = file_hash(path)
    manifest = {
        "generator_version": "2.3.0", "seed": config["seed"],
        "range_start": config["start_date"],
        "range_end": str(pd.Timestamp(config["start_date"]).date() + pd.Timedelta(days=config["days"] - 1)),
        "config_sha256": file_hash(raw / "simulation.yaml"), "simulation": config,
        "catalog_sha256": {name: file_hash(catalog.with_name(f"{name}.yaml"))
                           for name in ("branches", "menu", "ingredients", "recipes")},
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "synthetic": True, "rows": rows, "sha256": hashes, "cleaning": log,
    }
    manifest_path = output.parent / "manifest.json"
    temporary = manifest_path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(manifest_path)
    print(f"Sembilan tabel bersih, {rows['orders']} order, operasi cleaning {log}.")
    return manifest


def main():
    parser = argparse.ArgumentParser(description="Normalize and deduplicate the raw CSV files.")
    parser.add_argument("--input", type=Path, default=Path("data/raw"))
    parser.add_argument("--output", type=Path, default=Path("data/clean"))
    parser.add_argument("--catalog", type=Path, default=Path("config/menu.yaml"))
    args = parser.parse_args()
    clean(args.input, args.output, args.catalog)


if __name__ == "__main__":
    main()
