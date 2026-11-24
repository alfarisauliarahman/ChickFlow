# PHASE PROMPTS — Use these in Codex sequentially if one-shot implementation gets too broad

Use the milestone order in the roadmap. Use **one phase per Codex turn** when debugging or when the coding agent loses context. Do not let Codex move to the next phase until the previous gate is proven green. All prompts assume the full blueprint exists in working repo.

## Prompt 0 — Foundation

```text
Baca README, AGENTS.md, docs/01, docs/09, docs/12, docs/14 dan checklists/DELIVERY_GATES.md. Kerjakan Phase 0 task CF-001..CF-007: inisialisasi repository, paket Python dengan src/chickflow, editable install, config validation dasar, pytest harness, README awal, gitignore, ADR. Jangan buat dashboard palsu dulu. Jalankan pip install -e ., import smoke, pytest -q; tunjukkan hasil nyata dan gate P0. Tetap gunakan konsep ChickFlow asli, bukan sample Restora.
```

## Prompt 1 — Dimension model and seed catalogs

```text
Kerjakan Phase 1 CF-010..CF-017. Implementasikan master data branches/menu/ingredients/recipes/branch_inventory_policy persis berdasarkan docs/03 dan docs/15, 24 menu, 27 bahan, 3 cabang. Cost menu HARUS dihitung dari BOM. Tulis ERD + kamus data dan unit tests PK/FK/recipe coverage. Laporan ringkas jumlah row & cost SKU yang dihitung. Jangan hardcode KPI hasil di UI.
```

## Prompt 2 — Operations simulator and data cleaning

```text
Kerjakan Phase 2 CF-020..CF-032 menurut docs/04/03/15. Bangun generator deterministic 3600 orders/30 hari, time peaks, completed/cancelled, item & allocated discounts with largest remainder, queue kitchen + per-channel SLA derived, ledger inventory OPENING/USAGE/RECEIPT/WASTE, feedback Indonesian text. Inject raw data quality issues secara controlled, cleaning idempotent, validation strict, manifest hashes, static EDA Matplotlib & Seaborn. Jalankan 2 same-seed generations untuk cek reproducibility dan D-01..22. STOP jika Rp reconciliation atau stok negatif gagal.
```

## Prompt 3 — Facts, KPIs, inventory as-of and insights

```text
Kerjakan Phase 3 CF-040..CF-052. Implementasikan fakta line-level vs order-level, immutable FilterContext, full applicability matrix doc10, KPI registry doc05, food gross profit not net profit, stock as-of all past movements, rules A01..A06 with n minimum. Tambah FIX01..FIX10, M-01..20 dan R-01..14 tests. Jangan lanjut jika revenue/cost/stock mismatch. Simpan metric_dictionary.md.
```

## Prompt 4 — Plotly and static visualization catalog

```text
Kerjakan Phase 4 CF-060..CF-072 sesuai docs/07. Buat figure-building pure functions, exact 12 quantitative chart registrations, word cloud dari review text (bukan gambar dekoratif), order process flowchart, MapLibre point map 3 kota fiktif + fallback offline. Pastikan line/bar/hist/scatter/box disertai labels/n/units, chart registry PB↔V dan 5 libraries benar-benar dipakai. Simpan bukti PNG dari EDA bila tersedia. NO clone Restora layout/style.
```

## Prompt 5 — Shell and design system

```text
Kerjakan Phase 5 CF-080..CF-089. Bangun Streamlit st.navigation 6 pages, global three filters date/branch/category persisted via session_state, cached validated DataBundle, KPI cards, insights, download, no-data/loading/error state, synthetic disclaimer. Terapkan desain ChickFlow navy–amber docs/08, bukan Restora. Test navigation 1366px dan 768px, jangan isi fake metrics.
```

## Prompt 6 — Six real pages

```text
Kerjakan Phase 6 CF-100..CF-108. Implementasikan keenam modul benar-benar fungsional berdasarkan docs/06: Overview(8 KPI+insights), Orders(heatmap, channels, table, wordcloud, flowchart), Kitchen(hist+box+delay), Inventory(as-of ledger, critical, waste), Sales(revenue, menu rank, fictional branch map), Profit(BOM cost, food GP/margin). Uji filter matrix docs/10, no-doubles, date boundaries, no-data, nav drilldown, export. Jalankan tests dan browser smoke. Jangan mengklaim selesai sampai enam halaman bekerja dengan data computed.
```

## Prompt 7 — Test, visual audit & prototype evidence

```text
Kerjakan Phase 7 CF-120..CF-129. Jalanilah semua D/M/R/U tests, perbaiki kegagalan. Lakukan visual QA viewport 1366/1920/768; screenshot asli. Audit hierarchy, consistency, user feedback, accessibility, cold/warm performance. Siapkan instrumen uji usability 3 tasks + 3 second test untuk 5 responden. JANGAN mengarang responden atau skor; jika saya belum memberikan data feedback nyata, tandai uji pengguna PENDING dan sediakan form/log; lakukan perubahan UI berdasarkan issue teknis yang benar-benar ditemukan.
```

## Prompt 8 — Delivery & report evidence

```text
Kerjakan Phase 8 CF-140..CF-150. Verify fresh install and reproducible generator; pin versions; README with working CLI; no secrets; screenshots each page with seed+filter; ERD/metrics/visualization registry synchronized; artifact test reports; report evidence mapping Bab I–IX, AI use log; demo storyboard 3–5 minutes. Fokus project-ready, bukan menyusun final academic report yang butuh hasil uji pengguna asli. Berikan summary pass/fail checklist evidence and exact run commands.
```

## Debug prompts for common failures

**Mismatch revenue:**

```text
Jangan ubah angka mentah asal-asalan. Isolasi order_id yang gagal, tampilkan line gross, allocated discounts, line net vs header, cari join duplication. Tambahkan regression test dan jalankan D09/M01/M18. Fix function source bukan menambal UI.
```

**Wrong inventory when date changes:**

```text
Stock as-of harus sum seluruh movement sejak OPENING sebelum tengah malam WIB setelah end_date, bukan hanya selected date range. Tambahkan fixture opening50+receipt20−usage35−waste2=33. Buktikan stok invariant terhadap start_date jika end_date dan branch sama, lalu jalankan M12–M14.
```

**Bad filter category:**

```text
Bangun set DISTINCT order IDs setelah filtering category on line items. Revenue only selected lines, order-level prep once. Category never filters physical on-hand stock. Tambahkan test order dengan beberapa SKU kategori dan cek denominator, serta microcopy N/A untuk inventory.
```

**UI looks like sample/restora:**

```text
Kembali ke docs/08 original ChickFlow Ops Control Room. Jangan gunakan gambar, layout, palet, ikon dan design language Restora. Ganti dengan brand token dan information architecture ChickFlow. Ambil screenshot real app at 1366px untuk QA.
```
