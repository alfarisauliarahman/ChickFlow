"""Recalculate the eight Overview metrics directly from clean CSV records."""
import argparse
import csv
import json
from collections import defaultdict
from datetime import date, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from zoneinfo import ZoneInfo

from chickflow.data.schema import load_clean_bundle
from chickflow.metrics import FilterContext, build_facts, compute_overview_kpis, compute_stock_asof, scope


def rows(source, name):
    with (source / f"{name}.csv").open(newline="") as file:
        yield from csv.DictReader(file)


def quotient(amount, count):
    return amount / count if count else None


def recalculate(source, filters):
    wib = ZoneInfo("Asia/Jakarta")
    selected = {}
    for order in rows(source, "orders"):
        ordered = datetime.fromisoformat(order["ordered_at"]).astimezone(wib)
        if (filters.start_date <= ordered.date() <= filters.end_date
                and order["order_status"] == "COMPLETED" and order["payment_status"] == "PAID"
                and (not filters.branch_ids or order["branch_id"] in filters.branch_ids)):
            selected[order["order_id"]] = ordered, order

    categories = {row["menu_id"]: row["category"] for row in rows(source, "menu")}
    revenue = food_cost = 0
    contributing_orders = set()
    for item in rows(source, "order_items"):
        order_id = item["order_id"]
        if order_id not in selected or (filters.categories and categories[item["menu_id"]] not in filters.categories):
            continue
        contributing_orders.add(order_id)
        units = int(item["quantity"])
        revenue += units * int(item["unit_price_idr"]) - int(item["allocated_discount_idr"])
        food_cost += units * int(item["unit_food_cost_idr"])

    times = []
    late = 0
    for order_id in contributing_orders:
        ordered, order = selected[order_id]
        if order["ready_at"]:
            duration = (datetime.fromisoformat(order["ready_at"]) - ordered).total_seconds() / 60
            times.append(duration)
            late += duration > float(order["sla_min"])

    balances = defaultdict(Decimal)
    for move in rows(source, "inventory_movements"):
        day = datetime.fromisoformat(move["occurred_at"]).astimezone(wib).date()
        branch = move["branch_id"]
        if day <= filters.end_date and (not filters.branch_ids or branch in filters.branch_ids):
            balances[branch, move["ingredient_id"]] += Decimal(move["signed_qty"])

    evaluated = 0
    below_reorder = 0
    for policy in rows(source, "branch_inventory_policy"):
        pair = policy["branch_id"], policy["ingredient_id"]
        if pair in balances:
            evaluated += 1
            below_reorder += balances[pair] < Decimal(policy["reorder_point_qty"])

    order_count = len(contributing_orders)
    profit = revenue - food_cost
    return {
        "K01": revenue, "K02": order_count, "K03": quotient(revenue, order_count),
        "K04": quotient(sum(times), len(times)), "K05": quotient(late, len(times)),
        "K06": quotient(profit, revenue), "K07": below_reorder if evaluated else None, "K08": profit,
    }


def compare(source, manifest):
    end = date.fromisoformat(manifest["range_end"])
    start = max(end - timedelta(days=6), date.fromisoformat(manifest["range_start"]))
    scenarios = {
        "periode_default": FilterContext(start, end),
        "padang_minuman": FilterContext(start, end, ("BR-01",), ("Beverage",)),
        "tanggal_akhir": FilterContext(end, end),
    }
    result = []
    bundle = load_clean_bundle(source)
    facts = build_facts(bundle)
    for scenario, filters in scenarios.items():
        expected = recalculate(source, filters)
        stock = compute_stock_asof(bundle, filters.end_date, filters.branch_ids)
        values = compute_overview_kpis(scope(facts, filters), stock)
        for kpi, calculated in expected.items():
            dashboard = values[kpi]
            delta = dashboard - calculated if dashboard is not None and calculated is not None else None
            tolerance = 1e-8 if kpi == "K04" else 1e-12 if kpi in ("K03", "K05", "K06") else 0
            result.append({
                "scenario": scenario, "start_date": str(filters.start_date), "end_date": str(filters.end_date),
                "branch_ids": filters.branch_ids, "categories": filters.categories, "kpi": kpi,
                "expected": calculated, "dashboard": dashboard, "difference": delta, "tolerance": tolerance,
                "passed": abs(delta) <= tolerance if delta is not None else calculated is dashboard,
            })
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("data/clean"))
    parser.add_argument("--output", type=Path, default=Path("reports/evidence/kpi-checks.json"))
    args = parser.parse_args()
    manifest = json.loads((args.input.parent / "manifest.json").read_text())
    results = compare(args.input, manifest)
    passed = all(entry["passed"] for entry in results)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({
        "pass": passed, "seed": manifest["seed"], "csv_sha256": manifest["sha256"],
        "checks": results,
    }, ensure_ascii=False, indent=2) + "\n")
    print(f"{sum(entry['passed'] for entry in results)}/{len(results)} pemeriksaan KPI lulus.")
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
