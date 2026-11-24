# 05 — Canonical metrics, KPI formulas, thresholds, auto-insight rules

## 5.1 Aturan terpenting

1. **Satu fungsi untuk satu definisi metrik**, impor fungsi itu ke semua halaman.
2. **Revenue** selalu net sales setelah order-level discount, dihitung dari **completed+paid `order_items.line_net_idr`** (grain item).
3. **Order count** = jumlah **unique eligible completed+paid order ID**, bukan jumlah item/baris setelah join.
4. **COGS** = sum `line_food_cost_idr` item completed+paid; perincian resep hanya untuk audit. **Gross Profit** = net sales - COGS; belum menghitung gaji, waste, sewa, ongkir, service fee dan pajak.
5. **Inventory** = accumulated movement sampai end-date, bukan `sum(movements within current filter range)` untuk saldo akhir.
6. **Delayed rate** = delayed eligible orders / eligible orders dengan prep time valid, ditampilkan `%` dan `n/N`.
7. Semua perhitungan ratio = `sum numerator / sum denominator`, **bukan mean of branch percentages**.
8. Dividing zero: tampilkan em dash `—` atau label `Tidak ada data`, jangan `0%` seolah hasil sah.
9. Gunakan IDR integer; hasil `%` dibulatkan **untuk display saja**, tidak sebelum agregasi/alert.
10. Volume total pada chart menampilkan sample n jika relevan.

## 5.2 KPI registry formal

| KPI ID | Nama di UI | Formula resmi | Source/grain | Format | Kondisi |
|---|---|---|---|---|---|
| K01 | Net Revenue | Σ `line_net_idr` | fact_sales_lines | Rp dengan ribuan | paid+completed; item scope |
| K02 | Total Pesanan | `nunique(order_id)` | fact_orders_eligible | integer | completed+paid; category via distinct item→order |
| K03 | AOV / Omzet kategori per pesanan | K01/K02 | mixed scoped facts | Rp | zero-safe |
| K04 | Rata-rata Waktu Siap | mean(`prep_time_min`) | eligible orders | menit 1 digit | completed nonnull |
| K05 | Pesanan Terlambat | `sum(delayed_flag)/count(valid prep)` | eligible orders | % + n/N | channel-specific SLA |
| K06 | Food Gross Margin | `(K01 − K09)/K01` | sales line facts | % | K01 >0 |
| K07 | Bahan Stok Kritis | count(branch,ingredient with ending_qty < reorder_point) | ledger as-of | pasangan bahan–cabang | branch filter; category N/A |
| K08 | Total Food Gross Profit | `K01 − K09` | sales lines | Rp | not operating net profit |
| K09 | Food COGS | Σ `line_food_cost_idr` | sales lines | Rp | cost from BOM snapshot |
| K10 | Total Unit Terjual | Σ `order_items.quantity` | sales lines | integer | completed+paid |
| K11 | Food Waste Cost | Σ `abs(WASTE movement_qty × movement_unit_cost)` | ledger | Rp | **separate**, not in K09 |
| K12 | Rating Ulasan | mean(feedback.rating) | valid feedback | /5 + n | optional panel |
| K13 | Cancellation Rate | canceled orders / all orders | raw orders | % + n/N | **independent** from revenue |
| K14 | Median Waktu Siap | median(`prep_time_min`) | eligible orders | menit | kitchen context |
| K15 | P90 Waktu Siap | `quantile(0.90)` of prep minutes | eligible orders | menit | kitchen context |
| K16 | Diskon Diberikan | Σ `allocated_discount_idr` | sales lines | Rp | completed+paid |
| K17 | Revenue Growth | `(current−previous)/previous` | sales period | % | only if prior period exists+positive |
| K18 | Item Stock Cover Days | ending_stock / average daily usage last 7 days | ledger+usage | hari | invalid if daily usage=0; optional |

**6 KPI minimal** terpenuhi lewat K01-K06, namun **Overview target**: K01, K02, K03, K04, K05, K06, K07, K08. K09–K18 kontekstual pada halaman masing-masing. Food waste pada Inventory tidak sama dengan food COGS transaksi.

## 5.3 Leading / lagging

- **Lagging:** revenue, completed orders, AOV, food GP, margin realisasi, cancellations, delayed rate historis, customer rating.
- **Leading/proxy operasional:** ending critical stock count, pending reorder estimate/coverage, queue capacity utilization bila simulasi event tersedia. P90 prep time historis tetap **lagging**, meski dapat berfungsi sinyal dini terhadap risiko layanan berikutnya; jangan menandai otomatis sebagai leading tanpa penjelasan.
- KPI dapat bersifat proxy leading dalam konteks tindakan, tetapi label di laporan harus menyebut alasan.

## 5.4 Konvensi filter untuk KPI

