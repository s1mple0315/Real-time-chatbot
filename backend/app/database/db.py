from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(settings.MONGODB_URL)
db = client[settings.DATABASE_NAME]
messages_collection = db["messages"]

def save_message(message: str, sender: str):
    message_data = {
        "message": message,
        "sender": sender
    }
    messages_collection.insert_one(message_data)
    return message_data

def get_all_messages():
    return list(messages_collection.find({}, {"_id": 0}))