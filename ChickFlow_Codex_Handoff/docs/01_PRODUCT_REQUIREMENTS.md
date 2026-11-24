# 01 — Product charter, arah produk, ruang lingkup

## 1.1 Visi produk

**ChickFlow Operations Intelligence** adalah dashboard analitik restoran ayam cepat saji berbasis data sintetis, digunakan pengelola restoran untuk memantau penjualan, permintaan, waktu persiapan makanan, kesehatan persediaan, dan margin kontribusi makanan di tiga cabang simulasi. Fokus interaksi: **temukan perubahan → telusuri penyebab → pahami dampak → tentukan tindakan**.

### Apa yang dibangun

- **Satu aplikasi** Streamlit multi-page dengan Plotly untuk visualisasi interaktif dan filter global.
- **Satu pipeline data** deterministik untuk menghasilkan tabel operasi raw → clean/validated → analytical marts.
- **Satu pusat definisi metrik** mencegah hasil KPI berbeda antar halaman.
- **Satu mesin insight otomatis** berbasis aturan yang menyebut angka, konteks, dan tindakan, tanpa klaim AI/ML.
- **Satu paket QA & evidence**: pengujian, diagram, hasil EDA statis, screenshot, catatan perbaikan, dan panduan.

### Apa yang bukan produk ini

Bukan POS untuk kasir, bukan inventaris riil dengan pemesanan supplier, bukan peramalan ML, bukan sistem karyawan/gaji, bukan reservasi AYCE, bukan dashboard live production. Transaksi hanya dapat ditelusuri, bukan diedit demi demo.

## 1.2 Identitas ChickFlow yang dibekukan untuk v1

| Field | Nilai rancangan |
|---|---|
| Brand | **ChickFlow** |
| Tagline | **Fast Service. Smart Decisions.** |
| Jenis usaha | Fast-casual / quick service restaurant (QSR) ayam goreng |
| Produk | Fried chicken, burgers, rice bowls, wings, sides, drinks, combos |
| Segmen | Pelajar/mahasiswa, pekerja, keluarga kecil, delivery |
| Cabang simulasi | ChickFlow Padang, ChickFlow Bukittinggi, ChickFlow Payakumbuh (3 kota di Sumatra Barat, **bukan alamat komersial nyata**) |
| Channel | DINE_IN, TAKEAWAY, DELIVERY |
| Bahasa dan format | Bahasa Indonesia, IDR, WIB, tanggal `dd MMM yyyy` |
| Periode data awal | 1–30 Oktober 2026 (30 hari, 3.600 order total sebagai target generator) |
| Mode produk | Read-only historical analytics; synthetic demo banner |
| Pengguna primer | Manager restoran, Kitchen Lead, Inventory Officer, Owner/Finance |
| Layar primer | Laptop 1366×768 hingga desktop 1920×1080; tablet sebagai fallback |

**Merek/gaya:** tidak meniru Restora. Namanya mewakili aliran pesanan dan kinerja dapur; gunakan ikon visual yang orisinal atau sederhana, tanpa foto bermerek dari luar. Logo boleh berbentuk ikon garis sayap/ayam + aliran panah, dan menjadi artefak wajib Bab V serta sampul.

## 1.3 Tujuan bisnis (target simulasi, bukan fakta)

| Kode | Tujuan | KPI | Target evaluasi | Frekuensi |
|---|---|---|---|---|
| G01 | Monitoring pemasukan bersih | Net Revenue | cocok 100% dengan perhitungan transaksi | harian |
| G02 | Memahami beban dapur | Completed order count/h | jam sibuk teridentifikasi | per jam |
| G03 | Pelayanan tepat waktu | Delayed Orders % | baseline simulasi dibandingkan target bisnis **≤10%** | harian/mingguan |
| G04 | Memantau durasi persiapan | Median prep / P90 prep | disajikan per cabang dan channel | harian |
| G05 | Mempertahankan margin | Food gross margin % | target bisnis **≥30%** sebagai parameter; realisasi dihitung | mingguan |
| G06 | Mengidentifikasi menu bermargin lemah | Menu margin % | margin **<25%** memicu A02 jika minimal 10 unit terjual dan omzet positif | mingguan |
| G07 | Mengendalikan stok | Critical ingredient count | stok per bahan-cabang yang melewati ambang terdeteksi | per tanggal |
| G08 | Memahami perbedaan cabang | Revenue, AOV, delay, margin | ranking multimetric, tidak mengklaim sebab-akibat | mingguan |
| G09 | Menopang keputusan operasional | Insight panel | ≥4 aturan terbukti memicu sesuai fixture | per filter |

## 1.4 Functional requirements (FR)

