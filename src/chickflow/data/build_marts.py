import argparse
from pathlib import Path

from chickflow.data.schema import load_clean_bundle, write_csv
from chickflow.metrics import build_facts


def main():
    parser = argparse.ArgumentParser(description="Build sales-line and eligible-order facts.")
    parser.add_argument("--input", type=Path, default=Path("data/clean"))
    parser.add_argument("--output", type=Path, default=Path("data/marts"))
    args = parser.parse_args()
    facts = build_facts(load_clean_bundle(args.input))
    eligible = facts.orders.loc[facts.orders["order_id"].isin(facts.sales["order_id"])]
    write_csv(args.output / "fact_orders_eligible.csv", eligible)
    write_csv(args.output / "fact_sales_lines.csv", facts.sales)
    print(f"Mart: {len(eligible)} order selesai dan {len(facts.sales)} baris penjualan.")


if __name__ == "__main__":
    main()
