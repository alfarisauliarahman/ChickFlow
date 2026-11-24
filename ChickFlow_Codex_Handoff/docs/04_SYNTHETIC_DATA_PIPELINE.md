# 04 — Generator data sintetis: realism, cleaning, reproducibility, data quality

## 4.1 Tujuan generator

Dataset tidak boleh berupa kumpulan CSV acak yang kebetulan dapat diplot. Ia harus mewakili **sistem operasi restoran konsisten**: transaksi → line items → resep/BOM → penggunaan bahan → stok → food cost → pendapatan/GP, dan transaksi → station/queue → prep time → SLA/delay → feedback. Seluruh hubungan dapat diperiksa ulang.

**Generator bukan mesin penentu nilai tugas**: metrik kinerja baseline harus dihitung setelah data jadi; jangan mengarang hasil dan jangan mengubah data diam-diam demi membuat KPI tampak baik.

## 4.2 Input config dan seed

Contoh bentuk `config/simulation.yaml` (format referensi, bukan sudah ada):

```yaml
simulation:
  seed: 20261001
  start_date: "2026-10-01"
  days: 30
  target_orders: 3600
  timezone: Asia/Jakarta
  opening_hour: 10
  closing_hour: 22
  cancellation_probability: 0.025
  feedback_probability: 0.22
order_mix:
  min_items: 1
  max_items: 4
  channel_weights: {DINE_IN: 0.38, TAKEAWAY: 0.28, DELIVERY: 0.34}
  peak_hours: [12, 13, 18, 19]
sla_minutes:
  DINE_IN: 18
  TAKEAWAY: 20
  DELIVERY: 25
alerts:
  late_rate_warning_pct: 10
  margin_menu_warning_pct: 25
  food_margin_warning_pct: 30
  critical_stock_threshold: 1.0
```

**Kontrak config:** divalidasi dengan batas/enum yang eksplisit; seed disimpan di manifest, jangan pakai `np.random` global. Gunakan `numpy.random.default_rng(seed)` dan turunan generator yang dijadwalkan urut sehingga output deterministik.

## 4.3 Generator step by step

### Tahap A — master data

1. Buat 3 cabang simulasi dan koordinat pusat kota yang ditinjau, demand multipliers berbeda, station capacities berbeda.
2. Buat 20–24 menu dengan harga IDR, kategori, station dan popularity weight.
3. Buat 22–28 bahan, satuan, biaya/unit; hindari costing Rp0.
4. Buat BOM menu dari ingredients dengan qty positif; tiap menu ≥1 ingredient, termasuk combos flattened.
5. Hitung `unit_food_cost_idr` baseline per menu dari BOM (precision policy tersentral).
6. Buat policy opening_stock, reorder_point dan lot untuk setiap cabang-bahan.
7. Validasi kelayakan margin dan menu sehingga ada skenario menarik secara *wajar*: tidak semua menu sempurna, tidak semua menu rugi.

### Tahap B — demand calendar (tidak uniform)

- Total target 3.600 order secara deterministik; bagi di 30 hari × 3 cabang berdasar demand multiplier, weekday/weekend factor, event multiplier kecil, dan stokastik seeded.
- Gunakan `multinomial` atau allocation berbobot sehingga total order **persis** target walau distribusi bervariasi.
- Simulasikan jam makan siang 11–14 dan malam 17–20 dengan mixture distribution; sepanjang 10–22 masih ada transaksi.
- `branch_id` tidak uniform; Padang volume lebih banyak, yang lain tetap sampel memadai.
- Channel mix bercabang: misalnya Padang delivery tinggi, cabang lainnya lebih banyak dine-in. **Ini parameter simulasi, bukan pengetahuan faktual nyata.**
- Weekends memiliki volume berbeda dari weekdays; catat faktor dalam config.

### Tahap C — basket, prices, discounts, cancellations

1. Bagi status completed/canceled dengan target 2–3% canceled, seeded dan tidak menghitungnya sebagai completed.
2. Completed order berisi 1–4 line item, qty 1–3 per item; menu dipilih berbobot popularitas yang dapat bergantung pada jam/channel.
3. Prices disalin sebagai snapshot dari `menu.list_price_idr`, dengan skenario promosi harga terkontrol bila diperlukan.
4. Diskon bisa 0/5/10/15% dengan probabilitas realistis **sintetik**. Terapkan sebagai integer rupiah dan alokasikan ke line item dengan largest remainder; tidak ada diskon negatif.
5. Compute `line_net`, `line_cogs`, `line_gp` lalu `orders.gross`, `discount`, `net`; **reconcile 100%**.
6. Canceled order tidak memiliki order_items untuk versi 1, tidak memiliki food consumption/revenue/GP; tetap ada di status monitoring.

