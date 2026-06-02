gcloud services enable servicenetworking.googleapis.com

gcloud compute addresses create google-managed-services-iot-device-project \
    --global \
    --purpose=VPC_PEERING \
    --prefix-length=16 \
    --network=default

gcloud services vpc-peerings connect \
    --service=servicenetworking.googleapis.com \
    --network=default \
    --ranges=google-managed-services-iot-device-project


gcloud sql instances create balajee-postgres \
    --edition=ENTERPRISE \
    --database-version=POSTGRES_18 \
    --tier=db-custom-2-8192 \
    --region=europe-west1 \
    --storage-type=SSD \
    --storage-size=100 \
    --availability-type=zonal \
    --backup \
    --enable-point-in-time-recovery \
    --network=default \
    --assign-ip


-- Create posgress user

gcloud sql users create app_user \
    --instance=balajee-postgres \
    --password="StrongPassword123!"

gcloud sql users set-password postgres \
    --instance=balajee-postgres \
    --password="postgres123"
	
gcloud sql users create myusername \
    --instance=balajee-postgres \
    --password="Myusername123!"



#-- drop instance 
#gcloud sql instances delete balajee-postgres --quiet


#create a DB from cloud shell IAM provision (we could do this or superuser(postgres))

gcloud sql databases create mydb \
    --instance=balajee-postgres

#superuser(postgres))
# below proxy or connect to other user steps is required when i need to connect laptop to db connection using GUI

wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud-sql-proxy

chmod +x cloud-sql-proxy

./cloud-sql-proxy \
  -instances=iot-device-project:europe-west1:balajee-postgres=tcp:5432


#the result should - Listening on 127.0.0.1:5432 for iot-device-project:europe-west1:balajee-postgres

#Open a NEW Cloud Shell tab and connect as superuser

psql -h 127.0.0.1 -U postgres -d postgres

# enter password postgres123

CREATE DATABASE mydb_iot;

CREATE USER app_user WITH PASSWORD 'StrongPassword123!';

GRANT CONNECT ON DATABASE mydb_iot TO app_user;

\c mydb_iot

GRANT USAGE ON SCHEMA public TO app_user;
GRANT CREATE ON SCHEMA public TO app_user;

#Optional
GRANT ALL PRIVILEGES ON DATABASE mydb_iot TO app_user;

#open another shell
psql -h 127.0.0.1 -U app_user -d mydb_iot

CREATE TABLE test(id INT);





--- use UI to connect Postgress # below steps is required when i need to connect laptop to db connection using GUI

# Download 
https://sql-workbench.eu/dev-download.html # Workbench-Build132.5

https://github.com/GoogleCloudPlatform/cloud-sql-proxy/releases   #cloud_sql_proxy_x64.exe rename to cloud-sql-proxy.exe


C:\D_Drive_Study\IoT_Project\cloudsql\cloud-sql-proxy.exe iot-device-project:europe-west1:balajee-postgres --port=5432

# C:\Users\<yourname>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup  <-- Place the .bat file in: Make it auto‑start with Windows


#Prod 
sudo systemctl enable cloud-sql-proxy
sudo systemctl start cloud-sql-proxy



#==================== Now creating a source database 

1. Create a VM in GCP (Linux recommended)
You’ll create a small VM that acts like your “on‑prem server”.

Steps
Go to Compute Engine → VM Instances

Click Create Instance

Choose:

Name: onprem‑pg

Region: europe‑west1

Machine type: e2‑micro (free tier)

OS: Ubuntu 22.04 LTS

Allow:

✔ HTTP (optional)

✔ HTTPS (optional)

Create the VM.

This VM will act as your source PostgreSQL server.


#SSH
sudo apt update
sudo apt install postgresql postgresql-contrib -y

sudo systemctl start postgresql
sudo systemctl enable postgresql

sudo -i -u postgres

createdb mydb_sr

psql -c "CREATE USER sr_user WITH PASSWORD 'app123';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE mydb_sr TO sr_user;"


psql mydb_sr -c "CREATE TABLE sensor_data (
    sensor_id      INT,
    device_name    VARCHAR(50),
    temperature    DECIMAL(5,2),
    humidity       DECIMAL(5,2),
    reading_time   TIMESTAMP
);"



psql mydb_sr -c "INSERT INTO sensor_data VALUES
(1, 'device_A', 22.5, 45.2, '2026-05-16 10:00:00'),
(2, 'device_B', 23.1, 47.8, '2026-05-16 10:05:00'),
(3, 'device_C', 21.9, 44.0, '2026-05-16 10:10:00'),
(4, 'device_A', 22.8, 46.1, '2026-05-16 10:15:00'),
(5, 'device_B', 23.4, 48.3, '2026-05-16 10:20:00'),
(6, 'device_C', 21.7, 43.9, '2026-05-16 10:25:00'),
(7, 'device_A', 22.6, 45.7, '2026-05-16 10:30:00'),
(8, 'device_B', 23.0, 47.5, '2026-05-16 10:35:00'),
(9, 'device_C', 21.8, 44.3, '2026-05-16 10:40:00'),
(10, 'device_A', 22.9, 46.4, '2026-05-16 10:45:00');"


#interactive 
psql mydb_sr or  psql mydb_sr -c "SELECT * FROM sensor_data;"


pg_dump -U postgres mydb_sr > mydb_sr.sql

# improt

Option A — Upload via Cloud Console
Go to Cloud SQL → Import

Upload mydb_sr.sql

Choose your Cloud SQL instance

Choose database: mydb_sr

Click Import

Option B — Use gcloud
Upload the file to Cloud Storage:

Code
gsutil cp mydb_sr.sql gs://your-bucket/
Then import:

Code
gcloud sql import sql balajee-postgres gs://your-bucket/mydb_sr.sql --database=mydb_sr



#create a dump
pg_dump -U postgres mydb_sr > mydb_sr.sql # restriction to import in other user
# create using no 
pg_dump -U postgres --no-owner --no-privileges mydb_sr > mydb_sr1.sql

gcloud auth login
gsutil cp mydb_sr.sql gs://postgres-bkt1/ 
or
gsutil cp /var/lib/postgresql/mydb_sr.sql gs://YOUR_BUCKET_NAME/



4/0AeoWuM8pKL5eh2NNHcmkPm2XILLpMtmjWK1mtO8SuDma5SS_ftFLwTplvkEw9SSeUUT_qw