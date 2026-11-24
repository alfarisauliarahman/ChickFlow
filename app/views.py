import json
import re
from collections import Counter
from datetime import timedelta
from pathlib import Path

import pandas as pd
import streamlit as st
from wordcloud import WordCloud

from chickflow import charts
from chickflow.data.schema import cutoff_after
from chickflow.insights import compute_alerts
from chickflow.metrics import (
    branch_summary, compute_overview_kpis, compute_stock_asof, daily_revenue, delayed_breakdown,
    demand_heatmap, menu_summary, period_movements, prep_summary, prior_growth, sales_summary,
)

ASSETS = Path(__file__).resolve().parents[1] / "assets"
AOV_HELP = "Omzet bersih item terpilih dibagi jumlah pesanan unik yang memuat item tersebut."
STOCK_HELP = "Saldo menjumlahkan perubahan stok sampai akhir tanggal WIB. Filter kategori menu tidak mengubah stok."
EMPTY = "Belum ada pesanan pada filter ini. Tambah rentang tanggal atau reset filter."
TITLES = {
    "overview": "Ringkasan operasional", "orders": "Pesanan dan jam sibuk",
    "kitchen": "Waktu persiapan dapur", "inventory": "Persediaan bahan",
    "sales": "Penjualan cabang", "profit": "Biaya dan laba menu",
}
ALERT_LABELS = {
    "A01": "Pesanan lewat batas waktu", "A02": "Margin menu rendah",
    "A03": "Stok perlu dipesan ulang", "A04": "Omzet harian turun",
    "A05": "Margin kotor makanan rendah", "A06": "Waktu persiapan tinggi",
}
DEST_LABELS = {"kitchen":"Cek dapur","inventory":"Cek stok","profit":"Cek margin","sales":"Cek penjualan"}


def page_heading(page, scope_label):
    if page == "overview":
        with st.container(key="report-hero", border=True):
            title, photo = st.columns([1.03, 1])
            with title:
                st.title(TITLES[page])
                st.caption(scope_label)
            with photo:
                st.image(str(ASSETS / "brand/chickflow-serving-tray.png"), width="stretch")
    else:
        st.title(TITLES[page])
        st.caption(scope_label)


def money(value):
    return f"Rp{value:,.0f}".replace(",", ".")


def number(value):
    return f"{value:,.0f}".replace(",", ".")


def display_money(value):
    if abs(value) >= 1_000_000:
        return f"Rp{value / 1_000_000:.2f} jt".replace(".", ",")
    return money(value)


def percent(value):
    return f"{value:.1%}".replace(".", ",") if pd.notna(value) else "—"


def minutes(value):
    return f"{value:.1f} mnt".replace(".", ",") if pd.notna(value) else "—"


def aov_label(filters):
    return "Omzet kategori per pesanan" if filters.categories else "Rata-rata nilai pesanan"


def present_kpis(metrics, key):
    with st.container(key=key, border=True):
        cols = st.columns(len(metrics))
        for column, (label, value, help_text) in zip(cols, metrics):
            if isinstance(value, (int, float)) and label.endswith("(Rp)"):
                label = label.removesuffix(" (Rp)")
                help_text = f"{money(value)}. {help_text}"
                value = display_money(value)
            column.metric(label, value, help=help_text)


def figure(chart, key):
    st.plotly_chart(chart, key=key, width="stretch", theme=None, config={"displaylogo":False})


def table_export(table, key, *, height=310, column_config=None):
    st.dataframe(table, hide_index=True, width="stretch", height=height, column_config=column_config)
    st.download_button("Unduh tabel CSV", table.to_csv(index=False).encode("utf-8-sig"),
                       f"chickflow-{key}.csv", "text/csv", key=f"csv-{key}")


def view_branches(facts, scoped, filters):
    branches = facts.bundle["branches"]
    if filters.branch_ids:
        branches = branches.loc[branches["branch_id"].isin(filters.branch_ids)]
    return branch_summary(scoped, branches).sort_values("revenue", ascending=False)


