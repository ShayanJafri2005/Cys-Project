


import pandas as pd 
from src.CysProject.logging import logger 
from src.CysProject.exception.exception import NetworkSecurityException
import sys 
from sqlalchemy import create_engine
import sqlite3

class NetworkDataExtractSQLite():
    def __init__(self, db_path="network_data.db"):
        try:
            self.engine = create_engine(f"sqlite:///{db_path}")
        except Exception as e:
            raise Exception(f"DB connection error: {e}")
        
    def csv_to_df(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            return data
        except Exception as e:
            raise Exception(f"CSV error: {e}")
        
    def insert_data_sqlite(self, df, table_name):
        try:
            df.to_sql(table_name, self.engine, if_exists="replace", index=False)
            return len(df)
        except Exception as e:
            raise Exception(f"Insertion error: {e}")

if __name__ == '__main__':
    FILE_PATH = "Cys-Project-Data/phisingData.csv"
    TABLE_NAME = "NetworkData"
    
    networkobj = NetworkDataExtractSQLite()
    df = networkobj.csv_to_df(FILE_PATH)
    print(df.head())
    
    no_of_records = networkobj.insert_data_sqlite(df, TABLE_NAME)
    print(f"✅ {no_of_records} records inserted into SQLite table '{TABLE_NAME}'")