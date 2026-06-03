# PySpark DataProc ETL Project

A small PySpark ETL pipeline that reads employee CSV data from Google Cloud Storage, cleans and casts the schema, and writes the result to BigQuery.

## Project structure

- `src/etl/` - main ETL script
- `data/` - sample data and input CSV
- `scripts/` - deployment and Dataproc helper scripts
- `docs/` - notes, commands, and setup details

## Prerequisites

- Python 3.8+ installed
- Google Cloud SDK installed and authenticated
- `gcloud` configured for project `iot-device-project`
- A Dataproc cluster with the BigQuery Spark connector available

## Installation

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate the environment:

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Running tests

Install the test dependencies and run the test suite with:

```bash
pytest
```

## Running the ETL pipeline

The main ETL script is located at `src/etl/employees_csv_to_bq.py`.

```bash
python src/etl/employees_csv_to_bq.py
```

> Note: The script is configured to read from `gs://pyspark_test11/employees/employees.csv` and write to BigQuery dataset `employee_dataset`.

## Dataproc cluster setup

Use the helper script in `scripts/dataproc_cluster_setup.sh` to create and delete a Dataproc cluster.

```bash
bash scripts/dataproc_cluster_setup.sh
```

## Testing

1. Confirm the source CSV file exists in GCS or use the sample local file in `data/emp.csv`.
2. Verify your GCP project and permissions are correct.
3. Run the ETL script locally or submit it through Dataproc.

## Notes

- Additional project notes are available in `docs/project_notes.md`.
- If you need the original shell notes, see `docs/original_dataproc_notes.sh` and `docs/original_notes.md`.