**F = FilterContext(date_start, date_end_inclusive, branches, categories)**

- **K01, K06, K08, K09, K10, K16:** filter fact_sales_lines by order_date, branch, menu category; sum line-level fields.
- **K02, K03, K04, K05, K14, K15:** order scope selected through order IDs linked to **at least one item of selected categories**, then distinct order grain. Categorical selection tidak berarti prep time hanya milik kategori tersebut; cantumkan catatan.
- **K07:** as-of end_date, branch; category filter **not applicable to physical on-hand stock** karena bahan dipakai beberapa kategori dan saldo stock milik keseluruhan operasi. Tampilkan badge mikro `Kategori tidak memfilter stok saat ini` di Inventory, bukan angka yang tampak terfilter padahal tidak.
- **K11:** waste movement dalam date range, branch; category filter N/A sebab waste adalah event bahan, bukan menu.
- **K12:** valid feedback dari eligible order scope sesuai date/branch/category bila direlasikan ke order.
- **K13:** cancellation by date/branch; category filter **N/A** karena canceled order tanpa item; tampilkan label pengecualian.

**Contoh anti bug:** kategori Beverage memilih 2 dari 4 line items order `O-100`. Category revenue = Σ hanya 2 baris Beverage; Total Orders = 1 jika order O-100 punya beverage; Kitchen prep time = satu observasi order O-100, tidak 2 observasi.

## 5.5 SLA dan delayed

| Channel | SLA simulasi | Kondisi terlambat |
|---|---:|---|
| DINE_IN | 18 menit | prep_time >18 |
| TAKEAWAY | 20 menit | prep_time >20 |
| DELIVERY | 25 menit | prep_time >25 |

Semua angka SLA dapat diganti satu tempat (`config/simulation.yaml`). Jangan mencampur `completed_at - ordered_at` (service total) dengan `ready_at - ordered_at` (prep). Jika UI menyebut “Kecepatan Persiapan”, gunakan yang kedua. Delayed orders persentase dengan denominator seluruh eligible completed paid orders yang punya prep valid.

## 5.6 Profitabilitas per kategori/menu

```text
line_gross       = qty × historical_unit_price
order_gross      = Σ line_gross
order_discount   = configured deterministic discount (IDR int)
line_discount    = allocated largest-remainder share of order_discount
line_net         = line_gross − line_discount
unit_food_cost   = round_half_up(Σ ingredient qty_per_unit × ingredient_unit_cost)
line_food_cost   = qty × unit_food_cost
line_food_gp     = line_net − line_food_cost
food_margin_pct  = Σ line_food_gp / Σ line_net × 100
```

**Denominator low-margin menu:** gunakan menu revenue **setelah diskon**. Menu tanpa revenue: margin undefined; jangan masuk daftar bottom 10 dengan 0% atau >100% phantom. Jika keuntungan negatif, angka ditampilkan negatif dengan simbol `−Rp...`, bukan disembunyikan.

**Inventory waste accounting:** `waste_cost` dilaporkan di Inventory & optional cost analysis, **bukan otomatis dikurangkan dari food GP**. Kalau ingin “Food Contribution After Waste”, buat metrik tersendiri `Food GP − Waste Cost` dan jelaskan batasannya (waste tidak dialokasikan per menu). Default v1 tidak menampilkan “Net Profit” agar tidak menyesatkan.

## 5.7 Delta periods

`current window = [start,end] inclusive` dengan N hari kalender; `previous window = N hari tepat sebelumnya`, perlu dataset mencakup keseluruhan previous window. Jika tidak ada data lengkap (misal memilih seluruh 30 hari awal dataset), delta `N/A` dengan tooltip `Periode pembanding tidak tersedia`, bukan menghitung dari subset/0.

Growth dari integer sums dan `previous > 0`; turun 15% berarti `growth = -0.15`, tidak diterapkan pada n<3 hari jika alert memerlukan stabilitas.

## 5.8 Automatic insight rule engine

Format struktur rule output:

```yaml
rule_id: ALERT-KITCHEN-01
severity: warning
metric: delayed_rate
scope: {date_start: YYYY-MM-DD, date_end: YYYY-MM-DD, branches: [BR-01], categories: []}
actual_value: 0.135
threshold: 0.10
n: 27
N: 200
title: "13,5% pesanan melewati SLA"
explanation: "27 dari 200 pesanan selesai ..."
action: "Tinjau kapasitas fryer pada jam sibuk."
source_drilldown: "Kitchen Performance"
```

**Rule list target 6:**

