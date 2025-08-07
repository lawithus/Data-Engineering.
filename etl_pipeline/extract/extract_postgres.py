python
import pandas as pd
from sqlalchemy import create_engine

def extract_from_postgres():
    engine = create_engine("postgresql://postgres:admin@localhost:5432/creditdb")
    query = "SELECT * FROM credit_scores"
    df = pd.read_sql(query, engine)
    return df