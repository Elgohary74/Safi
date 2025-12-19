import os

import pytest
import test_router  # noqa: F401 Ensure test_router is imported first

from app import create_app
from app.config import TestingConfig
from app.repositories.user_repo import UserRepository

__all__ = [test_router]


@pytest.fixture(scope="session", autouse=True)
def configure_test_env():
    """Force the app to use mongomock and test secrets during the session."""

    overrides = {
        "MONGODB_URL": "mongomock://localhost/test_db",
        "MONGODB_DATABASE": "test_db",
        "SECRET_KEY": "test-secret-key",
        "JWT_SECRET_KEY": "jwt-test-secret",
    }

    original_env = {key: os.environ.get(key) for key in overrides}
    os.environ.update(overrides)

    yield

    for key, value in original_env.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value


@pytest.fixture(scope="session")
def app():
    """
    Creates the Flask application for the entire test session.
    Uses TestingConfig to ensure we use MongoMock (fake DB).
    """

    app = create_app(config_class=TestingConfig)
    return app


@pytest.fixture(autouse=True)
def clean_users_collection():
    """Clear users between tests to keep state isolated."""

    repo = UserRepository()
    repo.collection.delete_many({})
    yield
    repo.collection.delete_many({})


@pytest.fixture(scope="function")
def client(app):
    """
    Creates a test client (browser simulator) for sending HTTP requests.
    """

    with app.test_client() as client:
        with app.app_context():
            yield client
