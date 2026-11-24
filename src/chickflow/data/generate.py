import argparse
from collections import Counter, defaultdict
from datetime import date, datetime, time, timedelta
from heapq import heapreplace
from math import ceil
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import yaml

from .schema import MOVEMENT_PRIORITY, TZ, frame, write_csv

CHANNELS = ("DINE_IN", "TAKEAWAY", "DELIVERY")
THEMES = {
    "kecepatan": ("Pesanan cepat dan praktis", "Pesanan perlu waktu lebih lama"),
    "rasa": ("Ayam renyah dan bumbunya pas", "Bumbunya kurang terasa"),
    "porsi": ("Porsi nasi dan ayam pas", "Porsi kentang terasa kecil"),
    "harga": ("Harga sesuai dengan porsinya", "Harga paket terasa mahal"),
    "kemasan": ("Kemasan rapi dan minuman aman", "Minuman bocor di dalam kemasan"),
    "pelayanan": ("Pelayanan ramah saat ambil pesanan", "Informasi waktu tunggu kurang jelas"),
}
FOLLOWUPS = (
    "Akan pesan lagi.", "Sesuai untuk makan siang.", "Mudah dibawa pulang.",
    "Semoga konsisten.", "Semoga kunjungan berikutnya lebih baik.",
)


def read_yaml(path):
    return yaml.safe_load(path.read_text())


def allocate_discount(gross_values, discount):
    total = sum(gross_values)
    if not gross_values or total <= 0 or not 0 <= discount <= total:
        raise ValueError("Gross atau diskon tidak valid.")
    shares = [divmod(discount * value, total) for value in gross_values]
    amounts = [amount for amount, _ in shares]
    priority = sorted(range(len(shares)), key=lambda i: (-shares[i][1], i))
    for i in priority[:discount - sum(amounts)]:
        amounts[i] += 1
    return amounts


def validate_config(config):
    date.fromisoformat(config["start_date"])
    if config["timezone"] != TZ:
        raise ValueError("Zona simulasi harus Asia/Jakarta.")
    if not isinstance(config["seed"], int) or config["seed"] < 0:
        raise ValueError("Seed harus berupa bilangan bulat nonnegatif.")
    if config["days"] < 7 or config["target_orders"] < 500:
        raise ValueError("Simulasi membutuhkan minimal 7 hari dan 500 order.")
    if (config["opening_hour"], config["closing_hour"]) != (10, 22):
        raise ValueError("Jam operasi simulasi adalah 10.00–22.00 WIB.")
    for field in ("cancellation_probability", "feedback_probability"):
        if not 0 <= config[field] <= 1:
            raise ValueError(f"{field} harus di antara 0 dan 1.")
    sla = config["sla_minutes"]
    if set(sla) != set(CHANNELS) or any(minutes <= 0 for minutes in sla.values()):
        raise ValueError("SLA harus positif dan tersedia untuk tiga kanal.")


def arrivals(rng, config, branches, dates):
    hours = np.arange(config["opening_hour"], config["closing_hour"])
    hour_weights = 0.25 + np.exp(-((hours - 12) / 1.4) ** 2) + 0.95 * np.exp(-((hours - 19) / 1.5) ** 2)
    slots = [(day, branch["branch_id"]) for day in dates for branch in branches]
    factors = {4: 1.12, 5: 1.25, 6: 1.18}
    demand = {b["branch_id"]: b["demand_multiplier"] for b in branches}
    weights = np.array([factors.get(day.weekday(), 1.0) * demand[branch] for day, branch in slots])
    counts = rng.multinomial(config["target_orders"], weights / weights.sum())
    events = []
    for (day, branch), count in zip(slots, counts):
        sampled = rng.choice(hours, count, p=hour_weights / hour_weights.sum())
        minutes = rng.integers(0, 60, count)
        seconds = rng.integers(0, 60, count)
        events.extend(
            (datetime.combine(day, time(int(hour), int(minute), int(second)), ZoneInfo(TZ)), branch)
            for hour, minute, second in zip(sampled, minutes, seconds)
        )
    return sorted(events)


