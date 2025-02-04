from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["facebook_insights"]
pages_collection = db["pages"]

def save_page_to_db(page_data):
    pages_collection.insert_one(page_data)

def get_page_from_db(query):
    if isinstance(query, str):
        return pages_collection.find_one({"username": query})
    return pages_collection.find(query)