# 13 — Evidence-first academic report plan, RPS crosswalk, demo and deliverables

**Laporan final dikerjakan setelah dashboard terbukti bekerja, tetapi bukti dikumpulkan sejak fase pertama.** Dokumen ini bukan laporan akhir; semua contoh interpretasi harus diganti hasil penghitungan nyata pada data sintetis.

## 13.1 Source priority dan administrasi

- **Template tugas akhir** yang diberikan pengguna menjadi sumber spesifikasi minimum proyek individu. Template menuliskan mata kuliah DIF61143, semester 5, CPMK43 dan bobot UAS 30%.
- **RPS tahun 2025** yang baru diunggah menuliskan Visualisasi Data `DIF62132`, semester IV, CPMK32, bobot UAS 30%. Ini **tidak identik secara administratif**. Jangan memutuskan secara sepihak nomor mata kuliah definitif; bila final report/cover membutuhkannya, cek arahan pengampu.
- Kesesuaian akademik substantif: penguasaan konsep/pemilihan grafik; kemampuan membuat visualisasi kualitatif, kuantitatif, geografis; analisis/implementasi dashboard interaktif.
- Materi ZIP Restora dan gambar layout **hanya sebagai contoh belajar**, tidak mengatur desain, data, dan fitur ChickFlow.

## 13.2 Bukti yang dikumpulkan untuk setiap Bab (sebelum menyusun naskah)

| Bab template | Evidence yang harus dihasilkan selama implementasi | Phase |
|---|---|---|
| Sampul/abstrak | brand/logo, deskripsi solusi, **angka hasil actual** di akhir | P8 |
| I. Business Understanding | brand, 5+ masalah berbukti angka hasil generator, 10+ PB, KPI formula/target, rules | P1–P3 |
| II. RPL Methodology | Prototype process, tahapan v1–feedback–v2, tools Git, issue log | P0–P7 |
| III. Requirements | 2+ personas, FR, NFR, user stories, use case dan order workflow | P0–P5 |
| IV. Data understanding/preparation | generator seed, data dictionary, ERD, raw-vs-clean diff, info/describe, cleaning code, derived metrics | P1–P3 |
| V. Design + chart choices | sitemap, wireframe low-fi dan mockup hi-fi untuk enam halaman, token colors, 4 UI principles, PB→V rationale | P4–P7 |
| VI. Implementation | tools versions/reasons/alternatives, folders, 2 qual + 5 quant + 1 geo actual, 6 dashboard screenshots, deployment instructions | P4–P8 |
| VII. Testing & Evaluation | functional tests actual result, KPI manual recon, 4 UI tests, 2 feedback cycles, measured load times | P6–P7 |
| VIII. Interpretation & recommendation | answer PB with actual values, visuals code, specific action, expected impact **not claimed achieved** | P8 |
| IX. Conclusion & suggestion | compare goals/criteria against real test outcome, limitations, future scope | P8 |
| References | ≥8 trustworthy references, library docs versioned, consistent style APA/IEEE | P8 |
| Appendices | dataset, repo, design assets, AI usage log, tests, prototype log, 3–5 min demo URL | P8 |

## 13.3 RPS topic alignment (substansi)

| Topik RPS | Bukti ChickFlow |
|---|---|
| Konsep/jenis/tujuan visualisasi | chart registry, visualization rationale |
| Pengumpulan & pembersihan data | raw/clean pipeline, injection logs, validation report |
| Kualitatif | word cloud teks ulasan sintetis hasil generator + process flowchart |
| Kuantitatif | histogram, scatter, bar, line, boxplot, heatmap |
| Geografis | Plotly MapLibre point map cabang fiktif |
| Python pandas / Matplotlib / Seaborn | EDA code + static PNG |
| Plotly | all six modules interactive charts |
| Dashboard interaktif | three global filters and insight rules |

## 13.4 Continuous evidence capture convention

Untuk setiap screenshot simpan `reports/screenshots/{page}_{version}_{viewport}_{date}.png` dan file pendamping `reports/screenshots/manifest.csv` (filename, page, dataset seed/hash, filters, browser size, captured by, note). Jangan membuat screenshot dummy lalu menulis “hasil implementasi”. Screenshot v1 dan v2 sengaja dipisahkan.

Untuk setiap test run simpan `reports/test_results/phase##_pytest.txt` atau JSON junit report jika tersedia, timestamp/commit short hash, environment, pass/fail/skip; jangan mengklaim 100% pass bila ada skip.

Untuk setiap keputusan: `docs/adr/ADR-###.md` atau satu `docs/decision_log.md`, berisi tanggal, alternatif, alasan, risiko. Ini memudahkan isi Bab II/V/VI.

