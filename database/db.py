from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to MongoDB Atlas
def connect_db():
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["mydatabase"] 
    return db

# Function to add data
def add_data(db, data, collection_name="mycollection"):
    collection = db[collection_name]
    collection.insert_one(data)
    print("Data added successfully.")

# Function to fetch all data
def fetch_data(db, collection_name = "mycollection"):
    collection = db[collection_name]
    return list(collection.find({}, {"_id": 0}))  # Exclude _id

# Function to display the last 5 added items
def display_last_5(db, collection_name = "mycollection"):
    collection = db[collection_name]
    return list(collection.find({}, {"_id": 0}).sort("_id", -1).limit(5))


db = connect_db()
#sample = {        "name": "John",        "age": 30,        "city": "New York"    }

#add_data(db, "mycollection", sample)  # Insert data
all_data = fetch_data(db, "users")
print("All Data:", all_data)

#last_5_entries = display_last_5(db, "mycollection")
#print("Last 5 Entries:", last_5_entries)
