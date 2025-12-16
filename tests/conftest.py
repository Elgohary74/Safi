import pytest

from app import create_app
from app.config import TestingConfig


@pytest.fixture(scope="session")
def app():
    """
    Creates the Flask application for the entire test session.
    Uses TestingConfig to ensure we use MongoMock (fake DB).
    """

    app = create_app(config_class=TestingConfig)
    return app


@pytest.fixture(scope="function")
def client(app):
    """
    Creates a test client (browser simulator) for sending HTTP requests.
    """

    with app.test_client() as client:
        # Establish an application context
        with app.app_context():
            yield client
