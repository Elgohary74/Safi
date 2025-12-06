import os

from dotenv import load_dotenv

# Load .env file (only affects local development)
load_dotenv()


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
    # Allow HTTP in dev
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):

    DEBUG = False
    # Enforce HTTPS in prod
    SESSION_COOKIE_SECURE = True


# Note: TestingConfig inherits from DevelopmentConfig (not directly from Config)
# to ensure settings like SESSION_COOKIE_SECURE = False are inherited, which is
# appropriate for testing environments. This inheritance is intentional and should
# be maintained unless testing requirements change.
class TestingConfig(DevelopmentConfig):
    """Pytest Settings"""

    TESTING = True
    WTF_CSRF_ENABLED = False  # Disable CSRF tokens to make testing forms easier
    MONGODB_SETTINGS = {"host": "mongomock://localhost", "db": "test_db"}
