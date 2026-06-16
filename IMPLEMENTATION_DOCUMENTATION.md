# Last Mile Logistics Auditor: Complete Implementation Documentation

## 1. Purpose of This Document

This document is the full implementation guide for the Veridi Logistics take-home project. It is written before the final analysis is executed, so it does not present final findings, rankings, or business conclusions. The purpose is to document exactly how the project will be structured and implemented before any final coding, dashboarding, or storytelling work is completed.

The assignment asks for a delivery performance audit tool that connects logistics data with customer sentiment. The business problem is that Veridi Logistics has noticed a spike in negative customer reviews. The CEO suspects that customers are not only unhappy because packages are late, but because the company is giving estimated delivery dates that are too optimistic. In other words, Veridi may be over-promising and under-delivering.

The main business question is:

> Are we failing specific regions, or is this a nationwide problem?

This implementation plan is designed to answer that question in a disciplined way. It defines the project structure, data sources, join strategy, cleaning rules, calculated metrics, visualizations, dashboard layout, presentation structure, README content, and submission checklist. The goal is to make the work reproducible, professional, and easy for reviewers to understand.

This document should be treated as the blueprint for the final build. The next phase, after reviewing and approving this plan, will be to implement the notebook, run the analysis, create the public dashboard, prepare the presentation, and update the README with final numbers and links.

## 2. Project Objective

The objective is to audit delivery promise accuracy using the Olist Brazilian E-Commerce dataset. Delivery promise accuracy means comparing the date customers were told to expect a package with the date the package actually arrived.

The project will produce three business-facing outputs:

1. A reproducible notebook that loads, joins, cleans, and analyzes the data.
2. A public dashboard that shows delivery performance by geography, delivery status, review score, and product category.
3. A concise presentation that explains the findings and recommendations.

The final submission will also include a README file at the top of the repository. That README must contain an executive summary, public project links, and a technical explanation of the cleaning and Candidate's Choice analysis.

The analysis must satisfy four required user stories:

1. Join orders, reviews, and customers into one master dataset.
2. Calculate the difference between estimated and actual delivery dates.
3. Show which customer states have the highest late-delivery percentages.
4. Compare delivery delay with customer review scores.

The bonus requirement is to translate product categories from Portuguese to English. The Candidate's Choice requirement is to add one extra business-value analysis. For this project, the Candidate's Choice analysis will be product category delivery risk.

## 3. Scope and Non-Scope

The scope of this project is delivery performance, regional failure patterns, and customer sentiment. The core analysis will focus on completed deliveries because actual delivery date is required to calculate whether the delivery promise was met.

In scope:

- Loading the Olist CSV files from the downloaded Kaggle archive.
- Building an order-level master dataset.
- Validating joins to avoid accidental duplicate rows.
- Handling missing delivery dates.
- Calculating `Days_Difference`.
- Classifying orders as `On Time`, `Late`, `Super Late`, or `Not Delivered`.
- Calculating state-level late-delivery rates.
- Comparing review scores by delivery status and delay buckets.
- Translating product categories into English.
- Creating a Candidate's Choice product category risk analysis.
- Exporting summary CSVs for dashboard creation.
- Writing final README, presentation, and submission checklist content.

Out of scope for the first version:

- Building a production data pipeline.
- Training a machine learning model.
- Creating a causal inference model.
- Predicting future late deliveries.
- Using private APIs or external databases.
- Uploading the raw dataset to the public repository.

Optional extensions may be considered later, but the first implementation should prioritize correctness and clarity over complexity.

## 4. Data Source

The dataset is the Olist Brazilian E-Commerce dataset downloaded from Kaggle. It is a relational dataset split across multiple CSV files. The local downloaded files are in the `archive/` folder.

The available files are:

| File | Rows Including Header | Purpose |
| --- | ---: | --- |
| `archive/olist_orders_dataset.csv` | 99,442 | Central order table with status and delivery dates |
| `archive/olist_order_reviews_dataset.csv` | 104,720 | Review scores and review text |
| `archive/olist_customers_dataset.csv` | 99,442 | Customer city, state, and zip prefix |
| `archive/olist_products_dataset.csv` | 32,952 | Product category and product attributes |
| `archive/olist_order_items_dataset.csv` | 112,651 | Order items, products, sellers, price, and freight |
| `archive/product_category_name_translation.csv` | 71 | Portuguese-to-English product category mapping |
| `archive/olist_sellers_dataset.csv` | 3,096 | Seller location information |
| `archive/olist_order_payments_dataset.csv` | 103,887 | Payment method and payment amount |
| `archive/olist_geolocation_dataset.csv` | 1,000,164 | Latitude and longitude by zip prefix |

