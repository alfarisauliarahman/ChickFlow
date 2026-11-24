# Requirement Traceability Matrix — TEMPLATE → ChickFlow → Acceptance → Evidence

**Source:** user-provided `Template Laporan Proyek Akhir Visualisasi Data.docx` (task-specific). `RPS 25 VISUALISASI DATA ok(1).pdf` is an older RPS reference; it has a different course code, so do not replace specific assignment requirements with that administrative metadata. ZIP Restora contents are examples only.

| ID | Template requirement / chapter | ChickFlow implementation | Test/gate | Deliverable evidence |
|---|---|---|---|---|
| TR-01 | Individu, brand sendiri | ChickFlow original with own logo/tokens | visual audit | brand asset, logo license, README |
| TR-02 | ≥6 allowed modules | Overview, Orders, Kitchen, Inventory, Sales, Food Cost & Profit | U-01/U-06 | 6 real screenshots |
| TR-03 | synthetic ≥500 transactions | target 3,600 order | D-02 | raw/clean orders, manifest |
| TR-04 | ≥7 days | fixed 30-day window | D-02/D-21 | date range in manifest |
| TR-05 | ≥3 relational tables | 9 normalized tables | D-03/D-04 | ERD + data dictionary |
| TR-06 | ≥2 qualitative visuals | word cloud, order process flowchart | Gate P4 | V-L01, V-L02 images |
| TR-07 | ≥5 quantitative | line, bar, histogram, scatter, box plot (+heatmap etc) | Gate P4 | V-Q01..V-Q12 registry |
| TR-08 | ≥1 geographical | Plotly fictional branch map | U-09/Gate P4 | V-G01 screenshot |
| TR-09 | Interactive Plotly | charts across 6 pages | U-10 | screenshots + runtime |
| TR-10 | ≥3 filters | date / branch / category | U-02/U-03/U-04 | UI filters & tests |
| TR-11 | ≥6 KPIs | target Overview K01..K08 | M-01..M-20 | KPI dictionary & UI |
| TR-12 | ≥4 auto rules | A01..A06 pure rule engine | R-01..R-14 | alert fixtures & UI |
| TR-13 | pandas | cleaning, joins, metrics | D/M suites | import and code evidence |
| TR-14 | numpy | seeded RNG, statistics | D-20 | generator code + seed |
| TR-15 | matplotlib | static EDA revenue/bar charts | CF-032 | reports/eda PNG |
| TR-16 | seaborn | static dist/box plots | CF-032 | reports/eda PNG |
| TR-17 | plotly | interactive core + geo | Gate P4 | graph builders + UI |
| TR-18 | RPL Prototype methodology | v1 feedback → corrections → v2 | CF-123..125 | prototype versions/change log |
| TR-19 | Good UI four principles | hierarchy, consistency, feedback, accessibility | U-15/U-16/CF-126 | UI evaluation report |
| TR-20 | justify every tech decision | ADR tradeoffs | doc09/14 | architecture decision log |
| TR-21 | visuals numbered and captioned | V-IDs and screenshot captions | docs registry | report evidence matrix |
| TR-22 | APA/IEEE refs | ≥8 sources actual consulted | CF-145/149 | bibliography later |
| TR-23 | Bab I brand identity | docs 01/08/15 | CF-003/005 | profile/brand |
| TR-24 | Bab I ≥5 evidenced problems | PB hypotheses and computed baseline | after P3 | evidence actual numbers |
| TR-25 | Bab I objectives+success targets | docs 01/02/05 | M/R suites | target and actual |
| TR-26 | Bab I stakeholders | 4 roles | doc02 | persona matrix |
| TR-27 | Bab I ≥10 PB | 15 PB | V registry mapping | PB matrix |
| TR-28 | Bab I KPI definitions leading/lagging | K01..K18 and leading/lagging | doc05 | metric dictionary |
| TR-29 | Bab I ≥4 business rules | 6 rules | R suite | rule register |
| TR-30 | Bab II Prototype-RPL-CRISP-DM mapping | roadmap phase mappings | CF-123..125 | change history |
| TR-31 | Bab III ≥2 personas | 4 personas | doc02 | user stories |
| TR-32 | Bab III FR, NFR | FR-01..20, NFR-01..11 | U/test | requirements matrix |
| TR-33 | Bab III Use case + process diagram | roles, V-L02 | Gate P4 | SVG/PNG diagram |
| TR-34 | Bab IV generator method+seed | configuration & RNG | D-20 | simulation.yaml + log |
| TR-35 | Bab IV ERD and dictionary | 9 tables and field contracts | D-03..04 | docs/data_dictionary.md |
| TR-36 | Bab IV EDA `info`, `describe` | pandas EDA | CF-032 | text + visual evidence |
| TR-37 | Bab IV cleaning log before/after | controlled injected problems | D-19 | reports/data_quality.json |
| TR-38 | Bab IV derived metrics | margin, late, inventory | M suite | formula code+fixtures |
| TR-39 | Bab V sitemap+user flow | six page architecture | U-01 | sitemap diagram |
| TR-40 | Bab V low-fi and high-fi mockup | ASCII/Figma + real app screenshots | CF-123..125 | before/after assets |
| TR-41 | Bab V design tokens | original navy/amber tokens | CF-005/087 | design_system.md |
| TR-42 | Bab V chart type rationale | `V` registry 15 charts | Gate P4 | PB→V table |
| TR-43 | Bab V interaction | tooltips, filter, drill-down | U suite | UI screenshot/test |
| TR-44 | Bab VI framework comparison | Plotly/Matplotlib/Seaborn tradeoffs | doc09 | ADR + version list |
| TR-45 | Bab VI folder structure | architecture tree | CF-001 | repo structure screenshot |
| TR-46 | Bab VI screenshot each page | six images | CF-143 | screenshot manifest |
| TR-47 | Bab VI running/deploy instructions | README | CF-140..147 | reproducible run |
| TR-48 | Bab VII functional tests | D/M/R/U test plan | P7 | actual test outputs |
| TR-49 | Bab VII manual KPI validation | FIX01/02/05 etc | M suite | fixtures + manual compare |
| TR-50 | Bab VII UI four-principle test | WCAG/3-second/consistency etc | CF-126 | audit results |
| TR-51 | Bab VII two iteration feedback | v1/v2 actual respondents | CF-123..125 | feedback.csv, change log |
| TR-52 | Bab VII performance | measured cold/warm durations | CF-127 | benchmark results |
| TR-53 | Bab VIII PB interpretations | all 15 PB with output values | CF-145 | PB answer evidence |
| TR-54 | Bab IX conclusions/limitations | compare targets, state synthetic | CF-149 | report final later |
| TR-55 | Deliverables PDF report | later, not yet generated | P8 | report.pdf |
| TR-56 | Deliverables Github repo | cleaned code/data/README | CF-146 | valid repository URL |
| TR-57 | Deliverables 3–5 min demo | storyboard with actual app | CF-148 | demo video |
| TR-58 | Deliverables presentation | slide outline → pptx later | CF-149 | presentation |
| TR-59 | Originality and AI disclosure | honest AI use log | CF-145 | Lampiran D |

## Requirement status lifecycle

Each TR row is initially **PLANNED**. During implementation set **IMPLEMENTED**, then **TESTED**, and finally **EVIDENCED** when there is a real file/screenshot/repro command. Do not mark **DONE** based solely on this planning document. In report, mark missing items honestly with blocked reason, not fabricated evidence.

## Main grading emphasis from template rubric (planning priority)

1. Visualization qualitative/quantitative/geographic **25%** — fulfill and justify chart families, labels, no chart junk.
2. Interactive dashboard **20%** — six useful modules, KPI, filters and automated insight.
3. Data processing **15%** — cleaning log, derived metrics and validation.
4. Business understanding **10%** — problems backed by numbers, objectives, KPIs, questions.
5. RPL process **10%** — prototype feedback cycles and documentation.
6. Good UI design **10%** — evidence four principles.
7. Tools/framework discussion **5%**, presentation/demo/Q&A **5%**.

**Numerical rubric is from task template**, not a guarantee of grade. Focus on proof that each criterion is truly met.
