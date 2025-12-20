from app.models.user import UserRegister
from app.repositories.user_repo import UserRepository
from app.services import AuthService


def test_register_endpoint_creates_user_and_redirects(client):
    response = client.post(
        "/auth/register",
        data={
            "name": "Route User",
            "email": "routeuser@example.com",
            "password": "ValidPass3!",
            "phone": "5551234567",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "/auth/login" in response.headers.get("Location", "")

    stored = UserRepository().get_by_email("routeuser@example.com")
    assert stored is not None


def test_login_endpoint_sets_access_cookie(client):
    AuthService().register_user(
        UserRegister(
            name="Cookie User",
            email="cookie@example.com",
            password="ValidPass4!",
        )
    )

    response = client.post(
        "/auth/login",
        data={"email": "cookie@example.com", "password": "ValidPass4!"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "/dashboard/" in response.headers.get("Location", "")
    assert "access_token_cookie=" in response.headers.get("Set-Cookie", "")


def test_login_endpoint_invalid_credentials(client):
    response = client.post(
        "/auth/login",
        data={"email": "missing@example.com", "password": "WrongPass1!"},
        follow_redirects=False,
    )

    assert response.status_code == 401
    assert response.status_code == 401
    assert "Invalid email or password" in response.get_data(as_text=True)
