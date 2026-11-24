# 11 — Test plan, fixtures, QA, usability, performance, and acceptance

## 11.1 Testing strategy

**Test pyramid:** (1) pure unit tests: data quality, formula, filtering, rule boundaries; (2) integration tests: generated dataset → marts → six pages; (3) UI smoke: Streamlit `AppTest` where supported; (4) manual/e2e browser walkthrough, screenshot, accessibility/performance; (5) prototype feedback two iterations.

Acceptance cannot be replaced by “berhasil import semua library” or “angka di UI muncul”. Unit tests **nominal Rp0 difference** mandatory.

## 11.2 Dataset test cases (D)

| ID | Test | Expected |
|---|---|---|
| D-01 | 3 branches count | ==3, unique geolocation labels |
| D-02 | completed orders/date coverage | >=500 complete, >=7 unique dates |
| D-03 | all PK/unique composite | 0 duplicate after cleaning |
| D-04 | all foreign keys | 0 orphans |
| D-05 | order status+payment mapping | only allowed pairs |
| D-06 | eligible completed with item | >=1 item each |
| D-07 | cancelled with item | 0 line for cancelled v1 |
| D-08 | currency integer fields | all integer and >=0 except GP allowed negative |
| D-09 | gross, discount, net per order | exact IDR equality |
| D-10 | category totals vs total revenue | exact equality |
| D-11 | food cost source | consistent with recipe snapshot rounding |
| D-12 | kitchen chronology | ordered <= ready <= completed |
| D-13 | prep time derived | timestamp diff ≤1 sec |
| D-14 | delayed flag | matches channel SLA and strict > |
| D-15 | all ingredients have policy per branch | 100% expected pairs |
| D-16 | usage events match BOM | exact at unit precision |
| D-17 | ending stock and every running balance | ≥0 |
| D-18 | feedback rating/order relation | 1..5, completed order FK, no duplicate order |
| D-19 | data issue log | injected issues cleaned, count documented |
| D-20 | repeat generate twice same seed | clean normalized CSV hashes equal |
| D-21 | date filtering boundary | end inclusive in local day, midnight correct |
| D-22 | no source file writes by dashboard | read-only application |

## 11.3 Metric/filter test cases (M)

| ID | Case | Expected |
|---|---|---|
| M-01 | fixture gross35k discount3.5k | net31.5k exact |
| M-02 | fixture revenue31.5k COGS13k | food GP18.5k, margin58.730158…% |
| M-03 | 3 lines same order | count1, not 3 |
| M-04 | filter category beverage | only beverage net, distinct order count |
| M-05 | combined category + branch | both applied at correct grain |
| M-06 | time window date inclusivity | both boundary days counted |
| M-07 | average prep excludes canceled | no null-as-zero |
| M-08 | SLA equality vs greater | equality on-time, greater delayed |
| M-09 | group delayed percentage | ratio of sum numerators to denominators |
| M-10 | margin with zero revenue | N/A; no ZeroDivisionError |
| M-11 | no eligible records | revenue0, orders0, mean N/A |
| M-12 | inventory opening50 receipt20 usage35 waste2 | ending33 |
| M-13 | inventory as-of 20 Oct with start19 Oct | includes events since opening |
| M-14 | inventory category selected | ending stock unchanged, UI N/A note |
| M-15 | waste not double-counted into food GP | no duplicate deduction |
| M-16 | 30-day range prior-period incomplete | delta N/A |
| M-17 | price snapshot change | historic revenue unchanged |
| M-18 | category-branch revenue totals sum | equal global total in same scope |
| M-19 | time zone on another system | WIB daily bins unchanged |
| M-20 | one selected branch | chart and KPI match subset |

## 11.4 Rule-engine boundaries (R)

| ID | Input | Expected |
|---|---|---|
| R-01 | late rate =10% n≥20 | no A01 (strict >) |
| R-02 | late rate =15% n20 | A01 on |
| R-03 | late rate =25% n<20 | `not_evaluable`, not A01 |
| R-04 | menu margin24.9%, units10 | A02 on |
| R-05 | menu margin24.9%, units9 | A02 off |
| R-06 | stock9, reorder10 | A03 on |
| R-07 | stock10, reorder10 | A03 off |
| R-08 | daily sales84% prior7d mean | A04 on if n7 daily baselines |
| R-09 | daily sales84%, prior6 days | A04 not_evaluable |
| R-10 | food gross margin exactly30% | A05 off |
| R-11 | ratio P90 >1.4, n≥20 | A06 on |
| R-12 | n no data | no fake green success |
| R-13 | filters change | alerts recompute, scope correct |
| R-14 | multiple issues | max 4 visible, order severity |

## 11.5 UI scenarios (U)

