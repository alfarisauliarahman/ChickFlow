# 06 — Six mandatory page specifications (functional + visual + state)

**Prinsip tiap halaman:** headline menjawab suatu keputusan, KPI atau chart penting terlihat tanpa scroll panjang, data lineage jelas, insight berorientasi tindakan, dan label filter terlihat. Semua halaman punya state: `loading`, `loaded`, `empty`, `partial`, `error`.

## 6.0 Navigasi global

```text
CHICKFLOW | Operations Intelligence
├── 01 Overview                 → Apa yang terjadi dan prioritas apa?
├── 02 Orders                   → Kapan, di mana, channel apa?
├── 03 Kitchen Performance      → Mengapa lambat, seberapa parah?
├── 04 Inventory                → Bahan mana perlu perhatian?
├── 05 Sales & Reports          → Menu dan tren mana menyumbang revenue?
└── 06 Food Cost & Profit       → Dari mana food gross profit berasal?
```

Topbar: title, `Data Sintetis` hint, data cut off, range picker, branch multiselect, category multiselect, reset. Sidebar: logo/text, six page nav, active page indication. Footer: data source, metric conventions, build version.

### Global state contract

- Date start <= date end; allowed dates intersect dataset; default last 7 days dataset, bukan local today yang di luar data.
- Branch empty selection = ALL, category empty selection = ALL; `Semua Cabang` / `Semua Kategori` harus eksplisit agar tidak membingungkan.
- Periode pembanding opsional, default off jika kurang histori.
- `Refresh Data` reload files via cache clear only after validation; jangan rerun generator diam-diam.
- `Reset filters` mengembalikan periode default, all branches, all categories, dan scroll/selection chart opsional clear.
- **Scope tag:** modal KPI yang tidak dipengaruhi kategori wajib diberi label `Semua kategori`/`Kategori tak berlaku`.

## 6.1 Page 1 — Overview (Executive Command Center)

**Pertanyaan inti:** bagaimana kesehatan ChickFlow, apa yang harus ditangani pertama?

**Prioritas layout:** area first screen: title & context, 8 KPI card grid (4×2 desktop/2×4 tablet), highlighted insight strip, revenue trend lebar dan operational health chart. Detail breakdown di bawah.

**KPI:** K01 Net Revenue, K02 Completed Orders, K03 AOV, K04 Avg Prep, K05 Delayed %, K06 Food Gross Margin, K07 Critical Stock Items (category N/A), K08 Food GP. Delta prior-period hanya valid bila full comparison window exists.

**Grafik:** line net revenue by date (V-Q01), bar revenue by branch (V-Q04), mini delayed rate by branch/channel, optional Top menu concise bar. Peta *tidak perlu memenuhi halaman Overview* jika hanya mengganggu; geografis di Sales & Reports.

**Insight:** prioritized A01–A06 (empat kartu utama dan panel Lihat semua), masing-masing `angka -> kondisi -> rekomendasi -> halaman detail`. Card critical stock jump ke Inventory; delay ke Kitchen; low margin ke Profit.

**Interaksi:** filter global, hover sparkline/line, legend toggles; klik CTA `Tinjau detail` pindah page sesuai rule. Jangan membuat angka statis sebagai placeholder ketika data tidak ada.

**Table:** 3 cabang `Revenue | Orders | Delayed | Food margin` ringkas, row sorted by revenue default; branch sort toggle.

**Acceptance:** 8 KPI valid; chart scope sama; stock N/A category microcopy; branch compare tidak mean-of-percentage; first impression action obvious.

## 6.2 Page 2 — Orders (Demand & Channel)

**Pertanyaan:** kapan order masuk, tipe apa paling sibuk, dan transaksi mana perlu ditelusuri?

**KPI:** eligible completed orders, canceled orders/rate (category N/A), peak hour, AOV, delivery share, unit sold.

