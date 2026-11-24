# Release & Delivery Gates — DoD ChickFlow

## Rule for Codex

Mark a gate **PASS** only after citing an executed command/test output or inspected visual result. Do not mark PASS for planned/sketched code. If environment cannot execute, mark BLOCKED and give exact manual steps, without claiming success.

## Gate 0 — Reproducible environment

- [ ] Python version and install commands tested from clean repo.
- [ ] Editable package import works (`python -c "import chickflow"`).
- [ ] `pytest -q` runs in a new environment.
- [ ] `streamlit run app/main.py` starts (once app exists).
- [ ] No private secrets or fake real data.
- [ ] `AGENTS.md` installed in implementation repo.

## Gate 1 — Dataset integrity

- [ ] Nine tables match 03 contracts and 15 seed catalog.
- [ ] Completed orders >=500, period >=7 days, planned 3600 orders over 30 days.
- [ ] PK/FK and composite uniqueness validations pass.
- [ ] Cancelled orders have no line-items, no revenue or usage.
- [ ] Gross, discounts, net revenue reconcile **to Rp0**.
- [ ] Food cost calculated from BOM, unit costs and snapshot.
- [ ] Inventory usage from completed sales item×recipe; no negative running stock.
- [ ] Two same-seed runs produce equal normalized hashes.
- [ ] Raw/clean issue log and EDA created.

## Gate 2 — Analytical correctness

- [ ] Central FilterContext and facts implemented once.
- [ ] `orders_count = distinct orders`, not items.
- [ ] Category-specific revenue only selected lines, with proper order count.
- [ ] Prep from `ready_at - ordered_at`, strict `> SLA` for delay.
- [ ] Profit = net revenue − food/packaging direct COGS; no unsupported “net profit”.
- [ ] Stock as-of includes prior history, not only selected range.
- [ ] No divide-by-zero issues; undefined ratios display N/A.
- [ ] Rule tests on exact threshold and minimum denominator pass.

## Gate 3 — Visualization and curriculum

- [ ] ≥5 quantitative: line, bar, histogram, scatter, box plot; quality audit.
- [ ] ≥2 qualitative: word cloud dari teks ulasan sintetis + order flow diagram.
- [ ] ≥1 geographic: fictional branch map (or meaningful offline fallback).
- [ ] Plotly actual hover and charts show correct unit/label.
- [ ] Matplotlib and Seaborn static EDA images exist.
- [ ] All 15 PB have visualization registration.
- [ ] No copied Restora sample visual language.

## Gate 4 — Six-page app

- [ ] Overview fully interactive.
- [ ] Orders fully interactive (incl qualitative views).
- [ ] Kitchen fully interactive.
- [ ] Inventory fully interactive.
- [ ] Sales & Reports fully interactive (incl geographic map).
- [ ] Food Cost & Profit fully interactive.
- [ ] Date/branch/category filters tested across all relevant pages.
- [ ] 8 Overview KPI display from functions; each has tooltip/formula.
- [ ] ≥4 automated rules real triggers.
- [ ] State, export, loading, empty states and errors tested.

## Gate 5 — Human-visible quality and evidence

- [ ] Screenshot all six pages at 1366×768.
- [ ] No KPI overflow, axis clipping, overlapping cards, missing metadata.
- [ ] Four good UI principles measured/documented.
- [ ] Prototype v1 user testing recorded **from actual participants**.
- [ ] Feedback incorporated into v2; retest recorded.
- [ ] Performance benchmark measured not guessed.
- [ ] Screenshot manifest records data seed, filters, app version.

## Gate 6 — Handoff & final assignment readiness

- [ ] README installation and full CLI verified.
- [ ] Data dictionary, metrics dictionary, ERD, PB chart registry in repository.
- [ ] Tests, outputs, logs, design screenshots stored and cited.
- [ ] Report evidence for Bab I–IX mapped; actual report not fabricated.
- [ ] AI usage notes and originality declaration prepared.
- [ ] Demo storyboard 3–5 minutes ready with real app.
- [ ] All major blockers and remaining risks listed.

## Final Stop / Go

**Siap demo:** data, analitik, visual, dan aplikasi lulus pemeriksaan teknis. **Siap dikumpulkan:** dua putaran uji tercatat dan seluruh berkas pada checklist dosen telah tersedia.  
**STOP:** discrepancy in revenue/cost/stocks; required chart/page missing; tests not run while claimed passed; stale filter; misleading source; copyrighted sample copied.