def branch_text(table):
    return table.assign(rate=table.rate.map(percent), margin=table.margin.map(percent)).rename(columns={
        "city":"Cabang", "revenue":"Omzet (Rp)", "orders":"Pesanan",
        "rate":"Pesanan terlambat", "margin":"Margin kotor",
    })[["Cabang","Omzet (Rp)","Pesanan","Pesanan terlambat","Margin kotor"]]


def channels_for_readers(table):
    return table.assign(channel_name=table["channel_name"].replace("Delivery", "Pesan antar"))


def choose_view(view_key, view_name, value_key=None, value=None):
    st.session_state[view_key] = view_name
    if value_key is not None:
        st.session_state[value_key] = value


def view_switch(label, key, options):
    if key not in st.session_state:
        st.session_state[key] = options[0]
    return st.segmented_control(label, options, key=key, label_visibility="collapsed") or options[0]


def show_alert(alert, pages, *, compact=False):
    if alert.unit == "%":
        actual = percent(alert.actual)
        threshold = percent(alert.threshold)
    elif pd.notna(alert.actual):
        actual = f"{alert.actual:g} {alert.unit}"
        threshold = f"{alert.threshold:g} {alert.unit}"
    else:
        actual = threshold = "—"
    label = ALERT_LABELS[alert.rule_id]
    context = alert.context.replace("Delivery", "Pesan antar")
    if not compact:
        st.markdown(f"**{alert.severity} · {label}**")
        st.caption(f"{context} · Nilai {actual} · Batas {threshold}")
        st.write(alert.action)
        return
    detail, value_slot, action = st.columns([3.7, 1.15, 1.28], vertical_alignment="center")
    with detail:
        st.markdown(f"**{label}**")
        st.caption(f"{context} · batas {threshold}" if alert.rule_id == "A03" else context)
    value_slot.markdown(f"**{actual}**")
    if alert.destination in pages:
        action.page_link(pages[alert.destination], label=DEST_LABELS[alert.destination])


def overview(facts, scoped, filters, first, settings, pages):
    stock = compute_stock_asof(facts.bundle, filters.end_date, filters.branch_ids)
    values = compute_overview_kpis(scoped, stock)
    alerts = compute_alerts(facts, scoped, stock, filters, first, settings)
    priority = {"Kritis":0,"Peringatan":1,"Info":2}
    active = sorted((a for a in alerts if a.status == "triggered"),
                    key=lambda a: (priority[a.severity], a.rule_id))
    critical_stock = next((alert for alert in active if alert.rule_id == "A03"), None)
    if critical_stock is not None and "inventory" in pages:
        with st.container(key="mobile-stock-shortcut"):
            st.caption(f"{critical_stock.context} · {critical_stock.actual:g} {critical_stock.unit} tersisa")
            st.page_link(pages["inventory"], label=DEST_LABELS["inventory"], width="stretch")
    prep = prep_summary(scoped.orders)
    aov = money(values["K03"]) if values["K03"] is not None else "—"
    present_kpis([
        ("Omzet bersih (Rp)", values["K01"], "Penjualan setelah diskon."),
        ("Pesanan selesai", number(values["K02"]), "Pesanan unik selesai dan dibayar."),
        (aov_label(filters), aov, AOV_HELP),
        ("Pesanan terlambat", percent(values["K05"]), f"{prep['late']} dari {prep['n']} pesanan."),
        ("Laba kotor makanan (Rp)", values["K08"], "Omzet bersih dikurangi biaya bahan dan kemasan."),
    ], "metrics-overview")
    with st.container(key="overview-detail"):
        findings, trend = st.columns([1.2, 1])
        with findings:
            st.subheader("Perlu diperiksa")
            if not active:
                st.info("Tidak ada peringatan yang melewati batas pada periode ini.")
            for alert in active[:3]:
                key = "critical-alert" if alert.severity == "Kritis" else f"alert-{alert.rule_id}"
                with st.container(key=key):
                    show_alert(alert, pages, compact=True)
            with st.expander("Lihat semua aturan"):
                for alert in alerts:
                    label = ALERT_LABELS[alert.rule_id]
                    status = {"clear":"Dalam batas","triggered":"Aktif","not_evaluable":"Data belum cukup"}[alert.status]
                    if alert in active[3:]:
                        show_alert(alert, pages)
                    else:
                        st.caption(f"{alert.rule_id} · {label} · {status}")
            st.subheader("Perbandingan cabang")
            branches = branch_text(view_branches(facts, scoped, filters))
            st.dataframe(branches, hide_index=True, width="stretch", height="auto",
                         column_config={"Omzet (Rp)":st.column_config.NumberColumn(format="plain")})
        with trend:
            with st.container(key="trend-panel", border=True):
                st.subheader("Omzet per hari")
                growth = prior_growth(scoped, facts, filters, first)
                if scoped.sales.empty:
                    st.info(EMPTY)
                else:
                    if growth is not None:
                        st.caption(f"{percent(growth)} dibanding periode sebelumnya.")
                    figure(charts.revenue_line(daily_revenue(scoped.sales, filters.start_date, filters.end_date),
                                              height=234), "V-Q01")
            present_kpis([
                ("Waktu persiapan", minutes(values["K04"]), "Rata-rata dari pesanan masuk sampai siap."),
                ("Margin kotor", percent(values["K06"]), "Laba kotor makanan dibagi omzet bersih."),
                ("Bahan kritis", values["K07"] if values["K07"] is not None else "—", STOCK_HELP),
            ], "secondary-kpis")


