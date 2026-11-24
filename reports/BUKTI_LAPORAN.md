# Bukti visualisasi dan validasi ChickFlow

Gunakan bukti ini untuk mengisi Bab VI.3–VI.6, VII.2, dan VIII pada template dosen. Semua angka dan grafik pada halaman ini memakai **24–30 Oktober 2026 (WIB), semua cabang, semua kategori**, dengan seed **20261001**. Data merupakan simulasi. [Manifest 15 visual](evidence/figures-manifest.json) mencatat rute aplikasi, ukuran gambar, dan hash gambar serta data sumber.

## Visual dan jawaban pertanyaan bisnis

| Pertanyaan | Visual dan sumber data | Temuan simulasi dan tindak lanjut |
|---|---|---|
| PB-01. Bagaimana tren omzet harian? | [V-Q01 · Grafik garis](evidence/figures/V-Q01.png). Jumlah `order_items.line_net_idr` per tanggal pesanan valid. Garis mempertahankan urutan hari. | Omzet tertinggi Rp10.271.450 pada 24 Oktober, terendah Rp6.374.450 pada 27 Oktober, dan kembali ke Rp8.119.150 pada 30 Oktober. Omzet total turun 7,0% dibanding tujuh hari sebelumnya. Telusuri penurunan per cabang dan kanal. |
| PB-02. Menu apa yang paling banyak terjual? | [V-Q02 · Batang horizontal terurut](evidence/figures/V-Q02.png). Jumlah `order_items.quantity` per `menu_id`, dengan nama dari `menu`. Bentuk ini memudahkan perbandingan sepuluh SKU. | Spicy Crispy Chicken memimpin dengan 134 unit, disusul Iced Tea 129 dan Original Crispy Chicken 113. Daftar lengkap ada di grafik. Gunakan ranking untuk memperkirakan bahan dan kemasan yang paling dibutuhkan. |
| PB-03. Kapan pesanan paling padat? | [V-Q03 · Heatmap](evidence/figures/V-Q03.png). Pesanan unik selesai per hari dan jam WIB dari `orders.ordered_at`, dibagi jumlah hari pengamatan pada hari yang sama. | Sabtu pukul 12.00 WIB mencatat 33 pesanan, sel tertinggi pada periode ini. Ada satu Sabtu dalam sampel. Bandingkan beberapa pekan sebelum mengubah jadwal kerja. |
| PB-04. Cabang mana dengan omzet terbesar? | [V-Q04 · Batang omzet cabang](evidence/figures/V-Q04.png). Jumlah `line_net_idr` dari item pesanan valid, dikelompokkan menurut cabang dari `orders`. | Padang Rp20.555.400, Bukittinggi Rp16.995.650, dan Payakumbuh Rp14.259.050. Gunakan pesanan dan nilai per pesanan untuk menjelaskan selisihnya. |
| PB-05. Bagaimana sebaran waktu persiapan? | [V-Q05 · Histogram](evidence/figures/V-Q05.png). `orders.prep_time_min` untuk 813 pesanan valid, dengan interval dua menit. | Median 12,5 menit dan P90 25,5 menit. P90 lebih dari dua kali median, sehingga kasus persiapan lama perlu dilihat tersendiri. |
| PB-06. Kelompok mana yang paling sering terlambat? | [V-Q06 · Batang per cabang dan kanal](evidence/figures/V-Q06.png). Pembilang `delayed_flag` dan jumlah pesanan dengan durasi valid dari `orders`. Hover menampilkan pembilang dan penyebut. | Payakumbuh punya proporsi tertinggi untuk seluruh kanal, 49 dari 219 pesanan atau 22,4%. Dalam perbandingan cabang × kanal, Bawa pulang Payakumbuh tertinggi dengan 20 dari 67 pesanan atau 29,9%. Tinjau kapan pesanan bawa pulang menumpuk. |
| PB-07. Menu mana yang cukup laris tetapi marginnya rendah? | [V-Q07 · Scatter plot](evidence/figures/V-Q07.png). Setiap titik berisi unit terjual dan laba kotor dibagi omzet untuk satu menu. Garis putus-putus menandai batas margin 25%. | Family Feast Box terjual 58 unit dengan margin 10,7%, di bawah ambang 25%. Buka rincian resep dan diskon untuk menilai pilihan penyesuaian harga atau biaya. |
| PB-08. Bahan mana di bawah batas pesan ulang? | [V-Q08 · Batang rasio stok](evidence/figures/V-Q08.png). Saldo dihitung dari seluruh `inventory_movements` hingga akhir tanggal, lalu dibagi `branch_inventory_policy.reorder_point_qty`. Merah menandai rasio di bawah 100%. | Saus teriyaki Payakumbuh tersisa 48 ml dari batas 103 ml, atau 46,6%. Selisih terhadap batas adalah 55 ml. Cek riwayat stok dan jadwal penerimaan. |
| PB-09. Bagaimana rata-rata nilai pesanan tiap kanal? | [V-Q09 · Batang nilai pesanan](evidence/figures/V-Q09.png). Omzet item dibagi pesanan unik valid per `orders.channel`. | Bawa pulang Rp66.110 per pesanan dari 205 pesanan, makan di tempat Rp64.267 dari 305, dan pesan antar Rp61.571 dari 303. Bandingkan komposisi menu dan diskon tiap kanal sebelum menarik kesimpulan. |
| PB-10. Di mana cabang berada dan bagaimana omzetnya? | [V-G01 · Peta titik](evidence/figures/V-G01.png). Koordinat representatif dari `branches.latitude` dan `branches.longitude`. Luas titik mengikuti omzet. Garis provinsi dari geoBoundaries memuat atribusi pada aplikasi. | Padang menyumbang 39,7% omzet, Bukittinggi 32,8%, dan Payakumbuh 27,5%. Gunakan lokasi sebagai konteks perbandingan cabang. Ukuran titik menyatakan omzet pada periode simulasi. |
| PB-11. Bagaimana durasi persiapan berbeda antarcabang? | [V-Q10 · Box plot](evidence/figures/V-Q10.png). `prep_time_min` pada pesanan valid dikelompokkan per cabang. Bentuk ini memperlihatkan median, kuartil, dan pencilan. | Median Payakumbuh 13,48 menit, Bukittinggi 12,50, dan Padang 11,60. Durasi terpanjang Payakumbuh 61,40 menit. Periksa pesanan berdurasi ekstrem pada jam dan kanal terkait. |
| PB-12. Kategori mana yang paling banyak menyumbang laba kotor? | [V-Q11 · Batang kontribusi kategori](evidence/figures/V-Q11.png). Jumlah `line_food_gp_idr` per kategori menu, dari item yang selesai dan dibayar. | Rice Meal menyumbang Rp7.402.796, terbesar pada periode ini. Fried Chicken menyusul dengan Rp6.206.582. Gunakan kontribusi bersama volume dan margin saat mengevaluasi paket menu. |
| PB-13. Bahan apa yang menyumbang biaya pemborosan terbesar? | [V-Q12 · Batang biaya bahan terbuang](evidence/figures/V-Q12.png). Jumlah `movement_cost_idr` untuk mutasi `WASTE` pada periode ini, per bahan. | Daging paha ayam menyumbang Rp199.920 dari total Rp474.763. Tinjau takaran, ukuran batch, dan waktu persiapan bahan ini terlebih dahulu. |
| PB-14. Kata apa yang sering muncul dalam ulasan? | [V-L01 · Awan kata dan tabel](evidence/figures/V-L01.png). Token huruf dari `feedback.review_text`, setelah stopword bahasa Indonesia dikeluarkan. | Dari 158 ulasan berteks, “mudah”, “dibawa”, “pulang”, dan “ayam” masing-masing muncul 40 kali. Frekuensi menunjukkan topik yang muncul. Baca ulasan utuh untuk memahami konteks dan sentimen. |
| PB-15. Bagaimana alur pesanan dan titik ukur waktu? | [V-L02 · Diagram alur](evidence/figures/V-L02.png). Status `orders.order_status`, waktu `ordered_at` dan `ready_at`, serta mutasi stok resep. | Pesanan masuk dapat batal sebelum produksi. Pesanan yang diteruskan melewati pembayaran dan dapur sampai siap dan diserahkan. Waktu persiapan dihitung dari pesanan masuk sampai siap. Cakupan mencatat 813 selesai dan 20 batal. |