| ID | Action | Expected |
|---|---|---|
| U-01 | open app | six nav pages accessible |
| U-02 | toggle date filter | relevant KPI+charts update |
| U-03 | select branch | scoped data, no other branch in branch table |
| U-04 | select category | category sales only, unique orders, inventory N/A label |
| U-05 | reset filters | return default last 7 days |
| U-06 | navigate six pages | no uncaught exception, preserved filter state |
| U-07 | zero record filter | explanatory empty state |
| U-08 | corrupt CSV | visible diagnostic, no fake KPI |
| U-09 | no network / map tiles | fallback still communicates geographic position |
| U-10 | tooltip and chart labels | no missing units, clear source/scope |
| U-11 | download filtered CSV | matches visible aggregation |
| U-12 | alert CTA click | opens correct target module/context |
| U-13 | missing review text | word cloud skip null and show table |
| U-14 | single selected branch/channel | no chart crash |
| U-15 | keyboard controls / color | keyboard navigable, contrast target |
| U-16 | 1366×768 viewport | labels/cards not clipped, action visible |
| U-17 | 768px viewport | columns wrap, no overlapping content |
| U-18 | repeated page switches | no materially stale data/cache |

## 11.6 Integration and operational tests

- Generate + clean + validate + marts + static EDA + run all metric tests in **clean checkout**.
- Verify **unit tests pass from repo root** and `pip install -e .` works in clean environment.
- `streamlit run app/main.py` starts and routes all pages; startup logs show loaded manifest and seed.
- Fresh checkout with no `data/clean` should fail gracefully and say how to generate sample data; optional bootstrap dataset is allowed, but explicit and documented.
- Browser E2E (if time): Playwright Chromium screenshot per page, filter selection, alert navigation, empty state. `AppTest` can test Streamlit session widgets but not guarantee exact Plotly hover behavior; manual browser QA remains necessary.
- Screenshot artifact should be **captured from actual running app**, not generative mockup presented as finished product.

## 11.7 Usability tests — two prototype cycles required for rubric

### Cycle 1: prototype v1 setelah data dan tiga alur siap

- Recruit target 5 respondents if possible (may be classmates acting as manager/owner/inventory personas), record number and roles truthfully.
- Three tasks: (A) find branch with highest late rate; (B) identify menu with low food margin; (C) identify critical stock as-of date.
- Three-second test: show screenshot first fold for 3 seconds, ask most important action/info. Count respondents who identify.
- Task success, time-on-task, misclick count, major confusion (qualitative feedback), 1–5 satisfaction survey.
- Save `reports/prototype_v1/feedback.csv`, `screenshots/`, and issue log.

### Cycle 2: revised dashboard v2

- Prioritize and fix documented UX issues, rerun the same tasks with respondents, and preserve before/after screenshots.
- Log `issue → evidence → change → retest result`; no fabricated scores.
- One example possible change (not pre-stated as fact): `Users overlooked active branch filter → moved filter chips near title → retest.`

## 11.8 Accessibility checks

- Standard contrast for normal text target 4.5:1; large text >=3:1 WCAG AA style.
- Keyboard navigate page, filter, buttons, expander; check focus indicator visible.
- Alert states have textual labels `Kritis/Peringatan/Info`, not only green/red colors.
- Every important chart has concise accessible description and companion summary/table if needed.
- No flashing animations; charts don't require mouse-only hover for all information.
- `st.plotly_chart` optional `alt` supported when available in pinned version; verify official API.

## 11.9 Performance plan

**Target tentative, not claimed results**: with 3.600 orders and tens of thousands inventory events, cold-load target <5 sec, cached page switch/filter p95 target <3 sec on testing laptop. Benchmark exact hardware/OS/browser, event count, cold/warm start and 5 repeat runs. Use `time.perf_counter` for backend ops (load bundle, compute KPIs, generate charts); UI timing via browser manual or automation. If target fails, profile joins/cache, avoid prebuilding all 15 figures on one page.

## 11.10 Release gates

**G1 Foundation:** install/test/lint smoke passes.  
**G2 Data:** D-01..D-22 passes.  
**G3 Metrics:** M-01..M-20, R-01..R-14 passes.  
**G4 Visual:** 2 qualitative/5 quantitative/1 geo, 5 library evidence, chart correctness screenshots.  
**G5 App:** six modules U-01..U-18 pass (or documented skip with reason + manual alternative).  
**G6 Academic:** template mapping complete, two prototype cycles documented, report evidence archived, 3–5 min demo can run.  
**G7 Final:** no blocker, defects prioritized, README exact clean install command, reproducible repo.

**Rule:** if quantitative gate fails, do not hide it by improving visual cosmetics. All skipped automated tests must be documented honestly with manual substitute or open risk.
