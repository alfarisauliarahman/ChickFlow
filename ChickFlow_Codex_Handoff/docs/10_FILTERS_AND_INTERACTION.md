# 10 — Cross-page filters, time semantics, interaction contracts

## 10.1 Why this is a critical contract

A beautiful dashboard can be wrong if filtering category in a line-item table multiplies order counts, or if filtering date range accidentally removes opening stock from inventory. Before implementing UI, implement filtered facts as pure functions and exercise this matrix.

**Global filter context:** `date_start`, `date_end`, `branch_ids`, `categories`. Selected empty branch/category tuple means **All**. Local page controls (channel, status, Top-N, breakdown, ingredient) do not mutate global context unless explicitly configured.

## 10.2 Core filter applicability matrix

Legend: `Y`=applies, `ASOF`=end-date cutoff only, `ATTR`=only for attributed usage, `N/A`=does not apply; UI must disclose N/A.

| Object / Metric | Date range | Branch | Category | Notes |
|---|---|---|---|---|
| Net Revenue | Y | Y | Y | item-line; category-specific revenue |
| Food COGS / GP / Margin | Y | Y | Y | item-line cost allocation |
| Total completed Orders | Y | Y | Y* | unique order containing any selected category |
| AOV / Omzet kategori per pesanan | Y | Y | Y* | omzet item kategori ÷ jumlah pesanan unik yang memuat kategori |
| Prep mean/median/p90 | Y | Y | Y* | order contains category; prep measured order level |
| Delayed Rate | Y | Y | Y* | completed selected orders; once per order |
| Units Sold | Y | Y | Y | item-line quantity |
| Cancel Count/Rate | Y | Y | N/A | canceled don't have line items; show scope |
| Feedback count/rating | Y | Y | Y* | orders selected by matching item category |
| Inventory Ending Stock | ASOF | Y | N/A | **all historical movements** through end-date |
| Critical Inventory Count | ASOF | Y | N/A | count branch/ingredient, no “sum mixed units” |
| Waste Cost | Y | Y | N/A | waste event not menu-specific |
| Ingredient Consumption from Sales | Y | Y | ATTR | recipe attribution for filtered sold items |
| Branch Map Marker Revenue | Y | Y | Y | 3 fictional representative city points |
| Word Cloud | Y | Y | Y* | feedback linked once to eligible orders |
| Order Flow Diagram | N/A | N/A | N/A | static business-process representation |

`Y*`: infer `selected_order_ids = DISTINCT(order_items.order_id WHERE menu.category IN selected_categories AND order eligible)` then filter `orders` to IDs once. With no category selection, all eligible orders. Never duplicate orders in join.

## 10.3 Time range and timezone

- Operate with `date` in Asia/Jakarta; backend timestamp stored aware. Filter 1–7 Oct inclusive translated to start 1 Oct 00:00 and end **8 Oct 00:00 exclusive**.
- Orders use `ordered_at` local date for sales/kitchen/order analytics even if `ready_at` or `completed_at` crosses midnight. This simulation opens until 22:00, but long queues could cross day; preserve chosen ordering date consistently.
- Inventory uses event `occurred_at`, i.e. usage may take place after order date; as-of end-day is based on event time, not order_date.
- Report `simulation window 1–30 Okt 2026`, default last 7 complete days in data = 24–30 Okt.
- Date picker can't select after 30 Oct or before 1 Oct without showing meaningful empty state; no silent clamp that surprises user.
- Prior-period delta requires complete N calendar days before selected start. No partial comparison except explicit separate mode with footnote.

## 10.4 Category and mixed-grain examples

**Example:** O1 completed with `Chicken (Rp20k)` + `Iced Tea (Rp8k)` after alloc discount; O2 completed with `Iced Tea (Rp10k)` only.

