python
from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col, lit, current_timestamp
from pyspark.sql.types import StructType, StructField, IntegerType, FloatType, TimestampType

//Define schema for input data
schema = StructType([
    StructField("application_id", IntegerType(), True),
    StructField("user_id", IntegerType(), True),
    StructField("credit_score", IntegerType(), True),
    StructField("loan_amount", FloatType(), True),
    StructField("timestamp", TimestampType(), True)
])

//Start Spark session
spark = SparkSession.builder \
    .appName("CreditScoringJob") \
    .config("spark.jars", "/path/to/postgresql-connector.jar") \  # replace with your actual path
    .getOrCreate()

//Load data (from HDFS or local JSON file)
df = spark.read.schema(schema).json("hdfs://localhost:9000/credit_apps.json")

//Data validation
valid_df = df.filter((col("credit_score").isNotNull()) &
(col("loan_amount").isNotNull()) &
                     (col("credit_score") >= 300) & (col("credit_score") <= 850) &
                     (col("loan_amount") > 0))

invalid_df = df.subtract(valid_df).withColumn("issue", lit("Invalid record"))

//Risk scoring logic
scored_df = valid_df.withColumn(
    "risk_level",
    when(col("credit_score") >= 700, "Low")
    .when(col("credit_score") >= 500, "Medium")
    .otherwise("High")
)

//Write valid records to PostgreSQL
scored_df.write.format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/creditdb") \
    .option("dbtable", "credit_scores") \
    .option("user", "postgres") \
    .option("password", "admin") \
    .mode("append") \
    .save()

//Write invalid records to data quality log table
invalid_df.select("application_id", "user_id", "credit_score", "loan_amount", "issue", "timestamp") \
    .write.format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/creditdb") \
    .option("dbtable", "data_quality_issues") \
    .option("user", "postgres") \
    .option("password", "admin") \
    .mode("append") \
    .save()

//Metadata logging
meta = spark.createDataFrame([{
    "job": "credit_scoring_job",
    "source": "credit_apps.json",
    "target": "credit_scores",
"timestamp": None
}])
meta = meta.withColumn("timestamp", current_timestamp())

meta.write.format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/creditdb") \
    .option("dbtable", "metadata_table") \
    .option("user", "postgres") \
    .option("password", "admin") \
    .mode("append") \
    .save()

spark.stop()
