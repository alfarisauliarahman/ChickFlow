# 15 — Concrete seed catalog: 24 menu SKUs, 27 ingredients, BOM recipes

**Mengapa ada dokumen ini:** Codex tidak perlu mengarang nama menu, bahan, harga, atau resep secara sembarang. Semua angka di bawah adalah **parameter simulasi yang sengaja dibuat**, bukan harga pasar aktual atau klaim biaya restoran nyata. Dapat berubah hanya setelah tes profit/stock mengharuskannya dan perubahan dicatat.

## 15.1 Ingredient master (27 bahan)

| ID | Ingredient | Satuan basis | Biaya sintetik per basis unit (Rp) | Kelompok |
|---|---|---|---:|---|
| I01 | Daging paha ayam | g | 48 | Protein |
| I02 | Fillet dada ayam | g | 55 | Protein |
| I03 | Sayap ayam | g | 43 | Protein |
| I04 | Tepung crispy mix | g | 16 | Dry goods |
| I05 | Minyak goreng | ml | 25 | Oil |
| I06 | Bumbu rempah | g | 55 | Seasoning |
| I07 | Nasi matang | g | 12 | Carb |
| I08 | Roti burger | pcs | 3.000 | Carb |
| I09 | Keju slice | pcs | 1.600 | Dairy |
| I10 | Selada | g | 45 | Produce |
| I11 | Tomat | g | 35 | Produce |
| I12 | Mayonnaise | ml | 50 | Condiment |
| I13 | Saus pedas | ml | 65 | Condiment |
| I14 | Saus barbeque | ml | 60 | Condiment |
| I15 | Saus teriyaki | ml | 70 | Condiment |
| I16 | Kentang | g | 32 | Carb |
| I17 | Kubis | g | 22 | Produce |
| I18 | Wortel | g | 26 | Produce |
| I19 | Telur | pcs | 2.200 | Protein |
| I20 | Tortilla | pcs | 2.600 | Carb |
| I21 | Konsentrat teh | ml | 40 | Beverage |
| I22 | Sirup gula | ml | 45 | Beverage |
| I23 | Perasan lemon | ml | 75 | Beverage |
| I24 | Soda | ml | 18 | Beverage |
| I25 | Air | ml | 3 | Beverage |
| I26 | Gelas dan tutup | pcs | 850 | Packaging |
| I27 | Kotak makanan | pcs | 1.200 | Packaging |

**Satuan:** biaya I08/I09/I19/I20/I26/I27 per 1 pcs; bahan lain per g/ml. Simulasi komponen kemasan dihitung di BOM food cost (meski secara akuntansi bisa diklasifikasi sebagai packaging COGS). **Label UI lebih akurat:** `Food & Packaging COGS` bila kemasan dimasukkan. Keputusan final v1: kolom KPI tetap `Food COGS` dengan tooltip **“bahan dan kemasan langsung sesuai resep”**, bukan semua overhead.

**Biaya resep:** unit cost dari tabel bahan, hasil `SUM(qty × unit cost)` dibulatkan half-up ke IDR, disimpan di line snapshots.

## 15.2 Menu SKU catalog (24 item)