- All: Revenue Rp38k, unique order count 2.
- Beverage selected: Revenue Rp18k, unique order count 2; AOV beverage revenue/order = Rp9k. Not Rp38k.
- Fried Chicken selected: Revenue Rp20k, order count 1; prep time O1 is one observation.
- If only Beverage category, Inventory On Hand still includes all sales item usage; it is **not** beverage-only theoretical inventory. Beverage ingredient attribution chart may use filtered orders and recipes.

## 10.5 Global filter implementation rules

- `main.py` registers state defaults exactly once: `filter_start`, `filter_end`, `filter_branch_ids`, `filter_categories`, `filter_revision`.
- Validate and normalize to immutable `FilterContext` before calling business functions; reduce `None/[]/"All"` ambiguity.
- Category options derive from master `menu` sorted in stable business order; branches derive from master `branches`; options not artificially reduced by other filters by default (to prevent disappearing selection).
- `st.form` optional to batch filter changes and reduce reruns, but if used, provide `Terapkan` button and `Reset` outside/inside consistent. Another acceptable design: immediate updates with state and caching.
- Sidebar/page nav actions don't reset filters; page-specific drilldown may set branch filter using documented method, with breadcrumb/clear.
- When a category selection does not apply to a card, display a note or info tooltip. **No silent exceptions.**
- Chart hide by clicking legend affects only chart visibility, not KPI underlying filter unless clearly linked.

## 10.6 Drilldown flows

**Alert A01 → Kitchen:** preserve global date/branch/category, set local channel/branch highlighted if rule specifically identifies; show `Berdasarkan filter aktif`.

**Alert A03 → Inventory:** preserve date range/branch, set local filter `only critical` and target ingredient if rule identifies; show as-of cutoff context. Category selection remains in topbar but is marked N/A for stock.

**Low Margin → Profit:** preserve filters; target menu expanded in profitability table, if chart selected from filtered category correct detail.

**Overview → Orders:** preserve global filters, local peak hour default to peak under context without changing global date.

## 10.7 Crossfilter behavior (optional, NOT core)

Chart Plotly `on_select` is allowed only after all global filter tests pass. If enabled, scope must be explicit:

- Bar click may set local page filter, not mutate global filters unexpectedly.
- Selection clear button must exist.
- No crossfilter if chart selection unsupported in environment; fallback to visible selectbox.
- Avoid coupling chart internal `selectedpoints` to backend keys without tests.

## 10.8 UX test matrix

| Scenario | Expected result |
|---|---|
| All defaults | 3 branches, 24–30 Oct date, all categories; zero error |
| One branch | branch metrics and branch map single point |
| Two branches | both totals correct, alert scoped |
| One category | revenue subset, order count unique, inventory unaffected and explicit scope |
| Two categories | union of matching order IDs; revenue only selected lines |
| One date | charts readable with 1-day data; growth N/A if incomplete |
| Full period | all 30 days, totals reconcile; prior comparison N/A |
| 0 order fixture | no crash, averages N/A, clear empty state |
| Selection reset | returns exactly defaults from manifest |
| Nav page switch | all filter states preserved |
| 1/2 selected days | previous period check accurate |
| Map tiles offline | fallback visible plus disclaimer |
| Different timezone environment | same WIB day labels and totals |

## 10.9 Export behavior

`Download CSV` exports **aggregated table currently shown**, *not raw unfiltered underlying data*, with metadata header/README if needed. The file name includes page, date range and selected scope; characters safe for Windows. CSV numeric values stored as raw numeric (not preformatted `Rp` text) for reuse; separately provide descriptive column labels in `docs/metric_dictionary.md`.

## 10.10 Cache and freshness

- App load receives `data/manifest.json` hash; cache invalidates if manifest hash changes (or explicit Reload action), avoiding stale graphs after regeneration.
- `st.cache_data` memoizes DataFrame loads and expensive feature building; input FilterContext is hashable (frozen dataclass or tuples).
- Never cache alert card text independently of filtered metrics; when filters change alert must recompute.
- One source `DataBundle` per run, not independently loaded CSV with differing time parses on six pages.
