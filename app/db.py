from pymongo import MongoClient
from pymongo.collection import Collection

from app.config import settings


client = MongoClient(settings.mongodb_uri)
database = client[settings.mongodb_db_name]
message_logs_collection: Collection = database[settings.mongodb_collection_name]


def get_message_logs_collection() -> Collection:
    """Return the MongoDB collection used for chatbot logs."""
    return message_logs_collection