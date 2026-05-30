# BigQuery Cloud Analytics

A Python-based data cleaning and validation pipeline for sales data with BigQuery cloud integration. This project processes raw sales data through a cleaning pipeline, validates the cleaned data, and can export to Google BigQuery for analytics.

## Features

- **Data Cleaning**: Normalize column names, handle missing values, remove duplicates, and type conversion
- **Data Validation**: Comprehensive validation rules for sales data integrity
- **CSV Processing**: Load and save CSV files locally
- **BigQuery Integration**: Query and write data to Google Cloud BigQuery
- **Containerized**: Docker support for consistent environments
- **Tested**: Full test suite with pytest

## Project Structure

```
.
├── Dockerfile                      # Docker container configuration
├── README.md                        # This file
├── requirements.txt                 # Python dependencies
├── run_cleaning.py                 # Main pipeline entry point
├── config/
│   └── settings.yaml               # Configuration settings
├── data/
│   ├── sales_raw_100.csv          # Sample raw sales data
│   ├── sales_clean.csv            # Cleaned output data
│   └── venv_test_sales_clean.csv  # Test output
├── sql/
│   ├── raw_to_cleansed.sql        # Raw to cleansed layer transformation
│   └── cleansed_to_curated.sql    # Cleansed to curated layer transformation
└── src/
    ├── __init__.py
    ├── clean.py                    # Data cleaning functions
    ├── utils.py                    # Utility functions (load/save CSV, BigQuery)
    └── validate.py                 # Data validation functions
└── tests/
    ├── __init__.py
    ├── test_clean.py              # Tests for clean.py
    └── test_validate.py           # Tests for validate.py
```

## Requirements

- Python 3.10+
- pip (for virtual environment setup)
- Docker (for containerized execution)
- Google Cloud credentials (for BigQuery functionality)

## Setup & Installation

### Option 1: Using Python Virtual Environment

1. **Create a virtual environment**:
   ```powershell
   python -m venv .venv
   ```

2. **Activate the virtual environment**:
   - **Windows (PowerShell)**:
     ```powershell
     (Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& .\.venv\Scripts\Activate.ps1)
     ```
   - **Windows (Command Prompt)**:
     ```cmd
     .venv\Scripts\activate.bat
     ```
   - **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Option 2: Using Docker

Docker handles all dependencies automatically. No local Python installation required beyond Docker itself.

## Usage

### Running the Pipeline Locally (venv)

```bash
python run_cleaning.py
```

This will:
1. Load raw sales data from `data/sales_raw_100.csv`
2. Apply cleaning transformations
3. Validate the cleaned data
4. Save cleaned output to `data/sales_clean.csv`

**Example output**:
```
Cleaning pipeline completed successfully.
```

### Running with Docker

Build the Docker image:
```powershell
docker build -t bigquery-cloud-analytics .
```

Run the container with data volume mount:
```powershell
docker run --rm -v ${PWD}/data:/app/data bigquery-cloud-analytics
```

This mounts your local `data/` directory to the container's `/app/data` directory, allowing the pipeline to access your CSV files.

## Testing

### Run All Tests

```bash
pytest -v
```

### Test Results (venv verified ✓)

All tests passing on Python 3.13.9 with pytest 9.0.3:

```
platform win32 -- Python 3.13.9, pytest-9.0.3, pluggy-1.6.0
rootdir: <workspace>
collected 3 items                                                                               

tests/test_clean.py::test_clean_sales_basic PASSED                                        [ 33%]
tests/test_validate.py::test_validate_sales_pass PASSED                                   [ 66%]
tests/test_validate.py::test_validate_sales_negative_amount PASSED                        [100%]

====================================== 3 passed in 0.65s =======================================
```

### Run Specific Tests

```bash
pytest tests/test_clean.py -v        # Test data cleaning
pytest tests/test_validate.py -v     # Test data validation
```

## Data Cleaning Pipeline

The `clean_sales()` function performs:

- **Column Normalization**: Convert column names to lowercase and strip whitespace
- **Order ID**: Convert to numeric, remove invalid/negative values, convert to int64
- **Customer ID**: Convert to string, strip whitespace, handle empty values
- **Amount**: Convert to numeric values
- **Quantity**: Convert to numeric values
- **Order Date**: Parse as datetime
- **Null Handling**: Drop rows missing critical fields (order_id, customer_id, amount, quantity, order_date)
- **Deduplication**: Remove duplicate rows

