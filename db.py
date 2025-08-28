from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from pymongo import MongoClient, ASCENDING, ReturnDocument
import hashlib
from config import MONGO_URL, DB_NAME, VERIFY_EXPIRE

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

users = db["users"]
files = db["files"]
verifications = db["verifications"]
stats = db["stats"]
broadcasts = db["broadcasts"]

users.create_index([("_id", ASCENDING)])
files.create_index([("permanent_code", ASCENDING)], unique=True, sparse=True)
verifications.create_index([("user_id", ASCENDING)])
verifications.create_index([("token", ASCENDING)], unique=True)

def ensure_user(user_id: int) -> Dict[str, Any]:
    doc = users.find_one({"_id": user_id})
    if doc:
        return doc
    doc = {"_id": user_id, "free_used": 0, "is_premium": False, "joined_channels": [], "created_at": datetime.utcnow()}
    users.insert_one(doc)
    return doc

def increment_free_used(user_id: int) -> int:
    res = users.find_one_and_update({"_id": user_id}, {"$inc": {"free_used": 1}}, return_document=ReturnDocument.AFTER, upsert=True)
    return res["free_used"]

def reset_verification(user_id: int):
    verifications.delete_many({"user_id": user_id})

def create_file(owner_id: int, tg_file_id: str, ftype: str, caption: str = "", size: int = 0) -> str:
    base = f"{owner_id}:{tg_file_id}:{datetime.utcnow().timestamp()}"
    code = hashlib.sha256(base.encode()).hexdigest()[:16]
    files.insert_one({"owner_id": owner_id, "tg_file_id": tg_file_id, "type": ftype, "caption": caption, "size": size, "created_at": datetime.utcnow(), "permanent_code": code})
    return code

def get_file_by_code(code: str) -> Optional[Dict[str, Any]]:
    return files.find_one({"permanent_code": code})

def create_verification(user_id: int, provider: str, short_url: str, token: str) -> Dict[str, Any]:
    doc = {
        "user_id": user_id, "provider": provider, "short_url": short_url, "token": token,
        "created_at": datetime.utcnow(), "expires_at": datetime.utcnow() + timedelta(seconds=VERIFY_EXPIRE), "verified": False
    }
    verifications.insert_one(doc)
    return doc

def get_active_verification(user_id: int) -> Optional[Dict[str, Any]]:
    now = datetime.utcnow()
    return verifications.find_one({"user_id": user_id, "verified": False, "expires_at": {"$gt": now}})

def mark_verified(token: str):
    verifications.update_one({"token": token}, {"$set": {"verified": True}})

def is_premium(user_id: int) -> bool:
    doc = users.find_one({"_id": user_id}, {"is_premium": 1})
    return bool(doc and doc.get("is_premium"))

def set_premium(user_id: int, value: bool):
    users.update_one({"_id": user_id}, {"$set": {"is_premium": value}}, upsert=True)

def bump_stat(key: str, n: int = 1) -> int:
    res = stats.find_one_and_update({"key": key}, {"$inc": {"value": n}}, upsert=True, return_document=ReturnDocument.AFTER)
    return res["value"]

def count_users() -> int:
    return users.estimated_document_count()
  
