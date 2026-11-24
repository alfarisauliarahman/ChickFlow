# Bukti revisi antarmuka ChickFlow

Revisi ini menindaklanjuti [walkthrough AI sebelum perubahan](../walkthrough-ai.md). Kedua tangkapan setiap pasangan diambil dari Streamlit pada awal halaman, dengan periode **24–30 Oktober 2026 WIB**, semua cabang, dan semua kategori.

## Perbandingan sebelum dan sesudah

| Tampilan dan perubahan | Sebelum | Sesudah | Hasil |
|---|---|---|---|
| Ringkasan ponsel 390 × 844. **Cek stok** muncul sebelum kartu KPI saat ada peringatan stok kritis. | [PNG sebelum](before-ringkasan-mobile.png) | [PNG sesudah](after-ringkasan-mobile.png) | Posisi atas tautan berpindah dari y = 874 px ke y = 494 px. Tautan tampil penuh pada layar awal. |
| Persediaan bahan 1366 × 768. **Lihat riwayat stok** muncul setelah ringkasan stok dan sebelum tabel. | [PNG sebelum](before-stok.png) | [PNG sesudah](after-stok.png) | Kontrol berpindah dari y = 1019 px ke y = 489 px. Langkah Tab dari halaman persediaan turun dari **43 menjadi 17**. |
| Biaya dan laba 1366 × 768. **Cek biaya resep** tampil di samping judul perhitungan laba, sebelum KPI, grafik dan tabel. | [PNG sebelum](before-biaya-resep.png) | [PNG sesudah](after-biaya-resep.png) | Kontrol berpindah dari y = 740 px ke y = 333 px. Langkah Tab dari halaman biaya dan laba turun dari **29 menjadi 15**. |

[Pasangan Ringkasan ponsel dalam satu gambar](perbandingan-ringkasan-mobile.png) · [Metadata sebelum](before.json) · [Metadata sesudah](after.json)

Uji ulang lima skenario AI menghasilkan **15 dari 15 tugas lulus**. Ukuran langkah Tab berasal dari skenario SIM-04 dan posisi ponsel dari SIM-05. [Log sebelum](../walkthrough-ai.json) · [Log uji ulang](../walkthrough-ai-retest.json)

## Penempatan dalam laporan

Bagian **6.6** template Word meminta screenshot setiap halaman beserta penjelasan komponen. Bagian **7.4** meminta temuan, tugas yang diuji, dan perubahan yang dilakukan. **Lampiran F** memuat log perubahan prototipe. Pasangan screenshot ini bisa dipakai sebagai bukti pendukung Bab VII.3, VII.4, atau Lampiran F. Instruksi perbandingan sebelum–sesudah yang eksplisit pada bagian **4.4** mengacu pada pembersihan data.

**Usulan caption.** Perbandingan posisi tindakan Cek stok sebelum dan sesudah revisi Ringkasan ponsel. Tangkapan diambil pada viewport 390 × 844 dengan cakupan data yang sama.

Pemeriksaan ini merupakan evaluasi teknis berbasis skenario AI. Jumlah responden manusia pada pengujian ini adalah **0**.
