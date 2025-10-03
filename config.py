import os
from pathlib import Path
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
mongo_url = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@zero-hour.gskxdlj.mongodb.net/?retryWrites=true&w=majority&appName=zero-hour"
db_name = os.environ['DB_NAME']

# JWT and Password settings
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30