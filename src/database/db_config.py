from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

def connect_to_db():
    password = os.environ["MONGO_PASSWORD"]
    username = os.environ["MONGO_USERNAME"]
    mongo_url = os.environ["MONGO_URL"]
    uri = f"mongodb+srv://{username}:{password}@{mongo_url}/?retryWrites=true&w=majority&appName=TBDM-Heatmap-DB"
    client = MongoClient(uri, server_api=ServerApi('1'), socketTimeoutMS=5000, connectTimeoutMS=5000)
    try:
        client.admin.command('ping')
    except Exception as e:
        print("An error occurred:", e)