## BigQuery Integration

### Prerequisites

1. Set up Google Cloud credentials:
   ```bash
   gcloud auth application-default login
   ```

2. Set the active project:
   ```bash
   gcloud config set project pro-bigquery-cloud-analytics
   ```

3. Ensure required Google Cloud services are enabled:
   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable artifactregistry.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable bigquery.googleapis.com
   gcloud services enable storage.googleapis.com
   gcloud services enable cloudscheduler.googleapis.com
   ```

### Load raw data into BigQuery

1. Create a GCS bucket for raw data:
   ```bash
   gsutil mb -l europe-west2 gs://bkt_bigquery-cloud-analytics
   ```

2. Upload the raw CSV file:
   ```bash
   gsutil cp data/sales_raw_100.csv gs://bkt_bigquery-cloud-analytics/raw/
   ```

3. Create the BigQuery dataset:
   ```bash
   bq --location=europe-west2 mk ds_bigquery_cloud_analytics
   ```

4. Load the raw data into BigQuery:
   ```bash
   bq load --autodetect --source_format=CSV ds_bigquery_cloud_analytics.sales_raw gs://bkt_bigquery-cloud-analytics/raw/sales_raw_100.csv
   ```

### Run SQL transformations

Transform raw data into the cleansed layer:
```bash
bq query --use_legacy_sql=false < sql/raw_to_cleansed.sql
```

Transform cleansed data into the curated layer:
```bash
bq query --use_legacy_sql=false < sql/cleansed_to_curated.sql
```

### Usage Examples

Load data from BigQuery:
```python
from src.utils import load_from_bigquery

query = "SELECT * FROM `pro-bigquery-cloud-analytics.ds_bigquery_cloud_analytics.sales_curated` LIMIT 100"
df = load_from_bigquery(query)
```

Write data to BigQuery:
```python
from src.utils import write_to_bigquery

write_to_bigquery(df, "pro-bigquery-cloud-analytics.ds_bigquery_cloud_analytics.sales_curated", if_exists="WRITE_TRUNCATE")
```

## Deploy to Cloud Run

1. Build and publish the Docker image to Artifact Registry:
   ```bash
   gcloud builds submit --tag europe-west2-docker.pkg.dev/pro-bigquery-cloud-analytics/analytics-repo/bigquery-cloud-analytics .
   ```

2. Deploy the container to Cloud Run:
   ```bash
   gcloud run deploy bigquery-cloud-analytics \
     --image europe-west2-docker.pkg.dev/pro-bigquery-cloud-analytics/analytics-repo/bigquery-cloud-analytics \
     --region europe-west2 \
     --platform managed \
     --allow-unauthenticated
   ```

3. If you use PowerShell, make sure the backslash continuation is valid or run each line separately.

## GCP Setup — Commands Executed (Verified)

I have executed the full GCP setup and verified each step for this project. The commands run successfully in `europe-west2` under the `pro-bigquery-cloud-analytics` project.

Run the following to reproduce the exact steps I executed:

```bash
# Prepare your GCP project and enable services
gcloud config set project pro-bigquery-cloud-analytics
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable bigquery.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable cloudscheduler.googleapis.com

# Create the raw data bucket in GCS and upload sample CSV
gsutil mb -l europe-west2 gs://bkt_bigquery-cloud-analytics
gsutil cp data/sales_raw_100.csv gs://bkt_bigquery-cloud-analytics/raw/

# Create BigQuery dataset and load raw table
bq --location=europe-west2 mk ds_bigquery_cloud_analytics
bq load --autodetect --source_format=CSV ds_bigquery_cloud_analytics.sales_raw gs://bkt_bigquery-cloud-analytics/raw/sales_raw_100.csv

# Execute SQL transformations
bq query --use_legacy_sql=false < sql/raw_to_cleansed.sql
bq query --use_legacy_sql=false < sql/cleansed_to_curated.sql

