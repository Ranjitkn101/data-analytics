#!/bin/bash

# Variables
CLUSTER_NAME="my-cluster-demo1"
REGION="us-east1"

# Create Dataproc Cluster
-- window run 

set CLUSTER_NAME=my-cluster-demo1
set REGION=us-east1

gcloud dataproc clusters create %CLUSTER_NAME% ^
  --region=%REGION% ^
  --num-workers=2 ^
  --worker-machine-type=n1-standard-2 ^
  --worker-boot-disk-size=50 ^
  --master-machine-type=n1-standard-2 ^
  --master-boot-disk-size=50 ^
  --image-version=2.0-debian10 ^
  --enable-component-gateway ^
  --optional-components=JUPYTER ^
 
OLD  --initialization-actions=gs://goog-dataproc-initialization-actions-%REGION%/connectors/connectors.sh ^ #
  --metadata=bigquery-connector-version=1.2.0 ^
  --metadata=spark-bigquery-connector-version=0.21.0
  
 -- MODIFIED CODE
 
set CLUSTER_NAME=my-cluster-demo1
set REGION=us-east1

 gcloud dataproc clusters delete %CLUSTER_NAME% ^
  --region=us-east1 ^
  --quiet


 gcloud dataproc clusters create %CLUSTER_NAME% ^
  --region=%REGION% ^
  --num-workers=2 ^
  --worker-machine-type=n1-standard-2 ^
  --worker-boot-disk-size=50 ^
  --master-machine-type=n1-standard-2 ^
  --master-boot-disk-size=50 ^
  --image-version=2.0-debian10 ^
  --enable-component-gateway ^
  --optional-components=JUPYTER ^
  --properties=spark:spark.jars.packages=com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.36.1


#one more midification
#  --properties=spark:spark.jars.packages=com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.36.1

gcloud dataproc clusters create my-cluster-demo1 ^
  --region=us-east1 ^
  --zone=us-east1-c ^
  --subnet=default ^
  --num-workers=2 ^
  --worker-machine-type=n1-standard-2 ^
  --master-machine-type=n1-standard-4 ^
  --enable-component-gateway ^
  --optional-components=JUPYTER





Go to IAM 
827160918241-compute@developer.gserviceaccount.com --> add role dataproc.worker

or

gcloud auth login
gcloud config set project iot-device-project


gcloud projects add-iam-policy-binding iot-device-project ^
  --member="serviceAccount:827160918241-compute@developer.gserviceaccount.com" ^
  --role="roles/dataproc.worker"
  
