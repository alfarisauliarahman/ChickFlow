import argparse
import json
from pathlib import Path

import pandas as pd

from .generate import CHANNELS
from .schema import MOVEMENT_PRIORITY, cutoff_after, file_hash, load_clean_bundle

PRIMARY_KEYS = {
    "branches": ["branch_id"], "menu": ["menu_id"], "ingredients": ["ingredient_id"],
    "recipes": ["menu_id", "ingredient_id"], "branch_inventory_policy": ["branch_id", "ingredient_id"],
    "orders": ["order_id"], "order_items": ["order_item_id"], "inventory_movements": ["movement_id"],
    "feedback": ["feedback_id"],
}
FOREIGN_KEYS = (
    ("orders", "branches", "branch_id"), ("order_items", "orders", "order_id"),
    ("order_items", "menu", "menu_id"), ("recipes", "menu", "menu_id"),
    ("recipes", "ingredients", "ingredient_id"), ("branch_inventory_policy", "branches", "branch_id"),
    ("branch_inventory_policy", "ingredients", "ingredient_id"),
    ("inventory_movements", "branches", "branch_id"),
    ("inventory_movements", "ingredients", "ingredient_id"),
    ("inventory_movements", "orders", "order_id"), ("feedback", "orders", "order_id"),
)


def validate_bundle(bundle):
    errors = []

    def check(condition, message):
        if not condition:
            errors.append(message)

    for table, key in PRIMARY_KEYS.items():
        values = bundle[table][key]
        check(not values.isna().any().any() and not values.duplicated().any(), f"PK: {table}")
    for table, parent, key in FOREIGN_KEYS:
        values = bundle[table][key]
        if table == "inventory_movements" and key == "order_id":
            values = values.dropna()
        check(values.notna().all() and values.isin(bundle[parent][key]).all(), f"FK: {table}.{key}")

    orders, items, recipes, ingredients, movements, feedback, policy, branches, menu = (
        bundle[key] for key in ("orders", "order_items", "recipes", "ingredients", "inventory_movements", "feedback", "branch_inventory_policy", "branches", "menu")
    )
    completed = orders.loc[orders["order_status"].eq("COMPLETED")]
    canceled = orders.loc[orders["order_status"].eq("CANCELLED")]
    check(len(branches) == 3 and len(menu) == 24 and len(ingredients) == 27, "Ukuran katalog")
    check(len(completed) >= 500 and orders["simulation_date"].nunique() >= 7, "Cakupan transaksi")
    check(orders["simulation_date"].eq(orders["ordered_at"].dt.date).all()
          and orders["ordered_at"].dt.hour.between(10,21).all() and orders["channel"].isin(CHANNELS).all(), "Tanggal WIB, jam, kanal")
    check(len(orders) == len(completed) + len(canceled)
          and completed["payment_status"].eq("PAID").all() and canceled["payment_status"].eq("UNPAID").all(), "Status dan pembayaran")
    money_header = ["gross_amount_idr", "discount_amount_idr", "net_amount_idr"]
    check(canceled[money_header].eq(0).all().all()
          and canceled[["ready_at","completed_at","prep_time_min","delayed_flag"]].isna().all().all(), "Order batal bernilai nol")
    check(set(items["order_id"]) == set(completed["order_id"]), "Cakupan item order selesai")
    check(completed["ordered_at"].le(completed["ready_at"]).all()
          and completed["ready_at"].le(completed["completed_at"]).all(), "Kronologi dapur")
    prep = (completed["ready_at"]-completed["ordered_at"]).dt.total_seconds() / 60
    check((prep - completed["prep_time_min"]).abs().le(1/60).all()
          and completed["delayed_flag"].notna().all()
          and completed["delayed_flag"].eq(prep.gt(completed["sla_min"])).all(), "Waktu persiapan dan SLA")
    integer_fields = ["quantity", "unit_price_idr","line_gross_idr","allocated_discount_idr","line_net_idr","line_food_cost_idr","unit_food_cost_idr","line_food_gp_idr"]
    values = items[integer_fields]
    check(values.notna().all().all() and values.mod(1).eq(0).all().all(), "Kuantitas dan Rupiah bilangan bulat")
    check(items["quantity"].between(1, 5).all() and items["unit_price_idr"].gt(0).all()
          and (items["unit_price_idr"]*items["quantity"]).eq(items["line_gross_idr"]).all()
          and items["allocated_discount_idr"].ge(0).all()
          and items["allocated_discount_idr"].le(items["line_gross_idr"]).all()
          and (items["line_gross_idr"]-items["allocated_discount_idr"]).eq(items["line_net_idr"]).all(), "Nilai baris")
    totals = items.groupby("order_id")[["line_gross_idr","allocated_discount_idr","line_net_idr"]].sum()
    totals.columns = money_header
    expected = orders.set_index("order_id")[money_header].sort_index()
    actual = totals.reindex(expected.index, fill_value=0)
    diff = (expected - actual).abs().sum().to_dict()
    check(all(value == 0 for value in diff.values()), "Selisih gross/diskon/net")
    cost = recipes.merge(ingredients[["ingredient_id", "unit_cost_idr"]], on="ingredient_id")
    per_sku = (cost["qty_per_unit"]*cost["unit_cost_idr"]).groupby(cost["menu_id"]).sum()
    check(set(per_sku.index) == set(menu["menu_id"]) and recipes["qty_per_unit"].gt(0).all()
          and items["menu_id"].map(per_sku).eq(items["unit_food_cost_idr"]).all()
          and (items["unit_food_cost_idr"]*items["quantity"]).eq(items["line_food_cost_idr"]).all()
          and (items["line_net_idr"]-items["line_food_cost_idr"]).eq(items["line_food_gp_idr"]).all(), "BOM, COGS, dan Food Gross Profit")
    pair = ["branch_id","ingredient_id"]
    expected_pairs = set((branch, iid) for branch in branches["branch_id"] for iid in ingredients["ingredient_id"])
    check(set(policy[pair].itertuples(index=False, name=None)) == expected_pairs
          and policy[["opening_qty","restock_lot_qty"]].gt(0).all().all()
          and policy["reorder_point_qty"].gt(0).all(), "Kebijakan stok per cabang dan bahan")
    priority = movements["movement_type"].map(MOVEMENT_PRIORITY)
    inbound = movements["movement_type"].isin(("OPENING","RECEIPT"))
    check(priority.notna().all() and movements.loc[inbound,"signed_qty"].gt(0).all()
          and movements.loc[~inbound,"signed_qty"].lt(0).all()
          and (movements["signed_qty"].abs()*movements["unit_cost_idr"]).eq(movements["movement_cost_idr"]).all(), "Jumlah dan biaya mutasi")
    ledger = movements.assign(priority=priority).sort_values(["occurred_at","priority","movement_id"])
    minimum_balance = ledger.groupby(pair)["signed_qty"].cumsum().min()
    check(minimum_balance >= 0, "Saldo negatif")
    opening = movements.loc[movements["movement_type"].eq("OPENING")].set_index(pair)["signed_qty"].sort_index()
    check(opening.equals(policy.set_index(pair)["opening_qty"].sort_index().rename("signed_qty")), "Stok awal")
    consumption = items.merge(recipes, on="menu_id").assign(used=lambda t: t.quantity*t.qty_per_unit)
    use_key = ["order_id", "ingredient_id"]
    expected_use = consumption.groupby(use_key)["used"].sum().sort_index()
    used = movements.loc[movements["movement_type"].eq("USAGE")]
    audit = used.merge(orders[["order_id","branch_id","ready_at"]], on="order_id", suffixes=("","_order"))
    check(not used.duplicated(use_key).any() and len(audit) == len(used)
          and audit["branch_id"].eq(audit["branch_id_order"]).all() and audit["occurred_at"].eq(audit["ready_at"]).all()
          and used.set_index(use_key)["signed_qty"].sort_index().mul(-1).rename("used").equals(expected_use)
          and movements.loc[~movements["movement_type"].eq("USAGE"),"order_id"].isna().all(), "Penggunaan stok sesuai resep dan ready_at")
    feedback_audit = feedback.merge(completed[["order_id","completed_at"]], on="order_id")
    check(len(feedback) == len(feedback_audit) and feedback["rating"].between(1,5).all()
          and not feedback["order_id"].duplicated().any()
          and feedback_audit["feedback_at"].ge(feedback_audit["completed_at"]).all(), "Relasi, rating, dan waktu ulasan")
    return {
        "passed": not errors, "errors": errors, "rows": {k: len(t) for k,t in bundle.tables.items()},
        "completed_paid_orders": len(completed), "canceled_orders": len(canceled),
        "net_revenue_idr": int(items["line_net_idr"].sum()), "food_cogs_idr": int(items["line_food_cost_idr"].sum()),
        "food_gp_idr": int(items["line_food_gp_idr"].sum()),
        "reconciliation_abs_idr": {key: int(value) for key,value in diff.items()},
        "minimum_running_stock": int(minimum_balance) if pd.notna(minimum_balance) else None,
    }