| Rule ID | Kondisi | Severity | Teks tindakan | Trigger test |
|---|---|---|---|---|
| A01 | `delayed_rate > 10%` dan eligible n≥20 | warning | Audit station/shift pada jam dan cabang berkontribusi terbesar | n=20, late=3 → trigger |
| A02 | `menu_margin_pct <25%` untuk menu `units_sold≥10` dan `net_revenue>0` | warning | Tinjau BOM, harga dan promosi menu | menu margin24.99%, n10 → trigger |
| A03 | `ending_qty < reorder_point` | critical | Restock bahan/cabang terdampak; tampilkan qty+unit | stock 9, reorder10 → trigger |
| A04 | daily revenue <85% average daily revenue previous 7 complete days, n obs≥7, baseline>0 | info/warning | Telusuri channel dan menu yang menurun | 84% baseline → trigger |
| A05 | `food_margin_pct <30%` dan eligible revenue>0 | warning | Review kategori dengan gross profit rendah | 29.9% → trigger |
| A06 | `p90_prep_time >1.4× SLA_reference` pada channel dipilih, n≥20 | warning | Cek tail wait times, bukan hanya mean | p90=1.5× SLA → trigger |

**A06 detail:** apabila filter memilih banyak channel dengan SLA berbeda, hitung `lateness_ratio = prep_time / sla_min` per order dan bandingkan **p90 lateness_ratio >1.4**. Jangan rata-rata SLA 18/20/25 lalu p90 prep dibandingkan dengan SLA rata-rata. Jika satu channel, bisa tampilkan p90 menit selain ratio. Threshold configurable.

**Threshold boundaries:** `>` untuk persentase threshold, `<` untuk low stock, `= threshold` **tidak trigger** kecuali dinyatakan. A04 gunakan **rolling baseline** hari sebelum hari target, bukan window saat ini yang mencakup hari target (*data leakage*). Kategori/branch jika sampel kecil → `not_evaluable`, bukan alert positif/negatif palsu.

### Insight prioritas & suppression

1. Render maksimal 4 card aktif per view (sort critical > warning > info, lalu impact magnitude); sisa `Lihat semua` expander.
2. Jika tidak ada masalah, tampilkan `Tidak ada ambang yang terlampaui pada data terpilih` **bukan** “semua operasi baik” karena rules terbatas.
3. Jika data kurang, tampilkan `Insufficient evidence`; jangan klaim target tercapai.
4. Setiap alert harus memuat angka actual/threshold, satuan, N denominator, branch/date scope, rekomendasi yang **disarankan**, bukan tindakan otomatis.
5. Rule hasil pure function dari DataFrames + FilterContext, bukan text random.
6. Alert kategori N/A mengikuti filter semantics matriks.

## 5.9 Metric API yang wajib diuji

```python
# Signature spec (bukan implementasi final)
@dataclass(frozen=True)
class FilterContext:
    start_date: date
    end_date: date
    branch_ids: tuple[str, ...]  # empty tuple = semua
    categories: tuple[str, ...]  # empty tuple = semua

# pure functions; no st.* inside src/metrics
get_overview_metrics(bundle, filters: FilterContext) -> dict[str, MetricValue]
get_sales_metrics(bundle, filters: FilterContext) -> pd.DataFrame
get_kitchen_metrics(bundle, filters: FilterContext) -> pd.DataFrame
get_stock_snapshot(bundle, cutoff_date: date, branch_ids=()) -> pd.DataFrame
run_business_rules(bundle, filters: FilterContext) -> list[BusinessInsight]
```

Dataclass MetricValue memuat `value`, `unit`, `numerator`, `denominator` optional, `definition`, `filter_scope`, `data_status` dan `source_ids`; jika expensive, source_ids bisa dipakai debug test saja.

## 5.10 Golden fixtures untuk unit test

- **FIX01:** Rp35.000 gross − Rp3.500 diskon = Rp31.500 net; COGS Rp13.000; GP Rp18.500; margin 58.730158% (sesuai doc 03).
- **FIX02:** 1 order berisi 3 category lines harus dihitung sebagai **1** total order, bukan 3.
- **FIX03:** 1 delivery order prep 24 menit dengan SLA25 = **tidak terlambat**; 26 = terlambat.
- **FIX04:** 1 dine-in prep18.00 menit = **tidak terlambat**, 18.01 = terlambat.
- **FIX05:** Bahan opening50, receipt20, usage35, waste2 → as-of ending33; stok per tanggal tidak memakai date filter start.
- **FIX06:** Category Burger berisi order A+B; rice order B saja → subset burger order count2, revenue hanya burger lines.
- **FIX07:** No transactions → revenue0, orders0, AOV and margin N/A, aturan penjualan/layanan tidak dapat dievaluasi dan A03 tetap mengevaluasi ledger.
- **FIX08:** Menu 9 unit margin20% **tidak** memicu A02 karena minimum units10.
- **FIX09:** Previous period unavailable → growth N/A.
- **FIX10:** Rule n20 late2 delayed10.0% → **tidak** memicu A01 (`>`), n20 late3 =15% → memicu.
