import pandas as pd

def clean_sales(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Normalize column names
    df.columns = df.columns.str.lower().str.strip()

    # Convert order_id → numeric, drop invalid/negative
    df["order_id"] = pd.to_numeric(df["order_id"], errors="coerce")
    df = df[df["order_id"] > 0]

    # Convert order_id to integer (fixes the .0 issue)
    df["order_id"] = df["order_id"].astype("int64")

    # Customer ID → string, cleaned
    df["customer_id"] = (
        df["customer_id"]
        .astype("string")
        .str.strip()
        .replace({"": pd.NA})
    )

    # Amount → numeric
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # Quantity → numeric
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    # Order date → datetime
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    # Drop rows missing critical fields
    df = df.dropna(subset=["order_id", "customer_id", "amount", "quantity", "order_date"])

    # Remove duplicates
    df = df.drop_duplicates()

    return df
