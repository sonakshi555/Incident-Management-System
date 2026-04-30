import motor.motor_asyncio
from app.core.config import settings

# Initialize the Async MongoDB Client
client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URL)
db = client.ims_database

# Collection for raw high-volume signals
signal_collection = db.get_collection("raw_signals")

async def ping_mongo():
    """Verify MongoDB connection."""
    try:
        await client.admin.command('ping')
        return True
    except Exception:
        return False