def order_detail(scoped):
    with st.container(key="order-detail-layout"):
        if not scoped.orders.empty:
            recent = scoped.orders.sort_values("ordered_at", ascending=False)
            ids = recent.order_id.tolist()
            if st.session_state.get("detail-order-id") not in ids:
                st.session_state["detail-order-id"] = ids[0]
            selected = st.selectbox("Pilih pesanan", ids, key="detail-order-id")
            row = recent.loc[recent.order_id.eq(selected)].iloc[0]
            items = scoped.sales.loc[scoped.sales.order_id.eq(selected)]
            present_kpis([
                ("Subtotal (Rp)", int(items.line_net_idr.sum()), "Nilai item dalam filter."),
                ("Waktu persiapan", minutes(row.prep_time_min), "Dari pesanan masuk sampai siap."),
                ("Batas persiapan", minutes(row.sla_min), "Batas waktu untuk kanal pesanan ini."),
            ], "metrics-order-detail")
            st.subheader("Item pesanan")
            columns = {"menu_name":"Menu", "quantity":"Jumlah", "line_gross_idr":"Sebelum diskon (Rp)",
                       "allocated_discount_idr":"Diskon (Rp)", "line_net_idr":"Subtotal (Rp)"}
            st.dataframe(items[list(columns)].rename(columns=columns), hide_index=True, width="stretch")
        left, right = st.columns(2)
        with left:
            st.subheader("Alur pesanan · V-L02")
            st.graphviz_chart("""
digraph {
  graph [rankdir=TB, bgcolor="transparent"]
  node [shape=box, color="#789183", fontcolor="#262624", style=rounded]
  edge [color="#53534D"]
  "Pesanan masuk" -> "Dibatalkan sebelum produksi"
  "Pesanan masuk" -> "Pembayaran" -> "Dapur" -> "Pesanan siap dan stok berkurang" -> "Serah terima"
}
""", width="stretch")
            st.caption("Waktu persiapan dihitung dari pesanan masuk sampai siap.")
        with right:
            st.subheader("Kata yang sering muncul · V-L01")
            reviews = " ".join(scoped.feedback.review_text).lower()
            stopwords = set("dan dengan untuk yang dari saat dalam agak akan tetap ini itu lagi lebih pas sesuai semoga pesanan pesan chickflow".split())
            counts = Counter(word for word in re.findall(r"\b[a-z]{3,}\b", reviews) if word not in stopwords)
            if counts:
                cloud = WordCloud(width=1000, height=380, background_color="#FFFFFF", collocations=False,
                                  random_state=42, color_func=lambda word,random_state,**_: random_state.choice(
                                      ("#963C32","#35695E","#376982","#53534D"))).generate_from_frequencies(counts)
                st.caption(f"{scoped.feedback.review_text.ne('').sum()} ulasan berisi teks pada periode ini.")
                st.image(cloud.to_array(), caption="Kata yang lebih besar muncul lebih sering.", width="stretch")
                st.dataframe(pd.DataFrame(counts.most_common(12), columns=["Kata","Frekuensi"]),
                             hide_index=True, width="stretch")
            else:
                st.info("Belum ada teks ulasan pada filter ini. Coba periode yang lebih panjang.")


