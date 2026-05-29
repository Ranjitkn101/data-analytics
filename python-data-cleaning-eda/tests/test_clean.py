import pandas as pd
from src.clean import clean_sales

def test_clean_sales():
    raw = pd.DataFrame({
        "date": ["2023-01-01", "invalid"],
        "product_id": [101, 102],
        "product_name": ["Apple", "Banana"],
        "sales": [100, -50],
        "quantity": [10, 5],
        "store_id": [1, 1]
    })

    cleaned = clean_sales(raw)

    # Only 1 valid row should remain
    assert cleaned.shape[0] == 1