Only the file inventory and column headers are used in this documentation stage. No final analytical results are calculated here.

## 5. Recommended Project Structure

The project should be organized so the raw data, notebook, documentation, outputs, and exported notebook are easy to find. The recommended structure is:

```text
amalitech/
├── archive/
│   ├── olist_orders_dataset.csv
│   ├── olist_order_reviews_dataset.csv
│   ├── olist_customers_dataset.csv
│   ├── olist_products_dataset.csv
│   ├── olist_order_items_dataset.csv
│   ├── product_category_name_translation.csv
│   ├── olist_sellers_dataset.csv
│   ├── olist_order_payments_dataset.csv
│   └── olist_geolocation_dataset.csv
├── outputs/
│   ├── state_delivery_summary.csv
│   ├── sentiment_by_delivery_status.csv
│   ├── delay_bucket_review_summary.csv
│   └── category_delivery_summary.csv
├── notebook_exports/
│   └── last_mile_logistics_audit.html
├── README(1).md
├── README.md
├── IMPLEMENTATION_DOCUMENTATION.md
├── dashboard_blueprint.md
├── presentation_outline.md
├── last_mile_logistics_audit.ipynb
├── requirements.txt
└── .gitignore
```

The `archive/` folder contains raw data and should remain local. It should not be committed to GitHub. The `outputs/` folder will contain small aggregated files that can be used to build the dashboard. The `notebook_exports/` folder will contain the executed notebook export in HTML or PDF format. The root folder will contain documentation and the notebook.

`README(1).md` is the original assignment brief. It should be preserved as a reference. `README.md` will be the final candidate-facing repository README because GitHub automatically displays a file named `README.md` on the project homepage.

## 6. Git and Submission Rules

The final repository must be public and reproducible. It must not include the raw Olist CSV files. The `.gitignore` should block the raw archive files and any large downloads.

Recommended `.gitignore` behavior:

- Ignore `archive/`
- Ignore `data/`
- Ignore raw `olist_*.csv` files
- Ignore `product_category_name_translation.csv`
- Ignore zip files
- Ignore notebook checkpoints
- Ignore Python cache folders

The final repository should include:

- `README.md`
- `last_mile_logistics_audit.ipynb`
- HTML or PDF export of the executed notebook
- Documentation files
- Small output CSVs if needed for dashboard reproduction
- Presentation file or public presentation link

Before submitting, all public links must be tested in Incognito Mode. The assignment explicitly says permission errors will not be accepted.

## 7. Environment Plan

The implementation can be done in VS Code, local Jupyter Notebook, Google Colab, or Deepnote. The notebook must use relative paths only. It must not reference a personal path such as `C:/Downloads`, `/home/user/Downloads`, or any machine-specific location.

The notebook should use a simple path strategy:

```text
Use archive/ if it exists.
Otherwise, look for CSV files in the current notebook folder.
```

This makes the project reproducible across environments. In local development, the data can live in `archive/`. In Colab, the CSVs can be uploaded to the runtime or placed in a folder with the same name.

The required Python packages are:

| Package | Reason |
| --- | --- |
| `pandas` | Load CSVs, clean data, join tables, aggregate metrics |
| `numpy` | Conditional logic and numeric calculations |
| `matplotlib` | Static charts in the notebook |
| `seaborn` | Clean statistical charts |
| `plotly` | Interactive charts if needed |
| `nbformat` | Notebook and Plotly compatibility |
| `jupyter` | Running and exporting the notebook |

The project does not require a complex application backend unless Streamlit is selected for the dashboard. For a fast and clean submission, Tableau Public, Looker Studio, or Power BI Web can consume the summary CSVs exported from the notebook.

## 8. Table Understanding and Data Grain

Understanding data grain is critical. Grain means what one row represents. Most mistakes in relational datasets happen when tables with different grains are joined without care.

### 8.1 Orders Table

File: `archive/olist_orders_dataset.csv`

Columns:

```text
order_id
customer_id
order_status
order_purchase_timestamp
order_approved_at
order_delivered_carrier_date
order_delivered_customer_date
order_estimated_delivery_date
```

