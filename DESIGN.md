# ChickFlow design

ChickFlow is a historical analytics dashboard for a fictional fast-food chicken chain in West Sumatra. The manager reads it during a shift review. The kitchen lead, inventory officer, and owner use the detail pages to check the evidence behind an alert.

## Current FigCraft prototype

[ChickFlow Prototype](reports/design/ChickFlow-Prototype.figcraft) is the single editable FigCraft source. The desktop flow starts at Overview. It contains six main screens, one board with six wireframes, three filter examples, three detail screens, and a mobile Overview.

### Direction

A historical operations dashboard for a fast-casual restaurant manager, using the visual language of menu boards and printed shift summaries. Energy 2, Rhythm 3, Motion 1. Avenir Next Bold sets page titles. Demi Bold marks KPI values, section headings and controls. Regular supports table text and axis labels. Tabular figures help readers scan columns of money and counts.

| Use | Color | Reason |
|---|---|---|
| Workspace and table rows | `#F5F5F2` | A near-white ground for reviewing data during a shift |
| Cards, filters and navigation | `#FFFFFF` | Separates controls and dense figures from the work surface |
| Body and secondary text | `#262624` and `#53534D` | Measured contrast against the workspace is 13.88:1 and 7.09:1 |
| Action and selected navigation | `#963C32` | Muted brick picks up the color of the serving tray and marks the current action |
| Positive comparisons and secondary series | `#35695E` | Distinguishes supporting measures by hue and label |

Overview puts the shift findings next to the revenue series. Orders centers the transactions table. Kitchen opens with branch box plots and the SLA denominator. Inventory starts with the critical stock balance against its reorder point. Sales pairs the revenue series with branch geography. Profit puts the calculation before the margin scatter and opens to a separate recipe detail. The mobile Overview stacks the same decision fields.

Interface labels use direct Indonesian. Use `Pesanan terlambat` for the SLA measure and explain the channel-specific time limit on the kitchen screen. Use `Laba kotor makanan` for Food Gross Profit and `Biaya bahan dan kemasan` for Food COGS. Detail actions say what opens, such as `Cek stok`, `Cek dapur`, and `Cek margin`.

### Template and planning checks

- §5.2 of the lecturer's Word template is covered by the six wireframes and six editable high-fidelity screens. Navigation, KPI, main visual, insight, and primary action are named on the wireframe board.
- The desktop prototype includes the eight planned Overview KPIs and the three global filter controls. The controls navigate to labeled, precomputed examples. The Streamlit app computes filters from data.
- The screens use the planned transaction table, weekday/hour heatmap, prep histogram and box plot, restock ratio, geographic markers, margin scatter, order workflow and review word cloud. The app and its screenshot evidence cover §6.6.

### New references

