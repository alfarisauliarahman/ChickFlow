# Status ChickFlow

## Data

Seed 20261001 menghasilkan 3.600 pesanan untuk 1–30 Oktober 2026. Sebanyak 3.511 pesanan selesai dan dibayar, dan 89 dibatalkan. Sembilan tabel bersih dan 81 pasangan cabang–bahan tercatat di manifest. Selisih rekonsiliasi gross, diskon, dan net adalah Rp0. Saldo terendah sepanjang ledger adalah 0.

`uv run --locked pytest -q` menjalankan 21 tes. Cakupannya antara lain pengulangan seed, pemeriksaan hash, pesanan campuran kategori, cutoff tengah malam, alert stok dengan penjualan kosong, batas SLA, serta warna status pada grafik stok. Hasil tersedia di [data_quality.json](data_quality.json) dan [log pytest](pytest.txt). Empat grafik statis dan enam temuan ada di [EDA](eda/baseline.csv).

## Implementasi dan verifikasi

Enam modul Streamlit menerapkan desain FigCraft yang disetujui, termasuk navigasi atas, foto, palet, filter global, dan label bahasa Indonesia. Browser memeriksa enam halaman, delapan KPI, filter yang bertahan saat berpindah halaman, reset, pencarian, ekspor CSV, diagram alur dan word cloud, serta peta berlabel tanpa ubin eksternal. [Bukti browser](screenshots/manifest.json)

Pada periode default, uji teknis dari Ringkasan berhasil membuka tiga alur:

- **Dapur.** Payakumbuh mempunyai proporsi pesanan terlambat tertinggi, 22,4% atau 49 dari 219 pesanan.
- **Stok.** Saus teriyaki Payakumbuh tersisa 48 ml dengan batas pesan ulang 103 ml. Riwayat terbuka untuk bahan dan cabang yang sama.
- **Biaya dan laba.** Peringatan Family Feast Box membuka rincian resep senilai Rp58.320 per unit.

Screenshot diambil pada desktop dan Ringkasan diperiksa pada lebar 390, 768, 1366 dan 1920 piksel. Waktu tampil grafik di manifest berasal dari satu lintasan browser lokal.

[Bukti laporan](BUKTI_LAPORAN.md) memuat 15 tangkapan visual dari aplikasi dan temuan untuk 15 pertanyaan bisnis pada periode default. Perhitungan ulang dari CSV bersih lulus 24 dari 24 pemeriksaan KPI di tiga skenario filter.

## Putaran uji pengguna

Gunakan [FigCraft](design/ChickFlow-Prototype.figcraft) untuk putaran pertama dan Streamlit untuk putaran kedua. [Naskah dan lembar sesi](prototype/README.md) sudah siap. Jadwalkan putaran kedua setelah perbaikan dari temuan pertama diterapkan. Kedua putaran masih menunggu responden.

[Evaluasi AI lima skenario](prototype/walkthrough-ai.md) mencatat 15 pemeriksaan struktur FigCraft dan 15 tugas browser Streamlit yang lulus, serta hambatan navigasi pada ponsel dan keyboard. Evaluasi ini melibatkan 0 responden manusia.

[Bukti revisi](prototype/revision/README.md) mencatat tiga pasangan screenshot sesudah hambatan tersebut ditangani. Uji ulang meluluskan 15 dari 15 tugas. Tautan stok tampil pada layar awal ponsel, dan langkah Tab turun dari 43 ke 17 untuk riwayat stok serta dari 29 ke 15 untuk biaya resep.

## Catatan penggunaan AI

ChatGPT dan Codex membantu perencanaan, desain, implementasi dan pengujian. Lampiran D mencatat kontribusi alat, termasuk ImageGen pada foto ilustrasi. Penulis tugas perlu mencatat verifikasi yang ia lakukan sendiri.
