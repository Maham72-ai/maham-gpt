from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore
from app.core.config import settings

client: AsyncIOMotorClient = None  # type: ignore
db = None

async def connect_to_mongo():
    global client, db
    # Aapke config.py ke hisaab se
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[settings.MONGODB_DB_NAME]
    # Indexes
    try:
        await db.conversations.create_index("user_id")
        await db.messages.create_index("conversation_id")
        print("MongoDB connected with indexes")
    except Exception as e:
        print(f"MongoDB connected: {e}")

async def close_mongo_connection():
    global client
    if client:
        client.close()

def get_database():
    return db

def get_db():
    return db

def get_mongo_db():
    return db