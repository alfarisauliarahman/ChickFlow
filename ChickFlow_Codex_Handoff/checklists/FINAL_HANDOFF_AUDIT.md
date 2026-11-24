# Full Handoff Audit — What to show before saying complete

1. **Repository proof**: file tree, Python version, packages, exact setup/run commands, commit/hash.
2. **Generated dataset proof**: row counts for 9 tables, minimum transactions/date range, seed, SHA256 manifest, cleaning issue counts.
3. **Numeric proof**: gross-discount-net Rp0 delta per order; COGS/BOM exact; food GP; stock running balance nonnegative; manual fixture results.
4. **Visual proof**: screenshots of six pages from actual Streamlit; no copied sample and no placeholder hardcoded KPI; 2 qual + at least 5 quant + 1 geo; matplotlib/seaborn/Plotly evidence.
5. **Filter proof**: one category with multi-line order, one branch, one date, empty data, inventory as-of start-date invariant, category N/A stock note.
6. **Insight proof**: rule results with actual value, threshold, n, context, action, unit tests of threshold boundary.
7. **UX proof**: 1366×768 + 768px screenshots, contrast, keyboard and loading/error/empty states.
8. **Prototype proof**: v1 issues → v2 changes → retest; if no user tests, **pending** not invented.
9. **Academic proof**: traceability table TR-01..59, PB mapping, code/library comparison, references, report materials.
10. **Limitations**: synthetic data, simplified recipe/stock model, three representative map coordinates, 30-day history, gross food profit not full accounting profit.

**Single success criterion:** Someone with a clean machine can follow README, reproduce dataset and test suite, inspect all 6 pages, independently recompute critical figures, and get the same results without copying any Restora visual template.
