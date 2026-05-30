import pandas as pd
from src.clean import clean_sales

def test_clean_sales_basic():
    raw = pd.DataFrame({
        "order_id": ["1", "2", None],
        "customer_id": ["10", "20", "30"],
        "amount": ["100.5", "200.0", "300.0"],
        "quantity": ["1", "2", "3"],
        "order_date": ["2024-01-01", "2024-01-02", "bad-date"],
    })

    cleaned = clean_sales(raw)

    # order_id should be integer
    assert cleaned["order_id"].dtype.kind in "iu"

    # customer_id should be string (your pipeline logic)
    assert cleaned["customer_id"].dtype == "string"

    # amount should be float
    assert cleaned["amount"].dtype.kind == "f"

    # all dates must be valid
    assert cleaned["order_date"].isna().sum() == 0

    # only 2 valid rows should remain
    assert len(cleaned) == 2
