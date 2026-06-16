# Last Mile Logistics Auditor Presentation Outline

## Slide 1: Title

**Last Mile Logistics Auditor**

Delivery promise accuracy and customer sentiment audit for Veridi Logistics.

## Slide 2: Business Question

**CEO question:** Are we failing specific regions, or is this a nationwide problem?

Key audit focus:

- Compare estimated delivery dates with actual delivery dates.
- Identify where late deliveries are concentrated.
- Connect delivery performance to customer reviews.

## Slide 3: Data and Method

Dataset: Olist Brazilian E-Commerce Dataset.

Tables used:

- Orders
- Reviews
- Customers
- Products
- Order items
- Product category translations

Method:

- Joined orders, customers, and aggregated reviews.
- Calculated `Days_Difference = estimated delivery date - actual delivery date`.
- Classified delivered orders as `On Time`, `Late`, or `Super Late`.
- Excluded undelivered orders from delivered-order delay metrics.

## Slide 4: National Performance

Key metrics:

- Delivered orders: 96,476
- Late or super-late rate: 8.1%
- Super-late orders: 4,212
- On-time average review score: 4.29/5
- Super-late average review score: 1.79/5

Message:

Delivery promise accuracy is a real operational issue, and severe delays strongly damage customer sentiment.

## Slide 5: Regional Findings

Worst states by late rate:

- AL: 23.9%
- MA: 19.7%
- PI: 16.0%
- CE: 15.3%
- SE: 15.2%

Message:

The issue is regionally concentrated, not evenly distributed nationwide.

## Slide 6: Sentiment Impact

Review score by delivery status:

- On Time: 4.29/5
- Late: 3.46/5
- Super Late: 1.79/5

Message:

Late deliveries are associated with lower customer satisfaction, and super-late orders create the largest review-score damage.

## Slide 7: Delay Severity

Use the delay bucket chart from the dashboard or notebook.

Message:

Customer sentiment drops as delays become more severe, especially after the delivery is more than five days late.

## Slide 8: Candidate's Choice - Category Risk

Highest-risk category by late rate:

- Audio: 12.9%

Business value:

Category risk analysis shows whether delivery failures are linked to product type and fulfillment complexity, not only geography.

## Slide 9: Dashboard Walkthrough

Show the Streamlit dashboard:

- KPI cards
- State drilldown
- Regional late-rate ranking
- Risk matrix
- Delay severity curve
- Product category risk
- Leaderboards

## Slide 10: Recommendations

Recommended actions:

- Prioritize operational review in AL, MA, PI, CE, and SE.
- Recalibrate delivery estimates in high-risk states.
- Track super-late deliveries separately as a customer satisfaction risk.
- Investigate high-risk product categories such as audio.
- Monitor delivery promise accuracy as an ongoing executive KPI.

## Slide 11: Closing

Final answer to the CEO:

Delivery failures are not just a nationwide average problem. They are concentrated in specific regions and are strongly associated with lower review scores, especially when orders become super late.
