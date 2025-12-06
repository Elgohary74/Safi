import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str

    MONGODB_URI: str
    MONGODB_DATABASE: str

    INVITE_CODE_LENGTH: int

    model_config = {
        "env_file": os.path.join(os.path.dirname(__file__), "../.env"),
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }


def get_settings() -> Settings:
    return Settings()


class Config:
    """Base configuration."""

    # MongoDB Connection
    MONGODB_SETTINGS = {
        "host": os.environ.get("MONGO_URI"),
        "connect": False,  # We use connect=False to avoid connection issues with Gunicorn workers
    }

    # Security Defaults
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True


class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False  # Allow HTTP in dev


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True  # Enforce HTTPS in prod


# Note: TestingConfig inherits from DevelopmentConfig (not directly from Config)
# to ensure settings like SESSION_COOKIE_SECURE = False are inherited, which is
# appropriate for testing environments. This inheritance is intentional and should
# be maintained unless testing requirements change.
class TestingConfig(DevelopmentConfig):
    """Pytest Settings"""

    TESTING = True
    WTF_CSRF_ENABLED = False  # Disable CSRF tokens to make testing forms easier
    MONGODB_SETTINGS = {"host": "mongomock://localhost", "db": "test_db"}
