# AGENTS.md — ChickFlow implementation guardrails

You are coding **ChickFlow**, a synthetic fast-food chicken restaurant analytics dashboard for an individual data-visualization project. **Do not substitute the ZIP's Restora example or the SeoulGrill AYCE concept.** These are NOT templates for ChickFlow. Read `README.md`, `docs/01`–`docs/15`, `checklists/*`, and `codex/START_HERE.md` before writing production code.

## Sources of truth, in priority order

1. Assignment template: minimum criteria and academic evidence.
2. ChickFlow blueprint package: product-specific functional/data/design contracts.
3. Older RPS: curriculum outcomes, not replacement for task-specific requirements.
4. Official library docs: exact syntax supported by tested installed versions.
5. Restora/example images: only background learning, **never copy**.

## Non-negotiables

- Exactly six official pages: Overview, Orders, Kitchen Performance, Inventory, Sales & Reports, Food Cost & Profit. Do not rename/drop one without approval.
- Original ChickFlow brand and Ops Control Room visual identity. Do not copy sample colors/layout/branding.
- Three simulated branch cities, 30 days, target 3600 orders, 9 relational tables, menu/ingredient/BOM catalog source doc15.
- All data is synthetic and reproducible; expose seed/period disclaimer. Use deterministic RNG, normalized output, no random metrics in app.
- Test accuracy first: exact gross-discount-net reconciliation; one order != multiple items; food cost from BOM; stock from all events as-of cutoff.
- Global filters date, branch, category with doc10 semantics. Don't apply category to physical stock/cancellations silently.
- At least two qualitative (wordcloud+workflow), five quantitative (line/bar/hist/scatter/box), one map; five mandatory libraries actually used.
- At least 6 KPI/4 automatic rules; target 8 KPI + 6 rules. Rules show actual threshold/n and follow-ups; no fake LLM insights.
- Financial wording **Food Gross Profit**, not Net Profit. Exclude labor, rent, tax, delivery fees; waste separately labeled.
- Evidence matters: test outputs, EDA PNGs, six screenshots, prototype feedback log, report-ready artifacts.
- Never falsify user tests, sales results, test runs, benchmarks, citations, or deployment success.

## Execution discipline

- Use phase gates from `docs/12_IMPLEMENTATION_ROADMAP.md`. Implement and validate phases 0→8; don't jump ahead to decorative UI before data validation.
- Keep pure business logic in `src/chickflow/`, Streamlit presentation in `app/`.
- `pip install -e .` then `python -m chickflow.data.generate/clean/validate/build_marts`, not pseudo `src.data` modules.
- Prefer official `st.navigation/st.Page` and `px.scatter_map` backed by pinned tested versions; no deprecated `px.scatter_mapbox`.
- Keep tested commands and exact outputs in phase reviews. On failure: report real status and fix root cause, do not silently skip.
- Code and doc updates travel together. If changing recipe/threshold/field, update related tests, data dictionary and blueprint traceability.
- Do not touch unrelated user files, external accounts, remote repos, or deployment unless explicitly asked. Do not publish repo by assumption.
- Stop and ask before changing brand, module count, data source nature, tool stack, financial definitions, or sharing anything publicly.

## Definition of done for each task

1. Clear files changed.
2. Targeted test(s) executed and passed, or honest failure/block.
3. No unhandled empty/zero data paths.
4. Data/metric behavior matches related docs.
5. Comments/docs/typed public interfaces reflect reality.
6. Evidence path recorded if task requires it.
