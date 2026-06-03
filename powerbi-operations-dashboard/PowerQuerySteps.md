# Power Query Steps

This document summarizes the key Power Query transformations for the operations dashboard.

## 1. Load Data
- Import `orders.csv`, `warehouse.csv`, `products.csv`, and `delivery_status.csv` from the `/data` folder.
- Set the file path as a parameter to make refresh paths flexible.

## 2. Clean and Standardize
- Remove duplicate rows in each query.
- Set correct data types:
  - `OrderDate` as Date
  - `Quantity`, `OrderValue`, and `ProcessingTimeMin` as Whole Number or Decimal
  - `StatusID`, `WarehouseID`, `ProductID` as Text
- Rename columns consistently if needed.

## 3. Fix Errors and Fill Missing Values
- Replace nulls in `DelayReason` with `"No delay"`.
- Fix or remove rows where `WarehouseID` or `ProductID` are missing.
- Standardize status and category text values.

## 4. Create Custom Columns
- Add a `DelayCategory` column based on `StatusID` or `DelayReason`.
- Add `ProcessingTimeHours = [ProcessingTimeMin] / 60`.
- Add `OrderMonth` or `OrderWeek` if needed for analysis.

## 5. Merge Queries
- Merge `orders` with `products` on `ProductID`.
- Merge the resulting table with `warehouse` on `WarehouseID`.
- Merge with `delivery_status` on `StatusID`.
- Expand only the necessary fields after each merge.

## 6. Unpivot / Reshape (Optional)
- If there are any category columns that need normalization, unpivot them to a long format.
- Use unpivot only for columns that belong in attribute/value pairs.

## 7. Load to Data Model
- Set the final merged query as `FactOrders` in the model.
- Load dimension tables separately for `DimProduct`, `DimWarehouse`, and `DimStatus`.
- Create a dedicated `DimDate` table based on the order date range.

## 8. Parameterize File Paths
- Create a parameter called `DataPath` for the `/data` directory.
- Use that parameter in each source query to simplify refresh and deployment.

## 9. Performance Tips
- Disable `Load` on staging queries and intermediate datasets.
- Keep only the final columns needed for analysis in `FactOrders`.
- Use query folding when loading from supported sources.
