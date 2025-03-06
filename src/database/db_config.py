from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://pelato:calvizie@tbdm-heatmap-db.tlu9b.mongodb.net/?retryWrites=true&w=majority&appName=TBDM-Heatmap-DB"

client = MongoClient(uri, server_api=ServerApi('1'), socketTimeoutMS=5000, connectTimeoutMS=5000)
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("An error occurred:", e)
