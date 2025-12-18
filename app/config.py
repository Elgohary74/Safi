import os
from datetime import timedelta

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str

    MONGODB_URL: str
    MONGODB_DATABASE: str
    MONGODB_ROOT_USERNAME: str
    MONGODB_ROOT_PASSWORD: str

    INVITE_CODE_LENGTH: int

    model_config = {
        "env_file": os.path.join(os.path.dirname(__file__), "../.env"),
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


def get_settings() -> Settings:
    return Settings()


class Config:
    """Base configuration."""

    SECRET_KEY = os.environ.get("SECRET_KEY")

    # JWT Settings
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-secret-key")
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # Cookie Security
    JWT_COOKIE_SECURE = False  # Set to True in Production
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_COOKIE_NAME = "access_token_cookie"
    JWT_REFRESH_COOKIE_NAME = "refresh_token_cookie"
    JWT_ACCESS_CSRF_COOKIE_NAME = "csrf_access_token"

    # MongoDB Connection
    MONGODB_SETTINGS = {
        "host": os.environ.get("MONGODB_URL"),
        "connect": False,  # We use connect=False to avoid connection issues with Gunicorn workers
    }


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
