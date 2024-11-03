from motor.motor_asyncio import AsyncIOMotorClient

from conf import *

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
workers_collection = db[COLLECTION_NAME]