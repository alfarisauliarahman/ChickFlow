# 02 — Business understanding, problem formulation, stakeholder, PB register

## 2.1 Perspektif masalah yang harus dibuktikan setelah data jadi

Dokumen ini menyatakan **hipotesis** dan metode validasi. **Jangan masukkan angka temuan contoh sebagai fakta.** Setelah generator menghasilkan data, hitung nilai baseline dan isi evidence JSON/CSV. Sebaliknya, jangan sengaja mengatur data hingga semua target lolos; sedikit masalah bisnis memang diperlukan untuk analisis.

| Masalah | Hipotesis | Evidence minimal | Akibat potensial | Aksi yang masuk akal |
|---|---|---|---|---|
| P01 | Pesanan jam puncak lebih lama disiapkan | median dan P90 prep time per jam; sample size | antrean, tidak puas | evaluasi slot station/shift |
| P02 | Cabang tertentu memiliki delay lebih tinggi | late counts/eligible counts per cabang/channel | mutu layanan tak konsisten | audit workload cabang |
| P03 | Menu terlaris bisa bermargin rendah | unit sold, net sales, gross profit, margin | profit kurang optimal | evaluasi menu, BOM, harga |
| P04 | Stok kritis tidak seragam | ending stock vs reorder point per bahan-cabang | stockout | urutan restock berdasar coverage |
| P05 | Diskon berkorelasi dengan penurunan margin | discount %, menu-level profit | margin tertekan | telaah efektivitas paket |
| P06 | Hari dan jam punya campuran channel berbeda | channel × hour × weekday | salah jadwal personel | alokasi kapasitas |
| P07 | Rating pelanggan berkaitan dengan delay | rating dist by delay, N responden | retensi/kepuasan berpotensi menurun | review service experience |

**Pemisahan observasi vs rekomendasi:** bilang “Pada data sintetis, delayed rate meningkat di periode ...” bukan “cabang X perlu dipecat karyawannya”. Grafik korelasi tidak membuktikan kausalitas. Rating berasal dari data simulasi, sehingga kesimpulannya juga terbatas.

## 2.2 Stakeholder matrix

| Stakeholder | Tugas | Informasi kritis | Keputusan | Dashboard |
|---|---|---|---|---|
| Owner / finance | review kinerja | net sales, discount, COGS, food GP | menu/cabang prioritas | Overview, Sales, Profit |
| Operations manager | layanan harian | demand, delay, SLA, jam puncak | monitoring shift | Overview, Orders, Kitchen |
| Kitchen lead | pengendalian dapur | queue load, station, median/P90 | evaluasi bottleneck | Kitchen, Orders |
| Procurement | persediaan | saldo as-of, coverage, waste, reorder | restock item & cabang | Inventory |
| Akademik/evaluator | menilai proyek | pilihan chart, keterlacakan, test | validasi CPMK | semua + docs |

## 2.3 Personas

- **Persona-01 Maya, 30, manager operasional (fiktif):** laptop siang hari, fokus jam sibuk, butuh jawaban dalam ≤2 klik dari dashboard ke detail. Keputusan: memperiksa jam/cabang dengan delay tertinggi.
- **Persona-02 Arman, 42, owner (fiktif):** cek angka akhir hari, prioritas data exact dan biaya menu; tidak nyaman dengan grafik rumit tanpa penjelasan.
- **Persona-03 Sari, 27, inventory specialist (fiktif):** berangkat dari daftar bahan kritis, memerlukan unit dan tanggal saldo yang tidak ambigu.
- **Persona-04 Rina, 34, kitchen lead (fiktif):** butuh p90, distribution, station dan jumlah order; tidak menganggap rata-rata mewakili pesanan ekstrem.

## 2.4 Pertanyaan bisnis (15 PB, disimpan sebagai registry di kode/config)

| PB | Domain | Pertanyaan yang dijawab | Metrik primer | Visualisasi | Aksi potensial |
|---|---|---|---|---|---|
| PB-01 | Sales | Seperti apa tren pendapatan bersih per hari? | net revenue | V-Q01 line | periksa penurunan hari tertentu |
| PB-02 | Menu | Mana 10 menu terjual terbanyak? | units sold | V-Q02 bar | cek produk unggulan |
| PB-03 | Orders | Kapan order paling padat? | eligible order counts | V-Q03 heatmap | tinjau shift |
| PB-04 | Branch | Cabang mana dengan revenue terbesar? | net revenue/branch | V-Q04 bar | bandingkan volume |
| PB-05 | Kitchen | Bagaimana distribusi waktu persiapan? | prep minutes | V-Q05 histogram/KDE | evaluasi ekor distribusi |
| PB-06 | Kitchen | Mana cabang/channel paling banyak melampaui SLA? | delayed % | V-Q06 grouped bar | audit keterlambatan |
| PB-07 | Profit | Menu mana laris tapi low margin? | units, margin % | V-Q07 scatter | review recipe dan price |
| PB-08 | Stock | Bahan mana di bawah reorder point? | quantity on hand | V-Q08 grouped bar + table | restock |
| PB-09 | Channels | Bagaimana AOV tiap channel? | net revenue/order | V-Q09 bar | evaluasi mix transaksi |
| PB-10 | Branch | Bagaimana lokasi cabang dan kinerja spasialnya? | revenue/branch | V-G01 point map | orientasi antar kota |
| PB-11 | Kitchen | Bagaimana rentang/median waktu persiapan per cabang? | prep minutes | V-Q10 boxplot | review varians |
| PB-12 | Profit | Bagaimana kontribusi gross profit tiap kategori? | food GP | V-Q11 bar | prioritas menu |
| PB-13 | Stock | Bahan apa yang paling banyak terbuang? | waste qty/cost | V-Q12 bar | perbaiki batch planning |
| PB-14 | Feedback | Kata/tema apa muncul pada ulasan? | review tokens/themes | V-L01 word cloud | review kualitas layanan |
| PB-15 | Process | Bagaimana proses order→pembayaran→kitchen→siap→handoff? | event definitions | V-L02 flowchart | identifikasi titik ukur |

