import os
import sys
import json

from dotenv import load_dotenv

load_dotenv()
MONGODB_URL = os.getenv("MONGODB_URL")

import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logger.logger import logging

class NetworkDataExtraction():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
    
    def csv_to_json(self, file_path:str):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
    
    def pushing_data_to_mongodb(self, records:list, collection_name:str, database_name:str):
        try:
            self.database_name = database_name
            self.collection_name = collection_name
            self.records = records
            
            self.mongo_client = pymongo.MongoClient(MONGODB_URL, tlsCAFile=ca)
            self.database = self.mongo_client[self.database_name]
            self.collection = self.database[self.collection_name]
            self.collection.insert_many(self.records)

            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

if __name__ == "__main__":
    FILE_PATH = "Network_Data/NetworkData.csv"
    DATABASE_NAME = "networksecurity"
    COLLECTION_NAME = "networkdata"

    network_data_extraction = NetworkDataExtraction()
    records = network_data_extraction.csv_to_json(FILE_PATH)
    result = network_data_extraction.pushing_data_to_mongodb(records, COLLECTION_NAME, DATABASE_NAME)
    print(result)