# CHICKFLOW — MASTER IMPLEMENTATION BLUEPRINT (v2.3)

> **STATUS:** Rencana implementasi, **belum** ada dashboard atau dataset final yang dibangun.  
> **Tanggal perencanaan:** 24 November 2026 (WIB).  
> **Project:** ChickFlow — Fast Food Analytics & Operations Dashboard.  
> **Audiens:** pemilik proyek, Codex / coding agent, penguji, pembimbing akademik.  
> **Bahasa aplikasi:** Bahasa Indonesia (label UI), istilah teknis boleh bilingual. Mata uang IDR; zona waktu Asia/Jakarta.  
> **Prinsip utama:** *Correct data → correct decisions → clear visualization → attractive UI*. Bukan meniru Restora atau contoh dashboard apa pun.

## Cara menggunakan paket ini

1. Mulai dari **`codex/START_HERE.md`**, lalu ikuti tiga milestone pada roadmap.
2. `docs/01`–`docs/15` adalah *source of truth* untuk fitur, data, metrik, interaksi, desain, kualitas, dan dokumentasi.
3. `checklists/REQUIREMENT_TRACEABILITY.md` memetakan setiap syarat template ke implementasi dan bukti.
4. `checklists/DELIVERY_GATES.md` mendefinisikan *pass/fail* proyek. Fitur tidak selesai hanya karena halaman berhasil dirender.
5. `codex/PHASE_PROMPTS.md` berisi prompt berurutan untuk menghindari Codex membangun 6 halaman palsu sekaligus.
6. `codex/AGENTS.md` dapat **disalin ke root repository implementasi sebagai `AGENTS.md`** agar aturan pengembangan selalu dibaca coding agent.
7. Dokumen `CHICKFLOW_ALL_IN_ONE.md` (di tingkat paket hasil) menggabungkan spesifikasi agar bisa langsung diunggah ke Codex bila hanya ingin satu file.

## Prioritas sumber (jika berbeda)

1. **Template Laporan Proyek Akhir Visualisasi Data** yang disediakan pengguna: ketentuan wajib individu + rubrik + bukti.
2. **Keputusan produk ChickFlow dalam paket ini:** konsep, data, UX, rumus, modul, testing; merupakan keputusan proyek, bukan contoh.
3. **RPS Visualisasi Data 2025:** tujuan pembelajaran dan materi; RPS menuliskan `DIF62132`/`CPMK32` sedangkan template proyek menuliskan `DIF61143`/`CPMK43`. **Jangan menebak mana yang berlaku secara administratif**; konfirmasi dosen jika diperlukan. Ketentuan tugas spesifik mengikuti template.
4. **ZIP materi kelas (Restora, layout example, latihan, buku):** bacaan pembelajaran saja. **DILARANG** menyalin layout, urutan halaman, brand, logo, warna, atau data contoh menjadi ChickFlow. Sampel **tidak mengubah** keputusan utama.
5. Dokumentasi resmi pustaka untuk memastikan API yang digunakan valid pada versi yang dipasang.

## Batasan

- ChickFlow adalah **brand dan operasi restoran fiktif** yang dibuat untuk tugas individu.
- Data adalah **sintetis** dan dihitung dengan generator teruji. Jangan klaim sebagai penjualan, konsumen, alamat, atau evaluasi restoran nyata.
- Peran manajemen dan staf ialah **persona pengguna**, bukan login/role-based access control riil.
- Dashboard ini **analitik historis**, bukan POS/e-commerce/ERP produksi dan bukan sistem mengelola uang sungguhan.
- Fokus **enam modul** yang terkunci: `Overview`, `Orders`, `Kitchen Performance`, `Inventory`, `Sales & Reports`, `Food Cost & Profit`. Tidak diam-diam menggantinya dengan fitur contoh.
- **Dashboard dahulu; laporan final belakangan.** Bukti, screenshot, data cleaning log, matriks pengujian, dan perubahan prototype dicatat sepanjang pengembangan.

## Kontrak target

