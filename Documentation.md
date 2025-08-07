# Data-Engineering.

Credit Scoring, Lending, Fraud Alerts and Risk Management Project

💳 Credit Scoring, Lending & Fraud Detection Platform

A real-time, scalable data engineering project for credit risk analysis, fraud alerting, and lending decisions using modern big data tools.

🚀 Features

- Real-time credit application ingestion via *Kafka*
- Fraud detection using *Flink*
- Risk scoring using *Spark*
- Data storage in *PostgreSQL* and *MongoDB*
- Dashboarding via *Power BI*
- Monitoring via *Prometheus* and *Grafana*
- Packaged using *Docker Compose*


🏗️ Architecture Diagram (Text View)

                    ┌────────────────────┐
                    │  Kafka Producer    │
                    │ (Loan Applications)│
                    └────────┬───────────┘
                             │
                             ▼
              ┌─────────────────────────────┐
              │ Kafka Topic: credit_apps    │
              └────────┬────────────┬───────┘
                       │            │
                       ▼            ▼
        ┌─────────────────┐     ┌───────────────────┐
        │ Flink Stream Job│     │ Spark Batch Job   │
        │ Fraud Detection │     │ Risk Scoring      │
        └───────┬─────────┘     └──────┬────────────┘
                │                      │
                ▼                      ▼
     ┌──────────────────────┐   ┌──────────────────────┐
     │ MongoDB(Fraud Alerts)│   │ PostgreSQL (Data WH) │◀────┐
     └──────────────────────┘   └──────────────────────┘     │
                │                        │                   │
                └────────────┬───────────┘                   │
                             ▼                               │
                  ┌─────────────────────────────┐            │
                  │   Power BI Dashboard        │ ◀─────────┘
                  │ Risk, Lending,Fraud Insights│
                  └─────────────────────────────┘          
ETL Diagram

        ┌──────────────┐      ┌──────────────┐
        │  MongoDB     │      │ PostgreSQL   │
        │ (fraud data) │      │ (loan data)  │
        └──────┬───────┘      └──────┬───────┘
               │                     │
     ┌─────────▼────────┐  ┌────────▼────────┐
     │ extract_mongo.py │  │ extract_postgres│
     └─────────┬────────┘  └────────┬────────┘
               └────────┬───────────┘
                        ▼
                ┌────────────┐
                │ transform  │
                │  .py       │
                └────┬───────┘
                     ▼
              ┌──────────────┐
              │ load_to_dw   │
              └────┬─────────┘
                   ▼
     ┌────────────────────────────┐
     │ PostgreSQL Data Warehouse  │
     └────────────┬───────────────┘
                  ▼
        ┌────────────────────┐
        │ Power BI / Grafana │
        └────────────────────┘
        
ETL Pipeline Summary

1. Extract
   - Pulls fraud data from MongoDB
   - Pulls loan data from PostgreSQL

2. Transform
   - Cleans, joins, and enriches the data
   - Flags fraud and assigns risk levels

3. Load
   - Loads the final dataset into a PostgreSQL Data Warehouse

4. Visualize
   - Dashboards in Power BI / Grafana for insights

> Enables real-time analytics for credit scoring, lending, and fraud detection.
        
Pipeline Design Summary:

- Ingestion: Kafka Producer streams new loan applications.
- Streaming Layer: Flink processes applications in real-time and flags fraud.
- Batch Layer: Spark calculates risk scores periodically and writes to the data warehouse.
- Storage:
  - MongoDB for fast storage of fraud alerts.
  - PostgreSQL acts as the central data warehouse.
- Reporting Layer: Power BI pulls data from PostgreSQL for business intelligence.

 ETL Pipeline Diagram

MongoDB ──▶ extract_mongo.py
                        │
PostgreSQL ─▶ extract_postgres.py
                        ▼
              🔄 transform.py
                        ▼
              📥 load_to_dw.py
                        ▼
     PostgreSQL Data Warehouse
                        ▼
             📊 Power BI Dashboard

⚙️ Step-by-Step Breakdown

