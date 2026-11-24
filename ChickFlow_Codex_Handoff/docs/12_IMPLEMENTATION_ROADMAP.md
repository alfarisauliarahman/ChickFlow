# 12 — End-to-end implementation roadmap, task backlog, milestones

**Ini bukan estimasi deadline:** durasi aktual tergantung lingkungan, iterasi, debugging, dan pengujian. Jalankan fase berurutan; sebuah fase dianggap selesai **setelah acceptance check**, bukan setelah coding agent menulis summary. Format task ID `CF-###` digunakan lintas dokumen dan issue tracker.

## Milestone pelaksanaan v2.3

1. Fondasi, data, dan KPI (P0–P3). Buat logo, use case, enam wireframe, dan enam mockup saat menyusun fondasi. Validasi data sebelum menghubungkannya ke UI.
2. Prototipe v1. Ambil komponen P4–P6 yang diperlukan oleh Overview, Kitchen, Inventory, dan Profit. Jalankan CF-123 setelah ketiga tugas uji bisa dilakukan.
3. Dashboard v2. Lengkapi Orders dan Sales, dokumentasikan perbaikan berdasarkan feedback v1, lalu jalankan CF-125. Siapkan bukti P7–P8 dan deliverable pengumpulan setelah hasil uji tersedia.

## Phase 0 — Repository foundation & locked decisions

| ID | Task | Dependencies | Output / acceptance |
|---|---|---|---|
| CF-001 | Init repo, `.gitignore`, folder structure, AGENTS.md | none | tree sesuai doc09; no secrets |
| CF-002 | Setup Python environment and `pyproject.toml`/editable install | 001 | `import chickflow`, `python --version` recorded |
| CF-003 | Freeze conceptual scope & acceptance matrix | 001 | exact 6 modules documented |
| CF-004 | Config schema & simulation.yaml validation | 002 | invalid config raises clear error |
| CF-005 | Design tokens & UI copy glossary | 003 | centralized tokens, stable strings |
| CF-006 | Build test harness pytest, CI basic | 002 | `pytest -q` can run tiny fixture |
| CF-007 | ADR log, README baseline, issue template | 001 | architecture rationale stored |

**Gate P0:** empty project installs, tests run, scope locked.

## Phase 1 — Business model, master data & relational integrity

| ID | Task | Dependencies | Output / acceptance |
|---|---|---|---|
| CF-010 | Create branches master and coordinates (simulation disclaimer) | 004 | 3 validated branches |
| CF-011 | Create full 24-SKU menu/price/station/popularity | 004 | no duplicate SKU/category invalid |
| CF-012 | Create 25-ish ingredients, units and unit-cost | 004 | single unit per ingredient |
| CF-013 | Create flattened BOM recipes | 011,012 | every menu has BOM; cost computed |
| CF-014 | Branch inventory policy with opening/reorder lots | 010,012 | one policy for each branch×ingredient |
| CF-015 | Implement schema validation with explicit PK/FK | 010-014 | DB-like constraints pass |
| CF-016 | Document ERD and data dictionary | 010-015 | diagram accurate to code |
| CF-017 | Verify material costs and plausible margin opportunities | 013 | scenario diversity, not fake findings |

**Gate P1:** dimension tables and BOM valid; menu cost derives ingredients.

## Phase 2 — Deterministic simulated operations

| ID | Task | Dependencies | Output / acceptance |
|---|---|---|---|
| CF-020 | Date/branch/hour demand distribution engine | 010,004 | 3,600 target orders over 30 days, peaks exist |
| CF-021 | Order status/channel generation | 020 | canceled explicit, channel valid |
| CF-022 | Basket/items sampling weighted by menu and hour | 011,021 | completed orders 1+ item; canceled 0 |
| CF-023 | Snapshot prices, discount allocation | 022 | per-order gross-discount-net exact |
| CF-024 | Kitchen slot queue/scheduler & SLA derivation | 022,010 | prep derived timestamp; delay derived SLA |
| CF-025 | Recipe costing snapshots & line food GP | 013,023 | all cost from BOM, no random unrelated cost |
| CF-026 | Inventory OPENING/USAGE/RECEIPT/WASTE movements | 014,022,024 | usage matches recipe, no negative running stock |
| CF-027 | Feedback generator + themed Indonesian text | 024 | no PII, FK valid, rating 1..5 |
| CF-028 | Quality issues injection (controlled), clean pipeline | 020-027 | logged injection, deterministic repairs |
| CF-029 | Generate data manifest and all CSVs | 020-028 | config/hash/counts tracked |
| CF-030 | Build data integrity validator | 015,023-029 | asserts A01-A18 |
| CF-031 | Run 2 seeds, 2 repeat outputs; fix nondeterminism | 030 | same seed hash identical; different seed reasonable |
| CF-032 | Write EDA static reports Matplotlib/Seaborn | 030 | PNGs and summary text exist |

