from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# MongoDB connection settings
MONGO_URI = "mongodb+srv://2013volvod13:bxRhvV0r6nBwrM6d@sgi.xf4az.mongodb.net/?retryWrites=true&w=majority&appName=SGI"
DATABASE_NAME = "SGI"

# Collection names
ALL_PRODUCTS_COLLECTION = "all_products"
VENDORS_COLLECTION = "vendors"

def get_mongo_client():
    """
    Create and return a MongoDB client.
    """
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    try:
        # Confirm the connection
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None