Untuk setiap cleaning rule: raw issue count before/after, action, justification, code path, sample example ID anonymized. Jangan memasukkan screenshot `.info()` sebagai satu-satunya bukti tanpa penjelasan.

## 13.5 Template-specific quantity/quality gates

- **Modul:** 6 dari opsi yang ditentukan, dipenuhi dengan Overview, Orders, Kitchen, Inventory, Sales/Reports, Food Cost & Profit.
- **Data:** synthetic, ≥500 order rows, ≥7 days, ≥3 related tables, target 9.
- **Charts:** ≥2 qualitative, ≥5 quantitative, ≥1 geo; target 2+12+1.
- **Interactive:** Plotly + date/branch/category filters + ≥6 KPI + ≥4 rules.
- **Required packages:** pandas, numpy, matplotlib, seaborn, plotly (all actual evidence).
- **Business problems:** at least 5 operational problems backed by numeric evidence.
- **Business questions:** ≥10 PB and mapped to visualizations (15 planned).
- **Non-functional UI:** visual hierarchy, consistency, user feedback, accessibility with evidence.
- **Prototyping:** at least two feedback iterations intended, record actual data.
- **References:** at least eight sources/documentations consistently cited.
- **Deliverables:** PDF report, GitHub repo, runnable dashboard, 3–5 minute demo, presentation deck, originality and AI-use declaration.

## 13.6 Report honesty checklist

- Dataset disebut “sintetis” pada abstrak, metode, limitation, dan demo.
- Setiap grafik memiliki judul, figure no, sumber, interpretation, PB mapping.
- Angka penjualan, margin, delta, dan overdue di report berasal dari output seed + version yang sama, bukan contoh di blueprint.
- Uji usability dicatat responden nyata/yang benar-benar melakukan uji; jangan menghasilkan “5 responden” hanya sebagai placeholder hasil.
- Jangan klaim kenaikan revenue/penurunan delay **akibat dashboard** tanpa studi intervention; hanya kemampuan monitoring dan identifikasi risiko yang bisa diuji pada dataset.
- AI usage harus dicatat alat, tujuan, kode/analisis yang dibantu, cara pemeriksaan manual; jangan menuliskan seluruh proyek “murni tanpa AI” jika pakai Codex.
- Jangan menyalin branding atau visual Restora dalam lampiran ChickFlow.

## 13.7 Demo 3–5 menit storyboard (future evidence)

**0:00–0:25** — Jelaskan ChickFlow fiktif, tujuan, data/seed/30 hari.  
**0:25–0:55** — Overview: KPI, filters, top warning dengan n/N.  
**0:55–1:35** — Orders & Kitchen: jam ramai, distribusi prep, delayed vs SLA.  
**1:35–2:15** — Inventory: as-of date, bahan kritis, stock movement; tunjukkan filter category N/A secara benar.  
**2:15–2:55** — Sales & Profit: menu top, map, SKU margin & BOM.  
**2:55–3:25** — Tunjukkan word cloud + process flow sebagai kualitatif.  
**3:25–4:05** — Test & reproducibility: one reconciliation fixture, test report, screenshots v1/v2.  
**4:05–4:30** — Interpretasi 2 temuan berbasis angka aktual + limitation.

**Catatan:** urutan ini untuk **demo setelah implementasi**, bukan bukti bahwa fitur sudah ada. Sesuaikan durasi aktual 3–5 menit, jangan menyebut screenshot yang belum dibuat.

## 13.8 Rekomendasi referensi akademik/dokumentasi (belum daftar pustaka final)

1. Pandas official documentation — `https://pandas.pydata.org/docs/`.
2. NumPy docs — `https://numpy.org/doc/`.
3. Matplotlib docs — `https://matplotlib.org/stable/`.
4. Seaborn docs — `https://seaborn.pydata.org/`.
5. Plotly docs — `https://plotly.com/python/`.
6. Streamlit docs — `https://docs.streamlit.io/`.
7. McKinney, *Python for Data Analysis* (edisi dirujuk yang benar-benar dipakai).
8. Claus O. Wilke, *Fundamentals of Data Visualization* (jika buku ZIP dibaca, cek edisi & lisensi, kutip ide bukan salin materi).
9. Andy Kirk / Stephen Few / Edward Tufte sesuai akses sumber sebenarnya, dan cukup dengan sumber yang benar-benar diperiksa.
10. Nielsen Norman Group / W3C WCAG untuk prinsip UX/a11y — cek halaman resmi saat menulis report.

Gunakan format IEEE atau APA **konsisten** dan hanya mengutip sumber yang benar-benar dibaca. URL dokumentasi mencerminkan sumber teknis, bukan otomatis sumber semua klaim desain.