1. 🔌 extract/extract_mongo.py

python
from pymongo import MongoClient
import pandas as pd

def extract_from_mongo():
    client = MongoClient("mongodb://localhost:27017")
    db = client.fraud_detection
    collection = db.fraud_alerts
    data = list(collection.find())
    return pd.DataFrame(data)

2. 🗃️ extract/extract_postgres.py

python
import pandas as pd
from sqlalchemy import create_engine

def extract_from_postgres():
    engine = create_engine("postgresql://postgres:admin@localhost:5432/creditdb")
    query = "SELECT * FROM credit_scores"
    df = pd.read_sql(query, engine)
    return df

3. 🔄 transform/transform.py

python
def transform_data(loans_df, alerts_df):
    # Join data on application_id
    merged_df = loans_df.merge(alerts_df, on='application_id', how='left', suffixes=('', '_fraud'))
    merged_df['is_fraud'] = merged_df['reason'].notnull()
    return merged_df[['application_id', 'user_id', 'credit_score', 'loan_amount', 'risk_level', 'is_fraud']]

4. 📥 load/load_to_dw.py

python
def load_to_data_warehouse(df):
    from sqlalchemy import create_engine
    engine = create_engine("postgresql://postgres:admin@localhost:5432/dw_finance")
    df.to_sql("fact_loan_application", engine, if_exists="append", index=False)

5. 🚀 run_etl.py

python
from extract.extract_mongo import extract_from_mongo
from extract.extract_postgres import extract_from_postgres
from transform.transform import transform_data
from load.load_to_dw import load_to_data_warehouse

mongo_df = extract_from_mongo()
postgres_df = extract_from_postgres()
transformed_df = transform_data(postgres_df, mongo_df)
load_to_data_warehouse(transformed_df)

✅ Result

- Combines relational & document data
- Enriches risk records with fraud info
- Loads into star schema data warehouse

Datawarehouse Model

A Star Schema is used to support analytics for credit scoring, risk, and fraud detection.


🌟 Fact Table

fact_loan_application

| Column              | Description                          |
|---------------------|--------------------------------------|
| application_id      | Unique loan application ID           |
| user_id             | Reference to user dimension          |
| time_id             | Reference to time dimension          |
| credit_score        | Numeric score from bureau            |
| loan_amount         | Loan requested                       |
| risk_level          | Derived risk category (Low/Med/High) |
| is_fraud            | Flag from fraud detection system     |
| approval_status     | Approved, Rejected, Under Review     |

📐 Dimension Tables

dim_user
| Column       | Description             |
|--------------|-------------------------|
| user_id      | Primary key             |
| name         | (Optional for reporting)|
| age          | Age of applicant        |
| gender       | Gender                  |
| region       | Location info           |

dim_time
| Column      | Description             |
|-------------|-------------------------|
| time_id     | Surrogate key           |
| date        | Actual date             |
| month       | Month name              |
| quarter     | Q1–Q4                   |
| year        | Calendar year           |

dim_risk
| Column       | Description             |
|--------------|-------------------------|
| risk_level   | Low, Medium, High       |
| description  | Risk interpretation     |

dim_status
| Column         | Description           |
|----------------|-----------------------|
| status_code    | Approved, Rejected    |
| explanation    | Business meaning      |

SQL DDL scripts to create the data warehouse schema (star schema) for the credit scoring and lending project


📐 dim_user

sql
CREATE TABLE dim_user (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    region VARCHAR(50)
);



📅 dim_time

sql
CREATE TABLE dim_time (
    time_id SERIAL PRIMARY KEY,
    date DATE,
    month VARCHAR(15),
    quarter VARCHAR(5),
    year INT
);



⚠️ dim_risk

sql
CREATE TABLE dim_risk (
    risk_level VARCHAR(10) PRIMARY KEY,
    description TEXT
);



📄 dim_status

sql
CREATE TABLE dim_status (
    status_code VARCHAR(20) PRIMARY KEY,
    explanation TEXT
);


🌟 fact_loan_application