The orders table is the central table. The intended grain is one row per order. It contains the delivery timestamps needed to calculate whether a delivery was on time.

Important fields:

- `order_id`: primary order identifier.
- `customer_id`: key to join customer location.
- `order_status`: status such as delivered, canceled, unavailable, shipped, or processing.
- `order_delivered_customer_date`: actual date package reached customer.
- `order_estimated_delivery_date`: promised estimated delivery date.

This table is the base of the master dataset.

### 8.2 Reviews Table

File: `archive/olist_order_reviews_dataset.csv`

Columns:

```text
review_id
order_id
review_score
review_comment_title
review_comment_message
review_creation_date
review_answer_timestamp
```

The reviews table stores customer sentiment. The main required field is `review_score`, which ranges from 1 to 5.

This table may contain multiple review records for one order. Because the acceptance criteria warn about accidental duplicate rows, the implementation should aggregate reviews to one row per `order_id` before joining them to orders. The simplest approach is to calculate average review score per order and count the number of review IDs per order.

### 8.3 Customers Table

File: `archive/olist_customers_dataset.csv`

Columns:

```text
customer_id
customer_unique_id
customer_zip_code_prefix
customer_city
customer_state
```

The customers table provides location data. The required geographic field is `customer_state`. The join key is `customer_id`.

The main state analysis should use customer state, not seller state, because the user story asks which states customers are experiencing late deliveries in.

### 8.4 Products Table

File: `archive/olist_products_dataset.csv`

Columns:

```text
product_id
product_category_name
product_name_lenght
product_description_lenght
product_photos_qty
product_weight_g
product_length_cm
product_height_cm
product_width_cm
```

The products table provides product category and physical product attributes. The category name is in Portuguese. It must be translated into English for the final dashboard if category analysis is included.

The physical fields may support optional future work, such as testing whether heavier or larger products are more likely to be delayed.

### 8.5 Order Items Table

File: `archive/olist_order_items_dataset.csv`

Columns:

```text
order_id
order_item_id
product_id
seller_id
shipping_limit_date
price
freight_value
```

The order items table connects orders to products and sellers. It is not one row per order. One order can have multiple items. This means direct joins from orders to order items will increase the number of rows.

To avoid corrupting order-level delivery metrics, order items should only be used in a separate product category analysis or should be aggregated to one row per order before joining to the master table.

### 8.6 Translation Table

File: `archive/product_category_name_translation.csv`

Columns:

```text
product_category_name
product_category_name_english
```

This table maps Portuguese product category names to English category names. It should be joined to the products table on `product_category_name`.

### 8.7 Optional Tables

The sellers, payments, and geolocation tables are available but not required for the core analysis.

Possible future uses:

- Sellers: compare seller state to customer state.
- Payments: explore whether payment value or payment type relates to review score.
- Geolocation: create map coordinates or estimate distance.

These optional tables should be reserved for later extensions so the main submission stays focused.

## 9. Master Dataset Design

The master dataset should be an order-level table. One row must equal one order. This is the safest structure for calculating late delivery rates because each order should count once.

Planned join sequence:

1. Start with `orders`.
2. Join `customers` on `customer_id`.
3. Aggregate `reviews` to one row per `order_id`.
4. Join aggregated reviews on `order_id`.

The product category analysis should not be directly added to the main master table until the order item data has been reduced to one row per order. Otherwise, multi-item orders can create duplicate order rows and inflate counts.

Join validation checks:

- Compare raw orders row count with final master row count.
- Compare unique `order_id` count before and after joins.
- Check whether any `order_id` appears more than once in the master dataset.
- Confirm the review aggregation has one row per `order_id`.
- Confirm customers join as expected.

This validation is important because the assignment specifically calls out duplication as a common error.

## 10. Data Cleaning Plan

The cleaning process should be simple, transparent, and documented in the notebook.

Planned cleaning steps:

1. Load required CSVs.
2. Standardize column names only if necessary. Since Olist already uses consistent snake-case names, major renaming is not required.
3. Convert timestamp columns to datetime.
4. Count missing values in important delivery columns.
5. Flag orders without actual customer delivery date.
6. Aggregate reviews to order level.
7. Join tables using validated keys.
8. Create delay fields.
9. Translate product categories.
10. Export clean summary tables.

The date columns in the orders table that should be converted are:

- `order_purchase_timestamp`
- `order_approved_at`
- `order_delivered_carrier_date`
- `order_delivered_customer_date`
- `order_estimated_delivery_date`