def orders(facts, scoped, filters, *_):
    mode = view_switch("Tampilan pesanan", "orders-view", ["Daftar pesanan","Detail dan ulasan"])
    if mode == "Detail dan ulasan":
        order_detail(scoped)
        return
    sales = sales_summary(scoped.sales, scoped.orders)
    canceled = int(scoped.all_orders.order_status.eq("CANCELLED").sum())
    with st.container(key="orders-layout"):
        transactions, context = st.columns([1.73, 1])
        with transactions:
            st.subheader("Pesanan terakhir")
            st.caption(f"{number(sales['orders'])} selesai · {number(canceled)} batal · {number(sales['units'])} unit menu")
            if scoped.orders.empty:
                st.info(EMPTY)
            else:
                search = st.text_input("Cari ID pesanan", placeholder="Contoh: ORD-000001").strip()
                recent = channels_for_readers(scoped.orders)
                subset = recent.loc[recent.order_id.str.contains(search, case=False, regex=False)] if search else recent
                totals = scoped.sales.groupby("order_id").line_net_idr.sum().rename("subtotal")
                rows = subset.join(totals, on="order_id").sort_values("ordered_at", ascending=False)
                rows = rows.assign(ordered_at=rows.ordered_at.dt.strftime("%d/%m/%Y %H:%M"),
                                   delayed_flag=rows.delayed_flag.map({True:"Terlambat",False:"Tepat waktu"}))
                columns = {"order_id":"ID pesanan","ordered_at":"Masuk (WIB)","city":"Cabang","channel_name":"Kanal",
                           "subtotal":"Subtotal (Rp)","prep_time_min":"Persiapan (menit)","delayed_flag":"Ketepatan waktu"}
                if rows.empty:
                    st.info("ID tersebut tidak ditemukan pada filter ini.")
                else:
                    table_export(rows[list(columns)].rename(columns=columns), "orders", height=370,
                                 column_config={"Persiapan (menit)":st.column_config.NumberColumn(format="%.1f")})
                    st.button("Lihat pesanan dan ulasan", type="primary", on_click=choose_view,
                              args=("orders-view","Detail dan ulasan","detail-order-id",rows.iloc[0].order_id))
            if filters.categories:
                st.caption("Subtotal mencakup item kategori terpilih. Jumlah batal mencakup semua kategori.")
        with context:
            with st.container(key="orders-heatmap", border=True):
                st.subheader("Jam sibuk")
                st.caption("Rata-rata pesanan pada hari dan jam yang sama.")
                cells = demand_heatmap(scoped.orders, filters.start_date, filters.end_date)
                figure(charts.order_heatmap(cells), "V-Q03")
            if not scoped.sales.empty:
                channels = channels_for_readers(scoped.sales).groupby("channel_name", as_index=False).agg(
                    revenue=("line_net_idr","sum"), orders=("order_id","nunique"))
                channels["aov"] = channels.revenue / channels.orders
                st.subheader(f"{aov_label(filters)} per kanal")
                figure(charts.horizontal_bar(channels, "aov", "channel_name", aov_label(filters),
                                             charts.TEAL, True), "V-Q09")


