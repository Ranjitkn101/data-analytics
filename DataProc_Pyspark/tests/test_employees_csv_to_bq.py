import pytest
from pyspark.sql import SparkSession

from src.etl.employees_csv_to_bq import create_spark_session, rename_columns, clean_dataframe


def test_create_spark_session():
    spark = create_spark_session("test-spark-session")
    assert spark is not None
    spark.stop()


def test_rename_columns():
    spark = SparkSession.builder.master("local[1]").appName("test-rename-columns").getOrCreate()
    df = spark.createDataFrame(
        [(101, "Ranjit", "Nayak", "Engineering", 75000, "2020-04-12")],
        ["col1", "col2", "col3", "col4", "col5", "col6"]
    )

    renamed = rename_columns(df)
    assert renamed.columns == [
        "emp_id",
        "first_name",
        "last_name",
        "department",
        "salary",
        "join_date"
    ]
    spark.stop()


def test_clean_dataframe():
    spark = SparkSession.builder.master("local[1]").appName("test-clean-dataframe").getOrCreate()
    df = spark.createDataFrame([
        ("101", "Ranjit", "Nayak", "Engineering", "75000", "2020-04-12")
    ], ["emp_id", "first_name", "last_name", "department", "salary", "join_date"])

    cleaned = clean_dataframe(df)
    types = dict(cleaned.dtypes)

    assert types["emp_id"] == "int"
    assert types["salary"] == "int"
    assert types["join_date"] == "date"
    assert cleaned.collect()[0]["emp_id"] == 101
    spark.stop()
