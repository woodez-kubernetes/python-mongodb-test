import os
import time
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

# The hostname for a MongoDB running in the same K8s cluster should be
# the name of the Kubernetes Service for MongoDB.
# The port is the default MongoDB port, 27017.
MONGO_HOST = os.environ.get('MONGO_HOST', 'mongodb-service')
MONGO_PORT = int(os.environ.get('MONGO_PORT', 27017))
MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"
DATABASE_NAME = "testdb"
COLLECTION_NAME = "status"

def connect_to_mongodb():
    """Connects to MongoDB and performs a simple check."""
    client = None
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        
        # The ismaster command is a lightweight way to check connection
        client.admin.command('ismaster') 
        
        print(f"Successfully connected to MongoDB at {MONGO_URI}")
        
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        
        # Insert a document
        result = collection.insert_one({"message": "Python pod connected!", "timestamp": time.time()})
        print(f"Inserted document with ID: {result.inserted_id}")
        
        # Find the inserted document
        document = collection.find_one({"_id": result.inserted_id})
        print(f"Retrieved document: {document}")
        
    except ConnectionFailure as e:
        print(f"ConnectionFailure: Could not connect to MongoDB: {e}")
    except OperationFailure as e:
        print(f"OperationFailure: MongoDB operation failed (check permissions/auth): {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if client:
            client.close()

if __name__ == "__main__":
    print("Starting MongoDB connection test...")
    # Keep trying in a loop, as the MongoDB Pod may start slightly after the Python app Pod
    while True:
        connect_to_mongodb()
        print("Waiting 10 seconds before next attempt...")
        time.sleep(10)