def validate_files(source):
    manifest = json.loads((source.parent / "manifest.json").read_text())
    if set(manifest["sha256"]) != {f"{name}.csv" for name in PRIMARY_KEYS}:
        raise ValueError("Manifest wajib memuat hash kesembilan tabel.")
    for filename, expected in manifest["sha256"].items():
        if file_hash(source / filename) != expected:
            raise ValueError(f"Hash tidak cocok: {filename}")
    bundle = load_clean_bundle(source)
    report = validate_bundle(bundle)
    orders = bundle["orders"]
    config = manifest["simulation"]
    if len(orders) != config["target_orders"] or orders["ordered_at"].min().date().isoformat() < manifest["range_start"] or orders["ordered_at"].max() >= cutoff_after(pd.Timestamp(manifest["range_end"]).date()):
        report["errors"].append("Volume atau rentang order di luar konfigurasi.")
    if report["rows"] != manifest["rows"]:
        report["errors"].append("Jumlah baris berbeda dari manifest.")
    report["passed"] = not report["errors"]
    report["cleaning"] = manifest["cleaning"]
    return report


def main():
    parser = argparse.ArgumentParser(description="Check financial, inventory, and schema integrity.")
    parser.add_argument("--input", type=Path, default=Path("data/clean"))
    parser.add_argument("--report", type=Path, default=Path("reports/data_quality.json"))
    args = parser.parse_args()
    try:
        report = validate_files(args.input)
    except (OSError, ValueError, KeyError, TypeError) as error:
        report = {"passed": False, "errors": [str(error)]}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