**Grafik prioritas:** heatmap `weekday × hour` order count (V-Q03), grouped bar orders/AOV by channel (V-Q09), stacked channel mix per branch, hourly order trend. Warna heatmap adalah rata-rata order per hari pengamatan. Tooltip menampilkan jumlah order unik dan jumlah hari pengamatan.

**Table:** order detail read-only dengan ID, datetime, branch, channel, items summary, order net, prep min, delayed status. Paging/search (string order_id), sort, CSV download. Jika category active, tampilkan line subtotal kategori dan label `Subtotal menu kategori terpilih` untuk menghindari kebingungan terhadap full order total.

**Workflow:** user melihat `19:00 Jumat` peak → filter branch & channel → table sorted high prep → klik order → expander details (line item, SLA, margin tidak perlu semuanya).

**Acceptance:** canceled orders tidak berkontribusi revenue; filtered order list unik; category affects status of completed order in item scope; empty date shows helpful prompt.

## 6.3 Page 3 — Kitchen Performance (Operational Diagnostics)

**Pertanyaan:** berapa lama menyiapkan, apakah ada keterlambatan, dan di mana bottleneck terjadi?

**KPI:** avg prep, median prep, P90 prep, delayed orders n/N, throughput orders/hour, busiest station *simulated indicator* jika event queue tersedia.

**Grafik wajib:** histogram/kde prep time (V-Q05), **box plot** prep per branch (V-Q10), grouped delayed rate by branch/channel (V-Q06), hourly volume vs median prep (dua chart dengan aligned x, jangan dual axis yang menyesatkan), optional load vs p90 scatter.

**Interpretasi:** jelaskan median vs p90; confidence caution bila sample size rendah; outlier ditandai/tooltip; chart annotations SLA per channel hanya bila satu channel dipilih, kalau multichannel gunakan `prep/SLA` ratio chart agar tidak membandingkan apples-oranges.

**Workflow:** warning A01 → klik Kitchen → inspect delayed rate per branch → pilih branch + one channel → lihat distribusi, p90 dan jam → saran evaluasi station capacity (hipotesis, bukan pembuktian sebab).

**Acceptance:** strict > SLA, non-null prep only eligible; boxplot didukung n cukup; chart tidak menghitung line items sebagai banyak order; navigasi dari alert bekerja.

## 6.4 Page 4 — Inventory (Stock & Waste Monitor)

**Pertanyaan:** stok mana kritis pada cutoff date? Apa penggunaan dan waste yang perlu ditinjau?

**KPI:** critical stock pairs, ingredients with zero stock, waste cost period, receipts count, optional days-of-cover median valid; tidak tampilkan total stock across units sebagai satu angka.

**Tabel utama:** `Cabang | Ingredient | Unit | Stok akhir as-of | Reorder point | Gap | Status` dengan filter `critical/all`, sort by gap ratio; status CSS + text.

**Grafik:** grouped bar current stock vs reorder point untuk top 10 critical pairs (V-Q08), waste cost by ingredient (V-Q12), time-series stock level per selected ingredient (optional), 7-day usage trend for contextual restock.

**Filter scope:** `Tanggal` untuk saldo **menggunakan end date** sebagai cutoff; `Rentang tanggal` untuk waste/receipts. `Cabang` berlaku keduanya. **`Kategori` tidak mengubah fisik stock-on-hand**, tetapi boleh memfilter attributed usage via sold recipe by category dengan subtitel. Jelaskan di help icon; ini keputusan desain yang wajib, jangan menganggap filter diabaikan diam-diam.

**Units:** semua per bahan; chart antar bahan dengan beda units sebaiknya menggunakan **persentase terhadap reorder point** agar comparable, atau satu bahan/unit dalam satu chart. Jangan plot stok gram dan pcs pada satu sumbu angka.

**Acceptance:** historical as-of reconcile; tanda stock critical `< reorder`, zero stock count; baseline tanpa ledger events -> diagnostic fallback.

## 6.5 Page 5 — Sales & Reports (Menu Intelligence)

**Pertanyaan:** pendapatan dari mana, menu apa laris, bagaimana pola cabang?

