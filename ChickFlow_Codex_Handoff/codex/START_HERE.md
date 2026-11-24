# START HERE — Codex one-shot instruction to implement ChickFlow end-to-end

> Paste the **prompt below** into Codex **after putting this entire package in your working repo**, or attach `CHICKFLOW_ALL_IN_ONE.md` plus `codex/AGENTS.md`. Do not attach only a dashboard image and ask Codex to clone it. This is a functional project, not a mockup exercise.

## Main Codex prompt — copy below as one message

```text
Saya ingin kamu mengimplementasikan proyek akhir bernama CHICKFLOW dari NOL sampai siap diuji/didemokan. Semua keputusan fitur, skema data, data sintetis, formula KPI, UI, tests, dan acceptance ada pada blueprint Markdown yang saya berikan. HARAP BACA SEMUA sebelum mengubah kode.

MODE: autonomous coding agent dengan quality gates. Jangan hanya menulis rencana atau UI palsu: buat kode, dataset hasil generator, dashboard Streamlit 6 halaman, Plotly charts, static EDA, tests, documentation, dan evidence yang benar-benar bisa dijalankan. Fokus dulu pada deliverable aplikasi dan bukti; jangan menulis laporan akademik final sebelum data & tests nyata.

REFERENCES & PRIORITY:
1) README.md serta docs/01–15 dan checklists/* pada paket ChickFlow adalah source of truth produk.
2) Template Laporan Proyek Akhir Visualisasi Data adalah sumber minimum tugas. RPS yang lebih lama hanya referensi pembelajaran (ada beda kode mata kuliah).
3) ZIP contoh Restora/gambar dashboard TIDAK BOLEH menjadi acuan desain/fitur/data, TIDAK BOLEH DICLONE. Identitas ChickFlow harus orisinal Ops Control Room navy–amber.
4) Ikuti AGENTS.md dan versi API resmi yang tersedia di environment.

SCOPE LOCKED:
- Brand ChickFlow, quick-service fried-chicken chain sintetik, 3 cabang kota simulasi Sumatra Barat.
- Halaman persis 6: Overview, Orders, Kitchen Performance, Inventory, Sales & Reports, Food Cost & Profit.
- 30 hari data (Oktober 2026), target 3.600 order, 9 relational tables, 24 menu SKUs dan 27 ingredients di docs/15, BOM untuk food cost dan inventory usage.
- Libraries wajib: pandas, numpy, matplotlib, seaborn, plotly. UI Streamlit; Plotly interactive, `px.scatter_map` jika kompatibel.
- Filters global date, branch, category (lihat doc10 untuk applicability) dan ≥8 KPI utama/≥6 rule-based insights sebagai target.
- ≥2 qualitative visuals (real feedback word cloud + order workflow), ≥5 quantitative (line, bar, histogram, scatter, boxplot) dan ≥1 geographic point map.
- Net revenue = line gross minus allocated discount once; food gross profit = net revenue - direct food/packaging COGS, NOT net profit accounting; inventory ending as-of cumulative ledger; canceled orders do not count sales/usage; no double counting of orders.
- Strict test gates; 2 prototype feedback cycles at the v1 and v2 milestones must be based on actual user input, not made up. If actual respondents unavailable, provide instruments/templates and mark PENDING rather than fabricate results.

EXECUTION ORDER:
P0 foundation -> P1 master/reference data/BOM -> P2 deterministic generator+cleaning+validator+EDA -> P3 pure facts/KPI/filter/rules -> P4 chart builders -> P5 Streamlit shell/design/components -> P6 six complete pages -> P7 automated/manual tests, evidence and code cleanup -> P8 README/reproducibility/demo/report evidence preparation.

For EACH phase:
- Implement source files and tests, do not merely outline.
- Run relevant commands, inspect outputs, fix failing issues.
- Report actual changed files, commands, test pass/fail/skip, data counts, recon totals, evidence paths and unresolved blockers.
- Do not proceed to UI stages until data reconciliation and metric tests PASS. Do not claim PASSED if tests did not run.
- Maintain a PROJECT_STATUS.md checklist (task IDs CF-###) and docs/decision_log.md. Update docs if implementation changes.
- If environment lacks packages/network, use pinned compatible local deps or explain blocker, do not invent results.

FIRST ACTIONS:
1. Show concise inventory of blueprint documents read and any contradictions you identified; apply the precedence stated in README.
2. Show phased task plan with nearest files/tests.
3. Start implementing Phase 0 and Phase 1 immediately in the current workspace, not just a textual plan.
4. After P0–P3, build Overview, Kitchen, Inventory, and Profit first and start the v1 test. Complete Orders and Sales and run the v2 retest. If user approval needed for destructive publication/brand changes, ask; otherwise proceed.

FINAL ACCEPTANCE:
- User can run documented setup, generate/clean/validate data, run tests, run Streamlit dashboard and access 6 useful pages.
- All financial and inventory reconciliations exact; filters correct; alerts data-driven; all required visualizations present.
- Screenshots and tests are genuine artifacts and traceable to data seed/manifest.
- Output a final checklist mapping template requirements -> implemented file -> test -> evidence -> status.
```

## Handoff file layout

- **Minimum recommended upload:** entire `ChickFlow_Codex_Handoff.zip` (includes modular docs + all-in-one markdown). Do not supply only this small prompt without the actual blueprint.
- **Single Markdown alternative:** upload `CHICKFLOW_ALL_IN_ONE.md` plus `codex/AGENTS.md`.
- **Existing repository:** copy `codex/AGENTS.md` to repo root `AGENTS.md`. Copy docs, checklists, and start prompt into a `planning/` folder; adjust relative links (content does not change).

## What NOT to accept from Codex

- Dashboard filled with hardcoded metric cards that do not change with filters.
- “6 modules” that are empty placeholders or copied screenshots.
- Orders reported from `len(order_items)`; financial metrics from duplicated order join.
- Stock recalculated from date filter start only; negative inventory silently clipped to zero.
- Menu COGS independently random instead of BOM.
- `Net Profit` label without overhead/rent/payroll.
- Only importing matplotlib/seaborn without actual static visualization outputs.
- Invented respondent feedback, fake test counts, or generated screenshots presented as real runtime captures.
- Brand/style/theme resembling Restora examples because it was easier to reproduce.
