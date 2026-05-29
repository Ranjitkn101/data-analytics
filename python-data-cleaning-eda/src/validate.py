def validate_sales(df):
    """
    Validate cleaned sales data:
    - Required columns exist
    - No negative values
    - No missing critical fields
    """

    required_cols = ["date", "product_id", "product_name", "sales", "quantity", "store_id"]

    for col in required_cols:
        if col not in df.columns:
            raise AssertionError(f"Missing required column: {col}")

    if df["sales"].min() < 0:
        raise AssertionError("Negative sales found")

    if df["quantity"].min() < 0:
        raise AssertionError("Negative quantity found")

    if df.isna().sum().sum() > 0:
        raise AssertionError("Null values found in cleaned dataset")

    return True