**Gate P2:** all D tests green; data ready. Do not build UI before this gate.

## Phase 3 — Analytical fact layer, KPI & rule engine

| ID | Task | Dependencies | Output / acceptance |
|---|---|---|---|
| CF-040 | Clean DataBundle loader + time types | 030 | no unexpected mutating imports |
| CF-041 | Facts `fact_sales_lines`, `fact_orders_eligible` | 040 | all joins obey grain |
| CF-042 | Global FilterContext normalization | 041 | three filters, immutable validated |
| CF-043 | Category-specific order ID selection | 041,042 | distinct orders, no double count |
| CF-044 | Revenue/orders/AOV/discount metrics | 041-043 | fixture exact |
| CF-045 | Kitchen mean/median/p90/delay metrics | 041-043 | SLA thresholds correct |
| CF-046 | COGS/GP/menu margin metrics | 041,043 | amount exact; zero safe |
| CF-047 | Stock as-of cumulative ledger | 040,042 | start_date does not reset stock |
| CF-048 | Consumption attribution vs physical stock semantics | 047,043 | category applies only attribution |
| CF-049 | Rule engine A01–A06 | 044-048 | n minimum and boundaries tested |
| CF-050 | Period comparison guard | 044 | incomplete prior window = N/A |
| CF-051 | Metric dictionary & fixture tables | 044-050 | all formulas documented |
| CF-052 | Run reconciliations across 3 branches×7 categories×date sets | 051 | no mismatch |

**Gate P3:** all M and R tests green, no inconsistent denominators.

## Phase 4 — Chart builders & visual evidence

| ID | Task | Dependencies | Output / acceptance |
|---|---|---|---|
| CF-060 | Shared plotly theme & standardized hover | 005,041 | labels and units uniform |
| CF-061 | Revenue line and branch/category bar | 060,044 | amounts reconcile |
| CF-062 | Menu units sorted bar + AOV chart | 060,044 | correct ranking |
| CF-063 | Weekday×hour heatmap | 060,045 | unique order counts |
| CF-064 | Prep histogram + boxplot | 060,045 | n counts, no hidden outliers |
| CF-065 | Delay branch×channel grouped bar | 060,045 | n/N and % |
| CF-066 | Margin scatter and GP contribution bar | 060,046 | low margin exact |
| CF-067 | Stock vs reorder / waste bar | 060,047 | units not incorrectly mixed |
| CF-068 | Word cloud from synthetic review texts | 040 | keyword table accessible |
| CF-069 | Business flowchart as qualitative view | 003 | process correct; not UI clone |
| CF-070 | MapLibre geo branch map + offline fallback | 060,044 | pins correctly labeled fictional |
| CF-071 | Chart registry PB→V with rationales | 061-070 | >=2 L,>=5 Q,>=1 G |
| CF-072 | Export static EDA evidence | 032,071 | all 5 mandatory libs used |

**Gate P4:** chart functions can be tested/inspected independent of Streamlit; no chart uses wrong grain.

## Phase 5 — UI shell, nav, shared components

| ID | Task | Dependencies | Output / acceptance |
|---|---|---|---|
| CF-080 | Streamlit entrypoint, 6 page registry | 002,005 | navigates to all pages |
| CF-081 | DataBundle `st.cache_data` loading | 040,080 | hash invalidation works |
| CF-082 | Global date/branch/category widgets | 042,080 | state persists pages |
| CF-083 | KPI cards with labels, deltas, tooltips | 051,080 | zero/null cases |
| CF-084 | Insight cards with actionable CTA | 049,080 | scope & n visible |
| CF-085 | Chart wrapper with empty/loading/errors | 060,080 | safe fallback |
| CF-086 | Data tables, search/CSV export | 080 | export equals current view |
| CF-087 | Apply original Ops Control Room theme | 005,080 | no borrowed sample composition |
| CF-088 | Privacy/fictional data banner | 080 | clearly marked synthetic |
| CF-089 | Basic 1366×768 and tablet responsive QA | 083-088 | no clip/overflow |

**Gate P5:** shell + components work; still not final pages.

## Phase 6 — Six complete pages

