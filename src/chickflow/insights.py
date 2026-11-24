from dataclasses import dataclass
from datetime import timedelta

from chickflow.metrics import FilterContext, daily_revenue, delayed_breakdown, menu_summary, prep_summary, ratio, scope


@dataclass(frozen=True)
class Insight:
    rule_id: str
    label: str
    severity: str
    actual: float | None
    threshold: float
    sample: int | None
    destination: str
    context: str
    action: str
    status: str
    unit: str


def result(rule_id, label, severity, actual, threshold, sample, destination, context, action, unit, direction):
    if actual is None:
        status = "not_evaluable"
    else:
        crossed = actual > threshold if direction == "above" else actual < threshold
        status = "triggered" if crossed else "clear"
    return Insight(rule_id,label,severity,actual,threshold,sample,destination,context,action,status,unit)


def compute_alerts(facts, scoped, stock, filters, first_day, settings):
    prep = prep_summary(scoped.orders)
    best = delayed_breakdown(scoped.orders, ["city", "channel_name"]).sort_values("late", ascending=False)
    delay_context = "Periode dan cabang terpilih"
    if not best.empty:
        lead = best.iloc[0]
        delay_context = f"{prep['late']}/{prep['n']} pesanan · kontribusi terbesar {lead.city}, {lead.channel_name}"

    menu = menu_summary(scoped.sales)
    qualified = menu.loc[menu["units"].ge(settings["sku_min_units"]) & menu["revenue"].gt(0)].sort_values("margin")
    lowest = qualified.iloc[0] if not qualified.empty else None
    observed = stock.dropna(subset=["stock_qty"]).sort_values("reorder_ratio")
    worst = observed.iloc[0] if not observed.empty else None
    anchor = filters.end_date
    base_start = anchor - timedelta(days=settings["sales_baseline_days"])
    sales_ratio = None
    sales_days = 0
    if base_start >= first_day:
        check = FilterContext(base_start, anchor, filters.branch_ids, filters.categories)
        daily = daily_revenue(scope(facts,check).sales, base_start, anchor)["revenue"]
        sales_days = len(daily)-1
        sales_ratio = ratio(float(daily.iloc[-1]), float(daily.iloc[:-1].mean()))
    revenue = int(scoped.sales["line_net_idr"].sum())
    margin = ratio(int(scoped.sales["line_food_gp_idr"].sum()),revenue)

    return [
        result("A01","Keterlambatan melampaui target","Peringatan",
               prep["rate"] if prep["n"] >= settings["delay_min_orders"] else None,
               settings["delay_limit"], prep["n"],"kitchen",delay_context,
               "Periksa cabang, kanal, dan jam dengan pesanan terlambat terbanyak.","%","above"),
        result("A02","Menu bermargin rendah","Peringatan",
               float(lowest.margin) if lowest is not None else None, settings["sku_margin_limit"],
               int(lowest.units) if lowest is not None else None,"profit",
               lowest.menu_name if lowest is not None else "Tidak ada SKU dengan sampel memadai",
               "Periksa resep, harga, dan diskon menu ini.","%","below"),
        result("A03","Stok di bawah titik pesan ulang","Kritis",
               float(worst.stock_qty) if worst is not None else None,
               float(worst.reorder_point_qty) if worst is not None else 0,
               int(stock["critical"].sum()),"inventory",
               f"{worst.ingredient_name} · {worst.city}" if worst is not None else "Ledger belum mencakup tanggal ini",
               "Tinjau daftar bahan kritis dan cek mutasi sebelum merencanakan restock.",
               worst.unit if worst is not None else "","below"),
        result("A04","Omzet harian di bawah baseline","Info",sales_ratio,settings["sales_ratio_limit"],
               sales_days,"sales",f"{anchor:%d/%m/%Y} vs rata-rata tujuh hari sebelumnya",
               "Bandingkan kanal dan menu yang menyumbang penurunan.","%","below"),
        result("A05","Margin kotor makanan turun","Peringatan",margin,settings["margin_limit"],
               len(scoped.orders),"profit","Agregasi omzet dan food cost pada filter aktif",
               "Periksa kategori dan menu dengan kontribusi laba rendah.","%","below"),
        result("A06","Ekor waktu persiapan tinggi","Peringatan",
               prep["p90_sla"] if prep["n"] >= settings["prep_min_orders"] else None,
               settings["prep_sla_ratio_limit"],prep["n"],"kitchen","P90 dari rasio durasi persiapan terhadap SLA masing-masing order",
               "Periksa kelompok pesanan paling lambat dan konteks jamnya.","×","above"),
    ]
