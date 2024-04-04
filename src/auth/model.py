from pymongo import MongoClient

client = MongoClient("mongodb://admin:admin@mongodb:27017")
db = client.user_database
users_collection = db.users

def create_user(user_data):
    users_collection.insert_one(user_data)

def find_user_by_username(username):
    return users_collection.find_one({"username": username})