sql
CREATE TABLE fact_loan_application (
    application_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES dim_user(user_id),
    time_id INT REFERENCES dim_time(time_id),
    credit_score INT,
    loan_amount NUMERIC(12,2),
    risk_level VARCHAR(10) REFERENCES dim_risk(risk_level),
    is_fraud BOOLEAN,
    approval_status VARCHAR(20) REFERENCES dim_status(status_code)
);



 📂 Folder Structure

credit_scoring_project/
├── docker-compose.yml
├── ingestion/
│   └── kafka_producer.py
├── processing/
│   └── spark_jobs/
│       └── credit_scoring_job.py
├── storage/
│   ├── postgres_setup.sql
│   └── mongodb_setup.js
├── dashboards/
│   └── powerbi_reports/
│       └── credit_scoring_report.pbix
├── monitoring/
│   ├── prometheus.yml
│   └── grafana/
│       └── dashboards/
│           └── credit_dashboard.json
├── README.md
└── DOCUMENTATION.md

⚙️ Tech Stack

| Layer            | Tool               |
|------------------|--------------------|
| Ingestion        | Apache Kafka       |
| Streaming Engine | Apache Flink       |
| Batch Processing | Apache Spark       |
| Data Warehouse   | PostgreSQL         |
| Alert Storage    | MongoDB            |
| Dashboards       | Power BI           |
| Monitoring       | Prometheus, Grafana|
| Orchestration    | Docker Compose     |

🧑‍💻 Setup Instructions

1. Clone & Start
git clone https://github.com/lawithus/Data-Engineering..git

2. Setup Databases
psql -U postgres -f storage/postgres_setup.sql
mongo < storage/mongodb_setup.js

3. Run Kafka Producer
python ingestion/kafka_producer.py

4. Launch Spark Risk Job
spark-submit processing/spark_jobs/credit_scoring_job.py

⚙️ Components and Scripts

    Kafka Producer (Python) Simulates loan applications and streams to Kafka.

ingestion/kafka_producer.py python from kafka import KafkaProducer import json, time, random

