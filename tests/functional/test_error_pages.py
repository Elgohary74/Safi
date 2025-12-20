from app.models.user import UserRegister
from app.services import AuthService


def test_app_error_renders_html(client):
    # Register/Login

    email = "error_test@example.com"
    AuthService().register_user(
        UserRegister(name="Error User", email=email, password="Password123!")
    )
    client.post(
        "/auth/login",
        data={"email": email, "password": "Password123!"},
    )

    # Hit /groups/nonresident_id/members
    resp = client.get("/groups/nonexistent_id/members")

    # It should be 404 status
    assert resp.status_code == 404

    # It should be HTML
    assert "text/html" in resp.content_type

    # It should contain content from error.html
    # e.g. "Error 404" or "Resource not found"
    text = resp.get_data(as_text=True)
    assert "Error 404" in text
    assert "Resource not found" in text
