python
from extract.extract_mongo import extract_from_mongo
from extract.extract_postgres import extract_from_postgres
from transform.transform import transform_data
from load.load_to_dw import load_to_data_warehouse

mongo_df = extract_from_mongo()
postgres_df = extract_from_postgres()
transformed_df = transform_data(postgres_df, mongo_df)
load_to_data_warehouse(transformed_df)