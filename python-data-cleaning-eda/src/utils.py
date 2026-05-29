import pandas as pd

def load_csv(path: str) -> pd.DataFrame:
    """Load CSV with basic error handling."""
    try:
        return pd.read_csv(path)
    except Exception as e:
        raise RuntimeError(f"Failed to load CSV: {e}")

def save_csv(df: pd.DataFrame, path: str):
    """Save cleaned CSV."""
    df.to_csv(path, index=False)
