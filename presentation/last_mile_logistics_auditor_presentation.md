---
title: "Last Mile Logistics Auditor"
subtitle: "Delivery promise accuracy and customer sentiment audit"
author: "Irigenera Alliance | AIMS Rwanda | AmaliTech Rwanda Exam Task"
---

# Last Mile Logistics Auditor

Delivery promise accuracy and customer sentiment audit for Veridi Logistics.

Prepared by **Irigenera Alliance**  
Student at **AIMS Rwanda**  
Exam task for **AmaliTech Rwanda**

Dataset: Olist Brazilian E-Commerce Dataset.

# Executive Summary

- 96,476 delivered orders were analyzed.
- 8.1% of delivered orders were late or super late.
- AL has the highest late rate at 23.9%, followed by MA at 19.7%.
- On-time orders average 4.29/5 in review score.
- Super-late orders average 1.79/5.
- Audio has the highest category-level late rate at 12.9%.

# Data Model and Cleaning

- Orders joined to customers on `customer_id`.
- Reviews aggregated to one row per order before joining on `order_id`.
- Products, order items, and category translations used for category risk analysis.
- Date fields converted to datetime.
- Undelivered orders flagged separately and excluded from delivered-order delay metrics.

# Delay Classification

`Days_Difference = order_estimated_delivery_date - order_delivered_customer_date`

- `On Time`: delivered on or before the estimated date.
- `Late`: delivered 1 to 5 days after the estimated date.
- `Super Late`: delivered more than 5 days after the estimated date.
- `Not Delivered`: missing actual delivery date.

# National Performance

- Delivered orders: 96,476
- On-time orders: 88,649
- Late orders: 3,615
- Super-late orders: 4,212
- National late or super-late rate: 8.1%

# Regional Findings

Worst states by late rate:

- AL: 23.9%
- MA: 19.7%
- PI: 16.0%
- CE: 15.3%
- SE: 15.2%

The issue is regionally concentrated, not evenly distributed nationwide.

# Sentiment Impact

- On Time: 4.29/5
- Late: 3.46/5
- Super Late: 1.79/5

Late deliveries are associated with lower customer satisfaction, and super-late deliveries create the largest review-score damage.

# Candidate's Choice: Product Category Risk

Highest-risk categories by late rate:

- Audio: 12.9%
- Fashion underwear beach: 12.8%
- Home comfort: 11.0%

This helps Veridi identify product and fulfillment risks beyond geography.

# Dashboard Walkthrough

Dashboard link:

<https://amalitech-pzzepkval4rfh3phyyf2jh.streamlit.app/>

The dashboard includes:

- Executive KPI cards
- State drilldown
- Regional late-rate ranking
- Risk matrices
- Delay severity curve
- Category risk and impact analysis
- State and category leaderboards

# Recommendations

- Prioritize operational review in AL, MA, PI, CE, and SE.
- Recalibrate delivery estimates in high-risk states.
- Track super-late deliveries separately as a customer satisfaction risk.
- Investigate high-risk product categories such as audio.
- Monitor delivery promise accuracy as an ongoing KPI.

# Final CEO Answer

Delivery failures are not just a nationwide average problem. They are concentrated in specific regions and are strongly associated with lower review scores, especially when orders become super late.
