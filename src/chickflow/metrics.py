from dataclasses import dataclass
from datetime import date, timedelta

import pandas as pd

from chickflow.data.schema import DataBundle, cutoff_after

WEEKDAYS = ("Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu")
CHANNEL_NAMES = {"DINE_IN": "Makan di tempat", "TAKEAWAY": "Bawa pulang", "DELIVERY": "Delivery"}


@dataclass(frozen=True)
class FilterContext:
    start_date: date
    end_date: date
    branch_ids: tuple[str, ...] = ()
    categories: tuple[str, ...] = ()

    def __post_init__(self):
        if self.start_date > self.end_date:
            raise ValueError("Tanggal awal harus sebelum atau sama dengan tanggal akhir.")


@dataclass
class Facts:
    bundle: DataBundle
    orders: pd.DataFrame
    sales: pd.DataFrame
    feedback: pd.DataFrame


@dataclass
class ScopedFacts:
    orders: pd.DataFrame
    sales: pd.DataFrame
    all_orders: pd.DataFrame
    feedback: pd.DataFrame


def build_facts(bundle):
    orders = bundle["orders"].merge(
        bundle["branches"][["branch_id", "city"]], on="branch_id", validate="many_to_one"
    )
    orders["hour"] = orders["ordered_at"].dt.hour
    orders["weekday"] = orders["ordered_at"].dt.day_of_week
    orders["channel_name"] = orders["channel"].map(CHANNEL_NAMES)
    eligible = orders.loc[orders["order_status"].eq("COMPLETED") & orders["payment_status"].eq("PAID")]
    sales = bundle["order_items"].merge(
        eligible[["order_id", "simulation_date", "branch_id", "city", "channel", "channel_name"]],
        on="order_id", validate="many_to_one"
    ).merge(
        bundle["menu"][["menu_id", "menu_name", "category"]],
        on="menu_id", validate="many_to_one"
    )
    return Facts(bundle, orders, sales, bundle["feedback"])


def period_rows(table, filters):
    mask = table["simulation_date"].between(filters.start_date, filters.end_date)
    if filters.branch_ids:
        mask &= table["branch_id"].isin(filters.branch_ids)
    return table.loc[mask]


def scope(facts, filters):
    orders = period_rows(facts.orders, filters)
    sales = period_rows(facts.sales, filters)
    if filters.categories:
        sales = sales.loc[sales["category"].isin(filters.categories)]
    eligible = orders.loc[orders["order_id"].isin(sales["order_id"])]
    feedback = facts.feedback.loc[facts.feedback["order_id"].isin(eligible["order_id"])]
    return ScopedFacts(eligible, sales, orders, feedback)


def ratio(num, denom):
    return num / denom if denom > 0 else None


def prep_summary(orders):
    times = orders["prep_time_min"].dropna()
    shown = orders.loc[times.index]
    late = int(shown["delayed_flag"].sum())
    return {
        "n": len(times), "late": late, "rate": ratio(late, len(times)),
        "mean": float(times.mean()) if len(times) else None,
        "median": float(times.median()) if len(times) else None,
        "p90": float(times.quantile(.90)) if len(times) else None,
        "p90_sla": float((shown["prep_time_min"]/shown["sla_min"]).quantile(.90)) if len(times) else None,
    }


def compute_stock_asof(bundle, cutoff_date, branch_ids=()):
    policy = bundle["branch_inventory_policy"]
    if branch_ids:
        policy = policy.loc[policy["branch_id"].isin(branch_ids)]
    ledger = bundle["inventory_movements"]
    ledger = ledger.loc[ledger["occurred_at"].lt(cutoff_after(cutoff_date))]
    index = ["branch_id", "ingredient_id"]
    balance = ledger.groupby(index)["signed_qty"].sum().rename("stock_qty")
    seven_days = ledger.loc[
        ledger["occurred_at"].ge(cutoff_after(cutoff_date - timedelta(days=7)))
        & ledger["movement_type"].eq("USAGE")
    ]
    daily_usage = seven_days.groupby(index)["signed_qty"].sum().mul(-1/7).rename("daily_usage")
    stock = policy.join(balance, on=index).join(daily_usage, on=index)
    stock["critical"] = stock["stock_qty"].lt(stock["reorder_point_qty"])
    stock["reorder_ratio"] = stock["stock_qty"] / stock["reorder_point_qty"]
    stock["cover_days"] = stock["stock_qty"] / stock["daily_usage"].where(stock["daily_usage"].gt(0))
    stock = stock.merge(bundle["ingredients"][["ingredient_id", "ingredient_name", "unit"]],
                        on="ingredient_id", validate="many_to_one")
    return stock.merge(bundle["branches"][["branch_id", "city"]], on="branch_id", validate="many_to_one")