### Tahap D — kitchen queue dan SLA (bukan delayed random)

- Pisahkan cabang dan station (FRYER, GRILL, ASSEMBLY, DRINK), masing-masing punya `capacity_slots` parameter ≥1.
- Proses completed orders secara chronological. Untuk setiap line item, hitung `work_minutes = menu.base_prep_min × quantity_factor × branch/staff_multiplier × jitter`, dengan jitter bounded (contoh 0.85–1.15).
- Untuk station yang sama, pilih slot yang tersedia paling cepat (`next_free_at`). `start_at=max(ordered_at,next_free_at)`; finish = start + work.
- Beberapa station dalam satu order berjalan paralel; `ready_at = max(finish_at all items) + packing_minutes`.
- `completed_at = ready_at + handoff_minutes` (kedua parameter bounded, positif).
- `prep_time_min = (ready_at-ordered_at).total_seconds()/60`.
- `sla_min` ditentukan oleh channel; `delayed_flag = prep_time_min > sla_min` (strict >, bukan ≥).
- Peak load memperpanjang queue secara **mekanistik** (arrival rate > capacity), bukan karena delayed random. Jika queue meledak berjam-jam, tuning station/capacity; simpan tuning rationale.
- Canceled status tidak masuk antrean, jika cancel sudah sebelum produksi. Jangan pura-pura canceled diproses dan tetap distok sebagai usage.

### Tahap E — inventory ledger

1. Event `OPENING` pada sebelum awal transaksi, per branch × ingredient, senilai `opening_qty`.
2. Proyeksikan consumption dari **completed order line × recipe** dan buat event `USAGE` pada `ready_at`, per order × ingredient teragregasi; `signed_qty` negatif.
3. Buat `RECEIPT` restock otomatis berdasarkan reorder point dan lot pada waktu sebelum kebutuhan, sebisa mungkin dengan lead-time 1 hari.
4. Jika projected shortage akibat stok rendah, buat `RECEIPT` bertipe alasan `emergency_restock` (pembelian darurat sintetis) sebelum USAGE, **dicatat** dan menjadi temuan operasional; jangan langsung mengubah stock tanpa event.
5. Buat `WASTE` deterministik terpisah (mis. spoilage pada bahan tertentu per hari) dan jangan membuat total saldo negatif.
6. Semua movement diurutkan `(occurred_at, movement_type_sequence, movement_id)` agar pada timestamp sama receipt sebelum usage.
7. Reconcile event `USAGE` ke resep secara tepat dalam kuantitas basis; selisih 0 setelah precision policy.
8. Generate daily end-of-day snapshot dari cumulative ledger untuk inspect, bukan sebagai source-of-truth.

**Desain anti bias:** `RECEIPT` bukan pendapatan dan bukan biaya bahan yang otomatis menjadi COGS saat dibeli; pembelian stok = kenaikan aset persediaan dalam logika sederhana. Food COGS diakui saat menu completed digunakan; waste cost ditampilkan **terpisah**, tidak digabung dua kali.

### Tahap F — feedback text

- Sampling hanya completed orders; probability ~0.22, tema didistribusikan.
- Text memakai kalimat Bahasa Indonesia yang bervariasi (contoh: “Ayam renyah, tapi menunggu agak lama”). Variasi tidak menyertakan nama/nomor telepon.
- Rating 1..5 dan review theme dapat tergantung delayed, namun probabilistik, tidak hardcode semua delay buruk.
- Word cloud memakai token dari actual `review_text`, hilangkan stopwords dan filler kata `chickflow`, bukan sekadar gambar dekoratif yang dibuat manual.

## 4.4 Intervensi kualitas data untuk Bab IV

Karena tugas mengharuskan pembersihan data, buat pipeline: **`canonical_generated/` internal (truth) → `data/raw/` dengan injeksi masalah yang terkendali → `data/clean/` setelah cleaning → validasi**.

| Injected issue | Skala kecil rancangan | Target cleaning | Boleh mengubah fakta? |
|---|---|---|---|
| Row duplikat `orders` | ~0.5% order | keep canonical ID once | tidak |
| Format timestamp berbeda tetapi valid | ~1% | normalize ISO WIB | tidak |
| Whitespace/casing kategori | ~1% | normalize controlled enum | tidak |
| Null `review_text` | ~2% feedback | fill empty & flag; keep row | tidak |
| Null `menu.category` di salinan raw | ~0.5% | restore via master menu ID | tidak |
| Outlier prep time valid | sebagian kecil real simulation | flag+investigate, **tidak hapus otomatis** | tidak |
| Foreign key broken, price changed | **JANGAN injeksi** kecuali pemulihan deterministik dapat dibuktikan | fail rather than fabricate | tidak |