def kitchen(facts, scoped, filters, *_):
    orders = channels_for_readers(scoped.orders)
    channels = sorted(orders.channel_name.dropna().unique())
    selected = st.selectbox("Kanal layanan", ["Semua kanal", *channels])
    dataset = orders if selected == "Semua kanal" else orders.loc[orders.channel_name.eq(selected)]
    if dataset.empty:
        st.info(EMPTY)
        return
    summary = prep_summary(dataset)
    rates = delayed_breakdown(dataset, ["city","channel_name"])
    leader = delayed_breakdown(dataset, ["city"]).sort_values("rate", ascending=False).iloc[0]
    with st.container(key="kitchen-layout"):
        box, stats = st.columns([1.8, 1])
        with box, st.container(key="chart-box", border=True):
            st.subheader("Waktu persiapan tiap cabang")
            st.caption("Median, kuartil, dan pencilan.")
            figure(charts.prep_box(dataset), "V-Q10")
        with stats:
            with st.container(key="sla-panel", border=True):
                st.metric("Pesanan terlambat", percent(summary["rate"]),
                          help=f"{summary['late']} dari {summary['n']} pesanan.")
                st.caption(f"{summary['late']} dari {summary['n']} pesanan.")
                median, p90 = st.columns(2)
                median.metric("Median", minutes(summary["median"]))
                p90.metric("P90", minutes(summary["p90"]), help="90% pesanan siap dalam waktu ini atau lebih cepat.")
                st.caption("Batas waktu berbeda untuk tiap kanal.")
                st.markdown(f"**{leader.city} tertinggi** · {percent(leader.rate)} ({int(leader.late)} dari {int(leader.n)} pesanan)")
        delay, distribution = st.columns([1.8, 1])
        with delay:
            st.subheader("Pesanan terlambat menurut kanal")
            figure(charts.delay_bars(rates), "V-Q06")
        with distribution:
            st.subheader("Sebaran waktu persiapan")
            figure(charts.prep_histogram(dataset), "V-Q05")
    with st.expander("Lihat data per cabang dan kanal"):
        table_export(rates.assign(rate_pct=rates.rate*100).drop(columns="rate").rename(columns={
            "city":"Cabang","channel_name":"Kanal","n":"Pesanan dinilai","late":"Terlambat",
            "rate_pct":"Terlambat (%)","median":"Median (menit)",
        }), "kitchen")


def open_inventory_ledger(ingredient, branch):
    st.session_state["inventory-view"] = "Riwayat stok"
    if ingredient:
        st.session_state["ledger-ingredient"] = ingredient
    if branch:
        st.session_state["ledger-branch"] = branch


def inventory_ledger(facts, filters):
    ingredients = facts.bundle["ingredients"].set_index("ingredient_id").ingredient_name.to_dict()
    cities = facts.bundle["branches"].set_index("branch_id").city.to_dict()
    branches = list(filters.branch_ids) or list(cities)
    if st.session_state.get("ledger-branch") not in branches:
        st.session_state["ledger-branch"] = branches[0]
    item_slot, branch_slot = st.columns(2)
    ingredient = item_slot.selectbox("Pilih bahan", list(ingredients), format_func=ingredients.__getitem__,
                                     key="ledger-ingredient")
    branch = branch_slot.selectbox("Cabang riwayat stok", branches, format_func=cities.__getitem__,
                                   key="ledger-branch")
    ledger = facts.bundle["inventory_movements"]
    history = ledger.loc[ledger.ingredient_id.eq(ingredient) & ledger.branch_id.eq(branch)]
    left = cutoff_after(filters.start_date - timedelta(days=1))
    right = cutoff_after(filters.end_date)
    opening = history.loc[history.occurred_at.lt(left),"signed_qty"].sum()
    window = history.loc[history.occurred_at.ge(left) & history.occurred_at.lt(right)]
    by_day = window.groupby(window.occurred_at.dt.date)["signed_qty"].sum()
    dates = pd.date_range(filters.start_date,filters.end_date).date
    balances = opening + by_day.reindex(dates,fill_value=0).cumsum()
    stock = compute_stock_asof(facts.bundle, filters.end_date, (branch,))
    item = stock.loc[stock.ingredient_id.eq(ingredient)].iloc[0]
    st.subheader(f"{ingredients[ingredient]} · {cities[branch]}")
    st.caption(f"Saldo akhir per hari · batas pesan ulang {number(item.reorder_point_qty)} {item.unit}.")
    figure(charts.stock_history(dates, balances, item.reorder_point_qty, item.unit), "inventory-history")
    st.subheader("Riwayat stok")
    st.caption(f"Perubahan {filters.start_date:%d/%m/%Y}–{filters.end_date:%d/%m/%Y} WIB.")
    columns = {"occurred_at":"Waktu (WIB)","branch_id":"Cabang","movement_type":"Jenis perubahan",
               "signed_qty":"Jumlah","reason":"Alasan"}
    if window.empty:
        st.info("Belum ada perubahan stok untuk bahan ini pada periode terpilih.")
    else:
        ledger = window.sort_values("occurred_at",ascending=False)
        table_export(ledger[list(columns)].rename(columns=columns),"stock-history")


