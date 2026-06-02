# DAX Formulas

This document provides sample DAX formulas for the operations dashboard.

## Core Measures

### Total Orders
```dax
Total Orders = COUNTROWS(FactOrders)
```

### Total Delayed Orders
```dax
Total Delayed Orders =
CALCULATE(
    COUNTROWS(FactOrders),
    FactOrders[StatusName] = "Delayed"
)
```

### Fulfilment Rate
```dax
Fulfilment Rate =
DIVIDE(
    [Total Orders] - [Total Delayed Orders],
    [Total Orders],
    0
)
```

### Average Processing Time
```dax
Avg Processing Time =
AVERAGE(FactOrders[ProcessingTimeMin])
```

### Delay % by Warehouse
```dax
Delay % by Warehouse =
DIVIDE(
    [Total Delayed Orders],
    [Total Orders],
    0
)
```

## Time Intelligence

### Orders Year-over-Year Growth
```dax
Orders YoY Growth =
VAR Current = [Total Orders]
VAR PriorYear =
    CALCULATE(
        [Total Orders],
        SAMEPERIODLASTYEAR(DimDate[Date])
    )
RETURN
DIVIDE(Current - PriorYear, PriorYear, 0)
```

### Orders Last 12 Months
```dax
Orders Last 12 Months =
CALCULATE(
    [Total Orders],
    DATESINPERIOD(DimDate[Date], LASTDATE(DimDate[Date]), -12, MONTH)
)
```

### Delay Rate YoY
```dax
Delay Rate YoY =
VAR CurrentDelay = [Total Delayed Orders]
VAR PriorDelay =
    CALCULATE(
        [Total Delayed Orders],
        SAMEPERIODLASTYEAR(DimDate[Date])
    )
RETURN
DIVIDE(CurrentDelay - PriorDelay, PriorDelay, 0)
```

## Advanced Measures

### Top 5 Delayed Products
```dax
Top 5 Delayed Products =
TOPN(
    5,
    SUMMARIZE(
        FactOrders,
        DimProduct[ProductName],
        "DelayedCount",
        [Total Delayed Orders]
    ),
    [DelayedCount],
    DESC
)
```

### Warehouse Fulfilment Rate
```dax
Warehouse Fulfilment Rate =
DIVIDE(
    CALCULATE(
        [Total Orders],
        FactOrders[StatusName] <> "Delayed"
    ),
    [Total Orders],
    0
)
```

### Delay Reasons by Count
```dax
Delay Reason Count =
CALCULATE(
    COUNTROWS(FactOrders),
    FactOrders[StatusName] = "Delayed"
)
```

## DAX Patterns
- Use `CALCULATE` to change filter context for KPIs.
- Use `FILTER` and `ALL` to ignore slicers or context when needed.
- Use `ALLEXCEPT` for measures that should retain only specific dimensions.
- Use `DIVIDE` to avoid divide-by-zero errors.
- Use `SAMEPERIODLASTYEAR` and `DATESINPERIOD` for time comparisons.