Parameter injection terpisah dari simulator supaya dapat dinonaktifkan. Simpan `data_quality_injections.csv` (record ID, field, injected problem, expected fix) untuk QA; ini **bukti audit**, bukan dipakai langsung oleh chart dashboard. Cleaning harus **idempotent**, menghasilkan clean dataset konsisten dengan canonical truth pada data penting.

## 4.5 QA pipeline gates

**Gate A — entity integrity:** PK unique, FK complete, datetime valid, enums valid, minimal row/date/table counts terpenuhi.  
**Gate B — financial integrity:** total item gross, net, allocated discount, COGS, GP sesuai order & BOM tanpa double count.  
**Gate C — operational integrity:** prep >=0, SLA valid, flags computed, canceled excluded.  
**Gate D — inventory integrity:** event usage equals consumption, stock never negative, no movement per nonexistent branch/item.  
**Gate E — reproducibility:** same seed + code + config -> normalized clean CSV SHA256 equal.  
**Gate F — visual readiness:** seluruh chart memiliki sample size memadai / empty fallback; 3 cabang punya data.

Jika Gate B atau D gagal, **jangan lanjut membangun dashboard**. Betulkan generator dulu. Dokumentasi exception secara eksplisit bila ada skenario tak dimodelkan.

## 4.6 Struktur pipeline CLI yang harus dibuat Codex

```bash
python -m chickflow.data.generate --config config/simulation.yaml --output data/raw
python -m chickflow.data.clean --input data/raw --output data/clean
python -m chickflow.data.validate --input data/clean --report reports/data_quality.json
python -m chickflow.data.build_marts --input data/clean --output data/marts
python -m chickflow.reports.eda --input data/clean --output reports/eda
pytest -q tests/data tests/metrics
```

**Ekspektasi:** `python -m` perintah tidak tergantung working directory luar repo, file input divalidasi, error pesan deskriptif, path cross-platform, exit code nonzero untuk kegagalan kualitas. `--seed` boleh override melalui config.

## 4.7 Manifest hasil generate

`data/manifest.json` minimal memuat `generator_version`, `seed`, `config_sha256`, `range_start`, `range_end`, `generated_at` (tidak memengaruhi hash clean), jumlah baris tiap tabel, SHA256 CSV, daftar issues yang diinjeksikan dan dibersihkan, library/package versions, catatan interpretasi data sintetik.

**Determinisme:** jangan memasukkan `generated_at` runtime ke dalam CSV atau hash data; timestamp audit berada pada manifest metadata yang memang boleh berubah.

## 4.8 EDA wajib memakai library yang benar

- **pandas:** `.info()`, `.describe(include='all')`, missingness, uniqueness, joins, crosstab.
- **numpy:** generator seeded, statistik, quantile, histogram arrays.
- **matplotlib:** static line revenue harian + bar kategori, dengan judul/label/legenda.
- **seaborn:** histogram/KDE prep dan boxplot branch, set `hue`/palette eksplisit jika dipakai untuk menghindari warning versi baru.
- **plotly:** chart interaktif halaman dan peta.
- Buat `reports/eda/` PNG plus teks temuan; screenshot matplotlib+seaborn disiapkan untuk laporan, bukan diwajibkan ada di Streamlit.

## 4.9 Output yang diperiksa saat penutupan fase data

- `data/raw/*.csv`, `data/clean/*.csv`, `data/marts/*` (Parquet opsional bila interoperabilitas environment tervalidasi).
- `data/manifest.json`, `reports/data_quality.json`, `reports/eda/`, `docs/data_dictionary.md`, `docs/erd.md`, `tests/fixtures/`.
- Laporan ringkas jumlah trans, days, join failures, late rate, margin distribution, branch mix, canceled count, stock critical, injection/cleaning counts; semua **dihitung otomatis**.
- Kontrak tidak melanggar “minimal 500 order dan 7 hari” meskipun data batal dihitung terpisah.

## 4.10 Variasi dan boundary tests generator

- Jika user memilih seed lain, total target orders tetap tercapai, dan tidak ada invalid key/negative stock.
- Seed berbeda menghasilkan distribusi berbeda dalam limit kewajaran.
- Jam puncak terlihat sebagai pola statistik (tetapkan toleransi, contoh rata-rata orders/hour pada 11–13 dan 18–20 melebihi off-peak), tetapi jangan menduplikasi baris untuk menipu target.
- 0% discount seluruh orders masih menghasilkan KPI tanpa divide-by-zero.
- Dataset satu cabang sebagai *test fixture* tidak harus ada semua cabang di chart scope; app menampilkan “tidak cukup data” jika relevan.
- Semua sold menu memiliki recipe dan cost; unsold menu tetap dapat ada di master untuk coverage dan nol penjualan.
