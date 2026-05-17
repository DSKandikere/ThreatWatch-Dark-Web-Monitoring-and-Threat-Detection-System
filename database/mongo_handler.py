from pymongo import MongoClient
import os
import time

# Load from environment
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/")
DB_NAME = "darkweb_db"
COLLECTION_NAME = "leaks"


def connect_mongo(retries=10, delay=3):
    """
    Try connecting to MongoDB with retry logic
    """
    for i in range(retries):
        try:
            client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
            client.server_info()  # Force connection
            print("✅ Connected to MongoDB")
            return client
        except Exception as e:
            print(f"⏳ MongoDB not ready (attempt {i+1}/{retries})...")
            time.sleep(delay)

    raise Exception("❌ Could not connect to MongoDB after multiple attempts")


# Initialize connection
client = connect_mongo()
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


def save_data(data):
    """
    Save list of documents to MongoDB
    """
    if not data:
        print("⚠ No data to insert into MongoDB")
        return

    try:
        # Remove _id if exists (prevents duplication issues)
        for item in data:
            item.pop("_id", None)

        collection.insert_many(data)
        print(f"✅ Saved {len(data)} records to MongoDB")

    except Exception as e:
        print("❌ MongoDB insert error:", e)