| ID | Syarat perilaku | Prioritas | Verifikasi |
|---|---|---|---|
| FR-01 | Navigasi keenam modul terdaftar | MUST | AppTest/smoke UI |
| FR-02 | Tampilkan ≥6 KPI global dengan definisi | MUST | test metrics + visual inspect |
| FR-03 | Filter tanggal, cabang, kategori berlaku konsisten | MUST | matriks kombinasi filter |
| FR-04 | Semua grafik interaktif utama dibuat dengan Plotly | MUST | render + hover + dropdown |
| FR-05 | Pilihan grafik sesuai tipe data dan pertanyaan bisnis | MUST | traceability V ↔ PB |
| FR-06 | Peta geografis cabang memakai koordinat simulasi | MUST | validasi geodata + peta |
| FR-07 | ≥2 visualisasi kualitatif | MUST | word cloud + workflow diagram |
| FR-08 | ≥5 kuantitatif, mencakup 5 keluarga grafik utama | MUST | visual audit |
| FR-09 | ≥4 rules insight otomatis berbasis threshold | MUST | unit test per rule |
| FR-10 | Orders detail memuat pencarian dan pengecekan penyebab delay | MUST | scenario orders |
| FR-11 | Kitchen membandingkan prep time, SLA, jam ramai, cabang | MUST | scenario kitchen |
| FR-12 | Inventory saldo as-of dan bahan kritis per cabang | MUST | audit ledger |
| FR-13 | Profit mengalokasikan diskon dan menghitung COGS dari BOM | MUST | recon test |
| FR-14 | Grafik saling memperkuat tetapi tidak saling menghitung ganda | MUST | aggregation tests |
| FR-15 | Data loading mendukung empty/error states dan metadata freshness | MUST | simulated failures |
| FR-16 | Ringkasan ekspor CSV data yang difilter | SHOULD | download test |
| FR-17 | Penjelasan rumus KPI/tooltip dan link evidence | SHOULD | UAT |
| FR-18 | Perbandingan periode sebelumnya jika lengkap | SHOULD | comparison test |
| FR-19 | Filter chart-to-chart melalui klik Plotly | COULD | optional UI E2E |
| FR-20 | Light/dark theme toggle | COULD | a11y + snapshot |

## 1.5 Nonfunctional requirements (NFR)

| ID | Aspek | Target & metode |
|---|---|---|
| NFR-01 | Akurasi | Sum detail = sum header pada semua order; selisih nominal **Rp0** |
| NFR-02 | Reproducibility | dua kali generate dengan seed/config identik → hash tabel clean identik |
| NFR-03 | Kinerja | p95 pergantian filter target <3 detik pada laptop penguji; ukur, jangan klaim sebelum ada hasil |
| NFR-04 | Reliability | tidak crash untuk filter kosong, satu cabang, satu kategori, satu tanggal |
| NFR-05 | UX | mayoritas 5 responden menemukan tindakan utama dalam uji 3 detik (target penelitian kecil, bukan statistik representatif) |
| NFR-06 | Accessibility | kontras teks standar minimal 4.5:1, keyboard navigation, label jelas, tidak mengandalkan warna saja |
| NFR-07 | Portability | Windows/macOS/Linux Python 3.11/3.12 yang didukung dependensi; uji browser Chromium dan Firefox jika tersedia |
| NFR-08 | Maintainability | fungsi metrik murni, satu definisi schema, import tanpa efek side effect, type hints dan docstring |
| NFR-09 | Observability | status data/seed/periode/cabang terlihat; log data issue tanpa personal information |
| NFR-10 | Privacy/safety | tak ada PII asli, API key, kredensial, atau alamat outlet fiktif yang dipresentasikan sebagai nyata |
| NFR-11 | Data lineage | tabel sumber, aturan transform, grain, dan kolom KPI dapat dirunut |

## 1.6 Prioritas MoSCoW dan kontrol scope

- **MUST:** 6 modul, 9 tabel, generator, 8+ visualisasi wajib, 3 filter, 6 KPI, 4 alert, 5 library, dua putaran uji pengguna, proof-of-test, panduan.
- **SHOULD:** 8 KPI di overview, 15 pertanyaan bisnis terjawab, 6 alert, eksport CSV, tooltip penjelasan, responsif.
- **COULD:** chart crossfilter, scenario simulator, advanced staffing estimate, animated transitions, theme toggle, menu-detail deep dive.
- **WON'T:** login, checkout, penjualan riil, video AI, transaksi yang dapat diedit, alert WhatsApp, ML forecasting, SeoulGrill AYCE.

## 1.7 Keberhasilan pengguna (job stories)

- **Manajer:** Ketika keterlambatan naik, saya ingin melihat cabang + jam + channel penyumbang sehingga dapat memprioritaskan pemeriksaan kapasitas shift.
- **Chef:** Ketika waktu persiapan memanjang, saya ingin melihat distribusi waktu dan station terkait sehingga tidak hanya mengandalkan rata-rata.
- **Pengadaan:** Ketika bahan kritis, saya ingin tahu stok as-of, reorder point, unit, dan konsumsi historis sehingga bisa menyusun urutan pembelian.
- **Owner:** Ketika revenue tinggi tetapi profit lemah, saya ingin membandingkan menu, discount, food cost, dan margin sehingga tahu menu yang perlu evaluasi.

## 1.8 Acceptance utama produk

1. Tidak ada satu pun angka yang ditulis manual untuk menyamar menjadi metrik live aplikasi.
2. Mengubah filter menyebabkan KPI/grafik/insight yang relevan berubah, atau menampilkan penjelasan eksplisit bila filter tidak berlaku.
3. Revenue total dari halaman Overview, Orders, Sales, Profit setara pada konteks filter yang sama ketika definisi grain setara.
4. Peta menampilkan cabang fiktif berlabel lokasi simulasi, tidak mengklaim outlet nyata.
5. Ada bukti **matplotlib dan seaborn** melalui EDA/report bukan hanya deklarasi package.
6. Tidak ada klaim bahwa data sintetik membuktikan kondisi bisnis di dunia nyata.