producer = KafkaProducer( bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8') )

def generate_event(): return { "application_id": random.randint(1000, 9999), "user_id": random.randint(1, 100), "credit_score": random.randint(300, 850), "loan_amount": round(random.uniform(1000, 20000), 2), "timestamp": time.time() }

while True: data = generate_event() producer.send('credit_applications', value=data) print("Sent:", data) time.sleep(2)

    Flink Job (Pseudo) Detects fraud in real time.

Logic:

    If loan_amount > 15000 and credit_score < 450 → alert
    Result stored in MongoDB.

flink_jobs/fraud_detection.py python Pseudo-PyFlink if loan_amount > 15000 and credit_score < 450: emit_alert(application_id, reason="Risky transaction")

    Spark Job Calculates risk scores from Kafka or HDFS and writes to PostgreSQL.

processing/spark_jobs/credit_scoring_job.py python from pyspark.sql import SparkSession from pyspark.sql.functions import when

spark = SparkSession.builder.appName("CreditScoring").getOrCreate()

df = spark.read.json("hdfs://localhost:9000/kafka-data/credit_apps.json")

df = df.withColumn("risk_level", when(df.credit_score >= 700, "Low") .when(df.credit_score >= 500, "Medium" .otherwise("High"))

df.write.format("jdbc").option("url", "jdbc:postgresql://db:5432/creditdb")
.option("dbtable", "credit_scores")
.option("user", "postgres")
.option("password", "admin")
.mode("append").save()

    PostgreSQL Setup

storage/postgres_setup.sql sql CREATE TABLE credit_scores ( application_id INT, user_id INT, credit_score INT, loan_amount FLOAT, risk_level TEXT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP );

CREATE TABLE data_quality_issues ( record_id SERIAL, issue TEXT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP );

CREATE TABLE metadata_table ( job TEXT, source TEXT, target TEXT,

    Access Control: DB roles and service authentication
    Lineage: Metadata tracked in metadata_table
    Policies:
        Credit score ≥ 600 for low risk
        Loan amount ≤ $15,000 for instant approval
    Auditing: Logged via Kafka + Spark job logs


🧪 Generating Dummy Data

Use Python's Faker library to generate realistic dummy transaction data.

1. Install Dependencies

Ensure you have the necessary Python packages installed:
pip install faker pandas

2. Generate Dummy Data

Create a script named generate_dummy_data.py inside the data/ directory:

python
from faker import Faker
import pandas as pd
import uuid
import random

fake = Faker()
transactions = []

for _ in range(1000):
    transaction = {
        "transaction_id": str(uuid.uuid4()),
"user_id": str(uuid.uuid4()),
        "amount": round(random.uniform(10, 5000), 2),
        "timestamp": fake.iso8601(),
        "location": fake.city(),
        "merchant": fake.company(),
        "card_type": random.choice(["VISA", "MASTERCARD", "AMEX"]),
        "device_id": str(uuid.uuid4()),
        "credit_score": random.randint(300, 850),
        "risk_level": random.choice(["Low", "Medium", "High"]),
        "is_fraud": random.choice([True, False])
    }
    transactions.append(transaction)

df = pd.DataFrame(transactions)
df.to_csv("transactions.csv", index=False)


Run the script to generate the `transactions.csv` file:

python data/generate_dummy_data.py


⚙️ Setting Up the Environment

Use Docker Compose to set up the necessary services.

1. Docker Compose Configuration

Create a `docker-compose.yml` file in the root directory:

yaml
version: '3.8'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  kafka:
    image: confluentinc/cp-kafka
    depends_on: [zookeeper]
    ports: ["9092:9092"]
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  mongo:
image: mongo
    ports: ["27017:27017"]
    

  postgres:
    image: postgres
    environment:
      POSTGRES_DB: credit
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: yourpass
    ports: ["5432:5432"]


  grafana:
    image: grafana/grafana
    ports: ["3000:3000"]


Start the services:

docker-compose up -d

🚀 Running the Kafka Producer

The Kafka producer will read the dummy data and send it to the Kafka topic.

1. Kafka Producer Script

Create a script named `producer.py` inside the `src/kafka_producer/` directory:

python
from kafka import KafkaProducer
import json
import pandas as pd
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

df = pd.read_csv('data/transactions.csv')
for _, row in df.iterrows():
    message = row.to_dict()
    producer.send("transactions", message)
    print("Sent:", message)
    time.sleep(1)


Run the producer:

bash
python src/kafka_producer/producer.py

🔄 Apache Flink Job

The Flink job will process the data from Kafka, perform transformations, and detect fraud.

Note: Implement the Flink job in Java or Scala using the DataStream API. Due to the complexity, the full implementation is beyond this summary.


Processed data will be stored in MongoDB and PostgreSQL.

1. MongoDB Sink

Implement the MongoDB sink to store raw transactions.

2. PostgreSQL Sink

Implement the PostgreSQL sink to store processed transactions.

Ensure the PostgreSQL database has the necessary table:

sql
CREATE TABLE IF NOT EXISTS processed_transactions (
    transaction_id UUID PRIMARY KEY,
    user_id UUID,
    amount NUMERIC,
    timestamp TIMESTAMP,
    location TEXT,
    merchant TEXT,
    card_type TEXT,
    device_id UUID,
    credit_score NUMERIC,
    risk_level TEXT,
    is_fraud BOOLEAN
);


📊 Power BI Dashboard Setup (Step-by-Step)

✅ Prerequisites

- Power BI Desktop installed
- PostgreSQL running via Docker (localhost:5432)
- Processed transactions stored in PostgreSQL (from your transactions.csv or Flink job)

🔌 1. Connect Power BI to PostgreSQL

1. Open Power BI Desktop  
2. Click Home > Get Data > PostgreSQL database  
3. Set the connection:
   - Server: localhost
   - Database: credit
4. Click Advanced Options and paste:
   sql
   SELECT * FROM processed_transactions;
   
5. Click OK and load the data.

📈 2. Create Visuals

Use the following fields to create …
| Line Graph         | timestamp vs. amount                           | Trends over time                 |
| Map (if available) | location (use Geo table if needed)             | Regional fraud activity          |
| Table              | All fields                                     | Detailed record view             |
| Gauge              | Average credit_score                           | Customer score average           |
| Donut              | is_fraud count (True/False)                    | Fraud vs. normal distribution    |


🎨 3. Formatting Tips

- Add slicers for:
  - risk_level
  - card_type
  - is_fraud
- Color code fraud (e.g. red for True)
- Use tooltips to display additional info on hover (e.g., merchant, device ID)






✅ Data Quality Control

Ensures the pipeline delivers accurate, complete, and clean data at all times.

1. Validation Rules on Ingestion
- Kafka producer validates:
  python
  assert 300 <= data["credit_score"] <= 850
  assert data["loan_amount"] > 0
  
- Optionally use Avro schema with Confluent Schema Registry.

2. Spark Job Checks
- Detect and flag invalid or missing fields.
- Write to data_quality_issues table:
  sql
  CREATE TABLE data_quality_issues (
    record_id INT,
    issue TEXT,
    timestamp TIMESTAMP
  );
  

3. Monitoring & Alerts
- Prometheus tracks:
  - Kafka topic lag
  - Dropped/invalid records
  - Number of fraud alerts
- Grafana dashboard shows:
  - “Data Quality Events”
  - Anomalies
 
🔍 1. Data Quality Checks

a. Null or Missing Values
python
if df['credit_score'].isnull().any():
    log_warning("Missing credit scores detected")


b. Valid Range Checks
python
assert df['credit_score'].between(300, 850).all(), "Invalid credit scores"
assert df['loan_amount'].gt(0).all(), "Loan amounts must be positive"


c. Duplicate Detection
python
duplicates = df[df.duplicated(subset='application_id')]

d. Schema Validation
Use great_expectations or custom assertions to verify expected columns and data types.

🔔 2. Monitoring

a. Logging
- Log issues to data_quality_issues table
- Include timestamp, record ID, and failure reason

b. Metrics Collection
Use Prometheus to track:
- Number of invalid records
- Missing fields per batch
- ETL job durations

yaml
Custom metric in ETL script
data_quality_invalid_count{check="missing_credit_score"} 12

c. Alerts
Set up Grafana alerts:
- If >5% of records are invalid
- If ETL job fails or slows down
- If fraud spikes over threshold

📊 Example Quality Table

| id | timestamp           | check_type         | failed_record_id | reason               |
|----|---------------------|--------------------|------------------|----------------------|
| 1  | 2025-08-07 12:01:00 | missing_credit     | 10021            | credit_score is null|
| 2  | 2025-08-07 12:01:00 | invalid_loan_value | 10025            | loan_amount < 0     |

Data Governance Implementation

🔐 1. Data Security
- Role-Based Access Control (RBAC)  
  - Grant least-privilege access by role (e.g. Analyst, Engineer, Admin)
  - Use PostgreSQL GRANT/REVOKE and MongoDB roles

- Encryption
  - At-rest: Enable disk/database encryption
  - In-transit: Use SSL/TLS for all connections

- Audit Logs
  - Track data access, queries, inserts, updates, and deletions

🛡️ 2. Data Privacy

- Masking Sensitive Data  
  - Hide personal identifiers (e.g. names, ID numbers) in dev environments

- Anonymization/Pseudonymization  
  - Replace PII fields before analysis (e.g. user_id → token)

- Consent Tracking  
  - Record user consent status and apply opt-out logic

📜 3. Compliance

- Align with frameworks such as:
  - GDPR (EU)
  - CCPA (California)
  - PCI DSS (for financial data)

- Data Retention Policies  
  - Auto-delete or archive data older than X years

- Data Lineage & Cataloging  
  - Use tools like OpenMetadata or Amundsen to track data flow

✅ Tools to Support Governance

| Area         | Tool              |
|--------------|-------------------|
| Access Ctrl  | PostgreSQL Roles, MongoDB Auth  |
| Auditing     | db logs, Flink Kafka audit logs |
| Masking      | Python Pandas, SQL Views        |
| Lineage      | OpenMetadata, DataHub           |

⚙️ Components and Scripts

1. *Kafka Producer (Python)*
Simulates loan applications and streams to Kafka.

*`ingestion/kafka_producer.py`*
python
from kafka import KafkaProducer
import json, time, random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_event():
    return {
        "application_id": random.randint(1000, 9999),
        "user_id": random.randint(1, 100),
        "credit_score": random.randint(300, 850),
        "loan_amount": round(random.uniform(1000, 20000), 2),
        "timestamp": time.time()
    }

while True:
    data = generate_event()
    producer.send('credit_applications', value=data)
    print("Sent:", data)
    time.sleep(2)

2. Flink Job
Detects fraud in real time.

*Logic*:  
- If `loan_amount > 15000` and `credit_score < 450` → alert  
- Result stored in MongoDB.

*`flink_jobs/fraud_detection.py`*
python
Pseudo-PyFlink
if loan_amount > 15000 and credit_score < 450:
    emit_alert(application_id, reason="Risky transaction")

3. Spark Job
Calculates risk scores from Kafka or HDFS and writes to PostgreSQL.

'processing/spark_jobs/credit_scoring_job.py'
python
from pyspark.sql import SparkSession
from pyspark.sql.functions import when

spark = SparkSession.builder.appName("CreditScoring").getOrCreate()

df = spark.read.json("hdfs://localhost:9000/kafka-data/credit_apps.json")

df = df.withColumn("risk_level", when(df.credit_score >= 700, "Low")
.when(df.credit_score >= 500, "Medium")
.otherwise("High"))

df.write.format("jdbc").option("url", "jdbc:postgresql://db:5432/creditdb")\
    .option("dbtable", "credit_scores")\
    .option("user", "postgres")\
    .option("password", "admin")\
    .mode("append").save()

4. PostgreSQL Setup

*`storage/postgres_setup.sql`*
sql
CREATE TABLE credit_scores (
    application_id INT,
    user_id INT,
    credit_score INT,
    loan_amount FLOAT,
    risk_level TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE data_quality_issues (
    record_id SERIAL,
    issue TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE metadata_table (
    job TEXT,
    source TEXT,
    target TEXT,

- Access Control: DB roles and service authentication
- Lineage: Metadata tracked in metadata_table
- Policies:
  - Credit score ≥ 600 for low risk
  - Loan amount ≤ $15,000 for instant approval
- Auditing: Logged via Kafka + Spark job logs


🧪 How to Run

1. Launch All Services
docker-compose up -d


2. Start Producer
python ingestion/kafka_producer.py


3. Run Spark Job
spark-submit processing/spark_jobs/credit_scoring_job.py


📊 Dashboards
 Power BI connects to PostgreSQL
- Shows:
  - Loan distribution by risk
  - Fraud alerts
  - Approved/rejected rates by region
Grafana monitors:
  - Kafka lag
  - Spark job counts
  - Fraud spikes
    
- *Power BI*: Open `.pbix` file and connect to PostgreSQL  
- *Grafana*: http://localhost:3000 (admin/admin)  
- *Flink*: http://localhost:8081  
- *Prometheus*: http://localhost:9090

🔐 Data Governance
- Access Control: DB-level credentials & RBAC
- Lineage Tracking: Metadata logged in PostgreSQL
- Audit Logs: Kafka logs + Spark job output
- Policy Management: Thresholds & exceptions tracked in MongoDB + Power BI  


✅ Data Quality Control
- Validation at Ingestion (e.g., credit score range, nulls)
- Spark Cleansing: Invalid records → data_quality_issues table
- Metrics: Dropped records, fraud rates, Kafka lags
- Alerts: Triggered via Grafana thresholds
  
📈 Monitoring
Grafana dashboards visualize system throughput, job status, Kafka topics, and fraud alert volumes. Uses Prometheus to scrape metrics. 

🪪 License
MIT License — free to use, modify and share.

📬 Contact
*Maintainer:* lawithus  
*Email:* larryanesu@gmail.com
