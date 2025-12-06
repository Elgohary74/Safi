import logging
import os
from urllib.parse import urlparse

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

logger = logging.getLogger("app.services.database")


class MongoDatabase:
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDatabase, cls).__new__(cls)
            try:
                logger.info("attempting to connect to MongoDB")
                mongo_uri = os.getenv("MONGODB_URL")
                parsed = urlparse(mongo_uri)
                db_name = parsed.path[1:] or "safi_db"
                clean_host = f"{parsed.hostname}:{parsed.port}"

                cls._client = MongoClient(mongo_uri)
                cls._client.admin.command("ping")
                cls._db = cls._client[db_name]

                logger.info(f" Connected to MongoDB at {clean_host} (DB: {db_name})")
            except ConnectionFailure as e:
                logger.error(f"failed to connect to mongo : {e}", exc_info=True)
                cls._instance = None
                raise e
        return cls._instance

    def get_db(self):
        return self._db
