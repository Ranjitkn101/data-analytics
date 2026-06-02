# Data Model Diagram

This document describes the recommended data model and relationships for the operations dashboard.

## Star Schema Layout

The dashboard should use a star schema to keep analytics fast and intuitive.

### Fact Table
- `FactOrders`
  - `OrderID`
  - `OrderDate`
  - `ProductID`
  - `WarehouseID`
  - `StatusID`
  - `Quantity`
  - `OrderValue`
  - `ProcessingTimeMin`
  - `DelayReason`
  - `ProcessingTimeHours`

### Dimension Tables
- `DimDate`
  - `Date`
  - `Year`
  - `Quarter`
  - `Month`
  - `MonthName`
  - `WeekNumber`
  - `DayOfWeek`

- `DimProduct`
  - `ProductID`
  - `ProductName`
  - `Category`
  - `LeadTimeDays`
  - `WeightKg`

- `DimWarehouse`
  - `WarehouseID`
  - `WarehouseName`
  - `Region`
  - `Capacity`
  - `Manager`

- `DimStatus`
  - `StatusID`
  - `StatusName`
  - `IsFulfilled`

## Relationship Guidance

- Link `FactOrders[OrderDate]` to `DimDate[Date]`.
- Link `FactOrders[ProductID]` to `DimProduct[ProductID]`.
- Link `FactOrders[WarehouseID]` to `DimWarehouse[WarehouseID]`.
- Link `FactOrders[StatusID]` to `DimStatus[StatusID]`.

### Relationship settings
- Use single-direction relationships from each dimension into `FactOrders`.
- Keep them as one-to-many, with the dimension side set to "one" and fact side set to "many".
- Enable cross-filter direction only where needed; prefer single direction for performance and model clarity.

## Why this model

- A star schema reduces complexity and improves query performance.
- Dimensions isolate descriptive attributes from transactional data.
- The fact table stores metrics and keys only, making calculations easier.
- This structure supports time intelligence and filter propagation without ambiguity.
