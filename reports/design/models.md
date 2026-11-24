# Model ChickFlow

## Use case

```mermaid
flowchart LR
    manager[Manajer] --> review((Tinjau KPI dan insight))
    manager --> orders((Telusuri pesanan))
    kitchen[Kepala dapur] --> delay((Periksa SLA dan waktu persiapan))
    buyer[Pengadaan] --> stock((Periksa stok per tanggal dan mutasi))
    owner[Pemilik] --> sales((Bandingkan penjualan cabang))
    owner --> margin((Periksa margin dan resep))
    review --> filter((Atur tanggal cabang dan kategori))
    orders --> filter
    delay --> filter
    stock --> filter
    sales --> filter
    margin --> filter
```

## Alur pesanan

```mermaid
flowchart LR
    incoming[Pesanan masuk] --> cancel{Pembatalan?}
    cancel -- Ya --> canceled[Batalkan sebelum produksi]
    cancel -- Lanjut --> pay[Pembayaran simulasi]
    pay --> queue[Antrean dapur]
    queue --> ready[Pesanan siap dan stok terpakai]
    ready --> sla[Hitung durasi dan bandingkan SLA]
    sla --> complete[Serah terima dan pengakuan transaksi]
    complete --> feedback[Ulasan sintetis opsional]
```

Katalog dan ERD sembilan tabel tercantum pada spesifikasi [kontrak data](../../ChickFlow_Codex_Handoff/docs/03_DATA_CONTRACTS.md). File desain interaktif [layouts.html](layouts.html) berisi 12 tampilan untuk enam modul.