| SKU | Menu resmi | Kategori | Harga list Rp | Station | Popularity (weight) |
|---|---|---|---:|---|---:|
| M01 | Original Crispy Chicken | Fried Chicken | 22.000 | FRYER | 12 |
| M02 | Spicy Crispy Chicken | Fried Chicken | 24.000 | FRYER | 11 |
| M03 | Crispy Chicken Breast | Fried Chicken | 26.000 | FRYER | 8 |
| M04 | Smoky BBQ Chicken | Fried Chicken | 29.000 | FRYER | 7 |
| M05 | Mozza Crunch Chicken | Fried Chicken | 32.000 | FRYER | 5 |
| M06 | Original Chicken Rice | Rice Meal | 32.000 | ASSEMBLY | 10 |
| M07 | Spicy Chicken Rice | Rice Meal | 34.000 | ASSEMBLY | 9 |
| M08 | Teriyaki Chicken Rice | Rice Meal | 35.000 | ASSEMBLY | 7 |
| M09 | Fire Chicken Rice Bowl | Rice Meal | 33.000 | ASSEMBLY | 8 |
| M10 | BBQ Chicken Wings | Wings | 32.000 | FRYER | 8 |
| M11 | Hot Chicken Wings | Wings | 33.000 | FRYER | 7 |
| M12 | Crunchy Wings Bucket | Wings | 49.000 | FRYER | 4 |
| M13 | Classic Chicken Burger | Burger | 31.000 | GRILL | 9 |
| M14 | Spicy Chicken Burger | Burger | 32.000 | GRILL | 8 |
| M15 | Double Chicken Burger | Burger | 34.000 | GRILL | 5 |
| M16 | Crispy Chicken Wrap | Burger | 30.000 | ASSEMBLY | 6 |
| M17 | Classic French Fries | Sides | 16.000 | FRYER | 10 |
| M18 | Loaded Cheese Fries | Sides | 26.000 | FRYER | 6 |
| M19 | Chicken Nugget Bites | Sides | 24.000 | FRYER | 8 |
| M20 | Fresh Coleslaw | Sides | 14.000 | ASSEMBLY | 5 |
| M21 | Iced Tea | Beverage | 10.000 | DRINK | 13 |
| M22 | Fresh Lemon Tea | Beverage | 14.000 | DRINK | 9 |
| M23 | Cola Fizz | Beverage | 16.000 | DRINK | 7 |
| M24 | Family Feast Box | Combo | 69.000 | FRYER | 5 |

**Catatan:** Kategori `Combo` bisa muncul sebagai satu line SKU dengan BOM flattened, tidak menciptakan child order items untuk item internal. Kategori khusus `Burger` termasuk wrap untuk kesederhanaan; UI menu bisa menggunakan label `Burger & Wrap` asalkan enum konsisten. Menu menunggu persiapan dari station assigned; `Family Feast Box` kerja station FRYER paling berat.

## 15.3 Formula BOM (qty × kode bahan)

Satuan qty mengikuti `15.1`. Daftar ini adalah **kontrak awal**, bukan sekadar contoh untuk dipilih sesuka hati.

| SKU | BOM (ingredient ID : qty per 1 unit) |
|---|---|
| M01 | I01:140, I04:30, I05:20, I06:8, I27:1 |
| M02 | I01:140, I04:30, I05:20, I06:8, I13:12, I27:1 |
| M03 | I02:150, I04:32, I05:22, I06:8, I27:1 |
| M04 | I01:145, I04:30, I05:22, I06:8, I14:20, I27:1 |
| M05 | I01:150, I04:32, I05:22, I06:8, I09:1, I12:10, I27:1 |
| M06 | I01:130, I04:26, I05:18, I06:7, I07:180, I27:1 |
| M07 | I01:130, I04:26, I05:18, I06:7, I07:180, I13:15, I27:1 |
| M08 | I02:125, I04:22, I05:16, I06:6, I07:180, I15:25, I27:1 |
| M09 | I02:120, I04:24, I05:18, I06:8, I07:175, I13:22, I27:1 |
| M10 | I03:200, I04:36, I05:30, I06:10, I14:25, I27:1 |
| M11 | I03:200, I04:36, I05:30, I06:10, I13:25, I27:1 |
| M12 | I03:350, I04:62, I05:48, I06:18, I14:30, I27:1 |
| M13 | I02:110, I04:18, I05:12, I06:5, I08:1, I10:20, I11:20, I12:18, I27:1 |
| M14 | I02:110, I04:18, I05:12, I06:5, I08:1, I10:20, I11:20, I12:15, I13:12, I27:1 |
| M15 | I02:210, I04:36, I05:24, I06:10, I08:1, I09:2, I10:20, I11:25, I12:20, I27:1 |
| M16 | I02:105, I04:20, I05:14, I06:5, I20:1, I10:20, I11:18, I12:16, I27:1 |
| M17 | I16:150, I05:12, I06:4, I27:1 |
| M18 | I16:165, I05:14, I06:5, I09:2, I12:18, I27:1 |
| M19 | I02:110, I04:28, I05:20, I06:6, I27:1 |
| M20 | I17:90, I18:45, I12:22, I06:2, I27:1 |
| M21 | I21:20, I22:10, I25:180, I26:1 |
| M22 | I21:22, I22:12, I23:25, I25:165, I26:1 |
| M23 | I24:250, I25:30, I26:1 |
| M24 | **Flatten** 4×M01 + 2×M17 + 3×M21; sum repeated ingredient quantities into **one** recipe row per ingredient for M24 |