Bukti pemakaian Matplotlib dan Seaborn ada pada [grafik omzet](eda/V-Q01_net_sales.png), [ranking menu](eda/V-Q02_menu_units.png), [histogram persiapan](eda/V-Q05_prep_distribution.png), dan [box plot cabang](eda/V-Q10_prep_branch.png). [Enam temuan awal](eda/baseline.csv) untuk Bab I memakai cakupan **1–30 Oktober**, sehingga periodenya perlu ditulis terpisah dari tabel visual di atas.

Kode filter global ada di [app/main.py](../app/main.py). [metrics.py](../src/chickflow/metrics.py) memisahkan transaksi unik, item penjualan, dan saldo stok. [charts.py](../src/chickflow/charts.py) membentuk grafik Plotly. [views.py](../app/views.py) menghubungkan visual, filter, dan alur detail. [insights.py](../src/chickflow/insights.py) memuat peringatan otomatis berbasis ambang.

## Validasi KPI untuk Bab VII.2

Perhitungan ulang membaca CSV bersih secara langsung. Omzet dihitung dari takaran dan harga item dikurangi diskon alokasi. Laba memakai biaya per unit. Durasi dihitung ulang dari waktu pesanan masuk dan siap. Saldo stok dijumlahkan hingga akhir tanggal WIB.

