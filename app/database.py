import motor.motor_asyncio
from pymongo.mongo_client import MongoClient
from bson.son import SON
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_DETAILS = os.getenv("MONGO_DETAILS")
DATABASE_NAME = "assessment_db"
COLLECTION_NAME = "employees"

# Asynchronous Client (for API operations) 
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client[DATABASE_NAME]
employee_collection = database.get_collection(COLLECTION_NAME)

# Synchronous Client (for startup tasks) 
print("Initializing synchronous MongoDB client...")
sync_client = MongoClient(MONGO_DETAILS)
sync_db = sync_client[DATABASE_NAME] 
sync_employee_collection = sync_db.get_collection(COLLECTION_NAME)
print("Synchronous client initialized.")

# Add MongoDB Unique Index 
print("Attempting to create a unique index on 'employee_id'...")
try:
    sync_employee_collection.create_index("employee_id", unique=True)
    print("Index created successfully or already exists.")
except Exception as e:
    print(f"An error occurred while creating the index: {e}")

# Schema Validation 
employee_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["employee_id", "name", "department", "salary", "joining_date"],
        "properties": {
            "employee_id": {"bsonType": "string"},
            "name": {"bsonType": "string"},
            "department": {"bsonType": "string"},
            "salary": {"bsonType": ["double", "int"], "minimum": 0},
            "joining_date": {"bsonType": "date"},
            "skills": {"bsonType": "array", "items": {"bsonType": "string"}}
        }
    }
}

print("Attempting to apply schema validation...")
try:
    command = SON([('collMod', COLLECTION_NAME), ('validator', employee_validator)])
    sync_db.command(command)
    print("Schema validation applied successfully or already exists.")
except Exception as e:
    print(f"An error occurred while applying schema validation: {e}")