| Target | Ketentuan | Rencana ChickFlow |
|---|---|---|
| Modul | minimal 6 | tepat 6 modul wajib, opsional ditempatkan sebagai bagian modul |
| Data | ≥500 baris transaksi, ≥7 hari, ≥3 tabel berelasi | 3.600 order / 30 hari / 9 tabel inti, semua terhubung |
| Visualisasi | ≥2 kualitatif, ≥5 kuantitatif, ≥1 geografis | 2 / 10+ / 1; ada pemetaan pertanyaan bisnis |
| Dashboard | Plotly interaktif, ≥3 filter, ≥6 KPI | tanggal, cabang, kategori; target 8 KPI global + 4 KPI kontekstual |
| Insight otomatis | ≥4 aturan | target 6 aturan *rule-based*, transparan dan dapat diuji |
| Library wajib | pandas, numpy, matplotlib, seaborn, plotly | dipakai dan dibuktikan lewat file dan hasil visualisasi |
| UX/RPL | prinsip good UI, proses prototype | 2 iterasi, 4 prinsip, wireframe + screenshot + hasil uji |
| Tugas akhir | repo, laporan PDF, video, presentasi | pipeline dokumentasi dan handoff dipersiapkan, **tidak mengaku selesai** |

## Tahap pengerjaan

**00 Definition → 01 Foundation → 02 Data → 03 Business Metrics → 04 Visualizations → 05 Shell & UI → 06 Six Pages → 07 QA & Revisions → 08 Delivery & Report Evidence.**

**Aturan anti-*scope creep*:** jangan mengembangkan SeoulGrill AYCE, AI forecasting, login, pembayaran, notifikasi eksternal, atau database produksi ke ChickFlow v1. SeoulGrill adalah proyek terpisah di masa depan.

## Index lengkap

- [01 — Product requirements dan scope](docs/01_PRODUCT_REQUIREMENTS.md)
- [02 — Business analysis, personas, questions](docs/02_BUSINESS_AND_REQUIREMENTS.md)
- [03 — Dataset, skema relasional, kamus data](docs/03_DATA_CONTRACTS.md)
- [04 — Generator sintetis dan data preparation](docs/04_SYNTHETIC_DATA_PIPELINE.md)
- [05 — Definisi KPI, profit, SLA, stok, aturan insight](docs/05_METRICS_AND_BUSINESS_RULES.md)
- [06 — Spesifikasi 6 modul dan user flow](docs/06_SIX_PAGE_SPECS.md)
- [07 — Pemilihan visualisasi dan katalog grafik](docs/07_VISUALIZATIONS.md)
- [08 — UI/UX, design system, wireframe](docs/08_DESIGN_SYSTEM.md)
- [09 — Engineering, APIs, struktur repo](docs/09_ARCHITECTURE.md)
- [10 — Interaktivitas, filter semantics, state](docs/10_FILTERS_AND_INTERACTION.md)
- [11 — Testing: unit/integrasi/E2E/performance](docs/11_TEST_STRATEGY.md)
- [12 — Sprint backlog, prioritas, milestone](docs/12_IMPLEMENTATION_ROADMAP.md)
- [13 — Dokumentasi, demo, laporan, RPS alignment](docs/13_REPORT_EVIDENCE.md)
- [14 — Risiko, keputusan, alternatif, tradeoffs](docs/14_RISKS_AND_DECISIONS.md)
- [15 — Katalog konkret menu, bahan, dan BOM](docs/15_MENU_AND_SEED_CATALOG.md)
- [Matriks ketentuan → bukti](checklists/REQUIREMENT_TRACEABILITY.md)
- [Quality / delivery gates](checklists/DELIVERY_GATES.md)
- [Instrumen uji pengguna (kosong, tidak dibuat-buat)](checklists/PROTOTYPE_FEEDBACK_INSTRUMENT.md)
- [Template status implementasi](checklists/PROJECT_STATUS_TEMPLATE.md)
- [Template penggunaan AI](checklists/AI_USE_LOG_TEMPLATE.md)
- [Audit handoff final](checklists/FINAL_HANDOFF_AUDIT.md)
- [Validasi katalog 24 SKU dan biaya BOM](checklists/SEED_CATALOG_SANITY.md)
- [Codex entry point](codex/START_HERE.md)
- [Codex prompts per fase](codex/PHASE_PROMPTS.md)
- [AGENTS untuk Codex](codex/AGENTS.md)

## Definition of done proyek

**Tidak cukup:** aplikasi bisa `streamlit run`; navbar menunjukkan 6 judul; angka KPI muncul; grafik cantik.  
**Harus:** dataset reproducible, rekonsiliasi nominal **tepat**, tidak ada *double counting*, enam modul punya alur kerja yang relevan, filter tidak melanggar grain, ≥8 chart wajib dan peta benar, semua alert tertelusur ke angka, unit test & integration test lulus, bukti visualisasi kelima library, dua putaran prototype terarsipkan, demo bisa diulang dari README.