def period_movements(bundle, filters):
    ledger = bundle["inventory_movements"]
    start = cutoff_after(filters.start_date - timedelta(days=1))
    end = cutoff_after(filters.end_date)
    mask = ledger["occurred_at"].ge(start) & ledger["occurred_at"].lt(end)
    if filters.branch_ids:
        mask &= ledger["branch_id"].isin(filters.branch_ids)
    return ledger.loc[mask]


def sales_summary(sales, orders):
    revenue = int(sales["line_net_idr"].sum())
    cogs = int(sales["line_food_cost_idr"].sum())
    profit = revenue - cogs
    return dict(revenue=revenue, orders=len(orders), aov=ratio(revenue,len(orders)),
                gross=int(sales["line_gross_idr"].sum()), discounts=int(sales["allocated_discount_idr"].sum()),
                cogs=cogs, profit=profit, margin=ratio(profit,revenue), units=int(sales["quantity"].sum()))


def compute_overview_kpis(scoped, stock):
    values = sales_summary(scoped.sales, scoped.orders)
    prep = prep_summary(scoped.orders)
    observed_stock = stock["stock_qty"].notna().any()
    return {"K01": values["revenue"], "K02": values["orders"], "K03": values["aov"],
            "K04": prep["mean"], "K05": prep["rate"], "K06": values["margin"],
            "K07": int(stock["critical"].sum()) if observed_stock else None, "K08": values["profit"]}


def menu_summary(sales):
    data = sales.groupby(["menu_id","menu_name","category"], as_index=False).agg(
        units=("quantity","sum"), orders=("order_id","nunique"),
        gross=("line_gross_idr","sum"), discount=("allocated_discount_idr","sum"),
        revenue=("line_net_idr","sum"), cogs=("line_food_cost_idr","sum"), profit=("line_food_gp_idr","sum"),
    )
    data["margin"] = data["profit"] / data["revenue"].where(data["revenue"].gt(0))
    return data.sort_values(["units", "menu_name"], ascending=[False,True])


def calendar(start, end):
    return pd.date_range(start, end).date


def daily_revenue(sales, start, end):
    return (sales.groupby("simulation_date")["line_net_idr"].sum()
            .reindex(calendar(start,end), fill_value=0).rename("revenue")
            .rename_axis("date").reset_index())


def demand_heatmap(orders, start, end):
    dates = pd.Series(calendar(start, end), dtype="datetime64[ns]")
    n_days = dates.dt.day_of_week.value_counts().reindex(range(7), fill_value=0)
    index = pd.MultiIndex.from_product([range(7), range(10,22)], names=["weekday","hour"])
    cells = (orders.groupby(["weekday","hour"])["order_id"].nunique()
             .reindex(index, fill_value=0).rename("orders").reset_index())
    cells["days"] = cells["weekday"].map(n_days)
    cells["daily_mean"] = cells["orders"] / cells["days"].where(cells["days"].gt(0))
    cells["day"] = cells["weekday"].map(dict(enumerate(WEEKDAYS)))
    return cells


def delayed_breakdown(orders, group):
    valid = orders.dropna(subset=["prep_time_min"])
    result = valid.groupby(group, as_index=False).agg(
        n=("order_id","size"), late=("delayed_flag","sum"), median=("prep_time_min","median")
    )
    result["rate"] = result["late"] / result["n"]
    return result


def branch_summary(scoped, branches):
    values = scoped.sales.groupby("branch_id", as_index=False).agg(
        revenue=("line_net_idr","sum"), gp=("line_food_gp_idr","sum"), orders=("order_id","nunique")
    )
    table = branches[["branch_id","city","latitude","longitude"]].merge(values, how="left", on="branch_id")
    money = ["revenue","gp","orders"]
    table[money] = table[money].fillna(0).astype(int)
    table["margin"] = table["gp"] / table["revenue"].where(table["revenue"].gt(0))
    return table.merge(delayed_breakdown(scoped.orders, ["branch_id"])[["branch_id","late","n","rate"]],
                       how="left", on="branch_id")


def prior_growth(scoped, facts, filters, first_day):
    span = filters.end_date - filters.start_date + timedelta(days=1)
    earlier = filters.start_date - span
    if earlier < first_day:
        return None
    previous = FilterContext(earlier, filters.start_date - timedelta(days=1), filters.branch_ids, filters.categories)
    base = scope(facts, previous).sales["line_net_idr"].sum()
    return ratio(scoped.sales["line_net_idr"].sum()-base, base)
