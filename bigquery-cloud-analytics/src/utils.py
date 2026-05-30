import pandas as pd
from google.cloud import bigquery

def load_csv(path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(path)
    except Exception as e:
        raise RuntimeError(f"Failed to load CSV: {e}")

def save_csv(df: pd.DataFrame, path: str):
    df.to_csv(path, index=False)

def load_from_bigquery(query: str) -> pd.DataFrame:
    client = bigquery.Client()
    return client.query(query).to_dataframe()

def write_to_bigquery(df: pd.DataFrame, table_id: str, if_exists: str = "WRITE_TRUNCATE"):
    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(write_disposition=if_exists)
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()