| KPI | Perhitungan ulang · periode default | Logika dashboard | Selisih |
|---|---:|---:|---:|
| K01 Omzet bersih | Rp51.810.100 | Rp51.810.100 | Rp0 |
| K02 Pesanan selesai | 813 | 813 | 0 |
| K03 Rata-rata nilai pesanan | Rp63.727,06 | Rp63.727,06 | 0 |
| K04 Rata-rata waktu persiapan | 14,64286593 menit | 14,64286593 menit | ±0,00000000012 menit |
| K05 Pesanan terlambat | 18,45% | 18,45% | 0 poin persentase |
| K06 Margin kotor makanan | 54,87% | 54,87% | 0 poin persentase |
| K07 Bahan kritis per cabang | 1 pasangan bahan–cabang | 1 pasangan bahan–cabang | 0 |
| K08 Laba kotor makanan | Rp28.429.304 | Rp28.429.304 | Rp0 |

**24 dari 24 pemeriksaan lulus**, pada periode default, filter Padang + kategori Beverage, serta satu hari pada 30 Oktober. Selisih durasi berada dalam toleransi 0,00000001 menit untuk angka desimal. [Data perbandingan, selisih, dan toleransi](evidence/kpi-checks.json) · [Skrip hitung ulang](../src/chickflow/reports/verify_kpis.py)

## Bukti tahap prototipe

[File FigCraft dengan wireframe dan mockup](design/ChickFlow-Prototype.figcraft) mendukung Bab V. [Manifest tangkapan enam halaman Streamlit](screenshots/manifest.json) mendukung Bab VI.6 dan pengujian fungsi di Bab VII. [Walkthrough AI lima skenario](prototype/walkthrough-ai.md) mendokumentasikan evaluasi teknis FigCraft dan Streamlit dengan 0 responden manusia. Naskah, lembar waktu pengerjaan, dan log perbaikan ada di [panduan sesi pengguna](prototype/README.md). Dua putaran uji pengguna menunggu responden.

[Bukti revisi antarmuka](prototype/revision/README.md) memuat pasangan screenshot dan hasil uji ulang untuk Bab VII.3, VII.4, dan Lampiran F. Perubahan berasal dari temuan walkthrough AI.
