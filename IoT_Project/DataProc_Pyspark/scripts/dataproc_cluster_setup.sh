#!/bin/bash

# Dataproc cluster create/delete helper for the PySpark ETL project.
# Update CLUSTER_NAME and REGION before running.

CLUSTER_NAME="my-cluster-demo1"
REGION="us-east1"

# Create a Dataproc cluster with the BigQuery Spark connector.
gcloud dataproc clusters create "$CLUSTER_NAME" \
  --region="$REGION" \
  --num-workers=2 \
  --worker-machine-type=n1-standard-2 \
  --worker-boot-disk-size=50 \
  --master-machine-type=n1-standard-2 \
  --master-boot-disk-size=50 \
  --image-version=2.0-debian10 \
  --enable-component-gateway \
  --optional-components=JUPYTER \
  --properties=spark:spark.jars.packages=com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.36.1

# Delete the Dataproc cluster if required.
gcloud dataproc clusters delete "$CLUSTER_NAME" \
  --region="$REGION" \
  --quiet
