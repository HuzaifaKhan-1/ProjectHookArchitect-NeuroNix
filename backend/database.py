import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# Global MongoDB Atlas URI (Activated for Cloud Persistence)
MONGODB_URL = "mongodb+srv://rohitdb:rohit150288@cluster0.l4v0ldu.mongodb.net/?appName=Cluster0"

client = AsyncIOMotorClient(MONGODB_URL)
database = client.hook_architect_db
reports_collection = database.analysis_reports

async def archive_analysis(data: dict):
    """ 
    Saves a JSON serialized analysis report into MongoDB 
    Turn the ephemeral results into a persistent creator history.
    """
    try:
        data["timestamp"] = datetime.utcnow()
        result = await reports_collection.insert_one(data)
        print(f"📊 MongoDB: Archived Analysis Record [{result.inserted_id}]")
        return True
    except Exception as e:
        print(f"⚠️ MongoDB Archive Error: {e}")
        return False

async def get_analysis_history(limit: int = 10):
    """ Retrieves the most recent viral blueprints from the cloud """
    try:
        cursor = reports_collection.find().sort("timestamp", -1).limit(limit)
        results = await cursor.to_list(length=limit)
        # Convert ObjectId to string for JSON serialization
        for r in results:
            r["_id"] = str(r["_id"])
        return results
    except Exception as e:
        print(f"❌ MongoDB Fetch Error: {e}")
        return []