Undelivered orders should not be silently removed. They should be labeled as `Not Delivered` and counted. The main delay analysis will focus on delivered orders because there is no actual delivery date for missing deliveries.

## 11. Delay Metric Definition

The assignment requires this calculated column:

```text
Days_Difference = order_estimated_delivery_date - order_delivered_customer_date
```

Interpretation:

| Value | Meaning |
| ---: | --- |
| Positive | Delivered before the estimated date |
| Zero | Delivered exactly on estimated date |
| Negative | Delivered after the estimated date |

Because negative values can be awkward for dashboard users, a second field should be created:

```text
Delay_Days = maximum of 0 and negative Days_Difference reversed
```

Plain-language meaning:

- If an order is on time or early, `Delay_Days` is 0.
- If an order is late, `Delay_Days` is the number of days late.

Delivery status rules:

| Status | Rule |
| --- | --- |
| `On Time` | Actual delivery date is on or before estimated delivery date |
| `Late` | Actual delivery date is 1 to 5 days after estimated delivery date |
| `Super Late` | Actual delivery date is more than 5 days after estimated delivery date |
| `Not Delivered` | Actual delivery date is missing |

The main late rate should count both `Late` and `Super Late` as late deliveries.

## 12. Geographic Analysis Plan

The geographic user story asks for the percentage of late orders by state. The dimension is `customer_state`.

The state-level summary should include:

| Field | Meaning |
| --- | --- |
| `customer_state` | State abbreviation |
| `delivered_orders` | Number of delivered orders |
| `late_orders` | Number of delivered orders classified as Late or Super Late |
| `super_late_orders` | Number of delivered orders more than five days late |
| `late_rate` | Late orders divided by delivered orders |
| `super_late_rate` | Super late orders divided by delivered orders |
| `avg_delay_days` | Average number of late days, with on-time orders as zero |
| `avg_review_score` | Average review score |

The recommended first visualization is a descending bar chart of `late_rate` by `customer_state`. A map can also be created, but a bar chart is safer because it is easy to read and does not depend on geographic mapping configuration.

The final business interpretation should identify whether late deliveries are concentrated in a few states or spread broadly. The analysis should be careful when discussing remote states. If states far from the main commercial regions have higher late rates, the project can describe that as a pattern. However, without calculating actual shipping distance, the project should not claim distance is proven as the cause.

## 13. Sentiment Analysis Plan

The sentiment user story asks whether late deliveries are connected to bad reviews. The analysis will compare `review_score` with delay metrics.

Required views:

1. Average review score for `On Time`, `Late`, and `Super Late` orders.
2. Average review score by delivery delay bucket.
3. Optional scatter or box plot comparing delay days and review score.

Recommended delay buckets:

| Bucket | Rule |
| --- | --- |
| `0` | Delivered on time or early |
| `1-2` | 1 to 2 days late |
| `3-5` | 3 to 5 days late |
| `6-10` | 6 to 10 days late |
| `11-20` | 11 to 20 days late |
| `21+` | More than 20 days late |

The analysis should show both average review score and order count. Order count is important because averages based on small groups can be misleading.

The final wording should be cautious. This project can show association between late deliveries and review scores. It should not overstate causality unless more advanced causal analysis is added. Good wording is:

```text
Late deliveries are associated with lower review scores.
```

Avoid wording like:

```text
Late deliveries definitely caused every bad review.
```

## 14. Product Translation Plan

The product translation requirement will be handled with three tables:

```text
order_items -> products -> product_category_name_translation
```

The join path is:

1. Join order items to products using `product_id`.
2. Join products to translations using `product_category_name`.
3. Use `product_category_name_english` in the final dashboard.

Missing translations should be handled safely. If an English category is missing, the notebook can label it `unknown` or retain the Portuguese category as a fallback.

Because order items are a one-to-many table, the category analysis should either:

- Stay at item level and clearly explain that each row is an item, or
- Aggregate categories to order level before joining to the master order dataset.

The recommended approach is order-level aggregation because the rest of the project is order-level.

## 15. Candidate's Choice Analysis

The Candidate's Choice addition will be product category delivery risk.

Business reason:

Delivery failures may not only be regional. Some product categories may be harder to ship because they are heavy, bulky, fragile, expensive, or more dependent on specific sellers. Category-level analysis helps Veridi understand whether operational problems are connected to the nature of the products being shipped.

