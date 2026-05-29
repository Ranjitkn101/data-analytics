import pandas as pd

def summary_stats(df: pd.DataFrame):
    """Return basic summary statistics."""
    return df.describe(include="all")

def missing_values(df: pd.DataFrame):
    """Return missing value counts."""
    return df.isna().sum()
