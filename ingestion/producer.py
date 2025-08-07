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
