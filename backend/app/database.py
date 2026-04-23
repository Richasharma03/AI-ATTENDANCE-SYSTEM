from pymongo import MongoClient

# ✅ Your MongoDB Atlas URI (directly used)
mongo_uri = "mongodb+srv://richa:jaibholay0302R@cluster0.rmvn4et.mongodb.net/attendance_db?retryWrites=true&w=majority"

print("Mongo URI:", mongo_uri)

# Connect to MongoDB
client = MongoClient(mongo_uri)

# Database
db = client["attendance_db"]

# Collections
users_collection = db["users"]
attendance_collection = db["attendance"]