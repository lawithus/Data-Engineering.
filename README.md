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

🔁 Pipeline Design Summary:
- Ingestion: Kafka Producer streams new loan applications.
- Streaming Layer: Flink processes applications in real-time and flags fraud.
- Batch Layer: Spark calculates risk scores periodically and writes to the data warehouse.
- Storage:
  - MongoDB for fast storage of fraud alerts.
  - PostgreSQL acts as the central data warehouse.
- Reporting Layer: Power BI pulls data from PostgreSQL for business intelligence.

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


📊 Dashboards

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

📤 Exporting & Reporting
- Power BI reports can be exported to PDF
- MongoDB alerts exportable via script
- Grafana dashboards sharable as snapshots

🪪 License
MIT License — free to use, modify and share.

📬 Contact
*Maintainer:* lawithus  
*Email:* larryanesu@gmail.com
