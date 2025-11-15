# database.py
import os
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

# Environment variables (or defaults)
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.environ.get("MONGO_DB", "smartclean_db")
USERS_COL = os.environ.get("USERS_COL", "users")
POINTS_COL = os.environ.get("POINTS_COL", "litter_points")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# CORRECT COLLECTION REFERENCES
users_col = db[USERS_COL]
points_col = db[POINTS_COL]

# ----------------------- USERS FUNCTIONS -----------------------

def create_user(username: str, password_hash: str):
    user = {
        "username": username,
        "password_hash": password_hash,
        "created_at": datetime.utcnow()
    }
    res = users_col.insert_one(user)
    return str(res.inserted_id)

def find_user_by_username(username: str):
    u = users_col.find_one({"username": username})
    if u:
        u["_id"] = str(u["_id"])
    return u

# ----------------------- LITTER POINTS -----------------------

def insert_litter_point(doc: dict):
    doc["created_at"] = datetime.utcnow()
    res = points_col.insert_one(doc)
    return str(res.inserted_id)

def query_points(limit: int = 5000):
    cursor = points_col.find({}).sort("created_at", -1).limit(limit)
    out = []
    for c in cursor:
        c["_id"] = str(c["_id"])
        out.append(c)
    return out

def mark_resolved(point_id: str, cleaner_id: str = None):
    res = points_col.update_one(
        {"_id": ObjectId(point_id)},
        {"$set": {
            "resolved": True,
            "resolved_by": cleaner_id,
            "resolved_at": datetime.utcnow()
        }}
    )
    return res.modified_count
