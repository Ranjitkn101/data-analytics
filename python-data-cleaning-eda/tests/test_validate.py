import pandas as pd
from src.validate import validate_sales

def test_validate_sales():
    df = pd.DataFrame({
        "date": ["2023-01-01"],
        "product_id": [101],
        "product_name": ["Apple"],
        "sales": [120],
        "quantity": [10],
        "store_id": [1]
    })

    assert validate_sales(df) is True
