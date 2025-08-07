python
from pymongo import MongoClient
import pandas as pd

def extract_from_mongo():
    client = MongoClient("mongodb://localhost:27017")
    db = client.fraud_detection
    collection = db.fraud_alerts
    data = list(collection.find())
    return pd.DataFrame(data)
