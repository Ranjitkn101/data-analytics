import pandas as pd
from src.validate import validate_sales
import pytest

def test_validate_sales_pass():
    df = pd.DataFrame({
        "order_id": [1, 2],
        "customer_id": [10, 20],
        "amount": [100.0, 200.0],
        "quantity": [1, 2],
        "order_date": pd.to_datetime(["2024-01-01", "2024-01-02"]),
    })
    validate_sales(df)  # should not raise

def test_validate_sales_negative_amount():
    df = pd.DataFrame({
        "order_id": [1],
        "customer_id": [10],
        "amount": [-10.0],
        "quantity": [1],
        "order_date": pd.to_datetime(["2024-01-01"]),
    })
    with pytest.raises(ValueError):
        validate_sales(df)
