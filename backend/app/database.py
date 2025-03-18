from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["chatbot_db"]
messages_collection = db["messages"]


def save_message(message: str, sender: str):
    message_data = {"message": message, "sender": sender}
    messages_collection.insert_one(message_data)
    return message_data


def get_all_messages():
    return list(messages_collection.find({}, {'_id': 0 }))