| ID | Task | Dependencies | Output / acceptance |
|---|---|---|---|
| CF-100 | Overview | 061,065,080-088 | 8 KPIs + alert + branch comparison |
| CF-101 | Orders | 062,063,068,069,086 | heatmap, channel, transactions, wordcloud, process |
| CF-102 | Kitchen Performance | 064,065,083-085 | stats, histogram, box, delay |
| CF-103 | Inventory | 067,047-048,086 | as-of and unit-aware stock view |
| CF-104 | Sales & Reports | 061,062,070,086 | trend, menu leaderboard, geo |
| CF-105 | Food Cost & Profit | 066,046,086 | proper GP/margins and BOM detail |
| CF-106 | Global filter integration matrix | 100-105 | no conflicts, N/A explained |
| CF-107 | Alert CTA navigation & context continuity | 100-106 | destination receives correct scope |
| CF-108 | Empty/error/loading/export behavior | 100-105 | U tests core pass |

**Gate P6:** six pages work and use **real computed data**. No filler graphs and no missing module hidden by tabs.

## Phase 7 — Academic-quality evaluation and visual polish

| ID | Task | Dependencies | Output / acceptance |
|---|---|---|---|
| CF-120 | Full unit/integration suite, fix all blockers | P6 | all Must tests green |
| CF-121 | AppTest UI smoke, browser manual test | 120 | six pages no crash |
| CF-122 | Run visual QA 1920/1366/768 widths | 121 | no clip, legible labels |
| CF-123 | Conduct prototype v1 feedback | 4 halaman inti dan 3 tugas siap | original feedback log |
| CF-124 | Prioritize UI fixes and implement v2 | 123 | change log + diff screenshots |
| CF-125 | Conduct prototype v2 retest | 124 | outcomes logged truthfully |
| CF-126 | Accessibility / contrast / keyboard audit | 124 | evidence for 4 UI principles |
| CF-127 | Performance measurements | 120,124 | measured cold/warm timings |
| CF-128 | Verify 5 library usage via logs/screenshots | 072,120 | claims substantiated |
| CF-129 | Complete evidence matrix and limitations | 120-128 | template mapping covered |

**Gate P7:** dashboard can withstand questioning: formula, dataset, chart selection, UI feedback, testing, evidence.

## Phase 8 — Delivery, demo and later report preparation

| ID | Task | Dependencies | Output / acceptance |
|---|---|---|---|
| CF-140 | Clean README install/run/seed/test instructions | P7 | exact working commands |
| CF-141 | Re-run from fresh checkout | 140 | no hidden local dependencies |
| CF-142 | Pin dependencies, freeze tested versions | 141 | requirements tested |
| CF-143 | Save screenshots per six module & required charts | P7 | genuine app captures |
| CF-144 | Data dictionary, ERD, metrics dictionary | P7 | docs match code |
| CF-145 | Write evidence notes for Bab I–IX (not final report) | 129,143 | no fabricated results |
| CF-146 | GitHub public/private repo based on user choice | 141 | secrets absent; README present |
| CF-147 | Optional deploy Streamlit | 141 | only if environment permits; fallback local demo |
| CF-148 | 3–5 min demo storyboard & recording script | 143 | covers filters and business questions |
| CF-149 | Slide outline and PDF report later | 145 | don't write conclusions before evidence |
| CF-150 | Final QA check all template checkboxes | 140-149 | complete or documented gaps |

**Gate P8:** reproducible repo, complete evidence, ready to prepare the actual academic report.

## Example implementation sprints (dependency based, not calendar promise)

1. **Sprint 1 — Foundation & data design:** CF-001..017.
2. **Sprint 2 — Simulation & data correctness:** CF-020..032.
3. **Sprint 3 — Analytical correctness:** CF-040..052.
4. **Sprint 4 — Visuals + shell:** CF-060..089.
5. **Sprint 5 — Six pages:** CF-100..108.
6. **Sprint 6 — QA, iteration, delivery:** CF-120..150.

## Mandatory checkpoints before coding agent proceeds

At end of each phase Codex must report:

```markdown
### Phase X review
- Implemented task IDs: CF-...
- Changed paths:
- Executed commands + actual exit status:
- Test results (counts, pass/fail/skips):
- Data totals/reconciliation, where relevant:
- Screenshots/evidence produced:
- Deviations from blueprint (reason + ADR):
- Known blockers or open TODO:
- Recommendation: proceed / do not proceed with next phase
```

**Stop conditions:** financial mismatch, negative stock, wrong filter grain, failed 6-module navigation, chart count shortfall, faked test results, unlicensed asset, or sample Restora design copied. Stop and fix, not bypass tests.
