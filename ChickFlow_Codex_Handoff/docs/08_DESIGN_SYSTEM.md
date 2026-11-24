# 08 — UI/UX, original design system, information architecture, wireframes

## 8.1 Arah estetika yang sengaja berbeda dari contoh Restora

**Arah produk:** `ChickFlow — Ops Control Room`. Semi-dark charcoal/navy dengan aksen amber, rasa dashboard analitik operasional yang modern, tegas, fungsional. **Bukan** meniru brand, komposisi, logo, palet, ilustrasi, atau tata letak contoh Restora/ZIP. Kita tidak memakai contoh sebagai acuan desain.

Prinsip: *signal over decoration*, cukup kontras, grafik lebih penting dari background, ruang kosong terstruktur, radius moderat, komponen stateful punya feedback.

## 8.2 Color tokens (proposal harus diuji kontras)

```python
DESIGN_TOKENS = {
  "bg_canvas": "#0B1220",       # navy sangat gelap
  "bg_sidebar": "#111C2E",
  "bg_card": "#17263C",
  "bg_card_hover": "#1E314D",
  "border_subtle": "#2C4161",
  "text_primary": "#F8FAFC",
  "text_secondary": "#C7D2E0",
  "text_muted": "#AABBD0",
  "accent_primary": "#F5B301",  # amber ChickFlow, teks gelap pada tombol amber
  "accent_blue": "#60A5FA",
  "success": "#34D399",
  "warning": "#FBBF24",
  "danger": "#FB7185",
  "neutral": "#94A3B8",
}
```

**Kontras:** pasangkan teks gelap `#0B1220` pada fill amber/kuning. Untuk teks white on colored alert, hitung WCAG contrast (target body ≥4.5:1) atau pakai body text putih di card gelap dan badge semantik hanya sebagai accent. Warna bukan satu-satunya sarana menyatakan sukses/critical: selalu sertakan ikon dan label.

**Chart palette:** Sales amber, Kitchen blue, Inventory mint, Profit violet, alerts pink/red; kategori berjumlah 7 gunakan warna yang berbeda + legend. Hindari representasi warna arbitrer per chart; build centralized `get_category_color(category)`.

## 8.3 Typography and spacing

- UI text `Inter` jika tersedia, fallback `Arial`, `sans-serif` (jangan menyertakan font proprietary).
- Page title 28–32px, heading 18–22px, KPI number 26–32px, body 14–16px, metadata 12px minimal.
- Grid spacing token 4,8,12,16,24,32px. Card padding 16–20px, radius 12–14px, border 1px.
- Line height 1.4–1.6; jangan pakai all-caps untuk banyak paragraf.
- KPI label satu baris bila mungkin, number line dua baris tidak clip.
- Baseline UI desktop: 1366×768; max content width sekitar 1480px; sidebar ~240px (Streamlit default nav bisa di-styling seperlunya tanpa brittle DOM selectors).

## 8.4 Sitemap

```text
User
 ├── Global filters (date, branch, category) — persistent across pages
 ├── Overview
 │    ├── Health KPIs
 │    ├── Alerts
 │    └── Branch/Revenue trend
 ├── Orders
 │    ├── Demand heatmap
 │    ├── Channel mix
 │    ├── Order detail
 │    ├── Customer review word cloud
 │    └── Process flowchart
 ├── Kitchen
 │    ├── Prep distribution
 │    ├── SLA/delay analysis
 │    └── Branch boxplots
 ├── Inventory
 │    ├── Critical stock table
 │    ├── Stock vs reorder chart
 │    └── Waste/usage
 ├── Sales
 │    ├── Time series
 │    ├── Menu leaderboard
 │    └── Geographic branch map
 └── Profit
      ├── Margin/discount cards
      ├── SKU margin scatter
      ├── Category GP bar
      └── Recipe COGS detail
```

**Navigasi:** ≤2 klik ke halaman utama (1 klik langsung sidebar), global filters always near top, breadcrumb optional. Tidak memecah halaman jadi sub-menu berlapis yang membingungkan.

## 8.5 Desktop wireframe utama (konseptual, original)

