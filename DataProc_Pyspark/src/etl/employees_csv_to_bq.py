"""
ETL: Load CSV from GCS → Clean & Transform → Write to BigQuery
Author: Ranjit
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.utils import AnalysisException
import sys


# ---------------------------------------------------------
# 1. Create Spark Session
# ---------------------------------------------------------
def create_spark_session(app_name: str):
    return SparkSession.builder.appName(app_name).getOrCreate()


# ---------------------------------------------------------
# 2. Read CSV from GCS
# ---------------------------------------------------------
def read_csv_from_gcs(spark, input_path: str):
    print(f"Reading CSV from: {input_path}")

    try:
        df = (
            spark.read
                .option("header", "true")
                .option("inferSchema", "true")
                .csv(input_path)
        )
        print("CSV read successfully")
        return df

    except Exception as e:
        print("ERROR: Failed to read CSV")
        print(e)
        sys.exit(1)


# ---------------------------------------------------------
# 3. Rename columns (if header missing or inconsistent)
# ---------------------------------------------------------
def rename_columns(df):
    expected_cols = [
        "emp_id",
        "first_name",
        "last_name",
        "department",
        "salary",
        "join_date"
    ]

    print("Renaming columns to standard schema...")
    return df.toDF(*expected_cols)


# ---------------------------------------------------------
# 4. Clean & cast schema
# ---------------------------------------------------------
def clean_dataframe(df):
    print("Casting columns to correct data types...")

    df_clean = (
        df.withColumn("emp_id", col("emp_id").cast("integer"))
          .withColumn("first_name", col("first_name").cast("string"))
          .withColumn("last_name", col("last_name").cast("string"))
          .withColumn("department", col("department").cast("string"))
          .withColumn("salary", col("salary").cast("integer"))
          .withColumn("join_date", col("join_date").cast("date"))
    )

    return df_clean


# ---------------------------------------------------------
# 5. Write to BigQuery
# ---------------------------------------------------------
def write_to_bigquery(df, project_id, dataset, table):
    table_ref = f"{project_id}:{dataset}.{table}"
    print(f"Writing to BigQuery table: {table_ref}")

    try:
        (
            df.write
              .format("bigquery")
              .option("table", table_ref)
              .option("writeMethod", "direct")
              .mode("append")
              .save()
        )
        print("SUCCESS: Data written to BigQuery")

    except AnalysisException as e:
        print("ERROR: BigQuery write failed")
        print(e)
        sys.exit(1)


# ---------------------------------------------------------
# 6. Main ETL Pipeline
# ---------------------------------------------------------
def main():
    spark = create_spark_session("LoadCSVtoBigQuery")

    input_path = "gs://pyspark_test11/employees/employees.csv"
    project_id = "iot-device-project"
    dataset = "employee_dataset"
    table = "employees"

    df = read_csv_from_gcs(spark, input_path)

    print("Initial Schema:")
    df.printSchema()

    df = rename_columns(df)
    df_clean = clean_dataframe(df)

    print("Cleaned Schema:")
    df_clean.printSchema()

    write_to_bigquery(df_clean, project_id, dataset, table)

    print("ETL Pipeline Completed Successfully")


# ---------------------------------------------------------
# Run script
# ---------------------------------------------------------
if __name__ == "__main__":
    main()
