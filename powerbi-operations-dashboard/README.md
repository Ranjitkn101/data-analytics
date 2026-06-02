# Power BI Operations Dashboard

## ✔ Project Overview
This project is a Power BI operations dashboard built to help an operations team track orders, fulfillment efficiency, delays, and warehouse performance. The dashboard is designed for daily operational monitoring, root-cause analysis, and trend-based decision support.

## 1️⃣ Business Problem

### Business scenario
Operations leaders need a single view of order flow, fulfillment status, delay drivers, and warehouse bottlenecks. The goal is to answer:
- How many orders are processed each day?
- What is the fulfillment rate over time?
- Which warehouse is experiencing the most delays?
- Which products contribute most to delays?
- What are the volume and delay trends week-over-week and month-over-month?

## 2️⃣ Dataset Description
Sample datasets are stored in `/data` and include:
- `orders.csv` — order transactions with dates, warehouse, product, status, quantity, processing time, and delay reason.
- `warehouse.csv` — warehouse master data with region, capacity and manager.
- `products.csv` — product master with category, lead time and weight.
- `delivery_status.csv` — delivery status lookup with fulfillment flag.

### Data quality features
- Includes date fields, categories, numeric values, and status fields.
- Supports Power Query transformations for type cleanup, deduplication, merged tables, and conditional columns.

## 3️⃣ Power Query Transformations
Transformations to perform in Power Query:
- Remove duplicates from source tables.
- Fix data types for dates, numeric fields, and text values.
- Merge `orders` with `products`, `warehouse`, and `delivery_status` on keys.
- Create custom duration columns from `ProcessingTimeMin`.
- Unpivot multi-category columns if needed for analysis.
- Replace errors on missing warehouse or product data.
- Add conditional columns such as `DelayCategory` and `FulfilmentFlag`.
- Parameterize file paths using a directory parameter for `/data`.

## 4️⃣ Data Model Design
The model uses a star schema centered on `FactOrders`:

```
FactOrders
   |
   |--- DimDate
   |--- DimProduct
   |--- DimWarehouse
   |--- DimStatus
```

### Why star schema
- Supports fast aggregation and filtering.
- Simplifies DAX for KPIs and time intelligence.
- Enables clear single-direction relationships.

### Relationship design
- Use single-direction relationships from dimensions to fact to prevent ambiguity.
- Use surrogate keys where appropriate, especially in `DimDate` and `FactOrders`, for stable joins across data refreshes.

## 5️⃣ DAX Measures
### Key Measures
- `Total Orders = COUNTROWS(FactOrders)`
- `Total Delayed Orders = CALCULATE(COUNTROWS(FactOrders), FactOrders[StatusName] = "Delayed")`
- `Fulfilment Rate = DIVIDE([Total Orders] - [Total Delayed Orders], [Total Orders])`
- `Avg Processing Time = AVERAGE(FactOrders[ProcessingTimeMin])`
- `Orders YoY Growth = DIVIDE([Total Orders] - CALCULATE([Total Orders], SAMEPERIODLASTYEAR(DimDate[Date])), CALCULATE([Total Orders], SAMEPERIODLASTYEAR(DimDate[Date])))`
- `Delay % by Warehouse = DIVIDE([Total Delayed Orders], [Total Orders])` filtered by warehouse
- `Top 5 Delayed Products = TOPN(5, SUMMARIZE(FactOrders, DimProduct[ProductName], "DelayedCount", [Total Delayed Orders]), [DelayedCount], DESC)

### DAX techniques
- Time intelligence with `SAMEPERIODLASTYEAR`, `TOTALYTD`, and `DATEADD`.
- Calculation logic with `CALCULATE` and `FILTER`.
- Context control using `ALL` and `ALLEXCEPT`.
- Dynamic ranking for top products and warehouses.

## 6️⃣ Dashboard Design
### Page 1 — Executive Summary
- KPI cards: `Total Orders`, `Fulfilment Rate`, `Delayed Orders`, `Avg Processing Time`.
- Trend line: orders over time with fulfillment overlay.
- Fulfilment rate gauge.
- Delay % by warehouse.
- Map of warehouse locations and region performance.

### Page 2 — Operations Deep Dive
- Orders by product category and product.
- Orders by warehouse and region.
- Delay reasons breakdown.
- Processing time distribution histogram.
- Table of delayed order detail for root-cause analysis.

### Page 3 — Time Intelligence
- Monthly trend line for orders and delays.
- Year-over-year comparison chart.
- Forecasting visual (optional) using trend line or decomposition tree.

## 7️⃣ Advanced Features
Recommended advanced features:
- Bookmarks for before/after operational view.
- Drill-through page from summary to order detail.
- Tooltip page for delay reason context.
- Dynamic titles using selected filters.
- Custom theme for polished corporate styling.
- Performance Analyzer optimization for large data refresh.

## 8️⃣ Skills Demonstrated
This repository demonstrates:
- Data cleaning and ETL in Power Query.
- Star schema data modeling.
- DAX calculation and time intelligence.
- Dashboard storytelling and UX design.
- Advanced Power BI features like drill-through, tooltips, and dynamic titles.

## Insights & Findings
Document your business insights and report conclusions here once the dashboard is built. Example findings may include:
- The warehouse with the highest delay rate.
- Product categories causing the most fulfillment issues.
- Trends in order volume and processing time.
- Opportunities to improve fulfillment efficiency.

## Supplemental Documentation
- `PowerQuerySteps.md` — detailed ETL and transformation steps.
- `DAXFormulas.md` — sample DAX measures and time intelligence formulas.
- `DataModelDiagram.md` — recommended star schema layout and relationship guidance.
- `DataModelSchema.json` — JSON schema for the dimension and fact table definitions.

## 9️⃣ Screenshots
Add dashboard screenshots to `/screenshots`:
- `home-page.png`
- `deep-dive-page.png`
- `tooltip-page.png`
- `data-model-view.png`
- `power-query-steps.png`

## 🔟 PBIX Export
A placeholder file is included at `dashboard.pbix`. Replace it with your exported Power BI report file when the report is complete.

---

### How to use
1. Load the CSV files from `/data` into Power BI.
2. Apply Power Query transformations and build the star schema.
3. Create DAX measures and build the three dashboard pages.
4. Export the finished `.pbix` into the root folder as `dashboard.pbix`.
