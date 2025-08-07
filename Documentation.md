
💳 Credit Scoring, Lending & Fraud Detection System

A full-stack data engineering platform to automate loan application analysis, credit risk scoring, fraud detection, and real-time insights using Kafka, Spark, Flink, PostgreSQL, MongoDB, and Power BI.


📌 Features

- Real-time ingestion with Kafka
- Fraud detection with Flink
- Risk scoring with Spark
- PostgreSQL as data warehouse
- MongoDB for fraud alerts
- Dashboards via Power BI & Grafana
- Access control, governance, and monitoring

🧱 Architecture Diagram


[Kafka Producer] → [Kafka Topic: credit_applications]
        ↓               ↓
 [Flink Fraud Job]   [Spark Risk Job]
        ↓               ↓
  [MongoDB Alerts]   [PostgreSQL DW]
           ↘           ↙
        [Power BI Dashboards]

⚙️ Components

Kafka Producer
Simulates and streams loan applications.

bash
python ingestion/kafka_producer.py


Flink Job
Flags fraud cases in real time.

Rule: credit_score < 450 && loan_amount > 15000 → alert

Spark Job
Reads valid applications and classifies:
- High Risk: score < 500
- Medium Risk: 500–699
- Low Risk: ≥ 700

Saves to PostgreSQL.

bash
spark-submit processing/spark_jobs/credit_scoring_job.py

🧾 PostgreSQL Tables

- credit_scores: valid risk-classified loans
- data_quality_issues: invalid input logs
- metadata_table: pipeline lineage tracking

Run:
bash
psql -U postgres -d creditdb -f storage/postgres_setup.sql


🍃 MongoDB Setup

js
use fraud_detection;
db.createCollection("fraud_alerts");
db.fraud_alerts.createIndex({ application_id: 1 });


📊 Dashboards

Power BI
- Load data from PostgreSQL
- Visuals: risk breakdown, loan approval rates, fraud counts

Grafana (credit_dashboard.json)
- Fraud alerts
- Kafka lag
- Spark job stats
- System metrics via Node Exporter


🔐 Governance & Access Control

- PostgreSQL roles & DB grants
- Kafka auth (SSL/SASL configurable)
- Metadata table for lineage
- Logs and quality checks on ingestion


📈 Monitoring

- Prometheus collects metrics
- Grafana visualizes job and system health

bash
prometheus --config.file=monitoring/prometheus.yml


🧪 Data Quality Control

Spark filters:
- Missing credit scores
- Invalid loan amounts
- Out-of-range values

Bad records logged in data_quality_issues


📦 Folder Structure

├── ingestion/
│   └── kafka_producer.py
├── processing/
│   └── spark_jobs/
│       └── credit_scoring_job.py
│   └── flink_jobs/
│       └── fraud_detection.py
├── storage/
│   └── postgres_setup.sql
│   └── mongodb_setup.js
├── monitoring/
│   └── prometheus.yml
│   └── credit_dashboard.json
├── dashboards/
│   └── powerbi_report.pbix
└── documentation.md


🚀 How to Run End-to-End

1. *Start all services* (Kafka, MongoDB, PostgreSQL, Prometheus)
2. *Start Kafka producer*
3. *Run Spark job*
4. *Open Power BI / Grafana*

---

📚 Future Enhancements

- Add ML model for dynamic scoring
- REST API for external approval
- Integration with external bureaus
- Kafka + Delta Lake + Iceberg for scalable storage

---

👤 Maintainer

*Author*: Larry Anesu  
*GitHub*: github.com/larry0003  
*Email*: lar…