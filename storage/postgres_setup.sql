sql
-- Create the main database (run in psql shell or admin UI if needed)
CREATE DATABASE creditdb;

--Table 1: Credit Scores

CREATE TABLE IF NOT EXISTS credit_scores (
    application_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    credit_score INT CHECK (credit_score BETWEEN 300 AND 850),
    loan_amount FLOAT CHECK (loan_amount > 0),
    risk_level TEXT CHECK (risk_level IN ('Low', 'Medium', 'High')),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Table 2: Data Quality Issues

CREATE TABLE IF NOT EXISTS data_quality_issues (
    record_id SERIAL PRIMARY KEY,
    application_id INT,
    user_id INT,
    credit_score INT,
    loan_amount FLOAT,
    issue TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Table 3: Metadata / Job Lineage Logging
CREATE TABLE IF NOT EXISTS metadata_table (
    id SERIAL PRIMARY KEY,
    job TEXT,
    source TEXT,
    target TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


