import os
from urllib.parse import urlparse

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class MongoDatabase:
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDatabase, cls).__new__(cls)
            try:
                mongo_uri = os.getenv("MONGODB_URL")
                parsed = urlparse(mongo_uri)
                db_name = parsed.path[1:] or "safi_db"
                cls._client = MongoClient(mongo_uri)
                cls._client.admin.command("ping")
                cls._db = cls._client[db_name]
                print(f"connected to MongoDB at {mongo_uri}")
            except ConnectionFailure as e:
                print(f" connection Failed: {e}")
                cls._instance = None
                raise e
        return cls._instance

    def get_db(self):
        return self._db
