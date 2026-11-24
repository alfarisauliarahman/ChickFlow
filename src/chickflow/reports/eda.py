import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from chickflow.data.schema import load_clean_bundle, write_csv
from chickflow.metrics import (
    FilterContext, build_facts, compute_stock_asof, daily_revenue, delayed_breakdown,
    menu_summary, period_movements, scope,
)


def run(source, output):
    output.mkdir(parents=True, exist_ok=True)
    bundle = load_clean_bundle(source)
    facts = build_facts(bundle)
    dates = facts.orders["simulation_date"]
    filters = FilterContext(dates.min(),dates.max())
    sliced = scope(facts,filters)
    trend = daily_revenue(sliced.sales,filters.start_date,filters.end_date)
    ranking = menu_summary(sliced.sales)
    prep = sliced.orders
    stock = compute_stock_asof(bundle,filters.end_date)
    waste = period_movements(bundle,filters).loc[lambda x: x.movement_type.eq("WASTE")]
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(9,3.5),layout="constrained")
    ax.plot(trend.date,trend.revenue/1e6, color="#1c4877",marker="o",markersize=3)
    ax.set(title="Omzet bersih harian · data simulasi",ylabel="Juta rupiah",xlabel="Tanggal WIB")
    fig.autofmt_xdate()
    fig.savefig(output/"V-Q01_net_sales.png",dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7,4),layout="constrained")
    top = ranking.head(10).sort_values("units")
    ax.barh(top.menu_name,top.units,color="#1c4877")
    ax.set(title="Sepuluh menu dengan unit terjual terbanyak",xlabel="Unit menu")
    fig.savefig(output/"V-Q02_menu_units.png",dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7,4),layout="constrained")
    sns.histplot(data=prep,x="prep_time_min",binwidth=2,kde=True,color="#1c4877",ax=ax)
    ax.set(title="Distribusi waktu persiapan",xlabel="Menit",ylabel="Pesanan")
    fig.savefig(output/"V-Q05_prep_distribution.png",dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7,4),layout="constrained")
    sns.boxplot(data=prep,x="city",y="prep_time_min",color="#79a4cf",ax=ax)
    ax.set(title="Waktu persiapan per cabang",xlabel="Cabang",ylabel="Menit")
    fig.savefig(output/"V-Q10_prep_branch.png",dpi=150)
    plt.close(fig)

    delayed = delayed_breakdown(prep,["city"]).sort_values("rate",ascending=False)
    worst = delayed.iloc[0]
    weakest = ranking.loc[ranking["units"].ge(10)].sort_values("margin").iloc[0]
    critical = stock.loc[stock["critical"]].sort_values("reorder_ratio")
    peak = prep["hour"].value_counts()
    p90 = prep["prep_time_min"].quantile(.90)
    conditions = [
        ("P01","Permintaan terkonsentrasi pada jam tertentu",
         f"Pukul {peak.index[0]:02}:00 memuat {peak.iloc[0]} order, sedangkan pukul {peak.index[-1]:02}:00 memuat {peak.iloc[-1]}.",
         "V-Q03","Bandingkan beban rata-rata per hari saat meninjau kapasitas shift."),
        ("P02","Keterlambatan berbeda antarcabang",
         f"{worst.city} memiliki {int(worst.late)}/{int(worst.n)} order terlambat ({worst.rate:.1%}). Rentang antarcabang {delayed.rate.min():.1%}–{delayed.rate.max():.1%}.",
         "V-Q06","Periksa komposisi kanal dan jam sebelum mengubah alokasi shift."),
        ("P03","Terdapat menu dengan volume penjualan dan margin rendah",
         f"{weakest.menu_name} terjual {int(weakest.units)} unit dengan margin {weakest.margin:.1%}.",
         "V-Q07","Periksa harga, diskon dan biaya resep menu ini."),
        ("P04","Sejumlah bahan berada di bawah titik pesan ulang",
         f"{len(critical)} dari {len(stock)} pasangan bahan–cabang berada di bawah titik pesan ulang pada {filters.end_date}.",
         "V-Q08","Periksa unit, kekurangan, dan riwayat penerimaan sebelum restock."),
        ("P05","Waktu persiapan memiliki ekor panjang",
         f"Median {prep.prep_time_min.median():.1f} menit dan P90 {p90:.1f} menit pada {len(prep)} order.",
         "V-Q05, V-Q10","Telusuri kelompok pesanan paling lambat per cabang dan kanal."),
        ("P06","Pemborosan menambah biaya bahan terpisah dari COGS penjualan",
         f"{len(waste)} event waste dengan biaya Rp{waste.movement_cost_idr.sum():,.0f}.",
         "V-Q12","Dahulukan bahan dengan biaya waste paling besar untuk evaluasi batch."),
    ]
    write_csv(output/"baseline.csv", pd.DataFrame(conditions,columns=["id","masalah","bukti","visual","tindakan"]))
    write_csv(output/"delay_by_branch.csv", delayed)
    write_csv(output/"menu_summary.csv", ranking)
    with (output/"data_profile.txt").open("w") as handle:
        for name, table in bundle.tables.items():
            print(f"\n{name}",file=handle)
            table.info(buf=handle)
            print(table.describe(include="all").to_string(),file=handle)
    print(f"Empat figur EDA dan {len(conditions)} catatan baseline ditulis ke {output}.")


def main():
    parser = argparse.ArgumentParser(description="Generate EDA plots and evidence from validated data.")
    parser.add_argument("--input", type=Path, default=Path("data/clean"))
    parser.add_argument("--output", type=Path, default=Path("reports/eda"))
    args = parser.parse_args()
    run(args.input,args.output)


if __name__ == "__main__":
    main()
