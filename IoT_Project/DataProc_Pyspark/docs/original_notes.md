project-root/
│
├── etl/
│   ├── employees/
│   │   ├── etl_employees_csv_to_bq.py
│   │   ├── etl_employees_json_to_bq.py
│   │   ├── etl_employees_api_to_bq.py
│   │   └── schema_employees.py
│   │
│   ├── utils/
│   │   ├── spark_session.py
│   │   ├── gcs_reader.py
│   │   ├── bq_writer.py
│   │   └── schema_utils.py
│   │
│   └── config/
│       └── settings.yaml
│
├── jobs/
│   ├── run_employees_csv.sh
│   ├── run_employees_json.sh
│   └── run_all.sh
│
└── README.md




emp_id,first_name,last_name,department,salary,join_date
101,Ranjit,Nayak,Engineering,75000,2020-04-12
102,Pragnya,Nayak,Finance,68000,2021-01-18
103,Arjun,Patel,Marketing,72000,2019-11-03
104,Meera,Sharma,Engineering,80000,2022-06-25
105,David,Lee,HR,65000,2020-09-14


gs://pyspark_test11/employees/emp.csv


bq mk --location=us-east1 employee_dataset

bq mk --table employee_dataset.employees ^
emp_id:INTEGER,first_name:STRING,last_name:STRING,department:STRING,salary:INTEGER,join_date:DATE


-- check the service account  Storage Object Viewer (read-only) or Storage Object Admin (read/write) - asingged the service account to bucket

gsutil ls gs://pyspark_test11/employees/employees.csv



These permisions - > BigQuery Data Editor : Allows insert/update/delete. --BigQuery Job User ; Allows Spark to run load jobs.-- BigQuery Data Viewer


#C:\Users\ranji\GCP_Code\Python_practice\Pyspark>gsutil cp employees_csv_to_bq.py gs://pyspark_test11/code/scripts/
gsutil cp employees_csv_to_bq.py gs://pyspark_test11/code/scripts/


submit spark job 

gcloud dataproc jobs submit pyspark gs://pyspark_test11/code/scripts/employees_csv_to_bq.py ^
  --cluster=my-cluster-demo1 ^
  --region=us-east1 
 
# --jars=gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.36.1.jar
  