**KPI:** net revenue, order count, AOV, units sold, discount value, revenue growth (jika prior periode lengkap).

**Grafik:** daily revenue line (V-Q01), top menu by units horizontal bar (V-Q02), category net revenue bar/treemap (pilih bar jika banyak kategori), revenue vs branch bar (V-Q04), channel AOV (V-Q09), **point geographic map** cabang (V-G01).

**Peta:** titik simulasi pusat kota, lat/lon dari `branches`, size by net revenue within selected period, tooltip label city/branch/order count/revenue, not real address. Jika memilih satu cabang, peta tetap satu pin dengan status filter. Gunakan `px.scatter_map` (MapLibre family), hindari legacy `scatter_mapbox`; jika offline tiles gagal, fallback geospatial point visualization dengan disclaimer (bukan hilang total).

**Table:** menu leaderboard sorted unit sold/revenue/GP, category, average discount percent, branch count, export CSV.

**Acceptance:** revenue by category Σ = total revenue selected, branch Σ = total revenue selected, no row multiplication; when selecting category, best menu chart only category.

## 6.6 Page 6 — Food Cost & Profit (Cost & Margin)

**Pertanyaan:** produk mana menguntungkan secara *food gross profit*, bagaimana dampak discount dan BOM?

**KPI:** net revenue, COGS, food gross profit, food gross margin, average discount/order, low-margin menu count (sample threshold).

**Grafik:** scatter units sold × food gross margin (V-Q07; bubble = revenue optional), bar gross profit contribution by category (V-Q11), bar bottom 10 menu margin with threshold line, waterfall/stacked comparison revenue→discount→COGS→food GP (jelaskan quantity, hindari grafik menipu), optional boxplot menu margin across branches.

**Table:** menu `Price | Units | Gross | Alloc discount | Net sales | Food COGS | Food GP | Margin % | Flag`. Click/expander menu details menampilkan BOM cost per ingredient, pricing snapshot caveat, dan counted orders.

**Terminologi:** header **Food Gross Profit**, bukan **Net Profit**. Jangan menyatakan value = revenue - total expenses karena payroll, rent, tax, delivery fee tidak tersedia. Waste cost ditampilkan sebagai separately labeled item bila ingin konteks, bukan digabung ke COGS transaction.

**Acceptance:** margin % uses aggregated net denominator; no margin if 0 net sales; allocated discounts reconcile; menu BOM cost matches snapshot; category table Σ GP = overall GP.

## 6.7 Empty/loading/error states lintas halaman

| Situasi | UX yang benar | UX yang dilarang |
|---|---|---|
| Tidak ada order pada filter | pesan `Tidak ada pesanan selesai pada kombinasi filter` dan reset suggestion | chart placeholder palsu, divide 0 |
| 1 branch terpilih | chart branch compare bisa berubah menjadi single-bar + insight | error Plotly category none |
| Data corrupted/missing | banner error + file path + apa yang perlu diperbaiki | KPI “0” dan klaim data valid |
| Baseline delta unavailable | `—` + tooltip `Riwayat belum cukup` | `+∞%` |
| Category not applicable to stock/cancel | note eksplisit | angka diam-diam berubah acak |
| Input tanggal invalid | validasi, disable query | traceback |
| Map tiles offline | fallback visual + warning halus | blank chart |

## 6.8 UI copy dan microcopy examples

- `Pendapatan bersih` (tooltip: diskon sudah dikurangkan; hanya completed paid).
- `Pesanan selesai` (tooltip: jumlah order unik, tidak termasuk cancel).
- `Terlambat dari SLA` (contoh `14,2% · 36 dari 253` bukan hanya `14,2%`).
- `Stok per 30 Okt 2026` (bukan `stok selama 1–30 Okt` bila yang ditampilkan saldo).
- `Margin kotor makanan` (tooltip: tidak mencakup biaya tenaga kerja dan overhead).
- `Data simulasi untuk tugas Visualisasi Data` pada top banner/help, tidak disembunyikan.
