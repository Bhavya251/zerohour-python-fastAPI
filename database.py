from motor.motor_asyncio import AsyncIOMotorClient
from config import mongo_url, db

client = AsyncIOMotorClient(mongo_url)
db = client[db]

async def close_db():
    client.close()
