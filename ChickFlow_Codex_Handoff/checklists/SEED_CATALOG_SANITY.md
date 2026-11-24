# SEED CATALOG SANITY — deterministic cost reference (not generated sales results)

This is a **planning-level checksum** calculated directly from the proposed BOM/ingredient unit costs in `docs/15`. It is **not** a run of the ChickFlow generator, not a dashboard outcome, and excludes discounts and any cost changes. Codex should match this reference before writing random order simulation. Integer IDR arithmetic, no fractional unit costs in this fixture.

| SKU | Menu | Planned price (Rp) | Derived BOM cost per SKU (Rp) | Catalogue margin (before discounts) |
|---|---|---:|---:|---:|
| M01 | Original Crispy Chicken | 22,000 | 9,340 | 57.55% |
| M02 | Spicy Crispy Chicken | 24,000 | 10,120 | 57.83% |
| M03 | Crispy Chicken Breast | 26,000 | 10,952 | 57.88% |
| M04 | Smoky BBQ Chicken | 29,000 | 10,830 | 62.66% |
| M05 | Mozza Crunch Chicken | 32,000 | 12,002 | 62.49% |
| M06 | Original Chicken Rice | 32,000 | 10,851 | 66.09% |
| M07 | Spicy Chicken Rice | 34,000 | 11,826 | 65.22% |
| M08 | Teriyaki Chicken Rice | 35,000 | 13,067 | 62.67% |
| M09 | Fire Chicken Rice Bowl | 33,000 | 12,604 | 61.81% |
| M10 | BBQ Chicken Wings | 32,000 | 13,176 | 58.83% |
| M11 | Hot Chicken Wings | 33,000 | 13,301 | 59.69% |
| M12 | Crunchy Wings Bucket | 49,000 | 21,232 | 56.67% |
| M13 | Classic Chicken Burger | 31,000 | 13,613 | 56.09% |
| M14 | Spicy Chicken Burger | 32,000 | 14,243 | 55.49% |
| M15 | Double Chicken Burger | 34,000 | 23,451 | 31.03% |
| M16 | Crispy Chicken Wrap | 30,000 | 12,850 | 57.17% |
| M17 | Classic French Fries | 16,000 | 6,520 | 59.25% |
| M18 | Loaded Cheese Fries | 26,000 | 11,205 | 56.90% |
| M19 | Chicken Nugget Bites | 24,000 | 8,528 | 64.47% |
| M20 | Fresh Coleslaw | 14,000 | 5,560 | 60.29% |
| M21 | Iced Tea | 10,000 | 2,640 | 73.60% |
| M22 | Fresh Lemon Tea | 14,000 | 4,640 | 66.86% |
| M23 | Cola Fizz | 16,000 | 5,440 | 66.00% |
| M24 | Family Feast Box | 69,000 | 58,320 | 15.48% |

## Reference tests to implement

- `assert len(menu) == 24`, `assert len(ingredients) == 27`, `assert len(recipes_composite) >= 24` and all 24 SKUs have BOM.
- Every recipe ingredient matches the ingredient master; no duplicate composite `(menu_id, ingredient_id)`.
- `M24` flattened BOM exactly aggregates `4×M01 + 2×M17 + 3×M21`, **without** also counting those component SKUs as separate sold line items.
- For each SKU, `derived_unit_food_cost_idr` should equal the reference values in this table until config changes are explicitly documented.
- The percentages in this table are **pre-discount seed diagnostics**, NOT observed net-sales margins. Actual profit per menu must account for allocated transaction discounts and sold quantities.
- If the cost catalog has implausible outcome, change ingredient master/BOM with a documented ADR, regenerate reference and all raw/clean datasets, and rerun every reconciliation test.

## Quick consistency sample

The hypothetical `M24` Family Feast combines the component recipes as a **single saleable SKU**. At list price Rp69.000, its computed pre-discount margin is relatively low by design; this supplies a realistic teaching case **without hardcoding any final low-margin alert outcome**.
