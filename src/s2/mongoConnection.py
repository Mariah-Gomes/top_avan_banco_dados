from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')

def get_mongo_client():
    client = MongoClient(MONGO_URI)
    return client["LaudoExame"]

# client = MongoClient(MONGO_URI)

# Lista todos os bancos de dados
#print("Bancos disponíveis no cluster:")
#for db_name in client.list_database_names():
#    print("-", db_name)