# 14 — Risk register, design decisions, change governance, project limits

## 14.1 Risk register

| ID | Risiko | Likelihood × impact | Mitigasi preventif | Bukti mitigasi |
|---|---|---|---|---|
| RK-01 | Revenue terhitung ganda karena join orders→items | H×H | facts terpisah + exact recon tests | D-09/M-03/M-18 |
| RK-02 | Stok akhir salah setelah filter tanggal | H×H | cumulative ledger to end date, not range sum | M-12/M-13 |
| RK-03 | Category filter di Kitchen menghitung item bukan order | M×H | distinct order set semantics | M-04/M-05 |
| RK-04 | Food cost random tidak konsisten BOM | H×H | compute recipe costs, cost snapshot checks | D-11/D-16 |
| RK-05 | Banyak grafik tetapi bukan 5 family/2 qualitative/1 geo | M×H | V registry and coverage audit | Gate P4 |
| RK-06 | Dashboard bagus tapi performance lambat | M×M | caching, marts, measure p95 | NFR-03/CF-127 |
| RK-07 | Contoh Restora memengaruhi desain tanpa sengaja | M×H | freeze product charter, original brand tokens | design review |
| RK-08 | RPS vs template beda kode/CPMK | H×M | template proyek controls specs, ask teacher administratively | doc13 note |
| RK-09 | Synthetic data terlalu mulus tak ada masalah | M×M | realistic variation + audit scenario without fabricating findings | EDA baseline |
| RK-10 | Synthetic data terlalu kacau sehingga semua metrics absurd | M×H | bounded distributions, scenario checks, seeded repeatability | data validation |
| RK-11 | Salah sebut “net profit” | M×H | use Food Gross Profit only, limitations tooltip | terminology audit |
| RK-12 | Peta MapLibre memerlukan internet pada demo | M×M | offline geospatial fallback, smoke test | U-09 |
| RK-13 | Filter kosong membagi dengan nol atau crash | M×H | zero-safe MetricValue and no-data state | M-10/M-11 |
| RK-14 | Langsung coding enam halaman sebelum data valid | H×H | strict P2/P3 data correctness gates | roadmap |
| RK-15 | Dokumentasi laporan terlambat, screenshot/test hilang | H×H | evidence captured phase by phase | screenshots manifest |
| RK-16 | Library update memecahkan API lama | M×M | pin tested versions, Streamlit & Plotly official docs | clean install |
| RK-17 | Aset/font/logo copyright tidak jelas | M×M | original simple logo, licenses audit | assets README |
| RK-18 | Scope melebar ke AYCE/logins/POS | H×M | Won't list + changes require review | ADR |
| RK-19 | Codex mengklaim berhasil tanpa menjalankan test | H×H | require commands/exit/output at phase review | phase reports |
| RK-20 | Data geografis mengklaim outlet nyata | M×M | representative coords disclaimer | map caption |

## 14.2 Decision hierarchy — frozen and flexible

### Frozen (tidak boleh diubah Codex hanya karena selera)

- ChickFlow fast-food fried chicken, bukan Restora dan bukan SeoulGrill AYCE.
- 3 cabang simulasi (Padang/Bukittinggi/Payakumbuh), Bahasa Indonesia, IDR, WIB.
- 6 halaman resmi sesuai template.
- Dataset relational synthetic, 30 hari, target 3600 order, 9 tabel inti.
- Five required libraries + Plotly interactive core.
- Global filters tanggal/cabang/kategori, semantik grain benar.
- Food Gross Profit = Net Revenue - Food COGS; waste separate.
- All historical inventory movements to as-of cutoff.
- At least two qualitative, five quantitative, one geographic; at least four auto rules; two prototype iterations.
- **No cloning sample design**.

### Flexible (Codex boleh memilih sambil mendokumentasikan)

- Minor UI component spacing, exact navigation icon, responsive breakpoint.
- Exact 20–24 menu names, ingredient costs and BOM quantities if scenario validation demands (but update doc15 + config).
- Exact number chart beyond required family coverage, if meaningful.
- Data storage CSV/Parquet for marts if optional and tested; cleaned CSV mandatory for transparent evidence.
- Graphviz image vs Mermaid flowchart implementation method; result must be visible in app and exportable.
- Testing framework add-ons, CI platform, automated screenshot method.
- Workarounds for API changes, documented with ADR and links.

### Change control

Any frozen decision change requires a documented tradeoff and user's explicit approval, except breaking bug that makes solution impossible and can be fixed without changing user-visible product scope. For a necessary deviation, Codex records `deviation_id`, `old`, `new`, `reason`, `risk`, `tests_changed`, `docs_updated`, and asks before destructive change.

## 14.3 Quality vs scope choices

When under pressure, prioritize: **Correctness > completion of required modules > tests/evidence > clarity of UI > extra polish > experimental features**. Delete optional charts before dropping a required chart family. Do not fake data or pass status. A boring exact metric is better than a spectacular incorrect visualization.

## 14.4 Data realism parameters — not empirical claims

- Branch demand multipliers, channel shares, base prep minutes, unit costs, reorder points are parameters chosen to create a **plausible teaching scenario**.
- There is no “ground truth” actual restaurant behavior in this dataset, so findings belong to **synthetic scenario** only.
- More data volume does not automatically improve validity if all rows derive artificial rules; clearly disclose that limitation.

## 14.5 Decision escalation to user

Codex should normally proceed autonomously with this spec, but **stop and ask** before: removing one of six modules, substituting tool stack, creating real payment/account flows, switching brand, using sample Restora visual language, changing demographic or location assumptions, publishing repo to public, or using credentials/external integrations.

## 14.6 Future sequel — SeoulGrill AYCE (separate scope)

**Not part of ChickFlow.** It can reuse *generalized* patterns (typed metrics, filter context, data validation, test harness) but must have new brand, ERD and workflow: reservation, table sessions, package tier, time limit, refill, waste, revenue per seated group, constraints. Do not write any AYCE table/widget into ChickFlow as “future-proofing”.