- [Birdcall by PARDNER](https://www.pardner.studio/work/birdcall) and [Sweet Chick by Saint Urbain](https://www.sainturbain.com/work/sweet-chick/) informed the contrast between condensed restaurant display type and readable information text.
- [Tender Greens by Pentagram](https://www.pentagram.com/work/tender-greens/story) informed using a food photograph in a brand surface. [Toast Recipe View](https://support.toasttab.com/en/article/Recipe-View-on-Kitchen-Display-Systems-KDS?lang=en_US) informed placing the item image next to its recipe and cost.
- The Sales map shows representative points for fictional branches. The provincial outline is derived from geoBoundaries gbOpen IDN ADM1, OpenStreetMap and Wambacher sources, Open Database License 1.0. The map clips the outline to the area around the three points. [Dataset and attribution metadata](https://www.geoboundaries.org/api/current/gbOpen/IDN/ADM1/)

### Image provenance

Two original illustrative photographs are embedded in the FigCraft file. The files below were made with the built-in ImageGen tool. Neither photograph is evidence of a real store or sale.

- [ChickFlow serving tray](assets/brand/chickflow-serving-tray.png). Prompt: Use case: product-mockup. A single wide editorial overhead photograph for an Indonesian fast-casual fried-chicken restaurant analytics interface. At the right, an unbranded deep brick-red serving tray with three crisp golden ayam goreng pieces, a plain ivory carton and a small dark-red sambal cup. On the left only a warm ivory stainless-prep-counter backdrop, clean and quiet. Slight diagonal daylight, real handmade food texture, dark sour cherry #821F2F and warm off-white #F8F3EA palette, minimal composition, styled like contemporary restaurant packaging case-study photography. Landscape crop, subject primarily centered at x72%. No visible text, no logos, no checkered pattern, no watermark.
- [Family Feast Box](assets/brand/chickflow-family-feast.png). Composition prompt: Use case: product-mockup. Realistic original menu photograph of ChickFlow Family Feast Box, an Indonesian fried chicken combo: exactly four golden fried chicken portions in one plain kraft takeout tray, two individual small fries portions in undyed parchment cups, and three clear iced tea cups visible together. Overhead layout on matte dusty pale rose tabletop, plate and all seven side/drink containers clearly separated in the one compact arrangement, balanced framing with generous crop-safe margins. Hard directional editorial daylight from top-left, controlled shadows, exact product texture, warm cream and dark cherry color art direction. Landscape composition, no words, no logo, no people, no watermark. Final edit prompt: Use case: precise-object-edit. This input is the approved content composition for ChickFlow Family Feast Box, four fried chicken pieces in plain cardboard, two fries portions and three iced teas. Change only the dusty pink tabletop/substrate to a natural off-white commercial preparation counter, warm-toned light ivory gray, with original physically consistent shadows. Preserve the exact dish arrangement and counts, food shapes, earthy packaging, focus, framing, and realism. Remove all noticeable pink or red in the countertop. Slightly lower overall food saturation toward natural fried golden hues. No text or logo.

## Streamlit implementation

The application carries this palette, type scale, Indonesian labels, and top navigation into the six working pages. It loads the serving tray and recipe images from `assets/brand/`. Real date, branch, and menu filters persist across pages. Alert links lead to the related module, and the order, stock, and recipe detail controls use the filtered data. The offline map draws the local provincial outline and labels the three fictional branches.

The following notes document the initial dark-theme design exploration.

## Identity and visual direction

**Ops Control Room.** Deep navy surfaces keep the analytics workspace comfortable during a longer review. Warm amber draws attention to sales and the highest-priority action. Cool blue identifies preparation data. Status colors carry labels such as Kritis and Peringatan. The original ChickFlow mark uses three angled strokes that suggest a wing in motion. The mark belongs in the navigation and on report covers.

**Energy 2 · Rhythm 3 · Motion 1.** The amber signal and large analytical headline give the dashboard a clear first read. Overview pairs a wide trend with a short list of operational issues. Kitchen emphasizes distributions. Inventory opens with a full-width stock table. Motion is limited to native control feedback and respects reduced-motion settings.

## Visual vocabulary

| Role | Token | Use |
|---|---|---|
| Canvas | `#0B1220` | Main analytical workspace |
| Navigation | `#111C2E` | Persistent navigation and filter controls |
| Panel | `#17263C` | Charts and tables that belong together |
| Border | `#2C4161` | Subtle panel separation |
| Text | `#F8FAFC` | Headlines and values |
| Secondary text | `#C7D2E0` | Supporting labels and axis text |
| Amber | `#F5B301` | Revenue, primary focus, and active control accent |
| Blue | `#60A5FA` | Kitchen duration and comparison series |
| Mint / rose | `#34D399` / `#FB7185` | Health and critical markers with text |
| Focus | `#F5B301` | Visible control outline on navy |

Use Inter with system sans-serif fallback. Its clear numerals fit side-by-side currency and rate comparisons. Use tabular numerals for KPI values and right-align numeric table columns. Headline 30–36px, section heading 18–22px, labels 14px, supporting text 13px. The spacing scale is 4, 8, 12, 16, 24, and 32px. Controls have 6px corners and chart panels 10px. Dark navy text on filled amber controls maintains readability.

Categorical colors stay consistent across pages, with a restrained navy/amber/blue application palette. Use color plus text, marker shape, line dash, or position whenever a distinction is needed. Use a sequential scale for the order heatmap and a separate muted treatment for dates outside coverage.

## Navigation and global context

Group pages by the decisions they support. Overview stands alone, followed by Orders and Kitchen, then Inventory, Sales, and Profit. Active navigation has a visual marker and a text-weight change. Streamlit's collapsible navigation remains reachable on narrow screens. Label controls `Tanggal`, `Cabang`, and `Kategori menu`. Keep the selected scope visible at each page heading and preserve it across navigation. Display `Data sintetis` alongside the date range. A filter that does not apply to a metric appears in the metric's help or nearby text.

At laptop widths show a primary chart next to a supporting chart only where their comparison helps. At tablet widths make each primary view full width and use two KPI columns. At phone widths open navigation on demand, stack plots, and keep horizontal scroll inside detail tables. A 44px control row supports touch. Every key chart has a readable table or clear text equivalent where its values affect a decision.

## Page hierarchy

| Page | First read | Supporting evidence and action |
|---|---|---|
| Overview | Net sales trend and the highest-priority operational issue | Eight metrics, branch comparison, links to the affected module |
| Orders | Weekday-by-hour demand intensity | Channel AOV, searchable orders, workflow and customer review themes |
| Kitchen Performance | Delay rate by branch and channel, with the numerator and denominator | Prep histogram, branch box plot, channel filter, service-time audit |
| Inventory | Critical stock table ordered by shortage against the reorder point | Cutoff date, physical stock, waste cost, ingredient movement detail |
| Sales & Reports | Daily net sales and menu units | Branch revenue and optional basemap, category contribution, filtered export |
| Food Cost & Profit | Menu popularity versus food margin | Gross-to-net reconciliation, category contribution, recipe cost detail |

Charts use a question or a concrete analytical title, visible units, meaningful hover fields, and a defined denominator. On active category filters, show `Omzet kategori per pesanan`. Inventory explicitly shows the end-date balance and lists movement totals within the selected period separately. The default seven-day window is anchored to the dataset end date.

## States and evidence

A missing dataset gives the generator command. A valid filter with no matching orders offers a reset and leaves inventory alerts available when the ledger supports them. Loading identifies the dataset. Charts for rates show a dash when their denominator is zero. In a disconnected demo, the map keeps the city labels and metric details on the offline base.

Prepare a low-fidelity wireframe and a high-fidelity mockup for each of the six pages. Label both as design artifacts, with the implementation evidence captured separately from the running app. Check legibility at 1366×768 and 768px, narrow-screen reflow, keyboard focus, filtered export, and the three prototype tasks.

## References and design decisions

| Reference | Decision for ChickFlow |
|---|---|
| [Toast Sales Summary](https://support.toasttab.com/en/article/Sales-Summary-Report) | Keep date scope next to net sales and provide day/hour detail below the summary. |
| [Toast Weekly Overview](https://support.toasttab.com/en/article/How-to-Use-the-Toast-Reporting-Dashboard) | Use a short repeatable review window and explain the transaction definition. |
| [Toast Restaurant Reporting visuals](https://pos.toasttab.com/products/reporting) | Elevate a small set of sales figures in the narrow layout and expose the breakdown on scroll. |
| [Toast Menu Reports](https://support.toasttab.com/en/article/Menu-Report-Overview-1492794696577?lang=en_US) | Pair menu ranking with units, gross, discount, and net amounts. |
| [Square Restaurant Performance Reports](https://squareup.com/help/us/en/article/6433-reporting-with-square-for-restaurants) | Give kitchen measurements a dedicated page and show the population they cover. |
| [Square Reporting Views](https://developer.squareup.com/docs/reporting-api/views) | Keep order-level service measures and item-level sales measures distinct. |
| [Lightspeed Back Office Reports](https://o-series-support.lightspeedhq.com/hc/en-us/articles/31329355994523-Accessing-Back-Office-Reports) | Separate hourly demand, item ranking, stock, and sales history into task-focused views. |
| [Lightspeed MarginEdge visual](https://www.lightspeedhq.com/integrations/marginedge/) | Place numeric comparisons in aligned columns and tie margin analysis to its components. |
| [Shopify Analytics overview](https://help.shopify.com/en/manual/reports-and-analytics/shopify-reports/overview-dashboard/using-the-overview-dashboard) | Make the selected date range and scope obvious before comparing metrics. |
| [Grafana dashboard guidance](https://grafana.com/docs/grafana/latest/visualizations/dashboards/build-dashboards/best-practices/) | Put higher-level signals first and link to diagnostic detail. |
| [Grafana heatmaps](https://grafana.com/docs/grafana/latest/visualizations/panels-visualizations/visualizations/heatmap/) | Use a fixed legend and expose the count behind each heatmap cell. |
| [ONS dashboard guidance](https://service-manual.ons.gov.uk/data-visualisation/guidance/dashboards) | Pick the audience decisions first and prioritize only the content that supports them. |
| [Government Analysis Function dashboard guidance](https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-building-and-managing-dashboards/) | Plan for accessible alternatives and actual user testing. |
| [IBM Carbon color foundations](https://www.carbondesignsystem.com/building-blocks/foundations/color/overview) | Give interface and status colors consistent semantic roles. |
| [Datawrapper line chart guidance](https://www.datawrapper.de/blog/line-charts) | Keep time-series labels and context close to the data and avoid competing lines. |
| [Datawrapper color-vision guidance](https://www.datawrapper.de/blog/colorblindness-part2) | Add position, text, or line style to reinforce color-coded differences. |
| [Datawrapper map types](https://www.datawrapper.de/docs/maps-you-can-create-with-datawrapper) | Use point markers for the three representative cities. |
| [Wilke, Fundamentals of Data Visualization](https://clauswilke.com/dataviz/) | Use position for ranking and a box plot plus histogram for prep distributions. |
| [W3C contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) | Check text pairings at 4.5:1 for normal text and 3:1 for large text. |

The visual references inform information hierarchy and chart behavior. ChickFlow's logo, layout, and assets are created for this project. The original handoff details are in [the design system](ChickFlow_Codex_Handoff/docs/08_DESIGN_SYSTEM.md).
