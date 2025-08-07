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
bash
python ingestion/kafka_producer.py


4. Run Spark Job
spark-submit processing/spark_jobs/credit_scoring_job.py

📊 Dashboards

- *Power BI*: Open `.pbix` file and connect to PostgreSQL  
- *Grafana*: http://localhost:3000 (admin/admin)  
- *Flink*: http://localhost:8081  
- *Prometheus*: http://localhost:9090


🔒 Access Control

- PostgreSQL user/password protected  
- MongoDB accessible only via Docker network  
- Local-only Kafka/Zookeeper access  
- Dashboard login required

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
