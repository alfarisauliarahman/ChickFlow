# Uji prototipe ChickFlow

Siapkan dua versi dengan periode awal **24–30 Oktober 2026**, semua cabang, dan semua kategori. Gunakan [FigCraft](../design/ChickFlow-Prototype.figcraft) dalam mode Present untuk putaran pertama. Gunakan dashboard Streamlit enam halaman untuk putaran kedua, setelah temuan pertama diterapkan.

## Naskah untuk penguji

“Ini dashboard restoran dengan data simulasi. Kerjakan setiap tugas seperti biasa. Kamu boleh berpikir keras atau menyampaikan apa yang membingungkan.”

Tampilkan Ringkasan selama tiga detik, lalu sembunyikan. Tanyakan apa yang menarik perhatian pertama, di mana mereka akan mencari pesanan terlambat, dan apakah mereka tahu datanya simulasi. Targetkan lima responden dan catat jumlah yang benar-benar ikut.

1. “Cari cabang dengan persentase pesanan terlambat tertinggi. Tunjukkan persentasenya.”
2. “Cari bahan yang perlu dipesan ulang. Sebutkan cabang dan berapa stok yang tersisa.”
3. “Cari menu bermargin rendah. Buka rincian biaya resepnya.”

Mulai hitung waktu saat tugas dibacakan. Gunakan ID responden anonim. Catat berhasil atau belum berhasil, waktu, klik, dan hambatan di [lembar sesi](sessions.csv). Simpan temuan dan revisi di [log perubahan](changes.csv). Gunakan [instrumen lengkap](../../ChickFlow_Codex_Handoff/checklists/PROTOTYPE_FEEDBACK_INSTRUMENT.md) untuk pertanyaan kepuasan.

## Status

Ketiga alur telah diperiksa secara otomatis di Streamlit. Lembar responden tetap kosong sampai ada sesi nyata. Hasil browser tersimpan pada [bukti teknis](../screenshots/manifest.json).

[Walkthrough AI](walkthrough-ai.md) mencatat lima skenario pengujian teknis di FigCraft dan Streamlit. Metode dan hasilnya didokumentasikan terpisah dari lembar sesi responden.

[Bukti sebelum dan sesudah revisi](revision/README.md) memuat enam tangkapan layar dan perbandingan jumlah langkah Tab setelah perbaikan.