The category risk table should include:

| Field | Meaning |
| --- | --- |
| `product_category_name_english` | Product category in English |
| `delivered_orders` | Count of delivered orders in that category |
| `late_orders` | Count of late or super-late orders |
| `late_rate` | Late orders divided by delivered orders |
| `avg_delay_days` | Average delay days |
| `avg_review_score` | Average customer review score |

To avoid misleading results, categories with very small volume should be filtered out or clearly marked. A minimum threshold of 100 delivered orders is a reasonable starting point. The final notebook should state whatever threshold is used.

Recommended visualization:

- Horizontal bar chart of the top 10 to 15 categories by late rate.
- Tooltip or label for delivered order count.
- Optional color encoding for average review score.

This addition should be explained in the README under the technical explanation section.

## 16. Dashboard Design Plan

The dashboard must be publicly accessible. The recommended tools are Tableau Public, Google Looker Studio, Power BI Web, or Streamlit Cloud.

The dashboard should be designed for business users. It should focus on quick understanding, not technical detail.

Recommended dashboard title:

```text
Delivery Promise Accuracy and Customer Sentiment
```

Recommended layout:

1. KPI cards at the top.
2. State-level late delivery chart.
3. Review score by delivery status.
4. Delay bucket and review score trend.
5. Product category risk chart.
6. Short recommendation notes.

KPI cards:

| KPI | Purpose |
| --- | --- |
| Total Delivered Orders | Shows analysis size |
| National Late Rate | Shows overall delivery promise failure |
| Super Late Rate | Shows severe delivery failure |
| Average Review Score | Shows overall sentiment |
| Worst State Late Rate | Highlights regional risk |

Filters:

- Customer state
- Delivery status
- Product category
- Review score

The dashboard should use clear labels. Percentages should be formatted as percentages. Review score charts should use a 1-to-5 scale or a 0-to-5 scale with clear labeling.

## 17. Dashboard Data Outputs

The notebook should export summary tables for dashboarding.

Planned outputs:

| Output File | Purpose |
| --- | --- |
| `outputs/state_delivery_summary.csv` | State-level late rate and review metrics |
| `outputs/sentiment_by_delivery_status.csv` | Average review score by delivery status |
| `outputs/delay_bucket_review_summary.csv` | Review score by delay bucket |
| `outputs/category_delivery_summary.csv` | Product category delivery risk |

These files are small aggregated outputs, not raw data. They can be used to build the dashboard and may be safe to include in the repository if needed.

## 18. Notebook Structure Plan

The notebook should be written like a report. Each technical section should have Markdown explaining what the next code cell is doing.

Recommended notebook outline:

1. Title and objective
2. Import libraries
3. Define file paths
4. Load CSV files
5. Show file row counts
6. Convert date columns
7. Aggregate reviews
8. Build master dataset
9. Validate joins
10. Calculate delivery delay
11. Classify delivery status
12. Analyze national delivery performance
13. Analyze late delivery by state
14. Analyze review score by delivery status
15. Analyze review score by delay bucket
16. Translate product categories
17. Build Candidate's Choice category analysis
18. Export dashboard summary tables
19. Print README-ready final metrics

The notebook should avoid unnecessary complexity. The goal is to show strong data science judgment, not to make the solution harder than needed.

## 19. README Plan

The final `README.md` must begin with the three sections requested in the assignment.

### A. Executive Summary

This should be 3 to 5 sentences after the notebook has been run. It should include actual values from the analysis.

Recommended structure:

1. State the overall late-delivery rate.
2. Explain whether the issue is concentrated or broad.
3. Name the worst-performing state or states.
4. Summarize the review score difference between on-time and late deliveries.
5. Mention the Candidate's Choice category finding.

### B. Project Links

This section should include:

- Link to notebook
- Link to dashboard
- Link to presentation
- Optional video walkthrough

Every link must be tested in Incognito Mode.

### C. Technical Explanation

This section should explain:

- How the data was loaded.
- Which joins were performed.
- How duplicate rows were avoided.
- How missing delivery dates were handled.
- How delay status was calculated.
- How product categories were translated.
- Why product category risk was selected as the Candidate's Choice analysis.

## 20. Presentation Plan

The presentation should be short and business-focused. It should not be a code walkthrough. It should tell the story of the analysis and explain what Veridi should do next.

Recommended slides:

1. Title: Last Mile Logistics Auditor.
2. Business problem: negative reviews and delivery promise accuracy.
3. Data and methodology: Olist data, joins, delay calculation.
4. National performance: total delivered orders, late rate, super-late rate.
5. Geographic risk: worst states by late delivery percentage.
6. Sentiment impact: review score comparison by delivery status.
7. Candidate's Choice: product category delivery risk.
8. Recommendations: practical actions for Veridi.
9. Links: repository, notebook, dashboard, optional video.

The recommendations should be directly tied to findings. For example, if certain states have very high late rates, the recommendation can be to recalibrate delivery estimates or investigate carrier performance in those states. If late orders have much lower review scores, the recommendation can be to prioritize delay reduction as a customer satisfaction lever.

## 21. Notebook Export Plan

The assignment requires both the `.ipynb` notebook and an HTML or PDF export. This is important because GitHub sometimes fails to render notebooks.

After the notebook is executed, export it as HTML or PDF. A recommended command is:

```text
jupyter nbconvert --to html last_mile_logistics_audit.ipynb
```

The export should be saved with a clear filename such as:

```text
notebook_exports/last_mile_logistics_audit.html
```

Before submission, open the exported file and verify that charts are visible. If interactive charts do not render in the export, the notebook should include static chart versions as backup.

## 22. Quality Assurance Plan

Quality assurance is very important because this is a job exam. The work should look careful and trustworthy.

Data checks:

- Required files load successfully.
- Date columns convert correctly.
- Missing delivery dates are counted.
- Reviews are aggregated before joining.
- Master dataset remains one row per order.
- Late rate uses delivered orders as denominator.
- Product categories are translated.
- Small category sample sizes are handled.

Notebook checks:

- Notebook runs top to bottom without errors.
- No absolute local paths are used.
- All charts have titles.
- All axes are labeled.
- Summary tables are exported.
- Final metrics are easy to copy into the README.

Dashboard checks:

- Public link opens without login.
- Filters work.
- Metrics are formatted correctly.
- Tooltips include order counts.
- Dashboard clearly answers the business question.

Submission checks:

- GitHub repo is public.
- Raw CSVs are not committed.
- Notebook is uploaded.
- HTML or PDF export is uploaded.
- Dashboard link is public.
- Presentation link is public.
- README is updated with final findings.
- Official submission form is completed.

## 23. Risks and Mitigations

### Risk 1: Duplicate Orders After Join

The reviews and order items tables can create duplicates if joined directly. The mitigation is to aggregate them to one row per order before joining to the master dataset.

### Risk 2: Wrong Delay Sign

The assignment formula is estimated date minus actual date. Negative means late. The mitigation is to document the sign clearly and create a positive `Delay_Days` field for readability.

### Risk 3: Missing Actual Delivery Dates

Some orders are canceled, unavailable, or otherwise not delivered. The mitigation is to flag them as `Not Delivered` and exclude them from delivered-order delay rate calculations.

### Risk 4: Overclaiming Causality

The analysis can show that late deliveries are associated with lower review scores. It should not claim strict causation without further causal testing.

### Risk 5: Permission Errors

The assignment warns against permission problems. The mitigation is to test all links in Incognito Mode.

### Risk 6: Dashboard Too Complex

A dashboard with too many charts can confuse reviewers. The mitigation is to focus on the required story: national performance, geography, sentiment, and Candidate's Choice.

## 24. Final Implementation Sequence

The recommended order of work is:

1. Review and approve this implementation documentation.
2. Keep the raw Kaggle files in `archive/`.
3. Confirm `.gitignore` excludes raw CSV data.
4. Build or revise the notebook structure.
5. Load required CSV files.
6. Add join validation checks.
7. Create delay metrics and delivery status.
8. Create state-level summary table.
9. Create sentiment summary tables.
10. Create product category translation and risk table.
11. Export dashboard-ready CSV files.
12. Build the public dashboard.
13. Export the notebook as HTML or PDF.
14. Create the presentation.
15. Update README with actual findings and links.
16. Test all links in Incognito Mode.
17. Submit the official form.

## 25. Definition of Done

The project is done when each requirement has evidence.