def inventory(facts, scoped, filters, *_):
    mode = view_switch("Tampilan persediaan", "inventory-view", ["Saldo stok", "Riwayat stok"])
    if mode == "Riwayat stok":
        inventory_ledger(facts, filters)
        return
    moves = period_movements(facts.bundle, filters)
    stock = compute_stock_asof(facts.bundle, filters.end_date, filters.branch_ids)
    waste = moves.loc[moves.movement_type.eq("WASTE")]
    shown = stock.dropna(subset=["stock_qty"]).sort_values("reorder_ratio")
    critical = shown.loc[shown.critical]
    priority = critical.iloc[0] if not critical.empty else None
    if priority is not None:
        with st.container(key="restock-panel"):
            main, meter = st.columns([1.3, 1])
            with main:
                st.caption("Bahan yang perlu dipesan")
                st.subheader(f"{priority.ingredient_name}, {priority.city}")
                st.write(f"{number(priority.stock_qty)} {priority.unit} tersisa · batas {number(priority.reorder_point_qty)} {priority.unit}")
            with meter:
                st.progress(min(float(priority.reorder_ratio), 1), text="Saldo dibanding batas pesan ulang")
                st.caption(f"{percent(priority.reorder_ratio)} · Saldo akhir {filters.end_date:%d/%m/%Y}")
    else:
        st.info("Tidak ada bahan di bawah batas pesan ulang pada cakupan ini.")
    st.button("Lihat riwayat stok", type="primary", on_click=open_inventory_ledger,
              args=(priority.ingredient_id, priority.branch_id) if priority is not None else (None, None))
    with st.container(key="inventory-layout"):
        balances, losses = st.columns([1.55, 1])
        with balances:
            st.subheader("Stok per bahan dan cabang")
            st.caption(f"Saldo akhir {filters.end_date:%d/%m/%Y} WIB. Filter kategori menu tidak mengubah stok.")
            only_critical = st.checkbox("Hanya bahan kritis")
            selection = critical if only_critical else shown
            if selection.empty:
                st.info("Tidak ada bahan pada cakupan ini. Tampilkan semua bahan atau pilih tanggal lain.")
            else:
                table = selection.assign(status=selection.critical.map({True:"Kritis", False:"Aman"}))
                columns = {"ingredient_name":"Bahan","city":"Cabang","unit":"Satuan","stock_qty":"Saldo",
                           "reorder_point_qty":"Batas pesan ulang","status":"Status"}
                table_export(table[list(columns)].rename(columns=columns), "inventory")
            if not selection.empty:
                with st.expander("Lihat saldo terhadap batas pesan ulang"):
                    figure(charts.stock_chart(selection.head(10)), "V-Q08")
        with losses:
            st.subheader("Biaya bahan terbuang")
            st.markdown(f"**{money(waste.movement_cost_idr.sum())}** pada periode ini.")
            if not waste.empty:
                cost = waste.groupby("ingredient_id", as_index=False).movement_cost_idr.sum()
                cost = cost.merge(facts.bundle["ingredients"][["ingredient_id","ingredient_name"]], on="ingredient_id")
                figure(charts.horizontal_bar(cost.nlargest(8,"movement_cost_idr"), "movement_cost_idr",
                                             "ingredient_name", "Biaya bahan terbuang", charts.TEAL, True), "V-Q12")
            else:
                st.caption("Belum ada pemborosan tercatat pada periode dan cabang ini.")
            present_kpis([
                ("Stok masuk", int(moves.movement_type.eq("RECEIPT").sum()), "Mutasi masuk pada rentang tanggal."),
                ("Stok habis", int(shown.stock_qty.eq(0).sum()), "Pasangan bahan dan cabang dengan saldo nol."),
            ], "inventory-facts")


@st.cache_data
def geographic_outline():
    path = ASSETS / "geo/west-sumatra.geojson"
    return json.loads(path.read_text()) if path.is_file() else None


