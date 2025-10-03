from motor.motor_asyncio import AsyncIOMotorClient
from config import mongo_url, db_name

_client = AsyncIOMotorClient(mongo_url)

def get_db():
    """Return the database instance."""
    return _client[db_name]

# async def close_db():
#     client.close()