| Requirement | Evidence |
| --- | --- |
| Schema Builder | Master table joins orders, customers, and reviews with no duplicate order rows |
| Delay Calculator | `Days_Difference`, `Delay_Days`, and `Delivery_Status` are created |
| Geographic Analysis | Late percentage by `customer_state` is calculated and visualized |
| Sentiment Analysis | Review score is compared by delay and delivery status |
| Translation Bonus | Product categories are shown in English |
| Candidate's Choice | Product category risk is analyzed and justified |
| Dashboard | Public dashboard link works |
| Notebook | `.ipynb` and HTML or PDF export are available |
| README | Executive summary, links, and technical notes are complete |
| Submission | Official form is submitted after link testing |

The finished project should tell a complete story: whether delivery promise failures are isolated or broad, which regions need attention, whether customer sentiment drops when deliveries are late, and what operational action Veridi Logistics should take next.

## 26. Naming Conventions and Communication Standards

The project should use clear and consistent naming so that the notebook, dashboard, and presentation feel like one connected piece of work. This matters because hiring reviewers often judge not only the technical output but also the clarity of communication.

Recommended dataset names inside the notebook:

| Name | Meaning |
| --- | --- |
| `orders` | Raw orders table |
| `reviews` | Raw reviews table |
| `customers` | Raw customers table |
| `products` | Raw products table |
| `order_items` | Raw order items table |
| `translations` | Raw product category translation table |
| `review_summary` | Reviews aggregated to one row per order |
| `master` | Main order-level analytical dataset |
| `delivered` | Delivered orders only |
| `state_summary` | State-level dashboard table |
| `sentiment_summary` | Review score by delivery status |
| `category_summary` | Candidate's Choice category risk table |

Recommended calculated column names:

| Column | Meaning |
| --- | --- |
| `Days_Difference` | Estimated delivery date minus actual delivery date |
| `Delay_Days` | Positive number of days late, with on-time orders set to zero |
| `Delivery_Status` | `On Time`, `Late`, `Super Late`, or `Not Delivered` |
| `is_late` | Boolean flag for Late or Super Late |
| `delay_bucket` | Grouped delay range for sentiment charts |

Chart titles should be written in business language. For example, use `Late Delivery Rate by Customer State` instead of a technical title like `customer_state vs late_rate`. Axis labels should also be readable. Percent metrics should be formatted as percentages, and review scores should be clearly shown as 1-to-5 values.

The notebook should include short Markdown explanations before important code sections. Those explanations should tell the reader what the section does and why it matters. The tone should be confident and simple. The notebook should avoid long paragraphs inside code comments because business reviewers will mainly read section headings, charts, and result tables.

## 27. Review Process Before Building

Before moving from documentation to implementation, the plan should be reviewed against the assignment. The review should confirm that every acceptance criterion has a planned output.

Planned acceptance-criteria mapping:

| Assignment Item | Planned Output |
| --- | --- |
| Load raw CSVs | Notebook data-loading section |
| Join orders, reviews, and customers | `master` dataset |
| Avoid duplicate rows | Join validation table |
| Calculate `Days_Difference` | Delay metric section |
| Classify On Time, Late, Super Late | `Delivery_Status` column |
| Handle missing delivery values | `Not Delivered` status |
| Calculate late percentage by state | `state_summary` table |
| Visualize geography | State bar chart or map |
| Compare delay with review score | Sentiment charts |
| Translate categories | Product translation join |
| Add Candidate's Choice | Product category risk analysis |
| Explain Candidate's Choice | README technical section |

If any planned output is missing, it should be added before writing the final notebook. This reduces the risk of building something impressive but incomplete.

## 28. What Happens After This Documentation

After this document is reviewed, the next step will be implementation. The implementation should be done in a controlled order rather than trying to build everything at once.

First, the notebook will be created or revised to match this document. The data-loading and join-validation sections will be implemented before any charting. This is important because all later insights depend on the correctness of the master dataset.

Second, the delay fields and delivery status classification will be implemented. Once these are correct, the notebook can generate national delivery performance metrics and state-level summaries.

Third, the sentiment analysis will be added. This will connect review scores to delivery performance and directly address the CEO's concern.

Fourth, the product category translation and Candidate's Choice analysis will be implemented. This should be done after the core user stories so the required project remains stable.

Fifth, the summary tables will be exported and used to build the public dashboard. The dashboard will then be linked in the README and presentation.

Finally, the README will be rewritten with the real findings. No final executive summary should be written until the notebook has produced verified numbers. This protects the submission from unsupported claims and keeps the work credible.

This staged approach keeps the project calm, auditable, and professional. It also makes it easier to debug because each stage has a clear purpose and a clear expected output.