def order_events(rng, config, dates, branches, menu, recipes, costs):
    branch_map = {b["branch_id"]: b for b in branches}
    initial = datetime.combine(dates[0], time(0), ZoneInfo(TZ))
    queues = {(b["branch_id"], station): [initial] * capacity
              for b in branches for station, capacity in b["slots"].items()}
    sku_weights = np.array([m["popularity_weight"] for m in menu])
    orders, items, feedback = [], [], []
    usage = []
    for seq, (ordered, branch) in enumerate(arrivals(rng, config, branches, dates), start=1):
        oid = f"ORD-{seq:06}"
        channel = str(rng.choice(CHANNELS, p=branch_map[branch]["channels"]))
        sla = config["sla_minutes"][channel]
        canceled = rng.random() < config["cancellation_probability"]
        entry = dict(order_id=oid, branch_id=branch, ordered_at=ordered, ready_at=None,
                     completed_at=None, channel=channel, order_status="CANCELLED",
                     payment_status="UNPAID", gross_amount_idr=0, discount_amount_idr=0,
                     net_amount_idr=0, sla_min=sla, prep_time_min=None, delayed_flag=None,
                     simulation_date=ordered.date())
        orders.append(entry)
        if canceled:
            continue

        n = rng.choice((1, 2, 3, 4), p=(.32, .39, .22, .07))
        indices = rng.choice(len(menu), n, replace=False, p=sku_weights / sku_weights.sum())
        basket = [menu[index] for index in indices]
        quantities = [int(q) for q in rng.choice((1, 2, 3), n, p=(.86, .12, .02))]
        gross_values = [sku["list_price_idr"] * qty for sku, qty in zip(basket, quantities)]
        gross = sum(gross_values)
        promo = channel == "DELIVERY" or any(sku["category"] == "Combo" for sku in basket)
        discount_rate = int(rng.choice((0, 5, 10, 15), p=(.47, .17, .25, .11) if promo else (.78, .12, .08, .02)))
        discount = (gross * discount_rate + 50) // 100
        allocations = allocate_discount(gross_values, discount)
        work = Counter()
        used = Counter()
        for line, (sku, qty, row_gross, alloc) in enumerate(zip(basket, quantities, gross_values, allocations), 1):
            mid = sku["menu_id"]
            unit_cost = sum(costs[i] * q for i, q in recipes[mid].items())
            line_cost = unit_cost * qty
            items.append(dict(order_item_id=f"{oid}-{line:02}", order_id=oid, menu_id=mid,
                              quantity=qty, unit_price_idr=sku["list_price_idr"], line_gross_idr=row_gross,
                              allocated_discount_idr=alloc, line_net_idr=row_gross-alloc,
                              unit_food_cost_idr=unit_cost, line_food_cost_idr=line_cost,
                              line_food_gp_idr=row_gross-alloc-line_cost))
            used.update({iid: q * qty for iid, q in recipes[mid].items()})
            work[sku["station"]] += sku["base_prep_min"] * (1 + .25*(qty-1))
        finishes = []
        for station, minutes in work.items():
            available = queues[(branch, station)]
            finish = max(ordered, available[0]) + timedelta(seconds=round(minutes * 60 * rng.uniform(.75, 1.2)))
            heapreplace(available, finish)
            finishes.append(finish)
        ready = max(finishes) + timedelta(seconds=int(rng.integers(45, 151)))
        completed = ready + timedelta(seconds=int(rng.integers(25, 181)))
        prep = (ready - ordered).total_seconds() / 60
        delayed = prep > sla
        entry.update(ready_at=ready, completed_at=completed, order_status="COMPLETED", payment_status="PAID",
                     gross_amount_idr=gross, discount_amount_idr=discount, net_amount_idr=gross-discount,
                     prep_time_min=round(prep, 8), delayed_flag=delayed)
        usage.extend((ready, branch, iid, -q, oid, "USAGE", "order_consumption") for iid, q in used.items())
        if rng.random() < config["feedback_probability"]:
            theme = "kecepatan" if delayed and rng.random() < .5 else str(rng.choice(tuple(THEMES)))
            favorable = rng.random() < (.42 if delayed else .88)
            review = f"{THEMES[theme][0 if favorable else 1]}. {rng.choice(FOLLOWUPS[:3] if favorable else FOLLOWUPS[3:])}"
            feedback.append(dict(feedback_id=f"FB-{seq:06}", order_id=oid, rating=int(rng.choice((4,5) if favorable else (2,3))),
                                 review_text=review, theme=theme, feedback_at=completed + timedelta(minutes=int(rng.integers(2, 80)))))
    return orders, items, usage, feedback