**Important:** M24 physically includes 4 chickens, 2 fries, 3 drinks but customer buys **one Combo SKU**. For unit-sold chart, `M24 quantity=1` means **one family box**, not 9 menu units. Inventory BOM consumes all components. Compare `SKU units` vs `component-equivalent count` only with explicit derived metric; v1 uses SKU units.

## 15.4 Station prep base minutes

| Station | Example per SKU baseline and constraint |
|---|---|
| FRYER | M01/M02 9–11 min; wings 12–16; M24 18–24; max concurrency varies branch |
| GRILL | burger 6–10; M15 double 11–13 |
| ASSEMBLY | rice/wrap 5–9; coleslaw 2–3 |
| DRINK | tea/soda 1–3 |

**Simulation simplification:** station assigned at SKU level, not separate component operations, even though BOM combo has multiple foods. Family box fryer station bottleneck is a reasonable teaching abstraction. Do not imply exact real-world kitchen process.

Suggested per-branch slots (configurable):

| Branch | FRYER | GRILL | ASSEMBLY | DRINK | demand multiplier |
|---|---:|---:|---:|---:|---:|
| BR-01 Padang | 4 | 2 | 3 | 2 | 1.25 |
| BR-02 Bukittinggi | 3 | 2 | 2 | 2 | 1.00 |
| BR-03 Payakumbuh | 2 | 1 | 2 | 1 | 0.80 |

Peak concurrency and SLA should be calibrated by EDA so delayed rate not 0% for every branch and not near 100% unless explicitly documented. Adjust **capacity / demand parameters**, not raw `delayed_flag` outputs.

## 15.5 Demand default mix (simulation only)

- Channel baseline weights: Dine-in 38%, Takeaway 28%, Delivery 34%; branch-specific shift ±5–10 percentage points and normalize 100%.
- Mean items/order around 1.8–2.3 SKU line items, with 1–4 distinct SKU; qty 1 most common, 2 occasionally, 3+ rare.
- Date weights: weekday base1.0, Fri1.12, Sat1.25, Sun1.18; hour mixture high around 12 and 19, low near 10 and 21.
- Menu popularity from table; order items sample without replacement at the SKU-line level, but qty may exceed1.
- Cancellation target 2–3% and feedback response about 20–25% of completed orders; variability stochastic with deterministic seed.
- Discount rates candidate set `[0%, 5%, 10%, 15%]`; chance discounts higher on combo and selected delivery days. Never let net revenue negative.

## 15.6 Reorder policy generation

`expected_daily_usage_qty(branch, ingredient)` estimated from precomputed completed orders (or iterative seed demand plan). Define:

```text
reorder_point_qty = quantize_to_unit(max(minimum_qty, expected_daily_usage * 1.5))
opening_qty = quantize_to_unit(max(reorder_point_qty * 1.5, expected_daily_usage * 3))
restock_lot_qty = quantize_to_unit(expected_daily_usage * 5)
```

For zero-usage ingredients, policy still has small safe minimum with unit-aware scale. `quantize_to_unit` pcs→integer, g/ml→fixed precision; source `expected_daily_usage` is only simulation planning helper, not historic real consumption claim.

**Output scenario**: some critical stock events may occur depending on simulated receipts/waste; do not **force** critical event through fake ledger. For demonstrable low-stock alerts, tune reorder lead-time/lot or waste distribution, then rerun entire deterministic pipeline and QA. Document tuning changes.

## 15.7 Economics sanity check (analytical only)

- `M24` cost is expected close to net price; low margin is **intentional teaching scenario**, but the **actual margin** must be computed from I01..I27 and discounts. Do not hardcode “16%” in UI.
- `M15` double burger is likely food-cost heavier than single but cost computed, not asserted.
- Drinks have high nominal margin while volume driven; plot scatter margin vs units sold for business discussion.
- Cost does **not** include salaries, taxes, overhead, platform charges. Use precise naming.

## 15.8 Clean seed artifacts

Codex must create **actual** `config/menu.yaml`, `config/ingredients.yaml`, `config/recipes.yaml`, `config/branches.yaml` (or equivalent Python config masters) from these tables. Tests must assert every `menu_id`/`ingredient_id` appears with consistent names and an exact BOM. Record deviations from this plan in ADR and update source docs.
