# ChickFlow

ChickFlow adalah dashboard analitik historis restoran cepat saji fiktif dengan cabang Padang, Bukittinggi, dan Payakumbuh. Data simulasi mencakup 1–30 Oktober 2026. Dashboard membaca sembilan tabel bersih dan menampilkan enam modul Streamlit.

## Menjalankan aplikasi

Gunakan Python 3.12. Dari root proyek:

```bash
uv sync --locked --extra dev
uv run streamlit run app/main.py
```

Alternatif dengan pip:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install --no-deps -e .
streamlit run app/main.py
```

Pilih periode, cabang, dan kategori di baris filter di atas dashboard. Saat kategori dipilih, kartu nilai rata-rata pesanan menampilkan omzet item kategori per pesanan unik yang memuat kategori tersebut. Pembatalan, stok fisik, dan biaya bahan terbuang memakai filter periode dan cabang. Saldo stok berlaku sampai akhir tanggal WIB yang dipilih.

## Mengulang data dan pengujian

```bash
uv run python -m chickflow.data.generate
uv run python -m chickflow.data.clean
uv run python -m chickflow.data.validate
uv run python -m chickflow.data.build_marts
uv run python -m chickflow.reports.eda
uv run python -m chickflow.reports.verify_kpis
uv run pytest -q
```

Dataset seed `20261001` disertakan di `data/raw/` dan `data/clean/`. Generator menyediakan pilihan `--seed`. Simpan percobaan seed lain di folder output terpisah agar data demo dan bukti tetap konsisten.

- `data/manifest.json` berisi periode, seed, jumlah baris, hash CSV, dan ringkasan cleaning.
- `reports/data_quality.json` berisi rekonsiliasi dan hasil validasi sembilan tabel.
- `reports/eda/` berisi empat grafik Matplotlib dan Seaborn, profil data, serta enam temuan terhitung.
- [DESIGN.md](DESIGN.md) mencatat keputusan desain dan referensi.
- [Prototipe FigCraft](reports/design/ChickFlow-Prototype.figcraft) memuat enam wireframe, enam layar utama, dan alur detail yang dapat diklik.
- [Model sistem](reports/design/models.md) memuat use case dan alur pesanan.
- [Status implementasi](reports/STATUS.md) mencatat bukti dan pekerjaan yang masih pending.
- [Bukti laporan](reports/BUKTI_LAPORAN.md) menghubungkan 15 visual dashboard dan 15 pertanyaan bisnis dengan hasil validasi KPI.

## Uji pengguna

Gunakan [prototipe FigCraft](reports/design/ChickFlow-Prototype.figcraft) untuk putaran pertama dan aplikasi Streamlit untuk putaran kedua. [Panduan sesi](reports/prototype/README.md) berisi urutan tugas dan lembar pencatatan.

## Istilah

Laba kotor makanan adalah omzet bersih dikurangi biaya bahan dan kemasan langsung. Biaya bahan terbuang dihitung terpisah. Peta menampilkan titik pusat kota representatif di atas garis batas provinsi yang tersimpan lokal. Peta dasar daring tersedia sebagai pilihan.
