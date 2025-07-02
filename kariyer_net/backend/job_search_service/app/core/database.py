from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

class Database:
    client: AsyncIOMotorClient = None

db = Database()

async def get_database() -> AsyncIOMotorClient:
    return db.client

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    print("Connected to MongoDB.")
    # Ensure text index exists for search functionality
    try:
        await db.client.job_search.search_history.create_index([("job_name", "text")])
        print("Ensured text index on 'job_name' in 'search_history' collection.")
    except Exception as e:
        print(f"Index creation failed: {e}")

async def close_mongo_connection():
    if db.client:
        db.client.close()
        print("Disconnected from MongoDB.") 