## 2.5 Pemetaan ke target, test dan bukti

Setiap PB memiliki: (1) data sumber, (2) definisi metric, (3) chart yang sesuai, (4) judul berbentuk pertanyaan atau temuan, (5) deskripsi pengukuran, (6) screenshot, (7) interpretasi dengan angka hasil generator, (8) aksi dan keterbatasan. Pemetaan disimpan dalam `docs/visualization_registry.md` versi repo atau tabel di README.

## 2.6 User stories & acceptance

| ID | Sebagai ..., saya ingin ... | Kriteria penerimaan |
|---|---|---|
| US-01 | manager, melihat 8 KPI agar tahu kondisi harian | angka sesuai filters; satuan jelas; delta hanya bila periode pembanding valid |
| US-02 | owner, memfilter cabang agar tahu kinerja lokal | semua KPI berbasis cabang berubah; title menunjukkan cabang |
| US-03 | manager, memfilter kategori agar tahu kontribusi menu | revenue terfilter item kategori; order count unik; status cakupan jelas |
| US-04 | kitchen lead, melihat p90 agar tahu worst typical waits | p90 dari eligible completed orders, bukan rata-rata p90 antar cabang |
| US-05 | owner, meninjau menu low-margin agar memperbaiki pricing | unit, net revenue, COGS, GP dan margin dapat direkonsiliasi |
| US-06 | procurement, melihat stok tanggal tertentu agar dapat melakukan restock | as-of stock dari movement lengkap sampai cutoff; tidak disaring awal date range |
| US-07 | manager, melihat alert agar dapat bertindak | rule id, threshold, nilai aktual, affected context, tindakan, severity |
| US-08 | mahasiswa, menjalankan seed generator agar dataset konsisten | CLI idempotent, snapshot hash and validation lulus |
| US-09 | penguji, memeriksa jenis chart yang dipakai | chart registry menyebut tipe data, perbandingan alternatif dan library |
| US-10 | penguji, melihat uji produk | ada test report, prototype feedback log, screenshot sebelum/sesudah |

## 2.7 Asumsi dan batasan bisnis

1. Tiga cabang berada di kota simulasi Sumatra Barat, koordinat hanya lokasi representatif pusat kota.
2. Data meniru operasional 10.00–22.00 Asia/Jakarta; tanggal analitik order mengikuti `ordered_at` WIB, termasuk jika pesanan siap setelah tengah malam.
3. Harga/biaya sintetik, tidak mewakili harga pasar aktual. Diskon dialokasikan ke baris menu; tidak ada pajak, ongkos kirim, jasa platform, biaya sewa, upah, atau depresiasi.
4. Profit yang disajikan adalah **food gross profit**, bukan net profit akuntansi.
5. SLA waktu preparasi adalah parameter aturan bisnis simulasi, bukan standar universal restoran.
6. Stok historis dihitung dari event ledger, bukan data realtime supplier.
7. Review sintetik bisa mempunyai bias yang dirancang untuk mendukung skenario belajar. Jangan mengklaim hubungan kausal nyata.
8. Pengujian usability kecil dilakukan sebagai dokumentasi proses prototype, tidak mewakili seluruh populasi pengguna.

## 2.8 Analytical decision stories

**Story A — delay malam:** pilih rentang 7 hari → identifikasi alert delayed rate → klik Kitchen → bedakan p50 vs p90 → pilih cabang dan channel → lihat histogram/boxplot dan jumlah sampel → rekomendasi audit kapasitas fryer malam, bukan keputusan permanen.

**Story B — menu tampak populer tapi rugi food-cost:** top-selling burger terlihat di Sales → buka Profit → lihat bar units sold dan scatter price-vs-margin → uraikan diskon dialokasikan dan biaya recipe → tampilkan item dengan GP positif/negatif → catat saran evaluasi BOM/promo.

**Story C — stok kritis:** kartu Critical Inventory → Inventory → as-of sesuai end-date → pilih cabang, lihat bahan dan ratio on hand/reorder → cek 7-day usage sebagai konteks, filter kategori hanya memengaruhi pemakaian atributif → prioritaskan restock.
