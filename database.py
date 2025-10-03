from motor.motor_asyncio import AsyncIOMotorClient
from config import mongo_url, db_name

client: AsyncIOMotorClient = None
db = None

def get_db():
    global client, db
    if client is None:
        client = AsyncIOMotorClient(mongo_url)
        db = client[db_name]
    return db

# async def close_db():
#     client.close()
