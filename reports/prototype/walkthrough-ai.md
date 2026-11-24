# Walkthrough AI ChickFlow

Evaluasi teknis tanggal **24 November 2026 WIB** menggunakan lima skenario peran. **Jumlah responden manusia pada evaluasi ini: 0.** Cakupan pengujian adalah 24–30 Oktober 2026, semua cabang dan kategori, dengan seed 20261001.

Pada FigCraft, pemeriksaan menelusuri koneksi antarframe dan memastikan bukti jawaban muncul pada layar yang relevan. Pada Streamlit, setiap skenario menjalankan ketiga tugas di sesi browser baru. Skenario keyboard menekan Tab dan Enter. Pemeriksaan layar awal memakai posisi elemen terhadap tinggi viewport. [Log pengujian](walkthrough-ai.json)

## Hasil lima skenario

| Skenario | Perangkat dan jalur | A · Keterlambatan | B · Stok | C · Biaya resep | Temuan |
|---|---|---|---|---|---|
| SIM-01 · Pengguna baru | Laptop 1366 × 768, navigasi atas | Lulus | Lulus | Lulus | Tiga modul bisa dibuka dari navigasi atas. Ketiga tautan peringatan juga terlihat pada layar awal Ringkasan. |
| SIM-02 · Manajer operasional | Desktop 1920 × 1080, tautan peringatan | Lulus | Lulus | Lulus | **Cek dapur**, **Cek stok**, dan **Cek margin** mengarah ke modul terkait. Ketiganya terlihat pada layar awal. |
| SIM-03 · Staf persediaan | Laptop 1024 × 768, navigasi atas dan filter stok kritis | Lulus | Lulus | Lulus | Centang **Hanya bahan kritis** berfungsi. Riwayat stok terbuka untuk bahan dan cabang yang benar. Tautan **Cek margin** terlihat sebagian pada layar awal. |
| SIM-04 · Pengguna keyboard | Laptop 1366 × 768, Tab dan Enter | Lulus | Lulus | Lulus | Navigasi utama dapat diaktifkan lewat keyboard. Dari halaman tujuan, **Lihat riwayat stok** perlu 43 langkah Tab dan **Cek biaya resep** perlu 29 langkah dalam skenario ini. |
| SIM-05 · Pemilik melalui ponsel | 390 × 844, tautan peringatan setelah gulir | Lulus | Lulus | Lulus | Judul **Perlu diperiksa** terlihat pada layar awal. Ketiga tautan aksi memerlukan gulir. Di FigCraft, navigasi dari frame ponsel menuju layar detail desktop berlebar 1440 piksel. |

**Streamlit lulus 15 dari 15 jalur teknis.** Pemeriksaan struktur FigCraft menemukan 15 dari 15 jalur beserta bukti jawabannya. Angka ini menghitung kombinasi skenario dan tugas. Waktu penyelesaian, uji ingatan tiga detik, dan kepuasan menunggu sesi responden.

## Jawaban yang ditemukan pada dashboard

- **A · Keterlambatan.** Payakumbuh tertinggi dengan **22,4%**, atau **49 dari 219 pesanan**.
- **B · Stok.** Saus teriyaki di Payakumbuh tersisa **48 ml**, di bawah batas pesan ulang **103 ml**. Riwayat terbuka untuk bahan dan cabang yang sama.
- **C · Biaya resep.** Family Feast Box tercatat bermargin rendah. Biaya resepnya **Rp58.320 per unit** pada rincian menu.

## Temuan untuk revisi

1. Tempatkan **Cek stok** lebih awal pada Ringkasan ponsel agar tindakan paling mendesak langsung terlihat. Awal tautannya tercatat pada y = 874 px di viewport setinggi 844 px.
2. Dekatkan tombol menuju riwayat stok dan biaya resep dengan ringkasan masalah. Kurangi jumlah fokus yang harus dilewati pengguna keyboard sebelum bisa membuka rincian.
3. Bila alur ponsel juga akan diuji di prototipe, siapkan layar detail dengan lebar yang sama supaya navigasi dari Ringkasan ponsel bisa ditinjau utuh.

Untuk laporan, gunakan metode **evaluasi teknis berbasis skenario AI**, serta cantumkan cakupan dan sumber data di atas.
