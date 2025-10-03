from motor.motor_asyncio import AsyncIOMotorClient
from config import mongo_url, db_name

async def get_db():
    """Return a database instance per request."""
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    return db


# async def close_db():
#     client.close()