```text
┌────────────────┬────────────────────────────────────────────────────────────────┐
│ CHICKFLOW      │ Overview — Operations Intelligence                              │
│ ANALYTICS      │ Periode [ 7d   v ]  Cabang [ Semua v ]  Kategori [ Semua v ]    │
│                ├────────────────────────────────────────────────────────────────┤
│ > Overview     │  [Revenue] [Orders] [AOV] [Avg Prep]                           │
│   Orders       │  [Delayed] [Margin] [Critical Stock] [Food GP]                 │
│   Kitchen      ├────────────────────────────────────────────────────────────────┤
│   Inventory    │  INSIGHT TERPENTING: item/branch + nilai + tindakan + drill     │
│   Sales        ├─────────────────────────────────────┬──────────────────────────┤
│   Profit       │  REVENUE PER HARI                  │ DELAYED PER CABANG       │
│                │  time series line                 │ grouped bar              │
│                ├─────────────────────────────────────┴──────────────────────────┤
│ DEMO DATA      │ Branch comparison table | data context | disclaimer           │
└────────────────┴────────────────────────────────────────────────────────────────┘
```

Wireframe per halaman (lebih detail terdapat pada spesifikasi 06):

- **Orders:** row KPI → heatmap besar kiri, channel mix kanan → order searchable table → feedback word cloud + flowchart expander.
- **Kitchen:** row KPI→ histogram kiri, boxplot kanan → delayed branch×channel bar → bottleneck table.
- **Inventory:** as-of status header → low-stock table full-width → ratio-to-reorder chart → waste breakdown and usage.
- **Sales:** revenue trend full-width → menu ranking/category contribution → geo map+branch details.
- **Profit:** food GP summary + margin metrics → scatter units vs margin → bottom menu table & recipe cost.

Buat enam wireframe low-fi dan enam mockup hi-fi sebagai artefak desain Bab V dan Lampiran C. Screenshot Streamlit berjalan menjadi bukti implementasi Bab VI.

## 8.6 Four principles of good UI

| Prinsip | Implementasi konkret | Bukti & tes |
|---|---|---|
| Visual hierarchy | 1 pertanyaan utama per halaman, KPI dan insight prioritas di atas fold | uji 3 detik, screenshot 1366×768 |
| Consistency | shared tokens, shared KPI cards, filter bar, tooltip units, axis labels | audit 6 page screenshot dan style lint manual |
| User feedback | loading, no data, warning, error, alert drilldown, success feedback export | checklist state tests dan E2E |
| Accessibility | contrast, keyboard nav, alt/summary, tidak mengandalkan warna, descriptive table counterpart | color contrast check, keyboard walkthrough |

## 8.7 Information density guidance

- 8 KPI pada Overview boleh dua baris; jangan memaksa 12 kartu kecil sehingga label tak terbaca.
- Grafik menggunakan minimum height 280–360px; heatmap bisa 400px; responsif ke lebar kolom.
- Setiap chart: judul, 1 subheading/insight, chart, 1 footer yang menerangkan n atau scope.
- Batasi visual noise: minimal 2–3 gaya garis, tanpa animasi agresif, tidak pakai 3D pie/bar.
- Insight cards tidak boleh menutupi grafik saat hover; bukan notification toast terus-menerus.
- Data table menyediakan sort/search/export, bukan semua kolom mentah yang berlebihan.

## 8.8 Interaction feedback pattern

- **Loading:** `st.status`/spinner untuk load-data atau aggregate berat, tidak perlu spinner pada setiap perubahan cepat.
- **Success:** ketika unduh CSV tersedia, label `Unduh data sesuai filter`; tidak klaim data telah dikirim ke mana-mana.
- **Empty:** ikon netral + `Tidak ada data untuk kombinasi ini` + tombol reset.
- **Error:** `File dataset belum siap. Jalankan python -m chickflow.data.generate` + safe error ID di log. Jangan menampilkan traceback panjang ke pengguna kecuali debug mode.
- **Warning:** user tahu angka dan threshold yang dilanggar; disabled alert bila n terlalu kecil.
- **Tooltips:** definisi metric dan unit, bukan deskripsi dekoratif.

## 8.9 Visual quality QA at three widths

- **1920px:** chart area tidak melebar tidak proporsional.
- **1366px:** KPI tidak overflow, nav readable, bar labels visible, chart tooltip tidak memotong.
- **768px (tablet):** KPI 2 columns, chart 1 column, sidebar collapsible, filter wrap, tables horizontally scroll with clear label.
- **375px (opsional):** app minimal terbaca, bukan prioritas nilai; jika sulit, dokumentasikan batasannya, jangan klaim full mobile support.

## 8.10 Brand assets

- Logo ChickFlow **orisinal**: inisial CF dikombinasikan dengan stylized wing/stream motif sederhana. Gunakan SVG buatan sendiri.
- Tidak perlu mengambil foto restoran nyata; gunakan bentuk/ilustrasi abstrak buatan sendiri. Hak cipta aset yang digunakan dicatat.
- Simpan `assets/brand/README.md` berisi sumber/izin aset; jika pakai aset publik, tuliskan lisensinya; jangan mengklaim logo Restora orisinal.
