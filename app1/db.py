import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_DATABASE_URL = os.getenv("MONGO_DATABASE_URL")

client = MongoClient(MONGO_DATABASE_URL)

try:
    client.admin.command('ping')
    print("✅ MongoDB connection successful.")
except Exception as e:
    print("❌ MongoDB connection failed:", f"\nError: {str(e)}")

db = client["ticket_system"]
tickets_collection = db["tickets"]
