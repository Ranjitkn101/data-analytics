import pandas as pd

def validate_sales(df: pd.DataFrame):
    if df["amount"].isna().any():
        raise ValueError("Amount column contains nulls after cleaning.")
    if (df["amount"] < 0).any():
        raise ValueError("Amount column contains negative values.")
    if df["order_id"].duplicated().any():
        raise ValueError("Duplicate order_id found.")