def inventory_events(rng, dates, branches, ingredients, usage):
    consumption = Counter()
    for _, branch, iid, qty, *_ in usage:
        consumption[branch, iid] -= qty
    policy, ledger = [], []
    timeline = defaultdict(list)
    for event in usage:
        timeline[event[1:3]].append(event)
    for branch_row in branches:
        branch = branch_row["branch_id"]
        for ingredient in ingredients:
            iid = ingredient["ingredient_id"]
            daily = consumption[branch, iid] / len(dates)
            minimum = 2 if ingredient["unit"] == "pcs" else 100
            reorder = max(minimum, ceil(daily * 1.5))
            opening = max(ceil(reorder * 1.5), ceil(daily * 3))
            lot = max(minimum, ceil(daily * 5))
            policy.append(dict(branch_id=branch, ingredient_id=iid, opening_qty=opening, reorder_point_qty=reorder,
                               restock_lot_qty=lot, lead_time_days=1, target_cover_days=5))
            events = timeline[branch, iid]
            opening_at = datetime.combine(dates[0], time(8), ZoneInfo(TZ))
            ledger.append((opening_at, branch, iid, opening, None, "OPENING", "initial"))
            for day in dates:
                if daily and rng.random() < (.33 if ingredient["ingredient_group"] in ("Produce", "Protein") else .13):
                    waste = max(1, round(daily * rng.uniform(.025, .14)))
                    events.append((datetime.combine(day, time(21, 50), ZoneInfo(TZ)), branch, iid, -waste, None, "WASTE", "spoilage"))
            balance = opening
            pending = None
            for event in sorted(events, key=lambda e: (e[0], MOVEMENT_PRIORITY[e[5]], e[4] or "")):
                at, _, _, qty, _, kind, _ = event
                if pending is not None and pending <= at:
                    ledger.append((pending, branch, iid, lot, None, "RECEIPT", "reorder"))
                    balance += lot
                    pending = None
                if balance + qty < 0:
                    received = max(-qty - balance, ceil(daily))
                    ledger.append((at, branch, iid, received, None, "RECEIPT", "emergency_restock"))
                    balance += received
                ledger.append(event)
                balance += qty
                if balance < reorder and pending is None:
                    pending = datetime.combine(at.date() + timedelta(days=1), time(9), ZoneInfo(TZ))
            if pending is not None and pending.date() <= dates[-1]:
                ledger.append((pending, branch, iid, lot, None, "RECEIPT", "reorder"))
    ledger.sort(key=lambda e: (e[0], MOVEMENT_PRIORITY[e[5]], e[1], e[2], e[4] or ""))
    costs = {i["ingredient_id"]: i["unit_cost_idr"] for i in ingredients}
    return policy, [
        dict(movement_id=f"MOV-{seq:07}", occurred_at=at, branch_id=branch, ingredient_id=iid, order_id=oid,
             signed_qty=qty, movement_type=kind, reason=reason, unit_cost_idr=costs[iid], movement_cost_idr=abs(qty)*costs[iid])
        for seq, (at, branch, iid, qty, oid, kind, reason) in enumerate(ledger, 1)
    ]


