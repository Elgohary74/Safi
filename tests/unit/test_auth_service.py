import pytest
from werkzeug.security import check_password_hash

from app.models.user import UserRegister
from app.repositories.user_repo import UserRepository
from app.services import AuthService
from app.utils.exceptions import AuthenticationError


@pytest.fixture
def auth_service():
    return AuthService()


def test_register_user_persists_hashed_password(auth_service):
    data = UserRegister(
        name="Test User",
        email="user@example.com",
        password="ValidPass1!",
        phone_number="1234567890",
    )

    user = auth_service.register_user(data)

    assert user.email == data.email
    assert check_password_hash(user.password_hash, data.password)

    stored = UserRepository().get_by_email(data.email)
    assert stored is not None
    assert stored.user_id == user.user_id


def test_register_user_duplicate_email_raises(auth_service):
    data = UserRegister(
        name="Dup User",
        email="dup@example.com",
        password="Another1!",
    )

    auth_service.register_user(data)

    with pytest.raises(AuthenticationError, match="already exists"):
        auth_service.register_user(data)


def test_authenticate_user_returns_token(auth_service, monkeypatch):
    data = UserRegister(
        name="Login User",
        email="login@example.com",
        password="StrongPass1!",
    )
    registered = auth_service.register_user(data)

    monkeypatch.setattr(
        "app.services.auth.create_access_token", lambda identity: f"token-{identity}"
    )

    user, token = auth_service.authenticate_user(data.email, data.password)

    assert user.user_id == registered.user_id
    assert token == f"token-{registered.user_id}"


def test_authenticate_user_invalid_password(auth_service):
    data = UserRegister(
        name="Wrong Password",
        email="wrongpass@example.com",
        password="ValidPass2!",
    )
    auth_service.register_user(data)

    with pytest.raises(AuthenticationError, match="Invalid email or password"):
        auth_service.authenticate_user(data.email, "BadPass1!")