def sales(facts, scoped, filters, first, *_):
    value = sales_summary(scoped.sales, scoped.orders)
    growth = prior_growth(scoped, facts, filters, first)
    present_kpis([
        ("Omzet bersih (Rp)", value["revenue"], "Penjualan setelah diskon."),
        ("Unit terjual", number(value["units"]), "Jumlah unit menu pada kategori terpilih."),
        ("Total diskon (Rp)", value["discounts"], "Diskon yang dialokasikan ke item."),
        ("Perubahan omzet", percent(growth), "Dibandingkan dengan periode sebelumnya yang sama panjang."),
    ], "metrics-sales")
    branch = view_branches(facts, scoped, filters)
    with st.container(key="sales-layout"):
        trend, map_slot = st.columns([1.21, 1])
        with trend, st.container(key="sales-trend", border=True):
            st.subheader("Omzet per hari")
            st.caption("Setelah diskon · waktu WIB.")
            if scoped.sales.empty:
                st.info(EMPTY)
            else:
                figure(charts.revenue_line(daily_revenue(scoped.sales, filters.start_date, filters.end_date)),
                       "sales-V-Q01")
        with map_slot, st.container(key="sales-map", border=True):
            st.subheader("Lokasi cabang")
            online = st.checkbox("Tampilkan peta dasar dari internet")
            boundary = geographic_outline()
            figure(charts.city_map(branch, online, boundary), "V-G01")
            st.caption("Titik pusat kota mewakili cabang fiktif. Ukuran titik menunjukkan omzet.")
            if not online and boundary:
                st.caption("Batas provinsi © OpenStreetMap, Wambacher dan geoBoundaries (ODbL).")
        rank_slot, branch_slot = st.columns([1.21, 1])
        with rank_slot:
            st.subheader("Menu terlaris")
            if not scoped.sales.empty:
                rank = menu_summary(scoped.sales)
                figure(charts.horizontal_bar(rank.head(10), "units", "menu_name", "Unit terjual", charts.BRICK), "V-Q02")
                with st.expander("Lihat tabel penjualan menu"):
                    table_export(rank.rename(columns={"units":"Unit","revenue":"Omzet (Rp)","orders":"Pesanan",
                                                       "menu_name":"Menu","category":"Kategori"}), "sales")
        with branch_slot:
            st.subheader("Omzet per cabang")
            figure(charts.horizontal_bar(branch, "revenue", "city", "Omzet", charts.TEAL, True), "V-Q04")
            st.dataframe(branch_text(branch), hide_index=True, width="stretch", height="auto")


def recipe(facts, rank):
    labels = rank.set_index("menu_id").menu_name.to_dict()
    if st.session_state.get("recipe-menu") not in labels:
        st.session_state["recipe-menu"] = next(iter(labels))
    menu_id = st.selectbox("Pilih menu", list(labels), format_func=labels.__getitem__, key="recipe-menu")
    detail = facts.bundle["recipes"].loc[lambda df: df.menu_id.eq(menu_id)].merge(
        facts.bundle["ingredients"][["ingredient_id","ingredient_name","unit","unit_cost_idr"]], on="ingredient_id")
    detail["cost"] = detail.qty_per_unit * detail.unit_cost_idr
    summary = rank.loc[rank.menu_id.eq(menu_id)].iloc[0]
    columns = {"ingredient_name":"Bahan","qty_per_unit":"Takaran","unit":"Satuan",
               "unit_cost_idr":"Biaya per satuan (Rp)","cost":"Biaya resep (Rp)"}
    with st.container(key="recipe-layout"):
        components, product = st.columns([1.48, 1])
        with components:
            st.subheader("Bahan dan kemasan")
            st.caption("Takaran dikali biaya per satuan.")
            table_export(detail[list(columns)].rename(columns=columns), "recipe", height=352)
            st.markdown(f"**Biaya resep per unit · {money(detail.cost.sum())}**")
        with product, st.container(key="recipe-photo", border=True):
            if menu_id == "M24":
                st.image(str(ASSETS/"brand/chickflow-family-feast.png"), caption="Ilustrasi Family Feast Box",
                         width="stretch")
            st.subheader(labels[menu_id])
            st.metric("Margin kotor makanan", percent(summary.margin))
            st.caption(f"{number(summary.units)} unit terjual pada periode ini.")
            st.dataframe(pd.DataFrame([
                ("Omzet sebelum diskon", money(summary.gross)),
                ("Diskon", money(summary.discount)),
                ("Omzet bersih", money(summary.revenue)),
                ("Biaya bahan dan kemasan", money(summary.cogs)),
                ("Laba kotor makanan", money(summary.profit)),
            ], columns=["Rincian", "Nilai"]), hide_index=True, height="auto", width="stretch")


