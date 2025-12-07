import logging
import os
from typing import Optional
from urllib.parse import urlparse

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure

logger = logging.getLogger(__name__)


class MongoDatabase:
    """Singleton MongoDB database connection class with lazy initialization"""

    _instance: Optional["MongoDatabase"] = None
    _client: Optional[MongoClient] = None
    _db: Optional[Database] = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDatabase, cls).__new__(cls)
        return cls._instance

    def initialize(self):
        """Initialize the database connection only when needed"""
        if self._initialized:
            return

        try:
            logger.info("attempting to connect to MongoDB")
            mongo_url = os.getenv("MONGODB_URL", "")

            # Check for mongomock URI scheme
            if mongo_url.startswith("mongomock://"):
                try:
                    import mongomock

                    parsed = urlparse(mongo_url)
                    db_name = (
                        parsed.path[1:]
                        if parsed.path
                        else os.environ.get("MONGODB_DATABASE", "safi_db")
                    )
                    logger.info(f"Using mongomock for testing (DB: {db_name})")
                    self._client = mongomock.MongoClient()
                    self._db = self._client[db_name]
                    self._initialized = True
                    return
                except ImportError:
                    logger.error(
                        "mongomock package is not installed but mongomock:// URL was provided"
                    )
                    raise ImportError(
                        "mongomock package is required for testing"
                    ) from None

            # Handle regular MongoDB connections
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

            self._client = MongoClient(mongo_url)
            self._client.admin.command("ping")
            self._db = self._client[db_name]

            logger.info(f"Connected to MongoDB at {clean_host} (DB: {db_name})")
            self._initialized = True

        except ConnectionFailure as e:
            logger.error(f"failed to connect to mongo: {e}", exc_info=True)
            raise e

    def get_db(self):
        """Get the database connection with lazy initialization"""
        if not self._initialized:
            self.initialize()
        return self._db
