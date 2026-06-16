# Last Mile Logistics Auditor

Delivery performance audit for Veridi Logistics using the Olist Brazilian E-Commerce dataset.

## A. Executive Summary

Out of 96,476 delivered orders, **8.1% were late or super late**, confirming a measurable delivery promise gap. The issue is not evenly distributed: **Alagoas (AL) has the highest late rate at 23.9%**, followed by **Maranhao (MA) at 19.7%**, which shows that delivery failures are concentrated in specific regions rather than being purely nationwide. Late delivery is strongly associated with weaker customer sentiment: on-time orders average **4.29/5**, while super-late orders average only **1.79/5**. The Candidate's Choice analysis adds product-category risk, where **audio** has the highest category late rate at **12.9%**, showing that some delivery problems may also be linked to product and fulfillment complexity.

## B. Project Links

- **Link to Notebook:** <https://github.com/Alliance2k2/amalitech/blob/main/last_mile_logistics_audit.ipynb>
- **Notebook HTML Export:** <https://github.com/Alliance2k2/amalitech/blob/main/notebook_exports/last_mile_logistics_audit.html>
- **Link to Dashboard:** <https://amalitech-pzzepkval4rfh3phyyf2jh.streamlit.app/>
- **Link to Presentation PDF:** <https://github.com/Alliance2k2/amalitech/blob/main/presentation/last_mile_logistics_auditor_presentation.pdf>
- **Link to Presentation PPTX:** <https://github.com/Alliance2k2/amalitech/blob/main/presentation/last_mile_logistics_auditor_presentation.pptx>

## C. Technical Explanation

### Data Cleaning

The notebook uses relative paths and expects the raw Olist CSV files in a local `archive/` folder. Date fields are converted to datetime values before delay calculations. Orders without an actual customer delivery date are flagged as `Not Delivered` and excluded from the main delivered-order delay analysis because they do not have a reliable actual delivery timestamp.

The master dataset joins:

- `olist_orders_dataset.csv` to `olist_customers_dataset.csv` on `customer_id`
- aggregated `olist_order_reviews_dataset.csv` to orders on `order_id`
- product category analysis through `olist_order_items_dataset.csv`, `olist_products_dataset.csv`, and `product_category_name_translation.csv`

Reviews are aggregated to one row per order before joining, which prevents accidental row duplication from one-to-many review records. The notebook validates row counts and unique `order_id` values after the core joins.

### Delay Classification

The notebook creates:

```text
Days_Difference = order_estimated_delivery_date - order_delivered_customer_date
```

Positive values mean an order arrived before the promised date, `0` means it arrived on the promised date, and negative values mean it was late.

Delivery statuses:

- `On Time`: delivered on or before the estimated delivery date
- `Late`: delivered 1 to 5 days after the estimated delivery date
- `Super Late`: delivered more than 5 days after the estimated delivery date
- `Not Delivered`: missing actual delivery date

### Dashboard

The Streamlit dashboard uses only aggregated summary CSVs from `outputs/`, not the raw Kaggle dataset. It includes executive KPI cards, state drilldown, regional late-rate ranking, delivery-status mix, review-score comparisons, delay severity analysis, category risk ranking, impact matrices, and operational leaderboards.

### Candidate's Choice Addition

I added product-category delivery risk analysis using translated English category names. This matters because logistics failures may be connected to product type, packaging complexity, supplier behavior, or fulfillment process differences. The analysis helps Veridi decide whether improvement work should target only regions or also specific product categories.

## Deliverables

- `last_mile_logistics_audit.ipynb`: reproducible analysis notebook.
- `notebook_exports/last_mile_logistics_audit.html`: notebook export for reliable chart viewing.
- `app.py`: Streamlit dashboard application.
- `outputs/*.csv`: dashboard-ready summary tables.
- `outputs/*.png`: static chart exports from the notebook.
- `presentation/last_mile_logistics_auditor_presentation.pdf`: final designed presentation deck.
- `presentation/last_mile_logistics_auditor_presentation.pptx`: editable slide deck.
- `presentation_outline.md`: suggested slide structure for the insight presentation.
- `requirements.txt`: Python dependencies.
- `STREAMLIT_DASHBOARD_ENGINEERING_DOCUMENTATION.md`: dashboard deployment and design notes.

## How to Run

1. Download the Olist dataset from Kaggle: <https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce>
2. Place the raw CSV files in a local `archive/` folder next to the notebook.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the notebook from top to bottom:

```text
last_mile_logistics_audit.ipynb
```

5. Run the dashboard:

```bash
streamlit run app.py
```

## Deployment Notes

The repository should include the notebook, notebook export, dashboard code, requirements file, and `outputs/` summary files. The raw `archive/` folder should remain local and must not be committed to GitHub.

Before submission, test the GitHub repository, dashboard link, and presentation link in an Incognito or private browser window.

## Pre-Submission Checklist

- [x] GitHub repository is public and opens in Incognito Mode.
- [x] `.ipynb` notebook is uploaded.
- [x] HTML notebook export is uploaded.
- [x] Raw CSV dataset files are not committed.
- [x] Code uses relative paths only.
- [x] Dashboard link is public.
- [x] Presentation link is public.
- [x] README contains final executive summary and technical explanation.
- [x] User Stories 1-4 are complete.
- [x] Candidate's Choice analysis is complete and explained.