def profit(facts, scoped, filters, first, settings, pages):
    value = sales_summary(scoped.sales, scoped.orders)
    mode = view_switch("Tampilan biaya dan laba", "profit-view", ["Ringkasan margin","Biaya resep"])
    if scoped.sales.empty:
        st.info(EMPTY)
        return
    rank = menu_summary(scoped.sales)
    if mode == "Biaya resep":
        recipe(facts, rank)
        return
    threshold = settings["sku_margin_limit"]
    review = rank.loc[rank.margin.lt(threshold) & rank.units.ge(settings["sku_min_units"])].sort_values("margin")
    lowest = review.iloc[0] if not review.empty else None
    calculation, recipe_action = st.columns([1.65, 1], vertical_alignment="center")
    calculation.subheader("Cara menghitung laba kotor")
    if lowest is not None:
        recipe_action.button("Cek biaya resep", type="primary", on_click=choose_view,
                             args=("profit-view","Biaya resep","recipe-menu",lowest.menu_id))
    present_kpis([
        ("Omzet sebelum diskon (Rp)", value["gross"], "Penjualan atas item terpilih sebelum diskon."),
        ("Dikurangi diskon (Rp)", value["discounts"], "Diskon yang dialokasikan ke item."),
        ("Dikurangi biaya bahan dan kemasan (Rp)", value["cogs"], "Biaya langsung sesuai resep."),
        ("Laba kotor makanan (Rp)", value["profit"], "Omzet bersih dikurangi biaya bahan dan kemasan."),
    ], "equation")
    with st.container(key="profit-layout"):
        comparison, selected = st.columns([1.65, 1])
        with comparison, st.container(key="margin-scatter", border=True):
            st.subheader("Menu laris dan marginnya")
            figure(charts.margin_scatter(rank.dropna(subset=["margin"]), threshold), "V-Q07")
            st.caption(f"Satu titik untuk setiap menu. Garis putus-putus menandai batas margin {percent(threshold)}.")
        with selected:
            with st.container(key="margin-review", border=True):
                st.subheader("Menu yang perlu dicek")
                if lowest is not None:
                    st.markdown(f"**{lowest.menu_name}**")
                    st.metric("Margin menu", percent(lowest.margin))
                    st.caption(f"{number(lowest.units)} unit terjual · batas margin {percent(threshold)}.")
                else:
                    st.info("Tidak ada menu di bawah batas margin dengan jumlah unit yang cukup.")
                st.caption(f"Margin semua menu · {percent(value['margin'])}")
        report_slot, category_slot = st.columns([1.65, 1])
        with report_slot:
            st.subheader("Penjualan dan laba per menu")
            cols = {"menu_name":"Menu","units":"Unit","gross":"Sebelum diskon (Rp)","discount":"Diskon (Rp)",
                    "revenue":"Omzet (Rp)","cogs":"Biaya bahan dan kemasan (Rp)","profit":"Laba kotor (Rp)",
                    "margin":"Margin (%)"}
            formatted = rank.assign(margin=rank.margin*100)
            table_export(formatted[list(cols)].rename(columns=cols), "profit", height=275,
                         column_config={"Margin (%)":st.column_config.NumberColumn(format="%.1f")})
        with category_slot:
            st.subheader("Laba kotor per kategori")
            mixes = rank.groupby("category", as_index=False).profit.sum()
            figure(charts.horizontal_bar(mixes, "profit", "category", "Laba kotor makanan", charts.TEAL, True), "V-Q11")


VIEWS = {"overview":overview,"orders":orders,"kitchen":kitchen,"inventory":inventory,"sales":sales,"profit":profit}
