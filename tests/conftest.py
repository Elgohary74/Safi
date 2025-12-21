import os

import pytest

from app import create_app
from app.config import TestingConfig
from app.repositories.user_repo import UserRepository


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

    # Reset MongoDatabase singleton to force re-initialization with new env vars
    from app.services.database import MongoDatabase

    MongoDatabase._instance = None
    MongoDatabase._client = None
    MongoDatabase._db = None
    MongoDatabase._initialized = False

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


class AuthActions:
    def __init__(self, client):
        self._client = client
        self._current_email = None

    def login(self, email="test@example.com", password="ValidPass1!"):
        self._current_email = email
        return self._client.post(
            "/auth/login",
            data={"email": email, "password": password},
            follow_redirects=True,
        )

    def register(
        self,
        email="test@example.com",
        name="Test User",
        password="ValidPass1!",
        phone="1234567890",
    ):
        self._current_email = email
        return self._client.post(
            "/auth/register",
            data={"email": email, "name": name, "password": password, "phone": phone},
            follow_redirects=True,
        )

    def logout(self):
        self._current_email = None
        return self._client.get("/auth/logout", follow_redirects=True)

    def get_current_user(self):
        if not self._current_email:
            return None
        return UserRepository().get_by_email(self._current_email)


@pytest.fixture
def auth_client(client):
    return AuthActions(client)
