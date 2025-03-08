import logging
import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)


def connect_to_db():
    password = os.getenv("MONGO_PASSWORD")
    username = os.getenv("MONGO_USERNAME")
    mongo_url = os.getenv("MONGO_URL")
    uri = (f"mongodb+srv://{username}:{password}@{mongo_url}/"
           "?retryWrites=true&w=majority&appName=TBDM-Heatmap-DB")

    try:
        client = MongoClient(uri, server_api=ServerApi('1'), socketTimeoutMS=5000, connectTimeoutMS=5000)
        client.admin.command('ping')
        logger.info("Successfully connected to MongoDB.")
        return client
    except Exception as e:
        logger.error(f"An error occurred while connecting to MongoDB: {e}")
        raise


if __name__ == "__main__":
    connect_to_db()
