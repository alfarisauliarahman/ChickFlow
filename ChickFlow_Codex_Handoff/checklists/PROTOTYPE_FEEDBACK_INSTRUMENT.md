# Prototype & Usability Test Instrument (template — BELUM ada hasil)

**PENTING:** seluruh kotak di bawah adalah format pengumpulan data, **bukan responden, jawaban, atau hasil uji nyata**. Lakukan dua putaran pada prototype yang benar-benar ada. Target 5 responden bila memungkinkan, catat angka sesungguhnya.

## Informasi sesi

| Field | Diisi saat pengujian |
|---|---|
| Versi prototype | `v1` / `v2` |
| Tanggal uji | ... |
| Penguji & pengamat | ... |
| ID responden anonim | `P01`–`P05` atau sesuai realita |
| Persona/peran responden | ... |
| Laptop/browser/resolusi | ... |
| Seed/data hash | ... |
| Periode filter awal | ... |
| Persetujuan penggunaan umpan balik untuk tugas | ya/tidak; simpan tanpa PII |

## Task A — Temukan cabang dengan delayed rate tertinggi

**Prompt:** “Cari cabang yang paling membutuhkan perhatian karena proporsi pesanan terlambat dalam 7 hari terakhir. Tunjukkan angkanya dan halaman buktinya.”

- Expected path: Overview → Kitchen → delayed grouped chart / table → periksa n/N.
- Success 0/1: ...; durasi detik ...; klik ...; kesalahan ...; komentar verbatim singkat ...
- Periksa jika responden salah membaca count vs percentage.

## Task B — Temukan menu populer namun bermargin rendah

**Prompt:** “Pilih menu yang cukup laris tetapi margin kotor makanannya rendah. Tunjukkan perhitungan dari revenue dan food cost.”

- Expected path: Overview → Profit → margin scatter + detail menu.
- Success 0/1: ...; durasi ...; hambatan ...; komentar ...
- Periksa label `Food Gross Profit` vs salah tafsir `net profit`.

## Task C — Temukan bahan kritis pada tanggal akhir tertentu

**Prompt:** “Cari bahan yang stoknya berada di bawah titik pesan ulang pada akhir tanggal yang dipilih, untuk satu cabang.”

- Expected path: Inventory → set cutoff end date/branch → critical table → lihat unit/gap.
- Success 0/1: ...; durasi ...; hambatan ...; komentar ...
- Periksa apakah user paham tanggal sebagai as-of dan kategori tidak mengubah stock.

## Three-second test

Tampilkan screenshot Overview pertama selama tepat 3 detik, lalu sembunyikan. Tanyakan:

1. Informasi/aksi apa yang paling menonjol?
2. Di mana Anda akan mencari pesanan terlambat?
3. Apakah Anda tahu dataset ini simulasi?

Scoring: `recognizes primary action: 1/0`, `recognizes delayed: 1/0`, `recognizes synthetic: 1/0`. Jangan mengklaim hasil tanpa menjalankan.

## Skala umpan balik 1–5

1. Mudah mengetahui masalah operasional paling penting.
2. Filter tanggal/cabang/kategori mudah dipahami.
3. Warna dan visualisasi mudah dibaca.
4. Istilah margin/food cost jelas.
5. Saya merasa yakin angka berasal dari sumber yang konsisten.

Tambahan terbuka: “Bagian mana paling membingungkan?”, “Apa 1 perubahan yang akan Anda lakukan terlebih dahulu?”

## Data processing / change log

| Problem ID | Evidence v1 | Severity | Proposed change | Implemented in v2 | Retest result |
|---|---|---|---|---|---|
| UX-001 | ... | high/medium/low | ... | ... | ... |
| UX-002 | ... | ... | ... | ... | ... |
| UX-003 | ... | ... | ... | ... | ... |

## Result summary (only fill after real test)

- Number respondents v1: ...; v2: ...
- Task success rate A/B/C: ... / ... / ...
- Median completion time: ...
- Three-second action recognition: ... of ... respondents
- Satisfaction 1–5: mean ...; sample n ...
- Top 3 themes: ..., ..., ...
- What changed from v1→v2: ...
- Remaining limitations: ...