# Build and deploy Docker image to Cloud Run (Artifact Registry)
gcloud builds submit --tag europe-west2-docker.pkg.dev/pro-bigquery-cloud-analytics/analytics-repo/bigquery-cloud-analytics .
gcloud run deploy bigquery-cloud-analytics \
   --image europe-west2-docker.pkg.dev/pro-bigquery-cloud-analytics/analytics-repo/bigquery-cloud-analytics \
   --region europe-west2 \
   --platform managed \
   --allow-unauthenticated
```

Outcome: GCS bucket created, raw CSV uploaded, BigQuery dataset and `sales_raw` table loaded, `raw_to_cleansed` and `cleansed_to_curated` transformations executed, Docker image published and Cloud Run service deployed.

## Environment Verification

### venv Testing Status: ✅ VERIFIED
- **Python Version**: 3.13.9
- **pytest Version**: 9.0.3
- **Test Count**: 3
- **Test Status**: All PASSED (0.65s)
- **Platform**: Windows

### Local run (venv) — `run_cleaning.py`

I ran the cleaning pipeline locally inside the project's virtual environment using `python run_cleaning.py`. It executed successfully and produced the cleaned CSV at `data/sales_clean.csv`.

Reproduce locally (from project root):

```powershell
# activate venv (PowerShell)
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& .\.venv\Scripts\Activate.ps1)
python run_cleaning.py
```

Example output printed on success:

```
Cleaning pipeline completed successfully.
```

The cleaned file was written to: [data/sales_clean.csv](data/sales_clean.csv)

### BigQuery result snapshot (verified)

I queried the `sales_curated` table in BigQuery and verified the curated results. Below is a small sample snapshot from the table (first 10 rows shown):

| order_id | customer_id | amount | quantity | order_date  | total_order_value | order_month |
|---------:|:------------|-------:|---------:|:------------|------------------:|:-----------:|
| 1061     | C001        | 250.0  | 1        | 2024-03-01  | 250.0             | 2024-03     |
| 1091     | C001        | 325.0  | 1        | 2024-03-31  | 325.0             | 2024-03     |
| 1031     | C001        | 175.0  | 1        | 2024-01-31  | 175.0             | 2024-01     |
| 1001     | C001        | 100.0  | 1        | 2024-01-01  | 100.0             | 2024-01     |
| 1066     | C006        | 262.5  | 1        | 2024-03-06  | 262.5             | 2024-03     |

Full curated table: `pro-bigquery-cloud-analytics.ds_bigquery_cloud_analytics.sales_curated`

### Docker Testing Status: ✅ VERIFIED
- **Base Image**: python:3.10-slim
- **Build**: Successful
- **Execution**: Successful
- **Data Mounting**: Working (data/ directory accessible in container)

## Troubleshooting

### Virtual Environment Issues

- **PowerShell execution policy error**: Run the activation command with the execution policy flag as shown above
- **Module not found**: Ensure virtual environment is activated and `pip install -r requirements.txt` was run
- **Python version mismatch**: Project tested on Python 3.13.9, but 3.10+ should work

### Docker Issues

- **Permission denied**: On Linux/macOS, ensure Docker daemon is running
- **Volume mounting issues**: Use absolute paths or `${PWD}` for cross-platform compatibility
- **BigQuery credentials**: Mount your `.config/gcloud/` directory with credentials

### Data Issues

- **CSV format**: Ensure CSV files have headers and are UTF-8 encoded
- **Missing columns**: Required columns: order_id, customer_id, amount, quantity, order_date
- **Data types**: The cleaning pipeline automatically handles type conversions

## SQL Transformations

The `sql/` directory contains transformation scripts for multi-layer data processing:

- **raw_to_cleansed.sql**: Transforms raw data to cleansed layer with data quality rules
- **cleansed_to_curated.sql**: Transforms cleansed data to curated layer for analytics

These can be executed as BigQuery scheduled queries or manually as needed.

## Dependencies

See [requirements.txt](requirements.txt) for the full list:

- **pandas**: Data manipulation and CSV processing
- **google-cloud-bigquery**: Google Cloud BigQuery integration
- **pyarrow**: Data serialization for BigQuery
- **pytest**: Testing framework
- **python-dotenv**: Environment variable management

## License

This project is part of the BigQuery Cloud Analytics suite.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review test output with `pytest -v`
3. Verify data format matches expected schema
4. Ensure Google Cloud credentials are properly configured
