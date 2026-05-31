# Project Notes

This document captures notes from the original project files for the PySpark ETL pipeline.

## Data sample

CSV header:

```
emp_id,first_name,last_name,department,salary,join_date
```

Example rows:

```
101,Ranjit,Nayak,Engineering,75000,2020-04-12
102,Pragnya,Nayak,Finance,68000,2021-01-18
103,Arjun,Patel,Marketing,72000,2019-11-03
104,Meera,Sharma,Engineering,80000,2022-06-25
105,David,Lee,HR,65000,2020-09-14
```

## Google Cloud setup notes

- Bucket path used by code: `gs://pyspark_test11/employees/employees.csv`
- BigQuery dataset: `employee_dataset`
- BigQuery table: `employees`
- Project ID: `iot-device-project`

## Permissions needed

- `roles/dataproc.worker` for the Dataproc service account
- `BigQuery Data Editor` for write access to BigQuery
- `BigQuery Job User` to run load jobs
- `Storage Object Viewer` or `Storage Object Admin` for GCS read access

## Useful commands

Check bucket contents:

```bash
gsutil ls gs://pyspark_test11/employees/employees.csv
```

Create BigQuery dataset and table:

```bash
bq mk --location=us-east1 employee_dataset
bq mk --table employee_dataset.employees \
  emp_id:INTEGER,first_name:STRING,last_name:STRING,department:STRING,salary:INTEGER,join_date:DATE
```

Copy script to GCS for Dataproc submit:

```bash
gsutil cp employees_csv_to_bq.py gs://pyspark_test11/code/scripts/
```

Submit the PySpark job:

```bash
gcloud dataproc jobs submit pyspark gs://pyspark_test11/code/scripts/employees_csv_to_bq.py \
  --cluster=my-cluster-demo1 \
  --region=us-east1
```
