import logging
import os
from typing import Optional
from urllib.parse import urlparse

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure

logger = logging.getLogger(__name__)


class MongoDatabase:
    _instance: Optional["MongoDatabase"] = None
    _client: Optional[MongoClient] = None
    _db: Optional[Database] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDatabase, cls).__new__(cls)
            try:
                logger.info("attempting to connect to MongoDB")
                mongo_url = os.getenv("MONGODB_URL")

                root_user = os.environ.get("MONGODB_ROOT_USERNAME")
                root_pass = os.environ.get("MONGODB_ROOT_PASSWORD")
                db_name = os.environ.get("MONGODB_DATABASE", "safi_db")

                if root_user and root_pass and (not mongo_url or "@" not in mongo_url):
                    mongo_url = f"mongodb://{root_user}:{root_pass}@localhost:27017/{db_name}?authSource=admin"
                    logger.info("Using constructed authenticated connection string")
                elif not mongo_url:
                    mongo_url = "mongodb://localhost:27017/safi_db"
                    logger.warning("Using default unauthenticated connection string")

                parsed = urlparse(mongo_url)
                db_name = parsed.path[1:] or db_name or "safi_db"
                clean_host = f"{parsed.hostname}:{parsed.port}"

                cls._client = MongoClient(mongo_url)
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
