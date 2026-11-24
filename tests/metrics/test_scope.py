from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import pytest
import yaml

from chickflow.data.schema import DataBundle, TZ
from chickflow.insights import compute_alerts, result
from chickflow.metrics import (
    FilterContext, compute_overview_kpis, compute_stock_asof, demand_heatmap,
    period_movements, prep_summary, prior_growth, scope,
)

SETTINGS = yaml.safe_load((Path(__file__).resolve().parents[2]/"config/alerts.yaml").read_text())
START, END = date(2026,10,1), date(2026,10,30)


def test_category_uses_distinct_orders_and_line_amounts(facts):
    selected = FilterContext(START,END,("BR-01",),("Beverage",))
    filtered = scope(facts,selected)
    assert filtered.sales.category.eq("Beverage").all()
    assert filtered.sales.branch_id.eq("BR-01").all()
    assert filtered.orders.order_id.is_unique
    assert len(filtered.orders) == filtered.sales.order_id.nunique()
    stock = compute_stock_asof(facts.bundle,END,("BR-01",))
    kpi = compute_overview_kpis(filtered,stock)
    assert kpi["K03"] == filtered.sales.line_net_idr.sum() / filtered.sales.order_id.nunique()
    assert kpi["K02"] < len(filtered.all_orders)


def test_end_date_controls_stock_and_period_controls_waste(facts):
    wide = FilterContext(START,END)
    narrow = FilterContext(END,END,categories=("Combo",))
    stock = compute_stock_asof(facts.bundle,wide.end_date)
    same = compute_stock_asof(facts.bundle,narrow.end_date)
    pd.testing.assert_frame_equal(stock,same)
    assert len(period_movements(facts.bundle,wide)) > len(period_movements(facts.bundle,narrow))
    assert period_movements(facts.bundle,narrow).occurred_at.dt.date.eq(END).all()


def test_midnight_excluded_from_previous_day(facts):
    movements = facts.bundle["inventory_movements"].iloc[:1].copy()
    movements.loc[movements.index[0],"occurred_at"] = pd.Timestamp("2026-10-02 00:00",tz=TZ)
    bundle = DataBundle({**facts.bundle.tables,"inventory_movements":movements})
    assert period_movements(bundle,FilterContext(START,START)).empty
    assert len(period_movements(bundle,FilterContext(START+timedelta(days=1),START+timedelta(days=1)))) == 1


def test_stock_alert_evaluates_with_empty_sales(facts):
    filters = FilterContext(END,END,categories=("missing category",))
    filtered = scope(facts,filters)
    stock = compute_stock_asof(facts.bundle,END)
    alerts = {x.rule_id:x for x in compute_alerts(facts,filtered,stock,filters,START,SETTINGS)}
    assert filtered.sales.empty
    assert compute_overview_kpis(filtered,stock)["K03"] is None
    assert alerts["A01"].status == "not_evaluable"
    assert alerts["A03"].status == "triggered"
    assert alerts["A03"].sample > 0
    assert alerts["A06"].status == "not_evaluable"


def test_heatmap_normalizes_weekday_exposure():
    orders = pd.DataFrame({"weekday":[0,0,1],"hour":[13,13,13],"order_id":["a","b","c"]})
    cells = demand_heatmap(orders,date(2026,10,5),date(2026,10,12))
    monday,tuesday = cells.query("hour == 13 and weekday in [0,1]").itertuples(index=False)
    assert (monday.orders,monday.days,monday.daily_mean) == (2,2,1)
    assert (tuesday.orders,tuesday.days,tuesday.daily_mean) == (1,1,1)
    short = demand_heatmap(orders,date(2026,10,5),date(2026,10,5))
    assert short.loc[short.weekday.eq(1),"daily_mean"].isna().all()


@pytest.mark.parametrize("actual,threshold,direction,status",[
    (.10,.10,"above","clear"),(.11,.10,"above","triggered"),
    (9,10,"below","triggered"),(10,10,"below","clear"),
    (None,10,"below","not_evaluable"),(.30,.30,"below","clear"),
])
def test_rule_thresholds(actual,threshold,direction,status):
    assert result("A","test","Info",actual,threshold,20,"overview","","","%",direction).status == status


def test_previous_period_requires_full_coverage(facts):
    filters = FilterContext(START,END)
    assert prior_growth(scope(facts,filters),facts,filters,START) is None
    filters = FilterContext(END-timedelta(days=6),END)
    assert prior_growth(scope(facts,filters),facts,filters,START) is not None


def test_mixed_channel_p90_uses_per_order_sla():
    orders = pd.DataFrame({"prep_time_min":[18.,30.],"sla_min":[18.,25.],"delayed_flag":[False,True]})
    values = prep_summary(orders)
    assert values["rate"] == .5
    assert values["p90_sla"] == pytest.approx(1.18)
