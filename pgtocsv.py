import pandas as pd
import os


def pg_to_csv(filename, sql_query, orm_conn):
    df = pd.read_sql_query(sql_query, orm_conn)
    os.makedirs("output", exist_ok=True)
    path = os.path.join("output", filename+".csv")
    df.to_csv(path, index=False)
