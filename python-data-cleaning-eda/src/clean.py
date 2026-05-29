import pandas as pd

def clean_sales(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw sales data:
    - Standardize date formats
    - Remove invalid dates
    - Convert numeric fields
    - Remove negative or missing values
    - Drop duplicates
    """

    # Drop duplicates
    df = df.drop_duplicates()

    # Fix date formats
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Remove invalid dates
    df = df.dropna(subset=["date"])

    # Convert numeric fields
    df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["store_id"] = pd.to_numeric(df["store_id"], errors="coerce")

    # Remove negative or missing values
    df = df[df["sales"] >= 0]
    df = df.dropna(subset=["sales", "quantity", "store_id", "product_name"])

    return df