def inject_issues(tables, rng):
    orders, menu, feedback = (tables[name] for name in ("orders", "menu", "feedback"))
    log = []
    for i in rng.choice(len(orders), max(1, len(orders)//100), replace=False):
        value = datetime.fromisoformat(orders.at[i, "ordered_at"])
        orders.at[i, "ordered_at"] = value.strftime("%Y-%m-%dT%H:%M:%S%z")
        log.append(("orders", orders.at[i, "order_id"], "ordered_at", "format_timestamp"))
    rows = orders.iloc[rng.choice(len(orders), max(1, len(orders)//200), replace=False)]
    log.extend(("orders", oid, "order_id", "duplicate") for oid in rows["order_id"])
    tables["orders"] = pd.concat([orders, rows], ignore_index=True)
    for i in rng.choice(len(menu), 2, replace=False):
        menu.at[i,"category"] = " " + menu.at[i,"category"].lower() + " "
        log.append(("menu", menu.at[i,"menu_id"], "category", "case_whitespace"))
    missing_category = int(rng.integers(0, len(menu)))
    menu.at[missing_category, "category"] = None
    log.append(("menu", menu.at[missing_category, "menu_id"], "category", "missing"))
    for i in rng.choice(len(feedback), len(feedback)//50, replace=False):
        feedback.at[i,"review_text"] = None
        log.append(("feedback", feedback.at[i,"feedback_id"], "review_text", "missing"))
    return pd.DataFrame(log, columns=["table","record_id","field","issue"])


def generate(config_path, output, seed=None):
    config = read_yaml(config_path)
    if seed is not None:
        config["seed"] = seed
    validate_config(config)
    root = config_path.parent
    branches, menu, ingredients, recipes = [read_yaml(root / f"{name}.yaml") for name in ("branches", "menu", "ingredients", "recipes")]
    costs = {i["ingredient_id"]: i["unit_cost_idr"] for i in ingredients}
    start = date.fromisoformat(config["start_date"])
    dates = [start + timedelta(days=i) for i in range(config["days"])]
    demand_rng, stock_rng, quality_rng = (np.random.default_rng(s) for s in np.random.SeedSequence(config["seed"]).spawn(3))
    orders, items, usage, feedback = order_events(demand_rng, config, dates, branches, menu, recipes, costs)
    policy, movements = inventory_events(stock_rng, dates, branches, ingredients, usage)
    tables = {name: frame(name, data) for name,data in (
        ("branches", branches), ("menu", menu), ("ingredients", ingredients), ("recipes", [
            {"menu_id": m, "ingredient_id": i, "qty_per_unit": q}
            for m, recipe in recipes.items() for i,q in sorted(recipe.items())]),
        ("branch_inventory_policy", policy), ("orders", orders), ("order_items", items),
        ("inventory_movements", movements), ("feedback", feedback),
    )}
    tables["orders"]["ordered_at"] = tables["orders"]["ordered_at"].map(datetime.isoformat).astype(object)
    issues = inject_issues(tables, quality_rng) if config["quality_issues"] else pd.DataFrame(columns=["table","record_id","field","issue"])
    for name, table in tables.items():
        write_csv(output / f"{name}.csv", table)
    write_csv(output / "data_quality_injections.csv", issues)
    (output / "simulation.yaml").write_text(yaml.safe_dump(config, sort_keys=False))
    print(f"Data mentah seed {config['seed']}: {len(orders)} order, {len(items)} item, {len(movements)} mutasi, {len(issues)} anomali terkontrol.")


def main():
    parser = argparse.ArgumentParser(description="Generate ChickFlow synthetic restaurant data.")
    parser.add_argument("--config", type=Path, default=Path("config/simulation.yaml"))
    parser.add_argument("--output", type=Path, default=Path("data/raw"))
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()
    generate(args.config, args.output, args.seed)


if __name__ == "__main__":
    main()
